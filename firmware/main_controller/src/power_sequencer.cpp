#include "power_sequencer.h"
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/timers.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "uwb_vehicle_backbone.h"
#include "uwb_cartridge_dispatcher.h"

static const char *TAG = "PWR_SEQ";

static PowerSequenceStage_t s_current_stage = POWER_STAGE_STANDBY;
static TimerHandle_t s_boot_timer = NULL;
static TimerHandle_t s_shutdown_timer = NULL;
static uint32_t s_boot_step = 0;
static uint32_t s_shutdown_step = 0;

static void boot_timer_callback(TimerHandle_t xTimer) {
    s_boot_step++;
    switch (s_boot_step) {
        case 1: // T = 200 ms: Bucht 1 einschalten
            gpio_set_level(PIN_PORT1_VCC_EN, 1);
            s_current_stage = POWER_STAGE_BAY1;
            ESP_LOGI(TAG, "⚡ [T=200ms] Bucht 1 (+5V DC via TPS2051B) ACTIVE.");
            xTimerChangePeriod(s_boot_timer, pdMS_TO_TICKS(150), 0); // Weitere 150 ms bis T = 350 ms
            break;

        case 2: // T = 350 ms: Bucht 2 einschalten
            gpio_set_level(PIN_PORT2_VCC_EN, 1);
            s_current_stage = POWER_STAGE_BAY2;
            ESP_LOGI(TAG, "⚡ [T=350ms] Bucht 2 (+5V DC via TPS2051B) ACTIVE.");
            xTimerChangePeriod(s_boot_timer, pdMS_TO_TICKS(150), 0); // Weitere 150 ms bis T = 500 ms
            break;

        case 3: // T = 500 ms: Heckradar 12V einschalten
            gpio_set_level(PIN_RADAR_VCC_EN, 1);
            s_current_stage = POWER_STAGE_RADAR;
            ESP_LOGI(TAG, "⚡ [T=500ms] Heck-Radar (+12V DC via High-Side Gate) ACTIVE.");
            xTimerStop(s_boot_timer, 0);
            s_current_stage = POWER_STAGE_FULL_OPERATIONAL;
            ESP_LOGI(TAG, "✓ All vehicle peripherals staged and fully operational.");
            // Kassetten per UWB synchron hochfahren
            uwb_cartridge_power_on_all();
            break;

        default:
            xTimerStop(s_boot_timer, 0);
            break;
    }
}

static void shutdown_timer_callback(TimerHandle_t xTimer) {
    s_shutdown_step++;
    switch (s_shutdown_step) {
        case 1: // Nach 500 ms: Heck-Radar abschalten
            gpio_set_level(PIN_RADAR_VCC_EN, 0);
            ESP_LOGI(TAG, "🛑 [Shutdown Stage 1] Heck-Radar (+12V DC) powered down.");
            xTimerChangePeriod(s_shutdown_timer, pdMS_TO_TICKS(500), 0);
            break;

        case 2: // Nach weiteren 500 ms: Buchten 1 & 2 abschalten
            gpio_set_level(PIN_PORT1_VCC_EN, 0);
            gpio_set_level(PIN_PORT2_VCC_EN, 0);
            s_current_stage = POWER_STAGE_STANDBY;
            ESP_LOGI(TAG, "🛑 [Shutdown Stage 2] Buchten 1 & 2 (+5V DC) powered down.");
            xTimerStop(s_shutdown_timer, 0);
            break;

        default:
            xTimerStop(s_shutdown_timer, 0);
            break;
    }
}

esp_err_t power_sequencer_init(void) {
    ESP_LOGI(TAG, "Initializing Gestaffeltes Power-Sequencing Engine (PCBA 01)...");

    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_OUTPUT;
    io_conf.pin_bit_mask = (1ULL << PIN_PORT1_VCC_EN) | (1ULL << PIN_PORT2_VCC_EN) | (1ULL << PIN_RADAR_VCC_EN);
    io_conf.pull_down_en = GPIO_PULLDOWN_ENABLE;
    io_conf.pull_up_en = GPIO_PULLUP_DISABLE;
    gpio_config(&io_conf);

    // Initial alle Lastschalter gesperrt
    gpio_set_level(PIN_PORT1_VCC_EN, 0);
    gpio_set_level(PIN_PORT2_VCC_EN, 0);
    gpio_set_level(PIN_RADAR_VCC_EN, 0);

    s_boot_timer = xTimerCreate("PwrSeqBoot", pdMS_TO_TICKS(200), pdFALSE, NULL, boot_timer_callback);
    s_shutdown_timer = xTimerCreate("PwrSeqOff", pdMS_TO_TICKS(500), pdFALSE, NULL, shutdown_timer_callback);

    if (!s_boot_timer || !s_shutdown_timer) {
        ESP_LOGE(TAG, "Failed to create FreeRTOS Power-Sequencing Timers.");
        return ESP_ERR_NO_MEM;
    }

    s_current_stage = POWER_STAGE_STANDBY;
    return ESP_OK;
}

void power_sequencer_trigger_boot(void) {
    ESP_LOGI(TAG, "⚡ [T=0ms] Ignition ON detected. Central Box & Front Node running. Starting peripheral cascade...");
    s_current_stage = POWER_STAGE_CORE_BOOT;
    s_boot_step = 0;

    // Shutdown-Timer stoppen falls aktiv
    if (s_shutdown_timer && xTimerIsTimerActive(s_shutdown_timer)) {
        xTimerStop(s_shutdown_timer, 0);
    }

    // Erster Schritt nach 200 ms (Bucht 1)
    if (s_boot_timer) {
        xTimerChangePeriod(s_boot_timer, pdMS_TO_TICKS(200), 0);
        xTimerStart(s_boot_timer, 0);
    }
}

void power_sequencer_trigger_shutdown(void) {
    ESP_LOGI(TAG, "🛑 Ignition OFF detected. Initiating graceful shutdown cascade...");
    s_shutdown_step = 0;

    // Boot-Timer abbrechen falls noch lief
    if (s_boot_timer && xTimerIsTimerActive(s_boot_timer)) {
        xTimerStop(s_boot_timer, 0);
    }

    // Sofort Kassetten sauber per UWB herunterfahren
    uwb_cartridge_power_off_all();

    // Gestaffelte DC-Abschaltung starten (Radar nach 500 ms, Buchten nach weiteren 500 ms)
    if (s_shutdown_timer) {
        xTimerChangePeriod(s_shutdown_timer, pdMS_TO_TICKS(500), 0);
        xTimerStart(s_shutdown_timer, 0);
    }
}

PowerSequenceStage_t power_sequencer_get_stage(void) {
    return s_current_stage;
}

bool power_sequencer_is_fully_powered(void) {
    return (s_current_stage == POWER_STAGE_FULL_OPERATIONAL);
}

void power_sequencer_set_bay1_power(bool enable) {
    gpio_set_level(PIN_PORT1_VCC_EN, enable ? 1 : 0);
    ESP_LOGI(TAG, "Manual Power Switch Bay 1: %s", enable ? "ON" : "OFF");
}

void power_sequencer_set_bay2_power(bool enable) {
    gpio_set_level(PIN_PORT2_VCC_EN, enable ? 1 : 0);
    ESP_LOGI(TAG, "Manual Power Switch Bay 2: %s", enable ? "ON" : "OFF");
}

void power_sequencer_set_radar_power(bool enable) {
    gpio_set_level(PIN_RADAR_VCC_EN, enable ? 1 : 0);
    ESP_LOGI(TAG, "Manual Power Switch Radar: %s", enable ? "ON" : "OFF");
}
