# 16 - Bauanleitung, Verkabelung & Fahrzeug-Installation

Dieses Dokument ist die vollständige, praxisorientierte Schritt-für-Schritt-Bauanleitung für den Zusammenbau und die fahrzeugspezifische Montage eines kompletten **OpenMotorBridge (v8.0 Clean Architecture)** Gesamtsystems.

---

## 1. Übersicht des Gesamtkits (Was wird gebaut?)

Ein vollständiges OpenMotorBridge-Fahrzeugkit besteht aus folgenden Kern-Baugruppen:

```text
                      +-----------------------------------------+
                      |    1x ZENTRALE MAIN BOX (IP67)          |
                      |    (Unter der Sitzbank / im Heck)       |
                      |    * Unterwanne + Zwischenboden + Deckel|
                      |    * Hauptplatine PCBA 01 (ESP32-S3)    |
                      |    * Onboard SX1262 LoRa 868 MHz        |
                                     +--------------------+--------------------+
                                           |
                          1x ZENTRALER KABELBAUM (DEUTSCH DTM-12 IP67/IP69K)
                                           |
          +--------------------------------+--------------------------------+
          |                                |                                |
          v Peitsche 1 (2-Draht DC 5V)     v Peitsche 2 (2-Draht DC 5V)     v Peitsche 4 (2-Draht DC 12V)
+------------------+             +------------------+             +------------------+
| 1x BUCHT 1 LINKS |             | 1x BUCHT 2 RECHTS|             | 1x HECK-RADAR 2.0|
| (Rahmen / Koffer)|             | (Rahmen / Koffer)|             | (Kennzeichen/Heck)
| * Universal-Pod  |             | * Universal-Pod  |             | * Wheeltec MR20  |
|   (Monocoque PA12|             |   (Monocoque PA12|             |   77GHz (PCBA 08)|
|    kein PCB 02!) |             |    kein PCB 02!) |             | * 36x Warn-LEDs  |
| * 2 Federkontakte|             | * 2 Federkontakte|             | * UWB Telemetrie |
| * KASSETTE 1     |             | * KASSETTE 2     |             |   & LED-Makros   |
|   (Sena / Cardo /|             |   (Sena / Cardo /|             +--------+---------+
|    OMM / Midland)|             |    OMM / Midland)|                      |
+--------+---------+             +--------+---------+                      |
         |                                |                                |
         | UWB Steuer- & Telemetrielink   | UWB Steuer- & Telemetrielink   | UWB Radar-Link
         +----------------+---------------+--------------------------------+
                          | Deterministischer All-UWB Fahrzeug-Backbone
                          | (Qorvo DW3110 / 6.5 GHz Ch. 5, < 0.4 ms)
                          v
                 +----------------------------------+
                 | 1x UNIVERSAL FRONT-KNOTEN (IP67) |
                 | (Cockpit- & Sensor-Hub, PCBA 05) |
                 | * u-blox SAM-M10Q Multi-GNSS     |
                 | * TI TMP117 & OPT3001 Sensoren   |
                 | * Knowles MEMS Fahrtwind-Sensor  |
                 | * 4-Port USB-Hub & Dual USB-PD   |
                 | * Batteriefreier Lenker-PTT      |
                 +----------------------------------+
```

---

## 2. Bereitstellung vor Montagebeginn (Pre-Assembly Checklist)

> [!TIP]
> **Geprüfte Passungsmaße & 100 % lötkolbenfreie Montage (IKEA-Prinzip):**  
> Alle 3D-Druckteile (`.scad` / `.stl`) wurden mit definierten Toleranzen ($+0{,}15\,\text{mm}$ für HP MJF PA12 bzw. ASA/PET-CF) konstruiert. Auf das fehleranfällige Einschmelzen von Gewindebuchsen (Ruthex) wurde im gesamten System konsequent verzichtet: Alle Verschraubungen nutzen formschlüssige **DIN 934 Sechskant-Mutterntaschen** (einfach von Hand einlegen) oder direkte Kunststoff-Gewindefurchung in Kernlöchern.

Alle Einzelteile, Platinen-Bestelldaten und COTS-Zukauflisten sind detailliert in **[Kapitel 15: Stücklisten & SMT-Fertigungsdaten](15_bom_manufacturing.md)** aufgeführt. Vor Montagebeginn sicherstellen, dass folgende Baugruppen bereitliegen:

* [ ] **3D-Druckteile (MJF PA12 schwarz oder FDM ASA/PET-CF):**
  * 1x Main Box (Unterwanne mit UWB-Bodentasche $11 \times 11 \times 0{,}6\,\text{mm}$, Zwischenboden mit LiPo-Wanne, Deckel mit LoRa FXP895 Tasche $110 \times 20 \times 0{,}8\,\text{mm}$)
  * 2x Pod-Basisgehäuse & 2x Pod-Schottwände (symmetrisch für Bucht 1 und Bucht 2, ohne interne Platine)
  * 2x Kassetten-Basisschlitten, Inlays (Sena SPIDER X Slim, Cardo Packtalk Edge, Swap OMM oder Blindkassette) & 2x Rastwippen
  * 1x Front-Knoten (Unterwanne mit UWB-Bodentasche und AMPS-Nut-Pockets, Deckel, TPU-Dichtkämme & USB-C Kappe)
  * 1x Fahrzeugspezifisches Montage-Kit (BMW GS Klemmen & `adventure_rack_radar_mount.stl` / Harley Kofferdeckel-Docks & Kennzeichen-Radarhalter / Support-Car `car_sun_visor_pod_clip.stl`)
* [ ] **Vollautomatisch bestückte Platinen (von JLCPCB / Eurocircuits - 6 PCBAs):**
  * 1x PCBA 01 (Zentralbox mit LoRa SX1262, DW3110 UWB, SW1 Taster und DTM-12 Header)
  * 2x PCBA 03 (Universal Smart Cartridge Rev 3.0 All-UWB mit DW3110 UWB, MCU und 4x AO3400A MOSFETs, 2-seitig SMT)
  * 1x PCBA 05 (Front-Knoten mit DW3110 UWB)
  * *(Optional: 1x PCBA 08 Radar 2.0 Sub-MCU mit DW3110 UWB, PCBA 06 MagSafe Dock, PCBA 07 Smart-Keyfob)*
  * *(Hinweis: PCBA 02 und PCBA 04 sind ersatzlos entfallen).*
* [ ] **V4A Edelstahl-Normteile & Federn (IKEA-Prinzip - 100 % lötfrei):**
  * 8x DIN 934 / DIN 985 M3 Edelstahlmuttern (für Gehäuse-Nut-Pockets)
  * 6x DIN 934 M4 Muttern (4x AMPS-Nut-Pockets in Front-Node Wanne, 2x Radar 2.0 Heck-Mutterntaschen)
  * 4x M3 x 40 mm Schrauben (Zentralbox), 4x M3 x 20 mm Schrauben (Front-Node)
  * 8x M2.5 x 6 mm Platinenschrauben, 4x M2 x 8 mm Senkkopf (Schottwände), 8x M2 x 6 mm (Kassetten)
  * 2x DIN 7 M2 x 8 mm Zylinderstifte (Wippenachsen), 2x DIN 6325 Ø 6 x 8 mm gehärtete Stahlanker
  * 2x Wippen-Rückstellfedern, 4x Auto-Eject Druckfedern, 1x N52 Neodym-Entriegelungsschlüssel
  * 4x Vergoldete Blattfederkontakte (Keystone / Mill-Max) für Pod 1 & 2 Stromzuführung
* [ ] **Dichtungen, Pufferakku & Antennen:**
  * Silikon-Rundschnur Ø 1,5 mm Shore 40A ($40\,\text{cm}$ Main Box, $30\,\text{cm}$ Front-Knoten)
  * 2x Silikon-Flanschdichtungen für Pod 1 & 2 Mundlöcher, Gore ePTFE Membranpads
  * **1x 1S LiPo Flat-Pack 2.200 mAh** ($68 \times 39 \times 5{,}0\,\text{mm}$) mit Molex Micro-Fit 3.0 Stecker
  * **Taoglas FXUWB10 UWB Flex-Antennen** mit 20 mm U.FL Kabel (Zentralbox, Front-Node, Kassetten)
  * **1x Taoglas FXP895 LoRa 868 MHz Flex-Antenne** mit 50 $\Omega$ U.FL Kabel
  * **1x u-blox SAM-M10Q Multi-GNSS Modul** mit integrierter Patchantenne (Qwiic I2C)
  * **1x TI TMP117 & 1x TI OPT3001 Sensoren** (Qwiic I2C)
