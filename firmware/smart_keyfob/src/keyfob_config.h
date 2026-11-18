#pragma once

#include <stdint.h>
#include <stdbool.h>

// =============================================================================
// OpenMotorBridge - PCBA 07 2-in-1 LoRa Smart-Keyfob & Silent Pager
// Target: Nordic Semiconductor nRF52832-QFxx (QFN-48) @ 64 MHz ARM Cortex-M4F
// =============================================================================

// -----------------------------------------------------------------------------
// 1. Tactile Pushbuttons (Active LOW, 10k External Pull-Ups R1 & R2)
// -----------------------------------------------------------------------------
// SW1: Arm / Disarm Bike Alarm (Pin 23 / P0.20)
#define KEYFOB_PIN_BTN_ARM_N        20  // P0.20 (Pin 23)
#define KEYFOB_PAD_BTN_ARM_N        "23"

// SW2: SOS Panic Alert / Handlebar Shutter (Pin 27 / P0.22)
#define KEYFOB_PIN_BTN_SOS_N        22  // P0.22 (Pin 27)
#define KEYFOB_PAD_BTN_SOS_N        "27"

// -----------------------------------------------------------------------------
// 2. Battery & Qi Wireless Charger Supervision (TI BQ51003 & BQ25100)
// -----------------------------------------------------------------------------
// BQ25100 Charge Status Output (Pin 22 / P0.19, Low Active: 0 = Charging, 1 = Standby/Full)
#define KEYFOB_PIN_CHG_STAT         19  // P0.19 (Pin 22)
#define KEYFOB_PAD_CHG_STAT         "22"

// Analog Battery Voltage Sensing (Internal VDD SAADC channel)
#define KEYFOB_ADC_VBAT_PIN         30  // SAADC internal VDD channel
#define KEYFOB_BAT_LOW_THRESH_MV    3400 // 3.4V Low Battery Cut-Off / Alert
#define KEYFOB_BAT_FULL_THRESH_MV   4200 // 4.2V Full LiPo Charge

// -----------------------------------------------------------------------------
// 3. User Feedback: TI DRV2605L Haptics & LRA Linear Resonant Actuator
// -----------------------------------------------------------------------------
// DRV2605L Hardware Enable (Pin 40 / P0.28, Active HIGH)
#define KEYFOB_PIN_DRV_EN           28  // P0.28 (Pin 40)
#define KEYFOB_PAD_DRV_EN           "40"

// I2C Interface to DRV2605L (Pin 41 / P0.29 = SDA, Pin 42 / P0.30 = SCL)
#define KEYFOB_PIN_I2C_SDA          29  // P0.29 (Pin 41)
#define KEYFOB_PAD_I2C_SDA          "41"
#define KEYFOB_PIN_I2C_SCL          30  // P0.30 (Pin 42)
#define KEYFOB_PAD_I2C_SCL          "42"
#define KEYFOB_DRV2605_I2C_ADDR     0x5A

// -----------------------------------------------------------------------------
// 4. User Feedback: Piezo Buzzer & WS2812B Smart RGB LED
// -----------------------------------------------------------------------------
// Murata CPT-9019S SMD Piezo Buzzer (Pin 29 / P0.24, PWM Tone Generator)
#define KEYFOB_PIN_BUZZER_PWM       24  // P0.24 (Pin 29)
#define KEYFOB_PAD_BUZZER_PWM       "29"
#define KEYFOB_BUZZER_FREQ_ARM      2700 // 2.7 kHz confirmation chirp
#define KEYFOB_BUZZER_FREQ_ALARM    4000 // 4.0 kHz high-penetration alarm sweep

// WS2812B-2020 Smart RGB Status LED (Pin 28 / P0.23, Single-Wire NRZ Bitstream)
#define KEYFOB_PIN_LED_DATA         23  // P0.23 (Pin 28)
#define KEYFOB_PAD_LED_DATA         "28"

// -----------------------------------------------------------------------------
// 5. Semtech SX1262 LoRa 868.5 MHz Transceiver Interface
// -----------------------------------------------------------------------------
#define KEYFOB_PIN_LORA_SCK         2   // P0.02 (Pin 4)
#define KEYFOB_PAD_LORA_SCK         "4"
#define KEYFOB_PIN_LORA_MOSI        3   // P0.03 (Pin 5)
#define KEYFOB_PAD_LORA_MOSI        "5"
#define KEYFOB_PIN_LORA_MISO        4   // P0.04 (Pin 6)
#define KEYFOB_PAD_LORA_MISO        "6"
#define KEYFOB_PIN_LORA_NSS         5   // P0.05 (Pin 7)
#define KEYFOB_PAD_LORA_NSS         "7"
#define KEYFOB_PIN_LORA_DIO1        6   // P0.06 (Pin 8)
#define KEYFOB_PAD_LORA_DIO1        "8"
#define KEYFOB_PIN_LORA_BUSY        7   // P0.07 (Pin 9)
#define KEYFOB_PAD_LORA_BUSY        "9"
#define KEYFOB_PIN_LORA_RESET       8   // P0.08 (Pin 10)
#define KEYFOB_PAD_LORA_RESET       "10"

// LoRa RF Parameters
#define KEYFOB_LORA_FREQ_HZ         868500000 // 868.5 MHz EU Channel 3
#define KEYFOB_LORA_BANDWIDTH_KHZ   125
#define KEYFOB_LORA_SPREADING_FACTOR 7        // SF7 for fast < 25 ms transmission
#define KEYFOB_LORA_CODING_RATE     5        // 4/5
#define KEYFOB_LORA_TX_POWER_DBM    14       // +14 dBm (25 mW legal ERP)
#define KEYFOB_LORA_SYNC_WORD       0x1424   // OpenMotorBridge Network Sync Word

// -----------------------------------------------------------------------------
// 6. SWD Debug, Crystals & RF
// -----------------------------------------------------------------------------
#define KEYFOB_PIN_SWDCLK           "25"
#define KEYFOB_PIN_SWDIO            "26"
#define KEYFOB_PIN_BLE_ANT          "30"
#define KEYFOB_PIN_XTAL1            "34"
#define KEYFOB_PIN_XTAL2            "35"
#define KEYFOB_PIN_RTC1             "2"
#define KEYFOB_PIN_RTC2             "3"

// -----------------------------------------------------------------------------
// 7. Security & Key Exchange Parameters
// -----------------------------------------------------------------------------
#define KEYFOB_BLE_DEVICE_NAME      "OMB-KEYFOB"
#define KEYFOB_DISCOVERY_TIMEOUT_S  60
#define KEYFOB_KEEP_ALIVE_INTERVAL_S 15
