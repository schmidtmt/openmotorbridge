#include "can_bus_manager.h"
#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/twai.h"
#include "esp_log.h"
#include "adr_ekf_filter.h"

static const char *TAG = "CAN_MGR";

// GPIO Pin-Definitionen für TI TCAN334G Transceiver (v8.0 Pinout)
#define PIN_CAN_TX          GPIO_NUM_19
#define PIN_CAN_RX          GPIO_NUM_20

static bool s_can_initialized = false;
static bool s_can_traffic_active = false;
static float s_last_vehicle_speed_kmh = 0.0f;
static uint32_t s_rx_msg_count = 0;

esp_err_t can_bus_manager_init(void) {
    ESP_LOGI(TAG, "Initializing TI TCAN334G TWAI (CAN 2.0B) Interface on TX: GPIO %d, RX: GPIO %d...",
             PIN_CAN_TX, PIN_CAN_RX);

    // 1. TWAI Konfiguration: 500 kbps (Motorrad-Standard z.B. BMW / Harley-Davidson / Ducati)
    twai_general_config_t g_config = TWAI_GENERAL_CONFIG_DEFAULT(
        (gpio_num_t)PIN_CAN_TX,
        (gpio_num_t)PIN_CAN_RX,
        TWAI_MODE_NORMAL // Normal mode for listening & sending display popups
    );
    g_config.rx_queue_len = 32;
    g_config.tx_queue_len = 8;

    twai_timing_config_t t_config = TWAI_TIMING_CONFIG_500KBITS();
    twai_filter_config_t f_config = TWAI_FILTER_CONFIG_ACCEPT_ALL();

    // 2. Treiber installieren & starten
    esp_err_t ret = twai_driver_install(&g_config, &t_config, &f_config);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to install TWAI driver: %s", esp_err_to_name(ret));
        return ret;
    }

    ret = twai_start();
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to start TWAI driver: %s", esp_err_to_name(ret));
        return ret;
    }

    s_can_initialized = true;
    ESP_LOGI(TAG, "TWAI (CAN-Bus) Driver running at 500 kbps.");
    return ESP_OK;
}

void task_can_bus_manager(void *pvParameters) {
    ESP_LOGI(TAG, "CAN-Bus Manager Task running on Core 0.");

    twai_message_t rx_msg;

    while (true) {
        if (!s_can_initialized) {
            vTaskDelay(pdMS_TO_TICKS(1000));
            continue;
        }

        // 1. CAN-Frame mit 100 ms Timeout empfangen
        esp_err_t ret = twai_receive(&rx_msg, pdMS_TO_TICKS(100));
        if (ret == ESP_OK) {
            s_can_traffic_active = true;
            s_rx_msg_count++;

            // 2. Dekodierung bekannter Motorrad-CAN-Frames
            // A. Standard SAE J1939 Wheel Speed / CCVS (PGN 0xFEF1 / ID 0x18FEF100)
            if ((rx_msg.identifier & 0x00FFFF00) == 0x00FEF100 && rx_msg.data_length_code >= 3) {
                // Bytes 1 & 2: 1/256 km/h pro Bit
                uint16_t raw_speed = (uint16_t)rx_msg.data[1] | ((uint16_t)rx_msg.data[2] << 8);
                float speed_kmh = (float)raw_speed / 256.0f;
                s_last_vehicle_speed_kmh = speed_kmh;
                adr_ekf_update_can_speed(speed_kmh);
            }
            // B. BMW Motorrad K2x/K5x Wheel Speed (ID 0x130 / 0x2A8)
            else if (rx_msg.identifier == 0x130 && rx_msg.data_length_code >= 6) {
                uint16_t raw_rear_speed = (uint16_t)rx_msg.data[4] | ((uint16_t)(rx_msg.data[5] & 0x0F) << 8);
                float speed_kmh = (float)raw_rear_speed * 0.1f;
                s_last_vehicle_speed_kmh = speed_kmh;
                adr_ekf_update_can_speed(speed_kmh);
            }
            // C. Harley-Davidson HD-LAN / Skyline OS Speed Frame (ID 0x280)
            else if (rx_msg.identifier == 0x280 && rx_msg.data_length_code >= 4) {
                uint16_t raw_speed = (uint16_t)rx_msg.data[2] | ((uint16_t)rx_msg.data[3] << 8);
                float speed_kmh = (float)raw_speed * 0.0625f; // 1/16 km/h resolution
                s_last_vehicle_speed_kmh = speed_kmh;
                adr_ekf_update_can_speed(speed_kmh);
            }
        } else if (ret == ESP_ERR_TIMEOUT) {
            // Kein Frame im Intervall empfangen
            if (s_rx_msg_count == 0) {
                s_can_traffic_active = false;
            }
        }
    }
}

void can_bus_send_remote_battery_warning(uint8_t battery_pct) {
    if (!s_can_initialized) return;

    // Sende standardisierten OMB Alert-Frame (ID 0x5F0) an Motorrad-Display
    twai_message_t tx_msg = {};
    tx_msg.identifier = 0x5F0;
    tx_msg.extd = 0;
    tx_msg.data_length_code = 4;
    tx_msg.data[0] = 0x01; // Alert Type: Remote Battery Low
    tx_msg.data[1] = battery_pct; // Battery Level %
    tx_msg.data[2] = 0x00; // Reserved
    tx_msg.data[3] = 0xAA; // Checksum / Magic

    esp_err_t ret = twai_transmit(&tx_msg, pdMS_TO_TICKS(50));
    if (ret == ESP_OK) {
        ESP_LOGI(TAG, "Transmitted Handlebar Remote Low-Battery Warning (%d%%) to CAN-Bus.", battery_pct);
    } else {
        ESP_LOGW(TAG, "Failed to transmit CAN alert frame: %s", esp_err_to_name(ret));
    }
}

bool can_bus_is_connected(void) {
    return s_can_traffic_active;
}

float can_bus_get_vehicle_speed_kmh(void) {
    return s_last_vehicle_speed_kmh;
}
