#include "esp_now_front_node_client.h"
#include "esp_now.h"
#include "esp_wifi.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "nvs_flash.h"
#include "nvs.h"
#include "opto_pulse_sequencer.h"
#include "audio_dsp_pipeline.h"
#include <string.h>

static const char* TAG = "FRONT_NODE_CLIENT";

#define ESPNOW_WIFI_CHANNEL     1
#define FRONT_NODE_PROTOCOL_VER 0x01

#define NVS_NAMESPACE_FN        "fn_client"
#define NVS_KEY_FN_MAC          "fn_mac"

// Packet Types matching front_node_config.h
enum FrontNodePacketType : uint8_t {
    PKT_TYPE_HEARTBEAT       = 0x01,
    PKT_TYPE_PTT_EVENT       = 0x02,
    PKT_TYPE_AUDIO_RMS       = 0x03,
    PKT_TYPE_OTTOCAST_STATUS = 0x04,
    PKT_TYPE_CAN_TELEMETRY   = 0x05,
    PKT_TYPE_CAM_STATUS      = 0x06,
    PKT_TYPE_CAM_SCAN_RES    = 0x07,
    PKT_TYPE_BINDING_BEACON  = 0x08,
    PKT_TYPE_BINDING_ACK     = 0x09,
    PKT_TYPE_CMD_POWER_CYCLE = 0x10,
    PKT_TYPE_CMD_CONFIG      = 0x11,
    PKT_TYPE_CAM_CMD         = 0x12,
    PKT_TYPE_CMD_UNBIND      = 0x13
};

static const uint8_t s_broadcast_mac[6] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
static uint8_t s_front_node_mac[6] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
static bool s_is_paired = false;

static FrontNodeStatus s_status = {
    .is_linked = false,
    .binding_state = 0, // 0 = Unpaired
    .ottocast_state = 0,
    .ottocast_power_on = false,
    .ottocast_fault = false,
    .cafe_countdown_sec = 0,
    .ambient_dba = 45,
    .last_seen_us = 0,
    .cam_profile = 0,
    .cam_state = 0,
    .cam_battery_pct = 0,
    .cam_sd_min_rem = 0,
    .cam_autoconnect_en = true,
    .cam_fuel_filter_en = true
};

static bool load_stored_front_node_mac(uint8_t* mac_out) {
    if (!mac_out) return false;
    nvs_handle_t handle;
    esp_err_t err = nvs_open(NVS_NAMESPACE_FN, NVS_READONLY, &handle);
    if (err != ESP_OK) return false;

    size_t size = 6;
    err = nvs_get_blob(handle, NVS_KEY_FN_MAC, mac_out, &size);
    nvs_close(handle);

    if (err != ESP_OK || size != 6) return false;

    bool all_zero = true, all_ff = true;
    for (int i = 0; i < 6; i++) {
        if (mac_out[i] != 0x00) all_zero = false;
        if (mac_out[i] != 0xFF) all_ff = false;
    }
    return (!all_zero && !all_ff);
}

static bool save_stored_front_node_mac(const uint8_t* mac_in) {
    if (!mac_in) return false;
    nvs_handle_t handle;
    esp_err_t err = nvs_open(NVS_NAMESPACE_FN, NVS_READWRITE, &handle);
    if (err != ESP_OK) return false;

    err = nvs_set_blob(handle, NVS_KEY_FN_MAC, mac_in, 6);
    if (err == ESP_OK) {
        err = nvs_commit(handle);
    }
    nvs_close(handle);
    return (err == ESP_OK);
}

static void clear_stored_front_node_mac(void) {
    nvs_handle_t handle;
    if (nvs_open(NVS_NAMESPACE_FN, NVS_READWRITE, &handle) == ESP_OK) {
        nvs_erase_key(handle, NVS_KEY_FN_MAC);
        nvs_commit(handle);
        nvs_close(handle);
        ESP_LOGI(TAG, "Front Node MAC cleared from Central Box NVS.");
    }
}

