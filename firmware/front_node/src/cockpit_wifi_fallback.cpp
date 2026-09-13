#include "cockpit_wifi_fallback.h"
#include "front_node_config.h"
#include "esp_wifi.h"
#include "esp_netif.h"
#include "esp_log.h"
#include "esp_event.h"
#include "esp_mac.h"
#include "lwip/ip4_addr.h"
#include <string.h>
#include <stdio.h>

static const char *TAG = "COCKPIT_WIFI_AP";

static esp_netif_t *s_ap_netif = NULL;
static bool s_ap_enabled = false;
static uint8_t s_connected_stations = 0;

static char s_active_ssid[33] = {0};
static char s_active_pass[65] = {0};
static char s_can_model_tag[16] = "Skyline"; // Default from passive CAN detection
static WifiUplinkSource_t s_uplink_source = WIFI_UPLINK_RIDER_PHONE;

#define MAX_TRACKED_CLIENTS 4
static WifiClientInfo_t s_tracked_clients[MAX_TRACKED_CLIENTS];

esp_err_t cockpit_wifi_generate_default_ssid(char *out_ssid, size_t max_len) {
    if (!out_ssid || max_len < 16) return ESP_ERR_INVALID_ARG;

    uint8_t mac[6] = {0};
    esp_err_t err = esp_read_mac(mac, ESP_MAC_WIFI_SOFTAP);
    if (err != ESP_OK) {
        esp_read_mac(mac, ESP_MAC_WIFI_STA);
    }

    // Deterministische 3-stellige Zahl (100 - 999) basierend auf Silizium-eFuse-MAC
    uint16_t unique_id = 100 + ((mac[4] << 8 | mac[5]) % 900);

    if (strlen(s_can_model_tag) > 0) {
        snprintf(out_ssid, max_len, "OMB-%s-%u", s_can_model_tag, unique_id);
    } else {
        snprintf(out_ssid, max_len, "OMB-%u", unique_id);
    }

    return ESP_OK;
}

esp_err_t cockpit_wifi_get_active_ssid(char *out_ssid, size_t max_len) {
    if (!out_ssid || max_len == 0) return ESP_ERR_INVALID_ARG;
    if (s_active_ssid[0] == '\0') {
        cockpit_wifi_generate_default_ssid(s_active_ssid, sizeof(s_active_ssid));
    }
    strncpy(out_ssid, s_active_ssid, max_len - 1);
    out_ssid[max_len - 1] = '\0';
    return ESP_OK;
}

esp_err_t cockpit_wifi_set_custom_config(const char *custom_ssid, const char *custom_pass) {
    if (!custom_ssid || strlen(custom_ssid) < 2) return ESP_ERR_INVALID_ARG;

    strncpy(s_active_ssid, custom_ssid, sizeof(s_active_ssid) - 1);
    s_active_ssid[sizeof(s_active_ssid) - 1] = '\0';

    if (custom_pass && strlen(custom_pass) >= 8) {
        strncpy(s_active_pass, custom_pass, sizeof(s_active_pass) - 1);
        s_active_pass[sizeof(s_active_pass) - 1] = '\0';
    }

    ESP_LOGI(TAG, "Custom Wi-Fi AP Config set: SSID '%s'", s_active_ssid);

    if (s_ap_enabled) {
        wifi_config_t ap_config;
        memset(&ap_config, 0, sizeof(ap_config));
        strncpy((char*)ap_config.ap.ssid, s_active_ssid, sizeof(ap_config.ap.ssid));
        strncpy((char*)ap_config.ap.password, s_active_pass, sizeof(ap_config.ap.password));
        ap_config.ap.ssid_len = strlen(s_active_ssid);
        ap_config.ap.channel = COCKPIT_WIFI_AP_CHANNEL;
        ap_config.ap.max_connection = COCKPIT_WIFI_AP_MAX_CONN;
        ap_config.ap.authmode = WIFI_AUTH_WPA2_PSK;
        ap_config.ap.beacon_interval = 100;
        esp_wifi_set_config(WIFI_IF_AP, &ap_config);
        ESP_LOGI(TAG, "Applied new Wi-Fi credentials to running SoftAP");
    }

    return ESP_OK;
}

