# 07 - Hardware Architecture & Board Pinouts (PCBA 01 to 07)

This document serves as the **authoritative hardware specification for all 7 printed circuit board assemblies (PCBA 01 through PCBA 07)** of the OpenMotorBridge v8.0 system, detailing layer stackups, controlled impedance classes, zoning concepts, and complete pinout tables.

---

## 1. Overview of the 7 Hardware Assemblies (PCBAs)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   THE 7 HARDWARE ASSEMBLIES (PCBAs) OF OPENMOTORBRIDGE                 │
├───────┬───────────────────────────────┬───────────────┬─────────┬──────────────────────┤
│ Assy  │ Name & Function               │ PCB Outline   │ Layers  │ Key ICs / Components │
├───────┼───────────────────────────────┼───────────────┼─────────┼──────────────────────┤
│ **PCBA 01**│ **Central Box Main Controller**│ 85 x 55 mm    │ 4 Layer │ ESP32-S3, LM5164,    │
│       │ (Under-Seat, Audio / UPS / BT)│ (77x47 mm M3) │ (ENIG)  │ BQ24075, ES8388, IMU │
├───────┼───────────────────────────────┼───────────────┼─────────┼──────────────────────┤
│ **PCBA 02**│ **Satellite Pod Base Carrier** │ 36 x 20 mm    │ 2 Layer │ SP3012 TVS, M8 6-Pin,│
│       │ (Docking Base for Pod 1 & 2)  │ (30 mm M2)    │         │ Cartridge Receptacle │
├───────┼───────────────────────────────┼───────────────┼─────────┼──────────────────────┤
│ **PCBA 03**│ **Smart Modular Cartridge**   │ 35 x 25 mm    │ 2 Layer │ CH32V003 RISC-V MCU, │
│       │ (Rev 2.0 Mechatronic Carrier) │ (29x19 mm M2) │         │ 4x MOSFETs, J_ACT 8P │
├───────┼───────────────────────────────┼───────────────┼─────────┼──────────────────────┤
│ **PCBA 04**│ **Rear Pod 3 Transceiver Hub** │ 55 x 48 mm    │ 4 Layer │ RP2040 Coprocessor,  │
│       │ (Tail Pod: LoRa 868M & GNSS)  │ (46x19 mm M2) │ (ENIG)  │ SX1262 LoRa, MAX-M10S│
├───────┼───────────────────────────────┼───────────────┼─────────┼──────────────────────┤
│ **PCBA 05**│ **Universal Front Node**      │ 82 x 50 mm    │ 4 Layers│ ESP32-S3 Xtensa,     │
│            │ (Cockpit & Sensor Hub)        │               │         │ USB2514B 4-Port Hub, │
│            │                               │               │         │ USB-PD 20W, Qi/BSD   │
├───────┼───────────────────────────────┼───────────────┼─────────┼──────────────────────┤
│ **PCBA 06**│ **MagSafe Frame Dock Adapter** │ 28 x 11.5 mm  │ 2 Layer │ 500mA PPTC Fuse, 5V  │
│       │ (Frame Dock: M8 to MagSafe)   │ (Central M2.5)│         │ TVS, USBLC6-4SC6 ESD │
├───────┼───────────────────────────────┼───────────────┼─────────┼──────────────────────┤
│ **PCBA 07**│ **2-in-1 LoRa Smart-Keyfob**  │ 38 x 19 mm    │ 2 Layer │ nRF52840 SoC, SX1262 │
│       │ (Silent Pager, N52 Key & Qi)  │ (Pocket M2)   │ (ENIG)  │ DRV2605L LRA, BQ51003│
└───────┴───────────────────────────────┴───────────────┴─────────┴──────────────────────┘
```

---

## 2. JLCPCB 4-Layer Stackup & Controlled Impedances (JLC04161H-7628)

All 4-layer boards (PCBA 01, PCBA 04, and PCBA 05) utilize an identical controlled-impedance stackup:

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1 (F.Cu - Top): High-Speed Signals, USB Diff, SMDs    │  (35 µm / 1 oz Cu)
├─────────────────────────────────────────────────────────────┤
│ ── Prepreg 7628 (Dielectric, Er = 4.4, Thickness 0.2 mm) ── │
├─────────────────────────────────────────────────────────────┤
│ Layer 2 (In1.Cu): Solid Ground Plane (GND_PWR / AGND)       │  (17.5 µm Standard / opt. 35 µm)
├─────────────────────────────────────────────────────────────┤
│ ── FR4 Core (Dielectric Core, Thickness 1.0 mm) ─────────── │
├─────────────────────────────────────────────────────────────┤
│ Layer 3 (In2.Cu): Power Planes (VCC_3V3, VCC_5V Polygons)   │  (17.5 µm Standard / opt. 35 µm)
├─────────────────────────────────────────────────────────────┤
│ ── Prepreg 7628 (Dielectric, Er = 4.4, Thickness 0.2 mm) ── │
├─────────────────────────────────────────────────────────────┤
│ Layer 4 (B.Cu - Bottom): Secondary Routing & Sensors        │  (35 µm / 1 oz Cu)
└─────────────────────────────────────────────────────────────┘
```

### 2.1 Standardized Net Classes
* **`Default`:** Width $0{,}20\,\text{mm}$, Clearance $0{,}20\,\text{mm}$ (General I/O, logic).
* **`Power_5V_12V`:** Width $0{,}60\,\text{mm}$ (Up to $2{,}2\,\text{A}$ at $\Delta T < 10\,^\circ\text{C}$).
* **`RF_50R`:** Width $0{,}35\,\text{mm}$, Coplanar Gap $0{,}20\,\text{mm}$ to Ground ($50\,\Omega$ for 868 MHz LoRa & GNSS).
* **`USB_90R_DIFF`:** Width $0{,}20\,\text{mm}$, Differential Gap $0{,}15\,\text{mm}$ ($90\,\Omega \pm 10\,\%$ for USB 2.0 High-Speed 480 Mbps).
* **`Audio_Sensitive`:** Width $0{,}25\,\text{mm}$, Gap $0{,}30\,\text{mm}$ (Shielded by parallel ground guard traces).

---

## 3. PCBA 01: Central Box Main Controller (`openmotorbridge_central_box`)

![PCBA 01 Central Box Main Controller](../images/pcba/pcba01_central_box_3d.png)

*Figure 7.1: Precise KiCad 3D raytracing render of the Central Box main board (PCBA 01, 85 x 55 mm, 4 layers) with ESP32-S3 WROOM-1, LM5164-Q1 72V Buck, Bourns 1500V audio transformers, shrouded box headers, and gold ENIG pads.*

### 3.1 Board Specifications & Stackup
* **Dimensions:** $85{,}0 \times 55{,}0\,\text{mm}$ (Outer contour with 4x M2.5 mounting holes, $77{,}0 \times 47{,}0\,\text{mm}$ grid spacing).
* **Layer Stackup:** 4 Layers FR-4 High-TG150 ($1{,}6\,\text{mm}$ thickness, $35\,\mu\text{m}$ Cu on all 4 layers).
  * Layer 1 (Top): Components, RF traces, and differential audio pairs.
  * Layer 2 (Inner 1): Continuous, unbroken ground plane (Solid GND).
  * Layer 3 (Inner 2): Split Power planes ($+3{,}3\,\text{V}$, $+5{,}0\,\text{V}$, `VBUS`, `VBAT_LIPO`) and quiet audio ground.
  * Layer 4 (Bottom): Secondary signal routing, shield copper, and thermal stitch vias.
* **Surface Finish:** ENIG (Electroless Nickel Immersion Gold, $0{,}05\dots 0{,}1\,\mu\text{m}$ Au over $3\dots 5\,\mu\text{m}$ Ni).
* **Galvanic Isolation Barrier:** $4{,}0\,\text{mm}$ clearance and creepage distance beneath Bourns transformers `T1` and `T2`.

### 3.2 Pinout of Central 26-Pin Flange Connector (`J1` / HD26)

