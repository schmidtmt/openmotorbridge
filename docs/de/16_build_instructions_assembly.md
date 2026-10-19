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
          v Peitsche 1 (2-Draht DC 12V)    v Peitsche 2 (2-Draht DC 12V)    v Peitsche 3 (2-Draht DC 12V)
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
> Alle 3D-Druckteile (`.scad` / `.stl`) wurden mit definierten Toleranzen ($+0{,}15\,\text{mm}$ für HP MJF PA12 bzw. ASA/PET-CF) konstruiert. Auf das fehleranfällige Einschmelzen von Gewindebuchsen (Ruthex) wurde im gesamten System konsequent verzichtet: Alle Verschraubungen nutzen ausnahmslos formschlüssige **DIN 934 Sechskant-Mutterntaschen** (einfach von Hand einlegen). Selbstschneidende Gewinde in Kunststoff sind im gesamten System verboten, sodass jedes Gehäuse beliebig oft geöffnet und gewartet werden kann, ohne dass Gewindegänge ausleiern oder Gehäuse nach einmaliger Demontage unbrauchbar werden.

Alle Einzelteile, Platinen-Bestelldaten und COTS-Zukauflisten sind detailliert in **[Kapitel 15: Stücklisten & SMT-Fertigungsdaten](15_bom_manufacturing.md)** aufgeführt. Vor Montagebeginn sicherstellen, dass folgende Baugruppen bereitliegen:

* [ ] **3D-Druckteile (MJF PA12 schwarz oder FDM ASA/PET-CF):**
  * 1x Main Box (Unterwanne mit UWB-Bodentasche $11 \times 11 \times 0{,}6\,\text{mm}$, Zwischenboden mit LiPo-Wanne, Deckel mit LoRa FXP895 Tasche $110 \times 20 \times 0{,}8\,\text{mm}$)
  * 2x Pod-Basisgehäuse (nahtlose 1-Teil-Monocoques mit integrierter monolithischer Schottwand, Schachtaufnahme für IP67-Direktstecker & Federdomen; 0 Schrauben, 0 lose Teile)
  * 2x Kassetten-Basisschlitten (mit UWB-Antennentasche & M2 Mutterntaschen), Inlays (Sena SPIDER X Slim, Cardo Packtalk Edge, Swap OMM oder Blindkassette) & 2x Rastwippen
  * 1x Front-Knoten (Unterwanne mit UWB-Bodentasche und AMPS-Nut-Pockets, Deckel, TPU-Dichtkämme & USB-C Kappe)
  * 1x Fahrzeugspezifisches Montage-Kit (BMW GS Klemmen & `adventure_rack_radar_mount.stl` / Harley Kofferdeckel-Docks & Kennzeichen-Radarhalter / Support-Car `car_sun_visor_pod_clip.stl`)
  * *(Optional für Helmeinsatz / OMM):* 1-2x OMM UCS Gehäuse-Oberschalen ([`omm_ucs_top_shell.stl`](../../hardware/cad/stl/03_pod_cartridges/omm_ucs_top_shell.stl)), Unterschalen ([`omm_ucs_bottom_shell.stl`](../../hardware/cad/stl/03_pod_cartridges/omm_ucs_bottom_shell.stl)) & Silikon-Tastmatten ([`omm_ucs_silicone_keypad.stl`](../../hardware/cad/stl/03_pod_cartridges/omm_ucs_silicone_keypad.stl))
* [ ] **Vollautomatisch bestückte Platinen (von JLCPCB / Eurocircuits - das 7-PCBA Lineup):**
  * 1x PCBA 01 (Zentralbox mit LoRa SX1262, DW3110 UWB, SW1 Taster und DTM-12 Header)
  * 2x PCBA 03 (Universal Smart Cartridge Rev 3.0 All-UWB mit DW3110 UWB, MCU, 4x AO3400A MOSFETs und SMT-Schlitzbuchse `J_DC_IN`, 2-seitig SMT)
  * 1x PCBA 05 (Front-Knoten mit DW3110 UWB)
  * *(Optional: 1x PCBA 08 Radar 2.0 Sub-MCU mit DW3110 UWB, 1x PCBA 07 Smart-Keyfob)*
  * *(Optional für Helm / OpenMotorMesh):* 1x **PCBA 09 (OMM 2.4 GHz HD-Mesh)** und/oder 1x **PCBA 10 (OMM 446 PMR/DMR Funk)**
  * *(Hinweis: PCBA 02, PCBA 04 und PCBA 06 sind ersatzlos entfallen).*
* [ ] **V4A Edelstahl-Normteile & Federn (IKEA-Prinzip - 100 % lötfrei):**
  * 8x DIN 934 / DIN 985 M3 Edelstahlmuttern (für Gehäuse-Nut-Pockets)
  * 6x DIN 934 M4 Muttern (4x AMPS-Nut-Pockets in Front-Node Wanne, 2x Radar 2.0 Heck-Mutterntaschen)
  * 4x M3 x 40 mm Schrauben (Zentralbox), 4x M3 x 20 mm Schrauben (Front-Node)
  * 8x M2.5 x 6 mm Platinenschrauben (Zentralbox & Front-Node), 8x M2 x 6 mm Platinenschrauben (Kassetten PCBA 03; Schottwandschrauben entfallen komplett)
  * 4-8x DIN 934 M2 Muttern & 4-8x DIN 912 M2 x 8 mm Schrauben (für OMM UCS Modul-Verschraubung)
  * 2x DIN 7 M2 x 8 mm Zylinderstifte (Wippenachsen), 2x DIN 6325 Ø 6 x 8 mm gehärtete Stahlanker
  * 2x Wippen-Rückstellfedern, 4x Auto-Eject Druckfedern, 1x N52 Neodym-Entriegelungsschlüssel
  * 2x Vorkonfektionierte IP67 Gleichstrom-Direktstecker (2-Pin Automotive Blade mit axialem O-Ring und U-Sicherungsclip) für Pod 1 & 2 Stromzuführung
