#pragma once

#include "driver/gpio.h"

// =============================================================================
// OpenMotorBridge - Universal Smart Cartridge (PCBA 03 Rev 3.0) Pinout
// Target: Espressif ESP32-C6 RISC-V @ 160 MHz
// =============================================================================

// --- 1. Mechatronics Actuator Outputs (4x AO3400A N-MOSFETs, Active HIGH) ---
#define PIN_ACT1_PLUS           GPIO_NUM_16  // ACT 1: Plus (+) / Lauter / Next Track
#define PIN_ACT2_MINUS          GPIO_NUM_17  // ACT 2: Minus (-) / Leiser / Prev Track
#define PIN_ACT3_CENTER         GPIO_NUM_2   // ACT 3: Center / Phone / Confirm
#define PIN_ACT4_MESH           GPIO_NUM_3   // ACT 4: Mesh Button (Sena / Cardo / OMM)

// --- 2. Qorvo DW3110 Ultra-Wideband SPI Interface (6.489 GHz Ch. 5) ---
#define PIN_UWB_SCK             GPIO_NUM_4   // SPI SCK
#define PIN_UWB_MOSI            GPIO_NUM_5   // SPI MOSI
#define PIN_UWB_MISO            GPIO_NUM_6   // SPI MISO
#define PIN_UWB_CS              GPIO_NUM_7   // SPI Chip Select (Active Low)
#define PIN_UWB_IRQ             GPIO_NUM_8   // DW3110 Interrupt Request (Active High)
#define PIN_UWB_RST             GPIO_NUM_9   // DW3110 Hardware Reset (Active Low)

// --- 3. Status LED ---
#define PIN_CARTRIDGE_LED       GPIO_NUM_10  // Tiny SMD Status LED

// --- 4. Hardware Bay ID Detection (Bucht 1 Links vs Bucht 2 Rechts) ---
// Grounded via pin strap in Bay 1, pulled high in Bay 2
#define PIN_BAY_SELECT          GPIO_NUM_14

// --- 5. Everest Semi ES8388 Audio-Codec Interface (24-Bit / 48 kHz Stereo) ---
#define PIN_CODEC_I2C_SCL       GPIO_NUM_15  // ES8388 Control I2C SCL
#define PIN_I2S_MCLK            GPIO_NUM_18  // Master Clock (12.288 MHz = 256 * 48 kHz)
#define PIN_I2S_BCLK            GPIO_NUM_19  // Bit Clock (3.072 MHz = 64 * 48 kHz)
#define PIN_I2S_WS              GPIO_NUM_20  // Word Select / LRCLK (48 kHz)
#define PIN_I2S_DOUT            GPIO_NUM_21  // Serial Data Out (to ES8388 DAC -> Headset Mic-In)
#define PIN_I2S_DIN             GPIO_NUM_22  // Serial Data In (from ES8388 ADC <- Headset Spk-Out)
#define PIN_CODEC_I2C_SDA       GPIO_NUM_23  // ES8388 Control I2C SDA
