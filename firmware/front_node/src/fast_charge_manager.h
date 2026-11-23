#pragma once

#include <stdbool.h>
#include <stdint.h>
#include "usb_backbone_types.h"

#ifdef __cplusplus
extern "C" {
#endif

// Fast Charging & Wireless Qi States (PCBA 05 J4 Glovebox Feed)
enum FastChargeState : uint8_t {
    FAST_CHARGE_STATE_OFF            = 0,
    FAST_CHARGE_STATE_STANDBY        = 1,
    FAST_CHARGE_STATE_CHARGING       = 2,
    FAST_CHARGE_STATE_FAST_CHARGING  = 3, // 15W Qi or 30W USB-PD
    FAST_CHARGE_STATE_REBOOTING      = 4,
    FAST_CHARGE_STATE_FAULT          = 5, // Overcurrent / Short
    FAST_CHARGE_STATE_THERMAL_THROTTLE = 6, // Temperature > 55 deg C
    FAST_CHARGE_STATE_CAFE_COUNTDOWN = 7  // Post-KL15 60s Grace Period
};

#ifdef __cplusplus
}

class FastChargeManager {
public:
    static FastChargeManager& instance();

    bool init();
    void update();

    // Control Commands
    void set_power(bool enable);
    void trigger_hard_reset();
    void set_ignition(bool ignition_on);
    void pause_charging(uint32_t duration_ms);

    // Status Queries & Telemetry
    FastChargeState get_state() const;
    bool is_power_on() const;
    bool has_fault() const;
    uint32_t get_cafe_remaining_sec() const;
    
    // I2C Measurements (SW3526 Controller)
    uint16_t get_vbus_mv() const { return m_vbus_mv; }
    uint16_t get_current_ma() const { return m_current_ma; }
    uint16_t get_power_mw() const { return (uint32_t)m_vbus_mv * m_current_ma / 1000; }
    int16_t  get_temperature_c_10() const { return m_temp_c_10; }
    uint8_t  get_qi_state() const { return m_qi_state; }
    uint8_t  get_pd_profile() const { return m_pd_profile; }

    // Generates Backbone Telemetry Packet (COMM_23 / 0x05)
    void get_telemetry_packet(UsbPowerDeliveryStatPkt* pkt) const;

private:
    FastChargeManager();

    FastChargeState m_state;
    bool m_power_enabled;
    bool m_fault_detected;
    bool m_ignition_active;

    uint16_t m_vbus_mv;
    uint16_t m_current_ma;
    int16_t  m_temp_c_10;
    uint8_t  m_qi_state;
    uint8_t  m_pd_profile;

    uint64_t m_reset_start_us;
    uint64_t m_cafe_timer_start_us;
    uint64_t m_pause_until_us;
    uint64_t m_last_i2c_poll_us;

    void poll_sw3526_i2c();
};

// Backward Compatibility Aliases for OttocastPowerManager
typedef FastChargeManager OttocastPowerManager;
typedef FastChargeState   OttocastState;
#define OTTOCAST_STATE_OFF            FAST_CHARGE_STATE_OFF
#define OTTOCAST_STATE_ACTIVE         FAST_CHARGE_STATE_CHARGING
#define OTTOCAST_STATE_REBOOTING      FAST_CHARGE_STATE_REBOOTING
#define OTTOCAST_STATE_FAULT          FAST_CHARGE_STATE_FAULT
#define OTTOCAST_STATE_CAFE_COUNTDOWN FAST_CHARGE_STATE_CAFE_COUNTDOWN

#endif
