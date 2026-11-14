#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_system.h"
#include "esp_mac.h"
#include "driver/gpio.h"

#include "cartridge_config.h"
#include "cartridge_mechatronics.h"
#include "cartridge_audio_codec.h"
#include "cartridge_ble_profile.h"
#include "cartridge_ble_client.h"
#include "usb_vehicle_backbone.h"
#include "usb_backbone_types.h"

static const char* TAG = "POD_INTERFACE";

static UsbNodeType s_local_bay_node = USB_NODE_POD_BAY1;
static uint16_t s_model_id = 0x0101; // Default: Sena SPIDER X Slim (Klasse A) / OMM Tri-Band (0x0401)
static bool s_omm_digital_mode = false;
static bool s_ptt_pressed = false;

// -----------------------------------------------------------------------------
// Detect Bay ID from Hardware Strap & OMM_DETECT Mode (`U4` TS5A3159 Auto-Sense)
// -----------------------------------------------------------------------------
static UsbNodeType detect_bay_and_mode() {
    gpio_config_t conf = {
        .pin_bit_mask = (1ULL << PIN_BAY_SELECT) |
                        (1ULL << PIN_OMM_DETECT) |
                        (1ULL << PIN_POD_PTT_BTN),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&conf);

    // 1. Check OMM_DETECT (U1 Pad 16 / GPIO 14 -> J_AUDIO_PWR Pin 6 & U4 TS5A3159 IN):
    //    LOW (0V):    OEM Harness grounds Pin 6 -> U4 stays on NC (ES8388 Analog Voice Out)
    //    HIGH (3.3V): OMM Module leaves Pin 6 open (R9 10k pull-up) -> U4 switches to NO (Digital USB-Audio)
    int omm_lvl = gpio_get_level(PIN_OMM_DETECT);
    s_omm_digital_mode = (omm_lvl != 0);
    if (s_omm_digital_mode) {
        s_model_id = 0x0401; // OMM Universal Tri-Band Module (PCBA 09/10)
        ESP_LOGI(TAG, "OMM_DETECT (GPIO 14) is HIGH -> U4 TS5A3159 in DIGITAL USB-AUDIO Mode (OMM Tri-Band 0x0401)");
    } else {
        s_model_id = 0x0101; // Analog OEM Intercom (Sena / Cardo / Midland via ES8388 + Q1..Q4 Actuators)
        ESP_LOGI(TAG, "OMM_DETECT (GPIO 14) is LOW  -> U4 TS5A3159 in ANALOG ES8388 Mode (OEM Intercom 0x0101)");
    }

    // 2. Check Bay Strap (GPIO 2): LOW = Pod 1 Left (0x03), HIGH = Pod 2 Right (0x04)
    int bay_lvl = gpio_get_level(PIN_BAY_SELECT);
    if (bay_lvl == 0) {
        ESP_LOGI(TAG, "Hardware Bay Detect: GPIO %d is LOW -> Assigning POD BAY 1 (Links, 0x03)", PIN_BAY_SELECT);
        return USB_NODE_POD_BAY1;
    } else {
        ESP_LOGI(TAG, "Hardware Bay Detect: GPIO %d is HIGH -> Assigning POD BAY 2 (Rechts, 0x04)", PIN_BAY_SELECT);
        return USB_NODE_POD_BAY2;
    }
}

// -----------------------------------------------------------------------------
// Send Pod Announce Frame to Central Box over 4-Wire USB Backbone
// -----------------------------------------------------------------------------
static void send_pod_announce() {
    uint64_t uid = 0;
    esp_read_mac(reinterpret_cast<uint8_t*>(&uid), ESP_MAC_WIFI_STA);

    uint8_t class_id = s_omm_digital_mode ? 0x04 : 0x01;
    ESP_LOGI(TAG, "Broadcasting Pod Announce via USB Backbone: Class=0x%02X, Model=0x%04X, OMM_Digital=%d, UID=0x%016llX",
             class_id, s_model_id, s_omm_digital_mode ? 1 : 0, (unsigned long long)uid);

    UsbVehicleBackbone::instance().send_cartridge_announce(class_id, s_model_id, uid, 5000);
}

