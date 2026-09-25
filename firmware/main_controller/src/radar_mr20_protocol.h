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
    RADAR_PKT_CMD_POST_DIAG     = 0x25, // Central Box -> Sub-MCU (18-Pair POST Hardware Matrix)
    RADAR_PKT_CMD_MANUAL_TEST   = 0x30, // Central Box -> Sub-MCU (Strobe, Halo test, Patterns)
    RADAR_PKT_CMD_CONFIG_MACROS = 0x40, // Central Box -> Sub-MCU (Configurable Macro Pattern Flags)
    RADAR_PKT_CMD_ENTER_BOOTLOAD = 0xF0  // Central Box -> Sub-MCU (Reboot into In-System Flasher)
} RadarPktType_t;

// Configurable Warning Macro Bitmask (Enables/Disables specific patterns via NVS/Config)
typedef enum {
    RADAR_MACRO_POST_SWEEP_EN     = (1 << 0), // Welcome & POST Matrix Sweep on KL15 (Default: ON)
    RADAR_MACRO_ESS_STROBE_EN     = (1 << 1), // Emergency Stop Signal 4.5 Hz Strobe on ax < -0.6g (Default: ON)
    RADAR_MACRO_HAZARD_BEACON_EN  = (1 << 2), // Breakdown / Hazard 1.2 Hz Double Flash at v=0 (Default: ON)
    RADAR_MACRO_THEFT_STROBE_EN   = (1 << 3), // Tamper / Alarm 12 Hz High-Intensity Strobe (Default: ON)
    RADAR_MACRO_CONVOY_MARKER_EN  = (1 << 4), // Follow-Me / Guide Vehicle Wave Pulse (Default: OFF)
    RADAR_MACRO_TAILGATING_EN     = (1 << 5), // Inward Inflow Alert on Extreme Tailgating (Default: OFF)
    RADAR_MACRO_AMBIENT_GLOW_EN   = (1 << 6), // Dusk/Night Standby Taillight (Default: ON)
} RadarMacroConfigBits_t;

// Diagnostic LED State for 18-Pair POST Matrix
typedef enum {
    POST_LED_OFF        = 0x00, // Optional / Component not configured
    POST_LED_GREEN_OK   = 0x01, // Hardware found & operational
    POST_LED_AMBER_INIT = 0x02, // Initializing / Searching / Standby
    POST_LED_RED_FAIL   = 0x03, // Hardware error / Missing / Timeout
    POST_LED_RED_BLINK  = 0x04  // Critical failure (blinking 4 Hz)
} PostLedState_t;

typedef enum {
    RADAR_THREAT_LVL_CLEAR = 0,
    RADAR_THREAT_LVL_AMBER = 1,
    RADAR_THREAT_LVL_RED   = 2
} RadarSubMcuThreat_t;

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
    uint8_t brake_strobe_req;  // 0=Normal, 1=Brake Solid, 2=ESS Emergency 4.5Hz Strobe, 3=Hazard Beacon, 4=Theft Strobe
    bool cruise_mode_active;   // True if Cruise Mode (influences standby glow)
    uint16_t checksum;
} RadarCommandPacket_t;

// Hardware POST Diagnostic Matrix Command received from Central Box (Type 0x25)
typedef struct __attribute__((packed)) {
    uint8_t sync1;             // 0x5A
    uint8_t sync2;             // 0xA5
    uint8_t version;           // 0x02
    uint8_t pkt_type;          // 0x25
    uint8_t duration_tenths_s; // Display duration (e.g. 25 = 2.5 seconds, 0 = indefinite/manual mode)
    uint8_t led_states[36];    // Explicit state for D1..D36 (PostLedState_t)
    uint16_t checksum;
} RadarPostDiagPacket_t;

// Macro Configuration Command received from Central Box (Type 0x40)
typedef struct __attribute__((packed)) {
    uint8_t sync1;             // 0x5A
    uint8_t sync2;             // 0xA5
    uint8_t version;           // 0x02
    uint8_t pkt_type;          // 0x40
    uint16_t enabled_macros;   // Bitmask of RadarMacroConfigBits_t
    uint8_t ess_threshold_pct; // ESS trigger threshold (-0.6g = 60)
    uint8_t spare;
    uint16_t checksum;
} RadarConfigMacrosPacket_t;

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
