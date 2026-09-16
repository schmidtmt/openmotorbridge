# 16 - Build Instructions, Wiring & Vehicle Installation

This document is the comprehensive, hands-on assembly guide for building a complete **OpenMotorBridge (v8.0)** hardware kit for a motorcycle. It details 3D printing parameters, mechanical assembly, plug-and-play cabling, Front Node installation, and the step-by-step commissioning checklist.

---

## 1. Kit Architecture Overview (What Are We Building?)

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
│ • GATEWAY SLOT 1 │             │ • GATEWAY SLOT 2 │              │ • CARTRIDGE 3    │
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

#### 2.1.1 Base System (Universal for 1 Complete Motorcycle Setup)
| Subassembly | STL File Name | Qty | Function & Description |
| :--- | :--- | :---: | :--- |
| **Main Box Lower Tub** | [`main_box_lower_case.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lower_case.stl) | **1** | Monocoque tub with 4x M4 silentblock tabs, nut pockets, and perimeter O-ring groove |
| **Main Box Mid Tray** | [`main_box_mid_tray.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_mid_tray.stl) | **1** | Battery tray for 1000 mAh LiPo, 10x convection chimney slots & tongue-and-groove rib |
| **Main Box Lid** | [`main_box_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lid.stl) | **1** | Heavy-duty top lid with Gore ePTFE AVS 41 vent boss & 4x M3 screw counterbores |
| **Pod Base Enclosures** | [`pod_base_housing.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod_base_housing.stl) | **3** | Universal bay enclosure for Pod 1 (Gateway 1 Left), Pod 2 (Gateway 2 Right), and Pod 3 (Tail) with 120° pipe bed |
| **Pod Bulkhead Partitions**| [`03_pod_bulkhead_partition.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl) | **3** | Internal bulkhead with sealing collar & dual spring retainer posts (1 per pod) |
| **Cartridge Base Sleds** | [`cartridge_base_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl) | **3** | Universal sled chassis holding modular inlays and PCBA 03 (Pods 1 & 2) or PCBA 04 (Pod 3) |
| **Cartridge Locking Rocker**| [`cartridge_magnetic_lock_latch.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_magnetic_lock_latch.stl) | **2** | Magnetic anti-theft locking rocker latches with sawtooth lock for Pods 1 & 2 |
| **Rear Pod 3 OMM Radome** | [`cartridge_antenna_bracket_omm.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_antenna_bracket_omm.stl) | **1** | Dielectric antenna radome & carrier bridge for PCBA 04 transceiver in Rear Pod 3 |
| **Front Node Lower Tub** | [`front_node_lower_tub.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_lower_tub.stl) | **1** | Cockpit fairing tub with AMPS hole pattern ($30 \times 38\,\text{mm}$), nut pockets & V-bed (PA12 / ASA) |
| **Front Node Upper Lid** | [`front_node_upper_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_upper_lid.stl) | **1** | Front lid with acoustic sound entry port for Knowles MEMS & perimeter gasket groove (PA12 / ASA) |
| **Front Node Cable Glands**| [`front_node_cable_glands_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_cable_glands_tpu.stl) | **1 Pair** | Elastomeric cable glands for Front (3x USB) & Left (3x Signals/Power) (TPU 95A / 85A) |
| **Front Node USB-C Cap** | [`front_node_usbc_cap_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_usbc_cap_tpu.stl) | **1** | Elastomeric protective dust cap with retaining tether for service port (TPU 95A / 85A) |

#### 2.1.2 Cartridge Inlays for Gateway Slots 1 & 2 (Choose 2 Based on Desired Intercoms)
> **Architecture Principle:** OpenMotorBridge is a multi-protocol mesh bridge. Cartridge slots 1 and 2 are **hardware gateway transceivers**, not isolated driver/passenger headsets. They enable simultaneous dual-mesh bridging (e.g., Slot 1 = Sena Mesh 3.0 / Wave and Slot 2 = Cardo DMC 2.0 or PMR446), allowing riders and passengers to communicate wirelessly across both networks.

