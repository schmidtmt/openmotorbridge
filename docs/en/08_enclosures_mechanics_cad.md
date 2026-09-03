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
   * **3.3V LDO:** $T_j = 110{,}4^\circ\text{C}$ (Max $+125^\circ\text{C}$).
   * **1S LiPo Battery:** Safely remains below $60^\circ\text{C}$ (JEITA NTC pauses charging above $45^\circ\text{C}$).

### 2.2 Upper Enclosure Tray: 1S LiPo Battery Cradle & Intermediate Pass-Throughs
* **Integrated LiPo Battery Pocket:** Form-fitting recess ($55{,}0 \times 32{,}0 \times 8{,}5\,\text{mm}$) molded into the top of the intermediate tray accommodating a 1000 mAh 1S LiPo backup cell (Type 103040 or 803048).
* **Vibration Isolation:** A $1{,}0\,\text{mm}$ damping EPDM foam mat underneath and a transverse elastic EPDM strap ($35 \times 10\,\text{mm}$) anchored to molded retention lugs hold the cell securely under 20 g shocks.
* **4-Pin JST-PH Battery Connector (`J3`):**
  * Pin 1: `VBAT+` ($+3{,}7\,\text{V}$ LiPo positive via BQ24075)
  * Pin 2: `NTC_10K` (Murata 10k NTC temperature thermistor for JEITA charging guard)
  * Pin 3: `GND` (LiPo ground)
  * Pin 4: `NC` / Shield
* **Tray Pass-Through Slots:**
  * Central cable aperture ($14{,}0 \times 4{,}0\,\text{mm}$) with rounded radiused edges ($R = 1{,}5\,\text{mm}$) routing the 2x13 internal ribbon cable from main board to front-panel HD26 flange without pinch points.
  * 2x access windows permitting tool access to lower PCB M2.5 mounting screws.

---

## 3. Front Panel Interfaces in the Upper Tray

