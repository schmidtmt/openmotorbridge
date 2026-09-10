#!/usr/bin/env python3
"""
OpenMotorBridge - Realistic Test Track Generator: Wil -> Wattwil (Tunnel) -> Rickenpass
======================================================================================
Geodetic trajectory generation with realistic physical dynamics for 15-State ADR-EKF,
GNSS receiver simulation, and RF propagation modeling.

Key Waypoints & Characteristics:
1. Wil SG (Start): Lat 47.4640° N, Lon 9.0430° E, Alt 570.0 m
   - Urban departure, clear sky view, 18-22 satellites, speed 50 km/h.
2. Schnellstrasse Bazenheid / Dietfurt: Lat 47.3800° N, Lon 9.0650° E, Alt 605.0 m
   - Open rural highway, speeds 80-100 km/h, 2.4 GHz OMM mesh fully connected.
3. Umfahrung Wattwil - Tunnel Entrance: Lat 47.2970° N, Lon 9.0790° E, Alt 625.0 m
   - 2.2 km curved tunnel: GNSS blackout (Sats -> 0, HDOP -> 99.9).
   - Tunnel RF attenuation: >35 dB on 2.4 GHz (triggers handover to 868 MHz LoRa).
   - S-curves inside tunnel generating IMU yaw rate for ADR-EKF dead reckoning.
4. Wattwil Kreisel (Tunnel Exit & Divergence Point): Lat 47.2880° N, Lon 9.0830° E, Alt 635.0 m
   - Roundabout immediately after tunnel exit: tests whether EKF dead-reckoning holds
     the curve geometry or drifts into the Ebnat-Kappel branch before GNSS re-acquires.
5. Rickenpass Ascent & Summit: Lat 47.2580° N, Lon 9.0480° E, Alt 795.0 m
   - Alpine switchbacks, dynamic lean angles up to 42°, variable motorcycle gap (30-800 m).
"""

import math
from typing import List, Dict, Any, Tuple

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

# Master Route Keyframes: (lat, lon, alt_m, target_speed_kmh, in_tunnel, label)
ROUTE_KEYFRAMES = [
    (47.4640, 9.0430, 570.0, 50.0, False, "Wil SG Departure"),
    (47.4350, 9.0520, 580.0, 75.0, False, "Bazenheid Approach"),
    (47.3800, 9.0650, 605.0, 90.0, False, "Dietfurt Schnellstrasse"),
    (47.3300, 9.0720, 615.0, 85.0, False, "Lichtensteig Pre-Tunnel"),
    (47.2970, 9.0790, 625.0, 80.0, True,  "Wattwil Tunnel Entrance"),
    (47.2925, 9.0810, 630.0, 80.0, True,  "Wattwil Tunnel Mid S-Curve"),
    (47.2885, 9.0828, 634.0, 60.0, True,  "Wattwil Tunnel Pre-Exit Deceleration"),
    (47.2880, 9.0830, 635.0, 40.0, False, "Wattwil Kreisel Roundabout Exit"),
    (47.2750, 9.0680, 690.0, 65.0, False, "Rickenpass Lower Switchback"),
    (47.2650, 9.0550, 745.0, 60.0, False, "Rickenpass Hairpin 1"),
    (47.2580, 9.0480, 795.0, 65.0, False, "Rickenpass Summit Passhöhe")
]

class TrackPoint:
    """Instantaneous vehicle trajectory and sensor state."""
    def __init__(self, time_s: float, lat: float, lon: float, alt_m: float,
                 speed_kmh: float, heading_deg: float, yaw_rate_deg_s: float,
                 lean_angle_deg: float, in_tunnel: bool, sats_visible: int,
                 hdop: float, label: str = ""):
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

def generate_full_track(sample_rate_hz: float = 10.0) -> List[TrackPoint]:
    """
    Interpolates high-resolution trajectory along the Wil -> Wattwil -> Ricken route.
    Computes kinematics: yaw rate, centripetal acceleration, dynamic lean angle.
    """
    dt = 1.0 / sample_rate_hz
    points: List[TrackPoint] = []
    
    current_time = 0.0
    prev_heading = None

    for i in range(len(ROUTE_KEYFRAMES) - 1):
        lat1, lon1, alt1, v1_kmh, tun1, lbl1 = ROUTE_KEYFRAMES[i]
        lat2, lon2, alt2, v2_kmh, tun2, lbl2 = ROUTE_KEYFRAMES[i+1]

        segment_dist = latlon_distance(lat1, lon1, lat2, lon2)
        avg_speed_mps = ((v1_kmh + v2_kmh) / 2.0) / 3.6
        if avg_speed_mps < 1.0:
            avg_speed_mps = 1.0
        segment_duration = segment_dist / avg_speed_mps
        steps = max(1, int(segment_duration / dt))

        bearing = latlon_bearing(lat1, lon1, lat2, lon2)

        for step in range(steps):
            frac = step / float(steps)
            curr_lat = lat1 + frac * (lat2 - lat1)
            curr_lon = lon1 + frac * (lon2 - lon1)
            curr_alt = alt1 + frac * (alt2 - alt1)
            curr_v_kmh = v1_kmh + frac * (v2_kmh - v1_kmh)
            curr_v_mps = curr_v_kmh / 3.6

            # S-curve oscillation inside the tunnel for realistic steering
            in_tunnel = tun1 or (frac > 0.5 and tun2)
            eff_heading = bearing
            if in_tunnel:
                # Add sinusoidal lateral wobble simulating lane curves inside the 2.2km tube
                wobble = 6.0 * math.sin(current_time * 0.4)
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
            # Clamp to realistic motorcycle lean limit (45 deg)
            lean_angle_deg = max(-45.0, min(45.0, lean_angle_deg))

            # GNSS Satellite visibility and dilution of precision
            if in_tunnel:
                sats = 0
                hdop = 99.9 # Total GNSS loss
            else:
                # Normal sky view with slight natural variation
                sats = int(19 + 2.0 * math.sin(current_time * 0.05))
                hdop = 0.75 + 0.15 * math.cos(current_time * 0.03)

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
                label=lbl
            )
            points.append(pt)
            current_time += dt

    # Final summit point
    lat_f, lon_f, alt_f, v_f, tun_f, lbl_f = ROUTE_KEYFRAMES[-1]
    points.append(TrackPoint(
        time_s=current_time, lat=lat_f, lon=lon_f, alt_m=alt_f,
        speed_kmh=v_f, heading_deg=prev_heading or 0.0, yaw_rate_deg_s=0.0,
        lean_angle_deg=0.0, in_tunnel=False, sats_visible=21, hdop=0.7, label=lbl_f
    ))

    return points

if __name__ == "__main__":
    track = generate_full_track(sample_rate_hz=10.0)
    print(f"Generated {len(track)} track points.")
    print(f"Total simulated duration: {track[-1].time_s:.1f} s ({track[-1].time_s / 60.0:.1f} min)")
    tunnel_pts = [p for p in track if p.in_tunnel]
    print(f"Tunnel points: {len(tunnel_pts)} ({len(tunnel_pts)/10.0:.1f} s in blackout)")
    print(f"Start: {track[0].label} ({track[0].lat:.4f}, {track[0].lon:.4f})")
    print(f"End:   {track[-1].label} ({track[-1].lat:.4f}, {track[-1].lon:.4f})")
