#include "esp_now_bridge.h"
#include "front_node_config.h"
#include "esp_wifi.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "nvs_flash.h"
#include "nvs.h"
#include <string.h>

static const char* TAG = "ESPNOW_BRIDGE";

#define NVS_NAMESPACE_BINDING "fn_binding"
#define NVS_KEY_CBOX_MAC      "cbox_mac"

// Broadcast MAC fallback
static const uint8_t s_broadcast_mac[6] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

EspNowBridge& EspNowBridge::instance() {
    static EspNowBridge inst;
    return inst;
}

EspNowBridge::EspNowBridge()
    : m_peer_registered(false)
    , m_link_active(false)
    , m_binding_state(BINDING_STATE_UNPAIRED)
    , m_last_rx_heartbeat_us(0)
    , m_tx_success_count(0)
    , m_tx_fail_count(0)
    , m_cmd_callback(nullptr)
{
    memcpy(m_peer_mac, s_broadcast_mac, 6);
}

bool EspNowBridge::load_stored_central_mac(uint8_t* mac_out) {
    if (!mac_out) return false;
    nvs_handle_t handle;
    esp_err_t err = nvs_open(NVS_NAMESPACE_BINDING, NVS_READONLY, &handle);
    if (err != ESP_OK) {
        return false;
    }

    size_t mac_size = 6;
    err = nvs_get_blob(handle, NVS_KEY_CBOX_MAC, mac_out, &mac_size);
    nvs_close(handle);

    if (err != ESP_OK || mac_size != 6) {
        return false;
    }

    // Check if MAC is valid (not 00:00... or FF:FF...)
    bool all_zero = true;
    bool all_ff = true;
    for (int i = 0; i < 6; i++) {
        if (mac_out[i] != 0x00) all_zero = false;
        if (mac_out[i] != 0xFF) all_ff = false;
    }

    return (!all_zero && !all_ff);
}

bool EspNowBridge::save_stored_central_mac(const uint8_t* mac_in) {
    if (!mac_in) return false;
    nvs_handle_t handle;
    esp_err_t err = nvs_open(NVS_NAMESPACE_BINDING, NVS_READWRITE, &handle);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to open NVS namespace '%s' for writing: %s", NVS_NAMESPACE_BINDING, esp_err_to_name(err));
        return false;
    }

    err = nvs_set_blob(handle, NVS_KEY_CBOX_MAC, mac_in, 6);
    if (err == ESP_OK) {
        err = nvs_commit(handle);
    }
    nvs_close(handle);

    if (err == ESP_OK) {
        ESP_LOGI(TAG, "Saved Central Box MAC to NVS: %02X:%02X:%02X:%02X:%02X:%02X",
                 mac_in[0], mac_in[1], mac_in[2], mac_in[3], mac_in[4], mac_in[5]);
        return true;
    } else {
        ESP_LOGE(TAG, "Failed to commit Central Box MAC to NVS: %s", esp_err_to_name(err));
        return false;
    }
}

void EspNowBridge::clear_stored_central_mac() {
    nvs_handle_t handle;
    if (nvs_open(NVS_NAMESPACE_BINDING, NVS_READWRITE, &handle) == ESP_OK) {
        nvs_erase_key(handle, NVS_KEY_CBOX_MAC);
        nvs_commit(handle);
        nvs_close(handle);
        ESP_LOGI(TAG, "Central Box MAC binding erased from NVS.");
    }
}

bool EspNowBridge::set_peer_mac(const uint8_t* mac) {
    if (!mac) return false;

    // If a peer already exists with previous MAC, remove it
    if (m_peer_registered && esp_now_is_peer_exist(m_peer_mac)) {
        esp_now_del_peer(m_peer_mac);
        m_peer_registered = false;
    }

    memcpy(m_peer_mac, mac, 6);

    esp_now_peer_info_t peer_info = {};
    memcpy(peer_info.peer_addr, m_peer_mac, 6);
    peer_info.channel = ESPNOW_WIFI_CHANNEL;
    peer_info.ifidx = WIFI_IF_STA;
    peer_info.encrypt = false;

    esp_err_t ret = esp_now_add_peer(&peer_info);
    if (ret != ESP_OK && ret != ESP_ERR_ESPNOW_EXIST) {
        ESP_LOGE(TAG, "esp_now_add_peer failed: %s", esp_err_to_name(ret));
        return false;
    }

    m_peer_registered = true;
    return true;
}

