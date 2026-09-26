# 16 - Bauanleitung, Verkabelung & Fahrzeug-Installation

Dieses Dokument ist die vollständige, praxisorientierte Schritt-für-Schritt-Bauanleitung für den Zusammenbau und die fahrzeugspezifische Montage eines kompletten **OpenMotorBridge (v8.0 Clean Architecture)** Gesamtsystems.

---

## 1. Übersicht des Gesamtkits (Was wird gebaut?)

Ein vollständiges OpenMotorBridge-Fahrzeugkit besteht aus folgenden Kern-Baugruppen:

```text
                      ┌─────────────────────────────────────────┐
                      │    1x ZENTRALE MAIN BOX (IP67)          │
                      │    (Unter der Sitzbank / im Heck)       │
                      │    • Unterwanne + Zwischenboden + Deckel│
                      │    • Hauptplatine PCBA 01 (ESP32-S3)    │
                      │    • Onboard SX1262 LoRa 868 MHz        │
                      │    • Qorvo DW3110 UWB Transceiver       │
                      │    • 2.200 mAh LiPo-Pufferakku (USV)    │
                      └────────────────────┬────────────────────┘
                                           │
                         1x ZENTRALER KABELBAUM (HD26 SEAL-D IP67)
                                           │
          ┌────────────────────────────────┼────────────────────────────────┐
          │                                │                                │
          ▼ Peitsche 1                     ▼ Peitsche 2                     ▼ Peitsche 5
┌──────────────────┐             ┌──────────────────┐             ┌──────────────────┐
│ 1x POD 1 (LINKS) │             │ 1x POD 2 (RECHTS)│             │ 1x HECK-RADAR    │
│ (Rahmen / Koffer)│             │ (Rahmen / Koffer)│             │ (Optional)       │
│ • Pod-Gehäuse    │             │ • Pod-Gehäuse    │             │ • Wheeltec MR20  │
│ • Basis PCBA 02  │             │ • Basis PCBA 02  │             │   oder Garmin    │
│ • KASSETTE 1     │             │ • KASSETTE 2     │             │   Varia RTL515   │
│   (Sena SPIDER   │             │   (Cardo Edge    │             └──────────────────┘
│    X Slim)       │             │    / Swap OMM)   │
└──────────────────┘             └──────────────────┘
                                           ▲
                                           │ Deterministischer UWB Fahrzeug-Backbone
                                           │ (Qorvo DW3110 / 6.5 GHz Ch. 5, < 0.4 ms)
                                           ▼
                                 ┌──────────────────────────────────┐
                                 │ 1x UNIVERSAL FRONT-KNOTEN (IP67) │
                                 │ (Cockpit- & Sensor-Hub, PCBA 05) │
                                 │ • u-blox SAM-M10Q Multi-GNSS     │
                                 │ • TI TMP117 & OPT3001 Sensoren   │
                                 │ • Knowles MEMS Fahrtwind-Sensor  │
                                 │ • 4-Port USB-Hub & Dual USB-PD   │
                                 │ • Batteriefreier Lenker-PTT      │
                                 └──────────────────────────────────┘
```

---

## 2. Bereitstellung vor Montagebeginn (Pre-Assembly Checklist)

Alle Einzelteile, Platinen-Bestelldaten und COTS-Zukauflisten sind detailliert in **[Kapitel 15: Stücklisten & SMT-Fertigungsdaten](15_bom_manufacturing.md)** aufgeführt. Vor Montagebeginn sicherstellen, dass folgende Baugruppen bereitliegen:

* [ ] **3D-Druckteile (MJF PA12 schwarz oder FDM ASA/PET-CF):**
  * 1x Main Box (Unterwanne mit UWB-Bodentasche $11 \times 11 \times 0{,}6\,\text{mm}$, Zwischenboden mit LiPo-Wanne, Deckel mit LoRa FXP895 Tasche $110 \times 20 \times 0{,}8\,\text{mm}$)
  * 2x Pod-Basisgehäuse & 2x Pod-Schottwände (symmetrisch für Pod 1 und Pod 2)
  * 2x Kassetten-Basisschlitten, Inlays (Sena SPIDER X Slim, Cardo Packtalk Edge, Swap OMM oder Blindkassette) & 2x Rastwippen
  * 1x Front-Knoten (Unterwanne mit UWB-Bodentasche und AMPS-Nut-Pockets, Deckel, TPU-Dichtkämme & USB-C Kappe)
  * 1x Fahrzeugspezifisches Montage-Kit (BMW GS Klemmen & `adventure_rack_radar_mount.stl` / Harley Kofferdeckel-Docks & Kennzeichen-Radarhalter / Support-Car `car_sun_visor_pod_clip.stl`)
