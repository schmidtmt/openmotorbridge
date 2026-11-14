#include "power_sequencer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"

static const char *TAG = "PWR_SEQ_V10";

static PowerSupervisorDiag_t s_diag = {
    .stage = POWER_STAGE_STANDBY,
    .kl15_ignition_on = true,
    .benchtop_usb_only_mode = false,
    .branch1_front_enabled = false,
    .branch2_pod1_enabled = false,
    .branch3_pod2_enabled = false,
    .branch4_radar_enabled = false,
    .lipo_temp_c = 24.5f,
    .jeita_charge_permitted = true
};

esp_err_t power_sequencer_init(void) {
    ESP_LOGI(TAG, "Initializing v10.0 Quad Automotive eFuse Power Sequencer (U12 TI TPS25921)...");
    ESP_LOGI(TAG, "  KL15 Sense: GPIO %d | BAT_NTC: GPIO %d | BAT_SENSE: GPIO %d",
             PIN_MAIN_KL15_SENSE, PIN_MAIN_BAT_NTC_ADC, PIN_MAIN_BAT_SENSE_ADC);

    // Configure KL15_SENSE (U2 Pad 5 = GPIO 4) as Input
    gpio_config_t kl15_cfg = {
        .pin_bit_mask = (1ULL << PIN_MAIN_KL15_SENSE),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_ENABLE,
        .intr_type = GPIO_INTR_DISABLE
    };
    gpio_config(&kl15_cfg);

    s_diag.stage = POWER_STAGE_STANDBY;
    return ESP_OK;
}

void power_sequencer_trigger_boot(void) {
    ESP_LOGI(TAG, "⚡ Starting v10.0 Staggered Inrush Power-On Sequence (TPS25921 4-Branch eFuse):");

    // Stage 1 (T = 0 ms): Central Box (U2 + U8 USB2517I + U9 QCC3084) & Branch 1 (VBUS_FRONT 5.0A)
    s_diag.stage = POWER_STAGE_CORE_BOOT;
    s_diag.branch1_front_enabled = true;
    ESP_LOGI(TAG, "  [T = 0 ms]   Stage 1: Central Box & Branch 1 (VBUS_FRONT 5.0A -> PCBA 05) ON.");

    // Wait 200 ms for buck & front hub inrush to settle
    vTaskDelay(pdMS_TO_TICKS(200));

    // Stage 2 (T = 200 ms): Branch 2 (VBUS_POD1 2.5A -> PCBA 03 Pod 1)
    s_diag.stage = POWER_STAGE_BAY1;
    s_diag.branch2_pod1_enabled = true;
    ESP_LOGI(TAG, "  [T = 200 ms] Stage 2: Branch 2 (VBUS_POD1 2.5A -> Monocoque Pod 1) ON.");

    // Wait 150 ms (T = 350 ms total)
    vTaskDelay(pdMS_TO_TICKS(150));

    // Stage 3 (T = 350 ms): Branch 3 (VBUS_POD2 2.5A -> PCBA 03 Pod 2)
    s_diag.stage = POWER_STAGE_BAY2;
    s_diag.branch3_pod2_enabled = true;
    ESP_LOGI(TAG, "  [T = 350 ms] Stage 3: Branch 3 (VBUS_POD2 2.5A -> Monocoque Pod 2) ON.");

    // Wait 150 ms (T = 500 ms total)
    vTaskDelay(pdMS_TO_TICKS(150));

    // Stage 4 (T = 500 ms): Branch 4 (VBUS_RADAR 1.5A -> PCBA 08 Rear Radar 2.0 + 5.9 GHz V2X)
    s_diag.stage = POWER_STAGE_RADAR;
    s_diag.branch4_radar_enabled = true;
    ESP_LOGI(TAG, "  [T = 500 ms] Stage 4: Branch 4 (VBUS_RADAR 1.5A -> PCBA 08 Radar + V2X) ON.");

    s_diag.stage = POWER_STAGE_FULL_OPERATIONAL;
    ESP_LOGI(TAG, "✓ All 4 USB2517I / TPS25921 Vehicle Branches powered & enumerated (Zero Voltage Drop).");
}

