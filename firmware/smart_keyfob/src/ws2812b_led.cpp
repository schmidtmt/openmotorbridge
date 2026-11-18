#include "ws2812b_led.h"
#include "keyfob_config.h"
#include <math.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_cpu.h"
#include "driver/gpio.h"
#include "esp_rom_sys.h"

static const char* TAG = "Ws2812bLed";

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
    m_r = r;
    m_g = g;
    m_b = b;

    // WS2812B expects GRB order, MSB first
    uint32_t grb = ((uint32_t)g << 16) | ((uint32_t)r << 8) | ((uint32_t)b);

    // CPU clock cycles calculation for 160 MHz ESP32-C3 RISC-V:
    // Period = 1.25 us = 200 cycles @ 160 MHz
    // T0H = 0.35 us (~56 cycles),  T0L = 0.90 us (~144 cycles)
    // T1H = 0.70 us (~112 cycles), T1L = 0.55 us (~88 cycles)
    const uint32_t c_t0h = 56;
    const uint32_t c_t0l = 144;
    const uint32_t c_t1h = 112;
    const uint32_t c_t1l = 88;

    portMUX_TYPE mux = portMUX_INITIALIZER_UNLOCKED;
    taskENTER_CRITICAL(&mux);

    for (int i = 23; i >= 0; i--) {
        bool bit = (grb >> i) & 0x01;
        uint32_t high_cycles = bit ? c_t1h : c_t0h;
        uint32_t low_cycles  = bit ? c_t1l : c_t0l;

        // Drive HIGH
        gpio_set_level(KEYFOB_PIN_LED_DATA, 1);
        uint32_t start = esp_cpu_get_cycle_count();
        while ((esp_cpu_get_cycle_count() - start) < high_cycles) {
            // busy wait
        }

        // Drive LOW
        gpio_set_level(KEYFOB_PIN_LED_DATA, 0);
        start = esp_cpu_get_cycle_count();
        while ((esp_cpu_get_cycle_count() - start) < low_cycles) {
            // busy wait
        }
    }

    taskEXIT_CRITICAL(&mux);

    // Latch reset pulse (> 50 us)
    esp_rom_delay_us(60);
}

bool Ws2812bLed::init() {
    gpio_config_t io_conf = {};
    io_conf.pin_bit_mask = (1ULL << KEYFOB_PIN_LED_DATA);
    io_conf.mode         = GPIO_MODE_OUTPUT;
    io_conf.pull_up_en   = GPIO_PULLUP_DISABLE;
    io_conf.pull_down_en = GPIO_PULLDOWN_ENABLE;
    io_conf.intr_type    = GPIO_INTR_DISABLE;

    esp_err_t err = gpio_config(&io_conf);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to configure LED_DATA pin: %d", err);
        return false;
    }

    gpio_set_level(KEYFOB_PIN_LED_DATA, 0);
    esp_rom_delay_us(80);

    m_initialized = true;
    transmit_pixel(0, 0, 0);
    ESP_LOGI(TAG, "WS2812B RGB LED initialized on GPIO %d", KEYFOB_PIN_LED_DATA);
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
            // Pulsing amber/yellow when on Qi wireless pad (CHG_STAT active)
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
