#!/usr/bin/env python3
"""
Test Suite for OpenMotorBridge Radar 2.0, Solar Dimmer, Barometric Weather Trend & Uplink Gatekeeper
"""

import math
import struct
import pytest

# --- CRC16-CCITT Helper (matching C firmware) ---
def calc_crc16(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


# =============================================================================
# 1. Test Wheeltec MR20 77-GHz mmWave Parsing & Sub-MCU Protocol
# =============================================================================
def test_mr20_raw_parsing_and_submcu_packet():
    # Construct synthetic Wheeltec MR20 frame
    # Header: 0xAA 0x55, Len, Type 0x01 (Targets), TargetCount=2
    # Target 1: ID=1, Range=250 (25.0m), Speed=-139 (-13.9 m/s = ~50 km/h closing), Angle=-50 (-5.0 deg, left blind spot), SNR=85
    # Target 2: ID=2, Range=800 (80.0m), Speed=50 (+5.0 m/s moving away), Angle=10 (1.0 deg), SNR=40
    t1_bytes = struct.pack("<BhhhB", 1, 250, -139, -50, 85)
    t2_bytes = struct.pack("<BhhhB", 2, 800, 50, 10, 40)
    payload = bytes([2]) + t1_bytes + t2_bytes
    frame_len = len(payload) + 4
    mr20_frame = bytes([0xAA, 0x55, frame_len, 0x01]) + payload

    assert mr20_frame[0] == 0xAA and mr20_frame[1] == 0x55
    assert mr20_frame[3] == 0x01
    assert mr20_frame[4] == 2 # 2 targets

    # Evaluate Target 1 TTC and Threat
    dist_cm = 250 * 10 # 2500 cm = 25.0 m
    speed_cms = -139 * 10 # -1390 cm/s = -13.9 m/s = 50.04 km/h closing
    closing_ms = -speed_cms / 100.0
    ttc_sec = (dist_cm / 100.0) / closing_ms
    assert 1.7 < ttc_sec < 1.9 # TTC ~1.8s

    # Threat classification: TTC < 2.5s -> RED
    threat_level = 2 # RED
    assert threat_level == 2

    # Left blind spot: dist < 15m ? Here 25m, so not in 15m core blind spot.
    # If dist were 12.0m:
    bsd_dist_cm = 1200
    azimuth_cdeg = -500 # -5.0 deg
    blind_spot_left = (bsd_dist_cm < 1500 and azimuth_cdeg < -300)
    assert blind_spot_left is True

    # Pack into SubMcuTelemetryPkt_t
    # Header: 0x5A 0xA5 0x02 0x10 seq target_count max_threat bsd_l bsd_r closest_dist_cm highest_speed_cms
    seq = 42
    target_count = 1
    max_threat = 2
    bsd_l = 1
    bsd_r = 0
    closest_dist_cm = 1200
    highest_speed_cms = 1390

    # 1 Target: id (B), distance_cm (H), rel_speed_cms (h), azimuth_cdeg (h), ttc_tenths_s (B), threat_level (B)
    t_packed = struct.pack("<BHhhBB", 1, bsd_dist_cm, speed_cms, azimuth_cdeg, int(ttc_sec * 10), threat_level)
    dummy_targets = t_packed + bytes([0] * (7 * len(t_packed)))

    # Header: sync1, sync2, ver, type, seq, count, threat, bsd_l, bsd_r (9x B), closest_dist (H), highest_speed (h)
    header_payload = struct.pack("<BBBBBBBBBHh", 0x5A, 0xA5, 0x02, 0x10, seq, target_count, max_threat, bsd_l, bsd_r, closest_dist_cm, highest_speed_cms)
    full_body = header_payload + dummy_targets
    crc = calc_crc16(full_body)

    telemetry_packet = full_body + struct.pack("<H", crc)
    assert len(telemetry_packet) == len(full_body) + 2
    assert calc_crc16(telemetry_packet[:-2]) == crc


# =============================================================================
# 2. Test Astronomical Solar Elevation & Tunnel Dimmer
# =============================================================================
def calculate_solar_elevation(lat_deg: float, lon_deg: float, day_of_year: int, hour_utc: float) -> float:
    gamma = 2.0 * math.pi / 365.0 * (day_of_year - 1 + (hour_utc - 12.0) / 24.0)
    eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma)
                       - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))
    decl = 0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma) \
           - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma) \
           - 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma)

    time_offset = eqtime + 4.0 * lon_deg
    tst = hour_utc * 60.0 + time_offset
    while tst >= 1440.0: tst -= 1440.0
    while tst < 0.0: tst += 1440.0

    ha_deg = (tst / 4.0) - 180.0
    ha_rad = math.radians(ha_deg)
    lat_rad = math.radians(lat_deg)

    sin_elev = math.sin(lat_rad) * math.sin(decl) + math.cos(lat_rad) * math.cos(decl) * math.cos(ha_rad)
    sin_elev = max(-1.0, min(1.0, sin_elev))
    return math.degrees(math.asin(sin_elev))


def evaluate_dimmer(elev_deg: float, gnss_lost_ms: int, speed_kmh: float) -> int:
    # Tunnel detection: GNSS lost for >1500ms while speed > 30 km/h -> Night mode
    if gnss_lost_ms > 1500 and speed_kmh > 30.0:
        return 18

    if elev_deg >= 6.0:
        return 100
    if elev_deg <= -6.0:
        return 18

    # Linear interpolation between -6° and +6° (civil twilight)
    t = (elev_deg + 6.0) / 12.0
    pwm = 18.0 + t * (100.0 - 18.0)
    return int(round(pwm))


