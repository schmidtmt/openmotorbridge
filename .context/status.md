# OpenMotorBridge - Current System Context

## Hardware & Architecture (v8.0 Clean Architecture)
- **Topology:** Dual-Pod Satellite + Cockpit Front-Node (Main Box under seat, Pod 1 Left Sena, Pod 2 Right Cardo/Swap, Front-Node Cockpit Hub)
- **Vehicle Backbone:** Deterministic UWB 6.5 GHz (Qorvo DW3110 / Channel 5 @ 6.489 GHz, ETSI EN 302 065-3, < 0.4 ms latency, zero duty-cycle limit)
- **Connector:** HD26 SEAL-D Flange (IP67) -> 4-Whip Harness (Whip 1: Pod 1, Whip 2: Pod 2, Whip 4: Power/CAN, Whip 5: Rear Radar; Pins 9–11 unassigned reserve)
- **Pod Connection:** Symmetrical 6-wire shielded PUR cable (VCC, GND, Audio/UART, Opto/PPS, 1-Wire ID)
- **Front/Cockpit:** Universal Front-Node (PCBA 05) with u-blox SAM-M10Q Multi-GNSS via J12 Qwiic, dual Knowles MEMS mics, hardwired zero-latency PTT, 4-Port USB Hub & Dual 20W USB-PD
- **BOM:** ESP32-S3, onboard Semtech SX1262 LoRa 868 MHz (UPS-buffered 24/7), Qorvo DW3110 UWB, ES8388 24-Bit Codec, TCAN334G CAN-FD, LM5164 Buck, BQ24075 UPS with JEITA NTC
- **Retired:** Rear Pod 3 and PCBA 04 retired without replacement (cost and complexity reduced, no antenna holes in pods)

## Completed Milestones
- [x] **Documentation v8.0 in German & English:**
  - `docs/de/` (Chapters 01–17) & `docs/en/` (Chapters 01–17)
  - Root `README.md` (EN) and `README.de.md` (DE)
  - 100% syntactically verified across all 40 markdown files
- [x] **OpenMotorMesh (OMM) Dual-PHY & Adaptive QoS:**
  - 2.4 GHz Proximity High-Speed PHY (SC-FDMA TDMA 10ms Superframe, Full-Duplex HiFi Voice, Music Sharing)
  - 868 MHz Long-Range LoRa PHY (SX1262, Continuous GPS Group Radar, Codec2 1200 bps PTT Voice Tunnel)
  - 3-Tier Adaptive QoS (Proximity -> Fringe -> Long-Range Fallback)
  - LTE-Sidelink Cluster Partitioning & Inter-Cluster Gateway Relay with autonomous Sub-Leader election
- [x] **Tour-Logging, Dead Reckoning & Actioncam Control:**
  - Automotive Dead Reckoning (ADR) with 15-State EKF (GNSS + CAN wheel speed + BMI270 IMU)
  - Tunnel navigation & Multipath outlier rejection
  - Actioncam & 360° Cam BLE control (Open GoPro API, Insta360 GPS Smart Remote emulation, DJI BLE)
  - Map-Matching pipeline with strategic shaping points export (Garmin, BMW, Kurviger, Calimoto, TomTom)
- [x] **WebBLE PWA Dashboard with Lightweight i18n:**
  - Instant DE/EN language switcher without page reload
  - Live simulation & sensor visualizer (lean angle, speed, voltage, battery chemistry)
  - Complete 5-tab control center with glassmorphism dark theme
- [x] **KiCad 7/8 Projects & Hierarchical Block Schematics:**
  - `hardware/kicad_main_box/` (4 hierarchical sheets: Power, MCU/Codec/CAN, Audio Isolated, HD26 Interface)
  - `hardware/kicad_rear_pod3/` (ESP32-C3, MAX-M10S, SX1262, TPS7A0533, DS2401, 6-Pin Pogo)
  - `hardware/kicad_pod_cartridge/` (Mill-Max 6-Pin Pogo, DS2401, TLP222A interface, IP4220CZ6 ESD)
  - `hardware/README.md` (JLCPCB 4-Layer FR4 TG150 ENIG specification)