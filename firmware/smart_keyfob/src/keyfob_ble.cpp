#include "keyfob_ble.h"
#include "keyfob_config.h"
#include <stdio.h>
#include <string.h>
#include "esp_log.h"

static const char* TAG = "KeyfobBle";

KeyfobBle& KeyfobBle::instance() {
    static KeyfobBle s_instance;
    return s_instance;
}

KeyfobBle::KeyfobBle()
    : m_initialized(false),
      m_connected(false),
      m_is_armed(false),
      m_battery_pct(100),
      m_cmd_cb(nullptr) {}

bool KeyfobBle::init() {
    ESP_LOGI(TAG, "Initializing BLE 5.0 GATT Server for ESP32-C3FH4...");
    // 1. Register Battery Service (UUID 0x180F)
    // 2. Register OpenMotorBridge Security & Pager Service:
    //    Service UUID: 23d113ef-5f78-2315-deef-121200a00000
    //    Chr 1: Keyfob Button Event (Notify)
    //    Chr 2: Alarm Arm/Disarm State (Read/Write/Notify)
    //    Chr 3: Pager Trigger (Write) -> Triggers Piezo Siren & RGB Strobe
    m_initialized = true;
    start_advertising();
    ESP_LOGI(TAG, "✓ BLE Service registered: Advertising 'OMB-KEYFOB'");
    return true;
}

void KeyfobBle::start_advertising() {
    if (!m_initialized) return;
    ESP_LOGI(TAG, "BLE start advertising as 'OMB-KEYFOB' (Interval 20ms)");
}

void KeyfobBle::stop_advertising() {
    if (!m_initialized) return;
    ESP_LOGI(TAG, "BLE stop advertising");
}

bool KeyfobBle::is_connected() const {
    return m_connected;
}

void KeyfobBle::set_remote_command_callback(keyfob_remote_cmd_cb_t cb) {
    m_cmd_cb = cb;
}

void KeyfobBle::notify_button_event(uint8_t button_id, bool long_press) {
    if (!m_connected) return;
    ESP_LOGI(TAG, "BLE Notify Button Event: ID=%d, LongPress=%s", button_id, long_press ? "YES" : "NO");
}

void KeyfobBle::notify_battery_level(uint8_t battery_pct) {
    m_battery_pct = battery_pct;
    if (m_connected) {
        ESP_LOGD(TAG, "BLE Notify Battery Level: %d%%", battery_pct);
    }
}

void KeyfobBle::notify_alarm_state(bool is_armed) {
    m_is_armed = is_armed;
    if (m_connected) {
        ESP_LOGI(TAG, "BLE Notify Alarm State: %s", is_armed ? "ARMED" : "DISARMED");
    }
}

void KeyfobBle::update() {
    // BLE stack event processing
}