* [ ] **Vorkonfektionierte COTS-Kabel (kein Crimpen nötig):**
  * 1x Deutsch DTM-12 IP67/IP69K Zentral-Kabelbaum (reine 2-Draht DC-Peitschen für Pod 1, Pod 2, Radar sowie 12V Bordnetz & CAN)
  * 2-Pin JWPF / Superseal Steckverbinder für Pod- und Radar-Zuleitungen
  * JST-SH Kassetten-Kabelbäume (8-Pin `J_ACT` für Hubmagnete)
* [ ] **Werkzeuge:**
  * Innensechskantschlüsselsatz (1.5 / 2.0 / 2.5 / 3.0 mm), Torx TX10 / PH1 Schraubendreher, Gabelschlüssel SW 7 / 8 / 10 mm, Cuttermesser, dielektrisches Silikonfett

---

## 3. Montage der Baugruppen (Schritt-für-Schritt)

### Schritt 1: Zentralbox (Main Box) montieren
1. **Muttern einlegen:** 4x DIN 934 / DIN 985 M3 Edelstahlmuttern von unten in die Sechskant-Mutternaschen der Unterwanne ([`main_box_lower_case.stl`](../../hardware/cad/stl/01_main_box/main_box_lower_case.stl)) eindrücken.
2. **UWB-Antenne im Boden installieren:**
   * Die flexible UWB-Antenne (Taoglas FXUWB10, $11 \times 11 \times 0{,}6\,\text{mm}$) in die Bodentasche der Unterwanne einlegen und mit der rückseitigen 3M-Klebeschicht fixieren.
   * Das 20 mm kurze U.FL Mikro-Koaxialkabel senkrecht nach oben führen. Da der DW3110 UWB-Transceiver und die Buchse `ANT2` direkt auf der Platinenunterseite (`B.Cu`) liegen, verbindet das Kabel die Antenne unmittelbar und ohne Querung der Leiterplatte.
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

### Schritt 2: Satelliten-Pods 1 & 2 montieren (2x identisch, ohne interne Platine)
1. **2-Draht-DC-Zuleitung einführen:** Die 2-adrige Gleichstromleitung (+5V und GND) durch die rückseitige Kabeldurchführung des Pod-Basisgehäuses ([`pod_base_housing.stl`](../../hardware/cad/stl/02_pod_base/pod_base_housing.stl)) führen und abdichten.
2. **Federkontakte montieren:** Die beiden Leitungsadern mit den vergoldeten Federkontakten (Keystone / Mill-Max) im Schachtboden verbinden.
3. **Auto-Eject Schnappfedern einsetzen:** In die beiden rückseitigen Federtaschen der Schottwand ([`03_pod_bulkhead_partition.stl`](../../hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl)) je eine V4A Druckfeder ($\varnothing 4{,}5 \times 15\,\text{mm}$) einstecken.
4. **Schottwand fixieren:** Die Schottwand mit den Federn voran in das Pod-Gehäuse einschieben und mit 2x M2 $\times 8\,\text{mm}$ Senkkopfschrauben von außen bündig verschrauben.
5. **Prüfung:** Die beiden vergoldeten Federkontakte ragen federnd in den Aufnahmeschacht. Keine Buchsen, keine internen Platinen nötig. Wiederholen für Pod 2.

---

### Schritt 3: Multi-Protokoll Gateway-Kassetten 1 & 2 montieren
1. **Platine einsetzen:** Kassettenplatine PCBA 03 Rev 3.0 (beidseitig bestückt, mit DW3110 UWB) in den Kassetten-Schlitten ([`cartridge_base_sled.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl)) einklicken.
2. **Mechatronik-Aktuatoren & Niederhalteplatte montieren:**
   * 4x Miniatur-Hubmagnete ($\varnothing 6{,}5 \times 12\,\text{mm}$) mit dämpfenden TPU-Tastspitzen (`actuator_silicone_tip.stl`) in die vier Passbohrungen der Führungsbrücke des Inlays ([`cartridge_insert_sena.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) bzw. [`cartridge_insert_cardo.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl)) einstecken.
   * **Aktuator-Verkabelung an `J_ACT` (8-Pin JST-SH 1.0 mm):**
     * Das vorkonfektionierte 8-Pin Kabel auf den Header `J_ACT` aufstecken.
     * Die vier verdrillten Adernpaare (AWG30 Silikon) an die vier Hubmagnete führen (Paar 1 = Taste +, Paar 2 = Taste -, Paar 3 = Center/Phone, Paar 4 = Mesh/Pairing).
   * **Niederhalteplatte verschrauben:** Die PA12-Niederhalteplatte ([`cartridge_retainer_plate.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_retainer_plate.stl)) plan über die Hubmagnete legen und mit **4x M2 $\times 6\,\text{mm}$ Senkkopfschrauben (DIN 7991)** fest anziehen. Die Aktuatoren sitzen nun absolut spielfrei und rüttelfest im Schlitten.
