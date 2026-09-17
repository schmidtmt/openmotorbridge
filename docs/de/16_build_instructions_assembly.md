# 16 - Bauanleitung, Verkabelung & Fahrzeug-Installation

Dieses Dokument ist die vollständige, praxisorientierte Schritt-für-Schritt-Bauanleitung für den Zusammenbau und die fahrzeugspezifische Montage eines kompletten **OpenMotorBridge (v8.0)** Gesamtsystems.

---

## 1. Übersicht des Gesamtkits (Was wird gebaut?)

Ein vollständiges OpenMotorBridge-Fahrzeugkit besteht aus folgenden Kern-Baugruppen:

```text
                      ┌─────────────────────────────────────────┐
                      │    1x ZENTRALE MAIN BOX (IP67)          │
                      │    (Unter der Sitzbank / im Heck)       │
                      │    • Unterwanne + Zwischenboden + Deckel│
                      │    • Hauptplatine (ESP32-S3, Codec, USV)│
                      │    • 2.200 mAh LiPo-Pufferakku          │
                      └────────────────────┬────────────────────┘
                                           │
                         1x ZENTRALER KABELBAUM (HD26 IP67)
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         │                                 │                                 │
         ▼                                 ▼                                 ▼
┌──────────────────┐             ┌──────────────────┐              ┌──────────────────┐
│ 1x POD 1 (LINKS) │             │ 1x POD 2 (RECHTS)│              │ 1x POD 3 (HECK)  │
│ (Rahmen / Koffer)│             │ (Rahmen / Koffer)│              │ (Heckbürzel)     │
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
                                 │ • AMPS- / Rohrklemmen-Aufnahme   │
                                 │ • CarPlay/AA Dongle-Port (USB-A) │
                                 │ • Smartphone USB-PD Schnelllader │
                                 │ • Knowles MEMS Fahrtwind-Sensor  │
                                 │ • Batteriefreier Lenker-PTT      │
                                 └──────────────────────────────────┘
```

---

## 2. Bereitstellung vor Montagebeginn (Pre-Assembly Checklist)

