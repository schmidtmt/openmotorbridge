#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    bool is_linked;
    uint8_t ottocast_state;
    bool ottocast_power_on;
    bool ottocast_fault;
    uint32_t cafe_countdown_sec;
    uint8_t ambient_dba;
    uint64_t last_seen_us;
} FrontNodeStatus;

/**
 * @brief Initializes ESP-NOW link to the Universal Front Node
 */
esp_err_t esp_now_front_node_init(void);

/**
 * @brief Returns the latest telemetry & status from Front Node
 */
FrontNodeStatus esp_now_front_node_get_status(void);

/**
 * @brief Sends a 1-click reboot command to the Ottocast USB power switch
 */
esp_err_t esp_now_front_node_reboot_ottocast(void);

/**
 * @brief Synchronizes vehicle ignition state (KL15) with the Front Node
 */
esp_err_t esp_now_front_node_set_ignition(bool ignition_on);

#ifdef __cplusplus
}
#endif
