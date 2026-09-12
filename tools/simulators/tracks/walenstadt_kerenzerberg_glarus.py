#!/usr/bin/env python3
"""
OpenMotorBridge - Realistic Test Track Generator: Walenstadt -> Kerenzerberg -> Glarus -> T-Kreuzung
======================================================================================================
Geodetic trajectory generation with physical motorcycle dynamics for 15-State ADR-EKF,
GNSS receiver simulation, and RF propagation modeling.

Key Route Characteristics (Benutzer-Spezifikation):
1. Walenstadt Seepromenade (Start): Lat 47.1240° N, Lon 9.3140° E, Alt 425.0 m
   - Departure along Walensee, lake-side high-speed section (80-100 km/h).
2. Mühlehorn Vortunnel: Lat 47.1155° N, Lon 9.1850° E, Alt 428.0 m
   - Short 250 m tunnel (GNSS blackout: Sats -> 0, HDOP -> 99.9) immediately preceding highway exit.
3. Autobahn-Anschlusskreisel Mühlehorn (A3): Lat 47.1140° N, Lon 9.1720° E, Alt 430.0 m
   - Rapid deceleration from 100 to 35 km/h, 270° roundabout curve with high lateral acceleration (4.2 m/s²).
4. Kerenzerberg Passauffahrt (Obstalden -> Filzbach): Lat 47.1160° N -> 47.1180° N, Alt 430m -> 743m
   - Tight switchbacks, lean angles up to 43°.
   - NLOS (Non-Line-of-Sight): Steep rock crests separating hairpin terraces (>35 dB RF attenuation).
   - Forest sections (Wald): Dense foliage attenuation (0.35 dB/m on 2.4 GHz) and GNSS multipath (HDOP 1.8-2.6).
5. Kerenzerberg Passhöhe: Lat 47.1190° N, Lon 9.1050° E, Alt 743.0 m
   - Panoramic summit with open sky view over Walensee.
6. Serpentinen-Abfahrt Beglingen / Näfels: Alt 743m -> 440m
   - 12% descent, engine braking, rapid left-right transitions.
7. Glarus Hauptort: Lat 47.0400° N, Lon 9.0680° E, Alt 472.0 m
   - Urban valley floor, 50 km/h speed limit.
8. Schwanden / Hätzingen T-Kreuzung: Lat 46.9950° N, Lon 9.0750° E, Alt 520.0 m
   - Key junction: Left towards Klausenpass / Linthal, Right back towards Ziegelbrücke / Zürich.
"""

import math
from typing import List, Tuple

# Earth radius in meters (WGS-84 mean)
R_EARTH = 6371000.0

def latlon_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Haversine distance between two coordinates in meters."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2.0)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R_EARTH * c

def latlon_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Bearing in degrees from point 1 to point 2."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dlambda = math.radians(lon2 - lon1)
    y = math.sin(dlambda) * math.cos(phi2)
    x = math.cos(phi1)*math.sin(phi2) - math.sin(phi1)*math.cos(phi2)*math.cos(dlambda)
    b = math.degrees(math.atan2(y, x))
    return (b + 360.0) % 360.0

def latlon_offset(lat: float, lon: float, distance_m: float, bearing_deg: float) -> Tuple[float, float]:
    """Calculate target coordinate given distance in meters and bearing in degrees."""
    phi1 = math.radians(lat)
    lambda1 = math.radians(lon)
    theta = math.radians(bearing_deg)
    delta = distance_m / R_EARTH

    phi2 = math.asin(math.sin(phi1)*math.cos(delta) + math.cos(phi1)*math.sin(delta)*math.cos(theta))
    lambda2 = lambda1 + math.atan2(math.sin(theta)*math.sin(delta)*math.cos(phi1),
                                  math.cos(delta) - math.sin(phi1)*math.sin(phi2))
    return math.degrees(phi2), math.degrees(lambda2)

