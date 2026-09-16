# 15 - Stücklisten (BOM) & SMT-Fertigungsdaten (Alle 7 PCBAs)

Dieses Dokument enthält die vollständige Bauteilliste (Bill of Materials) und Fertigungsspezifikation für alle 5 Leiterplatten (PCBA 01 bis PCBA 05) bei JLCPCB / Eurocircuits, alle mechanischen 3D-Druck-Komponenten, das Inbetriebnahmeprotokoll, den JLCPCB SMT-Bestellleitfaden sowie die COTS-Einkaufsliste.

---

## 1. PCBA 01: Zentralbox Hauptplatine (`kicad_main_box`, 4-Layer FR4 TG150)

| Designator | Bauteil / MPN | Hersteller | Gehäuse | LCSC / JLCPCB Part # | Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | ESP32-S3-WROOM-1-N16R8 | Espressif Systems | SMD Modul | C2913200 | Haupt-MCU (Dual-Core, 16 MB Flash, 8 MB PSRAM) |
| **U2** | LM5164-Q1 | Texas Instruments | SOIC-8-EP | C2843477 | Automotive 65V Synchronous Buck Converter |
| **U3** | BQ24075RGTR | Texas Instruments | VQFN-16 | C128509 | Dynamisches Power-Path Management & LiPo-Lader mit TS |
| **U4** | BMI270 | Bosch Sensortec | LGA-14 | C2838380 | 6-Achsen IMU für Schräglagen- & Bewegungserkennung |
| **U5** | ES8388 | Everest Semi | QFN-28 | C144547 | 24-Bit Stereo Audio Codec (I2S ADC/DAC) |
| **U6** | TCAN334GDCNR | Texas Instruments | SOT-23-8 | C842340 | 3.3V Automotive CAN-FD Transceiver (±58V Fault) |
| **T1, T2** | LM-NP-1001-B1L | Bourns Inc. | SMD Übertrager | C114402 | 1:1 Audio-Übertrager (1500 V RMS galvanische Trennung) |
| **OC1, OC2**| TLP222A(F) | Toshiba | SOP-4 | C112444 | Halbleiter-PhotoMOS-Relais für PTT-Tastensimulation |
| **D1** | SMBJ33CA | Littelfuse | DO-214AA (SMB) | C87848 | TVS-Diode (33 V Standoff, 53.3 V max Clamping) |
| **F1** | MF-MSMF050-2 | Bourns | 1812 SMD | C22668 | Rückstellbare PPTC-Sicherung (500 mA Hold / 1.0 A Trip) |
| **LED1** | WS2812B-B | Worldsemi | 5050 SMD | C114586 | RGB Status-LED für optische Betriebsmodusanzeige |
| **J1** | 2x13 Wannenstecker | Standard 2.54 mm | THT Box Header | C2934175 | Interner Pfostenverbinder zur HD26-Flanschbuchse |
| **J2** | MicroSD Slot Push-Push | Molex / Korean Hro | SMD Push-Push | C266624 | 4-Bit SDIO Speicherkarte für Tour-Logging |
| **J_BAT** | Molex Micro-Fit 3.0 2P | Molex | SMD Header | C289110 | Steckverbindung zum LiPo Pufferakku |
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
| **U2** | USB2514B-AEZG | Microchip | QFN-36 | `C97185` | Automotive USB 2.0 High-Speed 480 Mbps 4-Port Hub Controller |
| **U3** | LMR36015FSCQRNXRQ1 | Texas Instruments | VQFN-12 | `C2843480` | Automotive 36V Synchronous Buck (5V / 2.0A, 91.8%) für Hub & Peripherie |
| **U4** | TPS2051BDBVR | Texas Instruments | SOT-23-5 | `C7818` | High-Side USB VBUS Power Switch (1.05A Clamp) für Port 2 Kaltstart-Reset |
| **U5** | SC8102QDER | Southchip | QFN-32 | `C2843510` | Automotive Synchronous Buck mit USB-PD 20W (9V/2.2A & QC3.0) für Smartphone Port 1 |
| **U6** | TCAN334GDCNT | Texas Instruments | SOT-23-8 | `C2843515` | 3.3V CAN-Transceiver (5 Mbps CAN-FD fähig, mit Pin 8 Silent-Listen-Only Mode) |
| **K1** | CPC1017NTR | IXYS / Littelfuse | SOP-4 | `C26789` | 60V / 100mA 1-Form-A Solid-State Relais für schaltbaren 120R CAN-Abschluss (Auto-Sensing) |
| **Q1** | DMN63D8LDW-7 | Diodes Incorporated| SOT-363 | `C283890` | Dual N-Kanal MOSFET (30V / 260mA) für richtungsgetrennte Spiegel-Totwinkel-LEDs (J9) |
| **Q2** | TPS1H100BQPWPRQ1 | Texas Instruments | HTSSOP-14 | `C2843520` | Automotive Smart High-Side Power Switch (bis 3.5A / 40W) für 12V Aux Light (J11) |
| **LED1**| WS2812B-2020 | Worldsemi | SMD 2020 | `C2843530` | Digital steuerbare RGB-Status-LED für Gehäusedeckel-Lichtleiter |
| **MIC1**| SPH0645LM4H-B | Knowles | 3.5x2.65 mm SMD | `C119850` | Digitales I2S-MEMS Akustik-Mikrofon für Fahrtwind- & Staudruckmessung |
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

