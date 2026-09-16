# 16 - Build Instructions, Wiring & Vehicle Installation

This document is the comprehensive, hands-on assembly guide for assembling and installing a complete **OpenMotorBridge (v8.0)** hardware system on a motorcycle.

---

## 1. Kit Architecture Overview (What Are We Building?)

A complete OpenMotorBridge motorcycle installation comprises:

```text
                      ┌─────────────────────────────────────────┐
                      │    1x CENTRAL MAIN BOX (IP67)           │
                      │    (Under-seat / tail frame)            │
                      │    • Lower case + mid tray + lid        │
                      │    • Main PCB (ESP32-S3, Codec, UPS)    │
                      │    • 2,200 mAh LiPo backup battery      │
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
                                 │ • AMPS / Tube Clamp Mount        │
                                 │ • CarPlay/AA Dongle Port (USB-A) │
                                 │ • Smartphone USB-PD Fast Charger │
                                 │ • Knowles MEMS Acoustic Sensor   │
                                 │ • Battery-Free Handlebar PTT     │
                                 └──────────────────────────────────┘
```

---

## 2. Pre-Assembly Checklist

All parts, circuit board production files, and COTS procurement links are cataloged in **[Chapter 15: Bill of Materials & Manufacturing Data](file:///Users/schmidtm/openMotorBridge/docs/en/15_bom_manufacturing.md)**. Before beginning assembly, verify that all necessary components are present:

* [ ] **3D Printed Components (MJF PA12 Black or FDM ASA/PET-CF):**
  * 1x Main Box (Lower case, mid-tray with 2,200 mAh LiPo pocket, lid)
  * 3x Pod base housings & 3x Pod bulkheads
  * 3x Cartridge base sleds, inlays (e.g., Sena, Cardo, or Blank) & 2x locking latches
  * 1x Rear Pod 3 OMM radome
  * 1x Front Node (Lower tub with AMPS nut pockets, lid, TPU cable glands & USB-C cap)
  * 1x Bike-specific mounting kit (BMW GS clamps / Harley saddlebag lid docks)
* [ ] **Turnkey Factory-Assembled Circuit Boards (JLCPCB / Eurocircuits):**
  * 1x PCBA 01 (Central Box), 3x PCBA 02 (Pod Base), 2x PCBA 03 (Cartridge), 1x PCBA 04 (Rear Pod 3), 1x PCBA 05 (Front Node)
  * *(Optional: PCBA 06 MagSafe Dock, PCBA 07 Smart Keyfob)*
* [ ] **V4A Stainless Hardware & Springs (IKEA Principle – 100% Solder-Free):**
  * 8x DIN 934 / DIN 985 M3 stainless nuts (for enclosure nut pockets)
  * 4x DIN 934 M4 nuts (for AMPS nut pockets in Front Node tub)
  * 4x M3 x 40 mm socket head screws (Central Box), 4x M3 x 20 mm screws (Front Node)
  * 8x M2.5 x 6 mm PCB screws, 6x M2 x 8 mm countersunk (bulkheads), 8x M2 x 6 mm (cartridges)
  * 2x DIN 7 M2 x 8 mm dowel pins (rocker pivots), 2x DIN 6325 Ø 6 x 8 mm hardened steel pins
  * 2x Rocker return springs, 6x Auto-eject compression springs, 1x N52 magnetic release key
* [ ] **Gaskets & Backup Battery:**
  * Silicone solid cord Ø 1.5 mm Shore 40A ($40\,\text{cm}$ Central Box, $30\,\text{cm}$ Front Node)
  * 3x Silicone face seals for Pod mouths, Gore ePTFE adhesive membrane discs
  * **1x 1S LiPo Flat-Pack 2,200 mAh** ($68 \times 39 \times 5.0\,\text{mm}$, Type 504068 / 503870) with Molex Micro-Fit 3.0 connector
* [ ] **Pre-Molded COTS Wiring Harnesses (No Crimping Required):**
  * 1x HD26 IP67 harness whip, 3x M8 6-Pin PUR cables (1.0 m / 1.5 m)
  * 1x 2-Pin JST-PH power lead with Posi-Tap connectors (cockpit 12V switched power & ground)
  * JST-SH cartridge harnesses (8-Pin `J_ACT` for solenoids, 6-Pin `J2` for audio/DC)
* [ ] **Tools:**
  * Hex key set (1.5 / 2.0 / 2.5 / 3.0 mm), Torx TX10 / PH1 screwdriver, wrench SW 7 / 8 mm, utility cutter, silicone grease

---

## 3. Step-by-Step Assembly Instructions

### Step 1: Central Box (Main Box) Assembly
1. **Insert Captive Nuts:** Press 4x DIN 934 / DIN 985 M3 stainless nuts from below into the captive hexagonal nut pockets of the lower case ([`main_box_lower_case.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lower_case.stl)).
2. **Mount Main Board:** Place the assembled PCBA 01 (`openmotorbridge_central_box`) onto the vibration-damping bosses and secure with 4x M2.5 $\times 6\,\text{mm}$ screws finger-tight.
3. **Mid Tray & 2,200 mAh LiPo Battery:** Place the mid-tray ([`main_box_mid_tray.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_mid_tray.stl)). Lay the **2,200 mAh Flat-LiPo battery** ($68 \times 39 \times 5.0\,\text{mm}$) into the tray pocket, route the Molex Micro-Fit cable through the partition cutout to `J_BAT`, and secure the battery with an EPDM damper strip.
4. **Gasket & Lid:** Coat silicone cord (Ø 1.5 mm, $40\,\text{cm}$) lightly with silicone grease and seat in the lid groove. Stick the Gore ePTFE membrane over the vent boss. Position the lid ([`main_box_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lid.stl)) and tighten the 4x M3 $\times 40\,\text{mm}$ screws in a cross pattern ($0.8\,\text{Nm}$).

---

### Step 2: Satellite Pods 1, 2, and Rear Pod 3 Assembly
1. **Insert Baseboard:** Slide the assembled PCBA 02 (`openmotorbridge_pod_base`) into the internal guide rails of the Pod chassis ([`pod_base_housing.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod_base_housing.stl)). Guide the M8 6-Pin IP67 connector through the rear port, seat the O-ring, and tighten the M8 nut externally using a 10 mm wrench ($1.2\,\text{Nm}$).
2. **Install Auto-Eject Springs:** Insert a V4A compression spring ($\varnothing 4.5 \times 15\,\text{mm}$) into each of the two rear spring pockets of the bulkhead ([`03_pod_bulkhead_partition.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl)).
3. **Secure Bulkhead:** Slide the bulkhead into the chassis until it seats against the internal shoulder stop. Fasten with 2x M2 $\times 8\,\text{mm}$ countersunk screws through the outer shell flush.
4. **Verification:** The spring-loaded Harwin 6-Pin docking pogo pins must protrude centered and square through the bulkhead window. Repeat for Pod 1, Pod 2, and Pod 3.

---

### Step 3: Multi-Protocol Gateway Cartridges 1 & 2 Assembly (e.g., Sena & Cardo)
> **Architecture Principle:** Slot 1 and Slot 2 are **Multi-Protocol Mesh Gateway Transceivers**, not separate rider/passenger headsets. One module (e.g., Sena SPIDER X Slim in Slot 1) bridges to the Sena Mesh network, while the second module (e.g., Cardo Packtalk Edge in Slot 2) concurrently bridges to the Cardo DMC network. The Central Box digitally routes audio between both wireless domains.

1. **Insert Board:** Snap the PCBA 03 Rev 2.0 cartridge board into the cartridge sled ([`cartridge_base_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl)).
2. **Mount Gateway Inlay & Mechatronics:**
   * **Class S (Smart Modular Cartridge with Mechatronics • Sena SPIDER / Cardo Packtalk):**
     * Insert 4x miniature solenoids ($\varnothing 6.5 \times 12\,\text{mm}$) with TPU tips into the guide frame of the inlay ([`cartridge_insert_sena.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) or [`cartridge_insert_cardo.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl)).
     * Place the actuator retainer plate and secure with 4x M2 $\times 6\,\text{mm}$ countersunk screws.
     * Plug pre-crimped 8-pin JST-SH cable `J_ACT` from the solenoids directly to header `J_ACT` on PCBA 03.
     * Seat the headset into the contoured cavity and secure with the quick-release clamp.
     * Connect pre-crimped J2 power/audio cable.
   * **Class D (Hermetic Blank Cartridge):**
     * Insert blank sled [`cartridge_insert_blindkassette.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_blindkassette.stl) if a slot is temporarily unused or serves as a waterproof dry storage box.
3. **Flange Gasket:** Stretch the molded silicone face seal over the cartridge collar and lubricate lightly with silicone grease.

---

### Step 3.1: Magnetic Anti-Theft Rocker Mechanism

```text
                    MAGNETIC ANTI-THEFT LOCKING & EJECTION KINEMATICS
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ [State 1: LOCKED]                                                                      │
│ Compression spring preloads rocker ──► Rocker pivots on M2 pin ──► Sawtooth claw       │
│ extends 2.5 mm into chassis slot. 90° shear face blocks pull-out 100%!                 │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [State 2: UNLOCK & EJECT]                                                              │
│ External N52 neodymium key held to chassis mark ──► Pulls Ø 6x8 mm steel armature     │
│ outwards ──► Sawtooth claw retracts flush ──► 2x V4A springs kick cartridge out 25 mm! │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **Press-Fit Armature Pin:** Press the hardened steel pin ($\varnothing 6 \times 8\,\text{mm}$, DIN 6325) flush into the lateral cross-hole of the rocker latch ([`cartridge_magnetic_lock_latch.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_magnetic_lock_latch.stl)).
2. **Seat Return Spring:** Place the small $\varnothing 3.5 \times 10\,\text{mm}$ spring into the inner pocket of the rocker.
3. **Mount Rocker in Sled:** Insert the pre-assembled rocker into the slot on the left guide rail of the sled ([`cartridge_base_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl)). Press the $\varnothing 2.0 \times 8\,\text{mm}$ stainless dowel pin (DIN 7) through the pivot bore from above.
4. **Test Function:**
   * The sawtooth claw must protrude $2.5\,\text{mm}$ under spring tension.
   * Applying the N52 magnet to the armature height tilts the rocker by $-4.8^\circ$, retracting the claw completely flush into the sled.

---

### Step 4: Rear Pod 3 Cartridge & OMM Radome (LoRa, GNSS & RF Bypass)
1. **Mount Transceiver Board:** Install PCBA 04 (`openmotorbridge_rear_pod3`) into the 3rd base sled ([`cartridge_base_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl)) with M2.5 screws.
2. **Mount OMM Radome:** Snap the dielectric radome ([`cartridge_antenna_bracket_omm.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_antenna_bracket_omm.stl)) in place.
3. **Mount SMA Bulkhead Jacks (Bypass for External Antennas):**
   * Pass the 3x SMA flange jacks through the cartridge front wall and tighten ($0.8\,\text{Nm}$).
   * Click micro-coax leads onto Murata MM8030 switch jacks (`J3` = 2.4 GHz Mesh, `J4` = 868 MHz LoRa, `J5` = GNSS).
   * When no external antennas are connected, the internal radome patch and helical antennas operate 100% autonomously.

---

### Step 4.1: Adventure Kit Mounting (BMW GS vs. BMW GSA / Enduro)

```text
                             OPENMOTORBRIDGE ADVENTURE-KIT MOUNTING SUITE
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ BMW R1250 / R1300 GS (STANDARD)                                                        │
│ • Transition-Dock (adventure_transition_dock.stl) in the seat crease (Ø 28 mm tube)    │
│ • 100% luggage-independent – zero protrusion beyond bike silhouette                    │
│ • Rack-Tail Mount (adventure_rack_tail_mount.stl) bolted to OEM luggage rack           │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ BMW R1250 / R1300 GSA (ADVENTURE / STAINLESS PANNIER RACKS)                            │
│ • Pannier cage clamp pair (adventure_pannier_rack_clamp_base.stl + cap.stl)            │
│ • Mounts Pod 1 & 2 protected inside frame triangle (Ø 18 mm stainless tube)            │
│ • Tail Balcony luggage cantilever extends 65 mm behind aluminum topcase                │
│ • 36-tooth Hirth gear lock & Garmin Varia radar dock with grub screw                   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **BMW GS (Standard) Installation:**
   * **Pod 1 & 2:** Clamp transition docks ([`adventure_transition_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_transition_dock.stl)) onto frame tubes (Ø 28 mm) below seat lip. Route M8 cables along under-seat channels to Central Box.
   * **Pod 3:** Fasten onto rack tail mount ([`adventure_rack_tail_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_rack_tail_mount.stl)) on rear luggage bridge.
   * **Cockpit & Front Node Fairing Disassembly:**
     * Remove 4x Torx T25 windshield screws and lift windscreen off.
     * Unclip upper TFT cockpit surround forwards.
     * Mount Front Node using AMPS bolts or tube clamps to handlebar / GPS bar.
     * **No wiring run through the steering stem:** The Front Node connects 100% wirelessly to the Central Box under the seat via 2.4 GHz ESP-NOW / BLE (< 1.8 ms latency).
     * Local power: Connect the 2-pin JST-PH power lead directly to the BMW Cartool nav connector (or parking light 12V switched & ground) in the cockpit.
2. **BMW GSA (Adventure) Installation:**
   * **Pod 1 & 2:** Wrap 1.0 mm EPDM strip around Ø 18 mm tube. Clamp base ([`adventure_pannier_rack_clamp_base.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_pannier_rack_clamp_base.stl)) and cap ([`adventure_pannier_rack_clamp_cap.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_pannier_rack_clamp_cap.stl)) using 2x M5 x 30 mm V4A screws and DIN 985 locknuts ($4.5\,\text{Nm}$). Bolt Pod base to clamp tabs.
   * **Pod 3 & Radar:** Bolt cantilever ([`adventure_rack_tail_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_rack_tail_mount.stl)) to rear luggage bridge.
   * **Radar Varia Dock:** Seat Garmin Varia dock ([`radar_varia_gopro_lock_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_varia_gopro_lock_dock.stl)) into Hirth rosette ([`011_gopro_hirth_lock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/011_gopro_hirth_lock.stl)) ($10^\circ$ increments for level horizon). Secure with M5 x 25 mm screw and locknut ($3.5\,\text{Nm}$). Slide Varia in and turn M3 grub screw to lock.