* [ ] **Vollautomatisch bestückte Platinen (von JLCPCB / Eurocircuits):**
  * 1x PCBA 01 (Zentralbox mit LoRa SX1262 und DW3110 UWB)
  * 2x PCBA 02 (Pod-Base, symmetrisch für Pod 1 und Pod 2)
  * 2x PCBA 03 (Smart Modular Cartridge mit CH32V003 und 4x AO3400 N-MOSFETs)
  * 1x PCBA 05 (Front-Knoten mit DW3110 UWB)
  * *(Optional: 1x PCBA 08 Radar 2.0 Sub-MCU, PCBA 06 MagSafe Dock, PCBA 07 Smart-Keyfob)*
* [ ] **V4A Edelstahl-Normteile & Federn (IKEA-Prinzip – 100 % lötfrei):**
  * 8x DIN 934 / DIN 985 M3 Edelstahlmuttern (für Gehäuse-Nut-Pockets)
  * 4x DIN 934 M4 Muttern (für AMPS-Nut-Pockets in Front-Node Wanne)
  * 4x M3 x 40 mm Schrauben (Zentralbox), 4x M3 x 20 mm Schrauben (Front-Node)
  * 8x M2.5 x 6 mm Platinenschrauben, 4x M2 x 8 mm Senkkopf (Schottwände), 8x M2 x 6 mm (Kassetten)
  * 2x DIN 7 M2 x 8 mm Zylinderstifte (Wippenachsen), 2x DIN 6325 Ø 6 x 8 mm gehärtete Stahlanker
  * 2x Wippen-Rückstellfedern, 4x Auto-Eject Druckfedern, 1x N52 Neodym-Entriegelungsschlüssel
* [ ] **Dichtungen, Pufferakku & Antennen:**
  * Silikon-Rundschnur Ø 1,5 mm Shore 40A ($40\,\text{cm}$ Main Box, $30\,\text{cm}$ Front-Knoten)
  * 2x Silikon-Flanschdichtungen für Pod 1 & 2 Mundlöcher, Gore ePTFE Membranpads
  * **1x 1S LiPo Flat-Pack 2.200 mAh** ($68 \times 39 \times 5{,}0\,\text{mm}$) mit Molex Micro-Fit 3.0 Stecker
  * **2x Taoglas FXUWB10 UWB Flex-Antennen** mit 20 mm U.FL Kabel
  * **1x Taoglas FXP895 LoRa 868 MHz Flex-Antenne** mit 50 $\Omega$ U.FL Kabel
  * **1x u-blox SAM-M10Q Multi-GNSS Modul** mit integrierter Patchantenne (Qwiic I2C)
  * **1x TI TMP117 & 1x TI OPT3001 Sensoren** (Qwiic I2C)
* [ ] **Vorkonfektionierte COTS-Kabel (kein Crimpen nötig):**
  * 1x HD26 SEAL-D IP67 4-Abzweig Kabelpeitsche (Pod 1, Pod 2, 12V Bordnetz, Peitsche 5 Heckradar)
  * 2x M8 6-Pin PUR-Kabel (1.0 m / 1.5 m)
  * 1x M8 4-Pin PUR-Kabel (Peitsche 5 für Radar)
  * JST-SH Kassetten-Kabelbäume (8-Pin `J_ACT` für Hubmagnete, 6-Pin `J2` für Audio/DC)
* [ ] **Werkzeuge:**
  * Innensechskantschlüsselsatz (1.5 / 2.0 / 2.5 / 3.0 mm), Torx TX10 / PH1 Schraubendreher, Gabelschlüssel SW 7 / 8 / 10 mm, Cuttermesser, dielektrisches Silikonfett

---

