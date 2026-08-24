#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    double latitude;        // Geodetic Latitude in degrees
    double longitude;       // Geodetic Longitude in degrees
    float altitude_m;       // Altitude above WGS84 ellipsoid in meters
    float speed_kmh;        // Filtered vehicle forward velocity in km/h
    float heading_deg;      // Heading / Yaw angle in degrees (0..360)
    float lean_angle_deg;   // Cornering lean angle in degrees (-60..+60)
    float pitch_angle_deg;  // Pitch / Incline angle in degrees (-30..+30)
    float roll_rate_dps;    // Roll angular velocity in deg/s
    bool dead_reckoning_active; // True if navigating in tunnel / satellite outage
    uint32_t gnss_outage_duration_ms; // Duration of current GNSS drop in ms
} AdrEkfState_t;

/**
 * @brief Initialisiert das 15-State Extended Kalman Filter und die Bosch BMI270 IMU
 */
esp_err_t adr_ekf_init(void);

/**
 * @brief Führt den 100 Hz IMU-Prädiktionsschritt aus (Beschleunigung & Drehraten)
 */
void adr_ekf_predict_imu(float ax_mps2, float ay_mps2, float az_mps2,
                         float gx_rads, float gy_rads, float gz_rads,
                         float dt_sec);

/**
 * @brief Führt den 10 Hz GNSS-Messwert-Korrekturschritt aus (u-blox MAX-M10S)
 */
void adr_ekf_update_gnss(double lat, double lon, float alt_m, float pdop, bool has_fix);

/**
 * @brief Führt den Odometer-Korrekturschritt via Fahrzeug-CAN-Bus aus
 */
void adr_ekf_update_can_wheel_speed(float wheel_speed_kmh);

/**
 * @brief Gibt den aktuellen gefilterten Fahrzeugzustand zurück
 */
AdrEkfState_t adr_ekf_get_state(void);

/**
 * @brief FreeRTOS Task für das 100 Hz Sensor-Fusions-Filter (Core 1)
 */
void task_adr_ekf_fusion(void *pvParameters);

#ifdef __cplusplus
}
#endif
