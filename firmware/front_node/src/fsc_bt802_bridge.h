#pragma once

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include "esp_err.h"
#include "front_node_config.h"
#include "usb_backbone_types.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge v10.0 - Front-Node Infotainment Bluetooth Bridge (PCBA 05 U2)
// Controls Feasycom FSC-BT802 (Qualcomm CSR8670) via UART AT-Commands & I2S:
//   - Mode A (BT802_MODE_HEADSET_SINK): Emulates Bluetooth Headset connected
//     to Harley Boom! Box GTS / Skyline OS or BMW TFT to receive navigation
//     audio prompts and phone voice into the OMB DSP pipeline.
//   - Mode B (BT802_MODE_BIKE_SPEAKER_SOURCE): A2DP Audio Source streaming
//     the OMB Master Mix (intercom, music, radio) directly to the bike head unit
//     to play over fairing and saddlebag speakers.
// =============================================================================

typedef struct {
    FscBt802OperatingMode mode;
    bool     bt_online;
    bool     connected_to_headunit;
    bool     a2dp_streaming;
    bool     hfp_call_active;
    int8_t   rssi_dbm;
    uint8_t  volume_pct;
} FscBt802Status_t;

typedef void (*FscBt802StatusCallback)(const FscBt802Status_t *status);

/**
 * @brief Initialize FSC-BT802 hardware enable, reset, AT UART and I2S bus
 */
esp_err_t fsc_bt802_bridge_init(void);

/**
 * @brief Set operating mode: Mode A (Headset Sink) vs. Mode B (Speaker Source)
 * @param mode Target mode
 * @param force Force immediate disconnect and reconfiguration
 */
esp_err_t fsc_bt802_bridge_set_mode(FscBt802OperatingMode mode, bool force);

/**
 * @brief Register status callback for state updates
 */
void fsc_bt802_bridge_set_status_callback(FscBt802StatusCallback cb);

/**
 * @brief Forward AVRCP / Media key to bike head unit
 * @param key_code 1=Play/Pause, 2=Next, 3=Prev, 4=Vol+, 5=Vol-, 6=Mute, 7=Voice
 */
esp_err_t fsc_bt802_bridge_send_media_key(uint8_t key_code);

/**
 * @brief Stream PCM master mix audio to bike speakers via I2S (active in Mode B)
 */
esp_err_t fsc_bt802_bridge_stream_audio_to_speakers(const int16_t *pcm_stereo, size_t sample_count);

/**
 * @brief Read incoming navigation audio PCM from bike head unit via I2S (active in Mode A)
 */
esp_err_t fsc_bt802_bridge_read_nav_audio(int16_t *pcm_out, size_t max_samples, size_t *samples_read);

/**
 * @brief Periodic supervisor tick (call every 10-50 ms)
 */
void fsc_bt802_bridge_update_tick(void);

/**
 * @brief Query current FSC-BT802 status
 */
FscBt802Status_t fsc_bt802_bridge_get_status(void);

#ifdef __cplusplus
}
#endif
