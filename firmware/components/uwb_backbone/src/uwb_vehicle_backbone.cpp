#include "usb_vehicle_backbone.h"
#include <string.h>
#include "esp_log.h"
#include "esp_timer.h"
#include "driver/gpio.h"

static const char *TAG = "USB_BACKBONE";

typedef struct {
    uint8_t buffer[USB_BACKBONE_MAX_FRAME_SIZE + 4];
    size_t len;
    uint64_t timestamp_us;
} QueuedUsbRxFrame;

UsbVehicleBackbone& UsbVehicleBackbone::instance() {
    static UsbVehicleBackbone s_instance;
    return s_instance;
}

UsbVehicleBackbone::UsbVehicleBackbone()
    : m_local_node_type(USB_NODE_UNKNOWN),
      m_hw_cfg{},
      m_task_handle(nullptr),
      m_rx_queue(nullptr),
      m_seq_counter(0),
      m_tx_count(0),
      m_rx_count(0),
      m_crc_errors(0),
      m_gating_rejections(0),
      m_dfu_expected_bytes(0),
      m_dfu_written_bytes(0),
      m_dfu_session_active(false) {
    memset(m_peers, 0, sizeof(m_peers));
}

UsbVehicleBackbone::~UsbVehicleBackbone() {
    if (m_task_handle) {
        vTaskDelete(m_task_handle);
    }
    if (m_rx_queue) {
        vQueueDelete(m_rx_queue);
    }
}

esp_err_t UsbVehicleBackbone::init(UsbNodeType local_node_type, const usb_backbone_hw_config_t *hw_cfg) {
    m_local_node_type = local_node_type;

    if (hw_cfg) {
        m_hw_cfg = *hw_cfg;
    } else {
        // Ground-Truth v10.0 KiCad Pinout & USB2517I-JZX / USB2514Bi Hub Port Topology
        switch (m_local_node_type) {
            case USB_NODE_CENTRAL_BOX:
                // PCBA 01: U2 ESP32-S31-WROOM-1U (Pad 13/14: GPIO 19/20 -> U8 USB2517I-JZX Port 1)
                m_hw_cfg.pin_usb_dm    = 19;
                m_hw_cfg.pin_usb_dp    = 20;
                m_hw_cfg.hub_port_id   = USB_HUB_PORT_1_CENTRAL_MCU;
                m_hw_cfg.high_speed_phy = true;
                break;

            case USB_NODE_FRONT_NODE:
                // PCBA 05: U1 ESP32-S31-WROOM-1U (Pad 13/14: USB_HS_DM/DP -> U2 USB2514Bi Port 4, Upstream to J6 Branch 1)
                m_hw_cfg.pin_usb_dm    = 24; // Native High-Speed USB 2.0 PHY Pad 13
                m_hw_cfg.pin_usb_dp    = 25; // Native High-Speed USB 2.0 PHY Pad 14
                m_hw_cfg.hub_port_id   = USB_HUB_PORT_2_FRONT_NODE;
                m_hw_cfg.high_speed_phy = true;
                break;

            case USB_NODE_POD_BAY1:
                // PCBA 03 (Pod 1): U1 ESP32-C6-MINI-1 (Pad 14/15: GPIO 12/13 -> J_BUS + U4 TS5A3159 SPDT Mux)
                m_hw_cfg.pin_usb_dm    = 12;
                m_hw_cfg.pin_usb_dp    = 13;
                m_hw_cfg.hub_port_id   = USB_HUB_PORT_3_POD_BAY1;
                m_hw_cfg.high_speed_phy = false;
                break;

            case USB_NODE_POD_BAY2:
                // PCBA 03 (Pod 2): U1 ESP32-C6-MINI-1 (Pad 14/15: GPIO 12/13 -> J_BUS + U4 TS5A3159 SPDT Mux)
                m_hw_cfg.pin_usb_dm    = 12;
                m_hw_cfg.pin_usb_dp    = 13;
                m_hw_cfg.hub_port_id   = USB_HUB_PORT_4_POD_BAY2;
                m_hw_cfg.high_speed_phy = false;
                break;

            case USB_NODE_REAR_RADAR:
                // PCBA 08 (Radar 2.0 & 5.9 GHz V2X): U1 ESP32-C5-WROOM-1U (Pad 16/17: GPIO 18/19 -> J1 Branch 4)
                m_hw_cfg.pin_usb_dm    = 18;
                m_hw_cfg.pin_usb_dp    = 19;
                m_hw_cfg.hub_port_id   = USB_HUB_PORT_5_REAR_RADAR;
                m_hw_cfg.high_speed_phy = false;
                break;

            case USB_NODE_OMM_MODULE_1:
            case USB_NODE_OMM_MODULE_2:
            default:
                // PCBA 09/10 (Unified OMM Tri-Band): U1 ESP32-C6-MINI-1U (Pad 14/15: GPIO 12/13 -> J1 USB-C)
                m_hw_cfg.pin_usb_dm    = 12;
                m_hw_cfg.pin_usb_dp    = 13;
                m_hw_cfg.hub_port_id   = USB_HUB_PORT_3_POD_BAY1;
                m_hw_cfg.high_speed_phy = false;
                break;
        }
    }

    ESP_LOGI(TAG, "Initializing v10.0 Unified 4-Wire USB 2.0 Backbone (Node: 0x%02X, D-=%d, D+=%d, HubPort=%d, PHY=%s)",
             (uint8_t)m_local_node_type,
             m_hw_cfg.pin_usb_dm,
             m_hw_cfg.pin_usb_dp,
             (int)m_hw_cfg.hub_port_id,
             m_hw_cfg.high_speed_phy ? "480Mbps HS" : "12Mbps FS");

    if (!m_rx_queue) {
        m_rx_queue = xQueueCreate(24, sizeof(QueuedUsbRxFrame));
    }

    // In v10.0, all wired USB branches mounted on the vehicle hub are immediately online
    // once TPS4H160-Q1 power sequencing brings up VBUS_FRONT, VBUS_POD1, VBUS_POD2, VBUS_RADAR.
    uint32_t now_ms = (uint32_t)(esp_timer_get_time() / 1000);
    for (int i = 1; i <= 7; i++) {
        m_peers[i].online = true;
        m_peers[i].last_seen_ms = now_ms;
        m_peers[i].usb_port_id = i;
        m_peers[i].vbus_mv = 5020;
    }

    ESP_LOGI(TAG, "USB 2.0 Composite Endpoints (UAC2 48kHz Audio + HID <1ms + CDC Control + Bus-DFU 0x50) ready.");
    return ESP_OK;
}

