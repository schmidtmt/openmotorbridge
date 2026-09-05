#pragma once

#include <stdbool.h>
#include <stdint.h>
#include "esp_now.h"

#include "front_node_config.h"

// Callback for remote command handling from Central Box
typedef void (*FrontNodeCmdCallback)(uint8_t cmd_id, const uint8_t* payload, size_t len);

class EspNowBridge {
public:
    static EspNowBridge& instance();

    bool init(const uint8_t* central_box_mac = nullptr);
    void set_command_callback(FrontNodeCmdCallback cb);

    // Fast Transmit Methods
    bool send_ptt_event(bool pressed, uint64_t timestamp_us);
    bool send_audio_rms(uint8_t dba, uint32_t raw_rms);
    bool send_ottocast_status(uint8_t state, bool power_on, bool fault, uint32_t cafe_sec);
    bool send_cam_status(uint8_t brand, uint8_t state, uint8_t bat_pct, uint16_t sd_min, bool autoconn, bool fuelfilt);
    bool send_cam_scan_result(const uint8_t* mac, int8_t rssi, uint8_t brand, const char* name);
    bool send_heartbeat();
    bool send_binding_ack(const uint8_t* target_mac);

    // Hardware Binding & State Machine
    FrontNodeBindingState get_binding_state() const;
    void reset_binding();
    void update(); // Periodic link supervision & orphan state check

    bool is_linked() const;
    const uint8_t* get_peer_mac() const;
    uint32_t get_tx_success_count() const;
    uint32_t get_tx_fail_count() const;

private:
    EspNowBridge();

    static void on_data_sent(const uint8_t* mac_addr, esp_now_send_status_t status);
    static void on_data_recv(const esp_now_recv_info_t* recv_info, const uint8_t* data, int len);

    // NVS Persistence
    bool load_stored_central_mac(uint8_t* mac_out);
    bool save_stored_central_mac(const uint8_t* mac_in);
    void clear_stored_central_mac();

    bool set_peer_mac(const uint8_t* mac);

    uint8_t m_peer_mac[6];
    bool m_peer_registered;
    bool m_link_active;
    FrontNodeBindingState m_binding_state;
    uint64_t m_last_rx_heartbeat_us;
    uint32_t m_tx_success_count;
    uint32_t m_tx_fail_count;
    FrontNodeCmdCallback m_cmd_callback;
};

