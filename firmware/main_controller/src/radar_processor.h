#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"
#include "radar_mr20_protocol.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge - Rear Radar Subsystem (Garmin Varia & Wheeltec MR20 Radar 2.0)
// =============================================================================

typedef enum {
    RADAR_THREAT_CLEAR = 0,    // 0 = Kein Fahrzeug im Gefahrenbereich (Grün)
    RADAR_THREAT_AMBER = 1,    // 1 = Annäherung normal (< 80m, v_rel > 15 km/h) (Gelb)
    RADAR_THREAT_RED = 2       // 2 = Schnelle Annäherung / Kollisionsgefahr (TTC < 2.5s) (Rot)
} RadarThreatLevel_t;

typedef enum {
    RADAR_HW_TYPE_UNKNOWN   = 0,
    RADAR_HW_TYPE_GARMIN    = 1, // Legacy Garmin Varia RTL515 / eRTL615
    RADAR_HW_TYPE_MR20_V2   = 2  // Radar 2.0 (Wheeltec MR20 77-GHz + ESP32-C3 Sub-MCU)
} RadarHardwareType_t;

typedef struct {
    uint8_t id;
    float distance_m;            // Distanz in Metern (0.0 bis 140.0 m)
    float rel_speed_kmh;         // Relativgeschwindigkeit in km/h (+ = nähert sich)
    float time_to_collision_s;   // Berechnete Zeit bis zum Aufprall (TTC)
    RadarThreatLevel_t threat;   // Bedrohungsstufe (CLEAR, AMBER, RED)
    int8_t azimuth_deg;          // Peilung: -60° (Links / Totwinkel) bis +60° (Rechts)
    uint32_t last_seen_ms;       // Timestamp der letzten Reflexion
} RadarTarget_t;

typedef struct {
    bool enabled;
    bool sound_alert_enabled;
    RadarHardwareType_t hw_type; // Erkanntes Radar-Modell
    uint8_t target_count;
    RadarTarget_t targets[8];
    RadarThreatLevel_t max_threat;
    float closest_distance_m;
    float highest_rel_speed_kmh;
    bool blind_spot_left;
    bool blind_spot_right;
    uint8_t current_dimming_pct; // 18% - 100%
    bool tunnel_mode_active;
} RadarState_t;

/**
 * @brief Initialisiert das Radar-Subsystem (UART2 / Binder M5 Schnittstelle)
 */
esp_err_t radar_processor_init(void);

/**
 * @brief FreeRTOS Task für Radar-Signalverarbeitung & Target-Tracking (Core 0)
 */
void task_radar_processor(void *pvParameters);

/**
 * @brief Liefert den aktuellen Aggregatszustand des Heck-Radars
 */
RadarState_t radar_get_current_state(void);

/**
 * @brief Aktiviert oder deaktiviert den akustischen Helm-Warnping
 */
void radar_set_sound_alert_enabled(bool enabled);

/**
 * @brief Manuelles Triggern eines Test-Pings (für PWA und Audio-Studio)
 */
void radar_trigger_test_alert(RadarThreatLevel_t threat);

/**
 * @brief Injiziert ein simuliertes Radar-Target (Demo- & Testmodus)
 */
void radar_inject_simulated_target(float distance_m, float rel_speed_kmh, int8_t azimuth_deg);

/**
 * @brief Überwacht Längsverzögerung ax für Notbremsblinken (Emergency Stop Signal - ESS)
 */
void radar_notify_vehicle_dynamics(float speed_kmh, float accel_x_g);

/**
 * @brief Gibt zurück, ob das Notbremsblinken (ESS) aktuell aktiv ist
 */
bool radar_is_ess_active(void);

/**
 * @brief Konfiguriert das ESS Notbremsblinken (Aktivierung & Schwellenwert in g)
 */
void radar_set_ess_config(bool enabled, float threshold_g);

/**
 * @brief Löst einen 2.5-Sekunden Test-Bremsblitz aus
 */
void radar_trigger_ess_test(void);

/**
 * @brief Setzt die GNSS-Positions- und Zeitdaten für den astronomischen Dimmer
 */
void radar_update_gnss_context(float lat, float lon, uint32_t utc_epoch, bool fix_valid);

/**
 * @brief Schaltet den Cruise Mode (Audio auf Lautsprecher) um
 */
void radar_set_cruise_mode(bool cruise_mode);

/**
 * @brief Triggert den In-System Bootloader auf der Radar 2.0 Sub-MCU
 */
esp_err_t radar_trigger_submcu_bootloader(void);

/**
 * @brief Default-Bitmaske für Radar 2.0 Warn-Makros (POST sweep, ESS strobe, Hazard beacon, Theft strobe, Ambient glow)
 */
#define RADAR_MACRO_DEFAULT_BITMASK   (RADAR_MACRO_POST_SWEEP_EN | RADAR_MACRO_ESS_STROBE_EN | \
                                       RADAR_MACRO_HAZARD_BEACON_EN | RADAR_MACRO_THEFT_STROBE_EN | \
                                       RADAR_MACRO_AMBIENT_GLOW_EN)

/**
 * @brief Gibt die aktuell konfigurierte Macro-Bitmaske zurück (RadarMacroConfigBits_t)
 */
uint16_t radar_get_macro_config(void);

/**
 * @brief Speichert die Macro-Konfiguration persistent im NVS und sendet sie an die Radar 2.0 Sub-MCU
 */
esp_err_t radar_set_macro_config(uint16_t macro_bitmask);

#ifdef __cplusplus
}
#endif
