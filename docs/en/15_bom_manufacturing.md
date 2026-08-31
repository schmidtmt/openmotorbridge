# 15 - Bill of Materials (BOM) & Manufacturing Guide

Complete Bill of Materials (BOM) and manufacturing specifications for all 4 PCBA circuit boards at JLCPCB / Eurocircuits, comprehensive mechanical BOM for 3D printed PA12 MJF parts and hardware fasteners, and step-by-step verification protocol.

---

## 1. Central Main Box PCB (`kicad_main_box` PCBA, 4-Layer FR4 TG150)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | ESP32-S3-WROOM-1-N16R8 | Espressif Systems | SMD Module | C2913200 | Host MCU (Dual-Core, 16 MB Flash, 8 MB PSRAM) |
| **U2** | LM5164-Q1 | Texas Instruments | SOIC-8-EP | C2843477 | Automotive 65V Synchronous Buck Converter |
| **U3** | BQ24075RGTR / BQ25798 | Texas Instruments | VQFN-16 | C128509 | Dynamic Power-Path Management & LiPo Charger with TS |
| **U4** | BMI270 | Bosch Sensortec | LGA-14 | C2838380 | 6-Axis IMU for Lean Angle & Crash Detection |
| **U5** | ES8388 | Everest Semi | QFN-28 | C144547 | 24-Bit Stereo Audio Codec (I2S ADC/DAC) |
| **U6** | TCAN334GDCNR | Texas Instruments | SOT-23-8 | C842340 | 3.3V Automotive CAN-FD Transceiver (±58V Fault) |
| **T1, T2** | LM-NP-1001-B1L | Bourns Inc. | SMD Transformer | C114402 | 1:1 Audio Transformer (1500 V RMS Galvanic Isolation) |
| **OC1, OC2**| TLP222A(F) | Toshiba | SOP-4 | C112444 | Solid-State PhotoMOS Relay for PTT Key Simulation |
| **D1** | SMBJ33CA | Littelfuse | DO-214AA (SMB) | C87848 | TVS Diode (33 V Standoff, 53.3 V max Clamping) |
| **F1** | MF-MSMF050-2 | Bourns | 1812 SMD | C22668 | Resettable PPTC Fuse (500 mA Hold / 1.0 A Trip) |
| **LED1** | WS2812B-B | Worldsemi | 5050 SMD | C114586 | RGB Status LED for Optical Mode Indication |
| **LP1** | PLPC3-3MM / 1292.1101 | Bivar / Mentor | Ø 3.0 mm PMMA | Mechanical | IP67 Light Pipe with O-Ring in Top Enclosure Lid |
| **VENT1** | AVS 41 | Gore Automotive | M8 x 1.25 Thread | Mechanical | ePTFE Pressure Equalization Element (IP67 / 120 ml/min) |
| **MIC1** | SPH0645LM4H / SiSonic | Knowles | 3.5x2.65 mm SMD | C119850 | IP67 Front Ambient Microphone with ePTFE Vent (Pin 25) |
| **J1** | 2x13 Box Header | Standard 2.54 mm | THT Box Header | C2934175 | Internal Ribbon Header to HD26 Flange Receptacle |
| **J2** | MicroSD Slot Push-Push | Molex / Korean Hro | SMD Push-Push | C266624 | 4-Bit SDIO Storage Card for Tour Logging |
| **J_BAT** | Molex Micro-Fit 3.0 2P | Molex | SMD Header | C289110 | Header for 18650 LiFePO4 Buffer Battery |
| **CN1** | HD26 Receptacle IP67 | Amphenol LTW | Flange D-Sub | Custom | Waterproof 26-pin Central Chassis Interface |

---

## 2. Pod Base PCB (`openmotorbridge_pod_base` PCBA, 2-Layer FR4 ENIG)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **J1** | PinHeader_1x06_P2.54mm_SMD | Harwin / Wurth | SMD Vertical | C2934176 | Centered 6-Pin Pin Header inside Bulkhead Shroud |
| **J2** | M8_6PIN_RECEPTACLE (A-Coded)| Binder / Phoenix | M8 Circular Conn | C289100 | M8 6-Pin IP67 Receptacle for Harness Connection (B.Cu) |
| **U1** | SP3012-06UTG | Littelfuse | DFN-14 (3.5x1.35mm)| C2834580 | 6-Channel Ultra-Low-Cap ESD Protection Array (< 0.5 pF)|
| **C1** | 100nF 50V X7R | Samsung / Yageo | 0603 SMD | C14663 | Decoupling Capacitor for 5V Power Supply |
| **H1, H2** | 2x M2 Mounting Holes | - | Hole Ø 2.2 mm | - | Vibration-Proof Fastening to PA12 Bulkhead Plate |