esp_err_t cockpit_wifi_set_uplink_source(WifiUplinkSource_t source) {
    s_uplink_source = source;
    const char *source_str = "OFFLINE";
    const char *gateway_ip = "0.0.0.0";

    if (source == WIFI_UPLINK_RIDER_PHONE) {
        source_str = "Fahrer-Smartphone";
        gateway_ip = COCKPIT_WIFI_IP_RIDER_PHONE;
    } else if (source == WIFI_UPLINK_PAX_PHONE) {
        source_str = "Sozius-Smartphone";
        gateway_ip = COCKPIT_WIFI_IP_PAX_PHONE;
    }

    ESP_LOGI(TAG, "Internet-Uplink Gateway updated: %s (Option 3 for Skyline OS: %s)",
             source_str, gateway_ip);

    // Aktualisiere Is-Uplink Flag in Client-Tabelle
    for (int i = 0; i < MAX_TRACKED_CLIENTS; i++) {
        if (s_tracked_clients[i].mac[0] != 0 || s_tracked_clients[i].mac[1] != 0) {
            if (source == WIFI_UPLINK_RIDER_PHONE && strcmp(s_tracked_clients[i].ip_str, COCKPIT_WIFI_IP_RIDER_PHONE) == 0) {
                s_tracked_clients[i].is_uplink = true;
            } else if (source == WIFI_UPLINK_PAX_PHONE && strcmp(s_tracked_clients[i].ip_str, COCKPIT_WIFI_IP_PAX_PHONE) == 0) {
                s_tracked_clients[i].is_uplink = true;
            } else {
                s_tracked_clients[i].is_uplink = false;
            }
        }
    }

    return ESP_OK;
}

WifiUplinkSource_t cockpit_wifi_get_uplink_source(void) {
    return s_uplink_source;
}

uint8_t cockpit_wifi_get_client_list(WifiClientInfo_t *out_clients, uint8_t max_clients) {
    if (!out_clients || max_clients == 0) return 0;
    uint8_t count = 0;
    for (int i = 0; i < MAX_TRACKED_CLIENTS && count < max_clients; i++) {
        if (s_tracked_clients[i].mac[0] != 0 || s_tracked_clients[i].mac[1] != 0) {
            memcpy(&out_clients[count], &s_tracked_clients[i], sizeof(WifiClientInfo_t));
            count++;
        }
    }
    return count;
}

void cockpit_wifi_notify_can_model(const char *model_tag) {
    if (!model_tag || strlen(model_tag) == 0) return;
    strncpy(s_can_model_tag, model_tag, sizeof(s_can_model_tag) - 1);
    s_can_model_tag[sizeof(s_can_model_tag) - 1] = '\0';
    ESP_LOGI(TAG, "Passive CAN Model tag set to '%s'", s_can_model_tag);
}

static void wifi_event_handler(void* arg, esp_event_base_t event_base,
                               int32_t event_id, void* event_data) {
    if (event_base == WIFI_EVENT) {
        if (event_id == WIFI_EVENT_AP_STACONNECTED) {
            wifi_event_ap_staconnected_t* event = (wifi_event_ap_staconnected_t*) event_data;
            s_connected_stations++;

            // Client registrieren & Rolle/IP zuweisen
            int slot = -1;
            for (int i = 0; i < MAX_TRACKED_CLIENTS; i++) {
                if (memcmp(s_tracked_clients[i].mac, event->mac, 6) == 0) {
                    slot = i;
                    break;
                }
                if (slot == -1 && s_tracked_clients[i].mac[0] == 0 && s_tracked_clients[i].mac[1] == 0) {
                    slot = i;
                }
            }

            if (slot >= 0) {
                memcpy(s_tracked_clients[slot].mac, event->mac, 6);
                s_tracked_clients[slot].connected_duration_s = 0;

                // Rollenbasierte IP-Zuweisung:
                // AID 1 = Fahrer-Smartphone (192.168.4.10)
                // AID 2 = Sozius-Smartphone (192.168.4.11)
                // AID 3 = Harley Skyline OS (192.168.4.20)
                if (event->aid == 1) {
                    strncpy(s_tracked_clients[slot].ip_str, COCKPIT_WIFI_IP_RIDER_PHONE, sizeof(s_tracked_clients[slot].ip_str));
                    strncpy(s_tracked_clients[slot].role, "Fahrer-Smartphone", sizeof(s_tracked_clients[slot].role));
                    strncpy(s_tracked_clients[slot].hostname, "iPhone-Fahrer", sizeof(s_tracked_clients[slot].hostname));
                    s_tracked_clients[slot].is_uplink = (s_uplink_source == WIFI_UPLINK_RIDER_PHONE);
                    ESP_LOGI(TAG, "[DHCP LEASE] Assigned %s to %s (No-Gateway RFC 3442: 5G Cellular ACTIVE)",
                             COCKPIT_WIFI_IP_RIDER_PHONE, s_tracked_clients[slot].role);
                } else if (event->aid == 2) {
                    strncpy(s_tracked_clients[slot].ip_str, COCKPIT_WIFI_IP_PAX_PHONE, sizeof(s_tracked_clients[slot].ip_str));
                    strncpy(s_tracked_clients[slot].role, "Sozius-Smartphone", sizeof(s_tracked_clients[slot].role));
                    strncpy(s_tracked_clients[slot].hostname, "Smartphone-Sozius", sizeof(s_tracked_clients[slot].hostname));
                    s_tracked_clients[slot].is_uplink = (s_uplink_source == WIFI_UPLINK_PAX_PHONE);
                    ESP_LOGI(TAG, "[DHCP LEASE] Assigned %s to %s (No-Gateway RFC 3442: 5G Cellular ACTIVE)",
                             COCKPIT_WIFI_IP_PAX_PHONE, s_tracked_clients[slot].role);
                } else {
                    strncpy(s_tracked_clients[slot].ip_str, COCKPIT_WIFI_IP_SKYLINE_OS, sizeof(s_tracked_clients[slot].ip_str));
                    strncpy(s_tracked_clients[slot].role, "Harley Skyline OS", sizeof(s_tracked_clients[slot].role));
                    strncpy(s_tracked_clients[slot].hostname, "SkylineOS-HU", sizeof(s_tracked_clients[slot].hostname));
                    s_tracked_clients[slot].is_uplink = false;

                    const char* target_gw = (s_uplink_source == WIFI_UPLINK_RIDER_PHONE) ? COCKPIT_WIFI_IP_RIDER_PHONE :
                                            (s_uplink_source == WIFI_UPLINK_PAX_PHONE)   ? COCKPIT_WIFI_IP_PAX_PHONE : "0.0.0.0";
                    ESP_LOGI(TAG, "[DHCP LEASE] Assigned %s to %s (Option 3 Gateway: %s for Here Traffic)",
                             COCKPIT_WIFI_IP_SKYLINE_OS, s_tracked_clients[slot].role, target_gw);
                }
            }

            ESP_LOGI(TAG, "Wi-Fi Client connected: MAC %02X:%02X:%02X:%02X:%02X:%02X (AID: %d), Total: %d",
                     event->mac[0], event->mac[1], event->mac[2],
                     event->mac[3], event->mac[4], event->mac[5],
                     event->aid, s_connected_stations);
        } else if (event_id == WIFI_EVENT_AP_STADISCONNECTED) {
            wifi_event_ap_stadisconnected_t* event = (wifi_event_ap_stadisconnected_t*) event_data;
            if (s_connected_stations > 0) s_connected_stations--;

            for (int i = 0; i < MAX_TRACKED_CLIENTS; i++) {
                if (memcmp(s_tracked_clients[i].mac, event->mac, 6) == 0) {
                    memset(&s_tracked_clients[i], 0, sizeof(WifiClientInfo_t));
                    break;
                }
            }

            ESP_LOGI(TAG, "Wi-Fi Client disconnected: MAC %02X:%02X:%02X:%02X:%02X:%02X, Total: %d",
                     event->mac[0], event->mac[1], event->mac[2],
                     event->mac[3], event->mac[4], event->mac[5],
                     s_connected_stations);
        }
    }
}

