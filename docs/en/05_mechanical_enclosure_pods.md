# 05 - Mechanical Construction: 3-Piece Sandwich Enclosure, Mid-Baffle & Modular Pods

This document specifies the mechanical construction, thermal management, and IP67/IP69K enclosure design of the central main control box (Type A) in a **3-piece sandwich construction (Lower Hull, Upper Tray with Mid-Baffle, Enclosure Lid)** with **integrated battery retention on top of the mid-baffle**, **front-panel interfaces (HD26, USB-C & RGB Status LED window)** in the upper tray, **planar 4-layer copper heat spreader and 11x mid-baffle convection slots**, as well as the universal satellite pod system (Type B) with modular slide-in cartridges.

---

## 1. Enclosure Type A: Central Main Box (3-Piece Sandwich Design)

The base housing of the central main box is engineered as a modular, 3-piece IP67/IP69K sandwich enclosure made of **PA12 (MJF process)** or **die-cast aluminum**, designed specifically for harsh motorcycle operating conditions (vibrations up to $20\,\text{g}$, high-pressure washdowns, heat buildup under the seat, and extreme road grime):

- **External Dimensions:** $110.0 \times 74.0 \times 38.0\,\text{mm}$ (L x W x H; Lower Hull $17.0\,\text{mm}$, Upper Tray $15.0\,\text{mm}$, Top Lid $6.0\,\text{mm}$).
- **Mounting:** 4x integrated corner ears on the lower hull with **hole spacing of $128.0 \times 56.0\,\text{mm}$** for vibration-damping **M4 silentblocks (Shore 50A EPDM)** to decouple high-frequency engine harmonics.
- **Internal Clearance:** $102.0 \times 66.0 \times 32.0\,\text{mm}$ (optimized for the $85.0 \times 55.0\,\text{mm}$ 4-layer main PCB).
- **Material & Manufacturing:** PA12 via HP Multi Jet Fusion (MJF) 3D printing (min. $3.0\,\text{mm}$ wall thickness), glass-bead blasted, chemically smoothed in hot vapor bath, and hydrophobic sealed.
- **Protection Class:** IP67 / IP69K (dust-tight, submersible to $1\,\text{m}$ depth, and resistant to high-pressure steam cleaning).

### 1.1 3D CAD Model & 3-Tier Sandwich Hierarchy

![OpenMotorBridge Central Main Box 3-Piece Sandwich Enclosure IP67](../images/cad/main_box_enclosure_cad.png)

*Figure 5.1: 3D CAD render of the central control box. Left: Closed IP67 housing with HD26 harness flange, USB-C service screw cap, and flush RGB status window on the front face of the upper tray, 4x M4 silentblock ears on the lower hull, and flat lid with Gore vent. Right: Sectional X-ray view revealing the 3 sandwich tiers: 1. Lower Hull (100% solid homogeneous PA12 floor, 4-layer PCB on M2.5 standoffs), 2. Upper Tray with Mid-Baffle (LiPo battery with EPDM strap on top, 11x convection slots & wire slot in floor, ports on front face), 3. Solid protective lid with Gore vent (100% sealed).*

```
┌────────────────────────────────────────────────────────────┐  ▲
│ 1. ENCLOSURE LID (6.0 mm Height / 3.0 mm Wall Thickness)   │  │
│    • Gore ePTFE Pressure Equalization Vent (Ø 7.0 mm)      │  │ 38.0 mm
│    • Perimeter Groove with Shore 40A Silicone Profile Seal │  │ Total
│    • 100% Homogeneous Solid PA12 Protective Cover          │  │ Height
├────────────────────────────────────────────────────────────┤  │
│ 2. UPPER TRAY WITH MID-BAFFLE (15.0 mm Height)             │  │
│    • Front Face (All Interfaces & Visual Indicators):      │  │
│      - HD26 D-Sub Wall Flange (Main Vehicle Harness)       │  │
│      - Waterproof USB-C Service Port (Aluminum Screw Cap)  │  │
│      - Waterproof RGB Status LED Window (Ø 3 mm Flush)     │  │
│    • Upper Compartment (on top of Mid-Baffle):             │  │
│      - 1S LiPo UPS Buffer Battery (52x36x6.5mm) in Cradle  │  │
│      - EPDM Rubber Retention Strap for Battery Fixation    │  │
│    • Mid-Baffle Floor (Optimized Thermal Circulation):     │  │
│      - 25.0 x 4.0 mm Cable Pass-Through Slot               │  │
│      - 11x Convection & Breathing Ventilation Slots        │  │
├────────────────────────────────────────────────────────────┤  │
│ 3. LOWER HULL (17.0 mm Height - Solid Monocoque Tray)      │  │
│    • 4-Layer Main PCB (85 x 55 mm) on M2.5 Damping Mounts  │  │
│    • 2x 35 µm Solid Internal Copper Planes as Heat Spreader│  │
│    • 4x M4 Silentblock Mounting Ears (Vibration Isolation) │  │
│    • 100% Solid PA12 Floor without Enclosure Penetrations  │  │
└────────────────────────────────────────────────────────────┘  ▼
```

### 1.2 3D Exploded View & Sandwich Stratification (1:1:1 CAD Fitting)

![OpenMotorBridge Central Main Box Exploded 3D CAD Fitting](../images/cad/main_box_full_assembly_exploded_3d.png)

*Figure 5.1.1: 1:1:1 Euclidean scale 3D CAD exploded assembly of the central main box. Displays all 5 assembly tiers along the vertical Z-axis: lower hull with 4x M4 silentblock mounts and 100% solid PA12 floor, 4-layer main PCB (85x55mm) with planar copper heat spreader, upper tray with mid-baffle (11x convection slots) and front interfaces (HD26, USB-C, LED), 1S LiPo buffer battery in cradle with EPDM retention strap, and protective lid with Gore ePTFE vent.*

### 1.3 3D Mated X-Ray View & Mechanical Fitting

![OpenMotorBridge Central Main Box Mated 3D X-Ray CAD Fitting](../images/cad/main_box_assembly_mated_3d.png)

*Figure 5.1.2: Translucent 3D X-ray view of the closed central control box. Confirms zero-collision component clearances, secure battery retention in the upper cradle, continuous convection through the 11 mid-baffle slots, and smooth wiring trajectory directly to the HD26 wall flange.*

### 1.4 True-to-Scale Longitudinal & Transverse Cross-Sections (X-Z Thermal & Y-Z Cable Path)

![OpenMotorBridge Central Main Box Cross Sections](../images/cad/main_box_assembly_cross_section.png)

*Figure 5.1.3: 2D cross-sections of the central main box. Top: Longitudinal (X-Z plane) showing the direct planar thermal dissipation path (4-layer Cu spreader $\rightarrow$ 11x mid-baffle convection slots $\rightarrow$ Gore ePTFE pressure vent) and battery bay. Bottom: Transverse (Y-Z plane) illustrating front interface integration directly to the sealed HD26 SEAL-D flange on the front wall.*

---

## 2. Thermal Management & Planar PCB Heat Spreading (Copper-Stud Free)

The central box houses the core active components: $100\,\text{V}$ switching regulator (LM5164-Q1, $0.42\dots 0.58\,\text{W}$), LiPo charge controller (BQ24075, up to $0.55\,\text{W}$ during fast charge), and ESP32-S3 DSP core ($0.46\,\text{W}$). Total continuous heat dissipation in regular operation is only **$\approx 1.5\,\text{W}$** (peak during initial 500mA fast-charging: $2.45\,\text{W}$).

```
       4-LAYER PRINTED CIRCUIT BOARD (PLANAR COPPER HEAT SPREADER)
┌────────────────────────────────────────────────────────┐
│ [ LM5164 Buck ]     [ BQ24075 UPS ]     [ ESP32-S3 ]   │ ◄── Active Components (SMD)
│   (100V DCDC)       (Power-Path)        (Dual-Core)    │
├────────────────────────────────────────────────────────┤
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │ ◄── Layer 2: 35 µm Solid GND Plane
├────────────────────────────────────────────────────────┤
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │ ◄── Layer 3: 35 µm Solid PWR/GND Plane
└──────────────────────────┬─────────────────────────────┘     (λ = 390 W/m·K, 93.5 cm² Area)
                           │
 ┌─────────────────────────▼─────────────────────────────┐
 │ 11x MID-BAFFLE CONVECTION SLOTS & INTERNAL AIR        │ ◄── Free Circulation in 210 cm³
 │ (Homogeneous heat distribution across total box)      │     Air Volume & Gore ePTFE Vent
 └─────────────────────────┬─────────────────────────────┘
                           ▼
        Dissipation through Outer PA12 Surface (300 cm²) to Ambient Air
```

### 2.1 Specification & Physical Operation:
1. **Planar 4-Layer Copper Heat Spreader ($85 \times 55\,\text{mm}$):**
   * Two continuous $35\,\mu\text{m}$ (1 oz) solid internal planes (`GND` and `PWR`) rapidly conduct heat ($\lambda = 390\,\text{W/(m}\cdot\text{K)}$) away from the LM5164, BQ24075, and ESP32, spreading it uniformly across the entire $93.5\,\text{cm}^2$ board surface.
   * Eliminates localized hot spots; normal summer PCB surface temperature stabilizes at a uniform $\approx 55\,^\circ\text{C}$.
2. **11x Enhanced Convection Slots in Mid-Baffle:**
   * 5 slots along the rear edge ($Y = 58\,\text{mm}$), 4 slots on the side flanks ($X = 10\,\text{mm}, 92\,\text{mm}$), and 2 slots on the front edge allow warmed air to rise freely into the upper lid chamber.
   * The total internal air volume ($\approx 210\,\text{cm}^3$) acts as an integrated thermal buffer, equalizing pressure and temperature through the central Gore ePTFE vent.
3. **Thermal Safety Margins Under Extreme Stress (Traffic Jam at $45\,^\circ\text{C}$ + $13\,^\circ\text{C}$ Engine Soak = $58\,^\circ\text{C}$ Under-Seat):**
   * **LM5164-Q1:** $T_j = 93.8\,^\circ\text{C}$ (AEC-Q100 rating up to $+150\,^\circ\text{C}$ $\rightarrow$ **$+56.2\,^\circ\text{C}$ Safety Margin**).
   * **ESP32-S3:** $T_j = 90.2\,^\circ\text{C}$ (Industrial rating up to $+105\,^\circ\text{C}$ $\rightarrow$ **$+14.8\,^\circ\text{C}$ Safety Margin**).
   * **3.3V LDO:** $T_j = 110.4\,^\circ\text{C}$ (Rated up to $+125\,^\circ\text{C}$ / $+150\,^\circ\text{C}$).
   * **1S LiPo Battery:** Remains safely under $60\,^\circ\text{C}$ in the upper chamber (JEITA NTC protection pauses charging above $45\,^\circ\text{C}$).
