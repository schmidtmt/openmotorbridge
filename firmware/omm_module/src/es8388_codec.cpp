#include "es8388_codec.h"
#include "omm_module_config.h"
#include "esp_log.h"
#include "driver/i2c.h"
#include "driver/i2s_std.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

static const char *TAG = "OMM_ES8388";

static i2s_chan_handle_t tx_chan = NULL;
static i2s_chan_handle_t rx_chan = NULL;
static bool s_muted = false;

static esp_err_t es8388_write_reg(uint8_t reg, uint8_t val) {
    uint8_t data[2] = { reg, val };
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (ES8388_I2C_ADDR << 1) | I2C_MASTER_WRITE, true);
    i2c_master_write(cmd, data, sizeof(data), true);
    i2c_master_stop(cmd);
    esp_err_t ret = i2c_master_cmd_begin(OMM_I2C_PORT, cmd, pdMS_TO_TICKS(100));
    i2c_cmd_link_delete(cmd);
    return ret;
}

static esp_err_t es8388_read_reg(uint8_t reg, uint8_t *val) {
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (ES8388_I2C_ADDR << 1) | I2C_MASTER_WRITE, true);
    i2c_master_write_byte(cmd, reg, true);
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (ES8388_I2C_ADDR << 1) | I2C_MASTER_READ, true);
    i2c_master_read_byte(cmd, val, I2C_MASTER_NACK);
    i2c_master_stop(cmd);
    esp_err_t ret = i2c_master_cmd_begin(OMM_I2C_PORT, cmd, pdMS_TO_TICKS(100));
    i2c_cmd_link_delete(cmd);
    return ret;
}

esp_err_t es8388_codec_init(void) {
    ESP_LOGI(TAG, "Initializing ES8388 stereo codec I2C control interface...");

    // 1. I2C Bus Configuration
    i2c_config_t i2c_conf = {};
    i2c_conf.mode = I2C_MODE_MASTER;
    i2c_conf.sda_io_num = OMM_PIN_I2C_SDA;
    i2c_conf.scl_io_num = OMM_PIN_I2C_SCL;
    i2c_conf.sda_pullup_en = GPIO_PULLUP_ENABLE;
    i2c_conf.scl_pullup_en = GPIO_PULLUP_ENABLE;
    i2c_conf.master.clk_speed = OMM_I2C_FREQ_HZ;

    esp_err_t ret = i2c_param_config(OMM_I2C_PORT, &i2c_conf);
    if (ret != ESP_OK) return ret;
    ret = i2c_driver_install(OMM_I2C_PORT, i2c_conf.mode, 0, 0, 0);
    if (ret != ESP_OK && ret != ESP_ERR_INVALID_STATE) return ret;

    // 2. ES8388 Hardware Register Sequence for 48 kHz / 16-bit Duplex
    es8388_write_reg(0x00, 0x80); // Chip soft reset
    vTaskDelay(pdMS_TO_TICKS(10));
    es8388_write_reg(0x00, 0x00); // Normal mode

    es8388_write_reg(0x01, 0x58); // Power up analog references & VMID
    es8388_write_reg(0x02, 0x00); // Power up all internal blocks
    es8388_write_reg(0x03, 0x00); // Power up ADC
    es8388_write_reg(0x04, 0x3C); // Power up DAC & LOUT1 / ROUT1 output drivers

    // Master / Slave mode: ES8388 operates as I2S Slave to ESP32-C6 Master
    es8388_write_reg(0x08, 0x00); // Slave mode

    // ADC setup: MIC1P differential/single-ended, +18 dB gain for motorcycle helmets
    es8388_write_reg(0x09, 0x88); // ADC PGA gain +24 dB
    es8388_write_reg(0x0A, 0x00); // Select MIC1 input channel
    es8388_write_reg(0x0C, 0x0C); // ADC I2S 16-bit format

    // DAC setup: Stereo LOUT1 / ROUT1 headphone out
    es8388_write_reg(0x17, 0x18); // DAC I2S 16-bit format
    es8388_write_reg(0x18, 0x02); // DAC unmute, 0 dB
    es8388_write_reg(0x1A, 0x00); // LOUT1 volume (0 dB)
    es8388_write_reg(0x1B, 0x00); // ROUT1 volume (0 dB)
    es8388_write_reg(0x27, 0xB8); // LOUT1 / ROUT1 mixer enable
    es8388_write_reg(0x2E, 0x1E); // LOUT1 drive level (+3 dB)
    es8388_write_reg(0x2F, 0x1E); // ROUT1 drive level (+3 dB)

    // 3. I2S Standard Stereo Duplex Bus Configuration
    ESP_LOGI(TAG, "Configuring I2S Standard Master Duplex Stream (48 kHz, 16-Bit Stereo)...");
    i2s_chan_config_t chan_cfg = I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_0, I2S_ROLE_MASTER);
    chan_cfg.auto_clear = true;
    ret = i2s_new_channel(&chan_cfg, &tx_chan, &rx_chan);
    if (ret != ESP_OK) return ret;

    i2s_std_config_t std_cfg = {
        .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(OMM_AUDIO_SAMPLE_RATE),
        .slot_cfg = I2S_STD_MSB_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_STEREO),
        .gpio_cfg = {
            .mclk = OMM_PIN_I2S_MCLK,
            .bclk = OMM_PIN_I2S_BCLK,
            .ws = OMM_PIN_I2S_WS,
            .dout = OMM_PIN_I2S_DOUT,
            .din = OMM_PIN_I2S_DIN,
            .invert_flags = {
                .mclk_inv = false,
                .bclk_inv = false,
                .ws_inv = false,
            },
        },
    };

    ret = i2s_channel_init_std_mode(tx_chan, &std_cfg);
    if (ret != ESP_OK) return ret;
    ret = i2s_channel_init_std_mode(rx_chan, &std_cfg);
    if (ret != ESP_OK) return ret;

    ret = i2s_channel_enable(tx_chan);
    if (ret != ESP_OK) return ret;
    ret = i2s_channel_enable(rx_chan);
    if (ret != ESP_OK) return ret;

    ESP_LOGI(TAG, "✓ ES8388 Stereo Codec & I2S Duplex Stream successfully initialized.");
    return ESP_OK;
}

