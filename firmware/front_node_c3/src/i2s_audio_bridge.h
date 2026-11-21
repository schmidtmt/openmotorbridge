#pragma once

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge v10.0 - Front-Node Digital I2S Audio Bridge (COMM_16 & COMM_17)
// ESP32-C3 U10 in I2S Slave Mode receiving 48 kHz Stereo PCM from S31 U1
// =============================================================================

/**
 * @brief Initialisiert den I2S Slave-Treiber für Empfang von Lautsprecher-Audio und Senden von Headunit-Mic
 */
esp_err_t i2s_audio_bridge_init(void);

/**
 * @brief Liest empfangene Stereo-Samples von S31 und leitet sie an USB UAC weiter
 */
void i2s_audio_bridge_process(void);

/**
 * @brief Aktiviert oder deaktiviert das Streaming zu den Bordlautsprechern
 */
void i2s_audio_bridge_set_speakers_active(bool active);

#ifdef __cplusplus
}
#endif
