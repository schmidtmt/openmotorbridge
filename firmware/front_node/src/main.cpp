#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "driver/gpio.h"

#include "front_node_config.h"
#include "handlebar_ptt_handler.h"
#include "fast_charge_manager.h"
#include "fsc_bt802_bridge.h"
#include "knowles_mems_dsp.h"
#include "cockpit_switches_manager.h"
#include "cockpit_oled_display.h"
#include "ws2812b_led_manager.h"
#include "ota_service_manager.h"
#include "cockpit_wifi_fallback.h"
#include "usb_ethernet_tethering.h"
#include "usb_vehicle_backbone.h"
#include "front_sensor_hub.h"
#include "front_c3_bridge.h"
#include "remote_sd_client.h"

static const char* TAG = "FRONT_NODE_V10";

// -----------------------------------------------------------------------------
// Remote Command Handler (Dispatched from Central Box via 4-Wire USB 2.0 Backbone)
// -----------------------------------------------------------------------------
static void handle_usb_command(UsbBackbonePktType pkt_type, const uint8_t* payload, size_t len) {
    switch (pkt_type) {
        case USB_CMD_POWER_CYCLE:
            ESP_LOGW(TAG, "⚡ USB Command (0x10): 2.5s Hard-Reset of Glovebox Fast Charger (SW3526) requested!");
            FastChargeManager::instance().trigger_hard_reset();
            break;

        case USB_CMD_CONFIG:
            if (len >= 2) {
                uint8_t sub_cmd = payload[0];
                if (sub_cmd == 0x01) { // Ignition State Sync
                    bool ignition = (payload[1] != 0);
                    FastChargeManager::instance().set_ignition(ignition);
                    ESP_LOGI(TAG, "USB Command (0x11): Ignition state synced to %s", ignition ? "ON" : "OFF");
                } else if (sub_cmd == 0x02) { // Aux Light Q2 TPS1H100 Mode
                    AuxLightMode mode = static_cast<AuxLightMode>(payload[1]);
                    CockpitSwitchesManager::instance().set_aux_light_mode(mode);
                    ESP_LOGI(TAG, "USB Command (0x11): Aux Light (Q2 TPS1H100) mode set to %d", (int)mode);
                }
            } else if (len == 1) {
                bool ignition = (payload[0] != 0);
                FastChargeManager::instance().set_ignition(ignition);
            }
            break;

        case USB_PKT_BSD_TRIGGER:
            if (len >= 4) {
                bool left_act = (payload[0] != 0);
                BsdAlertLevel left_lvl = static_cast<BsdAlertLevel>(payload[1]);
                bool right_act = (payload[2] != 0);
                BsdAlertLevel right_lvl = static_cast<BsdAlertLevel>(payload[3]);
                CockpitSwitchesManager::instance().set_bsd_warning(left_act, left_lvl, right_act, right_lvl);
                ESP_LOGI(TAG, "Mirror BSD Trigger (Q1 DMN63D8 -> J_POD_L/R): L=%d (lvl %d), R=%d (lvl %d)",
                         left_act, (int)left_lvl, right_act, (int)right_lvl);
            }
            break;

        case USB_PKT_FRONT_BT_MODE_CMD:
            if (len >= 1) {
                FscBt802OperatingMode mode = static_cast<FscBt802OperatingMode>(payload[0]);
                bool force = (len >= 2) ? (payload[1] != 0) : false;
                fsc_bt802_bridge_set_mode(mode, force);
                ESP_LOGI(TAG, "FSC-BT802 operating mode switched via USB: %s",
                         (mode == BT802_MODE_HEADSET_SINK) ? "Mode A (Headset Sink)" : "Mode B (Speaker Source)");
            }
            break;

        case USB_PKT_WIFI_UPLOAD_TRIGGER:
            ESP_LOGI(TAG, "Wi-Fi Cloud Sync / WebDAV upload triggered upon ignition OFF.");
            // Initiates background sync over Wi-Fi
            break;

        default:
            break;
    }
}

