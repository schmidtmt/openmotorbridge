#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"
#include "front_node_config.h"

// Animation Modes for the Onboard WS2812B RGB Smart LED
enum Ws2812bLedMode : uint8_t {
    LED_MODE_OFF = 0,
    LED_MODE_BREATHING_GREEN,  // Normal operation, linked to Central Box (1 Hz)
    LED_MODE_FLASHING_BLUE,    // BLE Pairing / Camera Scanning active (2 Hz)
    LED_MODE_SOLID_YELLOW,     // CP2AA Wireless CarPlay/AA Dongle Booting
    LED_MODE_FLASHING_RED,     // Hardware Fault / VBUS Overcurrent / Kaltstart (4 Hz)
    LED_MODE_SEARCHING_CYAN,   // Unpaired / Proximity Discovery mode (2 Hz)
    LED_MODE_ECALL_STROBE,     // Rapid Red / White Strobe for Emergency SOS
    LED_MODE_RECORDING_RED     // Pulsing red during active Action-Cam recording
};

class Ws2812bLedManager {
public:
    static Ws2812bLedManager& instance() {
        static Ws2812bLedManager s_instance;
        return s_instance;
    }

    esp_err_t init(void);
    void set_mode(Ws2812bLedMode mode);
    Ws2812bLedMode get_mode(void) const { return m_mode; }

    void trigger_click_flash(void); // Momentary white flash for 150 ms
    void update(uint32_t delta_ms); // Call at 20-50 Hz from supervisor task

    void set_color_raw(uint8_t r, uint8_t g, uint8_t b);

private:
    Ws2812bLedManager();
    ~Ws2812bLedManager() = default;

    Ws2812bLedManager(const Ws2812bLedManager&) = delete;
    Ws2812bLedManager& operator=(const Ws2812bLedManager&) = delete;

    void transmit_pixel(uint8_t r, uint8_t g, uint8_t b);

    Ws2812bLedMode m_mode;
    Ws2812bLedMode m_saved_mode;
    uint32_t m_timer_ms;
    uint32_t m_flash_remaining_ms;
    bool m_flash_active;
    uint8_t m_current_r;
    uint8_t m_current_g;
    uint8_t m_current_b;
};
