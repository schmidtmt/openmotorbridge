# 15 - Bill of Materials (BOM), COTS Sourcing & SMT Manufacturing (All 7 PCBAs)

This document serves as the master reference (Single Source of Truth) for the complete Bill of Materials (BOM), manufacturing specifications for all 7 printed circuit board assemblies (PCBA 01 to PCBA 03, PCBA 05 to PCBA 08 - PCBA 04 is retired without replacement in v8.0) at JLCPCB / Eurocircuits, all mechanical 3D printed components, COTS procurement lists, and a comprehensive cost and ordering strategy (Solo builder vs. Community group buy).

---

## 1. PCBA 01: Central Box Main Controller (`openmotorbridge_central_box`, 4-Layer FR4 TG150)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | ESP32-S3-WROOM-1-N16R8 | Espressif Systems | SMD Module | C2913200 | Host MCU (Dual-Core, 16 MB Flash, 8 MB PSRAM) |
| **U2** | LM5164-Q1 | Texas Instruments | SOIC-8-EP | C2843477 | Automotive 65V Synchronous Buck Converter |
| **U3** | BQ24075RGTR | Texas Instruments | VQFN-16 | C15464 | Dynamic Power-Path Controller & LiPo Charger with TS |
| **U4** | BMI270 | Bosch Sensortec | LGA-14 | C2836813 | 6-Axis IMU for Lean Angle & Dynamics |
| **U5** | ES8388 | Everest Semi | QFN-28 | C365736 | 24-Bit Stereo Audio Codec (I2S ADC/DAC) |
| **U6** | TCAN334GDCNR | Texas Instruments | SOT-23-8 | C842340 | 3.3V Automotive CAN-FD Transceiver (±58V Fault) |
| **U7** | SX1262IMLTRT | Semtech | QFN-24 | C190184 | Onboard 868 MHz LoRa Transceiver (+22 dBm, 24/7 UPS buffered) |
| **U8** | DW3110 | Qorvo | QFN-16 (B.Cu) | C2934600 | IEEE 802.15.4z UWB Transceiver (6.5 GHz Ch. 5 Backbone) |
| **SW1** | TS-1187A-C-A-B | C&K / Omron | SMD Push-Button | C318884 | Hardware Pairing & Reset Button (3s Pair, 10s Purge) |
| **D1** | SMBJ33CA | Littelfuse | DO-214AA (SMB) | C87848 | TVS Diode (33 V Standoff, 53.3 V max Clamping) |
| **F1** | MF-MSMF050-2 | Bourns | 1812 SMD | C22668 | Resettable PPTC Fuse (500 mA Hold / 1.0 A Trip) |
| **LED1** | WS2812B-B | Worldsemi | 5050 SMD | C114586 | RGB Status LED for Visual Mode Diagnostics |
| **J1** | DTM13-12PA Header | TE Connectivity | Automotive 12P | Custom Part | Automotive Deutsch DTM-12 Interface (11 active pins) |
| **J2** | MicroSD Slot Push-Push | Molex / Korean Hro | SMD Push-Push | C266624 | 4-Bit SDIO Flash Card for Tour Logging |
| **J_BAT** | Molex Micro-Fit 3.0 2P | Molex | SMD Header | C289110 | Header for 2,200 mAh LiPo Backup Battery |
| **ANT1** | U.FL-R-SMT-1 | Hirose / Murata | SMD RF | C2834595 | LoRa 868 MHz U.FL socket to Taoglas FXP895 in lid |
| **ANT2** | U.FL-R-SMT-1 | Hirose / Murata | SMD RF (B.Cu) | C2834595 | UWB 6.5 GHz U.FL socket to Taoglas FXUWB10 in tub floor |

*(Note: Migration to All-UWB completely eliminates previous audio transformers T1, T2 and optocouplers OC1, OC2).*

---

## 2. Satellite Pod Enclosure (Elimination of PCBA 02)
> **Architecture Note (v8.5 / v9.0 Clean Architecture):**  
> The previous pod base carrier PCB `PCBA 02` has been **completely eliminated without replacement**.  
> The pod enclosure (`pod_base_housing.stl`) is a seamless, monolithic 1-piece 3D printed monocoque with zero internal active electronics. The 2-wire DC harness (+12V/5V and GND) feeds directly through the rear gland/M8 port and terminates at two gold-plated Mill-Max heavy-duty spring contact sleeves, mating directly with the rear gold pads `PAD1` and `PAD2` on `B.Cu` of `PCBA 03`.

---

## 3. PCBA 03: Universal Smart Cartridge Rev 3.0 (`openmotorbridge_pod_cartridge`, 2-Layer FR4 TG150, 2-Sided SMT)
> **Quantity Note:** Fitted **2x per motorcycle** (Slot 1 for Sena SPIDER X Slim, Slot 2 for Cardo Packtalk Edge or optional OMM 2.4 GHz Swap Cartridge).

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | DW3110 | Qorvo | QFN-16 (B.Cu) | C2934600 | IEEE 802.15.4z UWB Transceiver (6.5 GHz Ch. 5 All-UWB Link) |
| **U2** | ES8388 / MCU | Everest / WCH | QFN-28 (F.Cu) | C2943200 | Low-Power Stereo Audio Codec & Host Controller |
| **Q1 - Q4** | AO3400A | Alpha & Omega | SOT-23 (B.Cu) | C20917 | 4x N-Channel Power MOSFETs ($30\,\text{V} / 5.7\,\text{A}$) for Solenoid Actuators |
| **D1 - D4** | 1N4148WS | Diodes Inc. | SOD-323 (B.Cu)| C2128 | 4x Flyback Suppression Diodes for Solenoid Coils |
| **F1** | MF-MSMF050-2 | Bourns | 1812 SMD | C22668 | Resettable PPTC Fuse for 5V Cartridge Rail |
| **J_ACT** | SM08B-SRSS-TB | JST | 8-Pin 1.0mm SMD | C160404 | Mechatronics Header for 4 Miniature Solenoids |
| **J_AUDIO_PWR**| SM08B-SRSS-TB | JST | 8-Pin 1.0mm SMD | C160404 | Audio & Power Header (Top, Isolated PGND / AGND Kelvin Grounds) |
| **ANT_UWB** | U.FL-R-SMT-1 | Hirose / Murata | SMD RF (B.Cu) | C2834595 | UWB Antenna Port to Taoglas FXUWB10 in Sled Floor Pocket |
| **PAD1, PAD2**| Mill-Max Contact Pads | Mill-Max / PCB | Gold Pad (B.Cu)| ENIG Surface | Rear DC Power Contact Pads (+12V/5V and GND) |