3. **Gateway-Inlay & OEM-Adapterkabel anschließen (`J_AUDIO_PWR` / `J2` 6-Pin JST-SH):**
   * **Bucht 1 (Sena SPIDER X Slim Inlay - OMB Referenz K2a):**
     * 6-Pin JST-SH Adapterkabel auf Header `J_AUDIO_PWR` stecken.
     * 2-Pin Micro-JST Stecker an die externe Akkuzuleitung des SPIDER X Slim anstecken (liefert permanente 3.85V Direct-DC Speisung ohne Akku im Pod!).
     * 2.5 mm Klinkenstecker an den Mikrofoneingang und 3.5 mm Klinkenstecker an den Lautsprecherausgang der Sena-Kabelpeitsche anstecken.
     * SPIDER X Slim formschlüssig in das PA12-Nest einlegen. *(Audio wird wahlweise per internem ES8388 Codec digitalisiert oder per Bluetooth direkt gestreamt; zero pogo pins!).*
   * **Bucht 2 (Cardo Packtalk Edge / Pro Inlay - Klasse 4 DMC Gen2):**
     * 6-Pin JST-SH Adapterkabel auf Header `J_AUDIO_PWR` stecken.
     * 3.5 mm Stereo-Klinkenstecker (Lautsprecherausgang ins OMB-Audioboard) und Cardo 2-Pin Micro-Stecker mit Rastnase (Mikrofoneingang vom ES8388 DAC) an die Cardo Air-Mount Kabelpeitsche anstecken.
     * Rechtwinkligen USB-C Ladestecker an den Ladeport des Packtalk Edge anstecken.
     * Cardo Packtalk Edge in das Air-Mount Bett einklicken (Dauerladung während aktivem Mesh-Betrieb voll unterstützt).
   * **Alternative Option: Midland PMR446 Funk-Kassette (Klasse 7 Analogfunk):**
     * 6-Pin JST-SH Adapterkabel auf Doppel-Klinke (2.5 mm Mic / 3.5 mm Spk) und 5V DC-Batteriedummy anstecken; PTT-Tastung erfolgt über den Open-Drain MOSFET `OPTO_PTT`.
   * **Alternative Option: OpenMotorMesh (OMM) 2.4 GHz OEM-Kassette (Klasse C UCS):**
     * 6-Pin JST-SH zu 6-Pin JST-SH Flachbandkabel anstecken.
     * Nativ gefertigt im standardisierten **UCS-Formfaktor** (Universal Communication Solution), reines Digital-Audio über UWB.
4. **Integrierte UWB-Antenne & Flanschdichtung:**
   * Auf `PCBA 03` arbeitet eine verlustarme SMD-Keramikantenne für 6.5 GHz UWB. Die Funkwellen durchdringen das dielektrische PA12-Gehäuse dämpfungsfrei; es sind keine externen Antennenradome erforderlich.
   * Silikon-Formdichtung auf den Kassettenkragen aufziehen und dünn mit Silikonfett benetzen.

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

> [!NOTE]
> **Radikal vereinfachter Prüfaufbau (Zero USB-C an Pods):**  
> Durch die v9.6 All-UWB Clean Architecture besitzen die Pods keine externen USB-C-Buchsen mehr. Für den Tischaufbau und das Begleitfahrzeug speist ein kompaktes **12V Werkstatt- & Car-Y-Adapterkabel** parallel den **Front-Knoten (`J1` JST-JWPF)** und die **Zentralbox (`J1` DTM-12)**. Dadurch bleibt der USB-C Port der Zentralbox vollkommen frei für CarPlay/Android Auto oder PWA-Diagnose! Die beiden Kassetten werden über die 2-Draht-DC-Federkontakte der Zentralbox mitversorgt. Alle Audio-, Steuer- und Telemetriedaten funken drahtlos über UWB.

Das Gesamtsystem lässt sich auf der Werkbank mit minimalem Verkabelungsaufwand zu 100 % testen, flashen und koppeln:

```text
+-------------------------------------------------------------------------------------------------+
|                 OPENMOTORBRIDGE TISCH-TESTAUFBAU & DRY-RUN (BENCH-LABOR SETUP)                  |
+-------------------------------------------------------------------------------------------------+
|                                                                                                 |
|   [ 12V DC Labornetzteil / 12V Kfz-Zigarettenanzünder / LiFePO4 Akku ]                          |
|        |                                                                                        |
|        | 12V DC Haupt-Zuleitung (FLRY 2x 0.75 mm² / AWG18)                                      |
|        |                                                                                        |
|        +--- 12V Y-ADAPTERKABEL ("Bench & Support-Car Harness") -----------------------+         |
|        |                                                                              |         |
|        | Abzweig A: 12V DC (JST-JWPF 2P)            Abzweig B: 12V DC (Deutsch DTM-12)|         |
|        v                                            v                                 |         |
|   +---------------+                            +---------------+                      |         |
|   |  FRONT-NODE   |  (Cockpit Hub PCBA 05)     |  ZENTRALBOX   |  (PCBA 01)           |         |
|   |  Port J1 12V  |  Dual SW3526 USB-PD        |  Port J1 DTM12|  LM5164 Buck, BQ USV |         |
|   |  Qwiic SAM-M10|  Knowles I2S MEMS          |  LoRa SX1262  |  Qualcomm QCC3084    |         |
|   +-------+-------+                            +-------+-------+                      |         |
|           |                                            |                              |         |
|           |                                            | 2-Draht 5V DC                |         |
|           |                                            v                              |         |
|           |                                   +-----------------+                     |         |
|           |                                   | SATELLITEN-PODS |                     |         |
|           |                                   | (Pod 1 & Pod 2) |                     |         |
|           |                                   | Pure DC Federn  |                     |         |
|           |                                   +--------+--------+                     |         |
|           |                                            |                              |         |
|           |                                            v                              |         |
|           |                                   +-----------------+                     |         |
|           |                                   | SMART KASSETTEN |                     |         |
|           |                                   | (Sena / Cardo / |                     |         |
|           |                                   |  OMM / Midland) |                     |         |
|           |                                   +--------+--------+                     |         |
|           |                                            |                              |         |
|           |          All-UWB Wireless Backbone         |                              |         |
|           |<==========================================>|                              |         |
|           |            (6.5 GHz, < 0.4 ms)             |                              |         |
|           |                                            v                              |         |
|           |                                   +-----------------+                     |         |
|           |                                   |   HECK-RADAR    |<--------------------+         |
|           |<=================================>|    (PCBA 08)    |  Opt. Abzweig C       |
|           |                                   | 36x Strobe-LEDs |  (12V DC JST-JWPF)    |
|           |                                   +-----------------+                       |
|           |                                            |                                |
|           v WebBLE / WebSerial                         v Bluetooth                      |
|     [ SMARTPHONE / LAPTOP MIT PWA ]             [ FAHRER-HELM ]                         |
|     (Dashboard & Flashing via USB-C / WebBLE)   (Dual-A2DP aptX HD)                     |
|                                                                                         |
+-------------------------------------------------------------------------------------------------+
```

### 4.0 Das universelle 12V Werkstatt- & Begleitfahrzeug-Y-Adapterkabel ("Bench & Support-Car Harness")

Um sowohl für den Prüfstandsbetrieb im Labor als auch für Begleitfahrzeuge (Support-Van, Mietwagen, Pkw-Rennleitung) eine absolut saubere, verwechslungsfreie und zerstörungsfreie Stromversorgung zu garantieren, wird das **12V-Y-Adapterkabel** verwendet. Es versorgt Front-Node und Zentralbox parallel aus einer 12V-Gleichspannungsquelle, wodurch der USB-C Port der Zentralbox für Apple CarPlay / Android Auto frei bleibt:

| Abschnitt / Ende | Steckverbinder & Typ | Pinbelegung | Kabelspezifikation | Funktion |
| :--- | :--- | :--- | :--- | :--- |
| **Eingang** | **Kfz-Zigarettenanzünderstecker** (mit 5A Glas-Sicherung) *oder* **4mm Labor-Bananenstecker** | Spitze / Rot: `+12V DC`<br>Flanken / Schwarz: `GND` | Stammkabel: $2 \times 0{,}75\,\text{mm}^2$ (AWG18) FLRY / Silikon, Länge $1{,}0\,\text{m}$ | Zentrale 12V DC Einspeisung aus Bordnetz oder Labornetzteil |
| **Abzweig A**<br>*(Front-Node)* | **JST JWPF 2-Pin Buchse**<br>Gehäuse: `02R-JWPF-VSLE-S`<br>Kontakte: `SWPR-001T-P025` | **Pin 1:** `+12V` (Rot, KL15)<br>**Pin 2:** `GND` (Schwarz) | $2 \times 0{,}5\,\text{mm}^2$ (AWG20), Länge $1{,}5\,\text{m}$ (flexibel bis zur Windschutzscheibe) | Speist den Cockpit-Hub PCBA 05 samt USB-PD Lader und GNSS |
| **Abzweig B**<br>*(Zentralbox)* | **Deutsch DTM-12 Buchsenstecker**<br>Gehäuse: `DTM-06-12S`<br>Keil: `WM-12S`, Pins: `0462-201-20141` | **Pin 1:** `KL30` (+12V)<br>**Pin 2:** `KL15` (+12V, gebrückt)<br>**Pin 3:** `GND` (Schwarz)<br>Pins 4–12: Blindstopfen `0413-204-2005` | $2 \times 0{,}75\,\text{mm}^2$ (AWG18), Länge $0{,}5\,\text{m}$ | Speist die Zentralbox direkt in den LM5164-Q1 72V Buck & BQ24075 USV |
| **Abzweig C**<br>*(Opt. Radar)* | **JST JWPF 2-Pin Buchse**<br>Gehäuse: `02R-JWPF-VSLE-S` | **Pin 1:** `+12V` (Rot)<br>**Pin 2:** `GND` (Schwarz) | $2 \times 0{,}35\,\text{mm}^2$ (AWG22), Länge $0{,}5\,\text{m}$ | Für Tisch-Prüfungen des Heckradars PCBA 08 auf der Werkbank |

> [!TIP]
> **Warum kein USB-C für die Stromversorgung der Zentralbox?**  
> 1. **CarPlay & Infotainment:** Im Begleitfahrzeug wird der USB-C Port der Zentralbox direkt mit der USB-Media-Buchse des Fahrzeugs verbunden, um kabelgebundenes Apple CarPlay / Android Auto auf das Auto-Display zu spiegeln. Wäre dieser Port durch ein Stromkabel vom Front-Node belegt, entfiele die Head-Unit-Integration!  
> 2. **Voller USV-Ladestrom:** Über den DTM-12-Eingang arbeitet der interne 72V-Buck-Converter (LM5164-Q1) im optimalen Wirkungsgradbereich und lädt die 2.200-mAh-USV zügig mit vollen $1{,}0\,\text{A}$, während beide Kassetten-Pods stabil mit 5V versorgt werden.

### 4.1 Der geführte 4-Punkte IKEA Smoke-Test
In der PWA (über WebSerial oder WebBLE) den Diagnosetest ausführen:
1. [x] **Bordnetz & USV (Check 1):** LM5164 Buck-Schiene aktiv (5.04 V), USV-LiPo (2.200 mAh) lädt mit 4.18 V.
2. [x] **Kassetten & Aktuatoren (Check 2):** UWB Handshake (`UWB_PKT_CARTRIDGE_ANNOUNCE`), Modell-Erkennung (Sena / Cardo / OMM / Midland) und mechatronischer Klicktest der 4 Aktuatoren ("Klack-Klack-Klack-Klack").
3. [x] **Front-Knoten & UWB Backbone (Check 3):** UWB-Link aktiv ($< 0{,}4\,\text{ms}$ Latenz), SAM-M10Q 3D-Fix, TMP117 Temperatur, Knowles MEMS Pegel & PTT-Tastendruck.
4. [x] **LoRa 868 MHz & Radar 2.0 (Check 4):** SX1262 LoRa Ping-Echo und drahtloser UWB-Telemetrie-Link zum Heckradar 2.0 (`PCBA 08`) inklusive 36-LED Flügel-Makrotest.
Erst wenn alle 4 Checks grün leuchten, die Gehäusedeckel mit den M3-Schrauben über Kreuz festziehen.

---

## 5. Fahrzeugspezifische Montage & Verkabelung am Motorrad

