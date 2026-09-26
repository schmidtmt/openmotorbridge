# 16 - Build Instructions, Wiring & Vehicle Installation

This document is the complete, hands-on step-by-step assembly manual for building and installing a complete **OpenMotorBridge (v8.0 Clean Architecture)** system on any motorcycle or support vehicle.

---

## 1. System Kit Overview (What is being built?)

A complete OpenMotorBridge vehicle kit consists of the following core assemblies:

```text
                      ┌─────────────────────────────────────────┐
                      │    1x CENTRAL MAIN BOX (IP67)           │
                      │    (Under the seat / in tail section)   │
                      │    • Lower tub + mid tray + lid         │
                      │    • Host PCBA 01 (ESP32-S3 Dual-Core)  │
                      │    • Onboard SX1262 LoRa 868 MHz        │
                      │    • Qorvo DW3110 UWB Transceiver       │
                      │    • 2,200 mAh LiPo backup battery (UPS)│
                      └────────────────────┬────────────────────┘
                                           │
                         1x CENTRAL HARNESS (HD26 SEAL-D IP67)
                                           │
          ┌────────────────────────────────┼────────────────────────────────┐
          │                                │                                │
          ▼ Whip 1                         ▼ Whip 2                         ▼ Whip 5
┌──────────────────┐             ┌──────────────────┐             ┌──────────────────┐
│ 1x POD 1 (LEFT)  │             │ 1x POD 2 (RIGHT) │             │ 1x REAR RADAR    │
│ (Frame / Pannier)│             │ (Frame / Pannier)│             │ (Optional)       │
│ • Pod enclosure  │             │ • Pod enclosure  │             │ • Wheeltec MR20  │
│ • Base PCBA 02   │             │ • Base PCBA 02   │             │   or Garmin      │
│ • CARTRIDGE 1    │             │ • CARTRIDGE 2    │             │   Varia RTL515   │
│   (Sena SPIDER   │             │   (Cardo Edge    │             └──────────────────┘
│    X Slim)       │             │    / Swap OMM)   │
└──────────────────┘             └──────────────────┘
                                           ▲
                                           │ Deterministic UWB Vehicle Backbone
                                           │ (Qorvo DW3110 / 6.5 GHz Ch. 5, < 0.4 ms)
                                           ▼
                                 ┌──────────────────────────────────┐
                                 │ 1x UNIVERSAL FRONT NODE (IP67)   │
                                 │ (Cockpit & Sensor Hub, PCBA 05)  │
                                 │ • u-blox SAM-M10Q Multi-GNSS     │
                                 │ • TI TMP117 & OPT3001 Sensors    │
                                 │ • Knowles MEMS Wind Noise Sensor │
                                 │ • 4-Port USB Hub & Dual USB-PD   │
                                 │ • Battery-Free Handlebar PTT     │
                                 └──────────────────────────────────┘
```

---

## 2. Pre-Assembly Checklist (Parts & Hardware Verification)

All discrete components, PCB ordering files, and COTS sourcing lists are documented in **[Chapter 15: Bill of Materials & Manufacturing](15_bom_manufacturing.md)**. Ensure the following items are ready before assembly begins:

* [ ] **3D Printed Parts (MJF PA12 Black or FDM ASA/PET-CF):**
  * 1x Main Box (lower tub with UWB bottom pocket $11 \times 11 \times 0.6\,\text{mm}$, mid tray with LiPo cradle, lid with LoRa FXP895 pocket $110 \times 20 \times 0.8\,\text{mm}$)
  * 2x Pod base enclosures & 2x pod bulkheads (100% symmetric for Pod 1 and Pod 2)
  * 2x Cartridge base sleds, inlays (Sena SPIDER X Slim, Cardo Packtalk Edge, Swap OMM, or blank cartridge) & 2x magnetic latches
  * 1x Front Node (lower tub with UWB bottom pocket and AMPS nut pockets, upper lid, TPU cable glands & USB-C cap)
  * 1x Vehicle-specific mounting kit (BMW GS clamps & `adventure_rack_radar_mount.stl` / Harley saddlebag docks & license plate bracket / Support-Car `car_sun_visor_pod_clip.stl`)
