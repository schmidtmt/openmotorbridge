#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_system.h"
#include "esp_mac.h"
#include "driver/gpio.h"

#include "cartridge_config.h"
#include "cartridge_mechatronics.h"
#include "cartridge_audio_codec.h"
#include "uwb_vehicle_backbone.h"
#include "uwb_backbone_types.h"

static const char* TAG = "SMART_CARTRIDGE";

static UwbNodeType s_local_bay_node = UWB_NODE_CARTRIDGE_BAY1;
static uint16_t s_model_id = 0x0101; // Default: Sena SPIDER X Slim (Klasse A)

// -----------------------------------------------------------------------------
// Detect Bay ID from Hardware Strap / Pin
// -----------------------------------------------------------------------------
static UwbNodeType detect_bay_node() {
    gpio_config_t conf = {
        .pin_bit_mask = (1ULL << PIN_BAY_SELECT),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&conf);

    // If pin is grounded (0), Bay 1 Left. If pulled up (1), Bay 2 Right.
    int lvl = gpio_get_level(PIN_BAY_SELECT);
    if (lvl == 0) {
        ESP_LOGI(TAG, "Hardware Bay Detect: Pin 14 is LOW -> Assigning BAY 1 (Links, 0x03)");
        return UWB_NODE_CARTRIDGE_BAY1;
    } else {
        ESP_LOGI(TAG, "Hardware Bay Detect: Pin 14 is HIGH -> Assigning BAY 2 (Rechts, 0x04)");
        return UWB_NODE_CARTRIDGE_BAY2;
    }
}

// -----------------------------------------------------------------------------
// Send Initial Cartridge Announce Frame to Central Box
// -----------------------------------------------------------------------------
static void send_cartridge_announce() {
    UwbCartridgeAnnouncePkt pkt = {};
    pkt.hardware_class = 0x01; // Klasse A (Smart Mechatronics)
    pkt.model_id = s_model_id;
    pkt.status_flags = 0x01;   // Intercom mounted & ready
    pkt.roaming_key_id = 0x00; // Local vehicle master

    // Fetch unique factory MAC / UID
    esp_read_mac(reinterpret_cast<uint8_t*>(&pkt.cartridge_uid), ESP_MAC_WIFI_STA);

    ESP_LOGI(TAG, "Broadcasting Cartridge Announce: Class=0x%02X, Model=0x%04X, UID=0x%016llX",
             pkt.hardware_class, pkt.model_id, (unsigned long long)pkt.cartridge_uid);

    UwbVehicleBackbone::instance().send_packet(UWB_NODE_CENTRAL_BOX, UWB_PKT_CARTRIDGE_ANNOUNCE,
                                               &pkt, sizeof(pkt));
}

// -----------------------------------------------------------------------------
// Opcode Execution Callback (Dispatched from Central Box via UWB)
// -----------------------------------------------------------------------------
static void on_uwb_packet_received(const uint8_t* payload, size_t len, UwbNodeType source) {
    if (!payload || len < sizeof(UwbBackboneHeader)) return;
    const UwbBackboneHeader* hdr = reinterpret_cast<const UwbBackboneHeader*>(payload);

    if (hdr->packet_type == UWB_PKT_CARTRIDGE_OPCODE) {
        if (len >= sizeof(UwbBackboneHeader) + sizeof(UwbCartridgeOpcodePkt)) {
            const UwbCartridgeOpcodePkt* op = reinterpret_cast<const UwbCartridgeOpcodePkt*>(
                payload + sizeof(UwbBackboneHeader));

            ESP_LOGI(TAG, "UWB Opcode RX from 0x%02X: Opcode=0x%02X, Param=%u ms",
                     (uint8_t)source, op->opcode, op->param_duration_ms);

            esp_err_t err = CartridgeMechatronics::instance().execute_opcode(op->opcode, op->param_duration_ms);

            // Send Acknowledgment back to Central Box
            UwbCartridgeAckPkt ack = {};
            ack.opcode = op->opcode;
            ack.result_code = (err == ESP_OK) ? 0x00 : 0x01; // 0x00 = Success
            ack.execution_time_ms = op->param_duration_ms > 0 ? op->param_duration_ms : 150;
            ack.current_button_state = CartridgeMechatronics::instance().get_active_mask();

            UwbVehicleBackbone::instance().send_packet(UWB_NODE_CENTRAL_BOX, UWB_PKT_CARTRIDGE_ACK,
                                                       &ack, sizeof(ack));
        }
    } else if (hdr->packet_type == UWB_PKT_AUDIO_STREAM_DOWN) {
        if (len >= sizeof(UwbBackboneHeader) + sizeof(UwbAudioStreamDownPkt)) {
            const UwbAudioStreamDownPkt* down = reinterpret_cast<const UwbAudioStreamDownPkt*>(
                payload + sizeof(UwbBackboneHeader));

            // 1. Sub-Kanal 2: Zero-Latency Voice (< 1 ms via ES8388 DAC direct to Intercom Mic Pin)
            CartridgeAudioCodec::instance().write_voice_mic(down->sub_voice, UWB_AUDIO_DOWN_VOICE_SAMPLES);

            // 2. Sub-Kanal 0 & 1: Stereo Media to Bluetooth A2DP Source buffer (for native Mesh Music Sharing)
            CartridgeAudioCodec::instance().push_music_samples(down->sub_music_l, down->sub_music_r, UWB_AUDIO_DOWN_MUSIC_SAMPLES);
        }
    }
}

