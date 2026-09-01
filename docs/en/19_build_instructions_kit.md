# 19 - Build Instructions & Kit Bill of Materials (BOM)

This document is the complete, practical step-by-step assembly guide and hardware kit bill of materials for building a complete **OpenMotorBridge (v8.0)** motorcycle communication and telemetry system from scratch. It provides an exact parts list for 3D printed parts, assembled circuit boards (PCBAs), mechanical fasteners, IP67 seals, wiring harness components, and commissioning protocols.

---

## 1. System Kit Overview (What are you building?)

A complete OpenMotorBridge vehicle installation consists of the following assemblies:

```
                      ┌─────────────────────────────────────────┐
                      │    1x CENTRAL MAIN BOX (IP67)           │
                      │    (Under seat / in rear tail compartment│
                      │    • Lower tub + Mid tray + Lid         │
                      │    • Main PCB (ESP32-S3, Codec, UPS)    │
                      │    • Integrated LiPo Backup Battery     │
                      └────────────────────┬────────────────────┘
                                           │
                        1x CENTRAL WIRING HARNESS (HD26 IP67)
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         │                                 │                                 │
         ▼                                 ▼                                 ▼
┌──────────────────┐             ┌──────────────────┐              ┌──────────────────┐
│ 1x POD 1 (LEFT)  │             │ 1x POD 2 (RIGHT) │              │ 1x POD 3 (REAR)  │
│ (Handlebar mount)│             │ (Handlebar mount)│              │ (License plate/tail)
│ • Pod housing    │             │ • Pod housing    │              │ • Pod housing    │
│ • Base PCBA      │             │ • Base PCBA      │              │ • Base PCBA      │
│ • CARTRIDGE 1    │             │ • CARTRIDGE 2    │              │ • CARTRIDGE 3    │
│   (e.g., Sena/   │             │   (e.g., Cardo/  │              │   (OMM Long-Range│
│    Cardo)        │             │    Blank dummy)  │              │    Mesh + GNSS)  │
└──────────────────┘             └──────────────────┘              └──────────────────┘
```

---

## 2. Complete Parts List (BOM for 1 Motorcycle Kit)

### 2.1 Category A: 3D Printed Parts & Manufacturing Options (FDM vs. MJF)

All enclosures and cartridges are designed to be manufactured **both on standard desktop FDM printers (Bambu Lab, Prusa, Voron, Creality) and via industrial powder-bed service providers (HP MJF / SLS)**.

#### Option 1: Desktop FDM Printing (Bambu Lab X1/P1/A1, Prusa MK3/MK4/XL, etc.)
* **Recommended Filaments for Motorcycle & Outdoor Use:**
  * **PETG:** *Ideal for open-frame printers without enclosure.* UV-resistant, fuel/oil resistant, impact tough up to $80\,^\circ\text{C}$ continuous temperature.
  * **ASA (or ABS):** *Best choice for enclosed printers (e.g., Bambu X1/P1, Prusa Enclosure).* $100\,\%$ UV & weather resistant, heat resistant up to $100\,^\circ\text{C}$.
  * **PA-CF / PET-CF (e.g., Bambu PAHT-CF, Prusament PA11-CF):** Outstanding rigidity, production-grade matte carbon finish.
  * ❌ *Important:* **Do not use standard PLA**, as PLA softens and warps in direct sunlight on a motorcycle above $55\,^\circ\text{C}$!
* **Optimal Slicer Settings for IP67 Water Resistance & Durability:**
  * **Wall Perimeters:** Set to **4 to 5 perimeters** (wall thickness $\approx 1.6 \dots 2.0\,\text{mm}$ $\rightarrow$ walls print $100\,\%$ solid with zero voids).
  * **Top/Bottom Solid Layers:** **5 to 6 layers**.
  * **Infill:** $25 \dots 40\,\%$ (Gyroid or Honeycomb).
  * **Layer Height:** $0.16\,\text{mm}$ (recommended for clean O-ring grooves) or $0.20\,\text{mm}$.
  * **Flow Rate:** $102 \dots 104\,\%$ (slight extrusion overlap permanently seals micro-voids between layer lines).
  * **Print Orientation & Support Strategy:**
    * `main_box_lower_case.stl`: Flat on bottom base $\rightarrow$ **$0\,\%$ support required**.
    * `main_box_mid_tray.stl`: Flat on partition floor $\rightarrow$ enable Tree Support under perimeter sealing lip.
    * `main_box_lid.stl`: Flat on top face on print bed $\rightarrow$ **$0\,\%$ support required**.
    * `pod_base_housing.stl`: Standing upright on rear M8 gland face $\rightarrow$ minimal Tree Support under V-saddle.
    * `cartridge_*_sled.stl`: Flat on sled floor $\rightarrow$ snap-fit cantilever arms lay in the $XY$ plane (optimal continuous filament grain direction for maximum flex endurance!).

