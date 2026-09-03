# 13 - Bill of Materials (BOM) & SMT Manufacturing (All 5 PCBAs)

This document provides the complete Bill of Materials (BOM) and manufacturing specifications for all 5 printed circuit board assemblies (PCBA 01 to PCBA 05) for production at JLCPCB / Eurocircuits, mechanical 3D printed parts, testing protocols, the JLCPCB SMT ordering guide, and COTS component procurement lists.

---

## 1. PCBA 01: Central Box Main Controller (`kicad_main_box`, 4-Layer FR4 TG150)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | ESP32-S3-WROOM-1-N16R8 | Espressif Systems | SMD Module | C2913200 | Host MCU (Dual-Core, 16 MB Flash, 8 MB PSRAM) |
| **U2** | LM5164-Q1 | Texas Instruments | SOIC-8-EP | C2843477 | Automotive 65V Synchronous Buck Converter |
| **U3** | BQ24075RGTR | Texas Instruments | VQFN-16 | C128509 | Dynamic Power-Path Controller & LiPo Charger |
| **U4** | BMI270 | Bosch Sensortec | LGA-14 | C2838380 | 6-Axis IMU for Lean Angle & Dynamics |
| **U5** | ES8388 | Everest Semi | QFN-28 | C144547 | 24-Bit Stereo Audio Codec (I2S ADC/DAC) |
| **U6** | TCAN334GDCNR | Texas Instruments | SOT-23-8 | C842340 | 3.3V Automotive CAN-FD Transceiver (±58V Fault) |
| **T1, T2** | LM-NP-1001-B1L | Bourns Inc. | SMD Transformer| C114402 | 1:1 Audio Transformer (1500 V RMS Isolation) |
| **OC1, OC2**| TLP222A(F) | Toshiba | SOP-4 | C112444 | Solid-State PhotoMOS Relay for PTT Keying |
| **D1** | SMBJ33CA | Littelfuse | DO-214AA (SMB) | C87848 | TVS Diode (33 V Standoff, 53.3 V max Clamping) |
| **F1** | MF-MSMF050-2 | Bourns | 1812 SMD | C22668 | Resettable PPTC Fuse (500 mA Hold / 1.0 A Trip) |
| **LED1** | WS2812B-B | Worldsemi | 5050 SMD | C114586 | RGB Status LED for Visual Diagnostics |
| **J1** | 2x13 Box Header | Standard 2.54 mm | THT Box Header | C2934175 | Internal Ribbon Connector to HD26 Flange |
| **J2** | MicroSD Slot Push-Push | Molex / Korean Hro | SMD Push-Push | C266624 | 4-Bit SDIO Flash Card for Tour Logging |
| **J_BAT** | Molex Micro-Fit 3.0 2P | Molex | SMD Header | C289110 | Header for LiPo Backup Battery |
| **CN1** | HD26 Receptacle IP67 | Amphenol LTW | Flange D-Sub | Custom Part | Waterproof 26-Pin Enclosure Interface |

---

## 2. PCBA 02: Satellite Pod Base Carrier (`openmotorbridge_pod_base`, 2-Layer FR4)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **J1** | PinHeader_1x06_P2.54mm_SMD | Harwin / Wurth | SMD Vertical | C2934176 | 6-Pin Pin Header inside Bulkhead Shroud |
| **J2** | M8_6PIN_RECEPTACLE (A-Coded)| Binder / Phoenix | M8 Connector | C289100 | M8 6-Pin IP67 Receptacle to Cable Harness |
| **U1** | SP3012-06UTG | Littelfuse | DFN-14 | C2834580 | 6-Channel Ultra-Low-Cap ESD Array (< 0.5 pF) |
| **C1** | 100nF 50V X7R | Samsung / Yageo | 0603 SMD | C14663 | Decoupling Capacitor for 5V Rail |

---

## 3. PCBA 03: Universal Cartridge Carrier (`openmotorbridge_pod_cartridge`, 2-Layer FR4)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **J1** | PinSocket_1x06_P2.54mm_SMD | Harwin / Samtec | SMD Horizontal | C2934177 | Front 6-Pin Precision Socket (Sled Insertion) |
| **J2** | JST-SH 1.0mm 6-Pin Horizontal| JST | SMD Right-Angle| C136657 | Ribbon Cable Connection to Headset Cradle |
| **U1** | DS2401Z+ | Maxim / ADI | SOT-23 | C2834570 | 64-Bit 1-Wire Silicon Serial ROM (Cartridge ID)|
| **F1** | MF-MSMF050-2 (500mA) | Bourns | 1812 SMD | C22668 | Resettable PPTC Fuse for 5V Cartridge Rail |
| **D1** | Green 5V Power LED | Everlight | 0805 SMD | C2297 | Visual Power Status Indicator |
| **D2** | SP3012-06UTG | Littelfuse | DFN-14 | C2834580 | 6-Channel ESD Protection Matrix |

