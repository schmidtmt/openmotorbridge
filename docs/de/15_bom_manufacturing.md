# 15 - Stücklisten (BOM), COTS-Kaufteile & SMT-Fertigungsdaten (Alle 7 PCBAs)

Dieses Dokument ist die zentrale Referenz (Single Source of Truth) für die vollständige Bauteilliste (Bill of Materials), die Fertigungsspezifikationen aller 7 Leiterplatten (PCBA 01 bis PCBA 03, PCBA 05 bis PCBA 08 – PCBA 04 ist in v8.0 ersatzlos entfallen) bei JLCPCB / Eurocircuits, alle mechanischen 3D-Druck-Komponenten, die COTS-Einkaufslisten sowie eine detaillierte Kosten- und Bestellkalkulation (Solo-Aufbau vs. Sammelbestellung).

---

## 1. PCBA 01: Zentralbox Hauptplatine (`openmotorbridge_central_box`, 4-Layer FR4 TG150)

| Designator | Bauteil / MPN | Hersteller | Gehäuse | LCSC / JLCPCB Part # | Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | ESP32-S3-WROOM-1-N16R8 | Espressif Systems | SMD Modul | C2913200 | Haupt-MCU (Dual-Core, 16 MB Flash, 8 MB PSRAM) |
| **U2** | LM5164-Q1 | Texas Instruments | SOIC-8-EP | C2843477 | Automotive 65V Synchronous Buck Converter |
| **U3** | BQ24075RGTR | Texas Instruments | VQFN-16 | C15464 | Dynamisches Power-Path Management & LiPo-Lader mit TS |
| **U4** | BMI270 | Bosch Sensortec | LGA-14 | C2836813 | 6-Achsen IMU für Schräglagen- & Bewegungserkennung |
| **U5** | ES8388 | Everest Semi | QFN-28 | C365736 | 24-Bit Stereo Audio Codec (I2S ADC/DAC) |
| **U6** | TCAN334GDCNR | Texas Instruments | SOT-23-8 | C842340 | 3.3V Automotive CAN-FD Transceiver (±58V Fault) |
| **U7** | SX1262IMLTRT | Semtech | QFN-24 | C190184 | Onboard 868 MHz LoRa Transceiver (+22 dBm, 24/7 USV-gepuffert) |
| **U8** | DW3110 | Qorvo | QFN-16 (B.Cu) | C2934600 | IEEE 802.15.4z UWB Transceiver (6.5 GHz Ch. 5 Backbone) |
| **T1, T2** | LM-NP-1001-B1L | Bourns Inc. | SMD Übertrager | C114402 | 1:1 Audio-Übertrager (1500 V RMS galvanische Trennung) |
| **OC1, OC2**| TLP222A(F) | Toshiba | SOP-4 | C112444 | Halbleiter-PhotoMOS-Relais für PTT-Tastensimulation |
| **D1** | SMBJ33CA | Littelfuse | DO-214AA (SMB) | C87848 | TVS-Diode (33 V Standoff, 53.3 V max Clamping) |
| **F1** | MF-MSMF050-2 | Bourns | 1812 SMD | C22668 | Rückstellbare PPTC-Sicherung (500 mA Hold / 1.0 A Trip) |
| **LED1** | WS2812B-B | Worldsemi | 5050 SMD | C114586 | RGB Status-LED für optische Betriebsmodusanzeige |
| **J1** | 2x13 Wannenstecker | Standard 2.54 mm | THT Box Header | C2934175 | Interner Pfostenverbinder zur HD26-Flanschbuchse |
| **J2** | MicroSD Slot Push-Push | Molex / Korean Hro | SMD Push-Push | C266624 | 4-Bit SDIO Speicherkarte für Tour-Logging |
| **J_BAT** | Molex Micro-Fit 3.0 2P | Molex | SMD Header | C289110 | Steckverbindung zum 2.200 mAh LiPo Pufferakku |
| **ANT1** | U.FL-R-SMT-1 | Hirose / Murata | SMD HF | C2834595 | LoRa 868 MHz U.FL Buchse zu Taoglas FXP895 im Deckel |
| **ANT2** | U.FL-R-SMT-1 | Hirose / Murata | SMD HF (B.Cu) | C2834595 | UWB 6.5 GHz U.FL Buchse zu Taoglas FXUWB10 im Boden |
| **CN1** | HD26 Buchse IP67 (SEAL-D)| Amphenol LTW | Flansch D-Sub | Kundenteil | Wasserdichte 26-polige Gehäuseschnittstelle (19 Pins aktiv) |

---

## 2. PCBA 02: Satelliten Pod Base Carrier (`openmotorbridge_pod_base`, 2-Layer FR4)
> **Hinweis zur Stückzahl:** Die Pod-Basis ist zu 100 % symmetrisch und wird **2x pro Motorrad** verbaut (Pod 1 links, Pod 2 rechts).

| Designator | Bauteil / MPN | Hersteller | Gehäuse | LCSC / JLCPCB Part # | Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **J1** | PinHeader_1x06_P2.54mm_SMD | Harwin / Wurth | SMD Vertikal | C2934176 | 6-Pin Stiftleiste im Schottwand-Schutzkragen |
| **J2** | M8_6PIN_RECEPTACLE (A-Coded)| Binder / Phoenix | M8 Rundsteckverbinder | C289100 | M8 6-Pin IP67 Buchse zur Zuleitung |
| **U1** | SP3012-06UTG | Littelfuse | DFN-14 (3.5x1.35mm)| C2834580 | 6-Kanal Ultra-Low-Cap ESD-Schutzarray (< 0.5 pF) |
| **C1** | 100nF 50V X7R | Samsung / Yageo | 0603 SMD | C14663 | Entkopplungskondensator für 5V Versorgungsspannung |

---

## 3. PCBA 03: Smart Modular Cartridge Rev 2.0 (`openmotorbridge_pod_cartridge`, 2-Layer FR4)
> **Hinweis zur Stückzahl:** Wird **2x pro Motorrad** bestückt (Slot 1 für Sena SPIDER X Slim, Slot 2 für Cardo Packtalk Edge oder optional OMM 2.4 GHz Swap Cartridge).

