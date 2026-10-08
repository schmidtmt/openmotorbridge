#pragma once

#include <stdint.h>
#include "driver/gpio.h"

// Hardware Configuration: PCBA 09 (OMM 2.4 GHz UCS Intercom Module)
#define OMM_HW_REV_MAJOR       1
#define OMM_HW_REV_MINOR       0
#define OMM_FW_VERSION_STRING  "v1.0.0-release"

// 1. I2S Audio Bus (Everest Semi ES8388 Stereo Codec)
#define OMM_PIN_I2S_MCLK       GPIO_NUM_19
#define OMM_PIN_I2S_BCLK       GPIO_NUM_20
#define OMM_PIN_I2S_WS         GPIO_NUM_21
#define OMM_PIN_I2S_DOUT       GPIO_NUM_22 // ESP32 -> ES8388 DAC (Stereo Headphone L/R)
#define OMM_PIN_I2S_DIN        GPIO_NUM_23 // ES8388 ADC -> ESP32 (Microphone)

#define OMM_AUDIO_SAMPLE_RATE  48000
#define OMM_AUDIO_BITS         16
#define OMM_AUDIO_CHANNELS     2           // Stereo Headphone Out
#define OMM_AUDIO_FRAME_MS     10          // 10 ms TDMA frame size (480 samples)
#define OMM_AUDIO_FRAME_SAMPLES (OMM_AUDIO_SAMPLE_RATE * OMM_AUDIO_FRAME_MS / 1000)

// 2. I2C Codec Control Bus
#define OMM_PIN_I2C_SDA        GPIO_NUM_8
#define OMM_PIN_I2C_SCL        GPIO_NUM_9
#define OMM_I2C_PORT           I2C_NUM_0
#define OMM_I2C_FREQ_HZ        400000
#define ES8388_I2C_ADDR        0x10        // AD0 = 0 (GND) -> 0x10
#define ES8311_I2C_ADDR        0x18        // Legacy fallback

// 3. Tactile Pushbuttons (Low Active, Internal Pull-Up)
#define OMM_PIN_SW_POWER       GPIO_NUM_2  // SW1: Power / MFB
#define OMM_PIN_SW_MESH        GPIO_NUM_3  // SW2: Mesh / Group Mode
#define OMM_PIN_SW_VOL_UP      GPIO_NUM_4  // SW3: Volume +
#define OMM_PIN_SW_VOL_DOWN    GPIO_NUM_5  // SW4: Volume -

// 4. Status Indicator LED (WS2812B-2020)
#define OMM_PIN_WS2812B        GPIO_NUM_6
#define OMM_LED_COUNT          1

// 5. Battery & PMIC Supervision (TI BQ24075)
#define OMM_PIN_CHG_STAT       GPIO_NUM_7  // Low active when charging
#define OMM_ADC_BAT_CHANNEL    ADC_CHANNEL_0 // GPIO 0 (ADC1_CH0) for NTC / Vbat divider

// 6. 2.4 GHz Mesh RF Parameters
#define OMM_MESH_DEFAULT_CHAN  1           // 2412 MHz (Channel 1)
#define OMM_MESH_MAX_PEERS     16          // Maximum convoy nodes
#define OMM_MESH_PTT_TIMEOUT_MS 30000      // 30 s max continuous transmit (stuck-mic watchdog)

// 7. Bluetooth Co-Processor Link (ESP32-PICO-V3-02 Dual-Engine)
#define OMM_PIN_BT_UART_TX     GPIO_NUM_16 // C6 TX -> PICO RX
#define OMM_PIN_BT_UART_RX     GPIO_NUM_17 // C6 RX -> PICO TX
#define OMM_PIN_BT_UART_RTS    GPIO_NUM_15 // C6 RTS -> PICO CTS
#define OMM_PIN_BT_UART_CTS    GPIO_NUM_14 // C6 CTS -> PICO RTS
#define OMM_PIN_BT_RESET       GPIO_NUM_18 // Co-processor reset / wakeup
#define OMM_PIN_BT_BOOT        GPIO_NUM_1  // Co-processor download mode trigger
#define OMM_BT_UART_BAUD       3000000     // 3 Mbps high-speed serial link