---

## 3. Universal Cartridge Carrier PCB (`openmotorbridge_pod_cartridge` PCBA, 2-Layer FR4)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **J1** | PinSocket_1x06_P2.54mm_SMD | Harwin / Samtec | SMD Horizontal | C2934177 | Leading-Edge 6-Pin Precision Socket (Piston Slide-In) |
| **J2** | JST-SH 1.0mm 6-Pin Horizontal| JST | SMD Right-Angle | C136657 | Flat-Ribbon Cable Header to Headset Inlay Contacts |
| **U1** | DS2401Z+ | Maxim / ADI | SOT-223 / SOT-23 | C2834570 | 64-Bit 1-Wire Silicon Serial ROM (Cartridge ID) |
| **F1** | MF-MSMF050-2 (500mA) | Bourns | 1812 / 1206 SMD | C22668 | Resettable PPTC Fuse for 5V Cartridge Circuit |
| **D1** | Green 5V Power LED | Everlight | 0805 SMD | C2297 | Visual Status Indication for 5V Power Supply |
| **R1** | 1.0 kΩ 1% | Yageo | 0603 SMD | C21190 | Current Limiting Resistor for Status LED D1 |
| **D2** | SP3012-06UTG / IP4220CZ6 | Littelfuse / Nexperia| DFN-14 / SOT-457 | C2834580 | 6-Channel ESD Protection Matrix for Internal Lines |

---

## 4. Rear Pod 3 Transceiver PCB (`openmotorbridge_rear_pod3` PCBA, 4-Layer FR4 TG150)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U10** | ESP32-C3-WROOM-02-N4 | Espressif Systems | SMD Module | C2868705 | 32-Bit RISC-V Co-Processor & 2.4 GHz Primary Mesh |
| **U11** | MAX-M10S-00B | u-blox | LGA-18 | C3006240 | Multi-Constellation GNSS Engine (10 Hz, 1-PPS) |
| **U12** | SX1262IMLTRT | Semtech | QFN-24 | C190184 | Secondary Fallback 868 MHz LoRa Transceiver (+22 dBm) |
| **U13** | DS2401Z+ | Maxim / ADI | SOT-223 / SOT-23 | C2834570 | 64-Bit 1-Wire Silicon Serial Number ID |
| **U14** | TPS7A0533PDBVR | Texas Instruments | SOT-23-5 | C505293 | Ultra-Low-Noise 3.3V LDO (200 mA) for GNSS & LoRa |
| **J1** | PinSocket_1x06_P2.54mm_SMD | Harwin / Samtec | SMD Horizontal | C2934177 | Leading-Edge 6-Pin Precision Socket (Piston Slide-In) |
| **F1** | MF-MSMF050-2 (500mA) | Bourns | 1812 SMD | C22668 | Resettable PPTC Fuse for 5V Power Supply |
| **D1** | Green 5V Power LED | Everlight | 0805 SMD | C2297 | Visual Status Indication for 5V Power Supply |
| **ANT1** | GP.1575.25.4.A.02 | Taoglas | 25x25x4 mm Patch | C2689100 | Ceramic Patch Antenna for GPS/Galileo/BeiDou |
| **ANT2** | ANT-868-CW-HWR-SMA | Linx / Taoglas | Helical Antenna | C290111 | 868 MHz Helical Antenna for Tail-Rack LoRa |
| **ANT3** | WLS.01.A.02 | Taoglas | 3.2x1.6 mm Chip | C2838381 | 2.4 GHz Ceramic Antenna for Primary HiFi Mesh |

---

## 5. Mechanical BOM (3D Printed MJF PA12 & Hardware Fasteners)

