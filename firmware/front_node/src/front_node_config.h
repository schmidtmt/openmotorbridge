#pragma once

#include <stdint.h>
#include "driver/gpio.h"

// =============================================================================
// OpenMotorBridge v10.0 - Universal Front-Node (PCBA 05) Ground-Truth Pinout
// Extracted 1:1 from hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb
// Core Architecture:
//   - U1: ESP32-S31-WROOM-1U (Dual-Core 320 MHz RISC-V with AI SIMD, 480 Mbps HS USB 2.0, internal 2.4GHz disabled)
//   - U9: ESP32-E22-WROOM-2X2 (Wi-Fi 6E 5/6 GHz 2x2 MIMO via 4-Bit SDIO 3.0)
//   - U2: Microchip USB2514Bi-AEZG 4-Port High-Speed USB 2.0 Hub:
//         * Upstream: J1 4-Wire USB Backbone to Central Box PCBA 01 (USB2517I Port 2)
//         * Port 1 (DN1): U3 SW3526 30W USB-PD Fast Charger (J_PD_PHONE)
//         * Port 2 (DN2): J_DONGLE (Ottocast / CarPlay via U4 TPS2051B)
//         * Port 3 (DN3): J4 Glovebox Hub PCBA 05B
//         * Port 4 (DN4): U1 ESP32-S31 Native High-Speed USB 2.0 PHY (Pad 13/14)
//   - J_SENSOR_EXT: External Sensor-Puck (SAM-M10Q GNSS + TMP117 + OPT3001 + Knowles Mic)
//   - J_DISP_L / J_DISP_R: Dual Cockpit Speaker-Corner OLED Displays (I2C 0x3C / 0x3D)
//   - NO local flash port (J7 removed; flashed via Central USB-Bus DFU 0x50 on J1!)
//   - NO 2.4 GHz radio on PCBA 05 (Action-Cam BLE migrated to Central Box PCBA 01!)
// =============================================================================

#define FRONT_NODE_HW_REV_MAJOR         10
#define FRONT_NODE_HW_REV_MINOR         0

// --- 1. U1 (ESP32-S31-WROOM-1U) Exact KiCad Pad & GPIO Assignments on PCBA 05 ---
#define PIN_BOOT_BUTTON         GPIO_NUM_0   // Boot / Service Mode Sense

// U4 (TI TPS2051BDBVR) High-Side Power Switch for J_DONGLE (CarPlay / Android Auto)
#define PIN_CP2AA_PWR_EN        GPIO_NUM_1   // U1 Pad 39 -> U4 Pin 3 (CP2AA_PWR_EN)
#define PIN_CP2AA_FAULT_N       GPIO_NUM_2   // U1 Pad 38 -> U4 Pin 4 (CP2AA_FAULT_N, Active Low)
#define PIN_OTTOCAST_PWR_EN     PIN_CP2AA_PWR_EN
#define PIN_OTTOCAST_FAULT_N    PIN_CP2AA_FAULT_N

// MK1 (Knowles SPH0645LM4H-B) & J_SENSOR_EXT (6-Pin: 1=3V3, 2=GND, 3=SDA, 4=SCL, 5=MIC_DATA, 6=MIC_WS)
#define PIN_MIC_I2S_WS          GPIO_NUM_6   // U1 Pad 6  -> MK1 Pin 2 & J_SENSOR_EXT Pin 6 (MIC_I2S_WS)
#define PIN_MIC_I2S_BCLK        GPIO_NUM_7   // U1 Pad 7  -> MK1 Pin 3 (MIC_I2S_BCLK)
#define PIN_MIC_I2S_DATA        GPIO_NUM_12  // U1 Pad 12 -> MK1 Pin 1 & J_SENSOR_EXT Pin 5 (MIC_I2S_DATA)

