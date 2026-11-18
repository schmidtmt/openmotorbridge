#include "buzzer_driver.h"
#include "keyfob_config.h"
#include "driver/ledc.h"
#include "esp_log.h"

static const char* TAG = "BuzzerDriver";

#define BUZZER_LEDC_TIMER       LEDC_TIMER_0
#define BUZZER_LEDC_MODE        LEDC_LOW_SPEED_MODE
#define BUZZER_LEDC_CHANNEL     LEDC_CHANNEL_0
#define BUZZER_LEDC_DUTY_RES    LEDC_TIMER_10_BIT

BuzzerDriver& BuzzerDriver::instance() {
    static BuzzerDriver s_instance;
    return s_instance;
}

BuzzerDriver::BuzzerDriver()
    : m_initialized(false),
      m_current_pattern(BUZZER_PATTERN_OFF),
      m_elapsed_ms(0),
      m_tone_duration_ms(0),
      m_tone_active(false) {}

void BuzzerDriver::set_pwm(uint16_t freq_hz, uint8_t duty_percent) {
    if (!m_initialized) return;

    if (freq_hz == 0 || duty_percent == 0) {
        ledc_stop(BUZZER_LEDC_MODE, BUZZER_LEDC_CHANNEL, 0);
        return;
    }

    ledc_set_freq(BUZZER_LEDC_MODE, BUZZER_LEDC_TIMER, freq_hz);
    // 10-bit duty resolution (0..1023)
    uint32_t duty = (1023 * duty_percent) / 100;
    ledc_set_duty(BUZZER_LEDC_MODE, BUZZER_LEDC_CHANNEL, duty);
    ledc_update_duty(BUZZER_LEDC_MODE, BUZZER_LEDC_CHANNEL);
}

bool BuzzerDriver::init() {
    ledc_timer_config_t timer_conf = {};
    timer_conf.speed_mode       = BUZZER_LEDC_MODE;
    timer_conf.duty_resolution  = BUZZER_LEDC_DUTY_RES;
    timer_conf.timer_num        = BUZZER_LEDC_TIMER;
    timer_conf.freq_hz          = KEYFOB_BUZZER_FREQ_ARM;
    timer_conf.clk_cfg          = LEDC_AUTO_CLK;

    if (ledc_timer_config(&timer_conf) != ESP_OK) {
        ESP_LOGE(TAG, "LEDC timer config failed");
        return false;
    }

    ledc_channel_config_t ch_conf = {};
    ch_conf.gpio_num   = KEYFOB_PIN_BUZZER_PWM;
    ch_conf.speed_mode = BUZZER_LEDC_MODE;
    ch_conf.channel    = BUZZER_LEDC_CHANNEL;
    ch_conf.intr_type  = LEDC_INTR_DISABLE;
    ch_conf.timer_sel  = BUZZER_LEDC_TIMER;
    ch_conf.duty       = 0;
    ch_conf.hpoint     = 0;

    if (ledc_channel_config(&ch_conf) != ESP_OK) {
        ESP_LOGE(TAG, "LEDC channel config failed");
        return false;
    }

    m_initialized = true;
    set_pwm(0, 0);
    ESP_LOGI(TAG, "Buzzer initialized on GPIO %d", KEYFOB_PIN_BUZZER_PWM);
    return true;
}

void BuzzerDriver::play_tone(uint16_t freq_hz, uint16_t duration_ms) {
    if (!m_initialized) return;
    m_tone_duration_ms = duration_ms;
    m_elapsed_ms = 0;
    m_tone_active = true;
    set_pwm(freq_hz, 50);
}

void BuzzerDriver::play_pattern(KeyfobBuzzerPattern pattern) {
    if (!m_initialized) return;
    m_current_pattern = pattern;
    m_elapsed_ms = 0;
    m_tone_active = true;

    switch (pattern) {
        case BUZZER_PATTERN_CONFIRM_CHIRP:
            play_tone(KEYFOB_BUZZER_FREQ_ARM, 80);
            break;

        case BUZZER_PATTERN_DISARM_CHIRP:
            play_tone(KEYFOB_BUZZER_FREQ_DISARM, 60);
            break;

        case BUZZER_PATTERN_BATTERY_WARN:
            play_tone(1800, 150);
            break;

        case BUZZER_PATTERN_ALARM_SIREN:
        case BUZZER_PATTERN_SOS_MORSE:
            // Handled dynamically in update()
            break;

        case BUZZER_PATTERN_OFF:
        default:
            stop();
            break;
    }
}

void BuzzerDriver::stop() {
    m_tone_active = false;
    m_current_pattern = BUZZER_PATTERN_OFF;
    set_pwm(0, 0);
}

bool BuzzerDriver::is_playing() const {
    return m_tone_active;
}

void BuzzerDriver::update(uint32_t delta_ms) {
    if (!m_initialized || !m_tone_active) return;
    m_elapsed_ms += delta_ms;

    // Fixed duration tone check
    if (m_current_pattern == BUZZER_PATTERN_OFF ||
        m_current_pattern == BUZZER_PATTERN_CONFIRM_CHIRP ||
        m_current_pattern == BUZZER_PATTERN_BATTERY_WARN) {
        if (m_elapsed_ms >= m_tone_duration_ms) {
            stop();
        }
        return;
    }

    // Pattern: DISARM dual-chirp
    if (m_current_pattern == BUZZER_PATTERN_DISARM_CHIRP) {
        if (m_elapsed_ms < 60) {
            set_pwm(KEYFOB_BUZZER_FREQ_DISARM, 50);
        } else if (m_elapsed_ms < 110) {
            set_pwm(0, 0);
        } else if (m_elapsed_ms < 170) {
            set_pwm(KEYFOB_BUZZER_FREQ_DISARM - 200, 50);
        } else {
            stop();
        }
        return;
    }

    // Pattern: High penetration alternating ALARM siren (2.7 kHz <-> 4.0 kHz)
    if (m_current_pattern == BUZZER_PATTERN_ALARM_SIREN) {
        uint32_t cycle = m_elapsed_ms % 400; // 400 ms period
        if (cycle < 200) {
            set_pwm(KEYFOB_BUZZER_FREQ_ARM, 50);
        } else {
            set_pwm(KEYFOB_BUZZER_FREQ_ALARM, 50);
        }
        return;
    }

    // Pattern: SOS Morse code (... --- ...)
    if (m_current_pattern == BUZZER_PATTERN_SOS_MORSE) {
        uint32_t t = m_elapsed_ms % 2800;
        bool beep = false;
        // 3 short (100 on, 100 off)
        if (t < 100 || (t >= 200 && t < 300) || (t >= 400 && t < 500)) beep = true;
        // 3 long (300 on, 100 off)
        else if ((t >= 700 && t < 1000) || (t >= 1100 && t < 1400) || (t >= 1500 && t < 1800)) beep = true;
        // 3 short (100 on, 100 off)
        else if ((t >= 2000 && t < 2100) || (t >= 2200 && t < 2300) || (t >= 2400 && t < 2500)) beep = true;

        set_pwm(beep ? KEYFOB_BUZZER_FREQ_ALARM : 0, beep ? 50 : 0);
    }
}