---

## 4. Assembly PCBA 04 (Rear Pod 3): Retired Without Replacement (Clean Architecture v8.0)

> [!NOTE]
> **Architecture Streamlining v8.0:** Circuit board `PCBA 04` and the 3rd satellite enclosure (Rear Pod 3) have been **completely eliminated without replacement**:
> 1. **LoRa 868 MHz (SX1262):** Sits directly on the Central Box (`PCBA 01`), backed up 24/7 by the UPS battery for continuous anti-theft sentry.
> 2. **Multi-GNSS (SAM-M10Q):** Sits in the cool ram-air intake zone on Front Node (`PCBA 05`), interfaced via Qwiic I2C (`J12`).
> 3. **Vehicle Wireless Backbone:** Transmitted via Ultra-Wideband (Qorvo DW3110 / 6.5 GHz Ch. 5, $< 0.4\,\text{ms}$ latency) between Front Node and Central Box.
> 4. **Rear Radar:** Connects directly to the Central Box via Whip 5 of the Deutsch DTM-12 automotive harness.

---

## 5. PCBA 05: Universal Front Node (`openmotorbridge_front_node`, 4-Layer FR4 TG150, 82 x 50 mm)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | ESP32-S3-WROOM-1U-N8R8 | Espressif Systems | SMD Module | `C2913200` | Dual-Core 32-Bit Xtensa LX7 (240 MHz, Vector-DSP, 8MB PSRAM, ext. U.FL) |
| **U2** | USB2514Bi-AEZG / USB2514B | Microchip | QFN-36 | `C16251` | Automotive/Industrial USB 2.0 High-Speed 480 Mbps 4-Port Hub Controller |
| **U3** | LMR36015FSCQRNXRQ1 | Texas Instruments | VQFN-12 | `C2843480` | Automotive 36V Synchronous Buck (5V / 2.0A, 91.8%) for Hub & Peripherals |
| **U4** | TPS2051BDBVR | Texas Instruments | SOT-23-5 | `C7818` | High-Side USB VBUS Power Switch (1.05A Clamp) for Port 2 Cold-Reboot Reset |
| **U5** | SC8102QDER | Southchip | QFN-32 | `C2843510` | Automotive Synchronous Buck with USB-PD 20W (9V/2.2A & QC3.0) for Smartphone Port 1 |
| **U6** | TCAN334GDCNT | Texas Instruments | SOT-23-8 | `C2843515` | 3.3V CAN Transceiver (5 Mbps CAN-FD capable, with Pin 8 Silent-Listen-Only Mode) |
| **U7** | DW3110 | Qorvo | QFN-16 (B.Cu) | `C2934600` | IEEE 802.15.4z UWB Transceiver (6.5 GHz Ch. 5 Backbone) |
| **K1** | CPC1017NTR | IXYS / Littelfuse | SOP-4 | `C26789` | 60V / 100mA 1-Form-A Solid-State Relay for switchable 120R CAN Termination (Auto-Sensing) |
| **Q1** | DMN63D8LDW-7 | Diodes Incorporated| SOT-363 | `C283890` | Dual N-Channel MOSFET (30V / 260mA) for directional mirror blind-spot LEDs (J9) |
| **Q2** | TPS1H100BQPWPRQ1 | Texas Instruments | HTSSOP-14 | `C2843520` | Automotive Smart High-Side Power Switch (up to 3.5A / 40W) for 12V Aux Light (J11) |
| **LED1**| WS2812B-2020 | Worldsemi | SMD 2020 | `C2843530` | Digitally controllable RGB status LED for enclosure lid light pipe |
| **MIC1**| MSM261S4030H0R / SPH0645 | Sipeed / Knowles | 3.5x2.65 mm SMD | `C544577` | Digital I2S MEMS Acoustic Microphone (Standard I2S, high availability) |
| **L1** | 4.7 µH Automotive Inductor | Sunlord / Wurth | SMD 5x5 mm | `C2843490` | Storage Inductor for LMR36015 5V Main Regulator |
| **L2** | 10 µH Automotive Inductor | Coilcraft / Wurth | SMD 7x7 mm | `C2843525` | Storage Inductor for SC8102 USB-PD Fast-Charge Buck (Port 1) |
| **J1** | JST-PH 2-Pin Header | JST | 2.00mm SMD | `C289115` | 12V Vehicle Power Input (KL15 & GND) |
| **J2** | JST-PH 3-Pin Header | JST | 2.00mm SMD | `C289116` | Cockpit CAN-Bus (CAN_H, CAN_L, GND with Auto-Sensing Relay) |
| **J3** | JST-PH 4-Pin Header | JST | 2.00mm SMD | `C289117` | Handlebar Multi-Button Interface (PTT, Cam-Action, Media-Voice, GND) |
| **J4** | JST-PH 4-Pin Header | JST | 2.00mm SMD | `C289117` | Upstream USB Port to Motorcycle Infotainment (Skyline OS / Boom! Box) |
| **J5** | JST-PH 4-Pin Header | JST | 2.00mm SMD | `C289117` | Port 1: Handlebar Smartphone (USB-PD 20W + High-Speed Data) |
| **J6** | JST-PH 4-Pin Header | JST | 2.00mm SMD | `C289117` | Port 2: Fairing Pigtail (shielded, 30 cm) to CP2AA CarPlay/AA Dongle |
| **J5_MP3**| JST-PH 4-Pin Header | JST | 2.00mm SMD | `C289117` | Port 3: Glovebox Cable for USB Drives (MP3s & Firmware Updates) |
| **J6_AUX**| JST-PH 4-Pin Header | JST | 2.00mm SMD | `C289117` | Port 4: Cockpit Accessories / Dashcam Storage / Zūmo Navi |
| **J7** | USB-C 16-Pin Receptacle IP67| GCT / Korean Hro | SMD Hybrid | `C2765186` | ESP32-S3 Service & Flash Port (Flank) with TPU Sealing Plug |
| **J8** | JST-PH 2-Pin Header | JST | 2.00mm SMD | `C289115` | Action-Cam 5V Charge-Only Power Port (up to 2.0A) |
| **J9** | JST-PH 3-Pin Header | JST | 2.00mm SMD | `C289116` | Mirror Blind-Spot Warning LEDs (12V_PROT, BSD_LEFT_N, BSD_RIGHT_N) |
| **J10** | JST-PH 2-Pin Header | JST | 2.00mm SMD | `C289115` | 12V Qi Wireless Charger Power (SP Connect / QuadLock Head) |
| **J11** | JST-PH 2-Pin Header | JST | 2.00mm SMD | `C289115` | 12V Aux Light (Adventure Driving Lights / Brake Flash Strobe) |
| **J12** | JST-SH 4-Pin Header | JST | 1.00mm SMD | `C289118` | Qwiic / STEMMA QT I2C Sensor Port (SAM-M10Q GNSS, TMP117, OPT3001) |
| **ANT1**| U.FL-R-SMT-1 | Hirose / Murata | SMD RF (B.Cu) | `C2834595` | UWB 6.5 GHz U.FL socket to Taoglas FXUWB10 in tub floor |

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

