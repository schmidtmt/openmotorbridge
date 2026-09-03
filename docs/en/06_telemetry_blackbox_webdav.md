# 06 - Telemetry Blackbox, SDIO Ringbuffer & WebDAV Sync

This document specifies the storage and telemetry subsystem of OpenMotorBridge v8.0: the 4-bit high-speed SDIO bus, the GDPR/BGH-compliant rolling ringbuffer with cryptographic signatures, the automated TLS-secured WebDAV cloud upload, and the **low-power USB Mass Storage Class (MSC) mode** for direct PC access.

---

## 1. High-Speed SDIO Storage Interface (4-Bit @ 40 MHz)

* **Interface:** Native 4-bit SDIO bus operating at 40 MHz connected to ESP32-S3 (GPIOs 40–45).
* **Throughput:** Continuous write speeds $> 12\,\text{MB/s}$ (enabling uninterrupted 10 Hz GPX, IMU, and audio telemetry logging).
* **Filesystem:** FAT32 with dynamic sector buffering (32 kB cluster size).
* **Failsafe:** The integrated BQ24075 UPS buffer guarantees clean unmounting and closing of FAT file allocation tables during abrupt power losses.

---

## 2. Sensor Fusion & Automotive Dead Reckoning (ADR Engine)

The telemetry subsystem fuses data from the multi-constellation GNSS receiver (**u-blox MAX-M10S** in Rear Pod 3), the 6-axis IMU (**Bosch BMI270**), and optional motorcycle wheel speed inputs (via CAN-bus or ABS sensor pulse line) in a **15-State Error-State Extended Kalman Filter (ES-EKF)**:

```
[ u-blox Multi-GNSS (M10S 10 Hz) ] ──(UART 460.8k)──┐
[ CAN-Bus Wheel Speed / Velocity ] ───(10-20 Hz)─────┼─► [ 15-State Extended Kalman Filter ] ──► [ MicroSD: tour.gpx ]
[ Bosch BMI270 Gyro / Accel (I2C) ] ──(50-100 Hz)────┘        (Dead Reckoning Engine)            (With Lean Angle & G-Force)
```

### 2.1 Continuous Tunnel and Mountain Gorge Tracking
* When satellite signals are lost in tunnels, underpasses, dense tree canopy, or narrow mountain ravines:
  * Wheel speed provides precise traveled distance increments ($\Delta s = v \cdot \Delta t$).
  * The BMI270 gyro continuously integrates pitch, roll, and yaw turns.
  * The recorded trajectory advances smoothly on the road centerline without route freezing, clipping, or jumping.

### 2.2 Rejection of Multipath Outliers (Alpine Pass Cliff Filtering)
GNSS multipath reflections (e.g. $40\,\text{m}$ lateral position spikes caused by satellite signals bouncing off vertical rock faces) are automatically detected and discarded: The IMU confirms to the EKF that no matching lateral acceleration occurred physically, keeping the track locked to the actual road.

---

## 3. MotoGP-Style Telemetry & GPX 2.0 XML Specification

Every trackpoint recorded at $10\,\text{Hz}$ is enriched with high-rate motorcycle dynamics:
* **Lean Angle Left/Right (°):** $\text{Lean\_Angle} = \arctan\left(\frac{v \cdot \dot{\psi}}{g}\right)$
* **Longitudinal & Lateral G-Forces:** Calibrated braking, cornering, and acceleration forces.
* **Vehicle Battery Voltage:** Monitors alternator health and stator output under load.
* **1-PPS Hardware Timecode:** Sub-15ns jitter reference for frame-accurate action camera video overlays.

```xml
<trkpt lat="47.3769" lon="8.5417">
  <ele>408.2</ele>
  <time>2026-08-23T09:15:00.100Z</time>
  <extensions>
    <omb:telemetry>
      <omb:lean_angle>44.2</omb:lean_angle>
      <omb:speed_kmh>84.6</omb:speed_kmh>
      <omb:accel_g_lon>-0.72</omb:accel_g_lon>
      <omb:accel_g_lat>0.98</omb:accel_g_lat>
      <omb:battery_v>12.6</omb:battery_v>
      <omb:satellites>18</omb:satellites>
      <omb:hdop>0.8</omb:hdop>
    </omb:telemetry>
  </extensions>
</trkpt>
```

---

## 4. Track Lifecycle & Intelligent Segmentation

* **Auto-Start:** Creates a new ride file (`YYYY-MM-DD_HH-MM-SS.gpx`) as soon as ignition (KL15) is ON and the motorcycle has moved for $> 10\,\text{s}$ at speed $> 5\,\text{km/h}$.
* **Segment Split (`<trkseg>`):** During traffic lights or brief fuel stops under 15 minutes, the file remains open while a new `<trkseg>` segment is appended, eliminating wandering GPS clusters while stationary.
* **Auto-Finalization:** After 15 minutes of continuous standstill or 60 seconds after ignition OFF, the GPX XML structure cleanly closes with `</gpx>` and queues for WebDAV synchronization.

