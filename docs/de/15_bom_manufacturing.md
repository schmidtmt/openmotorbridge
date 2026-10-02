# 15 - Stücklisten (BOM), COTS-Kaufteile & SMT-Fertigungsdaten (Das bereinigte PCBA-Lineup v9.6)

Dieses Dokument ist die zentrale Referenz (Single Source of Truth) für die vollständige Bauteilliste (Bill of Materials), die Fertigungsspezifikationen aller Leiterplatten (`PCBA 01`, `03`, `05`, `07`, `08` sowie optionales Passiv-Dock `06`) bei JLCPCB / Eurocircuits (`PCBA 02` und `PCBA 04` sind durch die All-UWB-Architektur ersatzlos entfallen), alle mechanischen 3D-Druck-Komponenten (MJF PA12), die COTS-Einkaufslisten sowie eine detaillierte Kosten- und Bestellkalkulation (Solo-Aufbau vs. Sammelbestellung).

> [!NOTE]
> **v9.6 Stücklisten-Harmonisierung & Konsolidierung:**  
> Alle Bauteile, LCSC-Teilenummern und Steckverbinder wurden mit den finalen Schaltplänen und Layouts in [Spezifikation 07 (PCBA Hardware & Pinouts)](07_pcba_hardware_pinouts.md) abgeglichen. Die frühere Pod-Bodenplatine `PCBA 02` und das Lenker-Interface `PCBA 04` sind vollständig entfallen. Kassetten (`PCBA 03`) arbeiten 100 % drahtlos über Qorvo DW3110 UWB und werden über direkte 2-Draht-DC-Bodenfederkontakte versorgt. Die mechanischen Kassetten-Inlays unterstützen das standardisierte 4-Klassen-Portfolio inklusive UCS (Universal Communication Solution) und OMM 2.4 GHz.

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
| **SW1** | TS-1187A-C-A-B | C&K / Omron | SMD Taster | C318884 | Hardware Pairing- & Reset-Taster (3s Pair, 10s Purge) |
| **D1** | SMBJ33CA | Littelfuse | DO-214AA (SMB) | C87848 | TVS-Diode (33 V Standoff, 53.3 V max Clamping) |
| **F1** | MF-MSMF050-2 | Bourns | 1812 SMD | C22668 | Rückstellbare PPTC-Sicherung (500 mA Hold / 1.0 A Trip) |
| **LED1** | WS2812B-B | Worldsemi | 5050 SMD | C114586 | RGB Status-LED für optische Betriebsmodusanzeige |
| **J1** | DTM13-12PA Header | TE Connectivity | Automotive 12P | Kundenteil | Automotive Deutsch DTM-12 Schnittstelle (11 Pins aktiv) |
| **J2** | MicroSD Slot Push-Push | Molex / Korean Hro | SMD Push-Push | C266624 | 4-Bit SDIO Speicherkarte für Tour-Logging |
| **J_BAT** | Molex Micro-Fit 3.0 2P | Molex | SMD Header | C289110 | Steckverbindung zum 2.200 mAh LiPo Pufferakku |
| **ANT1** | U.FL-R-SMT-1 | Hirose / Murata | SMD HF | C2834595 | LoRa 868 MHz U.FL Buchse zu Taoglas FXP895 im Deckel |
| **ANT2** | U.FL-R-SMT-1 | Hirose / Murata | SMD HF (B.Cu) | C2834595 | UWB 6.5 GHz U.FL Buchse zu Taoglas FXUWB10 im Boden |

*(Hinweis: Durch den Wechsel auf All-UWB entfallen die früheren Audio-Übertrager T1, T2 und Optokoppler OC1, OC2 ersatzlos).*

---

## 2. Satelliten Pod-Gehäuse (Entfall von PCBA 02)
> **Architektur-Hinweis (v8.5 / v9.0):**  
> Die frühere Pod-Bodenplatine `PCBA 02` ist **vollständig und ersatzlos entfallen**.  
> Das Pod-Gehäuse (`pod_base_housing.stl`) ist ein monolithisches 3D-Druckteil ohne interne Platine. Die 2-adrige Gleichstrompeitsche (+5V und GND) führt von hinten direkt in das Gehäuse und endet an zwei vergoldeten Federkontakten (Keystone / Mill-Max), die formschlüssig auf die Stirnflächen-Pads von `PCBA 03` greifen.

---

## 3. PCBA 03: Universal Smart Cartridge Rev 3.0 (`openmotorbridge_pod_cartridge`, 2-Layer FR4 TG150, 2-seitig SMT)
> **Hinweis zur Stückzahl:** Die Kassette ist universell und wird **2x pro Motorrad** verbaut (Bucht 1 links, Bucht 2 rechts).

| Designator | Bauteil / MPN | Hersteller | Gehäuse | LCSC / JLCPCB Part # | Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | DW3110 | Qorvo | QFN-16 (Top) | C2934600 | IEEE 802.15.4z UWB Transceiver (6.5 GHz Ch. 5 All-UWB Link) |
| **U2** | CH32V203 / MCU | WCH | QFN-20 (Top) | C2943200 | 32-Bit Host-MCU (SPI zu DW3110, NVS Multi-Vehicle Roaming) |
| **Q1 - Q4**| AO3400A | Alpha & Omega | SOT-23 (Bottom)| C20917 | 4x N-Kanal MOSFETs ($30\,\text{V} / 5{,}7\,\text{A}$) für Mechatronik |
| **D1 - D4**| 1N4148WS | Diodes Inc. | SOD-323 (Bottom)| C2128 | 4x Freilaufdioden für Hubmagnete |
| **F1** | MF-MSMF050-2 | Bourns | 1812 SMD | C22668 | PPTC 500mA Schutzsicherung |
| **J_ACT** | SM08B-SRSS-TB | JST | 8-Pin 1.0mm SMD | C160404 | Mechatronik-Header für 4 Hubmagnete |
| **ANT1** | U.FL-R-SMT-1 | Hirose | SMD Micro-Coax | C2834595 | UWB-Antennenport (Taoglas FXUWB10 oder SMD-Patch) |
| **U3 (DNP)**| ES8311 | Everest Semi | QFN-20 (3x3mm) | C396781 | Optional: Mono Audio-Codec (nur bestückt für Midland PMR446) |

---

## 4. Baugruppe PCBA 04 (Heck-Pod 3): Ersatzlos entfallen (Clean Architecture v8.0)

