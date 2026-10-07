#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

typedef enum {
    KEY_EVENT_NONE = 0,
    KEY_EVENT_PTT_PRESS,      // SW1 Pressed (Start TX)
    KEY_EVENT_PTT_RELEASE,    // SW1 Released (Stop TX)
    KEY_EVENT_PTT_LONG,       // SW1 Held > 3s (Power Down / Sleep)
    KEY_EVENT_MODE_TOGGLE,    // SW2 Pressed (Toggle Analog <-> DMR)
    KEY_EVENT_CH_UP,          // SW3 Pressed (CH+)
    KEY_EVENT_CH_DOWN         // SW4 Pressed (CH-)
} Omm446KeyEvent_t;

typedef enum {
    LED_MODE_OFF = 0,
    LED_MODE_RX_STANDBY_ANALOG, // Soft breathing Green
    LED_MODE_RX_STANDBY_DMR,    // Soft breathing Cyan
    LED_MODE_RX_ACTIVE_ANALOG,  // Solid bright Green
    LED_MODE_RX_ACTIVE_DMR,     // Solid bright Cyan
    LED_MODE_TX_ANALOG,         // Solid bright Red
    LED_MODE_TX_DMR,            // Solid bright Blue
    LED_MODE_MODE_SWITCH,       // Purple Flash
    LED_MODE_CHANNEL_CHANGE,    // Amber Flash
    LED_MODE_BATTERY_LOW,       // Fast Red Flash
    LED_MODE_CHARGING           // Amber Breathe
} Omm446LedMode_t;

esp_err_t keypad_indicator_init(void);

Omm446KeyEvent_t keypad_poll_events(void);

void indicator_set_mode(Omm446LedMode_t mode);

void indicator_update(void); // Call every 20ms for smooth animations
