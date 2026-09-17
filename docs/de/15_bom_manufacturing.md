# 15 - Stücklisten (BOM), COTS-Kaufteile & SMT-Fertigungsdaten (Alle 7 PCBAs)

Dieses Dokument ist die zentrale Referenz (Single Source of Truth) für die vollständige Bauteilliste (Bill of Materials), die Fertigungsspezifikationen aller 7 Leiterplatten (PCBA 01 bis PCBA 07) bei JLCPCB / Eurocircuits, alle mechanischen 3D-Druck-Komponenten, die COTS-Einkaufslisten sowie eine detaillierte Kosten- und Bestellkalkulation (Solo-Aufbau vs. Sammelbestellung).

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
| **T1, T2** | LM-NP-1001-B1L | Bourns Inc. | SMD Übertrager | C114402 | 1:1 Audio-Übertrager (1500 V RMS galvanische Trennung) |
| **OC1, OC2**| TLP222A(F) | Toshiba | SOP-4 | C112444 | Halbleiter-PhotoMOS-Relais für PTT-Tastensimulation |
| **D1** | SMBJ33CA | Littelfuse | DO-214AA (SMB) | C87848 | TVS-Diode (33 V Standoff, 53.3 V max Clamping) |
| **F1** | MF-MSMF050-2 | Bourns | 1812 SMD | C22668 | Rückstellbare PPTC-Sicherung (500 mA Hold / 1.0 A Trip) |
| **LED1** | WS2812B-B | Worldsemi | 5050 SMD | C114586 | RGB Status-LED für optische Betriebsmodusanzeige |
| **J1** | 2x13 Wannenstecker | Standard 2.54 mm | THT Box Header | C2934175 | Interner Pfostenverbinder zur HD26-Flanschbuchse |
| **J2** | MicroSD Slot Push-Push | Molex / Korean Hro | SMD Push-Push | C266624 | 4-Bit SDIO Speicherkarte für Tour-Logging |
| **J_BAT** | Molex Micro-Fit 3.0 2P | Molex | SMD Header | C289110 | Steckverbindung zum 2.200 mAh LiPo Pufferakku |
| **CN1** | HD26 Buchse IP67 | Amphenol LTW | Flansch D-Sub | Kundenteil | Wasserdichte 26-polige Gehäuseschnittstelle |

---

## 2. PCBA 02: Satelliten Pod Base Carrier (`openmotorbridge_pod_base`, 2-Layer FR4)

| Designator | Bauteil / MPN | Hersteller | Gehäuse | LCSC / JLCPCB Part # | Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **J1** | PinHeader_1x06_P2.54mm_SMD | Harwin / Wurth | SMD Vertikal | C2934176 | 6-Pin Stiftleiste im Schottwand-Schutzkragen |
| **J2** | M8_6PIN_RECEPTACLE (A-Coded)| Binder / Phoenix | M8 Rundsteckverbinder | C289100 | M8 6-Pin IP67 Buchse zur Zuleitung |
| **U1** | SP3012-06UTG | Littelfuse | DFN-14 (3.5x1.35mm)| C2834580 | 6-Kanal Ultra-Low-Cap ESD-Schutzarray (< 0.5 pF) |
| **C1** | 100nF 50V X7R | Samsung / Yageo | 0603 SMD | C14663 | Entkopplungskondensator für 5V Versorgungsspannung |

---

## 3. PCBA 03: Smart Modular Cartridge Rev 2.0 (`openmotorbridge_pod_cartridge`, 2-Layer FR4)

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

## 4. PCBA 04: Heck-Pod 3 Transceiver (`openmotorbridge_rear_pod3`, 4-Layer FR4 TG150)

| Designator | Bauteil / MPN | Hersteller | Gehäuse | LCSC / JLCPCB Part # | Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U10** | RP2040 Dual Cortex-M0+ | Raspberry Pi | QFN-56 | C2040 | Coprozessor für NMEA-Parsing & OMM-LoRa |
| **U11** | NEO-M9N-00B / MAX-M10S | u-blox | LCC-24 / LGA-18 | C3006240 | Multi-Konstellation GNSS Engine (10 Hz, 1-PPS) |
| **U12** | SX1262IMLTRT | Semtech | QFN-24 | C190184 | Secondary Fallback 868 MHz LoRa Transceiver (+22 dBm)|
| **U13** | DS2401Z+ | Maxim / ADI | SOT-23 | C2834570 | 64-Bit 1-Wire Silicon Serial Number ID |
| **U14** | TPS7A0533PDBVR | Texas Instruments | SOT-23-5 | C505293 | Ultra-Low-Noise 3.3V LDO (200 mA) für GNSS & LoRa |
| **ANT1** | GP.1575.25.4.A.02 | Taoglas | 25x25x4 mm Patch | C2689100 | Keramik-Patchantenne für GPS/Galileo/BeiDou |
| **ANT2** | ANT-868-CW-HWR-SMA | Linx / Taoglas | Wendelantenne | C290111 | 868 MHz Wendelantenne für Heckbürzel-LoRa |
| **J3, J4, J5**| MM8030-2610RJ3 | Murata Electronics | SMD 2.0x2.0 mm | C2834595 | Automatische HF-Umschaltbuchsen für externe Antennen (2.4G, 868M, GNSS) |

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
| **J12** | JST-SH 4-Pin Header | JST | 1.00mm SMD | `C289118` | Qwiic / STEMMA QT I2C Sensorport (3.3V, GND, SDA, SCL) |

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

