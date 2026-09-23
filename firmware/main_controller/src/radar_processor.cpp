#include "radar_processor.h"
#include "audio_dsp_pipeline.h"
#include "can_bus_manager.h"
#include "esp_now_front_node_client.h"
#include "solar_position.h"
#include "esp_log.h"
#include "esp_timer.h"
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

// Protocol Sync Bytes for Radar 2.0 (Wheeltec MR20 Sub-MCU)
#define OMB_RADAR_SYNC_1        0x5A
#define OMB_RADAR_SYNC_2        0xA5
#define OMB_RADAR_VER_2         0x02

static SemaphoreHandle_t s_radar_mutex = NULL;
static RadarState_t s_radar_state = {
    .enabled = true,
    .sound_alert_enabled = true,
    .hw_type = RADAR_HW_TYPE_UNKNOWN,
    .target_count = 0,
    .max_threat = RADAR_THREAT_CLEAR,
    .closest_distance_m = 999.0f,
    .highest_rel_speed_kmh = 0.0f,
    .blind_spot_left = false,
    .blind_spot_right = false,
    .current_dimming_pct = 100,
    .tunnel_mode_active = false
};

// Dynamics & GNSS state for Radar Commands and Dimmer
static float s_vehicle_speed_kmh = 0.0f;
static float s_vehicle_accel_x_g = 0.0f;
static float s_gnss_lat = 47.3769f;
static float s_gnss_lon = 8.5417f;
static uint32_t s_gnss_utc_epoch = 0;
static bool s_gnss_fix_valid = false;
static bool s_cruise_mode_active = false;

static bool s_ess_active = false;
static uint32_t s_ess_start_ms = 0;
static bool s_ess_enabled = true;
static float s_ess_threshold_g = -0.60f;
static uint32_t s_last_audio_alert_ms = 0;
static uint32_t s_last_submcu_cmd_time_ms = 0;

// Compact structs for Sub-MCU protocol communication
typedef struct __attribute__((packed)) {
    uint8_t id;
    uint16_t distance_cm;
    int16_t rel_speed_cms;
    int16_t azimuth_cdeg;
    uint8_t ttc_tenths_s;
    uint8_t threat_level;
} SubMcuTarget_t;

typedef struct __attribute__((packed)) {
    uint8_t sync1;
    uint8_t sync2;
    uint8_t version;
    uint8_t pkt_type;
    uint8_t seq_num;
    uint8_t target_count;
    uint8_t max_threat;
    bool blind_spot_left;
    bool blind_spot_right;
    uint16_t closest_dist_cm;
    int16_t highest_speed_cms;
    SubMcuTarget_t targets[8];
    uint16_t checksum;
} SubMcuTelemetryPkt_t;

typedef struct __attribute__((packed)) {
    uint8_t sync1;
    uint8_t sync2;
    uint8_t version;
    uint8_t pkt_type;
    uint16_t vehicle_speed_kmh_x10;
    int16_t accel_x_mg;
    uint8_t dimming_pwm_pct;
    uint8_t brake_strobe_req;
    bool cruise_mode_active;
    uint16_t checksum;
} SubMcuCommandPkt_t;

static uint16_t calc_crc16(const uint8_t *data, size_t len) {
    uint16_t crc = 0xFFFF;
    for (size_t i = 0; i < len; i++) {
        crc ^= (uint16_t)data[i] << 8;
        for (uint8_t bit = 0; bit < 8; bit++) {
            if (crc & 0x8000) crc = (crc << 1) ^ 0x1021;
            else crc <<= 1;
        }
    }
    return crc;
}

