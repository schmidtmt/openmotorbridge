#pragma once

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge - Autarkic Barometric Weather Trend & Thunderstorm Warning
// Sea-level Pressure Normalization via GNSS Altitude + Rate-of-Change Detection
// =============================================================================

typedef enum {
    WEATHER_TREND_STABLE = 0,               // Barometric pressure steady (-1.0 to +1.0 hPa/h)
    WEATHER_TREND_RISING_FAIR = 1,          // Rising pressure (+1.0 to +2.0 hPa/h) -> Fair weather
    WEATHER_TREND_FALLING_RAIN = 2,         // Falling pressure (-1.0 to -2.0 hPa/h) -> Rain approaching
    WEATHER_TREND_RAPID_FALL_STORM = 3      // Severe drop (<-2.0 hPa/h or temp plunge) -> Thunderstorm/Front
} BaroWeatherTrend_t;

typedef struct {
    float raw_pressure_hpa;
    float sea_level_pressure_hpa;
    float altitude_m;
    float temp_celsius;
    float pressure_change_1h_hpa;           // dP/dt in hPa/hour
    float temp_change_15m_celsius;          // dT/dt in °C / 15 min
    BaroWeatherTrend_t trend;
    bool storm_warning_active;
    bool should_display_on_dash;            // Gated: true only at standstill (v == 0 km/h)
} BaroWeatherStatus_t;

/**
 * @brief Initialisiert die autarke Wettertrend-Engine
 */
void baro_weather_init(void);

/**
 * @brief Speist periodische Messwerte (BMP390 + GNSS) ein (z. B. alle 10 Sekunden)
 * @param pressure_hpa Rohdruck vom BMP390 in hPa
 * @param altitude_m WGS84 Höhe vom GNSS in Metern
 * @param temp_celsius Gemessene Außentemperatur in °C
 * @param speed_kmh Aktuelle Fahrzeuggeschwindigkeit in km/h
 */
void baro_weather_update(float pressure_hpa, float altitude_m, float temp_celsius, float speed_kmh);

/**
 * @brief Liefert den aktuellen Wettertrend-Status
 */
BaroWeatherStatus_t baro_weather_get_status(void);

#ifdef __cplusplus
}
#endif