| Pin (HD26/J1) | Signal Name | Signal Type / Level | Function & Protection |
| :--- | :--- | :--- | :--- |
| **Pin 1** | `POD1_VCC` | $+5{,}0\,\text{V}$ switched (max. 300 mA) | Power Supply Handlebar Pod 1 (High-Side Switch, 500mA PPTC) |
| **Pin 2** | `POD1_NF_P` | Audio Line-Out ($1{,}0\,\text{V}_{\text{RMS}}$ diff.) | Galvanically isolated via Trafo `T1` (Positive) |
| **Pin 3** | `POD1_NF_N` | Audio Line-Out ($1{,}0\,\text{V}_{\text{RMS}}$ diff.) | Galvanically isolated via Trafo `T1` (Negative) |
| **Pin 4** | `POD1_OPTO_KEY` | Optocoupler PTT Keying | PhotoMOS `U7` Open-Collector / Switch (< 1 ms bounce-free) |
| **Pin 5** | `POD2_VCC` | $+5{,}0\,\text{V}$ switched (max. 300 mA) | Power Supply Helmet Pod 2 (High-Side Switch, 500mA PPTC) |
| **Pin 6** | `POD2_NF_P` | Audio Line-In ($1{,}0\,\text{V}_{\text{RMS}}$ diff.) | Galvanically isolated via Trafo `T2` (Positive) |
| **Pin 7** | `POD2_NF_N` | Audio Line-In ($1{,}0\,\text{V}_{\text{RMS}}$ diff.) | Galvanically isolated via Trafo `T2` (Negative) |
| **Pin 8** | `POD2_OPTO_KEY` | Optocoupler Mute / Keying | PhotoMOS `U8` Open-Collector / Switch (< 1 ms bounce-free) |
| **Pin 9** | `POD3_VCC` | $+5{,}0\,\text{V}$ switched (max. 500 mA) | Power Supply Rear Transceiver Pod 3 |
| **Pin 10** | `POD3_UART_TX` | UART TX ($3{,}3\,\text{V}$, 460,800 Baud) | High-speed data link to Pod 3 (GNSS/Telemetry/LoRa) |
| **Pin 11** | `POD3_UART_RX` | UART RX ($3{,}3\,\text{V}$, 460,800 Baud) | High-speed data link from Pod 3 (GNSS/Telemetry/LoRa) |
| **Pin 12** | `GND_PWR` | Power Ground ($0\,\text{V}$) | Main ground return for Pod power supplies |
| **Pin 13** | `GND_PWR` | Power Ground ($0\,\text{V}$) | Parallel ground path for minimal loop resistance |
| **Pin 14** | `KL30_IN` | $+9\,\text{V} \dots +72\,\text{V}$ DC (Constant+) | Main battery input (LM5164 Buck, SMBJ33CA TVS protected) |
| **Pin 15** | `KL15_IGN` | $+9\,\text{V} \dots +72\,\text{V}$ DC (Ignition+) | Ignition sense line with voltage divider & Schmitt-trigger |
| **Pin 16** | `GND_PWR` | Power Ground ($0\,\text{V}$) | Vehicle chassis ground |
| **Pin 17** | `CAN_H` | CAN High (ISO 11898-2) | CAN-FD busline High ($120\,\Omega$ switchable termination) |
| **Pin 18** | `CAN_L` | CAN Low (ISO 11898-2) | CAN-FD busline Low ($120\,\Omega$ switchable termination) |
| **Pin 19** | `ONEWIRE_ID` | 1-Wire Data Bus ($3{,}3\,\text{V}$) | Automatic Pod & Cartridge detection (DS2431 / DS2401) |
| **Pin 20** | `GND_SHIELD` | Enclosure & Shield Ground | Direct contact to aluminum housing & braided harness shield |
| **Pin 21** | `AGND` | Analog Audio Ground | Clean, isolated ground plane for ES8388 Codec |
| **Pin 22** | `RESERVE_GPIO_A`| Digital I/O ($3{,}3\,\text{V}$) | User-configurable GPIO / PWM output (ESP32-S3) |
| **Pin 23** | `RESERVE_GPIO_B`| Digital I/O ($3{,}3\,\text{V}$) | User-configurable GPIO / ADC input (ESP32-S3) |
| **Pin 24** | `I2S_DOUT` | I2S Data Out ($3{,}3\,\text{V}$) | Digital audio stream to external DSP / amplifier |
| **Pin 25** | `I2S_BCLK` | I2S Bit Clock ($3{,}3\,\text{V}$) | Digital I2S serial bit clock |
| **Pin 26** | `GND_SHIELD` | Enclosure & Shield Ground | Second shield contact for $360^\circ$ circumferential bonding |

### 3.3 Internal Connectors & Service Interfaces

| Connector | Type / Package | Pins | Function & Signal Assignment |
| :--- | :--- | :---: | :--- |
| **`J2`** | MicroSD Push-Push | 9-Pin | 4-Bit SDIO High-Speed Bus (`CLK`, `CMD`, `DAT0`-`DAT3`, `CD`, `3V3`, `GND`) for forensic telemetry blackbox. |
| **`J3`** | IDC Shrouded Header ($2{,}54\,\text{mm}$) | 10-Pin | Service, flashing, and debug interface: Pin 1: `3V3`, Pin 2: `TXD0`, Pin 3: `RXD0`, Pin 4: `GND`, Pin 5: `USB_D-`, Pin 6: `USB_D+`, Pin 7: `EN`, Pin 8: `IO0`, Pin 9: `CAN_H`, Pin 10: `CAN_L`. |
| **`J_BAT`**| Molex Micro-Fit 3.0 | 2-Pin | UPS LiPo Backup Cell: Pin 1: `VBAT_LIPO` ($+3{,}7\dots 4{,}2\,\text{V}$), Pin 2: `GND` (monitored by BQ24075 TS NTC). |
| **`J_AUD`**| JST-XH ($2{,}50\,\text{mm}$) | 4-Pin | Optional internal audio test port: `LINE_L+`, `LINE_L-`, `LINE_R+`, `LINE_R-`. |

---

## 4. PCBA 02: Satellite Pod Base Carrier (`openmotorbridge_pod_base`)

![PCBA 02 Satellite Pod Base Carrier](../images/pcba/pcba02_pod_base_3d.png)

*Figure 7.2: KiCad 3D render of the Pod Base carrier board (PCBA 02, 36 x 20 mm, 2 layers) with 6-pin precision pin header, M8 6-pin IP67 socket interface, and SP3012 TVS protection array.*

### 4.1 Board Specifications & Mechanical Fastening
* **Dimensions:** $36{,}0 \times 20{,}0\,\text{mm}$ (Rectangular PCB with 2x M2 mounting holes at $30{,}0\,\text{mm}$ spacing, seated inside the pod bulkhead chamber).
* **Layer Stackup:** 2 Layers FR-4 High-TG150 ($1{,}6\,\text{mm}$ thickness, $35\,\mu\text{m}$ copper).
  * Layer 1 (Top): Precision contact header `J1`, TVS array `U1`, decoupling capacitors.
  * Layer 2 (Bottom): Solid continuous GND plane for RF and transient suppression.
* **Surface Finish:** ENIG ($0{,}05\,\mu\text{m}$ gold plating for long-term corrosion resistance).

### 4.2 Pinout of Dual-Port Inputs (`J2` / Port A M8 & `J3` / Port B USB-C)

The pod base carrier board features two galvanically coupled input ports with automatic power multiplexing:
* **Port A (`J2`):** Rugged M8 circular receptacle (A-coded, 6-pin, IP67) for exposed outdoor mounting (e.g. rear radar Pod 3 or crash-bar clamps).
* **Port B (`J3`):** Ultra-flat 6-pin USB-C SMD receptacle for protected saddlebag interior mounting and tool-free chase/support vehicle deployment.

| Pin | Port A (`J2`, M8 6P) | Port B (`J3`, USB-C 6P) | Signal Type / Level | Function & Protection |
| :---: | :--- | :--- | :--- | :--- |
| **1** | `1_VCC_M8` | `A1/B12: GND` | Power Ground ($0\,\text{V}$) | Central low-impedance ground return |
| **2** | `2_GND` | `A4/B9: VCC_USBC` | $+5{,}0\,\text{V}$ DC (max. 500 mA) | Supply fed via LM66100 ideal-diode `U3` |
| **3** | `3_SIG_P` | `A6: SIG_P (D+)` | Audio Line Positive ($1{,}0\,\text{V}_{\text{RMS}}$ diff.) | Differential audio signal Positive (TVS Ch 2) |
| **4** | `4_SIG_N` | `A7: SIG_N (D-)` | Audio Line Negative ($1{,}0\,\text{V}_{\text{RMS}}$ diff.) | Differential audio signal Negative (TVS Ch 3) |
| **5** | `5_TRIGGER_PPS`| `A5: TRIGGER (CC1)` | Trigger / Timecode ($3{,}3\,\text{V}$ Logic) | Optocoupler PTT trigger or 1-PPS Timepulse (TVS Ch 4) |
| **6** | `6_1WIRE_ID` | `A8: 1WIRE_ID (SBU1)`| 1-Wire Data Bus ($3{,}3\,\text{V}$) | Auto-ID line for DS2401 cartridge recognition (TVS Ch 5) |
| **Collar**| `SHIELD` | `SH1/SH2: SHIELD` | Shield & Chassis Ground | $360^\circ$ circumferential contact to metal thread / shell |

