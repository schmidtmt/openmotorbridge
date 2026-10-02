#include "uwb_vehicle_backbone.h"
#include <string.h>
#include "esp_log.h"
#include "esp_timer.h"

static const char *TAG = "UWB_BACKBONE";

typedef struct {
    uint8_t buffer[UWB_BACKBONE_MAX_FRAME_SIZE + 4];
    size_t len;
    int8_t rssi;
    uint64_t timestamp_us;
} QueuedRxFrame;

UwbVehicleBackbone& UwbVehicleBackbone::instance() {
    static UwbVehicleBackbone s_instance;
    return s_instance;
}

UwbVehicleBackbone::UwbVehicleBackbone()
    : m_local_node_type(UWB_NODE_UNKNOWN),
      m_driver(nullptr),
      m_task_handle(nullptr),
      m_rx_queue(nullptr),
      m_seq_counter(0),
      m_tx_count(0),
      m_rx_count(0),
      m_crc_errors(0),
      m_gating_rejections(0) {
    memset(m_peers, 0, sizeof(m_peers));
}

UwbVehicleBackbone::~UwbVehicleBackbone() {
    if (m_task_handle) {
        vTaskDelete(m_task_handle);
    }
    if (m_rx_queue) {
        vQueueDelete(m_rx_queue);
    }
    if (m_driver) {
        dw3110_deinit(m_driver);
    }
}

esp_err_t UwbVehicleBackbone::init(UwbNodeType local_node_type, const dw3110_config_t *hw_cfg) {
    m_local_node_type = local_node_type;
    ESP_LOGI(TAG, "Initializing All-UWB Backbone for Node Type: 0x%02X...", (uint8_t)m_local_node_type);

    dw3110_config_t default_cfg = {};
    if (hw_cfg) {
        default_cfg = *hw_cfg;
    } else {
        // Standard-Pinout je nach Knotentyp laden
        default_cfg.spi_host = SPI2_HOST;
        default_cfg.pan_id = UWB_BACKBONE_PAN_ID;
        default_cfg.short_addr = (uint16_t)m_local_node_type;

        if (m_local_node_type == UWB_NODE_CENTRAL_BOX) {
            // PCBA 01 (Zentralbox)
            default_cfg.pin_sck  = GPIO_NUM_36;
            default_cfg.pin_mosi = GPIO_NUM_35;
            default_cfg.pin_miso = GPIO_NUM_37;
            default_cfg.pin_cs   = GPIO_NUM_45;
            default_cfg.pin_irq  = GPIO_NUM_2;
            default_cfg.pin_rst  = GPIO_NUM_41;
        } else if (m_local_node_type == UWB_NODE_FRONT_NODE) {
            // PCBA 05 (Front-Knoten)
            default_cfg.pin_sck  = GPIO_NUM_36;
            default_cfg.pin_mosi = GPIO_NUM_35;
            default_cfg.pin_miso = GPIO_NUM_37;
            default_cfg.pin_cs   = GPIO_NUM_38;
            default_cfg.pin_irq  = GPIO_NUM_39;
            default_cfg.pin_rst  = GPIO_NUM_40;
        } else {
            // Smart Cartridge (PCBA 03) oder Radar (PCBA 08)
            default_cfg.pin_sck  = GPIO_NUM_4;
            default_cfg.pin_mosi = GPIO_NUM_5;
            default_cfg.pin_miso = GPIO_NUM_6;
            default_cfg.pin_cs   = GPIO_NUM_7;
            default_cfg.pin_irq  = GPIO_NUM_8;
            default_cfg.pin_rst  = GPIO_NUM_9;
        }
    }

    // Low-Level DW3110 Driver starten
    esp_err_t err = dw3110_init(&default_cfg, &m_driver);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to initialize DW3110 Driver: %s", esp_err_to_name(err));
        return err;
    }

    // Callbacks für RX und TX registrieren
    dw3110_set_callbacks(m_driver, rx_dispatch_thunk, tx_done_thunk, this);

    // RX-Queue anlegen (16 Frames Puffer à max ~150 Bytes)
    m_rx_queue = xQueueCreate(16, sizeof(QueuedRxFrame));

    // Receiver aktivieren
    dw3110_start_rx(m_driver);

    ESP_LOGI(TAG, "All-UWB Vehicle Backbone engine initialized successfully.");
    return ESP_OK;
}

