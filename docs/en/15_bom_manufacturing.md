# 15 - Bill of Materials (BOM), COTS Sourcing & SMT Manufacturing (All 7 PCBAs)

This document serves as the master reference (Single Source of Truth) for the complete Bill of Materials (BOM), manufacturing specifications for all 7 printed circuit board assemblies (PCBA 01 to PCBA 03, PCBA 05 to PCBA 08 – PCBA 04 is retired without replacement in v8.0) at JLCPCB / Eurocircuits, all mechanical 3D printed components, COTS procurement lists, and a comprehensive cost and ordering strategy (Solo builder vs. Community group buy).

---

## 1. PCBA 01: Central Box Main Controller (`openmotorbridge_central_box`, 4-Layer FR4 TG150)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | ESP32-S3-WROOM-1-N16R8 | Espressif Systems | SMD Module | C2913200 | Host MCU (Dual-Core, 16 MB Flash, 8 MB PSRAM) |
| **U2** | LM5164-Q1 | Texas Instruments | SOIC-8-EP | C2843477 | Automotive 65V Synchronous Buck Converter |
| **U3** | BQ24075RGTR | Texas Instruments | VQFN-16 | C15464 | Dynamic Power-Path Controller & LiPo Charger with TS |
| **U4** | BMI270 | Bosch Sensortec | LGA-14 | C2836813 | 6-Axis IMU for Lean Angle & Dynamics |
| **U5** | ES8388 | Everest Semi | QFN-28 | C365736 | 24-Bit Stereo Audio Codec (I2S ADC/DAC) |
| **U6** | TCAN334GDCNR | Texas Instruments | SOT-23-8 | C842340 | 3.3V Automotive CAN-FD Transceiver (±58V Fault) |
| **U7** | SX1262IMLTRT | Semtech | QFN-24 | C190184 | Onboard 868 MHz LoRa Transceiver (+22 dBm, 24/7 UPS-buffered) |
| **U8** | DW3110 | Qorvo | QFN-16 (B.Cu) | C2934600 | IEEE 802.15.4z UWB Transceiver (6.5 GHz Ch. 5 Backbone) |
| **T1, T2** | LM-NP-1001-B1L | Bourns Inc. | SMD Transformer| C114402 | 1:1 Audio Transformer (1500 V RMS Galvanic Isolation) |
| **OC1, OC2**| TLP222A(F) | Toshiba | SOP-4 | C112444 | Solid-State PhotoMOS Relay for PTT Keying |
| **D1** | SMBJ33CA | Littelfuse | DO-214AA (SMB) | C87848 | TVS Diode (33 V Standoff, 53.3 V max Clamping) |
| **F1** | MF-MSMF050-2 | Bourns | 1812 SMD | C22668 | Resettable PPTC Fuse (500 mA Hold / 1.0 A Trip) |
| **LED1** | WS2812B-B | Worldsemi | 5050 SMD | C114586 | RGB Status LED for Visual Diagnostics |
| **J1** | 2x13 Box Header | Standard 2.54 mm | THT Box Header | C2934175 | Internal Ribbon Connector to HD26 Flange |
| **J2** | MicroSD Slot Push-Push | Molex / Korean Hro | SMD Push-Push | C266624 | 4-Bit SDIO Flash Card for Tour Logging |
| **J_BAT** | Molex Micro-Fit 3.0 2P | Molex | SMD Header | C289110 | Header for 2,200 mAh LiPo Backup Battery |
| **ANT1** | U.FL-R-SMT-1 | Hirose / Murata | SMD RF | C2834595 | LoRa 868 MHz U.FL socket to Taoglas FXP895 in lid |
| **ANT2** | U.FL-R-SMT-1 | Hirose / Murata | SMD RF (B.Cu) | C2834595 | UWB 6.5 GHz U.FL socket to Taoglas FXUWB10 in tub floor |
| **CN1** | HD26 Receptacle IP67 (SEAL-D)| Amphenol LTW | Flange D-Sub | Custom Part | Waterproof 26-Pin Enclosure Interface (19 active pins) |

---

## 2. PCBA 02: Satellite Pod Base Carrier (`openmotorbridge_pod_base`, 2-Layer FR4)
> **Quantity Note:** The pod base is 100% symmetric and installed **2x per motorcycle** (Pod 1 left, Pod 2 right).

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **J1** | PinHeader_1x06_P2.54mm_SMD | Harwin / Wurth | SMD Vertical | C2934176 | 6-Pin Pin Header inside Bulkhead Shroud |
| **J2** | M8_6PIN_RECEPTACLE (A-Coded)| Binder / Phoenix | M8 Connector | C289100 | M8 6-Pin IP67 Receptacle to Cable Harness |
| **U1** | SP3012-06UTG | Littelfuse | DFN-14 (3.5x1.35mm)| C2834580 | 6-Channel Ultra-Low-Cap ESD Array (< 0.5 pF) |
| **C1** | 100nF 50V X7R | Samsung / Yageo | 0603 SMD | C14663 | Decoupling Capacitor for 5V Rail |

---