### 5.1 Main Central Box (3-Piece Sandwich Enclosure Type A)
| Component / Subassembly | Material / Specification | CAD / STL File | Qty | Function |
| :--- | :--- | :--- | :---: | :--- |
| **Lower Base Tub** | PA12 MJF Black | `main_box_lower_case.stl` | 1 | Monocoque base case with gasket groove & 4x M4 silentblock ears |
| **Upper Deck with Divider** | PA12 MJF Black | `main_box_upper_case.stl` | 1 | Battery bay, 11x convection slots, HD26 flange, USB-C & LED |
| **Enclosure Top Lid** | PA12 MJF Black | `main_box_lid.stl` | 1 | Homogeneous cover lid with ePTFE vent seat |
| **Case Fastening Screws** | Stainless V4A M3 x 40 mm DIN 912 | Standard Part | 4 | Continuous 4-corner clamp fastening |
| **Threaded Inserts** | Brass M3 Ruthex / Tappex | Standard Part | 4 | Heat-set into lower base tub corner pillars |
| **Venting Element** | Gore Automotive AVS 41 (M8) | Commercial Off-The-Shelf| 1 | IP67 pressure balance & condensation prevention |
| **Chassis Gasket** | Silicone Shore 50A (1.5 mm Cord) | Custom Molded | 1 | Hermetic IP67/IP69K sandwich seal |
| **Light Pipe** | PMMA Ø 3.0 mm (Bivar PLPC3) | Commercial Off-The-Shelf| 1 | Optical light guide for WS2812B in enclosure lid |

### 5.2 Universal Satellite Pods (3x Identical for Pod 1, 2, and 3)
| Component / Subassembly | Material / Specification | CAD / STL File | Qty | Function |
| :--- | :--- | :--- | :---: | :--- |
| **Pod Monocoque Tunnel** | PA12 MJF Black | `pod_base_housing.stl` | 3 | 5-sided tunnel housing with V-groove & 4x EPDM strap lugs |
| **Protective Bulkhead** | PA12 MJF Black | `pod_bulkhead_plate.stl` | 3 | Bulkhead with 6-pin shroud funnel & spring seats |
| **Auto-Eject Compression Springs**| Stainless V4A (D=4.5mm, L0=15mm)| Standard Part | 6 | Ejection mechanism (10 mm cartridge pop-out stroke) |
| **Bulkhead Screws** | Stainless V4A M2 x 8 mm Flat-Head| Standard Part | 6 | 2x screws per pod to secure bulkhead plate |
| **Helmet Clamp Adapter** | PA12 MJF Black | `pod_mount_helmet_clamp.stl` | 2 | Universal helmet clamp mount for Pod 1 & Pod 2 |
| **GoPro / Rack Mount Plate** | PA12 MJF Black | `pod_mount_gopro_rack.stl` | 1 | 3x GoPro tabs for rear fender / luggage rack mount |

### 5.3 Modular Swappable Cartridges & Inlays
| Component / Subassembly | Material / Specification | CAD / STL File | Qty | Function |
| :--- | :--- | :--- | :---: | :--- |
| **Universal Carrier Sled** | PA12 MJF Black | `cartridge_base_sled.stl` | 3 | Universal carrier sled with Poka-Yoke guide rails |
| **Sena 50S/60S 3D Cradle** | PA12 MJF Black | `cartridge_sena.stl` | 1 | Module top cradle with Jog-Dial lock & pogo nest |
| **Cardo Edge Air-Mount Cradle** | PA12 MJF Black | `cartridge_cardo.stl` | 1 | Module top cradle with 2x N52 magnet pockets |
| **OMM Transceiver Sled** | PA12 MJF Black | `cartridge_omm_transceiver.stl`| 1 | Monolithic 1-tier sled for direct Pod 3 PCB |
| **IP67 Blind Cartridge (Dry Box)**| PA12 MJF Black | `cartridge_blindkassette.stl` | 1 | Hermetic dummy sled with emergency storage cavity |
| **Cartridge Flange Gaskets**| Shore 40A Silicone Molded | Commercial / Molded | 3 | Perimeter IP67 sealing at front bezel |
| **ePTFE Venting Membrane** | Gore Adhesive Vent Ø 6.0 mm | Commercial Off-The-Shelf| 3 | Pneumatic venting during cartridge insertion |

---

## 6. Manufacturing Notes, Conformal Coating & Vibration Hardening

### 6.1 Conformal Coating per IPC-CC-830B
* **Coating Compound:** Modified Polyurethane coating (*Peters Elpeguard SL 1307 FLZ* or *Electrolube UR5041*).
* **Layer Thickness:** $40\,\mu\text{m}$ to $60\,\mu\text{m}$ (Dielectric breakdown strength $> 60\,\text{kV/mm}$).
* **Masking Zones:** MicroSD slot contacts, SMD testpoints (TP1–TP8), ePTFE vent orifice, 6-pin precision contacts.

