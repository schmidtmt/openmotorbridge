#pragma once

#include "driver/gpio.h"
#include "driver/spi_master.h"
#include "driver/i2c.h"
#include "driver/uart.h"

// =============================================================================
// OpenMotorBridge v10.0 - Central Box (PCBA 01) Ground-Truth Hardware Pinout
// Extracted 1:1 from hardware/kicad_main_box/openmotorbridge_main.kicad_pcb
// Core MCU: U2 ESP32-S31-WROOM-1U (Dual-Core 320 MHz RISC-V / SIMD AI, 16MB/8MB)
// =============================================================================

#define MAIN_BOX_HW_REV_MAJOR           10
#define MAIN_BOX_HW_REV_MINOR           0
#define MAIN_BOX_MCU_MODEL_NAME         "ESP32-S31-WROOM-1U"

// -----------------------------------------------------------------------------
// 1. Native USB 2.0 High-Speed / Full-Speed Interface -> U8 (USB2517I-JZX Port 1)
// Upstream of U8 is J3 (Single External USB-C Service & DFU Port for Entire Bike)
// -----------------------------------------------------------------------------
#define PIN_MAIN_USB_DM                 GPIO_NUM_19  // U2 Pad 13 -> U8 Pin 16 (ESP_USB_DM)
#define PIN_MAIN_USB_DP                 GPIO_NUM_20  // U2 Pad 14 -> U8 Pin 17 (ESP_USB_DP)

// -----------------------------------------------------------------------------
// 2. Ignition Sense (KL15), Pairing Button (SW1) & Status RGB LED (D1 / J4)
// -----------------------------------------------------------------------------
#define PIN_MAIN_KL15_SENSE             GPIO_NUM_3   // U2 Pad 5 (GPIO3) -> R3/D4/Q1 Ignition Sense (KL15_SENSE)
#define PIN_MAIN_BOOT_PAIR_BTN          GPIO_NUM_0   // U2 Pad 27 -> SW1 Pairing / Boot Button (ESP_BOOT)
#define PIN_MAIN_RGB_LED_DATA           GPIO_NUM_48  // U2 Pad 28 -> D1 & J4 WS2812B-2020 (RGB_LED_DATA)

// -----------------------------------------------------------------------------
// 3. UPS LiPo Charger (U4 BQ24075RGTR), 10k NTC Guard (J5) & Dual-Power (D3 LM66100)
// -----------------------------------------------------------------------------
#define PIN_MAIN_BAT_SENSE_ADC          GPIO_NUM_1   // U2 Pad 31 -> R12/R13 Voltage Divider (BAT_SENSE)
#define PIN_MAIN_BAT_NTC_ADC            GPIO_NUM_15  // U2 Pad 25 -> J5 Pin 3 10k NTC Thermistor (BAT_NTC)
// JEITA LiPo Temperature Limits: Charge allowed only between 0.0 °C and +45.0 °C
#define MAIN_LIPO_JEITA_MIN_TEMP_C      0.0f
#define MAIN_LIPO_JEITA_MAX_TEMP_C      45.0f

// -----------------------------------------------------------------------------
// 4. Shared Internal I2C Bus (U3 ES8388 Codec, U5 Bosch BMI270 IMU)
// -----------------------------------------------------------------------------
#define MAIN_I2C_PORT                   I2C_NUM_0
#define PIN_MAIN_I2C_SDA                GPIO_NUM_22  // U2 Pad 17 (GPIO22) -> U3 Pin 28, U5 Pin 13 (I2C_SDA)
#define PIN_MAIN_I2C_SCL                GPIO_NUM_23  // U2 Pad 18 (GPIO23) -> U3 Pin 27, U5 Pin 12 (I2C_SCL)
#define I2C_ADDR_ES8388_CODEC           0x10         // U3 Everest ES8388 24-Bit Audio Codec
#define I2C_ADDR_BMI270_IMU             0x68         // U5 Bosch BMI270 6-Axis IMU + Hardware Step/Shock Interrupt

// -----------------------------------------------------------------------------
// 5. Master TDM / I2S Audio Bus (Shared by U3 ES8388 & Triple Qualcomm QCC3086)
// -----------------------------------------------------------------------------
#define PIN_MAIN_I2S_MCLK               GPIO_NUM_35  // U2 Pad 12 (GPIO35) -> U3 Pin 1 / QCC3086 Pin 1 (I2S_MCLK)
#define PIN_MAIN_I2S_BCLK               GPIO_NUM_16  // U2 Pad 30 -> U3 Pin 2 / QCC3086 Pin 2 (I2S_BCLK)
#define PIN_MAIN_I2S_WS                 GPIO_NUM_47  // U2 Pad 32 -> U3 Pin 3 / QCC3086 Pin 3 (I2S_WS)
#define PIN_MAIN_I2S_DOUT               GPIO_NUM_17  // U2 Pad 15 -> U3 Pin 4 / QCC3086 Pin 4 (I2S_DOUT)
#define PIN_MAIN_I2S_DIN                GPIO_NUM_18  // U2 Pad 16 -> U3 Pin 5 / QCC3086 Pin 5 (I2S_DIN)

