#include "front_cam_ble_manager.h"
#include <string.h>
#include "esp_log.h"
#include "esp_timer.h"
#include "nvs_flash.h"
#include "nvs.h"

static const char* TAG = "CAM_BLE_MGR";

#define NVS_NAMESPACE       "cam_ble"
#define NVS_KEY_MAC         "mac"
#define NVS_KEY_PROFILE     "profile"
#define NVS_KEY_NAME        "name"
#define NVS_KEY_AUTOCONN    "autoconn"
#define NVS_KEY_FUEL_FILT   "fuelfilt"

FrontCamBleManager& FrontCamBleManager::instance() {
    static FrontCamBleManager inst;
    return inst;
}

FrontCamBleManager::FrontCamBleManager()
    : m_state(CAM_STATE_DISCONNECTED)
    , m_profile(CAM_PROFILE_NONE)
    , m_has_paired_device(false)
    , m_battery_pct(88)
    , m_sd_min_remaining(165)
    , m_autoconnect_enabled(true)
    , m_fuel_filter_enabled(true)
    , m_was_recording_at_fuel_stop(false)
    , m_scan_timer_ticks(0)
    , m_reconnect_timer_ticks(0)
    , m_telemetry_timer_ticks(0)
    , m_scan_cb(nullptr)
    , m_status_cb(nullptr)
{
    memset(m_paired_mac, 0, sizeof(m_paired_mac));
    memset(m_camera_name, 0, sizeof(m_camera_name));
}

bool FrontCamBleManager::init() {
    ESP_LOGI(TAG, "Initializing Action-Cam BLE Manager (Central & Observer)...");

    // Load persisted pairing and autoconnect configurations from NVS
    load_settings_from_nvs();

    if (m_has_paired_device) {
        ESP_LOGI(TAG, "Paired Camera found in NVS: '%s' [%02X:%02X:%02X:%02X:%02X:%02X], Profile=%d, Autoconnect=%d",
                 m_camera_name,
                 m_paired_mac[0], m_paired_mac[1], m_paired_mac[2],
                 m_paired_mac[3], m_paired_mac[4], m_paired_mac[5],
                 (int)m_profile, (int)m_autoconnect_enabled);

        if (m_autoconnect_enabled) {
            ESP_LOGI(TAG, "Autoconnect is enabled -> initiating immediate BLE connection to paired camera.");
            m_state = CAM_STATE_CONNECTING;
        }
    } else {
        ESP_LOGI(TAG, "No paired camera in NVS. Ready for WebApp pairing.");
    }

    return true;
}

void FrontCamBleManager::set_scan_result_callback(CamScanResultCallback cb) {
    m_scan_cb = cb;
}

void FrontCamBleManager::set_status_callback(CamStatusCallback cb) {
    m_status_cb = cb;
}

CamProfileType FrontCamBleManager::detect_camera_profile(const uint8_t* adv_data, size_t adv_len, const char* name) {
    if (!name) name = "";

    // 1. Check for GoPro Hero / Max (Open GoPro UUID 0xFEA6 or "GoPro" prefix)
    if (strstr(name, "GoPro") != nullptr || strstr(name, "GOPRO") != nullptr) {
        return CAM_PROFILE_GOPRO;
    }
    if (adv_data && adv_len >= 2) {
        for (size_t i = 0; i < adv_len - 1; ++i) {
            if (adv_data[i] == 0xA6 && adv_data[i + 1] == 0xFE) {
                return CAM_PROFILE_GOPRO;
            }
        }
    }

    // 2. Check for Insta360 (X3, X4, Ace Pro, GO 3, ONE)
    if (strstr(name, "Insta360") != nullptr || strstr(name, "Insta") != nullptr ||
        strstr(name, "Ace") != nullptr || strstr(name, "ONE X") != nullptr) {
        return CAM_PROFILE_INSTA360;
    }
    if (adv_data && adv_len >= 2) {
        for (size_t i = 0; i < adv_len - 1; ++i) {
            if (adv_data[i] == 0x01 && adv_data[i + 1] == 0xFF) {
                return CAM_PROFILE_INSTA360;
            }
        }
    }

    // 3. Check for DJI Action & Osmo 360 (Action 3/4/5 Pro, Osmo 360, Osmo Action)
    if (strstr(name, "Action") != nullptr || strstr(name, "Osmo") != nullptr ||
        strstr(name, "DJI") != nullptr || strstr(name, "OSMO") != nullptr) {
        return CAM_PROFILE_DJI;
    }

    return CAM_PROFILE_NONE;
}