## 3. Montage der Baugruppen (Schritt-für-Schritt)

### Schritt 1: Zentralbox (Main Box) montieren
1. **Muttern einlegen:** 4x DIN 934 / DIN 985 M3 Edelstahlmuttern von unten in die Sechskant-Mutternaschen der Unterwanne ([`main_box_lower_case.stl`](../../hardware/cad/stl/01_main_box/main_box_lower_case.stl)) eindrücken.
2. **UWB-Antenne im Boden installieren:**
   * Die flexible UWB-Antenne (Taoglas FXUWB10, $11 \times 11 \times 0{,}6\,\text{mm}$) in die Bodentasche der Unterwanne einlegen und mit der rückseitigen 3M-Klebeschicht fixieren.
   * Das 20 mm kurze U.FL Mikro-Koaxialkabel senkrecht nach oben führen.
3. **Hauptplatine einsetzen:**
   * Fertig bestückte PCBA 01 auf die Dämpferdome setzen.
   * U.FL-Stecker des UWB-Kabels senkrecht auf die Buchse `ANT2` auf der Platinenunterseite (`B.Cu`) aufklicken.
   * Platine mit 4x M2.5 $\times 6\,\text{mm}$ Schrauben handfest fixieren.
4. **LoRa-Antenne im Deckel installieren:**
   * Die flexible LoRa-Antenne (Taoglas FXP895, $110 \times 20 \times 0{,}8\,\text{mm}$) in die Deckeltasche des Gehäusedeckels ([`main_box_lid.stl`](../../hardware/cad/stl/01_main_box/main_box_lid.stl)) einkleben.
   * U.FL-Koaxialkabel an die Buchse `ANT1` auf der Oberseite der PCBA 01 anstecken.
5. **Zwischenboden & 2.200 mAh LiPo-Akku:** Den Zwischenboden ([`main_box_mid_tray.stl`](../../hardware/cad/stl/01_main_box/main_box_mid_tray.stl)) aufsetzen. Den **2.200 mAh Flat-LiPo-Akku** in die Wanne einlegen, das Molex Micro-Fit Kabel an `J_BAT` anstecken und mit EPDM-Band sichern.
6. **Dichtung & Deckel:** Silikon-Rundschnur (Ø 1,5 mm, $40\,\text{cm}$) dünn mit Silikonfett einreiben und in die Deckelnut einlegen. Gore-Membran auf den Belüftungssitz kleben. Den Deckel vorerst nur lose aufsetzen.

---

### Schritt 2: Satelliten-Pods 1 & 2 montieren (2x identisch)
1. **Basisplatine einsetzen:** Die fertig bestückte PCBA 02 in die Führungsnuten des Pod-Basisgehäuses ([`pod_base_housing.stl`](../../hardware/cad/stl/02_pod_base/pod_base_housing.stl)) einschieben. Die M8 6-Pin IP67 Buchse durch die rückseitige Bohrung führen, O-Ring aufschieben und die M8-Mutter mit Gabelschlüssel SW 10 handfest anziehen ($1{,}2\,\text{Nm}$).
2. **Auto-Eject Schnappfedern einsetzen:** In die beiden rückseitigen Federtaschen der Schottwand ([`03_pod_bulkhead_partition.stl`](../../hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl)) je eine V4A Druckfeder ($\varnothing 4{,}5 \times 15\,\text{mm}$) einstecken.
3. **Schottwand fixieren:** Die Schottwand mit den Federn voran in das Pod-Gehäuse einschieben und mit 2x M2 $\times 8\,\text{mm}$ Senkkopfschrauben von außen bündig verschrauben.
4. **Prüfung:** Die 6-polige Buchsenleiste `J1` schließt zentriert im Schottwandkragen ab. Wiederholen für Pod 2.

---

