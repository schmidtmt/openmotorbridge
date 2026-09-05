# 14 - Build Instructions, Wiring & Vehicle Installation

This document is the comprehensive, hands-on assembly guide for building a complete **OpenMotorBridge (v8.0)** hardware kit for a motorcycle. It details 3D printing parameters, mechanical assembly, cable harnessing, Front Node installation, and the step-by-step commissioning checklist.

---

## 1. Kit Architecture Overview

A complete OpenMotorBridge motorcycle installation comprises:

```
                      ┌─────────────────────────────────────────┐
                      │    1x CENTRAL MAIN BOX (IP67)           │
                      │    (Under-seat / tail frame)            │
                      │    • Lower case + mid tray + lid        │
                      │    • Main PCB (ESP32-S3, Codec, UPS)    │
                      │    • Integrated LiPo backup battery     │
                      └────────────────────┬────────────────────┘
                                           │
                        1x CENTRAL HARNESS (HD26 IP67)
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         │                                 │                                 │
         ▼                                 ▼                                 ▼
┌──────────────────┐             ┌──────────────────┐              ┌──────────────────┐
│ 1x POD 1 (LEFT)  │             │ 1x POD 2 (RIGHT) │              │ 1x POD 3 (TAIL)  │
│ (Frame / Bar)    │             │ (Frame / Bar)    │              │ (Tail Cowl)      │
│ • Pod Enclosure  │             │ • Pod Enclosure  │              │ • Pod Enclosure  │
│ • Baseboard      │             │ • Baseboard      │              │ • Baseboard      │
│ • CARTRIDGE 1    │             │ • CARTRIDGE 2    │              │ • CARTRIDGE 3    │
│   (e.g., Sena)   │             │   (e.g., Cardo)  │              │   (LoRa + GNSS)  │
└──────────────────┘             └──────────────────┘              └──────────────────┘
                                           │
                                           ▼ 2.4 GHz Wireless Link (ESP-NOW < 1.8 ms)
                                 ┌──────────────────────────────────┐
                                 │ 1x UNIVERSAL FRONT NODE (IP67)   │
                                 │ (Cockpit & Sensor Hub)           │
                                 │ • 4-in-1 Universal Mounting      │
                                 │ • Ottocast USB-A Port (CarPlay)  │
                                 │ • Glovebox USB-C Charging Port   │
                                 │ • Knowles MEMS Wind Sensor       │
                                 │ • Battery-Free Handlebar PTT     │
                                 └──────────────────────────────────┘
```

---

## 2. Bill of Materials for One Complete Kit (What You Need for 1 Motorcycle)

To build a fully featured OpenMotorBridge (v8.0) installation for one motorcycle, the following complete bill of materials is required. It groups all components across 6 structured categories:

### 2.1 Category A: 3D Printed Parts (MJF PA12 Black or FDM ASA/PETG)
*Recommended manufacturing method: HP Multi Jet Fusion (MJF) or SLS in PA12 (glass-bead blasted, black dyed) or FDM in ASA/PET-CF. CAD files located in [`hardware/cad/stl/`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/).*