void EspNowBridge::on_data_sent(const uint8_t* mac_addr, esp_now_send_status_t status) {
    EspNowBridge& self = instance();
    if (status == ESP_NOW_SEND_SUCCESS) {
        self.m_tx_success_count++;
        if (self.m_binding_state == BINDING_STATE_LINKED) {
            self.m_link_active = true;
        }
    } else {
        self.m_tx_fail_count++;
    }
}

void EspNowBridge::on_data_recv(const esp_now_recv_info_t* recv_info, const uint8_t* data, int len) {
    EspNowBridge& self = instance();
    if (!data || len < 2 || !recv_info) return;

    uint8_t protocol_ver = data[0];
    uint8_t pkt_type = data[1];

    if (protocol_ver != FRONT_NODE_PROTOCOL_VER) {
        ESP_LOGW(TAG, "Mismatched protocol version: 0x%02X", protocol_ver);
        return;
    }

    const uint8_t* src_mac = recv_info->src_addr;
    int8_t rssi = recv_info->rx_ctrl ? recv_info->rx_ctrl->rssi : -127;

    // --- A. BINDING & PAIRING BEACONS ---
    if (pkt_type == PKT_TYPE_BINDING_BEACON) {
        if (self.m_binding_state == BINDING_STATE_UNPAIRED) {
            // Case 1: Initial pairing (e.g. home garage commissioning)
            ESP_LOGI(TAG, "✨ Pairing beacon received from Central Box %02X:%02X:%02X:%02X:%02X:%02X (RSSI=%d dBm). Binding...",
                     src_mac[0], src_mac[1], src_mac[2], src_mac[3], src_mac[4], src_mac[5], rssi);

            self.save_stored_central_mac(src_mac);
            self.set_peer_mac(src_mac);
            self.m_binding_state = BINDING_STATE_LINKED;
            self.m_last_rx_heartbeat_us = esp_timer_get_time();
            self.m_link_active = true;

            self.send_binding_ack(src_mac);
            return;
        }
        else if (self.m_binding_state == BINDING_STATE_ORPHAN) {
            // Case 2: Proximity-Rescue after >60s loss of old Central Box
            ESP_LOGI(TAG, "Rescue beacon from Central Box %02X:%02X:%02X:%02X:%02X:%02X received in [ORPHAN] state. RSSI=%d dBm (Threshold=%d dBm)",
                     src_mac[0], src_mac[1], src_mac[2], src_mac[3], src_mac[4], src_mac[5],
                     rssi, PROXIMITY_RSSI_THRESHOLD_DBM);

            if (rssi >= PROXIMITY_RSSI_THRESHOLD_DBM) {
                ESP_LOGI(TAG, "✨ Proximity validation passed! Overwriting Central Box binding to new host.");
                self.save_stored_central_mac(src_mac);
                self.set_peer_mac(src_mac);
                self.m_binding_state = BINDING_STATE_LINKED;
                self.m_last_rx_heartbeat_us = esp_timer_get_time();
                self.m_link_active = true;

                self.send_binding_ack(src_mac);
            } else {
                ESP_LOGW(TAG, "🚫 Proximity validation failed: RSSI=%d dBm is weaker than %d dBm threshold. Proximity rescue rejected.",
                         rssi, PROXIMITY_RSSI_THRESHOLD_DBM);
            }
            return;
        }
        else if (self.m_binding_state == BINDING_STATE_LINKED) {
            // Case 3: Already linked
            if (memcmp(src_mac, self.m_peer_mac, 6) == 0) {
                // Heartbeat / ping from our own Central Box
                self.m_last_rx_heartbeat_us = esp_timer_get_time();
                self.m_link_active = true;
                self.send_binding_ack(src_mac);
            } else {
                // Anti-Hijacking: another box tries to take over while active box is alive!
                ESP_LOGW(TAG, "🛡️ Anti-Hijacking: Rejected foreign pairing beacon from %02X:%02X:%02X:%02X:%02X:%02X while LINKED to active host.",
                         src_mac[0], src_mac[1], src_mac[2], src_mac[3], src_mac[4], src_mac[5]);
            }
            return;
        }
    }

    // --- B. CENTRAL BOX HEARTBEAT ---
    if (pkt_type == PKT_TYPE_HEARTBEAT) {
        if (memcmp(src_mac, self.m_peer_mac, 6) == 0) {
            self.m_last_rx_heartbeat_us = esp_timer_get_time();
            self.m_link_active = true;
            if (self.m_binding_state == BINDING_STATE_ORPHAN) {
                self.m_binding_state = BINDING_STATE_LINKED;
                ESP_LOGI(TAG, "Paired Central Box returned! Restoring state from ORPHAN back to [LINKED].");
            }
        }
        return;
    }

    // --- C. REMOTE UNBIND / FACTORY RESET COMMAND ---
    if (pkt_type == PKT_TYPE_CMD_UNBIND) {
        if (memcmp(src_mac, self.m_peer_mac, 6) == 0 || self.m_binding_state == BINDING_STATE_UNPAIRED) {
            ESP_LOGW(TAG, "Remote unbind command received. Resetting Front Node binding.");
            self.reset_binding();
        }
        return;
    }

    // --- D. REGULAR COMMANDS & TELEMETRY DISPATCH ---
    // Drop non-matching packets if strictly linked
    if (self.m_binding_state == BINDING_STATE_LINKED && memcmp(src_mac, self.m_peer_mac, 6) != 0) {
        return;
    }

    self.m_last_rx_heartbeat_us = esp_timer_get_time();
    self.m_link_active = true;

    if (self.m_cmd_callback) {
        self.m_cmd_callback(pkt_type, data + 2, len - 2);
    }
}

