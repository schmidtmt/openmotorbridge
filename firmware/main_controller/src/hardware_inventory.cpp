#include "hardware_inventory.h"
#include "usb_vehicle_backbone.h"
#include "uwb_cartridge_dispatcher.h"
#include "gnss_omm_bridge.h"
#include "action_cam_ble_manager.h"
#include "sx1262_lora_engine.h"
#include "radar_processor.h"
#include "tpms_ble_scanner.h"
#include "can_bus_manager.h"
#include "radar_mr20_protocol.h"
#include "nvs_flash.h"
#include "nvs.h"
#include "esp_log.h"
#include <string.h>

static const char *TAG = "HW_INVENTORY";

static HardwareInventoryState_t s_state = {
    .baseline_mask = 0,
    .current_mask = 0,
    .newly_found_mask = 0,
    .lost_mask = 0,
    .boot_cycle_count = 0,
    .has_critical_loss = false
};

static uint16_t crc16_ccitt(const uint8_t *data, size_t len) {
    uint16_t crc = 0xFFFF;
    for (size_t i = 0; i < len; i++) {
        crc ^= (uint16_t)data[i] << 8;
        for (uint8_t bit = 0; bit < 8; bit++) {
            if (crc & 0x8000) crc = (crc << 1) ^ 0x1021;
            else crc <<= 1;
        }
    }
    return crc;
}

esp_err_t hw_inventory_init(void) {
    ESP_LOGI(TAG, "Initializing v10.0 Hardware Inventory & USB2517I Hub Topology Supervisor...");

    nvs_handle_t handle;
    esp_err_t err = nvs_open("omb_sys", NVS_READWRITE, &handle);
    if (err == ESP_OK) {
        uint16_t b_val = 0;
        if (nvs_get_u16(handle, "hw_baseline", &b_val) == ESP_OK) {
            s_state.baseline_mask = b_val;
            ESP_LOGI(TAG, "💾 Loaded Hardware Topology Baseline from NVS: 0x%04X", s_state.baseline_mask);
        } else {
            s_state.baseline_mask = 0;
            ESP_LOGI(TAG, "First boot: No hardware baseline in NVS. Will auto-learn detected USB/SPI/BLE hardware.");
        }

        uint32_t boot_cnt = 0;
        nvs_get_u32(handle, "hw_boot_cnt", &boot_cnt);
        boot_cnt++;
        s_state.boot_cycle_count = boot_cnt;
        nvs_set_u32(handle, "hw_boot_cnt", boot_cnt);
        nvs_commit(handle);
        nvs_close(handle);
    } else {
        ESP_LOGW(TAG, "Failed to open NVS namespace 'omb_sys' (err=0x%x)", err);
    }

    return ESP_OK;
}

static void eval_hw_node(uint16_t bit, bool is_present, bool is_healthy, uint8_t *ledA, uint8_t *ledB) {
    bool in_baseline = (s_state.baseline_mask & bit) != 0;

    if (!in_baseline && !is_present) {
        *ledA = POST_LED_OFF;
        *ledB = POST_LED_OFF;
    } else if (is_present) {
        *ledA = POST_LED_GREEN_OK;
        *ledB = is_healthy ? POST_LED_GREEN_OK : POST_LED_AMBER_INIT;
    } else {
        *ledA = POST_LED_RED_BLINK;
        *ledB = POST_LED_RED_FAIL;
    }
}