## 6. Mechanik- & Gehäuse-BOM (3D-Druck MJF PA12 & Normteile)

Alle Gehäuseteile sind für das **IKEA-Prinzip** optimiert: **Kein Einschmelzen von Gewindeeinsätzen mit dem Lötkolben erforderlich!** Die Gehäuse verfügen über integrierte Sechskant-Mutternaschen (Nut Pockets für Standard DIN 934 / DIN 985 Edelstahlmuttern) bzw. Kernlöcher für selbstfurchende Kunststoffschrauben.

### 6.1 Basis-System (Universal für jedes Motorrad)
| Baugruppe | STL-Dateiname | Stück | Material & Fertigung | Funktion & Beschreibung |
| :--- | :--- | :---: | :--- | :--- |
| **Main Box Unterteil** | [`main_box_lower_case.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lower_case.stl) | **1** | MJF PA12 / ASA | Monocoque-Unterwanne mit 4x M4 Silentblock-Ohren, Mutternaschen & Dichtnut |
| **Main Box Zwischenboden** | [`main_box_mid_tray.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_mid_tray.stl) | **1** | MJF PA12 / ASA | Akku-Wanne für 1000 mAh LiPo, 10x Konvektionsschlitze & Dichtfeder |
| **Main Box Deckel** | [`main_box_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lid.stl) | **1** | MJF PA12 / ASA | Gehäusedeckel mit Gore ePTFE-Ventilsitz & Schraubensenkungen |
| **Pod-Basisgehäuse** | [`pod_base_housing.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod_base_housing.stl) | **3** | MJF PA12 / ASA | Universal-Schachtgehäuse für Pod 1 (Links), Pod 2 (Rechts) und Heck-Pod 3 |
| **Pod-Schottwände** | [`03_pod_bulkhead_partition.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl) | **3** | MJF PA12 / ASA | Schottwand mit Dichtkragen & Federaufnahmen (1x pro Pod) |
| **Kassetten-Basisschlitten**| [`cartridge_base_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl) | **3** | MJF PA12 / ASA | Universalschlitten für Gateway 1 (Pod 1), Gateway 2 (Pod 2) und OMM (Pod 3) |
| **Kassetten-Riegel / Wippe**| [`cartridge_magnetic_lock_latch.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_magnetic_lock_latch.stl) | **2** | MJF PA12 / ASA | Magnetische Diebstahlschutz-Rastwippen für Kassetten-Slots 1 & 2 |
| **Heck-Pod 3 OMM-Radom** | [`cartridge_antenna_bracket_omm.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_antenna_bracket_omm.stl) | **1** | MJF PA12 / ASA | Dielektrisches Antennenradom & Trägerbrücke für PCBA 04 im Heck-Pod 3 |
| **Front-Knoten Unterwanne** | [`front_node_lower_tub.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_lower_tub.stl) | **1** | MJF PA12 / ASA | Cockpit-Wanne mit AMPS-Bohrbild, Rohrbett & Mutternaschen |
| **Front-Knoten Deckel** | [`front_node_upper_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_upper_lid.stl) | **1** | MJF PA12 / ASA | Deckel mit Knowles MEMS Schalleintritt & O-Ring-Dichtnut |
| **Front-Knoten Dichtkämme** | [`front_node_cable_glands_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_cable_glands_tpu.stl) | **1 Paar**| TPU 95A / 85A | Elastische Dichtkämme für Front-USB & Signale |
| **Front-Knoten USB-C Kappe**| [`front_node_usbc_cap_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_usbc_cap_tpu.stl) | **1** | TPU 95A / 85A | Elastische Staubschutzkappe mit Haltekollier für Service-Port |

