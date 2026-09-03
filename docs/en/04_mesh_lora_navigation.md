# 04 - Mesh Network, LoRa & GNSS Navigation

This document specifies the communication and positioning architecture of OpenMotorBridge v8.0: the OpenMotorMesh (OMM) protocol with **Dynamic Leader Election (DLE)**, large group convoy partitioning, the **868 MHz LoRa Long-Range fallback**, and the **10 Hz Multi-GNSS engine (u-blox NEO-M9N)** with dead-reckoning and video telemetry synchronization.

---

## 1. Dual-PHY Hybrid Mesh Architecture (2.4 GHz HiFi & 868 MHz LoRa)

To balance wide audio bandwidth with long-range offroad resilience, OpenMotorBridge combines two complementary radio layers:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   HYBRID DUAL-PHY RADIO ARCHITECTURE                   │
├───────────────────────────────────┬────────────────────────────────────┤
│ LAYER 1: 2.4 GHz HiFi Audio Mesh  │ LAYER 2: 868 MHz Sub-GHz LoRa Mesh │
├───────────────────────────────────┼────────────────────────────────────┤
│ • Frequency: 2.402 - 2.480 GHz    │ • Frequency: 868.1 - 869.5 MHz     │
│ • Modulation: DSSS / GFSK 2 Mbps  │ • Modulation: LoRa CSS (BW 125/250)│
│ • Codec: Opus 24k HD Full-Duplex  │ • Codec: Codec2 1200 bps PTT Voice │
│ • Range: Up to 1.2 km line-of-sight│ • Range: Up to 4.0 km non-LOS / Pass│
│ • Latency: < 15 ms (convoy-wide)  │ • Function: GPS Radar & Emergency  │
└───────────────────────────────────┴────────────────────────────────────┘
```

### 1.1 Triple Coaxial RF Bypass (Murata MM8030 RF Switch Sockets)
Rear Pod 3 integrates all three RF subsystems (2.4 GHz Mesh, 868 MHz LoRa, Multi-GNSS) and features automated **Murata MM8030-2610** coaxial switch sockets:
* **Internal Antenna Array (Standard):** Encased within the dielectric radome are an Inverted-F PCB antenna (IFA for 2.4 GHz), an 868 MHz helical spring coil, and a $25 \times 25\,\text{mm}$ ceramic GNSS patch.
* **External Bypass (Plug & Play):** When an external coaxial plug is inserted (e.g. $+5\,\text{dBi}$ whip antenna or active roof-mounted GNSS patch), the internal mechanical switch disconnects the internal radiator with $< 0{,}15\,\text{dB}$ insertion loss and $> 25\,\text{dB}$ isolation.
* **Zero Disassembly:** External high-gain antennas plug in directly without opening the hermetic IP67 casing.

---

## 2. Layer 2: 802.11s-Light Loop Prevention & Managed Forwarding

OpenMotorMesh implements routing and loop-prevention mechanisms adapted from IEEE 802.11s directly on Layer 2:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Mesh Control  |   Hop Limit   |     Mesh Sequence Number      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                     Originator Node MAC                       |
|                       (Bytes 0..3)                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Originator MAC (4..5)        |      Target Node MAC (0..1)   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Target MAC (2..5)                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Payload: 6LoWPAN / IPv6 Multicast / RTP / Opus Audio ...      |
```

* **Hop Limit (TTL):** Decremented at each relay hop ($T_{\text{max}} = 5$).
* **Sequence Cache:** Each node maintains a 64-entry sequence cache; duplicates are discarded immediately in hardware.

### 2.1 Layer-2 Frame Header C++ Struct & Duplicate Filter
```cpp
struct MeshHeader_t {
    uint8_t  meshFlags;     // Priority & Type Flags (Bit 0..2: Prio, Bit 3..7: Type)
    uint8_t  hopLimit;      // TTL decrement per hop (Loop prevention, Default = 5)
    uint16_t meshSeqNum;    // Monotonic transmission ID
    uint8_t  originMac[6];  // Originator node MAC (derived from DS2401 UID)
    uint8_t  targetMac[6];  // Multicast (ff:ff:...) or Unicast Node MAC
} __attribute__((packed));

void onRawPacketReceived(uint8_t* rawData, size_t len) {
    if (len < sizeof(MeshHeader_t)) return;
    
    MeshHeader_t* meshHdr = (MeshHeader_t*)rawData;
    uint8_t* payload = rawData + sizeof(MeshHeader_t);
    size_t payloadLen = len - sizeof(MeshHeader_t);

    // 1. Layer-2 Loop & Duplicate Filter
    if (meshHdr->hopLimit == 0) return;
    if (checkAndRegisterL2Duplicate(meshHdr->originMac, meshHdr->meshSeqNum)) {
        return; // Duplicate discarded -> Saves CPU and DMA overhead
    }

    // 2. Local Processing (Audio playout or radar decoding)
    processL3Payload(payload, payloadLen);

    // 3. Managed Forwarding: Relay transmission if node is elected master
    if (currentRideMode == MODE_RELAY_AR) {
        meshHdr->hopLimit--;
        broadcastForward(rawData, len);
    }
}
```