### Schritt 3: Multi-Protokoll Gateway-Kassetten 1 & 2 montieren
1. **Platine einsetzen:** Kassettenplatine PCBA 03 Rev 2.0 in den Kassetten-Schlitten ([`cartridge_base_sled.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl)) einklicken.
2. **Gateway-Inlay & Mechatronik montieren:**
   * **Slot 1 (Sena SPIDER X Slim Inlay):**
     * 4x Miniatur-Aktuatoren ($\varnothing 6{,}5 \times 12\,\text{mm}$) mit TPU-Kappen in die Führungsbrücke des Inlays ([`cartridge_insert_sena.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl)) einlegen.
     * Niederhalteplatte mit 4x M2 $\times 6\,\text{mm}$ Senkkopfschrauben sichern.
     * Vorkonfektioniertes 8-Pin Kabel `J_ACT` auf Header `J_ACT` von PCBA 03 stecken.
     * Sena SPIDER X Slim einlegen; die direkte Micro-Kabelpeitsche an `J2` von PCBA 03 anstecken (zero pogo pins!).
   * **Slot 2 (Cardo Packtalk Edge Inlay / Swap OMM):**
     * 4x Aktuatoren in [`cartridge_insert_cardo.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl) montieren und an `J_ACT` anstecken.
     * Cardo Packtalk Edge im Air-Mount Bett fixieren und Micro-Kabelpeitsche an `J2` stecken.
3. **Flanschdichtung:** Silikon-Formdichtung auf den Kassettenkragen aufziehen und dünn mit Silikonfett benetzen.

---

### Schritt 3.1: Montage des magnetischen Diebstahlschutzes (Wippen-Mechanismus)
1. **Stahlanker einpressen:** Gehärteten Stahlstift ($\varnothing 6 \times 8\,\text{mm}$, DIN 6325) in die Querbohrung der Wippe ([`cartridge_magnetic_lock_latch.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_magnetic_lock_latch.stl)) bündig einpressen.
2. **Rückstellfeder einsetzen:** Die kleine $\varnothing 3{,}5 \times 10\,\text{mm}$ Druckfeder in die innenseitige Federtasche stecken.
3. **Wippe im Schlitten montieren:** Vormontierte Wippe in die linke Führungswange des Kassetten-Schlittens einsetzen und mit dem $\varnothing 2{,}0 \times 8\,\text{mm}$ Edelstahl-Zylinderstift (DIN 7) lagern.
4. **Funktionsprüfung:** Sägezahn ragt $2{,}5\,\text{mm}$ heraus; bei Annäherung des N52 Neodym-Magneten schwenkt die Wippe bündig ein.

---

### Schritt 4: Universal Front-Knoten (PCBA 05) zusammenbauen
1. **Muttern einlegen:** 4x M3 Edelstahlmuttern in die Gehäuse-Ecken und 4x M4 Muttern in das AMPS-Bohrbild der Unterwanne ([`front_node_lower_tub.stl`](../../hardware/cad/stl/04_front_node/front_node_lower_tub.stl)) einlegen.
2. **UWB-Antenne im Boden installieren:**
   * Taoglas FXUWB10 Flex-Antenne in die Bodentasche der Unterwanne einkleben.
   * U.FL-Kabel nach oben führen.
3. **Platine montieren:**
   * Fertig bestückte PCBA 05 auf die Dämpferdome setzen.
   * UWB-Kabel an die U.FL-Buchse auf `B.Cu` aufklicken.
   * Platine mit 4x M2.5 Schrauben fixieren.
4. **Cockpit-Sensoren anschließen (J12 Qwiic):**
   * u-blox SAM-M10Q Multi-GNSS Modul (mit integrierter $15 \times 15\,\text{mm}$ Patchantenne) per Qwiic-Kabel an `J12` anstecken.
   * TI TMP117 Temperatursensor und TI OPT3001 Lichtsensor per Daisy-Chain am Qwiic-Bus im Kaltluft-Staudruckbereich platzieren.
5. **Akustik-Membran:** Hydrophobe Gore ePTFE-Membran über die Schalleintrittsöffnung des Sipeed/Knowles MEMS Mikrofons (`MIC1`) kleben.
6. **Kabel einlegen & Gehäuse vorbereiten:**
   * 12V KL15 & GND an `J1`, CAN-Bus an `J2`, PTT-Taster an `J3`, CP2AA Dongle an `J6`, Smartphone Fast-Charge an `J5`.
   * TPU-Dichtkämme einsetzen, Silikon-Rundschnur (Ø 1,5 mm, $30\,\text{cm}$) in Deckelnut einlegen und Deckel vorerst lose auflegen.

---

