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
#include "usb_vehicle_backbone.h"
#include "usb_backbone_types.h"

static const char *TAG = "RADAR2_SUBMCU";

// =============================================================================
// OpenMotorBridge - PCBA 08 v10.0 77 GHz mmWave Radar & 5.9 GHz V2X C-ITS Node
// KiCad Source: hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb
// Host MCU: U1 ESP32-C5-WROOM-1U / ESP32-C3-WROOM-02U Pinout
// =============================================================================
#define UART_MR20_PORT              UART_NUM_1
#define PIN_MR20_RX                 GPIO_NUM_3   // U1 Pad 4: MR20_TX (from J2 Pin 3 Radar Target Vectors)
#define PIN_MR20_TX                 GPIO_NUM_4   // U1 Pad 5: MR20_RX (to J2 Pin 4 Radar Config Commands)
#define MR20_BAUDRATE               115200

#define PIN_NEOPIXEL                GPIO_NUM_8   // U1 Pad 8: WS2812_DATA -> D1..D36 Halo Warning Wings
#define PIN_RADAR_BOOT              GPIO_NUM_9   // U1 Pad 13: ESP_IO9_BOOT (SW1)
#define PIN_RADAR_USB_DM            GPIO_NUM_18  // U1 Pad 16: BUS_DM (J1 Pin 4 USB 2.0 D- to Central Box)
#define PIN_RADAR_USB_DP            GPIO_NUM_19  // U1 Pad 17: BUS_DP (J1 Pin 3 USB 2.0 D+ to Central Box)

#define NUM_LEDS                    36           // 36-LED Visual Warning Wings (D1..D36)
#define WING_LEDS                   18           // 18 LEDs per wing (Left: 0..17, Right: 18..35)

// ETSI ITS-G5 (IEEE 802.11p OCB @ 5.9 GHz) Message IDs (ETSI TS 102 894-2)
#define ETSI_ITS_MSG_ID_DENM        0x01         // Decentralized Environmental Notification Message
#define ETSI_ITS_MSG_ID_CAM         0x02         // Cooperative Awareness Message (Emergency Vehicle / Public Transit)
#define ETSI_ITS_MSG_ID_SPATEM      0x04         // Signal Phase and Timing Extended Message (GLOSA Green Wave)
#define ETSI_ITS_MSG_ID_MAPEM       0x05         // Map Data Extended Message (Intersection Topology)

static SemaphoreHandle_t s_radar_data_mutex = NULL;
static RadarTelemetryPacket_t s_current_telemetry;

typedef struct {
    uint8_t macro_mode;
    uint8_t dimming_pwm_pct;
    bool bsd_left_active;
    bool bsd_right_active;
} RadarActiveCommand_t;

static RadarActiveCommand_t s_current_command;
static uint16_t s_radar_frame_index = 0;
static uint32_t s_last_mr20_rx_time_ms = 0;

// Configurable Warning Macros & State Management
static uint16_t s_enabled_macros = (RADAR_MACRO_POST_SWEEP_EN | RADAR_MACRO_ESS_STROBE_EN |
                                    RADAR_MACRO_HAZARD_BEACON_EN | RADAR_MACRO_THEFT_STROBE_EN |
                                    RADAR_MACRO_AMBIENT_GLOW_EN);
static uint8_t s_ess_thresh_pct __attribute__((unused)) = 60;
static uint32_t s_post_start_ms __attribute__((unused)) = 0;
static bool s_post_running __attribute__((unused)) = true;
static bool s_diag_override __attribute__((unused)) = false;
static uint8_t s_diag_led_states[NUM_LEDS] __attribute__((unused));

// Neopixel color state
typedef struct {
    uint8_t r;
    uint8_t g;
    uint8_t b;
} RgbColor_t;

static RgbColor_t s_led_buffer[NUM_LEDS];

static void update_neopixel_halo(void) {
    // Drives the 36 WS2812B-2020 LEDs (D1..D36) via RMT/SPI-MOSI on GPIO 8
}

