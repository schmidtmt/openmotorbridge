#pragma once

#include <stdbool.h>
#include <stdint.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Initialisiert den Dual-Mode Cockpit Wi-Fi Fallback SoftAP im WIFI_MODE_APSTA.
 *        Behält Station-Interface auf Kanal 1 für unterbrechungsfreies ESP-NOW bei.
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

#ifdef __cplusplus
}
#endif
