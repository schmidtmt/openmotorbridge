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
 * @brief Erzeugt eine präzise Doppelklick-Pulssequenz (z.B. für Menüs/Kanalwahl)
 */
void opto_trigger_double_click(gpio_num_t pin, uint32_t click_ms, uint32_t pause_ms);

/**
 * @brief Port 1 bzw. 2: Power-On Boot Sequenz (Smart Cartridge Opcode 0x01 oder 1000 ms Puls)
 */
void opto_port_power_boot(uint8_t port);

/**
 * @brief Port 1 bzw. 2: Schrittweise Lautstärkeregelung (Opcode 0x03 Plus / 0x04 Minus)
 */
void opto_port_volume_step(uint8_t port, bool volume_up);

/**
 * @brief Port 1: Mesh On/Off Toggle (Opcode 0x05 oder 200 ms Puls)
 */
void opto_port1_toggle_mesh(void);

/**
 * @brief Port 1: Wechsel Open Mesh ↔ Group Mesh (Opcode 0x06 oder 3000 ms Haltepuls)
 */
void opto_port1_toggle_group_mesh(void);

/**
 * @brief Port 1: Kanalauswahl (Opcode 0x07 Autonomes Makro oder Doppelklick 2x 150 ms)
 */
void opto_port1_channel_next(void);

/**
 * @brief Port 2: Kanalweiterschaltung (Opcode 0x07 oder 800 ms Puls für Cardo DMC Gen2)
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