---

## 5. Rolling Ringbuffer & Court Admissibility (BGH VI ZR 233/17 & GDPR)

To comply with European data privacy regulations (GDPR Art. 5 & 25) and German Federal Court of Justice rulings (BGH VI ZR 233/17) regarding unprompted surveillance in road traffic:

```
┌─────────────────────────────────────────────────────────────┐
│          GDPR-COMPLIANT ROLLING RINGBUFFER ARCHITECTURE      │
├─────────────────────────────────────────────────────────────┤
│ • Continuous rolling buffer directory: /tracks/             │
│ • Auto-Purge Threshold: Free space < 200 MB                 │
│ • Oldest unprotected track segments overwritten in 50MB blk │
│ • Manual highlight protection via handlebar switch (*.fav)  │
│ • Crash sensor trigger: Impact > 4G locks last 15 min.      │
└─────────────────────────────────────────────────────────────┘
```

1. **Rolling Ringbuffer:** Normal riding data is recorded in 15-minute segments and cyclically overwritten.
2. **Crash Freeze:** If the Bosch BMI270 IMU detects a severe deceleration impact ($> 4{,}0\,\text{g}$) or an engine cutoff accompanied by high tilt, the last 15 minutes plus subsequent rundown data are permanently write-protected.
3. **Cryptographic Integrity (ECDSA SHA-256):** Every recorded segment is signed using a hardware key stored in the ESP32 eFuse/ATECC608A to provide tamper-proof evidence for accident reconstruction.

---

## 6. Map-Matching & Universal GPX Export (Web-App Pipeline)

```
[ MicroSD: tour_raw.gpx ] ──(BLE / WebDAV)──► [ Web Dashboard / Smartphone ]
                                                      │
                                                      ▼
                                       [ Map-Matching Engine (OSRM / Valhalla) ]
                                                      │
                         ┌────────────────────────────┴────────────────────────────┐
                         ▼                                                         ▼
           [ Clean Navigation Route (.gpx) ]                          [ Visual Track Overlay (.gpx) ]
           (20-50 placed Shaping Points for                            (1:1 smoothed line for
            Garmin, Kurviger, Calimoto, TomTom)                        Google Maps, Komoot, Relive)
```

1. **Automated Road Snapping:**
   * The Web-App leverages routing engines (OSRM or Valhalla) to snap raw GPS coordinates mathematically to the OpenStreetMap road network, eliminating parking lot wandering and GPS drift.
2. **Motorcycle GPS Export (Shaping Points):**
   * The app generates clean, routing-ready `.gpx` files with strategically placed shaping points.
   * Directly importable into **Garmin Tread/Zūmo, BMW ConnectedRide, Kurviger, Calimoto, or TomTom** without unwanted recalculation.

---

## 7. Automatic WebDAV / Nextcloud Upload in Home Wi-Fi

```
MOTORCYCLE ENTERS GARAGE (IGNITION OFF)
┌─────────────────────────────────────────────────────────────┐
│ 1. KL15 drops -> UPS rundown timer initiates (Graceful Run) │
│ 2. ESP32-S3 scans for configured Home Wi-Fi SSIDs for 60 s  │
│ 3. Wi-Fi connects via WPA2/WPA3 Personal / Enterprise       │
│ 4. TLS 1.3 Client connects to Nextcloud / ownCloud / NAS    │
│ 5. Automated upload of new *.gpx tracks and logs (1.8 MB/s) │
│ 6. Sync complete confirmation -> Filesystem unmount -> Sleep│
└─────────────────────────────────────────────────────────────┘
```

---

## 8. Minimal USB Mass Storage Class (MSC) Mode

Connecting the Central Box to a PC, Mac, or tablet via USB-C while the motorcycle ignition is OFF activates the **Minimal USB MSC Mode**:

```
┌─────────────────────────────────────────────────────────────┐
│             MINIMAL USB MASS STORAGE CLASS MODE             │
├─────────────────────────────────────────────────────────────┤
│ • VBUS detection (5V on native USB-C port)                  │
│ • Main power relays & audio DSP (ES8388) remain UNPOWERED   │
│ • Wireless modules (LoRa, Mesh, Bluetooth) remain DISABLED  │
│ • Current draw from USB port: < 80 mA (Zero battery drain)  │
│ • MicroSD card mounts instantly as standard flash drive     │
└─────────────────────────────────────────────────────────────┘
```

* **No Tools Required:** The MicroSD card stays safely sealed inside the IP67 enclosure. The computer immediately detects the drive `OPENMOTOR`.
* **Instant Access:** Rides can be opened directly in Google Earth, BaseCamp, GPXSee, or Kurviger.