## 3. PCBA 03: Smart Modular Cartridge Rev 2.0 (`openmotorbridge_pod_cartridge`, 2-Layer FR4)
> **Quantity Note:** Fitted **2x per motorcycle** (Slot 1 for Sena SPIDER X Slim, Slot 2 for Cardo Packtalk Edge or optional OMM 2.4 GHz Swap Cartridge).

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | CH32V003F4P6 | WCH | TSSOP-20 / QFN-20 | C3011382 | 32-Bit RISC-V MCU (1-Wire ROM-ID Emulation & ISP Macro Controller) |
| **Q1, Q2, Q3, Q4** | AO3400A | Alpha & Omega | SOT-23 | C20917 | 30V / 5.7A N-Channel Power MOSFETs for 4x Mechatronic Actuators |
| **D3, D4, D5, D6** | 1N4148WS | Diodes Inc. / LRC | SOD-323 | C81598 | Flyback Protection Diodes for Inductive Actuator Coils |
| **J1** | PinSocket_1x06_P2.54mm_SMD | Harwin / Samtec | SMD Horizontal | C2934177 | Front 6-Pin Precision Socket to Pod Base |
| **J2** | JST-SH 1.0mm 6-Pin Horizontal| JST | SMD Right-Angle| C136657 | Audio Diff & Direct-DC Cable Whip to Headset Inlay |
| **J_ACT** | JST-SH 1.0mm 8-Pin Horizontal| JST | SMD Right-Angle| C136659 | Mechatronics Header for 4 Independent Miniature Solenoids |
| **F1** | MF-MSMF050-2 (500mA) | Bourns | 1812 SMD | C22668 | Resettable PPTC Fuse for 5V Cartridge Rail |
| **D1** | Duo-Status LED Green/Blue | Everlight / Xinglight | 0805 SMD | C2834575 | Status LED: Green = 1-Wire Active / Config Synced, Blue = Actuator Pulse |
| **D2** | SP3012-06UTG | Littelfuse | DFN-14 | C2834580 | 6-Channel Ultra-Low-Cap ESD Protection Matrix |
| **C1, C2** | 100nF 50V X7R | Samsung | 0603 SMD | C14663 | Decoupling Capacitors for VCC and MCU Rail |

---

## 4. Assembly PCBA 04 (Rear Pod 3): Retired Without Replacement (Clean Architecture v8.0)

> [!NOTE]
> **Architecture Streamlining v8.0:** Circuit board `PCBA 04` and the 3rd satellite enclosure (Rear Pod 3) have been **completely eliminated without replacement**:
> 1. **LoRa 868 MHz (SX1262):** Sits directly on the Central Box (`PCBA 01`), backed up 24/7 by the UPS battery for continuous anti-theft sentry.
> 2. **Multi-GNSS (SAM-M10Q):** Sits in the cool ram-air intake zone on Front Node (`PCBA 05`), interfaced via Qwiic I2C (`J12`).
> 3. **Vehicle Wireless Backbone:** Transmitted via Ultra-Wideband (Qorvo DW3110 / 6.5 GHz Ch. 5, $< 0.4\,\text{ms}$ latency) between Front Node and Central Box.
> 4. **Rear Radar:** Connects directly to the Central Box via Whip 5 of the HD26 harness.

---

