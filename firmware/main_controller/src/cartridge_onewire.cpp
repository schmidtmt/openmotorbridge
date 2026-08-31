#include "cartridge_onewire.h"
#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_rom_sys.h"
#include "esp_log.h"
#include "audio_dsp_pipeline.h"

static const char *TAG = "1WIRE_MGR";

#define PIN_POD1_1WIRE_ID  GPIO_NUM_2
#define PIN_POD2_1WIRE_ID  GPIO_NUM_22

static CartridgeInfo_t s_cartridge_port1 = {};
static CartridgeInfo_t s_cartridge_port2 = {};

// Dallas 1-Wire CRC-8 Lookup
static uint8_t onewire_crc8(const uint8_t *data, uint8_t len) {
    uint8_t crc = 0;
    for (uint8_t i = 0; i < len; i++) {
        uint8_t inbyte = data[i];
        for (uint8_t j = 0; j < 8; j++) {
            uint8_t mix = (crc ^ inbyte) & 0x01;
            crc >>= 1;
            if (mix) crc ^= 0x8C;
            inbyte >>= 1;
        }
    }
    return crc;
}

// 1-Wire Bit-Banging Primitives fuer parametrisierbaren GPIO Pin
static bool onewire_reset(gpio_num_t pin) {
    gpio_set_direction(pin, GPIO_MODE_OUTPUT_OD);
    gpio_set_level(pin, 0);
    esp_rom_delay_us(480); // Reset Pulse

    gpio_set_direction(pin, GPIO_MODE_INPUT);
    esp_rom_delay_us(70);  // Warten auf Presence Pulse

    int presence = gpio_get_level(pin);
    esp_rom_delay_us(410); // Restlicher Zeitschlitz

    return (presence == 0);
}

static void onewire_write_bit(gpio_num_t pin, uint8_t bit) {
    gpio_set_direction(pin, GPIO_MODE_OUTPUT_OD);
    gpio_set_level(pin, 0);
    if (bit) {
        esp_rom_delay_us(6);
        gpio_set_direction(pin, GPIO_MODE_INPUT);
        esp_rom_delay_us(64);
    } else {
        esp_rom_delay_us(60);
        gpio_set_direction(pin, GPIO_MODE_INPUT);
        esp_rom_delay_us(10);
    }
}

static uint8_t onewire_read_bit(gpio_num_t pin) {
    gpio_set_direction(pin, GPIO_MODE_OUTPUT_OD);
    gpio_set_level(pin, 0);
    esp_rom_delay_us(6);
    gpio_set_direction(pin, GPIO_MODE_INPUT);
    esp_rom_delay_us(9);
    int bit = gpio_get_level(pin);
    esp_rom_delay_us(55);
    return (uint8_t)bit;
}

static void onewire_write_byte(gpio_num_t pin, uint8_t byte) {
    for (int i = 0; i < 8; i++) {
        onewire_write_bit(pin, (byte >> i) & 0x01);
    }
}

static uint8_t onewire_read_byte(gpio_num_t pin) {
    uint8_t byte = 0;
    for (int i = 0; i < 8; i++) {
        byte |= (onewire_read_bit(pin) << i);
    }
    return byte;
}

esp_err_t cartridge_onewire_init(void) {
    ESP_LOGI(TAG, "Initializing Independent Dual 1-Wire Channels (Port 1: GPIO %d, Port 2: GPIO %d)...",
             PIN_POD1_1WIRE_ID, PIN_POD2_1WIRE_ID);

    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << PIN_POD1_1WIRE_ID) | (1ULL << PIN_POD2_1WIRE_ID),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&io_conf);

    return ESP_OK;
}

CartridgeInfo_t cartridge_get_info(uint8_t port_num) {
    if (port_num == 1) return s_cartridge_port1;
    return s_cartridge_port2;
}

