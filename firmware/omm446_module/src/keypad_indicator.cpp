#include "keypad_indicator.h"
#include "omm446_config.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "driver/gpio.h"

static const char *TAG = "OMM446_KEYPAD";

static int64_t s_ptt_press_time = 0;
static bool s_ptt_held_long = false;
static bool s_ptt_is_pressed = false;

static Omm446LedMode_t s_current_led_mode = LED_MODE_RX_STANDBY_ANALOG;
static uint32_t s_anim_tick = 0;

esp_err_t keypad_indicator_init(void) {
    ESP_LOGI(TAG, "Initializing tactile keypad SW1..SW4 and status indicator...");

    gpio_config_t btn_conf = {};
    btn_conf.pin_bit_mask = (1ULL << OMM446_PIN_SW_PTT) |
                            (1ULL << OMM446_PIN_SW_MODE) |
                            (1ULL << OMM446_PIN_SW_CH_UP) |
                            (1ULL << OMM446_PIN_SW_CH_DOWN);
    btn_conf.mode = GPIO_MODE_INPUT;
    btn_conf.pull_up_en = GPIO_PULLUP_ENABLE;
    btn_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    btn_conf.intr_type = GPIO_INTR_DISABLE;
    esp_err_t ret = gpio_config(&btn_conf);
    if (ret != ESP_OK) return ret;

    // WS2812B GPIO output setup
    gpio_config_t led_conf = {};
    led_conf.pin_bit_mask = (1ULL << OMM446_PIN_WS2812B);
    led_conf.mode = GPIO_MODE_OUTPUT;
    led_conf.pull_up_en = GPIO_PULLUP_DISABLE;
    led_conf.pull_down_en = GPIO_PULLDOWN_ENABLE;
    ret = gpio_config(&led_conf);
    if (ret != ESP_OK) return ret;

    indicator_set_mode(LED_MODE_RX_STANDBY_ANALOG);
    return ESP_OK;
}

Omm446KeyEvent_t keypad_poll_events(void) {
    int64_t now = esp_timer_get_time() / 1000; // ms

    // SW1: PTT / Power
    bool ptt_low = (gpio_get_level(OMM446_PIN_SW_PTT) == 0);
    if (ptt_low) {
        if (!s_ptt_is_pressed) {
            s_ptt_is_pressed = true;
            s_ptt_press_time = now;
            s_ptt_held_long = false;
            return KEY_EVENT_PTT_PRESS;
        } else if (!s_ptt_held_long && (now - s_ptt_press_time >= 3000)) {
            s_ptt_held_long = true;
            return KEY_EVENT_PTT_LONG;
        }
    } else {
        if (s_ptt_is_pressed) {
            s_ptt_is_pressed = false;
            s_ptt_press_time = 0;
            if (!s_ptt_held_long) {
                return KEY_EVENT_PTT_RELEASE;
            }
        }
    }

    // SW2: Mode Switch (Analog PMR446 <-> Digital DMR Tier I)
    static bool mode_was_low = false;
    bool mode_low = (gpio_get_level(OMM446_PIN_SW_MODE) == 0);
    if (mode_low && !mode_was_low) {
        mode_was_low = true;
        return KEY_EVENT_MODE_TOGGLE;
    }
    mode_was_low = mode_low;

    // SW3: Channel Selection UP
    static bool ch_up_was_low = false;
    bool ch_up_low = (gpio_get_level(OMM446_PIN_SW_CH_UP) == 0);
    if (ch_up_low && !ch_up_was_low) {
        ch_up_was_low = true;
        return KEY_EVENT_CH_UP;
    }
    ch_up_was_low = ch_up_low;

    // SW4: Channel Selection DOWN
    static bool ch_dn_was_low = false;
    bool ch_dn_low = (gpio_get_level(OMM446_PIN_SW_CH_DOWN) == 0);
    if (ch_dn_low && !ch_dn_was_low) {
        ch_dn_was_low = true;
        return KEY_EVENT_CH_DOWN;
    }
    ch_dn_was_low = ch_dn_low;

    return KEY_EVENT_NONE;
}

void indicator_set_mode(Omm446LedMode_t mode) {
    if (s_current_led_mode == mode) return;
    s_current_led_mode = mode;
    s_anim_tick = 0;

    switch (mode) {
        case LED_MODE_TX_ANALOG:
            ESP_LOGI(TAG, "LED -> Solid RED (Analog TX Active)");
            break;
        case LED_MODE_TX_DMR:
            ESP_LOGI(TAG, "LED -> Solid BLUE (DMR TX Active)");
            break;
        case LED_MODE_RX_ACTIVE_ANALOG:
            ESP_LOGI(TAG, "LED -> Solid GREEN (Analog RX Signal Active)");
            break;
        case LED_MODE_RX_ACTIVE_DMR:
            ESP_LOGI(TAG, "LED -> Solid CYAN (DMR RX Digital Active)");
            break;
        case LED_MODE_RX_STANDBY_ANALOG:
            ESP_LOGI(TAG, "LED -> Breathing GREEN (Analog Standby)");
            break;
        case LED_MODE_RX_STANDBY_DMR:
            ESP_LOGI(TAG, "LED -> Breathing CYAN (DMR Standby)");
            break;
        case LED_MODE_MODE_SWITCH:
            ESP_LOGI(TAG, "LED -> Purple Flash (Mode Toggled)");
            break;
        case LED_MODE_CHANNEL_CHANGE:
            ESP_LOGI(TAG, "LED -> Amber Flash (Channel Changed)");
            break;
        case LED_MODE_BATTERY_LOW:
            ESP_LOGW(TAG, "LED -> Fast Red Flash (Battery Low)");
            break;
        case LED_MODE_CHARGING:
            ESP_LOGI(TAG, "LED -> Amber Breathe (Charging)");
            break;
        default:
            break;
    }
}

void indicator_update(void) {
    s_anim_tick++;
    // Periodische LED-Farbanpassung / Animationen
}