### 5.1 Montage Harley-Davidson Plattform (Touring, CVO ST, Road King)
* **Zentralbox:** Unter der Fahrersitzbank auf der Rahmenbrücke vor der Batterie auf 4x M4 Silentblöcken verschrauben.
* **Pod 1 & Pod 2:** Auf den Hartschalenkoffern mittels Kofferdeckel-Docks ([`saddlebag_lid_dock.stl`](../../hardware/cad/stl/02_pod_base/saddlebag_lid_dock.stl)) montieren.
* **Koffer-Trennstelle (2-Pin Magnet-Pogo "MagSafe-Ersatz"):**
  * **Rahmenseitiges Dock:** Das 3D-Druck Rahmendock ([`009_magsafe_frame_dock.stl`](../../hardware/cad/stl/02_pod_base/parts/009_magsafe_frame_dock.stl)) mit Klemmschelle ([`009_magsafe_frame_clamp.stl`](../../hardware/cad/stl/02_pod_base/parts/009_magsafe_frame_clamp.stl)) am Ø 26 mm Rahmenrohr unter dem Sitzüberhang mit 4x M3 $\times 16\,\text{mm}$ Schrauben verschrauben (DIN 934 Nut-Pockets). Die 2-Pin Magnet-Pogo Buchse (HytePro M411) formschlüssig einlegen und an Peitsche 1 bzw. 2 des DTM-12 Kabelbaums anschließen.
  * **Koffer-Vorderwand & Dichtung:** Ein einzelnes $\varnothing 12\,\text{mm}$ Loch seitlich-innen an der Koffer-Vorderwand oberhalb des Schwingenlagers bohren (im Wind- und Spritzwasserschatten; der **Kofferboden bleibt zu 100 % lochfrei**). Die geteilte EPDM/TPU-Dichtung ([`010_saddlebag_hole_grommet_split.stl`](../../hardware/cad/stl/02_pod_base/parts/010_saddlebag_hole_grommet_split.stl)) einsetzen, das 2-adrige Flachbandkabel der Magnetstecker-Kupplung hindurchführen und am integrierten Klemmturm per Mini-Kabelbinder zugentlasten. Im Kofferinneren das Kabel parallel zum Deckel-Fangband lastfrei zum Kofferdeckel-Dock führen.
* **Heck-Radar (Schwerlast-Neigegelenk & Spritzwasserschutz):**
  * **Vormontage auf der Werkbank (100 % lötkolbenfrei):** Das versiegelte Radar 2.0 Gehäuse ([`radar_mr20_housing.stl`](../../hardware/cad/stl/05_accessories/radar_mr20_housing.stl)) mit seinen zwei innenliegenden DIN 934 M4-Muttern wird über zwei DIN 912 M4 $\times$ 12 mm Schrauben fest an die Adapterplatte ([`radar_swivel_tilt_cradle.stl`](../../hardware/cad/stl/02_pod_base/radar_swivel_tilt_cradle.stl)) geschraubt. Die Passungs-Bosse nehmen 100 % der Scherkräfte auf.
  * **Montage am Motorrad:** Den Kennzeichenträger ([`radar_license_plate_bracket.stl`](../../hardware/cad/stl/02_pod_base/radar_license_plate_bracket.stl)) unter die unteren M6-Kennzeichenschrauben klemmen. Die Hirth-Zunge der Adapterplatte in die Gabelaufnahme einschieben, Nickwinkel waagerecht zur Fahrbahn justieren und mit einer DIN 912 M5 $\times$ 25 mm Klemmschraube in die versenkte M5-Mutter formschlüssig festziehen.
  * **Spritzwasser-Verkabelung (Abtropfbogen):** Das 2-adrige FLRY-B Kabel von Peitsche 5 im rückseitigen Kanal der Trägerwirbelsäule führen und in einer nach unten hängenden Abtropfschlaufe (Drip-Loop) von unten durch die M8 IP68-Kabelverschraubung führen. Der monolithische Roost-Deflector am Gehäuseboden schirmt die Verschraubung vollständig gegen aufgewirbelte Reifengischt ab.
* **Front-Knoten:** In der Verkleidung (Batwing / Sharknose) oder Nacelle verschraubt; 12V von Standlicht/Zubehör; CAN-Bus lokal an J2 (oder an Zentralbox unter der Sitzbank).

