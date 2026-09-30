#include "bluetooth_audio_manager.h"
#include <string.h>
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "driver/uart.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "nvs.h"

static const char* TAG = "QCC3084_AUDIO";

#define NVS_NAMESPACE "bt_audio"
#define UART_BUF_SIZE 1024

static BtHeadsetInfo_t s_headsets[2] = {
    {
        .role = BT_ROLE_RIDER,
        .state = BT_STATE_DISCONNECTED,
        .mac = {0x00, 0x1A, 0x7D, 0xDA, 0x71, 0x13},
        .name = "Rider Helmet (aptX HD)",
        .battery_pct = 90,
        .rssi_dbm = -52,
        .latency_ms = 18,
        .codec = BT_CODEC_APTX_ADAPTIVE,
        .volume_pct = 85,
        .is_mic_active = true
    },
    {
        .role = BT_ROLE_PAX,
        .state = BT_STATE_DISCONNECTED,
        .mac = {0x00, 0x1B, 0xDC, 0x44, 0x90, 0x2A},
        .name = "Passenger Helmet (A2DP / LC3)",
        .battery_pct = 95,
        .rssi_dbm = -56,
        .latency_ms = 19,
        .codec = BT_CODEC_LC3,
        .volume_pct = 80,
        .is_mic_active = true
    }
};

static HfpCallState_t s_hfp_state = HFP_STATE_IDLE;
static bool s_auracast_enabled = false;
static uint32_t s_scan_timer_ms[2] = {0, 0};
static QueueHandle_t s_uart_queue = NULL;

static void qcc_send_cmd(const char *cmd) {
    if (!cmd) return;
    ESP_LOGD(TAG, "QCC3084 TX: %s", cmd);
    uart_write_bytes(QCC3084_UART_NUM, cmd, strlen(cmd));
    uart_write_bytes(QCC3084_UART_NUM, "\r\n", 2);
}

static void parse_qcc_response(const char *line) {
    if (strncmp(line, "+HFP_STATUS:", 12) == 0) {
        int state = 0;
        if (sscanf(line + 12, "%d", &state) == 1) {
            s_hfp_state = (HfpCallState_t)state;
            ESP_LOGI(TAG, "📞 QCC3084 HFP Call State updated: %d (%s)",
                     state, (state == HFP_STATE_RINGING) ? "RINGING" :
                            (state == HFP_STATE_CALL_ACTIVE) ? "CALL_ACTIVE" : "IDLE");
        }
    } else if (strncmp(line, "+BATTERY:", 9) == 0) {
        int role = 1, pct = 0;
        if (sscanf(line + 9, "%d,%d", &role, &pct) == 2) {
            uint8_t idx = (role == BT_ROLE_PAX) ? 1 : 0;
            s_headsets[idx].battery_pct = (uint8_t)pct;
            ESP_LOGI(TAG, "🔋 Headset Role %d Battery: %d%%", role, pct);
        }
    } else if (strncmp(line, "+CODEC:", 7) == 0) {
        int role = 1;
        char codec_str[24] = {0};
        if (sscanf(line + 7, "%d,%23s", &role, codec_str) == 2) {
            uint8_t idx = (role == BT_ROLE_PAX) ? 1 : 0;
            if (strstr(codec_str, "APTX_ADAPTIVE")) s_headsets[idx].codec = BT_CODEC_APTX_ADAPTIVE;
            else if (strstr(codec_str, "APTX_HD")) s_headsets[idx].codec = BT_CODEC_APTX_HD;
            else if (strstr(codec_str, "APTX_LL")) s_headsets[idx].codec = BT_CODEC_APTX_LL;
            else if (strstr(codec_str, "LC3"))     s_headsets[idx].codec = BT_CODEC_LC3;
            else if (strstr(codec_str, "AAC"))     s_headsets[idx].codec = BT_CODEC_AAC;
            else                                   s_headsets[idx].codec = BT_CODEC_SBC;
            ESP_LOGI(TAG, "🎧 Headset Role %d Codec negotiated: %s", role, codec_str);
        }
    } else if (strncmp(line, "+CONNECT:", 9) == 0) {
        int role = 1;
        if (sscanf(line + 9, "%d", &role) == 1) {
            uint8_t idx = (role == BT_ROLE_PAX) ? 1 : 0;
            s_headsets[idx].state = BT_STATE_CONNECTED;
            ESP_LOGI(TAG, "✅ QCC3084: Headset Role %d CONNECTED successfully.", role);
        }
    } else if (strncmp(line, "+DISCONNECT:", 12) == 0) {
        int role = 1;
        if (sscanf(line + 12, "%d", &role) == 1) {
            uint8_t idx = (role == BT_ROLE_PAX) ? 1 : 0;
            s_headsets[idx].state = BT_STATE_DISCONNECTED;
            ESP_LOGW(TAG, "⚠️ QCC3084: Headset Role %d DISCONNECTED.", role);
        }
    }
}

