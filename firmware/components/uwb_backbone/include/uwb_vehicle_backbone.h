#pragma once

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <functional>
#include "esp_err.h"
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"
#include "freertos/task.h"
#include "uwb_backbone_types.h"
#include "dw3110_driver.h"

// =============================================================================
// OpenMotorBridge - All-UWB High-Level Vehicle Backbone Protocol Engine
// Deterministic Mesh & Star Routing with Two-Way Ranging Distance Gating
// =============================================================================

class UwbVehicleBackbone {
public:
    static UwbVehicleBackbone& instance();

    /**
     * @brief Initialisiert den UWB-Backbone für den lokalen Knoten
     */
    esp_err_t init(UwbNodeType local_node_type, const dw3110_config_t *hw_cfg = nullptr);

    /**
     * @brief Startet den FreeRTOS Hintergrund-Task für den UWB-Backbone
     */
    esp_err_t start_task(UBaseType_t priority = 22, BaseType_t core_id = 0);

    // -------------------------------------------------------------------------
    // Schnelle Sende-Methoden (< 0.4 ms Latenz)
    // -------------------------------------------------------------------------
    esp_err_t send_ptt_event(UwbHandlebarButton button, UwbPttEventType evt, uint16_t duration_ms = 0, uint8_t bat_pct = 100);
    esp_err_t send_front_telemetry(const UwbFrontTelemetryPkt &telem);
    esp_err_t send_cartridge_announce(uint8_t hw_class, uint16_t model_id, uint64_t uid, uint16_t vcc_mv);
    esp_err_t send_cartridge_opcode(UwbNodeType target_bay, uint8_t token, UwbCartridgeOpcode opcode, uint16_t pulse_ms = 0, uint8_t act_mask = 0);
    esp_err_t send_cartridge_ack(UwbNodeType target_box, uint8_t token, uint8_t opcode, uint8_t result, uint8_t act_mask, uint16_t exec_us);
    esp_err_t send_radar_targets(const UwbRadarTargetsPkt &radar);
    esp_err_t send_radar_led_cmd(uint8_t macro, uint8_t brightness, uint8_t left_bsd, uint8_t right_bsd);
    esp_err_t send_heartbeat(uint16_t vbus_mv = 5000, int16_t temp_c_10 = 250);
    esp_err_t send_pairing_request(uint64_t nonce, uint32_t vin_hash, uint16_t timeout_sec = 60);
    esp_err_t send_pairing_confirm(UwbNodeType target_node, uint64_t nonce, const uint8_t *session_key, uint8_t slot);
    esp_err_t send_bsd_trigger(bool left_active, uint8_t left_lvl, bool right_active, uint8_t right_lvl);

    /**
     * @brief Universelles Senden eines beliebigen UWB-Pakets
     */
    esp_err_t send_packet(UwbNodeType target, UwbBackbonePktType type, const void *payload, size_t len);

    // -------------------------------------------------------------------------
    // Registrierung von Ereignis-Callbacks
    // -------------------------------------------------------------------------
    void set_ptt_callback(std::function<void(const UwbPttEventPkt&, UwbNodeType source)> cb) { m_ptt_cb = cb; }
    void set_telemetry_callback(std::function<void(const UwbFrontTelemetryPkt&)> cb) { m_telem_cb = cb; }
    void set_cartridge_announce_callback(std::function<void(const UwbCartridgeAnnouncePkt&, UwbNodeType source)> cb) { m_cart_ann_cb = cb; }
    void set_cartridge_opcode_callback(std::function<void(const UwbCartridgeOpcodePkt&, UwbNodeType source)> cb) { m_cart_op_cb = cb; }
    void set_cartridge_ack_callback(std::function<void(const UwbCartridgeAckPkt&, UwbNodeType source)> cb) { m_cart_ack_cb = cb; }
    void set_radar_targets_callback(std::function<void(const UwbRadarTargetsPkt&)> cb) { m_radar_cb = cb; }
    void set_radar_led_callback(std::function<void(const UwbRadarLedCmdPkt&)> cb) { m_radar_led_cb = cb; }
    void set_heartbeat_callback(std::function<void(UwbNodeType node, const UwbNodeHeartbeatPkt&)> cb) { m_heartbeat_cb = cb; }
    void set_pairing_request_callback(std::function<void(const UwbPairingRequestPkt&, UwbNodeType source)> cb) { m_pair_req_cb = cb; }
    void set_pairing_confirm_callback(std::function<void(const UwbPairingConfirmPkt&, UwbNodeType source)> cb) { m_pair_cnf_cb = cb; }
    void set_generic_packet_callback(std::function<void(UwbBackbonePktType type, const uint8_t *payload, size_t len, UwbNodeType source)> cb) { m_generic_cb = cb; }