### 4.3 Pinout of 6-Pin Precision Pin Header (`J1` / Cartridge Interface)

Vertical, gold-plated SMD pin header ($2{,}54\,\text{mm}$ pitch, $4{,}8\,\text{mm}$ wipe length, centered at $X=118\,\text{mm}$):

| Pin (J1) | Signal Name | Direction | Description |
| :---: | :--- | :---: | :--- |
| **Pin 1** | `1_VCC` | Output $\rightarrow$ Cartridge | $+5{,}0\,\text{V}$ DC power routed from active port via LM66100 power-mux |
| **Pin 2** | `2_GND` | Bidirectional | Ground reference for power and signals |
| **Pin 3** | `3_SIG_P` | Bidirectional | Differential audio signal Positive |
| **Pin 4** | `4_SIG_N` | Bidirectional | Differential audio signal Negative |
| **Pin 5** | `5_TRIGGER_PPS`| Bidirectional | Bounce-free PTT trigger line to headset |
| **Pin 6** | `6_1WIRE_ID` | Bidirectional | 1-Wire ROM-ID query line to DS2401 silicon chip |

* **ESD Protection Array:** Littelfuse `SP3012-06UTG` clamps all active signal lines against electrostatic discharges per IEC 61000-4-2 ($\pm 15\,\text{kV}$ air, $\pm 8\,\text{kV}$ contact) with $< 0{,}5\,\text{pF}$ parasitic capacitance.

### 4.4 Automatic Power-Mux & Modular Harness Architecture

1. **Hardware Arbitration (`U2`, `U3` / TI LM66100):**
   * Dual SC-70-6 ideal-diode ICs provide near-zero-latency automatic power selection with ultra-low on-resistance ($R_{\text{ON}} \approx 79\,\text{m}\Omega$, minimal millivolt drop).
   * Cross-conduction and reverse-current feeding between Port A and Port B are physically prevented.
2. **Modular Cable Harness Configurations:**
   * **Type A (Outdoor Motorcycle):** HD26 $\rightarrow$ 3x rugged M8 A-coded lines to the pod base screw receptacles.
   * **Type B (Saddlebag with MagSafe):** HD26 $\rightarrow$ M8 line to frame dock under the seat $\rightarrow$ 6-pin IP67 MagSafe breakaway coupling $\rightarrow$ slim cable entering saddlebag via 19 mm hole directly into Port B.
   * **Type C (Support Vehicle / Cabin / Lab):** HD26 $\rightarrow$ USB-C slim harness for tool-free, clean dashboard installation powered via standard automotive USB chargers.

---

## 5. PCBA 03: Smart Modular Cartridge (`openmotorbridge_pod_cartridge` Rev 2.0)
*KiCad Project Directory: [`hardware/kicad_pod_cartridge/`](../../hardware/kicad_pod_cartridge)*

![PCBA 03 Universal Cartridge Carrier](../images/pcba/pcba03_pod_cartridge_3d.png)

*Figure 7.3: KiCad 3D render of the Smart Modular Cartridge carrier (PCBA 03 Rev 2.0, 35 x 25 mm, 2 layers) featuring the horizontal 6-pin precision docking receptacle J1 along the rear edge (mating with the counterpart on PCBA 02 Pod-Base), WCH CH32V003 RISC-V controller (native 1-Wire emulation & ISP), 4x MOSFET driver stages for mechatronic actuators (J_ACT 8-pin), and headset interface (J2 6-pin).*

### 5.1 Board Specifications & Features
* **Dimensions:** $35{,}0 \times 25{,}0\,\text{mm}$ (compact carrier PCB with 4x M2 mounting holes in $29{,}0 \times 19{,}0\,\text{mm}$ grid, form-fit integrated into the $116 \times 58\,\text{mm}$ base sled with EPDM vibration-dampened contour bed).
* **Positive-Lock Docking:** The horizontal 6-pin docking receptacle `J1` aligns precisely at $(X=14\,\text{mm}, Y=35\,\text{mm})$ with the mating pin header `J2` on the Pod Base (PCBA 02). The asymmetrical guide rails on the cartridge sled ($Z=10\,\text{mm}$ left, $Z=18\,\text{mm}$ right) prevent tilt or incorrect insertion, guaranteeing smooth blind mating.
* **Layer Stackup:** 2 Layers FR-4 High-TG150 ($1{,}6\,\text{mm}$ thickness, $35\,\mu\text{m}$ copper both sides).
* **On-Board Components (Rev 2.0):**
  * `U1`: WCH `CH32V003F4P6` (32-Bit RISC-V, 48 MHz, 16 KB Flash, 2 KB SRAM, SOIC-8 or QFN-20) providing autonomous pattern timing, In-System Flashing, and native 1-Wire ROM-ID emulation (completely eliminating dedicated DS2401 silicon!).
  * `Q1` – `Q4`: 4x N-Channel Power MOSFETs (`AO3400`, SOT-23, $30\,\text{V} / 5.7\,\text{A}$, $R_{\text{ON}} < 28\,\text{m}\Omega$) for independent, low-loss driving of 4 discrete miniature actuators.
  * `F1`: Resettable PPTC 500mA fuse (Bourns `MF-MSMF050-2`).
  * `D1`: Dual-color status LED Green/Blue (Green = 1-Wire Active / Config Synced, Blue = Actuator Pulse).
  * **Role of TLP222A Optocouplers on PCBA 01:** On Central Box PCBA 01, the TLP222A PhotoMOS optocouplers are intentionally preserved. They provide dry contact closure for legacy passive cartridges (Rev 1.0), COTS helmet harnesses (Class B), and analog PMR446 two-way radios (Class E, e.g. Kenwood PTT). On Smart Cartridges (Rev 2.0), the native MOSFETs `Q1`..`Q4` switch directly to ground with zero loss, while physical galvanic isolation is 100% ensured via non-conductive plastic pushrods between actuators and rubber buttons.

### 5.2 Pinout of Horizontal Docking Socket (`J1` / Pod Base Mating)

| Pin (J1) | Signal Name | Signal Type | Function & Protection |
| :---: | :--- | :--- | :--- |
| **Pin 1** | `1_VCC` | $+5{,}0\,\text{V}$ Input | Supply voltage from Pod Base via resettable PPTC fuse `F1` (500mA) |
| **Pin 2** | `2_GND` | Power Ground | System ground connection to Pod socket |
| **Pin 3** | `3_NF_P` | Audio Line In/Out | Differential audio Positive to isolation transformer |
| **Pin 4** | `4_NF_N` | Audio Line In/Out | Differential audio Negative to isolation transformer |
| **Pin 5** | `5_TRIGGER_PPS`| Single-Wire UART / Pattern | Bidirectional configuration and opcode bus to Cartridge MCU `U1` (19,200 Baud) |
| **Pin 6** | `6_1WIRE` | 1-Wire Data Bus | Native 64-bit ROM-ID emulation by `U1` (cartridge discovery and class matching) |

### 5.3 Pinout of Internal 6-Pin JST-SH Header (`J2` / Audio & Power Harness)

| Pin (J2) | Signal Name | Direction | Function & Signal Level |
| :---: | :--- | :---: | :--- |
| **Pin 1** | `VCC_DIRECT_DC` | Output $\rightarrow$ Intercom | $+5.0\,\text{V}$ DC continuous charging / $+3.85\,\text{V}$ battery power |
| **Pin 2** | `GND` | Ground | Ground return (battery ground, audio ground) |
| **Pin 3** | `AUDIO_R+` | Output $\leftarrow$ Headset | Speaker / Line-Out from intercom $\rightarrow$ to OMB Codec Line-In via transformer |
| **Pin 4** | `AUDIO_R-` | Output $\leftarrow$ Headset | Speaker / Line-Out Ground / Negative |
| **Pin 5** | `MIC_IN+` | Input $\rightarrow$ Headset | Mic audio from OMB Codec DAC $\rightarrow$ Intercom mic input |
| **Pin 6** | `RESERVE_IO` | Bidirectional | Diagnostic and programming pin for Cartridge MCU `U1` |

#### Modular Harness Variants for `J2`:
* **Harness Variant A (Sena SPIDER X Slim):** 2-pin DC solder pigtail to battery terminal ⑧, 2-pin jack line to audio output ⑩, 2-pin line to microphone input ⑨.
* **Harness Variant B (Cardo Packtalk Edge Air Mount Cradle):** Connects to the OEM cradle pigtail: 3.5 mm stereo socket (speakers) to Pins 3/4, 2-pin miniature socket (mic) to Pins 5/2, and USB-C 5V power pigtail to Pins 1/2 for continuous charging.
* **Harness Variant C (Universal COTS / PMR446):** Flying lead pigtail (AWG28 shielded) for direct termination to Kenwood 2-pin radio plugs or custom Bluetooth modules.

