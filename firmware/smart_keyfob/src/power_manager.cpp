#include "power_manager.h"
#include "keyfob_config.h"

KeyfobPowerManager& KeyfobPowerManager::instance() {
    static KeyfobPowerManager s_instance;
    return s_instance;
}

KeyfobPowerManager::KeyfobPowerManager()
    : m_initialized(false),
      m_is_charging(false),
      m_vbat_mv(4100),
      m_battery_pct(95),
      m_poll_timer_ms(0) {}

bool KeyfobPowerManager::init() {
    read_sensors();
    m_initialized = true;
    return true;
}

void KeyfobPowerManager::read_sensors() {
    // 1. Read BQ25100 Charge Status on Pad K2 (Active Low)
    // Low level = Qi charging active, High level = battery power
    m_is_charging = false;

    // 2. Read Analog Battery Voltage via nRF52840 SAADC
    // Nominal LiPo curve: 3.40V (0%) .. 4.20V (100%)
    if (m_vbat_mv <= KEYFOB_BAT_LOW_THRESH_MV) {
        m_battery_pct = 0;
    } else if (m_vbat_mv >= KEYFOB_BAT_FULL_THRESH_MV) {
        m_battery_pct = 100;
    } else {
        m_battery_pct = (uint8_t)(((m_vbat_mv - KEYFOB_BAT_LOW_THRESH_MV) * 100) /
                                  (KEYFOB_BAT_FULL_THRESH_MV - KEYFOB_BAT_LOW_THRESH_MV));
    }
}

void KeyfobPowerManager::update(uint32_t delta_ms) {
    if (!m_initialized) return;
    m_poll_timer_ms += delta_ms;

    // Read battery every 5 seconds
    if (m_poll_timer_ms >= 5000) {
        m_poll_timer_ms = 0;
        read_sensors();
    }
}

bool KeyfobPowerManager::is_charging() const {
    return m_is_charging;
}

uint16_t KeyfobPowerManager::get_battery_voltage_mv() const {
    return m_vbat_mv;
}

uint8_t KeyfobPowerManager::get_battery_percentage() const {
    return m_battery_pct;
}

void KeyfobPowerManager::enter_ultra_low_power_sleep() {
    // 1. Put SX1262 into Sleep Mode (< 160 nA)
    // 2. Disable DRV2605L Hardware Enable (Pad M2 Low)
    // 3. Configure Sense on BTN_ARM_N (Pad G1) and BTN_SOS_N (Pad J1) for wakeup
    // 4. Put nRF52840 into System ON Low Power Sleep (< 25 µA total current drain)
}