### 6.2 Gateway-Kassetten-Inlays (Passend zur gewünschten Intercom-Ausstattung)
> **Hinweis zur Architektur:** Slot 1 und Slot 2 sind **Multi-Protokoll Gateway-Transceiver**, keine Fahrer/Beifahrer-Kopfhörer! Sie verbinden das Motorrad gleichzeitig mit Sena Mesh und Cardo DMC. Fahrer und Sozius funken drahtlos mit ihren normalen Helmen.

| Baugruppe | STL-Dateiname | Stück | Material | Funktion & Beschreibung |
| :--- | :--- | :---: | :--- | :--- |
| **Gateway-Inlay Sena** | [`cartridge_insert_sena.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) | *Opt. (1)* | MJF PA12 / ASA | Formschlüssiges Inlay für Sena SPIDER X Slim / 50S / 60S (Mesh 3.0 Wave) |
| **Gateway-Inlay Cardo** | [`cartridge_insert_cardo.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl) | *Opt. (1)* | MJF PA12 / ASA | Inlay für Cardo Packtalk Edge / Pro (DMC Gen2) mit Air-Mount |
| **Blindkassette / Dry Box** | [`cartridge_insert_blindkassette.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_blindkassette.stl) | *Opt. (1)* | MJF PA12 / ASA | Hermetischer Schutzschlitten für ungenutzten Slot oder regendichte Dry Box |

### 6.3 Fahrzeugspezifische Montage-Kits (3D-Druckteile)
* **Kit 1: BMW R1250 / R1300 GS (Standard / Vario-Koffer):**
  * `adventure_transition_dock.stl` (2 Stk.): Kofferunabhängige Docks für die Sitzbank-Bügelfalte (Ø 28 mm Rahmenrohr).
  * `adventure_rack_tail_mount.stl` (1 Stk.): Heckbrücken-Ausleger für Pod 3 & Radar.
  * `radar_varia_gopro_lock_dock.stl` (1 Stk.) & `011_gopro_hirth_lock.stl` (1 Stk.): Radar-Bajonett-Dock mit Hirth-Verzahnung.
* **Kit 2: BMW R1250 / R1300 GSA (Adventure mit Ø 18 mm Edelstahl-Alukofferträger):**
  * `adventure_pannier_rack_clamp_base.stl` & `adventure_pannier_rack_clamp_cap.stl` (je 4 Stk.): Schwerlast-Klemmschellen-Paare für Pod 1 & 2 im Kofferträger-Rahmendreieck.
  * `adventure_rack_tail_mount.stl` (1 Stk.): Heck-Balkon hinter Alutopcase mit 45°-Astabweiser für Dipolantenne.
  * `radar_varia_gopro_lock_dock.stl` (1 Stk.) & `011_gopro_hirth_lock.stl` (1 Stk.): Radar-Dock mit Hirth-Verzahnung.
* **Kit 3: Harley-Davidson Touring & Classic Bagger (Street Glide, Road Glide, Road King):**
  * `saddlebag_lid_dock.stl` (2 Stk.): Kofferdeckel-Montagedocks für Pod 1 & 2.
  * `pod3_touring_fender_console.stl` (1 Stk.): Organische Heckkotflügel-Konsole für Pod 3 (Road King Special).
  * `radar_license_plate_bracket.stl` (1 Stk.): Entkoppelter Kennzeichen-Radarhalter.
* **Kit 4: Harley-Davidson CVO ST & Performance Bagger (Road Glide ST):**
  * `saddlebag_lid_dock.stl` (2 Stk.): Kofferdeckel-Montagedocks für Pod 1 & 2.
  * `cvo_st_undercowl_skeleton_dock.stl` (1 Stk.): Aufrechtes Federsitz-Dock für Pod 3 unter der Forged-Carbon-Hutze.
  * `cvo_st_telemetry_fin.stl` (1 Stk.): Aerodynamische Haifischflosse / Telemetrie-Finne auf der Hecklasche.
  * `radar_center_underfender_mount.stl` (1 Stk.): Zentrische Unter-Kotflügel-Platte für Radar (freie Showa-Reservoirs).
* **Kit 5: Universal (Andere Motorräder):**
  * Standard 120°-V-Nut am Pod-Basisgehäuse für Rahmenrohre (Ø 22–32 mm) mit EPDM-Spannringen oder M4 Silentblöcken.

### 6.4 Zubehör (Optional)
| Baugruppe | STL-Dateiname | Stück | Material | Funktion & Beschreibung |
| :--- | :--- | :---: | :--- | :--- |
| **Smart-Keyfob Unterschale**| [`smart_keyfob_lower_shell.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/smart_keyfob_lower_shell.stl) | **1** | MJF PA12 / ASA | Wanne mit LRA-Dämpfungsbett und Magnetaufnahme für PCBA 07 |
| **Smart-Keyfob Oberschale** | [`smart_keyfob_upper_shell.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/smart_keyfob_upper_shell.stl) | **1** | MJF PA12 / ASA | Deckel mit 3 Tastenfeldern & Lichtleiter |
| **Smart-Keyfob Bumper** | [`smart_keyfob_tpu_rim.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/smart_keyfob_tpu_rim.stl) | **1** | TPU 85A / 95A | Elastischer Stoßschutz-Umlaufring |