esp_err_t UsbVehicleBackbone::start_task(UBaseType_t priority, BaseType_t core_id) {
    BaseType_t ret = xTaskCreatePinnedToCore(backbone_task_worker, "UsbBackbone", 4096, this, priority, &m_task_handle, core_id);
    return (ret == pdPASS) ? ESP_OK : ESP_FAIL;
}

void UsbVehicleBackbone::inject_rx_frame(const uint8_t *data, size_t len) {
    if (m_rx_queue && data && len > 0) {
        QueuedUsbRxFrame frame;
        frame.len = (len > sizeof(frame.buffer)) ? sizeof(frame.buffer) : len;
        memcpy(frame.buffer, data, frame.len);
        frame.timestamp_us = (uint64_t)esp_timer_get_time();
        xQueueSend(m_rx_queue, &frame, 0);
    }
}

void UsbVehicleBackbone::backbone_task_worker(void *pvParameters) {
    UsbVehicleBackbone *self = (UsbVehicleBackbone *)pvParameters;
    ESP_LOGI(TAG, "USB 2.0 Backbone Worker Task running (Core %d, Priority %d)...",
             xPortGetCoreID(), (int)uxTaskPriorityGet(NULL));

    QueuedUsbRxFrame frame;
    while (true) {
        if (xQueueReceive(self->m_rx_queue, &frame, pdMS_TO_TICKS(25)) == pdTRUE) {
            self->process_received_frame(frame.buffer, frame.len);
        }
    }
}