4. **Engineering Advantages of 100% Copper-Stud-Free Design:**
   * **Guaranteed IP67/IP69K Waterproofing:** Monolithic lower tub without floor through-holes or sealant joints that could degrade over years of vibration.
   * **Direct-From-Printer Ready:** 3D-printed PA12 MJF parts require zero machining or insert-pressing.
   * **Full Mechanical Vibration Isolation:** 4x M4 rubber silentblocks on the hull mounting ears isolate the entire box from motorcycle chassis vibration.

---

## 3. Upper Tray: Front Interfaces, Battery Retention & Mid-Baffle

The upper tray forms the central functional module of the sandwich design: it consolidates all user-accessible interfaces and indicators on its front panel, and accommodates the UPS buffer battery on top of the integrated mid-baffle.

```
┌─────────────────────────────────────────────────────────────┐
│                 UPPER TRAY (Top-Down on Mid-Baffle)         │
│                                                             │
│  ┌─────────────────────────┐  ┌──────────────────────────┐  │
│  │ 1. BATTERY CRADLE       │  │ 2. Ribbon Cable Slot     │  │
│  │    (52 x 36 x 6.5 mm)   │  │    (38.0 x 6.0 mm, R1.5) │  │
│  │    with EPDM Strap      │  │    leads to J1 on PCB    │  │
│  │    [4P JST-PH Grommet]  │  └──────────────────────────┘  │
│  └─────────────────────────┘                                │
│                                                             │
│  FRONT WALL: [ USB-C Port ]   [ RGB-LED ]   [ HD26 Flange ] │
└─────────────────────────────────────────────────────────────┘
```

### 3.1 1S LiPo Battery Cradle & 4-Pin JST-PH Cable (On Mid-Baffle)
* **Form-Fit Battery Cradle ($52.0 \times 36.0 \times 6.5\,\text{mm}$):** Molded directly on top of the mid-baffle, lined with a $1.0\,\text{mm}$ EPDM closed-cell foam pad for shock absorption.
* **Elastic EPDM Rubber Retention Strap (Shore 50A, $10\,\text{mm}$ wide):** Spans across the battery pack. End eyelets snap tool-lessly into two undercut anchor hooks in the upper tray side walls. The battery remains securely locked in place and vibration-free.
* **Combined 4-Wire Cable (JST-PH 2.0 mm Shrouded Connector):**
  * Battery and integrated NTC thermistor connect via a single polarized **4-Pin JST-PH shrouded header with locking ramp** (`J5`):
    * Pin 1: `BAT+` (+3.7V / +4.2V 1S LiPo)
    * Pin 2: `BAT-` (`GND_PWR`)
    * Pin 3: `NTC_JEITA` (10k NTC temperature monitoring)
    * Pin 4: `NTC_GND` (Sensor ground)
  * The cable routes through a rounded $\varnothing\,5\,\text{mm}$ grommet in the left mid-baffle floor straight down to header `J5` on the front left edge of the main PCB (with $> 12\,\text{mm}$ clear safety margin to the ESP32-S3).

### 3.2 Pass-Through Specifications in Mid-Baffle
1. **Ribbon Cable Pass-Through for Main Harness:**
   * **Dimensions:** $38.0 \times 6.0\,\text{mm}$ with $R=1.5\,\text{mm}$ edge chamfer on top and bottom faces.
   * **Position:** Located on the right side directly above the 2x13 box header `J1` on the main PCB.
   * **Routing:** The $45\,\text{mm}$ flexible 26-conductor ribbon cable runs from the HD26 wall flange in the upper tray through this slot down to header `J1`.
2. **Labyrinth Pressure Equalization & Venting Slots:**
   * 4x Ventilation slots ($15.0 \times 2.0\,\text{mm}$) allow unimpeded airflow between the lower PCB chamber and the upper chamber / ePTFE vent in the lid.

---

## 4. Front Panel Interfaces in Upper Tray (USB-C, RGB-LED & HD26)

All three physical interface and display elements are co-located in the **front face of the upper tray**:

```
                  FRONT WALL OF UPPER TRAY
┌─────────────────────────────────────────────────────────────┐
│ ┌────────────┐     ┌────────┐      ┌──────────────────────┐ │
│ │ 1. USB-C   │     │ 2. RGB │      │ 3. HD26 D-Sub Flange │ │
│ │    Service │     │    LED │      │    (Main Harness)    │ │
│ │    Alu Cap │     │    Ø3mm│      │    2x M3 Jackscrews  │ │
│ └────────────┘     └────────┘      └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 4.1 HD26 D-Sub Wall Flange (Main Vehicle Harness Interface)
* **Cutout Geometry:** D-Sub High-Density 26-pin cutout ($39.2 \times 15.4\,\text{mm}$) in the front face of the upper tray.
* **Flange Gasket:** Precision-molded EPDM flat gasket ($1.5\,\text{mm}$ thickness, Shore 60A) between the metal collar of the Amphenol LTW / NorComp SEAL-D socket and the enclosure wall.
* **Fastening:** 2x M3 stainless steel hex jackscrews with O-ring sealing washers clamp the flange with $0.6\,\text{Nm}$ torque for a watertight seal.
* **Internal Decoupling:** Connected to the main PCB via the 26-conductor ribbon cable looping through the mid-baffle slot to the 2x13 box header (`J1`).

### 4.2 Waterproof USB-C Programming & Service Port
* **Access without Opening Housing:** Located adjacent to the HD26 flange is the waterproof USB-C service port with a **blue anodized aluminum screw cap** and red NBR/silicone O-ring.
* **Function:** Facilitates on-vehicle firmware updates, ESP-IDF JTAG debugging, and diagnostics without opening the IP67 enclosure under the seat.

### 4.3 Waterproof RGB Status LED Window
* **Flush-Mounted PMMA Lens:** A diffuse PMMA lens body ($\varnothing\,3.0\,\text{mm}$, *Mentor 1292.1101*) is flush-pressed with a perimeter NBR O-ring into the front face of the upper tray and sealed with clear polyurethane.
* **Direct Line of Sight:** Displays the system status directly on the front panel, providing instant visibility to rider or mechanic when inspecting the connectors under the seat.

### 4.4 Status LED Color Code (State Machine)

| LED Color & Pattern | Operational State | Meaning |
| :--- | :--- | :--- |
| 🟢 **Green Pulsing (1 Hz)** | **Normal Operation (Online)** | Main power active, all plugged pods operational, DLE OK |
| 🔵 **Blue Blinking (2 Hz)** | **BLE Dashboard / Pairing** | WebApp PWA actively connected / data transfer |
| 🟡 **Yellow Pulsing (0.5 Hz)**| **UPS Battery Mode (KL15 OFF)**| Shutdown rundown: GPX Tour-Close & WebDAV upload |
| 🔴 **Red Fast Blinking** | **Warning / Error** | Starter battery under-voltage ($< 11.8\,\text{V}$) / Cartridge short |
| 🟣 **Solid Purple** | **OMM DLE Leader** | Current motorcycle is coordinating the group mesh |
| ⚪ **White Double Flash** | **Actioncam Marker** | Handlebar button pressed: GPS highlight marker saved |

---

## 5. Enclosure Lid: Rugged 100% Solid Protective Cover with Pressure Vent

The enclosure lid hermetically seals the upper tray. Since all electrical interfaces and the status LED are integrated into the upper tray front panel, the lid is designed as a **rugged, homogeneous protective cover** without fragile optical penetrations:

* **Dimensions & Wall Thickness:** $110.0 \times 74.0 \times 6.0\,\text{mm}$, $3.0\,\text{mm}$ continuous PA12 wall thickness.
* **Pressure Equalization:** A central Gore ePTFE screw vent ($\varnothing\,7.0\,\text{mm}$, M8 thread) reliably balances atmospheric pressure variations (mountain pass rides up to $3,000\,\text{m}$) and thermal breathing effects.
* **Hermetic Sealing:** Perimeter Shore 40A silicone profile seal in the lid groove, clamped with 4x M3 stainless steel screws into brass Ruthex threaded inserts in the lower hull.
* **Maintenance Advantage:** The lid can be removed effortlessly for battery service or inspection without disconnecting any cables or optical light pipes.

---


## 5. Enclosure Type B: Universal Satellite Pod (Identical for Pods 1, 2, and 3)

- **100% Universal Design:** All 3 pod locations on the motorcycle share the identical enclosure body scaled to the **Enlarged Universal Envelope ($135.0 \times 70.0 \times 38.0\,\text{mm}$)**.
- **Chamber Dimensions:** $120.0 \times 60.0 \times 30.5\,\text{mm}$ (PA12 MJF, $3.0\,\text{mm}$ wall thickness).
- **Electronics Cartridge / Sled:** $116.0 \times 58.0 \times 30.0\,\text{mm}$ (Usable interior volume: $110.0 \times 54.0 \times 28.0\,\text{mm}$ – guaranteed to fit commercial off-the-shelf OEM adapters like Sena +Mesh intact with internal antenna pigtails).

### 5.1 2-Piece Modular Cartridge Architecture (Universal Base Sled & Module Top Inlay)

To achieve maximum modularity at minimal manufacturing cost, each swappable cartridge is engineered as a **2-piece modular assembly**:

```
                      MODULAR 2-PIECE SWAPPABLE CARTRIDGE
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. INTERCHANGEABLE MODULE TOP INLAY (3D Contour Bed & Cradle):              │
│    • Specific for Sena 50S/60S, Cardo Air-Mount, or Midland XT30/PMR        │
│    • Integrated Pogo-pin contact array / N52 magnets / EPDM retention strap │
│    • 10.0 x 3.0 mm cable pass-through slot (R=1.0 mm) into under-bed channel│
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. ACOUSTIC TPU DAMPING INTERFACE (Shore 40A, 0.5 mm - Anti-Rattle Layer)   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. UNIVERSAL BASE SLED (Generic Carrier Chassis):                           │
│    • 100% identical across ALL headset and radio variants                   │
│    • Floor compartment for carrier PCB (openmotorbridge_pod_cartridge, 35x25)│
│    • Front seat for 6-pin socket J1 & axial JST-SH header J2 facing +X      │
│    • 1.5 mm deep under-bed cable channel & 4x M2 threaded brass inserts     │
│    • Poka-Yoke guide rails (1.5 / 2.0 mm) & dual snap-fit click latches     │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Structural Division & Sealing Concept:
1. **Universal Base Sled ($116.0 \times 58.0 \times 30.0\,\text{mm}$):**
   * Standard PA12 base chassis with lateral Poka-Yoke guide rails and snap-fit locking latches.
   * Houses the standardized $35.0 \times 25.0\,\text{mm}$ carrier PCB (`openmotorbridge_pod_cartridge`) with Maxim DS2401 ID chip and front 6-pin horizontal socket `J1`.
   * Integrates an **$1.5\,\text{mm}$ deep and $8.0\,\text{mm}$ wide under-bed cable channel** as well as 4x heat-set brass threaded inserts (*Ruthex M2*).
