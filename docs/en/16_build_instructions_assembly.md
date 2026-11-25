# 16 - Build Instructions, Wiring & Vehicle Installation

This document is the complete, hands-on step-by-step assembly manual for building and installing a complete **OpenMotorBridge (v10.0 Native USB-PD & Edge-AI Generation)** system on any motorcycle or support vehicle.

---

## 1. System Kit Overview (What is being built?)

The v10.0 generation of OpenMotorBridge completely eliminates brittle short-range UWB wireless links, motorized cassettes, and servo actuators. Instead, it introduces the **Two-Cable Architecture of the Central Box**, a **ruggedized 4-wire Automotive USB-PD & USB 2.0 bus (`VBUS`, `GND`, `D+`, `D-`)** delivering up to 60 W to the Front Node and 30 W per saddlebag pod, paired with the **ESP32-S31** (Dual-Core 320 MHz RISC-V with 128-bit SIMD AI accelerator for on-device voice and audio classification), the **3× Qualcomm QCC3086** Bluetooth audio transceivers (Phone Link `U9`, Rider Helmet `U13`, Pillion Helmet `U14`), and **2 mechatronic cold-start pushers** per pod:

```text
                      +-------------------------------------------------------------+
                      |               1x CENTRAL MAIN BOX (IP67)                    |
                      |            (Under seat / over battery bridge)               |
                      |    * Host MCU: ESP32-S31 (Dual-Core RISC-V @ 320 MHz,       |
                      |      128-bit SIMD AI Audio Engine, Native USB 2.0 480 Mbps) |
                      |    * 3x QCC3086: Phone (U9), Rider (U13), Pillion (U14)     |
                      |    * Emergency SOS: SX1262 LoRa 868 MHz (Taoglas FXP895)    |
                      |    * UPS Backup: 2,200 mAh LiPo with Molex Micro-Fit 3.0    |
                      +--+---------------------------------------+------------------+
                         |                                       |
                         | [J1]                                  | [J_PERIPH]
                         v                                       v
                CABLE 1 (Vehicle & CAN)                 CABLE 2 (OMB Periphery Bus)
                Deutsch DTM06-6S (IP68)                 16-Pin Automotive Header (IP68)
                * Pin 1: KL30 (+12V Battery Power)      * Branch 1 (1.5 m): Front Node (60W PD + USB 2.0)
                * Pin 2: KL15 (Ignition Power)          * Branch 2 (1.0 m): Pod 1 Left (30W PD + USB 2.0)
                * Pin 3: GND (Chassis Ground)           * Branch 3 (1.0 m): Pod 2 Right (30W PD + USB 2.0)
                * Pin 4..5: CAN_H / CAN_L               * Branch 4 (0.5 m): Rear Radar MR20 (12V Switched)
                * Pin 6: SHIELD                         |
        +-----------------------+-----------------------+-----------------------+
        |                       |                       |                       |
        v Branch 2 (30W PD)     v Branch 3 (30W PD)     v Branch 4 (12V)        v Branch 1 (60W PD)
+-------------------+   +-------------------+   +-------------------+   +-------------------------------+
| 4-Pin Magnetic    |   | 4-Pin Magnetic    |   | 1x REAR RADAR 2.0 |   | 1x FRONT NODE & COCKPIT HUB   |
| Breakaway Coupling|   | Breakaway Coupling|   | (License Plate    |   | (Handlebar Riser / Nacelle)   |
| (HytePro M411)    |   | (HytePro M411)    |   |  Wheeltec MR20    |   | * 60W USB-PD Engine (SC8721/  |
+---------+---------+   +---------+---------+   |  77 GHz Radar     |   |   SC8102, Phone, GPS, Cams)   |
          |                       |             |  PCBA 08 Sub-MCU  |   | * Snap-On Sensor Puck (SAM-   |
          v Bag Wall Grommet      v Bag Wall Grommet|  36x Alert LEDs)  |   |   M10Q, TMP117, OPT3001,      |
+-------------------+   +-------------------+   +-------------------+   |   Knowles MEMS Wind-Mic)      |
| 1x POD 1 (LEFT)   |   | 1x POD 2 (RIGHT)  |                           +---------------+---------------+
| (Hard Saddlebag   |   | (Hard Saddlebag   |                                           |               |
|  Lid-Dock)        |   |  Lid-Dock)        |                           +---------------+               v
| * 2x Cold-Start   |   | * 2x Cold-Start   |                           | 2x UNDER-PERCH|   +---------------+
|   Pushers JF-0530B|   |   Pushers JF-0530B|                           | MIRROR PODS   |   | 1x GLOVE BOX  |
|   (15-85mm Slide  |   |   (15-85mm Slide  |                           | (Left & Right)|   | CHARGING BAY  |
|    Bracket)       |   |    Bracket)       |                           | * Left: PTT   |   | * 15W Qi Puck |
| * 30W Saddlebag   |   | * 30W Saddlebag   |                           | * Right: Cam  |   | * 30W USB-C PD|
|   USB Charging    |   |   USB Charging    |                           | * Bilateral   |   | * FSC-BT802   |
| * PCBA 03 Smart   |   | * PCBA 03 Smart   |                           |   BSD LEDs    |   |   Audio Bridge|
|   Gateway (Sena/  |   |   Gateway (Sena/  |                           +---------------+   | * Pure DC Feed|
|   Cardo/OMM/Midl) |   |   Cardo/OMM/Midl) |                                               +---------------+
+-------------------+   +-------------------+
```

---

## 2. Pre-Assembly Checklist (Parts & Hardware Verification)

> [!TIP]
> **100% Solder-Free Assembly (IKEA Principle) & Native USB-DFU:**  
> All 3D printed parts (`.scad` / `.stl`) are designed with precision manufacturing tolerances ($+0.15\,\text{mm}$ for HP MJF PA12 or ASA/PET-CF). Heat-set brass threaded inserts (Ruthex) have been completely eliminated across the entire system in favor of captive **DIN 934 hex nut pockets** (simply pressed in by hand). Self-tapping plastic screws are strictly prohibited.  
> **Native USB-DFU & Dual-Power Input:** All microcontrollers (ESP32-S31, ESP32-S31/E22, ESP32-C6, ESP32-C5) are centrally managed. The Central Box supports **Dual-Power Input (`LM66100` Ideal-Diode OR-ing)**: On the bench, any standard **5V USB-C cable into `J3`** (PC USB port or smartphone charger) powers the logic, configuration, and **Central Bus-DFU (firmware updates across all bus nodes)**. For full 60W/30W load testing of the 12V bus branches and cold-start solenoids, 12V DC is applied to `J1`.

All discrete components, PCB ordering files, and COTS sourcing lists are documented in **[Chapter 15: Bill of Materials & Manufacturing](15_bom_manufacturing.md)**. Ensure the following items are ready before assembly begins:

* [ ] **3D Printed Parts (MJF PA12 Black or FDM ASA/PET-CF):**
  * **1x Main Box (v10 Dual-Rail Monocoque):** Monolithic monocoque tub with isolation posts ([`000_monocoque_tub.stl`](../../hardware/cad/stl/01_main_box/000_monocoque_tub.stl)), slide-in intermediate tray with LiPo cradle and antenna nests ([`010_slide_tray.stl`](../../hardware/cad/stl/01_main_box/010_slide_tray.stl)), 100% cable-free L-Slide Lid with Slam-to-Shut Heckwand ([`020_slide_lid.stl`](../../hardware/cad/stl/01_main_box/020_slide_lid.stl)).
  * **2x Saddlebag Pods v10.0:** Monocoque pod tubs with fixed $14.0\,\text{mm}$ rear wall and optional SMA antenna knockout ([`002_pod_housing_base.stl`](../../hardware/cad/stl/02_pod_base/002_pod_housing_base.stl)), 2x seated TPU/EPDM intermediate dry-flap splash covers ($48 \times 56\,\text{mm}$, [`011_pod_slide_tray.stl`](../../hardware/cad/stl/02_pod_base/011_pod_slide_tray.stl)), 2x L-shaped slide-in lids with integrated rear wall (`Heckwand`) and PA12 U-yoke latch with downward-gripping **PA12 plastic claws ("Plastikkrallen")** ([`021_pod_slide_lid.stl`](../../hardware/cad/stl/02_pod_base/021_pod_slide_lid.stl)).
  * **2x Universal Actuator Cross-Struts (wall-guided in `Rail 1`):** ([`012_universal_actuator_slide_bracket.stl`](../../hardware/cad/stl/02_pod_base/012_universal_actuator_slide_bracket.stl)) with two independent cross-struts guided in the sidewall C-grooves (`Rail 1`, $Z = 21.5\dots 24.5\,\text{mm}$, 15–85 mm span), flush `DIN 7991` countersunk screws, and rear EPDM sealing plugs.
  * **1x Front Node Riser Enclosure (v10 Monocoque):** Monocoque tub ([`001_front_node_monocoque_tub.stl`](../../hardware/cad/stl/04_front_node/001_front_node_monocoque_tub.stl)) with 4-in-1 mounting floor / riser clamp ([`front_node_fairing_tube_clamp.stl`](../../hardware/cad/stl/04_front_node/front_node_fairing_tube_clamp.stl)), L-Slide lid with 2x2 MIMO antenna clips and sensor-puck snap dock ([`020_front_node_slide_lid.stl`](../../hardware/cad/stl/04_front_node/020_front_node_slide_lid.stl)), and TPU cable glands ([`front_node_cable_glands_tpu.stl`](../../hardware/cad/stl/04_front_node/front_node_cable_glands_tpu.stl)).
  * **1x Modular Snap-On Sensor Puck ($38 \times 38 \times 15\,\text{mm}$ enclosure with $\varnothing\,28 \times 14\,\text{mm}$ dome):** ([`sensor_puck_environmental.stl`](../../hardware/cad/stl/04_front_node/sensor_puck_environmental.stl) / [`sensor_puck_top.stl`](../../hardware/cad/stl/05_accessories/sensor_puck_top.stl) & [`sensor_puck_bottom.stl`](../../hardware/cad/stl/05_accessories/sensor_puck_bottom.stl)) tailored for `PCBA 05D` (34 x 34 mm, SAM-M10Q GNSS, TMP117, OPT3001).
  * **2x Symmetrical Under-Perch Mirror Pods (Left & Right):** Form-fitted brackets for mounting under both mirror perch nuts ([`under_perch_mirror_pod.stl`](../../hardware/cad/stl/05_accessories/under_perch_mirror_pod.stl)) with button guides (`PCBA 05C`, Left: PTT; Right: Cam-Tag) and integrated amber LED light tunnels for bilateral blind-spot detection.
  * **(Historically archived) 1x Glove Box 5-Port USB-C Hub Enclosure ($55 \times 25 \times 15\,\text{mm}$):** ([`glovebox_power_injection_hub.stl`](../../hardware/cad/stl/04_front_node/glovebox_power_injection_hub.stl)) for `PCBA 05B` (replaced in v10.5+ by 15W Qi Puck and 30W USB-C PD fast-charge port).
  * **1x Rear Radar Mount:** MR20 radar housing ([`radar_mr20_housing.stl`](../../hardware/cad/stl/05_accessories/radar_mr20_housing.stl)) with Hirth-joint swivel/tilt cradle, license plate bracket, and integrated roost deflector.
* [ ] **Fully Assembled PCBs (SMT Production, all 10 active PCBAs):**
  * **1x PCBA 01 (Central Box):** Host board with **ESP32-S31-WROOM-1U**, **3x Qualcomm QCC3086**, Microchip USB2517I Hub, SX1262 LoRa 868 MHz, vertical SMD headers (Vehicle Power `J1` Molex Micro-Lock Plus 1.25mm 6P, OMB Periphery Bus `J6` Molex Picoflex 1.27mm 16P, UPS `J5` 4P, Status LED `J4` 3P, Spare `J7` 4P), Dual-Power Input (12V Main & 5V USB-C Service Port `J3` with LM66100 Ideal-Diode OR-ing), and DM3D MicroSD Slot `J2`. *(DW3110 UWB completely eliminated!)*
  * **2x PCBA 03 (Saddlebag Pod Gateway):** Universal interface board with ESP32-C6-WROOM-1, 30W USB-PD sink/buck regulator, internal USB-C charging port, intercom audio routing (Sena / Cardo / OMM / Midland), PTT keying, and `J_ACT` header with AO3400A MOSFETs for 2.0 s cold-start actuation.
  * **1x PCBA 05 (Front Node Riser Hub):** 4-layer compact board ($82 \times 50\,\text{mm}$) with ESP32-S31-WROOM-1U + ESP32-E22 co-processor (480 Mbps High-Speed USB PHY, Wi-Fi 6E MIMO via SDIO 3.0), 60W USB-PD engine (TPS54302 + SW3526), `J_SENSOR_EXT` 8-Pin JST-GH port for the sensor puck, and accessory power (30W phone fast charge, 15W dedicated motorcycle GPS nav, 10W cam lead).
  * **(Historically archived) 1x PCBA 05B (Glovebox Hub):** 4-layer board ($50 \times 20\,\text{mm}$) (replaced in v10.5+ by 15W Qi puck and 30W USB-C PD fast-charge port).
  * **2x PCBA 05C (All-in-One Under-Perch Mirror Pod Board):** Identical 2-layer miniature boards ($18.25 \times 14.0\,\text{mm}$) for left and right mirror perches with micro-switch (Left: PTT; Right: Cam-Tag) and ultra-bright amber LED (BSD).
  * **1x PCBA 05D (Environmental Sensor Puck):** 4-layer board ($34 \times 34\,\text{mm}$) for SAM-M10Q GNSS, TMP117, OPT3001, and Bosch BMP390 altimeter (Knowles MEMS microphone `MK1` is positioned in the bottom of the Front Node).
  * **1x PCBA 07 (Smart-Keyfob & LoRa Pager):** 4-layer board ($46 \times 26\,\text{mm}$) with nRF52840, SX1262 LoRa, BQ51050B Qi receiver, and DRV2605L haptic driver.
  * **1x PCBA 08 (Rear Radar Sub-MCU):** 4-layer 77 GHz radar controller ($68 \times 28\,\text{mm}$) with ESP32-C5-WROOM-1, TPS54302, and 36x strobe warning LEDs.
  * **Optional 1x PCBA 09 (OMM 2.4 GHz Transceiver) / 1x PCBA 10 (Midland PMR446 Bridge):** 4-layer radio expansion boards ($56 \times 32\,\text{mm}$).
* [ ] **V4A Stainless Steel Hardware, Magnets & Actuators (100% Solder-Free & Screw-Free Lids):**
  * **4x Mini Linear Solenoids:** JF-0530B (12V DC, 300 mA, 10 mm stroke) with soft Shore A50 silicone caps (2x per pod).
  * 4x DIN 7991 V4A M2.5 x 8 mm countersunk screws (flush-mounted for snag-free clearance beneath the slide-in lid).
  * 8x DIN 934 / DIN 985 M2.5 / M3 stainless hex nuts (PCB standoff captive pockets)
  * 6x DIN 934 M4 nuts (radar and riser clamping)
  * 8x M2.5 x 6 mm PCB screws (Central Box & Front Node; enclosure lids themselves are 100% screw-free!)
  * 4x N52 Neodym magnets ($\varnothing 6 \times 2\,\text{mm}$ / $\varnothing 8 \times 3\,\text{mm}$) for L-slide-in lid latching
  * 1x OMB Smart Keyfob (`PCBA 07`) with matching N52 release magnet
