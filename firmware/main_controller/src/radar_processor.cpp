#include "radar_processor.h"
#include "audio_dsp_pipeline.h"
#include "can_bus_manager.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "driver/uart.h"
#include "driver/gpio.h"
#include <string.h>
#include <math.h>

static const char *TAG = "RADAR_PROC";

#define RADAR_UART_NUM          UART_NUM_2
#define RADAR_UART_TX_PIN       GPIO_NUM_23  // RESERVE_GPIO_B
#define RADAR_UART_RX_PIN       GPIO_NUM_22  // RESERVE_GPIO_A
#define RADAR_UART_BAUDRATE     115200
#define RADAR_RX_BUF_SIZE       1024

static SemaphoreHandle_t s_radar_mutex = NULL;
static RadarState_t s_radar_state = {
    .enabled = true,
    .sound_alert_enabled = true,
    .target_count = 0,
    .max_threat = RADAR_THREAT_CLEAR,
    .closest_distance_m = 999.0f,
    .highest_rel_speed_kmh = 0.0f,
    .blind_spot_left = false,
    .blind_spot_right = false
};

static uint32_t s_last_audio_alert_ms = 0;

esp_err_t radar_processor_init(void) {
    ESP_LOGI(TAG, "Initializing Rear Radar & Blind-Spot Detection Subsystem...");
    s_radar_mutex = xSemaphoreCreateMutex();

    const uart_config_t uart_config = {
        .baud_rate = RADAR_UART_BAUDRATE,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };

    esp_err_t ret = uart_param_config(RADAR_UART_NUM, &uart_config);
    if (ret != ESP_OK) return ret;

    ret = uart_set_pin(RADAR_UART_NUM, RADAR_UART_TX_PIN, RADAR_UART_RX_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    if (ret != ESP_OK) return ret;

    ret = uart_driver_install(RADAR_UART_NUM, RADAR_RX_BUF_SIZE * 2, 0, 0, NULL, 0);
    if (ret != ESP_OK) return ret;

    ESP_LOGI(TAG, "Radar UART2 initialized (RX: GPIO%d, TX: GPIO%d, Baud: %d)",
             RADAR_UART_RX_PIN, RADAR_UART_TX_PIN, RADAR_UART_BAUDRATE);
    return ESP_OK;
}

RadarState_t radar_get_current_state(void) {
    RadarState_t state_copy;
    if (s_radar_mutex && xSemaphoreTake(s_radar_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
        state_copy = s_radar_state;
        xSemaphoreGive(s_radar_mutex);
    } else {
        memset(&state_copy, 0, sizeof(RadarState_t));
    }
    return state_copy;
}

void radar_set_sound_alert_enabled(bool enabled) {
    if (s_radar_mutex && xSemaphoreTake(s_radar_mutex, pdMS_TO_TICKS(20)) == pdTRUE) {
        s_radar_state.sound_alert_enabled = enabled;
        xSemaphoreGive(s_radar_mutex);
    }
    ESP_LOGI(TAG, "Radar audio alerts: %s", enabled ? "ENABLED" : "MUTED");
}

void radar_trigger_test_alert(RadarThreatLevel_t threat) {
    ESP_LOGW(TAG, "Manual Radar Test Triggered: Threat Level %d", threat);
    audio_trigger_radar_alert((uint8_t)threat);
}

void radar_inject_simulated_target(float distance_m, float rel_speed_kmh, int8_t azimuth_deg) {
    if (!s_radar_mutex || xSemaphoreTake(s_radar_mutex, pdMS_TO_TICKS(20)) != pdTRUE) return;

    s_radar_state.target_count = 1;
    RadarTarget_t *t = &s_radar_state.targets[0];
    t->id = 1;
    t->distance_m = distance_m;
    t->rel_speed_kmh = rel_speed_kmh;
    t->azimuth_deg = azimuth_deg;
    t->last_seen_ms = esp_log_timestamp();

    // Time-To-Collision (TTC) in seconds
    if (rel_speed_kmh > 1.0f) {
        float speed_ms = (rel_speed_kmh * 1000.0f) / 3600.0f;
        t->time_to_collision_s = distance_m / speed_ms;
    } else {
        t->time_to_collision_s = 99.0f;
    }

    // Threat Classification
    if (t->time_to_collision_s < 3.5f || (distance_m < 35.0f && rel_speed_kmh > 25.0f)) {
        t->threat = RADAR_THREAT_RED;
    } else if (distance_m < 75.0f && rel_speed_kmh > 15.0f) {
        t->threat = RADAR_THREAT_AMBER;
    } else {
        t->threat = RADAR_THREAT_CLEAR;
    }

    s_radar_state.max_threat = t->threat;
    s_radar_state.closest_distance_m = distance_m;
    s_radar_state.highest_rel_speed_kmh = rel_speed_kmh;

    // Blind spot evaluation (distance < 12m, off-center azimuth)
    s_radar_state.blind_spot_left = (distance_m < 12.0f && azimuth_deg < -3);
    s_radar_state.blind_spot_right = (distance_m < 12.0f && azimuth_deg > 3);

    // Audio Ping Triggering on Threat Escalation
    uint32_t now = esp_log_timestamp();
    if (s_radar_state.sound_alert_enabled && t->threat != RADAR_THREAT_CLEAR) {
        if (now - s_last_audio_alert_ms > 2000) { // 2.0s Hold / Debounce
            s_last_audio_alert_ms = now;
            audio_trigger_radar_alert((uint8_t)t->threat);
        }
    }

    xSemaphoreGive(s_radar_mutex);
}

static void parse_radar_stream(const uint8_t *data, size_t len) {
    // 1. Garmin Varia Binary Protocol Parser
    // Preamble: 0xAA, Len, MsgID (0x20 = Threat Data), Target Array, CRC
    for (size_t i = 0; i < len; i++) {
        if (data[i] == 0xAA && (i + 4) < len) {
            uint8_t msg_len = data[i + 1];
            uint8_t msg_id = data[i + 2];

            if (msg_id == 0x20 && (i + msg_len) <= len) {
                // Parse target record
                uint8_t target_id = data[i + 3];
                uint8_t dist_raw = data[i + 4]; // in meters (0-140)
                uint8_t speed_raw = data[i + 5]; // relative speed offset
                int8_t azim_raw = (int8_t)data[i + 6]; // azimuth degrees

                float distance = (float)dist_raw;
                float rel_speed = (float)speed_raw;

                radar_inject_simulated_target(distance, rel_speed, azim_raw);
                i += msg_len;
            }
        }
    }
}

void task_radar_processor(void *pvParameters) {
    ESP_LOGI(TAG, "Radar Processor Task running on Core 0 (Priority 6, 20 Hz)...");
    uint8_t rx_buffer[128];

    while (true) {
        int bytes = uart_read_bytes(RADAR_UART_NUM, rx_buffer, sizeof(rx_buffer) - 1, pdMS_TO_TICKS(50));
        if (bytes > 0) {
            parse_radar_stream(rx_buffer, bytes);
        }

        // Timeout cleanup: If no target seen for > 1500 ms, clear threats
        if (s_radar_mutex && xSemaphoreTake(s_radar_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
            uint32_t now = esp_log_timestamp();
            if (s_radar_state.target_count > 0) {
                if (now - s_radar_state.targets[0].last_seen_ms > 1500) {
                    s_radar_state.target_count = 0;
                    s_radar_state.max_threat = RADAR_THREAT_CLEAR;
                    s_radar_state.closest_distance_m = 999.0f;
                    s_radar_state.highest_rel_speed_kmh = 0.0f;
                    s_radar_state.blind_spot_left = false;
                    s_radar_state.blind_spot_right = false;
                }
            }
            xSemaphoreGive(s_radar_mutex);
        }

        vTaskDelay(pdMS_TO_TICKS(50)); // 20 Hz Evaluation Loop
    }
}