## 8. 1-Click Bestellleitfaden für JLCPCB (Alle Leiterplatten fertig bestückt)

Alle Fertigungsdaten liegen im Repository unter `hardware/pcba/` als fertige ZIP- und CSV-Pakete vor:

| Baugruppe / PCBA | Gerber-ZIP Datei | BOM CSV Datei | CPL (Pick & Place) CSV | Lagen | Fertigungs-Hinweis |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **PCBA 01: Zentralbox** | `01_main_box_pcba_gerbers_jlcpcb.zip` | `01_main_box_pcba_bom_jlcpcb.csv` | `01_main_box_pcba_cpl_jlcpcb.csv` | **4 Lagen** | ENIG (Gold), 1.6 mm, TG150, SMT beidseitig |
| **PCBA 02: Pod-Basis** | `02_pod_base_pcba_gerbers_jlcpcb.zip` | `02_pod_base_pcba_bom_jlcpcb.csv` | `02_pod_base_pcba_cpl_jlcpcb.csv` | **2 Lagen** | ENIG (Gold), 1.6 mm, SMT Top |
| **PCBA 03: Kassetten-Träger**| `03_pod_cartridge_pcba_gerbers_jlcpcb.zip` | `03_pod_cartridge_pcba_bom_jlcpcb.csv` | `03_pod_cartridge_pcba_cpl_jlcpcb.csv` | **2 Lagen** | ENIG (Gold), 1.2 mm, SMT Top |
| **PCBA 04: Heck-Pod 3** | `04_rear_pod3_pcba_gerbers_jlcpcb.zip` | `04_rear_pod3_pcba_bom_jlcpcb.csv` | `04_rear_pod3_pcba_cpl_jlcpcb.csv` | **4 Lagen** | ENIG (Gold), 1.6 mm, TG150, SMT Top |
| **PCBA 05: Front-Knoten** | `05_front_node_pcba_gerbers_jlcpcb.zip` | `05_front_node_pcba_bom_jlcpcb.csv` | `05_front_node_pcba_cpl_jlcpcb.csv` | **4 Lagen** | ENIG (Gold), 1.6 mm, TG150, SMT beidseitig |
| **PCBA 06: MagSafe Dock** | `06_magsafe_dock_pcba_gerbers_jlcpcb.zip` | `06_magsafe_dock_pcba_bom_jlcpcb.csv` | `06_magsafe_dock_pcba_cpl_jlcpcb.csv` | **2 Lagen** | ENIG (Gold), 1.6 mm, SMT Top |
| **PCBA 07: Smart-Keyfob** | `07_smart_keyfob_pcba_gerbers_jlcpcb.zip` | `07_smart_keyfob_pcba_bom_jlcpcb.csv` | `07_smart_keyfob_pcba_cpl_jlcpcb.csv` | **2 Lagen** | ENIG (Gold), 1.0 mm, SMT beidseitig |

---

## 9. Mechanik- & Gehäuse-BOM (3D-Druck MJF PA12 & Normteile)

Alle Gehäuseteile sind konsequent für das **IKEA-Prinzip** konstruiert: **Kein Einschmelzen von Gewindeeinsätzen mit dem Lötkolben erforderlich!** Die Gehäuse verfügen über integrierte Sechskant-Mutternaschen (Nut Pockets für Standard DIN 934 / DIN 985 Edelstahlmuttern) bzw. präzise Kernlöcher für gewindefurchende Kunststoffschrauben.