---

### Step 4.2: Harley-Davidson Mounting Suite (Touring vs. CVO ST vs. Custom/Bobber)

```text
                       OPENMOTORBRIDGE HARLEY-DAVIDSON MOUNTING SUITE
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ HARLEY-DAVIDSON TOURING & BAGGER (STREET GLIDE, ROAD GLIDE, ROAD KING)                 │
│ • Saddlebag lid docks (saddlebag_lid_dock.stl) on hard bags (Pod 1 & Pod 2)           │
│ • Touring fender console (pod3_touring_fender_console.stl) contoured on rear fender   │
│ • License plate radar mount (radar_license_plate_bracket.stl) decoupled below plate    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ HARLEY-DAVIDSON CVO ROAD GLIDE ST / PERFORMANCE BAGGER                                 │
│ • Under-cowl skeleton dock (cvo_st_undercowl_skeleton_dock.stl) under solo cowl:       │
│   Full clearance from Showa remote reservoir canisters                                 │
│ • CVO ST telemetry fin (cvo_st_telemetry_fin.stl) as tail sharkfin                     │
│ • License plate radar mount (radar_license_plate_bracket.stl): Identical bracket to     │
│   Touring models, as CVO ST uses the stock centered license plate mount!               │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ CUSTOM BIKES, BOBBERS & UNIVERSAL (SIDE-MOUNTED LICENSE PLATE)                         │
│ • Centered under-fender plate (radar_center_underfender_mount.stl) mounted beneath     │
│   rear fender for unobstructed 140° radar field of view with side-mount plates         │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **Classic Touring Installation & Fairing Removal:**
   * **Pod 1 & 2:** Mount saddlebag lid docks ([`saddlebag_lid_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/saddlebag_lid_dock.stl)) using M4 countersunk screws and sealing washers or 3M VHB tape. Route M8 cable through grommet into bag and via quick-disconnect to frame.
   * **Pod 3:** Center and bolt fender console ([`pod3_touring_fender_console.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod3_touring_fender_console.stl)) flat on fender.
   * **Radar:** Fasten license plate mount ([`radar_license_plate_bracket.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_license_plate_bracket.stl)) beneath license plate frame.
   * **Batwing Fairing Removal (Street Glide):**
     * Remove 3x Torx T27 windshield screws (center screw last).
     * Remove 4x Torx T27 screws on inner fairing (2 below gauges, 2 beside speakers).
     * Lift outer fairing forward, disconnect headlight plug.
     * Mount Front Node to handlebar riser.
     * Connect local power: Plug 2-pin JST-PH power lead to fairing aux connector (or parking light 12V switched). **No wire run back through the tank tunnel**, as connection to Central Box is fully wireless via ESP-NOW / BLE!
     * Reinstall outer fairing and torque T27 screws to $3.8\,\text{Nm}$.