## 5. PCBA 05: Universal Front Node (`openmotorbridge_front_node`, 4-Layer FR4 TG150, 82 x 50 mm)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | ESP32-S3-WROOM-1U-N8R8 | Espressif Systems | SMD Module | `C2913200` | Dual-Core 32-Bit Xtensa LX7 (240 MHz, Vector-DSP, 8MB PSRAM, ext. U.FL) |
| **U2** | USB2514Bi-AEZG / USB2514B | Microchip | QFN-36 | `C16251` | Automotive/Industrial USB 2.0 High-Speed 480 Mbps 4-Port Hub Controller |
| **U3** | LMR36015FSCQRNXRQ1 | Texas Instruments | VQFN-12 | `C2843480` | Automotive 36V Synchronous Buck (5V / 2.0A, 91.8%) for Hub & Peripherals |
| **U4** | TPS2051BDBVR | Texas Instruments | SOT-23-5 | `C7818` | High-Side USB VBUS Power Switch (1.05A Clamp) for Port 2 Cold-Reboot Reset |
| **U5** | SC8102QDER | Southchip | QFN-32 | `C2843510` | Automotive Synchronous Buck with USB-PD 20W (9V/2.2A & QC3.0) for Smartphone Port 1 |
| **U6** | TCAN334GDCNT | Texas Instruments | SOT-23-8 | `C2843515` | 3.3V CAN Transceiver (5 Mbps CAN-FD capable, with Pin 8 Silent-Listen-Only Mode) |
| **U7** | DW3110 | Qorvo | QFN-16 (B.Cu) | `C2934600` | IEEE 802.15.4z UWB Transceiver (6.5 GHz Ch. 5 Backbone) |
| **K1** | CPC1017NTR | IXYS / Littelfuse | SOP-4 | `C26789` | 60V / 100mA 1-Form-A Solid-State Relay for switchable 120R CAN Termination (Auto-Sensing) |
| **Q1** | DMN63D8LDW-7 | Diodes Incorporated| SOT-363 | `C283890` | Dual N-Channel MOSFET (30V / 260mA) for directional mirror blind-spot LEDs (J9) |
| **Q2** | TPS1H100BQPWPRQ1 | Texas Instruments | HTSSOP-14 | `C2843520` | Automotive Smart High-Side Power Switch (up to 3.5A / 40W) for 12V Aux Light (J11) |
| **LED1**| WS2812B-2020 | Worldsemi | SMD 2020 | `C2843530` | Digitally controllable RGB status LED for enclosure lid light pipe |
| **MIC1**| MSM261S4030H0R / SPH0645 | Sipeed / Knowles | 3.5x2.65 mm SMD | `C544577` | Digital I2S MEMS Acoustic Microphone (Standard I2S, high availability) |
| **L1** | 4.7 µH Automotive Inductor | Sunlord / Wurth | SMD 5x5 mm | `C2843490` | Storage Inductor for LMR36015 5V Main Regulator |
| **L2** | 10 µH Automotive Inductor | Coilcraft / Wurth | SMD 7x7 mm | `C2843525` | Storage Inductor for SC8102 USB-PD Fast-Charge Buck (Port 1) |
| **J1** | JST-PH 2-Pin Header | JST | 2.00mm SMD | `C289115` | 12V Vehicle Power Input (KL15 & GND) |
| **J2** | JST-PH 3-Pin Header | JST | 2.00mm SMD | `C289116` | Cockpit CAN-Bus (CAN_H, CAN_L, GND with Auto-Sensing Relay) |
| **J3** | JST-PH 4-Pin Header | JST | 2.00mm SMD | `C289117` | Handlebar Multi-Button Interface (PTT, Cam-Action, Media-Voice, GND) |
| **J4** | JST-PH 4-Pin Header | JST | 2.00mm SMD | `C289117` | Upstream USB Port to Motorcycle Infotainment (Skyline OS / Boom! Box) |
| **J5** | JST-PH 4-Pin Header | JST | 2.00mm SMD | `C289117` | Port 1: Handlebar Smartphone (USB-PD 20W + High-Speed Data) |
| **J6** | JST-PH 4-Pin Header | JST | 2.00mm SMD | `C289117` | Port 2: Fairing Pigtail (shielded, 30 cm) to CP2AA CarPlay/AA Dongle |
| **J5_MP3**| JST-PH 4-Pin Header | JST | 2.00mm SMD | `C289117` | Port 3: Glovebox Cable for USB Drives (MP3s & Firmware Updates) |
| **J6_AUX**| JST-PH 4-Pin Header | JST | 2.00mm SMD | `C289117` | Port 4: Cockpit Accessories / Dashcam Storage / Zūmo Navi |
| **J7** | USB-C 16-Pin Receptacle IP67| GCT / Korean Hro | SMD Hybrid | `C2765186` | ESP32-S3 Service & Flash Port (Flank) with TPU Sealing Plug |
| **J8** | JST-PH 2-Pin Header | JST | 2.00mm SMD | `C289115` | Action-Cam 5V Charge-Only Power Port (up to 2.0A) |
| **J9** | JST-PH 3-Pin Header | JST | 2.00mm SMD | `C289116` | Mirror Blind-Spot Warning LEDs (12V_PROT, BSD_LEFT_N, BSD_RIGHT_N) |
| **J10** | JST-PH 2-Pin Header | JST | 2.00mm SMD | `C289115` | 12V Qi Wireless Charger Power (SP Connect / QuadLock Head) |
| **J11** | JST-PH 2-Pin Header | JST | 2.00mm SMD | `C289115` | 12V Aux Light (Adventure Driving Lights / Brake Flash Strobe) |
| **J12** | JST-SH 4-Pin Header | JST | 1.00mm SMD | `C289118` | Qwiic / STEMMA QT I2C Sensor Port (SAM-M10Q GNSS, TMP117, OPT3001) |
| **ANT1**| U.FL-R-SMT-1 | Hirose / Murata | SMD RF (B.Cu) | `C2834595` | UWB 6.5 GHz U.FL socket to Taoglas FXUWB10 in tub floor |

---

## 6. PCBA 06: MagSafe Framework Dock Adapter (`openmotorbridge_magsafe_dock`, 2-Layer FR4, 28 x 11.5 mm)

| Ref | Component / Type | Package | Specification & Function | LCSC Part |
| :--- | :--- | :--- | :--- | :--- |
| **`F1`** | 0ZCG0050FF2C | SMD 1206 | 500 mA Hold / 1000 mA Trip, 16V PPTC Resettable Fuse | `C207936` |
| **`D1`** | ESD5Z5.0T1G | SOD-323 | 5.0V Unidirectional TVS Diode (Transient Protection) | `C2834585` |
| **`U1`** | USBLC6-4SC6 | SOT-23-6 | 4-Channel ESD Protection Array ($<0.8\,\text{pF}$, $\pm 15\,\text{kV}$ ESD) | `C7519` |
| **`C1`** | 100nF 50V X7R | SMD 0603 | Ceramic Decoupling Capacitor on VCC_PROT | `C14663` |
| **`J1`** | M8 Wire Pads | SMD/THT 1x07 | 7-Pin Solder Pad Array with 0.6 mm Vias for M8 Harness Conductors | Custom |
| **`J2`** | MagSafe 6P Pads | SMD 1x06 | 6-Pin Gold-Plated Landing Pads for MagSafe Magnetic Pogo Coupler | `C224376` |
| **`H1`** | MountingHole_Pad | M2.5 (Ø 2.7 mm) | Hole Ø 2.7 mm, Pad Ø 4.5 mm, tied to System GND | Hardware |

---

## 7. PCBA 07: 2-in-1 LoRa Smart-Keyfob (`openmotorbridge_smart_keyfob`, 2-Layer FR4, 38 x 19 mm)

| Ref | Component / Type | Package | Specification & Function | LCSC Part |
| :--- | :--- | :--- | :--- | :--- |
| **`U1`** | nRF52840-QIAA-R | aQFN-73 | 32-Bit ARM Cortex-M4F SoC with Bluetooth 5.4, NFC & Crypto | `C190767` |
| **`U2`** | SX1262IMLTRT | QFN-24 | Semtech 868 MHz LoRa Transceiver (+22 dBm, TCXO) | `C90039` |
| **`U3`** | DRV2605LDGSR | VSSOP-10 | TI ERM/LRA Haptic Driver with Integrated Effect Library | `C61633` |
| **`U4`** | BQ51003YFPR | DSBGA-28 | TI 2.5W Qi Wireless Power Receiver Controller | `C144862` |
| **`U5`** | BQ25100YFPR | DSBGA-6 | TI Linear LiPo Charge Controller with 50 nA Quiescent Current | `C144857` |
| **`M1`** | VG1036001D | Coin 10x3.6mm | Vybronics LRA Linear Resonant Actuator (235 Hz Resonant Frequency) | Custom / Distrelec |
| **`BZ1`**| PKLCS1212E4001 | SMD 12x12mm | Murata SMD Piezo Sounder (85 dB @ 10 cm, 4 kHz) | `C94511` |

