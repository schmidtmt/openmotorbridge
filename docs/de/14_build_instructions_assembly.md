# 14 - Bauanleitung, Verkabelung & Fahrzeug-Installation

Dieses Dokument ist die vollständige, praxisorientierte Schritt-für-Schritt-Bauanleitung für den Eigenbau eines kompletten **OpenMotorBridge (v8.0)** Gesamtsystems. Es enthält eine exakte Bedarfsaufstellung aller 3D-Druckteile, bestückten Leiterplatten (PCBAs), mechanischen Normteile, Dichtungen, Kabelbaumkomponenten sowie das Inbetriebnahmeprotokoll.

---

## 1. Übersicht des Gesamtkits (Was wird gebaut?)

Ein vollständiges OpenMotorBridge-Fahrzeugkit besteht aus folgenden Baugruppen:

```
                      ┌─────────────────────────────────────────┐
                      │    1x ZENTRALE MAIN BOX (IP67)          │
                      │    (Unter der Sitzbank / im Heck)       │
                      │    • Unterwanne + Zwischenboden + Deckel│
                      │    • Hauptplatine (ESP32-S3, Codec, USV)│
                      │    • Integrierter Pufferakku (LiPo)     │
                      └────────────────────┬────────────────────┘
                                           │
                        1x ZENTRALER KABELBAUM (HD26 IP67)
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         │                                 │                                 │
         ▼                                 ▼                                 ▼
┌──────────────────┐             ┌──────────────────┐              ┌──────────────────┐
│ 1x POD 1 (LINKS) │             │ 1x POD 2 (RECHTS)│              │ 1x POD 3 (HECK)  │
│ (Rahmen / Sturzb)│             │ (Rahmen / Sturzb)│              │ (Heckbürzel)     │
│ • Pod-Gehäuse    │             │ • Pod-Gehäuse    │              │ • Pod-Gehäuse    │
│ • Basisplatine   │             │ • Basisplatine   │              │ • Basisplatine   │
│ • KASSETTE 1     │             │ • KASSETTE 2     │              │ • KASSETTE 3     │
│   (z. B. Sena)   │             │   (z. B. Cardo)  │              │   (LoRa + GNSS)  │
└──────────────────┘             └──────────────────┘              └──────────────────┘
                                           │
                                           ▼ 2.4 GHz Funkbrücke (ESP-NOW < 1.8 ms)
                                 ┌──────────────────────────────────┐
                                 │ 1x UNIVERSAL FRONT-KNOTEN (IP67) │
                                 │ (Smart Fairing Hub & Cockpit)    │
                                 │ • 4-in-1 Universal-Befestigung   │
                                 │ • Ottocast USB-A Port (CarPlay)  │
                                 │ • Handschuhfach USB-C Ladeport   │
                                 │ • Knowles MEMS Fahrtwind-Sensor  │
                                 │ • Batteriefreier Lenker-PTT      │
                                 └──────────────────────────────────┘
```

---

## 2. Das brauche ich für ein Komplettset (Bedarfsaufstellung für 1 Fahrzeug)

Um ein vollwertiges OpenMotorBridge (v8.0) Gesamtsystem für ein Motorrad aufzubauen, werden folgende Teile benötigt. Diese Aufstellung fasst alle Baugruppen (Zentralbox, 3 Satelliten-Pods, Kassetten, Front-Knoten, Kabelbaum und Normteile) strukturiert in 6 Kategorien zusammen:

### 2.1 Kategorie A: 3D-Druckteile (MJF PA12 schwarz oder FDM ASA/PETG)
*Empfohlenes Fertigungsverfahren: Multi Jet Fusion (MJF) oder SLS in PA12 (schwarz gefärbt, glasperlengestrahlt) oder FDM mit ASA/PET-CF. CAD-Dateien liegen in [`hardware/cad/stl/`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/).*