### 6.2 Vibration Damping per ISO 16750-3 (Motorcycle Vibration Profile)
* **PCB Decoupling:** 4x NBR O-rings (3.0 mm ID, 1.0 mm cord) between mounting bosses and PCB underside.
* **Screw Locking:** M2.5 board screws torqued to $0.35\,\text{Nm}$ with medium-strength threadlocker (*Loctite 243* blue).
* **Component Underfill:** Bourns LM-NP-1001 transformer corners bonded with elastic silicone adhesive (*Dow Corning 732* / *Dowsil 3145*).
* **Buffer Battery Retention:** $1.0\,\text{mm}$ damping pad (*3M VHB 4910* / EPDM) and elastic EPDM strap (Shore 50A) in the upper deck tray.

---

## 7. Commissioning, Measurement & Verification Protocol

### Step 1: Visual Inspection (Prior to Initial Power-Up)
* [ ] Solder bridges under U2 (LM5164), U3 (BQ24075) and U5 (ES8388) ruled out with microscope/loupe.
* [ ] Polarity of TVS diode D1 (SMBJ33CA) and P-FET reverse polarity protection verified.
* [ ] Verify that 2.5 mm isolation barrier around T1/T2 and OC1/OC2 is free of solder splashes or flux residues.

### Step 2: Voltage & Current Limit Test
* [ ] Bench power supply set to $12.0\,\text{V DC}$, current limit set to $150\,\text{mA}$.
* [ ] Quiescent current measured: Target $= 45\,\text{mA}$ to $75\,\text{mA}$ (without battery charge).
* [ ] Testpoint `TP_5V`: Target $= 5.15\,\text{V} \pm 0.05\,\text{V}$.
* [ ] Testpoint `TP_3V3`: Target $= 3.30\,\text{V} \pm 0.02\,\text{V}$.

### Step 3: Firmware Flashing & System Self-Test
* [ ] ESP-IDF / PlatformIO flash via native USB-C port executed (`firmware/main_controller/`).
* [ ] LittleFS partition formatted and profiles uploaded from `firmware/main_controller/data/profiles/`.
* [ ] Serial console ($115,200\,\text{Baud}$): Messages "LittleFS Mount OK", "1-Wire Manager Task OK", "I2S ES8388 Codec Init OK", "TCAN334G CAN-FD OK" verified.

### Step 4: Audio & Ducking Functional Verification
* [ ] $1\,\text{kHz}$ sine wave ($1.0\,\text{V}_{\text{RMS}}$) applied to audio input.
* [ ] Oscilloscope at `PORT1_AUDIO_OUT`: Verify signal ducks smoothly within $15\,\text{ms}$.
* [ ] Signal cut: Verify that after $600\,\text{ms}$ hold time, a soft $250\,\text{ms}$ raised-cosine release occurs.

### Step 5: IP67 Pressure Leak Test
* [ ] Assembled enclosure placed in vacuum chamber at $-20\,\text{kPa}$ for 60 seconds (pressure drop $< 0.5\,\text{kPa}$).

---

## 8. Step-by-Step Ordering Guide for JLCPCB (PCBA & SMT Assembly)

All production-ready manufacturing packages can be generated automatically via `python3 hardware/scripts/export_manufacturing_packages.py` into the [hardware/production_packages/](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/) directory.

### 8.1 Checklist for JLCPCB Upload (All 4 Circuit Boards)