> [!NOTE]
> **Architektur-Bereinigung v8.0:** Die Leiterplatte `PCBA 04` und das dritte Satellitengehäuse (Heck-Pod 3) wurden **vollständig und ersatzlos gestrichen**:
> 1. **LoRa 868 MHz (SX1262):** Sitzt nun direkt auf der Zentralbox (`PCBA 01`), gepuffert durch den USV-Akku (24/7 Diebstahl-Sentry).
> 2. **Multi-GNSS (SAM-M10Q):** Sitzt im kühlen Fahrtwindbereich am Front-Knoten (`PCBA 05`), angebunden über Qwiic I2C (`J12`).
> 3. **Fahrzeug-Backbone:** Erfolgt drahtlos über Ultra-Wideband (Qorvo DW3110 / 6.5 GHz Ch. 5, $< 0{,}4\,\text{ms}$ Latenz) zwischen Front-Knoten und Zentralbox.
> 4. **Heck-Radar:** Schließt direkt über Peitsche 3 des Deutsch DTM-12 Kabelbaums an die Zentralbox an (2-Draht 12V DC); Telemetrie läuft 100 % drahtlos via UWB.

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

## 6. PCBA 06: MagSafe Rahmendock-Adapter (`openmotorbridge_magsafe_dock`, 2-Layer FR4, 28 x 11.5 mm) [Optional / Legacy]

> [!NOTE]
> **Status:** In der aktuellen **All-UWB v9.6 Architektur** entfällt PCBA 06 im regulären Betrieb, da die Koffer-Trennstelle als reines 2-Draht DC-System ausgeführt wird und direkt über einen industriellen 2-Pin Magnet-Pogo-Steckverbinder (COTS) verbunden wird. Diese BOM dient als Referenz für Legacy-Aufbauten mit starrer Rahmenverschraubung.

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

## 8. PCBA 08: Radar 2.0 Sub-MCU & 36-LED Flügel-Träger (`openmotorbridge_radar_submcu`, 2-Lagen FR4 TG150, 115 x 65 mm)

| Ref | Bauteil / Typ | Gehäuse | Spezifikation & Funktion | LCSC Part |
| :--- | :--- | :--- | :--- | :--- |
| **`U1`** | ESP32-C5-WROOM-1-N8 | SMD Modul | 32-Bit RISC-V Dual-Band Sub-MCU (2.4 GHz + 5.9 GHz V2X, 4MB Flash) | `C2843550` |
| **`U2`** | LDO 3.3V 500mA | SOT-23-5 | TI TLV75533P / Richtek RT9013 LDO Spannungsregler | `C505293` |
| **`U3`** | Qorvo DW3110 | QFN-16 | Ultra-Wideband (UWB) Transceiver (6.5 GHz Ch. 5, All-UWB Backbone) | `C2934500` |
| **`Y1_UWB`**| 38.4 MHz Crystal | SMD 2016-4P | Präzisionsquarz für DW3110 UWB Transceiver | `C384351` |
| **`D1..36`**| WS2812B-2020 | SMD 2020 | 36x Digital RGB-LEDs in Doppel-Warnflügeln (18 links, 18 rechts) | `C2843530` |
| **`J1`** | JST-JWPF 2-Pin | THT/SMD 2.0mm | Wasserdichter 12V DC Kfz-Bordnetzeingang (`B02B-JWPF-SK-R`) | `C2843555` |
| **`J2`** | JST-SH 1.0mm 4-Pin | SMD Liegend | UART-Verbindung zum Wheeltec MR20 Transceiver (RX/TX/5V/GND) | `C136657` |
| **`J3`** | Hirose U.FL | SMT Vertical | 5.9 GHz V2X HF-Antennenanschluss | `C14894` |
| **`J4`** | Hirose U.FL | SMT Vertical | 6.5 GHz UWB HF-Antennenanschluss (Taoglas FXUWB10 Flexantenne) | `C14894` |
| **`SW1..2`**| Alps SKRK SMD | SMD 3.9x2.9mm | Lokale Boot- und Reset-Taster | `C115358` |

---

## 9. 1-Click Bestellleitfaden für JLCPCB (Alle 6 Leiterplatten fertig bestückt)

Alle Fertigungsdaten liegen im Repository unter `hardware/production_packages/` als fertige ZIP- und CSV-Pakete vor:

| Baugruppe / PCBA | Gerber-ZIP Datei | BOM CSV Datei | CPL (Pick & Place) CSV | Lagen | Fertigungs-Hinweis |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **PCBA 01: Zentralbox** | `01_main_box_pcba_gerbers_jlcpcb.zip` | `01_main_box_pcba_bom_jlcpcb.csv` | `01_main_box_pcba_cpl_jlcpcb.csv` | **4 Lagen** | ENIG (Gold), 1.6 mm, TG150, SMT beidseitig (DW3110 auf B.Cu) |
| **PCBA 03: Universal-Kassette**| `03_pod_cartridge_pcba_gerbers_jlcpcb.zip` | `03_pod_cartridge_pcba_bom_jlcpcb.csv` | `03_pod_cartridge_pcba_cpl_jlcpcb.csv` | **2 Lagen** | ENIG (Gold), 1.2 mm, SMT beidseitig (2x pro Fahrzeug bestellen) |
| **PCBA 05: Front-Knoten** | `05_front_node_pcba_gerbers_jlcpcb.zip` | `05_front_node_pcba_bom_jlcpcb.csv` | `05_front_node_pcba_cpl_jlcpcb.csv` | **4 Lagen** | ENIG (Gold), 1.6 mm, TG150, SMT beidseitig (DW3110 auf B.Cu) |
| **PCBA 06: MagSafe Dock** | `06_magsafe_dock_pcba_gerbers_jlcpcb.zip` | `06_magsafe_dock_pcba_bom_jlcpcb.csv` | `06_magsafe_dock_pcba_cpl_jlcpcb.csv` | **2 Lagen** | *Optional / Legacy* (bei All-UWB durch COTS 2-Pin Magnetkupplung ersetzt) |
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
| **Pod-Basisgehäuse** | [`pod_base_housing.stl`](../../hardware/cad/stl/02_pod_base/pod_base_housing.stl) | **2** | MJF PA12 / ASA | Monolithisches 1-Teil-Schachtgehäuse mit integrierter Schottwand, Kontaktführungen & Federdomen |
| **Pod-Schottwand (integriert)** | [`03_pod_bulkhead_partition.stl`](../../hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl) | *(integr.)* | MJF PA12 / ASA | Zu 100 % nahtlos im Monocoque integriert (0 lose Teile, 0 Montageschrauben) |
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
  * `adventure_transition_dock_base.stl` (2 Stk.): Kofferunabhängige Basis-Wannen für die Sitzbank-Bügelfalte (Ø 28 mm Rahmenrohr) mit 4x Spanngurt-Freisparungen und 2-Draht DC-Kabelführung.
  * `adventure_transition_dock_lid.stl` (2 Stk.): Aerodynamische Karosserie-Deckel mit Bügelfalten-Lichtkante & Cardo/Sena-Ausschnitt.
  * `adventure_underseat_cross_rail.stl` (1 Stk.): Verwindungssteife Unter-Sitzbank-Sattelbrücke zur 100 % verdrehsicheren Verbindung von links und rechts mit integrierter 2-Draht DC-Kabelrinne.
  * `adventure_rack_radar_mount.stl` & `adventure_rack_radar_clamp_cap.stl` (je 1 Stk.): Minimaler, schottergeschützter Heckradar-Rohrträger unter der Gepäckbrücke (Ø 18 mm Rohr) mit M5-Verschraubung von unten und integriertem Steinschlag-Spoiler.
  * `radar_swivel_tilt_cradle.stl` (1 Stk.): Schwerlast-Neigegelenk (Actioncam/GoPro-Hirth-Cradle) mit 2x M4-Verschraubung ins Radar 2.0 Gehäuse.
