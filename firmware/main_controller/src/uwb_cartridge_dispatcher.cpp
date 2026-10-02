#include "uwb_cartridge_dispatcher.h"
#include <string.h>
#include <stdio.h>
#include "esp_log.h"
#include "esp_timer.h"

static const char *TAG = "UWB_CART_DISPATCH";

static CartridgeBayState_t s_bays[2] = {}; // 0 = Bay 1 (Links), 1 = Bay 2 (Rechts)
static uint8_t s_token_counter = 1;

static const char* resolve_model_name(uint16_t model_id) {
    switch (model_id) {
        case 0x0101: return "Sena SPIDER X Slim";
        case 0x0102: return "Sena +Mesh Adapter";
        case 0x0201: return "Cardo Packtalk Edge/Pro";
        case 0x0202: return "Cardo Packtalk Bold/Black";
        case 0x0301: return "Cardo Freecom UCS";
        case 0x0302: return "Midland Mesh UCS";
        case 0x0303: return "OMM 2.4 GHz OEM Transceiver";
        case 0x0401: return "Midland PMR446 (Alan/G9)";
        default:     return "Universal Modular Cartridge";
    }
}

static void on_cartridge_announce(const UwbCartridgeAnnouncePkt &pkt, UwbNodeType source) {
    int bay_idx = (source == UWB_NODE_CARTRIDGE_BAY1) ? 0 :
                  (source == UWB_NODE_CARTRIDGE_BAY2) ? 1 : -1;
    if (bay_idx < 0) return;

    CartridgeBayState_t &bay = s_bays[bay_idx];
    bay.active = true;
    bay.hardware_class = pkt.hardware_class;
    bay.model_id = pkt.model_id;
    bay.uid = pkt.cartridge_uid;
    bay.vcc_mv = pkt.vcc_mv;
    snprintf(bay.model_name, sizeof(bay.model_name), "%s", resolve_model_name(pkt.model_id));

    ESP_LOGI(TAG, "UWB Cartridge ANNOUNCE from Bay %d (0x%02X): Model 0x%04X '%s' (UID: 0x%016llX, VCC: %u mV)",
             bay_idx + 1, (uint8_t)source, pkt.model_id, bay.model_name,
             (unsigned long long)pkt.cartridge_uid, pkt.vcc_mv);
}

static void on_cartridge_ack(const UwbCartridgeAckPkt &pkt, UwbNodeType source) {
    int bay_idx = (source == UWB_NODE_CARTRIDGE_BAY1) ? 0 :
                  (source == UWB_NODE_CARTRIDGE_BAY2) ? 1 : -1;
    if (bay_idx < 0) return;

    CartridgeBayState_t &bay = s_bays[bay_idx];
    bay.last_ack_time_ms = (uint32_t)(esp_timer_get_time() / 1000);
    bay.last_result_code = pkt.result_code;
    bay.last_exec_us = pkt.execution_time_us;

    ESP_LOGI(TAG, "UWB Cartridge ACK from Bay %d: Token %u, Opcode 0x%02X, Result: %d (Exec: %u µs, Act: 0x%02X)",
             bay_idx + 1, pkt.seq_token, pkt.opcode_executed, pkt.result_code,
             pkt.execution_time_us, pkt.active_actuators);
}

esp_err_t uwb_cartridge_dispatcher_init(void) {
    ESP_LOGI(TAG, "Initializing UWB Smart Cartridge Dispatcher for Bay 1 & Bay 2...");
    memset(s_bays, 0, sizeof(s_bays));

    // Callbacks beim UwbVehicleBackbone registrieren
    UwbVehicleBackbone::instance().set_cartridge_announce_callback(on_cartridge_announce);
    UwbVehicleBackbone::instance().set_cartridge_ack_callback(on_cartridge_ack);

    return ESP_OK;
}

esp_err_t uwb_cartridge_send_opcode(UwbNodeType bay, UwbCartridgeOpcode opcode, uint16_t custom_pulse_ms) {
    if (bay != UWB_NODE_CARTRIDGE_BAY1 && bay != UWB_NODE_CARTRIDGE_BAY2) {
        return ESP_ERR_INVALID_ARG;
    }

    uint8_t token = s_token_counter++;
    if (token == 0) s_token_counter = 1;

    uint8_t act_mask = 0;
    // Standard-Aktuatormaske je nach Opcode ableiten
    switch (opcode) {
        case CARTRIDGE_OPCODE_POWER_BOOT:
        case CARTRIDGE_OPCODE_POWER_OFF:
            act_mask = (1 << 0) | (1 << 2); // Center + Plus
            break;
        case CARTRIDGE_OPCODE_VOLUME_UP:
            act_mask = (1 << 0); // Plus
            break;
        case CARTRIDGE_OPCODE_VOLUME_DOWN:
            act_mask = (1 << 1); // Minus
            break;
        case CARTRIDGE_OPCODE_MESH_TOGGLE:
        case CARTRIDGE_OPCODE_OPEN_GROUP_SW:
            act_mask = (1 << 3); // Mesh
            break;
        default:
            act_mask = 0x01;
            break;
    }

    ESP_LOGI(TAG, "Dispatching UWB Opcode 0x%02X to Bay 0x%02X (Token: %u, Pulse: %u ms, ActMask: 0x%02X)...",
             (uint8_t)opcode, (uint8_t)bay, token, custom_pulse_ms, act_mask);

    return UwbVehicleBackbone::instance().send_cartridge_opcode(bay, token, opcode, custom_pulse_ms, act_mask);
}

esp_err_t uwb_cartridge_power_on_all(void) {
    ESP_LOGI(TAG, "Broadcasting UWB POWER_BOOT (Opcode 0x01) to all active bays...");
    esp_err_t err1 = uwb_cartridge_send_opcode(UWB_NODE_CARTRIDGE_BAY1, CARTRIDGE_OPCODE_POWER_BOOT, 1000);
    esp_err_t err2 = uwb_cartridge_send_opcode(UWB_NODE_CARTRIDGE_BAY2, CARTRIDGE_OPCODE_POWER_BOOT, 1000);
    return (err1 == ESP_OK || err2 == ESP_OK) ? ESP_OK : ESP_FAIL;
}

esp_err_t uwb_cartridge_power_off_all(void) {
    ESP_LOGI(TAG, "Broadcasting UWB POWER_OFF (Opcode 0x02) to all active bays...");
    esp_err_t err1 = uwb_cartridge_send_opcode(UWB_NODE_CARTRIDGE_BAY1, CARTRIDGE_OPCODE_POWER_OFF, 200);
    esp_err_t err2 = uwb_cartridge_send_opcode(UWB_NODE_CARTRIDGE_BAY2, CARTRIDGE_OPCODE_POWER_OFF, 200);
    return (err1 == ESP_OK || err2 == ESP_OK) ? ESP_OK : ESP_FAIL;
}

esp_err_t uwb_cartridge_toggle_mesh(UwbNodeType bay) {
    return uwb_cartridge_send_opcode(bay, CARTRIDGE_OPCODE_MESH_TOGGLE, 200);
}

CartridgeBayState_t uwb_cartridge_get_bay_state(UwbNodeType bay) {
    int idx = (bay == UWB_NODE_CARTRIDGE_BAY1) ? 0 : 1;
    return s_bays[idx];
}