### 5.2 Montage Adventure-Plattform (BMW GS / GSA Familie)
* **Zentralbox:** Im Rahmendreieck unter der Fahrersitzbank auf 4x M4 Silentblöcken montieren.
* **Cockpit & Front-Knoten:** An der Ø 12 mm GPS-Querstrebe über dem TFT befestigt; 12V über originalen BMW Cartool-Stecker.
* **Pod 1 & Pod 2:**
  * *Option A (Vario-Koffer / GS Standard):* Transition-Docks ([`adventure_transition_dock_base.stl`](../../hardware/cad/stl/02_pod_base/adventure_transition_dock_base.stl)) in der Sitzbank-Bügelfalte (Ø 28 mm Rahmenrohr) verbunden mit der Sattelbrücke ([`adventure_underseat_cross_rail.stl`](../../hardware/cad/stl/02_pod_base/adventure_underseat_cross_rail.stl)).
  * *Option B (Edelstahl-Rohrkofferträger / GSA):* Heavy-Duty GSA Cage Docks ([`adventure_gsa_cage_dock_body.stl`](../../hardware/cad/stl/02_pod_base/adventure_gsa_cage_dock_body.stl)) im 45 mm Totraum des Trägers.
  * *Koffer-Abreißtrennung:* Bei abnehmbaren Alukoffern wird die 2-Pin Magnet-Pogo Kupplung als elastischer Inline-Breakaway-Kabelstrang an der Soziusfußrasten-Aufnahme gehaltert.
* **Heck-Radar:** Minimaler Halter ([`adventure_rack_radar_mount.stl`](../../hardware/cad/stl/02_pod_base/adventure_rack_radar_mount.stl)) direkt unter der GS-Gepäckbrücke für Garmin Varia oder Wheeltec MR20 auf Peitsche 5.

### 5.3 Begleitfahrzeug- & Autokolonnen-Installation (Support-Car / Van)
* **Pod 1 & Pod 2:** Werden mit je einem Schnellwechsel-Clip ([`car_sun_visor_pod_clip.stl`](../../hardware/cad/stl/05_accessories/car_sun_visor_pod_clip.stl)) an Fahrer- und Beifahrer-Sonnenblende geklemmt.
  * Modus A (Begleitfahrzeug für Bike-Gruppe): Pod 1 = Sena SPIDER X Slim, Pod 2 = Cardo Packtalk Edge.
  * 2-poliges 5V DC-Stromkabel verdeckt in der Dachhimmel- und A-Säulen-Gummidichtung zur Mittelkonsole verlegen.
* **Zentralbox & Front-Knoten (Doppelgehäuse / Stack-Dock):**
  * Für den sauberen Einsatz im Pkw/Van werden Front-Knoten (unten) und Zentralbox (oben) in einem formschlüssigen **Doppelgehäuse (`car_dashboard_wedge_dock.scad`)** gestackt auf der Mittelkonsole oder dem Armaturenbrett platziert.
  * **Energie- & Stromversorgungskonzept (über das 12V Y-Adapterkabel, siehe Kap. 4.0):**
    * **Option A (Zigarettenanzünder / 12V Bordsteckdose):** 12V Speisung über das vorkonfektionierte 12V-Y-Adapterkabel ("Bench & Support-Car Harness"):
      * **Abzweig A (JST-JWPF 2-Pin):** Speist Port `J1` des Front-Knotens. Dessen interne Buck-Wandler versorgen die Sonnenblenden-Pods mit 5V VBUS sowie Smartphones via Dual 20W USB-PD / Qi.
      * **Abzweig B (Deutsch DTM-12):** Speist Port `J1` der Zentralbox (Pins 1+2 KL30/KL15, Pin 3 GND). Der interne LM5164-Q1 versorgt Zentralbox und USV mit vollem Ladestrom.
    * **Option B (Fahrerfußraum Zündungsplus):** Feste 2-Draht-Verkabelung an Klemme 15 (KL15 Zündungsplus + Karosserie-GND) im Sicherungskasten/Fußraum auf den Eingang des Y-Adapterkabels (strikt kein Dauerplus KL30 ohne Ruhestrom-Abschaltung).
* **SAM-M10Q GNSS:** Auf dem Armaturenbrett hinter der Windschutzscheibe (über Qwiic-Kabel an Front-Node Port `J12`).
* **Audio- & Infotainment-Integration:** Direkte USB-C Datenverbindung von der Zentralbox zur USB-Media-Buchse des Fahrzeugs. Startet kabelgebundenes Apple CarPlay / Android Auto, spiegelt die PWA-Navigation auf das Fahrzeug-Display und gibt Funkdurchsagen über das Pkw-Soundsystem aus.
* **Telemetrie:** Drahtloser BLE-OBD2 Dongle im Fahrerfußraum (oder direkter 16-Pin OBD-Port).

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
