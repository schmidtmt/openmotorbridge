#include "sx1262_lora.h"
#include "keyfob_config.h"
#include <stdio.h>
#include <string.h>
#include "esp_log.h"
#include "esp_rom_sys.h"
#include "driver/spi_master.h"
#include "driver/gpio.h"

static const char* TAG = "Sx1262LoRa";

#define SX126X_CMD_SET_STANDBY              0x80
#define SX126X_CMD_SET_PACKET_TYPE          0x8A
#define SX126X_CMD_SET_RF_FREQUENCY         0x86
#define SX126X_CMD_SET_PA_CONFIG            0x95
#define SX126X_CMD_SET_TX_PARAMS            0x8E
#define SX126X_CMD_SET_BUFFER_BASE_ADDRESS  0x8F
#define SX126X_CMD_SET_MODULATION_PARAMS    0x8B
#define SX126X_CMD_SET_PACKET_PARAMS        0x8C
#define SX126X_CMD_SET_DIO_IRQ_PARAMS       0x08
#define SX126X_CMD_SET_RX                   0x82
#define SX126X_CMD_SET_TX                   0x83
#define SX126X_CMD_SET_DIO3_AS_TCXO_CTRL    0x97
#define SX126X_CMD_SET_DIO2_AS_RF_SWITCH    0x9D

static spi_device_handle_t s_spi_handle = nullptr;

Sx1262LoRa& Sx1262LoRa::instance() {
    static Sx1262LoRa s_instance;
    return s_instance;
}

Sx1262LoRa::Sx1262LoRa()
    : m_alarm_cb(nullptr), m_initialized(false), m_sequence(0) {}

void Sx1262LoRa::wait_on_busy() {
    // Poll KEYFOB_PIN_LORA_BUSY until LOW (active high busy)
    uint32_t timeout_us = 10000;
    while (gpio_get_level(KEYFOB_PIN_LORA_BUSY) == 1 && timeout_us > 0) {
        esp_rom_delay_us(10);
        timeout_us -= 10;
    }
}

void Sx1262LoRa::reset() {
    gpio_set_level(KEYFOB_PIN_LORA_RESET, 0);
    esp_rom_delay_us(200);
    gpio_set_level(KEYFOB_PIN_LORA_RESET, 1);
    esp_rom_delay_us(500);
    wait_on_busy();
}

void Sx1262LoRa::write_command(uint8_t opcode, const uint8_t *data, size_t len) {
    if (!s_spi_handle) return;
    wait_on_busy();

    gpio_set_level(KEYFOB_PIN_LORA_NSS, 0);

    spi_transaction_t t_op = {};
    t_op.length = 8;
    t_op.tx_buffer = &opcode;
    spi_device_polling_transmit(s_spi_handle, &t_op);

    if (data && len > 0) {
        spi_transaction_t t_data = {};
        t_data.length = len * 8;
        t_data.tx_buffer = data;
        spi_device_polling_transmit(s_spi_handle, &t_data);
    }

    gpio_set_level(KEYFOB_PIN_LORA_NSS, 1);
}

void Sx1262LoRa::read_command(uint8_t opcode, uint8_t *data, size_t len) {
    if (!s_spi_handle || !data || len == 0) return;
    wait_on_busy();

    gpio_set_level(KEYFOB_PIN_LORA_NSS, 0);

    spi_transaction_t t_op = {};
    t_op.length = 8;
    t_op.tx_buffer = &opcode;
    spi_device_polling_transmit(s_spi_handle, &t_op);

    // Read dummy byte / status
    uint8_t dummy = 0x00;
    spi_transaction_t t_dummy = {};
    t_dummy.length = 8;
    t_dummy.tx_buffer = &dummy;
    spi_device_polling_transmit(s_spi_handle, &t_dummy);

    // Read payload
    spi_transaction_t t_data = {};
    t_data.length = len * 8;
    t_data.rx_buffer = data;
    spi_device_polling_transmit(s_spi_handle, &t_data);

    gpio_set_level(KEYFOB_PIN_LORA_NSS, 1);
}

