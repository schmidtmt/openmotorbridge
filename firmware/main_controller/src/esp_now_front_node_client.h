#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    bool is_linked;
    uint8_t ottocast_state;
    bool ottocast_power_on;
    bool ottocast_fault;
    uint32_t cafe_countdown_sec;
    uint8_t ambient_dba;
    uint64_t last_seen_us;

    // Action-Cam BLE Subsystem Status
    uint8_t cam_profile;          // 0=None, 1=GoPro, 2=Insta360, 3=DJI Action / Osmo 360
    uint8_t cam_state;            // 0=Disconnected, 1=Scanning, 2=Connecting, 3=Connected, 4=Recording
    uint8_t cam_battery_pct;      // 0-100%
    uint16_t cam_sd_min_rem;      // Minutes remaining SD capacity
    bool cam_autoconnect_en;      // Persistent autoconnect flag
    bool cam_fuel_filter_en;      // KL15 Tankpausen-Filter active
} FrontNodeStatus;

/**
 * @brief Initializes ESP-NOW link to the Universal Front Node
 */
esp_err_t esp_now_front_node_init(void);

/**
 * @brief Returns the latest telemetry & status from Front Node
 */
FrontNodeStatus esp_now_front_node_get_status(void);

/**
 * @brief Sends a 1-click reboot command to the Ottocast USB power switch
 */
esp_err_t esp_now_front_node_reboot_ottocast(void);

/**
 * @brief Synchronizes vehicle ignition state (KL15) with the Front Node
 */
esp_err_t esp_now_front_node_set_ignition(bool ignition_on);

/**
 * @brief Action-Cam Remote Control Commands sent to Front Node
 */
esp_err_t esp_now_front_node_cam_toggle_rec(void);
esp_err_t esp_now_front_node_cam_hilight_tag(void);
esp_err_t esp_now_front_node_cam_start_scan(void);
esp_err_t esp_now_front_node_cam_pair(const uint8_t* mac, uint8_t profile, const char* name);
esp_err_t esp_now_front_node_cam_unpair(void);
esp_err_t esp_now_front_node_cam_set_autoconnect(bool enable);
esp_err_t esp_now_front_node_cam_set_fuel_filter(bool enable);

#ifdef __cplusplus
}
#endif