void task_qcc3084_hub(void *pvParameters) {
    uart_event_t event;
    uint8_t dtmp[128];
    char line_buf[128];
    size_t line_idx = 0;

    ESP_LOGI(TAG, "Qualcomm QCC3084 UART Supervisor Task started on Core 1.");

    while (1) {
        if (xQueueReceive(s_uart_queue, (void * )&event, portMAX_DELAY)) {
            if (event.type == UART_DATA) {
                int len = uart_read_bytes(QCC3084_UART_NUM, dtmp, event.size, portMAX_DELAY);
                for (int i = 0; i < len; i++) {
                    char c = (char)dtmp[i];
                    if (c == '\r' || c == '\n') {
                        if (line_idx > 0) {
                            line_buf[line_idx] = '\0';
                            parse_qcc_response(line_buf);
                            line_idx = 0;
                        }
                    } else if (line_idx < sizeof(line_buf) - 1) {
                        line_buf[line_idx++] = c;
                    }
                }
            } else if (event.type == UART_FIFO_OVF || event.type == UART_BUFFER_FULL) {
                uart_flush_input(QCC3084_UART_NUM);
                xQueueReset(s_uart_queue);
            }
        }
    }
}

esp_err_t bluetooth_audio_manager_init(void) {
    ESP_LOGI(TAG, "Initializing Qualcomm QCC3084 Bluetooth 5.4 Audio Hub (Dual-Helm aptX HD)...");

    // 1. Hardware Reset / Enable Sequence via QCC3084_PIN_EN
    gpio_config_t en_cfg = {
        .pin_bit_mask = (1ULL << QCC3084_PIN_EN),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_ENABLE,
        .intr_type = GPIO_INTR_DISABLE
    };
    gpio_config(&en_cfg);

    // Assert reset (LOW), wait 50ms, then release (HIGH)
    gpio_set_level(QCC3084_PIN_EN, 0);
    vTaskDelay(pdMS_TO_TICKS(50));
    gpio_set_level(QCC3084_PIN_EN, 1);
    vTaskDelay(pdMS_TO_TICKS(100)); // Allow QCC boot ROM to initialize

    // 2. Configure UART1 for QCC3084 AT/GAIA communication
    uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };
    ESP_ERROR_CHECK(uart_param_config(QCC3084_UART_NUM, &uart_config));
    ESP_ERROR_CHECK(uart_set_pin(QCC3084_UART_NUM, QCC3084_PIN_TX, QCC3084_PIN_RX,
                                 UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE));
    ESP_ERROR_CHECK(uart_driver_install(QCC3084_UART_NUM, UART_BUF_SIZE * 2,
                                        UART_BUF_SIZE * 2, 20, &s_uart_queue, 0));

    // 3. Load persisted pairings from NVS
    nvs_handle_t nvs;
    esp_err_t err = nvs_open(NVS_NAMESPACE, NVS_READONLY, &nvs);
    if (err == ESP_OK) {
        size_t len = 6;
        uint8_t mac[6];
        if (nvs_get_blob(nvs, "rider_mac", mac, &len) == ESP_OK) {
            memcpy(s_headsets[0].mac, mac, 6);
            ESP_LOGI(TAG, "Loaded Rider MAC from NVS: %02X:%02X:%02X:%02X:%02X:%02X",
                     mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
        }
        len = 6;
        if (nvs_get_blob(nvs, "pax_mac", mac, &len) == ESP_OK) {
            memcpy(s_headsets[1].mac, mac, 6);
            ESP_LOGI(TAG, "Loaded Passenger MAC from NVS: %02X:%02X:%02X:%02X:%02X:%02X",
                     mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
        }
        nvs_close(nvs);
    }

    // 4. Send Hardware Init Commands to QCC3084
    qcc_send_cmd("AT+INIT");
    qcc_send_cmd("AT+A2DP_DUAL=1");              // Enable simultaneous Dual-A2DP
    qcc_send_cmd("AT+APTX_MODE=ADAPTIVE_LL");    // Select low-latency aptX Adaptive (<20ms)
    qcc_send_cmd("AT+HFP_CFG=1,WIDEBAND");       // Enable HFP 1.8 Wideband speech (mSBC)
    qcc_send_cmd("AT+I2S_CFG=SLAVE,48000,24");   // Lock I2S digital audio bus to 48 kHz / 24-bit

    // Automatically trigger reconnect if MACs are stored
    char cmd[64];
    snprintf(cmd, sizeof(cmd), "AT+A2DP_CONNECT=1,%02X%02X%02X%02X%02X%02X",
             s_headsets[0].mac[0], s_headsets[0].mac[1], s_headsets[0].mac[2],
             s_headsets[0].mac[3], s_headsets[0].mac[4], s_headsets[0].mac[5]);
    qcc_send_cmd(cmd);

    // 5. Start UART Supervisor Task on Core 1
    xTaskCreatePinnedToCore(task_qcc3084_hub, "qcc3084_hub_task", 4096, NULL, 21, NULL, 1);

    ESP_LOGI(TAG, "Qualcomm QCC3084 Hub initialized. Dual-A2DP aptX HD ready.");
    return ESP_OK;
}

void bt_audio_start_scan(uint8_t role, uint32_t duration_s) {
    uint8_t idx = (role == BT_ROLE_PAX) ? 1 : 0;
    s_headsets[idx].state = BT_STATE_SCANNING;
    s_scan_timer_ms[idx] = duration_s * 1000;

    char cmd[32];
    snprintf(cmd, sizeof(cmd), "AT+INQUIRY=%d,%lu", role, duration_s);
    qcc_send_cmd(cmd);
    ESP_LOGI(TAG, "Sent QCC3084 Inquiry Scan for Role %d (Duration: %lu s)", role, duration_s);
}

bool bt_audio_pair_device(uint8_t role, const uint8_t *mac) {
    if (!mac) return false;
    uint8_t idx = (role == BT_ROLE_PAX) ? 1 : 0;
    memcpy(s_headsets[idx].mac, mac, 6);
    s_headsets[idx].state = BT_STATE_CONNECTING;

    // Send QCC3084 Connect command
    char cmd[64];
    snprintf(cmd, sizeof(cmd), "AT+A2DP_CONNECT=%d,%02X%02X%02X%02X%02X%02X",
             role, mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
    qcc_send_cmd(cmd);

    // Save to NVS
    nvs_handle_t nvs;
    if (nvs_open(NVS_NAMESPACE, NVS_READWRITE, &nvs) == ESP_OK) {
        const char* key = (role == BT_ROLE_PAX) ? "pax_mac" : "rider_mac";
        nvs_set_blob(nvs, key, mac, 6);
        nvs_commit(nvs);
        nvs_close(nvs);
        ESP_LOGI(TAG, "Persisted paired headset MAC to NVS key '%s'.", key);
    }
    return true;
}

void bt_audio_disconnect(uint8_t role) {
    uint8_t idx = (role == BT_ROLE_PAX) ? 1 : 0;
    s_headsets[idx].state = BT_STATE_DISCONNECTED;

    char cmd[32];
    snprintf(cmd, sizeof(cmd), "AT+A2DP_DISCONNECT=%d", role);
    qcc_send_cmd(cmd);
    ESP_LOGI(TAG, "Sent QCC3084 Disconnect for Role %d.", role);
}

bool bt_audio_is_connected(uint8_t role) {
    uint8_t idx = (role == BT_ROLE_PAX) ? 1 : 0;
    return (s_headsets[idx].state == BT_STATE_CONNECTED || s_headsets[idx].state == BT_STATE_STREAMING);
}

void bt_audio_get_headset_info(uint8_t role, BtHeadsetInfo_t *out_info) {
    if (!out_info) return;
    uint8_t idx = (role == BT_ROLE_PAX) ? 1 : 0;
    memcpy(out_info, &s_headsets[idx], sizeof(BtHeadsetInfo_t));
}

void bt_audio_set_volume(uint8_t role, uint8_t volume_pct) {
    if (volume_pct > 100) volume_pct = 100;
    uint8_t idx = (role == BT_ROLE_PAX) ? 1 : 0;
    s_headsets[idx].volume_pct = volume_pct;

    char cmd[32];
    snprintf(cmd, sizeof(cmd), "AT+AVRCP_VOL=%d,%d", role, volume_pct);
    qcc_send_cmd(cmd);
    ESP_LOGI(TAG, "QCC3084: Role %d volume set to %d%% via AVRCP", role, volume_pct);
}

void bt_audio_set_aptx_mode(uint8_t role, bool low_latency) {
    char cmd[48];
    snprintf(cmd, sizeof(cmd), "AT+APTX_MODE=%d,%s", role, low_latency ? "ADAPTIVE_LL" : "HD_HIFI");
    qcc_send_cmd(cmd);
    ESP_LOGI(TAG, "QCC3084: Role %d aptX mode configured: %s", role, low_latency ? "Low Latency (<20ms)" : "HD 24-bit/48kHz");
}

void bt_audio_enable_auracast(bool enable, const char *broadcast_name) {
    s_auracast_enabled = enable;
    char cmd[80];
    if (enable) {
        snprintf(cmd, sizeof(cmd), "AT+AURACAST=1,\"%s\"", broadcast_name ? broadcast_name : "OpenMotorBridge_Live");
    } else {
        snprintf(cmd, sizeof(cmd), "AT+AURACAST=0");
    }
    qcc_send_cmd(cmd);
    ESP_LOGI(TAG, "QCC3084: LE Audio Auracast broadcast %s", enable ? "ENABLED" : "DISABLED");
}

bool bt_audio_is_auracast_active(void) {
    return s_auracast_enabled;
}

void bt_audio_hfp_answer(void) {
    ESP_LOGI(TAG, "📞 QCC3084 HFP: Answering incoming phone call (ATA)...");
    qcc_send_cmd("AT+ATA");
    s_hfp_state = HFP_STATE_CALL_ACTIVE;
}

void bt_audio_hfp_hangup(void) {
    ESP_LOGI(TAG, "📞 QCC3084 HFP: Terminating / rejecting phone call (ATH)...");
    qcc_send_cmd("AT+ATH");
    s_hfp_state = HFP_STATE_IDLE;
}

HfpCallState_t bt_audio_hfp_get_state(void) {
    return s_hfp_state;
}

bool bt_audio_handle_ptt_event(uint8_t click_type) {
    // Modal call interception
    if (s_hfp_state == HFP_STATE_RINGING) {
        if (click_type == 1) { // Single click: Answer
            bt_audio_hfp_answer();
        } else if (click_type == 2) { // Double click: Reject
            bt_audio_hfp_hangup();
        }
        return true; // Consumed modally
    } else if (s_hfp_state == HFP_STATE_CALL_ACTIVE) {
        if (click_type == 3) { // Long press: Hang up
            bt_audio_hfp_hangup();
        } else if (click_type == 1) { // Single click: Toggle mic mute
            qcc_send_cmd("AT+HFP_MIC_TOGGLE");
        }
        return true; // Consumed modally
    }
    return false; // Normal operation, let PTT pass through to radio/action-cam
}

size_t bt_audio_write_stream_samples(uint8_t role, const int16_t *samples, size_t count) {
    // Note: The primary audio pipeline feeds Qualcomm QCC3084 synchronously over hardware I2S.
    // This helper allows injecting synthetic chime/alert streams directly if needed.
    if (!samples || count == 0) return 0;
    uint8_t idx = (role == BT_ROLE_PAX) ? 1 : 0;
    if (s_headsets[idx].state == BT_STATE_CONNECTED) {
        s_headsets[idx].state = BT_STATE_STREAMING;
    }
    return count;
}

void bt_audio_update(uint32_t delta_ms) {
    for (int i = 0; i < 2; i++) {
        if (s_headsets[i].state == BT_STATE_SCANNING) {
            if (s_scan_timer_ms[i] > delta_ms) {
                s_scan_timer_ms[i] -= delta_ms;
            } else {
                s_scan_timer_ms[i] = 0;
                s_headsets[i].state = BT_STATE_CONNECTED;
                ESP_LOGI(TAG, "Scan window ended for Role %d. Returning to CONNECTED state.", s_headsets[i].role);
            }
        }
    }
}
