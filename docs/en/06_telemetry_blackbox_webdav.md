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

The telemetry subsystem fuses data from the multi-constellation GNSS receiver (**u-blox SAM-M10Q** with integrated $15 \times 15\,\text{mm}$ patch antenna on the Front Node via `J12` Qwiic), the 6-axis IMU (**Bosch BMI270**) on the Central Box, and optional motorcycle wheel speed inputs (via CAN-bus or ABS sensor pulse line) in a **15-State Error-State Extended Kalman Filter (ES-EKF)**:

```
[ u-blox SAM-M10Q GNSS (10 Hz) ] ──(I2C 400k / UWB)──┐
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
* **Lean Angle Left/Right (°):** $\text{Lean\_Angle} = \arctan\left(\frac{v \cdot \dot{\psi}}{g}\right)$ (captured independently for left and right curves).
* **Longitudinal & Lateral G-Forces:** Calibrated acceleration ($+g$) and braking deceleration ($-g$) forces.
* **Ambient Temperature (°C):** High-precision ambient air temperature via the 2-tier architecture.
* **Engine RPM:** Direct $10\,\text{Hz}$ engine speed capture via vehicle CAN-bus broadcast.
* **Vehicle Battery Voltage:** Monitors alternator health and stator output under load.
* **1-PPS Hardware Timecode:** Sub-15ns jitter reference for frame-accurate action camera video overlays.
* **CAN Gear Position (`<omb:gear>`):** Active gear (0 = Neutral, 1..6) extracted from vehicle CAN-bus broadcast.
* **Intercom Link QoS (`<omb:comm_tier>`):** Active communication layer (`hd` = 2.4 GHz Opus HD-Voice, `lora` = 868 MHz Codec2 Fallback).

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
      <omb:temp>21.4</omb:temp>
      <omb:rpm>4850</omb:rpm>
      <omb:gear>4</omb:gear>
      <omb:comm_tier>hd</omb:comm_tier>
      <omb:battery_v>12.6</omb:battery_v>
      <omb:satellites>18</omb:satellites>
      <omb:hdop>0.8</omb:hdop>
    </omb:telemetry>
  </extensions>
</trkpt>
```

### 3.1 2-Tier Architecture for Ambient Temperature Sensing

To strictly avoid running cables through the steering stem to the wireless Front-Node while eliminating false readings from engine heat dissipation, OpenMotorBridge implements a 2-tier sensing design:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              2-TIER AMBIENT TEMPERATURE SENSING ARCHITECTURE                │
├─────────────────────────────────────────────────────────────────────────────┤
│ TIER 1: CAN-Bus Broadcast (BMW R1250/R1300 GS, Harley Pan America / HD-LAN) │
│ • Reads OEM ambient/intake air temperature from CAN frames (ID 0x2D0 etc.)  │
│ • 0 extra wires, 0 hardware cost, factory calibrated                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ TIER 2: Front Node Cold-Air Scoop Sensing (Universal / CVO ST / Non-CAN)    │
│ • Dedicated sensor (TI TMP117 ±0.1°C & OPT3001 light sensor on J12 Qwiic) on PCBA 05 │
│ • Installation: Ram-air intake duct inside fairing / headlight scoop         │
│ • Thermal Isolation: Eliminates false readings from engine heat trapped     │
│   around cylinder heads or radiator exhaust                                  │
│ • Wireless Steering Head: Telemetry streams over UWB (< 0.4 ms)              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Barometric Altitude Fusion (15-State Kalman Filter)

In addition to GNSS 3D height, a Bosch BMP390 / BMP581 barometric pressure sensor on the Central Box (PCBA 01) measures relative vertical displacement down to $\pm 10\,\text{cm}$. The 15-state Error-State Extended Kalman Filter continuously cross-references barometric delta with u-blox SAM-M10Q 3D GNSS fixes during steady cruise to auto-calibrate QNH reference pressure without any manual zeroing required by the rider.

### 3.3 Shift Counter State Machine & Radio Link QoS Fallback Tracking

1. **Shift Counter State Machine:**
   * Parsed from `<omb:gear>` CAN telemetry, detecting upshifts (`shifts_up`) and downshifts (`shifts_down`).
   * A debounce filter ignores transient neutral blips (`1 -> N -> 2` registers as 1 upshift) to prevent artificial shift inflating.
   * `shifts_per_km` provides an objective metric for aggressive twisty shifting vs. calm highway cruising.

2. **Intercom QoS & LoRa Fallback Tracking:**
   * Every fallback from 2.4 GHz Opus HD-Voice to 868 MHz Codec2 LoRa is tagged (`<omb:comm_tier>lora</omb:comm_tier>`).
   * Computes HD-Voice availability (`comm_hd_pct`), total fallback count (`comm_lora_fallback_count`), and cumulative fallback duration (`comm_lora_fallback_duration_s`).

### 3.4 Direct Drive & Audio Mode Coupling (Zero-Overkill Scorecards)

