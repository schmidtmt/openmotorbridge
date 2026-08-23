# 12 - GNSS Multi-Constellation, Automotive Dead Reckoning (ADR) & Map-Matching

The OMB-TourLog subsystem combines high-precision satellite navigation (u-blox MAX-M10S) with inertial sensor fusion (Automotive Dead Reckoning - ADR) and CAN-bus wheel speeds to record seamless tracks with full vehicle dynamics, even in tunnels, mountain canyons, and heavy foliage.

---

## 1. Architecture & Sensor Fusion (Automotive Dead Reckoning - ADR)

```
[ u-blox GNSS Engine (M10S 10 Hz) ] ──(UART 460.8k)──┐
[ CAN-Bus Wheel Speed / Velocity ] ──(10-20 Hz)──────┼─► [ 15-State Extended Kalman Filter ] ──► [ MicroSD: tour.gpx ]
[ Bosch BMI270 Gyro / Accel (I2C) ] ─(50-100 Hz)─────┘        (Dead Reckoning Engine)            (With Lean Angle & G-Force)
```

### 1.1 Seamless Tunnel Navigation (Inertial Navigation)
When GPS reception is lost in tunnels, dense forests, or alpine valleys, the system switches instantly to dead reckoning:
* CAN-bus wheel speed delivers precise distance travelled ($\Delta s = v \cdot \Delta t$).
* The gyroscope on the BMI270 IMU continuously integrates heading, banking, and elevation changes.
* Track recording continues smoothly without freezing or erratic jumping.

### 1.2 Multipath Jump Rejection (Canyon Filtering)
GPS outlier jumps (e.g. 40-meter multipath reflections off vertical cliff faces) are rejected by the Kalman filter: The IMU confirms that no corresponding lateral acceleration occurred, locking the track firmly to the true road trajectory.

### 1.3 MotoGP-Style Telemetry & Lean Angle Logging
Every recorded waypoint in the GPX dataset includes high-precision vehicle dynamics:
- Cornering lean angle left/right (°): $\text{Lean\_Angle} = \arctan\left(\frac{v \cdot \dot{\psi}}{g}\right)$
- Longitudinal and lateral G-forces (braking and acceleration dynamics)
- Vehicle board voltage and UPS status

---

## 2. Track Lifecycle & Intelligent Segmentation
- **Auto-Start:** Automatically starts a new tour file (`YYYY-MM-DD_HH-MM-SS.gpx`) once ignition is on and the motorcycle moves at $> 5\,\text{km/h}$ for $> 10\,\text{s}$.
- **Segment Split (`<trkseg>`):** Traffic lights or fuel stops under 15 minutes open a new track segment without closing the active tour file.
- **Auto-Finalize:** After 15 minutes of standstill or 60 seconds after ignition OFF, the GPX file is finalized and queued for WebDAV upload.

---

## 3. GPX 2.0 Telemetry & 1-PPS Video Sync
- **1-PPS Hardware Sync:** The MAX-M10S outputs a precise 1-Hz time pulse on `PIN_GNSS_PPS` (GPIO 21) with jitter $< 1\,\mu\text{s}$ (RMS $< 15\,\text{ns}$).
- **Video Markers:** Shutter events from the BLE handlebar remote are timestamped to synchronize action camera footage (GoPro/Insta360/DJI) frame-accurately with telemetry:

```xml
<trkpt lat="47.3769" lon="8.5417">
  <ele>408.2</ele>
  <time>2026-08-23T09:15:00.100Z</time>
  <extensions>
    <omb:telemetry>
      <omb:lean_angle>44.2</omb:lean_angle>
      <omb:speed_kmh>84.6</omb:speed_kmh>
      <omb:accel_g_lon>-0.72</omb:accel_g_lon>
      <omb:battery_v>12.6</omb:battery_v>
      <omb:satellites>18</omb:satellites>
    </omb:telemetry>
  </extensions>
</trkpt>
```

---

## 4. Action Cam & 360-Degree Camera Control via Handlebar Remote

OpenMotorBridge enables direct wireless control of action cameras via the BLE handlebar remote, embedding real-time GPS and lean angle telemetry directly into video metadata.

### 4.1 Handlebar Remote Button Mapping
* **Short Press:** Inserts an action highlight marker (`<omb:action_event>`) into the active GPX track (for automated best-of highlight editing).
* **Double Press:** Starts / stops video recording on paired action cameras (recording toggle).
* **Long Press (> 1.5 s):** Captures a high-resolution photo snapshot.
* **Apex Auto-Trigger:** Automatically tags a video highlight or snapshot when cornering lean angle exceeds $> 45^\circ$.

### 4.2 Supported Camera Protocols (BLE Integration)
1. **GoPro (Hero 9/10/11/12/13, Max):**
   * Controlled via the official **Open GoPro BLE API** (GATT Service `0xFEA6`, Shutter Start/Stop, Mode Change).
2. **Insta360 (X3 / X4 / Ace Pro / ONE RS 360):**
   * **Insta360 GPS Smart Remote Emulation:** ESP32-S3 emulates the official Insta360 GPS remote over BLE.
   * Telemetry (10 Hz GPS position, speed, heading, altitude) is streamed live to the camera $\rightarrow$ the camera embeds telemetry **natively into the GPMF/INSV video container**, allowing the Insta360 app to render speedometers and lean angle gauges without manual alignment!
3. **DJI (Osmo Action 3 / 4 / 5 Pro):**
   * DJI BLE Remote Protocol for record start/stop and GPS tagging.
4. **Hardware Camera Power:**
   * Switched output `RESERVE_GPIO_B` (HD26 Pin 26) controls an external 5V USB power gate to power/charge cameras automatically on ignition ON/OFF.

### 4.3 Telemetry Overlay & Post-Processing Pipeline
* **Drift-Free Synchronization:** By referencing the 1-PPS GPS clock with the camera timecode, lean angle overlays remain frame-accurate ($< 15\,\text{ms}$) even over multi-hour rides.
* **Universal Telemetry Export:** Exports GPX datasets formatted for **Telemetry Overlay, Garmin VIRB Edit, Dashware**, or automated ffmpeg rendering scripts.

---

## 5. Map-Matching & Universal GPX Export (Web-App Pipeline)

```
[ MicroSD: tour_raw.gpx ] ──(BLE Download)──► [ Web Dashboard / Smartphone ]
                                                      │
                                                      ▼
                                       [ Map-Matching Engine (OSRM / Valhalla) ]
                                                      │
                         ┌────────────────────────────┴────────────────────────────┐
                         ▼                                                         ▼
           [ Clean Navigation Route (.gpx) ]                          [ Pure Visual Track (.gpx) ]
           (20-50 Strategic Shaping Points for                         (1:1 Smoothed Geometry for
            Garmin, Kurviger, Calimoto, TomTom)                        Google Maps, Komoot, Relive)
```

1. **Automated Road-Snapping:**
   * The web app utilizes routing engines (OSRM or Valhalla) to snap raw coordinates onto OpenStreetMap road centerlines, eliminating GPS noise and parking lot maneuvers.
2. **Export for Motorcycle Navis (Shaping Points):**
   * The app exports a clean, routing-ready `.gpx` file containing strategic shaping points.
   * Can be imported directly into **Garmin Tread/Zūmo, BMW ConnectedRide, Kurviger, Calimoto, or TomTom** without unwanted recalculation by the device.
