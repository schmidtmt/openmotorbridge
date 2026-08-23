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

#include "audio_dsp_pipeline.h"
#include "cartridge_onewire.h"
#include "opto_pulse_sequencer.h"
#include "ble_service_server.h"
#include "ble_handlebar_client.h"
#include "sdio_ring_buffer.h"
#include "webdav_uploader.h"
#include "gnss_omm_bridge.h"

static const char *TAG = "OMB_MAIN";

// GPIO Pin-Definitionen (v8.0 Pinout laut docs/de/02_pcb_hardware_pinout.md)
#define PIN_ADC_BAT         ADC_CHANNEL_0 // GPIO 1
#define PIN_ONEWIRE_ID      GPIO_NUM_2
#define PIN_ADC_LINE_LVL    ADC_CHANNEL_2 // GPIO 3
#define PIN_ADC_VIGN        ADC_CHANNEL_3 // GPIO 4
#define PIN_PORT1_KEY       GPIO_NUM_5
#define PIN_PORT1_VCC_EN    GPIO_NUM_6
#define PIN_PORT2_KEY       GPIO_NUM_7
#define PIN_PORT2_VCC_EN    GPIO_NUM_8
#define PIN_STATUS_LED      GPIO_NUM_48

// ADC Handles
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
static uint8_t s_handlebar_battery_pct = 100;
static bool s_is_usb_msc_mode = false;

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
    // Hardware-Treiber Aktualisierung fuer WS2812B an GPIO 48
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
    ESP_ERROR_CHECK(adc_oneshot_config_channel(adc1_handle, PIN_ADC_LINE_LVL, &chan_config));

    // Kalibrierungs-Initialisierung (Curve Fitting für ESP32-S3)
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
            // Teiler 1:11 (100k / 10k)
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
            // Teiler 1:2 (100k / 100k)
            return (voltage_mv * 2.0f) / 1000.0f;
        }
    }
    return (raw * 3.3f * 2.0f) / 4095.0f;
}

static void check_and_enter_usb_msc_mode(void) {
    // Wenn 5V VBUS am USB-C Port anliegt, aber Zündung AUS ist -> Minimaler USB MSC Boot
    s_v_ign = read_voltage_vign();
    if (s_v_ign < 5.0f) { // Kein KL15 Bordnetz aktiv -> Reiner USB-Betrieb
        ESP_LOGI(TAG, "USB-C VBUS detected without vehicle ignition. Entering Minimal USB MSC Mode...");
        s_is_usb_msc_mode = true;
        set_system_led_state(LED_BLE_PAIRING_BLUE);
        sdio_storage_init();
        // Exponiert MicroSD als USB Flash Drive (TinyUSB MSC Stack)
        ESP_LOGI(TAG, "MicroSD exposed as USB Flash Drive 'OPENMOTOR'. Audio/Radios remain isolated.");
        while (true) {
            vTaskDelay(pdMS_TO_TICKS(1000));
        }
    }
}