| Designator | Bauteil / MPN | Hersteller | Gehäuse | LCSC / JLCPCB Part # | Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | CH32V003F4P6 | WCH | TSSOP-20 / QFN-20 | C3011382 | 32-Bit RISC-V MCU (1-Wire ROM-ID Emulation & ISP Makro-Controller) |
| **Q1, Q2, Q3, Q4** | AO3400A | Alpha & Omega | SOT-23 | C20917 | 30V / 5.7A N-Kanal Power-MOSFETs für 4x Mechatronik-Aktuatoren |
| **D3, D4, D5, D6** | 1N4148WS | Diodes Inc. / LRC | SOD-323 | C81598 | Freilauf-Schutzdioden für induktive Aktuator-Spulen |
| **J1** | PinSocket_1x06_P2.54mm_SMD | Harwin / Samtec | SMD Horizontal | C2934177 | Stirnseitige 6-Pin Präzisionsbuchse zur Pod-Base |
| **J2** | JST-SH 1.0mm 6-Pin Horizontal| JST | SMD Liegend | C136657 | Audio Diff & Direct-DC Kabelpeitsche zum Headset-Inlay |
| **J_ACT** | JST-SH 1.0mm 8-Pin Horizontal| JST | SMD Liegend | C136659 | Mechatronik-Header für 4 unabhängige Miniatur-Hubmagnete |
| **F1** | MF-MSMF050-2 (500mA) | Bourns | 1812 SMD | C22668 | Rückstellbare PPTC-Sicherung für Kassettenstromkreis |
| **D1** | Duo-Status-LED Grün/Blau | Everlight / Xinglight | 0805 SMD | C2834575 | Status-LED: Grün = 1-Wire Active / Config Synced, Blau = Aktuator-Impuls |
| **D2** | SP3012-06UTG | Littelfuse | DFN-14 | C2834580 | 6-Kanal Ultra-Low-Cap ESD-Schutzmatrix für Audio & Daten |
| **C1, C2** | 100nF 50V X7R | Samsung | 0603 SMD | C14663 | Entkopplungskondensatoren für VCC und MCU |

---

## 4. Baugruppe PCBA 04 (Heck-Pod 3): Ersatzlos entfallen (Clean Architecture v8.0)

> [!NOTE]
> **Architektur-Bereinigung v8.0:** Die Leiterplatte `PCBA 04` und das dritte Satellitengehäuse (Heck-Pod 3) wurden **vollständig und ersatzlos gestrichen**:
> 1. **LoRa 868 MHz (SX1262):** Sitzt nun direkt auf der Zentralbox (`PCBA 01`), gepuffert durch den USV-Akku (24/7 Diebstahl-Sentry).
> 2. **Multi-GNSS (SAM-M10Q):** Sitzt im kühlen Fahrtwindbereich am Front-Knoten (`PCBA 05`), angebunden über Qwiic I2C (`J12`).
> 3. **Fahrzeug-Backbone:** Erfolgt drahtlos über Ultra-Wideband (Qorvo DW3110 / 6.5 GHz Ch. 5, $< 0{,}4\,\text{ms}$ Latenz) zwischen Front-Knoten und Zentralbox.
> 4. **Heck-Radar:** Schließt direkt über Peitsche 5 des HD26-Kabelbaums an die Zentralbox an.

---

## 5. PCBA 05: Universal Front-Knoten (`openmotorbridge_front_node`, 4-Layer FR4 TG150, 82 x 50 mm)

| Designator | Bauteil / MPN | Hersteller | Gehäuse | LCSC / JLCPCB Part # | Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | ESP32-S3-WROOM-1U-N8R8 | Espressif Systems | SMD Modul | `C2913200` | Dual-Core 32-Bit Xtensa LX7 (240 MHz, Vektor-DSP, 8MB PSRAM, ext. U.FL) |
| **U2** | USB2514Bi-AEZG / USB2514B | Microchip | QFN-36 | `C16251` | Automotive/Industrial USB 2.0 High-Speed 480 Mbps 4-Port Hub Controller |
| **U3** | LMR36015FSCQRNXRQ1 | Texas Instruments | VQFN-12 | `C2843480` | Automotive 36V Synchronous Buck (5V / 2.0A, 91.8%) für Hub & Peripherie |
| **U4** | TPS2051BDBVR | Texas Instruments | SOT-23-5 | `C7818` | High-Side USB VBUS Power Switch (1.05A Clamp) für Port 2 Kaltstart-Reset |
| **U5** | SC8102QDER | Southchip | QFN-32 | `C2843510` | Automotive Synchronous Buck mit USB-PD 20W (9V/2.2A & QC3.0) für Smartphone Port 1 |
| **U6** | TCAN334GDCNT | Texas Instruments | SOT-23-8 | `C2843515` | 3.3V CAN-Transceiver (5 Mbps CAN-FD fähig, mit Pin 8 Silent-Listen-Only Mode) |
| **U7** | DW3110 | Qorvo | QFN-16 (B.Cu) | `C2934600` | IEEE 802.15.4z UWB Transceiver (6.5 GHz Ch. 5 Backbone) |
| **K1** | CPC1017NTR | IXYS / Littelfuse | SOP-4 | `C26789` | 60V / 100mA 1-Form-A Solid-State Relais für schaltbaren 120R CAN-Abschluss (Auto-Sensing) |
| **Q1** | DMN63D8LDW-7 | Diodes Incorporated| SOT-363 | `C283890` | Dual N-Kanal MOSFET (30V / 260mA) für richtungsgetrennte Spiegel-Totwinkel-LEDs (J9) |
| **Q2** | TPS1H100BQPWPRQ1 | Texas Instruments | HTSSOP-14 | `C2843520` | Automotive Smart High-Side Power Switch (bis 3.5A / 40W) für 12V Aux Light (J11) |
| **LED1**| WS2812B-2020 | Worldsemi | SMD 2020 | `C2843530` | Digital steuerbare RGB-Status-LED für Gehäusedeckel-Lichtleiter |
| **MIC1**| MSM261S4030H0R / SPH0645 | Sipeed / Knowles | 3.5x2.65 mm SMD | `C544577` | Digitales I2S-MEMS Akustik-Mikrofon (Standard-I2S, hohe Verfügbarkeit) |
| **L1** | 4.7 µH Automotive Inductor | Sunlord / Wurth | SMD 5x5 mm | `C2843490` | Speicherdrossel für LMR36015 5V-Hauptregler |
| **L2** | 10 µH Automotive Inductor | Coilcraft / Wurth | SMD 7x7 mm | `C2843525` | Speicherdrossel für SC8102 USB-PD Fast-Charge Buck (Port 1) |
| **J1** | JST-PH 2-Pin Header | JST | 2.00mm SMD | `C289115` | 12V Bordnetz-Einspeisung (KL15 & GND) |
| **J2** | JST-PH 3-Pin Header | JST | 2.00mm SMD | `C289116` | Cockpit CAN-Bus (CAN_H, CAN_L, GND mit Auto-Sensing Relais) |
| **J3** | JST-PH 4-Pin Header | JST | 2.00mm SMD | `C289117` | Lenker Multi-Button Interface (PTT, Cam-Action, Media-Voice, GND) |
| **J4** | JST-PH 4-Pin Header | JST | 2.00mm SMD | `C289117` | Upstream USB-Port zum Motorrad-Infotainment (Skyline OS / Boom! Box) |
| **J5** | JST-PH 4-Pin Header | JST | 2.00mm SMD | `C289117` | Port 1: Lenker-Smartphone (USB-PD 20W + High-Speed Data) |
| **J6** | JST-PH 4-Pin Header | JST | 2.00mm SMD | `C289117` | Port 2: Fairing Pigtail (geschirmt, 30 cm) zum CP2AA CarPlay/AA Dongle |
| **J5_MP3**| JST-PH 4-Pin Header | JST | 2.00mm SMD | `C289117` | Port 3: Handschuhfach-Kabel für USB-Sticks (MP3s & Firmware-Updates) |
| **J6_AUX**| JST-PH 4-Pin Header | JST | 2.00mm SMD | `C289117` | Port 4: Cockpit-Zubehör / Dashcam-Massenspeicher / Zūmo-Navi |
| **J7** | USB-C 16-Pin Receptacle IP67| GCT / Korean Hro | SMD Hybrid | `C2765186` | ESP32-S3 Service- & Flash-Port (Flanke) mit TPU-Dichtstopfen |
| **J8** | JST-PH 2-Pin Header | JST | 2.00mm SMD | `C289115` | Action-Cam 5V Charge-Only Power-Port (bis 2.0A) |
| **J9** | JST-PH 3-Pin Header | JST | 2.00mm SMD | `C289116` | Spiegel-Totwinkel-LEDs (12V_PROT, BSD_LEFT_N, BSD_RIGHT_N) |
| **J10** | JST-PH 2-Pin Header | JST | 2.00mm SMD | `C289115` | 12V Qi-Smartphone-Power (SP Connect / QuadLock Ladekopf) |
| **J11** | JST-PH 2-Pin Header | JST | 2.00mm SMD | `C289115` | 12V Aux Light (Adventure Zusatzscheinwerfer / Notbrems-Strobe) |
| **J12** | JST-SH 4-Pin Header | JST | 1.00mm SMD | `C289118` | Qwiic / STEMMA QT I2C Sensorport (SAM-M10Q GNSS, TMP117, OPT3001) |
| **ANT1**| U.FL-R-SMT-1 | Hirose / Murata | SMD HF (B.Cu) | `C2834595` | UWB 6.5 GHz U.FL Buchse zu Taoglas FXUWB10 im Boden |

