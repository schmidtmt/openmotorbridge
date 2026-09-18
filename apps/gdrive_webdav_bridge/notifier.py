"""Optional event notification module for OpenMotorBridge Google Drive WebDAV Bridge.

Extracts track summary statistics from uploaded GPX files and publishes events
via MQTT (e.g. to Home Assistant / Homesphere) and/or Webhook.
"""

import json
import logging
import math
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
import httpx

from config import settings

logger = logging.getLogger("omb.notifier")


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance in kilometers between two GPS coordinates."""
    r = 6371.0  # Earth radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2.0) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return r * c


def parse_gpx_stats(content: bytes) -> Dict[str, Any]:
    """Extracts summary statistics from a GPX XML file."""
    stats = {
        "point_count": 0,
        "distance_km": 0.0,
        "duration_s": 0,
        "max_lean_deg": 0.0,
        "start_time": None,
        "end_time": None,
    }

    try:
        root = ET.fromstring(content)
        # Handle namespaces cleanly by stripping or matching local names
        points: List[Tuple[float, float, Optional[datetime], float]] = []

        # Iterate all trkpt elements regardless of namespace
        for elem in root.iter():
            if elem.tag.endswith("trkpt"):
                lat = float(elem.attrib.get("lat", 0.0))
                lon = float(elem.attrib.get("lon", 0.0))
                pt_time = None
                lean = 0.0

                for child in elem:
                    if child.tag.endswith("time") and child.text:
                        try:
                            # ISO 8601 parsing
                            pt_time = datetime.fromisoformat(child.text.replace("Z", "+00:00"))
                        except Exception:
                            pass
                    elif child.tag.endswith("extensions"):
                        for ext in child:
                            if "lean" in ext.tag.lower() and ext.text:
                                try:
                                    lean = abs(float(ext.text))
                                except Exception:
                                    pass

                points.append((lat, lon, pt_time, lean))

        if not points:
            return stats

        stats["point_count"] = len(points)
        max_lean = max((p[3] for p in points), default=0.0)
        stats["max_lean_deg"] = round(max_lean, 1)

        # Distance calculation
        total_dist = 0.0
        for i in range(1, len(points)):
            lat1, lon1, _, _ = points[i - 1]
            lat2, lon2, _, _ = points[i]
            if lat1 != 0.0 and lon1 != 0.0 and lat2 != 0.0 and lon2 != 0.0:
                total_dist += haversine_distance(lat1, lon1, lat2, lon2)
        stats["distance_km"] = round(total_dist, 2)

        # Duration
        times = [p[2] for p in points if p[2] is not None]
        if times:
            t_start = min(times)
            t_end = max(times)
            stats["start_time"] = t_start.isoformat()
            stats["end_time"] = t_end.isoformat()
            stats["duration_s"] = int((t_end - t_start).total_seconds())

    except Exception as e:
        logger.warning(f"Could not parse GPX track statistics: {e}")

    return stats


async def dispatch_upload_event(filename: str, file_info: Dict[str, Any], content: bytes):
    """Dispatches upload event to MQTT and/or Webhook if configured."""
    stats = parse_gpx_stats(content)
    payload = {
        "event": "track_uploaded",
        "filename": filename,
        "size_bytes": len(content),
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "gdrive_file_id": file_info.get("id"),
        "gdrive_link": file_info.get("webViewLink"),
        "stats": stats,
    }

    # 1. Dispatch via MQTT if enabled
    if settings.MQTT_ENABLED or settings.MQTT_BROKER:
        broker = settings.MQTT_BROKER or "localhost"
        try:
            import paho.mqtt.client as mqtt

            client = mqtt.Client()
            if settings.MQTT_USERNAME and settings.MQTT_PASSWORD:
                client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)

            client.connect(broker, settings.MQTT_PORT, keepalive=10)
            json_payload = json.dumps(payload, ensure_ascii=False)
            result = client.publish(settings.MQTT_TOPIC, json_payload, qos=1)
            result.wait_for_publish(timeout=3.0)
            client.disconnect()
            logger.info(f"Published upload notification to MQTT '{settings.MQTT_TOPIC}' on {broker}:{settings.MQTT_PORT}")
        except Exception as e:
            logger.error(f"Failed to publish MQTT upload notification: {e}")

    # 2. Dispatch via Webhook if configured
    if settings.WEBHOOK_URL:
        try:
            async with httpx.AsyncClient(timeout=5.0) as http_client:
                resp = await http_client.post(settings.WEBHOOK_URL, json=payload)
                logger.info(f"Webhook dispatched to {settings.WEBHOOK_URL} -> HTTP {resp.status_code}")
        except Exception as e:
            logger.error(f"Failed to dispatch webhook: {e}")
