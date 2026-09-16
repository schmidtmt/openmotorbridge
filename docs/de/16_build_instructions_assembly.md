# 16 - Bauanleitung, Verkabelung & Fahrzeug-Installation

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
                                 │ (Cockpit- & Sensor-Hub)          │
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

#### 2.1.1 Basis-System (Universal für 1 Gesamtsystem)
| Baugruppe | STL-Dateiname | Stück | Funktion & Beschreibung |
| :--- | :--- | :--- :--- | :--- |
| **Main Box Unterteil** | [`main_box_lower_case.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lower_case.stl) | **1** | Monocoque-Unterwanne mit 4x M4 Silentblock-Ohren, 4x PCB-Domen und O-Ring-Nut |
| **Main Box Zwischenboden** | [`main_box_mid_tray.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_mid_tray.stl) | **1** | Akku-Wanne für 1000 mAh LiPo, 10x Konvektionsschlitze & Dichtfeder |
| **Main Box Deckel** | [`main_box_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lid.stl) | **1** | Abschlussdeckel mit Gore ePTFE-Ventildom & 4x M3 Schraubenlöchern |
| **Pod-Basisgehäuse** | [`pod_base_housing.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod_base_housing.stl) | **3** | Schachtgehäuse für Pod 1 (Gateway 1 Links), Pod 2 (Gateway 2 Rechts) und Pod 3 (Heck) mit 120°-Rohrbett |
| **Pod-Schottwände** | [`03_pod_bulkhead_partition.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl) | **3** | Schottwand mit Dichtkragen & Federaufnahmen (1x pro Pod) |
| **Kassetten-Basisschlitten**| [`cartridge_base_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl) | **3** | Schlittengrundkörper zur Aufnahme der Inlays und PCBA 03 (Pod 1 & 2) bzw. PCBA 04 (Pod 3) |
| **Kassetten-Riegel / Wippe**| [`cartridge_magnetic_lock_latch.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_magnetic_lock_latch.stl) | **2** | Magnetische Diebstahlschutz-Wipphebel mit Sägezahn-Rastung für Pod 1 & Pod 2 |
| **Heck-Pod 3 OMM-Radom** | [`cartridge_antenna_bracket_omm.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_antenna_bracket_omm.stl) | **1** | Dielektrisches Antennenradom & Trägerbrücke für PCBA 04 Transceiver im Heck-Pod 3 |
| **Front-Knoten Unterwanne** | [`front_node_lower_tub.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_lower_tub.stl) | **1** | Cockpit-Gehäusewanne mit AMPS-Lochbild, EPDM-Dichtkämmen & V-Rohrbett (PA12 / ASA) |
| **Front-Knoten Deckel** | [`front_node_upper_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_upper_lid.stl) | **1** | Gehäusedeckel mit Knowles MEMS Schalleintritt & O-Ring-Dichtnut (PA12 / ASA) |
| **Front-Knoten Dichtkämme** | [`front_node_cable_glands_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_cable_glands_tpu.stl) | **1 Paar** | Elastische Dichtkämme für Front (3x USB) & Flanke (3x Signale) (TPU 95A / 85A) |
| **Front-Knoten USB-C Kappe**| [`front_node_usbc_cap_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_usbc_cap_tpu.stl) | **1** | Elastische Staubschutzkappe mit Haltekollier für Service-Port (TPU 95A / 85A) |

#### 2.1.2 Kassetten-Inlays für Gateway-Slots 1 & 2 (Je nach Konfiguration 2 Stück wählen)
> **Hinweis zur Systemarchitektur:** OpenMotorBridge ist eine Multi-Protokoll-Mesh-Bridge. Die beiden Kassetten-Slots sind keine separaten "Fahrer-" oder "Sozius"-Headsets, sondern **Hardware-Gateway-Transceiver**. Sie ermöglichen den simultanen Parallelbetrieb zweier unterschiedlicher Funknetze (z. B. Slot 1 = Sena Mesh 3.0 / Wave und Slot 2 = Cardo DMC 2.0 oder PMR446), sodass Fahrer und Beifahrer über ihre Helme nahtlos in beide Gruppen eingebunden sind.