* [ ] **Seals, Backup Battery & Antennas:**
  * Silicone round cord Ø 1.5 mm Shore 40A ($40\,\text{cm}$ Main Box, $25\,\text{cm}$ Front Node)
  * 2x Silicone profile gaskets for saddlebag slide-in lids
  * 2x EPDM/TPU split grommets for saddlebag front wall entry
  * **1x 1S LiPo Flat-Pack 2,200 mAh** ($68 \times 39 \times 5.0\,\text{mm}$) with Molex Micro-Lock Plus 1.25mm 4P connector (UPS)
  * **1x Taoglas FXP895 LoRa 868 MHz Flex Antenna** with U.FL cable
  * **1x Taoglas FXP73 2.4/5 GHz Wi-Fi/BLE Flex Antenna** with U.FL cable
  * 2x Gore ePTFE pressure equalization & acoustic vent membranes
* [ ] **Pre-Assembled Automotive Cable Harnesses (Two-Cable Architecture):**
  * **1x Cable 1 (Vehicle & CAN):** 6-Pin Deutsch DTM06-6S COTS pre-molded harness with Raychem DR-25 (KL30, KL15, GND, CAN_H, CAN_L, Shield) to internal Molex Micro-Lock Plus 6-Pin header `J1`.
  * **1x Cable 2 (OMB Periphery Bus):** 16-Pin Automotive COTS harness to internal Molex Picoflex 16-Pin header `J6` (4 branches: Front 60W, Pod 1 30W, Pod 2 30W, Rear Radar 12V).
  * **2x HytePro 4-Pin Magnetic Breakaway Couplings (IP67)** with 4-wire silicone ribbon cable ($V_{\text{BUS}}$, `GND`, `D+`, `D-`).
  * **1x 4-wire high-flex shielded automotive cable (AWG22/28)** for backbone pull (length approx. $1.5\,\text{m}$).
  * **1x Nylon Fish Tape (Ø 3 mm, 2 m length)** for routing through frame backbone.
* [ ] **Tools Required:**
  * Hex key set (1.5 / 2.0 / 2.5 / 3.0 / 4.0 mm), Torx TX10 / TX25, open-end wrenches 7 / 8 / 10 mm, utility knife, dielectric silicone grease.

---

## 3. Module Assembly (Step-by-Step)

### Step 1: Central Box (Main Box v10 Dual-Rail Monocoque) Assembly
1. **Insert Hex Nuts:** Press 4x DIN 934 M2.5/M3 stainless nuts into the captive hexagonal pockets on the underside of the monocoque tub ([`000_monocoque_tub.stl`](../../hardware/cad/stl/01_main_box/000_monocoque_tub.stl)).
2. **Install Main Board:**
   * Place the fully populated `PCBA 01` (with ESP32-S31-WROOM-1U, Microchip USB2517I Hub, 3x Qualcomm QCC3086, and Quad-eFuse) onto the integrated standoffs.
   * Secure board with 4x M2.5 $\times 6\,\text{mm}$ screws.
3. **Pre-Route Harnesses & Slide In Intermediate Tray (Rail 1 at $Z = 18.0\,\text{mm}$):**
   * Connect internal silicone wire harnesses from front bulkhead to vertical PCB headers on `PCBA 01`: Vehicle Power/CAN into `J1` (Molex Micro-Lock Plus 6P) and 4-channel periphery bus into `J6` (Molex Picoflex 16P). Pre-route UPS harness to `J5`/`J7`.
   * Connect U.FL coaxial cables for LoRa (`ANT1`, FXP895) and Wi-Fi (`FXP73`) antennas.
   * Slide the intermediate tray ([`010_slide_tray.stl`](../../hardware/cad/stl/01_main_box/010_slide_tray.stl)) horizontally from the rear into the lower C-groove rails (Rail 1). All wires pass smoothly through the front cable bay and drop slots into the upper chamber without pinching.
4. **Mount 2,200 mAh LiPo Battery & Flex Antennas on Intermediate Tray:**
   * Place the 2,200 mAh LiPo flat pack onto the $1.0\,\text{mm}$ EPDM foam mat in the molded battery cradle of the intermediate tray, secure with the elastic EPDM strap, and connect the battery plug.
   * Affix both flex antennas (Taoglas FXP895 LoRa and FXP73 2.4 GHz) into the recessed adhesive nests on top of the intermediate tray (`010_slide_tray.stl`).
5. **Slide In L-Slide Lid (Rail 2 at $Z = 33.0\,\text{mm}$, 100% Screw-Free):**
   * Lightly coat the silicone round cord (Ø 1.5 mm, $40\,\text{cm}$) with silicone grease and seat it in the perimeter sealing groove.
   * Slide the L-Slide Lid ([`020_slide_lid.stl`](../../hardware/cad/stl/01_main_box/020_slide_lid.stl)) from the rear into the upper C-groove rails (Rail 2) until the 15° front wedge nose seats and both Slam-to-Shut PA12 deadbolt latches on the integrated Heckwand click audibly into the lower rear sill. The lid is 100% cable-free and requires zero vertical screws.

---

### Step 2: Saddlebag Pods v10.0 Assembly (L-Slide Lid with Plastic Claws, Wall-Guided Actuator Struts & 30W In-Bag USB Charger)
1. **Understanding the v10.0 Pod Design (Zero Servos, 100% Reliable):**
   * The pod housing mounts securely inside the front corner of the hard saddlebag (or in the GSA Cage Dock / Transition Dock).
   * **L-Shaped Slide-in Lid (`021_pod_slide_lid.stl` / `013_pod_slide_lid.scad`) & Fixed $14.0\,\text{mm}$ Rear Wall:** The horizontal lid plate slides in the upper sidewall C-grooves (`Rail 2`, $Z = 32.0\dots 35.2\,\text{mm}$) and merges monolithically into the vertical upper rear wall (`Heckwand`). The lower rear wall of the monocoque tub (`002_pod_housing_base.stl`) is $14.0\,\text{mm}$ tall ($Z = 0\dots 14.0\,\text{mm}$), so the **optional SMA antenna bulkhead knockout ($Z = 7.5\,\text{mm}$, $Y = 35.0\,\text{mm}$) remains permanently fixed in the tub** and never moves when opening the lid.
   * **PA12 U-Yoke Latch with Downward-Gripping Plastic Claws ("Plastikkrallen", `016_fob_magnetic_lock_mechanism.scad`):** Housed inside the lid's rear wall is a non-metallic, spring-loaded PA12 U-yoke with a small N52 coin magnet ($\varnothing\,6 \times 2\,\text{mm}$). Two outer **PA12 plastic claws ("Plastikkrallen")** ($Y = 8.5\,\text{mm}$ and $Y = 55.5\,\text{mm}$) reach down from the lid's rear wall on either side of the central SMA arch and hook positively into the undercut pockets ($Z = 9.8\dots 14.2\,\text{mm}$) of the low fixed rear wall.
   * **FOB Proximity Unlocking:** To remove the intercom module, simply hold the magnetic OMB Smart Keyfob (`PCBA 07`) against the exterior rear-wall target. The magnetic field lifts the PA12 U-yoke and its plastic claws upward by $3.2\,\text{mm}$ out of the lower rear wall, allowing the L-lid to slide out smoothly.
   * **Seated TPU Dry-Flap Splash Shield (`011_pod_slide_tray.stl` / `014_pod_dry_flap.scad`):** In the forward electronics bay ($X = 8\dots 56\,\text{mm}$), the $48 \times 56\,\text{mm}$ TPU shield rests on the perimeter step shelf ($Z = 14.5\,\text{mm}$) over `PCBA 03`, leaving the upper sidewall C-grooves completely unobstructed.
   * **Chassis-Mounted Bulkhead Ports (Port A & Port B):** Both interfaces are horizontally centered ($Y = 35.0\,\text{mm}$) on the short front bulkhead end-wall and stacked vertically:
     * **Port A (top, $Z = 26.5\,\text{mm}$):** Weatherproof Bus socket (4-wire backbone `VCC_BUS`, `GND`, `USB_D+`, `USB_D-`), connected via a short internal 4-conductor silicone ribbon cable to header `J_BUS` on `PCBA 03`.
     * **Port B (bottom, $Z = 11.5\,\text{mm}$):** Weatherproof USB-C charging port (30W USB-PD), connected via an ultra-flexible 4-conductor internal silicone ribbon cable to header `J_USB_OUT` on `PCBA 03`.
