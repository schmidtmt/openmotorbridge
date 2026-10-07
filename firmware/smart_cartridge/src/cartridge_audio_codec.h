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

    // Write zero-latency voice audio to Intercom Mic-Pin (< 1 ms via ES8388 DAC)
    size_t write_voice_mic(const int16_t* voice_samples, size_t num_samples);

    // Push stereo music samples into A2DP streaming buffer for Mesh Music-Sharing
    void push_music_samples(const int16_t* music_l, const int16_t* music_r, size_t num_samples);

    // Read audio samples from Headset Speaker Out (ES8388 ADC)
    size_t read_audio_frames(int16_t* buffer, size_t max_samples);

    // Generic write
    size_t write_audio_frames(const int16_t* buffer, size_t num_samples);

    bool is_initialized() const { return m_initialized; }

private:
    CartridgeAudioCodec();
    ~CartridgeAudioCodec() = default;

    esp_err_t init_i2c();
    esp_err_t init_i2s();
    esp_err_t write_codec_reg(uint8_t reg, uint8_t val);

    bool m_initialized;
};