| Baugruppe | STL-Dateiname | Stück | Funktion & Beschreibung |
| :--- | :--- | :---: | :--- |
| **Gateway-Inlay Sena** | [`cartridge_insert_sena.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) | *Opt. (1)* | Kassetten-Inlay für Sena SPIDER X Slim / 50S / 60S (Mesh 3.0 / Wave) |
| **Gateway-Inlay Cardo** | [`cartridge_insert_cardo.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl) | *Opt. (1)* | Kassetten-Inlay für Cardo Packtalk Edge / Pro (DMC Gen2) mit Air-Mount |
| **Blindkassette / Dry Box** | [`cartridge_insert_blindkassette.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_blindkassette.stl) | *Opt. (1)* | Hermetischer Schutzschlitten mit O-Ring für ungenutzten Slot oder regendichte Kleinteile |

#### 2.1.3 Fahrzeugspezifische Pod-Befestigungskits (3D-Druckteile)
*Die Montage der Pods an Rahmen, Koffer oder Heck erfolgt über fahrzeugspezifische 3D-Druckteile:*

* **Option A: Adventure-Kit (BMW R1250/R1300 GS / Adventure, Africa Twin, KTM):**
  | Baugruppe | STL-Dateiname | Stück | Funktion & Beschreibung |
  | :--- | :--- | :---: | :--- |
  | **Rohrschellen-Unterteil** | [`adventure_pannier_rack_clamp_base.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_pannier_rack_clamp_base.stl) | **4** | Schellen-Basiskörper für Ø 18 mm Rohrträger (Rahmendreieck) |
  | **Rohrschellen-Kappe** | [`adventure_pannier_rack_clamp_cap.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_pannier_rack_clamp_cap.stl) | **4** | Klemmdeckel für M5 Verschraubung am Kofferträgerrohr |
  | **Rack-Tail Mount Heck** | [`adventure_rack_tail_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_rack_tail_mount.stl) | **1** | Heck-Balkon Gepäckbrücken-Ausleger für Pod 3 mit Astabweiser |
  | **Transition-Dock** | [`adventure_transition_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_transition_dock.stl) | **2** | Kofferunabhängiges Dock für die Sitzbank-Bügelfalte (Ø 28 mm Rohr) |
  | **Radar Varia Dock** | [`radar_varia_gopro_lock_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_varia_gopro_lock_dock.stl) | **1** | Garmin Varia Bajonett-Dock mit M3 Sicherung & Hirth-Verzahnung |
  | **Hirth-Formschluss** | [`011_gopro_hirth_lock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/011_gopro_hirth_lock.stl) | **1** | 36-Zahn-Rosette zur vibrationsfesten Radar-Winkelklemmung |

* **Option B: Harley-Davidson Touring & Bagger Kit (Street Glide, Road Glide, CVO ST, Road King):**
  | Baugruppe | STL-Dateiname | Stück | Funktion & Beschreibung |
  | :--- | :--- | :---: | :--- |
  | **Kofferdeckel-Dock** | [`saddlebag_lid_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/saddlebag_lid_dock.stl) | **2** | Flaches Kofferdeckel-Montagedock für Pod 1 & Pod 2 |
  | **Touring Fender Console** | [`pod3_touring_fender_console.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod3_touring_fender_console.stl) | **1** | Aerodynamische Heckpod-Konsole auf dem Heckkotflügel (Road King) |
  | *Alternativ: CVO ST Finne*| [`cvo_st_telemetry_fin.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/cvo_st_telemetry_fin.stl) | *(1)* | Aerodynamische Haifischflosse / Telemetrie-Finne für CVO Road Glide ST |
  | *Alternativ: Skeleton Dock*| [`cvo_st_undercowl_skeleton_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/cvo_st_undercowl_skeleton_dock.stl) | *(1)* | Aufrechtes Federsitz-Dock unter der Forged-Carbon-Hutze |
  | **Kennzeichen-Radarhalter**| [`radar_license_plate_bracket.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_license_plate_bracket.stl) | **1** | Entkoppelter Varia-Radarhalter unterhalb des Kennzeichens |
  | *Alternativ: Underfender* | [`radar_center_underfender_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_center_underfender_mount.stl) | *(1)* | Zentrische Unter-Kotflügel-Platte für Custom/Bagger mit seitlichem Kennzeichen |

#### 2.1.4 Zubehör (Optional)
| Baugruppe | STL-Dateiname | Stück | Funktion & Beschreibung |
| :--- | :--- | :---: | :--- |
| **Smart-Keyfob Unterschale**| [`smart_keyfob_lower_shell.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/smart_keyfob_lower_shell.stl) | **1** | Gehäusewanne mit LRA-Dämpfungsbett und Magnetaufnahme für PCBA 07 |
| **Smart-Keyfob Oberschale** | [`smart_keyfob_upper_shell.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/smart_keyfob_upper_shell.stl) | **1** | Gehäusedeckel mit 3 Tastenfeldern & Lichtleiter-Aussparung |
| **Smart-Keyfob Bumper** | [`smart_keyfob_tpu_rim.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/smart_keyfob_tpu_rim.stl) | **1** | Stoßabsorbierender Umlauf-Bumper (TPU 85A/95A) |


---

