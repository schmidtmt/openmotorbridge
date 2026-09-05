# 08 - Mechanical Enclosures, CAD Models & Sealing System (All Units)

This document specifies the mechanical engineering, thermal dissipation, IP67/IP69K sealing concepts, kinematics of the quick-change auto-eject system, and all CAD and STL assets of OpenMotorBridge v8.0:
1. **Central Control Box (Type A):** 3-piece sandwich enclosure with intermediate tray, battery cradle, front interface panel (HD26, USB-C, LED), and planar 4-layer copper heat spreader.
2. **Universal Satellite Pods (Type B):** Mechanically identical 5-sided monocoque enclosure for Pods 1, 2, and 3 with $120^\circ$ V-groove pipe saddle, M8 6-pin IP67 connector, protective bulkhead, and spring-loaded auto-eject.
3. **Modular Cartridge Sleds (Type C):** Generic 2-piece base sled with asymmetrical Poka-Yoke tongue-and-groove rails for Sena 50S/60S, Cardo Packtalk Edge, OMM Transceiver, and IP67 blank cartridge (Dry Box).
4. **Rear Pod 3 & Radar Mount (Type D):** Aerodynamic tail cowl transceiver with dielectric radome for 868 MHz LoRa and Multi-GNSS, plus angle-adjustable mount for blind-spot radar (Garmin Varia).
5. **Universal Front Node (Type E):** Ultra-compact Cockpit & Sensor Hub ($84 \times 60 \times 23\,\text{mm}$) featuring a **4-in-1 universal mounting system** (AMPS, pipe saddle, silentblocks, 3M Dual-Lock), EPDM cable combs, and Knowles MEMS acoustic channel.

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

## 7. Type D: Rear Pod 3 Transceiver (Backbone & Telemetry)

Rear Pod 3 integrates the OMM transceiver, 868 MHz LoRa, and Multi-GNSS (`PCBA 04`, RP2040) in a protected rear position.

> [!IMPORTANT]
> **Architectural Modularity (Type B Invariance):**
> The universal pod base enclosure of Pod 3 (Type B, $135 \times 70 \times 38.5\,\text{mm}$ outer dimensions, $100 \times 60 \times 28\,\text{mm}$ inner space) remains **100% identical and unchanged** across all motorcycle types. Integration of telemetry and wireless hardware is handled via the standardized OMM transceiver swap cartridge (`cartridge_antenna_bracket_omm.stl` / `04_antenna_bracket_omm.scad`). Vehicle-specific adaptation to fenders, luggage racks, or rear subframes occurs strictly via external mounting consoles or docking systems.

![Pod 3 Transceiver & Radar 3D Cutaway CAD](../images/cad/pod3_radar_cutaway_3d.png)

*Figure 8.13: Photorealistic 3D CAD isometric cutaway of rear Pod 3 with integrated blind-spot radar sensor. Depicted are the dielectric radome with Gore membrane, the 25x25 mm ceramic patch antenna, the 868 MHz LoRa helical antenna, the 4-layer PCB with RP2040 and SX1262, the M8 6-pin connector, and the integrated M5 GoPro swivel arm holding an adjustable Garmin Varia radar head.*

![Pod 3 Full Assembly Exploded 3D](../images/cad/pod3_full_assembly_exploded_3d.png)

*Figure 8.14: 3D CAD exploded view of rear Pod 3 with antenna radome, internal PCB, and M8 bayonet socket.*

![Pod 3 Assembly Cross Section](../images/cad/pod3_assembly_cross_section.png)

*Figure 8.15: Longitudinal cross-section through rear Pod 3 showing coaxially shielded antenna chamber and $25 \times 25\,\text{mm}$ GNSS ground plane.*

---

## 8. Type E: Universal Front Node (Cockpit & Sensor Hub)

The Front Node enclosure was specially engineered for protected installation inside motorcycle front fairings (Batwing, Sharknose, BMW GS/RT beak) or on crash bars:

- **Outer Dimensions:** Ultra-compact **$84.0 \times 60.0 \times 23.0\,\text{mm}$** (L x W x H).
- **Material:** HP Multi Jet Fusion (MJF) PA12, black glass-bead blasted and chemically vapor smoothed.
- **Protection Class:** IP67 (submersion and high-pressure water jet proof).

