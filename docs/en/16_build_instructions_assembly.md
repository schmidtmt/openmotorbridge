# 16 - Build Instructions, Wiring & Vehicle Installation

This document is the complete, hands-on step-by-step assembly manual for building and installing a complete **OpenMotorBridge (v8.0 Clean Architecture)** system on any motorcycle or support vehicle.

---

## 1. System Kit Overview (What is being built?)

A complete OpenMotorBridge vehicle kit consists of the following core assemblies:

```text
                      +-----------------------------------------+
                      |    1x CENTRAL MAIN BOX (IP67)           |
                      |    (Under the seat / in tail section)   |
                      |    * Lower tub + mid tray + lid         |
                      |    * Host PCBA 01 (ESP32-S3 Dual-Core)  |
                      |    * Onboard SX1262 LoRa 868 MHz        |
                      |    * Qorvo DW3110 UWB Transceiver       |
                      |    * 2,200 mAh LiPo backup battery (UPS)|
                      +--------------------+--------------------+
                                           |
                         1x CENTRAL HARNESS (HD26 SEAL-D IP67)
                                           |
          +--------------------------------+--------------------------------+
          |                                |                                |
          v Whip 1                         v Whip 2                         v Whip 5
+------------------+             +------------------+             +------------------+
| 1x POD 1 (LEFT)  |             | 1x POD 2 (RIGHT) |             | 1x REAR RADAR    |
| (Frame / Pannier)|             | (Frame / Pannier)|             | (Optional)       |
| * Pod enclosure  |             | * Pod enclosure  |             | * Wheeltec MR20  |
| * Base PCBA 02   |             | * Base PCBA 02   |             |   or Garmin      |
| * CARTRIDGE 1    |             | * CARTRIDGE 2    |             |   Varia RTL515   |
|   (Sena SPIDER   |             |   (Cardo Edge    |             +------------------+
|    X Slim)       |             |    / Swap OMM)   |
+------------------+             +------------------+
                                           ^
                                           | Deterministic UWB Vehicle Backbone
                                           | (Qorvo DW3110 / 6.5 GHz Ch. 5, < 0.4 ms)
                                           v
                                 +----------------------------------+
                                 | 1x UNIVERSAL FRONT NODE (IP67)   |
                                 | (Cockpit & Sensor Hub, PCBA 05)  |
                                 | * u-blox SAM-M10Q Multi-GNSS     |
                                 | * TI TMP117 & OPT3001 Sensors    |
                                 | * Knowles MEMS Wind Noise Sensor |
                                 | * 4-Port USB Hub & Dual USB-PD   |
                                 | * Battery-Free Handlebar PTT     |
                                 +----------------------------------+
```

---

## 2. Pre-Assembly Checklist (Parts & Hardware Verification)

All discrete components, PCB ordering files, and COTS sourcing lists are documented in **[Chapter 15: Bill of Materials & Manufacturing](15_bom_manufacturing.md)**. Ensure the following items are ready before assembly begins:

* [ ] **3D Printed Parts (MJF PA12 Black or FDM ASA/PET-CF):**
  * 1x Main Box (lower tub with UWB bottom pocket $11 \times 11 \times 0.6\,\text{mm}$, mid tray with LiPo cradle, lid with LoRa FXP895 pocket $110 \times 20 \times 0.8\,\text{mm}$)
  * 2x Pod base enclosures (seamless 1-piece monocoques with integral monolithic bulkhead, Mill-Max contact sleeves & spring guide posts; 0 assembly screws, 0 loose parts)
  * 2x Cartridge base sleds (with UWB antenna floor pocket & DIN 934 M2 captive nut standoffs), inlays (Sena SPIDER X Slim, Cardo Packtalk Edge, Swap OMM, or blank cartridge) & 2x magnetic latches
  * 1x Front Node (lower tub with UWB bottom pocket and AMPS nut pockets, upper lid, TPU cable glands & USB-C cap)
  * 1x Vehicle-specific mounting kit (BMW GS clamps & `adventure_rack_radar_mount.stl` / Harley saddlebag docks & license plate bracket / Support-Car `car_sun_visor_pod_clip.stl`)
  * *(Optional for helmet operation / OMM):* 1-2x OMM UCS upper shells ([`omm_ucs_top_shell.stl`](../../hardware/cad/stl/03_pod_cartridges/omm_ucs_top_shell.stl)), lower shells ([`omm_ucs_bottom_shell.stl`](../../hardware/cad/stl/03_pod_cartridges/omm_ucs_bottom_shell.stl)) & silicone keypads ([`omm_ucs_silicone_keypad.stl`](../../hardware/cad/stl/03_pod_cartridges/omm_ucs_silicone_keypad.stl))