esp_err_t radar_processor_init(void) {
    ESP_LOGI(TAG, "Initializing Radar Subsystem (Garmin Varia & Wheeltec MR20 Radar 2.0)...");
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

    ret = uart_driver_install(RADAR_UART_NUM, RADAR_RX_BUF_SIZE * 2, 512, 0, NULL, 0);
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

    if (rel_speed_kmh > 1.0f) {
        float speed_ms = (rel_speed_kmh * 1000.0f) / 3600.0f;
        t->time_to_collision_s = distance_m / speed_ms;
    } else {
        t->time_to_collision_s = 99.0f;
    }

    if (t->time_to_collision_s < 2.5f || (distance_m < 35.0f && rel_speed_kmh > 25.0f)) {
        t->threat = RADAR_THREAT_RED;
    } else if (distance_m < 75.0f && rel_speed_kmh > 15.0f) {
        t->threat = RADAR_THREAT_AMBER;
    } else {
        t->threat = RADAR_THREAT_CLEAR;
    }

    s_radar_state.max_threat = t->threat;
    s_radar_state.closest_distance_m = distance_m;
    s_radar_state.highest_rel_speed_kmh = rel_speed_kmh;

    s_radar_state.blind_spot_left = (distance_m < 15.0f && azimuth_deg < -3);
    s_radar_state.blind_spot_right = (distance_m < 15.0f && azimuth_deg > 3);

    uint8_t left_lvl = (s_radar_state.blind_spot_left) ? ((t->threat == RADAR_THREAT_RED) ? 2 : 1) : 0;
    uint8_t right_lvl = (s_radar_state.blind_spot_right) ? ((t->threat == RADAR_THREAT_RED) ? 2 : 1) : 0;
    esp_now_front_node_send_bsd_warning(s_radar_state.blind_spot_left, left_lvl,
                                        s_radar_state.blind_spot_right, right_lvl);

    uint32_t now = esp_log_timestamp();
    if (s_radar_state.sound_alert_enabled && t->threat != RADAR_THREAT_CLEAR) {
        if (now - s_last_audio_alert_ms > 2000) {
            s_last_audio_alert_ms = now;
            audio_trigger_radar_alert((uint8_t)t->threat);
        }
    }

    if (t->threat == RADAR_THREAT_RED && t->time_to_collision_s < 2.5f) {
        static uint32_t s_last_cam_tag_ms = 0;
        if (now - s_last_cam_tag_ms > 10000) {
            s_last_cam_tag_ms = now;
            ESP_LOGW(TAG, "⚡ Critical Radar Threat RED (TTC < 2.5s): Auto-setting Action Cam Bookmark!");
            esp_now_front_node_cam_hilight_tag();
        }
    }

    xSemaphoreGive(s_radar_mutex);
}