| Subassembly | STL File Name | Qty | Function & Description |
| :--- | :--- | :---: | :--- |
| **Main Box Lower Tub** | [`main_box_lower_case.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lower_case.stl) | **1** | Monocoque tub with 4x M4 silentblock tabs, 4x PCB standoffs, and perimeter O-ring groove |
| **Main Box Mid Tray** | [`main_box_mid_tray.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_mid_tray.stl) | **1** | Battery tray for 1000 mAh LiPo, 10x convection chimney slots & tongue-and-groove rib |
| **Main Box Lid** | [`main_box_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lid.stl) | **1** | Heavy-duty top lid with Gore ePTFE AVS 41 vent boss & 4x M3 screw counterbores |
| **Pod Base Enclosures** | [`pod_base_housing.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod_base_housing.stl) | **3** | Universal bay enclosure for Pod 1 (Left), Pod 2 (Right), and Pod 3 (Tail) with 120° pipe bed |
| **Pod Bulkhead Partitions**| [`03_pod_bulkhead_partition.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl) | **3** | Internal bulkhead with sealing collar & dual spring retainer posts (1 per pod) |
| **Cartridge 1 (Rider)** | [`cartridge_sena_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_sena_sled.stl) *(or Cardo)* | **1** | Hot-swap sled for primary rider headset (Sena 50S/60S or Cardo Packtalk Edge) |
| **Cartridge 2 (Passenger)**| [`cartridge_cardo_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_cardo_sled.stl) *(or Blank)* | **1** | Hot-swap sled for passenger headset or hermetic blank protector cartridge |
| **Cartridge 3 (Tail)** | [`cartridge_omm_transceiver_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_omm_transceiver_sled.stl) | **1** | Rear pod sled holding RP2040 coprocessor, active GNSS patch, and 868 MHz LoRa helical antenna |
| **Front Node Lower Tub** | [`front_node_lower_tub.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_lower_tub.stl) | **1** | Cockpit fairing tub with AMPS hole pattern ($30 \times 38\,\text{mm}$), EPDM cable combs & V-bed (PA12 / ASA) |
| **Front Node Upper Lid** | [`front_node_upper_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_upper_lid.stl) | **1** | Front lid with acoustic sound entry port for Knowles MEMS & perimeter gasket groove (PA12 / ASA) |
| **Front Node Cable Glands**| [`front_node_cable_glands_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_cable_glands_tpu.stl) | **1 Pair** | Elastomeric cable glands for Front (3x USB) & Left (3x Signals/Power) (TPU 95A / 85A) |
| **Front Node USB-C Cap** | [`front_node_usbc_cap_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_usbc_cap_tpu.stl) | **1** | Elastomeric protective dust cap with retaining tether for service port (TPU 95A / 85A) |
| **Rear Radar Dual Bracket**| [`pod3_radar_bracket.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod3_radar_bracket.stl) | **1** | M5 GoPro-style swivel hinge for horizontal leveling of Garmin Varia / mmWave radar |
| **Total 3D Printed Parts** | | **17** | **Complete hardware set for 1 motorcycle installation (15x PA12/ASA + 2x TPU)** |

---

### 2.2 Category B: Assembled Circuit Boards (5 PCBAs from JLCPCB / Eurocircuits)
*Production files (Gerber ZIP, BOM CSV, CPL Pick & Place) located in [`hardware/production_packages/`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages).*

| Circuit Board | Project / Identifier | Qty | Layer Count & Spec | Core Functions |
| :--- | :--- | :---: | :--- | :--- |
| **PCBA 01** | Central Main Controller (`kicad_main_box`) | **1** | 4-Layer FR4 TG150, ENIG Gold | ESP32-S3 Dual-Core, LM5164 DCDC, BQ24075 UPS, ES8388 Codec, Bourns audio transformers, BMI270 IMU, MicroSD |
| **PCBA 02** | Pod Base Carrier Board (`kicad_pod_base`) | **3** | 2-Layer FR4, ENIG Gold | M8 6-pin IP67 socket, SP3012 ESD array, Harwin 6-pin precision header with 4.8mm wipe |
| **PCBA 03** | Universal Cartridge Board (`kicad_cartridge`)| **2** | 2-Layer FR4, ENIG Gold | Harwin 6-pin precision socket, DS2401 1-Wire ID, JST-SH 6-pin ribbon header to OEM cradle |
| **PCBA 04** | Rear Pod 3 Transceiver (`kicad_rear_pod3`) | **1** | 4-Layer FR4 TG150, ENIG Gold | RP2040 coprocessor, u-blox NEO-M9N / MAX-M10S GNSS, Semtech SX1262 LoRa, 3x Murata MM8030 RF switches |
| **PCBA 05** | Universal Front Node (`kicad_front_node`) | **1** | 4-Layer FR4 TG150, ENIG Gold | ESP32-C3 RISC-V, USB2512B Hub, LMR36015 DCDC, TPS2051B power switch, Knowles MEMS mic, PTT trigger |

---

### 2.3 Category C: Mechanical Fasteners, Screws & Springs (A4 Stainless Steel / Brass)

| Fastener | Specification / Standard | Qty | Location & Purpose |
| :--- | :--- | :---: | :--- |
| **M3 Threaded Inserts** | Ruthex Brass M3 $\times 5.7\,\text{mm}$ (RX-M3x5.7) | **8** | 4x Main Box tub corners, 4x Front Node tub corners (heat-set at $220\,^\circ\text{C}$) |
| **M4 Threaded Inserts** | Ruthex Brass M4 $\times 8.1\,\text{mm}$ (RX-M4x8.1) | **4** | Front Node AMPS base pattern ($30 \times 38\,\text{mm}$) |
| **Main Case Screws** | Socket Head Cap DIN 912 A4 M3 $\times 40\,\text{mm}$ | **4** | Through-bolt 4-corner clamp for Central Main Box |
| **Front Node Screws** | Socket Head Cap DIN 912 A4 M3 $\times 20\,\text{mm}$ | **4** | 4-corner clamp for Universal Front Node |
| **PCB Mounting Screws** | Socket Head Cap DIN 912 A4 M2.5 $\times 6\,\text{mm}$| **8** | 4x Main Box PCB, 4x Front Node PCB |
| **Pod Bulkhead Screws** | Countersunk DIN 7991 A4 M2 $\times 8\,\text{mm}$ | **6** | Secures internal bulkheads in Pod 1, 2, and 3 (2 per pod) |
| **Ejector Coil Springs** | A4 Stainless Steel ($\varnothing 4.5\,\text{mm}, L_0=15\,\text{mm}, R=1.2\,\text{N/mm}$) | **6** | Auto-eject snap release mechanism (2 per pod bulkhead) |
| **Rubber Silentblocks** | Type A Rubber Bobbins (M4 Male / M4 Female, $\varnothing 15 \times 10\,\text{mm}$) | **4** | Vibration-isolated frame mounting for Central Main Box |
| **Nyloc Nuts & Washers** | DIN 985 M4 Nyloc Nuts + DIN 125 A4 Washers | **4** | Secures silentblocks to motorcycle subframe tabs |
| **M5 Clamp Screw & Nut** | Socket Head Cap DIN 912 A4 M5 $\times 25\,\text{mm}$ + M5 Acorn Nut | **1** | Secures GoPro-style radar hinge arm on Pod 3 |

---

### 2.4 Category D: Gaskets, Venting & Light Pipes (IP67)

| Component | Specification | Qty | Location & Function |
| :--- | :--- | :---: | :--- |
| **Silicone O-Ring Cord Main**| Silicone Solid Cord $\varnothing 1.5\,\text{mm}$ Shore 40A/50A ($40\,\text{cm}$) | **1** | Perimeter tongue-and-groove seal on Central Main Box |
| **Silicone O-Ring Cord Front**| Silicone Solid Cord $\varnothing 1.5\,\text{mm}$ Shore 40A/50A ($30\,\text{cm}$) | **1** | Perimeter lid seal on Universal Front Node |
| **Cartridge Face Seals** | Molded Silicone Flange Seal Shore 40A ($54 \times 18\,\text{mm}$, $1.5\,\text{mm}$) | **3** | Mouth opening seal on Pod 1, 2, and 3 |
| **EPDM Slotted Cable Combs** | EPDM Closed-Cell Rubber Slotted Block ($15 \times 8 \times 4\,\text{mm}$) | **2** | Waterproof cable feedthrough sealing in Front Node |
| **Pressure Relief Vent** | Gore Automotive AVS 41 (M8x1.25 screw-in vent) | **1** | Pressure equalization & condensation prevention in Main Box lid |
| **ePTFE Adhesive Vents** | Gore / Porex IP67 Adhesive Vent Disc $\varnothing 6.0 \dots 7.0\,\text{mm}$ | **5** | 3x Pod vent bosses, 1x Front Node, 1x Knowles MEMS acoustic port |
| **Optical Light Pipe** | Bivar PLPC3-3MM or Mentor PMMA $\varnothing 3.0\,\text{mm}$ ($L=8\,\text{mm}$) | **1** | Waterproof transmission of WS2812B RGB LED through Main Box lid |

---

### 2.5 Category E: Wiring Harness, Connectors, Backup Battery & RF Pigtails

| Component | Specification / Type | Qty | Purpose & Function |
| :--- | :--- | :---: | :--- |
| **HD26 IP67 Flange Socket**| Amphenol LTW HD26 Female (Front-mount with silicone seal) | **1** | Waterproof chassis interface on Central Main Box |
| **HD26 IP67 Cable Plug** | HD26 Male Connector with thumb screws & compression gland | **1** | Primary connector terminating the bike breakout harness |
| **M8 6-Pin Socket Leads** | M8 6-Pin A-coded IP67 Female (PUR shielded, 250 mm) | **3** | Pigtails 1, 2, and 3 on harness connecting to Pods |
| **M8 4-Pin Socket Lead** | M8 4-Pin A-coded IP67 Female (PUR shielded, 250 mm) | **1** | Pigtail 5 on harness for Rear Radar (Garmin Varia / mmWave) |
| **AMP Superseal 1.5 Socket**| TE Connectivity AMP Superseal 1.5 4-Pin Female Housing | **1** | Pigtail 4 on harness for 12V vehicle power (KL30, KL15, GND) |
| **M8 Extension Cables** | M8 6-Pin A-coded Male/Female (PUR shielded, 1.0 m / 1.5 m) | **3** | Extension cables from under-seat pigtails to pods |
| **UPS Backup Battery** | 1S 3.7V LiPo 1000 mAh with integrated 10k NTC | **1** | Seamless UPS power reserve inside Main Box (Molex Micro-Fit 3.0) |
| **Automotive Fuse Holder** | Waterproof Mini-Blade Inline Fuse Holder IP67 + **2A Fuse** | **1** | Protects permanent 12V supply (KL30) directly at battery terminal |
| **Automotive Wire** | FLRY-B $0.5\,\text{mm}^2$ (Power/GND) and $0.35\,\text{mm}^2$ (Signals/Audio) | *As req.* | Custom bike harness per [`central_breakout_harness_wirelist.csv`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/05_wiring_harness_spec/central_breakout_harness_wirelist.csv) |
| **EPDM Frame Straps** | UV/Ozone-resistant EPDM ladder straps ($\varnothing 45 \dots 75\,\text{mm}$) | **6** | Tool-free rapid mounting of pods to crash bars or frame tubes |
| **Murata MM8030 Pigtails** | Murata MM126036 to SMA Bulkhead IP67 (150 mm, RG-178)| **3** | Coaxial bypass for Pod 3: J3 (2.4G), J4 (868M), J5 (GNSS) |
| **U.FL Coaxial Pigtail** | IPEX MHF1 / U.FL to RP-SMA Bulkhead IP67 (150 mm, RG-178)| **1** | Coaxial feed for Front Node ESP32-C3 external antenna |
| **SMA Flange Double Bulkhead**| SMA Female to SMA Female Bulkhead IP67 with O-ring & nut | **1** | Waterproof RF feedthrough in cartridge faceplate (Class A) |
| **Internal Coax Pigtail** | RG-178 Coaxial Cable ($6\dots 10\,\text{cm}$, 90° SMA Male to SMA Male)| **1** | RF connection from Sena +Mesh / OEM adapter to faceplate |
| **SMA IP67 Protective Caps** | Nickel-plated brass with internal O-ring (knurled cap)| **5** | Waterproof seal for unpopulated SMA ports (3x Pod 3, 1x Front, 1x Pod) |
| **External Antennas (Opt.)**| 2.4G Collinear (+5 dBi), 868M LoRa (+3 dBi), Active GNSS Puck | *Optional* | High-gain external antennas for long range & unobstructed sky view |
| **USB-A Flat Ribbon Cable (Front)**| Short 90° USB-A male-to-female adapter ($10\dots 15\,\text{cm}$)| **1** | Ottocast connection to J1 via front cable gland |
| **USB-C Glovebox Cable (Front)**| Right-angle USB-C male-to-male ($1.0\,\text{m}$, PUR/Nylon) | **1** | Smartphone charging from J2 via front cable gland |
| **JST-GH Connector Kit (Left)** | JST-GH 1.25mm 2-pin female housings + crimp terminals | **2 sets** | Pre-crimped harness leads for J3 (PTT) & J7 (12V) |
| **90° USB Cartridge Cable** | Low-profile 90° right-angle Micro-USB/USB-C ($5\dots 8\,\text{cm}$) | **1** | 5V power feed for Sena +Mesh / MeshPort inside cartridge |
| **EPDM Cartridge Retaining Band**| Elastic EPDM rubber strap ($\approx 35 \times 10\,\text{mm}$) | **1** | Vibration-proof retention of OEM adapter via cartridge hooks |

---

### 2.6 Category F: Required Tools, Measurement Equipment & Assembly Chemicals

To assemble all subassemblies with vibration resistance and hermetic IP67 sealing, the following toolkit and consumables are recommended:

| Tool / Equipment | Recommended Model / Specification | Purpose in the Project | Essential? |
| :--- | :--- | :--- | :---: |
| **Hex Key Set (Ball End)** | Sizes 1.5 mm / 2.0 mm / 2.5 mm / 3.0 mm | M2 bulkheads, M2.5 PCBAs, M3 cases, M5 radar hinge | **Yes** |
| **Open Wrenches / Sockets** | 7 mm (M4 nuts), 8 mm (SMA bulkheads), 10 mm (Battery terminal) | Tightening silentblock nuts & SMA RF receptacles | **Yes** |
| **Precision Torque Screwdriver**| $0.2 \dots 1.5\,\text{Nm}$ (e.g. Wera 7440) | Even torque on M3 lids ($0.8\,\text{Nm}$) & PCBAs ($0.4\,\text{Nm}$) | *Recommended* |
| **Adjustable Soldering Station**| $200 \dots 450\,^\circ\text{C}$ (e.g. TS101, Pinecil, Weller) | Heat-set insert installation & harness soldering | **Yes** |
| **Ruthex Heat-Set Tips** | Dedicated brass soldering tips for M3 & M4 (Ruthex / CNC Kitchen)| Perpendicular, ridge-free insert seating ($220 \dots 240\,^\circ\text{C}$) | *Recommended* |
| **Micro-Crimp Pliers** | Engineer PA-09 or IWISS IWS-2820M ($1.0 \dots 1.6\,\text{mm}$ pitch) | Crimping JST-SH (1.0 mm Cartridges) & JST-GH (1.25 mm Front Node) | **Yes** |
| **Automotive Crimper** | For uninsulated open-barrel automotive terminals ($0.5 \dots 1.5\,\text{mm}^2$)| 12V spade terminals & M6 battery terminal ring lugs | **Yes** |
| **Precision Wire Stripper** | $0.08 \dots 1.0\,\text{mm}^2$ (AWG 28–18, e.g. Knipex 12 62 180) | Nick-free stripping of thin FLRY-B wires | **Yes** |
| **Flush Wire Cutters** | Precision electronics diagonal cutter (e.g. Knipex Super Knips) | Flush cuts on wires, pins, and zip-ties without sharp burrs | **Yes** |
| **Heat Gun / Hot Air Blower**| With reduction nozzle ($150 \dots 300\,^\circ\text{C}$) | Shrinking dual-wall adhesive-lined heatshrink tubing on harness | **Yes** |
| **ESD Precision Tweezers** | Fine curved plastic/ceramic tipped tweezers | Damage-free perpendicular snapping of Murata MM8030 & U.FL plugs | **Yes** |
| **Digital Multimeter (DMM)** | With continuity buzzer & mV/mA ranges | Harness continuity checking, quiescent current & 5V/3.3V rails | **Yes** |
| **Benchtop Power Supply** | $0 \dots 30\,\text{V DC}, 0 \dots 3\,\text{A}$ (adjustable current limit) | Safe first power-up at 12.0V / 150mA to prevent short-circuit damage | **Yes** |
| **Dielectric Silicone Grease**| OKS 1110 or Liqui Moly Silicone Paste (transparent, dielectric) | Lubrication of silicone O-rings, EPDM combs & cartridge lips | **Yes** |
| **Threadlocker (Loctite 243)** | Medium strength (blue) | Prevents motorcycle screw loosening under heavy vibrations | **Yes** |
| **Conformal Coating** | Peters Elpeguard SL 1307 or Electrolube UR5041 (IPC-CC-830B) | Full PCB encapsulation against condensation and road salt spray | *Recommended* |
| **Scalpel / Precision Knife** | With fresh sharp blade | Burr-free trimming of silicone cord gaskets & EPDM blocks | **Yes** |
| **USB-C Data Cable** | High-quality USB 2.0/3.0 data cable (not a power-only cable!) | Flashing ESP32-S3, RP2040, and ESP32-C3 via PlatformIO | **Yes** |

---

## 3. 3D Printing Guidelines (FDM vs. Industrial MJF)

### Recommended Filaments for Outdoor Motorcycle Use (FDM):
* **PETG:** *Ideal for open-frame printers.* UV-resistant, oil/chemical tolerant, heat stable up to $80\,^\circ\text{C}$.
* **ASA (or ABS):** *Best choice for enclosed printers (Bambu X1/P1, Prusa XL).* 100% UV stable, heat resistant to $100\,^\circ\text{C}$.
* **PA-CF / PET-CF:** Extreme stiffness and OEM-grade matte carbon texture.
* ❌ *Warning:* **Do NOT use standard PLA**, as it softens and deforms in direct sunlight (exceeding $55\,^\circ\text{C}$).

### Optimal Slicer Settings for IP67 Water Resistance:
* **Perimeters (Walls):** Set to 4–5 walls ($\approx 1{,}6 \dots 2{,}0\,\text{mm}$ thickness, resulting in 100% solid shell).
* **Infill:** $25 \dots 40\,\%$ Gyroid.
* **Layer Height:** $0{,}16\,\text{mm}$ (produces smooth O-ring sealing grooves).
* **Flow Rate:** $102 \dots 104\,\%$ (slight over-extrusion fuses inter-layer micropores).

---

## 4. Subsystem Assembly Steps

### Step 1: Central Control Box Assembly
1. **Heat-Set Inserts:** Melt 4x M3 brass threaded inserts (Ruthex) into the lower tub using a soldering iron ($240\,^\circ\text{C}$).
2. **Mount Main PCB:** Secure the main controller (`PCBA 01`) onto the damping standoffs using M2.5 screws.
3. **Mid Tray & Battery:** Position the upper case with the intermediate tray, place the 1000 mAh LiPo into the battery pocket, and secure with the EPDM strap.
4. **Gasket & Lid:** Seat the $\varnothing 1{,}5\,\text{mm}$ silicone O-ring cord into the perimeter groove, adhere the Gore ePTFE vent, and tighten the 4x M3 x 40 mm stainless screws in a cross pattern.

### Step 2: Satellite Pods 1, 2, and Rear Pod 3 (Tub & Bulkhead)
1. **Install Baseboard:** Slide `openmotorbridge_pod_base` into the pod tub and tighten the M8 hex nut.
2. **Mount Bulkhead:** Secure the protective partition wall with 2x M2 countersunk screws.

### Step 3: Headset Cartridges 1 & 2 (Rider & Passenger)
1. **Assemble Cartridge:** Snap the cartridge carrier (`PCBA 03`) into the sled.
2. **Connect OEM Adapter / Cradle (by device class):**
   * **Class A (Sena +Mesh B2M-01 / MeshPort Adapter):**
     * Slide the adapter laterally into the transverse slide rails of the cradle insert ([`01_insert_sena.scad`](file:///Users/schmidtm/openMotorBridge/hardware/cad/scad/03_pod_cartridges/parts/01_insert_sena.scad)) until the retaining snap latch clicks into place.
     * **Connect USB Power:** Route the low-profile $90^\circ$ right-angle cable (Micro-USB or USB-C) from the cartridge PCB 5V/GND header through the deck window into the +Mesh USB charging port (pure 5V continuous power supply; intercom audio routes wirelessly over Bluetooth to the helmet).
     * **RF Antenna:** Insert the waterproof SMA female-to-female flange bulkhead with O-ring from the outside into the $\varnothing 6.5\,\text{mm}$ faceplate bore and secure from the inside with the locknut. Connect the internal $90^\circ$ coaxial pigtail to the +Mesh antenna port, route through the front window, and fasten tightly to the inside of the faceplate SMA bulkhead. Fasten the external SMA IP67 protective cap whenever an external antenna is not connected.
     * Secure the +Mesh adapter against vibration shocks using the elastic EPDM retention strap across both lateral hooks.
   * **Class B & C (Sena 50S/60S or Cardo Packtalk Edge Cradles):**
     * Connect the 6-pin JST-SH ribbon cable from the cartridge PCB directly to the OEM pogo-pin dock (Sena) or magnetic Cardo Air-Mount (providing galvanically isolated analog audio channels, mic, and optocoupled PTT).
   * **Class D (Hermetic Blank Cartridge):**
     * Insert the blank sled with solid faceplate and O-ring seal when running solo without a passenger pod.
3. **Mouth Seal:** Fit the silicone molded flange gasket over the cartridge collar and lightly coat with dielectric silicone grease.

### Step 4: Rear Pod 3 Cartridge & RF Pigtails (Triple Coaxial Bypass)
1. **Install SMA Bulkheads:**
   * Feed the 3x SMA female bulkhead connectors of the Murata MM126036 pigtails from the outside through the prepared $\varnothing 6.5\,\text{mm}$ bores in the cartridge front face.
   * The integrated silicone O-ring seats hermetically in the $\varnothing 9.5 \times 1.2\,\text{mm}$ counterbore.
   * From inside, place the lock washer and tighten the hex nut (8 mm wrench) to approx. $0.8\,\text{Nm}$.
2. **Route Coaxial Cables:**
   * Lay the flexible 1.13mm / RG-178 coaxial leads neatly into the floor channel of the sled.
3. **Insert PCB & Connect Pigtails:**
   * Mount the rear transceiver board (`PCBA 04`) with M2.5 screws.
   * Using plastic tweezers, snap the right-angle Murata MM8030 plugs vertically onto the SMD switch receptacles until they click:
     * `J3` $\rightarrow$ 2.4 GHz OpenMotorMesh Bypass
     * `J4` $\rightarrow$ 868 MHz Semtech SX1262 LoRa Bypass
     * `J5` $\rightarrow$ Multi-GNSS u-blox M9N Bypass (with 3.3V phantom power)
4. **Automatic RF Switch Operation (Plug & Play):**
   * **Standard Operation (No external antennas):** The IP67 knurled brass caps are screwed onto the SMA ports. The internal antennas (2.4G IFA, 868M helical, and 25x25mm GNSS patch) operate 100% autonomously protected inside the dielectric radome.
   * **External High-Gain Operation:** When an external antenna is threaded on, the mechanical leaf switch inside the Murata MM8030 receptacle lifts: The internal antenna is electrically disconnected ($> 25\,\text{dB}$ isolation) and the RF energy flows to the external antenna with $< 0.15\,\text{dB}$ insertion loss.

---

## 5. Universal Front Node Assembly & Vehicle Installation

### 5.1 Enclosure Assembly
1. **Heat-Set Inserts:**
   * Melt 4x M3 inserts into the enclosure corners.
   * Melt 4x M4 inserts into the AMPS pattern ($30 \times 38\,\text{mm}$) on the bottom.
2. **Acoustic Membrane:** Adhere the hydrophobic Gore ePTFE acoustic membrane over the Knowles MEMS sound port.
3. **Mount PCB:** Fasten `PCBA 05` using M2.5 screws.
4. **RF Antenna Installation (ESP32-C3 2.4 GHz):**
   * Adhere the flexible 2.4 GHz FPC dipole antenna (e.g. Molex 146153) into the $48 \times 12\,\text{mm}$ recess pocket on the inside of the enclosure lid.
   * Route the $1.13\,\text{mm}$ micro-coaxial lead into the ceiling guide canal and snap the U.FL / IPEX-MHF1 connector perpendicular onto the antenna port of the ESP32-C3-WROOM-02U module. (Optional: For extreme installations such as solid carbon fiber fairings, the lead can be routed outside through an EPDM gland slit).
5. **Insert Cables into Front & Flank Openings:**
   * **Front Opening (South Wall, 4x $\varnothing 4.2\,\text{mm}$ slitted channels for USB):**
     * Insert the short USB-A flat ribbon cable into Channel 1 and connect to Port `J6` (switched VBUS for CarPlay / Dongle).
     * Insert the $1.0\,\text{m}$ right-angle USB-C charging cable into Channel 2 and connect to Port `J5` (glovebox charging).
     * Insert the USB cable into Channel 3 and connect to Port `J4` (USB host).
     * Insert the 5V Action-Cam charging cable into Channel 4 and connect to Port `J8` (continuous 5V charging backed by buffer capacitor C_BUF).
   * **Right Opening (East Wall, USB-C Service Port):**
     * Seat the elastomeric USB-C service dust cap (`front_node_usbc_cap_tpu.stl`) with its sealing flange collar into the East wall pocket over service port `J7`.
   * **Left Opening (West Wall, 3x $\varnothing 3.2\,\text{mm}$ slitted channels for Signals & Power):**
     * Route 12V vehicle power (KL15 & GND) with JST-PH 2-pin connector into Channel 1 and latch into `J1`.
     * Route CAN-Bus twisted pair with JST-PH 3-pin connector into Channel 2 and latch into `J2`.
     * Route Handlebar PTT switch lead with JST-PH 2-pin connector into Channel 3 and latch into `J3`.
6. **Seat Glands & Close Enclosure:**
   * Lightly coat the outer flanks of the EPDM/TPU cable glands with silicone grease.
   * Slide the combs into the enclosure cutouts (the slits close snugly around the wires).
   * Lay the $\varnothing 1.5\,\text{mm}$ silicone O-ring cord ($30\,\text{cm}$) into the lid perimeter groove and tighten the 4x M3 x 20 mm bolts in a cross pattern (compressing the glands by approx. 15% for hermetic IP67 sealing).

### 5.2 Motorcycle Mounting (4 Options)

```
┌────────────────────────────────────────────────────────────────────────┐
│               FRONT NODE 4-IN-1 MOUNTING OPTIONS                       │
├────────────────────────────────────────────────────────────────────────┤
│ Option 1: AMPS Pattern (30 x 38 mm)                                    │
│ • Bolts directly to RAM-Mount balls, Garmin brackets, nav towers       │
├────────────────────────────────────────────────────────────────────────┤
│ Option 2: 120° V-Groove Tube Saddle with EPDM O-Rings                  │
│ • Toolless attachment to Ø 22 mm to Ø 32 mm crash bars (BMW GS)        │
├────────────────────────────────────────────────────────────────────────┤
│ Option 3: M4 Silentblocks                                              │
│ • Vibration-isolated screw mounting inside the fairing beak            │
├────────────────────────────────────────────────────────────────────────┤
│ Option 4: 3M Dual-Lock Recesses                                        │
│ • Concealed attachment inside Harley Batwing / Sharknose fairings      │
└────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Electrical Connections
* **12V Vehicle Power:** Connect a single 2-core wire (KL15 switched ignition and chassis ground) to the parking light or accessory socket.
* **Ottocast Dongle:** Plug into USB-A Port `J1` and affix with 3M Dual-Lock inside the fairing.
* **Glovebox Extension:** Route a USB-C cable from Port `J2` to the glovebox for smartphone charging.
* **Handlebar PTT:** Wire the mechanical handlebar button to 2-pin header `J3`.

---

## 6. First Commissioning & Flashing Checklist

```bash
# 1. Flash Central Main Controller (ESP32-S3)
cd openMotorBridge/firmware/main_controller
pio run --target upload
pio run --target uploadfs

# 2. Flash Rear Tail Coprocessor (RP2040)
cd ../rear_coprocessor
pio run --target upload

# 3. Flash Front Node (ESP32-C3)
cd ../front_node
pio run --target upload
```

### Verification Checklist:
1. [ ] **Bench Power:** Apply $12{,}0\,\text{V DC}$ (current limit $150\,\text{mA}$). Quiescent draw should measure $45 \dots 75\,\text{mA}$.
2. [ ] **Status LED:** Pulses green (system ready, UPS charging).
3. [ ] **Web Dashboard:** Connect via Web Bluetooth to `OpenMotorBridge_v8`.
4. [ ] **Cartridge Detection:** Insert cartridges into Pods 1 and 2 $\rightarrow$ Headset profiles appear immediately.
5. [ ] **Front Node Wireless Link:** Dashboard displays `ESP-NOW LINK (2.4 GHz) - READY`.
6. [ ] **PTT Test:** Press handlebar button $\rightarrow$ Dashboard PTT tile illuminates green (`< 1.8 ms Latency`).
7. [ ] **CarPlay Hard Reboot:** Click "CarPlay 1-Click Hard Reboot" $\rightarrow$ VBUS drops to $0{,}00\,\text{V}$ for $2{,}5\,\text{s}$ and restarts cleanly.
8. [ ] **Audio Check:** Pair headset and play music $\rightarrow$ Crystal-clear audio free of ground loops.

---

## 7. Maintenance & Care

* **Gasket Inspection:** Lubricate the silicone O-ring cords on the Main Box, Front Node, and pod cartridges once per season with dielectric silicone grease.
* **Venting Integrity:** Verify that the ePTFE Gore vents are clean and unobstructed by mud or road grime.
* **Firmware Updates:** Wireless and modular in-system updates are directly performed via the Web Bluetooth PWA dashboard.
