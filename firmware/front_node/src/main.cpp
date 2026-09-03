#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "driver/gpio.h"

#include "front_node_config.h"
#include "handlebar_ptt_handler.h"
#include "ottocast_power_manager.h"
#include "knowles_mems_dsp.h"
#include "cockpit_can_manager.h"
#include "esp_now_bridge.h"
#include "ota_service_manager.h"

static const char* TAG = "FRONT_NODE_MAIN";

// -----------------------------------------------------------------------------
// Remote Command Handler (Dispatched from Central Box via ESP-NOW)
// -----------------------------------------------------------------------------
static void handle_remote_command(uint8_t cmd_type, const uint8_t* payload, size_t len) {
    switch (cmd_type) {
        case PKT_TYPE_CMD_POWER_CYCLE:
            ESP_LOGW(TAG, "ESP-NOW Command: Power-cycle Ottocast requested from WebApp");
            OttocastPowerManager::instance().trigger_hard_reset();
            break;

        case PKT_TYPE_CMD_CONFIG:
            if (len >= 2) {
                bool ignition = (payload[0] != 0);
                OttocastPowerManager::instance().set_ignition(ignition);
                ESP_LOGI(TAG, "ESP-NOW Command: Ignition state updated to %s", ignition ? "ON" : "OFF");
            }
            break;

        case PKT_TYPE_OTA_BEGIN:
            if (len >= 4) {
                uint32_t img_size = 0;
                memcpy(&img_size, payload, 4);
                ESP_LOGW(TAG, "ESP-NOW Command: Remote OTA Begin! Image size: %lu bytes", img_size);
                OtaServiceManager::instance().begin_update(img_size);
            }
            break;

        case PKT_TYPE_OTA_CHUNK:
            OtaServiceManager::instance().write_chunk(payload, len);
            break;

        case PKT_TYPE_OTA_FINISH:
            ESP_LOGW(TAG, "ESP-NOW Command: Remote OTA Finish! Finalizing and rebooting...");
            OtaServiceManager::instance().finalize_and_reboot();
            break;

        default:
            ESP_LOGD(TAG, "Unknown ESP-NOW command type: 0x%02X (len=%zu)", cmd_type, len);
            break;
    }
}

// -----------------------------------------------------------------------------
// Task 1: Zero-Latency Handlebar PTT Forwarding
// -----------------------------------------------------------------------------
static void ptt_task(void* pvParameters) {
    HandlebarPttHandler& ptt = HandlebarPttHandler::instance();
    EspNowBridge& bridge = EspNowBridge::instance();
    PttEvent evt;

    ESP_LOGI(TAG, "PTT monitoring task running on core %d (Priority 10)", xPortGetCoreID());

    while (1) {
        if (ptt.get_event(&evt, portMAX_DELAY)) {
            ESP_LOGI(TAG, "⚡ PTT Event: %s at %llu us -> Transmitting via ESP-NOW",
                     evt.pressed ? "PRESSED (ON)" : "RELEASED (OFF)",
                     evt.timestamp_us);

            // Immediate high-priority transmit
            bridge.send_ptt_event(evt.pressed, evt.timestamp_us);
        }
    }
}

// -----------------------------------------------------------------------------
// Task 2: Knowles MEMS I2S Audio Acquisition & Edge DSP
// -----------------------------------------------------------------------------
static void audio_dsp_task(void* pvParameters) {
    KnowlesMemsDsp& dsp = KnowlesMemsDsp::instance();
    EspNowBridge& bridge = EspNowBridge::instance();

    ESP_LOGI(TAG, "Audio Edge-DSP task running (50 Hz / 20 ms frames)");
    TickType_t last_wake_time = xTaskGetTickCount();

    while (1) {
        // Read 320 audio samples via I2S DMA, calculate A-weighted RMS
        dsp.process_audio();

        uint8_t dba = dsp.get_latest_dba();
        uint32_t rms = dsp.get_raw_rms();

        // Transmit 1-byte dBA acoustic telemetry to Central Box for helmet AGC
        bridge.send_audio_rms(dba, rms);

        vTaskDelayUntil(&last_wake_time, pdMS_TO_TICKS(AUDIO_RMS_INTERVAL_MS));
    }
}

