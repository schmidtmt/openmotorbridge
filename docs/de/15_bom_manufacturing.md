# 15 - BOM (Stueckliste) & Fertigungsleitfaden

Vollstaendige Bauteilliste (Bill of Materials) und Fertigungsspezifikation fuer die SMT-Bestueckung (PCBA) bei JLCPCB / Eurocircuits sowie Schritt-fuer-Schritt Inbetriebnahmeprotokoll.

---

## 1. Zentralbox Hauptplatine (Main Box PCBA)

| Designator | Bauteil / MPN | Hersteller | Gehaeuse | LCSC / JLCPCB Part # | Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | ESP32-S3-WROOM-1-N16R8 | Espressif Systems | SMD Modul | C2913200 | Haupt-MCU (Dual-Core, 16 MB Flash, 8 MB PSRAM) |
| **U2** | LM5164-Q1 | Texas Instruments | SOIC-8-EP | C2843477 | Automotive 65V Synchronous Buck Converter |
| **U3** | BQ24075RGTR | Texas Instruments | VQFN-16 | C128509 | Dynamisches Power-Path Management & LiPo-Lader mit TS |
| **U4** | BMI270 | Bosch Sensortec | LGA-14 | C2838380 | 6-Achsen IMU fuer Schraeglagen- & Bewegungserkennung |
| **U5** | ES8388 | Everest Semi | QFN-28 | C144547 | 24-Bit Stereo Audio Codec (I2S ADC/DAC) |
| **U6** | TCAN334GDCNR | Texas Instruments | SOT-23-8 | C842340 | 3.3V Automotive CAN-FD Transceiver (±58V Fault) |
| **T1, T2** | LM-NP-1001-B1L | Bourns Inc. | SMD Uebertrager | C114402 | 1:1 Audio-Uebertrager (1500 V RMS galvanische Trennung) |
| **OC1, OC2**| TLP222A(F) | Toshiba | SOP-4 | C112444 | Halbleiter-PhotoMOS-Relais fuer PTT-Tastensimulation |
| **D1** | SMBJ33CA | Littelfuse | DO-214AA (SMB) | C87848 | TVS-Diode (33 V Standoff, 53.3 V max Clamping) |
| **F1** | MF-MSMF050-2 | Bourns | 1812 SMD | C22668 | Rueckstellbare PPTC-Sicherung (500 mA Hold / 1.0 A Trip) |
| **LED1** | WS2812B-B | Worldsemi | 5050 SMD | C114586 | RGB Status-LED fuer optische Betriebsmodusanzeige |
| **LP1** | PLPC3-3MM / 1292.1101 | Bivar / Mentor | Ø 3.0 mm PMMA | Mechanik | IP67 Lichtleiter mit O-Ring im Gehaeusedeckel |
| **VENT1** | AVS 41 | Gore Automotive | M8 x 1.25 Schraub | Mechanik | ePTFE Druckausgleichselement (IP67 / 120 ml/min) |
| **MIC1** | SPH0645LM4H / SiSonic | Knowles | 3.5x2.65 mm SMD | C119850 | IP67 Front Ambient-Mikrofon mit ePTFE Membran (Pin 25) |
| **CN_M8** | M8 3-Pin Buchse IP67 | Binder / Phoenix | M8 Rundsteckverbinder | C289100 | Wasserdichter Kabelbaum-Steckabzweig fuer Front-Mikrofon |
| **J1** | 2x13 Wannenstecker | Standard 2.54 mm | THT Box Header | C2934175 | Interner Pfostenverbinder zur HD26-Flanschbuchse |
| **J2** | MicroSD Slot Push-Push | Molex / Korean Hro | SMD Push-Push | C266624 | 4-Bit SDIO Speicherkarte fuer Tour-Logging |
| **CN1** | HD26 Buchse IP67 | Amphenol LTW | Flansch D-Sub | Kundenteil | Wasserdichte 26-polige Gehaeuseschnittstelle |

---

## 2. Heck-Pod 3 Transceiver-Platine (Rear Pod 3 PCBA)

