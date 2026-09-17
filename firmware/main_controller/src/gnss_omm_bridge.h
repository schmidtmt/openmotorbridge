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
 * @brief Prüft, ob Heck-Pod 3 über UART1 aktiv antwortet
 */
bool gnss_bridge_is_pod3_connected(void);

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
 * @brief Sendet ein LoRa 868 MHz Alarmanlagen-Notrufpaket (TYPE_BIKE_ALARM = 0xFE)
 * Wird ausgelöst bei Erschütterung im Parkmodus oder Werksalarm (bcm_alarm_triggered).
 * @param alarm_source 0x01: OEM BCM Alarm, 0x02: OMB IMU Erschütterung, 0x03: Koffer-Reed / Kassettenhebeln, 0x04: Test-Alarm
 * @param lat Breitengrad (0.0f = aktuelle GPS Position verwenden)
 * @param lon Längengrad (0.0f = aktuelle GPS Position verwenden)
 */
esp_err_t omm_broadcast_bike_alarm(uint8_t alarm_source, float lat, float lon);

typedef struct {
    bool paired;
    uint8_t pager_mac[6];
    uint8_t aes_key[16];
    uint32_t tx_seq;
    bool buddy_mesh_relay;
    bool keyfob_present; // Detected within BLE RSSI threshold (> -65 dBm)
    uint8_t battery_pct;
    int8_t rssi_dbm;
} smart_keyfob_state_t;

/**
 * @brief Koppelt einen neuen 2-in-1 LoRa Smart-Keyfob mit generiertem AES-128 Schlüssel
 */
esp_err_t smart_keyfob_pair(const uint8_t *mac, const uint8_t *aes_key);

/**
 * @brief Sendet einen Test-Alarm an den gekoppelten Smart-Keyfob (LRA Haptik + LED)
 */
esp_err_t smart_keyfob_send_test_alert(void);

/**
 * @brief Aktiviert oder deaktiviert das Weiterleiten des Alarms an das Gruppen-Mesh (Buddy-Alarm)
 */
void smart_keyfob_set_buddy_relay(bool enable);

/**
 * @brief Aktualisiert den BLE-Präsenzstatus des Smart-Keyfobs (Zero-False-Alarm)
 */
void smart_keyfob_update_presence(bool present, int8_t rssi, uint8_t battery);

/**
 * @brief Liefert den aktuellen Status des gekoppelten Smart-Keyfobs
 */
smart_keyfob_state_t* smart_keyfob_get_state(void);

/**
 * @brief FreeRTOS Task zur Verarbeitung des UART-Streams von Pod 3 (Core 0)
 */
void task_rear_pod_bridge(void *pvParameters);

#ifdef __cplusplus
}
#endif