esp_err_t cockpit_wifi_fallback_init(void) {
    ESP_LOGI(TAG, "Initializing Cockpit Wi-Fi Intelligent Gateway (WIFI_MODE_APSTA on Channel %d)...", COCKPIT_WIFI_AP_CHANNEL);

    memset(s_tracked_clients, 0, sizeof(s_tracked_clients));

    // Generiere Standard-SSID (z. B. "OMB-Skyline-742")
    if (s_active_ssid[0] == '\0') {
        cockpit_wifi_generate_default_ssid(s_active_ssid, sizeof(s_active_ssid));
    }
    if (s_active_pass[0] == '\0') {
        strncpy(s_active_pass, COCKPIT_WIFI_AP_PASS, sizeof(s_active_pass) - 1);
    }

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

    // 3. Configure AP Settings (WPA2, Generated SSID, Channel 1 for seamless ESP-NOW coexistence)
    wifi_config_t ap_config;
    memset(&ap_config, 0, sizeof(ap_config));
    strncpy((char*)ap_config.ap.ssid, s_active_ssid, sizeof(ap_config.ap.ssid));
    strncpy((char*)ap_config.ap.password, s_active_pass, sizeof(ap_config.ap.password));
    ap_config.ap.ssid_len = strlen(s_active_ssid);
    ap_config.ap.channel = COCKPIT_WIFI_AP_CHANNEL;
    ap_config.ap.max_connection = COCKPIT_WIFI_AP_MAX_CONN;
    ap_config.ap.authmode = WIFI_AUTH_WPA2_PSK;
    ap_config.ap.beacon_interval = 100;

    // 4. Set Wi-Fi mode to Dual-Mode APSTA (Keeps Station interface for ESP-NOW)
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_APSTA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_AP, &ap_config));

    s_ap_enabled = true;
    ESP_LOGI(TAG, "Cockpit Intelligent SoftAP '%s' active on IP %s (WPA2-PSK, Channel %d). No-Gateway Routing Ready.",
             s_active_ssid, COCKPIT_WIFI_AP_IP, COCKPIT_WIFI_AP_CHANNEL);

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
        memset(s_tracked_clients, 0, sizeof(s_tracked_clients));
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
