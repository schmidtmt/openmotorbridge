#pragma once

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include "esp_err.h"
#include "usb_backbone_types.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge v10.0 - Remote SD Card Client (PCBA 05 Front Node)
// Requests offline map vector tiles and HUD graphics from Central Box (PCBA 01)
// over 4-Wire USB 2.0 Backbone (COMM_05 & COMM_06)
// =============================================================================

#define REMOTE_SD_CACHE_SECTORS  16 // In-memory LRU cache (8 KB)

typedef void (*RemoteSdSectorReadyCallback)(uint32_t sector_num, bool success);

/**
 * @brief Initialisiert den Remote-SD Client und reserviert den Cache-Speicher
 */
esp_err_t remote_sd_client_init(void);

/**
 * @brief Fordert einen 512-Byte Sektor von der Zentralbox-SD-Karte an (COMM_05)
 * @param sector_num LBA Sektoradresse auf der SD-Karte
 * @param flags Prioritäts-Flags (z.B. HUD-Icons vs. Offline-Karte)
 * @param cb Optionaler Benachrichtigungs-Callback bei Fertigstellung
 */
esp_err_t remote_sd_client_request_sector(uint32_t sector_num, uint8_t flags, RemoteSdSectorReadyCallback cb);

/**
 * @brief Verarbeitet ein von der Zentralbox empfangenes Datensegment (COMM_06)
 */
void remote_sd_client_handle_block_data(const UsbSdBlockDataPkt *pkt);

/**
 * @brief Liest einen zuvor geladenen Sektor aus dem lokalen Front-Node Cache
 * @return true wenn im Cache vorhanden, false wenn noch nicht geladen
 */
bool remote_sd_client_read_cache(uint32_t sector_num, uint8_t *out_buffer, size_t max_len);

/**
 * @brief Gibt an, ob der Remote-SD Dienst auf der Zentralbox erreichbar ist
 */
bool remote_sd_client_is_ready(void);

#ifdef __cplusplus
}
#endif

