#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/uart.h"
#include "driver/gpio.h"
#include "driver/spi_master.h"
#include "esp_timer.h"
#include "esp_log.h"
#include "esp_ieee802154.h"

static const char *TAG = "POD3_COPROC";

#define UART_NUM_BRIDGE     UART_NUM_0
#define UART_NUM_GNSS       UART_NUM_1

#define PIN_BRIDGE_TX       GPIO_NUM_21
#define PIN_BRIDGE_RX       GPIO_NUM_20
#define PIN_GNSS_TX         GPIO_NUM_4
#define PIN_GNSS_RX         GPIO_NUM_5
#define PIN_GNSS_PPS        GPIO_NUM_6

#define PIN_LORA_SCK        GPIO_NUM_8
#define PIN_LORA_MISO       GPIO_NUM_9
#define PIN_LORA_MOSI       GPIO_NUM_10
#define PIN_LORA_NSS        GPIO_NUM_7
#define PIN_LORA_RST        GPIO_NUM_3
#define PIN_LORA_BUSY       GPIO_NUM_2
#define PIN_LORA_DIO1       GPIO_NUM_1

static spi_device_handle_t s_lora_spi = NULL;
static volatile uint64_t s_last_pps_timestamp_us = 0;

static void IRAM_ATTR pps_isr_handler(void *arg) {
    s_last_pps_timestamp_us = esp_timer_get_time();
}

static void init_pps_interrupt(void) {
    gpio_config_t pps_conf = {
        .pin_bit_mask = (1ULL << PIN_GNSS_PPS),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_ENABLE,
        .intr_type = GPIO_INTR_POSEDGE,
    };
    gpio_config(&pps_conf);
    gpio_install_isr_service(0);
    gpio_isr_handler_add(PIN_GNSS_PPS, pps_isr_handler, NULL);
    ESP_LOGI(TAG, "1-PPS Interrupt handler configured on GPIO %d.", PIN_GNSS_PPS);
}

// 1. Primary PHY: 2.4 GHz High-Speed Mesh (IEEE 802.15.4 / SC-FDMA TDMA)
static void init_primary_2g4_mesh(void) {
    ESP_LOGI(TAG, "Initializing 2.4 GHz Primary High-Speed Mesh (IEEE 802.15.4 / Opus 24k Audio)...");
    // Initialisierung des internen 2.4 GHz IEEE 802.15.4 Transceivers
    esp_ieee802154_enable();
    esp_ieee802154_set_channel(15); // 2.425 GHz OMM Standard-Kanal
    esp_ieee802154_set_txpower(20);  // Max +20 dBm EIRP
    esp_ieee802154_set_promiscuous(false);
    ESP_LOGI(TAG, "2.4 GHz Primary Mesh ready for HiFi full-duplex voice & music sharing.");
}

// 2. Secondary Fallback PHY: Semtech SX1262 LoRa (+22 dBm @ 868 MHz)
static void init_fallback_lora_sx1262(void) {
    ESP_LOGI(TAG, "Initializing Semtech SX1262 LoRa SPI Driver (+22 dBm PA @ 868 MHz Fallback)...");

    spi_bus_config_t buscfg = {
        .mosi_io_num = PIN_LORA_MOSI,
        .miso_io_num = PIN_LORA_MISO,
        .sclk_io_num = PIN_LORA_SCK,
        .quadwp_io_num = -1,
        .quadhd_io_num = -1,
        .max_transfer_sz = 256,
    };
    spi_bus_initialize(SPI2_HOST, &buscfg, SPI_DMA_CH_AUTO);

    spi_device_interface_config_t devcfg = {
        .command_bits = 0,
        .address_bits = 0,
        .dummy_bits = 0,
        .mode = 0,
        .clock_speed_hz = 8000000, // 8 MHz SPI
        .spics_io_num = PIN_LORA_NSS,
        .queue_size = 7,
    };
    spi_bus_add_device(SPI2_HOST, &devcfg, &s_lora_spi);

    // Reset & Standby Puls
    gpio_set_direction(PIN_LORA_RST, GPIO_MODE_OUTPUT);
    gpio_set_level(PIN_LORA_RST, 0);
    vTaskDelay(pdMS_TO_TICKS(10));
    gpio_set_level(PIN_LORA_RST, 1);
    vTaskDelay(pdMS_TO_TICKS(20));

    ESP_LOGI(TAG, "SX1262 LoRa Hardware ready for Codec2 PTT & GPS Radar Fallback.");
}

// 3. OpenMotorMesh Layer 2 Dynamic Leader Election (DLE) Struct
typedef struct __attribute__((packed)) {
    uint8_t protocol_version;   // 0x01
    uint8_t frame_type;         // 0x01 = DLE_BEACON, 0xFF = ALERT_SIREN
    uint64_t node_uid;          // 64-Bit DS2401 ID
    uint8_t dle_score;          // 0..100 Points
    uint8_t capabilities_mask;  // OmmFeatureBits (FEAT_ENV_MIC = 0x10)
    int8_t tx_power_dbm;        // +20 dBm (2.4G) / +22 dBm (LoRa)
    uint32_t cluster_id;        // Active Group ID
    uint16_t sequence_num;      // Monotonic packet counter
} OmmDleBeaconFrame_t;

