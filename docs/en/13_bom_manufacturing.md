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

## 6. Mechanical CAD & 3D Printing BOM (MJF PA12 / ASA)

### 6.1 CAD / STL Asset Overview (17 Parts for 1 Motorcycle)
* **Central Main Box (3 parts, PA12 / ASA):** `main_box_lower_case.stl`, `main_box_mid_tray.stl`, `main_box_lid.stl`.
* **Satellite Pods (6 parts, PA12 / ASA):** 3x `pod_base_housing.stl`, 3x `03_pod_bulkhead_partition.stl`.
* **Cartridges (3 parts, PA12 / ASA):** `cartridge_sena_sled.stl` (or Cardo), `cartridge_cardo_sled.stl` (or Blank), `cartridge_omm_transceiver_sled.stl`.
* **Universal Front Node Housing (2 parts, PA12 / ASA):** `front_node_lower_tub.stl`, `front_node_upper_lid.stl`.
* **Front Node Glands & Dust Cap (2 parts, TPU 95A / 85A):** `front_node_cable_glands_tpu.stl` (Pair of South USB & West signal combs), `front_node_usbc_cap_tpu.stl` (Elastomeric USB-C dust cap with tether).
* **Rear Radar Bracket (1 part, PA12 / ASA):** `pod3_radar_bracket.stl` (M5 GoPro swivel arm for Pod 3).

---

## 7. Step-by-Step Commissioning, Measurement & Test Protocol

### Step 1: Visual Inspection (Prior to Initial Power-Up)
* [ ] Exclude solder bridges beneath LM5164, BQ24075, ES8388, and USB2512B under inspection microscope.
* [ ] Verify polarity of TVS diode D1 (SMBJ33CA) and P-channel MOSFET reverse polarity circuit.
* [ ] Confirm the 2.5 mm isolation barrier around Bourns transformers T1/T2 and PhotoMOS OC1/OC2 is free of tin whiskers.

### Step 2: Bench Power-Up & Current Verification
* [ ] Set laboratory DC power supply to $12{,}0\,\text{V DC}$ with $150\,\text{mA}$ current clamp.
* [ ] Measure quiescent current: Expected $= 45\,\text{mA}$ to $75\,\text{mA}$ (without battery charging).
* [ ] Test point `TP_5V`: Expected $= 5{,}15\,\text{V} \pm 0{,}05\,\text{V}$.
* [ ] Test point `TP_3V3`: Expected $= 3{,}30\,\text{V} \pm 0{,}02\,\text{V}$.

### Step 3: Firmware Flash & Hardware Self-Test
* [ ] Execute PlatformIO / ESP-IDF flash over USB-C port (`firmware/main_controller/`).
* [ ] Format LittleFS storage partition and flash OEM cartridge JSON profiles.
* [ ] Open serial console (115,200 Baud): Verify "LittleFS Mount OK", "1-Wire Manager Task OK", "I2S ES8388 Codec Init OK", "TCAN334G CAN-FD OK".

### Step 4: Audio & Ducking Verification
* [ ] Feed $1\,\text{kHz}$ sine wave ($1{,}0\,\text{V}_{\text{RMS}}$) into audio input line.
* [ ] Connect oscilloscope to `PORT1_AUDIO_OUT`: Verify audio attenuates smoothly within $15\,\text{ms}$ upon PTT trigger.
* [ ] Release PTT trigger: Confirm $600\,\text{ms}$ hold period followed by smooth $250\,\text{ms}$ raised-cosine volume restoration.

### Step 5: IP67 Pressure Decay Test
* [ ] Place assembled enclosure into vacuum decay chamber at $-20\,\text{kPa}$ gauge pressure for 60 seconds (leakage rate $< 0{,}5\,\text{kPa}$).

---

## 8. JLCPCB SMT Ordering Checklist (All 5 Boards)

