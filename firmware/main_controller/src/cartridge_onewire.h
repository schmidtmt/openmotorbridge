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
    uint32_t channel_next_ms;
    bool is_connected;
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
 * @brief Task zur zyklischen Kassetten-Erkennung & Profil-Aktualisierung (Core 0)
 */
void task_cartridge_manager(void *pvParameters);

#ifdef __cplusplus
}
#endif
