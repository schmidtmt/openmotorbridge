#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    double latitude;
    double longitude;
    float altitude;
    float speed_kmh;
    float heading_deg;
    float pdop;
    uint8_t satellites_visible;
    bool has_3d_fix;
    char utc_time[24];
} GnssData_t;

/**
 * @brief Initialisiert das High-Speed UART Interface zum Heck-Pod 3 (460.800 Baud)
 */
esp_err_t gnss_omm_bridge_init(void);

/**
 * @brief Gibt die neuesten geparsten GNSS-Positionsdaten zurück
 */
GnssData_t gnss_bridge_get_latest_data(void);

/**
 * @brief Sendet ein OpenMotorMesh Steuer- oder Audioframe an den Heck-Pod 3 Co-Prozessor
 */
esp_err_t gnss_bridge_send_omm_packet(const uint8_t *payload, size_t length);

/**
 * @brief FreeRTOS Task zur Verarbeitung des UART-Streams von Pod 3 (Core 0)
 */
void task_rear_pod_bridge(void *pvParameters);

#ifdef __cplusplus
}
#endif
