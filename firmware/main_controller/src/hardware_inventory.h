#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge v10.0 - Persistent Hardware Inventory & Topology Supervisor
// Evaluates the USB2517I 7-Port Hub Star Topology + Onboard Peripherals
// =============================================================================

typedef enum {
    HW_INV_POD1         = (1 << 0),  // Satelliten-Pod 1 (USB2517I Port 3 / PCBA 03 / OMM)
    HW_INV_POD2         = (1 << 1),  // Satelliten-Pod 2 (USB2517I Port 4 / PCBA 03 / OMM)
    HW_INV_LORA_SX1262  = (1 << 2),  // Onboard Semtech SX1262 868 MHz LoRa (U10 auf PCBA 01)
    HW_INV_FRONT_NODE   = (1 << 3),  // Front-Node Cockpit (USB2517I Port 2 / PCBA 05 ESP32-S31 + E22)
    HW_INV_RADAR        = (1 << 4),  // Radar 2.0 & 5.9 GHz C-ITS V2X (USB2517I Port 5 / PCBA 08 ESP32-C5)
    HW_INV_ACTION_CAM   = (1 << 5),  // Action-Cam BLE Master (Central Box PCBA 01)
    HW_INV_QCC3086_BT   = (1 << 6),  // Qualcomm QCC3086 BT 5.4 Hub (U9/U13/U14 auf PCBA 01)
    HW_INV_TPMS_FRONT   = (1 << 7),  // TPMS Vorderrad BLE
    HW_INV_TPMS_REAR    = (1 << 8),  // TPMS Hinterrad BLE
    HW_INV_KEYFOB       = (1 << 9),  // Smart-Keyfob LoRa Pager (PCBA 07)
    HW_INV_CAN_BUS      = (1 << 10), // Fahrzeug-CAN-FD Bus (TCAN334G U6)
    HW_INV_SD_CARD      = (1 << 11), // 4-Bit SDIO MicroSD-Karte gemountet (J2)
    HW_INV_SENSOR_PUCK  = (1 << 12)  // Externer Sensor-Puck am Front-Node (SAM-M10Q + TMP117 + OPT3001)
} HardwareInventoryBits_t;

// Legacy bit aliases for backward compatibility
#define HW_INV_POD3     HW_INV_LORA_SX1262
#define HW_INV_QCC3084_BT HW_INV_QCC3086_BT
#define HW_INV_OBD2     HW_INV_QCC3086_BT
#define HW_INV_DS18B20  HW_INV_SENSOR_PUCK

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
 * @brief Führt den v10.0 System-Scan aller USB-Ports (USB2517I), SPI/I2C-ICs und BLE-Peripherie durch
 *        und sendet das POST-Diagnosekommando über den 4-Draht USB-Bus an PCBA 08 (36x WS2812B Matrix).
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
