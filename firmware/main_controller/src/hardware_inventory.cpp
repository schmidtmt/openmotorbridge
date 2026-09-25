#include "hardware_inventory.h"
#include "cartridge_onewire.h"
#include "gnss_omm_bridge.h"
#include "esp_now_front_node_client.h"
#include "radar_processor.h"
#include "tpms_ble_scanner.h"
#include "can_bus_manager.h"
#include "radar_mr20_protocol.h"
#include "driver/uart.h"
#include "nvs_flash.h"
#include "nvs.h"
#include "esp_log.h"
#include <string.h>

static const char *TAG = "HW_INVENTORY";

#define RADAR_UART_NUM UART_NUM_2

static HardwareInventoryState_t s_state = {
    .baseline_mask = 0,
    .current_mask = 0,
    .newly_found_mask = 0,
    .lost_mask = 0,
    .boot_cycle_count = 0,
    .has_critical_loss = false
};

// CRC16 Helper
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
    ESP_LOGI(TAG, "Initializing Hardware Inventory & Topology Supervisor...");

    nvs_handle_t handle;
    esp_err_t err = nvs_open("omb_sys", NVS_READWRITE, &handle);
    if (err == ESP_OK) {
        uint16_t b_val = 0;
        if (nvs_get_u16(handle, "hw_baseline", &b_val) == ESP_OK) {
            s_state.baseline_mask = b_val;
            ESP_LOGI(TAG, "💾 Loaded Hardware Topology Baseline from NVS: 0x%04X", s_state.baseline_mask);
        } else {
            // Erstinitialisierung: Noch keine Baseline vorhanden
            s_state.baseline_mask = 0;
            ESP_LOGI(TAG, "First boot: No hardware baseline in NVS. Will auto-learn detected hardware.");
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
        // Fall 1: Weder in Baseline noch aktuell da -> Normalfall (optional nicht verbaut) -> DUNKEL
        *ledA = POST_LED_OFF;
        *ledB = POST_LED_OFF;
    } else if (is_present) {
        // Fall 2: Hardware da (entweder bekannt oder neu erkannt) -> GRÜN OK
        *ledA = POST_LED_GREEN_OK;
        *ledB = is_healthy ? POST_LED_GREEN_OK : POST_LED_AMBER_INIT;
    } else {
        // Fall 3: In Baseline als aktiv gespeichert, aber jetzt FEHLEND -> ANOMALIE / ROT BLINKEND!
        *ledA = POST_LED_RED_BLINK;
        *ledB = POST_LED_RED_FAIL;
    }
}

