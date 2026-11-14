#pragma once

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge v10.0 - Onboard Semtech SX1262 868 MHz LoRa Engine (PCBA 01, U10)
// Exact KiCad Pinout (openmotorbridge_main.kicad_pcb):
//   SPI_SCK  = GPIO 12 (U2 Pad 4  -> U10 Pin 20)
//   SPI_MISO = GPIO 13 (U2 Pad 6  -> U10 Pin 18)
//   SPI_MOSI = GPIO 11 (U2 Pad 7  -> U10 Pin 19)
//   LORA_NSS = GPIO 10 (U2 Pad 24 -> U10 Pin 21)
//   LORA_RST = GPIO 7  (U2 Pad 23 -> U10 Pin 1)
//   LORA_BUSY= GPIO 21 (U2 Pad 20 -> U10 Pin 14)
//   LORA_DIO1= GPIO 14 (U2 Pad 19 -> U10 Pin 15)
// =============================================================================

typedef enum : uint8_t {
    LORA_STATUS_NORMAL_TELEMETRY      = 0x00, // Regular convoy beacon
    LORA_STATUS_LEFT_INTENTIONALLY    = 0x01, // Rider Double-Clicked: "Alles OK / Absichtlich abgebogen"
    LORA_STATUS_TECH_STOP_WAIT        = 0x02, // Rider Long-Pressed: "Technischer Stopp / Bitte warten"
    LORA_STATUS_UNCONFIRMED_EMERGENCY = 0x03  // No response after 15s: "Unbestätigt / Peilung & Notfall"
} LoRaHumanLoopStatus_t;

typedef struct __attribute__((packed)) {
    uint8_t  magic;           // 0x4C ('L')
    uint8_t  packet_type;     // 0xA1 = LoRaAlarmPacket (Convoy Split), 0xFE = Bike Theft Alarm
    uint8_t  human_status;    // LoRaHumanLoopStatus_t
    uint32_t sender_uid_low;  // 32-bit Bike ID
    int32_t  latitude_1e7;    // WGS84 Latitude * 1e7
    int32_t  longitude_1e7;   // WGS84 Longitude * 1e7
    uint16_t speed_kph_10;    // Speed * 10
    uint16_t heading_deg_10;  // Heading * 10
    uint8_t  battery_soc_pct; // UPS LiPo SoC %
    uint8_t  crc8;
} LoRaConvoyAlarmPacket_t;

/**
 * @brief Initialisiert den Onboard Semtech SX1262 LoRa-Transceiver (U10) auf PCBA 01
 */
esp_err_t sx1262_lora_init(void);

/**
 * @brief Prüft, ob der SX1262 per SPI erreichbar und betriebsbereit ist
 */
bool sx1262_lora_is_ready(void);

/**
 * @brief Sendet ein Roh-Datenpaket über 868.1 MHz LoRa (SF9 / BW125 / +22 dBm)
 */
esp_err_t sx1262_lora_transmit(const uint8_t *data, size_t len);

/**
 * @brief Sendet ein Human-in-the-Loop Gruppen-Status-/Notrufpaket (0xA1)
 */
esp_err_t sx1262_lora_send_convoy_status(LoRaHumanLoopStatus_t status, double lat, double lon, float speed_kmh, float heading_deg);

/**
 * @brief Versetzt den SX1262 in den stromsparenden CAD / Rx-Duty-Cycle Modus für 24/7 Park-Wächter
 */
esp_err_t sx1262_lora_enter_sentry_mode(void);

#ifdef __cplusplus
}
#endif

