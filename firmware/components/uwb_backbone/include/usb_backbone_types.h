#pragma once

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge v10.0 - Unified 4-Wire USB 2.0 Automotive Backbone Protocol
// Physical Layer: Microchip USB2517I-JZX 7-Port Hub (PCBA 01) & USB2514Bi (PCBA 05)
// Transport: 4-Wire Shielded Automotive Bus (+5V VBUS, GND, USB_D+, USB_D-)
// Endpoints: USB Audio Class 2.0 (UAC2), USB HID (< 1 ms PTT), USB CDC/Vendor & DFU
// =============================================================================

#define USB_BACKBONE_MAGIC          0x55  // Framing Sync Byte ('U')
#define USB_BACKBONE_MAX_PAYLOAD    128   // Maximum control/telemetry payload per frame
#define USB_DFU_BLOCK_SIZE          96    // Firmware chunk size inside USB_PKT_FW_UPDATE_PUSH

// -----------------------------------------------------------------------------
// USB2517I-JZX 7-Port High-Speed Hub Topology on Central Box (PCBA 01, U8)
// -----------------------------------------------------------------------------
typedef enum : uint8_t {
    USB_HUB_PORT_UPSTREAM_USBC = 0, // J3 External Service & DFU Port (Single-Cable Flash for Entire Vehicle)
    USB_HUB_PORT_1_CENTRAL_MCU = 1, // U2 ESP32-S31-WROOM-1U (Pad 13/14: GPIO 19/20)
    USB_HUB_PORT_2_FRONT_NODE  = 2, // J6 Pin 3/4 -> Branch 1: Front-Node PCBA 05 (via U2 USB2514Bi)
    USB_HUB_PORT_3_POD_BAY1    = 3, // J6 Pin 7/8 -> Branch 2: Satellite Pod 1 PCBA 03 ( + U4 TS5A3159 OMM Mux)
    USB_HUB_PORT_4_POD_BAY2    = 4, // J6 Pin 11/12 -> Branch 3: Satellite Pod 2 PCBA 03 ( + U4 TS5A3159 OMM Mux)
    USB_HUB_PORT_5_REAR_RADAR  = 5, // J6 Pin 15/16 -> Branch 4: Rear Radar & V2X PCBA 08 (ESP32-C5)
    USB_HUB_PORT_6_QCC3084_BT  = 6, // U9 Qualcomm QCC3084 BT 5.4 Audio SoC (Pin 13/14)
    USB_HUB_PORT_7_RESERVE     = 7  // J7 Internal Reserve USB Header
} UsbHubPortId;

// -----------------------------------------------------------------------------
// Authorized Node Identifiers across the v10.0 Vehicle Topology
// -----------------------------------------------------------------------------
typedef enum : uint8_t {
    USB_NODE_UNKNOWN        = 0x00,
    USB_NODE_CENTRAL_BOX    = 0x01,  // Coordinator / Master (ESP32-S31-WROOM-1U, PCBA 01)
    USB_NODE_FRONT_NODE     = 0x02,  // Cockpit Hub & Sensorik (ESP32-S31 + ESP32-E22, PCBA 05)
    USB_NODE_POD_BAY1       = 0x03,  // Monocoque-Pod 1 Links (ESP32-C6-MINI-1, PCBA 03)
    USB_NODE_POD_BAY2       = 0x04,  // Monocoque-Pod 2 Rechts (ESP32-C6-MINI-1, PCBA 03)
    USB_NODE_REAR_RADAR     = 0x05,  // Heck-Radar 2.0 & 5.9 GHz V2X (ESP32-C5-WROOM-1U, PCBA 08)
    USB_NODE_OMM_MODULE_1   = 0x06,  // Unified OMM Tri-Band Module in Pod 1 (ESP32-C6 + PICO-V3-02, PCBA 09/10)
    USB_NODE_OMM_MODULE_2   = 0x07,  // Unified OMM Tri-Band Module in Pod 2 (ESP32-C6 + PICO-V3-02, PCBA 09/10)
    USB_NODE_BROADCAST      = 0xFF   // Broadcast to all connected USB bus nodes
} UsbNodeType;

// Legacy aliases for seamless compatibility across modules
typedef UsbNodeType UwbNodeType;
#define UWB_NODE_UNKNOWN        USB_NODE_UNKNOWN
#define UWB_NODE_CENTRAL_BOX    USB_NODE_CENTRAL_BOX
#define UWB_NODE_FRONT_NODE     USB_NODE_FRONT_NODE
#define UWB_NODE_CARTRIDGE_BAY1 USB_NODE_POD_BAY1
#define UWB_NODE_CARTRIDGE_BAY2 USB_NODE_POD_BAY2
#define UWB_NODE_REAR_RADAR     USB_NODE_REAR_RADAR
#define UWB_NODE_BROADCAST      USB_NODE_BROADCAST

// -----------------------------------------------------------------------------
// Backbone Packet & Endpoint Types (gemäß docs/de/09_firmware_architecture.md)
// -----------------------------------------------------------------------------
enum UsbBackbonePktType : uint8_t {
    // --- Node-Management & System-Heartbeat (Universal für alle USB-Nodes) ---
    USB_DESC_NODE_ANNOUNCE      = 0x01,  // Boot-Handshake: Node-Typ, Chip-UID, FW-Version, Features
    USB_PKT_NODE_HEARTBEAT      = 0x02,  // 1 Hz Heartbeat: Uptime, VBUS-Spannung, USB-Port-ID, Temp
    USB_PKT_GESTURE_EVENT       = 0x03,  // Lenker-PTT / Pod-Taster (< 1 ms USB HID Interrupt Endpoint)

