#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"
#include "front_c3_config.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge v10.0 - Front-Node Inter-Chip UART Link (COMM_14 & COMM_15)
// Connects ESP32-S31 (U1) and ESP32-C3FH4 (U10) @ 921600 Baud
// =============================================================================

typedef void (*InterchipCommandCallback)(InterchipPktType type, const uint8_t *payload, size_t len);

/**
 * @brief Initialisiert die UART-Schnittstelle zu Chip 1 (S31 U1)
 */
esp_err_t interchip_uart_init(InterchipCommandCallback cb);

/**
 * @brief Sendet den aktuellen Status von Chip 2 an Chip 1
 */
esp_err_t interchip_uart_send_status(const C3HeadunitState *state);

/**
 * @brief Sendet Feedback zur aktuellen Headunit-Lautstärke an Chip 1
 */
esp_err_t interchip_uart_send_volume_feedback(uint8_t vol_pct);

/**
 * @brief Liest und verarbeitet empfangene Bytes aus dem UART-Puffer
 */
void interchip_uart_process_rx(void);

#ifdef __cplusplus
}
#endif