### 5.4 Pinout of Mechatronic 8-Pin Actuator Header (`J_ACT` / $1{,}0\,\text{mm}$ JST-SH)
To control devices with different button layouts (Sena Spider X Slim vs. Cardo Packtalk Edge) flexibly, **4 discrete, independently positionable miniature actuators** are employed. Each actuator features its own 2-wire AWG30 silicone cable:

| Pin (J_ACT) | Signal Name | Driving Switch | Mapping: Sena SPIDER X Slim | Mapping: Cardo Packtalk Edge |
| :---: | :--- | :---: | :--- | :--- |
| **Pin 1 & 2** | `VCC_5V` | Continuous 5V | Common $+5\,\text{V}$ power rail for all 4 actuators | Common $+5\,\text{V}$ power rail |
| **Pin 3** | `ACT1_OUT` | MOSFET `Q1` | **Plus (+)** (Volume Up / Menu forward) | **Media Button** (Front/Top) |
| **Pin 4** | `ACT2_OUT` | MOSFET `Q2` | **Minus (-)** (Volume Down / Menu back) | **Mobile Button** (Phone/Pairing) |
| **Pin 5** | `ACT3_OUT` | MOSFET `Q3` | **Center / Phone** (Confirm / Select)  | **Intercom Button** (DMC Grouping) |
| **Pin 6** | `ACT4_OUT` | MOSFET `Q4` | **Mesh Button** (45° angled side)      | **Control Wheel Center-Press** |
| **Pin 7 & 8** | `GND` | Power Ground | Shield and return ground | Shield and return ground |

### 5.5 In-System Profile Flashing (ISP / IAP via Single-Wire) & Click Sequence Table
* **Zero Programmers Required:** When a profile (e.g. `sena_spider_x.json` or `cardo_dmc_gen2.json`) is assigned via the WebApp, the ESP32-S3 transmits an encrypted configuration packet via Pin 5 (`TRIGGER_PPS`) containing timing tables, pulse durations, and macro steps.
* **Persistent EEPROM Storage:** The Cartridge MCU burns the configuration table into internal EEPROM. The cartridge operates fully autonomously thereafter, executing multi-step macros locally.

#### Autonomous Smart Cartridge Click Sequences & Opcode Table:
| Opcode | Semantic Function | Sequence: Sena SPIDER X Slim | Sequence: Cardo Packtalk Edge |
| :---: | :--- | :--- | :--- |
| **`0x01`** | **Power Boot / Auto-On** | Simultaneous Plus + Center ($1000\,\text{ms}$) | Simultaneous Media + Mobile ($2000\,\text{ms}$) |
| **`0x02`** | **Power Off** | Simultaneous Plus + Center ($200\,\text{ms}$) | Simultaneous Media + Mobile ($2000\,\text{ms}$) |
| **`0x03`** | **Mute / Primary Action**| Single click Plus ($100\,\text{ms}$) | Wheel Center-Press $2000\,\text{ms}$ (DMC Group Mute) |
| **`0x04`** | **Stop / Secondary Action**| Single click Minus ($100\,\text{ms}$) | Wheel Center-Press $150\,\text{ms}$ tap (Audio Stop) |
| **`0x05`** | **Mesh Audio Toggle** | Mesh button $200\,\text{ms}$ tap (Open Mesh) | Intercom button $200\,\text{ms}$ tap (DMC Intercom) |
| **`0x06`** | **Group Pairing Mode** | Mesh button $3000\,\text{ms}$ hold pulse | Intercom button $5000\,\text{ms}$ hold pulse (Grouping) |
| **`0x07`** | **Channel / Macro 1** | Autonomous: 2x Mesh ($150\,\text{ms}$) + Pause + 1x Plus | Autonomous: 2x Intercom ($150\,\text{ms}$) (Private Chat) |
| **`0x08`** | **Channel / Macro 2** | Autonomous: 2x Mesh ($150\,\text{ms}$) + Pause + 1x Minus | Autonomous: 3x Intercom ($150\,\text{ms}$) (DMC Bridge) |
| **`0x09`** | **Phone / BLE Pairing** | Center button $5000\,\text{ms}$ hold pulse | Mobile button $5000\,\text{ms}$ hold pulse |


---

## 6. PCBA 04: Rear Pod 3 Transceiver Hub (`openmotorbridge_rear_pod3`)

![PCBA 04 Rear Pod 3 Transceiver Hub](../images/pcba/pcba04_rear_pod3_3d.png)

*Figure 7.4: KiCad 3D render of the Rear Pod 3 Transceiver PCB (PCBA 04, 55 x 48 mm, 4 layers) with RP2040 coprocessor, Semtech SX1262 LoRa, u-blox Multi-GNSS, and U.FL/Murata MM8030 RF switch ports.*

### 6.1 Board Specifications & RF Layout
* **Dimensions:** $55{,}0 \times 48{,}0\,\text{mm}$ (4 Layers FR-4 High-TG150, 4x M2 mounting holes in $46{,}0 \times 19{,}0\,\text{mm}$ grid, housed inside aerodynamic tail cowl with dielectric RF radome).
* **Layer Stackup:** 4 Layers FR-4 High-TG150 ($1{,}6\,\text{mm}$, $35\,\mu\text{m}$ Cu) with controlled $50\,\Omega$ coplanar waveguides.
  * Layer 1 (Top): RF transceivers, GNSS module, Murata MM8030 switches, $50\,\Omega$ coplanar RF traces.
  * Layer 2 (Inner 1): Continuous, unslotted RF ground reference plane.
  * Layer 3 (Inner 2): Split Power planes ($+3{,}3\,\text{V}_{\text{RF}}$, $+3{,}3\,\text{V}_{\text{DIG}}$, $+5{,}0\,\text{V}$).
  * Layer 4 (Bottom): RP2040 coprocessor, SPI Flash, passives, and secondary logic traces.

### 6.2 Pinout of 6-Pin Interface to Central Box (`J1`)

| Pin (J1) | Signal Name | Signal Type / Level | Function & Description |
| :--- | :--- | :--- | :--- |
| **Pin 1** | `1_VCC_5V` | $+5{,}0\,\text{V}$ DC switched (max. 500 mA) | Main power supply from Central Box |
| **Pin 2** | `2_GND` | Power & RF Ground ($0\,\text{V}$) | Common reference ground for logic and RF |
| **Pin 3** | `3_UART_TX` | UART TX ($3{,}3\,\text{V}$, 460,800 Baud) | High-speed telemetry and NMEA stream to Central Box |
| **Pin 4** | `4_UART_RX` | UART RX ($3{,}3\,\text{V}$, 460,800 Baud) | Command packets and LoRa payloads from Central Box |
| **Pin 5** | `5_1PPS` | Digital Pulse ($3{,}3\,\text{V}$, active-high) | Sub-microsecond timepulse from NEO-M9N GNSS |
| **Pin 6** | `6_1WIRE_ID` | 1-Wire Data Bus ($3{,}3\,\text{V}$) | Pod hardware identification via on-board DS2401 |

### 6.3 Coaxial RF Switch Ports (`Murata MM8030-2610`)

The board features 3 automatic coaxial switch connectors (`Murata MM8030-2610`) that seamlessly switch to external antennas upon insertion ($< 0{,}15\,\text{dB}$ insertion loss, $> 25\,\text{dB}$ isolation up to 6 GHz):

| RF Port | Frequency Band | Internal Default Antenna | External Bypass Path (MM8030) |
| :--- | :--- | :--- | :--- |
| **`J3`** | $2{,}4\,\text{GHz}$ ISM | Internal Inverted-F PCB Antenna (IFA, $0\,\text{dBi}$) | External $+5\,\text{dBi}$ whip or sharkfin antenna |
| **`J4`** | $868\,\text{MHz}$ LoRa | Internal helical coil antenna ($+1{,}5\,\text{dBi}$) | External $\lambda/4$ monopole antenna for maximum range |
| **`J5`** | $1{,}575\,\text{GHz}$ GNSS | Internal $25 \times 25\,\text{mm}$ ceramic patch antenna | External active patch antenna with $+3{,}3\,\text{V}$ phantom power |

### 6.4 RP2040 Dual-Cortex-M0+ Coprocessor Pin Mapping

