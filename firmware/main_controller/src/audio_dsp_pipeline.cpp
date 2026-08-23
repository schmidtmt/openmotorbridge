#include "audio_dsp_pipeline.h"
#include <stdio.h>
#include <string.h>
#include <math.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/i2s_std.h"
#include "esp_log.h"

static const char *TAG = "AUDIO_DSP";

// I2S Pin-Definitionen (v8.0 Pinout)
#define I2S_PIN_MCLK        GPIO_NUM_9
#define I2S_PIN_BCLK        GPIO_NUM_10
#define I2S_PIN_WS          GPIO_NUM_11
#define I2S_PIN_DOUT        GPIO_NUM_12
#define I2S_PIN_DIN         GPIO_NUM_13

#define SAMPLE_RATE_HZ      48000
#define BUFFER_SAMPLES      128
#define DUCKING_ATTACK      0.05f   // Schneller Ducking-Eintritt (ca. 15 ms)
#define DUCKING_RELEASE     0.002f  // Sanftes Ausblenden (ca. 800 ms)

static i2s_chan_handle_t tx_chan = NULL;
static i2s_chan_handle_t rx_chan = NULL;

static AudioOperationMode s_current_mode = MODE_STANDARD;
static float s_ducking_factor = 1.0f;
static bool s_nav_ducking_active = false;

static float s_port1_gain = 1.0f;
static float s_port2_gain = 1.0f;

esp_err_t audio_dsp_init(void) {
    ESP_LOGI(TAG, "Initializing I2S Standard Master Driver (48 kHz / 16-Bit Stereo)...");

    i2s_chan_config_t chan_cfg = I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_0, I2S_ROLE_MASTER);
    chan_cfg.dma_desc_num = 6;
    chan_cfg.dma_frame_num = BUFFER_SAMPLES;
    chan_cfg.auto_clear = true;

    esp_err_t ret = i2s_new_channel(&chan_cfg, &tx_chan, &rx_chan);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to allocate I2S channels: %s", esp_err_to_name(ret));
        return ret;
    }

    i2s_std_config_t std_cfg = {
        .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(SAMPLE_RATE_HZ),
        .slot_cfg = I2S_STD_MSB_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_STEREO),
        .gpio_cfg = {
            .mclk = I2S_PIN_MCLK,
            .bclk = I2S_PIN_BCLK,
            .ws   = I2S_PIN_WS,
            .dout = I2S_PIN_DOUT,
            .din  = I2S_PIN_DIN,
            .invert_flags = {
                .mclk_inv = false,
                .bclk_inv = false,
                .ws_inv   = false,
            },
        },
    };
    std_cfg.clk_cfg.mclk_multiple = I2S_MCLK_MULTIPLE_256;

    ESP_ERROR_CHECK(i2s_channel_init_std_mode(tx_chan, &std_cfg));
    ESP_ERROR_CHECK(i2s_channel_init_std_mode(rx_chan, &std_cfg));

    ESP_ERROR_CHECK(i2s_channel_enable(tx_chan));
    ESP_ERROR_CHECK(i2s_channel_enable(rx_chan));

    ESP_LOGI(TAG, "I2S DMA Channels enabled and running.");
    return ESP_OK;
}

void audio_set_operation_mode(AudioOperationMode mode) {
    s_current_mode = mode;
    ESP_LOGI(TAG, "Audio Operating Mode changed to: %d", mode);
}

AudioOperationMode audio_get_operation_mode(void) {
    return s_current_mode;
}

void audio_set_port_gains(float port1_gain_db, float port2_gain_db) {
    s_port1_gain = powf(10.0f, port1_gain_db / 20.0f);
    s_port2_gain = powf(10.0f, port2_gain_db / 20.0f);
    ESP_LOGI(TAG, "Port Gains updated: P1=%.2f (%.1f dB), P2=%.2f (%.1f dB)",
             s_port1_gain, port1_gain_db, s_port2_gain, port2_gain_db);
}

void audio_set_nav_ducking(bool active) {
    s_nav_ducking_active = active;
}

void task_audio_dsp(void *pvParameters) {
    ESP_LOGI(TAG, "Audio DSP Realtime Pipeline Task running on Core 1.");

    int16_t rx_buffer[BUFFER_SAMPLES * 2]; // Interleaved Stereo (L=Port1, R=Port2)
    int16_t tx_buffer[BUFFER_SAMPLES * 2];
    size_t bytes_read = 0;
    size_t bytes_written = 0;

    while (true) {
        // 1. DMA Leseoperation vom Audio-Frontend
        esp_err_t ret = i2s_channel_read(rx_chan, rx_buffer, sizeof(rx_buffer), &bytes_read, pdMS_TO_TICKS(10));
        if (ret != ESP_OK || bytes_read == 0) {
            vTaskDelay(pdMS_TO_TICKS(1));
            continue;
        }

        // 2. Raised-Cosine Ducking Filterberechnung
        if (s_nav_ducking_active) {
            if (s_ducking_factor > 0.25f) { // -12 dB Ducking
                s_ducking_factor -= DUCKING_ATTACK;
                if (s_ducking_factor < 0.25f) s_ducking_factor = 0.25f;
            }
        } else {
            if (s_ducking_factor < 1.0f) {
                s_ducking_factor += DUCKING_RELEASE;
                if (s_ducking_factor > 1.0f) s_ducking_factor = 1.0f;
            }
        }

        // 3. Audio-Routing & Mischmatrix
        int samples_count = bytes_read / (sizeof(int16_t) * 2);
        for (int i = 0; i < samples_count; i++) {
            float p1_sample = (float)rx_buffer[i * 2] * s_port1_gain;
            float p2_sample = (float)rx_buffer[i * 2 + 1] * s_port2_gain;

            float out_l = 0.0f;
            float out_r = 0.0f;

            switch (s_current_mode) {
                case MODE_SINGLE_RIDER:
                    // Port 2 stumm, nur Port 1 geduckt
                    out_l = p1_sample * s_ducking_factor;
                    out_r = p1_sample * s_ducking_factor;
                    break;

                case MODE_CRUISE:
                    // Fokus auf Bordlautsprecher, Intercom -6 dB
                    out_l = (p1_sample + p2_sample) * 0.5f * s_ducking_factor;
                    out_r = (p1_sample + p2_sample) * 0.5f * s_ducking_factor;
                    break;

                case MODE_STANDARD:
                default:
                    // Volle Mischung beider Ports zum Helm
                    out_l = (p1_sample * 0.8f + p2_sample * 0.2f) * s_ducking_factor;
                    out_r = (p1_sample * 0.2f + p2_sample * 0.8f) * s_ducking_factor;
                    break;
            }

            // Hard Limiting / Clipping Protection
            if (out_l > 32767.0f) out_l = 32767.0f;
            if (out_l < -32768.0f) out_l = -32768.0f;
            if (out_r > 32767.0f) out_r = 32767.0f;
            if (out_r < -32768.0f) out_r = -32768.0f;

            tx_buffer[i * 2] = (int16_t)out_l;
            tx_buffer[i * 2 + 1] = (int16_t)out_r;
        }

        // 4. DMA Schreiboperation zum Audio-Ausgang
        i2s_channel_write(tx_chan, tx_buffer, bytes_read, &bytes_written, pdMS_TO_TICKS(10));
    }
}