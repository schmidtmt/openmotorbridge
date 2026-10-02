#include "pairing_roaming_mgr.h"
#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "esp_random.h"
#include "esp_timer.h"
#include "nvs_flash.h"
#include "nvs.h"

static const char *TAG = "PAIR_ROAM";
#define NVS_ROAM_NAMESPACE "omb_roam"

static PairingManagerState_t s_pairing_state = PAIRING_STATE_IDLE;
static uint32_t s_window_end_time_ms = 0;
static uint64_t s_active_nonce = 0;
static uint32_t s_vehicle_vin_hash = 0x0MB96001; // Default vehicle identity hash

// Autorisierte Node-UIDs im Speicher (Indexiert nach UwbNodeType 1..5)
static uint64_t s_authorized_uids[6] = {0};

static void pairing_monitor_task(void *pvParameters) {
    ESP_LOGI(TAG, "SW1 Pairing & Roaming Monitor Task started (GPIO %d)...", PIN_SW1_PAIR_RESET);

    uint32_t press_start_ms = 0;
    bool is_pressed = false;
    bool triggered_3s = false;
    bool triggered_10s = false;

    while (true) {
        int level = gpio_get_level(PIN_SW1_PAIR_RESET);
        uint32_t now = (uint32_t)(esp_timer_get_time() / 1000);

        if (level == 0) { // SW1 gedrückt (Low-aktiv)
            if (!is_pressed) {
                is_pressed = true;
                press_start_ms = now;
                triggered_3s = false;
                triggered_10s = false;
            } else {
                uint32_t hold_time = now - press_start_ms;

                if (hold_time >= 3000 && !triggered_3s) {
                    triggered_3s = true;
                    ESP_LOGW(TAG, "🔘 SW1 held for 3 seconds -> OPENING UWB PAIRING WINDOW (60s)...");
                    pairing_mgr_start_pairing_window(60);
                }

                if (hold_time >= 10000 && !triggered_10s) {
                    triggered_10s = true;
                    ESP_LOGE(TAG, "⚠️ SW1 held for 10 seconds -> EXECUTING FACTORY HARD PURGE OF ALL NVS KEYS!");
                    pairing_mgr_hard_purge_all_keys();
                }
            }
        } else { // SW1 losgelassen
            if (is_pressed) {
                is_pressed = false;
            }
        }

        // Überprüfen, ob das 60s Pairing-Fenster abgelaufen ist
        if (s_pairing_state == PAIRING_STATE_WINDOW_ACTIVE) {
            if (now >= s_window_end_time_ms) {
                s_pairing_state = PAIRING_STATE_IDLE;
                ESP_LOGI(TAG, "Pairing window expired. System returned to IDLE security state.");
            }
        }

        vTaskDelay(pdMS_TO_TICKS(50));
    }
}

static void on_uwb_pairing_confirm_received(const UwbPairingConfirmPkt &pkt, UwbNodeType source) {
    if (s_pairing_state != PAIRING_STATE_WINDOW_ACTIVE) {
        ESP_LOGW(TAG, "Ignored pairing confirm from 0x%02X: Window not active.", (uint8_t)source);
        return;
    }

    if (pkt.pairing_nonce != s_active_nonce) {
        ESP_LOGW(TAG, "Pairing nonce mismatch from 0x%02X! Spoofing attempt rejected.", (uint8_t)source);
        return;
    }

    ESP_LOGI(TAG, "✓ UWB Peer 0x%02X successfully validated nonce and confirmed binding (Slot %d)!",
             (uint8_t)source, pkt.roaming_slot);
}

