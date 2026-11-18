#pragma once

#include <stdint.h>
#include <stdbool.h>

class KeyfobPowerManager {
public:
    static KeyfobPowerManager& instance();

    bool init();
    void update(uint32_t delta_ms);

    bool is_charging() const;
    uint16_t get_battery_voltage_mv() const;
    uint8_t get_battery_percentage() const;
    bool is_low_battery() const;

    void enter_light_sleep(uint32_t sleep_time_ms);
    void enter_deep_sleep();

private:
    KeyfobPowerManager();
    void read_sensors();
    void configure_sleep_wakeups();

    bool m_initialized;
    bool m_is_charging;
    uint16_t m_vbat_mv;
    uint8_t m_battery_pct;
    uint32_t m_poll_timer_ms;
};