    // --- Konsolidierte Telemetrie (10 Hz Frame) & Cockpit-Peripherie ---
    USB_PKT_FRONT_TELEMETRY     = 0x04,  // Konsolidierter 10 Hz Frame: GNSS PVT + Wind-RMS + TMP117 + Lux
    USB_PKT_WIRELESS_CP_AA_STAT = 0x05,  // CarPlay / Android Auto Bridge Status, Stromaufnahme, Auto-Café Timer
    USB_PKT_CAN_TELEMETRY       = 0x06,  // Raw CAN Telemetrie Stream
    USB_PKT_BSD_TRIGGER         = 0x07,  // Zentralbox -> Front-Node: Mirror Radar BSD Warning LEDs Gate (Q1)
    USB_PKT_COCKPIT_HUD_STATE   = 0x08,  // Zentralbox -> Front-Node: Dual Cockpit Speaker-Corner OLED HUD Update

    // --- Steuerbefehle & System-Synchronisation ---
    USB_CMD_POWER_CYCLE         = 0x10,  // Zentralbox -> Front-Node / Switch: 2.5s Kaltstart (TPS2051B / TPS4H160-Q1)
    USB_CMD_CONFIG              = 0x11,  // Zentralbox -> Satelliten: Zündungs-Sync, Aux-Light (Q2) & Sleep-State
    USB_PKT_PAIRING_REQUEST     = 0x12,  // Pairing-Ablauf nach SW1 Tasterdruck (60s Fenster)
    USB_PKT_PAIRING_CONFIRM     = 0x13,  // AES-128 Session-Key Austausch & NVS Speicherung

    // --- Monocoque-Pod & Smart-Interface-Protokoll (Pod 1 & Pod 2, PCBA 03) ---
    USB_DESC_POD_ANNOUNCE       = 0x20,  // Handshake: Hardware-Klasse (Sena/Cardo/OMM), OMM_DETECT, UID, VCC
    USB_CMD_POD_CONTROL         = 0x21,  // Zentralbox -> Pod: Mechatronik-Trigger-Opcode (AO3400A ACT1..4)
    USB_PKT_POD_ACK             = 0x22,  // Pod -> Zentralbox: Ausführungsquittung & Taster-Status

    // --- Digitales USB Audio Class 2.0 (UAC2) Backbone (48 kHz Bidirektional) ---
    USB_PKT_AUDIO_STREAM_DOWN   = 0x24,  // Zentralbox -> Pods: Master-Mix an Headsets (Voice + Stereo Media)
    USB_PKT_AUDIO_STREAM_UP     = 0x25,  // Pods -> Zentralbox: Intercom Spk-Out / OMM Voice zur Zentralbox
    USB_PKT_AUDIO_MEDIA_UP      = 0x26,  // Front-Node -> Zentralbox: Musik / Navigations-Ansagen (ESP32-S31/E22)

    // --- Radar 2.0 & 5.9 GHz C-ITS V2X (PCBA 08, ESP32-C5-WROOM-1U) ---
    USB_PKT_RADAR_TARGETS       = 0x30,  // 20 Hz voroptimierte Zielliste (TTC, Distanz, Azimut) + URGENT-Flag
    USB_PKT_RADAR_LED_CMD       = 0x31,  // Zentralbox -> Radar-C5: 36x WS2812B Matrix Makro-Befehl
    USB_PKT_V2X_CITS_EVENT      = 0x32,  // Radar-C5 -> Zentralbox: 5.9 GHz 802.11p OCB C-ITS Paket (SPATEM/DENM/CAM)

    // --- Zero-Disassembly Central USB-Bus DFU & OTA Firmware-Verteilung ---
    USB_PKT_FW_UPDATE_PUSH      = 0x50,  // Zentralbox -> USB-Node: Blockweises Firmware-Update / DFU-Steuerung
    USB_PKT_FW_UPDATE_DONE      = 0x51   // USB-Node -> Zentralbox: Flash-Quittung / CRC32-OK / Reboot-Ready
};

typedef UsbBackbonePktType UwbBackbonePktType;
#define UWB_PKT_NODE_ANNOUNCE       USB_DESC_NODE_ANNOUNCE
#define UWB_PKT_NODE_HEARTBEAT      USB_PKT_NODE_HEARTBEAT
#define UWB_PKT_PTT_EVENT           USB_PKT_GESTURE_EVENT
#define UWB_PKT_FRONT_TELEMETRY     USB_PKT_FRONT_TELEMETRY
#define UWB_PKT_WIRELESS_CP_AA_STAT USB_PKT_WIRELESS_CP_AA_STAT
#define UWB_PKT_CAN_TELEMETRY       USB_PKT_CAN_TELEMETRY
#define UWB_PKT_BSD_TRIGGER         USB_PKT_BSD_TRIGGER
#define UWB_PKT_CMD_POWER_CYCLE     USB_CMD_POWER_CYCLE
#define UWB_PKT_CMD_CONFIG          USB_CMD_CONFIG
#define UWB_PKT_PAIRING_REQUEST     USB_PKT_PAIRING_REQUEST
#define UWB_PKT_PAIRING_CONFIRM     USB_PKT_PAIRING_CONFIRM
#define UWB_PKT_CARTRIDGE_ANNOUNCE  USB_DESC_POD_ANNOUNCE
#define UWB_PKT_CARTRIDGE_OPCODE    USB_CMD_POD_CONTROL
#define UWB_PKT_CARTRIDGE_ACK       USB_PKT_POD_ACK
#define UWB_PKT_AUDIO_STREAM_DOWN   USB_PKT_AUDIO_STREAM_DOWN
#define UWB_PKT_AUDIO_STREAM_UP     USB_PKT_AUDIO_STREAM_UP
#define UWB_PKT_AUDIO_MEDIA_UP      USB_PKT_AUDIO_MEDIA_UP
#define UWB_PKT_RADAR_TARGETS       USB_PKT_RADAR_TARGETS
#define UWB_PKT_RADAR_LED_CMD       USB_PKT_RADAR_LED_CMD
#define UWB_PKT_FW_UPDATE_PUSH      USB_PKT_FW_UPDATE_PUSH
#define UWB_PKT_FW_UPDATE_DONE      USB_PKT_FW_UPDATE_DONE