* **Kit 2: BMW R1250 / R1300 GSA (Adventure mit Ø 18 mm Edelstahl-Alukofferträger):**
  * `adventure_gsa_cage_dock_body.stl` & `adventure_gsa_clamp_cap.stl` (je 2 Stk.): Schwerlast-Käfigdocks ("GSA Cage Dock") für Pod 1 & 2 im $45\,\text{mm}$ Totraum des Trägerrahmens mit $85\,\text{mm}$ Doppel-Rohrsattelbasis, 4x M5 Verschraubung, 4x Spanngurt-Freisparungen, Steinschlag-Gleitkeil & verdecktem 2-Draht DC-Kanal mit Kabelbinderbrücke im Rohrschatten.
  * `adventure_rack_radar_mount.stl` & `adventure_rack_radar_clamp_cap.stl` (je 1 Stk.): Schottergeschützter Heckradar-Rohrträger unter der Gepäckbrücke.
  * `radar_swivel_tilt_cradle.stl` (1 Stk.): Schwerlast-Neigegelenk mit 2x M4-Verschraubung.
* **Kit 3: Harley-Davidson Touring & Classic Bagger (Street Glide, Road Glide, Road King):**
  * `saddlebag_lid_dock.stl` (2 Stk.): Kofferdeckel-Docks mit Scharnier-Torx-Flansch, 4x Spanngurt-Freisparungen & 2-Draht DC-Zugentlastungsschnauze.
  * `010_saddlebag_hole_grommet_split.stl` (2 Stk.): Geteilte EPDM/TPU-Durchführung für Ø 3,6 mm 2-Draht DC-Kabel in Ø 12 mm Wandbohrung (oberhalb Schwingenlager).
  * `radar_license_plate_bracket.stl` (1 Stk.): Entkoppelter Kennzeichen-Radarhalter für Peitsche 3.
  * `radar_swivel_tilt_cradle.stl` (1 Stk.): Radar 2.0 Schwerlast-Neigegelenk (Actioncam/GoPro-Hirth-Cradle) mit 2x M4-Verschraubung und 36-Zahn Hirth-Verzahnung.
  * `radar_mr20_housing.stl` & `radar_mr20_radome.stl` (1 Stk.): Radar 2.0 PA12 Flügel-Gehäuse mit Spritzwasser-Schutzspoiler und PC-Radom.
  * `009_magsafe_frame_dock.stl` (1 Stk.), `009_magsafe_frame_lid.stl` (1 Stk.) & `009_magsafe_frame_clamp.stl` (1 Stk.): MagSafe Rahmendock-Komponenten (optional). Sowie `road_glide_inductive_cam_dock.stl` (1 Stk.): Induktives Cam-Docking für Sharknose-Verkleidungen.
* **Optionale Bobber & Custom-Kit Teile:**
  * `radar_center_underfender_mount.stl` (1 Stk.): Stealth Center Under-Fender Mount mit $46\,\text{mm}$ Tiefgang und integriertem $42\,\text{mm}$ Spritzwasser-Schmutzfänger-Spoiler.
  * `radar_swivel_tilt_cradle.stl` (1 Stk.): Schwerlast-Neigegelenk mit 2x M4-Verschraubung.
* **Kit 4: Support-Car / Begleitfahrzeug Kolonnen-Kit (Car-Kit):**
  * `car_sun_visor_pod3_clip.stl` (2 Stk.): Schnellwechsel-Spannclips zur vibrationsfreien Befestigung von Pod 1 und Pod 2 an den beiden Sonnenblenden im Pkw/Van (Fahrer- und Beifahrerseite).
  * `car_dashboard_wedge_dock.stl` (1 Stk.): Zweistufige Armaturenbrett-Doppelaufnahme (Dual-Stack Dock) zur formschlüssigen, vibrationsgedämpften Aufnahme von Front-Knoten (unten, freie GNSS-Sicht) und Zentralbox (oben, 15° geneigt).

---

## 11. Vorkonfektionierte COTS-Kabel & HF-Antennen (Kein Crimpen, kein Löten!)

Für den Aufbau müssen **keine Kabelbäume selbst gecrimpt oder gelötet werden**. Das System verwendet zu 100 % handelsübliche, industriell gefertigte Standard-Kabel (COTS):

### 11.1 Der Hauptkabelbaum am Motorrad (Deutsch DTM-12 COTS-Fertigkabelbaum)

```
                       DAS PLUG-AND-PLAY KABELKONZEPT (COTS FERTIGKABEL)
+-------------------------+
| Deutsch DTM-12 Fertig-  | --> Vorkonfektionierter IP68/IP69K Deutsch DTM-12 Hauptkabelbaum
| Kabelbaum (Zentralbox)  | --> Industriell gefertigt, Raychem DR-25 Schrumpfschlauch
+-+-----------------------+
  +-> Peitsche 1: 2-Draht FLRY-B (1.0 m / 1.5 m): Reine DC-Power (+12V geschaltet / GND) --> Pod 1 (Bucht 1)
  +-> Peitsche 2: 2-Draht FLRY-B (1.0 m / 1.5 m): Reine DC-Power (+12V geschaltet / GND) --> Pod 2 (Bucht 2)
  +-> Peitsche 3: 2-Draht FLRY-B (0.5 m): Heck-Radar PCBA 08 (+12V geschaltet / GND)
  +-> Peitsche 4: AMP Superseal 1.5 6-Pin / FLRY-B (1.0 m): Bordnetz & CAN (KL30, KL15, GND, CAN-H, CAN-L, CHASSIS_EARTH)
      (Hinweis: Sämtliche Interconnects & Telemetriedaten laufen zu 100 % drahtlos via UWB!)
```

### 11.2 Das 12V Werkstatt- & Begleitfahrzeug-Y-Adapterkabel ("Bench & Support-Car Harness")

Für Laborprüfungen (Tisch-Inbetriebnahme ohne Motorrad-Kabelbaum) sowie den mobilen Einsatz im Begleitfahrzeug (Support-Van, Mietwagen, Pkw-Rennleitung) wird das universelle **12V-Y-Adapterkabel** eingesetzt. Es versorgt Front-Node und Zentralbox parallel aus einer beliebigen 12V-DC-Quelle.

