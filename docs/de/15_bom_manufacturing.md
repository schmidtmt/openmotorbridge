# 15 - BOM (Stückliste) & Fertigungsleitfaden

Vollständige Bauteilliste (Bill of Materials) und Fertigungsspezifikation für alle 4 Leiterplatten (PCBA) bei JLCPCB / Eurocircuits, vollständige Stückliste aller mechanischen 3D-Druck- und Montageelemente sowie Schritt-für-Schritt Inbetriebnahmeprotokoll.

---

## 1. Zentralbox Hauptplatine (`kicad_main_box` PCBA, 4-Layer FR4 TG150)

| Designator | Bauteil / MPN | Hersteller | Gehäuse | LCSC / JLCPCB Part # | Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | ESP32-S3-WROOM-1-N16R8 | Espressif Systems | SMD Modul | C2913200 | Haupt-MCU (Dual-Core, 16 MB Flash, 8 MB PSRAM) |
| **U2** | LM5164-Q1 | Texas Instruments | SOIC-8-EP | C2843477 | Automotive 65V Synchronous Buck Converter |
| **U3** | BQ24075RGTR / BQ25798 | Texas Instruments | VQFN-16 | C128509 | Dynamisches Power-Path Management & LiPo-Lader mit TS |
| **U4** | BMI270 | Bosch Sensortec | LGA-14 | C2838380 | 6-Achsen IMU für Schräglagen- & Bewegungserkennung |
| **U5** | ES8388 | Everest Semi | QFN-28 | C144547 | 24-Bit Stereo Audio Codec (I2S ADC/DAC) |
| **U6** | TCAN334GDCNR | Texas Instruments | SOT-23-8 | C842340 | 3.3V Automotive CAN-FD Transceiver (±58V Fault) |
| **T1, T2** | LM-NP-1001-B1L | Bourns Inc. | SMD Übertrager | C114402 | 1:1 Audio-Übertrager (1500 V RMS galvanische Trennung) |
| **OC1, OC2**| TLP222A(F) | Toshiba | SOP-4 | C112444 | Halbleiter-PhotoMOS-Relais für PTT-Tastensimulation |
| **D1** | SMBJ33CA | Littelfuse | DO-214AA (SMB) | C87848 | TVS-Diode (33 V Standoff, 53.3 V max Clamping) |
| **F1** | MF-MSMF050-2 | Bourns | 1812 SMD | C22668 | Rückstellbare PPTC-Sicherung (500 mA Hold / 1.0 A Trip) |
| **LED1** | WS2812B-B | Worldsemi | 5050 SMD | C114586 | RGB Status-LED für optische Betriebsmodusanzeige |
| **LP1** | PLPC3-3MM / 1292.1101 | Bivar / Mentor | Ø 3.0 mm PMMA | Mechanik | IP67 Lichtleiter mit O-Ring im Gehäusedeckel |
| **VENT1** | AVS 41 | Gore Automotive | M8 x 1.25 Schraub | Mechanik | ePTFE Druckausgleichselement (IP67 / 120 ml/min) |
| **MIC1** | SPH0645LM4H / SiSonic | Knowles | 3.5x2.65 mm SMD | C119850 | IP67 Front Ambient-Mikrofon mit ePTFE Membran (Pin 25) |
| **J1** | 2x13 Wannenstecker | Standard 2.54 mm | THT Box Header | C2934175 | Interner Pfostenverbinder zur HD26-Flanschbuchse |
| **J2** | MicroSD Slot Push-Push | Molex / Korean Hro | SMD Push-Push | C266624 | 4-Bit SDIO Speicherkarte für Tour-Logging |
| **J_BAT** | Molex Micro-Fit 3.0 2P | Molex | SMD Header | C289110 | Steckverbindung zum 18650 LiFePO4 Pufferakku |
| **CN1** | HD26 Buchse IP67 | Amphenol LTW | Flansch D-Sub | Kundenteil | Wasserdichte 26-polige Gehäuseschnittstelle |

---

## 2. Pod-Basisplatine (`openmotorbridge_pod_base` PCBA, 2-Layer FR4 ENIG)

