#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_log.h"
#include "esp_sleep.h"
#include "nvs_flash.h"
#include "driver/gpio.h"
#include "esp_adc/adc_oneshot.h"
#include "esp_adc/adc_cali.h"
#include "esp_adc/adc_cali_scheme.h"

#include "main_box_config.h"
#include "audio_dsp_pipeline.h"
#include "ble_service_server.h"
#include "sdio_ring_buffer.h"
#include "webdav_uploader.h"
#include "gnss_omm_bridge.h"
#include "adr_ekf_filter.h"
#include "omm_flasher.h"
#include "can_bus_manager.h"
#include "radar_processor.h"
#include "action_cam_ble_manager.h"
#include "sx1262_lora_engine.h"
#include "tpms_ble_scanner.h"
#include "bluetooth_audio_manager.h"
#include "baro_weather_trend.h"
#include "hardware_inventory.h"
#include "usb_vehicle_backbone.h"
#include "uwb_cartridge_dispatcher.h"
#include "uwb_radar_parser.h"
#include "power_sequencer.h"
#include "pairing_roaming_mgr.h"
#include "group_split_rescue_engine.h"

static const char *TAG = "OMB_MAIN_V10";

// ADC Channels on PCBA 01 (openmotorbridge_main.kicad_pcb)
#define PIN_ADC_BAT         ADC_CHANNEL_0 // U2 Pad 31 (BAT_SENSE via R12/R13)
#define PIN_ADC_NTC_SENSE   ADC_CHANNEL_2 // J5 Pin 3 10k NTC Thermistor (BAT_NTC, GPIO 15 / ADC)
#define PIN_ADC_VIGN        ADC_CHANNEL_3 // U2 Pad 5  (KL15_SENSE, GPIO 4)
#define PIN_STATUS_LED      PIN_MAIN_RGB_LED_DATA // U2 Pad 28 (GPIO 48 WS2812B-2020)

static adc_oneshot_unit_handle_t adc1_handle = NULL;
static adc_cali_handle_t adc1_cali_handle = NULL;

// Power Supervisor Schwellwerte & Timing
#define VOLTAGE_IGN_THRESHOLD_V     11.8f // Zündung EIN/AUS Schwelle
#define VOLTAGE_CUTOFF_AGM_V        11.8f // Hard Cut-off Blei/AGM
#define VOLTAGE_UPS_LOW_V            3.4f // LiPo-USV Tiefentladeschutz
#define RUN_DOWN_TIMEOUT_SEC         900  // 15 Minuten WebDAV & GPX Run-Down
#define HIBERNATE_TIMEOUT_SEC       259200 // 72 Stunden -> ULP Hibernate (< 20 µA)

static bool s_ignition_active = false;
static float s_v_ign = 12.6f;
static float s_v_bat = 4.1f;
static float s_ntc_temp_c = 24.5f;
static float s_last_speed_kmh = 0.0f;

// WS2812B Status LED State Machine
typedef enum {
    LED_NORMAL_PULSE_GREEN,
    LED_BLE_PAIRING_BLUE,
    LED_UPS_BATTERY_YELLOW,
    LED_WARNING_ERROR_RED,
    LED_OMM_LEADER_PURPLE,
    LED_ACTIONCAM_MARKER_WHITE
} SystemLedState;

static SystemLedState s_led_state = LED_NORMAL_PULSE_GREEN;

static void set_system_led_state(SystemLedState state) {
    s_led_state = state;
}