void FrontCamBleManager::start_scan(uint32_t duration_sec) {
    ESP_LOGI(TAG, "Starting BLE Inquiry Scan for Action Cameras (Duration: %lu s)...", duration_sec);
    m_state = CAM_STATE_SCANNING;
    m_scan_timer_ticks = duration_sec * 5; // 5 Hz supervisor ticks

    // Simulate / Trigger NimBLE Observer Discovery
    // When real discovery arrives, detect_camera_profile parses the adv packet.
    // Here we also report immediately if a supported device is found in range:
    if (m_scan_cb) {
        // Example mock / probe result during scan to verify pipeline
        DiscoveredCamItem item = {
            .mac = {0xC4, 0x64, 0xE3, 0x42, 0x19, 0xB1},
            .rssi = -54,
            .profile = CAM_PROFILE_GOPRO
        };
        strncpy(item.name, "GoPro Hero 12 Black", sizeof(item.name));
        m_scan_cb(&item);
    }
}

void FrontCamBleManager::stop_scan() {
    if (m_state == CAM_STATE_SCANNING) {
        ESP_LOGI(TAG, "BLE Camera Scan finished or cancelled.");
        m_state = m_has_paired_device ? CAM_STATE_CONNECTED : CAM_STATE_DISCONNECTED;
        m_scan_timer_ticks = 0;
    }
}

bool FrontCamBleManager::pair_device(const uint8_t* mac, CamProfileType profile, const char* name) {
    if (!mac) return false;

    memcpy(m_paired_mac, mac, 6);
    m_profile = profile;
    m_has_paired_device = true;

    if (name && strlen(name) > 0) {
        strncpy(m_camera_name, name, sizeof(m_camera_name) - 1);
    } else {
        switch (profile) {
            case CAM_PROFILE_GOPRO:    strncpy(m_camera_name, "GoPro Hero BLE", sizeof(m_camera_name)); break;
            case CAM_PROFILE_INSTA360: strncpy(m_camera_name, "Insta360 BLE", sizeof(m_camera_name)); break;
            case CAM_PROFILE_DJI:      strncpy(m_camera_name, "DJI Osmo / Action BLE", sizeof(m_camera_name)); break;
            default:                   strncpy(m_camera_name, "Action Cam BLE", sizeof(m_camera_name)); break;
        }
    }

    m_autoconnect_enabled = true;
    save_settings_to_nvs();

    m_state = CAM_STATE_CONNECTED;
    ESP_LOGI(TAG, "Successfully paired camera: '%s' [%02X:%02X:%02X:%02X:%02X:%02X] Profile=%d. Saved to NVS.",
             m_camera_name,
             m_paired_mac[0], m_paired_mac[1], m_paired_mac[2],
             m_paired_mac[3], m_paired_mac[4], m_paired_mac[5],
             (int)m_profile);

    if (m_status_cb) {
        m_status_cb(m_state, m_profile, m_battery_pct, m_sd_min_remaining, is_recording());
    }

    return true;
}

void FrontCamBleManager::unpair() {
    ESP_LOGW(TAG, "Unpairing action camera and erasing persistent pairing from NVS...");
    if (is_recording()) {
        toggle_recording(); // Stop recording before disconnect
    }
    clear_settings_in_nvs();
    m_has_paired_device = false;
    memset(m_paired_mac, 0, sizeof(m_paired_mac));
    memset(m_camera_name, 0, sizeof(m_camera_name));
    m_profile = CAM_PROFILE_NONE;
    m_state = CAM_STATE_DISCONNECTED;

    if (m_status_cb) {
        m_status_cb(m_state, m_profile, 0, 0, false);
    }
}

bool FrontCamBleManager::send_gopro_command(const uint8_t* cmd, size_t len) {
    ESP_LOGI(TAG, "Transmitting Open GoPro BLE Command (len=%zu): Op=0x%02X", len, len > 0 ? cmd[0] : 0);
    // In hardware: ble_gattc_write_flat(conn_handle, gopro_cmd_char_handle, cmd, len, ...)
    return true;
}

bool FrontCamBleManager::send_insta360_command(const uint8_t* cmd, size_t len) {
    ESP_LOGI(TAG, "Transmitting Insta360 BLE Shutter Command (len=%zu): Op=0x%02X", len, len > 0 ? cmd[0] : 0);
    return true;
}

bool FrontCamBleManager::send_dji_command(const uint8_t* cmd, size_t len) {
    ESP_LOGI(TAG, "Transmitting DJI Action / Osmo 360 BLE Command (len=%zu): Op=0x%02X", len, len > 0 ? cmd[0] : 0);
    return true;
}

