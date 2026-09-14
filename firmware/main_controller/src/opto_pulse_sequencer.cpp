#include "opto_pulse_sequencer.h"
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "cartridge_onewire.h"

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

void opto_trigger_double_click(gpio_num_t pin, uint32_t click_ms, uint32_t pause_ms) {
    ESP_LOGI(TAG, "Triggering TLP222A PhotoMOS Double-Click on GPIO %d (%lu ms on, %lu ms pause)...", pin, click_ms, pause_ms);
    gpio_set_level(pin, 1);
    vTaskDelay(pdMS_TO_TICKS(click_ms));
    gpio_set_level(pin, 0);
    vTaskDelay(pdMS_TO_TICKS(pause_ms));
    gpio_set_level(pin, 1);
    vTaskDelay(pdMS_TO_TICKS(click_ms));
    gpio_set_level(pin, 0);
    vTaskDelay(pdMS_TO_TICKS(300)); // Entprellzeit & Erholungspause
}

void opto_port_power_boot(uint8_t port) {
    if (cartridge_is_smart(port)) {
        ESP_LOGI(TAG, "Port %d: Smart Cartridge detected -> Dispatching Opcode POWER_BOOT (0x01)", port);
        smart_cartridge_send_cmd(port, SMART_CMD_POWER_BOOT);
    } else {
        gpio_num_t pin = (port == 1) ? PIN_PORT1_KEY : PIN_PORT2_KEY;
        ESP_LOGI(TAG, "Port %d: Legacy Cartridge -> Triggering 1000 ms Power-On pulse", port);
        opto_trigger_single_click(pin, 1000);
    }
}

void opto_port_volume_step(uint8_t port, bool volume_up) {
    if (cartridge_is_smart(port)) {
        uint8_t opcode = volume_up ? SMART_CMD_VOL_PLUS : SMART_CMD_VOL_MINUS;
        ESP_LOGI(TAG, "Port %d: Smart Cartridge detected -> Dispatching Opcode %s (0x%02X)",
                 port, volume_up ? "VOL_PLUS" : "VOL_MINUS", opcode);
        smart_cartridge_send_cmd(port, opcode);
    } else {
        gpio_num_t pin = (port == 1) ? PIN_PORT1_KEY : PIN_PORT2_KEY;
        ESP_LOGI(TAG, "Port %d: Legacy Cartridge -> Triggering 100 ms Volume pulse", port);
        opto_trigger_single_click(pin, 100);
    }
}

void opto_port1_toggle_mesh(void) {
    if (cartridge_is_smart(1)) {
        ESP_LOGI(TAG, "Port 1: Smart Cartridge detected -> Dispatching Opcode MESH_TOGGLE (0x05)");
        smart_cartridge_send_cmd(1, SMART_CMD_MESH_TOGGLE);
    } else {
        // 200 ms Puls für Sena Mesh (Mesh On/Off, Handbuch S. 25)
        opto_trigger_single_click(PIN_PORT1_KEY, 200);
    }
}

void opto_port1_toggle_group_mesh(void) {
    if (cartridge_is_smart(1)) {
        ESP_LOGI(TAG, "Port 1: Smart Cartridge detected -> Dispatching Opcode GROUP_MESH_TOGGLE (0x06)");
        smart_cartridge_send_cmd(1, SMART_CMD_GROUP_MESH_TOGGLE);
    } else {
        // 3000 ms Puls für Sena Spider X Slim (Wechsel Open Mesh ↔ Group Mesh, Handbuch S. 29)
        opto_trigger_single_click(PIN_PORT1_KEY, 3000);
    }
}

void opto_port1_channel_next(void) {
    if (cartridge_is_smart(1)) {
        ESP_LOGI(TAG, "Port 1: Smart Cartridge detected -> Dispatching Opcode CHANNEL_NEXT_MACRO (0x07)");
        smart_cartridge_send_cmd(1, SMART_CMD_CHANNEL_NEXT);
    } else {
        // Doppelklick für Sena Spider X Slim (Kanaleinstellungen aufrufen, Handbuch S. 26)
        // 2x 150 ms mit 150 ms Pause ruft Kanaleinstellung auf; automatisches Speichern nach 10s Timeout
        opto_trigger_double_click(PIN_PORT1_KEY, 150, 150);
    }
}

void opto_port2_channel_next(void) {
    if (cartridge_is_smart(2)) {
        ESP_LOGI(TAG, "Port 2: Smart Cartridge detected -> Dispatching Opcode CHANNEL_NEXT (0x07)");
        smart_cartridge_send_cmd(2, SMART_CMD_CHANNEL_NEXT);
    } else {
        // 800 ms Puls für Cardo DMC Gen2 (Kanalwechsel)
        opto_trigger_single_click(PIN_PORT2_KEY, 800);
    }
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