| Designator | Bauteil / MPN | Hersteller | Gehäuse | LCSC / JLCPCB Part # | Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **J1** | PinHeader_1x06_P2.54mm_SMD | Harwin / Wurth | SMD Vertikal | C2934176 | Zentrierte 6-Pin Stiftleiste im Schottwand-Schutzkragen |
| **J2** | M8_6PIN_RECEPTACLE (A-Coded)| Binder / Phoenix | M8 Rundsteckverbinder | C289100 | M8 6-Pin IP67 Buchse zur Heck-/Helm-Verkabelung (B.Cu) |
| **U1** | SP3012-06UTG | Littelfuse | DFN-14 (3.5x1.35mm)| C2834580 | 6-Kanal Ultra-Low-Cap ESD-Schutzarray (< 0.5 pF) |
| **C1** | 100nF 50V X7R | Samsung / Yageo | 0603 SMD | C14663 | Entkopplungskondensator für 5V Versorgungsspannung |
| **H1, H2** | 2x M2 Montagelöcher | - | Bohrung Ø 2.2 mm | - | Rüttelsichere Verschraubung an der PA12-Schottwand |

---

## 3. Universelle Kassetten-Trägerplatine (`openmotorbridge_pod_cartridge` PCBA, 2-Layer FR4)

| Designator | Bauteil / MPN | Hersteller | Gehäuse | LCSC / JLCPCB Part # | Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **J1** | PinSocket_1x06_P2.54mm_SMD | Harwin / Samtec | SMD Horizontal | C2934177 | Stirnseitige 6-Pin Präzisionsbuchse (Kolbeneinschub) |
| **J2** | JST-SH 1.0mm 6-Pin Horizontal| JST | SMD Liegend | C136657 | Flachbandkabel-Anschluss zum Headset-Inlay |
| **U1** | DS2401Z+ | Maxim / ADI | SOT-223 / SOT-23 | C2834570 | 64-Bit 1-Wire Silicon Serial ROM (Kassetten-Identifikation)|
| **F1** | MF-MSMF050-2 (500mA) | Bourns | 1812 / 1206 SMD | C22668 | Rückstellbare PPTC-Sicherung für 5V Kassettenstromkreis |
| **D1** | Grüne 5V Power-LED | Everlight | 0805 SMD | C2297 | Optische Betriebsanzeige für 5V Stromversorgung |
| **R1** | 1.0 kΩ 1% | Yageo | 0603 SMD | C21190 | Vorwiderstand für Status-LED D1 |
| **D2** | SP3012-06UTG / IP4220CZ6 | Littelfuse / Nexperia| DFN-14 / SOT-457 | C2834580 | 6-Kanal ESD-Schutzmatrix für interne Audio- & Datenleitungen|

---

## 4. Heck-Pod 3 Transceiver-Platine (`openmotorbridge_rear_pod3` PCBA, 4-Layer FR4 TG150)

| Designator | Bauteil / MPN | Hersteller | Gehäuse | LCSC / JLCPCB Part # | Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U10** | ESP32-C3-WROOM-02-N4 | Espressif Systems | SMD Modul | C2868705 | 32-Bit RISC-V Co-Prozessor & 2.4 GHz Primary Mesh (Opus 24k) |
| **U11** | MAX-M10S-00B | u-blox | LGA-18 | C3006240 | Multi-Konstellation GNSS Engine (10 Hz, 1-PPS) |
| **U12** | SX1262IMLTRT | Semtech | QFN-24 | C190184 | Secondary Fallback 868 MHz LoRa Transceiver (+22 dBm) |
| **U13** | DS2401Z+ | Maxim / ADI | SOT-223 / SOT-23 | C2834570 | 64-Bit 1-Wire Silicon Serial Number ID |
| **U14** | TPS7A0533PDBVR | Texas Instruments | SOT-23-5 | C505293 | Ultra-Low-Noise 3.3V LDO (200 mA) für GNSS & LoRa |
| **J1** | PinSocket_1x06_P2.54mm_SMD | Harwin / Samtec | SMD Horizontal | C2934177 | Stirnseitige 6-Pin Präzisionsbuchse (Kolbeneinschub) |
| **F1** | MF-MSMF050-2 (500mA) | Bourns | 1812 SMD | C22668 | Rückstellbare PPTC-Sicherung für 5V Stromversorgung |
| **D1** | Grüne 5V Power-LED | Everlight | 0805 SMD | C2297 | Status-LED für 5V Versorgungsspannung |
| **ANT1** | GP.1575.25.4.A.02 | Taoglas | 25x25x4 mm Patch | C2689100 | Keramik-Patchantenne für GPS/Galileo/BeiDou |
| **ANT2** | ANT-868-CW-HWR-SMA | Linx / Taoglas | Wendelantenne | C290111 | 868 MHz Wendelantenne für Heckbürzel-LoRa |
| **ANT3** | WLS.01.A.02 | Taoglas | 3.2x1.6 mm Chip | C2838381 | 2.4 GHz Keramik-Antenne für Primary HiFi Mesh |