---

## 8. PCBA 08: Radar 2.0 Sub-MCU & 36-LED Wing Carrier (`openmotorbridge_radar_submcu`, 4-Layer FR4 TG150, 115 x 65 mm)

| Ref | Component / Type | Package | Specification & Function | LCSC Part |
| :--- | :--- | :--- | :--- | :--- |
| **`U1`** | ESP32-C5-WROOM-1-N8 | SMD Module | 32-Bit RISC-V Dual-Band Sub-MCU (2.4 GHz + 5.9 GHz V2X, 4MB Flash) | `C2843550` |
| **`U2`** | LDO 3.3V 500mA | SOT-23-5 | TI TPS7A0533 / Richtek RT9013 LDO Voltage Regulator | `C505293` |
| **`D1..36`**| WS2812B-2020 | SMD 2020 | 36x Digital RGB LEDs in Dual Warning Wings (18 left, 18 right) | `C2843530` |
| **`ANT1`** | 5.9 GHz V2X Patch | 20x20x4 mm | Ceramic Patch Antenna for ITS-G5 Car-to-X Safety Broadcasts | `C290456` |
| **`J1`** | JST-SH 1.0mm 4-Pin | SMD Right-Angle| Decoupled Internal Signal Whip to Binder M5 Housing Receptacle | `C136657` |
| **`J2`** | JST-SH 1.0mm 4-Pin | SMD Right-Angle| UART Interface to Wheeltec MR20 Transceiver (RX/TX/5V/GND) | `C136657` |
| **`D_TVS`**| PESD5V0S2BT | SOT-23 | TVS Diode Array for UART & Power Lines | `C2834580` |

---

## 9. 1-Click Ordering Guide for JLCPCB (All 7 PCBAs Fully Assembled)

All manufacturing packages reside in the repository under `hardware/pcba/` as complete ZIP and CSV archives:

| Subassembly / PCBA | Gerber ZIP Archive | BOM CSV File | CPL (Pick & Place) CSV | Layers | Manufacturing Notes |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **PCBA 01: Central Box** | `01_main_box_pcba_gerbers_jlcpcb.zip` | `01_main_box_pcba_bom_jlcpcb.csv` | `01_main_box_pcba_cpl_jlcpcb.csv` | **4 Layers** | ENIG (Gold), 1.6 mm, TG150, 2-sided SMT (DW3110 on B.Cu) |
| **PCBA 02: Pod Base** | `02_pod_base_pcba_gerbers_jlcpcb.zip` | `02_pod_base_pcba_bom_jlcpcb.csv` | `02_pod_base_pcba_cpl_jlcpcb.csv` | **2 Layers** | ENIG (Gold), 1.6 mm, SMT Top (Order 2x per vehicle) |
| **PCBA 03: Cartridge Carrier**| `03_pod_cartridge_pcba_gerbers_jlcpcb.zip` | `03_pod_cartridge_pcba_bom_jlcpcb.csv` | `03_pod_cartridge_pcba_cpl_jlcpcb.csv` | **2 Layers** | ENIG (Gold), 1.2 mm, SMT Top (Order 2x per vehicle) |
| **PCBA 05: Front Node** | `05_front_node_pcba_gerbers_jlcpcb.zip` | `05_front_node_pcba_bom_jlcpcb.csv` | `05_front_node_pcba_cpl_jlcpcb.csv` | **4 Layers** | ENIG (Gold), 1.6 mm, TG150, 2-sided SMT (DW3110 on B.Cu) |
| **PCBA 06: MagSafe Dock** | `06_magsafe_dock_pcba_gerbers_jlcpcb.zip` | `06_magsafe_dock_pcba_bom_jlcpcb.csv` | `06_magsafe_dock_pcba_cpl_jlcpcb.csv` | **2 Layers** | ENIG (Gold), 1.6 mm, SMT Top |
| **PCBA 07: Smart-Keyfob** | `07_smart_keyfob_pcba_gerbers_jlcpcb.zip` | `07_smart_keyfob_pcba_bom_jlcpcb.csv` | `07_smart_keyfob_pcba_cpl_jlcpcb.csv` | **2 Layers** | ENIG (Gold), 1.0 mm, 2-sided SMT |
| **PCBA 08: Radar 2.0 Sub-MCU** | `08_radar_submcu_pcba_gerbers_jlcpcb.zip` | `08_radar_submcu_pcba_bom_jlcpcb.csv` | `08_radar_submcu_pcba_cpl_jlcpcb.csv` | **2 Layers** | ENIG (Gold), 1.2 mm, TG150, SMT Top |

---

## 10. Mechanical & Enclosure BOM (3D Printing MJF PA12 & Hardware)

All enclosure parts are strictly engineered according to the **IKEA Principle**: **Zero heat-set threaded brass inserts required!** Enclosures feature captive hexagonal nut pockets (for DIN 934 / DIN 985 stainless steel nuts) or precise pilot holes for direct self-tapping plastic screws.

