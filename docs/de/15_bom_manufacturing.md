# 15 - BOM & Fertigungsleitfaden

## 1. Kern-Bauelemente (SMT-Bestueckung via JLCPCB)

| Designator | Bauteil | Hersteller / MPN | Gehaeuse | Funktion |
| :--- | :--- | :--- | :--- | :--- |
| **U1** | ESP32-S3-WROOM-1-N16R8 | Espressif Systems | SMD Modul | Haupt-MCU (Dual-Core, 16 MB Flash, 8 MB PSRAM) |
| **U2** | LM5164-Q1 | Texas Instruments | SOIC-8-EP | Automotive 65V Synchronous Buck Converter |
| **U3** | BQ24075RGTR | Texas Instruments | VQFN-16 | Dynamisches Power-Path Management & LiPo-Lader mit TS |
| **U4** | BMI270 | Bosch Sensortec | LGA-14 | 6-Achsen IMU fuer Schraeglagen- & Bewegungserkennung |
| **U5** | ES8388 | Everest Semi | QFN-28 | **24-Bit Stereo Audio Codec (I2S ADC/DAC)** |
| **U6** | TCAN334GDCNR | Texas Instruments | SOT-23-8 | **3.3V Automotive CAN-FD Transceiver (+-58V Fault)** |
| **T1, T2** | LM-NP-1001-B1L | Bourns Inc. | SMD Uebertrager | 1:1 Audio-Uebertrager (1500 V RMS galvanische Trennung) |
| **OC1, OC2** | TLP222A(F) | Toshiba | SOP-4 | Halbleiter-PhotoMOS-Relais fuer Tastensimulation |
| **D1** | SMBJ33CA | Littelfuse | SMB / DO-214AA | **TVS-Diode (33 V Standoff, 53.3 V max Clamping)** |
| **F1** | MF-MSMF050-2 | Bourns | 1812 SMD | **Rueckstellbare PPTC-Sicherung (500 mA Hold / 1.0 A Trip)** |
| **TH1** | NCP18XH103F03RB | Murata | 0603 SMD | **10k NTC Thermistor fuer BQ24075 JEITA-Temperaturschutz** |
| **J1** | 2x13 Wannenstecker | Standard 2.54 mm | THT | Interner Pfostenverbinder zur HD26-Buchse |
| **CN1** | HD26 Buchse IP67 | Amphenol / D-Sub HD | Flansch | Wasserdichte 26-polige Gehaeuseschnittstelle |

## 2. Fertigungshinweise & CPL-Ausrichtung
- **CPL-Rotationsabgleich:** Bei der JLCPCB-Bestueckung ist auf die Pin-1-Ausrichtung der Bourns-Uebertrager, TLP222A Optokoppler und des ES8388 QFN-28 im CPL-File zu achten.
- **Gehaeuse (Typ A & B):** HP Multi Jet Fusion (MJF) in PA12 Schwarz, kugelgestrahlt und im Heissbad versiegelt.
- **Dichtungen:** Massgefertigte Silikon-O-Ringe (Shore-Haerte 50 A) fuer Deckel und Kassetten-Einschuebe.
- **Pogo-Pins:** Mill-Max 824-22-006-00-001101 6-polige Federkontaktleiste mit 1.4 mm Arbeitshub.