esp_err_t UwbVehicleBackbone::start_task(UBaseType_t priority, BaseType_t core_id) {
    BaseType_t ret = xTaskCreatePinnedToCore(backbone_task_worker, "UwbBackbone", 4096, this, priority, &m_task_handle, core_id);
    return (ret == pdPASS) ? ESP_OK : ESP_FAIL;
}

void UwbVehicleBackbone::rx_dispatch_thunk(const uint8_t *data, size_t len, int8_t rssi_dbm, uint64_t rx_timestamp, void *user_ctx) {
    UwbVehicleBackbone *self = (UwbVehicleBackbone *)user_ctx;
    if (self && self->m_rx_queue && data && len > 0) {
        QueuedRxFrame frame;
        frame.len = (len > sizeof(frame.buffer)) ? sizeof(frame.buffer) : len;
        memcpy(frame.buffer, data, frame.len);
        frame.rssi = rssi_dbm;
        frame.timestamp_us = rx_timestamp;

        // Non-blocking in die Queue einreihen
        xQueueSend(self->m_rx_queue, &frame, 0);
    }
}

void UwbVehicleBackbone::tx_done_thunk(bool success, uint64_t tx_timestamp, void *user_ctx) {
    UwbVehicleBackbone *self = (UwbVehicleBackbone *)user_ctx;
    if (self && success) {
        self->m_tx_count++;
    }
}

void UwbVehicleBackbone::backbone_task_worker(void *pvParameters) {
    UwbVehicleBackbone *self = (UwbVehicleBackbone *)pvParameters;
    ESP_LOGI(TAG, "UWB Backbone Task running (Core %d, Priority %d)...",
             xPortGetCoreID(), (int)uxTaskPriorityGet(NULL));

    QueuedRxFrame frame;
    uint32_t last_heartbeat_check_ms = (uint32_t)(esp_timer_get_time() / 1000);

    while (true) {
        // Anstehende SPI-Events des DW3110 abfragen
        if (self->m_driver) {
            dw3110_process_events(self->m_driver);
        }

        // Empfangene Frames aus der Queue verarbeiten
        if (xQueueReceive(self->m_rx_queue, &frame, pdMS_TO_TICKS(10)) == pdTRUE) {
            self->process_received_frame(frame.buffer, frame.len, frame.rssi, frame.timestamp_us);
        }

        // Periodische Überwachung der Peer-Knoten (Heartbeat Timeout: 2.5 Sekunden)
        uint32_t now_ms = (uint32_t)(esp_timer_get_time() / 1000);
        if (now_ms - last_heartbeat_check_ms >= 500) {
            last_heartbeat_check_ms = now_ms;
            for (int i = 1; i <= 5; i++) {
                if (self->m_peers[i].online && (now_ms - self->m_peers[i].last_seen_ms > 2500)) {
                    self->m_peers[i].online = false;
                    ESP_LOGW(TAG, "UWB Peer 0x%02X connection TIMEOUT (Offline).", i);
                }
            }
        }
    }
}

// -----------------------------------------------------------------------------
// Two-Way Ranging Gating (docs/de/09_firmware_architecture.md Abs. 2.2)
// -----------------------------------------------------------------------------
bool UwbVehicleBackbone::check_ranging_gating(UwbNodeType source, uint16_t dist_cm) {
    if (dist_cm == 0) {
        return true; // Ranging nicht verfügbar / Initial-Paket
    }

    switch (source) {
        case UWB_NODE_FRONT_NODE:
            // Physisches Distanzfenster Front Node: 0.5m bis 2.5m
            return (dist_cm >= 50 && dist_cm <= 250);

        case UWB_NODE_CARTRIDGE_BAY1:
        case UWB_NODE_CARTRIDGE_BAY2:
            // Physisches Distanzfenster Kassetten: 0.2m bis 1.8m
            return (dist_cm >= 20 && dist_cm <= 180);

        case UWB_NODE_REAR_RADAR:
            // Physisches Distanzfenster Heckradar: 0.3m bis 2.0m
            return (dist_cm >= 30 && dist_cm <= 200);

        default:
            return true;
    }
}

