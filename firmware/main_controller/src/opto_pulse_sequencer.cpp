#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"

static const char *TAG = "OPTO_SEQ";

#define PIN_PORT1_KEY   GPIO_NUM_5
#define PIN_PORT2_KEY   GPIO_NUM_7

// Getakteter TLP222A Tastensimulations-Puls
void opto_trigger_single_click(gpio_num_t pin, uint32_t duration_ms) {
    ESP_LOGI(TAG, "Triggering Click Pulse on GPIO %d (%lu ms)", pin, duration_ms);
    gpio_set_level(pin, 1);
    vTaskDelay(pdMS_TO_TICKS(duration_ms));
    gpio_set_level(pin, 0);
    vTaskDelay(pdMS_TO_TICKS(300)); // Prellschutz & Pause
}

void opto_port1_toggle_mesh(void) {
    // 200 ms Puls für Sena Apex / Mesh Toggle
    opto_trigger_single_click(PIN_PORT1_KEY, 200);
}

void opto_port1_channel_next(void) {
    // 1000 ms Puls für Sena Apex / Channel Next
    opto_trigger_single_click(PIN_PORT1_KEY, 1000);
}

void opto_port2_channel_next(void) {
    // 800 ms Puls für Cardo DMC Gen2 / Channel Advance
    opto_trigger_single_click(PIN_PORT2_KEY, 800);
}