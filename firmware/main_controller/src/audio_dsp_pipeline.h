#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

enum AudioOperationMode {
    MODE_STANDARD = 0,     // Beide Intercom-Ports aktiv, gemischt zum Fahrerhelm
    MODE_SINGLE_RIDER = 1, // Port 2 stumm, Fokus auf Helm & Navi
    MODE_CRUISE = 2        // Ausgabe über Bord-Lautsprecher, Intercom gedämpft
};

/**
 * @brief Initialisiert I2S DMA Kanäle und Audio-Frontend
 */
esp_err_t audio_dsp_init(void);

/**
 * @brief Setzt den Betriebsmodus der Audio-Matrix
 */
void audio_set_operation_mode(AudioOperationMode mode);

/**
 * @brief Gibt den aktuellen Betriebsmodus zurück
 */
AudioOperationMode audio_get_operation_mode(void);

/**
 * @brief Setzt die Gain-Werte für Port 1 und Port 2 (aus LittleFS Profil)
 */
void audio_set_port_gains(float port1_gain_db, float port2_gain_db);

/**
 * @brief Meldet dem DSP eine aktive Navi-Durchsage für automatisches Ducking
 */
void audio_set_nav_ducking(bool active);

/**
 * @brief Konfiguriert den geschwindigkeitsabhängigen Transparenzmodus & AGC-Limiter
 * @param enabled Transparenzmodus aktiv/inaktiv
 * @param speed_kmh Aktuelle Fahrzeuggeschwindigkeit via GPS/CAN
 * @param sensitivity_gain_db Eingangsempfindlichkeit (-12.0 bis +6.0 dB)
 */
void audio_set_ambient_transparency(bool enabled, float speed_kmh, float sensitivity_gain_db);

/**
 * @brief Triggert Priorität-1 Ducking (-18 dB) und spielt synthetisierten Radar-Doppelton
 * @param threat_level 1 = Gelb (Annäherung), 2 = Rot (Kritische Annäherung / Notfall)
 */
void audio_trigger_radar_alert(uint8_t threat_level);

/**
 * @brief FreeRTOS Task für Echtzeit-Audioverarbeitung (Core 1)
 */
void task_audio_dsp(void *pvParameters);

#ifdef __cplusplus
}
#endif