* [ ] **Fully Populated PCBAs (from JLCPCB / Eurocircuits):**
  * 1x PCBA 01 (Central Box with onboard LoRa SX1262 and DW3110 UWB)
  * 2x PCBA 02 (Pod Base, symmetric for Pod 1 and Pod 2)
  * 2x PCBA 03 (Smart Modular Cartridge with CH32V003 and 4x AO3400 N-MOSFETs)
  * 1x PCBA 05 (Front Node with DW3110 UWB)
  * *(Optional: 1x PCBA 08 Radar 2.0 Sub-MCU, PCBA 06 MagSafe Dock, PCBA 07 Smart-Keyfob)*
* [ ] **A4 / 316 Stainless Fasteners & Springs (IKEA Principle – 100% Solder-Free):**
  * 8x DIN 934 / DIN 985 M3 stainless nuts (for captive enclosure nut pockets)
  * 4x DIN 934 M4 nuts (for AMPS nut pockets in Front Node tub)
  * 4x M3 x 40 mm socket head screws (Central Box), 4x M3 x 20 mm screws (Front Node)
  * 8x M2.5 x 6 mm board screws, 4x M2 x 8 mm countersunk screws (bulkheads), 8x M2 x 6 mm (cartridges)
  * 2x DIN 7 M2 x 8 mm dowel pins (latch pivots), 2x DIN 6325 Ø 6 x 8 mm hardened steel keeper pins
  * 2x Latch return springs, 4x auto-eject compression springs, 1x N52 neodymium release key
* [ ] **Gaskets, Battery & Antennas:**
  * Silicone O-ring cord Ø 1.5 mm Shore 40A ($40\,\text{cm}$ Main Box, $30\,\text{cm}$ Front Node)
  * 2x Molded silicone face gaskets for Pod 1 & 2 mouths, Gore ePTFE vent stickers
  * **1x 1S LiPo Flat Pack 2,200 mAh** ($68 \times 39 \times 5.0\,\text{mm}$) with Molex Micro-Fit 3.0 connector
  * **2x Taoglas FXUWB10 UWB Flex Antennas** with 20 mm U.FL leads
  * **1x Taoglas FXP895 LoRa 868 MHz Flex Antenna** with 50 $\Omega$ U.FL lead
  * **1x u-blox SAM-M10Q Multi-GNSS Module** with integrated patch antenna (Qwiic I2C)
  * **1x TI TMP117 & 1x TI OPT3001 Sensors** (Qwiic I2C)
* [ ] **Pre-Assembled COTS Harnesses (Zero Crimping Required):**
  * 1x HD26 SEAL-D IP67 4-branch breakout harness (Pod 1, Pod 2, 12V Battery, Whip 5 Rear Radar)
  * 2x M8 6-Pin PUR cables (1.0 m / 1.5 m)
  * 1x M8 4-Pin PUR cable (Whip 5 for radar)
  * JST-SH cartridge wiring harnesses (8-Pin `J_ACT` for solenoids, 6-Pin `J2` for audio/DC)
* [ ] **Tools:**
  * Hex key set (1.5 / 2.0 / 2.5 / 3.0 mm), Torx TX10 / PH1 driver, open-end wrenches 7 / 8 / 10 mm, utility knife, dielectric silicone grease

---

## 3. Step-by-Step Module Assembly

### Step 1: Central Box Assembly
1. **Insert Captive Nuts:** Press 4x DIN 934 / DIN 985 M3 stainless nuts into the captive hexagonal pockets from underneath the lower tub ([`main_box_lower_case.stl`](../../hardware/cad/stl/01_main_box/main_box_lower_case.stl)).
2. **Install Tub Floor UWB Antenna:**
   * Affix the flexible UWB antenna (Taoglas FXUWB10, $11 \times 11 \times 0.6\,\text{mm}$) into the bottom recess of the lower tub using its adhesive backing.
   * Route the short 20 mm U.FL micro-coax cable vertically upward.
3. **Mount Host PCB:**
   * Place fully assembled PCBA 01 onto the vibration-damping bosses.
   * Snap the U.FL connector onto receptacle `ANT2` located on the bottom copper layer (`B.Cu`).
   * Fasten the board with 4x M2.5 $\times 6\,\text{mm}$ screws finger-tight.