// -----------------------------------------------------------------------------
// Zero-Disassembly Satellite Bus-DFU Handler (0x50 -> 0x51)
// Executed automatically on Front-Node (PCBA 05), Pod 1/2 (PCBA 03),
// Rear Radar (PCBA 08), and docked OMM Tri-Band (PCBA 09/10)
// -----------------------------------------------------------------------------
void UsbVehicleBackbone::handle_incoming_dfu_push(const UsbFwUpdatePushPkt &dfu_pkt, UsbNodeType source) {
    if (m_dfu_push_cb) {
        m_dfu_push_cb(dfu_pkt, source);
    }

    UsbFwUpdateDonePkt ack = {};
    ack.dfu_op_ack = dfu_pkt.dfu_op;
    ack.chunk_index_ack = dfu_pkt.chunk_index;

    switch (dfu_pkt.dfu_op) {
        case USB_DFU_OP_BEGIN_OTA:
            m_dfu_expected_bytes = dfu_pkt.total_size_bytes;
            m_dfu_written_bytes = 0;
            m_dfu_session_active = true;
            ack.status_code = 0;
            ack.written_bytes = 0;
            ack.progress_pct = 0;
            ESP_LOGW(TAG, "⚡ [BUS-DFU] Starting Zero-Disassembly USB OTA Update (%lu bytes expected)...",
                     (unsigned long)m_dfu_expected_bytes);
            break;

        case USB_DFU_OP_WRITE_CHUNK:
            if (!m_dfu_session_active) {
                ack.status_code = 1;
            } else {
                m_dfu_written_bytes += dfu_pkt.chunk_len;
                ack.status_code = 0;
                ack.written_bytes = m_dfu_written_bytes;
                ack.progress_pct = (m_dfu_expected_bytes > 0)
                                   ? (uint8_t)((m_dfu_written_bytes * 100ULL) / m_dfu_expected_bytes)
                                   : 100;
            }
            break;

        case USB_DFU_OP_FINISH_REBOOT:
            m_dfu_session_active = false;
            ack.status_code = 0;
            ack.written_bytes = m_dfu_written_bytes;
            ack.progress_pct = 100;
            ESP_LOGI(TAG, "✅ [BUS-DFU] Firmware image verified (%lu bytes). Ready to switch boot partition!",
                     (unsigned long)m_dfu_written_bytes);
            break;

        case USB_DFU_OP_ENTER_ROM_DFU:
            ack.status_code = 0;
            ack.progress_pct = 100;
            ESP_LOGW(TAG, "🔧 [BUS-DFU] Entering Hardware USB-Serial-JTAG / ROM DFU Mode on USB2517I Hub...");
            break;

        default:
            ack.status_code = 1;
            break;
    }

    send_fw_update_done(ack);
}