---

## 5. Mechanik- & Gehäuse-BOM (3D-Druck MJF PA12 & Montageelemente)

### 5.1 Zentralbox (3-teiliges Sandwich-Gehäuse Typ A)
| Bauteil / Baugruppe | Material / Spezifikation | CAD / STL Datei | Menge | Funktion |
| :--- | :--- | :--- | :---: | :--- |
| **Unterwanne** | PA12 MJF Schwarz | `main_box_lower_case.stl` | 1 | Monocoque-Grundgehäuse mit Dichtnut & 4x M4 Silentblock-Ohren |
| **Oberwanne mit Zwischenboden**| PA12 MJF Schwarz | `main_box_upper_case.stl` | 1 | Akku-Halterung, 11x Konvektionsschlitze, HD26-Flansch, USB-C & LED |
| **Gehäusedeckel** | PA12 MJF Schwarz | `main_box_lid.stl` | 1 | Homogener Verschlussdeckel mit ePTFE-Ventilsitz |
| **Gehäuseschrauben** | Edelstahl V4A M3 x 40 mm DIN 912 | Normteil | 4 | Durchgehende 4-Eck-Verschraubung |
| **Gewindeeinsätze** | Messing M3 Ruthex / Tappex | Normteil | 4 | Eingeschmolzen in Unterwanne |
| **Druckausgleichselement** | Gore Automotive AVS 41 (M8) | Zukaufteil | 1 | IP67 Druckausgleich & Kondensatvermeidung |
| **Gehäusedichtung** | Silikon Shore 50A (1.5 mm Schnur) | Formdichtung | 1 | Hermetische IP67/IP69K Sandwich-Abdichtung |
| **Lichtleiter** | PMMA Ø 3.0 mm (Bivar PLPC3) | Zukaufteil | 1 | Statusanzeige WS2812B im Gehäusedeckel |

### 5.2 Universelle Satelliten-Pods (3x identisch für Pod 1, 2 und 3)
| Bauteil / Baugruppe | Material / Spezifikation | CAD / STL Datei | Menge | Funktion |
| :--- | :--- | :--- | :---: | :--- |
| **Pod-Monocoque-Schacht** | PA12 MJF Schwarz | `pod_base_housing.stl` | 3 | 5-seitiges Schachtgehäuse mit V-Rohrbett & 4x EPDM-Spannbandnasen |
| **Schutz-Schottwand** | PA12 MJF Schwarz | `03_pod_bulkhead_partition.stl` | 3 | Schottwand mit 6-Pin Schutzkragen & Federsitzen |
| **Auswerfer-Druckfedern** | Edelstahl V4A (D=4.5mm, L0=15mm)| Normteil | 6 | Auto-Eject Mechanismus (9 mm Kassettenauswurf) |
| **Schottwandschrauben** | Edelstahl V4A M2 x 8 mm Senkkopf | Normteil | 6 | 2x Schrauben zur Schottwandfixierung pro Pod |