* [ ] **Dichtungen, Pufferakku & Antennen:**
  * Silikon-Rundschnur Ø 1,5 mm Shore 40A ($40\,\text{cm}$ Main Box, $30\,\text{cm}$ Front-Knoten)
  * Silikon-Rundschnur Ø 0,8 mm Shore 40A ($25\,\text{cm}$ pro OMM UCS Modul)
  * 2x Silikon-Flanschdichtungen für Pod 1 & 2 Mundlöcher, Gore ePTFE Membranpads
  * **1x 1S LiPo Flat-Pack 2.200 mAh** ($68 \times 39 \times 5{,}0\,\text{mm}$) mit Molex Micro-Fit 3.0 Stecker (Zentralbox USV)
  * 2x O-Ringe NBR70 ($\varnothing 12 \times 1{,}5\,\text{mm}$) für die IP67-Direktstecker an Pod 1 & 2
  * **1-2x 1S LiPo Pouch-Akkus 600 mAh** ($38 \times 24 \times 4{,}5\,\text{mm}$) mit JST 2-Pin Stecker (OMM UCS Module)
  * **Taoglas FXUWB10 UWB Flex-Antennen** mit 20 mm U.FL Kabel (Zentralbox, Front-Node, Kassetten)
  * **1x Taoglas FXP895 LoRa 868 MHz Flex-Antenne** mit 50 $\Omega$ U.FL Kabel
  * **1x u-blox SAM-M10Q Multi-GNSS Modul** mit integrierter Patchantenne (Qwiic I2C)
  * **1x TI TMP117 & 1x TI OPT3001 Sensoren** (Qwiic I2C)
  * **1-2x HF-Koaxialpigtails U.FL auf SMA-Bulkhead** (RG-178 / 1.13mm, 50 mm) mit IP67 EPDM O-Ring und M6 V4A Mutter
  * **1x OMM 2.4 GHz Stummelantenne** (SMA-Male, $38\,\text{mm}$ Rubber-Duck Helix)
  * **1x OMM 446 MHz Stummelantenne** (SMA-Male, $48\,\text{mm}$ Helical Stubby)
* [ ] **Vorkonfektionierte COTS-Kabel (kein Crimpen nötig):**
  * 1x Deutsch DTM-12 IP67/IP69K Zentral-Kabelbaum (reine 2-Draht DC-Peitschen 1 bis 3 für Pod 1, Pod 2, Heck-Radar sowie Peitsche 4 für 12V Bordnetz & CAN)
  * 2-Pin JWPF / Superseal Steckverbinder für Pod- und Radar-Zuleitungen
  * JST-SH Kassetten-Kabelbäume (8-Pin `J_ACT` für Hubmagnete)
  * 1-2x OMM Helm-Audio & PTT-Kabelbäume (6-Pin JST-SH 1.0mm Buchse auf 3.5mm Klinke + Mic + PTT, AWG30/32 Silikon, $12\dots 15\,\text{cm}$)
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

### Schritt 2: Satelliten-Pods 1 & 2 montieren (2x identisch, 100 % schraubenloses Monocoque)
1. **2-Draht-DC-Zuleitung vom Zentralbaum bereitstellen:**
   * Die Stromversorgung der Pods stammt direkt aus der Zentralbox (`PCBA 01`). Vom Deutsch DTM-12 Zentralstecker führen zwei vorkonfektionierte 2-Draht-Gleichstrompeitschen (Peitsche 1 für Pod 1 links, Peitsche 2 für Pod 2 rechts) entlang des Rahmens.
   * Adernbelegung:
     * **Ader 1 (Rot):** Geschaltete Speisung $+5\,\text{V}$ (bzw. VCC, auf `PCBA 01` abgesichert über PolySwitch PPTC 500mA), Querschnitt $0{,}34\,\text{mm}^2$ (AWG22 Silikon).
     * **Ader 2 (Schwarz):** Gemeinsame System-Masse `GND`, Querschnitt $0{,}34\,\text{mm}^2$ (AWG22 Silikon).
2. **IP67 Gleichstrom-Direktstecker werkzeug- & lötfrei montieren (IKEA-Prinzip):**
   * Die beiden Adern enden am vorkonfektionierten, wasserdichten **2-Pin Automotive Blade-Direktstecker (`CON_POD_DC`)**.
   * Den axialen NBR70 O-Ring ($\varnothing 12 \times 1{,}5\,\text{mm}$) auf den Steckerbund aufziehen.
   * Den Stecker von außen durch die formschlüssige Aufnahme der Gehäuserückwand einschieben. Die beiden massiven, vergoldeten Kontaktklingen ($2{,}8 \times 0{,}8\,\text{mm}$, $10{,}0\,\text{mm}$ Raster) ragen nun $6{,}0\,\text{mm}$ weit in horizontaler $+X$-Richtung durch die Schottwand in den Kassetten-Aufnahmeschacht.
   * Den Edelstahl-U-Sicherungsclip seitlich in die Verriegelungsnut des Gehäuses einschieben, bis er mit einem satten Klick einrastet. Der Stecker ist damit **100 % formschlüssig verriegelt, vibrationsfest gesichert und dichtet die Gehäuserückwand hermetisch nach IP67 ab** – komplett ohne Lötkolben und ohne Werkzeug!
3. **Auto-Eject Schnappfedern aufstecken:**
   * Von vorne in den Kassetten-Schacht die beiden V4A-Edelstahl-Druckfedern ($\varnothing 4{,}5 \times 15\,\text{mm}$, Federrate $1{,}2\,\text{N/mm}$) direkt auf die beiden monolithischen Führungsdome der Schottwand (bei $Y = 16{,}0\,\text{mm}$ und $Y = 54{,}0\,\text{mm}$) aufschieben.
4. **Schraubenlose Fertigstellung des Pods:**
   * Da das Pod-Gehäuse ein nahtloses 1-Teil-Monocoque ist (`PCBA 02` ist ersatzlos entfallen), sind im Pod keinerlei interne Platinen, Schrauben oder lose Kabelverbindungen erforderlich (0 Schrauben). Die beiden federnd kontaktierenden Messerklingen und die beiden Auswerferfedern warten im Schacht auf das Einschieben der Kassette. Wiederholen für Pod 2.
   * *(Hinweis zum Leerbetrieb):* Wird ein Pod temporär ohne Aktiv-Kassette gefahren, schützt die standardmäßige Blindkassette (`03_insert_blindkassette.scad`) oder eine elastische TPU-Gummikappe die Schachtöffnung. Die eFuse auf `PCBA 01` schaltet den Port im Leerbetrieb automatisch zu 100 % stromlos ($0{,}0\,\text{V}$).

