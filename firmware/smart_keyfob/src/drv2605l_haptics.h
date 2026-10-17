#pragma once

#include <stdint.h>
#include <stdbool.h>

typedef enum {
    HAPTIC_CLICK_CONFIRM,   // Short crisp click (e.g. Arm Bike)
    HAPTIC_CLICK_DISARM,    // Soft click (e.g. Disarm Bike)
    HAPTIC_ALARM_PULSE,     // Heavy pulsing vibration (Silent Pager Alarm)
    HAPTIC_SOS_PANIC,       // Triple urgent vibration (SOS Beacon)
    HAPTIC_BATTERY_LOW      // Low-frequency warning rumble
} KeyfobHapticEffect;

class Drv2605lHaptics {
public:
    static Drv2605lHaptics& instance();

    bool init();
    void play_effect(KeyfobHapticEffect effect);
    void stop();
    void set_enabled(bool enable);
    bool is_busy() const;

private:
    Drv2605lHaptics();
    bool write_register(uint8_t reg, uint8_t val);
    uint8_t read_register(uint8_t reg);

    bool m_initialized;
    bool m_busy;
};