#### Option 2: Industrial 3D Printing (JLCPCB 3D Print, Weerg, Craftcloud, Shapeways)
* **Process:** **HP Multi Jet Fusion (MJF)** or **SLS** (Selective Laser Sintering).
* **Material:** **PA12 (Polyamide 12)**, black dyed and glass-bead blasted.
* **Advantage:** Isotropic mechanical strength across all 3 axes, 100% leak-proof, zero support artifacts.
* **Pre-packaged ZIP files for service providers:** [`hardware/production_packages/06_3d_print_mjf_stls/`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/06_3d_print_mjf_stls).

#### 3D Printed Parts Bill of Materials:

#### Bill of Materials: 3D Printed Parts

| Assembly | Filename / STL | Qty | Function & Description |
| :--- | :--- | :---: | :--- |
| **Main Box Lower Tub** | [`main_box_lower_case.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lower_case.stl) | **1** | Monocoque base with 4x M4 silentblock ears, 4x PCB standoffs & O-ring groove |
| **Main Box Mid Tray** | [`main_box_mid_tray.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_mid_tray.stl) | **1** | Battery cradle, 10x convective vent slots, HD26/USB-C/LED cutouts & sealing lip |
| **Main Box Top Lid** | [`main_box_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lid.stl) | **1** | Top closure lid with Gore ePTFE vent boss & 4x M3 corner screw counterbores |
| **Pod Base Housing** | [`pod_base_housing.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod_base_housing.stl) | **3** | Universal bay for Pod 1, 2, and 3 with V-tube saddle, 4x EPDM strap hooks & M8 neck |
| **Universal Base Sled** | [`cartridge_base_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl) | **2** | Base chassis for Pods 1 & 2 with $360^\circ$ seal seat, guide rails, latch arms & M2 bosses |
| **Sena Adapter Insert** | [`cartridge_insert_sena.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) | **1** | Modular top cradle for Sena 50S/60S, pogo array pocket (fastened with 4x M2 screws) |
| **Cardo Adapter Insert** | [`cartridge_insert_cardo.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl) | *(opt)* | Modular top cradle for Cardo AirMount with magnet pockets (alternative to Sena) |
| **Waterproof Blank Cover** | [`cartridge_insert_blindkassette.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_blindkassette.stl) | **1** | Hermetic IP67 solid cover for unused Pod 2 slot (fastened with 4x M2 screws) |
| **OMM Rear Cartridge** | [`cartridge_omm_transceiver_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_omm_transceiver_sled.stl) | **1** | Monocoque sled for Pod 3 (directly houses $70 \times 48\,\text{mm}$ Rear Pod 3 PCBA) |
| **Total 3D Printed Parts** | | **9** | **Pre-packaged in 3D Print ZIP archives in `hardware/production_packages/`** |

---

### 2.2 Category B: Assembled Circuit Boards (PCBAs from JLCPCB / Eurocircuits)
*All production files (Gerber ZIP, CPL Pick & Place, BOM CSV) are pre-validated in [`hardware/production_packages/`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages).*

| Board | Production Package | Qty | Layers / Specification |
| :--- | :--- | :---: | :--- |
| **1. Main Box Controller PCBA** | [`01_main_box_pcba_gerbers_jlcpcb.zip`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/01_main_box_pcba/01_main_box_pcba_gerbers_jlcpcb.zip) | **1** | 4-Layer FR4 TG150, ENIG, $110 \times 60\,\text{mm}$, ESP32-S3, LM5164, BQ24075 |
| **2. Pod Base Carrier PCBA** | [`02_pod_base_pcba_gerbers_jlcpcb.zip`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/02_pod_base_pcba/02_pod_base_pcba_gerbers_jlcpcb.zip) | **3** | 2-Layer FR4, ENIG, M8 6-pin connector, SP3012 ESD array |
| **3. Universal Cartridge PCBA** | [`03_pod_cartridge_pcba_gerbers_jlcpcb.zip`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/03_pod_cartridge_pcba/03_pod_cartridge_pcba_gerbers_jlcpcb.zip) | **2** | 2-Layer FR4, 6-pin socket, DS2401 1-Wire silicon ID, JST-SH connector |
| **4. Rear Pod 3 Transceiver PCBA**| [`04_rear_pod3_pcba_gerbers_jlcpcb.zip`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/04_rear_pod3_pcba/04_rear_pod3_pcba_gerbers_jlcpcb.zip) | **1** | 4-Layer FR4 TG150, ESP32-C3, u-blox MAX-M10S GNSS, SX1262 LoRa, patch antenna |

---

### 2.3 Category C: Standard Fasteners, Screws & Springs (V4A Stainless / Brass)

| Item | Specification / Standard | Qty | Purpose |
| :--- | :--- | :---: | :--- |
| **Threaded Inserts** | Brass M3 $\times 5.7\,\text{mm}$ (Ruthex RX-M3x5.7 / Tappex) | **4** | Heat-set into the 4 corners of the lower case tub |
| **Enclosure Clamping Screws** | Socket Head Cap Screw DIN 912 Stainless V4A M3 $\times 40\,\text{mm}$ | **4** | 4-corner through-bolt clamping (Lid $\rightarrow$ Mid Tray $\rightarrow$ Lower Case) |
| **Main Board PCB Screws** | Socket Head Cap Screw DIN 912 Stainless V4A M2.5 $\times 6\,\text{mm}$ | **4** | PCB fastening onto lower tub vibration standoffs |
| **Cartridge Insert Screws** | Countersunk Screw DIN 7991 Stainless V4A M2 $\times 6\,\text{mm}$ | **12** | 4x screws per cartridge to secure modular OEM top inserts (3 cartridges: 2x Intercom Pods + 1x Rear Transceiver) |
| **Cartridge PCB Screws** | Socket Head Cap Screw DIN 912 Stainless V4A M2 $\times 4\,\text{mm}$ | **12** | 4x screws per cartridge to mount Carrier PCBs / Transceiver PCB inside base sled (3 cartridges) |
| **Pod Bulkhead Screws** | Countersunk Screw DIN 7991 V4A M2 $\times 8\,\text{mm}$ | **6** | 2x screws per pod to secure internal bulkhead partition |
| **Auto-Eject Compression Springs**| Stainless V4A, $\text{OD} = 4.5\,\text{mm}$, $L_0 = 15\,\text{mm}$, wire $d = 0.4\,\text{mm}$ | **6** | Auto-Eject mechanism (2 springs per pod bulkhead) |
| **Anti-Vibration Silentblocks** | Rubber Buffer Type A (Male/Female M4, $\varnothing 15 \times 10\,\text{mm}$) | **4** | Decoupled chassis mounting of central main box |
| **Nyloc Lock Nuts & Washers** | DIN 985 M4 Locknuts + DIN 125 Washers V4A | **4** | Securing silentblock studs to motorcycle subframe |

---

### 2.4 Category D: Seals, Breathers & Optical Elements (IP67)

| Item | Specification | Qty | Purpose |
| :--- | :--- | :---: | :--- |
| **Main Box Perimeter Gasket** | Silicone cord $\varnothing 1.5\,\text{mm}$ Shore 40A / 50A ($40\,\text{cm}$ length) | **1** | Hermetic tongue-and-groove seal between lower case and mid tray |
| **Cartridge Faceplate Gaskets** | Molded silicone gasket Shore 40A ($54 \times 18\,\text{mm}$, $1.5\,\text{mm}$ thk) | **3** | IP67 front faceplate seal against pod mouth rim |
| **Pressure Equalization Vent** | Gore Automotive AVS 41 (M8 screw-in vent) or AVS 4 | **1** | Pressure equalization & condensate prevention in main box lid (optional) |
| **ePTFE Adhesive Breathers** | Gore / Porex IP67 adhesive membrane disc $\varnothing 7.0\,\text{mm}$ | **4** | 3x for the top breather bosses of the 3 pod roofs + 1x for main box lid (or 1x spare) |
| **Light Pipe (RGB LED)** | Bivar PLPC3-3MM or Mentor 1292.1101 (PMMA $\varnothing 3.0\,\text{mm}$) | **1** | IP67 optical coupling of WS2812B RGB LED through top lid |

---

### 2.5 Category E: Wiring Harness, Connectors, Remote & Sensors

| Item | Specification / MPN | Qty | Purpose |
| :--- | :--- | :---: | :--- |
| **HD26 Receptacle (Chassis)** | Amphenol LTW HD26 IP67 Panel Mount Receptacle | **1** | Main enclosure connector on central box |
| **HD26 Cable Plug** | HD26 Plug IP67 with metal/plastic hood & thumbscrews | **1** | Mating plug on motorcycle wiring harness |
| **M8 6-Pin Cable Plugs** | M8 Circular Connector 6-Pin A-Coded IP67 (Male, screw termination)| **3** | Harness connections to the 3 pods (Pigtails 1, 2, and 3) |
| **M8 4-Pin Cable Plug** | M8 Circular Connector 4-Pin A-Coded IP67 (Male, screw termination)| **1** | Front cockpit branch (Pigtail 5: CAN-Bus & Ambient Mic) |
| **Superseal 4-Pin Plug** | AMP Superseal 1.5 4-Pin Housing with seals & terminals | **1** | 12V vehicle power supply branch (Pigtail 4: Kl. 30, Kl. 15, GND) |
| **Front Ambient Mic** | Knowles SiSonic / SPH0645 MEMS with IP67 ePTFE Acoustic Vent | **1** | *Optional:* Ambient noise sensing for DSP transparency mode (Pigtail 5) |
| **Wireless Handlebar Remote**| BLE 5.0 Wireless Remote with CR2032 Battery (e.g. Sena RC4 / generic)| **1** | Wireless PTT voice control & Action Cam video highlight marker ($\varnothing 22 \dots 28\,\text{mm}$) |
| **Backup Battery** | 3.7V LiPo $1000\,\text{mAh}$ (max $52 \times 36 \times 6\,\text{mm}$) with 10k NTC | **1** | UPS power during engine crank & ignition-off logging |
| **Battery Connector** | Molex Micro-Fit 3.0 2-Pin Receptacle Housing with crimps | **1** | Battery connection to main board (`J_BAT`) |
| **Inline Fuse Holder** | Waterproof Mini Blade Fuse Holder IP67 with **2A fuse** | **1** | Primary battery lead protection (Kl. 30 directly at battery) |
| **Automotive Wire** | FLRY-B $0.35\,\text{mm}^2$ (Signals/Audio) and $0.5\,\text{mm}^2$ (12V Power/GND) | *as needed*| Harness assembly according to [`central_breakout_harness_wirelist.csv`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/05_wiring_harness/central_breakout_harness_wirelist.csv) |
| **EPDM Straps** | Ozone & UV-resistant EPDM rubber ladder straps or heavy-duty O-rings | **6** | Toolless mounting of the 3 pods to handlebar/frame tubes ($\varnothing 22 \dots 28\,\text{mm}$) |

---

### 2.6 Category F: Tools & Consumables

* **Soldering Iron / Station** with fine tip (for harness & heat-setting brass inserts at $\approx 220\,^\circ\text{C}$).
* **Hex Keys (Allen):** $1.5\,\text{mm}$ (M2), $2.0\,\text{mm}$ (M2.5), $2.5\,\text{mm}$ (M3), $3.0\,\text{mm}$ (M4).
* **Threadlocker:** *Loctite 243* (blue, medium strength).
* **Silicone Grease:** Thin film for O-ring cord and cartridge sealing lips.
* **Conformal Coating:** *Peters Elpeguard SL 1307* or *Electrolube UR5041* polyurethane coating (IPC-CC-830B).
* **USB-C Data Cable:** For firmware upload and WebBLE testing.

---

## 3. Step-by-Step Build & Assembly Guide

### Step 1: 3D Printed Parts Preparation
1. **Inspection:** Clean all parts from residual MJF powder. Blow through guide grooves and sealing channels with compressed air.
2. **Heat-Set Threaded Inserts:**
   * Set soldering station to $220\,^\circ\text{C}$.
   * Gently press the 4x M3 brass inserts perpendicularly into the corner posts of the lower case tub ([`main_box_lower_case.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lower_case.stl)) until flush with the post tops.
