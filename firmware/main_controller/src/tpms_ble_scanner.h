#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    TPMS_WHEEL_FRONT = 0,
    TPMS_WHEEL_REAR  = 1
} tpms_wheel_pos_t;

typedef struct {
    float pressure_bar;
    int8_t temp_c;
    uint8_t battery_pct;
    uint8_t sensor_mac[6];
    uint32_t last_seen_ms;
    bool valid;
} tpms_sensor_val_t;

/**
 * @brief Initialisiert den passiven BLE GAP Scanner für Ventilkappen
 *        (FOBO Bike 2, Deelife, TireMinder).
 */
esp_err_t tpms_ble_scanner_init(void);

/**
 * @brief Startet oder stoppt den kontinuierlichen passiven BLE Scan
 */
esp_err_t tpms_ble_scanner_set_active(bool active);

/**
 * @brief Startet 15-sekündigen Sensor-Anlernmodus (speichert Sensor-MACs im NVS)
 */
esp_err_t tpms_ble_scanner_start_learn(tpms_wheel_pos_t pos);

/**
 * @brief Gibt die aktuellen Messwerte für Vorderrad und Hinterrad zurück
 */
bool tpms_ble_scanner_get_values(tpms_sensor_val_t *out_front, tpms_sensor_val_t *out_rear);

#ifdef __cplusplus
}
#endif
