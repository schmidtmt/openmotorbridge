#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    RADAR_THREAT_CLEAR = 0,    // 0 = Kein Fahrzeug im Gefahrenbereich (Grün)
    RADAR_THREAT_AMBER = 1,    // 1 = Annäherung normal (< 80m, v_rel > 15 km/h) (Gelb)
    RADAR_THREAT_RED = 2       // 2 = Schnelle Annäherung / Kollisionsgefahr (TTC < 3.5s) (Rot)
} RadarThreatLevel_t;

typedef struct {
    uint8_t id;
    float distance_m;            // Distanz in Metern (0.0 bis 140.0 m)
    float rel_speed_kmh;         // Relativgeschwindigkeit in km/h (+ = nähert sich)
    float time_to_collision_s;   // Berechnete Zeit bis zum Aufprall (TTC)
    RadarThreatLevel_t threat;   // Bedrohungsstufe (CLEAR, AMBER, RED)
    int8_t azimuth_deg;          // Peilung: -15° (Links / Totwinkel) bis +15° (Rechts)
    uint32_t last_seen_ms;       // Timestamp der letzten Reflexion
} RadarTarget_t;

typedef struct {
    bool enabled;
    bool sound_alert_enabled;
    uint8_t target_count;
    RadarTarget_t targets[8];
    RadarThreatLevel_t max_threat;
    float closest_distance_m;
    float highest_rel_speed_kmh;
    bool blind_spot_left;
    bool blind_spot_right;
} RadarState_t;

/**
 * @brief Initialisiert das Radar-Subsystem (UART2 / CAN-Bus Listener)
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

#ifdef __cplusplus
}
#endif
