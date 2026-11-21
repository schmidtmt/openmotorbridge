#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_system.h"
#include "driver/gpio.h"
#include "driver/uart.h"
#include "omm_module_config.h"
#include "es8388_codec.h"
#include "omm_ble_service.h"
#include "power_supervisor.h"
#include "omm_transceiver.h"
#include "keypad_indicator.h"
#include "usb_vehicle_backbone.h"
#include "usb_backbone_types.h"

static const char *TAG = "OMM_TRIBAND";

static uint8_t s_current_volume = 80; // 80% default volume
static bool s_sa818_present = false;
static bool s_pod_docked_mode = false;

// Probe U3 (NiceRF SA818-DMR on Pad 16..20 / GPIO 14..18) at boot
static bool probe_sa818_446mhz_module(void) {
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << OMM_PIN_SA818_PTT) | (1ULL << OMM_PIN_SA818_PWR_HL),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&io_conf);
    gpio_set_level(OMM_PIN_SA818_PTT, 1);    // Idle RX
    gpio_set_level(OMM_PIN_SA818_PWR_HL, 0); // 0.2W Helmet SAR-Safe default

    uart_config_t uart_cfg = {
        .baud_rate = 9600,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };
    if (uart_param_config(UART_NUM_1, &uart_cfg) != ESP_OK) return false;
    uart_set_pin(UART_NUM_1, OMM_PIN_SA818_TXD, OMM_PIN_SA818_RXD, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    if (uart_driver_install(UART_NUM_1, 512, 0, 0, NULL, 0) != ESP_OK) return false;

    const char *cmd = "AT+DMOCONNECT\r\n";
    uart_write_bytes(UART_NUM_1, cmd, strlen(cmd));
    char resp[32] = {0};
    int len = uart_read_bytes(UART_NUM_1, (uint8_t*)resp, sizeof(resp) - 1, pdMS_TO_TICKS(150));
    if (len > 0 && strstr(resp, "+DMOCONNECT:0") != nullptr) {
        ESP_LOGI(TAG, "✓ U3 NiceRF SA818-DMR detected on GPIO 14/15 -> Full Tri-Band Mode (2.4G + BT + 446MHz PMR/DMR)");
        return true;
    }
    ESP_LOGI(TAG, "U3 SA818-DMR not populated (PCBA 09 variant) -> Dual-Engine Mode (2.4G Mesh + BT Bridge)");
    return false;
}

// Audio RX callback from 2.4 GHz Mesh -> Headphone DAC & Pod USB-Audio Upstream
static void on_mesh_audio_received(const int16_t *audio_data, size_t samples, uint8_t sender_id) {
    (void)sender_id;
    indicator_set_mode(LED_MODE_RX_CYAN);
    size_t written = 0;
    es8388_write_audio(audio_data, samples, &written);

    // If docked in Satellite Pod PCBA 03 (VBUS present on J1), also stream digital PCM over USB Backbone
    if (s_pod_docked_mode && audio_data && samples > 0) {
        UsbAudioStreamUpPkt up_pkt = {};
        static uint16_t s_up_seq = 0;
        up_pkt.frame_seq = ++s_up_seq;
        up_pkt.status_flags = USB_AUDIO_UP_FLAG_STREAM_ACTIVE | USB_AUDIO_UP_FLAG_OMM_DIGITAL | USB_AUDIO_UP_FLAG_MESH_VOICE;
        if (s_sa818_present && gpio_get_level(OMM_PIN_SA818_SQL) == 0) {
            up_pkt.status_flags |= USB_AUDIO_UP_FLAG_FUNK_CARRIER;
        }
        if (omm_transceiver_is_ptt()) {
            up_pkt.status_flags |= USB_AUDIO_UP_FLAG_PTT_PRESSED;
        }

        up_pkt.sample_count = 0; // 0 denotes multistream layout
        up_pkt.multistream.rssi_dbm = 65; // Nominal -65 dBm
        up_pkt.multistream.voice_mesh_count = static_cast<uint8_t>(samples > USB_OMM_UP_VOICE_SAMPLES ? USB_OMM_UP_VOICE_SAMPLES : samples);
        memcpy(up_pkt.multistream.sub_voice_mesh, audio_data, up_pkt.multistream.voice_mesh_count * sizeof(int16_t));

        // If SA818 446 MHz squelch is open, populate sub_voice_funk from carrier audio
        if (up_pkt.status_flags & USB_AUDIO_UP_FLAG_FUNK_CARRIER) {
            up_pkt.multistream.voice_funk_count = up_pkt.multistream.voice_mesh_count;
            for (size_t f = 0; f < up_pkt.multistream.voice_funk_count; f++) {
                up_pkt.multistream.sub_voice_funk[f] = audio_data[f];
            }
        }

        UsbVehicleBackbone::instance().send_packet(USB_NODE_CENTRAL_BOX, USB_PKT_AUDIO_STREAM_UP,
                                                   &up_pkt, sizeof(up_pkt));
    }
}

