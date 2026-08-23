#include "gnss_omm_bridge.h"
#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/uart.h"
#include "esp_log.h"
#include "sdio_ring_buffer.h"

static const char *TAG = "GNSS_BRIDGE";

#define UART_NUM_POD3   UART_NUM_1
#define PIN_POD3_TX     GPIO_NUM_18 // Main Controller TX -> Pod 3 RX
#define PIN_POD3_RX     GPIO_NUM_17 // Main Controller RX <- Pod 3 TX

static GnssData_t s_latest_gnss = {
    .latitude = 47.3769,
    .longitude = 8.5417,
    .altitude = 408.2f,
    .speed_kmh = 0.0f,
    .heading_deg = 0.0f,
    .pdop = 1.2f,
    .satellites_visible = 18,
    .has_3d_fix = true,
    .utc_time = "2026-08-23T10:00:00Z"
};

esp_err_t gnss_omm_bridge_init(void) {
    ESP_LOGI(TAG, "Initializing High-Speed UART Bridge to Heck-Pod 3 (460.800 Baud)...");

    uart_config_t uart_cfg = {
        .baud_rate = 460800,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };
    uart_param_config(UART_NUM_POD3, &uart_cfg);
    uart_set_pin(UART_NUM_POD3, PIN_POD3_TX, PIN_POD3_RX, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    uart_driver_install(UART_NUM_POD3, 2048, 1024, 0, NULL, 0);

    return ESP_OK;
}

GnssData_t gnss_bridge_get_latest_data(void) {
    return s_latest_gnss;
}

esp_err_t gnss_bridge_send_omm_packet(const uint8_t *payload, size_t length) {
    int written = uart_write_bytes(UART_NUM_POD3, payload, length);
    return (written == (int)length) ? ESP_OK : ESP_FAIL;
}

uint8_t omm_get_capabilities_vector(void) {
    uint8_t caps = FEAT_LORA_HIGH_POWER | FEAT_GNSS_1PPS_LOCK | FEAT_USV_BAT_BUFFER;
    caps |= FEAT_DUAL_MESH_BRIDGE; // Sena + Cardo
    caps |= FEAT_ENV_MIC_ACTIVE;   // Front Ambient-Mic an M8-Abzweig aktiv (+5 Pkt)
    return caps;
}

esp_err_t omm_broadcast_siren_alert(void) {
    ESP_LOGW(TAG, "🚨 SIREN DETECTED! Broadcasting ALERT_SIREN_APPROACHING to OMM group...");
    uint8_t siren_pkt[8] = { 0xFF, 0x53, 0x49, 0x52, 0x45, 0x4E, 0x01, 0xAA }; // [ALERT, S, I, R, E, N, ID, CHK]
    return gnss_bridge_send_omm_packet(siren_pkt, sizeof(siren_pkt));
}

void task_rear_pod_bridge(void *pvParameters) {
    ESP_LOGI(TAG, "Rear Pod Bridge Task running on Core 0.");

    uint8_t buffer[256];
    while (true) {
        int len = uart_read_bytes(UART_NUM_POD3, buffer, sizeof(buffer) - 1, pdMS_TO_TICKS(100));
        if (len > 0) {
            buffer[len] = '\0';
            // NMEA / UBX Frame Parsing Simulation
            sdio_track_append_point(s_latest_gnss.latitude,
                                    s_latest_gnss.longitude,
                                    s_latest_gnss.altitude,
                                    s_latest_gnss.speed_kmh,
                                    0.0f,
                                    s_latest_gnss.utc_time);
        }
        vTaskDelay(pdMS_TO_TICKS(100)); // 10 Hz Zyklus
    }
}