---

## 8. PCBA 08: Radar 2.0 Sub-MCU & 36-LED Wing Carrier (`openmotorbridge_radar_submcu`, 2-Layer FR4 TG150, 115 x 65 mm)

| Ref | Component / Type | Package | Specification & Function | LCSC Part |
| :--- | :--- | :--- | :--- | :--- |
| **`U1`** | ESP32-C5-WROOM-1-N8 | SMD Module | 32-Bit RISC-V Sub-MCU & 5.9 GHz V2X Uplink (2.4 GHz strictly disabled at rear) | `C2843550` |
| **`U2`** | LDO 3.3V 500mA | SOT-23-5 | TI TPS7A0533 / Richtek RT9013 LDO Voltage Regulator | `C505293` |
| **`U3`** | DW3110 | QFN-24 (4x4mm) | Qorvo Ultra-Wideband Transceiver (6.5 GHz Ch. 5/9, All-UWB backbone) | `C2834570` |
| **`D1..36`**| WS2812B-2020 | SMD 2020 | 36x Digital RGB LEDs in Dual Warning Wings (18 left, 18 right, autonomous strobe) | `C2843530` |
| **`J1`** | JST-JWPF 2-Pin | Automotive IP67 | 12V Power Supply Input (`RADAR_PWR_12V` / `RADAR_GND`) | `C2834590` |
| **`J2`** | JST-SH 1.0mm 4-Pin | SMD Right-Angle| UART Interface to Wheeltec MR20 mmWave Radar (AoP patch array on front) | `C136657` |
| **`J3`** | 4-Pin 2.54mm Header| 90° Right-Angle | Flashing & Debug Header (`3V3`, `TX`, `RX`, `GND`) at housing edge | `C12437` |
| **`J4`** | Hirose U.FL | SMT Vertical | 6.5 GHz UWB Antenna Port to Taoglas FXUWB10 Flex Antenna | `C14894` |
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
| **`J1`** | TYPE-C-31-M-12 | SMT/THT IP67 | Waterproof 16-Pin USB-C Receptacle (5V charging on the go via powerbank/bike, WebUSB DFU, cartridge dock) | `C2765186` |
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
| **`J1`** | TYPE-C-31-M-12 | SMT/THT IP67 | Waterproof 16-Pin USB-C Receptacle (5V DC power, charging on the go, WebUSB DFU, cartridge dock) | `C2765186` |
| **`J_HELMET`**| SM06B-SRSS-TB | 6-Pin JST-SH 1.0mm Horiz.| Internal Helmet Audio & PTT port on B.Cu (HP_OUT_L, HP_OUT_R, AGND_SPK, MIC_IN+, AGND_MIC, BTN_PTT; 0V DC) | `C136657` |
| **`J_RF`** | U.FL-R-SMT-1 | SMD U.FL Socket (B.Cu)| 50 Ohm U.FL RF connector for coax pigtail to waterproof SMA bulkhead or bike antenna | `C14899` |
| **`PAD_ANT`**| SMD Testpad D3.0mm| Copper Pad (F.Cu) | Alternate RF solder connection for internal helical antenna | - |
| **`BAT1`** | BM02B-SRSS-TB | SMD 1.0mm pitch | Connection to internal 600-mAh LiPo pouch cell (with PCM) | `C2902341` |
| **`D1`** | WS2812B-2020 | SMD 2020 | RGB Status LED (RX Green, TX Red, DMR Blue, Charging Yellow) | `C2843785` |
| **`D2`** | USBLC6-2SC6 | SOT-23-6 | High-speed TVS diode array for USB D+/D- and VBUS ESD protection | `C7519` |
| **`SW1..4`** | EVQ-P2 / KMT0 | SMD 3.5x2.8mm | 4x Tactile IP67 micro-switches (PTT, Mode, Ch+, Ch-) | `C318884` |

---

## 9. 1-Click Ordering Guide for JLCPCB (All PCBAs Fully Assembled)

All manufacturing packages reside in the repository under `hardware/production_packages/` as complete ZIP and CSV archives:

| Subassembly / PCBA | Gerber ZIP Archive | BOM CSV File | CPL (Pick & Place) CSV | Layers | Manufacturing Notes |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **PCBA 01: Central Box** | `01_main_box_pcba_gerbers_jlcpcb.zip` | `01_main_box_pcba_bom_jlcpcb.csv` | `01_main_box_pcba_cpl_jlcpcb.csv` | **4 Layers** | ENIG (Gold), 1.6 mm, TG150, 2-sided SMT (DW3110 on B.Cu) |
| **PCBA 03: Cartridge Carrier**| `03_pod_cartridge_pcba_gerbers_jlcpcb.zip` | `03_pod_cartridge_pcba_bom_jlcpcb.csv` | `03_pod_cartridge_pcba_cpl_jlcpcb.csv` | **2 Layers** | ENIG (Gold), 1.2 mm, 2-sided SMT (Order 2x per vehicle) |
| **PCBA 05: Front Node** | `05_front_node_pcba_gerbers_jlcpcb.zip` | `05_front_node_pcba_bom_jlcpcb.csv` | `05_front_node_pcba_cpl_jlcpcb.csv` | **4 Layers** | ENIG (Gold), 1.6 mm, TG150, 2-sided SMT (DW3110 on B.Cu) |
| **PCBA 06: MagSafe Dock** | `06_magsafe_dock_pcba_gerbers_jlcpcb.zip` | `06_magsafe_dock_pcba_bom_jlcpcb.csv` | `06_magsafe_dock_pcba_cpl_jlcpcb.csv` | **2 Layers** | *Optional / Legacy* (replaced by COTS 2-Pin magnetic connector) |
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
| **Main Box Lower Case** | [`main_box_lower_case.stl`](../../hardware/cad/stl/01_main_box/main_box_lower_case.stl) | **1** | MJF PA12 / ASA | Monocoque tub with UWB bottom pocket ($11 \times 11 \times 0.6\,\text{mm}$), 4x M4 silentblock ears & sealing groove |
| **Main Box Mid Tray** | [`main_box_mid_tray.stl`](../../hardware/cad/stl/01_main_box/main_box_mid_tray.stl) | **1** | MJF PA12 / ASA | Battery tray for 2,200 mAh flat LiPo ($68 \times 39 \times 5.0\,\text{mm}$), 11x convection vents & tongue-and-groove rib |
| **Main Box Lid** | [`main_box_lid.stl`](../../hardware/cad/stl/01_main_box/main_box_lid.stl) | **1** | MJF PA12 / ASA | Lid with LoRa FXP895 antenna pocket ($110 \times 20 \times 0.8\,\text{mm}$), Gore ePTFE vent seat & countersinks |
| **Pod Base Housing** | [`pod_base_housing.stl`](../../hardware/cad/stl/02_pod_base/pod_base_housing.stl) | **2** | MJF PA12 / ASA | Monolithic 1-piece tunnel enclosure with integral bulkhead, contact guides & spring posts |
| **Pod Bulkhead (Integrated)**| [`03_pod_bulkhead_partition.stl`](../../hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl) | *(integr.)* | MJF PA12 / ASA | 100% integrally molded into the monocoque housing (0 loose parts, 0 assembly screws) |
| **Cartridge Base Sled**| [`cartridge_base_sled.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl) | **2** | MJF PA12 / ASA | Universal sled for Gateway 1 (Pod 1) and Gateway 2 (Pod 2) |
| **Cartridge Latch Lever**| [`cartridge_magnetic_lock_latch.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_magnetic_lock_latch.stl) | **2** | MJF PA12 / ASA | Magnetic anti-theft locking latch levers for Cartridge Slots 1 & 2 |
| **Front Node Lower Tub** | [`front_node_lower_tub.stl`](../../hardware/cad/stl/04_front_node/front_node_lower_tub.stl) | **1** | MJF PA12 / ASA | Cockpit tub with UWB bottom pocket ($11 \times 11 \times 0.6\,\text{mm}$), AMPS pattern & handlebar tube cradle |
| **Front Node Upper Lid** | [`front_node_upper_lid.stl`](../../hardware/cad/stl/04_front_node/front_node_upper_lid.stl) | **1** | MJF PA12 / ASA | Lid with Knowles MEMS acoustic inlet port & O-ring sealing channel |
| **Front Node Cable Glands**| [`front_node_cable_glands_tpu.stl`](../../hardware/cad/stl/04_front_node/front_node_cable_glands_tpu.stl) | **1 Pair**| TPU 95A / 85A | Flexible split sealing comb for front USB and signal wiring |
| **Front Node USB-C Cap** | [`front_node_usbc_cap_tpu.stl`](../../hardware/cad/stl/04_front_node/front_node_usbc_cap_tpu.stl) | **1** | TPU 95A / 85A | Elastic dust cap with retention tether for service port |

### 10.2 Gateway Cartridge Inlays (Intercom Selection)
> **Architecture Note:** Slot 1 and Slot 2 are **Multi-Protocol Gateway Transceivers**, not rider/passenger headsets! They link the motorcycle simultaneously to Sena Mesh and Cardo DMC. Rider and pillion communicate wirelessly with their standard helmet headsets.

| Subassembly | STL File Path | Qty | Material | Function & Description |
| :--- | :--- | :---: | :--- | :--- |
| **Gateway Inlay Sena** | [`cartridge_insert_sena.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) | *Opt. (1)* | MJF PA12 / ASA | Form-fitting inlay for Sena SPIDER X Slim (Mesh 3.0 / 2.0, direct micro-cable whip) |
| **Gateway Inlay Cardo** | [`cartridge_insert_cardo.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl) | *Opt. (1)* | MJF PA12 / ASA | Inlay for Cardo Packtalk Edge / Pro (DMC Gen2) with Air-Mount cradle |
| **Swap Inlay OMM 2.4 GHz** | [`cartridge_insert_omm.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_omm.stl) | *Opt. (1)* | MJF PA12 / ASA | Inlay for OMM 2.4 GHz Swap Cartridge (ESP32-C3) |
| **Blank Cartridge / Dry Box** | [`cartridge_insert_blindkassette.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_blindkassette.stl) | *Opt. (1)* | MJF PA12 / ASA | Hermetic protective dummy sled for unused slots or watertight dry box |

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
* **Kit 3: Harley-Davidson Touring & Classic Bagger (Street Glide, Road Glide, Road King):**
  * `saddlebag_lid_dock.stl` (2 pcs): Hard saddlebag lid mounting docks for Pod 1 & 2 with hinge Torx flange, 4x strap hook clearance pockets & 2-wire DC strain relief snout.
  * `010_saddlebag_hole_grommet_split.stl` (2 pcs): Split EPDM/TPU grommet for Ø 3.6 mm 2-wire DC cable in Ø 12 mm forward wall bore (above swingarm pivot).
  * `radar_license_plate_bracket.stl` (1 pc): Vibration-isolated license plate radar bracket for Whip 5.
  * `radar_swivel_tilt_cradle.stl` (1 pc): Radar 2.0 heavy-duty center-of-gravity swivel tilt cradle with 2x M4 bolts and 36-tooth radial Hirth rosette.
  * `radar_mr20_housing.stl` & `radar_mr20_radome.stl` (1 pc): Radar 2.0 PA12 wing housing with tire roost deflector and PC radome.
  * `magsafe_cockpit_mount_harley.stl` (1 pc), `magsafe_frame_dock.stl` (1 pc) & `magsafe_clamp_wings.stl` (1 pc): MagSafe frame dock components.
