#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge - Front Node USB CDC-NCM Ethernet Tethering Driver
// =============================================================================
// Enables high-speed USB Ethernet network bridging between OpenMotorBridge and
// motorcycle infotainment systems (e.g. Harley-Davidson Skyline OS 2024+,
// Boom! Box GTS, BMW Connectivity) via native USB CDC-NCM.

#define USB_ETHERNET_IP_LOCAL       "192.168.4.1"       // Front-Node Gateway IP
#define USB_ETHERNET_IP_CLIENT      "192.168.4.2"       // Assigned Infotainment Client IP
#define USB_ETHERNET_NETMASK        "255.255.255.0"
#define USB_ETHERNET_DNS_PRIMARY    "1.1.1.1"
#define USB_ETHERNET_DNS_SECONDARY  "8.8.8.8"

typedef enum {
    USB_ETH_STATE_DISABLED = 0,
    USB_ETH_STATE_DISCONNECTED,     // USB cable disconnected / no host VBUS
    USB_ETH_STATE_CONNECTING,       // USB enumeration / CDC-NCM negotiation
    USB_ETH_STATE_CONNECTED,        // Link UP, waiting for DHCP request
    USB_ETH_STATE_IP_ASSIGNED,      // Infotainment has IP 192.168.4.2, routing active
    USB_ETH_STATE_FAULT             // Driver or lwIP buffer error
} UsbEthernetState_t;

typedef struct {
    UsbEthernetState_t state;
    bool link_up;
    uint32_t ip_address;            // Network byte order
    uint32_t rx_bytes;
    uint32_t tx_bytes;
    uint32_t rx_packets;
    uint32_t tx_packets;
    uint32_t connection_duration_s;
    uint16_t active_tcp_sessions;
} UsbEthernetStats_t;

/**
 * @brief Initialize TinyUSB CDC-NCM Device stack and lwIP netif
 * @return ESP_OK on success
 */
esp_err_t usb_ethernet_tethering_init(void);

/**
 * @brief Enable or disable USB tethering interface
 */
void usb_ethernet_set_enabled(bool enabled);

/**
 * @brief Check if USB CDC-NCM link is established and IP is leased
 */
bool usb_ethernet_is_connected(void);

/**
 * @brief Retrieve current USB Ethernet driver state
 */
UsbEthernetState_t usb_ethernet_get_state(void);

/**
 * @brief Retrieve real-time throughput and connection statistics
 */
void usb_ethernet_get_stats(UsbEthernetStats_t *out_stats);

/**
 * @brief Periodic driver maintenance task called from FreeRTOS supervisor
 * @param delta_ms Time elapsed in milliseconds
 */
void usb_ethernet_update(uint32_t delta_ms);

#ifdef __cplusplus
}
#endif
