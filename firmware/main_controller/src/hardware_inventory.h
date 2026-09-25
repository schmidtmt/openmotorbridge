#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge - Persistent Hardware Inventory & Topology Anomaly Supervisor
// =============================================================================

typedef enum {
    HW_INV_POD1        = (1 << 0),  // Satelliten-Pod 1 (Intercom A / 1-Wire)
    HW_INV_POD2        = (1 << 1),  // Satelliten-Pod 2 (Intercom B / 1-Wire)
    HW_INV_POD3        = (1 << 2),  // Heck-Pod 3 Backbone (GNSS / LoRa / UART1)
    HW_INV_FRONT_NODE  = (1 << 3),  // Front-Node (Cockpit / ESP-NOW)
    HW_INV_RADAR       = (1 << 4),  // Radar 2.0 Sub-MCU / Garmin Varia (UART2)
    HW_INV_ACTION_CAM  = (1 << 5),  // Action-Cam BLE Remote
    HW_INV_OBD2        = (1 << 6),  // OBD2 / CAN BLE Adapter
    HW_INV_TPMS_FRONT  = (1 << 7),  // TPMS Vorderrad BLE
    HW_INV_TPMS_REAR   = (1 << 8),  // TPMS Hinterrad BLE
    HW_INV_KEYFOB      = (1 << 9),  // Smart-Keyfob LoRa Pager
    HW_INV_CAN_BUS     = (1 << 10), // Fahrzeug-CAN Bus
    HW_INV_SD_CARD     = (1 << 11), // MicroSD-Karte gemountet
    HW_INV_DS18B20     = (1 << 12)  // 1-Wire Außentemperaturfühler
} HardwareInventoryBits_t;

typedef enum {
    HW_NODE_OPTIONAL_ABSENT = 0, // In Baseline 0 & Aktuell 0 -> Dunkel (Normalfall für optionale Komponenten)
    HW_NODE_PRESENT_OK      = 1, // In Baseline 1 & Aktuell 1 -> Grün (Normalbetrieb)
    HW_NODE_NEW_DISCOVERED  = 2, // In Baseline 0 & Aktuell 1 -> Grün + Auto-Learn in Baseline
    HW_NODE_LOST_ANOMALY    = 3  // In Baseline 1 & Aktuell 0 -> Rot blinkend + Alarm (Kabelbruch / Verlust!)
} HardwareNodeStatus_t;

typedef struct {
    uint16_t baseline_mask;    // Gespeicherte Hardware-Topologie aus NVS ("omb_sys")
    uint16_t current_mask;     // Aktuell im Boot-Scan gefundene Hardware
    uint16_t newly_found_mask; // Neu hinzugekommene Hardware (Auto-Discovery)
    uint16_t lost_mask;        // Vermisste Hardware (war aktiv, antwortet nicht mehr!)
    uint32_t boot_cycle_count; // Zähler der Zündungszyklen
    bool has_critical_loss;    // True wenn mindestens eine Komponente unerwartet fehlt
} HardwareInventoryState_t;

/**
 * @brief Initialisiert das Hardware-Inventar und lädt die Baseline aus dem NVS Flash
 */
esp_err_t hw_inventory_init(void);

/**
 * @brief Führt den System-Scan aller Busse (1-Wire, UART1, UART2, ESP-NOW, BLE) durch
 *        und generiert das 18-Paar Diagnosepaket für die Radar-LED-Matrix.
 */
void hw_inventory_scan_and_evaluate(void);

/**
 * @brief Gibt den aktuellen Inventar- und Anomalie-Zustand zurück
 */
HardwareInventoryState_t hw_inventory_get_state(void);

/**
 * @brief Bestätigt das absichtliche Entfernen einer Hardware-Komponente (löscht Bit in NVS-Baseline)
 */
esp_err_t hw_inventory_confirm_removal(uint16_t remove_mask);

/**
 * @brief Aktualisiert die Baseline manuell auf den aktuellen Ist-Zustand
 */
esp_err_t hw_inventory_adopt_current_as_baseline(void);

#ifdef __cplusplus
}
#endif
