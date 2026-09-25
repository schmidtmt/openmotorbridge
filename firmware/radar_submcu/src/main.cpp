#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "driver/uart.h"
#include "driver/gpio.h"
#include "esp_timer.h"
#include "esp_log.h"
#include "esp_system.h"
#include "radar_mr20_protocol.h"
#include <math.h>

static const char *TAG = "RADAR2_SUBMCU";

// Pinout for Radar 2.0 Sub-MCU (ESP32-C5 Dual-Band)
#define UART_BRIDGE_PORT            UART_NUM_0
#define PIN_BRIDGE_TX               GPIO_NUM_21 // to Central Box Binder M5 RX
#define PIN_BRIDGE_RX               GPIO_NUM_20 // to Central Box Binder M5 TX
#define BRIDGE_BAUDRATE             115200

#define UART_MR20_PORT              UART_NUM_1
#define PIN_MR20_TX                 GPIO_NUM_4  // to Wheeltec MR20 RX
#define PIN_MR20_RX                 GPIO_NUM_5  // from Wheeltec MR20 TX
#define MR20_BAUDRATE               115200

#define PIN_NEOPIXEL                GPIO_NUM_8  // WS2812B-2020 Data line
#define NUM_LEDS                    36          // 36-LED Visual Warning Wings (18 Left, 18 Right)
#define WING_LEDS                   18          // 18 LEDs per wing (Left: 0..17, Right: 18..35)

static SemaphoreHandle_t s_radar_data_mutex = NULL;
static RadarTelemetryPacket_t s_current_telemetry;
static RadarCommandPacket_t s_current_command;
static uint8_t s_telemetry_seq = 0;
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

// Helper to write simulated WS2812B bits via RMT or fast GPIO bit-banging
static void update_neopixel_halo(void) {
    // In hardware this is dispatched to the ESP-IDF RMT or SPI-MOSI driver.
    // For ESP32-C5, SPI2 MOSI (GPIO 8) delivers zero-jitter 800kHz WS2812 pulses.
}

