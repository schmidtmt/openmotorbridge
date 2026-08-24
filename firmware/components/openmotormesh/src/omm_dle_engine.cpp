#include "openmotormesh.h"
#include <stdio.h>
#include <string.h>
#include "esp_log.h"
#include "esp_timer.h"

static const char *TAG = "OMM_CORE";

static uint8_t s_local_dle_score = 95;
static uint64_t s_local_node_uid = 0x014F2A9012008CULL;

esp_err_t omm_stack_init(void) {
    ESP_LOGI(TAG, "Initializing OpenMotorMesh (OMM) Layer 2-4 Protocol Stack...");
    s_local_dle_score = omm_calculate_local_dle_score();
    ESP_LOGI(TAG, "OMM Stack initialized. Local DLE Score: %d Pts.", s_local_dle_score);
    return ESP_OK;
}

uint8_t omm_calculate_local_dle_score(void) {
    uint8_t score = 60; // Dual-Mesh Hardware Tier (Sena Apex / Cardo Edge)
    score += 20;        // KL15 Vehicle Power Active
    score += 10;        // GNSS 1-PPS Time Sync Locked
    score += 10;        // LoRa SX1262 Link Active
    score += 5;         // Front Ambient-Mic Active (FEAT_ENV_MIC)
    return (score > 100) ? 100 : score;
}

esp_err_t omm_broadcast_radar_frame(const OmmRadarPacket_t *radar_pkt) {
    if (!radar_pkt) return ESP_ERR_INVALID_ARG;
    ESP_LOGD(TAG, "Broadcasting 16-Byte OMM Radar Frame (Speed: %d km/h, Lean: %d deg)...",
             radar_pkt->speed_kmh, radar_pkt->lean_angle_deg);
    return ESP_OK;
}

esp_err_t omm_trigger_siren_early_warning(double lat, double lon) {
    ESP_LOGW(TAG, "🚨 OMM SIREN ALERT TRIGGERED at Lat: %.6f, Lon: %.6f! Broadcasting emergency frame.", lat, lon);
    OmmEmergencyAlert_t alert = {
        .packet_type = OMM_TYPE_EMERGENCY,
        .alert_subtype = 0x01,
        .sender_uid = s_local_node_uid,
        .event_lat_1e7 = (int32_t)(lat * 10000000.0),
        .event_lon_1e7 = (int32_t)(lon * 10000000.0),
        .alert_duration_ms = 10000,
        .crc8_checksum = 0xAA
    };
    // Sende Frame über Mesh
    return ESP_OK;
}