| Designator | Bauteil / MPN | Hersteller | Gehaeuse | LCSC / JLCPCB Part # | Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U10** | ESP32-C3-WROOM-02-N4 | Espressif Systems | SMD Modul | C2868705 | 32-Bit RISC-V Co-Prozessor & 2.4 GHz Primary Mesh (Opus 24k) |
| **U11** | MAX-M10S-00B | u-blox | LGA-18 | C3006240 | Multi-Konstellation GNSS Engine (10 Hz, 1-PPS) |
| **U12** | SX1262IMLTRT | Semtech | QFN-24 | C190184 | Secondary Fallback 868 MHz LoRa Transceiver (+22 dBm) |
| **U13** | DS2401Z+ | Maxim / ADI | SOT-223 / TO-92 | C14440 | 64-Bit 1-Wire Silicon Serial Number ID |
| **U14** | TPS7A0533PDBVR | Texas Instruments | SOT-23-5 | C505293 | Ultra-Low-Noise 3.3V LDO (200 mA) fuer GNSS & LoRa |
| **ANT1** | GP.1575.25.4.A.02 | Taoglas | 25x25x4 mm Patch | C2689100 | Keramik-Patchantenne fuer GPS/Galileo |
| **ANT2** | ANT-868-CW-HWR-SMA | Linx / Taoglas | Wendelantenne | C290111 | 868 MHz Wendelantenne fuer Heckbuerzel |
| **ANT3** | WLS.01.A.02 | Taoglas | 3.2x1.6 mm Chip | C2838381 | 2.4 GHz Keramik-Antenne fuer Primary HiFi Mesh |
| **CN3** | 824-22-006-00-001101 | Mill-Max | SMD Pad Header | C189201 | 6-poliges vergoldetes Pogo-Zielkontakt-Array |

---

## 3. Universelle Pod-Kassette & Blindkassette (Pod 1 & Pod 2 Cartridge PCBA)

| Designator | Bauteil / MPN | Hersteller | Gehaeuse | LCSC / JLCPCB Part # | Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U20** | DS2401Z+ | Maxim / ADI | SOT-223 | C14440 | 64-Bit 1-Wire Silicon Serial Number (Kassetten-ID) |
| **D20** | IP4220CZ6 | Nexperia | SOT-457 | C119330 | 4-Kanal ESD-Schutzarray fuer Audio- und Opto-Leitungen |
| **CN2** | 824-22-006-00-001101 | Mill-Max | SMD Pad Header | C189201 | 6-poliges vergoldetes Pogo-Zielkontakt-Array |
| **DUMMY1** | Pod_Dummy_Cartridge_IP67.stl | OpenMotorBridge | PA12 MJF 3D-Druck | Mechanik | IP67 Blind-Kassette fuer unbestueckte Schacht-Plaetze |

---

## 4. Fertigungshinweise, Schutzlackierung & Vibrationshaertung

### 4.1 Schutzlackierung nach IPC-CC-830B (Conformal Coating)
* **Lackmaterial:** Modifizierter Polyurethan-Schutzlack (*Peters Elpeguard SL 1307 FLZ* oder *Electrolube UR5041*).
* **Schichtdicke:** $40\,\mu\text{m}$ bis $60\,\mu\text{m}$ (Durchschlagfestigkeit $> 60\,\text{kV/mm}$ gegen Betauung und Salznebel).
* **Maskierungszonen:** MicroSD-Kartenkontakte, SMD-Testpunkte (TP1–TP8), ePTFE-Ventil-Oeffnung.

