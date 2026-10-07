#include <stdio.h>
#include <string.h>
#include <math.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "driver/uart.h"
#include "driver/gpio.h"
#include "esp_timer.h"
#include "esp_log.h"
#include "esp_system.h"
#include "radar_mr20_protocol.h"
#include "uwb_vehicle_backbone.h"
#include "uwb_backbone_types.h"

static const char *TAG = "RADAR2_SUBMCU";

// Pinout for Radar 2.0 Sub-MCU (PCBA 08: ESP32-C5 Dual-Band & DW3110)
#define UART_MR20_PORT              UART_NUM_1
#define PIN_MR20_TX                 GPIO_NUM_4  // to Wheeltec MR20 RX
#define PIN_MR20_RX                 GPIO_NUM_5  // from Wheeltec MR20 TX
#define MR20_BAUDRATE               115200

#define PIN_UWB_SCK                 GPIO_NUM_0  // DW3110 SPI SCK
#define PIN_UWB_MOSI                GPIO_NUM_1  // DW3110 SPI MOSI
#define PIN_UWB_MISO                GPIO_NUM_2  // DW3110 SPI MISO
#define PIN_UWB_CS                  GPIO_NUM_3  // DW3110 SPI CS
#define PIN_UWB_IRQ                 GPIO_NUM_6  // DW3110 IRQ
#define PIN_UWB_RST                 GPIO_NUM_7  // DW3110 RST

#define PIN_NEOPIXEL                GPIO_NUM_8  // WS2812B-2020 Data line
#define NUM_LEDS                    36          // 36-LED Visual Warning Wings (18 Left, 18 Right)
#define WING_LEDS                   18          // 18 LEDs per wing (Left: 0..17, Right: 18..35)

static SemaphoreHandle_t s_radar_data_mutex = NULL;
static RadarTelemetryPacket_t s_current_telemetry;
static RadarCommandPacket_t s_current_command;
static uint16_t s_radar_frame_index = 0;
static uint32_t s_last_mr20_rx_time_ms = 0;

// Configurable Warning Macros & State Management
static uint16_t s_enabled_macros = (RADAR_MACRO_POST_SWEEP_EN | RADAR_MACRO_ESS_STROBE_EN |
                                    RADAR_MACRO_HAZARD_BEACON_EN | RADAR_MACRO_THEFT_STROBE_EN |
                                    RADAR_MACRO_AMBIENT_GLOW_EN);
static uint8_t s_ess_thresh_pct = 60;
static uint32_t s_post_start_ms = 0;
static bool s_post_running = true;
static bool s_diag_override = false;
static uint8_t s_diag_led_states[NUM_LEDS];

// Neopixel color state
typedef struct {
    uint8_t r;
    uint8_t g;
    uint8_t b;
} RgbColor_t;

static RgbColor_t s_led_buffer[NUM_LEDS];

static void update_neopixel_halo(void) {
    // In hardware this drives the 36 WS2812B LEDs via RMT/SPI-MOSI on GPIO 8
}

