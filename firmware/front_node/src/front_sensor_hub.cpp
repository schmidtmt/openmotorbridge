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
#define BMP390_I2C_ADDR         0x76

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
      m_ambient_lux(1200),
      m_baro_pressure_pa(101325),
      m_bmp_calib{} {
    m_bmp_calib.valid = false;
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

    // 3. Configure Bosch BMP390 Barometer (0x76 on Sensor Puck PCBA 05D)
    // Read 21 bytes calibration data from NVM 0x31..0x45
    uint8_t calib_addr = 0x31;
    uint8_t c_buf[21] = {0};
    if (i2c_master_write_read_device(I2C_MASTER_NUM, BMP390_I2C_ADDR, &calib_addr, 1,
                                     c_buf, sizeof(c_buf), pdMS_TO_TICKS(50)) == ESP_OK) {
        uint16_t raw_t1 = (uint16_t)c_buf[0] | ((uint16_t)c_buf[1] << 8);
        uint16_t raw_t2 = (uint16_t)c_buf[2] | ((uint16_t)c_buf[3] << 8);
        int8_t   raw_t3 = (int8_t)c_buf[4];
        int16_t  raw_p1 = (int16_t)((uint16_t)c_buf[5] | ((uint16_t)c_buf[6] << 8));
        int16_t  raw_p2 = (int16_t)((uint16_t)c_buf[7] | ((uint16_t)c_buf[8] << 8));
        int8_t   raw_p3 = (int8_t)c_buf[9];
        int8_t   raw_p4 = (int8_t)c_buf[10];
        uint16_t raw_p5 = (uint16_t)c_buf[11] | ((uint16_t)c_buf[12] << 8);
        uint16_t raw_p6 = (uint16_t)c_buf[13] | ((uint16_t)c_buf[14] << 8);
        int8_t   raw_p7 = (int8_t)c_buf[15];
        int8_t   raw_p8 = (int8_t)c_buf[16];
        int16_t  raw_p9 = (int16_t)((uint16_t)c_buf[17] | ((uint16_t)c_buf[18] << 8));
        int8_t   raw_p10 = (int8_t)c_buf[19];
        int8_t   raw_p11 = (int8_t)c_buf[20];

        // Bosch floating-point quantization factors
        m_bmp_calib.par_t1 = (double)raw_t1 * 256.0;                    // / 2^-8
        m_bmp_calib.par_t2 = (double)raw_t2 / 1073741824.0;             // / 2^30
        m_bmp_calib.par_t3 = (double)raw_t3 / 281474976710656.0;        // / 2^48
        m_bmp_calib.par_p1 = ((double)raw_p1 - 16384.0) / 1048576.0;    // (raw - 2^14) / 2^20
        m_bmp_calib.par_p2 = ((double)raw_p2 - 16384.0) / 536870912.0;  // (raw - 2^14) / 2^29
        m_bmp_calib.par_p3 = (double)raw_p3 / 4294967296.0;             // / 2^32
        m_bmp_calib.par_p4 = (double)raw_p4 / 137438953472.0;           // / 2^37
        m_bmp_calib.par_p5 = (double)raw_p5 * 8.0;                      // / 2^-3
        m_bmp_calib.par_p6 = (double)raw_p6 / 64.0;                     // / 2^6
        m_bmp_calib.par_p7 = (double)raw_p7 / 256.0;                    // / 2^8
        m_bmp_calib.par_p8 = (double)raw_p8 / 32768.0;                  // / 2^15
        m_bmp_calib.par_p9 = (double)raw_p9 / 281474976710656.0;        // / 2^48
        m_bmp_calib.par_p10 = (double)raw_p10 / 281474976710656.0;      // / 2^48
        m_bmp_calib.par_p11 = (double)raw_p11 / 36893488147419103232.0; // / 2^65
        m_bmp_calib.valid = true;
        ESP_LOGI(TAG, "BMP390 factory NVM calibration loaded successfully.");
    } else {
        ESP_LOGW(TAG, "Failed to read BMP390 calibration registers (NVM 0x31..0x45)!");
    }

    // PWR_CTRL: Press EN (bit 0), Temp EN (bit 1), Mode normal (bits 4-5 = 0b11) -> 0x33
    uint8_t bmp_pwr[2] = {0x1B, 0x33};
    i2c_master_write_to_device(I2C_MASTER_NUM, BMP390_I2C_ADDR, bmp_pwr, sizeof(bmp_pwr), pdMS_TO_TICKS(50));
    // OSR: Pressure oversampling 4x (0x02), Temp oversampling 1x (0x00) -> 0x02
    uint8_t bmp_osr[2] = {0x1C, 0x02};
    i2c_master_write_to_device(I2C_MASTER_NUM, BMP390_I2C_ADDR, bmp_osr, sizeof(bmp_osr), pdMS_TO_TICKS(50));

    ESP_LOGI(TAG, "Cockpit Sensor Hub initialized successfully (SAM-M10Q, TMP117, OPT3001, BMP390).");
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

void FrontSensorHub::poll_bmp390_baro() {
    if (!m_i2c_initialized) return;

    // Burst read 6 bytes: DATA_0..5 (Press XLSB/LSB/MSB at 0x04..0x06, Temp XLSB/LSB/MSB at 0x07..0x09)
    uint8_t reg_addr = 0x04;
    uint8_t buf[6] = {0};
    if (i2c_master_write_read_device(I2C_MASTER_NUM, BMP390_I2C_ADDR, &reg_addr, 1,
                                     buf, sizeof(buf), pdMS_TO_TICKS(20)) != ESP_OK) {
        return;
    }

    uint32_t raw_press = ((uint32_t)buf[2] << 16) | ((uint32_t)buf[1] << 8) | buf[0];
    uint32_t raw_temp  = ((uint32_t)buf[5] << 16) | ((uint32_t)buf[4] << 8) | buf[3];

    if (raw_press == 0 || raw_temp == 0) return;

    if (!m_bmp_calib.valid) {
        // Fallback if calibration read failed
        m_baro_pressure_pa = raw_press / 256;
        return;
    }

    // 1. Bosch temperature compensation -> t_lin in deg C
    double p_t1 = (double)raw_temp - m_bmp_calib.par_t1;
    double p_t2 = p_t1 * m_bmp_calib.par_t2;
    double t_lin = p_t2 + (p_t1 * p_t1) * m_bmp_calib.par_t3;

    // 2. Bosch pressure compensation -> comp_press in Pa
    double t_sq = t_lin * t_lin;
    double t_cube = t_sq * t_lin;

    double p_out1 = m_bmp_calib.par_p5 +
                    m_bmp_calib.par_p6 * t_lin +
                    m_bmp_calib.par_p7 * t_sq +
                    m_bmp_calib.par_p8 * t_cube;

    double p_sens = m_bmp_calib.par_p1 +
                    m_bmp_calib.par_p2 * t_lin +
                    m_bmp_calib.par_p3 * t_sq +
                    m_bmp_calib.par_p4 * t_cube;
    double p_out2 = (double)raw_press * p_sens;

    double pr_sq = (double)raw_press * (double)raw_press;
    double pr_cube = pr_sq * (double)raw_press;
    double p_out3 = pr_sq * (m_bmp_calib.par_p9 + m_bmp_calib.par_p10 * t_lin) +
                    pr_cube * m_bmp_calib.par_p11;

    double comp_press = p_out1 + p_out2 + p_out3;

    // Plausibility check for atmospheric pressure (300 hPa to 1250 hPa)
    if (comp_press >= 30000.0 && comp_press <= 125000.0) {
        m_baro_pressure_pa = (uint32_t)(comp_press + 0.5);
    }
}

void FrontSensorHub::update() {
    poll_ublox_gnss();
    poll_tmp117_temp();
    poll_opt3001_lux();
    poll_bmp390_baro();
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
    pkt.baro_pressure_pa   = m_baro_pressure_pa;
}
