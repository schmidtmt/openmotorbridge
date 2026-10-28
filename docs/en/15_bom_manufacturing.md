# 15 - Bill of Materials (BOM), COTS Sourcing & SMT Manufacturing (All 7 PCBAs)

This document serves as the master reference (Single Source of Truth) for the complete Bill of Materials (BOM), manufacturing specifications for all 7 active printed circuit board assemblies (`PCBA 01`, `PCBA 03`, `PCBA 05`, `PCBA 07`, `PCBA 08`, `PCBA 09`, `PCBA 10` - `PCBA 02`, `PCBA 04` and `PCBA 06` are retired without replacement) at JLCPCB / Eurocircuits, all mechanical 3D printed components, COTS procurement lists, and a comprehensive cost and ordering strategy (Solo builder vs. Community group buy).

---

## 1. PCBA 01: Central Box Main Controller (`openmotorbridge_central_box`, 4-Layer FR4 TG150)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | LM5164-Q1 | Texas Instruments | SOIC-8-EP | C2843477 | Automotive 65V/72V Synchronous Buck Converter |
| **U2** | ESP32-S3-WROOM-1U | Espressif Systems | SMD Module | C2913200 | Host MCU (Dual-Core Xtensa LX7 @ 240 MHz, 16 MB Flash, 8 MB Octal-PSRAM) |
| **U3** | ES8388 | Everest Semi | QFN-28 (B.Cu) | C365736 | 24-Bit Stereo Audio Codec (I2S ADC/DAC) |
| **U5** | BMI270 | Bosch Sensortec | LGA-14 (B.Cu) | C2836813 | 6-Axis IMU for Lean Angle & Dynamics |
| **U6** | TCAN334G | Texas Instruments | SOIC-8 (B.Cu) | C842340 | 3.3V Automotive CAN-FD Transceiver (±58V Fault Protection) |
| **U8** | USB2517I-JZX | Microchip | QFN-64 | C136706 | Industrial 7-Port High-Speed USB 2.0 Hub Controller (-40°C...+85°C) |
| **U9** | Qualcomm QCC3084 | Qualcomm | SMD Module (13x18mm) | C-Qualcomm | Bluetooth 5.4 Audio SoC (Dual-A2DP, LE Audio Auracast, HFP 1.8 HD Voice) |
| **U10** | SX1262IMLTRT | Semtech | QFN-24 | C190184 | Onboard 868 MHz LoRa Transceiver (+22 dBm, 24/7 UPS buffered) |
| **U11** | TPS7A0533 | Texas Instruments | SOT-23-5 (B.Cu)| C2845350 | 3.3V Ultra-Low-Noise LDO for Analog & Audio Rails |
| **U12** | TPS25921 / Quad eFuse | Texas Instruments | QFN-20 | C2843580 | Quad Automotive eFuse Smart Switch (Isolated Protection for Front, Pod 1, Pod 2, Radar) |
| **D3** | LM66100DCKR | Texas Instruments | SOT-23-6 (B.Cu)| C443274 | Automotive Ideal-Diode for Ultra-Low Drop Dual-Power OR-ing (12V Main vs. USB-C 5V) |
| **D1** | WS2812B-B | Worldsemi | 5050 SMD | C114586 | Onboard RGB Status LED for Visual Mode Diagnostics |
| **SW1** | TS-1187A-C-A-B | C&K / Omron | SMD Push-Button | C318884 | Hardware Pairing & Reset Button (3s Pair, 10s Purge) |
| **Y2** | 24.000 MHz Crystal | Murata / Abracon | SMD 3225-4 | C38378 | 24.000 MHz Crystal for USB2517I USB Hub |
| **J1** | 505568-0671 | Molex | Micro-Lock Plus 1.25mm 6P Vert.| C2897372 | Cable 1: Vehicle Power & CAN Bus (KL30, KL15, GND, CAN_H, CAN_L, Shield) |
| **J6** | 90814-0016 | Molex | Picoflex 1.27mm 16P Vert. SMD | C2901234 | Cable 2: OMB 4-Channel Periphery Bus (Front 60W, Pod 1 30W, Pod 2 30W, Radar 12V) |
| **J5** | 505568-0471 | Molex | Micro-Lock Plus 1.25mm 4P Vert.| C2897370 | UPS Battery Interface (BAT+, GND, 10k NTC Thermistor, GND) |
| **J4** | 505568-0371 | Molex | Micro-Lock Plus 1.25mm 3P Vert.| C2897369 | External Enclosure RGB Status LED (5V, WS2812B DIN, GND) |
| **J7** | 505568-0471 | Molex | Micro-Lock Plus 1.25mm 4P Vert.| C2897370 | Spare USB 2.0 Port 7 (5V, D-, D+, GND) |
| **J3** | TYPE-C-31-M-12 | Korean HRO | USB-C 16-Pin SMD Receptacle | C2765186 | Front Service, DFU Flash & Diagnostic Port (USB 2.0 High-Speed) |
| **J2** | DM3D-SF | Hirose | SMD Push-Pull (B.Cu) | C266624 | 4-Bit High-Speed SDIO MicroSD Socket for Tour Logging & Offline Maps |
| **ANT1** | U.FL-R-SMT-1 | Hirose / Murata | SMD RF | C2834595 | LoRa 868 MHz U.FL socket to Taoglas FXP895 in lid |

*(Note: All PCB headers J1, J6, J5, J4, J7 point vertically UP into the housing overhead wiring channel, eliminating sharp wire bends and allowing the slide-in sled to be removed vibration-free).*

---

## 2. Satellite Pod Enclosure & Universal Mechatronics (Elimination of PCBA 02)
> **Architecture Note (v10.0 Standardized Node Architecture):**  
> The previous pod base carrier PCB `PCBA 02` and specialized cassette sleds have been **completely eliminated without replacement**.  
> The pod enclosure (`pod_base_housing.stl`) is a seamless, monolithic 1-piece 3D printed monocoque. `PCBA 03` rests vibration-damped on the enclosure floor and is powered via a shielded 4-wire bus (`VCC_BUS`, `GND`, `USB_D-`, `USB_D+`) with a 4-pin IP67 magnetic breakaway interface at the saddlebag parting line. A tool-free slide-in lid locks automatically and unlocks contact-free via an N52 magnet in the Smart Keyfob (`PCBA 07`). An EPDM dry flap protects internal electronics and the in-bag 30W USB-PD charging port from moisture.  
> **Universal Mechatronics ("One Size Fits All"):** For automated, non-destructive cold-booting of OEM intercoms (Cardo Packtalk Edge, Sena 50S/Spider, Midland) without voiding warranties or requiring manual pod disassembly, **two mini-solenoids** (JF-0530B) mount onto a continuously adjustable slide bracket (`012_universal_actuator_slide_bracket.stl`, 15–85 mm span). Upon KL15 ignition ON, `PCBA 03` energizes both actuators simultaneously for 2.0 s.

---

## 3. PCBA 03: Satellite Pod Interface Rev 4.0 (`openmotorbridge_pod_cartridge`, 4-Layer FR4 TG150, Single-Sided SMT)
> **Quantity Note:** Fitted **2x per motorcycle** (Pod 1 Left, Pod 2 Right).

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | SC8721 / TPS25750 | Southchip / TI | QFN-32 | C2843580 | Automotive USB-PD Sink Controller & Synchronous Buck-Boost (up to 30W USB-PD per pod) |
| **U2** | ESP32-C6-MINI-1U | Espressif | SMD Module (Top) | C5267233 | 32-Bit RISC-V Host MCU (manages pod profiles, USB 2.0 descriptors & power-gating) |
| **U3** | ES8388 | Everest Semi | QFN-28 (Bottom) | C2845349 | 24-Bit / 48 kHz Stereo Audio Codec (discrete L/R ADC & DAC channels) |
| **K1** | CPC1017NTR | IXYS / Littelfuse | SOP-4 | C26789 | 60V / 100mA Solid-State OptoMOS Relay for galvanically isolated PTT keying (`PTT_KEY`) |
| **Q1, Q2** | AO3400A | Alpha & Omega | SOT-23 | C20917 | 2x N-Channel MOSFETs (30V / 5.7A) for Mechatronic Cold-Start Actuators (2.0s pulse) |
| **F1** | MF-MSMF150-2 | Bourns | 1812 SMD | C22669 | PPTC 1.5A Resettable Fuse for internal USB charging rail |
| **J_BUS** | SM04B-GHS-TB | JST | 4-Pin 1.25mm SMD Horiz.| C2897370 | 4-Wire Automotive Backbone (`VCC_BUS`, `GND`, `USB_D-`, `USB_D+`) |
| **J_USBC** | TYPE-C-31-M-12 | Korean HRO | SMT/THT IP67 | C2765186 | Internal saddlebag charging receptacle for OEM headsets & smartphone (up to 30W USB-PD) |
| **J_ACT** | BM04B-SRSS-TB | JST | 4-Pin 1.0mm SMD Vert. | C160401 | Mechatronic Actuator Header (Pins: 1: VCC_ACT, 2: ACT1_DRIVE, 3: VCC_ACT, 4: ACT2_DRIVE) |
| **J_AUDIO_PWR**| BM08B-SRSS-TB | JST | 8-Pin 1.0mm SMD Vert. | C160404 | Audio & Power Header (Top-Entry, vertical, isolated PGND / AGND Kelvin grounds) |

---

## 4. Assembly PCBA 04 (Rear Pod 3): Retired Without Replacement (Clean Architecture v8.0)

> [!NOTE]
> **Architecture Streamlining v8.0:** Circuit board `PCBA 04` and the 3rd satellite enclosure (Rear Pod 3) have been **completely eliminated without replacement**:
> 1. **LoRa 868 MHz (SX1262):** Sits directly on the Central Box (`PCBA 01`), backed up 24/7 by the UPS battery for continuous anti-theft sentry.
> 2. **Multi-GNSS (SAM-M10Q):** Sits in the cool ram-air intake zone, interfaced via the modular snap-on sensor puck (`sensor_puck_environmental.stl`).
> 3. **Vehicle Backbone:** Runs over the shielded 4-wire automotive bus (`VCC_BUS` 12V/PD, `GND`, `USB_D-`, `USB_D+`), pulled without tools through the Harley frame wire caddy under the tank console (ZERO fuel tank lifting required!).
> 4. **Rear Radar:** Connects directly via Branch 4 of the 16-pin Periphery Bus (Cable 2) from the Central Box (12V Bordnetz) and transmits target telemetry over a shielded 2-wire high-speed link.

---