* [ ] **Fully Populated PCBAs (from JLCPCB / Eurocircuits - up to 8 PCBAs):**
  * 1x PCBA 01 (Central Box with onboard LoRa SX1262 and DW3110 UWB)
  * 2x PCBA 03 (Universal Smart Cartridge Rev 3.0 All-UWB with DW3110 UWB, ES8388 / MCU and 4x AO3400 N-MOSFETs, 2-sided SMT)
  * 1x PCBA 05 (Front Node with DW3110 UWB)
  * *(Optional: 1x PCBA 08 Radar 2.0 Sub-MCU, PCBA 06 MagSafe Dock, PCBA 07 Smart-Keyfob)*
  * *(Optional for Helmet / OpenMotorMesh):* 1x **PCBA 09 (OMM 2.4 GHz HD-Mesh)** and/or 1x **PCBA 10 (OMM 446 PMR/DMR Radio)**
  * *(Note: PCBA 02 and PCBA 04 are completely eliminated).*
* [ ] **A4 / 316 Stainless Fasteners & Springs (IKEA Principle - 100% Solder-Free):**
  * 8x DIN 934 / DIN 985 M3 stainless nuts (for captive enclosure nut pockets)
  * 6x DIN 934 M4 nuts (4x AMPS nut pockets in Front Node tub, 2x Radar 2.0 rear housing)
  * 4x M3 x 40 mm socket head screws (Central Box), 4x M3 x 20 mm screws (Front Node)
  * 8x M2.5 x 6 mm board screws (Central Box & Front Node), 8x M2 x 6 mm board screws (Cartridge PCBA 03; bulkhead screws completely eliminated)
  * 4-8x DIN 934 M2 nuts & 4-8x DIN 912 M2 x 8 mm socket head screws (for OMM UCS enclosure fastening)
  * 2x DIN 7 M2 x 8 mm dowel pins (latch pivots), 2x DIN 6325 Ø 6 x 8 mm hardened steel keeper pins
  * 2x Latch return springs, 4x auto-eject compression springs, 1x N52 neodymium release key
  * 4x Gold-plated Mill-Max heavy-duty spring contact sleeves for Pod 1 & 2 power feed
* [ ] **Gaskets, Battery & Antennas:**
  * Silicone O-ring cord Ø 1.5 mm Shore 40A ($40\,\text{cm}$ Main Box, $30\,\text{cm}$ Front Node)
  * Silicone O-ring cord Ø 0.8 mm Shore 40A ($25\,\text{cm}$ per OMM UCS module)
  * 2x Molded silicone face gaskets for Pod 1 & 2 mouths, Gore ePTFE vent stickers
  * **1x 1S LiPo Flat Pack 2,200 mAh** ($68 \times 39 \times 5.0\,\text{mm}$) with Molex Micro-Fit 3.0 connector (Central Box UPS)
  * **1-2x 1S LiPo Pouch Battery 600 mAh** ($38 \times 24 \times 4.5\,\text{mm}$) with JST 2-Pin connector (OMM UCS modules)
  * **Taoglas FXUWB10 UWB Flex Antennas** with 20 mm U.FL leads (Central Box, Front Node, Cartridges)
  * **1x Taoglas FXP895 LoRa 868 MHz Flex Antenna** with 50 $\Omega$ U.FL lead
  * **1x u-blox SAM-M10Q Multi-GNSS Module** with integrated patch antenna (Qwiic I2C)
  * **1x TI TMP117 & 1x TI OPT3001 Sensors** (Qwiic I2C)
  * **1-2x RF Micro-Coaxial Pigtails U.FL to SMA-Bulkhead** (RG-178 / 1.13mm, 50 mm) with IP67 EPDM O-ring and M6 stainless nut
  * **1x OMM 2.4 GHz Stubby Antenna** (SMA-Male, 38 mm Rubber-Duck helix)
  * **1x OMM 446 MHz Stubby Antenna** (SMA-Male, 48 mm Helical stubby)
