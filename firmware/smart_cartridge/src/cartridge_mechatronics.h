#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

// Actuator Bitmask Flags
#define ACT_MASK_PLUS     (1 << 0)
#define ACT_MASK_MINUS    (1 << 1)
#define ACT_MASK_CENTER   (1 << 2)
#define ACT_MASK_MESH     (1 << 3)

class CartridgeMechatronics {
public:
    static CartridgeMechatronics& instance();

    esp_err_t init();

    // Direct hardware pulse (non-blocking)
    esp_err_t trigger_pulse(uint8_t actuator_mask, uint16_t duration_ms);

    // Standardized Opcode execution (interprets macro / profile timing)
    esp_err_t execute_opcode(uint8_t opcode, uint16_t param_duration_ms = 0);

    // Periodic state machine update (called in supervisor or timer)
    void update();

    bool is_busy() const { return m_busy; }
    uint8_t get_active_mask() const { return m_active_mask; }

private:
    CartridgeMechatronics();
    ~CartridgeMechatronics() = default;

    void set_actuators_raw(uint8_t mask);

    bool m_busy;
    uint8_t m_active_mask;
    uint32_t m_pulse_end_ms;

    // Macro step sequencing for Channel +/- (2x Mesh, 1x Plus/Minus)
    uint8_t m_macro_step;
    uint8_t m_macro_type;
    uint32_t m_macro_next_action_ms;
};