### 10.1 Base System (Universal for Every Motorcycle)
| Subassembly | STL File Path | Qty | Material & Process | Function & Description |
| :--- | :--- | :---: | :--- | :--- |
| **Main Box Lower Case** | [`main_box_lower_case.stl`](../../hardware/cad/stl/01_main_box/main_box_lower_case.stl) | **1** | MJF PA12 / ASA | Monocoque tub with UWB bottom pocket ($11 \times 11 \times 0.6\,\text{mm}$), 4x M4 silentblock ears & sealing groove |
| **Main Box Mid Tray** | [`main_box_mid_tray.stl`](../../hardware/cad/stl/01_main_box/main_box_mid_tray.stl) | **1** | MJF PA12 / ASA | Battery tray for 2,200 mAh flat LiPo ($68 \times 39 \times 5.0\,\text{mm}$), 11x convection vents & tongue-and-groove rib |
| **Main Box Lid** | [`main_box_lid.stl`](../../hardware/cad/stl/01_main_box/main_box_lid.stl) | **1** | MJF PA12 / ASA | Lid with LoRa FXP895 antenna pocket ($110 \times 20 \times 0.8\,\text{mm}$), Gore ePTFE vent seat & countersinks |
| **Pod Base Housing** | [`pod_base_housing.stl`](../../hardware/cad/stl/02_pod_base/pod_base_housing.stl) | **2** | MJF PA12 / ASA | Universal bay enclosure for Pod 1 (Left) and Pod 2 (Right) |
| **Pod Bulkheads** | [`03_pod_bulkhead_partition.stl`](../../hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl) | **2** | MJF PA12 / ASA | Bulkhead partition with sealing collar & spring guides (1x per pod) |
| **Cartridge Base Sled**| [`cartridge_base_sled.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl) | **2** | MJF PA12 / ASA | Universal sled for Gateway 1 (Pod 1) and Gateway 2 (Pod 2) |
| **Cartridge Latch Lever**| [`cartridge_magnetic_lock_latch.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_magnetic_lock_latch.stl) | **2** | MJF PA12 / ASA | Magnetic anti-theft locking latch levers for Cartridge Slots 1 & 2 |
| **Front Node Lower Tub** | [`front_node_lower_tub.stl`](../../hardware/cad/stl/04_front_node/front_node_lower_tub.stl) | **1** | MJF PA12 / ASA | Cockpit tub with UWB bottom pocket ($11 \times 11 \times 0.6\,\text{mm}$), AMPS pattern & handlebar tube cradle |
| **Front Node Upper Lid** | [`front_node_upper_lid.stl`](../../hardware/cad/stl/04_front_node/front_node_upper_lid.stl) | **1** | MJF PA12 / ASA | Lid with Knowles MEMS acoustic inlet port & O-ring sealing channel |
| **Front Node Cable Glands**| [`front_node_cable_glands_tpu.stl`](../../hardware/cad/stl/04_front_node/front_node_cable_glands_tpu.stl) | **1 Pair**| TPU 95A / 85A | Flexible split sealing comb for front USB and signal wiring |
| **Front Node USB-C Cap** | [`front_node_usbc_cap_tpu.stl`](../../hardware/cad/stl/04_front_node/front_node_usbc_cap_tpu.stl) | **1** | TPU 95A / 85A | Elastic dust cap with retention tether for service port |

### 10.2 Gateway Cartridge Inlays (Intercom Selection)
> **Architecture Note:** Slot 1 and Slot 2 are **Multi-Protocol Gateway Transceivers**, not rider/passenger headsets! They link the motorcycle simultaneously to Sena Mesh and Cardo DMC. Rider and pillion communicate wirelessly with their standard helmet headsets.

| Subassembly | STL File Path | Qty | Material | Function & Description |
| :--- | :--- | :---: | :--- | :--- |
| **Gateway Inlay Sena** | [`cartridge_insert_sena.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) | *Opt. (1)* | MJF PA12 / ASA | Form-fitting inlay for Sena SPIDER X Slim (Mesh 3.0 / 2.0, direct micro-cable whip) |
| **Gateway Inlay Cardo** | [`cartridge_insert_cardo.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl) | *Opt. (1)* | MJF PA12 / ASA | Inlay for Cardo Packtalk Edge / Pro (DMC Gen2) with Air-Mount cradle |
| **Swap Inlay OMM 2.4 GHz** | [`cartridge_insert_omm.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_omm.stl) | *Opt. (1)* | MJF PA12 / ASA | Inlay for OMM 2.4 GHz Swap Cartridge (ESP32-C3) |
| **Blank Cartridge / Dry Box** | [`cartridge_insert_blindkassette.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_blindkassette.stl) | *Opt. (1)* | MJF PA12 / ASA | Hermetic protective dummy sled for unused slots or watertight dry box |

### 10.3 Vehicle-Specific Mounting Kits (3D Printed Parts)
* **Kit 1: BMW R1250 / R1300 GS (Standard / Vario Panniers):**
  * `adventure_transition_dock_base.stl` (2 pcs): Pannier-independent base cradles for the seat frame crease (Ø 28 mm tube).
  * `adventure_transition_dock_lid.stl` (2 pcs): Aerodynamic body lids with transition crease & Cardo/Sena cutouts.
  * `adventure_underseat_cross_rail.stl` (1 pc): Rigid under-seat saddle bridge locking left and right docks with integrated M8 channel.
  * `adventure_rack_radar_mount.stl` (1 pc): Minimal rear radar mount positioned under the GS luggage bridge for Garmin Varia / Wheeltec MR20 on Whip 5.