**Architektur-Vorteil:** Der USB-C Port der Zentralbox bleibt hardwareseitig komplett frei für die kabelgebundene Verbindung zur Infotainment-Head-Unit des Autos (Apple CarPlay / Android Auto Audio- und Display-Mirroring) oder zum Laptop (WebSerial Flashing):

| Komponente / Baugruppe | Spezifikation / Herstellernummer | Bezugsquelle / P/N | Menge | Funktion |
| :--- | :--- | :--- | :---: | :--- |
| **12V DC Einspeisestecker** | Kfz-Zigarettenanzünderstecker mit 5A Feinsicherung ($5 \times 20\,\text{mm}$) & LED *oder* 4mm Labor-Bananenstecker | COTS Standard | 1 Stk. | Anschluss an Zigarettenanzünder-Buchse oder Labornetzteil |
| **Stammkabel** | FLRY-B $2 \times 0{,}75\,\text{mm}^2$ (AWG18), Länge $1{,}0\,\text{m}$ (Rot: +12V, Schwarz: GND) | Fahrzeugleitung | 1 m | Zuleitung bis zum Y-Verteilerpunkt |
| **Abzweig A (Front-Node)** | JST JWPF 2-Pin Buchse `02R-JWPF-VSLE-S` mit Kontakten `SWPR-001T-P025` | JST / Mouser | 1 Stk. | Pin 1: +12V (Rot, KL15), Pin 2: GND (Schwarz), Leitung $1{,}5\,\text{m}$ ($2 \times 0{,}5\,\text{mm}^2$) |
| **Abzweig B (Zentralbox)** | Deutsch DTM 12-Pin Buchsengehäuse `DTM-06-12S`, Sperrkeil `WM-12S`, Buchsen `0462-201-20141` | TE Connectivity / Mouser | 1 Stk. | Pin 1: KL30 (+12V), Pin 2: KL15 (+12V gebrückt), Pin 3: GND (Schwarz), Leitung $0{,}5\,\text{m}$ ($2 \times 0{,}75\,\text{mm}^2$) |
| **Blindstopfen (DTM-12)** | Dichtstopfen Größe 20 `0413-204-2005` (Weiß/Rot) | TE Connectivity | 9 Stk. | IP68-Versiegelung der ungenutzten Kammern 4–12 |
| **Opt. Abzweig C (Radar)** | JST JWPF 2-Pin Buchse `02R-JWPF-VSLE-S` mit Kontakten `SWPR-001T-P025` | JST / Mouser | Opt. (1)| Pin 1: +12V, Pin 2: GND, Leitung $0{,}5\,\text{m}$ ($2 \times 0{,}35\,\text{mm}^2$) für Radar-Benchtest |
| **Schrumpfschlauch / Y-Splice**| Raychem ATUM 4:1 mit Innenkleber oder Schrumpfformteil | TE Connectivity | 1 Stk. | Wasserdichte, zugentlastete Kapselung der Y-Verzweigung |

### 11.3 HF-Antennen & Sensoren (COTS)
1. **UWB 6.5 GHz Flex-Antennen (2 Stk.):** **Taoglas FXUWB10** ($11 \times 11 \times 0{,}6\,\text{mm}$) mit 20 mm U.FL Koaxialkabel für Zentralbox und Front-Knoten Unterwannen-Bucht.
2. **LoRa 868 MHz Flex-Antenne (1 Stk.):** **Taoglas FXP895** ($110 \times 20 \times 0{,}8\,\text{mm}$) mit 50 $\Omega$ U.FL Speisung für Zentralbox-Deckeltasche.
3. **Multi-GNSS Modul (1 Stk.):** **u-blox SAM-M10Q** mit integrierter $15 \times 15\,\text{mm}$ Keramik-Patchantenne, Qwiic I2C (`J12`) am Front-Knoten im Fahrtwindkanal.
4. **Umgebungssensoren (Front-Knoten J12 Daisy-Chain):**
   * **TI TMP117:** Hochpräziser Temperatursensor ($\pm 0{,}1\,^\circ\text{C}$) für Glatteis-Frühwarnung.
### 11.4 Internes COTS-Kabelset & Pigtails für Front-Node & Peripherie

Für alle internen Verbindungen innerhalb der Gehäuse (vom Platinen-Header zur Gehäuseflanke oder zum Nachbarmodul) kommen **ausschließlich industriell vorkonfektionierte COTS-Pigtails (Plug & Play)** zum Einsatz. Es muss kein einziger Steckkontakt von Hand gecrimpt werden:

| Funktion / Baugruppe | Header auf Platine | Steckertyp & Raster | Gegenstück / Gehäuseauslass | Länge | Bezugsquelle / Typ |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **Smartphone PD 20W** | Front-Node `J5` | JST-PH 5-Pin (2.0 mm) | Wasserdichte Panel-Mount USB-C Buchse (IP67 mit Schraubkappe) am Lenker | 20 cm | COTS USB-C Panel-Mount Pigtail |
| **Glovebox PD 20W + MP3**| Front-Node `J5_MP3` | JST-PH 5-Pin (2.0 mm) | Wasserdichte Panel-Mount USB-C Buchse (IP67) für Handschuhfach / Tankrucksack | 30 cm | COTS USB-C Panel-Mount Pigtail |
| **CP2AA Wireless Dongle** | Front-Node `J6` | JST-PH 4-Pin (2.0 mm) | USB-A Buchse zur internen Aufnahme von Ottocast / Carlinkit Adapter | 15 cm | COTS JST-PH 4P auf USB-A Buchse |
| **Cockpit Aux USB** | Front-Node `J6_AUX` | JST-PH 4-Pin (2.0 mm) | USB-A Buchse oder Panel-Mount für Dashcam / Display / Zūmo | 20 cm | COTS JST-PH 4P auf USB-A Buchse |
| **OEM Upstream Host** | Front-Node `J4` | JST-PH 4-Pin (2.0 mm) | USB-A Stecker oder Litzen für Harley Skyline OS / Boom! Box GTS | 30 cm | COTS JST-PH 4P auf USB-A Stecker |
| **Cockpit 12V Speisung** | Front-Node `J1` | JST-PH 2-Pin (2.0 mm) | Offene Litzen (0.5 mm²) mit Posi-Tap / Cartool-Stecker (KL15 Standlicht) | 50 cm | COTS JST-PH 2P Pigtail |
| **Cockpit CAN-Bus** | Front-Node `J2` | JST-PH 3-Pin (2.0 mm) | Offene Litzen mit Posi-Tap für CAN_H / CAN_L / GND im Cockpit | 50 cm | COTS JST-PH 3P Pigtail |
| **Lenkertaster / PTT** | Front-Node `J3` | JST-PH 4-Pin (2.0 mm) | 4-adriges Steuerkabel zur Lenkerarmatur (PTT Funk, Cam-Bookmark, Menü) | 100 cm | COTS JST-PH 4P Pigtail |
| **Action-Cam Power 5V** | Front-Node `J8` | JST-PH 2-Pin (2.0 mm) | Rechtwinkliger USB-C Stecker für Helm- oder Verkleidungs-GoPro | 60 cm | COTS JST-PH 2P auf USB-C Stecker |
| **Spiegel-Warn-LEDs (BSD)**| Front-Node `J9` | JST-PH 3-Pin (2.0 mm) | Y-Kabel ($2 \times 2$-Pin) zu bernsteinfarbenen LED-Pads in beiden Rückspiegeln | 120 cm | COTS JST-PH 3P Y-Pigtail |
| **Qi Wireless Pad 12V** | Front-Node `J10` | JST-PH 2-Pin (2.0 mm) | 2-Pin Stecker für SP Connect / Quad Lock Wireless Charging Head | 25 cm | COTS JST-PH 2P Pigtail |
| **Aux-Licht Schaltausgang**| Front-Node `J11` | JST-PH 2-Pin (2.0 mm) | 2-Pin Litzen zum Relais für Zusatzscheinwerfer / Stroboskop | 30 cm | COTS JST-PH 2P Pigtail |
| **Qwiic / GNSS I2C Bus** | Front-Node `J12` | JST-SH 4-Pin (1.0 mm) | 4-Pin JST-SH Stecker zu u-blox SAM-M10Q & TMP117 / OPT3001 | 50-100 mm | SparkFun Qwiic / Adafruit STEMMA QT |
| **MR20 Radar-Interconnect**| Radar PCBA 08 `J2` | JST-SH 4-Pin (1.0 mm) | 4-Pin JST-SH Stecker direkt in das Wheeltec MR20 Sensormodul | 40-50 mm | COTS JST-SH 4P zu JST-SH 4P |
| **Zentralbox CarPlay Port**| Zentralbox `J3` | IDC 10-Pin (2.54 mm) | Wasserdichte Panel-Mount USB-C Buchse (IP67) an der Gehäuseflanke | 15 cm | COTS IDC-10 auf USB-C Panel-Mount |
| **USV LiPo-Akku Anschluss**| Zentralbox `J5` | JST-PH 4-Pin / Molex | Anschlusskabel mit NTC-Sensor des 2.200 mAh LiPo Flat-Packs | 8 cm | Am LiPo-Pouch konfektioniert |

### 11.5 Die Gateway-Adapterkabel für OEM-Intercoms (Header `J_AUDIO_PWR` / `J2`)

Um handelsübliche OEM-Intercom-Module vollkommen zerstörungsfrei und ohne Garantieverlust im Kassetten-Einschub zu betreiben, wird der 6-polige **JST-SH 1.0 mm Header `J_AUDIO_PWR`** auf `PCBA 03` über modellspezifische COTS-Adapterkabelstränge angeschlossen:

| Headset-Modell / Klasse | Adapterkabel-Typ & Anschlüsse | Belegung am 6-Pin JST-SH Header | Länge | Funktion & Besonderheiten |
| :--- | :--- | :--- | :---: | :--- |
| **Sena SPIDER X Slim**<br>*(OMB-Referenz K2a)* | **6-Pin JST-SH auf 3-fach Pigtail:**<br>- 2-Pin Micro-JST (Direct-DC)<br>- 2.5 mm Klinkenbuchse (Mic In)<br>- 3.5 mm Klinkenbuchse (Spk Out) | **Pin 1:** `GND`<br>**Pin 2:** `VCC_HEADSET` ($3{,}85\,\text{V}$ Festspannung)<br>**Pin 3:** `AUDIO_R+`<br>**Pin 4:** `AUDIO_R-`<br>**Pin 5:** `MIC_IN+`<br>**Pin 6:** `RESERVE_IO` (N/C) | 8 cm | **Zero Pogo-Pins:** Direkte 3.85V Speisung ab Werk ohne LiPo-Akku im Pod (keine Brandgefahr, kein Verschleiß). Mikrofon und Lautsprecher werden direkt mit dem ES8388 Codec gekoppelt. |
| **Cardo Packtalk Edge / Pro**<br>*(Klasse 4 DMC Gen2)* | **6-Pin JST-SH auf Klinke, Micro-2Pin & USB-C:**<br>- 3.5 mm Stereo-Klinkenstecker (Spk Out)<br>- Cardo 2-Pin Micro-Stecker mit Rastnase (Mic In)<br>- Rechtwinkliger USB-C Stecker (5V Ladeport) | **Pin 1:** `GND`<br>**Pin 2:** `VCC_5V` (Lade- & Dauerstrom)<br>**Pin 3:** `AUDIO_R+` (Audio Spk+)<br>**Pin 4:** `AUDIO_R-` (Audio Spk-)<br>**Pin 5:** `MIC_IN+` (Mikrofonsignal)<br>**Pin 6:** `RESERVE_IO` (N/C) | 10 cm | Koppelt die werkseitige Air-Mount Halterung. Lautsprecherausgang über 3.5 mm Klinke, Mikrofoneingang über Cardo-spezifischen 2-Pin Micro-Stecker mit Rastnase (z. B. Pigtail aus Original-Kabelmikrofon), Dauerladung während aktivem Mesh-Betrieb über USB-C. |
| **Midland G9 Pro / PMR446**<br>*(Klasse 7 Analogfunk)* | **6-Pin JST-SH auf Midland-Doppelklinke:**<br>- 3.5 mm Lautsprecher-Klinke<br>- 2.5 mm Mikrofon/PTT-Klinke<br>- DC-Batteriedummy | **Pin 1:** `GND`<br>**Pin 2:** `VCC_5V` (Batteriedummy Speisung)<br>**Pin 3:** `AUDIO_R+`<br>**Pin 4:** `AUDIO_R-`<br>**Pin 5:** `MIC_IN+`<br>**Pin 6:** `OPTO_PTT` (PTT gegen GND geschaltet) | 10 cm | Schaltet den analogen Sender tastend via MOSFET `Q4` / Optokoppler durch und speist das Funkgerät aus dem Bordnetz. |
| **OpenMotorMesh (OMM) 2.4 GHz**<br>*(Klasse C Native UCS)* | **6-Pin JST-SH auf USB-C (90° abgewinkelt):**<br>- 6-Pin JST-SH 1.0mm Buchse<br>- Rechtwinkliger USB-C Stecker | **Pin 1:** `GND`<br>**Pin 2:** `VCC_5V`<br>**Pin 3-5:** Digital Audio / I2S<br>**Pin 6:** Config / UART | 5 cm | Verbindet PCBA 03 direkt mit dem IP67 USB-C Port des OMM-Moduls. Vollverschleißfreie digitale Speisung & Steuerung. Im Helmbetrieb wird derselbe USB-C Port für das Helm-Pigtail (3.5 mm Spk + 2-Pin Mic) genutzt. |

