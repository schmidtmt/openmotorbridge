#include "can_bus_manager.h"
#include <stdio.h>
#include <string.h>
#include <math.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/twai.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "adr_ekf_filter.h"

static const char *TAG = "CAN_MGR";

// GPIO Pin-Definitionen für TI TCAN334G Transceiver (v8.0 Pinout)
#define PIN_CAN_TX          GPIO_NUM_19
#define PIN_CAN_RX          GPIO_NUM_20

static bool s_can_initialized = false;
static bool s_can_traffic_active = false;
static bool s_listen_only_mode = true;
static float s_last_vehicle_speed_kmh = 0.0f;
static uint32_t s_rx_msg_count = 0;
static float s_current_fps = 0.0f;

// Profile & Signal Table
static char s_active_profile_id[CAN_PROFILE_MAX_NAME_LEN] = "harley_skyline_2024";
static CanDecodedSignal_t s_signals[CAN_PROFILE_MAX_SIGNALS];
static size_t s_num_signals = 0;

// Fingerprint Auto-Scan State
static bool s_fingerprint_scan_active = false;
static uint64_t s_fingerprint_start_us = 0;
static uint32_t s_seen_ids[32];
static size_t s_seen_id_count = 0;
static char s_detected_profile_id[CAN_PROFILE_MAX_NAME_LEN] = "";

// Bit extraction helper
static uint64_t extract_raw_bits(const uint8_t *data, uint8_t dlc, uint16_t start_bit, uint16_t length_bits, bool is_big_endian) {
    if (!data || dlc == 0 || length_bits == 0 || length_bits > 64) return 0;

    uint64_t raw_val = 0;
    if (!is_big_endian) {
        // Little-Endian (Intel)
        uint64_t payload = 0;
        size_t copy_bytes = dlc > 8 ? 8 : dlc;
        for (size_t i = 0; i < copy_bytes; i++) {
            payload |= ((uint64_t)data[i]) << (i * 8);
        }
        raw_val = (payload >> start_bit) & ((length_bits >= 64) ? ~0ULL : ((1ULL << length_bits) - 1ULL));
    } else {
        // Big-Endian (Motorola)
        for (uint16_t i = 0; i < length_bits; i++) {
            uint16_t bit_idx = start_bit + i;
            uint16_t byte_idx = bit_idx / 8;
            uint16_t bit_in_byte = 7 - (bit_idx % 8);
            if (byte_idx < dlc) {
                uint8_t bit = (data[byte_idx] >> bit_in_byte) & 0x01;
                raw_val = (raw_val << 1) | bit;
            }
        }
    }
    return raw_val;
}