// -----------------------------------------------------------------------------
// Universal Frame Header for 4-Wire USB 2.0 Backbone Packets
// -----------------------------------------------------------------------------
typedef struct __attribute__((packed)) {
    uint8_t  magic;           // USB_BACKBONE_MAGIC (0x55)
    uint8_t  pkt_type;        // UsbBackbonePktType
    uint8_t  source_node;     // UsbNodeType
    uint8_t  target_node;     // UsbNodeType (or 0xFF for Broadcast)
    uint16_t seq_num;         // Monotonically increasing packet sequence number
    uint32_t timestamp_us;    // Precision microsecond timestamp (USB SOF synchronized)
    uint8_t  payload_len;     // Length of following payload in bytes
} UsbBackboneHeader;

typedef UsbBackboneHeader UwbBackboneHeader;

#define USB_BACKBONE_MAX_FRAME_SIZE (sizeof(UsbBackboneHeader) + USB_BACKBONE_MAX_PAYLOAD + 2)
#define UWB_BACKBONE_MAGIC          USB_BACKBONE_MAGIC
#define UWB_BACKBONE_MAX_PAYLOAD    USB_BACKBONE_MAX_PAYLOAD
#define UWB_BACKBONE_MAX_FRAME_SIZE USB_BACKBONE_MAX_FRAME_SIZE

// -----------------------------------------------------------------------------
// 1. Node Management & Heartbeat Payloads
// -----------------------------------------------------------------------------
typedef struct __attribute__((packed)) {
    uint8_t  node_type;       // UsbNodeType
    uint8_t  hw_rev_major;    // 10 für v10.0
    uint8_t  hw_rev_minor;    // 0
    uint8_t  fw_version_major;
    uint8_t  fw_version_minor;
    uint8_t  fw_version_patch;
    uint64_t unique_id;       // 64-Bit Chip-UID (eFuse MAC)
    uint32_t feature_flags;   // Bitmask of supported hardware capabilities
} UsbNodeAnnouncePkt;

typedef UsbNodeAnnouncePkt UwbNodeAnnouncePkt;

typedef struct __attribute__((packed)) {
    uint32_t uptime_sec;      // Node uptime since boot
    uint16_t vbus_mv;         // Measured USB VBUS supply voltage in mV
    int16_t  temperature_c_10;// Die / board temperature in 0.1 deg C
    uint16_t usb_port_id;     // Assigned USB2517I / USB2514Bi port index (or legacy distance_cm)
    int8_t   rssi_dbm;        // Secondary radio RSSI or 0 for wired USB
    uint8_t  link_quality;    // 100% for High-Speed / Full-Speed USB lock
} UsbNodeHeartbeatPkt;

typedef UsbNodeHeartbeatPkt UwbNodeHeartbeatPkt;

// -----------------------------------------------------------------------------
// 2. Handlebar & Pod PTT / Gesture Event (< 1 ms USB HID Interrupt Latency)
// -----------------------------------------------------------------------------
typedef enum : uint8_t {
    USB_PTT_EDGE_DOWN         = 0x00,
    USB_PTT_EDGE_UP           = 0x01,
    USB_PTT_CLICK_SHORT       = 0x02,
    USB_PTT_CLICK_LONG        = 0x03,
    USB_PTT_CLICK_DOUBLE      = 0x04,
    USB_PTT_CLICK_TRIPLE      = 0x05
} UsbPttEventType;

typedef UsbPttEventType UwbPttEventType;
#define UWB_PTT_EDGE_DOWN   USB_PTT_EDGE_DOWN
#define UWB_PTT_EDGE_UP     USB_PTT_EDGE_UP
#define UWB_PTT_CLICK_SHORT USB_PTT_CLICK_SHORT
#define UWB_PTT_CLICK_LONG  USB_PTT_CLICK_LONG
#define UWB_PTT_CLICK_DOUBLE USB_PTT_CLICK_DOUBLE
#define UWB_PTT_CLICK_TRIPLE USB_PTT_CLICK_TRIPLE

typedef enum : uint8_t {
    USB_BTN_INTERCOM_PTT      = 0x01, // Button 1 (J_POD_L / Pad 8): Intercom / Mesh Toggle / HFP Call
    USB_BTN_CAM_HIGHLIGHT     = 0x02, // Button 2 (J_POD_R / Pad 9): Action-Cam Bookmark / Highlight
    USB_BTN_MEDIA_VOICE       = 0x03  // Button 3: Media / Voice / Siri / Display Mode
} UsbHandlebarButton;

