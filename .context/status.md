# OpenMotorBridge - Current System Context

## Hardware & Architecture (v8.5 / v9.0 All-UWB Clean Architecture)
- **Topology:** 6-PCBA Lineup (`PCBA 01` Central Box, `PCBA 03` Universal Cartridge, `PCBA 05` Cockpit Front-Node, `PCBA 06` MagSafe Dock, `PCBA 07` Smart Keyfob, `PCBA 08` Radar 2.0 Sub-MCU & Wings).
- **Vehicle Data Backbone:** 100% Wireless All-UWB 6.5 GHz (Qorvo DW3110 / Channel 5 @ 6.489 GHz, ETSI EN 302 065-3, < 0.4 ms latency) für alle Satelliten (Front-Node, Bucht 1, Bucht 2, Radar). Bluetooth ist exklusiv für Helm-Headsets und Smartphone reserviert; 2.4 GHz OMM ist eine rein optionale Swap-Kassette.
- **Audio Routing:** 100% Wireless. OEM headsets in cartridges connect via Bluetooth to Central Box ES8388 24-bit DSP mixer; mixed audio streams wirelessly via BT to rider/pillion helmets. Zero copper audio wiring across the vehicle.
- **Main Connector:** Automotive Deutsch DTM-12 (IP67/IP69K, 12 pins, 11 active: KL30, KL15, GND, CAN_H, CAN_L, 2x Pod 1 5V, 2x Pod 2 5V, 2x Radar 12V, 1x Chassis Earth).
- **Wiring Harness:** Pure 2-wire DC power whips (AWG22 +5V/GND for Pods, AWG22 +12V/GND for Radar). M8 and USB-C connectors on pods completely eliminated.
- **Satellite Pod Housings:** Monolithic 3D-printed PA12 MJF parts (`pod_base_housing.stl`) without internal PCB. The 2-wire DC lead connects directly to 2 gold-plated leaf spring contacts.
- **Modular Cartridge (`PCBA 03`):** 35 x 25 mm, 2 Lagen ENIG, 2-seitig SMT (Top: Qorvo DW3110 UWB Transceiver, SPI Host-MCU; Bottom: 4x AO3400A MOSFETs, 8P J_ACT, 2P Front-Goldpads +5V/GND). 100% unified PCB layout with DNP strategy (Midland PMR446 populates ES8311 mono audio codec; Sena/Cardo DNP). Sämtliche Steuerdaten laufen über UWB.
- **Slot Assignment & Security:** 
  - Sequential Power-Sequencing ($T = 0\,\text{ms}$ Front-Node & Central Box, $T = 200\,\text{ms}$ Bucht 1 Links, $T = 350\,\text{ms}$ Bucht 2 Rechts, $T = 500\,\text{ms}$ Radar 12V).
  - AES-128-CCM vehicle encryption & UWB Time-of-Flight (ToF) geofence ($< 1.2\,\text{m}$).
  - Hardware Pair/Reset button (`SW1`) on Central Box + Companion App management + seamless Multi-Vehicle Roaming (up to 4 NVS profiles per cartridge).
- **Retired Hardware:**
  - `PCBA 02` (Pod Base) retired without replacement (direct 2-pin contact in housing).
  - `PCBA 04` (Heck-Pod 3) retired without replacement (GNSS on Front-Node, LoRa on Central Box).
  - Bourns transformers `T1, T2` and PhotoMOS optos `OC1, OC2` removed from Central Box.

## Completed Milestones
- [x] **All-UWB & Pure-DC Architecture Finalized (v8.5 / v9.0):**
  - Consolidated from 8 to exactly 6 PCBAs.
  - Deutsch DTM-12 wirelist and central breakout harness specification.
  - Verification & production scripts (`verify_pcb_designs_jlcpcb.py`, `export_manufacturing_packages.py`) 100% passing.
  - Central Box `PCBA 01` schematics and PCB updated with SX1262 LoRa, DW3110 UWB, U.FL antennas, SW1 button, and DTM-12.
- [x] **OpenMotorMesh (OMM) Dual-PHY & Adaptive QoS:**
  - 2.4 GHz Proximity High-Speed PHY (SC-FDMA TDMA 10ms Superframe, Full-Duplex HiFi Voice, Music Sharing).
  - 868 MHz Long-Range LoRa PHY (SX1262, Continuous GPS Group Radar, Codec2 1200 bps PTT Voice Tunnel).
  - 3-Tier Adaptive QoS (Proximity -> Fringe -> Long-Range Fallback).
  - LTE-Sidelink Cluster Partitioning & Inter-Cluster Gateway Relay.
- [x] **Tour-Logging, Dead Reckoning & Actioncam Control:**
  - Automotive Dead Reckoning (ADR) with 15-State EKF (GNSS + CAN wheel speed + BMI270 IMU).
  - Actioncam & 360° Cam BLE control (Open GoPro API, Insta360 GPS Smart Remote emulation, DJI BLE).
- [x] **WebBLE PWA Dashboard with Lightweight i18n:**
  - Instant DE/EN language switcher without page reload.
  - Live simulation & sensor visualizer (lean angle, speed, voltage, battery chemistry).
- [x] **Manufacturing & JLCPCB Packages:**
  - Complete Gerbers, Drills, BOMs, CPLs, and MJF STLs generated for all 6 active PCBAs.