// Built-in reference profile loader (also serves as fallback if LittleFS is not mounted)
static void load_builtin_profile(const char *profile_id) {
    memset(s_signals, 0, sizeof(s_signals));
    s_num_signals = 0;
    strncpy(s_active_profile_id, profile_id, sizeof(s_active_profile_id) - 1);

    if (strcmp(profile_id, "bmw_motorrad_k5x_r1250_r1300") == 0) {
        // BMW K5x / R1250 / R1300
        // Speed: ID 0x130, start 32, len 12, scale 0.1
        strncpy(s_signals[0].name, "speed_kmh", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[0].can_id = 0x130; s_signals[0].start_bit = 32; s_signals[0].length_bits = 12; s_signals[0].scale = 0.1f;
        
        strncpy(s_signals[1].name, "engine_rpm", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[1].can_id = 0x10C; s_signals[1].start_bit = 16; s_signals[1].length_bits = 16; s_signals[1].scale = 0.25f;

        strncpy(s_signals[2].name, "gear_selected", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[2].can_id = 0x130; s_signals[2].start_bit = 48; s_signals[2].length_bits = 4; s_signals[2].scale = 1.0f;

        strncpy(s_signals[3].name, "wonderwheel_scroll", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[3].can_id = 0x2A0; s_signals[3].start_bit = 8; s_signals[3].length_bits = 8; s_signals[3].scale = 1.0f;

        strncpy(s_signals[4].name, "wonderwheel_tilt_left", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[4].can_id = 0x2A0; s_signals[4].start_bit = 16; s_signals[4].length_bits = 1; s_signals[4].scale = 1.0f;

        strncpy(s_signals[5].name, "wonderwheel_tilt_right", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[5].can_id = 0x2A0; s_signals[5].start_bit = 17; s_signals[5].length_bits = 1; s_signals[5].scale = 1.0f;

        strncpy(s_signals[6].name, "tire_pressure_front_bar", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[6].can_id = 0x2D0; s_signals[6].start_bit = 16; s_signals[6].length_bits = 8; s_signals[6].scale = 0.02f;

        strncpy(s_signals[7].name, "tire_pressure_rear_bar", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[7].can_id = 0x2D0; s_signals[7].start_bit = 24; s_signals[7].length_bits = 8; s_signals[7].scale = 0.02f;

        s_num_signals = 8;
        ESP_LOGI(TAG, "Loaded built-in profile: BMW Motorrad K5x/K6x (8 signals configured).");
    } else if (strcmp(profile_id, "generic_obd2_iso15765") == 0) {
        // Generic Euro 4/5 OBD2
        strncpy(s_signals[0].name, "speed_kmh", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[0].can_id = 0x7E8; s_signals[0].start_bit = 24; s_signals[0].length_bits = 8; s_signals[0].scale = 1.0f;

        strncpy(s_signals[1].name, "engine_rpm", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[1].can_id = 0x7E8; s_signals[1].start_bit = 24; s_signals[1].length_bits = 16; s_signals[1].scale = 0.25f;

        strncpy(s_signals[2].name, "engine_temp_c", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[2].can_id = 0x7E8; s_signals[2].start_bit = 24; s_signals[2].length_bits = 8; s_signals[2].scale = 1.0f; s_signals[2].offset = -40.0f;

        s_num_signals = 3;
        ESP_LOGI(TAG, "Loaded built-in profile: Generic OBD2 ISO 15765 (3 signals configured).");
    } else {
        // Default: Harley-Davidson Skyline OS / HD-LAN
        strncpy(s_signals[0].name, "speed_kmh", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[0].can_id = 0x280; s_signals[0].start_bit = 16; s_signals[0].length_bits = 16; s_signals[0].scale = 0.0625f;

        strncpy(s_signals[1].name, "engine_rpm", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[1].can_id = 0x200; s_signals[1].start_bit = 0; s_signals[1].length_bits = 16; s_signals[1].scale = 1.0f;

        strncpy(s_signals[2].name, "gear_selected", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[2].can_id = 0x280; s_signals[2].start_bit = 32; s_signals[2].length_bits = 4; s_signals[2].scale = 1.0f;

        strncpy(s_signals[3].name, "engine_temp_c", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[3].can_id = 0x380; s_signals[3].start_bit = 0; s_signals[3].length_bits = 8; s_signals[3].scale = 1.0f; s_signals[3].offset = -40.0f;

        strncpy(s_signals[4].name, "fuel_remaining_liters", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[4].can_id = 0x400; s_signals[4].start_bit = 8; s_signals[4].length_bits = 8; s_signals[4].scale = 0.1f;

        strncpy(s_signals[5].name, "fuel_range_km", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[5].can_id = 0x400; s_signals[5].start_bit = 16; s_signals[5].length_bits = 16; s_signals[5].scale = 1.0f;

        strncpy(s_signals[6].name, "tire_pressure_front_bar", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[6].can_id = 0x420; s_signals[6].start_bit = 0; s_signals[6].length_bits = 8; s_signals[6].scale = 0.025f;

        strncpy(s_signals[7].name, "tire_pressure_rear_bar", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[7].can_id = 0x420; s_signals[7].start_bit = 8; s_signals[7].length_bits = 8; s_signals[7].scale = 0.025f;

        strncpy(s_signals[8].name, "handlebar_voice_btn", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[8].can_id = 0x290; s_signals[8].start_bit = 16; s_signals[8].length_bits = 1; s_signals[8].scale = 1.0f;

        strncpy(s_signals[9].name, "handlebar_joystick_left", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[9].can_id = 0x290; s_signals[9].start_bit = 17; s_signals[9].length_bits = 1; s_signals[9].scale = 1.0f;

        strncpy(s_signals[10].name, "handlebar_joystick_right", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[10].can_id = 0x290; s_signals[10].start_bit = 18; s_signals[10].length_bits = 1; s_signals[10].scale = 1.0f;

        strncpy(s_signals[11].name, "handlebar_joystick_click", CAN_PROFILE_MAX_NAME_LEN);
        s_signals[11].can_id = 0x290; s_signals[11].start_bit = 19; s_signals[11].length_bits = 1; s_signals[11].scale = 1.0f;

        s_num_signals = 12;
        ESP_LOGI(TAG, "Loaded built-in profile: Harley-Davidson Skyline OS (12 signals configured).");
    }
}

esp_err_t can_bus_manager_init(void) {
    ESP_LOGI(TAG, "Initializing TI TCAN334G TWAI Interface on TX: GPIO %d, RX: GPIO %d...",
             PIN_CAN_TX, PIN_CAN_RX);

    // Initialisiere Standard-Profil
    load_builtin_profile(s_active_profile_id);

    // 1. TWAI Konfiguration: 500 kbps (Motorrad-Standard)
    twai_general_config_t g_config = TWAI_GENERAL_CONFIG_DEFAULT(
        (gpio_num_t)PIN_CAN_TX,
        (gpio_num_t)PIN_CAN_RX,
        s_listen_only_mode ? TWAI_MODE_LISTEN_ONLY : TWAI_MODE_NORMAL
    );
    g_config.rx_queue_len = 64;
    g_config.tx_queue_len = 8;

    twai_timing_config_t t_config = TWAI_TIMING_CONFIG_500KBITS();
    twai_filter_config_t f_config = TWAI_FILTER_CONFIG_ACCEPT_ALL();

    // 2. Treiber installieren & starten
    esp_err_t ret = twai_driver_install(&g_config, &t_config, &f_config);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to install TWAI driver: %s", esp_err_to_name(ret));
        return ret;
    }

    ret = twai_start();
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to start TWAI driver: %s", esp_err_to_name(ret));
        return ret;
    }

    s_can_initialized = true;
    ESP_LOGI(TAG, "TWAI (CAN-Bus) Driver running at 500 kbps (Mode: %s).",
             s_listen_only_mode ? "LISTEN-ONLY (Safe)" : "NORMAL");
    return ESP_OK;
}

esp_err_t can_bus_load_profile(const char *profile_id) {
    if (!profile_id) return ESP_ERR_INVALID_ARG;
    load_builtin_profile(profile_id);
    return ESP_OK;
}

const char* can_bus_get_active_profile_id(void) {
    return s_active_profile_id;
}

bool can_bus_has_signal(const char *signal_name) {
    if (!signal_name) return false;
    for (size_t i = 0; i < s_num_signals; i++) {
        if (strcmp(s_signals[i].name, signal_name) == 0) {
            return true;
        }
    }
    return false;
}

bool can_bus_get_signal(const char *signal_name, float *out_value) {
    if (!signal_name || !out_value) return false;
    uint32_t now_ms = (uint32_t)(esp_timer_get_time() / 1000ULL);
    for (size_t i = 0; i < s_num_signals; i++) {
        if (strcmp(s_signals[i].name, signal_name) == 0) {
            if (s_signals[i].valid && (now_ms - s_signals[i].last_update_ms < 3000)) {
                *out_value = s_signals[i].current_val;
                return true;
            }
        }
    }
    return false;
}

void task_can_bus_manager(void *pvParameters) {
    ESP_LOGI(TAG, "CAN-Bus Manager Task running on Core 0.");

    twai_message_t rx_msg;
    uint32_t last_fps_calc_ms = 0;
    uint32_t fps_frame_counter = 0;

    while (true) {
        if (!s_can_initialized) {
            vTaskDelay(pdMS_TO_TICKS(1000));
            continue;
        }

        // CAN-Frame empfangen (50 ms Timeout)
        esp_err_t ret = twai_receive(&rx_msg, pdMS_TO_TICKS(50));
        uint32_t now_ms = (uint32_t)(esp_timer_get_time() / 1000ULL);

        if (ret == ESP_OK) {
            s_can_traffic_active = true;
            s_rx_msg_count++;
            fps_frame_counter++;

            // Fingerprint Scan Tracking
            if (s_fingerprint_scan_active) {
                bool already_seen = false;
                for (size_t k = 0; k < s_seen_id_count; k++) {
                    if (s_seen_ids[k] == rx_msg.identifier) {
                        already_seen = true;
                        break;
                    }
                }
                if (!already_seen && s_seen_id_count < 32) {
                    s_seen_ids[s_seen_id_count++] = rx_msg.identifier;
                }
            }

            // Dynamisches Parsen nach aktiver Signal-Tabelle
            for (size_t i = 0; i < s_num_signals; i++) {
                if (s_signals[i].can_id == rx_msg.identifier) {
                    uint64_t raw = extract_raw_bits(
                        rx_msg.data,
                        rx_msg.data_length_code,
                        s_signals[i].start_bit,
                        s_signals[i].length_bits,
                        s_signals[i].is_big_endian
                    );
                    float val = ((float)raw * s_signals[i].scale) + s_signals[i].offset;
                    s_signals[i].current_val = val;
                    s_signals[i].last_update_ms = now_ms;
                    s_signals[i].valid = true;

                    // Sensor-Fusion Schnittstelle mit ADR-EKF (Raddrehzahl)
                    if (strcmp(s_signals[i].name, "speed_kmh") == 0 ||
                        strcmp(s_signals[i].name, "wheel_speed_rear") == 0) {
                        s_last_vehicle_speed_kmh = val;
                        adr_ekf_update_can_wheel_speed(val);
                    }
                }
            }
        }

        // FPS Berechnung jede Sekunde
        if (now_ms - last_fps_calc_ms >= 1000) {
            s_current_fps = (float)fps_frame_counter * 1000.0f / (float)(now_ms - last_fps_calc_ms);
            fps_frame_counter = 0;
            last_fps_calc_ms = now_ms;

            // Fingerprint Auto-Scan Timeout Check (500 ms)
            if (s_fingerprint_scan_active && (esp_timer_get_time() - s_fingerprint_start_us > 500000ULL)) {
                s_fingerprint_scan_active = false;
                // Match signature
                bool has_280 = false, has_290 = false;
                bool has_130 = false, has_2a0 = false;
                bool has_7e8 = false;

                for (size_t k = 0; k < s_seen_id_count; k++) {
                    if (s_seen_ids[k] == 0x280) has_280 = true;
                    if (s_seen_ids[k] == 0x290) has_290 = true;
                    if (s_seen_ids[k] == 0x130) has_130 = true;
                    if (s_seen_ids[k] == 0x2A0) has_2a0 = true;
                    if (s_seen_ids[k] == 0x7E8) has_7e8 = true;
                }

                if (has_280 && has_290) {
                    strncpy(s_detected_profile_id, "harley_skyline_2024", sizeof(s_detected_profile_id));
                    ESP_LOGI(TAG, "Fingerprint match: Harley-Davidson Skyline OS detected!");
                } else if (has_130 && has_2a0) {
                    strncpy(s_detected_profile_id, "bmw_motorrad_k5x_r1250_r1300", sizeof(s_detected_profile_id));
                    ESP_LOGI(TAG, "Fingerprint match: BMW Motorrad K5x/K6x detected!");
                } else if (has_7e8) {
                    strncpy(s_detected_profile_id, "generic_obd2_iso15765", sizeof(s_detected_profile_id));
                    ESP_LOGI(TAG, "Fingerprint match: Generic Euro 4/5 OBD2 detected!");
                } else {
                    strncpy(s_detected_profile_id, "unknown", sizeof(s_detected_profile_id));
                    ESP_LOGI(TAG, "Fingerprint scan complete: No distinct profile match (%d IDs seen).", (int)s_seen_id_count);
                }
            }
        }
    }
}

void can_bus_send_remote_battery_warning(uint8_t battery_pct) {
    if (!s_can_initialized || s_listen_only_mode) return;

    twai_message_t tx_msg = {};
    tx_msg.identifier = 0x5F0;
    tx_msg.extd = 0;
    tx_msg.data_length_code = 4;
    tx_msg.data[0] = 0x01; // Alert Type: Remote Battery Low
    tx_msg.data[1] = battery_pct;
    tx_msg.data[2] = 0x00;
    tx_msg.data[3] = 0xAA;

    esp_err_t ret = twai_transmit(&tx_msg, pdMS_TO_TICKS(50));
    if (ret == ESP_OK) {
        ESP_LOGI(TAG, "Transmitted Handlebar Remote Low-Battery Warning (%d%%) to CAN-Bus.", battery_pct);
    }
}

bool can_bus_is_connected(void) {
    return s_can_traffic_active;
}

bool can_bus_is_listen_only(void) {
    return s_listen_only_mode;
}

float can_bus_get_vehicle_speed_kmh(void) {
    return s_last_vehicle_speed_kmh;
}

uint32_t can_bus_get_rx_count(void) {
    return s_rx_msg_count;
}

float can_bus_get_fps(void) {
    return s_current_fps;
}

esp_err_t can_bus_start_fingerprint_scan(void) {
    s_seen_id_count = 0;
    s_fingerprint_start_us = esp_timer_get_time();
    s_fingerprint_scan_active = true;
    strcpy(s_detected_profile_id, "");
    ESP_LOGI(TAG, "Started 500 ms passive CAN bus fingerprint scan...");
    return ESP_OK;
}

bool can_bus_is_fingerprint_scan_running(void) {
    return s_fingerprint_scan_active;
}

const char* can_bus_get_detected_profile_id(void) {
    return s_detected_profile_id;
}
