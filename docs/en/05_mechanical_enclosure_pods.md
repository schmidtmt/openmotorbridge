# 05 - Mechanical Construction: Central Main Box, Thermal Concept, Sealing & Modular Pods

This document specifies the mechanical construction, thermal management, and IP67 enclosure design of the central main control box (Type A) featuring an integrated **HD26 wall flange**, **waterproof USB-C service port**, **solid copper thermal stud cooling system**, and **waterproof RGB status light pipe**, as well as the universal satellite pod system (Type B) with modular slide-in cartridges.

---

## 1. Enclosure Type A: Central Main Box (Under Seat)

The base housing of the central main box is engineered as an ultra-rugged, 2-piece IP67/IP69K enclosure made of **PA12 (MJF process)** or **die-cast aluminum**, designed specifically for harsh motorcycle operating conditions (vibrations up to $20\,\text{g}$, high-pressure washdowns, heat buildup under the seat, and extreme road grime).

- **External Dimensions:** $110.0 \times 74.0 \times 38.0\,\text{mm}$ (L x W x H; Lower Hull $26.0\,\text{mm}$, Top Lid $12.0\,\text{mm}$).
- **Mounting:** 4x integrated corner ears with **hole spacing of $128.0 \times 56.0\,\text{mm}$** for vibration-damping **M4 silentblocks (Shore 50A EPDM)** to decouple high-frequency engine harmonics.
- **Internal Clearance:** $102.0 \times 66.0 \times 32.0\,\text{mm}$ (optimized for the $85.0 \times 55.0\,\text{mm}$ 4-layer main PCB).
- **Material & Manufacturing:** PA12 via HP Multi Jet Fusion (MJF) 3D printing (min. $3.0\,\text{mm}$ wall thickness), glass-bead blasted, chemically smoothed in hot vapor bath, and hydrophobic sealed.
- **Protection Class:** IP67 / IP69K (dust-tight, submersible to $1\,\text{m}$ depth, and resistant to high-pressure steam cleaning).

### 1.1 3D CAD Model & Thermal Concept

![OpenMotorBridge Central Main Box Base Enclosure IP67](../../hardware/cad/main_box_enclosure_cad.png)

*Figure 5.1: 3D CAD render of the central control box. Left: Closed IP67 housing with HD26 harness flange, blue anodized USB-C service screw cap, and 4x M4 silentblock mounting ears. Right: Sectional X-ray view revealing 4x solid copper thermal studs ($\varnothing\,8\,\text{mm}$), $2.0\,\text{mm}$ silicone thermal gap pad, 4-layer FR4 PCB, and integrated LiPo UPS battery pocket.*

```
┌────────────────────────────────────────────────────────────┐  ▲
│ 1. ENCLOSURE LID (12.0 mm Height)                          │  │
│    • PMMA RGB Status Light Guide (Ø 3.0 mm, IP67 O-Ring)   │  │ 38.0 mm
│    • Gore ePTFE Pressure Equalization Vent (Ø 7.0 mm)      │  │ Total
│    • Perimeter Groove with Shore 40A Silicone Profile Seal │  │ Height
├────────────────────────────────────────────────────────────┤  │
│ 2. LOWER HULL (26.0 mm Height - Solid Submersion Tray)     │  │
│    • Front Panel: HD26 D-Sub Flange + USB-C Service Cap    │  │
│    • 4-Layer Main PCB (85 x 55 mm) on M2.5 Damping Mounts  │  │
│    • 2.0 mm Silicone Thermal Gap-Pad (Shore 00 35)         │  │
│    • 4x Solid Copper Thermal Studs (Ø 8.0 mm)              │  │
│    • Recessed LiPo UPS Battery Pocket (52 x 36 x 6.5 mm)   │  │
└────────────────────────────────────────────────────────────┘  ▼
```

---

## 2. Comprehensive Thermal Management & Cooling Concept

