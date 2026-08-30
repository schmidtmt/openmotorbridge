# 02 - PCB Hardware, Layout & Pinout Specification

This document specifies the 4-layer PCB layout of the central main box (`openmotorbridge_main_box`), EMC zoning, barrier-free connector corridor, vibration decoupling, and complete pin/GPIO assignments.

---

## 1. 3D Board Visualization & Photorealistic Render

The main board integrates on a compact **$85.0 \times 55.0\,\text{mm}$** footprint the entire automotive power supply, uninterruptible LiPo UPS, digital DSP host core, and galvanic isolated audio frontend:

![OpenMotorBridge Main Box 3D PCB Render](../../hardware/kicad_main_box/kicad_3d_render.png)

*Figure 2.1: Photorealistic 3D Raytracing Render of the OpenMotorBridge Central Main Box PCB (KiCad 10.0, 4-layer FR4 TG150 ENIG, 874 tracks, 114 vias, 0 DRC errors).*

---

## 2. PCB Dimensions, Stackup & Manufacturing Specification

| Parameter | Specification | Standard / Manufacturing Level |
| :--- | :--- | :--- |
| **Dimensions** | $85.0\,\text{mm} \times 55.0\,\text{mm} \times 1.6\,\text{mm}$ | DIN ISO 2768-m (Tolerance $\pm 0.1\,\text{mm}$) |
| **Layer Count** | **4 Copper Layers** | Symmetrical Stackup |
| **Base Material** | FR4 High-TG ($T_g \ge 150\,^\circ\text{C}$) | Automotive-grade thermal endurance |
| **Surface Finish** | **ENIG (Electroless Nickel Immersion Gold)** | Corrosion resistant, planar SMD pads |
| **Copper Weight** | $35\,\mu\text{m}$ (1.0 oz) Outer / $35\,\mu\text{m}$ Inner | High current capability for Buck & Power-Path |
| **Solder Mask** | Matte Black | Low reflection, UV resistant |
| **Silkscreen** | Crisp White High-Res | Crisp component & connector labeling |
| **Min. Trace / Spacing** | $0.127\,\text{mm}$ (5 mil) / $0.127\,\text{mm}$ (5 mil) | JLCPCB Standard / Prototype compatible |
| **Min. Drill (Via)** | $0.30\,\text{mm}$ Drill / $0.60\,\text{mm}$ Pad | Tented vias on all layers |

