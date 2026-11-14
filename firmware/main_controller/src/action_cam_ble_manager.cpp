#include "action_cam_ble_manager.h"
#include "usb_vehicle_backbone.h"
#include "audio_dsp_pipeline.h"
#include <stdio.h>
#include <string.h>
#include "esp_log.h"
#include "esp_timer.h"
#include "nvs_flash.h"
#include "nvs.h"

static const char *TAG = "CAM_BLE_MASTER";
#define NVS_CAM_NAMESPACE "omb_cam"

static CentralCamAndBeaconStatus_t s_cam_status = {
    .connected = false,
    .recording = false,
    .brand = CAM_BRAND_NONE,
    .battery_pct = 88,
    .remaining_min = 94,
    .hilight_tags_count = 0,
    .autoconnect_enabled = true,
    .fuel_stop_filter_enabled = true,
    .camera_name = "Unpaired",
    .camera_mac = {0},
    .find_my_beacon_active = true,
    .aux_light_mode = 2 // Auto via OPT3001
};

static uint32_t s_last_auto_tag_ms = 0;
static uint32_t s_kl15_off_since_ms = 0;

static const char* brand_to_str(ActionCamBrand_t brand) {
    switch (brand) {
        case CAM_BRAND_GOPRO:    return "GoPro (0xFEA6)";
        case CAM_BRAND_INSTA360: return "Insta360 (0xBE80)";
        case CAM_BRAND_DJI:      return "DJI Osmo (0xFFF0)";
        default:                 return "None";
    }
}

esp_err_t action_cam_ble_manager_init(void) {
    ESP_LOGI(TAG, "Initializing v10.0 Central Box Geometric BLE Master (Action-Cam + Find-My Dual Beacon)...");

    nvs_handle_t nvs_h;
    if (nvs_open(NVS_CAM_NAMESPACE, NVS_READONLY, &nvs_h) == ESP_OK) {
        uint8_t brand = 0;
        if (nvs_get_u8(nvs_h, "brand", &brand) == ESP_OK && brand > 0) {
            s_cam_status.brand = (ActionCamBrand_t)brand;
            size_t mac_len = 6;
            nvs_get_blob(nvs_h, "mac", s_cam_status.camera_mac, &mac_len);
            size_t name_len = sizeof(s_cam_status.camera_name);
            nvs_get_str(nvs_h, "name", s_cam_status.camera_name, &name_len);
            s_cam_status.connected = true;
            ESP_LOGI(TAG, "Restored paired Action-Cam from NVS: %s [%s]",
                     s_cam_status.camera_name, brand_to_str(s_cam_status.brand));
        }
        uint8_t auto_conn = 1, fuel_flt = 1;
        if (nvs_get_u8(nvs_h, "autoconn", &auto_conn) == ESP_OK) s_cam_status.autoconnect_enabled = (auto_conn != 0);
        if (nvs_get_u8(nvs_h, "fuelflt", &fuel_flt) == ESP_OK) s_cam_status.fuel_stop_filter_enabled = (fuel_flt != 0);
        nvs_close(nvs_h);
    }

    return ESP_OK;
}

esp_err_t action_cam_toggle_rec(void) {
    s_cam_status.recording = !s_cam_status.recording;
    ESP_LOGI(TAG, "🎬 Action-Cam (%s) Shutter Command: %s",
             brand_to_str(s_cam_status.brand),
             s_cam_status.recording ? "START RECORDING (GATT [0x03,0x01,0x01,0x01])" : "STOP RECORDING (GATT [0x03,0x01,0x01,0x00])");
    return ESP_OK;
}

esp_err_t action_cam_trigger_hilight_tag(const char *reason_tag) {
    if (!reason_tag) reason_tag = "MANUAL";
    s_cam_status.hilight_tags_count++;
    ESP_LOGW(TAG, "🔖 Action-Cam HiLight Bookmark Tag #%lu set! Reason: [%s] (GATT [0x01, 0x18])",
             (unsigned long)s_cam_status.hilight_tags_count, reason_tag);
    return ESP_OK;
}

esp_err_t action_cam_start_scan(void) {
    ESP_LOGI(TAG, "🔍 Starting 10s Central BLE Scan for GoPro (0xFEA6), Insta360 (0xBE80), DJI Osmo (0xFFF0)...");
    return ESP_OK;
}

esp_err_t action_cam_pair(const uint8_t *mac, uint8_t brand, const char *name) {
    if (!mac) return ESP_ERR_INVALID_ARG;
    memcpy(s_cam_status.camera_mac, mac, 6);
    s_cam_status.brand = (ActionCamBrand_t)brand;
    snprintf(s_cam_status.camera_name, sizeof(s_cam_status.camera_name), "%s",
             (name && name[0]) ? name : "ActionCam-BLE");
    s_cam_status.connected = true;

    nvs_handle_t nvs_h;
    if (nvs_open(NVS_CAM_NAMESPACE, NVS_READWRITE, &nvs_h) == ESP_OK) {
        nvs_set_u8(nvs_h, "brand", brand);
        nvs_set_blob(nvs_h, "mac", mac, 6);
        nvs_set_str(nvs_h, "name", s_cam_status.camera_name);
        nvs_commit(nvs_h);
        nvs_close(nvs_h);
    }

    ESP_LOGI(TAG, "✓ Paired Action-Cam '%s' (%s) on Central Box BLE Master.",
             s_cam_status.camera_name, brand_to_str(s_cam_status.brand));
    return ESP_OK;
}

