#include "interchip_uart_link.h"
#include <string.h>
#include "esp_log.h"
#include "driver/uart.h"

static const char *TAG = "INTERCHIP_UART";

#define UART_BUF_SIZE (1024)

static struct {
    InterchipCommandCallback cmd_cb;
    bool initialized;
} s_uart_state = {0};

static uint16_t calculate_crc16(const uint8_t *data, size_t len) {
    uint16_t crc = 0xFFFF;
    for (size_t i = 0; i < len; i++) {
        crc ^= (uint16_t)data[i] << 8;
        for (int j = 0; j < 8; j++) {
            if (crc & 0x8000) crc = (crc << 1) ^ 0x1021;
            else crc <<= 1;
        }
    }
    return crc;
}

esp_err_t interchip_uart_init(InterchipCommandCallback cb) {
    ESP_LOGI(TAG, "Initializing Inter-Chip UART Link (GPIO20/21 @ %d baud)...", C3_INTERCHIP_BAUDRATE);

    s_uart_state.cmd_cb = cb;

    uart_config_t uart_config = {
        .baud_rate = C3_INTERCHIP_BAUDRATE,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };

    esp_err_t err = uart_param_config(C3_INTERCHIP_UART_NUM, &uart_config);
    if (err != ESP_OK) return err;

    err = uart_set_pin(C3_INTERCHIP_UART_NUM, PIN_C3_UART_TX, PIN_C3_UART_RX, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    if (err != ESP_OK) return err;

    err = uart_driver_install(C3_INTERCHIP_UART_NUM, UART_BUF_SIZE * 2, 0, 0, NULL, 0);
    if (err != ESP_OK) return err;

    s_uart_state.initialized = true;
    ESP_LOGI(TAG, "✅ Inter-Chip UART Link online.");
    return ESP_OK;
}

static esp_err_t send_frame(InterchipPktType type, const void *payload, uint8_t len) {
    if (!s_uart_state.initialized || len > 32) return ESP_ERR_INVALID_ARG;

    InterchipFrame frame;
    frame.magic = INTERCHIP_MAGIC;
    frame.pkt_type = (uint8_t)type;
    frame.payload_len = len;
    if (payload && len > 0) {
        memcpy(frame.payload, payload, len);
    }
    frame.crc16 = calculate_crc16((const uint8_t*)&frame, sizeof(frame) - 2);

    int sent = uart_write_bytes(C3_INTERCHIP_UART_NUM, &frame, sizeof(InterchipFrame));
    return (sent == sizeof(InterchipFrame)) ? ESP_OK : ESP_FAIL;
}

esp_err_t interchip_uart_send_status(const C3HeadunitState *state) {
    if (!state) return ESP_ERR_INVALID_ARG;
    return send_frame(INTERCHIP_RESP_STATUS, state, sizeof(C3HeadunitState));
}

esp_err_t interchip_uart_send_volume_feedback(uint8_t vol_pct) {
    return send_frame(INTERCHIP_RESP_VOLUME_FEEDBACK, &vol_pct, sizeof(vol_pct));
}

void interchip_uart_process_rx(void) {
    if (!s_uart_state.initialized) return;

    size_t available = 0;
    uart_get_buffered_data_len(C3_INTERCHIP_UART_NUM, &available);
    if (available < sizeof(InterchipFrame)) return;

    InterchipFrame frame;
    int read_bytes = uart_read_bytes(C3_INTERCHIP_UART_NUM, &frame, sizeof(InterchipFrame), 0);
    if (read_bytes == sizeof(InterchipFrame)) {
        if (frame.magic != INTERCHIP_MAGIC) {
            ESP_LOGW(TAG, "Invalid magic byte: 0x%02X", frame.magic);
            return;
        }

        uint16_t expected_crc = calculate_crc16((const uint8_t*)&frame, sizeof(frame) - 2);
        if (frame.crc16 != expected_crc) {
            ESP_LOGW(TAG, "CRC Mismatch: got 0x%04X, expected 0x%04X", frame.crc16, expected_crc);
            return;
        }

        if (s_uart_state.cmd_cb) {
            s_uart_state.cmd_cb((InterchipPktType)frame.pkt_type, frame.payload, frame.payload_len);
        }
    }
}

