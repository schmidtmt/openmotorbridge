# 08 - Mechanical Enclosures, CAD Models & Sealing System (All Units)

This document specifies the mechanical engineering, thermal dissipation, IP67/IP69K sealing concepts, kinematics of the quick-change auto-eject system, and all CAD and STL assets of OpenMotorBridge v8.0:
1. **Central Control Box (Type A):** 3-piece sandwich enclosure with intermediate tray, battery cradle, front interface panel (HD26, USB-C, LED), and planar 4-layer copper heat spreader.
2. **Universal Satellite Pods (Type B):** Mechanically identical 5-sided monocoque enclosure for Pods 1, 2, and 3 with $120^\circ$ V-groove pipe saddle, M8 6-pin IP67 connector, protective bulkhead, and spring-loaded auto-eject.
3. **Modular Cartridge Sleds (Type C):** Generic 2-piece base sled with asymmetrical Poka-Yoke tongue-and-groove rails for Sena 50S/60S, Cardo Packtalk Edge, OMM Transceiver, and IP67 blank cartridge (Dry Box).
4. **Rear Pod 3 & Radar Mount (Type D):** Aerodynamic tail cowl transceiver with dielectric radome for 868 MHz LoRa and Multi-GNSS, plus angle-adjustable mount for blind-spot radar (Garmin Varia).
5. **Universal Front Node (Type E):** Ultra-compact Smart Fairing Hub ($84 \times 60 \times 23\,\text{mm}$) featuring a **4-in-1 universal mounting system** (AMPS, pipe saddle, silentblocks, 3M Dual-Lock), EPDM cable combs, and Knowles MEMS acoustic channel.

---

## 1. Type A: Central Control Box (3-Piece Sandwich Architecture)

The Central Box enclosure is engineered in **PA12 (HP Multi Jet Fusion)** for harsh motorcycle environments (up to 20 g vibration, direct spray, under-seat heat soak):

- **External Dimensions:** $110{,}0 \times 74{,}0 \times 38{,}0\,\text{mm}$ (L x W x H; lower case $17{,}0\,\text{mm}$, upper case $15{,}0\,\text{mm}$, lid $6{,}0\,\text{mm}$).
- **Mounting:** 4x corner ears on lower case with **hole spacing $128{,}0 \times 56{,}0\,\text{mm}$** for M4 EPDM silentblocks (Shore 50A).
- **Internal Clearance:** $102{,}0 \times 66{,}0 \times 32{,}0\,\text{mm}$ (optimized for the $85 \times 55\,\text{mm}$ 4-layer main PCB).
- **Ingress Protection:** IP67 / IP69K (dust-tight, submersible to 1 m, steam-jet resistant).

![OpenMotorBridge Central Box 3D Cutaway CAD](../images/cad/main_box_cutaway_3d.png)

*Figure 8.1: Photorealistic 3D CAD diagonal cutaway render of the Central Control Box. The 3-tier sandwich is exposed: bottom tub with 4-layer PCB (ENIG) on M2.5 standoffs, intermediate tray with 11 convection cooling slots, upper LiPo UPS battery cradle with EPDM strap, HD26 flange, USB-C service port, and lid with Gore ePTFE vent.*

![OpenMotorBridge Central Box 3-Piece Sandwich IP67](../images/cad/main_box_enclosure_cad.png)

*Figure 8.2: 3D CAD visualization of the Central Control Box (Type A).*

```
┌────────────────────────────────────────────────────────────┐  ▲
│ 1. ENCLOSURE LID (6.0 mm Height / 3.0 mm Wall Thickness)   │  │
│    • Gore ePTFE pressure equalization vent (Ø 7.0 mm)      │  │ 38.0 mm
│    • Perimeter groove with Shore 40A silicone cord gasket  │  │ Total
│    • 100% monolithic solid polymer lid                     │  │ Height
├────────────────────────────────────────────────────────────┤  │
│ 2. UPPER CASE WITH INTERMEDIATE TRAY (15.0 mm Height)      │  │
│    • Front Panel: HD26 D-Sub flange, USB-C port, Status-LED│  │
│    • Upper Chamber: 1S LiPo UPS battery with EPDM strap    │  │
│    • Intermediate Tray: 11x convection vents & cable slot  │  │
├────────────────────────────────────────────────────────────┤  │
│ 3. LOWER CASE (17.0 mm Height - Monocoque Tub)             │  │
│    • 4-Layer Main PCB (85 x 55 mm) on M2.5 dampers         │  │
│    • 4x M4 silentblock mounting ears                       │  │
│    • 100% solid PA12 floor without through-holes           │  │
└────────────────────────────────────────────────────────────┘  ▼
```

