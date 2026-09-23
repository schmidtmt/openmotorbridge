#pragma once

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge - Astronomical Solar Elevation & Tunnel Dimmer
// Computes Sun Elevation Angle and evaluates Mirror/LED Dimming (18% - 100%)
// =============================================================================

#define DIMMER_MIN_NIGHT_PCT        18   // 18% PWM prevents driver glare at night/tunnel
#define DIMMER_MAX_DAY_PCT          100  // 100% daylight visibility
#define DIMMER_CIVIL_TWILIGHT_DEG   6.0f // Threshold: Sun elevation +/- 6 deg

/**
 * @brief Berechnet den Sonnenstandswinkel (Solar Elevation Angle in Grad)
 * @param lat_deg Breitengrad (-90.0 bis +90.0, WGS84)
 * @param lon_deg Längengrad (-180.0 bis +180.0, WGS84)
 * @param utc_epoch_s Unix-Timestamp in Sekunden (UTC)
 * @return Sonnenhöhenwinkel in Grad (+90° = Zenit, 0° = Horizont, -90° = Nadir)
 */
float solar_calculate_elevation_deg(float lat_deg, float lon_deg, uint32_t utc_epoch_s);

/**
 * @brief Ermittelt den aktuellen Dimmwert (18% - 100%) unter Berücksichtigung von
 *        Sonnenstand und Tunnel-Detektion (GNSS-Abriss bei Tempo > 30 km/h)
 * @param lat_deg Breitengrad
 * @param lon_deg Längengrad
 * @param utc_epoch_s UTC Unix-Timestamp
 * @param gnss_fix_valid True wenn GNSS Fix aktiv
 * @param speed_kmh Aktuelle Fahrzeuggeschwindigkeit in km/h
 * @return Dimm-Prozentwert von 18 bis 100%
 */
uint8_t solar_dimmer_evaluate(float lat_deg, float lon_deg, uint32_t utc_epoch_s,
                              bool gnss_fix_valid, float speed_kmh);

/**
 * @brief Gibt zurück, ob die Tunnel-Dimmung aktuell aktiv ist
 */
bool solar_dimmer_is_tunnel_active(void);

#ifdef __cplusplus
}
#endif