### 6.5 OrcaSlicer 3MF Projekt-Platten (Standard vs. Kompakt Bauraum)
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

## 7. Inbetriebnahme, WebSerial 1-Click Flasher & Smoke-Test

Da alle Platinen fertig bestückt und vorgetestet geliefert werden, reduziert sich die Inbetriebnahme auf wenige geführte Schritte direkt im Browser:

### Schritt 1: WebSerial 1-Click Firmware Installer (PWA)
* Kein Terminal, kein Python, keine Treiberinstallation!
* Zentralbox per USB-C an den PC/Mac anschließen.
* In der OpenMotorBridge PWA im Tab *System Builder* auf **„USB-C verbinden & Flashen“** klicken.
* Der Browser überträgt Bootloader, Partitionen, Firmware und SPIFFS-Profile automatisch auf den ESP32-S3 und RP2040.

### Schritt 2: Der interaktive 4-Punkte IKEA Smoke-Test
Vor dem endgültigen Zudrücken und Verschrauben der Gehäusedeckel führt die PWA einen automatischen Diagnose-Check durch:
* [x] **Check 1 (Bordnetz & USV):** 12.6V Batteriespannung, 5.04V Buck-Schiene, 1000 mAh LiPo-Zelle auf 4.18V.
* [x] **Check 2 (Kassetten & Aktuatoren):** 1-Wire DS2431 Auslesen der Kassetten-IDs (Sena / Cardo), Pogo-Pin Kontaktierung und automatischer 4-Aktuator Klicktest.
* [x] **Check 3 (Front-Knoten & Cockpit):** I2C-Ping Knowles MEMS Mikrofon, SDP31 Staudruck-Sensor (0.02 hPa) und Lenker-PTT Taster.
* [x] **Check 4 (Heck-Pod 3):** SX1262 LoRa 868 MHz Ping-Echo und u-blox GNSS 3D-Satellitenfix.
* [ ] Status-Check: Beide Gateway-Slots (Pod 1 & Pod 2) werden erkannt, Heck-Pod 3 liefert GNSS-Fix.

---

## 8. 1-Click Bestellleitfaden für JLCPCB (Alle Leiterplatten fertig bestückt)

Alle Fertigungsdaten liegen im Repository als fertige ZIP- und CSV-Pakete vor:

| Baugruppe / PCBA | Gerber-ZIP Datei | BOM CSV Datei | CPL (Pick & Place) CSV | Lagen | Fertigungs-Hinweis |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **1. Zentralbox Hauptplatine** | `01_main_box_pcba_gerbers_jlcpcb.zip` | `01_main_box_pcba_bom_jlcpcb.csv` | `01_main_box_pcba_cpl_jlcpcb.csv` | **4 Lagen** | ENIG (Gold), 1.6 mm, TG150, SMT beidseitig |
| **2. Pod-Basisplatine** | `02_pod_base_pcba_gerbers_jlcpcb.zip` | `02_pod_base_pcba_bom_jlcpcb.csv` | `02_pod_base_pcba_cpl_jlcpcb.csv` | **2 Lagen** | ENIG (Gold), 1.6 mm, SMT Top |
| **3. Kassetten-Trägerplatine** | `03_pod_cartridge_pcba_gerbers_jlcpcb.zip` | `03_pod_cartridge_pcba_bom_jlcpcb.csv` | `03_pod_cartridge_pcba_cpl_jlcpcb.csv` | **2 Lagen** | ENIG (Gold), 1.2 mm, SMT Top |
| **4. Heck-Pod 3 Transceiver** | `04_rear_pod3_pcba_gerbers_jlcpcb.zip` | `04_rear_pod3_pcba_bom_jlcpcb.csv` | `04_rear_pod3_pcba_cpl_jlcpcb.csv` | **4 Lagen** | ENIG (Gold), 1.6 mm, TG150, SMT Top |
| **5. Universal Front-Knoten** | `05_front_node_pcba_gerbers_jlcpcb.zip` | `05_front_node_pcba_bom_jlcpcb.csv` | `05_front_node_pcba_cpl_jlcpcb.csv` | **4 Lagen** | ENIG (Gold), 1.6 mm, TG150, SMT beidseitig |
| **7. Smart-Keyfob (Zubehör)** | `07_smart_keyfob_pcba_gerbers_jlcpcb.zip` | `07_smart_keyfob_pcba_bom_jlcpcb.csv` | `07_smart_keyfob_pcba_cpl_jlcpcb.csv` | **2 Lagen** | ENIG (Gold), 1.0 mm, SMT beidseitig |