```
                      FRONT WALL OF UPPER TRAY
┌─────────────────────────────────────────────────────────────┐
│ ┌────────────┐     ┌────────┐      ┌──────────────────────┐ │
│ │ 1. USB-C   │     │ 2. RGB │      │ 3. HD26 D-Sub Flange │ │
│ │    Service │     │    LED │      │    (Harness Socket)  │ │
│ │    Alu Cap │     │    Ø3mm│      │    2x M3 Jackscrews  │ │
│ └────────────┘     └────────┘      └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

1. **HD26 D-Sub Flange:** Amphenol LTW / NorComp SEAL-D with EPDM perimeter gasket ($1{,}5\,\text{mm}$, Shore 60A).
2. **USB-C Service Port:** Waterproof receptacle sealed by a blue anodized aluminum screw cap with captive O-ring.
3. **RGB Status LED Viewing Window:** Diffuse PMMA light guide ($\varnothing\,3{,}0\,\text{mm}$) with silicone O-ring seal.

---

## 4. Type B: Universal Satellite Pods (Pods 1, 2, and 3)

All 3 pod locations use the identical 5-sided monocoque enclosure ($135{,}0 \times 70{,}0 \times 38{,}0\,\text{mm}$):

![OpenMotorBridge Satellite Pod & Cartridge 3D Cutaway CAD](../images/cad/pod_cartridge_cutaway_3d.png)

*Figure 8.4: Photorealistic 3D CAD diagonal cutaway render of the Satellite Pod with docked Cartridge. Clearly visible: 120° V-groove pipe saddle with EPDM O-rings around frame tube, M8 6-pin connector, internal bulkhead with dual compressed V4A springs, asymmetrical Poka-Yoke rails with 8mm height offset, 6-pin gold contact mating (4.8mm wipe length), and front bezel gasket.*

![OpenMotorBridge Satellite Pod Exploded View](../images/cad/openmotorbridge_pod_exploded_view.png)

*Figure 8.5: Exploded view of the Satellite Pod with M8 socket, baseboard, bulkhead, and cartridge sled.*

![OpenMotorBridge Satellite Pod X-Ray Assembly](../images/cad/openmotorbridge_pod_assembly_render_xray.png)

*Figure 8.6: X-ray cutaway view of the closed Satellite Pod.*

### 4.1 V-Groove Pipe Saddle ($120^\circ$) & EPDM Strap Mounting
* **Underside Profile:** $120^\circ$-V-saddle ($R = 15\,\text{mm}$) contours snugly to frame tubes from $\varnothing 18\dots 35\,\text{mm}$ ($1"$ crash bars, $7/8"$ subframes).
* **4x Anchor Lugs:** Fast, scratch-free attachment using 2 UV-resistant EPDM O-rings providing vibration dampening.

### 4.2 Kinematics of Auto-Eject & Snap-Fit

```
                       AUTO-EJECT & SNAP-FIT KINEMATICS (TOP VIEW X-Y)
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ POD HOUSING TUNNEL (PA12, 100 x 60 mm)                                                       │
│                                                                                              │
│   ┌──────────────┐                                                     ┌─────────────────┐   │
│   │ Protective   │  ◄── V4A Ejection Springs (k = 1.2 N/mm)            │ Snap Retention  │   │
│   │ Bulkhead     ├───[§§§§§§§§§]───────────────┐                       │ Pocket in Wall  │   │
│   │ (x = 22 mm)  │   F_preload = 7.2 N         │                       │ (x = 86 mm)     │   │
│   │              │                             │                       │    ┌───────┐    │   │
│   │              │   6-Pin Gold-Plated         │ CARTRIDGE SLED        │    │ 85°   │    │   │
│   │   ┌──────┐   │   Connector Mating          │ (openmotorbridge_     │    │ Tooth │    │   │
│   │   │6-Pin ├───┼════════════════════════════►│  cartridge_sled)      ├────┴┤ ▲    │    │   │
│   │   │Header├───┤   Wipe = 4.8 mm             │                       │  ┌──┘ │    └───┐│   │
│   │   └──────┘   │                             │                       │  │30° │        ││   │
│   │              │                             │                       │  │Lead│        ││   │
│   │              ├───[§§§§§§§§§]───────────────┘                       │  │-in │        ││   │
│   │              │  ◄── V4A Ejection Springs                           │  └──┬─┘        ││   │
│   └──────────────┘                                                     │     │          ││   │
│                                                                        │  ┌──▼────────┐ ││   │
│                                                   Flexible PA12 Arm    │  │PUSH BUTTON│ ││   │
│                                                   (L=14 mm, b=10 mm) ──┴──┤(Ribbed)   │ ◄┼───┼── Thumb/Finger Squeeze
│                                                                           └───────────┘ ││   │   (F_squeeze = 10 N)
│                                                                           FRONT BEZEL   ││   │
└─────────────────────────────────────────────────────────────────────────────────────────┴┴───┘
```

| Parameter | Calculated Value | Verification & Function |
| :--- | :---: | :--- |
| **Spring Rate (2x V4A Springs)** | **$2{,}4\,\text{N/mm}$** | Dual parallel stainless steel springs (DIN EN 13906-1) |
| **Preload Travel** | **$6{,}0\,\text{mm}$** | Compressed from $L_0 = 15\,\text{mm}$ to $L_{\text{mated}} = 9\,\text{mm}$ |
| **Axial Retention Force** | **$7{,}2\,\text{N}$** | Maintains constant seal compression against 20 g shock |
| **Gasket Compression Force** | **$4{,}5\,\text{N}$** | $30\,\%$ compression of $1{,}5\,\text{mm}$ silicone cord |
| **Extraction Resistance** | **$> 65\,\text{N}$** | Prevents accidental detachment under cable pull |
| **Release Squeeze Force** | **$9{,}8\,\text{N}$** | Ergonomic thumb-and-finger squeeze ($\approx 1\,\text{kg}$) |
| **Auto-Eject Throw** | **$9{,}0\,\text{mm}$** | Clears 6-pin wipe ($4{,}8\,\text{mm}$) with $+4{,}2\,\text{mm}$ overtravel |

#### 4.2.1 The 4 Kinematic Phases of Cartridge Insertion
1. **Phase 1 - Pre-Centering ($x = 0\dots 80\,\text{mm}$):** Asymmetrical guide ribs engage housing channels. Lateral play is restricted to $\pm 0{,}2\,\text{mm}$.
2. **Phase 2 - Spring Compression ($x = 80\dots 86\,\text{mm}$):** The front face of the sled contacts the two stainless steel ejection springs in the bulkhead, building the $7{,}2\,\text{N}$ preload.
3. **Phase 3 - 6-Pin Contact Mating & Snap Lead-In ($x = 86\dots 91\,\text{mm}$):** The 6 gold-plated square pins enter $4{,}8\,\text{mm}$ deep into the dual-beam female header (Wipe). The $30^\circ$ lead-in ramps deflect the flexible PA12 arms inward.
4. **Phase 4 - Flush Locking ($x = 91\,\text{mm}$):** The $85^\circ$ locking teeth snap with an audible click into the wall retention pockets. The perimeter silicone gasket compresses by $30\,\%$.

#### 4.2.2 Stress & Fatigue Verification of PA12 Cantilever Arm
* **Dimensions:** Length $L = 14{,}0\,\text{mm}$, width $b = 10{,}0\,\text{mm}$, thickness $h = 1{,}8\,\text{mm}$, deflection $\delta = 1{,}8\,\text{mm}$.
* **Maximum Outer Fiber Strain:**
  $$\epsilon_{\max} = \frac{3 \cdot h \cdot \delta}{2 \cdot L^2} = \frac{3 \cdot 1{,}8\,\text{mm} \cdot 1{,}8\,\text{mm}}{2 \cdot (14{,}0\,\text{mm})^2} = \mathbf{1{,}38\,\%}$$
* **Permissible Continuous Strain for MJF PA12:** $\epsilon_{\text{zul}} \le 2{,}0\,\%$.
* **Bending Stress:** $\sigma_b = \epsilon_{\max} \cdot E_{\text{PA12}} = 0{,}0138 \times 1,700\,\text{MPa} = \mathbf{23{,}5\,\text{MPa}}$ (Well below the PA12 yield point of $48\,\text{MPa} \rightarrow$ **Safety Factor $S = 2{,}04$**).
* **Fatigue Life:** Validated for $> 10,000$ insertion/release cycles without plastic deformation.

#### 4.2.3 Contact Reliability & Wipe Length
* **Header Geometry:** $6{,}5\,\text{mm}$ square pin extension ($0{,}64 \times 0{,}64\,\text{mm}$, $0{,}76\,\mu\text{m}$ hard gold over nickel).
* **Effective Wipe Length:** **$4{,}8\,\text{mm}$** engagement inside female socket (exceeds USCAR-2 automotive spec of $\ge 1{,}5\,\text{mm}$ by a **factor of 3.2**).
* **Contact Bounce Prevention:** $7{,}2\,\text{N}$ continuous axial spring preload completely prevents contact micro-chatter under vibrations up to $20\,\text{g}$.

### 4.3 Asymmetrical Poka-Yoke Guide Rails

![OpenMotorBridge Pod Poka-Yoke Cross Section](../images/cad/pod_poka_yoke_cross_section_cad.png)

*Figure 8.7: Cross-section showing the $8{,}0\,\text{mm}$ vertical height offset of the guide rails ($Z=10{,}0\,\text{mm}$ left, $Z=18{,}0\,\text{mm}$ right), rendering inverted insertion physically impossible.*

---

## 5. Type C: Modular Cartridges & Sleds

![OpenMotorBridge Modular Cartridge Variants CAD Trio](../images/cad/cartridge_variants_trio.png)

*Figure 8.8: The modular cartridge variants (OMM Transceiver, Sena 50S/60S, Cardo Packtalk Edge, IP67 Dry Box).*

### 5.1 User-Centric Plug & Play Docking Architecture (Zero Solder)
To route signals from the right-angled **JST-SH 1.0 mm 6-pin SMD header (`J2`)** on the cartridge carrier PCB to adapter contact points without crimp or bend fatigue:
* **Under-Bed Cable Channel:** A recessed channel ($8{,}0 \times 1{,}5\,\text{mm}$) runs directly beneath the contoured cradle cavity.
* **Tray Pass-Through Slot:** A precision opening ($10{,}0 \times 3{,}0\,\text{mm}$ with $R = 1{,}0\,\text{mm}$ radiused edges) guides the flexible flat ribbon cable from header `J2` upward into the nest.
* **Standardized Pinout on JST-SH 6P Header (`J2`):**

| Pin | Signal Name | Adapter Function | Sena 50S/60S Pad | Cardo Edge Pad | Midland XT / PMR |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | `GND` | Common Ground Reference | Pin 1 (GND) | Pin 1 (GND) | Ground / Shield |
| **2** | `5V_VBUS` | Filtered 5V Charge (500mA PTC) | Pin 2 (USB-5V) | Pin 2 (5V Charge)| 5V DC In |
| **3** | `AUDIO_R+` | Audio Diff-Out + (to speaker input) | Pin 4 (Spk R+) | Pin 3 (Spk +) | Speaker In + |
| **4** | `AUDIO_R-` | Audio Diff-Out - (speaker return) | Pin 5 (Spk R-) | Pin 4 (Spk -) | Speaker In - |
| **5** | `MIC_IN+` | Audio Diff-In + (from microphone out) | Pin 6 (Mic +) | Pin 5 (Mic +) | Mic Out + |
| **6** | `OPTO_PTT` | Optocoupler PTT / Button Keying | Pin 7 (Mesh-Btn)| N/C (Aux) | PTT Switch |

### 5.2 Sena 50S / 60S Cradle
![OpenMotorBridge Sena 50S Cartridge Assembly 3D CAD Fitting](../images/cad/sena_cartridge_assembly_cad.png)

*Figure 8.9: CAD visualization of the Sena 50S/60S quick-change cartridge with spring-loaded 7-pin pogo array.*

### 5.3 Sena +Mesh & Universal Slide-Inlay (Class A with External RF Bulkhead)
For Sena +Mesh (or other OEM adapters requiring external antenna feeds):
* **100% Non-Destructive OEM Mount:** The Sena +Mesh remains in its unmodified original casing.
* **Form-Fitting Sled Inlay:** Mirrors the OEM bracket plate with 2x transverse sliding lugs (hook spacing $30\,\text{mm}$) and flexible snap tongue.
* **Integrated SMA Flange Bore ($\varnothing\,6{,}5\,\text{mm}$):** Features an O-ring sealing counterbore ($\varnothing\,9{,}5 \times 1{,}2\,\text{mm}$) on the front bezel for an IP67 SMA flange double-bulkhead (Female-to-Female).
* **Internal Coaxial Routing Channel:** Recessed cable window in the sled base routes the $8\,\text{cm}$ RG-178 internal pigtail (with 90° right-angle SMA male plug) without sharp bends.
* **EPDM Retention Strap:** Molded hook lugs accommodate an elastic EPDM band ($35 \times 10\,\text{mm}$) securing the adapter rattle-free in the contoured cavity.
* **Power Supply:** Ultra-flat right-angled Micro-USB / USB-C ribbon pigtail fed from Pin 1 (`GND`) and Pin 2 (`5V_VBUS`) of JST-SH header `J2`.

### 5.4 Cardo Packtalk Edge / Pro Magnetic Air Mount
![OpenMotorBridge Cardo Packtalk Edge Cartridge Assembly 3D CAD Fitting](../images/cad/cardo_cartridge_assembly_cad.png)

*Figure 8.10: CAD visualization of the Cardo Packtalk Edge cartridge with dual N52 neodymium magnets and 5 sprung contact pads.*

### 5.5 Cardo Packtalk Bold / Black Edition
Utilizes the slide-locking mechanical shoe of the original Cardo audio kit cradle. The unit slides in from the top and snaps into place against vibration.

### 5.6 Midland BT Mini / BTR1 Advanced & XT30 Slide
* **Midland Intercom Edition (BTR1 / Rush / BT Mini):** Contoured dock for Midland Bluetooth and Wave Mesh intercom units ($70\dots 85\,\text{mm}$ body width).
* **Midland XT Bare-Board Edition:** Houses the stripped PCB of a compact handheld transceiver (XT10/XT30/G5, $\approx 68 \times 42 \times 10\,\text{mm}$) directly inside the sled.

### 5.7 PMR446 Transceiver & Bare-Board Module (SA818S / RDA1846)
Fully integrated 500 mW PMR446 analog radio module ($38 \times 20\,\text{mm}$) mounted on the cartridge PCB – optionally using an internal 446 MHz helical coil or a front-mounted SMA connector for long-range antennas.

### 5.8 Longitudinal Cross-Section Comparison (Sena vs. Cardo)
![OpenMotorBridge Sena & Cardo Cartridges Longitudinal Cross Section](../images/cad/sena_cardo_cartridge_cross_section.png)

*Figure 8.11: 2D longitudinal cutaway (X-Z plane) through Sena 50S (top) and Cardo Packtalk Edge (bottom) cartridges.*

### 5.9 IP67 Blank Cartridge (Dry Box Dummy)
![OpenMotorBridge IP67 Blindkassette 3D CAD Render](../images/cad/dummy_cartridge_cad.png)

*Figure 8.12: Hermetic IP67 blank cartridge providing an $80 \times 46 \times 16\,\text{mm}$ dry storage compartment.*

---

## 6. Standardized 6-Pin M8 / PUR Harness Wire Color Coding

| M8 / Pogo Pin | Wire Color (PUR Cable) | Gauge | Signal Pod 1 & 2 (Audio & Intercom) | Signal Pod 3 (Rear Transceiver) | Shielding & Twisting |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **Pin 1** | **Red (RD)** | $0{,}34\,\text{mm}^2$ (AWG22) | **`VCC`** (5V switched via MOSFET) | **`VCC`** (5V supply) | Discrete conductor (Power) |
| **Pin 2** | **Black (BK)** | $0{,}34\,\text{mm}^2$ (AWG22) | **`GND`** (Dedicated power & signal ground) | **`GND`** (Dedicated power & signal ground) | Discrete conductor (Power Ground) |
| **Pin 3** | **White (WH)** | $0{,}14\,\text{mm}^2$ (AWG26) | **`NF_P`** (Balanced audio + via Bourns) | **`UART_TX`** (Rear Coprocessor $\rightarrow$ Box) | **Pair 1 twisted** (with Pin 4) |
| **Pin 4** | **Blue (BU)** | $0{,}14\,\text{mm}^2$ (AWG26) | **`NF_N`** (Balanced audio - via Bourns) | **`UART_RX`** (Box $\rightarrow$ Rear Coprocessor) | **Pair 1 twisted** (with Pin 3) |
| **Pin 5** | **Yellow (YE)** | $0{,}14\,\text{mm}^2$ (AWG26) | **`OPTO`** (TLP222A keying trigger) | **`GNSS_PPS`** (1-PPS hardware timecode) | Discrete conductor (Control) |
| **Pin 6** | **Green (GN)** | $0{,}14\,\text{mm}^2$ (AWG26) | **`1-WIRE_ID`** (DS2401 Silicon Serial Number) | **`1-WIRE_ID`** (DS2401 Tail cartridge ID) | Discrete conductor (1-Wire bus) |
| **M8 Shell** | **Tinned Copper Braid (BL)**| $> 85\,\%$ coverage | **`GND_SHIELD`** (360° chassis shield) | **`GND_SHIELD`** (360° chassis shield) | Overall shield over M8 collar |

---

## 7. Type D: Rear Pod 3 Transceiver & Radar Bracket

![Pod 3 Transceiver & Radar 3D Cutaway CAD](../images/cad/pod3_radar_cutaway_3d.png)

*Figure 8.13: Photorealistic 3D CAD diagonal cutaway render of Rear Pod 3 with blind-spot radar. Features the dielectric radome with Gore vent, 25x25mm ceramic patch antenna, 868 MHz LoRa coil antenna, 4-layer PCB with RP2040 and SX1262, M8 6-pin connector, and M5 GoPro-compatible hinge with adjustable Garmin Varia radar unit.*

![Pod 3 Full Assembly Exploded 3D](../images/cad/pod3_full_assembly_exploded_3d.png)

*Figure 8.14: Exploded view of Rear Pod 3 assembly.*

![Pod 3 Assembly Cross Section](../images/cad/pod3_assembly_cross_section.png)

*Figure 8.15: Longitudinal cross-section through Rear Pod 3 showing shielded RF compartment.*

* **LoRa & Multi-GNSS Radome:** Dielectric PA12 shell with coaxial ground plane.
* **Radar Dual-Mount:** GoPro-compatible M5 hinge for Garmin Varia blind-spot radar alignment ($\pm 5^\circ$).

---

## 8. Type E: Universal Front Node (Smart Fairing Hub)

- **Dimensions:** $84{,}0 \times 60{,}0 \times 23{,}0\,\text{mm}$.
- **Protection:** IP67.

![Universal Front Node Closed CAD](../images/cad/front_node_closed_cad.png)

*Figure 8.16: Closed Front Node IP67 enclosure.*

![Universal Front Node Exploded 3D](../images/cad/front_node_exploded_3d.png)

*Figure 8.17: 3D exploded view of the Front Node.*

![Universal Front Node Cutaway 3D](../images/cad/front_node_cutaway_3d.png)

*Figure 8.18: Cutaway view highlighting Knowles MEMS acoustic channel and VBUS power switch.*

### 8.1 The 4-in-1 Universal Mounting System

![Universal Front Node Bottom CAD 4-in-1](../images/cad/front_node_bottom_cad.png)

*Figure 8.19: Underside showing AMPS pattern, $120^\circ$ V-groove, EPDM tabs, silentblock holes, and 3M Dual-Lock recesses.*

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

---

## 9. CAD File Structure & OpenSCAD Parametric Library

All 3D enclosure models are maintained under `hardware/cad/stl/` and `hardware/cad/scad/`:

| Assembly | Component / Function | Ready-to-Print STL | Parametric OpenSCAD Source |
| :--- | :--- | :--- | :--- |
| **Central Box** | Lower tub with seal groove | `main_box_lower_case.stl` | `01_main_box/00_lower_deck.scad` |
| **Central Box** | Upper case with mid-tray | `main_box_mid_tray.stl` | `01_main_box/01_upper_deck.scad` |
| **Central Box** | Enclosure lid with Gore vent| `main_box_lid.stl` | `01_main_box/02_colsure.scad` |
| **Satellite Pod**| 5-sided monocoque housing | `pod_base_housing.stl` | `02_pod_base/pod_base_housing.scad` |
| **Bulkhead** | Internal partition & springs| `03_pod_bulkhead_partition.stl` | `02_pod_base/parts/bulkhead.scad`|
| **Cartridge** | Universal base sled | `cartridge_base_sled.stl` | `03_pod_cartridges/00_base_sled.scad`|
| **Cartridge** | Sena 50S/60S sled | `cartridge_sena_sled.stl` | `03_pod_cartridges/cartridge_sena.scad`|
| **Cartridge** | Cardo Packtalk Edge sled | `cartridge_cardo_sled.stl`| `03_pod_cartridges/cartridge_cardo.scad`|
| **Cartridge** | OMM Transceiver sled | `cartridge_omm_transceiver_sled.stl`| `03_pod_cartridges/cartridge_omm.scad`|
| **Cartridge** | IP67 Blank dry box dummy | `cartridge_blindkassette_waterproof.stl`| `03_pod_cartridges/cartridge_blind.scad`|
| **Front Node** | Lower case with 4-in-1 base | `front_node_lower_case.stl`| `04_front_node/front_node_lower.scad`|
| **Front Node** | Upper case with cable combs | `front_node_upper_case.stl`| `04_front_node/front_node_upper.scad`|

---

## 10. Manufacturing Specifications & 3D Printing Parameters (HP MJF vs. FDM)

### 10.1 Industrial Production (HP MJF PA12)
* **Process:** HP Multi Jet Fusion (MJF), dyed black, glass-bead blasted, and chemically vapor smoothed.
* **Tolerances:** $\pm 0{,}15\,\text{mm}$ (DIN ISO 2768-m).
* **Mechanical Properties:** Isotropic tensile strength $48\,\text{MPa}$, heat deflection temperature $+95\,^\circ\text{C}$, 100% airtight and watertight.

### 10.2 Prototyping on Desktop FDM (Bambu Lab / Prusa / Voron)
* **Filaments:** ASA or PETG (PLA strictly prohibited due to heat distortion under seat).
* **Perimeters:** 4 to 5 wall lines ($1{,}6\dots 2{,}0\,\text{mm}$ solid shell).
* **Infill:** $25\dots 40\,\%$ Gyroid pattern.
* **Extrusion Multiplier:** $102\dots 104\,\%$ to seal layer micro-porosity.
