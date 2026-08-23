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
 * @brief Startet den Auto-Upload ausstehender GPX-Touren bei Zündung AUS
 * @return ESP_OK bei erfolgreichem Upload oder wenn kein WLAN erreichbar
 */
esp_err_t webdav_trigger_sync_sequence(void);

#ifdef __cplusplus
}
#endif
