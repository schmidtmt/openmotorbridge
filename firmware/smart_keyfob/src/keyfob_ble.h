#pragma once

#include <stdint.h>
#include <stdbool.h>

typedef void (*keyfob_remote_cmd_cb_t)(uint8_t cmd, uint8_t param);

class KeyfobBle {
public:
    static KeyfobBle& instance();

    bool init();
    void start_advertising();
    void stop_advertising();
    bool is_connected() const;

    void set_remote_command_callback(keyfob_remote_cmd_cb_t cb);
    void notify_button_event(uint8_t button_id, bool long_press);
    void notify_battery_level(uint8_t battery_pct);
    void notify_alarm_state(bool is_armed);

    void update();

private:
    KeyfobBle();

    bool m_initialized;
    bool m_connected;
    bool m_is_armed;
    uint8_t m_battery_pct;
    keyfob_remote_cmd_cb_t m_cmd_cb;
};
