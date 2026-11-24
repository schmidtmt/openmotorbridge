#pragma once

#include <stdint.h>
#include "driver/gpio.h"

// Forward compatibility definitions for ESP32-S31 extended GPIOs when building under ESP32-S3 target
#ifndef GPIO_NUM_22
#define GPIO_NUM_22 ((gpio_num_t)22)
#endif
#ifndef GPIO_NUM_23
#define GPIO_NUM_23 ((gpio_num_t)23)
#endif
#ifndef GPIO_NUM_24
#define GPIO_NUM_24 ((gpio_num_t)24)
#endif
#ifndef GPIO_NUM_25
#define GPIO_NUM_25 ((gpio_num_t)25)
#endif
#ifndef GPIO_NUM_56
#define GPIO_NUM_56 ((gpio_num_t)56)
#endif
#ifndef GPIO_NUM_57
#define GPIO_NUM_57 ((gpio_num_t)57)
#endif
#ifndef GPIO_NUM_59
#define GPIO_NUM_59 ((gpio_num_t)59)
#endif
#ifndef GPIO_NUM_60
#define GPIO_NUM_60 ((gpio_num_t)60)
#endif

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

// U5 (Southchip SW3526) 30W USB-PD & 15W Qi-Puck Fast Charger at J4 (Glovebox)
#define PIN_FAST_CHARGE_EN      GPIO_NUM_15  // U1 GPIO15 -> SW3526 / J4 Enable
#define PIN_FAST_CHARGE_FAULT_N GPIO_NUM_16  // U1 GPIO16 -> SW3526 Fault Interrupt (Active Low)
#define PIN_CP2AA_PWR_EN        PIN_FAST_CHARGE_EN
#define PIN_CP2AA_FAULT_N       PIN_FAST_CHARGE_FAULT_N
#define PIN_OTTOCAST_PWR_EN     PIN_FAST_CHARGE_EN
#define PIN_OTTOCAST_FAULT_N    PIN_FAST_CHARGE_FAULT_N
#define SW3526_I2C_ADDR         0x3C         // SW3526 Fast Charge Controller I2C Address

// MK1 (Knowles SPH0645LM4H-B) & J_SENSOR_EXT (6-Pin: 1=3V3, 2=GND, 3=SDA, 4=SCL, 5=MIC_DATA, 6=MIC_WS)
#define PIN_MIC_I2S_WS          GPIO_NUM_4   // U1 GPIO4  -> MK1 Pin 2 & J_SENSOR_EXT Pin 6 (MIC_I2S_WS)
#define PIN_MIC_I2S_BCLK        GPIO_NUM_5   // U1 GPIO5  -> MK1 Pin 3 (MIC_I2S_BCLK)
#define PIN_MIC_I2S_DATA        GPIO_NUM_35  // U1 Pad 12 (GPIO35) -> MK1 Pin 1 & J_SENSOR_EXT Pin 5 (MIC_I2S_DATA)

// J_POD_L & J_POD_R Wired Handlebar / Mirror Pod Buttons (Active Low)
#define PIN_BTN_SIG_L_N         GPIO_NUM_8   // U1 GPIO8  -> J_POD_L Pin 3 (BTN_SIG_L_N: Intercom PTT / HFP)
#define PIN_BTN_SIG_R_N         GPIO_NUM_9   // U1 GPIO9  -> J_POD_R Pin 3 (BTN_SIG_R_N: Action-Cam / Mode)
#define PIN_PTT_IN1_N           PIN_BTN_SIG_L_N
#define PIN_PTT_IN2_N           PIN_BTN_SIG_R_N

// U2 Feasycom FSC-BT802 (CSR8670) Bluetooth 5.1 Infotainment Bridge & SkylineOS / Boom! Box Audio Mux
#define PIN_FRONT_BT_EN         GPIO_NUM_57  // U1 Pad 39 (GPIO57) -> U2 Pin 3 (BT_EN / Power Enable)
#define PIN_FRONT_BT_RST        GPIO_NUM_56  // U1 Pad 38 (GPIO56) -> U2 Pin 4 (BT_RST / Hardware Reset)
#define PIN_FRONT_BT_UART_RX    GPIO_NUM_43  // U1 GPIO43 -> U2 TX (AT Command UART RX)
#define PIN_FRONT_BT_UART_TX    GPIO_NUM_44  // U1 GPIO44 -> U2 RX (AT Command UART TX)
#define PIN_FRONT_BT_I2S_BCLK   GPIO_NUM_10  // U1 GPIO10 -> U2 I2S Bit Clock
#define PIN_FRONT_BT_I2S_WS     GPIO_NUM_11  // U1 GPIO11 -> U2 I2S Word Select
#define PIN_FRONT_BT_I2S_DOUT   GPIO_NUM_12  // U1 GPIO12 -> U2 I2S Data In (Audio stream to bike speakers)
#define PIN_FRONT_BT_I2S_DIN    GPIO_NUM_48  // U1 GPIO48 -> U2 I2S Data Out (Nav audio in from headunit)