2. **Interchangeable Module Top Inlay (3D Contour Nest):**
   * Tailored to the specific intercom geometry (e.g. Sena 50S snap nest with latch, Cardo Packtalk Edge with dual N52 magnets, Midland XT30 clamp nest).
   * Features a **$10.0 \times 3.0\,\text{mm}$ pass-through slot** with $R=1.0\,\text{mm}$ filleted edges, routing the 6-conductor JST-SH ribbon cable directly from the under-bed channel to the solder pads of the contact field.
   * Fastened securely to the base sled with **4x M2 countersunk screws** (V4A stainless steel). When switching headset brands, the rider only replaces the 3D-printed top inlay—the electronic carrier board is retained.
3. **Enclosure Sealing Concept (Clarification on IP67 Sealing):**
   * **IP67/IP69K ingress protection is established at the front perimeter flange of the Pod enclosure:** The Shore 40A silicone profile seal on the cartridge faceplate hermetically seals the entire slide-in chamber against high-pressure water and dust upon latching.
   * Because the entire interior of the Pod chamber is **100% dry and protected during operation**, **no compression gasket is required between the cartridge base sled and top inlay**.
   * A thin $0.5\,\text{mm}$ Shore 40A TPU/silicone intermediate layer provides vibration isolation and prevents acoustic rattling under severe motorcycle road shocks.

```
                  ◄──────────── 64.0 mm Pod Width ────────────►
 ┌─────────────────────────────────────────────────────────────┐ ▲
 │                    3.0 mm Enclosure Lid                     │ │
 │ ┌───┬─────────────────────────────────────────────────┬───┐ │ │ 32.0 mm
 │ │   │                                                 │   │ │ │ Pod
 │ │3.0│      OPEN SLED CHAMBER (NO CARTRIDGE LID!)      │3.0│ │ │ Height
 │ │mm │      Full 23.5 mm internal height for antennas  │mm │ │ │
 │ │   │      Headset inlays & OMM transceiver modules   │   │ │ │
 │ │Key├───────────► ┌─────────────────────┐ ◄───────────┤Key│ │ │
 │ │1.5│             │  6-PIN SOCKET       │             │2.0│ │ │
 │ │mm │             │  (Piston Slide-In)  │             │mm │ │ │
 │ │   │             └─────────────────────┘             │   │ │ │
 │ └───┴─────────────────────────────────────────────────┴───┘ │ │
 │                    3.0 mm Enclosure Floor                   │ │
 └─────────────────────────────────────────────────────────────┘ ▼
```

#### Advantages of the Large-Format Open Sled:
1. **100% Generic Compatibility:** Fits all mainstream headset form factors (Sena 50S/60S, Cardo Packtalk Edge/Pro/Bold, Midland) as well as the standalone OpenMotorMesh transceiver module with GNSS and LoRa.
2. **No Double Wall Thickness:** No separate cartridge lid is needed. This saves plastic thickness and eliminates an insulating air gap.
3. **Full Usable Internal Height ($23.5\,\text{mm}$):** Massive headroom for $25 \times 25 \times 4\,\text{mm}$ GNSS ceramic patch antennas, helical LoRa coils, and tall headset components.
4. **Protection Provided by Pod Shell:** Once slid in, the solid, weatherproof PA12 top wall of the Pod enclosure ($3.0\,\text{mm}$) provides the outer protective envelope.

---

### 5.2 IP67 Perimeter Faceplate Gasket & Snap-Fit Click-Lock

```
    OUTSIDE (IP67)                            POD INSERTION BAY
┌─────────────────────────┐               ┌─────────────────────────────────┐
│ PA12 Faceplate          │  Perimeter    │ Open U-Carrier Sled             │
│ with Grip Ridge         ├── Flange ─────┤ with Carrier PCB & Module       │
│ Dual Snap-Fit Latches   │  Gasket       │ ──► Slides along Poka-Yoke keys │
│ (Tactile "Click")       │  (Shore 40A)  │ ──► Socket mates into Shroud    │
└─────────────────────────┘               └─────────────────────────────────┘
```

1. **Perimeter Faceplate Gasket (IP67 Seal):**
   * The outer faceplate of the sled features an integrated sealing groove with a **Shore 40A silicone profile gasket** ($1.5\,\text{mm}$ cord diameter).
   * When fully seated, the faceplate compresses the gasket against the Pod opening flange, sealing the entire bay **100% watertight and dustproof to IP67**.
2. **Dual Snap-Fit Quick-Release Latching (Click-Lock):**
   * Integrated POM/PA12 snap-fit clips on the sled side flanks engage with positive detents in the Pod enclosure upon reaching the mechanical end-stop.
   * Elastic compression of the silicone gasket maintains positive tension—**100% vibration-proof (> 20 g) and rattle-free**.
   * **Toolless Quick-Release:** Squeezing the two lateral buttons with thumb and index finger releases the latch for effortless removal.

---

### 5.3 Cartridge Carrier PCB (`openmotorbridge_pod_cartridge`) & 3D Board Renders

The universal cartridge carrier PCB forms the core of every removable cartridge. It acts as the mechanical and electrical bridge between the pod base and the internal headset cradle contacts:

#### Top View (Inlay Header, 1-Wire ID & Decoupling):
![OpenMotorBridge Cartridge Carrier PCB Top 3D Render](../../hardware/kicad_pod_cartridge/cartridge_3d_render_top.png)

#### Bottom View (6-Pin Socket Header for Direct Mating onto Pod Base):
![OpenMotorBridge Cartridge Carrier PCB Bottom 3D Render](../../hardware/kicad_pod_cartridge/cartridge_3d_render_bottom.png)

*Figure 5.1: Photorealistic 3D raytracing render of the Universal Pod Cartridge Carrier PCB (KiCad 8.0, 35.0 x 25.0 mm, ENIG Gold with downward-facing 6-pin socket on B.Cu, low-profile JST-SH 1.0 mm header on F.Cu, and Maxim DS2401 ID chip).*

#### Board Architecture:
* **Bottom Side (`B.Cu` – Interface to Pod Base):**
  * **6-Pin Female Socket Header (`J1` / PinSocket 2.54 mm):** Centered on the bottom face, opening straight downwards. When inserting the cartridge, the upward-pointing pins from the pod base slide directly and securely into this socket.
  * **Ground Plane (`GND Shield Plane`):** Solid copper fill for low-impedance RF shielding and mechanical support.
* **Top Side (`F.Cu` – Docking Interface & ID):**
  * **Low-Profile Inlay Header (`J2`):** 90° rotated **JST-SH 1.0 mm 6-Pin SMD connector** (only $1.8\,\text{mm}$ profile height). A short internal flex cable connects this header tool-free to the headset cradle contacts in the cartridge lid.
  * **Digital Cartridge ID Chip (`U1`):** **Maxim DS2401Z+** Silicon Serial ROM (SOT-23) providing a globally unique 64-bit ROM ID. The central box identifies the inserted headset profile within milliseconds (e.g. `sena_50_series.json`, `cardo_dmc_gen2.json`).
  * **Decoupling Capacitor (`C1`):** 100nF 0603 ceramic filter on the 1-Wire bus line.
* **Vibration Decoupling & Mounting (`H1`, `H2`):**
  * 2x M2 mounting insets with Shore 40A silicone bushings isolate the board against vehicle vibration up to $20\,\text{g}$.

---

### 5.4 Screwed-In Protective Bulkhead Cover with Integrated Auto-Eject Springs
* **Mechanical Touch Protection:** After seating the Pod Base PCB and torquing the M8 knurled lock nut, a **$2.0\,\text{mm}$ thick PA12 protective bulkhead plate** is fastened to internal housing bosses with two M2 countersunk screws.
* **Hermetic Isolation:** The bulkhead isolates the Pod Base PCB cavity (M8 solder joints, Littelfuse SP3012 TVS array, SMD filter capacitors) completely from the cartridge bay. Repeated sliding in/out of the cartridge cannot touch, scratch, or stress any components or solder pads.
* **Integrated Shroud Collar:** The bulkhead integrates the central PA12 protective shroud with $45^\circ$ self-centering funnel, ensuring zero pin bending risk.
* **Poka-Yoke Anti-Rotation PCB Protection (Mechanical Keying):**
  * All PCBs in the system are keyed to **fit in exactly one orientation only**:
    * **Cartridge PCBs (Pods 1, 2 & 3):** Cannot be installed backwards because the 6-pin interface is fixed at the leading front edge; a $180^\circ$ rotation would face the connector backwards into the cartridge body.
    * **Bulkhead Adapter PCB (`openmotorbridge_pod_base`):** To prevent an accidental $180^\circ$ upside-down assembly (which would reverse Pin 1 `VCC` with Pin 6 `1-WIRE_ID`), the board features an asymmetric **$4.0 \times 2.5\,\text{mm}$ keying notch** (`Edge.Cuts` at $X = 125 \dots 129\,\text{mm}$) on its bottom edge. A matching **PA12 alignment lug** on the housing floor engages positively into this notch. If placed upside down, the solid board edge hits the lug, causing the PCB to stick out cocked and preventing screw engagement.
