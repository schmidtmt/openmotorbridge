#include "cockpit_switches_manager.h"
#include "esp_log.h"
#include "driver/gpio.h"

static const char* TAG = "COCKPIT_SWITCHES";

CockpitSwitchesManager::CockpitSwitchesManager()
    : m_e22_enabled(true),
      m_bsd_left_level(BSD_LEVEL_OFF),
      m_bsd_right_level(BSD_LEVEL_OFF),
      m_bsd_strobe_timer_ms(0),
      m_bsd_strobe_state(false),
      m_aux_light_mode(AUX_LIGHT_OFF),
      m_aux_strobe_timer_ms(0),
      m_aux_strobe_state(false) {}

esp_err_t CockpitSwitchesManager::init(void) {
    ESP_LOGI(TAG, "Initializing v10.0 Cockpit Hardware Switches (Q1 DMN63D8 BSD, Q2 TPS1H100 Aux, U9 E22_EN)...");

    uint64_t out_mask = (1ULL << PIN_BSD_LED_LEFT) |
                        (1ULL << PIN_BSD_LED_RIGHT) |
                        (1ULL << PIN_AUX_LIGHT_EN) |
                        (1ULL << PIN_E22_EN);

    gpio_config_t out_conf = {
        .pin_bit_mask = out_mask,
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_ENABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    esp_err_t err = gpio_config(&out_conf);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to configure switch output GPIOs: %d", err);
        return err;
    }

    gpio_set_level(PIN_BSD_LED_LEFT, 0);
    gpio_set_level(PIN_BSD_LED_RIGHT, 0);
    gpio_set_level(PIN_AUX_LIGHT_EN, 0);
    gpio_set_level(PIN_E22_EN, 1); // Enable U9 ESP32-E22 Wi-Fi 6E Co-Processor

    ESP_LOGI(TAG, "✓ Cockpit Hardware Switches & ESP32-E22 4-Bit SDIO 3.0 Power initialized.");
    return ESP_OK;
}

void CockpitSwitchesManager::set_bsd_warning(bool left_active, BsdAlertLevel left_level,
                                             bool right_active, BsdAlertLevel right_level) {
    m_bsd_left_level = left_active ? left_level : BSD_LEVEL_OFF;
    m_bsd_right_level = right_active ? right_level : BSD_LEVEL_OFF;

    if (m_bsd_left_level == BSD_LEVEL_OFF) {
        gpio_set_level(PIN_BSD_LED_LEFT, 0);
    } else if (m_bsd_left_level == BSD_LEVEL_SOLID_AMBER) {
        gpio_set_level(PIN_BSD_LED_LEFT, 1);
    }

    if (m_bsd_right_level == BSD_LEVEL_OFF) {
        gpio_set_level(PIN_BSD_LED_RIGHT, 0);
    } else if (m_bsd_right_level == BSD_LEVEL_SOLID_AMBER) {
        gpio_set_level(PIN_BSD_LED_RIGHT, 1);
    }
}

void CockpitSwitchesManager::set_aux_light_mode(AuxLightMode mode) {
    m_aux_light_mode = mode;
    if (mode == AUX_LIGHT_OFF) {
        gpio_set_level(PIN_AUX_LIGHT_EN, 0);
        ESP_LOGI(TAG, "Aux Light (J_AUX_LIGHT Q2 TPS1H100): OFF");
    } else if (mode == AUX_LIGHT_ON) {
        gpio_set_level(PIN_AUX_LIGHT_EN, 1);
        ESP_LOGI(TAG, "Aux Light (J_AUX_LIGHT Q2 TPS1H100): ON (12V Active)");
    } else if (mode == AUX_LIGHT_STROBE) {
        m_aux_strobe_timer_ms = 0;
        m_aux_strobe_state = true;
        gpio_set_level(PIN_AUX_LIGHT_EN, 1);
        ESP_LOGW(TAG, "Aux Light (J_AUX_LIGHT Q2 TPS1H100): EMERGENCY STROBE (4.5 Hz Active)");
    }
}

void CockpitSwitchesManager::set_e22_wifi6e_enable(bool enable) {
    m_e22_enabled = enable;
    gpio_set_level(PIN_E22_EN, enable ? 1 : 0);
    ESP_LOGI(TAG, "U9 ESP32-E22 Wi-Fi 6E Co-Processor (Pad 40 E22_EN): %s", enable ? "ENABLED" : "SLEEP");
}

void CockpitSwitchesManager::update(uint32_t delta_ms) {
    // 1. Advance BSD 8 Hz Fast Strobe Timer (62 ms toggle)
    m_bsd_strobe_timer_ms += delta_ms;
    if (m_bsd_strobe_timer_ms >= 62) {
        m_bsd_strobe_timer_ms = 0;
        m_bsd_strobe_state = !m_bsd_strobe_state;

        if (m_bsd_left_level == BSD_LEVEL_FAST_STROBE) {
            gpio_set_level(PIN_BSD_LED_LEFT, m_bsd_strobe_state ? 1 : 0);
        }
        if (m_bsd_right_level == BSD_LEVEL_FAST_STROBE) {
            gpio_set_level(PIN_BSD_LED_RIGHT, m_bsd_strobe_state ? 1 : 0);
        }
    }

    // 2. Advance Aux Light 4.5 Hz Emergency Strobe Timer (110 ms toggle)
    if (m_aux_light_mode == AUX_LIGHT_STROBE) {
        m_aux_strobe_timer_ms += delta_ms;
        if (m_aux_strobe_timer_ms >= 110) {
            m_aux_strobe_timer_ms = 0;
            m_aux_strobe_state = !m_aux_strobe_state;
            gpio_set_level(PIN_AUX_LIGHT_EN, m_aux_strobe_state ? 1 : 0);
        }
    }
}
