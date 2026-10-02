#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"
#include "uwb_backbone_types.h"

class FrontSensorHub {
public:
    static FrontSensorHub& instance();

    esp_err_t init();

    // Periodic sensor read (called at 10 Hz)
    void update();

    // Populate consolidated 10 Hz UWB telemetry packet
    void populate_telemetry(UwbFrontTelemetryPkt& pkt);

    // Inject u-blox AssistNow A-GPS UBX-MGA packet via Qwiic I2C (0x42)
    esp_err_t inject_assistnow_mga(const uint8_t* mga_data, size_t len);

    bool has_gnss_fix() const { return m_gnss_fix_type >= 3; }
    uint8_t get_gnss_fix_type() const { return m_gnss_fix_type; }
    uint8_t get_satellites_used() const { return m_satellites_used; }
    int16_t get_temperature_c_100() const { return m_temp_c_100; }
    uint32_t get_ambient_lux() const { return m_ambient_lux; }

private:
    FrontSensorHub();
    ~FrontSensorHub() = default;

    esp_err_t init_i2c();
    void poll_ublox_gnss();
    void poll_tmp117_temp();
    void poll_opt3001_lux();

    bool m_i2c_initialized;

    // Latest GNSS state
    int32_t  m_latitude_1e7;
    int32_t  m_longitude_1e7;
    int32_t  m_altitude_mm;
    uint16_t m_speed_kph_100;
    uint16_t m_heading_deg_100;
    uint8_t  m_satellites_used;
    uint8_t  m_gnss_fix_type;

    // Environmental sensors
    int16_t  m_temp_c_100;
    uint32_t m_ambient_lux;
};