Rather than introducing cluttered configuration menus, OpenMotorBridge couples telemetry reporting directly to the 3 active modes from `🎛️ Audio-Routing & Operating Modes`:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   TELEMETRY SCORECARDS BY OPERATING MODE                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ MODE 1: Single Rider Mode 🏍️ (Sport & Dynamic Telemetry)                    │
│ • Lean angles L/R, corner density (turns/km), % time at lean (≥20°)          │
│ • Shift Counter (Total, Up/Down, Shifts/km), G-Forces, Panic Brakes, Max RPM│
├─────────────────────────────────────────────────────────────────────────────┤
│ MODE 0: Standard Mesh Bridge 👥 (Group & Intercom QoS)                      │
│ • Radio availability (% HD-Voice), LoRa fallback count/duration, Drops       │
│ • Formation pace (Ø km/h), total turns, electrical bus stability            │
├─────────────────────────────────────────────────────────────────────────────┤
│ MODE 2: Cruise Mode 🛣️ (Cruising & Touring Comfort)                         │
│ • Net/pause times, elevation gain/loss, ambient temperature range            │
│ • Braking smoothness (panic-free braking), cruising pace, shift index        │
└─────────────────────────────────────────────────────────────────────────────┘
```

The PWA Tour Inspector features 3 instantaneous pills (`[ 🏍️ Sportlich ]`, `[ 👥 Gruppe / Funk ]`, `[ 🛣️ Cruising ]`) to switch scorecard perspectives on the fly.

### 3.5 GPS Co-Existence & RF De-Sensing Protection (+22 dBm LoRa Bursts)

Operating +22 dBm (160 mW) LoRa transmissions at 868 MHz near a sensitive GNSS receiver requires deliberate RF isolation. OpenMotorBridge resolves this through a robust 3-tier protection architecture:
1. **Maximum Physical Separation ($> 1.2\,\text{m}$ Distance):** The Semtech SX1262 LoRa transceiver sits on Central Box PCBA 01 under the seat (with Taoglas FXP895 flex antenna in the lid pocket), while the SAM-M10Q GNSS receiver sits at the very front of the fairing/windshield. Free-space path loss between both locations exceeds $> 45\,\text{dB}$.
2. **Integrated SAW Bandpass Filtering:** The SAM-M10Q module integrates a steep surface acoustic wave (SAW) filter ahead of its internal LNA, providing $> 50\,\text{dB}$ attenuation in the 868 MHz band.
3. **Inertial EKF Bridging:** The 15-state EKF Dead Reckoning engine uses 50 Hz IMU inertial data to seamlessly bridge any transient SNR dip during packet bursts.

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

* **100% Automated:** The rider neither needs to unlock a smartphone nor physically extract microSD cards. The day's rides are already filed in the cloud upon entering the house.

### 7.1 Cloud Storage Architecture: Nextcloud vs. Lightweight Google Drive WebDAV Proxy (`omb.f0o.bar`)

While power users with a private Nextcloud or Synology NAS point directly to their native WebDAV URL, riders without home servers can deploy the lightweight **OpenMotorBridge Google Drive WebDAV Proxy**:

1. **Advantages of a Cloud Service Architecture:**
   * **100% Platform Independent:** Operates identically for iPhone riders (zero $99/year Apple Developer fee required) and Android users alike.
   * **Fully Autonomous & Phone-Free:** The motorcycle syncs independently upon reconnecting to home Wi-Fi (or on the road via the mobile proxy) without requiring the rider's phone to be awake.
2. **Why Avoid Heavy Rclone Binaries?**
   * Rclone ships a 100MB+ binary with dozens of unnecessary cloud backends and heavy state engines.
   * OpenMotorBridge's WebDAV requirements are strictly minimal: an HTTP `PUT /tracks/<filename>.gpx` (typical file size 200 KB to 3 MB) with HTTP Basic Auth.
3. **Microservice Architecture (`omb-gdrive-bridge` on `omb.f0o.bar`):**
   * A lean Python/FastAPI container (< 30 MB RAM) ingests the WebDAV `PUT` stream.
   * Using a stored Google OAuth2 refresh token (Google Drive API v3), the GPX file streams directly into the target folder `omb/tracks/` in Google Drive.
   * Returns HTTP `201 Created` upon completion.
   * **Smart Home Hook & Rich Ride Summary Statistics:** Immediately following upload, publishes structured telemetry events via MQTT (`omb/tracks/uploaded` as JSON and `omb/tracks/summary` as formatted text) and/or Webhook:
     * **Times & Net Moving Time:** Gross departure and arrival timestamps, true net moving time (automatic standstill filter $< 3\,\text{km/h}$), and total pause duration.
     * **Elevation & Cumulative Climb:** Min/Max altitude above sea level and cumulative elevation gain ($\sum \Delta h_{\text{up}}$) and descent ($\sum \Delta h_{\text{down}}$).
     * **Ambient Temperature:** Min, max, and tour average ambient temperature ($T_{\min}, T_{\max}, T_{\text{avg}}$).
     * **Speed Metrics:** Maximum speed ($v_{\max}$) and true net average moving speed ($\bar{v}_{\text{net}}$).
     * **Vehicle Dynamics (G-Forces):** Maximum forward acceleration ($+g$) and maximum braking deceleration ($-g$).
     * **Lean Angle Analysis:** Maximum lean angle tracked independently for left and right turns.
     * **Corner Counter:** Hysteresis state-machine detecting left, right, and total corner counts.
     * **Engine Speed (CAN):** Maximum and average engine RPM.
     * **Electrical Health:** Minimum and average vehicle battery voltage during the tour.
4. **Self-Hosted & Zero-Trust Privacy (Zero Third-Party Drive Access):**
   * **Full Data Sovereignty:** OpenMotorBridge does not operate a centralized cloud harvesting service. The `omb-gdrive-bridge` microservice is published as an open-source container template (`Dockerfile` / `podman-compose.yml`).
   * **Private Google Credentials:** Each rider runs the container on their personal infrastructure (e.g. home server, Synology Docker, Raspberry Pi, Unraid, or private VPS) and configures their own Google Cloud API credentials.
   * **Zero Liability & Zero GDPR Risk:** No user ever grants the OpenMotorBridge maintainers access or tokens to their Google Drive. GPS routes, lean angle profiles, and driving logs remain strictly under personal control.
   * **Source Code & Setup Walkthrough:** Production source code, Dockerfile, and the interactive token generator CLI are located in [`apps/gdrive_webdav_bridge/`](../../apps/gdrive_webdav_bridge/README.md).

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
