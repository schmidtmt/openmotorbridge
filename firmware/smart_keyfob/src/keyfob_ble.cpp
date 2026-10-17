#include "keyfob_ble.h"
#include "keyfob_config.h"
#include <stdio.h>
#include <string.h>

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
    // 1. Initialize Nordic BLE Controller and Host stack (nRF52840 2.4 GHz)
    // 2. Register Battery Service (UUID 0x180F)
    // 3. Register OpenMotorBridge Security & Pager Service:
    //    UUID: 23d113ef-5f78-2315-deef-121200a00000
    //    Chr 1: Keyfob Button State (Notify)
    //    Chr 2: Alarm State Arm/Disarm (Read/Write/Notify)
    //    Chr 3: Silent Pager Trigger (Write) -> Triggers LRA Haptics & Piezo
    m_initialized = true;
    start_advertising();
    return true;
}

void KeyfobBle::start_advertising() {
    // Advertise as "OMB-KEYFOB" with fast 20 ms interval for quick reconnect
}

void KeyfobBle::stop_advertising() {
}

bool KeyfobBle::is_connected() const {
    return m_connected;
}

void KeyfobBle::set_remote_command_callback(keyfob_remote_cmd_cb_t cb) {
    m_cmd_cb = cb;
}

void KeyfobBle::notify_button_event(uint8_t button_id, bool long_press) {
    if (!m_connected) return;
    // Push notification over GATT Characteristic
    (void)button_id;
    (void)long_press;
}

void KeyfobBle::notify_battery_level(uint8_t battery_pct) {
    m_battery_pct = battery_pct;
    // Push SIG 0x180F Battery Level notification
}

void KeyfobBle::notify_alarm_state(bool is_armed) {
    m_is_armed = is_armed;
}

void KeyfobBle::update() {
    // Process BLE events and connection timeouts
}