2. **PCB, Wiring & Dry-Flap Installation:**
   * Secure `PCBA 03` ($42 \times 48\,\text{mm}$) onto the forward floor standoffs with 4x M2.5 screws ($36 \times 42\,\text{mm}$ hole pitch).
   * Connect the 4-conductor internal silicone ribbon cable from Port A (top, $Z = 26.5\,\text{mm}$) to `J_BUS` and from Port B (bottom, $Z = 11.5\,\text{mm}$) to `J_USB_OUT`.
   * Connect rearward equipment interfaces: Intercom OEM adapter harness to `J_AUDIO_PWR` (8-Pin JST-SH, top-right) and actuator harness to `J_ACT` (8-Pin JST-SH, bottom-right).
   * Seat the TPU dry-flap (`011_pod_slide_tray.stl`) onto the $Z = 14.5\,\text{mm}$ step shelf over `PCBA 03`, routing the cables cleanly through its rear pass-through slot.
3. **Equipping & Calibrating the Wall-Guided Actuator Cross-Struts (`Rail 1`):**
   * Insert the two mini-solenoids JF-0530B (with soft Shore A50 silicone caps) into the under-slung Z-carriages of the two independent cross-struts ([`012_universal_actuator_slide_bracket.stl`](../../hardware/cad/stl/02_pod_base/012_universal_actuator_slide_bracket.stl)).
   * **Crucial (100% Unobstructed Tub Floor):** The struts are **not** bolted to the tub floor; instead, they slide horizontally from the rear into the middle sidewall C-grooves (**`Rail 1` at $Z = 21.5\dots 24.5\,\text{mm}$**)! This keeps the entire tub floor 100% smooth and unobstructed for the OEM intercom cradle (Cardo Air-Mount, Sena clamp, or OMM).
   * Align the struts along X (in the sidewall C-groove), the carriages along Y ($Y = 16\dots 54\,\text{mm}$), and the plunger height along Z ($8\,\text{mm}$ vertical slot) directly above the headset buttons, then lock them using the **flush-countersunk `DIN 7991` M2.5 screws** into the captive `DIN 934` hex nuts (preserving over $8\,\text{mm}$ overhead clearance to the lid underside!).
   * Press the two **EPDM rubber sealing plugs** into the rear `Rail 1` entry slots to lock the struts axially and seal the rail openings.
   * **Function of the Mechatronic Cold-Start:** When switching ignition ON (KL15), the `AO3400A` MOSFETs on `PCBA 03` energize the solenoids automatically for 2.0 s, booting the powered-off headset hands-free.
4. **L-Slide-in Lid & Plastic-Claw Magnetic Latch Setup:**
   * Insert the PA12 U-yoke (`016_fob_magnetic_lock_mechanism.scad`) with its $\varnothing\,6 \times 2\,\text{mm}$ N52 coin magnet and dual return springs into the guide pocket inside the lid's rear wall so the two lower **PA12 plastic claws ("Plastikkrallen")** protrude downward.
   * Fit the silicone cord into the lid's perimeter groove. Slide the L-lid from the rear into the upper C-grooves (`Rail 2`): at full insertion, both **plastic claws** snap audibly downward into the fixed $14.0\,\text{mm}$ lower rear wall (Slam-to-Shut). Bringing the Smart Keyfob near the rear wall lifts the claws and releases the lid instantly.

---

### Step 3: Multi-Protocol Gateway Inlays Installation
1. **Sena SPIDER X Slim / 50S (Reference K2a):**
   * Connect the pre-wired adapter harness from `PCBA 03` (Audio In, Audio Out, PTT, 5V power).
   * Seat the Sena module into the form-fit PA12 cradle. Direct DC power is supplied by `PCBA 03`'s high-efficiency step-down regulator (no onboard intercom battery needed).
2. **Cardo Packtalk Edge / Pro (Class 1d DMC Gen2):**
   * Connect audio and charging pigtails to the Cardo Air-Mount harness.
   * Snap the Cardo unit into the Air-Mount cradle. Continuous charging during active mesh operation is supported with isolated `PGND` ground return.
3. **OpenMotorMesh (OMM) 2.4 GHz & 446 PMR Modules (Class 4 / 3b UCS):**
   * Connected directly via USB-C digital audio for bit-perfect transmission to `PCBA 03`.
4. **Midland PMR446 Analog Radios:**
   * Integrated via `PCBA 03`'s galvanic isolation transformers and optocoupler PTT keying.

---

### Step 4: Mount Front Node at Riser, Modular Sensor Puck & Symmetrical Dual Under-Perch Mirror Pods
1. **Front Node Riser Mounting & Modular Sensor Puck:**
   * The Front Node (`PCBA 05`) with **ESP32-S31-WROOM-1U + ESP32-E22** and integrated **60W USB-PD Engine** (TPS54302 + SW3526) is mounted in its compact Dual-Rail Monocoque enclosure (`001_front_node_monocoque_tub.stl`) directly onto the handlebar riser or upper triple tree clamp (using the included riser clamp).
   * **Modular Snap-On Environmental Sensor Puck ("Körbchen", `PCBA 05D`):** The hermetic sensor puck ([`sensor_puck_top.stl`](../../hardware/cad/stl/05_accessories/sensor_puck_top.stl) / [`sensor_puck_bottom.stl`](../../hardware/cad/stl/05_accessories/sensor_puck_bottom.stl)) snaps form-fittingly from above onto the Front Node. It contacts via `J1` (8-pin JST-GH) and houses the u-blox SAM-M10Q GNSS, TI TMP117 precision thermometer, TI OPT3001 ambient light sensor, and Bosch BMP390 altimeter (the Knowles MEMS microphone `MK1` sits in the Front Node floor). (In a car/van, the puck unclips with a single click and mounts via a 1.5 m extension lead in the windshield wedge dock!).
2. **Symmetrical Dual Under-Perch Mirror Pods Mounting (Left & Right, `PCBA 05C`):**
   * Loosen both mirror mounting bolts beneath the left and right handlebar perches.
   * Slide the ergonomic mirror pods ([`under_perch_mirror_pod.stl`](../../hardware/cad/stl/05_accessories/under_perch_mirror_pod.stl)) under the perch brackets and retorque mirror stems to $15\,\text{Nm}$.
   * **Symmetrical Ergonomics & Safety Advantage:**
     * **Left Pod:** Tactile PTT button sits right at the natural resting position of the left thumb (intercom comm & voice assistant); amber LED beams directly into left mirror (overtaking traffic on left).
     * **Right Pod:** Tactile Action-Cam button under right thumb instantly bookmarks/highlights video clips; amber LED beams into right mirror (traffic on right when merging back).
     * **Bilateral:** True 360° blind-spot alerting directly in the peripheral sightline of the exact mirror checked!
   * Route the two slim matte-black PUR cables along the OEM control harnesses down to the riser Front Node and plug into `J_POD_L` and `J_POD_R`.