## 5. PCBA 05: Universal Front Node (`openmotorbridge_front_node`, 4-Layer FR4 TG150, 82 x 50 mm)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | ESP32-S31-WROOM-1U | Espressif Systems | SMD Module | `C2913200` | Dual-Core 32-Bit Xtensa LX7 (240 MHz, Vector-DSP, 8MB PSRAM, ext. U.FL) |
| **U2** | USB2514Bi-AEZG / USB2514B | Microchip | QFN-36 | `C16251` | Automotive/Industrial USB 2.0 High-Speed 480 Mbps 4-Port Hub Controller |
| **U3** | LMR36015FSCQRNXRQ1 | Texas Instruments | VQFN-12 | `C2843480` | Automotive 36V Synchronous Buck (5V / 2.0A, 91.8%) for Hub & Peripherals |
| **U4** | TPS2051BDBVR | Texas Instruments | SOT-23-5 | `C7818` | High-Side USB VBUS Power Switch (1.05A Clamp) for Port 2 Cold-Reboot Reset |
| **U5** | SC8721 / SC8102 | Southchip | QFN-32 | `C2843510` | Automotive Synchronous Buck with USB-PD 60W (5V/3A, 9V/3A, 12V/3A, 15V/3A, 20V/3A) for Smartphone Fast-Charging, GPS Nav & Cockpit Peripherals |
| **U6** | TCAN334GDCNT | Texas Instruments | SOT-23-8 | `C2843515` | 3.3V CAN Transceiver (5 Mbps CAN-FD capable, with Pin 8 Silent-Listen-Only Mode) |
| **U7** | LM5050-Q1 | Texas Instruments | SOT-23-6 (B.Cu)| `C111394` | Automotive Ideal-Diode Controller for Dual-Power Input OR-ing |
| **U8** | SAM-M10Q | u-blox | SMD Module (Top) | `C5141445` | Ultra-Low-Power Multi-GNSS Receiver (GPS/GLONASS/Galileo/BeiDou) in Sensor Puck |
| **U9** | TMP117AIDRVR | Texas Instruments | WSON-6 | `C2843535` | ±0.1°C high-precision digital I2C temperature sensor in cool airflow |
| **K1** | CPC1017NTR | IXYS / Littelfuse | SOP-4 | `C26789` | 60V / 100mA 1-Form-A Solid-State Relay for switchable 120R CAN Termination (Auto-Sensing) |
| **Q1** | DMN63D8LDW-7 | Diodes Incorporated| SOT-363 | `C283890` | Dual N-Channel MOSFET (30V / 260mA) for directional mirror blind-spot LEDs |
| **Q2** | TPS1H100BQPWPRQ1 | Texas Instruments | HTSSOP-14 | `C2843520` | Automotive Smart High-Side Power Switch (up to 3.5A / 40W) for 12V Aux Light |
| **LED1**| WS2812B-2020 | Worldsemi | SMD 2020 | `C2843530` | Digitally controllable RGB status LED for enclosure lid light pipe |
| **MIC1**| MSM261S4030H0R / SPH0645 | Knowles / Sipeed | 3.5x2.65 mm SMD | `C544577` | Digital I2S MEMS Acoustic Microphone for dynamic wind-noise compensation |
| **L1** | 4.7 µH Automotive Inductor | Sunlord / Wurth | SMD 5x5 mm | `C2843490` | Storage Inductor for LMR36015 5V Main Regulator |
| **L2** | 10 µH Automotive Inductor | Coilcraft / Wurth | SMD 7x7 mm | `C2843525` | Storage Inductor for SC8721/SC8102 60W USB-PD Fast-Charge Buck-Boost |
| **J_BUS** | SM04B-GHS-TB | JST | 4-Pin 1.25mm SMD | `C2897370` | 4-Wire Automotive Backbone (`VCC_BUS`, `GND`, `USB_D-`, `USB_D+`) to Central Box (Branch 1, 60W) |
| **J_SENSOR_EXT**| BM06B-SRSS-TB | JST | 6-Pin 1.0mm SMD Vert. | `C160403` | Modular Snap-On Sensor Puck Interface (GNSS, Temp, Light, MEMS I2C/I2S) |
| **J_POD_L** | SM04B-GHS-TB | JST | 4-Pin 1.25mm SMD | `C2897370` | Left Mirror Pod Interface (PCBA 05B: BSD LED, PTT / gesture switch) |
| **J_POD_R** | SM04B-GHS-TB | JST | 4-Pin 1.25mm SMD | `C2897370` | Right Mirror Pod Interface (PCBA 05B: BSD LED, Hazard / Cam-Tag switch) |
| **J7** | TYPE-C-31-M-12 | Korean Hro | SMD Hybrid IP67 | `C2765186` | ESP32-S3 Service & Flash Port (Flank) with TPU Sealing Plug |

---

## 5.1 PCBA 05B: Symmetrical Under-Perch Mirror Pod (`openmotorbridge_mirror_pod`, 2-Layer FR4 TG150, 24 x 18 mm)
> **Quantity Note:** The module is 100% symmetrical and fitted **2x per motorcycle** (Left under clutch perch nut, Right under brake perch nut).

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SW1** | EVQ-P2 / KMT0 | Panasonic / C&K | SMD 3.5x2.8mm IP67 | C318884 | Tactile gold-contact sealed switch for 5-gesture engine (PTT, Cam-Tag, Hazard pin) |
| **LED1-2** | Osram Amber SMD LED | ams OSRAM | SMD 0805 | C2843590 | 2x ultra-bright amber blind-spot alert LEDs (BSD), aimed at mirror glass |
| **D1** | ESD5Z5.0T1G | ON Semi | SOD-323 | C2834585 | TVS diode for ESD protection on switch contact line |
| **J1** | SM04B-SRSS-TB | JST | 4-Pin 1.0mm SMD Horiz. | C160402 | Connection to Front Node (`PTT_SIG`, `LED_BSD`, `VCC_3V3`, `GND`) |

---

## 6. PCBA 06: MagSafe Framework Dock Adapter (`openmotorbridge_magsafe_dock`, 2-Layer FR4, 28 x 11.5 mm)

| Ref | Component / Type | Package | Specification & Function | LCSC Part |
| :--- | :--- | :--- | :--- | :--- |
| **`F1`** | 0ZCG0050FF2C | SMD 1206 | 500 mA Hold / 1000 mA Trip, 16V PPTC Resettable Fuse | `C207936` |
| **`D1`** | ESD5Z5.0T1G | SOD-323 | 5.0V Unidirectional TVS Diode (Transient Protection) | `C2834585` |
| **`U1`** | USBLC6-4SC6 | SOT-23-6 | 4-Channel ESD Protection Array ($<0.8\,\text{pF}$, $\pm 15\,\text{kV}$ ESD) | `C7519` |
| **`C1`** | 100nF 50V X7R | SMD 0603 | Ceramic Decoupling Capacitor on VCC_PROT | `C14663` |
| **`J1`** | M8 Wire Pads | SMD/THT 1x07 | 7-Pin Solder Pad Array with 0.6 mm Vias for M8 Harness Conductors | Custom |
| **`J2`** | MagSafe 6P Pads | SMD 1x06 | 6-Pin Gold-Plated Landing Pads for MagSafe Magnetic Pogo Coupler | `C224376` |
| **`H1`** | MountingHole_Pad | M2.5 (Ø 2.7 mm) | Hole Ø 2.7 mm, Pad Ø 4.5 mm, tied to System GND | Hardware |

---

## 7. PCBA 07: 2-in-1 LoRa Smart-Keyfob (`openmotorbridge_smart_keyfob`, 2-Layer FR4, 38 x 19 mm)

| Ref | Component / Type | Package | Specification & Function | LCSC Part |
| :--- | :--- | :--- | :--- | :--- |
| **`U1`** | nRF52840-QIAA-R | aQFN-73 | 32-Bit ARM Cortex-M4F SoC with Bluetooth 5.4, NFC & Crypto | `C190767` |
| **`U2`** | SX1262IMLTRT | QFN-24 | Semtech 868 MHz LoRa Transceiver (+22 dBm, TCXO) | `C90039` |
| **`U3`** | DRV2605LDGSR | VSSOP-10 | TI ERM/LRA Haptic Driver with Integrated Effect Library | `C61633` |
| **`U4`** | BQ51003YFPR | DSBGA-28 | TI 2.5W Qi Wireless Power Receiver Controller | `C144862` |
| **`U5`** | BQ25100YFPR | DSBGA-6 | TI Linear LiPo Charge Controller with 50 nA Quiescent Current | `C144857` |
| **`M1`** | VG1036001D | Coin 10x3.6mm | Vybronics LRA Linear Resonant Actuator (235 Hz Resonant Frequency) | Custom / Distrelec |
| **`BZ1`**| PKLCS1212E4001 | SMD 12x12mm | Murata SMD Piezo Sounder (85 dB @ 10 cm, 4 kHz) | `C94511` |
| **`J_SWD`**| 1x04 1.27mm PinHeader | SMD 1.27mm Vert. | SWD programming header (3V3/SWDIO/SWDCLK/GND; populate for prototypes!) | `C2883733` |
| **`SW1..2`**| Alps SKRK / EVQ-P2 | SMD 3.9x2.9mm | 2x Tactile IP67 micro push-buttons (Arm/Disarm, Aux/Light) | `C115358` |
| **`D1`** | WS2812B-2020 | SMD 2020 | RGB status LED under PMMA lightpipe | `C2843785` |
| **`J_QI`**| BM02B-ACHSS-GAN-ETF | JST-ACH 2-Pin SMD (1.2mm) | 100% solderless plug connection for 24 mm Qi receiver coil (1.4 mm profile) | `C2843552` |
| **`J_BAT`**| BM02B-ACHSS-GAN-ETF | JST-ACH 2-Pin SMD (1.2mm) | 100% solderless plug connection for 180–200 mAh LiPo pouch battery with PCM | `C2843552` |

---

## 8. PCBA 08: Radar 2.0 Sub-MCU & 36-LED Wing Carrier (`openmotorbridge_radar_submcu`, 2-Layer FR4 TG150, 115 x 65 mm)

| Ref | Component / Type | Package | Specification & Function | LCSC Part |
| :--- | :--- | :--- | :--- | :--- |
| **`U1`** | ESP32-C5-WROOM-1-N8 | SMD Module | 32-Bit RISC-V Sub-MCU & 5.9 GHz V2X Uplink (2.4 GHz strictly disabled at rear) | `C2843550` |
| **`U2`** | LDO 3.3V 500mA | SOT-23-5 | TI TPS7A0533 / Richtek RT9013 LDO Voltage Regulator | `C505293` |
| **`U3`** | LM5050-Q1 | QFN-24 (4x4mm) | Qorvo Ultra-Wideband Transceiver (6.5 GHz Ch. 5/9, All-4-wire bus backbone) | `C2834570` |
| **`D1..36`**| WS2812B-2020 | SMD 2020 | 36x Digital RGB LEDs in Dual Warning Wings (18 left, 18 right, autonomous strobe) | `C2843530` |
| **`J1`** | JST-JWPF 2-Pin | Automotive IP67 | 12V Power Supply Input (`RADAR_PWR_12V` / `RADAR_GND`) | `C2834590` |
| **`J2`** | JST-SH 1.0mm 4-Pin | SMD Right-Angle| UART Interface to Wheeltec MR20 mmWave Radar (AoP patch array on front) | `C136657` |
| **`J3`** | 4-Pin 2.54mm Header| 90° Right-Angle | Flashing & Debug Header (`3V3`, `TX`, `RX`, `GND`) at housing edge | `C12437` |
| **`J4`** | Hirose U.FL | SMT Vertical | 6.5 GHz 4-wire bus Antenna Port to Taoglas FX4-wire bus10 Flex Antenna | `C14894` |
| **`U.FL_5G9`**| Hirose U.FL | SMT Vertical | 5.9 GHz V2X Antenna Port to Taoglas FXP524 Flex Antenna | `C14894` |

---

## 8b. PCBA 09: OMM 2.4 GHz Autonomous Intercom Module (`openmotorbridge_omm_ucs`, 2-Layer FR4 TG150, 60 x 30 mm)

## 8b. PCBA 09: OMM 2.4 GHz Autonomous Intercom Module (`openmotorbridge_omm_ucs`, 2-Layer FR4 TG150, 60 x 30 mm)

| Ref | Component / Type | Package | Specification & Function | LCSC Part |
| :--- | :--- | :--- | :--- | :---: |
| **`U1`** | ESP32-C6-MINI-1U | SMD Module w/ U.FL| 32-Bit RISC-V 160MHz Host MCU, Wi-Fi 6, 802.15.4 TDMA, BLE 5.3, 4MB Flash, integrated U.FL port for coax pigtail / stubby antenna | `C5267233` |
| **`U2`** | BQ24075RGTR | QFN-16 (3x3mm) | 1.5A LiPo PMIC with Dynamic Power Path Management (Zero-reboot UPS operation) | `C96825` |
| **`U3`** | XC6206P332MR | SOT-23-3 | 3.3V / 250mA Low-Iq LDO Voltage Regulator | `C5446` |
| **`U4`** | ES8388 | QFN-28 (4x4mm) | 24-Bit / 96kHz Stereo Audio Codec with separate L/R HP amps & differential mic preamp | `C365736` |
| **`U5`** | ESP32-PICO-V3-02 | QFN-48 (7x7mm) | Bluetooth Classic / BLE Co-Processor (Dual-Engine OMB Lite: HFP HD Voice, A2DP, Cross-Bridge, BLE GATT) | `C2686884` |
| **`ANT1`** | 2450AT18x100 | SMD 3216 (1.2x3.2mm) | 2.45 GHz Ceramic Chip Antenna for ESP32-PICO-V3-02 Bluetooth Co-Processor (Phone / Display link) | `C2909988` |
| **`J1`** | TYPE-C-31-M-12 | SMT/THT IP67 | Waterproof 16-Pin USB-C Receptacle (5V charging on the go via powerbank/bike, WebUSB DFU, pod dock) | `C2765186` |
| **`J_HELMET`**| SM06B-SRSS-TB | 6-Pin JST-SH 1.0mm Horiz.| Internal Helmet Audio & PTT port on B.Cu (HP_OUT_L, HP_OUT_R, AGND_SPK, MIC_IN+, AGND_MIC, BTN_PTT; 0V DC) | `C136657` |
| **`BAT1`** | BM02B-SRSS-TB | SMD 1.0mm pitch | Connection to internal 600-mAh LiPo pouch cell (with PCM) | `C2902341` |
| **`D1`** | WS2812B-2020 | SMD 2020 | RGB Status LED (Charge, Mesh channel, pairing indicator) | `C2843785` |
| **`D2`** | USBLC6-2SC6 | SOT-23-6 | High-speed TVS diode array for USB D+/D- and VBUS ESD protection | `C7519` |
| **`SW1..4`** | EVQ-P2 / KMT0 | SMD 3.5x2.8mm | 4x Tactile IP67 micro-switches (Power, Mesh, Vol+, Vol-) | `C318884` |
| **`R_NTC`** | 10k NTC 1% | 0402 | Battery temperature monitoring according to JEITA standard | `C25804` |

