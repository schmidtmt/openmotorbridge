#include "fast_charge_manager.h"
#include "front_node_config.h"
#include "esp_timer.h"
#include "esp_log.h"
#include "driver/gpio.h"
#include "driver/i2c.h"

static const char* TAG = "FAST_CHARGE_MGR";

FastChargeManager& FastChargeManager::instance() {
    static FastChargeManager inst;
    return inst;
}

FastChargeManager::FastChargeManager()
    : m_state(FAST_CHARGE_STATE_OFF)
    , m_power_enabled(false)
    , m_fault_detected(false)
    , m_ignition_active(true)
    , m_vbus_mv(5000)
    , m_current_ma(0)
    , m_temp_c_10(250)
    , m_qi_state(0)
    , m_pd_profile(0)
    , m_reset_start_us(0)
    , m_cafe_timer_start_us(0)
    , m_pause_until_us(0)
    , m_last_i2c_poll_us(0)
{
}

bool FastChargeManager::init() {
    // 1. Configure Power Enable Pin (GPIO57, Output, Active-High)
    gpio_config_t en_conf = {
        .pin_bit_mask = (1ULL << PIN_FAST_CHARGE_EN),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_ENABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&en_conf);
    gpio_set_level(PIN_FAST_CHARGE_EN, 0); // Start OFF

    // 2. Configure Fault Alert Pin (GPIO56, Input, Active-Low)
    gpio_config_t fault_conf = {
        .pin_bit_mask = (1ULL << PIN_FAST_CHARGE_FAULT_N),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE, // Open-Drain interrupt
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&fault_conf);

    // Initial power-up
    set_power(true);
    ESP_LOGI(TAG, "Fast charge manager initialized (SW3526 30W USB-PD & 15W Qi-Puck at J4). Initial state: STANDBY");
    return true;
}

void FastChargeManager::set_power(bool enable) {
    if (enable && m_fault_detected) {
        ESP_LOGW(TAG, "Cannot enable VBUS: Overcurrent / short fault condition persists!");
        return;
    }

    m_power_enabled = enable;
    gpio_set_level(PIN_FAST_CHARGE_EN, enable ? 1 : 0);
    m_state = enable ? FAST_CHARGE_STATE_STANDBY : FAST_CHARGE_STATE_OFF;
    ESP_LOGI(TAG, "Glovebox J4 fast charge power %s", enable ? "ENABLED (+VBUS ON)" : "DISABLED (0V OFF)");
}

void FastChargeManager::trigger_hard_reset() {
    ESP_LOGW(TAG, "1-Click Hard Reset triggered! Power-cycling glovebox fast charger for %d ms...", OTTOCAST_RESET_PULSE_MS);
    gpio_set_level(PIN_FAST_CHARGE_EN, 0);
    m_state = FAST_CHARGE_STATE_REBOOTING;
    m_reset_start_us = esp_timer_get_time();
}

void FastChargeManager::set_ignition(bool ignition_on) {
    if (m_ignition_active == ignition_on) return;
    m_ignition_active = ignition_on;

    if (!ignition_on) {
        ESP_LOGI(TAG, "Ignition OFF detected. Starting %d-second charging grace period...", CAFE_DISCONNECT_SEC);
        m_state = FAST_CHARGE_STATE_CAFE_COUNTDOWN;
        m_cafe_timer_start_us = esp_timer_get_time();
    } else {
        ESP_LOGI(TAG, "Ignition ON detected. Restoring active fast charge operation.");
        m_cafe_timer_start_us = 0;
        set_power(true);
    }
}

void FastChargeManager::pause_charging(uint32_t duration_ms) {
    ESP_LOGI(TAG, "Pausing fast charging for %lu ms (thermal / power negotiation)", duration_ms);
    gpio_set_level(PIN_FAST_CHARGE_EN, 0);
    m_pause_until_us = esp_timer_get_time() + (duration_ms * 1000ULL);
}

