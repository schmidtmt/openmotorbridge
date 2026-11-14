#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge v10.0 - Central Box Geometric BLE Master (PCBA 01)
// 1. Multi-Vendor Action-Cam BLE Control (GoPro / Insta360 / DJI)
// 2. Automated Dashcam Event-Tagging (ESS Brake < -0.60g / Radar TTC < 2.5s / eCall)
// 3. KL15 Fuel-Stop Filter (10-min recording hold on short ignition off)
// 4. Apple Find My (FMNP) & Google Find My Device (FMDN) Dual-Beaconing
// 5. USB 2.0 Front-Node Peripherals Control (Ottocast Power-Cycle, Aux Light Q2)
// =============================================================================

typedef enum {
    CAM_BRAND_NONE     = 0,
    CAM_BRAND_GOPRO    = 1, // GoPro Hero 9/10/11/12/13 (Service 0xFEA6)
    CAM_BRAND_INSTA360 = 2, // Insta360 X3/X4/Ace Pro (Service 0xBE80)
    CAM_BRAND_DJI      = 3  // DJI Osmo Action 3/4/5 Pro (Service 0xFFF0)
} ActionCamBrand_t;

typedef struct {
    bool connected;
    bool recording;
    ActionCamBrand_t brand;
    uint8_t battery_pct;
    uint16_t remaining_min;
    uint32_t hilight_tags_count;
    bool autoconnect_enabled;
    bool fuel_stop_filter_enabled;
    char camera_name[32];
    uint8_t camera_mac[6];
    bool find_my_beacon_active;
    uint8_t aux_light_mode; // 0=Off, 1=On, 2=Auto-Tunnel/Night via OPT3001
} CentralCamAndBeaconStatus_t;

/**
 * @brief Initialisiert den Action-Cam BLE Master & Find-My Dual-Beaconing auf PCBA 01
 */
esp_err_t action_cam_ble_manager_init(void);

/**
 * @brief Startet oder stoppt die Videoaufnahme der gekoppelten Action-Cam
 */
esp_err_t action_cam_toggle_rec(void);

/**
 * @brief Setzt einen HiLight-Bookmark-Tag im laufenden Video (manuell per Lenker oder automatisch)
 * @param reason_tag Grund des Tags (z. B. "MANUAL_PTT", "ESS_BRAKE", "RADAR_TTC", "ECALL")
 */
esp_err_t action_cam_trigger_hilight_tag(const char *reason_tag);

/**
 * @brief Startet den 10-Sekunden BLE-Scan nach GoPro, Insta360 und DJI Kameras
 */
esp_err_t action_cam_start_scan(void);

/**
 * @brief Koppelt eine gefundene Kamera und speichert sie persistent im NVS ("omb_cam")
 */
esp_err_t action_cam_pair(const uint8_t *mac, uint8_t brand, const char *name);

/**
 * @brief Löscht die gekoppelte Kamera aus dem NVS
 */
esp_err_t action_cam_unpair(void);

/**
 * @brief Konfiguriert Auto-Wake & Auto-Record bei Fahrtbeginn (v > 10 km/h)
 */
void action_cam_set_autoconnect(bool enable);

/**
 * @brief Konfiguriert den Tankstopp-Filter (10 Min Nachlauf bei Zündung AUS)
 */
void action_cam_set_fuel_filter(bool enable);

/**
 * @brief Periodischer Tick für Auto-Record (v > 10 km/h), Tankstopp-Filter und Find-My Beaconing
 */
void action_cam_update_tick(float speed_kmh, bool kl15_active, bool radar_urgent, bool ess_braking);

/**
 * @brief Sendet über den 4-Draht USB-Bus einen 2.5s Kaltstart-Befehl an U4 (TPS2051B) am Front-Node
 */
esp_err_t front_node_usb_reboot_cp2aa_dongle(void);

/**
 * @brief Steuert den High-Side Smart-Switch Q2 (TPS1H100) für Zusatzscheinwerfer am Front-Node via USB
 */
esp_err_t front_node_usb_set_aux_light(uint8_t mode);

/**
 * @brief Aktiviert oder deaktiviert das Apple Find My & Google FMDN Dual-Beaconing im Parkmodus
 */
void find_my_set_dual_beacon(bool enable);

/**
 * @brief Liefert den aktuellen Status zurück
 */
CentralCamAndBeaconStatus_t action_cam_get_status(void);

#ifdef __cplusplus
}
#endif