typedef UsbHandlebarButton UwbHandlebarButton;
#define UWB_BTN_INTERCOM_PTT  USB_BTN_INTERCOM_PTT
#define UWB_BTN_CAM_HIGHLIGHT USB_BTN_CAM_HIGHLIGHT
#define UWB_BTN_MEDIA_VOICE   USB_BTN_MEDIA_VOICE

typedef struct __attribute__((packed)) {
    uint8_t  button_id;       // UsbHandlebarButton (1..3)
    uint8_t  event_type;      // UsbPttEventType
    uint16_t press_duration_ms; // Duration button was held down
    uint8_t  battery_pct;     // 100% (Wired via Front-Node J_POD_L/R) or Keyfob battery
    uint8_t  flags;           // Bit 0: Repeat, Bit 1: HFP Intercepted
} UsbPttEventPkt;

typedef UsbPttEventPkt UwbPttEventPkt;

// -----------------------------------------------------------------------------
// 3. Consolidated Front Node Telemetry (10 Hz Frame from PCBA 05 + Sensor Puck)
// -----------------------------------------------------------------------------
#define FRONT_STAT_KL15_ACTIVE       (1 << 0)
#define FRONT_STAT_SENSOR_PUCK_OK    (1 << 1) // J_SENSOR_EXT (SAM-M10Q + TMP117 + OPT3001)
#define FRONT_STAT_SW3526_PD_ACTIVE  (1 << 2) // U3 SW3526 30W USB-PD Active
#define FRONT_STAT_CP2AA_PWR_ACTIVE  (1 << 3) // U4 TPS2051B J_DONGLE Power Active
#define FRONT_STAT_CP2AA_FAULT       (1 << 4) // U4 TPS2051B Overcurrent Fault (Pad 38)
#define FRONT_STAT_E22_WIFI6E_OK     (1 << 5) // U9 ESP32-E22 SDIO 3.0 Wi-Fi 6E Bridge OK
#define FRONT_STAT_DUAL_OLED_OK      (1 << 6) // J_DISP_L & J_DISP_R Cockpit Displays OK
#define FRONT_STAT_AUX_LIGHT_ON      (1 << 7) // Q2 TPS1H100 Aux Light Active

typedef struct __attribute__((packed)) {
    int32_t  latitude_1e7;    // u-blox SAM-M10Q: Latitude * 1e7 (WGS84)
    int32_t  longitude_1e7;   // u-blox SAM-M10Q: Longitude * 1e7 (WGS84)
    int32_t  altitude_mm;     // Altitude above mean sea level in mm
    uint16_t speed_kph_100;   // Ground speed * 100 (e.g. 5050 = 50.50 km/h)
    uint16_t heading_deg_100; // Heading in 0.01 deg (0..35999)
    uint8_t  satellites_used; // Satellites in PVT solution
    uint8_t  gnss_fix_type;   // 0=No fix, 2=2D, 3=3D, 4=GNSS+Dead Reckoning
    uint8_t  wind_noise_dba;  // Knowles SPH0645LM4H MEMS Acoustic SPL (30..130 dB(A))
    int16_t  ambient_temp_c_100; // TI TMP117 High-Precision Temp * 100 (-4000..+12500)
    uint32_t ambient_lux;     // TI OPT3001 Ambient Light (0..83000 Lux)
    uint32_t baro_pressure_pa; // Bosch BMP390 Barometric Pressure in Pa (30000..125000 Pa)
    uint16_t status_flags;    // FRONT_STAT_* bitmask
} UsbFrontTelemetryPkt;

typedef UsbFrontTelemetryPkt UwbFrontTelemetryPkt;

// -----------------------------------------------------------------------------
// 3b. Dual Cockpit Speaker-Corner OLED HUD Update (J_DISP_L & J_DISP_R on PCBA 05)
// -----------------------------------------------------------------------------
typedef struct __attribute__((packed)) {
    uint8_t  left_threat_level;   // 0=Clear, 1=BSD Amber, 2=Collision Red
    uint8_t  right_threat_level;  // 0=Clear, 1=BSD Amber, 2=Collision Red
    uint16_t closest_rear_dist_m; // Closest radar target distance in 0.1m
    uint8_t  glosa_active;        // 1 if 5.9 GHz V2X Traffic Light SPATEM active
    uint8_t  glosa_phase;         // 0=Unknown, 1=Green, 2=Yellow, 3=Red
    uint8_t  glosa_rec_speed_kph; // Recommended Green-Wave speed in km/h
    uint8_t  glosa_countdown_s;   // Seconds until traffic light phase change
    uint8_t  v2x_hazard_type;     // 0=None, 1=Emergency Vehicle, 2=Accident/Breakdown, 3=Roadworks
    uint8_t  intercom_mode;       // 0=Standby, 1=Micro-Cluster, 2=Macro-Group, 3=Rescue-LoRa, 4=Phone-Call
    uint8_t  brightness_pct;      // Auto-dimmed via OPT3001 Lux & Solar Elevation (5..100%)
    char     status_line[20];     // Short text for right OLED (e.g. "CH8 DMR | 4 Bikes")
} UsbCockpitHudStatePkt;