---

## 3. Layer 3 & 4: 6LoWPAN, IPv6 Multicast & Audio Streaming

* **Multicast Routing:** Voice payloads are transmitted via IPv6 Multicast to group addresses (e.g. `ff02::1`). A single packet reaches all convoy participants without unicast duplication.
* **Header Compression (6LoWPAN per RFC 6282):** Compresses the 40-byte IPv6 header down to 2 to 4 bytes for minimal RF airtime overhead.
* **Autonomous Addressing (SLAAC):** Each node derives its Link-Local address (`fe80::/64`) autonomously from the 64-bit DS2401 silicon UID.

---

## 4. Dynamic Leader Election (DLE) Algorithm

The mesh dynamically and autonomously elects the optimal gateway master (Cluster Head) within each RF cell:

$$\text{Score}_{\text{DLE}} = S_{\text{HW}} + S_{\text{PWR}} + S_{\text{GNSS}} + S_{\text{LORA}} + S_{\text{UPTIME}} + S_{\text{MIC}}$$

| Parameter | Condition | Points |
| :--- | :--- | :---: |
| **S_HW (Hardware Tier)** | Sena Apex (Mesh 3.0) OR Cardo Edge (DMC Gen2) docked | **+60 Pts** |
| | Sena Legacy / Cardo DMC Gen1 docked | +30 Pts |
| **S_PWR (Power Supply)** | Ignition Active (KL15 > 12.5 V via LM5164) | **+20 Pts** |
| | UPS Battery Buffer Mode (> 3.8 V) | +5 Pts |
| **S_GNSS (Position Lock)**| 3D Fix with PDOP < 1.5 & 1-PPS Lock | **+10 Pts** |
| **S_LORA (Link Quality)** | Average neighbor RSSI > -85 dBm | **+10 Pts** |
| **S_MIC (Acoustic Sensor)**| IP67 Front Ambient Mic active (`FEAT_ENV_MIC`) | **+5 Pts** |
| **S_UPTIME (Hysteresis Guard)**| Currently active leader (prevents thrashing) | **+15 Pts** |

### 4.1 Node Capability Vector & Smart Convoy Functions
Nodes announce their hardware feature set in periodic DLE beacon frames:

```cpp
enum OmmFeatureBits : uint8_t {
    FEAT_DUAL_MESH_BRIDGE  = (1 << 0), // Sena + Cardo active (+60 Pts)
    FEAT_LORA_HIGH_POWER   = (1 << 1), // SX1262 +22 dBm PA
    FEAT_GNSS_1PPS_LOCK    = (1 << 2), // Hardware timecode reference
    FEAT_CAN_TELEMETRY     = (1 << 3), // OBD2 / CAN-Bus active
    FEAT_ENV_MIC_ACTIVE    = (1 << 4), // Front Ambient Mic active (+5 Pts)
    FEAT_USV_BAT_BUFFER    = (1 << 5)  // UPS battery buffer capable
};
```

1. **🚨 Convoy Siren Early Warning:**
   * When the front mic of the lead motorcycle detects emergency sirens ($350\dots 1000\,\text{Hz}$ warble from an approaching emergency vehicle at an intersection), the node transmits an `ALERT_SIREN_APPROACHING` broadcast packet.
   * Following riders receive an acoustic warning beep in their helmet before the vehicle is directly audible to them.
2. **🎙️ Guide Pass-Through (Toll / Border Control Channel):**
   * At toll booths or checkpoints, the convoy leader can route their front ambient mic into the group mesh for 10 seconds via handlebar button, broadcasting instructions clearly to all group members.

### 4.2 Adaptive Tiered QoS (Bandwidth & Range Cascades)
To prevent sudden communication dropouts, OMM operates a 3-tier cascade:
1. **Tier 1 - Proximity (< 500 m, 2.4 GHz):** Full-Duplex HD Voice, A2DP Music Sharing, and Nav Ducking active. LoRa sends background pings (Duty Cycle $< 0{,}1\,\%$).
2. **Tier 2 - Edge Range (500 m - 1.2 km):** As Link Quality drops, Music Sharing pauses automatically to dedicate 100% of RF channel bandwidth to speech.
3. **Tier 3 - Extended / Severed (1 km - 15 km, 868 MHz LoRa):**
   * Music Sharing: OFF.
   * GPS Convoy Radar & Telemetry: 100% active on cockpit dashboard.
   * Voice: Automatic fallback to Codec2 (1200 bps narrow-band PTT radio).

