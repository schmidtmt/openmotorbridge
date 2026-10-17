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
    uint64_t uid = 0;
    esp_read_mac(reinterpret_cast<uint8_t*>(&uid), ESP_MAC_WIFI_STA);

    ESP_LOGI(TAG, "Broadcasting Cartridge Announce: Class=0x01, Model=0x%04X, UID=0x%016llX",
             s_model_id, (unsigned long long)uid);

    UwbVehicleBackbone::instance().send_cartridge_announce(0x01, s_model_id, uid, 3300);
}

#include "cartridge_ble_profile.h"
#include "cartridge_ble_client.h"

// Active BLE Profile Configuration (synchronized with active profile)
static CartridgeBleConfig_t s_active_ble_config = {
    .supported = true,
    .flavor = BLE_FLAVOR_SENA_RC_GATT,
    .device_prefix = "SPIDER",
    .service_uuid = 0xFFE0,
    .fallback_to_mechatronics_on_disconnect = true,
    .can_power_boot = false, // Always false (cold-boot requires physical mechatronics)
    .can_power_off = true,
    .can_mesh_toggle = true,
    .can_group_toggle = true,
    .can_volume = true,
    .can_channel_select = true,
    .can_mic_mute = true,
    .can_telemetry = true,
    .can_le_audio_lc3 = false
};

static esp_err_t execute_smart_command(uint8_t opcode, uint16_t duration_ms) {
    // 1. Power Boot (0x01) ALWAYS requires physical Mechatronics
    // (Headset BT chip is completely dead / unpowered when shut down)
    if (opcode == CARTRIDGE_OPCODE_POWER_BOOT) {
        ESP_LOGI(TAG, "⚡ Power Boot (0x01) -> Enforcing physical Mechatronic actuator pulse.");
        esp_err_t err = CartridgeMechatronics::instance().execute_opcode(opcode, duration_ms);
        // After booting the headset, trigger BLE auto-connect to establish digital link
        CartridgeBleClient::instance().trigger_connect();
        return err;
    }

    // 2. Primary Path: Use digital BLE GATT command if available and connected
    if (CartridgeBleClient::instance().is_connected()) {
        esp_err_t ble_err = CartridgeBleClient::instance().send_command(opcode);
        if (ble_err == ESP_OK) {
            ESP_LOGI(TAG, "✓ Opcode 0x%02X executed via BLE (< 5 ms, 0 mechanical wear).", opcode);
            return ESP_OK;
        }
        ESP_LOGW(TAG, "⚠️ BLE command TX returned error (0x%X) -> Falling back to physical click sequence!", ble_err);
    }

    // 3. Mechatronic Fallback Path:
    // If BLE is not supported (e.g. PMR446), disconnected, or transmission failed -> execute physical click sequence!
    ESP_LOGI(TAG, "🔧 Executing physical Mechatronic click sequence for Opcode 0x%02X.", opcode);
    return CartridgeMechatronics::instance().execute_opcode(opcode, duration_ms);
}

// -----------------------------------------------------------------------------
// Opcode Execution Callback (Dispatched from Central Box via UWB)
// -----------------------------------------------------------------------------
static void on_cartridge_opcode_received(const UwbCartridgeOpcodePkt& op, UwbNodeType source) {
    ESP_LOGI(TAG, "UWB Opcode RX from 0x%02X: Opcode=0x%02X, Pulse=%u ms",
             (uint8_t)source, op.opcode, op.pulse_duration_ms);

    esp_err_t err = execute_smart_command(op.opcode, op.pulse_duration_ms);

    // Send Acknowledgment back to Central Box
    uint16_t exec_us = static_cast<uint16_t>((op.pulse_duration_ms > 0 ? op.pulse_duration_ms : 150) * 1000);
    uint8_t act_mask = CartridgeMechatronics::instance().get_active_mask();
    uint8_t result = (err == ESP_OK) ? 0x00 : 0x01; // 0x00 = Success

    UwbVehicleBackbone::instance().send_cartridge_ack(UWB_NODE_CENTRAL_BOX,
                                                      op.seq_token,
                                                      op.opcode,
                                                      result,
                                                      act_mask,
                                                      exec_us);
}

static void on_generic_packet_received(UwbBackbonePktType type, const uint8_t* payload, size_t len, UwbNodeType source) {
    (void)source;
    if (type == UWB_PKT_AUDIO_STREAM_DOWN && len >= sizeof(UwbAudioStreamDownPkt)) {
        const UwbAudioStreamDownPkt* down = reinterpret_cast<const UwbAudioStreamDownPkt*>(payload);

        // 1. Sub-Kanal 2: Zero-Latency Voice (< 1 ms via ES8388 DAC direct to Intercom Mic Pin)
        int16_t voice_buf[UWB_AUDIO_DOWN_VOICE_SAMPLES];
        memcpy(voice_buf, down->sub_voice, sizeof(voice_buf));
        CartridgeAudioCodec::instance().write_voice_mic(voice_buf, UWB_AUDIO_DOWN_VOICE_SAMPLES);

        // 2. Sub-Kanal 0 & 1: Stereo Media to Bluetooth A2DP Source buffer (for native Mesh Music Sharing)
        int16_t music_l_buf[UWB_AUDIO_DOWN_MUSIC_SAMPLES];
        int16_t music_r_buf[UWB_AUDIO_DOWN_MUSIC_SAMPLES];
        memcpy(music_l_buf, down->sub_music_l, sizeof(music_l_buf));
        memcpy(music_r_buf, down->sub_music_r, sizeof(music_r_buf));
        CartridgeAudioCodec::instance().push_music_samples(music_l_buf, music_r_buf, UWB_AUDIO_DOWN_MUSIC_SAMPLES);
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

        // 2. BLE Central connection supervision & reconnect
        CartridgeBleClient::instance().update();

        // 3. Periodic UWB Heartbeat & Status (every 500 ms)
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

    // 4. Initialize BLE Client Subsystem & apply initial profile config
    CartridgeBleClient::instance().init();
    CartridgeBleClient::instance().configure(s_active_ble_config);

    // 5. Initialize All-UWB Backbone (DW3110)
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
    UwbVehicleBackbone::instance().set_cartridge_opcode_callback(on_cartridge_opcode_received);
    UwbVehicleBackbone::instance().set_generic_packet_callback(on_generic_packet_received);
    UwbVehicleBackbone::instance().start_task(22, 0);

    // 5. Send initial Announce frame to Central Box
    send_cartridge_announce();

    // 6. Spawn Supervisor Task & Real-Time Audio Upstream Task
    xTaskCreate(cartridge_supervisor_task, "cartridge_sup", 3072, NULL, 5, NULL);
    xTaskCreate(cartridge_audio_upstream_task, "cartridge_audio_up", 4096, NULL, 10, NULL);

    ESP_LOGI(TAG, "Smart Cartridge operational in %s.",
             s_local_bay_node == UWB_NODE_CARTRIDGE_BAY1 ? "BAY 1 (Links)" : "BAY 2 (Rechts)");
}