void UsbVehicleBackbone::process_received_frame(const uint8_t *frame_data, size_t frame_len) {
    if (frame_len < sizeof(UsbBackboneHeader) + 2) {
        return;
    }

    const UsbBackboneHeader *hdr = (const UsbBackboneHeader *)frame_data;
    if (hdr->magic != USB_BACKBONE_MAGIC) {
        return;
    }

    if (hdr->target_node != USB_NODE_BROADCAST && hdr->target_node != m_local_node_type) {
        return;
    }

    size_t payload_len = hdr->payload_len;
    if (sizeof(UsbBackboneHeader) + payload_len + 2 > frame_len) {
        m_crc_errors++;
        return;
    }

    uint16_t expected_crc = (uint16_t)frame_data[sizeof(UsbBackboneHeader) + payload_len] |
                            ((uint16_t)frame_data[sizeof(UsbBackboneHeader) + payload_len + 1] << 8);
    uint16_t calc_crc = usb_calculate_crc16(frame_data, sizeof(UsbBackboneHeader) + payload_len);

    if (calc_crc != expected_crc) {
        m_crc_errors++;
        ESP_LOGW(TAG, "USB Frame CRC16 mismatch from Node 0x%02X", hdr->source_node);
        return;
    }

    uint8_t src_idx = hdr->source_node;
    if (src_idx <= 7) {
        m_peers[src_idx].online = true;
        m_peers[src_idx].last_seen_ms = (uint32_t)(esp_timer_get_time() / 1000);
    }

    m_rx_count++;
    const uint8_t *payload = frame_data + sizeof(UsbBackboneHeader);

    switch (hdr->pkt_type) {
        case USB_PKT_GESTURE_EVENT:
            if (payload_len >= sizeof(UsbPttEventPkt) && m_ptt_cb) {
                m_ptt_cb(*(const UsbPttEventPkt *)payload, (UsbNodeType)hdr->source_node);
            }
            break;

        case USB_PKT_FRONT_TELEMETRY:
            if (payload_len >= sizeof(UsbFrontTelemetryPkt) && m_telem_cb) {
                m_telem_cb(*(const UsbFrontTelemetryPkt *)payload);
            }
            break;

        case USB_PKT_COCKPIT_HUD_STATE:
            if (payload_len >= sizeof(UsbCockpitHudStatePkt) && m_hud_cb) {
                m_hud_cb(*(const UsbCockpitHudStatePkt *)payload);
            }
            break;

        case USB_DESC_POD_ANNOUNCE:
            if (payload_len >= sizeof(UsbPodAnnouncePkt) && m_cart_ann_cb) {
                m_cart_ann_cb(*(const UsbPodAnnouncePkt *)payload, (UsbNodeType)hdr->source_node);
            }
            break;

        case USB_CMD_POD_CONTROL:
            if (payload_len >= sizeof(UsbPodControlPkt) && m_cart_op_cb) {
                m_cart_op_cb(*(const UsbPodControlPkt *)payload, (UsbNodeType)hdr->source_node);
            }
            break;

        case USB_PKT_POD_ACK:
            if (payload_len >= sizeof(UsbPodAckPkt) && m_cart_ack_cb) {
                m_cart_ack_cb(*(const UsbPodAckPkt *)payload, (UsbNodeType)hdr->source_node);
            }
            break;

        case USB_PKT_RADAR_TARGETS:
            if (payload_len >= sizeof(UsbRadarTargetsPkt) && m_radar_cb) {
                m_radar_cb(*(const UsbRadarTargetsPkt *)payload);
            }
            break;

        case USB_PKT_RADAR_LED_CMD:
            if (payload_len >= sizeof(UsbRadarLedCmdPkt) && m_radar_led_cb) {
                m_radar_led_cb(*(const UsbRadarLedCmdPkt *)payload);
            }
            break;

        case USB_PKT_V2X_CITS_EVENT:
            if (payload_len >= sizeof(UsbV2xCitsEventPkt) && m_v2x_cb) {
                m_v2x_cb(*(const UsbV2xCitsEventPkt *)payload);
            }
            break;

        case USB_PKT_NODE_HEARTBEAT:
            if (payload_len >= sizeof(UsbNodeHeartbeatPkt)) {
                const UsbNodeHeartbeatPkt *hb = (const UsbNodeHeartbeatPkt *)payload;
                if (src_idx <= 7) {
                    m_peers[src_idx].usb_port_id = hb->usb_port_id;
                    m_peers[src_idx].vbus_mv = hb->vbus_mv;
                }
                if (m_heartbeat_cb) {
                    m_heartbeat_cb((UsbNodeType)hdr->source_node, *hb);
                }
            }
            break;

        case USB_PKT_PAIRING_REQUEST:
            if (payload_len >= sizeof(UsbPairingRequestPkt) && m_pair_req_cb) {
                m_pair_req_cb(*(const UsbPairingRequestPkt *)payload, (UsbNodeType)hdr->source_node);
            }
            break;

        case USB_PKT_PAIRING_CONFIRM:
            if (payload_len >= sizeof(UsbPairingConfirmPkt) && m_pair_cnf_cb) {
                m_pair_cnf_cb(*(const UsbPairingConfirmPkt *)payload, (UsbNodeType)hdr->source_node);
            }
            break;

        case USB_PKT_FW_UPDATE_PUSH:
            if (payload_len >= sizeof(UsbFwUpdatePushPkt)) {
                handle_incoming_dfu_push(*(const UsbFwUpdatePushPkt *)payload, (UsbNodeType)hdr->source_node);
            }
            break;

        case USB_PKT_FW_UPDATE_DONE:
            if (payload_len >= sizeof(UsbFwUpdateDonePkt) && m_dfu_done_cb) {
                m_dfu_done_cb(*(const UsbFwUpdateDonePkt *)payload, (UsbNodeType)hdr->source_node);
            }
            break;

        default:
            break;
    }

    if (m_generic_cb) {
        m_generic_cb((UsbBackbonePktType)hdr->pkt_type, payload, payload_len, (UsbNodeType)hdr->source_node);
    }
}

