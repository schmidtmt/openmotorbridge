#include "front_sensor_hub.h"
#include "front_node_config.h"
#include <string.h>
#include "esp_log.h"
#include "driver/i2c.h"

static const char* TAG = "FRONT_SENSOR_HUB";

#define I2C_MASTER_NUM          I2C_NUM_0
#define UBLOX_I2C_ADDR          0x42
#define TMP117_I2C_ADDR         0x48
#define OPT3001_I2C_ADDR        0x44

FrontSensorHub& FrontSensorHub::instance() {
    static FrontSensorHub s_instance;
    return s_instance;
}

FrontSensorHub::FrontSensorHub()
    : m_i2c_initialized(false),
      m_latitude_1e7(0),
      m_longitude_1e7(0),
      m_altitude_mm(0),
      m_speed_kph_100(0),
      m_heading_deg_100(0),
      m_satellites_used(0),
      m_gnss_fix_type(0),
      m_temp_c_100(2150),
      m_ambient_lux(1200) {
}

esp_err_t FrontSensorHub::init_i2c() {
    i2c_config_t conf = {};
    conf.mode = I2C_MODE_MASTER;
    conf.sda_io_num = PIN_I2C_SDA;
    conf.scl_io_num = PIN_I2C_SCL;
    conf.sda_pullup_en = GPIO_PULLUP_ENABLE;
    conf.scl_pullup_en = GPIO_PULLUP_ENABLE;
    conf.master.clk_speed = 400000; // 400 kHz Fast-Mode

    esp_err_t err = i2c_param_config(I2C_MASTER_NUM, &conf);
    if (err != ESP_OK) return err;

    return i2c_driver_install(I2C_MASTER_NUM, conf.mode, 0, 0, 0);
}

esp_err_t FrontSensorHub::init() {
    ESP_LOGI(TAG, "Initializing Cockpit Sensor Hub (Qwiic J12: SAM-M10Q, TMP117, OPT3001)...");

    esp_err_t err = init_i2c();
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to initialize I2C bus on GPIO %d/%d: %s",
                 PIN_I2C_SDA, PIN_I2C_SCL, esp_err_to_name(err));
        return err;
    }
    m_i2c_initialized = true;

    // 1. Configure OPT3001 for continuous 100 ms conversions
    uint8_t opt_cfg[3] = {0x01, 0xCE, 0x10}; // Reg 0x01 (Config), Continuous mode, 100 ms
    i2c_master_write_to_device(I2C_MASTER_NUM, OPT3001_I2C_ADDR, opt_cfg, sizeof(opt_cfg), pdMS_TO_TICKS(50));

    // 2. Configure u-blox SAM-M10Q for 10 Hz PVT navigation rate (UBX-CFG-RATE: 100 ms)
    static const uint8_t ubx_cfg_rate_10hz[] = {
        0xB5, 0x62, 0x06, 0x08, 0x06, 0x00, 0x64, 0x00, 0x01, 0x00, 0x01, 0x00, 0x7A, 0x12
    };
    inject_assistnow_mga(ubx_cfg_rate_10hz, sizeof(ubx_cfg_rate_10hz));

    ESP_LOGI(TAG, "Cockpit Sensor Hub initialized successfully.");
    return ESP_OK;
}

esp_err_t FrontSensorHub::inject_assistnow_mga(const uint8_t* mga_data, size_t len) {
    if (!m_i2c_initialized || !mga_data || len == 0) return ESP_ERR_INVALID_STATE;
    return i2c_master_write_to_device(I2C_MASTER_NUM, UBLOX_I2C_ADDR, mga_data, len, pdMS_TO_TICKS(100));
}

