#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    char server_url[128]; // z. B. "https://cloud.example.com/remote.php/dav/files/user/omb_tracks/"
    char username[64];
    char password[64];
    char target_dir[64];
    char wifi_ssid[32];   // Garage / Home Wi-Fi SSID
    char wifi_password[64];
} WebDAVConfig_t;

/**
 * @brief Initialisiert das WebDAV Upload Subsystem
 */
esp_err_t webdav_uploader_init(void);

/**
 * @brief Konfiguriert die WebDAV Server-Zugangsdaten
 */
void webdav_set_config(const WebDAVConfig_t *config);

/**
 * @brief Führt den kompletten Post-Ride Garage-Sync durch (WLAN STA Connect, GPX Upload, Disconnect)
 * @param timeout_ms Maximale Zeit für Verbindungsaufbau und Upload in Millisekunden
 * @return ESP_OK bei erfolgreichem Upload oder wenn kein WLAN erreichbar (Graceful Fallback)
 */
esp_err_t webdav_execute_post_ride_garage_sync(uint32_t timeout_ms);

/**
 * @brief Startet den Auto-Upload ausstehender GPX-Touren bei Zündung AUS
 * @return ESP_OK bei erfolgreichem Upload oder wenn kein WLAN erreichbar
 */
esp_err_t webdav_trigger_sync_sequence(void);

/**
 * @brief Aktualisiert den Internet-Uplink-Status für den Cloud-Sync
 */
void webdav_set_uplink_status(bool available);

/**
 * @brief Prüft, ob ein verifizierter Cloud-Uplink bereitsteht
 */
bool webdav_is_uplink_ready(void);

#ifdef __cplusplus
}
#endif