---

## 4. Bench Testing, Flashing & Dry-Run Setup

> [!IMPORTANT]
> **Native USB-DFU, Central Bus-OTA & Bench Operation (`J3` 5V Service Input vs. `J1` 12V Full Load):**  
> OpenMotorBridge v10.0 eliminates external UART bridge dongles and avoids opening individual nodes for firmware flashing:  
> * **5V USB-C Service & Bench Input (`J3` with `LM66100` Ideal-Diode OR-ing):** On the workbench, the Central Box can be powered for initial setup, logic verification, LiPo charging (`BQ24075`), battery monitoring (`J5`), and **Central Bus-DFU of all nodes** directly from a standard **5V USB-C cable into `J3`** (PC/Mac USB port or 5V/3A USB-C adapter) – the `LM66100` ideal diode feeds `VCC_5V_MAIN` with zero reverse current into the 12V rail.
> * **12V Full-Load Bench Test (`J1` KL30/KL15):** For high-power testing of the 12V periphery smart switch (`TPS4H160-Q1` `U12`), the 60W/30W buck converters in the Front Node and Pods, and the cold-start solenoids, apply 12V DC to vehicle power header `J1`.
> * **Native USB-DFU & Bus Bootloader:** The **ESP32-S31** host enumerates over `J3` directly as `ESP32-S31 USB JTAG/serial debug unit` on your PC/Mac and flashes the Front Node (`PCBA 05`), both Saddlebag Pods (`PCBA 03`), and the Rear Radar (`PCBA 08`) automatically via the internal `USB2517I` hub and RS-485 bus bootloader.

```text
+-------------------------------------------------------------------------------------------------+
                      OPENMOTORBRIDGE v10.0 BENCH DRY-RUN SETUP
+-------------------------------------------------------------------------------------------------+
|                                                                                                 |
|   [ USB-C CHARGER (5V-20V PD) OR 12V DC BENCH POWER SUPPLY ]                                    |
|        |                                                                                        |
|        | USB-C PD Sink (5V-20V up to 60W) OR 12V DTM-6 Cable 1 (Dual Ideal-Diode OR-ing)        |
|        v                                                                                        |
|   +---------------+   Cable 2 Branch 1: 4-Wire (60W PD / USB 2.0)   +---------------+          |
|   |  CENTRAL BOX  |================================================>|  FRONT NODE   |          |
|   |  (PCBA 01)    |   (VBUS, GND, D+, D-)                            |  (PCBA 05)    |          |
|   |  ESP32-S31    |                                                  +-------+-------+          |
|   |  3x QCC3086   |                                                          |                  |
|   |  4-Branch Bus |                                                          v                  |
|   +-------+-------+                                             +-------------------------+     |
|           |                                                     | 2x SYMMETRICAL MIRROR   |     |
|           | Cable 2: 16-Pin Automotive Header                   | PODS (Left PTT /        |     |
|           |                                                     | Right Cam-Tag & BSD)    |     |
|           +-------------------------------+                     +-------------------------+     |
|           | Branch 2 (30W PD)             | Branch 3 (30W PD)                                   |
|           v                               v                                                     |
|   +---------------+               +---------------+                                             |
|   | SADDLEBAG POD1| (Left)        | SADDLEBAG POD2| (Right)                                     |
|   | PCBA 03 Smart |               | PCBA 03 Smart |                                             |
|   | 2x Solenoids  |               | 2x Solenoids  |                                             |
|   | 30W In-Bag USB|               | 30W In-Bag USB|                                             |
|   +---------------+               +---------------+                                             |
|                                                                                                 |
|   USB-C DFU Port on PCBA 01                                                                     |
|        |                                                                                        |
|        v Standard USB-C Cable (WebSerial / DFU)                                                 |
|   [ LAPTOP / WORKBENCH RUNNING OMB PWA ]                                                        |
|                                                                                                 |
+-------------------------------------------------------------------------------------------------+
```

### Guided 4-Point v10.0 Smoke Test
1. [x] **Power Supply, UPS & USB-PD (Check 1):** Connect Central Box via USB-C charger (or 12V bench supply). Internal 5.0 V and 3.3 V rails stable; UPS LiPo (2,200 mAh) charges at 4.18 V. USB-PD power negotiation powers all branches cleanly (60W Front Node, 30W each Pod).
2. [x] **Saddlebag Pods, Mechatronics & Intercom (Check 2):** Both pods enumerate over the USB 2.0 bus without errors. When switching KL15 ignition ON, both mini-solenoids on the slide rail pull in synchronously for exactly 2.0 s (cold-start pulse). Intercom audio routing (Sena/Cardo/OMM) is verified; PTT keying triggers instantly. The integrated 30W saddlebag USB charging port provides full PD charging power.
3. [x] **Front Node & Cockpit Controls (Check 3):** SAM-M10Q in the sensor puck acquires 3D GNSS lock, TMP117 reads ambient temp, Knowles MEMS registers audio transients. Pressing left Under-Perch PTT button switches intercom transmit and lights left amber LED; pressing right Action-Cam button bookmarks a highlight tag and lights right amber LED.
4. [x] **LoRa Emergency Radio & 77 GHz Rear Radar (Check 4):** SX1262 LoRa 868 MHz ping-echo succeeds; Wheeltec MR20 radar reports simulated vehicle approach and triggers the 36 rear strobe LEDs.

---

## 5. Vehicle-Specific Installation & Routing

### 5.1 Harley-Davidson Bagger Platform Installation (FL Touring: Street Glide, Road Glide, CVO, CVO ST, Road King Special RKS)

> [!NOTE]
> **HARLEY-DAVIDSON TOURING PLATFORM UNIFICATION:**  
> All FL Touring baggers share the same hard saddlebags, the same OEM Ø 19 mm saddlebag wall pass-through ([`010_saddlebag_hole_grommet_split.scad`](../../hardware/cad/scad/02_pod_base/parts/010_saddlebag_hole_grommet_split.scad)), the same under-seat Central Box mounting location, and the same open frame backbone wire caddy:  
> * **Faired Baggers (Road Glide / Street Glide / CVO / CVO ST):** Utilize Sharknose or Batwing fairings with symmetrical Rockford Fosgate speaker corner display pods ([`cockpit_speaker_corner_pod.scad`](../../hardware/cad/scad/04_front_node/cockpit_speaker_corner_pod.scad)) and the 5-Port Glove Box Media & Power-Injection Hub in the right media compartment.  
> * **Unfaired Baggers (Road King Special RKS):** Smartphone/Garmin mounts directly on the handlebar; the Front Node is installed in "Front-to-Back Flip" protected under the headlight nacelle (no glove box hub).

> [!CAUTION]
> **WARRANTY & FINISH INTEGRITY: THE THREE GOLDEN BAGGER RULES:**  
> 1. **ZERO OUTER FAIRING REMOVAL (Never remove the outer fairing shell!):**  
>    The speaker grilles and vent diverters feature delicate, high-tension retention clips. **The outer fairing remains 100% untouched throughout the entire OMB installation!**  
> 2. **ZERO FUEL TANK LIFTING (Never unbolt or raise the fuel tank!):**  
>    The Harley-Davidson Touring frame features an open plastic wire caddy running along the top of the backbone frame tube, accessible directly from beneath the rider seat tongue. Using a flexible nylon fish tape, the 4-wire harness is pulled through in 5 minutes without removing or loosening screws on the fuel tank!  
> 3. **HERMETIC GLOVE BOX INTEGRITY (Never pinch cables across door weatherstripping!):**  
>    The right glove compartment is accessed solely from *below* through the factory rubber grommet. The door perimeter seal remains 100% intact and weatherproof.

