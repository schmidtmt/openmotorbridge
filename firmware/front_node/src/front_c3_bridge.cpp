#include "front_c3_bridge.h"
#include <string.h>
#include "esp_log.h"
#include "esp_timer.h"
#include "driver/gpio.h"
#include "driver/uart.h"
#include "driver/i2s_std.h"

static const char *TAG = "FRONT_C3_BRIDGE";

#define C3_UART_NUM            UART_NUM_1
#define C3_UART_BUF_SIZE       (1024)
#define INTERCHIP_MAGIC        0xA5

#pragma pack(push, 1)
typedef struct {
    uint8_t  magic;          // 0xA5
    uint8_t  pkt_type;
    uint8_t  payload_len;
    uint8_t  payload[32];
    uint16_t crc16;
} InterchipFrame;

typedef struct {
    bool     usb_enumerated;
    bool     whim_emulation_active;
    bool     carplay_active;
    bool     speakers_active;
    uint8_t  headunit_vol_pct;
    uint8_t  current_mux_target;
} C3PayloadState;
#pragma pack(pop)

static struct {
    FrontC3BridgeStatus_t status;
    FrontC3StatusCallback status_cb;
    i2s_chan_handle_t     tx_chan;
    bool                  initialized;
    uint64_t              last_rx_us;
} s_bridge = {0};

static uint16_t calculate_crc16(const uint8_t *data, size_t len) {
    uint16_t crc = 0xFFFF;
    for (size_t i = 0; i < len; i++) {
        crc ^= (uint16_t)data[i] << 8;
        for (int j = 0; j < 8; j++) {
            if (crc & 0x8000) crc = (crc << 1) ^ 0x1021;
            else crc <<= 1;
        }
    }
    return crc;
}

static esp_err_t send_interchip_frame(uint8_t type, const void *payload, uint8_t len) {
    if (!s_bridge.initialized || len > 32) return ESP_ERR_INVALID_ARG;

    InterchipFrame frame;
    frame.magic = INTERCHIP_MAGIC;
    frame.pkt_type = type;
    frame.payload_len = len;
    if (payload && len > 0) {
        memcpy(frame.payload, payload, len);
    }
    frame.crc16 = calculate_crc16((const uint8_t*)&frame, sizeof(frame) - 2);

    int sent = uart_write_bytes(C3_UART_NUM, &frame, sizeof(InterchipFrame));
    return (sent == sizeof(InterchipFrame)) ? ESP_OK : ESP_FAIL;
}

esp_err_t front_c3_bridge_init(void) {
    ESP_LOGI(TAG, "Initializing Front-Node C3 Bridge (U1 S31 -> U10 C3FH4)...");

    // 1. Configure Hardware Reset & Boot Pins for U10
    gpio_config_t rst_conf = {
        .pin_bit_mask = (1ULL << PIN_C3_EN) | (1ULL << PIN_C3_BOOT),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&rst_conf);

    // Boot into Normal Mode (BOOT=1, EN=0 -> EN=1)
    gpio_set_level(PIN_C3_BOOT, 1);
    gpio_set_level(PIN_C3_EN, 0);
    vTaskDelay(pdMS_TO_TICKS(10));
    gpio_set_level(PIN_C3_EN, 1);
    ESP_LOGI(TAG, "U10 (ESP32-C3FH4) powered up and taken out of reset.");

    // 2. Configure 921600 Baud UART
    uart_config_t uart_cfg = {
        .baud_rate = 921600,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };
    esp_err_t err = uart_param_config(C3_UART_NUM, &uart_cfg);
    if (err != ESP_OK) return err;

    err = uart_set_pin(C3_UART_NUM, PIN_C3_UART_TX, PIN_C3_UART_RX, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    if (err != ESP_OK) return err;

    err = uart_driver_install(C3_UART_NUM, C3_UART_BUF_SIZE * 2, 0, 0, NULL, 0);
    if (err != ESP_OK) return err;

    // 3. Configure I2S Master Audio Stream (Stereo 48 kHz 16-bit)
    i2s_chan_config_t chan_cfg = I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_1, I2S_ROLE_MASTER);
    err = i2s_new_channel(&chan_cfg, &s_bridge.tx_chan, NULL);
    if (err == ESP_OK && s_bridge.tx_chan) {
        i2s_std_config_t std_cfg = {
            .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(48000),
            .slot_cfg = I2S_STD_PHILIPS_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_STEREO),
            .gpio_cfg = {
                .mclk = I2S_GPIO_UNUSED,
                .bclk = PIN_C3_I2S_BCLK,
                .ws   = PIN_C3_I2S_WS,
                .dout = PIN_C3_I2S_SDO,
                .din  = PIN_C3_I2S_SDI,
                .invert_flags = {
                    .mclk_inv = false,
                    .bclk_inv = false,
                    .ws_inv   = false,
                },
            },
        };
        i2s_channel_init_std_mode(s_bridge.tx_chan, &std_cfg);
        i2s_channel_enable(s_bridge.tx_chan);
    }

    s_bridge.status.c3_online = true;
    s_bridge.status.usb_headunit_connected = true;
    s_bridge.status.carplay_unlocked = true;
    s_bridge.status.bike_speakers_active = true;
    s_bridge.status.headunit_volume_pct = 75;
    s_bridge.status.display_mux_target = 0;
    s_bridge.initialized = true;

    ESP_LOGI(TAG, "✅ Front-Node C3 Bridge online (UART + I2S Master active).");
    return ESP_OK;
}

