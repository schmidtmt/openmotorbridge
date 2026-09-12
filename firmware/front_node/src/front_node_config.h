#pragma once

#include "driver/gpio.h"

// =============================================================================
// OpenMotorBridge - Universal Front Node (PCBA 05) Pinout & Configuration
// =============================================================================

// --- 1. GPIO Pin Assignments (ESP32-S3 on PCBA 05) ---
#define PIN_BOOT_BUTTON         GPIO_NUM_0   // Boot/Config Tactile Button SW1 (Active Low)
#define PIN_OTTOCAST_PWR_EN     GPIO_NUM_1   // TI TPS2051B USB VBUS Power Enable (Active High)
#define PIN_OTTOCAST_FAULT_N    GPIO_NUM_2   // TI TPS2051B Fault Alert (Active Low, Open-Drain)
#define PIN_CAN_TERM_EN         GPIO_NUM_3   // CPC1017N Solid-State Relay for 120R CAN Termination (Auto-Sensing)
#define PIN_KL15_SENSE          GPIO_NUM_4   // 12V Ignition KL15 Sense via voltage divider
#define PIN_CAN_SILENT          GPIO_NUM_5   // TI TCAN334G Pin 8 Silent / Listen-Only Mode
#define PIN_MIC_I2S_WS          GPIO_NUM_6   // Knowles SPH0645 I2S Word Select / LRCLK
#define PIN_MIC_I2S_BCLK        GPIO_NUM_7   // Knowles SPH0645 I2S Bit Clock
#define PIN_MIC_I2S_DATA        GPIO_NUM_8   // Knowles SPH0645 I2S Serial Data
#define PIN_I2C_SDA             GPIO_NUM_9   // Qwiic J12 I2C SDA
#define PIN_I2C_SCL             GPIO_NUM_10  // Qwiic J12 I2C SCL
#define PIN_WS2812B_DIN         GPIO_NUM_11  // Onboard WS2812B-2020 RGB Status LED (Light-pipe in lid)
#define PIN_BSD_LED_LEFT        GPIO_NUM_12  // Left Mirror Radar BSD Warning LED Gate (DMN63D8 Ch A)
#define PIN_BSD_LED_RIGHT       GPIO_NUM_13  // Right Mirror Radar BSD Warning LED Gate (DMN63D8 Ch B)
#define PIN_AUX_LIGHT_EN        GPIO_NUM_14  // TPS1H100 High-Side Switch (J11 Aux Light / Strobe)
#define PIN_PTT_IN1_N           GPIO_NUM_15  // Handlebar Button 1: Intercom PTT (Active Low)
#define PIN_PTT_IN2_N           GPIO_NUM_16  // Handlebar Button 2: Action-Cam Bookmark / Highlight (Active Low)
#define PIN_PTT_IN3_N           GPIO_NUM_17  // Handlebar Button 3: Media Next / Siri / Voice (Active Low)
#define PIN_USB_DM              GPIO_NUM_18  // Native USB D- (Service / Flash Port J7)
#define PIN_USB_DP              GPIO_NUM_19  // Native USB D+ (Service / Flash Port J7)
#define PIN_CAN_TX              GPIO_NUM_21  // TCAN334G TWAI / CAN Transmitter
#define PIN_CAN_RX              GPIO_NUM_47  // TCAN334G TWAI / CAN Receiver

// Legacy alias for single PTT button compatibility
#define PIN_PTT_INPUT_N         PIN_PTT_IN1_N

// --- 2. ESP-NOW Wireless Bridge Constants ---
#define ESPNOW_WIFI_CHANNEL     1
#define ESPNOW_MAX_PAYLOAD      250
#define FRONT_NODE_PROTOCOL_VER 0x02

// Packet Types
enum FrontNodePacketType : uint8_t {
    PKT_TYPE_HEARTBEAT       = 0x01,
    PKT_TYPE_PTT_EVENT       = 0x02,
    PKT_TYPE_AUDIO_RMS       = 0x03,
    PKT_TYPE_OTTOCAST_STATUS = 0x04,
    PKT_TYPE_CAN_TELEMETRY   = 0x05,
    PKT_TYPE_CAM_STATUS      = 0x06,   // Action-Cam telemetry (brand, state, bat%, sd_min, flags)
    PKT_TYPE_CAM_SCAN_RES    = 0x07,   // Discovered BLE camera item (mac, rssi, brand, name)
    PKT_TYPE_BINDING_BEACON  = 0x08,   // Rescue / pairing beacon from Central Box
    PKT_TYPE_BINDING_ACK     = 0x09,   // Binding confirmation from Front Node to Central Box
    PKT_TYPE_BSD_TRIGGER     = 0x0A,   // Central Box -> Front Node: Rear Radar Mirror BSD Trigger
    PKT_TYPE_COCKPIT_STATUS  = 0x0B,   // Front Node -> Central Box: 4-Port Hub, Qi, Aux Light, CAN Term
    PKT_TYPE_CMD_POWER_CYCLE = 0x10,
    PKT_TYPE_CMD_CONFIG      = 0x11,
    PKT_TYPE_CAM_CMD         = 0x12,   // Action-Cam remote command from Central Box / WebApp
    PKT_TYPE_CMD_UNBIND      = 0x13,   // Manual unpair / clear NVS binding command
    PKT_TYPE_CMD_AUX_LIGHT   = 0x14,   // Central Box / PWA -> Front Node: Set Aux Light state (Off, On, Strobe)
    PKT_TYPE_CMD_CAN_TERM    = 0x15,   // Central Box -> Front Node: Set CAN Termination Relay state
    PKT_TYPE_OTA_BEGIN       = 0x20,
    PKT_TYPE_OTA_CHUNK       = 0x21,
    PKT_TYPE_OTA_FINISH      = 0x22
};