void FastChargeManager::poll_sw3526_i2c() {
    // In production hardware, read SW3526 registers over I2C (SW3526_I2C_ADDR = 0x3C):
    // Reg 0x01: Output Voltage (mV)
    // Reg 0x02: Output Current (mA)
    // Reg 0x03: Die / NTC Temperature
    // Reg 0x04: Fast Charge Protocol (0x01=QC2, 0x02=QC3, 0x04=PD, 0x08=PPS, 0x10=Qi)
    
    // Default simulated / normal baseline:
    if (m_power_enabled) {
        if (m_current_ma > 1800) {
            m_state = FAST_CHARGE_STATE_FAST_CHARGING;
            m_qi_state = 2; // Fast charging
            m_pd_profile = 2; // 12V / 2.5A or 9V / 3A
        } else if (m_current_ma > 100) {
            m_state = FAST_CHARGE_STATE_CHARGING;
            m_qi_state = 1; // Standard charging
            m_pd_profile = 0; // 5V / 3A
        } else {
            m_state = FAST_CHARGE_STATE_STANDBY;
            m_qi_state = 0; // Idle
        }

        // Thermal protection check (> 55°C = 550 * 0.1°C)
        if (m_temp_c_10 > 550) {
            ESP_LOGW(TAG, "⚠️ Thermal warning: SW3526 / Puck temp is %d.%d°C -> Throttling!",
                     m_temp_c_10 / 10, m_temp_c_10 % 10);
            m_state = FAST_CHARGE_STATE_THERMAL_THROTTLE;
        }
    }
}

void FastChargeManager::update() {
    uint64_t now = esp_timer_get_time();

    // 1. Check Hardware Overcurrent / Fault Pin (Active-Low)
    int fault_pin = gpio_get_level(PIN_FAST_CHARGE_FAULT_N);
    if (fault_pin == 0 && !m_fault_detected) {
        m_fault_detected = true;
        m_state = FAST_CHARGE_STATE_FAULT;
        ESP_LOGE(TAG, "🚨 OVERCURRENT FAULT DETECTED on glovebox fast charger! Hardware shutdown triggered.");
        gpio_set_level(PIN_FAST_CHARGE_EN, 0);
    } else if (fault_pin == 1 && m_fault_detected) {
        m_fault_detected = false;
        ESP_LOGI(TAG, "Fault condition cleared. Auto-recovering fast charger.");
        set_power(true);
    }

    // 2. Handle Reboot Timer
    if (m_state == FAST_CHARGE_STATE_REBOOTING) {
        if (now - m_reset_start_us >= (OTTOCAST_RESET_PULSE_MS * 1000ULL)) {
            ESP_LOGI(TAG, "Hard reset completed. Re-enabling fast charger VBUS.");
            set_power(true);
        }
    }

    // 3. Handle Delayed Shutdown Grace Period (Ignition OFF)
    if (m_state == FAST_CHARGE_STATE_CAFE_COUNTDOWN) {
        uint64_t elapsed_us = now - m_cafe_timer_start_us;
        uint64_t limit_us = (uint64_t)CAFE_DISCONNECT_SEC * 1000000ULL;
        if (elapsed_us >= limit_us) {
            ESP_LOGI(TAG, "Grace period expired (%d s). Disabling glovebox power to prevent battery drain.", CAFE_DISCONNECT_SEC);
            set_power(false);
        }
    }

    // 4. Handle Pause Resume
    if (m_pause_until_us > 0 && now >= m_pause_until_us) {
        m_pause_until_us = 0;
        set_power(true);
    }

    // 5. Periodic I2C Polling (every 500 ms)
    if (now - m_last_i2c_poll_us >= 500000ULL) {
        m_last_i2c_poll_us = now;
        poll_sw3526_i2c();
    }
}

FastChargeState FastChargeManager::get_state() const {
    return m_state;
}

bool FastChargeManager::is_power_on() const {
    return m_power_enabled && !m_fault_detected;
}

bool FastChargeManager::has_fault() const {
    return m_fault_detected;
}

uint32_t FastChargeManager::get_cafe_remaining_sec() const {
    if (m_state != FAST_CHARGE_STATE_CAFE_COUNTDOWN) return 0;
    uint64_t elapsed_us = esp_timer_get_time() - m_cafe_timer_start_us;
    uint64_t limit_us = (uint64_t)CAFE_DISCONNECT_SEC * 1000000ULL;
    if (elapsed_us >= limit_us) return 0;
    return (uint32_t)((limit_us - elapsed_us) / 1000000ULL);
}

void FastChargeManager::get_telemetry_packet(UsbPowerDeliveryStatPkt* pkt) const {
    if (!pkt) return;
    pkt->vbus_mv = m_vbus_mv;
    pkt->current_ma = m_current_ma;
    pkt->power_mw = get_power_mw();
    pkt->temperature_c_10 = m_temp_c_10;
    pkt->qi_state = m_qi_state;
    pkt->pd_profile = m_pd_profile;
    pkt->kl15_grace_active = (m_state == FAST_CHARGE_STATE_CAFE_COUNTDOWN) ? 1 : 0;
    pkt->fault_flags = m_fault_detected ? 0x01 : 0x00;
}