### 2.1 4-Layer Stackup Architecture
```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1 (F.Cu - Top): High-Speed Signals, I2S, Components  │  (35 µm Cu)
├─────────────────────────────────────────────────────────────┤
│ ── Prepreg 7628 (Dielectric, Er = 4.4, Thickness 0.2 mm) ── │
├─────────────────────────────────────────────────────────────┤
│ Layer 2 (In1.Cu): Continuous Ground Plane (GND_PWR / AGND) │  (35 µm Cu)
├─────────────────────────────────────────────────────────────┤
│ ── FR4 Core (Isolation Core, Thickness 1.0 mm) ──────────── │
├─────────────────────────────────────────────────────────────┤
│ Layer 3 (In2.Cu): Power Planes (VCC_3V3, VCC_5V Polygons)   │  (35 µm Cu)
├─────────────────────────────────────────────────────────────┤
│ ── Prepreg 7628 (Dielectric, Er = 4.4, Thickness 0.2 mm) ── │
├─────────────────────────────────────────────────────────────┤
│ Layer 4 (B.Cu - Bottom): Secondary Routing & SMD Sensors   │  (35 µm Cu)
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Zoning Architecture (Zero-Cross-Talk & Zero-Collision Topology)

![OpenMotorBridge Mainboard Top-Down Layout Diagram](../../hardware/cad/main_board_pcb_top_down.png)

*Figure 2.2: Collision-free 2D top-down component placement diagram of the central main board ($85 \times 55\,\text{mm}$). Color-coded zones with $100\,\%$ certified overlap-free bounding boxes.*

To eliminate cross-talk between the switching regulator RF ($2.1\,\text{MHz}$), 2.4 GHz Bluetooth/Wi-Fi wireless core, and ultra-sensitive analog audio paths, the PCB is segmented into **5 strictly isolated functional zones**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ZONE 1: RF & ESP32-S3 CORE                      │
│                • ESP32-S3-WROOM-1 (Top Center, Y in [73, 86])          │
│                • Clear 2.4 GHz PCB Antenna Zone (>21mm to H1/H2)       │
├─────────────────────────┬──────────────────┬───────────────────────────┤
│ ZONE 2: 72V BUCK POWER  │ ZONE 5: SENSORS  │ ZONE 3: GALV. AUDIO & CAN │
│ • LM5164 Buck (U1)      │ • MicroSD (J2)   │ • Bourns Trafo 1 (T1)     │
│ • 47µH Inductor (L1)    │ • ES8388 (U3)    │ • Bourns Trafo 2 (T2)     │
│ • SMBJ33CA TVS (D2 B.Cu)│ • BMI270 (U5)    │ • 2x TLP222A Opto (U7/U8) │
│ • TPS7A0533 LDO (U9)    │ (Bottom B.Cu)    │ • TCAN334G CAN (U6)       │
├─────────────────────────┴──────────────────┴───────────────────────────┤
│ ZONE 4: LOWER FLANGE CONNECTORS (Between Mounting Holes H3 & H4)       │
│ [J3: 10-Pin USB/UART IDC-10]            [J1: 26-Pin System-Bus IDC-26] │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Zone 1 (Top Center Edge – RF & Digital Core):**
   * Hosts the **ESP32-S3-WROOM-1** module (240 MHz Dual-Core) at $X = 149.50\,\text{mm}, Y = 86.00\,\text{mm}$.
   * The PCB antenna points **vertically upwards** ($Y \in [73.25, 79.75\,\text{mm}]$) with generous clearance:
     * $> 21.2\,\text{mm}$ clearance to mounting hole `H1` (top-left)
     * $> 37.0\,\text{mm}$ clearance to mounting hole `H2` (top-right)
   * The entire top strip ($Y \le 84.0\,\text{mm}$) is 100% free of copper fills, tracks, and tall components.

2. **Zone 2 (Left Flank – Automotive Power & UPS):**
   * Contains TI LM5164-Q1 Step-Down switching regulator `U1` ($X = 124.00, Y = 88.00$), Sunlord $47\,\mu\text{H}$ inductor `L1` ($X = 124.00, Y = 103.00$), and ultra-low-noise 3.3V LDO `U9` ($X = 134.00, Y = 84.00$).
   * SMBJ33CA TVS diode `D2` ($X = 123.00, Y = 84.00$) and $10\,\mu\text{F}$ 100V cap `C1` ($X = 130.00, Y = 84.00$) sit on the bottom layer (`B.Cu`) directly beneath `VIN` pins for minimal loop inductance.

3. **Zone 3 (Right Flank – Galvanic Isolation, Audio & CAN):**
   * **Galvanic Isolation Barrier ($4.0\,\text{mm}$ Creepage Distance):** Vertical isolation gap at $X = 162\,\text{mm}$ separates primary from secondary domain.
   * **Audio Isolation Transformers:** 2x Bourns LM-NP-1001 `T1` ($X = 174.00, Y = 90.00$) and `T2` ($X = 174.00, Y = 107.00$) with $17\,\text{mm}$ pitch for separated assembly courtyards.
   * **Optocouplers:** 2x Toshiba TLP222A PhotoMOS `U7` ($X = 186.00, Y = 90.00$) and `U8` ($X = 186.00, Y = 107.00$).
   * **CAN-FD:** TI TCAN334G Transceiver `U6` ($X = 185.00, Y = 78.00$) with $120\,\Omega$ termination resistor `R9`.
   * **Auxiliary Connectors:** `J5` (4-Pin JST-PH Battery+NTC, $X = 195.00, Y = 92.00$) and `J4` (3-Pin JST-PH RGB LED, $X = 195.00, Y = 108.00$).

4. **Zone 4 (Lower Flange Edge – Main Connectors):**
   * **`J3` (10-Pin USB & UART Service IDC-10):** Located at $X = 128.00\,\text{mm}, Y = 121.50\,\text{mm}$ (flush with mounting holes $H3/H4$).
   * **`J1` (26-Pin Automotive System Bus IDC-26):** Located at $X = 157.00\,\text{mm}, Y = 121.50\,\text{mm}$.
   * **Ergonomics:** Both connectors sit side-by-side with a snug $1.0\,\text{mm}$ gap at the lower edge and route via ribbon cable straight to the waterproof HD26 enclosure flange.

5. **Zone 5 (Bottom Layer `B.Cu` / Center – Sensors & Audio DSP):**
   * **MicroSD Slot `J2`:** Centrally at $X = 158.00\,\text{mm}, Y = 98.00\,\text{mm}$.
   * **Everest ES8388 Audio Codec `U3`:** At $X = 158.00\,\text{mm}, Y = 84.00\,\text{mm}$ on `B.Cu` for ultra-short trace routes to ESP32 and transformers.
   * **Bosch BMI270 6-Axis IMU `U5`:** At $X = 149.50\,\text{mm}, Y = 108.00\,\text{mm}$ at the PCB center of mass.

---

## 4. Central HD26/IDC-26 Connector Pinout (`J1`)

![OpenMotorBridge Central Automotive Wiring Harness](../../hardware/cad/wiring_harness_cad.png)

*Figure 2.3: Automotive Wiring Harness of the 26-Pin Flange Interface.*

| Pin (HD26/J1) | Signal Name | Type / Voltage Range | Function & Protection |
| :--- | :--- | :--- | :--- |
| **Pin 1** | `POD1_VCC` | $+5.0\,\text{V}$ switched (max. 300 mA) | Handlebar Pod 1 Power Supply (High-Side Switch) |
| **Pin 2** | `POD1_NF_P` | Audio Line-Out ($1.0\,\text{V}_{\text{RMS}}$ diff.) | Galvanically isolated via Trafo `T1` (Positive) |
| **Pin 3** | `POD1_NF_N` | Audio Line-Out ($1.0\,\text{V}_{\text{RMS}}$ diff.) | Galvanically isolated via Trafo `T1` (Negative) |
| **Pin 4** | `POD1_OPTO_KEY` | Optocoupler PTT Keying | PhotoMOS `U7` Open-Collector / Normally Open |
| **Pin 5** | `POD2_VCC` | $+5.0\,\text{V}$ switched (max. 300 mA) | Helmet Pod 2 Power Supply (High-Side Switch) |
| **Pin 6** | `POD2_NF_P` | Audio Line-In ($1.0\,\text{V}_{\text{RMS}}$ diff.) | Galvanically isolated via Trafo `T2` (Positive) |
| **Pin 7** | `POD2_NF_N` | Audio Line-In ($1.0\,\text{V}_{\text{RMS}}$ diff.) | Galvanically isolated via Trafo `T2` (Negative) |
| **Pin 8** | `POD2_OPTO_KEY` | Optocoupler Mute/Keying | PhotoMOS `U8` Open-Collector / Normally Open |
| **Pin 9** | `POD3_VCC` | $+5.0\,\text{V}$ switched (max. 500 mA) | Rear Transceiver Pod 3 Power Supply |
| **Pin 10** | `POD3_UART_TX` | UART TX ($3.3\,\text{V}$, 115200 Baud) | Data line to Pod 3 (GNSS/Telemetry) |
| **Pin 11** | `POD3_UART_RX` | UART RX ($3.3\,\text{V}$, 115200 Baud) | Data line from Pod 3 (GNSS/Telemetry) |
| **Pin 12** | `GND_PWR` | Power Ground ($0\,\text{V}$) | Main return path for Pod power supplies |
| **Pin 13** | `GND_PWR` | Power Ground ($0\,\text{V}$) | Parallel ground path for low resistance |
| **Pin 14** | `KL30_IN` | $+9\,\text{V} \dots +72\,\text{V}$ DC (Permanent Battery) | Battery Main Input (LM5164 Buck, TVS Protected) |
| **Pin 15** | `KL15_IGN` | $+9\,\text{V} \dots +72\,\text{V}$ DC (Switched Ignition) | Ignition sense with voltage divider & Schmitt trigger |
| **Pin 16** | `GND_PWR` | Power Ground ($0\,\text{V}$) | Vehicle ground reference |
| **Pin 17** | `CAN_H` | CAN High (ISO 11898-2) | CAN-FD Bus line High ($120\,\Omega$ termination) |
| **Pin 18** | `CAN_L` | CAN Low (ISO 11898-2) | CAN-FD Bus line Low ($120\,\Omega$ termination) |
| **Pin 19** | `ONEWIRE_ID` | 1-Wire Data Bus ($3.3\,\text{V}$) | Automatic Pod & Accessory Detection (DS2431) |
| **Pin 20** | `GND_SHIELD` | Enclosure & Cable Shield | Direct 360° chassis ground coupling |
| **Pin 21** | `AGND` | Analog Audio Ground | Quiet ground plane for Codec reference |
| **Pin 22** | `RESERVE_GPIO_A`| GPIO Digital I/O ($3.3\,\text{V}$) | Programmable GPIO / PWM Output |
| **Pin 23** | `RESERVE_GPIO_B`| GPIO Digital I/O ($3.3\,\text{V}$) | Programmable GPIO / ADC Input |
| **Pin 24** | `I2S_DOUT` | I2S Data Out ($3.3\,\text{V}$) | Digital Audio Stream to external DSP/Amp |
| **Pin 25** | `I2S_BCLK` | I2S Bit Clock ($3.3\,\text{V}$) | Digital I2S Clock |
| **Pin 26** | `GND_SHIELD` | Enclosure & Cable Shield | Second shield contact for full 360° enclosure bonding |

---

## 5. Service IDC-10 Connector Pinout (`J3`)

| Pin (`J3`) | Signal Name | Description |
| :--- | :--- | :--- |
| **Pin 1** | `VCC_5V_USB` | +5V USB-VBUS Power / Charging Input |
| **Pin 2** | `USB_D_N` | USB 2.0 Full-Speed Data Line Negative (ESP32-S3 USB-OTG) |
| **Pin 3** | `USB_D_P` | USB 2.0 Full-Speed Data Line Positive (ESP32-S3 USB-OTG) |
| **Pin 4** | `GND_PWR` | USB Ground |
| **Pin 5** | `UART_TXD0` | ESP32 Hardware UART0 TX (Debug & Flash Console) |
| **Pin 6** | `UART_RXD0` | ESP32 Hardware UART0 RX (Debug & Flash Console) |
| **Pin 7** | `ESP_EN` | Reset / Enable Control Signal |
| **Pin 8** | `ESP_BOOT` | Boot Mode Select (GPIO0) |
| **Pin 9** | `GND_PWR` | Debug Ground |
| **Pin 10** | `GND_SHIELD` | USB Cable Shield |