### 9.1 Basis-System (Universal für jedes Motorrad)
| Baugruppe | STL-Dateiname | Stück | Material & Fertigung | Funktion & Beschreibung |
| :--- | :--- | :---: | :--- | :--- |
| **Main Box Unterteil** | [`main_box_lower_case.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lower_case.stl) | **1** | MJF PA12 / ASA | Monocoque-Unterwanne mit 4x M4 Silentblock-Ohren, Mutternaschen & Dichtnut |
| **Main Box Zwischenboden** | [`main_box_mid_tray.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_mid_tray.stl) | **1** | MJF PA12 / ASA | Akku-Wanne für 2.200 mAh Flat-LiPo ($68 \times 39 \times 5{,}0\,\text{mm}$), 11x Konvektionsschlitze & Dichtfeder |
| **Main Box Deckel** | [`main_box_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lid.stl) | **1** | MJF PA12 / ASA | Gehäusedeckel mit Gore ePTFE-Ventilsitz & Schraubensenkungen |
| **Pod-Basisgehäuse** | [`pod_base_housing.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod_base_housing.stl) | **3** | MJF PA12 / ASA | Universal-Schachtgehäuse für Pod 1 (Links), Pod 2 (Rechts) und Heck-Pod 3 |
| **Pod-Schottwände** | [`03_pod_bulkhead_partition.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl) | **3** | MJF PA12 / ASA | Schottwand mit Dichtkragen & Federaufnahmen (1x pro Pod) |
| **Kassetten-Basisschlitten**| [`cartridge_base_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl) | **3** | MJF PA12 / ASA | Universalschlitten für Gateway 1 (Pod 1), Gateway 2 (Pod 2) und OMM (Pod 3) |
| **Kassetten-Riegel / Wippe**| [`cartridge_magnetic_lock_latch.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_magnetic_lock_latch.stl) | **2** | MJF PA12 / ASA | Magnetische Diebstahlschutz-Rastwippen für Kassetten-Slots 1 & 2 |
| **Heck-Pod 3 OMM-Radom** | [`cartridge_antenna_bracket_omm.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_antenna_bracket_omm.stl) | **1** | MJF PA12 / ASA | Dielektrisches Antennenradom & Trägerbrücke für PCBA 04 im Heck-Pod 3 |
| **Front-Knoten Unterwanne** | [`front_node_lower_tub.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_lower_tub.stl) | **1** | MJF PA12 / ASA | Cockpit-Wanne mit AMPS-Bohrbild (DIN 934 M4 Taschen), Rohrbett & Mutternaschen |
| **Front-Knoten Deckel** | [`front_node_upper_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_upper_lid.stl) | **1** | MJF PA12 / ASA | Deckel mit Knowles MEMS Schalleintritt & O-Ring-Dichtnut |
| **Front-Knoten Dichtkämme** | [`front_node_cable_glands_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_cable_glands_tpu.stl) | **1 Paar**| TPU 95A / 85A | Elastische Dichtkämme für Front-USB & Signale |
| **Front-Knoten USB-C Kappe**| [`front_node_usbc_cap_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_usbc_cap_tpu.stl) | **1** | TPU 95A / 85A | Elastische Staubschutzkappe mit Haltekollier für Service-Port |

### 9.2 Gateway-Kassetten-Inlays (Passend zur gewünschten Intercom-Ausstattung)
> **Hinweis zur Architektur:** Slot 1 und Slot 2 sind **Multi-Protokoll Gateway-Transceiver**, keine Fahrer/Beifahrer-Kopfhörer! Sie verbinden das Motorrad gleichzeitig mit Sena Mesh und Cardo DMC. Fahrer und Sozius funken drahtlos mit ihren normalen Helmen.

