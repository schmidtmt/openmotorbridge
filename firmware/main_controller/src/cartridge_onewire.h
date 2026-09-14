#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    uint8_t rom_id[8];
    char profile_id[32];
    char name[64];
    char vendor[32];
    uint8_t hardware_tier;
    float input_gain_db;
    float output_gain_db;
    uint32_t toggle_mesh_ms;
    uint32_t toggle_group_mesh_ms;
    uint32_t channel_next_ms;
    bool is_connected;
    bool is_smart_cartridge;
    uint8_t num_actuators;
    uint8_t smart_mcu_protocol_ver;
} CartridgeInfo_t;

/**
 * @brief Initialisiert den 1-Wire Bus an PIN_ONEWIRE_ID (GPIO 2)
 */
esp_err_t cartridge_onewire_init(void);

/**
 * @brief Gibt die Informationen der an Port 1 bzw. Port 2 gesteckten Kassette zurück
 */
CartridgeInfo_t cartridge_get_info(uint8_t port_num);

/**
 * @brief Führt ein Profil-Merge zur Laufzeit durch und flasht Smart Cartridge MCUs
 */
void cartridge_apply_profile_merge(uint8_t port, const char *profile_id, float gain_offset);

/**
 * @brief Flasht/provisioniert die Kassetten-Konfiguration in den Smart Cartridge MCU (CH32V003/ATtiny)
 */
esp_err_t smart_cartridge_flash_config(uint8_t port, const char *profile_id);

/**
 * @brief Sendet ein Steuer-Kommando (Opcode) an den Smart Cartridge MCU
 */
esp_err_t smart_cartridge_send_cmd(uint8_t port, uint8_t cmd_opcode);

/**
 * @brief Task zur zyklischen Kassetten-Erkennung & Profil-Aktualisierung (Core 0)
 */
void task_cartridge_manager(void *pvParameters);

#ifdef __cplusplus
}
#endif