// J_POD_L & J_POD_R Wired Handlebar / Mirror Pod Buttons (Active Low)
#define PIN_BTN_SIG_L_N         GPIO_NUM_8   // U1 Pad 8  -> J_POD_L Pin 3 (BTN_SIG_L_N: Intercom PTT / HFP)
#define PIN_BTN_SIG_R_N         GPIO_NUM_9   // U1 Pad 9  -> J_POD_R Pin 3 (BTN_SIG_R_N: Action-Cam / Mode)
#define PIN_PTT_IN1_N           PIN_BTN_SIG_L_N
#define PIN_PTT_IN2_N           PIN_BTN_SIG_R_N
#define PIN_PTT_IN3_N           GPIO_NUM_15  // Optional 3rd Handlebar Input

// Shared I2C Bus: J_SENSOR_EXT Pin 3/4 (SAM-M10Q 0x42, TMP117 0x48, OPT3001 0x44) + Dual OLEDs (J_DISP_L 0x3C, J_DISP_R 0x3D)
#define PIN_I2C_SDA             GPIO_NUM_17  // U1 Pad 17 -> J_SENSOR_EXT Pin 3, J_DISP_L/R Pin 4 (I2C_SDA)
#define PIN_I2C_SCL             GPIO_NUM_18  // U1 Pad 18 -> J_SENSOR_EXT Pin 4, J_DISP_L/R Pin 3 (I2C_SCL)
#define I2C_ADDR_OLED_LEFT      0x3C         // J_DISP_L Left Speaker-Corner Cockpit OLED
#define I2C_ADDR_OLED_RIGHT     0x3D         // J_DISP_R Right Speaker-Corner Cockpit OLED

// LED1 (WS2812B-2020), Q1 (DMN63D8 Dual MOSFET Mirror BSD LEDs) & Q2 (TPS1H100 Aux Light)
#define PIN_WS2812B_DIN         GPIO_NUM_11  // U1 Pad 19 -> LED1 Pin 4 (WS2812B_DIN)
#define PIN_BSD_LED_LEFT        GPIO_NUM_13  // U1 Pad 20 -> Q1 Pin 2 -> J_POD_L Pin 2 (BSD_LED_LEFT)
#define PIN_BSD_LED_RIGHT       GPIO_NUM_16  // U1 Pad 21 -> Q1 Pin 5 -> J_POD_R Pin 2 (BSD_LED_RIGHT)
#define PIN_AUX_LIGHT_EN        GPIO_NUM_14  // U1 Pad 22 -> Q2 Pin 3 -> J_AUX_LIGHT Pin 1 (AUX_LIGHT_EN)

// U1 Native High-Speed USB 2.0 PHY -> U2 (USB2514Bi-AEZG Port 4) -> J1 (Central Box)
#define PIN_USB_HS_DM           GPIO_NUM_19  // U1 Pad 13 -> U2 Pin 7 (USB_HS_DM)
#define PIN_USB_HS_DP           GPIO_NUM_20  // U1 Pad 14 -> U2 Pin 8 (USB_HS_DP)

// U9 (ESP32-E22-WROOM-2X2) 4-Bit SDIO 3.0 Wi-Fi 6E (5 GHz / 6 GHz) Co-Processor Interface
#define PIN_E22_SDIO_CLK        GPIO_NUM_35  // U1 Pad 30 -> U9 Pin 10 (SDIO_CLK)
#define PIN_E22_SDIO_CMD        GPIO_NUM_36  // U1 Pad 31 -> U9 Pin 11 (SDIO_CMD)
#define PIN_E22_SDIO_D0         GPIO_NUM_37  // U1 Pad 32 -> U9 Pin 12 (SDIO_D0)
#define PIN_E22_SDIO_D1         GPIO_NUM_33  // U1 Pad 33 -> U9 Pin 13 (SDIO_D1)
#define PIN_E22_SDIO_D2         GPIO_NUM_34  // U1 Pad 34 -> U9 Pin 14 (SDIO_D2)
#define PIN_E22_SDIO_D3         GPIO_NUM_38  // U1 Pad 35 -> U9 Pin 15 (SDIO_D3)
#define PIN_E22_IRQ             GPIO_NUM_39  // U1 Pad 37 -> U9 Pin 16 (E22_IRQ)
#define PIN_E22_EN              GPIO_NUM_40  // U1 Pad 40 -> U9 Pin 3  (E22_EN)

