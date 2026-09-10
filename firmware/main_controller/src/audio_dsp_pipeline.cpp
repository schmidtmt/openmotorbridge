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

#define SAMPLE_RATE         48000
#define SAMPLE_RATE_HZ      SAMPLE_RATE
#define BUFFER_SAMPLES      128
#define DUCKING_ATTACK      0.05f   // Schneller Ducking-Eintritt (ca. 15 ms)
#define DUCKING_RELEASE     0.002f  // Sanftes Ausblenden (ca. 800 ms)

static i2s_chan_handle_t tx_chan = NULL;
static i2s_chan_handle_t rx_chan = NULL;

static AudioOperationMode s_current_mode = MODE_STANDARD;
static float s_ducking_factor = 1.0f;
static bool s_nav_ducking_active = false;
static bool s_nav_auto_sense_active = false;
static uint32_t s_nav_detect_counter = 0;
static uint32_t s_nav_hold_counter = 0;

static float s_port1_gain = 1.0f;
static float s_port2_gain = 1.0f;

static bool s_transparency_enabled = true;
static float s_transparency_gain = 1.0f; // 0.0 to 1.0
static float s_ambient_sensitivity = 1.0f; // User Gain
static float s_agc_level = 1.0f; // Dynamic Automatic Gain Control

static bool s_radar_alert_active = false;
static uint32_t s_radar_sample_idx = 0;
static uint32_t s_radar_sample_len = 0;
static float s_radar_f1 = 880.0f;
static float s_radar_f2 = 1760.0f;

// -----------------------------------------------------------------------------
// Biquad IIR Filter Definition & Presets (Transposed Direct Form II)
// -----------------------------------------------------------------------------
typedef struct {
    float b0, b1, b2;
    float a1, a2;
    float z1, z2;
} BiquadFilter;

static inline float biquad_process(BiquadFilter *f, float in) {
    float out = f->b0 * in + f->z1;
    f->z1 = f->b1 * in - f->a1 * out + f->z2;
    f->z2 = f->b2 * in - f->a2 * out;
    return out;
}

static void biquad_calc_hpf(BiquadFilter *f, float fc, float fs, float q) {
    if (fc <= 20.0f) {
        // Pass-through / Bypass
        f->b0 = 1.0f; f->b1 = 0.0f; f->b2 = 0.0f;
        f->a1 = 0.0f; f->a2 = 0.0f;
        return;
    }
    float w0 = 2.0f * (float)M_PI * fc / fs;
    float alpha = sinf(w0) / (2.0f * q);
    float cos_w0 = cosf(w0);

    float b0 = (1.0f + cos_w0) * 0.5f;
    float b1 = -(1.0f + cos_w0);
    float b2 = (1.0f + cos_w0) * 0.5f;
    float a0 = 1.0f + alpha;
    float a1 = -2.0f * cos_w0;
    float a2 = 1.0f - alpha;

    f->b0 = b0 / a0;
    f->b1 = b1 / a0;
    f->b2 = b2 / a0;
    f->a1 = a1 / a0;
    f->a2 = a2 / a0;
}

static void biquad_calc_peaking(BiquadFilter *f, float fc, float gain_db, float fs, float q) {
    if (fabsf(gain_db) < 0.05f) {
        // Flat Bypass
        f->b0 = 1.0f; f->b1 = 0.0f; f->b2 = 0.0f;
        f->a1 = 0.0f; f->a2 = 0.0f;
        return;
    }
    float a_lin = powf(10.0f, gain_db / 40.0f);
    float w0 = 2.0f * (float)M_PI * fc / fs;
    float alpha = sinf(w0) / (2.0f * q);
    float cos_w0 = cosf(w0);

    float b0 = 1.0f + alpha * a_lin;
    float b1 = -2.0f * cos_w0;
    float b2 = 1.0f - alpha * a_lin;
    float a0 = 1.0f + alpha / a_lin;
    float a1 = -2.0f * cos_w0;
    float a2 = 1.0f - alpha / a_lin;

    f->b0 = b0 / a0;
    f->b1 = b1 / a0;
    f->b2 = b2 / a0;
    f->a1 = a1 / a0;
    f->a2 = a2 / a0;
}

static HelmetEqPreset s_helmet_eq_preset = HELMET_EQ_INTEGRAL;
static BiquadFilter s_hpf_p1 = {1,0,0,0,0,0,0};
static BiquadFilter s_peak_p1 = {1,0,0,0,0,0,0};
static BiquadFilter s_hpf_p2 = {1,0,0,0,0,0,0};
static BiquadFilter s_peak_p2 = {1,0,0,0,0,0,0};

