#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"
#include "usb_backbone_types.h"

// =============================================================================
// OpenMotorBridge v10.0 - Dual Cockpit Speaker-Corner OLED HUD Engine (PCBA 05)
// Connectors: J_DISP_L (I2C 0x3C) & J_DISP_R (I2C 0x3D) on Pad 17/18 (I2C_SDA/SCL)
// Renders:
//   - Left OLED (0x3C):  Radar 2.0 Threat Bars, Left/Right BSD, Target Distance & V2X DENM Hazard
//   - Right OLED (0x3D): 5.9 GHz C-ITS V2X Traffic Light GLOSA (Recommended Speed & Countdown),
//                        Intercom / Group Split / Smartphone HFP Call Status
//   - Auto-Dimming:      Coupled to TI OPT3001 Ambient Lux Sensor (5% Night .. 100% Sunlight)
// =============================================================================

class CockpitOledDisplay {
public:
    static CockpitOledDisplay& instance();

    esp_err_t init();

    /**
     * @brief Empfängt ein USB_PKT_COCKPIT_HUD_STATE (0x08) Update von der Zentralbox
     */
    void update_hud_state(const UsbCockpitHudStatePkt& hud_pkt);

    /**
     * @brief Passt den OLED-Kontrast automatisch an den aktuellen OPT3001 Umgebungslichtwert an
     */
    void update_ambient_brightness(uint32_t ambient_lux);

    /**
     * @brief Periodischer Refresh der beiden Cockpit-OLEDs (10 Hz)
     */
    void refresh();

    bool is_initialized() const { return m_initialized; }

private:
    CockpitOledDisplay();

    esp_err_t send_oled_cmd(uint8_t i2c_addr, uint8_t cmd);

    bool m_initialized;
    uint8_t m_contrast_reg;
    UsbCockpitHudStatePkt m_hud;
};

