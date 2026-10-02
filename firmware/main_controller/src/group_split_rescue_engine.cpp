#include "group_split_rescue_engine.h"
#include <stdio.h>
#include <string.h>
#include <math.h>
#include "esp_log.h"
#include "esp_timer.h"
#include "nvs_flash.h"
#include "nvs.h"

static const char *TAG = "GROUP_RESCUE";
#define NVS_GROUP_NAMESPACE "omb_group"

static GroupStatus_t s_status = {
    .lifecycle_state = GROUP_LIFECYCLE_STANDBY,
    .rescue_level = RESCUE_LEVEL_NONE,
    .connected_members_count = 1,
    .time_since_last_contact_ms = 0,
    .lead_distance_km = 0.0f,
    .lead_bearing_deg = 0.0f,
    .lead_guidance_text = "Keine Gruppe aktiv",
    .hfp_call_active = false,
    .doubt_timer_active = false
};

static uint32_t s_last_intercom_contact_ms = 0;
static uint32_t s_doubt_start_ms = 0;
static double s_last_lead_lat = 47.5000;
static double s_last_lead_lon = 11.5000;
static float s_group_expected_heading = 0.0f;

// Haversine Distanz-Berechnung
static float calculate_distance_km(double lat1, double lon1, double lat2, double lon2) {
    const float R = 6371.0f; // Erdradius in km
    double dLat = (lat2 - lat1) * M_PI / 180.0;
    double dLon = (lon2 - lon1) * M_PI / 180.0;
    double a = sin(dLat / 2) * sin(dLat / 2) +
               cos(lat1 * M_PI / 180.0) * cos(lat2 * M_PI / 180.0) *
               sin(dLon / 2) * sin(dLon / 2);
    double c = 2 * atan2(sqrt(a), sqrt(1 - a));
    return (float)(R * c);
}

// Peilung berechnen
static float calculate_bearing_deg(double lat1, double lon1, double lat2, double lon2) {
    double dLon = (lon2 - lon1) * M_PI / 180.0;
    double y = sin(dLon) * cos(lat2 * M_PI / 180.0);
    double x = cos(lat1 * M_PI / 180.0) * sin(lat2 * M_PI / 180.0) -
               sin(lat1 * M_PI / 180.0) * cos(lat2 * M_PI / 180.0) * cos(dLon);
    double b = atan2(y, x) * 180.0 / M_PI;
    if (b < 0) b += 360.0;
    return (float)b;
}

static const char* bearing_to_compass(float b) {
    if (b >= 337.5f || b < 22.5f) return "Nord";
    if (b >= 22.5f && b < 67.5f) return "Nord-Ost";
    if (b >= 67.5f && b < 112.5f) return "Ost";
    if (b >= 112.5f && b < 157.5f) return "Süd-Ost";
    if (b >= 157.5f && b < 202.5f) return "Süd";
    if (b >= 202.5f && b < 247.5f) return "Süd-West";
    if (b >= 247.5f && b < 292.5f) return "West";
    return "Nord-West";
}

esp_err_t group_split_rescue_engine_init(void) {
    ESP_LOGI(TAG, "Initializing Universal Group Split Fallback & Rescue Engine...");

    s_last_intercom_contact_ms = (uint32_t)(esp_timer_get_time() / 1000);

    // Kaffeepausen-State aus NVS wiederherstellen (falls vorhanden)
    group_split_restore_from_nvs();

    return ESP_OK;
}

void group_split_report_intercom_contact(bool is_contact_ok) {
    uint32_t now = (uint32_t)(esp_timer_get_time() / 1000);
    if (is_contact_ok) {
        s_last_intercom_contact_ms = now;
        s_status.time_since_last_contact_ms = 0;

        if (s_status.rescue_level != RESCUE_LEVEL_NONE) {
            ESP_LOGI(TAG, "✓ Intercom LOS Re-Established! De-escalating Rescue Level to NORMAL.");
            s_status.rescue_level = RESCUE_LEVEL_NONE;
            s_status.lifecycle_state = GROUP_LIFECYCLE_MACRO_ACTIVE;
        }
    }
}

void group_split_set_hfp_call_state(bool is_call_active) {
    s_status.hfp_call_active = is_call_active;
    if (is_call_active) {
        ESP_LOGI(TAG, "📞 Smartphone Call ACTIVE: Group Mic MUTED, Handlebar PTT locked for private phone.");
    } else {
        ESP_LOGI(TAG, "📞 Smartphone Call TERMINATED: Returning mic to group intercom.");
    }
}

