#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"
#include "usb_vehicle_backbone.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge v10.0 - USB Radar 2.0 & 5.9 GHz C-ITS V2X Telemetry Parser
// Processes:
//   - USB_PKT_RADAR_TARGETS (0x30): 20 Hz Wheeltec MR20 24 GHz Target List
//   - USB_PKT_V2X_CITS_EVENT (0x32): 5.9 GHz 802.11p OCB C-ITS (SPATEM/GLOSA, DENM)
// Dispatches:
//   - Audio DSP Prio-1 Ducking (-18 dB) & Dual-Tone Alert
//   - Mirror BSD LEDs (USB_PKT_BSD_TRIGGER 0x07)
//   - Dual Cockpit Speaker-Corner OLED HUD (USB_PKT_COCKPIT_HUD_STATE 0x08)
//   - Auto Dashcam Event-Tagging on Prio-1 Threat (TTC < 2.5s)
// =============================================================================

typedef struct {
    bool     radar_online;
    uint32_t last_frame_time_ms;
    uint8_t  target_count;
    uint8_t  highest_threat_level; // 0 = None, 1 = Caution (Amber), 2 = Imminent Collision (Prio-1)
    uint16_t min_ttc_ms;
    uint16_t closest_dist_cm;
    int16_t  closing_speed_cm_s;
    bool     urgent_alert_active;

    // 5.9 GHz C-ITS / ITS-G5 (IEEE 802.11p OCB) V2X State
    bool     v2x_glosa_active;
    uint8_t  v2x_traffic_light_phase; // 1=Green, 2=Yellow, 3=Red
    uint8_t  v2x_time_to_change_s;
    uint8_t  v2x_recommended_speed_kph;
    uint8_t  v2x_denm_hazard_cause;   // e.g. 95=EmergencyVehicle, 91=Breakdown
    uint16_t v2x_station_distance_m;
} RadarOverview_t;

/**
 * @brief Initialisiert den v10.0 USB Radar 2.0 & 5.9 GHz C-ITS V2X Parser
 */
esp_err_t uwb_radar_parser_init(void);

/**
 * @brief Gibt die aktuelle Übersicht der Radarziele und 5.9 GHz V2X C-ITS Events zurück
 */
RadarOverview_t uwb_radar_get_overview(void);

#ifdef __cplusplus
}
#endif
