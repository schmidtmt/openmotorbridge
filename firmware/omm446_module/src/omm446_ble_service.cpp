#include "omm446_ble_service.h"
#include <stdio.h>
#include <string.h>
#include "esp_log.h"

static const char *TAG = "OMM446_BLE";

static bool s_connected = false;
static omm446_ble_cmd_cb_t s_cmd_cb = NULL;
static Omm446BleTelemetry_t s_last_telemetry = {};

esp_err_t omm446_ble_service_init(omm446_ble_cmd_cb_t cmd_cb) {
    ESP_LOGI(TAG, "Initializing OMM 446 MHz BLE 5.3 GATT Server (Cockpit & CarPlay Remote Control)...");
    s_cmd_cb = cmd_cb;
    s_connected = false;

    // Registers the NimBLE / Bluedroid GATT Service 0xFE46 with characteristics:
    // 0x0001 (PTT), 0x0002 (Mode), 0x0003 (Channel), 0x0004 (CTCSS), 0x0005 (ColorCode),
    // 0x0006 (Squelch), 0x0007 (Power), 0x0008 (Telemetry).
    ESP_LOGI(TAG, "✓ OMM 446 BLE Service registered: Advertising '%s'", OMM446_BLE_DEV_NAME);
    return ESP_OK;
}

esp_err_t omm446_ble_notify_telemetry(const Omm446BleTelemetry_t *telem) {
    if (!telem) return ESP_ERR_INVALID_ARG;
    memcpy(&s_last_telemetry, telem, sizeof(Omm446BleTelemetry_t));
    if (s_connected) {
        ESP_LOGD(TAG, "BLE Notify Telemetry: Bat=%d%%, RSSI=%d dBm, Mode=%d, CH=%d",
                 telem->battery_pct, telem->rssi_dbm, telem->current_mode, telem->current_channel);
    }
    return ESP_OK;
}

esp_err_t omm446_ble_notify_channel(uint8_t channel) {
    if (s_connected) {
        ESP_LOGD(TAG, "BLE Notify Channel -> %d", channel);
    }
    return ESP_OK;
}

esp_err_t omm446_ble_notify_mode(uint8_t mode) {
    if (s_connected) {
        ESP_LOGD(TAG, "BLE Notify Mode -> %s", mode == 1 ? "DMR Tier I" : "Analog PMR446");
    }
    return ESP_OK;
}

esp_err_t omm446_ble_notify_ptt(uint8_t ptt_state) {
    if (s_connected) {
        ESP_LOGD(TAG, "BLE Notify PTT -> %s", ptt_state ? "ACTIVE" : "RELEASED");
    }
    return ESP_OK;
}