// -----------------------------------------------------------------------------
// Task 3: System Supervisor, Ottocast Management & CAN-Bus
// -----------------------------------------------------------------------------
static void supervisor_task(void* pvParameters) {
    OttocastPowerManager& ottocast = OttocastPowerManager::instance();
    CockpitCanManager& can = CockpitCanManager::instance();
    EspNowBridge& bridge = EspNowBridge::instance();

    ESP_LOGI(TAG, "System supervisor task active (10 Hz)");

    uint32_t heartbeat_counter = 0;
    uint32_t led_tick = 0;

    while (1) {
        // 1. Advance Ottocast State Machine (Overcurrent & Auto-Café timers)
        ottocast.update();

        // 2. Poll Cockpit CAN Messages
        CanMessage can_msg;
        while (can.receive_message(&can_msg, 0)) {
            ESP_LOGD(TAG, "CAN Frame RX: ID=0x%08lX, DLC=%d", can_msg.id, can_msg.dlc);
            // Forward relevant cockpit telemetry if needed
        }

        // 3. Heartbeat & Ottocast Status Telemetry (every 500 ms)
        heartbeat_counter++;
        if (heartbeat_counter >= 5) {
            heartbeat_counter = 0;
            bridge.send_heartbeat();
            bridge.send_ottocast_status(
                static_cast<uint8_t>(ottocast.get_state()),
                ottocast.is_power_on(),
                ottocast.has_fault(),
                ottocast.get_cafe_remaining_sec()
            );
        }

        // 4. Status LED Blinking Logic (GPIO8)
        led_tick++;
        if (OtaServiceManager::instance().is_updating()) {
            // Rapid flash (10 Hz) during OTA firmware flashing
            gpio_set_level(PIN_STATUS_LED, (led_tick % 2) == 0 ? 1 : 0);
        } else if (ottocast.has_fault()) {
            // Double flash on hardware fault
            gpio_set_level(PIN_STATUS_LED, (led_tick % 10 < 4 && (led_tick % 2) == 0) ? 1 : 0);
        } else if (bridge.is_linked()) {
            // Solid ON or calm 1 Hz breathing blink when linked to Central Box
            gpio_set_level(PIN_STATUS_LED, (led_tick % 10 < 8) ? 1 : 0);
        } else {
            // 2 Hz flashing when searching for Central Box
            gpio_set_level(PIN_STATUS_LED, (led_tick % 5 < 2) ? 1 : 0);
        }

        vTaskDelay(pdMS_TO_TICKS(100)); // 100 ms tick
    }
}

// -----------------------------------------------------------------------------
// Application Entry Point
// -----------------------------------------------------------------------------
extern "C" void app_main(void) {
    ESP_LOGI(TAG, "============================================================");
    ESP_LOGI(TAG, "   OPENMOTORBRIDGE UNIVERSAL FRONT NODE FIRMWARE v1.0.0     ");
    ESP_LOGI(TAG, "   Target: ESP32-C3-WROOM-02U (PCBA 05)                     ");
    ESP_LOGI(TAG, "============================================================");

    // 1. Configure Status LED & Boot Button
    gpio_config_t led_conf = {
        .pin_bit_mask = (1ULL << PIN_STATUS_LED),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&led_conf);
    gpio_set_level(PIN_STATUS_LED, 1);

    gpio_config_t btn_conf = {
        .pin_bit_mask = (1ULL << PIN_BOOT_BUTTON),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&btn_conf);

    // 2. Initialize Subsystems
    OtaServiceManager::instance().init();
    HandlebarPttHandler::instance().init();
    OttocastPowerManager::instance().init();
    KnowlesMemsDsp::instance().init();
    CockpitCanManager::instance().init(250); // Default 250 kbps for Harley / BMW cockpit CAN

    // 3. Initialize ESP-NOW Wireless Bridge
    EspNowBridge& bridge = EspNowBridge::instance();
    bridge.init();
    bridge.set_command_callback(handle_remote_command);

    // 4. Spawn Real-Time FreeRTOS Tasks
    xTaskCreate(ptt_task, "ptt_task", 3072, NULL, 10, NULL);          // Highest priority
    xTaskCreate(audio_dsp_task, "audio_dsp", 4096, NULL, 6, NULL);    // Real-time audio DSP
    xTaskCreate(supervisor_task, "supervisor", 3072, NULL, 3, NULL);  // System housekeeping

    ESP_LOGI(TAG, "All Front Node real-time tasks successfully started. System ready.");
}