---

## 4. PCBA 04: Rear Pod 3 Transceiver (`openmotorbridge_rear_pod3`, 4-Layer FR4 TG150)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U10** | RP2040 Dual Cortex-M0+ | Raspberry Pi | QFN-56 | C2040 | Coprocessor for NMEA Parsing & OMM LoRa Engine |
| **U11** | NEO-M9N-00B / MAX-M10S | u-blox | LCC-24 / LGA-18 | C3006240 | Multi-Constellation GNSS Engine (10 Hz, 1-PPS) |
| **U12** | SX1262IMLTRT | Semtech | QFN-24 | C190184 | Secondary Fallback 868 MHz LoRa Transceiver (+22 dBm)|
| **U13** | DS2401Z+ | Maxim / ADI | SOT-23 | C2834570 | 64-Bit 1-Wire Silicon Serial Number ID |
| **U14** | TPS7A0533PDBVR | Texas Instruments | SOT-23-5 | C505293 | Ultra-Low-Noise 3.3V LDO (200 mA) for GNSS & LoRa |
| **ANT1** | GP.1575.25.4.A.02 | Taoglas | 25x25x4 mm Patch | C2689100 | Ceramic Patch Antenna for GPS/Galileo/BeiDou |
| **ANT2** | ANT-868-CW-HWR-SMA | Linx / Taoglas | Helical Antenna| C290111 | 868 MHz Helical Antenna for LoRa Tail Cowl |
| **J3, J4, J5**| MM8030-2610RJ3 | Murata Electronics | SMD 2.0x2.0 mm | C2834595 | Automatic RF switch sockets for external antennas (2.4G, 868M, GNSS) |

---

## 5. PCBA 05: Universal Front Node (`openmotorbridge_front_node`, 4-Layer FR4 TG150)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | ESP32-C3-WROOM-02U-N4 | Espressif Systems | SMD Module | C2934560 | 32-Bit RISC-V Controller (160 MHz, ext. U.FL) |
| **U2** | USB2512B-AEZG | Microchip | QFN-36 | C97184 | USB 2.0 High-Speed 480 Mbps 2-Port Hub Controller |
| **U3** | LMR36015FSCQRNXRQ1 | Texas Instruments | VQFN-12 | C2843480 | Automotive 36V Synchronous Buck (5V / 2.0A, 91.8%) |
| **U4** | TPS2051BDBVR | Texas Instruments | SOT-23-5 | C7818 | High-Side USB VBUS Power Switch (1.05A Clamp) |
| **MIC1** | SPH0645LM4H-B | Knowles | 3.5x2.65 mm SMD | C119850 | Digital I2S MEMS Acoustic Microphone |
| **L1** | 4.7 µH Automotive Inductor | Sunlord / Wurth | SMD 5x5 mm | C2843490 | Power Inductor for LMR36015 Buck Converter |
| **J1** | USB-A Receptacle R/A | Amphenol / Korean Hro | SMD Right-Angle| C2934180 | Port 1: Switched VBUS for Ottocast Dongle |
| **J2** | USB-C 16-Pin Receptacle IP67| GCT / Korean Hro | SMD Hybrid | C2765186 | Port 2: Constant VBUS Glovebox / Charging Port |
| **J3** | JST-GH 2-Pin Header | JST | 1.25mm SMD | C2934185 | Handlebar PTT Interface (GPIO 0 Interrupt) |
| **J7** | 2-Pin Screw Terminal / JST-GH| Phoenix / JST | 2.54mm THT | C289115 | 12V Vehicle Power Input (KL15 & GND) |

---

## 6. JLCPCB SMT Ordering Checklist (All 5 Boards)

