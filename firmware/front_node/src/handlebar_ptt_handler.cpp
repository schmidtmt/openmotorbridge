#include "handlebar_ptt_handler.h"
#include "front_node_config.h"
#include "esp_timer.h"
#include "esp_log.h"
#include "driver/gpio.h"

static const char* TAG = "PTT_HANDLER";

HandlebarPttHandler& HandlebarPttHandler::instance() {
    static HandlebarPttHandler inst;
    return inst;
}

HandlebarPttHandler::HandlebarPttHandler()
    : m_event_queue(nullptr)
    , m_is_pressed(false)
    , m_last_edge_us(0)
{
}

void IRAM_ATTR HandlebarPttHandler::isr_handler(void* arg) {
    HandlebarPttHandler* self = static_cast<HandlebarPttHandler*>(arg);
    uint64_t now = esp_timer_get_time();
    
    // Hardware-assisted microsecond debounce check
    if ((now - self->m_last_edge_us) < (PTT_DEBOUNCE_MS * 1000ULL)) {
        return;
    }
    self->m_last_edge_us = now;

    // Pin is active-low (0 = Pressed, 1 = Released)
    int level = gpio_get_level(PIN_PTT_INPUT_N);
    bool pressed = (level == 0);
    self->m_is_pressed = pressed;

    PttEvent evt = {
        .pressed = pressed,
        .timestamp_us = now
    };

    BaseType_t high_task_woken = pdFALSE;
    if (self->m_event_queue) {
        xQueueSendFromISR(self->m_event_queue, &evt, &high_task_woken);
    }

    if (high_task_woken == pdTRUE) {
        portYIELD_FROM_ISR();
    }
}

bool HandlebarPttHandler::init() {
    m_event_queue = xQueueCreate(16, sizeof(PttEvent));
    if (!m_event_queue) {
        ESP_LOGE(TAG, "Failed to allocate PTT event queue");
        return false;
    }

    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << PIN_PTT_INPUT_N),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE, // Internal pullup backup to external 10k resistor
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_ANYEDGE,    // Trigger on both press and release
    };

    esp_err_t err = gpio_config(&io_conf);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "gpio_config failed: %s", esp_err_to_name(err));
        return false;
    }

    // Read initial state
    m_is_pressed = (gpio_get_level(PIN_PTT_INPUT_N) == 0);

    // Install ISR service if not already present
    gpio_install_isr_service(ESP_INTR_FLAG_IRAM);
    err = gpio_isr_handler_add(PIN_PTT_INPUT_N, isr_handler, this);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "gpio_isr_handler_add failed: %s", esp_err_to_name(err));
        return false;
    }

    ESP_LOGI(TAG, "Handlebar PTT driver initialized (GPIO0, Active-Low, Interrupt-Driven). Initial: %s",
             m_is_pressed ? "PRESSED" : "RELEASED");
    return true;
}

bool HandlebarPttHandler::get_event(PttEvent* evt, TickType_t wait_ticks) {
    if (!m_event_queue || !evt) return false;
    return (xQueueReceive(m_event_queue, evt, wait_ticks) == pdTRUE);
}

bool HandlebarPttHandler::is_pressed() const {
    return m_is_pressed;
}