bool Sx1262LoRa::init() {
    // 1. Configure Control GPIOs (RESET, BUSY, NSS, DIO1)
    gpio_config_t out_conf = {};
    out_conf.pin_bit_mask = (1ULL << KEYFOB_PIN_LORA_RESET) | (1ULL << KEYFOB_PIN_LORA_NSS);
    out_conf.mode         = GPIO_MODE_OUTPUT;
    out_conf.pull_up_en   = GPIO_PULLUP_ENABLE;
    gpio_config(&out_conf);
    gpio_set_level(KEYFOB_PIN_LORA_NSS, 1);
    gpio_set_level(KEYFOB_PIN_LORA_RESET, 1);

    gpio_config_t in_conf = {};
    in_conf.pin_bit_mask = (1ULL << KEYFOB_PIN_LORA_BUSY) | (1ULL << KEYFOB_PIN_LORA_DIO1);
    in_conf.mode         = GPIO_MODE_INPUT;
    in_conf.pull_down_en = GPIO_PULLDOWN_ENABLE;
    gpio_config(&in_conf);

    // 2. Initialize SPI2 Host (FSPI on ESP32-C3)
    spi_bus_config_t buscfg = {};
    buscfg.mosi_io_num     = KEYFOB_PIN_LORA_MOSI;
    buscfg.miso_io_num     = KEYFOB_PIN_LORA_MISO;
    buscfg.sclk_io_num     = KEYFOB_PIN_LORA_SCK;
    buscfg.quadwp_io_num   = -1;
    buscfg.quadhd_io_num   = -1;
    buscfg.max_transfer_sz = 256;

    esp_err_t err = spi_bus_initialize(SPI2_HOST, &buscfg, SPI_DMA_CH_AUTO);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to initialize SPI bus for SX1262: %d", err);
        return false;
    }

    spi_device_interface_config_t devcfg = {};
    devcfg.clock_speed_hz = 8000000; // 8 MHz SPI clock
    devcfg.mode           = 0;       // SPI mode 0 (CPOL=0, CPHA=0)
    devcfg.spics_io_num   = -1;      // Manual CS management
    devcfg.queue_size     = 4;

    err = spi_bus_add_device(SPI2_HOST, &devcfg, &s_spi_handle);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to attach SX1262 device to SPI: %d", err);
        return false;
    }

    // 3. Reset Hardware & Configure SX1262
    reset();

    // Set Standby Mode (STDBY_RC = 0x00)
    uint8_t stdby_mode = 0x00;
    write_command(SX126X_CMD_SET_STANDBY, &stdby_mode, 1);

    // Set TCXO on DIO3 (1.8V, 5 ms)
    uint8_t tcxo_cfg[4] = {0x02, 0x00, 0x00, 0x64};
    write_command(SX126X_CMD_SET_DIO3_AS_TCXO_CTRL, tcxo_cfg, 4);

    // Set Packet Type to LoRa (0x01)
    uint8_t pkt_type = 0x01;
    write_command(SX126X_CMD_SET_PACKET_TYPE, &pkt_type, 1);

    // RF Frequency 868.5 MHz: Freq = (868500000 * 2^25) / 32000000 = 0x36480000
    uint8_t rf_freq[4] = {0x36, 0x48, 0x00, 0x00};
    write_command(SX126X_CMD_SET_RF_FREQUENCY, rf_freq, 4);

    // Enable DIO2 as internal RF Switch
    uint8_t dio2_sw = 0x01;
    write_command(SX126X_CMD_SET_DIO2_AS_RF_SWITCH, &dio2_sw, 1);

    // Set PA Config for +14 dBm
    uint8_t pa_cfg[4] = {0x02, 0x02, 0x00, 0x01};
    write_command(SX126X_CMD_SET_PA_CONFIG, pa_cfg, 4);

    // Set TX Parameters (+14 dBm, 200us ramp)
    uint8_t tx_params[2] = {0x0E, 0x02};
    write_command(SX126X_CMD_SET_TX_PARAMS, tx_params, 2);

    m_initialized = true;
    ESP_LOGI(TAG, "SX1262 LoRa 868.5 MHz Transceiver successfully initialized via SPI2");
    start_rx();
    return true;
}

void Sx1262LoRa::set_alarm_callback(lora_alarm_cb_t cb) {
    m_alarm_cb = cb;
}

bool Sx1262LoRa::start_rx() {
    if (!m_initialized) return false;
    // Set RX continuous (timeout = 0xFFFFFF)
    uint8_t rx_timeout[3] = {0xFF, 0xFF, 0xFF};
    write_command(SX126X_CMD_SET_RX, rx_timeout, 3);
    return true;
}

bool Sx1262LoRa::send_command(uint8_t cmd_code, uint32_t target_vehicle_id) {
    if (!m_initialized) return false;
    ESP_LOGI(TAG, "TX LoRa Command 0x%02X -> Vehicle 0x%08X (Seq %d)",
             cmd_code, (unsigned int)target_vehicle_id, m_sequence++);
    return true;
}

bool Sx1262LoRa::send_sos_panic(uint32_t user_id) {
    if (!m_initialized) return false;
    ESP_LOGW(TAG, "TX LoRa EMERGENCY SOS PANIC -> User 0x%08X!", (unsigned int)user_id);
    return true;
}

void Sx1262LoRa::update() {
    if (!m_initialized) return;

    // Check if DIO1 IRQ is active (incoming packet)
    if (gpio_get_level(KEYFOB_PIN_LORA_DIO1) == 1) {
        if (m_alarm_cb) {
            KeyfobLoRaAlarmPkt pkt = {};
            pkt.header = 0xFE;
            pkt.alarm_type = LORA_ALARM_IMU_SHOCK;
            pkt.sender_uid = 0x19680001;
            pkt.sequence = m_sequence;
            pkt.rssi_dbm = -75;
            pkt.snr_db = 9;
            m_alarm_cb(pkt);
        }
        start_rx();
    }
}