* **Spring-Loaded Auto-Eject Mechanism:**
  * To the left and right of the protective shroud, **dual stainless steel (V4A 1.4310) compression springs** with guide pushers are housed in the bulkhead.
  * **On Insertion:** Sliding the cartridge sled in compresses the dual springs by $6.0\,\text{mm}$ until the 6-pin socket mates fully into the shrouded header and the snap-fit latches engage with a positive click. The compressed springs maintain continuous pre-tension against the silicone gasket—**100% vibration-proof and rattle-free**.
  * **On Release (Auto-Eject):** When the rider squeezes the two quick-release buttons on the faceplate, the snap-fit latches disengage, and **the dual springs pop the cartridge out by $8\dots 10\,\text{mm}$**.
  * Electrical contact is cleanly broken, and the rider can effortlessly pull the cartridge out even while wearing heavy winter motorcycle gloves without any jamming.

---

### 5.4.1 Detailed Mechanics & Kinematics of the Snap-Fit & Auto-Eject System

The quick-change cartridge system combines high-shock automotive latching (resistant up to $20\,\text{g}$) with intuitive, single-handed **Auto-Eject kinematics**:

```
                       AUTO-EJECT & SNAP-FIT KINEMATICS (TOP VIEW X-Y)
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ POD TUNNEL HOUSING (PA12, 100 x 60 mm)                                                       │
│                                                                                              │
│   ┌──────────────┐                                                     ┌─────────────────┐   │
│   │ Protective   │  ◄── V4A Ejection Spring (k = 1.2 N/mm)             │ Catch Pocket    │   │
│   │ Bulkhead     ├───[§§§§§§§§§]───────────────┐                       │ in Tunnel Wall  │   │
│   │ (x = 22 mm)  │   F_preload = 7.2 N         │                       │ (x = 86 mm)     │   │
│   │              │                             │                       │    ┌───────┐    │   │
│   │              │   6-Pin Gold-Plated         │ CARTRIDGE SLED BODY   │    │ 85°   │    │   │
│   │   ┌──────┐   │   Header Engagement         │ (openmotorbridge_     │    │ Tooth │    │   │
│   │   │6-Pin ├───┼════════════════════════════►│  cartridge_sled)      ├────┴┤ ▲    │    │   │
│   │   │Header├───┤   Wipe = 4.8 mm             │                       │  ┌──┘ │    └───┐│   │
│   │   └──────┘   │                             │                       │  │30° │        ││   │
│   │              │                             │                       │  │Ramp│        ││   │
│   │              ├───[§§§§§§§§§]───────────────┘                       │  └──┬─┘        ││   │
│   │              │  ◄── V4A Ejection Spring                            │     │          ││   │
│   └──────────────┘                                                     │  ┌──▼────────┐ ││   │
│                                                   Flexible PA12 Arm    │  │PUSH BUTTON│ ││   │
│                                                   (L=14 mm, b=10 mm) ──┴──┤ (Ribbed)  │ ◄┼───┼── Thumb/Finger
│                                                                           └───────────┘ ││   │   Squeeze (F_squeeze = 10 N)
│                                                                           FACEPLATE     ││   │
└─────────────────────────────────────────────────────────────────────────────────────────┴┴───┘
```

#### 1. 4-Phase Kinematic Operation:

1. **Phase 1: Slide-In & Alignment ($X = 0\dots 65\,\text{mm}$):**
   * Sled slides along the asymmetric tongue-and-groove rails (Poka-Yoke error-proofing prevents inverted insertion).
2. **Phase 2: Spring Compression & Lead-In ($X = 65\dots 74\,\text{mm}$):**
   * The front sled face contacts the two V4A coil springs on the bulkhead guide posts.
   * The $45^\circ$ alignment funnel guides the 6-pin socket over the pin header.
   * The $30^\circ$ ramps on the latch teeth ride over the inner pod wall, deflecting the cantilever arms inward by $1.8\,\text{mm}$.
3. **Phase 3: Positive Snap-Locking & Gasket Compression ($X = 75\,\text{mm}$ - Mated Position):**
   * The latch teeth snap outward into the $1.8\,\text{mm}$ deep catch pockets with a crisp, audible **"CLICK"**.
   * The dual springs are compressed by $\Delta x = 6.0\,\text{mm}$, exerting a continuous axial preload force of **$F_{\text{preload}} = 7.2\,\text{N}$**.
   * This preload compresses the perimeter silicone faceplate seal by $30\%$ $\rightarrow$ **Hermetic IP67/IP69K sealing with zero rattle under $20\,\text{g}$ shock**.
4. **Phase 4: Quick-Release Squeeze & Auto-Ejection ($8\dots 10\,\text{mm}$ Pop-Out):**
   * Rider pinches the two lateral ribbed push buttons on the faceplate.
   * Cantilever arms flex inward, clearing the $85^\circ$ retention teeth from the catch pockets.
   * Instant release of the compressed springs **pops the cartridge out by $8\dots 10\,\text{mm}$**.
   * The 6-pin contact ($4.8\,\text{mm}$ wipe) is completely disengaged; the cartridge is cleanly presented and easily extracted even with thick winter riding gloves.

#### 2. Mechanical Force Balance:

| Parameter | Symbol / Formula | Calculated Value | Function & Verification |
| :--- | :--- | :---: | :--- |
| **Combined Spring Rate** | $c_{\text{tot}} = 2 \times 1.2\,\text{N/mm}$ | **$2.4\,\text{N/mm}$** | Dual parallel V4A stainless compression springs |
| **Preload Compression Stroke**| $\Delta x_{\text{pre}}$ | **$6.0\,\text{mm}$** | Compressed from $L_0 = 15.0\,\text{mm}$ to $L_{\text{mated}} = 9.0\,\text{mm}$ |
| **Axial Preload Force** | $F_{\text{preload}} = c_{\text{tot}} \cdot \Delta x_{\text{pre}}$ | **$7.2\,\text{N}$** | Maintains constant contact & seal pressure under vibration |
| **Gasket Reaction Force** | $F_{\text{seal}}$ (Shore 40A Silicone) | **$4.5\,\text{N}$** | $30\%$ compression of $1.5\,\text{mm}$ silicone seal cord |
| **Retention Pullout Resistance**| $F_{\text{retention}} = 2 \times \frac{E I \delta}{L^3} \cdot \tan(85^\circ)$| **$> 65\,\text{N}$** | Prevents accidental release from cable tension |
| **Squeeze Release Force** | $F_{\text{squeeze}} = 2 \times \frac{3 E I \delta}{L^3}$ | **$9.8\,\text{N}$** | Ergonomic single-handed thumb/index pinch force ($\approx 1\,\text{kg}$) |
| **Automatic Ejection Stroke** | $\Delta x_{\text{eject}} = L_0 - L_{\text{mated}}$ | **$9.0\,\text{mm}$** | Fully clears $4.8\,\text{mm}$ pin wipe with **$+4.2\,\text{mm}$ overstroke** |

#### 3. Cantilever Beam Stress & Fatigue Life:
* **Cantilever Dimensions:** Length $L = 14.0\,\text{mm}$, width $b = 10.0\,\text{mm}$, thickness $h = 1.8\,\text{mm}$.
* **Maximum Surface Strain:**
  $$\epsilon_{\max} = \frac{3 \cdot h \cdot \delta}{2 \cdot L^2} = \frac{3 \cdot 1.8\,\text{mm} \cdot 1.8\,\text{mm}}{2 \cdot (14.0\,\text{mm})^2} = \frac{9.72}{392} \approx 0.0248 \implies \mathbf{1.38\% \text{ at full deflection}}$$
* **Allowable Elastic Strain (PA12 MJF):** $\epsilon_{\text{allow}} \le 2.0\%$.
* **Bending Stress:** $\sigma_b = \epsilon \cdot E_{\text{PA12}} = 0.0138 \times 1,700\,\text{MPa} = \mathbf{23.5\,\text{MPa}}$ (Well below the $48\,\text{MPa}$ yield strength $\rightarrow$ **Safety Factor $S = 2.04$**).
* **Result:** Designed for $> 10,000$ insertion and release cycles without plastic deformation or fatigue failure.

---

### 5.5 Central Pod Pressure Equalization Membrane (ePTFE on Long Top Roof)
* **Thermal & Pressure Cycling:** Internal heat dissipation (SX1262 LoRa $+22\,\text{dBm}$ PA, charging circuits) and solar exposure cause air expansion/contraction inside the Pod.
* **Central Top Placement:** Located centrally on the **long top enclosure roof** ($X = 0.0\,\text{mm}, Y = 0.0\,\text{mm}$) inside a recessed pocket is a **$\varnothing\,7.0\,\text{mm}$ ePTFE vent membrane** (*Schreiner Air Vent* / *Gore Automotive Adhesive Vent*).
* **Function:** Airflow $> 25\,\text{ml/min}$ at $70\,\text{mbar}$, water intrusion pressure $> 1.5\,\text{bar}$ (IP67). Prevents internal vacuum and water ingestion during sudden rainstorms and provides symmetric breathing across the internal chamber.

---

### 5.6 IP67 Dummy Cartridge (Blank Sled)
* **Partial Fitment:** If a pod bay is temporarily unused, the identical **IP67 Dummy Cartridge (`Pod_Dummy_Cartridge_IP67.stl`)** seals the opening.
* **Sealing:** Integrated perimeter silicone faceplate gasket protects internal contacts from road salt and water spray.
* **Latching:** Employs the same dual snap-fit quick-release latching mechanism.
* **Firmware State:** Main box detects the open slot and isolates it via `disabled.json`.

---

### 5.7 Pod Base PCB (`openmotorbridge_pod_base`) & Centric Cartridge Guide
┌─────────────────────────────────────────────────────────────────────────┐
│ CARTRIDGE (e.g. "Sena 50S" or "Cardo Edge Edition")                     │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ DOCKING CRADLE & 3D CONTOUR NEGATIVE NEST                         │  │
│  │ (Rider snaps their OEM headset into this cradle)                  │  │
│  │                                                                   │  │
│  │  [ OEM Spring Contacts / Pogo Pins ]                              │  │
│  └──────────────────────────┬────────────────────────────────────────┘  │
│                             │ Protected JST-SH Cable Channel            │
│                             │ (1.5mm under-bed recess)                  │
│                             ▼                                           │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ CARTRIDGE CARRIER PCB (60x36mm)                                   │  │
│  │  - J2: JST-SH 6P Header (Top side F.Cu)                           │  │
│  │  - U1: DS2401 ID Chip (Reports device type to ESP32)              │  │
│  │  - F1: 500mA PTC Fuse & D1: Green Power LED                       │  │
│  │  - J1: 6-Pin Socket (Centered Front Edge B.Cu)                    │  │
│  └──────────────────────────┬────────────────────────────────────────┘  │
└─────────────────────────────┼───────────────────────────────────────────┘
                              ▼ (Horizontal slide-in)