* **Optional Bobber & Custom Bike Parts:**
  * `radar_center_underfender_mount.stl` (1 pc): Stealth Center Under-Fender Mount with 46 mm drop and integrated 42 mm tire roost deflector shield.
  * `radar_swivel_tilt_cradle.stl` (1 pc): Heavy-duty swivel tilt cradle with 2x M4 screws.
* **Kit 4: Support Car / Van Convoy Kit (Car-Kit):**
  * `car_sun_visor_pod_clip.stl` (2 pcs): Quick-release spring clips for secure, vibration-free mounting of Pod 1 and Pod 2 to the sun visors in chase car or van (driver and passenger side).
  * `car_dashboard_wedge_dock.stl` (1 pc): Dual-stack dashboard dock for Front Node (bottom, clear sky GNSS view) and Central Box (top, 15° tilted).

---

## 11. Pre-Assembled COTS Harnesses & RF Antennas (Zero Crimping, Zero Soldering!)

No custom wire harnessing or crimping is required. The system leverages 100% commercially available, industrially molded standard cables (COTS):

### 11.1 Main Motorcycle Wiring Harness (Deutsch DTM-12 COTS Finished Harness)

```
                       PLUG-AND-PLAY HARNESS CONCEPT (COTS PRE-MOLDED)
+-------------------------+
| Deutsch DTM-12 IP68     | --> Pre-terminated DTM-12 breakout harness whip (TE Connectivity COTS)
| (Central Box Interface) | --> 100% watertight automotive seal, Raychem DR-25 heatshrink jacket
+-+-----------------------+
  +-> Whip 1: 2-Wire FLRY-B (1.0 m / 1.5 m): Pure DC Power (+12V switched / GND) --> Pod 1 (Bay 1)
  +-> Whip 2: 2-Wire FLRY-B (1.0 m / 1.5 m): Pure DC Power (+12V switched / GND) --> Pod 2 (Bay 2)
  +-> Whip 3: 2-Wire FLRY-B (0.5 m): Rear Radar PCBA 08 (+12V switched / GND via JST-JWPF)
  +-> Whip 4: AMP Superseal 1.5 6-Pin / FLRY-B (1.0 m): Vehicle Rail & CAN (KL30, KL15, GND, CAN-H, CAN-L, CHASSIS_EARTH)
      (Note: All interconnects, audio channels, and telemetry streams communicate 100% wirelessly over UWB!)
```

### 11.2 The 12V Workshop & Chase Vehicle Y-Adapter Harness ("Bench & Support-Car Harness")

For bench testing without a bike harness, or mobile operation in chase vans, the universal 12V Y-adapter harness powers both Front Node and Central Box in parallel from any 12V DC auxiliary cigarette outlet or bench power supply. The USB-C ports remain completely free for CarPlay wired bridge testing or WebSerial firmware development.

### 11.3 RF Antennas & Sensors (COTS)
1. **UWB 6.5 GHz Flex Antennas (2 pcs):** **Taoglas FXUWB10** ($11 \times 11 \times 0.6\,\text{mm}$) with 20 mm U.FL coaxial lead for Central Box and Front Node lower tub floor recesses.
2. **LoRa 868 MHz Flex Antenna (1 pc):** **Taoglas FXP895** ($110 \times 20 \times 0.8\,\text{mm}$) with 50 $\Omega$ U.FL feed for Central Box lid pocket.
3. **Multi-GNSS Module (1 pc):** **u-blox SAM-M10Q** with integrated $15 \times 15\,\text{mm}$ ceramic patch antenna, Qwiic I2C (`J12`) on Front Node inside ram-air duct.
4. **Environmental Sensors (Front Node J12 Daisy-Chain):**
   * **TI TMP117:** High-precision temperature sensor ($\pm 0.1\,^\circ\text{C}$) for black ice early warning.
   * **TI OPT3001:** Ambient light sensor for display and driving light control.

### 11.4 Internal COTS Cable Set & Pigtails for Front Node & Periphery

All internal housing connections utilize pre-crimped COTS pigtails:
* **J5 / J5_MP3:** JST-PH 5-Pin to Panel-Mount USB-C (IP67) for cockpit fast charging (20W PD).
* **J6:** JST-PH 4-Pin to USB-A receptacle for CP2AA wireless dongles (Ottocast / Carlinkit).
* **J1..J3:** JST-PH 2P/3P/4P pigtails for Cockpit 12V, CAN-Bus, and handlebar PTT switches.
* **J9..J11:** JST-PH pigtails for Mirror BSD warning LEDs, Qi pad 12V, and aux lighting relay.
* **J12:** JST-SH 4-Pin SparkFun Qwiic / STEMMA QT cable to SAM-M10Q and TMP117.

### 11.5 Gateway Adapter Cables for OEM Intercoms (Header `J_AUDIO_PWR` / 8-Pin JST-SH)

To operate commercial OEM intercom modules completely non-destructively and without voiding factory warranties, the 8-pin **JST-SH 1.0 mm Header `J_AUDIO_PWR`** on `PCBA 03` connects to model-specific COTS adapter cable harnesses. Complete physical separation of high-current power return (`PGND`) and audio references (`AGND_SPK`, `AGND_MIC`) eliminates all ground-loop charging and Mesh TDMA buzzing:

| Headset Model / Class | Adapter Cable Type & Connectors | 8-Pin JST-SH Header Pinout | Length | Function & Key Features |
| :--- | :--- | :--- | :---: | :--- |
| **Sena SPIDER X Slim**<br>*(OMB Reference K2a)* | **8-Pin JST-SH to 3-Way Pigtail:**<br>- 2-Pin Micro-JST (Direct-DC)<br>- 2.5 mm Jack (Mic In)<br>- 3.5 mm Stereo Jack (Spk Out) | **Pin 1:** `PGND` (Power Return)<br>**Pin 2:** `VCC_HEADSET` ($3.85\,\text{V}$ regulated DC)<br>**Pin 3:** `AGND_SPK` (Audio Ground Sleeve)<br>**Pin 4:** `AUDIO_L_IN` (Spk L)<br>**Pin 5:** `AUDIO_R_IN` (Spk R)<br>**Pin 6:** `AGND_MIC` (Mic Ground Return)<br>**Pin 7:** `MIC_OUT`<br>**Pin 8:** `RESERVE_IO` (N/C) | 8 cm | **Zero Pogo-Pins & Zero Hum:** Direct 3.85V battery-free supply. High DC return current flows solely across Pin 1 (`PGND`). Audio lines stay 100% hum-free over zero-current pins 3 and 6! |
| **Cardo Packtalk Edge / Pro**<br>*(Class 1d DMC Gen2)* | **8-Pin JST-SH to 3.5mm, Micro-2Pin & USB-C:**<br>- 3.5 mm Stereo Jack (Spk Out L/R)<br>- Cardo 2-Pin Micro Plug (Mic In)<br>- Right-Angle USB-C (5V Charge Port) | **Pin 1:** `PGND` (Charge Return)<br>**Pin 2:** `VCC_5V` (Charge & Run Power)<br>**Pin 3:** `AGND_SPK` (Audio Ground Sleeve)<br>**Pin 4:** `AUDIO_L_IN` (Spk L)<br>**Pin 5:** `AUDIO_R_IN` (Spk R)<br>**Pin 6:** `AGND_MIC` (Mic Ground Return)<br>**Pin 7:** `MIC_OUT` (Voice Signal)<br>**Pin 8:** `RESERVE_IO` (N/C) | 10 cm | Connects factory Air-Mount cradle. 500mA charging current returns across Pin 1; audio grounds remain pristine -- zero charging whine in helmet! |
| **OpenMotorMesh (OMM) 2.4 GHz / 446**<br>*(Class 4 / 3b Native UCS)* | **8-Pin JST-SH to USB-C (90° Angled) & opt. 5V Branch:**<br>- 8-Pin JST-SH 1.0mm Socket<br>- Right-Angle USB-C Plug<br>- Opt. 2-Pin Micro Pigtail (5V / PGND) | **Pin 1:** `PGND` (Power Return)<br>**Pin 2:** `VCC_5V` (Module + Booster Supply)<br>**Pin 3:** `AGND_SPK`<br>**Pin 4:** `AUDIO_L_IN` (Stereo L)<br>**Pin 5:** `AUDIO_R_IN` (Stereo R)<br>**Pin 6:** `AGND_MIC`<br>**Pin 7:** `MIC_OUT`<br>**Pin 8:** `PTT_IO` / Config | 5 cm | Connects PCBA 03 directly to the IP67 USB-C port of the OMM module. Zero-wear digital/analog interface. When fitted with optional RF booster, the 2-pin branch powers the amplifier via Pins 1 & 2 without violating Kelvin ground isolation! |

### 11.6 Mechatronic Actuator Harness & Mechanical Retention (Header `J_ACT`)

Each Universal Smart Cartridge (`PCBA 03`) drives up to four linear solenoids ("mechanical fingers") to actuate OEM headset buttons:
1. **Pre-crimped 8-Pin Splitter Harness:** 8 AWG30 silicone wires (60 mm) split into 4 twisted pairs connected to MOSFET outputs `ACT1_OUT` through `ACT4_OUT`.
2. **Miniature Solenoids:** 4x 5V DC miniature pull solenoids ($\varnothing 6.5 \times 12\,\text{mm}$) with soft damping TPU tips (`actuator_silicone_tip.stl`).
3. **Rigid Retainer Plate:** Retained by PA12 plate (`cartridge_retainer_plate.stl`) and 4x M2 x 6 mm countersunk screws (DIN 7991).

---

## 12. COTS Hardware & Fastener Procurement List (1 Complete Kit)

### 11.7 Pannier Disconnect (Industrial 2-Pin Magnetic Pogo "MagSafe Replacement")

Instead of the former proprietary `PCBA 06` board, the tool-free pannier breakaway connection is engineered as a **pure 2-wire DC system (5V / GND)** with an industrial **2-Pin Magnetic Pogo Breakaway Coupler (IP68 COTS)**:
* Industrial 2-Pin magnetic pogo connector (HytePro M411, IP68 rated, gold-plated contacts, N52 neodymium magnets).
* Rated up to $2.5\,\text{A}$ continuous DC current at $12\,\text{V}/5\,\text{V}$; contact resistance $< 30\,\text{m}\Omega$.
* **Breakaway Safety:** Separates non-destructively at $10\dots 15\,\text{N}$ axial pull force when the pannier is removed without manual uncoupling.
* **Sealing:** Single $\varnothing 12\,\text{mm}$ bore in the forward pannier wall accepts split EPDM/TPU grommet ([`010_saddlebag_hole_grommet_split.scad`](../../hardware/cad/scad/02_pod_base/parts/010_saddlebag_hole_grommet_split.scad)). The pannier floor remains 100% intact and watertight.

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
   * **Fitment:** Seats inside the $5.0 \times 4.0\,\text{mm}$ cutout at the $+X$ flank of the OMM UCS enclosure ([`omm_ucs_bottom_shell.scad`](../../hardware/cad/scad/03_pod_cartridges/parts/omm_ucs_module.scad)) to maintain IP67 water and dust sealing.

4. **Compact Helmet Stubby Antennas (COTS Stubby Antennas):**
   * **Stubby Antenna 1 (OMM 2.4 GHz HD-Mesh, PCBA 09):**
     - 2.4 GHz ISM band stubby antenna ($2400\dots 2500\,\text{MHz}$), $+2.0\dots +2.5\,\text{dBi}$ omnidirectional gain.
     - SMA-Male connector, overall length only **$35\dots 40\,\text{mm}$**, diameter $\varnothing 8\,\text{mm}$, weight approx. $6\,\text{g}$.
     - Rubber-duck flexible TPU jacket prevents helmet buffeting, wind whistle, and lever forces at highway speeds.
   * **Stubby Antenna 2 (OMM 446 MHz PMR/DMR, PCBA 10):**
     - 446 MHz PMR446 / DMR Tier I stubby antenna ($430\dots 470\,\text{MHz}$, resonant at $446.1\,\text{MHz}$), approx. $0\dots +1.5\,\text{dBi}$ gain.
     - SMA-Male connector, length approx. **$45\dots 50\,\text{mm}$**, diameter $\varnothing 10\,\text{mm}$, weight approx. $9\,\text{g}$.
     - Shortened helical coil inside flexible shock-damping rubber jacket. Delivers $1.5\dots 2.5\,\text{km}$ range with full rider ergonomics.