| Assembly / PCBA | Gerber ZIP Archive | BOM CSV File | CPL (Pick & Place) CSV | Layers & Stackup | Surface Finish |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **1. Central Box Main Board** | `01_main_box_pcba_gerbers_jlcpcb.zip` | `01_main_box_pcba_bom_jlcpcb.csv` | `01_main_box_pcba_cpl_jlcpcb.csv` | **4 Layers** (JLC04161H-7628) | **ENIG (Gold)**, 1.6 mm, TG150 |
| **2. Pod Base Board** | `02_pod_base_pcba_gerbers_jlcpcb.zip` | `02_pod_base_pcba_bom_jlcpcb.csv` | `02_pod_base_pcba_cpl_jlcpcb.csv` | **2 Layers** (Standard) | **ENIG (Gold)**, 1.6 mm |
| **3. Cartridge Carrier** | `03_pod_cartridge_pcba_gerbers_jlcpcb.zip` | `03_pod_cartridge_pcba_bom_jlcpcb.csv` | `03_pod_cartridge_pcba_cpl_jlcpcb.csv` | **2 Layers** (Standard) | **ENIG (Gold)**, 1.2 mm |
| **4. Rear Pod 3 Transceiver** | `04_rear_pod3_pcba_gerbers_jlcpcb.zip` | `04_rear_pod3_pcba_bom_jlcpcb.csv` | `04_rear_pod3_pcba_cpl_jlcpcb.csv` | **4 Layers** (JLC04161H-7628) | **ENIG (Gold)**, 1.6 mm, TG150 |
| **5. Universal Front Node** | `05_smart_fairing_pcba_gerbers_jlcpcb.zip` | `05_smart_fairing_pcba_bom_jlcpcb.csv` | `05_smart_fairing_pcba_cpl_jlcpcb.csv` | **4 Layers** (JLC04161H-7628) | **ENIG (Gold)**, 1.6 mm, TG150 |

---

## 9. Central Wiring Harness (HD26 Breakout Pigtail)

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

## 10. COTS Procurement List (Complete Kit for 1 Vehicle)