    // -------------------------------------------------------------------------
    // Link-Status & Two-Way Ranging Gating
    // -------------------------------------------------------------------------
    bool is_peer_online(UwbNodeType node) const;
    uint16_t get_peer_distance_cm(UwbNodeType node) const;
    uint32_t get_peer_last_seen_ms(UwbNodeType node) const;
    UwbNodeType get_local_node_type() const { return m_local_node_type; }

    uint32_t get_tx_count() const { return m_tx_count; }
    uint32_t get_rx_count() const { return m_rx_count; }
    uint32_t get_crc_errors() const { return m_crc_errors; }
    uint32_t get_gating_rejections() const { return m_gating_rejections; }

private:
    UwbVehicleBackbone();
    ~UwbVehicleBackbone();

    static void rx_dispatch_thunk(const uint8_t *data, size_t len, int8_t rssi_dbm, uint64_t rx_timestamp, void *user_ctx);
    static void tx_done_thunk(bool success, uint64_t tx_timestamp, void *user_ctx);
    static void backbone_task_worker(void *pvParameters);

    void process_received_frame(const uint8_t *frame_data, size_t frame_len, int8_t rssi_dbm, uint64_t rx_ts);
    bool check_ranging_gating(UwbNodeType source, uint16_t dist_cm);

    UwbNodeType m_local_node_type;
    dw3110_driver_t *m_driver;
    TaskHandle_t m_task_handle;
    QueueHandle_t m_rx_queue;

    uint16_t m_seq_counter;
    uint32_t m_tx_count;
    uint32_t m_rx_count;
    uint32_t m_crc_errors;
    uint32_t m_gating_rejections;

    struct PeerState {
        bool online;
        uint32_t last_seen_ms;
        uint16_t distance_cm;
        int8_t last_rssi;
    } m_peers[6]; // Indexiert nach UwbNodeType (1..5)

    // Callbacks
    std::function<void(const UwbPttEventPkt&, UwbNodeType source)> m_ptt_cb;
    std::function<void(const UwbFrontTelemetryPkt&)> m_telem_cb;
    std::function<void(const UwbCartridgeAnnouncePkt&, UwbNodeType source)> m_cart_ann_cb;
    std::function<void(const UwbCartridgeOpcodePkt&, UwbNodeType source)> m_cart_op_cb;
    std::function<void(const UwbCartridgeAckPkt&, UwbNodeType source)> m_cart_ack_cb;
    std::function<void(const UwbRadarTargetsPkt&)> m_radar_cb;
    std::function<void(const UwbRadarLedCmdPkt&)> m_radar_led_cb;
    std::function<void(UwbNodeType node, const UwbNodeHeartbeatPkt&)> m_heartbeat_cb;
    std::function<void(const UwbPairingRequestPkt&, UwbNodeType source)> m_pair_req_cb;
    std::function<void(const UwbPairingConfirmPkt&, UwbNodeType source)> m_pair_cnf_cb;
    std::function<void(UwbBackbonePktType type, const uint8_t *payload, size_t len, UwbNodeType source)> m_generic_cb;
};