void hw_inventory_scan_and_evaluate(void) {
    uint16_t current = 0;

    // 1. Bus-Scans und Präsenz-Checks
    CartridgeInfo_t pod1 = cartridge_get_info(1);
    if (pod1.is_connected) current |= HW_INV_POD1;

    CartridgeInfo_t pod2 = cartridge_get_info(2);
    if (pod2.is_connected) current |= HW_INV_POD2;

    bool pod3_ok = gnss_bridge_is_pod3_connected();
    if (pod3_ok) current |= HW_INV_POD3;

    FrontNodeStatus front = esp_now_front_node_get_status();
    if (front.is_linked) current |= HW_INV_FRONT_NODE;

    RadarState_t radar = radar_get_current_state();
    if (radar.hw_type != RADAR_HW_TYPE_UNKNOWN) current |= HW_INV_RADAR;

    // TPMS
    current |= HW_INV_TPMS_FRONT; // Sensors active or registered
    current |= HW_INV_TPMS_REAR;

    // CAN-Bus
    current |= HW_INV_CAN_BUS;

    s_state.current_mask = current;

    // 2. Baseline-Vergleich: Neu erkannt vs. Verloren
    s_state.newly_found_mask = current & ~s_state.baseline_mask;
    s_state.lost_mask = s_state.baseline_mask & ~current;
    s_state.has_critical_loss = (s_state.lost_mask != 0);

    // 3. Auto-Discovery: Neu angeschlossene Hardware wird gelernt
    if (s_state.newly_found_mask != 0) {
        s_state.baseline_mask |= s_state.newly_found_mask;
        nvs_handle_t handle;
        if (nvs_open("omb_sys", NVS_READWRITE, &handle) == ESP_OK) {
            nvs_set_u16(handle, "hw_baseline", s_state.baseline_mask);
            nvs_commit(handle);
            nvs_close(handle);
            ESP_LOGI(TAG, "✨ Auto-discovered new hardware: 0x%04X -> Updated NVS baseline to 0x%04X",
                     s_state.newly_found_mask, s_state.baseline_mask);
        }
    }

    // 4. Warnung bei Hardware-Verlust
    if (s_state.has_critical_loss) {
        ESP_LOGE(TAG, "🚨 HARDWARE LOSS ANOMALY DETECTED! Lost mask: 0x%04X (Baseline: 0x%04X, Now: 0x%04X)",
                 s_state.lost_mask, s_state.baseline_mask, s_state.current_mask);
        if (s_state.lost_mask & HW_INV_POD3) {
            ESP_LOGE(TAG, "   ⚠️ Satelliten-Pod 3 (Heck-Backbone) FEHLT! (Zuvor aktiv, antwortet nicht)");
        }
        if (s_state.lost_mask & HW_INV_POD1) {
            ESP_LOGE(TAG, "   ⚠️ Satelliten-Pod 1 (Intercom A) FEHLT!");
        }
        if (s_state.lost_mask & HW_INV_POD2) {
            ESP_LOGE(TAG, "   ⚠️ Satelliten-Pod 2 (Intercom B) FEHLT!");
        }
        if (s_state.lost_mask & HW_INV_FRONT_NODE) {
            ESP_LOGE(TAG, "   ⚠️ Universal Front-Node (Cockpit) FEHLT!");
        }
        if (s_state.lost_mask & HW_INV_RADAR) {
            ESP_LOGE(TAG, "   ⚠️ Radar 2.0 / Garmin Varia FEHLT!");
        }
    } else {
        ESP_LOGI(TAG, "✓ Hardware Inventory verification passed (Mask: 0x%04X, Baseline: 0x%04X)",
                 s_state.current_mask, s_state.baseline_mask);
    }

    // 5. 18-Paar Diagnosematrix generieren & an Sub-MCU übermitteln
    RadarPostDiagPacket_t diag_pkt;
    memset(&diag_pkt, 0, sizeof(diag_pkt));
    diag_pkt.sync1 = OMB_RADAR_SYNC_BYTE_1;
    diag_pkt.sync2 = OMB_RADAR_SYNC_BYTE_2;
    diag_pkt.version = OMB_RADAR_PROTOCOL_VERSION;
    diag_pkt.pkt_type = RADAR_PKT_CMD_POST_DIAG;
    diag_pkt.duration_tenths_s = 25; // 2.5 Sekunden

    // Pair 1: Front-Node (D1/D2)
    eval_hw_node(HW_INV_FRONT_NODE, (current & HW_INV_FRONT_NODE), front.is_linked, &diag_pkt.led_states[0], &diag_pkt.led_states[1]);
    // Pair 2: CAN-Bus (D3/D4)
    eval_hw_node(HW_INV_CAN_BUS, (current & HW_INV_CAN_BUS), true, &diag_pkt.led_states[2], &diag_pkt.led_states[3]);
    // Pair 3: Pod 1 (D5/D6)
    eval_hw_node(HW_INV_POD1, (current & HW_INV_POD1), pod1.is_connected, &diag_pkt.led_states[4], &diag_pkt.led_states[5]);
    // Pair 4: BSD Spiegel Links (D7/D8)
    eval_hw_node(HW_INV_FRONT_NODE, (current & HW_INV_FRONT_NODE), true, &diag_pkt.led_states[6], &diag_pkt.led_states[7]);
    // Pair 5: TPMS Vorne (D9/D10)
    eval_hw_node(HW_INV_TPMS_FRONT, (current & HW_INV_TPMS_FRONT), true, &diag_pkt.led_states[8], &diag_pkt.led_states[9]);
    // Pair 6: Actioncam (D11/D12)
    eval_hw_node(HW_INV_ACTION_CAM, (current & HW_INV_ACTION_CAM), true, &diag_pkt.led_states[10], &diag_pkt.led_states[11]);

    // Pair 7: GNSS MAX-M10S (D13/D14)
    eval_hw_node(HW_INV_POD3, pod3_ok, true, &diag_pkt.led_states[12], &diag_pkt.led_states[13]);
    // Pair 8: LoRa SX1262 (D15/D16)
    eval_hw_node(HW_INV_POD3, pod3_ok, true, &diag_pkt.led_states[14], &diag_pkt.led_states[15]);
    // Pair 9: V2X / Wi-Fi (D17/D18)
    eval_hw_node(HW_INV_RADAR, (current & HW_INV_RADAR), true, &diag_pkt.led_states[16], &diag_pkt.led_states[17]);

    // Pair 10: Pod 2 (D19/D20)
    eval_hw_node(HW_INV_POD2, (current & HW_INV_POD2), pod2.is_connected, &diag_pkt.led_states[18], &diag_pkt.led_states[19]);
    // Pair 11: Pod 3 Backbone (D21/D22)
    eval_hw_node(HW_INV_POD3, pod3_ok, true, &diag_pkt.led_states[20], &diag_pkt.led_states[21]);
    // Pair 12: BSD Spiegel Rechts (D23/D24)
    eval_hw_node(HW_INV_FRONT_NODE, (current & HW_INV_FRONT_NODE), true, &diag_pkt.led_states[22], &diag_pkt.led_states[23]);
    // Pair 13: TPMS Hinten (D25/D26)
    eval_hw_node(HW_INV_TPMS_REAR, (current & HW_INV_TPMS_REAR), true, &diag_pkt.led_states[24], &diag_pkt.led_states[25]);
    // Pair 14: Dallas DS18B20 (D27/D28)
    eval_hw_node(HW_INV_POD3, pod3_ok, true, &diag_pkt.led_states[26], &diag_pkt.led_states[27]);
    // Pair 15: MicroSD Card (D29/D30)
    eval_hw_node(HW_INV_SD_CARD, true, true, &diag_pkt.led_states[28], &diag_pkt.led_states[29]);

    // Pair 16: 12V KL15 (D31/D32)
    diag_pkt.led_states[30] = POST_LED_GREEN_OK; diag_pkt.led_states[31] = POST_LED_GREEN_OK;
    // Pair 17: 18650 USV (D33/D34)
    diag_pkt.led_states[32] = POST_LED_GREEN_OK; diag_pkt.led_states[33] = POST_LED_GREEN_OK;
    // Pair 18: Wheeltec MR20 Radar (D35/D36)
    eval_hw_node(HW_INV_RADAR, (current & HW_INV_RADAR), true, &diag_pkt.led_states[34], &diag_pkt.led_states[35]);

    diag_pkt.checksum = crc16_ccitt((const uint8_t *)&diag_pkt, sizeof(diag_pkt) - 2);

    // Asynchron an Sub-MCU senden (Blockiert nicht, falls kein Radar montiert ist)
    uart_write_bytes(RADAR_UART_NUM, (const char *)&diag_pkt, sizeof(diag_pkt));
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
