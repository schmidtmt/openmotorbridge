#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_timer.h"

#include "front_c3_config.h"
#include "usb_headunit_device.h"
#include "interchip_uart_link.h"
#include "i2s_audio_bridge.h"

static const char *TAG = "FRONT_C3_MAIN";

static C3HeadunitState s_current_state = {
    .usb_enumerated = true,
    .whim_emulation_active = true,
    .carplay_active = true,
    .speakers_active = true,
    .headunit_vol_pct = 75,
    .current_mux_target = 0 // 0=SkylineOS / Boom! Box
};

static void on_interchip_command(InterchipPktType type, const uint8_t *payload, size_t len) {
    switch (type) {
        case INTERCHIP_CMD_AUDIO_ROUTE:
            if (len >= 1) {
                uint8_t route_mode = payload[0];
                bool spk = (route_mode == 1 || route_mode == 2);
                s_current_state.speakers_active = spk;
                i2s_audio_bridge_set_speakers_active(spk);
                ESP_LOGI(TAG, "Audio Route command: mode=%d (Speakers %s)", route_mode, spk ? "ON" : "OFF");
            }
            break;

        case INTERCHIP_CMD_WHIM_OVERRIDE:
            if (len >= 1) {
                bool enable_whim = (payload[0] != 0);
                s_current_state.whim_emulation_active = enable_whim;
                usb_headunit_set_whim_connected(enable_whim);
            }
            break;

        case INTERCHIP_CMD_MEDIA_KEY:
            if (len >= 1) {
                MediaKeyCode code = static_cast<MediaKeyCode>(payload[0]);
                usb_headunit_send_media_key(code);
            }
            break;

        case INTERCHIP_CMD_VOLUME_SET:
            if (len >= 1) {
                s_current_state.headunit_vol_pct = payload[0];
                ESP_LOGI(TAG, "Volume set: %d%%", s_current_state.headunit_vol_pct);
            }
            break;

        case INTERCHIP_CMD_MUX_SELECT:
            if (len >= 1) {
                s_current_state.current_mux_target = payload[0];
                ESP_LOGI(TAG, "Display Mux target: %s", payload[0] == 0 ? "SkylineOS / Boom!" : "Aftermarket AA");
            }
            break;

        default:
            ESP_LOGW(TAG, "Unknown Interchip command: 0x%02X", (unsigned int)type);
            break;
    }
}

static void audio_bridge_task(void *pvParameters) {
    ESP_LOGI(TAG, "I2S -> USB UAC Audio streaming task running on Core %d", xPortGetCoreID());
    while (1) {
        i2s_audio_bridge_process();
        vTaskDelay(pdMS_TO_TICKS(2));
    }
}

extern "C" void app_main(void) {
    ESP_LOGI(TAG, "==================================================================");
    ESP_LOGI(TAG, "   OPENMOTORBRIDGE v10.0 FRONT-NODE CHIP 2 (PCBA 05 U10)          ");
    ESP_LOGI(TAG, "   Controller: ESP32-C3FH4 (32-Bit RISC-V @ 160 MHz)              ");
    ESP_LOGI(TAG, "   Role:       Infotainment Client & Harley WHIM Bypass Bridge    ");
    ESP_LOGI(TAG, "   Features:   COMM_20 WHIM | COMM_19 UAC Audio | COMM_21 HID Keys");
    ESP_LOGI(TAG, "==================================================================");

    // 1. Initialize Inter-Chip Link to S31 U1
    interchip_uart_init(on_interchip_command);

    // 2. Initialize USB Headunit Composite Device (WHIM + UAC + HID)
    usb_headunit_device_init();

    // 3. Initialize Digital I2S Slave Audio Bridge
    i2s_audio_bridge_init();

    // 4. Spawn high-priority audio processing task
    xTaskCreate(audio_bridge_task, "audio_bridge", 4096, NULL, 12, NULL);

    ESP_LOGI(TAG, "✓ Front-Node Chip 2 (ESP32-C3FH4 U10) is fully OPERATIONAL.");

    uint64_t last_status_report_us = 0;

    // Supervisor Loop
    while (1) {
        // Read incoming commands from S31
        interchip_uart_process_rx();

        // Update USB Headunit keepalives and WHIM presence heartbeats
        usb_headunit_update_tick();

        // Send periodic status feedback to S31 every 500 ms
        uint64_t now = esp_timer_get_time();
        if ((now - last_status_report_us) >= 500000ULL) {
            last_status_report_us = now;
            s_current_state.carplay_active = usb_headunit_is_carplay_unlocked();
            s_current_state.usb_enumerated = usb_headunit_is_connected();
            interchip_uart_send_status(&s_current_state);
        }

        vTaskDelay(pdMS_TO_TICKS(10));
    }
}