---

## 6. PCBA 06: MagSafe Rahmendock-Adapter (`openmotorbridge_magsafe_dock`, 2-Layer FR4, 28 x 11.5 mm)

| Ref | Bauteil / Typ | Gehäuse | Spezifikation & Funktion | LCSC Part |
| :--- | :--- | :--- | :--- | :--- |
| **`F1`** | 0ZCG0050FF2C | SMD 1206 | 500 mA Hold / 1000 mA Trip, 16V PPTC Selbstrückstellende Sicherung | `C207936` |
| **`D1`** | ESD5Z5.0T1G | SOD-323 | 5,0V Unidirektionale TVS-Diode (Transient-Schutz) | `C2834585` |
| **`U1`** | USBLC6-4SC6 | SOT-23-6 | 4-Kanal ESD-Schutzarray ($<0{,}8\,\text{pF}$, $\pm 15\,\text{kV}$ ESD) | `C7519` |
| **`C1`** | 100nF 50V X7R | SMD 0603 | Keramischer Entkoppelkondensator auf VCC_PROT | `C14663` |
| **`J1`** | M8 Wire Pads | SMD/THT 1x07 | 7-poliges Lötpad-Array mit 0,6mm Durchkontaktierung für M8-Kabeladern | Custom |
| **`J2`** | MagSafe 6P Pads | SMD 1x06 | 6-polige vergoldete Kontaktflächen für MagSafe Magnet-Pogo-Kupplung | `C224376` |
| **`H1`** | MountingHole_Pad | M2.5 (Ø 2.7 mm) | Bohrung Ø 2.7 mm, Pad Ø 4.5 mm, geerdet an System-GND | Hardware |

---

## 7. PCBA 07: 2-in-1 LoRa Smart-Keyfob (`openmotorbridge_smart_keyfob`, 2-Layer FR4, 38 x 19 mm)

| Ref | Bauteil / Typ | Gehäuse | Spezifikation & Funktion | LCSC Part |
| :--- | :--- | :--- | :--- | :--- |
| **`U1`** | nRF52840-QIAA-R | aQFN-73 | 32-Bit ARM Cortex-M4F SoC mit Bluetooth 5.4, NFC & Crypto | `C190767` |
| **`U2`** | SX1262IMLTRT | QFN-24 | Semtech 868 MHz LoRa Transceiver (+22 dBm, TCXO) | `C90039` |
| **`U3`** | DRV2605LDGSR | VSSOP-10 | TI ERM/LRA Haptic Driver mit integrierter Effekt-Bibliothek | `C61633` |
| **`U4`** | BQ51003YFPR | DSBGA-28 | TI 2.5W Qi Wireless Power Receiver Controller | `C144862` |
| **`U5`** | BQ25100YFPR | DSBGA-6 | TI Linearer LiPo-Ladecontroller mit 50 nA Ruhestrom | `C144857` |
| **`M1`** | VG1036001D | Coin 10x3.6mm | Vybronics LRA Linearmotor (235 Hz Resonanzfrequenz) | Custom / Distrelec |
| **`BZ1`**| PKLCS1212E4001 | SMD 12x12mm | Murata SMD-Piezo-Schallwandler (85 dB @ 10 cm, 4 kHz) | `C94511` |

---

## 8. PCBA 08: Radar 2.0 Sub-MCU & 36-LED Flügel-Träger (`openmotorbridge_radar_submcu`, 4-Lagen FR4 TG150, 115 x 65 mm)

