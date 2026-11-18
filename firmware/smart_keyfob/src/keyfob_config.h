#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "driver/gpio.h"

// =============================================================================
// OpenMotorBridge - PCBA 07 2-in-1 LoRa Smart-Keyfob & Acoustic Pager
// Target: Espressif ESP32-C3FH4 (QFN-32 5x5mm) @ 160 MHz 32-Bit RISC-V
// =============================================================================

// -----------------------------------------------------------------------------
// 1. Tactile Pushbuttons (Active LOW, 10k External Pull-Ups R1 & R2)
// -----------------------------------------------------------------------------
// SW1: Arm / Disarm Bike Alarm (GPIO 9, QFN-32 Pad 15, Strapping Boot Pin)
#define KEYFOB_PIN_BTN_ARM_N        GPIO_NUM_9
#define KEYFOB_PAD_BTN_ARM_N        "15"

// SW2: SOS Panic Alert / Alarm Beacon (GPIO 10, QFN-32 Pad 16)
#define KEYFOB_PIN_BTN_SOS_N        GPIO_NUM_10
#define KEYFOB_PAD_BTN_SOS_N        "16"

// -----------------------------------------------------------------------------
// 2. Battery & Qi Wireless Charger Supervision (TI BQ51050BRHLR Direct LiPo)
// -----------------------------------------------------------------------------
// BQ51050B Charge Status (GPIO 21, QFN-32 Pad 28, Active LOW: 0 = Charging, 1 = Standby/Full)
#define KEYFOB_PIN_CHG_STAT         GPIO_NUM_21
#define KEYFOB_PAD_CHG_STAT         "28"

// Analog Battery Voltage Sensing (GPIO 0, QFN-32 Pad 4, ADC1 Channel 0, 100k/100k Divider)
#define KEYFOB_PIN_BAT_SENSE        GPIO_NUM_0
#define KEYFOB_ADC1_CHANNEL_VBAT    ADC_CHANNEL_0
#define KEYFOB_PAD_BAT_SENSE        "4"
#define KEYFOB_BAT_LOW_THRESH_MV    3400 // 3.4V Low Battery Cut-Off / Alert
#define KEYFOB_BAT_FULL_THRESH_MV   4200 // 4.2V Full LiPo Charge

// -----------------------------------------------------------------------------
// 3. User Feedback: CUI Devices CPT-9019S-SMT 9mm Piezo Buzzer (LS1)
// -----------------------------------------------------------------------------
// Driven via ESP-IDF LEDC PWM peripheral (GPIO 20, QFN-32 Pad 27)
#define KEYFOB_PIN_BUZZER_PWM       GPIO_NUM_20
#define KEYFOB_PAD_BUZZER_PWM       "27"
#define KEYFOB_BUZZER_FREQ_ARM      2700 // 2.7 kHz confirmation chirp
#define KEYFOB_BUZZER_FREQ_DISARM   2400 // 2.4 kHz gentle disarm chirp
#define KEYFOB_BUZZER_FREQ_ALARM    4000 // 4.0 kHz high-penetration alarm sweep

// -----------------------------------------------------------------------------
// 4. User Feedback: WS2812B-2020 Smart RGB Status LED (D1)
// -----------------------------------------------------------------------------
// Single-wire bitstream via RMT / LED Strip driver (GPIO 8, QFN-32 Pad 14)
#define KEYFOB_PIN_LED_DATA         GPIO_NUM_8
#define KEYFOB_PAD_LED_DATA         "14"

// -----------------------------------------------------------------------------
// 5. Semtech SX1262 LoRa 868.5 MHz Transceiver Interface (SPI2 / FSPI)
// -----------------------------------------------------------------------------
#define KEYFOB_PIN_LORA_SCK         GPIO_NUM_4  // FSPIHD (Pad 9)
#define KEYFOB_PAD_LORA_SCK         "9"
#define KEYFOB_PIN_LORA_MOSI        GPIO_NUM_3  // FSPID (Pad 8)
#define KEYFOB_PAD_LORA_MOSI        "8"
#define KEYFOB_PIN_LORA_MISO        GPIO_NUM_2  // FSPIQ (Pad 6)
#define KEYFOB_PAD_LORA_MISO        "6"
#define KEYFOB_PIN_LORA_NSS         GPIO_NUM_5  // FSPIWP (Pad 10, Active-LOW)
#define KEYFOB_PAD_LORA_NSS         "10"
#define KEYFOB_PIN_LORA_DIO1        GPIO_NUM_1  // IRQ Interrupt (Pad 5)
#define KEYFOB_PAD_LORA_DIO1        "5"
#define KEYFOB_PIN_LORA_BUSY        GPIO_NUM_6  // Busy Status (Pad 12)
#define KEYFOB_PAD_LORA_BUSY        "12"
#define KEYFOB_PIN_LORA_RESET       GPIO_NUM_7  // Hardware Reset (Pad 13)
#define KEYFOB_PAD_LORA_RESET       "13"

// LoRa RF Parameters
#define KEYFOB_LORA_FREQ_HZ         868500000 // 868.5 MHz EU Channel 3
#define KEYFOB_LORA_BANDWIDTH_KHZ   125
#define KEYFOB_LORA_SPREADING_FACTOR 7        // SF7 for fast < 25 ms transmission
#define KEYFOB_LORA_CODING_RATE     5        // 4/5
#define KEYFOB_LORA_TX_POWER_DBM    14       // +14 dBm (25 mW legal ERP)
#define KEYFOB_LORA_SYNC_WORD       0x1424   // OpenMotorBridge Network Sync Word

// -----------------------------------------------------------------------------
// 6. Native USB CDC / JTAG Telemetry Port (J2 Header)
// -----------------------------------------------------------------------------
#define KEYFOB_PIN_USB_DM           GPIO_NUM_18 // Pad 25 (J2 Pin 2)
#define KEYFOB_PIN_USB_DP           GPIO_NUM_19 // Pad 26 (J2 Pin 3)
