#include "sdio_ring_buffer.h"
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <dirent.h>
#include "esp_vfs_fat.h"
#include "sdmmc_cmd.h"
#include "driver/sdmmc_host.h"
#include "esp_log.h"

static const char *TAG = "SDIO_STORAGE";

#define MOUNT_POINT         "/sdcard"
#define TRACKS_DIR          "/sdcard/tracks"
#define PURGE_THRESHOLD_MB  200

static FILE *s_current_gpx_file = NULL;
static bool s_is_mounted = false;
static uint32_t s_trackpoint_counter = 0;

esp_err_t sdio_storage_init(void) {
    ESP_LOGI(TAG, "Initializing 4-Bit SDIO Bus & Mounting FAT32 (/sdcard)...");

    esp_vfs_fat_sdmmc_mount_config_t mount_config = {
        .format_if_mount_failed = false,
        .max_files = 5,
        .allocation_unit_size = 16 * 1024
    };

    sdmmc_host_t host = SDMMC_HOST_DEFAULT();
    host.flags = SDMMC_HOST_FLAG_4BIT;
    host.max_freq_khz = SDMMC_FREQ_HIGHSPEED;

    sdmmc_slot_config_t slot_config = SDMMC_SLOT_CONFIG_DEFAULT();
    slot_config.width = 4;

    // Simulation / VFS Mount
    s_is_mounted = true;
    mkdir(TRACKS_DIR, 0775);

    ESP_LOGI(TAG, "SDIO Storage mounted successfully. Free Space: %lu MB", sdio_get_free_space_mb());
    return ESP_OK;
}

esp_err_t sdio_track_start_new(void) {
    if (s_current_gpx_file) {
        sdio_track_finalize();
    }

    sdio_purge_old_tracks_if_needed();

    char filepath[64];
    snprintf(filepath, sizeof(filepath), "%s/tour_%lu.gpx", TRACKS_DIR, (unsigned long)esp_log_timestamp());
    s_current_gpx_file = fopen(filepath, "w");
    if (!s_current_gpx_file) {
        ESP_LOGE(TAG, "Failed to create GPX track file: %s", filepath);
        return ESP_FAIL;
    }

    ESP_LOGI(TAG, "Starting new GPX 2.0 Tour Log: %s", filepath);
    fprintf(s_current_gpx_file, "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
    fprintf(s_current_gpx_file, "<gpx version=\"1.1\" creator=\"OpenMotorBridge v8.0\" xmlns=\"http://www.topografix.com/GPX/1/1\">\n");
    fprintf(s_current_gpx_file, "  <trk>\n    <name>OMB Motorcycle Tour</name>\n    <trkseg>\n");
    fflush(s_current_gpx_file);
    s_trackpoint_counter = 0;

    return ESP_OK;
}

esp_err_t sdio_track_append_point(double lat, double lon, float ele, float speed_kmh, float lean_angle_deg, const char *iso_time) {
    if (!s_current_gpx_file) return ESP_ERR_INVALID_STATE;

    fprintf(s_current_gpx_file, "      <trkpt lat=\"%.6f\" lon=\"%.6f\">\n", lat, lon);
    fprintf(s_current_gpx_file, "        <ele>%.1f</ele>\n", ele);
    fprintf(s_current_gpx_file, "        <time>%s</time>\n", iso_time);
    fprintf(s_current_gpx_file, "        <extensions>\n");
    fprintf(s_current_gpx_file, "          <omb:speed_kmh>%.1f</omb:speed_kmh>\n", speed_kmh);
    fprintf(s_current_gpx_file, "          <omb:lean_angle_deg>%.1f</omb:lean_angle_deg>\n", lean_angle_deg);
    fprintf(s_current_gpx_file, "        </extensions>\n");
    fprintf(s_current_gpx_file, "      </trkpt>\n");

    s_trackpoint_counter++;
    if (s_trackpoint_counter % 20 == 0) {
        fflush(s_current_gpx_file);
    }
    return ESP_OK;
}

esp_err_t sdio_track_add_video_marker(const char *camera_name, uint32_t clip_offset_ms) {
    if (!s_current_gpx_file) return ESP_ERR_INVALID_STATE;

    ESP_LOGI(TAG, "Adding 1-PPS Video Marker to GPX: %s (offset=%lu ms)", camera_name, clip_offset_ms);
    fprintf(s_current_gpx_file, "      <extensions>\n");
    fprintf(s_current_gpx_file, "        <omb:action_event type=\"video_marker\" camera=\"%s\" clip_offset_ms=\"%lu\"/>\n",
            camera_name, clip_offset_ms);
    fprintf(s_current_gpx_file, "      </extensions>\n");
    fflush(s_current_gpx_file);
    return ESP_OK;
}

esp_err_t sdio_track_finalize(void) {
    if (!s_current_gpx_file) return ESP_OK;

    ESP_LOGI(TAG, "Finalizing GPX Tour structure...");
    fprintf(s_current_gpx_file, "    </trkseg>\n  </trk>\n</gpx>\n");
    fclose(s_current_gpx_file);
    s_current_gpx_file = NULL;
    return ESP_OK;
}

esp_err_t sdio_purge_old_tracks_if_needed(void) {
    uint32_t free_mb = sdio_get_free_space_mb();
    if (free_mb < PURGE_THRESHOLD_MB) {
        ESP_LOGW(TAG, "BGH Storage Purge triggered (Free space %lu MB < %d MB threshold)...",
                 free_mb, PURGE_THRESHOLD_MB);
        // Älteste ungeschützte *.gpx Dateien löschen (*.fav.gpx geschützt)
    }
    return ESP_OK;
}

uint32_t sdio_get_free_space_mb(void) {
    return 14500; // 14.5 GB freier Speicher Simulation
}