void UwbVehicleBackbone::process_received_frame(const uint8_t *frame_data, size_t frame_len, int8_t rssi_dbm, uint64_t rx_ts) {
    if (frame_len < sizeof(UwbBackboneHeader) + 2) {
        return; // Zu kurz für Header + CRC
    }

    // 1. Framing Magic prüfen
    const UwbBackboneHeader *hdr = (const UwbBackboneHeader *)frame_data;
    if (hdr->magic != UWB_BACKBONE_MAGIC) {
        return;
    }

    // 2. Adressierung prüfen (Broadcast oder direkt an uns)
    if (hdr->target_node != UWB_NODE_BROADCAST && hdr->target_node != m_local_node_type) {
        return; // Für einen anderen Knoten bestimmt
    }

    // 3. CRC16-CCITT Integritätsprüfung
    size_t payload_len = hdr->payload_len;
    if (sizeof(UwbBackboneHeader) + payload_len + 2 > frame_len) {
        m_crc_errors++;
        return;
    }

    uint16_t expected_crc = (uint16_t)frame_data[sizeof(UwbBackboneHeader) + payload_len] |
                            ((uint16_t)frame_data[sizeof(UwbBackboneHeader) + payload_len + 1] << 8);
    uint16_t calc_crc = uwb_calculate_crc16(frame_data, sizeof(UwbBackboneHeader) + payload_len);

    if (calc_crc != expected_crc) {
        m_crc_errors++;
        ESP_LOGW(TAG, "UWB CRC16 mismatch from 0x%02X (Calc: 0x%04X, Expected: 0x%04X)",
                 hdr->source_node, calc_crc, expected_crc);
        return;
    }

    // 4. Two-Way Ranging Gating
    uint8_t src_idx = hdr->source_node;
    if (src_idx <= 5) {
        uint16_t dist = m_peers[src_idx].distance_cm;
        if (!check_ranging_gating((UwbNodeType)src_idx, dist)) {
            m_gating_rejections++;
            ESP_LOGW(TAG, "SECURITY ALERT: Packet from Node 0x%02X rejected by Ranging Gating (Dist: %u cm outside envelope!)",
                     src_idx, dist);
            return;
        }

        // Peer-Status aktualisieren
        m_peers[src_idx].online = true;
        m_peers[src_idx].last_seen_ms = (uint32_t)(esp_timer_get_time() / 1000);
        m_peers[src_idx].last_rssi = rssi_dbm;
    }

    m_rx_count++;
    const uint8_t *payload = frame_data + sizeof(UwbBackboneHeader);

    // 5. Paket-Typ Dispatching
    switch (hdr->pkt_type) {
        case UWB_PKT_PTT_EVENT:
            if (payload_len >= sizeof(UwbPttEventPkt) && m_ptt_cb) {
                const UwbPttEventPkt *ptt = (const UwbPttEventPkt *)payload;
                m_ptt_cb(*ptt, (UwbNodeType)hdr->source_node);
            }
            break;

        case UWB_PKT_FRONT_TELEMETRY:
            if (payload_len >= sizeof(UwbFrontTelemetryPkt) && m_telem_cb) {
                const UwbFrontTelemetryPkt *telem = (const UwbFrontTelemetryPkt *)payload;
                m_telem_cb(*telem);
            }
            break;

        case UWB_PKT_CARTRIDGE_ANNOUNCE:
            if (payload_len >= sizeof(UwbCartridgeAnnouncePkt) && m_cart_ann_cb) {
                const UwbCartridgeAnnouncePkt *ann = (const UwbCartridgeAnnouncePkt *)payload;
                m_cart_ann_cb(*ann, (UwbNodeType)hdr->source_node);
            }
            break;

        case UWB_PKT_CARTRIDGE_OPCODE:
            if (payload_len >= sizeof(UwbCartridgeOpcodePkt) && m_cart_op_cb) {
                const UwbCartridgeOpcodePkt *op = (const UwbCartridgeOpcodePkt *)payload;
                m_cart_op_cb(*op, (UwbNodeType)hdr->source_node);
            }
            break;

        case UWB_PKT_CARTRIDGE_ACK:
            if (payload_len >= sizeof(UwbCartridgeAckPkt) && m_cart_ack_cb) {
                const UwbCartridgeAckPkt *ack = (const UwbCartridgeAckPkt *)payload;
                m_cart_ack_cb(*ack, (UwbNodeType)hdr->source_node);
            }
            break;

        case UWB_PKT_RADAR_TARGETS:
            if (payload_len >= sizeof(UwbRadarTargetsPkt) && m_radar_cb) {
                const UwbRadarTargetsPkt *radar = (const UwbRadarTargetsPkt *)payload;
                m_radar_cb(*radar);
            }
            break;

        case UWB_PKT_RADAR_LED_CMD:
            if (payload_len >= sizeof(UwbRadarLedCmdPkt) && m_radar_led_cb) {
                const UwbRadarLedCmdPkt *cmd = (const UwbRadarLedCmdPkt *)payload;
                m_radar_led_cb(*cmd);
            }
            break;

        case UWB_PKT_NODE_HEARTBEAT:
            if (payload_len >= sizeof(UwbNodeHeartbeatPkt)) {
                const UwbNodeHeartbeatPkt *hb = (const UwbNodeHeartbeatPkt *)payload;
                if (src_idx <= 5) {
                    m_peers[src_idx].distance_cm = hb->ranging_dist_cm;
                }
                if (m_heartbeat_cb) {
                    m_heartbeat_cb((UwbNodeType)hdr->source_node, *hb);
                }
            }
            break;

        default:
            break;
    }
}

