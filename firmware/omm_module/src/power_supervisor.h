#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    float    v_bat;          // Battery Voltage in Volts (3.0 .. 4.2V)
    uint8_t  battery_pct;    // 0 .. 100%
    float    temp_celsius;   // NTC Temperature in °C
    bool     is_charging;    // True if BQ24075 is actively charging via USB-C
    bool     is_vbus_present;// True if 5V USB-C connected
    bool     jeita_fault;    // True if outside 0..45°C window
} OmmPowerStatus_t;

esp_err_t power_supervisor_init(void);
void power_supervisor_poll(OmmPowerStatus_t *status);
void power_enter_deep_sleep(void);

#ifdef __cplusplus
}
#endif
