#pragma once

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

#define OMM446_BLE_DEV_NAME                "OMM-446-Radio"
#define OMM446_BLE_SERVICE_UUID            0xFE46

// Characteristic UUIDs
#define OMM446_CHAR_UUID_PTT               0x0001 // R/W/N: 0 = Idle/RX, 1 = PTT Transmit
#define OMM446_CHAR_UUID_MODE              0x0002 // R/W/N: 0 = Analog PMR446, 1 = Digital DMR Tier I
#define OMM446_CHAR_UUID_CHANNEL           0x0003 // R/W/N: 1..16 Frequency Channel
#define OMM446_CHAR_UUID_CTCSS             0x0004 // R/W: 0..38 CTCSS Subtone Index
#define OMM446_CHAR_UUID_DMR_COLOR_CODE    0x0005 // R/W: 1..16 DMR Color Code
#define OMM446_CHAR_UUID_SQUELCH           0x0006 // R/W: 1..8 Squelch Level
#define OMM446_CHAR_UUID_POWER_LEVEL       0x0007 // R/W/N: 0 = 0.2W (Helmet), 1 = 0.5W (Bike)
#define OMM446_CHAR_UUID_TELEMETRY         0x0008 // R/N: Battery %, RSSI, Carrier Status

typedef struct __attribute__((packed)) {
    uint8_t  battery_pct;       // 0..100%
    uint8_t  is_charging;       // 1 if charging
    int8_t   rssi_dbm;          // -120 .. -40 dBm
    uint8_t  is_receiving;      // 1 if carrier detected
    uint8_t  is_transmitting;   // 1 if PTT active
    uint8_t  current_channel;   // 1..16
    uint8_t  current_mode;      // 0 = Analog, 1 = DMR
} Omm446BleTelemetry_t;

typedef void (*omm446_ble_cmd_cb_t)(uint16_t char_uuid, const uint8_t *data, size_t len);

esp_err_t omm446_ble_service_init(omm446_ble_cmd_cb_t cmd_cb);
esp_err_t omm446_ble_notify_telemetry(const Omm446BleTelemetry_t *telem);
esp_err_t omm446_ble_notify_channel(uint8_t channel);
esp_err_t omm446_ble_notify_mode(uint8_t mode);
esp_err_t omm446_ble_notify_ptt(uint8_t ptt_state);

#ifdef __cplusplus
}
#endif