---

## 8c. PCBA 10: OMM 446 Analog & Digital PMR446 Module (`openmotorbridge_omm446_ucs`, 4-Layer FR4 TG150, 60 x 30 mm)

| Ref | Component / Type | Package | Specification & Function | LCSC Part |
| :--- | :--- | :--- | :--- | :---: |
| **`U1`** | ESP32-C6-MINI-1U | SMD Module w/ U.FL| 32-Bit RISC-V Host MCU, BLE 5.3 Setup, WebUSB DFU, AT-Command Engine for SA818-DMR | `C5267233` |
| **`U2`** | BQ24075RGTR | QFN-16 (3x3mm) | 1.5A LiPo PMIC with DPPM (In-operation USB charging, internal battery as UPS) | `C96825` |
| **`U3`** | SA818-DMR | SMD Module (16x38mm)| 446 MHz Analog FM & Digital DMR Tier I Transceiver (0.2W Helmet / 0.5W Bike) | `C2839211` |
| **`U4`** | ES8388 | QFN-28 (4x4mm) | 24-Bit Stereo Audio Codec for radio audio processing & helmet speakers | `C365736` |
| **`U5`** | ME6211C33M5G | SOT-23-5 | 3.3V / 500mA High-Speed Low-Dropout Voltage Regulator | `C82942` |
| **`U6`** | ESP32-PICO-V3-02 | QFN-48 (7x7mm) | Bluetooth Classic / BLE Co-Processor (Dual-Engine OMB Lite: HFP HD Voice, A2DP, Cross-Bridge, BLE GATT) | `C2686884` |
| **`ANT1`** | 2450AT18x100 | SMD 3216 (1.2x3.2mm) | 2.45 GHz Ceramic Chip Antenna for ESP32-PICO-V3-02 Bluetooth Co-Processor | `C2909988` |
| **`J1`** | TYPE-C-31-M-12 | SMT/THT IP67 | Waterproof 16-Pin USB-C Receptacle (5V DC power, charging on the go, WebUSB DFU, pod dock) | `C2765186` |
| **`J_HELMET`**| SM06B-SRSS-TB | 6-Pin JST-SH 1.0mm Horiz.| Internal Helmet Audio & PTT port on B.Cu (HP_OUT_L, HP_OUT_R, AGND_SPK, MIC_IN+, AGND_MIC, BTN_PTT; 0V DC) | `C136657` |
| **`J_RF`** | U.FL-R-SMT-1 | SMD U.FL Socket (B.Cu)| 50 Ohm U.FL RF connector for coax pigtail to waterproof SMA bulkhead or bike antenna | `C14899` |
| **`BAT1`** | BM02B-SRSS-TB | SMD 1.0mm pitch | Connection to internal 600-mAh LiPo pouch cell (with PCM) | `C2902341` |
| **`D1`** | WS2812B-2020 | SMD 2020 | RGB Status LED (RX Green, TX Red, DMR Blue, Charging Yellow) | `C2843785` |
| **`D2`** | USBLC6-2SC6 | SOT-23-6 | High-speed TVS diode array for USB D+/D- and VBUS ESD protection | `C7519` |
| **`SW1..4`** | EVQ-P2 / KMT0 | SMD 3.5x2.8mm | 4x Tactile IP67 micro-switches (PTT, Mode, Ch+, Ch-) | `C318884` |

---

## 9. 1-Click Ordering Guide for JLCPCB (All PCBAs Fully Assembled)

All manufacturing packages reside in the repository under `hardware/production_packages/` as complete ZIP and CSV archives:

| Subassembly / PCBA | Gerber ZIP Archive | BOM CSV File | CPL (Pick & Place) CSV | Layers | Manufacturing Notes |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **PCBA 01: Central Box** | `01_main_box_pcba_gerbers_jlcpcb.zip` | `01_main_box_pcba_bom_jlcpcb.csv` | `01_main_box_pcba_cpl_jlcpcb.csv` | **4 Layers** | ENIG (Gold), 1.6 mm, TG150, 2-sided SMT (LM5050-Q1 on B.Cu) |
| **PCBA 03: Universal Pod**| `03_pod_cartridge_pcba_gerbers_jlcpcb.zip` | `03_pod_cartridge_pcba_bom_jlcpcb.csv` | `03_pod_cartridge_pcba_cpl_jlcpcb.csv` | **4 Layers** | ENIG (Gold), 1.6 mm, Single-Sided SMT (Top; Order 2x per vehicle) |
| **PCBA 05: Front Node** | `05_front_node_pcba_gerbers_jlcpcb.zip` | `05_front_node_pcba_bom_jlcpcb.csv` | `05_front_node_pcba_cpl_jlcpcb.csv` | **4 Layers** | ENIG (Gold), 1.6 mm, TG150, 2-sided SMT (LM5050-Q1 on B.Cu) |
| **PCBA 05B: Mirror Pod** | `05b_mirror_pod_pcba_gerbers_jlcpcb.zip` | `05b_mirror_pod_pcba_bom_jlcpcb.csv` | `05b_mirror_pod_pcba_cpl_jlcpcb.csv` | **2 Layers** | ENIG, 1.6 mm, TG150, SMT Top (2x per bike for Left & Right, BSD LED + Button) |
| **PCBA 06: MagSafe Dock** | - | - | - | - | *Purged in v10.0* (replaced by COTS 4-Pin IP67 magnetic breakaway coupling) |
| **PCBA 07: Smart-Keyfob** | `07_smart_keyfob_pcba_gerbers_jlcpcb.zip` | `07_smart_keyfob_pcba_bom_jlcpcb.csv` | `07_smart_keyfob_pcba_cpl_jlcpcb.csv` | **2 Layers** | ENIG (Gold), 1.0 mm, 2-sided SMT |
| **PCBA 08: Radar 2.0 Sub-MCU** | `08_radar_submcu_pcba_gerbers_jlcpcb.zip` | `08_radar_submcu_pcba_bom_jlcpcb.csv` | `08_radar_submcu_pcba_cpl_jlcpcb.csv` | **2 Layers** | ENIG (Gold), 1.2 mm, TG150, SMT Top (2x U.FL, 90° pin header) |
| **PCBA 09: OMM UCS Module** | `09_omm_ucs_pcba_gerbers_jlcpcb.zip` | `09_omm_ucs_pcba_bom_jlcpcb.csv` | `09_omm_ucs_pcba_cpl_jlcpcb.csv` | **2 Layers** | ENIG (Gold), 1.0 mm, TG150, 2-sided SMT (ECE 22.06 & Pod) |
| **PCBA 10: OMM 446 UCS** | `10_omm446_ucs_pcba_gerbers_jlcpcb.zip` | `10_omm446_ucs_pcba_bom_jlcpcb.csv` | `10_omm446_ucs_pcba_cpl_jlcpcb.csv` | **4 Layers** | ENIG (Gold), 1.0 mm, TG150, 2-sided SMT (ECE 22.06 & Pod) |

---

## 10. Mechanical & Enclosure BOM (3D Printing MJF PA12 & Hardware)

All enclosure parts are strictly engineered according to the **IKEA Principle**: **Zero heat-set threaded brass inserts and zero self-tapping screws!** All enclosures exclusively feature form-fit captive hexagonal nut pockets for standard metric stainless steel nuts (DIN 934 / DIN 985), ensuring unlimited reassembly cycles without stripping threads.

### 10.1 Base System (Universal for Every Motorcycle)
| Subassembly | STL File Path | Qty | Material & Process | Function & Description |
| :--- | :--- | :---: | :--- | :--- |
| **Main Box Lower Case** | [`main_box_lower_case.stl`](../../hardware/cad/stl/01_main_box/main_box_lower_case.stl) | **1** | MJF PA12 / ASA | Monocoque tub with 4x M4 silentblock ears & sealing groove (optimized for 4-wire bus & Two-Cable architecture) |
| **Main Box Mid Tray** | [`main_box_mid_tray.stl`](../../hardware/cad/stl/01_main_box/main_box_mid_tray.stl) | **1** | MJF PA12 / ASA | Battery tray for 2,200 mAh flat LiPo ($68 \times 39 \times 5.0\,\text{mm}$), 11x convection vents & tongue-and-groove rib |
| **Main Box Lid** | [`main_box_lid.stl`](../../hardware/cad/stl/01_main_box/main_box_lid.stl) | **1** | MJF PA12 / ASA | Lid with LoRa FXP895 antenna pocket ($110 \times 20 \times 0.8\,\text{mm}$), Gore ePTFE vent seat & countersinks |
| **Pod Base Housing** | [`pod_base_housing.stl`](../../hardware/cad/stl/02_pod_base/pod_base_housing.stl) | **2** | MJF PA12 / ASA | Monolithic 1-piece tunnel enclosure with integral bulkhead, contact guides & spring posts |
| **Pod Bulkhead (Integrated)**| [`03_pod_bulkhead_partition.stl`](../../hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl) | *(integr.)* | MJF PA12 / ASA | 100% integrally molded into the monocoque housing (0 loose parts, 0 assembly screws) |
| **Pod Slide-in Lid** | [`pod_slide_lid.stl`](../../hardware/cad/stl/02_pod_base/pod_slide_lid.stl) | **2** | MJF PA12 / ASA | Tool-free slide-in lid with integral magnetic FOB latch |
| **Pod Dry-Flap** | [`pod_dry_flap.stl`](../../hardware/cad/stl/02_pod_base/pod_dry_flap.stl) | **2** | TPU 85A / EPDM | Flexible sealing and protective flap between charging bay and device bed |
| **Universal Actuator Slide Bracket**| [`012_universal_actuator_slide_bracket.stl`](../../hardware/cad/stl/02_pod_base/012_universal_actuator_slide_bracket.stl) | **2** | MJF PA12 / ASA | Continuously adjustable 15–85 mm slide guide for 2x mini solenoids in pod floor (One-Size-Fits-All) |
| **Under-Perch Mirror Pod Housing**| [`05b_mirror_pod_housing.stl`](../../hardware/cad/stl/04_front_node/05b_mirror_pod_housing.stl) | **2** | MJF PA12 / ASA | Symmetrical housing under mirror stems (Left & Right) |
| **Front Node Lower Tub** | [`front_node_lower_tub.stl`](../../hardware/cad/stl/04_front_node/front_node_lower_tub.stl) | **1** | MJF PA12 / ASA | Cockpit tub with AMPS hole pattern & tube cradle (Zero Tank-Lifting cable routing) |
| **Front Node Upper Lid** | [`front_node_upper_lid.stl`](../../hardware/cad/stl/04_front_node/front_node_upper_lid.stl) | **1** | MJF PA12 / ASA | Lid with Knowles MEMS acoustic inlet port & O-ring sealing channel |
| **Front Node Cable Glands**| [`front_node_cable_glands_tpu.stl`](../../hardware/cad/stl/04_front_node/front_node_cable_glands_tpu.stl) | **1 Pair**| TPU 95A / 85A | Flexible split sealing comb for front USB and signal wiring |
| **Front Node USB-C Cap** | [`front_node_usbc_cap_tpu.stl`](../../hardware/cad/stl/04_front_node/front_node_usbc_cap_tpu.stl) | **1** | TPU 95A / 85A | Elastic dust cap with retention tether for service port |
| **Modular Snap-On Sensor Puck**| [`sensor_puck_environmental.stl`](../../hardware/cad/stl/04_front_node/sensor_puck_environmental.stl) | **1** | MJF PA12 / ASA | Snap-on cradle for GNSS SAM-M10Q, TMP117, OPT3001 & Knowles MEMS (Bike & Car) |
| **Glovebox 4-Port Hub** | [`glovebox_power_injection_hub.stl`](../../hardware/cad/stl/04_front_node/glovebox_power_injection_hub.stl) | *Opt. (1)* | MJF PA12 / ASA | Form-fitting 4-port media & power-injection hub for right Harley Touring glovebox |
| **Fairing Tube Clamp**| [`front_node_fairing_tube_clamp.stl`](../../hardware/cad/stl/04_front_node/front_node_fairing_tube_clamp.stl) | *Opt. (1)* | MJF PA12 / ASA | 2-piece tube clamp (Ø 12–22 mm) for fairing stay & subframe struts |

