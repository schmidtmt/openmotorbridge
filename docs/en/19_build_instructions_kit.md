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

### 2.1 Category A: 3D Printed Parts (HP MJF PA12 Black)
*Recommended manufacturing process: Multi Jet Fusion (MJF) or SLS in PA12 (glass-bead blasted, black dyed). Production packages are located in [`hardware/production_packages/06_3d_print_mjf_stls/`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/06_3d_print_mjf_stls).*

| Assembly | Filename / STL | Qty | Function & Description |
| :--- | :--- | :---: | :--- |
| **Main Box Lower Tub** | [`main_box_lower_case.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lower_case.stl) | **1** | Monocoque base with 4x M4 silentblock ears, 4x PCB standoffs & O-ring groove |
| **Main Box Mid Tray** | [`main_box_mid_tray.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_mid_tray.stl) | **1** | Battery cradle, 10x convective vent slots, HD26/USB-C/LED cutouts & sealing lip |
| **Main Box Top Lid** | [`main_box_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lid.stl) | **1** | Top closure lid with Gore ePTFE vent boss & 4x M3 corner screw counterbores |
| **Pod Base Housing** | [`pod_base_housing.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod_base_housing.stl) | **3** | Universal bay for Pod 1, 2, and 3 with V-tube saddle, 4x EPDM strap hooks & M8 neck |
| **OMM Rear Cartridge** | [`cartridge_omm_transceiver_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_omm_transceiver_sled.stl) | **1** | Sled for Pod 3 (houses Rear Pod 3 PCBA with GNSS/LoRa/2.4GHz antennas) |
| **Handlebar Cartridge Left**| [`cartridge_sena_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_sena_sled.stl) *(or Cardo)* | **1** | Sled for Headset 1 (Sena 50S/60S or Cardo Packtalk Edge) |
| **Handlebar Cartridge Right**| [`cartridge_blindkassette_waterproof.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_blindkassette_waterproof.stl) *(or Cardo/Sena)* | **1** | Sled for Headset 2 or hermetic IP67 blank dummy with storage dry box |
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
| **Pressure Equalization Vent** | Gore Automotive AVS 41 (M8 screw-in vent) or AVS 4 | **1** | Pressure equalization & condensate prevention in main box lid |
| **ePTFE Adhesive Breathers** | Gore / Porex IP67 adhesive membrane disc $\varnothing 7.0\,\text{mm}$ | **4** | Applied to top breather bosses of the 3 pods and cartridges |
| **Light Pipe (RGB LED)** | Bivar PLPC3-3MM or Mentor 1292.1101 (PMMA $\varnothing 3.0\,\text{mm}$) | **1** | IP67 optical coupling of WS2812B RGB LED through top lid |

---

### 2.5 Category E: Wiring Harness, Connectors & Battery

| Item | Specification / MPN | Qty | Purpose |
| :--- | :--- | :---: | :--- |
| **HD26 Receptacle (Chassis)** | Amphenol LTW HD26 IP67 Panel Mount Receptacle | **1** | Main enclosure connector on central box |
| **HD26 Cable Plug** | HD26 Plug IP67 with metal/plastic hood & thumbscrews | **1** | Mating plug on motorcycle wiring harness |
| **M8 6-Pin Cable Plugs** | M8 Circular Connector 6-Pin A-Coded IP67 (Male, screw termination)| **3** | Harness connections to the 3 pods |
| **Backup Battery** | 3.7V LiPo $1000\,\text{mAh}$ (max $52 \times 36 \times 6\,\text{mm}$) with 10k NTC | **1** | UPS power during engine crank & ignition-off logging |
| **Battery Connector** | Molex Micro-Fit 3.0 2-Pin Receptacle Housing with crimps | **1** | Battery connection to main board (`J_BAT`) |
| **Inline Fuse Holder** | Waterproof Mini Blade Fuse Holder IP67 with **2A fuse** | **1** | Primary battery lead protection (Kl. 30 directly at battery) |
| **Automotive Wire** | FLRY-B $0.35\,\text{mm}^2$ (Signals/Audio) and $0.5\,\text{mm}^2$ (12V Power/GND) | *as needed*| Harness assembly according to [`central_breakout_harness_wirelist.csv`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/05_wiring_harness_spec/central_breakout_harness_wirelist.csv) |
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

### Step 5: Cartridge Assembly & Test
1. **Rear Cartridge (Pod 3):** Snap the `04_rear_pod3_pcba` into [`cartridge_omm_transceiver_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_omm_transceiver_sled.stl) and secure with 2x M2 screws.
2. **Handlebar Cartridges (Pod 1 & 2):** Mount the `03_pod_cartridge_pcba` adapter board into the respective sled and plug in the headset harness (JST-SH).
3. **Attach Flange Gasket:** Fit the silicone faceplate seal over the cartridge rim.
4. **Latch & Eject Test:** Insert cartridge into pod bay $\rightarrow$ must lock with an audible click. Squeezing both release buttons must automatically eject the cartridge by $8 \dots 10\,\text{mm}$.

---

### Step 6: Motorcycle Wiring Harness Assembly
1. **Wire Gauge:** Use FLRY-B $0.5\,\text{mm}^2$ for 12V power/ground and $0.35\,\text{mm}^2$ for audio and signals.
2. **Cable Lengths:** Measure and cut the 3 pod branches to fit your vehicle:
   * **Pod 1 (Handlebar Left):** $\approx 150 \dots 180\,\text{cm}$.
   * **Pod 2 (Handlebar Right):** $\approx 150 \dots 180\,\text{cm}$.
   * **Pod 3 (Tail/License Plate):** $\approx 40 \dots 80\,\text{cm}$.
3. **Pin Assignment:** Solder and crimp strictly following [`central_breakout_harness_wirelist.csv`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/05_wiring_harness_spec/central_breakout_harness_wirelist.csv).
4. **Harness Protection:** Encase all branches in braided expandable sleeving and adhesive-lined heat shrink tubing.
5. **Inline Fuse:** Solder the waterproof inline fuse holder with **2A fuse** into the red Kl. 30 lead directly at the battery terminal.

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
3. [ ] **Web Dashboard:** Open `https://schmidtmt.github.io/openmotorbridge/` in Chrome/Edge, click "Connect WebBLE", and pair with `OpenMotorBridge_v8`.
4. [ ] **Cartridge Detection:** Insert cartridges into Pods 1, 2, and 3. The dashboard must immediately display the detected profile (e.g., "Sena 50S Mesh", "Cardo Packtalk", "OMM Transceiver") and 1-Wire serial number.
5. [ ] **Audio Test:** Connect headset, play music $\rightarrow$ pristine audio without alternator whine or ground loop noise (isolated by 1500V Bourns transformers).

---

## 5. Maintenance & Care

* **Gasket Lubrication:** Once per season, apply a tiny smear of silicone grease to the main box perimeter seal and cartridge flange gaskets.
* **Breather Inspection:** Keep the ePTFE Gore membranes free of mud and heavy wax.
* **Firmware Updates:** Perform wireless over-the-air updates directly via the WebBLE PWA dashboard.
