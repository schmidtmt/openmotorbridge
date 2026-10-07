#pragma once

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

// -----------------------------------------------------------------------------
// BLE Control Flavors supported by Smart Cartridges (PCBA 03)
// -----------------------------------------------------------------------------
typedef enum : uint8_t {
    BLE_FLAVOR_NONE            = 0x00, // No BLE control: purely mechanical/mechatronic (e.g. PMR446 or unsmart unit)
    BLE_FLAVOR_OMM_NATIVE      = 0x01, // OpenMotorMesh proprietary 0x00MB GATT service & LE Audio LC3 bi-directional stereo
    BLE_FLAVOR_SENA_RC_GATT    = 0x02, // Sena RC3 / RC4 Remote Control GATT protocol (Mesh, Group, Vol, Channel)
    BLE_FLAVOR_CARDO_BLE_V2    = 0x03, // Cardo Connect / Packtalk Edge/Pro Remote BLE API (DMC Mute, Vol, Reconnect)
    BLE_FLAVOR_HID_CONSUMER    = 0x04  // Bluetooth Standard HID Consumer Control (0x0C: Play/Pause, Vol +/-)
} BleControlFlavor_t;

typedef struct {
    bool                supported;
    BleControlFlavor_t  flavor;
    char                device_prefix[16]; // e.g. "SPIDER", "SENA", "PT-EDGE", "OMM-UCS"
    uint16_t            service_uuid;      // e.g. 0xFFE0, 0xFE59, 0x00MB
    bool                fallback_to_mechatronics_on_disconnect;
    // Capabilities
    bool                can_power_boot;    // Always false! Cold boot requires physical unpowered mechatronic press
    bool                can_power_off;
    bool                can_mesh_toggle;
    bool                can_group_toggle;
    bool                can_volume;
    bool                can_channel_select;
    bool                can_mic_mute;
    bool                can_telemetry;
    bool                can_le_audio_lc3;
} CartridgeBleConfig_t;

/**
 * @brief Get human-readable name of BLE flavor
 */
static inline const char* get_ble_flavor_name(BleControlFlavor_t flavor) {
    switch (flavor) {
        case BLE_FLAVOR_OMM_NATIVE:   return "OMM_NATIVE (0x00MB / LC3)";
        case BLE_FLAVOR_SENA_RC_GATT: return "SENA_RC_GATT (0xFFE0)";
        case BLE_FLAVOR_CARDO_BLE_V2: return "CARDO_BLE_V2 (0xFE59)";
        case BLE_FLAVOR_HID_CONSUMER: return "HID_CONSUMER (0x0C)";
        case BLE_FLAVOR_NONE:
        default:                      return "NONE (Mechatronics-Only)";
    }
}

#ifdef __cplusplus
}
#endif