2. **CVO ST / Performance Bagger Installation (Road Glide Sharknose):**
   * **Pod 1 & 2:** Mount upright skeleton dock ([`cvo_st_undercowl_skeleton_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/cvo_st_undercowl_skeleton_dock.stl)) beneath solo seat cowl. Pods stand vertically, completely clearing Showa remote reservoirs.
   * **Pod 3:** Mount aerodynamic telemetry fin ([`cvo_st_telemetry_fin.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/cvo_st_telemetry_fin.stl)) on tail cowl.
   * **Radar:** CVO ST also uses the standard license plate bracket ([`radar_license_plate_bracket.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_license_plate_bracket.stl)), since the license plate is factory-centered!
   * **Sharknose Disassembly:** Remove turn signal bolts, remove 4x T27 inner screws, lift Sharknose fairing off. Mount Front Node in media compartment / riser and tap local 12V supply.
3. **Custom Bikes & Bobbers with Side-Mounted License Plates:**
   * For builds with an offset side-mount license plate, the centered under-fender plate ([`radar_center_underfender_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_center_underfender_mount.stl)) is bolted centered beneath the fender curve to ensure an unobstructed 140° radar sweep.

---

## 4. Universal Front Node Assembly & Installation

### 4.1 Assembling the Front Node (100% Solder-Free)
1. **Insert Captive Nuts (Nut Pockets):**
   * Press 4x DIN 934 / DIN 985 M3 stainless nuts from below into the corner nut pockets of the lower tub ([`front_node_lower_tub.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_lower_tub.stl)).
   * Press 4x DIN 934 M4 nuts into the hexagonal pockets of the AMPS pattern ($30 \times 38\,\text{mm}$) on the bottom of the tub.
2. **Affix Acoustic Disc:** Stick hydrophobic Gore ePTFE membrane disc over Knowles MEMS acoustic opening.
3. **Mount Board:** Fasten assembled Front Node board PCBA 05 (`openmotorbridge_front_node`) with 4x M2.5 screws finger-tight.
4. **RF Antenna Installation (ESP32-S3 2.4 GHz):**
   * Stick flexible 2.4 GHz FPC dipole antenna (Molex 146153) into the adhesive recess on the inside of the lid ([`front_node_upper_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_upper_lid.stl)).
   * Click micro-coax U.FL connector squarely onto the ESP32-S3 module.