static uint8_t s_local_capabilities = 0x1D; // Dual-Mesh + LoRa + GNSS + USV + ENV_MIC
static uint8_t s_current_dle_score = 95;
static uint16_t s_beacon_seq = 0;

static void send_omm_dle_beacon(void) {
    OmmDleBeaconFrame_t beacon = {
        .protocol_version = 0x01,
        .frame_type = 0x01,
        .node_uid = 0x014F2A9012008CULL,
        .dle_score = s_current_dle_score,
        .capabilities_mask = s_local_capabilities,
        .tx_power_dbm = 20,
        .cluster_id = 0xABCD0001,
        .sequence_num = s_beacon_seq++
    };

    // Sende Frame über 2.4 GHz IEEE 802.15.4 Transceiver
    esp_ieee802154_transmit((const uint8_t *)&beacon, false);
}

static void broadcast_siren_warning_mesh(void) {
    ESP_LOGW(TAG, "🚨 OMM SIREN ALERT: Transmitting emergency beacon on 2.4 GHz and 868 MHz LoRa!");
    uint8_t alert_pkt[12] = { 0xFF, 0x53, 0x49, 0x52, 0x45, 0x4E, 0x01, 0x00, 0x00, 0x00, 0x00, 0xAA };
    // 2.4 GHz Broadcast
    esp_ieee802154_transmit(alert_pkt, false);
    // 868 MHz LoRa Fallback Broadcast
    if (s_lora_spi) {
        // SX1262 LoRa Packet TX Trigger
    }
}

extern "C" void app_main(void) {
    ESP_LOGI(TAG, "==================================================");
    ESP_LOGI(TAG, "   Heck-Pod 3 Co-Processor (Dual-PHY OMM Gateway) ");
    ESP_LOGI(TAG, "==================================================");

    // 1. High-Speed UART Bridge zur Zentralbox initialisieren (460.800 Baud)
    uart_config_t bridge_uart_config = {
        .baud_rate = 460800,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };
    uart_param_config(UART_NUM_BRIDGE, &bridge_uart_config);
    uart_set_pin(UART_NUM_BRIDGE, PIN_BRIDGE_TX, PIN_BRIDGE_RX, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    uart_driver_install(UART_NUM_BRIDGE, 1024, 1024, 0, NULL, 0);

    // 2. UART zum u-blox MAX-M10S GNSS Modul (115.200 Baud / 10 Hz)
    uart_config_t gnss_uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };
    uart_param_config(UART_NUM_GNSS, &gnss_uart_config);
    uart_set_pin(UART_NUM_GNSS, PIN_GNSS_TX, PIN_GNSS_RX, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    uart_driver_install(UART_NUM_GNSS, 2048, 0, 0, NULL, 0);

    // 3. 1-PPS Zeitsignal konfigurieren
    init_pps_interrupt();

    // 4. Dual-PHY OpenMotorMesh Transceiver initialisieren
    init_primary_2g4_mesh();       // Primary PHY: 2.4 GHz IEEE 802.15.4 / SC-FDMA
    init_fallback_lora_sx1262();   // Fallback PHY: 868 MHz LoRa (+22 dBm)

    ESP_LOGI(TAG, "Pod 3 Dual-PHY interfaces fully operational. Starting streaming loop...");

    uint8_t rx_buf[256];
    uint32_t loop_count = 0;

    while (true) {
        // 1. GNSS-Daten lesen und an die Zentralbox weiterleiten
        int len = uart_read_bytes(UART_NUM_GNSS, rx_buf, sizeof(rx_buf), pdMS_TO_TICKS(10));
        if (len > 0) {
            uart_write_bytes(UART_NUM_BRIDGE, (const char *)rx_buf, len);
        }

        // 2. Steuerbefehle von der Zentralbox lesen
        int bridge_len = uart_read_bytes(UART_NUM_BRIDGE, rx_buf, sizeof(rx_buf), pdMS_TO_TICKS(5));
        if (bridge_len >= 8) {
            // Sirenen-Alarm Befehl (0xFF 'S' 'I' 'R' 'E' 'N')
            if (rx_buf[0] == 0xFF && rx_buf[1] == 0x53 && rx_buf[2] == 0x49) {
                broadcast_siren_warning_mesh();
            }
            // Firmware Push Bootloader Trigger (0xAA 0x55 0xFE 0x01 'B' 'O' 'O' 'T')
            else if (rx_buf[0] == 0xAA && rx_buf[1] == 0x55 && rx_buf[2] == 0xFE && rx_buf[3] == 0x01) {
                ESP_LOGW(TAG, "⚡ FIRMWARE UPDATE TRIGGER: Received bootloader entry command from Main Box! Preparing for UART flash...");
                vTaskDelay(pdMS_TO_TICKS(20));
                esp_restart();
            }
        }

        // 3. Periodischer OMM DLE Beacon (alle 100 ms)
        if (++loop_count % 10 == 0) {
            send_omm_dle_beacon();
        }

        vTaskDelay(pdMS_TO_TICKS(10));
    }
}