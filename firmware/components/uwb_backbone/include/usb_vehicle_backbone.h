#pragma once

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <functional>
#include "esp_err.h"
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"
#include "freertos/task.h"
#include "usb_backbone_types.h"

// =============================================================================
// OpenMotorBridge v10.0 - Unified 4-Wire USB 2.0 Automotive Backbone Engine
// Physical Hub Star Topology:
//   - PCBA 01 Central Box: Microchip USB2517I-JZX 7-Port High-Speed Hub (U8)
//   - PCBA 05 Front-Node:  Microchip USB2514Bi-AEZG 4-Port Hub (U2)
//   - PCBA 03 Pod 1 & 2:   TI TS5A3159DBVR SPDT USB Mux (U4) via OMM_DETECT (Pad 16)
//   - PCBA 08 Rear Radar:  ESP32-C5-WROOM-1U (U1) Native USB 2.0 (Pad 16/17)
//   - PCBA 09/10 OMM:      ESP32-C6-MINI-1U (U1) Native USB 2.0 (Pad 14/15)
// =============================================================================

typedef struct {
    int pin_usb_dm;           // Native USB D- GPIO (e.g. GPIO 19 on S31, GPIO 12 on C6, GPIO 18 on C5)
    int pin_usb_dp;           // Native USB D+ GPIO (e.g. GPIO 20 on S31, GPIO 13 on C6, GPIO 19 on C5)
    UsbHubPortId hub_port_id; // Assigned port on USB2517I-JZX / USB2514Bi
    bool high_speed_phy;      // true = 480 Mbps HS (ESP32-S31 / USB2517I), false = 12 Mbps FS
} usb_backbone_hw_config_t;

// Legacy config alias
typedef usb_backbone_hw_config_t usb_backbone_config_t;
typedef usb_backbone_hw_config_t dw3110_config_t;

class UsbVehicleBackbone {
public:
    static UsbVehicleBackbone& instance();

    /**
     * @brief Initialisiert den 4-Draht USB 2.0 Fahrzeug-Backbone für den lokalen Knoten
     */
    esp_err_t init(UsbNodeType local_node_type, const usb_backbone_hw_config_t *hw_cfg = nullptr);

    /**
     * @brief Startet den FreeRTOS Hintergrund-Task für USB CDC/HID/UAC2 & Bus-DFU Dispatching
     */
    esp_err_t start_task(UBaseType_t priority = 22, BaseType_t core_id = 0);

    // -------------------------------------------------------------------------
    // Deterministische Sende-Methoden über den 4-Draht USB-Bus (< 1 ms Latenz)
    // -------------------------------------------------------------------------
    esp_err_t send_ptt_event(UsbHandlebarButton button, UsbPttEventType evt, uint16_t duration_ms = 0, uint8_t bat_pct = 100);
    esp_err_t send_front_telemetry(const UsbFrontTelemetryPkt &telem);
    esp_err_t send_cockpit_hud_state(const UsbCockpitHudStatePkt &hud);
    esp_err_t send_cartridge_announce(uint8_t hw_class, uint16_t model_id, uint64_t uid, uint16_t vcc_mv, uint8_t status_flags = 0x07);
    esp_err_t send_cartridge_opcode(UsbNodeType target_bay, uint8_t token, UsbPodControlOpcode opcode, uint16_t pulse_ms = 0, uint8_t act_mask = 0);
    esp_err_t send_cartridge_ack(UsbNodeType target_box, uint8_t token, uint8_t opcode, uint8_t result, uint8_t act_mask, uint16_t exec_us);
    esp_err_t send_radar_targets(const UsbRadarTargetsPkt &radar);
    esp_err_t send_radar_led_cmd(uint8_t macro, uint8_t brightness, uint8_t left_bsd, uint8_t right_bsd);
    esp_err_t send_v2x_cits_event(const UsbV2xCitsEventPkt &v2x_evt);
    esp_err_t send_heartbeat(uint16_t vbus_mv = 5000, int16_t temp_c_10 = 250);
    esp_err_t send_pairing_request(uint64_t nonce, uint32_t vin_hash, uint16_t timeout_sec = 60);
    esp_err_t send_pairing_confirm(UsbNodeType target_node, uint64_t nonce, const uint8_t *session_key, uint8_t slot);
    esp_err_t send_bsd_trigger(bool left_active, uint8_t left_lvl, bool right_active, uint8_t right_lvl);
    esp_err_t send_power_cycle_cmd(UsbNodeType target_node, uint8_t sub_target = 0, uint16_t off_duration_ms = 2500);
    esp_err_t send_fw_update_push(UsbNodeType target_node, const UsbFwUpdatePushPkt &dfu_pkt);
    esp_err_t send_fw_update_done(const UsbFwUpdateDonePkt &done_pkt);
    esp_err_t send_sd_block_req(const UsbSdBlockReqPkt &req);
    esp_err_t send_sd_block_data(UsbNodeType target_node, const UsbSdBlockDataPkt &data);
    esp_err_t send_cam_trigger(const UsbCamTriggerPkt &trig);
    esp_err_t send_cam_status(const UsbCamStatusFeedPkt &status);

