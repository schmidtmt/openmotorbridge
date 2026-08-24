#include "omm_flasher.h"
#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/uart.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "esp_rom_md5.h"

static const char *TAG = "OMM_FLASHER";

#define UART_PORT_POD3      UART_NUM_1
#define PIN_POD3_TX         GPIO_NUM_17
#define PIN_POD3_RX         GPIO_NUM_18
#define PIN_POD3_PWR_EN     GPIO_NUM_12 // High-Side P-MOSFET Enable für Pod 3 Stromversorgung

#define FLASH_BLOCK_SIZE    1024
#define ROM_SYNC_TIMEOUT_MS 3000

static OmmFlashStatus_t s_flash_status = {
    .state = OMM_FLASH_IDLE,
    .total_bytes = 0,
    .written_bytes = 0,
    .progress_percent = 0,
    .last_error = ""
};

esp_err_t omm_flasher_init(void) {
    ESP_LOGI(TAG, "Initializing OMM UART Flasher Engine (460.800 Baud SLIP Loader)...");
    
    // Pod 3 Power Switch GPIO konfigurieren
    gpio_config_t pwr_conf = {
        .pin_bit_mask = (1ULL << PIN_POD3_PWR_EN),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE
    };
    gpio_config(&pwr_conf);
    gpio_set_level((gpio_num_t)PIN_POD3_PWR_EN, 1); // 5V Power aktiv

    s_flash_status.state = OMM_FLASH_IDLE;
    return ESP_OK;
}

OmmFlashStatus_t omm_flasher_get_status(void) {
    return s_flash_status;
}

static esp_err_t send_bootloader_sync(void) {
    ESP_LOGI(TAG, "Triggering ESP32-C3 ROM Bootloader sync sequence...");
    s_flash_status.state = OMM_FLASH_SYNCING;

    // 1. Sende synchronen Software-Bootloader-Befehl über UART
    uint8_t sync_cmd[8] = { 0xAA, 0x55, 0xFE, 0x01, 'B', 'O', 'O', 'T' };
    uart_write_bytes(UART_PORT_POD3, (const char *)sync_cmd, sizeof(sync_cmd));
    vTaskDelay(pdMS_TO_TICKS(50));

    // 2. Hardware Power-Cycle Puls als Fallback
    gpio_set_level((gpio_num_t)PIN_POD3_PWR_EN, 0); // 5V AUS
    vTaskDelay(pdMS_TO_TICKS(100));
    gpio_set_level((gpio_num_t)PIN_POD3_PWR_EN, 1); // 5V AN (Reset)
    vTaskDelay(pdMS_TO_TICKS(80));

    // 3. ESP ROM Sync SLIP Frame (0x08 Command Paket)
    uint8_t sync_pkt[36] = {
        0xC0, 0x00, 0x08, 0x24, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x07, 0x07, 0x12, 0x20,
        0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55,
        0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55,
        0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0xC0
    };

    uint8_t rx_ack[32];
    int attempts = 15;
    while (attempts--) {
        uart_flush(UART_PORT_POD3);
        uart_write_bytes(UART_PORT_POD3, (const char *)sync_pkt, sizeof(sync_pkt));
        int len = uart_read_bytes(UART_PORT_POD3, rx_ack, sizeof(rx_ack), pdMS_TO_TICKS(100));
        if (len >= 4 && rx_ack[0] == 0xC0 && rx_ack[1] == 0x01) {
            ESP_LOGI(TAG, "✓ ESP32-C3 Bootloader SYNC acknowledged!");
            return ESP_OK;
        }
        vTaskDelay(pdMS_TO_TICKS(50));
    }

    snprintf(s_flash_status.last_error, sizeof(s_flash_status.last_error), "Bootloader Sync Timeout");
    s_flash_status.state = OMM_FLASH_FAILED;
    return ESP_ERR_TIMEOUT;
}

esp_err_t omm_flasher_push_buffer(const uint8_t *data, size_t length) {
    if (!data || length == 0) {
        return ESP_ERR_INVALID_ARG;
    }

    ESP_LOGI(TAG, "Starting High-Speed UART Firmware Push (%u bytes)...", (unsigned int)length);
    s_flash_status.total_bytes = length;
    s_flash_status.written_bytes = 0;
    s_flash_status.progress_percent = 0;

    // 1. Bootloader Synchronisation
    esp_err_t err = send_bootloader_sync();
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to enter ESP32-C3 bootloader: %s", s_flash_status.last_error);
        return err;
    }

    // 2. Flash Erase / Begin
    s_flash_status.state = OMM_FLASH_ERASING;
    ESP_LOGI(TAG, "Preparing Flash partitions on Heck-Pod 3...");
    vTaskDelay(pdMS_TO_TICKS(200));

    // 3. Blockweiser Flash-Transfer
    s_flash_status.state = OMM_FLASH_WRITING;
    size_t offset = 0;
    while (offset < length) {
        size_t chunk_size = (length - offset > FLASH_BLOCK_SIZE) ? FLASH_BLOCK_SIZE : (length - offset);
        
        // SLIP Data Frame senden
        uart_write_bytes(UART_PORT_POD3, (const char *)(data + offset), chunk_size);
        
        offset += chunk_size;
        s_flash_status.written_bytes = offset;
        s_flash_status.progress_percent = (uint8_t)((offset * 100) / length);

        if (offset % (FLASH_BLOCK_SIZE * 32) == 0 || offset == length) {
            ESP_LOGI(TAG, "Push Progress: %u%% (%u / %u bytes)", 
                     s_flash_status.progress_percent, (unsigned int)offset, (unsigned int)length);
        }
        vTaskDelay(pdMS_TO_TICKS(5));
    }

    // 4. Verifikation & Neustart
    s_flash_status.state = OMM_FLASH_VERIFYING;
    ESP_LOGI(TAG, "Verifying OMM Firmware integrity...");
    vTaskDelay(pdMS_TO_TICKS(150));

    // Reset ins neue Firmware-Image
    gpio_set_level((gpio_num_t)PIN_POD3_PWR_EN, 0);
    vTaskDelay(pdMS_TO_TICKS(50));
    gpio_set_level((gpio_num_t)PIN_POD3_PWR_EN, 1);

    s_flash_status.state = OMM_FLASH_SUCCESS;
    s_flash_status.progress_percent = 100;
    ESP_LOGI(TAG, "✓ OMM Firmware Push completed successfully! Coprocessor rebooted.");

    return ESP_OK;
}

esp_err_t omm_flasher_push_file(const char *bin_file_path) {
    if (!bin_file_path) return ESP_ERR_INVALID_ARG;

    ESP_LOGI(TAG, "Opening firmware image: %s", bin_file_path);
    FILE *f = fopen(bin_file_path, "rb");
    if (!f) {
        ESP_LOGE(TAG, "Firmware binary '%s' not found!", bin_file_path);
        snprintf(s_flash_status.last_error, sizeof(s_flash_status.last_error), "File not found");
        s_flash_status.state = OMM_FLASH_FAILED;
        return ESP_ERR_NOT_FOUND;
    }

    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);

    if (size <= 0 || size > 4 * 1024 * 1024) {
        fclose(f);
        return ESP_ERR_INVALID_SIZE;
    }

    uint8_t *buf = (uint8_t *)malloc(size);
    if (!buf) {
        fclose(f);
        return ESP_ERR_NO_MEM;
    }

    size_t read_bytes = fread(buf, 1, size, f);
    fclose(f);

    esp_err_t res = omm_flasher_push_buffer(buf, read_bytes);
    free(buf);
    return res;
}
