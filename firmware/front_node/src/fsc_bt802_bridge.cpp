#include "fsc_bt802_bridge.h"
#include <string.h>
#include <stdio.h>
#include "esp_log.h"
#include "driver/gpio.h"
#include "driver/uart.h"
#include "driver/i2s_std.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

static const char* TAG = "FSC_BT802";

#define BT802_UART_PORT      UART_NUM_1
#define BT802_UART_BAUD      115200
#define BT802_BUF_SIZE       512
#define BT802_I2S_PORT       I2S_NUM_1

static i2s_chan_handle_t s_i2s_tx_chan = NULL;
static i2s_chan_handle_t s_i2s_rx_chan = NULL;

static FscBt802Status_t s_status = {
    .mode = BT802_MODE_STANDBY,
    .bt_online = false,
    .connected_to_headunit = false,
    .a2dp_streaming = false,
    .hfp_call_active = false,
    .rssi_dbm = -65,
    .volume_pct = 75
};

static FscBt802StatusCallback s_callback = NULL;

static void bt802_send_at(const char* cmd) {
    ESP_LOGD(TAG, "TX AT: %s", cmd);
    uart_write_bytes(BT802_UART_PORT, cmd, strlen(cmd));
    uart_write_bytes(BT802_UART_PORT, "\r\n", 2);
}

esp_err_t fsc_bt802_bridge_init(void) {
    ESP_LOGI(TAG, "Initializing FSC-BT802 CSR8670 Infotainment Bridge on PCBA 05...");

    // 1. Hardware Power & Reset Sequence
    gpio_config_t pwr_conf = {
        .pin_bit_mask = (1ULL << PIN_FRONT_BT_EN) | (1ULL << PIN_FRONT_BT_RST),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&pwr_conf);

    // Assert reset, enable power
    gpio_set_level(PIN_FRONT_BT_EN, 1);
    gpio_set_level(PIN_FRONT_BT_RST, 0);
    vTaskDelay(pdMS_TO_TICKS(50));
    gpio_set_level(PIN_FRONT_BT_RST, 1);
    vTaskDelay(pdMS_TO_TICKS(150));

    // 2. Configure UART for AT Command Interface
    uart_config_t uart_config = {
        .baud_rate = BT802_UART_BAUD,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };
    uart_param_config(BT802_UART_PORT, &uart_config);
    uart_set_pin(BT802_UART_PORT, PIN_FRONT_BT_UART_TX, PIN_FRONT_BT_UART_RX,
                 UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    uart_driver_install(BT802_UART_PORT, BT802_BUF_SIZE * 2, 0, 0, NULL, 0);

    // 3. Configure I2S Bus for Synchronous Audio (48 kHz Stereo 16-bit)
    i2s_chan_config_t chan_cfg = I2S_CHANNEL_DEFAULT_CONFIG(BT802_I2S_PORT, I2S_ROLE_MASTER);
    chan_cfg.auto_clear_after_cb = true;
    esp_err_t i2s_err = i2s_new_channel(&chan_cfg, &s_i2s_tx_chan, &s_i2s_rx_chan);
    if (i2s_err == ESP_OK) {
        i2s_std_config_t std_cfg = {
            .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(48000),
            .slot_cfg = I2S_STD_PHILIPS_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_STEREO),
            .gpio_cfg = {
                .mclk = I2S_GPIO_UNUSED,
                .bclk = (gpio_num_t)PIN_FRONT_BT_I2S_BCLK,
                .ws = (gpio_num_t)PIN_FRONT_BT_I2S_WS,
                .dout = (gpio_num_t)PIN_FRONT_BT_I2S_DOUT,
                .din = (gpio_num_t)PIN_FRONT_BT_I2S_DIN,
                .invert_flags = {
                    .mclk_inv = false,
                    .bclk_inv = false,
                    .ws_inv = false,
                },
            },
        };
        i2s_channel_init_std_mode(s_i2s_tx_chan, &std_cfg);
        i2s_channel_init_std_mode(s_i2s_rx_chan, &std_cfg);
        i2s_channel_enable(s_i2s_tx_chan);
        i2s_channel_enable(s_i2s_rx_chan);
    } else {
        ESP_LOGE(TAG, "Failed to allocate FSC-BT802 I2S channels: %s", esp_err_to_name(i2s_err));
    }

    // Default boot mode: Mode A (Headset / Sink) to capture bike navigation voice
    fsc_bt802_bridge_set_mode(BT802_MODE_HEADSET_SINK, true);

    s_status.bt_online = true;
    ESP_LOGI(TAG, "FSC-BT802 initialized. Default: Mode A (Headset Sink for Navigation audio)");
    return ESP_OK;
}

