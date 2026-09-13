#include "tpms_ble_scanner.h"
#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "nvs_flash.h"
#include "nvs.h"
#include "nimble/nimble_port.h"
#include "host/ble_hs.h"
#include "host/ble_gap.h"
#include "ble_service_server.h"

static const char *TAG = "TPMS_SCANNER";

#define NVS_NAMESPACE_TPMS "omb_tpms"
#define FOBO_SERVICE_UUID  0xFBB0
#define DEELIFE_SERVICE_UUID 0x27A5

static SemaphoreHandle_t s_tpms_mutex = NULL;
static tpms_sensor_val_t s_front_val = { 2.45f, 24, 95, {0}, 0, true };
static tpms_sensor_val_t s_rear_val  = { 2.80f, 26, 92, {0}, 0, true };

static uint8_t s_learned_front_mac[6] = {0};
static uint8_t s_learned_rear_mac[6]  = {0};
static bool s_has_learned_front = false;
static bool s_has_learned_rear  = false;

static bool s_scanner_active = false;
static bool s_learning_active = false;
static tpms_wheel_pos_t s_learn_pos = TPMS_WHEEL_FRONT;
static int64_t s_learn_timeout_us = 0;

static void load_learned_sensors_nvs(void) {
    nvs_handle_t nvs;
    if (nvs_open(NVS_NAMESPACE_TPMS, NVS_READONLY, &nvs) == ESP_OK) {
        size_t len = 6;
        if (nvs_get_blob(nvs, "mac_front", s_learned_front_mac, &len) == ESP_OK && len == 6) {
            s_has_learned_front = true;
            ESP_LOGI(TAG, "Loaded Front TPMS MAC: %02X:%02X:%02X:%02X:%02X:%02X",
                     s_learned_front_mac[0], s_learned_front_mac[1], s_learned_front_mac[2],
                     s_learned_front_mac[3], s_learned_front_mac[4], s_learned_front_mac[5]);
        }
        len = 6;
        if (nvs_get_blob(nvs, "mac_rear", s_learned_rear_mac, &len) == ESP_OK && len == 6) {
            s_has_learned_rear = true;
            ESP_LOGI(TAG, "Loaded Rear TPMS MAC: %02X:%02X:%02X:%02X:%02X:%02X",
                     s_learned_rear_mac[0], s_learned_rear_mac[1], s_learned_rear_mac[2],
                     s_learned_rear_mac[3], s_learned_rear_mac[4], s_learned_rear_mac[5]);
        }
        nvs_close(nvs);
    }
}

static void save_learned_sensor_nvs(tpms_wheel_pos_t pos, const uint8_t *mac) {
    nvs_handle_t nvs;
    if (nvs_open(NVS_NAMESPACE_TPMS, NVS_READWRITE, &nvs) == ESP_OK) {
        const char *key = (pos == TPMS_WHEEL_FRONT) ? "mac_front" : "mac_rear";
        nvs_set_blob(nvs, key, mac, 6);
        nvs_commit(nvs);
        nvs_close(nvs);
        ESP_LOGI(TAG, "Saved %s TPMS MAC to NVS", (pos == TPMS_WHEEL_FRONT) ? "Front" : "Rear");
    }
}

// Decodes manufacturer / service data payload from FOBO or Deelife caps
static bool decode_tpms_payload(const uint8_t *data, uint8_t len, float *out_bar, int8_t *out_temp, uint8_t *out_bat) {
    if (!data || len < 6) return false;

    // Format A: Standard Deelife / Generic Motorcycle BLE TPMS (16-bit pressure in kPa, 8-bit temp with offset)
    // Packet layout: [0x00..0x01: Pressure_kPa (big-endian), 0x02: Temp_C (offset -40 or raw), 0x03: Battery %]
    uint16_t pressure_kpa = (data[0] << 8) | data[1];
    float bar = pressure_kpa / 100.0f;
    
    // Sanity check: motorcycle tire pressure usually between 1.0 and 4.5 bar
    if (bar >= 0.8f && bar <= 5.0f) {
        *out_bar = bar;
        *out_temp = (int8_t)(data[2] - 40); // 40 degree offset
        *out_bat = (len > 3) ? data[3] : 90;
        return true;
    }

    // Format B: FOBO Bike 2 (32-bit float or 16-bit 0.1 PSI)
    // If pressure in 0.1 PSI:
    uint16_t psi_tenth = (data[1] << 8) | data[0];
    float bar_from_psi = (psi_tenth * 0.1f) * 0.0689476f;
    if (bar_from_psi >= 0.8f && bar_from_psi <= 5.0f) {
        *out_bar = bar_from_psi;
        *out_temp = (int8_t)data[2];
        *out_bat = (len > 3) ? data[3] : 90;
        return true;
    }

    return false;
}

