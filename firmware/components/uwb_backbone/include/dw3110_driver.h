#pragma once

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include "esp_err.h"
#include "driver/spi_master.h"
#include "driver/gpio.h"
#include "dw3110_regs.h"

#ifdef __cplusplus
extern "C" {
#endif

// -----------------------------------------------------------------------------
// DW3110 Hardware Pinout & SPI Bus Configuration
// -----------------------------------------------------------------------------
typedef struct {
    spi_host_device_t spi_host;   // z. B. SPI2_HOST
    gpio_num_t pin_sck;           // SPI Clock
    gpio_num_t pin_mosi;          // SPI MOSI
    gpio_num_t pin_miso;          // SPI MISO
    gpio_num_t pin_cs;            // SPI Chip Select (Active Low)
    gpio_num_t pin_irq;           // Interrupt Request from DW3110 (Active High)
    gpio_num_t pin_rst;           // Hardware Reset (Active Low)
    uint16_t   pan_id;            // IEEE 802.15.4 PAN ID (e.g. 0x0MB1)
    uint16_t   short_addr;        // Local 16-bit short address
} dw3110_config_t;

// -----------------------------------------------------------------------------
// Driver Callbacks
// -----------------------------------------------------------------------------
typedef void (*dw3110_rx_callback_t)(const uint8_t *data, size_t len, int8_t rssi_dbm, uint64_t rx_timestamp, void *user_ctx);
typedef void (*dw3110_tx_done_callback_t)(bool success, uint64_t tx_timestamp, void *user_ctx);

// -----------------------------------------------------------------------------
// DW3110 Low-Level Driver API
// -----------------------------------------------------------------------------
typedef struct dw3110_driver_s dw3110_driver_t;

/**
 * @brief Erzeugt und initialisiert eine DW3110 Transceiver-Instanz
 */
esp_err_t dw3110_init(const dw3110_config_t *config, dw3110_driver_t **driver_out);

/**
 * @brief Prüft ob der physische DW3110 über SPI antwortet
 */
bool dw3110_is_hardware_present(dw3110_driver_t *driver);

/**
 * @brief Liest die 32-Bit Device-ID aus (erwartet 0xDECA03xx)
 */
uint32_t dw3110_read_dev_id(dw3110_driver_t *driver);

/**
 * @brief Registriert RX und TX Callbacks
 */
void dw3110_set_callbacks(dw3110_driver_t *driver,
                          dw3110_rx_callback_t rx_cb,
                          dw3110_tx_done_callback_t tx_cb,
                          void *user_ctx);

/**
 * @brief Sendet ein Datenpaket mit deterministischer Latenz (< 0.2 ms on-air)
 * @param wait_for_response Wenn true, wechselt der Transceiver nach TX sofort in den RX-Modus
 */
esp_err_t dw3110_transmit(dw3110_driver_t *driver, const uint8_t *data, size_t len, bool wait_for_response);

/**
 * @brief Aktiviert den kontinuierlichen Empfangsmodus
 */
esp_err_t dw3110_start_rx(dw3110_driver_t *driver);

/**
 * @brief Schaltet den Transceiver in den Low-Power Standby
 */
esp_err_t dw3110_sleep(dw3110_driver_t *driver);

/**
 * @brief Interrupt Service Routine Handler (wird bei Pegelwechsel an pin_irq aufgerufen)
 */
void dw3110_isr_handler(dw3110_driver_t *driver);

/**
 * @brief Verarbeitet anstehende Events (im Task-Kontext)
 */
void dw3110_process_events(dw3110_driver_t *driver);

/**
 * @brief Berechnet die Distanz zweier Timestamps (Two-Way Ranging in cm)
 */
uint16_t dw3110_compute_twr_distance_cm(uint64_t poll_tx, uint64_t poll_rx,
                                        uint64_t resp_tx, uint64_t resp_rx);

/**
 * @brief Gibt die Hardware-Ressourcen des Treibers frei
 */
void dw3110_deinit(dw3110_driver_t *driver);

#ifdef __cplusplus
}
#endif