Alle Einzelteile, Platinen-Bestelldaten und COTS-Zukauflisten sind detailliert in **[Kapitel 15: Stücklisten & SMT-Fertigungsdaten](file:///Users/schmidtm/openMotorBridge/docs/de/15_bom_manufacturing.md)** aufgeführt. Vor Montagebeginn sicherstellen, dass folgende Baugruppen bereitliegen:

* [ ] **3D-Druckteile (MJF PA12 schwarz oder FDM ASA/PET-CF):**
  * 1x Main Box (Unterwanne, Zwischenboden mit Wanne für 2.200 mAh LiPo, Deckel)
  * 3x Pod-Basisgehäuse & 3x Pod-Schottwände
  * 3x Kassetten-Basisschlitten, Inlays (z. B. Sena, Cardo oder Blindkassette) & 2x Rastwippen
  * 1x Heck-Pod 3 OMM-Radom
  * 1x Front-Knoten (Unterwanne mit AMPS-Nut-Pockets, Deckel, TPU-Dichtkämme & USB-C Kappe)
  * 1x Fahrzeugspezifisches Montage-Kit (BMW GS Klemmen / Harley Kofferdeckel-Docks)
* [ ] **Vollautomatisch bestückte Platinen (von JLCPCB / Eurocircuits):**
  * 1x PCBA 01 (Zentralbox), 3x PCBA 02 (Pod-Base), 2x PCBA 03 (Cartridge), 1x PCBA 04 (Heck-Pod 3), 1x PCBA 05 (Front-Knoten)
  * *(Optional: PCBA 06 MagSafe Dock, PCBA 07 Smart-Keyfob)*
* [ ] **V4A Edelstahl-Normteile & Federn (IKEA-Prinzip – 100 % lötfrei):**
  * 8x DIN 934 / DIN 985 M3 Edelstahlmuttern (für Gehäuse-Nut-Pockets)
  * 4x DIN 934 M4 Muttern (für AMPS-Nut-Pockets in Front-Node Wanne)
  * 4x M3 x 40 mm Schrauben (Zentralbox), 4x M3 x 20 mm Schrauben (Front-Node)
  * 8x M2.5 x 6 mm Platinenschrauben, 6x M2 x 8 mm Senkkopf (Schottwände), 8x M2 x 6 mm (Kassetten)
  * 2x DIN 7 M2 x 8 mm Zylinderstifte (Wippenachsen), 2x DIN 6325 Ø 6 x 8 mm gehärtete Stahlanker
  * 2x Wippen-Rückstellfedern, 6x Auto-Eject Druckfedern, 1x N52 Neodym-Entriegelungsschlüssel
* [ ] **Dichtungen & Pufferakku:**
  * Silikon-Rundschnur Ø 1,5 mm Shore 40A ($40\,\text{cm}$ Main Box, $30\,\text{cm}$ Front-Knoten)
  * 3x Silikon-Flanschdichtungen für Pod-Mundlöcher, Gore ePTFE Membranpads
  * **1x 1S LiPo Flat-Pack 2.200 mAh** ($68 \times 39 \times 5{,}0\,\text{mm}$, Typ 504068 / 503870) mit Molex Micro-Fit 3.0 Stecker
* [ ] **Vorkonfektionierte COTS-Kabel (kein Crimpen nötig):**
  * 1x HD26 IP67 Kabelpeitsche, 3x M8 6-Pin PUR-Kabel (1.0 m / 1.5 m)
  * 1x 2-Pin JST-PH Stromkabel mit Posi-Tap Abzweigverbindern (Cockpit 12V Zündungsplus & Masse)
  * JST-SH Kassetten-Kabelbäume (8-Pin `J_ACT` für Hubmagnete, 6-Pin `J2` für Audio/DC)
* [ ] **Werkzeuge:**
  * Innensechskantschlüsselsatz (1.5 / 2.0 / 2.5 / 3.0 mm), Torx TX10 / PH1 Schraubendreher, Gabelschlüssel SW 7 / 8 mm, Cuttermesser, Silikonfett

---

## 3. Montage der Baugruppen (Schritt-für-Schritt)

### Schritt 1: Zentralbox (Main Box) montieren
1. **Muttern einlegen:** 4x DIN 934 / DIN 985 M3 Edelstahlmuttern von unten in die Sechskant-Mutternaschen (Nut Pockets) der Unterwanne ([`main_box_lower_case.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lower_case.stl)) eindrücken.
2. **Hauptplatine einsetzen:** Fertig bestückte PCBA 01 (`openmotorbridge_central_box`) auf die Dämpferdome setzen und mit 4x M2.5 $\times 6\,\text{mm}$ Schrauben handfest fixieren.
3. **Zwischenboden & 2.200 mAh LiPo-Akku:** Den Zwischenboden ([`main_box_mid_tray.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_mid_tray.stl)) aufsetzen. Den **2.200 mAh Flat-LiPo-Akku** ($68 \times 39 \times 5{,}0\,\text{mm}$) in die Wanne einlegen, das Molex Micro-Fit Kabel durch die Zwischenbodenöffnung an `J_BAT` anstecken und die Zelle mit einem Streifen EPDM-Band schwingungsdämpfend sichern.
4. **Dichtung & Deckel:** Silikon-Rundschnur (Ø 1,5 mm, $40\,\text{cm}$) dünn mit Silikonfett einreiben und in die Deckelnut einlegen. Gore-Membran auf den Belüftungssitz kleben. Den Deckel ([`main_box_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lid.stl)) vorerst nur lose aufsetzen. *(Wichtiger Hinweis: Die finale 4x M3-Verschraubung und Dichtungskompression erfolgt erst nach dem erfolgreichen Tisch-Smoke-Test in Abschnitt 4!)*

---

### Schritt 2: Satelliten-Pods 1, 2 und Heck-Pod 3 montieren
1. **Basisplatine einsetzen:** Die fertig bestückte PCBA 02 (`openmotorbridge_pod_base`) in die Führungsnuten des Pod-Basisgehäuses ([`pod_base_housing.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod_base_housing.stl)) einschieben. Die M8 6-Pin IP67 Buchse durch die rückseitige Bohrung führen, O-Ring aufschieben und von außen die M8-Mutter mit Gabelschlüssel SW 10 handfest anziehen ($1{,}2\,\text{Nm}$).
2. **Auto-Eject Schnappfedern einsetzen:** In die beiden rückseitigen Federtaschen der Schottwand ([`03_pod_bulkhead_partition.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl)) je eine V4A Druckfeder ($\varnothing 4{,}5 \times 15\,\text{mm}$) einstecken.
3. **Schottwand fixieren:** Die Schottwand mit den Federn voran in das Pod-Gehäuse einschieben, bis sie an der inneren Anschlagschulter anliegt. Mit 2x M2 $\times 8\,\text{mm}$ Senkkopfschrauben von außen durch die Gehäusewand bündig verschrauben.
4. **Prüfung:** Die federbelasteten Harwin 6-Pin Docking-Pogo-Pins müssen zentriert und plan durch das Schottwandfenster ragen. Wiederholen für Pod 1, Pod 2 und Pod 3.

---

### Schritt 3: Multi-Protokoll Gateway-Kassetten 1 & 2 montieren (z. B. Sena & Cardo)
> **Architektur-Grundsatz:** Slot 1 und Slot 2 sind **Multi-Protokoll Mesh-Gateway-Einschübe**, keine isolierten Fahrer- oder Sozius-Headsets. Ein Modul (z. B. Sena SPIDER X Slim in Slot 1) dockt an das Sena Mesh-Netzwerk an, während das zweite Modul (z. B. Cardo Packtalk Edge in Slot 2) parallel das Cardo DMC-Netzwerk bedient. Die Zentralbox vermittelt die Audiodaten digital zwischen beiden Funkwelten.

1. **Platine einsetzen:** Kassettenplatine PCBA 03 Rev 2.0 in den Kassetten-Schlitten ([`cartridge_base_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl)) einklicken.
2. **Gateway-Inlay & Mechatronik montieren:**
   * **Klasse S (Smart Modular Cartridge mit Mechatronik • Sena SPIDER / Cardo Packtalk):**
     * 4x Miniatur-Aktuatoren ($\varnothing 6{,}5 \times 12\,\text{mm}$) mit TPU-Schutzkappen in die Führungsbrücke des Inlays ([`cartridge_insert_sena.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) bzw. [`cartridge_insert_cardo.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl)) einlegen.
     * Aktuator-Niederhalteplatte auflegen und mit 4x M2 $\times 6\,\text{mm}$ Senkkopfschrauben sichern.
     * Vorkonfektioniertes 8-poliges JST-SH Kabel `J_ACT` von den Aktuatoren auf Header `J_ACT` von PCBA 03 stecken (kein Crimpen!).
     * Headset in das Konturbett einlegen und mit dem Schnellspann-Niederhalter fixieren.
     * Vorkonfektioniertes J2-Kabel anstecken.
   * **Klasse D (Hermetische Blindkassette):**
     * Schutzschlitten [`cartridge_insert_blindkassette.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_blindkassette.stl) einsetzen, falls ein Slot vorübergehend ungenutzt bleibt oder als regendichte Dry Box für Kleinteile dient.
3. **Flanschdichtung:** Silikon-Formdichtung auf den Kassettenkragen aufziehen und dünn mit dielektrischem Silikonfett benetzen.

> [!TIP]
> **Vorrüstungs-Strategie für geplante Zweit-Headsets (z. B. "Black-Friday-Kauf"):**
> Wer im Frühjahr startet und vorerst nur ein Headset besitzt (z. B. Sena SPIDER X in Slot 1) und bereits weiß, dass später ein zweites System hinzukommt (z. B. Cardo Packtalk Edge im Herbst/Winter), hat zwei clevere Optionen:
> 1. **Option A (Hermetische Blindkassette / Dry Box):** Man druckt [`cartridge_insert_blindkassette.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_blindkassette.stl). Slot 2 dient bis zum Upgrade als wasserdichtes Notfall-Staufach (Bargeld, Ersatzsicherungen, Ventileinsatz). Zum Aufrüsten werden lediglich die 4x M2 Schrauben gelöst und das Cardo-Inlay auf denselben Basisschlitten geschraubt.
> 2. **Option B (Direkte Cardo-Vorrüstung ohne Gerät):** Man baut direkt die vollständige Cardo-Kassette ([`cartridge_insert_cardo.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl)) ein, lässt aber die interne Adapter-Platine/Verkabelung noch weg (oder verschließt den leeren AirMount-Sockel mit der beiliegenden Cardo-Silikonschutzkappe bzw. einem TPU-Dummystopfen).
>    * **Firmware-Verhalten:** Da ohne Platine kein 1-Wire DS2431 EEPROM antwortet, erkennt die openMotorBridge Firmware den Slot automatisch als *„Empty Slot / Blindkassette“* und schaltet den DSP-Audiokanal hardwareseitig auf **-96 dB Mute**. Es gibt kein Rauschen, Brummen oder Fehlauslösungen!
>    * **Upgrade-Vorteil:** Sobald das Zweitgerät da ist, wird es einfach in den bereits montierten Sockel eingeklinkt – null Umbauaufwand am Motorrad!

---

### Schritt 3.1: Montage des magnetischen Diebstahlschutzes (Kassetten-Wippen-Mechanismus)

```text
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
4. **Funktionsprüfung:**
   * Die Sägezahn-Rastkralle am vorderen Arm muss durch Federkraft $2{,}5\,\text{mm}$ über die Führungsfeder hinausragen.
   * Den N52 Neodym-Blockmagneten außen an die Höhe des Stahlankers halten: Die Wippe kippt um $-4{,}8^\circ$, und die Kralle taucht vollständig bündig in den Schlitten ein.

---

### Schritt 4: Heck-Kassette Pod 3 & OMM-Radom (LoRa, GNSS & HF-Bypass)
1. **Transceiver-Platine einsetzen:** PCBA 04 (`openmotorbridge_rear_pod3`) in den 3. Basisschlitten ([`cartridge_base_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl)) einlegen und mit M2.5 Schrauben sichern.
2. **OMM-Radom montieren:** Das dielektrische Radom ([`cartridge_antenna_bracket_omm.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_antenna_bracket_omm.stl)) aufsetzen.
3. **SMA-Bulkhead-Buchsen montieren (Bypass für externe Antennen):**
   * Die 3x SMA-Flanschbuchsen durch die Kassetten-Stirnwand führen und festziehen ($0{,}8\,\text{Nm}$).
   * Koax-Stecker auf die Murata MM8030 Umschaltbuchsen klicken (`J3` = 2.4 GHz Mesh, `J4` = 868 MHz LoRa, `J5` = GNSS).
   * Werden keine externen Antennen angeschraubt, arbeiten die internen Antennen im Radom zu 100 % autark.

---

### Schritt 5: Universal Front-Knoten (PCBA 05) zusammenbauen (100 % lötfrei)
1. **Muttern einlegen (Nut-Pockets):**
   * 4x DIN 934 / DIN 985 M3 Edelstahlmuttern von unten in die Sechskant-Mutternaschen der Gehäuse-Ecken der Unterwanne ([`front_node_lower_tub.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_lower_tub.stl)) eindrücken.
   * 4x DIN 934 M4 Muttern in die Sechskant-Taschen des AMPS-Lochbilds ($30 \times 38\,\text{mm}$) am Gehäuseboden einlegen.
2. **Akustik-Membran aufkleben:** Hydrophobe Gore ePTFE-Membran über die Schallöffnung des digitalen MEMS-Mikrofons (MSM261S4030H0R / SPH0645) kleben.
3. **Platine montieren:** Fertig bestückte Front-Node Platine PCBA 05 (`openmotorbridge_front_node`) mit 4x M2.5 Schrauben handfest fixieren.
4. **HF-Antennenmontage (ESP32-S3 2,4 GHz):**
   * Die flexible 2,4-GHz-FPC-Dipolantenne (Molex 146153) in die Klebetasche an der Innenseite des Deckels ([`front_node_upper_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_upper_lid.stl)) einkleben.
   * U.FL-Stecker des Mikro-Koaxialkabels senkrecht auf das ESP32-S3 Modul aufklicken.
5. **Vorkonfektionierte COTS-Kabel einlegen (kein Crimpen!):**
   * **Vordere Öffnung (Südwand für USB):**
     * Kurzes USB-A/C Flachbandkabel an Port `J6` (CarPlay/Android Auto Dongle / Ottocast) stecken.
     * 1,0 m USB-C Ladekabel an Port `J5` (Handschuhfach / 20W Fast Charging) stecken.
     * USB-Host Kabel an `J4` stecken (Verbindung zum OEM-Display / Radio).
   * **Rechte Öffnung (Ostwand):** Elastische Staubschutzkappe ([`front_node_usbc_cap_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_usbc_cap_tpu.stl)) in Service-Port `J7` einsetzen.
   * **Linke Öffnung (Westwand für Strom & Signale):**
     * Fertiges JST-PH 2-Pin Litzenkabel für 12V Bordnetz (KL15 & Masse) an `J1` stecken.
     * JST-PH 3-Pin Kabel für CAN-Bus an `J2` stecken (nur bei Fairing-Bikes mit Front-Audio-CAN nötig).
     * Fertiges JST-PH 2-Pin Litzenkabel vom Lenkertaster an `J3` (PTT) stecken.
6. **Dichtkämme einsetzen & Deckel verschließen:**
   * Dünnen Film Silikonfett auf die elastischen TPU-Dichtkämme ([`front_node_cable_glands_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_cable_glands_tpu.stl)) auftragen und in die Gehäusetaschen schieben.
   * Silikon-Rundschnur (Ø 1,5 mm, $30\,\text{cm}$) in die Deckelnut einlegen.
   * Den Deckel vorerst nur lose aufsetzen (die 4x M3 Schrauben werden erst nach dem erfolgreichen Tisch-Smoke-Test in Abschnitt 4 festgezogen).

---

## 4. Tisch-Testaufbau & Dry-Run (Werkstatt / Schreibtisch / Wohnung) mit USB-Kabeln VOR der Bike-Montage

Der größte und teuerste Fehler beim Motorrad-Customizing ist es, Module ungetestet in enge Verkleidungen und unter Kraftstofftanks einzubauen, um erst bei der ersten Probefahrt festzustellen, dass ein Stecker wackelt, eine Firmware fehlt oder ein Intercom-Kanal nicht schaltet.

OpenMotorBridge ist von Grund auf so konstruiert, dass das **vollständige Gesamtsystem auf dem Schreibtisch oder Werkbank-Tisch mit Standard-USB-C-Kabeln zu 100 % in Betrieb genommen, geflasht, gekoppelt und getestet werden kann – ganz ohne Motorradbatterie, ohne Kfz-Kabelbaum und im Warmen**.

### 4.1 Warum der Tisch-Trockentest unbezahlbar ist
* **Im Warmen & Bequemen:** Fehlersuche auf der Couch, am Schreibtisch oder in der warmen Werkstatt statt auf Knien in der kalten Garage bei schlechtem Licht.
* **Sichtkontrolle bei offenen Gehäusen:** Status-LEDs (ESP32-S3 RGB-LEDs, RP2040 Status, Ladeanzeige des BQ24074-Controllers) und Prüfpunkte sind direkt sichtbar.
* **Akustischer Klick-Check:** Die mechanischen Tauchanker-Hubmagnete der Kassetten (`PCBA 03`) sind ohne Motor- oder Umgebungsgeräusche klar hör- und fühlbar ("Klack-Klack-Klack-Klack").
* **Kabelbaum-Schonung:** Der 26-polige HD26-Hauptkabelbaum bleibt während des Tischtests sicher verpackt im Karton und wird erst verlegt, wenn alle Platinen und Kassetten nachweislich fehlerfrei arbeiten.
* **Minimale Werkzeuge:** 2 bis 3 handelsübliche USB-C-Kabel (Handy-Ladekabel) und ein normales Multiport-USB-Netzteil / Powerbank / Laptop ($5\,\text{V} / \ge 2{,}0\,\text{A}$) genügen.

### 4.2 Was wird benötigt (Tisch-Labor-Bedarf)
* [ ] 1x USB-Netzteil (Multiport $5\,\text{V} / \ge 2{,}4\,\text{A}$) oder Powerbank / Laptop
* [ ] 2–3x Standard USB-C Kabel (Slim-Steckergehäuse für Port B der Pods)
* [ ] 1x Kurzes M8-Prüfkabel (optional zur direkten Kopplung von Heck-Pod 3 an Port A der Zentralbox)
* [ ] 1x PC/Mac/Laptop oder Smartphone/Tablet mit Google Chrome oder MS Edge (für WebSerial Flasher & WebBLE PWA)
* [ ] Die eigenen Intercom-Geräte (z. B. Sena 50S, Cardo Packtalk Edge) und der Fahrerhelm

### 4.3 Der Tisch-Verdrahtungsplan (Labor- & Wohnungs-Setup)

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
│  │   (PCBA 01)   │     │   (PCBA 05)   │      │   (PCBA 02)   │             │
│  │  Port J7 USB-C│     │  Port J5 USB-C│      │ Port B (USB-C)│             │
│  └───────┬───────┘     └───────┬───────┘      └───────┬───────┘             │
│          │                     │                      │                     │
│          │   ESP-NOW Funk      │                      │ 1-Wire & Pogo       │
│          │◄───────────────────►│                      ▼                     │
│          │   (< 1.8 ms Latenz) │             ┌───────────────────┐          │
│          │                     │             │ SMR-KASSETTE      │          │
│          │                     │             │ (Sena / Cardo)    │          │
│          │                     │             └────────┬──────────┘          │
│          │ WebBLE / WebSerial  │                      │                     │
│          ▼                     ▼                      ▼                     │
│    [ SMARTPHONE / LAPTOP MIT PWA ]             [ FAHRER-HELM ]              │
│    (Chrome / Edge: Flasher & Dashboard)        (Bluetooth gekoppelt)        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.4 Schritt-für-Schritt Tischverkabelung & Modulprüfung

1. **Zentralbox (PCBA 01) anstecken:**
   * Standard USB-C Kabel in Port `J7` (hinter der Service-Schraubkappe) stecken und mit Laptop oder USB-Netzteil verbinden.
   * Der ESP32-S3 bootet sofort, das BQ24074 Powermanagement lädt den 2.200 mAh LiPo-Pufferakku und die blaue Status-LED pulsiert langsam.
   * Bei Verbindung mit dem Laptop meldet sich der interne USB-JTAG/Serial-Controller direkt als COM-Port bzw. `/dev/ttyACM0` an.

2. **Universal Front-Node (PCBA 05) anstecken:**
   * Ein zweites USB-C Kabel in Port `J5` (20W PD Schnellladebuchse) einstecken.
   * Der ESP32-S3 des Front-Knotens startet und synchronisiert sich per ESP-NOW vollautomatisch mit der Zentralbox ($< 1{,}8\,\text{ms}$ Latenz, keine manuelle IP- oder WLAN-Konfiguration erforderlich).
   * Die grüne Sync-LED auf PCBA 05 leuchtet dauerhaft als Bestätigung der Funkbrücke.

3. **Satelliten-Pods 1 & 2 (PCBA 02) mit Kassetten testen:**
   * Ein USB-C Kabel in **Port B (USB-C Slim-Port)** der Pod-Basis einstecken.
   * Die Basisplatine wird mit $+5\,\text{V}$ versorgt; die gefederte Pogo-Pin-Kontaktleiste `J1` wird scharfgeschaltet.
   * Wechselkassette (Sena 50S, Cardo Packtalk Edge oder Sena SPIDER X) in die Führungsschiene einschieben, bis die Haltekralle hörbar einrastet.
   * Der integrierte 1-Wire EEPROM (DS2431) übermittelt Kassetten-Typ und Seriennummer an die Zentralbox.

4. **Heck-Pod 3 (PCBA 04) prüfen:**
   * Provisorisch mit dem kurzen M8-Testkabel an Port A der Zentralbox anstecken.
   * RP2040 Co-Prozessor und SX1262 LoRa melden sich im PWA-Dashboard grün.
   * Am Fensterbrett platziert liefert der u-blox MAX-M10S innerhalb von 25–35 Sekunden den ersten GNSS-3D-Fix.

### 4.5 Erstinbetriebnahme: WebSerial 1-Click Flasher & der 4-Punkte IKEA Smoke-Test

Dank der modernen **WebSerial-Integration** in der OpenMotorBridge PWA ist für die Erstinbetriebnahme **keine Installation von Python, PlatformIO, Treibern oder Terminal-Tools** erforderlich:

#### Methode A: WebSerial 1-Click Installer (Empfohlen für Endanwender)
1. Zentralbox per USB-C Kabel an den PC/Mac/Laptop anschließen.
2. Chrome, Edge oder Opera öffnen und die PWA aufrufen (oder lokal über den System-Builder).
3. Im Tab *System Builder* auf **„USB-C verbinden & Flashen“** klicken.
4. Den erkannten seriellen Port (z. B. `CP2102N` / `ESP32-S3`) auswählen.
5. Die PWA flasht Bootloader, Partitionen, Firmware (`openmotorbridge_main_v8.12.bin`) und SPIFFS-Dateisystem vollautomatisch mit Fortschrittsbalken und Live-Protokoll.

#### Der geführte 4-Punkte IKEA Smoke-Test
Vor dem Aufsetzen der Gehäusedeckel wird der interaktive Selbsttest in der PWA gestartet:
1. [x] **Bordnetz & USV (Check 1):** 5.04V Buck-Schiene aktiv, USV-LiPo (2.200 mAh) lädt mit 4.18V Ladeschlussspannung.
2. [x] **Kassetten & Aktuatoren (Check 2):** 1-Wire DS2431 Auslesen der Kassetten-IDs (Sena / Cardo), Pogo-Pin Kontaktierung und automatischer 4-Aktuator Klicktest (Klick 1 bis 4).
3. [x] **Front-Knoten & Cockpit (Check 3):** I2C-Ping Sipeed/Knowles MEMS Mikrofon, SDP31 Staudruck-Sensor (0.02 hPa) und Lenker-PTT Taster.
4. [x] **Heck-Pod 3 (Check 4):** SX1262 LoRa 868 MHz Ping-Echo und u-blox GNSS 3D-Fix.

#### Methode B: Manuelles Flashen via PlatformIO (Power-User Fallback)
```bash
# 1. Zentralcontroller via USB-C flashen (ESP32-S3)
cd openMotorBridge/firmware/main_controller && pio run --target upload && pio run --target uploadfs
# 2. Heck-Co-Prozessor flashen (RP2040 in Pod 3)
cd ../rear_coprocessor && pio run --target upload
# 3. Front-Knoten flashen (ESP32-S3)
cd ../front_node && pio run --target upload
```

### 4.6 Kassetten-Klicktest, Intercom- & Helm-Pairing im Warmen
* **Mechanischer Klick-Check:** Im PWA-Diagnosemenü die 4 Aktuatoren manuell oder zyklisch ansteuern. Die Tauchanker drücken die Tasten des Sena/Cardo spür- und hörbar durch.
* **Helm-Pairing:** Fahrer- und Soziushelm per Bluetooth mit den Intercoms koppeln.
* **Audio-Routing & Ducking:** Musik vom Smartphone abspielen. Beim Druck auf den Lenker-PTT-Taster (oder PIN 1/2 an `J3` des Front-Knotens) duckt sich die Musik sofort um $-18\,\text{dB}$ ab und die Sprachbrücke öffnet verzögerungsfrei ($< 5\,\text{ms}$).

### 4.7 Finaler Gehäuseverschluss vor dem Gang in die Garage
Erst wenn im PWA-Dashboard alle 4 Checks grün leuchten und Audio- sowie Funkbrücken stehen:
1. **Dichtungsprüfung:** Silikon-Profildichtungen (Ø 1,5 mm Rundschnur) in die Deckelnuten von Zentralbox, Front-Knoten und Pods einlegen und hauchdünn mit dielektrischem Silikonfett benetzen.
2. **Schrauben anziehen:** Deckel aufsetzen und M3-Schrauben über Kreuz festziehen (greifen vibrationssicher in die unverlierbaren Sechskantmuttern an der Gehäuseunterseite).
3. **Ports versiegeln:** TPU-Staubschutzkappen in ungenutzte Buchsen einsetzen.
4. **Ergebnis:** Das Gesamtsystem ist zu 100 % funktionsgeprüft, wasserdicht versiegelt (IP67) und bereit für die mechanische Montage am Motorrad!

---

## 5. Fahrzeugspezifische Montage & Verkabelung am Motorrad

### Schritt 5.1: Montage Harley-Davidson Plattform (Touring, CVO ST, Limited, Road King & Cruiser mit Saddlebags)

```text
                       OPENMOTORBRIDGE HARLEY-DAVIDSON MOUNTING SUITE
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. GEMEINSAME BASIS (TOURING- & SOFTAIL CRUISER-PLATTFORM IDENTISCH)                   │
│ • Zentralbox: Unter der Sitzbank auf der Rahmenbrücke auf 4x M4 Silentblöcken montiert │
│ • Pod 1 & 2: Kofferdeckel-Docks (saddlebag_lid_dock.stl) auf Serien-Hartschalen- oder  │
│   Heritage-Formkoffern (auch Sport Glide & Low Rider ST Clamshell-Koffer!)             │
│ • Radar: Entkoppelter Kennzeichen-Radarhalter (radar_license_plate_bracket.stl)        │
│   unter dem serienmäßig zentrischen Kennzeichenrahmen (auch bei CVO ST identisch!)     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. COCKPIT & FRONT-NODE MONTAGE (DREI MODULARE VERKLEIDUNGS-OPTIONEN)                  │
│ • Option A (Batwing): Street Glide / Ultra / Electra Glide (2024+ vs. 2014–2023)       │
│ • Option B (Sharknose): Road Glide / CVO ST / Performance Bagger (2024+ vs. 2015–2023) │
│ • Option C (Nacelle & Cruiser): Road King (RK/RKS) sowie Softail Cruiser mit Koffern   │
│   (Heritage Classic FLHCS, Low Rider ST FXLRST, Sport Glide FLSB, Fat Boy mit Bags):   │
│   -> Keine Fairing-Headunit: Front-Node sitzt in Scheinwerfergondel / Mini-Fairing;    │
│      CAN-Bus wird direkt an Zentralbox unter Sitzbank/Seitendeckel abgegriffen (100% Funk!) │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 3. HECK-MONTAGE POD 3 (VIER FAHRZEUGSPEZIFISCHE VARIANTEN)                             │
│ • Bagger / Cruiser: Fender-Konsole (pod3_touring_fender_console.stl) an 1/4"-20 Mutter │
│ • Limited / Ultra: King Tour-Pak Stahlrohrrahmen blockiert Fender! Pod 3 wird per      │
│   Rohrschellen (adventure_pannier_rack_clamp_base.stl) am Tour-Pak-Träger montiert     │
│ • CVO ST / Performance: Under-Cowl Skeleton Dock (cvo_st_undercowl_skeleton_dock.stl) │
│   unter Forged-Carbon Solositz-Hutze mit vollem Freigang zu Showa-Ausgleichsbehältern  │
│ • Custom / Bobber: Zentrische Underfender-Platte (radar_center_underfender_mount.stl)  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 5.1.1 Gemeinsame System-Basis (alle Modelle)
* **Zentralbox:** Unter der Fahrersitzbank auf der massiven Rahmenbrücke vor der Batterie auf 4x M4 Silentblöcken (EPDM Shore 50A) verschrauben. Bei Softail-Modellen sitzt die Zentralbox im Hohlraum unter der Sitzbank oder im seitlichen Rahmendreieck. Die Kabelpeitsche des HD26-Steckers führt nach hinten links und rechts zu den M8 Trennstellen der Koffer sowie zum BCM / Diagnosestecker.
* **Pod 1 & Pod 2 (Satelliten auf Kofferdeckel):** Die Kofferdeckel-Docks ([`saddlebag_lid_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/saddlebag_lid_dock.stl)) mit M4 Senkkopfschrauben und rückseitigen EPDM-Dichtscheiben an den Befestigungspunkten oder per 3M VHB Tape auf den Koffern montieren. *(Hinweis: Neben Street Glide, Road Glide, CVO ST, Road King und Ultra Limited verfügen auch die Cruiser mit Saddlebags wie Low Rider ST und Sport Glide über feste Clamshell-Koffer sowie die Heritage Classic über formstabile Leder-/Vinylkoffer mit flachem Deckel – alle nutzen dieselben Kofferdeckel-Docks [`saddlebag_lid_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/saddlebag_lid_dock.stl)!)*
* **Stationäres MagSafe-Rahmendock & Werkstattsichere Koffer-Abreißkupplung:**
  * **Stationäres Rahmendock am Motorrad montieren ([`009_magsafe_frame_dock.scad`](file:///Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/parts/009_magsafe_frame_dock.scad)):**
    - Das Gehäuseoberteil ([`009_magsafe_frame_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/009_magsafe_frame_dock.stl)) mit seiner integrierten Ø 26 mm Rohrwiege unter dem Sitzüberhang am Rahmenrohr ansetzen (passend für alle Harley Touring- und Softail-Rahmenrohre mit $\varnothing 25{,}4\dots 28{,}6\,\text{mm}$).
    - Den Rohrschellen-Bügel ([`009_magsafe_frame_clamp.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/009_magsafe_frame_clamp.stl)) auflegen und mit 4x M3 Schrauben und DIN 934 Muttern über Kreuz anziehen ($2{,}2\,\text{Nm}$).
    - Die vorkonfektionierte Baugruppe aus M8-PUR-Zuleitung (von der Zentralbox), PCBA 06 Schutzplatine (mit 500mA PPTC-Sicherung & TVS-Dioden) und dem 6-Pin IP67 MagSafe-Magnetpuck spannungsfrei von oben in das Gehäuseunterteil ([`009_magsafe_frame_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/009_magsafe_frame_lid.stl)) einlegen.
    - Ober- und Untergehäuse zusammenfügen und mit der zentralen **M2.5 x 12 mm Edelstahlschraube (DIN 912)** durch die Zentralbohrung der PCBA 06 fest verschrauben. Das Dock baut mit nur $16\,\text{mm}$ Breite extrem schlank und verschwindet vollkommen im Rohrschatten.
  * **Kofferboden-Durchführung & 2-Stufen-Zugentlastung ([`010_saddlebag_hole_grommet_split.scad`](file:///Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/parts/010_saddlebag_hole_grommet_split.scad)):**
    - Die geteilte TPU-Dichtung in das serienmäßige $19\,\text{mm}$-Bodenloch des Koffers einsetzen.
    - Das schlanke Koffer-Innenkabel mit der Gegen-MagSafe-Magnetkupplung durchführen und am angeformten Klemmturm per Kabelbinder fixieren (**Stufe 1 Zugentlastung:** Nimmt alle magnetischen Trennkräfte von $10\dots 15\,\text{N}$ auf).
    - Das Flachkabel lastfrei parallel zum textilen Deckel-Fangband in den Kofferdeckel führen, im Schnauz des Kofferdeckel-Docks formschlüssig abfangen (**Stufe 2 Zugentlastung**) und direkt in den Slim-Port B des Pods einstecken.
    - **Werkstatt-Vorteil:** Mechaniker heben die Koffer für Inspektion oder Reifenwechsel ohne Werkzeug einfach ab – die Magnetkupplung trennt sich zerstörungsfrei und schnappt beim Aufsetzen des Koffers automatisch zentriert wieder ein (*Klack*).
* **Radar:** Der Kennzeichen-Radarhalter ([`radar_license_plate_bracket.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_license_plate_bracket.stl)) wird direkt unter dem Kennzeichenrahmen verschraubt. *(Hinweis: Alle Touring-, CVO ST- und Softail-Cruiser-Modelle besitzen standardmäßig mittige US/EU-Kennzeichenaufnahmen).*

#### 5.1.2 Cockpit-Verkleidung & Front-Node Installation
* **Option A: Batwing-Verkleidung (Street Glide / Electra Glide / Ultra):**
  * **Aktuelle Generation (2024+ All-New Street Glide mit 12.3" Skyline OS):**
    1. Die **2x Torx T25 Schrauben** der Windschutzscheibe oben lösen und Scheibe nach oben herausnehmen (kein 3-Schrauben-System mehr!).
    2. Die beiden seitlichen Lautsprechergitter / Zierblenden vorsichtig mit einem Kunststoff-Demontagekeil nach vorn aus ihren Rasthaken ausclipsen.
    3. Die **2x T25 Schrauben** an der Oberkante unter der Scheibe und die **2x T25/T27 Schrauben** an den seitlichen Flanken (hinter den Lautsprechergittern) lösen.
    4. Die Verkleidung nach vorne von den Zentrierstiften abziehen und den zentralen Multi-Pin-Kompaktstecker des Hauptkabelbaums entriegeln.
  * **Letzte Generation (2014–2023 Rushmore / Boom! Box GTS / 6.5GT):**
    1. Die **3x Torx T27 Schrauben** der Windschutzscheibe entfernen (mittlere Schraube zuletzt halten, um Scheibe vor dem Herabfallen zu schützen).
    2. Die **4x Torx T27 Schrauben** an der Innenseite (Inner Fairing) lösen: 2x oben unter den Zusatzinstrumenten, 2x unten neben den Lautsprechergehäusen.
    3. Outer Fairing nach vorn klappen, H4/LED-Scheinwerfer- und Blinkerstecker trennen.
  * **Verkabelung in der Batwing-Verkleidung:**
    * Front-Node am Lenkerriser / Verkleidungsträger vibrationsfest mit 3M Dual-Lock oder AMPS-Halterung montieren.
    * **12V Strom (`J1`):** 2-Pin JST-PH Kabel an die interne 12V Zubehörbuchse (P&A Accessory) oder Standlichtleitung anklemmen.
    * **CAN-Bus (`J2`):** 3-Pin JST-PH Kabel anstecken. Bei Rushmore (2014–2023) an den 4-poligen P&A Audio-CAN-Stecker hinter der Boom! Box einpinnen. Bei 2024+ Modellen direkt am Skyline OS Display-Kabelbaum anschließen.
    * **Externer Wireless CarPlay / Android Auto Dongle (z. B. Ottocast U2Air Pro / CarlinKit 5.0):**
      * Port `J4` (USB Host Upstream): Mit dem OEM-USB-Medienkabel des Motorrads (Boom! Box / Skyline OS) verbinden.
      * Port `J6` (USB Downstream 2): Mit kurzem USB-Pigtail an den externen Wireless-Dongle anschließen. Der Dongle wird im Fach fixiert. Bei Verbindungsverlust kann die OpenMotorBridge Firmware per 1-Click-Hardreset die 5V VBUS-Spannung über den integrierten TPS2051B Lastschalter für 2,5 s trennen und den Dongle neu starten.
    * **Smartphone Fast-Charging (`J5`):** 20W PD Ladekabel ins Handschuhfach oder an die Lenkerhalterung führen.
    * Fairing wieder aufsetzen und Schrauben mit $3{,}8\,\text{Nm}$ anziehen.

* **Option B: Sharknose-Verkleidung (Road Glide, Road Glide ST, CVO Road Glide ST):**
  * **Aktuelle Generation (2024+ New Road Glide & CVO ST mit 12.3" Skyline OS):**
    1. Die LED-Blinker sind integral in die Verkleidungskanten integriert – es müssen **keine Blinkertürme** mehr von der Gabel abgeschraubt werden!
    2. Die **4x Torx T25 Schrauben** der Scheibe lösen und Scheibe abnehmen.
    3. In den beiden inneren Verkleidungsfächern je **1x T27 Schraube** lösen (insgesamt 2x T27).
    4. An den unteren Verkleidungshaltelaschen neben dem Sturzbügel **2x T25 Schrauben** herausdrehen.
    5. Verkleidung nach vorne oben aus den Fanghaken heben und den Hauptstecker trennen.
  * **Letzte Generation (2015–2023 Rushmore Road Glide / ST):**
    1. Instrumentenabdeckung (Gauge Nacelle) nach oben ausclipsen.
    2. Blinker links und rechts abschrauben (je 2x 1/2" Sechskantschrauben pro Seite).
    3. Die **4x Torx T27 Schrauben** an der Innenseite (neben Lautsprechern/Luftkanälen) herausdrehen.
    4. Sharknose nach vorn aushängen und Multistecker trennen.
  * **Verkabelung:** Identisch zu Option A (Media-Fach / Riser-Montage, `J1` 12V, `J2` CAN-Bus, `J4` Upstream zum Display, `J6` Ottocast-Dongle, `J5` 20W PD-Ladekabel).

* **Option C: Scheinwerfergondel & Softail Cruiser mit Saddlebags (Road King / RKS, Heritage Classic, Low Rider ST, Sport Glide):**
  * **Konzept-Gleichheit (Cruiser mit Saddlebags = Road King Architektur):**
    - Alle Harley-Davidson Cruiser mit Koffern (ob Touring Road King FLHR/FLHRXS oder Softail-Cruiser wie Heritage Classic FLHC/FLHCS, Sport Glide FLSB und Low Rider ST FXLRST) teilen sich dieselbe Architektur:
      - Sie haben **keine große Infotainment-Headunit** (Boom! Box GTS oder 12.3" Skyline OS) im Cockpit.
      - Sie besitzen **Saddlebags** (Hartschalenkoffer bei RKS, feste Clamshells bei Sport Glide und Low Rider ST, formstabile Koffer bei Heritage).
      - Die Bordelektronik und der CAN-Bus (HD-LAN mit 250 bzw. 500 kbps) sind unter der Sitzbank bzw. hinter dem linken Seitendeckel am BCM (Body Control Module) und Diagnosestecker direkt zugänglich.
  * **CAN-Bus Architektur (Abgriff an der Zentralbox unter der Sitzbank / Seitendeckel):**
    - Da im Cockpit kein P&A-Audio-CAN-Bus existiert, wird der CAN-Bus **direkt an der Zentralbox unter der Sitzbank bzw. am BCM/Diagnosestecker** angeschlossen.
      - *Pre-2021 Modelle:* 6-poliger roter Deutsch-Diagnosestecker.
      - *Ab 2021 (Euro 5 / Euro 5+):* 16-poliger Standard-OBD2-Stecker.
      - Der HD26-Kabelbaum greift den CAN-Bus über die Pins 17 (`CAN_H`) und 18 (`CAN_L`) direkt am BCM ab. Sämtliche Fahrdaten (Geschwindigkeit, Drehzahl, Motortemperatur, Blinker, Bremsstatus, Ganganzeige) stehen bereit.
      - **100 % Funkbrücke zur Front:** Der Front-Node benötigt **KEINERLEI CAN-KABEL** an `J2` (Port wird automatisch deaktiviert). Er kommuniziert komplett kabellos über 2,4 GHz ESP-NOW (< 1,8 ms) mit der Zentralbox. Es muss **kein einziges Kabel durch den Lenkkopf oder unter dem Tank hindurch** gezogen werden!
  * **Cockpit- & Verkleidungsmontage des Front-Nodes:**
    - *Road King / Heritage Classic / Fat Boy:* Klemmschraube des 7"-Scheinwerfer-Zierrings lösen, Daymaker herausnehmen. Front-Node sitzt schwingungsentkoppelt im Hohlraum der Aluminium-Scheinwerfergondel hinter dem Reflektor.
    - *Low Rider ST / Sport Glide:* Front-Node hinter der FXRT-/Mini-Batwing-Verkleidung oder an der Lenkerbrücke / Riser verschrauben.
    - **Front-Verkabelung:** Port `J1` (12V KL15 & GND) wird direkt am Standlicht oder Zubehörstecker in der Front angeschlossen. Optional werden Lenker-PTT an `J3`, Totwinkel-LEDs an `J9` und Smartphone Qi-Power an `J5`/`J10` angeschlossen.

#### 5.1.3 Modulare Heck-Montage (Pod 3)
* **Variante 1: Standard Bagger & Softail Cruiser (Street Glide, Road Glide, Road King, Heritage Classic, Low Rider ST, Sport Glide):**
  - Die flache Fender-Konsole ([`pod3_touring_fender_console.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod3_touring_fender_console.stl)) wird zentrisch auf dem Kotflügel an der $1/4"-20$ Soziussitz-Mutter verschraubt. *(Hinweis: Softail- und Touring-Heckfender nutzen dasselbe genormte 1/4"-20 Gewinde).*
* **Variante 2: Touring Limited & Ultra (Ultra Limited FLHTK, Road Glide Limited FLTRK, CVO Limited):**
  - *Wichtige Einschränkung:* Bei allen Modellen mit werkseitig fest verbautem King Tour-Pak stützt sich der massive Stahlrohr-Trägerrahmen direkt über dem Kotflügel ab. Die Fender-Konsole (`pod3_touring_fender_console.stl`) kann bauartbedingt *nicht* montiert werden!
  - *Lösung:* Pod 3 wird stattdessen mit dem formschlüssigen Rohrträger-Klemmschellen-Paar ([`adventure_pannier_rack_clamp_base.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_pannier_rack_clamp_base.stl) / `cap.stl`) direkt am Ø 18 mm Stahlrohrrahmen des Tour-Paks oder unter der Gepäckträger-Brücke montiert.
* **Variante 3: CVO ST / Performance Bagger:**
  - Pod 3 wird im aufrechten Bionic Skeleton Dock ([`cvo_st_undercowl_skeleton_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/cvo_st_undercowl_skeleton_dock.stl)) unsichtbar unter der Forged-Carbon-Einzelsitzhutze montiert (voller Freigang zu den Showa-Ausgleichsbehältern). Die aerodynamische Telemetrie-Finne ([`cvo_st_telemetry_fin.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/cvo_st_telemetry_fin.stl)) wird oben auf der Heck-Hutze verschraubt.
* **Variante 4: Custom-Bikes & Bobber mit seitlichem Kennzeichen:**
  - Bei Umbauten mit seitlich versetztem Kennzeichenhalter wird die zentrische Underfender-Platte ([`radar_center_underfender_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_center_underfender_mount.stl)) mittig unter der Heckfender-Rundung montiert, um eine freie 140°-Sicht des Radars nach hinten zu gewährleisten.

---

### Schritt 5.2: Montage Adventure- & Reiseenduro-Plattform (BMW GS / GSA Familie, KTM, Africa Twin, Universal)

Die Adventure-Montage ist für die gesamte **BMW GS Modellfamilie** (Boxer und Paralleltwins aller Modelljahre) sowie vergleichbare Reiseenduros standardisiert:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        BMW GS MODELL- & PLATTFORM-ZUORDNUNG                            │
├───────────────────────────────────┬────────────────────────────────────────────────────┤
│ Modellreihe                       │ Besonderheiten & Anschlussspezifika                │
├───────────────────────────────────┼────────────────────────────────────────────────────┤
│ • R 1250 GS / R 1300 GS           │ 6.5" TFT Connectivity, Wonder Wheel, 16-Pin OBD2,  │
│   F 750 GS / F 850 GS / F 900 GS  │ Cartool im Cockpit, Vario-Aufnahmen (Option A)     │
├───────────────────────────────────┼────────────────────────────────────────────────────┤
│ • R 1250 GSA / R 1300 GSA         │ 6.5" TFT Connectivity, Wonder Wheel, 16-Pin OBD2,  │
│   F 850 GSA / F 900 GSA           │ Cartool im Cockpit, Ø 18 mm Edelstahlrohr (Opt. B) │
├───────────────────────────────────┼────────────────────────────────────────────────────┤
│ • R 1200 GS LC / GSA LC           │ Wonder Wheel, Cartool vorhanden. Diagnosestecker:  │
│   (K50/K51, 2013–2018)            │ 2013–2016 rund 10-Pin, ab 2017 rechteckig 16-Pin   │
├───────────────────────────────────┼────────────────────────────────────────────────────┤
│ • Klassische R 1200 GS / GSA (K25)│ Analog/LCD Cockpit, Cartool am Lenkkopf vorhanden. │
│   & F 650 / 700 / 800 GS (K70/72) │ Runder 10-Pin Diagnosestecker unter Sitzbank.      │
│   (luft-/ölgekühlt, bis 2012/2018)│ Steuerung via OMB BLE-Lenkertaster (kein Wonderwh.)│
│                                   │ GSA-Rohrträger: Exakt identischer Ø 18 mm Träger!  │
└───────────────────────────────────┴────────────────────────────────────────────────────┘
```

```text
                             OPENMOTORBRIDGE ADVENTURE-KIT MOUNTING SUITE
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. GEMEINSAME BASIS (FÜR ALLE REISEENDUROS IDENTISCH)                                   │
│ • Zentralbox: Unter der Fahrersitzbank im Heckrahmen vibrationsgedämpft montiert       │
│ • Cockpit & Front-Node: Am Ø 12 mm GPS/Navi-Bügel über TFT / Windschild befestigt     │
│   (12V Cartool-Strom, drahtlose 2.4 GHz Funkbrücke zur Zentralbox, keine Lenkkopfwand) │
│ • Heck-Pod 3: Auf Rack-Tail Mount (adventure_rack_tail_mount.stl) an Gepäckbrücke     │
│ • Radar Varia Dock: Am 36-Zahn Hirth-Gelenk im 10°-Raster diebstahlgeschützt montiert  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. MODULARE POD 1 & 2 KOFFERTRÄGER-BEFESTIGUNG (ZWEI OPTIONEN)                         │
│ • Option A (Vario-Koffer / Rahmenmontage - BMW GS Standard, KTM ohne Rohrträger):      │
│   Transition-Dock (adventure_transition_dock.stl) in der Sitzbank-Bügelfalte (Ø 28 mm) │
│   -> 100 % kofferunabhängig, baut nicht breiter als die schlanke Fahrzeug-Silhouette   │
│ • Option B (Edelstahl-Rohrkofferträger - BMW GSA, Touratech, Hepco&Becker, Alukoffer): │
│   GSA Heavy-Duty Cage Dock (adventure_gsa_cage_dock_body.stl + clamp_cap.stl)          │
│   -> Montiert Pod 1 & 2 im 45 mm Totraum hinter dem Träger (100 % verdeckt & geschützt)│
└────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 5.2.1 Gemeinsame System-Basis
* **Zentralbox:** Im Rahmendreieck unter der Fahrersitzbank auf 4x M4 Silentblöcken montieren. M8 Kabelpeitschen nach hinten links/rechts und zum Heck führen.
* **Cockpit & Front-Node:**
  * 4x Torx T25 Schrauben der Windschild-Befestigung lösen und Scheibe abnehmen.
  * Obere TFT-Cockpitblende nach vorne ausclipsen (bei K25/F800: Instrumentenabdeckung lösen).
  * Front-Node mit AMPS-Halterung oder Rohrschelle an der Ø 12 mm GPS-Querstrebe bzw. am Lenker fixieren.
  * **Stromversorgung & CAN-Bus Anbindung (2 Optionen):**
    * **Stromversorgung:** 2-Pin JST-PH Kabel an `J1` direkt am originalen BMW Cartool-Navistecker (SZ-Stecker im Cockpit/Lenkkopf: Pin 1 Masse, Pin 3 +12V geschaltet KL15) anstecken.
    * **CAN-Bus Option 1 (Empfohlen – Plug & Play unter Sitzbank):** Der CAN-Bus wird an der Zentralbox über den HD26-Kabelbaum (Pins 17 `CAN_H` und 18 `CAN_L`) abgegriffen:
      * *Modelle ab 2017 (Euro 4 / Euro 5 / Euro 5+):* Direkt am 16-poligen Standard-OBD2-Stecker bzw. RDC/DWA-Stecker (analog zu Hex ezCAN / WunderLINQ).
      * *Klassische Modelle bis 2016 (Euro 3, K25 / K72 / frühe K50):* Über ein handelsübliches 10-Pin-Rundstecker-auf-OBD2-Adapterkabel (ICOM-Adapter).
      * Port `J2` am Front-Knoten bleibt frei und wird automatisch deaktiviert. Keinerlei Kabelbeschädigung im Cockpit!
    * **CAN-Bus Option 2 (Cockpit-Abgriff am 12-Pin TFT – nur Modelle mit TFT):** Das BMW 6,5" TFT-Display führt auf seiner Rückseite an Pin 2 (`CAN_H`, weiß/schwarz) und Pin 3 (`CAN_L`, weiß/braun) K-CAN. Wer ein 12-Pin Y-Adapterkabel nutzt, kann diesen direkt an `J2` des Front-Knotens anschließen. Der Front-Knoten streamt Drehzahl, Tacho und Wonder-Wheel dann drahtlos via ESP-NOW zur Zentralbox.
* **Pod 3 & Radar (Rallye-Aero-Balkon Montage):**
  * Basis-Wanne ([`adventure_rack_tail_mount_base.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_rack_tail_mount_base.stl)) mit 2x M6 Schrauben und Halbschellen am Ø 18 mm Gepäckbrückenrohr oder an den M6-Punkten der Trägerplatte befestigen.
  * M8-PUR-Kabel durch die untere Kabelrinne führen und von oben an Port A des Pod 3 anschließen. Pod 3 in die Wanne einlegen.
  * Karosserie-Deckel ([`adventure_rack_tail_cowl.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_rack_tail_cowl.stl)) aufsetzen (2.4-GHz-Dipolantenne in die Shark-Finne einrasten) und mit 4x M3 Torx-Schrauben bündig verschrauben.
  * Zunge des Garmin Varia Docks ([`radar_varia_gopro_lock_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_varia_gopro_lock_dock.stl)) in die bionische Hirth-Rosette des Unterseiten-Pylons einrasten ($10^\circ$-Schritte für exakt waagerechten Radar-Horizont). Mit M5 x 25 mm Schraube und Stoppmutter sichern ($3{,}5\,\text{Nm}$). Varia einklinken und M3 Madenschraube als Diebstahlschutz eindrehen.

#### 5.2.2 Modulare Koffer- & Pod 1/2-Befestigung
* **Option A: Vario-Koffer & Rahmenrohr-Montage (BMW GS Standard R1200/R1250/R1300, F750/F850/F900, KTM / Enduro ohne Rohrträger):**
  * Die Unter-Sitzbank-Sattelbrücke ([`adventure_underseat_cross_rail.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_underseat_cross_rail.stl)) unter der Sitzbank flach auf den Rahmensteg auflegen und an vorhandenen OEM-Punkten (M5/M6) verschrauben.
  * Die Transition-Dock Basis-Wannen ([`adventure_transition_dock_base.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_transition_dock_base.stl)) an den Ø 28 mm Heckrahmenrohren in der Bügelfalte ansetzen und über die inneren Zungen mit je 2x M4-Schrauben fest mit der Sattelbrücke verschrauben (100 % verdrehsicheres U-Portal).
  * **Kabelführung & Anschluss (Top-Access):**
    * Das M8-PUR-Kabel von der Zentralbox aus dem Batterietrog unter dem Sitzbankschaumstoff durchschieben.
    * Das Kabel tritt durch die fahrzeuginnere ovale Öffnung (Ø 10 mm) direkt in die vordere Stecker- und Service-Bucht der Transition-Dock-Basis ein.
    * Bei noch abgenommenem Karosserie-Deckel wird das M8-Kabel bequem von oben auf Port A des Pods gesteckt und handfest angezogen.
    * Den Pod in die Wanne absenken (der Stecker und die Kabelschlaufe betten sich spannungsfrei in der 24-mm-Nasenbucht).
  * Karosserie-Deckel ([`adventure_transition_dock_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_transition_dock_lid.stl)) aufsetzen und mit 4x M3 Torx-Schrauben bündig verschrauben.
  * **100 % kofferunabhängig & Clean Look:** Keine sichtbaren Schellen oder Kabel von außen; die Konsole schmiegt sich aerodynamisch an die Bügelfalte an.
* **Option B: Edelstahl-Rohrkofferträger (BMW GSA aller Baujahre inkl. K25 & F800 GSA, Touratech, Hepco&Becker, Alukoffer):**
  * 1,0 mm EPDM-Schutzstreifen um das Ø 18 mm Kofferträgerrohr an der Innenseite wickeln.
  * Das **GSA Cage Dock** ([`adventure_gsa_cage_dock_body.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_gsa_cage_dock_body.stl)) mit seinen zwei Rohrsätteln am Rohr ansetzen. Die Klemmschellen-Kappe ([`adventure_gsa_clamp_cap.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_gsa_clamp_cap.stl)) auflegen und mit 4x M5 x 25 mm V4A Zylinderschrauben und DIN 985 Stoppmuttern über Kreuz mit $4{,}5\,\text{Nm}$ anziehen (85 mm Stützbasis verhindert jedes Verdrehen oder Kippen).
  * Pod 1 bzw. 2 in die gepanzerte Schutznische einschieben. Der Pod sitzt zu 80 % tief versenkt im $45\,\text{mm}$ breiten Totraum zwischen Trägerrohr und Radkasten.
  * Das M8-PUR-Kabel verläuft verdeckt in der M8-Kabelrinne im Rohrschatten direkt ins Batteriefach.
  * **Ergebnis:** Bei eingehängtem Alukoffer ist der Pod von außen 100 % unsichtbar. Radseitig schützt der $45^\circ$-Gleitkeil vor Steinschlag (Roost) und Schlamm.
  * *(Minimalistische Option:)* Für besonders beengte Rohrrahmenverläufe können alternativ die einfachen 2x M5 Halbschellen ([`adventure_pannier_rack_clamp_base.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_pannier_rack_clamp_base.stl) / `cap.stl`) verwendet werden.

---

### Schritt 5.3: Montage & Anschluss optionaler Cockpit- & Zubehör-Komponenten

Der Universal Front-Knoten (PCBA 05) dient als zentrale Anschlussstelle für das gesamte Fahrer-Cockpit. Folgende optionale Zubehörteile können nach Bedarf per vorkonfektioniertem Plug-and-Play-Kabel angeschlossen werden:

```text
               COCKPIT-ZUBEHÖR & ANSCHLUSSÜBERSICHT (FRONT-KNOTEN PCBA 05)
┌───────────────────────┬─────────┬────────────────────────────────────────────────────────┐
│ Zubehör-Komponente    │ Port    │ Anschluss & Signalbelegung                             │
├───────────────────────┼─────────┼────────────────────────────────────────────────────────┤
│ **Lenker-Bedienung**  │ **CAN** │ CAN-ID 0x290 (Harley TRIP) / 0x2A0 (BMW Wonder Wheel)   │
│ (Cam, PTT & Marker)   │ / **J3**│ oder 4-Pin JST-PH Hardware-Taster (Under-Perch / Klemme)│
├───────────────────────┼─────────┼────────────────────────────────────────────────────────┤
│ **Totwinkel-LEDs**    │ **J9**  │ 3-Pin JST-PH (Pin 1: +12V_PROT, Pin 2: BSD Links,       │
│ (Radar Blind Spot)    │         │ Pin 3: BSD Rechts über N-MOSFET Low-Side Treiber)      │
├───────────────────────┼─────────┼────────────────────────────────────────────────────────┤
│ **Actioncam-Power**   │ **J8**  │ 2-Pin/4-Pin JST-PH (+5.0V / 2.0A, Charge-Only ohne     │
│ (GoPro/Insta360/DJI)  │         │ USB-Daten zur Vermeidung von Headunit-Lockups)         │
├───────────────────────┼─────────┼────────────────────────────────────────────────────────┤
│ **Qi-Ladehalterung**  │ **J10** │ 2-Pin JST-PH (+12V geschaltet über Zündungs-Gate,      │
│ (Quad Lock / SP Conn.)│ / **J5**│ bis 2.0A / 24W) oder 20W USB-C PD Fast Charging an J5  │
├───────────────────────┼─────────┼────────────────────────────────────────────────────────┤
│ **Zusatzscheinwerfer**│ **J11** │ 2-Pin JST-PH (+12V High-Side Switch bis 3.5A / 40W,    │
│ (Notbrems-Stroboskop) │         │ automatischer 4–5 Hz Warnblitz bei Notbremsung > 0.8g) │
└───────────────────────┴─────────┴────────────────────────────────────────────────────────┘
```

#### 5.3.1 Lenker-Bedieneinheit: Dual-Input Architektur (OEM CAN-Bus & Dedizierter Hardware-Taster `J3`)

OpenMotorBridge implementiert eine flexible **Dual-Input-Architektur** für die Lenkerbedienung. Beide Signalquellen speisen dieselbe interne Zustandsmaschine im Front-Node und können wahlweise autark oder parallel betrieben werden:

##### Option A: OEM CAN-Bus Daumen-Integration (Empfohlen – 0 mm Lenker-Platzbedarf)
* **Mechanischer Platzbedarf:** **0 mm** – keine zusätzliche Klemmschelle am Lenkerrohr. Die obere Klemmschelle der Kupplungsarmatur bleibt vollkommen frei für die Steuereinheit eines Klappenauspuffs (z. B. Dr. Jekill & Mr. Hyde oder KessTech).
* **Fahrergonomie bei 2-Finger-Hebelüberdeckung:** Zeige- und Mittelfinger verbleiben unterbrechungsfrei auf dem Kupplungshebel. Der linke Daumen steuert die Funktionen ermüdungsfrei über die serienmäßige **TRIP-Taste** am oberen Armaturengehäuse (Harley-Davidson HD-LAN CAN-ID `0x290`, Bit 20) bzw. den Multicontroller / Wonder Wheel (BMW K-CAN):
* **„Cam-First“ Gestensteuerung während der Fahrt ($v > 0$):**
  - **Kurzer Klick ($< 300\,\text{ms}$):** Action-Cam REC Start / Stopp. Weckt GoPro (Hero 9–13 via Open GoPro BLE `0xFEA6`), Insta360 (X3/X4 via Smart Remote BLE) oder DJI Action verzögerungsfrei aus dem Ruhezustand auf. Ein heller Bestätigungs-Doppelton (*„Ding-Ding“*) bzw. Tiefton (*„Dong“*) im Helm-Headset bestätigt den Aufnahmestatus ohne Blickabwendung.
  - **Gedrückt halten ($> 300\,\text{ms}$):** Push-to-Talk (PTT) für Intercom-Mesh / Funk. Solange der Taster gehalten wird, ist der Sprachkanal offen; beim Loslassen schließt er verzögerungsfrei (klassisches Walkie-Talkie-Prinzip).
  - **Doppelklick:** Setzt einen Video-Highlight-Marker (HiLight-Tag) in der Videoaufzeichnung und der GPX-Telemetrie zur schnellen Auffindung von Schlüsselstellen im späteren Videoschnitt.
  - *(Hinweis zum Bordcomputer: Bei kurzem Klick im Stand $v = 0$ sowie während der Fahrt wechselt der originale Harley-Tacho wie gewohnt durch Trip A, Trip B, Uhrzeit und Restreichweite. Ein Trip-Reset erfolgt auf der Harley weiterhin nur durch langes Halten im Stillstand).*

##### Option B: Dedizierter taktiler Hardware-Taster (Port `J3` am Front-Node)
* **Einsatzbereich:** Für Fahrzeuge ohne CAN-Bus-Zugriff am Lenker oder Fahrer, die einen separaten physischen Taster mit spürbarem mechanischem Klick bevorzugen.
* **Mechanische Montage – Zwei kollisionsfreie Varianten:**
  1. **Under-Perch / Spiegelfuß-Halter (Empfohlen für Cruiser):**
     - Gedruckt aus MJF PA12-CF / ASA: [`under_perch_switch_bracket.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/under_perch_switch_bracket.stl) (für M4 Armaturschraube) bzw. mit Adapterplatte [`under_perch_mirror_plate.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/under_perch_mirror_plate.stl) (für M8/M10 Spiegelschaft).
     - Der Mikrotaster sitzt ca. 15 mm **unterhalb** des Blinkerschalters – vollkommen kollisionsfrei unterhalb einer eventuell montierten Jekill & Hyde Klappensteuerung und ergonomisch im natürlichen Absenkbereich des Daumens.
  2. **Schlanke Rohrklemmschelle (10 mm):** Montage eines schmalen Tasters (z. B. Daytona Slimline oder motogadget m-switch mini) unmittelbar am Innenflansch des linken Griffgummis.
* **Elektrischer Anschluss an Port `J3` (4-Pin JST-PH):**
  - **Pin 1:** `GND` (Gemeinsamer Massebezug)
  - **Pin 2:** `PTT_INTERCOM` (Schließt gegen Masse: Tastet sofort das Intercom-Mesh / Funknetzwerk oder führt bei 2-Pin-Taster die obige Gestensteuerung aus)
  - **Pin 3:** `CAM_ACTION` (Schließt gegen Masse: Separater Actioncam Start/Stopp & Highlight Taster bei 3-fach Clustern)
  - **Pin 4:** `MEDIA_VOICE` (Schließt gegen Masse: Sprachassistent Siri/Google Assistant oder nächster Musiktitel)
  - *(Hinweis: Ein handelsüblicher 2-Pin PTT-Taster passt direkt auf Pin 1 und Pin 2).*
* **Systemvorteil:** 100 % batteriefrei, keine Verzögerung durch Funk-Latenz (< 1,8 ms Reaktionszeit), hardwareseitig über Schmitt-Trigger entprellt und gegen 12V-Überspannung geschützt.

#### 5.3.2 Totwinkel-Spiegelanzeigen (Radar Blind Spot Detection - BSD) (`J9`)
* **Mechanische Montage (Aerodynamisches 2-Schalen Mirror-Pod):**
  - Montage am linken und rechten Spiegelschaft (Ø 10 mm / Ø 12 mm) mittels 2-teiliger Klemmschelle:
    - Oberschale mit 38° Lichttunnel und 3,8 mm Blendschutzvisier: [`bsd_mirror_upper_pod.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/bsd_mirror_upper_pod.stl)
    - Unterschale mit M3 Einschmelz- bzw. Sechskantmuttern-Taschen: [`bsd_mirror_lower_clamp.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/bsd_mirror_lower_clamp.stl)
    - Bernstein/Rot-transluzente Diffusorlinse: [`bsd_mirror_lens.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/05_accessories/bsd_mirror_lens.stl)
  - **100 % StVZO- und ECE-R50-konform:** Durch die opake Vorwand und das 3,8 mm Schutzdach wird jegliche Vorwärts- und Seitenabstrahlung verhindert – der Gegenverkehr wird niemals geblendet, während das Signal im Fahrer-Blickfeld unübersehbar leuchtet.
* **Elektrischer Anschluss an Port `J9` (3-Pin JST-PH):**
  - **Pin 1:** `+12V_PROT` (Geschützte 12V Anoden-Speisung)
  - **Pin 2:** `BSD_LEFT_N` (Kathode linke Spiegel-LED, geschaltet über N-MOSFET Kanal A)
  - **Pin 3:** `BSD_RIGHT_N` (Kathode rechte Spiegel-LED, geschaltet über N-MOSFET Kanal B)
* **Funktionsweise:**
  - Gesteuert über das Heckradar (Garmin Varia oder OMM Radar über die Zentralbox):
    - **Dauerleuchten (Bernstein):** Ein Fahrzeug befindet sich im toten Winkel oder nähert sich auf der jeweiligen Spur.
    - **Schnelles Warnblitzen (8 Hz, Rot/Bernstein):** Akute Kollisionsgefahr (hohe Differenzgeschwindigkeit oder Blinker in Richtung des herannahenden Fahrzeugs gesetzt).
  - *Automatisches Dimmen:* Über den optionalen Umgebungslichtsensor (`OPT3001` an `J12`) werden die LEDs bei Dunkelheit blendfrei heruntergedimmt.

#### 5.3.3 Stromversorgung für Actioncam (GoPro, Insta360, DJI) (`J8`)
* **Mechanische Montage:**
  - Actioncam am Lenker, am Windschild-Träger oder am Sturzbügel befestigen.
* **Elektrischer Anschluss an Port `J8` (JST-PH):**
  - Reine $+5{,}0\,\text{V}$ Speisung (bis zu $2{,}0\,\text{A}$) direkt vom Front-Node.
* **Kritischer Systemvorteil (Charge-Only):**
  - Port `J8` führt **bewusst keine USB-Datenleitungen**. Dadurch wird zuverlässig verhindert, dass die Kamera beim Einschalten der Motorradzündung in den lästigen PC-Massenspeichermodus ("USB verbunden") wechselt oder die Infotainment-Headunit (Boom! Box / Skyline OS) zum Einfrieren bringt.
  - **Automatischer BLE-Shutter-Stop:** Über den integrierten KL15-Pufferkondensator (`C_BUF`) auf der Front-Node Platine bleibt der ESP32-S3 beim Ausschalten der Zündung noch für 1,5 Sekunden aktiv und sendet per Bluetooth LE den "Record Stop"-Befehl an die Kamera – Videodateien werden sauber finalisiert und korrumpieren nicht.

#### 5.3.4 Anschluss Qi-Induktionshalterung (Quad Lock, SP Connect) (`J10` & `J5`)
* **Mechanische Montage:**
  - Quad Lock Handlebar Mount mit wetterfestem Wireless Charging Head oder SP Connect Moto Mount mit Wireless Charging Module.
* **Elektrischer Anschluss – Zwei flexible Optionen:**
  - **Option 1 (Empfohlen: 12V Hardwire an Port `J10`):**
    - 2-Pin JST-PH Stecker: Pin 1 = `+12V_SW`, Pin 2 = `GND`.
    - Dauerlast bis $2{,}0\,\text{A}$ ($24\,\text{W}$).
    - Das Direktanschlusskabel von Quad Lock / SP Connect wird ohne fliegende Sicherungen sauber am Front-Node eingesteckt.
    - **Null Ruhestrom:** Die Speisung wird über das interne Zündungs-Gate des Front-Nodes geschaltet – die Motorradbatterie wird bei Standzeit niemals entladen.
  - **Option 2 (USB-PD Fast-Charging an Port `J5`):**
    - Standard USB-C Kabel von Port `J5` direkt in den Ladekopf.
    - Unterstützt echte 20W USB-PD Schnellladung ($9\,\text{V} / 2{,}2\,\text{A}$, QC 4+ und Apple Fast Charge) – lädt Smartphones auch bei voller Displayhelligkeit und Navigation im Sommer zuverlässig schnell.
* **„Handy vergessen“-Warnung:**
  - Schaltet der Fahrer die Zündung ab und entfernt sich vom Motorrad (Bluetooth-Signal reißt ab), während die Qi-Ladeschale (`J10`) oder USB-Buchse (`J5`) noch eine Last misst, warnt OpenMotorBridge sofort über die Fahrzeughupe oder den LoRa-Pager am Schlüsselbund.

---

## 6. Endabnahme am Motorrad, Probefahrt & Sign-Off Checkliste

Nachdem das System am Motorrad mechanisch befestigt und elektrisch verkabelt ist:

1. **Zündungs-Check (KL15):**
   * Motorrad-Zündung einschalten: Die Zentralbox und der Front-Node erwachen synchron innerhalb von $800\,\text{ms}$.
   * Display / Infotainment (Boom! Box / Skyline OS / TFT) zeigt die OpenMotorBridge Headset-Verbindung und CarPlay/Android Auto Icon.
2. **Totwinkel-Radar-Test (Garmin Varia):**
   * Hinter das Motorrad treten: Die bernsteinfarbenen Spiegel-LEDs (`J9`) leuchten kontinuierlich auf.
   * Blinker setzen: Bei herantretender Person wechselt die entsprechende LED in schnelles Warnblitzen (8 Hz).
3. **Probefahrt & Audio-Ducking:**
   * Motor starten und Probefahrt durchführen: Der SDP31 Staudrucksensor und das Sipeed/Knowles MEMS Fahrtwind-Mikrofon regeln die Lautstärke adaptiv und pegelfest nach.
   * PTT-Taster am Lenker bedienen: Glasklare Funkübertragung zu Mitfahrern und Sozius.
4. **Zündung aus (KL15 Nachlauf & Diebstahlschutz):**
   * Zündung ausschalten: Actioncam stoppt sauber per Bluetooth-Shutter, USV puffert System herunter.
   * Bei unbefugter Fahrzeugbewegung im Stand löst der 6-Achs-Beschleunigungssensor (BMI270) sofort Alarm über den LoRa-Pager am Schlüsselbund aus.

---

## 7. Wartung & Pflege

* **Dichtungsinspektion:** 1x pro Saison die Silikon-Rundschnur der Main Box, des Front-Knotens und der Kassetten dünn mit dielektrischem Silikonfett pflegen.
* **Druckausgleich:** Sicherstellen, dass die ePTFE-Gore-Membranen sauber und frei von Schlamm sind.
* **Firmware-Updates:** Drahtlos und ohne Werkzeug direkt über die WebBLE-PWA-Oberfläche durchführbar.
