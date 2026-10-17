#pragma once

#include <stdint.h>
#include <stdbool.h>

// =============================================================================
// OpenMotorBridge - PCBA 07 2-in-1 LoRa Smart-Keyfob & Silent Pager
// Target: Nordic Semiconductor nRF52840-QIAA (AQFN-73) @ 64 MHz ARM Cortex-M4F
// =============================================================================

// -----------------------------------------------------------------------------
// 1. Tactile Pushbuttons (Active LOW, 10k External Pull-Ups R1 & R2)
// -----------------------------------------------------------------------------
// SW1: Arm / Disarm Bike Alarm (Pad G1)
#define KEYFOB_PIN_BTN_ARM_N        8   // P0.08
#define KEYFOB_PAD_BTN_ARM_N        "G1"

// SW2: SOS Panic Alert / Handlebar Shutter (Pad J1)
#define KEYFOB_PIN_BTN_SOS_N        7   // P0.07
#define KEYFOB_PAD_BTN_SOS_N        "J1"

// -----------------------------------------------------------------------------
// 2. Battery & Qi Wireless Charger Supervision (TI BQ51003 & BQ25100)
// -----------------------------------------------------------------------------
// BQ25100 Charge Status Output (Pad K2, Low Active: 0 = Charging, 1 = Standby/Full)
#define KEYFOB_PIN_CHG_STAT         5   // P0.05
#define KEYFOB_PAD_CHG_STAT         "K2"

// Analog Battery Voltage Sensing (VBAT divider connected to AIN1)
#define KEYFOB_ADC_VBAT_PIN         29  // P0.29 (SAADC Input)
#define KEYFOB_BAT_LOW_THRESH_MV    3400 // 3.4V Low Battery Cut-Off / Alert
#define KEYFOB_BAT_FULL_THRESH_MV   4200 // 4.2V Full LiPo Charge

// -----------------------------------------------------------------------------
// 3. User Feedback: TI DRV2605L Haptics & LRA Linear Resonant Actuator
// -----------------------------------------------------------------------------
// DRV2605L Hardware Enable (Pad M2, Active HIGH)
#define KEYFOB_PIN_DRV_EN           3   // P0.03
#define KEYFOB_PAD_DRV_EN           "M2"

// I2C Interface to DRV2605L (Pad N1 = SDA, Pad P2 = SCL)
#define KEYFOB_PIN_I2C_SDA          2   // P0.02
#define KEYFOB_PAD_I2C_SDA          "N1"
#define KEYFOB_PIN_I2C_SCL          28  // P0.28
#define KEYFOB_PAD_I2C_SCL          "P2"
#define KEYFOB_DRV2605_I2C_ADDR     0x5A

// -----------------------------------------------------------------------------
// 4. User Feedback: Piezo Buzzer & WS2812B Smart RGB LED
// -----------------------------------------------------------------------------
// Murata CPT-9019S SMD Piezo Buzzer (Pad F2, PWM Tone Generator)
#define KEYFOB_PIN_BUZZER_PWM       6   // P0.06
#define KEYFOB_PAD_BUZZER_PWM       "F2"
#define KEYFOB_BUZZER_FREQ_ARM      2700 // 2.7 kHz confirmation chirp
#define KEYFOB_BUZZER_FREQ_ALARM    4000 // 4.0 kHz high-penetration alarm sweep

// WS2812B-2020 Smart RGB Status LED (Pad L1, Single-Wire NRZ Bitstream)
#define KEYFOB_PIN_LED_DATA         4   // P0.04
#define KEYFOB_PAD_LED_DATA         "L1"

// -----------------------------------------------------------------------------
// 5. Semtech SX1262 LoRa 868.5 MHz Transceiver Interface
// -----------------------------------------------------------------------------
#define KEYFOB_PIN_LORA_SCK         26  // P0.26 (Pad C1)
#define KEYFOB_PAD_LORA_SCK         "C1"
#define KEYFOB_PIN_LORA_NSS         29  // P0.29 (Pad R1)
#define KEYFOB_PAD_LORA_NSS         "R1"
#define KEYFOB_PIN_LORA_MOSI        30  // P0.30 (Pad T2)
#define KEYFOB_PAD_LORA_MOSI        "T2"
#define KEYFOB_PIN_LORA_MISO        31  // P0.31 (Pad U1)
#define KEYFOB_PAD_LORA_MISO        "U1"
#define KEYFOB_PIN_LORA_BUSY        41  // P1.09 (Pad W1)
#define KEYFOB_PAD_LORA_BUSY        "W1"
#define KEYFOB_PIN_LORA_DIO1        27  // P0.27 (Pad D2)
#define KEYFOB_PAD_LORA_DIO1        "D2"
#define KEYFOB_PIN_LORA_RESET       24  // P0.24 (Pad Y2)
#define KEYFOB_PAD_LORA_RESET       "Y2"

// LoRa RF Parameters
#define KEYFOB_LORA_FREQ_HZ         868500000 // 868.5 MHz EU Channel 3
#define KEYFOB_LORA_BANDWIDTH_KHZ   125
#define KEYFOB_LORA_SPREADING_FACTOR 7        // SF7 for fast < 25 ms transmission
#define KEYFOB_LORA_CODING_RATE     5        // 4/5
#define KEYFOB_LORA_TX_POWER_DBM    14       // +14 dBm (25 mW legal ERP)
#define KEYFOB_LORA_SYNC_WORD       0x1424   // OpenMotorBridge Network Sync Word

// -----------------------------------------------------------------------------
// 6. SWD Debug & Crystals
// -----------------------------------------------------------------------------
#define KEYFOB_PIN_SWDCLK           "H2"
#define KEYFOB_PIN_SWDIO            "AC24"
#define KEYFOB_PIN_XTAL1            "A12"
#define KEYFOB_PIN_XTAL2            "A14"
#define KEYFOB_PIN_RTC1             "F23"
#define KEYFOB_PIN_RTC2             "H23"
#define KEYFOB_PIN_BLE_ANT          "A8"

// -----------------------------------------------------------------------------
// 7. Security & Key Exchange Parameters
// -----------------------------------------------------------------------------
#define KEYFOB_BLE_DEVICE_NAME      "OMB-KEYFOB"
#define KEYFOB_DISCOVERY_TIMEOUT_S  60
#define KEYFOB_KEEP_ALIVE_INTERVAL_S 15
