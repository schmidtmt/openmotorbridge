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
                         1x CENTRAL HARNESS (DEUTSCH DTM-12 IP67/IP69K)
                                           |
          +--------------------------------+--------------------------------+
          |                                |                                |
          v Whip 1                         v Whip 2                         v Whip 5
+------------------+             +------------------+             +------------------+
| 1x POD 1 (LEFT)  |             | 1x POD 2 (RIGHT) |             | 1x REAR RADAR    |
| (Frame / Pannier)|             | (Frame / Pannier)|             | (Optional)       |
| * Pod enclosure  |             | * Pod enclosure  |             | * Wheeltec MR20  |
| * 2-Wire DC      |             | * 2-Wire DC      |             |   or Garmin      |
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
  * 1x Main Box (lower tub with UWB bottom pocket $11 \times 11 \times 0.6\,\text{mm}$, mid tray with $70 \times 10\,\text{mm}$ open front cable bay, hinged battery & antenna bridge [`main_box_battery_bridge.stl`](../../hardware/cad/stl/01_main_box/main_box_battery_bridge.stl), and 100% cable-free solid lid [`main_box_lid.stl`](../../hardware/cad/stl/01_main_box/main_box_lid.stl))
  * 2x Pod base enclosures (seamless 1-piece monocoques with integral monolithic bulkhead, mounting pocket for IP67 direct blade plug & spring guide posts; 0 assembly screws, 0 loose parts)
  * 2x Cartridge base sleds (with UWB antenna floor pocket & DIN 934 M2 captive nut standoffs), inlays (Sena SPIDER X Slim, Cardo Packtalk Edge, Swap OMM, or blank cartridge) & 2x magnetic latches
  * 1x Front Node (lower tub with UWB bottom pocket and AMPS nut pockets, upper lid, TPU cable glands & USB-C cap)
  * 1x Vehicle-specific mounting kit (BMW GS clamps & `adventure_rack_radar_mount.stl` / Harley saddlebag docks & license plate bracket / Support-Car `car_sun_visor_pod_clip.stl`)
  * *(Optional for helmet operation / OMM):* 1-2x OMM UCS upper shells ([`omm_ucs_top_shell.stl`](../../hardware/cad/stl/03_pod_cartridges/omm_ucs_top_shell.stl)), lower shells ([`omm_ucs_bottom_shell.stl`](../../hardware/cad/stl/03_pod_cartridges/omm_ucs_bottom_shell.stl)) & silicone keypads ([`omm_ucs_silicone_keypad.stl`](../../hardware/cad/stl/03_pod_cartridges/omm_ucs_silicone_keypad.stl))
* [ ] **Fully Populated PCBAs (from JLCPCB / Eurocircuits - the 7-PCBA lineup):**
  * 1x PCBA 01 (Central Box with onboard LoRa SX1262 and DW3110 UWB)
  * 2x PCBA 03 (Universal Smart Cartridge Rev 3.0 All-UWB with DW3110 UWB, ES8388 / MCU, 4x AO3400 N-MOSFETs and SMT dual-beam slot socket `J_DC_IN`, 2-sided SMT)
  * 1x PCBA 05 (Front Node with DW3110 UWB)
  * *(Optional: 1x PCBA 08 Radar 2.0 Sub-MCU, 1x PCBA 07 Smart-Keyfob)*
  * *(Optional for Helmet / OpenMotorMesh):* 1x **PCBA 09 (OMM 2.4 GHz HD-Mesh)** and/or 1x **PCBA 10 (OMM 446 PMR/DMR Radio)**
  * *(Note: PCBA 02, PCBA 04 and PCBA 06 are completely eliminated).*
* [ ] **A4 / 316 Stainless Fasteners & Springs (IKEA Principle - 100% Solder-Free):**
  * 8x DIN 934 / DIN 985 M3 stainless nuts (for captive enclosure nut pockets)
  * 6x DIN 934 M4 nuts (4x AMPS nut pockets in Front Node tub, 2x Radar 2.0 rear housing)
  * 4x M3 x 40 mm socket head screws (Central Box), 4x M3 x 20 mm screws (Front Node)
  * 8x M2.5 x 6 mm board screws (Central Box & Front Node), 8x M2 x 6 mm board screws (Cartridge PCBA 03; bulkhead screws completely eliminated)
  * 4-8x DIN 934 M2 nuts & 4-8x DIN 912 M2 x 8 mm socket head screws (for OMM UCS enclosure fastening)
  * 2x DIN 7 M2 x 8 mm dowel pins (latch pivots), 2x DIN 6325 Ø 6 x 8 mm hardened steel keeper pins
  * 2x Latch return springs, 4x auto-eject compression springs, 1x N52 neodymium release key
  * 2x Pre-assembled IP67 DC direct blade plugs (2-pin automotive blade with axial O-ring & U-clip) for Pod 1 & 2 power feed
