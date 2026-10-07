#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_system.h"
#include "nvs_flash.h"
#include "omm446_config.h"
#include "sa818_dmr_driver.h"
#include "es8388_codec.h"
#include "keypad_indicator.h"
#include "omm446_ble_service.h"
#include "power_supervisor.h"

static const char *TAG = "OMM446_MAIN";

static uint8_t s_current_volume = 80;

// Squelch / Carrier State Change Callback (called from SA818 driver)
static void on_squelch_changed(bool carrier_active, void *user_ctx) {
    Sa818DmrDriver &radio = Sa818DmrDriver::getInstance();
    const Sa818State_t &state = radio.getState();

    if (carrier_active) {
        // Träger / DMR-Burst erkannt -> Signal aktiv
        indicator_set_mode(state.mode == SA818_MODE_DIGITAL_DMR ?
                           LED_MODE_RX_ACTIVE_DMR : LED_MODE_RX_ACTIVE_ANALOG);
        es8388_set_mute(false);
    } else {
        // Rauschsperre geschlossen -> Standby
        indicator_set_mode(state.mode == SA818_MODE_DIGITAL_DMR ?
                           LED_MODE_RX_STANDBY_DMR : LED_MODE_RX_STANDBY_ANALOG);
        es8388_set_mute(true);
    }
}

// Remote BLE Command Callback (from Cockpit, CarPlay or Handlebar)
static void on_ble_command_received(uint16_t char_uuid, const uint8_t *data, size_t len) {
    if (!data || len == 0) return;
    Sa818DmrDriver &radio = Sa818DmrDriver::getInstance();

    switch (char_uuid) {
        case OMM446_CHAR_UUID_PTT: {
            bool ptt_active = (data[0] != 0);
            radio.setPtt(ptt_active);
            indicator_set_mode(ptt_active ?
                (radio.getState().mode == SA818_MODE_DIGITAL_DMR ? LED_MODE_TX_DMR : LED_MODE_TX_ANALOG) :
                (radio.getState().mode == SA818_MODE_DIGITAL_DMR ? LED_MODE_RX_STANDBY_DMR : LED_MODE_RX_STANDBY_ANALOG));
            omm446_ble_notify_ptt(ptt_active ? 1 : 0);
            break;
        }

        case OMM446_CHAR_UUID_MODE: {
            Sa818RadioMode_t mode = (data[0] == 1) ? SA818_MODE_DIGITAL_DMR : SA818_MODE_ANALOG_FM;
            radio.setRadioMode(mode);
            indicator_set_mode(mode == SA818_MODE_DIGITAL_DMR ? LED_MODE_RX_STANDBY_DMR : LED_MODE_RX_STANDBY_ANALOG);
            omm446_ble_notify_mode(mode);
            break;
        }

        case OMM446_CHAR_UUID_CHANNEL: {
            uint8_t ch = data[0];
            radio.setChannel(ch);
            omm446_ble_notify_channel(ch);
            break;
        }

        case OMM446_CHAR_UUID_CTCSS: {
            uint8_t ctcss = data[0];
            radio.setCtcss(ctcss);
            break;
        }

        case OMM446_CHAR_UUID_DMR_COLOR_CODE: {
            uint8_t cc = data[0];
            radio.setDmrColorCode(cc);
            break;
        }

        case OMM446_CHAR_UUID_SQUELCH: {
            uint8_t sq = data[0];
            radio.setSquelch(sq);
            break;
        }

        case OMM446_CHAR_UUID_POWER_LEVEL: {
            Sa818PowerLevel_t pwr = (data[0] == 1) ? SA818_PWR_HIGH_0_5W : SA818_PWR_LOW_0_2W;
            radio.setPowerLevel(pwr);
            break;
        }

        default:
            ESP_LOGW(TAG, "Unknown BLE Char UUID: 0x%04X", char_uuid);
            break;
    }
}

