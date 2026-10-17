#include <stdio.h>
#include <string.h>

#include "keyfob_config.h"
#include "keyfob_ble.h"
#include "sx1262_lora.h"
#include "drv2605l_haptics.h"
#include "buzzer_driver.h"
#include "ws2812b_led.h"
#include "power_manager.h"

static bool s_is_armed = false;
static bool s_alarm_triggered = false;
static uint32_t s_idle_sleep_timer_ms = 0;

// Callback: LoRa Security Alarm received from Central Box (up to 4.5 km range)
static void on_lora_alarm_received(const KeyfobLoRaAlarmPkt& pkt) {
    if (pkt.header != 0xFE) return;

    s_alarm_triggered = true;

    // 1. Silent Pager Haptic Alert: Strong LRA vibration pulse in pocket
    Drv2605lHaptics::instance().play_effect(HAPTIC_ALARM_PULSE);

    // 2. Acoustic Buzzer Siren
    BuzzerDriver::instance().play_pattern(BUZZER_PATTERN_ALARM_SIREN);

    // 3. WS2812B LED Strobe Red
    Ws2812bLed::instance().set_mode(KEYFOB_LED_ALARM_STROBE_RED);
}

// Callback: Remote Command from Smartphone PWA via BLE
static void on_ble_remote_command(uint8_t cmd, uint8_t param) {
    if (cmd == 0x20) { // Arm / Disarm command
        s_is_armed = (param != 0);
        Drv2605lHaptics::instance().play_effect(s_is_armed ? HAPTIC_CLICK_CONFIRM : HAPTIC_CLICK_DISARM);
        BuzzerDriver::instance().play_pattern(s_is_armed ? BUZZER_PATTERN_CONFIRM_CHIRP : BUZZER_PATTERN_DISARM_CHIRP);
        Ws2812bLed::instance().set_mode(s_is_armed ? KEYFOB_LED_ARMED_CYAN : KEYFOB_LED_STANDBY_BREATHING_GREEN);
    }
}

// Button Handler for SW1 (Arm / Disarm)
static void handle_button_arm() {
    s_idle_sleep_timer_ms = 0;

    if (s_alarm_triggered) {
        // Acknowledge & clear active alarm
        s_alarm_triggered = false;
        BuzzerDriver::instance().stop();
        Drv2605lHaptics::instance().stop();
        Ws2812bLed::instance().set_mode(s_is_armed ? KEYFOB_LED_ARMED_CYAN : KEYFOB_LED_STANDBY_BREATHING_GREEN);
        return;
    }

    s_is_armed = !s_is_armed;

    // Haptic & Acoustic User Feedback
    Drv2605lHaptics::instance().play_effect(s_is_armed ? HAPTIC_CLICK_CONFIRM : HAPTIC_CLICK_DISARM);
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
    s_idle_sleep_timer_ms = 0;

    // Trigger Emergency SOS Panic
    Drv2605lHaptics::instance().play_effect(HAPTIC_SOS_PANIC);
    BuzzerDriver::instance().play_pattern(BUZZER_PATTERN_SOS_MORSE);
    Ws2812bLed::instance().set_mode(KEYFOB_LED_SOS_WHITE_RED);

    // Broadcast Emergency SOS Frame
    Sx1262LoRa::instance().send_sos_panic(0x19680001);

    if (KeyfobBle::instance().is_connected()) {
        KeyfobBle::instance().notify_button_event(2, true);
    }
}

int main(void) {
    // 1. Initialize Subsystems
    Ws2812bLed::instance().init();
    Ws2812bLed::instance().set_mode(KEYFOB_LED_STANDBY_BREATHING_GREEN);

    BuzzerDriver::instance().init();
    BuzzerDriver::instance().play_tone(KEYFOB_BUZZER_FREQ_ARM, 50); // Power-on chirp

    Drv2605lHaptics::instance().init();
    Drv2605lHaptics::instance().play_effect(HAPTIC_CLICK_CONFIRM);

    Sx1262LoRa::instance().init();
    Sx1262LoRa::instance().set_alarm_callback(on_lora_alarm_received);

    KeyfobBle::instance().init();
    KeyfobBle::instance().set_remote_command_callback(on_ble_remote_command);

    KeyfobPowerManager::instance().init();

    // 2. Main Event Loop (100 Hz / 10 ms Tick)
    while (1) {
        const uint32_t delta_ms = 10;

        Ws2812bLed::instance().update(delta_ms);
        BuzzerDriver::instance().update(delta_ms);
        Sx1262LoRa::instance().update();
        KeyfobBle::instance().update();
        KeyfobPowerManager::instance().update(delta_ms);

        // Update Qi Wireless Charging Status LED
        if (KeyfobPowerManager::instance().is_charging()) {
            Ws2812bLed::instance().set_mode(KEYFOB_LED_CHARGING_AMBER);
            s_idle_sleep_timer_ms = 0;
        }

        // Low Power Sleep Inactivity Management
        s_idle_sleep_timer_ms += delta_ms;
        if (!s_alarm_triggered && !BuzzerDriver::instance().is_playing() &&
            s_idle_sleep_timer_ms > 30000 && !KeyfobPowerManager::instance().is_charging()) {
            // Turn off LED and enter < 25 µA System ON Sleep
            Ws2812bLed::instance().set_mode(KEYFOB_LED_OFF);
            KeyfobPowerManager::instance().enter_ultra_low_power_sleep();
        }

        // Delay 10 ms
    }

    return 0;
}
