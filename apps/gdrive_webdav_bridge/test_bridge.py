"""Comprehensive unit and integration test suite for OpenMotorBridge Google Drive WebDAV Bridge."""

import base64
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from config import settings
from main import app
from notifier import parse_gpx_stats

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
