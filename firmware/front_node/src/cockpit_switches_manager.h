#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"
#include "front_node_config.h"

class CockpitSwitchesManager {
public:
    static CockpitSwitchesManager& instance() {
        static CockpitSwitchesManager s_instance;
        return s_instance;
    }

    esp_err_t init(void);
    void update(uint32_t delta_ms); // Call at 10-50 Hz from supervisor task

    // --- 1. Mirror BSD (Blind-Spot Detection) Warning LEDs (Q1 DMN63D8 -> J_POD_L / J_POD_R) ---
    void set_bsd_warning(bool left_active, BsdAlertLevel left_level,
                         bool right_active, BsdAlertLevel right_level);
    bool is_bsd_left_active(void) const { return m_bsd_left_level != BSD_LEVEL_OFF; }
    bool is_bsd_right_active(void) const { return m_bsd_right_level != BSD_LEVEL_OFF; }

    // --- 2. 12V Aux Light (Q2 TPS1H100 Smart High-Side Switch -> J_AUX_LIGHT) ---
    void set_aux_light_mode(AuxLightMode mode);
    AuxLightMode get_aux_light_mode(void) const { return m_aux_light_mode; }
    bool is_aux_light_on(void) const { return m_aux_light_mode != AUX_LIGHT_OFF; }

    // --- 3. ESP32-E22 Wi-Fi 6E Co-Processor Hardware Enable (U9 Pin 3) ---
    void set_e22_wifi6e_enable(bool enable);
    bool is_e22_wifi6e_enabled(void) const { return m_e22_enabled; }

private:
    CockpitSwitchesManager();
    ~CockpitSwitchesManager() = default;

    CockpitSwitchesManager(const CockpitSwitchesManager&) = delete;
    CockpitSwitchesManager& operator=(const CockpitSwitchesManager&) = delete;

    bool m_e22_enabled;

    // BSD State
    BsdAlertLevel m_bsd_left_level;
    BsdAlertLevel m_bsd_right_level;
    uint32_t m_bsd_strobe_timer_ms;
    bool m_bsd_strobe_state; // Toggles at 8 Hz

    // Aux Light State
    AuxLightMode m_aux_light_mode;
    uint32_t m_aux_strobe_timer_ms;
    bool m_aux_strobe_state; // Toggles at 4.5 Hz
};