3. **Install Light Pipe:** Press the PMMA light pipe from inside into the lid ([`main_box_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lid.stl)) with a tiny drop of clear silicone.

---

### Step 2: PCB Preparation & Conformal Coating
1. **Visual QC:** Inspect solder joints on all 4 PCBAs under magnification. Verify no solder bridges under ESP32-S3, LM5164, BQ24075, or audio transformers.
2. **Masking:** Mask the MicroSD slot (`J2`), 6-pin precision headers (`J1`), M8 connector contacts, and ePTFE vent areas with Kapton tape.
3. **Apply Conformal Coating:** Apply a uniform $40 \dots 60\,\mu\text{m}$ PU coating (*Peters Elpeguard*) to both sides and allow to cure for 24 hours.

---

### Step 3: Central Main Box Assembly
1. **Mount Main Board:**
   * Place 4x small NBR O-rings ($\varnothing 3 \times 1\,\text{mm}$) as vibration dampers onto the lower tub standoffs.
   * Insert main board and fasten with 4x M2.5 $\times 6\,\text{mm}$ screws with a drop of *Loctite 243* ($0.35\,\text{Nm}$).
2. **Mount HD26 Flange Receptacle:**
   * Seat the HD26 receptacle with its silicone gasket into the mid tray cutout and connect the ribbon cable to the main board.
3. **Install Backup Battery:**
   * Affix the $1000\,\text{mAh}$ LiPo into the mid tray cradle ([`main_box_mid_tray.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_mid_tray.stl)) using a $1\,\text{mm}$ EPDM foam pad.
   * Route battery leads through the front wire slot and plug into `J_BAT`.
