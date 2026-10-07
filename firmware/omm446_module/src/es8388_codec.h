#pragma once

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Initialize ES8388 I2C control interface and I2S audio stream.
 */
esp_err_t es8388_codec_init(void);

/**
 * @brief Set master playback output volume.
 * @param volume_pct Volume from 0 to 100%.
 */
esp_err_t es8388_set_volume(uint8_t volume_pct);

/**
 * @brief Set microphone preamplifier analog gain.
 * @param gain_db Gain in dB (0 to +30 dB).
 */
esp_err_t es8388_set_mic_gain(uint8_t gain_db);

/**
 * @brief Read mono microphone samples from ADC stream.
 */
esp_err_t es8388_read_audio(int16_t *samples, size_t count, size_t *out_read);

/**
 * @brief Write stereo samples to DAC headphone stream.
 */
esp_err_t es8388_write_audio(const int16_t *samples, size_t count, size_t *out_written);

/**
 * @brief Mute or unmute the headphone DAC output.
 */
void es8388_set_mute(bool mute);

#ifdef __cplusplus
}
#endif