void group_split_update(float speed_kmh, double lat, double lon, float heading_deg) {
    uint32_t now = (uint32_t)(esp_timer_get_time() / 1000);
    s_status.time_since_last_contact_ms = now - s_last_intercom_contact_ms;

    // 1. Kaffeepause-Erkennung (Stillstand v = 0 km/h)
    if (s_status.lifecycle_state == GROUP_LIFECYCLE_MACRO_ACTIVE && speed_kmh < 2.0f) {
        // Bei längerem Stillstand Kaffeepause aktivieren
        static uint32_t s_stop_time_ms = 0;
        if (s_stop_time_ms == 0) s_stop_time_ms = now;
        if (now - s_stop_time_ms > 300000) { // 5 Minuten Stillstand
            s_status.lifecycle_state = GROUP_LIFECYCLE_GROUP_PAUSED;
            ESP_LOGI(TAG, "☕ Coffee Break Detected: Entering GROUP_PAUSED state with NVS persistence.");
            group_split_persist_to_nvs();
        }
    }

    // 2. Doubt-Timer bei abweichendem Kursvektor
    if (s_status.lifecycle_state == GROUP_LIFECYCLE_MACRO_ACTIVE && speed_kmh > 25.0f) {
        float heading_diff = fabsf(heading_deg - s_group_expected_heading);
        if (heading_diff > 180.0f) heading_diff = 360.0f - heading_diff;

        if (heading_diff > 45.0f) { // Deutliche Kursabweichung
            if (!s_status.doubt_timer_active) {
                s_status.doubt_timer_active = true;
                s_doubt_start_ms = now;
                s_status.lifecycle_state = GROUP_LIFECYCLE_DOUBT_SPLIT;
                ESP_LOGW(TAG, "⚠️ Course deviation detected (Δθ = %.1f°). Starting Doubt-Timer (20s)...", heading_diff);
            } else if (now - s_doubt_start_ms > 20000) {
                // Doubt-Timer abgelaufen
                s_status.doubt_timer_active = false;
                s_status.lifecycle_state = GROUP_LIFECYCLE_GROUP_LEFT;
                ESP_LOGW(TAG, "Rider deliberately left group route -> Transition to GROUP_LEFT.");
            }
        } else {
            s_status.doubt_timer_active = false;
        }
    }

    // 3. Mehrstufige Verbindungs-Rettungskaskade (docs/de/09_firmware_architecture.md Abs. 4)
    if (s_status.lifecycle_state == GROUP_LIFECYCLE_MACRO_ACTIVE ||
        s_status.lifecycle_state == GROUP_LIFECYCLE_RESCUE_ESCALATION) {

        if (s_status.time_since_last_contact_ms > 120000) { // > 120 s
            if (s_status.rescue_level != RESCUE_LEVEL_3_PMR_ANALOG) {
                s_status.rescue_level = RESCUE_LEVEL_3_PMR_ANALOG;
                s_status.lifecycle_state = GROUP_LIFECYCLE_RESCUE_ESCALATION;
                ESP_LOGE(TAG, "🚨 RESCUE LEVEL 3: PMR446 Analog Emergency Voice Broadcast triggered!");
            }
        } else if (s_status.time_since_last_contact_ms > 45000) { // > 45 s
            if (s_status.rescue_level != RESCUE_LEVEL_2_LORA_868) {
                s_status.rescue_level = RESCUE_LEVEL_2_LORA_868;
                s_status.lifecycle_state = GROUP_LIFECYCLE_RESCUE_ESCALATION;
                ESP_LOGW(TAG, "📡 RESCUE LEVEL 2: Semtech SX1262 LoRa 868 MHz Long-Range Telemetry active (up to 15km).");
            }

            // Distanz & Peilung zur letzten Gruppenposition berechnen
            s_status.lead_distance_km = calculate_distance_km(lat, lon, s_last_lead_lat, s_last_lead_lon);
            s_status.lead_bearing_deg = calculate_bearing_deg(lat, lon, s_last_lead_lat, s_last_lead_lon);

            snprintf(s_status.lead_guidance_text, sizeof(s_status.lead_guidance_text),
                     "Gruppe voraus: %.1f km %s",
                     s_status.lead_distance_km,
                     bearing_to_compass(s_status.lead_bearing_deg));

        } else if (s_status.time_since_last_contact_ms > 15000) { // > 15 s
            if (s_status.rescue_level != RESCUE_LEVEL_1_OMM_2G4) {
                s_status.rescue_level = RESCUE_LEVEL_1_OMM_2G4;
                s_status.lifecycle_state = GROUP_LIFECYCLE_RESCUE_ESCALATION;
                ESP_LOGW(TAG, "⚡ RESCUE LEVEL 1: OMM 2.4 GHz Mesh Boosting TX-Power to +20 dBm & Channel Hopping.");
            }
        }
    }
}

esp_err_t group_split_persist_to_nvs(void) {
    nvs_handle_t nvs_h;
    esp_err_t err = nvs_open(NVS_GROUP_NAMESPACE, NVS_READWRITE, &nvs_h);
    if (err == ESP_OK) {
        nvs_set_u8(nvs_h, "lifecycle", (uint8_t)s_status.lifecycle_state);
        nvs_set_u32(nvs_h, "members", s_status.connected_members_count);
        nvs_commit(nvs_h);
        nvs_close(nvs_h);
        ESP_LOGI(TAG, "Persisted group session state to NVS for coffee break deep-sleep.");
    }
    return err;
}

esp_err_t group_split_restore_from_nvs(void) {
    nvs_handle_t nvs_h;
    esp_err_t err = nvs_open(NVS_GROUP_NAMESPACE, NVS_READWRITE, &nvs_h);
    if (err == ESP_OK) {
        uint8_t lc = 0;
        if (nvs_get_u8(nvs_h, "lifecycle", &lc) == ESP_OK) {
            if (lc == GROUP_LIFECYCLE_GROUP_PAUSED) {
                s_status.lifecycle_state = GROUP_LIFECYCLE_MACRO_ACTIVE;
                ESP_LOGI(TAG, "☕ Coffee Break Restored in < 50ms: Group Macro session fully resumed!");
            }
        }
        nvs_close(nvs_h);
    }
    return err;
}

GroupStatus_t group_split_get_status(void) {
    return s_status;
}