// Aux Light Operating Modes
enum AuxLightMode : uint8_t {
    AUX_LIGHT_OFF            = 0x00,
    AUX_LIGHT_ON             = 0x01,
    AUX_LIGHT_STROBE         = 0x02    // 4-5 Hz Emergency Brake Strobe
};

// Radar Blind Spot Warning Alert Level
enum BsdAlertLevel : uint8_t {
    BSD_LEVEL_OFF            = 0x00,
    BSD_LEVEL_SOLID_AMBER    = 0x01,   // Target in blind spot zone (< 15 m)
    BSD_LEVEL_FAST_STROBE    = 0x02    // Rapid overtake / collision hazard (< 2.5s TTC, 8 Hz flash)
};

// Handlebar Button Identifier
enum HandlebarButtonId : uint8_t {
    BTN_INTERCOM_PTT         = 0x01,   // J3 Pin 2 (PTT_IN1_N)
    BTN_CAM_HIGHLIGHT        = 0x02,   // J3 Pin 3 (PTT_IN2_N)
    BTN_MEDIA_VOICE          = 0x03    // J3 Pin 4 (PTT_IN3_N)
};

// Front Node Hardware-Binding States (1:1 Binding Machine)
enum FrontNodeBindingState : uint8_t {
    BINDING_STATE_UNPAIRED   = 0x00,   // Fresh / factory-reset: open pairing beacon listener
    BINDING_STATE_LINKED     = 0x01,   // Exclusive 1:1 link with stored Central Box MAC
    BINDING_STATE_ORPHAN     = 0x02    // Central Box lost (>60s timeout): ready for Proximity-Rescue
};

// Camera Profile Types
enum CamProfileType : uint8_t {
    CAM_PROFILE_NONE         = 0x00,
    CAM_PROFILE_GOPRO        = 0x01,   // GoPro Hero 9/10/11/12/13, Max (Open GoPro BLE)
    CAM_PROFILE_INSTA360     = 0x02,   // Insta360 X3/X4, Ace Pro, GO 3
    CAM_PROFILE_DJI          = 0x03    // DJI Osmo Action 3/4/5 Pro, Osmo 360
};

// Camera Connection & Recording States
enum CamState : uint8_t {
    CAM_STATE_DISCONNECTED   = 0x00,
    CAM_STATE_SCANNING       = 0x01,
    CAM_STATE_CONNECTING     = 0x02,
    CAM_STATE_CONNECTED      = 0x03,
    CAM_STATE_RECORDING      = 0x04
};

// Action-Cam Command Subtypes for PKT_TYPE_CAM_CMD
enum CamCmdSubtype : uint8_t {
    CAM_CMD_TOGGLE_REC       = 0x01,   // Start/Stop recording toggle
    CAM_CMD_HILIGHT_TAG      = 0x02,   // Insert bookmark / highlight marker
    CAM_CMD_START_SCAN       = 0x03,   // Scan for nearby BLE cameras (10s)
    CAM_CMD_PAIR             = 0x04,   // Pair specific MAC with profile
    CAM_CMD_UNPAIR           = 0x05,   // Unpair and clear from NVS
    CAM_CMD_SET_AUTOCONNECT  = 0x06,   // Toggle autonomous autoconnect on boot/wake
    CAM_CMD_SET_FUEL_FILTER  = 0x07    // Toggle KL15 Tankpausen-Filter (Auto-Stop/Resume)
};

// PTT Multi-Click Action Types
enum PttClickType : uint8_t {
    PTT_CLICK_NONE           = 0x00,
    PTT_CLICK_SINGLE         = 0x01,   // Short press <400ms: Intercom/Radio PTT (<0.9ms zero-latency)
    PTT_CLICK_DOUBLE         = 0x02,   // Double click: Action-Cam Record Toggle (Start/Stop)
    PTT_CLICK_LONG           = 0x03,   // Long press >800ms: Action-Cam HiLight Marker
    PTT_CLICK_RESET_PAIRING  = 0x04    // Continuous 10s hold: Manual unpair & NVS binding reset
};

// --- 3. Functional Timing & Threshold Parameters ---
#define PTT_DEBOUNCE_MS              15      // Hardware/Software RC debounce threshold
#define PTT_DOUBLE_CLICK_MS          350     // Inter-click max duration for double click
#define PTT_LONG_PRESS_MS            800     // Duration threshold for HiLight bookmark trigger
#define PTT_RESET_HOLD_MS            10000   // Continuous 10s hold to force unpair and NVS reset
#define OTTOCAST_RESET_PULSE_MS      2500    // VBUS power-off duration during 1-click reboot
#define CAFE_DISCONNECT_SEC          60      // Delay before disabling VBUS after ignition off
#define AUDIO_RMS_INTERVAL_MS        20      // 50 Hz telemetry rate for dBA edge audio
#define HEARTBEAT_INTERVAL_MS        500     // Link supervision heartbeat
#define ORPHAN_HEARTBEAT_TIMEOUT_SEC 60      // Heartbeat timeout before entering ORPHAN state
#define PROXIMITY_RSSI_THRESHOLD_DBM -42     // Minimum RSSI for Proximity-Rescue (< 1 m on bike)

