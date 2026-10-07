#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"
#include "cartridge_ble_profile.h"

// =============================================================================
// Smart Cartridge BLE Central Client (ESP32-C6 @ PCBA 03 Rev 3.0)
// Manages digital Bluetooth Low Energy control of docked intercom units
// (Sena RC GATT, Cardo BLE v2, OMM Native, or HID Consumer Control)
// =============================================================================

class CartridgeBleClient {
public:
    static CartridgeBleClient& instance();

    /**
     * @brief Initialize BLE subsystem in Client / Central mode
     */
    esp_err_t init();

    /**
     * @brief Configure active BLE profile flavor and connection parameters
     */
    esp_err_t configure(const CartridgeBleConfig_t &config);

    /**
     * @brief Check whether BLE is actively connected and authenticated with the intercom
     */
    bool is_connected() const { return m_connected; }

    /**
     * @brief Transmit runtime opcode digitally over BLE GATT
     * @param opcode Cartridge opcode (CARTRIDGE_OPCODE_*)
     * @return ESP_OK if transmitted successfully, ESP_FAIL / ESP_ERR_* if BLE disconnected or failed
     */
    esp_err_t send_command(uint8_t opcode);

    /**
     * @brief Trigger reconnect / background scan
     */
    void trigger_connect();

    /**
     * @brief Disconnect BLE (e.g. before powering down or switching profile)
     */
    void disconnect();

    /**
     * @brief Periodic supervision loop (called in background task)
     */
    void update();

    const CartridgeBleConfig_t& get_config() const { return m_config; }

private:
    CartridgeBleClient();
    ~CartridgeBleClient() = default;

    // Protocol-specific packet builders
    esp_err_t send_omm_native(uint8_t opcode);
    esp_err_t send_sena_rc_gatt(uint8_t opcode);
    esp_err_t send_cardo_ble_v2(uint8_t opcode);
    esp_err_t send_hid_consumer(uint8_t opcode);

    CartridgeBleConfig_t m_config;
    bool                 m_initialized;
    bool                 m_connected;
    uint32_t             m_last_connect_attempt_ms;
    uint16_t             m_conn_handle;
};
