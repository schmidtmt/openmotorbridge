#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

class CartridgeAudioCodec {
public:
    static CartridgeAudioCodec& instance();

    esp_err_t init();
    esp_err_t set_mic_volume(uint8_t volume_pct);
    esp_err_t set_spk_gain(uint8_t gain_db);

    // Read audio samples from Headset Speaker Out (ES8388 ADC)
    size_t read_audio_frames(int16_t* buffer, size_t max_samples);

    // Write audio samples to Headset Microphone In (ES8388 DAC)
    size_t write_audio_frames(const int16_t* buffer, size_t num_samples);

private:
    CartridgeAudioCodec();
    ~CartridgeAudioCodec() = default;

    esp_err_t init_i2c();
    esp_err_t init_i2s();
    esp_err_t write_codec_reg(uint8_t reg, uint8_t val);

    bool m_initialized;
};