* [ ] **Gaskets, Battery & Antennas:**
  * Silicone O-ring cord Ø 1.5 mm Shore 40A ($40\,\text{cm}$ Main Box, $30\,\text{cm}$ Front Node)
  * Silicone O-ring cord Ø 0.8 mm Shore 40A ($25\,\text{cm}$ per OMM UCS module)
  * 2x Molded silicone face gaskets for Pod 1 & 2 mouths, Gore ePTFE vent stickers
  * 2x NBR70 O-rings ($\varnothing 12 \times 1.5\,\text{mm}$) for Pod 1 & 2 IP67 direct blade plugs
  * **1x 1S LiPo Flat Pack 2,200 mAh** ($68 \times 39 \times 5.0\,\text{mm}$) with Molex Micro-Fit 3.0 connector (Central Box UPS)PS)
  * **1-2x 1S LiPo Pouch Battery 600 mAh** ($38 \times 24 \times 4.5\,\text{mm}$) with JST 2-Pin connector (OMM UCS modules)
  * **Taoglas FXUWB10 UWB Flex Antennas** with 20 mm U.FL leads (Central Box, Front Node, Cartridges)
  * **1x Taoglas FXP895 LoRa 868 MHz Flex Antenna** with 50 $\Omega$ U.FL lead
  * **1x Taoglas FXP73 2.4 GHz Wi-Fi/BLE Flex Antenna** with 50 $\Omega$ U.FL lead
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
4. **Mid Tray & Open Front Cable Bay:**
   * Lower the mid tray ([`main_box_mid_tray.stl`](../../hardware/cad/stl/01_main_box/main_box_mid_tray.stl)) into place.
   * Route all 6 internal cable leads (12-pin DTM-12 harness, USB-C service lead, DC power harness, Molex Micro-Fit battery lead, LoRa U.FL coax, 2.4 GHz Wi-Fi/BLE U.FL coax) freely and smoothly through the wide $70 \times 10\,\text{mm}$ open front bay without pinching.
5. **Hinged Battery & Antenna Bridge Installation:**
   * Adhere the Taoglas FXP895 (LoRa 868 MHz) and Taoglas FXP73 (2.4 GHz) flex antennas into their designated pockets on the upper side of the bridge ([`main_box_battery_bridge.stl`](../../hardware/cad/stl/01_main_box/main_box_battery_bridge.stl)).
   * Snap the $0.8\,\text{mm}$ PA12 protective cover plate into place over both antennas for complete scratch and handling protection.
   * Press the antenna coaxial leads into the integrated $\varnothing 1.25\,\text{mm}$ C-clip strain reliefs on the hinge end.
   * Hook the L-tabs on the left side of the bridge into the hinge sockets of the mid tray cradle.
   * Insert the 2,200 mAh LiPo battery into the cradle beneath the 1.0 mm EPDM compression pad, plug the Micro-Fit lead into `J_BAT`, and swing the bridge down until the right cantilever snap latch clicks securely into the frame pocket.
6. **Seal & 100% Cable-Free Solid Lid:**
   * Seat the silicone O-ring cord (Ø 1.5 mm, $40\,\text{cm}$) into the perimeter sealing groove of the mid tray.
   * Affix the Gore ePTFE pressure equalization vent membrane to the lid boss.
   * Place the 100% passive, cable-free solid lid ([`main_box_lid.stl`](../../hardware/cad/stl/01_main_box/main_box_lid.stl)) on top and fasten with 4x M3 $\times 40\,\text{mm}$ screws. Because there are no antennas or cables attached to the lid, the box can be opened during maintenance in seconds without touching or straining any fragile RF connectors!

---