4. **Install Lid LoRa Antenna:**
   * Adhere the flexible LoRa antenna (Taoglas FXP895, $110 \times 20 \times 0.8\,\text{mm}$) into the lid pocket of [`main_box_lid.stl`](../../hardware/cad/stl/01_main_box/main_box_lid.stl).
   * Connect the U.FL lead to header `ANT1` on the top surface of PCBA 01.
5. **Mid Tray & 2,200 mAh LiPo Battery:** Seat the mid tray ([`main_box_mid_tray.stl`](../../hardware/cad/stl/01_main_box/main_box_mid_tray.stl)). Place the **2,200 mAh flat LiPo battery** into the tray, connect the Micro-Fit plug to `J_BAT`, and secure the cell with EPDM foam tape.
6. **Seal & Temporary Cover:** Lightly lubricate the silicone O-ring cord (Ø 1.5 mm, $40\,\text{cm}$) and seat it into the lid groove. Stick the Gore vent membrane onto the vent boss. Place the lid loosely on top.

---

### Step 2: Assemble Satellite Pods 1 & 2 (2x Identical Units)
1. **Insert Base PCB:** Slide fully assembled PCBA 02 into the guide tracks of the pod base housing ([`pod_base_housing.stl`](../../hardware/cad/stl/02_pod_base/pod_base_housing.stl)). Push the M8 6-pin IP67 socket through the rear bore, slip on the O-ring, and tighten the M8 jam nut ($1.2\,\text{Nm}$) using a 10 mm wrench.
2. **Install Auto-Eject Springs:** Insert a stainless compression spring ($\varnothing 4.5 \times 15\,\text{mm}$) into each of the two rear spring cavities of the bulkhead partition ([`03_pod_bulkhead_partition.stl`](../../hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl)).
3. **Secure Bulkhead:** Slide the bulkhead partition into the pod enclosure until seated against the internal stop shoulder. Fasten with 2x M2 $\times 8\,\text{mm}$ countersunk screws through the outer shell.
4. **Inspection:** The 6-pin socket header `J1` aligns flush inside the bulkhead protective collar. Repeat for Pod 2.

---

### Step 3: Multi-Protocol Gateway Cartridges 1 & 2 Assembly
1. **Mount PCB:** Snap PCBA 03 Rev 2.0 into the cartridge base sled ([`cartridge_base_sled.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl)).
2. **Install Gateway Inlay & Solenoids:**
   * **Slot 1 (Sena SPIDER X Slim Inlay):**
     * Insert 4x miniature solenoids ($\varnothing 6.5 \times 12\,\text{mm}$) with TPU tips into the actuator bridge of [`cartridge_insert_sena.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl).
     * Fasten retainer plate with 4x M2 $\times 6\,\text{mm}$ countersunk screws.
     * Connect pre-crimped 8-pin harness `J_ACT` to header `J_ACT` on PCBA 03.
     * Seat Sena SPIDER X Slim; connect direct micro-cable whip to `J2` on PCBA 03 (zero pogo pins!).
   * **Slot 2 (Cardo Packtalk Edge Inlay / Swap OMM):**
     * Mount 4x solenoids into [`cartridge_insert_cardo.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl) and connect to `J_ACT`.
     * Lock Cardo Packtalk Edge into Air-Mount cradle and attach micro-cable whip to `J2`.
3. **Mouth Gasket:** Slide molded silicone gasket over the cartridge collar and lightly apply silicone grease.

---

### Step 3.1: Assemble Magnetic Anti-Theft Latch (Lever Mechanism)
1. **Press Steel Pin:** Press the hardened steel keeper pin ($\varnothing 6 \times 8\,\text{mm}$, DIN 6325) into the transverse hole of the latch lever ([`cartridge_magnetic_lock_latch.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_magnetic_lock_latch.stl)).
2. **Insert Spring:** Place the small $\varnothing 3.5 \times 10\,\text{mm}$ compression spring into the inward pocket.
3. **Pivot Mounting:** Slide the assembled latch into the left cheek of the cartridge sled and drive the $\varnothing 2.0 \times 8\,\text{mm}$ stainless dowel pin (DIN 7) through the pivot hole.
4. **Functional Test:** Latch tooth extends $2.5\,\text{mm}$ outward; holding the N52 neodymium block magnet outside the housing retracts the tooth flush into the sled.

---