---

### Schritt 3: Multi-Protokoll Gateway-Kassetten 1 & 2 montieren
1. **Stromversorgungs- & UWB-Antennen-Konzept verstehen (100 % kabel- und steckerfrei zum Pod):**
   * **Stromzuführung via Dual-Beam Schlitzbuchse (Kein Kabel zum Gehäuse!):** Die Kassetten benötigen keine lose Kabelpeitsche und kein Gehäusekabel. Die Stromversorgung erfolgt beim Einschieben rein elektromechanisch über eine werkseitig auf `PCBA 03` bestückte Hochstrom-Schlitzbuchse:
     * Am hinteren Platinenrand von `PCBA 03` ist eine liegende, vergoldete **2-Pin Dual-Beam Schlitzbuchse (`J_DC_IN`)** per SMT aufgelötet (Pin 1: $+5\,\text{V}$, Pin 2: `GND`, $10{,}0\,\text{mm}$ Raster, bis 5 A Dauerstrom).
     * Die gefederten Buchsenkontakte liegen geschützt tief im isolierenden Hochtemperatur-Kunststoffkörper der Buchse. Dadurch ist die mobile Kassette beim Transport in Jackentasche oder Rucksack absolut **berührungssicher (IP2X) und kurzschlussfest gegen Schlüssel oder Münzen**.
     * Im Boden des Kassetten-Grundschlittens ([`cartridge_base_sled.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl)) ist an der hinteren Stirnseite das offene Kontaktfenster ($15{,}0 \times 6{,}0\,\text{mm}$) ausgespart.
     * Beim vollständigen Einschieben der Kassette tauchen die beiden massiven Klingen des Pod-Direktsteckers formschlüssig in die Schlitzbuchse `J_DC_IN` ein. Die gegenüberliegenden Federarme spannen die Klingen mit hoher Normalkraft beidseitig ein (**selbstreinigender Wischkontakt**). 
     * **Absolut rüttelfest:** Im Gegensatz zu stirnseitigen Pogo-Pins gleitet die Zunge bei Fahrbahnstößen und axialen Vibrationen prellfrei im Schlitz. **Zero Kontaktprellen (Micro-Bouncing), keine Reibkorrosion.**
   * **UWB-Antennenanbindung (Hirose U.FL-Buchse & Taoglas FXUWB10 Flexantenne):**
     * Auf `PCBA 03` arbeitet **keine** Keramik-Chipantenne, sondern eine **Hirose U.FL-Koaxialbuchse** (`ANT_UWB`, Hirose U.FL-R-SMT-1) auf der Platinenunterseite (`B.Cu`) unmittelbar am Qorvo DW3110 Transceiver.
     * Als dedizierte UWB-Antenne kommt die flexible Breitband-Flachantenne **Taoglas FXUWB10** ($12{,}0 \times 12{,}0 \times 0{,}8\,\text{mm}$, 6.5 GHz Channel 5) zum Einsatz.
     * Die Antenne wird passgenau in die vertiefte Tasche ($12{,}0 \times 12{,}0 \times 0{,}9\,\text{mm}$) im Boden des Kassetten-Schlittens eingelegt und mit dem rückseitigen 3M-Klebepad fixiert.
     * Das ultrakurze $20\dots 30\,\text{mm}$ U.FL-Mikrokoaxialkabel wird im integrierten Führungskanal des Schlittenbodens verlegt und senkrecht auf die U.FL-Buchse `ANT_UWB` auf der Unterseite der `PCBA 03` aufgeklickt.
2. **Platinenmontage PCBA 03 im Schlitten:**
   * Kassettenplatine `PCBA 03 Rev 3.0` mit der Oberseite (`F.Cu`: ESP32-C6, MOSFETs, Header `J_ACT`, `J_AUDIO_PWR`, Buchse `J_DC_IN`) nach oben auf die vier M2-Schraubdome im hinteren Bereich des Schlittens setzen.
   * Zuvor das U.FL-Kabel der UWB-Bodenantenne auf `ANT_UWB` aufklicken.
   * Platine mit 4x M2 $\times 6\,\text{mm}$ Schrauben handfest fixieren.
   * *Sichtprüfung:* Von der Rückseite des Schlittens durch das Kontaktfenster blicken. Die beiden Trichtereinführungen der Schlitzbuchse `J_DC_IN` müssen frei und zentriert zugänglich sein.
3. **Mechatronik-Aktuatoren & Niederhalteplatte montieren:**
   * 4x Miniatur-Hubmagnete ($\varnothing 6{,}5 \times 12\,\text{mm}$) mit dämpfenden TPU-Tastspitzen (`actuator_silicone_tip.stl`) in die vier Passbohrungen der Führungsbrücke des Inlays ([`cartridge_insert_sena.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) bzw. [`cartridge_insert_cardo.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl)) einstecken.
   * **Aktuator-Verkabelung an `J_ACT` (8-Pin JST-SH 1.0 mm):**
     * Das vorkonfektionierte 8-Pin Kabel auf den Header `J_ACT` aufstecken.
     * Die vier verdrillten Adernpaare (AWG30 Silikon) an die vier Hubmagnete führen (Paar 1 = Taste +, Paar 2 = Taste -, Paar 3 = Center/Phone, Paar 4 = Mesh/Pairing).
   * **Niederhalteplatte verschrauben:** Die PA12-Niederhalteplatte ([`cartridge_retainer_plate.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_retainer_plate.stl)) plan über die Hubmagnete legen und mit **4x M2 $\times 6\,\text{mm}$ Senkkopfschrauben (DIN 7991)** fest anziehen. Die Aktuatoren sitzen nun absolut spielfrei und rüttelfest im Schlitten.
