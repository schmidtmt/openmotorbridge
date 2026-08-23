# 15 - Bill of Materials (BOM) & Manufacturing Guide

Complete component list and manufacturing specifications for SMT pick-and-place assembly (PCBA) via JLCPCB / Eurocircuits.

---

## 1. Central Main Box PCB (Main Box PCBA)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | ESP32-S3-WROOM-1-N16R8 | Espressif Systems | SMD Module | C2913200 | Main MCU (Dual-Core, 16 MB Flash, 8 MB PSRAM) |
| **U2** | LM5164-Q1 | Texas Instruments | SOIC-8-EP | C2843477 | Automotive 65V Synchronous Buck Converter |
| **U3** | BQ24075RGTR | Texas Instruments | VQFN-16 | C128509 | Dynamic Power-Path Management & LiPo Charger with TS |
| **U4** | BMI270 | Bosch Sensortec | LGA-14 | C2838380 | 6-Axis IMU for Lean Angle & Motion Detection |
| **U5** | ES8388 | Everest Semi | QFN-28 | C144547 | 24-Bit Stereo Audio Codec (I2S ADC/DAC) |
| **U6** | TCAN334GDCNR | Texas Instruments | SOT-23-8 | C842340 | 3.3V Automotive CAN-FD Transceiver (±58V Fault) |
| **T1, T2** | LM-NP-1001-B1L | Bourns Inc. | SMD Transformer | C114402 | 1:1 Audio Transformer (1500 V RMS Galvanic Isolation) |
| **OC1, OC2**| TLP222A(F) | Toshiba | SOP-4 | C112444 | Solid-State PhotoMOS Relay for PTT Button Simulation |
| **D1** | SMBJ33CA | Littelfuse | DO-214AA (SMB) | C87848 | TVS Diode (33 V Standoff, 53.3 V max Clamping) |
| **F1** | MF-MSMF050-2 | Bourns | 1812 SMD | C22668 | Resettable PPTC Fuse (500 mA Hold / 1.0 A Trip) |
| **TH1** | NCP18XH103F03RB | Murata | 0603 SMD | C25804 | 10k NTC Thermistor for BQ24075 JEITA Thermal Cutoff |
| **J1** | 2x13 Box Header | Standard 2.54 mm | THT Box Header | C2934175 | Internal Ribbon Header to HD26 Flange Connector |
| **J2** | MicroSD Slot Push-Push | Molex / Korean Hro | SMD Push-Push | C266624 | 4-Bit SDIO Memory Card Slot for Tour Logging |
| **CN1** | HD26 Socket IP67 | Amphenol LTW | Flange D-Sub | Custom Part | Waterproof 26-pin Outer Enclosure Interface |

---

## 2. Rear Pod 3 Transceiver PCB (Rear Pod 3 PCBA)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U10** | ESP32-C3-WROOM-02-N4 | Espressif Systems | SMD Module | C2868705 | 32-Bit RISC-V Co-Processor (NMEA & LoRa Parser) |
| **U11** | MAX-M10S-00B | u-blox | LGA-18 | C3006240 | Multi-Constellation GNSS Engine (10 Hz, 1-PPS) |
| **U12** | SX1262IMLTRT | Semtech | QFN-24 | C190184 | OpenMotorMesh 868 MHz LoRa Transceiver (+22 dBm) |
| **U13** | DS2401Z+ | Maxim / ADI | SOT-223 / TO-92 | C14440 | 64-Bit 1-Wire Silicon Serial Number ID |
| **U14** | TPS7A0533PDBVR | Texas Instruments | SOT-23-5 | C505293 | Ultra-Low-Noise 3.3V LDO (200 mA) for GNSS/LoRa |
| **ANT1** | GP.1575.25.4.A.02 | Taoglas | 25x25x4 mm Patch | C2689100 | Ceramic Patch Antenna for GPS/Galileo |
| **ANT2** | ANT-868-CW-HWR-SMA | Linx / Taoglas | Helical Antenna | C290111 | 868 MHz Helical Antenna for Rear Fender |
| **CN3** | 824-22-006-00-001101 | Mill-Max | SMD Pad Header | C189201 | 6-Pin Gold-Plated Pogo Target Contact Array |

---

## 3. Universal Pod Cartridge (Pod 1 & Pod 2 Cartridge PCBA)

| Designator | Component / MPN | Manufacturer | Package | LCSC / JLCPCB Part # | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U20** | DS2401Z+ | Maxim / ADI | SOT-223 | C14440 | 64-Bit 1-Wire Silicon Serial Number (Cartridge ID) |
| **D20** | IP4220CZ6 | Nexperia | SOT-457 | C119330 | 4-Channel ESD Protection Array for Audio & Opto Lines |
| **CN2** | 824-22-006-00-001101 | Mill-Max | SMD Pad Header | C189201 | 6-Pin Gold-Plated Pogo Target Contact Array |

---

## 4. Assembly & Manufacturing Instructions
- **CPL Rotation Verification:** Pay close attention to pin 1 orientation for the Bourns transformers (T1, T2), optocouplers (OC1, OC2), and QFN packages (ES8388, SX1262) in the CPL file.
- **Enclosure Manufacturing:** HP Multi Jet Fusion (MJF) in PA12 Black, glass-bead blasted, and vapor-sealed against fuel and oil exposure.
- **Seals:** Custom molded silicone O-rings (Shore 50 A) for IP67 enclosure lid and cartridge bays.