static void update_helmet_eq_filters(HelmetEqPreset preset) {
    s_helmet_eq_preset = preset;
    float hpf_fc = 120.0f;
    float peak_gain = 3.5f;

    switch (preset) {
        case HELMET_EQ_INTEGRAL:
            hpf_fc = 120.0f;
            peak_gain = 3.5f;
            break;
        case HELMET_EQ_OPEN_FACE:
            hpf_fc = 160.0f;
            peak_gain = 6.0f;
            break;
        case HELMET_EQ_TOURING:
            hpf_fc = 90.0f;
            peak_gain = 2.0f;
            break;
        case HELMET_EQ_FLAT:
        default:
            hpf_fc = 20.0f;
            peak_gain = 0.0f;
            break;
    }

    biquad_calc_hpf(&s_hpf_p1, hpf_fc, SAMPLE_RATE, 0.7071f);
    biquad_calc_peaking(&s_peak_p1, 2500.0f, peak_gain, SAMPLE_RATE, 1.2f);
    biquad_calc_hpf(&s_hpf_p2, hpf_fc, SAMPLE_RATE, 0.7071f);
    biquad_calc_peaking(&s_peak_p2, 2500.0f, peak_gain, SAMPLE_RATE, 1.2f);

    ESP_LOGI(TAG, "Helmet EQ Updated: Preset=%d (HPF=%.1f Hz, 2.5kHz Boost=+%.1f dB)",
             preset, hpf_fc, peak_gain);
}

// -----------------------------------------------------------------------------
// Adaptive VOX Detector & Wind Noise Floor Compensation
// -----------------------------------------------------------------------------
static bool s_vox_enabled = true;
static float s_vox_threshold_dbfs = -32.0f;
static float s_vox_hangover_ms = 400.0f;
static uint32_t s_vox_hangover_samples = (SAMPLE_RATE * 400) / 1000;
static uint32_t s_vox_hangover_counter = 0;
static bool s_vox_active = false;
static float s_front_wind_spl_dba = 65.0f;
static float s_mic_envelope = 0.0f;

void audio_set_vox_config(bool enabled, float threshold_dbfs, float hangover_ms) {
    s_vox_enabled = enabled;
    s_vox_threshold_dbfs = threshold_dbfs;
    s_vox_hangover_ms = hangover_ms;
    s_vox_hangover_samples = (uint32_t)((SAMPLE_RATE * hangover_ms) / 1000.0f);
    ESP_LOGI(TAG, "VOX Config updated: En=%d, Thresh=%.1f dBFS, Hangover=%.0f ms",
             enabled, threshold_dbfs, hangover_ms);
}

bool audio_get_vox_active(void) {
    return s_vox_enabled ? s_vox_active : true;
}

void audio_set_front_wind_noise_spl(float spl_dba) {
    s_front_wind_spl_dba = spl_dba;
}

// -----------------------------------------------------------------------------
// Sidetone Eigenstimmen-Rückführung
// -----------------------------------------------------------------------------
static float s_sidetone_gain_db = -12.0f;
static float s_sidetone_linear = 0.251f; // powf(10.0f, -12/20)

void audio_set_sidetone_gain(float gain_db) {
    s_sidetone_gain_db = gain_db;
    if (gain_db < -35.0f) {
        s_sidetone_linear = 0.0f; // Mute
    } else {
        s_sidetone_linear = powf(10.0f, gain_db / 20.0f);
    }
    ESP_LOGI(TAG, "Sidetone Gain set: %.1f dB (Linear: %.3f)", gain_db, s_sidetone_linear);
}

float audio_get_sidetone_gain(void) {
    return s_sidetone_gain_db;
}

// -----------------------------------------------------------------------------
// Helmet EQ Preset Getters / Setters
// -----------------------------------------------------------------------------
void audio_set_helmet_eq_preset(HelmetEqPreset preset) {
    update_helmet_eq_filters(preset);
}

HelmetEqPreset audio_get_helmet_eq_preset(void) {
    return s_helmet_eq_preset;
}

// -----------------------------------------------------------------------------
// Cross-Intercom Bridge & Anti-Feedback Gate (Port 1 <-> Port 2)
// -----------------------------------------------------------------------------
static bool s_cross_bridge_enabled = true;
static float s_cross_bleed_db = -6.0f;
static float s_cross_bleed_linear = 0.501f; // powf(10.0f, -6/20)
static float s_p2_envelope = 0.0f;