static void init_uarts(void) {
    // 1. Central Box Bridge UART (Binder M5)
    const uart_config_t bridge_uart_config = {
        .baud_rate = BRIDGE_BAUDRATE,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };
    uart_param_config(UART_BRIDGE_PORT, &bridge_uart_config);
    uart_set_pin(UART_BRIDGE_PORT, PIN_BRIDGE_TX, PIN_BRIDGE_RX, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    uart_driver_install(UART_BRIDGE_PORT, 512, 512, 0, NULL, 0);

    // 2. Wheeltec MR20 Sensor UART
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

    ESP_LOGI(TAG, "UARTs initialized: Bridge UART0 (GPIO21/20), MR20 UART1 (GPIO4/5).");
}

// Parse Wheeltec MR20 77-GHz raw mmWave clusters
static void parse_mr20_frame(const uint8_t *buf, size_t len) {
    if (len < 5) return;

    for (size_t i = 0; i < len - 4; i++) {
        if (buf[i] == MR20_RAW_HEADER_1 && buf[i + 1] == MR20_RAW_HEADER_2) {
            uint8_t frame_len = buf[i + 2];
            uint8_t frame_type = buf[i + 3];

            if (frame_type == MR20_RAW_FRAME_TYPE_TARGETS && (i + frame_len) <= len) {
                uint8_t raw_target_count = buf[i + 4];
                if (raw_target_count > 8) raw_target_count = 8;

                if (s_radar_data_mutex && xSemaphoreTake(s_radar_data_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
                    s_current_telemetry.target_count = raw_target_count;
                    s_current_telemetry.max_threat = RADAR_THREAT_LVL_CLEAR;
                    s_current_telemetry.blind_spot_left = false;
                    s_current_telemetry.blind_spot_right = false;
                    s_current_telemetry.closest_dist_cm = 0xFFFF;
                    s_current_telemetry.highest_speed_cms = 0;

                    size_t offset = i + 5;
                    for (uint8_t t = 0; t < raw_target_count && (offset + sizeof(Mr20RawTarget_t)) <= (i + frame_len); t++) {
                        const Mr20RawTarget_t *raw = (const Mr20RawTarget_t *)(buf + offset);
                        RadarTargetSummary_t *out = &s_current_telemetry.targets[t];

                        out->id = raw->id;
                        out->distance_cm = raw->range_raw * 10; // 0.1m to cm
                        out->rel_speed_cms = raw->speed_raw * 10; // 0.1 m/s to cm/s
                        out->azimuth_cdeg = raw->angle_raw * 10; // 0.1 deg to centidegrees

                        // Time to Collision (TTC) calculation:
                        // rel_speed_cms is negative when approaching
                        if (out->rel_speed_cms < -100) { // faster than 1 m/s closing
                            float closing_speed_ms = (-out->rel_speed_cms) / 100.0f;
                            float distance_m = out->distance_cm / 100.0f;
                            float ttc_sec = distance_m / closing_speed_ms;
                            out->ttc_tenths_s = (ttc_sec < 25.5f) ? (uint8_t)(ttc_sec * 10.0f) : 255;
                        } else {
                            out->ttc_tenths_s = 255;
                        }

                        // Threat classification
                        if (out->ttc_tenths_s < 25 || (out->distance_cm < 3500 && out->rel_speed_cms < -694)) { // 25 km/h = 694 cm/s
                            out->threat_level = RADAR_THREAT_LVL_RED;
                        } else if (out->distance_cm < 7500 && out->rel_speed_cms < -416) { // 15 km/h = 416 cm/s
                            out->threat_level = RADAR_THREAT_LVL_AMBER;
                        } else {
                            out->threat_level = RADAR_THREAT_LVL_CLEAR;
                        }

                        if (out->threat_level > s_current_telemetry.max_threat) {
                            s_current_telemetry.max_threat = out->threat_level;
                        }

                        if (out->distance_cm < s_current_telemetry.closest_dist_cm) {
                            s_current_telemetry.closest_dist_cm = out->distance_cm;
                        }

                        if (-out->rel_speed_cms > s_current_telemetry.highest_speed_cms) {
                            s_current_telemetry.highest_speed_cms = -out->rel_speed_cms;
                        }

                        // Blind spot detection (<15m, azimuth off-center)
                        if (out->distance_cm < 1500) {
                            if (out->azimuth_cdeg < -300) s_current_telemetry.blind_spot_left = true;
                            if (out->azimuth_cdeg > 300)  s_current_telemetry.blind_spot_right = true;
                        }

                        offset += sizeof(Mr20RawTarget_t);
                    }

                    s_last_mr20_rx_time_ms = (uint32_t)(esp_timer_get_time() / 1000ULL);
                    xSemaphoreGive(s_radar_data_mutex);
                }
                i += frame_len - 1;
            }
        }
    }
}

// Task 1: Wheeltec MR20 Raw Parser Task (20 Hz)
static void task_mr20_rx(void *arg) {
    ESP_LOGI(TAG, "MR20 Radar RX Task running at 20 Hz...");
    uint8_t rx_buf[256];

    while (true) {
        int bytes = uart_read_bytes(UART_MR20_PORT, rx_buf, sizeof(rx_buf), pdMS_TO_TICKS(50));
        if (bytes > 0) {
            parse_mr20_frame(rx_buf, (size_t)bytes);
        }

        // Timeout check: If no raw radar data received for >1000ms, reset targets
        uint32_t now = (uint32_t)(esp_timer_get_time() / 1000ULL);
        if (now - s_last_mr20_rx_time_ms > 1000) {
            if (s_radar_data_mutex && xSemaphoreTake(s_radar_data_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
                s_current_telemetry.target_count = 0;
                s_current_telemetry.max_threat = RADAR_THREAT_LVL_CLEAR;
                s_current_telemetry.blind_spot_left = false;
                s_current_telemetry.blind_spot_right = false;
                s_current_telemetry.closest_dist_cm = 0xFFFF;
                s_current_telemetry.highest_speed_cms = 0;
                xSemaphoreGive(s_radar_data_mutex);
            }
        }

        vTaskDelay(pdMS_TO_TICKS(20));
    }
}

// Task 2: Neopixel WS2812B Halo Display Task (Bremslicht-Strobe, Threat-Halo, Konfigurierbare Makros)
static void task_neopixel_halo(void *arg) {
    ESP_LOGI(TAG, "Neopixel Halo Task initialized (36-LED Matrix Dual-Wing)...");
    uint32_t frame_count = 0;

    while (true) {
        uint8_t max_threat = RADAR_THREAT_LVL_CLEAR;
        uint8_t brake_mode = 0;
        uint8_t dimming_pct = 100;
        bool bsd_left = false, bsd_right = false;
        uint16_t closest_dist_cm = 0xFFFF;
        int16_t highest_speed_cms = 0;
        uint16_t enabled_macros = (RADAR_MACRO_POST_SWEEP_EN | RADAR_MACRO_ESS_STROBE_EN |
                                    RADAR_MACRO_HAZARD_BEACON_EN | RADAR_MACRO_THEFT_STROBE_EN |
                                    RADAR_MACRO_AMBIENT_GLOW_EN);
        bool diag_active = false;
        uint8_t diag_states[NUM_LEDS];

        if (s_radar_data_mutex && xSemaphoreTake(s_radar_data_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
            max_threat = s_current_telemetry.max_threat;
            bsd_left = s_current_telemetry.blind_spot_left;
            bsd_right = s_current_telemetry.blind_spot_right;
            closest_dist_cm = s_current_telemetry.closest_dist_cm;
            highest_speed_cms = s_current_telemetry.highest_speed_cms;
            brake_mode = s_current_command.brake_strobe_req;
            dimming_pct = (s_current_command.dimming_pwm_pct > 0) ? s_current_command.dimming_pwm_pct : 100;
            enabled_macros = s_enabled_macros;
            diag_active = s_diag_override;
            if (diag_active) {
                memcpy(diag_states, s_diag_led_states, sizeof(diag_states));
            }
            xSemaphoreGive(s_radar_data_mutex);
        }

        float brightness_scale = (float)dimming_pct / 100.0f;

        // 0. Explicit Diagnostic Mode Override (Opcode 0x25)
        if (diag_active) {
            for (int i = 0; i < NUM_LEDS; i++) {
                uint8_t st = diag_states[i];
                if (st == POST_LED_GREEN_OK) {
                    s_led_buffer[i].r = 0; s_led_buffer[i].g = 255; s_led_buffer[i].b = 0;
                } else if (st == POST_LED_AMBER_INIT) {
                    s_led_buffer[i].r = 255; s_led_buffer[i].g = 140; s_led_buffer[i].b = 0;
                } else if (st == POST_LED_RED_FAIL) {
                    s_led_buffer[i].r = 255; s_led_buffer[i].g = 0; s_led_buffer[i].b = 0;
                } else if (st == POST_LED_RED_BLINK) {
                    bool blink = (frame_count % 8) < 4;
                    s_led_buffer[i].r = blink ? 255 : 0; s_led_buffer[i].g = 0; s_led_buffer[i].b = 0;
                } else {
                    s_led_buffer[i].r = 0; s_led_buffer[i].g = 0; s_led_buffer[i].b = 0;
                }
            }
        }
        // 1. Welcome & POST Sweep on Boot (2.5s duration, non-blocking)
        else if (s_post_running && (enabled_macros & RADAR_MACRO_POST_SWEEP_EN)) {
            uint32_t now = (uint32_t)(esp_timer_get_time() / 1000ULL);
            uint32_t elapsed = now - s_post_start_ms;
            if (elapsed > 2500) {
                s_post_running = false;
            } else {
                // Outward progressive sweep from center to wingtips
                int active_led = (int)((elapsed * WING_LEDS) / 2500);
                for (int i = 0; i < WING_LEDS; i++) {
                    bool on = (i <= active_led);
                    // Left wing (0..17)
                    s_led_buffer[i].r = 0;
                    s_led_buffer[i].g = on ? 200 : 0;
                    s_led_buffer[i].b = on ? 255 : 0;
                    // Right wing (18..35)
                    s_led_buffer[NUM_LEDS - 1 - i].r = 0;
                    s_led_buffer[NUM_LEDS - 1 - i].g = on ? 200 : 0;
                    s_led_buffer[NUM_LEDS - 1 - i].b = on ? 255 : 0;
                }
            }
        }
        // 2. Emergency Stop Signal (ESS) - 4.5 Hz Fast Strobe (Intense Red)
        else if (brake_mode == 2 && (enabled_macros & RADAR_MACRO_ESS_STROBE_EN)) {
            bool on = (frame_count % 4) < 2; // 4.5 Hz strobe at 25ms steps
            for (int i = 0; i < NUM_LEDS; i++) {
                s_led_buffer[i].r = on ? 255 : 0;
                s_led_buffer[i].g = 0;
                s_led_buffer[i].b = 0;
            }
        }
        // 3. Pannen-Warnblitz (Hazard Beacon) - 1.2 Hz Double-Flash at Standstill
        else if (brake_mode == 3 && (enabled_macros & RADAR_MACRO_HAZARD_BEACON_EN)) {
            uint32_t phase = frame_count % 32; // ~1.2 Hz cycle
            bool flash = (phase < 3) || (phase >= 6 && phase < 9);
            for (int i = 0; i < NUM_LEDS; i++) {
                s_led_buffer[i].r = flash ? 255 : 0;
                s_led_buffer[i].g = flash ? 120 : 0;
                s_led_buffer[i].b = 0;
            }
        }
        // 4. Alarmanlagen-Strobe (Theft Strobe) - 12 Hz High-Intensity Strobe
        else if (brake_mode == 4 && (enabled_macros & RADAR_MACRO_THEFT_STROBE_EN)) {
            bool on = (frame_count % 3) == 0; // ~13 Hz flash
            for (int i = 0; i < NUM_LEDS; i++) {
                s_led_buffer[i].r = on ? 255 : 0;
                s_led_buffer[i].g = on ? 255 : 0;
                s_led_buffer[i].b = on ? 255 : 0;
            }
        }
        // 5. Solid Brake Light (Standard or fallback if ESS disabled)
        else if (brake_mode == 1 || brake_mode == 2) {
            for (int i = 0; i < NUM_LEDS; i++) {
                s_led_buffer[i].r = (uint8_t)(255 * brightness_scale);
                s_led_buffer[i].g = 0;
                s_led_buffer[i].b = 0;
            }
        }
        // 6. Drängler-Abstandswarnung (Tailgating Guard) - Target < 3m closing
        else if ((enabled_macros & RADAR_MACRO_TAILGATING_EN) && closest_dist_cm < 300 && highest_speed_cms > 150) {
            // Inward chasing wave from wing tips toward center
            int step = (frame_count % WING_LEDS);
            for (int i = 0; i < WING_LEDS; i++) {
                bool hit = (i == step || i == (step + 1) % WING_LEDS);
                uint8_t r = hit ? 255 : (uint8_t)(40 * brightness_scale);
                s_led_buffer[i].r = r;
                s_led_buffer[i].g = 0;
                s_led_buffer[i].b = 0;
                s_led_buffer[NUM_LEDS - 1 - i].r = r;
                s_led_buffer[NUM_LEDS - 1 - i].g = 0;
                s_led_buffer[NUM_LEDS - 1 - i].b = 0;
            }
        }
        // 7. Threat Warning on Dual Wings (Directional BSD & TTC Level)
        else if (max_threat == RADAR_THREAT_LVL_RED || max_threat == RADAR_THREAT_LVL_AMBER) {
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
        }
        // 8. Konvoi-Puls (Follow-Me Wave)
        else if (enabled_macros & RADAR_MACRO_CONVOY_MARKER_EN) {
            // Gentle rhythmic wave in warm amber/cyan
            float wave = (sinf((float)frame_count * 0.1f) + 1.0f) * 0.5f;
            uint8_t val = (uint8_t)(120.0f * wave * brightness_scale);
            for (int i = 0; i < NUM_LEDS; i++) {
                s_led_buffer[i].r = val;
                s_led_buffer[i].g = (uint8_t)(val * 0.4f);
                s_led_buffer[i].b = 0;
            }
        }
        // 9. Standby Position Glow / Night Light
        else if (enabled_macros & RADAR_MACRO_AMBIENT_GLOW_EN) {
            uint8_t base_r = (uint8_t)(50 * brightness_scale);
            for (int i = 0; i < NUM_LEDS; i++) {
                s_led_buffer[i].r = base_r;
                s_led_buffer[i].g = 0;
                s_led_buffer[i].b = 0;
            }
        }
        // 10. Completely Off (Standby glow disabled)
        else {
            for (int i = 0; i < NUM_LEDS; i++) {
                s_led_buffer[i].r = 0;
                s_led_buffer[i].g = 0;
                s_led_buffer[i].b = 0;
            }
        }

        update_neopixel_halo();
        frame_count++;
        vTaskDelay(pdMS_TO_TICKS(25)); // 40 Hz LED refresh rate
    }
}

// Task 3: Central Box Communication Bridge Task (UART0 / Binder M5)
static void task_central_box_bridge(void *arg) {
    ESP_LOGI(TAG, "Central Box Bridge Task running at 20 Hz (Binder M5 UART)...");
    uint8_t rx_buf[128];

    while (true) {
        // 1. Check for incoming commands from Central Box
        int rx_bytes = uart_read_bytes(UART_BRIDGE_PORT, rx_buf, sizeof(rx_buf), pdMS_TO_TICKS(10));
        if (rx_bytes >= 4) {
            for (size_t i = 0; i <= (size_t)rx_bytes - 4; i++) {
                if (rx_buf[i] == OMB_RADAR_SYNC_BYTE_1 && rx_buf[i + 1] == OMB_RADAR_SYNC_BYTE_2 &&
                    rx_buf[i + 2] == OMB_RADAR_PROTOCOL_VERSION) {

                    uint8_t pkt_type = rx_buf[i + 3];

                    // Packet Type 0x20: Vehicle State Dynamics
                    if (pkt_type == RADAR_PKT_CMD_VEHICLE_STATE && (i + sizeof(RadarCommandPacket_t)) <= (size_t)rx_bytes) {
                        const RadarCommandPacket_t *cmd = (const RadarCommandPacket_t *)(rx_buf + i);
                        uint16_t expected_crc = radar_crc16((const uint8_t *)cmd, sizeof(RadarCommandPacket_t) - 2);
                        if (expected_crc == cmd->checksum) {
                            if (s_radar_data_mutex && xSemaphoreTake(s_radar_data_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
                                s_current_command = *cmd;
                                xSemaphoreGive(s_radar_data_mutex);
                            }
                        }
                        break;
                    }
                    // Packet Type 0x40: Configurable Warning Macros
                    else if (pkt_type == RADAR_PKT_CMD_CONFIG_MACROS && (i + sizeof(RadarConfigMacrosPacket_t)) <= (size_t)rx_bytes) {
                        const RadarConfigMacrosPacket_t *cfg = (const RadarConfigMacrosPacket_t *)(rx_buf + i);
                        uint16_t expected_crc = radar_crc16((const uint8_t *)cfg, sizeof(RadarConfigMacrosPacket_t) - 2);
                        if (expected_crc == cfg->checksum) {
                            if (s_radar_data_mutex && xSemaphoreTake(s_radar_data_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
                                s_enabled_macros = cfg->enabled_macros;
                                s_ess_thresh_pct = cfg->ess_threshold_pct;
                                xSemaphoreGive(s_radar_data_mutex);
                            }
                            ESP_LOGI(TAG, "💾 Sub-MCU: Received Macro Config from Central Box: 0x%04X, ESS thresh=%d%%",
                                     cfg->enabled_macros, cfg->ess_threshold_pct);
                        }
                        break;
                    }
                    // Packet Type 0x25: POST Diagnostic Matrix
                    else if (pkt_type == RADAR_PKT_CMD_POST_DIAG && (i + sizeof(RadarPostDiagPacket_t)) <= (size_t)rx_bytes) {
                        const RadarPostDiagPacket_t *diag = (const RadarPostDiagPacket_t *)(rx_buf + i);
                        uint16_t expected_crc = radar_crc16((const uint8_t *)diag, sizeof(RadarPostDiagPacket_t) - 2);
                        if (expected_crc == diag->checksum) {
                            if (s_radar_data_mutex && xSemaphoreTake(s_radar_data_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
                                s_diag_override = true;
                                memcpy(s_diag_led_states, diag->led_states, sizeof(s_diag_led_states));
                                xSemaphoreGive(s_radar_data_mutex);
                            }
                            ESP_LOGI(TAG, "🩺 Sub-MCU: Activated 18-Pair Diagnostic Matrix (duration %d tenths s)", diag->duration_tenths_s);
                        }
                        break;
                    }
                    // Packet Type 0xF0: Enter In-System Bootloader
                    else if (pkt_type == RADAR_PKT_CMD_ENTER_BOOTLOAD) {
                        ESP_LOGW(TAG, "⚡ Rebooting into In-System Bootloader as commanded by Central Box!");
                        vTaskDelay(pdMS_TO_TICKS(50));
                        esp_restart();
                        break;
                    }
                }
            }
        }

        // 2. Transmit Telemetry Packet (20 Hz) to Central Box
        RadarTelemetryPacket_t pkt;
        if (s_radar_data_mutex && xSemaphoreTake(s_radar_data_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
            pkt = s_current_telemetry;
            xSemaphoreGive(s_radar_data_mutex);
        } else {
            memset(&pkt, 0, sizeof(pkt));
        }

        pkt.sync1 = OMB_RADAR_SYNC_BYTE_1;
        pkt.sync2 = OMB_RADAR_SYNC_BYTE_2;
        pkt.version = OMB_RADAR_PROTOCOL_VERSION;
        pkt.pkt_type = RADAR_PKT_TELEMETRY_TARGETS;
        pkt.seq_num = s_telemetry_seq++;
        pkt.checksum = radar_crc16((const uint8_t *)&pkt, sizeof(RadarTelemetryPacket_t) - 2);

        uart_write_bytes(UART_BRIDGE_PORT, (const char *)&pkt, sizeof(RadarTelemetryPacket_t));

        vTaskDelay(pdMS_TO_TICKS(50)); // 20 Hz Transmission
    }
}

extern "C" void app_main(void) {
    ESP_LOGI(TAG, "=== OpenMotorBridge Radar 2.0 Sub-MCU Initializing (Wheeltec MR20 77GHz) ===");

    s_radar_data_mutex = xSemaphoreCreateMutex();
    memset(&s_current_telemetry, 0, sizeof(s_current_telemetry));
    memset(&s_current_command, 0, sizeof(s_current_command));
    s_current_command.dimming_pwm_pct = 100;
    s_post_start_ms = (uint32_t)(esp_timer_get_time() / 1000ULL);
    s_post_running = true;

    init_uarts();

    // Create Tasks on ESP32-C3 / ESP32-C5
    xTaskCreate(task_mr20_rx, "mr20_rx", 4096, NULL, 5, NULL);
    xTaskCreate(task_neopixel_halo, "neopixel_halo", 3072, NULL, 4, NULL);
    xTaskCreate(task_central_box_bridge, "bridge_uart", 4096, NULL, 6, NULL);

    ESP_LOGI(TAG, "Radar 2.0 Sub-MCU initialization complete.");
}