#### Step 5.1.1: Mount Central Box Under the Seat
1. Remove rider seat (remove rear thumb screw, slide seat rearward).
2. Position Central Box on the frame cross-bridge directly in front of/above the main battery.
3. Secure using 4x M4 vibration bobbins or high-strength 3M Dual-Lock pads.
4. **Connect Two-Cable Architecture:**
   * **Cable 1 (Deutsch DTM-6 `J1`):** Connect positive lead (with 7.5A COTS blade fuse) to Terminal 30 (constant battery) or Terminal 15 (switched ignition on OEM diagnostic connector); bolt ground lead to central chassis ground stud; route CAN bus (Pins 4/5) to vehicle net CAN.
   * **Cable 2 (16-Pin Automotive `J_PERIPH`):** Lock connector and route the 4 branches to their respective locations (Branch 1 Front Node, Branch 2 Pod 1, Branch 3 Pod 2, Branch 4 Radar).

#### Step 5.1.2: 5-Minute Backbone Cable Pull (Zero Tank Removal)
1. Locate the front seat-tongue receiver bracket on the backbone tunnel. The open factory plastic wire caddy begins directly beneath this point.
2. Carefully feed a 3 mm nylon fish tape into the caddy from the seat area, pushing forward until the tip exits near the steering neck.
3. Tape the 4-wire shielded automotive cable (AWG22/28, Branch 1) to the fish tape tip with friction tape.
4. Pull the fish tape through. The cable is now routed inside the original factory channel—completely concealed and protected from engine heat.
5. Connect the rear cable end into the 16-pin periphery harness; route the front end to the upper triple tree clamp.

#### Step 5.1.3: Front Node & Symmetrical Dual Under-Perch Mirror Pods
1. **Front Node:** Secure with the handlebar clamp onto the riser or top triple tree (for RKS: under the nacelle). Connect the 4-wire cable (60W) emerging from the backbone.
2. **Symmetrical Under-Perch Mirror Pods (Left & Right):**
   * Loosen both mirror retaining nuts beneath the left and right perches.
   * Slip both identical pods over the mirror stems and retorque each nut to $15\,\text{Nm}$.
   * Route the two slim 3-wire leads along the handlebar wiring down to the Front Node and plug into `J_POD_L` and `J_POD_R`.
   * **Result:** Symmetrical cockpit aesthetics, left thumb operates PTT, right thumb bookmarks action-cam highlights, bilateral amber radar alerts reflected directly on both mirrors!
3. **Direct Cockpit Peripherals (Navi & Action-Cam Power Supply):**
   * **Dedicated Motorcycle GPS (15W at `J10`):** Connect Garmin Zūmo XT2 / Tread / Chigee AIO-5 using the 2-pin DC lead from `J10`.
   * **Action-Cam (10W at `J8`):** Route the weather-sealed USB-C lead directly from `J8` on the Front Node to the camera at handlebars or windshield mount.
   > [!IMPORTANT]
   > **USB DATA LINE ISOLATION FOR NAVI & ACTION-CAM (POWER-ONLY / BC 1.2 DCP):**  
   > Both cockpit feeds are **strictly Power-Only**! They have zero data connection to the `USB2514B` host hub. On the action-cam connector, data pins `D+` and `D-` are shorted per **USB BC 1.2 DCP** ($R < 200\,\Omega$). This ensures the GPS and action-cam recognize a dedicated vehicle charger, boot up immediately into active navigation or loop recording upon ignition ON, and **never** stall in a PC mass storage or webcam dialog! Direct Front Node connection also eliminates running camera cables through the glove compartment.

#### Step 5.1.3b: Symmetrical Cockpit Displays (Dual Speaker Corner-Pods)
1. **Ergonomic Principle (Bagger & Touring):**
   * The rider's smartphone charges safely and weather-protected in the right glove box (Media Compartment) via USB-PD.
   * For critical glanceable telemetry, two compact miniature displays are symmetrically positioned in the rider's primary line of sight.
2. **Mounting on Rockford Fosgate Stage II Speakers:**
   * Both display pods ([`cockpit_speaker_corner_pod.scad`](../../hardware/cad/scad/04_front_node/cockpit_speaker_corner_pod.scad)) clip form-fittingly onto the **lower inner corners** of the speaker grilles flanking the 12.3" Skyline OS display.
   * **Brand Preservation & Clean Aesthetics:** The upper Rockford Fosgate emblems and the Harley-Davidson Bar & Shield badge remain 100% visible and untouched. The handlebar riser plate with its machined "CVO ST" badge remains completely unobstructed.
3. **Invisible Cable Routing (Zero Fairing Disassembly):**
   * The cable drops directly into the natural shadow seam at the bottom inner edge of the speaker surround and routes concealed downward into the steering head / triple tree area to the Front Node (`PCBA 05`).
   * **0 cm visible cable, 0 screws removed from the outer fairing!**
4. **Functionality:** Driven locally by the ESP32-S3 on `PCBA 05` via SPI/QSPI (left: rear radar proximity bar & blind spot warnings; right: turn-by-turn navigation arrows, TPMS pressures, intercom channel/talking state, and smartphone charge status).

#### Step 5.1.4: Glovebox Fast-Charging Bay with Qi Puck & USB-C (Harley Touring)
1. Open the right glove box.
2. Locate the OEM rubber grommet on the underside of the compartment floor for accessory wiring.
3. Route the pre-regulated charging line from the Front Node (`PCBA 05` `J4`, SW3526 30W USB-PD / 5V BC1.2 Dual-Mode) up into the compartment (or up to the handlebar/QuadLock on adventure bikes).
4. Connect the modular charging cable as needed:
   * **Mode A (Wireless Qi Charging):** Connect the USB-C cable to the flat COTS Qi/MagSafe puck (in the glovebox) or the waterproof QuadLock Wireless Charging Head (on the handlebar).
   * **Mode B (Direct Cable Charging):** For accessories without Qi (helmet lamps, remotes, powerbanks) or when maximum charging speed without thermal throttling is required, plug the cable directly into the mobile device. The SW3526 automatically detects whether USB-PD is negotiated or falls back to standard 5V BC1.2.
   * *(Note: The legacy 5-port hub `PCBA 05B` and external CarPlay dongles have been eliminated; motorcycle navigation audio links wirelessly via the FSC-BT802 headunit bridge on the Front Node).*
5. All connected devices and cabling remain 100% inside the compartment. Zero external cable egress! The glove box door seals airtight with zero cable interference across weatherstripping!

#### Step 5.1.5: Saddlebag Pods & 100% Zero-Drill Feedthrough (OEM Ø 19 mm)
1. **Magnetic Breakaway Coupling at Frame Spar:**
   * Secure the 2-pin/4-pin HytePro magnetic pogo socket (`cots_pogo_magnetic_2pin`, IP68) with clamp to the rear subframe tube under the seat overhang.
2. **100% Zero-Drill Saddlebag Feedthrough (OEM Ø 19.0 mm Bore):**
   * **Zero Drilling in Saddlebags:** Neither the bag floor nor the side walls are drilled (strictly taboo on CVO ST).
   * Unscrew the forward OEM saddlebag lever knob and washer, and push out the factory rubber isolator grommet into the bag. The bare ABS pass-through hole measures **$\varnothing 19.0\,\text{mm}$**.
   * **Tool-Free Pre-Assembled Connector Passage:** The factory-terminated OMB cable harness complete with plug (USB-C / JST-GH, outer dimensions max. $\approx 12 \times 7\,\text{mm}$) slides effortlessly through the bare $\varnothing 19\,\text{mm}$ bore into the bag (zero de-pinning, zero cutting, zero soldering!).
   * **Install Split TPU Grommet:** Place the two-piece EPDM/TPU grommet ([`010_saddlebag_hole_grommet_split.scad`](../../hardware/cad/scad/02_pod_base/parts/010_saddlebag_hole_grommet_split.scad), Half A & B) around the cable and OEM M8 steel sleeve, and press-fit into the $\varnothing 19\,\text{mm}$ bore (IP67).
   * **Slide On U-Slotted Tunnel-Spacer Ring:** Slide the C-slotted 4 mm PA12-CF/Alu spacer ring laterally over the cable beneath the OEM $\varnothing 25\,\text{mm}$ steel washer.
   * **Torque OEM Lever Knob:** Thread in the OEM lever knob. The $\varnothing 25\,\text{mm}$ OEM washer seats flush against the spacer ring; 100% of the axial clamping force transfers into the steel sleeve. The cable exits completely uncompressed through the 4 mm tunnel along the inner wall. The lever knob retains full 360° rotation above the cable exit!
