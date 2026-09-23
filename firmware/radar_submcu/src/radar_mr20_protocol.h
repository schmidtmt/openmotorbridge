#pragma once

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge - Radar 2.0 Sub-MCU Protocol Definitions
// Wheeltec MR20 77-GHz mmWave & Central Box UART Interface (Binder M5)
// =============================================================================

// --- Central Box <-> Radar Sub-MCU Packet Framing ---
#define OMB_RADAR_SYNC_BYTE_1       0x5A
#define OMB_RADAR_SYNC_BYTE_2       0xA5
#define OMB_RADAR_PROTOCOL_VERSION  0x02

typedef enum {
    RADAR_PKT_TELEMETRY_TARGETS = 0x10, // Sub-MCU -> Central Box (20 Hz)
    RADAR_PKT_CMD_VEHICLE_STATE = 0x20, // Central Box -> Sub-MCU (Dynamics, Dimming)
    RADAR_PKT_CMD_MANUAL_TEST   = 0x30, // Central Box -> Sub-MCU (Strobe, Halo test)
    RADAR_PKT_CMD_ENTER_BOOTLOAD = 0xF0  // Central Box -> Sub-MCU (Reboot into In-System Flasher)
} RadarPktType_t;

typedef enum {
    RADAR_THREAT_LVL_CLEAR = 0,
    RADAR_THREAT_LVL_AMBER = 1,
    RADAR_THREAT_LVL_RED   = 2
} RadarThreatLevel_t;

// Compact Target representation transmitted to Central Box
typedef struct __attribute__((packed)) {
    uint8_t id;
    uint16_t distance_cm;      // Distance in centimeters (0 - 15000 cm = 150m)
    int16_t rel_speed_cms;     // Relative speed in cm/s (negative = approaching)
    int16_t azimuth_cdeg;      // Azimuth in centidegrees (-6000 to +6000 = -60.0° to +60.0°)
    uint8_t ttc_tenths_s;      // Time to collision in 0.1s (e.g., 25 = 2.5s; 255 = >25.5s)
    uint8_t threat_level;      // 0=Clear, 1=Amber, 2=Red
} RadarTargetSummary_t;

// Telemetry frame sent to Central Box (Type 0x10)
typedef struct __attribute__((packed)) {
    uint8_t sync1;             // 0x5A
    uint8_t sync2;             // 0xA5
    uint8_t version;           // 0x02
    uint8_t pkt_type;          // 0x10
    uint8_t seq_num;
    uint8_t target_count;      // 0 .. 8
    uint8_t max_threat;        // Highest threat level among targets
    bool blind_spot_left;      // Target in left blind spot (<15m, azimuth < -3°)
    bool blind_spot_right;     // Target in right blind spot (<15m, azimuth > +3°)
    uint16_t closest_dist_cm;  // Closest target distance
    int16_t highest_speed_cms; // Highest closing speed
    RadarTargetSummary_t targets[8];
    uint16_t checksum;         // CRC16-CCITT across header and payload
} RadarTelemetryPacket_t;

// Macro Command received from Central Box (Type 0x20)
typedef struct __attribute__((packed)) {
    uint8_t sync1;             // 0x5A
    uint8_t sync2;             // 0xA5
    uint8_t version;           // 0x02
    uint8_t pkt_type;          // 0x20
    uint16_t vehicle_speed_kmh_x10; // Vehicle speed in 0.1 km/h
    int16_t accel_x_mg;        // Longitudinal acceleration in milli-g (negative = braking)
    uint8_t dimming_pwm_pct;   // Astronomical / Tunnel dimming: 18% - 100%
    uint8_t brake_strobe_req;  // 0=Normal, 1=Brake Solid, 2=ESS Emergency 4.5Hz Strobe
    bool cruise_mode_active;   // True if Cruise Mode (influences standby glow)
    uint16_t checksum;
} RadarCommandPacket_t;

// --- Wheeltec MR20 Raw Radar Frame Parsing ---
// The Wheeltec MR20 77-GHz module outputs binary clusters at 20 Hz (115200 baud default)
#define MR20_RAW_HEADER_1           0xAA
#define MR20_RAW_HEADER_2           0x55
#define MR20_RAW_FRAME_TYPE_TARGETS 0x01

typedef struct __attribute__((packed)) {
    uint8_t id;
    uint16_t range_raw;        // 0.1 m resolution (e.g. 150 = 15.0 m)
    int16_t speed_raw;         // 0.1 m/s resolution (negative = approaching)
    int16_t angle_raw;         // 0.1 deg resolution (-600 to +600 = -60° to +60°)
    uint8_t snr;               // Signal-to-noise ratio / RCS reflection quality
} Mr20RawTarget_t;

// CRC16-CCITT helper (Polynomial 0x1021, Init 0xFFFF)
static inline uint16_t radar_crc16(const uint8_t *data, size_t len) {
    uint16_t crc = 0xFFFF;
    for (size_t i = 0; i < len; i++) {
        crc ^= (uint16_t)data[i] << 8;
        for (uint8_t bit = 0; bit < 8; bit++) {
            if (crc & 0x8000) {
                crc = (crc << 1) ^ 0x1021;
            } else {
                crc <<= 1;
            }
        }
    }
    return crc;
}

#ifdef __cplusplus
}
#endif