| Component | Specification / Type | Supplier / Manufacturer | Quantity | Location & Function |
| :--- | :--- | :--- | :---: | :--- |
| **M3 Case Screws** | M3 x 40 mm Socket Head V4A (DIN 912) | Standard Hardware | 4 pcs | 4-Corner Central Box Assembly |
| **M3 Front Case Screws**| M3 x 20 mm Socket Head V4A (DIN 912) | Standard Hardware | 4 pcs | 4-Corner Front Node Enclosure Screws |
| **M2.5 PCB Mounting Screws**| M2.5 x 6 mm Socket Head V4A (DIN 912) | Standard Hardware | 8 pcs | 4x Central Box PCB, 4x Front Node PCB |
| **M3 Threaded Inserts** | Ruthex M3 x 5.7 mm Brass (RX-M3x5.7) | Ruthex / Amazon | 8 pcs | 4x Central Box Tub, 4x Front Node Tub |
| **M4 Threaded Inserts** | Ruthex M4 x 8.1 mm Brass (RX-M4x8.1) | Ruthex / Amazon | 4 pcs | Front Node Base (AMPS pattern 30 x 38 mm) |
| **M2 Bulkhead Screws** | M2 x 8 mm Countersunk V4A (DIN 7991) | Standard Hardware | 6 pcs | Secures 3 Pod Bulkheads (2 per pod) |
| **M5 Radar Clamp Screw** | M5 x 25 mm Socket Head V4A (DIN 912) + Acorn Nut | Standard Hardware | 1 pc | Secures Pod 3 GoPro radar swivel hinge |
| **Ejector Springs** | Stainless V4A ($D=4{,}5\,\text{mm}, L_0=15\,\text{mm}, R=1{,}2\,\text{N/mm}$) | Gutekunst Federn | 6 pcs | Auto-Eject Mechanism (2 per Pod) |
| **Rubber Silentblocks** | Type A M4 Male/Female ($\varnothing 15 \times 10\,\text{mm}$) + Nyloc Nuts | Standard Hardware | 4 pcs | Vibration-isolated frame mount for Main Box |
| **EPDM Frame O-Rings** | UV- & Ozone-resistant EPDM ($\varnothing 45\dots 75\,\text{mm}$) | QuadLock / Standard | 6 pcs | Tool-free tube saddle mount (Pods & Front Node) |
| **EPDM Cable Combs (Front)**| EPDM Closed-Cell Slotted Rubber ($15 \times 8 \times 4\,\text{mm}$) | Custom / EPDM Shop | 2 pcs | Waterproof ribbon cable feedthrough in Front Node |
| **Silicone Gasket Cord** | Silicone Solid Cord $\varnothing 1.5\,\text{mm}$ Shore 40A (1.0 m) | Standard O-Ring Shop | 1 pc | $40\,\text{cm}$ Main Box groove, $30\,\text{cm}$ Front Node lid groove |
| **Cartridge Face Seals** | Molded Silicone Flange Seal Shore 40A ($54 \times 18\,\text{mm}$) | Custom / Silicone | 3 pcs | Front face seal on Pods 1, 2, and 3 |
| **Silicone USB-C Cap** | Waterproof tethered silicone dust cap | GCT / Amazon | 1 pc | IP67 protective cover for Front Node Port J2 |
| **Handlebar PTT Button** | IP67 Button (Momentary NO) with Clamp ($\varnothing 22/28\,\text{mm}$) | Daytona / Oxford / APEM | 1 pc | Battery-free handlebar PTT wired to Front Node (J3) |
| **Gore Vent Screw** | Gore Automotive AVS 41 (M8x1.25) | W. L. Gore & Associates | 1 pc | Central Box Lid Equalization & Condensation Inhibit |
| **Gore Adhesive Vents**| Gore Adhesive Vent $\varnothing 6{,}0\,\text{mm}$ IP67 | W. L. Gore & Associates | 5 pcs | 3x Pods, 1x Front Node, 1x Knowles MEMS acoustic port |
| **Optical Light Pipe** | Bivar PLPC3-3MM ($\varnothing 3{,}0\,\text{mm}, L=8\,\text{mm}$) | Bivar / Mentor | 1 pc | Optical transmission of WS2812B LED through lid |
| **3M Dual-Lock Tape** | 3M Dual-Lock SJ3550 (Mushroom tape, 25 mm wide) | 3M / Amazon | 25 cm | Vibration-proof fairing mount for Ottocast & Front Node |
| **Backup Battery** | 1S LiPo (3.7V 1000mAh) with 10k NTC & Molex Micro-Fit | EEMB / Enerpower | 1 pc | Seamless UPS power reserve in Central Box |
| **Automotive Fuse Holder** | Waterproof Mini-Blade Inline Fuse Holder + **2A Fuse** | Hella / MTA | 1 pc | Protects permanent 12V feed (KL30) at battery terminal |
| **HD26 Flange & Plug** | Amphenol LTW HD26 IP67 (Chassis socket + Cable plug) | Amphenol LTW | 1 set | 26-pin primary interface between box and harness |
| **AMP Superseal 1.5 Plug**| TE Connectivity 4-Pin Housing with female contacts | TE Connectivity | 1 pc | 12V vehicle power connection on harness |
| **M8 Extension Cables (Pods)**| M8 6-Pin A-Coded PUR Shielded (1.0m / 1.5m) | Binder / Phoenix / Murr | 3 pcs | Pigtail to Pod 1, 2, and 3 Interconnect |
| **M8 Extension Cable (Radar)**| M8 4-Pin A-Coded PUR Shielded (1.0m) | Binder / Phoenix / Murr | 1 pc | Connection to Garmin Varia / mmWave rear radar |
| **Automotive Wire** | FLRY-B $0.5\,\text{mm}^2$ & $0.35\,\text{mm}^2$ (various colors) | Leoni / Helukabel | As req. | Bike harness per `central_breakout_harness_wirelist.csv` |
| **Murata MM8030 Pigtails (Pod 3)**| Murata MM126036 to SMA Bulkhead IP67 (150 mm, RG-178)| Murata / Mouser | 3 pcs | Coaxial bypass for J3 (2.4G), J4 (868M), J5 (GNSS) |
| **U.FL Pigtail (Front Node)**| IPEX MHF1 / U.FL to RP-SMA Bulkhead IP67 (150 mm, RG-178) | Taoglas / Molex | 1 pc | Coaxial lead for ESP32-C3 external fairing antenna |
| **SMA Flange Double Bulkhead**| SMA Female to SMA Female Bulkhead IP67 with O-ring & nut | Amphenol / Radiall | 1 pc | Waterproof RF feedthrough in cartridge faceplate (Class A) |
| **Internal Coax Pigtail (Cartridge)**| RG-178 Coaxial Cable ($6\dots 10\,\text{cm}$, 90° SMA Male to SMA Male)| Delock / Taoglas | 1 pc | RF connection from Sena +Mesh / OEM adapter to faceplate |
| **SMA IP67 Protective Caps** | Nickel-plated brass with internal O-ring (knurled cap)| Amphenol / Radiall | 5 pcs | Waterproof seal for unpopulated external SMA ports (3x Pod 3, 1x Front, 1x Pod) |
| **External 2.4 GHz Mesh Antenna**| 2.4 GHz Collinear Dipole (+5 dBi / +7 dBi) with SMA Male | Taoglas / Linx | 1 pc | Optional high-gain antenna on tail / topcase |
| **External 868 MHz LoRa Antenna**| 868 MHz Monopole / Dipole (+3 dBi / +5 dBi) with SMA Male | Linx ANT-868 / Taoglas | 1 pc | Optional long-range mountain pass antenna |
| **External Active GNSS Antenna**| Active Flat Puck (+28 dB LNA, 3.3V phantom power, SMA) | Taoglas AA.162 / Garmin | 1 pc | Optional roof/luggage mount for clear sky view |
| **USB-A Flat Ribbon Cable (Front)**| Short 90° USB-A male-to-female adapter ($10\dots 15\,\text{cm}$)| Delock / Amazon | 1 pc | Ottocast connection to J1 via front cable gland |
| **USB-C Glovebox Cable (Front)**| Right-angle USB-C male-to-male ($1.0\,\text{m}$, PUR/Nylon) | Anker / Baseus | 1 pc | Smartphone charging from J2 via front cable gland |
| **JST-GH Connector Kit (Left)** | JST-GH 1.25mm 2-Pin female housings + crimp terminals | JST / Mouser | 2 sets | Pre-crimped harness leads for J3 (PTT) & J7 (12V) |
| **90° USB Cartridge Cable** | Low-profile 90° right-angle Micro-USB/USB-C ($5\dots 8\,\text{cm}$) | Delock / Amazon | 1 pc | 5V power feed for Sena +Mesh / MeshPort inside cartridge |
| **EPDM Cartridge Retaining Band**| Elastic EPDM rubber strap ($\approx 35 \times 10\,\text{mm}$) | Custom / Sena | 1 pc | Vibration-proof retention of OEM adapter via cartridge hooks |