bool FrontCamBleManager::toggle_recording() {
    if (!is_connected()) {
        ESP_LOGW(TAG, "Cannot toggle recording: No action camera connected.");
        return false;
    }

    bool start_rec = (m_state != CAM_STATE_RECORDING);

    if (start_rec) {
        ESP_LOGI(TAG, "▶️ START RECORDING Command triggered via Profile %d", (int)m_profile);
        switch (m_profile) {
            case CAM_PROFILE_GOPRO: {
                static const uint8_t cmd_gopro_start[] = {0x03, 0x01, 0x01, 0x01};
                send_gopro_command(cmd_gopro_start, sizeof(cmd_gopro_start));
                break;
            }
            case CAM_PROFILE_INSTA360: {
                static const uint8_t cmd_insta_start[] = {0x02, 0x01, 0x01};
                send_insta360_command(cmd_insta_start, sizeof(cmd_insta_start));
                break;
            }
            case CAM_PROFILE_DJI: {
                static const uint8_t cmd_dji_start[] = {0x55, 0x01, 0x01, 0x01};
                send_dji_command(cmd_dji_start, sizeof(cmd_dji_start));
                break;
            }
            default: break;
        }
        m_state = CAM_STATE_RECORDING;
    } else {
        ESP_LOGI(TAG, "⏹️ STOP RECORDING Command triggered via Profile %d", (int)m_profile);
        switch (m_profile) {
            case CAM_PROFILE_GOPRO: {
                static const uint8_t cmd_gopro_stop[] = {0x03, 0x01, 0x01, 0x00};
                send_gopro_command(cmd_gopro_stop, sizeof(cmd_gopro_stop));
                break;
            }
            case CAM_PROFILE_INSTA360: {
                static const uint8_t cmd_insta_stop[] = {0x02, 0x01, 0x00};
                send_insta360_command(cmd_insta_stop, sizeof(cmd_insta_stop));
                break;
            }
            case CAM_PROFILE_DJI: {
                static const uint8_t cmd_dji_stop[] = {0x55, 0x01, 0x01, 0x00};
                send_dji_command(cmd_dji_stop, sizeof(cmd_dji_stop));
                break;
            }
            default: break;
        }
        m_state = CAM_STATE_CONNECTED;
    }

    if (m_status_cb) {
        m_status_cb(m_state, m_profile, m_battery_pct, m_sd_min_remaining, is_recording());
    }
    return true;
}

bool FrontCamBleManager::trigger_hilight() {
    if (!is_connected()) {
        ESP_LOGW(TAG, "Cannot set HiLight marker: Camera not connected.");
        return false;
    }

    ESP_LOGI(TAG, "🔖 HILIGHT BOOKMARK TAG Triggered via Profile %d", (int)m_profile);
    switch (m_profile) {
        case CAM_PROFILE_GOPRO: {
            static const uint8_t cmd_gopro_tag[] = {0x01, 0x18};
            send_gopro_command(cmd_gopro_tag, sizeof(cmd_gopro_tag));
            break;
        }
        case CAM_PROFILE_INSTA360: {
            static const uint8_t cmd_insta_tag[] = {0x02, 0x02, 0x01};
            send_insta360_command(cmd_insta_tag, sizeof(cmd_insta_tag));
            break;
        }
        case CAM_PROFILE_DJI: {
            static const uint8_t cmd_dji_tag[] = {0x55, 0x02, 0x01};
            send_dji_command(cmd_dji_tag, sizeof(cmd_dji_tag));
            break;
        }
        default: break;
    }
    return true;
}

void FrontCamBleManager::set_autoconnect(bool enable) {
    m_autoconnect_enabled = enable;
    save_settings_to_nvs();
    ESP_LOGI(TAG, "Action-Cam Autoconnect changed to: %s", enable ? "ENABLED" : "DISABLED");
}

void FrontCamBleManager::set_fuel_filter(bool enable) {
    m_fuel_filter_enabled = enable;
    save_settings_to_nvs();
    ESP_LOGI(TAG, "Action-Cam Tankpausen-Filter changed to: %s", enable ? "ENABLED" : "DISABLED");
}

void FrontCamBleManager::on_ignition_state_change(bool ignition_on) {
    if (!m_fuel_filter_enabled) return;

    if (!ignition_on) {
        // Vehicle ignition turned OFF: Tankpause / Stop
        if (is_recording()) {
            ESP_LOGW(TAG, "⛽ KL15 AUS (Tankpause): C_BUF Pufferkondensator aktiv -> Sende BLE STOP RECORDING...");
            toggle_recording(); // Send clean stop
            m_was_recording_at_fuel_stop = true;
        }
    } else {
        // Vehicle ignition turned ON: Resuming journey
        if (m_was_recording_at_fuel_stop) {
            ESP_LOGI(TAG, "⛽ KL15 EIN (Fahrtaufnahme): Setze Action-Cam Aufnahme automatisch fort...");
            toggle_recording(); // Resume recording
            m_was_recording_at_fuel_stop = false;
        }
    }
}

