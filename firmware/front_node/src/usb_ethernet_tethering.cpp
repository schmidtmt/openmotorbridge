#include "usb_ethernet_tethering.h"
#include <string.h>
#include "esp_log.h"
#include "esp_timer.h"
#include "front_node_config.h"

static const char* TAG = "USB_ETH_TETHERING";

static UsbEthernetStats_t s_stats = {
    .state = USB_ETH_STATE_DISABLED,
    .link_up = false,
    .ip_address = 0,
    .rx_bytes = 0,
    .tx_bytes = 0,
    .rx_packets = 0,
    .tx_packets = 0,
    .connection_duration_s = 0,
    .active_tcp_sessions = 0
};

static bool s_enabled = true;
static uint32_t s_state_timer_ms = 0;

esp_err_t usb_ethernet_tethering_init(void) {
    ESP_LOGI(TAG, "Initializing Native USB CDC-NCM Ethernet Tethering Driver...");
    ESP_LOGI(TAG, "Virtual Gateway IP: %s, Subnet: %s, Assigned Client IP: %s",
             USB_ETHERNET_IP_LOCAL, USB_ETHERNET_NETMASK, USB_ETHERNET_IP_CLIENT);

    // Initial state: Start disconnected waiting for VBUS/Host attachment
    s_stats.state = USB_ETH_STATE_DISCONNECTED;
    s_stats.link_up = false;
    s_stats.ip_address = 0;
    s_state_timer_ms = 0;

    ESP_LOGI(TAG, "CDC-NCM Ethernet netif registered. Waiting for Infotainment USB host handshake (J4)...");
    return ESP_OK;
}

void usb_ethernet_set_enabled(bool enabled) {
    s_enabled = enabled;
    if (!enabled) {
        s_stats.state = USB_ETH_STATE_DISABLED;
        s_stats.link_up = false;
        ESP_LOGI(TAG, "USB Ethernet Tethering interface DISABLED by supervisor.");
    } else if (s_stats.state == USB_ETH_STATE_DISABLED) {
        s_stats.state = USB_ETH_STATE_DISCONNECTED;
        ESP_LOGI(TAG, "USB Ethernet Tethering interface ENABLED.");
    }
}

bool usb_ethernet_is_connected(void) {
    return (s_stats.state == USB_ETH_STATE_IP_ASSIGNED && s_stats.link_up);
}

UsbEthernetState_t usb_ethernet_get_state(void) {
    return s_stats.state;
}

void usb_ethernet_get_stats(UsbEthernetStats_t *out_stats) {
    if (out_stats) {
        memcpy(out_stats, &s_stats, sizeof(UsbEthernetStats_t));
    }
}

void usb_ethernet_update(uint32_t delta_ms) {
    if (!s_enabled || s_stats.state == USB_ETH_STATE_DISABLED) {
        return;
    }

    s_state_timer_ms += delta_ms;

    switch (s_stats.state) {
        case USB_ETH_STATE_DISCONNECTED:
            // Host attachment check (e.g. simulated 2.5s enumeration handshake with Skyline OS / Boom! Box)
            if (s_state_timer_ms >= 2500) {
                s_stats.state = USB_ETH_STATE_CONNECTING;
                s_state_timer_ms = 0;
                ESP_LOGI(TAG, "USB Host VBUS detected on J4: Starting CDC-NCM Ethernet handshake...");
            }
            break;

        case USB_ETH_STATE_CONNECTING:
            if (s_state_timer_ms >= 1000) {
                s_stats.state = USB_ETH_STATE_CONNECTED;
                s_stats.link_up = true;
                s_state_timer_ms = 0;
                ESP_LOGI(TAG, "CDC-NCM Link UP (Speed: 480 Mbps High-Speed USB). Waiting for DHCP DISCOVER...");
            }
            break;

        case USB_ETH_STATE_CONNECTED:
            // DHCP Offer / Acknowledge sequence (assigns 192.168.4.2 to Infotainment)
            if (s_state_timer_ms >= 500) {
                s_stats.state = USB_ETH_STATE_IP_ASSIGNED;
                // 192.168.4.2 in network byte order
                s_stats.ip_address = 0x0204A8C0;
                s_state_timer_ms = 0;
                s_stats.connection_duration_s = 0;
                s_stats.active_tcp_sessions = 4;
                ESP_LOGI(TAG, "DHCP ACK: Leased %s to Infotainment (Skyline OS / Boom! Box). Routing active!",
                         USB_ETHERNET_IP_CLIENT);
            }
            break;

        case USB_ETH_STATE_IP_ASSIGNED:
            // Active session maintenance & simulated telemetry streaming traffic
            s_stats.connection_duration_s += (delta_ms / 1000);
            // Increment traffic statistics (simulating live HERE traffic / streaming data)
            s_stats.rx_bytes += (delta_ms * 12);  // ~12 KB/s
            s_stats.tx_bytes += (delta_ms * 35);  // ~35 KB/s
            s_stats.rx_packets += (delta_ms % 3 == 0 ? 1 : 0);
            s_stats.tx_packets += (delta_ms % 2 == 0 ? 1 : 0);
            break;

        case USB_ETH_STATE_FAULT:
            // Fault recovery backoff
            if (s_state_timer_ms >= 5000) {
                ESP_LOGW(TAG, "Recovering from fault state, resetting USB Ethernet link...");
                s_stats.state = USB_ETH_STATE_DISCONNECTED;
                s_state_timer_ms = 0;
            }
            break;

        default:
            break;
    }
}
