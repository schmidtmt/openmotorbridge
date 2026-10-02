#pragma once

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge - All-UWB Deterministic Vehicle Backbone Protocol Specification
// IEEE 802.15.4z Ultra-Wideband (Qorvo DW3110 / 6.489 GHz Ch. 5, Latency < 0.4 ms)
// =============================================================================

#define UWB_BACKBONE_MAGIC          0x55  // Framing Sync Byte ('U')
#define UWB_BACKBONE_PAN_ID         0x0MB1 // Default PAN ID (OpenMotorBridge Network 1)
#define UWB_BACKBONE_MAX_PAYLOAD    128   // Maximum payload size per UWB frame
#define UWB_BACKBONE_MAX_FRAME_SIZE (sizeof(UwbBackboneHeader) + UWB_BACKBONE_MAX_PAYLOAD + 2) // +2 for CRC16

// -----------------------------------------------------------------------------
// Authorized Node Identifiers across the Vehicle Topology
// -----------------------------------------------------------------------------
typedef enum : uint8_t {
    UWB_NODE_UNKNOWN        = 0x00,
    UWB_NODE_CENTRAL_BOX    = 0x01,  // Coordinator / Master (ESP32-S3, PCBA 01)
    UWB_NODE_FRONT_NODE     = 0x02,  // Cockpit Hub & Sensorik (ESP32-S3, PCBA 05)
    UWB_NODE_CARTRIDGE_BAY1 = 0x03,  // Kassetten-Bucht 1 Links (ESP32-C6, PCBA 03)
    UWB_NODE_CARTRIDGE_BAY2 = 0x04,  // Kassetten-Bucht 2 Rechts (ESP32-C6, PCBA 03)
    UWB_NODE_REAR_RADAR     = 0x05,  // Heck-Radar 2.0 Sub-MCU & Wings (RP2040/C5, PCBA 08)
    UWB_NODE_BROADCAST      = 0xFF   // Broadcast an alle autorisierten Knoten
} UwbNodeType;

// -----------------------------------------------------------------------------
// Backbone Packet Types (gemäß docs/de/09_firmware_architecture.md)
// -----------------------------------------------------------------------------
enum UwbBackbonePktType : uint8_t {
    // --- Node-Management & System-Heartbeat (Universal für alle Nodes) ---
    UWB_PKT_NODE_ANNOUNCE       = 0x01,  // Boot-Handshake: Node-Typ, UID, FW-Version, Features
    UWB_PKT_NODE_HEARTBEAT      = 0x02,  // 1 Hz Heartbeat: Uptime, VBUS-Spannung, Ranging-Distanz, RSSI
    UWB_PKT_PTT_EVENT           = 0x03,  // Lenker-PTT Edge (< 0.4 ms Latenz): Down, Up, Long, Double, Triple

    // --- Konsolidierte Telemetrie (10 Hz Frame) & Peripherie ---
    UWB_PKT_FRONT_TELEMETRY     = 0x04,  // Konsolidierter 10 Hz Frame: GNSS PVT + Wind-RMS + TMP117 + Lux + CAN
    UWB_PKT_WIRELESS_CP_AA_STAT = 0x05,  // COTS CarPlay / Android Auto Bridge Status, Stromaufnahme, Auto-Café Timer
    UWB_PKT_CAN_TELEMETRY       = 0x06,  // Raw CAN Telemetrie Stream (falls Cockpit-CAN J2 aktiv)
    UWB_PKT_BSD_TRIGGER         = 0x07,  // Zentralbox -> Front-Node: Mirror Radar BSD Warning LEDs Gate

    // --- Steuerbefehle & System-Synchronisation ---
    UWB_PKT_CMD_POWER_CYCLE     = 0x10,  // Zentralbox -> Front-Node: 2.5s Kaltstart (Ottocast / USB)
    UWB_PKT_CMD_CONFIG          = 0x11,  // Zentralbox -> Satelliten: Zündungs-Sync & Sleep-State
    UWB_PKT_PAIRING_REQUEST     = 0x12,  // Pairing-Ablauf nach SW1 Tasterdruck (60s Fenster)
    UWB_PKT_PAIRING_CONFIRM     = 0x13,  // AES-128 Session-Key Austausch & NVS Speicherung