| Baugruppe | STL-Dateiname | Stück | Material | Funktion & Beschreibung |
| :--- | :--- | :---: | :--- | :--- |
| **Gateway-Inlay Sena** | [`cartridge_insert_sena.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) | *Opt. (1)* | MJF PA12 / ASA | Formschlüssiges Inlay für Sena SPIDER X Slim / 50S / 60S (Mesh 3.0 Wave) |
| **Gateway-Inlay Cardo** | [`cartridge_insert_cardo.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl) | *Opt. (1)* | MJF PA12 / ASA | Inlay für Cardo Packtalk Edge / Pro (DMC Gen2) mit Air-Mount |
| **Blindkassette / Dry Box** | [`cartridge_insert_blindkassette.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_blindkassette.stl) | *Opt. (1)* | MJF PA12 / ASA | Hermetischer Schutzschlitten für ungenutzten Slot oder regendichte Dry Box |

### 9.3 Fahrzeugspezifische Montage-Kits (3D-Druckteile)
* **Kit 1: BMW R1250 / R1300 GS (Standard / Vario-Koffer):**
  * `adventure_transition_dock.stl` (2 Stk.): Kofferunabhängige Docks für die Sitzbank-Bügelfalte (Ø 28 mm Rahmenrohr).
  * `adventure_rack_tail_mount.stl` (1 Stk.): Heckbrücken-Ausleger für Pod 3 & Radar.
  * `radar_varia_gopro_lock_dock.stl` (1 Stk.) & `011_gopro_hirth_lock.stl` (1 Stk.): Radar-Bajonett-Dock mit Hirth-Verzahnung.
* **Kit 2: BMW R1250 / R1300 GSA (Adventure mit Ø 18 mm Edelstahl-Alukofferträger):**
  * `adventure_pannier_rack_clamp_base.stl` & `adventure_pannier_rack_clamp_cap.stl` (je 4 Stk.): Schwerlast-Klemmschellen-Paare für Pod 1 & 2 im Kofferträger-Rahmendreieck.
  * `adventure_rack_tail_mount.stl` (1 Stk.): Heck-Balkon hinter Alutopcase mit 45°-Astabweiser für Dipolantenne.
  * `radar_varia_gopro_lock_dock.stl` (1 Stk.) & `011_gopro_hirth_lock.stl` (1 Stk.): Radar-Dock mit Hirth-Verzahnung.
* **Kit 3: Harley-Davidson Touring & Classic Bagger (Street Glide, Road Glide, Road King):**
  * `saddlebag_lid_dock.stl` (2 Stk.): Kofferdeckel-Montagedocks für Pod 1 & 2 auf den Hartschalenkoffern.
  * `pod3_touring_fender_console.stl` (1 Stk.): Organische Heckkotflügel-Konsole für Pod 3 *(für Non-Tour-Pak Bagger; bei Ultra Limited / Road Glide Limited mit werkseitigem King Tour-Pak entfällt die Fender-Konsole wegen des Stahlrohr-Trägerrahmens zugunsten einer Rohr-Klemmschellenmontage am Tour-Pak-Träger!)*.
  * `radar_license_plate_bracket.stl` (1 Stk.): Entkoppelter Kennzeichen-Radarhalter.
  * `magsafe_cockpit_mount_harley.stl` (1 Stk.), `magsafe_frame_dock.stl` (1 Stk.) & `magsafe_clamp_wings.stl` (1 Stk.): MagSafe Rahmendock-Komponenten.
* **Kit 4: Harley-Davidson CVO ST & Performance Bagger (Road Glide ST):**
  * `saddlebag_lid_dock.stl` (2 Stk.): Kofferdeckel-Montagedocks für Pod 1 & 2 auf den Hartschalenkoffern.
  * `cvo_st_undercowl_skeleton_dock.stl` (1 Stk.): Aufrechtes bionisches Skeleton-Dock für Pod 3 unter der Forged-Carbon-Hutze (vollständiger Freigang zu Showa-Ausgleichsbehältern & Auspuffhitze).
  * `cvo_st_telemetry_fin.stl` (1 Stk.): Aerodynamische Haifischflosse / Telemetrie-Finne auf der Hecklasche.
  * `radar_license_plate_bracket.stl` (1 Stk.): Entkoppelter Kennzeichen-Radarhalter *(CVO ST verfügt serienmäßig über das mittige Kennzeichen wie alle Touring-Modelle!)*.
* **Kit 5: Custom-Bikes, Bobber & Universal:**
  * `radar_center_underfender_mount.stl` (1 Stk.): Zentrische Unter-Kotflügel-Platte für Heck-Radar *(speziell für Custom-Bikes & Umbauten mit seitlichem Kennzeichenhalter!)*.
  * Standard 120°-V-Nut am Pod-Basisgehäuse für Rahmenrohre (Ø 22–32 mm) mit EPDM-Spannringen oder M4 Silentblöcken.

### 9.4 Zubehör (Optional)
| Baugruppe | STL-Dateiname | Stück | Material | Funktion & Beschreibung |
| :--- | :--- | :---: | :--- | :--- |
| **Smart-Keyfob Unterschale**| [`smart_keyfob_lower_shell.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/smart_keyfob_lower_shell.stl) | **1** | MJF PA12 / ASA | Wanne mit LRA-Dämpfungsbett und Magnetaufnahme für PCBA 07 |
| **Smart-Keyfob Oberschale** | [`smart_keyfob_upper_shell.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/smart_keyfob_upper_shell.stl) | **1** | MJF PA12 / ASA | Deckel mit 3 Tastenfeldern & Lichtleiter |
| **Smart-Keyfob Bumper** | [`smart_keyfob_tpu_rim.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/smart_keyfob_tpu_rim.stl) | **1** | TPU 85A / 95A | Elastischer Stoßschutz-Umlaufring |
| **MagSafe Rahmendock** | [`magsafe_frame_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/magsafe_frame_dock.stl) | **1** | MJF PA12 / ASA | Cockpit-Dockkörper mit M2.5 & M3 Mutternaschen für PCBA 06 |
| **MagSafe Klemmflügel** | [`magsafe_clamp_wings.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/magsafe_clamp_wings.stl) | **1** | MJF PA12 / ASA | Klemmflügel zur Rohrbefestigung am Lenker |

### 9.5 OrcaSlicer 3MF Projekt-Platten (Standard vs. Kompakt Bauraum)
Für Selbstdrucker stehen vorkonfigurierte `.3mf`-Projektdateien für **OrcaSlicer** (voll kompatibel mit Bambu Studio und PrusaSlicer) bereit. Alle Platten sind mit **6 Wandlinien** (für 100 %ige Wasserdichtigkeit ohne Infiltration), 40 % Gyroid-Infill und optimierter Nahtplatzierung in verdeckten Radien vorkonfiguriert:

#### Profil A: Standard & Großes Druckbett (≥ 220×220 mm bis 300×300 mm)
*Geeignet für: Bambu Lab X1C / P1S / P1P / A1 (256×256 mm), Prusa MK3/MK4 (250×210 mm), Creality K1 / Ender-3, Voron 2.4 / Trident (250–350 mm).*
| Platte | Projekt-Dateiname | Material | Enthaltene Bauteile |
| :---: | :--- | :---: | :--- |
| **Platte 1** | `main_box_standard_plate.3mf` | ASA / PA-CF | Komplette Zentralbox auf 1 Platte: Unterwanne, Zwischenboden & Deckel |
| **Platte 2** | `pods_standard_plate.3mf` | ASA / PA-CF | Alle 3 Pod-Gehäuse (Pod 1, 2 & Heck-Pod 3) + 3x Schottwände |
| **Platte 3** | `cartridges_frontnode_standard_plate.3mf`| ASA / PA-CF | 3x Basisschlitten, Gateway-Inlays, Verriegelungen & Front-Node Gehäuse |
| **Platte 4** | `glands_tpu_standard_plate.3mf` | TPU 95A | Alle flexiblen Dichtkämme, USB-C Staubkappe & Dichtschnüre |
| **Platte 5** | `bike_mounts_standard_plate.3mf` | ASA / PA-CF | Fahrzeugspezifisches Kit (BMW Rohrschellen bzw. Harley Docks) |

#### Profil B: Kompaktes Druckbett (180×180 mm)
*Geeignet für: Bambu Lab A1 Mini (180×180×180 mm), Prusa Mini+ (180×180×180 mm).*
| Platte | Projekt-Dateiname | Material | Enthaltene Bauteile |
| :---: | :--- | :---: | :--- |
| **Platte 1** | `main_box_tub_mini_plate.3mf` | ASA / PA-CF | Main Box Unterwanne (diagonal 45° im Bauraum platziert) |
| **Platte 2** | `main_box_lid_tray_mini_plate.3mf` | ASA / PA-CF | Main Box Zwischenboden & Gehäusedeckel |
| **Platte 3** | `pod_1_2_mini_plate.3mf` | ASA / PA-CF | Pod 1 & Pod 2 Basisgehäuse (aufrecht stehend) |
| **Platte 4** | `pod_3_bulkheads_mini_plate.3mf` | ASA / PA-CF | Heck-Pod 3 Gehäuse & 3x Schottwände |
| **Platte 5** | `cartridges_mini_plate.3mf` | ASA / PA-CF | 3x Kassetten-Basisschlitten, Inlays & Verriegelungswippen |
| **Platte 6** | `front_node_mini_plate.3mf` | ASA / PA-CF | Universal Front-Knoten Unterwanne & Deckel |
| **Platte 7** | `glands_tpu_mini_plate.3mf` | TPU 95A | TPU-Dichtkämme, USB-C Schutzkappe & Dichtungen |
| **Platte 8** | `bike_mounts_mini_plate.3mf` | ASA / PA-CF | Fahrzeugspezifische Docks / Schellen |

---

## 10. Vorkonfektionierte COTS-Kabel & Pufferakku (Kein Crimpen, kein Löten!)

Für den Aufbau müssen **keine Kabelbäume selbst gecrimpt oder gelötet werden**. Das System verwendet zu 100 % handelsübliche, industriell gefertigte Standard-Kabel (COTS):

```
                       DAS PLUG-AND-PLAY KABELKONZEPT (COTS FERTIGKABEL)
┌─────────────────────────┐
│ HD26 IP67 Fertig-Kabel  │ ──► Fertig umspritzte HD26-Breakout-Kabelpeitsche (Amphenol LTW COTS)
│ (Zentralbox-Hauptanschl)│ ──► Keine Einzeladern konfektionieren, 100 % wasserdicht vergossen
└─┬───────────────────────┘
  ├─► M8 6-Pin PUR-Kabel (1.0 m / 1.5 m): Fertiges Standard Sensor-/Aktorkabel ──► Pod 1 (Gateway 1)
  ├─► M8 6-Pin PUR-Kabel (1.0 m / 1.5 m): Fertiges Standard Sensor-/Aktorkabel ──► Pod 2 (Gateway 2)
  ├─► M8 6-Pin PUR-Kabel (1.5 m / 2.0 m): Fertiges Standard Sensor-/Aktorkabel ──► Pod 3 (Heck-Transceiver)
  ├─► AMP Superseal 12V-Kabel (1.0 m): Vorkonfektioniertes Batteriekabel mit Sicherung ──► 12V Bordnetz
  └─► M8 4-Pin Buchse (Peitsche 5, 250 mm): Heck-Radar (Garmin Varia: 12V + UART) / Heck-OBD2
      (Hinweis: Der Front-Node benötigt KEIN Kabel nach hinten – er verbindet sich drahtlos via ESP-NOW!)
```

