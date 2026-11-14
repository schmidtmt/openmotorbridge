#pragma once

#include <stdint.h>
#include "driver/gpio.h"

// =============================================================================
// OpenMotorBridge - PCBA 09 / PCBA 10 v10.0 Unified OMM Tri-Band Intercom
// KiCad Source: hardware/kicad_omm446_intercom/openmotorbridge_omm446_intercom.kicad_pcb
// Target: U1 ESP32-C6-MINI-1U + U3 SA818-DMR + U6 ESP32-PICO-V3-02 + U2 ES8388
// =============================================================================
#define OMM_HW_REV_MAJOR        10
#define OMM_HW_REV_MINOR        0
#define OMM_FW_VERSION_STRING   "v10.0.0-triband"

// 1. I2S Audio Bus (U2 Everest Semi ES8388 Stereo Codec, Pad 21..25)
#define OMM_PIN_I2S_MCLK        GPIO_NUM_19  // U1 Pad 21 -> ES8388 MCLK (12.288 MHz)
#define OMM_PIN_I2S_BCLK        GPIO_NUM_20  // U1 Pad 22 -> ES8388 BCLK
#define OMM_PIN_I2S_WS          GPIO_NUM_21  // U1 Pad 23 -> ES8388 LRCK / WS (48 kHz)
#define OMM_PIN_I2S_DOUT        GPIO_NUM_22  // U1 Pad 24 -> ES8388 DAC (J_HELMET Pin 1/2 HP_OUT_L/R)
#define OMM_PIN_I2S_DIN         GPIO_NUM_23  // U1 Pad 25 <- ES8388 ADC (J_HELMET Pin 4 MIC_IN+ & SA818 AF)

#define OMM_AUDIO_SAMPLE_RATE   48000
#define OMM_AUDIO_BITS          16
#define OMM_AUDIO_CHANNELS      2            // Stereo Headphone Out
#define OMM_AUDIO_FRAME_MS      10           // 10 ms TDMA frame size (480 samples)
#define OMM_AUDIO_FRAME_SAMPLES (OMM_AUDIO_SAMPLE_RATE * OMM_AUDIO_FRAME_MS / 1000)

// 2. I2C Codec Control Bus (U2 ES8388, Pad 10/11)
#define OMM_PIN_I2C_SDA         GPIO_NUM_8   // U1 Pad 10 -> ES8388 SDA
#define OMM_PIN_I2C_SCL         GPIO_NUM_9   // U1 Pad 11 -> ES8388 SCL
#define OMM_I2C_PORT            I2C_NUM_0
#define OMM_I2C_FREQ_HZ         400000
#define ES8388_I2C_ADDR         0x10         // AD0 = 0 (GND) -> 0x10
#define ES8311_I2C_ADDR         0x18         // Legacy fallback

// 3. Tactile Pushbuttons & J_HELMET Pin 6 PTT (Low Active, Internal Pull-Up)
#define OMM_PIN_SW_POWER        GPIO_NUM_2   // U1 Pad 8: SW1 (BTN_1 PTT / MFB & J_HELMET Pin 6 BTN_PTT)
#define OMM_PIN_SW_MESH         GPIO_NUM_3   // U1 Pad 9: SW2 (BTN_2 Tri-Band Mode: 2.4G / PMR / DMR / Combi)
#define OMM_PIN_SW_VOL_UP       GPIO_NUM_4   // U1 Pad 4: SW3 (BTN_3 Vol+ / Channel+)
#define OMM_PIN_SW_VOL_DOWN     GPIO_NUM_5   // U1 Pad 5: SW4 (BTN_4 Vol- / Channel-)

// 4. Status Indicator LED (D1 WS2812B-2020, Pad 6)
#define OMM_PIN_WS2812B         GPIO_NUM_6   // U1 Pad 6 -> D1 WS2812B-2020
#define OMM_LED_COUNT           1

// 5. Battery & PMIC Supervision (U5 TI BQ24075RGTR + BAT1 1000mAh LiPo, Pad 7)
#define OMM_PIN_CHG_STAT        GPIO_NUM_7   // U1 Pad 7 <- BQ24075 /STAT (Low active when charging)
#define OMM_ADC_BAT_CHANNEL     ADC_CHANNEL_0 // GPIO 0 (ADC1_CH0) for Vbat divider

// 6. Native USB 2.0 PHY (J1 IP67 USB-C: Digital USB-Audio in Pod PCBA 03 & Central Bus-DFU, Pad 14/15)
#define OMM_PIN_USB_DN          GPIO_NUM_12  // U1 Pad 14 -> J1 USB_DN (via D2 USBLC6-2SC6)
#define OMM_PIN_USB_DP          GPIO_NUM_13  // U1 Pad 15 -> J1 USB_DP (via D2 USBLC6-2SC6)

// 7. NiceRF SA818-DMR 446 MHz PMR/DMR Transceiver (U3, Pad 16..20 - auto-detected at boot)
#define OMM_PIN_SA818_TXD       GPIO_NUM_14  // U1 Pad 16 -> U3 SA818 RXD (AT Commands @ 9600 Bd)
#define OMM_PIN_SA818_RXD       GPIO_NUM_15  // U1 Pad 17 <- U3 SA818 TXD (Status/Telemetry)
#define OMM_PIN_SA818_PTT       GPIO_NUM_16  // U1 Pad 18 -> U3 SA818 PTT (Low = TX, High = RX)
#define OMM_PIN_SA818_SQL       GPIO_NUM_17  // U1 Pad 19 <- U3 SA818 SQL (Low = Carrier detected)
#define OMM_PIN_SA818_PWR_HL    GPIO_NUM_18  // U1 Pad 20 -> U3 SA818 H/L (0 = 0.2W Helmet, 1 = 0.5W Bike Pod)

// 8. 2.4 GHz Mesh RF Parameters (U1 ESP32-C6 U.FL -> SMA_24G)
#define OMM_MESH_DEFAULT_CHAN   1            // 2412 MHz (Channel 1)
#define OMM_MESH_MAX_PEERS      16           // Maximum convoy nodes
#define OMM_MESH_PTT_TIMEOUT_MS 30000        // 30 s max continuous transmit (stuck-mic watchdog)

// 9. Bluetooth Classic / Bridge Co-Processor Link (U6 ESP32-PICO-V3-02 + ANT1, Pad 12,13,26..29)
#define OMM_PIN_BT_UART_TX      GPIO_NUM_24  // U1 Pad 26 -> U6 PICO RX
#define OMM_PIN_BT_UART_RX      GPIO_NUM_25  // U1 Pad 27 <- U6 PICO TX
#define OMM_PIN_BT_UART_RTS     GPIO_NUM_26  // U1 Pad 28 -> U6 PICO CTS
#define OMM_PIN_BT_UART_CTS     GPIO_NUM_27  // U1 Pad 29 <- U6 PICO RTS
#define OMM_PIN_BT_RESET        GPIO_NUM_1   // U1 Pad 13 -> U6 PICO EN
#define OMM_PIN_BT_BOOT         GPIO_NUM_0   // U1 Pad 12 -> U6 PICO IO0
#define OMM_BT_UART_BAUD        3000000      // 3 Mbps high-speed serial link
