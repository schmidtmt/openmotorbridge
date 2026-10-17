#include "buzzer_driver.h"
#include "keyfob_config.h"

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
    if (freq_hz == 0 || duty_percent == 0) {
        // Stop PWM output on KEYFOB_PIN_BUZZER_PWM (Pad F2)
        return;
    }
    // Set hardware timer PWM frequency and 50% duty cycle on Pad F2
}

bool BuzzerDriver::init() {
    set_pwm(0, 0);
    m_initialized = true;
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
            play_tone(2400, 60);
            break;

        case BUZZER_PATTERN_ALARM_SIREN:
            set_pwm(KEYFOB_BUZZER_FREQ_ALARM, 50);
            break;

        case BUZZER_PATTERN_SOS_MORSE:
            play_tone(3000, 150);
            break;

        case BUZZER_PATTERN_BATTERY_WARN:
            play_tone(1800, 200);
            break;

        case BUZZER_PATTERN_OFF:
        default:
            stop();
            break;
    }
}

void BuzzerDriver::stop() {
    set_pwm(0, 0);
    m_current_pattern = BUZZER_PATTERN_OFF;
    m_tone_active = false;
    m_elapsed_ms = 0;
}

void BuzzerDriver::update(uint32_t delta_ms) {
    if (!m_tone_active) return;
    m_elapsed_ms += delta_ms;

    if (m_current_pattern == BUZZER_PATTERN_CONFIRM_CHIRP ||
        m_current_pattern == BUZZER_PATTERN_DISARM_CHIRP ||
        m_current_pattern == BUZZER_PATTERN_BATTERY_WARN) {
        if (m_elapsed_ms >= m_tone_duration_ms) {
            stop();
        }
    } else if (m_current_pattern == BUZZER_PATTERN_ALARM_SIREN) {
        // Siren frequency modulation (2.7 kHz <-> 4.0 kHz every 250 ms)
        uint32_t cycle = (m_elapsed_ms / 250) % 2;
        set_pwm(cycle == 0 ? KEYFOB_BUZZER_FREQ_ALARM : KEYFOB_BUZZER_FREQ_ARM, 50);
    } else if (m_current_pattern == BUZZER_PATTERN_SOS_MORSE) {
        // Morse SOS timing
        uint32_t mod = m_elapsed_ms % 2000;
        if (mod < 200 || (mod >= 300 && mod < 500) || (mod >= 600 && mod < 800)) {
            set_pwm(3000, 50); // S (. . .)
        } else if ((mod >= 900 && mod < 1200) || (mod >= 1300 && mod < 1600) || (mod >= 1700 && mod < 2000)) {
            set_pwm(2500, 50); // O (- - -)
        } else {
            set_pwm(0, 0);
        }
    }
}

bool BuzzerDriver::is_playing() const {
    return m_tone_active;
}