### 10.2 Gateway Pod Inlays (Intercom Selection)
> **Architecture Note:** Slot 1 and Slot 2 are **Multi-Protocol Gateway Transceivers**, not rider/passenger headsets! They link the motorcycle simultaneously to Sena Mesh and Cardo DMC. Rider and pillion communicate wirelessly with their standard helmet headsets.

| Subassembly | STL File Path | Qty | Material | Function & Description |
| :--- | :--- | :---: | :--- | :--- |
| **Gateway Inlay Sena** | [`cartridge_insert_sena.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) | *Opt. (1)* | MJF PA12 / ASA | Form-fitting inlay for Sena SPIDER X Slim (Mesh 3.0 / 2.0, direct micro-cable whip) |
| **Gateway Inlay Cardo** | [`cartridge_insert_cardo.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl) | *Opt. (1)* | MJF PA12 / ASA | Inlay for Cardo Packtalk Edge / Pro (DMC Gen2) with Air-Mount cradle |
| **Gateway Inlay OMM UCS**| [`cartridge_insert_omm_ucs.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_omm_ucs.stl) | *Opt. (1..2)*| MJF PA12 / ASA | Form-fitting inlay & charging bay for OMM 2.4 GHz UCS module in pod |
| **OMM UCS Enclosure Top Shell**| [`omm_ucs_top_shell.stl`](../../hardware/cad/stl/03_pod_cartridges/omm_ucs_top_shell.stl) | *Opt. (1..2)*| MJF PA12 / ABS | Autonomous OMM UCS top shell with 4x DIN 934 M2 captive nut pockets & sealing groove |
| **OMM UCS Enclosure Bottom Shell**| [`omm_ucs_bottom_shell.stl`](../../hardware/cad/stl/03_pod_cartridges/omm_ucs_bottom_shell.stl) | *Opt. (1..2)*| MJF PA12 / ABS | Autonomous OMM UCS bottom shell with ECE 22.06 snap lugs & M2 countersinks |
| **OMM UCS Silicone Keypad**| [`omm_ucs_silicone_keypad.stl`](../../hardware/cad/stl/03_pod_cartridges/omm_ucs_silicone_keypad.stl) | *Opt. (1..2)*| Shore 50A Silicone| Seamless 100% waterproof 4-button switch pad with diffuse LED dome |
| **Blank Pod / Dry Box** | [`cartridge_insert_blindkassette.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_blindkassette.stl) | *Opt. (1)* | MJF PA12 / ASA | Hermetic protective dummy sled for unused slots or watertight dry box |

### 10.3 Vehicle-Specific Mounting Kits (3D Printed Parts)
* **Kit 1: BMW R1250 / R1300 GS (Standard / Vario Panniers):**
  * `adventure_transition_dock_base.stl` (2 pcs): Pannier-independent base cradles for the seat frame crease (Ø 28 mm tube) with 4x strap hook clearance pockets and 2-wire DC guide channel.
  * `adventure_transition_dock_lid.stl` (2 pcs): Aerodynamic body lids with transition crease & Cardo/Sena cutouts.
  * `adventure_underseat_cross_rail.stl` (1 pc): Rigid under-seat saddle bridge locking left and right docks with integrated 2-wire DC conduit.
  * `adventure_rack_radar_mount.stl` & `adventure_rack_radar_clamp_cap.stl` (1 pc each): Minimal, roost-shielded rear radar mount beneath luggage bridge (Ø 18 mm tube) with bottom-accessible M5 bolts and stone-deflector wedge.
  * `radar_swivel_tilt_cradle.stl` (1 pc): Heavy-duty swivel tilt cradle (Actioncam/GoPro-Hirth) with 2x M4 screws into radar housing.
* **Kit 2: BMW R1250 / R1300 GSA (Adventure with Ø 18 mm Stainless Rack):**
  * `adventure_gsa_cage_dock_body.stl` & `adventure_gsa_clamp_cap.stl` (2 pcs each): Heavy-duty cage docks for Pod 1 & 2 in the 45 mm dead space of the pannier frame with 85 mm dual-saddle clamp, 4x strap hook clearance pockets, stone-guard wedge & concealed 2-wire DC conduit with zip-tie anchor in tube shadow.
  * `adventure_rack_radar_mount.stl` & `adventure_rack_radar_clamp_cap.stl` (1 pc each): Roost-shielded rear radar mount under luggage bridge.
  * `radar_swivel_tilt_cradle.stl` (1 pc): Heavy-duty swivel tilt cradle with 2x M4 screws.
* **Kit 3: Harley-Davidson Touring & Classic Bagger (Street Glide, Road Glide, CVO, CVO ST, Road King Special):**
  * `saddlebag_lid_dock.stl` (2 pcs): Hard saddlebag lid mounting docks for Pod 1 & 2 with hinge Torx flange, 4x strap hook clearance pockets & 4-wire automotive strain relief.
  * `010_saddlebag_hole_grommet_split.stl` (2 pcs): Split EPDM/TPU grommet for Ø 4.2 mm 4-wire bus cable in OEM Ø 19.0 mm forward wall bore (100% Zero-Drill, above swingarm pivot) incl. U-slotted tunnel-spacer ring.
  * `radar_license_plate_bracket.stl` (1 pc): Vibration-isolated license plate radar bracket for Branch 4 (Radar).
  * `radar_swivel_tilt_cradle.stl` (1 pc): Radar 2.0 heavy-duty center-of-gravity swivel tilt cradle (Actioncam/GoPro-Hirth) with 2x M4 bolts and 36-tooth radial Hirth rosette.
  * `radar_mr20_housing.stl` & `radar_mr20_radome.stl` (1 pc): Radar 2.0 PA12 wing housing with tire roost deflector and PC radome.
  * `cots_magnetic_frame_dock_body.stl` (1 pc) & `cots_magnetic_frame_clamp.stl` (1 pc): COTS 4-pin magnetic frame dock for tool-free saddlebag removal at Ø 26 mm frame tube (optional; omitted when using pure inline-breakaway harness).
  * `glovebox_power_injection_hub.stl` (1 pc): 4-Port glovebox media & power-injection hub for right glovebox (Zero-drill pass-through, taps OEM USB-C to Skyline OS / Boom! Box, 30W phone fast charge, 10W switched dongle port, free media port; action-cam connects directly at Front Node).
  * `cockpit_speaker_corner_pod.stl` (2 pcs): Symmetrical Cockpit Display Pods for lower inner corners of Rockford Fosgate speaker grilles (Bagger / CVO ST).
* **Optional Bobber & Custom Bike Parts:**
  * `radar_center_underfender_mount.stl` (1 pc): Stealth Center Under-Fender Mount with 46 mm drop and integrated 42 mm tire roost deflector shield.
  * `radar_swivel_tilt_cradle.stl` (1 pc): Heavy-duty swivel tilt cradle with 2x M4 screws.
* **Kit 4: Support Car / Van Convoy Kit (Car-Kit / Reference Kit 5):**
  * `car_sun_visor_pod_clip.stl` (2 pcs): Quick-release spring clips for secure, vibration-free mounting of Pod 1 and Pod 2 to the sun visors in chase car or van (driver and passenger side).
  * `cockpit_breakout_block.stl` (1 pc) & `vehicle_breakout_block.stl` (1 pc): Form-fitting satellite breakout blocks for center console / armrest (cockpit) and door sill / rocker trim (vehicle).
  * `car_dashboard_wedge_dock.stl` (1 pc): Windshield base conversion wedge for remote snap-on sensor puck (`sensor_puck_environmental.stl`) in non-metallized toll window.


---

## 11. Pre-Assembled COTS Harnesses & RF Antennas (Zero Crimping, Zero Soldering!)

No custom wire harnessing or crimping is required. The system leverages 100% commercially available, industrially molded standard cables (COTS):

### 11.1 The Two-Cable Architecture of the Central Box

```text
               TWO-CABLE ARCHITECTURE (PLUG-AND-PLAY COTS FINISHED HARNESSES)
+-------------------------+
| CENTRAL BOX (PCBA 01)   |
| (Under Rider Seat)      |
+-+---------------------+-+
  |                     |
  | [J1]                | [J_PERIPH]
  v                     v
CABLE 1 (Vehicle & CAN) CABLE 2 (OMB Periphery Bus)
Deutsch DTM06-6S (IP68) 16-Pin Automotive Header (IP68)
  |                     |
  +-> Pin 1: KL30 (+12V) +-> Branch 1 (1.5 m, AWG22/28): Front Node (60W USB-PD + USB 2.0 D+/D-)
  +-> Pin 2: KL15 (Ign)  +-> Branch 2 (1.0 m, AWG22/28): Pod 1 Left (30W USB-PD + USB 2.0 D+/D-)
  +-> Pin 3: GND (Earth) +-> Branch 3 (1.0 m, AWG22/28): Pod 2 Right (30W USB-PD + USB 2.0 D+/D-)
  +-> Pin 4: CAN_H       +-> Branch 4 (0.5 m, AWG20/26): Rear Radar MR20 (12V switched + Telemetry)
  +-> Pin 5: CAN_L
  +-> Pin 6: SHIELD
```

### 11.2 The 12V Workshop & Chase Vehicle Y-Adapter Harness ("Bench & Support-Car Harness")

For laboratory testing (bench commissioning without motorcycle harness) as well as mobile deployment in convoy chase vehicles (support van, rental car, race director car), the universal **12V Y-adapter harness** is utilized. It powers Front Node and Central Box in parallel from any 12V DC power source.

**Architectural Advantage:** The USB-C port of the Central Box remains completely free on the hardware level for wired connections to the car's infotainment head unit (Apple CarPlay / Android Auto audio and display mirroring) or to a laptop (WebSerial flashing):

| Component / Subassembly | Specification / Part Number | Sourcing / P/N | Qty | Function |
| :--- | :--- | :--- | :---: | :--- |
| **12V DC Supply Plug** | Cigarette lighter plug with 5A fuse ($5 \times 20\,\text{mm}$) & LED *or* 4mm banana plugs | COTS Standard | 1 pc | Connects to 12V vehicle socket or lab power supply |
| **Main Trunk Cable** | FLRY-B $2 \times 0.75\,\text{mm}^2$ (AWG18), length $1.0\,\text{m}$ (Red: +12V, Black: GND) | Automotive wire | 1 m | Feed line to Y-junction point |
| **Branch A (Front Node)** | JST JWPF 2-Pin receptacle `02R-JWPF-VSLE-S` with socket pins `SWPR-001T-P025` | JST / Mouser | 1 pc | Pin 1: +12V (Red, KL15), Pin 2: GND (Black), lead $1.5\,\text{m}$ ($2 \times 0.5\,\text{mm}^2$) |
| **Branch B (Central Box)** | Deutsch DTM 6-Pin receptacle `DTM06-6S`, wedgelock `WM-6S`, sockets `0462-201-20141` | TE Connectivity / Mouser | 1 pc | Pin 1: KL30 (+12V), Pin 2: KL15 (+12V jumpered), Pin 3: GND (Black), lead $0.5\,\text{m}$ ($2 \times 0.75\,\text{mm}^2$) |
| **Sealing Plugs (DTM-6)** | Size 20 sealing plugs `0413-204-2005` (White/Red) | TE Connectivity | 3 pcs | IP68 sealing of unused chambers 4–6 (CAN pins) |
| **Opt. Branch C (Radar)** | JST JWPF 2-Pin receptacle `02R-JWPF-VSLE-S` with socket pins `SWPR-001T-P025` | JST / Mouser | Opt. (1)| Pin 1: +12V, Pin 2: GND, lead $0.5\,\text{m}$ ($2 \times 0.35\,\text{mm}^2$) for radar bench test |
| **Heatshrink / Y-Splice** | Raychem ATUM 4:1 adhesive-lined heatshrink or molded boot | TE Connectivity | 1 pc | Watertight, strain-relieved encapsulation of the Y-junction |