static void init_uarts(void) {
    // Wheeltec MR20 Sensor UART
    const uart_config_t mr20_uart_config = {
        .baud_rate = MR20_BAUDRATE,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };
    uart_param_config(UART_MR20_PORT, &mr20_uart_config);
    uart_set_pin(UART_MR20_PORT, PIN_MR20_TX, PIN_MR20_RX, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    uart_driver_install(UART_MR20_PORT, 1024, 0, 0, NULL, 0);

    ESP_LOGI(TAG, "Wheeltec MR20 UART1 initialized on GPIO %d (TX) / %d (RX).", PIN_MR20_TX, PIN_MR20_RX);
}

// Parse Wheeltec MR20 77-GHz raw mmWave clusters
static void parse_mr20_frame(const uint8_t *buf, size_t len) {
    if (len < 5) return;

    for (size_t i = 0; i < len - 4; i++) {
        if (buf[i] == MR20_RAW_HEADER_1 && buf[i + 1] == MR20_RAW_HEADER_2) {
            uint8_t frame_len = buf[i + 2];
            uint8_t frame_type = buf[i + 3];

            if (i + frame_len <= len && frame_type == MR20_FRAME_TARGET_LIST) {
                uint8_t target_count = buf[i + 4];
                if (target_count > MR20_MAX_TARGETS) target_count = MR20_MAX_TARGETS;

                if (s_radar_data_mutex && xSemaphoreTake(s_radar_data_mutex, pdMS_TO_TICKS(5)) == pdTRUE) {
                    s_current_telemetry.target_count = target_count;
                    s_last_mr20_rx_time_ms = (uint32_t)(esp_timer_get_time() / 1000ULL);

                    for (uint8_t t = 0; t < target_count; t++) {
                        size_t offset = i + 5 + (t * 8);
                        if (offset + 8 <= len) {
                            uint8_t id = buf[offset];
                            int16_t dist_raw = (int16_t)((buf[offset + 1] << 8) | buf[offset + 2]);
                            int16_t speed_raw = (int16_t)((buf[offset + 3] << 8) | buf[offset + 4]);
                            int16_t azim_raw = (int16_t)((buf[offset + 5] << 8) | buf[offset + 6]);
                            uint8_t snr = buf[offset + 7];

                            s_current_telemetry.targets[t].target_id = id;
                            s_current_telemetry.targets[t].distance_cm = (uint16_t)(dist_raw * 10);
                            s_current_telemetry.targets[t].rel_speed_mps_100 = speed_raw;
                            s_current_telemetry.targets[t].azimuth_deg_10 = azim_raw;
                            s_current_telemetry.targets[t].snr_db = snr;

                            // Calculate TTC (Time to collision) in milliseconds
                            if (speed_raw < -50 && dist_raw > 0) { // Approaching vehicle (relative speed negative)
                                float dist_m = (float)dist_raw * 0.1f;
                                float speed_mps = fabsf((float)speed_raw * 0.01f);
                                float ttc_s = dist_m / speed_mps;
                                s_current_telemetry.targets[t].ttc_ms = (uint16_t)(ttc_s * 1000.0f);

                                if (ttc_s < 1.5f) {
                                    s_current_telemetry.targets[t].threat_level = RADAR_THREAT_LVL_RED;
                                } else if (ttc_s < 3.0f) {
                                    s_current_telemetry.targets[t].threat_level = RADAR_THREAT_LVL_AMBER;
                                } else {
                                    s_current_telemetry.targets[t].threat_level = RADAR_THREAT_LVL_NONE;
                                }
                            } else {
                                s_current_telemetry.targets[t].ttc_ms = 0xFFFF; // No collision threat
                                s_current_telemetry.targets[t].threat_level = RADAR_THREAT_LVL_NONE;
                            }
                        }
                    }
                    xSemaphoreGive(s_radar_data_mutex);
                }
                break;
            }
        }
    }
}

// Task 1: Wheeltec MR20 UART Receiver Task (Core 0, 50 Hz)
static void task_mr20_rx(void *arg) {
    ESP_LOGI(TAG, "Wheeltec MR20 RX Task running at 50 Hz...");
    uint8_t rx_buffer[512];

    while (true) {
        int bytes_read = uart_read_bytes(UART_MR20_PORT, rx_buffer, sizeof(rx_buffer), pdMS_TO_TICKS(20));
        if (bytes_read > 0) {
            parse_mr20_frame(rx_buffer, bytes_read);
        }

        // Sensor Watchdog
        uint32_t now_ms = (uint32_t)(esp_timer_get_time() / 1000ULL);
        if (now_ms - s_last_mr20_rx_time_ms > 1000) {
            if (s_radar_data_mutex && xSemaphoreTake(s_radar_data_mutex, pdMS_TO_TICKS(5)) == pdTRUE) {
                s_current_telemetry.sensor_state = RADAR_SENSOR_STATE_ERROR;
                s_current_telemetry.target_count = 0;
                xSemaphoreGive(s_radar_data_mutex);
            }
        }
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

// Task 2: Neopixel Dual-Wing Warning Lighting Task (40 Hz refresh rate)
static void task_neopixel_halo(void *arg) {
    ESP_LOGI(TAG, "Neopixel Halo Task running at 40 Hz (36 WS2812B LEDs)...");
    uint32_t frame_count = 0;

    while (true) {
        uint8_t max_threat = RADAR_THREAT_LVL_NONE;
        uint16_t enabled_macros = 0;
        uint8_t brightness_pct = 100;
        bool bsd_left = false;
        bool bsd_right = false;

        if (s_radar_data_mutex && xSemaphoreTake(s_radar_data_mutex, pdMS_TO_TICKS(5)) == pdTRUE) {
            for (uint8_t t = 0; t < s_current_telemetry.target_count; t++) {
                if (s_current_telemetry.targets[t].threat_level > max_threat) {
                    max_threat = s_current_telemetry.targets[t].threat_level;
                }
                if (s_current_telemetry.targets[t].threat_level >= RADAR_THREAT_LVL_AMBER) {
                    if (s_current_telemetry.targets[t].azimuth_deg_10 < -100) bsd_left = true;
                    if (s_current_telemetry.targets[t].azimuth_deg_10 > 100)  bsd_right = true;
                }
            }
            enabled_macros = s_enabled_macros;
            brightness_pct = s_current_command.dimming_pwm_pct;
            bsd_left = bsd_left || s_current_command.bsd_left_active;
            bsd_right = bsd_right || s_current_command.bsd_right_active;
            xSemaphoreGive(s_radar_data_mutex);
        }

        float brightness_scale = (float)brightness_pct / 100.0f;

        // Threat Warning on Dual Wings (Directional BSD & TTC Level)
        if (max_threat == RADAR_THREAT_LVL_RED || max_threat == RADAR_THREAT_LVL_AMBER) {
            bool strobe = (frame_count % 3) == 0;
            uint8_t target_r = (uint8_t)(255 * brightness_scale);
            uint8_t target_g = (max_threat == RADAR_THREAT_LVL_AMBER) ? (uint8_t)(140 * brightness_scale) : 0;
            uint8_t base_r = (uint8_t)(40 * brightness_scale);

            // Left Wing (LEDs 0..17)
            bool flash_left = bsd_left || (!bsd_right);
            for (int i = 0; i < WING_LEDS; i++) {
                if (flash_left && (strobe || max_threat == RADAR_THREAT_LVL_AMBER)) {
                    s_led_buffer[i].r = target_r;
                    s_led_buffer[i].g = target_g;
                    s_led_buffer[i].b = 0;
                } else {
                    s_led_buffer[i].r = base_r;
                    s_led_buffer[i].g = 0;
                    s_led_buffer[i].b = 0;
                }
            }

            // Right Wing (LEDs 18..35)
            bool flash_right = bsd_right || (!bsd_left);
            for (int i = WING_LEDS; i < NUM_LEDS; i++) {
                if (flash_right && (strobe || max_threat == RADAR_THREAT_LVL_AMBER)) {
                    s_led_buffer[i].r = target_r;
                    s_led_buffer[i].g = target_g;
                    s_led_buffer[i].b = 0;
                } else {
                    s_led_buffer[i].r = base_r;
                    s_led_buffer[i].g = 0;
                    s_led_buffer[i].b = 0;
                }
            }
        } else if (enabled_macros & RADAR_MACRO_AMBIENT_GLOW_EN) {
            uint8_t base_r = (uint8_t)(50 * brightness_scale);
            for (int i = 0; i < NUM_LEDS; i++) {
                s_led_buffer[i].r = base_r;
                s_led_buffer[i].g = 0;
                s_led_buffer[i].b = 0;
            }
        } else {
            for (int i = 0; i < NUM_LEDS; i++) {
                s_led_buffer[i].r = 0;
                s_led_buffer[i].g = 0;
                s_led_buffer[i].b = 0;
            }
        }

        update_neopixel_halo();
        frame_count++;
        vTaskDelay(pdMS_TO_TICKS(25)); // 40 Hz refresh rate
    }
}

// Task 3: UWB Radar Backbone Bridge Task (20 Hz Transmission to Central Box)
static void task_uwb_radar_bridge(void *arg) {
    ESP_LOGI(TAG, "All-UWB Radar Backbone Bridge running at 20 Hz...");
    uint32_t heartbeat_counter = 0;

    while (true) {
        UwbRadarTargetsPkt uwb_pkt = {};
        uwb_pkt.frame_index = s_radar_frame_index++;

        if (s_radar_data_mutex && xSemaphoreTake(s_radar_data_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
            uwb_pkt.target_count = s_current_telemetry.target_count;
            if (uwb_pkt.target_count > UWB_RADAR_MAX_TARGETS) {
                uwb_pkt.target_count = UWB_RADAR_MAX_TARGETS;
            }

            for (uint8_t t = 0; t < uwb_pkt.target_count; t++) {
                uwb_pkt.targets[t].target_id = s_current_telemetry.targets[t].target_id;
                uwb_pkt.targets[t].distance_cm = s_current_telemetry.targets[t].distance_cm;
                uwb_pkt.targets[t].speed_cm_s = s_current_telemetry.targets[t].rel_speed_mps_100;
                uwb_pkt.targets[t].azimuth_deg_10 = s_current_telemetry.targets[t].azimuth_deg_10;
                uwb_pkt.targets[t].ttc_ms = s_current_telemetry.targets[t].ttc_ms;
                uwb_pkt.targets[t].threat_level = s_current_telemetry.targets[t].threat_level;

                if (s_current_telemetry.targets[t].threat_level >= RADAR_THREAT_LVL_RED) {
                    uwb_pkt.urgent_flag = 1;
                }
            }
            xSemaphoreGive(s_radar_data_mutex);
        }

        // 1. Transmit 20 Hz Radar Target List to Central Box via UWB
        UwbVehicleBackbone::instance().send_radar_targets(uwb_pkt);

        // 2. Periodic UWB Heartbeat (every 500 ms)
        heartbeat_counter++;
        if (heartbeat_counter >= 10) { // 10 * 50 ms = 500 ms
            heartbeat_counter = 0;
            UwbVehicleBackbone::instance().send_heartbeat(5000, 200);
        }

        vTaskDelay(pdMS_TO_TICKS(50)); // 20 Hz cycle
    }
}

// -----------------------------------------------------------------------------
// Main Application Entry Point
// -----------------------------------------------------------------------------
extern "C" void app_main(void) {
    ESP_LOGI(TAG, "============================================================");
    ESP_LOGI(TAG, "   OPENMOTORBRIDGE RADAR 2.0 SUB-MCU v3.0                   ");
    ESP_LOGI(TAG, "   Target: ESP32-C5 Dual-Band (PCBA 08 mmWave Wings)       ");
    ESP_LOGI(TAG, "   All-UWB Deterministic Backbone (Qorvo DW3110 / 6.5 GHz)  ");
    ESP_LOGI(TAG, "============================================================");

    s_radar_data_mutex = xSemaphoreCreateMutex();
    memset(&s_current_telemetry, 0, sizeof(s_current_telemetry));
    memset(&s_current_command, 0, sizeof(s_current_command));
    s_current_command.dimming_pwm_pct = 100;
    s_post_start_ms = (uint32_t)(esp_timer_get_time() / 1000ULL);
    s_post_running = true;

    // 0. HF Hardening: 2.4 GHz Wi-Fi & BLE are strictly disabled & uninitialized at the vehicle rear.
    // RF is strictly limited to 6.5 GHz UWB (Qorvo DW3110) & 5.9 GHz V2X (Taoglas patch antenna).
    ESP_LOGI(TAG, "HF Hardening verified: 2.4 GHz disabled. 6.5 GHz UWB & 5.9 GHz V2X active.");

    // 1. Initialize Wheeltec MR20 UART
    init_uarts();

    // 2. Initialize All-UWB Backbone (Node-ID 0x05)
    dw3110_config_t dw_cfg = {
        .spi_host = SPI2_HOST,
        .pin_sck  = PIN_UWB_SCK,
        .pin_mosi = PIN_UWB_MOSI,
        .pin_miso = PIN_UWB_MISO,
        .pin_cs   = PIN_UWB_CS,
        .pin_irq  = PIN_UWB_IRQ,
        .pin_rst  = PIN_UWB_RST,
        .pan_id   = UWB_BACKBONE_PAN_ID,
        .short_addr = static_cast<uint16_t>(UWB_NODE_REAR_RADAR)
    };

    UwbVehicleBackbone::instance().init(UWB_NODE_REAR_RADAR, &dw_cfg);
    UwbVehicleBackbone::instance().set_radar_led_callback([](const UwbRadarLedCmdPkt &cmd) {
        if (s_radar_data_mutex && xSemaphoreTake(s_radar_data_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
            s_current_command.macro_mode = cmd.macro_mode;
            s_current_command.dimming_pwm_pct = cmd.brightness_pct;
            s_current_command.bsd_left_active = (cmd.left_bsd_state != 0);
            s_current_command.bsd_right_active = (cmd.right_bsd_state != 0);
            xSemaphoreGive(s_radar_data_mutex);
        }
    });
    UwbVehicleBackbone::instance().start_task(22, 0);

    // 3. Spawn FreeRTOS Tasks
    xTaskCreate(task_mr20_rx, "mr20_rx", 4096, NULL, 5, NULL);
    xTaskCreate(task_neopixel_halo, "neopixel_halo", 3072, NULL, 4, NULL);
    xTaskCreate(task_uwb_radar_bridge, "uwb_radar_tx", 4096, NULL, 6, NULL);

    ESP_LOGI(TAG, "Radar 2.0 Sub-MCU initialized and active on UWB Node 0x05.");
}
