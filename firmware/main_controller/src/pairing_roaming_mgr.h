#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"
#include "uwb_vehicle_backbone.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge - SW1 Hardware Pairing & Multi-Vehicle Roaming Manager
// (docs/de/09_firmware_architecture.md Abs. 1.1 & 2.2)
// =============================================================================

#define PIN_SW1_PAIR_RESET   GPIO_NUM_0  // Hardware-Taster SW1 auf PCBA 01 (Low-aktiv)
#define MAX_ROAMING_VEHICLES 4

typedef enum {
    PAIRING_STATE_IDLE = 0,
    PAIRING_STATE_WINDOW_ACTIVE,
    PAIRING_STATE_SUCCESS,
    PAIRING_STATE_PURGE_COMPLETE
} PairingManagerState_t;

typedef struct {
    uint32_t vin_hash;
    uint8_t  session_key[16];
    uint32_t paired_timestamp;
    bool     valid;
} VehicleRoamingSlot_t;

/**
 * @brief Initialisiert den SW1 Taster-Interrupt und den Roaming NVS-Manager
 */
esp_err_t pairing_roaming_mgr_init(void);

/**
 * @brief Startet manuell das 60-Sekunden UWB-Pairing-Fenster (z. B. via PWA BLE oder SW1 3s)
 */
esp_err_t pairing_mgr_start_pairing_window(uint16_t timeout_sec);

/**
 * @brief Führt einen vollständigen Hard-Purge aller NVS-Keys und Pairings durch (SW1 10s)
 */
esp_err_t pairing_mgr_hard_purge_all_keys(void);

/**
 * @brief Prüft, ob das Pairing-Fenster aktuell aktiv ist
 */
bool pairing_mgr_is_pairing_active(void);

/**
 * @brief Gibt die verbleibende Restzeit des Pairing-Fensters in Sekunden zurück
 */
uint16_t pairing_mgr_get_window_remaining_sec(void);

/**
 * @brief Prüft, ob ein Knoten mit der angegebenen UID autorisiert ist
 */
bool pairing_mgr_is_node_authorized(UwbNodeType node_type, uint64_t uid);

/**
 * @brief Registriert einen neuen autorisierten UWB-Satelliten nach erfolgreichem Handshake
 */
esp_err_t pairing_mgr_store_node_binding(UwbNodeType node_type, uint64_t uid, const uint8_t *session_key);

#ifdef __cplusplus
}
#endif
