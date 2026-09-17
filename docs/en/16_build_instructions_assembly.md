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

### Step 5: Universal Front Node (PCBA 05) Assembly (100% Solder-Free)
1. **Insert Captive Nuts (Nut Pockets):**
   * Press 4x DIN 934 / DIN 985 M3 stainless nuts from below into the corner hexagonal nut pockets of the lower tub ([`front_node_lower_tub.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_lower_tub.stl)).
   * Press 4x DIN 934 M4 nuts into the hexagonal pockets of the AMPS hole pattern ($30 \times 38\,\text{mm}$) on the bottom of the tub.
2. **Affix Acoustic Membrane:** Stick hydrophobic Gore ePTFE membrane disc over the sound port of the digital MEMS acoustic sensor (MSM261S4030H0R / SPH0645).
3. **Mount Circuit Board:** Fasten turnkey assembled Front Node board PCBA 05 (`openmotorbridge_front_node`) with 4x M2.5 screws finger-tight.
4. **RF Antenna Installation (ESP32-S3 2.4 GHz):**
   * Adhere flexible 2.4 GHz FPC dipole antenna (Molex 146153) into the adhesive pocket on the inside of the lid ([`front_node_upper_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_upper_lid.stl)).
   * Click U.FL connector of the micro-coaxial cable squarely onto the ESP32-S3 module receptacle.
5. **Connect Pre-Molded COTS Cables (No Crimping!):**
   * **Front Opening (South Wall for USB):**
     * Connect short USB-A/C flat ribbon cable to port `J6` (CarPlay / Android Auto Dongle / Ottocast).
     * Connect 1.0 m USB-C charging cable to port `J5` (glovebox / phone mount for 20W Fast Charging).
     * Connect USB host cable to `J4` (upstream connection to OEM display / head unit).
   * **Right Opening (East Wall):** Insert elastomeric dust plug ([`front_node_usbc_cap_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_usbc_cap_tpu.stl)) into service port `J7`.
   * **Left Opening (West Wall for Power & Signals):**
     * Plug pre-crimped JST-PH 2-pin power lead for 12V switched bike supply (KL15 & Ground) into `J1`.
     * Plug JST-PH 3-pin lead for CAN-bus into `J2` (only required on fairing models with front audio CAN).
     * Plug pre-crimped JST-PH 2-pin lead from handlebar push-button into `J3` (PTT).
6. **Insert Sealing Glands & Fasten Lid:**
   * Apply a thin film of silicone grease to the elastic TPU cable gland blocks ([`front_node_cable_glands_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_cable_glands_tpu.stl)) and slide into the enclosure slots.
   * Seat silicone cord (Ø 1.5 mm, $30\,\text{cm}$) into the lid seal groove.
   * Fasten lid with 4x M3 $\times 20\,\text{mm}$ screws in a cross pattern (threading directly into the captive M3 nuts in the lower pockets).

---

## 4. Vehicle-Specific Mounting & Motorcycle Wiring

### Step 4.1: Harley-Davidson Platform Installation (Touring, CVO ST, Limited, Road King & Cruisers with Saddlebags)

