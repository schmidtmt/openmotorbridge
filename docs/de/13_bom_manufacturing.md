# 13 - Stücklisten (BOM) & SMT-Fertigungsdaten (Alle 5 PCBAs)

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

## 3. PCBA 03: Universalschlitten Cartridge (`openmotorbridge_pod_cartridge`, 2-Layer FR4)

| Designator | Bauteil / MPN | Hersteller | Gehäuse | LCSC / JLCPCB Part # | Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **J1** | PinSocket_1x06_P2.54mm_SMD | Harwin / Samtec | SMD Horizontal | C2934177 | Stirnseitige 6-Pin Präzisionsbuchse |
| **J2** | JST-SH 1.0mm 6-Pin Horizontal| JST | SMD Liegend | C136657 | Flachbandkabel-Anschluss zum Headset-Inlay |
| **U1** | DS2401Z+ | Maxim / ADI | SOT-223 / SOT-23 | C2834570 | 64-Bit 1-Wire Silicon Serial ROM (Kassetten-ID) |
| **F1** | MF-MSMF050-2 (500mA) | Bourns | 1812 SMD | C22668 | Rückstellbare PPTC-Sicherung für Kassettenstromkreis |
| **D1** | Grüne 5V Power-LED | Everlight | 0805 SMD | C2297 | Optische Betriebsanzeige für 5V Speisung |
| **D2** | SP3012-06UTG | Littelfuse | DFN-14 | C2834580 | 6-Kanal ESD-Schutzmatrix für Audio & Daten |

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

## 5. PCBA 05: Universal Front-Knoten (`openmotorbridge_front_node`, 4-Layer FR4 TG150)

| Designator | Bauteil / MPN | Hersteller | Gehäuse | LCSC / JLCPCB Part # | Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | ESP32-C3-WROOM-02U-N4 | Espressif Systems | SMD Modul | C2934560 | 32-Bit RISC-V Controller (160 MHz, ext. U.FL) |
| **U2** | USB2512B-AEZG | Microchip | QFN-36 | C97184 | USB 2.0 High-Speed 480 Mbps 2-Port Hub Controller |
| **U3** | LMR36015FSCQRNXRQ1 | Texas Instruments | VQFN-12 | C2843480 | Automotive 36V Synchronous Buck (5V / 2.0A, 91.8%) |
| **U4** | TPS2051BDBVR | Texas Instruments | SOT-23-5 | C7818 | High-Side USB VBUS Power Switch (1.05A Clamp) |
| **MIC1** | SPH0645LM4H-B | Knowles | 3.5x2.65 mm SMD | C119850 | Digitales I2S-MEMS Akustik-Mikrofon für Fahrtwind |
| **L1** | 4.7 µH Automotive Inductor | Sunlord / Wurth | SMD 5x5 mm | C2843490 | Speicherdrossel für LMR36015 Abwärtswandler |
| **J1** | USB-A Receptacle R/A | Amphenol / Korean Hro | SMD Liegend | C2934180 | Port 1: Geschalteter VBUS für Ottocast Dongle |
| **J2** | USB-C 16-Pin Receptacle IP67| GCT / Korean Hro | SMD Hybrid | C2765186 | Port 2: Dauerstrom Handschuhfach / Ladeport |
| **J3** | JST-GH 2-Pin Header | JST | 1.25mm SMD | C2934185 | Lenker-PTT Schnittstelle (GPIO 0 Interrupt) |
| **J7** | 2-Pin Schraubklemme / JST-GH | Phoenix / JST | 2.54mm THT | C289115 | 12V Bordnetz-Einspeisung (KL15 & GND) |

---

## 6. Mechanik- & Gehäuse-BOM (3D-Druck MJF PA12 & Normteile)