Due to the sealed IP67 enclosure under the seat and power dissipation from the $100\,\text{V}$ switching regulator (LM5164-Q1, up to $1.8\,\text{W}$ under full pod load), LiPo charge controller (BQ24075, up to $1.2\,\text{W}$), and ESP32-S3 DSP core ($0.8\,\text{W}$), the lower hull incorporates a high-efficiency **solid copper thermal stud system**:

```
      PRINTED CIRCUIT BOARD (TOP & INNER LAYERS)
┌────────────────────────────────────────────────────────┐
│ [ LM5164 Buck ]     [ BQ24075 UPS ]     [ ESP32-S3 ]   │ ◄── Thermal Hotspots
│   (100V DCDC)       (Power-Path)        (Dual-Core)    │
├────────────────────────────────────────────────────────┤
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │ ◄── Thermal Vias (GND Plane)
└──────────────────────────┬─────────────────────────────┘
                           │
 ┌─────────────────────────▼─────────────────────────────┐
 │ 2.0 mm Compressible Silicone Gap-Pad (Shore 00 35)    │ ◄── λ = 3.0 W/(m·K)
 │ (Absorbs shock & vibration while bridging tolerances) │
 └─────────────────────────┬─────────────────────────────┘
                           │
 ┌─────────────────────────▼─────────────────────────────┐
 │ 4x Solid Copper Thermal Studs (Ø 8.0 mm, Pure Cu)     │ ◄── λ = 390 W/(m·K)
 │ Pressed into bottom hull & hydrophobically sealed     │     Direct Heat Sink
 └─────────────────────────┬─────────────────────────────┘
                           ▼
        Dissipation to Enclosure Base / Vehicle Chassis
```

### 2.1 Specification of Thermal Components:
1. **4x Solid Copper Thermal Pins ($\varnothing\,8.0\,\text{mm} \times 6.5\,\text{mm}$):**
   * Manufactured from electrolytic copper (CW004A / E-Cu58, $\lambda = 390\,\text{W/(m}\cdot\text{K)}$).
   * Direct waterproof press-fit / insert-molded into the bottom of the lower hull. Internal heads are machined flat ($\varnothing\,10\,\text{mm}$ flat head); external ends sit flush with the bottom surface or thermally couple to the vehicle frame.
   * Positioned directly beneath the 3 primary thermal hotspots:
     - **Pins 1 & 2:** Beneath the $100\,\text{V}$ power stage (LM5164-Q1 & power inductor $L_1$).
     - **Pin 3:** Beneath the BQ24075 UPS battery management controller.
     - **Pin 4:** Beneath the ESP32-S3 dual-core DSP module.
2. **Compressible Silicone Thermal Gap-Pad ($60 \times 40 \times 2.0\,\text{mm}$):**
   * Ultra-soft, vibration-damping silicone (*Bergquist Gap Pad 3000S30* / *Laird Tflex HD90000*, Shore 00 35, $\lambda = 3.0\,\text{W/(m}\cdot\text{K)}$).
   * Compresses by approximately $30\,\%$ ($0.6\,\text{mm}$ compression) upon PCB installation, absorbing mechanical tolerances without stress on SMD solder joints.
3. **Thermal Result:** Total thermal resistance drops from $> 45\,\text{K/W}$ (solid plastic enclosure) to **$< 5.8\,\text{K/W}$**. Peak junction temperature of the LM5164 stays safely below $+78\,^\circ\text{C}$ even at $+50\,^\circ\text{C}$ ambient under-seat temperature (rated up to $+125\,^\circ\text{C}$).

---

## 3. Front Panel Interfaces & Serviceability

### 3.1 HD26 D-Sub Wall Flange (Main Vehicle Harness Interface)
* **Cutout Geometry:** D-Sub High-Density 26-pin cutout ($39.2 \times 15.4\,\text{mm}$) in the front face of the **lower hull**.
* **Flange Gasket:** Precision-molded EPDM flat gasket ($1.5\,\text{mm}$ thickness, Shore 60A) between the metal collar of the Amphenol LTW / NorComp SEAL-D socket and the enclosure wall.
* **Fastening:** 2x M3 stainless steel hex jackscrews with O-ring sealing washers clamp the flange with $0.6\,\text{Nm}$ torque for a watertight seal.
* **Internal Decoupling:** Connected to the main PCB via a vibration-resistant $45\,\text{mm}$ ribbon cable or direct right-angle socket header.

