#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    KEY_EVENT_NONE = 0,
    KEY_EVENT_POWER_SHORT,
    KEY_EVENT_POWER_LONG,
    KEY_EVENT_MESH_TOGGLE,
    KEY_EVENT_VOL_UP,
    KEY_EVENT_VOL_DOWN
} OmmKeyEvent_t;

typedef enum {
    LED_MODE_OFF = 0,
    LED_MODE_STANDBY_GREEN,
    LED_MODE_TX_BLUE,
    LED_MODE_RX_CYAN,
    LED_MODE_GROUP_PURPLE,
    LED_MODE_WARN_YELLOW,
    LED_MODE_EMERGENCY_RED
} OmmLedMode_t;

esp_err_t keypad_indicator_init(void);
OmmKeyEvent_t keypad_poll_events(void);
void indicator_set_mode(OmmLedMode_t mode);

#ifdef __cplusplus
}
#endif