### Step 2: Assemble Satellite Pods 1 & 2 (2x Identical 1-Piece Screwless Monocoques)
1. **Provide 2-Wire DC Feed from Main Harness:**
   * Power originates directly from the central box (`PCBA 01`). Two pre-crimped 2-wire DC whips (Whip 1 for left Pod 1, Whip 2 for right Pod 2) branch off the main Deutsch DTM-12 connector:
     * **Wire 1 (Red):** Switched $+5\,\text{V}$ (or VCC, protected via 500mA PPTC on `PCBA 01`), AWG22 ($0.34\,\text{mm}^2$) silicone.
     * **Wire 2 (Black):** Common system ground `GND`, AWG22 ($0.34\,\text{mm}^2$) silicone.
2. **Mount IP67 Direct DC Blade Plug Tool- & Solder-Free (IKEA Principle):**
   * The 2-wire leads terminate at the pre-assembled, waterproof **2-Pin Automotive Blade Direct Plug (`CON_POD_DC`)**.
   * Slide the axial NBR70 O-ring ($\varnothing 12 \times 1.5\,\text{mm}$) onto the plug shoulder collar.
   * Push the plug from the exterior into the form-fitting aperture in the enclosure rear bulkhead wall. The two heavy-duty gold-plated contact blades ($2.8 \times 0.8\,\text{mm}$, $10.0\,\text{mm}$ pitch) project $6.0\,\text{mm}$ in horizontal $+X$ direction into the cartridge docking chamber.
   * Slide the stainless steel U-retaining clip sideways into the locking groove until it clicks into position. The plug is **100% positively retained, vibration-proof, and seals the rear wall hermetically to IP67** — completely solder-free and tool-free!
3. **Mount Auto-Eject Springs:**
   * From the front opening, slide the two stainless compression springs ($\varnothing 4.5 \times 15\,\text{mm}$, $1.2\,\text{N/mm}$ spring rate) directly onto the two integrated guide posts of the monolithic bulkhead partition (at $Y = 16.0\,\text{mm}$ and $Y = 54.0\,\text{mm}$).
4. **Screwless Completion:**
   * Because the transverse bulkhead is 100% integrally molded into the 1-piece monocoque (`PCBA 02` is completely retired), no internal PCBs, screws, or loose wire harnesses are required inside the pod (0 screws). The two blade contacts and dual ejection springs await cartridge docking. Repeat for Pod 2.
   * *(Note on Unpopulated Bays):* When riding without an active cartridge, the pod bay is sealed by the standard blank storage cartridge (`03_insert_blindkassette.scad`) or an elastic TPU dust cap. The electronic eFuse on `PCBA 01` keeps unpopulated ports 100% unpowered ($0.0\,\text{V}$).

---