| Ref | Bauteil / Typ | Gehäuse | Spezifikation & Funktion | LCSC Part |
| :--- | :--- | :--- | :--- | :--- |
| **`U1`** | ESP32-C5-WROOM-1-N8 | SMD Modul | 32-Bit RISC-V Dual-Band Sub-MCU (2.4 GHz + 5.9 GHz V2X, 4MB Flash) | `C2843550` |
| **`U2`** | LDO 3.3V 500mA | SOT-23-5 | TI TPS7A0533 / Richtek RT9013 LDO Spannungsregler | `C505293` |
| **`D1..36`**| WS2812B-2020 | SMD 2020 | 36x Digital RGB-LEDs in Doppel-Warnflügeln (18 links, 18 rechts) | `C2843530` |
| **`ANT1`** | 5.9 GHz V2X Patch | 20x20x4 mm | Keramik-Patchantenne für ITS-G5 Car-to-X Sicherheitswarnungen | `C290456` |
| **`J1`** | JST-SH 1.0mm 4-Pin | SMD Liegend | Entkoppelte interne Signalpeitsche zur Binder M5 Gehäuse-Buchse | `C136657` |
| **`J2`** | JST-SH 1.0mm 4-Pin | SMD Liegend | UART-Verbindung zum Wheeltec MR20 Transceiver (RX/TX/5V/GND) | `C136657` |
| **`D_TVS`**| PESD5V0S2BT | SOT-23 | TVS-Dioden-Array für UART & Stromversorgung | `C2834580` |

---

## 9. 1-Click Bestellleitfaden für JLCPCB (Alle 7 Leiterplatten fertig bestückt)

Alle Fertigungsdaten liegen im Repository unter `hardware/pcba/` als fertige ZIP- und CSV-Pakete vor:

| Baugruppe / PCBA | Gerber-ZIP Datei | BOM CSV Datei | CPL (Pick & Place) CSV | Lagen | Fertigungs-Hinweis |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **PCBA 01: Zentralbox** | `01_main_box_pcba_gerbers_jlcpcb.zip` | `01_main_box_pcba_bom_jlcpcb.csv` | `01_main_box_pcba_cpl_jlcpcb.csv` | **4 Lagen** | ENIG (Gold), 1.6 mm, TG150, SMT beidseitig (DW3110 auf B.Cu) |
| **PCBA 02: Pod-Basis** | `02_pod_base_pcba_gerbers_jlcpcb.zip` | `02_pod_base_pcba_bom_jlcpcb.csv` | `02_pod_base_pcba_cpl_jlcpcb.csv` | **2 Lagen** | ENIG (Gold), 1.6 mm, SMT Top (2x pro Fahrzeug bestellen) |
| **PCBA 03: Kassetten-Träger**| `03_pod_cartridge_pcba_gerbers_jlcpcb.zip` | `03_pod_cartridge_pcba_bom_jlcpcb.csv` | `03_pod_cartridge_pcba_cpl_jlcpcb.csv` | **2 Lagen** | ENIG (Gold), 1.2 mm, SMT Top (2x pro Fahrzeug bestellen) |
| **PCBA 05: Front-Knoten** | `05_front_node_pcba_gerbers_jlcpcb.zip` | `05_front_node_pcba_bom_jlcpcb.csv` | `05_front_node_pcba_cpl_jlcpcb.csv` | **4 Lagen** | ENIG (Gold), 1.6 mm, TG150, SMT beidseitig (DW3110 auf B.Cu) |
| **PCBA 06: MagSafe Dock** | `06_magsafe_dock_pcba_gerbers_jlcpcb.zip` | `06_magsafe_dock_pcba_bom_jlcpcb.csv` | `06_magsafe_dock_pcba_cpl_jlcpcb.csv` | **2 Lagen** | ENIG (Gold), 1.6 mm, SMT Top |
| **PCBA 07: Smart-Keyfob** | `07_smart_keyfob_pcba_gerbers_jlcpcb.zip` | `07_smart_keyfob_pcba_bom_jlcpcb.csv` | `07_smart_keyfob_pcba_cpl_jlcpcb.csv` | **2 Lagen** | ENIG (Gold), 1.0 mm, SMT beidseitig |
| **PCBA 08: Radar 2.0 Sub-MCU** | `08_radar_submcu_pcba_gerbers_jlcpcb.zip` | `08_radar_submcu_pcba_bom_jlcpcb.csv` | `08_radar_submcu_pcba_cpl_jlcpcb.csv` | **2 Lagen** | ENIG (Gold), 1.2 mm, TG150, SMT Top |

---

## 10. Mechanik- & Gehäuse-BOM (3D-Druck MJF PA12 & Normteile)

Alle Gehäuseteile sind konsequent für das **IKEA-Prinzip** konstruiert: **Kein Einschmelzen von Gewindeeinsätzen mit dem Lötkolben erforderlich!** Die Gehäuse verfügen über integrierte Sechskant-Mutternaschen (Nut Pockets für Standard DIN 934 / DIN 985 Edelstahlmuttern) bzw. präzise Kernlöcher für gewindefurchende Kunststoffschrauben.

