#include "keypad_indicator.h"
#include "omm_module_config.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "driver/gpio.h"

static const char *TAG = "OMM_KEYPAD";

static int64_t s_pwr_press_time = 0;
static bool s_pwr_held = false;

esp_err_t keypad_indicator_init(void) {
    ESP_LOGI(TAG, "Initializing tactile keypad SW1..SW4 and status indicator...");

    gpio_config_t btn_conf = {};
    btn_conf.pin_bit_mask = (1ULL << OMM_PIN_SW_POWER) |
                            (1ULL << OMM_PIN_SW_MESH) |
                            (1ULL << OMM_PIN_SW_VOL_UP) |
                            (1ULL << OMM_PIN_SW_VOL_DOWN);
    btn_conf.mode = GPIO_MODE_INPUT;
    btn_conf.pull_up_en = GPIO_PULLUP_ENABLE;
    btn_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    btn_conf.intr_type = GPIO_INTR_DISABLE;
    esp_err_t ret = gpio_config(&btn_conf);
    if (ret != ESP_OK) return ret;

    // WS2812B GPIO output setup
    gpio_config_t led_conf = {};
    led_conf.pin_bit_mask = (1ULL << OMM_PIN_WS2812B);
    led_conf.mode = GPIO_MODE_OUTPUT;
    led_conf.pull_up_en = GPIO_PULLUP_DISABLE;
    led_conf.pull_down_en = GPIO_PULLDOWN_ENABLE;
    ret = gpio_config(&led_conf);
    if (ret != ESP_OK) return ret;

    indicator_set_mode(LED_MODE_STANDBY_GREEN);
    return ESP_OK;
}

OmmKeyEvent_t keypad_poll_events(void) {
    int64_t now = esp_timer_get_time() / 1000; // ms

    // SW1: Power / MFB
    if (gpio_get_level(OMM_PIN_SW_POWER) == 0) {
        if (s_pwr_press_time == 0) {
            s_pwr_press_time = now;
        } else if (!s_pwr_held && (now - s_pwr_press_time >= 2500)) {
            s_pwr_held = true;
            return KEY_EVENT_POWER_LONG;
        }
    } else {
        if (s_pwr_press_time > 0) {
            int64_t dur = now - s_pwr_press_time;
            s_pwr_press_time = 0;
            if (!s_pwr_held && dur > 50 && dur < 2000) {
                return KEY_EVENT_POWER_SHORT;
            }
            s_pwr_held = false;
        }
    }

    // SW2: Mesh Toggle
    static bool mesh_was_low = false;
    bool mesh_low = (gpio_get_level(OMM_PIN_SW_MESH) == 0);
    if (mesh_low && !mesh_was_low) {
        mesh_was_low = true;
        return KEY_EVENT_MESH_TOGGLE;
    }
    mesh_was_low = mesh_low;

    // SW3: Volume +
    static bool vol_up_was_low = false;
    bool vol_up_low = (gpio_get_level(OMM_PIN_SW_VOL_UP) == 0);
    if (vol_up_low && !vol_up_was_low) {
        vol_up_was_low = true;
        return KEY_EVENT_VOL_UP;
    }
    vol_up_was_low = vol_up_low;

    // SW4: Volume -
    static bool vol_dn_was_low = false;
    bool vol_dn_low = (gpio_get_level(OMM_PIN_SW_VOL_DOWN) == 0);
    if (vol_dn_low && !vol_dn_was_low) {
        vol_dn_was_low = true;
        return KEY_EVENT_VOL_DOWN;
    }
    vol_dn_was_low = vol_dn_low;

    return KEY_EVENT_NONE;
}

void indicator_set_mode(OmmLedMode_t mode) {
    // LED Mode representation
    switch (mode) {
        case LED_MODE_TX_BLUE:
            ESP_LOGD(TAG, "LED: Blue (TX)");
            break;
        case LED_MODE_RX_CYAN:
            ESP_LOGD(TAG, "LED: Cyan (RX)");
            break;
        case LED_MODE_GROUP_PURPLE:
            ESP_LOGD(TAG, "LED: Purple (Group Mesh)");
            break;
        case LED_MODE_WARN_YELLOW:
            ESP_LOGD(TAG, "LED: Yellow (Battery Warning)");
            break;
        case LED_MODE_EMERGENCY_RED:
            ESP_LOGD(TAG, "LED: Red (Emergency / Fault)");
            break;
        case LED_MODE_STANDBY_GREEN:
        default:
            ESP_LOGD(TAG, "LED: Green (Standby OK)");
            break;
    }
}