    /**
     * @brief Universelles Senden eines beliebigen USB-Backbone-Pakets
     */
    esp_err_t send_packet(UsbNodeType target, UsbBackbonePktType type, const void *payload, size_t len);
    esp_err_t send_generic_packet(UsbBackbonePktType type, const void *payload, size_t len, UsbNodeType target) {
        return send_packet(target, type, payload, len);
    }

    /**
     * @brief Einspeisen eines empfangenen Roh-Frames (für Loopback-Test oder USB-CDC/HID IRQ)
     */
    void inject_rx_frame(const uint8_t *data, size_t len);

    // -------------------------------------------------------------------------
    // Registrierung von Ereignis-Callbacks
    // -------------------------------------------------------------------------
    void set_ptt_callback(std::function<void(const UsbPttEventPkt&, UsbNodeType source)> cb) { m_ptt_cb = cb; }
    void set_telemetry_callback(std::function<void(const UsbFrontTelemetryPkt&)> cb) { m_telem_cb = cb; }
    void set_cockpit_hud_callback(std::function<void(const UsbCockpitHudStatePkt&)> cb) { m_hud_cb = cb; }
    void set_cartridge_announce_callback(std::function<void(const UsbPodAnnouncePkt&, UsbNodeType source)> cb) { m_cart_ann_cb = cb; }
    void set_cartridge_opcode_callback(std::function<void(const UsbPodControlPkt&, UsbNodeType source)> cb) { m_cart_op_cb = cb; }
    void set_cartridge_ack_callback(std::function<void(const UsbPodAckPkt&, UsbNodeType source)> cb) { m_cart_ack_cb = cb; }
    void set_radar_targets_callback(std::function<void(const UsbRadarTargetsPkt&)> cb) { m_radar_cb = cb; }
    void set_radar_led_callback(std::function<void(const UsbRadarLedCmdPkt&)> cb) { m_radar_led_cb = cb; }
    void set_v2x_cits_callback(std::function<void(const UsbV2xCitsEventPkt&)> cb) { m_v2x_cb = cb; }
    void set_heartbeat_callback(std::function<void(UsbNodeType node, const UsbNodeHeartbeatPkt&)> cb) { m_heartbeat_cb = cb; }
    void set_pairing_request_callback(std::function<void(const UsbPairingRequestPkt&, UsbNodeType source)> cb) { m_pair_req_cb = cb; }
    void set_pairing_confirm_callback(std::function<void(const UsbPairingConfirmPkt&, UsbNodeType source)> cb) { m_pair_cnf_cb = cb; }
    void set_fw_update_push_callback(std::function<void(const UsbFwUpdatePushPkt&, UsbNodeType source)> cb) { m_dfu_push_cb = cb; }
    void set_fw_update_done_callback(std::function<void(const UsbFwUpdateDonePkt&, UsbNodeType source)> cb) { m_dfu_done_cb = cb; }
    void set_sd_block_req_callback(std::function<void(const UsbSdBlockReqPkt&, UsbNodeType source)> cb) { m_sd_req_cb = cb; }
    void set_sd_block_data_callback(std::function<void(const UsbSdBlockDataPkt&, UsbNodeType source)> cb) { m_sd_data_cb = cb; }
    void set_cam_trigger_callback(std::function<void(const UsbCamTriggerPkt&, UsbNodeType source)> cb) { m_cam_trig_cb = cb; }
    void set_cam_status_callback(std::function<void(const UsbCamStatusFeedPkt&, UsbNodeType source)> cb) { m_cam_stat_cb = cb; }
    void set_generic_packet_callback(std::function<void(UsbBackbonePktType type, const uint8_t *payload, size_t len, UsbNodeType source)> cb) { m_generic_cb = cb; }

