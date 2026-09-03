#include "ottocast_power_manager.h"
#include "front_node_config.h"
#include "esp_timer.h"
#include "esp_log.h"
#include "driver/gpio.h"

static const char* TAG = "OTTOCAST_PWR";

OttocastPowerManager& OttocastPowerManager::instance() {
    static OttocastPowerManager inst;
    return inst;
}

OttocastPowerManager::OttocastPowerManager()
    : m_state(OTTOCAST_STATE_OFF)
    , m_power_enabled(false)
    , m_fault_detected(false)
    , m_ignition_active(true)
    , m_reset_start_us(0)
    , m_cafe_timer_start_us(0)
    , m_arbitration_until_us(0)
{
}

bool OttocastPowerManager::init() {
    // 1. Configure Power Enable Pin (GPIO6, Output, Active-High)
    gpio_config_t en_conf = {
        .pin_bit_mask = (1ULL << PIN_OTTOCAST_PWR_EN),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_ENABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&en_conf);
    gpio_set_level(PIN_OTTOCAST_PWR_EN, 0); // Start OFF

    // 2. Configure Fault Alert Pin (GPIO7, Input, Active-Low)
    gpio_config_t fault_conf = {
        .pin_bit_mask = (1ULL << PIN_OTTOCAST_FAULT_N),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE, // TPS2051B is Open-Drain
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&fault_conf);

    // Initial power-up
    set_power(true);
    ESP_LOGI(TAG, "Ottocast power manager initialized (TPS2051B: EN=GPIO6, FAULT_N=GPIO7). Initial state: ACTIVE");
    return true;
}

void OttocastPowerManager::set_power(bool enable) {
    if (enable && m_fault_detected) {
        ESP_LOGW(TAG, "Cannot enable VBUS: Overcurrent fault condition persists!");
        return;
    }

    m_power_enabled = enable;
    gpio_set_level(PIN_OTTOCAST_PWR_EN, enable ? 1 : 0);
    m_state = enable ? OTTOCAST_STATE_ACTIVE : OTTOCAST_STATE_OFF;
    ESP_LOGI(TAG, "Ottocast VBUS power %s", enable ? "ENABLED (+5V ON)" : "DISABLED (0V OFF)");
}

void OttocastPowerManager::trigger_hard_reset() {
    ESP_LOGW(TAG, "1-Click Hard Reset triggered! Power-cycling Ottocast for %d ms...", OTTOCAST_RESET_PULSE_MS);
    gpio_set_level(PIN_OTTOCAST_PWR_EN, 0);
    m_state = OTTOCAST_STATE_REBOOTING;
    m_reset_start_us = esp_timer_get_time();
}

void OttocastPowerManager::set_ignition(bool ignition_on) {
    if (m_ignition_active == ignition_on) return;
    m_ignition_active = ignition_on;

    if (!ignition_on) {
        ESP_LOGI(TAG, "Ignition OFF detected. Starting %d-second Auto-Café countdown...", CAFE_DISCONNECT_SEC);
        m_state = OTTOCAST_STATE_CAFE_COUNTDOWN;
        m_cafe_timer_start_us = esp_timer_get_time();
    } else {
        ESP_LOGI(TAG, "Ignition ON detected. Restoring active VBUS operation.");
        m_cafe_timer_start_us = 0;
        set_power(true);
    }
}

void OttocastPowerManager::pause_for_usb_host_arbitration(uint32_t duration_ms) {
    ESP_LOGI(TAG, "Glovebox USB activity detected: Pausing Ottocast for %lu ms to avoid host collisions", duration_ms);
    gpio_set_level(PIN_OTTOCAST_PWR_EN, 0);
    m_arbitration_until_us = esp_timer_get_time() + (duration_ms * 1000ULL);
}

void OttocastPowerManager::update() {
    uint64_t now = esp_timer_get_time();

    // 1. Check Hardware Overcurrent / Fault Pin (Active-Low)
    int fault_pin = gpio_get_level(PIN_OTTOCAST_FAULT_N);
    if (fault_pin == 0 && !m_fault_detected) {
        m_fault_detected = true;
        m_state = OTTOCAST_STATE_FAULT;
        gpio_set_level(PIN_OTTOCAST_PWR_EN, 0); // Fast hardware shutdown
        ESP_LOGE(TAG, "CRITICAL: TPS2051B reports OVERCURRENT / SHORT CIRCUIT on CarPlay VBUS! Power severed.");
    } else if (fault_pin == 1 && m_fault_detected) {
        m_fault_detected = false;
        ESP_LOGI(TAG, "TPS2051B overcurrent condition cleared.");
    }

    // 2. Handle Reboot Pulse State
    if (m_state == OTTOCAST_STATE_REBOOTING) {
        if ((now - m_reset_start_us) >= (OTTOCAST_RESET_PULSE_MS * 1000ULL)) {
            ESP_LOGI(TAG, "Reboot pulse complete. Re-enabling +5V VBUS.");
            set_power(true);
        }
    }

    // 3. Handle Auto-Café Disconnect Countdown
    if (m_state == OTTOCAST_STATE_CAFE_COUNTDOWN) {
        if ((now - m_cafe_timer_start_us) >= (CAFE_DISCONNECT_SEC * 1000000ULL)) {
            ESP_LOGI(TAG, "Auto-Café countdown expired. Powering down Ottocast to release phone Wi-Fi connection.");
            set_power(false);
        }
    }

    // 4. Handle USB Host Arbitration Timeout
    if (m_arbitration_until_us > 0 && now >= m_arbitration_until_us) {
        m_arbitration_until_us = 0;
        if (m_ignition_active) {
            ESP_LOGI(TAG, "USB host arbitration complete. Restoring CarPlay VBUS.");
            set_power(true);
        }
    }
}

OttocastState OttocastPowerManager::get_state() const {
    return m_state;
}

bool OttocastPowerManager::is_power_on() const {
    return (gpio_get_level(PIN_OTTOCAST_PWR_EN) == 1);
}

bool OttocastPowerManager::has_fault() const {
    return m_fault_detected;
}

uint32_t OttocastPowerManager::get_cafe_remaining_sec() const {
    if (m_state != OTTOCAST_STATE_CAFE_COUNTDOWN) return 0;
    uint64_t elapsed_us = esp_timer_get_time() - m_cafe_timer_start_us;
    uint64_t total_us = CAFE_DISCONNECT_SEC * 1000000ULL;
    if (elapsed_us >= total_us) return 0;
    return static_cast<uint32_t>((total_us - elapsed_us) / 1000000ULL);
}