    // --- Kassetten-Steuerung & Smart-Cartridge-Protokoll (Bucht 1 & 2) ---
    UWB_PKT_CARTRIDGE_ANNOUNCE  = 0x20,  // Handshake: Hardware-Klasse, Modell-ID, UID, Status, Roaming-ID
    UWB_PKT_CARTRIDGE_OPCODE    = 0x21,  // Zentralbox -> Kassette: Mechatronik-Trigger-Opcode (AO3400A Pulsgatter)
    UWB_PKT_CARTRIDGE_ACK       = 0x22,  // Kassette -> Zentralbox: Ausführungsquittung & Taster-Status

    // --- Digitales UWB Audio-Backbone (Bidirektional, 48 kHz / 16-Bit komprimiert) ---
    UWB_PKT_AUDIO_STREAM_DOWN   = 0x24,  // Zentralbox -> Pods: Master-Mix an Headsets (Mic + Navigation + TTS)
    UWB_PKT_AUDIO_STREAM_UP     = 0x25,  // Pods -> Zentralbox: Intercom Spk-Out / Helm-Audio zur Zentralbox
    UWB_PKT_AUDIO_MEDIA_UP      = 0x26,  // Front-Node -> Zentralbox: Musik / Navigations-Ansagen vom Smartphone

    // --- Radar 2.0 (PCBA 06 / 08): Vorfilterung & LED-Makrosteuerung ---
    UWB_PKT_RADAR_TARGETS       = 0x30,  // 20 Hz voroptimierte Zielliste (TTC, Distanz, Azimut) + URGENT-Flag
    UWB_PKT_RADAR_LED_CMD       = 0x31,  // Zentralbox -> Radar-ESP: Makro-Befehl (Idle, Warnung, Prio-1 Strobe)

    // --- OTA Firmware-Verteilung über UWB ---
    UWB_PKT_FW_UPDATE_PUSH      = 0x50,  // Zentralbox -> Nodes: Blockweises Firmware-Update
    UWB_PKT_FW_UPDATE_DONE      = 0x51   // Nodes -> Zentralbox: Flash-Quittung / Reboot-Ready
};

// -----------------------------------------------------------------------------
// Universal Frame Header for All-UWB Backbone Packets
// -----------------------------------------------------------------------------
typedef struct __attribute__((packed)) {
    uint8_t  magic;           // UWB_BACKBONE_MAGIC (0x55)
    uint8_t  pkt_type;        // UwbBackbonePktType
    uint8_t  source_node;     // UwbNodeType
    uint8_t  target_node;     // UwbNodeType (or 0xFF for Broadcast)
    uint16_t seq_num;         // Monotonically increasing packet sequence number
    uint32_t timestamp_us;    // Precision microsecond timestamp
    uint8_t  payload_len;     // Length of following payload in bytes
} UwbBackboneHeader;

// -----------------------------------------------------------------------------
// 1. Node Management & Heartbeat Payloads
// -----------------------------------------------------------------------------
typedef struct __attribute__((packed)) {
    uint8_t  node_type;       // UwbNodeType
    uint8_t  hw_rev_major;    // z. B. 9 für v9.6
    uint8_t  hw_rev_minor;    // z. B. 6
    uint8_t  fw_version_major;
    uint8_t  fw_version_minor;
    uint8_t  fw_version_patch;
    uint64_t unique_id;       // 64-Bit Chip-UID (eFuse MAC / DS2401)
    uint32_t feature_flags;   // Bitmask of supported hardware capabilities
} UwbNodeAnnouncePkt;

typedef struct __attribute__((packed)) {
    uint32_t uptime_sec;      // Node uptime since boot
    uint16_t vbus_mv;         // Supply voltage in mV
    int16_t  temperature_c_10;// Temperature in 0.1 deg C
    uint16_t ranging_dist_cm; // Last measured Two-Way Ranging distance to coordinator in cm
    int8_t   rssi_dbm;        // Signal strength in dBm
    uint8_t  link_quality;    // 0..100% link quality estimator
} UwbNodeHeartbeatPkt;

// -----------------------------------------------------------------------------
// 2. Handlebar PTT Event (< 0.4 ms deterministic latency)
// -----------------------------------------------------------------------------
typedef enum : uint8_t {
    UWB_PTT_EDGE_DOWN         = 0x00,
    UWB_PTT_EDGE_UP           = 0x01,
    UWB_PTT_CLICK_SHORT       = 0x02,
    UWB_PTT_CLICK_LONG        = 0x03,
    UWB_PTT_CLICK_DOUBLE      = 0x04,
    UWB_PTT_CLICK_TRIPLE      = 0x05
} UwbPttEventType;