esp_err_t fsc_bt802_bridge_set_mode(FscBt802OperatingMode mode, bool force) {
    if (s_status.mode == mode && !force) {
        return ESP_OK;
    }

    ESP_LOGI(TAG, "Switching FSC-BT802 mode: %s -> %s (force=%d)",
             (s_status.mode == BT802_MODE_HEADSET_SINK) ? "Mode A (Headset Sink)" : "Mode B (Speaker Source)",
             (mode == BT802_MODE_HEADSET_SINK) ? "Mode A (Headset Sink)" : "Mode B (Speaker Source)",
             force);

    if (mode == BT802_MODE_HEADSET_SINK) {
        // Mode A: Emulate Bluetooth Headset connected to Harley Boom! Box / SkylineOS / BMW TFT
        // AT+PROFILE=24 -> HFP + A2DP Sink
        bt802_send_at("AT+DISC"); // Disconnect active link before reconfig
        vTaskDelay(pdMS_TO_TICKS(50));
        bt802_send_at("AT+NAME=OpenMotorBridge Headset");
        bt802_send_at("AT+PROFILE=24"); // HFP + A2DP Sink
        bt802_send_at("AT+I2SCFG=1,0,0,16"); // 48kHz I2S Master
        bt802_send_at("AT+SCAN=1"); // Make discoverable for head unit pairing
        s_status.mode = BT802_MODE_HEADSET_SINK;
        ESP_LOGI(TAG, "FSC-BT802 configured as Headset Sink (Receiving bike nav prompts via I2S)");
    } else if (mode == BT802_MODE_BIKE_SPEAKER_SOURCE) {
        // Mode B: A2DP Source streaming OMB Master Mix to bike speakers
        // AT+PROFILE=02 -> A2DP Source
        bt802_send_at("AT+DISC");
        vTaskDelay(pdMS_TO_TICKS(50));
        bt802_send_at("AT+NAME=OpenMotorBridge Audio");
        bt802_send_at("AT+PROFILE=02"); // A2DP Source
        bt802_send_at("AT+I2SCFG=1,0,0,16");
        bt802_send_at("AT+AUTOCONN=1"); // Auto connect to paired SkylineOS / Boom! Box
        s_status.mode = BT802_MODE_BIKE_SPEAKER_SOURCE;
        ESP_LOGI(TAG, "FSC-BT802 configured as Speaker Source (Streaming master mix to bike speakers)");
    }

    if (s_callback) {
        s_callback(&s_status);
    }
    return ESP_OK;
}

void fsc_bt802_bridge_set_status_callback(FscBt802StatusCallback cb) {
    s_callback = cb;
}

esp_err_t fsc_bt802_bridge_send_media_key(uint8_t key_code) {
    char cmd[32];
    snprintf(cmd, sizeof(cmd), "AT+PLAYCMD=%u", key_code);
    bt802_send_at(cmd);
    ESP_LOGD(TAG, "Forwarded Media Key %u to bike headunit", key_code);
    return ESP_OK;
}

esp_err_t fsc_bt802_bridge_stream_audio_to_speakers(const int16_t *pcm_stereo, size_t sample_count) {
    if (s_status.mode != BT802_MODE_BIKE_SPEAKER_SOURCE || !s_i2s_tx_chan) {
        return ESP_ERR_INVALID_STATE;
    }
    size_t bytes_written = 0;
    return i2s_channel_write(s_i2s_tx_chan, pcm_stereo, sample_count * 2 * sizeof(int16_t), &bytes_written, 1000);
}

esp_err_t fsc_bt802_bridge_read_nav_audio(int16_t *pcm_out, size_t max_samples, size_t *samples_read) {
    if (s_status.mode != BT802_MODE_HEADSET_SINK || !s_i2s_rx_chan) {
        return ESP_ERR_INVALID_STATE;
    }
    size_t bytes_read = 0;
    esp_err_t ret = i2s_channel_read(s_i2s_rx_chan, pcm_out, max_samples * sizeof(int16_t), &bytes_read, 10);
    if (samples_read) {
        *samples_read = bytes_read / sizeof(int16_t);
    }
    return ret;
}

void fsc_bt802_bridge_update_tick(void) {
    uint8_t rx_buf[128];
    int len = uart_read_bytes(BT802_UART_PORT, rx_buf, sizeof(rx_buf) - 1, 0);
    if (len > 0) {
        rx_buf[len] = '\0';
        ESP_LOGD(TAG, "RX AT: %s", (char*)rx_buf);
        
        // Parse AT unsolicited notifications
        if (strstr((char*)rx_buf, "+HFPSTAT=3")) {
            s_status.hfp_call_active = true;
            ESP_LOGI(TAG, "📞 Bike Head Unit: Call Active");
        } else if (strstr((char*)rx_buf, "+HFPSTAT=0")) {
            s_status.hfp_call_active = false;
        }

        if (strstr((char*)rx_buf, "+CONNECTED")) {
            s_status.connected_to_headunit = true;
            ESP_LOGI(TAG, "✅ Connected to Bike Infotainment (SkylineOS / Boom! Box)");
        } else if (strstr((char*)rx_buf, "+DISCONNECT")) {
            s_status.connected_to_headunit = false;
            s_status.a2dp_streaming = false;
        }

        if (strstr((char*)rx_buf, "+A2DPSTAT=2")) {
            s_status.a2dp_streaming = true;
        }

        if (s_callback) {
            s_callback(&s_status);
        }
    }
}

FscBt802Status_t fsc_bt802_bridge_get_status(void) {
    return s_status;
}