| RP2040 Pin | Net Name | Function & Peripheral Assignment |
| :--- | :--- | :--- |
| **GPIO 0 / 1** | `UART0_TX` / `RX` | High-Speed UART link to Central Box (460,800 Baud, DMA-buffered) |
| **GPIO 4 / 5** | `UART1_TX` / `RX` | High-Speed UBX/NMEA binary link to u-blox NEO-M9N GNSS module |
| **GPIO 6** | `TIMEPULSE_1PPS` | Hardware capture timer input for frame-accurate action cam synchronization |
| **GPIO 8** | `SPI0_SCK` | SPI Serial Clock to Semtech SX1262 LoRa transceiver |
| **GPIO 9** | `SPI0_MISO` | SPI Master-In Slave-Out from SX1262 |
| **GPIO 10** | `SPI0_MOSI` | SPI Master-Out Slave-In to SX1262 |
| **GPIO 11** | `SPI0_NSS` | SPI Chip Select (Active-Low) to SX1262 |
| **GPIO 2** | `LORA_BUSY` | SX1262 State Flag (hardware hold condition for SPI commands) |
| **GPIO 3** | `LORA_DIO1` | SX1262 IRQ (Packet Received / Packet Sent Interrupt) |
| **GPIO 16** | `WS2812B_LED` | Serial data stream to RGB status indicator LED |
| **GPIO 14** | `I2C1_SDA` / `1WIRE_BUS` | I2C Data / 1-Wire data link for external antenna fin sensor port (`J6`) |
| **GPIO 15** | `I2C1_SCL` | I2C Clock for high-precision temperature probe (TI TMP117) & barometer |

### 6.5 External Antenna Base Sensor Port (`J6` / `J_EXT_TEMP`)

To ensure stable ambient air temperature readings unaffected by heat buildup under the tail cowl ($45\text{–}55\,^\circ\text{C}$), PCBA 04 integrates a dedicated 3-pin JST-SH micro header (`J6`). The wiring harness routes directly through the antenna mounting boss into the slipstream duct of the telemetry fin (`cvo_st_telemetry_fin.stl`):

| Pin (J6) | Signal | Level | Description |
| :---: | :--- | :--- | :--- |
| **Pin 1** | `+3V3_SENS` | $+3.3\,\text{V}$ DC switched | Sensor power supply (low-noise LDO rail) |
| **Pin 2** | `EXT_TEMP_DATA` | $3.3\,\text{V}$ open-drain (4.7 kΩ pullup) | 1-Wire (Dallas DS18B20) or I2C SDA (TI TMP117) |
| **Pin 3** | `GND` | $0\,\text{V}$ | Signal ground reference (RF shielded) |

* **Thermal Isolation:** Sensor probe sits completely outside the frame and exhaust heat plume directly in laminar oncoming airflow.
* **No Steering Head Cabling:** Siting ambient sensing at the tail preserves the 100% wireless Front-Node design (ESP-NOW).

---

## 7. PCBA 05: Universal Front Node (`openmotorbridge_front_node`)

![PCBA 05 Universal Front Node](../images/pcba/pcba05_front_node_3d.png)

*Figure 7.5: KiCad 3D render of the Universal Front Node (PCBA 05, 82 x 50 mm, 4 layers) with ESP32-S3-WROOM-1U (U.FL), Microchip USB2514B 4-Port hub, Southchip SC8102 USB-PD 20W Fast-Charge, TI TPS2051B power gate, Knowles I2S MEMS microphone, CPC1017N CAN auto-sensing relay, dual-MOSFET mirror BSD drivers, and WS2812B RGB status LED.*

### 7.1 Board Specifications & Features
* **Dimensions:** $82{,}0 \times 50{,}0\,\text{mm}$ (Fits $86 \times 56 \times 24\,\text{mm}$ internal cavity, $98 \times 68 \times 25\,\text{mm}$ outer enclosure with 4-in-1 mounting).
* **Layer Stackup:** 4 Layers FR-4 High-TG150 ($1{,}6\,\text{mm}$, $35\,\mu\text{m}$ copper).
  * Layer 1 (Top): ESP32-S3 controller, USB2514B hub, Knowles MEMS, WS2812B RGB, $90\,\Omega$ USB differential pairs.
  * Layer 2 (Inner 1): Continuous low-impedance ground plane (Solid GND).
  * Layer 3 (Inner 2): Split Power planes ($+5{,}0\,\text{V}_{\text{MAIN}}$, $+5{,}0\,\text{V}_{\text{DONGLE}}$, $+5{,}0\,\text{V}_{\text{CAM}}$, $+9\dots 12\,\text{V}_{\text{PD}}$, $+12\,\text{V}_{\text{SW}}$, $+3{,}3\,\text{V}$).
  * Layer 4 (Bottom): LMR36015 / TPS54302 buck, SC8102 USB-PD controller, TPS2051B load switch, CPC1017N relay, DMN63D8 dual-MOSFET, TVS diodes, and filters.
* **KL15 Buffer Capacitor (`C_BUF`):** $470\dots 1000\,\mu\text{F}$ 10V low-ESR polymer SMD (7343 / D-case) buffers the ESP32-S3 for $1\dots 2\,\text{s}$ upon ignition shutoff, ensuring clean transmission of the BLE shutter-stop command to action cameras.
* **RF Antenna Concept:** ESP32-S3-WROOM-1U with U.FL antenna jack; 2.4 GHz FPC dipole antenna mounted at the rear housing flank pointing along the frame tunnel toward the Central Box under the seat for maximal range and total decoupling from fairing electronics.

### 7.2 Vehicle & Sensor Interfaces (JST-PH Headers)

| Connector | Type | Pins | Signal Assignment & Function |
| :--- | :--- | :---: | :--- |
| **`J1`** | JST-PH / 2-Pin Terminal | 2-Pin | **12V Vehicle Input:** Pin 1: `KL15_12V_SW` ($+9\dots 36\,\text{V}$ DC Ignition+), Pin 2: `GND` (Vehicle chassis ground). Powered via LMR36015 buck converter. |
| **`J2`** | JST-PH ($2{,}00\,\text{mm}$) | 3-Pin | **Cockpit CAN Bus:** Pin 1: `CAN_H`, Pin 2: `CAN_L`, Pin 3: `GND`. Equipped with **electronic auto-sensing $120\,\Omega$ solid-state relay (`CPC1017N`)** (probes bus impedance at boot; enables termination only if $R_{\text{Bus}} > 100\,\Omega$) and hardware Listen-Only Mode pin (`S`). |
| **`J3`** | JST-PH ($2{,}00\,\text{mm}$) | 4-Pin | **Handlebar Multi-Button Interface:** Pin 1: `GND`, Pin 2: `PTT_INTERCOM` (Intercom transmit button), Pin 3: `CAM_ACTION` (Action-Cam bookmark/highlight), Pin 4: `MEDIA_VOICE` (Track Next / Siri / Google Assistant). All lines filtered with Schmitt-trigger, pull-ups, and 3.3V Zener/TVS overvoltage clamps against 12V shorts. (Standard 2-pin PTT switches fit directly onto Pins 1+2). |
| **`J9`** | JST-PH ($2{,}00\,\text{mm}$) | 3-Pin | **Blind-Spot Mirror LEDs (Radar BSD):** Pin 1: `+12V_PROT`, Pin 2: `BSD_LEFT_N` (switched via N-MOSFET Ch A), Pin 3: `BSD_RIGHT_N` (switched via N-MOSFET Ch B). Drives stealth amber/red LEDs on mirror stems (left/right independent; steady illumination on blind-spot approach, 8 Hz flashing on acute collision hazard). |
| **`J10`** | JST-PH ($2{,}00\,\text{mm}$) | 2-Pin | **12V Qi Smartphone Power:** Pin 1: `+12V_SW` (continuous switched power via ignition gate, up to $2{,}0\,\text{A}$ / $24\,\text{W}$), Pin 2: `GND`. Powers SP Connect / QuadLock Qi wireless charging heads on the handlebar with 0.0 µA quiescent drain at key-off. |
| **`J11`** | JST-PH ($2{,}00\,\text{mm}$) | 2-Pin | **Auxiliary Light / Fog (Adventure):** Pin 1: `+12V_AUX` (switched via smart high-side switch `TPS1H100`, up to $3{,}5\,\text{A}$ / $40\,\text{W}$), Pin 2: `GND`. Controls auxiliary fog/driving lights or automatic 4–5 Hz strobe flashing under panic braking. Left unpopulated/unused on Cruisers/Tourers. |
| **`J12`** | JST-SH ($1{,}00\,\text{mm}$) | 4-Pin | **I2C Sensor Expansion Port (Qwiic / STEMMA QT):** Pin 1: `GND`, Pin 2: `+3V3`, Pin 3: `I2C_SDA`, Pin 4: `I2C_SCL` with $4{,}7\,\text{k}\Omega$ pull-ups. Allows plug-and-play addition of ambient light sensors (`OPT3001` for automatic tunnel day/night display switching) or barometric altimeters. |

