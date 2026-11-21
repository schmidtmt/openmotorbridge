#pragma once

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include "esp_err.h"
#include "front_c3_config.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge v10.0 - USB Headunit Device Controller (PCBA 05 U10)
// Emulates Composite USB Device to Harley Boom! Box GTS / SkylineOS:
//   1. COMM_20: WHIM Wireless Headset Interface Module Emulation
//   2. COMM_19: USB Audio Class 1.0 (UAC) Bike Speaker Output (48 kHz Stereo)
//   3. COMM_21: USB HID Consumer Control (Media Key Injection)
// =============================================================================

/**
 * @brief Initialisiert das USB-Device Subsystem und registriert die Deskriptoren
 */
esp_err_t usb_headunit_device_init(void);

/**
 * @brief Setzt den WHIM Emulations-Status (Headset verbunden/getrennt)
 * @param connected true schaltet Apple CarPlay an der Boom! Box frei
 */
void usb_headunit_set_whim_connected(bool connected);

/**
 * @brief Sendet einen Consumer-Control Tastencode an die Headunit
 */
esp_err_t usb_headunit_send_media_key(MediaKeyCode code);

/**
 * @brief Schreibt PCM Audio-Samples in den UAC Isochronous Streaming-Puffer
 */
esp_err_t usb_headunit_push_speaker_audio(const int16_t *pcm_stereo, size_t sample_count);

/**
 * @brief Gibt an, ob das USB-Kabel mit der Headunit verbunden und enumeriert ist
 */
bool usb_headunit_is_connected(void);

/**
 * @brief Gibt an, ob Apple CarPlay durch den WHIM-Bypass erfolgreich freigeschaltet wurde
 */
bool usb_headunit_is_carplay_unlocked(void);

/**
 * @brief Periodischer Tick für USB-Polling und WHIM-Heartbeat (100 ms)
 */
void usb_headunit_update_tick(void);

#ifdef __cplusplus
}
#endif