// Backward compatibility defines for legacy C3 bridge names
#define PIN_C3_EN               PIN_FRONT_BT_EN
#define PIN_C3_BOOT             PIN_FRONT_BT_RST
#define PIN_C3_UART_RX          PIN_FRONT_BT_UART_RX
#define PIN_C3_UART_TX          PIN_FRONT_BT_UART_TX
#define PIN_C3_I2S_BCLK         PIN_FRONT_BT_I2S_BCLK
#define PIN_C3_I2S_WS           PIN_FRONT_BT_I2S_WS
#define PIN_C3_I2S_SDO          PIN_FRONT_BT_I2S_DOUT
#define PIN_C3_I2S_SDI          PIN_FRONT_BT_I2S_DIN

// Shared I2C Bus: J_SENSOR_EXT Pin 3/4 (SAM-M10Q 0x42, TMP117 0x48, OPT3001 0x44, BMP390 0x76) + Dual OLEDs (J_DISP_L 0x3C, J_DISP_R 0x3D)
#define PIN_I2C_SDA             GPIO_NUM_22  // U1 Pad 17 (GPIO22) -> J_SENSOR_EXT Pin 3, J_DISP_L/R Pin 4 (I2C_SDA)
#define PIN_I2C_SCL             GPIO_NUM_23  // U1 Pad 18 (GPIO23) -> J_SENSOR_EXT Pin 4, J_DISP_L/R Pin 3 (I2C_SCL)
#define PIN_GNSS_RESET_N        GPIO_NUM_7   // U1 Pad 11 (GPIO7)  -> J_SENSOR_EXT Pin 8 (GNSS_RESET_N, Active-Low)
#define I2C_ADDR_OLED_LEFT      0x3C         // J_DISP_L Left Speaker-Corner Cockpit OLED
#define I2C_ADDR_OLED_RIGHT     0x3D         // J_DISP_R Right Speaker-Corner Cockpit OLED
#define I2C_ADDR_BMP390_BARO    0x76         // Sensor Puck BMP390 Barometer/Altimeter

// LED1 (WS2812B-2020), Q1 (DMN63D8 Dual MOSFET Mirror BSD LEDs) & Q2 (TPS1H100 Aux Light)
#define PIN_WS2812B_DIN         GPIO_NUM_24  // U1 Pad 19 (GPIO24) -> LED1 Pin 4 (WS2812B_DIN)
#define PIN_BSD_LED_LEFT        GPIO_NUM_25  // U1 Pad 20 (GPIO25) -> Q1 Pin 2 -> J_POD_L Pin 2 (BSD_LED_LEFT)
#define PIN_BSD_LED_RIGHT       GPIO_NUM_26  // U1 Pad 21 (GPIO26) -> Q1 Pin 5 -> J_POD_R Pin 2 (BSD_LED_RIGHT)
#define PIN_AUX_LIGHT_EN        GPIO_NUM_27  // U1 Pad 22 (GPIO27) -> Q2 Pin 3 -> J_AUX_LIGHT Pin 1 (AUX_LIGHT_EN)

// U1 Native High-Speed USB 2.0 PHY (480 Mbps) -> J1 Pins 3 & 4 (Direct 4-Wire Central Box Backbone)
#define PIN_USB_HS_DM           GPIO_NUM_19  // U1 Pad 54 -> J1 Pin 4 (USB_HS_DM)
#define PIN_USB_HS_DP           GPIO_NUM_20  // U1 Pad 55 -> J1 Pin 3 (USB_HS_DP)

// U9 (ESP32-E22-WROOM-2X2) 4-Bit SDIO 3.0 Wi-Fi 6E (5 GHz / 6 GHz) Co-Processor Interface
#define PIN_E22_SDIO_CLK        GPIO_NUM_35  // U1 Pad 30 -> U9 Pin 10 (SDIO_CLK)
#define PIN_E22_SDIO_CMD        GPIO_NUM_36  // U1 Pad 31 -> U9 Pin 11 (SDIO_CMD)
#define PIN_E22_SDIO_D0         GPIO_NUM_37  // U1 Pad 32 -> U9 Pin 12 (SDIO_D0)
#define PIN_E22_SDIO_D1         GPIO_NUM_38  // U1 Pad 33 -> U9 Pin 13 (SDIO_D1)
#define PIN_E22_SDIO_D2         GPIO_NUM_39  // U1 Pad 34 -> U9 Pin 14 (SDIO_D2)
#define PIN_E22_SDIO_D3         GPIO_NUM_40  // U1 Pad 35 -> U9 Pin 15 (SDIO_D3)
#define PIN_E22_IRQ             GPIO_NUM_60  // U1 Pad 37 (GPIO60) -> U9 Pin 16 (E22_IRQ)
#define PIN_E22_EN              GPIO_NUM_59  // U1 Pad 36 (GPIO59) -> U9 Pin 3 (E22_EN)

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