| Subassembly / PCBA | Gerber ZIP File | BOM CSV File | CPL (Pick & Place) CSV | Layers & Stackup | Surface Finish & Thickness |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **1. Central Main Box PCB** | `01_main_box_pcba_gerbers_jlcpcb.zip` | `01_main_box_pcba_bom_jlcpcb.csv` | `01_main_box_pcba_cpl_jlcpcb.csv` | **4 Layers** (JLC04161H-7628) | **ENIG (Gold)**, 1.6 mm, TG150 |
| **2. Pod Base PCB** | `02_pod_base_pcba_gerbers_jlcpcb.zip` | `02_pod_base_pcba_bom_jlcpcb.csv` | `02_pod_base_pcba_cpl_jlcpcb.csv` | **2 Layers** (Standard) | **ENIG (Gold)**, 1.6 mm |
| **3. Cartridge Carrier PCB**| `03_pod_cartridge_pcba_gerbers_jlcpcb.zip` | `03_pod_cartridge_pcba_bom_jlcpcb.csv` | `03_pod_cartridge_pcba_cpl_jlcpcb.csv` | **2 Layers** (Standard) | **ENIG (Gold)**, 1.2 mm |
| **4. Rear Pod 3 Transceiver**| `04_rear_pod3_pcba_gerbers_jlcpcb.zip` | `04_rear_pod3_pcba_bom_jlcpcb.csv` | `04_rear_pod3_pcba_cpl_jlcpcb.csv` | **4 Layers** (JLC04161H-7628) | **ENIG (Gold)**, 1.6 mm, TG150 |

### 8.2 Options to Select in JLCPCB Web Configurator:
1. **PCB Order:**
   * **Base Material:** FR-4 (TG150 for Main Box & Pod 3).
   * **Surface Finish:** **ENIG (Electroless Nickel Immersion Gold)** – strictly required for corrosion-proof contact wiping and vibration-resistant QFN joints.
   * **Solder Mask Color:** Matte Black or Green.
   * **Via Covering:** *Tented* or *Filled & Capped* (under exposed thermal pads).
2. **SMT Assembly:**
   * Enable **"PCB Assembly"**.
   * **Assembly Side:** *Top Side* (or *Both Sides* for Main Box).
   * **Upload BOM & CPL:** Upload the generated `*_bom_jlcpcb.csv` and `*_cpl_jlcpcb.csv`.
   * **Verify DFM Preview:** Visually verify Pin 1 orientation for Bourns transformers (T1/T2), optocouplers (OC1/OC2), and ESP32-S3.

---

## 9. Central Wiring Harness Manufacturing (HD26 Breakout Pigtail)

The central wiring harness bridges the under-seat Central Box to the 3 satellite pods, 12V vehicle power, and CAN-bus / front microphone.

### 9.1 Contract Manufacturing (JLCPCB Wire Harness / Cabelcon / Sinohand)
Submit [central_breakout_harness_wirelist.csv](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/05_wiring_harness/central_breakout_harness_wirelist.csv) directly to the cable assembly house.

```
                               CENTRAL HD26 BREAKOUT HARNESS
┌─────────────────────────┐
│ HD26 IP67 Male Plug     │ ──► Branch Pigtail Length: 250 mm each (sheathed in black PET braid)
│ (Amphenol LTW / D-Sub)  │ ──► Y-Junction sealed with hotmelt adhesive / heatshrink cap
└─┬───────────────────────┘
  ├─► BRANCH 1 (250 mm): M8 6-Pin Receptacle (A-coded, IP67) ──► Pod 1 (Rider Helmet Left)
  ├─► BRANCH 2 (250 mm): M8 6-Pin Receptacle (A-coded, IP67) ──► Pod 2 (Pillion Helmet Right)
  ├─► BRANCH 3 (250 mm): M8 6-Pin Receptacle (A-coded, IP67) ──► Pod 3 (Rear OMM & GNSS)
  ├─► BRANCH 4 (250 mm): AMP Superseal 1.5 4-Pin Receptacle  ──► 12V Vehicle Power (KL30, KL15, GND)
  └─► BRANCH 5 (250 mm): M8 4-Pin Receptacle (A-coded, IP67) ──► CAN-Bus & IP67 Front Microphone
```

### 9.2 DIY Assembly Guide for Prototyping (Workbench Setup):
1. **Prepare Materials:**
   * 1x HD26 D-Sub solder-cup plug with IP67 metal backshell.
   * 3x M8 6-Pin female pigtails (25 cm cut lead with color-coded conductors).
   * 1x M8 4-Pin female pigtail (for CAN / microphone).
   * 1x AMP Superseal 1.5 4-Pin connector housing with crimp pins.
   * 3:1 dual-wall heatshrink tubing with hotmelt adhesive.
2. **Solder to Pinout Schedule:**
   * Solder wires to cups 1..26 according to [central_breakout_harness_wirelist.csv](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/05_wiring_harness/central_breakout_harness_wirelist.csv).
   * Twist audio wire pairs (3/4 and 9/10) and CAN pairs (23/24).