### 4.3 Cluster Partitioning & Inter-Cluster Gateway Relay
When a convoy is divided by terrain or traffic lights, automatic cluster partitioning activates:

```mermaid
sequenceDiagram
    participant VG as Lead Group (Bikes 1-3)
    participant L1 as Leader 1 (Bike 1)
    participant L2 as Leader 2 (Bike 4)
    participant HG as Trailing Group (Bikes 4-6)

    Note over VG,HG: Unified Convoy (Leader 1 active on 2.4 GHz)
    Note over VG,HG: Group splits (e.g. traffic light turns red)
    HG->>HG: 2.4 GHz Beacon from Leader 1 lost -> DLE re-election
    HG->>L2: Bike 4 elected autonomous Leader 2
    Note over VG: Local 2.4 GHz Mesh active (HD Voice)
    Note over HG: Local 2.4 GHz Mesh active (HD Voice)
    HG->>L2: Bike 5 speaks in trailing group 2.4 GHz mesh
    L2->>L2: VAD Trigger: Voice active locally, cluster severed
    L2->>L1: Send Codec2 Audio Packet (300 B) via 868 MHz LoRa
    L1->>VG: Decompress & inject audio into Lead Group 2.4 GHz mesh
    Note over VG: Lead Group hears: "Stopped at red light!"
```

1. **Sub-Leader Election:** The trailing group detects lost sync beacons ($T_{\text{timeout}} > 500\,\text{ms}$) and instantly elects Bike 4 as local Leader 2.
2. **Local HD Audio Maintained:** Both clusters maintain local high-bandwidth 2.4 GHz intercom without interruption.
3. **LoRa Cross-Gateway Bridge:** When voice is spoken in either sub-group, the local leader compresses it to Codec2 (1200 bps) and beams it across the 868 MHz LoRa link to the remote leader for local re-injection.
4. **Cluster Fusion (Re-Merge):** When the trailing group closes distance ($< 400\,\text{m}$), Leader 2 detects Leader 1, yields master role, and closes the LoRa bridge seamlessly.

### 4.4 OpenMotorMesh Packet Formats & Binary Specification

#### Compact 16-Byte Group Radar Packet (`TYPE_RADAR = 0x03`)
```cpp
struct __attribute__((packed)) OmmRadarPacket_t {
    uint8_t  packet_type;       // 0x03 = TYPE_RADAR
    uint8_t  node_id_short;     // Lower 8-bit of DS2401 UID
    int32_t  latitude_1e7;      // Latitude * 10,000,000
    int32_t  longitude_1e7;     // Longitude * 10,000,000
    int16_t  altitude_m;        // Altitude AMSL (-500 .. +8000 m)
    uint8_t  speed_kmh;         // 0 .. 255 km/h
    uint8_t  heading_div2;      // Heading / 2 (0..179 corresponds to 0..358 deg)
    int8_t   lean_angle_deg;    // Lean angle (-60..+60 deg)
    uint8_t  status_flags;      // Bit 0: 1-PPS Lock, Bit 1: KL15, Bit 2..7: Batt%
};
```

#### Emergency & Siren Early Warning Packet (`TYPE_EMERGENCY = 0xFF`)
```cpp
struct __attribute__((packed)) OmmEmergencyAlert_t {
    uint8_t  packet_type;       // 0xFF = TYPE_EMERGENCY
    uint8_t  alert_subtype;     // 0x01: Siren warble, 0x02: Crash detection (eCall)
    uint64_t sender_uid;        // 64-bit silicon UID of originating motorcycle
    int32_t  event_lat_1e7;     // GPS coordinates of incident
    int32_t  event_lon_1e7;
    uint16_t alert_duration_ms; // Validity window (e.g. 10,000 ms)
    uint8_t  crc8_checksum;     // CRC-8/AUTOSAR checksum
};
```

---

## 5. Rear Pod 3 Transceiver Architecture & UART Protocol

Rear Pod 3 (`PCBA 04`) operates as the central RF gateway and positioning node, powered by a **Raspberry Pi RP2040** dual-core coprocessor:
* **Core 0 (`rear_nmea_task`):** Parses UBX/NMEA binary streams from the u-blox MAX-M10S Multi-GNSS at 10 Hz and performs dead-reckoning position extrapolation.
* **Core 1 (`rear_lora_task`):** Drives the Semtech SX1262 LoRa transceiver over high-speed SPI (@ 16 MHz), handling CSMA/CA channel access and packet buffering.

### 5.1 Protocol Specification (Rear Pod $\leftrightarrow$ Central Box)
Communication over the 460,800 Baud physical UART uses framed binary packets with CRC16-CCITT integrity checks:

```
┌──────┬──────┬──────┬──────┬─────────────────┬──────┬──────┐
│ SYNC │ TYPE │ LEN  │ SEQ  │ PAYLOAD (0..n)  │ CRC16-CCITT  │
│ 0xAA │ 0x55 │ 1 B  │ 1 B  │ Variable        │ 2 Bytes      │
└──────┴──────┴──────┴──────┴─────────────────┴──────┴──────┘
```

#### Message Types:
* **`0x01` - GNSS PVT Telemetry (10 Hz):** Pre-packed binary vector containing latitude, longitude, altitude, speed, heading, PDOP, and satellite lock status.
* **`0x02` - OMM 2.4 GHz Primary Audio Frame:** Opus 24k/12k frame from proximity mesh.
* **`0x03` - OMM 868 MHz LoRa Fallback Frame:** Codec2 voice frame or radar telemetry from long-range link.
* **`0x04` - OMM Tx Request (Dual-PHY):** Transmit request from Central Box to 2.4 GHz mesh or SX1262 LoRa PA.
* **`0x05` - DLE Status & Link Quality:** Reports SNR, RSSI, active PHY mode, and node capability score.
* **`0xFE` - Firmware Update Bootloader Command:** `0xAA 0x55 0xFE 0x01 "BOOT"` drops RP2040 into USB-ROM bootloader for in-system firmware reflashing.

### 5.2 V2 Upgrade Roadmap: Optional LTE-M / NB-IoT Cloud Sled & RF Triplexer
For trans-continental expeditions, an alternate Pod 3 sled design is prepared:
* **Quectel BG95-M3 Modem:** Adds LTE Cat M1, NB-IoT, eGPRS, and integrated GNSS fallback.
* **RF Triplexer:** Combines antenna connections for 868 MHz LoRa, LTE-M (Bands B1/B3/B8/B20), and GNSS L1 onto a single ruggedized feed.
* **Cloud Telemetry Mirror:** Enables live location tracking on web dashboards far beyond direct LoRa range.

---

## 6. Automotive Dead Reckoning (ADR) & Sensor Fusion

The GNSS subsystem in Rear Pod 3 (**u-blox NEO-M9N / MAX-M10S**) is coupled to the 6-axis IMU (**Bosch BMI270**) and motorcycle wheel speed sensors via a **15-State Error-State Kalman Filter (ES-EKF)**:

```
[ u-blox GNSS Module (M10S 10 Hz) ] ──(UART 460.8k)──┐
[ CAN-Bus Wheel Speed / Velocity ] ───(10-20 Hz)─────┼─► [ 15-State Extended Kalman Filter ] ──► [ MicroSD: tour.gpx ]
[ Bosch BMI270 Gyro / Accel (I2C) ] ──(50-100 Hz)────┘        (Dead Reckoning Engine)            (With Lean Angle & G-Force)
```

### 6.1 Continuous Tunnel and Mountain Gorge Tracking
* When satellite signals are lost in tunnels or deep alpine canyons, the Kalman filter continuously integrates wheel velocity and angular yaw/pitch rates.
* Prevents route freezing or erratic map snapping.

### 6.2 MotoGP-Style Telemetry in GPX 2.0 Format
Each trackpoint records comprehensive vehicle dynamics:
* **Lean Angle Left/Right (°):** $\text{Lean\_Angle} = \arctan\left(\frac{v \cdot \dot{\psi}}{g}\right)$
* **Longitudinal and Lateral Acceleration (Braking and acceleration G-forces)**
* **Vehicle Battery Voltage and Satellite Metrics**

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

## 7. Actioncam Control & 1-PPS Precision Video Synchronization

OpenMotorBridge controls mounted action cameras wirelessly via handlebar controls and embeds sensor telemetry into video containers:

1. **1-PPS Hardware Timestamping:** The GNSS receiver outputs a 1 Hz pulse on `PIN_GNSS_PPS` with $< 15\,\text{ns}$ jitter, keeping video footage and lean angle logs synchronized frame-accurately over multiple hours.
2. **Supported Camera Protocols:**
   * **GoPro (Hero 9/10/11/12/13):** Open GoPro BLE API (GATT Service `0xFEA6`).
   * **Insta360 (X3 / X4 / Ace Pro):** Emulates official Insta360 GPS Smart Remote; telemetry is written natively into GPMF/INSV streams.
   * **DJI (Osmo Action 3/4/5 Pro):** DJI BLE Remote protocol.
3. **Handlebar Remote Gestures:**
   * **Single Click:** Places a video highlight marker in the GPX log.
   * **Double Click:** Start / Stop recording.
   * **Apex Auto-Trigger:** Lean angles exceeding $45^\circ$ automatically generate a highlight tag.
