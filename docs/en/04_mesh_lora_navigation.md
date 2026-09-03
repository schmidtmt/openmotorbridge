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

---

## 2. Dynamic Leader Election (DLE) & Group Partitioning

In large riding groups (up to 20 motorcycles), terrain obstacles (mountain ridges, tunnels, traffic gaps) often divide the group. The DLE algorithm ensures continuous group integrity:

1. **Heartbeat & Scoring:** Every motorcycle broadcasts a 10 Hz heartbeat containing its GNSS position, speed, and link quality.
2. **Leader Selection:** The node located centrally within the convoy with the lowest packet error rate is dynamically elected group leader ($T_{\text{election}} < 250\,\text{ms}$).
3. **Sub-Mesh Partitioning:** If the convoy splits across a mountain pass, two autonomous sub-meshes form automatically without audio stutter.
4. **Seamless Re-Merge:** When the groups rejoin, the sub-meshes merge in $< 300\,\text{ms}$ with zero rider intervention.

---

## 3. 10 Hz Multi-GNSS Engine (u-blox NEO-M9N) & 1-PPS Timecode

Located in the Rear Pod 3, the u-blox NEO-M9N multi-constellation receiver tracks GPS, Galileo, GLONASS, and BeiDou concurrently:

* **10 Hz Update Rate:** Position, velocity, and lean-angle updates every $100\,\text{ms}$.
* **Active 3.3V LNA Phantom Feed:** Bias-T circuit supplies an external low-noise amplifier on the ceramic patch antenna.
* **1-PPS Hardware Synchronization:** Generates a sub-microsecond pulse per second (`GNSS_PPS`) to align IMU data, audio recordings, and video markers across the entire motorcycle network.
* **Dead-Reckoning (ADR-EKF):** When entering tunnels or mountain gorges, a 15-state Extended Kalman Filter merges the Bosch BMI270 6-axis IMU data with wheel speeds from the CAN-bus to sustain continuous navigation.

---

## 4. Video Telemetry Overlay Synchronization

GPX tracks recorded by OpenMotorBridge include embedded `<omb:video_sync>` metadata for instant alignment in telemetry tools (VIRB Edit, Telemetry Overlay, Dashware):
* Frame-accurate timecode matching camera clock ($10\,\text{Hz}$).
* Real-time lean angle ($^\circ$), forward acceleration ($g$), and speed ($v$).
* Handlebar PTT button presses recorded as highlight markers.