| Subassembly | STL File Name | Qty | Function & Description |
| :--- | :--- | :---: | :--- |
| **Gateway Inlay Sena** | [`cartridge_insert_sena.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) | *Opt. (1)* | Form-fitting inlay for Sena SPIDER X Slim / 50S / 60S (Mesh 3.0 Wave) |
| **Gateway Inlay Cardo** | [`cartridge_insert_cardo.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl) | *Opt. (1)* | Inlay for Cardo Packtalk Edge / Pro (DMC Gen2) with Air-Mount |
| **Blank Cartridge / Dry Box**| [`cartridge_insert_blindkassette.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_blindkassette.stl) | *Opt. (1)* | Hermetic protective sled with O-ring for unused slot or dry storage box |

#### 2.1.3 Vehicle-Specific Mounting Kits (3D Printed Parts)
*Mounting pods to frames, luggage, or tails uses vehicle-specific 3D printed components:*

* **Option A: Adventure Kit (BMW R1250/R1300 GS / GSA, Africa Twin, KTM):**
  | Subassembly | STL File Name | Qty | Function & Description |
  | :--- | :--- | :---: | :--- |
  | **Pannier Clamp Base** | [`adventure_pannier_rack_clamp_base.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_pannier_rack_clamp_base.stl) | **4** | Clamp base for Ø 18 mm stainless pannier racks (BMW GSA) |
  | **Pannier Clamp Cap** | [`adventure_pannier_rack_clamp_cap.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_pannier_rack_clamp_cap.stl) | **4** | Clamp cap with M5 bolt through-holes |
  | **Rack-Tail Mount Heck** | [`adventure_rack_tail_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_rack_tail_mount.stl) | **1** | Tail Balcony cantilever for Pod 3 behind topcase with branch deflector |
  | **Transition Dock** | [`adventure_transition_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_transition_dock.stl) | **2** | Luggage-independent dock in seat crease for BMW GS (Ø 28 mm tube) |
  | **Radar Varia Dock** | [`radar_varia_gopro_lock_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_varia_gopro_lock_dock.stl) | **1** | Garmin Varia quarter-turn dock with M3 anti-theft set screw |
  | **Hirth Gear Lock** | [`011_gopro_hirth_lock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/011_gopro_hirth_lock.stl) | **1** | 36-tooth positive-locking rosette for vibration-proof radar angle |

* **Option B: Harley-Davidson Touring & Bagger Kit (Street Glide, Road Glide, CVO ST, Road King):**
  | Subassembly | STL File Name | Qty | Function & Description |
  | :--- | :--- | :---: | :--- |
  | **Saddlebag Lid Dock** | [`saddlebag_lid_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/saddlebag_lid_dock.stl) | **2** | Low-profile hard saddlebag lid dock for Pod 1 & Pod 2 |
  | **Touring Fender Console** | [`pod3_touring_fender_console.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod3_touring_fender_console.stl) | **1** | Organic rear fender console for Pod 3 (Road King Special) |
  | *Alternative: CVO ST Fin* | [`cvo_st_telemetry_fin.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/cvo_st_telemetry_fin.stl) | *(1)* | Aerodynamic tail fin for CVO Road Glide ST |
  | *Alternative: Skeleton Dock*| [`cvo_st_undercowl_skeleton_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/cvo_st_undercowl_skeleton_dock.stl) | *(1)* | Upright spring dock under forged carbon solo seat cowl |
  | **License Plate Radar Mount**| [`radar_license_plate_bracket.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_license_plate_bracket.stl) | **1** | Decoupled radar bracket below license plate |
  | *Alternative: Underfender* | [`radar_center_underfender_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_center_underfender_mount.stl) | *(1)* | Centered under-fender mount for custom baggers with side license plates |

#### 2.1.4 Accessories (Optional)
| Subassembly | STL File Name | Qty | Function & Description |
| :--- | :--- | :---: | :--- |
| **Smart Keyfob Lower Shell**| [`smart_keyfob_lower_shell.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/smart_keyfob_lower_shell.stl) | **1** | Tub with LRA dampening cradle & magnet pocket for PCBA 07 |
| **Smart Keyfob Upper Shell**| [`smart_keyfob_upper_shell.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/smart_keyfob_upper_shell.stl) | **1** | Lid with 3 button keypads & optical light pipe port |
| **Smart Keyfob Bumper** | [`smart_keyfob_tpu_rim.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/smart_keyfob_tpu_rim.stl) | **1** | Shock-absorbing perimeter rim (TPU 85A/95A) |

---