    // -------------------------------------------------------------------------
    // Link-Status & USB Hub Port Topologie-Verifikation
    // -------------------------------------------------------------------------
    bool is_peer_online(UsbNodeType node) const;
    uint16_t get_peer_distance_cm(UsbNodeType node) const; // Returns USB Hub Port ID or virtual cable length
    uint32_t get_peer_last_seen_ms(UsbNodeType node) const;
    UsbNodeType get_local_node_type() const { return m_local_node_type; }
    const usb_backbone_hw_config_t& get_hw_config() const { return m_hw_cfg; }

    uint32_t get_tx_count() const { return m_tx_count; }
    uint32_t get_rx_count() const { return m_rx_count; }
    uint32_t get_crc_errors() const { return m_crc_errors; }
    uint32_t get_gating_rejections() const { return m_gating_rejections; }

private:
    UsbVehicleBackbone();
    ~UsbVehicleBackbone();

    static void backbone_task_worker(void *pvParameters);
    void process_received_frame(const uint8_t *frame_data, size_t frame_len);
    void handle_incoming_dfu_push(const UsbFwUpdatePushPkt &dfu_pkt, UsbNodeType source);

    UsbNodeType m_local_node_type;
    usb_backbone_hw_config_t m_hw_cfg;
    TaskHandle_t m_task_handle;
    QueueHandle_t m_rx_queue;

    uint16_t m_seq_counter;
    uint32_t m_tx_count;
    uint32_t m_rx_count;
    uint32_t m_crc_errors;
    uint32_t m_gating_rejections;

    // Built-in Satellite OTA / Bus-DFU receiver state
    uint32_t m_dfu_expected_bytes;
    uint32_t m_dfu_written_bytes;
    bool     m_dfu_session_active;

    struct PeerState {
        bool online;
        uint32_t last_seen_ms;
        uint16_t usb_port_id;
        uint16_t vbus_mv;
    } m_peers[8]; // Indexed by UsbNodeType (1..7)

    // Callbacks
    std::function<void(const UsbPttEventPkt&, UsbNodeType source)> m_ptt_cb;
    std::function<void(const UsbFrontTelemetryPkt&)> m_telem_cb;
    std::function<void(const UsbCockpitHudStatePkt&)> m_hud_cb;
    std::function<void(const UsbPodAnnouncePkt&, UsbNodeType source)> m_cart_ann_cb;
    std::function<void(const UsbPodControlPkt&, UsbNodeType source)> m_cart_op_cb;
    std::function<void(const UsbPodAckPkt&, UsbNodeType source)> m_cart_ack_cb;
    std::function<void(const UsbRadarTargetsPkt&)> m_radar_cb;
    std::function<void(const UsbRadarLedCmdPkt&)> m_radar_led_cb;
    std::function<void(const UsbV2xCitsEventPkt&)> m_v2x_cb;
    std::function<void(UsbNodeType node, const UsbNodeHeartbeatPkt&)> m_heartbeat_cb;
    std::function<void(const UsbPairingRequestPkt&, UsbNodeType source)> m_pair_req_cb;
    std::function<void(const UsbPairingConfirmPkt&, UsbNodeType source)> m_pair_cnf_cb;
    std::function<void(const UsbFwUpdatePushPkt&, UsbNodeType source)> m_dfu_push_cb;
    std::function<void(const UsbFwUpdateDonePkt&, UsbNodeType source)> m_dfu_done_cb;
    std::function<void(const UsbSdBlockReqPkt&, UsbNodeType source)> m_sd_req_cb;
    std::function<void(const UsbSdBlockDataPkt&, UsbNodeType source)> m_sd_data_cb;
    std::function<void(const UsbCamTriggerPkt&, UsbNodeType source)> m_cam_trig_cb;
    std::function<void(const UsbCamStatusFeedPkt&, UsbNodeType source)> m_cam_stat_cb;
    std::function<void(UsbBackbonePktType type, const uint8_t *payload, size_t len, UsbNodeType source)> m_generic_cb;
};

using UwbVehicleBackbone = UsbVehicleBackbone;