4. **Gateway-Inlay & OEM-Adapterkabel anschließen (`J_AUDIO_PWR` / 8-Pin JST-SH):**
   * **Bucht 1 (Sena SPIDER X Slim Inlay - OMB Referenz K2a):**
     * Vorkonfektioniertes 8-Pin JST-SH Adapterkabel auf Header `J_AUDIO_PWR` stecken (Pin 1: `PGND`, Pin 2: `VCC_5V_PROT`, Pin 3: `AGND_AUDIO_IN`, Pin 4/5: Stereo Spk In, Pin 6: `OMM_DETECT` gebrückt auf GND, Pin 7: Mic Out `VOICE_OUT`).
     * 2-Pin Micro-JST Stecker an die externe Akkuzuleitung des SPIDER X Slim anstecken (liefert permanente 3.85V Direct-DC Speisung via MP2315 Step-Down ohne Akku im Pod!).
     * 2.5 mm Klinkenstecker an den Mikrofoneingang und 3.5 mm Klinkenstecker an den Lautsprecherausgang der Sena-Kabelpeitsche anstecken.
     * SPIDER X Slim formschlüssig in das PA12-Nest einlegen. *(Zero Pogo-Pins, Laststrom fließt isoliert über `PGND`, Audio über stromlose `AGND_AUDIO_IN`-Masse Pin 3 zu 100 % brummfrei).*
   * **Alternative Option: Universelle OEM-Upcycling-Kassette (Schuberth SC2, Shoei SRL-Mesh/SRL3, HJC Smart 50B - 0 € Budget-Option):**
     * *Vorbereitung (Battery Eliminator):* Gehäuse des ausgemusterten OEM-Intercoms (SC2, Shoei SRL oder Smart HJC) öffnen, LiPo-Pouch-Akku ablöten. Miniatur Step-Down-Wandler (z. B. MP2315) von `VCC` (5V von `J_AUDIO_PWR` Pin 2) auf $3{,}75\dots 3{,}85\,\text{V}$ einstellen und an `BAT+` / `BAT-` anlöten. Einen $10\,\text{k}\Omega$-Widerstand zwischen NTC-Pad und Masse (`GND`) anlöten (simuliert 22 °C Akkutemperatur gegen Sensor-Fehler). Litzen zugentlastet mit Silikon/B-7000 vergießen.
     * *Audio- & Antennen-Adaption:* 8-Pin JST-SH Kabelpeitsche mit den OEM-Lautsprecher- und Mikrofonleitungen verbinden (`AGND`-Massen getrennt!). Internes U.FL/Micro-Koaxialkabel auf ein kurzes RG-178 Pigtail zur SMA-Flanschbuchse der Kassettenstirnseite adaptieren.
     * *Montage im Schlitten:* Hauptmodul ($75 \times 40 \times 12\,\text{mm}$ oder flaches Nackenmodul) und Step-Down-Regler im Basisschlitten platzieren. Steuerung drahtlos über BLE-Lenkerfernbedienung (SC2 Remote oder Sena RC4) oder mechatronisch. Mit Blindkassettendeckel (`03_insert_blindkassette.scad`) und 4x M2-Schrauben wetterfest verschließen.
   * **Bucht 2 (Cardo Packtalk Edge / Pro Inlay - Klasse 1d DMC Gen2):**
     * 8-Pin JST-SH Adapterkabel auf Header `J_AUDIO_PWR` stecken (Pin 6 `OMM_DETECT` intern mit GND gebrückt $\rightarrow$ `U4` NC analog, Pin 7 `VOICE_OUT` an Mic In, Pin 4/5 Stereo Spk an Line-In ADC, Pin 1/2 an USB-C 5V Ladeport).
     * 3.5 mm Stereo-Klinkenstecker (Lautsprecherausgang ins OMB-Audioboard) und Cardo 2-Pin Micro-Stecker mit Rastnase (Mikrofoneingang vom ES8388 DAC) an die Cardo Air-Mount Kabelpeitsche bzw. das Direkt-Kontaktfeld anstecken.
     * Rechtwinkligen USB-C Ladestecker an den Ladeport des Packtalk Edge anstecken.
     * Cardo Packtalk Edge in das Air-Mount Bett einklicken (Dauerladung während aktivem Mesh-Betrieb voll unterstützt; Laderückstrom fließt getrennt über `PGND` ab).
   * **Alternative Option: Midland PMR446 Funk-Kassette (Klasse 3a Analogfunk):**
     * **Variante A (Internes Kompakt-Inlay):** Kompakte Handfunkgeräte (z. B. Midland XT30 oder Bare-Boards) werden direkt in das Kassetten-Nest eingelegt. 8-Pin JST-SH Adapterkabel auf Doppel-Klinke (2.5 mm Mic / 3.5 mm Spk) und 5V DC-Batteriedummy anstecken; PTT-Tastung erfolgt über Pin 8 (`PTT_IO` via MOSFET `Q4`). Das Kassetten-Gehäuse bleibt 100 % geschlossen (IP67).
     * **Variante B (Externe Groß-Handfunke / Tethered Breakout):** Für voluminöse Handfunkgeräte (Midland G7/G9 Pro, Kenwood, Baofeng, Betriebsfunk), die nicht in den Pod passen, wird der Basisschlitten mit offener Frontbohrung (`has_sma_port = true`) verwendet. In die $\varnothing 6{,}5\,\text{mm}$ Bohrung wird eine M8- bzw. PG7-Kabelverschraubung oder EPDM-Dichtetülle eingesetzt. Das mehradrige Spiralkabel führt von `J_AUDIO_PWR` (Mic, Spk, PTT, 5V Speisung) wasserdicht nach außen zur externen Funke im Tankrucksack, Koffer oder Lenker-Holster.
   * **Alternative Option: OpenMotorMesh (OMM) 2.4 GHz / 446 Funk-Kassette (Klasse 4 / 3b UCS):**
     * 8-Pin JST-SH zu 90° USB-C Adapterkabel (4-polig: VBUS, GND, D+, D-) anstecken. Pin 6 (`OMM_DETECT`) bleibt unbeschaltet (N/C), wodurch `R9` den Hardware-Umschalter `U4` auf `PCBA 03` automatisch auf digitalen USB-Audio-Betrieb schaltet!
     * Nativ gefertigt im standardisierten **UCS-Formfaktor** (Universal Communication Solution), reines verlustfreies Digital-Audio über USB ohne zusätzliche D/A-Wandler.