static void add_or_update_peer(const uint8_t* mac) {
    if (!mac) return;
    if (esp_now_is_peer_exist(mac)) {
        return;
    }
    esp_now_peer_info_t peer = {};
    memcpy(peer.peer_addr, mac, 6);
    peer.channel = ESPNOW_WIFI_CHANNEL;
    peer.ifidx = WIFI_IF_STA;
    peer.encrypt = false;
    esp_now_add_peer(&peer);
}

static void on_esp_now_recv(const esp_now_recv_info_t* recv_info, const uint8_t* data, int len) {
    if (!data || len < 2 || !recv_info) return;

    uint8_t ver = data[0];
    uint8_t pkt_type = data[1];

    if (ver != FRONT_NODE_PROTOCOL_VER) return;

    const uint8_t* src_mac = recv_info->src_addr;

    // Handle BINDING_ACK
    if (pkt_type == PKT_TYPE_BINDING_ACK) {
        ESP_LOGI(TAG, "✨ Received BINDING_ACK from Front Node %02X:%02X:%02X:%02X:%02X:%02X",
                 src_mac[0], src_mac[1], src_mac[2], src_mac[3], src_mac[4], src_mac[5]);

        save_stored_front_node_mac(src_mac);
        memcpy(s_front_node_mac, src_mac, 6);
        add_or_update_peer(s_front_node_mac);

        s_is_paired = true;
        s_status.is_linked = true;
        s_status.binding_state = (len >= 3) ? data[2] : 1;
        s_status.last_seen_us = esp_timer_get_time();
        return;
    }

    // Drop non-matching packets if strictly paired
    if (s_is_paired && memcmp(src_mac, s_front_node_mac, 6) != 0) {
        return;
    }

    s_status.is_linked = true;
    s_status.binding_state = 1; // Linked
    s_status.last_seen_us = esp_timer_get_time();

    switch (pkt_type) {
        case PKT_TYPE_PTT_EVENT:
            if (len >= 3) {
                bool pressed = (data[2] != 0);
                ESP_LOGI(TAG, "⚡ Zero-Latency PTT from Front Node: %s", pressed ? "DOWN" : "UP");
                // Trigger intercom optocoupler keying on Port 1 or Port 2
                opto_trigger_port_ptt(1, pressed);
            }
            break;

        case PKT_TYPE_AUDIO_RMS:
            if (len >= 3) {
                s_status.ambient_dba = data[2];
                // Feed real-time dBA level to DSP AGC limiter
                float dba_gain = (s_status.ambient_dba > 70) ? (s_status.ambient_dba - 70) * 0.3f : 0.0f;
                audio_set_port_gains(dba_gain, dba_gain);
            }
            break;

        case PKT_TYPE_OTTOCAST_STATUS:
            if (len >= 5) {
                s_status.ottocast_state = data[2];
                s_status.ottocast_power_on = (data[3] != 0);
                s_status.ottocast_fault = (data[4] != 0);
                if (len >= 9) {
                    memcpy(&s_status.cafe_countdown_sec, &data[5], sizeof(uint32_t));
                }
            }
            break;

        case PKT_TYPE_CAM_STATUS:
            if (len >= 9) {
                s_status.cam_profile = data[2];
                s_status.cam_state = data[3];
                s_status.cam_battery_pct = data[4];
                memcpy(&s_status.cam_sd_min_rem, &data[5], sizeof(uint16_t));
                s_status.cam_autoconnect_en = (data[7] != 0);
                s_status.cam_fuel_filter_en = (data[8] != 0);
            }
            break;

        case PKT_TYPE_CAM_SCAN_RES:
            if (len >= 10) {
                ESP_LOGI(TAG, "Action-Cam BLE Scan Item: MAC=%02X:%02X:%02X:%02X:%02X:%02X RSSI=%d Profile=%d Name='%s'",
                         data[2], data[3], data[4], data[5], data[6], data[7],
                         (int8_t)data[8], data[9], (len > 10) ? reinterpret_cast<const char*>(&data[10]) : "");
            }
            break;

        default:
            break;
    }
}

