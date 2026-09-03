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

### 6.1 Druckdateien-Übersicht
* **Zentralbox:** `main_box_lower_case.stl`, `main_box_mid_tray.stl`, `main_box_lid.stl`.
* **Satelliten-Pods (3x):** `pod_base_housing.stl`, `03_pod_bulkhead_partition.stl`.
* **Kassetten:** `cartridge_base_sled.stl`, `cartridge_sena_sled.stl`, `cartridge_cardo_sled.stl`, `cartridge_omm_transceiver_sled.stl`, `cartridge_blindkassette_waterproof.stl`.
* **Front-Knoten:** `front_node_lower_case.stl`, `front_node_upper_case.stl`.

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
| **5. Universal Front-Knoten** | `05_smart_fairing_pcba_gerbers_jlcpcb.zip` | `05_smart_fairing_pcba_bom_jlcpcb.csv` | `05_smart_fairing_pcba_cpl_jlcpcb.csv` | **4 Lagen** (JLC04161H-7628) | **ENIG (Gold)**, 1.6 mm, TG150 |

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

## 10. Zukaufteile & Normteile-Einkaufsliste (COTS-Komponenten)

| Bauteil | Spezifikation / Typ | Bezugsquelle / Hersteller | Menge | Funktion |
| :--- | :--- | :--- | :---: | :--- |
| **M3 Gehäuseschrauben** | M3 x 40 mm Zylinderkopf V4A (DIN 912) | Normteil / Schrauben-Express | 4 Stk. | 4-Eck Zentralbox-Verschraubung |
| **M3 Gehäuseschrauben (Front)** | M3 x 20 mm Zylinderkopf V4A (DIN 912) | Normteil / Schrauben-Express | 4 Stk. | Front-Node Gehäuseverschraubung |
| **M3 Gewindeeinsätze** | Ruthex M3 x 5.7 mm Messing | Ruthex / Amazon | 8 Stk. | Einschmelzgewinde (Box & Front-Node) |
| **M4 Gewindeeinsätze** | Ruthex M4 x 8.1 mm Messing | Ruthex / Amazon | 4 Stk. | Einschmelzgewinde Front-Node AMPS-Boden |
| **M2 Schottwandschrauben** | M2 x 8 mm Senkkopf V4A (DIN 7991) | Normteil | 6 Stk. | Fixierung der 3 Pod-Schottwände |
| **Auswerfer-Druckfedern** | Edelstahl V4A ($D=4{,}5\,\text{mm}, L_0=15\,\text{mm}, R=1{,}2\,\text{N/mm}$) | Gutekunst Federn / Sodemann | 6 Stk. | Auto-Eject Mechanismus (2x pro Pod) |
| **EPDM-Spannringe** | UV- & Ozonbeständiges EPDM ($\varnothing 45\dots 75\,\text{mm}$) | QuadLock / O-Ring-Shop | 6 Stk. | Rohrbett-Schnellmontage (Pods & Front-Node) |
| **Gore Druckausgleichsventil** | Gore Automotive AVS 41 (M8x1.25) | W. L. Gore & Associates | 1 Stk. | Zentralbox-Deckelbelüftung |
| **Gore Klebemembranen** | Gore Adhesive Vent $\varnothing 6{,}0\,\text{mm}$ IP67 | W. L. Gore & Associates | 4 Stk. | Pod- & Front-Node Druckausgleich |
| **Pufferakku** | 1S LiPo (3.7V 1000mAh) mit NTC | EEMB / Enerpower | 1 Stk. | USV-Notstromversorgung |
| **M8 Zuleitungskabel** | M8 6-Pin A-Coded PUR geschirmt (1.0m / 1.5m)| Binder / Phoenix / Murr | 3 Stk. | Verbindung von Pigtail zu Pods |
