#pragma once

#include "driver/gpio.h"

// =============================================================================
// OpenMotorBridge - PCBA 03 v10.0 Satellite Pod Interface Board Pinout
// Target: Espressif ESP32-C6-MINI-1U (U1, 32-Bit RISC-V @ 160 MHz)
// KiCad Source: hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb
// =============================================================================

// --- 1. Mechatronics Actuator Outputs (4x AO3400A N-MOSFETs Q1..Q4, Active HIGH) ---
// J_ACT (8-Pin JST-SH 1.0mm): Pin 6=ACT_1, Pin 5=ACT_2, Pin 4=ACT_3, Pin 3=ACT_4
#define PIN_ACT1_PLUS           GPIO_NUM_5   // U1 Pad 10 (GPIO5)  -> R1 -> Q1 Gate (ACT 1: Plus / Vol+)
#define PIN_ACT2_MINUS          GPIO_NUM_8   // U1 Pad 22 (GPIO8)  -> R2 -> Q2 Gate (ACT 2: Minus / Vol-)
#define PIN_ACT3_CENTER         GPIO_NUM_3   // U1 Pad 6  (GPIO3)  -> R3 -> Q3 Gate (ACT 3: Center / Phone)
#define PIN_ACT4_MESH           GPIO_NUM_4   // U1 Pad 9  (GPIO4)  -> R4 -> Q4 Gate (ACT 4: Mesh Button)

// --- 2. 4-Wire USB 2.0 Automotive Backbone Interface (J_BUS 4-Pin JST-GH) ---
#define PIN_POD_USB_DM          GPIO_NUM_12  // U1 Pad 17 (GPIO12) -> J_BUS Pin 4 (USB D-)
#define PIN_POD_USB_DP          GPIO_NUM_13  // U1 Pad 18 (GPIO13) -> J_BUS Pin 3 (USB D+)

// --- 3. J_AUDIO_PWR (8-Pin JST-SH 1.0mm) Control & Auto-Sense Signals ---
// OMM_DETECT (J_AUDIO_PWR Pin 6 & U4 TS5A3159DBVR Pin 6 IN):
//   LOW (0V)    = Analog OEM Intercom (Sena / Cardo / Midland via U3 ES8388)
//   HIGH (3.3V) = Digital OMM Tri-Band Module (PCBA 09/10 via U4 NO USB-Audio)
#define PIN_OMM_DETECT          GPIO_NUM_0   // U1 Pad 12 (GPIO0)  -> OMM_DETECT (10k R9 Pull-Up)
#define PIN_POD_PTT_BTN         GPIO_NUM_2   // U1 Pad 5  (GPIO2)  -> J_AUDIO_PWR Pin 8 (Physical PTT, Active-Low)

// --- 4. Status LED & Bay ID Strap ---
#define PIN_CARTRIDGE_LED       GPIO_NUM_19  // U1 Pad 25 (GPIO19) -> Tiny SMD Status LED
#define PIN_BAY_SELECT          GPIO_NUM_20  // U1 Pad 26 (GPIO20) -> Hardware Bay Strap: LOW = Pod 1 Left (0x03), HIGH = Pod 2 Right (0x04)

// --- 5. Everest Semi ES8388 Audio-Codec (U3) & SW3516 30W USB-PD (U_PD) ---
#define PIN_CODEC_I2C_SCL       GPIO_NUM_1   // U1 Pad 13 (GPIO1)  -> ES8388 Pin 27 & SW3516 SCL
#define PIN_CODEC_I2C_SDA       GPIO_NUM_9   // U1 Pad 23 (GPIO9)  -> ES8388 Pin 28 & SW3516 SDA
#define PIN_I2S_MCLK            GPIO_NUM_6   // U1 Pad 15 (GPIO6)  -> ES8388 Master Clock (12.288 MHz)
#define PIN_I2S_BCLK            GPIO_NUM_7   // U1 Pad 16 (GPIO7)  -> ES8388 Bit Clock (3.072 MHz)
#define PIN_I2S_WS              GPIO_NUM_14  // U1 Pad 19 (GPIO14) -> ES8388 Word Select / LRCLK (48 kHz)
#define PIN_I2S_DOUT            GPIO_NUM_15  // U1 Pad 20 (GPIO15) -> ES8388 DAC In (to OEM Mic-In via U4 NC)
#define PIN_I2S_DIN             GPIO_NUM_18  // U1 Pad 24 (GPIO18) -> ES8388 ADC Out (from OEM Spk-Out L/R)