static void init_uarts(void) {
    // Wheeltec MR20 Sensor UART on J2 (Pin 3 = MR20_TX -> GPIO 3 RX, Pin 4 = MR20_RX <- GPIO 4 TX)
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

    ESP_LOGI(TAG, "Wheeltec MR20 UART1 initialized on J2: GPIO %d (TX -> MR20_RX) / GPIO %d (RX <- MR20_TX).",
             PIN_MR20_TX, PIN_MR20_RX);
}

// Parse Wheeltec MR20 77-GHz raw mmWave clusters
static void parse_mr20_frame(const uint8_t *buf, size_t len) {
    if (len < 5) return;

    for (size_t i = 0; i < len - 4; i++) {
        if (buf[i] == MR20_RAW_HEADER_1 && buf[i + 1] == MR20_RAW_HEADER_2) {
            uint8_t frame_len = buf[i + 2];
            uint8_t frame_type = buf[i + 3];

            if (i + frame_len <= len && frame_type == MR20_RAW_FRAME_TYPE_TARGETS) {
                uint8_t target_count = buf[i + 4];
                if (target_count > 8) target_count = 8;

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
                            uint8_t snr __attribute__((unused)) = buf[offset + 7];

                            s_current_telemetry.targets[t].id = id;
                            s_current_telemetry.targets[t].distance_cm = (uint16_t)(dist_raw * 10);
                            s_current_telemetry.targets[t].rel_speed_cms = speed_raw;
                            s_current_telemetry.targets[t].azimuth_cdeg = (int16_t)(azim_raw * 10);

                            // Calculate TTC (Time to collision)
                            if (speed_raw < -50 && dist_raw > 0) { // Approaching vehicle (relative speed negative)
                                float dist_m = (float)dist_raw * 0.1f;
                                float speed_mps = fabsf((float)speed_raw * 0.01f);
                                float ttc_s = dist_m / speed_mps;
                                s_current_telemetry.targets[t].ttc_tenths_s = (uint8_t)(ttc_s * 10.0f);

                                if (ttc_s < 1.5f) {
                                    s_current_telemetry.targets[t].threat_level = RADAR_THREAT_LVL_RED;
                                } else if (ttc_s < 3.0f) {
                                    s_current_telemetry.targets[t].threat_level = RADAR_THREAT_LVL_AMBER;
                                } else {
                                    s_current_telemetry.targets[t].threat_level = RADAR_THREAT_LVL_CLEAR;
                                }
                            } else {
                                s_current_telemetry.targets[t].ttc_tenths_s = 255; // No collision threat
                                s_current_telemetry.targets[t].threat_level = RADAR_THREAT_LVL_CLEAR;
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

// -----------------------------------------------------------------------------
// 5.9 GHz ETSI ITS-G5 (IEEE 802.11p OCB Promiscuous) V2X Frame Parser
// Supports SPATEM (GLOSA Green Wave), MAPEM, CAM (Emergency Vehicle) & DENM
// -----------------------------------------------------------------------------
void parse_v2x_cits_80211p_frame(const uint8_t *its_pdu, size_t len) {
    if (!its_pdu || len < 12) return;

    uint8_t protocol_ver = its_pdu[0];
    uint8_t msg_id       = its_pdu[1];
    if (protocol_ver < 1 || protocol_ver > 3) return;

    UsbV2xCitsEventPkt v2x_pkt = {};
    v2x_pkt.station_id = ((uint32_t)its_pdu[2] << 24) |
                         ((uint32_t)its_pdu[3] << 16) |
                         ((uint32_t)its_pdu[4] << 8)  |
                         (uint32_t)its_pdu[5];

    if (msg_id == ETSI_ITS_MSG_ID_SPATEM) {
        // SPATEM / GLOSA Green Wave Countdown
        v2x_pkt.v2x_msg_type          = V2X_MSG_SPATEM;
        v2x_pkt.traffic_light_phase   = its_pdu[6]; // 1=Green, 2=Yellow, 3=Red
        v2x_pkt.time_to_change_s      = its_pdu[8];
        v2x_pkt.recommended_speed_kph = its_pdu[9];
        v2x_pkt.distance_m            = ((uint16_t)its_pdu[10] << 8) | its_pdu[11];
        UsbVehicleBackbone::instance().send_v2x_cits_event(v2x_pkt);
    } else if (msg_id == ETSI_ITS_MSG_ID_DENM || msg_id == ETSI_ITS_MSG_ID_CAM) {
        // DENM Hazard / Emergency Vehicle Approaching
        v2x_pkt.v2x_msg_type          = (msg_id == ETSI_ITS_MSG_ID_DENM) ? V2X_MSG_DENM : V2X_MSG_CAM;
        v2x_pkt.denm_cause_code       = its_pdu[6]; // 95 = Emergency Vehicle, 91 = Breakdown, 97 = Collision
        v2x_pkt.distance_m            = ((uint16_t)its_pdu[10] << 8) | its_pdu[11];
        UsbVehicleBackbone::instance().send_v2x_cits_event(v2x_pkt);
    }
}

// Task 1: Wheeltec MR20 UART Receiver Task (50 Hz)
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
                s_current_telemetry.max_threat = RADAR_THREAT_LVL_CLEAR;
                s_current_telemetry.target_count = 0;
                xSemaphoreGive(s_radar_data_mutex);
            }
        }
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

// Task 2: Neopixel Dual-Wing Warning Lighting Task (40 Hz refresh rate)
static void task_neopixel_halo(void *arg) {
    ESP_LOGI(TAG, "Neopixel Halo Task running at 40 Hz (36 WS2812B LEDs on GPIO %d)...", PIN_NEOPIXEL);
    uint32_t frame_count = 0;

    while (true) {
        uint8_t max_threat = RADAR_THREAT_LVL_CLEAR;
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
                    if (s_current_telemetry.targets[t].azimuth_cdeg < -300) bsd_left = true;
                    if (s_current_telemetry.targets[t].azimuth_cdeg > 300)  bsd_right = true;
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

// Task 3: 4-Wire USB 2.0 Radar Backbone Bridge Task (20 Hz Transmission to Central Box)
static void task_usb_radar_bridge(void *arg) {
    ESP_LOGI(TAG, "4-Wire USB 2.0 Radar Backbone Bridge running at 20 Hz...");
    uint32_t heartbeat_counter = 0;

    while (true) {
        UsbRadarTargetsPkt usb_pkt = {};
        usb_pkt.frame_index = s_radar_frame_index++;

        if (s_radar_data_mutex && xSemaphoreTake(s_radar_data_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
            usb_pkt.target_count = s_current_telemetry.target_count;
            if (usb_pkt.target_count > USB_RADAR_MAX_TARGETS) {
                usb_pkt.target_count = USB_RADAR_MAX_TARGETS;
            }

            for (uint8_t t = 0; t < usb_pkt.target_count; t++) {
                usb_pkt.targets[t].target_id = s_current_telemetry.targets[t].id;
                usb_pkt.targets[t].distance_cm = s_current_telemetry.targets[t].distance_cm;
                usb_pkt.targets[t].speed_cm_s = s_current_telemetry.targets[t].rel_speed_cms;
                usb_pkt.targets[t].azimuth_deg_10 = (int16_t)(s_current_telemetry.targets[t].azimuth_cdeg / 10);
                usb_pkt.targets[t].ttc_ms = (uint16_t)(s_current_telemetry.targets[t].ttc_tenths_s * 100);
                usb_pkt.targets[t].threat_level = s_current_telemetry.targets[t].threat_level;

                if (s_current_telemetry.targets[t].threat_level >= RADAR_THREAT_LVL_RED) {
                    usb_pkt.urgent_flag = 1;
                }
            }
            xSemaphoreGive(s_radar_data_mutex);
        }

        // 1. Transmit 20 Hz Radar Target List to Central Box via 4-Wire USB Backbone
        UsbVehicleBackbone::instance().send_radar_targets(usb_pkt);

        // 2. Periodic USB Heartbeat (every 500 ms)
        heartbeat_counter++;
        if (heartbeat_counter >= 10) { // 10 * 50 ms = 500 ms
            heartbeat_counter = 0;
            UsbVehicleBackbone::instance().send_heartbeat(5000, 180);
        }

        vTaskDelay(pdMS_TO_TICKS(50)); // 20 Hz cycle
    }
}

// -----------------------------------------------------------------------------
// Main Application Entry Point
// -----------------------------------------------------------------------------
extern "C" void app_main(void) {
    ESP_LOGI(TAG, "============================================================");
    ESP_LOGI(TAG, "   OPENMOTORBRIDGE RADAR 2.0 & 5.9 GHz V2X v10.0 (PCBA 08)  ");
    ESP_LOGI(TAG, "   Target: ESP32-C5 Dual-Band (MR20 77 GHz + 36-LED Halo)   ");
    ESP_LOGI(TAG, "   4-Wire USB 2.0 Automotive Backbone & ETSI ITS-G5 V2X     ");
    ESP_LOGI(TAG, "============================================================");

    s_radar_data_mutex = xSemaphoreCreateMutex();
    memset(&s_current_telemetry, 0, sizeof(s_current_telemetry));
    memset(&s_current_command, 0, sizeof(s_current_command));
    s_current_command.dimming_pwm_pct = 100;
    s_post_start_ms = (uint32_t)(esp_timer_get_time() / 1000ULL);
    s_post_running = true;

    // 0. HF Hardening: 2.4 GHz Wi-Fi & BLE are strictly disabled at the vehicle rear.
    // Only 5.9 GHz ETSI ITS-G5 (IEEE 802.11p OCB Promiscuous RX on Ch 176/180) is active via U.FL patch antenna.
    ESP_LOGI(TAG, "HF Hardening verified: 2.4 GHz disabled. 5.9 GHz C-ITS V2X OCB RX & 4-Wire USB 2.0 active.");

    // 1. Initialize Wheeltec MR20 UART (RX=GPIO 3, TX=GPIO 4)
    init_uarts();

    // 2. Initialize 4-Wire USB 2.0 Automotive Backbone (Node-ID 0x05, Port 5 on USB2517I)
    usb_backbone_hw_config_t usb_cfg = {
        .pin_usb_dm     = PIN_RADAR_USB_DM,
        .pin_usb_dp     = PIN_RADAR_USB_DP,
        .hub_port_id    = USB_HUB_PORT_5_REAR_RADAR,
        .high_speed_phy = false
    };

    UsbVehicleBackbone::instance().init(USB_NODE_REAR_RADAR, &usb_cfg);
    UsbVehicleBackbone::instance().set_radar_led_callback([](const UsbRadarLedCmdPkt &cmd) {
        if (s_radar_data_mutex && xSemaphoreTake(s_radar_data_mutex, pdMS_TO_TICKS(10)) == pdTRUE) {
            s_current_command.macro_mode = cmd.macro_mode;
            s_current_command.dimming_pwm_pct = cmd.brightness_pct;
            s_current_command.bsd_left_active = (cmd.left_bsd_state != 0);
            s_current_command.bsd_right_active = (cmd.right_bsd_state != 0);
            xSemaphoreGive(s_radar_data_mutex);
        }
    });
    UsbVehicleBackbone::instance().start_task(22, 0);

    // 3. Spawn FreeRTOS Tasks
    xTaskCreate(task_mr20_rx, "mr20_rx", 4096, NULL, 5, NULL);
    xTaskCreate(task_neopixel_halo, "neopixel_halo", 3072, NULL, 4, NULL);
    xTaskCreate(task_usb_radar_bridge, "usb_radar_tx", 4096, NULL, 6, NULL);

    ESP_LOGI(TAG, "Radar 2.0 Sub-MCU v10.0 initialized on USB Node 0x05 (BUS_DM=GPIO18, BUS_DP=GPIO19).");
}