bool EspNowBridge::init(const uint8_t* central_box_mac) {
    // 1. Initialize NVS (required by Wi-Fi & Binding Storage)
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

    // 4. Resolve Peer Binding & State
    uint8_t stored_mac[6] = {0};

    if (central_box_mac) {
        // Explicit MAC passed
        save_stored_central_mac(central_box_mac);
        set_peer_mac(central_box_mac);
        m_binding_state = BINDING_STATE_LINKED;
        m_last_rx_heartbeat_us = esp_timer_get_time();
        m_link_active = true;
        ESP_LOGI(TAG, "ESP-NOW bridge explicit init [LINKED] to %02X:%02X:%02X:%02X:%02X:%02X",
                 m_peer_mac[0], m_peer_mac[1], m_peer_mac[2], m_peer_mac[3], m_peer_mac[4], m_peer_mac[5]);
    } else if (load_stored_central_mac(stored_mac)) {
        // Stored MAC loaded from NVS
        set_peer_mac(stored_mac);
        m_binding_state = BINDING_STATE_LINKED;
        m_last_rx_heartbeat_us = esp_timer_get_time();
        m_link_active = false; // Waiting for first heartbeat
        ESP_LOGI(TAG, "ESP-NOW bridge NVS init [LINKED] to Central Box %02X:%02X:%02X:%02X:%02X:%02X",
                 m_peer_mac[0], m_peer_mac[1], m_peer_mac[2], m_peer_mac[3], m_peer_mac[4], m_peer_mac[5]);
    } else {
        // No binding in NVS: Open discovery mode
        set_peer_mac(s_broadcast_mac);
        m_binding_state = BINDING_STATE_UNPAIRED;
        m_last_rx_heartbeat_us = 0;
        m_link_active = false;
        ESP_LOGW(TAG, "No Central Box MAC in NVS. Front Node entering [UNPAIRED] open pairing mode.");
    }

    return true;
}

