#include "cockpit_wifi_fallback.h"
#include "front_node_config.h"
#include "esp_wifi.h"
#include "esp_netif.h"
#include "esp_log.h"
#include "esp_event.h"
#include "lwip/ip4_addr.h"
#include <string.h>

static const char *TAG = "COCKPIT_WIFI_AP";

static esp_netif_t *s_ap_netif = NULL;
static bool s_ap_enabled = false;
static uint8_t s_connected_stations = 0;

static void wifi_event_handler(void* arg, esp_event_base_t event_base,
                               int32_t event_id, void* event_data) {
    if (event_base == WIFI_EVENT) {
        if (event_id == WIFI_EVENT_AP_STACONNECTED) {
            wifi_event_ap_staconnected_t* event = (wifi_event_ap_staconnected_t*) event_data;
            s_connected_stations++;
            ESP_LOGI(TAG, "Wi-Fi Client connected: MAC %02X:%02X:%02X:%02X:%02X:%02X (AID: %d), Total: %d",
                     event->mac[0], event->mac[1], event->mac[2],
                     event->mac[3], event->mac[4], event->mac[5],
                     event->aid, s_connected_stations);
        } else if (event_id == WIFI_EVENT_AP_STADISCONNECTED) {
            wifi_event_ap_stadisconnected_t* event = (wifi_event_ap_stadisconnected_t*) event_data;
            if (s_connected_stations > 0) s_connected_stations--;
            ESP_LOGI(TAG, "Wi-Fi Client disconnected: MAC %02X:%02X:%02X:%02X:%02X:%02X, Total: %d",
                     event->mac[0], event->mac[1], event->mac[2],
                     event->mac[3], event->mac[4], event->mac[5],
                     s_connected_stations);
        }
    }
}

esp_err_t cockpit_wifi_fallback_init(void) {
    ESP_LOGI(TAG, "Initializing Cockpit Wi-Fi Fallback SoftAP (WIFI_MODE_APSTA on Channel %d)...", COCKPIT_WIFI_AP_CHANNEL);

    // 1. Create AP network interface if not already created
    if (!s_ap_netif) {
        s_ap_netif = esp_netif_create_default_wifi_ap();
        if (!s_ap_netif) {
            ESP_LOGE(TAG, "Failed to create default Wi-Fi AP netif");
            return ESP_FAIL;
        }

        // Configure static IP for Front Node SoftAP (192.168.4.1)
        esp_netif_ip_info_t ip_info;
        memset(&ip_info, 0, sizeof(ip_info));
        ip4addr_aton(COCKPIT_WIFI_AP_IP, &ip_info.ip);
        ip4addr_aton(COCKPIT_WIFI_AP_GW, &ip_info.gw);
        ip4addr_aton(COCKPIT_WIFI_AP_NETMASK, &ip_info.netmask);

        esp_netif_dhcps_stop(s_ap_netif);
        esp_netif_set_ip_info(s_ap_netif, &ip_info);
        esp_netif_dhcps_start(s_ap_netif);
    }

    // 2. Register event handler for station connection events
    esp_event_handler_instance_register(WIFI_EVENT, ESP_EVENT_ANY_ID,
                                        &wifi_event_handler, NULL, NULL);

    // 3. Configure AP Settings (WPA2, SSID, Channel 1 for seamless ESP-NOW coexistence)
    wifi_config_t ap_config;
    memset(&ap_config, 0, sizeof(ap_config));
    strncpy((char*)ap_config.ap.ssid, COCKPIT_WIFI_AP_SSID, sizeof(ap_config.ap.ssid));
    strncpy((char*)ap_config.ap.password, COCKPIT_WIFI_AP_PASS, sizeof(ap_config.ap.password));
    ap_config.ap.ssid_len = strlen(COCKPIT_WIFI_AP_SSID);
    ap_config.ap.channel = COCKPIT_WIFI_AP_CHANNEL;
    ap_config.ap.max_connection = COCKPIT_WIFI_AP_MAX_CONN;
    ap_config.ap.authmode = WIFI_AUTH_WPA2_PSK;
    ap_config.ap.beacon_interval = 100;

    // 4. Set Wi-Fi mode to Dual-Mode APSTA (Keeps Station interface for ESP-NOW)
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_APSTA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_AP, &ap_config));

    s_ap_enabled = true;
    ESP_LOGI(TAG, "Cockpit SoftAP '%s' active on IP %s (WPA2-PSK). Dual-mode APSTA operational.",
             COCKPIT_WIFI_AP_SSID, COCKPIT_WIFI_AP_IP);

    return ESP_OK;
}

esp_err_t cockpit_wifi_fallback_set_enabled(bool enabled) {
    if (enabled == s_ap_enabled) return ESP_OK;

    if (enabled) {
        ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_APSTA));
        s_ap_enabled = true;
        ESP_LOGI(TAG, "Cockpit Wi-Fi SoftAP ENABLED");
    } else {
        ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
        s_ap_enabled = false;
        s_connected_stations = 0;
        ESP_LOGI(TAG, "Cockpit Wi-Fi SoftAP DISABLED (Station-only mode active)");
    }
    return ESP_OK;
}

bool cockpit_wifi_fallback_is_enabled(void) {
    return s_ap_enabled;
}

uint8_t cockpit_wifi_fallback_get_connected_stations(void) {
    return s_connected_stations;
}