static void init_adc(void) {
    adc_oneshot_unit_init_cfg_t init_config = {
        .unit_id = ADC_UNIT_1,
        .ulp_mode = ADC_ULP_MODE_DISABLE,
    };
    ESP_ERROR_CHECK(adc_oneshot_new_unit(&init_config, &adc1_handle));

    adc_oneshot_chan_cfg_t chan_config = {
        .atten = ADC_ATTEN_DB_12,
        .bitwidth = ADC_BITWIDTH_DEFAULT,
    };
    ESP_ERROR_CHECK(adc_oneshot_config_channel(adc1_handle, PIN_ADC_BAT, &chan_config));
    ESP_ERROR_CHECK(adc_oneshot_config_channel(adc1_handle, PIN_ADC_VIGN, &chan_config));
    ESP_ERROR_CHECK(adc_oneshot_config_channel(adc1_handle, PIN_ADC_NTC_SENSE, &chan_config));

    adc_cali_curve_fitting_config_t cali_config = {
        .unit_id = ADC_UNIT_1,
        .chan = PIN_ADC_VIGN,
        .atten = ADC_ATTEN_DB_12,
        .bitwidth = ADC_BITWIDTH_DEFAULT,
    };
    adc_cali_create_scheme_curve_fitting(&cali_config, &adc1_cali_handle);
}

static float read_voltage_vign(void) {
    int raw = 0, voltage_mv = 0;
    if (adc1_handle) {
        adc_oneshot_read(adc1_handle, PIN_ADC_VIGN, &raw);
        if (adc1_cali_handle) {
            adc_cali_raw_to_voltage(adc1_cali_handle, raw, &voltage_mv);
            return (voltage_mv * 11.0f) / 1000.0f;
        }
    }
    return (raw * 3.3f * 11.0f) / 4095.0f;
}

static float read_voltage_bat(void) {
    int raw = 0, voltage_mv = 0;
    if (adc1_handle) {
        adc_oneshot_read(adc1_handle, PIN_ADC_BAT, &raw);
        if (adc1_cali_handle) {
            adc_cali_raw_to_voltage(adc1_cali_handle, raw, &voltage_mv);
            return (voltage_mv * 2.0f) / 1000.0f;
        }
    }
    return (raw * 3.3f * 2.0f) / 4095.0f;
}

static float read_lipo_ntc_temp_c(void) {
    // J5 Pin 3: 10k NTC Thermistor voltage divider on GPIO 15 (BAT_NTC)
    int raw = 0;
    if (adc1_handle) {
        adc_oneshot_read(adc1_handle, PIN_ADC_NTC_SENSE, &raw);
    }
    if (raw <= 100 || raw >= 3950) {
        return 25.0f; // Nominal fallback if benchtop without NTC pack
    }
    return 25.0f + ((2048 - raw) * 0.015f);
}

// -----------------------------------------------------------------------------
// v10.0 Unified 4-Wire USB 2.0 Backbone Callbacks
// -----------------------------------------------------------------------------
static void on_usb_ptt_event(const UsbPttEventPkt &pkt, UsbNodeType source) {
    ESP_LOGI(TAG, "⚡ USB HID PTT Event from Node 0x%02X: Button %d, Event %d (< 1 ms Latenz)",
             (uint8_t)source, pkt.button_id, pkt.event_type);

    uint8_t click_type = 1; // 1 = Short, 2 = Double, 3 = Long
    if (pkt.event_type == USB_PTT_CLICK_DOUBLE) click_type = 2;
    else if (pkt.event_type == USB_PTT_CLICK_LONG) click_type = 3;

    // 1. Priority 1: Modal Smartphone Call Protection (Qualcomm QCC3084 HFP 1.8)
    // Intercepts PTT for AT+ATA / AT+ATH when a phone call is ringing or active!
    if (bt_audio_handle_ptt_event(click_type)) {
        ESP_LOGI(TAG, "📞 PTT event consumed modally by QCC3084 HFP Call Protection.");
        return;
    }

    // 2. Priority 2: Human-in-the-Loop Group Split Confirmation (Doubt-Timer / Rescue Level 2)
    // Double-Click = "Alles OK / Verlassen", Long-Press = "Technischer Stopp / Bitte warten"
    if (group_split_handle_human_loop_ptt(click_type)) {
        return;
    }

    // 3. Normal Handlebar / Pod Button Dispatch
    if (pkt.button_id == USB_BTN_INTERCOM_PTT) {
        uwb_cartridge_toggle_mesh(USB_NODE_POD_BAY1);
    } else if (pkt.button_id == USB_BTN_CAM_HIGHLIGHT) {
        set_system_led_state(LED_ACTIONCAM_MARKER_WHITE);
        action_cam_trigger_hilight_tag("HANDLEBAR_PTT");
        sdio_track_add_video_marker("actioncam_v10", 0);
        vTaskDelay(pdMS_TO_TICKS(200));
        set_system_led_state(s_ignition_active ? LED_NORMAL_PULSE_GREEN : LED_UPS_BATTERY_YELLOW);
    } else if (pkt.button_id == USB_BTN_MEDIA_VOICE) {
        AudioOperationMode next_mode = (AudioOperationMode)((audio_get_operation_mode() + 1) % 3);
        audio_set_operation_mode(next_mode);
    }
}

