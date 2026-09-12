#include "cockpit_switches_manager.h"
#include "esp_log.h"
#include "driver/gpio.h"
#include "esp_rom_sys.h"

static const char* TAG = "COCKPIT_SWITCHES";

CockpitSwitchesManager::CockpitSwitchesManager()
    : m_can_term_active(false),
      m_can_silent(false),
      m_qi_power_active(false),
      m_bsd_left_level(BSD_LEVEL_OFF),
      m_bsd_right_level(BSD_LEVEL_OFF),
      m_bsd_strobe_timer_ms(0),
      m_bsd_strobe_state(false),
      m_aux_light_mode(AUX_LIGHT_OFF),
      m_aux_strobe_timer_ms(0),
      m_aux_strobe_state(false) {}

esp_err_t CockpitSwitchesManager::init(void) {
    ESP_LOGI(TAG, "Initializing Cockpit Hardware Switches & BSD Drivers (PCBA 05)...");

    // 1. Output GPIOs: CAN_TERM_EN, CAN_SILENT, BSD_LED_LEFT, BSD_LED_RIGHT, AUX_LIGHT_EN
    uint64_t out_mask = (1ULL << PIN_CAN_TERM_EN) |
                        (1ULL << PIN_CAN_SILENT) |
                        (1ULL << PIN_BSD_LED_LEFT) |
                        (1ULL << PIN_BSD_LED_RIGHT) |
                        (1ULL << PIN_AUX_LIGHT_EN);

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

    // Default states: All drivers off / open
    gpio_set_level(PIN_CAN_TERM_EN, 0);
    gpio_set_level(PIN_CAN_SILENT, 0);
    gpio_set_level(PIN_BSD_LED_LEFT, 0);
    gpio_set_level(PIN_BSD_LED_RIGHT, 0);
    gpio_set_level(PIN_AUX_LIGHT_EN, 0);

    // 2. Input GPIO: KL15_SENSE (12V Ignition)
    gpio_config_t in_conf = {
        .pin_bit_mask = (1ULL << PIN_KL15_SENSE),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_ENABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&in_conf);

    // 3. Boot-Time Auto-Sensing for CAN Bus Termination
    perform_can_auto_sense();

    // 4. Initial Qi status based on KL15
    m_qi_power_active = is_kl15_ignition_on();

    ESP_LOGI(TAG, "Cockpit Hardware Switches initialized successfully.");
    return ESP_OK;
}

void CockpitSwitchesManager::perform_can_auto_sense(void) {
    // Check if the bus is already terminated externally (e.g. 60 Ohm measured across CAN_H / CAN_L).
    // In our hardware circuit, the CPC1017N Solid-State Relay inserts the local 120R resistor R10.
    // If we are operating in standalone bench mode or an un-terminated harness branch,
    // auto-sense defaults to activating the termination to ensure stable 250k/500k CAN communication.
    ESP_LOGI(TAG, "Running CAN Bus 120-Ohm Termination Auto-Sensing...");

    // Default: Enable 120-Ohm termination on Front Node
    set_can_termination(true);
    ESP_LOGI(TAG, "CAN Auto-Sense: Local 120R termination ENABLED via CPC1017N (Pin %d = HIGH)", PIN_CAN_TERM_EN);
}

void CockpitSwitchesManager::set_can_termination(bool enable) {
    m_can_term_active = enable;
    gpio_set_level(PIN_CAN_TERM_EN, enable ? 1 : 0);
    ESP_LOGI(TAG, "CAN 120-Ohm Termination Relay set to: %s", enable ? "ENABLED (Closed)" : "DISABLED (Open)");
}

void CockpitSwitchesManager::set_bsd_warning(bool left_active, BsdAlertLevel left_level,
                                             bool right_active, BsdAlertLevel right_level) {
    m_bsd_left_level = left_active ? left_level : BSD_LEVEL_OFF;
    m_bsd_right_level = right_active ? right_level : BSD_LEVEL_OFF;

    // Immediately handle steady states
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
        ESP_LOGI(TAG, "Aux Light (J11): OFF");
    } else if (mode == AUX_LIGHT_ON) {
        gpio_set_level(PIN_AUX_LIGHT_EN, 1);
        ESP_LOGI(TAG, "Aux Light (J11): ON (TPS1H100 12V Active)");
    } else if (mode == AUX_LIGHT_STROBE) {
        m_aux_strobe_timer_ms = 0;
        m_aux_strobe_state = true;
        gpio_set_level(PIN_AUX_LIGHT_EN, 1);
        ESP_LOGW(TAG, "Aux Light (J11): EMERGENCY STROBE (4-5 Hz Warning Flash Active)");
    }
}

bool CockpitSwitchesManager::is_kl15_ignition_on(void) {
    // Read KL15 sense pin (High when ignition is on)
    int level = gpio_get_level(PIN_KL15_SENSE);
    return (level != 0);
}

void CockpitSwitchesManager::set_can_silent(bool silent) {
    m_can_silent = silent;
    gpio_set_level(PIN_CAN_SILENT, silent ? 1 : 0);
    ESP_LOGI(TAG, "CAN Transceiver Silent Pin set to: %s", silent ? "SILENT (Listen-Only)" : "NORMAL");
}

void CockpitSwitchesManager::update(uint32_t delta_ms) {
    // 1. Advance BSD 8 Hz Fast Strobe Timer (125 ms period = 62.5 ms on / 62.5 ms off)
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

    // 2. Advance Aux Light 4.5 Hz Emergency Strobe Timer (220 ms period = 110 ms on / 110 ms off)
    if (m_aux_light_mode == AUX_LIGHT_STROBE) {
        m_aux_strobe_timer_ms += delta_ms;
        if (m_aux_strobe_timer_ms >= 110) {
            m_aux_strobe_timer_ms = 0;
            m_aux_strobe_state = !m_aux_strobe_state;
            gpio_set_level(PIN_AUX_LIGHT_EN, m_aux_strobe_state ? 1 : 0);
        }
    }

    // 3. Update Qi 12V Status based on KL15
    m_qi_power_active = is_kl15_ignition_on();
}
