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

// Smart Cartridge Opcodes (Single-Wire UART 19200 Baud / GATT 0x09)
#define SMART_CMD_POWER_BOOT        0x01 // Sena: ACT_PLUS + ACT_CENTER (1000 ms) / Cardo: ACT_MEDIA + ACT_MOBILE (2000 ms)
#define SMART_CMD_POWER_OFF         0x02 // Sena: ACT_PLUS + ACT_CENTER (200 ms)  / Cardo: ACT_MEDIA + ACT_MOBILE (2000 ms)
#define SMART_CMD_VOL_PLUS          0x03 // Sena: ACT_PLUS (100 ms) / Cardo: ACT_WHEEL_PRESS (2000 ms, DMC Mute Toggle)
#define SMART_CMD_VOL_MINUS         0x04 // Sena: ACT_MINUS (100 ms) / Cardo: ACT_WHEEL_PRESS tap (150 ms, Audio Stop)
#define SMART_CMD_MESH_TOGGLE       0x05 // Sena: ACT_MESH (200 ms) / Cardo: ACT_INTERCOM tap (200 ms, DMC Audio Toggle)
#define SMART_CMD_GROUP_MESH_TOGGLE 0x06 // Sena: ACT_MESH 3s hold / Cardo: ACT_INTERCOM 5s hold (DMC Grouping)
#define SMART_CMD_CHANNEL_NEXT      0x07 // Autonomes Makro: Sena 2x MESH + 1x PLUS / Cardo 2x INTERCOM (Private Chat)
#define SMART_CMD_CHANNEL_PREV      0x08 // Autonomes Makro: Sena 2x MESH + 1x MINUS / Cardo 3x INTERCOM (DMC Bridge)
#define SMART_CMD_PHONE_PAIRING     0x09 // Haltepuls 5000 ms: Sena ACT_CENTER / Cardo ACT_MOBILE (Phone/BLE Pairing)

/**
 * @brief Initialisiert den 1-Wire Bus an PIN_ONEWIRE_ID (GPIO 2)
 */
esp_err_t cartridge_onewire_init(void);

/**
 * @brief Gibt die Informationen der an Port 1 bzw. Port 2 gesteckten Kassette zurück
 */
CartridgeInfo_t cartridge_get_info(uint8_t port_num);

/**
 * @brief Prüft, ob an Port 1 bzw. 2 eine Smart Cartridge (Rev 2.0 Mechatronik) aktiv ist
 */
bool cartridge_is_smart(uint8_t port_num);

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