esp_err_t pairing_roaming_mgr_init(void) {
    ESP_LOGI(TAG, "Initializing SW1 Pairing & Multi-Vehicle Roaming Manager...");

    // GPIO 0 konfigurieren (Pullup, Input)
    gpio_config_t btn_conf = {
        .pin_bit_mask = (1ULL << PIN_SW1_PAIR_RESET),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&btn_conf);

    // Gespeicherte Node UIDs aus dem NVS laden
    nvs_handle_t nvs_h;
    if (nvs_open(NVS_ROAM_NAMESPACE, NVS_READWRITE, &nvs_h) == ESP_OK) {
        size_t len = sizeof(s_authorized_uids);
        if (nvs_get_blob(nvs_h, "auth_uids", s_authorized_uids, &len) == ESP_OK) {
            ESP_LOGI(TAG, "Loaded authorized UWB Node UIDs from NVS.");
        }
        nvs_close(nvs_h);
    }

    // Callbacks im UWB-Backbone verknüpfen
    UwbVehicleBackbone::instance().set_pairing_confirm_callback(on_uwb_pairing_confirm_received);

    // Monitoring-Task starten (Core 0, Prio 12)
    xTaskCreatePinnedToCore(pairing_monitor_task, "PairingMgr", 3072, NULL, 12, NULL, 0);

    return ESP_OK;
}

esp_err_t pairing_mgr_start_pairing_window(uint16_t timeout_sec) {
    s_pairing_state = PAIRING_STATE_WINDOW_ACTIVE;
    uint32_t now = (uint32_t)(esp_timer_get_time() / 1000);
    s_window_end_time_ms = now + (timeout_sec * 1000);

    // Zufällige 64-Bit Nonce generieren
    s_active_nonce = ((uint64_t)esp_random() << 32) | esp_random();

    ESP_LOGW(TAG, "⚡ BROADCASTING UWB PAIRING REQUEST (Nonce: 0x%016llX, VIN: 0x%08lX, Window: %u s)",
             s_active_nonce, s_vehicle_vin_hash, timeout_sec);

    return UwbVehicleBackbone::instance().send_pairing_request(s_active_nonce, s_vehicle_vin_hash, timeout_sec);
}

esp_err_t pairing_mgr_hard_purge_all_keys(void) {
    ESP_LOGW(TAG, "Erasing all stored pairing keys and node UIDs from NVS...");

    memset(s_authorized_uids, 0, sizeof(s_authorized_uids));

    nvs_handle_t nvs_h;
    if (nvs_open(NVS_ROAM_NAMESPACE, NVS_READWRITE, &nvs_h) == ESP_OK) {
        nvs_erase_all(nvs_h);
        nvs_commit(nvs_h);
        nvs_close(nvs_h);
    }

    s_pairing_state = PAIRING_STATE_PURGE_COMPLETE;
    ESP_LOGI(TAG, "✓ Hard-Purge complete: All vehicle bindings returned to unconfigured factory state.");
    return ESP_OK;
}

bool pairing_mgr_is_pairing_active(void) {
    return (s_pairing_state == PAIRING_STATE_WINDOW_ACTIVE);
}

uint16_t pairing_mgr_get_window_remaining_sec(void) {
    if (s_pairing_state != PAIRING_STATE_WINDOW_ACTIVE) return 0;
    uint32_t now = (uint32_t)(esp_timer_get_time() / 1000);
    if (now >= s_window_end_time_ms) return 0;
    return (uint16_t)((s_window_end_time_ms - now) / 1000);
}

bool pairing_mgr_is_node_authorized(UwbNodeType node_type, uint64_t uid) {
    if (node_type > 5) return false;
    // Wenn Slot 0 ist, ist noch kein Hard-Binding hinterlegt -> Trust-on-First-Use während Test/Dev
    if (s_authorized_uids[node_type] == 0) return true;
    return (s_authorized_uids[node_type] == uid);
}

esp_err_t pairing_mgr_store_node_binding(UwbNodeType node_type, uint64_t uid, const uint8_t *session_key) {
    if (node_type > 5) return ESP_ERR_INVALID_ARG;

    s_authorized_uids[node_type] = uid;

    nvs_handle_t nvs_h;
    esp_err_t err = nvs_open(NVS_ROAM_NAMESPACE, NVS_READWRITE, &nvs_h);
    if (err == ESP_OK) {
        nvs_set_blob(nvs_h, "auth_uids", s_authorized_uids, sizeof(s_authorized_uids));
        nvs_commit(nvs_h);
        nvs_close(nvs_h);
        ESP_LOGI(TAG, "Persisted authorized binding for Node 0x%02X (UID: 0x%016llX) to NVS.",
                 (uint8_t)node_type, uid);
    }
    return err;
}
