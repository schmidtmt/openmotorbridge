#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "nimble/nimble_port.h"
#include "nimble/nimble_port_freertos.h"
#include "host/ble_hs.h"
#include "services/gap/ble_svc_gap.h"
#include "services/gatt/ble_svc_gatt.h"

static const char *TAG = "BLE_SERVER";

// GATT Service UUIDs
static const ble_uuid128_t gatt_svr_svc_omb_uuid =
    BLE_UUID128_INIT(0x23, 0xD1, 0x13, 0xEF, 0x5F, 0x78, 0x23, 0x15, 0xDE, 0xEF, 0x12, 0x12, 0x00, 0xA0, 0x00, 0x00);

void task_ble_services(void *pvParameters) {
    ESP_LOGI(TAG, "BLE NimBLE Stack starting on Core 0...");

    // NimBLE Host & GAP/GATT Server Konfiguration
    // Bereitstellung von Echtzeit-Telemetrie & Steuerung für die WebBLE PWA

    while (true) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}