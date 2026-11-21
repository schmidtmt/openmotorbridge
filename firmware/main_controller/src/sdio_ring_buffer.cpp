#include "sdio_ring_buffer.h"
#include "main_box_config.h"
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/unistd.h>
#include <dirent.h>
#include <limits.h>
#include "esp_vfs_fat.h"
#include "sdmmc_cmd.h"
#include "driver/sdmmc_host.h"
#include "mbedtls/sha256.h"
#include "mbedtls/md.h"
#include "esp_mac.h"
#include "nvs.h"
#include "esp_log.h"

static const char *TAG = "SDIO_STORAGE";

#define MOUNT_POINT         "/sdcard"
#define TRACKS_DIR          "/sdcard/tracks"
#define PURGE_THRESHOLD_MB  200

static FILE *s_current_gpx_file = NULL;
static char s_current_filepath[128] = {0};
static bool s_is_mounted = false;
static bool s_current_locked = false;
static bool s_current_favorite = false;
static uint32_t s_trackpoint_counter = 0;
static sdmmc_card_t *s_card = NULL;
static mbedtls_sha256_context s_sha_ctx;
static uint8_t s_prev_chain_hash[32] = {0};

static void write_and_hash(const char *str) {
    if (!s_current_gpx_file || !str) return;
    size_t len = strlen(str);
    fwrite(str, 1, len, s_current_gpx_file);
    mbedtls_sha256_update(&s_sha_ctx, (const unsigned char *)str, len);
}

esp_err_t sdio_storage_init(void) {
    ESP_LOGI(TAG, "Initializing 4-Bit SDIO Bus & Mounting FAT32 (/sdcard)...");

    esp_vfs_fat_sdmmc_mount_config_t mount_config = {
        .format_if_mount_failed = false,
        .max_files = 8,
        .allocation_unit_size = 16 * 1024,
        .disk_status_check_enable = false,
        .use_one_fat = false
    };

    sdmmc_host_t host = SDMMC_HOST_DEFAULT();
    host.flags = SDMMC_HOST_FLAG_4BIT;
    host.max_freq_khz = SDMMC_FREQ_HIGHSPEED;

    sdmmc_slot_config_t slot_config = SDMMC_SLOT_CONFIG_DEFAULT();
    slot_config.width = 4;
    slot_config.clk = PIN_MAIN_SD_CLK;   // GPIO 35 (U2 Pad 35 -> J2 Pin 5)
    slot_config.cmd = PIN_MAIN_SD_CMD;   // GPIO 36 (U2 Pad 36 -> J2 Pin 3)
    slot_config.d0  = PIN_MAIN_SD_DAT0;  // GPIO 37 (U2 Pad 37 -> J2 Pin 7)
    slot_config.d1  = PIN_MAIN_SD_DAT1;  // GPIO 33 (U2 Pad 33 -> J2 Pin 8)
    slot_config.d2  = PIN_MAIN_SD_DAT2;  // GPIO 34 (U2 Pad 34 -> J2 Pin 1)
    slot_config.d3  = PIN_MAIN_SD_DAT3;  // GPIO 38 (U2 Pad 38 -> J2 Pin 2)
    slot_config.cd  = PIN_MAIN_SD_CD;    // GPIO 39 (U2 Pad 39 -> J2 Pin 9)

    esp_err_t ret = esp_vfs_fat_sdmmc_mount(MOUNT_POINT, &host, &slot_config, &mount_config, &s_card);
    if (ret != ESP_OK) {
        ESP_LOGW(TAG, "Hardware SDMMC mount returned %s (no MicroSD inserted or bench mode)", esp_err_to_name(ret));
        s_is_mounted = false;
        return ret;
    }

    s_is_mounted = true;
    mkdir(TRACKS_DIR, 0775);

    ESP_LOGI(TAG, "SDIO Storage mounted successfully. Free Space: %lu MB", (unsigned long)sdio_get_free_space_mb());
    return ESP_OK;
}