3. **Install Pod in Bag:**
   * Fasten the pod body inside the bag (preferably on the lid via [`saddlebag_lid_dock.scad`](../../hardware/cad/scad/02_pod_base/saddlebag_lid_dock.scad) onto the hinge bolts).
   * Connect the 4-wire harness to `PCBA 03`.
   * Insert intercom module and slide the lid in until it locks magnetically.
4. **Day-to-Day Operation (100% Breakaway):** When removing saddlebags (e.g. for hotel stops, tire changes, washing), **simply loosen both OEM lever knobs** and lift off the bag. The external magnetic coupler on the frame disconnects cleanly at $10\dots 15\,\text{N}$ axial tension ("MagSafe principle"). No internal connectors are touched! When remounting, the coupling snaps back together self-centering.

#### Step 5.1.6: 77 GHz Rear Radar at License Plate Bracket (Two-Tier Mounting)
1. **Mount Swivel Cradle:** Insert the 3D printed cradle ([`radar_swivel_tilt_cradle.stl`](../../hardware/cad/stl/02_pod_base/radar_swivel_tilt_cradle.stl)) with its 36-tooth Hirth index tongue into the clevis fork of the license plate bracket ([`radar_license_plate_bracket.stl`](../../hardware/cad/stl/02_pod_base/radar_license_plate_bracket.stl)). Insert the DIN 912 M5 $\times$ 25 mm screw and loosely thread on the DIN 934 M5 nut.
2. **Insert EPDM Vibration Damping Pad:** Place the **$58 \times 40 \times 2.0\,\text{mm}$ elastomer damping pad** ([`radar_vibration_damping_pad.stl`](../../hardware/cad/stl/02_pod_base/radar_vibration_damping_pad.stl), Shore 60A/70A EPDM or TPU 85A) onto the front mating face of the cradle plate, ensuring the M4 bores and Ø 34 mm Garmin well line up cleanly.
3. **Bolt Radar 2.0 Enclosure (Vibration Isolation):** Place the sealed radar enclosure against the damping pad. From the rear of the cradle, thread two **DIN 912 M4 $\times$ 14 mm screws** (with EPDM damping washers under screw heads) through the plate and pad directly into the captive M4 nuts of the enclosure backwall.  
   > [!IMPORTANT]
   > **Torque Warning:** Tighten M4 screws hand-snug to approximately **$1.0\dots 1.2\,\text{Nm}$**. The elastomer pad must be resiliently compressed, not crushed solid, in order to isolate high-frequency engine harmonics ($50\dots 250\,\text{Hz}$) from reaching the 77-GHz MR20 antenna array!
4. **Calibrate Pitch & Lock Hirth Rosette:** Settle the motorcycle with rider weight on a flat floor. Level the radar unit horizontally ($\pm 2^\circ$ to road surface). Firmly tighten the **M5 pivot bolt to approx. $4.0\,\text{Nm}$**: the 36-tooth Hirth rosettes interlock positively, preventing any pitch deflection under aerodynamic drag ($130+\,\text{km/h}$) or bumpy road rebound.
5. **Cabling & Drip Loop:** Route the 4-wire lead from Branch 4 down along the rear frame. Form a **$30\,\text{mm}$ radius drip loop** before entering the M8 cable gland so road spray drips free by gravity. Secure the cable with a UV-resistant zip-tie to the saddle at the bottom of the cradle.
6. **Roost Deflector Verification:** Confirm that the integrated monolithic roost deflector stands flush in front of the cable gland to physically deflect roost and gravel kicked up by the spinning rear tire.

---

### 5.2 Adventure Platform Installation (BMW R 1200 / 1250 / 1300 GS & GSA)

> [!IMPORTANT]
> **CABLE ROUTING ON GS/GSA (The Physical Reality vs. Harley):**  
> The v10.0 bus architecture (4-wire Automotive USB-PD) functions just as reliably on an adventure bike as on a Harley-Davidson. **However, the cable routing physical reality is fundamentally different:**  
> While the Harley Touring frame features an open, straight backbone tube (allowing a cable to be pulled through in 5 minutes via nylon fish tape), the BMW GS features a voluminous 20-liter (or 30-liter on GSA) tank, nested plastic fairing panels, and above all the **BMW Telelever front suspension (A-arm / trailing link)**:  
> * **Warning against Blind Pulling:** A cable pulled through blindly or left loose risks snagging in the moving Telelever swingarm triangle during heavy braking compression, or snapping under tension at full steering lock!  
> * **Proper Workshop Routing (approx. 20–25 minutes):**  
>   1. Loosen 3–4 screws (Torx T25) on the left or right upper tank side panel and lift it slightly.  
>   2. Route the 4-wire shielded automotive cable (`VBUS`, `GND`, `D+`, `D-`) from the Central Box (under the seat) along the upper frame tubes parallel to the factory BMW main wiring harness, securing loosely with UV-rated zip-ties.  
>   3. **The Telelever Steering Neck Arc:** At the steering head, the cable must **strictly follow the natural curvature of the OEM brake lines and factory harness**! Ensure a generous flex loop of approx. 50 mm. Before tightening zip-ties, cycle the handlebars lock-to-lock and compress the front suspension deeply: ensure zero binding, zero tension, and zero chafing against sharp casting edges in any position.  
>   4. Guide the forward cable end to the Ø 12 mm nav crossbar above the TFT and plug into the Front Node.

* **Central Box & 12V Vehicle Power (100% Under the Rider Seat!):**
  * Mount on 4x M4 vibration bobbins in the frame triangle or tool well under the rider seat.
  * **Cable 1 (Deutsch DTM-6 `J1`):** Connects directly inside the under-seat battery compartment:
    * **Constant Battery Power (KL30) & Ground (GND):** Short $< 15\,\text{cm}$ lead with included 7.5A COTS blade fuse directly to battery positive terminal (or jump-start post) and chassis ground stud.
    * **Switched Ignition (KL15) & K-CAN Bus:** Tapped right next to the battery via the factory BMW 16-pin OBD-2 diagnostic connector (Pin 1/16 switched power, Pin 6/14 K-CAN High/Low) or the OEM under-seat 12V auxiliary DIN socket (DIN ISO 4165, ZFE/BCO 60s shutdown).
  > [!CAUTION]
  > **Never Route a Power Cable from the Steering Head Back to the Seat!**  
  > The factory 3-pin Cartool accessory plug at the steering head remains **completely untouched** for the OMB system installation (retained as factory spare for third-party accessories)! No power cable is ever routed backwards from the front handlebar down under the seat. The Central Box powers the entire system directly from the under-seat battery/vehicle net and feeds the Front Node forward via the shielded 4-wire automotive harness (Cable 2, Branch 1) with up to 60W USB-PD.