### Step 4: Universal Front Node (PCBA 05) Assembly
1. **Insert Captive Nuts:** Press 4x M3 nuts into corner pockets and 4x M4 nuts into AMPS base pockets of [`front_node_lower_tub.stl`](../../hardware/cad/stl/04_front_node/front_node_lower_tub.stl).
2. **Install Tub Floor UWB Antenna:**
   * Adhere Taoglas FXUWB10 flex antenna into the lower tub floor recess.
   * Route U.FL lead upward.
3. **Mount Host PCB:**
   * Place PCBA 05 onto damping bosses.
   * Snap UWB coax lead onto U.FL receptacle on `B.Cu`.
   * Secure board with 4x M2.5 screws.
4. **Connect Cockpit Sensors (J12 Qwiic):**
   * Connect u-blox SAM-M10Q Multi-GNSS module (with integrated $15 \times 15\,\text{mm}$ patch antenna) via Qwiic cable to `J12`.
   * Daisy-chain TI TMP117 temperature sensor and TI OPT3001 light sensor along the Qwiic bus inside the cool ram-air intake zone.
5. **Acoustic Membrane:** Stick hydrophobic Gore ePTFE membrane over the acoustic port of the digital MEMS microphone (`MIC1`).
6. **Connect Wiring & Enclosure Closure:**
   * Plug 12V KL15 & GND to `J1`, CAN-bus to `J2`, handlebar PTT to `J3`, CP2AA dongle to `J6`, fast-charging to `J5`.
   * Insert TPU sealing combs, place silicone cord in lid groove, and seat lid loosely.

---

## 4. Benchtop Dry-Run & Testing BEFORE Bike Installation

The entire system can be fully powered, flashed, and tested on a workbench using standard USB-C cables and a multi-port 5V USB charger:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│       OPENMOTORBRIDGE BENCHTOP DRY-RUN (LABORATORY WORKBENCH SETUP)         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [ 230V USB Charger / Power Bank / Laptop (5V / ≥ 2.4A) ]                  │
│       │                      │                      │                       │
│  USB-C│Cable 1          USB-C│Cable 2          USB-C│Cable 3                │
│       ▼                      ▼                      ▼                       │
│  ┌───────────────┐     ┌───────────────┐      ┌───────────────┐             │
│  │  CENTRAL BOX  │     │  FRONT NODE   │      │ SATELLITE POD │             │
│  │   (PCBA 01)   │     │   (PCBA 05)   │      │ (Pod 1 / 2)   │             │
│  │  Port J7 USB-C│     │  Port J5 USB-C│      │ M8 Adapter    │             │
│  └───────┬───────┘     └───────┬───────┘      └───────┬───────┘             │
│          │                     │                      │                     │
│          │   UWB Wireless Link │                      │ 1-Wire & Direct-DC  │
│          │◄───────────────────►│                      ▼                     │
│          │  (6.5 GHz, <0.4 ms) │             ┌───────────────────┐          │
│          │                     │             │ SMART CARTRIDGE   │          │
│          │                     │             │ (Sena / Cardo)    │          │
│          │                     │             └────────┬──────────┘          │
│          │ WebBLE / WebSerial  │                      │                     │
│          ▼                     ▼                      ▼                     │
│    [ SMARTPHONE / LAPTOP WITH PWA ]            [ RIDER HELMET ]             │
│    (Chrome / Edge: Flasher & Dashboard)        (Bluetooth Paired)           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.1 Guided 4-Point IKEA Smoke Test
In the PWA (via WebSerial or WebBLE), verify diagnostics:
1. [x] **Power & UPS (Check 1):** LM5164 buck active (5.04 V), UPS LiPo (2,200 mAh) charging to 4.18 V.
2. [x] **Cartridges & Solenoids (Check 2):** 1-Wire detection of Slot 1 (Sena) and Slot 2 (Cardo), automated 4-solenoid click test ("Click-Click-Click-Click").
3. [x] **Front Node & UWB Backbone (Check 3):** UWB link active ($< 0.4\,\text{ms}$ latency), SAM-M10Q 3D fix, TMP117 temperature, Knowles MEMS level & handlebar PTT keying.
4. [x] **LoRa 868 MHz & Radar (Check 4):** SX1262 LoRa ping-echo and UART telemetry to rear radar on Whip 5.

Once all 4 checks indicate green, tighten enclosure lids with M3 screws diagonally.

