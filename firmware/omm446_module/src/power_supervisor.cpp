#include "power_supervisor.h"
#include "omm446_config.h"
#include "esp_log.h"
#include "driver/gpio.h"
#include "esp_sleep.h"

static const char *TAG = "OMM446_PWR";

esp_err_t power_supervisor_init(void) {
    ESP_LOGI(TAG, "Initializing TI BQ24075 PMIC & Battery Supervisor...");

    // GPIO 7: BQ24075 /STAT pin (Open drain with pullup)
    gpio_config_t stat_conf = {};
    stat_conf.pin_bit_mask = (1ULL << OMM446_PIN_CHG_STAT);
    stat_conf.mode = GPIO_MODE_INPUT;
    stat_conf.pull_up_en = GPIO_PULLUP_ENABLE;
    stat_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    stat_conf.intr_type = GPIO_INTR_DISABLE;
    return gpio_config(&stat_conf);
}

void power_supervisor_poll(Omm446PowerStatus_t *status) {
    if (!status) return;

    // Check charging status: BQ24075 pulls /STAT low when actively charging
    status->is_charging = (gpio_get_level(OMM446_PIN_CHG_STAT) == 0);
    status->is_vbus_present = status->is_charging; // If charging, 5V VBUS is present

    // Default battery estimation
    status->v_bat = 3.90f;
    status->battery_pct = 75;
}

void power_enter_deep_sleep(void) {
    ESP_LOGI(TAG, "Entering ultra-low power deep sleep (Wakeup via SW1 PTT)...");

    // Configure SW1 (GPIO 2) as wakeup source
    esp_deep_sleep_enable_gpio_wakeup((1ULL << OMM446_PIN_SW_PTT), ESP_GPIO_WAKEUP_GPIO_LOW);
    esp_deep_sleep_start();
}