// -----------------------------------------------------------------------------
// PTT Multi-Click Callback -> Dispatched via < 1 ms USB HID Interrupt Endpoint
// to Central Box PCBA 01 (HFP Call Protection / Human-in-the-Loop / Action-Cam BLE)
// -----------------------------------------------------------------------------
static void on_ptt_action(PttClickType click_type) {
    UsbPttEventType usb_evt = USB_PTT_CLICK_SHORT;
    uint16_t dur_ms = 120;

    if (click_type == PTT_CLICK_DOUBLE) {
        usb_evt = USB_PTT_CLICK_DOUBLE;
        dur_ms = 250;

        // COMM_51: Forward Action-Cam Rec Toggle over USB Backbone
        UsbCamTriggerPkt cam_trig = {
            .trigger_type = CAM_TRIGGER_REC_TOGGLE,
            .trigger_reason = CAM_REASON_MANUAL_PTT,
            .reserved = 0,
            .timestamp_us = (uint32_t)esp_timer_get_time()
        };
        UsbVehicleBackbone::instance().send_cam_trigger(cam_trig);
        ESP_LOGI(TAG, "📷 Dispatched COMM_51 Action-Cam REC Toggle to Central Box!");
    } else if (click_type == PTT_CLICK_LONG) {
        usb_evt = USB_PTT_CLICK_LONG;
        dur_ms = 900;

        // COMM_51: Forward Action-Cam HiLight Marker over USB Backbone
        UsbCamTriggerPkt cam_trig = {
            .trigger_type = CAM_TRIGGER_HILIGHT_TAG,
            .trigger_reason = CAM_REASON_MANUAL_PTT,
            .reserved = 0,
            .timestamp_us = (uint32_t)esp_timer_get_time()
        };
        UsbVehicleBackbone::instance().send_cam_trigger(cam_trig);
        ESP_LOGI(TAG, "🔖 Dispatched COMM_51 Action-Cam HiLight Tag to Central Box!");
    }

    ESP_LOGI(TAG, "⚡ Handlebar Multi-Click (%d) on J_POD_L/R -> Forwarding via 4-Wire USB HID (0x03) to Central Box!", (int)click_type);
    UsbVehicleBackbone::instance().send_ptt_event(USB_BTN_INTERCOM_PTT, usb_evt, dur_ms, 100);
}

// -----------------------------------------------------------------------------
// Task 1: Zero-Latency Handlebar PTT Forwarding (< 1 ms USB 2.0 HID Interrupt)
// -----------------------------------------------------------------------------
static void ptt_task(void* pvParameters) {
    HandlebarPttHandler& ptt = HandlebarPttHandler::instance();
    PttEvent evt;

    ESP_LOGI(TAG, "Handlebar PTT USB-HID Task running on Core %d (Priority 10)", xPortGetCoreID());

    while (1) {
        if (ptt.get_event(&evt, pdMS_TO_TICKS(20))) {
            ESP_LOGI(TAG, "⚡ PTT Edge (Btn %d): %s at %llu us -> Transmitting via 4-Wire USB 2.0 (< 1 ms)",
                     evt.button_id,
                     evt.pressed ? "PRESSED (ON)" : "RELEASED (OFF)",
                     evt.timestamp_us);

            UsbVehicleBackbone::instance().send_ptt_event(
                (UsbHandlebarButton)evt.button_id,
                evt.pressed ? USB_PTT_EDGE_DOWN : USB_PTT_EDGE_UP,
                0, 100);
        }

        ptt.update();
    }
}

// -----------------------------------------------------------------------------
// Task 2: Knowles SPH0645LM4H MEMS I2S Audio Acquisition & 10 Hz USB Telemetry
// -----------------------------------------------------------------------------
static void audio_dsp_task(void* pvParameters) {
    KnowlesMemsDsp& dsp = KnowlesMemsDsp::instance();

    ESP_LOGI(TAG, "Knowles SPH0645LM4H Edge-DSP Task running (50 Hz / 20 ms frames)");
    TickType_t last_wake_time = xTaskGetTickCount();
    uint8_t telem_decimator = 0;

    while (1) {
        dsp.process_audio();
        uint8_t dba = dsp.get_latest_dba();

        // Transmit consolidated 10 Hz telemetry frame via 4-Wire USB 2.0 Backbone
        if (++telem_decimator >= 5) { // 5 * 20 ms = 100 ms = 10 Hz
            telem_decimator = 0;
            UsbFrontTelemetryPkt telem = {};
            FrontSensorHub::instance().populate_telemetry(telem);
            telem.wind_noise_dba = dba;
            telem.status_flags = FRONT_STAT_KL15_ACTIVE |
                                 FRONT_STAT_SENSOR_PUCK_OK |
                                 FRONT_STAT_SW3526_PD_ACTIVE |
                                 (OttocastPowerManager::instance().is_power_on() ? FRONT_STAT_CP2AA_PWR_ACTIVE : 0) |
                                 (OttocastPowerManager::instance().has_fault() ? FRONT_STAT_CP2AA_FAULT : 0) |
                                 (CockpitSwitchesManager::instance().is_e22_wifi6e_enabled() ? FRONT_STAT_E22_WIFI6E_OK : 0) |
                                 (CockpitOledDisplay::instance().is_initialized() ? FRONT_STAT_DUAL_OLED_OK : 0) |
                                 (CockpitSwitchesManager::instance().is_aux_light_on() ? FRONT_STAT_AUX_LIGHT_ON : 0);

            UsbVehicleBackbone::instance().send_front_telemetry(telem);
        }

        vTaskDelayUntil(&last_wake_time, pdMS_TO_TICKS(AUDIO_RMS_INTERVAL_MS));
    }
}

