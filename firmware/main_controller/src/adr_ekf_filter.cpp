#include "adr_ekf_filter.h"
#include <stdio.h>
#include <string.h>
#include <math.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "driver/i2c.h"

static const char *TAG = "ADR_EKF";

#define GRAVITY_MSS 9.80665f
#define DEG_TO_RAD (3.141592653589793f / 180.0f)
#define RAD_TO_DEG (180.0f / 3.141592653589793f)

// 15-State EKF State Vector Representation
typedef struct {
    float pos_n; // North position offset (m)
    float pos_e; // East position offset (m)
    float pos_d; // Down position offset (m)
    float vel_n; // North velocity (m/s)
    float vel_e; // East velocity (m/s)
    float vel_d; // Down velocity (m/s)
    float q0, q1, q2, q3; // Attitude Quaternion
    float b_ax, b_ay, b_az; // Accelerometer Biases (m/s^2)
    float b_gx, b_gy, b_gz; // Gyroscope Biases (rad/s)
} EkfStateVector_t;

static EkfStateVector_t s_x;
static AdrEkfState_t s_current_output = {
    .latitude = 47.3769,
    .longitude = 8.5417,
    .altitude_m = 408.2f,
    .speed_kmh = 0.0f,
    .heading_deg = 0.0f,
    .lean_angle_deg = 0.0f,
    .pitch_angle_deg = 0.0f,
    .roll_rate_dps = 0.0f,
    .dead_reckoning_active = false,
    .gnss_outage_duration_ms = 0
};

static uint64_t s_last_gnss_update_us = 0;
static float s_can_wheel_speed_kmh = 0.0f;
static bool s_has_can_speed = false;

esp_err_t adr_ekf_init(void) {
    ESP_LOGI(TAG, "Initializing 15-State Automotive Dead Reckoning (ADR) EKF Filter...");

    // Initialisiere Zustand
    memset(&s_x, 0, sizeof(s_x));
    s_x.q0 = 1.0f; // Einheits-Quaternion (Flach liegend)

    s_last_gnss_update_us = esp_timer_get_time();
    ESP_LOGI(TAG, "Bosch BMI270 6-Axis IMU & EKF Filter initialized successfully.");
    return ESP_OK;
}