// Active BLE Profile Configuration (for local OEM headset GATT remote control)
static CartridgeBleConfig_t s_active_ble_config = {
    .supported = true,
    .flavor = BLE_FLAVOR_SENA_RC_GATT,
    .device_prefix = "SPIDER",
    .service_uuid = 0xFFE0,
    .fallback_to_mechatronics_on_disconnect = true,
    .can_power_boot = false, // Cold-boot always uses physical mechatronics (Q1..Q4)
    .can_power_off = true,
    .can_mesh_toggle = true,
    .can_group_toggle = true,
    .can_volume = true,
    .can_channel_select = true,
    .can_mic_mute = true,
    .can_telemetry = true,
    .can_le_audio_lc3 = false
};

static esp_err_t execute_smart_command(uint8_t opcode, uint16_t duration_ms) {
    // 1. Power Boot (0x01) ALWAYS requires physical Mechatronics on OEM headsets
    if (opcode == CARTRIDGE_OPCODE_POWER_BOOT && !s_omm_digital_mode) {
        ESP_LOGI(TAG, "⚡ Power Boot (0x01) -> Enforcing physical Mechatronic actuator pulse (Q1..Q4).");
        esp_err_t err = CartridgeMechatronics::instance().execute_opcode(opcode, duration_ms);
        CartridgeBleClient::instance().trigger_connect();
        return err;
    }

    // 2. Primary Path: Use digital BLE GATT command if available and connected
    if (CartridgeBleClient::instance().is_connected()) {
        esp_err_t ble_err = CartridgeBleClient::instance().send_command(opcode);
        if (ble_err == ESP_OK) {
            ESP_LOGI(TAG, "✓ Opcode 0x%02X executed via BLE (< 5 ms, 0 mechanical wear).", opcode);
            return ESP_OK;
        }
        ESP_LOGW(TAG, "⚠️ BLE command TX returned error (0x%X) -> Falling back to physical click sequence!", ble_err);
    }

    // 3. Mechatronic Fallback Path (Q1..Q4 AO3400A on J_ACT)
    ESP_LOGI(TAG, "🔧 Executing physical Mechatronic click sequence for Opcode 0x%02X.", opcode);
    return CartridgeMechatronics::instance().execute_opcode(opcode, duration_ms);
}

// -----------------------------------------------------------------------------
// Opcode Execution Callback (Dispatched from Central Box via USB Backbone)
// -----------------------------------------------------------------------------
static void on_pod_opcode_received(const UsbPodOpcodePkt& op, UsbNodeType source) {
    ESP_LOGI(TAG, "USB Opcode RX from 0x%02X: Opcode=0x%02X, Pulse=%u ms",
             (uint8_t)source, op.opcode, op.pulse_duration_ms);

    esp_err_t err = execute_smart_command(op.opcode, op.pulse_duration_ms);

    uint16_t exec_us = static_cast<uint16_t>((op.pulse_duration_ms > 0 ? op.pulse_duration_ms : 150) * 1000);
    uint8_t act_mask = CartridgeMechatronics::instance().get_active_mask();
    uint8_t result = (err == ESP_OK) ? 0x00 : 0x01;

    UsbVehicleBackbone::instance().send_cartridge_ack(USB_NODE_CENTRAL_BOX,
                                                      op.seq_token,
                                                      op.opcode,
                                                      result,
                                                      act_mask,
                                                      exec_us);
}