### 2.2 Kategorie B: Bestückte Leiterplatten (100 % fertig von JLCPCB / Eurocircuits)
*Alle Platinen werden vollautomatisch im SMT-Verfahren bestückt und vorgetestet geliefert. Es sind **keinerlei Lötarbeiten** durch den Anwender erforderlich!*
*Fertigungsdaten (Gerber ZIP, BOM CSV, CPL Pick & Place) siehe [Kapitel 15, Abschnitt 8](file:///Users/schmidtm/openMotorBridge/docs/de/15_bom_manufacturing.md#8-1-click-bestellleitfaden-f%C3%BCr-jlcpcb-alle-leiterplatten-fertig-best%C3%BCckt).*

| Leiterplatte | Bezeichnung / Projekt | Stück | Hauptfunktionen im System |
| :--- | :--- | :---: | :--- |
| **PCBA 01** | Zentralbox Hauptplatine (`kicad_main_box`) | **1** | ESP32-S3 Dual-Core, LM5164 DCDC, BQ24075 USV, ES8388 DSP-Codec, Audio-Übertrager, IMU |
| **PCBA 02** | Pod-Basis Trägerplatine (`kicad_pod_base`) | **3** | M8 6-Pin IP67 Buchse, ESD-Schutzarray, Harwin 6-Pin Präzisions-Dockingleiste |
| **PCBA 03** | Smart Modular Kassettenplatine Rev 2.0 (`kicad_cartridge`)| **2** | WCH CH32V003 RISC-V MCU (1-Wire Emulation & Opcode-Engine), 4x MOSFETs, J_ACT 8-Pin Header |
| **PCBA 04** | Heck-Pod 3 Transceiver (`kicad_rear_pod3`) | **1** | RP2040 Coprozessor, u-blox Multi-GNSS, Semtech SX1262 LoRa, 3x Murata MM8030 HF-Ports |
| **PCBA 05** | Universal Front-Knoten (`kicad_front_node`) | **1** | ESP32-S3 Xtensa, USB2514B Hub, SC8102 USB-PD 20W, TCAN334G CAN-FD, Knowles MEMS, PTT |
| **PCBA 07** | Smart-Keyfob (Zubehör, `kicad_smart_keyfob`)| *Opt.* | Bluetooth LE Tracker, LRA-Haptikmotor, MAX17048 Fuel-Gauge, 3 Tasten |

---

### 2.3 Kategorie C: Mechanische Normteile & Schrauben (V4A Edelstahl)
*Das Gehäusekonzept nutzt integrierte **Nut-Pockets (Sechskant-Mutternaschen)**. Muttern werden einfach eingelegt – **kein Einschmelzen von Gewindeeinsätzen mit dem Lötkolben!***

| Bauteil | Spezifikation / Norm | Stück | Montageort & Zweck |
| :--- | :--- | :---: | :--- |
| **Gehäuseschrauben Main** | Zylinderkopf DIN 912 V4A M3 $\times 40\,\text{mm}$ | **4** | Zentralbox-Gehäuse (greift in Nut-Pockets) |
| **Gehäuseschrauben Front**| Zylinderkopf DIN 912 V4A M3 $\times 20\,\text{mm}$ | **4** | Front-Node Gehäuse (greift in Nut-Pockets) |
| **Edelstahlmuttern M3** | DIN 934 / DIN 985 M3 V4A Muttern | **8** | Unverlierbar in Nut-Pockets eingelegt |
| **Platinenschrauben** | Zylinderkopf DIN 912 V4A M2.5 $\times 6\,\text{mm}$ | **8** | 4x Main Box PCBA, 4x Front-Node PCBA |
| **Schottwandschrauben Pod**| Senkkopf DIN 7991 V4A M2 $\times 8\,\text{mm}$ | **6** | Fixierung der 3 Pod-Schottwände (2x pro Pod) |
| **Kassetten-Halteplattenschrauben**| Senkkopf DIN 7991 V4A M2 $\times 6\,\text{mm}$ | **8** | Fixierung der Aktuator-Niederhalteplatten (4x pro Gateway) |
| **M2 Schwenkachsen Wippe** | Zylinderstift Edelstahl DIN 7 M2 $\times 8\,\text{mm}$ | **2** | Drehachsen für magnetische Kassetten-Rastwippen (Pod 1 & 2) |
| **Ferromagnetische Stahlanker**| Zylinderstift Stahl gehärtet DIN 6325 $\varnothing 6 \times 8\,\text{mm}$| **2** | Magnetanker im Hebelarm der Kassetten-Wippe |
| **Wippen-Rückstellfedern** | Edelstahl V4A ($\varnothing 3{,}5\,\text{mm}, L_0=10\,\text{mm}$)| **2** | Rückstellung der Sägezahn-Rastkralle |
| **Auswerfer-Druckfedern** | Edelstahl V4A ($\varnothing 4{,}5\,\text{mm}, L_0=15\,\text{mm}$) | **6** | Auto-Eject Schnappfedern (2x pro Pod-Schottwand) |
| **N52 Entriegelungsschlüssel**| Neodym N52 Blockmagnet ($20 \times 10 \times 5\,\text{mm}$) | **1** | Berührungsloser Magnetschlüssel für Kassetten-Auswurf |
| **Silentblöcke / Puffer** | Gummipuffer Typ A (M4 Außengewinde / M4 Innen, $\varnothing 15 \times 10\,\text{mm}$) | **4** | Schwingungsentkoppelte Rahmenmontage der Zentralbox |
| **Sicherungsmuttern M4 / Scheiben**| DIN 985 M4 Stoppmuttern + DIN 125 Unterlegscheiben V4A | **4** | Konterung der Silentblöcke am Motorradrahmen |

---

### 2.4 Kategorie D: Dichtungen, Druckausgleich & Lichtleiter (IP67)

| Bauteil | Spezifikation | Stück | Montageort & Funktion |
| :--- | :--- | :---: | :--- |
| **Silikon-Dichtschnur Main** | Silikon-Rundschnur $\varnothing 1{,}5\,\text{mm}$ Shore 40A ($40\,\text{cm}$) | **1** | Umlaufende Nut-Feder-Abdichtung Zentralbox |
| **Silikon-Dichtschnur Front**| Silikon-Rundschnur $\varnothing 1{,}5\,\text{mm}$ Shore 40A ($30\,\text{cm}$) | **1** | Umlaufende Deckel-Dichtung Front-Knoten |
| **Kassetten-Flanschdichtungen**| Silikon Formdichtung Shore 40A ($54 \times 18\,\text{mm}$, $1{,}5\,\text{mm}$) | **3** | Stirnseitige Mundloch-Abdichtung an Pod 1, 2 und 3 |
| **EPDM-Dichtkämme** | EPDM Zellkautschuk geschlitzt ($15 \times 8 \times 4\,\text{mm}$) | **2** | Wasserdichte Kabeleinführung im Front-Knoten |
| **Druckausgleichsventil** | Gore Automotive AVS 41 (M8x1.25 Schraubventil) | **1** | Belüftung & Kondensatvermeidung im Main Box Deckel |
| **ePTFE-Klebemembranen** | Gore IP67 Membranpad $\varnothing 6{,}0 \dots 7{,}0\,\text{mm}$ (selbstklebend) | **5** | 3x Entlüftungsdome Pods, 1x Front-Node, 1x Knowles MEMS Port |
| **Lichtleiter (LED)** | Bivar PLPC3-3MM oder Mentor PMMA $\varnothing 3{,}0\,\text{mm}$ ($L=8\,\text{mm}$) | **1** | Wasserdichte Einkopplung der RGB Status-LED im Main Box Deckel |

---

### 2.5 Kategorie E: Vorkonfektionierte COTS-Kabel & Pufferakku (Kein Crimpen!)

| Bauteil | Spezifikation / Typ | Stück | Zweck & Funktion |
| :--- | :--- | :---: | :--- |
| **HD26 IP67 Fertigkabelpeitsche**| Amphenol LTW HD26 Breakout auf M8-Buchsen | **1** | Hauptstecker an Zentralbox, fix und fertig umspritzt |
| **M8 6-Pin PUR-Kabel** | M8 6-Pin A-kodiert Stecker/Buchse (PUR, 1.0 m / 1.5 m) | **3** | Standard Sensor-/Aktorkabel zu Pod 1, 2 und 3 |
| **M8 4-Pin PUR-Kabel** | M8 4-Pin A-kodiert Stecker/Buchse (PUR, 1.5 m) | **1** | Standardkabel zum Front-Knoten (CAN & Signale) |
| **Pufferakku (LiPo USV)** | 1S 3.7V LiPo 1000 mAh mit NTC & Molex Micro-Fit 3.0 | **1** | USV-Notstrompuffer in der Zentralbox (einfach anstecken) |
| **KFZ-Sicherungskabel** | Wasserdichter Flachsicherungshalter mit 2A Sicherung | **1** | Dauerplus-Absicherung (KL30) direkt am Batteriepol |
| **J_ACT Aktuator-Kabelbaum** | Fertiges 8-Pin JST-SH Kabel auf 4x 2-Pin Litzen ($8\,\text{cm}$)| **1–2** | Vorkonfektioniertes Kabel für die 4 Miniatur-Aktuatoren |
| **Miniatur-Aktuatoren** | 5V DC Hubmagnete ($\varnothing 6{,}5 \times 12\,\text{mm}$) mit TPU-Spitze | **4–8** | Mechatronische Tastenbetätigung (4 Stk. pro Smart-Kassette) |
| **J2 Gateway-Kabelbaum** | Fertiges 6-Pin JST-SH Kabel auf Audio- & DC-Schnittstelle | **1–2** | Modularer Kassetten-Kabelbaum (Sena bzw. Cardo Air-Mount) |

---

### 2.6 Kategorie F: Benötigtes Werkzeug (Minimal-Set nach dem IKEA-Prinzip)

Da **weder Löten, noch Crimpen, noch thermisches Einschmelzen von Gewinden** erforderlich ist, reicht haushaltsübliches Standardwerkzeug vollständig aus:

| Werkzeug | Größe / Spezifikation | Zweck beim Zusammenbau |
| :--- | :--- | :--- |
| **Innensechskant-Schlüsselsatz**| **1,5 mm / 2,0 mm / 2,5 mm / 3,0 mm** | Verschrauben aller Gehäuse, Platinen und Klemmen |
| **Torx-Schlüssel / Schraubendreher**| **TX10 / PH1** | Gehäusedeckel und Diebstahlsicherungsschraube |
| **Gabelschlüssel** | **SW 7 mm / SW 8 mm** | Kontern der M4/M5 Muttern bei Rohrschellen |
| **Schere / Cuttermesser** | Standard | Sauberes Ablängen der Silikon-Dichtschnur |
| **Silikonfett** | Liqui Moly / OKS 1110 (kleine Tube) | Leichtes Einölen der Gehäusedichtungen |

> [!TIP]
> **Keine Lötstation, keine Fein-Crimpzangen und kein Heißluftföhn erforderlich!** Alle mechanischen und elektronischen Verbindungen werden ausschließlich gesteckt und geschraubt.

---

## 3. Montage der Baugruppen (Schritt-für-Schritt)

### Schritt 1: Zentralbox (Main Box) montieren
1. **Muttern einlegen:** 4x DIN 934 / DIN 985 M3 Edelstahlmuttern von unten in die Sechskant-Mutternaschen (Nut Pockets) der Unterwanne eindrücken.
2. **Hauptplatine einsetzen:** Fertig bestückte PCBA 01 (`kicad_main_box`) auf die Dämpferdome setzen und mit 4x M2.5 $\times 6\,\text{mm}$ Schrauben handfest fixieren.
3. **Zwischenboden & Akku:** Zwischenboden aufsetzen, 1000 mAh LiPo-Akku in die Wanne legen, Molex Micro-Fit Stecker an `J_BAT` anstecken und mit EPDM-Band sichern.
4. **Dichtung & Deckel:** Silikon-Rundschnur (Ø 1,5 mm) in die Deckelnut einlegen, Gore-Membran aufkleben und Deckel mit 4x M3 $\times 40\,\text{mm}$ Schrauben über Kreuz festziehen ($0{,}8\,\text{Nm}$).


### Schritt 2: Satelliten-Pods 1, 2 und Heck-Pod 3 (Basisgehäuse & Schottwand)
1. **Basisplatine einsetzen:** Die fertig bestückte PCBA 02 (`kicad_pod_base`) in die Führungsnuten des Pod-Basisgehäuses ([`pod_base_housing.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod_base_housing.stl)) einschieben. Die M8 6-Pin IP67 Buchse durch die rückseitige Bohrung führen, Dichtungs-O-Ring aufschieben und von außen die M8-Mutter mit Gabelschlüssel SW 10 handfest anziehen ($1{,}2\,\text{Nm}$).
2. **Auto-Eject Schnappfedern einsetzen:** In die beiden rückseitigen Federtaschen der Schottwand ([`03_pod_bulkhead_partition.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl)) je eine V4A Druckfeder ($\varnothing 4{,}5 \times 15\,\text{mm}$) einstecken.
3. **Schottwand fixieren:** Die Schottwand mit den Federn voran in das Pod-Gehäuse einschieben, bis sie an der inneren Anschlagschulter anliegt. Mit 2x M2 $\times 8\,\text{mm}$ Senkkopfschrauben von außen durch die Gehäusewand bündig verschrauben.
4. **Prüfung:** Die federbelasteten Harwin 6-Pin Docking-Pogo-Pins müssen zentriert und plan durch das Schottwandfenster ragen. Wiederholen für Pod 1, Pod 2 und Pod 3.

### Schritt 3: Multi-Protokoll Gateway-Kassetten 1 & 2 montieren (z. B. Sena & Cardo)
> **Architektur-Grundsatz:** Slot 1 und Slot 2 sind **Multi-Protokoll Mesh-Gateway-Einschübe**, keine isolierten Fahrer- oder Sozius-Headsets. Ein Modul (z. B. Sena SPIDER X Slim in Slot 1) dockt an das Sena Mesh-Netzwerk an, während das zweite Modul (z. B. Cardo Packtalk Edge in Slot 2) parallel das Cardo DMC-Netzwerk bedient. Die Zentralbox vermittelt die Audiodaten zwischen beiden Funkwelten, sodass Fahrer und Sozius mit ihren drahtlosen Helm-Headsets vollwertig an beiden Gruppen-Gesprächen teilnehmen.

1. **Platine einsetzen:** Kassettenplatine PCBA 03 Rev 2.0 in den Kassetten-Schlitten ([`cartridge_base_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl)) einklicken.
2. **Gateway-Inlay & Mechatronik montieren (nach Gerätetyp):**
   * **Klasse S (Smart Modular Cartridge mit Mechatronik • OMB-Referenz: Sena SPIDER X Slim / Cardo Packtalk Edge):**
     * 4x Miniatur-Aktuatoren ($\varnothing 6{,}5 \times 12\,\text{mm}$) mit aufgesteckten elastischen TPU-Schutzkappen in die Führungsbrücke des Inlays ([`cartridge_insert_sena.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) bzw. [`cartridge_insert_cardo.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl)) einlegen.
     * Aktuator-Niederhalteplatte auflegen und mit 4x M2 $\times 6\,\text{mm}$ Senkkopfschrauben sichern.
     * Das vorkonfektionierte 8-polige JST-SH Kabel `J_ACT` von den Aktuatoren direkt auf Header `J_ACT` von PCBA 03 stecken (kein Crimpen/Löten!).
     * Headset in das formschlüssige PA12-Konturbett einlegen und mit dem werkzeuglosen Schnellspann-Niederhalter fixieren.
     * Vorkonfektioniertes J2-Stromkabel (Dauerversorgung 3,85V oder Flachkabel-USB) anstecken.
   * **Klasse A (Sena +Mesh B2M-01 / MeshPort Adapter):**
     * Adapter seitlich in die Quer-Führungsschienen des Inlays einschieben, bis die Rastklinke arretiert.
     * Ultraflaches 90°-Winkelkabel (Micro-USB bzw. USB-C) anstecken (reine 5V-Dauerversorgung).
     * Koax-Pigtail an den SMA-Port schrauben und durch die Frontblende führen.
     * Mit elastischem EPDM-Spannband gegen Erschütterungen sichern.
   * **Klasse D (Hermetische Blindkassette):**
     * Schutzschlitten [`cartridge_insert_blindkassette.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_blindkassette.stl) mit geschlossener Frontblende und O-Ring einsetzen, falls ein Slot ungenutzt bleibt oder als regendichte Dry Box für Kleinteile dient.
3. **Flanschdichtung:** Silikon-Formdichtung auf den Kassettenkragen aufziehen und dünn mit dielektrischem Silikonfett benetzen.

### Schritt 3.1: Montage des magnetischen Diebstahlschutzes (Kassetten-Wippen-Mechanismus)

```
                       MAGNETISCHER DIEBSTAHL-SCHUTZ & AUSWURF-KINEMATIK
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ [Zustand 1: VERRIEGELT]                                                                │
│ Druckfeder drückt Hebelarm ──► 1. Klasse Wippe dreht um M2 Stift ──► Sägezahnkralle     │
│ schwenkt 2.5 mm nach außen in die Gehäusenut. 90°-Sperrflanke blockiert Auszug 100%!   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [Zustand 2: ENTRIEGELN & AUSWURFKICK]                                                  │
│ Externer N52 Neodym-Schlüssel an Gehäusemarkierung anlegen ──► Zieht Ø 6x8 mm Stahl-    │
│ anker nach außen ──► Sägezahn schwenkt bündig ein ──► 2x V4A Druckfedern werfen        │
│ Kassette blitzschnell 25 mm weit aus dem Pod-Gehäuse!                                  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **Stahlanker einpressen:** Den gehärteten ferromagnetischen Stahlstift ($\varnothing 6 \times 8\,\text{mm}$, DIN 6325) in die Querbohrung des hinteren Hebelarms der Wippe ([`cartridge_magnetic_lock_latch.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_magnetic_lock_latch.stl)) bündig einpressen.
2. **Rückstellfeder einsetzen:** Die kleine $\varnothing 3{,}5 \times 10\,\text{mm}$ V4A Druckfeder in die innenseitige Federtasche des hinteren Hebelarms stecken.
3. **Wippe im Schlitten montieren:** Die vormontierte Wippe in die Aussparung an der linken Führungswange des Kassetten-Schlittens ([`cartridge_base_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl)) einsetzen. Den $\varnothing 2{,}0 \times 8\,\text{mm}$ Edelstahl-Zylinderstift (DIN 7) von oben durch die Lagerbohrung durchdrücken.
4. **Funktionsprüfung vor dem Einschieben:**
   * Die Sägezahn-Rastkralle am vorderen Arm muss durch Federkraft $2{,}5\,\text{mm}$ über die Führungsfeder hinausragen.
   * Den N52 Neodym-Blockmagneten außen an die Höhe des Stahlankers halten: Die Wippe kippt um $-4{,}8^\circ$, und die Kralle taucht vollständig bündig in den Schlitten ein.

### Schritt 4: Heck-Kassette Pod 3 & OMM-Radom (LoRa, GNSS & Dreifach-Koaxial-Bypass)
1. **Transceiver-Platine einsetzen:** PCBA 04 (`kicad_rear_pod3`) in den 3. Basisschlitten ([`cartridge_base_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl)) einlegen und mit M2.5 Schrauben sichern.
2. **OMM-Radom montieren:** Das dielektrische Radom ([`cartridge_antenna_bracket_omm.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_antenna_bracket_omm.stl)) aufsetzen.
3. **SMA-Bulkhead-Buchsen montieren (Bypass-Option für externe Antennen):**
   * Die 3x SMA-Flanschbuchsen von außen durch die $\varnothing 6{,}5\,\text{mm}$ Bohrungen der Kassetten-Stirnwand führen (integrierter O-Ring dichtet ab).
   * Von innen Zahnscheibe und Mutter (SW 8) handfest anziehen ($0{,}8\,\text{Nm}$).
   * Mit Kunststoff-Pinzette die Murata MM8030-Koaxstecker senkrecht auf die Umschaltbuchsen aufklicken:
     * `J3` $\rightarrow$ 2.4 GHz OpenMotorMesh Bypass
     * `J4` $\rightarrow$ 868 MHz Semtech SX1262 LoRa Bypass
     * `J5` $\rightarrow$ Multi-GNSS u-blox M9N Bypass (3.3V Phantomspeisung)
4. **Funktionsweise der automatischen Umschaltung:**
   * **Standardbetrieb (ohne externe Antennen):** IP67-Messing-Rändelkappen aufschrauben. Die internen Antennen im Radom arbeiten zu 100 % autark.
   * **Externer Antennenbetrieb:** Beim Aufschrauben einer externen Antenne schaltet die Murata-Buchse mechanisch um (die interne Antenne wird mit $> 25\,\text{dB}$ Isolation weggeschaltet).

### Schritt 4.1: Montage Adventure-Kit (BMW GS vs. BMW GSA / Enduro)

```
                            OPENMOTORBRIDGE ADVENTURE-KIT MOUNTING SUITE
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ BMW R1250 / R1300 GS (STANDARD)                                                        │
│ • Transition-Dock (adventure_transition_dock.stl) in der Sitzbank-Bügelfalte (Ø 28 mm) │
│ • 100 % kofferunabhängig – kein Überstand über die Fahrzeugsilhouette                  │
│ • Rack-Tail Mount (adventure_rack_tail_mount.stl) an der Serien-Gepäckbrücke           │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ BMW R1250 / R1300 GSA (ADVENTURE / TOURATECH KOFFERTRÄGER)                             │
│ • Rohrträger-Klemmschellen-Käfig (adventure_pannier_rack_clamp_base.stl + cap.stl)     │
│ • Montiert Pod 1 & 2 geschützt im Rohrrahmen-Dreieck (Ø 18 mm Edelstahlrohr)           │
│ • Heck-Balkon Gepäckbrücken-Ausleger ragt 65 mm hinter Alutopcase hervor:              │
│   360° freie HF-Sicht für LoRa/Mesh + 45° Astabweiser-Finne für Enduro-Dickicht        │
│ • 36-Zahn Hirth-Formschluss-Gelenk & Garmin Varia Radar-Dock mit Madenschraube         │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **BMW GS (Standard) Montage:**
   * **Pod 1 & 2:** Die Transition-Docks ([`adventure_transition_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_transition_dock.stl)) unterhalb der Sitzbankkante an die Rahmenrohre (Ø 28 mm) klemmen. Die M8 Zuleitungskabel im Unterflurkanal direkt unter die Sitzbank zur Zentralbox führen.
   * **Pod 3:** Auf dem Rack-Tail Mount ([`adventure_rack_tail_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_rack_tail_mount.stl)) an der Gepäckbrücke verschrauben.
2. **BMW GSA (Adventure) Montage:**
   * **Pod 1 & 2:** 1,0 mm EPDM-Schutzstreifen um das Ø 18 mm Kofferträgerrohr wickeln. Unterschale ([`adventure_pannier_rack_clamp_base.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_pannier_rack_clamp_base.stl)) und Kappe ([`adventure_pannier_rack_clamp_cap.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_pannier_rack_clamp_cap.stl)) mit 2x M5 x 30 mm V4A Schrauben und DIN 985 Stoppmuttern über Kreuz mit $4{,}5\,\text{Nm}$ anziehen. Pod-Basisgehäuse an den Augen der Schelle verschrauben.
   * **Pod 3 & Radar (Heck-Balkon):** Ausleger ([`adventure_rack_tail_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_rack_tail_mount.stl)) mit 4x M6 Schrauben an der Gepäckbrücke montieren. Taoglas Antenne an der 45°-Finne ausrichten.
   * **Radar Varia Dock:** Zunge des Garmin Varia Docks ([`radar_varia_gopro_lock_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_varia_gopro_lock_dock.stl)) in die Hirth-Rosette ([`011_gopro_hirth_lock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/011_gopro_hirth_lock.stl)) einrasten ($10^\circ$-Schritte für exakten Radar-Horizont). Mit M5 x 25 mm Schraube und Stoppmutter sichern ($3{,}5\,\text{Nm}$). Varia einklinken und M3 Madenschraube als Diebstahlschutz eindrehen.

### Schritt 4.2: Montage Harley-Davidson Kit (Classic Touring vs. CVO ST / Performance Bagger)

```
                       OPENMOTORBRIDGE HARLEY-DAVIDSON MOUNTING SUITE
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ HARLEY-DAVIDSON TOURING & BAGGER (CLASSIC: STREET GLIDE, ROAD GLIDE, ROAD KING)        │
│ • Kofferdeckel-Docks (saddlebag_lid_dock.stl) auf Hartschalenkoffern (Pod 1 & Pod 2)   │
│ • Touring Fender Console (pod3_touring_fender_console.stl) strömungsgünstig am Fender  │
│ • Kennzeichen-Radarhalter (radar_license_plate_bracket.stl) entkoppelt unter Kennzeichen│
├────────────────────────────────────────────────────────────────────────────────────────┤
│ HARLEY-DAVIDSON CVO ROAD GLIDE ST / PERFORMANCE BAGGER                                 │
│ • Under-Cowl Skeleton Dock (cvo_st_undercowl_skeleton_dock.stl) unter Forged Carbon    │
│   Sitz-Hutze: Schützt vor Hitze und Ausgleichsbehältern der Showa-Stoßdämpfer          │
│ • CVO ST Telemetrie-Finne (cvo_st_telemetry_fin.stl) als Haifischflosse am Heck        │
│ • Zentrische Underfender-Platte (radar_center_underfender_mount.stl) bei Side-Mount    │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **Classic Touring Montage:**
   * **Pod 1 & 2:** Die Kofferdeckel-Docks ([`saddlebag_lid_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/saddlebag_lid_dock.stl)) mit M4 Senkkopfschrauben und rückseitigen Dichtscheiben an den OEM-Befestigungspunkten oder per 3M VHB Tape auf den Kofferdeckeln montieren. Vorkonfektioniertes M8 Kabel durch die Gummitülle in den Koffer und über Schnellkupplung zum Rahmen führen.
   * **Pod 3:** Die Fender-Konsole ([`pod3_touring_fender_console.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod3_touring_fender_console.stl)) flach auf dem Kotflügel zentrieren und verschrauben.
   * **Radar:** Kennzeichen-Halter ([`radar_license_plate_bracket.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_license_plate_bracket.stl)) unter dem Kennzeichenrahmen verschrauben.
2. **CVO ST / Performance Bagger Montage:**
   * **Pod 1 & 2:** Das aufrechte Skeleton Dock ([`cvo_st_undercowl_skeleton_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/cvo_st_undercowl_skeleton_dock.stl)) unter der Einzelsitz-Hutze montieren. Die Pods stehen senkrecht und haben vollen Abstand zu den Ausgleichsbehältern der Federbeine.
   * **Pod 3:** Die aerodynamische Telemetrie-Finne ([`cvo_st_telemetry_fin.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/cvo_st_telemetry_fin.stl)) auf der Heck-Hutze montieren.
   * **Radar:** Die zentrische Underfender-Halterung ([`radar_center_underfender_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_center_underfender_mount.stl)) mittig unter dem gekürzten Heckfender verschrauben.

---

## 5. Universal Front-Knoten Aufbau & Montage

### 5.1 Zusammenbau der Front-Node Box (100 % lötfrei & ohne Einschmelzen)
1. **Muttern einlegen (Nut-Pockets):**
   * 4x DIN 934 / DIN 985 M3 Edelstahlmuttern von unten in die Sechskant-Mutternaschen der Gehäuse-Ecken der Unterwanne ([`front_node_lower_tub.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_lower_tub.stl)) eindrücken.
   * 4x DIN 934 M4 Muttern in die Sechskant-Taschen des AMPS-Lochbilds ($30 \times 38\,\text{mm}$) am Gehäuseboden einlegen.
2. **Akustik-Membran aufkleben:** Hydrophobe Gore ePTFE-Membran über die Schallöffnung des Knowles MEMS Mikrofons kleben.
3. **Platine montieren:** Fertig bestückte Front-Node Platine PCBA 05 (`kicad_front_node`) mit 4x M2.5 Schrauben handfest fixieren.
4. **HF-Antennenmontage (ESP32-S3 2,4 GHz):**
   * Die flexible 2,4-GHz-FPC-Dipolantenne (Molex 146153) in die Klebetasche an der Innenseite des Deckels ([`front_node_upper_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_upper_lid.stl)) einkleben.
   * U.FL-Stecker des Mikro-Koaxialkabels senkrecht auf das ESP32-S3 Modul aufklicken.
5. **Vorkonfektionierte COTS-Kabel einlegen (kein Crimpen!):**
   * **Vordere Öffnung (Südwand für USB):**
     * Kurzes USB-A Flachbandkabel an Port `J6` (CarPlay Dongle / Ottocast) stecken.
     * 1,0 m USB-C Ladekabel an Port `J5` (Handschuhfach) stecken.
     * USB-Host Kabel an `J4` stecken.
   * **Rechte Öffnung (Ostwand):** Elastische Staubschutzkappe ([`front_node_usbc_cap_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_usbc_cap_tpu.stl)) in Port `J7` einsetzen.
   * **Linke Öffnung (Westwand für Strom & Signale):**
     * Fertiges JST-PH 2-Pin Litzenkabel für 12V Bordnetz (KL15 & Masse) an `J1` stecken.
     * Fertiges JST-PH 3-Pin Litzenkabel für CAN-Bus an `J2` stecken.
     * Fertiges JST-PH 2-Pin Litzenkabel vom Lenkertaster an `J3` (PTT) stecken.
6. **Dichtkämme einsetzen & Deckel verschließen:**
   * Dünnen Film Silikonfett auf die elastischen TPU-Dichtkämme ([`front_node_cable_glands_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_cable_glands_tpu.stl)) auftragen und in die Gehäusetaschen schieben.
   * Silikon-Rundschnur (Ø 1,5 mm, $30\,\text{cm}$) in die Deckelnut einlegen.
   * Deckel mit 4x M3 $\times 20\,\text{mm}$ Schrauben über Kreuz festziehen (greifen direkt in die unverlierbaren M3 Muttern in den Nut-Pockets).

### 5.2 Montage am Fahrzeug (4 werkzeuglose & schraubbare Optionen)

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

### 5.3 Elektrischer Anschluss am Motorrad (Plug-and-Play)
* **12V Bordnetz-Einspeisung:** Der Front-Knoten benötigt lediglich eine einzige 2-adrige Zuleitung (KL15 Zündungsplus und Fahrzeugmasse), die am Standlicht, Scheinwerfer oder Cartool-Zubehörstecker abgegriffen wird.
* **Ottocast Dongle:** Wird an USB-A Port `J6` angesteckt und mit 3M Dual-Lock in der Verkleidung fixiert.
* **Handschuhfach:** Ein USB-C Verlängerungskabel führt von Port `J5` ins Handschuhfach für das Smartphone.
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

# 5. Front-Knoten flashen (ESP32-S3)
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
