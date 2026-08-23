#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"

static const char *TAG = "1WIRE_MGR";

#define PIN_ONEWIRE_ID  GPIO_NUM_2

// 1-Wire Scan- und Erkennungstask
void task_cartridge_manager(void *pvParameters) {
    ESP_LOGI(TAG, "1-Wire Cartridge Recognition Task initialized on GPIO %d", PIN_ONEWIRE_ID);

    gpio_set_direction(PIN_ONEWIRE_ID, GPIO_MODE_INPUT_OUTPUT_OD);
    gpio_set_pull_mode(PIN_ONEWIRE_ID, GPIO_PULLUP_ONLY);

    while (true) {
        // Zyklischer 1-Wire ROM Search Scan (0xF0)
        // Erkennt angeschlossene DS2401 Silicon Serial Numbers der Kassetten
        // Bei Änderung des Steckplatz-Zustands: Laden des passenden JSON-Profils

        vTaskDelay(pdMS_TO_TICKS(2000));
    }
}