static void on_usb_front_telemetry(const UsbFrontTelemetryPkt &telem) {
    // 1. Knowles SPH0645LM4H MEMS Fahrtwindpegel -> Dynamische AGC & VOX-Nachführung im DSP
    float speed_kmh = telem.speed_kph_100 / 100.0f;
    s_last_speed_kmh = speed_kmh;
    float heading = telem.heading_deg_100 / 100.0f;
    float noise_gain = (telem.wind_noise_dba > 70) ? (telem.wind_noise_dba - 70) * 0.2f : 0.0f;

    audio_set_front_wind_noise_spl((float)telem.wind_noise_dba);
    audio_set_ambient_transparency(true, speed_kmh, noise_gain);
    audio_update_standstill_proximity(speed_kmh, -40);

    // 2. SAM-M10Q Multi-GNSS Fix + TMP117 + OPT3001 (Sensor-Puck J_SENSOR_EXT)
    if (telem.gnss_fix_type >= 2) {
        double lat = (double)telem.latitude_1e7 / 1e7;
        double lon = (double)telem.longitude_1e7 / 1e7;
        float alt_m = (float)telem.altitude_mm / 1000.0f;
        adr_ekf_update_gnss(lat, lon, alt_m, 1.2f, true);
        gnss_bridge_update_from_telemetry(lat, lon, alt_m, speed_kmh, heading, telem.satellites_used, true);
        group_split_update(speed_kmh, lat, lon, heading);
    }
}