static int tpms_gap_event(struct ble_gap_event *event, void *arg) {
    if (event->type == BLE_GAP_EVENT_DISC) {
        const struct ble_gap_disc_desc *disc = &event->disc;
        
        float bar = 0.0f;
        int8_t temp = 0;
        uint8_t bat = 0;

        // Parse fields in advertisement
        struct ble_hs_adv_fields fields;
        if (ble_hs_adv_parse_fields(&fields, disc->data, disc->length_data) == 0) {
            bool parsed = false;

            // Check manufacturer data first
            if (fields.mfg_data != NULL && fields.mfg_data_len >= 6) {
                parsed = decode_tpms_payload(fields.mfg_data, fields.mfg_data_len, &bar, &temp, &bat);
            }
            // Fallback: check 16-bit service data
            if (!parsed && fields.svc_data_uuid16 != NULL && fields.svc_data_uuid16_len >= 6) {
                parsed = decode_tpms_payload(fields.svc_data_uuid16, fields.svc_data_uuid16_len, &bar, &temp, &bat);
            }

            if (parsed) {
                int64_t now_us = esp_timer_get_time();
                uint32_t now_ms = (uint32_t)(now_us / 1000);

                // Check learning mode
                if (s_learning_active) {
                    if (now_us < s_learn_timeout_us) {
                        if (s_learn_pos == TPMS_WHEEL_FRONT) {
                            memcpy(s_learned_front_mac, disc->addr.val, 6);
                            s_has_learned_front = true;
                            save_learned_sensor_nvs(TPMS_WHEEL_FRONT, s_learned_front_mac);
                        } else {
                            memcpy(s_learned_rear_mac, disc->addr.val, 6);
                            s_has_learned_rear = true;
                            save_learned_sensor_nvs(TPMS_WHEEL_REAR, s_learned_rear_mac);
                        }
                        ESP_LOGI(TAG, "Learned Sensor for %s", (s_learn_pos == TPMS_WHEEL_FRONT) ? "Front" : "Rear");
                        s_learning_active = false;
                    } else {
                        s_learning_active = false;
                    }
                }

                // Determine whether front or rear
                bool is_front = false;
                bool is_rear = false;

                if (s_has_learned_front && memcmp(disc->addr.val, s_learned_front_mac, 6) == 0) {
                    is_front = true;
                } else if (s_has_learned_rear && memcmp(disc->addr.val, s_learned_rear_mac, 6) == 0) {
                    is_rear = true;
                } else if (!s_has_learned_front && !s_has_learned_rear) {
                    // Auto-assign: lower MAC = front, higher MAC = rear
                    is_front = (disc->addr.val[0] % 2 == 0);
                    is_rear = !is_front;
                }

                if (xSemaphoreTake(s_tpms_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
                    if (is_front) {
                        s_front_val.pressure_bar = bar;
                        s_front_val.temp_c = temp;
                        s_front_val.battery_pct = bat;
                        memcpy(s_front_val.sensor_mac, disc->addr.val, 6);
                        s_front_val.last_seen_ms = now_ms;
                        s_front_val.valid = true;
                    }
                    if (is_rear) {
                        s_rear_val.pressure_bar = bar;
                        s_rear_val.temp_c = temp;
                        s_rear_val.battery_pct = bat;
                        memcpy(s_rear_val.sensor_mac, disc->addr.val, 6);
                        s_rear_val.last_seen_ms = now_ms;
                        s_rear_val.valid = true;
                    }

                    // Forward to GATT Server
                    ble_tpms_update(s_front_val.pressure_bar, s_rear_val.pressure_bar,
                                    s_front_val.temp_c, s_rear_val.temp_c);

                    xSemaphoreGive(s_tpms_mutex);
                }
            }
        }
    }
    return 0;
}

esp_err_t tpms_ble_scanner_init(void) {
    if (s_tpms_mutex == NULL) {
        s_tpms_mutex = xSemaphoreCreateMutex();
    }

    load_learned_sensors_nvs();
    ESP_LOGI(TAG, "TPMS BLE Scanner initialized successfully.");
    return tpms_ble_scanner_set_active(true);
}

esp_err_t tpms_ble_scanner_set_active(bool active) {
    if (active == s_scanner_active) return ESP_OK;

    if (active) {
        struct ble_gap_disc_params disc_params;
        memset(&disc_params, 0, sizeof(disc_params));
        disc_params.passive = 1;              // Passive scan: do not transmit SCAN_REQ
        disc_params.itvl = BLE_GAP_SCAN_ITVL_MS(250);
        disc_params.window = BLE_GAP_SCAN_WIN_MS(50);
        disc_params.filter_duplicates = 0;

        int rc = ble_gap_disc(BLE_OWN_ADDR_PUBLIC, BLE_HS_FOREVER, &disc_params, tpms_gap_event, NULL);
        if (rc != 0 && rc != BLE_HS_EALREADY) {
            ESP_LOGW(TAG, "ble_gap_disc failed (rc=%d)", rc);
            return ESP_FAIL;
        }
        s_scanner_active = true;
        ESP_LOGI(TAG, "TPMS Passive BLE Scan started.");
    } else {
        ble_gap_disc_cancel();
        s_scanner_active = false;
        ESP_LOGI(TAG, "TPMS Passive BLE Scan stopped.");
    }
    return ESP_OK;
}

esp_err_t tpms_ble_scanner_start_learn(tpms_wheel_pos_t pos) {
    s_learn_pos = pos;
    s_learn_timeout_us = esp_timer_get_time() + (15LL * 1000000LL); // 15 seconds
    s_learning_active = true;
    ESP_LOGI(TAG, "Started 15s TPMS learning mode for %s", (pos == TPMS_WHEEL_FRONT) ? "Front" : "Rear");
    return ESP_OK;
}

bool tpms_ble_scanner_get_values(tpms_sensor_val_t *out_front, tpms_sensor_val_t *out_rear) {
    if (s_tpms_mutex == NULL) return false;
    if (xSemaphoreTake(s_tpms_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
        if (out_front) *out_front = s_front_val;
        if (out_rear) *out_rear = s_rear_val;
        xSemaphoreGive(s_tpms_mutex);
        return true;
    }
    return false;
}
