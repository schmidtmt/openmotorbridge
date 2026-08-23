#include "ble_handlebar_client.h"
#include <stdio.h>
#include <string.h>
#include "esp_log.h"
#include "host/ble_hs.h"

static const char *TAG = "BLE_REMOTE";

static handlebar_button_cb_t s_btn_callback = NULL;
static handlebar_battery_cb_t s_bat_callback = NULL;
static uint8_t s_last_battery_pct = 95; // Initialer CR2032 Wert
static bool s_is_connected = false;

esp_err_t ble_handlebar_client_init(handlebar_button_cb_t btn_cb, handlebar_battery_cb_t bat_cb) {
    ESP_LOGI(TAG, "Initializing BLE Handlebar Remote Client (Battery SIG 0x180F)...");
    s_btn_callback = btn_cb;
    s_bat_callback = bat_cb;
    s_is_connected = true; // Auto-Paired / Connected Simulation
    return ESP_OK;
}

uint8_t ble_handlebar_get_battery_level(void) {
    return s_last_battery_pct;
}

bool ble_handlebar_is_connected(void) {
    return s_is_connected;
}

// Simulierte Event-Verarbeitung für Shutter / PTT
void ble_handlebar_inject_button_event(uint8_t button_id, bool long_press) {
    if (s_btn_callback) {
        s_btn_callback(button_id, long_press);
    }
}
