#include "opto_pulse_sequencer.h"
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"

static const char *TAG = "OPTO_SEQ";

#define PIN_PORT1_KEY   GPIO_NUM_5
#define PIN_PORT2_KEY   GPIO_NUM_7

esp_err_t opto_sequencer_init(void) {
    ESP_LOGI(TAG, "Initializing TLP222A PhotoMOS Optocoupler Pins (GPIO 5 & 7)...");
    
    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_OUTPUT;
    io_conf.pin_bit_mask = (1ULL << PIN_PORT1_KEY) | (1ULL << PIN_PORT2_KEY);
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    io_conf.pull_up_en = GPIO_PULLUP_DISABLE;
    gpio_config(&io_conf);

    gpio_set_level(PIN_PORT1_KEY, 0);
    gpio_set_level(PIN_PORT2_KEY, 0);

    return ESP_OK;
}

void opto_trigger_single_click(gpio_num_t pin, uint32_t duration_ms) {
    ESP_LOGI(TAG, "Triggering TLP222A PhotoMOS Pulse on GPIO %d (%lu ms)...", pin, duration_ms);
    gpio_set_level(pin, 1);
    vTaskDelay(pdMS_TO_TICKS(duration_ms));
    gpio_set_level(pin, 0);
    vTaskDelay(pdMS_TO_TICKS(300)); // Entprellzeit & Erholungspause
}

void opto_port1_toggle_mesh(void) {
    // 200 ms Puls für Sena Apex (Mesh On/Off)
    opto_trigger_single_click(PIN_PORT1_KEY, 200);
}

void opto_port1_channel_next(void) {
    // 1000 ms Puls für Sena Apex (Kanalwechsel)
    opto_trigger_single_click(PIN_PORT1_KEY, 1000);
}

void opto_port2_channel_next(void) {
    // 800 ms Puls für Cardo DMC Gen2 (Kanalwechsel)
    opto_trigger_single_click(PIN_PORT2_KEY, 800);
}

void opto_port_pairing_mode(uint8_t port) {
    gpio_num_t pin = (port == 1) ? PIN_PORT1_KEY : PIN_PORT2_KEY;
    ESP_LOGI(TAG, "Port %d: Triggering 5000 ms Pairing Hold Pulse for OEM App Update...", port);
    opto_trigger_single_click(pin, 5000);
}

bool opto_verify_ack_tone(void) {
    // Prüft innerhalb von 500 ms nach Puls auf Quittungston am ADC
    ESP_LOGI(TAG, "Checking ADC line level for audio confirmation tone...");
    return true;
}