static void on_generic_packet_received(UsbBackbonePktType type, const uint8_t* payload, size_t len, UsbNodeType source) {
    (void)source;
    if (type == USB_PKT_AUDIO_STREAM_DOWN && len >= sizeof(UsbAudioStreamDownPkt)) {
        const UsbAudioStreamDownPkt* down = reinterpret_cast<const UsbAudioStreamDownPkt*>(payload);

        // In Analog OEM Mode (OMM_DETECT == LOW), route voice & stereo media to ES8388 DAC
        if (!s_omm_digital_mode) {
            int16_t voice_buf[USB_AUDIO_DOWN_VOICE_SAMPLES];
            memcpy(voice_buf, down->sub_voice, sizeof(voice_buf));
            CartridgeAudioCodec::instance().write_voice_mic(voice_buf, USB_AUDIO_DOWN_VOICE_SAMPLES);

            int16_t music_l_buf[USB_AUDIO_DOWN_MUSIC_SAMPLES];
            int16_t music_r_buf[USB_AUDIO_DOWN_MUSIC_SAMPLES];
            memcpy(music_l_buf, down->sub_music_l, sizeof(music_l_buf));
            memcpy(music_r_buf, down->sub_music_r, sizeof(music_r_buf));
            CartridgeAudioCodec::instance().push_music_samples(music_l_buf, music_r_buf, USB_AUDIO_DOWN_MUSIC_SAMPLES);
        }
    }
}

