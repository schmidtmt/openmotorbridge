#pragma once

#include <stdbool.h>
#include <stdint.h>
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"

struct PttEvent {
    bool pressed;          // true = Pressed (Key Down), false = Released (Key Up)
    uint64_t timestamp_us; // High-precision microsecond hardware timestamp
};

class HandlebarPttHandler {
public:
    static HandlebarPttHandler& instance();

    bool init();
    bool get_event(PttEvent* evt, TickType_t wait_ticks);
    bool is_pressed() const;

private:
    HandlebarPttHandler();
    static void IRAM_ATTR isr_handler(void* arg);

    QueueHandle_t m_event_queue;
    volatile bool m_is_pressed;
    volatile uint64_t m_last_edge_us;
};
