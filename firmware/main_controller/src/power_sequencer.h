#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge - Gestaffeltes Power-Sequencing (docs/de/09_firmware_architecture.md)
// Verhindert Einschalt-Stromspitzen beim Booten (Inrush Current Limiting)
// =============================================================================

#define PIN_PORT1_VCC_EN    GPIO_NUM_6   // High-Side Switch Bucht 1 (TPS2051B / 5V DC)
#define PIN_PORT2_VCC_EN    GPIO_NUM_8   // High-Side Switch Bucht 2 (TPS2051B / 5V DC)
#define PIN_RADAR_VCC_EN    GPIO_NUM_7   // High-Side Switch Heck-Radar (12V DC)

typedef enum {
    POWER_STAGE_STANDBY = 0,         // Alles aus / Tier 2 Deep Sleep
    POWER_STAGE_CORE_BOOT = 1,        // T = 0 ms: Zentralbox & Front-Node booten
    POWER_STAGE_BAY1 = 2,             // T = 200 ms: Bucht 1 (+5V DC) EIN
    POWER_STAGE_BAY2 = 3,             // T = 350 ms: Bucht 2 (+5V DC) EIN
    POWER_STAGE_RADAR = 4,            // T = 500 ms: Heck-Radar (+12V DC) EIN
    POWER_STAGE_FULL_OPERATIONAL = 5  // Gesamtes Fahrzeugnetz aktiv
} PowerSequenceStage_t;

/**
 * @brief Initialisiert das gestaffelte Power-Sequencing Subsystem und konfiguriert GPIOs
 */
esp_err_t power_sequencer_init(void);

/**
 * @brief Startet die zeitverzögerte Einschalt-Sequenz bei Zündung EIN (KL15)
 * T = 0 ms: Core, T = 200 ms: Bucht 1, T = 350 ms: Bucht 2, T = 500 ms: Radar
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
 * @brief Manuelles Schalten einzelner Kanäle für Diagnose oder Überlast-Abschaltung
 */
void power_sequencer_set_bay1_power(bool enable);
void power_sequencer_set_bay2_power(bool enable);
void power_sequencer_set_radar_power(bool enable);

#ifdef __cplusplus
}
#endif
