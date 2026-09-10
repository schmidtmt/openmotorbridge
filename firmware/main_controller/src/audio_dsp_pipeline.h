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

enum HelmetEqPreset {
    HELMET_EQ_FLAT = 0,        // Linear / HiFi (Studio-Referenz)
    HELMET_EQ_INTEGRAL = 1,    // Integralhelm: 120 Hz HPF + 2.5 kHz Boost (+3.5 dB)
    HELMET_EQ_OPEN_FACE = 2,   // Klapphelm/Jethelm: 160 Hz HPF + 2.5 kHz Boost (+6.0 dB)
    HELMET_EQ_TOURING = 3      // Touring/Windschild: 90 Hz HPF + 2.5 kHz Boost (+2.0 dB)
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
 * @brief Konfiguriert den adaptiven VOX-Sprachauslöser
 * @param enabled VOX aktiv/inaktiv
 * @param threshold_dbfs Grund-Auslöseschwelle (-45 bis -15 dBFS)
 * @param hangover_ms Nachlaufzeit zur Vermeidung von Wortverschlucken (z. B. 400 ms)
 */
void audio_set_vox_config(bool enabled, float threshold_dbfs, float hangover_ms);

/**
 * @brief Gibt zurück, ob VOX aktuell Sprache erkannt hat
 */
bool audio_get_vox_active(void);

/**
 * @brief Konfiguriert den Sidetone-Pegel (Eigenstimmenrückführung)
 * @param gain_db Lautstärke der Eigenstimme im Helm (-40.0 dB bis 0.0 dB, < -35 dB = Mute)
 */
void audio_set_sidetone_gain(float gain_db);

/**
 * @brief Gibt den aktuellen Sidetone-Gain in dB zurück
 */
float audio_get_sidetone_gain(void);

/**
 * @brief Setzt das Helm-Akustikprofil (Biquad-Filterung)
 */
void audio_set_helmet_eq_preset(HelmetEqPreset preset);

/**
 * @brief Gibt das aktuelle Helm-Akustikprofil zurück
 */
HelmetEqPreset audio_get_helmet_eq_preset(void);

/**
 * @brief Konfiguriert die bidirektionale Intercom-Kreuzschiene (Port 1 <-> Port 2)
 * @param enabled Cross-Bridge aktiv/inaktiv
 * @param cross_bleed_db Überblend-Dämpfung (-18 bis 0 dB)
 */
void audio_set_cross_intercom_bridge(bool enabled, float cross_bleed_db);

/**
 * @brief Gibt den Status der Cross-Intercom-Bridge zurück
 */
bool audio_get_cross_intercom_bridge(void);

/**
 * @brief Führt den aktuellen Knowles MEMS Fahrtwindschallpegel zur VOX-Nachführung zu
 * @param spl_dba Schalldruckpegel in dBA am Frontknoten
 */
void audio_set_front_wind_noise_spl(float spl_dba);

/**
 * @brief FreeRTOS Task für Echtzeit-Audioverarbeitung (Core 1)
 */
void task_audio_dsp(void *pvParameters);

#ifdef __cplusplus
}
#endif