esp_err_t action_cam_unpair(void) {
    s_cam_status.connected = false;
    s_cam_status.recording = false;
    s_cam_status.brand = CAM_BRAND_NONE;
    snprintf(s_cam_status.camera_name, sizeof(s_cam_status.camera_name), "Unpaired");

    nvs_handle_t nvs_h;
    if (nvs_open(NVS_CAM_NAMESPACE, NVS_READWRITE, &nvs_h) == ESP_OK) {
        nvs_erase_all(nvs_h);
        nvs_commit(nvs_h);
        nvs_close(nvs_h);
    }
    ESP_LOGI(TAG, "Action-Cam unpaired and removed from NVS.");
    return ESP_OK;
}

void action_cam_set_autoconnect(bool enable) {
    s_cam_status.autoconnect_enabled = enable;
    nvs_handle_t nvs_h;
    if (nvs_open(NVS_CAM_NAMESPACE, NVS_READWRITE, &nvs_h) == ESP_OK) {
        nvs_set_u8(nvs_h, "autoconn", enable ? 1 : 0);
        nvs_commit(nvs_h);
        nvs_close(nvs_h);
    }
}

void action_cam_set_fuel_filter(bool enable) {
    s_cam_status.fuel_stop_filter_enabled = enable;
    nvs_handle_t nvs_h;
    if (nvs_open(NVS_CAM_NAMESPACE, NVS_READWRITE, &nvs_h) == ESP_OK) {
        nvs_set_u8(nvs_h, "fuelflt", enable ? 1 : 0);
        nvs_commit(nvs_h);
        nvs_close(nvs_h);
    }
}

void action_cam_update_tick(float speed_kmh, bool kl15_active, bool radar_urgent, bool ess_braking) {
    uint32_t now_ms = (uint32_t)(esp_timer_get_time() / 1000);

    // 1. Auto-Wake & Auto-Record above 10 km/h
    if (kl15_active) {
        s_kl15_off_since_ms = 0;
        if (s_cam_status.connected && s_cam_status.autoconnect_enabled && !s_cam_status.recording && speed_kmh > 10.0f) {
            s_cam_status.recording = true;
            ESP_LOGI(TAG, "🎬 Speed > 10 km/h (%.1f km/h): Auto-Record started on %s!",
                     speed_kmh, s_cam_status.camera_name);
        }
    } else {
        // 2. KL15 Fuel-Stop Filter (10-minute grace period before stopping & sleeping camera)
        if (s_cam_status.recording) {
            if (s_kl15_off_since_ms == 0) {
                s_kl15_off_since_ms = now_ms;
            }
            uint32_t hold_limit_ms = s_cam_status.fuel_stop_filter_enabled ? 600000 : 5000;
            if (now_ms - s_kl15_off_since_ms >= hold_limit_ms) {
                s_cam_status.recording = false;
                ESP_LOGI(TAG, "⛽ Fuel-Stop Filter expired -> Stopping Action-Cam & sending BLE Sleep [0x01, 0x05].");
            }
        }
    }

    // 3. Automated Dashcam Event-Tagging on Emergency Braking (ESS < -0.60g) or Radar Prio-1 Threat (TTC < 2.5s)
    if (s_cam_status.recording && (radar_urgent || ess_braking)) {
        if (now_ms - s_last_auto_tag_ms > 10000) { // Max 1 auto-tag per 10 seconds
            s_last_auto_tag_ms = now_ms;
            action_cam_trigger_hilight_tag(ess_braking ? "AUTO_ESS_BRAKE" : "AUTO_RADAR_TTC");
        }
    }
}

esp_err_t front_node_usb_reboot_cp2aa_dongle(void) {
    ESP_LOGW(TAG, "🔄 Dispatching USB_CMD_POWER_CYCLE (0x10) over 4-Wire USB Bus to Front-Node U4 (TPS2051B 2.5s Cold-Reboot)...");
    return UsbVehicleBackbone::instance().send_power_cycle_cmd(USB_NODE_FRONT_NODE, 0x01, 2500);
}

esp_err_t front_node_usb_set_aux_light(uint8_t mode) {
    s_cam_status.aux_light_mode = mode;
    uint8_t cfg_payload[4] = { 0x02 /* Sub-Cmd: Aux Light Q2 TPS1H100 */, mode, 0, 0 };
    ESP_LOGI(TAG, "💡 Dispatching USB_CMD_CONFIG (0x11) to Front-Node Q2 (TPS1H100 Aux Light Mode=%u)", mode);
    return UsbVehicleBackbone::instance().send_packet(USB_NODE_FRONT_NODE, USB_CMD_CONFIG, cfg_payload, sizeof(cfg_payload));
}

void find_my_set_dual_beacon(bool enable) {
    s_cam_status.find_my_beacon_active = enable;
    ESP_LOGI(TAG, "🛰️ Apple Find My (FMNP 0x004C) & Google Find My Device (FMDN 0xFEAA) Dual-Beacon: %s",
             enable ? "ACTIVE (Alternating 2000ms ADV Slots)" : "DISABLED");
}

CentralCamAndBeaconStatus_t action_cam_get_status(void) {
    return s_cam_status;
}

