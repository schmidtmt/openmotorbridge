#pragma once

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include "esp_err.h"
#include "usb_backbone_types.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge v10.0 - Central Zero-Disassembly USB-Bus DFU & OTA Flasher
// Replaces legacy UART SLIP flasher with high-speed USB2517I-JZX 7-Port Hub
// Firmware Distribution (USB_PKT_FW_UPDATE_PUSH 0x50 / 0x51 + ROM USB-Serial-JTAG).
// Any satellite node (PCBA 05 Front-Node, PCBA 03 Pod 1/2, PCBA 08 Radar,
// PCBA 09/10 Unified OMM Tri-Band) can be flashed from Central Box or J3 USB-C!
// =============================================================================

typedef enum {
    OMM_FLASH_IDLE = 0,
    OMM_FLASH_SYNCING,
    OMM_FLASH_ERASING,
    OMM_FLASH_WRITING,
    OMM_FLASH_VERIFYING,
    OMM_FLASH_SUCCESS,
    OMM_FLASH_FAILED
} OmmFlashState_t;

typedef struct {
    OmmFlashState_t state;
    UsbNodeType target_node;
    uint32_t total_bytes;
    uint32_t written_bytes;
    uint8_t progress_percent;
    char last_error[64];
} OmmFlashStatus_t;

/**
 * @brief Initialisiert den v10.0 Central USB-Bus DFU & OTA Flasher
 */
esp_err_t omm_flasher_init(void);

/**
 * @brief Flasht eine Firmware-Binärdatei über den 4-Draht USB-Bus an einen spezifischen Zielknoten
 *        (Front-Node PCBA 05, Pod 1/2 PCBA 03, Radar PCBA 08, oder OMM Tri-Band PCBA 09/10)
 */
esp_err_t usb_bus_dfu_flash_node_file(UsbNodeType target_node, const char *bin_file_path);

/**
 * @brief Flasht ein Firmware-Image aus einem Puffer über den 4-Draht USB-Bus an einen Zielknoten
 */
esp_err_t usb_bus_dfu_flash_node_buffer(UsbNodeType target_node, const uint8_t *data, size_t length);

/**
 * @brief Versetzt einen Zielknoten über den USB2517I-Hub + TPS25921 eFuse in den Hardware-DFU-Modus
 */
esp_err_t usb_bus_dfu_enter_rom_bootloader(UsbNodeType target_node);

/**
 * @brief Legacy-Wrapper: Flasht ein gedocktes OMM Tri-Band Modul (oder Broadcast an alle OMM-Pods)
 */
esp_err_t omm_flasher_push_file(const char *bin_file_path);

/**
 * @brief Legacy-Wrapper: Flasht Puffer an OMM Tri-Band Modul
 */
esp_err_t omm_flasher_push_buffer(const uint8_t *data, size_t length);

/**
 * @brief Gibt den aktuellen Status und Fortschritt des USB-Bus-Flashvorgangs zurück
 */
OmmFlashStatus_t omm_flasher_get_status(void);

#ifdef __cplusplus
}
#endif