void front_c3_bridge_set_status_callback(FrontC3StatusCallback cb) {
    s_bridge.status_cb = cb;
}

esp_err_t front_c3_bridge_set_speakers(bool active) {
    s_bridge.status.bike_speakers_active = active;
    uint8_t payload = active ? 1 : 0;
    return send_interchip_frame(0x01, &payload, 1);
}

esp_err_t front_c3_bridge_send_media_key(uint8_t key_code) {
    ESP_LOGI(TAG, "Forwarding Media Key %d to Headunit via C3 USB HID...", key_code);
    return send_interchip_frame(0x03, &key_code, 1);
}

esp_err_t front_c3_bridge_select_mux(uint8_t target) {
    s_bridge.status.display_mux_target = target;
    return send_interchip_frame(0x05, &target, 1);
}

esp_err_t front_c3_bridge_stream_audio(const int16_t *pcm_stereo, size_t sample_count) {
    if (!s_bridge.initialized || !s_bridge.tx_chan || !s_bridge.status.bike_speakers_active) {
        return ESP_OK;
    }
    size_t bytes_to_write = sample_count * sizeof(int16_t) * 2;
    size_t bytes_written = 0;
    return i2s_channel_write(s_bridge.tx_chan, pcm_stereo, bytes_to_write, &bytes_written, 0);
}

void front_c3_bridge_update_tick(void) {
    if (!s_bridge.initialized) return;

    size_t available = 0;
    uart_get_buffered_data_len(C3_UART_NUM, &available);
    if (available < sizeof(InterchipFrame)) return;

    InterchipFrame frame;
    int read_bytes = uart_read_bytes(C3_UART_NUM, &frame, sizeof(InterchipFrame), 0);
    if (read_bytes == sizeof(InterchipFrame)) {
        if (frame.magic != INTERCHIP_MAGIC) return;

        uint16_t expected_crc = calculate_crc16((const uint8_t*)&frame, sizeof(frame) - 2);
        if (frame.crc16 != expected_crc) return;

        s_bridge.last_rx_us = esp_timer_get_time();
        s_bridge.status.c3_online = true;

        if (frame.pkt_type == 0x10 && frame.payload_len >= sizeof(C3PayloadState)) {
            const C3PayloadState *c3_stat = (const C3PayloadState*)frame.payload;
            s_bridge.status.usb_headunit_connected = c3_stat->usb_enumerated;
            s_bridge.status.carplay_unlocked = c3_stat->carplay_active;
            s_bridge.status.bike_speakers_active = c3_stat->speakers_active;
            s_bridge.status.headunit_volume_pct = c3_stat->headunit_vol_pct;

            if (s_bridge.status_cb) {
                s_bridge.status_cb(&s_bridge.status);
            }
        }
    }
}

FrontC3BridgeStatus_t front_c3_bridge_get_status(void) {
    return s_bridge.status;
}