5. **Flanschdichtung aufziehen & Kassettenabschluss:**
   * Shore 40A Silikon-Formdichtung auf den Kassettenkragen aufziehen und dünn mit dielektrischem Silikonfett benetzen.
   * Die Dichtung dichtet beim vollständigen Verrasten im Pod das Einschubmaul umlaufend gegen Spritzwasser (IP67) ab. Die UWB-Funkwellen durchdringen das dielektrische PA12-Gehäuse völlig dämpfungsfrei; es sind keine externen Radome oder Öffnungen nötig.

---

### Schritt 3.1: Montage des magnetischen Diebstahlschutzes (Wippen-Mechanismus)
1. **Stahlanker einpressen:** Gehärteten Stahlstift ($\varnothing 6 \times 8\,\text{mm}$, DIN 6325) in die Querbohrung der Wippe ([`cartridge_magnetic_lock_latch.stl`](../../hardware/cad/stl/03_pod_cartridges/cartridge_magnetic_lock_latch.stl)) bündig einpressen.
2. **Rückstellfeder einsetzen:** Die kleine $\varnothing 3{,}5 \times 10\,\text{mm}$ Druckfeder in die innenseitige Federtasche stecken.
3. **Wippe im Schlitten montieren:** Vormontierte Wippe in die linke Führungswange des Kassetten-Schlittens einsetzen und mit dem $\varnothing 2{,}0 \times 8\,\text{mm}$ Edelstahl-Zylinderstift (DIN 7) lagern.
4. **Funktionsprüfung:** Sägezahn ragt $2{,}5\,\text{mm}$ heraus; bei Annäherung des N52 Neodym-Magneten schwenkt die Wippe bündig ein.

---

### Schritt 3.2: OMM UCS Intercom-Module (PCBA 09 & PCBA 10) zusammenbauen & für Helmmontage vorbereiten

Die beiden autarken Module (**PCBA 09: OMM 2.4 GHz HD-Mesh** und **PCBA 10: OMM 446 PMR/DMR**) teilen sich ein 100 % identisches ECE 22.06 UCS-Gehäuse ($68 \times 36 \times 9{,}5\,\text{mm}$) und werden nach folgendem Ablauf montiert:

1. **Muttern & Dichtungen in OMM-Gehäuse einlegen:**
   * 4x DIN 934 M2 Edelstahlmuttern von innen in die formschlüssigen Mutterntaschen der Oberschale ([`omm_ucs_top_shell.stl`](../../hardware/cad/stl/03_pod_cartridges/omm_ucs_top_shell.stl)) eindrücken.
   * Shore 50A Silikon-Tastmatte ([`omm_ucs_silicone_keypad.stl`](../../hardware/cad/stl/03_pod_cartridges/omm_ucs_silicone_keypad.stl)) formschlüssig in die Oberschale einpassen (Tastenknöpfe ragen durch die 4 Bohrungen, diffuser LED-Dom sitzt über der Aussparung für `D1`).
   * Silikon-Rundschnur ($\varnothing 0{,}8\,\text{mm}$, ca. $22\,\text{cm}$) dünn mit Silikonfett benetzen und in die umlaufende Dichtnut der Oberschale einlegen.
2. **HF-Koaxialpigtail & wasserdichte SMA-Durchführung montieren:**
   * Das $50\,\text{mm}$ kurze HF-Koaxialkabel (U.FL auf SMA-Bulkhead) an der Platine anschließen:
     * Bei `PCBA 09`: U.FL-Stecker senkrecht auf die integrierte U.FL-Buchse des `ESP32-C6-MINI-1U` (`U1`) aufklicken.
     * Bei `PCBA 10`: U.FL-Stecker auf die Buchse `J_RF` auf der Platinenunterseite (`B.Cu`) aufklicken.
   * Den EPDM/Silikon O-Ring ($\varnothing 6{,}0 \times 1{,}0\,\text{mm}$) auf das Gewinde der SMA-Bulkhead-Buchse schieben.
   * Die Buchse mit der D-Cut Abflachung in die $5{,}0 \times 4{,}0\,\text{mm}$ stirnseitige Aussparung an der $+X$-Flanke der Unterschale ([`omm_ucs_bottom_shell.stl`](../../hardware/cad/stl/03_pod_cartridges/omm_ucs_bottom_shell.stl)) einsetzen und von außen mit der V4A Edelstahlmutter und Fächerscheibe festziehen (IP67 Dichtsitz).
3. **Akku & Platinenmontage:**
   * Den 600 mAh LiPo Pouch-Akku in die zentrale Akkutasche ($X = 14\dots 54\,\text{mm}$) der Unterschale einlegen.
   * Den 2-Pin JST-Stecker des Akkus an `BAT1` anstecken.
   * Platine mit der Bestückungsseite nach oben in die Gehäuseführung einsetzen, sodass der USB-C Port `J1` exakt in der frontalen Dichtungsmanschette sitzt.
4. **Helm-Audio- & PTT-Kabelbaum anschließen (`J_HELMET`):**
   * Den 6-Pin JST-SH Stecker des Helm-Audio-Kabelbaums in den Header `J_HELMET` auf `B.Cu` ($X=126{,}5, Y=99{,}75\,\text{mm}$ in KiCad bzw. $X_{\text{mod}} = 60{,}5\,\text{mm}$, Buchsenöffnung zeigt nach innen) einstecken.
   * Das hochflexible AWG30/32 Silikonkabel in sanftem Bogen durch den rückseitigen Bodendurchbruch ($9{,}0 \times 9{,}0\,\text{mm}$ bei $X = 55\dots 64\,\text{mm}$) der Unterschale lastfrei nach unten herausführen.