### Step 3: Multi-Protocol Gateway Cartridges 1 & 2 Assembly
1. **Power Delivery & UWB Antenna Concept (100% Cable- & Plug-Free to Pod):**
   * **Power Delivery via SMT Dual-Beam Slot Socket (Zero Cables to Housing!):** The cartridges require no loose wire whip and no external plug to the pod enclosure. Power is transferred purely electromechanically via a factory-assembled high-current dual-beam blade slot socket:
     * Mounted horizontally at the rear edge of `PCBA 03` is a factory SMT-assembled **2-Pin Dual-Beam Slot Socket (`J_DC_IN`)** (Pin 1: $+5\,\text{V}$, Pin 2: `GND`, $10.0\,\text{mm}$ pitch, rated for 5 A continuous).
     * The internal spring contact beams are deeply recessed within the high-temperature insulating polymer body. This makes the portable cartridge completely **finger-safe (IP2X) and immune to short circuits against keys or coins** when carried in jacket pockets or luggage.
     * In the floor of the cartridge base sled ([`cartridge_base_sled.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl)), an open rectangular contact window ($15.0 \times 6.0\,\text{mm}$) is molded into the rear face.
     * When sliding the cartridge fully into the pod, the two solid blade contacts of the pod direct plug mate positively into slot socket `J_DC_IN`. Opposing spring beams clamp the blades firmly from both sides (**self-cleaning wiping contact**).
     * **100% Vibration-Proof:** Unlike blunt butt-contact pogo pins, axial vehicle shocks and engine vibrations merely slide the blade deeper or shallower inside the slot without breaking electrical continuity. **Zero contact bounce (micro-bouncing), zero fretting corrosion.**
   * **UWB Antenna Interface (Hirose U.FL Receptacle & Taoglas FXUWB10 Flex Antenna):**
     * `PCBA 03` does **not** use a ceramic chip antenna. Instead, a **Hirose U.FL coaxial receptacle** (`ANT_UWB`, U.FL-R-SMT-1) is mounted on the bottom copper face (`B.Cu`) directly beside the Qorvo DW3110 transceiver IC.
     * The dedicated antenna is a flexible wideband flat antenna: **Taoglas FXUWB10** ($12.0 \times 12.0 \times 0.8\,\text{mm}$, 6.5 GHz Channel 5).
     * Place the antenna into the form-fitting recess pocket ($12.0 \times 12.0 \times 0.9\,\text{mm}$) in the floor of the cartridge base sled and secure with its 3M adhesive backing.
     * Route the short $20\dots 30\,\text{mm}$ U.FL micro-coax cable in the sled floor routing channel and snap vertically onto receptacle `ANT_UWB` on `B.Cu` of `PCBA 03`.
2. **Mount PCBA 03 in Sled:**
   * Place `PCBA 03 Rev 3.0` onto the four M2 standoffs in the rear section of the sled with top side facing up (`F.Cu`: ESP32-C6, MOSFETs, `J_ACT`, `J_AUDIO_PWR`, socket `J_DC_IN`).
   * Snap U.FL antenna lead onto `ANT_UWB` before fastening the board.
   * Fasten board finger-tight with 4x M2 $\times 6\,\text{mm}$ screws.
   * *Visual Inspection:* Verify through the rear contact window that the lead-in funnels of socket `J_DC_IN` are cleanly centered and unobstructed.
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
   * **Alternative Option: Midland PMR446 Radio Cartridge (Class 3a Analog Radio):**
     * **Variant A (Internal Compact Inlay):** Compact walkie-talkies (e.g. Midland XT30 or bare-board modules) sit directly inside the cartridge bay. Connect 8-pin JST-SH harness to dual-jack (2.5 mm Mic / 3.5 mm Spk) and 5V DC battery eliminator dummy; PTT keying is handled via Pin 8 (`PTT_IO` via MOSFET `Q4`). The cartridge shell remains 100% solid & sealed (IP67).
     * **Variant B (External Bulky Radio / Tethered Breakout):** For large handheld radios (Midland G7/G9 Pro, Kenwood, Baofeng, commercial VHF/UHF) that cannot fit into the pod, use the base sled with front through-hole (`has_sma_port = true`). Fit an M8 or PG7 cable gland or EPDM sealing grommet into the $\varnothing 6.5\,\text{mm}$ bore. Route the multi-conductor shielded umbilical cable from `J_AUDIO_PWR` (Mic, Spk, PTT, 5V power) through the gland to the external radio in a tank bag, pannier, or handlebar holster.
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
4. **Acoustic Membrane:** Stick hydrophobic Gore ePTFE membrane over the frontal acoustic port of the digital MEMS microphone (`MK1`).
5. **Connect Harnesses (2-Strand Clean-Architecture):**
   * **Cockpit Harness (`cable_cockpit_harness_16p`):** Snap 16-pin 2.0 mm latching connector onto `J_COCKPIT`. Route shielded round harness ($\varnothing 6.0\,\text{mm}$) through South TPU gland to **Cockpit Breakout Satellite** ([`cockpit_breakout_block.scad`](../../hardware/cad/scad/04_front_node/cockpit_breakout_block.scad)).
   * **Vehicle Harness (`cable_vehicle_harness_12p`):** Snap 12-pin 2.0 mm latching connector onto `J_VEHICLE`. Route shielded round harness ($\varnothing 6.5\,\text{mm}$) through North TPU gland to **Vehicle Breakout Satellite** ([`vehicle_breakout_block.scad`](../../hardware/cad/scad/04_front_node/vehicle_breakout_block.scad)).
6. **Seal Enclosure:**
   * Insert TPU sealing combs into lower tub guide slots.
   * Place silicone cord (Ø 1.5 mm Shore 40A, $30\,\text{cm}$) into lid groove.
   * Seat lid and tighten 4x M3 $\times 20\,\text{mm}$ stainless steel bolts crosswise.
7. **Assemble Breakout Satellites:**
   * **Cockpit Satellite:** The 16-wire cable plugs via 16-pin 2.0 mm latching connector onto `J_IN` of `PCBA 05B` ([`cockpit_breakout_block.scad`](../../hardware/cad/scad/04_front_node/cockpit_breakout_block.scad)). The board provides 5x USB-C receptacles (`[ PHONE 20W ]`, `[ DONGLE ]`, `[ HOST ]`, `[ CAM 5V ]`, `[ NAVI 5V ]`) and the positive-locking 2-pin **JST-GH SMD Header (`J6`)** for handlebar PTT (100% SMD with 0 mm underside protrusion, laying completely flush). The M3 strain-relief clamp bar secures COTS USB-C plug necks against vibration.
   * **Vehicle Satellite:** The 12-wire cable breaks out directly into 5 watertight **JST-JWPF (IP67)** latching sockets (`[ 12V IN ]`, `[ CAN BUS ]`, `[ MIRROR BSD ]`, `[ AUX LIGHT ]`, `[ GNSS / CLIMATE PUCK ]`). For bike connection, vehicle-specific adapter cables (e.g. BMW Cartool, BMW CAN Y-Splitter, Harley Fairing Aux) plug directly into the JWPF sockets without cutting wires. Snap lid closed.

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
* **Front Node & Breakout Satellites (Fairing Stealth Installation):**
  * **Front Node Mounting:** Mount directly under fairing (Sharknose FLTRX, Batwing FLHX or CVO ST) on fairing support brackets (Ø 16–19 mm tube) using the 2-piece clamp ([`front_node_fairing_tube_clamp.stl`](../../hardware/cad/stl/04_front_node/front_node_fairing_tube_clamp.stl)).
  * **Dovetail Combo Block:** Cockpit and vehicle satellites can slide-interlock via lateral dovetail rails into a single compact combo block inside glovebox or fairing wall.
  * **Plug-and-Play Vehicle Interfacing (Zero Wire-Cut):**
    * `[ 12V IN ]`: Connect directly to 2-pin OEM fairing accessory plug via **Harley Fairing-Aux Adapter Cable** (`cable_adapter_jwpf_hd_fairing_aux`).
    * `[ CAN BUS ]`: Intercept HD-LAN / CAN bus non-destructively at diagnostic port or speedo Y via **Harley CAN Y-Splitter Cable** (`cable_adapter_jwpf_hd_can_splitter`).
    * `[ AUX LIGHT ]`: Connect auxiliary lights or GPS cradle via **Deutsch DT-2 Adapter Cable** (`cable_adapter_jwpf_deutsch_dt2_aux`).
    * `[ GNSS / CLIMATE PUCK ]`: Route to SAM-M10Q GNSS & TMP117 puck in air intake via **Qwiic JST-SH Adapter Cable** (`cable_adapter_jwpf_qwiic_sh`).

### 5.2 Adventure Platform (BMW GS / GSA Family)
* **Central Box:** Mount inside frame triangle under rider seat on 4x M4 vibration isolators.
* **Cockpit, Front Node & Satellites (Plug & Play at Beak / Handlebars):**
  * **Front Node Mounting:** Fasten to Ø 12 mm GPS rail above TFT display or fairing stays using 2-piece clamp.
  * **Cockpit Satellite:** Positioned separately on handlebars/riser (via zip-tie channels) for cable-free phone charging without steering neck entanglement.
  * **Vehicle Satellite:** Fastened frame-side at steering head / beak.
  * **Plug-and-Play Vehicle Interfacing (Zero Wire-Cut):**
    * `[ 12V IN ]`: Plug directly into factory 3-pin BMW Cartool accessory socket (BMW P/N 83300413585) over oil cooler/steering head using pre-assembled **BMW Cartool Adapter Cable** (`cable_adapter_jwpf_bmw_cartool`). Provides clean switched ignition (KL15) with automatic ZFE/BCO 60-second shutdown.
    * `[ CAN BUS ]`: Intercept BMW CAN bus non-destructively at navigation prep cradle via **BMW CAN Y-Splitter Cable** (`cable_adapter_jwpf_bmw_can_splitter`).
    * `[ AUX LIGHT ]` (GSA): Connect directly to auxiliary LED lamps (Denali D3/D7 or Wunderlich) via **Deutsch DT-2 Adapter Cable** (`cable_adapter_jwpf_deutsch_dt2_aux`).
    * `[ GNSS / CLIMATE PUCK ]`: Route to SAM-M10Q GNSS & TMP117 puck inside beak via **Qwiic JST-SH Adapter Cable** (`cable_adapter_jwpf_qwiic_sh`).
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