## 4. Tisch-Testaufbau & Dry-Run (Werkstatt / Schreibtisch) VOR der Bike-Montage

Das Gesamtsystem lässt sich auf der Werkbank mit Standard-USB-C-Kabeln zu 100 % testen, flashen und koppeln:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│       OPENMOTORBRIDGE TISCH-TESTAUFBAU & DRY-RUN (BENCH-LABOR SETUP)        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [ 230V USB-Netzteil / Powerbank / Laptop (5V / ≥ 2.4A) ]                  │
│       │                      │                      │                       │
│  USB-C│Kabel 1          USB-C│Kabel 2          USB-C│Kabel 3                │
│       ▼                      ▼                      ▼                       │
│  ┌───────────────┐     ┌───────────────┐      ┌───────────────┐             │
│  │  ZENTRALBOX   │     │  FRONT-NODE   │      │ SATELLIT-POD  │             │
│  │   (PCBA 01)   │     │   (PCBA 05)   │      │ (Pod 1 / 2)   │             │
│  │  Port J7 USB-C│     │  Port J5 USB-C│      │ M8 Adapter    │             │
│  └───────┬───────┘     └───────┬───────┘      └───────┬───────┘             │
│          │                     │                      │                     │
│          │   UWB Funk-Backbone │                      │ 1-Wire & Direct-DC  │
│          │◄───────────────────►│                      ▼                     │
│          │  (6.5 GHz, <0.4 ms) │             ┌───────────────────┐          │
│          │                     │             │ SMART KASSETTE    │          │
│          │                     │             │ (Sena / Cardo)    │          │
│          │                     │             └────────┬──────────┘          │
│          │ WebBLE / WebSerial  │                      │                     │
│          ▼                     ▼                      ▼                     │
│    [ SMARTPHONE / LAPTOP MIT PWA ]             [ FAHRER-HELM ]              │
│    (Chrome / Edge: Flasher & Dashboard)        (Bluetooth gekoppelt)        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.1 Der geführte 4-Punkte IKEA Smoke-Test
In der PWA (über WebSerial oder WebBLE) den Diagnosetest ausführen:
1. [x] **Bordnetz & USV (Check 1):** LM5164 Buck-Schiene aktiv (5.04 V), USV-LiPo (2.200 mAh) lädt mit 4.18 V.
2. [x] **Kassetten & Aktuatoren (Check 2):** 1-Wire Erkennung von Slot 1 (Sena) und Slot 2 (Cardo), mechatronischer Klicktest der 4 Aktuatoren ("Klack-Klack-Klack-Klack").
3. [x] **Front-Knoten & UWB Backbone (Check 3):** UWB-Link aktiv ($< 0{,}4\,\text{ms}$ Latenz), SAM-M10Q 3D-Fix, TMP117 Temperatur, Knowles MEMS Pegel & PTT-Tastendruck.
4. [x] **LoRa 868 MHz & Radar (Check 4):** SX1262 LoRa Ping-Echo und UART-Kommunikation zum Heckradar auf Peitsche 5.

Erst wenn alle 4 Checks grün leuchten, die Gehäusedeckel mit den M3-Schrauben über Kreuz festziehen.

---

## 5. Fahrzeugspezifische Montage & Verkabelung am Motorrad

### 5.1 Montage Harley-Davidson Plattform (Touring, CVO ST, Road King)
* **Zentralbox:** Unter der Fahrersitzbank auf der Rahmenbrücke vor der Batterie auf 4x M4 Silentblöcken verschrauben.
* **Pod 1 & Pod 2:** Auf den Hartschalenkoffern mittels Kofferdeckel-Docks ([`saddlebag_lid_dock.stl`](../../hardware/cad/stl/02_pod_base/saddlebag_lid_dock.stl)) montieren.
* **Heck-Radar:** Entkoppelter Kennzeichen-Radarhalter ([`radar_license_plate_bracket.stl`](../../hardware/cad/stl/02_pod_base/radar_license_plate_bracket.stl)) unter dem Kennzeichenrahmen, angeschlossen an Peitsche 5 des HD26-Kabelbaums.
* **Front-Knoten:** In der Verkleidung (Batwing / Sharknose) oder Nacelle verschraubt; 12V von Standlicht/Zubehör; CAN-Bus lokal an J2 (oder an Zentralbox unter der Sitzbank).

