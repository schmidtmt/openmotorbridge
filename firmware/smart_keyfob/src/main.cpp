#include <stdio.h>
#include <string.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "driver/gpio.h"

#include "keyfob_config.h"
#include "keyfob_ble.h"
#include "sx1262_lora.h"
#include "buzzer_driver.h"
#include "ws2812b_led.h"
#include "power_manager.h"

static const char* TAG = "SmartKeyfob";

static bool s_is_armed = false;
static bool s_alarm_triggered = false;
static uint32_t s_idle_timer_ms = 0;

// Callback: LoRa Security Alarm received from Central Box (up to 4.5 km range)
static void on_lora_alarm_received(const KeyfobLoRaAlarmPkt& pkt) {
    if (pkt.header != 0xFE) return;

    s_alarm_triggered = true;
    s_idle_timer_ms = 0;

    ESP_LOGW(TAG, "🚨 LORA ALARM RECEIVED! Type: 0x%02X from Central Box 0x%08X (RSSI %d dBm)",
             pkt.alarm_type, (unsigned int)pkt.sender_uid, pkt.rssi_dbm);

    // 1. Acoustic Buzzer Siren (high penetration sweep)
    BuzzerDriver::instance().play_pattern(BUZZER_PATTERN_ALARM_SIREN);

    // 2. WS2812B LED Strobe Red (10 Hz urgent strobe)
    Ws2812bLed::instance().set_mode(KEYFOB_LED_ALARM_STROBE_RED);
}

// Callback: Remote Command from Smartphone PWA via BLE
static void on_ble_remote_command(uint8_t cmd, uint8_t param) {
    s_idle_timer_ms = 0;
    if (cmd == 0x20) { // Arm / Disarm command
        s_is_armed = (param != 0);
        BuzzerDriver::instance().play_pattern(s_is_armed ? BUZZER_PATTERN_CONFIRM_CHIRP : BUZZER_PATTERN_DISARM_CHIRP);
        Ws2812bLed::instance().set_mode(s_is_armed ? KEYFOB_LED_ARMED_CYAN : KEYFOB_LED_STANDBY_BREATHING_GREEN);
    }
}

// Button Handler for SW1 (Arm / Disarm)
static void handle_button_arm() {
    s_idle_timer_ms = 0;

    if (s_alarm_triggered) {
        // Acknowledge & clear active alarm
        ESP_LOGI(TAG, "Alarm acknowledged by user via SW1");
        s_alarm_triggered = false;
        BuzzerDriver::instance().stop();
        Ws2812bLed::instance().set_mode(s_is_armed ? KEYFOB_LED_ARMED_CYAN : KEYFOB_LED_STANDBY_BREATHING_GREEN);
        return;
    }

    s_is_armed = !s_is_armed;
    ESP_LOGI(TAG, "Keyfob SW1 pressed: State -> %s", s_is_armed ? "ARMED" : "DISARMED");

    // Acoustic & Visual User Feedback
    BuzzerDriver::instance().play_pattern(s_is_armed ? BUZZER_PATTERN_CONFIRM_CHIRP : BUZZER_PATTERN_DISARM_CHIRP);
    Ws2812bLed::instance().set_mode(s_is_armed ? KEYFOB_LED_ARMED_CYAN : KEYFOB_LED_STANDBY_BREATHING_GREEN);

    // Transmit to Central Box via BLE or LoRa
    if (KeyfobBle::instance().is_connected()) {
        KeyfobBle::instance().notify_alarm_state(s_is_armed);
        KeyfobBle::instance().notify_button_event(1, false);
    } else {
        Sx1262LoRa::instance().send_command(s_is_armed ? 0x20 : 0x21, 0x19680001);
    }
}

// Button Handler for SW2 (SOS Panic / Alarm)
static void handle_button_sos() {
    s_idle_timer_ms = 0;
    ESP_LOGW(TAG, "Keyfob SW2 pressed: TRIGGERING SOS PANIC BEACON!");

    // Acoustic Morse Code & High-Intensity White/Red Flash
    BuzzerDriver::instance().play_pattern(BUZZER_PATTERN_SOS_MORSE);
    Ws2812bLed::instance().set_mode(KEYFOB_LED_SOS_WHITE_RED);

    // Broadcast Emergency SOS Frame over 868.5 MHz LoRa
    Sx1262LoRa::instance().send_sos_panic(0x19680001);

    if (KeyfobBle::instance().is_connected()) {
        KeyfobBle::instance().notify_button_event(2, true);
    }
}

