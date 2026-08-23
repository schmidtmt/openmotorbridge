#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "driver/gpio.h"
#include "driver/adc.h"

static const char *TAG = "OMB_MAIN";

// GPIO Pin-Definitionen (v8.0 Pinout)
#define PIN_ADC_BAT         GPIO_NUM_1
#define PIN_ONEWIRE_ID      GPIO_NUM_2
#define PIN_ADC_LINE_LVL    GPIO_NUM_3
#define PIN_ADC_VIGN        GPIO_NUM_4
#define PIN_PORT1_KEY       GPIO_NUM_5
#define PIN_PORT1_VCC_EN    GPIO_NUM_6
#define PIN_PORT2_KEY       GPIO_NUM_7
#define PIN_PORT2_VCC_EN    GPIO_NUM_8
#define PIN_STATUS_LED      GPIO_NUM_48

// Task-Deklarationen
void task_audio_dsp(void *pvParameters);
void task_ble_services(void *pvParameters);
void task_cartridge_manager(void *pvParameters);
void task_power_supervisor(void *pvParameters);
void task_rear_pod_bridge(void *pvParameters);

extern "C" void app_main(void) {
    ESP_LOGI(TAG, "OpenMotorBridge v8.0 booting on ESP32-S3...");

    // 1. NVS Initialisierung
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    // 2. Hardware GPIOs & MOSFET Power-Gates schalten
    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_OUTPUT;
    io_conf.pin_bit_mask = (1ULL << PIN_PORT1_KEY) | (1ULL << PIN_PORT1_VCC_EN) |
                           (1ULL << PIN_PORT2_KEY) | (1ULL << PIN_PORT2_VCC_EN) |
                           (1ULL << PIN_STATUS_LED);
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    io_conf.pull_up_en = GPIO_PULLUP_DISABLE;
    gpio_config(&io_conf);

    // VCC für Pod 1 & Pod 2 freischalten
    gpio_set_level(PIN_PORT1_VCC_EN, 1);
    gpio_set_level(PIN_PORT2_VCC_EN, 1);
    gpio_set_level(PIN_PORT1_KEY, 0);
    gpio_set_level(PIN_PORT2_KEY, 0);

    ESP_LOGI(TAG, "Hardware power rails activated. Launching FreeRTOS tasks...");

    // 3. Task-Verteilung auf die CPU-Cores
    // CORE 1: Echtzeit-Audio DSP Pipeline (Latenzkritisch)
    xTaskCreatePinnedToCore(task_audio_dsp, "AudioDSP", 8192, NULL, configMAX_PRIORITIES - 1, NULL, 1);

    // CORE 0: Kommunikation, BLE Server, 1-Wire & Systemüberwachung
    xTaskCreatePinnedToCore(task_ble_services, "BLE_Server", 6144, NULL, 5, NULL, 0);
    xTaskCreatePinnedToCore(task_cartridge_manager, "Cartridge1W", 4096, NULL, 4, NULL, 0);
    xTaskCreatePinnedToCore(task_rear_pod_bridge, "RearPodBridge", 4096, NULL, 4, NULL, 0);
    xTaskCreatePinnedToCore(task_power_supervisor, "PowerSup", 3072, NULL, 2, NULL, 0);

    ESP_LOGI(TAG, "OpenMotorBridge v8.0 operational.");
}

// Dummy/Stub für Power-Supervisor-Task
void task_power_supervisor(void *pvParameters) {
    while (true) {
        // Zyklische Prüfung von KL15 (Zündung) und LiPo-USV-Spannung
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}