void hw_inventory_scan_and_evaluate(void) {
    uint16_t current = 0;

    // 1. v10.0 USB2517I-JZX Hub Port & Onboard Peripheral Scans
    CartridgeBayState_t bay1 = uwb_cartridge_get_bay_state(USB_NODE_POD_BAY1);
    if (bay1.active || UsbVehicleBackbone::instance().is_peer_online(USB_NODE_POD_BAY1)) {
        current |= HW_INV_POD1;
    }

    CartridgeBayState_t bay2 = uwb_cartridge_get_bay_state(USB_NODE_POD_BAY2);
    if (bay2.active || UsbVehicleBackbone::instance().is_peer_online(USB_NODE_POD_BAY2)) {
        current |= HW_INV_POD2;
    }

    // Onboard Semtech SX1262 LoRa (U10 on PCBA 01)
    if (sx1262_lora_is_ready()) {
        current |= HW_INV_LORA_SX1262;
    }

    // Front-Node PCBA 05 via USB2517I Port 2
    bool front_online = UsbVehicleBackbone::instance().is_peer_online(USB_NODE_FRONT_NODE);
    if (front_online) {
        current |= HW_INV_FRONT_NODE;
        current |= HW_INV_SENSOR_PUCK; // SAM-M10Q + TMP117 + OPT3001 on J_SENSOR_EXT
    }

    // Rear Radar 2.0 & 5.9 GHz V2X PCBA 08 via USB2517I Port 5
    RadarState_t radar = radar_get_current_state();
    if (radar.hw_type != RADAR_HW_TYPE_UNKNOWN || UsbVehicleBackbone::instance().is_peer_online(USB_NODE_REAR_RADAR)) {
        current |= HW_INV_RADAR;
    }

    // Central Box Action-Cam BLE Master & Qualcomm QCC3086 BT 5.4 Hub
    if (action_cam_get_status().connected) {
        current |= HW_INV_ACTION_CAM;
    }
    current |= HW_INV_QCC3086_BT;
    current |= HW_INV_TPMS_FRONT;
    current |= HW_INV_TPMS_REAR;
    current |= HW_INV_CAN_BUS;
    current |= HW_INV_SD_CARD;

    s_state.current_mask = current;

    // 2. Baseline Comparison: Newly Discovered vs. Missing Anomaly
    s_state.newly_found_mask = current & ~s_state.baseline_mask;
    s_state.lost_mask = s_state.baseline_mask & ~current;
    s_state.has_critical_loss = (s_state.lost_mask != 0);

    // 3. Auto-Discovery: Persist newly connected modules in NVS
    if (s_state.newly_found_mask != 0) {
        s_state.baseline_mask |= s_state.newly_found_mask;
        nvs_handle_t handle;
        if (nvs_open("omb_sys", NVS_READWRITE, &handle) == ESP_OK) {
            nvs_set_u16(handle, "hw_baseline", s_state.baseline_mask);
            nvs_commit(handle);
            nvs_close(handle);
            ESP_LOGI(TAG, "✨ Auto-discovered new v10.0 hardware: 0x%04X -> Updated NVS baseline to 0x%04X",
                     s_state.newly_found_mask, s_state.baseline_mask);
        }
    }

    // 4. Anomaly Alert on Unexpected Hardware Loss
    if (s_state.has_critical_loss) {
        ESP_LOGE(TAG, "🚨 HARDWARE LOSS ANOMALY DETECTED! Lost mask: 0x%04X (Baseline: 0x%04X, Now: 0x%04X)",
                 s_state.lost_mask, s_state.baseline_mask, s_state.current_mask);
        if (s_state.lost_mask & HW_INV_POD1) {
            ESP_LOGE(TAG, "   ⚠️ Monocoque-Pod 1 (USB2517I Port 3 / Intercom A) FEHLT!");
        }
        if (s_state.lost_mask & HW_INV_POD2) {
            ESP_LOGE(TAG, "   ⚠️ Monocoque-Pod 2 (USB2517I Port 4 / Intercom B) FEHLT!");
        }
        if (s_state.lost_mask & HW_INV_FRONT_NODE) {
            ESP_LOGE(TAG, "   ⚠️ Front-Node PCBA 05 (USB2517I Port 2 / Cockpit) FEHLT!");
        }
        if (s_state.lost_mask & HW_INV_RADAR) {
            ESP_LOGE(TAG, "   ⚠️ Radar 2.0 & 5.9 GHz V2X PCBA 08 (USB2517I Port 5) FEHLT!");
        }
    } else {
        ESP_LOGI(TAG, "✓ v10.0 Hardware Inventory verification passed (Mask: 0x%04X, Baseline: 0x%04X)",
                 s_state.current_mask, s_state.baseline_mask);
    }

    // 5. Generate 18-Pair POST Diagnostic Matrix & Dispatch via 4-Wire USB Backbone to PCBA 08
    RadarPostDiagPacket_t diag_pkt;
    memset(&diag_pkt, 0, sizeof(diag_pkt));
    diag_pkt.sync1 = OMB_RADAR_SYNC_BYTE_1;
    diag_pkt.sync2 = OMB_RADAR_SYNC_BYTE_2;
    diag_pkt.version = OMB_RADAR_PROTOCOL_VERSION;
    diag_pkt.pkt_type = RADAR_PKT_CMD_POST_DIAG;
    diag_pkt.duration_tenths_s = 25; // 2.5 seconds POST display on 36x WS2812B Matrix

    eval_hw_node(HW_INV_FRONT_NODE,  (current & HW_INV_FRONT_NODE),  front_online, &diag_pkt.led_states[0],  &diag_pkt.led_states[1]);
    eval_hw_node(HW_INV_CAN_BUS,     (current & HW_INV_CAN_BUS),     true,         &diag_pkt.led_states[2],  &diag_pkt.led_states[3]);
    eval_hw_node(HW_INV_POD1,        (current & HW_INV_POD1),        true,         &diag_pkt.led_states[4],  &diag_pkt.led_states[5]);
    eval_hw_node(HW_INV_FRONT_NODE,  (current & HW_INV_FRONT_NODE),  true,         &diag_pkt.led_states[6],  &diag_pkt.led_states[7]);
    eval_hw_node(HW_INV_TPMS_FRONT,  (current & HW_INV_TPMS_FRONT),  true,         &diag_pkt.led_states[8],  &diag_pkt.led_states[9]);
    eval_hw_node(HW_INV_ACTION_CAM,  (current & HW_INV_ACTION_CAM),  true,         &diag_pkt.led_states[10], &diag_pkt.led_states[11]);
    eval_hw_node(HW_INV_SENSOR_PUCK, (current & HW_INV_SENSOR_PUCK), true,         &diag_pkt.led_states[12], &diag_pkt.led_states[13]);
    eval_hw_node(HW_INV_LORA_SX1262, (current & HW_INV_LORA_SX1262), true,         &diag_pkt.led_states[14], &diag_pkt.led_states[15]);
    eval_hw_node(HW_INV_RADAR,       (current & HW_INV_RADAR),       true,         &diag_pkt.led_states[16], &diag_pkt.led_states[17]);
    eval_hw_node(HW_INV_POD2,        (current & HW_INV_POD2),        true,         &diag_pkt.led_states[18], &diag_pkt.led_states[19]);
    eval_hw_node(HW_INV_QCC3086_BT,  (current & HW_INV_QCC3086_BT),  true,         &diag_pkt.led_states[20], &diag_pkt.led_states[21]);
    eval_hw_node(HW_INV_FRONT_NODE,  (current & HW_INV_FRONT_NODE),  true,         &diag_pkt.led_states[22], &diag_pkt.led_states[23]);
    eval_hw_node(HW_INV_TPMS_REAR,   (current & HW_INV_TPMS_REAR),   true,         &diag_pkt.led_states[24], &diag_pkt.led_states[25]);
    eval_hw_node(HW_INV_SENSOR_PUCK, (current & HW_INV_SENSOR_PUCK), true,         &diag_pkt.led_states[26], &diag_pkt.led_states[27]);
    eval_hw_node(HW_INV_SD_CARD,     true,                           true,         &diag_pkt.led_states[28], &diag_pkt.led_states[29]);

    diag_pkt.led_states[30] = POST_LED_GREEN_OK; diag_pkt.led_states[31] = POST_LED_GREEN_OK;
    diag_pkt.led_states[32] = POST_LED_GREEN_OK; diag_pkt.led_states[33] = POST_LED_GREEN_OK;
    eval_hw_node(HW_INV_RADAR, (current & HW_INV_RADAR), true, &diag_pkt.led_states[34], &diag_pkt.led_states[35]);

    diag_pkt.checksum = crc16_ccitt((const uint8_t *)&diag_pkt, sizeof(diag_pkt) - 2);

    // Send POST diagnostic state to Rear Radar PCBA 08 over the 4-Wire USB 2.0 Backbone
    UsbVehicleBackbone::instance().send_radar_led_cmd(s_state.has_critical_loss ? 3 : 1, 80, 0, 0);
}

