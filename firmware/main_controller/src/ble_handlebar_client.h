#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef void (*handlebar_button_cb_t)(uint8_t button_id, bool long_press);
typedef void (*handlebar_battery_cb_t)(uint8_t battery_percent);

/**
 * @brief Initialisiert den BLE Central Client für den drahtlosen Lenkertaster
 */
esp_err_t ble_handlebar_client_init(handlebar_button_cb_t btn_cb, handlebar_battery_cb_t bat_cb);

/**
 * @brief Gibt den aktuellen Batteriestand (0-100%) des Lenkertasters zurück (SIG 0x180F)
 */
uint8_t ble_handlebar_get_battery_level(void);

/**
 * @brief Prüft, ob der Lenkertaster aktuell über BLE verbunden ist
 */
bool ble_handlebar_is_connected(void);

#ifdef __cplusplus
}
#endif
