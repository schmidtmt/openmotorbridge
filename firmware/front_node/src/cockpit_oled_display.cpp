#include "cockpit_oled_display.h"
#include "front_node_config.h"
#include "driver/i2c.h"
#include "esp_log.h"
#include <string.h>

static const char *TAG = "COCKPIT_OLED";
#define OLED_I2C_PORT I2C_NUM_0

CockpitOledDisplay& CockpitOledDisplay::instance() {
    static CockpitOledDisplay s_instance;
    return s_instance;
}

CockpitOledDisplay::CockpitOledDisplay()
    : m_initialized(false),
      m_contrast_reg(0xCF),
      m_hud{} {
}

esp_err_t CockpitOledDisplay::send_oled_cmd(uint8_t i2c_addr, uint8_t cmd) {
    uint8_t buf[2] = { 0x00 /* Control Byte: Command */, cmd };
    return i2c_master_write_to_device(OLED_I2C_PORT, i2c_addr, buf, sizeof(buf), pdMS_TO_TICKS(15));
}

esp_err_t CockpitOledDisplay::init() {
    ESP_LOGI(TAG, "Initializing Dual Cockpit Speaker-Corner OLED Displays (J_DISP_L=0x%02X, J_DISP_R=0x%02X)...",
             I2C_ADDR_OLED_LEFT, I2C_ADDR_OLED_RIGHT);

    static const uint8_t ssd1306_init_seq[] = {
        0xAE,       // Display OFF
        0xD5, 0x80, // Clock divide ratio
        0xA8, 0x3F, // Multiplex 1/64
        0xD3, 0x00, // Display offset 0
        0x40,       // Start line 0
        0x8D, 0x14, // Charge pump ON
        0x20, 0x00, // Horizontal addressing mode
        0xA1,       // Segment remap
        0xC8,       // COM scan direction
        0xDA, 0x12, // COM pins hardware config
        0x81, 0xCF, // Contrast control
        0xD9, 0xF1, // Pre-charge period
        0xDB, 0x40, // VCOMH deselect level
        0xA4,       // Entire display ON from RAM
        0xA6,       // Normal display
        0xAF        // Display ON
    };

    for (size_t i = 0; i < sizeof(ssd1306_init_seq); i++) {
        send_oled_cmd(I2C_ADDR_OLED_LEFT, ssd1306_init_seq[i]);
        send_oled_cmd(I2C_ADDR_OLED_RIGHT, ssd1306_init_seq[i]);
    }

    m_initialized = true;
    ESP_LOGI(TAG, "✓ Dual Cockpit Speaker-Corner OLEDs (J_DISP_L & J_DISP_R) active (Radar BSD + 5.9 GHz V2X GLOSA HUD).");
    return ESP_OK;
}

void CockpitOledDisplay::update_hud_state(const UsbCockpitHudStatePkt& hud_pkt) {
    m_hud = hud_pkt;
    ESP_LOGD(TAG, "OLED HUD Update: L_BSD=%u, R_BSD=%u, Dist=%.1fm, GLOSA=%u (%u km/h, %us), Status='%s'",
             m_hud.left_threat_level, m_hud.right_threat_level,
             m_hud.closest_rear_dist_m / 10.0f,
             m_hud.glosa_active, m_hud.glosa_rec_speed_kph, m_hud.glosa_countdown_s,
             m_hud.status_line);
}

void CockpitOledDisplay::update_ambient_brightness(uint32_t ambient_lux) {
    // Map OPT3001 ambient lux (0 .. 50,000+ Lux) to SSD1306 contrast register (0x08 Night .. 0xFF Direct Sun)
    uint8_t target_contrast = 0xCF;
    if (ambient_lux < 15) {
        target_contrast = 0x10; // Night / Tunnel glare-free mode
    } else if (ambient_lux < 300) {
        target_contrast = 0x7F; // Dawn / Overcast
    } else {
        target_contrast = 0xFF; // Full daylight visibility
    }

    if (target_contrast != m_contrast_reg && m_initialized) {
        m_contrast_reg = target_contrast;
        send_oled_cmd(I2C_ADDR_OLED_LEFT, 0x81);
        send_oled_cmd(I2C_ADDR_OLED_LEFT, m_contrast_reg);
        send_oled_cmd(I2C_ADDR_OLED_RIGHT, 0x81);
        send_oled_cmd(I2C_ADDR_OLED_RIGHT, m_contrast_reg);
    }
}

void CockpitOledDisplay::refresh() {
    if (!m_initialized) return;
    // Invert display on Prio-1 Collision Threat or V2X Emergency Vehicle Alert for immediate peripheral vision catch
    bool urgent_flash = (m_hud.left_threat_level >= 2 || m_hud.right_threat_level >= 2 || m_hud.v2x_hazard_type == 1);
    send_oled_cmd(I2C_ADDR_OLED_LEFT, urgent_flash ? 0xA7 : 0xA6);
}

