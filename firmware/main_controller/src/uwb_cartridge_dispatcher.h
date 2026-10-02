#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"
#include "uwb_vehicle_backbone.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    bool     active;
    uint8_t  hardware_class;   // 0x01 = Sena, 0x02 = Cardo, 0x03 = UCS, 0x04 = PMR446
    uint16_t model_id;         // z. B. 0x0101 (Sena SPIDER), 0x0201 (Cardo Edge)
    uint64_t uid;              // 64-Bit Chip UID
    uint16_t vcc_mv;
    char     model_name[32];
    uint32_t last_ack_time_ms;
    uint8_t  last_result_code;
    uint16_t last_exec_us;
} CartridgeBayState_t;

/**
 * @brief Initialisiert den UWB Smart Cartridge Dispatcher
 */
esp_err_t uwb_cartridge_dispatcher_init(void);

/**
 * @brief Sendet einen mechatronischen Opcode per UWB (< 0.4 ms) an Bucht 1 oder Bucht 2
 */
esp_err_t uwb_cartridge_send_opcode(UwbNodeType bay, UwbCartridgeOpcode opcode, uint16_t custom_pulse_ms);

/**
 * @brief Bootet beide Kassetten simultan (z. B. bei Zündung AN)
 */
esp_err_t uwb_cartridge_power_on_all(void);

/**
 * @brief Fährt beide Kassetten sauber herunter (z. B. bei Zündung AUS)
 */
esp_err_t uwb_cartridge_power_off_all(void);

/**
 * @brief Toggelt Mesh-Intercom auf der angegebenen Bucht
 */
esp_err_t uwb_cartridge_toggle_mesh(UwbNodeType bay);

/**
 * @brief Fragt den aktuellen Zustand einer Kassettenbucht ab
 */
CartridgeBayState_t uwb_cartridge_get_bay_state(UwbNodeType bay);

#ifdef __cplusplus
}
#endif