### 5.3 Modulare Wechselkassetten & Inlays
| Bauteil / Baugruppe | Material / Spezifikation | CAD / STL Datei | Menge | Funktion |
| :--- | :--- | :--- | :---: | :--- |
| **Universal-Grundschlitten** | PA12 MJF Schwarz | `cartridge_base_sled.stl` | 3 | Universeller Trägerschlitten mit Führungsfedern & Snap-Fit |
| **Sena 50S/60S Kassetten-Schlitten** | PA12 MJF Schwarz | `cartridge_sena_sled.stl` | 1 | Sena Kassetten-Schlitten mit Jog-Dial Arretierung |
| **Cardo Edge Kassetten-Schlitten**| PA12 MJF Schwarz | `cartridge_cardo_sled.stl` | 1 | Cardo Kassetten-Schlitten mit 2x N52 Magnetsitzen |
| **OMM Transceiver-Schlitten** | PA12 MJF Schwarz | `cartridge_omm_transceiver_sled.stl`| 1 | 1-teiliger Schlitten für direkte Pod 3 Platine |
| **IP67 Blindkassette (Dry Box)**| PA12 MJF Schwarz | `cartridge_blindkassette_waterproof.stl` | 1 | Hermetischer Dummy mit Notfall-Staufach |
| **Kassetten-Flanschdichtungen**| Shore 40A Silikon Formdichtung | Zukaufteil / Formteil| 3 | Umlaufende IP67-Abdichtung an Stirnblende |
| **ePTFE Druckausgleichsmembran**| Gore Adhesive Vent Ø 7.0 mm | Zukaufteil | 3 | Pneumatischer Ausgleich auf Gehäuse-Oberseite |

---

## 6. Fertigungshinweise, Schutzlackierung & Vibrationshärtung

### 6.1 Schutzlackierung nach IPC-CC-830B (Conformal Coating)
* **Lackmaterial:** Modifizierter Polyurethan-Schutzlack (*Peters Elpeguard SL 1307 FLZ* oder *Electrolube UR5041*).
* **Schichtdicke:** $40\,\mu\text{m}$ bis $60\,\mu\text{m}$ (Durchschlagfestigkeit $> 60\,\text{kV/mm}$ gegen Betauung und Salznebel).
* **Maskierungszonen:** MicroSD-Kartenkontakte, SMD-Testpunkte (TP1–TP8), ePTFE-Ventil-Öffnung, 6-Pin Präzisionskontakte.

### 6.2 Vibrationsdämpfung nach ISO 16750-3 (Motorrad-Schwingungsprüfung)
* **PCB-Entkopplung:** 4x NBR-O-Ringe (3.0 mm Innendurchmesser, 1.0 mm Schnurstärke) zwischen Gehäusedomen und PCB-Unterseite.
* **Schraubensicherung:** M2.5 Platinschrauben mit Anzugsmoment $0{,}35\,\text{Nm}$ und mittelfestem Sicherungslack (*Loctite 243* blau).
* **Bauteil-Underfill:** Bourns LM-NP-1001 Übertrager-Ecken mit elastischem Silikonkleber (*Dow Corning 732* / *Dowsil 3145*) am PCB gesichert.
* **Pufferakku-Fixierung:** $1{,}0\,\text{mm}$ Dämpfungspolster (*3M VHB 4910* / EPDM) und elastisches EPDM-Gummispannband (Shore 50A) in der Oberwanne auf dem Zwischenboden.

---

## 7. Inbetriebnahme-, Mess- & Testprotokoll (Schritt-für-Schritt)

### Schritt 1: Visuelle Inspektion (Vor dem ersten Einschalten)
* [ ] Lötbrücken unter U2 (LM5164), U3 (BQ24075) und U5 (ES8388) mit Mikroskop/Lupe ausschließen.
* [ ] Polarität der TVS-Diode D1 (SMBJ33CA) und des P-FET Verpolschutzes kontrollieren.
* [ ] Prüfen, ob die 2,5 mm Isolationsbarriere um T1/T2 und OC1/OC2 frei von Zinnresten oder Flussmittel ist.

