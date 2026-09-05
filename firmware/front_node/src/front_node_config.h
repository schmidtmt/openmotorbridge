#pragma once

#include "driver/gpio.h"

// =============================================================================
// OpenMotorBridge - Universal Front Node (PCBA 05) Pinout & Configuration
// =============================================================================

// --- 1. GPIO Pin Assignments ---
#define PIN_PTT_INPUT_N         GPIO_NUM_0   // Active-Low Handlebar PTT (Interrupt)
#define PIN_MIC_I2S_WS          GPIO_NUM_1   // Knowles SPH0645 I2S Word Select / LRCLK
#define PIN_MIC_I2S_BCLK        GPIO_NUM_2   // Knowles SPH0645 I2S Bit Clock
#define PIN_MIC_I2S_DATA        GPIO_NUM_3   // Knowles SPH0645 I2S Serial Data
#define PIN_CAN_RX             GPIO_NUM_4   // TCAN334G TWAI / CAN Receiver
#define PIN_CAN_TX             GPIO_NUM_5   // TCAN334G TWAI / CAN Transmitter
#define PIN_OTTOCAST_PWR_EN     GPIO_NUM_6   // TI TPS2051B USB VBUS Power Enable (Active High)
#define PIN_OTTOCAST_FAULT_N    GPIO_NUM_7   // TI TPS2051B Fault Alert (Active Low, Open-Drain)
#define PIN_STATUS_LED          GPIO_NUM_8   // Status LED D1 (Green, Active High)
#define PIN_BOOT_BUTTON         GPIO_NUM_9   // Boot/Config Tactile Button SW2 (Active Low)
#define PIN_USB_DM              GPIO_NUM_18  // Native USB D- (Service / Flash Port)
#define PIN_USB_DP              GPIO_NUM_19  // Native USB D+ (Service / Flash Port)

// --- 2. ESP-NOW Wireless Bridge Constants ---
#define ESPNOW_WIFI_CHANNEL     1
#define ESPNOW_MAX_PAYLOAD      250
#define FRONT_NODE_PROTOCOL_VER 0x01

// Packet Types
enum FrontNodePacketType : uint8_t {
    PKT_TYPE_HEARTBEAT       = 0x01,
    PKT_TYPE_PTT_EVENT       = 0x02,
    PKT_TYPE_AUDIO_RMS       = 0x03,
    PKT_TYPE_OTTOCAST_STATUS = 0x04,
    PKT_TYPE_CAN_TELEMETRY   = 0x05,
    PKT_TYPE_CAM_STATUS      = 0x06,   // Action-Cam telemetry (brand, state, bat%, sd_min, flags)
    PKT_TYPE_CAM_SCAN_RES    = 0x07,   // Discovered BLE camera item (mac, rssi, brand, name)
    PKT_TYPE_CMD_POWER_CYCLE = 0x10,
    PKT_TYPE_CMD_CONFIG      = 0x11,
    PKT_TYPE_CAM_CMD         = 0x12,   // Action-Cam remote command from Central Box / WebApp
    PKT_TYPE_OTA_BEGIN       = 0x20,
    PKT_TYPE_OTA_CHUNK       = 0x21,
    PKT_TYPE_OTA_FINISH      = 0x22
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
    PTT_CLICK_LONG           = 0x03    // Long press >800ms: Action-Cam HiLight Marker
};

// --- 3. Functional Timing Parameters ---
#define PTT_DEBOUNCE_MS         15      // Hardware/Software RC debounce threshold
#define PTT_DOUBLE_CLICK_MS     350     // Inter-click max duration for double click
#define PTT_LONG_PRESS_MS       800     // Duration threshold for HiLight bookmark trigger
#define OTTOCAST_RESET_PULSE_MS 2500    // VBUS power-off duration during 1-click reboot
#define CAFE_DISCONNECT_SEC     60      // Delay before disabling VBUS after ignition off
#define AUDIO_RMS_INTERVAL_MS   20      // 50 Hz telemetry rate for dBA edge audio
#define HEARTBEAT_INTERVAL_MS   500     // Link supervision heartbeat

