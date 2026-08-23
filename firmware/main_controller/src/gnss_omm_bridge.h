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

enum OmmFeatureBits : uint8_t {
    FEAT_DUAL_MESH_BRIDGE  = (1 << 0), // Sena + Cardo aktiv (+60 Pkt)
    FEAT_LORA_HIGH_POWER   = (1 << 1), // SX1262 +22 dBm PA
    FEAT_GNSS_1PPS_LOCK    = (1 << 2), // Zeitnormal-Master
    FEAT_CAN_TELEMETRY     = (1 << 3), // OBD2 / CAN-Bus aktiv
    FEAT_ENV_MIC_ACTIVE    = (1 << 4), // Front Ambient-Mikrofon aktiv (+5 Pkt)
    FEAT_USV_BAT_BUFFER    = (1 << 5)  // USV Pufferbetrieb möglich
};

/**
 * @brief Berechnet den aktuellen DLE Feature-Vektor
 */
uint8_t omm_get_capabilities_vector(void);

/**
 * @brief Sendet ein Kolonnen-Sirenen-Frühwarnpaket über das Mesh
 */
esp_err_t omm_broadcast_siren_alert(void);

/**
 * @brief FreeRTOS Task zur Verarbeitung des UART-Streams von Pod 3 (Core 0)
 */
void task_rear_pod_bridge(void *pvParameters);

#ifdef __cplusplus
}
#endif
