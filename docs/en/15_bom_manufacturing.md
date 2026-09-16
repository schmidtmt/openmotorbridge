# 15 - Bill of Materials (BOM) & SMT Manufacturing (All 7 PCBAs)

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

## 3. PCBA 03: Smart Modular Cartridge Rev 2.0 (`openmotorbridge_pod_cartridge`, 2-Layer FR4)

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

## 5. PCBA 05: Universal Front Node (`openmotorbridge_front_node`, 4-Layer FR4 TG150, 82 x 50 mm)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | ESP32-S3-WROOM-1U-N8R8 | Espressif Systems | SMD Module | `C2913200` | Dual-Core 32-Bit Xtensa LX7 (240 MHz, Vector-DSP, 8MB PSRAM, ext. U.FL) |
| **U2** | USB2514B-AEZG | Microchip | QFN-36 | `C97185` | Automotive USB 2.0 High-Speed 480 Mbps 4-Port Hub Controller |
| **U3** | LMR36015FSCQRNXRQ1 | Texas Instruments | VQFN-12 | `C2843480` | Automotive 36V Synchronous Buck (5V / 2.0A, 91.8%) for Hub & Peripherals |
| **U4** | TPS2051BDBVR | Texas Instruments | SOT-23-5 | `C7818` | High-Side USB VBUS Power Switch (1.05A Clamp) for Port 2 Cold-Reboot Reset |
| **U5** | SC8102QDER | Southchip | QFN-32 | `C2843510` | Automotive Synchronous Buck with USB-PD 20W (9V/2.2A & QC3.0) for Smartphone Port 1 |
| **U6** | TCAN334GDCNT | Texas Instruments | SOT-23-8 | `C2843515` | 3.3V CAN Transceiver (5 Mbps CAN-FD capable, with Pin 8 Silent-Listen-Only Mode) |
| **K1** | CPC1017NTR | IXYS / Littelfuse | SOP-4 | `C26789` | 60V / 100mA 1-Form-A Solid-State Relay for switchable 120R CAN Termination (Auto-Sensing) |
| **Q1** | DMN63D8LDW-7 | Diodes Incorporated| SOT-363 | `C283890` | Dual N-Channel MOSFET (30V / 260mA) for directional mirror blind-spot LEDs (J9) |
| **Q2** | TPS1H100BQPWPRQ1 | Texas Instruments | HTSSOP-14 | `C2843520` | Automotive Smart High-Side Power Switch (up to 3.5A / 40W) for 12V Aux Light (J11) |
| **LED1**| WS2812B-2020 | Worldsemi | SMD 2020 | `C2843530` | Digitally controllable RGB status LED for enclosure lid light pipe |
| **MIC1**| SPH0645LM4H-B | Knowles | 3.5x2.65 mm SMD | `C119850` | Digital I2S MEMS Acoustic Microphone for wind noise & dynamic pressure measurement |
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
| **J10** | JST-PH 2-Pin Header | JST | 2.00mm SMD | `C289115` | 12V Qi Wireless Charging (SP Connect / QuadLock Head) |
| **J11** | JST-PH 2-Pin Header | JST | 2.00mm SMD | `C289115` | 12V Aux Light (Adventure Auxiliary Spotlight / Emergency Brake Strobe) |
| **J12** | JST-SH 4-Pin Header | JST | 1.00mm SMD | `C289118` | Qwiic / STEMMA QT I2C Sensor Port (3.3V, GND, SDA, SCL) |

--## 6. Mechanical & Enclosure BOM (MJF PA12 3D Printing & Hardware)

All enclosure parts are optimized for the **IKEA Principle**: **No heat-set brass threaded inserts or soldering irons required!** The enclosures integrate captive hexagonal nut pockets (Nut Pockets for standard DIN 934 / DIN 985 stainless nuts) and direct piloting for plastics.