// -----------------------------------------------------------------------------
// 4. Monocoque-Pod Interface & OMM Auto-Sense Protocol (PCBA 03 in Pod 1 & Pod 2)
// -----------------------------------------------------------------------------
typedef enum : uint8_t {
    POD_OPCODE_POWER_BOOT    = 0x01, // Kaltstart (Center + Plus 1000 ms)
    POD_OPCODE_POWER_OFF     = 0x02, // Power-Off (Center + Plus 200 ms)
    POD_OPCODE_VOLUME_UP     = 0x03, // Plus (solo 100 ms)
    POD_OPCODE_VOLUME_DOWN   = 0x04, // Minus (solo 100 ms)
    POD_OPCODE_MESH_TOGGLE   = 0x05, // Mesh Button (solo 200 ms)
    POD_OPCODE_OPEN_GROUP_SW = 0x06, // Mesh Button (solo 3000 ms)
    POD_OPCODE_CHANNEL_NEXT  = 0x07, // Makro: 2x Mesh, 1x Plus
    POD_OPCODE_CHANNEL_PREV  = 0x08, // Makro: 2x Mesh, 1x Minus
    POD_OPCODE_OMM_PTT_DOWN  = 0x09, // Digital PTT Down for OMM Tri-Band Module
    POD_OPCODE_OMM_PTT_UP    = 0x0A, // Digital PTT Up for OMM Tri-Band Module
    POD_OPCODE_CUSTOM_PULSE  = 0x0F  // Parametric Pulse
} UsbPodControlOpcode;

typedef UsbPodControlOpcode UwbCartridgeOpcode;
#define CARTRIDGE_OPCODE_POWER_BOOT    POD_OPCODE_POWER_BOOT
#define CARTRIDGE_OPCODE_POWER_OFF     POD_OPCODE_POWER_OFF
#define CARTRIDGE_OPCODE_VOLUME_UP     POD_OPCODE_VOLUME_UP
#define CARTRIDGE_OPCODE_VOLUME_DOWN   POD_OPCODE_VOLUME_DOWN
#define CARTRIDGE_OPCODE_MESH_TOGGLE   POD_OPCODE_MESH_TOGGLE
#define CARTRIDGE_OPCODE_OPEN_GROUP_SW POD_OPCODE_OPEN_GROUP_SW
#define CARTRIDGE_OPCODE_CHANNEL_NEXT  POD_OPCODE_CHANNEL_NEXT
#define CARTRIDGE_OPCODE_CHANNEL_PREV  POD_OPCODE_CHANNEL_PREV
#define CARTRIDGE_OPCODE_CUSTOM_PULSE  POD_OPCODE_CUSTOM_PULSE

// Status flags in UsbPodAnnouncePkt.status_flags
#define POD_STAT_DEVICE_DOCKED      (1 << 0)
#define POD_STAT_ES8388_CODEC_OK    (1 << 1)
#define POD_STAT_ACTUATORS_READY    (1 << 2)
#define POD_STAT_OMM_DIGITAL_MODE   (1 << 3) // Pad 16 OMM_DETECT == HIGH (U4 TS5A3159 switched to USB passthrough)

typedef struct __attribute__((packed)) {
    uint8_t  hardware_class;  // 0x01 = Sena (3M Dual Lock), 0x02 = Cardo (OEM-Clip), 0x03 = UCS (Adapter Plate), 0x05 = Unified OMM Tri-Band (PCBA 09/10)
    uint16_t model_id;        // e.g. 0x0101 (Sena), 0x0201 (Cardo Edge), 0x0501 (OMM Tri-Band 2.4G+PMR446+BT)
    uint64_t cartridge_uid;   // 64-Bit eFuse Chip UID
    uint8_t  roaming_keys_count; // Number of vehicle keys saved (0..4)
    uint16_t vcc_mv;          // Measured VBUS supply voltage in mV
    uint8_t  status_flags;    // POD_STAT_* bitmask (including OMM_DETECT state)
} UsbPodAnnouncePkt;

typedef UsbPodAnnouncePkt UwbCartridgeAnnouncePkt;

typedef struct __attribute__((packed)) {
    uint8_t  seq_token;       // Tracking token for matching ACK
    uint8_t  opcode;          // UsbPodControlOpcode
    uint16_t pulse_duration_ms; // 0 = default from profile, >0 = explicit pulse duration
    uint8_t  actuator_mask;   // Bitmask of AO3400A gates to pulse (ACT1=Pad18, ACT2=Pad19, ACT3=Pad8, ACT4=Pad9)
} UsbPodControlPkt;

typedef UsbPodControlPkt UsbPodOpcodePkt;
typedef UsbPodControlPkt UwbCartridgeOpcodePkt;

typedef struct __attribute__((packed)) {
    uint8_t  seq_token;       // Matched tracking token from opcode
    uint8_t  opcode_executed; // Opcode that was handled
    uint8_t  result_code;     // 0 = Success, 1 = Busy, 2 = Invalid Opcode, 3 = Thermal Limit
    uint8_t  active_actuators;// Physical MOSFET mask actually driven
    uint16_t execution_time_us;// Measured execution duration in microseconds
} UsbPodAckPkt;

typedef UsbPodAckPkt UwbCartridgeAckPkt;