### 11.3 RF Antennas & Sensors (COTS)
1. **Shielded 4-Wire Automotive Backbone Cable (2.5 m):** 2x AWG22 + 2x AWG28 twisted with foil shield for USB 2.0 & up to 60W USB-PD.
2. **LoRa 868 MHz Flex Antenna (1 pc):** **Taoglas FXP895** ($110 \times 20 \times 0.8\,\text{mm}$) with 50 $\Omega$ U.FL feed for Central Box lid pocket.
3. **Multi-GNSS Module (1 pc):** **u-blox SAM-M10Q** with integrated $15 \times 15\,\text{mm}$ ceramic patch antenna, connected to port 5 of the Vehicle Satellite (`[ GNSS / CLIMATE PUCK ]`).
4. **Environmental Sensors (Vehicle Satellite I2C Daisy-Chain):**
   * **TI TMP117:** High-precision temperature sensor ($\pm 0.1\,^\circ\text{C}$) for black ice early warning.
5. **868 MHz Miniature Magnetic Roof Mount Antenna (1 pc, Default in Car Kit):** Compact $\varnothing 30\,\text{mm}$ magnetic base with 8 cm stainless whip (+3.0 dBi) and $2.5\,\text{m}$ RG-174 coaxial cable (SMA male) for scratch-free roof mounting (overcoming 20-30 dB chassis attenuation). Complemented by a $100\,\text{mm}$ IP67 SMA female to U.FL bulkhead pigtail with O-ring for Central Box rear knockout.

### 11.4 Internal COTS Cable Set & Pigtails for Front Node & Periphery

For all interconnections between the hermetic IP68 Front Node, the modular satellite breakout blocks, and peripherals, **factory pre-crimped COTS cables (Plug & Play)** are utilized exclusively. Zero manual crimping or field soldering is required:

| Function / Assembly | Header on PCB | Connector Type & Pitch | Mating End / Enclosure Outlet | Length | Sourcing / Model |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **Cockpit Main Harness (Motorcycle)** | Front Node `J_COCKPIT` | 16-Pin Dual-Row (2.0 mm Latch) | Cockpit Satellite (`cockpit_breakout_block`) | 50 cm | Shielded 16-conductor round cable (Ø 6.0 mm) with TPU seal |
| **Cockpit Harness (Car-Kit)** | Front Node `J_COCKPIT` | 16-Pin Dual-Row (2.0 mm Latch) | Cockpit Satellite in center console / armrest | 75 cm | High-flexibility 16-conductor drag-chain cable (compensates for 25 cm seat travel) |
| **Vehicle Main Harness** | Front Node `J_VEHICLE` | 12-Pin Dual-Row (2.0 mm Latch) | Vehicle Satellite (`vehicle_breakout_block`) | 40 cm | Shielded 12-conductor round cable (Ø 6.5 mm) with TPU seal |
| **Smartphone Charge Cable** | Cockpit Satellite Port 1 | Standard USB-C Plug | Smartphone on handlebar (with 3D strain-relief clamp) | 20–30 cm | Standard COTS USB-C to USB-C cable (angled/braided) |
| **CP2AA Wireless Dongle** | Cockpit Satellite Port 2 | USB-C or USB-A Socket | Ottocast / Carlinkit dongle in fairing | 15 cm | COTS USB cable with anti-vibration clamp |
| **OEM Upstream Host** | Cockpit Satellite Port 3 | USB-C Socket | Head unit (Harley Skyline / Boom! Box) | 30 cm | COTS USB-C to OEM USB male plug |
| **Action Cam Power Supply** | Cockpit Satellite Port 4 | USB-C Socket (Power-Only) | Action Cam (GoPro / Insta360) on handlebar/screen | 20–40 cm | COTS USB-C charging cable with strain clamp |
| **Navi 5V Power Supply** | Cockpit Satellite Port 5 | USB-C Socket (Power-Only) | GPS Navigator (Garmin / TomTom / Beeline) | 20–30 cm | COTS USB-C charging cable with strain clamp |
| **Handlebar PTT Switch** | Cockpit Satellite Terminal | Screw / Spring Terminal 2-Pin | Handlebar controls (PTT intercom / voice assistant) | 80 cm | 2-conductor control wire to handlebar switch |
| **Vehicle 12V DC In** | Vehicle Satellite Port 1 | JST-JWPF 2-Pin (IP67) | Flying leads (0.5 mm²) with Posi-Tap / Cartool plug | 50 cm | COTS JST-JWPF 2P pigtail (KL15 ignition & GND) |
| **Vehicle CAN-Bus (Motorcycle)** | Vehicle Satellite Port 2 | JST-JWPF 3-Pin (IP67) | Flying leads with Posi-Tap for CAN_H / CAN_L / GND | 50 cm | COTS JST-JWPF 3P pigtail |
| **OBD2 Car Direct Cable (Opt.)** | Vehicle Satellite Port 2 | JST-JWPF 3-Pin (IP67) | Flat 90° OBD2 male connector in driver footwell | 80 cm | Ultra-flat ribbon cable (10 mm profile, zero pedal conflict) |
| **Mirror BSD Warning LEDs**| Vehicle Satellite Port 3 | JST-JWPF 3-Pin (IP67) | Y-cable ($2 \times 2$-Pin) to amber mirror LED indicators | 120 cm | COTS JST-JWPF 3P Y-pigtail |
| **Auxiliary Light Output** | Vehicle Satellite Port 4 | JST-JWPF 2-Pin (IP67) | 2-pin flying leads to driving lights / strobe relay | 40 cm | COTS JST-JWPF 2P pigtail |
| **Qwiic / GNSS I2C Bus** | Vehicle Satellite Port 5 | JST-SH 4-Pin (1.0 mm) | 4-Pin JST-SH connector to SAM-M10Q & TMP117 puck | 10–20 cm | SparkFun Qwiic / Adafruit STEMMA QT COTS |
| **MR20 Radar Interconnect**| Radar PCBA 08 `J2` | JST-SH 4-Pin (1.0 mm) | 4-Pin JST-SH connector directly to Wheeltec MR20 module | 40-50 mm | COTS JST-SH 4P to JST-SH 4P |
| **Central Box CarPlay Port**| Central Box `J3` | IDC 10-Pin (2.54 mm) | Waterproof panel-mount USB-C receptacle (IP67) | 15 cm | COTS IDC-10 to USB-C panel-mount |
| **UPS LiPo Battery Plug** | Central Box `J5` | JST-PH 4-Pin / Molex | Integrated harness with NTC of 2,200 mAh LiPo pack | 8 cm | Pre-crimped on LiPo battery pouch |

### 11.5 Gateway Adapter Cables for OEM Intercoms (Header `J_AUDIO_PWR` / 8-Pin JST-SH)

To operate commercial OEM intercom modules completely non-destructively and without voiding factory warranties, the 8-pin **JST-SH 1.0 mm Header `J_AUDIO_PWR`** on `PCBA 03` connects to model-specific COTS adapter cable harnesses. Complete physical separation of high-current power return (`PGND`) and audio references (`AGND_SPK`, `AGND_MIC`) eliminates all ground-loop charging and Mesh TDMA buzzing:

| Headset Model / Class | Adapter Cable Type & Connectors | 8-Pin JST-SH Header Pinout | Length | Function & Key Features |
| :--- | :--- | :--- | :---: | :--- |
| **Sena SPIDER X Slim**<br>*(OMB Reference K2a)* | **8-Pin JST-SH to 3-Way Pigtail:**<br>- 2-Pin Micro-JST (Direct-DC 3.85V)<br>- 2.5 mm Jack (Mic In)<br>- 3.5 mm Stereo Jack (Spk Out) | **Pin 1:** `PGND` (Power Return)<br>**Pin 2:** `VCC_5V_PROT` (Feed to MP2315 step-down $\rightarrow 3.85\,\text{V}$)<br>**Pin 3:** `AGND_AUDIO_IN` (Audio Ground Sleeve, $I = 0\,\text{mA}$)<br>**Pin 4:** `AUDIO_IN_L` (Spk L $\rightarrow$ ES8388 Line-In L)<br>**Pin 5:** `AUDIO_IN_R` (Spk R $\rightarrow$ ES8388 Line-In R)<br>**Pin 6:** `OMM_DETECT` (**GND jumper inside connector** $\rightarrow$ holds `U4` in NC/Analog)<br>**Pin 7:** `AUDIO_IO_P` (`VOICE_OUT` from ES8388 DAC $\rightarrow$ Sena Mic)<br>**Pin 8:** `PTT_USB_N` (N/C) | 8 cm | **Zero Pogo-Pins & Zero Hum:** Direct 3.85V battery-free supply. High DC return current flows solely across Pin 1 (`PGND`). Audio lines stay 100% hum-free over zero-current Pin 3! |
| **Cardo Packtalk Edge / Pro**<br>*(Class 4 DMC Gen2)* | **8-Pin JST-SH to 3.5mm, Micro-2Pin & 90° USB-C:**<br>- 3.5 mm Stereo Jack (Spk Out L/R)<br>- Cardo 2-Pin Micro Plug (Mic In)<br>- Right-Angle USB-C (5V Charge Port) | **Pin 1:** `PGND` (USB-C charge return up to 500 mA)<br>**Pin 2:** `VCC_5V_PROT` (USB-C 5V charge & run power)<br>**Pin 3:** `AGND_AUDIO_IN` (Audio Ground Sleeve, $I = 0\,\text{mA}$)<br>**Pin 4:** `AUDIO_IN_L` (Spk L $\rightarrow$ ES8388 Line-In L)<br>**Pin 5:** `AUDIO_IN_R` (Spk R $\rightarrow$ ES8388 Line-In R)<br>**Pin 6:** `OMM_DETECT` (**GND jumper inside connector** $\rightarrow$ holds `U4` in NC/Analog)<br>**Pin 7:** `AUDIO_IO_P` (`VOICE_OUT` from ES8388 DAC $\rightarrow$ Cardo Mic)<br>**Pin 8:** `PTT_USB_N` (N/C) | 10 cm | Connects Air-Mount cradle or pogo pads. 500 mA charging current returns across Pin 1; audio lines stay completely decoupled on pins 3, 4, 5, and 7 -- zero charging whine in helmet! |
| **OpenMotorMesh (OMM) 2.4 GHz / 446**<br>*(Class C/D Native UCS)* | **8-Pin JST-SH to USB-C (90° Angled, 4-Conductor):**<br>- 8-Pin JST-SH 1.0mm Socket<br>- Right-Angle USB-C Plug (VBUS, GND, D+, D-) | **Pin 1:** `PGND` (USB-C GND Power Return)<br>**Pin 2:** `VCC_5V_PROT` (USB-C VBUS 5V supply & UPS charge)<br>**Pin 3..5:** N/C (Analog paths unpopulated)<br>**Pin 6:** `OMM_DETECT` (**Open / N/C** $\rightarrow$ `R9` pulls to 3.3V $\rightarrow$ `U4` switches to NO/Digital)<br>**Pin 7:** `AUDIO_IO_P` $\rightarrow$ USB-C D+ (`USB_DP` native digital audio stream)<br>**Pin 8:** `PTT_USB_N` $\rightarrow$ USB-C D- (`USB_DN` native digital audio stream) | 5 cm | **Pure Digital USB 2.0 Full-Speed Audio Channel:** Losslessly transfers digital PCM/Opus audio stream between ESP32-C6 host (`PCBA 03`) and OMM module (`PCBA 09`/`10`). Zero D/A conversion losses, zero common-impedance hum. |

### 11.6 Mechatronic Cold-Start & Digital 4-Wire Automotive Bus

In OpenMotorBridge v10.0, automated mechatronic cold-start boot is handled via 2 mini-solenoids on the universal slide bracket (2.0 s simultaneous pulse upon KL15 ignition ON via `J_ACT` / dual AO3400A MOSFETs on PCBA 03), while routine PTT and media control is handled digitally via BLE GATT / AVRCP or direct OptoMOS PTT keying:

1. **Mechatronic Cold-Start Actuators (JF-0530B):**
   * Two mini linear solenoids (12V DC, 300 mA, 10 mm stroke, ~4 N push force) fitted with soft Shore A50 silicone caps mounted on `012_universal_actuator_slide_bracket.stl`. They physically actuate OEM intercom buttons (e.g. Cardo Intercom + Media, Sena Phone + Jog button) for 2.0 s upon KL15 power-up, waking dormant intercoms without voiding warranties or draining batteries in standby.
2. **4-Wire Automotive Bus Cable:**
   * **Specification:** Shielded 4-conductor automotive cable (2x AWG22 power `VCC_BUS` / `GND`, 2x AWG28 twisted `USB_D-` / `USB_D+`).
   * **Routing:** From Central Box harness through Harley frame caddy (ZERO tank removal) to saddlebag breakaway coupling.
3. **OptoMOS PTT Keying (`CPC1017N`):**
   * Keys analog radios (Midland PMR446) or audio ports bounce-free in $< 10\,\mu\text{s}$ against ground.
4. **USB-PD Power-Cycling & In-Bag Fast Charge:**
   * Powers OEM communicators ON and OFF gracefully via software power-gating and supplies up to 30W USB-PD fast charging per pod.

### 11.7 Pannier Disconnect (Industrial 2-Pin Magnetic Pogo "MagSafe Replacement") & Mounting

Instead of the former proprietary `PCBA 06` board, the tool-free pannier breakaway connection is engineered as a **pure 2-wire DC system (5V / GND)** with an industrial **2-Pin Magnetic Pogo Breakaway Coupler (IP68 COTS)**:

```text
                  THE 2-PIN MAGNETIC POGO SADDLEBAG DISCONNECT (IP68 COTS)
  +--------------------+                                    +--------------------+
  | BIKE FRAME         |                                    | HARD SADDLEBAG     |
  | (Under rider seat  |                                    | (Pannier / Vario)  |
  |  at Ø 26 mm tube)  |                                    |                    |
  | [cots_magnetic_    |     Magnetic Breakaway Coupling    | [010_saddlebag_    |
  |  frame_dock.stl]   |     (10 - 15 N axial hold force)   |  grommet_split.stl]|
  |   +--------------+ |             (Click!)               | +----------------+ |
  |   | 2-Pin Magnet-| | <================================> | | 2-Pin Magnet-  | |
  |   | Pogo SOCKET  | |                                    | | Pogo PLUG      | |
  |   +-------+------+ |                                    | +-------+--------+ |
  +-----------|--------+                                    +---------|----------+
              | 2x 0.5 mm² PUR                                        | 2x 0.34 mm² Ribbon
              v                                                       v (on lid tether)
        [Central Box J1]                                      [Saddlebag Lid Dock]
```

1. **The Magnetic Coupler (COTS):**
   * Industrial 2-Pin magnetic pogo connector (type **HytePro M411 / COTS 2-Pole Magnetic Coupling**, IP68 waterproof with gold-plated pogo pins and N52 neodymium ring magnets).
   * Electrical parameters: Up to $2.5\,\text{A}$ continuous current at $12\,\text{V}/5\,\text{V}$ DC; contact resistance $< 30\,\text{m}\Omega$.
   * **Mechanic-Proof Breakaway:** Disconnects non-destructively under $10\dots 15\,\text{N}$ axial pull if luggage is removed in shop or hotel without uncoupling. Self-aligns upon reinstallation.
2. **Mechanical Frame Mounting (Bike Side):**
   * **Option A (Elastic Inline Breakaway Harness - Standard for Adventure Bikes):** The magnetic coupler floats inline, sealed in resin and adhesive-lined heatshrink, held by an EPDM clip or cable tie to frame tube or passenger footpeg bracket. Zero rigid frame dock required.
   * **Option B (Stationary COTS Frame Dock for Baggers/Harley):** Sits form-fitting inside [`cots_magnetic_frame_dock.scad`](../../hardware/cad/scad/02_pod_base/parts/cots_magnetic_frame_dock.scad). Clamped to Ø 25.4–28.6 mm frame tube via `cots_magnetic_frame_clamp.stl` with 4x M3 screws into captive DIN 934 nut pockets (100% solder-free).
3. **Mechanical Saddlebag Mounting (100% Zero-Drill):**
   * **Mounting Location:** Forward OEM saddlebag mounting bore (above swingarm pivot) in complete spray shadow.
   * **100% Zero-Drill (OEM $\varnothing 19.0\,\text{mm}$ Hole):** Factory rubber isolator is removed; pre-assembled OMB harness slides smoothly through bare $\varnothing 19\,\text{mm}$ bore without de-pinning.
   * **Split Grommet & U-Tunnel Spacer Ring:** Split EPDM/TPU grommet ([`010_saddlebag_hole_grommet_split.scad`](../../hardware/cad/scad/02_pod_base/parts/010_saddlebag_hole_grommet_split.scad)) wraps around cable and M8 sleeve. A C-slotted 4 mm PA12-CF/Alu spacer transfers clamping force directly to the sleeve, keeping 360° lever freedom. Saddlebag remains 100% watertight (IP67).
   * **Integral Stage-1 Strain Relief:** Cable tie tower on grommet anchors cable. Any $10\dots 15\,\text{N}$ pull transfers into the saddlebag wall, never straining internal wiring.

### 11.8 OMM UCS Helmet Accessories: Audio Harness, RF Coaxial Pigtails & Stubby Antennas

For standalone helmet operation of both intercom modules (**PCBA 09: OMM 2.4 GHz HD-Mesh** and **PCBA 10: OMM 446 PMR/DMR**) in standard ECE 22.06 UCS slots, commercially available COTS accessories provide plug-and-play assembly:

1. **OMM UCS Helmet Audio & PTT Harness (`J_HELMET` Pigtail):**
   * **PCB Side:** 6-Pin JST-SH female connector ($1.0\,\text{mm}$ pitch, gold-plated crimp contacts, positive snap-lock to header `J_HELMET` on `B.Cu`).
   * **Wire Harness:** High-flex AWG30/32 silicone wires (halogen-free, flexible routing beneath helmet cheek pads, length $120\dots 150\,\text{mm}$).
   * **Helmet Interfacing:**
     - **Speakers:** $3.5\,\text{mm}$ inline gold-plated stereo jack for 40 mm helmet speakers (JBL, Sena HD) carrying Pin 1 (`HP_OUT_L`), Pin 2 (`HP_OUT_R`), and Pin 3 (`AGND_SPK`).
     - **Microphone:** 2-Pin Micro-JST / Molex PicoBlade socket for boom or adhesive ECM microphone carrying Pin 4 (`MIC_IN+`) and Pin 5 (`AGND_MIC`).
     - **PTT Switch:** 2-conductor lead to weather-sealed velcro/finger PTT button carrying Pin 6 (`BTN_PTT`) keyed to GND.
   * **Zero Charging Whine / Hum:** The harness carries **0 V DC power**. Ground-loop hum and switching noise from charging regulators are physically impossible!
   * **Grommet Routing:** Exits smoothly through the $7.0 \times 9.0\,\text{mm}$ floor cutout in the lower shell directly into helmet liner recesses.

