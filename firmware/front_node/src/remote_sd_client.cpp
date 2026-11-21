#include "remote_sd_client.h"
#include <string.h>
#include "esp_log.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"
#include "usb_vehicle_backbone.h"

static const char *TAG = "REMOTE_SD_CLIENT";

struct CachedSector {
    uint32_t sector_num;
    uint8_t  data[512];
    uint8_t  chunks_received; // Bitmask of chunks 0..3 received
    uint64_t last_accessed_us;
    bool     valid;
    RemoteSdSectorReadyCallback cb;
};

static struct {
    CachedSector cache[REMOTE_SD_CACHE_SECTORS];
    SemaphoreHandle_t mutex;
    uint16_t next_req_tag;
    bool     initialized;
} s_sd_client = {0};

esp_err_t remote_sd_client_init(void) {
    ESP_LOGI(TAG, "Initializing Remote SD Card Client (PCBA 05 -> PCBA 01)...");

    s_sd_client.mutex = xSemaphoreCreateMutex();
    if (!s_sd_client.mutex) {
        return ESP_ERR_NO_MEM;
    }

    for (int i = 0; i < REMOTE_SD_CACHE_SECTORS; i++) {
        s_sd_client.cache[i].valid = false;
        s_sd_client.cache[i].chunks_received = 0;
    }

    s_sd_client.next_req_tag = 1;
    s_sd_client.initialized = true;

    // Register callback on USB backbone for COMM_06
    UsbVehicleBackbone::instance().set_sd_block_data_callback([](const UsbSdBlockDataPkt &pkt, UsbNodeType source) {
        remote_sd_client_handle_block_data(&pkt);
    });

    ESP_LOGI(TAG, "✅ Remote SD Client online (LRU Cache: %d sectors / 8 KB).", REMOTE_SD_CACHE_SECTORS);
    return ESP_OK;
}

esp_err_t remote_sd_client_request_sector(uint32_t sector_num, uint8_t flags, RemoteSdSectorReadyCallback cb) {
    if (!s_sd_client.initialized) return ESP_ERR_INVALID_STATE;

    if (xSemaphoreTake(s_sd_client.mutex, pdMS_TO_TICKS(50)) != pdTRUE) {
        return ESP_ERR_TIMEOUT;
    }

    // Check if sector already in cache
    for (int i = 0; i < REMOTE_SD_CACHE_SECTORS; i++) {
        if (s_sd_client.cache[i].valid && s_sd_client.cache[i].sector_num == sector_num) {
            s_sd_client.cache[i].last_accessed_us = esp_timer_get_time();
            xSemaphoreGive(s_sd_client.mutex);
            if (cb) cb(sector_num, true);
            return ESP_OK;
        }
    }

    // Find an empty slot or oldest LRU slot
    int victim_idx = 0;
    uint64_t oldest_us = UINT64_MAX;
    for (int i = 0; i < REMOTE_SD_CACHE_SECTORS; i++) {
        if (!s_sd_client.cache[i].valid) {
            victim_idx = i;
            break;
        }
        if (s_sd_client.cache[i].last_accessed_us < oldest_us) {
            oldest_us = s_sd_client.cache[i].last_accessed_us;
            victim_idx = i;
        }
    }

    s_sd_client.cache[victim_idx].sector_num = sector_num;
    s_sd_client.cache[victim_idx].chunks_received = 0;
    s_sd_client.cache[victim_idx].valid = false;
    s_sd_client.cache[victim_idx].last_accessed_us = esp_timer_get_time();
    s_sd_client.cache[victim_idx].cb = cb;

    uint16_t tag = s_sd_client.next_req_tag++;
    xSemaphoreGive(s_sd_client.mutex);

    // Send COMM_05 request to Central Box
    UsbSdBlockReqPkt req = {
        .sector_num = sector_num,
        .req_tag = tag,
        .chunk_index = 0,
        .flags = flags
    };

    ESP_LOGD(TAG, "Requesting SD Sector %lu via USB Backbone (Tag %u)...", (unsigned long)sector_num, tag);
    return UsbVehicleBackbone::instance().send_sd_block_req(req);
}

void remote_sd_client_handle_block_data(const UsbSdBlockDataPkt *pkt) {
    if (!pkt || !s_sd_client.initialized) return;

    if (xSemaphoreTake(s_sd_client.mutex, pdMS_TO_TICKS(50)) != pdTRUE) {
        return;
    }

    for (int i = 0; i < REMOTE_SD_CACHE_SECTORS; i++) {
        if (s_sd_client.cache[i].sector_num == pkt->sector_num) {
            uint8_t chunk = pkt->chunk_index;
            if (chunk < 4 && pkt->data_len <= 128) {
                size_t offset = chunk * 128;
                memcpy(&s_sd_client.cache[i].data[offset], pkt->data, pkt->data_len);
                s_sd_client.cache[i].chunks_received |= (1 << chunk);

                // All 4 chunks (512 bytes) received?
                if (s_sd_client.cache[i].chunks_received == 0x0F) {
                    s_sd_client.cache[i].valid = true;
                    s_sd_client.cache[i].last_accessed_us = esp_timer_get_time();
                    RemoteSdSectorReadyCallback cb = s_sd_client.cache[i].cb;
                    xSemaphoreGive(s_sd_client.mutex);

                    ESP_LOGD(TAG, "✅ SD Sector %lu completely received & cached (512B)", (unsigned long)pkt->sector_num);
                    if (cb) cb(pkt->sector_num, true);
                    return;
                }
            }
            break;
        }
    }

    xSemaphoreGive(s_sd_client.mutex);
}

bool remote_sd_client_read_cache(uint32_t sector_num, uint8_t *out_buffer, size_t max_len) {
    if (!out_buffer || max_len < 512 || !s_sd_client.initialized) return false;

    if (xSemaphoreTake(s_sd_client.mutex, pdMS_TO_TICKS(50)) != pdTRUE) {
        return false;
    }

    for (int i = 0; i < REMOTE_SD_CACHE_SECTORS; i++) {
        if (s_sd_client.cache[i].valid && s_sd_client.cache[i].sector_num == sector_num) {
            memcpy(out_buffer, s_sd_client.cache[i].data, 512);
            s_sd_client.cache[i].last_accessed_us = esp_timer_get_time();
            xSemaphoreGive(s_sd_client.mutex);
            return true;
        }
    }

    xSemaphoreGive(s_sd_client.mutex);
    return false;
}

bool remote_sd_client_is_ready(void) {
    return UsbVehicleBackbone::instance().is_peer_online(USB_NODE_CENTRAL_BOX);
}

