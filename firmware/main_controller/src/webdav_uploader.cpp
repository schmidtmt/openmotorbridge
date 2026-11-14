#include "webdav_uploader.h"
#include <stdio.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_http_client.h"

static const char *TAG = "WEBDAV_SYNC";

#define TRACKS_LOCAL_DIR    "/sdcard/tracks"
#define WEBDAV_CHUNK_SIZE   2048

static WebDAVConfig_t s_config = {
    .server_url = "https://cloud.local/remote.php/dav/files/user/omb_tracks/",
    .username = "omb_rider",
    .password = "secure_token",
    .target_dir = "/omb_tracks"
};

static bool s_has_internet_uplink = false;

esp_err_t webdav_uploader_init(void) {
    ESP_LOGI(TAG, "Initializing WebDAV TLS 1.3 Garage-Sync Client...");
    return ESP_OK;
}

void webdav_set_config(const WebDAVConfig_t *config) {
    if (config) {
        s_config = *config;
        ESP_LOGI(TAG, "WebDAV Configuration updated: Target=%s", s_config.server_url);
    }
}

void webdav_set_uplink_status(bool available) {
    s_has_internet_uplink = available;
    ESP_LOGI(TAG, "WebDAV Cloud Uplink Status: %s", available ? "ONLINE (Garage Wi-Fi / Relay)" : "OFFLINE (Autarkic Riding Mode)");
}

bool webdav_is_uplink_ready(void) {
    return s_has_internet_uplink;
}

static esp_err_t webdav_ensure_remote_collection(void) {
    esp_http_client_config_t cfg = {};
    cfg.url = s_config.server_url;
    cfg.username = s_config.username;
    cfg.password = s_config.password;
    cfg.auth_type = HTTP_AUTH_TYPE_BASIC;
    cfg.method = HTTP_METHOD_MKCOL;
    cfg.timeout_ms = 5000;

    esp_http_client_handle_t client = esp_http_client_init(&cfg);
    if (!client) return ESP_FAIL;

    esp_err_t err = esp_http_client_perform(client);
    int status = esp_http_client_get_status_code(client);
    esp_http_client_cleanup(client);

    // 201 Created or 405 Method Not Allowed (already exists) are both valid
    if (err == ESP_OK && (status == 201 || status == 405 || status == 200)) {
        return ESP_OK;
    }
    return err;
}

static esp_err_t webdav_upload_single_file(const char *local_path, const char *filename) {
    struct stat st;
    if (stat(local_path, &st) != 0 || st.st_size <= 0) {
        return ESP_ERR_NOT_FOUND;
    }

    FILE *fp = fopen(local_path, "rb");
    if (!fp) {
        return ESP_FAIL;
    }

    char remote_url[256];
    size_t base_len = strlen(s_config.server_url);
    bool has_slash = (base_len > 0 && s_config.server_url[base_len - 1] == '/');
    snprintf(remote_url, sizeof(remote_url), "%s%s%s",
             s_config.server_url, has_slash ? "" : "/", filename);

    esp_http_client_config_t cfg = {};
    cfg.url = remote_url;
    cfg.username = s_config.username;
    cfg.password = s_config.password;
    cfg.auth_type = HTTP_AUTH_TYPE_BASIC;
    cfg.method = HTTP_METHOD_PUT;
    cfg.timeout_ms = 15000;

    esp_http_client_handle_t client = esp_http_client_init(&cfg);
    if (!client) {
        fclose(fp);
        return ESP_FAIL;
    }

    esp_http_client_set_header(client, "Content-Type", "application/gpx+xml");
    esp_err_t err = esp_http_client_open(client, (int)st.st_size);
    if (err != ESP_OK) {
        esp_http_client_cleanup(client);
        fclose(fp);
        return err;
    }

    uint8_t chunk[WEBDAV_CHUNK_SIZE];
    size_t read_bytes = 0;
    while ((read_bytes = fread(chunk, 1, sizeof(chunk), fp)) > 0) {
        size_t total_written = 0;
        while (total_written < read_bytes) {
            int written = esp_http_client_write(client, (const char *)(chunk + total_written), (int)(read_bytes - total_written));
            if (written <= 0) {
                err = ESP_FAIL;
                break;
            }
            total_written += (size_t)written;
        }
        if (err != ESP_OK) {
            break;
        }
    }
    if (ferror(fp)) {
        ESP_LOGE(TAG, "File read error on %s", local_path);
        err = ESP_FAIL;
    }
    fclose(fp);

    int status = 0;
    if (err == ESP_OK) {
        esp_http_client_fetch_headers(client);
        status = esp_http_client_get_status_code(client);
    }
    esp_http_client_close(client);
    esp_http_client_cleanup(client);

    if (err == ESP_OK && (status == 200 || status == 201 || status == 204)) {
        ESP_LOGI(TAG, "Uploaded %s (%ld bytes) -> HTTP %d", filename, (long)st.st_size, status);
        // Write .uploaded marker so this file is not re-uploaded on next garage sync
        char marker_path[280];
        snprintf(marker_path, sizeof(marker_path), "%s.uploaded", local_path);
        FILE *mfp = fopen(marker_path, "w");
        if (mfp) {
            fprintf(mfp, "HTTP %d\n", status);
            fclose(mfp);
        }
        return ESP_OK;
    }

    ESP_LOGW(TAG, "WebDAV PUT failed for %s (err=%s, status=%d)", filename, esp_err_to_name(err), status);
    return ESP_FAIL;
}

esp_err_t webdav_trigger_sync_sequence(void) {
    ESP_LOGI(TAG, "Checking Garage Wi-Fi / Uplink for WebDAV Auto-Upload sequence...");

    // During active riding, 2.4 GHz Wi-Fi on PCBA 01 remains disabled for 0 dB RF coexistence.
    // Sync only runs in Garage/Post-Ride mode when a verified Home Wi-Fi or PWA uplink is active.
    if (!s_has_internet_uplink) {
        ESP_LOGI(TAG, "No verified Internet uplink active. Keeping GPX logs buffered on MicroSD.");
        return ESP_OK;
    }

    DIR *dir = opendir(TRACKS_LOCAL_DIR);
    if (!dir) {
        ESP_LOGW(TAG, "Local tracks directory (%s) not mounted or empty.", TRACKS_LOCAL_DIR);
        return ESP_OK;
    }

    webdav_ensure_remote_collection();

    struct dirent *entry = NULL;
    uint32_t uploaded_count = 0;
    while ((entry = readdir(dir)) != NULL) {
        size_t len = strlen(entry->d_name);
        if (len < 5 || strcmp(entry->d_name + len - 4, ".gpx") != 0) {
            continue;
        }

        char local_path[320];
        char marker_path[352];
        snprintf(local_path, sizeof(local_path), "%s/%.240s", TRACKS_LOCAL_DIR, entry->d_name);
        snprintf(marker_path, sizeof(marker_path), "%s.uploaded", local_path);

        struct stat mst;
        if (stat(marker_path, &mst) == 0) {
            continue; // Already synced
        }

        if (webdav_upload_single_file(local_path, entry->d_name) == ESP_OK) {
            uploaded_count++;
        }
    }
    closedir(dir);

    ESP_LOGI(TAG, "WebDAV Garage Sync completed (%lu new GPX files uploaded).", (unsigned long)uploaded_count);
    return ESP_OK;
}