| Baugruppe | STL-Dateiname | Stück | Funktion & Beschreibung |
| :--- | :--- | :---: | :--- |
| **Main Box Unterteil** | [`main_box_lower_case.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lower_case.stl) | **1** | Monocoque-Unterwanne mit 4x M4 Silentblock-Ohren, 4x PCB-Domen und O-Ring-Nut |
| **Main Box Zwischenboden** | [`main_box_mid_tray.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_mid_tray.stl) | **1** | Akku-Wanne für 1000 mAh LiPo, 10x Konvektionsschlitze & Dichtfeder |
| **Main Box Deckel** | [`main_box_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lid.stl) | **1** | Abschlussdeckel mit Gore ePTFE-Ventildom & 4x M3 Schraubenlöchern |
| **Pod-Basisgehäuse** | [`pod_base_housing.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod_base_housing.stl) | **3** | Schachtgehäuse für Pod 1 (Links), Pod 2 (Rechts) und Pod 3 (Heck) mit 120°-Rohrbett |
| **Pod-Schottwände** | [`03_pod_bulkhead_partition.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl) | **3** | Schottwand mit Dichtkragen & Federaufnahmen (1x pro Pod) |
| **Kassette 1 (Fahrer)** | [`cartridge_sena_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_sena_sled.stl) *(oder Cardo)* | **1** | Kassetten-Schlitten für Fahrer-Headset (Sena 50S/60S oder Cardo Packtalk Edge) |
| **Kassette 2 (Sozius)** | [`cartridge_cardo_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_cardo_sled.stl) *(oder Blind)* | **1** | Kassetten-Schlitten für Zweit-Headset oder hermetische Blindkassette |
| **Kassette 3 (Heckbürzel)**| [`cartridge_omm_transceiver_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_omm_transceiver_sled.stl) | **1** | Heck-Kassette für RP2040 Coprozessor, GNSS-Patch und LoRa-Antenne |
| **Front-Knoten Unterwanne** | [`front_node_lower_case.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_lower_case.stl) | **1** | Cockpit-Gehäusewanne mit AMPS-Lochbild, EPDM-Dichtkämmen & V-Rohrbett |
| **Front-Knoten Deckel** | [`front_node_upper_case.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_upper_case.stl) | **1** | Gehäusedeckel mit Knowles MEMS Schalleintritt & O-Ring-Dichtnut |
| **Heck-Radar Kombihalter** | [`pod3_radar_bracket.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod3_radar_bracket.stl) | **1** | M5 GoPro-Ausleger zur horizontalen Ausrichtung des Garmin Varia / mmWave Radars |
| **Summe 3D-Druckteile** | | **15** | **Vollständiger Teilesatz für 1 Gesamtsystem** |

---

### 2.2 Kategorie B: Bestückte Leiterplatten (5 PCBAs bei JLCPCB / Eurocircuits)
*Fertigungsdaten (Gerber ZIP, BOM CSV, CPL Pick & Place) liegen in [`hardware/production_packages/`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages).*

| Leiterplatte | Bezeichnung / Projekt | Stück | Lagen & Spezifikation | Hauptfunktionen |
| :--- | :--- | :---: | :--- | :--- |
| **PCBA 01** | Zentralbox Hauptplatine (`kicad_main_box`) | **1** | 4-Layer FR4 TG150, ENIG Gold | ESP32-S3 Dual-Core, LM5164 DCDC, BQ24075 USV, ES8388 Codec, Bourns Audio-Übertrager, BMI270 IMU, MicroSD |
| **PCBA 02** | Pod-Basis Trägerplatine (`kicad_pod_base`) | **3** | 2-Layer FR4, ENIG Gold | M8 6-Pin IP67 Buchse, SP3012 ESD-Schutzarray, Harwin 6-Pin Präzisions-Stiftleiste |
| **PCBA 03** | Universal Kassettenplatine (`kicad_cartridge`)| **2** | 2-Layer FR4, ENIG Gold | Harwin 6-Pin Präzisionsbuchse, DS2401 1-Wire Seriennummer, JST-SH 6-Pin Header zum OEM-Headset |
| **PCBA 04** | Heck-Pod 3 Transceiver (`kicad_rear_pod3`) | **1** | 4-Layer FR4 TG150, ENIG Gold | RP2040 Coprozessor, u-blox NEO-M9N / MAX-M10S GNSS, Semtech SX1262 LoRa, 3x Murata MM8030 HF-Umschalter |
| **PCBA 05** | Universal Front-Knoten (`kicad_front_node`) | **1** | 4-Layer FR4 TG150, ENIG Gold | ESP32-C3 RISC-V, USB2512B Hub, LMR36015 DCDC, TPS2051B Lastschalter, Knowles MEMS Mikrofon, PTT-Interface |

---

### 2.3 Kategorie C: Mechanische Normteile, Schrauben & Federn (V4A Edelstahl / Messing)

| Bauteil | Spezifikation / Norm | Stück | Montageort & Zweck |
| :--- | :--- | :---: | :--- |
| **M3 Gewindeeinsätze** | Ruthex Messing M3 $\times 5{,}7\,\text{mm}$ (RX-M3x5.7) | **8** | 4x Zentralbox-Unterwanne, 4x Front-Knoten Unterwanne (Lötkolben $220\,^\circ\text{C}$) |
| **M4 Gewindeeinsätze** | Ruthex Messing M4 $\times 8{,}1\,\text{mm}$ (RX-M4x8.1) | **4** | Front-Knoten AMPS-Bodenmontage ($30 \times 38\,\text{mm}$) |
| **Gehäuseschrauben Main** | Zylinderkopf DIN 912 V4A M3 $\times 40\,\text{mm}$ | **4** | Durchgehende 4-Eck-Verschraubung Zentralbox |
| **Gehäuseschrauben Front**| Zylinderkopf DIN 912 V4A M3 $\times 20\,\text{mm}$ | **4** | 4-Eck-Verschraubung Front-Knoten |
| **Platinenschrauben** | Zylinderkopf DIN 912 V4A M2.5 $\times 6\,\text{mm}$ | **8** | 4x Main Box PCBA, 4x Front-Node PCBA |
| **Schottwandschrauben Pod**| Senkkopf DIN 7991 V4A M2 $\times 8\,\text{mm}$ | **6** | Fixierung der 3 Pod-Schottwände (2x pro Pod) |
| **Auswerfer-Druckfedern** | Edelstahl V4A ($\varnothing 4{,}5\,\text{mm}, L_0=15\,\text{mm}, R=1{,}2\,\text{N/mm}$) | **6** | Auto-Eject Schnappmechanismus (2x pro Pod-Schottwand) |
| **Silentblöcke / Puffer** | Gummipuffer Typ A (M4 Außengewinde / M4 Innen, $\varnothing 15 \times 10\,\text{mm}$) | **4** | Schwingungsentkoppelte Rahmenmontage der Zentralbox |
| **Sicherungsmuttern / U-Scheiben**| DIN 985 M4 Stoppmuttern + DIN 125 Unterlegscheiben V4A | **4** | Konterung der Silentblöcke am Motorradrahmen |
| **M5 Klemmschraube & Hutmutter** | DIN 912 V4A M5 $\times 25\,\text{mm}$ + M5 Hutmutter | **1** | Klemmung des GoPro-Radar-Schwenkarms an Pod 3 |

---

### 2.4 Kategorie D: Dichtungen, Druckausgleich & Lichtleiter (IP67)

| Bauteil | Spezifikation | Stück | Montageort & Funktion |
| :--- | :--- | :---: | :--- |
| **Silikon-Dichtschnur Main** | Silikon-Rundschnur $\varnothing 1{,}5\,\text{mm}$ Shore 40A/50A ($40\,\text{cm}$) | **1** | Umlaufende Nut-Feder-Abdichtung Zentralbox |
| **Silikon-Dichtschnur Front**| Silikon-Rundschnur $\varnothing 1{,}5\,\text{mm}$ Shore 40A/50A ($30\,\text{cm}$) | **1** | Umlaufende Deckel-Dichtung Front-Knoten |
| **Kassetten-Flanschdichtungen**| Silikon Formdichtung Shore 40A ($54 \times 18\,\text{mm}$, $1{,}5\,\text{mm}$) | **3** | Stirnseitige Mundloch-Abdichtung an Pod 1, 2 und 3 |
| **EPDM-Dichtkämme** | EPDM Zellkautschuk geschlitzt ($15 \times 8 \times 4\,\text{mm}$) | **2** | Wasserdichte Kabeleinführung der Flachkabel im Front-Knoten |
| **Druckausgleichsventil** | Gore Automotive AVS 41 (M8x1.25 Schraubventil) | **1** | Belüftung & Kondensatvermeidung im Main Box Deckel |
| **ePTFE-Klebemembranen** | Gore / Porex IP67 Membranpad $\varnothing 6{,}0 \dots 7{,}0\,\text{mm}$ (selbstklebend) | **5** | 3x Entlüftungsdome Pods, 1x Front-Node, 1x Knowles MEMS Akustik-Schallöffnung |
| **Lichtleiter (LED)** | Bivar PLPC3-3MM oder Mentor PMMA $\varnothing 3{,}0\,\text{mm}$ ($L=8\,\text{mm}$) | **1** | Wasserdichte Einkopplung der RGB Status-LED im Main Box Deckel |

---

### 2.5 Kategorie E: Kabelbaum, Steckverbinder & Pufferakku

| Bauteil | Spezifikation / Typ | Stück | Zweck & Funktion |
| :--- | :--- | :---: | :--- |
| **HD26 Flanschbuchse IP67** | Amphenol LTW HD26 Buchse (Frontmontage mit Dichtung) | **1** | Gehäuseschnittstelle an der Zentralbox |
| **HD26 Kabelstecker IP67** | HD26 Stecker mit Rändelschrauben & Gummitülle | **1** | Hauptstecker am zentralen Kabelbaum |
| **M8 6-Pin Buchsenkabel** | M8 6-Pin A-kodiert IP67 Buchse (PUR geschirmt, 250 mm) | **3** | Peitschen 1, 2, 3 am Kabelbaum zu den Pods |
| **M8 4-Pin Buchsenkabel** | M8 4-Pin A-kodiert IP67 Buchse (PUR geschirmt, 250 mm) | **1** | Peitsche 5 am Kabelbaum für Heck-Radar (Garmin Varia / mmWave) |
| **AMP Superseal 1.5 Buchse**| TE Connectivity AMP Superseal 1.5 4-Pin Buchsengehäuse | **1** | Peitsche 4 am Kabelbaum für 12V Bordnetz (KL30, KL15, GND) |
| **M8 Verbindungskabel** | M8 6-Pin A-kodiert Stecker/Buchse (PUR, 1.0 m bzw. 1.5 m) | **3** | Zuleitungskabel vom Pigtail unter der Sitzbank zu den Pods |
| **Pufferakku (LiPo USV)** | 1S 3.7V LiPo 1000 mAh mit integriertem 10k NTC | **1** | USV-Notstrompuffer in der Zentralbox (Molex Micro-Fit 3.0) |
| **KFZ-Sicherungshalter** | Wasserdichter Mini-Flachsicherungshalter IP67 + **2A Sicherung**| **1** | Absicherung der 12V Dauerplus-Leitung (KL30) direkt am Batteriepol |
| **Automotive-Leitungen** | FLRY-B $0{,}5\,\text{mm}^2$ (Power/GND) und $0{,}35\,\text{mm}^2$ (Signale/Audio)| *nach Bedarf* | Fahrzeugkabelbaum nach [`central_breakout_harness_wirelist.csv`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/05_wiring_harness_spec/central_breakout_harness_wirelist.csv) |
| **EPDM-Spannbänder** | UV- und ozonbeständiges EPDM ($\varnothing 45 \dots 75\,\text{mm}$) | **6** | Werkzeuglose Schnellmontage der Pods an Rahmen- & Sturzbügeln |

---

### 2.6 Kategorie F: Werkzeuge, Chemie & Hilfsmittel

* **Lötkolben / Lötstation:** Mit feiner Spitze ($220 \dots 240\,^\circ\text{C}$) zum sauberen Einschmelzen der Ruthex-Gewindeeinsätze und Löten des Kabelbaums.
* **Sechskantschlüssel (Inbus):** Größen $1{,}5\,\text{mm}$ (M2), $2{,}0\,\text{mm}$ (M2.5), $2{,}5\,\text{mm}$ (M3) und $3{,}0\,\text{mm}$ (M4/M5).
* **Schraubensicherung:** *Loctite 243* (blau, mittelfest) für alle Schraubverbindungen am Motorrad gegen Vibrationslösen.
* **Silikonfett / Dichtungsfett:** Für die O-Ring-Dichtschnüre und Kassettenlippen (verhindert Versprödung und Reibung).
* **Elektronik-Schutzlack (Conformal Coating):** *Peters Elpeguard SL 1307* oder *Electrolube UR5041* Polyurethanlack (IPC-CC-830B).
* **Crimpzange:** Für JST-SH/GH Kontakte und Kfz-Flachsteckhülsen.
* **USB-C Datenkabel:** Zum Flashen der Firmware via PlatformIO / ESP-IDF.

---

## 3. 3D-Druck-Leitfaden & Materialauswahl (FDM vs. MJF)

### Empfohlene Filamente für Outdoor & Motorrad (FDM):
* **PETG:** *Ideal für alle Drucker ohne Einhausung.* UV-stabil, benzin-/ölbeständig, schlagzäh bis $80\,^\circ\text{C}$ Dauertemperatur.
* **ASA (oder ABS):** *Beste Wahl für Drucker mit geschlossenem Bauraum (z. B. Bambu X1/P1, Prusa XL).* $100\,\%$ UV- und witterungsbeständig, hitzebeständig bis $100\,^\circ\text{C}$.
* **PA-CF / PET-CF:** Exzellente Steifigkeit, seriennahe matte Carbon-Haptik.
* ❌ *Wichtig:* **Kein Standard-PLA verwenden**, da PLA am Motorrad in der prallen Sonne (über $55\,^\circ\text{C}$) erweicht und verzieht!

### Optimale Slicer-Einstellungen für IP67-Dichtigkeit:
* **Wandlinien (Perimeter):** 4 bis 5 Wände einstellen ($\approx 1{,}6 \dots 2{,}0\,\text{mm}$ für massive Wände ohne Hohlräume).
* **Infill:** $25 \dots 40\,\%$ (Gyroid oder Honeycomb).
* **Schichthöhe:** $0{,}16\,\text{mm}$ (saubere O-Ring-Nuten).
* **Flussrate (Flow):** $102 \dots 104\,\%$ (leichte Überextrusion dichtet Mikroporen zuverlässig ab).

---

## 4. Montage der Baugruppen

### Schritt 1: Zentralbox (Main Box) montieren
1. **Gewindeeinsätze:** 4x M3 Messing-Gewindeeinsätze (Ruthex) mit Lötkolben ($240\,^\circ\text{C}$) bündig in die Unterwanne einschmelzen.
2. **Platine fixieren:** Hauptplatine (`openmotorbridge_central_box`) mit M2.5 Schrauben auf die Dämpferdome setzen.
3. **Zwischenboden & Akku:** Oberwanne aufsetzen, 1000 mAh LiPo in die Wanne legen und mit EPDM-Spannband sichern.
4. **Dichtungen & Deckel:** Silikon-Rundschnur (Ø 1,5 mm) in die Deckelnut einlegen, Gore-Membran einkleben und mit 4x M3 x 40 mm Schrauben über Kreuz festziehen.

### Schritt 2: Satelliten-Pods 1, 2 und Heck-Pod 3
1. **Basisplatine einsetzen:** `openmotorbridge_pod_base` in das Pod-Gehäuse einschieben und M8-Buchse festziehen.
2. **Schottwand fixieren:** Schottwand mit M2 Schrauben sichern.
3. **Kassetten-Montage:** Kassettenplatine (`openmotorbridge_pod_cartridge`) in den Kassetten-Schlitten einklicken und OEM-Cradle (Sena Pogo-Leiste oder Cardo Air-Mount) anschließen.

---

## 5. Universal Front-Knoten Aufbau & Montage

### 5.1 Zusammenbau der Front-Node Box
1. **Gewindeeinsätze einschmelzen:**
   * 4x M3 Messingeinsätze in die Gehäuse-Ecken der Unterwanne einschmelzen.
   * 4x M4 Messingeinsätze in das AMPS-Lochbild ($30 \times 38\,\text{mm}$) am Gehäuseboden einschmelzen.
2. **Akustik-Membran einsetzen:** Hydrophobe Gore ePTFE-Membran über die Schallöffnung des Knowles MEMS Mikrofons kleben.
3. **Platine montieren:** Front-Node Platine (`PCBA 05`) mit M2.5 Schrauben fixieren.
4. **Verkabelung & EPDM-Kämme:** Zuleitungskabel in die EPDM-Dichtkämme einlegen und Deckel mit Silikon-Rundschnur und 4x M3 x 20 mm Schrauben verschließen.
5. **USB-C Kappe:** Silikon-Schutzkappe am Port `J2` befestigen.

### 5.2 Montage am Fahrzeug (4 Optionen)

```
┌────────────────────────────────────────────────────────────────────────┐
│               MONTAGE-OPTIONEN DES UNIVERSAL FRONT-KNOTENS             │
├────────────────────────────────────────────────────────────────────────┤
│ Option 1: AMPS-Bohrung (30 x 38 mm)                                    │
│ • Direktmontage an RAM-Mount Kugel, Garmin-Halter oder Navi-Strebe     │
│ • Perfekt für Adventure-Bikes und Naked Bikes                          │
├────────────────────────────────────────────────────────────────────────┤
│ Option 2: 120° V-Nut Rohrbett mit EPDM-Spannringen                     │
│ • Werkzeuglose Befestigung an Ø 22 bis Ø 32 mm Sturzbügeln (BMW GS/RT) │
│ • Vibrationsgedämpft, beschädigt keine Lackierung                      │
├────────────────────────────────────────────────────────────────────────┤
│ Option 3: M4 Silentblöcke                                              │
│ • Schwingungsentkoppelte Schraubmontage im Verkleidungsschnabel         │
├────────────────────────────────────────────────────────────────────────┤
│ Option 4: 3M Dual-Lock Klettnuten                                      │
│ • Verdeckte Innenmontage an der Innenseite von Harley Batwing /        │
│   Sharknose Frontverkleidungen                                         │
└────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Elektrischer Anschluss am Motorrad
* **12V Bordnetz-Einspeisung:** Der Front-Knoten benötigt lediglich eine einzige 2-adrige Zuleitung (KL15 Zündungsplus und Fahrzeugmasse), die am Standlicht, Scheinwerfer oder Cartool-Zubehörstecker abgegriffen wird.
* **Ottocast Dongle:** Wird an USB-A Port `J1` angesteckt und mit 3M Dual-Lock in der Verkleidung fixiert.
* **Handschuhfach:** Ein USB-C Verlängerungskabel führt von Port `J2` ins Handschuhfach für das Smartphone.
* **Lenkertaster:** 2-adriges Kabel vom mechanischen Lenker-PTT-Taster führt auf Buchse `J3` (GPIO 0).

---

## 6. Erstinbetriebnahme & Software-Flash (Schritt-für-Schritt)

```bash
# 1. Firmware-Repository klonen & in Zentralcontroller-Verzeichnis wechseln
cd openMotorBridge/firmware/main_controller

# 2. Zentralcontroller via USB-C flashen (ESP32-S3)
pio run --target upload

# 3. Kassetten-Profile auf das LittleFS-Dateisystem hochladen
pio run --target uploadfs

# 4. Heck-Co-Prozessor flashen (RP2040 in Pod 3)
cd ../rear_coprocessor
pio run --target upload

# 5. Front-Knoten flashen (ESP32-C3)
cd ../front_node
pio run --target upload
```

### Selbsttest-Checkliste:
1. [ ] **Labornetzteil:** $12{,}0\,\text{V}$ anlegen (Strombegrenzung $150\,\text{mA}$). Ruhestrom messen: Sollwert $= 45 \dots 75\,\text{mA}$.
2. [ ] **Status-LED:** Blinkt nach dem Start grün (System bereit, Pufferakku lädt).
3. [ ] **Web-Dashboard:** Im Browser via Web-Bluetooth mit `OpenMotorBridge_v8` koppeln.
4. [ ] **Kassettenerkennung:** Kassetten in Pod 1 und 2 einstecken $\rightarrow$ Profile werden im Dashboard sofort mit Seriennummer angezeigt.
5. [ ] **Front-Knoten Funkverbindung:** Status-Kachel im Dashboard zeigt `ESP-NOW LINK (2.4 GHz) - BEREIT`.
6. [ ] **PTT-Test:** Lenkertaster drücken $\rightarrow$ Grüne PTT-Anzeige im Dashboard leuchtet auf (`< 1.8 ms Latenz`), TLP222A Optokoppler schaltet durch.
7. [ ] **CarPlay Kaltstart-Test:** Im Dashboard auf "CarPlay 1-Klick Kaltstart" klicken $\rightarrow$ VBUS schaltet für $2{,}5\,\text{s}$ auf $0{,}00\,\text{V}$ ab und startet sauber neu.
8. [ ] **Audio-Check:** Headset koppeln, Musik abspielen $\rightarrow$ sauberes, glasklares Signal ohne Lichtmaschinenpfeifen oder Masseschleifen (dank 1500V Bourns Übertrager-Trennung).

---

## 7. Wartung & Pflege

* **Dichtungsinspektion:** 1x pro Saison die O-Ring-Dichtschnur der Main Box, des Front-Knotens und der Kassetten mit Silikonfett pflegen.
* **Druckausgleich:** Sicherstellen, dass die ePTFE-Gore-Membranen sauber und durchlässig sind.
* **Firmware-Updates:** Drahtlos und ohne Ausbau direkt über die WebBLE-PWA-Oberfläche durchführbar.