esp_err_t es8388_set_volume(uint8_t volume_pct) {
    if (volume_pct > 100) volume_pct = 100;
    // Invert scale: 0x00 is max (0 dB), 0x60 is -48 dB, 0x7F is mute
    uint8_t reg_val = (uint8_t)((100 - volume_pct) * 96 / 100);
    es8388_write_reg(0x1A, reg_val); // LOUT1
    return es8388_write_reg(0x1B, reg_val); // ROUT1
}

esp_err_t es8388_set_mic_gain(uint8_t gain_db) {
    if (gain_db > 30) gain_db = 30;
    uint8_t pga = (gain_db / 3) & 0x0F;
    return es8388_write_reg(0x09, (pga << 4) | pga);
}

esp_err_t es8388_read_audio(int16_t *samples, size_t count, size_t *out_read) {
    if (!rx_chan) return ESP_ERR_INVALID_STATE;
    size_t bytes_to_read = count * sizeof(int16_t);
    size_t bytes_read = 0;
    esp_err_t ret = i2s_channel_read(rx_chan, samples, bytes_to_read, &bytes_read, pdMS_TO_TICKS(50));
    if (out_read) *out_read = bytes_read / sizeof(int16_t);
    return ret;
}

esp_err_t es8388_write_audio(const int16_t *samples, size_t count, size_t *out_written) {
    if (!tx_chan) return ESP_ERR_INVALID_STATE;
    if (s_muted) {
        if (out_written) *out_written = count;
        return ESP_OK;
    }
    size_t bytes_to_write = count * sizeof(int16_t);
    size_t bytes_written = 0;
    esp_err_t ret = i2s_channel_write(tx_chan, samples, bytes_to_write, &bytes_written, pdMS_TO_TICKS(50));
    if (out_written) *out_written = bytes_written / sizeof(int16_t);
    return ret;
}

void es8388_set_mute(bool mute) {
    s_muted = mute;
    es8388_write_reg(0x18, mute ? 0x22 : 0x02); // DAC soft mute
}
