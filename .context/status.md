# OpenMotorBridge - Current System Context

## Hardware & Architecture (v8.0)
- **Topology:** 4-Point Satellite (Main Box under seat, Pod 1 Left Sena, Pod 2 Right Cardo, Pod 3 Rear OMM/GNSS)
- **Connector:** HD26 Flange (IP67) -> Internal 2x13 Ribbon to ESP32-S3 PCB (26 Pins, 0 NC)
- **Pod Connection:** Symmetrical 6-wire shielded PUR cable (VCC, GND, Audio/UART, Opto/PPS, 1-Wire ID)
- **Front/Cockpit:** 100% wireless via BLE 5.0 handlebar remote (CR2032 monitored via Service 0x180F)
- **BOM:** ESP32-S3, ES8388 24-Bit Codec, TCAN334G CAN-FD, LM5164 Buck, BQ24075 UPS with JEITA NTC
- **Rear Pod 3:** ESP32-C3 Co-Processor, u-blox MAX-M10S 10Hz GNSS, Semtech SX1262 LoRa (+22 dBm PA), DS2401 ID, TPS7A0533 LDO

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