---

## 11. Required Tools & Workshop Equipment

To assemble all 5 subassemblies, crimp the harness, and perform commissioning, the following minimum equipment and assembly chemicals are required (for details, see [Chapter 14, Section 2.6](file:///Users/schmidtm/openMotorBridge/docs/en/14_build_instructions_assembly.md#26-category-f-required-tools-measurement-equipment--assembly-chemicals)):

| Tool Category | Tools & Specification | Primary Project Purpose |
| :--- | :--- | :--- |
| **Mechanics & Screws** | Hex keys 1.5 / 2.0 / 2.5 / 3.0 mm; Wrenches 7, 8, 10 mm; Torque driver ($0.2 \dots 1.5\,\text{Nm}$) | Even tightening of enclosures, PCBAs, and SMA bulkheads |
| **Thermal Assembly** | Soldering station ($200 \dots 450\,^\circ\text{C}$) with Ruthex M3/M4 tips & fine chisel tip | Perpendicular insertion of 12x brass inserts; harness soldering |
| **Crimp & Harnessing** | Micro-crimper (Engineer PA-09 / IWISS IWS-2820M); Automotive crimper; Wire stripper; Heat gun | Crimping JST-SH (1.0 mm), JST-GH (1.25 mm), and dual-wall heatshrink |
| **RF & Precision Electronics**| ESD precision tweezers (curved, plastic/ceramic coated) | Safe perpendicular mating of Murata MM8030 and U.FL coax plugs |
| **Chemicals & Sealing** | OKS 1110 / Liqui Moly silicone grease; Loctite 243 threadlocker; Conformal coating | IP67 sliding seal lubrication, vibration locking, and PCB humidity protection |
| **Testing & Flashing** | Digital multimeter; Benchtop power supply with current limit ($12\,\text{V} / 150\,\text{mA}$); USB-C cable | Short-circuit prevention, rail validation, and firmware flashing |




