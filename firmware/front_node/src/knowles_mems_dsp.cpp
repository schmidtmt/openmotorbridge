#include "knowles_mems_dsp.h"
#include "front_node_config.h"
#include "driver/i2s.h"
#include "esp_log.h"
#include <math.h>

static const char* TAG = "KNOWLES_DSP";

#define I2S_PORT            I2S_NUM_0
#define SAMPLE_RATE_HZ      16000
#define SAMPLES_PER_FRAME   320   // 20 ms @ 16 kHz

KnowlesMemsDsp& KnowlesMemsDsp::instance() {
    static KnowlesMemsDsp inst;
    return inst;
}

KnowlesMemsDsp::KnowlesMemsDsp()
    : m_w1(0.0f)
    , m_w2(0.0f)
    , m_latest_dba(45) // Default ambient background
    , m_raw_rms(0)
{
}

bool KnowlesMemsDsp::init() {
    // 1. Configure I2S driver for Knowles SPH0645LM4H
    // The SPH0645 outputs 24-bit data in a 32-bit slot, MSB first, standard Philips I2S.
    i2s_config_t i2s_config = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
        .sample_rate = SAMPLE_RATE_HZ,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_32BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT, // SPH0645 left channel
        .communication_format = I2S_COMM_FORMAT_STAND_I2S,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = 4,
        .dma_buf_len = SAMPLES_PER_FRAME,
        .use_apll = false,
        .tx_desc_auto_clear = false,
        .fixed_mclk = 0
    };

    i2s_pin_config_t pin_config = {
        .bck_io_num = PIN_MIC_I2S_BCLK,
        .ws_io_num = PIN_MIC_I2S_WS,
        .data_out_num = I2S_PIN_NO_CHANGE,
        .data_in_num = PIN_MIC_I2S_DATA
    };

    esp_err_t err = i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "i2s_driver_install failed: %s", esp_err_to_name(err));
        return false;
    }

    err = i2s_set_pin(I2S_PORT, &pin_config);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "i2s_set_pin failed: %s", esp_err_to_name(err));
        return false;
    }

    ESP_LOGI(TAG, "Knowles SPH0645LM4H I2S driver initialized (16 kHz, 24/32-Bit, WS=GPIO1, BCLK=GPIO2, DIN=GPIO3)");
    return true;
}

void KnowlesMemsDsp::process_audio() {
    int32_t raw_samples[SAMPLES_PER_FRAME];
    size_t bytes_read = 0;

    esp_err_t res = i2s_read(I2S_PORT, raw_samples, sizeof(raw_samples), &bytes_read, pdMS_TO_TICKS(50));
    if (res != ESP_OK || bytes_read == 0) {
        return;
    }

    size_t sample_count = bytes_read / sizeof(int32_t);
    double sum_squares = 0.0;

    // Direct Form II Biquad A-Weighting Filter Coefficients (fs = 16 kHz)
    // Approximate acoustic weighting in human speech/wind range
    const float b0 = 0.255f, b1 = 0.0f, b2 = -0.255f;
    const float a1 = -1.250f, a2 = 0.420f;

    for (size_t i = 0; i < sample_count; ++i) {
        // Shift 32-bit container to signed 24-bit PCM
        int32_t val = raw_samples[i] >> 8;
        float input_sample = static_cast<float>(val) / 8388608.0f; // Normalize to -1.0 .. +1.0

        // Apply Biquad Filter
        float w0 = input_sample - a1 * m_w1 - a2 * m_w2;
        float filtered = b0 * w0 + b1 * m_w1 + b2 * m_w2;
        m_w2 = m_w1;
        m_w1 = w0;

        sum_squares += (filtered * filtered);
    }

    float mean_square = static_cast<float>(sum_squares / sample_count);
    float rms = sqrtf(mean_square);
    m_raw_rms = static_cast<uint32_t>(rms * 10000.0f);

    // Convert normalized RMS to acoustic dB(A) SPL estimate
    // Standard calibration: 0 dBFS RMS ≈ 120 dBA SPL (SPH0645 Acoustic Overload Point)
    float dba_calc = 120.0f + 20.0f * log10f(rms + 1e-6f);
    if (dba_calc < 35.0f) dba_calc = 35.0f;
    if (dba_calc > 115.0f) dba_calc = 115.0f;

    // Low-pass smooth the dBA output (alpha = 0.3)
    m_latest_dba = static_cast<uint8_t>(0.7f * m_latest_dba + 0.3f * dba_calc);
}

uint8_t KnowlesMemsDsp::get_latest_dba() const {
    return m_latest_dba;
}

uint32_t KnowlesMemsDsp::get_raw_rms() const {
    return m_raw_rms;
}