| Assembly / PCBA | Gerber ZIP Archive | BOM CSV File | CPL (Pick & Place) CSV | Layers & Stackup | Surface Finish |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **1. Central Box Main Board** | `01_main_box_pcba_gerbers_jlcpcb.zip` | `01_main_box_pcba_bom_jlcpcb.csv` | `01_main_box_pcba_cpl_jlcpcb.csv` | **4 Layers** (JLC04161H-7628) | **ENIG (Gold)**, 1.6 mm, TG150 |
| **2. Pod Base Board** | `02_pod_base_pcba_gerbers_jlcpcb.zip` | `02_pod_base_pcba_bom_jlcpcb.csv` | `02_pod_base_pcba_cpl_jlcpcb.csv` | **2 Layers** (Standard) | **ENIG (Gold)**, 1.6 mm |
| **3. Cartridge Carrier** | `03_pod_cartridge_pcba_gerbers_jlcpcb.zip` | `03_pod_cartridge_pcba_bom_jlcpcb.csv` | `03_pod_cartridge_pcba_cpl_jlcpcb.csv` | **2 Layers** (Standard) | **ENIG (Gold)**, 1.2 mm |
| **4. Rear Pod 3 Transceiver** | `04_rear_pod3_pcba_gerbers_jlcpcb.zip` | `04_rear_pod3_pcba_bom_jlcpcb.csv` | `04_rear_pod3_pcba_cpl_jlcpcb.csv` | **4 Layers** (JLC04161H-7628) | **ENIG (Gold)**, 1.6 mm, TG150 |
| **5. Universal Front Node** | `05_smart_fairing_pcba_gerbers_jlcpcb.zip` | `05_smart_fairing_pcba_bom_jlcpcb.csv` | `05_smart_fairing_pcba_cpl_jlcpcb.csv` | **4 Layers** (JLC04161H-7628) | **ENIG (Gold)**, 1.6 mm, TG150 |

---

## 7. Central Wiring Harness (HD26 Breakout Pigtail)

```
                               CENTRAL HD26 BREAKOUT HARNESS
┌─────────────────────────┐
│ HD26 IP67 Male Plug     │ ──► Overall pigtail length: 250 mm each (protective braided sleeving)
│ (Amphenol LTW / D-Sub)  │ ──► Y-breakout junction molded with hot-melt / heatshrink boot
└─┬───────────────────────┘
  ├─► PIGTAIL 1 (250 mm): M8 6-Pin Female (A-Coded, IP67) ──► Pod 1 (Driver Helmet Left)
  ├─► PIGTAIL 2 (250 mm): M8 6-Pin Female (A-Coded, IP67) ──► Pod 2 (Passenger Helmet Right)
  ├─► PIGTAIL 3 (250 mm): M8 6-Pin Female (A-Coded, IP67) ──► Pod 3 (Tail Cowl OMM & GNSS)
  ├─► PIGTAIL 4 (250 mm): AMP Superseal 1.5 4-Pin Female   ──► 12V Power (KL30, KL15, GND, Chassis)
  └─► PIGTAIL 5 (250 mm): M8 4-Pin Female (A-Coded, IP67) ──► CAN-Bus & Cockpit Front Mic
```

---

## 8. COTS Procurement List

| Component | Specification / Type | Supplier / Manufacturer | Quantity | Function |
| :--- | :--- | :--- | :---: | :--- |
| **M3 Case Screws** | M3 x 40 mm Socket Head V4A (DIN 912) | Standard Hardware | 4 pcs | 4-Corner Central Box Assembly |
| **M3 Front Case Screws**| M3 x 20 mm Socket Head V4A (DIN 912) | Standard Hardware | 4 pcs | Front Node Enclosure Screws |
| **M3 Threaded Inserts** | Ruthex M3 x 5.7 mm Brass | Ruthex / Amazon | 8 pcs | Heat-Set Inserts (Box & Front Node) |
| **M4 Threaded Inserts** | Ruthex M4 x 8.1 mm Brass | Ruthex / Amazon | 4 pcs | Heat-Set Inserts for AMPS Base |
| **M2 Bulkhead Screws** | M2 x 8 mm Countersunk V4A (DIN 7991) | Standard Hardware | 6 pcs | Secures 3 Pod Bulkheads |
| **Ejector Springs** | Stainless V4A ($D=4{,}5\,\text{mm}, L_0=15\,\text{mm}, R=1{,}2\,\text{N/mm}$) | Gutekunst Federn | 6 pcs | Auto-Eject Mechanism (2 per Pod) |
| **EPDM O-Rings** | UV- & Ozone-resistant EPDM ($\varnothing 45\dots 75\,\text{mm}$) | QuadLock / Standard | 6 pcs | Tube Saddle Mount (Pods & Front Node) |
| **Gore Vent Screw** | Gore Automotive AVS 41 (M8x1.25) | W. L. Gore & Associates | 1 pc | Central Box Lid Equalization |
| **Gore Adhesive Vents**| Gore Adhesive Vent $\varnothing 6{,}0\,\text{mm}$ IP67 | W. L. Gore & Associates | 4 pcs | Pod & Front Node Equalization |
| **Backup Battery** | 1S LiPo (3.7V 1000mAh) with NTC | EEMB / Enerpower | 1 pc | UPS Emergency Power Supply |
| **M8 Extension Cables**| M8 6-Pin A-Coded PUR Shielded (1.0m / 1.5m)| Binder / Phoenix / Murr | 3 pcs | Pigtail to Pod Interconnect |