```text
                       OPENMOTORBRIDGE HARLEY-DAVIDSON MOUNTING SUITE
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. COMMON SYSTEM FOUNDATION (IDENTICAL FOR TOURING & SOFTAIL CRUISER PLATFORMS)        │
│ • Central Box: Mounted under seat on frame crossmember on 4x M4 EPDM silentblocks      │
│ • Pod 1 & 2: Saddlebag lid docks (saddlebag_lid_dock.stl) on OEM hard bags or          │
│   Heritage structured cases (also Sport Glide & Low Rider ST clamshells!)              │
│ • Radar: Decoupled radar mount (radar_license_plate_bracket.stl) underneath stock      │
│   centered license plate bracket (identical on Touring, Limited, Softails, & CVO ST!)  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. COCKPIT & FRONT NODE INSTALLATION (THREE MODULAR FAIRING OPTIONS)                   │
│ • Option A (Batwing): Street Glide / Ultra / Electra Glide (2024+ vs. 2014–2023)       │
│ • Option B (Sharknose): Road Glide / CVO ST / Performance Bagger (2024+ vs. 2015–2023) │
│ • Option C (Nacelle & Cruiser): Road King (RK/RKS) & Softail Cruisers with Bags        │
│   (Heritage Classic FLHCS, Low Rider ST FXLRST, Sport Glide FLSB, Fat Boy with Bags):  │
│   -> No Fairing Headunit: Front Node mounts in headlight nacelle / mini-fairing;       │
│      CAN-bus connects directly at Central Box under seat/side cover (100% wireless!)   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 3. MODULAR TAIL POD 3 INSTALLATION (FOUR VEHICLE-SPECIFIC VARIANTS)                    │
│ • Bagger / Cruiser: Touring fender console (pod3_touring_fender_console.stl) on 1/4"  │
│ • Limited / Ultra: King Tour-Pak steel frame blocks fender! Pod 3 mounts via tube      │
│   clamp (adventure_pannier_rack_clamp_base.stl) to Tour-Pak tube rail or rack bridge   │
│ • CVO ST / Performance: Under-Cowl Skeleton Dock (cvo_st_undercowl_skeleton_dock.stl) │
│   under Forged-Carbon solo cowl with full clearance from Showa remote canisters        │
│ • Custom / Bobber: Centered under-fender plate (radar_center_underfender_mount.stl)    │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 4.1.1 Common System Foundation (All Models)
* **Central Box:** Fasten under the rider seat onto the massive frame crossmember in front of the battery using 4x M4 silentblocks (EPDM Shore 50A). On Softail Cruiser models, the Central Box sits in the cavity beneath the seat or within the side frame triangle. The HD26 harness whip branches rearward left and right to the M8 saddlebag disconnects and directly to the BCM / diagnostic plug.
* **Pod 1 & Pod 2 (Satellites):** Fasten saddlebag lid docks ([`saddlebag_lid_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/saddlebag_lid_dock.stl)) using M4 countersunk screws with backing EPDM sealing washers or 3M VHB high-bond tape onto the saddlebags. *(Note: Alongside Street Glide, Road Glide, CVO ST, Road King, and Ultra Limited, Cruisers with saddlebags like Low Rider ST and Sport Glide feature rigid clamshell bags, while the Heritage Classic has structured leather/vinyl bags with flat top lids—all share identical saddlebag lid dock [`saddlebag_lid_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/saddlebag_lid_dock.stl) mounting!)* Route the pre-molded M8 PUR cable through the bag rubber grommet and connect via quick-disconnect to the main harness.
* **Radar:** The license plate radar bracket ([`radar_license_plate_bracket.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_license_plate_bracket.stl)) bolts directly beneath the license plate frame. *(Note: All Touring, CVO ST, and Softail Cruiser models feature standardized centered US/EU license plate mounts).*

