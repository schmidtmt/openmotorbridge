#include "cartridge_audio_codec.h"
#include "cartridge_config.h"
#include "esp_log.h"
#include "driver/i2c.h"
#include "driver/i2s_std.h"

static const char* TAG = "CARTRIDGE_CODEC";

#define ES8388_I2C_ADDR         0x10 // ES8388 7-bit I2C Address (CE=0)
#define CODEC_I2C_NUM           I2C_NUM_0
#define I2S_PORT_NUM            I2S_NUM_0

static i2s_chan_handle_t s_tx_chan = NULL;
static i2s_chan_handle_t s_rx_chan = NULL;

CartridgeAudioCodec& CartridgeAudioCodec::instance() {
    static CartridgeAudioCodec s_instance;
    return s_instance;
}

CartridgeAudioCodec::CartridgeAudioCodec() : m_initialized(false) {
}

esp_err_t CartridgeAudioCodec::init_i2c() {
    i2c_config_t conf = {};
    conf.mode = I2C_MODE_MASTER;
    conf.sda_io_num = PIN_CODEC_I2C_SDA;
    conf.scl_io_num = PIN_CODEC_I2C_SCL;
    conf.sda_pullup_en = GPIO_PULLUP_ENABLE;
    conf.scl_pullup_en = GPIO_PULLUP_ENABLE;
    conf.master.clk_speed = 100000;

    esp_err_t err = i2c_param_config(CODEC_I2C_NUM, &conf);
    if (err != ESP_OK) return err;
    return i2c_driver_install(CODEC_I2C_NUM, conf.mode, 0, 0, 0);
}

esp_err_t CartridgeAudioCodec::write_codec_reg(uint8_t reg, uint8_t val) {
    uint8_t write_buf[2] = {reg, val};
    return i2c_master_write_to_device(CODEC_I2C_NUM, ES8388_I2C_ADDR, write_buf, sizeof(write_buf), pdMS_TO_TICKS(100));
}

esp_err_t CartridgeAudioCodec::init_i2s() {
    i2s_chan_config_t chan_cfg = I2S_CHANNEL_DEFAULT_CONFIG(I2S_PORT_NUM, I2S_ROLE_MASTER);
    esp_err_t err = i2s_new_channel(&chan_cfg, &s_tx_chan, &s_rx_chan);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to create I2S channels: %s", esp_err_to_name(err));
        return err;
    }

    i2s_std_config_t std_cfg = {
        .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(48000),
        .slot_cfg = I2S_STD_PHILIP_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_STEREO),
        .gpio_cfg = {
            .mclk = PIN_I2S_MCLK,
            .bclk = PIN_I2S_BCLK,
            .ws = PIN_I2S_WS,
            .dout = PIN_I2S_DOUT,
            .din = PIN_I2S_DIN,
            .invert_flags = {
                .mclk_inv = false,
                .bclk_inv = false,
                .ws_inv = false,
            },
        },
    };

    err = i2s_channel_init_std_mode(s_tx_chan, &std_cfg);
    if (err != ESP_OK) return err;
    err = i2s_channel_init_std_mode(s_rx_chan, &std_cfg);
    if (err != ESP_OK) return err;

    i2s_channel_enable(s_tx_chan);
    i2s_channel_enable(s_rx_chan);
    return ESP_OK;
}

esp_err_t CartridgeAudioCodec::init() {
    ESP_LOGI(TAG, "Initializing Everest Semi ES8388 Codec on PCBA 03...");

    esp_err_t err = init_i2c();
    if (err != ESP_OK) {
        ESP_LOGW(TAG, "ES8388 I2C init failed (%s) - continuing in digital/mechatronic-only mode", esp_err_to_name(err));
        return err;
    }

    // Configure ES8388 Registers (Basic 48 kHz 16-Bit I2S setup)
    write_codec_reg(0x00, 0x80); // Chip control 1: reset
    write_codec_reg(0x00, 0x00);
    write_codec_reg(0x01, 0x58); // Power down all except analog reference
    write_codec_reg(0x02, 0xF3); // Power up analog reference, power down DAC/ADC
    write_codec_reg(0x04, 0x00); // DAC power up
    write_codec_reg(0x03, 0x00); // ADC power up
    write_codec_reg(0x09, 0x00); // ADC Master / Slave mode: Slave
    write_codec_reg(0x0A, 0x00); // ADC Format: I2S 16-bit
    write_codec_reg(0x17, 0x00); // DAC Master / Slave mode: Slave
    write_codec_reg(0x18, 0x00); // DAC Format: I2S 16-bit
    write_codec_reg(0x2E, 0x1E); // Output volume L
    write_codec_reg(0x2F, 0x1E); // Output volume R

    err = init_i2s();
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "ES8388 I2S init failed: %s", esp_err_to_name(err));
        return err;
    }

    m_initialized = true;
    ESP_LOGI(TAG, "ES8388 Codec initialized successfully.");
    return ESP_OK;
}

esp_err_t CartridgeAudioCodec::set_mic_volume(uint8_t volume_pct) {
    if (!m_initialized) return ESP_ERR_INVALID_STATE;
    uint8_t reg_val = (volume_pct * 33) / 100;
    return write_codec_reg(0x2E, reg_val);
}

esp_err_t CartridgeAudioCodec::set_spk_gain(uint8_t gain_db) {
    if (!m_initialized) return ESP_ERR_INVALID_STATE;
    return write_codec_reg(0x10, gain_db & 0x1F);
}

size_t CartridgeAudioCodec::read_audio_frames(int16_t* buffer, size_t max_samples) {
    if (!m_initialized || !s_rx_chan) return 0;
    size_t bytes_read = 0;
    i2s_channel_read(s_rx_chan, buffer, max_samples * sizeof(int16_t), &bytes_read, pdMS_TO_TICKS(10));
    return bytes_read / sizeof(int16_t);
}

size_t CartridgeAudioCodec::write_audio_frames(const int16_t* buffer, size_t num_samples) {
    if (!m_initialized || !s_tx_chan) return 0;
    size_t bytes_written = 0;
    i2s_channel_write(s_tx_chan, buffer, num_samples * sizeof(int16_t), &bytes_written, pdMS_TO_TICKS(10));
    return bytes_written / sizeof(int16_t);
}
