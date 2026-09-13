#pragma once

#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge - Cockpit Wi-Fi AP & Intelligent Routing Gateway
// =============================================================================

typedef enum {
    WIFI_UPLINK_RIDER_PHONE = 0, // Option 3 = 192.168.4.10 for Skyline OS
    WIFI_UPLINK_PAX_PHONE   = 1, // Option 3 = 192.168.4.11 for Skyline OS
    WIFI_UPLINK_OFFLINE     = 2  // No Option 3 pushed to Skyline OS (offline)
} WifiUplinkSource_t;

typedef struct {
    uint8_t mac[6];
    char ip_str[16];
    char hostname[32];
    char role[24];              // "Fahrer-Phone", "Sozius-Phone", "Skyline OS", "Client"
    bool is_uplink;
    uint32_t connected_duration_s;
} WifiClientInfo_t;

/**
 * @brief Initialisiert den Dual-Mode Cockpit Wi-Fi Fallback SoftAP im WIFI_MODE_APSTA.
 *        Behält Station-Interface auf Kanal 1 für unterbrechungsfreies ESP-NOW bei.
 *        Generiert dynamische SSID: OMB-[Modell]-[3-stellige eFuse ID]
 */
esp_err_t cockpit_wifi_fallback_init(void);

/**
 * @brief Schaltet den Wi-Fi SoftAP ein oder aus
 */
esp_err_t cockpit_wifi_fallback_set_enabled(bool enabled);

/**
 * @brief Prüft, ob der Wi-Fi SoftAP aktiv ist
 */
bool cockpit_wifi_fallback_is_enabled(void);

/**
 * @brief Liefert die Anzahl aktuell verbundener Wi-Fi Clients
 */
uint8_t cockpit_wifi_fallback_get_connected_stations(void);

/**
 * @brief Generiert die deterministische Default-SSID: OMB-[Modell]-[3-stellige ID]
 */
esp_err_t cockpit_wifi_generate_default_ssid(char *out_ssid, size_t max_len);

/**
 * @brief Liefert die aktuell aktive SSID (entweder Custom aus NVS oder Default)
 */
esp_err_t cockpit_wifi_get_active_ssid(char *out_ssid, size_t max_len);

/**
 * @brief Setzt eine benutzerdefinierte SSID und WPA2-Passwort im NVS
 */
esp_err_t cockpit_wifi_set_custom_config(const char *custom_ssid, const char *custom_pass);

/**
 * @brief Wählt die aktive Uplink-Quelle für das Routing von Skyline OS
 */
esp_err_t cockpit_wifi_set_uplink_source(WifiUplinkSource_t source);

/**
 * @brief Liefert die aktuell gewählte Uplink-Quelle
 */
WifiUplinkSource_t cockpit_wifi_get_uplink_source(void);

/**
 * @brief Liefert die Tabelle aller aktuell verbundenen Wi-Fi Clients
 */
uint8_t cockpit_wifi_get_client_list(WifiClientInfo_t *out_clients, uint8_t max_clients);

/**
 * @brief Aktualisiert das passive CAN-Modellkürzel (z. B. "Skyline", "HD", "GS")
 */
void cockpit_wifi_notify_can_model(const char *model_tag);

#ifdef __cplusplus
}
#endif