![OpenMotorBridge Central Box Exploded 3D CAD Fitting](../images/cad/main_box_full_assembly_exploded_3d.png)

*Figure 8.2: 1:1:1 Euclidean CAD exploded view of the Central Box along the Z-axis.*

![OpenMotorBridge Central Box Mated 3D X-Ray CAD Fitting](../images/cad/main_box_assembly_mated_3d.png)

*Figure 8.3: Transparent 3D X-ray view of the closed Central Box showing clean internal clearances.*

---

## 2. Thermal Dissipation & Planar PCB Heat Spreading

Total heat dissipation during standard riding is only **$\approx 1{,}5\,\text{W}$** (peaking at $2{,}45\,\text{W}$ during fast charging):

1. **Planar 4-Layer Copper Heat Spreader ($85 \times 55\,\text{mm}$):** Two continuous $35\,\mu\text{m}$ inner copper layers spread heat rapidly ($\lambda = 390\,\text{W/(m}\cdot\text{K)}$) across the entire board surface.
2. **11x Intermediate Convection Slots:** 5 rear slots, 4 side slots, and 2 front slots allow warm air to rise into the upper lid chamber.
3. **Worst-Case Thermal Margins ($45^\circ\text{C}$ ambient + $13^\circ\text{C}$ motor heat = $58^\circ\text{C}$ under seat):**
   * **LM5164-Q1:** $T_j = 93{,}8^\circ\text{C}$ (Max $+150^\circ\text{C}$ $\rightarrow$ $+56{,}2^\circ\text{C}$ margin).
   * **ESP32-S3:** $T_j = 90{,}2^\circ\text{C}$ (Max $+105^\circ\text{C}$ $\rightarrow$ $+14{,}8^\circ\text{C}$ margin, zero throttling).
   * **1S LiPo Battery:** Safely remains below $60^\circ\text{C}$ (JEITA NTC pauses charging above $45^\circ\text{C}$).

---

## 3. Type B: Universal Satellite Pods (Pods 1, 2, and 3)

All 3 pod locations use the identical 5-sided monocoque enclosure ($135{,}0 \times 70{,}0 \times 38{,}0\,\text{mm}$):

![OpenMotorBridge Satellite Pod & Cartridge 3D Cutaway CAD](../images/cad/pod_cartridge_cutaway_3d.png)

*Figure 8.4: Photorealistic 3D CAD diagonal cutaway render of the Satellite Pod with docked Cartridge. Clearly visible: 120° V-groove pipe saddle with EPDM O-rings around frame tube, M8 6-pin connector, internal bulkhead with dual compressed V4A springs, asymmetrical Poka-Yoke rails with 6mm height offset, 6-pin gold contact mating (4.8mm wipe length), and front bezel gasket.*

![OpenMotorBridge Satellite Pod Exploded View](../images/cad/openmotorbridge_pod_exploded_view.png)

*Figure 8.5: Exploded view of the Satellite Pod with M8 socket, baseboard, bulkhead, and cartridge sled.*

![OpenMotorBridge Satellite Pod X-Ray Assembly](../images/cad/openmotorbridge_pod_assembly_render_xray.png)

*Figure 8.6: X-ray cutaway view of the closed Satellite Pod.*

### 3.1 Kinematics of Auto-Eject & Snap-Fit

| Parameter | Calculated Value | Verification & Function |
| :--- | :---: | :--- |
| **Spring Rate (2x V4A Springs)** | **$2{,}4\,\text{N/mm}$** | Dual parallel stainless steel springs |
| **Preload Travel** | **$6{,}0\,\text{mm}$** | Compressed from $L_0 = 15\,\text{mm}$ to $L_{\text{mated}} = 9\,\text{mm}$ |
| **Axial Retention Force** | **$7{,}2\,\text{N}$** | Maintains constant seal compression against 20 g shock |
| **Gasket Compression Force** | **$4{,}5\,\text{N}$** | $30\,\%$ compression of $1{,}5\,\text{mm}$ silicone cord |
| **Extraction Resistance** | **$> 65\,\text{N}$** | Prevents accidental detachment under cable pull |
| **Release Squeeze Force** | **$9{,}8\,\text{N}$** | Ergonomic thumb-and-finger squeeze ($\approx 1\,\text{kg}$) |
| **Auto-Eject Throw** | **$9{,}0\,\text{mm}$** | Clears 6-pin wipe ($4{,}8\,\text{mm}$) with $+4{,}2\,\text{mm}$ overtravel |