void audio_set_cross_intercom_bridge(bool enabled, float cross_bleed_db) {
    s_cross_bridge_enabled = enabled;
    s_cross_bleed_db = cross_bleed_db;
    s_cross_bleed_linear = powf(10.0f, cross_bleed_db / 20.0f);
    ESP_LOGI(TAG, "Cross-Intercom Bridge: En=%d, Bleed=%.1f dB (Linear: %.3f)",
             enabled, cross_bleed_db, s_cross_bleed_linear);
}

bool audio_get_cross_intercom_bridge(void) {
    return s_cross_bridge_enabled;
}

void audio_trigger_radar_alert(uint8_t threat_level) {
    s_radar_alert_active = true;
    s_radar_sample_idx = 0;
    s_radar_sample_len = (SAMPLE_RATE * 230) / 1000; // 230 ms dual-tone
    if (threat_level >= 2) {
        s_radar_f1 = 987.77f;  // B5
        s_radar_f2 = 1975.53f; // B6 (Critical fast-closing warning)
    } else {
        s_radar_f1 = 880.0f;   // A5
        s_radar_f2 = 1760.0f;  // A6 (Amber approach warning)
    }
    ESP_LOGW(TAG, "🚨 Radar Warning Alert triggered in DSP Pipeline (Threat: %d)", threat_level);
}