┌─────────────────────────────┼───────────────────────────────────────────┐
│ POD BASE PCB                │                                           │
│  - J1: 6-Pin Pin Header ◄───┘ (Inner End-Wall, Centered)                │
│  - U1: SP3012 TVS Protection Matrix                                     │
│  - J2: Centered M8 6-Pin IP67 Receptacle (Bottom side)                  │
└─────────────────────────────┬───────────────────────────────────────────┘
                              ▼
     M8 PUR Harness to Motorcycle / Central Box
```

#### 5.2.1 Protected Internal JST-SH Cable Routing & Pin-Mapping

To route all analog audio, microphone, power, and PTT signals from the right-angle **JST-SH 1.0 mm 6-Pin SMD header (`J2`)** on the carrier PCB to the cradle contact array without pinching or soldering hassles:

1. **Protected Under-Bed Routing Channel:**
   * A **$1.5\,\text{mm}$ deep and $8.0\,\text{mm}$ wide recessed conduit** is molded/machined into the floor of the PA12 sled directly beneath the 3D contour negative nest.
   * The ultra-flexible, silicone-insulated 6-conductor JST-SH ribbon cable rests fully recessed beneath the TPU damping liner, protected against wear and accidental pinching.
2. **Standardized JST-SH 6P Header (`J2`) Pinout:**

| Pin | Signal Name | Headset Adapter Function | Sena 50S/60S Pad | Cardo Edge Pad | Midland XT / PMR |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | `GND` | Common Ground Reference | Pin 1 (GND) | Pin 1 (GND) | Ground / Shield |
| **2** | `5V_VBUS` | Filtered 5V Charge Rail (500mA PTC) | Pin 2 (USB-5V) | Pin 2 (5V Charge)| 5V DC In |
| **3** | `AUDIO_R+` | Audio Diff-Out + (to Headset Speaker In) | Pin 4 (Spk R+) | Pin 3 (Spk +) | Speaker In + |
| **4** | `AUDIO_R-` | Audio Diff-Out - (Speaker Return) | Pin 5 (Spk R-) | Pin 4 (Spk -) | Speaker In - |
| **5** | `MIC_IN+` | Audio Diff-In + (from Headset Mic Out) | Pin 6 (Mic +) | Pin 5 (Mic +) | Mic Out + |
| **6** | `OPTO_PTT` | Optocoupler PTT / Button Synthesis | Pin 7 (Mesh-Btn)| N/C (Aux) | PTT Switch |

3. **Termination on the 3 Target Adapters:**
   * **Sena 50S / 60S:** The JST-SH ribbon solders/crimps to the base of the gold-plated 7-pin pogo pin strip inside the contour nest.
   * **Cardo Packtalk Edge / Pro:** The JST-SH ribbon terminates at the underside of the 5 Air Mount spring contact pads.
   * **Midland XT / PMR446:** Plugs via a 4-pin micro header directly into bare PMR transceiver boards or solders to the waterproof 2-pin ($2.5\,\text{mm} + 3.5\,\text{mm}$) audio jack.

#### Modular Cartridge Variants (Community & 3D Print Designs):
1. **Sena 50S / 60S / 30K / 20S EVO Edition:** Integrates the OEM clamp-kit spring contact array. The unit simply clicks into place from above.
2. **Cardo Packtalk Edge / Pro Edition:** Integrates the magnetic *Air Mount* contact pads for tool-free docking.
3. **Cardo Packtalk Bold / Black Edition:** Uses the slide-in contacts of the Cardo audio-kit cradle.
4. **Midland Intercom Edition (BT Mini / BTR1 Advanced / Rush / Wave):** Docking cradle for Midland Bluetooth and Wave-Mesh intercoms ($70\dots 85\,\text{mm}$ chassis width).
5. **Midland XT / Compact PMR446 Bare-Board Edition:** Houses the stripped bare PCB of a compact Midland PMR walkie-talkie (e.g. XT10/XT30/G5, $\approx 68 \times 42 \times 10\,\text{mm}$ without battery bay) directly inside the sled. Powered via 5V bus, PTT triggered via PhotoMOS optocoupler.
6. **Embedded PMR446 Transceiver Edition (SA818S / RDA1846):** Fully integrated 500mW PMR446 transceiver module ($38 \times 20\,\text{mm}$) directly on the carrier PCB – with internal 446 MHz helical coil or rugged SMA front jack.
7. **PMR446 Dual-Jack Adapter Edition:** Weatherproof Midland/Kenwood 2-Pin socket ($2.5\,\text{mm} + 3.5\,\text{mm}$) on the cartridge faceplate for connecting external handheld radios (Midland G9 Pro / G13).
8. **Sena +Mesh & MeshPort Edition (Off-the-Shelf Slide Mount & SMA Bulkhead):**
   * **100% Non-Destructive Use of Unmodified OEM Hardware:** The Sena +Mesh adapter remains in its factory original enclosure (zero warranty voiding, no opening or soldering required).
   * **Sena-Compatible 3D Slide-Mount Inlay:** The cartridge top inlay replicates the exact geometry of the original Sena motorcycle frame mounting plate:
     * **2x Transverse Slide Guide Rails (Short-Axis Slide Travel):** Mates with the dual sliding hooks on the rear of the +Mesh housing (hooks spaced ~30 mm apart along length, each ~20 mm long parallel to the short axis). The +Mesh slides crosswise into positive lock.
     * **Integrated Resilient Latch Trigger (Auslöser):** Snaps audibly behind the catch notch at transverse end-stop; manually released via fingertip pressure on the release paddle.
     * **2x End Retention Hooks:** Accommodate the original Sena EPDM rubber tension strap for dual redundant anti-vibration locking against severe road shock.
   * **RF Antenna Interface (SMA Bulkhead Double-Socket on Faceplate):**
     * Waterproof **SMA flange bulkhead with O-ring** integrated into the cartridge front faceplate.
     * **Internal:** Short, flexible RG178 coaxial pigtail with $90^\circ$ elbow connector ($R \ge 12\,\text{mm}$) routes cleanly to the antenna port of the Sena +Mesh.
     * **External:** Standardized gold-plated SMA female thread. Connects either to an ultra-compact 2.4 GHz stub antenna ($25\dots 30\,\text{mm}$) or a low-loss extension cable leading to the cockpit windshield or rear fairing.
     * **Protection When Unused:** Waterproof silicone/rubber sealing plug (or threaded brass O-ring cap) protects against moisture and road grime.
   * **Electrical Power Supply (90° Micro-USB / USB-C Ribbon Pigtail):**
     * Routed from Pin 1 (`GND`) and Pin 2 (`5V_VBUS`) of the JST-SH header `J2` in the under-bed channel directly into the side charging port of the +Mesh.
     * Central controller manages power with inrush-limiting, automatic sleep-tier transitions, and starter battery protection. Audio is bridged wirelessly via Bluetooth to the helmet (audio pins 3–6 on `J2` remain N/C).

---

### 5.3 Detailed Fixing Mechanisms: 3D Contour Negative Nesting & EPDM Retention Strap

To ensure 100% vibration-proof, play-free, and tool-free retention ($> 20\,\text{g}$ motorcycle rating), each cartridge sled integrates a **3-tier locking architecture**:

```
 ┌─────────────────────────────────────────────────────────────┐
 │       ELASTIC EPDM RETENTION STRAP WITH QUICK-PULL TAB      │ ◄─── Continuous downward clamping
 └──────────────────────────────┬──────────────────────────────┘
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │        ORIGINAL HEADSET (SENA 50S / CARDO EDGE / MIDLAND)   │
 └──────────────────────────────┬──────────────────────────────┘
                                ▼ (Form- & Force-Fit)
 ┌─────────────────────────────────────────────────────────────┐
 │ 3D CONTOUR NEGATIVE NEST (Exact negative of device rear)    │ ◄─── 100% play-free X/Y centering
 │  • Vibration-damped TPU/NBR liner (Shore 40A, 0.8 mm)       │
 │  • Integrated OEM snap latch / Neodymium disc magnets       │
 └─────────────────────────────────────────────────────────────┘