* **Front Node:** Clamp directly to the Ø 12 mm GPS bar above the 6.5" TFT display with the 2-piece bar clamp. Powered entirely over Branch 1 of the 4-wire bus from the Central Box; delivers cold-air sensing, uncompromised GNSS reception, and 60W USB-PD charging power for smartphones and motorcycle navigation devices (Garmin Zūmo XT2 / Tread / Chigee AIO-5 / Carpuride).
* **All-in-One Under-Perch Mirror Pod:** Mount under the left mirror perch bracket (thumb PTT + directed amber BSD radar alert LED).
* **Pods:** Mount **strictly vehicle-fixed** on the motorcycle – either on the tubular pannier rack via the rugged [GSA Cage Dock](../../hardware/cad/scad/02_pod_base/adventure_gsa_cage_dock.scad) in the 45 mm dead space between pannier and rear wheel well, or along the seat crease via the [Transition Dock](../../hardware/cad/scad/02_pod_base/adventure_transition_dock.scad). *(Important: Never mount pods inside aluminum cases, as aluminum blocks 2.4 GHz RF like a Faraday cage!).*
* **Rear Radar:** Clamp via the minimal [Adventure Rack Radar Mount](../../hardware/cad/scad/02_pod_base/adventure_rack_radar_mount.scad) directly to the rear Ø 18 mm tube of the luggage rack. The $45^\circ$ roost deflector shields against gravel from knobby tires; topcases remain 100% accessible and quick-detachable.

---

### 5.3 Support Vehicle & Chase Car Setup (Support Van / Team Car / RV)

> [!TIP]
> **THE v10.0 SUPPORT CAR REVOLUTION: CENTRAL BOX & FRONT NODE REUNITED!**  
> In earlier generations (v8.0/v9.0), the Central Box and Front Node had to be placed in separate locations inside the vehicle (driver seat vs. passenger seat) to prevent extreme near-field RF coupling and de-sensing between the two 6.5 GHz UWB antennas.  
> **With UWB completely eliminated in v10.0, zero RF conflict exists:**  
> In the support vehicle, the **Central Box (`PCBA 01`) and Front Node (`PCBA 05`) are now co-located into a single, compact "All-in-One Car Support Core Unit"** (either stacked, docked via dovetail joints, or mounted side-by-side)!

```
                v10.0 ALL-IN-ONE CAR SUPPORT TOPOLOGY (10-MINUTE SETUP)
+-----------------------------------------------------------------------------------------+
| WINDSHIELD / A-PILLAR:                         SUN VISORS:                              |
| [ SAM-M10Q GNSS Puck at Windshield Base ]      [ Pod 1 (Driver) & Pod 2 (Passenger) ]   |
| (Positioned in unshielded toll-tag window)     (2.4 GHz radiates freely through glass)  |
+-----------------------------------------------------------------------------------------+
       ^                                                        ^
       | Thin I2C Sensor Cable                                  | 2x 4-Wire USB-PD Leads
+---------------------------------------------------------------+-------------------------+
| CENTRAL "CAR SUPPORT CORE UNIT" (Compact under passenger seat or center console):        |
| +------------------------------------+     +------------------------------------------+ |
| |        FRONT NODE (PCBA 05)        |<===>|           CENTRAL BOX (PCBA 01)          | |
| | * 4-Port USB Hub for Infotainment  | 10cm| * ESP32-S31 AI Host & 3x QCC3086 Audio   | |
| | * 20W USB-PD Charge Bypass Ottocast| Bus | * SX1262 LoRa Emergency & Theft Sentry  | |
| +------------------------------------+     +--------------------+---------------------+ |
+-----------------------------------------------------------------|-----------------------+
       |                                                          |
       | USB Cable & PTT                                          | Coaxial Cable (RG-174)
       v                                                          v
+--------------------------------------+      +-------------------------------------------+
| CENTER CONSOLE (Controls):           |      | EXTERNAL 868 MHz MAGNETIC ROOF ANTENNA:   |
| * OEM Media-USB (Data-only D+/D-)    |      | * Scratch-free magnetic mount on roof     |
| * AAWireless/Ottocast to OMB (5V/3A) |      | * Vehicle roof ground plane delivers      |
| * PTT button at gear shift / handbrak|      |   15–25 km real-world LoRa range to group |
+--------------------------------------+      +-------------------------------------------+
```

1. **Core Unit Placement:**
   * Central Box and Front Node co-locate as a unified unit in the cool passenger footwell or inside the center console tunnel.
   * **Single-Cable Power Supply:** A single 12V automotive power lead runs to the 12V auxiliary/cigarette lighter socket – eliminating all messy Y-cable splitters running between seats!
2. **Radial Cable Exits from Core Unit:**
   * **Up to the Roof:** A $2.5\,\text{m}$ thin RG-174 coaxial cable runs beneath the carpet through the rear hatch weatherstrip to the external $\varnothing 30\,\text{mm}$ magnetic roof antenna. Delivers $15\dots 25\,\text{km}$ LoRa range to the motorcycle group, overcoming metal car body shielding.
   * **To Windshield Base:** A thin 4-conductor lead routes to the SAM-M10Q GNSS puck at the windshield base (in the athermic glass cutout window).
   * **To Sun Visors:** Two 4-wire ribbon cables route along A-pillar door seals to Pod 1 (Driver: Sena/OMM) and Pod 2 (Passenger: Cardo/Midland).
   * **To Center Console (AAWireless Clean Power Injection):**
     * The AAWireless or Ottocast adapter plugs directly into OMB's dedicated $5\,\text{V}\,/\,3\,\text{A}$ ($15\,\text{W}$) USB port.
     * A pure high-speed data cable (`D+`, `D-`, `GND` with isolated `VBUS`) connects into the car's OEM Media USB socket.
     * **Result:** The car head unit receives stable Android Auto / Apple CarPlay without the endless bootloop cycles caused by weak OEM $500\,\text{mA}$ vehicle USB sockets!
     * The PTT switch secures with Velcro to the gear shift lever or handbrake.
3. **Rental Car & Rally Readiness:** The entire setup installs in less than 10 minutes in any support van or chase car, and uninstalls cleanly with zero vehicle modifications.

---

## 6. Final Inspection, Road Test & Sign-Off Checklist

1. **Ignition Check (KL15):**
   * Turn Ignition ON: Central Box and Front Node wake synchronously in $< 500\,\text{ms}$.
   * USB-PD power rails stable; green status LED on `PCBA 01` shines solid.
   * Mirror BSD LED performs a 1.0 s amber self-test flash.
2. **Saddlebag Pods & Charging Verification:**
   * Unlock slide-in lid with Smart Keyfob: smooth latch retraction and release.
   * Plug phone / action cam into saddlebag USB port: rapid PD charging confirmed.
   * Intercom audio test: crystal-clear audio transfer with zero hum or ground loops.
3. **Blind-Spot Radar Test:**
   * Assistant walks toward rear of stationary motorcycle: Amber LED on left mirror perch illuminates steadily at 25 m.
   * Activate left turn signal with target in blind spot: Mirror LED pulses rapidly at 8 Hz red/amber; rear radar LEDs strobe alert to trailing traffic.
4. **Infotainment & Head Unit (CVO Road Glide ST):**
   * 12.3" Skyline OS display connects wirelessly to Apple CarPlay / Android Auto within 15 seconds.
   * Pressing the Under-Perch PTT button activates Siri / Google Assistant voice recognition instantly.
5. **Road Test & Dynamics:**
   * Knowles wind noise sensor smoothly modulates helmet volume with road speed.
   * Raised-Cosine ducking attenuates media audio softly by $-18\,\text{dB}$ during incoming radio calls.
6. **Ignition OFF:**
   * Turn Ignition OFF: Central Box logs graceful shutdown to flash memory.
   * LoRa 868 MHz theft sentry remains active 24/7 in ultra-low-power mode.
