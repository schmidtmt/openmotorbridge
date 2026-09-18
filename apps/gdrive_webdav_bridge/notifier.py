"""Optional event notification module for OpenMotorBridge Google Drive WebDAV Bridge.

Extracts rich ride summary statistics from uploaded GPX files (netto ride time,
elevation profile, temperature min/max/avg, acceleration/braking g-forces,
left/right lean angles, engine RPM, and turn counter) and publishes events
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


def format_duration(seconds: int) -> str:
    """Formats seconds into human readable duration (e.g. '3h 24m' or '45m')."""
    if seconds <= 0:
        return "0m"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    if hours > 0:
        return f"{hours}h {minutes:02d}m"
    return f"{minutes}m"


def build_human_summary(stats: Dict[str, Any], filename: str) -> str:
    """Creates a beautifully formatted human-readable summary text for push/chat/MQTT."""
    lines = [f"🏁 OpenMotorBridge: Tour abgeschlossen ({filename})"]

    # Date & Times
    if stats.get("start_time") and stats.get("end_time"):
        try:
            t_start = datetime.fromisoformat(stats["start_time"])
            t_end = datetime.fromisoformat(stats["end_time"])
            date_str = t_start.strftime("%d.%m.%Y")
            time_span = f"{t_start.strftime('%H:%M')} – {t_end.strftime('%H:%M')} Uhr"
            net_str = format_duration(stats.get("netto_duration_s", stats.get("duration_s", 0)))
            lines.append(f"📅 {date_str} · {time_span} (Netto: {net_str})")
        except Exception:
            pass

    # Distance & Elevation
    dist_km = stats.get("distance_km", 0.0)
    ele_gain = stats.get("elevation_gain_m")
    ele_min = stats.get("elevation_min_m")
    ele_max = stats.get("elevation_max_m")

    dist_line = f"📍 {dist_km:.1f} km"
    if ele_gain is not None and ele_min is not None and ele_max is not None:
        dist_line += f" · ⛰️ +{int(ele_gain):,} hm ({int(ele_min)} m – {int(ele_max)} m)".replace(",", ".")
    lines.append(dist_line)

    # Temperature
    t_min = stats.get("temp_min_c")
    t_max = stats.get("temp_max_c")
    t_avg = stats.get("temp_avg_c")
    if t_avg is not None:
        if t_min is not None and t_max is not None and t_min != t_max:
            lines.append(f"🌡️ Temp: {t_min:.1f} °C – {t_max:.1f} °C (Ø {t_avg:.1f} °C)")
        else:
            lines.append(f"🌡️ Temp: Ø {t_avg:.1f} °C")

    # Lean angle & Curves
    lean_l = stats.get("max_lean_left_deg", 0.0)
    lean_r = stats.get("max_lean_right_deg", 0.0)
    curves_tot = stats.get("curve_count_total", 0)
    curves_l = stats.get("curve_count_left", 0)
    curves_r = stats.get("curve_count_right", 0)

    lean_line = f"🏍️ Schräglage: {lean_l:.1f}° L / {lean_r:.1f}° R"
    if curves_tot > 0:
        lean_line += f" · 🔄 {curves_tot} Kurven ({curves_l} L / {curves_r} R)"
    lines.append(lean_line)

    # Speeds & Dynamics & RPM
    v_max = stats.get("speed_max_kmh", 0.0)
    v_avg = stats.get("speed_avg_kmh", 0.0)
    accel_g = stats.get("max_accel_g")
    decel_g = stats.get("max_decel_g")
    rpm_max = stats.get("rpm_max")

    dyn_parts = []
    if v_max > 0:
        dyn_parts.append(f"⚡ Max: {v_max:.1f} km/h (Ø {v_avg:.1f} km/h)")
    if accel_g is not None and accel_g > 0:
        dyn_parts.append(f"Beschl.: +{accel_g:.2f}g")
    if decel_g is not None and decel_g > 0:
        dyn_parts.append(f"Bremsen: -{decel_g:.2f}g")
    if rpm_max is not None and rpm_max > 0:
        dyn_parts.append(f"RPM max: {rpm_max:,} U/min".replace(",", "."))

    if dyn_parts:
        lines.append(" · ".join(dyn_parts))

    return "\n".join(lines)


def parse_gpx_stats(content: bytes) -> Dict[str, Any]:
    """Extracts extended summary statistics from a GPX XML file.

    Extracts:
    - Distance, gross duration, net moving duration, pause time
    - Elevation min, max, cumulative gain (climbed), cumulative loss (descended)
    - Ambient temperature min, max, average
    - Speeds (max, average moving speed)
    - Dynamics: max forward acceleration (+g) and braking deceleration (-g)
    - Maximum lean angles separated by left and right
    - Turn / curve counter (left, right, total)
    - Maximum and average engine RPM (from CAN telemetry if present)
    - Battery voltage (min during tour, average)
    """
    stats: Dict[str, Any] = {
        "point_count": 0,
        "distance_km": 0.0,
        "duration_s": 0,
        "netto_duration_s": 0,
        "pause_duration_s": 0,
        "start_time": None,
        "end_time": None,
        "speed_max_kmh": 0.0,
        "speed_avg_kmh": 0.0,
        "elevation_min_m": None,
        "elevation_max_m": None,
        "elevation_gain_m": None,
        "elevation_loss_m": None,
        "temp_min_c": None,
        "temp_max_c": None,
        "temp_avg_c": None,
        "max_accel_g": None,
        "max_decel_g": None,
        "max_lean_deg": 0.0,
        "max_lean_left_deg": 0.0,
        "max_lean_right_deg": 0.0,
        "curve_count_left": 0,
        "curve_count_right": 0,
        "curve_count_total": 0,
        "rpm_max": None,
        "rpm_avg": None,
        "battery_v_min": None,
        "battery_v_avg": None,
        "summary_text": "",
    }

    try:
        root = ET.fromstring(content)
        parsed_points = []

        for elem in root.iter():
            if elem.tag.endswith("trkpt"):
                lat = float(elem.attrib.get("lat", 0.0))
                lon = float(elem.attrib.get("lon", 0.0))
                pt_time: Optional[datetime] = None
                ele: Optional[float] = None
                speed_kmh: Optional[float] = None
                lean_deg: Optional[float] = None  # signed: negative = left, positive = right
                temp_c: Optional[float] = None
                accel_g: Optional[float] = None
                rpm: Optional[int] = None
                battery_v: Optional[float] = None

                for child in elem:
                    tag_low = child.tag.lower()
                    if tag_low.endswith("time") and child.text:
                        try:
                            pt_time = datetime.fromisoformat(child.text.replace("Z", "+00:00"))
                        except Exception:
                            pass
                    elif tag_low.endswith("ele") and child.text:
                        try:
                            ele = float(child.text)
                        except Exception:
                            pass
                    elif tag_low.endswith("extensions"):
                        # Search within extensions recursively
                        for ext in child.iter():
                            ext_tag = ext.tag.lower()
                            txt = (ext.text or "").strip()
                            if not txt:
                                continue
                            try:
                                if "lean_angle" in ext_tag or "lean" in ext_tag:
                                    lean_deg = float(txt)
                                elif "speed_kmh" in ext_tag or ext_tag.endswith("speed"):
                                    speed_kmh = float(txt)
                                elif "temp" in ext_tag:
                                    temp_c = float(txt)
                                elif "accel" in ext_tag:
                                    accel_g = float(txt)
                                elif "rpm" in ext_tag:
                                    rpm = int(float(txt))
                                elif "battery" in ext_tag:
                                    battery_v = float(txt)
                            except Exception:
                                pass

                parsed_points.append({
                    "lat": lat,
                    "lon": lon,
                    "time": pt_time,
                    "ele": ele,
                    "speed_kmh": speed_kmh,
                    "lean": lean_deg,
                    "temp": temp_c,
                    "accel_g": accel_g,
                    "rpm": rpm,
                    "battery_v": battery_v
                })

        if not parsed_points:
            return stats

        stats["point_count"] = len(parsed_points)

        # 1. Distances & Speed calculation
        total_dist = 0.0
        speeds = []
        moving_seconds = 0
        elevations = []
        temps = []
        accels = []
        rpms = []
        batteries = []
        lean_left_vals = []
        lean_right_vals = []

        # State machine for curve counting
        # State: 0 = straight, -1 = in left turn, +1 = in right turn
        curve_state = 0
        curve_pts_count = 0
        curve_l_count = 0
        curve_r_count = 0

        for i in range(len(parsed_points)):
            p = parsed_points[i]

            if p["ele"] is not None:
                elevations.append(p["ele"])
            if p["temp"] is not None:
                temps.append(p["temp"])
            if p["accel_g"] is not None:
                accels.append(p["accel_g"])
            if p["rpm"] is not None:
                rpms.append(p["rpm"])
            if p["battery_v"] is not None:
                batteries.append(p["battery_v"])

            # Lean angles
            if p["lean"] is not None:
                l_val = p["lean"]
                if l_val < 0:
                    lean_left_vals.append(abs(l_val))
                elif l_val > 0:
                    lean_right_vals.append(l_val)
                else:
                    lean_left_vals.append(0.0)
                    lean_right_vals.append(0.0)

                # Curve counter detector:
                # Turn threshold: |lean| >= 12.0 degrees
                # Straight threshold: |lean| < 7.0 degrees
                abs_lean = abs(l_val)
                if abs_lean >= 12.0:
                    dir_now = -1 if l_val < 0 else 1
                    if curve_state == dir_now:
                        curve_pts_count += 1
                    else:
                        # Direction switch
                        curve_state = dir_now
                        curve_pts_count = 1
                elif abs_lean < 7.0:
                    if curve_state != 0:
                        # Exited turn: require at least 2 consecutive points to count as true curve
                        if curve_pts_count >= 2:
                            if curve_state == -1:
                                curve_l_count += 1
                            elif curve_state == 1:
                                curve_r_count += 1
                        curve_state = 0
                        curve_pts_count = 0

            # Delta calculations between consecutive points
            if i > 0:
                p_prev = parsed_points[i - 1]
                if p["lat"] != 0.0 and p["lon"] != 0.0 and p_prev["lat"] != 0.0 and p_prev["lon"] != 0.0:
                    step_dist = haversine_distance(p_prev["lat"], p_prev["lon"], p["lat"], p["lon"])
                    total_dist += step_dist

                    # Net moving time & speed
                    dt_s = 0.0
                    if p["time"] and p_prev["time"]:
                        dt_s = max(0.0, (p["time"] - p_prev["time"]).total_seconds())

                    # Use logged speed if available, otherwise compute from distance / time
                    pt_spd = p.get("speed_kmh")
                    if pt_spd is None and dt_s > 0:
                        pt_spd = (step_dist / (dt_s / 3600.0))

                    if pt_spd is not None and pt_spd > 0:
                        speeds.append(pt_spd)
                        if pt_spd >= 3.0 and dt_s > 0:
                            moving_seconds += int(dt_s)

        # Flush any active curve that finished at the end of the track
        if curve_state != 0 and curve_pts_count >= 2:
            if curve_state == -1:
                curve_l_count += 1
            elif curve_state == 1:
                curve_r_count += 1

        stats["distance_km"] = round(total_dist, 2)

        # 2. Timing
        times = [p["time"] for p in parsed_points if p["time"] is not None]
        if times:
            t_start = min(times)
            t_end = max(times)
            stats["start_time"] = t_start.isoformat()
            stats["end_time"] = t_end.isoformat()
            total_duration = int((t_end - t_start).total_seconds())
            stats["duration_s"] = total_duration
            stats["netto_duration_s"] = min(moving_seconds if moving_seconds > 0 else total_duration, total_duration)
            stats["pause_duration_s"] = max(0, total_duration - stats["netto_duration_s"])

        # 3. Speeds
        if speeds:
            stats["speed_max_kmh"] = round(max(speeds), 1)
            # Net average speed = total distance / net moving hours
            net_h = stats["netto_duration_s"] / 3600.0
            if net_h > 0:
                stats["speed_avg_kmh"] = round(stats["distance_km"] / net_h, 1)
            else:
                stats["speed_avg_kmh"] = round(sum(speeds) / len(speeds), 1)

        # 4. Elevation & Cumulative Gain/Loss (with 1.0 m noise threshold filter)
        if elevations:
            stats["elevation_min_m"] = round(min(elevations), 1)
            stats["elevation_max_m"] = round(max(elevations), 1)

            gain = 0.0
            loss = 0.0
            for i in range(1, len(elevations)):
                diff = elevations[i] - elevations[i - 1]
                if diff > 0.8:
                    gain += diff
                elif diff < -0.8:
                    loss += abs(diff)

            stats["elevation_gain_m"] = round(gain, 1)
            stats["elevation_loss_m"] = round(loss, 1)

        # 5. Ambient Temperature
        if temps:
            stats["temp_min_c"] = round(min(temps), 1)
            stats["temp_max_c"] = round(max(temps), 1)
            stats["temp_avg_c"] = round(sum(temps) / len(temps), 1)

        # 6. Accelerations (g-forces)
        if accels:
            pos_accels = [a for a in accels if a > 0]
            neg_accels = [abs(a) for a in accels if a < 0]
            if pos_accels:
                stats["max_accel_g"] = round(max(pos_accels), 2)
            if neg_accels:
                stats["max_decel_g"] = round(max(neg_accels), 2)

        # 7. Lean Angles & Curves
        max_l = max(lean_left_vals, default=0.0)
        max_r = max(lean_right_vals, default=0.0)
        stats["max_lean_left_deg"] = round(max_l, 1)
        stats["max_lean_right_deg"] = round(max_r, 1)
        stats["max_lean_deg"] = round(max(max_l, max_r), 1)

        stats["curve_count_left"] = curve_l_count
        stats["curve_count_right"] = curve_r_count
        stats["curve_count_total"] = curve_l_count + curve_r_count

        # 8. Engine RPM
        if rpms:
            stats["rpm_max"] = max(rpms)
            stats["rpm_avg"] = int(sum(rpms) / len(rpms))

        # 9. Battery Voltage
        if batteries:
            stats["battery_v_min"] = round(min(batteries), 1)
            stats["battery_v_avg"] = round(sum(batteries) / len(batteries), 1)

        # 10. Human Summary String
        stats["summary_text"] = build_human_summary(stats, "Tour")

    except Exception as e:
        logger.warning(f"Could not parse GPX track statistics: {e}")

    return stats


async def dispatch_upload_event(filename: str, file_info: Dict[str, Any], content: bytes):
    """Dispatches upload event to MQTT and/or Webhook if configured."""
    stats = parse_gpx_stats(content)
    stats["summary_text"] = build_human_summary(stats, filename)

    payload = {
        "event": "track_uploaded",
        "filename": filename,
        "size_bytes": len(content),
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "gdrive_file_id": file_info.get("id"),
        "gdrive_link": file_info.get("webViewLink"),
        "summary": stats["summary_text"],
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

            # Publish full JSON telemetry event
            result = client.publish(settings.MQTT_TOPIC, json_payload, qos=1)
            result.wait_for_publish(timeout=3.0)

            # Also publish human-readable summary string to /summary subtopic for direct notifications
            summary_topic = f"{settings.MQTT_TOPIC.rstrip('/')}/summary"
            client.publish(summary_topic, stats["summary_text"], qos=1)

            client.disconnect()
            logger.info(f"Published upload notification to MQTT '{settings.MQTT_TOPIC}' & '{summary_topic}' on {broker}:{settings.MQTT_PORT}")
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