* **Kit 2: BMW R1250 / R1300 GSA (Adventure with Ø 18 mm Stainless Rack):**
  * `adventure_gsa_cage_dock_body.stl` & `adventure_gsa_clamp_cap.stl` (2 pcs each): Heavy-duty cage docks for Pod 1 & 2 in the 45 mm dead space of the pannier frame with 85 mm dual-saddle clamp, stone-guard wedge & concealed M8 conduit.
  * `adventure_rack_radar_mount.stl` (1 pc): Minimal rear radar mount under luggage bridge.
* **Kit 3: Harley-Davidson Touring & Classic Bagger (Street Glide, Road Glide, Road King):**
  * `saddlebag_lid_dock.stl` (2 pcs): Hard saddlebag lid mounting docks for Pod 1 & 2.
  * `radar_license_plate_bracket.stl` (1 pc): Vibration-isolated license plate radar bracket for Whip 5.
  * `magsafe_cockpit_mount_harley.stl` (1 pc), `magsafe_frame_dock.stl` (1 pc) & `magsafe_clamp_wings.stl` (1 pc): MagSafe frame dock components.
* **Kit 4: Support Car / Van Convoy Kit (Car-Kit):**
  * `car_sun_visor_pod_clip.stl` (2 pcs): Quick-release spring clips for secure, vibration-free mounting of Pod 1 and Pod 2 to the sun visors in chase car or van (driver and passenger side).
  * Dashboard dock for SAM-M10Q GNSS receiver behind the windshield.

---

## 11. Pre-Assembled COTS Harnesses & RF Antennas (Zero Crimping, Zero Soldering!)

No custom wire harnessing or crimping is required. The system leverages 100% commercially available, industrially molded standard cables (COTS):

```
                        PLUG-AND-PLAY HARNESS CONCEPT (COTS PRE-MOLDED)
┌─────────────────────────┐
│ HD26 IP67 Pre-Molded    │ ──► Overmolded HD26 breakout harness whip (Amphenol LTW COTS)
│ (Central Box Interface) │ ──► 100% watertight molded, zero discrete pin crimping required
└─┬───────────────────────┘
  ├─► Whip 1: M8 6-Pin PUR Cable (1.0 m / 1.5 m): Standard pre-molded sensor/actuator cable ──► Pod 1
  ├─► Whip 2: M8 6-Pin PUR Cable (1.0 m / 1.5 m): Standard pre-molded sensor/actuator cable ──► Pod 2
  ├─► Whip 4: AMP Superseal 12V Cable (1.0 m): Pre-assembled fused battery harness ──► Vehicle 12V Rail
  └─► Whip 5: M8 4-Pin Socket (250 mm): Rear Radar (Wheeltec MR20 / Garmin Varia: 12V + UART)
      (Note: Front Node requires ZERO wiring to the rear – links wirelessly via UWB!)
```

### 11.1 RF Antennas & Sensors (COTS)
1. **UWB 6.5 GHz Flex Antennas (2 pcs):** **Taoglas FXUWB10** ($11 \times 11 \times 0.6\,\text{mm}$) with 20 mm U.FL coaxial lead for Central Box and Front Node lower tub floor recesses.
2. **LoRa 868 MHz Flex Antenna (1 pc):** **Taoglas FXP895** ($110 \times 20 \times 0.8\,\text{mm}$) with 50 $\Omega$ U.FL feed for Central Box lid pocket.
3. **Multi-GNSS Module (1 pc):** **u-blox SAM-M10Q** with integrated $15 \times 15\,\text{mm}$ ceramic patch antenna, Qwiic I2C (`J12`) on Front Node inside ram-air duct.
4. **Environmental Sensors (Front Node J12 Daisy-Chain):**
   * **TI TMP117:** High-precision temperature sensor ($\pm 0.1\,^\circ\text{C}$) for black ice early warning.
   * **TI OPT3001:** Ambient light sensor for display and driving light control.

---

## 12. COTS Hardware & Fastener Procurement List (1 Complete Kit)