3. **Strain Relief & Sealing:**
   * Pot solder cups with neutral-cure RTV silicone / potting resin.
   * Fasten thumbscrews and seal the cable exit with adhesive-lined heatshrink.

---

## 10. 3D Printing Production Order (HP Multi Jet Fusion PA12)

All 3D printing STL bundles are organized in [hardware/production_packages/06_3d_print_mjf_stls/](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/06_3d_print_mjf_stls/):

### 10.1 Order Packages:
1. **`01_main_box_3d_print_mjf.zip`:**
   * `main_box_lower_case.stl` (1x)
   * `main_box_upper_case.stl` (1x)
   * `main_box_lid.stl` (1x)
2. **`02_satellite_pods_3d_print_mjf.zip`:**
   * `pod_base_housing.stl` (3x – for Pod 1, 2, and 3)
   * `pod_bulkhead_plate.stl` (3x – for Pod 1, 2, and 3)
   * `pod_mount_helmet_clamp.stl` (2x – for Pod 1 and 2 on helmet)
   * `pod_mount_gopro_rack.stl` (1x – for Pod 3 on tail rack)
3. **`03_cartridges_and_inlays_3d_print_mjf.zip`:**
   * `cartridge_base_sled.stl` (3x)
   * `cartridge_sena.stl` (1x)
   * `cartridge_cardo.stl` (1x)
   * `cartridge_omm_transceiver.stl` (1x)
   * `cartridge_blindkassette.stl` (1x)

### 10.2 Material Recommendations:
* **Process:** **HP Multi Jet Fusion (MJF)** or **SLS (Selective Laser Sintering)**.
* **Material:** **PA12 (Polyamide 12) Black**, bead blasted.
* **Finish:** **Chemical Vapor Smoothing** – seals all microscopic surface pores against gasoline, brake fluid, chain lube, and high-pressure water jets (IP69K).

---

## 11. COTS Fasteners & Hardware Procurement List

| Component | Specification / Type | Supplier / Manufacturer | Qty | Function |
| :--- | :--- | :--- | :---: | :--- |
| **M3 Case Screws** | M3 x 40 mm Socket Head V4A (DIN 912) | Standard Fastener | 4 pcs | 4-Corner Central Box clamping |
| **M3 Threaded Inserts**| Ruthex M3 x 5.7 mm Brass | Ruthex / Amazon | 4 pcs | Heat-set inserts in lower base tub |
| **M2 Bulkhead Screws** | M2 x 8 mm Flat Head V4A (DIN 7991) | Standard Fastener | 6 pcs | Secures 3x pod bulkhead plates |
| **Ejection Springs** | Stainless V4A ($D=4.5\,\text{mm}, L_0=15\,\text{mm}, R=1.2\,\text{N/mm}$) | Gutekunst Federn / Sodemann | 6 pcs | Auto-Eject mechanism (2x per pod) |
| **EPDM Tension Rings / Straps**| UV- & Ozone-Resistant EPDM ($\varnothing 45\dots 75\,\text{mm}$) | QuadLock / O-Ring-Shop / Amazon | 6 pcs | Universal tube saddle quick mount (2x per pod) |
| **UV Cable Ties (Theft Protection)**| $4.8 \times 200\,\text{mm}$ Polyamide 6.6 Black | HellermannTyton / Würth | 6 pcs | Permanent fixed frame mounting |
| **Gore Vent Valve** | Gore Automotive AVS 41 (M8x1.25) | W. L. Gore & Associates | 1 pc | Central box lid pressure venting |
| **Gore Vent Stickers** | Gore Adhesive Vent $\varnothing 6.0\,\text{mm}$ IP67 | W. L. Gore & Associates | 3 pcs | Pod pressure venting (1x per pod) |
| **Light Pipe** | PMMA $\varnothing 3.0\,\text{mm}$ (Bivar PLPC3-3MM) | Bivar / Mouser / Digikey | 1 pc | LED status window in top lid |
| **Buffer Battery** | 18650 LiFePO4 (3.2V 1500mAh) / LiPo 1S | EEMB / Enerpower | 1 pc | UPS battery backup |
| **M8 Extension Cables** | M8 6-Pin A-Coded PUR shielded (1.0m / 1.5m) | Binder / Phoenix / Murr / LCSC | 3 pcs | Harness-to-pod extension lines |

