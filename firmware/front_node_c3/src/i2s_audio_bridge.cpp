#include "i2s_audio_bridge.h"
#include <string.h>
#include "esp_log.h"
#include "driver/i2s_std.h"
#include "front_c3_config.h"
#include "usb_headunit_device.h"

static const char *TAG = "I2S_BRIDGE";

#define I2S_FRAME_SAMPLES (128) // ~2.6 ms per frame at 48 kHz stereo

static struct {
    i2s_chan_handle_t rx_handle;
    i2s_chan_handle_t tx_handle;
    bool speakers_active;
    bool initialized;
} s_i2s_state = {0};

esp_err_t i2s_audio_bridge_init(void) {
    ESP_LOGI(TAG, "Initializing I2S Audio Bridge in Slave Mode (48 kHz 16-bit Stereo)...");

    i2s_chan_config_t chan_cfg = I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_0, I2S_ROLE_SLAVE);
    esp_err_t err = i2s_new_channel(&chan_cfg, &s_i2s_state.tx_handle, &s_i2s_state.rx_handle);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to create I2S channels: %s", esp_err_to_name(err));
        return err;
    }

    i2s_std_config_t std_cfg = {
        .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(48000),
        .slot_cfg = I2S_STD_PHILIPS_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_STEREO),
        .gpio_cfg = {
            .mclk = PIN_C3_I2S_MCLK,
            .bclk = PIN_C3_I2S_BCLK,
            .ws   = PIN_C3_I2S_WS,
            .dout = PIN_C3_I2S_SDI, // Transmit Mic data back to S31
            .din  = PIN_C3_I2S_SDO, // Receive Audio Playback from S31
            .invert_flags = {
                .mclk_inv = false,
                .bclk_inv = false,
                .ws_inv   = false,
            },
        },
    };

    if (s_i2s_state.rx_handle) {
        err = i2s_channel_init_std_mode(s_i2s_state.rx_handle, &std_cfg);
        if (err == ESP_OK) {
            i2s_channel_enable(s_i2s_state.rx_handle);
        }
    }

    if (s_i2s_state.tx_handle) {
        err = i2s_channel_init_std_mode(s_i2s_state.tx_handle, &std_cfg);
        if (err == ESP_OK) {
            i2s_channel_enable(s_i2s_state.tx_handle);
        }
    }

    s_i2s_state.speakers_active = true;
    s_i2s_state.initialized = true;

    ESP_LOGI(TAG, "✅ I2S Audio Bridge initialized in Slave Mode.");
    return ESP_OK;
}

void i2s_audio_bridge_set_speakers_active(bool active) {
    s_i2s_state.speakers_active = active;
    ESP_LOGI(TAG, "Bord-Lautsprecher Streaming %s", active ? "AKTIV (Stereo UAC)" : "STUMM / HEADSET-ONLY");
}

void i2s_audio_bridge_process(void) {
    if (!s_i2s_state.initialized || !s_i2s_state.rx_handle) return;

    int16_t buffer[I2S_FRAME_SAMPLES * 2]; // 128 samples * 2 channels
    size_t bytes_read = 0;

    esp_err_t err = i2s_channel_read(s_i2s_state.rx_handle, buffer, sizeof(buffer), &bytes_read, 0);
    if (err == ESP_OK && bytes_read > 0) {
        if (s_i2s_state.speakers_active) {
            size_t sample_count = bytes_read / (sizeof(int16_t) * 2);
            usb_headunit_push_speaker_audio(buffer, sample_count);
        }
    }
}

