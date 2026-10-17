#include "drv2605l_haptics.h"
#include "keyfob_config.h"
#include <stdio.h>
#include <string.h>

#define REG_STATUS          0x00
#define REG_MODE            0x01
#define REG_RTP_IN          0x02
#define REG_LIBRARY         0x03
#define REG_WAVEFORM_SEQ1   0x04
#define REG_WAVEFORM_SEQ2   0x05
#define REG_WAVEFORM_SEQ3   0x06
#define REG_GO              0x0C
#define REG_FEEDBACK_CTRL   0x1A
#define REG_CONTROL1        0x1B
#define REG_CONTROL2        0x1C
#define REG_CONTROL3        0x1D

// Standard ROM waveform IDs from TI DRV2605L Library 6 (LRA)
#define LRA_STRONG_CLICK_100    1   // Crisp click 100%
#define LRA_SHARP_CLICK_100     4   // Sharp click
#define LRA_SOFT_BUMP_100       7   // Soft bump
#define LRA_DOUBLE_CLICK_100    10  // Double click 100%
#define LRA_TRIPLE_CLICK_100    12  // Triple click 100%
#define LRA_ALERT_750MS         47  // Long alert pulse
#define LRA_BUZZ_100            14  // High priority buzz

Drv2605lHaptics& Drv2605lHaptics::instance() {
    static Drv2605lHaptics s_instance;
    return s_instance;
}

Drv2605lHaptics::Drv2605lHaptics()
    : m_initialized(false), m_busy(false) {}

bool Drv2605lHaptics::write_register(uint8_t reg, uint8_t val) {
    // Hardware I2C write abstraction to KEYFOB_DRV2605_I2C_ADDR (0x5A)
    (void)reg;
    (void)val;
    return true;
}

uint8_t Drv2605lHaptics::read_register(uint8_t reg) {
    (void)reg;
    return 0x00;
}

void Drv2605lHaptics::set_enabled(bool enable) {
    // Controls KEYFOB_PIN_DRV_EN (Pad M2)
    (void)enable;
}

bool Drv2605lHaptics::init() {
    set_enabled(true);

    // 1. Take out of standby mode
    write_register(REG_MODE, 0x00); // Internal Trigger Mode

    // 2. Select Library 6 (LRA Optimized Library for Vybronics 10x3.6mm Actuator)
    write_register(REG_LIBRARY, 0x06);

    // 3. Configure Feedback Control: Set N_ERM_LRA = 1 (LRA Mode)
    write_register(REG_FEEDBACK_CTRL, 0xB6); // Closed-loop LRA, auto-resonance tracking

    // 4. Configure Control3 (Closed loop, auto calibration defaults)
    write_register(REG_CONTROL3, 0xA0);

    m_initialized = true;
    return true;
}

void Drv2605lHaptics::play_effect(KeyfobHapticEffect effect) {
    if (!m_initialized) return;

    uint8_t seq1 = 0, seq2 = 0, seq3 = 0;

    switch (effect) {
        case HAPTIC_CLICK_CONFIRM:
            // Double click: Confirm arming bike
            seq1 = LRA_DOUBLE_CLICK_100;
            break;

        case HAPTIC_CLICK_DISARM:
            // Single soft bump: Disarm bike
            seq1 = LRA_SOFT_BUMP_100;
            break;

        case HAPTIC_ALARM_PULSE:
            // High intensity continuous pulsing: Silent Pager Theft Alarm
            seq1 = LRA_ALERT_750MS;
            seq2 = LRA_BUZZ_100;
            break;

        case HAPTIC_SOS_PANIC:
            // Triple strong alert: Emergency SOS
            seq1 = LRA_TRIPLE_CLICK_100;
            seq2 = LRA_ALERT_750MS;
            break;

        case HAPTIC_BATTERY_LOW:
            // Low-frequency warning rumble
            seq1 = LRA_SOFT_BUMP_100;
            seq2 = LRA_SOFT_BUMP_100;
            break;
    }

    write_register(REG_WAVEFORM_SEQ1, seq1);
    write_register(REG_WAVEFORM_SEQ2, seq2);
    write_register(REG_WAVEFORM_SEQ3, seq3);

    // Trigger Playback
    write_register(REG_GO, 0x01);
    m_busy = true;
}

void Drv2605lHaptics::stop() {
    write_register(REG_GO, 0x00);
    m_busy = false;
}

bool Drv2605lHaptics::is_busy() const {
    return m_busy;
}
