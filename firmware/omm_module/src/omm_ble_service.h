#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

// -----------------------------------------------------------------------------
// OpenMotorMesh (OMM) Proprietary BLE GATT Control & LE Audio LC3 Service
// -----------------------------------------------------------------------------
#define OMM_BLE_DEV_NAME                "OMM-UCS-Intercom"
#define OMM_BLE_SERVICE_UUID            0x00MB // 16-Bit Alias / Base 000000MB-0000-1000-8000-00805F9B34FB

// Characteristic UUIDs
#define OMM_CHAR_UUID_PTT               0x0001 // R/W/N: 0 = Idle, 1 = PTT Active (Mic Open), 2 = VOX Active
#define OMM_CHAR_UUID_MESH_MODE         0x0002 // R/W/N: 0 = Open Convoy, 1 = Private Group
#define OMM_CHAR_UUID_CHANNEL           0x0003 // R/W/N: 1..16 Mesh Frequency Channel
#define OMM_CHAR_UUID_VOLUME            0x0004 // R/W/N: 0..100% Master Playback Gain
#define OMM_CHAR_UUID_TELEMETRY         0x0005 // R/N: Battery %, VBUS sense, Link Quality, RSSI
#define OMM_CHAR_UUID_LE_AUDIO_LC3      0x0006 // R/W/N: Bluetooth 5.3 Bi-directional Stereo LC3 Setup

typedef struct __attribute__((packed)) {
    uint8_t  battery_pct;       // 0..100%
    uint8_t  is_charging;       // 1 if VBUS active and charging
    uint16_t vbus_mv;           // USB-C Voltage in mV
    uint16_t vbat_mv;           // LiPo Voltage in mV
    int8_t   mesh_rssi_dbm;     // Average mesh link RSSI in dBm
    uint8_t  connected_peers;   // Number of active mesh convoy members
} OmmBleTelemetry_t;

typedef struct __attribute__((packed)) {
    uint8_t  le_audio_enabled;  // 1 = Active Bi-directional Stereo LE Audio
    uint16_t sample_rate_hz;    // e.g. 48000 Hz
    uint8_t  frame_duration_ms; // 10 ms (LC3 standard frame)
    uint8_t  octets_per_frame;  // 100 bytes / frame (80 kbps per channel)
    uint8_t  bi_directional;    // 1 = Full-Duplex Stereo Downlink + Stereo/Wideband Uplink
    uint16_t latency_ms;        // Target latency (< 25 ms)
} OmmLeAudioConfig_t;

// Callback for remote commands received via BLE from Smart Cartridge or Handlebar
typedef void (*omm_ble_cmd_cb_t)(uint16_t char_uuid, const uint8_t *data, size_t len);

/**
 * @brief Initialize OMM BLE GATT Server and advertise control interface
 */
esp_err_t omm_ble_service_init(omm_ble_cmd_cb_t cmd_cb);

/**
 * @brief Check if a BLE Central (Bike Central Box or Cartridge) is actively connected
 */
bool omm_ble_is_connected(void);

/**
 * @brief Notify connected central of telemetry update (Battery, VBUS, Peers)
 */
esp_err_t omm_ble_notify_telemetry(const OmmBleTelemetry_t *telemetry);

/**
 * @brief Notify connected central of PTT or Mesh state change
 */
esp_err_t omm_ble_notify_state(uint16_t char_uuid, uint8_t value);

#ifdef __cplusplus
}
#endif