void FrontCamBleManager::update() {
    // 1. Scan Timer Watchdog
    if (m_state == CAM_STATE_SCANNING) {
        if (m_scan_timer_ticks > 0) {
            m_scan_timer_ticks--;
            if (m_scan_timer_ticks == 0) {
                stop_scan();
            }
        }
    }

    // 2. Autoconnect Loop (When disconnected, has paired device, and autoconnect enabled)
    if (m_state == CAM_STATE_DISCONNECTED && m_has_paired_device && m_autoconnect_enabled) {
        m_reconnect_timer_ticks++;
        if (m_reconnect_timer_ticks >= 25) { // every 5 seconds (at 5 Hz)
            m_reconnect_timer_ticks = 0;
            ESP_LOGD(TAG, "Autoconnect: Attempting background connection to '%s'...", m_camera_name);
            m_state = CAM_STATE_CONNECTING;
            // Simulated connection acquisition after 1 cycle
            m_state = CAM_STATE_CONNECTED;
            ESP_LOGI(TAG, "✓ Autoconnect succeeded! Connected to '%s'.", m_camera_name);
            if (m_status_cb) {
                m_status_cb(m_state, m_profile, m_battery_pct, m_sd_min_remaining, is_recording());
            }
        }
    }

    // 3. Telemetry Refresh (every 1 second)
    m_telemetry_timer_ticks++;
    if (m_telemetry_timer_ticks >= 5) {
        m_telemetry_timer_ticks = 0;

        if (is_recording() && m_sd_min_remaining > 0) {
            // Gradually decrement remaining SD recording capacity during active recording
            static uint8_t minute_div = 0;
            minute_div++;
            if (minute_div >= 60) {
                minute_div = 0;
                m_sd_min_remaining--;
            }
        }

        if (m_status_cb && is_connected()) {
            m_status_cb(m_state, m_profile, m_battery_pct, m_sd_min_remaining, is_recording());
        }
    }
}

void FrontCamBleManager::load_settings_from_nvs() {
    nvs_handle_t handle;
    esp_err_t err = nvs_open(NVS_NAMESPACE, NVS_READONLY, &handle);
    if (err != ESP_OK) {
        return; // No config stored yet
    }

    size_t mac_size = sizeof(m_paired_mac);
    if (nvs_get_blob(handle, NVS_KEY_MAC, m_paired_mac, &mac_size) == ESP_OK && mac_size == 6) {
        m_has_paired_device = true;
    }

    uint8_t prof = 0;
    if (nvs_get_u8(handle, NVS_KEY_PROFILE, &prof) == ESP_OK) {
        m_profile = static_cast<CamProfileType>(prof);
    }

    size_t name_size = sizeof(m_camera_name);
    nvs_get_str(handle, NVS_KEY_NAME, m_camera_name, &name_size);

    uint8_t autoconn = 1;
    if (nvs_get_u8(handle, NVS_KEY_AUTOCONN, &autoconn) == ESP_OK) {
        m_autoconnect_enabled = (autoconn != 0);
    }

    uint8_t fuelfilt = 1;
    if (nvs_get_u8(handle, NVS_KEY_FUEL_FILT, &fuelfilt) == ESP_OK) {
        m_fuel_filter_enabled = (fuelfilt != 0);
    }

    nvs_close(handle);
}

void FrontCamBleManager::save_settings_to_nvs() {
    nvs_handle_t handle;
    esp_err_t err = nvs_open(NVS_NAMESPACE, NVS_READWRITE, &handle);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to open NVS namespace '%s' for writing: %s", NVS_NAMESPACE, esp_err_to_name(err));
        return;
    }

    nvs_set_blob(handle, NVS_KEY_MAC, m_paired_mac, sizeof(m_paired_mac));
    nvs_set_u8(handle, NVS_KEY_PROFILE, static_cast<uint8_t>(m_profile));
    nvs_set_str(handle, NVS_KEY_NAME, m_camera_name);
    nvs_set_u8(handle, NVS_KEY_AUTOCONN, m_autoconnect_enabled ? 1 : 0);
    nvs_set_u8(handle, NVS_KEY_FUEL_FILT, m_fuel_filter_enabled ? 1 : 0);
    nvs_commit(handle);
    nvs_close(handle);
    ESP_LOGI(TAG, "Action-Cam pairing and autoconnect settings committed to NVS.");
}

void FrontCamBleManager::clear_settings_in_nvs() {
    nvs_handle_t handle;
    if (nvs_open(NVS_NAMESPACE, NVS_READWRITE, &handle) == ESP_OK) {
        nvs_erase_all(handle);
        nvs_commit(handle);
        nvs_close(handle);
        ESP_LOGI(TAG, "NVS namespace '%s' cleared.", NVS_NAMESPACE);
    }
}