### 3.2 Waterproof USB-C Programming & Service Port
* **Access without Opening Housing:** Located on the front face adjacent to the HD26 flange is a waterproof USB-C service port with a **blue anodized aluminum screw cap** and red NBR/silicone O-ring.
* **Function:** Facilitates on-vehicle firmware updates, ESP-IDF JTAG debugging, and diagnostics without disassembling the IP67 enclosure under the seat.

---

## 4. Waterproof Light Pipe for WS2812B RGB Status LED & Pressure Vent

```
┌─────────────────────────────────────────────────────────────┐
│ ENCLOSURE LID (3.0 mm Wall Thickness / 12.0 mm Height)      │
│                  ┌──────────────────┐                       │
│                  │  PMMA Light Pipe │ ◄── NBR O-Ring        │
│                  │  (Ø 3.0 mm Matt) │     (IP67 Sealed)     │
│                  └────────┬─────────┘                       │
├───────────────────────────┼─────────────────────────────────┤
│                           │ Optical Air Gap 0.8 mm          │
│                           ▼                                 │
│                  ┌──────────────────┐                       │
│                  │ WS2812B RGB LED  │                       │
│  MAIN PCB        │ (ESP32 GPIO 48)  │                       │
│  (LOWER HULL)    └──────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

### 4.1 Optical & Mechanical Specification
* **Light Pipe Component:** Precision PMMA light pipe with diffuse matte lens (*Mentor 1292.1101* / *Bivar PLPC3-3MM*), $\varnothing\,3.0\,\text{mm}$.
* **Sealing:** Perimeter NBR O-ring ($\varnothing\,3.0\,\text{mm}$ ID, $1.0\,\text{mm}$ cord thickness) in stepped lid aperture, flush pressed and sealed with clear polyurethane.
* **Pressure Equalization:** Gore ePTFE screw-in vent ($\varnothing\,7.0\,\text{mm}$) in the lid reliably balances atmospheric pressure variations (mountain pass rides up to $3,000\,\text{m}$) and thermal breathing effects.

### 4.2 Status LED Color Code (State Machine)

| LED Color & Pattern | Operational State | Meaning |
| :--- | :--- | :--- |
| 🟢 **Green Pulsing (1 Hz)** | **Normal Operation (Online)** | Main power active, all plugged pods operational, DLE OK |
| 🔵 **Blue Blinking (2 Hz)** | **BLE Dashboard / Pairing** | WebApp PWA actively connected / data transfer |
| 🟡 **Yellow Pulsing (0.5 Hz)**| **UPS Battery Mode (KL15 OFF)**| Shutdown rundown: GPX Tour-Close & WebDAV upload |
| 🔴 **Red Fast Blinking** | **Warning / Error** | Starter battery under-voltage ($< 11.8\,\text{V}$) / Cartridge short |
| 🟣 **Solid Purple** | **OMM DLE Leader** | Current motorcycle is coordinating the group mesh |
| ⚪ **White Double Flash** | **Actioncam Marker** | Handlebar button pressed: GPS highlight marker saved |

---


## 5. Enclosure Type B: Universal Satellite Pod (Identical for Pods 1, 2, and 3)

- **100% Universal Design:** All 3 pod locations on the motorcycle share the identical enclosure body scaled to the **Generic Maximum Envelope ($120.0 \times 64.0 \times 32.0\,\text{mm}$)**.
- **Chamber Dimensions:** $96.0 \times 56.0 \times 24.0\,\text{mm}$ (PA12 MJF, $3.0\,\text{mm}$ wall thickness).
- **Electronics Cartridge / Sled:** $92.0 \times 54.0 \times 23.5\,\text{mm}$ (Usable interior volume: $88.0 \times 50.0 \times 23.5\,\text{mm}$).

### 5.1 Open Cartridge Carrier Sled (Open Sled Architecture) & Carrier PCB
The removable cartridge is designed as an **open U-shaped carrier sled (Open Carrier Sled)**:

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
* **Spring-Loaded Auto-Eject Mechanism:**
  * To the left and right of the protective shroud, **dual stainless steel (V4A 1.4310) compression springs** with guide pushers are housed in the bulkhead.
  * **On Insertion:** Sliding the cartridge sled in compresses the dual springs by $5\dots 6\,\text{mm}$ until the 6-pin socket mates fully into the shrouded header and the snap-fit latches engage with a positive click. The compressed springs maintain continuous pre-tension against the silicone gasket—**100% vibration-proof and rattle-free**.
  * **On Release (Auto-Eject):** When the rider squeezes the two quick-release buttons on the faceplate, the snap-fit latches disengage, and **the dual springs pop the cartridge out by $8\dots 10\,\text{mm}$**.
  * Electrical contact is cleanly broken, and the rider can effortlessly pull the cartridge out even while wearing heavy winter motorcycle gloves without any jamming.

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

![OpenMotorBridge Modular Cartridge Variants CAD Trio](../../hardware/cad/cartridge_variants_trio.png)

*Figure 5.2: 3D CAD visualization of the three reference swappable cartridge cradles with form-fit 3D contour negative bedding and elastic EPDM retention straps in the open carrier sled ($92 \times 54 \times 23.5\,\text{mm}$): Sena Quick-Snap Cradle (left), Cardo Magnetic Air Mount (center), and Midland Dovetail Slide / Bare-PCB Inlay (right).*

#### 1. Sena 50S / 60S Contour Nest & Snap-Cradle
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

### 5.6 Monolithic Thermal Management: Lateral Thermal Slide Rails & Metallic Contact Plates

To dramatically maximize the thermal conduction surface while simultaneously eliminating sliding wear on the 3D-printed guide tracks, the system integrates a **lateral metallic cooling and guide rail architecture (*Lateral Thermal Slide Rails*)**:

```
                    REMOVABLE CARTRIDGE SLED (PA12)
 ┌───────────────────────────────────────────────────────────────────────────┐
 │   PCB / HEADSET BATTERY (5V charge loss, SX1262 LoRa PA, ESP32-C3)        │
 ├───────────────────────────────────────────────────────────────────────────┤
 │   FLEXIBLE SILICONE GAP-PAD (Shore 00 35, 1.5 mm, λ = 3.0 W/m·K)          │ ◄── Vibration Damping & Heat-Flow
 ├─────────────────────────┬───────────────────────┬─────────────────────────┤
 │ CARTRIDGE FLANK PLATE   │                       │ CARTRIDGE FLANK PLATE   │ ◄── 0.8 mm Copper/Alu Spring Plate
 └────────────┬────────────┴───────────────────────┴────────────┬────────────┘     (75 x 14 mm = 1050 mm² Area)
              │                                                 │
              ▼ (Large-Area Metallic Sliding Contact)           ▼
 ┌────────────┴────────────┬───────────────────────┬────────────┴────────────┐
 │ POD THERMAL SLIDE RAIL  │                       │ POD THERMAL SLIDE RAIL  │ ◄── Molded into Pod Side-Wall
 ├─────────────────────────┴───────────────────────┴─────────────────────────┤
 │                  MONOCOQUE POD OUTER HOUSING (PA12)                       │
 └─────────────────────────┬───────────────────────┬─────────────────────────┘
                           │                       │
                           ▼                       ▼
              ═══════════════════════════════════════════════════
                 DIRECT MOTORCYCLE AIRFLOW ACROSS OUTER FLANKS
              ═══════════════════════════════════════════════════
