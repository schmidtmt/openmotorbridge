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
    void update(uint32_t delta_ms); // Call at 20-50 Hz from supervisor task

    // --- 1. CAN Auto-Sensing 120-Ohm Termination ---
    void perform_can_auto_sense(void);
    void set_can_termination(bool enable);
    bool is_can_termination_active(void) const { return m_can_term_active; }

    // --- 2. Mirror BSD (Blind-Spot Detection) Warning LEDs ---
    void set_bsd_warning(bool left_active, BsdAlertLevel left_level,
                         bool right_active, BsdAlertLevel right_level);
    bool is_bsd_left_active(void) const { return m_bsd_left_level != BSD_LEVEL_OFF; }
    bool is_bsd_right_active(void) const { return m_bsd_right_level != BSD_LEVEL_OFF; }

    // --- 3. 12V Aux Light (TPS1H100 Smart High-Side Switch) ---
    void set_aux_light_mode(AuxLightMode mode);
    AuxLightMode get_aux_light_mode(void) const { return m_aux_light_mode; }
    bool is_aux_light_on(void) const { return m_aux_light_mode != AUX_LIGHT_OFF; }

    // --- 4. KL15 Ignition & Qi-Power Status ---
    bool is_kl15_ignition_on(void);
    bool is_qi_power_active(void) const { return m_qi_power_active; }

    // --- 5. CAN Silent (Listen-Only) Mode ---
    void set_can_silent(bool silent);

private:
    CockpitSwitchesManager();
    ~CockpitSwitchesManager() = default;

    CockpitSwitchesManager(const CockpitSwitchesManager&) = delete;
    CockpitSwitchesManager& operator=(const CockpitSwitchesManager&) = delete;

    bool m_can_term_active;
    bool m_can_silent;
    bool m_qi_power_active;

    // BSD State
    BsdAlertLevel m_bsd_left_level;
    BsdAlertLevel m_bsd_right_level;
    uint32_t m_bsd_strobe_timer_ms;
    bool m_bsd_strobe_state; // Toggles at 8 Hz

    // Aux Light State
    AuxLightMode m_aux_light_mode;
    uint32_t m_aux_strobe_timer_ms;
    bool m_aux_strobe_state; // Toggles at 4 Hz
};