### 11.6 Der Mechatronik-Aktuatorkabelbaum & mechanische Befestigung (Header `J_ACT`)

Jede Universal Smart Cartridge (`PCBA 03`) steuert bis zu vier mechanische Druck-Aktuatoren ("mechanische Finger") an, die die Tasten des jeweiligen OEM-Headsets betätigen:

1. **Vorkonfektionierter 8-Pin Splitter-Kabelbaum:**
   * **Stecker:** JST-SH 8-Pin Buchse ($1{,}0\,\text{mm}$ Raster, vergoldete Kontakte).
   * **Leitung:** 8 hochflexible AWG30 Silikonlitzen (Länge $60\,\text{mm}$), aufgeteilt in vier verdrillte 2-Ader-Paare:
     * **Paar 1 (Taste + / Menü vor):** Pin 1 (`VCC_5V`) + Pin 3 (`ACT1_OUT`, geschaltet gegen GND via AO3400A MOSFET `Q1`).
     * **Paar 2 (Taste - / Menü zurück):** Pin 1 (`VCC_5V`) + Pin 4 (`ACT2_OUT`, geschaltet via `Q2`).
     * **Paar 3 (Taste Center / Phone):** Pin 2 (`VCC_5V`) + Pin 5 (`ACT3_OUT`, geschaltet via `Q3`).
     * **Paar 4 (Taste Mesh / Pairing):** Pin 2 (`VCC_5V`) + Pin 6 (`ACT4_OUT`, geschaltet via `Q4`).
2. **Die Miniatur-Hubmagnete:**
   * 4x 5V DC Miniatur-Solenoide ($\varnothing 6{,}5 \times 12\,\text{mm}$, Hub $1{,}5\dots 2{,}0\,\text{mm}$, Schaltkraft $> 0{,}3\,\text{N}$, Spulenwiderstand ca. $25\,\Omega$, Stromaufnahme kurzzeitig ca. $200\,\text{mA}$ bei $50\,\text{ms}$ Puls).
   * Auf jedem Magnetstößel sitzt eine elastische, dämpfende **TPU-Tastspitze (`actuator_silicone_tip.stl`)**, die Tastenverschleiß und Knackgeräusche eliminiert.
3. **Mechanische Niederhalte-Befestigung:**
   * Die 4 Hubmagnete werden formschlüssig von oben in die Führungsbrücke des Inlays (`cartridge_insert_sena.stl` bzw. `cartridge_insert_cardo.stl`) eingesteckt.
   * Darüber wird die **Aktuator-Niederhalteplatte (`cartridge_retainer_plate.stl`)** gelegt und mit **4x M2 x 6 mm Senkkopf-Edelstahlschrauben (DIN 7991)** vibrationsfest verschraubt. Kein Kleben, kein Wackeln, jederzeit demontierbar.

### 11.7 Die Koffer-Trennstelle (Industrieller 2-Pin Magnet-Pogo "MagSafe-Ersatz") & Befestigung

Anstelle der früheren proprietären Platine `PCBA 06` wird die werkzeuglose Koffer-Trennstelle als **reines 2-Draht-DC-System (5V / GND)** mit einer industriellen **2-Pin Magnet-Pogo-Abreißkupplung (IP68 COTS)** realisiert:

```
                  DIE 2-PIN MAGNET-POGO KOFFER-TRENNSTELLE (IP68 COTS)
  +--------------------+                                    +--------------------+
  | FAHRZEUGRAHMEN     |                                    | SEITENKOFFER       |
  | (Unter der Sitzbank|                                    | (Pannier / Vario)  |
  |  am Rohr Ø 26 mm)  |                                    |                    |
  | [009_magsafe_      |     Magnetische Abreißtrennung     | [010_saddlebag_    |
  |  frame_dock.stl]   |     (10 - 15 N axiale Haltekraft)  |  grommet_split.stl]|
  |   +--------------+ |             (Klack!)               | +----------------+ |
  |   | 2-Pin Magnet-| | <================================> | | 2-Pin Magnet-  | |
  |   | Pogo BUCHSE  | |                                    | | Pogo STECKER   | |
  |   +-------+------+ |                                    | +-------+--------+ |
  +-----------|--------+                                    +---------|----------+
              | 2x 0.5 mm² PUR                                        | 2x 0.34 mm² Flachband
              v                                                       v (am Deckel-Fangband)
        [Zentralbox J1]                                       [Kofferdeckel-Dock Pod]
```

1. **Die Magnetkupplung (COTS):**
   * Industrieller 2-Pin Magnet-Pogo-Steckverbinder (Typ **HytePro M411 / COTS 2-Pol Magnetanschluss**, IP68 wasserdicht mit vergoldeten Pogo-Pins und N52-Neodym-Ringmagneten).
   * Elektrische Parameter: Bis zu $2{,}5\,\text{A}$ Dauerstrom bei $12\,\text{V}/5\,\text{V}$ DC; Übergangswiderstand $< 30\,\text{m}\Omega$.
   * **Mechanische Schutzfunktion ("Mechaniker-Sicherheit"):** Trennt sich bei ca. $10\dots 15\,\text{N}$ axialer Zugkraft völlig verschleiß- und zerstörungsfrei, wenn der Koffer in der Werkstatt oder im Hotel ohne vorheriges Abstecken abgenommen wird. Zieht sich beim Aufsetzen des Koffers selbstzentrierend zusammen.
2. **Mechanische Befestigung Fahrzeugseite (Rahmen):**
   * **Option A (Stationäres Rahmendock):** Die Buchse wird formschlüssig in das 3D-Druck Gehäuse [`009_magsafe_frame_dock.scad`](../../hardware/cad/scad/02_pod_base/parts/009_magsafe_frame_dock.scad) eingelegt. Es wird mit der Halbschelle (`009_magsafe_frame_clamp.stl`) am Ø 25.4–28.6 mm Rahmenrohr unter der Sitzbank mit 4x M3 Schrauben (in integrierten DIN 934 Nut-Pockets) fest verschraubt.
   * **Option B (Flexibler Rahmentunnel-Clip):** Bei Adventure-Bikes ohne freies Rahmenrohr sitzt die Buchse in einem elastischen Clip an der Soziusfußrasten-Aufnahme.