### 4.2 Vibrationsdaempfung nach ISO 16750-3 (Motorrad-Schwingungspruefung)
* **PCB-Entkopplung:** 4x NBR-O-Ringe (3.0 mm Innendurchmesser, 1.0 mm Schnurstaerke) zwischen Gehaeusedomen und PCB-Unterseite.
* **Schraubensicherung:** M2.5 Platinschrauben mit Anzugsmoment $0{,}35\,\text{Nm}$ und mittelfestem Sicherungslack (*Loctite 243* blau).
* **Bauteil-Underfill:** Bourns LM-NP-1001 Uebertrager-Ecken mit elastischem Silikonkleber (*Dow Corning 732* / *Dowsil 3145*) am PCB gesichert.
* **Pufferakku-Fixierung:** Vollflaechiges Acrylat-Schaum-Klebeband (*3M VHB 4910*, 1.0 mm Dicke) in der Oberwanne.

### 4.3 CPL-Ausrichtung & Gehaeuse
- **CPL-Rotationsabgleich:** Bei der automatisierten Bestueckung ist auf die Pin-1-Ausrichtung der Bourns-Uebertrager (T1, T2), Optokoppler (OC1, OC2) und der QFN-ICs (ES8388, SX1262) zu achten.
- **Gehaeusefertigung:** HP Multi Jet Fusion (MJF) in PA12 Schwarz, kugelgestrahlt und mit Heissbad-Dampfversiegelung gegen Benzin/Oel.
- **Dichtungen:** Massgefertigte Silikon-Formdichtungen (Shore-Haerte 50 A) fuer IP67-Deckel und Kassetten-Einschuebe.

---

## 5. Inbetriebnahme-, Mess- & Testprotokoll (Schritt-fuer-Schritt)

### Schritt 1: Visuelle Inspektion (Vor dem ersten Einschalten)
* [ ] Loetbruecken unter U2 (LM5164), U3 (BQ24075) und U5 (ES8388) mit Mikroskop/Lupe ausschliessen.
* [ ] Polaritaet der TVS-Diode D1 (SMBJ33CA) und des P-FET Verpolschutzes kontrollieren.
* [ ] Pruefen, ob die 2,0 mm Isolationsbarriere um T1/T2 und OC1/OC2 frei von Zinnresten oder Flussmittel ist.

### Schritt 2: Spannungspruefung & Strombegrenzung
* [ ] Labornetzteil auf $12{,}0\,\text{V DC}$ einstellen, Strombegrenzung auf $150\,\text{mA}$.
* [ ] Ruhestrom messen: Sollwert $= 45\,\text{mA}$ bis $75\,\text{mA}$ (ohne Akkuladung).
* [ ] Pruefpunkt `TP_5V`: Sollwert $= 5{,}15\,\text{V} \pm 0{,}05\,\text{V}$.
* [ ] Pruefpunkt `TP_3V3`: Sollwert $= 3{,}30\,\text{V} \pm 0{,}02\,\text{V}$.

### Schritt 3: Flashen & System-Selbsttest
* [ ] ESP-IDF / PlatformIO Flash via nativem USB-C Port ausfuehren (`firmware/main_controller/`).
* [ ] LittleFS-Partition formatieren und Profile aus `firmware/main_controller/data/profiles/` hochladen.
* [ ] Serielle Konsole ($115.200\,\text{Baud}$): Meldungen "LittleFS Mount OK", "1-Wire Manager Task OK", "I2S ES8388 Codec Init OK", "TCAN334G CAN-FD OK" verifizieren.

### Schritt 4: Audio- & Ducking-Funktionstest
* [ ] $1\,\text{kHz}$ Sinuston ($1{,}0\,\text{V}_{\text{RMS}}$) an Audio-Input anlegen.
* [ ] Oszilloskop an `PORT1_AUDIO_OUT`: Ueberpruefen, ob das Signal innerhalb von $15\,\text{ms}$ weich gedaempft wird.
* [ ] Signal abschalten: Pruefen, ob nach $600\,\text{ms}$ Hold-Zeit die weiche $250\,\text{ms}$-Raised-Cosine-Rueckkehr erfolgt.

### Schritt 5: IP67-Dichtheitspruefung
* [ ] Montiertes Gehaeuse in Vakuumkammer bei $-20\,\text{kPa}$ Unterdruck fuer 60 Sekunden halten (Druckverlust $< 0{,}5\,\text{kPa}$).