typedef enum : uint8_t {
    UWB_BTN_INTERCOM_PTT      = 0x01, // Button 1: Intercom / Mesh Toggle
    UWB_BTN_CAM_HIGHLIGHT     = 0x02, // Button 2: Action-Cam Bookmark / Highlight
    UWB_BTN_MEDIA_VOICE       = 0x03  // Button 3: Media / Voice / Siri
} UwbHandlebarButton;

typedef struct __attribute__((packed)) {
    uint8_t  button_id;       // UwbHandlebarButton (1..3)
    uint8_t  event_type;      // UwbPttEventType
    uint16_t press_duration_ms; // Duration button was held down
    uint8_t  battery_pct;     // Battery status (Front Node supply or keyfob CR2032)
    uint8_t  flags;           // Bit 0: Repeat, Bit 1: Suppressed
} UwbPttEventPkt;

// -----------------------------------------------------------------------------
// 3. Consolidated Front Node Telemetry (10 Hz Frame)
// -----------------------------------------------------------------------------
typedef struct __attribute__((packed)) {
    int32_t  latitude_1e7;    // u-blox SAM-M10Q: Latitude * 1e7 (WGS84)
    int32_t  longitude_1e7;   // u-blox SAM-M10Q: Longitude * 1e7 (WGS84)
    int32_t  altitude_mm;     // Altitude above mean sea level in mm
    uint16_t speed_kph_100;   // Ground speed * 100 (e.g. 5050 = 50.50 km/h)
    uint16_t heading_deg_100; // Heading in 0.01 deg (0..35999)
    uint8_t  satellites_used; // Satellites in PVT solution
    uint8_t  gnss_fix_type;   // 0=No fix, 2=2D, 3=3D, 4=GNSS+Dead Reckoning
    uint8_t  wind_noise_dba;  // Knowles MEMS Acoustic SPL (30..130 dB(A))
    int16_t  ambient_temp_c_100; // TI TMP117 High-Precision Temp * 100 (-4000..+12500)
    uint32_t ambient_lux;     // TI OPT3001 Ambient Light (0..83000 Lux)
    uint16_t status_flags;    // Bit 0: KL15, Bit 1: Cockpit CAN active, Bit 2: USB-PD 1, Bit 3: USB-PD 2
} UwbFrontTelemetryPkt;

// -----------------------------------------------------------------------------
// 4. Smart Cartridge Mechatronic Protocol (PCBA 03 in Bay 1 & Bay 2)
// -----------------------------------------------------------------------------
typedef enum : uint8_t {
    CARTRIDGE_OPCODE_POWER_BOOT    = 0x01, // Kaltstart (Center + Plus 1000 ms)
    CARTRIDGE_OPCODE_POWER_OFF     = 0x02, // Power-Off (Center + Plus 200 ms)
    CARTRIDGE_OPCODE_VOLUME_UP     = 0x03, // Plus (solo 100 ms)
    CARTRIDGE_OPCODE_VOLUME_DOWN   = 0x04, // Minus (solo 100 ms)
    CARTRIDGE_OPCODE_MESH_TOGGLE   = 0x05, // Mesh Button (solo 200 ms)
    CARTRIDGE_OPCODE_OPEN_GROUP_SW = 0x06, // Mesh Button (solo 3000 ms)
    CARTRIDGE_OPCODE_CHANNEL_NEXT  = 0x07, // Makro: 2x Mesh, 1x Plus
    CARTRIDGE_OPCODE_CHANNEL_PREV  = 0x08, // Makro: 2x Mesh, 1x Minus
    CARTRIDGE_OPCODE_CUSTOM_PULSE  = 0x0F  // Parametric Pulse
} UwbCartridgeOpcode;

typedef struct __attribute__((packed)) {
    uint8_t  hardware_class;  // 0x01 = Sena, 0x02 = Cardo, 0x03 = UCS, 0x04 = PMR446
    uint16_t model_id;        // z. B. 0x0101 (Sena SPIDER), 0x0201 (Cardo Edge)
    uint64_t cartridge_uid;   // 64-Bit DS2401 / Chip UID
    uint8_t  roaming_keys_count; // Number of vehicle keys saved (0..4)
    uint16_t vcc_mv;          // Measured supply voltage in mV
    uint8_t  status_flags;    // Bit 0: Headset Docked, Bit 1: Audio Codec OK, Bit 2: MOSFETs Ready
} UwbCartridgeAnnouncePkt;