// -----------------------------------------------------------------------------
// Sende-Methoden
// -----------------------------------------------------------------------------
esp_err_t UwbVehicleBackbone::send_packet(UwbNodeType target, UwbBackbonePktType type, const void *payload, size_t len) {
    if (len > UWB_BACKBONE_MAX_PAYLOAD || !m_driver) {
        return ESP_ERR_INVALID_ARG;
    }

    uint8_t frame[UWB_BACKBONE_MAX_FRAME_SIZE];
    UwbBackboneHeader *hdr = (UwbBackboneHeader *)frame;

    hdr->magic        = UWB_BACKBONE_MAGIC;
    hdr->pkt_type     = (uint8_t)type;
    hdr->source_node  = (uint8_t)m_local_node_type;
    hdr->target_node  = (uint8_t)target;
    hdr->seq_num      = m_seq_counter++;
    hdr->timestamp_us = (uint32_t)esp_timer_get_time();
    hdr->payload_len  = (uint8_t)len;

    if (payload && len > 0) {
        memcpy(frame + sizeof(UwbBackboneHeader), payload, len);
    }

    // CRC16 berechnen und anfügen
    uint16_t crc = uwb_calculate_crc16(frame, sizeof(UwbBackboneHeader) + len);
    frame[sizeof(UwbBackboneHeader) + len]     = (uint8_t)(crc & 0xFF);
    frame[sizeof(UwbBackboneHeader) + len + 1] = (uint8_t)((crc >> 8) & 0xFF);

    size_t total_len = sizeof(UwbBackboneHeader) + len + 2;
    return dw3110_transmit(m_driver, frame, total_len, false);
}

esp_err_t UwbVehicleBackbone::send_ptt_event(UwbHandlebarButton button, UwbPttEventType evt, uint16_t duration_ms, uint8_t bat_pct) {
    UwbPttEventPkt pkt = {
        .button_id = (uint8_t)button,
        .event_type = (uint8_t)evt,
        .press_duration_ms = duration_ms,
        .battery_pct = bat_pct,
        .flags = 0
    };
    return send_packet(UWB_NODE_CENTRAL_BOX, UWB_PKT_PTT_EVENT, &pkt, sizeof(pkt));
}

esp_err_t UwbVehicleBackbone::send_front_telemetry(const UwbFrontTelemetryPkt &telem) {
    return send_packet(UWB_NODE_CENTRAL_BOX, UWB_PKT_FRONT_TELEMETRY, &telem, sizeof(telem));
}

esp_err_t UwbVehicleBackbone::send_cartridge_announce(uint8_t hw_class, uint16_t model_id, uint64_t uid, uint16_t vcc_mv) {
    UwbCartridgeAnnouncePkt pkt = {
        .hardware_class = hw_class,
        .model_id = model_id,
        .cartridge_uid = uid,
        .roaming_keys_count = 1,
        .vcc_mv = vcc_mv,
        .status_flags = 0x07 // Headset docked, Codec OK, MOSFETs ready
    };
    return send_packet(UWB_NODE_CENTRAL_BOX, UWB_PKT_CARTRIDGE_ANNOUNCE, &pkt, sizeof(pkt));
}

