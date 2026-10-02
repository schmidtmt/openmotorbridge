# 14 - EMV-Härtung, Schirmung & ESD-Schutz

Dieses Dokument spezifiziert die Schutzschaltungen gegen Kfz-Bordnetz-Transienten (ISO 7637-2), die HF-Entkopplung im 2.4-GHz-, 868-MHz- und 6.5-GHz-UWB-Band, die Schutzlackierung nach IPC-CC-830B sowie die mechanische Vibrations- und Schockdämpfung nach ISO 16750-3 für die OpenMotorBridge v8.0 Clean Architecture.

---

## 1. Kfz-Transienten- und Überspannungsschutz (ISO 7637-2 & ISO 16750-2)

* **Bordnetz-Absicherung:** Vollständige Konformität nach ISO 7637-2 (Pulse 1, 2a, 3a/b bis 100 V) und ISO 16750-2 Load-Dump.
* **Eingangssicherung:** Bourns MF-MSMF050-2 rückstellbare PPTC-Sicherung (1812 SMD, 500 mA Hold / 1.0 A Trip).
* **Überspannungsschutz:** Littelfuse SMBJ33CA bidirektionale TVS-Diode (33 V Standoff, 53.3 V max Clamping) $\rightarrow$ bietet dem 65V LM5164 Regler komfortable $> 11{,}7\,\text{V}$ Sicherheitsabstand bei Load-Dumps.
* **Verpolschutz:** Diodes Inc. DMP6023L P-Kanal MOSFET in der Masseleitung mit extrem geringem Durchlasswiderstand ($R_{\text{DS(on)}} < 25\,\text{m}\Omega$).
* **Filterung & Entstörung:** Zweistufiger LC-PI-Filter ($10\,\mu\text{H}$ Shielded Automotive Inductor / 3 A + 2x $10\,\mu\text{F}$ X7R 100V Keramikkondensatoren) am KL30/KL15-Eingang.

---

## 2. HF-Entkopplung, UWB-Backbone & Raumdiversität

* **2,4-GHz-Koexistenz (Sena vs. Cardo):** Durch die räumliche Trennung von Pod 1 (Rahmen links / Koffer links) und Pod 2 (Rahmen rechts / Koffer rechts) über das metallische Fahrzeugchassis wird eine minimale Freiraumdämpfung von $> 35\,\text{dB}$ sichergestellt. Dies verhindert De-Sensing und HF-Intermodulation effektiv.
* **Deterministischer UWB Fahrzeug-Backbone (Qorvo DW3110 / 6.489 GHz Ch. 5):**
  * Drahtlose Verbindung zwischen Front-Knoten (`PCBA 05`) und Zentralbox (`PCBA 01`).
  * Vollständig konform mit **ETSI EN 302 065-1, EN 302 065-3** und **EU-Beschluss 2019/785** ($-41{,}3\,\text{dBm/MHz}$, kontinuierlicher legaler Sendebetrieb ohne Duty-Cycle-Beschränkung).
  * Arbeitet im Frequenzbereich 6.240-6.739 GHz (Mittenfrequenz 6.489 GHz) mit 499.2 MHz Bandbreite weitab von 2.4 GHz (WLAN, Bluetooth, Mesh) und 5.8 GHz.
  * **Antennenintegration:** Taoglas FXUWB10 Flex-Antenne montiert in einer $11 \times 11 \times 0{,}6\,\text{mm}$ Aussparung im Gehäuseboden (Unterwanne) von Zentralbox und Front-Knoten. Verbindung über 20 mm U.FL Mikro-Koax. Die PCB-Oberseite behält eine geschlossene Massefläche (Zero-Keepout), und der Gehäusedeckel kann ohne Kabelzug geöffnet werden.
* **LoRa 868 MHz (Semtech SX1262) auf der Zentralbox (`PCBA 01`):**
  * Direkt auf der Zentralbox integriert und 24/7 über die USV-Batterieschiene gepuffert für unterbrechungsfreie Diebstahl-Sentry und Gruppen-Telemetrie.
  * Taoglas FXP895 Flex-Antenne ($110 \times 20 \times 0{,}8\,\text{mm}$) in einer geschützten Tasche im Deckel der Zentralbox mit 50 $\Omega$ U.FL Speisung.
* **Multi-GNSS & Sensor-Koexistenz am Front-Knoten (`PCBA 05`):**
  * u-blox SAM-M10Q mit integrierter $15 \times 15\,\text{mm}$ Keramik-Patchantenne, angebunden über Qwiic I2C (`J12`) im kalten Fahrtwind-Staudruckbereich.
  * Koexistenz mit TI TMP117 ($\pm 0{,}1\,^\circ\text{C}$ Temperatur) und OPT3001 Umgebungslichtsensor ohne HF-Einstrahlung auf den GNSS-LNA.