typedef struct __attribute__((packed)) {
    uint8_t  seq_token;       // Tracking token for matching ACK
    uint8_t  opcode;          // UwbCartridgeOpcode
    uint16_t pulse_duration_ms; // 0 = default from profile, >0 = explicit pulse duration
    uint8_t  actuator_mask;   // Bitmask of AO3400A gates to pulse (Bits 0..3)
} UwbCartridgeOpcodePkt;

typedef struct __attribute__((packed)) {
    uint8_t  seq_token;       // Matched tracking token from opcode
    uint8_t  opcode_executed; // Opcode that was handled
    uint8_t  result_code;     // 0 = Success, 1 = Busy, 2 = Invalid Opcode, 3 = Thermal Limit
    uint8_t  active_actuators;// Physical MOSFET mask actually driven
    uint16_t execution_time_us;// Measured execution duration in microseconds
} UwbCartridgeAckPkt;

// -----------------------------------------------------------------------------
// 5. Radar 2.0 Telemetry & LED Macro Commands (PCBA 08)
// -----------------------------------------------------------------------------
#define UWB_RADAR_MAX_TARGETS 8

typedef struct __attribute__((packed)) {
    uint8_t  target_id;       // Track ID assigned by Wheeltec MR20
    uint16_t distance_cm;     // Distance in cm (0..10000 = 0..100 m)
    int16_t  speed_cm_s;      // Relative radial velocity in cm/s (positive = approaching)
    int16_t  azimuth_deg_10;  // Azimuth angle * 10 (-900..+900 = -90.0° .. +90.0°)
    uint16_t ttc_ms;          // Calculated Time-To-Collision in ms (0xFFFF = no risk)
    uint8_t  threat_level;    // 0 = None, 1 = Warning (Amber), 2 = Imminent Collision (Prio-1 Strobe)
} UwbRadarTargetEntry;

typedef struct __attribute__((packed)) {
    uint8_t  target_count;    // Number of active targets (0..UWB_RADAR_MAX_TARGETS)
    uint8_t  urgent_flag;     // 1 if any target has threat_level == 2 (Imminent Collision)
    uint16_t frame_index;     // Radar cycle counter
    UwbRadarTargetEntry targets[UWB_RADAR_MAX_TARGETS];
} UwbRadarTargetsPkt;

typedef struct __attribute__((packed)) {
    uint8_t  macro_mode;      // 0 = Standby/Off, 1 = Idle Halo, 2 = BSD Warning Amber, 3 = Hazard Prio-1 Strobe
    uint8_t  brightness_pct;  // 0..100%
    uint8_t  left_bsd_state;  // Left mirror warning: 0=Off, 1=Amber Solid, 2=Fast Strobe
    uint8_t  right_bsd_state; // Right mirror warning: 0=Off, 1=Amber Solid, 2=Fast Strobe
} UwbRadarLedCmdPkt;

// -----------------------------------------------------------------------------
// 6. Pairing, Cryptographic Binding & Roaming
// -----------------------------------------------------------------------------
typedef struct __attribute__((packed)) {
    uint64_t pairing_nonce;   // Random 64-bit pairing challenge
    uint32_t vehicle_vin_hash;// 32-bit hash of vehicle identity for roaming slots
    uint16_t timeout_sec;     // Pairing window duration (e.g. 60 seconds)
} UwbPairingRequestPkt;

typedef struct __attribute__((packed)) {
    uint64_t pairing_nonce;   // Echo of pairing nonce
    uint8_t  session_key[16]; // 128-Bit AES-GCM Session Key
    uint8_t  roaming_slot;    // Assigned vehicle slot (0..3)
    uint8_t  status;          // 0 = Success, 1 = Rejected
} UwbPairingConfirmPkt;

// -----------------------------------------------------------------------------
// CRC16-CCITT Verification Function
// -----------------------------------------------------------------------------
static inline uint16_t uwb_calculate_crc16(const uint8_t *data, size_t len) {
    uint16_t crc = 0xFFFF;
    for (size_t i = 0; i < len; i++) {
        crc ^= (uint16_t)data[i] << 8;
        for (int j = 0; j < 8; j++) {
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
