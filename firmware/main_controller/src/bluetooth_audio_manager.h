#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge - Bluetooth Audio Headset Manager (Central Box)
// =============================================================================
// Manages dual high-definition wireless headset connections for rider & passenger
// (aptX Adaptive / LC3 / Bluetooth 5.3), NVS persistence, and ring buffer DSP feed.

typedef enum {
    BT_ROLE_RIDER = 1,   // Primary Rider Helmet (Port 1 Inlay)
    BT_ROLE_PAX   = 2    // Passenger / Sozius Helmet (Port 2 Inlay)
} BtHeadsetRole_t;

typedef enum {
    BT_STATE_DISCONNECTED = 0,
    BT_STATE_SCANNING,
    BT_STATE_CONNECTING,
    BT_STATE_CONNECTED,
    BT_STATE_STREAMING
} BtHeadsetState_t;

typedef enum {
    BT_CODEC_SBC = 0,
    BT_CODEC_AAC,
    BT_CODEC_APTX_ADAPTIVE,
    BT_CODEC_LC3
} BtAudioCodec_t;

typedef struct {
    BtHeadsetRole_t role;
    BtHeadsetState_t state;
    uint8_t mac[6];
    char name[32];
    uint8_t battery_pct;
    int8_t rssi_dbm;
    uint16_t latency_ms;
    BtAudioCodec_t codec;
    bool is_mic_active;
} BtHeadsetInfo_t;

/**
 * @brief Initialize Bluetooth Audio subsystem, load NVS pairings, setup ringbuffers
 * @return ESP_OK on success
 */
esp_err_t bluetooth_audio_manager_init(void);

/**
 * @brief Start scanning for discoverable Bluetooth headsets
 * @param role 1 = Rider, 2 = Passenger
 * @param duration_s Scan duration in seconds
 */
void bt_audio_start_scan(uint8_t role, uint32_t duration_s);

/**
 * @brief Pair and connect to a specific headset MAC address
 * @param role 1 = Rider, 2 = Passenger
 * @param mac 6-byte target MAC address
 * @return true if connection initiation succeeded
 */
bool bt_audio_pair_device(uint8_t role, const uint8_t *mac);

/**
 * @brief Disconnect active headset connection
 * @param role 1 = Rider, 2 = Passenger
 */
void bt_audio_disconnect(uint8_t role);

/**
 * @brief Check if a headset role is actively connected
 */
bool bt_audio_is_connected(uint8_t role);

/**
 * @brief Retrieve real-time telemetry and status for a headset role
 */
void bt_audio_get_headset_info(uint8_t role, BtHeadsetInfo_t *out_info);

/**
 * @brief Push stereo PCM audio samples to the headset transmit ringbuffer
 * @return Number of samples written
 */
size_t bt_audio_write_stream_samples(uint8_t role, const int16_t *samples, size_t count);

/**
 * @brief Periodic driver maintenance task called from FreeRTOS supervisor
 * @param delta_ms Time elapsed in milliseconds
 */
void bt_audio_update(uint32_t delta_ms);

#ifdef __cplusplus
}
#endif