5. **Gehäuse verschrauben (100 % lötkolbenfrei):**
   * Oberschale aufsetzen, umlaufende Dichtungsnaht kontrollieren.
   * 4x M2 $\times 8\,\text{mm}$ Zylinderkopfschrauben (DIN 912) von der Unterseite durch die Senkungen in die eingelegten DIN 934 M2 Muttern handfest über Kreuz anziehen.
6. **Stummelantenne aufschrauben:**
   * Für OMM 2.4 GHz (`PCBA 09`): Die $38\,\text{mm}$ kurze 2.4 GHz Rubber-Duck Stummelantenne auf die SMA-Buchse schrauben.
   * Für OMM 446 (`PCBA 10`): Die $48\,\text{mm}$ kurze 446 MHz Wendel-Stummelantenne auf die SMA-Buchse schrauben.
7. **Helmmontage (ECE 22.06 UCS-Schacht):**
   * Das fertige Modul in die herstellerseitige UCS-Helmmulde (z. B. HJC, Shoei, Schuberth) einschieben und formschlüssig einrasten.
   * Das aus dem Gehäuseboden austretende Audiokabel direkt und unsichtbar unter das Wangenpolster verlegen:
     - 3.5 mm Klinkenbuchse mit den Helmlautsprechern koppeln.
     - 2-Pin Mikrofonbuchse mit dem Schwanenhals- oder Klebemikrofon verbinden.
     - PTT-Leitung zum gewünschten Taster am Kinnteil oder Finger führen.
   * Der stirnseitige USB-C Port bleibt außen am Helm für Unterwegs-Laden per Powerbank oder WebUSB-Flashing zugänglich.

---

### Schritt 4: Universal Front-Knoten (PCBA 05) zusammenbauen
1. **Muttern einlegen (100 % lötkolbenfrei & dauerfest):**
   * **4x M3 Edelstahlmuttern (DIN 934 / DIN 985)** von unten in die formschlüssigen Sechskanttaschen der 4 Gehäuse-Ecken der Unterwanne ([`front_node_lower_tub.stl`](../../hardware/cad/stl/04_front_node/front_node_lower_tub.stl)) eindrücken (vollkommen analog zur Zentralbox).
   * **4x M4 Edelstahlmuttern (DIN 934)** in die formschlüssigen Sechskanttaschen des AMPS-Bohrbilds auf der Gehäuseunterseite einlegen.
   * *Ergebnis:* Reine Stahl-in-Stahl-Verschraubung. Das Gehäuse kann beliebig oft für Kabel-Upgrades oder Wartung geöffnet und mit vollem Anzugsmoment wieder rüttelfest verschraubt werden – kein Ausleiern von Kunststoffgewinden!
2. **UWB-Antenne im Boden installieren:**
   * Taoglas FXUWB10 Flex-Antenne in die Bodentasche der Unterwanne einkleben.
   * U.FL-Kabel nach oben führen.
3. **Platine montieren:**
   * Fertig bestückte PCBA 05 auf die Dämpferdome setzen.
   * UWB-Kabel an die U.FL-Buchse auf `B.Cu` aufklicken.
   * Platine mit 4x M2.5 Schrauben fixieren.
4. **Akustik-Membran:** Hydrophobe Gore ePTFE-Membran über die frontale Schalleintrittsöffnung des Sipeed/Knowles MEMS Mikrofons (`MK1`) kleben.
5. **Kabelbäume anschließen (2-Strang Clean-Architecture):**
   * **Cockpit-Kabelbaum (`cable_cockpit_harness_16p`):** 16-poligen 2.0 mm Verriegelungsstecker auf `J_COCKPIT` aufrasten. Das geschirmte Rundkabel ($\varnothing 6{,}0\,\text{mm}$) durch die südliche TPU-Knickschutztülle nach außen zum **Cockpit-Satellitenverteiler** ([`cockpit_breakout_block.scad`](../../hardware/cad/scad/04_front_node/cockpit_breakout_block.scad)) führen.
   * **Fahrzeug-Kabelbaum (`cable_vehicle_harness_12p`):** 12-poligen 2.0 mm Verriegelungsstecker auf `J_VEHICLE` aufrasten. Das geschirmte Rundkabel ($\varnothing 6{,}5\,\text{mm}$) durch die nördliche TPU-Knickschutztülle nach außen zum **Fahrzeug-Satellitenverteiler** ([`vehicle_breakout_block.scad`](../../hardware/cad/scad/04_front_node/vehicle_breakout_block.scad)) führen.
6. **Gehäuse versiegeln:**
   * TPU-Dichtkämme in die Führungsnuten der Unterwanne einsetzen.
   * Silikon-Rundschnur (Ø 1,5 mm Shore 40A, $30\,\text{cm}$) in die Deckelnut einlegen.
   * Gehäusedeckel aufsetzen und mit 4x M3 $\times 20\,\text{mm}$ Edelstahlschrauben gleichmäßig über Kreuz festziehen.