### 6.1 Base System (Universal for Every Motorcycle)
| Assembly | STL Filename | Qty | Material & Process | Function & Description |
| :--- | :--- | :---: | :--- | :--- |
| **Main Box Lower Tub** | [`main_box_lower_case.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lower_case.stl) | **1** | MJF PA12 / ASA | Monocoque lower tub with 4x M4 silentblock ears, nut pockets & seal groove |
| **Main Box Mid Tray** | [`main_box_mid_tray.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_mid_tray.stl) | **1** | MJF PA12 / ASA | Battery tray for 1000 mAh LiPo, 10x convection louvers & tongue-and-groove lip |
| **Main Box Lid** | [`main_box_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lid.stl) | **1** | MJF PA12 / ASA | Enclosure lid with Gore ePTFE valve dome & bolt counterbores |
| **Pod Base Housing** | [`pod_base_housing.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod_base_housing.stl) | **3** | MJF PA12 / ASA | Universal chassis housing for Pod 1 (Left), Pod 2 (Right), and Rear Pod 3 |
| **Pod Bulkhead Partitions**| [`03_pod_bulkhead_partition.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl) | **3** | MJF PA12 / ASA | Bulkhead partition with sealing collar & spring pockets (1 per pod) |
| **Cartridge Base Sled** | [`cartridge_base_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl) | **3** | MJF PA12 / ASA | Universal sled for Gateway 1 (Pod 1), Gateway 2 (Pod 2), and OMM (Pod 3) |
| **Cartridge Magnetic Latch**| [`cartridge_magnetic_lock_latch.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_magnetic_lock_latch.stl) | **2** | MJF PA12 / ASA | Magnetic anti-theft locking rocker latches for Cartridge Slots 1 & 2 |
| **Rear Pod 3 OMM Radome** | [`cartridge_antenna_bracket_omm.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_antenna_bracket_omm.stl) | **1** | MJF PA12 / ASA | Dielectric antenna radome & carrier bridge for PCBA 04 in Rear Pod 3 |
| **Front Node Lower Tub** | [`front_node_lower_tub.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_lower_tub.stl) | **1** | MJF PA12 / ASA | Cockpit tub with AMPS bolt pattern, tube cradle & nut pockets |
| **Front Node Lid** | [`front_node_upper_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_upper_lid.stl) | **1** | MJF PA12 / ASA | Lid with Knowles MEMS acoustic port & perimeter O-ring groove |
| **Front Node Cable Glands**| [`front_node_cable_glands_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_cable_glands_tpu.stl) | **1 Pair**| TPU 95A / 85A | Elastomeric sealing combs for front USB & lateral signals |
| **Front Node USB-C Cap** | [`front_node_usbc_cap_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_usbc_cap_tpu.stl) | **1** | TPU 95A / 85A | Elastomeric dust cap with retention tether for service port |

### 6.2 Gateway Cartridge Inlays (Choose 2 Based on Desired Intercoms)
> **Architecture Principle:** Slot 1 and Slot 2 are **Multi-Protocol Gateway Transceivers**, not isolated driver/passenger headsets! They connect the motorcycle simultaneously to Sena Mesh and Cardo DMC networks. Driver and passenger communicate wirelessly using their standard helmets.