### 7.3 Automotive USB 2.0 Subsystem & Hub Architecture (`Microchip USB2514B`)

The Front Node integrates an automotive-grade 4-port High-Speed hub (`USB2514B`), completely eliminating port starvation:

| Port | Connector Type | Function & Performance Specifications |
| :--- | :--- | :--- |
| **`J4`** | JST-PH (4-Pin) | **Upstream Host Port:** Carries `USB_UP_VBUS` ($+5{,}0\,\text{V}$), `USB_UP_DM`, `USB_UP_DP`, `GND` linking the hub to the motorcycle infotainment (Harley Skyline OS / Boom! Box GTS USB input). |
| **`J5`** | JST-PH (4-Pin) | **Downstream Port 1 (Smartphone on Handlebar):** High-speed USB data line paired with **Automotive USB Power Delivery (USB-PD 20W, 9V/2.2A & QC 3.0)** via the `Southchip SC8102` fast-charge buck controller. Fast-charges smartphones even while navigating in full summer sunlight. |
| **`J6`** | JST-PH (4-Pin) | **Downstream Port 2 (Fairing Pigtail to CP2AA Dongle):** Switched $+5{,}0\,\text{V}$ VBUS via `TI TPS2051B` load switch with **1-Click Cold Restart** (2.5s power cut) and Auto-Café timer. Feeds via a shielded $25\dots 30\,\text{cm}$ cable to a commercial wireless adapter (Carlinkit / Ottocast) secured with **3M Dual-Lock** in the fairing cavity (guarantees $> 30\,\text{dB}$ RF isolation to the ESP32-S3 and zero-tool maintenance). |
| **`J5_MP3`**| JST-PH (4-Pin) | **Downstream Port 3 (Glovebox / Jukebox):** Runs as a dedicated USB lead into the bike's glovebox. Stays **100% free for local USB flash drives playing MP3/FLAC music** and official **dealer infotainment firmware updates**. |
| **`J6_AUX`**| JST-PH (4-Pin) | **Downstream Port 4 (Cockpit Accessories):** High-speed data port for dashcam storage, external Zūmo GPS, or Chigee/Carpuride displays. |
| **`J7`** | USB-C 16-Pin Receptacle | **Service & Flashing Port (right edge):** Native ESP32-S3 USB-JTAG / CDC-Serial interface for firmware upgrades and calibration (protected by TPU plug). |
| **`J8`** | JST-PH (2-Pin / 4-Pin) | **Action Cam Power Port (Charge-Only):** Dedicated $+5{,}0\,\text{V}$ DC power (up to $2{,}0\,\text{A}$) for GoPro / Insta360 / DJI — purposely without USB data to prevent headunit mass-storage lockouts. |

### 7.4 ESP32-S3 Controller Pin Mapping

| ESP32-S3 Pin | Signal Name | Direction | Function & Peripheral Assignment |
| :--- | :--- | :---: | :--- |
| **GPIO 0** | `BOOT_BTN_N` | Input | Boot mode button (Active-Low) |
| **GPIO 1** | `OTTOCAST_PWR_EN` | Output | Enable control signal for TPS2051B VBUS load switch (High = Active) |
| **GPIO 2** | `OTTOCAST_FAULT_N`| Input | Overcurrent & thermal fault flag from TPS2051B (Active-Low interrupt) |
| **GPIO 3** | `CAN_TERM_EN` | Output | Controls CPC1017N solid-state relay for 120-Ohm CAN termination (Auto-Sensing) |
| **GPIO 4** | `KL15_SENSE` | Input | Vehicle ignition monitoring via 10:1 voltage divider & Schmitt-trigger |
| **GPIO 5** | `CAN_SILENT` | Output | Drives Pin 8 (S) of CAN transceiver for hardware Listen-Only Mode |
| **GPIO 6** | `MIC_I2S_WS` | Output | I2S Word Select (LRCLK, 48 kHz) for MSM261S4030H0R / SPH0645 digital microphone |
| **GPIO 7** | `MIC_I2S_BCLK` | Output | I2S Bit Clock ($3{,}072\,\text{MHz}$) for MSM261S4030H0R / SPH0645 digital microphone |
| **GPIO 8** | `MIC_I2S_DATA` | Input | I2S Serial Audio Data from digital MEMS microphone (standard Philips I2S, wind noise tracking) |
| **GPIO 9** | `I2C_SDA` | Bidir | I2C data line for Qwiic sensor port J12 (OPT3001 light sensor) |
| **GPIO 10** | `I2C_SCL` | Output | I2C clock line for Qwiic sensor port J12 |
| **GPIO 11** | `WS2812B_DIN` | Output | Data signal for onboard WS2812B-2020 RGB status LED (light pipe in lid) |
| **GPIO 12** | `BSD_LED_LEFT` | Output | Gate control for left blind-spot mirror LED MOSFET (J9) |
| **GPIO 13** | `BSD_LED_RIGHT` | Output | Gate control for right blind-spot mirror LED MOSFET (J9) |
| **GPIO 14** | `AUX_LIGHT_EN` | Output | Enable control for TPS1H100 high-side switch (J11 aux driving light / strobe) |
| **GPIO 15** | `PTT_IN1_N` | Input | Handlebar switch 1: PTT Intercom transmit (Active-Low, Schmitt-trigger) |
| **GPIO 16** | `PTT_IN2_N` | Input | Handlebar switch 2: Action-Cam bookmark / highlight (Active-Low) |
| **GPIO 17** | `PTT_IN3_N` | Input | Handlebar switch 3: Media Next / Siri / Voice Assist (Active-Low) |
| **GPIO 18** | `USB_SERV_DM` | Bidir | Native USB D- for JTAG / CDC flashing port (J7) |
| **GPIO 19** | `USB_SERV_DP` | Bidir | Native USB D+ for JTAG / CDC flashing port (J7) |
| **GPIO 20** | `TWAI_RX` | Input | CAN Bus receive line from TI TCAN334G transceiver |
| **GPIO 21** | `TWAI_TX` | Output | CAN Bus transmit line to TI TCAN334G transceiver |

### 7.5 Status & Diagnostic LED (WS2812B with Light Pipe)

Viewable through a flush polycarbonate light-pipe lens integrated into the top enclosure lid:
* **Green breathing (1 Hz):** Normal operation, 12V stable, CAN bus active, ESP-NOW synchronized to Central Box.
* **Blue blinking:** Bluetooth LE discovery/pairing active (Action-Cam search or PWA connection).
* **Yellow steady:** CP2AA CarPlay/Android Auto dongle currently booting on Port 2.
* **Red blinking (4 Hz):** USB overcurrent or cold restart in progress (dongle hard-reboot).
### 7.6 Device Recognition & Smart Docking Logic (Qi J10 vs Handlebar USB J5 vs Glovebox J5_MP3)