esp_err_t esp_now_front_node_init(void) {
    esp_now_register_recv_cb(on_esp_now_recv);

    // Ensure broadcast peer is always available for pairing beacons
    add_or_update_peer(s_broadcast_mac);

    // Load paired MAC from NVS if available
    uint8_t stored_mac[6] = {0};
    if (load_stored_front_node_mac(stored_mac)) {
        memcpy(s_front_node_mac, stored_mac, 6);
        add_or_update_peer(s_front_node_mac);
        s_is_paired = true;
        s_status.binding_state = 1;
        ESP_LOGI(TAG, "Central Box restored Front Node binding from NVS: %02X:%02X:%02X:%02X:%02X:%02X",
                 s_front_node_mac[0], s_front_node_mac[1], s_front_node_mac[2],
                 s_front_node_mac[3], s_front_node_mac[4], s_front_node_mac[5]);
    } else {
        memcpy(s_front_node_mac, s_broadcast_mac, 6);
        s_is_paired = false;
        s_status.binding_state = 0;
        ESP_LOGW(TAG, "Central Box has no Front Node paired in NVS. Ready for pairing discovery.");
    }

    return ESP_OK;
}

FrontNodeStatus esp_now_front_node_get_status(void) {
    uint64_t now = esp_timer_get_time();
    if (now - s_status.last_seen_us > 3000000ULL) { // 3 seconds timeout
        s_status.is_linked = false;
    }
    return s_status;
}

esp_err_t esp_now_front_node_start_pairing(void) {
    uint8_t buf[8] = {0};
    buf[0] = FRONT_NODE_PROTOCOL_VER;
    buf[1] = PKT_TYPE_BINDING_BEACON;

    // Embed Central Box Wi-Fi Station MAC
    esp_wifi_get_mac(WIFI_IF_STA, &buf[2]);

    ESP_LOGI(TAG, "Broadcasting Front Node Pairing / Rescue Beacon on Channel 1 (Central Box STA: %02X:%02X:%02X:%02X:%02X:%02X)",
             buf[2], buf[3], buf[4], buf[5], buf[6], buf[7]);

    // Broadcast to open listening nodes
    esp_err_t err = esp_now_send(s_broadcast_mac, buf, sizeof(buf));

    // Also send unicast if previously paired
    if (s_is_paired && memcmp(s_front_node_mac, s_broadcast_mac, 6) != 0) {
        esp_now_send(s_front_node_mac, buf, sizeof(buf));
    }

    return err;
}

esp_err_t esp_now_front_node_unbind(void) {
    uint8_t buf[2] = {FRONT_NODE_PROTOCOL_VER, PKT_TYPE_CMD_UNBIND};
    ESP_LOGW(TAG, "Sending Unbind Command to Front Node and clearing Central Box NVS...");

    if (s_is_paired && memcmp(s_front_node_mac, s_broadcast_mac, 6) != 0) {
        esp_now_send(s_front_node_mac, buf, sizeof(buf));
    }

    clear_stored_front_node_mac();
    memcpy(s_front_node_mac, s_broadcast_mac, 6);
    s_is_paired = false;
    s_status.is_linked = false;
    s_status.binding_state = 0;

    return ESP_OK;
}

esp_err_t esp_now_front_node_send_heartbeat(void) {
    uint8_t buf[2] = {FRONT_NODE_PROTOCOL_VER, PKT_TYPE_HEARTBEAT};
    return esp_now_send(s_front_node_mac, buf, sizeof(buf));
}

bool esp_now_front_node_is_paired(void) {
    return s_is_paired;
}