| Assembly | STL Filename | Qty | Material | Function & Description |
| :--- | :--- | :---: | :--- | :--- |
| **Gateway Inlay Sena** | [`cartridge_insert_sena.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) | *Opt. (1)* | MJF PA12 / ASA | Form-fitting inlay for Sena SPIDER X Slim / 50S / 60S (Mesh 3.0 Wave) |
| **Gateway Inlay Cardo** | [`cartridge_insert_cardo.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl) | *Opt. (1)* | MJF PA12 / ASA | Inlay for Cardo Packtalk Edge / Pro (DMC Gen2) with Air-Mount |
| **Blank Cartridge / Dry Box**| [`cartridge_insert_blindkassette.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_blindkassette.stl) | *Opt. (1)* | MJF PA12 / ASA | Hermetic protective sled for unused slot or waterproof dry storage box |

### 6.3 Vehicle-Specific Mounting Kits (3D Printed Parts)
* **Kit 1: BMW R1250 / R1300 GS (Standard / Vario Cases):**
  * `adventure_transition_dock.stl` (2 pcs): Luggage-independent docks in the seat crease (Ø 28 mm frame tube).
  * `adventure_rack_tail_mount.stl` (1 pc): Luggage rack cantilever for Pod 3 & radar.
  * `radar_varia_gopro_lock_dock.stl` (1 pc) & `011_gopro_hirth_lock.stl` (1 pc): Radar bayonet dock with 36-tooth Hirth gear lock.
* **Kit 2: BMW R1250 / R1300 GSA (Adventure with Ø 18 mm Stainless Pannier Rack Cage):**
  * `adventure_pannier_rack_clamp_base.stl` & `adventure_pannier_rack_clamp_cap.stl` (4 pairs): Heavy-duty clamp pairs for Pod 1 & 2 in the pannier rack cage triangle.
  * `adventure_rack_tail_mount.stl` (1 pc): Tail Balcony behind aluminum topcase with 45° branch deflector fin for dipole antenna.
  * `radar_varia_gopro_lock_dock.stl` (1 pc) & `011_gopro_hirth_lock.stl` (1 pc): Radar dock with Hirth gear lock.
* **Kit 3: Harley-Davidson Touring & Classic Bagger (Street Glide, Road Glide, Road King):**
  * `saddlebag_lid_dock.stl` (2 pcs): Saddlebag lid mounting docks for Pod 1 & 2.
  * `pod3_touring_fender_console.stl` (1 pc): Organic rear fender console for Pod 3 (Road King Special).
  * `radar_license_plate_bracket.stl` (1 pc): Decoupled license plate radar mount.
* **Kit 4: Harley-Davidson CVO ST & Performance Bagger (Road Glide ST):**
  * `saddlebag_lid_dock.stl` (2 pcs): Saddlebag lid mounting docks for Pod 1 & 2.
  * `cvo_st_undercowl_skeleton_dock.stl` (1 pc): Upright spring-preloaded dock for Pod 3 under forged carbon solo seat cowl.
  * `cvo_st_telemetry_fin.stl` (1 pc): Aerodynamic tail fin / telemetry radome on rear tab.
  * `radar_center_underfender_mount.stl` (1 pc): Centered under-fender plate for radar (avoids Showa remote reservoirs).
* **Kit 5: Universal (Other Motorcycles):**
  * Standard 120° V-cradle on Pod base housing for frame tubes (Ø 22–32 mm) with EPDM strap rings or M4 silentblocks.

### 6.4 Accessories (Optional)
| Assembly | STL Filename | Qty | Material | Function & Description |
| :--- | :--- | :---: | :--- | :--- |
| **Smart Keyfob Lower Shell**| [`smart_keyfob_lower_shell.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/smart_keyfob_lower_shell.stl) | **1** | MJF PA12 / ASA | Tub with LRA dampening cradle & magnet pocket for PCBA 07 |
| **Smart Keyfob Upper Shell**| [`smart_keyfob_upper_shell.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/smart_keyfob_upper_shell.stl) | **1** | MJF PA12 / ASA | Lid with 3 button keypads & optical light pipe port |
| **Smart Keyfob Bumper** | [`smart_keyfob_tpu_rim.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/smart_keyfob_tpu_rim.stl) | **1** | TPU 85A / 95A | Shock-absorbing perimeter rim |

---

## 7. Commissioning & Test Protocol (100% Solder-Free)

Because all circuit boards are factory-assembled and pre-tested, commissioning is reduced to a straightforward functional verification:

### Step 1: Physical Check & Visual Inspection
* [ ] Inspect all PCBAs for transit damage.
* [ ] Verify silicone gaskets seat cleanly in the enclosure channels.

### Step 2: Bench Power-Up with Power Supply or Bike Battery
* [ ] Connect 12V supply wire (fused via inline 2A automotive blade fuse).
* [ ] Verify quiescent current: Expected $= 45\,\text{mA}$ to $75\,\text{mA}$ (without battery charging).
* [ ] Status LEDs on Central Box and Front Node illuminate solid green.

### Step 3: Firmware Self-Test & WebApp Connection
* [ ] Connect smartphone / PC to WiFi `OpenMotorBridge-Setup`.
* [ ] Open PWA dashboard in browser (`http://192.168.4.1`).
* [ ] Status check: Both gateway slots (Pod 1 & Pod 2) identified, Rear Pod 3 reports GNSS 3D fix.

---

## 8. 1-Click JLCPCB Ordering Guide (All Circuit Boards Pre-Assembled)

All manufacturing files are available in the repository as ready-to-upload ZIP and CSV archives:

| Subassembly / PCBA | Gerber ZIP Archive | BOM CSV File | CPL (Pick & Place) CSV | Layers | Manufacturing Notes |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **1. Central Box Main Board** | `01_main_box_pcba_gerbers_jlcpcb.zip` | `01_main_box_pcba_bom_jlcpcb.csv` | `01_main_box_pcba_cpl_jlcpcb.csv` | **4 Layers** | ENIG (Gold), 1.6 mm, TG150, SMT top & bottom |
| **2. Pod Base Board** | `02_pod_base_pcba_gerbers_jlcpcb.zip` | `02_pod_base_pcba_bom_jlcpcb.csv` | `02_pod_base_pcba_cpl_jlcpcb.csv` | **2 Layers** | ENIG (Gold), 1.6 mm, SMT top |
| **3. Cartridge Carrier Board**| `03_pod_cartridge_pcba_gerbers_jlcpcb.zip` | `03_pod_cartridge_pcba_bom_jlcpcb.csv` | `03_pod_cartridge_pcba_cpl_jlcpcb.csv` | **2 Layers** | ENIG (Gold), 1.2 mm, SMT top |
| **4. Rear Pod 3 Transceiver** | `04_rear_pod3_pcba_gerbers_jlcpcb.zip` | `04_rear_pod3_pcba_bom_jlcpcb.csv` | `04_rear_pod3_pcba_cpl_jlcpcb.csv` | **4 Layers** | ENIG (Gold), 1.6 mm, TG150, SMT top |
| **5. Universal Front Node** | `05_front_node_pcba_gerbers_jlcpcb.zip` | `05_front_node_pcba_bom_jlcpcb.csv` | `05_front_node_pcba_cpl_jlcpcb.csv` | **4 Layers** | ENIG (Gold), 1.6 mm, TG150, SMT top & bottom |
| **7. Smart Keyfob (Accessory)**| `07_smart_keyfob_pcba_gerbers_jlcpcb.zip` | `07_smart_keyfob_pcba_bom_jlcpcb.csv` | `07_smart_keyfob_pcba_cpl_jlcpcb.csv` | **2 Layers** | ENIG (Gold), 1.0 mm, SMT top & bottom |

---

## 9. Pre-Molded COTS Cabling (No Crimping, No Soldering!)

Riders **never need to crimp or solder wiring harnesses**. The system relies 100% on standard commercial off-the-shelf (COTS) molded cables:

```
                      THE PLUG-AND-PLAY CABLING ARCHITECTURE (COTS PRE-MOLDED)
┌─────────────────────────┐
│ HD26 IP67 Harness Whip  │ ──► Factory pre-molded HD26 breakout harness (Amphenol LTW COTS)
│ (Central Box Main Port) │ ──► No discrete wire termination, 100% waterproof overmolded
└─┬───────────────────────┘
  ├─► M8 6-Pin PUR Cable (1.0 m / 1.5 m): Standard sensor/actuator cable ──► Pod 1 (Gateway 1)
  ├─► M8 6-Pin PUR Cable (1.0 m / 1.5 m): Standard sensor/actuator cable ──► Pod 2 (Gateway 2)
  ├─► M8 6-Pin PUR Cable (1.5 m / 2.0 m): Standard sensor/actuator cable ──► Pod 3 (Rear Transceiver)
  ├─► AMP Superseal 12V Cable (1.0 m): Pre-terminated battery wire with blade fuse ──► 12V Bike Supply
  └─► M8 4-Pin PUR Cable (1.5 m): Shielded CAN/Front umbilical cable ──► Front Node (Cockpit)
```

---

## 10. Hardware & Standard Parts Procurement List (1 Complete System)