# Keyframes: (lat, lon, alt_m, target_speed_kmh, in_tunnel, in_forest, is_nlos, label)
ROUTE_KEYFRAMES = [
    (47.1240, 9.3140, 425.0, 50.0, False, False, False, "Walenstadt Seepromenade Start"),
    (47.1195, 9.2700, 426.0, 95.0, False, False, False, "Walensee Schnellstrasse Unterterzen"),
    (47.1165, 9.2250, 427.0, 90.0, False, False, False, "Walensee Murg Uferpassage"),
    (47.1158, 9.1890, 428.0, 85.0, False, False, False, "Muehlehorn Autobahn-Zulauf"),
    (47.1155, 9.1850, 428.0, 80.0, True,  False, False, "Muehlehorn Vortunnel Einfahrt"),
    (47.1148, 9.1780, 429.0, 55.0, True,  False, False, "Muehlehorn Vortunnel Ausfahrt"),
    (47.1140, 9.1720, 430.0, 35.0, False, False, False, "Muehlehorn A3 Kreisel (270 Grad Turn)"),
    (47.1148, 9.1630, 490.0, 55.0, False, True,  True,  "Kerenzerberg Kehre 1 (Wald & Fels-NLOS)"),
    (47.1155, 9.1530, 590.0, 48.0, False, True,  True,  "Kerenzerberg Kehre 2 (Serpentine Südhang)"),
    (47.1162, 9.1430, 685.0, 50.0, False, True,  True,  "Obstalden Hairpin 3 (Felsrippe NLOS)"),
    (47.1172, 9.1300, 710.0, 55.0, False, True,  False, "Kerenzerberg Mittelwald Schikane"),
    (47.1180, 9.1180, 720.0, 60.0, False, False, False, "Filzbach Hochebene"),
    (47.1190, 9.1050, 743.0, 65.0, False, False, False, "Kerenzerberg Passhoehe (Walensee-Blick)"),
    (47.1150, 9.0920, 670.0, 55.0, False, True,  True,  "Beglingen Kehre 1 Abfahrt (12% Gefaelle)"),
    (47.1080, 9.0780, 550.0, 58.0, False, True,  True,  "Beglingen Kehre 2 Abfahrt"),
    (47.1000, 9.0600, 440.0, 70.0, False, False, False, "Naefels / Mollis Taleinfahrt"),
    (47.0600, 9.0550, 455.0, 75.0, False, False, False, "Netstal Talstrasse"),
    (47.0400, 9.0680, 472.0, 50.0, False, False, False, "Glarus Stadtzentrum Ortsdurchfahrt"),
    (47.0150, 9.0720, 495.0, 65.0, False, False, False, "Mitloedi Talabschnitt"),
    (46.9950, 9.0750, 520.0, 40.0, False, False, False, "Schwanden T-Kreuzung (Links Klausen / Rechts Zuerich)")
]

class TrackPoint:
    """Instantaneous vehicle trajectory and sensor state."""
    def __init__(self, time_s: float, lat: float, lon: float, alt_m: float,
                 speed_kmh: float, heading_deg: float, yaw_rate_deg_s: float,
                 lean_angle_deg: float, in_tunnel: bool, sats_visible: int,
                 hdop: float, label: str = "", in_forest: bool = False,
                 is_nlos: bool = False):
        self.time_s = time_s
        self.lat = lat
        self.lon = lon
        self.alt_m = alt_m
        self.speed_kmh = speed_kmh
        self.speed_mps = speed_kmh / 3.6
        self.heading_deg = heading_deg
        self.yaw_rate_deg_s = yaw_rate_deg_s
        self.lean_angle_deg = lean_angle_deg
        self.in_tunnel = in_tunnel
        self.sats_visible = sats_visible
        self.hdop = hdop
        self.label = label
        self.in_forest = in_forest
        self.is_nlos = is_nlos