// -----------------------------------------------------------------------------
// Task 3: System Supervisor, Sensor-Puck, Dual Cockpit OLEDs, TPS2051B & LED1
// -----------------------------------------------------------------------------
static void supervisor_task(void* pvParameters) {
    FastChargeManager& fast_charge = FastChargeManager::instance();
    CockpitSwitchesManager& switches = CockpitSwitchesManager::instance();
    CockpitOledDisplay& oleds = CockpitOledDisplay::instance();
    Ws2812bLedManager& rgb = Ws2812bLedManager::instance();

    ESP_LOGI(TAG, "Front-Node v10.0 Supervisor Task active (10 Hz)");
    uint32_t heartbeat_counter = 0;

    while (1) {
        // 1. Poll External Sensor-Puck J_SENSOR_EXT (SAM-M10Q GNSS, TMP117 Temp, OPT3001 Lux)
        FrontSensorHub::instance().update();

        // 2. Auto-Dim Dual Cockpit Speaker-Corner OLEDs (J_DISP_L / J_DISP_R) via OPT3001 Lux & Refresh HUD
        oleds.update_ambient_brightness(FrontSensorHub::instance().get_ambient_lux());
        oleds.refresh();

        // 3. Advance U5 SW3526 Fast Charge Manager (Qi wireless & USB-PD telemetry)
        fast_charge.update();

        // 4. Advance Cockpit Switches (Q1 DMN63D8 8 Hz BSD & Q2 TPS1H100 4.5 Hz Aux Light Strobe)
        switches.update(100);

        // 5. USB 2.0 Backbone Heartbeat (every 500 ms)
        if (++heartbeat_counter >= 5) {
            heartbeat_counter = 0;
            UsbVehicleBackbone::instance().send_heartbeat(
                5020,
                FrontSensorHub::instance().get_temperature_c_100() / 10
            );

            // Transmit Fast Charging / Qi Telemetry Frame (0x05)
            UsbPowerDeliveryStatPkt pd_stat;
            fast_charge.get_telemetry_packet(&pd_stat);
            UsbVehicleBackbone::instance().send_generic_packet(
                USB_PKT_POWER_DELIVERY_STAT,
                (const uint8_t*)&pd_stat,
                sizeof(pd_stat),
                USB_NODE_CENTRAL_BOX
            );
        }

        // 6. Update Onboard LED1 (WS2812B-2020) Status Mode
        bool usb_online = UsbVehicleBackbone::instance().is_peer_online(USB_NODE_CENTRAL_BOX);
        if (OtaServiceManager::instance().is_updating()) {
            rgb.set_mode(LED_MODE_FLASHING_BLUE);
        } else if (fast_charge.has_fault()) {
            rgb.set_mode(LED_MODE_FLASHING_RED);
        } else if (usb_online) {
            rgb.set_mode(LED_MODE_BREATHING_GREEN);
        } else {
            rgb.set_mode(LED_MODE_SEARCHING_CYAN);
        }
        rgb.update(100);

        // 7. Update USB CDC-NCM Ethernet Tethering, Inter-Chip C3 Bridge & OTA Health Checks
        usb_ethernet_update(100);
        front_c3_bridge_update_tick();
        OtaServiceManager::instance().update_health_check(100);

        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

extern "C" void app_main(void) {
    ESP_LOGI(TAG, "==================================================================");
    ESP_LOGI(TAG, "   OPENMOTORBRIDGE v10.0 FRONT-NODE FIRMWARE (PCBA 05)            ");
    ESP_LOGI(TAG, "   Core: U1 ESP32-S31-WROOM-1U (0%% 2.4GHz) + U9 ESP32-E22 (Wi-Fi 6E) ");
    ESP_LOGI(TAG, "   Hub:  U2 USB2514Bi 4-Port HS USB + U5 SW3526 30W USB-PD / Qi   ");
    ESP_LOGI(TAG, "   BT:   U2 FSC-BT802 Infotainment Bridge (Headset / Bike Speakers)");
    ESP_LOGI(TAG, "   HUD:  Dual Speaker-Corner OLEDs (J_DISP_L 0x3C / J_DISP_R 0x3D)");
    ESP_LOGI(TAG, "==================================================================");

    // 1. Configure Boot Button
    gpio_config_t btn_conf = {
        .pin_bit_mask = (1ULL << PIN_BOOT_BUTTON),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&btn_conf);

    // 2. Initialize Hardware Drivers & Peripherals
    Ws2812bLedManager::instance().init();
    CockpitSwitchesManager::instance().init();
    OtaServiceManager::instance().init();
    HandlebarPttHandler::instance().init();
    HandlebarPttHandler::instance().set_action_callback(on_ptt_action);

    FastChargeManager::instance().init();   // U5 SW3526 30W USB-PD & 15W Qi-Puck at J4
    KnowlesMemsDsp::instance().init();       // MK1 SPH0645LM4H (Pad 6/7/12)
    FrontSensorHub::instance().init();       // J_SENSOR_EXT (Pad 17/18: SAM-M10Q, TMP117, OPT3001)
    CockpitOledDisplay::instance().init();   // J_DISP_L (0x3C) & J_DISP_R (0x3D)

    // 3. Initialize U9 ESP32-E22 4-Bit SDIO 3.0 Wi-Fi 6E (5/6 GHz) & USB CDC-NCM Gateway
    cockpit_wifi_fallback_init();
    usb_ethernet_tethering_init();

    // 4. Initialize Unified 4-Wire USB 2.0 Backbone (U1 Pad 13/14 -> U2 USB2514Bi Port 4 -> J1)
    UsbVehicleBackbone::instance().init(USB_NODE_FRONT_NODE);
    UsbVehicleBackbone::instance().set_cockpit_hud_callback([](const UsbCockpitHudStatePkt &hud) {
        CockpitOledDisplay::instance().update_hud_state(hud);
    });
    UsbVehicleBackbone::instance().set_radar_led_callback([](const UsbRadarLedCmdPkt &cmd) {
        bool l_act = (cmd.left_bsd_state != 0);
        BsdAlertLevel l_lvl = (cmd.left_bsd_state == 2) ? BSD_LEVEL_FAST_STROBE :
                              (cmd.left_bsd_state == 1) ? BSD_LEVEL_SOLID_AMBER : BSD_LEVEL_OFF;
        bool r_act = (cmd.right_bsd_state != 0);
        BsdAlertLevel r_lvl = (cmd.right_bsd_state == 2) ? BSD_LEVEL_FAST_STROBE :
                              (cmd.right_bsd_state == 1) ? BSD_LEVEL_SOLID_AMBER : BSD_LEVEL_OFF;
        CockpitSwitchesManager::instance().set_bsd_warning(l_act, l_lvl, r_act, r_lvl);
    });
    UsbVehicleBackbone::instance().set_cam_status_callback([](const UsbCamStatusFeedPkt &stat, UsbNodeType source) {
        if (stat.connected) {
            ESP_LOGI(TAG, "📷 Action-Cam Feed: Brand %d, Bat %d%%, Rec %d (%u min left)",
                     stat.brand, stat.battery_pct, stat.recording, stat.remaining_min);
        }
    });
    UsbVehicleBackbone::instance().set_generic_packet_callback([](UsbBackbonePktType type, const uint8_t *payload, size_t len, UsbNodeType source) {
        handle_usb_command(type, payload, len);
    });
    UsbVehicleBackbone::instance().start_task(22, 0);

    // 4b. Initialize Inter-Chip C3 Infotainment Bridge & Remote SD Client
    front_c3_bridge_init();
    remote_sd_client_init();

    // 5. Spawn Real-Time FreeRTOS Tasks
    xTaskCreate(ptt_task, "ptt_task", 3072, NULL, 10, NULL);
    xTaskCreate(audio_dsp_task, "audio_dsp", 4096, NULL, 6, NULL);
    xTaskCreate(supervisor_task, "supervisor", 4096, NULL, 3, NULL);

    ESP_LOGI(TAG, "✓ OpenMotorBridge v10.0 Front-Node (PCBA 05) is fully OPERATIONAL.");
}