---

## 9. Vorkonfektionierte COTS-Kabel (Kein Crimpen, kein Löten!)

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
  └─► M8 4-Pin Buchse (Peitsche 5, 250 mm): Heck-Radar (Garmin Varia) / Heck-OBD2/CAN (Front-Node verbindet sich drahtlos via ESP-NOW!)
```

---

## 10. Zukaufteile & Normteile-Einkaufsliste (1 Komplettset)

| Bauteil | Spezifikation / Typ | Bezugsquelle | Menge | Montageort & Funktion |
| :--- | :--- | :--- | :---: | :--- |
| **M3 Edelstahlschrauben** | M3 x 40 mm Zylinderkopf V4A (DIN 912) | Normteil / Amazon | 4 Stk. | Zentralbox-Gehäuse (greift in Nut-Pockets) |
| **M3 Edelstahlschrauben (Front)** | M3 x 20 mm Zylinderkopf V4A (DIN 912) | Normteil / Amazon | 4 Stk. | Front-Node Gehäuse (greift in Nut-Pockets) |
| **M3 Edelstahlmuttern** | DIN 934 / DIN 985 M3 V4A Muttern | Normteil / Amazon | 8 Stk. | Unverlierbar in Nut-Pockets eingelegt (kein Lötkolben nötig!) |
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
| **Pufferakku (LiPo USV)** | 1S LiPo (3.7V 1000mAh) mit Micro-Fit Stecker | EEMB / Enerpower | 1 Stk. | USV-Pufferung in der Zentralbox |
| **KFZ-Sicherungshalter** | Wasserdichter Flachsicherungshalter + 2A Sicherung | Hella / MTA | 1 Stk. | Dauerplus-Absicherung an Batteriepol |
| **M8 6-Pin Fertigkabel (PUR)**| M8 6-Pin A-Coded Stecker/Buchse (1.0m / 1.5m) | Binder / Phoenix | 3 Stk. | Plug-and-Play Verbindung zu Pod 1, 2 und 3 |
| **M8 4-Pin Fertigkabel (PUR)**| M8 4-Pin A-Coded Stecker/Buchse (0.5–1.5m) | Binder / Phoenix | Opt. (1)| Peitsche 5: Heck-Radar (Garmin Varia: 12V + UART) / Heck-OBD2 (nur bei Radar-Nutzung) |
| **Front-Node 12V Anschlusskabel**| 2-Pin JST-PH Litzenkabel mit Posi-Tap | COTS Standard | 1 Stk. | Lokale Cockpit-Stromversorgung (Standlicht/Navistecker) – *Funkbrücke via ESP-NOW / BLE!* |
| **J_ACT Aktuator-Kabelbaum** | Fertiges 8-Pin JST-SH Kabel auf 4x 2-Pin Litzen | Adafruit / SparkFun | 1–2 Stk.| Vorkonfektioniertes Fertigkabel für 4 Hubmagnete |
| **Miniatur-Aktuatoren** | 5V DC Hubmagnete ($\varnothing 6{,}5 \times 12\,\text{mm}$) mit TPU-Spitze | Solenoid / Web | 4–8 Stk.| 4 Stk. pro Smart Cartridge (Sena / Cardo) |
| **J2 Gateway-Kabelbaum** | Fertiges 6-Pin JST-SH Kabel auf Klinke / USB | COTS Standard | 1–2 Stk.| Fertigkabel für Headset-Audio & Dauerstrom |

---

## 11. Minimalistische Werkzeugliste (Das echte IKEA-Prinzip)

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





