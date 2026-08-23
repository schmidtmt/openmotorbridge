#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    float v_ign_volts;
    float v_bat_volts;
    uint8_t remote_bat_pct;
    uint8_t operation_mode;
    bool port1_active;
    bool port2_active;
    bool pod3_gnss_fix;
    float lean_angle_deg;
} SystemTelemetry_t;

/**
 * @brief Initialisiert den NimBLE GATT Server für die WebBLE PWA
 */
esp_err_t ble_server_init(void);

/**
 * @brief Sendet ein Telemetrie-Update an verbundene PWA-Clients
 */
void ble_server_notify_telemetry(const SystemTelemetry_t *telemetry);

/**
 * @brief FreeRTOS Task für NimBLE Server Host (Core 0)
 */
void task_ble_services(void *pvParameters);

#ifdef __cplusplus
}
#endif