To reliably differentiate between local USB audio sticks, standalone MP3 players, and charging smartphones during rides and upon parking, the Front Node utilizes a 3-tier detection matrix:

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                     DEVICE RECOGNITION MATRIX (PCBA 05 FRONT NODE)                                │
├────────────────────┬──────────────────┬─────────────────┬─────────────────┬───────────────────────┤
│ Connected Device   │ USB Enumeration  │ Charging Draw   │ BLE Rider Link  │ System Response       │
├────────────────────┼──────────────────┼─────────────────┼─────────────────┼───────────────────────┤
│ **USB Stick**      │ **Class 0x08**   │ Minimal         │ No / Irrelevant │ • Mounts MP3/FLAC     │
│ (Glove Box)        │ (Mass Storage)   │ < 100 mA (0.5W) │                 │ • No false alarm!     │
├────────────────────┼──────────────────┼─────────────────┼─────────────────┼───────────────────────┤
│ **MP3 Player**     │ **Class 0x08**   │ Low             │ No / Irrelevant │ • Reads music catalog │
│ (iPod / Clip)      │ or MTP           │ 200 - 500 mA    │                 │ • Charges slowly (5V) │
├────────────────────┼──────────────────┼─────────────────┼─────────────────┼───────────────────────┤
│ **Rider Phone**    │ Blocked (Data    │ **USB-PD 20W**  │ **YES (Active)**│ • Ride mode enabled   │
│ (Glovebox / J5)    │ restricted)      │ 9V / 1.5 - 2.2A │ Phone reports   │ • **"Phone left       │
│                    │                  │ (> 15 Watts)    │ 'charging=true' │    behind" on IGN OFF │
├────────────────────┼──────────────────┼─────────────────┼─────────────────┼───────────────────────┤
│ **Rider Phone**    │ None (Pure Qi)   │ **12V Qi Load** │ **YES (Active)**│ • Ride mode enabled   │
│ (on Qi Dock J10)   │                  │ 10W - 15W Qi    │ Phone reports   │ • **"Phone left       │
│                    │                  │                 │ 'charging=true' │    behind" on IGN OFF │
├────────────────────┼──────────────────┼─────────────────┼─────────────────┼───────────────────────┤
│ **Guest Phone**    │ Blocked          │ USB-PD or Qi    │ **NO**          │ • Neutral charge mode │
│ (Passenger)        │                  │ Fast-charge     │ (No handshake)  │ • No dashboard switch │
└────────────────────┴──────────────────┴─────────────────┴─────────────────┴───────────────────────┘
```

1. **USB Memory Stick / Jukebox in Glove Box (`J5_MP3`):**
   * Enumerates across the `USB2514B` as standard USB Mass Storage Class (`0x08`). Quiescent power draw remains negligible ($< 0{,}5\,\text{W}$).
   * The filesystem is mounted and handed off to the motorcycle headunit (Harley Skyline OS / Boom! Box) or local codec.
   * **Zero False Alarms on Departure:** Because the device is identified as permanent storage without a smartphone charging handshake, turning the ignition OFF never triggers a "Phone Left-Behind" alarm.
2. **Smartphone at Handlebar (`J5` / `J10`) or Glove Box (`J5_MP3`):**
   * The fast-charge controller registers heavy charging draw (USB-PD $9\,\text{V}$ or Qi $12\,\text{V}$) while the rider's phone simultaneously reports `battery.charging == true` over BLE $\rightarrow$ OMB confirms authorized rider docking.
   * **Single Edge-Triggered Cockpit Transition:** The WebApp switches to the Cockpit/Dashboard view **strictly once upon the rising edge** of docking. If the rider subsequently navigates to Settings, Media, or Diagnostics, that choice is strictly respected—the system never forcefully bounces the rider back.
   * **Phone Left-Behind Alert:** If the rider turns ignition OFF and walks away (BLE link drops) while Qi or USB still detects a seated device, the bike immediately gives a double horn chirp and the LoRa keyfob buzzes vigorously.

---

---

## 8. PCBA 06: MagSafe Frame Dock Adapter (`openmotorbridge_magsafe_dock`)

![PCBA 06 MagSafe Frame Dock Adapter](../images/pcba/pcba06_magsafe_dock_3d.png)

*Figure 7.6: KiCad 3D raytracing render of the MagSafe Frame Dock adapter board (PCBA 06, 28 x 11.5 mm, 2 layers) with 1206 PPTC self-resetting fuse (F1, 500 mA), SOD-323 TVS diode (D1), SOT-23-6 4-channel ESD protection array (U1, USBLC6-4SC6), 100nF decoupling capacitor (C1), horizontal M8 wire-to-board solder pad strip (J1), 6-pin MagSafe contact pad strip (J2), and central M2.5 mounting hole (H1).*

### 8.1 Purpose & Protection Architecture for Saddlebag Detachment
When the saddlebag is removed from the motorcycle (e.g. for cleaning, service, or hotel check-in), the bike-side MagSafe coupling sits exposed under the seat overhang. PCBA 06 isolates and protects the Central Box and vehicle electrical system against:
1. **Short Circuits on Exposed Pogo Pins:** Rainwater, road spray, loose keys, or metal tools trip the self-resetting **1206 PPTC polyfuse `F1`** ($I_{\text{hold}} = 500\,\text{mA}$, $I_{\text{trip}} = 1000\,\text{mA}$, $V_{\text{max}} = 16\,\text{V}$). As soon as the conductive object is removed or the contacts dry, power is automatically restored with zero fuse replacements.
2. **Inductive Switching Transients:** The **unidirectional 5V TVS diode `D1`** (SOD-323) clamps voltage spikes on the $+5\,\text{V}$ line to $< 7.0\,\text{V}$.
3. **Electrostatic Discharge (ESD):** The **4-channel ultra-low-capacitance TVS array `U1`** (USBLC6-4SC6 in SOT-23-6, $C_{\text{io}} < 0.8\,\text{pF}$) protects the differential audio lines (`SIG_P`, `SIG_N`), the optocoupler boot trigger (`TRIGGER_PPS`), and the 1-Wire ID bus (`1WIRE_ID`) to **IEC 61000-4-2 Level 4** ($\pm 15\,\text{kV}$ air discharge, $\pm 8\,\text{kV}$ contact discharge).

### 8.2 Technical PCB Specifications
* **Dimensions:** $28.0 \times 11.5 \times 1.6\,\text{mm}$ (FR-4 2 layers, $35\,\mu\text{m}$ Cu, ENIG gold finish).
* **Central M2.5 Mounting Hole:** Centered mounting hole $\varnothing 2.7\,\text{mm}$ (hole center at $X = 114.0\,\text{mm}, Y = 75.75\,\text{mm}$) with double-sided $\varnothing 4.5\,\text{mm}$ GND ring pad and keepout zone. The PCB is rigidly and torsion-free clamped between the upper and lower dock half-shells by a single central DIN 912 M2.5 screw boss.
* **Layout & Routing State:** All component footprints, 3D models (M8 horizontal receptacle, MagSafe dock connector, SMD components), net associations, and DRC clearance rules are fully defined and set up in the KiCad project, ready for manual interactive routing in the KiCad GUI.
* **Layer Stackup:**
  * **Top (F.Cu):** Component placement (F1, D1, U1, C1, J1, J2), signal and power traces.
  * **Bottom (B.Cu):** Continuous low-impedance ground plane (GND) with thermal relief and ground stitching vias.
* **DFM/DRC:** 100% compliant with JLCPCB standard 2-layer manufacturing rules.

### 8.3 Pinout & Interface Mapping

| Pin | Signal Name | Polarity / Type | Function & Protection Path |
| :---: | :--- | :--- | :--- |
| **`J1.1`** | `VCC_IN` | $+5.0\,\text{V}$ DC In | Raw power input from Central Box M8 harness (fed by LM5164 / BQ24075 UPS) |
| **`J1.2`** | `GND` | Power / Signal GND | Central ground reference, tied to solid B.Cu ground plane via thermal vias |
| **`J1.3`** | `SIG_P` | Audio Diff + / D+ | Differential Audio Positive (filtered via U1 Ch 1, protected up to $\pm 15\,\text{kV}$) |
| **`J1.4`** | `SIG_N` | Audio Diff - / D- | Differential Audio Negative (filtered via U1 Ch 2, protected up to $\pm 15\,\text{kV}$) |
| **`J1.5`** | `TRIGGER_PPS`| 3.3V Opto-Trigger | Boot/wake pulse from Central Box TLP222A PhotoMOS (filtered via U1 Ch 3) |
| **`J1.6`** | `1WIRE_ID` | Digital 1-Wire Bus| Cartridge identification bus for DS2401 Silicon Serial ROM (filtered via U1 Ch 4) |
| **`J1.7`** | `GND_SHIELD`| Cable Shield | M8 cable foil/braid shield, grounded directly to system ground on PCB |
| **`J2.1`** | `VCC_PROT` | $+5.0\,\text{V}$ DC Out | Protected MagSafe output: Post-PPTC fuse `F1`, TVS `D1`, and 100nF cap `C1` |
| **`J2.2`** | `GND` | Power / Signal GND | MagSafe ground contact (grounded via heavy B.Cu copper plane) |
| **`J2.3`** | `SIG_P` | Audio Diff + | MagSafe Pogo Pin 3: Differential audio output to saddlebag pod |
| **`J2.4`** | `SIG_N` | Audio Diff - | MagSafe Pogo Pin 4: Differential audio output to saddlebag pod |
| **`J2.5`** | `TRIGGER_PPS`| 3.3V Opto-Trigger | MagSafe Pogo Pin 5: Power-on and boot trigger to saddlebag pod cartridge |
| **`J2.6`** | `1WIRE_ID` | Digital 1-Wire Bus| MagSafe Pogo Pin 6: 1-Wire bus for detecting inserted OEM headset cartridge |

### 8.4 Bill of Materials (BOM) PCBA 06
| Ref | Component / Type | Package | Specification & Function | LCSC Part |
| :--- | :--- | :--- | :--- | :--- |
| **`F1`** | 0ZCG0050FF2C | SMD 1206 | 500 mA Hold / 1000 mA Trip, 16V PPTC Resettable Polyfuse | `C207936` |
| **`D1`** | ESD5Z5.0T1G | SOD-323 | 5.0V Unidirectional TVS Diode (VCC Transient Clamp) | `C2834585` |
| **`U1`** | USBLC6-4SC6 | SOT-23-6 | 4-Channel Low-Cap ($<0.8\,\text{pF}$, $\pm 15\,\text{kV}$) ESD Protection Array | `C7519` |
| **`C1`** | 100nF 50V X7R | SMD 0603 | Ceramic decoupling capacitor on VCC_PROT | `C14663` |
| **`J1`** | M8 Wire Pads | SMD/THT 1x07 | 7-pin wire-to-board solder pad array with 0.6mm through-holes for M8 leads | Custom |
| **`J2`** | MagSafe 6P Pads | SMD 1x06 | 6-pin gold-plated contact pads for MagSafe magnetic pogo coupling | `C224376` |
| **`H1`** | MountingHole_Pad | M2.5 (Ø 2.7 mm) | Hole Ø 2.7 mm, Pad Ø 4.5 mm, tied to System GND | Hardware |

---

## 9. PCBA 07: 2-in-1 LoRa Smart-Keyfob (`openmotorbridge_smart_keyfob`)

The PCBA 07 assembly constitutes the electronics core inside the pocket keyfob enclosure (`smart_keyfob_pager.scad`, $58 \times 34 \times 13\,\text{mm}$), overcoming the traditional weaknesses of motorcycle key fobs (exhausted CR2032 coin cells, winter sub-zero failure, and lack of two-way feedback):

![PCBA 07 2-in-1 LoRa Smart-Keyfob](../images/pcba/pcba07_smart_keyfob_3d.png)

*Figure 7.7: 3D board render of the ultra-compact PCBA 07 carrier board ($38.0 \times 19.0\,\text{mm}$) hosting the Nordic nRF52840 SoC, Semtech SX1262 LoRa transceiver, TI DRV2605L haptic driver, BQ51003 Qi receiver, and BQ25100 LiPo charger.*

```
                                PCBA 07 SYSTEM ARCHITECTURE
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        NORDIC nRF52840 BLUETOOTH LE 5.4 SoC                           │
│ • ARM Cortex-M4F @ 64 MHz, 1 MB Flash, 256 KB RAM • Hardware AES-128 Crypto Engine    │
│ • Manages BLE rider presence token, pager state, battery telemetry & smartphone bridge │
└──────────────┬─────────────────────────┬─────────────────────────┬─────────────────────┘
               │ SPI                     │ I2C                     │ PWM / GPIO
               ▼                         ▼                         ▼