| Component | Specification / Type | Sourcing Source | Qty | Location & Purpose |
| :--- | :--- | :--- | :---: | :--- |
| **M3 Stainless Screws** | M3 x 40 mm Socket Head A4 / 316 (DIN 912) | Standard Fastener | 4 pcs | Central Box enclosure (engages nut pockets) |
| **M3 Stainless Screws (Front)**| M3 x 20 mm Socket Head A4 / 316 (DIN 912) | Standard Fastener | 4 pcs | Front Node enclosure (engages nut pockets) |
| **M3 Stainless Nuts** | DIN 934 / DIN 985 M3 A4 Nuts | Standard Fastener | 8 pcs | Captive in nut pockets (no soldering iron required!) |
| **M4 Stainless Nuts (AMPS)**| DIN 934 M4 A4 Nuts | Standard Fastener | 4 pcs | Captive in Front Node tub nut pockets |
| **M2.5 Board Screws** | M2.5 x 6 mm Socket Head A4 (DIN 912) | Standard Fastener | 8 pcs | 4x Central Box PCB, 4x Front Node PCB |
| **M2 Bulkhead Screws** | M2 x 8 mm Countersunk A4 (DIN 7991) | Standard Fastener | 4 pcs | Securing the 2 pod bulkheads (2x per Pod 1 & 2) |
| **M2 Sled Retainer Screws** | M2 x 6 mm Countersunk A4 (DIN 7991) | Standard Fastener | 8 pcs | Securing actuator hold-down brackets (4x per gateway) |
| **M2 Pivot Dowel Pins** | M2 x 8 mm Stainless Dowel Pin (DIN 7) | Standard / Misumi | 2 pcs | Pivot pins for magnetic cartridge latches |
| **Magnetic Armature** | Ø 6 x 8 mm Hardened Steel Pin (DIN 6325) | Standard / Misumi | 2 pcs | Steel keeper pin in cartridge latch arm |
| **Latch Return Springs** | Stainless 316 ($\varnothing 3.5\,\text{mm}, L_0=10\,\text{mm}$) | Standard Spring | 2 pcs | Return springs for latch hook |
| **Ejection Springs** | Stainless 316 ($D=4.5\,\text{mm}, L_0=15\,\text{mm}$) | Standard Spring | 4 pcs | Auto-eject springs inside bulkheads (2x per pod) |
| **N52 Release Key** | N52 Neodymium Block ($20 \times 10 \times 5\,\text{mm}$) | Magnet Supplier | 1 pc | Magnetic key for manual cartridge release |
| **Vibration Isolators** | Type A M4 Male/Female ($\varnothing 15 \times 10\,\text{mm}$) | Ganter / Standard | 4 pcs | Shock-isolated Central Box mounting |
| **Silicone O-Ring Cord** | Silicone Solid Cord $\varnothing 1.5\,\text{mm}$ Shore 40A (1.0 m) | O-Ring Supplier | 1 pc | 40 cm Central Box groove, 30 cm Front Node groove |
| **Cartridge Gaskets** | Molded Silicone Gasket Shore 40A ($54 \times 18\,\text{mm}$) | Custom Mold | 2 pcs | Front face mouth sealing on Pod 1 and Pod 2 |
| **UPS Battery Pack** | 1S LiPo Flat Pack 2,200 mAh ($68 \times 39 \times 5.0\,\text{mm}$) with Micro-Fit | EEMB / Enerpower | 1 pc | Central Box UPS buffer (Type 504068 / 503870) |
| **Automotive Fuse Holder** | Waterproof Blade Fuse Holder + 2A Fuse | Hella / MTA | 1 pc | KL30 battery terminal line protection |
| **M8 6-Pin Cables (PUR)** | M8 6-Pin A-Coded Male/Female (1.0m / 1.5m) | Binder / Phoenix | 2 pcs | Plug-and-play harness to Pod 1 and Pod 2 |
| **M8 4-Pin Cable (PUR)** | M8 4-Pin A-Coded Male/Female (0.5–1.5m) | Binder / Phoenix | Opt. (1)| Whip 5: Rear Radar (Wheeltec MR20 / Garmin Varia) |
| **Front Node 12V Cable** | 2-Pin JST-PH Lead with Posi-Tap | COTS Standard | 1 pc | Local cockpit power connection (parking light/GPS plug) |
| **J_ACT Actuator Harness** | Pre-crimped 8-Pin JST-SH to 4x 2-Pin Leads | Adafruit / SparkFun | 2 pcs | Pre-assembled harness for 4 solenoids |
| **Miniature Solenoids** | 5V DC Pull Solenoids ($\varnothing 6.5 \times 12\,\text{mm}$) with TPU Tip | Solenoid Supplier | 8 pcs | 4 pcs per Smart Cartridge (Sena / Cardo) |
| **J2 Gateway Cable** | Pre-crimped 6-Pin JST-SH to Jack / USB | COTS Standard | 2 pcs | Audio & power harness to headset inlays |
| **Binder M5 4-Pin Receptacle**| Series 707 M5 4-Pin Panel Mount with D-Flat | Binder | 1 pc | Housing bulkhead socket for Radar 2.0 Sub-MCU |
| **Wheeltec MR20 77-GHz mmWave**| 77-GHz FMCW Automotive Radar (150 m Range) | Wheeltec | Opt. (1)| Radar 2.0 transceiver module inside rear housing |
| **PC Radome Window** | Laser-cut Polycarbonate 1.6 mm (RF-transparent)| COTS / Plexiglas | Opt. (1)| Microwave & optical window for MR20 & 24-LED Halo |
| **3M Dual Lock SJ3550** | Interlocking Adhesive Fastener Strip (VHB) | 3M | 0.5 m | Vibration-resistant, tool-free module mounting |
| **car_sun_visor_pod_clip** | 3D Printed PA12 Sun Visor Clips | OMB CAD | Opt. (2)| Chase car / van visor mounting kit for Pod 1 & 2 |

---

## 13. Minimalist Tooling List (The True IKEA Principle)

Because **no soldering, no crimping, and no thermal heat-staking of threaded inserts** is required, the tool kit shrinks to an absolute minimum that every rider carries in their standard toolkit:

| Tool | Size / Specification | Assembly Purpose |
| :--- | :--- | :--- |
| **Hex Key Set (Allen)** | **1.5 mm / 2.0 mm / 2.5 mm / 3.0 mm** | Tightening all enclosures, circuit boards, and clamps |
| **Phillips / Torx Driver** | **TX10 / PH1** | Enclosure covers and anti-theft security screws |
| **Open-End Wrench / Socket**| **7 mm AF / 8 mm AF** | Counter-holding M4/M5 nuts during clamp assembly |
| **Scissors / Utility Knife**| Standard | Trimming silicone O-ring cord to length |
| **Silicone Grease** | Liqui Moly / OKS 1110 (small tube) | Lightly lubricating enclosure seals |

> [!TIP]
> **No soldering iron, no hot air station, no specialized crimper, and no heat-staking brass insert tool is needed.** All mechanical and electronic modules assemble exclusively with pre-crimped snap connectors and standard fasteners!

---

## 14. Cost Calculation, Ordering Strategy & Economies of Scale (Solo vs. 2–3 Bikes)