### 6.1 Druckdateien-Übersicht (Modulare STLs für 1 Fahrzeug)
* **Zentralbox (3 Teile, PA12 / ASA):** `main_box_lower_case.stl`, `main_box_mid_tray.stl`, `main_box_lid.stl`.
* **Satelliten-Pods Basis (6 Teile, PA12 / ASA):** 3x `pod_base_housing.stl`, 3x `03_pod_bulkhead_partition.stl`.
* **Kassetten (3 Teile, PA12 / ASA):** `cartridge_sena_sled.stl` (oder Cardo), `cartridge_cardo_sled.stl` (oder Blindkassette), `cartridge_omm_transceiver_sled.stl`.
* **Front-Knoten Gehäuse (2 Teile, PA12 / ASA):** `front_node_lower_tub.stl`, `front_node_upper_lid.stl`.
* **Front-Knoten Dichtungen & Kappe (2 Teile, TPU 95A / 85A):** `front_node_cable_glands_tpu.stl` (Paar Dichtkämme für Front-USB & Flanken-Signale), `front_node_usbc_cap_tpu.stl` (elastische USB-C Staubschutzkappe mit Haltekollier).
* **Heck-Montage & Konsolen-Optionen für Pod 3 & Koffer (Referenz-Kits):**
  * **Typ D1 (Adventure / Rohrträger):** `pod3_radar_bracket.stl` (M5 GoPro-Schwenkarm direkt an Pod 3) & Standard-Rohrsattel (`005_pod_strap_hooks.scad`).
  * **Referenz-Kit 1 (CVO Road Glide ST & New Touring):** `cvo_st_undercowl_skeleton_dock.stl` (aufrechtes Federsitz-Dock unter Carbonhutze) + `cvo_st_telemetry_fin.stl` (2,4 GHz Heckfinne) + `saddlebag_lid_dock.stl` (Kofferdeckel-Dock).
  * **Referenz-Kit 2 (Road King Special):** `pod3_touring_fender_console.stl` (organische Kotflügel-Konsole für 1/4"-20 Mutter) + `saddlebag_lid_dock.stl`.
  * **Referenz-Kit 3 (Classic Bagger & Cruiser):** `pod3_touring_stealth_console.stl` (flache Touring-Konsole).
  * **Entkoppelter Radar-Halter (Cruiser / Bagger):** `radar_license_plate_bracket.stl` (zentrisch symmetrische M6-Klemmung unterhalb Kennzeichenhalter mit M5 GoPro-Gelenk & verdeckter M8-Kabelführung).

---

## 7. Inbetriebnahme-, Mess- & Testprotokoll (Schritt-für-Schritt)

### Schritt 1: Visuelle Inspektion (Vor dem ersten Einschalten)
* [ ] Lötbrücken unter LM5164, BQ24075, ES8388 und USB2512B mit Mikroskop/Lupe ausschließen.
* [ ] Polarität der TVS-Diode D1 (SMBJ33CA) und des P-FET Verpolschutzes kontrollieren.
* [ ] Prüfen, ob die 2,5 mm Isolationsbarriere um T1/T2 und OC1/OC2 frei von Zinnresten ist.

### Schritt 2: Spannungsprüfung & Strombegrenzung
* [ ] Labornetzteil auf $12{,}0\,\text{V DC}$ einstellen, Strombegrenzung auf $150\,\text{mA}$.
* [ ] Ruhestrom messen: Sollwert $= 45\,\text{mA}$ bis $75\,\text{mA}$ (ohne Akkuladung).
* [ ] Prüfpunkt `TP_5V`: Sollwert $= 5{,}15\,\text{V} \pm 0{,}05\,\text{V}$.
* [ ] Prüfpunkt `TP_3V3`: Sollwert $= 3{,}30\,\text{V} \pm 0{,}02\,\text{V}$.

### Schritt 3: Flashen & System-Selbsttest
* [ ] ESP-IDF / PlatformIO Flash via USB-C Port ausführen (`firmware/main_controller/`).
* [ ] LittleFS-Partition formatieren und Profile hochladen.
* [ ] Serielle Konsole ($115.200\,\text{Baud}$): Meldungen "LittleFS Mount OK", "1-Wire Manager Task OK", "I2S ES8388 Codec Init OK", "TCAN334G CAN-FD OK" verifizieren.

### Schritt 4: Audio- & Ducking-Funktionstest
* [ ] $1\,\text{kHz}$ Sinuston ($1{,}0\,\text{V}_{\text{RMS}}$) an Audio-Input anlegen.
* [ ] Oszilloskop an `PORT1_AUDIO_OUT`: Überprüfen, ob Signal innerhalb von $15\,\text{ms}$ weich gedämpft wird.
* [ ] Signal abschalten: Prüfen, ob nach $600\,\text{ms}$ Hold-Zeit die weiche $250\,\text{ms}$-Raised-Cosine-Rückkehr erfolgt.

### Schritt 5: IP67-Dichtheitsprüfung
* [ ] Montiertes Gehäuse in Vakuumkammer bei $-20\,\text{kPa}$ Unterdruck für 60 Sekunden halten (Druckverlust $< 0{,}5\,\text{kPa}$).

---

## 8. Schritt-für-Schritt Bestellleitfaden für JLCPCB (Alle 5 Leiterplatten)

| Baugruppe / PCBA | Gerber-ZIP Datei | BOM CSV Datei | CPL (Pick & Place) CSV | Lagen & Stackup | Oberfläche & Dicke |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **1. Zentralbox Hauptplatine** | `01_main_box_pcba_gerbers_jlcpcb.zip` | `01_main_box_pcba_bom_jlcpcb.csv` | `01_main_box_pcba_cpl_jlcpcb.csv` | **4 Lagen** (JLC04161H-7628) | **ENIG (Gold)**, 1.6 mm, TG150 |
| **2. Pod-Basisplatine** | `02_pod_base_pcba_gerbers_jlcpcb.zip` | `02_pod_base_pcba_bom_jlcpcb.csv` | `02_pod_base_pcba_cpl_jlcpcb.csv` | **2 Lagen** (Standard) | **ENIG (Gold)**, 1.6 mm |
| **3. Kassetten-Trägerplatine** | `03_pod_cartridge_pcba_gerbers_jlcpcb.zip` | `03_pod_cartridge_pcba_bom_jlcpcb.csv` | `03_pod_cartridge_pcba_cpl_jlcpcb.csv` | **2 Lagen** (Standard) | **ENIG (Gold)**, 1.2 mm |
| **4. Heck-Pod 3 Transceiver** | `04_rear_pod3_pcba_gerbers_jlcpcb.zip` | `04_rear_pod3_pcba_bom_jlcpcb.csv` | `04_rear_pod3_pcba_cpl_jlcpcb.csv` | **4 Lagen** (JLC04161H-7628) | **ENIG (Gold)**, 1.6 mm, TG150 |
| **5. Universal Front-Knoten** | `05_front_node_pcba_gerbers_jlcpcb.zip` | `05_front_node_pcba_bom_jlcpcb.csv` | `05_front_node_pcba_cpl_jlcpcb.csv` | **4 Lagen** (JLC04161H-7628) | **ENIG (Gold)**, 1.6 mm, TG150 |

---

## 9. Fertigung des zentralen Kabelbaums (HD26-Breakout-Pigtail)

```
                               ZENTRALER HD26 BREAKOUT-KABELBAUM
┌─────────────────────────┐
│ HD26 IP67 Stecker       │ ──► Gesamtlänge Peitschen: je 250 mm (mit schwarzem Geflechtschlauch)
│ (Amphenol LTW / D-Sub)  │ ──► Y-Verteilerpunkt vergossen mit Schmelzkleber / Schrumpfkappe
└─┬───────────────────────┘
  ├─► PEITSCHE 1 (250 mm): M8 6-Pin Buchse (A-kodiert, IP67) ──► Pod 1 (Helm Fahrer Links)
  ├─► PEITSCHE 2 (250 mm): M8 6-Pin Buchse (A-kodiert, IP67) ──► Pod 2 (Helm Sozius Rechts)
  ├─► PEITSCHE 3 (250 mm): M8 6-Pin Buchse (A-kodiert, IP67) ──► Pod 3 (Heckbürzel OMM & GNSS)
  ├─► PEITSCHE 4 (250 mm): AMP Superseal 1.5 4-Pin Buchse     ──► 12V Bordnetz (KL30, KL15, GND, Masse)
  └─► PEITSCHE 5 (250 mm): M8 4-Pin Buchse (A-kodiert, IP67) ──► CAN-Bus & IP67 Front-Mikrofon
```

---

## 10. Zukaufteile & Normteile-Einkaufsliste (COTS-Komponenten für 1 Komplettset)

| Bauteil | Spezifikation / Typ | Bezugsquelle / Hersteller | Menge | Montageort & Funktion |
| :--- | :--- | :--- | :---: | :--- |
| **M3 Gehäuseschrauben** | M3 x 40 mm Zylinderkopf V4A (DIN 912) | Normteil / Schrauben-Express | 4 Stk. | 4-Eck Zentralbox-Verschraubung |
| **M3 Gehäuseschrauben (Front)** | M3 x 20 mm Zylinderkopf V4A (DIN 912) | Normteil / Schrauben-Express | 4 Stk. | 4-Eck Front-Node Gehäuseverschraubung |
| **M2.5 Platinenschrauben** | M2.5 x 6 mm Zylinderkopf V4A (DIN 912) | Normteil / Schrauben-Express | 8 Stk. | 4x Zentralbox-Platine, 4x Front-Node-Platine |
| **M3 Gewindeeinsätze** | Ruthex M3 x 5.7 mm Messing (RX-M3x5.7) | Ruthex / Amazon | 8 Stk. | 4x Zentralbox Unterwanne, 4x Front-Node Unterwanne |
| **M4 Gewindeeinsätze** | Ruthex M4 x 8.1 mm Messing (RX-M4x8.1) | Ruthex / Amazon | 4 Stk. | Front-Node Gehäuseboden (AMPS-Lochbild 30 x 38 mm) |
| **M2 Schottwandschrauben** | M2 x 8 mm Senkkopf V4A (DIN 7991) | Normteil | 6 Stk. | Fixierung der 3 Pod-Schottwände (2x pro Pod) |
| **M5 Radar-Klemmschraube** | M5 x 25 mm V4A (DIN 912) + Hutmutter | Normteil | 1 Stk. | Klemmschraube für Pod 3 GoPro-Radar-Schwenkarm |
| **Auswerfer-Druckfedern** | Edelstahl V4A ($D=4{,}5\,\text{mm}, L_0=15\,\text{mm}, R=1{,}2\,\text{N/mm}$) | Gutekunst Federn / Sodemann | 6 Stk. | Auto-Eject Schnappmechanismus (2x pro Pod) |
| **Silentblöcke / Gummipuffer**| Typ A M4 Außen/Innen ($\varnothing 15 \times 10\,\text{mm}$) + Stoppmuttern | Ganter / Normteil | 4 Stk. | Schwingungsentkoppelte Rahmenmontage Zentralbox |
| **EPDM-Spannringe** | UV- & Ozonbeständiges EPDM ($\varnothing 45\dots 75\,\text{mm}$) | QuadLock / O-Ring-Shop | 6 Stk. | Rohrbett-Schnellmontage (Pods & Front-Node) |
| **EPDM-Dichtkämme (Front)** | EPDM Zellkautschuk geschlitzt ($15 \times 8 \times 4\,\text{mm}$) | Sonderfertigung / EPDM-Shop | 2 Stk. | Wasserdichte Flachkabel-Einführung im Front-Knoten |
| **Silikon-Dichtschnur** | Silikon-Rundschnur $\varnothing 1{,}5\,\text{mm}$ Shore 40A (1.0 m) | O-Ring-Shop | 1 Stk. | $40\,\text{cm}$ Zentralbox-Nut, $30\,\text{cm}$ Front-Node Deckelnut |
| **Kassetten-Flanschdichtungen**| Silikon-Formdichtung Shore 40A ($54 \times 18\,\text{mm}$) | Sonderfertigung / Silikon | 3 Stk. | Stirnseitige Mundloch-Abdichtung an Pod 1, 2 und 3 |
| **Silikon USB-C Schutzkappe** | Wasserdichte Schutzkappe mit Haltelasche | GCT / Amazon | 1 Stk. | IP67 Schutzabdeckung für Front-Node Port J2 |
| **Lenker-PTT Taster** | IP67 Taster (Schließer) mit Schelle ($\varnothing 22/28\,\text{mm}$) | Daytona / Oxford / APEM | 1 Stk. | Batteriefreier Lenker-PTT am Front-Knoten (Port J3) |
| **Gore Druckausgleichsventil** | Gore Automotive AVS 41 (M8x1.25 Schraubventil) | W. L. Gore & Associates | 1 Stk. | Zentralbox-Deckelbelüftung & Kondensatschutz |
| **Gore Klebemembranen** | Gore Adhesive Vent $\varnothing 6{,}0\,\text{mm}$ IP67 | W. L. Gore & Associates | 5 Stk. | 3x Pods, 1x Front-Node, 1x Knowles MEMS Akustikport |
| **PMMA Lichtleiter** | Bivar PLPC3-3MM ($\varnothing 3{,}0\,\text{mm}, L=8\,\text{mm}$) | Bivar / Mentor | 1 Stk. | Optische WS2812B Statusübertragung im Deckel |
| **3M Dual-Lock Klettband** | 3M Dual-Lock SJ3550 (Pilzkopfband, 25 mm breit) | 3M / Amazon | 25 cm | Vibrationsfeste Verkleidungsmontage für Ottocast & Node |
| **Pufferakku (LiPo USV)** | 1S LiPo (3.7V 1000mAh) mit 10k NTC & Molex Micro-Fit | EEMB / Enerpower | 1 Stk. | USV-Pufferung in der Zentralbox |
| **KFZ-Sicherungshalter** | Wasserdichter Mini-Flachsicherungshalter + **2A Sicherung** | Hella / MTA | 1 Stk. | Absicherung Dauerplus (KL30) direkt am Batteriepol |
| **HD26 Flanschbuchse & Stecker**| Amphenol LTW HD26 IP67 (Buchse + Stecker mit Tülle) | Amphenol LTW | 1 Satz | 26-Pin Hauptschnittstelle Box & Kabelbaum |
| **AMP Superseal 1.5 Buchse**| TE Connectivity 4-Pin Buchsengehäuse mit Kontakten | TE Connectivity | 1 Stk. | 12V Bordnetz-Einspeisung am Kabelbaum |
| **M8 Zuleitungskabel (Pods)** | M8 6-Pin A-Coded PUR geschirmt (1.0m / 1.5m) | Binder / Phoenix / Murr | 3 Stk. | Verbindung Kabelbaum-Pigtail zu Pod 1, 2 und 3 |
| **M8 Zuleitungskabel (Radar)**| M8 4-Pin A-Coded PUR geschirmt (1.0m) | Binder / Phoenix / Murr | 1 Stk. | Zuleitung zu Garmin Varia / mmWave Heckradar |
| **Automotive-Leitungen** | FLRY-B $0{,}5\,\text{mm}^2$ & $0{,}35\,\text{mm}^2$ (diverse Farben) | Leoni / Helukabel | nach Bed. | Fahrzeugkabelbaum nach `central_breakout_harness_wirelist.csv` |
| **Murata MM8030 Pigtails (Pod 3)**| Murata MM126036 auf SMA-Bulkhead IP67 (150 mm, RG-178)| Murata / Mouser | 3 Stk. | Koaxial-Bypass für J3 (2.4G), J4 (868M), J5 (GNSS) |
| **U.FL Pigtail (Front-Node)** | IPEX MHF1 / U.FL auf RP-SMA Bulkhead IP67 (150 mm, RG-178) | Taoglas / Molex | 1 Stk. | Koaxial-Zuleitung für ESP32-C3 externe Antenne |
| **SMA-Flansch-Doppelbuchse** | SMA-Buchse auf SMA-Buchse Bulkhead IP67 mit O-Ring & Mutter | Amphenol / Radiall | 1 Stk. | Wasserdichte HF-Durchführung in Kassetten-Frontblende (Klasse A) |
| **Koax-Pigtail intern (Kassette)**| RG-178 Koaxialkabel ($6\dots 10\,\text{cm}$, SMA-Stecker 90° auf SMA-Stecker)| Delock / Taoglas | 1 Stk. | HF-Verbindung von Sena +Mesh / OEM-Adapter zur Frontblende |
| **SMA IP67 Schutzkappen** | Messing vernickelt mit Dichtungs-O-Ring (Rändelkappe) | Amphenol / Radiall | 5 Stk. | Wasserdichter Schutz ungenutzter externer SMA-Buchsen (3x Heck, 1x Front, 1x Pod) |
| **Externe 2.4 GHz Mesh-Antenne**| 2.4 GHz Collinear Dipol (+5 dBi / +7 dBi) mit SMA-Stecker | Taoglas / Linx | 1 Stk. | Optionale High-Gain Antenne am Heck/Topcase |
| **Externe 868 MHz LoRa-Antenne**| 868 MHz Monopol / Dipol (+3 dBi / +5 dBi) mit SMA-Stecker | Linx ANT-868 / Taoglas | 1 Stk. | Optionale Long-Range Bergpass-Antenne |
| **Externe aktive GNSS-Antenne** | Aktiver Flachpuck (+28 dB LNA, 3.3V Phantomspeisung, SMA) | Taoglas AA.162 / Garmin | 1 Stk. | Optionale Dach-/Koffermontage bei verdecktem Heck |
| **USB-A Flachbandkabel (Front)**| USB-A Stecker/Kupplung kurz ($10\dots 15\,\text{cm}$, 90°-Winkel)| Delock / Amazon | 1 Stk. | Ottocast-Anbindung an J1 durch vorderen Dichtkamm |
| **USB-C Ladekabel (Handschuhf.)**| USB-C Stecker/Stecker ($1{,}0\,\text{m}$, 90°-Winkel, PUR)| Anker / Baseus | 1 Stk. | Smartphone-Ladekabel von J2 durch vorderen Dichtkamm |
| **JST-GH Crimpstecker-Set** | JST-GH 1.25mm 2-Pin Gehäuse + Crimpkontakte | JST / Mouser | 2 Sätze| Vorkonfektionierte Litzen für J3 (PTT) & J7 (12V) durch linken Kamm |
| **90° USB Kassetten-Kabel** | Ultraflaches 90°-Winkelkabel Micro-USB/USB-C ($5\dots 8\,\text{cm}$) | Delock / Amazon | 1 Stk. | 5V-Speisung für Sena +Mesh / MeshPort Adapter in Kassette |
| **EPDM Kassetten-Spannband** | Elastisches EPDM-Gummiband ($\approx 35 \times 10\,\text{mm}$) | Sonderfertigung / Sena | 1 Stk. | Vibrationssichere Arretierung des OEM-Adapters über Kassettennasen |

---

## 11. Benötigte Werkzeuge & Fertigungshilfsmittel (Werkstatt-Ausstattung)

Für die Montage aller 5 Baugruppen, die Kabelkonfektionierung und die Erstinbetriebnahme wird folgende Mindestausstattung an Werkzeugen und Montagechemie benötigt (Details siehe [Kapitel 14, Abschnitt 2.6](file:///Users/schmidtm/openMotorBridge/docs/de/14_build_instructions_assembly.md#26-kategorie-f-ben%C3%B6tigte-werkzeuge-messmittel--montagechemie)):

| Werkzeug-Kategorie | Enthaltene Werkzeuge & Spezifikation | Hauptzweck im OpenMotorBridge-Aufbau |
| :--- | :--- | :--- |
| **Mechanik & Schrauben** | Inbus 1,5 / 2,0 / 2,5 / 3,0 mm; Gabelschlüssel SW 7, 8, 10; Drehmomentschlüssel ($0{,}2 \dots 1{,}5\,\text{Nm}$) | Verzugsfreies Verschrauben aller Gehäuse, PCBAs und SMA-Buchsen |
| **Thermisches Fügen** | Lötstation ($200 \dots 450\,^\circ\text{C}$) mit Ruthex M3/M4 Einschmelzspitzen & feiner Lötspitze | Lotrechtes Einschmelzen der 12x Messinggewinde; Kabelbaumlötung |
| **Kabel- & Crimpmittel** | Fein-Crimpzange (Engineer PA-09 / IWISS IWS-2820M); Kfz-Crimpzange; Abisolierzange; Heißluftföhn | Konfektionierung von JST-SH (1.0 mm), JST-GH (1.25 mm) und Schrumpfschläuchen |
| **HF- & Feinelektronik** | ESD-Präzisionspinzette (abgewinkelt, kunststoffbeschichtet) | Zerstörungsfreies Aufstecken der Murata MM8030 und U.FL Koax-Stecker |
| **Montagechemie & Dichten**| OKS 1110 / Liqui Moly Silikonfett; Loctite 243 mittelfest; Peters Elpeguard Conformal Coating | IP67-Gleitdichtung, Vibrationssicherung und Feuchteschutz der Leiterplatten |
| **Prüf- & Flash-Hardware**| Digitalmultimeter; Labornetzteil mit Strombegrenzung ($12\,\text{V} / 150\,\text{mA}$); USB-C Datenkabel | Kurzschluss-Schutz, Spannungs-Check und Firmware-Flash aller 3 Controller |