---

## 11. Zukaufteile & Normteile-Einkaufsliste (1 Komplettset)

| Bauteil | Spezifikation / Typ | Bezugsquelle | Menge | Montageort & Funktion |
| :--- | :--- | :--- | :---: | :--- |
| **M3 Edelstahlschrauben** | M3 x 40 mm Zylinderkopf V4A (DIN 912) | Normteil / Amazon | 4 Stk. | Zentralbox-Gehäuse (greift in Nut-Pockets) |
| **M3 Edelstahlschrauben (Front)** | M3 x 20 mm Zylinderkopf V4A (DIN 912) | Normteil / Amazon | 4 Stk. | Front-Node Gehäuse (greift in Nut-Pockets) |
| **M3 Edelstahlmuttern** | DIN 934 / DIN 985 M3 V4A Muttern | Normteil / Amazon | 8 Stk. | Unverlierbar in Nut-Pockets eingelegt (kein Lötkolben nötig!) |
| **M4 Edelstahlmuttern (AMPS)**| DIN 934 M4 V4A Muttern | Normteil / Amazon | 4 Stk. | Unverlierbar in Nut-Pockets der Front-Node Wanne |
| **M2.5 Platinenschrauben** | M2.5 x 6 mm Zylinderkopf V4A (DIN 912) | Normteil | 8 Stk. | 4x Zentralbox-Platine, 4x Front-Node-Platine |
| **M2 Schottwandschrauben** | M2 x 8 mm Senkkopf V4A (DIN 7991) | Normteil | 6 Stk. | Fixierung der 3 Pod-Schottwände (2x pro Pod) |
| **M2 Kassetten-Halteplattenschrauben**| M2 x 6 mm Senkkopf V4A (DIN 7991) | Normteil | 8 Stk. | Fixierung der Aktuator-Niederhalteplatten (4x pro Gateway) |
| **M2 Schwenkachsen Wippe** | M2 x 8 mm Zylinderstift Edelstahl (DIN 7) | Normteil / Misumi | 2 Stk. | Drehachsen für magnetische Kassetten-Rastwippen |
| **Magnetanker (Kassette)** | Ø 6 x 8 mm Zylinderstift gehärtet (DIN 6325) | Normteil / Misumi | 2 Stk. | Stahlanker im Hebelarm der Kassetten-Wippe |
| **Wippen-Rückstellfedern** | Edelstahl V4A ($\varnothing 3{,}5\,\text{mm}, L_0=10\,\text{mm}$) | Gutekunst / Web | 2 Stk. | Rückstellfedern für Kassetten-Rastkralle |
| **Auswerfer-Druckfedern** | Edelstahl V4A ($D=4{,}5\,\text{mm}, L_0=15\,\text{mm}$) | Gutekunst / Web | 6 Stk. | Auto-Eject Federn in den Schottwänden (2x pro Pod) |
| **N52 Entriegelungsschlüssel**| N52 Neodym-Block ($20 \times 10 \times 5\,\text{mm}$) | Supermagnete / Web | 1 Stk. | Magnetschlüssel für Kassettenauswurf |
| **Silentblöcke / Gummipuffer**| Typ A M4 Außen/Innen ($\varnothing 15 \times 10\,\text{mm}$) | Ganter / Normteil | 4 Stk. | Schwingungsentkoppelte Zentralbox-Montage |
| **Silikon-Dichtschnur** | Silikon-Rundschnur $\varnothing 1{,}5\,\text{mm}$ Shore 40A (1.0 m) | O-Ring-Shop | 1 Stk. | $40\,\text{cm}$ Zentralbox-Nut, $30\,\text{cm}$ Front-Node Nut |
| **Kassetten-Flanschdichtungen**| Silikon-Formdichtung Shore 40A ($54 \times 18\,\text{mm}$) | Sonderfertigung | 3 Stk. | Stirnseitige Mundloch-Abdichtung an Pod 1, 2 und 3 |
| **Pufferakku (LiPo USV)** | 1S LiPo Flat-Pack 2.200 mAh ($68 \times 39 \times 5{,}0\,\text{mm}$) mit Molex Micro-Fit | EEMB / Enerpower | 1 Stk. | USV-Pufferung in der Zentralbox (Typ 504068 / 503870) |
| **KFZ-Sicherungshalter** | Wasserdichter Flachsicherungshalter + 2A Sicherung | Hella / MTA | 1 Stk. | Dauerplus-Absicherung an Batteriepol |
| **M8 6-Pin Fertigkabel (PUR)**| M8 6-Pin A-Coded Stecker/Buchse (1.0m / 1.5m) | Binder / Phoenix | 3 Stk. | Plug-and-Play Verbindung zu Pod 1, 2 und 3 |
| **M8 4-Pin Fertigkabel (PUR)**| M8 4-Pin A-Coded Stecker/Buchse (0.5–1.5m) | Binder / Phoenix | Opt. (1)| Peitsche 5: Heck-Radar (Garmin Varia: 12V + UART) / Heck-OBD2 (nur bei Radar-Nutzung) |
| **Front-Node 12V Anschlusskabel**| 2-Pin JST-PH Litzenkabel mit Posi-Tap | COTS Standard | 1 Stk. | Lokale Cockpit-Stromversorgung (Standlicht/Navistecker) – *Funkbrücke via ESP-NOW / BLE!* |
| **J_ACT Aktuator-Kabelbaum** | Fertiges 8-Pin JST-SH Kabel auf 4x 2-Pin Litzen | Adafruit / SparkFun | 1–2 Stk.| Vorkonfektioniertes Fertigkabel für 4 Hubmagnete |
| **Miniatur-Aktuatoren** | 5V DC Hubmagnete ($\varnothing 6{,}5 \times 12\,\text{mm}$) mit TPU-Spitze | Solenoid / Web | 4–8 Stk.| 4 Stk. pro Smart Cartridge (Sena / Cardo) |
| **J2 Gateway-Kabelbaum** | Fertiges 6-Pin JST-SH Kabel auf Klinke / USB | COTS Standard | 1–2 Stk.| Fertigkabel für Headset-Audio & Dauerstrom |