esp_err_t esp_now_front_node_reboot_ottocast(void) {
    uint8_t buf[2] = {FRONT_NODE_PROTOCOL_VER, PKT_TYPE_CMD_POWER_CYCLE};
    ESP_LOGI(TAG, "Sending 1-Click Ottocast Reboot command to Front Node via ESP-NOW");
    return esp_now_send(s_front_node_mac, buf, sizeof(buf));
}

esp_err_t esp_now_front_node_set_ignition(bool ignition_on) {
    uint8_t buf[3] = {FRONT_NODE_PROTOCOL_VER, PKT_TYPE_CMD_CONFIG, static_cast<uint8_t>(ignition_on ? 1 : 0)};
    return esp_now_send(s_front_node_mac, buf, sizeof(buf));
}

esp_err_t esp_now_front_node_cam_toggle_rec(void) {
    uint8_t buf[3] = {FRONT_NODE_PROTOCOL_VER, PKT_TYPE_CAM_CMD, 0x01}; // 0x01 = CAM_CMD_TOGGLE_REC
    ESP_LOGI(TAG, "Relaying Action-Cam REC Toggle to Front Node");
    return esp_now_send(s_front_node_mac, buf, sizeof(buf));
}

esp_err_t esp_now_front_node_cam_hilight_tag(void) {
    uint8_t buf[3] = {FRONT_NODE_PROTOCOL_VER, PKT_TYPE_CAM_CMD, 0x02}; // 0x02 = CAM_CMD_HILIGHT_TAG
    ESP_LOGI(TAG, "Relaying Action-Cam HiLight Tag to Front Node");
    return esp_now_send(s_front_node_mac, buf, sizeof(buf));
}

esp_err_t esp_now_front_node_cam_start_scan(void) {
    uint8_t buf[3] = {FRONT_NODE_PROTOCOL_VER, PKT_TYPE_CAM_CMD, 0x03}; // 0x03 = CAM_CMD_START_SCAN
    ESP_LOGI(TAG, "Triggering Action-Cam BLE Inquiry Scan on Front Node");
    return esp_now_send(s_front_node_mac, buf, sizeof(buf));
}

esp_err_t esp_now_front_node_cam_pair(const uint8_t* mac, uint8_t profile, const char* name) {
    uint8_t buf[40] = {0};
    buf[0] = FRONT_NODE_PROTOCOL_VER;
    buf[1] = PKT_TYPE_CAM_CMD;
    buf[2] = 0x04; // CAM_CMD_PAIR
    if (mac) memcpy(&buf[3], mac, 6);
    buf[9] = profile;
    if (name) strncpy(reinterpret_cast<char*>(&buf[10]), name, 28);

    ESP_LOGI(TAG, "Sending Action-Cam Pair command to Front Node (Profile=%d)", profile);
    return esp_now_send(s_front_node_mac, buf, sizeof(buf));
}

esp_err_t esp_now_front_node_cam_unpair(void) {
    uint8_t buf[3] = {FRONT_NODE_PROTOCOL_VER, PKT_TYPE_CAM_CMD, 0x05}; // 0x05 = CAM_CMD_UNPAIR
    ESP_LOGI(TAG, "Sending Action-Cam Unpair command to Front Node");
    return esp_now_send(s_front_node_mac, buf, sizeof(buf));
}

esp_err_t esp_now_front_node_cam_set_autoconnect(bool enable) {
    uint8_t buf[4] = {FRONT_NODE_PROTOCOL_VER, PKT_TYPE_CAM_CMD, 0x06, static_cast<uint8_t>(enable ? 1 : 0)};
    return esp_now_send(s_front_node_mac, buf, sizeof(buf));
}

esp_err_t esp_now_front_node_cam_set_fuel_filter(bool enable) {
    uint8_t buf[4] = {FRONT_NODE_PROTOCOL_VER, PKT_TYPE_CAM_CMD, 0x07, static_cast<uint8_t>(enable ? 1 : 0)};
    return esp_now_send(s_front_node_mac, buf, sizeof(buf));
}