void EspNowBridge::update() {
    uint64_t now = esp_timer_get_time();

    // Check orphan condition when linked
    if (m_binding_state == BINDING_STATE_LINKED) {
        if (m_last_rx_heartbeat_us > 0 && (now - m_last_rx_heartbeat_us) >= (ORPHAN_HEARTBEAT_TIMEOUT_SEC * 1000000ULL)) {
            m_binding_state = BINDING_STATE_ORPHAN;
            m_link_active = false;
            ESP_LOGW(TAG, "⚠️ Central Box heartbeat timeout (>%d s)! State transitioned to [ORPHAN / RE-PAIRING READY]",
                     ORPHAN_HEARTBEAT_TIMEOUT_SEC);
        }
    }
}

void EspNowBridge::reset_binding() {
    clear_stored_central_mac();
    set_peer_mac(s_broadcast_mac);
    m_binding_state = BINDING_STATE_UNPAIRED;
    m_link_active = false;
    m_last_rx_heartbeat_us = 0;
    ESP_LOGW(TAG, "Front Node NVS binding cleared: state is now [UNPAIRED]. Listening for pairing beacon...");
}

bool EspNowBridge::send_binding_ack(const uint8_t* target_mac) {
    if (!target_mac) return false;

    // Ensure peer exists in ESP-NOW table
    if (!esp_now_is_peer_exist(target_mac)) {
        esp_now_peer_info_t peer_info = {};
        memcpy(peer_info.peer_addr, target_mac, 6);
        peer_info.channel = ESPNOW_WIFI_CHANNEL;
        peer_info.ifidx = WIFI_IF_STA;
        peer_info.encrypt = false;
        esp_now_add_peer(&peer_info);
    }

    uint8_t buf[3];
    buf[0] = FRONT_NODE_PROTOCOL_VER;
    buf[1] = PKT_TYPE_BINDING_ACK;
    buf[2] = static_cast<uint8_t>(m_binding_state);

    esp_err_t res = esp_now_send(target_mac, buf, sizeof(buf));
    ESP_LOGI(TAG, "Sent BINDING_ACK to %02X:%02X:%02X:%02X:%02X:%02X (state=%d, res=%d)",
             target_mac[0], target_mac[1], target_mac[2], target_mac[3], target_mac[4], target_mac[5],
             (int)m_binding_state, res);
    return (res == ESP_OK);
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

bool EspNowBridge::send_cam_status(uint8_t brand, uint8_t state, uint8_t bat_pct, uint16_t sd_min, bool autoconn, bool fuelfilt) {
    uint8_t buf[9];
    buf[0] = FRONT_NODE_PROTOCOL_VER;
    buf[1] = PKT_TYPE_CAM_STATUS;
    buf[2] = brand;
    buf[3] = state;
    buf[4] = bat_pct;
    memcpy(&buf[5], &sd_min, sizeof(uint16_t));
    buf[7] = autoconn ? 1 : 0;
    buf[8] = fuelfilt ? 1 : 0;

    esp_err_t res = esp_now_send(m_peer_mac, buf, sizeof(buf));
    return (res == ESP_OK);
}

bool EspNowBridge::send_cam_scan_result(const uint8_t* mac, int8_t rssi, uint8_t brand, const char* name) {
    uint8_t buf[40] = {0};
    buf[0] = FRONT_NODE_PROTOCOL_VER;
    buf[1] = PKT_TYPE_CAM_SCAN_RES;
    if (mac) memcpy(&buf[2], mac, 6);
    buf[8] = static_cast<uint8_t>(rssi);
    buf[9] = brand;
    if (name) {
        strncpy(reinterpret_cast<char*>(&buf[10]), name, 29);
    }

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

FrontNodeBindingState EspNowBridge::get_binding_state() const {
    return m_binding_state;
}

bool EspNowBridge::is_linked() const {
    return (m_binding_state == BINDING_STATE_LINKED && m_link_active);
}

const uint8_t* EspNowBridge::get_peer_mac() const {
    return m_peer_mac;
}

uint32_t EspNowBridge::get_tx_success_count() const {
    return m_tx_success_count;
}

uint32_t EspNowBridge::get_tx_fail_count() const {
    return m_tx_fail_count;
}