4. **Close Sandwich Enclosure:**
   * Lay the silicone cord ($\varnothing 1.5\,\text{mm}$) lightly greased into the lower tub perimeter groove.
   * Place mid tray on top, then place top lid.
   * Fasten the 4x M3 $\times 40\,\text{mm}$ screws in a cross pattern to $0.8\,\text{Nm}$.
   * Screw the Gore AVS 41 vent into the lid.

---

### Step 4: Satellite Pods Assembly
*Perform identically for all 3 pods (Pod 1 Left, Pod 2 Right, Pod 3 Rear):*
1. **Insert Pod Base PCBA:** Slide the board into the tunnel from the front mouth until the M8 threaded neck protrudes from the rear gland.
2. **Secure M8 Neck:** Tighten the M8 nut and O-ring at the rear collar.
3. **Install Eject Springs:** Push 2x stainless springs ($\varnothing 4.5 \times 15\,\text{mm}$) onto the bulkhead guide posts.
4. **Fasten Bulkhead:** Secure the bulkhead ([`03_pod_bulkhead_partition.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl)) using 2x M2 $\times 8\,\text{mm}$ screws.
5. **Apply Vent Membrane:** Stick an ePTFE disc ($\varnothing 7\,\text{mm}$) onto the top vent boss.

---

### Step 5: Assembling the Modular Cartridges
1. **Rear Cartridge (Pod 3):** Insert the `04_rear_pod3_pcba` transceiver board with front-facing 6-pin precision socket into the sled [`cartridge_omm_transceiver_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_omm_transceiver_sled.stl) and secure with **4x M2/M2.5 screws** into the 4 corner standoff posts.
2. **Audio & Intercom Cartridges (Pod 1 & 2):**
   * Insert the `03_pod_cartridge_pcba` carrier board ($35 \times 25\,\text{mm}$) into the front bay of the base sled and secure with **4x M2 screws** (minimum 2 diagonally) onto the 4 floor bosses.
   * Plug in the headset wiring harness (JST-SH 1.0 mm) and route upward through the floor opening.
   * Seat the desired intermediate deck ([`cartridge_insert_sena.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) or [`cartridge_insert_cardo.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl)) and fasten with **4x M2 countersunk screws** into the 4 tall corner posts.
   * Place OEM clamp cradle (Sena clamp kit / Cardo Air-Mount) and secure with an elastic EPDM retention strap on the outer hooks.
3. **Attach Flange Gasket:** Slide the molded silicone flange seal over the sealing collar behind the front faceplate.
4. **Functional Latch Test:** Slide cartridge into pod tunnel $\rightarrow$ must latch with a crisp, audible click. Squeezing both side buttons must cause the cartridge to auto-eject outward by $\approx 8 \dots 10\,\text{mm}$.

---

### Step 6: Vehicle Wiring Harness Assembly
The central HD26 breakout harness fans out from the main box under the seat into **5 dedicated pigtails**:
1. **Pigtails 1 & 2 (M8 6-Pin):** To Satellite Pod 1 (Rider) & Pod 2 (Pillion) for audio in/out, isolated opto-PTT, and 1-Wire ID.
2. **Pigtail 3 (M8 6-Pin):** To Rear Pod 3 (tail / license plate bracket) for high-speed UART (460.8k baud), 1-PPS GNSS time sync, and 1-Wire ID.
3. **Pigtail 4 (Superseal 1.5 4-Pin):** 12V vehicle power directly to motorcycle battery (`Kl. 30` fused permanent 12V, `Kl. 15` switched ignition, `GND` vehicle ground).
4. **Pigtail 5 (M8 4-Pin A-Coded):** Combined front cockpit branch behind headlight mask:
   * **Pins 1 & 2:** `CAN_H` & `CAN_L` for vehicle CAN-bus telemetry (120 Ω differential).
   * **Pins 3 & 4:** `FRONT_MIC_SIG` & `FRONT_MIC_GND` for the optional weatherproof Knowles SiSonic MEMS ambient microphone.

#### Vehicle-Specific Length Adjustment:
Mock-route on the motorcycle frame with cord before cutting:
* **Handlebar / Cockpit / Front Branch (Pigtails 1, 2, 5):** approx. $150 \dots 190\,\text{cm}$ (along frame backbone through steering head area).
* **Crash Bars (Travel Enduros e.g. BMW GS, T7, Africa Twin):** approx. $110 \dots 140\,\text{cm}$.
* **Side Covers / Battery Trays (Harley-Davidson Tourers, Cruisers, Softail):** approx. $25 \dots 50\,\text{cm}$.
* **Rear Tail / License Plate Carrier (Pigtail 3 / Pod 3):** approx. $40 \dots 80\,\text{cm}$.
* **Pin Assignment & Wiring:** Solder and crimp strictly following [`central_breakout_harness_wirelist.csv`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/05_wiring_harness/central_breakout_harness_wirelist.csv).
* **Harness Protection:** Encase all branches in braided expandable sleeving and adhesive-lined heat shrink tubing.
* **Inline Fuse:** Solder the waterproof inline fuse holder with **2A fuse** into the red Kl. 30 lead directly at the battery terminal.

---

## 4. Software Flashing & Initial Test (Step-by-Step)

```bash
# 1. Clone repository and navigate to main controller
cd openMotorBridge/firmware/main_controller

# 2. Flash Central Controller via native USB-C (ESP32-S3)
pio run --target upload

# 3. Upload Cartridge JSON profiles to LittleFS
pio run --target uploadfs

# 4. Flash Rear Pod 3 Co-Processor (ESP32-C3 in Pod 3)
cd ../rear_coprocessor
pio run --target upload
```

### Commissioning Checklist:
1. [ ] **Bench Power:** Apply $12.0\,\text{V}$ with $150\,\text{mA}$ current limit. Measure idle current: $45 \dots 75\,\text{mA}$.
2. [ ] **Status LED:** Flashes green on boot (system initialized, backup battery charging).
3. [ ] **Web Dashboard:** Open [`https://schmidtmt.github.io/openmotorbridge/`](https://schmidtmt.github.io/openmotorbridge/) in Chrome/Edge (or locally [`webapp_pwa/index.html`](file:///Users/schmidtm/openMotorBridge/webapp_pwa/index.html)), click "⚡ Connect BLE", and pair with `OpenMotorBridge_v8`.
4. [ ] **Cartridge Detection:** Insert cartridges into Pods 1, 2, and 3. The dashboard must immediately display the detected profile (e.g., "Sena 50S Mesh", "Cardo Packtalk", "OMM Transceiver") and 1-Wire serial number.
5. [ ] **Pair Wireless Handlebar Remote:** In dashboard under *Cockpit & Power*, click **"🔗 Pair Remote"** on the Handlebar Remote tile and hold the button on the BLE remote for 5 s. Confirm pairing and check CR2032 battery readout (e.g., 95%).
6. [ ] **Configure Home Wi-Fi & WebDAV:** In dashboard under *Tours & WebDAV*, enter your garage Wi-Fi SSID, password, and WebDAV server URL (Nextcloud/Synology), then click **"Save Wi-Fi & WebDAV"**.
7. [ ] **Front Ambient Mic & Transparency Mode:** Plug optional microphone into M8 4-pin pigtail 5. Speak into microphone while stationary (< 30 km/h) $\rightarrow$ ambient audio is injected into helmet headset (automatically mutes while riding).
8. [ ] **Audio Test:** Connect headset, play music $\rightarrow$ pristine audio without alternator whine or ground loop noise (isolated by 1500V Bourns transformers).

---

## 5. Maintenance & Care

* **Gasket Lubrication:** Once per season, apply a tiny smear of silicone grease to the main box perimeter seal and cartridge flange gaskets.
* **Breather Inspection:** Keep the ePTFE Gore membranes free of mud and heavy wax.
* **Firmware Updates:** Perform wireless over-the-air updates directly via the WebBLE PWA dashboard.