* [ ] **Pre-Assembled COTS Harnesses (Zero Crimping Required):**
  * 1x Deutsch DTM-12 IP67/IP69K central breakout harness (pure 2-wire DC whips for Pod 1, Pod 2, Radar and 12V battery & CAN)
  * 2-Pin JWPF / Superseal connectors for Pod and Radar power leads
  * JST-SH cartridge wiring harnesses (8-Pin `J_ACT` for solenoids)
  * 1-2x OMM Helmet Audio & PTT Harnesses (6-Pin JST-SH 1.0mm socket to 3.5mm jack + mic + PTT, AWG30/32 silicone, $12\dots 15\,\text{cm}$)
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

### Step 2: Assemble Satellite Pods 1 & 2 (2x Identical 1-Piece Screwless Monocoques)
1. **Route 2-Wire DC Feed:** Feed the 2-wire DC harness (+12V/5V and GND) through the rear cable gland or M8 port of the monolithic pod base housing ([`pod_base_housing.stl`](../../hardware/cad/stl/02_pod_base/pod_base_housing.stl)).
2. **Install Mill-Max Spring Contacts:** Press the two gold-plated Mill-Max heavy-duty spring contact sleeves from behind into the two guide bores of the integral monolithic bulkhead wall and connect/crimp with the supply wires.
3. **Mount Auto-Eject Springs:** From the front opening, slide the two stainless compression springs ($\varnothing 4.5 \times 15\,\text{mm}$) directly onto the two integrated guide posts of the monolithic bulkhead partition.
4. **Screwless Completion:** Because the transverse bulkhead is 100% integrally molded into the 1-piece monocoque, all assembly and countersunk screws are eliminated (0 screws). The two gold-plated spring pins extend with spring compliance into the cartridge bay. Repeat for Pod 2.

---

