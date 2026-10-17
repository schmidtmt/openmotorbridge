#pragma once

#include <stdint.h>
#include <stdbool.h>

typedef enum {
    BUZZER_PATTERN_OFF,
    BUZZER_PATTERN_CONFIRM_CHIRP,  // Single crisp 2.7 kHz chirp
    BUZZER_PATTERN_DISARM_CHIRP,   // Dual gentle 2.4 kHz chirp
    BUZZER_PATTERN_ALARM_SIREN,    // High penetration alternating 2.7 kHz / 4.0 kHz siren
    BUZZER_PATTERN_SOS_MORSE,      // ... --- ... emergency acoustic beacon
    BUZZER_PATTERN_BATTERY_WARN    // Low acoustic beep
} KeyfobBuzzerPattern;

class BuzzerDriver {
public:
    static BuzzerDriver& instance();

    bool init();
    void play_pattern(KeyfobBuzzerPattern pattern);
    void play_tone(uint16_t freq_hz, uint16_t duration_ms);
    void stop();
    void update(uint32_t delta_ms);
    bool is_playing() const;

private:
    BuzzerDriver();
    void set_pwm(uint16_t freq_hz, uint8_t duty_percent);

    bool m_initialized;
    KeyfobBuzzerPattern m_current_pattern;
    uint32_t m_elapsed_ms;
    uint16_t m_tone_duration_ms;
    bool m_tone_active;
};