3. **Mechanische Befestigung Kofferseite (Pannier):**
   * **Montageort:** Die Koffer-Durchführung sitzt **seitlich-innen an der Koffer-Vorderwand (oberhalb des Schwingenlagers)** im absoluten Wind- und Spritzwasserschatten des Rahmens.
   * **Bohrung & Dichtung:** Ein einzelnes $\varnothing 12\,\text{mm}$ Loch in der Koffer-Vorderwand nimmt die geteilte EPDM/TPU-Dichtung ([`010_saddlebag_hole_grommet_split.scad`](../../hardware/cad/scad/02_pod_base/parts/010_saddlebag_hole_grommet_split.scad)) auf. Der **Kofferboden bleibt zu 100 % intakt, lochfrei und wasserdicht**.
   * **Integrierte Stufe-1 Zugentlastung:** Ein an der Dichtung angeformter Klemmturm fixiert das Kabel per Mini-Kabelbinder formschlüssig. Reißt die Magnetkupplung ab, werden die $10\dots 15\,\text{N}$ Zugkraft vollständig in die Kofferwand eingeleitet – kein Zug auf die Kofferinnenverkabelung!

---

## 12. Zukaufteile & Normteile-Einkaufsliste (1 Komplettset)

| Bauteil | Spezifikation / Typ | Bezugsquelle | Menge | Montageort & Funktion |
| :--- | :--- | :--- | :---: | :--- |
| **M3 Edelstahlschrauben** | M3 x 40 mm Zylinderkopf V4A (DIN 912) | Normteil / Amazon | 4 Stk. | Zentralbox-Gehäuse (greift in Nut-Pockets) |
| **M3 Edelstahlschrauben (Front)** | M3 x 20 mm Zylinderkopf V4A (DIN 912) | Normteil / Amazon | 4 Stk. | Front-Node Gehäuse (greift in Nut-Pockets) |
| **M3 Edelstahlschrauben (Dock)** | M3 x 16 mm Zylinderkopf V4A (DIN 912) | Normteil / Amazon | 4 Stk. | Rahmenklemmschelle `009_magsafe_frame_dock` |
| **M3 Edelstahlmuttern** | DIN 934 / DIN 985 M3 V4A Muttern | Normteil / Amazon | 12 Stk.| Unverlierbar in Nut-Pockets eingelegt (Zentralbox, Front-Node, Rahmendock) |
| **M4 Edelstahlmuttern (AMPS & Radar)**| DIN 934 M4 V4A Muttern | Normteil / Amazon | 6 Stk. | 4x Front-Node Wanne (AMPS), 2x Radar 2.0 Gehäuserückwand |
| **M4 Schrauben (Radar-Cradle)** | M4 x 12 mm Zylinderkopf V4A (DIN 912) | Normteil / Amazon | 2 Stk. | Verschraubung Adapterplatte `radar_swivel_tilt_cradle` an Radar 2.0 Gehäuse |
| **M5 Hirth-Klemmschraube** | M5 x 25 mm Zylinderkopf V4A (DIN 912) | Normteil / Amazon | 1 Stk. | Horizontale Gelenkachse Radar-Hirth-Gelenk (Kennzeichenträger / Underfender / Adventure-Rack) |
| **M5 Edelstahlmutter (Radar)** | DIN 934 M5 V4A Mutter | Normteil / Amazon | 1 Stk. | Unverlierbar in rechter Gabelwange des Radarträgers |
| **M5 Klemmschrauben (Adventure)** | M5 x 25 mm Zylinderkopf V4A (DIN 912) | Normteil / Amazon | 2 Stk. | Rohrklemmschelle `adventure_rack_radar_mount` (von unten montiert) |
| **M5 Muttern (Adventure-Clamp)** | DIN 934 M5 V4A Muttern | Normteil / Amazon | 2 Stk. | Unverlierbar in oberer Klemmschellen-Kappe `adventure_rack_radar_clamp_cap` |
| **M8 IP68 Kabelverschraubung** | M8 x 1.25 Messing vernickelt / PA66 IP68 mit EPDM-Dichtung | Skintop / Lapp / Amazon | 1 Stk. | Spritzwasserdichte Gehäuseboden-Durchführung für 2-poliges FLRY-B Kabel |
| **M2.5 Platinenschrauben** | M2.5 x 6 mm Zylinderkopf V4A (DIN 912) | Normteil | 8 Stk. | 4x Zentralbox-Platine, 4x Front-Node-Platine |
| **M2 Kassetten-Platinenschrauben**| M2 x 6 mm Zylinder-/Flachkopf V4A (DIN 7985/912) | Normteil | 8 Stk. | Befestigung von PCBA 03 im Kassetten-Schlitten (4x pro Kassette; Schottwandschrauben entfallen zu 100 %) |
| **M2 Kassetten-Halteplattenschrauben**| M2 x 6 mm Senkkopf V4A (DIN 7991) | Normteil | 8 Stk. | Fixierung der Aktuator-Niederhalteplatten (4x pro Gateway-Kassette) |
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
| **2-Pin Magnet-Pogo Kupplung**| IP68 Magnetstecker + Buchse (z. B. HytePro M411) | COTS Standard | 2 Sets | Koffer-Trennstelle (Abreißkraft 10-15 N, wasserdicht) |
| **Pure-DC 2-Ader Zuleitung (PUR)**| 2x 0.34 mm² (AWG22) mit JST-JWPF 2-Pin / Magnetkupplung | COTS Standard | 2 Stk. | Pure-DC 5V Stromversorgung zu Pod 1 und Pod 2 (Audio/Daten 100 % via UWB) |
| **Radar 12V Zuleitung (PUR)** | 2x 0.5 mm² (AWG20) mit JST-JWPF 2-Pin IP67 Stecker | COTS Standard | Opt. (1)| 12V DC Bordnetzspeisung für Heck-Radar (Datenübertragung 100 % drahtlos via UWB) |
| **Front-Node 12V Anschlusskabel**| 2-Pin JST-PH Litzenkabel mit Posi-Tap | COTS Standard | 1 Stk. | Lokale Cockpit-Stromversorgung (Standlicht/Navistecker) - *Funkbrücke via UWB!* |
| **12V Y-Adapterkabel (Bench/Car)**| Zigarettenanzünderstecker -> JST-JWPF 2P + Deutsch DTM-12 | Eigenbau / COTS | 1 Stk. | Prüfstands- & Begleitfahrzeug-Versorgung (Front-Node + Zentralbox), CarPlay frei |
| **USB-C Panel-Mount Pigtails**| JST-PH 5-Pin auf wasserdichte USB-C Buchse (IP67) | Amazon / COTS | 2 Stk. | Phone Fast-Charge (Lenker) & Glovebox (Tankrucksack) |
| **USB-A Buchsen Pigtails** | JST-PH 4-Pin auf Standard USB-A Buchse (15-20 cm) | Amazon / COTS | 2 Stk. | CP2AA Wireless CarPlay Dongle & Cockpit Aux Port |
| **JST-PH Pigtail Sortiments-Set**| 2-Pin, 3-Pin, 4-Pin JST-PH mit vormontierten Litzen | Amazon / COTS | 1 Set (10 Stk.) | CAN-Bus, Lenkertaster, Spiegel-LEDs, Qi-Lader, Action-Cam |
| **Qwiic / STEMMA QT Sensorkabel**| 4-Pin JST-SH Buchse zu Buchse (50 mm / 100 mm) | SparkFun / Adafruit | 1 Stk. | Verbindung PCBA 05 `J12` zu SAM-M10Q GNSS |
| **MR20 Radar-Kabel** | 4-Pin JST-SH Buchse zu Buchse (50 mm) | SparkFun / Adafruit | Opt. (1)| Verbindung PCBA 08 `J2` zu Wheeltec MR20 Radar |
| **Zentralbox USB-C Pigtail** | IDC 10-Pin auf wasserdichte Panel-Mount USB-C Buchse | COTS Standard | 1 Stk. | CarPlay / Flashing Port an der Zentralbox-Flanke |
| **J_ACT Aktuator-Kabelbaum** | Vorkonfektioniertes 8-Pin JST-SH Kabel auf 4x 2-Pin Litzen | Adafruit / SparkFun | 2 Stk. | 4 verdrillte Paare (AWG30 Silikon, 60 mm) zu den 4 Hubmagneten |
| **Miniatur-Aktuatoren** | 5V DC Hubmagnete ($\varnothing 6{,}5 \times 12\,\text{mm}$) mit TPU-Spitze | Solenoid / Web | 8 Stk. | 4 Stk. pro Smart Cartridge (Sena / Cardo) |
| **J2 Gateway OEM-Kabelstrang**| 6-Pin JST-SH Adapterkabel für Sena / Cardo / Midland | COTS Standard | 2 Stk. | Modellspezifisches Fertigkabel für Headset-Audio & Dauerstrom |
| **JST-JWPF 2-Pin IP67 Steckverbinder-Set**| 02R-JWPF-VSLE-S & 02T-JWPF-VSLE-S (2-Pol wasserdicht) | JST | 1 Set | Wasserdichte 12V DC Kfz-Zuleitung für Radar 2.0 Sub-MCU |
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