### Step 3: Multi-Protocol Gateway Cartridges 1 & 2 Assembly
1. **Mount UWB Antenna & PCB in Sled:**
   * Place the flexible UWB antenna (Taoglas FXUWB10, $12 \times 12 \times 0.8\,\text{mm}$) into the bottom pocket of the cartridge sled ([`cartridge_base_sled.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl)) and route the U.FL micro-coax cable in the recess channel.
   * Place PCBA 03 Rev 3.0 onto the four M2 standoffs, snap the U.FL connector onto `ANT_UWB` (`B.Cu`), and secure the board finger-tight with 4x M2 $\times 6\,\text{mm}$ screws. Gold contact pads `PAD1` (+12V/5V) and `PAD2` (GND) on the bottom copper face remain directly accessible through the rear floor cutout for mating with the pod Mill-Max pins.
2. **Install Gateway Inlay & Solenoids:**
   * **Slot 1 (Sena SPIDER X Slim Inlay):**
     * Insert 4x miniature solenoids ($\varnothing 6.5 \times 12\,\text{mm}$) with TPU tips into the actuator bridge of [`cartridge_insert_sena.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl).
     * Fasten retainer plate with 4x M2 $\times 6\,\text{mm}$ countersunk screws.
     * Connect pre-crimped 8-pin harness `J_ACT` to header `J_ACT` on PCBA 03.
     * Seat Sena SPIDER X Slim; connect direct micro-cable whip to `J_AUDIO_PWR` on PCBA 03 (zero pogo pins!).
   * **Alternative Option: Universal OEM Upcycling Cartridge (Schuberth SC2, Shoei SRL Series, HJC Smart 50B - €0 Budget Option):**
     * *Preparation (Battery Eliminator):* Open the retired OEM intercom shell (SC2, Shoei SRL, or Smart HJC), desolder the LiPo pouch cell. Configure a miniature buck converter (e.g. MP2315) from `VCC` (5V from `J_AUDIO_PWR` Pin 2) to $3.75\dots 3.85\,\text{V}$ and solder to `BAT+` / `BAT-`. Solder a $10\,\text{k}\Omega$ resistor between NTC pad and `GND` (simulating 22°C cell temperature against boot error). Pot and strain-relieve wires with silicone or B-7000.
     * *Audio & Antenna Adaptation:* Connect 8-pin JST-SH harness to OEM speaker and microphone wires (keeping `AGND` grounds isolated!). Adapt internal U.FL/micro-coax leads via short RG-178 pigtail to the front SMA bulkhead port of the cartridge.
     * *Mounting in Base Sled:* Place main electronics module ($75 \times 40 \times 12\,\text{mm}$ or flat neck module) and step-down converter inside the base sled. Control wirelessly via BLE handlebar remote (SC2 Remote or Sena RC4) or mechatronic bridge. Fasten solid blind cover (`03_insert_blindkassette.scad`) with 4x M2 screws for a weatherproof seal.
   * **Slot 2 (Cardo Packtalk Edge Inlay / Swap OMM):**
     * Mount 4x solenoids into [`cartridge_insert_cardo.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl) and connect to `J_ACT`.
     * Lock Cardo Packtalk Edge into Air-Mount cradle and attach micro-cable whip to `J_AUDIO_PWR`.
3. **Mouth Gasket:** Slide molded silicone gasket over the cartridge collar and lightly apply silicone grease.

---

### Step 3.1: Assemble Magnetic Anti-Theft Latch (Lever Mechanism)
1. **Press Steel Pin:** Press the hardened steel keeper pin ($\varnothing 6 \times 8\,\text{mm}$, DIN 6325) into the transverse hole of the latch lever ([`cartridge_magnetic_lock_latch.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_magnetic_lock_latch.stl)).
2. **Insert Spring:** Place the small $\varnothing 3.5 \times 10\,\text{mm}$ compression spring into the inward pocket.
3. **Pivot Mounting:** Slide the assembled latch into the left cheek of the cartridge sled and drive the $\varnothing 2.0 \times 8\,\text{mm}$ stainless dowel pin (DIN 7) through the pivot hole.
4. **Functional Test:** Latch tooth extends $2.5\,\text{mm}$ outward; holding the N52 neodymium block magnet outside the housing retracts the tooth flush into the sled.

---

### Step 3.2: Assemble OMM UCS Intercom Modules (PCBA 09 & PCBA 10) & Prepare for Helmet Installation

Both standalone modules (**PCBA 09: OMM 2.4 GHz HD-Mesh** and **PCBA 10: OMM 446 PMR/DMR**) share an identical ECE 22.06 UCS enclosure ($68 \times 36 \times 9.5\,\text{mm}$) and assemble as follows:

1. **Insert Captive Nuts & Keypad Gasket:**
   * Press 4x DIN 934 M2 stainless nuts from inside into the captive nut pockets of the upper shell ([`omm_ucs_top_shell.stl`](../../hardware/cad/stl/03_pod_cartridges/omm_ucs_top_shell.stl)).
   * Seat the Shore 50A silicone keypad ([`omm_ucs_silicone_keypad.stl`](../../hardware/cad/stl/03_pod_cartridges/omm_ucs_silicone_keypad.stl)) into the upper shell recess (key plungers protrude through the 4 aperture holes, diffuse LED dome aligns with `D1`).
   * Lightly lubricate silicone O-ring cord ($\varnothing 0.8\,\text{mm}$, approx. $22\,\text{cm}$) with silicone grease and press it into the perimeter sealing channel of the upper shell.
