#include "sa818_dmr_driver.h"
#include <stdio.h>
#include <string.h>
#include "esp_log.h"
#include "driver/uart.h"
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

static const char *TAG = "SA818_DMR";

static void IRAM_ATTR sa818_sql_isr_handler(void *arg) {
    Sa818DmrDriver *driver = static_cast<Sa818DmrDriver*>(arg);
    int level = gpio_get_level(OMM446_PIN_SA818_SQL);
    // SA818 SQL: 0 = Carrier detected (RX active), 1 = Muted / Standby
    driver->handleSquelchIsr(level == 0);
}

Sa818DmrDriver::Sa818DmrDriver()
    : m_squelch_cb(nullptr),
      m_squelch_user_ctx(nullptr),
      m_ptt_start_tick(0),
      m_initialized(false)
{
    // Default: Analog PMR446 Channel 8 (Standard Motorcycle / Safety Channel 446.09375 MHz)
    m_state.mode = SA818_MODE_ANALOG_FM;
    m_state.channel = 8;
    m_state.tx_freq_mhz = OMM446_CHANNEL_FREQS[7];
    m_state.rx_freq_mhz = OMM446_CHANNEL_FREQS[7];
    m_state.ctcss_index = 16;       // Standard CTCSS 16 (114.8 Hz)
    m_state.dmr_color_code = 1;     // Color Code 1
    m_state.dmr_slot = 1;           // Time Slot 1
    m_state.squelch_level = 3;      // Standard Squelch 3 of 8
    m_state.volume_level = 6;       // Volume 6 of 8
    m_state.power = SA818_PWR_LOW_0_2W; // Default to SAR-Safe 0.2W
    m_state.is_transmitting = false;
    m_state.is_receiving = false;
    m_state.last_rssi_dbm = -105;
}

esp_err_t Sa818DmrDriver::init() {
    ESP_LOGI(TAG, "Initializing NiceRF SA818-DMR Transceiver on UART1 (TX=%d, RX=%d)...",
             OMM446_PIN_SA818_TXD, OMM446_PIN_SA818_RXD);

    // 1. Configure Hardware GPIOs
    gpio_config_t io_conf = {};
    
    // PTT Output (Low-active, start HIGH = idle)
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_OUTPUT;
    io_conf.pin_bit_mask = (1ULL << OMM446_PIN_SA818_PTT) | (1ULL << OMM446_PIN_SA818_PWR_HL);
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    io_conf.pull_up_en = GPIO_PULLUP_ENABLE;
    gpio_config(&io_conf);

    gpio_set_level(OMM446_PIN_SA818_PTT, 1);    // Senden inaktiv
    gpio_set_level(OMM446_PIN_SA818_PWR_HL, 0); // 0.2W Low-Power Helmmodus

    // Squelch Input (Low-active interrupt)
    io_conf.intr_type = GPIO_INTR_ANYEDGE;
    io_conf.mode = GPIO_MODE_INPUT;
    io_conf.pin_bit_mask = (1ULL << OMM446_PIN_SA818_SQL);
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    io_conf.pull_up_en = GPIO_PULLUP_ENABLE;
    gpio_config(&io_conf);

    // Install GPIO ISR service
    gpio_install_isr_service(0);
    gpio_isr_handler_add(OMM446_PIN_SA818_SQL, sa818_sql_isr_handler, this);

    // 2. Configure UART (9600 Baud, 8N1)
    uart_config_t uart_config = {
        .baud_rate = OMM446_UART_BAUDRATE,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };
    ESP_ERROR_CHECK(uart_param_config(OMM446_UART_PORT, &uart_config));
    ESP_ERROR_CHECK(uart_set_pin(OMM446_UART_PORT, OMM446_PIN_SA818_TXD, OMM446_PIN_SA818_RXD,
                                 UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE));
    ESP_ERROR_CHECK(uart_driver_install(OMM446_UART_PORT, 1024, 0, 0, NULL, 0));

    // 3. Connect Handshake with SA818 Module
    vTaskDelay(pdMS_TO_TICKS(200)); // SA818 Boot-Zeit
    esp_err_t ret = connectHandshake();
    if (ret != ESP_OK) {
        ESP_LOGW(TAG, "SA818 handshake retry needed, module booting...");
        vTaskDelay(pdMS_TO_TICKS(500));
        ret = connectHandshake();
    }

    if (ret == ESP_OK) {
        setAudioFilters(true, true, true);
        setVolume(m_state.volume_level);
        applyChannelConfig();
        m_initialized = true;
        ESP_LOGI(TAG, "✓ NiceRF SA818-DMR successfully initialized and ready!");
    } else {
        ESP_LOGE(TAG, "Failed to connect to SA818-DMR module via UART AT interface!");
    }

    return ret;
}