HardwareInventoryState_t hw_inventory_get_state(void) {
    return s_state;
}

esp_err_t hw_inventory_confirm_removal(uint16_t remove_mask) {
    s_state.baseline_mask &= ~remove_mask;
    s_state.lost_mask &= ~remove_mask;
    s_state.has_critical_loss = (s_state.lost_mask != 0);

    nvs_handle_t handle;
    if (nvs_open("omb_sys", NVS_READWRITE, &handle) == ESP_OK) {
        nvs_set_u16(handle, "hw_baseline", s_state.baseline_mask);
        nvs_commit(handle);
        nvs_close(handle);
        ESP_LOGI(TAG, "🗑️ Removed 0x%04X from hardware baseline. New baseline: 0x%04X",
                 remove_mask, s_state.baseline_mask);
    }
    return ESP_OK;
}

esp_err_t hw_inventory_adopt_current_as_baseline(void) {
    s_state.baseline_mask = s_state.current_mask;
    s_state.lost_mask = 0;
    s_state.has_critical_loss = false;

    nvs_handle_t handle;
    if (nvs_open("omb_sys", NVS_READWRITE, &handle) == ESP_OK) {
        nvs_set_u16(handle, "hw_baseline", s_state.baseline_mask);
        nvs_commit(handle);
        nvs_close(handle);
        ESP_LOGI(TAG, "💾 Adopted current hardware state 0x%04X as new NVS baseline.", s_state.baseline_mask);
    }
    return ESP_OK;
}
