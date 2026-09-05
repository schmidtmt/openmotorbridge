#pragma once

#include <stdbool.h>
#include <stdint.h>
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"
#include "front_node_config.h"

struct PttEvent {
    bool pressed;          // true = Pressed (Key Down), false = Released (Key Up)
    uint64_t timestamp_us; // High-precision microsecond hardware timestamp
};

// Callback for high-level multi-click actions (single, double, long-press)
typedef void (*PttActionCallback)(PttClickType click_type);

class HandlebarPttHandler {
public:
    static HandlebarPttHandler& instance();

    bool init();
    void set_action_callback(PttActionCallback cb);

    // Raw fast event polling (for zero-latency ESP-NOW forwarding <0.9ms)
    bool get_event(PttEvent* evt, TickType_t wait_ticks);
    bool is_pressed() const;

    // Multi-click state machine update (called periodically by supervisor or PTT task)
    void update();

private:
    HandlebarPttHandler();
    static void IRAM_ATTR isr_handler(void* arg);

    QueueHandle_t m_event_queue;
    volatile bool m_is_pressed;
    volatile uint64_t m_last_edge_us;

    // Multi-click state tracking
    PttActionCallback m_action_cb;
    uint64_t m_press_start_us;
    uint64_t m_release_time_us;
    uint8_t  m_click_count;
    bool     m_long_press_fired;
    bool     m_reset_hold_fired;
};