// Task 1: Real-Time Audio Streaming Task (Core 0, Priority 10)
static void audio_processing_task(void *pvParameters) {
    int16_t audio_buf[OMM446_AUDIO_FRAME_SAMPLES * 2]; // Stereo buffer
    Sa818DmrDriver &radio = Sa818DmrDriver::getInstance();

    ESP_LOGI(TAG, "Audio processing task running (Frame: %d samples, %d Hz)...",
             OMM446_AUDIO_FRAME_SAMPLES, OMM446_AUDIO_SAMPLE_RATE);

    while (1) {
        size_t samples_read = 0;
        esp_err_t ret = es8388_read_audio(audio_buf, OMM446_AUDIO_FRAME_SAMPLES, &samples_read);
        if (ret == ESP_OK && samples_read > 0) {
            // Wenn Senden aktiv ist, gelangt das Mikrofon-Signal an den SA818 MIC-Eingang
            if (radio.getState().is_transmitting) {
                // Audio loopback / processing
            }
        }
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

// Task 2: Supervision, Keypad & Telemetry Task (Core 0, Priority 3)
static void supervision_task(void *pvParameters) {
    ESP_LOGI(TAG, "Supervision & Keypad task running...");
    Sa818DmrDriver &radio = Sa818DmrDriver::getInstance();

    while (1) {
        // 1. Tasten abfragen
        Omm446KeyEvent_t evt = keypad_poll_events();
        switch (evt) {
            case KEY_EVENT_PTT_PRESS:
                radio.setPtt(true);
                indicator_set_mode(radio.getState().mode == SA818_MODE_DIGITAL_DMR ?
                                   LED_MODE_TX_DMR : LED_MODE_TX_ANALOG);
                omm446_ble_notify_ptt(1);
                break;

            case KEY_EVENT_PTT_RELEASE:
                radio.setPtt(false);
                indicator_set_mode(radio.getState().mode == SA818_MODE_DIGITAL_DMR ?
                                   LED_MODE_RX_STANDBY_DMR : LED_MODE_RX_STANDBY_ANALOG);
                omm446_ble_notify_ptt(0);
                break;

            case KEY_EVENT_PTT_LONG:
                ESP_LOGI(TAG, "Power button long press -> entering deep sleep");
                indicator_set_mode(LED_MODE_OFF);
                vTaskDelay(pdMS_TO_TICKS(300));
                power_enter_deep_sleep();
                break;

            case KEY_EVENT_MODE_TOGGLE: {
                Sa818RadioMode_t next_mode = (radio.getState().mode == SA818_MODE_ANALOG_FM) ?
                                              SA818_MODE_DIGITAL_DMR : SA818_MODE_ANALOG_FM;
                radio.setRadioMode(next_mode);
                indicator_set_mode(next_mode == SA818_MODE_DIGITAL_DMR ?
                                   LED_MODE_RX_STANDBY_DMR : LED_MODE_RX_STANDBY_ANALOG);
                omm446_ble_notify_mode(next_mode);
                break;
            }

            case KEY_EVENT_CH_UP:
                radio.nextChannel();
                omm446_ble_notify_channel(radio.getState().channel);
                indicator_set_mode(LED_MODE_CHANNEL_CHANGE);
                vTaskDelay(pdMS_TO_TICKS(150));
                indicator_set_mode(radio.getState().mode == SA818_MODE_DIGITAL_DMR ?
                                   LED_MODE_RX_STANDBY_DMR : LED_MODE_RX_STANDBY_ANALOG);
                break;

            case KEY_EVENT_CH_DOWN:
                radio.prevChannel();
                omm446_ble_notify_channel(radio.getState().channel);
                indicator_set_mode(LED_MODE_CHANNEL_CHANGE);
                vTaskDelay(pdMS_TO_TICKS(150));
                indicator_set_mode(radio.getState().mode == SA818_MODE_DIGITAL_DMR ?
                                   LED_MODE_RX_STANDBY_DMR : LED_MODE_RX_STANDBY_ANALOG);
                break;

            case KEY_EVENT_NONE:
            default:
                break;
        }

        // 2. LED Animation aktualisieren
        indicator_update();

        // 3. Telemetrie & Akkustatus alle 500ms
        static int cycle = 0;
        if (++cycle >= 25) {
            cycle = 0;
            Omm446PowerStatus_t pwr = {};
            power_supervisor_poll(&pwr);

            int8_t rssi = radio.pollRssi();

            Omm446BleTelemetry_t telem = {
                .battery_pct = pwr.battery_pct,
                .is_charging = (uint8_t)(pwr.is_charging ? 1 : 0),
                .rssi_dbm = rssi,
                .is_receiving = (uint8_t)(radio.getState().is_receiving ? 1 : 0),
                .is_transmitting = (uint8_t)(radio.getState().is_transmitting ? 1 : 0),
                .current_channel = radio.getState().channel,
                .current_mode = (uint8_t)radio.getState().mode
            };
            omm446_ble_notify_telemetry(&telem);
        }

        vTaskDelay(pdMS_TO_TICKS(20)); // 50 Hz Poll-Rate
    }
}

extern "C" void app_main(void) {
    ESP_LOGI(TAG, "==========================================================");
    ESP_LOGI(TAG, " OpenMotorMesh 446 MHz PMR/DMR Transceiver Module (PCBA 10)");
    ESP_LOGI(TAG, " Firmware: %s | ESP32-C6 Dual-Mode Transceiver Host", OMM446_FW_VERSION_STRING);
    ESP_LOGI(TAG, "==========================================================");

    // 1. Initialize NVS
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    // 2. Initialize Hardware Codec (Everest Semi ES8388)
    ESP_ERROR_CHECK(es8388_codec_init());
    es8388_set_volume(s_current_volume);

    // 3. Initialize Keypad & Indicator
    ESP_ERROR_CHECK(keypad_indicator_init());

    // 4. Initialize Power Management (BQ24075)
    ESP_ERROR_CHECK(power_supervisor_init());

    // 5. Initialize NiceRF SA818-DMR Transceiver
    Sa818DmrDriver &radio = Sa818DmrDriver::getInstance();
    radio.registerSquelchCallback(on_squelch_changed, nullptr);
    radio.init();

    // 6. Initialize BLE Service for Cockpit / CarPlay Remote Control
    ESP_ERROR_CHECK(omm446_ble_service_init(on_ble_command_received));

    // 7. Launch FreeRTOS Tasks
    xTaskCreatePinnedToCore(audio_processing_task, "audio_task", 4096, NULL, 10, NULL, 0);
    xTaskCreatePinnedToCore(supervision_task, "supervision_task", 4096, NULL, 3, NULL, 0);

    ESP_LOGI(TAG, "✓ System fully booted and listening on PMR446 CH8 (446.09375 MHz)!");
}