### 10.1 Basis-System (Universal für jedes Motorrad)
| Baugruppe | STL-Dateiname | Stück | Material & Fertigung | Funktion & Beschreibung |
| :--- | :--- | :---: | :--- | :--- |
| **Main Box Unterteil** | [`main_box_lower_case.stl`](../../hardware/cad/stl/01_main_box/main_box_lower_case.stl) | **1** | MJF PA12 / ASA | Monocoque-Unterwanne mit UWB-Bodentasche ($11 \times 11 \times 0{,}6\,\text{mm}$), 4x M4 Silentblock-Ohren & Dichtnut |
| **Main Box Zwischenboden** | [`main_box_mid_tray.stl`](../../hardware/cad/stl/01_main_box/main_box_mid_tray.stl) | **1** | MJF PA12 / ASA | Akku-Wanne für 2.200 mAh Flat-LiPo ($68 \times 39 \times 5{,}0\,\text{mm}$), 11x Konvektionsschlitze & Dichtfeder |
| **Main Box Deckel** | [`main_box_lid.stl`](../../hardware/cad/stl/01_main_box/main_box_lid.stl) | **1** | MJF PA12 / ASA | Gehäusedeckel mit LoRa FXP895 Tasche ($110 \times 20 \times 0{,}8\,\text{mm}$), Gore ePTFE-Ventilsitz & Schraubensenkungen |
| **Pod-Basisgehäuse** | [`pod_base_housing.stl`](../../hardware/cad/stl/02_pod_base/pod_base_housing.stl) | **2** | MJF PA12 / ASA | Universal-Schachtgehäuse für Pod 1 (Links) und Pod 2 (Rechts) |
| **Pod-Schottwände** | [`03_pod_bulkhead_partition.stl`](../../hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl) | **2** | MJF PA12 / ASA | Schottwand mit Dichtkragen & Federaufnahmen (1x pro Pod) |
| **Kassetten-Basisschlitten**| [`cartridge_base_sled.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl) | **2** | MJF PA12 / ASA | Universalschlitten für Gateway 1 (Pod 1) und Gateway 2 (Pod 2) |
| **Kassetten-Riegel / Wippe**| [`cartridge_magnetic_lock_latch.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_magnetic_lock_latch.stl) | **2** | MJF PA12 / ASA | Magnetische Diebstahlschutz-Rastwippen für Kassetten-Slots 1 & 2 |
| **Front-Knoten Unterwanne** | [`front_node_lower_tub.stl`](../../hardware/cad/stl/04_front_node/front_node_lower_tub.stl) | **1** | MJF PA12 / ASA | Cockpit-Wanne mit UWB-Bodentasche ($11 \times 11 \times 0{,}6\,\text{mm}$), AMPS-Bohrbild & Rohrbett |
| **Front-Knoten Deckel** | [`front_node_upper_lid.stl`](../../hardware/cad/stl/04_front_node/front_node_upper_lid.stl) | **1** | MJF PA12 / ASA | Deckel mit Knowles MEMS Schalleintritt & O-Ring-Dichtnut |
| **Front-Knoten Dichtkämme** | [`front_node_cable_glands_tpu.stl`](../../hardware/cad/stl/04_front_node/front_node_cable_glands_tpu.stl) | **1 Paar**| TPU 95A / 85A | Elastische Dichtkämme für Front-USB & Signale |
| **Front-Knoten USB-C Kappe**| [`front_node_usbc_cap_tpu.stl`](../../hardware/cad/stl/04_front_node/front_node_usbc_cap_tpu.stl) | **1** | TPU 95A / 85A | Elastische Staubschutzkappe mit Haltekollier für Service-Port |

### 10.2 Gateway-Kassetten-Inlays (Passend zur gewünschten Intercom-Ausstattung)
> **Hinweis zur Architektur:** Slot 1 und Slot 2 sind **Multi-Protokoll Gateway-Transceiver**, keine Fahrer/Beifahrer-Kopfhörer! Sie verbinden das Motorrad gleichzeitig mit Sena Mesh und Cardo DMC. Fahrer und Sozius funken drahtlos mit ihren normalen Helmen.

| Baugruppe | STL-Dateiname | Stück | Material | Funktion & Beschreibung |
| :--- | :--- | :---: | :--- | :--- |
| **Gateway-Inlay Sena** | [`cartridge_insert_sena.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) | *Opt. (1)* | MJF PA12 / ASA | Formschlüssiges Inlay für Sena SPIDER X Slim (Mesh 3.0 / 2.0, Direkt-Micro-Kabelpeitsche) |
| **Gateway-Inlay Cardo** | [`cartridge_insert_cardo.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl) | *Opt. (1)* | MJF PA12 / ASA | Inlay für Cardo Packtalk Edge / Pro (DMC Gen2) mit Air-Mount |
| **Swap-Inlay OMM 2.4 GHz** | [`cartridge_insert_omm.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_omm.stl) | *Opt. (1)* | MJF PA12 / ASA | Inlay für OMM 2.4 GHz Swap Cartridge (ESP32-C3) |
| **Blindkassette / Dry Box** | [`cartridge_insert_blindkassette.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_blindkassette.stl) | *Opt. (1)* | MJF PA12 / ASA | Hermetischer Schutzschlitten für ungenutzten Slot oder regendichte Dry Box |

### 10.3 Fahrzeugspezifische Montage-Kits (3D-Druckteile)
* **Kit 1: BMW R1250 / R1300 GS (Standard / Vario-Koffer):**
  * `adventure_transition_dock_base.stl` (2 Stk.): Kofferunabhängige Basis-Wannen für die Sitzbank-Bügelfalte (Ø 28 mm Rahmenrohr).
  * `adventure_transition_dock_lid.stl` (2 Stk.): Aerodynamische Karosserie-Deckel mit Bügelfalten-Lichtkante & Cardo/Sena-Ausschnitt.
  * `adventure_underseat_cross_rail.stl` (1 Stk.): Verwindungssteife Unter-Sitzbank-Sattelbrücke zur 100 % verdrehsicheren Verbindung von links und rechts mit integrierter M8-Kabelrinne.
  * `adventure_rack_radar_mount.stl` (1 Stk.): Minimaler Heckradar-Halter direkt unter der GS-Gepäckbrücke für Garmin Varia / Wheeltec MR20 auf Peitsche 5.
* **Kit 2: BMW R1250 / R1300 GSA (Adventure mit Ø 18 mm Edelstahl-Alukofferträger):**
  * `adventure_gsa_cage_dock_body.stl` & `adventure_gsa_clamp_cap.stl` (je 2 Stk.): Schwerlast-Käfigdocks ("GSA Cage Dock") für Pod 1 & 2 im $45\,\text{mm}$ Totraum des Trägerrahmens mit $85\,\text{mm}$ Doppel-Rohrsattelbasis, 4x M5 Verschraubung, Steinschlag-Gleitkeil & verdecktem M8-Kanal.
  * `adventure_rack_radar_mount.stl` (1 Stk.): Minimaler Heckradar-Halter unter der Gepäckbrücke.
* **Kit 3: Harley-Davidson Touring & Classic Bagger (Street Glide, Road Glide, Road King):**
  * `saddlebag_lid_dock.stl` (2 Stk.): Kofferdeckel-Montagedocks für Pod 1 & 2 auf den Hartschalenkoffern.
  * `radar_license_plate_bracket.stl` (1 Stk.): Entkoppelter Kennzeichen-Radarhalter für Peitsche 5.
  * `magsafe_cockpit_mount_harley.stl` (1 Stk.), `magsafe_frame_dock.stl` (1 Stk.) & `magsafe_clamp_wings.stl` (1 Stk.): MagSafe Rahmendock-Komponenten.