```

![OpenMotorBridge Modular Cartridge Variants CAD Trio](../images/cad/cartridge_variants_trio.png)

*Figure 5.2: 3D CAD visualization of the 4 modular swappable cartridge variants inside the universal base sled ($75 \times 54 \times 20.5\,\text{mm}$): OMM Rear Transceiver with GNSS & LoRa (front left), Sena 50S/60S Quick-Snap Cradle (front right), Cardo Magnetic Air Mount (rear left), and waterproof IP67 dummy cartridge / Dry Box (rear right).*

#### 1. Sena 50S / 60S Contour Nest & Snap-Cradle
![OpenMotorBridge Sena 50S Cartridge Assembly 3D CAD Fitting](../images/cad/sena_cartridge_assembly_cad.png)

*Figure 5.3: 1:1:1 Euclidean scale 3D CAD visualization of the Sena 50S/60S 2-piece modular cartridge inside the Satellite Pod. Highlights the universal base sled with adapter PCB (50x22 mm), 1.5 mm under-bed routing channel, interchangeable 3D contour top nest with Jog-Dial lock, and EPDM retention strap.*

* **3D Contour Nest:** Sled floor forms an exact 3D negative of the Sena intercom bottom shell ($4.0\,\text{mm}$ deep recess, zero play along X and Y).
* **OEM Snap Retention:** Positive lower retention lip ($4.0\,\text{mm}$ Bottom Hook) and upper spring-loaded POM latch (Top Release Latch).
* **Elastic EPDM Retention Strap:** $12\,\text{mm}$ wide UV-resistant EPDM strap arches across center body, pulling the Sena firmly into the contour nest.
* **Electrical Interface:** 7-pin gold-plated spring Pogo array at $X = +22.0\,\text{mm}$ contacts the Sena gold pads; JST-SH 6P flat ribbon cable routes via under-bed channel to carrier PCB (`openmotorbridge_pod_cartridge`).

#### 2. Cardo Packtalk Edge / Pro Magnetic Air Mount & Contour Nest
![OpenMotorBridge Cardo Packtalk Edge Cartridge Assembly 3D CAD Fitting](../images/cad/cardo_cartridge_assembly_cad.png)

*Figure 5.4: 1:1:1 Euclidean scale 3D CAD visualization of the Cardo Packtalk Edge 2-piece modular cartridge inside the Satellite Pod. Features N52 neodymium disc magnet seat (Ø8x2 mm), 5-pin spring contact pad array at X = +10 mm, and protected under-bed cable channel.*

* **3D Contour Nest:** Replicates the curved underside of the Packtalk Edge with $0.8\,\text{mm}$ Shore 40A vibration isolation lining.
* **Dual N52 Magnet Array & Locking Jaws:** Two N52 neodymium disc magnets ($2\times \varnothing\,8 \times 2\,\text{mm}$ at $X = -8\,\text{mm}$ and $X = +28\,\text{mm}$) provide $> 120\,\text{N}$ retention force in combination with lateral snap-lock flanks.
* **Elastic EPDM Retention Strap:** Provides fail-safe mechanical retention under high offroad shocks.
* **Electrical Interface:** 5-pin spring contact array at $X = +10.0\,\text{mm}$ contacts audio, mic, and 5V charge rails.

---

### 5.3.1 Mechanical & Electrical Longitudinal Cross-Section (Tolerance & Clearance Stack-Up)

![OpenMotorBridge Sena & Cardo Cartridges Longitudinal Cross Section](../images/cad/sena_cardo_cartridge_cross_section.png)

*Figure 5.4: True-to-scale 2D longitudinal cross-section (X-Z plane) comparing Sena 50S (top) and Cardo Packtalk Edge (bottom) swappable cartridges inside the closed Pod enclosure. Shows the 2-piece sandwich stratification, axial JST-SH cable exit (+X), M2 fastening planes, and exact axial centering of the 6-pin interface on Y=0, Z=0.*

<!-- replaced -->
 & Snap-Cradle
* **3D Contour Negative Nest:** The sled floor is precision-contoured as the exact 3D negative matching the curved underside of the Sena 50S/60S. The device recesses $4.0\,\text{mm}$ into the pocket, physically locking out any $X/Y$ shifting.
* **OEM Snap-Fit Docking Latch:** Lower $4.0\,\text{mm}$ retention hook (*Bottom Hook*) and upper spring-loaded POM release latch (*Top Release Latch*) lock the device with an audible click.
* **Elastic EPDM Retention Strap:** A $12\,\text{mm}$ wide, UV- and ozone-resistant EPDM rubber strap stretches across the device center, locking into side T-anchor pins. It exerts constant downward pre-tension – **zero vibration or rattling even on harsh off-road washboard tracks**.
* **Electrical Interface:** Gold-plated 7-pin spring pogo pin array directly engages the OEM Sena contact pads; short JST-SH 6P ribbon connects to the cartridge carrier board (`openmotorbridge_pod_cartridge`).

#### 2. Cardo Packtalk Edge / Pro Magnetic Air Mount & Contour Nest
* **3D Contour Negative Nest:** Seamlessly mirrors the sleek aerodynamic curvature of the Packtalk Edge with an integrated $0.8\,\text{mm}$ Shore 40A silicone damping liner.
* **Dual N52 Magnetic Attraction & Side Jaws:** Two embedded N52 neodymium disc magnets ($2\times \varnothing\,8 \times 2\,\text{mm}$) snap the unit into the contour pocket. Dual lateral PA12/POM jaws latch into the Cardo side recesses ($> 120\,\text{N}$ retention force).
* **Elastic EPDM Retention Strap:** Provides supplemental downward retention for extreme enduro/gravel vibration profiles.
* **Electrical Interface:** 5-pin spring contact pads mate with the Cardo audio/power pads with zero friction.

#### 3. Midland BTR1 Advanced & XT30 Dovetail Slide / Contour Clamp
* **For Midland Intercoms (BTR1 Advanced / Rush / Wave):**
  * **Dovetail Slide Rail:** Intercom unit slides smoothly from above into the $72\,\text{mm}$ dovetail channel.
  * **Spring-Locking Tooth & Strap:** A spring-loaded tooth clicks into the base recess; the EPDM strap secures the unit downward.
* **For Midland XT Series & Bare-Board PMR446 (XT10 / XT30 / G5 stripped):**
  * **4-Point Silicone Damped Contour Bed:** The stripped board ($\approx 68 \times 42 \times 10\,\text{mm}$) rests inside a dedicated milled/printed contour pocket on 4 silicone standoffs, secured by 2x M2 clamp screws and the EPDM rubber strap.
  * **Antenna Options:** Internal $32\,\text{mm}$ 446 MHz helical coil inside the sled or an external SMA jack on the cartridge faceplate. Direct solder or JST header to carrier PCB.

---

### 5.5 Pod Pressure Equalization Membrane (ePTFE)
* **Problem:** Internal thermal dissipation (SX1262 LoRa $+22\,\text{dBm}$ PA, charging circuits) and direct solar radiation create pressure differentials in small pod volumes.
* **Specification:** The center of the top housing wall ($X=0, Y=0$) integrates an **adhesive $\varnothing\,7.0\,\text{mm}$ ePTFE venting membrane** (*Schreiner Air Vent* / *Gore Automotive Adhesive Vent*).
* **Function:** Airflow $> 25\,\text{ml/min}$ @ 70 mbar, water intrusion pressure $> 1.5\,\text{bar}$ (IP67). Eliminates vacuum-induced moisture ingress during sudden rain cooling.

---

### 5.6 Monolithic PA12 Precision Linear Guide & Contact Wipe Reliability

Because the Satellite Pods operate with ultra-low thermal dissipation (Pods 1 & 2: $< 50\,\text{mW}$; Pod 3: max. $0.56\,\text{W}$ within an internal air volume $> 85\,\text{cm}^3$), add-on metallic heat pipes or copper sliding strips are physically redundant. The architecture relies on a **100% monolithic, corrosion-free PA12-on-PA12 precision linear slide track**:

```
                 POD BAY & CARTRIDGE INTERFACE (X-Z SECTION)