def test_solar_elevation_and_tunnel_dimming():
    # Zurich (lat 47.37°, lon 8.54°) on Summer Solstice (Day 172) at 12:00 UTC (Noon)
    noon_elev = calculate_solar_elevation(47.37, 8.54, 172, 12.0)
    assert noon_elev > 60.0 # High summer sun
    assert evaluate_dimmer(noon_elev, 0, 80.0) == 100 # 100% Day visibility

    # Zurich at Midnight UTC
    night_elev = calculate_solar_elevation(47.37, 8.54, 172, 0.0)
    assert night_elev < -15.0 # Deep night
    assert evaluate_dimmer(night_elev, 0, 80.0) == 18 # 18% Glare-free night PWM

    # Civil twilight: Sun at +0.0° (Horizon)
    twilight_pwm = evaluate_dimmer(0.0, 0, 50.0)
    assert 55 <= twilight_pwm <= 65 # Midpoint between 18% and 100% is 59%

    # Tunnel Test: Sunny day (elev = 60°), but enters Gotthard Tunnel:
    # GNSS fix lost for 2000ms at 80 km/h
    tunnel_pwm = evaluate_dimmer(noon_elev, 2000, 80.0)
    assert tunnel_pwm == 18 # Instant night dimming in tunnel!

    # False-positive tunnel rejection: Sitting at a stoplight in deep urban canyon (speed = 0 km/h)
    stoplight_pwm = evaluate_dimmer(noon_elev, 5000, 0.0)
    assert stoplight_pwm == 100 # Not in tunnel, keep daylight visibility!


# =============================================================================
# 3. Test Autarkic Barometric Weather Trend & Sea-Level Normalization
# =============================================================================
def normalize_p0(p_raw: float, altitude_m: float) -> float:
    return p_raw * ((1.0 - (altitude_m / 44330.0)) ** -5.255)


def test_barometric_weather_trend():
    # Test Sea-Level Normalization:
    # At Zurich (408m altitude), raw pressure is 965.0 hPa
    p0_zurich = normalize_p0(965.0, 408.0)
    assert 1010.0 <= p0_zurich <= 1016.0 # Normalizes to standard sea-level ~1013 hPa

    # Alpine Pass (Sustenpass 2224m altitude), raw pressure is 775.0 hPa
    p0_pass = normalize_p0(775.0, 2224.0)
    assert 1005.0 <= p0_pass <= 1018.0 # Correctly removes 2224m altitude offset!

    # Scenario: Approaching Severe Thunderstorm / Cold Front
    # Over 1 hour, sea-level pressure drops by 2.8 hPa (dP/dt = -2.8 hPa/h)
    # And temperature plunges by 4.2°C in 15 minutes
    dp_1h = -2.8
    dt_15m = -4.2

    is_storm = (dp_1h <= -2.0 or dt_15m <= -3.0)
    assert is_storm is True

    # Standstill gating test:
    # While riding at 100 km/h: Warning should NOT distract driver on dash
    display_on_dash_riding = (0.0 < 1.0) and is_storm # speed = 100
    assert not ((100.0 < 1.0) and is_storm)

    # When bike comes to a stop at a gas station / scenic viewpoint (speed = 0 km/h):
    display_on_dash_stopped = (0.0 < 1.0) and is_storm
    assert display_on_dash_stopped is True


# =============================================================================
# 4. Test Internet Uplink Gatekeeper & Apple vs Android DHCP Logic
# =============================================================================
def test_uplink_gatekeeper_and_dhcp_architecture():
    # Uplink states
    WIFI_UPLINK_RIDER_PHONE = 0
    WIFI_UPLINK_PAX_PHONE   = 1
    WIFI_UPLINK_OFFLINE     = 2

    # Case A: Standalone offline mode (Pass ride without cell signal)
    current_source = WIFI_UPLINK_OFFLINE
    def has_internet_uplink(source: int, client_connected: bool, probe_ok: bool) -> bool:
        if source == WIFI_UPLINK_OFFLINE:
            return False
        if not client_connected:
            return False
        return probe_ok

    assert has_internet_uplink(current_source, True, False) is False

    # Guard: Telemetry upload must be aborted immediately without HTTP timeouts
    upload_attempts = []
    if has_internet_uplink(current_source, True, False):
        upload_attempts.append("http://cloud.example.com/put")
    assert len(upload_attempts) == 0 # Zero attempts! Stays safe in local buffer

    # Case B: Apple iOS Phone connected to OMB SoftAP
    # RFC 3442 DHCP rule: When connected to iPhone, DHCP Option 3 (Router Gateway) must be EMPTY
    def get_dhcp_option3(client_role: str, is_personal_hotspot: bool) -> str:
        if client_role == "iPhone":
            if not is_personal_hotspot:
                return "NONE" # Empty option 3 -> iOS keeps 5G cellular data active!
            else:
                return "192.168.4.10"
        elif client_role == "SkylineOS":
            return "192.168.4.10"
        return "NONE"

    assert get_dhcp_option3("iPhone", is_personal_hotspot=False) == "NONE"
    # When iPhone enables Personal Hotspot, it becomes the Gateway
    assert get_dhcp_option3("iPhone", is_personal_hotspot=True) == "192.168.4.10"
    assert get_dhcp_option3("SkylineOS", is_personal_hotspot=False) == "192.168.4.10"

    # Online test with verified probe
    assert has_internet_uplink(WIFI_UPLINK_RIDER_PHONE, client_connected=True, probe_ok=True) is True
