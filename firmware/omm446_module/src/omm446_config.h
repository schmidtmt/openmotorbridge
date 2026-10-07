#pragma once

#include <stdint.h>
#include "driver/gpio.h"

// Hardware Configuration: PCBA 10 (OMM 446 MHz PMR/DMR Transceiver Module)
#define OMM446_HW_REV_MAJOR       1
#define OMM446_HW_REV_MINOR       0
#define OMM446_FW_VERSION_STRING  "v1.0.0-release"

// ---------------------------------------------------------------------------
// 1. Tactile Pushbuttons (Low Active, Internal Pull-Up 45k)
// ---------------------------------------------------------------------------
#define OMM446_PIN_SW_PTT         GPIO_NUM_2  // SW1: Push-To-Talk / MFB
#define OMM446_PIN_SW_MODE        GPIO_NUM_3  // SW2: Mode Toggle (Analog FM <-> DMR)
#define OMM446_PIN_SW_CH_UP       GPIO_NUM_4  // SW3: Channel Selection UP (1..16)
#define OMM446_PIN_SW_CH_DOWN     GPIO_NUM_5  // SW4: Channel Selection DOWN (16..1)

// ---------------------------------------------------------------------------
// 2. Status Indicator LED (WS2812B-2020)
// ---------------------------------------------------------------------------
#define OMM446_PIN_WS2812B        GPIO_NUM_6
#define OMM446_LED_COUNT          1

// ---------------------------------------------------------------------------
// 3. Battery & PMIC Supervision (TI BQ24075)
// ---------------------------------------------------------------------------
#define OMM446_PIN_CHG_STAT       GPIO_NUM_7  // Low active when charging
#define OMM446_ADC_BAT_CHANNEL    ADC_CHANNEL_0 // GPIO 0 (ADC1_CH0) for Vbat sensing

// ---------------------------------------------------------------------------
// 4. I2C Codec Control Bus (Everest Semi ES8388)
// ---------------------------------------------------------------------------
#define OMM446_PIN_I2C_SDA        GPIO_NUM_8
#define OMM446_PIN_I2C_SCL        GPIO_NUM_9
#define OMM446_I2C_PORT           I2C_NUM_0
#define OMM446_I2C_FREQ_HZ        400000
#define ES8388_I2C_ADDR           0x10        // AD0 = 0 (GND) -> 0x10

// ---------------------------------------------------------------------------
// 5. USB 2.0 PHY (Native DFU & Serial)
// ---------------------------------------------------------------------------
#define OMM446_PIN_USB_DN         GPIO_NUM_12
#define OMM446_PIN_USB_DP         GPIO_NUM_13

// ---------------------------------------------------------------------------
// 6. NiceRF SA818-DMR Transceiver Control Interface
// ---------------------------------------------------------------------------
#define OMM446_PIN_SA818_TXD      GPIO_NUM_14 // ESP32 TXD -> SA818 RXD (AT Commands)
#define OMM446_PIN_SA818_RXD      GPIO_NUM_15 // SA818 TXD -> ESP32 RXD (Status/Telemetry)
#define OMM446_UART_PORT          UART_NUM_1
#define OMM446_UART_BAUDRATE      9600

#define OMM446_PIN_SA818_PTT      GPIO_NUM_16 // Low active: 0 = Transmit, 1 = Receive
#define OMM446_PIN_SA818_SQL      GPIO_NUM_17 // Squelch Output: 0 = Carrier detected, 1 = Muted
#define OMM446_PIN_SA818_PWR_HL   GPIO_NUM_18 // Power mode: 0 = 0.2W (Helmet), 1 = 0.5W (Bike)

// ---------------------------------------------------------------------------
// 7. I2S Audio Bus (Everest Semi ES8388 Stereo Codec)
// ---------------------------------------------------------------------------
#define OMM446_PIN_I2S_MCLK       GPIO_NUM_19 // 12.288 MHz Master Clock (256 * fs)
#define OMM446_PIN_I2S_BCLK       GPIO_NUM_20 // 1.536 MHz Bit Clock (32 * fs)
#define OMM446_PIN_I2S_WS         GPIO_NUM_21 // 48.0 kHz Word Select / Frame Sync
#define OMM446_PIN_I2S_DOUT       GPIO_NUM_22 // ESP32 -> ES8388 DAC (Audio output)
#define OMM446_PIN_I2S_DIN        GPIO_NUM_23 // ES8388 ADC -> ESP32 (Microphone input)

#define OMM446_AUDIO_SAMPLE_RATE  16000       // 16 kHz optimized for narrow-band PMR voice
#define OMM446_AUDIO_BITS         16
#define OMM446_AUDIO_CHANNELS     2
#define OMM446_AUDIO_FRAME_MS     10
#define OMM446_AUDIO_FRAME_SAMPLES (OMM446_AUDIO_SAMPLE_RATE * OMM446_AUDIO_FRAME_MS / 1000)

// ---------------------------------------------------------------------------
// 8. RF Parameters & Legal Limits (ETSI PMR446 & DMR Tier I)
// ---------------------------------------------------------------------------
#define OMM446_NUM_CHANNELS       16
#define OMM446_PTT_MAX_TIMEOUT_MS 60000       // 60 s stuck-mic watchdog

// 16 Standard PMR446 Frequencies (12.5 kHz Channel Spacing)
static const double OMM446_CHANNEL_FREQS[OMM446_NUM_CHANNELS] = {
    446.00625, // Ch 1
    446.01875, // Ch 2
    446.03125, // Ch 3
    446.04375, // Ch 4
    446.05625, // Ch 5
    446.06875, // Ch 6
    446.08125, // Ch 7
    446.09375, // Ch 8 (Standard Motorcycle / Mountain Safety Channel)
    446.10625, // Ch 9
    446.11875, // Ch 10
    446.13125, // Ch 11
    446.14375, // Ch 12
    446.15625, // Ch 13
    446.16875, // Ch 14
    446.18125, // Ch 15
    446.19375  // Ch 16
};

// Standard CTCSS Subtone Frequencies (Hz * 10)
static const uint16_t OMM446_CTCSS_TONES[39] = {
    0,     // 0 = Off
    670,   693,   719,   744,   770,   797,   825,   854,   885,   915,
    948,   974,   1000,  1035,  1072,  1109,  1148,  1188,  1230,  1273,
    1318,  1365,  1413,  1462,  1514,  1567,  1622,  1679,  1738,  1799,
    1862,  1928,  2035,  2107,  2181,  2257,  2336,  2418,  2503
};
