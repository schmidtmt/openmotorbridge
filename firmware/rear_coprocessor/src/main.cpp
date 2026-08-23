#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/uart.h"
#include "driver/gpio.h"
#include "driver/spi_master.h"
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

extern "C" void app_main(void) {
    ESP_LOGI(TAG, "Heck-Pod 3 Co-Processor booting (ESP32-C3)...");

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

    // 2. UART zum u-blox MAX-M10S GNSS Modul (9600 initial / 115200 NMEA+UBX)
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

    ESP_LOGI(TAG, "Pod 3 communication interfaces ready. Starting forwarding loop...");

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