// --- 2. ESP32-E22 Wi-Fi 6E (5 GHz / 6 GHz) Cockpit Gateway Configuration ---
#define COCKPIT_WIFI_AP_SSID        "OpenMotorBridge-6E"
#define COCKPIT_WIFI_AP_PASS        "openmotor2026"
#define COCKPIT_WIFI_AP_CHANNEL     36       // Clean 5 GHz UNII-1 Channel 36 (Zero 2.4 GHz Interference!)
#define COCKPIT_WIFI_AP_MAX_CONN    4
#define COCKPIT_WIFI_AP_IP          "192.168.4.1"
#define COCKPIT_WIFI_AP_GW          "192.168.4.1"
#define COCKPIT_WIFI_AP_NETMASK     "255.255.255.0"
#define COCKPIT_WIFI_IP_RIDER_PHONE "192.168.4.10"
#define COCKPIT_WIFI_IP_PAX_PHONE   "192.168.4.11"
#define COCKPIT_WIFI_IP_SKYLINE_OS  "192.168.4.20"

// Aux Light Operating Modes (Q2 TPS1H100)
enum AuxLightMode : uint8_t {
    AUX_LIGHT_OFF            = 0x00,
    AUX_LIGHT_ON             = 0x01,
    AUX_LIGHT_STROBE         = 0x02    // 4.5 Hz Emergency Brake / Hazard Strobe
};

// Mirror Blind Spot Warning Alert Level (Q1 DMN63D8 -> J_POD_L / J_POD_R)
enum BsdAlertLevel : uint8_t {
    BSD_LEVEL_OFF            = 0x00,
    BSD_LEVEL_SOLID_AMBER    = 0x01,   // Target in blind spot zone (< 15 m)
    BSD_LEVEL_FAST_STROBE    = 0x02    // Rapid overtake / collision hazard (< 2.5s TTC, 8 Hz flash)
};

// Handlebar Button Identifier (J_POD_L / J_POD_R)
enum HandlebarButtonId : uint8_t {
    BTN_INTERCOM_PTT         = 0x01,   // J_POD_L Pin 3 (BTN_SIG_L_N)
    BTN_CAM_HIGHLIGHT        = 0x02,   // J_POD_R Pin 3 (BTN_SIG_R_N)
    BTN_MEDIA_VOICE          = 0x03
};

// PTT Multi-Click Action Types
enum PttClickType : uint8_t {
    PTT_CLICK_NONE           = 0x00,
    PTT_CLICK_SINGLE         = 0x01,   // Short press <400ms
    PTT_CLICK_DOUBLE         = 0x02,   // Double click
    PTT_CLICK_LONG           = 0x03,   // Long press >800ms
    PTT_CLICK_RESET_PAIRING  = 0x04    // Continuous 10s hold
};

// --- 3. Functional Timing & Threshold Parameters ---
#define PTT_DEBOUNCE_MS              15      // Hardware/Software RC debounce threshold
#define PTT_DOUBLE_CLICK_MS          350     // Inter-click max duration for double click
#define PTT_LONG_PRESS_MS            800     // Duration threshold for long press
#define PTT_RESET_HOLD_MS            10000   // Continuous 10s hold
#define OTTOCAST_RESET_PULSE_MS      2500    // U4 TPS2051B power-off duration during 1-click reboot
#define CAFE_DISCONNECT_SEC          60      // Delay before disabling J_DONGLE VBUS after ignition off
#define AUDIO_RMS_INTERVAL_MS        20      // 50 Hz telemetry rate for dBA edge audio
#define HEARTBEAT_INTERVAL_MS        500     // USB 2.0 Backbone link supervision heartbeat
