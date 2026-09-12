#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    bool is_linked;
    uint8_t binding_state;        // 0=Unpaired / Discovery, 1=Linked, 2=Orphan
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

    // 4-Port USB Hub Subsystem (USB2514B on PCBA 05)
    bool hub_port1_pd_active;     // Port 1: Lenker Phone (SC8102 USB-PD 20W Fast Charge)
    bool hub_port2_cp2aa_active;  // Port 2: CP2AA Wireless Dongle
    bool hub_port3_mp3_active;    // Port 3: Handschuhfach MP3 Jukebox & Updates
    bool hub_port4_aux_active;    // Port 4: Cockpit Aux

    // Cockpit 12V Power & Light
    bool bsd_left_active;         // Left Mirror Radar BSD LED active
    bool bsd_right_active;        // Right Mirror Radar BSD LED active
    bool aux_light_on;            // TPS1H100 High-Side Switch (J11 Aux Light)
    bool aux_light_strobe;        // Emergency Strobe active
    bool can_term_active;         // CPC1017N 120-Ohm Termination Relay active
    bool qi_power_active;         // 12V Qi Charger active
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
 * @brief Broadcasts pairing / proximity-rescue beacon to discover or adopt Front Node
 */
esp_err_t esp_now_front_node_start_pairing(void);

/**
 * @brief Sends unbind command to Front Node and clears NVS binding on Central Box
 */
esp_err_t esp_now_front_node_unbind(void);

/**
 * @brief Sends periodic link supervision heartbeat to Front Node
 */
esp_err_t esp_now_front_node_send_heartbeat(void);

/**
 * @brief Checks if Central Box currently has a stored Front Node pairing in NVS
 */
bool esp_now_front_node_is_paired(void);

/**
 * @brief Sends a 1-click reboot command to the Ottocast USB power switch
 */
esp_err_t esp_now_front_node_reboot_ottocast(void);

/**
 * @brief Synchronizes vehicle ignition state (KL15) with the Front Node
 */
esp_err_t esp_now_front_node_set_ignition(bool ignition_on);

/**
 * @brief Sends radar blind-spot detection warning to Front Node mirror LEDs
 */
esp_err_t esp_now_front_node_send_bsd_warning(bool left_active, uint8_t left_level,
                                             bool right_active, uint8_t right_level);

/**
 * @brief Sets Cockpit Aux Light mode on Front Node (0=Off, 1=On, 2=Strobe)
 */
esp_err_t esp_now_front_node_set_aux_light(uint8_t mode);

/**
 * @brief Controls CAN bus 120-Ohm auto-sensing termination relay on Front Node
 */
esp_err_t esp_now_front_node_set_can_term(bool enable);

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