5. **Optional Fixed-Installation Upgrade in Cartridge Pod (5V COTS Bi-Directional Booster / LNA):**
   * **Purpose:** For permanent fixed installations of OMM modules in sealed cartridges (`has_sma_port = false`), compensating for luggage lid and rider body shadowing without external holes or appendages.
   * **Specification:** Ultra-compact 5V bi-directional RF booster module ($25 \times 15\,\text{mm}$) featuring an integrated Low-Noise Amplifier (+12 dB RX gain, NF < 2.5 dB) and automatic T/R power detection.
   * **100% Modular Decoupling:** Seats form-fittingly in the rear cradle bay of `cartridge_insert_omm_ucs.scad` and draws 5V from `PCBA 03`. The universal carrier board `PCBA 03` remains completely untouched and identical across Sena and Cardo cartridges.
   * **Power Supply via 2-Pin Branch from `J_AUDIO_PWR`:** The 5V DC supply ($< 100\,\text{mA}$) branches directly off **Pin 1 (`PGND`)** and **Pin 2 (`VCC_5V`)** of the 8-pin cartridge gateway harness. Because the booster return current flows exclusively across `PGND` and the audio ground lines (`AGND_SPK`, `AGND_MIC`) remain zero-current, Kelvin ground isolation is 100% maintained – zero common-impedance RF whine in helmet audio!

---

## 12. COTS Hardware & Fastener Procurement List (1 Complete Kit)