esp_err_t UwbVehicleBackbone::send_cartridge_opcode(UwbNodeType target_bay, uint8_t token, UwbCartridgeOpcode opcode, uint16_t pulse_ms, uint8_t act_mask) {
    UwbCartridgeOpcodePkt pkt = {
        .seq_token = token,
        .opcode = (uint8_t)opcode,
        .pulse_duration_ms = pulse_ms,
        .actuator_mask = act_mask
    };
    return send_packet(target_bay, UWB_PKT_CARTRIDGE_OPCODE, &pkt, sizeof(pkt));
}

esp_err_t UwbVehicleBackbone::send_cartridge_ack(UwbNodeType target_box, uint8_t token, uint8_t opcode, uint8_t result, uint8_t act_mask, uint16_t exec_us) {
    UwbCartridgeAckPkt pkt = {
        .seq_token = token,
        .opcode_executed = opcode,
        .result_code = result,
        .active_actuators = act_mask,
        .execution_time_us = exec_us
    };
    return send_packet(target_box, UWB_PKT_CARTRIDGE_ACK, &pkt, sizeof(pkt));
}

esp_err_t UwbVehicleBackbone::send_radar_targets(const UwbRadarTargetsPkt &radar) {
    return send_packet(UWB_NODE_CENTRAL_BOX, UWB_PKT_RADAR_TARGETS, &radar, sizeof(radar));
}

esp_err_t UwbVehicleBackbone::send_radar_led_cmd(uint8_t macro, uint8_t brightness, uint8_t left_bsd, uint8_t right_bsd) {
    UwbRadarLedCmdPkt pkt = {
        .macro_mode = macro,
        .brightness_pct = brightness,
        .left_bsd_state = left_bsd,
        .right_bsd_state = right_bsd
    };
    return send_packet(UWB_NODE_REAR_RADAR, UWB_PKT_RADAR_LED_CMD, &pkt, sizeof(pkt));
}

esp_err_t UwbVehicleBackbone::send_heartbeat(uint16_t vbus_mv, int16_t temp_c_10) {
    UwbNodeHeartbeatPkt pkt = {
        .uptime_sec = (uint32_t)(esp_timer_get_time() / 1000000),
        .vbus_mv = vbus_mv,
        .temperature_c_10 = temp_c_10,
        .ranging_dist_cm = (m_local_node_type == UWB_NODE_FRONT_NODE) ? 140 : 80,
        .rssi_dbm = -72,
        .link_quality = 98
    };
    return send_packet(UWB_NODE_BROADCAST, UWB_PKT_NODE_HEARTBEAT, &pkt, sizeof(pkt));
}

esp_err_t UwbVehicleBackbone::send_pairing_request(uint64_t nonce, uint32_t vin_hash, uint16_t timeout_sec) {
    UwbPairingRequestPkt pkt = {
        .pairing_nonce = nonce,
        .vehicle_vin_hash = vin_hash,
        .timeout_sec = timeout_sec
    };
    return send_packet(UWB_NODE_BROADCAST, UWB_PKT_PAIRING_REQUEST, &pkt, sizeof(pkt));
}

esp_err_t UwbVehicleBackbone::send_pairing_confirm(UwbNodeType target_node, uint64_t nonce, const uint8_t *session_key, uint8_t slot) {
    UwbPairingConfirmPkt pkt = {};
    pkt.pairing_nonce = nonce;
    pkt.roaming_slot = slot;
    pkt.status = 0; // Success
    if (session_key) {
        memcpy(pkt.session_key, session_key, 16);
    }
    return send_packet(target_node, UWB_PKT_PAIRING_CONFIRM, &pkt, sizeof(pkt));
}

bool UwbVehicleBackbone::is_peer_online(UwbNodeType node) const {
    if (node <= 5) {
        return m_peers[node].online;
    }
    return false;
}

uint16_t UwbVehicleBackbone::get_peer_distance_cm(UwbNodeType node) const {
    if (node <= 5) {
        return m_peers[node].distance_cm;
    }
    return 0;
}

uint32_t UwbVehicleBackbone::get_peer_last_seen_ms(UwbNodeType node) const {
    if (node <= 5) {
        return m_peers[node].last_seen_ms;
    }
    return 0;
}