* **Kit 4: Support-Car / Begleitfahrzeug Kolonnen-Kit (Car-Kit):**
  * `car_sun_visor_pod_clip.stl` (2 Stk.): Schnellwechsel-Spannclips zur vibrationsfreien Befestigung von Pod 1 und Pod 2 an den beiden Sonnenblenden im Pkw/Van (Fahrer- und Beifahrerseite).
  * Dashboard-Dock für SAM-M10Q GNSS-Empfänger hinter der Windschutzscheibe.

---

## 11. Vorkonfektionierte COTS-Kabel & HF-Antennen (Kein Crimpen, kein Löten!)

Für den Aufbau müssen **keine Kabelbäume selbst gecrimpt oder gelötet werden**. Das System verwendet zu 100 % handelsübliche, industriell gefertigte Standard-Kabel (COTS):

```
                       DAS PLUG-AND-PLAY KABELKONZEPT (COTS FERTIGKABEL)
┌─────────────────────────┐
│ HD26 IP67 Fertig-Kabel  │ ──► Fertig umspritzte HD26-Breakout-Kabelpeitsche (Amphenol LTW COTS)
│ (Zentralbox-Hauptanschl)│ ──► Keine Einzeladern konfektionieren, 100 % wasserdicht vergossen
└─┬───────────────────────┘
  ├─► Peitsche 1: M8 6-Pin PUR-Kabel (1.0 m / 1.5 m): Fertiges Standard Sensor-/Aktorkabel ──► Pod 1
  ├─► Peitsche 2: M8 6-Pin PUR-Kabel (1.0 m / 1.5 m): Fertiges Standard Sensor-/Aktorkabel ──► Pod 2
  ├─► Peitsche 4: AMP Superseal 12V-Kabel (1.0 m): Vorkonfektioniertes Batteriekabel mit Sicherung ──► Bordnetz
  └─► Peitsche 5: M8 4-Pin Buchse (250 mm): Heck-Radar (Wheeltec MR20 / Garmin Varia: 12V + UART)
      (Hinweis: Der Front-Node benötigt KEIN Kabel nach hinten – er verbindet sich drahtlos via UWB!)
```

### 11.1 HF-Antennen & Sensoren (COTS)
1. **UWB 6.5 GHz Flex-Antennen (2 Stk.):** **Taoglas FXUWB10** ($11 \times 11 \times 0{,}6\,\text{mm}$) mit 20 mm U.FL Koaxialkabel für Zentralbox und Front-Knoten Unterwannen-Bucht.
2. **LoRa 868 MHz Flex-Antenne (1 Stk.):** **Taoglas FXP895** ($110 \times 20 \times 0{,}8\,\text{mm}$) mit 50 $\Omega$ U.FL Speisung für Zentralbox-Deckeltasche.
3. **Multi-GNSS Modul (1 Stk.):** **u-blox SAM-M10Q** mit integrierter $15 \times 15\,\text{mm}$ Keramik-Patchantenne, Qwiic I2C (`J12`) am Front-Knoten im Fahrtwindkanal.
4. **Umgebungssensoren (Front-Knoten J12 Daisy-Chain):**
   * **TI TMP117:** Hochpräziser Temperatursensor ($\pm 0{,}1\,^\circ\text{C}$) für Glatteis-Frühwarnung.
   * **TI OPT3001:** Umgebungslichtsensor für Display- und Scheinwerfer-Steuerung.

---

## 12. Zukaufteile & Normteile-Einkaufsliste (1 Komplettset)

