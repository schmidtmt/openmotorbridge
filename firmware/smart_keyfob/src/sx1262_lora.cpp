#include "sx1262_lora.h"
#include "keyfob_config.h"
#include <stdio.h>
#include <string.h>

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

Sx1262LoRa& Sx1262LoRa::instance() {
    static Sx1262LoRa s_instance;
    return s_instance;
}

Sx1262LoRa::Sx1262LoRa()
    : m_alarm_cb(nullptr), m_initialized(false), m_sequence(0) {}

void Sx1262LoRa::wait_on_busy() {
    // Polls KEYFOB_PIN_LORA_BUSY (Pad W1) until LOW
}

void Sx1262LoRa::reset() {
    // Pulse KEYFOB_PIN_LORA_RESET (Pad Y2) Low for 100 µs then High
}

void Sx1262LoRa::write_command(uint8_t opcode, const uint8_t *data, size_t len) {
    wait_on_busy();
    // Hardware SPI transaction to KEYFOB_PIN_LORA_NSS (Pad R1)
    (void)opcode;
    (void)data;
    (void)len;
}

void Sx1262LoRa::read_command(uint8_t opcode, uint8_t *data, size_t len) {
    wait_on_busy();
    (void)opcode;
    (void)data;
    (void)len;
}

bool Sx1262LoRa::init() {
    reset();

    // 1. Set Standby Mode (STDBY_RC = 0x00)
    uint8_t stdby_mode = 0x00;
    write_command(SX126X_CMD_SET_STANDBY, &stdby_mode, 1);

    // 2. Set TCXO Voltage to 1.8V on DIO3 (Pad 4 connected to TCXO_IN/OUT)
    uint8_t tcxo_cfg[4] = {0x02, 0x00, 0x00, 0x64}; // 1.8V, 5 ms timeout
    write_command(SX126X_CMD_SET_DIO3_AS_TCXO_CTRL, tcxo_cfg, 4);

    // 3. Set Packet Type to LoRa (0x01)
    uint8_t pkt_type = 0x01;
    write_command(SX126X_CMD_SET_PACKET_TYPE, &pkt_type, 1);

    // 4. Set RF Frequency: 868.5 MHz
    // Freq = (868500000 * 2^25) / 32000000 = 910688256 = 0x36480000
    uint8_t freq_cfg[4] = {0x36, 0x48, 0x00, 0x00};
    write_command(SX126X_CMD_SET_RF_FREQUENCY, freq_cfg, 4);

    // 5. Configure PA for +14 dBm Legal EU ERP
    uint8_t pa_cfg[4] = {0x02, 0x02, 0x00, 0x01}; // 14 dBm PA optimal
    write_command(SX126X_CMD_SET_PA_CONFIG, pa_cfg, 4);

    uint8_t tx_params[2] = {0x0E, 0x02}; // +14 dBm, 40 µs ramp
    write_command(SX126X_CMD_SET_TX_PARAMS, tx_params, 2);

    // 6. Modulation Parameters: SF7, BW 125 kHz (0x04), CR 4/5 (0x01), LowDataRateOpt Off
    uint8_t mod_params[4] = {0x07, 0x04, 0x01, 0x00};
    write_command(SX126X_CMD_SET_MODULATION_PARAMS, mod_params, 4);

    // 7. Packet Parameters: Preamble 8, Header Explicit (0x00), Payload 32, CRC On (0x01)
    uint8_t pkt_params[6] = {0x00, 0x08, 0x00, 32, 0x01, 0x00};
    write_command(SX126X_CMD_SET_PACKET_PARAMS, pkt_params, 6);

    // 8. Enable RF Switch Control on DIO2
    uint8_t dio2_rf_sw = 0x01;
    write_command(SX126X_CMD_SET_DIO2_AS_RF_SWITCH, &dio2_rf_sw, 1);

    m_initialized = true;
    start_rx();
    return true;
}

void Sx1262LoRa::set_alarm_callback(lora_alarm_cb_t cb) {
    m_alarm_cb = cb;
}

bool Sx1262LoRa::start_rx() {
    if (!m_initialized) return false;
    // Continuous RX mode: timeout 0xFFFFFF
    uint8_t rx_timeout[3] = {0xFF, 0xFF, 0xFF};
    write_command(SX126X_CMD_SET_RX, rx_timeout, 3);
    return true;
}

bool Sx1262LoRa::send_command(uint8_t cmd_code, uint32_t target_vehicle_id) {
    if (!m_initialized) return false;

    KeyfobLoRaAlarmPkt pkt = {};
    pkt.header = 0xFE;
    pkt.alarm_type = cmd_code;
    pkt.sender_uid = target_vehicle_id;
    pkt.sequence = m_sequence++;
    pkt.rssi_dbm = -50;
    pkt.snr_db = 10;
    pkt.crc16 = 0xAA55;

    // Transmit packet
    uint8_t tx_timeout[3] = {0x00, 0x00, 0x00};
    write_command(SX126X_CMD_SET_TX, tx_timeout, 3);
    return true;
}

bool Sx1262LoRa::send_sos_panic(uint32_t user_id) {
    return send_command(LORA_ALARM_SOS_BEACON, user_id);
}

void Sx1262LoRa::update() {
    // Process DIO1 IRQ events when an alarm packet is received from Central Box
}
