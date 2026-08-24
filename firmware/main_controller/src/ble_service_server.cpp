#include "ble_service_server.h"
#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "nimble/nimble_port.h"
#include "nimble/nimble_port_freertos.h"
#include "host/ble_hs.h"
#include "services/gap/ble_svc_gap.h"
#include "services/gatt/ble_svc_gatt.h"
#include "audio_dsp_pipeline.h"
#include "opto_pulse_sequencer.h"
#include "cartridge_onewire.h"
#include "omm_flasher.h"

static const char *TAG = "BLE_SERVER";

// GATT Service & Characteristic UUIDs
// Main Service: 23d113ef-5f78-2315-deef-121200a00000
static const ble_uuid128_t gatt_svr_svc_omb_uuid =
    BLE_UUID128_INIT(0x00, 0x00, 0xA0, 0x00, 0x12, 0x12, 0xEF, 0xDE, 0x15, 0x23, 0x78, 0x5F, 0xEF, 0x13, 0xD1, 0x23);

// Telemetry Characteristic: 23d113ef-5f78-2315-deef-121200a00001
static const ble_uuid128_t gatt_svr_chr_telemetry_uuid =
    BLE_UUID128_INIT(0x01, 0x00, 0xA0, 0x00, 0x12, 0x12, 0xEF, 0xDE, 0x15, 0x23, 0x78, 0x5F, 0xEF, 0x13, 0xD1, 0x23);

// Control Characteristic: 23d113ef-5f78-2315-deef-121200a00002
static const ble_uuid128_t gatt_svr_chr_control_uuid =
    BLE_UUID128_INIT(0x02, 0x00, 0xA0, 0x00, 0x12, 0x12, 0xEF, 0xDE, 0x15, 0x23, 0x78, 0x5F, 0xEF, 0x13, 0xD1, 0x23);

static uint16_t telemetry_val_handle = 0;
static uint16_t conn_handle_pwa = BLE_HS_CONN_HANDLE_NONE;

static int gatt_svr_chr_access_omb(uint16_t conn_handle, uint16_t attr_handle,
                                   struct ble_gatt_access_ctxt *ctxt, void *arg) {
    if (ctxt->op == BLE_GATT_ACCESS_OP_WRITE_CHR) {
        uint8_t cmd[4] = {0};
        uint16_t len = OS_MBUF_PKTLEN(ctxt->om);
        if (len > sizeof(cmd)) len = sizeof(cmd);
        os_mbuf_copydata(ctxt->om, 0, len, cmd);

        ESP_LOGI(TAG, "GATT Control Command received: 0x%02X 0x%02X", cmd[0], cmd[1]);
        if (cmd[0] == 0x01) { // Change Audio Mode
            audio_set_operation_mode((AudioOperationMode)cmd[1]);
        } else if (cmd[0] == 0x02) { // Trigger Port 1 Mesh Toggle
            opto_port1_toggle_mesh();
        } else if (cmd[0] == 0x03) { // Trigger Port 1 Channel Next
            opto_port1_channel_next();
        } else if (cmd[0] == 0x04) { // Trigger Port 2 Channel Next
            opto_port2_channel_next();
        } else if (cmd[0] == 0x05) { // Trigger OEM Auto-Pairing (5s Opto Hold)
            opto_port_pairing_mode(cmd[1]);
        } else if (cmd[0] == 0x06) { // Trigger OMM High-Speed UART Push
            omm_flasher_push_from_storage("/spiffs/omm_rear.bin");
        } else if (cmd[0] == 0x07) { // Trigger Profile Merge & Hot-Reload
            cartridge_apply_profile_merge(cmd[1], "sena_apex", 0.0f);
        }
        return 0;
    }
    return 0;
}

static const struct ble_gatt_svc_def gatt_svr_svcs[] = {
    {
        .type = BLE_GATT_SVC_TYPE_PRIMARY,
        .uuid = &gatt_svr_svc_omb_uuid.u,
        .characteristics = (struct ble_gatt_chr_def[]) {
            {
                .uuid = &gatt_svr_chr_telemetry_uuid.u,
                .access_cb = gatt_svr_chr_access_omb,
                .flags = BLE_GATT_CHR_F_READ | BLE_GATT_CHR_F_NOTIFY,
                .val_handle = &telemetry_val_handle,
            },
            {
                .uuid = &gatt_svr_chr_control_uuid.u,
                .access_cb = gatt_svr_chr_access_omb,
                .flags = BLE_GATT_CHR_F_WRITE,
            },
            { 0 }
        },
    },
    { 0 }
};

static int ble_gap_event(struct ble_gap_event *event, void *arg) {
    switch (event->type) {
        case BLE_GAP_EVENT_CONNECT:
            if (event->connect.status == 0) {
                conn_handle_pwa = event->connect.conn_handle;
                ESP_LOGI(TAG, "PWA Client connected (conn_handle=%d)", conn_handle_pwa);
            }
            break;

        case BLE_GAP_EVENT_DISCONNECT:
            ESP_LOGI(TAG, "PWA Client disconnected.");
            conn_handle_pwa = BLE_HS_CONN_HANDLE_NONE;
            break;

        default:
            break;
    }
    return 0;
}

esp_err_t ble_server_init(void) {
    ESP_LOGI(TAG, "Initializing NimBLE GATT Server for WebBLE PWA...");

    nimble_port_init();
    ble_svc_gap_init();
    ble_svc_gatt_init();

    ble_svc_gap_device_name_set("OpenMotorBridge-v8");
    ble_gatts_count_cfg(gatt_svr_svcs);
    ble_gatts_add_svcs(gatt_svr_svcs);

    return ESP_OK;
}

void ble_server_notify_telemetry(const SystemTelemetry_t *telemetry) {
    if (conn_handle_pwa != BLE_HS_CONN_HANDLE_NONE && telemetry_val_handle != 0) {
        struct os_mbuf *om = ble_hs_mbuf_from_flat(telemetry, sizeof(SystemTelemetry_t));
        if (om) {
            ble_gatts_notify_custom(conn_handle_pwa, telemetry_val_handle, om);
        }
    }
}

static void ble_host_task(void *param) {
    ESP_LOGI(TAG, "NimBLE Host Task running on Core 0.");
    nimble_port_run();
    nimble_port_freertos_deinit();
}

void task_ble_services(void *pvParameters) {
    nimble_port_freertos_init(ble_host_task);

    struct ble_gap_adv_params adv_params = {};
    adv_params.conn_mode = BLE_GAP_CONN_MODE_UND;
    adv_params.disc_mode = BLE_GAP_DISC_MODE_GEN;
    ble_gap_adv_start(BLE_OWN_ADDR_PUBLIC, NULL, BLE_HS_FOREVER, &adv_params, ble_gap_event, NULL);

    while (true) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}