---

## 5. Vehicle-Specific Mounting & Wiring on Motorcycle

### 5.1 Harley-Davidson Platform (Touring, CVO ST, Road King)
* **Central Box:** Fasten under rider seat on frame crossmember forward of battery using 4x M4 vibration isolators.
* **Pod 1 & Pod 2:** Mount to hard saddlebag lids using [`saddlebag_lid_dock.stl`](../../hardware/cad/stl/02_pod_base/saddlebag_lid_dock.stl).
* **Rear Radar:** Mount via license plate radar bracket ([`radar_license_plate_bracket.stl`](../../hardware/cad/stl/02_pod_base/radar_license_plate_bracket.stl)) connected to Whip 5 of the HD26 harness.
* **Front Node:** Secure inside fairing (Batwing / Sharknose) or nacelle; 12V from auxiliary plug; CAN connected locally at J2 (or under seat at Central Box).

### 5.2 Adventure Platform (BMW GS / GSA Family)
* **Central Box:** Mount inside frame triangle under rider seat on 4x M4 vibration isolators.
* **Cockpit & Front Node:** Mount to Ø 12 mm GPS bar above TFT display; 12V via factory BMW Cartool plug.
* **Pod 1 & Pod 2:**
  * *Option A (Vario Panniers / GS Standard):* Transition docks ([`adventure_transition_dock_base.stl`](../../hardware/cad/stl/02_pod_base/adventure_transition_dock_base.stl)) in seat frame crease (Ø 28 mm tube) coupled with underseat cross-rail ([`adventure_underseat_cross_rail.stl`](../../hardware/cad/stl/02_pod_base/adventure_underseat_cross_rail.stl)).
  * *Option B (Stainless Pannier Racks / GSA):* Heavy-duty GSA cage docks ([`adventure_gsa_cage_dock_body.stl`](../../hardware/cad/stl/02_pod_base/adventure_gsa_cage_dock_body.stl)) in 45 mm frame dead space.
* **Rear Radar:** Minimalist bracket ([`adventure_rack_radar_mount.stl`](../../hardware/cad/stl/02_pod_base/adventure_rack_radar_mount.stl)) directly under GS luggage rack for Garmin Varia or Wheeltec MR20 on Whip 5.

### 5.3 Support Car / Chase Van Installation (Car-Kit)
* **Pod 1 & Pod 2:** Attached to driver and passenger sun visors using quick-release clips ([`car_sun_visor_pod_clip.stl`](../../hardware/cad/stl/05_accessories/car_sun_visor_pod_clip.stl)).
  * Mode A (Chase vehicle for bike group): Pod 1 = Sena SPIDER X Slim, Pod 2 = Cardo Packtalk Edge.
  * Mode B (Pure car convoy): Pod 1 = OMM 2.4 GHz Swap Cartridge, Pod 2 = Midland PMR446 radio cartridge.
* **Central Box:** Sits in 15° dashboard wedge dock on center console.
* **SAM-M10Q GNSS:** Positioned on dashboard behind windshield.
* **Audio Integration:** USB-C audio link to vehicle headunit for group intercom through vehicle speakers.
* **Telemetry:** Wireless BLE OBD2 dongle plugged into driver footwell.

---

## 6. Final Sign-Off & Road Test Checklist

1. **Ignition ON (KL15):**
   * Central Box and Front Node wake synchronously in $< 800\,\text{ms}$.
   * UWB wireless backbone locks immediately (green sync LED).
   * Mirror blind-spot LEDs (`J9`) acknowledge with 1.0 s amber flash.
2. **Cartridge Keying:**
   * Press handlebar controls: Solenoids actuate headset buttons reliably.
3. **Blind-Spot Radar Test:**
   * Approaching vehicle from rear triggers amber mirror LEDs; signaling for lane change triggers 8 Hz red/amber hazard flash.
4. **Road Dynamics:**
   * Knowles MEMS wind sensor smoothly scales helmet volume.
   * Raised-Cosine Ducking attenuates music by $-18\,\text{dB}$ during incoming radio transmissions.
5. **Ignition OFF:**
   * Action cameras stop recording automatically via Bluetooth LE shutter.
   * Central Box executes graceful shutdown; LoRa 868 MHz theft sentry remains active 24/7 on UPS rail.
