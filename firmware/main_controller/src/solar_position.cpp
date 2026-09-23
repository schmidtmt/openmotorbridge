#include "solar_position.h"
#include <math.h>
#include <time.h>
#include "esp_timer.h"
#include "esp_log.h"

static const char *TAG = "SOLAR_DIM";

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#define DEG_TO_RAD(deg) ((deg) * (M_PI / 180.0))
#define RAD_TO_DEG(rad) ((rad) * (180.0 / M_PI))

static bool s_tunnel_active = false;
static uint32_t s_gnss_loss_start_ms = 0;

float solar_calculate_elevation_deg(float lat_deg, float lon_deg, uint32_t utc_epoch_s) {
    if (utc_epoch_s == 0) return 45.0f; // Default day if no time fix yet

    time_t raw_time = (time_t)utc_epoch_s;
    struct tm timeinfo;
    gmtime_r(&raw_time, &timeinfo);

    int day_of_year = timeinfo.tm_yday + 1; // 1 - 366
    float hour_utc = timeinfo.tm_hour + timeinfo.tm_min / 60.0f + timeinfo.tm_sec / 3600.0f;

    // Fractional year in radians
    float gamma = 2.0f * M_PI / 365.0f * (day_of_year - 1 + (hour_utc - 12.0f) / 24.0f);

    // Equation of time (in minutes)
    float eqtime = 229.18f * (0.000075f + 0.001868f * cosf(gamma) - 0.032077f * sinf(gamma)
                              - 0.014615f * cosf(2.0f * gamma) - 0.040849f * sinf(2.0f * gamma));

    // Solar declination angle (in radians)
    float decl = 0.006918f - 0.399912f * cosf(gamma) + 0.070257f * sinf(gamma)
                 - 0.006758f * cosf(2.0f * gamma) + 0.000907f * sinf(2.0f * gamma)
                 - 0.002697f * cosf(3.0f * gamma) + 0.00148f * sinf(3.0f * gamma);

    // True solar time in minutes
    float time_offset = eqtime + 4.0f * lon_deg;
    float tst = hour_utc * 60.0f + time_offset;
    while (tst >= 1440.0f) tst -= 1440.0f;
    while (tst < 0.0f) tst += 1440.0f;

    // Solar hour angle in degrees
    float ha_deg = (tst / 4.0f) - 180.0f;
    float ha_rad = DEG_TO_RAD(ha_deg);

    float lat_rad = DEG_TO_RAD(lat_deg);

    // Solar elevation angle sin(alpha) = sin(lat)*sin(decl) + cos(lat)*cos(decl)*cos(ha)
    float sin_elev = sinf(lat_rad) * sinf(decl) + cosf(lat_rad) * cosf(decl) * cosf(ha_rad);
    if (sin_elev > 1.0f) sin_elev = 1.0f;
    if (sin_elev < -1.0f) sin_elev = -1.0f;

    float elev_deg = RAD_TO_DEG(asinf(sin_elev));
    return elev_deg;
}

uint8_t solar_dimmer_evaluate(float lat_deg, float lon_deg, uint32_t utc_epoch_s,
                              bool gnss_fix_valid, float speed_kmh) {
    uint32_t now_ms = (uint32_t)(esp_timer_get_time() / 1000ULL);

    // 1. Tunnel Detection: Loss of GNSS Fix (>1500 ms) while moving at >30 km/h
    if (!gnss_fix_valid && speed_kmh > 30.0f) {
        if (s_gnss_loss_start_ms == 0) {
            s_gnss_loss_start_ms = now_ms;
        } else if (now_ms - s_gnss_loss_start_ms > 1500) {
            if (!s_tunnel_active) {
                s_tunnel_active = true;
                ESP_LOGW(TAG, "⚡ Tunnel Detected! (GNSS fix lost >1.5s @ %.1f km/h) -> Forcing Night Dimming (18%%)", speed_kmh);
            }
            return DIMMER_MIN_NIGHT_PCT;
        }
    } else {
        s_gnss_loss_start_ms = 0;
        if (s_tunnel_active) {
            s_tunnel_active = false;
            ESP_LOGI(TAG, "Tunnel exit detected (GNSS restored or vehicle stopped). Reverting to astronomical dimming.");
        }
    }

    // 2. Astronomical Solar Elevation Calculation
    float elev_deg = solar_calculate_elevation_deg(lat_deg, lon_deg, utc_epoch_s);

    // 3. Smooth Dimming Curve
    // Above +6° (Day): 100% PWM
    if (elev_deg >= DIMMER_CIVIL_TWILIGHT_DEG) {
        return DIMMER_MAX_DAY_PCT;
    }
    // Below -6° (Night): 18% PWM
    if (elev_deg <= -DIMMER_CIVIL_TWILIGHT_DEG) {
        return DIMMER_MIN_NIGHT_PCT;
    }

    // Linear interpolation between -6° and +6° (Civil Twilight)
    // Normalized position t in [0.0, 1.0]: t = (elev - (-6)) / (6 - (-6)) = (elev + 6) / 12
    float t = (elev_deg + DIMMER_CIVIL_TWILIGHT_DEG) / (2.0f * DIMMER_CIVIL_TWILIGHT_DEG);
    float pwm_f = (float)DIMMER_MIN_NIGHT_PCT + t * (float)(DIMMER_MAX_DAY_PCT - DIMMER_MIN_NIGHT_PCT);

    uint8_t pwm_pct = (uint8_t)(pwm_f + 0.5f);
    if (pwm_pct < DIMMER_MIN_NIGHT_PCT) pwm_pct = DIMMER_MIN_NIGHT_PCT;
    if (pwm_pct > DIMMER_MAX_DAY_PCT) pwm_pct = DIMMER_MAX_DAY_PCT;

    return pwm_pct;
}

bool solar_dimmer_is_tunnel_active(void) {
    return s_tunnel_active;
}