| Bauteil | Spezifikation / Typ | Bezugsquelle | Menge | Montageort & Funktion |
| :--- | :--- | :--- | :---: | :--- |
| **M3 Edelstahlschrauben** | M3 x 40 mm Zylinderkopf V4A (DIN 912) | Normteil / Amazon | 4 Stk. | Zentralbox-Gehäuse (greift in Nut-Pockets) |
| **M3 Edelstahlschrauben (Front)** | M3 x 20 mm Zylinderkopf V4A (DIN 912) | Normteil / Amazon | 4 Stk. | Front-Node Gehäuse (greift in Nut-Pockets) |
| **M3 Edelstahlmuttern** | DIN 934 / DIN 985 M3 V4A Muttern | Normteil / Amazon | 8 Stk. | Unverlierbar in Nut-Pockets eingelegt (kein Lötkolben nötig!) |
| **M4 Edelstahlmuttern (AMPS)**| DIN 934 M4 V4A Muttern | Normteil / Amazon | 4 Stk. | Unverlierbar in Nut-Pockets der Front-Node Wanne |
| **M2.5 Platinenschrauben** | M2.5 x 6 mm Zylinderkopf V4A (DIN 912) | Normteil | 8 Stk. | 4x Zentralbox-Platine, 4x Front-Node-Platine |
| **M2 Schottwandschrauben** | M2 x 8 mm Senkkopf V4A (DIN 7991) | Normteil | 4 Stk. | Fixierung der 2 Pod-Schottwände (2x pro Pod 1 & 2) |
| **M2 Kassetten-Halteplattenschrauben**| M2 x 6 mm Senkkopf V4A (DIN 7991) | Normteil | 8 Stk. | Fixierung der Aktuator-Niederhalteplatten (4x pro Gateway) |
| **M2 Schwenkachsen Wippe** | M2 x 8 mm Zylinderstift Edelstahl (DIN 7) | Normteil / Misumi | 2 Stk. | Drehachsen für magnetische Kassetten-Rastwippen |
| **Magnetanker (Kassette)** | Ø 6 x 8 mm Zylinderstift gehärtet (DIN 6325) | Normteil / Misumi | 2 Stk. | Stahlanker im Hebelarm der Kassetten-Wippe |
| **Wippen-Rückstellfedern** | Edelstahl V4A ($\varnothing 3{,}5\,\text{mm}, L_0=10\,\text{mm}$) | Gutekunst / Web | 2 Stk. | Rückstellfedern für Kassetten-Rastkralle |
| **Auswerfer-Druckfedern** | Edelstahl V4A ($D=4{,}5\,\text{mm}, L_0=15\,\text{mm}$) | Gutekunst / Web | 4 Stk. | Auto-Eject Federn in den Schottwänden (2x pro Pod) |
| **N52 Entriegelungsschlüssel**| N52 Neodym-Block ($20 \times 10 \times 5\,\text{mm}$) | Supermagnete / Web | 1 Stk. | Magnetschlüssel für Kassettenauswurf |
| **Silentblöcke / Gummipuffer**| Typ A M4 Außen/Innen ($\varnothing 15 \times 10\,\text{mm}$) | Ganter / Normteil | 4 Stk. | Schwingungsentkoppelte Zentralbox-Montage |
| **Silikon-Dichtschnur** | Silikon-Rundschnur $\varnothing 1{,}5\,\text{mm}$ Shore 40A (1.0 m) | O-Ring-Shop | 1 Stk. | $40\,\text{cm}$ Zentralbox-Nut, $30\,\text{cm}$ Front-Node Nut |
| **Kassetten-Flanschdichtungen**| Silikon-Formdichtung Shore 40A ($54 \times 18\,\text{mm}$) | Sonderfertigung | 2 Stk. | Stirnseitige Mundloch-Abdichtung an Pod 1 und Pod 2 |
| **Pufferakku (LiPo USV)** | 1S LiPo Flat-Pack 2.200 mAh ($68 \times 39 \times 5{,}0\,\text{mm}$) mit Molex Micro-Fit | EEMB / Enerpower | 1 Stk. | USV-Pufferung in der Zentralbox (Typ 504068 / 503870) |
| **KFZ-Sicherungshalter** | Wasserdichter Flachsicherungshalter + 2A Sicherung | Hella / MTA | 1 Stk. | Dauerplus-Absicherung an Batteriepol |
| **M8 6-Pin Fertigkabel (PUR)**| M8 6-Pin A-Coded Stecker/Buchse (1.0m / 1.5m) | Binder / Phoenix | 2 Stk. | Plug-and-Play Verbindung zu Pod 1 und Pod 2 |
| **M8 4-Pin Fertigkabel (PUR)**| M8 4-Pin A-Coded Stecker/Buchse (0.5–1.5m) | Binder / Phoenix | Opt. (1)| Peitsche 5: Heck-Radar (Garmin Varia: 12V + UART / Wheeltec MR20) |
| **Front-Node 12V Anschlusskabel**| 2-Pin JST-PH Litzenkabel mit Posi-Tap | COTS Standard | 1 Stk. | Lokale Cockpit-Stromversorgung (Standlicht/Navistecker) – *Funkbrücke via UWB!* |
| **J_ACT Aktuator-Kabelbaum** | Fertiges 8-Pin JST-SH Kabel auf 4x 2-Pin Litzen | Adafruit / SparkFun | 2 Stk. | Vorkonfektioniertes Fertigkabel für 4 Hubmagnete |
| **Miniatur-Aktuatoren** | 5V DC Hubmagnete ($\varnothing 6{,}5 \times 12\,\text{mm}$) mit TPU-Spitze | Solenoid / Web | 8 Stk. | 4 Stk. pro Smart Cartridge (Sena / Cardo) |
| **J2 Gateway-Kabelbaum** | Fertiges 6-Pin JST-SH Kabel auf Klinke / USB | COTS Standard | 2 Stk. | Fertigkabel für Headset-Audio & Dauerstrom |
| **Binder M5 4-Pin IP67 Buchse**| Serie 707 M5 4-Pol Einbaubuchse mit D-Flat | Binder | 1 Stk. | Gehäuse-Flanschanschluss Radar 2.0 Sub-MCU |
| **Wheeltec MR20 77-GHz mmWave**| 77-GHz FMCW Automotive Radar (150m Reichweite)| Wheeltec | Opt. (1)| Radar 2.0 Transceiver-Modul im Heck-Gehäuse |
| **PC Radom-Sichtfenster** | Laserzuschnitt Polycarbonat 1.6 mm (RF-transparent)| COTS / Plexiglas | Opt. (1)| Mikrowellen- & optisches Fenster für MR20 & 24-LED Halo |
| **3M Dual Lock SJ3550** | Pilzkopf-Klettband selbstklebend (VHB-Klebstoff) | 3M | 0.5 m | Rüttelfeste, werkzeuglose Dongle- & Sensor-Montage |
| **car_sun_visor_pod_clip** | 3D-Druck PA12 Federspangen für Sonnenblende | OMB CAD | Opt. (2)| Begleitfahrzeug / Van Montagekit für Pod 1 & 2 |

---

## 13. Minimalistische Werkzeugliste (Das echte IKEA-Prinzip)

Da **weder Löten, noch Crimpen, noch thermisches Einschmelzen von Gewinden** erforderlich ist, schrumpft die Werkzeugliste auf ein absolutes Minimum zusammen, das jeder Motorradfahrer in seinem Standard-Bordwerkzeug besitzt:

| Werkzeug | Größe / Spezifikation | Zweck beim Zusammenbau |
| :--- | :--- | :--- |
| **Innensechskant-Schlüsselsatz**| **1,5 mm / 2,0 mm / 2,5 mm / 3,0 mm** | Verschrauben aller Gehäuse, Platinen und Klemmen |
| **Kreuzschlitz- / Torx-Schlüssel**| **TX10 / PH1** | Gehäusedeckel und Diebstahlsicherungsschraube |
| **Gabelschlüssel / Stecknuss** | **SW 7 mm / SW 8 mm** | Kontern der M4/M5 Muttern bei Schellenmontage |
| **Schere / Cuttermesser** | Standard | Ablängen der Silikon-Dichtschnur |
| **Silikonfett** | Liqui Moly / OKS 1110 (kleine Tube) | Leichtes Einölen der Gehäusedichtungen |

> [!TIP]
> **Es wird keine Lötstation, keine Heißluftpistole, keine Spezial-Crimpzange und kein Einschmelzwerkzeug benötigt.** Alle mechanischen und elektronischen Baugruppen werden ausschließlich gesteckt und geschraubt!

---

## 14. Kostenkalkulation, Bestelltaktik & Skaleneffekt (Solo vs. 2–3 Bikes)

> [!IMPORTANT]
> **Wichtiger Preishinweis zu OEM-Adaptern & Fremdgeräten:**
> Die hier kalkulierten Hardware-Kosten von **ca. 135 € bis 250 €** beziehen sich **ausschließlich auf das OpenMotorBridge-Gesamtsystem** (bestückte PCBAs, 3D-Druckteile, COTS-Kabelbäume, 2.200 mAh Pufferakku, Dichtungen, Normteile).
> Eventuell in die Gateway-Slots eingesetzte kommerzielle Fremd-Intercoms (wie z. B. **Sena SPIDER X Slim**, **Cardo Packtalk Edge**) oder Radargeräte (**Garmin Varia RTL515 / eRTL615**) sind **Zukaufteile des Benutzers** und nicht in den genannten Selbstbau-Kosten enthalten!