┌─────────────────────────────────────────────────────────────────────────────┐
│ HOUSING ROOF (PA12 MJF, 2.5 mm Nominal Wall Thickness)                      │
├───────────────────────────────┬─────────────────────────────────────────────┤
│ 1. POD BASE PCB               │ 3. SWAPPABLE CARTRIDGE SLED                 │
│    (openmotorbridge_pod_base) │    (openmotorbridge_pod_cartridge)          │
│                               │                                             │
│    ┌──────────┐  4.8 mm Wipe  │  ┌───────────┐                              │
│    │ 6-Pin    ├═══════════════╪═►│ 6-Pin     │                              │
│    │ Pin-Array│   Engagement  │  │ Socket-   │                              │
│    │ (L=6.5mm)│ (Gold Au/Ni)  │  │ Header    │                              │
│    └────┬─────┘               │  └─────┬─────┘                              │
│         │                     │        │                                    │
│    ┌────▼─────────────────────┴────────▼─────┐                              │
│    │ Bulkhead Shroud & Auto-Eject Springs    │ ◄── 7.2 N Constant Preload
└────┴─────────────────────────────────────────┴──────────────────────────────┘
```

#### 1. Detailed Pin Length & Contact Wipe Engagement Calculations:
* **Connector Pair:** 6-Pin Precision Square Pin Header (`J1` Pod Base) $\leftrightarrow$ 6-Pin Precision Socket Header (`J1` Cartridge) on $2.54\,\text{mm}$ pitch with $0.76\,\mu\text{m}$ ($30\,\mu\text{in}$) hard gold plating over nickel (Au/Ni).
* **Dimensional Relationships:**
  * **Free Pin Length ($L_{\text{pin}}$):** Gold-plated square pins ($0.64 \times 0.64\,\text{mm}$) extend $6.5\,\text{mm}$ forward from the bulkhead shroud mounting plane.
  * **Socket Cavity Depth:** The mating precision female socket on the cartridge PCB features an internal contact cavity depth of $6.2\,\text{mm}$.
  * **Effective Contact Wipe Engagement:** In the fully latched operating position, the pins penetrate **$4.8\,\text{mm}$ deep into the dual-beam phosphor bronze contact springs**.
  * **Safety Margin vs. Automotive Standards:** Standards like *USCAR-2 / IEC 60603* require a minimum contact wipe of $\ge 1.5\,\text{mm}$ for automotive vibration environments. With **$4.8\,\text{mm}$** of continuous wipe, our design exceeds the automotive requirement by a **factor of 3.2**.
* **Zero Contact Chatter Under High Vibration (> 20 g):**
  * Dual V4A stainless steel springs in the bulkhead exert **$7.2\,\text{N}$ of continuous axial pre-load** against the POM snap-fit latch tabs.
  * The front silicone flange gasket is maintained at $30\%$ continuous compression.
  * Relative axial movement or micro-arcing across road bumps and engine vibrations is mechanically prevented.

#### 2. Friction & Wear Profile of the PA12 Slide Track:
* **Low-Friction Self-Lubricating Behavior:** Chemical vapor-smoothed PA12 exhibits a low dynamic friction coefficient ($\mu \approx 0.15\dots 0.20$).
* **Guide Clearances:** Nominal clearance between the asymmetrical tongue rails ($2.6\,\text{mm}$) and the housing grooves ($3.0\,\text{mm}$) is $0.2\,\text{mm}$ per side — ensuring precise alignment while tolerating fine dust particles without binding.
* **Service Life:** Rated for $> 1,000$ tool-free cartridge insertion cycles with zero measurable polymer wear.

### 5.7 IP67 Dummy Cartridge (`Pod_Dummy_Cartridge_IP67.stl`)

When a pod bay is temporarily unpopulated (e.g. single-intercom configurations, seasonal winter storage of headsets, or maintenance), the form-identical **IP67 Dummy Cartridge** hermetically seals the bay:

![OpenMotorBridge IP67 Dummy Cartridge 3D CAD Render](../images/cad/dummy_cartridge_cad.png)

#### Mechanical Specification & Sealing Architecture:
* **100% Form-Identical Sled Body ($92.0 \times 54.0 \times 23.5\,\text{mm}$):**
  * Glides with zero play on the same lateral slide tracks as active cartridges.
  * Completely closed, ergonomic faceplate ($58.0 \times 28.0 \times 5.0\,\text{mm}$) featuring textured finger-grip knurling and a centered pull recess.
* **Hermetic IP67 / IP69K Perimeter Gasket:**
  * A high-compliance silicone / EPDM profile gasket is nested within a $2.5\,\text{mm}$ deep groove behind the front collar.
  * When clicked into lock, the gasket compresses by 30%, sealing internal contacts permanently against road grime, pressure washers, and salt spray.
* **Dual Side Snap-Fit Latches & Auto-Eject:**
  * Uses the identical PA12/POM side latches. Depressing the dual side buttons triggers the internal bulkhead ejection springs to automatically pop the cartridge out $10\,\text{mm}$.
* **Integrated Waterproof Utility Dry-Storage Compartment:**
  * Since no electronics or battery are required, the hollow cavity serves as an **IP67 waterproof $80 \times 46 \times 16\,\text{mm}$ dry storage box** (with snap-lock lid) for emergency cash, vehicle registration copy, Allen key, or spare O-rings.
* **Electrical System State:**
  * Pure mechanical seal without PCB assembly. The bulkhead pin header remains safely isolated inside its protective collar.
  * The ESP32-S3 host detects the open 1-Wire bus (timeout) and automatically invokes `disabled.json` (audio relays high-Z isolated, 5V charge rail unpowered).

---

### 5.8 Pod Base PCB (`openmotorbridge_pod_base`) & Centric Cartridge Guide

The mechanical and electrical interface from the interchangeable cartridge to the M8 wiring harness is governed by the centered **Pod Base PCB (`openmotorbridge_pod_base`)**:

#### Top View (Vertical/Horizontal 6-Pin Header & SP3012 TVS Protection Stage):
![OpenMotorBridge Pod Base PCB Top 3D Render](../../hardware/kicad_pod_base/pod_base_3d_render_top.png)

#### Bottom View (Centered M8 6-Pin IP67 Receptacle & GND Shield Plane):
![OpenMotorBridge Pod Base PCB Bottom 3D Render](../../hardware/kicad_pod_base/pod_base_3d_render_bottom.png)

* **Dimensions:** $36.0 \times 20.0\,\text{mm}$ (Compact 2-layer FR4 base board with $4.0 \times 2.5\,\text{mm}$ Poka-Yoke keying notch at bottom edge).
* **Poka-Yoke Alignment:** Asymmetric keying notch on bottom edge (`Edge.Cuts` at $X = 125 \dots 129\,\text{mm}$) mates with the corresponding alignment lug on the enclosure floor, physically blocking $180^\circ$ upside-down mounting.
* **Centered 6-Pin Header (`J1`) with PA12 Protective Shroud:** 6-pin precision pin array ($2.54\,\text{mm}$ pitch, gold-plated) positioned at the exact geometric center line ($Y=0, Z=0$).
* **Integrated PA12 Protective Shroud & Lead-in Funnel:** The protective bulkhead forms a **4-sided, $1.2\,\text{mm}$ thick protective collar with $45^\circ$ self-centering lead-in chamfers** surrounding `J1`. The female socket header on the cartridge slides snugly into this shroud like a piston, fully encapsulating the pins against manual touching or mechanical bending.
* **Integrated ESD Protection Array (`U1`):** **Littelfuse SP3012-06UTG** (6-channel TVS diode array with $< 0.5\,\text{pF}$ parasitic capacitance) shunts ESD strikes upon pin contact directly to chassis ground.
* **Centered M8 Receptacle (`J2`):** Metal-shielded **M8 6-Pin A-Coded IP67 Receptacle** (IEC 61076-2-104) with solid mounting base and threaded barrel soldered at the exact geometric center of the bottom layer (`B.Cu`).
* **Mechanical Damping & Mounting (`H1`, `H2`):** 2x M2 mounting holes with Shore 40A silicone dampening bushings against road vibrations. Insertion forces are absorbed 100% by the PA12 housing end-stop.

---

### 5.8 Centric Slide-in Bay & Poka-Yoke Alignment Architecture

To eliminate tilting, asymmetric lever forces, and reverse insertion, the cartridge chamber is **100% centric across all spatial axes**:

```
                  ◄──────────── 64.0 mm Pod Width ─────────────►
 ┌─────────────────────────────────────────────────────────────┐ ▲
 │                     3.0 mm Housing Top                      │ │
 │ ┌───┬─────────────────────────────────────────────────┬───┐ │ │ 32.0 mm
 │ │   │                                                 │   │ │ │ Pod
 │ │3.0│          CENTRIC CARTRIDGE SLIDE-IN BAY         │3.0│ │ │ Height
 │ │mm │                   (56 x 24 mm)                  │mm │ │ │
 │ │   │                                                 │   │ │ │
 │ │Key├───────────► ┌─────────────────────┐ ◄───────────┤Key│ │ │
 │ │1.5│             │  6-PIN CONNECTOR    │             │2.0│ │ │
 │ │mm │             │  (Exact Center)     │             │mm │ │ │
 │ │   │             └─────────────────────┘             │   │ │ │
 │ └───┴─────────────────────────────────────────────────┴───┘ │ │
 │                    3.0 mm Housing Floor                     │ │
 └─────────────────────────────────────────────────────────────┘ ▼
```

#### 3D CAD Cross-Section View of Poka-Yoke Asymmetrical Guide Rails:

![OpenMotorBridge Pod Poka-Yoke Asymmetrical Guide Rails 3D Cross Section](../images/cad/pod_poka_yoke_cross_section_cad.png)

*Figure 5.6: 3D CAD transverse cross-section (Y-Z plane) through the Satellite Pod housing and inserted swappable cartridge sled. Clearly highlights the $6.0\,\text{mm}$ vertical height offset of the guide tracks (Left: $Z=8.2\,\text{mm}$, Right: $Z=14.2\,\text{mm}$) with precision tongue-and-groove slide fit and centered 6-pin contact plane.*

#### 4-Stage Safety Architecture for Perfect Alignment:
1. **Fully Centric Geometry:**
   * **Width ($Y$):** $64.0\,\text{mm}$ pod width and $56.0\,\text{mm}$ bay width yield symmetric **$3.0\,\text{mm}$ side walls**.
   * **Height ($Z$):** $32.0\,\text{mm}$ pod height and $24.0\,\text{mm}$ bay height yield symmetric **$3.0\,\text{mm}$ top/bottom walls**.
   * Connector sits at the intersection of symmetry axes $\rightarrow$ **Zero torque or lever strain**.
2. **Poka-Yoke Asymmetric Keying Grooves:**
   * Left guide rail: $1.5\,\text{mm}$ width.
   * Right guide rail: $2.0\,\text{mm}$ width.
   * Inverted (upside-down) insertion is physically impossible.
3. **$45^\circ$ Self-Centering Funnel:**
   * The cartridge nose features a $45^\circ$ lead-in bevel with a $\pm 1.5\,\text{mm}$ capture zone. Pins align smoothly before electrical contact.
4. **Positive Mechanical Stop & Auto-Eject:**
   * Insertion force is arrested by the solid PA12 bulkhead – zero stress is transmitted to PCB solder joints. The dual V4A springs maintain continuous pre-tension and pop the sled out by $10\,\text{mm}$ upon release.

```
┌─────────────────────────────────────────────────────────────────────────┐
│               POD BASE & CARTRIDGE INTERFACE PROGRESSION                │
├─────────────────────────────────────────────────────────────────────────┤
│ 1. CARTRIDGE SLED DOCKING CRADLE:                                       │
│    • Original headset (Sena 50S/60S / Cardo Edge) clicked in tool-free  │
│    • Internal JST-SH 6P ribbon cable to Cartridge Carrier PCB           │
│                               ▼                                         │
│ 2. CARTRIDGE CARRIER PCB (openmotorbridge_pod_cartridge, 60x36mm):      │
│    • DS2401 1-Wire ID ROM (identifies headset model to ESP32 host)      │
│    • 500mA PTC resettable fuse + green 5V power status LED              │
│    • Centered 6-pin precision socket at leading edge                    │
│                               ▼ (Horizontal cartridge slide-in)         │
│ 3. POD BASE PCB (openmotorbridge_pod_base, 48x24mm):                    │
│    • Centered 6-pin pin header on inner end-wall                        │
│    • Integrated ESD TVS array (Littelfuse SP3012, 6x TVS < 0.5pF)       │
│    • Centered M8 6-pin A-coded IP67 receptacle on outside (B.Cu)        │
│                               ▼ (M8 external thread facing outward)     │
│ 4. MODULAR M8 PANEL RECEPTACLE (Housing underside):                     │
│    • M8 6-pin A-coded IP67 receptacle with Poka-Yoke keyway             │
│    • Solid metal shield collar for 360° EMI shielding                   │
│                               ▼                                         │
│ 5. MODULAR M8-TO-M8 PUR HARNESS (0.5m .. 2.0m):                         │
│    • Shielded 6-conductor PUR cable (Halogen-free, oil- & UV-resistant) │
│    • 2x Power (0.34 mm²) + 2x Audio/UART twisted (0.14 mm²) + 2x Signal │
│    • Dual M8 6-Pin IP67 male plugs with vibration ratchet               │
│                               ▼                                         │
│ 6. CENTRAL BOX HD26 BREAKOUT PIGTAIL (Under Seat):                      │
│    • 3x M8 6-Pin sockets (Pod 1 Left, Pod 2 Right, Pod 3 Rear)          │
│    • 1x M8 4-Pin / Superseal (Vehicle power KL30/KL15/GND/Shield)       │
│    • 1x M8 4-Pin (CAN-Bus telemetry & front ambient microphone)         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.9 3D X-Ray CAD Architecture & Exploded Assembly View

To holistically verify mechanical clearances, sealing boundaries, and electrical transitions, the complete assembly of the **Universal Satellite Pod** and **Removable Cartridge** was modeled in a translucent X-ray aesthetic (*Ghosted X-Ray*) and an exploded layer hierarchy:

#### Translucent 3D X-Ray CAD Architecture (100 x 60 x 28 mm, Universal Monocoque):
![OpenMotorBridge 3D X-Ray CAD Architecture](../images/cad/openmotorbridge_pod_assembly_render_xray.png)

#### Exploded Assembly Hierarchy (Along Horizontal Insertion Axis):
![OpenMotorBridge 3D Exploded View](../images/cad/openmotorbridge_pod_exploded_view.png)