| Component | Specification / Type | Sourcing Source | Qty | Location & Purpose |
| :--- | :--- | :--- | :---: | :--- |
| **M3 Stainless Screws** | M3 x 40 mm Socket Head A4 / 316 (DIN 912) | Standard Fastener | 4 pcs | Central Box enclosure (engages nut pockets) |
| **M3 Stainless Screws (Front)**| M3 x 20 mm Socket Head A4 / 316 (DIN 912) | Standard Fastener | 4 pcs | Front Node enclosure (engages nut pockets) |
| **M3 Stainless Screws (Dock)** | M3 x 16 mm Socket Head A4 / 316 (DIN 912) | Standard Fastener | 4 pcs | Frame clamp `cots_magnetic_frame_dock` |
| **M3 Stainless Nuts** | DIN 934 / DIN 985 M3 A4 Nuts | Standard Fastener | 12 pcs| Captive in nut pockets (Central Box, Front Node, Frame Dock) |
| **M4 Stainless Nuts (AMPS & Radar)**| DIN 934 M4 A4 Nuts | Standard Fastener | 6 pcs | 4x Front Node tub (AMPS), 2x Radar 2.0 rear housing |
| **M4 Screws (Radar Cradle)** | M4 x 12 mm Socket Head A4 (DIN 912) | Standard Fastener | 2 pcs | Securing cradle `radar_swivel_tilt_cradle` to Radar 2.0 housing |
| **M5 Hirth Pivot Bolt** | M5 x 25 mm Socket Head A4 (DIN 912) | Standard Fastener | 1 pc | Horizontal pivot bolt for radar Hirth joint |
| **M5 Stainless Nut (Radar)** | DIN 934 M5 A4 Nut | Standard Fastener | 1 pc | Captive in right fork of radar mount |
| **M5 Clamp Screws (Adventure)** | M5 x 25 mm Socket Head A4 (DIN 912) | Standard Fastener | 2 pcs | Clamp cap `adventure_rack_radar_mount` (bottom access) |
| **M5 Nuts (Adventure Clamp)** | DIN 934 M5 A4 Nuts | Standard Fastener | 2 pcs | Captive in clamp cap `adventure_rack_radar_clamp_cap` |
| **M8 IP68 Cable Gland** | M8 x 1.25 Nickel-plated brass / PA66 with EPDM seal | Skintop / Lapp | 1 pc | Watertight bottom entry gland for 2-wire FLRY-B cable |
| **M2.5 Board Screws** | M2.5 x 6 mm Socket Head A4 (DIN 912) | Standard Fastener | 8 pcs | 4x Central Box PCB, 4x Front Node PCB |
| **M2 Cartridge Board Screws** | M2 x 6 mm Pan/Socket Head A4 (DIN 7985/912) | Standard Fastener | 8 pcs | Securing PCBA 03 to cartridge sled (4x per sled; bulkhead screws completely eliminated) |
| **M2 Sled Retainer Screws** | M2 x 6 mm Countersunk A4 (DIN 7991) | Standard Fastener | 8 pcs | Securing actuator hold-down brackets (4x per gateway) |
| **M2 UCS Enclosure Screws** | M2 x 8 mm Socket Head A4 (DIN 912) | Standard Fastener | 4-8 pcs| OMM UCS module enclosure (engages captive M2 nuts) |
| **M2 UCS Stainless Nuts** | DIN 934 M2 A4 Nuts | Standard Fastener | 4-8 pcs| Captive in upper shell of OMM UCS module |
| **OMM LiPo Pouch Battery** | 1S LiPo 600 mAh ($38 \times 24 \times 4.5\,\text{mm}$) with PCM | EEMB / Web | 1-2 pcs| Internal battery for OMM UCS module (12-14 h runtime) |
| **OMM Silicone Gasket** | Silicone solid cord $\varnothing 0.8\,\text{mm}$ Shore 40A | O-Ring Supplier | 0.5 m | IP67 perimeter seal for OMM UCS module |
| **OMM Helmet Audio & PTT Harness**| 6-Pin JST-SH 1.0mm Socket to 3.5mm Jack + Mic + PTT | COTS Standard | 1-2 pcs| Pure audio headset harness for helmet interior (0V DC, 12-15 cm) |
| **RF Coax Pigtail U.FL to SMA**| RG-178 / 1.13mm (50 mm) with IP67 SMA Bulkhead & O-Ring | COTS Standard | 1-2 pcs| Connection from U.FL port to enclosure feedthrough on OMM UCS |
| **OMM 2.4 GHz Stubby Antenna** | 2.4 GHz Stubby Rubber Antenna (38 mm, SMA-Male) | COTS Standard | 1 pc | Compact helical antenna for OMM 2.4G helmet use (zero buffeting) |
| **OMM 446 MHz Stubby Antenna** | 446 MHz PMR/DMR Stubby Antenna (48 mm, SMA-Male) | COTS Standard | 1 pc | Compact helical antenna for OMM 446 helmet use (1.5-2.5 km range) |
| **M2 Pivot Dowel Pins** | M2 x 8 mm Stainless Dowel Pin (DIN 7) | Standard / Misumi | 2 pcs | Pivot pins for magnetic cartridge latches |
| **Magnetic Armature** | Ø 6 x 8 mm Hardened Steel Pin (DIN 6325) | Standard / Misumi | 2 pcs | Steel keeper pin in cartridge latch arm |
| **Latch Return Springs** | Stainless 316 ($\varnothing 3.5\,\text{mm}, L_0=10\,\text{mm}$) | Standard Spring | 2 pcs | Return springs for latch hook |
| **Ejection Springs** | Stainless 316 ($D=4.5\,\text{mm}, L_0=15\,\text{mm}$) | Standard Spring | 4 pcs | Auto-eject springs inside bulkheads (2x per pod) |
| **N52 Release Key** | N52 Neodymium Block ($20 \times 10 \times 5\,\text{mm}$) | Magnet Supplier | 1 pc | Magnetic key for manual cartridge release |
| **Vibration Isolators** | Type A M4 Male/Female ($\varnothing 15 \times 10\,\text{mm}$) | Ganter / Standard | 4 pcs | Shock-isolated Central Box mounting |
| **Silicone O-Ring Cord** | Silicone Solid Cord $\varnothing 1.5\,\text{mm}$ Shore 40A (1.0 m) | O-Ring Supplier | 1 pc | 40 cm Central Box groove, 30 cm Front Node groove |
| **Cartridge Gaskets** | Molded Silicone Gasket Shore 40A ($54 \times 18\,\text{mm}$) | Custom Mold | 2 pcs | Front face mouth sealing on Pod 1 and Pod 2 |
| **UPS Battery Pack** | 1S LiPo Flat Pack 2,200 mAh ($68 \times 39 \times 5.0\,\text{mm}$) with Micro-Fit | EEMB / Enerpower | 1 pc | Central Box UPS buffer (Type 504068 / 503870) |
| **Automotive Fuse Holder** | Waterproof Blade Fuse Holder + 2A Fuse | Hella / MTA | 1 pc | KL30 battery terminal line protection |
| **2-Pin Magnetic Breakaway**| IP68 Magnetic Plug + Socket (e.g., HytePro M411) | COTS Standard | 2 sets | Pannier breakaway connection (10-15 N pull force) |
| **Pure DC 2-Wire Cable (PUR)**| 2x 0.34 mm² (AWG22) with JST-JWPF 2-Pin / Magnetic Pogo | COTS Standard | 2 pcs | Pure 5V DC power to Pod 1 and Pod 2 (data 100% via UWB) |
| **Radar 12V Cable (PUR)** | 2x 0.5 mm² (AWG20) with JST-JWPF 2-Pin IP67 Plug | COTS Standard | Opt. (1)| 12V DC feed to rear radar (data 100% via UWB) |
| **DTM-12 Breakout Harness** | Deutsch DTM 12-Pin Pre-terminated IP68 Harness | TE Connectivity | 1 pc | Automotive master harness from Central Box |
| **Front Node 12V Cable** | 2-Pin JST-PH Lead with Posi-Tap | COTS Standard | 1 pc | Local cockpit power connection (parking light/GPS plug) |
| **J_ACT Actuator Harness** | Pre-crimped 8-Pin JST-SH to 4x 2-Pin Leads | Adafruit / SparkFun | 2 pcs | Pre-assembled harness for 4 solenoids (C160404) |
| **Miniature Solenoids** | 5V DC Pull Solenoids ($\varnothing 6.5 \times 12\,\text{mm}$) with TPU Tip | Solenoid Supplier | 8 pcs | 4 pcs per Smart Cartridge (Sena / Cardo) |
| **J_AUDIO_PWR Gateway Cable**| Pre-crimped 8-Pin JST-SH to Jack / Direct-DC / USB | COTS Standard | 2 pcs | Audio & power harness to headset inlays (Kelvin Grounded) |
| **Wheeltec MR20 77-GHz mmWave**| 77-GHz FMCW Automotive Radar (150 m Range) | Wheeltec | Opt. (1)| Radar 2.0 transceiver module inside rear housing |
| **PC Radome Window** | Laser-cut Polycarbonate 1.6 mm (RF-transparent)| COTS / Plexiglas | Opt. (1)| Microwave & optical window for MR20 & 24-LED Halo |
| **3M Dual Lock SJ3550** | Interlocking Adhesive Fastener Strip (VHB) | 3M | 0.5 m | Vibration-resistant, tool-free module mounting |
| **car_sun_visor_pod_clip** | 3D Printed PA12 Sun Visor Clips | OMB CAD | Opt. (2)| Chase car / van visor mounting kit for Pod 1 & 2 |

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
   * **The OpenMotorBridge Solution:** The rider's expensive helmet remains untouched for years, connected strictly via standard Bluetooth to the Central Box. There is zero redundant purchase of proprietary helmet units. When the group's mesh technology advances, only the bike-mounted cartridge module is swapped or upgraded via open OMM 2.4G / OMM 446.
3. **Mechatronic Advantage: Dedicated Pushbuttons vs. Jog Dials ("Poison for Mechatronics"):**
   * Rotary jog dials (such as on the Sena 50S, 20S, 30K, or new 60S) introduce mechanical rotational backlash, soft stops without tactile feedback, and require complex angular torque actuators. For mechatronic solenoids or micro-plungers (handling automated Power ON/OFF), jog dials are poison for mechatronic reliability.
   * **Strict Procurement Recommendation:** For cartridge bay installation, strictly select units with **dedicated, tactile pushbuttons**:
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
   * JST-SH / JST-PH pin headers (`J1..J12` Front Node, `J1..J2` Cartridges)
   * MicroSD card slot (`J2` Central Box)
2. **Acoustic Sensors & Venting:**
   * **MEMS Microphone (`MIC1` MSM261S4030H0R on PCBA 05):** Acoustic inlet port ($\varnothing 0.5\,\text{mm}$) must be sealed with a Kapton dot!
   * **Equalization Vent (Gore ePTFE Vent):** Must remain free of lacquer.
3. **RF Antenna Connectors & Test Points:**
   * U.FL coaxial sockets (`ANT1`, `ANT2`)
   * Test points for in-circuit programming and oscilloscope probing
