"""Comprehensive unit and integration test suite for OpenMotorBridge Google Drive WebDAV Bridge."""

import base64
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from config import settings
from main import app
from notifier import parse_gpx_stats, build_human_summary

SAMPLE_GPX = b"""<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="OpenMotorBridge v8.0" xmlns="http://www.topografix.com/GPX/1/1" xmlns:omb="http://openmotorbridge.org/gpx/1/0">
  <trk>
    <name>Alpentour 2026</name>
    <trkseg>
      <trkpt lat="47.4125" lon="9.0435">
        <ele>550.0</ele>
        <time>2026-09-18T10:00:00Z</time>
        <extensions><omb:lean>12.4</omb:lean></extensions>
      </trkpt>
      <trkpt lat="47.4140" lon="9.0460">
        <ele>558.0</ele>
        <time>2026-09-18T10:01:00Z</time>
        <extensions><omb:lean>42.8</omb:lean></extensions>
      </trkpt>
      <trkpt lat="47.4160" lon="9.0490">
        <ele>565.0</ele>
        <time>2026-09-18T10:02:00Z</time>
        <extensions><omb:lean>31.2</omb:lean></extensions>
      </trkpt>
    </trkseg>
  </trk>
</gpx>"""

RICH_TELEMETRY_GPX = b"""<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="OpenMotorBridge v8.0" xmlns="http://www.topografix.com/GPX/1/1" xmlns:omb="http://openmotorbridge.org/gpx/1/0">
  <trk>
    <name>Silvretta Pass High Telemetry</name>
    <trkseg>
      <!-- Point 1: Upright departure -->
      <trkpt lat="47.0100" lon="10.0500">
        <ele>1200.0</ele>
        <time>2026-09-18T09:00:00Z</time>
        <speed>8.33</speed> <!-- 30 km/h -->
        <extensions>
          <omb:lean>0.0</omb:lean>
          <omb:temp>15.0</omb:temp>
          <omb:accel>0.15</omb:accel>
          <omb:rpm>3200</omb:rpm>
          <omb:battery>14.2</omb:battery>
          <omb:gear>2</omb:gear>
          <omb:comm_tier>hd</omb:comm_tier>
        </extensions>
      </trkpt>
      <!-- Point 2: Left turn entry -->
      <trkpt lat="47.0110" lon="10.0515">
        <ele>1225.0</ele>
        <time>2026-09-18T09:01:00Z</time>
        <speed>16.66</speed> <!-- 60 km/h -->
        <extensions>
          <omb:lean>-24.5</omb:lean>
          <omb:temp>15.5</omb:temp>
          <omb:accel>0.42</omb:accel>
          <omb:rpm>4800</omb:rpm>
          <omb:battery>14.2</omb:battery>
          <omb:gear>3</omb:gear>
          <omb:comm_tier>hd</omb:comm_tier>
        </extensions>
      </trkpt>
      <!-- Point 3: Left turn apex (max left lean) -->
      <trkpt lat="47.0125" lon="10.0530">
        <ele>1250.0</ele>
        <time>2026-09-18T09:02:00Z</time>
        <speed>15.0</speed> <!-- 54 km/h -->
        <extensions>
          <omb:lean>-38.6</omb:lean>
          <omb:temp>16.0</omb:temp>
          <omb:accel>-0.55</omb:accel>
          <omb:rpm>5100</omb:rpm>
          <omb:battery>14.1</omb:battery>
          <omb:gear>2</omb:gear>
          <omb:comm_tier>lora</omb:comm_tier>
        </extensions>
      </trkpt>
      <!-- Point 4: Straight transition -->
      <trkpt lat="47.0140" lon="10.0550">
        <ele>1270.0</ele>
        <time>2026-09-18T09:03:00Z</time>
        <speed>22.22</speed> <!-- 80 km/h -->
        <extensions>
          <omb:lean>2.0</omb:lean>
          <omb:temp>17.2</omb:temp>
          <omb:accel>0.62</omb:accel>
          <omb:rpm>6200</omb:rpm>
          <omb:battery>14.3</omb:battery>
          <omb:gear>4</omb:gear>
          <omb:comm_tier>hd</omb:comm_tier>
        </extensions>
      </trkpt>
      <!-- Point 5: Right turn entry -->
      <trkpt lat="47.0155" lon="10.0570">
        <ele>1265.0</ele>
        <time>2026-09-18T09:04:00Z</time>
        <speed>16.0</speed>
        <extensions>
          <omb:lean>26.0</omb:lean>
          <omb:temp>18.0</omb:temp>
          <omb:accel>-0.68</omb:accel>
          <omb:rpm>4500</omb:rpm>
          <omb:battery>14.1</omb:battery>
          <omb:gear>3</omb:gear>
          <omb:comm_tier>hd</omb:comm_tier>
        </extensions>
      </trkpt>
      <!-- Point 6: Right turn apex (max right lean) -->
      <trkpt lat="47.0170" lon="10.0590">
        <ele>1245.0</ele>
        <time>2026-09-18T09:05:00Z</time>
        <speed>14.0</speed>
        <extensions>
          <omb:lean>44.2</omb:lean>
          <omb:temp>18.5</omb:temp>
          <omb:accel>0.30</omb:accel>
          <omb:rpm>5800</omb:rpm>
          <omb:battery>14.2</omb:battery>
          <omb:gear>2</omb:gear>
          <omb:comm_tier>hd</omb:comm_tier>
        </extensions>
      </trkpt>
      <!-- Point 7: Straight arrival / stop -->
      <trkpt lat="47.0180" lon="10.0600">
        <ele>1240.0</ele>
        <time>2026-09-18T09:06:00Z</time>
        <speed>0.0</speed>
        <extensions>
          <omb:lean>0.0</omb:lean>
          <omb:temp>19.0</omb:temp>
          <omb:accel>0.0</omb:accel>
          <omb:rpm>1100</omb:rpm>
          <omb:battery>13.8</omb:battery>
          <omb:gear>1</omb:gear>
          <omb:comm_tier>hd</omb:comm_tier>
        </extensions>
      </trkpt>
    </trkseg>
  </trk>
</gpx>"""


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_settings(monkeypatch):
    """Configures predictable test settings."""
    monkeypatch.setattr(settings, "WEBDAV_USER", "testuser")
    monkeypatch.setattr(settings, "WEBDAV_PASSWORD", "testpass123")
    monkeypatch.setattr(settings, "GOOGLE_CLIENT_ID", "mock_client_id")
    monkeypatch.setattr(settings, "GOOGLE_CLIENT_SECRET", "mock_secret")
    monkeypatch.setattr(settings, "GOOGLE_REFRESH_TOKEN", "mock_refresh")
    monkeypatch.setattr(settings, "GOOGLE_DRIVE_FOLDER", "omb/test_tracks")
    monkeypatch.setattr(settings, "MQTT_ENABLED", False)
    monkeypatch.setattr(settings, "MQTT_BROKER", None)
    monkeypatch.setattr(settings, "WEBHOOK_URL", None)


