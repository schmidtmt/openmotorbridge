#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_system.h"
#include "omm_module_config.h"
#include "es8388_codec.h"
#include "omm_ble_service.h"
#include "power_supervisor.h"
#include "omm_transceiver.h"
#include "keypad_indicator.h"

static const char *TAG = "OMM_MAIN";

static uint8_t s_current_volume = 80; // 80% default volume

// Audio RX callback from 2.4 GHz Mesh -> Headphone DAC
static void on_mesh_audio_received(const int16_t *audio_data, size_t samples, uint8_t sender_id) {
    indicator_set_mode(LED_MODE_RX_CYAN);
    size_t written = 0;
    es8388_write_audio(audio_data, samples, &written);
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
            // Check if PTT is active
            if (omm_transceiver_is_ptt()) {
                omm_transceiver_send_audio(mic_buf, samples_read);
            }
        }
        vTaskDelay(pdMS_TO_TICKS(5));
    }
}

// Task 2: Supervision, Keypad & Battery Management Task (Core 0, Priority 3)
static void supervision_task(void *pvParameters) {
    ESP_LOGI(TAG, "Supervision & Keypad task running...");

    while (1) {
        // 1. Poll Keypad Events
        OmmKeyEvent_t evt = keypad_poll_events();
        switch (evt) {
            case KEY_EVENT_POWER_SHORT:
                // Toggle PTT Transmit
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

        // 2. Poll Battery Status every 500 ms
        // 2. Poll Battery Status every 500 ms and notify BLE Central
        static int cycle = 0;
        if (++cycle >= 25) {
            cycle = 0;
            OmmPowerStatus_t pwr = {};
            power_supervisor_poll(&pwr);
            if (pwr.battery_pct < 15 && !pwr.is_charging) {
                indicator_set_mode(LED_MODE_WARN_YELLOW);
            }

            OmmBleTelemetry_t telem = {
                .battery_pct = pwr.battery_pct,
                .is_charging = static_cast<uint8_t>(pwr.is_charging ? 1 : 0),
                .vbus_mv = pwr.vbus_mv,
                .vbat_mv = pwr.vbat_mv,
                .mesh_rssi_dbm = -65,
                .connected_peers = 1
            };
            omm_ble_notify_telemetry(&telem);
        }

        vTaskDelay(pdMS_TO_TICKS(20));
    }
}

extern "C" void app_main(void) {
    ESP_LOGI(TAG, "==========================================================");
    ESP_LOGI(TAG, "  OpenMotorMesh (OMM) 2.4 GHz Intercom Module (PCBA 09)   ");
    ESP_LOGI(TAG, "  ECE 22.06 UCS Autonomous Headset & Cartridge Firmware   ");
    ESP_LOGI(TAG, "  Firmware: %s | Target: ESP32-C6                       ", OMM_FW_VERSION_STRING);
    ESP_LOGI(TAG, "==========================================================");

    // 1. Initialize Subsystems
    ESP_ERROR_CHECK(power_supervisor_init());
    ESP_ERROR_CHECK(keypad_indicator_init());
    ESP_ERROR_CHECK(es8388_codec_init());
    ESP_ERROR_CHECK(omm_transceiver_init(on_mesh_audio_received));

    // 2. Initialize BLE 5.3 GATT Server (Remote Control & LE Audio LC3 profile)
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
    es8388_set_mic_gain(18); // +18 dB for helmet boom mic

    // 3. Spawn FreeRTOS Tasks
    xTaskCreate(audio_processing_task, "audio_task", 4096, NULL, 10, NULL);
    xTaskCreate(supervision_task, "supervision_task", 3072, NULL, 3, NULL);

    ESP_LOGI(TAG, "✓ OMM 2.4 GHz UCS Intercom Module boot sequence complete.");
}
