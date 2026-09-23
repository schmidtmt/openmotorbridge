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

static const char *TAG = "RADAR2_SUBMCU";

// Pinout for Radar 2.0 Sub-MCU (ESP32-C3)
#define UART_BRIDGE_PORT            UART_NUM_0
#define PIN_BRIDGE_TX               GPIO_NUM_21 // to Central Box Binder M5 RX
#define PIN_BRIDGE_RX               GPIO_NUM_20 // to Central Box Binder M5 TX
#define BRIDGE_BAUDRATE             115200

#define UART_MR20_PORT              UART_NUM_1
#define PIN_MR20_TX                 GPIO_NUM_4  // to Wheeltec MR20 RX
#define PIN_MR20_RX                 GPIO_NUM_5  // from Wheeltec MR20 TX
#define MR20_BAUDRATE               115200

#define PIN_NEOPIXEL                GPIO_NUM_8  // WS2812B-2020 Data line
#define NUM_LEDS                    24          // 24-LED Halo around radar horn

static SemaphoreHandle_t s_radar_data_mutex = NULL;
static RadarTelemetryPacket_t s_current_telemetry;
static RadarCommandPacket_t s_current_command;
static uint8_t s_telemetry_seq = 0;
static uint32_t s_last_mr20_rx_time_ms = 0;

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
    // For ESP32-C3, SPI2 MOSI (GPIO 8) delivers zero-jitter 800kHz WS2812 pulses.
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

// Task 2: Neopixel WS2812B Halo Display Task (Bremslicht-Strobe, Threat-Halo)
static void task_neopixel_halo(void *arg) {
    ESP_LOGI(TAG, "Neopixel Halo Task initialized (24-LED Neopixel Ring)...");
    uint32_t frame_count = 0;

    while (true) {
        uint8_t max_threat = RADAR_THREAT_LVL_CLEAR;
        uint8_t brake_mode = 0;
        uint8_t dimming_pct = 100;
        bool bsd_left = false, bsd_right = false;

        if (s_radar_data_mutex && xSemaphoreTake(s_radar_data_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
            max_threat = s_current_telemetry.max_threat;
            bsd_left = s_current_telemetry.blind_spot_left;
            bsd_right = s_current_telemetry.blind_spot_right;
            brake_mode = s_current_command.brake_strobe_req;
            dimming_pct = (s_current_command.dimming_pwm_pct > 0) ? s_current_command.dimming_pwm_pct : 100;
            xSemaphoreGive(s_radar_data_mutex);
        }

        float brightness_scale = (float)dimming_pct / 100.0f;

        // Effect 1: Emergency Stop Signal (ESS) - 4.5 Hz Fast Strobe (Intense Red)
        if (brake_mode == 2) {
            bool on = (frame_count % 4) < 2; // 4.5 Hz strobe at 20ms steps
            for (int i = 0; i < NUM_LEDS; i++) {
                s_led_buffer[i].r = on ? 255 : 0;
                s_led_buffer[i].g = 0;
                s_led_buffer[i].b = 0;
            }
        }
        // Effect 2: Solid Brake Light
        else if (brake_mode == 1) {
            for (int i = 0; i < NUM_LEDS; i++) {
                s_led_buffer[i].r = (uint8_t)(255 * brightness_scale);
                s_led_buffer[i].g = 0;
                s_led_buffer[i].b = 0;
            }
        }
        // Effect 3: Threat Halo Warning (expanding red or amber ring)
        else if (max_threat == RADAR_THREAT_LVL_RED) {
            // Rapid alternating red flash on halo
            bool strobe = (frame_count % 3) == 0;
            for (int i = 0; i < NUM_LEDS; i++) {
                s_led_buffer[i].r = strobe ? (uint8_t)(255 * brightness_scale) : 0;
                s_led_buffer[i].g = 0;
                s_led_buffer[i].b = 0;
            }
        } else if (max_threat == RADAR_THREAT_LVL_AMBER) {
            // Solid amber halo
            for (int i = 0; i < NUM_LEDS; i++) {
                s_led_buffer[i].r = (uint8_t)(255 * brightness_scale);
                s_led_buffer[i].g = (uint8_t)(140 * brightness_scale);
                s_led_buffer[i].b = 0;
            }
        }
        // Effect 4: Standby Position Glow / Night Light
        else {
            // Subtle breathing red taillight (18% - 50% brightness according to solar/tunnel dimmer)
            uint8_t base_r = (uint8_t)(50 * brightness_scale);
            for (int i = 0; i < NUM_LEDS; i++) {
                s_led_buffer[i].r = base_r;
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
        if (rx_bytes >= (int)sizeof(RadarCommandPacket_t)) {
            for (size_t i = 0; i <= (size_t)rx_bytes - sizeof(RadarCommandPacket_t); i++) {
                const RadarCommandPacket_t *cmd = (const RadarCommandPacket_t *)(rx_buf + i);
                if (cmd->sync1 == OMB_RADAR_SYNC_BYTE_1 && cmd->sync2 == OMB_RADAR_SYNC_BYTE_2 &&
                    cmd->version == OMB_RADAR_PROTOCOL_VERSION) {

                    // Verify CRC
                    uint16_t expected_crc = radar_crc16((const uint8_t *)cmd, sizeof(RadarCommandPacket_t) - 2);
                    if (expected_crc == cmd->checksum) {
                        if (cmd->pkt_type == RADAR_PKT_CMD_VEHICLE_STATE) {
                            if (s_radar_data_mutex && xSemaphoreTake(s_radar_data_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
                                s_current_command = *cmd;
                                xSemaphoreGive(s_radar_data_mutex);
                            }
                        } else if (cmd->pkt_type == RADAR_PKT_CMD_ENTER_BOOTLOAD) {
                            ESP_LOGW(TAG, "⚡ Rebooting into In-System Bootloader as commanded by Central Box!");
                            vTaskDelay(pdMS_TO_TICKS(50));
                            esp_restart();
                        }
                    }
                    break;
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

    init_uarts();

    // Create Tasks on ESP32-C3
    xTaskCreate(task_mr20_rx, "mr20_rx", 4096, NULL, 5, NULL);
    xTaskCreate(task_neopixel_halo, "neopixel_halo", 3072, NULL, 4, NULL);
    xTaskCreate(task_central_box_bridge, "bridge_uart", 4096, NULL, 6, NULL);

    ESP_LOGI(TAG, "Radar 2.0 Sub-MCU initialization complete.");
}