void task_power_supervisor(void *pvParameters) {
    ESP_LOGI(TAG, "v10.0 Power Supervisor Task started (KL15 GPIO 4, TPS25921 Quad eFuse, LM66100 Dual-Power & NTC JEITA)...");
    uint32_t ignition_off_timer_sec = 0;

    while (true) {
        s_v_ign = read_voltage_vign();
        s_v_bat = read_voltage_bat();
        s_ntc_temp_c = read_lipo_ntc_temp_c();

        // Update Dual-Power (LM66100 J3 USB-C vs. 12V) & JEITA NTC Guard
        power_sequencer_update_telemetry(s_v_ign, s_v_bat, s_ntc_temp_c);

        bool ign_now = (s_v_ign >= VOLTAGE_IGN_THRESHOLD_V);

        if (ign_now != s_ignition_active) {
            s_ignition_active = ign_now;
            ESP_LOGI(TAG, "Ignition state changed: %s (V_IGN = %.2f V, V_BAT = %.2f V, NTC = %.1f °C)",
                     s_ignition_active ? "ON" : "OFF", s_v_ign, s_v_bat, s_ntc_temp_c);

            if (s_ignition_active) {
                ignition_off_timer_sec = 0;
                set_system_led_state(LED_NORMAL_PULSE_GREEN);
                find_my_set_dual_beacon(false);
                sdio_track_start_new();
                // Staggered TPS25921 4-Branch eFuse Power-On (T=0 Front, T=200ms Pod1, T=350ms Pod2, T=500ms Radar)
                power_sequencer_trigger_boot();
            } else {
                // Zündung AUS: 15-Minuten Tier-1 Graceful Rundown (ESP32-E22 Wi-Fi 6E WebDAV Sync + Coffee Break NVS)
                ESP_LOGI(TAG, "Initiating Tier-1 Graceful Rundown (15-min Wi-Fi 6E WebDAV Sync + Find-My Dual Beacon)...");
                set_system_led_state(LED_UPS_BATTERY_YELLOW);
                group_split_persist_to_nvs();
                sdio_track_finalize();
                webdav_trigger_sync_sequence();
                find_my_set_dual_beacon(true);
                power_sequencer_trigger_shutdown();
            }

            // Front-Node Zündungs-Sync über 4-Draht USB 2.0 Backbone (USB_CMD_CONFIG 0x11)
            uint8_t ign_payload[2] = { 0x01 /* Sub-Cmd: Ignition State */, (uint8_t)(s_ignition_active ? 1 : 0) };
            UsbVehicleBackbone::instance().send_packet(USB_NODE_FRONT_NODE, USB_CMD_CONFIG, ign_payload, sizeof(ign_payload));
        }

        // Update Central BLE Action-Cam Manager (Auto-Record > 10 km/h, Fuel-Stop Filter, Auto Event-Tagging)
        RadarOverview_t rad_ov = uwb_radar_get_overview();
        action_cam_update_tick(s_last_speed_kmh, s_ignition_active, rad_ov.urgent_alert_active, false);

        // Tier-2 Park Sentry Deep Sleep Transition after 15-min Rundown
        if (!s_ignition_active && !power_sequencer_get_diagnostics().benchtop_usb_only_mode) {
            ignition_off_timer_sec++;
            if (ignition_off_timer_sec >= RUN_DOWN_TIMEOUT_SEC || s_v_bat < VOLTAGE_UPS_LOW_V) {
                ESP_LOGW(TAG, "Entering Tier-2 Park Sentry Deep Sleep (BMI270 + SX1262 LoRa + Find-My active)...");
                sx1262_lora_enter_sentry_mode();
                esp_sleep_enable_ext0_wakeup(PIN_MAIN_KL15_SENSE, 1);
                esp_deep_sleep_start();
            }
        }

        // USB 2.0 Backbone Heartbeat (1 Hz)
        UsbVehicleBackbone::instance().send_heartbeat(5000, (int16_t)(s_ntc_temp_c * 10));

        // Notify PWA Dashboard over NimBLE GATT
        HardwareInventoryState_t hw_st = hw_inventory_get_state();
        CartridgeBayState_t bay1 = uwb_cartridge_get_bay_state(USB_NODE_POD_BAY1);
        CartridgeBayState_t bay2 = uwb_cartridge_get_bay_state(USB_NODE_POD_BAY2);

        GroupStatus_t grp_st = group_split_get_status();
        uint8_t rescue_byte = (uint8_t)grp_st.rescue_level;
        if (grp_st.doubt_timer_active) {
            rescue_byte |= 0x80;
        }

        SystemTelemetry_t telem = {
            .v_ign_volts = s_v_ign,
            .v_bat_volts = s_v_bat,
            .remote_bat_pct = 100, // Wired via Front-Node J_POD_L/R
            .operation_mode = (uint8_t)audio_get_operation_mode(),
            .port1_active = bay1.active,
            .port2_active = bay2.active,
            .pod3_gnss_fix = UsbVehicleBackbone::instance().is_peer_online(USB_NODE_FRONT_NODE),
            .lean_angle_deg = 0,
            .spare = { (uint8_t)grp_st.lifecycle_state, rescue_byte },
            .hw_baseline_mask = hw_st.baseline_mask,
            .hw_current_mask = hw_st.current_mask,
            .hw_lost_mask = hw_st.lost_mask
        };
        ble_server_notify_telemetry(&telem);

        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

extern "C" void app_main(void) {
    ESP_LOGI(TAG, "============================================================");
    ESP_LOGI(TAG, "   OpenMotorBridge v10.0 - Unified 4-Wire USB 2.0 Backbone  ");
    ESP_LOGI(TAG, "   Central Box (PCBA 01: ESP32-S31 + USB2517I + QCC3084)    ");
    ESP_LOGI(TAG, "============================================================");

    // 1. NVS Flash Initialization
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    // 2. Quad Automotive eFuse Power Sequencer (U12 TPS25921) & Status RGB LED (GPIO 48)
    power_sequencer_init();

    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_OUTPUT;
    io_conf.pin_bit_mask = (1ULL << PIN_STATUS_LED);
    gpio_config(&io_conf);
    gpio_set_level(PIN_STATUS_LED, 1);

    init_adc();

    // 3. Initialize Onboard & Bus Subsystems
    hw_inventory_init();
    sx1262_lora_init();             // U10 Semtech SX1262 868 MHz LoRa on PCBA 01
    action_cam_ble_manager_init();  // Central Box Geometric BLE Master (Action-Cam + Find-My)
    audio_dsp_init();               // U3 ES8388 + U9 QCC3084 TDM/I2S DSP Pipeline
    adr_ekf_init();                 // U5 Bosch BMI270 6-Axis IMU + GNSS Sensor Fusion
    sdio_storage_init();            // J2 4-Bit SDIO MicroSD Blackbox
    webdav_uploader_init();
    gnss_omm_bridge_init();
    pairing_roaming_mgr_init();
    group_split_rescue_engine_init();
    omm_flasher_init();             // Central Zero-Disassembly USB-Bus DFU & OTA Engine
    can_bus_manager_init();         // U6 TCAN334G CAN-FD (GPIO 5 / GPIO 6)
    radar_processor_init();
    ble_server_init();
    tpms_ble_scanner_init();
    bluetooth_audio_manager_init(); // U9 Qualcomm QCC3084 BT 5.4 (GPIO 1 / 2 / 3)
    baro_weather_init();

    // 4. Start Unified 4-Wire USB 2.0 Automotive Backbone (U8 USB2517I-JZX Port 1: GPIO 19/20)
    UsbVehicleBackbone::instance().init(USB_NODE_CENTRAL_BOX);
    UsbVehicleBackbone::instance().set_ptt_callback(on_usb_ptt_event);
    UsbVehicleBackbone::instance().set_telemetry_callback(on_usb_front_telemetry);
    UsbVehicleBackbone::instance().start_task(22, 0);

    uwb_cartridge_dispatcher_init();
    uwb_radar_parser_init();

    // 5. Boot-Time Hardware Inventory Scan & POST Matrix Dispatch to PCBA 08
    hw_inventory_scan_and_evaluate();
    HardwareInventoryState_t init_hw = hw_inventory_get_state();
    if (init_hw.has_critical_loss) {
        set_system_led_state(LED_WARNING_ERROR_RED);
        ESP_LOGW(TAG, "⚠️ System starts with HARDWARE LOSS: Check missing USB/BLE modules!");
    } else {
        set_system_led_state(LED_NORMAL_PULSE_GREEN);
    }

    // 6. Launch FreeRTOS Tasks with strict Dual-Core Isolation
    // CORE 1: Deterministic Real-Time Audio DSP Pipeline (48 kHz / 24-Bit)
    xTaskCreatePinnedToCore(task_audio_dsp, "AudioDSP", 8192, NULL, configMAX_PRIORITIES - 1, NULL, 1);

    // CORE 0: USB 2.0 Backbone, Sensor-Fusion, CAN-FD, LoRa, BLE & Power Supervisor
    xTaskCreatePinnedToCore(task_adr_ekf_fusion, "ADR_EKF", 4096, NULL, 15, NULL, 0);
    xTaskCreatePinnedToCore(task_can_bus_manager, "CAN_Bus", 4096, NULL, 16, NULL, 0);
    xTaskCreatePinnedToCore(task_radar_processor, "RadarProc", 4096, NULL, 16, NULL, 0);
    xTaskCreatePinnedToCore(task_ble_services, "BLE_Server", 6144, NULL, 10, NULL, 0);
    xTaskCreatePinnedToCore(task_power_supervisor, "PowerSup", 4096, NULL, 14, NULL, 0);

    ESP_LOGI(TAG, "✓ OpenMotorBridge v10.0 Central Box (PCBA 01) is fully OPERATIONAL.");
}