5. **Connect Pre-Molded COTS Cables (No Crimping!):**
   * **Front Opening (South Wall for USB):**
     * Connect short USB-A flat ribbon cable to port `J6` (CarPlay Dongle / Ottocast).
     * Connect 1.0 m USB-C charging cable to port `J5` (glovebox).
     * Connect USB host cable to `J4`.
   * **Right Opening (East Wall):** Insert elastomeric dust plug ([`front_node_usbc_cap_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_usbc_cap_tpu.stl)) into port `J7`.
   * **Left Opening (West Wall for Power & Signals):**
     * Plug pre-crimped JST-PH 2-pin power lead for 12V bike supply (KL15 & Ground) into `J1`.
     * Optional: Plug JST-PH 3-pin lead for CAN-bus into `J2` (only needed for local cockpit CAN).
     * Plug pre-crimped JST-PH 2-pin lead from handlebar switch into `J3` (PTT).
6. **Insert Sealing Combs & Fasten Lid:**
   * Apply thin film of silicone grease to TPU cable glands ([`front_node_cable_glands_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_cable_glands_tpu.stl)) and slide into housing slots.
   * Seat silicone cord (Ø 1.5 mm, $30\,\text{cm}$) into lid groove.
   * Fasten lid with 4x M3 $\times 20\,\text{mm}$ screws in a cross pattern (threading into the captive M3 nuts in the pockets).