### 5.2 Montage Adventure-Plattform (BMW GS / GSA Familie)
* **Zentralbox:** Im Rahmendreieck unter der Fahrersitzbank auf 4x M4 Silentblöcken montieren.
* **Cockpit & Front-Knoten:** An der Ø 12 mm GPS-Querstrebe über dem TFT befestigt; 12V über originalen BMW Cartool-Stecker.
* **Pod 1 & Pod 2:**
  * *Option A (Vario-Koffer / GS Standard):* Transition-Docks ([`adventure_transition_dock_base.stl`](../../hardware/cad/stl/02_pod_base/adventure_transition_dock_base.stl)) in der Sitzbank-Bügelfalte (Ø 28 mm Rahmenrohr) verbunden mit der Sattelbrücke ([`adventure_underseat_cross_rail.stl`](../../hardware/cad/stl/02_pod_base/adventure_underseat_cross_rail.stl)).
  * *Option B (Edelstahl-Rohrkofferträger / GSA):* Heavy-Duty GSA Cage Docks ([`adventure_gsa_cage_dock_body.stl`](../../hardware/cad/stl/02_pod_base/adventure_gsa_cage_dock_body.stl)) im 45 mm Totraum des Trägers.
* **Heck-Radar:** Minimaler Halter ([`adventure_rack_radar_mount.stl`](../../hardware/cad/stl/02_pod_base/adventure_rack_radar_mount.stl)) direkt unter der GS-Gepäckbrücke für Garmin Varia oder Wheeltec MR20 auf Peitsche 5.

### 5.3 Begleitfahrzeug- & Autokolonnen-Installation (Support-Car / Van)
* **Pod 1 & Pod 2:** Werden mit je einem Schnellwechsel-Clip ([`car_sun_visor_pod_clip.stl`](../../hardware/cad/stl/05_accessories/car_sun_visor_pod_clip.stl)) an Fahrer- und Beifahrer-Sonnenblende geklemmt.
  * Modus A (Begleitfahrzeug für Bike-Gruppe): Pod 1 = Sena SPIDER X Slim, Pod 2 = Cardo Packtalk Edge.
  * Modus B (Reine Autokolonne): Pod 1 = OMM 2.4 GHz Swap Cartridge, Pod 2 = Midland PMR446 Funkkassette.
* **Zentralbox:** In der 15°-Dashboard-Keilaufnahme auf der Mittelkonsole.
* **SAM-M10Q GNSS:** Auf dem Armaturenbrett hinter der Windschutzscheibe.
* **Audio-Integration:** USB-C Audio-Link zum Autoradio für Gruppenfunk über die Fahrzeuglautsprecher.
* **Telemetrie:** Drahtloser BLE-OBD2 Dongle im Fahrerfußraum.

---

## 6. Endabnahme, Probefahrt & Sign-Off Checkliste

1. **Zündungs-Check (KL15):**
   * Zündung EIN: Zentralbox und Front-Node erwachen synchron in $< 800\,\text{ms}$.
   * UWB-Backbone etabliert sich sofort (grüne Sync-LED).
   * Spiegel-LEDs (`J9`) quittieren für 1,0 s (Amber).
2. **Kassetten-Check:**
   * Tasten an Lenkerarmatur / Front-Node betätigen: Aktuatoren schalten zuverlässig durch.
3. **Totwinkel-Radar Test:**
   * Bei Annäherung eines Fahrzeugs von hinten leuchten Spiegel-LEDs bernsteinfarben; bei Spurwechsel mit Blinker blitzen sie mit 8 Hz Rot/Amber.
4. **Probefahrt & Dynamik:**
   * Fahrtwind-Mikrofon regelt Intercom-Lautstärke stufenlos und knackfrei nach.
   * Raised-Cosine Ducking senkt Musik bei Funksprüchen weich um $-18\,\text{dB}$ ab.
5. **Zündung AUS:**
   * Automatischer Action-Cam Stop via Bluetooth LE.
   * USV schaltet Zentralbox sauber ab; Diebstahl-Sentry auf LoRa 868 MHz bleibt 24/7 aktiv.
