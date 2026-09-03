#pragma once

#include <stdbool.h>
#include <stdint.h>

enum OttocastState : uint8_t {
    OTTOCAST_STATE_OFF            = 0,
    OTTOCAST_STATE_ACTIVE         = 1,
    OTTOCAST_STATE_REBOOTING      = 2,
    OTTOCAST_STATE_FAULT          = 3,
    OTTOCAST_STATE_CAFE_COUNTDOWN = 4
};

class OttocastPowerManager {
public:
    static OttocastPowerManager& instance();

    bool init();
    void update();

    // Control Commands
    void set_power(bool enable);
    void trigger_hard_reset();
    void set_ignition(bool ignition_on);
    void pause_for_usb_host_arbitration(uint32_t duration_ms);

    // Status Queries
    OttocastState get_state() const;
    bool is_power_on() const;
    bool has_fault() const;
    uint32_t get_cafe_remaining_sec() const;

private:
    OttocastPowerManager();

    OttocastState m_state;
    bool m_power_enabled;
    bool m_fault_detected;
    bool m_ignition_active;

    uint64_t m_reset_start_us;
    uint64_t m_cafe_timer_start_us;
    uint64_t m_arbitration_until_us;
};
