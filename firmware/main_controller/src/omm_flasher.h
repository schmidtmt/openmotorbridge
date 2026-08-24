#pragma once

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    OMM_FLASH_IDLE = 0,
    OMM_FLASH_SYNCING,
    OMM_FLASH_ERASING,
    OMM_FLASH_WRITING,
    OMM_FLASH_VERIFYING,
    OMM_FLASH_SUCCESS,
    OMM_FLASH_FAILED
} OmmFlashState_t;

typedef struct {
    OmmFlashState_t state;
    uint32_t total_bytes;
    uint32_t written_bytes;
    uint8_t progress_percent;
    char last_error[64];
} OmmFlashStatus_t;

/**
 * @brief Initialisiert das OMM UART-Push-Flasher Subsystem
 */
esp_err_t omm_flasher_init(void);

/**
 * @brief Flasht eine Firmware-Binärdatei aus dem Dateisystem (LittleFS / SD-Karte)
 *        transparent über den 460.800 Baud High-Speed UART auf den Heck-Pod ESP32-C3
 * 
 * @param bin_file_path Pfad zur Firmware-Datei (z.B. "/spiffs/omm_rear.bin" oder "/sdcard/firmware/omm_v8.bin")
 * @return esp_err_t ESP_OK bei erfolgreichem Flash und Verifikation, sonst Fehlercode
 */
esp_err_t omm_flasher_push_file(const char *bin_file_path);

/**
 * @brief Flasht ein Firmware-Image aus einem Speicherpuffer
 * 
 * @param data Zeiger auf Binärdaten
 * @param length Länge der Binärdaten in Bytes
 */
esp_err_t omm_flasher_push_buffer(const uint8_t *data, size_t length);

/**
 * @brief Gibt den aktuellen Status und Fortschritt des Flash-Vorgangs zurück
 */
OmmFlashStatus_t omm_flasher_get_status(void);

#ifdef __cplusplus
}
#endif