7. **Satelliten-Verteilerblöcke komplettieren:**
   * **Cockpit-Satellit:** Das 16-polige Kabel wird über den 16-poligen 2.0 mm Verriegelungsstecker auf `J_IN` der Satellitenplatine `PCBA 05B` ([`cockpit_breakout_block.scad`](../../hardware/cad/scad/04_front_node/cockpit_breakout_block.scad)) aufgesteckt. Die Platine stellt 5x USB-C Buchsen (`[ PHONE 20W ]`, `[ DONGLE ]`, `[ HOST ]`, `[ CAM 5V ]`, `[ NAVI 5V ]`) und die formschlüssig verriegelnde 2-polige **JST-GH SMD Buchse (`J6`)** für den Lenker-PTT-Taster bereit (100 % SMD mit 0 mm Unterseiten-Überstand, plan aufliegend). Die M3-Zugentlastungsschiene sichert die Steckerhälse eingesteckter COTS-Kabel vibrationsfest.
   * **Fahrzeug-Satellit:** Das 12-polige Kabel splittet sich im Fahrzeug-Block direkt in die 5 wasserdichten **JST-JWPF (IP67)** Einrast-Buchsen (`[ 12V IN ]`, `[ CAN BUS ]`, `[ MIRROR BSD ]`, `[ AUX LIGHT ]`, `[ GNSS / CLIMATE PUCK ]`). Zur fahrzeugseitigen Plug-and-Play Anbindung werden die modellspezifischen Adapterkabel (z. B. BMW Cartool, BMW CAN Y-Splitter, Harley Fairing Aux) einfach werkzeuglos auf die JWPF-Buchsen angesteckt. Schnappdeckel aufrasten.

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
  * **Rahmenseitiges Dock (bei Festmontage):** Das 3D-Druck COTS-Rahmendock ([`cots_magnetic_frame_dock_body.stl`](../../hardware/cad/stl/02_pod_base/components/cots_magnetic_frame_dock_body.stl)) mit Klemmschelle ([`cots_magnetic_frame_clamp.stl`](../../hardware/cad/stl/02_pod_base/components/cots_magnetic_frame_clamp.stl)) am Ø 26 mm Rahmenrohr unter dem Sitzüberhang mit 4x M3 $\times 16\,\text{mm}$ Schrauben verschrauben (DIN 934 Nut-Pockets). Die 2-Pin Magnet-Pogo Buchse (HytePro M411) formschlüssig einlegen (der integrierte Haltekragen verhindert jedes Herausziehen beim Abreißen) und an Peitsche 1 bzw. 2 des DTM-12 Kabelbaums anschließen. *(Alternativ: Reiner elastischer Inline-Breakaway-Kabelstrang ohne festes Gehäuse).*
  * **Koffer-Vorderwand & Dichtung:** Ein einzelnes $\varnothing 12\,\text{mm}$ Loch seitlich-innen an der Koffer-Vorderwand oberhalb des Schwingenlagers bohren (im Wind- und Spritzwasserschatten; der **Kofferboden bleibt zu 100 % lochfrei**). Die geteilte EPDM/TPU-Dichtung ([`010_saddlebag_hole_grommet_split.stl`](../../hardware/cad/stl/02_pod_base/parts/010_saddlebag_hole_grommet_split.stl)) einsetzen, das 2-adrige Flachbandkabel der Magnetstecker-Kupplung hindurchführen und am integrierten Klemmturm per Mini-Kabelbinder zugentlasten. Im Kofferinneren das Kabel parallel zum Deckel-Fangband lastfrei zum Kofferdeckel-Dock führen.
* **Heck-Radar (Schwerlast-Neigegelenk & Spritzwasserschutz):**
  * **Vormontage auf der Werkbank (100 % lötkolbenfrei):** Das versiegelte Radar 2.0 Gehäuse ([`radar_mr20_housing.stl`](../../hardware/cad/stl/05_accessories/radar_mr20_housing.stl)) mit seinen zwei innenliegenden DIN 934 M4-Muttern wird über zwei DIN 912 M4 $\times$ 12 mm Schrauben fest an die Adapterplatte ([`radar_swivel_tilt_cradle.stl`](../../hardware/cad/stl/02_pod_base/radar_swivel_tilt_cradle.stl)) geschraubt. Die Passungs-Bosse nehmen 100 % der Scherkräfte auf.
  * **Option A: Montage am Kennzeichenträger:** Den Kennzeichenträger ([`radar_license_plate_bracket.stl`](../../hardware/cad/stl/02_pod_base/radar_license_plate_bracket.stl)) unter die unteren M6-Kennzeichenschrauben klemmen. Die Hirth-Zunge der Adapterplatte in die Gabelaufnahme einschieben, Nickwinkel waagerecht zur Fahrbahn justieren und mit einer DIN 912 M5 $\times$ 25 mm Klemmschraube in die versenkte M5-Mutter formschlüssig festziehen.
  * **Option B: Montage am Heckkotflügel (Bobber / Custom-Bike):** Den Stealth Center Under-Fender Mount ([`radar_center_underfender_mount.stl`](../../hardware/cad/stl/02_pod_base/radar_center_underfender_mount.stl)) mittig unter die Kotflügelkante kleben (3M VHB 5952) oder mit 2x M4/M5 Senkkopfschrauben verschrauben. Die Neigungswiege in die Clevis-Gabel einschieben und per M5-Schraube arretieren. Der integrierte $42\,\text{mm}$ Schmutzfänger-Spoiler hält Reifengischt zuverlässig vom Drehgelenk und der M8-Kabelverschraubung ab.
  * **Spritzwasser-Verkabelung (Abtropfbogen):** Das 2-adrige FLRY-B Kabel von Peitsche 3 im rückseitigen Kanal der Trägerwirbelsäule führen und in einer nach unten hängenden Abtropfschlaufe (Drip-Loop) von unten durch die M8 IP68-Kabelverschraubung führen. Der monolithische Roost-Deflector am Gehäuseboden schirmt die Verschraubung vollständig gegen aufgewirbelte Reifengischt ab.
* **Front-Knoten & Satelliten-Verteiler (Stealth-Montage unterm Fairing):**
  * **Front-Node Montage:** Direkt unter der Verkleidung (Sharknose FLTRX, Batwing FLHX oder CVO ST) an den runden Metallstangen des Verkleidungsgeweihs (Ø 16–19 mm Fairing Support Brackets) mit der 2-teiligen Verkleidungs-Rohrschelle ([`front_node_fairing_tube_clamp.stl`](../../hardware/cad/stl/04_front_node/front_node_fairing_tube_clamp.stl)) oder per EPDM-Kabelbinder-Kreuztunnel vibrationsentkoppelt verschrauben (0° oder 90° drehbar). Hält Lenker und Riser 100% frei; sitzt unmittelbar neben der Headunit, dem OEM-USB-Kabelbaum und dem Ottocast CarPlay/AA Dongle.
  * **Satelliten-Dovetail-Verbund:** Cockpit- und Fahrzeug-Satellit können per Schwalbenschwanzführung zu einer Kombi-Box zusammengesteckt und im Handschuhfach oder hinter der Verkleidungswand fixiert werden.
  * **Plug-and-Play Fahrzeug-Anbindung (Zero Wire-Cut):**
    * `[ 12V IN ]`: Mit dem **Harley Fairing-Aux Adapterkabel** (`cable_adapter_jwpf_hd_fairing_aux`) direkt an den 2-poligen OEM-Zubehörstecker unter der Verkleidung anstecken (Klemme 15 Zündungsplus, schaltet automatisch mit Zündung).
    * `[ CAN BUS ]`: Mit dem **Harley CAN Y-Splitter-Adapterkabel** (`cable_adapter_jwpf_hd_can_splitter`) am Diagnosestecker / Tacho-Y zerstörungsfrei einschleifen.
    * `[ AUX LIGHT ]`: Über das **Deutsch DT-2 Adapterkabel** (`cable_adapter_jwpf_deutsch_dt2_aux`) an Zusatzleuchten oder Navi anschließen.
    * `[ GNSS / CLIMATE PUCK ]`: Über das **Qwiic JST-SH Adapterkabel** (`cable_adapter_jwpf_qwiic_sh`) zum SAM-M10Q GNSS- & Klimasensor im Luftkanal führen.

