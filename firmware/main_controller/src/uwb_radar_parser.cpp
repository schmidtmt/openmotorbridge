#include "uwb_radar_parser.h"
#include <string.h>
#include "esp_log.h"
#include "esp_timer.h"
#include "audio_dsp_pipeline.h"

static const char *TAG = "UWB_RADAR_PARSER";

static RadarOverview_t s_radar_overview = {};
static uint32_t s_last_threat_trigger_ms = 0;

static void on_radar_targets_received(const UwbRadarTargetsPkt &pkt) {
    uint32_t now_ms = (uint32_t)(esp_timer_get_time() / 1000);
    s_radar_overview.radar_online = true;
    s_radar_overview.last_frame_time_ms = now_ms;
    s_radar_overview.target_count = pkt.target_count;

    uint8_t highest_threat = 0;
    uint16_t min_ttc = 0xFFFF;
    uint16_t closest_d = 0xFFFF;
    int16_t max_closing_spd = 0;

    for (int i = 0; i < pkt.target_count && i < UWB_RADAR_MAX_TARGETS; i++) {
        const UwbRadarTargetEntry &tgt = pkt.targets[i];
        if (tgt.threat_level > highest_threat) {
            highest_threat = tgt.threat_level;
        }
        if (tgt.ttc_ms < min_ttc) {
            min_ttc = tgt.ttc_ms;
        }
        if (tgt.distance_cm < closest_d) {
            closest_d = tgt.distance_cm;
            max_closing_spd = tgt.speed_cm_s;
        }
    }

    s_radar_overview.highest_threat_level = highest_threat;
    s_radar_overview.min_ttc_ms = min_ttc;
    s_radar_overview.closest_dist_cm = (closest_d == 0xFFFF) ? 0 : closest_d;
    s_radar_overview.closing_speed_cm_s = max_closing_spd;
    s_radar_overview.urgent_alert_active = (highest_threat == 2 || pkt.urgent_flag != 0);

    // Kollisionswarnung auslösen wenn Prio-1 Threat erkannt
    if (s_radar_overview.urgent_alert_active) {
        if (now_ms - s_last_threat_trigger_ms > 1500) { // Entprellung für Doppelton
            s_last_threat_trigger_ms = now_ms;
            ESP_LOGW(TAG, "URGENT RADAR THREAT: Closest target %u cm, TTC: %u ms, Speed: %d cm/s! Triggering Audio Ducking Prio 1 & Strobe.",
                     s_radar_overview.closest_dist_cm, min_ttc, max_closing_spd);

            // 1. Audio DSP Prio-1 Ducking (-18 dB) & Warnton im Helm
            audio_trigger_radar_alert(2);

            // 2. Spiegel-LEDs am Front-Knoten auf Fast Strobe schalten (per UWB)
            uint8_t bsd_cmd[4] = {1, 2, 1, 2}; // Left active (Fast Strobe), Right active (Fast Strobe)
            UwbVehicleBackbone::instance().send_packet(UWB_NODE_FRONT_NODE, UWB_PKT_BSD_TRIGGER, bsd_cmd, sizeof(bsd_cmd));

            // 3. Heck-Radar Wings Makro auf Modus 3 (Hazard Prio-1 Strobe) setzen
            UwbVehicleBackbone::instance().send_radar_led_cmd(3, 100, 2, 2);
        }
    } else if (highest_threat == 1) {
        if (now_ms - s_last_threat_trigger_ms > 2500) {
            s_last_threat_trigger_ms = now_ms;
            // Gelbe Vorwarnung
            audio_trigger_radar_alert(1);
            uint8_t bsd_cmd[4] = {1, 1, 1, 1}; // Amber Solid
            UwbVehicleBackbone::instance().send_packet(UWB_NODE_FRONT_NODE, UWB_PKT_BSD_TRIGGER, bsd_cmd, sizeof(bsd_cmd));
            UwbVehicleBackbone::instance().send_radar_led_cmd(2, 60, 1, 1);
        }
    }
}

esp_err_t uwb_radar_parser_init(void) {
    ESP_LOGI(TAG, "Initializing UWB Radar Telemetry Parser...");
    memset(&s_radar_overview, 0, sizeof(s_radar_overview));

    // Callback beim UWB Backbone registrieren
    UwbVehicleBackbone::instance().set_radar_targets_callback(on_radar_targets_received);
    return ESP_OK;
}

RadarOverview_t uwb_radar_get_overview(void) {
    uint32_t now_ms = (uint32_t)(esp_timer_get_time() / 1000);
    if (s_radar_overview.radar_online && (now_ms - s_radar_overview.last_frame_time_ms > 1000)) {
        s_radar_overview.radar_online = false;
        s_radar_overview.highest_threat_level = 0;
        s_radar_overview.urgent_alert_active = false;
    }
    return s_radar_overview;
}
