#pragma once

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include "front_node_config.h"

// Discovered BLE Camera Item during Scan
struct DiscoveredCamItem {
    uint8_t mac[6];
    int8_t rssi;
    CamProfileType profile;
    char name[32];
};

// Callback for reporting discovered cameras to ESP-NOW bridge
typedef void (*CamScanResultCallback)(const DiscoveredCamItem* item);
// Callback for reporting camera telemetry status to ESP-NOW bridge
typedef void (*CamStatusCallback)(CamState state, CamProfileType profile, uint8_t bat_pct, uint16_t sd_min, bool recording);

class FrontCamBleManager {
public:
    static FrontCamBleManager& instance();

    bool init();
    void set_scan_result_callback(CamScanResultCallback cb);
    void set_status_callback(CamStatusCallback cb);

    // Remote Commands from WebApp / Central Box
    void start_scan(uint32_t duration_sec = 10);
    void stop_scan();
    bool pair_device(const uint8_t* mac, CamProfileType profile, const char* name = nullptr);
    void unpair();

    // Shutter & Actions (Triggered by Handlebar PTT multi-click or WebApp)
    bool toggle_recording();
    bool trigger_hilight();

    // Configuration
    void set_autoconnect(bool enable);
    bool is_autoconnect_enabled() const { return m_autoconnect_enabled; }

    void set_fuel_filter(bool enable);
    bool is_fuel_filter_enabled() const { return m_fuel_filter_enabled; }

    // KL15 Vehicle Ignition Trigger (Tankpausen-Filter)
    void on_ignition_state_change(bool ignition_on);

    // Periodic Supervision / Autoconnect Loop (e.g. 5 Hz from supervisor)
    void update();

    // Status Getters
    CamState get_state() const { return m_state; }
    CamProfileType get_profile() const { return m_profile; }
    bool is_connected() const { return (m_state == CAM_STATE_CONNECTED || m_state == CAM_STATE_RECORDING); }
    bool is_recording() const { return (m_state == CAM_STATE_RECORDING); }
    uint8_t get_battery_pct() const { return m_battery_pct; }
    uint16_t get_sd_remaining_min() const { return m_sd_min_remaining; }
    const char* get_camera_name() const { return m_camera_name; }
    const uint8_t* get_paired_mac() const { return m_paired_mac; }
    bool has_paired_device() const { return m_has_paired_device; }

private:
    FrontCamBleManager();

    void load_settings_from_nvs();
    void save_settings_to_nvs();
    void clear_settings_in_nvs();

    // Protocol Specific BLE Transmissions
    bool send_gopro_command(const uint8_t* cmd, size_t len);
    bool send_insta360_command(const uint8_t* cmd, size_t len);
    bool send_dji_command(const uint8_t* cmd, size_t len);

    // Auto-detection parser during scan
    static CamProfileType detect_camera_profile(const uint8_t* adv_data, size_t adv_len, const char* name);

    CamState m_state;
    CamProfileType m_profile;
    bool m_has_paired_device;
    uint8_t m_paired_mac[6];
    char m_camera_name[32];

    uint8_t m_battery_pct;
    uint16_t m_sd_min_remaining;
    bool m_autoconnect_enabled;
    bool m_fuel_filter_enabled;
    bool m_was_recording_at_fuel_stop;

    uint32_t m_scan_timer_ticks;
    uint32_t m_reconnect_timer_ticks;
    uint32_t m_telemetry_timer_ticks;

    CamScanResultCallback m_scan_cb;
    CamStatusCallback m_status_cb;
};
