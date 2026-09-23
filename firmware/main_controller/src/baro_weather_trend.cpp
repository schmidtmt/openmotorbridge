#include "baro_weather_trend.h"
#include <math.h>
#include <string.h>
#include "esp_timer.h"
#include "esp_log.h"

static const char *TAG = "BARO_WEATHER";

#define HISTORY_BUFFER_SIZE         60  // 60 samples (1 sample per minute = 1 hour window)
#define SAMPLE_INTERVAL_MS          60000 // 1 minute

typedef struct {
    uint32_t timestamp_ms;
    float sea_level_p0;
    float temp_c;
} HistorySample_t;

static HistorySample_t s_history[HISTORY_BUFFER_SIZE];
static size_t s_history_count = 0;
static size_t s_history_head = 0;
static uint32_t s_last_sample_time_ms = 0;

static BaroWeatherStatus_t s_status = {
    .raw_pressure_hpa = 1013.25f,
    .sea_level_pressure_hpa = 1013.25f,
    .altitude_m = 0.0f,
    .temp_celsius = 20.0f,
    .pressure_change_1h_hpa = 0.0f,
    .temp_change_15m_celsius = 0.0f,
    .trend = WEATHER_TREND_STABLE,
    .storm_warning_active = false,
    .should_display_on_dash = false
};

// Standard Barometric Formula: P0 = P * (1 - h / 44330)^(-5.255)
static inline float calculate_p0(float p_hpa, float h_m) {
    if (h_m < -500.0f) h_m = -500.0f;
    if (h_m > 9000.0f) h_m = 9000.0f;
    float base = 1.0f - (h_m / 44330.0f);
    if (base <= 0.001f) base = 0.001f;
    return p_hpa * powf(base, -5.255f);
}

void baro_weather_init(void) {
    s_history_count = 0;
    s_history_head = 0;
    s_last_sample_time_ms = 0;
    memset(s_history, 0, sizeof(s_history));
    ESP_LOGI(TAG, "Autarkic Barometric Weather Trend Engine initialized.");
}

void baro_weather_update(float pressure_hpa, float altitude_m, float temp_celsius, float speed_kmh) {
    if (pressure_hpa < 300.0f || pressure_hpa > 1100.0f) return; // Discard invalid sensor readings

    uint32_t now_ms = (uint32_t)(esp_timer_get_time() / 1000ULL);
    float p0 = calculate_p0(pressure_hpa, altitude_m);

    s_status.raw_pressure_hpa = pressure_hpa;
    s_status.altitude_m = altitude_m;
    s_status.temp_celsius = temp_celsius;
    s_status.sea_level_pressure_hpa = p0;

    // Sample into history buffer every 60 seconds
    if (s_last_sample_time_ms == 0 || (now_ms - s_last_sample_time_ms >= SAMPLE_INTERVAL_MS)) {
        s_last_sample_time_ms = now_ms;

        s_history[s_history_head].timestamp_ms = now_ms;
        s_history[s_history_head].sea_level_p0 = p0;
        s_history[s_history_head].temp_c = temp_celsius;

        s_history_head = (s_history_head + 1) % HISTORY_BUFFER_SIZE;
        if (s_history_count < HISTORY_BUFFER_SIZE) {
            s_history_count++;
        }
    }

    // Evaluate 1-hour pressure change dP/dt
    if (s_history_count >= 10) { // Require at least 10 minutes of history
        // Oldest sample in the buffer
        size_t oldest_idx = (s_history_head + HISTORY_BUFFER_SIZE - s_history_count) % HISTORY_BUFFER_SIZE;
        float oldest_p0 = s_history[oldest_idx].sea_level_p0;
        uint32_t dt_ms = now_ms - s_history[oldest_idx].timestamp_ms;

        if (dt_ms > 60000) {
            float dt_hours = (float)dt_ms / 3600000.0f;
            float dp = p0 - oldest_p0;
            s_status.pressure_change_1h_hpa = dp / dt_hours;
        }

        // Evaluate 15-minute temperature change
        size_t samples_15m = (s_history_count >= 15) ? 15 : s_history_count;
        size_t idx_15m = (s_history_head + HISTORY_BUFFER_SIZE - samples_15m) % HISTORY_BUFFER_SIZE;
        s_status.temp_change_15m_celsius = temp_celsius - s_history[idx_15m].temp_c;
    } else {
        s_status.pressure_change_1h_hpa = 0.0f;
        s_status.temp_change_15m_celsius = 0.0f;
    }

    // Trend classification
    // Severe Drop: dP/dt <= -2.0 hPa/h OR rapid temp drop <= -3.0°C in 15m
    if (s_status.pressure_change_1h_hpa <= -2.0f || s_status.temp_change_15m_celsius <= -3.0f) {
        s_status.trend = WEATHER_TREND_RAPID_FALL_STORM;
        s_status.storm_warning_active = true;
    } else if (s_status.pressure_change_1h_hpa <= -1.0f) {
        s_status.trend = WEATHER_TREND_FALLING_RAIN;
        s_status.storm_warning_active = false;
    } else if (s_status.pressure_change_1h_hpa >= 1.0f) {
        s_status.trend = WEATHER_TREND_RISING_FAIR;
        s_status.storm_warning_active = false;
    } else {
        s_status.trend = WEATHER_TREND_STABLE;
        s_status.storm_warning_active = false;
    }

    // Standstill gating: Only display warnings on the dash/display when stopped (v < 1.0 km/h)
    s_status.should_display_on_dash = (speed_kmh < 1.0f && s_status.trend != WEATHER_TREND_STABLE);
}

BaroWeatherStatus_t baro_weather_get_status(void) {
    return s_status;
}