// -----------------------------------------------------------------------------
// Real-Time Audio Upstream Task (Intercom Headset Out -> UWB Central Box)
// -----------------------------------------------------------------------------
static void cartridge_audio_upstream_task(void* pvParameters) {
    ESP_LOGI(TAG, "Cartridge Audio Upstream Task started (100 Hz)");
    int16_t rx_buf[UWB_AUDIO_UP_SAMPLES];
    uint16_t up_seq = 0;

    while (1) {
        size_t samples_read = CartridgeAudioCodec::instance().read_audio_frames(rx_buf, UWB_AUDIO_UP_SAMPLES);
        if (samples_read > 0) {
            UwbAudioStreamUpPkt up_pkt = {};
            up_pkt.frame_seq = ++up_seq;
            up_pkt.status_flags = 0x01; // Headset stream active
            up_pkt.sample_count = static_cast<uint8_t>(samples_read > UWB_AUDIO_UP_SAMPLES ? UWB_AUDIO_UP_SAMPLES : samples_read);
            memcpy(up_pkt.samples, rx_buf, up_pkt.sample_count * sizeof(int16_t));

            UwbVehicleBackbone::instance().send_packet(UWB_NODE_CENTRAL_BOX, UWB_PKT_AUDIO_STREAM_UP,
                                                       &up_pkt, sizeof(up_pkt));
        }
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

// -----------------------------------------------------------------------------
// Supervisor & Mechatronics Task
// -----------------------------------------------------------------------------
static void cartridge_supervisor_task(void* pvParameters) {
    ESP_LOGI(TAG, "Cartridge Supervisor Task started (50 Hz)");
    TickType_t last_wake = xTaskGetTickCount();
    uint32_t heartbeat_counter = 0;

    while (1) {
        // 1. Advance mechatronics pulse state machine
        CartridgeMechatronics::instance().update();

        // 2. Periodic UWB Heartbeat & Status (every 500 ms)
        heartbeat_counter++;
        if (heartbeat_counter >= 25) { // 25 * 20 ms = 500 ms
            heartbeat_counter = 0;
            UwbVehicleBackbone::instance().send_heartbeat(5000, 100);
        }

        vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(20)); // 50 Hz / 20 ms
    }
}

// -----------------------------------------------------------------------------
// Main Application Entry Point
// -----------------------------------------------------------------------------
extern "C" void app_main(void) {
    ESP_LOGI(TAG, "============================================================");
    ESP_LOGI(TAG, "   OPENMOTORBRIDGE UNIVERSAL SMART CARTRIDGE v3.0           ");
    ESP_LOGI(TAG, "   Target: ESP32-C6 RISC-V (PCBA 03 Rev 3.0)                ");
    ESP_LOGI(TAG, "   All-UWB Deterministic Backbone (Qorvo DW3110 / 6.5 GHz)  ");
    ESP_LOGI(TAG, "============================================================");

    // 1. Detect Bay (Bay 1 Left or Bay 2 Right)
    s_local_bay_node = detect_bay_node();

    // 2. Initialize Mechatronics Actuator Gates (Q1-Q4 AO3400A)
    CartridgeMechatronics::instance().init();

    // 3. Initialize Audio Codec (ES8388)
    CartridgeAudioCodec::instance().init();

    // 4. Initialize All-UWB Backbone (DW3110)
    dw3110_config_t dw_cfg = {
        .spi_host = SPI2_HOST,
        .pin_sck  = PIN_UWB_SCK,
        .pin_mosi = PIN_UWB_MOSI,
        .pin_miso = PIN_UWB_MISO,
        .pin_cs   = PIN_UWB_CS,
        .pin_irq  = PIN_UWB_IRQ,
        .pin_rst  = PIN_UWB_RST,
        .pan_id   = UWB_BACKBONE_PAN_ID,
        .short_addr = static_cast<uint16_t>(s_local_bay_node)
    };

    UwbVehicleBackbone::instance().init(s_local_bay_node, &dw_cfg);
    UwbVehicleBackbone::instance().set_raw_rx_callback(on_uwb_packet_received);
    UwbVehicleBackbone::instance().start_task(22, 0);

    // 5. Send initial Announce frame to Central Box
    send_cartridge_announce();

    // 6. Spawn Supervisor Task & Real-Time Audio Upstream Task
    xTaskCreate(cartridge_supervisor_task, "cartridge_sup", 3072, NULL, 5, NULL);
    xTaskCreate(cartridge_audio_upstream_task, "cartridge_audio_up", 4096, NULL, 10, NULL);

    ESP_LOGI(TAG, "Smart Cartridge operational in %s.",
             s_local_bay_node == UWB_NODE_CARTRIDGE_BAY1 ? "BAY 1 (Links)" : "BAY 2 (Rechts)");
}