// Task 1: Real-Time Audio Capture & Broadcast Task (Core 0, Priority 10)
static void audio_processing_task(void *pvParameters) {
    int16_t mic_buf[OMM_AUDIO_FRAME_SAMPLES];

    ESP_LOGI(TAG, "Audio processing task running (Frame: %d samples, %d ms)...",
             OMM_AUDIO_FRAME_SAMPLES, OMM_AUDIO_FRAME_MS);

    while (1) {
        size_t samples_read = 0;
        esp_err_t ret = es8388_read_audio(mic_buf, OMM_AUDIO_FRAME_SAMPLES, &samples_read);
        if (ret == ESP_OK && samples_read > 0) {
            if (omm_transceiver_is_ptt()) {
                omm_transceiver_send_audio(mic_buf, samples_read);
                if (s_sa818_present) {
                    gpio_set_level(OMM_PIN_SA818_PTT, 0); // Key SA818 446 MHz PTT in Combi/Bridge mode
                }
            } else if (s_sa818_present) {
                gpio_set_level(OMM_PIN_SA818_PTT, 1);
            }
        }
        vTaskDelay(pdMS_TO_TICKS(5));
    }
}

// Task 2: Supervision, Keypad, Pod-Dock Auto-Sense & Battery Management Task (Core 0, Priority 3)
static void supervision_task(void *pvParameters) {
    ESP_LOGI(TAG, "Supervision & Keypad task running...");

    while (1) {
        // 1. Poll Keypad Events (SW1..SW4 on GPIO 2, 3, 4, 5 & J_HELMET Pin 6 BTN_PTT)
        OmmKeyEvent_t evt = keypad_poll_events();
        switch (evt) {
            case KEY_EVENT_POWER_SHORT:
                omm_transceiver_set_ptt(!omm_transceiver_is_ptt());
                indicator_set_mode(omm_transceiver_is_ptt() ? LED_MODE_TX_BLUE : LED_MODE_STANDBY_GREEN);
                break;

            case KEY_EVENT_POWER_LONG:
                ESP_LOGI(TAG, "Power button long press detected -> powering down");
                indicator_set_mode(LED_MODE_OFF);
                vTaskDelay(pdMS_TO_TICKS(500));
                power_enter_deep_sleep();
                break;

            case KEY_EVENT_MESH_TOGGLE: {
                OmmMeshState_t current = omm_transceiver_get_mesh_mode();
                OmmMeshState_t next = (current == OMM_MESH_OPEN_GROUP) ? OMM_MESH_PRIVATE_GROUP : OMM_MESH_OPEN_GROUP;
                omm_transceiver_set_mesh_mode(next);
                indicator_set_mode(next == OMM_MESH_PRIVATE_GROUP ? LED_MODE_GROUP_PURPLE : LED_MODE_STANDBY_GREEN);
                ESP_LOGI(TAG, "Switched Mesh Mode -> %s", next == OMM_MESH_PRIVATE_GROUP ? "PRIVATE GROUP" : "OPEN CONVOY");
                break;
            }

            case KEY_EVENT_VOL_UP:
                if (s_current_volume <= 90) s_current_volume += 10;
                else s_current_volume = 100;
                es8388_set_volume(s_current_volume);
                ESP_LOGI(TAG, "Volume UP: %d%%", s_current_volume);
                break;

            case KEY_EVENT_VOL_DOWN:
                if (s_current_volume >= 10) s_current_volume -= 10;
                else s_current_volume = 0;
                es8388_set_volume(s_current_volume);
                ESP_LOGI(TAG, "Volume DOWN: %d%%", s_current_volume);
                break;

            case KEY_EVENT_NONE:
            default:
                break;
        }

        // 2. Poll Battery & Pod-Dock Status every 500 ms
        static int cycle = 0;
        if (++cycle >= 25) {
            cycle = 0;
            OmmPowerStatus_t pwr = {};
            power_supervisor_poll(&pwr);
            if (pwr.battery_pct < 15 && !pwr.is_charging) {
                indicator_set_mode(LED_MODE_WARN_YELLOW);
            }

            // Auto-switch SA818 RF Power (0.2W SAR-Safe Helmet vs. 0.5W Bike Pod Mode when VBUS present)
            if (pwr.is_vbus_present != s_pod_docked_mode) {
                s_pod_docked_mode = pwr.is_vbus_present;
                if (s_sa818_present) {
                    gpio_set_level(OMM_PIN_SA818_PWR_HL, s_pod_docked_mode ? 1 : 0);
                }
                ESP_LOGI(TAG, "OMM Operating Context -> %s (%s)",
                         s_pod_docked_mode ? "DOCKED IN POD PCBA 03 (Digital USB-Audio & 0.5W RF)" :
                                             "AUTONOMOUS UCS HELMET (1000mAh LiPo & 0.2W SAR-Safe)",
                         s_sa818_present ? "Tri-Band" : "Dual-Engine");
            }

            OmmBleTelemetry_t telem = {
                .battery_pct = pwr.battery_pct,
                .is_charging = static_cast<uint8_t>(pwr.is_charging ? 1 : 0),
                .vbus_mv = static_cast<uint16_t>(pwr.is_vbus_present ? 5000 : 0),
                .vbat_mv = static_cast<uint16_t>(pwr.v_bat * 1000.0f),
                .mesh_rssi_dbm = -65,
                .connected_peers = 1
            };
            omm_ble_notify_telemetry(&telem);

            if (s_pod_docked_mode) {
                UsbVehicleBackbone::instance().send_heartbeat(telem.vbus_mv, pwr.is_charging ? 350 : 120);
            }
        }

        vTaskDelay(pdMS_TO_TICKS(20));
    }
}