void FrontSensorHub::poll_ublox_gnss() {
    if (!m_i2c_initialized) return;

    // Check number of bytes available at u-blox I2C stream (registers 0xFD / 0xFE)
    uint8_t reg_addr = 0xFD;
    uint8_t bytes_avail_buf[2] = {0, 0};
    if (i2c_master_write_read_device(I2C_MASTER_NUM, UBLOX_I2C_ADDR, &reg_addr, 1,
                                     bytes_avail_buf, 2, pdMS_TO_TICKS(20)) != ESP_OK) {
        return;
    }

    uint16_t bytes_available = ((uint16_t)bytes_avail_buf[0] << 8) | bytes_avail_buf[1];
    if (bytes_available < 100 || bytes_available > 1024) return;

    uint8_t rx_buf[256];
    size_t to_read = (bytes_available > sizeof(rx_buf)) ? sizeof(rx_buf) : bytes_available;
    uint8_t stream_reg = 0xFF;

    if (i2c_master_write_read_device(I2C_MASTER_NUM, UBLOX_I2C_ADDR, &stream_reg, 1,
                                     rx_buf, to_read, pdMS_TO_TICKS(50)) != ESP_OK) {
        return;
    }

    // Search for UBX-NAV-PVT frame (Sync 0xB5 0x62, Class 0x01, ID 0x07, Payload Length 92)
    for (size_t i = 0; i <= to_read - 100; i++) {
        if (rx_buf[i] == 0xB5 && rx_buf[i+1] == 0x62 && rx_buf[i+2] == 0x01 && rx_buf[i+3] == 0x07) {
            const uint8_t* pvt = &rx_buf[i + 6];

            m_gnss_fix_type   = pvt[20];
            m_satellites_used = pvt[23];

            int32_t lon_raw, lat_raw, height_raw, speed_raw, head_raw;
            memcpy(&lon_raw,    &pvt[24], 4);
            memcpy(&lat_raw,    &pvt[28], 4);
            memcpy(&height_raw, &pvt[36], 4);
            memcpy(&speed_raw,  &pvt[60], 4); // mm/s
            memcpy(&head_raw,   &pvt[64], 4); // 1e-5 deg

            m_longitude_1e7   = lon_raw;
            m_latitude_1e7    = lat_raw;
            m_altitude_mm     = height_raw;
            m_speed_kph_100   = (speed_raw > 0) ? (uint16_t)((speed_raw * 36) / 100) : 0;
            m_heading_deg_100 = (uint16_t)((head_raw > 0 ? head_raw : 0) / 1000);

            ESP_LOGD(TAG, "GNSS Fix: Type=%u, Sats=%u, Lat=%ld, Lon=%ld, Speed=%u km/h*100",
                     m_gnss_fix_type, m_satellites_used, (long)m_latitude_1e7, (long)m_longitude_1e7, m_speed_kph_100);
            break;
        }
    }
}

void FrontSensorHub::poll_tmp117_temp() {
    if (!m_i2c_initialized) return;

    uint8_t temp_reg = 0x00;
    uint8_t buf[2] = {0, 0};
    if (i2c_master_write_read_device(I2C_MASTER_NUM, TMP117_I2C_ADDR, &temp_reg, 1,
                                     buf, 2, pdMS_TO_TICKS(20)) == ESP_OK) {
        int16_t raw_temp = (int16_t)(((uint16_t)buf[0] << 8) | buf[1]);
        // TMP117: 7.8125 mC per LSB -> * 100 / 1000 -> * 25 / 32
        m_temp_c_100 = (int16_t)(((int32_t)raw_temp * 25) / 32);
    }
}

void FrontSensorHub::poll_opt3001_lux() {
    if (!m_i2c_initialized) return;

    uint8_t result_reg = 0x00;
    uint8_t buf[2] = {0, 0};
    if (i2c_master_write_read_device(I2C_MASTER_NUM, OPT3001_I2C_ADDR, &result_reg, 1,
                                     buf, 2, pdMS_TO_TICKS(20)) == ESP_OK) {
        uint16_t raw = ((uint16_t)buf[0] << 8) | buf[1];
        uint8_t exponent = (raw >> 12) & 0x0F;
        uint16_t mantissa = raw & 0x0FFF;
        // Lux = mantissa * (0.01 * 2^exponent) -> in integer Lux
        m_ambient_lux = (uint32_t)((mantissa * (1UL << exponent)) / 100UL);
    }
}

void FrontSensorHub::update() {
    poll_ublox_gnss();
    poll_tmp117_temp();
    poll_opt3001_lux();
}

void FrontSensorHub::populate_telemetry(UwbFrontTelemetryPkt& pkt) {
    pkt.latitude_1e7       = m_latitude_1e7;
    pkt.longitude_1e7      = m_longitude_1e7;
    pkt.altitude_mm        = m_altitude_mm;
    pkt.speed_kph_100      = m_speed_kph_100;
    pkt.heading_deg_100    = m_heading_deg_100;
    pkt.satellites_used    = m_satellites_used;
    pkt.gnss_fix_type      = m_gnss_fix_type;
    pkt.ambient_temp_c_100 = m_temp_c_100;
    pkt.ambient_lux        = m_ambient_lux;
}
