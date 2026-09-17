#pragma once

#include <stdbool.h>
#include <stdint.h>
#include "driver/twai.h"

struct CanMessage {
    uint32_t id;
    uint8_t dlc;
    uint8_t data[8];
    bool is_extended;
};

enum CockpitCanState : uint8_t {
    CAN_STATE_AUTO_SENSING = 0, // Sniffing bus in Listen-Only mode (2.5s window)
    CAN_STATE_CONNECTED    = 1, // Active CAN traffic detected on J2 (Fairing bikes)
    CAN_STATE_DEACTIVATED  = 2  // No CAN bus detected on J2 (Road King / Adventure bikes)
};

class CockpitCanManager {
public:
    static CockpitCanManager& instance();

    bool init(uint32_t baud_rate_kbps = 250);
    void update(uint32_t delta_ms);
    bool receive_message(CanMessage* msg, TickType_t wait_ticks);
    bool transmit_message(const CanMessage& msg);
    bool is_bus_healthy() const;
    bool is_bus_connected() const { return m_state == CAN_STATE_CONNECTED; }
    CockpitCanState get_state() const { return m_state; }

private:
    CockpitCanManager();

    bool m_installed;
    bool m_bus_ok;
    CockpitCanState m_state;
    uint32_t m_auto_sense_timer_ms;
    uint32_t m_rx_count;
    uint32_t m_baud_rate_kbps;
};