### 5.2 Montage Adventure-Plattform (BMW GS / GSA Familie)
* **Zentralbox:** Im Rahmendreieck unter der Fahrersitzbank auf 4x M4 Silentblöcken montieren.
* **Cockpit, Front-Knoten & Satelliten (Plug & Play am Schnabel / Lenker):**
  * **Front-Node Montage:** An der Ø 12 mm GPS-Querstrebe über dem TFT-Display oder an der Verkleidungsstrebe mit der 2-teiligen Klemmschelle fixieren.
  * **Cockpit-Satellit:** Wird separat direkt am Lenker / Riser platziert (mittels Kabelbinder-Tunnel), sodass Smartphones und Zubehör ohne Kabelsalat am Lenkkopf geladen werden.
  * **Fahrzeug-Satellit:** Wird fahrzeugfest am Steuerkopf / Schnabel befestigt.
  * **Plug-and-Play Fahrzeug-Anbindung (Zero Wire-Cut):**
    * `[ 12V IN ]`: Mit dem vorkonfektionierten **BMW Cartool-Adapterkabel** (`cable_adapter_jwpf_bmw_cartool`) direkt in den originalen 3-Pin Cartool-Zubehörstecker (BMW Teilenr. 83300413585) über dem Ölkühler / Lenkkopf einstecken. Liefert sauberes Zündungsplus (KL15) mit automatischer ZFE/BCO-Abschaltung nach 60 Sekunden (kein Entladen der Starterbatterie, keine CAN-Bus Fehlereinträge).
    * `[ CAN BUS ]`: Mit dem **BMW CAN Y-Splitter-Adapterkabel** (`cable_adapter_jwpf_bmw_can_splitter`) an der Vorbereitung Navigationssystem / TFT zerstörungsfrei einschleifen.
    * `[ AUX LIGHT ]` (GSA): Mit dem **Deutsch DT-2 Adapterkabel** (`cable_adapter_jwpf_deutsch_dt2_aux`) direkt an Zusatzscheinwerfer (z.B. Denali D3/D7 oder Wunderlich) ankoppeln (geschaltet über PCBA 05 High-Side Switch TPS1H100).
    * `[ GNSS / CLIMATE PUCK ]`: Mit dem **Qwiic JST-SH Adapterkabel** (`cable_adapter_jwpf_qwiic_sh`) zum SAM-M10Q GNSS- & Klimasensor im Verkleidungsschnabel führen.
* **Pod 1 & Pod 2 (Strikt fahrzeugfest montiert - KEINE Pods im Alukoffer!):**
  * *Option A (Vario-Koffer / GS Standard):* Transition-Docks ([`adventure_transition_dock_base.stl`](../../hardware/cad/stl/02_pod_base/adventure_transition_dock_base.stl)) in der Sitzbank-Bügelfalte (Ø 28 mm Rahmenrohr) verbunden mit der Sattelbrücke ([`adventure_underseat_cross_rail.stl`](../../hardware/cad/stl/02_pod_base/adventure_underseat_cross_rail.stl)).
  * *Option B (Edelstahl-Rohrkofferträger / GSA):* Heavy-Duty GSA Cage Docks ([`adventure_gsa_cage_dock_body.stl`](../../hardware/cad/stl/02_pod_base/adventure_gsa_cage_dock_body.stl)) im 45 mm Totraum des Trägers zwischen Trägerrohr und Radkasten.
  * *Wichtiger Hinweis zu Aluminium-Koffern:* Pods dürfen **unter keinen Umständen im Inneren von Aluminium-Koffern** montiert werden (Faradayscher Käfig schirmt 2.4 GHz und 6.5 GHz UWB vollständig ab!). Die Pods verbleiben bei Kofferabnahme sicher am Motorrad. Eine 2-Pin Magnetkupplung ist bei Reiseenduros nur dann relevant, wenn Kofferinnenräume optional mit 5V Ladespannung versorgt werden sollen.
* **Heck-Radar (Adventure Gepäckbrücke):**
  * **Rohrträger-Klemmschelle:** Untere Trägerbasis ([`adventure_rack_radar_mount.stl`](../../hardware/cad/stl/02_pod_base/adventure_rack_radar_mount.stl)) und obere Kappe ([`adventure_rack_radar_clamp_cap.stl`](../../hardware/cad/stl/02_pod_base/adventure_rack_radar_clamp_cap.stl)) um das hintere Ø 18 mm Querrohr der Gepäckbrücke legen.
  * 2x DIN 934 M5 Muttern in die Taschen der oberen Kappe einlegen. Zwei DIN 912 M5 $\times$ 25 mm Schrauben von unten einschrauben und handfest anziehen. (Durch den Schraubenzugang von unten bleibt der Halter auch bei montierter Alukoffer-Topcase-Trägerplatte voll justierbar!).
  * Das vormontierte Radar 2.0 Gehäuse mit `radar_swivel_tilt_cradle.stl` in die Clevis-Gabel einschieben, Neigungswinkel ausrichten und mit M5 $\times$ 25 mm Klemmschraube formschlüssig in die Hirth-Verzahnung spannen.
  * Der integrierte $45^\circ$-Abweiserkeil schützt das Gelenk und das M8-Kabel wirksam gegen Schotterschlag von grobstolligen Enduro-Hinterreifen.

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
