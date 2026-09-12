#include "ws2812b_led_manager.h"
#include <math.h>
#include "esp_log.h"
#include "esp_cpu.h"
#include "driver/gpio.h"
#include "esp_rom_sys.h"

static const char* TAG = "WS2812B_LED";

Ws2812bLedManager::Ws2812bLedManager()
    : m_mode(LED_MODE_BREATHING_GREEN),
      m_saved_mode(LED_MODE_BREATHING_GREEN),
      m_timer_ms(0),
      m_flash_remaining_ms(0),
      m_flash_active(false),
      m_current_r(0),
      m_current_g(0),
      m_current_b(0) {}

esp_err_t Ws2812bLedManager::init(void) {
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << PIN_WS2812B_DIN),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_ENABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    esp_err_t err = gpio_config(&io_conf);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to configure WS2812B DIN pin: %d", err);
        return err;
    }

    gpio_set_level(PIN_WS2812B_DIN, 0);
    esp_rom_delay_us(80); // Reset pulse (>50us)

    // Initial state: Off
    transmit_pixel(0, 0, 0);
    ESP_LOGI(TAG, "WS2812B RGB Smart LED initialized on GPIO %d", PIN_WS2812B_DIN);
    return ESP_OK;
}

void Ws2812bLedManager::set_mode(Ws2812bLedMode mode) {
    if (m_mode != mode) {
        m_mode = mode;
        m_timer_ms = 0;
    }
}

void Ws2812bLedManager::trigger_click_flash(void) {
    if (!m_flash_active) {
        m_saved_mode = m_mode;
    }
    m_flash_active = true;
    m_flash_remaining_ms = 150; // 150 ms bright white flash
}

void Ws2812bLedManager::set_color_raw(uint8_t r, uint8_t g, uint8_t b) {
    m_current_r = r;
    m_current_g = g;
    m_current_b = b;
    transmit_pixel(r, g, b);
}

void Ws2812bLedManager::update(uint32_t delta_ms) {
    m_timer_ms += delta_ms;

    // Handle momentary button click flash override
    if (m_flash_active) {
        if (m_flash_remaining_ms > delta_ms) {
            m_flash_remaining_ms -= delta_ms;
            set_color_raw(255, 255, 255); // High-intensity white
            return;
        } else {
            m_flash_active = false;
            m_flash_remaining_ms = 0;
            // Restore previous mode
        }
    }

    uint8_t r = 0, g = 0, b = 0;

    switch (m_mode) {
        case LED_MODE_OFF:
            r = 0; g = 0; b = 0;
            break;

        case LED_MODE_BREATHING_GREEN: {
            // Calm 1 Hz breathing green (0.1 to 1.0 intensity)
            float phase = (m_timer_ms % 1000) / 1000.0f;
            float intensity = 0.15f + 0.85f * (0.5f * (1.0f + sinf(phase * 2.0f * (float)M_PI - (float)M_PI_2)));
            r = 0;
            g = (uint8_t)(intensity * 200.0f);
            b = (uint8_t)(intensity * 25.0f);
            break;
        }

        case LED_MODE_FLASHING_BLUE: {
            // 2 Hz flashing blue for BLE advertising / scanning
            bool on = (m_timer_ms % 500) < 250;
            r = 0;
            g = on ? 40 : 0;
            b = on ? 240 : 0;
            break;
        }

        case LED_MODE_SOLID_YELLOW: {
            // Solid Amber / Yellow during CP2AA Dongle Boot
            r = 240;
            g = 160;
            b = 0;
            break;
        }

        case LED_MODE_FLASHING_RED: {
            // Rapid 4 Hz red flash on VBUS overcurrent fault or reboot pulse
            bool on = (m_timer_ms % 250) < 125;
            r = on ? 255 : 0;
            g = 0;
            b = 0;
            break;
        }

        case LED_MODE_SEARCHING_CYAN: {
            // 2 Hz pulsing cyan while searching for Central Box in unlinked state
            bool on = (m_timer_ms % 500) < 250;
            r = 0;
            g = on ? 180 : 0;
            b = on ? 220 : 0;
            break;
        }

        case LED_MODE_ECALL_STROBE: {
            // Emergency SOS: alternating red and white 10 Hz strobe
            uint32_t step = (m_timer_ms % 200) / 50;
            if (step == 0) { r = 255; g = 0; b = 0; }
            else if (step == 2) { r = 255; g = 255; b = 255; }
            else { r = 0; g = 0; b = 0; }
            break;
        }

        case LED_MODE_RECORDING_RED: {
            // Heartbeat pulse red while Action-Cam is actively recording
            uint32_t beat = m_timer_ms % 1000;
            bool pulse = (beat < 100) || (beat >= 200 && beat < 300);
            r = pulse ? 250 : 25;
            g = 0;
            b = 0;
            break;
        }
    }

    set_color_raw(r, g, b);
}

// -----------------------------------------------------------------------------
// Cycle-accurate bit-bang for WS2812B (GRB 800 kHz protocol)
// -----------------------------------------------------------------------------
void Ws2812bLedManager::transmit_pixel(uint8_t r, uint8_t g, uint8_t b) {
    // WS2812B expects GRB order, MSB first
    uint32_t grb = ((uint32_t)g << 16) | ((uint32_t)r << 8) | ((uint32_t)b);

    // CPU clock cycles calculation for 240 MHz Xtensa LX7
    // Period = 1.25 us = 300 cycles @ 240 MHz
    // T0H = 0.35 us (~84 cycles),  T0L = 0.90 us (~216 cycles)
    // T1H = 0.70 us (~168 cycles), T1L = 0.55 us (~132 cycles)
    const uint32_t c_t0h = 84;
    const uint32_t c_t0l = 216;
    const uint32_t c_t1h = 168;
    const uint32_t c_t1l = 132;

    portMUX_TYPE mux = portMUX_INITIALIZER_UNLOCKED;
    taskENTER_CRITICAL(&mux);

    for (int i = 23; i >= 0; i--) {
        bool bit = (grb >> i) & 0x01;
        uint32_t high_cycles = bit ? c_t1h : c_t0h;
        uint32_t low_cycles  = bit ? c_t1l : c_t0l;

        // Drive HIGH
        gpio_set_level(PIN_WS2812B_DIN, 1);
        uint32_t start = esp_cpu_get_cycle_count();
        while ((esp_cpu_get_cycle_count() - start) < high_cycles) {
            // busy wait
        }

        // Drive LOW
        gpio_set_level(PIN_WS2812B_DIN, 0);
        start = esp_cpu_get_cycle_count();
        while ((esp_cpu_get_cycle_count() - start) < low_cycles) {
            // busy wait
        }
    }

    taskEXIT_CRITICAL(&mux);

    // Latch reset pulse (> 50 us)
    esp_rom_delay_us(60);
}