// -----------------------------------------------------------------------------
// 4b. Digital USB Audio Multi-Stream Downlink & Uplink (Opus / Codec2 / DMR)
// -----------------------------------------------------------------------------
// Audio Codec Types for Digital USB Backbone & RF Links
typedef enum : uint8_t {
    AUDIO_CODEC_OPUS_24K       = 0x01, // Opus Wideband 24 kHz (2.4 GHz Mesh Voice & Music Sharing)
    AUDIO_CODEC_CODEC2_1200    = 0x02, // Codec2 1200 bps (LoRa Tactical Fallback)
    AUDIO_CODEC_AMBE2_DMR      = 0x03, // DMR AMBE+2 Vocoder (446 MHz Digital DMR)
    AUDIO_CODEC_OPUS_VOICE_8K  = 0x04, // Opus SILK/Voice Low-Bitrate 6-8 kbps (PMR446 Analog capture)
    AUDIO_CODEC_PCM_LEGACY     = 0xFF  // Legacy uncompressed PCM (Analog OEM Headset ES8388 ADC)
} AudioCodecType;

#define USB_AUDIO_DOWN_VOICE_SAMPLES  24   // 24x int16_t mono = 48 Bytes (Legacy PCM)
#define USB_AUDIO_DOWN_MUSIC_SAMPLES  18   // 18x stereo pairs = 72 Bytes (Legacy PCM)

#define USB_AUDIO_FLAG_DUCKING_ACTIVE   (1 << 0) // Central Box DSP ducking active (-18 dB on music)
#define USB_AUDIO_FLAG_VOICE_ACTIVE     (1 << 1) // Voice Activity Detected (VAD) on rider mic
#define USB_AUDIO_FLAG_RADAR_ALERT      (1 << 2) // Priority-1 Radar audible warning active
#define USB_AUDIO_FLAG_HFP_CALL_MUTE    (1 << 3) // Smartphone HFP Call active -> Mute group intercom mic!
#define USB_AUDIO_FLAG_PTT_ACTIVE       (1 << 4) // Driver Handlebar PTT active -> route driver voice to Funk
#define USB_AUDIO_FLAG_TARGET_FUNK      (1 << 5) // Active transmit request for 446 MHz PMR/DMR
#define USB_AUDIO_FLAG_PILLION_WHISPER  (1 << 6) // Pillion Private Cabin Whisper active -> Muted towards Mesh!

#define UWB_AUDIO_DOWN_VOICE_SAMPLES  USB_AUDIO_DOWN_VOICE_SAMPLES
#define UWB_AUDIO_DOWN_MUSIC_SAMPLES  USB_AUDIO_DOWN_MUSIC_SAMPLES
#define UWB_AUDIO_FLAG_DUCKING_ACTIVE USB_AUDIO_FLAG_DUCKING_ACTIVE
#define UWB_AUDIO_FLAG_VOICE_ACTIVE   USB_AUDIO_FLAG_VOICE_ACTIVE
#define UWB_AUDIO_FLAG_RADAR_ALERT    USB_AUDIO_FLAG_RADAR_ALERT

typedef struct __attribute__((packed)) {
    uint16_t frame_seq;       // Monotonically increasing audio frame sequence counter
    uint8_t  flags;           // USB_AUDIO_FLAG_*
    uint8_t  codec_type;      // AudioCodecType (default: AUDIO_CODEC_OPUS_24K)
    uint8_t  voice_gain_db;   // Master voice preamp gain set by Central Box DSP
    uint8_t  music_gain_db;   // Master music gain (with ducking already factored in)
    union {
        struct {
            int16_t  sub_voice[USB_AUDIO_DOWN_VOICE_SAMPLES]; // 48 Bytes legacy PCM
            int16_t  sub_music_l[USB_AUDIO_DOWN_MUSIC_SAMPLES]; // 36 Bytes legacy PCM
            int16_t  sub_music_r[USB_AUDIO_DOWN_MUSIC_SAMPLES]; // 36 Bytes legacy PCM
        };
        struct {
            uint8_t  driver_voice_bytes;  // Compressed driver voice frame (Opus 24k: ~24..48 B)
            uint8_t  pillion_voice_bytes; // Compressed pillion voice frame (Opus 24k: ~24..48 B, 0 = muted / whisper)
            uint8_t  music_down_bytes;    // Compressed stereo media/nav frame (Opus Stereo: ~48..80 B)
            union {
                struct {
                    uint8_t voice_mic_bytes; // Alias for backward compatibility
                };
                uint8_t compressed_payload[116]; // Packed [driver_bytes][pillion_bytes][music_bytes]
            };
        } compressed;
    };
} UsbAudioStreamDownPkt;

typedef UsbAudioStreamDownPkt UwbAudioStreamDownPkt;

// Upstream Audio Status Flags
#define USB_AUDIO_UP_FLAG_STREAM_ACTIVE   (1 << 0) // Audio stream active
#define USB_AUDIO_UP_FLAG_PTT_PRESSED     (1 << 1) // Physical PTT pressed on Pod/Headset
#define USB_AUDIO_UP_FLAG_OMM_DIGITAL     (1 << 2) // OMM digital mode active
#define USB_AUDIO_UP_FLAG_FUNK_CARRIER    (1 << 3) // 446 MHz PMR/DMR Carrier / Squelch open
#define USB_AUDIO_UP_FLAG_MESH_VOICE      (1 << 4) // 2.4 GHz Mesh Voice packet active
#define USB_AUDIO_UP_FLAG_MESH_MUSIC      (1 << 5) // 2.4 GHz Mesh Stereo Music packet active

#define USB_AUDIO_UP_SAMPLES 48
#define UWB_AUDIO_UP_SAMPLES USB_AUDIO_UP_SAMPLES