2. **Install RF Coax Pigtail & Watertight SMA Bulkhead:**
   * Connect the 50 mm low-loss micro-coax pigtail (U.FL to SMA bulkhead) to the board:
     * On `PCBA 09`: Snap U.FL connector vertically onto the integrated U.FL receptacle on the `ESP32-C6-MINI-1U` (`U1`).
     * On `PCBA 10`: Snap U.FL connector onto receptacle `J_RF` on the bottom copper side (`B.Cu`).
   * Slide the EPDM/Silicone O-ring ($\varnothing 6.0 \times 1.0\,\text{mm}$) over the SMA bulkhead threads.
   * Seat the SMA jack with its D-cut anti-twist flat into the $5.0 \times 4.0\,\text{mm}$ slot on the $+X$ flank of the lower shell ([`omm_ucs_bottom_shell.stl`](../../hardware/cad/stl/03_pod_cartridges/omm_ucs_bottom_shell.stl)) and tighten the A4 stainless hex nut and star lockwasher from the outside to achieve an IP67 seal.
3. **Install Battery & PCB:**
   * Place the 600 mAh LiPo pouch battery into the central battery cradle ($X = 14\dots 54\,\text{mm}$) of the lower shell.
   * Plug the 2-pin JST lead into `BAT1`.
   * Seat the PCB component-side up into the guide bosses, ensuring the USB-C port `J1` seats cleanly into its frontal gasket flange.
4. **Connect Helmet Audio & PTT Harness (`J_HELMET`):**
   * Plug the 6-pin JST-SH connector of the helmet audio harness into header `J_HELMET` on `B.Cu` ($X=126.5, Y=99.75\,\text{mm}$ in KiCad, $X_{\text{mod}} = 60.5\,\text{mm}$, receptacle socket facing inward).
   * Route the flexible AWG30/32 silicone lead in a gentle bend downward through the rear bottom slot ($9.0 \times 9.0\,\text{mm}$ at $X = 55\dots 64\,\text{mm}$) of the lower shell.
5. **Fasten Enclosure (100% Soldering-Iron Free):**
   * Seat the upper shell, verifying seamless perimeter gasket alignment.
   * Fasten 4x DIN 912 M2 $\times 8\,\text{mm}$ stainless socket head screws from underneath through the countersunk holes into the captive DIN 934 M2 nuts in a crosswise pattern.
6. **Thread On Stubby Antenna:**
   * For OMM 2.4 GHz (`PCBA 09`): Screw on the compact 38 mm 2.4 GHz Rubber-Duck stubby antenna onto the SMA jack.
   * For OMM 446 (`PCBA 10`): Screw on the compact 48 mm 446 MHz helical stubby antenna onto the SMA jack.
7. **Helmet Installation (ECE 22.06 UCS Slot):**
   * Slide the assembled module into the helmet manufacturer's UCS recess (e.g., HJC, Shoei, Schuberth) until it locks in place.
   * Route the audio harness exiting from the underside directly into cheek pad cutouts:
     - Connect 3.5 mm stereo jack to helmet speakers.
     - Connect 2-pin micro jack to boom or adhesive microphone.
     - Route PTT line to chin bar or finger button.
   * The frontal USB-C port remains fully accessible on the outside of the helmet for powerbank charging on the go or WebUSB DFU updates.

---