2. **RF Micro-Coaxial Pigtail (U.FL to SMA Bulkhead):**
   * **Coax Cable:** 50 $\Omega$ low-loss micro-coax (RG-178 with FEP jacket or $\varnothing 1.13\,\text{mm}$ silver-plated, length $45\dots 50\,\text{mm}$, shielding $> 60\,\text{dB}$, insertion loss $< 0.15\,\text{dB}$).
   * **PCB Side:** IPEX MHF1 / U.FL female snap connector (clicks onto `U1` on PCBA 09 or `J_RF` on PCBA 10).
   * **Enclosure Side:** SMA-Female Bulkhead jack (1/4"-36 UNS thread with D-cut flat anti-twist profile).

3. **IP67 Antenna Feedthrough (Bulkhead with O-Ring):**
   * **Seal:** UV- and ozone-resistant EPDM / Silicone O-ring (Shore 60A, $\varnothing 6.0 \times 1.0\,\text{mm}$).
   * **Fastening:** A4 / 316 stainless steel hex nut with internal star lockwasher for vibration-proof retention.
   * **Fitment:** Seats inside the $5.0 \times 4.0\,\text{mm}$ cutout at the $+X$ flank of the OMM UCS enclosure ([`omm_ucs_bottom_shell.scad`](../../hardware/cad/scad/03_pod_pods/parts/omm_ucs_module.scad)) to maintain IP67 water and dust sealing.

4. **Compact Helmet Stubby Antennas (COTS Stubby Antennas):**
   * **Stubby Antenna 1 (OMM 2.4 GHz HD-Mesh, PCBA 09):**
     - 2.4 GHz ISM band stubby antenna ($2400\dots 2500\,\text{MHz}$), $+2.0\dots +2.5\,\text{dBi}$ omnidirectional gain.
     - SMA-Male connector, overall length only **$35\dots 40\,\text{mm}$**, diameter $\varnothing 8\,\text{mm}$, weight approx. $6\,\text{g}$.
     - Rubber-duck flexible TPU jacket prevents helmet buffeting, wind whistle, and lever forces at highway speeds.
   * **Stubby Antenna 2 (OMM 446 MHz PMR/DMR, PCBA 10):**
     - 446 MHz PMR446 / DMR Tier I stubby antenna ($430\dots 470\,\text{MHz}$, resonant at $446.1\,\text{MHz}$), approx. $0\dots +1.5\,\text{dBi}$ gain.
     - SMA-Male connector, length approx. **$45\dots 50\,\text{mm}$**, diameter $\varnothing 10\,\text{mm}$, weight approx. $9\,\text{g}$.
     - Shortened helical coil inside flexible shock-damping rubber jacket. Delivers $1.5\dots 2.5\,\text{km}$ range with full rider ergonomics.

5. **Optional Fixed-Installation Upgrade in Pod Pod (5V COTS Bi-Directional Booster / LNA):**
   * **Purpose:** For permanent fixed installations of OMM modules in sealed pods (`has_sma_port = false`), compensating for luggage lid and rider body shadowing without external holes or appendages.
   * **Specification:** Ultra-compact 5V bi-directional RF booster module ($25 \times 15\,\text{mm}$) featuring an integrated Low-Noise Amplifier (+12 dB RX gain, NF < 2.5 dB) and automatic T/R power detection.
   * **100% Modular Decoupling:** Seats form-fittingly in the rear cradle bay of `pod_insert_omm_ucs.scad` and draws 5V from `PCBA 03`. The universal carrier board `PCBA 03` remains completely untouched and identical across Sena and Cardo pods.
   * **Power Supply via 2-Pin Branch from `J_AUDIO_PWR`:** The 5V DC supply ($< 100\,\text{mA}$) branches directly off **Pin 1 (`PGND`)** and **Pin 2 (`VCC_5V`)** of the 8-pin pod gateway harness. Because the booster return current flows exclusively across `PGND` and the audio ground lines (`AGND_SPK`, `AGND_MIC`) remain zero-current, Kelvin ground isolation is 100% maintained – zero common-impedance RF whine in helmet audio!

---

## 12. COTS Hardware & Fastener Procurement List (1 Complete Kit)

<!-- AUTOGEN_BOM_TABLE_START -->

| Component | Specification / Type | Sourcing Source | Qty (Ref-Set) | Location & Purpose |
| :--- | :--- | :--- | :---: | :--- |
| **3M Dual Lock SJ3550 Fastener** | Pilzkopf-Klettband selbstklebend (VHB-Kleber) | 3M / Amazon | 0.5 m | Rattle-free tool-less mounting of dongles and sensors in cockpit and luggage |
| **3M VHB R130 Adhesive Pad** | 3M VHB R130 Hochleistungs-Klebepad passgenau | 3M / COTS | 1 pcs | Vibration-proof & weatherproof ECE 22.06 helmet mounting for OMM UCS cradle |
| **Ejector Spring (Bulkhead)** | Edelstahl V4A D = 4.5 mm, L0 = 15 mm | Gutekunst / Web | 4 pcs | Auto-eject springs inside pod bulkhead (2x per pod, ejects cartridge 25 mm upon unlock) |
| **Stainless Steel Lanyard Bushing (Keyfob)** | 316L V4A Ø 8.5 x 4.5 mm, L = 13 mm | Normteil / Misumi | 1 pcs | Press-fit stainless bushing inside solid block of keyfob lanyard eyelet |
| **M2 Stainless Nut (Captive UCS)** | DIN 934 M2 V4A | Normteil / Amazon | 8 pcs | Captive nuts in upper shell pockets of OMM UCS module (4x per module) |
| **M2 Retainer Plate Screw (Countersunk)** | DIN 7991 V4A M2 x 6 mm | Normteil / Amazon | 8 pcs | Retaining actuator clamping bridge plates (4x per gateway cartridge) |
| **M2 Cartridge PCB Screw** | DIN 7985 / DIN 912 V4A M2 x 6 mm | Normteil / Amazon | 8 pcs | Securing PCBA 03 in cartridge sled (4x per cartridge; bulkhead screws eliminated) |
| **M2 Rocker Pivot Pin** | DIN 7 V4A Zylinderstift M2 x 8 mm | Normteil / Misumi | 2 pcs | Precision pivot axle for magnetic cartridge locking rocker inside sled |
| **M2 UCS Module Screw** | DIN 912 V4A M2 x 8 mm | Normteil / Amazon | 8 pcs | Fastening OMM UCS housing shells (4x per module, threads into M2 captive nuts) |
| **M2.5 PCB Mounting Screw** | DIN 912 V4A M2.5 x 6 mm | Normteil / Amazon | 10 pcs | Fastening main controller boards (4x Central Box PCBA 01, 4x Front Node PCBA 05) |
| **M3 Stainless Nut (Captive)** | DIN 934 / DIN 985 M3 V4A | Normteil / Amazon | 10 pcs | Captive in nut pockets (Central Box, Front Node, frame dock – zero heat-set inserts!) |
| **M3 Front Screw (Front Node)** | DIN 912 V4A M3 x 20 mm | Normteil / Amazon | 4 pcs | Front Node enclosure lid fastener into captive nut pockets |
| **M3 Enclosure Screw (Main Box)** | DIN 912 V4A M3 x 40 mm | Normteil / Amazon | 4 pcs | Central box enclosure fastener (threads from top into bottom tub nut pockets) |
| **M3 Clamp Screw (Dock / Clamp)** | DIN 912 V4A M3 x 16 mm | Normteil / Amazon | 2 pcs | Frame clamp cots_magnetic_frame_dock / transition dock clamp |
| **M4 Stainless Nut (AMPS & Radar)** | DIN 934 M4 V4A | Normteil / Amazon | 6 pcs | 4x Front Node tub (AMPS pockets), 2x Radar 2.0 rear housing |
| **M4 Screw (Radar Cradle)** | DIN 912 V4A M4 x 12 mm | Normteil / Amazon | 2 pcs | Securing adapter bracket radar_swivel_tilt_cradle to Radar 2.0 housing |
| **M4 Anti-Vibration Silentblocks** | Typ A M4 Außen/Innen Ø 15 x 10 mm | Ganter / Normteil | 4 pcs | Vibration-decoupled 4-point mounting of Central Box on bike frame (damps 10-100 Hz) |
| **M5 Clamp Screw (Hirth & Tube Clamps)** | DIN 912 V4A M5 x 25 mm | Normteil / Amazon | 3 pcs | Horizontal axis bolt for Hirth gear lock joints & round tube clamps (Ø 12-22 mm) |
| **M5 Lock Nut / Stainless Nut** | DIN 985 / DIN 934 M5 V4A | Normteil / Amazon | 3 pcs | Captive lock nuts in radar forks and tube clamp caps |
| **Steel Armature Pin (Cartridge)** | DIN 6325 gehärteter Passstift Ø 6 x 8 mm | Normteil / Misumi | 2 pcs | Ferromagnetic steel armature inside rocker lever (actuated by N52 magnetic key) |
| **N52 Magnetic Release Key** | N52 Neodym-Block 20 x 10 x 5 mm (vernickelt) | Supermagnete / Web | 2 pcs | Contactless magnetic key for anti-theft ejection of pods from motorcycle bays |
| **Rocker Return Spring** | Edelstahl V4A Ø 3.5 mm, L0 = 10 mm | Gutekunst / Web | 2 pcs | Keeps cartridge locking claw securely engaged with 2.5 N preload |
| **Gore ePTFE Pressure Vent** | Ø 12 mm selbstklebendes ePTFE Membran-Patch IP68 | Gore / COTS | 1 pcs | Pressure equalization & condensation prevention in Central Box lid pocket |
| **Cartridge Flange Mouth Gasket** | Silikon-Formdichtung Shore 40A (54 x 18 mm) | Sonderfertigung / Silikon | 2 pcs | Front mouth-opening seal on Pod 1 and Pod 2 against road spray and rain |
| **OMM Silicone Gasket Cord Ø 0.8 mm** | Silikon-Rundschnur Ø 0.8 mm Shore 40A | O-Ring-Shop / Web | 0.4 m | Ultra-flexible housing seal for OMM UCS enclosure (approx. 22 cm per module, IP67) |
| **Silicone Sealing Cord Ø 1.5 mm** | Silikon-Rundschnur Ø 1.5 mm Shore 40A | O-Ring-Shop / Amazon | 0.7 m | Continuous sealing cord for Central Box (40 cm) & Front Node (30 cm) groove for IP67 |
| **1S LiPo Pouch Battery 180-200 mAh (Keyfob)** | 3.7V / 0.74Wh (Typ 402030, 25x18x3.8 mm) mit PCM & JST-ACH 2-Pin | EEMB / Web | 1 pcs | Flat LiPo pouch for Smart Keyfob (100% solderless with JST-ACH 2P plug) |
| **1S LiPo Pouch Battery 600 mAh (OMM)** | 3.7V / 2.22Wh (Typ 452438) mit PCM & JST-ACH | EEMB / Web | 2 pcs | Internal battery for OMM UCS modules (12-14 h standalone helmet runtime) |
| **5V DC Miniature Solenoid** | Ø 6.5 x 12 mm, Hub 1.5-2.0 mm, mit TPU-Dämpfungsspitze | Solenoid / Web | 8 pcs | Mechatronic pushers actuating Sena & Cardo buttons (4x per smart slot) |
| **Helmet Speakers & ECM Mic Kit** | 40 mm 32 Ohm Hi-Fi Stereo-Lautsprecher + ECM Schwanenhalsmikrofon | COTS Audio / Web | 1 Set | Plug-and-play audio peripherals for OMM UCS headset inside helmet |
| **IP67 DC Direct Plug (CON_POD_DC)** | 2-Pin Automotive Blade mit axialem NBR70 O-Ring & Edelstahl-U-Clip | COTS Automotive / Web | 2 pcs | Tool-free locking IP67 direct blade plug for Pod 1 & 2 power feed (100% solder-free) |
| **Polycarbonate Radome Window** | Laserzuschnitt Polycarbonat 1.6 mm (RF-transparent) | COTS / Plexiglas | 1 pcs | Microwave & optical window for MR20 radar & 24-LED Halo |
| **Buffer Battery (LiPo UPS 2,200 mAh)** | 1S 3.7V 2.200 mAh Flat-Pack (Typ 504068) Molex Micro-Fit | EEMB / Enerpower | 1 pcs | Seamless UPS reserve in Central Box during engine cranking & ignition off |
| **Qi Inductive Receiver Coil Ø 24 mm** | Ø 24 x 0.3 mm Flachspule mit Ferritfolie (0.3 mm) & JST-ACH 2-Pin | Sunlord / Web | 1 pcs | Ultra-thin Qi receiver coil for Smart Keyfob (100% solderless plug connection) |
| **Wheeltec MR20 77-GHz mmWave Radar** | 77-GHz FMCW Automotive Radar (150 m Reichweite) | Wheeltec / DE-Distributor | 1 pcs | Automotive mmWave radar for blind spot detection & forward/rear collision alert |
| **u-blox SAM-M10Q Multi-GNSS Module** | 15x15 mm Keramik-Patchantenne, Qwiic I2C | SparkFun / u-blox | 1 pcs | Satellite navigation on 5-port Vehicle Satellite with clear zenith view |
| **OMM 2.4 GHz Stubby Antenna** | 2.4 GHz Rubber-Duck (38 mm, SMA-Male, +2.5 dBi omni) | COTS Standard | 1 pcs | Compact helmet stubby antenna for PCBA 09 (zero buffeting or wind noise) |
| **Taoglas FXP524 V2X Flex Antenna** | 5.9 GHz Flex-Patch (+3.5 dBi) mit U.FL Buchse (50 mm) | Taoglas / Mouser | 1 pcs | Car-to-X / ITS-G5 RF uplink for ESP32-C5 sub-MCU on PCBA 08 |
| **Taoglas FXP73 2.4 GHz FPC Flex Antenna** | 2.4 GHz FPC Klebeantenne (+2.5 dBi) mit U.FL (50 mm) | Taoglas / Mouser | 1 pcs | Internal antenna along cartridge sled cavity for sealed pod operation |
| **Taoglas FXP895 LoRa Flex Antenna** | 868 MHz Flex-Dipol (+2.0 dBi) U.FL (100 mm) | Taoglas / Mouser | 1 pcs | Long-range convoy mesh for SX1262 LoRa in Central Box lid cavity |
| **Taoglas FXUWB10 UWB Flex Antenna** | 6.5 GHz Ch. 5 Flex-Patch mit 20 mm U.FL Koaxialkabel | Taoglas / Mouser | 5 pcs | Wireless UWB 6.5 GHz backbone (Central Box, Front Node, Cartridges, Radar) |
| **COTS USB-C Smartphone Cable** | Standard USB-C auf USB-C Kabel (20-30 cm, gewinkelt/geflochten) | Amazon / COTS | 1 pcs | Connection from Cockpit Satellite to smartphone with strain relief |
| **Cockpit Harness 16-Conductor (Shielded)** | 16-poliges geschirmtes Rundkabel (Ø 6.0 mm, 50 cm) mit 2.0 mm Verriegelungsstecker | COTS Standard | 1 pcs | Connects PCBA 05 J_COCKPIT to Cockpit Breakout Satellite |
| **Deutsch DTM-12 Main Harness** | IP68/IP69K Deutsch DTM-12 COTS Fertigkabelbaum mit Raychem DR-25 | COTS / Deutsch | 1 pcs | Central main harness for bike power, CAN bus & DC leads to pods |
| **Vehicle Harness 12-Conductor (Shielded)** | 12-poliges geschirmtes Rundkabel (Ø 6.5 mm, 40 cm) mit 2.0 mm Verriegelungsstecker | COTS Standard | 1 pcs | Connects PCBA 05 J_VEHICLE to 5-Port Vehicle Breakout Satellite |
| **JST-PH Pigtail Assortment Set** | 2-Pin, 3-Pin, 4-Pin JST-PH mit vormontierten Litzen | Amazon / COTS | 1 Set | CAN bus, handlebar buttons, mirror LEDs, Qi charger & action cam |
| **J_ACT Actuator Harness** | Vorkonfektioniertes 8-Pin JST-SH Kabel (Top-Entry, gerade Abgangsrichtung) auf 4x 2-Pin Litzenpaare (AWG30 Silikon, 60 mm) | Adafruit / SparkFun | 2 pcs | 4 twisted pairs from PCBA 03 J_ACT (vertical top-entry) to the 4 solenoids (no 180° loop, zero crimping!) |
| **J_AUDIO_PWR Cable Cardo Packtalk** | 8-Pin JST-SH (Top-Entry) auf 3.5mm Spk, Micro-2Pin Mic & 90° USB-C 5V (10 cm) | COTS Standard | 1 pcs | Couples Cardo Air-Mount cradle via vertical top-entry with 5V charge & pristine audio without ground loop |
| **J_AUDIO_PWR Cable Sena SPIDER X** | 8-Pin JST-SH (Top-Entry) auf 3-fach Pigtail (Direct-DC, 2.5mm Mic, 3.5mm Spk, 8 cm) | COTS Standard | 1 pcs | Direct-DC power (3.85V) & stereo audio with Kelvin grounding plugged straight from top (zero pogo-pins) |
| **Automotive Fuse Holder & 2A Fuse** | Wasserdichter Halter + 2A Mini-Flachsicherung | Hella / MTA | 1 pcs | Direct battery terminal protection (KL30) |
| **OMM Helmet Audio & PTT Harness (J_HELMET)** | 6-Pin JST-SH 1.0mm auf 3.5mm Stereo-Klinke + 2-Pin Mic + PTT (0V DC, 12-15 cm) | COTS Standard | 1 pcs | Hum-free headset & mic harness for helmet interior (pure 0V DC signals) |
| **Pure-DC 2-Wire Cable (PUR)** | 2x 0.34 mm² (AWG22) mit JST-JWPF 2-Pin IP67 Stecker | COTS Standard | 2 pcs | 4-wire automotive cable to Pod 1 & 2 (30W USB-PD & USB 2.0 data) |
| **Qwiic Sensor Cable (100 mm)** | 4-Pin JST-SH Buchse zu Buchse (100 mm Silikonlitze) | SparkFun / Adafruit | 1 pcs | Link from 5-port Vehicle Satellite to SAM-M10Q GNSS module |
| **RF Micro-Coax Pigtail (U.FL to SMA IP67)** | 50 mm low-loss RG-178 / 1.13mm mit IP67 EPDM O-Ring & V4A-Mutter | COTS Standard | 2 pcs | Watertight enclosure bulkhead feed-through for OMM UCS antenna |
| **Radar 12V Power Cable (PUR)** | 2x 0.5 mm² (AWG20) mit JST-JWPF 2-Pin IP67 Stecker | COTS Standard | 1 pcs | 12V DC power feed & trigger for rear radar (Branch 4) |
| **Universal Pigtail Adapter Set (JST-JWPF to Open Wire Posi-Tap)** | JST-JWPF 2-Pin & 3-Pin mit verzinnten Aderenden (AWG20) und 4x Posi-Tap Zerstörungsfrei-Klemmen | Posi-Products / COTS | 1 Set | For bikes without pre-assembled plugs: Non-destructive wire tap via Posi-Tap connectors |
| **Central Box USB-C Flashing Pigtail** | IDC 10-Pin auf wasserdichte Panel-Mount USB-C Buchse IP67 | COTS Standard | 1 pcs | CarPlay / firmware flashing port on Central Box flank |

<!-- AUTOGEN_BOM_TABLE_END -->

---

## 13. Minimalist Tooling List (The True IKEA Principle)

Because **no soldering, no crimping, and no thermal heat-staking of threaded inserts** is required, the tool kit shrinks to an absolute minimum that every rider carries in their standard toolkit:

| Tool | Size / Specification | Assembly Purpose |
| :--- | :--- | :--- |
| **Hex Key Set (Allen)** | **1.5 mm / 2.0 mm / 2.5 mm / 3.0 mm** | Tightening all enclosures, circuit boards, and clamps |
| **Phillips / Torx Driver** | **TX10 / PH1** | Enclosure covers and anti-theft security screws |
| **Open-End Wrench / Socket**| **7 mm AF / 8 mm AF** | Counter-holding M4/M5 nuts during clamp assembly |
| **Scissors / Utility Knife**| Standard | Trimming silicone O-ring cord to length |
| **Silicone Grease** | Liqui Moly / OKS 1110 (small tube) | Lightly lubricating enclosure seals |

> [!TIP]
> **No soldering iron, no hot air station, no specialized crimper, and no heat-staking brass insert tool is needed.** All mechanical and electronic modules assemble exclusively with pre-crimped snap connectors and standard fasteners!

---

## 14. Cost Calculation, Ordering Strategy & Economies of Scale (Solo vs. 2-3 Bikes)

> [!IMPORTANT]
> **Important Note Regarding Commercial Intercoms:**
> The estimated hardware cost of **approx. 130 € to 250 €** applies **exclusively to the OpenMotorBridge system** (assembled PCBAs, 3D printed parts, COTS harnesses, 2,200 mAh backup battery, gaskets, standard hardware).
> Any commercial third-party intercoms inserted into the gateway bays (such as **Sena SPIDER X Slim**, **Cardo Packtalk Edge**) or radar devices (**Garmin Varia RTL515 / eRTL615**) are **sourced by the user** and not included in the self-build BOM cost!

### 14.1 Scenario A: Solo Builder (1 Complete System for 1 Motorcycle)
When an individual builder orders all PCBs alone:
* JLCPCB supplies 5 boards per design (2 fully assembled plus 3 unpopulated spares).
* **Cost Breakdown Solo Builder:**
  * JLCPCB PCBAs (PCBA 01, 03 [2x], 05 assembled incl. shipping & customs): approx. 135-160 €
  * 3D Printing (MJF PA12 bureau or own ASA filament): approx. 35-45 €
  * COTS harnesses, 2,200 mAh LiPo, stainless fasteners & gaskets: approx. 35-45 €
  * **Total System Cost Solo: approx. 205 € to 250 €**

### 14.2 Scenario B: Community / Group Order (2 to 3 Motorcycles)
When 2 to 3 riders order together:
* All 5 boards are ordered fully populated from JLCPCB.
* Fixed setup fees distribute across 5 fully operational board sets.
* **Cost Breakdown per Motorcycle (at 3 bikes):**
  * JLCPCB PCBAs (share per bike): approx. 70-80 €
  * 3D Printing (per bike): approx. 30-35 €
  * COTS harnesses, 2,200 mAh LiPo, fasteners (bulk discount): approx. 30 €
  * **Total Cost per Motorcycle: only approx. 130 € to 145 €!**

### 14.3 Smart Procurement Guide & Strategy for Commercial Intercoms (Prime Day Traps, Mechatronics & Helmet Generations)

Builders intending to purchase commercial third-party intercoms for Bay 1 or Bay 2 should observe these market and engineering principles:

1. **Market Dynamics & "Prime Day Traps" with COTS Intercoms:**
   * **Sena Spider Series (Spider ST1 / RT1 / Spider X):** Regularly retails around 190–210 €. During major sales events (such as Amazon Prime Day), retailers frequently inflate list prices artificially to 260–270 €, resulting in higher out-of-pocket costs despite deceptive discount tags.
   * **Cardo Packtalk Edge:** Frequently experiences artificial price increases up to MSRP right before sales promotions, only to be reduced back to its normal street price of ~260 € on the day of the sale.
   * **Recommendation:** Use historical price-tracking tools (Keepa, CamelCamelCamel). The most reliable purchasing window for motorcycle communication hardware is the off-season (November to February) or certified warehouse refurbished units.
2. **The "Helmet Generation Trap" & Planned Obsolescence (Schuberth C4 $\rightarrow$ C5 $\rightarrow$ C6):**
   * **Historical Compatibility Churn:** Riders with a Schuberth C4 and built-in Sena SC1 (Bluetooth-only) were forced to buy an expensive external Sena `+Mesh` adapter (~130 €) to join modern mesh rides. Upgrading to the Schuberth C5 with SC2 (Mesh 2.0 native) immediately rendered that adapter useless. As Sena introduces the 60-series (Mesh 3.0 / Wave), riders face another 400–600 € helmet-specific hardware cycle.
   * **The OpenMotorBridge Solution:** The rider's expensive helmet remains untouched for years, connected strictly via standard Bluetooth to the Central Box. There is zero redundant purchase of proprietary helmet units. When the group's mesh technology advances, only the bike-mounted pod module is swapped or upgraded via open OMM 2.4G / OMM 446.
   * **Upcycling Option for Retired Helmets (€0 Acquisition Cost):** When retiring a helmet after its 5- to 7-year service life or switching brands (e.g., Schuberth C5 with SC2, Shoei Neotec 2/3 with SRL-Mesh/SRL3, or HJC with Smart HJC 50B), the existing system need not be scrapped or sold off cheaply with a degraded battery: Using a universal 3.75V battery-eliminator mod, it can be upcycled directly into Bay 1 as a full Sena Mesh 3.0 bike gateway (see [Chapter 02, Section 3.2](02_intercom_matrix_profiles.md#32-practical-guide-universal-oem-intercom-upcycling-for-helmet-switchers-schuberth-sc2-shoei-srl-series-hjc-smart-50b)).
3. **Mechatronic Advantage: Dedicated Pushbuttons vs. Jog Dials ("Poison for Mechatronics"):**
   * Rotary jog dials (such as on the Sena 50S, 20S, 30K, or new 60S) introduce mechanical rotational backlash, soft stops without tactile feedback, and require complex angular torque actuators. For mechatronic direct digital controls or micro-plungers (handling automated Power ON/OFF), jog dials are poison for mechatronic reliability.
   * **Strict Procurement Recommendation:** For pod bay installation, strictly select units with **dedicated, tactile pushbuttons**:
     * In the Sena ecosystem: **Sena 60X** (modular/integrated buttons, avoiding the 60S dial), **Sena Spider RT1**, or **Sena Spider X Slim** (crisp snap domes, flat profile).
     * In the Cardo ecosystem: **Cardo Packtalk Edge / Neo** (pronounced 3-button ergonomics with linear orthogonal actuation).

---

## 15. Component Lifecycle & SMT Sourcing Audit (EOL / NRND Alternatives)

### 15.1 Critical Finding: MEMS Microphone (Knowles SPH0645LM4H-B is EOL)
* **Status:** The originally specified Knowles **SPH0645LM4H-B** is formally declared **Obsolete / End-of-Life**.
* **Recommended Successor / Primary Part:** **Sipeed / Zilltek MSM261S4030H0R** (LCSC Part: **`C544577`**).
  * *Advantages:* 100% standard I2S compliant (no DMA bit-shift workarounds required in ESP-IDF), excellent large-scale stock availability at LCSC, pin and footprint compatible.

### 15.2 JLCPCB Extended-Parts & Second-Source Alternatives

| Subassembly / Function | Primary Component | JLCPCB / LCSC Part | Status / Sourcing | Recommended Second-Source / Drop-In Alternative |
| :--- | :--- | :--- | :--- | :--- |
| **Central Box 12V Buck** | TI LM5164-Q1 | `C2843477` | Active (TI), JLCPCB Extended | **TI LMR36015** (60V 1.5A, `C2843480`) or **XLSEMI XL7005A** (80V) |
| **Front Node USB Hub** | Microchip USB2514Bi | `C16251` | Active, Industrial (-40..+85°C) | **Terminus FE1.1s / FE8.1** (JLCPCB Basic Part, cents-level price) |
| **CAN-FD Transceiver (3.3V)** | TI TCAN334GDCNR | `C842340` | Active (TI) | **TI TCAN332G / TCAN337G** or **SITCORE SIT1051T/3** |
| **Audio Transformer (1500V)**| Bourns LM-NP-1001-B1L| `C114402` | Active, JLCPCB Extended | **Triad Magnetics SP-66** or **Bourns SM-LP-5001** |
| **Stereo DSP Codec** | Everest Semi ES8388 | `C365736` | Active (Standard in ESP-ADF) | **Everest Semi ES8311** or **TI TLV320AIC3104** |

---

## 16. Conformal Coating Manufacturing Guidelines (IPC-CC-830B)

To ensure 100% automotive-grade reliability against vibration, condensation, and road salt, all 7 PCBAs are conformal coated during the assembly process:

### 16.1 Coating Specification
* **Standard:** Certified to **IPC-CC-830B** and **MIL-I-46058C**.
* **Type:** **Modified Acrylic Resin (AR)**, e.g., *Peters ELPEGUARD SL 1307 FLZ* (fast curing, UV fluorescent for optical inspection).
* **Layer Thickness:** $30\,\mu\text{m} \dots 60\,\mu\text{m}$ evenly across top and bottom layers.

### 16.2 Mandatory Masking Zones (Kapton Tape Protection)
The following areas must **never** be coated:
1. **Connectors & Sockets:**
   * USB-C receptacles (`J7` Front Node, service ports)
   * M8 / M5 connector pins (`J2` Pod Base, Binder M5 Radar)
   * JST-SH / JST-PH pin headers (`J_COCKPIT`, `J_VEHICLE`, `J7` Front Node, `J1..J2` Pods)
   * MicroSD card slot (`J2` Central Box)
2. **Acoustic Sensors & Venting:**
   * **MEMS Microphone (`MIC1` MSM261S4030H0R on PCBA 05):** Acoustic inlet port ($\varnothing 0.5\,\text{mm}$) must be sealed with a Kapton dot!
   * **Equalization Vent (Gore ePTFE Vent):** Must remain free of lacquer.
3. **RF Antenna Connectors & Test Points:**
   * U.FL coaxial sockets (`ANT1`, `ANT2`)
   * Test points for in-circuit programming and oscilloscope probing
