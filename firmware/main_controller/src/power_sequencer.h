#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"
#include "main_box_config.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge v10.0 - Gestaffeltes Power-Sequencing & Quad Automotive eFuse
// Hardware:
//   - U12 TI TPS25921 Quad eFuse (J6 Branch 1..4):
//       CH1: VBUS_FRONT (5.0 A Limit) -> T = 0 ms
//       CH2: VBUS_POD1  (2.5 A Limit) -> T = 200 ms
//       CH3: VBUS_POD2  (2.5 A Limit) -> T = 350 ms
//       CH4: VBUS_RADAR (1.5 A Limit) -> T = 500 ms
//   - D3 TI LM66100 Ideal Diode OR-ing (J3 USB-C Benchtop 5V Mode vs. 12V Vehicle)
//   - U4 TI BQ24075 UPS Charger + J5 Pin 3 10k NTC (GPIO 15 JEITA Thermal Guard)
// =============================================================================

typedef enum {
    POWER_STAGE_STANDBY = 0,         // Alles aus / Tier 2 Deep Sleep (nur U2 + U10 SX1262 + U5 BMI270 an USV)
    POWER_STAGE_CORE_BOOT = 1,       // T = 0 ms: Zentralbox (PCBA 01) & Branch 1 Front-Node (VBUS_FRONT 5.0A)
    POWER_STAGE_BAY1 = 2,            // T = 200 ms: Branch 2 Satelliten-Pod 1 (VBUS_POD1 2.5A) EIN
    POWER_STAGE_BAY2 = 3,            // T = 350 ms: Branch 3 Satelliten-Pod 2 (VBUS_POD2 2.5A) EIN
    POWER_STAGE_RADAR = 4,           // T = 500 ms: Branch 4 Heck-Radar 2.0 & V2X (VBUS_RADAR 1.5A) EIN
    POWER_STAGE_FULL_OPERATIONAL = 5,// Gesamtes 4-Draht USB-Fahrzeugnetz aktiv
    POWER_STAGE_BENCHTOP_DFU = 6     // 5V Schreibtisch-Modus über J3 USB-C (LM66100 aktiv, kein 12V Bordnetz)
} PowerSequenceStage_t;

typedef struct {
    PowerSequenceStage_t stage;
    bool kl15_ignition_on;
    bool benchtop_usb_only_mode; // True wenn Versorgung rein über J3 USB-C (D3 LM66100) ohne 12V erfolgt
    bool branch1_front_enabled;  // VBUS_FRONT (5.0A)
    bool branch2_pod1_enabled;   // VBUS_POD1  (2.5A)
    bool branch3_pod2_enabled;   // VBUS_POD2  (2.5A)
    bool branch4_radar_enabled;  // VBUS_RADAR (1.5A)
    float lipo_temp_c;           // Gemessene LiPo-Temperatur über J5 Pin 3 (10k NTC an GPIO 15)
    bool jeita_charge_permitted; // True wenn 0.0 °C <= lipo_temp_c <= 45.0 °C
} PowerSupervisorDiag_t;

/**
 * @brief Initialisiert das v10.0 Quad-eFuse Power-Sequencing Subsystem, LM66100 Erkennung & NTC-Wächter
 */
esp_err_t power_sequencer_init(void);

/**
 * @brief Startet die zeitverzögerte Einschalt-Sequenz bei Zündung EIN (KL15, GPIO 4)
 * T = 0 ms: Core + Front-Node, T = 200 ms: Pod 1, T = 350 ms: Pod 2, T = 500 ms: Radar 2.0 + V2X
 */
void power_sequencer_trigger_boot(void);

/**
 * @brief Startet die saubere gestaffelte Abschalt-Sequenz bei Zündung AUS
 */
void power_sequencer_trigger_shutdown(void);

/**
 * @brief Liefert die aktuelle Power-Stufe zurück
 */
PowerSequenceStage_t power_sequencer_get_stage(void);

/**
 * @brief Prüft, ob alle Stufen vollständig aktiv sind
 */
bool power_sequencer_is_fully_powered(void);

/**
 * @brief Manuelles Schalten einzelner eFuse-Kanäle (für Diagnose, Bus-DFU Kaltstart oder Überlast-Reset)
 */
void power_sequencer_set_front_power(bool enable);
void power_sequencer_set_bay1_power(bool enable);
void power_sequencer_set_bay2_power(bool enable);
void power_sequencer_set_radar_power(bool enable);

/**
 * @brief Aktualisiert den Dual-Power Status (12V Bordnetz vs. 5V J3 USB-C) und prüft den 10k NTC (GPIO 15)
 */
void power_sequencer_update_telemetry(float v_ign_volts, float v_bat_volts, float ntc_temp_c);

/**
 * @brief Liefert die vollständige Diagnose-Struktur des Power-Supervisors
 */
PowerSupervisorDiag_t power_sequencer_get_diagnostics(void);

#ifdef __cplusplus
}
#endif