// -----------------------------------------------------------------------------
// Real-Time Audio Upstream Task (Intercom Headset Out -> USB Central Box)
// -----------------------------------------------------------------------------
static void pod_audio_upstream_task(void* pvParameters) {
    ESP_LOGI(TAG, "Pod Audio Upstream Task started (100 Hz over USB 2.0 Backbone)");
    int16_t rx_buf[USB_AUDIO_UP_SAMPLES];
    uint16_t up_seq = 0;

    while (1) {
        if (!s_omm_digital_mode) {
            size_t samples_read = CartridgeAudioCodec::instance().read_audio_frames(rx_buf, USB_AUDIO_UP_SAMPLES);
            if (samples_read > 0) {
                UsbAudioStreamUpPkt up_pkt = {};
                up_pkt.frame_seq = ++up_seq;
                up_pkt.status_flags = s_ptt_pressed ? 0x03 : 0x01; // Bit 0 = stream active, Bit 1 = PTT pressed
                up_pkt.sample_count = static_cast<uint8_t>(samples_read > USB_AUDIO_UP_SAMPLES ? USB_AUDIO_UP_SAMPLES : samples_read);
                memcpy(up_pkt.samples, rx_buf, up_pkt.sample_count * sizeof(int16_t));

                UsbVehicleBackbone::instance().send_packet(USB_NODE_CENTRAL_BOX, USB_PKT_AUDIO_STREAM_UP,
                                                           &up_pkt, sizeof(up_pkt));
            }
        }
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

// -----------------------------------------------------------------------------
// Supervisor, OMM_DETECT Auto-Sense & Mechatronics Task (50 Hz)
// -----------------------------------------------------------------------------
static void pod_supervisor_task(void* pvParameters) {
    ESP_LOGI(TAG, "Pod Supervisor Task started (50 Hz)");
    TickType_t last_wake = xTaskGetTickCount();
    uint32_t heartbeat_counter = 0;

    while (1) {
        // 1. Advance mechatronics pulse state machine (Q1..Q4 AO3400A on GPIO 18, 19, 4, 5)
        CartridgeMechatronics::instance().update();

        // 2. BLE Central connection supervision & reconnect
        CartridgeBleClient::instance().update();

        // 3. Live hot-plug check on OMM_DETECT (GPIO 14) & PTT_BTN (GPIO 9)
        bool omm_now = (gpio_get_level(PIN_OMM_DETECT) != 0);
        if (omm_now != s_omm_digital_mode) {
            s_omm_digital_mode = omm_now;
            s_model_id = s_omm_digital_mode ? 0x0401 : 0x0101;
            ESP_LOGI(TAG, "OMM_DETECT hot-plug change -> Mode is now %s",
                     s_omm_digital_mode ? "DIGITAL USB-AUDIO (OMM)" : "ANALOG ES8388 (OEM Headset)");
            send_pod_announce();
        }
        s_ptt_pressed = (gpio_get_level(PIN_POD_PTT_BTN) == 0);

        // 4. Periodic USB Heartbeat & 30W SW3516 VBUS Status (every 500 ms)
        heartbeat_counter++;
        if (heartbeat_counter >= 25) { // 25 * 20 ms = 500 ms
            heartbeat_counter = 0;
            UsbVehicleBackbone::instance().send_heartbeat(5000, s_omm_digital_mode ? 250 : 120);
        }

        vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(20)); // 50 Hz / 20 ms
    }
}

// -----------------------------------------------------------------------------
// Main Application Entry Point
// -----------------------------------------------------------------------------
extern "C" void app_main(void) {
    ESP_LOGI(TAG, "============================================================");
    ESP_LOGI(TAG, "   OPENMOTORBRIDGE SATELLITE POD INTERFACE v10.0 (PCBA 03)  ");
    ESP_LOGI(TAG, "   Target: ESP32-C6-MINI-1U + SW3516 30W PD + ES8388 + U4   ");
    ESP_LOGI(TAG, "   4-Wire USB 2.0 Automotive Backbone & Central Bus-DFU     ");
    ESP_LOGI(TAG, "============================================================");

    // 1. Detect Bay (Pod 1 Left or Pod 2 Right) & OMM_DETECT Mode (U4 TS5A3159)
    s_local_bay_node = detect_bay_and_mode();

    // 2. Initialize Mechatronics Actuator Gates (Q1-Q4 AO3400A on GPIO 18, 19, 4, 5)
    CartridgeMechatronics::instance().init();

    // 3. Initialize Audio Codec (ES8388 on I2C GPIO 23/15, I2S GPIO 16/17/20/21/22)
    CartridgeAudioCodec::instance().init();

    // 4. Initialize BLE Client Subsystem & apply initial profile config
    CartridgeBleClient::instance().init();
    CartridgeBleClient::instance().configure(s_active_ble_config);

    // 5. Initialize 4-Wire USB 2.0 Automotive Backbone (J_BUS: USB D- GPIO 12, D+ GPIO 13)
    UsbHubPortId hub_port = (s_local_bay_node == USB_NODE_POD_BAY1) ?
                            USB_HUB_PORT_3_POD_BAY1 : USB_HUB_PORT_4_POD_BAY2;
    usb_backbone_hw_config_t usb_cfg = {
        .pin_usb_dm     = PIN_POD_USB_DM,
        .pin_usb_dp     = PIN_POD_USB_DP,
        .hub_port_id    = hub_port,
        .high_speed_phy = false
    };

    UsbVehicleBackbone::instance().init(s_local_bay_node, &usb_cfg);
    UsbVehicleBackbone::instance().set_cartridge_opcode_callback(on_pod_opcode_received);
    UsbVehicleBackbone::instance().set_generic_packet_callback(on_generic_packet_received);
    UsbVehicleBackbone::instance().start_task(22, 0);

    // 6. Send initial Announce frame to Central Box
    send_pod_announce();

    // 7. Spawn Supervisor Task & Real-Time Audio Upstream Task
    xTaskCreate(pod_supervisor_task, "pod_sup", 3072, NULL, 5, NULL);
    xTaskCreate(pod_audio_upstream_task, "pod_audio_up", 4096, NULL, 10, NULL);

    ESP_LOGI(TAG, "Satellite Pod PCBA 03 v10.0 operational in %s (%s).",
             s_local_bay_node == USB_NODE_POD_BAY1 ? "POD BAY 1 (Links)" : "POD BAY 2 (Rechts)",
             s_omm_digital_mode ? "Digital OMM Mode" : "Analog OEM Mode");
}