esp_err_t audio_dsp_init(void) {
    ESP_LOGI(TAG, "Initializing I2S Standard Master Driver (48 kHz / 16-Bit Stereo)...");

    update_helmet_eq_filters(HELMET_EQ_INTEGRAL);
    audio_set_sidetone_gain(-12.0f);
    audio_set_vox_config(true, -32.0f, 400.0f);

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

void audio_set_ambient_transparency(bool enabled, float speed_kmh, float sensitivity_gain_db) {
    s_transparency_enabled = enabled;
    s_ambient_sensitivity = powf(10.0f, sensitivity_gain_db / 20.0f);

    if (!enabled || speed_kmh > 30.0f) {
        s_transparency_gain = 0.0f; // Full Mute above 30 km/h (Noise Gate)
    } else if (speed_kmh <= 15.0f) {
        s_transparency_gain = 1.0f; // Full transparency 0-15 km/h
    } else {
        // Raised-cosine fade between 15 and 30 km/h
        float norm = (speed_kmh - 15.0f) / 15.0f; // 0.0 to 1.0
        s_transparency_gain = 0.5f * (1.0f + cosf(norm * (float)M_PI));
    }
}

void task_audio_dsp(void *pvParameters) {
    ESP_LOGI(TAG, "Audio DSP Realtime Pipeline Task running on Core 1.");

    int16_t rx_buffer[BUFFER_SAMPLES * 2]; // Interleaved Stereo (L=Port1, R=Port2)
    int16_t tx_buffer[BUFFER_SAMPLES * 2];
    size_t bytes_read = 0;
    size_t bytes_written = 0;

    // Threshold calculation helpers
    const float nav_thresh_linear = 32767.0f * powf(10.0f, -36.0f / 20.0f); // -36 dBFS (~519)
    const float nav_release_linear = 32767.0f * powf(10.0f, -42.0f / 20.0f); // -42 dBFS (~260)
    const uint32_t nav_detect_samples = (SAMPLE_RATE * 50) / 1000; // 50 ms
    const uint32_t nav_hold_samples = (SAMPLE_RATE * 800) / 1000;  // 800 ms

    while (true) {
        // 1. DMA Leseoperation vom Audio-Frontend
        esp_err_t ret = i2s_channel_read(rx_chan, rx_buffer, sizeof(rx_buffer), &bytes_read, pdMS_TO_TICKS(10));
        if (ret != ESP_OK || bytes_read == 0) {
            vTaskDelay(pdMS_TO_TICKS(1));
            continue;
        }

        // Compute dynamic VOX threshold with Knowles MEMS wind noise floor tracking
        // +0.3 dB per dBA exceeding 75 dBA inside/outside helmet
        float wind_boost_db = fmaxf(0.0f, (s_front_wind_spl_dba - 75.0f) * 0.3f);
        float current_vox_thresh_dbfs = s_vox_threshold_dbfs + wind_boost_db;
        float current_vox_thresh_linear = 32767.0f * powf(10.0f, current_vox_thresh_dbfs / 20.0f);

        int samples_count = bytes_read / (sizeof(int16_t) * 2);

        // 2. Audio-Routing, DSP Filtering & Mischmatrix
        for (int i = 0; i < samples_count; i++) {
            float raw_p1 = (float)rx_buffer[i * 2] * s_port1_gain;
            float raw_p2 = (float)rx_buffer[i * 2 + 1] * s_port2_gain;

            // A. Helmet Acoustic Biquad Filtering (HPF + 2.5 kHz Speech Boost)
            float filtered_p1 = biquad_process(&s_peak_p1, biquad_process(&s_hpf_p1, raw_p1));
            float filtered_p2 = biquad_process(&s_peak_p2, biquad_process(&s_hpf_p2, raw_p2));

            // B. Adaptive VOX Voice Activity Detection on Port 1
            float abs_p1 = fabsf(filtered_p1);
            if (abs_p1 > s_mic_envelope) {
                s_mic_envelope += 0.08f * (abs_p1 - s_mic_envelope); // Fast attack (1-2 ms)
            } else {
                s_mic_envelope += 0.0008f * (abs_p1 - s_mic_envelope); // Slow release
            }

            if (s_vox_enabled) {
                if (s_mic_envelope > current_vox_thresh_linear) {
                    s_vox_active = true;
                    s_vox_hangover_counter = s_vox_hangover_samples;
                } else {
                    if (s_vox_hangover_counter > 0) {
                        s_vox_hangover_counter--;
                        s_vox_active = true;
                    } else {
                        s_vox_active = false;
                    }
                }
            } else {
                s_vox_active = true; // Always active if VOX is disabled (PTT-only or open mic)
            }

            // C. Envelope tracker on Port 2 (Cross-Intercom detection)
            float abs_p2 = fabsf(filtered_p2);
            if (abs_p2 > s_p2_envelope) {
                s_p2_envelope += 0.08f * (abs_p2 - s_p2_envelope);
            } else {
                s_p2_envelope += 0.0008f * (abs_p2 - s_p2_envelope);
            }

            // D. Automatic Navigation Audio Sensing (e.g. Garmin Line-In on Port 2 Aux)
            if (abs_p2 > nav_thresh_linear) {
                if (s_nav_detect_counter < nav_detect_samples) {
                    s_nav_detect_counter++;
                } else {
                    s_nav_auto_sense_active = true;
                    s_nav_hold_counter = nav_hold_samples;
                }
            } else if (abs_p2 < nav_release_linear) {
                s_nav_detect_counter = 0;
                if (s_nav_hold_counter > 0) {
                    s_nav_hold_counter--;
                } else {
                    s_nav_auto_sense_active = false;
                }
            }

            // E. Cross-Intercom Bridge Anti-Feedback Loopback Suppression (-24 dB = 0.063f)
            float p1_to_p2_bleed = filtered_p1 * s_cross_bleed_linear;
            float p2_to_p1_bleed = filtered_p2 * s_cross_bleed_linear;

            if (s_cross_bridge_enabled) {
                // If Port 1 rider is actively speaking, heavily attenuate Port 2 -> Port 1 loopback
                if (s_vox_active) {
                    p2_to_p1_bleed *= 0.063f; // -24 dB anti-feedback suppression
                }
                // If Port 2 passenger is speaking loudly, attenuate Port 1 -> Port 2 loopback
                if (s_p2_envelope > current_vox_thresh_linear) {
                    p1_to_p2_bleed *= 0.063f; // -24 dB anti-feedback suppression
                }
            } else {
                p1_to_p2_bleed = 0.0f;
                p2_to_p1_bleed = 0.0f;
            }

            // F. Sidetone Feedback (Rider Mic -> Rider Earphones)
            float sidetone_signal = 0.0f;
            if (s_sidetone_linear > 0.001f && s_vox_active) {
                sidetone_signal = filtered_p1 * s_sidetone_linear;
            }

            // G. Ducking Engine State Machine
            bool nav_active = s_nav_ducking_active || s_nav_auto_sense_active;
            if (s_radar_alert_active) {
                // Priorität 1: Sofortiges Absenken auf -18 dB (0.125f) bei Annäherungsgefahr
                if (s_ducking_factor > 0.125f) {
                    s_ducking_factor -= (DUCKING_ATTACK * 2.5f);
                    if (s_ducking_factor < 0.125f) s_ducking_factor = 0.125f;
                }
            } else if (nav_active) {
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

            // H. Ambient Microphone Input Processing with AGC (v <= 30 km/h)
            float ambient_mix = 0.0f;
            if (s_transparency_enabled && s_transparency_gain > 0.001f) {
                float raw_amb = (raw_p1 + raw_p2) * 0.15f * s_ambient_sensitivity;
                float abs_amb = fabsf(raw_amb);

                if (abs_amb > s_agc_level) {
                    s_agc_level += 0.1f * (abs_amb - s_agc_level); // Fast attack
                } else {
                    s_agc_level += 0.0005f * (abs_amb - s_agc_level); // Slow decay
                }

                float agc_scaler = 1.0f;
                if (s_agc_level > 16384.0f) { // Above -6 dBFS
                    agc_scaler = 16384.0f / s_agc_level;
                }
                ambient_mix = raw_amb * agc_scaler * s_transparency_gain;
            }

            // I. Synthesize Radar Dual-Tone Warning Ping
            float radar_chime = 0.0f;
            if (s_radar_alert_active) {
                float t_sec = (float)s_radar_sample_idx / (float)SAMPLE_RATE;
                if (t_sec < 0.10f) {
                    radar_chime = sinf(2.0f * (float)M_PI * s_radar_f1 * t_sec) * 12000.0f;
                } else if (t_sec >= 0.13f && t_sec < 0.23f) {
                    radar_chime = sinf(2.0f * (float)M_PI * s_radar_f2 * (t_sec - 0.13f)) * 14000.0f;
                }
                s_radar_sample_idx++;
                if (s_radar_sample_idx >= s_radar_sample_len) {
                    s_radar_alert_active = false;
                }
            }

            // J. Audio Output Routing to Rider Helmet (Tx L/R)
            float out_l = 0.0f;
            float out_r = 0.0f;

            switch (s_current_mode) {
                case MODE_SINGLE_RIDER:
                    // Port 2 stumm, nur Port 1 + Sidetone + Ambient + Radar Chime
                    out_l = (filtered_p1 * s_ducking_factor) + sidetone_signal + ambient_mix + radar_chime;
                    out_r = (filtered_p1 * s_ducking_factor) + sidetone_signal + ambient_mix + radar_chime;
                    break;

                case MODE_CRUISE:
                    // Fokus auf Bordlautsprecher, Intercom -6 dB + Radar Chime
                    out_l = ((filtered_p1 + filtered_p2 + p2_to_p1_bleed) * 0.5f * s_ducking_factor) + (ambient_mix * 0.5f) + sidetone_signal + radar_chime;
                    out_r = ((filtered_p1 + filtered_p2 + p1_to_p2_bleed) * 0.5f * s_ducking_factor) + (ambient_mix * 0.5f) + sidetone_signal + radar_chime;
                    break;

                case MODE_STANDARD:
                default:
                    // Volle Mischung beider Ports zum Helm + Cross-Bleed + Sidetone + Ambient + Radar
                    out_l = ((filtered_p1 * 0.8f + filtered_p2 * 0.2f + p2_to_p1_bleed) * s_ducking_factor) + sidetone_signal + ambient_mix + radar_chime;
                    out_r = ((filtered_p1 * 0.2f + filtered_p2 * 0.8f + p1_to_p2_bleed) * s_ducking_factor) + sidetone_signal + ambient_mix + radar_chime;
                    break;
            }

            // K. Soft-Knee Peak Limiting / Brickwall Overdrive Protection
            if (out_l > 30000.0f) {
                out_l = 30000.0f + tanhf((out_l - 30000.0f) / 5000.0f) * 2767.0f;
            } else if (out_l < -30000.0f) {
                out_l = -30000.0f + tanhf((out_l + 30000.0f) / 5000.0f) * 2768.0f;
            }

            if (out_r > 30000.0f) {
                out_r = 30000.0f + tanhf((out_r - 30000.0f) / 5000.0f) * 2767.0f;
            } else if (out_r < -30000.0f) {
                out_r = -30000.0f + tanhf((out_r + 30000.0f) / 5000.0f) * 2768.0f;
            }

            tx_buffer[i * 2] = (int16_t)out_l;
            tx_buffer[i * 2 + 1] = (int16_t)out_r;
        }

        // 3. DMA Schreiboperation zum Audio-Ausgang
        i2s_channel_write(tx_chan, tx_buffer, bytes_read, &bytes_written, pdMS_TO_TICKS(10));
    }
}