---

## 12. Minimalistische Werkzeugliste (Das echte IKEA-Prinzip)

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

## 13. Kostenkalkulation, Bestelltaktik & Skaleneffekt (Solo vs. 2–3 Bikes)

> [!IMPORTANT]
> **Wichtiger Preishinweis zu OEM-Adaptern & Fremdgeräten:**
> Die hier kalkulierten Hardware-Kosten von **ca. 135 € bis 260 €** beziehen sich **ausschließlich auf das OpenMotorBridge-Gesamtsystem** (bestückte PCBAs, 3D-Druckteile, COTS-Kabelbäume, 2.200 mAh Pufferakku, Dichtungen, Normteile).
> Eventuell in die Gateway-Slots eingesetzte kommerzielle Fremd-Intercoms (wie z. B. **Sena SPIDER X Slim**, **Cardo Packtalk Edge**) oder Radargeräte (**Garmin Varia RTL515 / eRTL615**) sind **Zukaufteile des Benutzers** und nicht in den genannten Selbstbau-Kosten enthalten!

### 13.1 Warum schwanken die Kosten zwischen ~135 € und ~260 €?
Bei Fertigungsdienstleistern wie JLCPCB oder PCBWay entstehen die Stückkosten primär durch **fixe Rüst- und Einrichtungskosten** pro Platinen-Design:
1. **Mindestbestellmenge (MOQ):** JLCPCB fertigt bei Leiterplatten immer mindestens **5 Stück** pro Design.
2. **SMT-Rüstpauschale:** Für jedes PCBA-Design fällt eine feste Einrichtungsgebühr für Schablone (Stencil), Feeder-Rüstung und Pick-and-Place-Programmierung an (ca. 15–25 $ pro Platinentyp, in Summe über alle Boards ca. 110–130 $).
3. **SMT-Bestückungsanzahl:** Standardmäßig lässt man bei JLCPCB entweder 2 Stück (Minimum) oder direkt alle 5 Stück bestücken.

### 13.2 Szenario A: Der Solo-Builder (1 Gesamtsystem für 1 Motorrad)
Bestellt ein einzelner Anwender alle Platinen für sich allein:
* JLCPCB liefert 5 Platinen pro Design (davon 2 voll bestückt und 3 unbestückte Ersatzplatinen).
* Die gesamten SMT-Rüstkosten (ca. 110 €) lasten voll auf diesem einen fertigen System.
* **Kostenaufstellung Solo-Builder:**
  * JLCPCB PCBAs (PCBA 01 bis 05 bestückt inkl. Versand & Zoll): ca. 140–165 €
  * 3D-Druck (MJF PA12 Dienstleister oder eigenes ASA-Filament): ca. 35–50 €
  * COTS-Kabel, 2.200 mAh LiPo, V4A Normteile & Dichtungen: ca. 35–45 €
  * **Gesamtkosten Solo-System: ca. 210 € bis 260 €**

### 13.3 Szenario B: Community- / Gruppenbestellung (2 bis 3 Motorräder)
Bestellen 2 bis 3 Motorradfahrer gemeinsam (oder ein Fahrer stattet Erst- und Zweitbike aus):
* Bei JLCPCB werden direkt **alle 5 Platinen voll bestückt** bestellt.
* Die fixen Rüstkosten (110 €) verteilen sich nun auf 5 voll funktionsfähige Platinensätze.
* Die Bauteilpreise sinken durch höhere Abnahmemengen (Staffelpreise bei LCSC).
* **Kostenaufstellung pro Motorrad (bei 3 Bikes):**
  * JLCPCB PCBAs (Anteil pro Bike): ca. 75–85 €
  * 3D-Druck (pro Bike): ca. 30–40 €
  * COTS-Kabel, 2.200 mAh LiPo, Normteile (Mengenrabatt): ca. 30 €
  * **Gesamtkosten pro Motorrad: nur noch ca. 135 € bis 155 €!**