### 2.2 Category B: Factory-Assembled Circuit Boards (100% SMT from JLCPCB / Eurocircuits)
*All circuit boards arrive fully assembled and pre-tested via automated SMT. **Zero soldering required by the builder!***
*Production files (Gerber ZIP, BOM CSV, CPL Pick & Place) detailed in [Chapter 15, Section 8](file:///Users/schmidtm/openMotorBridge/docs/en/15_bom_manufacturing.md#8-1-click-jlcpcb-ordering-guide-all-circuit-boards-pre-assembled).*

| Circuit Board | Project / Identifier | Qty | Core Functions |
| :--- | :--- | :---: | :--- |
| **PCBA 01** | Central Main Controller (`kicad_main_box`) | **1** | ESP32-S3 Dual-Core, LM5164 DCDC, BQ24075 UPS, ES8388 Codec, Bourns audio transformers, IMU |
| **PCBA 02** | Pod Base Carrier Board (`kicad_pod_base`) | **3** | M8 6-pin IP67 socket, SP3012 ESD array, Harwin 6-pin precision docking header |
| **PCBA 03** | Smart Modular Cartridge Board Rev 2.0 (`kicad_cartridge`)| **2** | WCH CH32V003 RISC-V MCU (1-Wire emulation & opcode engine), 4x MOSFETs, J_ACT header |
| **PCBA 04** | Rear Pod 3 Transceiver (`kicad_rear_pod3`) | **1** | RP2040 coprocessor, u-blox Multi-GNSS, Semtech SX1262 LoRa, 3x Murata MM8030 RF switches |
| **PCBA 05** | Universal Front Node (`kicad_front_node`) | **1** | ESP32-S3 Xtensa, USB2514B Hub, SC8102 USB-PD 20W, TCAN334G CAN-FD, Knowles MEMS, PTT |
| **PCBA 07** | Smart Keyfob (Accessory, `kicad_smart_keyfob`)| *Opt.* | Bluetooth LE tracker, LRA haptic motor, MAX17048 fuel-gauge, 3 tactile buttons |

---

### 2.3 Category C: Mechanical Fasteners & Screws (A4 Stainless Steel)
*The enclosure design uses integrated **Nut-Pockets (hexagonal nut slots)**. Standard nuts slide right in – **no heat-set threaded inserts or soldering irons!***

| Fastener | Specification / Standard | Qty | Location & Purpose |
| :--- | :--- | :---: | :--- |
| **Main Case Screws** | Socket Head Cap DIN 912 A4 M3 $\times 40\,\text{mm}$ | **4** | Central Main Box enclosure (threads into captive nuts) |
| **Front Node Screws** | Socket Head Cap DIN 912 A4 M3 $\times 20\,\text{mm}$ | **4** | Front Node enclosure (threads into captive nuts) |
| **M3 Stainless Nuts** | DIN 934 / DIN 985 M3 A4 Stainless Nuts | **8** | Captive in Nut-Pockets (enclosures) |
| **PCB Mounting Screws** | Socket Head Cap DIN 912 A4 M2.5 $\times 6\,\text{mm}$| **8** | 4x Main Box PCBA, 4x Front Node PCBA |
| **Pod Bulkhead Screws** | Countersunk DIN 7991 A4 M2 $\times 8\,\text{mm}$ | **6** | Secures 3 Pod bulkheads (2 per pod) |
| **Cartridge Bracket Screws**| Countersunk DIN 7991 A4 M2 $\times 6\,\text{mm}$ | **8** | Secures actuator retainer plates (4 per gateway) |
| **M2 Rocker Hinge Pins** | Dowel Pin Stainless DIN 7 M2 $\times 8\,\text{mm}$ | **2** | Pivot pins for magnetic cartridge latches (Pods 1 & 2) |
| **Ferromagnetic Steel Pins**| Hardened Steel Pin DIN 6325 $\varnothing 6 \times 8\,\text{mm}$ | **2** | Magnetic steel armature in rocker arm |
| **Rocker Return Springs** | A4 Stainless Steel ($\varnothing 3.5\,\text{mm}, L_0=10\,\text{mm}$) | **2** | Return spring for cartridge locking claw |
| **Ejector Compression Springs**| A4 Stainless Steel ($\varnothing 4.5\,\text{mm}, L_0=15\,\text{mm}$) | **6** | Auto-eject snap release springs (2 per pod bulkhead) |
| **N52 Magnetic Key** | Neodymium N52 Block Magnet ($20 \times 10 \times 5\,\text{mm}$) | **1** | Contactless key for rapid cartridge ejection |
| **Rubber Silentblocks** | Type A Rubber Bobbins (M4 Male / M4 Female, $\varnothing 15 \times 10\,\text{mm}$) | **4** | Vibration-isolated subframe mounting for Main Box |
| **Nyloc Nuts & Washers** | DIN 985 M4 Nyloc Nuts + DIN 125 A4 Washers | **4** | Secures silentblocks to motorcycle subframe tabs |

---

### 2.4 Category D: Gaskets, Venting & Light Pipes (IP67)

| Component | Specification | Qty | Location & Function |
| :--- | :--- | :---: | :--- |
| **Silicone Gasket Cord Main**| Silicone Solid Cord $\varnothing 1.5\,\text{mm}$ Shore 40A ($40\,\text{cm}$) | **1** | Perimeter tongue-and-groove seal on Central Main Box |
| **Silicone Gasket Cord Front**| Silicone Solid Cord $\varnothing 1.5\,\text{mm}$ Shore 40A ($30\,\text{cm}$) | **1** | Perimeter lid seal on Universal Front Node |
| **Cartridge Face Seals** | Molded Silicone Flange Seal Shore 40A ($54 \times 18\,\text{mm}$, $1.5\,\text{mm}$) | **3** | Mouth opening seal on Pod 1, 2, and 3 |
| **EPDM Slotted Cable Combs** | EPDM Slotted Cable Comb Block ($15 \times 8 \times 4\,\text{mm}$) | **2** | Waterproof cable feedthrough in Front Node |
| **Pressure Relief Vent** | Gore Automotive AVS 41 (M8x1.25 screw-in vent) | **1** | Pressure equalization & condensation prevention in Main Box lid |
| **ePTFE Adhesive Vents** | Gore IP67 Adhesive Vent Disc $\varnothing 6.0 \dots 7.0\,\text{mm}$ | **5** | 3x Pod vent bosses, 1x Front Node, 1x Knowles MEMS acoustic port |
| **Optical Light Pipe** | Bivar PLPC3-3MM or Mentor PMMA $\varnothing 3.0\,\text{mm}$ ($L=8\,\text{mm}$) | **1** | Waterproof transmission of WS2812B RGB LED through Main Box lid |

---

### 2.5 Category E: Pre-Molded COTS Cabling & Backup Battery (No Crimping!)

| Component | Specification / Type | Qty | Purpose & Function |
| :--- | :--- | :---: | :--- |
| **HD26 IP67 Breakout Harness**| Factory pre-molded HD26 breakout harness (Amphenol LTW COTS)| **1** | Main harness plug at Central Box, completely overmolded |
| **M8 6-Pin PUR Cables** | M8 6-Pin A-coded Male/Female (PUR, 1.0 m / 1.5 m) | **3** | Standard sensor/actuator cables to Pods 1, 2, and 3 |
| **M8 4-Pin PUR Cable** | M8 4-Pin A-coded Male/Female (PUR, 0.5–1.5 m) | *Opt. (1)* | Pigtail 5: Rear Radar (Garmin Varia: 12V + UART) or Rear OBD2/CAN (only when using radar or as hardwired fallback) |
| **Front Node Power Pigtail** | Pre-crimped JST-PH 2-Pin lead with Posi-Tap connectors | **1** | Local 12V power tap at cockpit (parking light / nav plug) – *Front Node connects wirelessly via ESP-NOW / BLE!* |
| **UPS Backup Battery** | 1S 3.7V LiPo 1000 mAh with NTC & Molex Micro-Fit 3.0 | **1** | Seamless UPS power reserve inside Main Box (plug-in) |
| **Automotive Fuse Cable** | Waterproof Mini-Blade Inline Fuse Holder with 2A Fuse | **1** | Protects permanent 12V supply (KL30) directly at battery terminal |
| **J_ACT Actuator Harness** | Pre-crimped 8-Pin JST-SH to 4x 2-Pin silicone leads ($8\,\text{cm}$)| **1–2** | Pre-molded wiring harness for the 4 miniature actuators |
| **Miniature Actuators** | 5V DC Push/Pull Solenoids ($\varnothing 6.5 \times 12\,\text{mm}$) + TPU tip | **4–8** | Mechatronic button actuation (4 per Smart Cartridge) |
| **J2 Gateway Harness** | Pre-crimped 6-Pin JST-SH to Audio & DC interface | **1–2** | Modular cartridge harness (Sena or Cardo Air-Mount) |

---

### 2.6 Category F: Minimalist Tool List (The True IKEA Principle)

Because **no soldering, no crimping, and no thermal thread-embedding** are required, standard household tools are all that is needed:

| Tool | Size / Specification | Purpose during Assembly |
| :--- | :--- | :--- |
| **Hex Key Set** | **1.5 mm / 2.0 mm / 2.5 mm / 3.0 mm** | Tightening all enclosures, boards, and clamps |
| **Torx / Screwdriver** | **TX10 / PH1** | Enclosure lid and anti-theft locking screw |
| **Wrench / Socket** | **SW 7 mm / SW 8 mm** | Countering M4/M5 nuts on tube clamps |
| **Scissors / Cutter** | Standard | Sizing silicone gasket cord to length |
| **Silicone Grease** | Liqui Moly / OKS 1110 (small tube) | Light coating on enclosure gaskets |

> [!TIP]
> **No soldering iron, no heat gun, no specialized micro-crimping pliers, and no insert melting tips required.** All mechanical and electronic assemblies are exclusively snapped, plugged, and bolted!

---

## 3. Subsystem Assembly Steps (Step-by-Step)

### Step 1: Central Main Box Assembly
1. **Insert Nuts (Nut-Pockets):** Press 4x DIN 934 / DIN 985 M3 stainless steel nuts into the hexagonal nut pockets in the lower tub from underneath.
2. **Install Main PCB:** Seat the factory-assembled PCBA 01 (`kicad_main_box`) onto the damping standoffs and secure with 4x M2.5 $\times 6\,\text{mm}$ screws finger-tight.
3. **Mid Tray & Battery:** Place the mid tray on top, lay the 1000 mAh LiPo battery into the tray, plug the Molex Micro-Fit connector into `J_BAT`, and secure with the EPDM strap.
4. **Gasket & Lid:** Lay the $\varnothing 1.5\,\text{mm}$ silicone gasket cord into the lid perimeter groove, adhere the Gore vent, and tighten the 4x M3 $\times 40\,\text{mm}$ screws in a cross pattern ($0.8\,\text{Nm}$).

### Step 2: Satellite Pods 1, 2, and Rear Pod 3 (Base Housing & Bulkhead)
1. **Install Baseboard:** Slide factory-assembled PCBA 02 (`kicad_pod_base`) into the guide grooves of the pod base housing ([`pod_base_housing.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod_base_housing.stl)). Feed the M8 6-pin IP67 connector through the rear hole, seat the O-ring, and tighten the M8 hex nut from outside using an open wrench (SW 10) to $1.2\,\text{Nm}$.
2. **Insert Auto-Eject Springs:** Slide one A4 stainless steel compression spring ($\varnothing 4.5 \times 15\,\text{mm}$) into each of the two rear spring pockets of the bulkhead ([`03_pod_bulkhead_partition.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl)).
3. **Secure Bulkhead:** Push the bulkhead with springs forward into the pod housing until it rests against the stop shoulder. Fasten with 2x M2 $\times 8\,\text{mm}$ countersunk screws through the housing wall.
4. **Verification:** The spring-loaded Harwin 6-pin docking pogo pins must protrude centered and flush through the bulkhead aperture. Repeat for Pod 1, Pod 2, and Pod 3.

### Step 3: Multi-Protocol Gateway Cartridges 1 & 2 (e.g., Sena & Cardo)
> **Architecture Principle:** Slot 1 and Slot 2 are **Multi-Protocol Gateway Transceivers**, not isolated driver/passenger headsets! They connect the motorcycle simultaneously to Sena Mesh and Cardo DMC networks. Driver and passenger communicate wirelessly using their standard helmets.

1. **Install PCB:** Snap the cartridge carrier PCBA 03 Rev 2.0 into the cartridge sled ([`cartridge_base_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl)).
2. **Mount Gateway Inlay & Mechatronics (by device class):**
   * **Class S (Smart Modular Cartridge with Mechatronics • OMB Reference: Sena SPIDER X Slim / Cardo Packtalk Edge):**
     * Place 4x miniature actuators ($\varnothing 6.5 \times 12\,\text{mm}$) with attached flexible TPU tips into the guide bridge of the inlay ([`cartridge_insert_sena.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) or [`cartridge_insert_cardo.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl)).
     * Place the actuator retainer plate on top and secure with 4x M2 $\times 6\,\text{mm}$ countersunk screws.
     * Connect the pre-molded 8-pin JST-SH cable `J_ACT` directly from the actuators to header `J_ACT` on PCBA 03 (zero crimping or soldering!).
     * Place the headset into the form-fit PA12 contour bed and lock with the tool-free quick-release clamp.
     * Plug the pre-molded J2 power cable (3.85V continuous direct feed or ribbon USB) into header `J2`.
   * **Class A (Sena +Mesh B2M-01 / MeshPort Adapter):**
     * Slide the adapter laterally into the transverse slide rails of the inlay until the snap latch locks.
     * Connect low-profile 90° USB power cable (continuous 5V supply).
     * Connect coaxial pigtail to SMA bulkhead port on front face.
     * Secure against shock with elastic EPDM retention strap.
   * **Class D (Hermetic Blank Cartridge):**
     * Insert blank sled [`cartridge_insert_blindkassette.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_blindkassette.stl) with solid faceplate and O-ring when a slot is unused or used as a waterproof storage box.
3. **Flange Gasket:** Slide the molded silicone face seal over the cartridge collar and lightly coat with dielectric silicone grease.

### Step 3.1: Magnetic Anti-Theft Lock & Ejector Mechanism (Rocker Latches)

```
                       MAGNETIC ANTI-THEFT LOCK & AUTO-EJECT KINEMATICS
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ [STATE 1: LOCKED]                                                                      │
│ Compression spring pushes lever arm ──► 1st class rocker pivots on M2 pin ──► Sawtooth │
│ claw swings 2.5 mm outward into housing notch. 90° stop face blocks extraction 100%!   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [STATE 2: UNLOCK & FAST EJECTION]                                                      │
│ External N52 neodymium key held to housing mark ──► Pulls Ø 6x8 mm steel armature out ──►│
│ Sawtooth retracts flush ──► 2x stainless compression springs eject cartridge 25 mm!    │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **Press Steel Armature:** Press the hardened steel pin ($\varnothing 6 \times 8\,\text{mm}$, DIN 6325) flush into the transverse hole of the rocker lever arm ([`cartridge_magnetic_lock_latch.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_magnetic_lock_latch.stl)).
2. **Insert Return Spring:** Insert the small $\varnothing 3.5 \times 10\,\text{mm}$ stainless spring into the inner pocket of the rear lever arm.
3. **Mount Rocker in Sled:** Place the pre-assembled rocker into the slot on the left guide cheek of the sled ([`cartridge_base_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl)). Push the $\varnothing 2.0 \times 8\,\text{mm}$ stainless pin (DIN 7) through the pivot hole from above.
4. **Pre-Insertion Functional Test:**
   * The locking claw on the front arm must protrude $2.5\,\text{mm}$ beyond the guide tongue under spring tension.
   * Hold the N52 block magnet outside adjacent to the steel pin: The rocker pivots by $-4.8^\circ$, and the claw retracts completely flush into the sled.

### Step 4: Rear Pod 3 Cartridge & OMM Radome (LoRa, GNSS & Triple Coaxial Bypass)
1. **Mount Transceiver PCB:** Seat PCBA 04 (`kicad_rear_pod3`) into the 3rd base sled ([`cartridge_base_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl)) and secure with M2.5 screws.
2. **Mount OMM Radome:** Position the dielectric radome ([`cartridge_antenna_bracket_omm.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_antenna_bracket_omm.stl)) on top.
3. **Install SMA Bulkhead Connectors (External Antenna Bypass Option):**
   * Feed the 3x SMA flange bulkheads through the $\varnothing 6.5\,\text{mm}$ holes in the faceplate from outside (integrated O-ring seals).
   * Fasten lock washer and nut (SW 8) from inside to $0.8\,\text{Nm}$.
   * Using plastic tweezers, snap the Murata MM8030 coaxial plugs vertically onto the SMD switch receptacles:
     * `J3` $\rightarrow$ 2.4 GHz OpenMotorMesh Bypass
     * `J4` $\rightarrow$ 868 MHz Semtech SX1262 LoRa Bypass
     * `J5` $\rightarrow$ Multi-GNSS u-blox M9N Bypass (3.3V phantom power)
4. **Automatic Switch Mechanism:**
   * **Internal Antennas (Standard):** Knurled brass IP67 caps installed. Internal antennas operate 100% inside radome.
   * **External Antennas:** Threading an external antenna automatically decouples internal antennas ($> 25\,\text{dB}$ isolation).

### Step 4.1: Adventure Kit Bike Mounting (BMW GS vs. BMW GSA / Enduro)

```
                            OPENMOTORBRIDGE ADVENTURE-KIT MOUNTING SUITE
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ BMW R1250 / R1300 GS (STANDARD)                                                        │
│ • Transition Dock (adventure_transition_dock.stl) in seat crease (Ø 28 mm tube)        │
│ • 100% luggage-independent – does not protrude beyond bike silhouette                  │
│ • Rack-Tail Mount (adventure_rack_tail_mount.stl) on OEM luggage rack                  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ BMW R1250 / R1300 GSA (ADVENTURE / TOURATECH PANNIER RACKS)                            │
│ • Tubular rack clamp cage (adventure_pannier_rack_clamp_base.stl + cap.stl)            │
│ • Mounts Pods 1 & 2 protected inside rack triangle (Ø 18 mm stainless tube)           │
│ • Tail Balcony luggage cantilever extends 65 mm behind aluminum topcase:               │
│   360° clear RF line-of-sight for LoRa/Mesh + 45° branch deflector fin for woods       │
│ • 36-tooth Hirth gear lock & Garmin Varia radar dock with anti-theft set screw         │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **BMW GS (Standard) Installation:**
   * **Pods 1 & 2:** Clamp transition docks ([`adventure_transition_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_transition_dock.stl)) beneath seat crease to frame tubes (Ø 28 mm). Route M8 PUR cables through lower channel directly under seat to Main Box.
   * **Pod 3:** Fasten onto rack-tail mount ([`adventure_rack_tail_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_rack_tail_mount.stl)) on luggage rack.
   * **Cockpit & Front-Node Fairing Disassembly (Wireless Connection):**
     * Remove 4x Torx T25 windshield mounting screws and lift off windscreen.
     * Unclip upper TFT cockpit shroud forward out of retaining tabs.
     * Secure Front Node via AMPS mount or tube clamp to handlebar / nav bar.
     * **Zero Cables Through Steering Head:** The Front Node communicates 100% wirelessly over the integrated 2.4 GHz wireless link (ESP-NOW / BLE, latency < 1.8 ms) with the Central Box under the seat.
     * Local Power: Plug the 2-pin JST-PH power lead directly into the OEM BMW Cartool nav connector (or parking light KL15 ignition + ground) in the cockpit. Optionally connect the 3-pin JST-PH lead to local front CAN/LIN.
2. **BMW GSA (Adventure) Installation:**
   * **Pods 1 & 2:** Wrap 1.0 mm EPDM strip around Ø 18 mm rack tube. Fasten clamp base ([`adventure_pannier_rack_clamp_base.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_pannier_rack_clamp_base.stl)) and cap ([`adventure_pannier_rack_clamp_cap.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_pannier_rack_clamp_cap.stl)) using 2x M5 x 30 mm stainless bolts and Nyloc nuts to $4.5\,\text{Nm}$. Bolt pod base housing to clamp eyelets.
   * **Pod 3 & Radar (Tail Balcony):** Bolt cantilever ([`adventure_rack_tail_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_rack_tail_mount.stl)) with 4x M6 bolts to rear rack. Align antenna along 45° fin.
   * **Radar Varia Dock:** Insert Garmin Varia dock tongue ([`radar_varia_gopro_lock_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_varia_gopro_lock_dock.stl)) into Hirth rosette ([`011_gopro_hirth_lock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/011_gopro_hirth_lock.stl)) in $10^\circ$ increments for level horizon. Lock with M5 x 25 mm bolt and nut ($3.5\,\text{Nm}$). Click Varia into bayonet and tighten M3 set screw.

### Step 4.2: Harley-Davidson Kit Bike Mounting (Classic Touring vs. CVO ST / Performance Bagger)

```
                       OPENMOTORBRIDGE HARLEY-DAVIDSON MOUNTING SUITE
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ HARLEY-DAVIDSON TOURING & BAGGER (CLASSIC: STREET GLIDE, ROAD GLIDE, ROAD KING)        │
│ • Saddlebag lid docks (saddlebag_lid_dock.stl) on hard bags (Pod 1 & Pod 2)           │
│ • Touring fender console (pod3_touring_fender_console.stl) streamlined on rear fender  │
│ • License plate radar mount (radar_license_plate_bracket.stl) decoupled under plate    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ HARLEY-DAVIDSON CVO ROAD GLIDE ST / PERFORMANCE BAGGER                                 │
│ • Under-Cowl skeleton dock (cvo_st_undercowl_skeleton_dock.stl) under solo seat cowl:  │
│   Shields from exhaust heat and clears Showa remote reservoir shock canisters          │
│ • CVO ST telemetry fin (cvo_st_telemetry_fin.stl) as shark fin on rear tab            │
│ • Centered under-fender mount (radar_center_underfender_mount.stl) for side-mount plates│
└────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **Classic Touring Installation & Fairing Disassembly:**
   * **Pods 1 & 2:** Mount saddlebag lid docks ([`saddlebag_lid_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/saddlebag_lid_dock.stl)) using M4 countersunk screws with sealing washers at OEM points or via 3M VHB tape. Route M8 cable through grommet to quick-disconnect at frame.
   * **Pod 3:** Center and fasten fender console ([`pod3_touring_fender_console.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod3_touring_fender_console.stl)) flat onto rear fender.
   * **Radar:** Fasten license plate bracket ([`radar_license_plate_bracket.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_license_plate_bracket.stl)) beneath license plate frame.
   * **Fairing Disassembly (Street Glide Batwing) & Local Hookup:**
     * Remove 3x Torx T27 windshield screws (center screw last).
     * Remove 4x Torx T27 screws on the inner fairing (2x below instruments, 2x beside speakers).
     * Carefully tilt outer fairing forward, disconnect main headlight multi-plug.
     * Bolt Front Node to handlebar riser.
     * Local Power: Tap the 2-pin JST-PH power lead directly into the internal fairing accessory plug (or parking light KL15 switched power). **No wiring harness through the tank tunnel is required**, as the Front Node connects 100% wirelessly to the Central Box via ESP-NOW / BLE!
     * Reinstall outer fairing and torque T27 screws to $3.8\,\text{Nm}$.
2. **CVO ST / Performance Bagger Installation (Road Glide Sharknose):**
   * **Pods 1 & 2:** Mount upright skeleton dock ([`cvo_st_undercowl_skeleton_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/cvo_st_undercowl_skeleton_dock.stl)) under solo seat cowl. Pods stand vertically, clearing suspension remote reservoirs.
   * **Pod 3:** Mount telemetry fin ([`cvo_st_telemetry_fin.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/cvo_st_telemetry_fin.stl)) on rear cowl tab.
   * **Radar:** Mount centered under-fender plate ([`radar_center_underfender_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_center_underfender_mount.stl)) under shortened rear fender.
   * **Sharknose Fairing Disassembly:** Remove turn signal bolts, back out 4x T27 inner fairing screws, lift off Sharknose outer fairing forward. Mount Front Node in media compartment / riser and connect locally to 12V switched power.

---

## 5. Universal Front Node Assembly & Vehicle Installation

### 5.1 Front Node Box Assembly (100% Solder-Free & Zero Melting)
1. **Insert Captive Nuts (Nut-Pockets):**
   * Press 4x DIN 934 / DIN 985 M3 stainless nuts into the corner nut pockets of the lower tub ([`front_node_lower_tub.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_lower_tub.stl)).
   * Insert 4x DIN 934 M4 nuts into the rear hex pockets of the AMPS pattern ($30 \times 38\,\text{mm}$) at the tub floor.
2. **Acoustic Membrane:** Adhere hydrophobic Gore ePTFE acoustic membrane over the Knowles MEMS microphone port.
3. **Mount Circuit Board:** Fasten factory-assembled PCBA 05 (`kicad_front_node`) using 4x M2.5 screws finger-tight.
4. **RF Antenna Installation (ESP32-S3 2.4 GHz):**
   * Adhere flexible 2.4 GHz FPC dipole antenna (Molex 146153) into the lid pocket ([`front_node_upper_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_upper_lid.stl)).
   * Snap micro-coax U.FL connector vertically onto ESP32-S3 module.
5. **Insert Pre-Molded COTS Cables (Zero Crimping!):**
   * **Front Opening (South Wall for USB):**
     * Short USB-A flat ribbon cable to Port `J6` (switched VBUS for CarPlay dongle / Ottocast).
     * 1.0 m USB-C cable to Port `J5` (glovebox phone charging).
     * USB host cable to `J4`.
   * **Right Opening (East Wall):** Insert elastomeric dust cap ([`front_node_usbc_cap_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_usbc_cap_tpu.stl)) into service port `J7`.
   * **Left Opening (West Wall for Power & Signals):**
     * Pre-crimped JST-PH 2-pin lead for 12V supply (KL15 & GND) to `J1`.
     * Pre-crimped JST-PH 3-pin lead for CAN-Bus to `J2`.
     * Pre-crimped JST-PH 2-pin lead from handlebar switch to `J3` (PTT).
6. **Insert Cable Glands & Fasten Lid:**
   * Apply light film of silicone grease to TPU cable glands ([`front_node_cable_glands_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_cable_glands_tpu.stl)) and push into housing pockets.
   * Seat silicone gasket cord (Ø 1.5 mm, $30\,\text{cm}$) in lid groove.
   * Tighten lid with 4x M3 $\times 20\,\text{mm}$ screws in a cross pattern (threads into captive M3 nuts in nut pockets).

### 5.2 Motorcycle Mounting (4 Options)

```
┌────────────────────────────────────────────────────────────────────────┐
│               FRONT NODE 4-IN-1 MOUNTING OPTIONS                       │
├────────────────────────────────────────────────────────────────────────┤
│ Option 1: AMPS Pattern (30 x 38 mm)                                    │
│ • Bolts directly to RAM-Mount balls, Garmin brackets, nav towers       │
│ • Ideal for adventure bikes and naked bikes                            │
├────────────────────────────────────────────────────────────────────────┤
│ Option 2: 120° V-Groove Tube Saddle with EPDM O-Rings                  │
│ • Toolless attachment to Ø 22 mm to Ø 32 mm crash bars (BMW GS/RT)     │
│ • Vibration-isolated, will not scratch powdercoat                      │
├────────────────────────────────────────────────────────────────────────┤
│ Option 3: M4 Silentblocks                                              │
│ • Vibration-isolated screw mounting inside the fairing beak            │
├────────────────────────────────────────────────────────────────────────┤
│ Option 4: 3M Dual-Lock Recesses                                        │
│ • Concealed attachment inside Harley Batwing / Sharknose fairings      │
└────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Electrical Connections (Plug-and-Play)
* **12V Vehicle Power:** Single 2-core wire (KL15 switched ignition and ground) tapped from parking light or accessory plug.
* **Ottocast Dongle:** Plugs into USB-A Port `J6` and mounts with 3M Dual-Lock inside fairing.
* **Glovebox Extension:** USB-C cable from Port `J5` leads to glovebox for phone charging.
* **Handlebar PTT:** 2-wire lead from handlebar momentary button leads to socket `J3` (GPIO 0).

---

## 6. First Commissioning, WebSerial 1-Click Flasher & Smoke-Test

Thanks to the modern **WebSerial integration** within the OpenMotorBridge PWA, initial commissioning requires **no installation of Python, PlatformIO, drivers, or terminal tools**:

### 6.1 Method A: WebSerial 1-Click Installer (Recommended for End Users)
1. Connect Main Box to PC/Mac/Laptop via standard USB-C cable.
2. Open Chrome, Edge, or Opera and launch the PWA (or open locally via the System Builder).
3. In the *System Builder* tab, click **"Connect USB-C & Flash"**.
4. Select the detected serial port (e.g. `CP2102N` / `ESP32-S3`).
5. The PWA flashes bootloader, partition table, firmware (`openmotorbridge_main_v8.12.bin`), and SPIFFS filesystem fully automatically with progress bar and live log.

### 6.2 The Guided 4-Point IKEA Smoke-Test
Before screwing on the enclosure lid, execute the interactive self-test in the PWA:
1. [x] **Vehicle Power & UPS (Check 1):** 12.6V battery voltage, 5.04V buck rail, UPS LiPo at 4.18V.
2. [x] **Cartridges & Actuators (Check 2):** 1-Wire DS2431 cartridge ID readout (Sena / Cardo), pogo pin contact integrity, and automated 4-actuator click sequence (Clicks 1 to 4).
3. [x] **Front Node & Cockpit (Check 3):** I2C ping Knowles MEMS microphone, SDP31 dynamic air pressure sensor (0.02 hPa), and handlebar PTT button.
4. [x] **Rear Pod 3 (Check 4):** SX1262 LoRa 868 MHz ping-echo and u-blox GNSS 3D fix.

### 6.3 Method B: Manual Flashing via PlatformIO (Power-User Fallback)
```bash
# 1. Flash Central Main Controller via USB-C (ESP32-S3)
cd openMotorBridge/firmware/main_controller && pio run --target upload && pio run --target uploadfs
# 2. Flash Rear Tail Coprocessor (RP2040 in Pod 3)
cd ../rear_coprocessor && pio run --target upload
# 3. Flash Front Node (ESP32-S3)
cd ../front_node && pio run --target upload
```

---

## 7. Maintenance & Care

* **Gasket Inspection:** Lubricate the silicone O-ring cords on the Main Box, Front Node, and pod cartridges once per season with dielectric silicone grease.
* **Venting Integrity:** Verify that the ePTFE Gore vents are clean and unobstructed by mud or road grime.
* **Firmware Updates:** Wireless and modular in-system updates are directly performed via the Web Bluetooth PWA dashboard.