| Component | Specification / Type | Supplier / Reference | Quantity | Location & Function |
| :--- | :--- | :--- | :---: | :--- |
| **M3 Stainless Screws** | M3 x 40 mm Socket Head V4A (DIN 912) | Standard Hardware | 4 pcs | Central Box Enclosure (threads into Nut-Pockets) |
| **M3 Screws (Front Node)**| M3 x 20 mm Socket Head V4A (DIN 912) | Standard Hardware | 4 pcs | Front Node Enclosure (threads into Nut-Pockets) |
| **M3 Stainless Nuts** | DIN 934 / DIN 985 M3 V4A Nuts | Standard Hardware | 8 pcs | Captive in Nut-Pockets (no soldering iron needed!) |
| **M2.5 PCB Screws** | M2.5 x 6 mm Socket Head V4A (DIN 912) | Standard Hardware | 8 pcs | 4x Central Box PCBA, 4x Front Node PCBA |
| **M2 Bulkhead Screws** | M2 x 8 mm Countersunk V4A (DIN 7991) | Standard Hardware | 6 pcs | Secures 3 Pod bulkheads (2 per pod) |
| **M2 Cartridge Bracket Screws**| M2 x 6 mm Countersunk V4A (DIN 7991) | Standard Hardware | 8 pcs | Secures actuator retainer plates (4 per gateway) |
| **M2 Rocker Hinge Pins** | M2 x 8 mm Dowel Pin Stainless (DIN 7) | Standard / Misumi | 2 pcs | Pivot pins for magnetic cartridge latches |
| **Magnetic Armature Pin** | Ø 6 x 8 mm Hardened Steel Pin (DIN 6325) | Standard / Misumi | 2 pcs | Steel armature in cartridge rocker arm |
| **Rocker Return Springs** | Stainless V4A ($\varnothing 3.5\,\text{mm}, L_0=10\,\text{mm}$) | Gutekunst / Web | 2 pcs | Return spring for cartridge locking claw |
| **Ejector Compression Springs**| Stainless V4A ($D=4.5\,\text{mm}, L_0=15\,\text{mm}$) | Gutekunst / Web | 6 pcs | Auto-eject springs in bulkheads (2 per pod) |
| **N52 Magnetic Key** | N52 Neodymium Block ($20 \times 10 \times 5\,\text{mm}$) | Supermagnete / Web | 1 pc | Contactless key for cartridge ejection |
| **Rubber Silentblocks** | Type A M4 Male/Female ($\varnothing 15 \times 10\,\text{mm}$) | Standard Hardware | 4 pcs | Vibration-isolated frame mount for Central Box |
| **Silicone Gasket Cord** | Silicone Solid Cord $\varnothing 1.5\,\text{mm}$ Shore 40A (1.0 m) | Standard O-Ring Shop | 1 pc | $40\,\text{cm}$ Central Box groove, $30\,\text{cm}$ Front Node groove |
| **Cartridge Flange Seals** | Molded Silicone Face Seal Shore 40A ($54 \times 18\,\text{mm}$) | Custom / Silicone | 3 pcs | Front face seal on Pods 1, 2, and 3 |
| **Backup Battery (LiPo UPS)**| 1S LiPo (3.7V 1000mAh) with Micro-Fit plug | EEMB / Enerpower | 1 pc | Seamless UPS reserve in Central Box |
| **Automotive Fuse Holder** | Waterproof inline blade fuse holder + 2A fuse | Hella / MTA | 1 pc | Battery-terminal protection for KL30 |
| **M8 6-Pin Pre-Molded Cable**| M8 6-Pin A-Coded Male/Female (1.0m / 1.5m PUR) | Binder / Phoenix | 3 pcs | Plug-and-play connection to Pods 1, 2, and 3 |
| **M8 4-Pin Pre-Molded Cable**| M8 4-Pin A-Coded Male/Female (1.5m PUR) | Binder / Phoenix | 1 pc | Plug-and-play connection to Front Node |
| **J_ACT Actuator Harness** | Pre-crimped 8-Pin JST-SH to 4x 2-Pin leads | Adafruit / SparkFun | 1–2 pcs | Pre-molded wiring for 4 solenoids |
| **Miniature Actuators** | 5V DC Push/Pull Solenoids ($\varnothing 6.5 \times 12\,\text{mm}$) + TPU tip | Solenoid / Web | 4–8 pcs | 4 pcs per Smart Cartridge (Sena / Cardo) |
| **J2 Gateway Harness** | Pre-crimped 6-Pin JST-SH to Jack / USB | COTS Standard | 1–2 pcs | Pre-molded harness for headset audio & DC power |

---

## 11. Minimalist Tool List (The True IKEA Principle)

Because **no soldering, no crimping, and no heat-set threaded inserts** are required, the assembly tool list shrinks to the standard tools every motorcyclist carries:

| Tool | Size / Specification | Purpose during Assembly |
| :--- | :--- | :--- |
| **Hex Key Set** | **1.5 mm / 2.0 mm / 2.5 mm / 3.0 mm** | Tightening all enclosures, boards, and clamps |
| **Torx / Screwdriver** | **TX10 / PH1** | Enclosure lid and anti-theft locking screw |
| **Wrench / Socket** | **SW 7 mm / SW 8 mm** | Countering M4/M5 nuts on tube clamps |
| **Scissors / Cutter** | Standard | Sizing silicone gasket cord to length |
| **Silicone Grease** | Liqui Moly / OKS 1110 (small tube) | Light coating on enclosure gaskets |

> [!TIP]
> **No soldering iron, no heat gun, no specialized micro-crimping pliers, and no insert melting tips required.** All mechanical and electronic assemblies are exclusively snapped, plugged, and bolted!
