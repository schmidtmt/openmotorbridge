#include "uwb_radar_parser.h"
#include "audio_dsp_pipeline.h"
#include "action_cam_ble_manager.h"
#include "group_split_rescue_engine.h"
#include <stdio.h>
#include <string.h>
#include "esp_log.h"
#include "esp_timer.h"

static const char *TAG = "USB_RADAR_V2X";

static RadarOverview_t s_radar_overview = {};
static uint32_t s_last_threat_trigger_ms = 0;

static void dispatch_cockpit_oled_hud_update(uint8_t left_threat, uint8_t right_threat) {
    UsbCockpitHudStatePkt hud = {};
    hud.left_threat_level  = left_threat;
    hud.right_threat_level = right_threat;
    hud.closest_rear_dist_m = s_radar_overview.closest_dist_cm / 10;
    hud.glosa_active       = s_radar_overview.v2x_glosa_active ? 1 : 0;
    hud.glosa_phase        = s_radar_overview.v2x_traffic_light_phase;
    hud.glosa_rec_speed_kph = s_radar_overview.v2x_recommended_speed_kph;
    hud.glosa_countdown_s  = s_radar_overview.v2x_time_to_change_s;
    hud.v2x_hazard_type    = (s_radar_overview.v2x_denm_hazard_cause == 95) ? 1 :
                             (s_radar_overview.v2x_denm_hazard_cause > 0)   ? 2 : 0;

    GroupStatus_t grp = group_split_get_status();
    hud.intercom_mode = grp.hfp_call_active ? 4 : (uint8_t)grp.lifecycle_state;
    hud.brightness_pct = 85;
    snprintf(hud.status_line, sizeof(hud.status_line), "%s",
             grp.hfp_call_active ? "TEL ANRUF AKTIV" : "OMM MESH BEREIT");

    UsbVehicleBackbone::instance().send_cockpit_hud_state(hud);
}

static void on_radar_targets_received(const UsbRadarTargetsPkt &pkt) {
    uint32_t now_ms = (uint32_t)(esp_timer_get_time() / 1000);
    s_radar_overview.radar_online = true;
    s_radar_overview.last_frame_time_ms = now_ms;
    s_radar_overview.target_count = pkt.target_count;

    uint8_t highest_threat = 0;
    uint8_t left_threat = 0;
    uint8_t right_threat = 0;
    uint16_t min_ttc = 0xFFFF;
    uint16_t closest_d = 0xFFFF;
    int16_t max_closing_spd = 0;

    for (int i = 0; i < pkt.target_count && i < USB_RADAR_MAX_TARGETS; i++) {
        const UsbRadarTargetEntry &tgt = pkt.targets[i];
        if (tgt.threat_level > highest_threat) {
            highest_threat = tgt.threat_level;
        }
        if (tgt.azimuth_deg_10 <= 0 && tgt.threat_level > left_threat) {
            left_threat = tgt.threat_level;
        }
        if (tgt.azimuth_deg_10 >= 0 && tgt.threat_level > right_threat) {
            right_threat = tgt.threat_level;
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

    if (s_radar_overview.urgent_alert_active) {
        if (now_ms - s_last_threat_trigger_ms > 1500) {
            s_last_threat_trigger_ms = now_ms;
            ESP_LOGW(TAG, "🚨 URGENT RADAR THREAT: Target %u cm, TTC: %u ms, Speed: %d cm/s! Triggering Prio-1 Ducking, Strobe & Auto-Cam Tag.",
                     s_radar_overview.closest_dist_cm, min_ttc, max_closing_spd);

            // 1. Audio DSP Prio-1 Ducking (-18 dB) & Warnton im Helm
            audio_trigger_radar_alert(2);

            // 2. Automated Dashcam Event-Tagging on Central Box BLE Master
            action_cam_trigger_hilight_tag("AUTO_RADAR_TTC");

            // 3. Spiegel-LEDs am Front-Knoten auf Fast Strobe schalten (per 4-Draht USB)
            UsbVehicleBackbone::instance().send_bsd_trigger(true, 2, true, 2);

            // 4. Heck-Radar Wings Makro auf Modus 3 (Hazard Prio-1 Strobe) setzen
            UsbVehicleBackbone::instance().send_radar_led_cmd(3, 100, 2, 2);
        }
    } else if (highest_threat == 1) {
        if (now_ms - s_last_threat_trigger_ms > 2500) {
            s_last_threat_trigger_ms = now_ms;
            audio_trigger_radar_alert(1);
            UsbVehicleBackbone::instance().send_bsd_trigger(left_threat > 0, left_threat, right_threat > 0, right_threat);
            UsbVehicleBackbone::instance().send_radar_led_cmd(2, 60, left_threat, right_threat);
        }
    }

    // Update Dual Cockpit Speaker-Corner OLED HUD (J_DISP_L & J_DISP_R on PCBA 05)
    dispatch_cockpit_oled_hud_update(left_threat, right_threat);
}

static void on_v2x_cits_event_received(const UsbV2xCitsEventPkt &evt) {
    s_radar_overview.v2x_station_distance_m = evt.distance_m;

    if (evt.v2x_msg_type == V2X_MSG_SPATEM) {
        s_radar_overview.v2x_glosa_active = true;
        s_radar_overview.v2x_traffic_light_phase = evt.traffic_light_phase;
        s_radar_overview.v2x_time_to_change_s = evt.time_to_change_s;
        s_radar_overview.v2x_recommended_speed_kph = evt.recommended_speed_kph;

        ESP_LOGI(TAG, "🚦 [5.9 GHz V2X SPATEM/GLOSA] RSU #%lu (%u m): Phase=%u, Switch in %u s -> Recommended Green-Wave Speed: %u km/h",
                 (unsigned long)evt.station_id, evt.distance_m,
                 evt.traffic_light_phase, evt.time_to_change_s, evt.recommended_speed_kph);

        dispatch_cockpit_oled_hud_update(0, 0);
    } else if (evt.v2x_msg_type == V2X_MSG_DENM) {
        s_radar_overview.v2x_denm_hazard_cause = evt.denm_cause_code;
        ESP_LOGW(TAG, "🚨 [5.9 GHz V2X DENM HAZARD] Station #%lu (%u m): CauseCode=%u (95=EmergencyVehicle, 91=Breakdown)!",
                 (unsigned long)evt.station_id, evt.distance_m, evt.denm_cause_code);

        // Trigger Prio-1 audible alert + Cockpit OLED Hazard warning
        audio_trigger_radar_alert(evt.denm_cause_code == 95 ? 2 : 1);
        dispatch_cockpit_oled_hud_update(2, 2);
    }
}

esp_err_t uwb_radar_parser_init(void) {
    ESP_LOGI(TAG, "Initializing v10.0 USB Radar 2.0 & 5.9 GHz C-ITS V2X Telemetry Parser...");
    memset(&s_radar_overview, 0, sizeof(s_radar_overview));

    UsbVehicleBackbone::instance().set_radar_targets_callback(on_radar_targets_received);
    UsbVehicleBackbone::instance().set_v2x_cits_callback(on_v2x_cits_event_received);
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
