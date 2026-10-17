#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

// OMM Packet Types
#define OMM_TYPE_DLE_BEACON    0x01
#define OMM_TYPE_AUDIO_RTP     0x02
#define OMM_TYPE_RADAR         0x03
#define OMM_TYPE_EMERGENCY     0xFF

// OMM Node Feature Bits
typedef enum {
    OMM_FEAT_DUAL_MESH_BRIDGE = (1 << 0), // Sena + Cardo (+60 Pkt)
    OMM_FEAT_LORA_HIGH_POWER  = (1 << 1), // SX1262 +22 dBm PA
    OMM_FEAT_GNSS_1PPS_LOCK   = (1 << 2), // 1-PPS Time Master
    OMM_FEAT_CAN_TELEMETRY    = (1 << 3), // OBD2 / CAN-Bus active
    OMM_FEAT_ENV_MIC_ACTIVE   = (1 << 4), // Front Ambient-Mic (+5 Pkt)
    OMM_FEAT_USV_BAT_BUFFER   = (1 << 5)  // UPS Battery Buffer
} OmmFeatureBitmask_t;

typedef struct __attribute__((packed)) {
    uint8_t  packet_type;       // 0x03 = OMM_TYPE_RADAR
    uint8_t  node_id_short;     // Lower 8-Bit DS2401 ID
    int32_t  latitude_1e7;      // Latitude * 10,000,000
    int32_t  longitude_1e7;     // Longitude * 10,000,000
    int16_t  altitude_m;        // Altitude AMSL (-500 .. +8000 m)
    uint8_t  speed_kmh;         // 0 .. 255 km/h
    uint8_t  heading_div2;      // Heading / 2 (0..179 maps to 0..358 deg)
    int8_t   lean_angle_deg;    // Lean angle (-60..+60 deg)
    uint8_t  status_flags;      // Bit 0: 1-PPS Lock, Bit 1: KL15, Bit 2..7: Batt%
} OmmRadarPacket_t;

typedef struct __attribute__((packed)) {
    uint8_t  packet_type;       // 0xFF = OMM_TYPE_EMERGENCY
    uint8_t  alert_subtype;     // 0x01: Siren Early Warning, 0x02: Crash eCall
    uint64_t sender_uid;        // 64-Bit Chip UID of origin
    int32_t  event_lat_1e7;     // GPS Coordinates
    int32_t  event_lon_1e7;
    uint16_t alert_duration_ms; // Lifetime of alert
    uint8_t  crc8_checksum;     // CRC-8/AUTOSAR
} OmmEmergencyAlert_t;

#define OMM_TYPE_BRIDGE_ACTIVE      0x04
#define OMM_FLAG_DO_NOT_TRANSLATE   0x80

// First-Receiver-Wins (FRW) LoRa Bridging Arbitration Packet (docs/de/04_mesh_lora_navigation.md Sec 3.2)
typedef struct __attribute__((packed)) {
    uint8_t  packet_type;       // 0x04 = OMM_TYPE_BRIDGE_ACTIVE
    uint8_t  source_network;    // 0x01: SENA, 0x02: CARDO, 0x03: OMM_2G4, 0x04: MIDLAND
    uint8_t  target_network;    // Destination network being translated to
    uint8_t  bridging_node_id;  // Short node ID of active translator
    uint16_t sequence_id;       // Monotonic sequence number
    uint8_t  flags;             // Bit 7: FLAG_DO_NOT_TRANSLATE
    uint8_t  crc8_checksum;
} OmmBridgeActivePacket_t;

#define OMM_TYPE_TACTICAL_VOICE     0x05

// Tactical Voice Burst Header over LoRa (Codec2 1200 bps / Opus 6 kbps, Sec 4)
typedef struct __attribute__((packed)) {
    uint8_t  packet_type;       // 0x05 = OMM_TYPE_TACTICAL_VOICE
    uint8_t  node_id_short;     // Sender node ID
    uint8_t  codec_type;        // 0x01: Codec2 (1200 bps), 0x02: Opus (6 kbps)
    uint8_t  burst_seq;         // Monotonic burst sequence (0..255)
    uint16_t payload_len;       // Compressed voice byte length (e.g. 450 bytes)
    uint8_t  flags;             // Bit 0: Mic only (strict LoRa one-way rule)
} OmmTacticalVoiceHeader_t;

/**
 * @brief Initialisiert den OpenMotorMesh Stack
 */
esp_err_t omm_stack_init(void);

/**
 * @brief Berechnet den aktuellen DLE Leader Score
 */
uint8_t omm_calculate_local_dle_score(void);

/**
 * @brief Sendet ein 16-Byte Gruppenradar-Frame
 */
esp_err_t omm_broadcast_radar_frame(const OmmRadarPacket_t *radar_pkt);

/**
 * @brief Löst eine Kolonnen-Sirenen-Frühwarnung aus
 */
esp_err_t omm_trigger_siren_early_warning(double lat, double lon);

#ifdef __cplusplus
}
#endif
