#include "power_manager.h"
#include "keyfob_config.h"
#include "esp_log.h"
#include "esp_sleep.h"
#include "driver/gpio.h"
#include "esp_adc/adc_oneshot.h"

static const char* TAG = "PowerManager";

static adc_oneshot_unit_handle_t s_adc1_handle = nullptr;

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
    // 1. Configure BQ51050B Charge Status Pin (Active Low)
    gpio_config_t chg_conf = {};
    chg_conf.pin_bit_mask = (1ULL << KEYFOB_PIN_CHG_STAT);
    chg_conf.mode         = GPIO_MODE_INPUT;
    chg_conf.pull_up_en   = GPIO_PULLUP_ENABLE;
    chg_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    chg_conf.intr_type    = GPIO_INTR_DISABLE;
    gpio_config(&chg_conf);

    // 2. Configure ADC1 for VBAT Sense (GPIO 0 / Channel 0)
    adc_oneshot_unit_init_cfg_t init_config = {
        .unit_id = ADC_UNIT_1,
        .ulp_mode = ADC_ULP_MODE_DISABLE,
    };
    if (adc_oneshot_new_unit(&init_config, &s_adc1_handle) == ESP_OK) {
        adc_oneshot_chan_cfg_t chan_config = {
            .atten = ADC_ATTEN_DB_12, // Up to ~3.1V full-scale
            .bitwidth = ADC_BITWIDTH_DEFAULT,
        };
        adc_oneshot_config_channel(s_adc1_handle, KEYFOB_ADC1_CHANNEL_VBAT, &chan_config);
    } else {
        ESP_LOGW(TAG, "ADC1 initialization failed, using nominal battery values");
    }

    read_sensors();
    configure_sleep_wakeups();
    m_initialized = true;
    ESP_LOGI(TAG, "Power Manager initialized: VBAT=%d mV (%d%%), Charging=%s",
             m_vbat_mv, m_battery_pct, m_is_charging ? "YES" : "NO");
    return true;
}

void KeyfobPowerManager::read_sensors() {
    // 1. Read BQ51050B Charge Status (Low = Qi wireless charging active)
    m_is_charging = (gpio_get_level(KEYFOB_PIN_CHG_STAT) == 0);

    // 2. Read Battery Voltage via ADC1 Channel 0
    if (s_adc1_handle) {
        int raw = 0;
        if (adc_oneshot_read(s_adc1_handle, KEYFOB_ADC1_CHANNEL_VBAT, &raw) == ESP_OK) {
            // 12-bit ADC (0..4095) with 12dB attenuation (~3100 mV full scale)
            // Voltage divider: 100k / 100k (2:1 ratio)
            uint32_t adc_mv = (raw * 3100) / 4095;
            m_vbat_mv = (uint16_t)(adc_mv * 2);
        }
    }

    // 3. Compute Percentage: 3.40V (0%) .. 4.20V (100%)
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

    // Refresh readings every 5 seconds
    if (m_poll_timer_ms >= 5000) {
        m_poll_timer_ms = 0;
        read_sensors();
    }
}

void KeyfobPowerManager::configure_sleep_wakeups() {
    // Enable GPIO wakeup for Buttons SW1/SW2, LoRa IRQ, and Qi Charger
    gpio_wakeup_enable(KEYFOB_PIN_BTN_ARM_N, GPIO_INTR_LOW_LEVEL);
    gpio_wakeup_enable(KEYFOB_PIN_BTN_SOS_N, GPIO_INTR_LOW_LEVEL);
    gpio_wakeup_enable(KEYFOB_PIN_LORA_DIO1, GPIO_INTR_HIGH_LEVEL);
    gpio_wakeup_enable(KEYFOB_PIN_CHG_STAT,  GPIO_INTR_LOW_LEVEL);
    esp_sleep_enable_gpio_wakeup();
}

void KeyfobPowerManager::enter_light_sleep(uint32_t sleep_time_ms) {
    if (sleep_time_ms > 0) {
        esp_sleep_enable_timer_wakeup((uint64_t)sleep_time_ms * 1000ULL);
    }
    esp_light_sleep_start();
}

void KeyfobPowerManager::enter_deep_sleep() {
    ESP_LOGI(TAG, "Entering Deep Sleep... Wakeup via SW1, SW2, LoRa DIO1 or Qi Charger");
    esp_deep_sleep_start();
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

bool KeyfobPowerManager::is_low_battery() const {
    return m_battery_pct < 15;
}