> [!IMPORTANT]
> **Important Note Regarding Commercial Intercoms:**
> The estimated hardware cost of **approx. 130 € to 250 €** applies **exclusively to the OpenMotorBridge system** (assembled PCBAs, 3D printed parts, COTS harnesses, 2,200 mAh backup battery, gaskets, standard hardware).
> Any commercial third-party intercoms inserted into the gateway bays (such as **Sena SPIDER X Slim**, **Cardo Packtalk Edge**) or radar devices (**Garmin Varia RTL515 / eRTL615**) are **sourced by the user** and not included in the self-build BOM cost!

### 14.1 Scenario A: Solo Builder (1 Complete System for 1 Motorcycle)
When an individual builder orders all PCBs alone:
* JLCPCB supplies 5 boards per design (2 fully assembled plus 3 unpopulated spares).
* **Cost Breakdown Solo Builder:**
  * JLCPCB PCBAs (PCBA 01, 02 [2x], 03 [2x], 05 assembled incl. shipping & customs): approx. 135–160 €
  * 3D Printing (MJF PA12 bureau or own ASA filament): approx. 35–45 €
  * COTS harnesses, 2,200 mAh LiPo, stainless fasteners & gaskets: approx. 35–45 €
  * **Total System Cost Solo: approx. 205 € to 250 €**

### 14.2 Scenario B: Community / Group Order (2 to 3 Motorcycles)
When 2 to 3 riders order together:
* All 5 boards are ordered fully populated from JLCPCB.
* Fixed setup fees distribute across 5 fully operational board sets.
* **Cost Breakdown per Motorcycle (at 3 bikes):**
  * JLCPCB PCBAs (share per bike): approx. 70–80 €
  * 3D Printing (per bike): approx. 30–35 €
  * COTS harnesses, 2,200 mAh LiPo, fasteners (bulk discount): approx. 30 €
  * **Total Cost per Motorcycle: only approx. 130 € to 145 €!**

---

## 15. Component Lifecycle & SMT Sourcing Audit (EOL / NRND Alternatives)

### 15.1 Critical Finding: MEMS Microphone (Knowles SPH0645LM4H-B is EOL)
* **Status:** The originally specified Knowles **SPH0645LM4H-B** is formally declared **Obsolete / End-of-Life**.
* **Recommended Successor / Primary Part:** **Sipeed / Zilltek MSM261S4030H0R** (LCSC Part: **`C544577`**).
  * *Advantages:* 100% standard I2S compliant (no DMA bit-shift workarounds required in ESP-IDF), excellent large-scale stock availability at LCSC, pin and footprint compatible.

### 15.2 JLCPCB Extended-Parts & Second-Source Alternatives

| Subassembly / Function | Primary Component | JLCPCB / LCSC Part | Status / Sourcing | Recommended Second-Source / Drop-In Alternative |
| :--- | :--- | :--- | :--- | :--- |
| **Central Box 12V Buck** | TI LM5164-Q1 | `C2843477` | Active (TI), JLCPCB Extended | **TI LMR36015** (60V 1.5A, `C2843480`) or **XLSEMI XL7005A** (80V) |
| **Front Node USB Hub** | Microchip USB2514Bi | `C16251` | Active, Industrial (-40..+85°C) | **Terminus FE1.1s / FE8.1** (JLCPCB Basic Part, cents-level price) |
| **CAN-FD Transceiver (3.3V)** | TI TCAN334GDCNR | `C842340` | Active (TI) | **TI TCAN332G / TCAN337G** or **SITCORE SIT1051T/3** |
| **Audio Transformer (1500V)**| Bourns LM-NP-1001-B1L| `C114402` | Active, JLCPCB Extended | **Triad Magnetics SP-66** or **Bourns SM-LP-5001** |
| **Stereo DSP Codec** | Everest Semi ES8388 | `C365736` | Active (Standard in ESP-ADF) | **Everest Semi ES8311** or **TI TLV320AIC3104** |

---

## 16. Conformal Coating Manufacturing Guidelines (IPC-CC-830B)

To ensure 100% automotive-grade reliability against vibration, condensation, and road salt, all 7 PCBAs are conformal coated during the assembly process:

### 16.1 Coating Specification
* **Standard:** Certified to **IPC-CC-830B** and **MIL-I-46058C**.
* **Type:** **Modified Acrylic Resin (AR)**, e.g., *Peters ELPEGUARD SL 1307 FLZ* (fast curing, UV fluorescent for optical inspection).
* **Layer Thickness:** $30\,\mu\text{m} \dots 60\,\mu\text{m}$ evenly across top and bottom layers.

### 16.2 Mandatory Masking Zones (Kapton Tape Protection)
The following areas must **never** be coated:
1. **Connectors & Sockets:**
   * USB-C receptacles (`J7` Front Node, service ports)
   * M8 / M5 connector pins (`J2` Pod Base, Binder M5 Radar)
   * JST-SH / JST-PH pin headers (`J1..J12` Front Node, `J1..J2` Cartridges)
   * MicroSD card slot (`J2` Central Box)
2. **Acoustic Sensors & Venting:**
   * **MEMS Microphone (`MIC1` MSM261S4030H0R on PCBA 05):** Acoustic inlet port ($\varnothing 0.5\,\text{mm}$) must be sealed with a Kapton dot!
   * **Equalization Vent (Gore ePTFE Vent):** Must remain free of lacquer.
3. **RF Antenna Connectors & Test Points:**
   * U.FL coaxial sockets (`ANT1`, `ANT2`)
   * Test points for in-circuit programming and oscilloscope probing