def generate_full_track(sample_rate_hz: float = 10.0) -> List[TrackPoint]:
    """
    Interpolates high-resolution trajectory along the Walenstadt -> Kerenzerberg -> Glarus route.
    Computes kinematics: yaw rate, centripetal acceleration, dynamic lean angle,
    tunnel transitions, roundabout dynamics, forest foliage, and rock NLOS zones.
    """
    dt = 1.0 / sample_rate_hz
    points: List[TrackPoint] = []
    
    current_time = 0.0
    prev_heading = None

    for i in range(len(ROUTE_KEYFRAMES) - 1):
        lat1, lon1, alt1, v1_kmh, tun1, for1, nlos1, lbl1 = ROUTE_KEYFRAMES[i]
        lat2, lon2, alt2, v2_kmh, tun2, for2, nlos2, lbl2 = ROUTE_KEYFRAMES[i+1]

        segment_dist = latlon_distance(lat1, lon1, lat2, lon2)
        avg_speed_mps = ((v1_kmh + v2_kmh) / 2.0) / 3.6
        if avg_speed_mps < 1.0:
            avg_speed_mps = 1.0
        segment_duration = segment_dist / avg_speed_mps
        steps = max(1, int(segment_duration / dt))

        bearing = latlon_bearing(lat1, lon1, lat2, lon2)

        is_roundabout = "Kreisel" in lbl1 or "Kreisel" in lbl2
        is_pass_climb = ("Kerenzerberg" in lbl1 or "Obstalden" in lbl1 or "Beglingen" in lbl1) and (alt1 > 450.0 or alt2 > 450.0)

        for step in range(steps):
            frac = step / float(steps)
            curr_lat = lat1 + frac * (lat2 - lat1)
            curr_lon = lon1 + frac * (lon2 - lon1)
            curr_alt = alt1 + frac * (alt2 - alt1)
            curr_v_kmh = v1_kmh + frac * (v2_kmh - v1_kmh)
            curr_v_mps = curr_v_kmh / 3.6

            in_tunnel = tun1 and tun2
            in_forest = for1 or (frac > 0.5 and for2)
            is_nlos = nlos1 or (frac > 0.3 and nlos2)

            if in_tunnel:
                # Slight tunnel wall curvature
                wobble = 4.0 * math.sin(current_time * 0.5)
            elif is_roundabout:
                # 270° continuous counter-clockwise roundabout turn (Querbeschleunigung ~4.2 m/s²)
                wobble = 65.0 * math.sin(frac * math.pi)
            elif is_pass_climb:
                # Alpine serpentines: hairpin switchbacks with high lean angles (up to 43°)
                wobble = 28.0 * math.sin(current_time * 0.48) + 10.0 * math.cos(current_time * 0.96)
            else:
                # Open road sweeping bends along Walensee and Glarnerland
                wobble = 14.0 * math.sin(current_time * 0.35) + 5.0 * math.cos(current_time * 0.70)

            eff_heading = (bearing + wobble) % 360.0

            # Compute yaw rate
            if prev_heading is None:
                yaw_rate_deg_s = 0.0
            else:
                dh = (eff_heading - prev_heading + 540.0) % 360.0 - 180.0
                yaw_rate_deg_s = dh / dt
            prev_heading = eff_heading

            # Centripetal lean angle: theta = arctan(v * yaw_rate / g)
            g = 9.80665
            yaw_rate_rad_s = math.radians(yaw_rate_deg_s)
            centripetal_accel = curr_v_mps * yaw_rate_rad_s
            lean_angle_deg = math.degrees(math.atan(centripetal_accel / g))
            # Clamp to realistic sport-touring motorcycle lean limit (43 deg)
            lean_angle_deg = max(-43.0, min(43.0, lean_angle_deg))

            # GNSS Satellite visibility and dilution of precision
            if in_tunnel:
                sats = 0
                hdop = 99.9 # Total GNSS loss in Vortunnel
            elif in_forest:
                # Canopy foliage attenuation and multipath
                sats = int(13 + 2.0 * math.sin(current_time * 0.08))
                hdop = 2.1 + 0.5 * math.cos(current_time * 0.05)
            elif is_pass_climb:
                # Mountain rock face partially shadowing southern/northern horizon
                sats = int(16 + 2.0 * math.sin(current_time * 0.06))
                hdop = 1.25 + 0.3 * math.cos(current_time * 0.04)
            else:
                # Normal open sky
                sats = int(20 + 2.0 * math.sin(current_time * 0.04))
                hdop = 0.75 + 0.12 * math.cos(current_time * 0.03)

            lbl = lbl1 if step == 0 else ""
            pt = TrackPoint(
                time_s=current_time,
                lat=curr_lat,
                lon=curr_lon,
                alt_m=curr_alt,
                speed_kmh=curr_v_kmh,
                heading_deg=eff_heading,
                yaw_rate_deg_s=yaw_rate_deg_s,
                lean_angle_deg=lean_angle_deg,
                in_tunnel=in_tunnel,
                sats_visible=sats,
                hdop=hdop,
                label=lbl,
                in_forest=in_forest,
                is_nlos=is_nlos
            )
            points.append(pt)
            current_time += dt

    # Final destination point (T-Kreuzung Schwanden)
    lat_f, lon_f, alt_f, v_f, tun_f, for_f, nlos_f, lbl_f = ROUTE_KEYFRAMES[-1]
    points.append(TrackPoint(
        time_s=current_time, lat=lat_f, lon=lon_f, alt_m=alt_f,
        speed_kmh=v_f, heading_deg=prev_heading or 0.0, yaw_rate_deg_s=0.0,
        lean_angle_deg=0.0, in_tunnel=False, sats_visible=21, hdop=0.7,
        label=lbl_f, in_forest=False, is_nlos=False
    ))

    return points

if __name__ == "__main__":
    track = generate_full_track(sample_rate_hz=10.0)
    print(f"===================================================================")
    print(f"  TRACK 2: WALENSTADT -> KERENZERBERG -> GLARUS -> T-KREUZUNG     ")
    print(f"===================================================================")
    print(f"Generated {len(track)} high-resolution track points.")
    print(f"Total simulated duration: {track[-1].time_s:.1f} s ({track[-1].time_s / 60.0:.1f} min)")
    
    tunnel_pts = [p for p in track if p.in_tunnel]
    forest_pts = [p for p in track if p.in_forest]
    nlos_pts = [p for p in track if p.is_nlos]
    max_lean = max(abs(p.lean_angle_deg) for p in track)
    min_alt = min(p.alt_m for p in track)
    max_alt = max(p.alt_m for p in track)

    print(f"Altitude range:      {min_alt:.1f} m -> {max_alt:.1f} m (Delta: {max_alt - min_alt:.1f} m)")
    print(f"Max dynamic lean:    {max_lean:.1f}°")
    print(f"Vortunnel blackout:  {len(tunnel_pts)} points ({len(tunnel_pts)/10.0:.1f} s)")
    print(f"Forest canopy zones: {len(forest_pts)} points ({len(forest_pts)/10.0:.1f} s)")
    print(f"NLOS rock face zones:{len(nlos_pts)} points ({len(nlos_pts)/10.0:.1f} s)")
    print(f"Start: {track[0].label} ({track[0].lat:.4f}°N, {track[0].lon:.4f}°E)")
    print(f"End:   {track[-1].label} ({track[-1].lat:.4f}°N, {track[-1].lon:.4f}°E)")
    print(f"===================================================================")
