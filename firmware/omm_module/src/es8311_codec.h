#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Initialize ES8311 I2C control interface and I2S audio stream.
 */
esp_err_t es8311_codec_init(void);

/**
 * @brief Set DAC / Headphone playback volume (0..100%).
 */
esp_err_t es8311_set_volume(uint8_t volume_pct);

/**
 * @brief Set Microphone preamp gain in dB (0..+30 dB).
 */
esp_err_t es8311_set_mic_gain(uint8_t gain_db);

/**
 * @brief Read microphone audio samples from I2S RX DMA.
 */
esp_err_t es8311_read_audio(int16_t *samples, size_t count, size_t *out_read);

/**
 * @brief Write received audio samples to I2S TX DMA for headphone playback.
 */
esp_err_t es8311_write_audio(const int16_t *samples, size_t count, size_t *out_written);

/**
 * @brief Hardware mute / unmute headphone output.
 */
void es8311_set_mute(bool mute);

#ifdef __cplusplus
}
#endif