void task_power_supervisor(void *pvParameters) {
    ESP_LOGI(TAG, "Power Supervisor Task started (KL15, 3-Tier Sleep & USV Monitoring)...");

    uint32_t ignition_off_timer_sec = 0;

    while (true) {
        s_v_ign = read_voltage_vign();
        s_v_bat = read_voltage_bat();

        bool ign_now = (s_v_ign >= VOLTAGE_IGN_THRESHOLD_V);

        if (ign_now != s_ignition_active) {
            s_ignition_active = ign_now;
            ESP_LOGI(TAG, "Ignition state changed: %s (V_IGN = %.2f V, V_BAT = %.2f V)",
                     s_ignition_active ? "ON" : "OFF", s_v_ign, s_v_bat);

            if (s_ignition_active) {
                ignition_off_timer_sec = 0;
                set_system_led_state(LED_NORMAL_PULSE_GREEN);
                sdio_track_start_new();
            } else {
                // Zündung AUS: 15-Minuten Graceful Rundown einleiten
                ESP_LOGI(TAG, "Initiating Graceful Shutdown sequence (Tier 1 Rundown)...");
                set_system_led_state(LED_UPS_BATTERY_YELLOW);
                sdio_track_finalize();
                webdav_trigger_sync_sequence();
            }
        }

        // Bei Zündung AUS: Nachlaufzeit zählen & 3-Stufen Schlaf-Kaskade steuern
        if (!s_ignition_active) {
            ignition_off_timer_sec++;

            // Tier 2: Nach 15 Minuten Rundown -> Deep Sleep (< 100 µA)
            if (ignition_off_timer_sec >= RUN_DOWN_TIMEOUT_SEC || s_v_bat < VOLTAGE_UPS_LOW_V) {
                ESP_LOGW(TAG, "Entering Tier 2 Deep Sleep mode (< 100 µA)...");
                // Pod-Stromversorgungen trennen
                gpio_set_level(PIN_PORT1_VCC_EN, 0);
                gpio_set_level(PIN_PORT2_VCC_EN, 0);

                // Wake-Up via KL15 Flankenerkennung (GPIO 4)
                esp_sleep_enable_ext0_wakeup(GPIO_NUM_4, 1);
                esp_deep_sleep_start();
            }
        }

        // Telemetrie an PWA senden
        SystemTelemetry_t telem = {
            .v_ign_volts = s_v_ign,
            .v_bat_volts = s_v_bat,
            .remote_bat_pct = s_handlebar_battery_pct,
            .operation_mode = (uint8_t)audio_get_operation_mode(),
            .port1_active = true,
            .port2_active = true,
            .pod3_gnss_fix = true,
            .lean_angle_deg = 0.0f
        };
        ble_server_notify_telemetry(&telem);

        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

static void on_handlebar_button_event(uint8_t button_id, bool long_press) {
    ESP_LOGI(TAG, "Handlebar Button Event: Button %d, LongPress: %d", button_id, long_press);
    if (button_id == 1) { // Mesh Toggle Button
        opto_port1_toggle_mesh();
    } else if (button_id == 2) { // Shutter / Actioncam Highlight Marker
        set_system_led_state(LED_ACTIONCAM_MARKER_WHITE);
        sdio_track_add_video_marker("gopro_hero12", 0);
        vTaskDelay(pdMS_TO_TICKS(200));
        set_system_led_state(s_ignition_active ? LED_NORMAL_PULSE_GREEN : LED_UPS_BATTERY_YELLOW);
    } else if (button_id == 3) { // Mode Switch
        AudioOperationMode next_mode = (AudioOperationMode)((audio_get_operation_mode() + 1) % 3);
        audio_set_operation_mode(next_mode);
    }
}

static void on_handlebar_battery_event(uint8_t battery_percent) {
    s_handlebar_battery_pct = battery_percent;
    ESP_LOGI(TAG, "Handlebar CR2032 Battery: %d%%", battery_percent);
    if (battery_percent <= 15) {
        ESP_LOGW(TAG, "CR2032 Battery LOW (<= 15%%)! Triggering Alert LED & CAN Warning.");
        set_system_led_state(LED_WARNING_ERROR_RED);
    }
}

extern "C" void app_main(void) {
    ESP_LOGI(TAG, "==================================================");
    ESP_LOGI(TAG, "   OpenMotorBridge v8.0 - Booting ESP32-S3 Core   ");
    ESP_LOGI(TAG, "==================================================");

    // 1. NVS Initialisierung
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    // 2. Hardware Power-Gates & GPIOs
    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_OUTPUT;
    io_conf.pin_bit_mask = (1ULL << PIN_PORT1_VCC_EN) | (1ULL << PIN_PORT2_VCC_EN) | (1ULL << PIN_STATUS_LED);
    gpio_config(&io_conf);

    gpio_set_level(PIN_PORT1_VCC_EN, 1);
    gpio_set_level(PIN_PORT2_VCC_EN, 1);
    gpio_set_level(PIN_STATUS_LED, 1);

    init_adc();

    // 3. USB Mass Storage Class Minimal Boot Check
    check_and_enter_usb_msc_mode();

    // 4. Subsysteme initialisieren
    opto_sequencer_init();
    audio_dsp_init();
    cartridge_onewire_init();
    sdio_storage_init();
    webdav_uploader_init();
    gnss_omm_bridge_init();
    ble_server_init();
    ble_handlebar_client_init(on_handlebar_button_event, on_handlebar_battery_event);

    set_system_led_state(LED_NORMAL_PULSE_GREEN);
    ESP_LOGI(TAG, "All subsystems initialized. Launching FreeRTOS tasks...");

    // 5. FreeRTOS Tasks starten mit strikter Core-Trennung
    // CORE 1: Echtzeit-Audio DSP Pipeline (Höchste Priorität)
    xTaskCreatePinnedToCore(task_audio_dsp, "AudioDSP", 8192, NULL, configMAX_PRIORITIES - 1, NULL, 1);

    // CORE 0: Kommunikation, Busse & Systemüberwachung
    xTaskCreatePinnedToCore(task_ble_services, "BLE_Server", 6144, NULL, 5, NULL, 0);
    xTaskCreatePinnedToCore(task_cartridge_manager, "Cartridge1W", 4096, NULL, 4, NULL, 0);
    xTaskCreatePinnedToCore(task_rear_pod_bridge, "RearPodBridge", 4096, NULL, 4, NULL, 0);
    xTaskCreatePinnedToCore(task_power_supervisor, "PowerSup", 4096, NULL, 2, NULL, 0);

    ESP_LOGI(TAG, "OpenMotorBridge v8.0 is fully OPERATIONAL.");
}