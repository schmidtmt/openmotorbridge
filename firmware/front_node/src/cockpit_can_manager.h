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

class CockpitCanManager {
public:
    static CockpitCanManager& instance();

    bool init(uint32_t baud_rate_kbps = 250);
    bool receive_message(CanMessage* msg, TickType_t wait_ticks);
    bool transmit_message(const CanMessage& msg);
    bool is_bus_healthy() const;

private:
    CockpitCanManager();

    bool m_installed;
    bool m_bus_ok;
};