esp_err_t Sa818DmrDriver::connectHandshake() {
    char resp[64] = {0};
    esp_err_t ret = sendCommand("AT+DMOCONNECT\r\n", resp, sizeof(resp), 500);
    if (ret == ESP_OK && strstr(resp, "+DMOCONNECT:0") != nullptr) {
        ESP_LOGI(TAG, "Handshake successful: %s", resp);
        return ESP_OK;
    }
    return ESP_FAIL;
}

esp_err_t Sa818DmrDriver::setRadioMode(Sa818RadioMode_t mode) {
    if (m_state.mode == mode) return ESP_OK;
    m_state.mode = mode;
    ESP_LOGI(TAG, "Switching Radio Mode -> %s",
             mode == SA818_MODE_DIGITAL_DMR ? "DIGITAL DMR TIER I" : "ANALOG PMR446");
    return applyChannelConfig();
}

esp_err_t Sa818DmrDriver::setChannel(uint8_t channel) {
    if (channel < 1 || channel > OMM446_NUM_CHANNELS) {
        return ESP_ERR_INVALID_ARG;
    }
    m_state.channel = channel;
    m_state.tx_freq_mhz = OMM446_CHANNEL_FREQS[channel - 1];
    m_state.rx_freq_mhz = OMM446_CHANNEL_FREQS[channel - 1];
    ESP_LOGI(TAG, "Setting Channel %d (%.5f MHz)", m_state.channel, m_state.tx_freq_mhz);
    return applyChannelConfig();
}

esp_err_t Sa818DmrDriver::nextChannel() {
    uint8_t next = (m_state.channel >= OMM446_NUM_CHANNELS) ? 1 : (m_state.channel + 1);
    return setChannel(next);
}

esp_err_t Sa818DmrDriver::prevChannel() {
    uint8_t prev = (m_state.channel <= 1) ? OMM446_NUM_CHANNELS : (m_state.channel - 1);
    return setChannel(prev);
}

esp_err_t Sa818DmrDriver::setCtcss(uint8_t ctcss_index) {
    if (ctcss_index > 38) return ESP_ERR_INVALID_ARG;
    m_state.ctcss_index = ctcss_index;
    return applyChannelConfig();
}

esp_err_t Sa818DmrDriver::setDmrColorCode(uint8_t color_code) {
    if (color_code < 1 || color_code > 16) return ESP_ERR_INVALID_ARG;
    m_state.dmr_color_code = color_code;
    return applyChannelConfig();
}

esp_err_t Sa818DmrDriver::setVolume(uint8_t volume_1_to_8) {
    if (volume_1_to_8 < 1) volume_1_to_8 = 1;
    if (volume_1_to_8 > 8) volume_1_to_8 = 8;
    m_state.volume_level = volume_1_to_8;

    char cmd[32];
    snprintf(cmd, sizeof(cmd), "AT+DMOSETVOLUME=%d\r\n", volume_1_to_8);
    char resp[32] = {0};
    return sendCommand(cmd, resp, sizeof(resp), 300);
}

esp_err_t Sa818DmrDriver::setSquelch(uint8_t sq_level_1_to_8) {
    if (sq_level_1_to_8 < 1) sq_level_1_to_8 = 1;
    if (sq_level_1_to_8 > 8) sq_level_1_to_8 = 8;
    m_state.squelch_level = sq_level_1_to_8;
    return applyChannelConfig();
}

esp_err_t Sa818DmrDriver::setAudioFilters(bool pre_emphasis, bool high_pass, bool low_pass) {
    char cmd[32];
    snprintf(cmd, sizeof(cmd), "AT+SETFILTER=%d,%d,%d\r\n",
             pre_emphasis ? 1 : 0, high_pass ? 1 : 0, low_pass ? 1 : 0);
    char resp[32] = {0};
    return sendCommand(cmd, resp, sizeof(resp), 300);
}

esp_err_t Sa818DmrDriver::setPtt(bool active) {
    if (active) {
        // PTT aktivieren (Low-aktiv)
        gpio_set_level(OMM446_PIN_SA818_PTT, 0);
        m_state.is_transmitting = true;
        m_ptt_start_tick = xTaskGetTickCount();
        ESP_LOGI(TAG, "TX PTT ACTIVE [Channel %d, %.5f MHz, %s]",
                 m_state.channel, m_state.tx_freq_mhz,
                 m_state.mode == SA818_MODE_DIGITAL_DMR ? "DMR Tier I" : "Analog FM");
    } else {
        // PTT deaktivieren (High = idle)
        gpio_set_level(OMM446_PIN_SA818_PTT, 1);
        m_state.is_transmitting = false;
        m_ptt_start_tick = 0;
        ESP_LOGI(TAG, "TX PTT RELEASED (Standby / RX)");
    }
    return ESP_OK;
}