### Schritt 2: Spannungsprüfung & Strombegrenzung
* [ ] Labornetzteil auf $12{,}0\,\text{V DC}$ einstellen, Strombegrenzung auf $150\,\text{mA}$.
* [ ] Ruhestrom messen: Sollwert $= 45\,\text{mA}$ bis $75\,\text{mA}$ (ohne Akkuladung).
* [ ] Prüfpunkt `TP_5V`: Sollwert $= 5{,}15\,\text{V} \pm 0{,}05\,\text{V}$.
* [ ] Prüfpunkt `TP_3V3`: Sollwert $= 3{,}30\,\text{V} \pm 0{,}02\,\text{V}$.

### Schritt 3: Flashen & System-Selbsttest
* [ ] ESP-IDF / PlatformIO Flash via nativem USB-C Port ausführen (`firmware/main_controller/`).
* [ ] LittleFS-Partition formatieren und Profile aus `firmware/main_controller/data/profiles/` hochladen.
* [ ] Serielle Konsole ($115.200\,\text{Baud}$): Meldungen "LittleFS Mount OK", "1-Wire Manager Task OK", "I2S ES8388 Codec Init OK", "TCAN334G CAN-FD OK" verifizieren.

### Schritt 4: Audio- & Ducking-Funktionstest
* [ ] $1\,\text{kHz}$ Sinuston ($1{,}0\,\text{V}_{\text{RMS}}$) an Audio-Input anlegen.
* [ ] Oszilloskop an `PORT1_AUDIO_OUT`: Überprüfen, ob das Signal innerhalb von $15\,\text{ms}$ weich gedämpft wird.
* [ ] Signal abschalten: Prüfen, ob nach $600\,\text{ms}$ Hold-Zeit die weiche $250\,\text{ms}$-Raised-Cosine-Rückkehr erfolgt.

### Schritt 5: IP67-Dichtheitsprüfung
* [ ] Montiertes Gehäuse in Vakuumkammer bei $-20\,\text{kPa}$ Unterdruck für 60 Sekunden halten (Druckverlust $< 0{,}5\,\text{kPa}$).

---

## 8. Schritt-für-Schritt Bestellleitfaden für JLCPCB (PCBA & SMT-Bestückung)

Alle fertigen Produktionspakete werden mit dem Master-Skript `python3 hardware/scripts/export_manufacturing_packages.py` vollautomatisch in das Verzeichnis [hardware/production_packages/](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/) exportiert.

### 8.1 Checkliste für den JLCPCB-Upload (Alle 5 Leiterplatten)

| Baugruppe / PCBA | Gerber-ZIP Datei | BOM CSV Datei | CPL (Pick & Place) CSV | Lagen & Stackup | Oberfläche & Dicke |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **1. Zentralbox Hauptplatine** | `01_main_box_pcba_gerbers_jlcpcb.zip` | `01_main_box_pcba_bom_jlcpcb.csv` | `01_main_box_pcba_cpl_jlcpcb.csv` | **4 Lagen** (JLC04161H-7628) | **ENIG (Gold)**, 1.6 mm, TG150 |
| **2. Pod-Basisplatine** | `02_pod_base_pcba_gerbers_jlcpcb.zip` | `02_pod_base_pcba_bom_jlcpcb.csv` | `02_pod_base_pcba_cpl_jlcpcb.csv` | **2 Lagen** (Standard) | **ENIG (Gold)**, 1.6 mm |
| **3. Kassetten-Trägerplatine** | `03_pod_cartridge_pcba_gerbers_jlcpcb.zip` | `03_pod_cartridge_pcba_bom_jlcpcb.csv` | `03_pod_cartridge_pcba_cpl_jlcpcb.csv` | **2 Lagen** (Standard) | **ENIG (Gold)**, 1.2 mm |
| **4. Heck-Pod 3 Transceiver** | `04_rear_pod3_pcba_gerbers_jlcpcb.zip` | `04_rear_pod3_pcba_bom_jlcpcb.csv` | `04_rear_pod3_pcba_cpl_jlcpcb.csv` | **4 Lagen** (JLC04161H-7628) | **ENIG (Gold)**, 1.6 mm, TG150 |
| **5. Smart Fairing Hub** | `05_smart_fairing_pcba_gerbers_jlcpcb.zip` | `05_smart_fairing_pcba_bom_jlcpcb.csv` | `05_smart_fairing_pcba_cpl_jlcpcb.csv` | **4 Lagen** (JLC04161H-7628) | **ENIG (Gold)**, 1.6 mm, TG150 |