```

#### Engineering Advantages of Lateral Thermal Slide Rails:

1. **Massive Thermal Contact Surface ($> 1,050\,\text{mm}^2$ per flank):**
   * Instead of tiny isolated pins, the $75 \times 14\,\text{mm}$ **copper/aluminum flank plate** on the sled engages across its full length into the corresponding metal slide rail in the pod side-wall.
   * Thermal resistance drops by $> 5\times$ compared to localized pin contacts.
2. **Zero-Wear Metal-on-Metal Guidance:**
   * Repeated cartridge swapping (Sena $\leftrightarrow$ Cardo $\leftrightarrow$ OMM) eliminates plastic-on-plastic friction. The precision metal rails provide silky-smooth, durable insertion across thousands of cycles.
3. **Elastic Pre-load for Continuous Contact:**
   * The cartridge flank plate features a subtle convex spring bow ($0.3\,\text{mm}$ travel) backed by the flexible silicone pad, maintaining steady mechanical contact pressure against the outer rail.
4. **Airflow Dissipation on Outer Pod Flank:**
   * The pod slide rail extends slightly onto the exterior flank (or couples to the M5 mounting bracket), transferring heat directly into motorcycle airflow.
5. **100% RF-Neutral:**
   * Because the rails reside strictly on the lower side flanks, the upper $180^\circ$ hemispherical horizon for GNSS, LoRa, and Wi-Fi remains completely unobstructed, while providing beneficial side EMI shielding.

### 5.7 IP67 Dummy Cartridge (`Pod_Dummy_Cartridge_IP67.stl`)

When a pod bay is temporarily unpopulated (e.g. single-intercom configurations, seasonal winter storage of headsets, or maintenance), the form-identical **IP67 Dummy Cartridge** hermetically seals the bay:

![OpenMotorBridge IP67 Dummy Cartridge 3D CAD Render](../../hardware/cad/dummy_cartridge_cad.png)

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

* **Dimensions:** $48.0 \times 24.0\,\text{mm}$ (Compact 2-layer FR4 base board with generous clearance margins).
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

#### Translucent 3D X-Ray CAD Architecture (120 x 64 x 32 mm, Generic Max Envelope):
![OpenMotorBridge 3D X-Ray CAD Architecture](../../hardware/cad/openmotorbridge_pod_assembly_render_xray.png)

#### Exploded Assembly Hierarchy (Along Horizontal Insertion Axis):
![OpenMotorBridge 3D Exploded View](../../hardware/cad/openmotorbridge_pod_exploded_view.png)

#### Mechanical Specifications & Tolerances:
* **Outer Pod Enclosure:** Makrolon 2805 Polycarbonate / PA12 MJF ($120.0 \times 64.0 \times 32.0\,\text{mm}$, internal bay $96.0 \times 56.0 \times 24.0\,\text{mm}$).
* **Pod Base PCB (`openmotorbridge_pod_base`):** $48.0 \times 24.0 \times 1.6\,\text{mm}$ PCB with centered M8 6-Pin IP67 all-metal receptacle (B.Cu) and vertical 6-pin pin header (F.Cu).
* **Screwed-in Bulkhead Plate:** $56.0 \times 24.0 \times 2.0\,\text{mm}$ PA12 with 2x M2 countersunk screws, protective shroud, and dual stainless steel ejector springs ($10\,\text{mm}$ stroke).
* **Open Cartridge Carrier Sled:** $92.0 \times 54.0 \times 23.5\,\text{mm}$ U-sled without top lid ($88.0 \times 50.0 \times 23.5\,\text{mm}$ usable inner volume).
* **Cartridge Carrier PCB (`openmotorbridge_pod_cartridge`):** $60.0 \times 36.0 \times 1.2\,\text{mm}$ FR4 carrier with DS2401 1-Wire ID, right-angle low-profile JST-SH 1.0mm 6P flex connector (F.Cu), and horizontal 6-pin socket header (B.Cu).
* **IP67 Sealing Plane:** Perimeter $58.0 \times 28.0\,\text{mm}$ Shore 40A silicone flange gasket pre-compressed by $0.8\,\text{mm}$ upon latching, hermetically sealing the internal chamber against high-pressure water jets and road dust.

---

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


