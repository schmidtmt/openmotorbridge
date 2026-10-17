#pragma once

#include <stdint.h>
#include <stdbool.h>

typedef enum {
    KEYFOB_LED_OFF,
    KEYFOB_LED_STANDBY_BREATHING_GREEN,
    KEYFOB_LED_ARMED_CYAN,
    KEYFOB_LED_ALARM_STROBE_RED,
    KEYFOB_LED_CHARGING_AMBER,
    KEYFOB_LED_PAIRING_BLUE,
    KEYFOB_LED_SOS_WHITE_RED
} KeyfobLedMode;

class Ws2812bLed {
public:
    static Ws2812bLed& instance();

    bool init();
    void set_mode(KeyfobLedMode mode);
    void set_color(uint8_t r, uint8_t g, uint8_t b);
    void update(uint32_t delta_ms);

private:
    Ws2812bLed();
    void transmit_pixel(uint8_t r, uint8_t g, uint8_t b);

    bool m_initialized;
    KeyfobLedMode m_mode;
    uint32_t m_anim_time_ms;
    uint8_t m_r, m_g, m_b;
};
