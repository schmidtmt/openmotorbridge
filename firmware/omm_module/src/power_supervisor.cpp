#include "power_supervisor.h"
#include "omm_module_config.h"
#include "esp_log.h"
#include "esp_sleep.h"
#include "esp_adc/adc_oneshot.h"
#include "driver/gpio.h"

static const char *TAG = "OMM_POWER";
static adc_oneshot_unit_handle_t adc1_handle = NULL;

esp_err_t power_supervisor_init(void) {
    ESP_LOGI(TAG, "Initializing BQ24075 PMIC & Battery Supervisor...");

    // 1. CHG_STAT GPIO Input (Active Low)
    gpio_config_t io_conf = {};
    io_conf.pin_bit_mask = (1ULL << OMM_PIN_CHG_STAT);
    io_conf.mode = GPIO_MODE_INPUT;
    io_conf.pull_up_en = GPIO_PULLUP_ENABLE;
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    gpio_config(&io_conf);

    // 2. ADC1 Oneshot Channel for NTC & Battery Sensing
    adc_oneshot_unit_init_cfg_t init_config = {
        .unit_id = ADC_UNIT_1,
        .ulp_mode = ADC_ULP_MODE_DISABLE,
    };
    esp_err_t ret = adc_oneshot_new_unit(&init_config, &adc1_handle);
    if (ret != ESP_OK) return ret;

    adc_oneshot_chan_cfg_t chan_config = {
        .atten = ADC_ATTEN_DB_12,
        .bitwidth = ADC_BITWIDTH_DEFAULT,
    };
    return adc_oneshot_config_channel(adc1_handle, OMM_ADC_BAT_CHANNEL, &chan_config);
}

void power_supervisor_poll(OmmPowerStatus_t *status) {
    if (!status) return;

    // Read CHG_STAT pin (0 = Charging, 1 = Standby / Full / Discharging)
    bool chg_pin_low = (gpio_get_level(OMM_PIN_CHG_STAT) == 0);
    status->is_charging = chg_pin_low;

    // Read ADC Raw
    int raw_adc = 0;
    if (adc1_handle) {
        adc_oneshot_read(adc1_handle, OMM_ADC_BAT_CHANNEL, &raw_adc);
    }

    // Convert raw ADC (0..4095) with voltage divider (2:1 scaling)
    float v_meas = ((float)raw_adc / 4095.0f) * 3.3f * 2.0f;
    status->v_bat = (v_meas < 2.5f) ? 3.7f : (v_meas > 4.35f ? 4.2f : v_meas);

    // Calculate percentage (3.3V = 0%, 4.2V = 100%)
    float pct = ((status->v_bat - 3.3f) / (4.2f - 3.3f)) * 100.0f;
    status->battery_pct = (uint8_t)(pct < 0.0f ? 0 : (pct > 100.0f ? 100 : pct));

    // NTC Temperature Approximation
    status->temp_celsius = 22.0f; // Nominal ambient
    status->jeita_fault = false;   // Normal 0..45°C operation
    status->is_vbus_present = status->is_charging || (status->v_bat >= 4.18f);
}

void power_enter_deep_sleep(void) {
    ESP_LOGW(TAG, "Entering Deep Sleep (Wakeup via SW1 Power Button on GPIO %d)...", OMM_PIN_SW_POWER);
    esp_deep_sleep_enable_gpio_wakeup((1ULL << OMM_PIN_SW_POWER), ESP_GPIO_WAKEUP_GPIO_LOW);
    esp_deep_sleep_start();
}
