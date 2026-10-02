#include "cartridge_mechatronics.h"
#include "cartridge_config.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "uwb_backbone_types.h"

static const char* TAG = "CARTRIDGE_MECH";

CartridgeMechatronics& CartridgeMechatronics::instance() {
    static CartridgeMechatronics s_instance;
    return s_instance;
}

CartridgeMechatronics::CartridgeMechatronics()
    : m_busy(false),
      m_active_mask(0),
      m_pulse_end_ms(0),
      m_macro_step(0),
      m_macro_type(0),
      m_macro_next_action_ms(0) {
}

esp_err_t CartridgeMechatronics::init() {
    ESP_LOGI(TAG, "Initializing Mechatronics Actuator Gates (Q1-Q4 AO3400A)...");

    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_OUTPUT;
    io_conf.pin_bit_mask = (1ULL << PIN_ACT1_PLUS) |
                           (1ULL << PIN_ACT2_MINUS) |
                           (1ULL << PIN_ACT3_CENTER) |
                           (1ULL << PIN_ACT4_MESH) |
                           (1ULL << PIN_CARTRIDGE_LED);
    io_conf.pull_down_en = GPIO_PULLDOWN_ENABLE;
    io_conf.pull_up_en = GPIO_PULLUP_DISABLE;
    gpio_config(&io_conf);

    // Initial safe state: All gates 0V
    set_actuators_raw(0);
    gpio_set_level(PIN_CARTRIDGE_LED, 0);

    return ESP_OK;
}

void CartridgeMechatronics::set_actuators_raw(uint8_t mask) {
    gpio_set_level(PIN_ACT1_PLUS,   (mask & ACT_MASK_PLUS)   ? 1 : 0);
    gpio_set_level(PIN_ACT2_MINUS,  (mask & ACT_MASK_MINUS)  ? 1 : 0);
    gpio_set_level(PIN_ACT3_CENTER, (mask & ACT_MASK_CENTER) ? 1 : 0);
    gpio_set_level(PIN_ACT4_MESH,   (mask & ACT_MASK_MESH)   ? 1 : 0);
    gpio_set_level(PIN_CARTRIDGE_LED, mask != 0 ? 1 : 0);
    m_active_mask = mask;
}

esp_err_t CartridgeMechatronics::trigger_pulse(uint8_t actuator_mask, uint16_t duration_ms) {
    if (duration_ms == 0) {
        set_actuators_raw(0);
        m_busy = false;
        return ESP_OK;
    }

    uint32_t now_ms = (uint32_t)(esp_timer_get_time() / 1000ULL);
    set_actuators_raw(actuator_mask);
    m_pulse_end_ms = now_ms + duration_ms;
    m_busy = true;

    ESP_LOGD(TAG, "Pulse triggered: Mask 0x%02X for %u ms (End: %lu ms)",
             actuator_mask, duration_ms, (unsigned long)m_pulse_end_ms);
    return ESP_OK;
}

esp_err_t CartridgeMechatronics::execute_opcode(uint8_t opcode, uint16_t param_duration_ms) {
    ESP_LOGI(TAG, "Executing Cartridge Opcode 0x%02X (Param: %u ms)", opcode, param_duration_ms);

    switch (opcode) {
        case CARTRIDGE_OPCODE_POWER_BOOT: // 0x01: Center + Plus 1000 ms
            return trigger_pulse(ACT_MASK_CENTER | ACT_MASK_PLUS, param_duration_ms > 0 ? param_duration_ms : 1000);

        case CARTRIDGE_OPCODE_POWER_OFF:  // 0x02: Center + Plus 200 ms
            return trigger_pulse(ACT_MASK_CENTER | ACT_MASK_PLUS, param_duration_ms > 0 ? param_duration_ms : 200);

        case CARTRIDGE_OPCODE_VOLUME_UP:  // 0x03: Plus 100 ms
            return trigger_pulse(ACT_MASK_PLUS, param_duration_ms > 0 ? param_duration_ms : 100);

        case CARTRIDGE_OPCODE_VOLUME_DOWN:// 0x04: Minus 100 ms
            return trigger_pulse(ACT_MASK_MINUS, param_duration_ms > 0 ? param_duration_ms : 100);

        case CARTRIDGE_OPCODE_MESH_TOGGLE:// 0x05: Mesh 200 ms
            return trigger_pulse(ACT_MASK_MESH, param_duration_ms > 0 ? param_duration_ms : 200);

        case CARTRIDGE_OPCODE_OPEN_GROUP_SW:// 0x06: Mesh 3000 ms
            return trigger_pulse(ACT_MASK_MESH, param_duration_ms > 0 ? param_duration_ms : 3000);

        case CARTRIDGE_OPCODE_CHANNEL_NEXT: // 0x07: Macro 2x Mesh, 1x Plus
        case CARTRIDGE_OPCODE_CHANNEL_PREV: // 0x08: Macro 2x Mesh, 1x Minus
            m_macro_type = opcode;
            m_macro_step = 1;
            trigger_pulse(ACT_MASK_MESH, 150); // Click 1
            m_macro_next_action_ms = (uint32_t)(esp_timer_get_time() / 1000ULL) + 350; // 150 ms pulse + 200 ms gap
            return ESP_OK;

        case CARTRIDGE_OPCODE_CUSTOM_PULSE: // 0x0F: Parametric pulse
            return trigger_pulse((uint8_t)(param_duration_ms >> 12) & 0x0F, param_duration_ms & 0x0FFF);

        default:
            ESP_LOGW(TAG, "Unknown Cartridge Opcode 0x%02X", opcode);
            return ESP_ERR_NOT_SUPPORTED;
    }
}

void CartridgeMechatronics::update() {
    uint32_t now_ms = (uint32_t)(esp_timer_get_time() / 1000ULL);

    // 1. Check active pulse expiration
    if (m_busy && m_active_mask != 0) {
        if (now_ms >= m_pulse_end_ms) {
            set_actuators_raw(0);
            if (m_macro_step == 0) {
                m_busy = false;
            }
        }
    }

    // 2. Advance Macro Sequencer for Channel Next / Prev
    if (m_macro_step > 0 && now_ms >= m_macro_next_action_ms) {
        if (m_macro_step == 1) {
            // Click 2: Mesh 150 ms
            m_macro_step = 2;
            trigger_pulse(ACT_MASK_MESH, 150);
            m_macro_next_action_ms = now_ms + 350; // 150 ms pulse + 200 ms gap
        } else if (m_macro_step == 2) {
            // Click 3: Plus or Minus 150 ms
            m_macro_step = 3;
            uint8_t dir_mask = (m_macro_type == CARTRIDGE_OPCODE_CHANNEL_NEXT) ? ACT_MASK_PLUS : ACT_MASK_MINUS;
            trigger_pulse(dir_mask, 150);
            m_macro_next_action_ms = now_ms + 200;
        } else {
            // Macro complete
            m_macro_step = 0;
            m_macro_type = 0;
            m_busy = false;
            ESP_LOGI(TAG, "Macro sequence completed.");
        }
    }
}
