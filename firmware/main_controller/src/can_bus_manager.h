#pragma once

#include "esp_err.h"
#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Initialize the TI TCAN334G TWAI (CAN-Bus) Driver on GPIO 19 (TX) and GPIO 20 (RX).
 * Configured in Listen-Only mode by default to ensure zero interference with vehicle ECUs.
 */
esp_err_t can_bus_manager_init(void);

/**
 * @brief FreeRTOS Task for handling incoming CAN-Bus frames (wheel speed, RPM, telemetry).
 */
void task_can_bus_manager(void *pvParameters);

/**
 * @brief Transmit low battery alert frame for Handlebar Remote to motorcycle TFT display.
 * @param battery_pct Current battery percentage of CR2032 button cell.
 */
void can_bus_send_remote_battery_warning(uint8_t battery_pct);

/**
 * @brief Check if active CAN-bus traffic is being received.
 */
bool can_bus_is_connected(void);

/**
 * @brief Get last received vehicle speed from CAN bus.
 */
float can_bus_get_vehicle_speed_kmh(void);

#ifdef __cplusplus
}
#endif
