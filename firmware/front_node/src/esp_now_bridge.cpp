#include "esp_now_bridge.h"
#include "front_node_config.h"
#include "esp_wifi.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include <string.h>

static const char* TAG = "ESPNOW_BRIDGE";

// Broadcast MAC fallback
static const uint8_t s_broadcast_mac[6] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

EspNowBridge& EspNowBridge::instance() {
    static EspNowBridge inst;
    return inst;
}

EspNowBridge::EspNowBridge()
    : m_peer_registered(false)
    , m_link_active(false)
    , m_tx_success_count(0)
    , m_tx_fail_count(0)
    , m_cmd_callback(nullptr)
{
    memcpy(m_peer_mac, s_broadcast_mac, 6);
}

void EspNowBridge::on_data_sent(const uint8_t* mac_addr, esp_now_send_status_t status) {
    EspNowBridge& self = instance();
    if (status == ESP_NOW_SEND_SUCCESS) {
        self.m_tx_success_count++;
        self.m_link_active = true;
    } else {
        self.m_tx_fail_count++;
    }
}

void EspNowBridge::on_data_recv(const esp_now_recv_info_t* recv_info, const uint8_t* data, int len) {
    EspNowBridge& self = instance();
    if (!data || len < 2) return;

    uint8_t protocol_ver = data[0];
    uint8_t pkt_type = data[1];

    if (protocol_ver != FRONT_NODE_PROTOCOL_VER) {
        ESP_LOGW(TAG, "Mismatched protocol version: 0x%02X", protocol_ver);
        return;
    }

    if (self.m_cmd_callback) {
        self.m_cmd_callback(pkt_type, data + 2, len - 2);
    }
}

bool EspNowBridge::init(const uint8_t* central_box_mac) {
    // 1. Initialize NVS (required by Wi-Fi)
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        nvs_flash_erase();
        ret = nvs_flash_init();
    }

    // 2. Initialize Wi-Fi in Station mode
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));
    ESP_ERROR_CHECK(esp_wifi_set_storage(WIFI_STORAGE_RAM));
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_start());
    ESP_ERROR_CHECK(esp_wifi_set_channel(ESPNOW_WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE));

    // 3. Initialize ESP-NOW
    ret = esp_now_init();
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "esp_now_init failed: %s", esp_err_to_name(ret));
        return false;
    }

    esp_now_register_send_cb(on_data_sent);
    esp_now_register_recv_cb(on_data_recv);

    // 4. Register Peer (Central Box MAC or Broadcast)
    if (central_box_mac) {
        memcpy(m_peer_mac, central_box_mac, 6);
    }

    esp_now_peer_info_t peer_info = {};
    memcpy(peer_info.peer_addr, m_peer_mac, 6);
    peer_info.channel = ESPNOW_WIFI_CHANNEL;
    peer_info.ifidx = WIFI_IF_STA;
    peer_info.encrypt = false; // Plaintext or AES-128 if keys provided

    ret = esp_now_add_peer(&peer_info);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "esp_now_add_peer failed: %s", esp_err_to_name(ret));
        return false;
    }

    m_peer_registered = true;
    ESP_LOGI(TAG, "ESP-NOW bridge active on Channel %d. Target MAC: %02X:%02X:%02X:%02X:%02X:%02X",
             ESPNOW_WIFI_CHANNEL,
             m_peer_mac[0], m_peer_mac[1], m_peer_mac[2],
             m_peer_mac[3], m_peer_mac[4], m_peer_mac[5]);
    return true;
}

void EspNowBridge::set_command_callback(FrontNodeCmdCallback cb) {
    m_cmd_callback = cb;
}

bool EspNowBridge::send_ptt_event(bool pressed, uint64_t timestamp_us) {
    uint8_t buf[11];
    buf[0] = FRONT_NODE_PROTOCOL_VER;
    buf[1] = PKT_TYPE_PTT_EVENT;
    buf[2] = pressed ? 1 : 0;
    memcpy(&buf[3], &timestamp_us, sizeof(uint64_t));

    esp_err_t res = esp_now_send(m_peer_mac, buf, sizeof(buf));
    return (res == ESP_OK);
}

bool EspNowBridge::send_audio_rms(uint8_t dba, uint32_t raw_rms) {
    uint8_t buf[7];
    buf[0] = FRONT_NODE_PROTOCOL_VER;
    buf[1] = PKT_TYPE_AUDIO_RMS;
    buf[2] = dba;
    memcpy(&buf[3], &raw_rms, sizeof(uint32_t));

    esp_err_t res = esp_now_send(m_peer_mac, buf, sizeof(buf));
    return (res == ESP_OK);
}

bool EspNowBridge::send_ottocast_status(uint8_t state, bool power_on, bool fault, uint32_t cafe_sec) {
    uint8_t buf[9];
    buf[0] = FRONT_NODE_PROTOCOL_VER;
    buf[1] = PKT_TYPE_OTTOCAST_STATUS;
    buf[2] = state;
    buf[3] = power_on ? 1 : 0;
    buf[4] = fault ? 1 : 0;
    memcpy(&buf[5], &cafe_sec, sizeof(uint32_t));

    esp_err_t res = esp_now_send(m_peer_mac, buf, sizeof(buf));
    return (res == ESP_OK);
}

bool EspNowBridge::send_heartbeat() {
    uint8_t buf[2];
    buf[0] = FRONT_NODE_PROTOCOL_VER;
    buf[1] = PKT_TYPE_HEARTBEAT;

    esp_err_t res = esp_now_send(m_peer_mac, buf, sizeof(buf));
    return (res == ESP_OK);
}

bool EspNowBridge::is_linked() const {
    return m_link_active;
}

uint32_t EspNowBridge::get_tx_success_count() const {
    return m_tx_success_count;
}

uint32_t EspNowBridge::get_tx_fail_count() const {
    return m_tx_fail_count;
}
