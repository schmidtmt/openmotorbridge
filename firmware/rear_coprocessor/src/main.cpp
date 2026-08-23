#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/uart.h"
#include "driver/gpio.h"
#include "driver/spi_master.h"
#include "esp_timer.h"
#include "esp_log.h"

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

static void init_lora_sx1262(void) {
    ESP_LOGI(TAG, "Initializing Semtech SX1262 LoRa SPI Driver (+22 dBm PA @ 868 MHz)...");

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

    ESP_LOGI(TAG, "SX1262 LoRa Hardware ready for OpenMotorMesh Superframe.");
}

extern "C" void app_main(void) {
    ESP_LOGI(TAG, "==================================================");
    ESP_LOGI(TAG, "   Heck-Pod 3 Co-Processor (ESP32-C3 RISC-V)      ");
    ESP_LOGI(TAG, "==================================================");

    // 1. UART zur Zentralbox initialisieren (460.800 Baud High-Speed)
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
    uart_driver_install(UART_NUM_BRIDGE, 1024, 0, 0, NULL, 0);

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

    // 3. 1-PPS & SX1262 LoRa SPI initialisieren
    init_pps_interrupt();
    init_lora_sx1262();

    ESP_LOGI(TAG, "Pod 3 communication interfaces fully operational. Starting loop...");

    uint8_t rx_buf[256];
    while (true) {
        // GNSS-Daten lesen und vorkomprimiert an die Zentralbox streamen
        int len = uart_read_bytes(UART_NUM_GNSS, rx_buf, sizeof(rx_buf), pdMS_TO_TICKS(10));
        if (len > 0) {
            uart_write_bytes(UART_NUM_BRIDGE, (const char *)rx_buf, len);
        }
        vTaskDelay(pdMS_TO_TICKS(5));
    }
}