┌───────────────────────────┐ ┌─────────────────────┐ ┌──────────────────────────────────┐
│ SEMTECH SX1262 LoRa       │ │ TI DRV2605L HAPTICS │ │ STATUS & ACOUSTICS               │
│ • 868 MHz Emergency RX    │ │ • I2C Haptic Driver │ │ • WS2812B RGB Status LED         │
│ • Up to 4.5 km range      │ │ • 10x3.6mm LRA Coin │ │ • Murata SMD Piezo Buzzer (85 dB)│
│ • Receives 0xFE packets   │ │   (Vybronics LRA)   │ │ • Diffuse lightpipe lens         │
└───────────────────────────┘ └─────────────────────┘ └──────────────────────────────────┘
               ▲
               │ DC 3.3V Power Rail
┌──────────────┴─────────────────────────────────────────────────────────────────────────┐
│                           POWER & INDUCTIVE CHARGING SUB-SYSTEM                        │
│ • 180–200 mAh 1S LiPo pouch cell (25 x 18 x 3.8 mm) with PCM protection board          │
│ • TI BQ51003 Qi Wireless Power Receiver: Charges inductively on PCBA 06 Cockpit Dock   │
│ • TI BQ25100 Linear LiPo charger with quiescent current < 50 nA (Months of standby)    │
│ • 2x Gold-plated pogo contact pads on bottom face for optional direct charging         │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 9.1 Technical Board Characteristics
* **Dimensions:** $38.0 \times 19.0 \times 1.0\,\text{mm}$ (Ultra-compact 2-layer FR-4, $35\,\mu\text{m}$ Cu, ENIG gold finish, corner radius $R = 3\,\text{mm}$).
* **Magnetic Flux Shielding:** Adjacent to the PCB sits the pocket for the $20 \times 10 \times 5\,\text{mm}$ N52 neodymium key. A $0.5\,\text{mm}$ soft-iron / mu-metal shield isolates RF traces, the LRA actuator, and the LiPo cell from magnetic saturation.
* **LRA Haptic Signatures:** The TI DRV2605L generates distinct, crisp tactile patterns:
  * *Pre-Alarm (Minor Shock):* 2 short clicks ($150\,\text{Hz}$).
  * *Theft / Cartridge Tamper:* Piercing crescendo staccato (readily felt through heavy leather motorcycle jackets or on a nightstand).
* **Inductive Cockpit Charging:** Snapping the keyfob onto the cockpit MagSafe frame dock (PCBA 06) centers the 28-mm receiver coil $\rightarrow$ the keyfob recharges automatically during every ride.

### 9.2 Interface & Pin-Mapping of nRF52840

| nRF52840 Pin | Signal Name | Direction | Function & Peripheral |
| :--- | :--- | :---: | :--- |
| **P0.02** | `AIN0_VBAT` | Input | Battery voltage sense via high-Z 1M/1M divider ($< 1\,\mu\text{A}$ load) |
| **P0.05** | `LRA_SDA` | Bidir | I2C Data to TI DRV2605L haptic driver |
| **P0.06** | `LRA_SCL` | Output | I2C Clock to TI DRV2605L haptic driver |
| **P0.08** | `LRA_EN` | Output | Hardware enable for DRV2605L (powers down in deep sleep) |
| **P0.12** | `LORA_SCK` | Output | SPI Serial Clock to SX1262 |
| **P0.13** | `LORA_MISO` | Input | SPI Master-In Slave-Out from SX1262 |
| **P0.14** | `LORA_MOSI` | Output | SPI Master-Out Slave-In to SX1262 |
| **P0.15** | `LORA_NSS` | Output | SPI Chip Select (Active-Low) to SX1262 |
| **P0.16** | `LORA_BUSY` | Input | SX1262 Busy status |
| **P0.17** | `LORA_DIO1` | Input | SX1262 IRQ (Received 0xFE emergency packet) |
| **P0.20** | `PIEZO_PWM` | Output | PWM drive (2.7 kHz) for Murata SMD piezo buzzer |
| **P0.22** | `WS2812_DATA`| Output | Digital data line for RGB status LED |
| **P0.24** | `CHG_STAT` | Input | Charge status from BQ25100 (Low = Charging, High = Done) |
| **P0.26** | `QI_DETECT` | Input | Digital detect flag from BQ51003 (High = Docked on Qi charger) |

### 9.3 Bill of Materials (BOM) PCBA 07
| Ref | Component / Type | Package | Specification & Function | LCSC Part |
| :--- | :--- | :--- | :--- | :--- |
| **`U1`** | nRF52840-QIAA-R | aQFN-73 | 32-Bit ARM Cortex-M4F SoC with Bluetooth 5.4, NFC & Crypto | `C190767` |
| **`U2`** | SX1262IMLTRT | QFN-24 | Semtech 868 MHz LoRa Transceiver (+22 dBm, TCXO) | `C90039` |
| **`U3`** | DRV2605LDGSR | VSSOP-10 | TI ERM/LRA Haptic Driver with embedded effect waveform library | `C61633` |
| **`U4`** | BQ51003YFPR | DSBGA-28 | TI 2.5W Qi Wireless Power Receiver Controller | `C144862` |
| **`U5`** | BQ25100YFPR | DSBGA-6 | TI Linear LiPo Charger with 50 nA quiescent current | `C144857` |
| **`M1`** | VG1036001D | Coin 10x3.6mm | Vybronics LRA Linear Resonant Actuator (235 Hz resonance) | Custom / Distrelec |
| **`BZ1`**| PKLCS1212E4001 | SMD 12x12mm | Murata SMD Piezo Transducer (85 dB @ 10 cm, 4 kHz) | `C94511` |
| **`D1`** | WS2812B-2020 | SMD 2020 | Intelligent RGB Status LED with integrated WS2811 IC | `C2843785` |
| **`BAT`**| LiPo 1S 180-200mAh| Pouch 25x18x3.8| 3.7V 180-200 mAh LiPo with PCM protection circuit & 10k NTC | EEMB / Custom |


