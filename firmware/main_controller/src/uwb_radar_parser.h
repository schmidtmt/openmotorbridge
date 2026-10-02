#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"
#include "uwb_vehicle_backbone.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    bool     radar_online;
    uint32_t last_frame_time_ms;
    uint8_t  target_count;
    uint8_t  highest_threat_level; // 0 = None, 1 = Caution (Amber), 2 = Imminent Collision (Prio-1)
    uint16_t min_ttc_ms;
    uint16_t closest_dist_cm;
    int16_t  closing_speed_cm_s;
    bool     urgent_alert_active;
} RadarOverview_t;

/**
 * @brief Initialisiert den UWB Radar Parser & Kollisions-Überwacher
 */
esp_err_t uwb_radar_parser_init(void);

/**
 * @brief Gibt die aktuelle Übersicht der Radarziele zurück
 */
RadarOverview_t uwb_radar_get_overview(void);

#ifdef __cplusplus
}
#endif