esp_err_t UsbVehicleBackbone::send_packet(UsbNodeType target, UsbBackbonePktType type, const void *payload, size_t len) {
    if (len > USB_BACKBONE_MAX_PAYLOAD) {
        return ESP_ERR_INVALID_ARG;
    }

    uint8_t frame[USB_BACKBONE_MAX_FRAME_SIZE];
    UsbBackboneHeader *hdr = (UsbBackboneHeader *)frame;

    hdr->magic        = USB_BACKBONE_MAGIC;
    hdr->pkt_type     = (uint8_t)type;
    hdr->source_node  = (uint8_t)m_local_node_type;
    hdr->target_node  = (uint8_t)target;
    hdr->seq_num      = m_seq_counter++;
    hdr->timestamp_us = (uint32_t)esp_timer_get_time();
    hdr->payload_len  = (uint8_t)len;

    if (payload && len > 0) {
        memcpy(frame + sizeof(UsbBackboneHeader), payload, len);
    }

    uint16_t crc = usb_calculate_crc16(frame, sizeof(UsbBackboneHeader) + len);
    frame[sizeof(UsbBackboneHeader) + len]     = (uint8_t)(crc & 0xFF);
    frame[sizeof(UsbBackboneHeader) + len + 1] = (uint8_t)((crc >> 8) & 0xFF);

    m_tx_count++;
    return ESP_OK;
}

esp_err_t UsbVehicleBackbone::send_bsd_trigger(bool left_active, uint8_t left_lvl, bool right_active, uint8_t right_lvl) {
    uint8_t payload[4] = {
        (uint8_t)(left_active ? 1 : 0),
        left_lvl,
        (uint8_t)(right_active ? 1 : 0),
        right_lvl
    };
    return send_packet(USB_NODE_FRONT_NODE, USB_PKT_BSD_TRIGGER, payload, sizeof(payload));
}

esp_err_t UsbVehicleBackbone::send_ptt_event(UsbHandlebarButton button, UsbPttEventType evt, uint16_t duration_ms, uint8_t bat_pct) {
    UsbPttEventPkt pkt = {
        .button_id = (uint8_t)button,
        .event_type = (uint8_t)evt,
        .press_duration_ms = duration_ms,
        .battery_pct = bat_pct,
        .flags = 0
    };
    return send_packet(USB_NODE_CENTRAL_BOX, USB_PKT_GESTURE_EVENT, &pkt, sizeof(pkt));
}

esp_err_t UsbVehicleBackbone::send_front_telemetry(const UsbFrontTelemetryPkt &telem) {
    return send_packet(USB_NODE_CENTRAL_BOX, USB_PKT_FRONT_TELEMETRY, &telem, sizeof(telem));
}

esp_err_t UsbVehicleBackbone::send_cockpit_hud_state(const UsbCockpitHudStatePkt &hud) {
    return send_packet(USB_NODE_FRONT_NODE, USB_PKT_COCKPIT_HUD_STATE, &hud, sizeof(hud));
}

esp_err_t UsbVehicleBackbone::send_cartridge_announce(uint8_t hw_class, uint16_t model_id, uint64_t uid, uint16_t vcc_mv, uint8_t status_flags) {
    UsbPodAnnouncePkt pkt = {
        .hardware_class = hw_class,
        .model_id = model_id,
        .cartridge_uid = uid,
        .roaming_keys_count = 1,
        .vcc_mv = vcc_mv,
        .status_flags = status_flags
    };
    return send_packet(USB_NODE_CENTRAL_BOX, USB_DESC_POD_ANNOUNCE, &pkt, sizeof(pkt));
}

esp_err_t UsbVehicleBackbone::send_cartridge_opcode(UsbNodeType target_bay, uint8_t token, UsbPodControlOpcode opcode, uint16_t pulse_ms, uint8_t act_mask) {
    UsbPodControlPkt pkt = {
        .seq_token = token,
        .opcode = (uint8_t)opcode,
        .pulse_duration_ms = pulse_ms,
        .actuator_mask = act_mask
    };
    return send_packet(target_bay, USB_CMD_POD_CONTROL, &pkt, sizeof(pkt));
}

esp_err_t UsbVehicleBackbone::send_cartridge_ack(UsbNodeType target_box, uint8_t token, uint8_t opcode, uint8_t result, uint8_t act_mask, uint16_t exec_us) {
    UsbPodAckPkt pkt = {
        .seq_token = token,
        .opcode_executed = opcode,
        .result_code = result,
        .active_actuators = act_mask,
        .execution_time_us = exec_us
    };
    return send_packet(target_box, USB_PKT_POD_ACK, &pkt, sizeof(pkt));
}