#define USB_OMM_UP_VOICE_SAMPLES 16 // 16x int16_t mono = 32 Bytes
#define USB_OMM_UP_MUSIC_SAMPLES 18 // 18x stereo pairs = 72 Bytes

typedef struct __attribute__((packed)) {
    uint16_t frame_seq;
    uint8_t  status_flags;    // USB_AUDIO_UP_FLAG_*
    uint8_t  sample_count;    // Actual samples for single mono (legacy / OEM analog: up to USB_AUDIO_UP_SAMPLES)
    uint8_t  codec_type;      // AudioCodecType (AUDIO_CODEC_OPUS_24K, AUDIO_CODEC_AMBE2_DMR, etc.)
    union {
        int16_t  samples[USB_AUDIO_UP_SAMPLES]; // Legacy mono stream (e.g. from ES8388 ADC)
        struct {
            uint8_t rssi_dbm;            // Signal strength in -dBm
            uint8_t voice_funk_count;    // Number of 446 MHz PMR/DMR samples or compressed bytes
            uint8_t voice_mesh_count;    // Number of 2.4 GHz Mesh Voice samples or compressed bytes
            uint8_t music_mesh_pairs;    // Number of 2.4 GHz Mesh Stereo Music pairs or compressed bytes
            union {
                struct {
                    int16_t sub_voice_funk[USB_OMM_UP_VOICE_SAMPLES]; // 32 Bytes: Mono Voice from PMR/DMR
                    int16_t sub_voice_mesh[USB_OMM_UP_VOICE_SAMPLES]; // 32 Bytes: Mono Voice from 2.4 GHz Mesh
                    int16_t sub_music_l[USB_OMM_UP_MUSIC_SAMPLES];    // 36 Bytes: Stereo Music Left from Mesh
                    int16_t sub_music_r[USB_OMM_UP_MUSIC_SAMPLES];    // 36 Bytes: Stereo Music Right from Mesh
                };
                uint8_t compressed_payload[100]; // Packed Opus & Vocoder bytes: [funk][mesh][music]
            };
        } multistream;
    };
} UsbAudioStreamUpPkt;

typedef UsbAudioStreamUpPkt UwbAudioStreamUpPkt;

#define USB_AUDIO_MEDIA_SAMPLES 28
#define UWB_AUDIO_MEDIA_SAMPLES USB_AUDIO_MEDIA_SAMPLES
typedef struct __attribute__((packed)) {
    uint16_t frame_seq;
    uint8_t  source_id;       // 0x01 = ESP32-E22 Wi-Fi 6E CarPlay/AA, 0x02 = USB Dongle
    uint8_t  sample_pairs;    // Number of L/R pairs
    int16_t  media_l[USB_AUDIO_MEDIA_SAMPLES];
    int16_t  media_r[USB_AUDIO_MEDIA_SAMPLES];
} UsbAudioMediaUpPkt;

typedef UsbAudioMediaUpPkt UwbAudioMediaUpPkt;

// -----------------------------------------------------------------------------
// 5. Radar 2.0 Telemetry, LED Matrix & 5.9 GHz C-ITS V2X (PCBA 08, ESP32-C5)
// -----------------------------------------------------------------------------
#define USB_RADAR_MAX_TARGETS 8
#define UWB_RADAR_MAX_TARGETS USB_RADAR_MAX_TARGETS

typedef struct __attribute__((packed)) {
    uint8_t  target_id;       // Track ID assigned by Wheeltec MR20 (24 GHz)
    uint16_t distance_cm;     // Distance in cm (0..10000 = 0..100 m)
    int16_t  speed_cm_s;      // Relative radial velocity in cm/s (positive = approaching)
    int16_t  azimuth_deg_10;  // Azimuth angle * 10 (-900..+900 = -90.0° .. +90.0°)
    uint16_t ttc_ms;          // Calculated Time-To-Collision in ms (0xFFFF = no risk)
    uint8_t  threat_level;    // 0 = None, 1 = Warning (Amber), 2 = Imminent Collision (Prio-1 Strobe)
} UsbRadarTargetEntry;

typedef UsbRadarTargetEntry UwbRadarTargetEntry;

typedef struct __attribute__((packed)) {
    uint8_t  target_count;    // Number of active targets (0..USB_RADAR_MAX_TARGETS)
    uint8_t  urgent_flag;     // 1 if any target has threat_level == 2 (Imminent Collision)
    uint16_t frame_index;     // Radar cycle counter
    UsbRadarTargetEntry targets[USB_RADAR_MAX_TARGETS];
} UsbRadarTargetsPkt;

typedef UsbRadarTargetsPkt UwbRadarTargetsPkt;

typedef struct __attribute__((packed)) {
    uint8_t  macro_mode;      // 0 = Standby/Off, 1 = Idle Halo, 2 = BSD Warning Amber, 3 = Hazard Prio-1 Strobe, 4 = ESS Brake Flash
    uint8_t  brightness_pct;  // 0..100%
    uint8_t  left_bsd_state;  // Left wing/mirror warning: 0=Off, 1=Amber Solid, 2=Fast Strobe
    uint8_t  right_bsd_state; // Right wing/mirror warning: 0=Off, 1=Amber Solid, 2=Fast Strobe
} UsbRadarLedCmdPkt;

typedef UsbRadarLedCmdPkt UwbRadarLedCmdPkt;