#### Mechanical Specifications & Tolerances:
* **Outer Pod Enclosure:** PA12 MJF ($100.0 \times 60.0 \times 28.0\,\text{mm}$, internal bay $76.0 \times 55.0 \times 23.0\,\text{mm}$) with $R=3.0\,\text{mm}$ rounded corners.
* **Integrated Universal Tube Saddle (V-Groove):** Molded $120^\circ$ concave prism ($R=15\,\text{mm}$) on the bottom face that cradles frame tubes from $\varnothing 18\,\text{mm}$ to $\varnothing 35\,\text{mm}$ ($1"$ crash bars, $7/8"$ subframes, $1\,1/8"$ handlebars). Sits rock-solid on flat panels.
* **4x Side Hook Lugs & Zip-Tie Slots:** 4 integrated lateral retaining lugs for toolless attachment using 2 UV-resistant EPDM rubber rings, plus $5.0 \times 2.5\,\text{mm}$ passthrough slots for heavy-duty zip-ties or stainless hose clamps.
* **Solid PA12 Bottom Floor:** Continuous, sealed, leak-free, and crash-safe polymer bottom without external copper stud penetrations (100% compliant with ECE 22.06).
* **Pod Base PCB (`openmotorbridge_pod_base`):** $48.0 \times 24.0 \times 1.6\,\text{mm}$ PCB with centered M8 6-Pin IP67 all-metal receptacle (B.Cu) and vertical 6-pin pin header (F.Cu).
* **Screwed-in Bulkhead Plate:** $55.0 \times 23.0 \times 2.0\,\text{mm}$ PA12 with 2x M2 countersunk screws, protective shroud, and dual stainless steel ejector springs ($10\,\text{mm}$ stroke).
* **Open Cartridge Carrier Sled:** $75.0 \times 54.0 \times 20.5\,\text{mm}$ U-sled without top lid ($72.0 \times 50.0 \times 20.5\,\text{mm}$ usable inner volume).
* **Cartridge Carrier PCB (`openmotorbridge_pod_cartridge`):** $50.0 \times 22.0 \times 1.2\,\text{mm}$ FR4 carrier with DS2401 1-Wire ID, right-angle low-profile JST-SH 1.0mm 6P flex connector (F.Cu), and horizontal 6-pin socket header (B.Cu).
* **IP67 Sealing Plane:** Perimeter Shore 40A silicone flange gasket pre-compressed upon latching, hermetically sealing the internal chamber against high-pressure water jets and road dust (IP67 / IP69K).

---


---

### 5.10 Pod 3 Assembly & 1:1:1 CAD Fitting Verification

To validate the mechanical, thermal, and electrical integration of the entire system, the complete **Rear Pod 3 assembly (with OMM Transceiver and modular slide-in cartridge)** was modeled and verified in true 1:1:1 Euclidean scale CAD:

#### 1. 3D Assembly Exploded View (Full Component Hierarchy):
![OpenMotorBridge Pod 3 Assembly Exploded 3D CAD](../images/cad/pod3_full_assembly_exploded_3d.png)

*Figure 5.3: Exploded view of Satellite Pod 3 (120x64x32 mm monocoque enclosure, M8 6-pin panel receptacle on bottom face, vertical Pod Base PCB at inner bulkhead, screw-in PA12 protective partition with 45° alignment shroud and dual auto-eject stainless steel springs, and slide-in cartridge sled).*

#### 2. Close-Up View of Mated Interface & Shroud:
![OpenMotorBridge Pod 3 Mated Interface Close-Up](../images/cad/pod3_assembly_mated_closeup.png)

*Figure 5.4: Translucent close-up view of the mated state. The 6-pin precision pin header of the Pod Base engages the socket of the cartridge sled, fully enclosed by the 4-sided protective shroud. Compressed springs maintain constant preload against the IP67 flange gasket.*

#### 3. Cross-Sectional Fitting (Mechanical & Electrical Alignment):
![OpenMotorBridge Pod 3 Cross-Sectional Fitting](../images/cad/pod3_assembly_cross_section.png)

*Figure 5.5: True-to-scale cross section (X-Z plane) through Satellite Pod 3. Highlights the centered position of the 6-pin interface on the horizontal centerline, symmetrical sled guide rails, and stress-free transition from vehicle M8 connector to internal electronics.*

#### Summary of Mechanical Tolerances (Tolerance Stack-Up):
1. **Axial Centering:** The 6-pin interface ($J_1 \leftrightarrow J_1$) is located precisely on the horizontal centerline ($Y=0.0\,\text{mm}, Z=0.0\,\text{mm}$).
2. **Stress-Free Electrical Contacts:** Insertion forces are 100% absorbed by the solid $2.0\,\text{mm}$ PA12 bulkhead against the monocoque enclosure. PCB solder joints remain entirely free of bending moments.
3. **Auto-Eject Mechanism:** Dual V4A stainless steel springs produce an $8\dots 10\,\text{mm}$ automatic push-out stroke upon latch release, allowing easy removal even with heavy winter motorcycle gloves.

## 6. 6-Pin M8 / Pogo Interface & PUR Harness Color Coding

| M8 / Pogo Pin | Wire Color (PUR Cable) | Wire Gauge | Signal Pods 1 & 2 (Audio & Intercom) | Signal Pod 3 (Rear Transceiver) | Shielding & Twisting |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **Pin 1** | **Red (RD)** | $0.34\,\text{mm}^2$ (AWG22) | **`VCC`** (5V switched supply via P-FET) | **`VCC`** (5V continuous supply) | Single Conductor (Power) |
| **Pin 2** | **Black (BK)** | $0.34\,\text{mm}^2$ (AWG22) | **`GND`** (Dedicated power & signal ground) | **`GND`** (Dedicated power & signal ground) | Single Conductor (Power GND) |
| **Pin 3** | **White (WH)** | $0.14\,\text{mm}^2$ (AWG26) | **`NF_P`** (Balanced audio signal + via Bourns) | **`UART_TX`** (Rear MCU $\rightarrow$ Central Box) | **Pair 1 Twisted** (with Pin 4) |
| **Pin 4** | **Blue (BU)** | $0.14\,\text{mm}^2$ (AWG26) | **`NF_N`** (Balanced audio signal - via Bourns) | **`UART_RX`** (Central Box $\rightarrow$ Rear MCU) | **Pair 1 Twisted** (with Pin 3) |
| **Pin 5** | **Yellow (YE)** | $0.14\,\text{mm}^2$ (AWG26) | **`OPTO`** (TLP222A button simulation trigger) | **`GNSS_PPS`** (1-PPS hardware time sync) | Single Conductor (Control) |
| **Pin 6** | **Green (GN)** | $0.14\,\text{mm}^2$ (AWG26) | **`1-WIRE_ID`** (DS2401 Silicon Serial Number) | **`1-WIRE_ID`** (DS2401 rear cartridge ID) | Single Conductor (1-Wire Bus) |
| **M8 Shell** | **Braided Copper (BL)**| $> 85\,\%$ Braid | **`GND_SHIELD`** (360° Chassis & overall shield) | **`GND_SHIELD`** (360° Chassis & overall shield) | Overall shield via M8 metal collar |

---

## 7. Manufacturing & Material Selection: Desktop FDM vs. Industrial MJF

The entire OpenMotorBridge enclosure system is specifically engineered to be produced **both on standard desktop FDM 3D printers (Prusa, Bambu Lab, Voron, Creality) and via professional powder-bed 3D printing services (HP MJF / SLS)**:

### 7.1 Desktop FDM 3D Printing (Prusa MK3/MK4/XL, Bambu Lab X1/P1/A1, etc.)
* **Recommended Filaments for Motorcycle & Automotive Environments:**
  * **PETG:** *Ideal for all open-frame printers.* UV-resistant, impact tough, fuel and oil resistant, heat stable up to $80\,^\circ\text{C}$.
  * **ASA (or ABS):** *Recommended for enclosed printers (e.g., Bambu X1/P1, Prusa Enclosure).* $100\,\%$ UV and weather stable, heat resistant up to $100\,^\circ\text{C}$, beautiful matte finish.
  * **PA-CF / PET-CF (e.g., Bambu PAHT-CF, Prusament PA11-CF):** Maximum stiffness and OEM-like carbon finish.
  * ❌ *Note:* **Do not use standard PLA**, as PLA softens and deforms in direct sunlight on a motorcycle above $55\,^\circ\text{C}$!
* **Slicer Settings for IP67 Water Resistance (PrusaSlicer, Bambu Studio, OrcaSlicer):**
  * **Wall Perimeters:** Set to **4 to 5 perimeters** (wall thickness $\approx 1.6 \dots 2.0\,\text{mm}$ $\rightarrow$ walls print $100\,\%$ solid with no internal voids).
  * **Top/Bottom Solid Layers:** **5 to 6 layers**.
  * **Infill:** $25 \dots 40\,\%$ (Gyroid or Honeycomb).
  * **Layer Height:** $0.16\,\text{mm}$ (recommended for clean O-ring grooves) or $0.20\,\text{mm}$.
  * **Flow Rate:** $102 \dots 104\,\%$ (slight extrusion overlap permanently seals micro-pores between layer lines).
  * **Print Orientation:**
    * `main_box_lower_case.stl`: Flat on bottom base $\rightarrow$ **$0\,\%$ support required**.
    * `main_box_mid_tray.stl`: Flat on partition floor $\rightarrow$ Tree Support under perimeter sealing lip.
    * `main_box_lid.stl`: Flat on top face on print bed $\rightarrow$ **$0\,\%$ support required**.
    * `pod_base_housing.stl`: Standing upright on rear M8 gland face $\rightarrow$ minimal Tree Support under V-saddle.
    * `cartridge_*_sled.stl`: Flat on sled floor $\rightarrow$ snap-fit cantilever arms lay in the $XY$ plane (optimal continuous filament grain direction for maximum flex endurance!).

### 7.2 Industrial 3D Printing (HP MJF / SLS from JLCPCB, Weerg, Craftcloud)
* **Process:** **HP Multi Jet Fusion (MJF)** or **SLS** (Selective Laser Sintering).
* **Material:** **PA12 (Polyamide 12)**, black dyed and glass-bead blasted.
* **Advantages:** Isotropic mechanical strength across all 3 axes, 100% leak-proof, zero support artifacts.
* **Pre-packaged ZIP files for service providers:** [`hardware/production_packages/06_3d_print_mjf_stls/`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/06_3d_print_mjf_stls).


