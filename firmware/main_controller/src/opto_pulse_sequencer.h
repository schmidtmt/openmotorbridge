#pragma once

#include <stdint.h>
#include "driver/gpio.h"
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Initialisiert die GPIOs für die TLP222A Halbleiterrelais
 */
esp_err_t opto_sequencer_init(void);

/**
 * @brief Erzeugt einen exakt getakteten Tastensimulations-Puls
 */
void opto_trigger_single_click(gpio_num_t pin, uint32_t duration_ms);

/**
 * @brief Port 1: Mesh On/Off Toggle (200 ms Puls für Sena Apex)
 */
void opto_port1_toggle_mesh(void);

/**
 * @brief Port 1: Kanalweiterschaltung (1000 ms Puls für Sena Apex)
 */
void opto_port1_channel_next(void);

/**
 * @brief Port 2: Kanalweiterschaltung (800 ms Puls für Cardo DMC Gen2)
 */
void opto_port2_channel_next(void);

/**
 * @brief Triggert 5-Sekunden Haltepuls für Bluetooth-Pairing Modus (Hersteller-App Update)
 * @param port 1 für Port 1 (Links), 2 für Port 2 (Rechts)
 */
void opto_port_pairing_mode(uint8_t port);

/**
 * @brief Prüft innerhalb von 500 ms nach Puls auf Quittungston am ADC
 */
bool opto_verify_ack_tone(void);

#ifdef __cplusplus
}
#endif