// 5.9 GHz C-ITS / ITS-G5 (IEEE 802.11p OCB) V2X Event from PCBA 08 (ESP32-C5-WROOM-1U)
typedef enum : uint8_t {
    V2X_MSG_NONE   = 0x00,
    V2X_MSG_SPATEM = 0x01, // Signal Phase and Timing (Traffic Light GLOSA Green Wave)
    V2X_MSG_MAPEM  = 0x02, // Intersection Geometry / Lane Topology
    V2X_MSG_CAM    = 0x03, // Cooperative Awareness Message (Approaching V2X Vehicle)
    V2X_MSG_DENM   = 0x04  // Decentralized Environmental Notification (Emergency Vehicle / Black Ice / Accident)
} UsbV2xMsgType;

typedef struct __attribute__((packed)) {
    uint8_t  v2x_msg_type;        // UsbV2xMsgType (SPATEM, MAPEM, CAM, DENM)
    uint32_t station_id;          // ITS Station ID (RSU or Emergency Vehicle ID)
    int32_t  latitude_1e7;        // Event / RSU Latitude * 1e7
    int32_t  longitude_1e7;       // Event / RSU Longitude * 1e7
    uint16_t distance_m;          // Distance to RSU / Hazard in meters
    uint8_t  traffic_light_phase; // 0=N/A, 1=Green, 2=Yellow, 3=Red
    uint8_t  time_to_change_s;    // Seconds until phase switch (GLOSA)
    uint8_t  recommended_speed_kph;// Optimal GLOSA green-wave speed in km/h
    uint8_t  denm_cause_code;     // ETSI EN 302 637-3 CauseCode (e.g. 95=EmergencyVehicle, 91=Breakdown, 3=Roadworks)
    int8_t   rssi_dbm;            // 5.9 GHz 802.11p OCB signal strength
} UsbV2xCitsEventPkt;

// -----------------------------------------------------------------------------
// 6. Pairing, Cryptographic Binding & Roaming
// -----------------------------------------------------------------------------
typedef struct __attribute__((packed)) {
    uint64_t pairing_nonce;   // Random 64-bit pairing challenge
    uint32_t vehicle_vin_hash;// 32-bit hash of vehicle identity for roaming slots
    uint16_t timeout_sec;     // Pairing window duration (e.g. 60 seconds)
} UsbPairingRequestPkt;

typedef UsbPairingRequestPkt UwbPairingRequestPkt;

typedef struct __attribute__((packed)) {
    uint64_t pairing_nonce;   // Echo of pairing nonce
    uint8_t  session_key[16]; // 128-Bit AES-GCM Session Key
    uint8_t  roaming_slot;    // Assigned vehicle slot (0..3)
    uint8_t  status;          // 0 = Success, 1 = Rejected
} UsbPairingConfirmPkt;

typedef UsbPairingConfirmPkt UwbPairingConfirmPkt;

// -----------------------------------------------------------------------------
// 7. Zero-Disassembly Central USB-Bus DFU & OTA Firmware Update (0x50 / 0x51)
// Allows Central Box (PCBA 01) or External Laptop on J3 to flash ALL nodes
// (PCBA 05, PCBA 03 Pod 1/2, PCBA 08 Radar, PCBA 09/10 OMM) over the 4-wire USB bus!
// -----------------------------------------------------------------------------
typedef enum : uint8_t {
    USB_DFU_OP_BEGIN_OTA     = 0x01, // Prepare target OTA partition (esp_ota_begin), erase flash
    USB_DFU_OP_WRITE_CHUNK   = 0x02, // Write 96-byte firmware block to OTA partition
    USB_DFU_OP_FINISH_REBOOT = 0x03, // Verify SHA256/CRC32, esp_ota_set_boot_partition, reboot
    USB_DFU_OP_ENTER_ROM_DFU = 0x04  // Switch target chip into hardware USB-Serial-JTAG / ROM DFU mode
} UsbDfuOperation;

typedef struct __attribute__((packed)) {
    uint8_t  dfu_op;          // UsbDfuOperation
    uint8_t  target_node;     // UsbNodeType being updated
    uint16_t chunk_index;     // Block sequence index (0..N)
    uint32_t offset_bytes;    // Byte offset in firmware image
    uint32_t total_size_bytes;// Total firmware image size (or expected CRC32 on FINISH_REBOOT)
    uint8_t  chunk_len;       // Valid bytes in data[] (0..USB_DFU_BLOCK_SIZE)
    uint8_t  data[USB_DFU_BLOCK_SIZE];
} UsbFwUpdatePushPkt;

typedef struct __attribute__((packed)) {
    uint8_t  dfu_op_ack;      // Echoed UsbDfuOperation
    uint8_t  status_code;     // 0 = OK, 1 = Flash Error, 2 = CRC Mismatch, 3 = Busy
    uint16_t chunk_index_ack; // Last committed chunk index
    uint32_t written_bytes;   // Total bytes written to target flash partition so far
    uint8_t  progress_pct;    // 0..100%
} UsbFwUpdateDonePkt;

// -----------------------------------------------------------------------------
// CRC16-CCITT Verification Function
// -----------------------------------------------------------------------------
static inline uint16_t usb_calculate_crc16(const uint8_t *data, size_t len) {
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

static inline uint16_t uwb_calculate_crc16(const uint8_t *data, size_t len) {
    return usb_calculate_crc16(data, len);
}

#ifdef __cplusplus
}
#endif