### Step 4: Universal Front Node (PCBA 05) Assembly
1. **Insert Captive Nuts (100% Soldering-Iron Free & Infinite Service Life):**
   * Press **4x M3 stainless steel nuts (DIN 934 / DIN 985)** from below into the form-fit hex pockets at the 4 corners of the lower tub ([`front_node_lower_tub.stl`](../../hardware/cad/stl/04_front_node/front_node_lower_tub.stl)) (fully analogous to the Central Box).
   * Press **4x M4 stainless steel nuts (DIN 934)** into the form-fit hex pockets of the AMPS pattern on the tub underside.
   * *Benefit:* Pure steel-in-steel clamping. The enclosure can be opened and retorqued indefinitely for wiring maintenance without degrading plastic threads.
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
+-----------------------------------------------------------------------------+
|       OPENMOTORBRIDGE BENCHTOP DRY-RUN (LABORATORY WORKBENCH SETUP)         |
+-----------------------------------------------------------------------------+
|                                                                             |
|   [ 230V USB Charger / Power Bank / Laptop (5V / ≥ 2.4A) ]                  |
|       |                      |                      |                       |
|  USB-C|Cable 1          USB-C|Cable 2          USB-C|Cable 3                |
|       v                      v                      v                       |
|  +---------------+     +---------------+      +---------------+             |
|  |  CENTRAL BOX  |     |  FRONT NODE   |      | SATELLITE POD |             |
|  |   (PCBA 01)   |     |   (PCBA 05)   |      | (Pod 1 / 2)   |             |
|  |  Port J7 USB-C|     |  Port J5 USB-C|      | M8 Adapter    |             |
|  +-------+-------+     +-------+-------+      +-------+-------+             |
|          |                     |                      |                     |
|          |   UWB Wireless Link |                      | 1-Wire & Direct-DC  |
|          |<------------------->|                      v                     |
|          |  (6.5 GHz, <0.4 ms) |             +-------------------+          |
|          |                     |             | SMART CARTRIDGE   |          |
|          |                     |             | (Sena / Cardo)    |          |
|          |                     |             +--------+----------+          |
|          | WebBLE / WebSerial  |                      |                     |
|          v                     v                      v                     |
|    [ SMARTPHONE / LAPTOP WITH PWA ]            [ RIDER HELMET ]             |
|    (Chrome / Edge: Flasher & Dashboard)        (Bluetooth Paired)           |
|                                                                             |
+-----------------------------------------------------------------------------+
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
* **Saddlebag Quick-Breakaway Interface (2-Pin Magnetic Pogo "MagSafe Alternative"):**
  * **Frame-Side Dock:** Bolt the 3D-printed frame dock ([`009_magsafe_frame_dock.stl`](../../hardware/cad/stl/02_pod_base/parts/009_magsafe_frame_dock.stl)) with clamp collar ([`009_magsafe_frame_clamp.stl`](../../hardware/cad/stl/02_pod_base/parts/009_magsafe_frame_clamp.stl)) to the Ø 26 mm frame tube under the seat overhang with 4x M3 $\times 16\,\text{mm}$ screws (DIN 934 nut pockets). Seat the 2-pin magnetic pogo socket (HytePro M411) form-fittingly and connect to Whip 1 or 2 of the DTM-12 harness.
  * **Saddlebag Forward Wall & Split Grommet:** Drill a single $\varnothing 12\,\text{mm}$ hole on the inner forward wall of the saddlebag above the swingarm pivot (inside the wind and road spray shadow; the **saddlebag floor remains 100% hole-free and watertight**). Insert the split EPDM/TPU grommet ([`010_saddlebag_hole_grommet_split.stl`](../../hardware/cad/stl/02_pod_base/parts/010_saddlebag_hole_grommet_split.stl)), route the 2-wire ribbon cable through, and anchor it with a mini zip-tie on the integrated clamp tower. Inside the bag, guide the cable along the check strap without tension to the lid dock snout.