static void load_profile_class(CartridgeInfo_t *cart, const char *profile_id) {
    strncpy(cart->profile_id, profile_id, sizeof(cart->profile_id) - 1);

    if (strcmp(profile_id, "disabled") == 0) {
        strncpy(cart->name, "Slot Deaktiviert (Mute)", sizeof(cart->name) - 1);
        strncpy(cart->vendor, "OpenMotorBridge System", sizeof(cart->vendor) - 1);
        cart->hardware_tier = 0;
        cart->input_gain_db = -96.0f;
        cart->output_gain_db = -96.0f;
        cart->toggle_mesh_ms = 0;
        cart->channel_next_ms = 0;
    } else if (strcmp(profile_id, "sena_60s") == 0) {
        strncpy(cart->name, "Sena 60S (Mesh 3.0 Wave)", sizeof(cart->name) - 1);
        strncpy(cart->vendor, "Sena Technologies", sizeof(cart->vendor) - 1);
        cart->hardware_tier = 1;
        cart->input_gain_db = 2.5f;
        cart->output_gain_db = 0.0f;
        cart->toggle_mesh_ms = 250;
        cart->channel_next_ms = 1000;
    } else if (strcmp(profile_id, "sena_apex") == 0) {
        strncpy(cart->name, "Sena Apex / Apex Plus (Mesh 3.0)", sizeof(cart->name) - 1);
        strncpy(cart->vendor, "Sena Technologies", sizeof(cart->vendor) - 1);
        cart->hardware_tier = 1;
        cart->input_gain_db = 2.0f;
        cart->output_gain_db = 0.0f;
        cart->toggle_mesh_ms = 200;
        cart->channel_next_ms = 1000;
    } else if (strcmp(profile_id, "sena_50_series") == 0) {
        strncpy(cart->name, "Sena 50S/R/C / MeshPort (Mesh 2.0/3.0)", sizeof(cart->name) - 1);
        strncpy(cart->vendor, "Sena Technologies", sizeof(cart->vendor) - 1);
        cart->hardware_tier = 1;
        cart->input_gain_db = 2.0f;
        cart->output_gain_db = 0.0f;
        cart->toggle_mesh_ms = 200;
        cart->channel_next_ms = 1000;
    } else if (strcmp(profile_id, "sena_spider") == 0) {
        strncpy(cart->name, "Sena Spider RT1 / ST1 (Mesh-Only)", sizeof(cart->name) - 1);
        strncpy(cart->vendor, "Sena Technologies", sizeof(cart->vendor) - 1);
        cart->hardware_tier = 2;
        cart->input_gain_db = 1.5f;
        cart->output_gain_db = 0.0f;
        cart->toggle_mesh_ms = 200;
        cart->channel_next_ms = 800;
    } else if (strcmp(profile_id, "sena_vortex") == 0) {
        strncpy(cart->name, "Sena Vortex (Bluetooth 5.1 Intercom)", sizeof(cart->name) - 1);
        strncpy(cart->vendor, "Sena Technologies", sizeof(cart->vendor) - 1);
        cart->hardware_tier = 3;
        cart->input_gain_db = 0.5f;
        cart->output_gain_db = 0.0f;
        cart->toggle_mesh_ms = 300;
        cart->channel_next_ms = 0;
    } else if (strcmp(profile_id, "sena_legacy_bt") == 0) {
        strncpy(cart->name, "Sena 20S / 10S / SF Series (Bluetooth)", sizeof(cart->name) - 1);
        strncpy(cart->vendor, "Sena Technologies", sizeof(cart->vendor) - 1);
        cart->hardware_tier = 3;
        cart->input_gain_db = 0.0f;
        cart->output_gain_db = 0.0f;
        cart->toggle_mesh_ms = 350;
        cart->channel_next_ms = 0;
    } else if (strcmp(profile_id, "cardo_dmc_gen2") == 0) {
        strncpy(cart->name, "Cardo Packtalk Pro / Edge (DMC Gen2)", sizeof(cart->name) - 1);
        strncpy(cart->vendor, "Cardo Systems", sizeof(cart->vendor) - 1);
        cart->hardware_tier = 1;
        cart->input_gain_db = 1.5f;
        cart->output_gain_db = -0.5f;
        cart->toggle_mesh_ms = 200;
        cart->channel_next_ms = 800;
    } else if (strcmp(profile_id, "cardo_freecom_live") == 0) {
        strncpy(cart->name, "Cardo Freecom 4x/2x / Spirit (Live)", sizeof(cart->name) - 1);
        strncpy(cart->vendor, "Cardo Systems", sizeof(cart->vendor) - 1);
        cart->hardware_tier = 2;
        cart->input_gain_db = 1.0f;
        cart->output_gain_db = -0.5f;
        cart->toggle_mesh_ms = 250;
        cart->channel_next_ms = 0;
    } else if (strcmp(profile_id, "cardo_dmc_legacy") == 0) {
        strncpy(cart->name, "Cardo Packtalk Bold / Black (DMC Gen1)", sizeof(cart->name) - 1);
        strncpy(cart->vendor, "Cardo Systems", sizeof(cart->vendor) - 1);
        cart->hardware_tier = 3;
        cart->input_gain_db = 0.5f;
        cart->output_gain_db = 0.0f;
        cart->toggle_mesh_ms = 300;
        cart->channel_next_ms = 600;
    } else if (strcmp(profile_id, "midland_wave") == 0) {
        strncpy(cart->name, "Midland Wave (Mesh / Digital Intercom)", sizeof(cart->name) - 1);
        strncpy(cart->vendor, "Midland Europe", sizeof(cart->vendor) - 1);
        cart->hardware_tier = 2;
        cart->input_gain_db = 2.0f;
        cart->output_gain_db = 0.0f;
        cart->toggle_mesh_ms = 250;
        cart->channel_next_ms = 800;
    } else if (strcmp(profile_id, "midland_bt") == 0) {
        strncpy(cart->name, "Midland BTR1 / Rush / BTX Series", sizeof(cart->name) - 1);
        strncpy(cart->vendor, "Midland Europe", sizeof(cart->vendor) - 1);
        cart->hardware_tier = 3;
        cart->input_gain_db = 1.5f;
        cart->output_gain_db = 0.0f;
        cart->toggle_mesh_ms = 300;
        cart->channel_next_ms = 0;
    } else if (strcmp(profile_id, "openmotormesh_pod3") == 0) {
        strncpy(cart->name, "OpenMotorMesh Rear Pod 3 Gateway", sizeof(cart->name) - 1);
        strncpy(cart->vendor, "OpenMotorBridge OSHW", sizeof(cart->vendor) - 1);
        cart->hardware_tier = 1;
        cart->input_gain_db = 0.0f;
        cart->output_gain_db = 0.0f;
        cart->toggle_mesh_ms = 0;
        cart->channel_next_ms = 0;
    } else {
        strncpy(cart->name, "Midland G9 Pro PMR446 Gateway", sizeof(cart->name) - 1);
        strncpy(cart->vendor, "Alan Electronics", sizeof(cart->vendor) - 1);
        cart->hardware_tier = 3;
        cart->input_gain_db = 4.0f;
        cart->output_gain_db = 2.0f;
        cart->toggle_mesh_ms = 0;
        cart->channel_next_ms = 0;
    }
}

