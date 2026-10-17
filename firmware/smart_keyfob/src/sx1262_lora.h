#pragma once

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

// Alarm Types matching OpenMotorBridge Central Box Security Protocol
#define LORA_ALARM_NONE         0x00
#define LORA_ALARM_IMU_SHOCK    0x01 // Motorcycle bumped / moved
#define LORA_ALARM_GEO_BREACH   0x02 // Geo-fence breach / GPS movement
#define LORA_ALARM_IGN_TAMPER   0x03 // Ignition / lock tampered
#define LORA_ALARM_BAT_CUT      0x04 // Main vehicle battery cut
#define LORA_ALARM_SOS_BEACON   0x05 // Remote SOS beacon active

#pragma pack(push, 1)
typedef struct {
    uint8_t  header;        // 0xFE (OMB LoRa Security Frame)
    uint8_t  alarm_type;    // LORA_ALARM_*
    uint32_t sender_uid;    // Vehicle Central Box 32-bit ID
    uint16_t sequence;      // Rolling monotonic counter
    int8_t   rssi_dbm;      // Link signal strength
    int8_t   snr_db;        // Signal to noise ratio
    uint16_t crc16;         // Packet CRC-16
} KeyfobLoRaAlarmPkt;
#pragma pack(pop)

typedef void (*lora_alarm_cb_t)(const KeyfobLoRaAlarmPkt& pkt);

class Sx1262LoRa {
public:
    static Sx1262LoRa& instance();

    bool init();
    void set_alarm_callback(lora_alarm_cb_t cb);
    bool start_rx();
    bool send_command(uint8_t cmd_code, uint32_t target_vehicle_id);
    bool send_sos_panic(uint32_t user_id);
    void update();

private:
    Sx1262LoRa();
    void reset();
    void wait_on_busy();
    void write_command(uint8_t opcode, const uint8_t *data, size_t len);
    void read_command(uint8_t opcode, uint8_t *data, size_t len);

    lora_alarm_cb_t m_alarm_cb;
    bool m_initialized;
    uint16_t m_sequence;
};