esp_err_t Sa818DmrDriver::setPowerLevel(Sa818PowerLevel_t level) {
    m_state.power = level;
    gpio_set_level(OMM446_PIN_SA818_PWR_HL, (level == SA818_PWR_HIGH_0_5W) ? 1 : 0);
    ESP_LOGI(TAG, "RF Output Power set to: %s",
             level == SA818_PWR_HIGH_0_5W ? "0.5W ERP (Bike Limit)" : "0.2W ERP (Helmet SAR-Safe)");
    return ESP_OK;
}

int8_t Sa818DmrDriver::pollRssi() {
    char resp[32] = {0};
    esp_err_t ret = sendCommand("AT+RSSI?\r\n", resp, sizeof(resp), 200);
    if (ret == ESP_OK && strstr(resp, "+RSSI:") != nullptr) {
        int rssi_raw = 0;
        if (sscanf(resp, "+RSSI:%d", &rssi_raw) == 1) {
            // SA818 returns raw RSSI (e.g. 0..255) -> Map to approx dBm
            m_state.last_rssi_dbm = (int8_t)(-120 + (rssi_raw * 70 / 255));
            return m_state.last_rssi_dbm;
        }
    }
    return m_state.last_rssi_dbm;
}

void Sa818DmrDriver::registerSquelchCallback(sa818_squelch_cb_t cb, void *user_ctx) {
    m_squelch_cb = cb;
    m_squelch_user_ctx = user_ctx;
}

void Sa818DmrDriver::handleSquelchIsr(bool carrier_active) {
    m_state.is_receiving = carrier_active;
    if (m_squelch_cb) {
        m_squelch_cb(carrier_active, m_squelch_user_ctx);
    }
}

esp_err_t Sa818DmrDriver::sendCommand(const char *cmd, char *response_buf, size_t max_len, uint32_t timeout_ms) {
    uart_flush_input(OMM446_UART_PORT);
    uart_write_bytes(OMM446_UART_PORT, cmd, strlen(cmd));

    int len = uart_read_bytes(OMM446_UART_PORT, (uint8_t*)response_buf, max_len - 1, pdMS_TO_TICKS(timeout_ms));
    if (len > 0) {
        response_buf[len] = '\0';
        return ESP_OK;
    }
    return ESP_ERR_TIMEOUT;
}

esp_err_t Sa818DmrDriver::applyChannelConfig() {
    char cmd[128];
    char resp[64] = {0};

    if (m_state.mode == SA818_MODE_ANALOG_FM) {
        // Format: AT+DMOSETGROUP=BW,TX_FREQ,RX_FREQ,CTCSS,SQL,TAIL
        // BW = 0 (12.5 kHz narrow)
        snprintf(cmd, sizeof(cmd), "AT+DMOSETGROUP=0,%.5f,%.5f,%04d,%d,0\r\n",
                 m_state.tx_freq_mhz, m_state.rx_freq_mhz,
                 m_state.ctcss_index, m_state.squelch_level);
        esp_err_t ret = sendCommand(cmd, resp, sizeof(resp), 500);
        if (ret == ESP_OK && strstr(resp, "+DMOSETGROUP:0") != nullptr) {
            ESP_LOGI(TAG, "Analog PMR446 configured: CH%d (%.5f MHz, CTCSS %d, SQ %d)",
                     m_state.channel, m_state.tx_freq_mhz, m_state.ctcss_index, m_state.squelch_level);
            return ESP_OK;
        }
    } else {
        // Format: AT+DMRSETGROUP=TX_FREQ,RX_FREQ,COLOR_CODE,SLOT,CALL_MODE,CALL_TYPE
        snprintf(cmd, sizeof(cmd), "AT+DMRSETGROUP=%.5f,%.5f,%02d,%d,0,1\r\n",
                 m_state.tx_freq_mhz, m_state.rx_freq_mhz,
                 m_state.dmr_color_code, m_state.dmr_slot);
        esp_err_t ret = sendCommand(cmd, resp, sizeof(resp), 500);
        if (ret == ESP_OK && strstr(resp, "+DMRSETGROUP:0") != nullptr) {
            ESP_LOGI(TAG, "Digital DMR Tier I configured: CH%d (%.5f MHz, CC %d, Slot %d)",
                     m_state.channel, m_state.tx_freq_mhz, m_state.dmr_color_code, m_state.dmr_slot);
            return ESP_OK;
        }
    }

    ESP_LOGE(TAG, "Failed to apply channel configuration! Response: %s", resp);
    return ESP_FAIL;
}