*(Alle Preisangaben Stand 2026, Richtwerte inkl. MwSt., zzgl. optionaler OEM-Intercom-Module).*

---

## 14. Bauteilverfügbarkeit, Lifecycle-Audit (EOL/NRND) & Second-Source Alternativen

Um böse Überraschungen bei der Bauteilbeschaffung und automatisierten Bestückung bei JLCPCB/LCSC zu vermeiden, wurde die gesamte Stückliste einem Lifecycle- und Verfügbarkeits-Audit unterzogen:

### 14.1 Kritischer Befund: MEMS-Mikrofon (Knowles SPH0645LM4H-B ist EOL)
* **Status:** Das ursprünglich spezifizierte Knowles **SPH0645LM4H-B** wurde vom Hersteller offiziell abgekündigt (**Obsolete / End-of-Life**) und ist bei Distributoren als Auslaufmodell klassifiziert. Zudem wies der Chip ein unkonventionelles I2S-Timing (1-Bit Offset) auf.
* **Empfohlener Nachfolger / Primärbauteil:** **Sipeed / Zilltek MSM261S4030H0R** (LCSC Part: **`C544577`**).
  * *Vorteile:* Vollständig Standard-I2S-konform (kein DMA-Workaround im ESP-IDF Treiber nötig), exzellente Großserien-Verfügbarkeit bei LCSC, pin- und footprint-kompatibel.
  * *Zweit-Alternativen:* **TDK InvenSense ICS-43434 / ICS-43432** oder **Knowles SPK0641HT4H-1**.

### 14.2 JLCPCB Extended-Parts & Second-Source Alternativen

| Baugruppe / Funktion | Primärbauteil | JLCPCB / LCSC Part | Status / Verfügbarkeit | Empfohlene Second-Source / Drop-In Alternative |
| :--- | :--- | :--- | :--- | :--- |
| **Zentralbox DCDC 12V Buck** | TI LM5164-Q1 | `C2843477` | Active (TI), oft JLCPCB Extended | **TI LMR36015** (60V 1.5A, `C2843480`) oder **XLSEMI XL7005A** (80V, JLCPCB Basic Part!) |
| **Front-Node USB-Hub** | Microchip USB2514Bi | `C16251` | Active, Industrie (-40..+85°C) | **Terminus FE1.1s / FE8.1** (JLCPCB Basic Part, Cent-Artikel, riesige Lagerbestände) |
| **CAN-FD Transceiver (3.3V)** | TI TCAN334GDCNR | `C842340` | Active (TI) | **TI TCAN332G / TCAN337G** oder **SITCORE SIT1051T/3** (pin-kompatibel, riesige LCSC-Bestände) |
| **Audio-Übertrager (1500V)**| Bourns LM-NP-1001-B1L| `C114402` | Active, oft JLCPCB Extended | **Triad Magnetics SP-66** oder **Bourns SM-LP-5001** |
| **Stereo DSP Codec** | Everest Semi ES8388 | `C365736` | Active (Standard in ESP-ADF) | **Everest Semi ES8311** (modernere Low-Power Variante) oder **TI TLV320AIC3104** |

### 14.3 Langzeit-gesicherte Schlüsselkomponenten (Liefergarantie bis mindestens 2034)
* **Espressif ESP32-S3-WROOM-1 / 1U:** Espressif garantiert eine Mindestverfügbarkeit von 10 Jahren (mindestens bis 2034).
* **Raspberry Pi RP2040:** Extreme Millionen-Verfügbarkeit (~0,70 €). *Hinweis zum neuen RP2350:* Der im Herbst 2024 erschienene RP2350 ist software- und hardwareseitig noch in der frühen Einführungsphase (bekannter Hardware-Errata E9 am Pull-Down-Pin) – der bewährte RP2040 ist für OpenMotorBridge die stabilere und günstigere Wahl.
* **Semtech SX1262 LoRa:** Aktueller Standard-Transceiver für 868 MHz (+22 dBm) in OpenMotorMesh / Meshtastic.
* **Bosch Sensortec BMI270:** Moderne 6-Achsen-IMU (hat den veralteten/abgekündigten BMI160 abgelöst).
* **WCH CH32V003F4P6:** 32-Bit RISC-V Kassettentreiber, Cent-Artikel mit gigantischen LCSC-Lagerbeständen.
* **Nordic nRF52840:** Marktführer für BLE 5.4 und Thread/Zigbee mit garantierter Langzeitfertigung.

