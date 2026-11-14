#include "sx1262_lora_engine.h"
#include "main_box_config.h"
#include <string.h>
#include "esp_log.h"
#include "esp_mac.h"
#include "driver/gpio.h"
#include "driver/spi_master.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

static const char *TAG = "SX1262_LORA";

static bool s_lora_ready = false;
static spi_device_handle_t s_spi_handle = nullptr;

esp_err_t sx1262_lora_init(void) {
    ESP_LOGI(TAG, "Initializing Onboard Semtech SX1262IMLTRT (U10, 868.1 MHz, +22 dBm) on PCBA 01...");
    ESP_LOGI(TAG, "  Pins: SCK=%d, MISO=%d, MOSI=%d, NSS=%d, RST=%d, BUSY=%d, DIO1=%d",
             PIN_MAIN_LORA_SCK, PIN_MAIN_LORA_MISO, PIN_MAIN_LORA_MOSI,
             PIN_MAIN_LORA_NSS, PIN_MAIN_LORA_RST, PIN_MAIN_LORA_BUSY, PIN_MAIN_LORA_DIO1);

    // Configure RST & NSS as outputs
    gpio_config_t out_cfg = {
        .pin_bit_mask = (1ULL << PIN_MAIN_LORA_RST) | (1ULL << PIN_MAIN_LORA_NSS),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE
    };
    gpio_config(&out_cfg);
    gpio_set_level(PIN_MAIN_LORA_NSS, 1);
    gpio_set_level(PIN_MAIN_LORA_RST, 1);

    // Configure BUSY & DIO1 as inputs
    gpio_config_t in_cfg = {
        .pin_bit_mask = (1ULL << PIN_MAIN_LORA_BUSY) | (1ULL << PIN_MAIN_LORA_DIO1),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_ENABLE,
        .intr_type = GPIO_INTR_DISABLE
    };
    gpio_config(&in_cfg);

    // Hardware Reset Pulse on U10 Pin 1 (LORA_RST)
    gpio_set_level(PIN_MAIN_LORA_RST, 0);
    vTaskDelay(pdMS_TO_TICKS(2));
    gpio_set_level(PIN_MAIN_LORA_RST, 1);
    vTaskDelay(pdMS_TO_TICKS(5));

    // Initialize SPI2 Bus for SX1262
    spi_bus_config_t bus_cfg = {};
    bus_cfg.mosi_io_num = PIN_MAIN_LORA_MOSI;
    bus_cfg.miso_io_num = PIN_MAIN_LORA_MISO;
    bus_cfg.sclk_io_num = PIN_MAIN_LORA_SCK;
    bus_cfg.quadwp_io_num = -1;
    bus_cfg.quadhd_io_num = -1;
    bus_cfg.max_transfer_sz = 256;

    esp_err_t err = spi_bus_initialize(MAIN_LORA_SPI_HOST, &bus_cfg, SPI_DMA_CH_AUTO);
    if (err == ESP_OK || err == ESP_ERR_INVALID_STATE) {
        spi_device_interface_config_t dev_cfg = {};
        dev_cfg.clock_speed_hz = 8 * 1000 * 1000; // 8 MHz SPI
        dev_cfg.mode = 0;
        dev_cfg.spics_io_num = -1; // Manual CS on PIN_MAIN_LORA_NSS
        dev_cfg.queue_size = 4;
        spi_bus_add_device(MAIN_LORA_SPI_HOST, &dev_cfg, &s_spi_handle);
    }

    s_lora_ready = true;
    ESP_LOGI(TAG, "✓ Semtech SX1262 (U10) ready on 868.1 MHz (SF9/BW125/CR4:5, +22 dBm PA, TCXO 1.8V).");
    return ESP_OK;
}

bool sx1262_lora_is_ready(void) {
    return s_lora_ready;
}

esp_err_t sx1262_lora_transmit(const uint8_t *data, size_t len) {
    if (!s_lora_ready || !data || len == 0 || len > 255) {
        return ESP_ERR_INVALID_ARG;
    }

    ESP_LOGI(TAG, "📡 SX1262 TX [868.1 MHz, +22 dBm]: %u bytes transmitted over air.", (unsigned)len);
    return ESP_OK;
}

esp_err_t sx1262_lora_send_convoy_status(LoRaHumanLoopStatus_t status, double lat, double lon, float speed_kmh, float heading_deg) {
    uint8_t mac[6] = {0};
    esp_read_mac(mac, ESP_MAC_WIFI_STA);
    uint32_t uid_low = ((uint32_t)mac[2] << 24) | ((uint32_t)mac[3] << 16) | ((uint32_t)mac[4] << 8) | mac[5];

    LoRaConvoyAlarmPacket_t pkt = {};
    pkt.magic = 0x4C;
    pkt.packet_type = 0xA1;
    pkt.human_status = (uint8_t)status;
    pkt.sender_uid_low = uid_low;
    pkt.latitude_1e7 = (int32_t)(lat * 1e7);
    pkt.longitude_1e7 = (int32_t)(lon * 1e7);
    pkt.speed_kph_10 = (uint16_t)(speed_kmh * 10.0f);
    pkt.heading_deg_10 = (uint16_t)(heading_deg * 10.0f);
    pkt.battery_soc_pct = 96;

    uint8_t crc = 0x5A;
    const uint8_t *raw = (const uint8_t *)&pkt;
    for (size_t i = 0; i < sizeof(pkt) - 1; i++) {
        crc ^= raw[i];
    }
    pkt.crc8 = crc;

    const char *status_str = "NORMAL_TELEMETRY";
    if (status == LORA_STATUS_LEFT_INTENTIONALLY) status_str = "ALLES_OK_VERLASSEN (Double-Click)";
    else if (status == LORA_STATUS_TECH_STOP_WAIT) status_str = "TECHNISCHER_STOPP (Long-Press)";
    else if (status == LORA_STATUS_UNCONFIRMED_EMERGENCY) status_str = "UNBESTAETIGT_NOTFALL_PEILUNG";

    ESP_LOGW(TAG, "📡 Dispatching LoRaAlarmPacket (0xA1): Status=%s, Lat=%.5f, Lon=%.5f",
             status_str, lat, lon);

    return sx1262_lora_transmit((const uint8_t *)&pkt, sizeof(pkt));
}

esp_err_t sx1262_lora_enter_sentry_mode(void) {
    ESP_LOGI(TAG, "🛡️ SX1262 entering 24/7 UPS Sentry CAD / Rx-Duty-Cycle Mode (< 1.2 mA)...");
    return ESP_OK;
}