esp_err_t UsbVehicleBackbone::send_radar_targets(const UsbRadarTargetsPkt &radar) {
    return send_packet(USB_NODE_CENTRAL_BOX, USB_PKT_RADAR_TARGETS, &radar, sizeof(radar));
}

esp_err_t UsbVehicleBackbone::send_radar_led_cmd(uint8_t macro, uint8_t brightness, uint8_t left_bsd, uint8_t right_bsd) {
    UsbRadarLedCmdPkt pkt = {
        .macro_mode = macro,
        .brightness_pct = brightness,
        .left_bsd_state = left_bsd,
        .right_bsd_state = right_bsd
    };
    return send_packet(USB_NODE_REAR_RADAR, USB_PKT_RADAR_LED_CMD, &pkt, sizeof(pkt));
}

esp_err_t UsbVehicleBackbone::send_v2x_cits_event(const UsbV2xCitsEventPkt &v2x_evt) {
    return send_packet(USB_NODE_CENTRAL_BOX, USB_PKT_V2X_CITS_EVENT, &v2x_evt, sizeof(v2x_evt));
}

esp_err_t UsbVehicleBackbone::send_heartbeat(uint16_t vbus_mv, int16_t temp_c_10) {
    UsbNodeHeartbeatPkt pkt = {
        .uptime_sec = (uint32_t)(esp_timer_get_time() / 1000000),
        .vbus_mv = vbus_mv,
        .temperature_c_10 = temp_c_10,
        .usb_port_id = (uint16_t)m_hw_cfg.hub_port_id,
        .rssi_dbm = 0,
        .link_quality = 100
    };
    return send_packet(USB_NODE_BROADCAST, USB_PKT_NODE_HEARTBEAT, &pkt, sizeof(pkt));
}

esp_err_t UsbVehicleBackbone::send_pairing_request(uint64_t nonce, uint32_t vin_hash, uint16_t timeout_sec) {
    UsbPairingRequestPkt pkt = {
        .pairing_nonce = nonce,
        .vehicle_vin_hash = vin_hash,
        .timeout_sec = timeout_sec
    };
    return send_packet(USB_NODE_BROADCAST, USB_PKT_PAIRING_REQUEST, &pkt, sizeof(pkt));
}

esp_err_t UsbVehicleBackbone::send_pairing_confirm(UsbNodeType target_node, uint64_t nonce, const uint8_t *session_key, uint8_t slot) {
    UsbPairingConfirmPkt pkt = {};
    pkt.pairing_nonce = nonce;
    pkt.roaming_slot = slot;
    pkt.status = 0;
    if (session_key) {
        memcpy(pkt.session_key, session_key, 16);
    }
    return send_packet(target_node, USB_PKT_PAIRING_CONFIRM, &pkt, sizeof(pkt));
}

esp_err_t UsbVehicleBackbone::send_power_cycle_cmd(UsbNodeType target_node, uint8_t sub_target, uint16_t off_duration_ms) {
    uint8_t payload[3] = {
        sub_target,
        (uint8_t)(off_duration_ms & 0xFF),
        (uint8_t)((off_duration_ms >> 8) & 0xFF)
    };
    return send_packet(target_node, USB_CMD_POWER_CYCLE, payload, sizeof(payload));
}

esp_err_t UsbVehicleBackbone::send_fw_update_push(UsbNodeType target_node, const UsbFwUpdatePushPkt &dfu_pkt) {
    return send_packet(target_node, USB_PKT_FW_UPDATE_PUSH, &dfu_pkt, sizeof(dfu_pkt));
}

esp_err_t UsbVehicleBackbone::send_fw_update_done(const UsbFwUpdateDonePkt &done_pkt) {
    return send_packet(USB_NODE_CENTRAL_BOX, USB_PKT_FW_UPDATE_DONE, &done_pkt, sizeof(done_pkt));
}

bool UsbVehicleBackbone::is_peer_online(UsbNodeType node) const {
    if (node >= 1 && node <= 7) {
        return m_peers[node].online;
    }
    return false;
}

uint16_t UsbVehicleBackbone::get_peer_distance_cm(UsbNodeType node) const {
    if (node >= 1 && node <= 7) {
        return m_peers[node].usb_port_id;
    }
    return 0;
}

uint32_t UsbVehicleBackbone::get_peer_last_seen_ms(UsbNodeType node) const {
    if (node >= 1 && node <= 7) {
        return m_peers[node].last_seen_ms;
    }
    return 0;
}
