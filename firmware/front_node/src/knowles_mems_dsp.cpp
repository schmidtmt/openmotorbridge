#include "knowles_mems_dsp.h"
#include "front_node_config.h"
#include "driver/i2s_std.h"
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
    , m_rx_chan(NULL)
{
}

bool KnowlesMemsDsp::init() {
    // 1. Configure I2S driver for MSM261S4030H0R (compatible with Knowles SPH0645LM4H)
    // The MSM261S4030H0R outputs standard Philips I2S 24-bit data in a 32-bit slot, MSB first.
    i2s_chan_config_t chan_cfg = I2S_CHANNEL_DEFAULT_CONFIG(I2S_PORT, I2S_ROLE_MASTER);
    i2s_chan_handle_t rx_handle = NULL;
    esp_err_t err = i2s_new_channel(&chan_cfg, NULL, &rx_handle);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "i2s_new_channel failed: %s", esp_err_to_name(err));
        return false;
    }
    m_rx_chan = (void*)rx_handle;

    i2s_std_config_t std_cfg = {
        .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(SAMPLE_RATE_HZ),
        .slot_cfg = I2S_STD_PHILIPS_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_32BIT, I2S_SLOT_MODE_MONO),
        .gpio_cfg = {
            .mclk = I2S_GPIO_UNUSED,
            .bclk = (gpio_num_t)PIN_MIC_I2S_BCLK,
            .ws = (gpio_num_t)PIN_MIC_I2S_WS,
            .dout = I2S_GPIO_UNUSED,
            .din = (gpio_num_t)PIN_MIC_I2S_DATA,
            .invert_flags = {
                .mclk_inv = false,
                .bclk_inv = false,
                .ws_inv = false,
            },
        },
    };

    err = i2s_channel_init_std_mode((i2s_chan_handle_t)m_rx_chan, &std_cfg);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "i2s_channel_init_std_mode failed: %s", esp_err_to_name(err));
        return false;
    }

    err = i2s_channel_enable((i2s_chan_handle_t)m_rx_chan);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "i2s_channel_enable failed: %s", esp_err_to_name(err));
        return false;
    }

    ESP_LOGI(TAG, "Digital MEMS Microphone I2S driver initialized (16 kHz, 24/32-Bit, WS=GPIO%d, BCLK=GPIO%d, DIN=GPIO%d)",
             PIN_MIC_I2S_WS, PIN_MIC_I2S_BCLK, PIN_MIC_I2S_DATA);
    return true;
}

void KnowlesMemsDsp::process_audio() {
    if (!m_rx_chan) return;
    int32_t raw_samples[SAMPLES_PER_FRAME];
    size_t bytes_read = 0;

    esp_err_t res = i2s_channel_read((i2s_chan_handle_t)m_rx_chan, raw_samples, sizeof(raw_samples), &bytes_read, 50);
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