* **Rear Radar (Heavy-Duty Swivel Cradle & Spray Protection):**
  * **Bench Pre-Assembly (100% Soldering-Iron Free):** Bolt the sealed Radar 2.0 housing ([`radar_mr20_housing.stl`](../../hardware/cad/stl/05_accessories/radar_mr20_housing.stl)) with its internal DIN 934 M4 nuts to the adapter plate ([`radar_swivel_tilt_cradle.stl`](../../hardware/cad/stl/02_pod_base/radar_swivel_tilt_cradle.stl)) using two DIN 912 M4 $\times$ 12 mm steel bolts. Solid shear bosses absorb 100% of lateral shock loads.
  * **Option A: License Plate Bracket:** Clamp the license plate bracket ([`radar_license_plate_bracket.stl`](../../hardware/cad/stl/02_pod_base/radar_license_plate_bracket.stl)) under the lower M6 license plate screws. Slide the cradle Hirth tongue into the clevis fork, align the radar beam horizontally ($\pm 2^\circ$), and clamp securely with a DIN 912 M5 $\times$ 25 mm bolt and DIN 934 M5 nut.
  * **Option B: Under-Fender Mount (Bobbers / Custom Bikes):** Bond or bolt the Stealth Center Under-Fender Mount ([`radar_center_underfender_mount.stl`](../../hardware/cad/stl/02_pod_base/radar_center_underfender_mount.stl)) centrally under the rear fender trailing edge using 3M VHB 5952 tape or 2x M4/M5 countersunk screws. Slide the cradle into the clevis and lock with an M5 bolt. The integrated 42 mm roost deflector shield protects the joint and bottom M8 gland from rear tire spray.
  * **Water Spray Protection (Drip Loop):** Route the 2-wire FLRY-B cable from Whip 5 down the spine conduit and guide it in an upward drip loop through the bottom M8 IP68 cable gland. The monolithic roost deflector on the housing bottom protects the gland from rear tire road spray.
* **Front Node:** Secure inside fairing (Batwing / Sharknose) or nacelle; 12V from auxiliary plug; CAN connected locally at J2 (or under seat at Central Box).

### 5.2 Adventure Platform (BMW GS / GSA Family)
* **Central Box:** Mount inside frame triangle under rider seat on 4x M4 vibration isolators.
* **Cockpit & Front Node:** Mount to Ø 12 mm GPS bar above TFT display; 12V via factory BMW Cartool plug.
* **Pod 1 & Pod 2:**
  * *Option A (Vario Panniers / GS Standard):* Transition docks ([`adventure_transition_dock_base.stl`](../../hardware/cad/stl/02_pod_base/adventure_transition_dock_base.stl)) in seat frame crease (Ø 28 mm tube) with 4x strap hook clearance pockets, coupled with underseat cross-rail ([`adventure_underseat_cross_rail.stl`](../../hardware/cad/stl/02_pod_base/adventure_underseat_cross_rail.stl)) for concealed 2-wire DC harness routing.
  * *Option B (Stainless Pannier Racks / GSA):* Heavy-duty GSA cage docks ([`adventure_gsa_cage_dock_body.stl`](../../hardware/cad/stl/02_pod_base/adventure_gsa_cage_dock_body.stl)) in 45 mm frame dead space with 4x strap hook clearance pockets and zip-tie anchor bridge in tube clamp shadow for 2-wire DC cable.
* **Rear Radar (Adventure Luggage Rack Mount):**
  * **Tube Clamp Assembly:** Place the lower base mount ([`adventure_rack_radar_mount.stl`](../../hardware/cad/stl/02_pod_base/adventure_rack_radar_mount.stl)) and upper clamp cap ([`adventure_rack_radar_clamp_cap.stl`](../../hardware/cad/stl/02_pod_base/adventure_rack_radar_clamp_cap.stl)) around the rear Ø 18 mm luggage bridge cross-tube.
  * Insert 2x DIN 934 M5 nuts into the top cap pockets. Fasten with 2x DIN 912 M5 $\times$ 25 mm bolts from below (bottom screw access allows full adjustment without removing topcase baseplates).
  * Insert the pre-assembled Radar 2.0 housing with `radar_swivel_tilt_cradle.stl` into the clevis fork, level horizontally, and clamp firmly with a DIN 912 M5 $\times$ 25 mm bolt.
  * The monolithic $45^\circ$ forward deflector wedge shields the pivot joint and M8 wiring from stones thrown up by knobby offroad tires.

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