static void keyfob_main_task(void* pvParameters) {
    (void)pvParameters;
    const uint32_t TICK_MS = 20;

    int sw1_prev = 1;
    int sw2_prev = 1;
    uint32_t sw1_debounce = 0;
    uint32_t sw2_debounce = 0;

    while (1) {
        vTaskDelay(pdMS_TO_TICKS(TICK_MS));

        // 1. Update Subsystems
        BuzzerDriver::instance().update(TICK_MS);
        Ws2812bLed::instance().update(TICK_MS);
        KeyfobPowerManager::instance().update(TICK_MS);
        Sx1262LoRa::instance().update();
        KeyfobBle::instance().update();

        // 2. Button Debounce & State Machines
        int sw1_cur = gpio_get_level(KEYFOB_PIN_BTN_ARM_N);
        if (sw1_cur == 0 && sw1_prev == 1 && (xTaskGetTickCount() - sw1_debounce > pdMS_TO_TICKS(200))) {
            sw1_debounce = xTaskGetTickCount();
            handle_button_arm();
        }
        sw1_prev = sw1_cur;

        int sw2_cur = gpio_get_level(KEYFOB_PIN_BTN_SOS_N);
        if (sw2_cur == 0 && sw2_prev == 1 && (xTaskGetTickCount() - sw2_debounce > pdMS_TO_TICKS(200))) {
            sw2_debounce = xTaskGetTickCount();
            handle_button_sos();
        }
        sw2_prev = sw2_cur;

        // 3. Qi Charging Visual Feedback
        if (KeyfobPowerManager::instance().is_charging() && !s_alarm_triggered && !BuzzerDriver::instance().is_playing()) {
            Ws2812bLed::instance().set_mode(KEYFOB_LED_CHARGING_AMBER);
            s_idle_timer_ms = 0;
        }

        // 4. Power Saving: Enter light sleep if idle and no active alarm / buzzer
        s_idle_timer_ms += TICK_MS;
        if (s_idle_timer_ms >= 30000 && !s_alarm_triggered && !BuzzerDriver::instance().is_playing()) {
            ESP_LOGD(TAG, "Idle timeout reached, entering light sleep");
            Ws2812bLed::instance().set_mode(KEYFOB_LED_OFF);
            KeyfobPowerManager::instance().enter_light_sleep(1000);
            s_idle_timer_ms = 25000; // Reset timer so it wakes up periodically
            Ws2812bLed::instance().set_mode(s_is_armed ? KEYFOB_LED_ARMED_CYAN : KEYFOB_LED_STANDBY_BREATHING_GREEN);
        }
    }
}

extern "C" void app_main(void) {
    ESP_LOGI(TAG, "=======================================================");
    ESP_LOGI(TAG, "🚀 OpenMotorBridge Smart Keyfob & Pager (PCBA 07) v10.0");
    ESP_LOGI(TAG, "   Target: ESP32-C3FH4 RISC-V @ 160 MHz (4MB Flash)");
    ESP_LOGI(TAG, "=======================================================");

    // 1. Initialize NVS (required for BLE and settings)
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        nvs_flash_erase();
        nvs_flash_init();
    }

    // 2. Configure Button GPIOs (SW1 GPIO 9, SW2 GPIO 10)
    gpio_config_t btn_conf = {};
    btn_conf.pin_bit_mask = (1ULL << KEYFOB_PIN_BTN_ARM_N) | (1ULL << KEYFOB_PIN_BTN_SOS_N);
    btn_conf.mode         = GPIO_MODE_INPUT;
    btn_conf.pull_up_en   = GPIO_PULLUP_ENABLE;
    btn_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    btn_conf.intr_type    = GPIO_INTR_DISABLE;
    gpio_config(&btn_conf);

    // 3. Initialize Peripherals
    Ws2812bLed::instance().init();
    Ws2812bLed::instance().set_mode(KEYFOB_LED_STANDBY_BREATHING_GREEN);

    BuzzerDriver::instance().init();
    BuzzerDriver::instance().play_tone(KEYFOB_BUZZER_FREQ_ARM, 50); // Power-on chirp

    KeyfobPowerManager::instance().init();

    Sx1262LoRa::instance().init();
    Sx1262LoRa::instance().set_alarm_callback(on_lora_alarm_received);

    KeyfobBle::instance().init();
    KeyfobBle::instance().set_remote_command_callback(on_ble_remote_command);

    // 4. Start Main Execution Task
    xTaskCreatePinnedToCore(
        keyfob_main_task,
        "keyfob_task",
        4096,
        nullptr,
        5,
        nullptr,
        0
    );
}