extern "C" void app_main(void) {
    ESP_LOGI(TAG, "==========================================================");
    ESP_LOGI(TAG, "  OpenMotorMesh (OMM) Unified Tri-Band Intercom (PCBA 10) ");
    ESP_LOGI(TAG, "  2.4 GHz Mesh (U1) + BT Co-Proc (U6) + 446 MHz DMR (U3)  ");
    ESP_LOGI(TAG, "  ECE 22.06 UCS Helmet & Digital USB-Audio Pod Firmware   ");
    ESP_LOGI(TAG, "  Firmware: %s | Target: ESP32-C6-MINI-1U     ", OMM_FW_VERSION_STRING);
    ESP_LOGI(TAG, "==========================================================");

    // 1. Initialize Subsystems
    ESP_ERROR_CHECK(power_supervisor_init());
    ESP_ERROR_CHECK(keypad_indicator_init());
    ESP_ERROR_CHECK(es8388_codec_init());
    ESP_ERROR_CHECK(omm_transceiver_init(on_mesh_audio_received));

    // 2. Auto-detect NiceRF SA818-DMR 446 MHz module (U3 on GPIO 14..18)
    s_sa818_present = probe_sa818_446mhz_module();

    // 3. Initialize J1 USB-C Digital Audio & Central Bus-DFU Listener (GPIO 12/13)
    usb_backbone_hw_config_t usb_cfg = {
        .pin_usb_dm     = OMM_PIN_USB_DN,
        .pin_usb_dp     = OMM_PIN_USB_DP,
        .hub_port_id    = USB_HUB_PORT_3_POD_BAY1,
        .high_speed_phy = false
    };
    UsbVehicleBackbone::instance().init(USB_NODE_OMM_MODULE_1, &usb_cfg);
    UsbVehicleBackbone::instance().set_generic_packet_callback(
        [](UsbBackbonePktType type, const uint8_t* payload, size_t len, UsbNodeType source) {
            (void)source;
            if (type == USB_PKT_AUDIO_STREAM_DOWN && len >= sizeof(UsbAudioStreamDownPkt)) {
                const UsbAudioStreamDownPkt* down = reinterpret_cast<const UsbAudioStreamDownPkt*>(payload);

                // 1. Driver Handlebar PTT towards 446 MHz PMR/DMR Funk: Key SA818 PTT
                if ((down->flags & USB_AUDIO_FLAG_PTT_ACTIVE) && (down->flags & USB_AUDIO_FLAG_TARGET_FUNK)) {
                    if (s_sa818_present) {
                        gpio_set_level(OMM_PIN_SA818_PTT, 0); // Key SA818 446 MHz PTT for TX
                    }
                } else if (s_sa818_present) {
                    gpio_set_level(OMM_PIN_SA818_PTT, 1); // Release SA818 PTT to RX
                }

                // 2. Transmit to 2.4 GHz Mesh
                // Note: If Pillion Private Whisper is active (USB_AUDIO_FLAG_PILLION_WHISPER),
                // pillion microphone is already muted by Central Box DSP (only driver transmitted).
                if (omm_transceiver_is_ptt() || (down->flags & USB_AUDIO_FLAG_VOICE_ACTIVE)) {
                    int16_t voice_buf[USB_AUDIO_DOWN_VOICE_SAMPLES];
                    memcpy(voice_buf, down->sub_voice, sizeof(voice_buf));
                    omm_transceiver_send_audio(voice_buf, USB_AUDIO_DOWN_VOICE_SAMPLES);
                }
            }
        });
    UsbVehicleBackbone::instance().start_task(18, 0);

    // 4. Initialize BLE 5.3 GATT Server (Remote Control & LE Audio LC3 profile)
    ESP_ERROR_CHECK(omm_ble_service_init([](uint16_t char_uuid, const uint8_t *data, size_t len) {
        if (!data || len == 0) return;
        switch (char_uuid) {
            case OMM_CHAR_UUID_PTT:
                omm_transceiver_set_ptt(data[0] != 0);
                indicator_set_mode(omm_transceiver_is_ptt() ? LED_MODE_TX_BLUE : LED_MODE_STANDBY_GREEN);
                break;
            case OMM_CHAR_UUID_MESH_MODE:
                omm_transceiver_set_mesh_mode(data[0] != 0 ? OMM_MESH_PRIVATE_GROUP : OMM_MESH_OPEN_GROUP);
                indicator_set_mode(data[0] != 0 ? LED_MODE_GROUP_PURPLE : LED_MODE_STANDBY_GREEN);
                break;
            case OMM_CHAR_UUID_VOLUME:
                s_current_volume = data[0] > 100 ? 100 : data[0];
                es8388_set_volume(s_current_volume);
                break;
            default:
                break;
        }
    }));

    // Set initial volume & mic gain
    es8388_set_volume(s_current_volume);
    es8388_set_mic_gain(18); // +18 dB for helmet boom mic on J_HELMET Pin 4

    // 5. Spawn FreeRTOS Tasks
    xTaskCreate(audio_processing_task, "audio_task", 4096, NULL, 10, NULL);
    xTaskCreate(supervision_task, "supervision_task", 3072, NULL, 3, NULL);

    ESP_LOGI(TAG, "✓ OMM Unified Tri-Band UCS Intercom Module v10.0 boot sequence complete.");
}
