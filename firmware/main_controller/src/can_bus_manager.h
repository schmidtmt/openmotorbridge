#pragma once

#include "esp_err.h"
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Maximum signals tracked simultaneously per vehicle profile
 */
#define CAN_PROFILE_MAX_SIGNALS     32
#define CAN_PROFILE_MAX_NAME_LEN    32

/**
 * @brief Decoded signal representation
 */
typedef struct {
    char name[CAN_PROFILE_MAX_NAME_LEN];
    uint32_t can_id;
    bool is_extended;
    uint16_t start_bit;
    uint16_t length_bits;
    bool is_big_endian;
    float scale;
    float offset;
    float current_val;
    uint32_t last_update_ms;
    bool valid;
} CanDecodedSignal_t;

/**
 * @brief Initialize the TI TCAN334G TWAI (CAN-Bus) Driver on GPIO 19 (TX) and GPIO 20 (RX).
 * Configured in Listen-Only mode by default to ensure zero interference with vehicle ECUs.
 */
esp_err_t can_bus_manager_init(void);

/**
 * @brief FreeRTOS Task for handling incoming CAN-Bus frames (wheel speed, RPM, telemetry).
 */
void task_can_bus_manager(void *pvParameters);

/**
 * @brief Load a vehicle profile by ID (e.g. "harley_skyline_2024", "bmw_motorrad_k5x_r1250_r1300", "generic_obd2_iso15765").
 * Searches LittleFS `/data/can_profiles/<id>.json`.
 */
esp_err_t can_bus_load_profile(const char *profile_id);

/**
 * @brief Get currently active CAN vehicle profile ID.
 */
const char* can_bus_get_active_profile_id(void);

/**
 * @brief Query if a specific signal is defined and active in the current vehicle profile.
 */
bool can_bus_has_signal(const char *signal_name);

/**
 * @brief Read the latest decoded value for a named signal.
 * @param signal_name Signal name (e.g. "speed_kmh", "engine_rpm", "tire_pressure_front_bar")
 * @param out_value Pointer to receive value
 * @return true if signal exists and has been received within valid timeout, false otherwise
 */
bool can_bus_get_signal(const char *signal_name, float *out_value);

/**
 * @brief Transmit low battery alert frame for Handlebar Remote to motorcycle TFT display.
 * @param battery_pct Current battery percentage of CR2032 button cell.
 */
void can_bus_send_remote_battery_warning(uint8_t battery_pct);

/**
 * @brief Check if active CAN-bus traffic is being received.
 */
bool can_bus_is_connected(void);

/**
 * @brief Check if CAN bus is operating in passive Listen-Only mode.
 */
bool can_bus_is_listen_only(void);

/**
 * @brief Get last received vehicle speed from CAN bus.
 */
float can_bus_get_vehicle_speed_kmh(void);

/**
 * @brief Get total received CAN frames count.
 */
uint32_t can_bus_get_rx_count(void);

/**
 * @brief Get current CAN frames per second rate.
 */
float can_bus_get_fps(void);

/**
 * @brief Trigger a 500 ms passive fingerprint scan across the CAN bus.
 */
esp_err_t can_bus_start_fingerprint_scan(void);

/**
 * @brief Check if fingerprint scan is currently in progress.
 */
bool can_bus_is_fingerprint_scan_running(void);

/**
 * @brief Get the profile ID detected by fingerprint scan (or NULL if unresolved).
 */
const char* can_bus_get_detected_profile_id(void);

#ifdef __cplusplus
}
#endif