// -----------------------------------------------------------------------------
// 6. Qualcomm QCC3086 Bluetooth 5.4 Triple-SoC Hub (PCBA 01)
// - U9: Smartphone Link (A2DP Sink, HFP 1.8 voice return < 20ms, AVRCP 1.6)
// - U13: Rider Helmet Link (A2DP Source, aptX Adaptive, HFP 1.8 voice mic)
// - U14: Pillion Helmet Link (A2DP Source, aptX / LC3, HFP 1.8 voice mic)
// RF Output: Taoglas BT Helmaudio Lid dipole via dedicated coaxial connection.
// -----------------------------------------------------------------------------
#define QCC3086_UART_PORT               UART_NUM_1
#define QCC3084_UART_PORT               QCC3086_UART_PORT
#define PIN_MAIN_BT_EN                  GPIO_NUM_1   // U2 Pad 9  -> QCC3086 Pin 11 (BT_EN)
#define PIN_MAIN_BT_UART_RX             GPIO_NUM_2   // U2 Pad 10 -> QCC3086 Pin 10 (BT_UART_RX)
#define PIN_MAIN_BT_UART_TX             GPIO_NUM_3   // U2 Pad 11 -> QCC3086 Pin 9  (BT_UART_TX)

// -----------------------------------------------------------------------------
// 7. Onboard Semtech SX1262IMLTRT 868 MHz LoRa Transceiver (U10, +22 dBm)
// Powered directly from UPS rail for 24/7 Theft Sentry & Convoy Split Rescue
// RF Output: Dedicated U.FL Coaxial Receptacle ANT1 (Taoglas_FXP895_868MHz_Lid)
// at KiCad (X=176.03, Y=74.75) routed to external lid 868MHz dipole.
// -----------------------------------------------------------------------------
#define MAIN_LORA_SPI_HOST              SPI2_HOST
#define PIN_MAIN_LORA_SCK               GPIO_NUM_2   // U2 Pad 4 (GPIO2) -> U10 Pin 20 (SPI_SCK)
#define PIN_MAIN_LORA_MISO              GPIO_NUM_4   // U2 Pad 6 (GPIO4) -> U10 Pin 18 (SPI_MISO)
#define PIN_MAIN_LORA_MOSI              GPIO_NUM_5   // U2 Pad 7 (GPIO5) -> U10 Pin 19 (SPI_MOSI)
#define PIN_MAIN_LORA_NSS               GPIO_NUM_10  // U2 Pad 24 -> U10 Pin 21 (LORA_NSS)
#define PIN_MAIN_LORA_RST               GPIO_NUM_7   // U2 Pad 23 -> U10 Pin 1  (LORA_RST)
#define PIN_MAIN_LORA_BUSY              GPIO_NUM_21  // U2 Pad 20 -> U10 Pin 14 (LORA_BUSY)
#define PIN_MAIN_LORA_DIO1              GPIO_NUM_14  // U2 Pad 19 -> U10 Pin 15 (LORA_DIO1)

// -----------------------------------------------------------------------------
// 7b. On-Board 2.4 GHz BLE Control Antenna (ANT3 Johanson 2450AT18D0100)
// Dedicated SMD ceramic chip antenna (3.2 x 1.6 mm) on left board edge
// at KiCad (X=117.80, Y=88.25, rot=180 deg) with feed pad facing inward.
// Driven directly from U2 ESP32-S31-WROOM-1U Pin 63 (BLE_RF_2G4).
// Handles vehicle control: Pods, Action Cam, TPMS & Smart Keyfob proximity.
// Separated by >65 mm from ANT1 (LoRa) and ANT2 (Helmaudio) to prevent desense.
// -----------------------------------------------------------------------------
#define MAIN_BLE_ANTENNA_TYPE           "Johanson_2450AT18D0100_Ceramic_SMD"
#define MAIN_BLE_RF_PIN_U2_PAD          63           // ESP32-S31 Pad 63 (BLE_RF_2G4)