### 8.2 Auszufüllende Optionen im JLCPCB-Webkonfigurator:
1. **PCB Order:**
   * **Base Material:** FR-4 (TG150 für Zentralbox & Pod 3).
   * **Surface Finish:** **ENIG (Electroless Nickel Immersion Gold)** – zwingend erforderlich für korrosionsbeständige Schleifkontakte und vibrationsfeste QFN-Lötstellen.
   * **Solder Mask Color:** Beliebig (Standard: Matt-Schwarz oder Grün).
   * **Via Covering:** *Tented* oder *Filled & Capped* (unter BGA/QFN EP-Pads).
2. **SMT Assembly:**
   * Häkchen bei **"PCB Assembly"** setzen.
   * **Assembly Side:** *Top Side* (bzw. *Both Sides* für Zentralbox).
   * **BOM & CPL hochladen:** Die generierten `*_bom_jlcpcb.csv` und `*_cpl_jlcpcb.csv` hochladen.
   * **DFM-Vorschau prüfen:** Im visuellen CPL-Viewer die Ausrichtung von Pin 1 (Bourns-Übertrager T1/T2, Optokoppler OC1/OC2, ESP32-S3) kontrollieren und ggf. Rotation bestätigen.

---

## 9. Fertigung des zentralen Kabelbaums (HD26-Breakout-Pigtail)

Der zentrale Kabelbaum verbindet die unter der Sitzbank montierte Zentralbox mit den 3 Pod-Anschlüssen, der Bordspannung und dem CAN-Bus / Front-Mikrofon.

### 9.1 Auftragsfertigung (z. B. JLCPCB Wire Harness / Cabelcon / Sinohand)
Für eine professionelle Fertigung wird die Datei [central_breakout_harness_wirelist.csv](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/05_wiring_harness/central_breakout_harness_wirelist.csv) direkt an den Konfektionär übergeben.

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

### 9.2 DIY-Bauanleitung für den Prototypen-Kabelbaum (Werkbank-Aufbau):
1. **Materialien bereitstellen:**
   * 1x HD26 D-Sub Stecker mit Lötkelchen und IP67-Metallhaube.
   * 3x M8 6-Pin Buchsen-Pigtails (25 cm langes Kabel mit einseitig offener Litze).
   * 1x M8 4-Pin Buchsen-Pigtail (für CAN/Mikrofon).
   * 1x AMP Superseal 1.5 4-Pin Buchsengehäuse mit Crimpkontakten.
   * Schrumpfschlauch mit Heißschmelzkleber (Innenkleber).
2. **Löten nach Pinout-Tabelle:**
   * Die Adern gemäß Tabelle aus [central_breakout_harness_wirelist.csv](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/05_wiring_harness/central_breakout_harness_wirelist.csv) an die Lötkelche 1 bis 26 des HD26-Steckers anlöten.
   * Audio-Adernpaare (Pins 3/4 und Pins 9/10) sowie CAN-Adern (Pins 23/24) jeweils paarig verdrillen.
3. **Zugentlastung & Versiegelung:**
   * Die Lötkelche im HD26-Gehäuse mit Silikonkautschuk / Heißkleber vergießen.
   * Die Rändelschrauben der IP67-Haube festziehen und den Ausgang mit 3:1 Schrumpfschlauch abdichten.

---

## 10. 3D-Druck-Auftrag (HP Multi Jet Fusion PA12)

Alle 3D-Druckdaten liegen gebündelt als ZIP-Pakete im Ordner [hardware/production_packages/06_3d_print_mjf_stls/](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/06_3d_print_mjf_stls/):