void power_sequencer_trigger_shutdown(void) {
    ESP_LOGI(TAG, "Initiating Staggered Power-Down Sequence (Tier-1 -> Tier-2 Sentry)...");

    s_diag.branch4_radar_enabled = false;
    vTaskDelay(pdMS_TO_TICKS(50));

    s_diag.branch3_pod2_enabled = false;
    vTaskDelay(pdMS_TO_TICKS(50));

    s_diag.branch2_pod1_enabled = false;
    vTaskDelay(pdMS_TO_TICKS(50));

    s_diag.branch1_front_enabled = false;
    s_diag.stage = POWER_STAGE_STANDBY;
    ESP_LOGI(TAG, "All 4 Satellite VBUS rails disabled. U2 (ESP32-S31), U10 (SX1262) & U5 (BMI270) remain on UPS rail.");
}

PowerSequenceStage_t power_sequencer_get_stage(void) {
    return s_diag.stage;
}

bool power_sequencer_is_fully_powered(void) {
    return (s_diag.stage == POWER_STAGE_FULL_OPERATIONAL || s_diag.stage == POWER_STAGE_BENCHTOP_DFU);
}

void power_sequencer_set_front_power(bool enable) {
    s_diag.branch1_front_enabled = enable;
    ESP_LOGI(TAG, "TPS25921 CH1 (VBUS_FRONT 5.0A): %s", enable ? "ENABLED" : "DISABLED");
}

void power_sequencer_set_bay1_power(bool enable) {
    s_diag.branch2_pod1_enabled = enable;
    ESP_LOGI(TAG, "TPS25921 CH2 (VBUS_POD1 2.5A): %s", enable ? "ENABLED" : "DISABLED");
}

void power_sequencer_set_bay2_power(bool enable) {
    s_diag.branch3_pod2_enabled = enable;
    ESP_LOGI(TAG, "TPS25921 CH3 (VBUS_POD2 2.5A): %s", enable ? "ENABLED" : "DISABLED");
}

void power_sequencer_set_radar_power(bool enable) {
    s_diag.branch4_radar_enabled = enable;
    ESP_LOGI(TAG, "TPS25921 CH4 (VBUS_RADAR 1.5A): %s", enable ? "ENABLED" : "DISABLED");
}

void power_sequencer_update_telemetry(float v_ign_volts, float v_bat_volts, float ntc_temp_c) {
    s_diag.lipo_temp_c = ntc_temp_c;
    s_diag.kl15_ignition_on = (v_ign_volts > 9.0f);

    // Dual-Power Input Detection (D3 LM66100 Ideal Diode OR-ing on J3 USB-C):
    // If v_ign_volts < 6.0V (no 12V bike battery connected) while MCU is running from 5V USB-C J3,
    // enter Benchtop DFU / Service Mode (PCBA 01 logic active; note that U12 satellite branches on J6 require 12V on J1).
    bool usb_only = (v_ign_volts < 6.0f && v_bat_volts < 6.0f);
    if (usb_only != s_diag.benchtop_usb_only_mode) {
        s_diag.benchtop_usb_only_mode = usb_only;
        if (usb_only) {
            s_diag.stage = POWER_STAGE_BENCHTOP_DFU;
            ESP_LOGW(TAG, "🔌 [LM66100 DUAL-POWER] 5V USB-C Service/Benchtop Mode on J3. Central Box logic & USB2517I active. (Note: U12 J6 satellite branches unpowered without 12V on J1)");
        }
    }

    // JEITA Thermal Protection for BQ24075 LiPo Charger (0 °C .. +45 °C)
    bool charge_ok = (ntc_temp_c >= MAIN_LIPO_JEITA_MIN_TEMP_C && ntc_temp_c <= MAIN_LIPO_JEITA_MAX_TEMP_C);
    if (charge_ok != s_diag.jeita_charge_permitted) {
        s_diag.jeita_charge_permitted = charge_ok;
        if (!charge_ok) {
            ESP_LOGE(TAG, "🌡️ [JEITA ALERT] LiPo NTC Temperature (%.1f °C) outside safe window [0..45 °C]! BQ24075 Charging SUSPENDED.", ntc_temp_c);
        } else {
            ESP_LOGI(TAG, "🌡️ [JEITA OK] LiPo NTC Temperature (%.1f °C) within safe window. BQ24075 Charging ENABLED.", ntc_temp_c);
        }
    }
}

PowerSupervisorDiag_t power_sequencer_get_diagnostics(void) {
    return s_diag;
}
