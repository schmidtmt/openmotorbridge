#include "ws2812b_led.h"
#include "keyfob_config.h"
#include <math.h>

Ws2812bLed& Ws2812bLed::instance() {
    static Ws2812bLed s_instance;
    return s_instance;
}

Ws2812bLed::Ws2812bLed()
    : m_initialized(false),
      m_mode(KEYFOB_LED_OFF),
      m_anim_time_ms(0),
      m_r(0), m_g(0), m_b(0) {}

void Ws2812bLed::transmit_pixel(uint8_t r, uint8_t g, uint8_t b) {
    // Hardware NRZ 800 kHz PWM/SPI single-wire stream to KEYFOB_PIN_LED_DATA (Pad L1)
    m_r = r;
    m_g = g;
    m_b = b;
}

bool Ws2812bLed::init() {
    transmit_pixel(0, 0, 0);
    m_initialized = true;
    return true;
}

void Ws2812bLed::set_mode(KeyfobLedMode mode) {
    m_mode = mode;
    m_anim_time_ms = 0;
    if (mode == KEYFOB_LED_OFF) {
        transmit_pixel(0, 0, 0);
    }
}

void Ws2812bLed::set_color(uint8_t r, uint8_t g, uint8_t b) {
    m_mode = KEYFOB_LED_OFF;
    transmit_pixel(r, g, b);
}

void Ws2812bLed::update(uint32_t delta_ms) {
    if (!m_initialized || m_mode == KEYFOB_LED_OFF) return;
    m_anim_time_ms += delta_ms;

    switch (m_mode) {
        case KEYFOB_LED_STANDBY_BREATHING_GREEN: {
            // Gentle breathing green (cycle 2000 ms)
            float phase = (float)(m_anim_time_ms % 2000) / 2000.0f;
            float brightness = 0.5f * (1.0f + sinf(phase * 2.0f * (float)M_PI - (float)M_PI * 0.5f));
            uint8_t g = (uint8_t)(brightness * 120.0f);
            transmit_pixel(0, g, 0);
            break;
        }

        case KEYFOB_LED_ARMED_CYAN: {
            // Pulsing cyan indicator (cycle 1500 ms)
            float phase = (float)(m_anim_time_ms % 1500) / 1500.0f;
            float brightness = 0.5f * (1.0f + sinf(phase * 2.0f * (float)M_PI));
            uint8_t val = (uint8_t)(brightness * 140.0f);
            transmit_pixel(0, val, val);
            break;
        }

        case KEYFOB_LED_ALARM_STROBE_RED: {
            // Fast urgent red strobe (10 Hz = 100 ms period)
            bool on = ((m_anim_time_ms / 50) % 2) == 0;
            transmit_pixel(on ? 255 : 0, 0, 0);
            break;
        }

        case KEYFOB_LED_CHARGING_AMBER: {
            // Pulsing amber/yellow when on Qi wireless pad (Pad K2 CHG_STAT active)
            float phase = (float)(m_anim_time_ms % 1200) / 1200.0f;
            float brightness = 0.3f + 0.7f * 0.5f * (1.0f + sinf(phase * 2.0f * (float)M_PI));
            uint8_t r = (uint8_t)(brightness * 200.0f);
            uint8_t g = (uint8_t)(brightness * 90.0f);
            transmit_pixel(r, g, 0);
            break;
        }

        case KEYFOB_LED_PAIRING_BLUE: {
            // Fast flashing blue (cycle 400 ms)
            bool on = ((m_anim_time_ms / 200) % 2) == 0;
            transmit_pixel(0, 0, on ? 180 : 20);
            break;
        }

        case KEYFOB_LED_SOS_WHITE_RED: {
            // Alternating white / red high-intensity flash
            bool phase = ((m_anim_time_ms / 150) % 2) == 0;
            if (phase) transmit_pixel(255, 255, 255);
            else transmit_pixel(255, 0, 0);
            break;
        }

        case KEYFOB_LED_OFF:
        default:
            transmit_pixel(0, 0, 0);
            break;
    }
}