### 10.1 Bestellpakete:
1. **`01_main_box_3d_print_mjf.zip`:**
   * `main_box_lower_case.stl` (1x)
   * `main_box_mid_tray.stl` (1x)
   * `main_box_lid.stl` (1x)
2. **`02_satellite_pods_3d_print_mjf.zip`:**
   * `pod_base_housing.stl` (3x – für Pod 1, 2 und 3)
3. **`03_cartridges_and_inlays_3d_print_mjf.zip`:**
   * `cartridge_base_sled.stl` (3x)
   * `cartridge_sena_sled.stl` (1x)
   * `cartridge_cardo_sled.stl` (1x)
   * `cartridge_omm_transceiver_sled.stl` (1x)
   * `cartridge_blindkassette_waterproof.stl` (1x)

### 10.2 Materialempfehlung:
* **Verfahren:** **HP Multi Jet Fusion (MJF)** oder **SLS (Selective Laser Sintering)**.
* **Material:** **PA12 (Polyamid 12) Schwarz**, kugelgestrahlt (*bead blasted*).
* **Finish / Veredelung:** **Chemische Dampfglättung (*Vapor Smoothing / Chemical Polish*)** – versiegelt die Poren zu 100% gegen Benzin, Bremsflüssigkeit, Kettenöl und Hochdruckwasser (IP69K).

---

## 11. Zukaufteile & Normteile-Einkaufsliste (COTS-Komponenten)

| Bauteil | Spezifikation / Typ | Bezugsquelle / Hersteller | Menge | Funktion |
| :--- | :--- | :--- | :---: | :--- |
| **M3 Gehäuseschrauben** | M3 x 40 mm Zylinderkopf V4A (DIN 912) | Normteil / Schrauben-Express | 4 Stk. | 4-Eck Zentralbox-Verschraubung |
| **M3 Gewindeeinsätze** | Ruthex M3 x 5.7 mm Messing | Ruthex / Amazon | 4 Stk. | Einschmelzgewinde in Unterwanne |
| **M2 Schottwandschrauben** | M2 x 8 mm Senkkopf V4A (DIN 7991) | Normteil | 6 Stk. | Fixierung der 3 Pod-Schottwände |
| **Auswerfer-Druckfedern** | Edelstahl V4A ($D=4{,}5\,\text{mm}, L_0=15\,\text{mm}, R=1{,}2\,\text{N/mm}$) | Gutekunst Federn / Sodemann | 6 Stk. | Auto-Eject Mechanismus (2x pro Pod) |
| **EPDM-Spannringe / Leiterbänder**| UV- & Ozonbeständiges EPDM ($\varnothing 45\dots 75\,\text{mm}$) | QuadLock / O-Ring-Shop / Amazon | 6 Stk. | Universal-Rohrbett-Schnellmontage (2x pro Pod) |
| **UV-Kabelbinder (Diebstahlschutz)**| $4{,}8 \times 200\,\text{mm}$ Polyamid 6.6 Schwarz | HellermannTyton / Würth | 6 Stk. | Permanente Festmontage an Rahmenrohren |
| **Gore Druckausgleichsventil** | Gore Automotive AVS 41 (M8x1.25) | W. L. Gore & Associates | 1 Stk. | Zentralbox-Deckelbelüftung |
| **Gore Klebemembranen** | Gore Adhesive Vent $\varnothing 6{,}0\,\text{mm}$ IP67 | W. L. Gore & Associates | 3 Stk. | Pod-Druckausgleich (1x pro Pod) |
| **Lichtleiter** | PMMA $\varnothing 3{,}0\,\text{mm}$ (Bivar PLPC3-3MM) | Bivar / Mouser / Digikey | 1 Stk. | LED-Statusfenster im Deckel |
| **Pufferakku** | 18650 LiFePO4 (3.2V 1500mAh) / LiPo 1S | EEMB / Enerpower | 1 Stk. | USV-Notstromversorgung |
| **M8 Verlängerungskabel** | M8 6-Pin A-Coded PUR geschirmt (1.0m / 1.5m)| Binder / Phoenix / Murr / LCSC | 3 Stk. | Verbindung von Pigtail zu Pods |