// Parse Radar 2.0 Sub-MCU Packets
static void parse_submcu_packet(const uint8_t *data, size_t len) {
    if (len < sizeof(SubMcuTelemetryPkt_t)) return;

    for (size_t i = 0; i <= len - sizeof(SubMcuTelemetryPkt_t); i++) {
        if (data[i] == OMB_RADAR_SYNC_1 && data[i + 1] == OMB_RADAR_SYNC_2 && data[i + 2] == OMB_RADAR_VER_2) {
            const SubMcuTelemetryPkt_t *pkt = (const SubMcuTelemetryPkt_t *)(data + i);
            uint16_t expected_crc = calc_crc16((const uint8_t *)pkt, sizeof(SubMcuTelemetryPkt_t) - 2);

            if (expected_crc == pkt->checksum && pkt->pkt_type == 0x10) {
                if (s_radar_mutex && xSemaphoreTake(s_radar_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
                    s_radar_state.hw_type = RADAR_HW_TYPE_MR20_V2;
                    s_radar_state.target_count = pkt->target_count;
                    s_radar_state.max_threat = (RadarThreatLevel_t)pkt->max_threat;
                    s_radar_state.blind_spot_left = pkt->blind_spot_left;
                    s_radar_state.blind_spot_right = pkt->blind_spot_right;
                    s_radar_state.closest_distance_m = (float)pkt->closest_dist_cm / 100.0f;
                    s_radar_state.highest_rel_speed_kmh = ((float)pkt->highest_speed_cms * 36.0f) / 1000.0f;

                    for (uint8_t t = 0; t < pkt->target_count && t < 8; t++) {
                        s_radar_state.targets[t].id = pkt->targets[t].id;
                        s_radar_state.targets[t].distance_m = (float)pkt->targets[t].distance_cm / 100.0f;
                        s_radar_state.targets[t].rel_speed_kmh = ((float)(-pkt->targets[t].rel_speed_cms) * 36.0f) / 1000.0f;
                        s_radar_state.targets[t].azimuth_deg = (int8_t)(pkt->targets[t].azimuth_cdeg / 100);
                        s_radar_state.targets[t].time_to_collision_s = (float)pkt->targets[t].ttc_tenths_s / 10.0f;
                        s_radar_state.targets[t].threat = (RadarThreatLevel_t)pkt->targets[t].threat_level;
                        s_radar_state.targets[t].last_seen_ms = esp_log_timestamp();
                    }

                    // Forward to Front-Node Mirror LEDs
                    uint8_t left_lvl = (s_radar_state.blind_spot_left) ? ((s_radar_state.max_threat == RADAR_THREAT_RED) ? 2 : 1) : 0;
                    uint8_t right_lvl = (s_radar_state.blind_spot_right) ? ((s_radar_state.max_threat == RADAR_THREAT_RED) ? 2 : 1) : 0;
                    esp_now_front_node_send_bsd_warning(s_radar_state.blind_spot_left, left_lvl,
                                                        s_radar_state.blind_spot_right, right_lvl);

                    // Sound Alert
                    uint32_t now = esp_log_timestamp();
                    if (s_radar_state.sound_alert_enabled && s_radar_state.max_threat != RADAR_THREAT_CLEAR) {
                        if (now - s_last_audio_alert_ms > 2000) {
                            s_last_audio_alert_ms = now;
                            audio_trigger_radar_alert((uint8_t)s_radar_state.max_threat);
                        }
                    }

                    // Action Cam Bookmark on critical threat
                    if (s_radar_state.max_threat == RADAR_THREAT_RED && s_radar_state.closest_distance_m < 25.0f) {
                        static uint32_t s_last_cam_tag_ms = 0;
                        if (now - s_last_cam_tag_ms > 10000) {
                            s_last_cam_tag_ms = now;
                            esp_now_front_node_cam_hilight_tag();
                        }
                    }

                    xSemaphoreGive(s_radar_mutex);
                }
                return;
            }
        }
    }
}

// Parse Garmin Varia Stream (Legacy Mode)
static void parse_varia_stream(const uint8_t *data, size_t len) {
    for (size_t i = 0; i < len; i++) {
        if (data[i] == 0xAA && (i + 4) < len) {
            uint8_t msg_len = data[i + 1];
            uint8_t msg_id = data[i + 2];

            if (msg_id == 0x20 && (i + msg_len) <= len) {
                if (s_radar_state.hw_type != RADAR_HW_TYPE_MR20_V2) {
                    s_radar_state.hw_type = RADAR_HW_TYPE_GARMIN;
                }
                uint8_t dist_raw = data[i + 4];
                uint8_t speed_raw = data[i + 5];
                int8_t azim_raw = (int8_t)data[i + 6];

                radar_inject_simulated_target((float)dist_raw, (float)speed_raw, azim_raw);
                i += msg_len;
            }
        }
    }
}

static void parse_radar_stream(const uint8_t *data, size_t len) {
    // Check for Radar 2.0 Sub-MCU first
    if (len >= sizeof(SubMcuTelemetryPkt_t)) {
        for (size_t i = 0; i < len - 1; i++) {
            if (data[i] == OMB_RADAR_SYNC_1 && data[i + 1] == OMB_RADAR_SYNC_2) {
                parse_submcu_packet(data, len);
                return;
            }
        }
    }
    // Fall back to Garmin Varia
    parse_varia_stream(data, len);
}

void radar_update_gnss_context(float lat, float lon, uint32_t utc_epoch, bool fix_valid) {
    s_gnss_lat = lat;
    s_gnss_lon = lon;
    s_gnss_utc_epoch = utc_epoch;
    s_gnss_fix_valid = fix_valid;
}

void radar_set_cruise_mode(bool cruise_mode) {
    s_cruise_mode_active = cruise_mode;
    ESP_LOGI(TAG, "Radar notified: Cruise Mode = %s", cruise_mode ? "ACTIVE" : "OFF");
}

esp_err_t radar_trigger_submcu_bootloader(void) {
    ESP_LOGW(TAG, "⚡ Sending Bootloader Entry Request to Radar 2.0 Sub-MCU...");
    SubMcuCommandPkt_t cmd = {
        .sync1 = OMB_RADAR_SYNC_1,
        .sync2 = OMB_RADAR_SYNC_2,
        .version = OMB_RADAR_VER_2,
        .pkt_type = 0xF0, // RADAR_PKT_CMD_ENTER_BOOTLOAD
        .vehicle_speed_kmh_x10 = 0,
        .accel_x_mg = 0,
        .dimming_pwm_pct = 100,
        .brake_strobe_req = 0,
        .cruise_mode_active = false,
        .checksum = 0
    };
    cmd.checksum = calc_crc16((const uint8_t *)&cmd, sizeof(cmd) - 2);
    uart_write_bytes(RADAR_UART_NUM, (const char *)&cmd, sizeof(cmd));
    return ESP_OK;
}

void radar_set_ess_config(bool enabled, float threshold_g) {
    s_ess_enabled = enabled;
    if (threshold_g < 0.0f) s_ess_threshold_g = threshold_g;
    ESP_LOGI(TAG, "ESS Configuration: Enabled=%d, Threshold=%.2fg", s_ess_enabled, s_ess_threshold_g);
}

void radar_trigger_ess_test(void) {
    ESP_LOGW(TAG, "⚡ Manual ESS Brake Light Test triggered! 4.5 Hz Strobe active.");
    s_ess_active = true;
    s_ess_start_ms = esp_log_timestamp();

    // 1. Send Varia Strobe
    uint8_t varia_strobe[] = { 0xAA, 0x04, 0x30, 0x02, 0x00 };
    uart_write_bytes(RADAR_UART_NUM, (const char *)varia_strobe, sizeof(varia_strobe));

    // 2. Send Radar 2.0 Sub-MCU Strobe
    SubMcuCommandPkt_t cmd = {
        .sync1 = OMB_RADAR_SYNC_1,
        .sync2 = OMB_RADAR_SYNC_2,
        .version = OMB_RADAR_VER_2,
        .pkt_type = 0x20,
        .vehicle_speed_kmh_x10 = (uint16_t)(s_vehicle_speed_kmh * 10.0f),
        .accel_x_mg = (int16_t)(s_vehicle_accel_x_g * 1000.0f),
        .dimming_pwm_pct = s_radar_state.current_dimming_pct,
        .brake_strobe_req = 2, // 2 = ESS Strobe
        .cruise_mode_active = s_cruise_mode_active,
        .checksum = 0
    };
    cmd.checksum = calc_crc16((const uint8_t *)&cmd, sizeof(cmd) - 2);
    uart_write_bytes(RADAR_UART_NUM, (const char *)&cmd, sizeof(cmd));

    esp_now_front_node_set_aux_light(2);
    esp_now_front_node_cam_hilight_tag();
}

void radar_notify_vehicle_dynamics(float speed_kmh, float accel_x_g) {
    s_vehicle_speed_kmh = speed_kmh;
    s_vehicle_accel_x_g = accel_x_g;

    if (!s_ess_enabled) return;
    uint32_t now = esp_log_timestamp();

    if (accel_x_g < s_ess_threshold_g && speed_kmh > 20.0f) {
        if (!s_ess_active) {
            s_ess_active = true;
            s_ess_start_ms = now;
            ESP_LOGW(TAG, "⚡ EMERGENCY STOP SIGNAL (ESS) TRIGGERED! (ax = %.2f g)", accel_x_g);

            uint8_t varia_strobe[] = { 0xAA, 0x04, 0x30, 0x02, 0x00 };
            uart_write_bytes(RADAR_UART_NUM, (const char *)varia_strobe, sizeof(varia_strobe));

            esp_now_front_node_set_aux_light(2);
            esp_now_front_node_cam_hilight_tag();
        }
    } else if (s_ess_active && (now - s_ess_start_ms > 2500 || accel_x_g > -0.20f)) {
        s_ess_active = false;
        ESP_LOGI(TAG, "ESS Deactivated. Reverting lights.");

        uint8_t varia_solid[] = { 0xAA, 0x04, 0x30, 0x01, 0x00 };
        uart_write_bytes(RADAR_UART_NUM, (const char *)varia_solid, sizeof(varia_solid));

        esp_now_front_node_set_aux_light(0);
    }
}

bool radar_is_ess_active(void) {
    return s_ess_active;
}

void task_radar_processor(void *pvParameters) {
    ESP_LOGI(TAG, "Radar Processor Task running on Core 0 (Priority 6, 20 Hz)...");
    uint8_t rx_buffer[256];

    while (true) {
        int bytes = uart_read_bytes(RADAR_UART_NUM, rx_buffer, sizeof(rx_buffer) - 1, pdMS_TO_TICKS(50));
        if (bytes > 0) {
            parse_radar_stream(rx_buffer, (size_t)bytes);
        }

        // Calculate astronomical dimming & tunnel detection
        uint8_t dimming = solar_dimmer_evaluate(s_gnss_lat, s_gnss_lon, s_gnss_utc_epoch,
                                                s_gnss_fix_valid, s_vehicle_speed_kmh);
        s_radar_state.current_dimming_pct = dimming;
        s_radar_state.tunnel_mode_active = solar_dimmer_is_tunnel_active();

        // Transmit Command Frame to Sub-MCU at 10 Hz (every 100ms)
        uint32_t now_ms = (uint32_t)(esp_timer_get_time() / 1000ULL);
        if (now_ms - s_last_submcu_cmd_time_ms >= 100) {
            s_last_submcu_cmd_time_ms = now_ms;

            uint8_t brake_req = 0;
            if (s_ess_active) brake_req = 2;
            else if (s_vehicle_accel_x_g < -0.15f) brake_req = 1;

            SubMcuCommandPkt_t cmd = {
                .sync1 = OMB_RADAR_SYNC_1,
                .sync2 = OMB_RADAR_SYNC_2,
                .version = OMB_RADAR_VER_2,
                .pkt_type = 0x20, // RADAR_PKT_CMD_VEHICLE_STATE
                .vehicle_speed_kmh_x10 = (uint16_t)(s_vehicle_speed_kmh * 10.0f),
                .accel_x_mg = (int16_t)(s_vehicle_accel_x_g * 1000.0f),
                .dimming_pwm_pct = dimming,
                .brake_strobe_req = brake_req,
                .cruise_mode_active = s_cruise_mode_active,
                .checksum = 0
            };
            cmd.checksum = calc_crc16((const uint8_t *)&cmd, sizeof(cmd) - 2);
            uart_write_bytes(RADAR_UART_NUM, (const char *)&cmd, sizeof(cmd));
        }

        // Target Timeout check (1500 ms)
        if (s_radar_mutex && xSemaphoreTake(s_radar_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
            uint32_t now = esp_log_timestamp();
            if (s_radar_state.target_count > 0 && (now - s_radar_state.targets[0].last_seen_ms > 1500)) {
                s_radar_state.target_count = 0;
                s_radar_state.max_threat = RADAR_THREAT_CLEAR;
                s_radar_state.closest_distance_m = 999.0f;
                s_radar_state.highest_rel_speed_kmh = 0.0f;
                s_radar_state.blind_spot_left = false;
                s_radar_state.blind_spot_right = false;
                esp_now_front_node_send_bsd_warning(false, 0, false, 0);
            }
            xSemaphoreGive(s_radar_mutex);
        }

        vTaskDelay(pdMS_TO_TICKS(50)); // 20 Hz
    }
}