// -----------------------------------------------------------------------------
// 8. Automotive CAN-FD Transceiver (U6 TI TCAN334GDCNT -> J1 Pin 3/4)
// -----------------------------------------------------------------------------
#define PIN_MAIN_CAN_TX                 GPIO_NUM_26  // U2 Pad 21 (GPIO 26) -> U6 Pin 1 (CAN_TX)
#define PIN_MAIN_CAN_RX                 GPIO_NUM_27  // U2 Pad 22 (GPIO 27) -> U6 Pin 4 (CAN_RX)

// -----------------------------------------------------------------------------
// 9. High-Speed 4-Bit SDIO MicroSD Blackbox Slot (J2 Hirose DM3D-SF)
// -----------------------------------------------------------------------------
#define PIN_MAIN_SD_DAT1                GPIO_NUM_33  // U2 Pad 33 -> J2 Pin 8 (SD_DAT1)
#define PIN_MAIN_SD_DAT2                GPIO_NUM_34  // U2 Pad 34 -> J2 Pin 1 (SD_DAT2)
#define PIN_MAIN_SD_CLK                 GPIO_NUM_55  // U2 Pad 35 (GPIO55) -> J2 Pin 5 (SD_CLK)
#define PIN_MAIN_SD_CMD                 GPIO_NUM_36  // U2 Pad 36 -> J2 Pin 3 (SD_CMD)
#define PIN_MAIN_SD_DAT0                GPIO_NUM_37  // U2 Pad 37 -> J2 Pin 7 (SD_DAT0)
#define PIN_MAIN_SD_DAT3                GPIO_NUM_38  // U2 Pad 38 -> J2 Pin 2 (SD_DAT3)
#define PIN_MAIN_SD_CD                  GPIO_NUM_39  // U2 Pad 39 -> J2 Pin 9 (SD_CD Card Detect)

// -----------------------------------------------------------------------------
// 10. ESP32-PICO-V3-02 Classic A2DP Music Sharing Transmitter (U13)
// Dedicated A2DP transmitter feeding Pod OEM Intercoms (Sena/Cardo) for Mesh sharing.
// Driven via I2S DOUT/BCLK/WS, controlled via UART and HW Enable / Boot strapping.
// RF Output: Dedicated SMD Ceramic Chip Antenna ANT4 (Johanson 2450AT18x100) at South edge.
// -----------------------------------------------------------------------------
#define A2DP_PICO_UART_PORT             UART_NUM_2
#define PIN_MAIN_A2DP_UART_TX           GPIO_NUM_33  // U2 Pad 13 (GPIO33) -> U13 Pin 41 (A2DP_UART_TX)
#define PIN_MAIN_A2DP_UART_RX           GPIO_NUM_34  // U2 Pad 14 (GPIO34) -> U13 Pin 40 (A2DP_UART_RX)
#define PIN_MAIN_A2DP_EN                GPIO_NUM_43  // U2 Pad 8  (GPIO43) -> U13 Pin 9  (A2DP_EN)
#define PIN_MAIN_A2DP_BOOT              GPIO_NUM_44  // U2 Pad 29 (GPIO44) -> U13 Pin 23 (A2DP_BOOT)

// -----------------------------------------------------------------------------
// 10. Quad Automotive High-Side Switch Smart Power Distribution (U12 TI TPS4H160-Q1 -> J6)
// Current Limits & Channels:
//   - Branch 1 (VBUS_FRONT): 5.0 A (PCBA 05 + 30W USB-PD SW3526 + Ottocast)
//   - Branch 2 (VBUS_POD1):  2.5 A (PCBA 03 Pod 1 + Intercom / OMM)
//   - Branch 3 (VBUS_POD2):  2.5 A (PCBA 03 Pod 2 + Intercom / OMM)
//   - Branch 4 (VBUS_RADAR): 1.5 A (PCBA 08 MR20 77GHz Radar + 36x WS2812B + 5GHz V2X)
// -----------------------------------------------------------------------------
#define SWITCH_LIMIT_BRANCH1_FRONT_MA   5000
#define SWITCH_LIMIT_BRANCH2_POD1_MA    2500
#define SWITCH_LIMIT_BRANCH3_POD2_MA    2500
#define SWITCH_LIMIT_BRANCH4_RADAR_MA   1500
// Legacy aliases
#define EFUSE_LIMIT_BRANCH1_FRONT_MA    SWITCH_LIMIT_BRANCH1_FRONT_MA
#define EFUSE_LIMIT_BRANCH2_POD1_MA     SWITCH_LIMIT_BRANCH2_POD1_MA
#define EFUSE_LIMIT_BRANCH3_POD2_MA     SWITCH_LIMIT_BRANCH3_POD2_MA
#define EFUSE_LIMIT_BRANCH4_RADAR_MA    SWITCH_LIMIT_BRANCH4_RADAR_MA