esp_err_t sdio_track_start_new(void) {
    if (!s_is_mounted) return ESP_ERR_INVALID_STATE;
    if (s_current_gpx_file) {
        sdio_track_finalize();
    }

    sdio_purge_old_tracks_if_needed();

    snprintf(s_current_filepath, sizeof(s_current_filepath), "%s/tour_%lu.gpx",
             TRACKS_DIR, (unsigned long)esp_log_timestamp());
    s_current_gpx_file = fopen(s_current_filepath, "w");
    if (!s_current_gpx_file) {
        ESP_LOGE(TAG, "Failed to create GPX track file: %s", s_current_filepath);
        return ESP_FAIL;
    }

    s_current_locked = false;
    s_current_favorite = false;
    s_trackpoint_counter = 0;
    mbedtls_sha256_init(&s_sha_ctx);
    mbedtls_sha256_starts(&s_sha_ctx, 0);
    // Include previous segment hash in chain (blockchain-style continuity)
    mbedtls_sha256_update(&s_sha_ctx, s_prev_chain_hash, sizeof(s_prev_chain_hash));

    ESP_LOGI(TAG, "Starting new GPX 2.0 Tour Log: %s", s_current_filepath);
    write_and_hash("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
    write_and_hash("<gpx version=\"1.1\" creator=\"OpenMotorBridge v10.0\" xmlns=\"http://www.topografix.com/GPX/1/1\">\n");
    write_and_hash("  <trk>\n    <name>OMB Motorcycle Tour</name>\n    <trkseg>\n");
    fflush(s_current_gpx_file);

    return ESP_OK;
}

esp_err_t sdio_track_append_point(double lat, double lon, float ele, float speed_kmh, float lean_angle_deg, const char *iso_time) {
    if (!s_current_gpx_file) return ESP_ERR_INVALID_STATE;

    char buf[384];
    snprintf(buf, sizeof(buf),
             "      <trkpt lat=\"%.6f\" lon=\"%.6f\">\n"
             "        <ele>%.1f</ele>\n"
             "        <time>%s</time>\n"
             "        <extensions>\n"
             "          <omb:speed_kmh>%.1f</omb:speed_kmh>\n"
             "          <omb:lean_angle_deg>%.1f</omb:lean_angle_deg>\n"
             "        </extensions>\n"
             "      </trkpt>\n",
             lat, lon, ele, iso_time ? iso_time : "", speed_kmh, lean_angle_deg);
    write_and_hash(buf);

    s_trackpoint_counter++;
    if (s_trackpoint_counter % 20 == 0) {
        fflush(s_current_gpx_file);
    }
    return ESP_OK;
}

esp_err_t sdio_track_add_video_marker(const char *camera_name, uint32_t clip_offset_ms) {
    if (!s_current_gpx_file) return ESP_ERR_INVALID_STATE;

    ESP_LOGI(TAG, "Adding 1-PPS Video Marker to GPX: %s (offset=%lu ms)", camera_name, (unsigned long)clip_offset_ms);
    char buf[256];
    snprintf(buf, sizeof(buf),
             "      <extensions>\n"
             "        <omb:action_event type=\"video_marker\" camera=\"%s\" clip_offset_ms=\"%lu\"/>\n"
             "      </extensions>\n",
             camera_name ? camera_name : "CAM", (unsigned long)clip_offset_ms);
    write_and_hash(buf);
    fflush(s_current_gpx_file);
    return ESP_OK;
}

esp_err_t sdio_track_lock_incident(const char *reason) {
    if (!s_current_gpx_file) return ESP_ERR_INVALID_STATE;
    s_current_locked = true;
    char buf[256];
    snprintf(buf, sizeof(buf),
             "      <extensions>\n"
             "        <omb:incident_lock reason=\"%s\" timestamp_ms=\"%lu\"/>\n"
             "      </extensions>\n",
             reason ? reason : "IMU_CRASH_EVENT", (unsigned long)esp_log_timestamp());
    write_and_hash(buf);
    fflush(s_current_gpx_file);
    ESP_LOGW(TAG, "Current blackbox segment locked as write-protected evidence (%s)", reason ? reason : "CRASH");
    return ESP_OK;
}

esp_err_t sdio_track_lock_favorite(const char *tag) {
    if (!s_current_gpx_file) return ESP_ERR_INVALID_STATE;
    s_current_favorite = true;
    char buf[256];
    snprintf(buf, sizeof(buf),
             "      <extensions>\n"
             "        <omb:favorite_tag name=\"%s\" timestamp_ms=\"%lu\"/>\n"
             "      </extensions>\n",
             tag ? tag : "USER_BOOKMARK", (unsigned long)esp_log_timestamp());
    write_and_hash(buf);
    fflush(s_current_gpx_file);
    ESP_LOGI(TAG, "Current track tagged as protected favorite (%s)", tag ? tag : "USER_BOOKMARK");
    return ESP_OK;
}

esp_err_t sdio_track_finalize(void) {
    if (!s_current_gpx_file) return ESP_OK;

    ESP_LOGI(TAG, "Finalizing & sealing GPX Tour integrity (HMAC-SHA256 seal)...");
    write_and_hash("    </trkseg>\n  </trk>\n");

    uint8_t digest[32];
    mbedtls_sha256_finish(&s_sha_ctx, digest);
    mbedtls_sha256_free(&s_sha_ctx);

    // Retrieve hardware-backed secret key:
    // First attempt to load a provisioned 256-bit secret from secure NVS ("sec_storage" / "hmac_key").
    // If unprovisioned, fall back to device-unique hardware derivation from factory eFuse MAC.
    uint8_t hw_key[32] = {0};
    bool key_from_nvs = false;
    nvs_handle_t nvs_h;
    if (nvs_open("sec_storage", NVS_READONLY, &nvs_h) == ESP_OK) {
        size_t key_len = sizeof(hw_key);
        if (nvs_get_blob(nvs_h, "hmac_key", hw_key, &key_len) == ESP_OK && key_len == 32) {
            key_from_nvs = true;
            ESP_LOGD(TAG, "Using provisioned secure NVS HMAC key for tour integrity sealing");
        }
        nvs_close(nvs_h);
    }

    if (!key_from_nvs) {
        esp_efuse_mac_get_default(hw_key);
        for (int i = 6; i < 32; ++i) {
            hw_key[i] = (uint8_t)(hw_key[i % 6] ^ (0xA5 + i * 7));
        }
    }

    uint8_t sig_bytes[32];
    mbedtls_md_hmac(mbedtls_md_info_from_type(MBEDTLS_MD_SHA256),
                    hw_key, sizeof(hw_key),
                    digest, sizeof(digest),
                    sig_bytes);

    char digest_hex[65];
    char prev_hex[65];
    char sig_hex[65];
    for (int i = 0; i < 32; ++i) {
        snprintf(&digest_hex[i * 2], 3, "%02x", digest[i]);
        snprintf(&prev_hex[i * 2], 3, "%02x", s_prev_chain_hash[i]);
        snprintf(&sig_hex[i * 2], 3, "%02x", sig_bytes[i]);
    }
    memcpy(s_prev_chain_hash, digest, sizeof(digest));

    fprintf(s_current_gpx_file,
            "  <extensions>\n"
            "    <omb:chain_prev_sha256>%s</omb:chain_prev_sha256>\n"
            "    <omb:segment_sha256>%s</omb:segment_sha256>\n"
            "    <omb:hw_hmac_sha256>%s</omb:hw_hmac_sha256>\n"
            "  </extensions>\n"
            "</gpx>\n",
            prev_hex, digest_hex, sig_hex);

    fclose(s_current_gpx_file);
    s_current_gpx_file = NULL;

    // If locked by incident/crash trigger, rename to .crash.gpx; if favorite, rename to .fav.gpx
    if (s_current_locked && strlen(s_current_filepath) > 4) {
        char locked_path[140];
        snprintf(locked_path, sizeof(locked_path), "%.*s.crash.gpx",
                 (int)(strlen(s_current_filepath) - 4), s_current_filepath);
        rename(s_current_filepath, locked_path);
        ESP_LOGW(TAG, "Renamed incident segment to write-protected crash log: %s", locked_path);
    } else if (s_current_favorite && strlen(s_current_filepath) > 4) {
        char fav_path[140];
        snprintf(fav_path, sizeof(fav_path), "%.*s.fav.gpx",
                 (int)(strlen(s_current_filepath) - 4), s_current_filepath);
        rename(s_current_filepath, fav_path);
        ESP_LOGI(TAG, "Renamed favorite segment to write-protected bookmark: %s", fav_path);
    }

    return ESP_OK;
}

static bool is_unprotected_gpx(const char *name) {
    size_t len = strlen(name);
    if (len < 5 || strcmp(name + len - 4, ".gpx") != 0) {
        return false;
    }
    if (strstr(name, ".fav.gpx") != NULL || strstr(name, ".crash.gpx") != NULL) {
        return false;
    }
    return true;
}

esp_err_t sdio_purge_old_tracks_if_needed(void) {
    if (!s_is_mounted) return ESP_ERR_INVALID_STATE;

    for (int iter = 0; iter < 16; ++iter) {
        uint32_t free_mb = sdio_get_free_space_mb();
        if (free_mb >= PURGE_THRESHOLD_MB) {
            break;
        }

        ESP_LOGW(TAG, "BGH Ring-Buffer Purge active (Free space %lu MB < %d MB threshold)...",
                 (unsigned long)free_mb, PURGE_THRESHOLD_MB);

        DIR *dir = opendir(TRACKS_DIR);
        if (!dir) {
            return ESP_FAIL;
        }

        char oldest_path[320] = {0};
        time_t oldest_mtime = LONG_MAX;
        struct dirent *entry = NULL;

        while ((entry = readdir(dir)) != NULL) {
            if (!is_unprotected_gpx(entry->d_name)) {
                continue;
            }
            char candidate[320];
            snprintf(candidate, sizeof(candidate), "%s/%.240s", TRACKS_DIR, entry->d_name);
            struct stat st;
            if (stat(candidate, &st) == 0 && st.st_mtime < oldest_mtime) {
                oldest_mtime = st.st_mtime;
                strncpy(oldest_path, candidate, sizeof(oldest_path) - 1);
            }
        }
        closedir(dir);

        if (oldest_path[0] == '\0') {
            ESP_LOGW(TAG, "No unprotected .gpx files left to purge.");
            break;
        }

        if (unlink(oldest_path) == 0) {
            ESP_LOGI(TAG, "Purged oldest unprotected segment: %s", oldest_path);
        } else {
            ESP_LOGE(TAG, "Failed to unlink %s", oldest_path);
            break;
        }
    }
    return ESP_OK;
}

uint32_t sdio_get_free_space_mb(void) {
    if (!s_is_mounted) {
        return 0;
    }
    uint64_t bytes_total = 0;
    uint64_t bytes_free = 0;
    if (esp_vfs_fat_info(MOUNT_POINT, &bytes_total, &bytes_free) == ESP_OK) {
        return (uint32_t)(bytes_free / (1024ULL * 1024ULL));
    }
    return 0;
}

#include "usb_vehicle_backbone.h"

esp_err_t sdio_serve_sector_request(const UsbSdBlockReqPkt *req, uint8_t target_node) {
    if (!req) return ESP_ERR_INVALID_ARG;

    UsbSdBlockDataPkt resp = {
        .sector_num = req->sector_num,
        .req_tag = req->req_tag,
        .chunk_index = 0,
        .total_chunks = 4,
        .status = 0,
        .data_len = 128
    };

    if (!s_card || !s_is_mounted) {
        resp.status = 3; // No card
        resp.data_len = 0;
        return UsbVehicleBackbone::instance().send_sd_block_data((UsbNodeType)target_node, resp);
    }

    uint8_t sector_buf[512];
    esp_err_t err = sdmmc_read_sectors(s_card, sector_buf, req->sector_num, 1);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to read SD sector %lu: %s", (unsigned long)req->sector_num, esp_err_to_name(err));
        resp.status = 1; // Read error
        resp.data_len = 0;
        return UsbVehicleBackbone::instance().send_sd_block_data((UsbNodeType)target_node, resp);
    }

    for (uint8_t c = 0; c < 4; c++) {
        resp.chunk_index = c;
        resp.status = 0;
        resp.data_len = 128;
        memcpy(resp.data, &sector_buf[c * 128], 128);
        UsbVehicleBackbone::instance().send_sd_block_data((UsbNodeType)target_node, resp);
    }

    ESP_LOGD(TAG, "Served Remote SD Sector %lu in 4 chunks to Node 0x%02X", (unsigned long)req->sector_num, target_node);
    return ESP_OK;
}