## 14. Kostenkalkulation, Bestelltaktik & Skaleneffekt (Solo vs. 2-3 Bikes)

> [!IMPORTANT]
> **Wichtiger Preishinweis zu OEM-Adaptern & Fremdgeräten:**
> Die hier kalkulierten Hardware-Kosten von **ca. 135 € bis 250 €** beziehen sich **ausschließlich auf das OpenMotorBridge-Gesamtsystem** (bestückte PCBAs, 3D-Druckteile, COTS-Kabelbäume, 2.200 mAh Pufferakku, Dichtungen, Normteile).
> Eventuell in die Gateway-Slots eingesetzte kommerzielle Fremd-Intercoms (wie z. B. **Sena SPIDER X Slim**, **Cardo Packtalk Edge**) oder Radargeräte (**Garmin Varia RTL515 / eRTL615**) sind **Zukaufteile des Benutzers** und nicht in den genannten Selbstbau-Kosten enthalten!

### 14.1 Szenario A: Der Solo-Builder (1 Gesamtsystem für 1 Motorrad)
Bestellt ein einzelner Anwender alle Platinen für sich allein:
* JLCPCB liefert 5 Platinen pro Design (davon 2 voll bestückt und 3 unbestückte Ersatzplatinen).
* **Kostenaufstellung Solo-Builder:**
  * JLCPCB PCBAs (PCBA 01, 02 [2x], 03 [2x], 05 bestückt inkl. Versand & Zoll): ca. 135-160 €
  * 3D-Druck (MJF PA12 Dienstleister oder eigenes ASA-Filament): ca. 35-45 €
  * COTS-Kabel, 2.200 mAh LiPo, V4A Normteile & Dichtungen: ca. 35-45 €
  * **Gesamtkosten Solo-System: ca. 205 € bis 250 €**

### 14.2 Szenario B: Community- / Gruppenbestellung (2 bis 3 Motorräder)
Bestellen 2 bis 3 Motorradfahrer gemeinsam:
* Bei JLCPCB werden direkt **alle 5 Platinen voll bestückt** bestellt.
* Die fixen Rüstkosten verteilen sich nun auf 5 voll funktionsfähige Platinensätze.
* **Kostenaufstellung pro Motorrad (bei 3 Bikes):**
  * JLCPCB PCBAs (Anteil pro Bike): ca. 70-80 €
  * 3D-Druck (pro Bike): ca. 30-35 €
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

Um eine 100%ige Langzeitausfallsicherheit nach Automotive-Standard zu gewährleisten, werden alle 5 aktiven PCBAs im Serienbestellprozess schutzlackiert:

### 16.1 Lackspezifikation & Qualifikation
* **Standard:** Zertifiziert nach **IPC-CC-830B** und **MIL-I-46058C**.
* **Lacktyp:** **Modifizierter Acryllack (AR)**, z. B. *Peters ELPEGUARD SL 1307 FLZ* (schnell trocknend, fluoreszierend unter UV-Licht zur optischen Qualitätskontrolle).
* **Schichtdicke:** $30\,\mu\text{m}$ bis $60\,\mu\text{m}$ gleichmäßig auf Top- und Bottom-Layer.

### 16.2 Maskierungsvorgaben (Kapton-Tape Schutzmaske)
Folgende Bereiche dürfen **unter keinen Umständen** mit Schutzlack benetzt werden:
1. **Steckverbinder & Kontaktbuchsen:**
   * USB-C Buchsen (`J7` Front-Node, Service-Ports)
   * Automotive-Steckverbinder & Kontakte (`PAD1`/`PAD2` Kassetten-Pads, JST-JWPF 2-Pin Radar `J1`, Deutsch DTM-12 Zentralbox `J1`)
   * JST-SH / JST-PH / Qwiic Buchsenleisten (`J1..J12` Front-Node, `J_ACT`/`J2` Kassetten, `J2` Radar-Sensor)
   * MicroSD Kartenleser-Slot (`J2` Zentralbox auf B.Cu)
2. **Akustische Sensoren & Ventile:**
   * **MEMS-Mikrofon (`MIC1` MSM261S4030H0R auf PCBA 05):** Schalleintrittsöffnung ($\varnothing 0{,}5\,\text{mm}$) muss zwingend mit Kapton versiegelt werden!
   * **Druckausgleichsmembran (Gore ePTFE Vent):** Darf nicht verkleben.
3. **HF-Antennen & Messpunkte:**
   * U.FL Koaxial-Buchsen (`ANT1`, `ANT2`)
   * Testpunkte für In-Circuit-Flash & Oszilloskop-Abgriffe
