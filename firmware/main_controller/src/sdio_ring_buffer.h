#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Initialisiert das 4-Bit SDIO Interface und mountet das FAT32 Dateisystem
 */
esp_err_t sdio_storage_init(void);

/**
 * @brief Startet eine neue GPX-Touraufzeichnung in /tracks/
 */
esp_err_t sdio_track_start_new(void);

/**
 * @brief Schreibt einen GPS/IMU Telemetriepunkt in die aktuelle GPX-Datei
 */
esp_err_t sdio_track_append_point(double lat, double lon, float ele, float speed_kmh, float lean_angle_deg, const char *iso_time);

/**
 * @brief Fügt einen Actioncam Video-Marker mit 1-PPS Zeitstempel ein
 */
esp_err_t sdio_track_add_video_marker(const char *camera_name, uint32_t clip_offset_ms);

/**
 * @brief Schließt die aktuelle GPX-Datei sauber ab (Zündung AUS oder Stillstand > 15 min)
 */
esp_err_t sdio_track_finalize(void);

/**
 * @brief BGH-Konformer Purge-Manager: Löscht älteste ungeschützte GPX-Dateien bei < 200 MB
 */
esp_err_t sdio_purge_old_tracks_if_needed(void);

/**
 * @brief Gibt den freien Speicherplatz der MicroSD-Karte in Megabytes zurück
 */
uint32_t sdio_get_free_space_mb(void);

#ifdef __cplusplus
}
#endif