### 3.2 Asymmetrical Poka-Yoke Guide Rails

![OpenMotorBridge Pod Poka-Yoke Cross Section](../images/cad/pod_poka_yoke_cross_section_cad.png)

*Figure 8.7: Cross-section showing the $6{,}0\,\text{mm}$ vertical height offset of the guide rails ($Z=8{,}2\,\text{mm}$ left, $Z=14{,}2\,\text{mm}$ right), rendering inverted insertion physically impossible.*

---

## 4. Type C: Modular Cartridges & Sleds

![OpenMotorBridge Modular Cartridge Variants CAD Trio](../images/cad/cartridge_variants_trio.png)

*Figure 8.8: The 4 modular cartridge variants (OMM Transceiver, Sena 50S/60S, Cardo Packtalk Edge, IP67 Dry Box).*

* **Sena 50S/60S Cradle:** Form-fit nesting with OEM hook latching and 7-pin pogo array.
* **Cardo Packtalk Edge Cradle:** Magnetic Air Mount nest with dual N52 magnets and 5-pin spring contacts.
* **IP67 Blank Cartridge:** Hermetic dummy with $80 \times 46 \times 16\,\text{mm}$ dry storage compartment.

---

## 5. Type D: Rear Pod 3 Transceiver & Radar Bracket

![Pod 3 Transceiver & Radar 3D Cutaway CAD](../images/cad/pod3_radar_cutaway_3d.png)

*Figure 8.9: Photorealistic 3D CAD diagonal cutaway render of Rear Pod 3 with blind-spot radar. Features the dielectric radome with Gore vent, 25x25mm ceramic patch antenna, 868 MHz LoRa coil antenna, 4-layer PCB with RP2040 and SX1262, M8 6-pin connector, and M5 GoPro-compatible hinge with adjustable Garmin Varia radar unit.*

* **LoRa & Multi-GNSS Radome:** Dielectric PA12 shell with coaxial ground plane.
* **Radar Dual-Mount:** GoPro-compatible M5 hinge for Garmin Varia blind-spot radar alignment ($\pm 5^\circ$).

---

## 6. Type E: Universal Front Node (Smart Fairing Hub)

- **Dimensions:** $84{,}0 \times 60{,}0 \times 23{,}0\,\text{mm}$.
- **Protection:** IP67.

![Universal Front Node Closed CAD](../images/cad/front_node_closed_cad.png)

*Figure 8.8: Closed Front Node IP67 enclosure.*

![Universal Front Node Exploded 3D](../images/cad/front_node_exploded_3d.png)

*Figure 8.9: 3D exploded view of the Front Node.*

![Universal Front Node Cutaway 3D](../images/cad/front_node_cutaway_3d.png)

*Figure 8.10: Cutaway view highlighting Knowles MEMS acoustic channel and VBUS power switch.*

### 6.1 The 4-in-1 Universal Mounting System

![Universal Front Node Bottom CAD 4-in-1](../images/cad/front_node_bottom_cad.png)

*Figure 8.11: Underside showing AMPS pattern, $120^\circ$ V-groove, EPDM tabs, silentblock holes, and 3M Dual-Lock recesses.*

```
┌────────────────────────────────────────────────────────────────────────┐
│               THE 4-IN-1 UNIVERSAL MOUNTING SYSTEM (BOTTOM VIEW)       │
├────────────────────────────────────────────────────────────────────────┤
│ 1. AMPS HOLE PATTERN (30 x 38 mm):                                     │
│    • 4x M4 brass threaded inserts (Ruthex)                             │
│    • Direct mount to RAM-Mount balls, Garmin brackets, nav towers      │
├────────────────────────────────────────────────────────────────────────┤
│ 2. CRASH BAR / TUBE SADDLE (120° V-Groove):                            │
│    • Fits tube diameters from Ø 22 mm to Ø 32 mm                       │
│    • 4x anchor tabs for 2x weatherproof EPDM O-rings (BMW GS crash bar)│
│    • 100% toolless rapid installation without scratching paint         │
├────────────────────────────────────────────────────────────────────────┤
│ 3. SILENTBLOCK VIBRATION ISOLATION:                                    │
│    • Corner holes for M4 EPDM dampers (isolates single/twin vibration) │
├────────────────────────────────────────────────────────────────────────┤
│ 4. 3M DUAL-LOCK RECESSES:                                              │
│    • 2x flush 20 mm channels for 3M Dual-Lock adhesive tape            │
│    • Concealed installation inside Batwing or Sharknose fairings       │
└────────────────────────────────────────────────────────────────────────┘
```