### 14.1 Szenario A: Der Solo-Builder (1 Gesamtsystem für 1 Motorrad)
Bestellt ein einzelner Anwender alle Platinen für sich allein:
* JLCPCB liefert 5 Platinen pro Design (davon 2 voll bestückt und 3 unbestückte Ersatzplatinen).
* **Kostenaufstellung Solo-Builder:**
  * JLCPCB PCBAs (PCBA 01, 02 [2x], 03 [2x], 05 bestückt inkl. Versand & Zoll): ca. 135–160 €
  * 3D-Druck (MJF PA12 Dienstleister oder eigenes ASA-Filament): ca. 35–45 €
  * COTS-Kabel, 2.200 mAh LiPo, V4A Normteile & Dichtungen: ca. 35–45 €
  * **Gesamtkosten Solo-System: ca. 205 € bis 250 €**

### 14.2 Szenario B: Community- / Gruppenbestellung (2 bis 3 Motorräder)
Bestellen 2 bis 3 Motorradfahrer gemeinsam:
* Bei JLCPCB werden direkt **alle 5 Platinen voll bestückt** bestellt.
* Die fixen Rüstkosten verteilen sich nun auf 5 voll funktionsfähige Platinensätze.
* **Kostenaufstellung pro Motorrad (bei 3 Bikes):**
  * JLCPCB PCBAs (Anteil pro Bike): ca. 70–80 €
  * 3D-Druck (pro Bike): ca. 30–35 €
  * COTS-Kabel, 2.200 mAh LiPo, Normteile (Mengenrabatt): ca. 30 €
  * **Gesamtkosten pro Motorrad: nur noch ca. 130 € bis 145 €!**

---

## 15. Bauteilverfügbarkeit, Lifecycle-Audit (EOL/NRND) & Second-Source Alternativen

### 15.1 Kritischer Befund: MEMS-Mikrofon (Knowles SPH0645LM4H-B ist EOL)
* **Status:** Das ursprünglich spezifizierte Knowles **SPH0645LM4H-B** wurde vom Hersteller offiziell abgekündigt (**Obsolete / End-of-Life**).
* **Empfohlener Nachfolger / Primärbauteil:** **Sipeed / Zilltek MSM261S4030H0R** (LCSC Part: **`C544577`**).
  * *Vorteile:* Vollständig Standard-I2S-konform (kein DMA-Workaround im ESP-IDF Treiber nötig), exzellente Großserien-Verfügbarkeit bei LCSC, pin- und footprint-kompatibel.

### 15.2 JLCPCB Extended-Parts & Second-Source Alternativen

| Baugruppe / Funktion | Primärbauteil | JLCPCB / LCSC Part | Status / Verfügbarkeit | Empfohlene Second-Source / Drop-In Alternative |
| :--- | :--- | :--- | :--- | :--- |
| **Zentralbox DCDC 12V Buck** | TI LM5164-Q1 | `C2843477` | Active (TI), oft JLCPCB Extended | **TI LMR36015** (60V 1.5A, `C2843480`) oder **XLSEMI XL7005A** (80V) |
| **Front-Node USB-Hub** | Microchip USB2514Bi | `C16251` | Active, Industrie (-40..+85°C) | **Terminus FE1.1s / FE8.1** (JLCPCB Basic Part, Cent-Artikel) |
| **CAN-FD Transceiver (3.3V)** | TI TCAN334GDCNR | `C842340` | Active (TI) | **TI TCAN332G / TCAN337G** oder **SITCORE SIT1051T/3** |
| **Audio-Übertrager (1500V)**| Bourns LM-NP-1001-B1L| `C114402` | Active, oft JLCPCB Extended | **Triad Magnetics SP-66** oder **Bourns SM-LP-5001** |
| **Stereo DSP Codec** | Everest Semi ES8388 | `C365736` | Active (Standard in ESP-ADF) | **Everest Semi ES8311** oder **TI TLV320AIC3104** |

---

## 16. Fertigungs- & Schutzlackierungs-Richtlinien (Conformal Coating IPC-CC-830B)

Um eine 100%ige Langzeitausfallsicherheit nach Automotive-Standard zu gewährleisten, werden alle 7 PCBAs im Serienbestellprozess schutzlackiert:

### 16.1 Lackspezifikation & Qualifikation
* **Standard:** Zertifiziert nach **IPC-CC-830B** und **MIL-I-46058C**.
* **Lacktyp:** **Modifizierter Acryllack (AR)**, z. B. *Peters ELPEGUARD SL 1307 FLZ* (schnell trocknend, fluoreszierend unter UV-Licht zur optischen Qualitätskontrolle).
* **Schichtdicke:** $30\,\mu\text{m}$ bis $60\,\mu\text{m}$ gleichmäßig auf Top- und Bottom-Layer.

### 16.2 Maskierungsvorgaben (Kapton-Tape Schutzmaske)
Folgende Bereiche dürfen **unter keinen Umständen** mit Schutzlack benetzt werden:
1. **Steckverbinder & Kontaktbuchsen:**
   * USB-C Buchsen (`J7` Front-Node, Service-Ports)
   * M8 / M5 Buchsenkontakte (`J2` Pod-Base, Binder M5 Radar)
   * JST-SH / JST-PH Buchsenleisten (`J1..J12` Front-Node, `J1..J2` Kassetten)
   * MicroSD Kartenleser-Slot (`J2` Zentralbox)
2. **Akustische Sensoren & Ventile:**
   * **MEMS-Mikrofon (`MIC1` MSM261S4030H0R auf PCBA 05):** Schalleintrittsöffnung ($\varnothing 0{,}5\,\text{mm}$) muss zwingend mit Kapton versiegelt werden!
   * **Druckausgleichsmembran (Gore ePTFE Vent):** Darf nicht verkleben.
3. **HF-Antennen & Messpunkte:**
   * U.FL Koaxial-Buchsen (`ANT1`, `ANT2`)
   * Testpunkte für In-Circuit-Flash & Oszilloskop-Abgriffe