static void scan_port(gpio_num_t pin, CartridgeInfo_t *cart, uint8_t port_idx, const char *default_profile) {
    taskENTER_CRITICAL_ISR(NULL);
    bool present = onewire_reset(pin);
    taskEXIT_CRITICAL_ISR(NULL);

    if (present) {
        uint8_t rom[8];
        taskENTER_CRITICAL_ISR(NULL);
        onewire_write_byte(pin, 0x33); // READ ROM Befehl (0x33)
        for (int i = 0; i < 8; i++) {
            rom[i] = onewire_read_byte(pin);
        }
        taskEXIT_CRITICAL_ISR(NULL);

        uint8_t crc = onewire_crc8(rom, 7);
        if (crc == rom[7] && rom[0] == 0x01) { // DS2401 Family Code
            if (!cart->is_connected) {
                cart->is_connected = true;
                memcpy(cart->rom_id, rom, 8);
                load_profile_class(cart, default_profile);
                ESP_LOGI(TAG, "Port %d: New Cartridge detected via 1-Wire: %s (%s)",
                         port_idx, cart->name, cart->vendor);
                audio_set_port_gains(s_cartridge_port1.input_gain_db, s_cartridge_port2.input_gain_db);
            }
        }
    } else {
        if (cart->is_connected) {
            cart->is_connected = false;
            load_profile_class(cart, "disabled");
            ESP_LOGW(TAG, "Port %d: Cartridge removed / empty. Applied disabled.json (Mute).", port_idx);
            audio_set_port_gains(s_cartridge_port1.input_gain_db, s_cartridge_port2.input_gain_db);
        }
    }
}

void cartridge_apply_profile_merge(uint8_t port, const char *profile_id, float gain_offset) {
    CartridgeInfo_t *cart = (port == 1) ? &s_cartridge_port1 : &s_cartridge_port2;
    if (cart->is_connected) {
        load_profile_class(cart, profile_id);
        cart->input_gain_db += gain_offset;
        ESP_LOGI(TAG, "Port %d: Merged dynamic profile '%s' with gain offset %.1f dB (Effective Gain: %.1f dB)",
                 port, profile_id, gain_offset, cart->input_gain_db);
        audio_set_port_gains(s_cartridge_port1.input_gain_db, s_cartridge_port2.input_gain_db);
    }
}

void task_cartridge_manager(void *pvParameters) {
    ESP_LOGI(TAG, "Dedicated Dual-Channel 1-Wire Manager Task running on Core 0.");

    while (true) {
        scan_port(PIN_POD1_1WIRE_ID, &s_cartridge_port1, 1, "sena_apex");
        scan_port(PIN_POD2_1WIRE_ID, &s_cartridge_port2, 2, "cardo_dmc_gen2");
        vTaskDelay(pdMS_TO_TICKS(2000));
    }
}