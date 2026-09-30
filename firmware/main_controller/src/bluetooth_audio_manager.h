#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge - Qualcomm QCC3084 Bluetooth 5.4 Audio Manager (Central Box)
// =============================================================================
// Manages dedicated hardware Qualcomm QCC3084 Bluetooth 5.4 Audio SoC (U9 on PCBA 01)
// for dual high-definition wireless headset connections (Rider & Passenger),
// Dual-A2DP (aptX HD / aptX Adaptive / Low-Latency < 20 ms), LE Audio Auracast broadcast,
// HFP 1.8 Wideband Speech telephony offload, and direct I2S DMA link to ESP32-S3 DSP.

#define QCC3084_UART_NUM        UART_NUM_1
#define QCC3084_PIN_TX          GPIO_NUM_17
#define QCC3084_PIN_RX          GPIO_NUM_18
#define QCC3084_PIN_EN          GPIO_NUM_16
#define QCC3084_PIN_STATUS      GPIO_NUM_21

typedef enum {
    BT_ROLE_RIDER = 1,   // Primary Rider Helmet (Stream 1 / HFP Telephony)
    BT_ROLE_PAX   = 2    // Passenger / Sozius Helmet (Stream 2 / Synchronous A2DP)
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
    BT_CODEC_APTX,
    BT_CODEC_APTX_HD,
    BT_CODEC_APTX_ADAPTIVE,
    BT_CODEC_APTX_LL,
    BT_CODEC_LC3
} BtAudioCodec_t;

typedef enum {
    HFP_STATE_IDLE = 0,
    HFP_STATE_RINGING,
    HFP_STATE_CALL_ACTIVE,
    HFP_STATE_CALL_HELD
} HfpCallState_t;

typedef struct {
    BtHeadsetRole_t role;
    BtHeadsetState_t state;
    uint8_t mac[6];
    char name[32];
    uint8_t battery_pct;
    int8_t rssi_dbm;
    uint16_t latency_ms;
    BtAudioCodec_t codec;
    uint8_t volume_pct;
    bool is_mic_active;
} BtHeadsetInfo_t;

/**
 * @brief Initialize Qualcomm QCC3084 UART driver, hardware enable pin, and NVS pairings
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
 * @brief Set independent volume level for a headset role (0..100 %) via AVRCP
 */
void bt_audio_set_volume(uint8_t role, uint8_t volume_pct);

/**
 * @brief Configure aptX mode (High-Quality 24-bit/48kHz vs. Ultra Low-Latency < 20 ms)
 */
void bt_audio_set_aptx_mode(uint8_t role, bool low_latency);

/**
 * @brief Enable or disable LE Audio Auracast broadcast to unlimited headsets
 */
void bt_audio_enable_auracast(bool enable, const char *broadcast_name);

/**
 * @brief Query if Auracast broadcast is active
 */
bool bt_audio_is_auracast_active(void);

/**
 * @brief Answer an incoming telephone call via QCC3084 HFP 1.8 engine (ATA)
 */
void bt_audio_hfp_answer(void);

/**
 * @brief Reject or terminate an active telephone call via QCC3084 HFP 1.8 engine (ATH)
 */
void bt_audio_hfp_hangup(void);

/**
 * @brief Query current HFP telephony state
 */
HfpCallState_t bt_audio_hfp_get_state(void);

/**
 * @brief Modal Lenker-PTT event interceptor during phone calls
 * @param click_type 1=Single click, 2=Double click, 3=Long press
 * @return true if event was consumed modally by phone call logic, false if normal PTT
 */
bool bt_audio_handle_ptt_event(uint8_t click_type);

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

/**
 * @brief FreeRTOS background task handling UART telemetry from Qualcomm QCC3084
 */
void task_qcc3084_hub(void *pvParameters);

#ifdef __cplusplus
}
#endif