#### 4.1.2 Cockpit Fairing & Front Node Installation
* **Option A: Batwing Fairing (Street Glide / Electra Glide / Ultra):**
  * **Current Generation (2024+ All-New Street Glide with 12.3" Skyline OS):**
    1. Remove the **2x Torx T25 screws** on the windshield and lift windscreen out upward (no 3-screw system anymore!).
    2. Gently pry out the two lateral speaker grilles / trim panels forward from their snap catches using a plastic pry tool.
    3. Remove the **2x T25 screws** at the upper cowl edge beneath the windshield, and the **2x T25/T27 screws** on the outer flanks (exposed behind the speaker grilles).
    4. Pull the outer fairing forward off its locating guide pins and disconnect the central multi-pin harness connector.
  * **Previous Generation (2014–2023 Rushmore / Boom! Box GTS / 6.5GT):**
    1. Remove the **3x Torx T27 screws** securing the windshield (hold center screw last to prevent windshield from dropping).
    2. Remove the **4x Torx T27 screws** on the inner fairing: 2x below the instrument cluster, 2x low beside the speaker pods.
    3. Tilt outer fairing forward, disconnect headlight and turn signal connectors.
  * **Wiring Inside Batwing Fairing:**
    * Mount Front Node to handlebar riser or fairing subframe securely using 3M Dual-Lock or AMPS bracket.
    * **12V Power (`J1`):** Tap the 2-pin JST-PH power lead to the internal 12V P&A accessory connector or parking light circuit.
    * **CAN-Bus (`J2`):** Plug 3-pin JST-PH cable. On Rushmore (2014–2023), pin into the 4-pole P&A audio CAN socket behind the Boom! Box. On 2024+ models, connect directly to the Skyline OS display harness.
    * **External Wireless CarPlay / Android Auto Dongle (e.g., Ottocast U2Air Pro / CarlinKit 5.0):**
      * Port `J4` (USB Host Upstream): Connect to the motorcycle's OEM USB media pigtail leading to Boom! Box / Skyline OS.
      * Port `J6` (USB Downstream 2): Connect via short USB pigtail to the external wireless dongle secured inside the media compartment. In case of smartphone dropouts or frozen dongles, the OpenMotorBridge firmware triggers a 1-click watchdog hard power-cycle by cutting 5V VBUS for 2.5 seconds via the integrated TI TPS2051B power switch.
    * **Smartphone Fast-Charging (`J5`):** Route 20W USB-PD cable to the glovebox or handlebar phone cradle.
    * Reinstall outer fairing and torque screws to $3.8\,\text{Nm}$.

* **Option B: Sharknose Fairing (Road Glide, Road Glide ST, CVO Road Glide ST):**
  * **Current Generation (2024+ New Road Glide & CVO ST with 12.3" Skyline OS):**
    1. The LED turn signals are integral in the fairing outer blades—there are **no turn signal brackets** to unbolt from the fork tubes!
    2. Remove the **4x Torx T25 screws** on the windshield and lift windscreen off.
    3. Remove **1x T27 screw** inside each of the two inner glove compartments (2x T27 total).
    4. Remove **2x T25 screws** on the lower mounting tabs near the engine crash bar.
    5. Lift fairing forward and up off its catching hooks and unplug the central main harness connector.
  * **Previous Generation (2015–2023 Rushmore Road Glide / ST):**
    1. Unclip instrument gauge nacelle upward.
    2. Unbolt turn signals left and right (2x 1/2" hex bolts per side).
    3. Remove the **4x Torx T27 screws** on the inner fairing (adjacent to speakers / air ducts).
    4. Unhook Sharknose forward and disconnect harness.
  * **Wiring:** Identical to Option A (media compartment / riser mounting, `J1` 12V, `J2` CAN-bus, `J4` upstream to display, `J6` Ottocast dongle with TPS2051B watchdog reset, `J5` 20W PD cable).

* **Option C: Headlight Nacelle & Softail Cruisers with Saddlebags (Road King / RKS, Heritage Classic, Low Rider ST, Sport Glide):**
  * **Conceptual Architectural Equivalence (Cruisers with Saddlebags = Road King Architecture):**
    - All Harley-Davidson Cruisers with bags (whether Touring Road King FLHR/FLHRXS or Softail models like Heritage Classic FLHC/FLHCS, Sport Glide FLSB, and Low Rider ST FXLRST) share the exact same architecture:
      - They have **no large infotainment head unit** (Boom! Box GTS or 12.3" Skyline OS) in the cockpit.
      - They feature **saddlebags** (factory hard bags on RKS, rigid clamshells on Sport Glide and Low Rider ST, structured leather/vinyl cases on Heritage).
      - Onboard vehicle electronics and the CAN-bus (HD-LAN at 250 or 500 kbps) are readily accessible beneath the seat or behind the left side cover at the BCM (Body Control Module) and diagnostic port.
  * **CAN-Bus Architecture (Direct Tap at Central Box under Seat / Side Cover):**
    - Because no front P&A audio CAN-bus exists, the CAN-bus connects **directly to the Central Box under the seat or at the BCM/diagnostic port**.
      - *Pre-2021 Models:* 6-pin red Deutsch diagnostic socket.
      - *2021+ Models (Euro 5 / Euro 5+):* 16-pin standardized OBD2 socket.
      - The Central Box HD26 harness taps CAN directly from the BCM via pins 17 (`CAN_H`) and 18 (`CAN_L`). All telemetry (vehicle speed, engine RPM, engine temperature, turn signals, brake status, clutch switch, gear position) is broadcast.
      - **100% Wireless Link to Front:** The Front Node requires **ZERO CAN WIRING** at `J2` (port automatically deactivates). It communicates 100% wirelessly with the Central Box via 2.4 GHz ESP-NOW (< 1.8 ms). **Zero wiring needs to be routed through the steering neck or beneath the fuel tank!**
  * **Cockpit & Fairing Front Node Mounting:**
    - *Road King / Heritage Classic / Fat Boy:* Loosen pinch screw on 7" headlight trim ring, remove Daymaker. Front Node mounts vibration-isolated inside the aluminum headlight nacelle cavity behind the reflector.
    - *Low Rider ST / Sport Glide:* Fasten Front Node behind the FXRT / mini-batwing fairing or onto the triple tree clamp / handlebar riser.
    - **Front Wiring:** Port `J1` (12V KL15 & GND) connects directly to parking light or front accessory harness. Optional handlebar PTT (`J3`), blind-spot LEDs (`J9`), and smartphone Qi power (`J5`/`J10`) connect locally at the Front Node.

#### 4.1.3 Modular Rear Mounting (Pod 3)
* **Variant 1: Standard Bagger & Softail Cruisers (Street Glide, Road Glide, Road King, Heritage Classic, Low Rider ST, Sport Glide):**
  - Bolt the flat touring fender console ([`pod3_touring_fender_console.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod3_touring_fender_console.stl)) centered onto the rear fender to the stock $1/4"-20$ passenger seat nut. *(Note: Softail and Touring rear fenders utilize the exact same standardized 1/4"-20 seat thread).*
* **Variant 2: Touring Limited & Ultra (Ultra Limited FLHTK, Road Glide Limited FLTRK, CVO Limited):**
  - *Important Restriction:* On all models with a factory-installed rigid King Tour-Pak, the massive tubular steel carrier frame bolts directly over the rear fender. The fender console (`pod3_touring_fender_console.stl`) *cannot* be installed due to physical clearance and sliding cartridge access!
  - *Solution:* Pod 3 is instead bolted directly to the Ø 18 mm tubular frame of the Tour-Pak or underneath the luggage rack using the tube clamp pair ([`adventure_pannier_rack_clamp_base.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_pannier_rack_clamp_base.stl) / `cap.stl`).
* **Variant 3: CVO ST / Performance Bagger:**
  - Pod 3 is mounted concealed beneath the Forged Carbon solo seat cowl in the upright Bionic Skeleton Dock ([`cvo_st_undercowl_skeleton_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/cvo_st_undercowl_skeleton_dock.stl)) (providing full clearance from the Showa remote reservoir canisters). The aerodynamic telemetry fin ([`cvo_st_telemetry_fin.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/cvo_st_telemetry_fin.stl)) bolts to the cowl apex.
* **Variant 4: Custom Bikes & Bobbers with Side-Mounted License Plate:**
  - On custom conversions with a side-mounted plate, the centered under-fender plate ([`radar_center_underfender_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_center_underfender_mount.stl)) is bolted centered beneath the rear fender arch to ensure an unobstructed 140° radar field of view.

---

### Step 4.2: Adventure & Enduro Platform Installation (BMW GS / GSA Family, KTM, Africa Twin, Universal)

The adventure mounting suite is standardized across the entire **BMW GS model family** (Boxer and Parallel-Twin generations) and comparable dual-sport motorcycles:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        BMW GS MODEL & PLATFORM COMPATIBILITY                           │
├───────────────────────────────────┬────────────────────────────────────────────────────┤
│ Model Line                        │ Specifics & Electrical Ingress Details             │
├───────────────────────────────────┼────────────────────────────────────────────────────┤
│ • R 1250 GS / R 1300 GS           │ 6.5" TFT Connectivity, Wonder Wheel, 16-Pin OBD2,  │
│   F 750 GS / F 850 GS / F 900 GS  │ Cockpit Cartool power, Vario frame docks (Opt. A)  │
├───────────────────────────────────┼────────────────────────────────────────────────────┤
│ • R 1250 GSA / R 1300 GSA         │ 6.5" TFT Connectivity, Wonder Wheel, 16-Pin OBD2,  │
│   F 850 GSA / F 900 GSA           │ Cockpit Cartool power, Ø 18 mm stainless (Opt. B)  │
├───────────────────────────────────┼────────────────────────────────────────────────────┤
│ • R 1200 GS LC / GSA LC           │ Wonder Wheel, Cartool present. Diagnostic socket:  │
│   (K50/K51, 2013–2018)            │ 2013–2016 round 10-pin, 2017+ rectangular 16-pin   │
├───────────────────────────────────┼────────────────────────────────────────────────────┤
│ • Classic R 1200 GS / GSA (K25)   │ Analog/LCD dials, Cartool present at headstock.    │
│   & F 650 / 700 / 800 GS (K70/72) │ Round 10-pin diagnostic plug under seat.           │
│   (oil-cooled, up to 2012/2018)   │ Control via OMB BLE handlebar remote (no Wonderwh.)│
│                                   │ GSA tube racks: Identical Ø 18 mm tube diameter!   │
└───────────────────────────────────┴────────────────────────────────────────────────────┘
```

```text
                             OPENMOTORBRIDGE ADVENTURE-KIT MOUNTING SUITE
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. COMMON SYSTEM FOUNDATION (IDENTICAL FOR ALL ADVENTURE / DUAL-SPORT BIKES)           │
│ • Central Box: Mounted vibration-damped in rear subframe under rider seat              │
│ • Cockpit & Front Node: Clamped to Ø 12 mm GPS bar above TFT / windscreen              │
│   (12V Cartool power, wireless 2.4 GHz link to Central Box, zero steering head wiring) │
│ • Rear Pod 3: Fastened to luggage bridge via Rack-Tail Mount (adventure_rack_tail_mount)│
│ • Radar Varia Dock: Mounted to 36-tooth Hirth rosette in 10° increments for level horizon│
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. MODULAR POD 1 & 2 PANNIER MOUNTING (TWO MODULAR OPTIONS)                            │
│ • Option A (Vario Panniers / Frame Mount - BMW GS Standard, KTM without tube racks):   │
│   Transition Dock (adventure_transition_dock.stl) in seat crease (Ø 28 mm frame tube)  │
│   -> 100% luggage-independent, builds zero additional width beyond bike silhouette     │
│ • Option B (Stainless Pannier Tube Racks - BMW GSA, Touratech, Hepco&Becker, Alucases):│
│   Pannier rack clamp cage (adventure_pannier_rack_clamp_base.stl + cap.stl)            │
│   -> Mounts Pod 1 & 2 protected inside frame triangle (Ø 18 mm) in front of alu cases  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 4.2.1 Common System Foundation
* **Central Box:** Install in the frame triangle beneath the rider seat on 4x M4 silentblocks. Route M8 harness leads rearward left and right and toward the tail.
* **Cockpit & Front Node:**
  * Remove 4x Torx T25 windshield screws and lift windscreen off.
  * Unclip upper TFT instrument surround forward (on K25 / F800: remove instrument shroud).
  * Fasten Front Node via AMPS mount or tube clamp to the Ø 12 mm GPS crossbar or handlebar.
  * **Power Supply & CAN-Bus Options (2 Ingress Paths):**
    * **Power Supply:** Connect 2-pin JST-PH power lead at `J1` directly to the factory BMW Cartool accessory connector (SZ plug in cockpit / headstock: Pin 1 GND, Pin 3 switched +12V KL15).
    * **CAN-Bus Option 1 (Recommended – Plug & Play Under Seat):** Tapped at Central Box via HD26 harness (pins 17 `CAN_H` and 18 `CAN_L`):
      * *2017+ Models (Euro 4 / Euro 5 / Euro 5+):* Directly into 16-pin OBD2 socket or RDC/DWA module (identical to Hex ezCAN / WunderLINQ).
      * *Pre-2017 Classic Models (Euro 3, K25 / K72 / early K50):* Via standard COTS 10-pin round to OBD2 adapter cable (ICOM adapter).
      * Port `J2` on Front Node remains empty and auto-deactivates. Zero wiring tampering in the cockpit!
    * **CAN-Bus Option 2 (Cockpit Tapping at 12-Pin TFT – TFT Models Only):** The BMW 6.5" TFT display routes K-CAN directly on its rear connector (Pin 2 `CAN_H`, White/Black and Pin 3 `CAN_L`, White/Brown). Riders using a 12-pin PnP Y-cable can connect directly to `J2` on the Front Node. The Front Node streams RPM, speed, and Wonder Wheel wirelessly via ESP-NOW to Central Box.
* **Pod 3 & Radar:**
  * Bolt Pod 3 onto the Rack-Tail Mount ([`adventure_rack_tail_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_rack_tail_mount.stl)) on the factory luggage rack.
  * Engage Garmin Varia dock ([`radar_varia_gopro_lock_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_varia_gopro_lock_dock.stl)) into Hirth rosette ([`011_gopro_hirth_lock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/011_gopro_hirth_lock.stl)) ($10^\circ$ increments for an exact horizontal radar line). Secure with M5 x 25 mm screw and locknut ($3.5\,\text{Nm}$). Slide Varia into dock and tighten M3 grub screw as anti-theft lock.

#### 4.2.2 Modular Pannier & Pod 1/2 Mounting
* **Option A: Vario Panniers & Frame Tube Mount (BMW GS Standard R1200/R1250/R1300, F750/F850/F900, KTM / Enduro without racks):**
  * Clamp Transition Docks ([`adventure_transition_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_transition_dock.stl)) onto main subframe tubes (Ø 28 mm) below seat lip.
  * **100% Luggage-Independent:** The pods do not protrude beyond the motorcycle silhouette and can be ridden with Vario cases or completely without luggage.
* **Option B: Stainless Tubular Pannier Racks (BMW GSA All Generations incl. K25 & F800 GSA, Touratech, Hepco&Becker, Aluminum Cases):**
  * Wrap 1.0 mm EPDM strip around the Ø 18 mm pannier rack tube.
  * Fasten clamp base ([`adventure_pannier_rack_clamp_base.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_pannier_rack_clamp_base.stl)) and cap ([`adventure_pannier_rack_clamp_cap.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_pannier_rack_clamp_cap.stl)) using 2x M5 x 30 mm V4A screws and DIN 985 locknuts tightened in a cross pattern ($4.5\,\text{Nm}$).
  * Mount Pod base housing securely within the frame triangle ahead of the aluminum cases. All BMW Adventure aluminum rack cages (from 2006 to present day) utilize the identical standardized Ø 18 mm tube dimension.

#### 4.2.3 Front Node Bike Mounting Options (Universal)
* **Option 1: AMPS Pattern (30 x 38 mm):** Direct bolt-on to RAM-Mount ball, Garmin cradle, or GPS bar (utilizing the 4x captive M4 nuts).
* **Option 2: 120° V-Cradle:** Toolless mounting on Ø 22 to Ø 32 mm handlebars / crash bars using EPDM strap rings.
* **Option 3: M4 Silentblocks:** Vibration-isolated stud mounting inside fairing nose.
* **Option 4: 3M Dual-Lock Hook-and-Loop:** Concealed mounting inside Harley Batwing / Sharknose inner fairings or headlight nacelle.

---

### Step 4.3: Installation & Wiring of Optional Cockpit & Accessory Components

The Universal Front Node (PCBA 05) serves as the central wiring and communication hub for all cockpit peripherals. The following optional accessories can be integrated as needed via pre-molded plug-and-play wiring:

```text
              COCKPIT ACCESSORY WIRING OVERVIEW (FRONT NODE PCBA 05)
┌───────────────────────┬─────────┬────────────────────────────────────────────────────────┐
│ Accessory Component   │ Port    │ Connection & Pinout                                    │
├───────────────────────┼─────────┼────────────────────────────────────────────────────────┤
│ **Handlebar PTT**     │ **J3**  │ 4-Pin JST-PH (Pin 1: GND, Pin 2: PTT Intercom,         │
│ (Intercom & Action)   │         │ Pin 3: Action-Cam Bookmark, Pin 4: Siri/Voice Assist)  │
├───────────────────────┼─────────┼────────────────────────────────────────────────────────┤
│ **Blind Spot LEDs**   │ **J9**  │ 3-Pin JST-PH (Pin 1: +12V_PROT, Pin 2: BSD Left,       │
│ (Radar Mirror Alerts) │         │ Pin 3: BSD Right via Low-Side N-MOSFET drivers)        │
├───────────────────────┼─────────┼────────────────────────────────────────────────────────┤
│ **Actioncam Power**   │ **J8**  │ 2-Pin/4-Pin JST-PH (+5.0V / 2.0A, Charge-Only without  │
│ (GoPro/Insta360/DJI)  │         │ USB data lines to prevent head unit lockups)           │
├───────────────────────┼─────────┼────────────────────────────────────────────────────────┤
│ **Qi Wireless Mount** │ **J10** │ 2-Pin JST-PH (+12V switched ignition gate, up to 2.0A  │
│ (Quad Lock / SP Conn.)│ / **J5**│ / 24W) or 20W USB-C PD Fast Charging port J5           │
├───────────────────────┼─────────┼────────────────────────────────────────────────────────┤
│ **Auxiliary Lights**  │ **J11** │ 2-Pin JST-PH (+12V High-Side Switch up to 3.5A / 40W,  │
│ (Emergency Strobe)    │         │ automated 4–5 Hz hazard strobe on hard braking > 0.8g) │
└───────────────────────┴─────────┴────────────────────────────────────────────────────────┘
```

#### 4.3.1 Handlebar PTT (Push-To-Talk) & Multi-Button Control Cluster (`J3`)
* **Mechanical Mounting:**
  - Secure the tactile IP67 handlebar button with a slim clamp bracket (sized for Ø 22 mm / 7/8", Ø 25.4 mm / 1", or Ø 31.8 mm / 1 1/4" bars) directly adjacent to the left grip / mirror mount within ergonomic thumb reach.
  - Alternatively, a 3-button slim cluster (e.g. Daytona Slim or motogadget m-switch) can be used.
* **Electrical Connection at Port `J3` (4-Pin JST-PH):**
  - **Pin 1:** `GND` (Common ground reference)
  - **Pin 2:** `PTT_INTERCOM` (Closes to ground: triggers instant intercom mesh / radio transmit)
  - **Pin 3:** `CAM_ACTION` (Closes to ground: sets highlight bookmark in video or toggles recording)
  - **Pin 4:** `MEDIA_VOICE` (Closes to ground: triggers Siri / Google Assistant or skips audio track)
  - *(Note: Standard 2-pin momentary push buttons plug directly onto Pin 1 and Pin 2).*
* **System Benefit:** 100% battery-free, zero wireless latency (< 5 ms response time), hardware Schmitt-trigger debounced, and protected against accidental 12V shorts.

#### 4.3.2 Blind Spot Detection Mirror LED Indicators (`J9`)
* **Mechanical Mounting:**
  - Affix two compact, amber or red 12V LED indicators (sealed micro-LEDs or machined mirror clips) subtly onto the left and right mirror arms or inside the fairing mirror triangles.
  - Positioned within the rider's peripheral vision to capture overtaking traffic without blinding night vision.
* **Electrical Connection at Port `J9` (3-Pin JST-PH):**
  - **Pin 1:** `+12V_PROT` (Protected 12V anode supply)
  - **Pin 2:** `BSD_LEFT_N` (Left mirror cathode, switched via low-side N-MOSFET Ch A)
  - **Pin 3:** `BSD_RIGHT_N` (Right mirror cathode, switched via low-side N-MOSFET Ch B)
* **Operational Logic:**
  - Fed by real-time telemetry from the rear radar (Garmin Varia or OMM Radar):
    - **Solid Amber Glow:** Vehicle detected in blind spot or adjacent overtaking lane.
    - **Rapid 8 Hz Flash (Red/Amber):** Imminent collision hazard (high closing speed or turn signal activated toward overtaking vehicle).
  - *Automated Night Dimming:* Controlled via ambient light sensor (`OPT3001` on `J12`) for glare-free night operation.

#### 4.3.3 Action-Cam Power Supply (GoPro, Insta360, DJI) (`J8`)
* **Mechanical Mounting:**
  - Secure camera to handlebar, windshield bar, crash bar, or helmet tether.
* **Electrical Connection at Port `J8` (JST-PH):**
  - Clean $+5.0\,\text{V}$ dedicated power (up to $2.0\,\text{A}$) directly from Front Node.
* **Critical System Advantage (Charge-Only):**
  - Port `J8` **deliberately omits USB data lines**. This completely prevents the action camera from defaulting into "USB Mass Storage Mode" upon bike ignition, ensuring uninterrupted video recording and preventing bike head unit lockups.
  - **Automated BLE Shutter Stop:** With onboard polymer buffer capacitor `C_BUF`, the ESP32-S3 stays powered for 1.5 seconds after ignition off to send a clean Bluetooth LE "Record Stop" packet, cleanly finalizing video clips without file corruption.

#### 4.3.4 Qi Wireless Charging Cradle Integration (Quad Lock, SP Connect) (`J10` & `J5`)
* **Mechanical Mounting:**
  - Quad Lock Handlebar / Stem Mount with Weatherproof Wireless Charging Head or SP Connect Moto Mount with Wireless Charging Module.
* **Electrical Connection – Two Flexible Options:**
  - **Option 1 (Recommended: 12V Hardwire to Port `J10`):**
    - 2-Pin JST-PH: Pin 1 = `+12V_SW`, Pin 2 = `GND`.
    - Handles continuous loads up to $2.0\,\text{A}$ ($24\,\text{W}$).
    - Connects Quad Lock / SP Connect hardwire cables cleanly without flying fuses.
    - **Zero Parasitic Battery Drain:** Switched completely via Front Node internal power gate—zero drain during bike parking.
  - **Option 2 (USB-PD Fast-Charging at Port `J5`):**
    - Connect short USB-C cable from Port `J5` directly into charging head.
    - Delivers full 20W USB Power Delivery ($9\,\text{V} / 2.2\,\text{A}$, QC 4+) for maximum Qi fast charging under high sun navigation.
* **"Forgot Phone" Proximity Warning:**
  - If the ignition is turned off and the rider walks away (BLE proximity lost) while the Qi mount (`J10`) or USB port (`J5`) still senses phone load, OpenMotorBridge triggers an immediate double-beep on the horn or vibrates the LoRa smart keyfob.

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
