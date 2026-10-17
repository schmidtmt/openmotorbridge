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

    void enter_ultra_low_power_sleep();

private:
    KeyfobPowerManager();
    void read_sensors();

    bool m_initialized;
    bool m_is_charging;
    uint16_t m_vbat_mv;
    uint8_t m_battery_pct;
    uint32_t m_poll_timer_ms;
};
