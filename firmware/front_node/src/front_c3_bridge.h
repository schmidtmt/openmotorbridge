#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"
#include "front_node_config.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge v10.0 - Front-Node C3 Bridge Manager (PCBA 05 S31 U1 -> C3 U10)
// Controls Sub-MCU U10 (ESP32-C3FH4) for Infotainment & Harley WHIM Bypass:
//   - COMM_14: 921600 Baud Control Frame Transmission
//   - COMM_15: Headunit Status & Volume Telemetry Reception
//   - COMM_16: Digital I2S Master Audio Stream to Bike Speakers
//   - COMM_17: Digital I2S Headunit Mic In
// =============================================================================

typedef struct {
    bool     c3_online;
    bool     usb_headunit_connected;
    bool     carplay_unlocked;
    bool     bike_speakers_active;
    uint8_t  headunit_volume_pct;
    uint8_t  display_mux_target; // 0=SkylineOS / Boom!, 1=Aftermarket Display
} FrontC3BridgeStatus_t;

typedef void (*FrontC3StatusCallback)(const FrontC3BridgeStatus_t *status);

/**
 * @brief Initialisiert GPIO-Powersequenz, UART @ 921600 Baud und I2S Master
 */
esp_err_t front_c3_bridge_init(void);

/**
 * @brief Registriert einen Callback für Statusänderungen der Headunit
 */
void front_c3_bridge_set_status_callback(FrontC3StatusCallback cb);

/**
 * @brief Schaltet das Audio-Streaming zu den Bordlautsprechern ein oder aus
 */
esp_err_t front_c3_bridge_set_speakers(bool active);

/**
 * @brief Sendet einen USB-HID Consumer Media Key über U10 an die Headunit
 * @param key_code 1=Play/Pause, 2=Next, 3=Prev, 4=Vol+, 5=Vol-, 6=Mute, 7=Siri/Voice
 */
esp_err_t front_c3_bridge_send_media_key(uint8_t key_code);

/**
 * @brief Steuert den TS3USB221 Hardware-Multiplexer (U8) um
 * @param target 0 = SkylineOS / Boom! Box GTS, 1 = Nachrüst-Display an J4
 */
esp_err_t front_c3_bridge_select_mux(uint8_t target);

/**
 * @brief Schreibt Stereo-Audio PCM Daten in den I2S Master Stream zu U10
 */
esp_err_t front_c3_bridge_stream_audio(const int16_t *pcm_stereo, size_t sample_count);

/**
 * @brief Verarbeitet periodische RX-Pakete von U10 (100 Hz Task Tick)
 */
void front_c3_bridge_update_tick(void);

/**
 * @brief Liefert den aktuellen Status von Chip 2
 */
FrontC3BridgeStatus_t front_c3_bridge_get_status(void);

#ifdef __cplusplus
}
#endif
