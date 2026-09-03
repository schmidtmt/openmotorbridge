#include "esp_now_front_node_client.h"
#include "esp_now.h"
#include "esp_wifi.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "opto_pulse_sequencer.h"
#include "audio_dsp_pipeline.h"
#include <string.h>

static const char* TAG = "FRONT_NODE_CLIENT";

#define ESPNOW_WIFI_CHANNEL     1
#define FRONT_NODE_PROTOCOL_VER 0x01

// Packet Types matching front_node_config.h
enum FrontNodePacketType : uint8_t {
    PKT_TYPE_HEARTBEAT       = 0x01,
    PKT_TYPE_PTT_EVENT       = 0x02,
    PKT_TYPE_AUDIO_RMS       = 0x03,
    PKT_TYPE_OTTOCAST_STATUS = 0x04,
    PKT_TYPE_CAN_TELEMETRY   = 0x05,
    PKT_TYPE_CMD_POWER_CYCLE = 0x10,
    PKT_TYPE_CMD_CONFIG      = 0x11
};

static uint8_t s_front_node_mac[6] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF}; // Broadcast or paired
static FrontNodeStatus s_status = {
    .is_linked = false,
    .ottocast_state = 0,
    .ottocast_power_on = false,
    .ottocast_fault = false,
    .cafe_countdown_sec = 0,
    .ambient_dba = 45,
    .last_seen_us = 0
};

static void on_esp_now_recv(const esp_now_recv_info_t* recv_info, const uint8_t* data, int len) {
    if (!data || len < 2) return;

    uint8_t ver = data[0];
    uint8_t pkt_type = data[1];

    if (ver != FRONT_NODE_PROTOCOL_VER) return;

    s_status.is_linked = true;
    s_status.last_seen_us = esp_timer_get_time();

    // Auto-learn Front Node MAC address
    if (recv_info && recv_info->src_addr) {
        memcpy(s_front_node_mac, recv_info->src_addr, 6);
    }

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

        default:
            break;
    }
}

esp_err_t esp_now_front_node_init(void) {
    esp_now_register_recv_cb(on_esp_now_recv);

    // Register broadcast peer
    esp_now_peer_info_t peer = {};
    memcpy(peer.peer_addr, s_front_node_mac, 6);
    peer.channel = ESPNOW_WIFI_CHANNEL;
    peer.ifidx = WIFI_IF_STA;
    peer.encrypt = false;

    if (!esp_now_is_peer_exist(s_front_node_mac)) {
        esp_now_add_peer(&peer);
    }

    ESP_LOGI(TAG, "Central Box ESP-NOW client for Front Node initialized.");
    return ESP_OK;
}

FrontNodeStatus esp_now_front_node_get_status(void) {
    uint64_t now = esp_timer_get_time();
    if (now - s_status.last_seen_us > 3000000ULL) { // 3 seconds timeout
        s_status.is_linked = false;
    }
    return s_status;
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