### 4.2 Front Node Bike Mounting Options
* **Option 1: AMPS Pattern (30 x 38 mm):** Direct bolt-on to RAM-Mount ball, Garmin cradle, or GPS bar (utilizing the 4x captive M4 nuts).
* **Option 2: 120° V-Cradle:** Toolless mounting on Ø 22 to Ø 32 mm handlebars / crash bars using EPDM strap rings.
* **Option 3: M4 Silentblocks:** Vibration-isolated stud mounting inside fairing nose.
* **Option 4: 3M Dual-Lock Hook-and-Loop:** Concealed mounting inside Harley Batwing / Sharknose inner fairings.

---

## 5. Commissioning, WebSerial 1-Click Flasher & Smoke Test

With **WebSerial integration** inside the OpenMotorBridge PWA, commissioning requires **zero installation of Python, PlatformIO, drivers, or terminal utilities**:

### 5.1 Method A: WebSerial 1-Click Installer (Recommended)
1. Connect Central Box via standard USB-C cable to PC/Mac/laptop.
2. Open Chrome, Edge, or Opera and load the PWA (or open locally).
3. In the *System Builder* tab, click **"Connect USB-C & Flash"**.
4. Select the detected serial port (e.g., `CP2102N` / `ESP32-S3`).
5. The PWA flashes bootloader, partition table, firmware (`openmotorbridge_main_v8.12.bin`), and SPIFFS filesystem with live progress reporting.