def auth_header(user="testuser", pwd="testpass123"):
    token = base64.b64encode(f"{user}:{pwd}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def test_health_check(client):
    """Verifies the health check endpoint returns 200 and expected status."""
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["service"] == "omb-gdrive-bridge"
    assert data["gdrive_ready"] is True
    assert data["target_folder"] == "omb/test_tracks"


def test_webdav_options(client):
    """Verifies OPTIONS request returns proper WebDAV DAV: 1 headers."""
    resp = client.options("/tracks")
    assert resp.status_code == 200
    assert "DAV" in resp.headers
    assert "1" in resp.headers["DAV"]
    assert "PUT" in resp.headers.get("Allow", "")
    assert "MKCOL" in resp.headers.get("Allow", "")


def test_webdav_mkcol_authorized(client):
    """Verifies MKCOL creates a collection with HTTP 201 when authenticated."""
    resp = client.request("MKCOL", "/tracks", headers=auth_header())
    assert resp.status_code == 201


def test_webdav_mkcol_unauthorized(client):
    """Verifies MKCOL rejects unauthenticated calls with 401."""
    resp = client.request("MKCOL", "/tracks")
    assert resp.status_code == 401


def test_webdav_propfind(client):
    """Verifies PROPFIND returns 207 Multi-Status XML."""
    resp = client.request("PROPFIND", "/tracks", headers=auth_header())
    assert resp.status_code == 207
    assert "xml" in resp.headers.get("content-type", "")
    assert "multistatus" in resp.text


def test_webdav_put_unauthorized(client):
    """Verifies PUT rejects invalid password with 401."""
    resp = client.put(
        "/tracks/tour.gpx",
        content=SAMPLE_GPX,
        headers=auth_header("testuser", "wrongpassword"),
    )
    assert resp.status_code == 401


def test_webdav_put_empty_body(client):
    """Verifies PUT rejects empty body with 400."""
    resp = client.put(
        "/tracks/empty.gpx",
        content=b"",
        headers=auth_header(),
    )
    assert resp.status_code == 400


@patch("main.gdrive_client.upload_file", new_callable=AsyncMock)
def test_webdav_put_success(mock_upload, client):
    """Verifies successful WebDAV PUT uploads to Google Drive and returns HTTP 201."""
    mock_upload.return_value = {
        "id": "gdrive_file_12345",
        "name": "alpentour.gpx",
        "webViewLink": "https://drive.google.com/file/d/gdrive_file_12345/view",
        "size": "1024",
    }

    resp = client.put(
        "/tracks/alpentour.gpx",
        content=SAMPLE_GPX,
        headers={**auth_header(), "Content-Type": "application/gpx+xml"},
    )

    assert resp.status_code == 201
    assert resp.headers["Location"] == "/tracks/alpentour.gpx"
    data = resp.json()
    assert data["status"] == "created"
    assert data["file_id"] == "gdrive_file_12345"
    assert data["name"] == "alpentour.gpx"

    mock_upload.assert_called_once_with(
        "alpentour.gpx",
        SAMPLE_GPX,
        "application/gpx+xml",
    )


def test_gpx_statistics_parsing():
    """Verifies GPX parsing calculates point counts, distance, and max lean angle."""
    stats = parse_gpx_stats(SAMPLE_GPX)
    assert stats["point_count"] == 3
    assert stats["distance_km"] > 0.3  # Around ~0.45 km
    assert stats["max_lean_deg"] == 42.8
    assert stats["duration_s"] == 120  # 10:00:00 to 10:02:00
    assert "2026-09-18T10:00:00" in stats["start_time"]
    assert "2026-09-18T10:02:00" in stats["end_time"]


def test_gpx_extended_statistics_parsing():
    """Verifies rich telemetry: elevation gain/loss, temperature min/max/avg, acceleration, lean left/right, RPM and curves."""
    stats = parse_gpx_stats(RICH_TELEMETRY_GPX)

    # Point count & timing
    assert stats["point_count"] == 7
    assert stats["duration_s"] == 360  # 09:00 to 09:06 = 6 mins
    assert stats["netto_duration_s"] > 0
    assert stats["distance_km"] > 0.5

    # Elevation profile
    assert stats["elevation_min_m"] == 1200.0
    assert stats["elevation_max_m"] == 1270.0
    assert stats["elevation_gain_m"] == 70.0   # 1200 -> 1225 (+25) -> 1250 (+25) -> 1270 (+20) = 70
    assert stats["elevation_loss_m"] == 30.0   # 1270 -> 1265 (-5) -> 1245 (-20) -> 1240 (-5) = 30

    # Ambient Temperature
    assert stats["temp_min_c"] == 15.0
    assert stats["temp_max_c"] == 19.0
    assert 17.0 <= stats["temp_avg_c"] <= 17.5

    # Accelerations & Decelerations
    assert stats["max_accel_g"] == 0.62
    assert stats["max_decel_g"] == 0.68

    # Lean Angles & Curves
    assert stats["max_lean_left_deg"] == 38.6
    assert stats["max_lean_right_deg"] == 44.2
    assert stats["max_lean_deg"] == 44.2
    assert stats["curve_count_left"] == 1
    assert stats["curve_count_right"] == 1
    assert stats["curve_count_total"] == 2

    # Engine RPM & Battery
    assert stats["rpm_max"] == 6200
    assert stats["rpm_avg"] > 3000
    assert stats["battery_v_min"] == 13.8

    # Gear Shift Counter
    assert stats["shifts_total"] == 6
    assert stats["shifts_up"] == 2
    assert stats["shifts_down"] == 4
    assert stats["shifts_per_km"] > 0

    # Hard Braking & Dynamics
    assert stats["hard_braking_count"] == 1
    assert stats["time_at_lean_pct"] > 0
    assert stats["corner_density_per_km"] > 0

    # Radio Intercom QoS & LoRa Fallback
    assert stats["comm_lora_fallback_count"] == 1
    assert stats["comm_lora_fallback_duration_s"] == 60
    assert stats["comm_hd_pct"] == 83.3

    # Summary texts in default, sport, group, and cruise modes
    summary = stats.get("summary_text", "")
    assert "Silvretta Pass High Telemetry" in summary or "Tour" in summary
    assert "15.0 °C – 19.0 °C" in summary
    assert "38.6° L / 44.2° R" in summary
    assert "Beschl.: +0.62g" in summary
    assert "Bremsen: -0.68g" in summary
    assert "6.200 U/min" in summary
    assert "+70 hm" in summary
    assert "Schaltvorgänge: 6" in summary
    assert "83.3% HD" in summary
    assert "1x LoRa-Fallback" in summary

    # Sport summary
    sport_summary = stats.get("summary_sport", "")
    assert "[Sportlich]" in sport_summary
    assert "Schaltvorgänge" in sport_summary
    assert "1 Notbremsungen" in sport_summary

    # Group summary
    group_summary = stats.get("summary_group", "")
    assert "[Gruppe / Mesh]" in group_summary
    assert "83.3% HD-Voice" in group_summary
    assert "1x LoRa-Fallback" in group_summary

    # Cruise summary
    cruise_summary = stats.get("summary_cruise", "")
    assert "[Cruising & Tour]" in cruise_summary
    assert "Reisegeschwindigkeit" in cruise_summary


def test_build_human_summary_formatting():
    """Verifies that build_human_summary generates structured text with all key metrics."""
    mock_stats = {
        "start_time": "2026-09-18T10:15:00+02:00",
        "end_time": "2026-09-18T12:45:00+02:00",
        "duration_s": 9000,         # 2h 30m
        "netto_duration_s": 7800,   # 2h 10m
        "distance_km": 142.5,
        "speed_max_kmh": 118.4,
        "speed_avg_kmh": 65.8,
        "elevation_min_m": 420.0,
        "elevation_max_m": 1890.0,
        "elevation_gain_m": 2150.0,
        "temp_min_c": 11.5,
        "temp_max_c": 24.2,
        "temp_avg_c": 18.3,
        "max_lean_left_deg": 41.5,
        "max_lean_right_deg": 43.8,
        "curve_count_left": 128,
        "curve_count_right": 134,
        "curve_count_total": 262,
        "max_accel_g": 0.74,
        "max_decel_g": 0.89,
        "rpm_max": 7800,
        "rpm_avg": 4250,
        "battery_v_min": 13.9,
    }
    summary = build_human_summary(mock_stats, "Stelvio_Pass.gpx")

    assert "Stelvio_Pass.gpx" in summary
    assert "10:15 – 12:45 Uhr" in summary
    assert "2h 10m" in summary
    assert "142.5 km" in summary
    assert "+2.150 hm" in summary
    assert "(420 m – 1890 m)" in summary
    assert "11.5 °C – 24.2 °C (Ø 18.3 °C)" in summary
    assert "118.4 km/h" in summary
    assert "Ø 65.8 km/h" in summary
    assert "Beschl.: +0.74g" in summary
    assert "Bremsen: -0.89g" in summary
    assert "41.5° L / 43.8° R" in summary
    assert "262 Kurven (128 L / 134 R)" in summary
    assert "7.800 U/min" in summary


def test_mode_tailored_summaries():
    """Verifies that each mode (sport, group, cruise) highlights its respective domain scorecard."""
    mock_stats = {
        "start_time": "2026-09-18T14:00:00+02:00",
        "end_time": "2026-09-18T16:00:00+02:00",
        "duration_s": 7200,
        "netto_duration_s": 6300,
        "pause_duration_s": 900,
        "distance_km": 94.0,
        "speed_max_kmh": 124.0,
        "speed_avg_kmh": 53.7,
        "elevation_min_m": 800.0,
        "elevation_max_m": 1950.0,
        "elevation_gain_m": 1450.0,
        "temp_min_c": 14.0,
        "temp_max_c": 22.0,
        "temp_avg_c": 17.5,
        "max_lean_left_deg": 46.2,
        "max_lean_right_deg": 48.0,
        "curve_count_left": 85,
        "curve_count_right": 87,
        "curve_count_total": 172,
        "time_at_lean_pct": 24.5,
        "corner_density_per_km": 1.8,
        "max_accel_g": 0.82,
        "max_decel_g": 0.95,
        "hard_braking_count": 2,
        "rpm_max": 9400,
        "shifts_total": 312,
        "shifts_per_km": 3.3,
        "comm_hd_pct": 94.2,
        "comm_lora_fallback_count": 2,
        "comm_lora_fallback_duration_s": 180,
        "battery_v_min": 13.8,
        "battery_v_avg": 14.2,
    }

    # 1. Sport mode
    sport = build_human_summary(mock_stats, "Hahntennjoch.gpx", mode="sport")
    assert "[Sportlich]" in sport
    assert "46.2° L / 48.0° R (24.5% in Schräglage)" in sport
    assert "312 Schaltvorgänge (3.3/km)" in sport
    assert "1.8 Kurven/km" in sport
    assert "Bremsen: -0.95g (2 Notbremsungen)" in sport
    assert "RPM max: 9.400 U/min" in sport

    # 2. Group mode
    group = build_human_summary(mock_stats, "Hahntennjoch.gpx", mode="group")
    assert "[Gruppe / Mesh]" in group
    assert "94.2% HD-Voice" in group
    assert "2x LoRa-Fallback (3m)" in group
    assert "Kolonnen-Tempo: Ø 53.7 km/h" in group

    # 3. Cruise mode
    cruise = build_human_summary(mock_stats, "Hahntennjoch.gpx", mode="cruise")
    assert "[Cruising & Tour]" in cruise
    assert "Pausen: 15m" in cruise
    assert "Reisegeschwindigkeit: Ø 53.7 km/h" in cruise
    assert "Bremsruhe: 2 stärkere Bremsungen" in cruise
    assert "Temp: 14.0 °C – 22.0 °C (Ø 17.5 °C)" in cruise