* **Zentrale ePTFE-Druckausgleichsmembran:** $\varnothing\,7{,}0\,\text{mm}$ Gore/Schreiner Air Vent mittig auf dem Gehäusedach gleicht thermische Druckstöße symmetrisch aus, ohne das HF-Fernfeld zu verzerren.
* **Robuster Deutsch DTM-12 Hauptkabelbaum:**
  * 4 Abzweige (Peitsche 1: Pod 1 DC-Power +12V geschaltet / GND, Peitsche 2: Pod 2 DC-Power +12V geschaltet / GND, Peitsche 3: Heck-Radar DC-Power +12V geschaltet / GND, Peitsche 4: Bordnetz KL30/KL15/CAN).
  * Alle 12 Pins belegt nach DTM-12 Belegungstabelle (Pins 1–5, 12 für Peitsche 4 / Bordnetz & CAN; Pins 6–7 für Peitsche 1 / Pod 1; Pins 8–9 für Peitsche 2 / Pod 2; Pins 10–11 für Peitsche 3 / Heck-Radar).
  * IP68/IP69K Dichtung über Deutsch DTM-Verriegelung und Raychem DR-25 Schrumpfschlauch.

### 2.1 Multi-Band HF-Frequenzbelegungs- & Koexistenzmatrix

Um Interferenzen zwischen den 7 simultan aktiven Funksystemen der OpenMotorBridge vollständig auszuschließen, sind Frequenzen, Sendeleistungen und Antennenpositionen streng orthogonal ausgelegt:

| Funksystem / Band | Frequenzbereich | Sendeleistung / EIRP | Einbauort & Antennentyp | Koexistenz- & Entkopplungsmaßnahme |
| :--- | :--- | :---: | :--- | :--- |
| **868 MHz LoRa (SX1262)** | 863.0 - 870.0 MHz | +14 dBm (25 mW) | Zentralbox / Taoglas FXP895 Flex | Harmonischen-Tiefpass ($f_{\text{cut}} = 1{,}0\,\text{GHz}$); 24/7 USV-Dauerbetrieb |
| **1.575 GHz GNSS (SAM-M10Q)** | 1559 - 1610 MHz | Nur Empfang (-167 dBm) | Front-Knoten (`PCBA 05`) / 15x15 Keramik-Patch | SAW-Vorfilter im LNA; räumlich maximal entfernt von 868M/2.4G |
| **2.4 GHz ISM (Sena/Cardo/OMM/BLE)** | 2402 - 2480 MHz | +10 bis +20 dBm | Pod 1 (Links), Pod 2 (Rechts), Cockpit | $> 35\,\text{dB}$ Freiraumdämpfung über Fahrzeugrahmen; AFH & TDMA |
| **5 GHz Wi-Fi (CarPlay / AA)** | 5180 - 5825 MHz | +14 dBm (25 mW) | Cockpit / Front-Knoten (Integrierter Dongle) | Begrenzt auf Cockpit-Nahfeld; $> 600\,\text{MHz}$ Abstand zu UWB Ch. 5 |
| **5.9 GHz C-V2X / DSRC (ETSI)** | 5855 - 5925 MHz | +23 dBm (200 mW) | Fahrzeug-Heck / Monopol-Patch | Striktes Bandpassfilter; räumliche Trennung vom 5 GHz Cockpit-WLAN |
| **6.5 GHz UWB (DW3110 Ch. 5)** | 6240 - 6739 MHz | -41.3 dBm/MHz (< 1 mW) | Zentralbox, Front-Node, Pods, Radar | Ultra-Breitband (499.2 MHz BW); Null Interferenz mit Schmalband |
| **77 GHz mmWave Radar (MR20)** | 76.0 - 81.0 GHz | +30 dBm EIRP | Kennzeichen- / Heck-Bracket (`PCBA 08`) | Vollkommen entkoppelt; Millimeterwellen-Spektrum ohne HF-Kopplung |

### 2.2 Verbindliche Gesamtsystem-Antennenmatrix & Exakte Positionen

Zur Gewährleistung maximaler Link-Budgets und reproduzierbarer EMV-Konformität gilt folgende verbindliche Spezifikation aller Antennen und Montagepositionen im Gesamtsystem:

| Baugruppe | Funktechnik | Frequenz | Antennentyp | Genaue Position & Montage |
| :--- | :--- | :--- | :--- | :--- |
| **Zentralbox (`PCBA 01`)** | Semtech SX1262 LoRa | 868 MHz | Taoglas FXP895 Flex | Eingeklebt in Gehäusedeckel (`ANT1`), U.FL |
| **Zentralbox (`PCBA 01`)** | Qorvo DW3110 UWB | 6.5 GHz (Ch. 5) | Taoglas FXUWB10 Flex | Eigene Antennentasche im Gehäuseboden (`ANT2`), U.FL |
| **Zentralbox (`PCBA 01`)** | Qualcomm QCC3084 BT | 2.4 GHz | Keramik-Chipantenne | Onboard auf Moduloberseite (`F.Cu`), 0 mm Koax |
| **Zentralbox (`PCBA 01`)** | ESP32-S3 BLE/WiFi | 2.4 GHz | PCB-Trace-Antenne | Onboard WROOM-1 Modul |
| **Front-Knoten (`PCBA 05`)** | u-blox SAM-M10Q GNSS | 1.575 / 1.602 GHz | Keramik-Patchantenne | Onboard Moduloberseite mit freier Sicht zum Himmel |
| **Front-Knoten (`PCBA 05`)** | Qorvo DW3110 UWB | 6.5 GHz (Ch. 5) | Taoglas FXUWB10 Flex | Gehäusebodentasche der Front-Node Wanne, U.FL |
| **Front-Knoten (`PCBA 05`)** | ESP32-S3 BLE/WiFi | 2.4 / 5 GHz | COTS Stummel / Sharknose | U.FL Buchse am WROOM-1U Modul |
| **Smart Cartridge (`PCBA 03`)**| Qorvo DW3110 UWB | 6.5 GHz (Ch. 5) | Integrierte PCB-Antenne | Unterseite (`B.Cu`), strahlt nach unten durch Pod-Boden |
| **Smart Cartridge (`PCBA 03`)**| OMM Intercom Modul | 2.4 GHz TDMA | Keramik-Chipantenne | Stirnseitig auf Trägerplatine |
| **Heck-Radar (`PCBA 08`)** | Qorvo DW3110 UWB | 6.5 GHz (Ch. 5) | Taoglas FXUWB10 Flex | Gehäusetasche im Flügelfuß, U.FL Buchse |
| **Heck-Radar (`PCBA 08`)** | Wheeltec MR20 Radar | 77 GHz mmWave | On-Chip Patch-Array | Radom-Linse im Zentrum von PCBA 08 |

---

## 3. Schutzlackierung & Klimabeständigkeit (IPC-CC-830B)

### 3.1 Schutzlack-Spezifikation (Conformal Coating)
* **Material:** Modifizierter Polyurethan-Schutzlack (*Peters Elpeguard SL 1307 FLZ* oder *Electrolube UR5041*).
* **Schichtdicke:** $40\,\mu\text{m}$ bis $60\,\mu\text{m}$ (gemessen auf planen Kupferflächen).
* **Durchschlagfestigkeit:** $> 60\,\text{kV/mm}$ (zuverlässiger Schutz vor Kriechströmen bei Betauung, Nebel und salzhaltigem Spritzwasser).

### 3.2 Maskierungszonen vor dem Lackierprozess
Folgende Bauteile und Kontaktflächen dürfen **nicht** beschichtet werden:
1. MicroSD-Kartenhalter-Kontakte (innenliegende Federzungen auf PCBA 01).
2. Deutsch DTM-12 Header-Pins & vergoldete Federzungen-Kontakte.
3. J12 Qwiic I2C Buchsenkontakte auf PCBA 05.
4. USB-Buchsen (USB-A, USB-C) am Front-Knoten.
5. SMD-Testpunkte (TP_5V, TP_3V3, TP_GND).
6. Druckausgleichs-Bohrung der ePTFE-Membran.

---

## 4. Vibrations- & Schockfestigkeit (ISO 16750-3)

### 4.1 Schwingungsdämpfung am Motorrad
* **Platinenentkopplung:** 4x NBR-O-Ringe (Innendurchmesser 3,0 mm, Schnurstärke 1,0 mm) zwischen den Gehäusedomen und der PCB-Unterseite dämpfen hochfrequente Motorvibrationen.
* **Schraubensicherung:** Alle PCB-Befestigungsschrauben (M2,5) werden mit einem Drehmoment von $0{,}35\,\text{Nm}$ angezogen und mit mittelfestem Sicherungslack (blau, *Loctite 243*) gesichert.
* **Bauteilfixierung (Underfill / RTV-Silikon):**
  * **Bourns LM-NP-1001 Übertrager:** Ecken werden mit elastischem Silikonkleber (*Dow Corning 732* / *Dowsil 3145*) gegen Rissbildung an SMD-Lötstellen gesichert.
  * **Pufferakku:** Fixierung in der Oberwanne auf dem Zwischenboden mit vibrationsdämpfendem $1{,}0\,\text{mm}$ Schaumpolster (*3M VHB 4910* / EPDM) und elastischem EPDM-Gummispannband (Shore 50A).