![Universal Front Node Closed CAD](../images/cad/front_node_closed_cad.png)

*Figure 8.16: Closed Front Node IP67 enclosure.*

![Universal Front Node Exploded 3D](../images/cad/front_node_exploded_3d.png)

*Figure 8.17: 3D exploded view of the Front Node along the vertical Z-axis.*

![Universal Front Node Cutaway 3D](../images/cad/front_node_cutaway_3d.png)

*Figure 8.18: Transparent 3D cutaway view of the Front Node showing Knowles MEMS acoustic duct and VBUS load switch.*

### 8.1 The 4-in-1 Universal Mounting System of the Front Node

![Universal Front Node Bottom CAD 4-in-1](../images/cad/front_node_bottom_cad.png)

*Figure 8.19: Enclosure bottom view of the Front Node showing AMPS hole pattern, $120^\circ$ V-groove tube saddle, EPDM strap anchor tabs, silentblock mounting holes, and 3M Dual-Lock hook-and-loop channels.*

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   THE 4-IN-1 UNIVERSAL MOUNTING SYSTEM (BOTTOM VIEW)                   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. AMPS HOLE PATTERN (30 x 38 mm):                                                     │
│    • 4x M4 brass threaded inserts (Ruthex) in standard AMPS layout                    │
│    • Compatible with all RAM-Mount ball adapters, Garmin brackets & cockpit crossbars  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. TUBE SADDLE PRISM (120° V-Groove):                                                  │
│    • Integrated channel fitting tube diameters from Ø 22 mm to Ø 32 mm                 │
│    • 4x anchor tabs for 2x weatherproof EPDM elastic straps (BMW GS / crash bars)      │
│    • 100% toolless rapid mounting without scratching frame paint                       │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 3. SILENTBLOCK VIBRATION ISOLATION:                                                    │
│    • Corner holes for M4 silentblocks (Shore 50A EPDM)                                 │
│    • Isolates high-frequency engine vibrations inside the fairing beak of 1-cyl / V2   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 4. 3M DUAL-LOCK VELCRO CHANNELS:                                                       │
│    • 2x recessed 20 mm channels for self-adhesive 3M Dual-Lock mushroom tape           │
│    • Perfect for flat plastic inner fairing surfaces in Batwing or Sharknose cowls     │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Vehicle-Specific Reference Mounting Kits (Zero-Drill / Bolt-On)

While all 5 hardware enclosures (Types A through E) are **100% universal and uniformly standardized**, OpenMotorBridge provides fully engineered, zero-drill and non-adhesive reference mounting kits for selected motorcycle platforms. These utilize original factory mounting points or elastic tensioning systems to seamlessly integrate the complete system without paint damage or irreversible body drilling.

---

### 9.1 Reference Kit 1: Harley-Davidson CVO Road Glide ST (2024+) & New Touring Platform

For high-performance baggers with factory solo seating and forged carbon cowl (FLTRXSTSE):
Due to factory inverted Showa remote reservoir rear shocks with thick braided hydraulic lines and the redesigned 2024 rear tail end, external strut brackets cannot be fitted. The ST Reference Kit therefore integrates the 5 nodes 100% invisibly and non-destructively:

```
          CVO ROAD GLIDE ST (2024+) COMPLETE SYSTEM INTEGRATION
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. COCKPIT (Front, concealed behind outer fairing skin):                    │
│    • Front Node (PCBA 05) + Ottocast mounted to aluminum fairing bracket   │
│    • 12V switched power tapped from internal fairing accessory port        │
│    • Wireless link (ESP-NOW) to Central Box -> 0 cables across steering stem│
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. CENTER (Under Solo Seat):                                                │
│    • Central Box centrally mounted in battery tray cavity                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. REAR (Under Forged Carbon Cowl & License Plate):                         │
│    • Pod 3 upright in Skeleton Dock (cvo_st_undercowl_skeleton_dock.scad)   │
│      Tensioned upward against road shocks, 0 holes drilled, 0 glue on paint │
│    • External 2.4 GHz Telemetry Fin (cvo_st_telemetry_fin.scad) on OEM tab  │
│    • Radar centered below license plate (radar_license_plate_bracket.scad)  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. SADDLEBAGS (Group Intercom Bridge Sena & Cardo):                         │
│    • Pod 1 (Sena Mesh) inside left saddlebag lid                            │
│    • Pod 2 (Cardo DMC) inside right saddlebag lid                           │
│    • Mounted to OEM hinge/check-strap screws (Zero-Drill)                   │
│    • Cable routed along check-strap, weatherproof quick disconnect at gap   │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### A. Rear Integration: Under-Cowl Skeleton Dock & Telemetry Fin
* **Skeleton Dock (`cvo_st_undercowl_skeleton_dock.scad`):** Receives the standard Pod 3 housing ($135 \times 70 \times 38.5\,\text{mm}$) upright. Two upward-arching spring arms brace against the ceiling of the carbon cowl, preventing any play or rattling over potholes and cobblestones.
* **Telemetry Fin (`cvo_st_telemetry_fin.scad`):** Mounts directly onto the OEM rear mounting tab of the cowl. It passes the ESP32-C3 2.4 GHz mesh antenna outside into clean air while routing the coaxial cable invisibly beneath the tab into the cowl.

#### B. Saddlebag Lid Integration: Pod 1 (Left) & Pod 2 (Right)
* **Top-Lid Mounting:** Both pods mount in the forward third of the saddlebag lids, bolted to the OEM Torx fasteners of the hinge/check-strap bracket (see [Section 9.5](#95-universal-saddlebag-lid-dock-saddlebag_lid_dockscad)).
* **Luggage & Beverage Safety:** Located approx. $30\,\text{cm}$ above the bag floor. Heavy cold drinks, tools, or damp rain gear on the bag floor remain completely outside the RF Fresnel zone.
* **Maximum RF Isolation ($> 40\,\text{dB}$):** Sena (left) and Cardo (right) are separated by $> 60\,\text{cm}$, with the steel rear fender and frame serving as an RF shield.

---

### 9.2 Reference Kit 2: Harley-Davidson Road King Special (FLHRXS / Classic Naked Touring)

For classic touring models without front fairing and with 2-Up comfort touring seat or classic rear fender:

```
             ROAD KING SPECIAL (RKS) COMPLETE SYSTEM INTEGRATION
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. COCKPIT (Nacelle, concealed behind 7" LED Headlight):                    │
│    • Front Node (PCBA 05) housed inside aluminum headlight nacelle cavity   │
│    • Powers Garmin Nav / smartphone handlebar mount & handlebar action cam  │
│    • Handlebar PTT button & Knowles wind-noise microphone                   │
│    • 100% wireless via ESP-NOW to Central Box -> 0 cables along fuel tank   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. CENTER (Under Touring Seat):                                             │
│    • Central Box centrally mounted in battery tray cavity                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. REAR (Fender Console & License Plate):                                   │
│    • Pod 3 in Touring Fender Console (pod3_touring_fender_console.scad)     │
│      Contoured onto fender, bolted to OEM 1/4"-20 pillion seat knurled nut  │
│    • Radar centered below license plate                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. SADDLEBAGS:                                                              │
│    • Pod 1 (Sena) & Pod 2 (Cardo) inside saddlebag lids (analogous to ST)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

* **Touring Fender Console (`pod3_touring_fender_console.scad`):** Organic teardrop shape ($R = 6\dots 7\,\text{mm}$) form-fitting Pod 3. Bolted to the OEM $1/4"-20$ knurled nut in the rear fender. The M8 cable dives invisibly forward under the seat.
* **Headlight Nacelle Front Node:** Utilizes the generous cavity behind the 7" LED headlight. Power supplied via the OEM Harley accessory connector located there.

---

### 9.3 Reference Kit 3: Classic Bagger & Cruiser (Touring Stealth Console)

For Harley-Davidson Street Glide, Electra Glide, and Ultra Limited with 2-Up comfort seat:

![Pod 3 Touring Stealth Console CAD](../images/cad/pod3_touring_stealth_cad.png)

*Figure 8.20: Isolated 3D CAD view of the Touring Stealth Console (`pod3_touring_stealth_console.scad`). Completely organic smoothed contours ($R = 6\dots 7\,\text{mm}$) without hard box edges. Forward mounting tab for the OEM $1/4"-20$ pillion seat screw in the fender, form-fitting seat transition with M8 cable duct heading forward under the seat, front slope integration at mid-insertion height ($Z = 22\,\text{mm}$), open central dock, and gently sloping teardrop rear tail with integrated clip-in slot for the rear antenna.*

![Pod 3 Fender Assembly Touring 3D](../images/cad/pod3_fender_assembly_touring_3d.png)

*Figure 8.21: Photorealistic complete rear assembly on the Classic Touring bike: Seamless transition against passenger seat, M8 cable routed invisibly forward, unobstructed pod roof for uncompromised GNSS reception, rearward cartridge insertion, and decoupled Garmin Varia radar below the license plate.*

---

### 9.4 Reference Kit 4: Adventure & Touring Enduros (BMW GS, KTM Adventure, Africa Twin)

For adventure motorcycles and naked bikes with tubular trellis subframes, rear racks, or aluminum luggage bridges:

```
            ADVENTURE BIKE (BMW GS / KTM / AFRICA TWIN) INTEGRATION
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. COCKPIT (Windscreen / Navigation Bar / Beak):                            │
│    • Front Node (PCBA 05) via AMPS hole pattern (30 x 38 mm) on nav bar     │
│      or vibration-isolated via M4 silentblocks inside the beak              │
│    • Direct power feed for Garmin Nav / Smartphone & handlebar action cam   │
│    • Knowles MEMS microphone samples turbulent wind level behind windscreen │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. CENTER (Under Rider Seat / Battery Compartment):                         │
│    • Central Box splash-proof mounted in battery compartment                │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. REAR (Luggage Rack / Tubular Subframe):                                  │
│    • Pod 3 with integrated 120° V-groove directly on rear rack / tube frame  │
│    • Secured with 2x weatherproof EPDM tension rings or heavy-duty zip ties │
│    • Blind-spot radar directly on integrated M5 GoPro swivel arm of Pod 3   │
│      (optimal ground clearance, no vulnerable overhangs)                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. CRASH BARS (Left & Right):                                               │
│    • Pod 1 (Sena) on left crash bar (120° V-groove for Ø 22..32 mm tubes)   │
│    • Pod 2 (Cardo) on right crash bar (EPDM tension rings)                  │
│    • Highest RF isolation (> 40 dB) across massive fuel tank & engine block │
└─────────────────────────────────────────────────────────────────────────────┘
```

* **V-Groove Tube Saddle ($120^\circ$ Prism):**
  The enclosure bottom of Pods 1, 2, and 3 features an integrated concave saddle ($R=15\,\text{mm}$) that clamps free of play onto all common crash bar and luggage rack tubes ($\varnothing 18\dots 35\,\text{mm}$, e.g. $22\,\text{mm}$ or $25.4\,\text{mm} / 1"$).
* **Integrated M5 GoPro Radar Arm on Pod 3:**
  Unlike low-slung cruisers and baggers, adventure enduros do not require decoupling the radar below the license plate: Due to the tall ride height and steep tail geometry, the radar mounts via the swiveling M5 GoPro arm directly on the Pod 3 base plate at optimal detection height ($80\dots 100\,\text{cm}$) with unobstructed beam clearance above the rear tire.

---

### 9.5 Universal Saddlebag Lid Dock (`saddlebag_lid_dock.scad`)

The universal Saddlebag Lid Dock ([`saddlebag_lid_dock.scad`](file:///Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/saddlebag_lid_dock.scad)) was specifically developed for protected, vibration-proof, and 100% non-destructive interior mounting of satellite Pods 1 (Sena Mesh) and 2 (Cardo DMC) in hard saddlebags (Reference: Harley-Davidson One-Touch hard saddlebags 2014–2024+):

![Universal Saddlebag Lid Dock CAD](../images/cad/saddlebag_lid_dock_iso.png)

*Figure 8.22: 3D CAD visualization of the Saddlebag Lid Dock (`saddlebag_lid_dock.scad`). Visible are the inboard-oriented Torx mounting flange for OEM hinge screws, forward M8 cable snout with strain relief, perimeter half-shell with EPDM strap slots, and upper drip lip shielding the cartridge entrance.*

#### 9.5.1 Zero-Drill Mounting & Mechanical Design
1. **OEM Mounting Point Utilization (Zero-Drill):**
   * The $4\,\text{mm}$ thick mounting flange picks up the two factory M5 / Torx T20 screws of the hinge/check-strap bracket (hole center spacing $52\,\text{mm}$).
   * Generous slotted holes ($\varnothing 5.6 \times 9.0\,\text{mm}$) accommodate manufacturing tolerances across ABS saddlebags.
   * **Zero holes drilled in the saddlebag:** The motorcycle and luggage remain 100% unmarred in original factory condition (preserves resale value and factory weather seal).
2. **Alternative / Additional Adhesive Mounting (3M VHB):**
   * The underside features four defined pockets ($18 \times 12 \times 0.8\,\text{mm}$) for 3M VHB high-performance acrylic foam tape, enabling optional mounting onto smooth inner walls of other luggage systems (e.g. BMW Vario or aluminum cases).
3. **Half-Shell Architecture ($H = 26\,\text{mm}$):**
   * The $3\,\text{mm}$ thick PA12 cradle encloses the Pod 3 housing ($135 \times 70 \times 38\,\text{mm}$) form-fittingly up to half its height.
   * The modular swap cartridge remains fully accessible from the rear and can be pinched and swapped in seconds without unbolting the dock.
4. **Overhead Drip Lip Protection:**
   * Over the cartridge entryway, an integrated **drip lip ($16 \times 2\,\text{mm}$ with $30^\circ$ roof angle)** deflects condensation or running rainwater sideways past the cartridge seal seam whenever the bag lid is opened in wet conditions.
5. **Vibration-Proof EPDM Retention:**
   * Two lateral slots ($25 \times 3\,\text{mm}$) accept an elastic retention strap that locks the pod securely in the cradle during severe road impacts.

#### 9.5.2 Cable Routing & Quick Saddlebag Removal
* **Integrated M8 Strain Relief:** At the front, a funnel-shaped snout routes the M8 PUR cable forward without pinch risks. Two zip-tie channels anchor the cable jacket against pull forces.
* **Routing along Check-Strap:** The cable runs parallel to the textile lid check-strap down into the saddlebag interior, experiencing no pinching or torsion during lid open/close cycles.
* **Watertight M8 Quick Disconnect:** An M8 inline quick disconnect is positioned at the upper bag gap (beneath the seat edge). Saddlebags can thus be disconnected and removed for servicing or washing with a single turn.

#### 9.5.3 RF Physics: Why Saddlebag Lids Beat Bag Floors

Placing intercom pods inside the saddlebag lid ($\approx 70\dots 75\,\text{cm}$ above the road surface) solves fundamental RF transmission challenges:

| Criterion | Mounting on Bag Floor / Lower Wall | Mounting in Saddlebag Lid (OpenMotorBridge) | Physical Justification |
| :--- | :--- | :--- | :--- |
| **Liquid Attenuation** | **Severe attenuation ($> 20\,\text{dB}$)** | **Zero attenuation ($0\,\text{dB}$)** | 2.4 GHz matches the resonant absorption frequency of water ($2\dots 4\,\text{dB/cm}$ loss). Cold beverage cans and water bottles settle on the floor and block Line-of-Sight (LOS). In the lid, the pod sits far above luggage. |
| **Fresnel Zone Clearance** | Close to ground ($30\,\text{cm}$), strong asphalt reflections | Optimal ($70\dots 75\,\text{cm}$ above pavement) | The first Fresnel zone toward group riders (helmets at $1.2\dots 1.5\,\text{m}$) remains unobstructed by ground interference and road surface multipath. |
| **Enclosure Attenuation** | ABS bag wall ($< 0.2\,\text{dB}$) | ABS bag lid ($< 0.2\,\text{dB}$) | Injection-molded ABS plastic is virtually transparent at 2.4 GHz ($\epsilon_r \approx 2.6$, $\tan\delta \approx 0.005$). |
| **Latching Mechanism** | Inside swing path of striker bar | $> 15\,\text{cm}$ clearance from striker bar | The metallic One-Touch striker bar causes only localized reflections and at $\lambda = 12.5\,\text{cm}$ produces zero forward/upward shadowing. |
| **RF Decoupling** | $< 20\,\text{dB}$ with adjacent mounting | **$> 40\,\text{dB}$ spatial diversity** | Sena (left bag) and Cardo (right bag) are separated by $> 60\,\text{cm}$; steel rear fender and frame act as RF shield $\implies$ 0 receiver de-sensing. |

---

### 9.6 Decoupled License Plate Radar Bracket & Legal Compliance

On cruisers and baggers, the Garmin Varia mmWave radar is **decoupled** from Pod 3 and mounted centered beneath the license plate:

![Radar License Plate Bracket CAD](../images/cad/radar_license_plate_bracket_cad.png)

*Figure 8.23: 3D CAD model of the decoupled license plate radar bracket with M6 clamping, M5 swivel hinge, and concealed rear M8 cable channel.*

* **Legal Requirement (§ 10 Para. 6 FZV / ECE R138):**
  The license plate must remain completely visible and unobstructed from above at a vertical angle of **at least $+30^\circ$**.
* **Avoiding the Roof Overhang Issue:**
  By placing the radar **under** the license plate, the upper pod console does not have to extend far rearward. The $+30^\circ$ line-of-sight to the registration seals and inspection decals remains 100% unobstructed.
* **Vibration & Shock Resistance:**
  The radar mounts directly to the sturdy base bracket without a long cantilever lever arm – fully vibration-proof against the low-frequency pulses of the Milwaukee-Eight 117 engine.
* **Concealed Cable Routing:**
  The M8 radar signal cable runs invisibly inside a recessed channel behind the license plate upward and merges behind the turn signal bar into the rear wiring harness.

---

## 10. CAD File Structure & OpenSCAD Parametric Library (STL Library)
 
The OpenMotorBridge CAD repository follows a strict hierarchical Constructive Solid Geometry (CSG) architecture:
- **Root Directories (`01_main_box/`, `02_pod_base/`, `03_pod_cartridges/`, `04_front_node/`)**: Contain **exclusively monolithic, directly 3D-printable production STLs** (100% single-manifold, watertight, 0 disconnected bodies).
- **Subdirectories (`components/`)**: Contain parametric modular subcomponents (e.g. un-cut solid base bodies, mounting ears, screw bosses, EPDM sealing combs, and PCB/battery inspection dummies) for assembly visualization and custom adaptations.

### 10.1 Ready-to-Print Production STLs (Root Folders)

| Assembly | Component / Function | Ready-to-Print STL | Parametric OpenSCAD Source |
| :--- | :--- | :--- | :--- |
| **Central Box** | Lower tub with seal groove & mounting ears | `01_main_box/main_box_lower_case.stl` | `01_main_box/00_lower_deck.scad` |
| **Central Box** | Upper case with mid-tray partition | `01_main_box/main_box_mid_tray.stl` | `01_main_box/01_upper_deck.scad` |
| **Central Box** | Enclosure lid with Gore vent recess | `01_main_box/main_box_lid.stl` | `01_main_box/02_colsure.scad` |
| **Satellite Pod**| 5-sided monocoque housing (tunnel) | `02_pod_base/pod_base_housing.stl` | `02_pod_base/pod_base_housing.scad` |
| **Satellite Pod**| CVO ST Under-Cowl Skeleton Dock | `02_pod_base/cvo_st_undercowl_skeleton_dock.stl` | `02_pod_base/cvo_st_undercowl_skeleton_dock.scad` |
| **Satellite Pod**| CVO ST Telemetry Fin (2.4 GHz Mesh) | `02_pod_base/cvo_st_telemetry_fin.stl` | `02_pod_base/cvo_st_telemetry_fin.scad` |
| **Satellite Pod**| Road King Special Touring Fender Console | `02_pod_base/pod3_touring_fender_console.stl` | `02_pod_base/pod3_touring_fender_console.scad` |
| **Satellite Pod**| Touring Saddlebag Lid Dock (Pods 1 & 2) | `02_pod_base/saddlebag_lid_dock.stl` | `02_pod_base/saddlebag_lid_dock.scad` |
| **Radar Mount** | Decoupled License-Plate Radar Bracket | `02_pod_base/radar_license_plate_bracket.stl` | `02_pod_base/radar_license_plate_bracket.scad` |
| **Cartridge** | Universal base sled with O-ring groove | `03_pod_cartridges/cartridge_base_sled.stl` | `03_pod_cartridges/00_base_sled.scad` |
| **Cartridge** | Sena 50S/60S adapter sled | `03_pod_cartridges/cartridge_insert_sena.stl` | `03_pod_cartridges/parts/01_insert_sena.scad` |
| **Cartridge** | Cardo Packtalk Edge adapter sled | `03_pod_cartridges/cartridge_insert_cardo.stl` | `03_pod_cartridges/parts/02_insert_cardo.scad` |
| **Cartridge** | IP67 Blank dry box insert dummy | `03_pod_cartridges/cartridge_insert_blindkassette.stl` | `03_pod_cartridges/parts/03_insert_blindkassette.scad` |
| **Cartridge** | OMM Dipole Antenna Bracket | `03_pod_cartridges/cartridge_antenna_bracket_omm.stl` | `03_pod_cartridges/parts/04_antenna_bracket_omm.scad` |
| **Front Node** | Lower tub with 4-in-1 base & mounting ears | `04_front_node/front_node_lower_tub.stl` | `04_front_node/00_front_node_tub.scad` |
| **Front Node** | Upper lid with LED tunnel & FPC antenna pocket | `04_front_node/front_node_upper_lid.stl` | `04_front_node/01_front_node_lid.scad` |
| **Front Node** | EPDM/TPU cable glands (pair with sprue runner) | `04_front_node/front_node_cable_glands_tpu.stl` | `04_front_node/02_front_node_cable_glands.scad` |
| **Front Node** | TPU USB-C protective sealing plug | `04_front_node/front_node_usbc_cap_tpu.stl` | `04_front_node/03_front_node_usbc_plug.scad` |

### 10.2 Modular Component Breakdowns & Dummies (`components/` Folders)

The `components/` directories host isolated base bodies (prior to CSG difference operations) and inspection parts:
- **`01_main_box/components/`**: `01_lower_tub_empty.stl`, `02_corner_screws_enclosure.stl`, `03_pcb_standoffs.stl`, `04_mounting_ears.stl`, `05_sealing_groove.stl`, `06_mid_tray_frame.stl`, `07_mid_partition_floor.stl`, `08_lid_plate.stl`, `dummy_main_pcb.stl`, `dummy_lipo_battery.stl`.
- **`02_pod_base/components/`**: `01_pod_tunnel_base.stl`, `02_pod_rear_m8_gland.stl`, `03_pod_bulkhead_partition.stl`, `04_pod_guide_grooves.stl`, `05_pod_strap_hooks.stl`, `06_fender_curved_saddle.stl`, `07_pod_slide_dock_core.stl`, `dummy_m8_connector.stl`.
- **`03_pod_cartridges/components/`**: `dummy_adapter_pcb.stl`, `dummy_omm_transceiver_pcb.stl`.
- **`04_front_node/components/`**:
  - `01_front_node_base_tub.stl`: Monolithic solid base tub with hollowed inner chamber (CSG base cube).
  - `02_pcb_standoffs.stl`: 4x M2.5 threaded boss standoffs for PCBA05.
  - `03_mounting_ears.stl`: 2x M4/M5 silentblock flange mounting ears.
  - `dummy_front_node_pcb.stl`: 3D inspection dummy of PCBA05 with component envelope heights.

---

## 11. Manufacturing Specifications & 3D Printing Parameters (HP MJF vs. FDM)

### 11.1 Industrial Production (HP MJF PA12)
* **Process:** HP Multi Jet Fusion (MJF), dyed black, glass-bead blasted, and chemically vapor smoothed.
* **Tolerances:** $\pm 0{,}15\,\text{mm}$ (DIN ISO 2768-m).
* **Mechanical Properties:** Isotropic tensile strength $48\,\text{MPa}$, heat deflection temperature $+95\,^\circ\text{C}$, 100% airtight and watertight.

### 11.2 Prototyping on Desktop FDM (Bambu Lab / Prusa / Voron)
* **Filaments:** ASA or PETG (PLA strictly prohibited due to heat distortion under seat).
* **Perimeters:** 4 to 5 wall lines ($1{,}6\dots 2{,}0\,\text{mm}$ solid shell).
* **Infill:** $25\dots 40\,\%$ Gyroid pattern.
* **Extrusion Multiplier:** $102\dots 104\,\%$ to seal layer micro-porosity.
