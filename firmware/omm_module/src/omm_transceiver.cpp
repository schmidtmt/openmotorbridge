#include "omm_transceiver.h"
#include "omm_module_config.h"
#include "esp_log.h"
#include "esp_wifi.h"
#include "esp_now.h"
#include "nvs_flash.h"
#include <string.h>

static const char *TAG = "OMM_RF";

static omm_audio_rx_cb_t s_rx_callback = NULL;
static bool s_ptt_active = false;
static OmmMeshState_t s_mesh_mode = OMM_MESH_OPEN_GROUP;
static uint8_t s_active_peers = 1;
static uint8_t s_broadcast_mac[6] = { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF };

static void esp_now_recv_cb(const esp_now_recv_info_t *recv_info, const uint8_t *data, int len) {
    if (!data || len < 4) return;

    uint8_t packet_type = data[0];
    if (packet_type == OMM_TYPE_AUDIO_RTP) {
        // Voice Frame: [0: TYPE] [1: SENDER_ID] [2..len-1: PCM Audio Data]
        if (s_rx_callback && len > 2) {
            uint8_t sender = data[1];
            size_t sample_count = (len - 2) / sizeof(int16_t);
            s_rx_callback((const int16_t *)(data + 2), sample_count, sender);
        }
    } else if (packet_type == OMM_TYPE_DLE_BEACON) {
        // DLE Heartbeat beacon
        s_active_peers = (s_active_peers < OMM_MESH_MAX_PEERS) ? s_active_peers + 1 : OMM_MESH_MAX_PEERS;
    } else if (packet_type == OMM_TYPE_EMERGENCY) {
        ESP_LOGW(TAG, "🚨 OMM EMERGENCY ALERT RECEIVED VIA 2.4 GHz MESH!");
    }
}

esp_err_t omm_transceiver_init(omm_audio_rx_cb_t rx_callback) {
    s_rx_callback = rx_callback;
    ESP_LOGI(TAG, "Initializing 2.4 GHz ESP-NOW Mesh Transceiver...");

    // Initialize NVS
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        nvs_flash_erase();
        ret = nvs_flash_init();
    }
    if (ret != ESP_OK) return ret;

    // Wi-Fi Station Mode for ESP-NOW
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ret = esp_wifi_init(&cfg);
    if (ret != ESP_OK) return ret;

    ret = esp_wifi_set_storage(WIFI_STORAGE_RAM);
    if (ret != ESP_OK) return ret;
    ret = esp_wifi_set_mode(WIFI_MODE_STA);
    if (ret != ESP_OK) return ret;
    ret = esp_wifi_start();
    if (ret != ESP_OK) return ret;
    ret = esp_wifi_set_channel(OMM_MESH_DEFAULT_CHAN, WIFI_SECOND_CHAN_NONE);
    if (ret != ESP_OK) return ret;

    // Initialize ESP-NOW
    ret = esp_now_init();
    if (ret != ESP_OK) return ret;

    ret = esp_now_register_recv_cb(esp_now_recv_cb);
    if (ret != ESP_OK) return ret;

    // Add Broadcast Peer
    esp_now_peer_info_t peer_info = {};
    memcpy(peer_info.peer_addr, s_broadcast_mac, 6);
    peer_info.channel = OMM_MESH_DEFAULT_CHAN;
    peer_info.ifidx = WIFI_IF_STA;
    peer_info.encrypt = false;
    ret = esp_now_add_peer(&peer_info);
    if (ret != ESP_OK) return ret;

    ESP_LOGI(TAG, "✓ OMM 2.4 GHz Transceiver ready (Channel %d).", OMM_MESH_DEFAULT_CHAN);
    return ESP_OK;
}

esp_err_t omm_transceiver_send_audio(const int16_t *samples, size_t count) {
    if (!s_ptt_active || !samples || count == 0) return ESP_OK;

    // Pack into OMM_TYPE_AUDIO_RTP frame
    uint8_t frame_buf[250];
    frame_buf[0] = OMM_TYPE_AUDIO_RTP;
    frame_buf[1] = 0x09; // Local node ID short (PCBA 09 OMM)
    
    size_t audio_bytes = count * sizeof(int16_t);
    if (audio_bytes > sizeof(frame_buf) - 2) {
        audio_bytes = sizeof(frame_buf) - 2;
    }
    memcpy(frame_buf + 2, samples, audio_bytes);

    return esp_now_send(s_broadcast_mac, frame_buf, audio_bytes + 2);
}

void omm_transceiver_set_ptt(bool ptt_active) {
    s_ptt_active = ptt_active;
    ESP_LOGI(TAG, "OMM PTT State changed -> %s", ptt_active ? "TRANSMITTING (TX)" : "LISTENING (RX)");
}

bool omm_transceiver_is_ptt(void) {
    return s_ptt_active;
}

void omm_transceiver_set_mesh_mode(OmmMeshState_t mode) {
    s_mesh_mode = mode;
}

OmmMeshState_t omm_transceiver_get_mesh_mode(void) {
    return s_mesh_mode;
}

uint8_t omm_transceiver_get_active_peers(void) {
    return s_active_peers;
}