### 5.2 Guided 4-Point IKEA Smoke Test
Before fastening the lids permanently, start the interactive self-test in the PWA:
1. [x] **Power & UPS (Check 1):** 12.6V bike voltage, 5.04V buck rail, UPS LiPo (2,200 mAh) at 4.18V.
2. [x] **Cartridges & Actuators (Check 2):** 1-Wire DS2431 cartridge identification (Sena / Cardo), pogo-pin contact, and automated 4-actuator click test (clicks 1 to 4).
3. [x] **Front Node & Cockpit (Check 3):** I2C ping Knowles MEMS microphone, SDP31 differential pressure sensor (0.02 hPa), and handlebar PTT button.
4. [x] **Rear Pod 3 (Check 4):** SX1262 LoRa 868 MHz ping-echo and u-blox GNSS 3D fix lock.

### 5.3 Method B: Manual PlatformIO Flashing (Power-User Fallback)
```bash
# 1. Flash Main Controller via USB-C (ESP32-S3)
cd openMotorBridge/firmware/main_controller && pio run --target upload && pio run --target uploadfs
# 2. Flash Rear Co-Processor (RP2040 in Pod 3)
cd ../rear_coprocessor && pio run --target upload
# 3. Flash Front Node (ESP32-S3)
cd ../front_node && pio run --target upload
```

---

## 6. Maintenance & Care

* **Gasket Inspection:** Once per season, lubricate silicone cord on Main Box, Front Node, and cartridges lightly with dielectric silicone grease.
* **Breather Inspection:** Ensure Gore ePTFE membranes remain clean and clear of mud/debris.
* **Firmware Updates:** Perform wireless over-the-air updates directly via the WebBLE PWA interface.