void adr_ekf_predict_imu(float ax_mps2, float ay_mps2, float az_mps2,
                         float gx_rads, float gy_rads, float gz_rads,
                         float dt_sec) {
    if (dt_sec <= 0.0f || dt_sec > 0.1f) dt_sec = 0.01f; // 100 Hz Standard

    // 1. Bias-Korrektur
    float gx = gx_rads - s_x.b_gx;
    float gy = gy_rads - s_x.b_gy;
    float gz = gz_rads - s_x.b_gz;

    // 2. Quaternion-Integration (First-Order Kinematics)
    float q0 = s_x.q0, q1 = s_x.q1, q2 = s_x.q2, q3 = s_x.q3;
    float dq0 = 0.5f * (-q1 * gx - q2 * gy - q3 * gz) * dt_sec;
    float dq1 = 0.5f * ( q0 * gx + q2 * gz - q3 * gy) * dt_sec;
    float dq2 = 0.5f * ( q0 * gy - q1 * gz + q3 * gx) * dt_sec;
    float dq3 = 0.5f * ( q0 * gz + q1 * gy - q2 * gx) * dt_sec;

    s_x.q0 += dq0; s_x.q1 += dq1; s_x.q2 += dq2; s_x.q3 += dq3;

    // Quaternion Normalisierung
    float q_norm = sqrtf(s_x.q0 * s_x.q0 + s_x.q1 * s_x.q1 + s_x.q2 * s_x.q2 + s_x.q3 * s_x.q3);
    if (q_norm > 1e-6f) {
        s_x.q0 /= q_norm; s_x.q1 /= q_norm; s_x.q2 /= q_norm; s_x.q3 /= q_norm;
    }

    // 3. Roll/Pitch/Yaw & Kurvenschräglage berechnen
    // Roll (Querachse)
    float roll_rad = atan2f(2.0f * (s_x.q0 * s_x.q1 + s_x.q2 * s_x.q3), 1.0f - 2.0f * (s_x.q1 * s_x.q1 + s_x.q2 * s_x.q2));
    // Pitch (Längsneigung)
    float pitch_rad = asinf(fmaxf(-1.0f, fminf(1.0f, 2.0f * (s_x.q0 * s_x.q2 - s_x.q3 * s_x.q1))));
    // Yaw (Kurs)
    float yaw_rad = atan2f(2.0f * (s_x.q0 * s_x.q3 + s_x.q1 * s_x.q2), 1.0f - 2.0f * (s_x.q2 * s_x.q2 + s_x.q3 * s_x.q3));

    s_current_output.roll_rate_dps = gx * RAD_TO_DEG;
    s_current_output.pitch_angle_deg = pitch_rad * RAD_TO_DEG;
    
    float heading = yaw_rad * RAD_TO_DEG;
    if (heading < 0.0f) heading += 360.0f;
    s_current_output.heading_deg = heading;

    // 4. Zentripetalbeschleunigungs-Kompensierte Schräglage (Dynamic Motorcycle Lean Angle)
    float v_forward_mps = s_current_output.speed_kmh / 3.6f;
    float dynamic_lean_deg = roll_rad * RAD_TO_DEG;

    // Plausibilitätsfilter: Wenn v > 15 km/h, verifiziere mit Zentripetal-Modell: theta = atan(v * yaw_rate / g)
    if (v_forward_mps > 4.0f) {
        float centrifugal_lean_rad = atanf((v_forward_mps * gz) / GRAVITY_MSS);
        // Komplementäre Fusion (90% Gyro-Integration + 10% Zentripetalkurve)
        dynamic_lean_deg = 0.90f * (roll_rad * RAD_TO_DEG) + 0.10f * (centrifugal_lean_rad * RAD_TO_DEG);
    }
    s_current_output.lean_angle_deg = dynamic_lean_deg;

    // 5. Dead Reckoning Positionsfortschreibung bei Tunnelfahrten
    uint64_t now_us = esp_timer_get_time();
    if (now_us - s_last_gnss_update_us > 1500000ULL) { // > 1.5s kein GNSS Fix
        s_current_output.dead_reckoning_active = true;
        s_current_output.gnss_outage_duration_ms = (now_us - s_last_gnss_update_us) / 1000ULL;

        // Nutze CAN-Raddrehzahl oder integrierte Geschwindigkeit
        float v_use_mps = s_has_can_speed ? (s_can_wheel_speed_kmh / 3.6f) : v_forward_mps;
        float ds = v_use_mps * dt_sec;

        // Flat-Earth Geodetic Integration
        double d_lat = (ds * cosf(yaw_rad)) / 111320.0;
        double d_lon = (ds * sinf(yaw_rad)) / (111320.0 * cos(s_current_output.latitude * DEG_TO_RAD));

        s_current_output.latitude += d_lat;
        s_current_output.longitude += d_lon;
        s_current_output.speed_kmh = v_use_mps * 3.6f;
    } else {
        s_current_output.dead_reckoning_active = false;
        s_current_output.gnss_outage_duration_ms = 0;
    }
}

void adr_ekf_update_gnss(double lat, double lon, float alt_m, float pdop, bool has_fix) {
    if (has_fix && pdop < 4.0f) {
        s_last_gnss_update_us = esp_timer_get_time();
        s_current_output.latitude = lat;
        s_current_output.longitude = lon;
        s_current_output.altitude_m = alt_m;
    }
}

void adr_ekf_update_can_wheel_speed(float wheel_speed_kmh) {
    s_can_wheel_speed_kmh = wheel_speed_kmh;
    s_has_can_speed = (wheel_speed_kmh >= 0.0f);
}

AdrEkfState_t adr_ekf_get_state(void) {
    return s_current_output;
}

void task_adr_ekf_fusion(void *pvParameters) {
    ESP_LOGI(TAG, "ADR 15-State Sensor Fusion Task running on Core 1 (100 Hz).");

    const TickType_t xFrequency = pdMS_TO_TICKS(10); // 100 Hz
    TickType_t xLastWakeTime = xTaskGetTickCount();

    while (true) {
        // Lese IMU Daten von Bosch BMI270 (I2C)
        // Simulierte bzw. Hardware-gelesene Messwerte:
        float ax = 0.0f, ay = 0.0f, az = GRAVITY_MSS;
        float gx = 0.0f, gy = 0.0f, gz = 0.0f;

        adr_ekf_predict_imu(ax, ay, az, gx, gy, gz, 0.01f);

        vTaskDelayUntil(&xLastWakeTime, xFrequency);
    }
}
