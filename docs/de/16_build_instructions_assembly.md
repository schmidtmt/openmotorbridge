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
4. **Dichtung & Deckel:** Silikon-Rundschnur (Ø 1,5 mm, $40\,\text{cm}$) dünn mit Silikonfett einreiben und in die Deckelnut einlegen. Gore-Membran auf den Belüftungssitz kleben. Den Deckel ([`main_box_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lid.stl)) aufsetzen und mit 4x M3 $\times 40\,\text{mm}$ Schrauben über Kreuz handfest festziehen ($0{,}8\,\text{Nm}$).

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

### Schritt 4.1: Montage Adventure-Kit (BMW GS vs. BMW GSA / Enduro)

```text
                             OPENMOTORBRIDGE ADVENTURE-KIT MOUNTING SUITE
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ BMW R1250 / R1300 GS (STANDARD)                                                        │
│ • Transition-Dock (adventure_transition_dock.stl) in der Sitzbank-Bügelfalte (Ø 28 mm) │
│ • 100 % kofferunabhängig – kein Überstand über die Fahrzeugsilhouette                  │
│ • Rack-Tail Mount (adventure_rack_tail_mount.stl) an der Serien-Gepäckbrücke           │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ BMW R1250 / R1300 GSA (ADVENTURE / EDELSTAHL-KOFFERTRÄGER)                             │
│ • Rohrträger-Klemmschellen-Käfig (adventure_pannier_rack_clamp_base.stl + cap.stl)     │
│ • Montiert Pod 1 & 2 geschützt im Rohrrahmen-Dreieck (Ø 18 mm Edelstahlrohr)           │
│ • Heck-Balkon Gepäckbrücken-Ausleger ragt 65 mm hinter Alutopcase hervor               │
│ • 36-Zahn Hirth-Formschluss-Gelenk & Garmin Varia Radar-Dock mit Madenschraube         │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **BMW GS (Standard) Montage:**
   * **Pod 1 & 2:** Die Transition-Docks ([`adventure_transition_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_transition_dock.stl)) unterhalb der Sitzbankkante an die Rahmenrohre (Ø 28 mm) klemmen. Die M8 Zuleitungskabel im Unterflurkanal direkt unter die Sitzbank zur Zentralbox führen.
   * **Pod 3:** Auf dem Rack-Tail Mount ([`adventure_rack_tail_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_rack_tail_mount.stl)) an der Gepäckbrücke verschrauben.
   * **Cockpit & Front-Node Fairing-Demontage:**
     * 4x Torx T25 Schrauben der Windschild-Befestigung lösen und Scheibe abnehmen.
     * Obere TFT-Cockpitblende nach vorne aus den Rastnasen ausclipsen.
     * Front-Node mit AMPS-Verschraubung oder Rohrklemmen am Lenker / Navi-Bügel fixieren.
     * **Keine Kabelverlegung durch den Lenkkopf:** Der Front-Knoten kommuniziert zu 100 % drahtlos über die integrierte 2,4 GHz Funkbrücke (ESP-NOW / BLE, Latenz < 1,8 ms) mit der Zentralbox unter der Sitzbank.
     * Lokale Stromversorgung: Das 2-polige JST-PH Kabel wird direkt am originalen BMW Cartool-Navistecker (oder Standlicht KL15 Zündungsplus & Masse) im Cockpitbereich angesteckt.
2. **BMW GSA (Adventure) Montage:**
   * **Pod 1 & 2:** 1,0 mm EPDM-Schutzstreifen um das Ø 18 mm Kofferträgerrohr wickeln. Unterschale ([`adventure_pannier_rack_clamp_base.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_pannier_rack_clamp_base.stl)) und Kappe ([`adventure_pannier_rack_clamp_cap.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_pannier_rack_clamp_cap.stl)) mit 2x M5 x 30 mm V4A Schrauben und DIN 985 Stoppmuttern über Kreuz mit $4{,}5\,\text{Nm}$ anziehen. Pod-Basisgehäuse an den Augen der Schelle verschrauben.
   * **Pod 3 & Radar:** Ausleger ([`adventure_rack_tail_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/adventure_rack_tail_mount.stl)) an der Gepäckbrücke montieren.
   * **Radar Varia Dock:** Zunge des Garmin Varia Docks ([`radar_varia_gopro_lock_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_varia_gopro_lock_dock.stl)) in die Hirth-Rosette ([`011_gopro_hirth_lock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/011_gopro_hirth_lock.stl)) einrasten ($10^\circ$-Schritte für exakten Radar-Horizont). Mit M5 x 25 mm Schraube und Stoppmutter sichern ($3{,}5\,\text{Nm}$). Varia einklinken und M3 Madenschraube als Diebstahlschutz eindrehen.

---

### Schritt 4.2: Montage Harley-Davidson Kit (Touring vs. CVO ST vs. Custom/Bobber)

```text
                       OPENMOTORBRIDGE HARLEY-DAVIDSON MOUNTING SUITE
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ HARLEY-DAVIDSON TOURING & BAGGER (STREET GLIDE, ROAD GLIDE, ROAD KING)                 │
│ • Kofferdeckel-Docks (saddlebag_lid_dock.stl) auf Hartschalenkoffern (Pod 1 & Pod 2)   │
│ • Touring Fender Console (pod3_touring_fender_console.stl) strömungsgünstig am Fender  │
│ • Kennzeichen-Radarhalter (radar_license_plate_bracket.stl) entkoppelt unter Kennzeichen│
├────────────────────────────────────────────────────────────────────────────────────────┤
│ HARLEY-DAVIDSON CVO ROAD GLIDE ST / PERFORMANCE BAGGER                                 │
│ • Under-Cowl Skeleton Dock (cvo_st_undercowl_skeleton_dock.stl) unter Forged Carbon    │
│   Sitz-Hutze: Voller Freigang zu den Ausgleichsbehältern der Showa-Stoßdämpfer         │
│ • CVO ST Telemetrie-Finne (cvo_st_telemetry_fin.stl) als Haifischflosse am Heck        │
│ • Kennzeichen-Radarhalter (radar_license_plate_bracket.stl): Gleicher Halter wie alle  │
│   Touring-Modelle, da Kennzeichen auch bei der CVO ST serienmäßig mittig montiert ist! │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ CUSTOM-BIKES, BOBBERS & UNIVERSAL (SEITLICHER KENNZEICHENHALTER)                       │
│ • Zentrische Underfender-Platte (radar_center_underfender_mount.stl) mittig unter dem   │
│   Kotflügel montiert für freie Radar-Sicht nach hinten bei seitlichem Kennzeichen      │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **Classic Touring Montage & Fairing-Demontage:**
   * **Pod 1 & 2:** Die Kofferdeckel-Docks ([`saddlebag_lid_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/saddlebag_lid_dock.stl)) mit M4 Senkkopfschrauben und rückseitigen Dichtscheiben an den OEM-Befestigungspunkten oder per 3M VHB Tape auf den Kofferdeckeln montieren. Vorkonfektioniertes M8 Kabel durch die Gummitülle in den Koffer und über Schnellkupplung zum Rahmen führen.
   * **Pod 3:** Die Fender-Konsole ([`pod3_touring_fender_console.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod3_touring_fender_console.stl)) flach auf dem Kotflügel zentrieren und verschrauben.
   * **Radar:** Kennzeichen-Halter ([`radar_license_plate_bracket.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_license_plate_bracket.stl)) unter dem Kennzeichenrahmen verschrauben.
   * **Batwing Fairing-Demontage (Street Glide):**
     * Die 3x Torx T27 Schrauben der Windschutzscheibe entfernen (mittlere Schraube zuletzt).
     * Die 4x Torx T27 Schrauben an der Innenseite der Verkleidung lösen (2x unter den Instrumenten, 2x neben den Lautsprechern).
     * Outer Fairing vorsichtig nach vorne abnehmen, Scheinwerfer-Kompaktstecker trennen.
     * Front-Node am Lenkerriser verschrauben.
     * Lokale Stromversorgung: Das 2-polige JST-PH Stromkabel direkt an der internen Verkleidungs-Zubehörbuchse (oder Standlicht KL15 Zündungsplus) anklemmen. **Kein Kabel nach hinten durch den Tanktunnel erforderlich**, da die Verbindung zur Zentralbox vollkommen drahtlos via ESP-NOW / BLE erfolgt!
     * Outer Fairing wieder ansetzen und T27 Schrauben mit $3{,}8\,\text{Nm}$ anziehen.
2. **CVO ST / Performance Bagger Montage (Road Glide Sharknose):**
   * **Pod 1 & 2:** Das aufrechte Skeleton Dock ([`cvo_st_undercowl_skeleton_dock.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/cvo_st_undercowl_skeleton_dock.stl)) unter der Einzelsitz-Hutze montieren. Die Pods stehen senkrecht und haben vollen Abstand zu den Ausgleichsbehältern der Federbeine.
   * **Pod 3:** Die aerodynamische Telemetrie-Finne ([`cvo_st_telemetry_fin.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/cvo_st_telemetry_fin.stl)) auf der Heck-Hutze montieren.
   * **Radar:** Auch bei der CVO ST kommt der Kennzeichen-Halter ([`radar_license_plate_bracket.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_license_plate_bracket.stl)) zum Einsatz, da das Kennzeichen serienmäßig mittig montiert ist!
   * **Sharknose-Demontage:** Blinkerschrauben lösen, 4x T27 Innenschrauben herausdrehen, Sharknose-Verkleidung nach vorn abheben. Front-Node im Media-Fach / Riser montieren und lokal an die 12V-Zuleitung anstecken.
3. **Custom-Bikes & Bobber mit seitlichem Kennzeichen:**
   * Bei Umbauten mit seitlich versetztem Kennzeichenhalter wird die zentrische Underfender-Platte ([`radar_center_underfender_mount.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/radar_center_underfender_mount.stl)) mittig unter der Heckfender-Rundung verschraubt, um eine unbeeinträchtigte 140°-Erfassung des Radars zu garantieren.

---

## 4. Universal Front-Knoten Aufbau & Montage

### 4.1 Zusammenbau der Front-Node Box (100 % lötfrei)
1. **Muttern einlegen (Nut-Pockets):**
   * 4x DIN 934 / DIN 985 M3 Edelstahlmuttern von unten in die Sechskant-Mutternaschen der Gehäuse-Ecken der Unterwanne ([`front_node_lower_tub.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_lower_tub.stl)) eindrücken.
   * 4x DIN 934 M4 Muttern in die Sechskant-Taschen des AMPS-Lochbilds ($30 \times 38\,\text{mm}$) am Gehäuseboden einlegen.
2. **Akustik-Membran aufkleben:** Hydrophobe Gore ePTFE-Membran über die Schallöffnung des Knowles MEMS Mikrofons kleben.
3. **Platine montieren:** Fertig bestückte Front-Node Platine PCBA 05 (`openmotorbridge_front_node`) mit 4x M2.5 Schrauben handfest fixieren.
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
     * Optional: JST-PH 3-Pin Kabel für CAN-Bus an `J2` stecken (nur bei lokalem Cockpit-CAN nötig).
     * Fertiges JST-PH 2-Pin Litzenkabel vom Lenkertaster an `J3` (PTT) stecken.
6. **Dichtkämme einsetzen & Deckel verschließen:**
   * Dünnen Film Silikonfett auf die elastischen TPU-Dichtkämme ([`front_node_cable_glands_tpu.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/04_front_node/front_node_cable_glands_tpu.stl)) auftragen und in die Gehäusetaschen schieben.
   * Silikon-Rundschnur (Ø 1,5 mm, $30\,\text{cm}$) in die Deckelnut einlegen.
   * Deckel mit 4x M3 $\times 20\,\text{mm}$ Schrauben über Kreuz festziehen (greifen direkt in die unverlierbaren M3 Muttern in den Nut-Pockets).

### 4.2 Montage-Optionen des Front-Knotens am Fahrzeug
* **Option 1: AMPS-Bohrung (30 x 38 mm):** Direktmontage an RAM-Mount Kugel, Garmin-Halter oder Navi-Strebe (greift in die 4x M4 Mutternaschen am Boden).
* **Option 2: 120° V-Nut Rohrbett:** Werkzeuglose Befestigung an Ø 22 bis Ø 32 mm Lenkern / Sturzbügeln mit EPDM-Spannringen.
* **Option 3: M4 Silentblöcke:** Schwingungsentkoppelte Schraubmontage im Verkleidungsschnabel.
* **Option 4: 3M Dual-Lock Klettnuten:** Verdeckte Innenmontage an der Innenseite von Harley Batwing / Sharknose Frontverkleidungen.

---

## 5. Erstinbetriebnahme, WebSerial 1-Click Flasher & Smoke-Test

Dank der modernen **WebSerial-Integration** in der OpenMotorBridge PWA ist für die Erstinbetriebnahme **keine Installation von Python, PlatformIO, Treibern oder Terminal-Tools** erforderlich:

### 5.1 Methode A: WebSerial 1-Click Installer (Empfohlen für Endanwender)
1. Zentralbox per Standard USB-C Kabel an den PC/Mac/Laptop anschließen.
2. Chrome, Edge oder Opera öffnen und die PWA aufrufen (oder lokal über den System-Builder).
3. Im Tab *System Builder* auf **„USB-C verbinden & Flashen“** klicken.
4. Den erkannten seriellen Port (z. B. `CP2102N` / `ESP32-S3`) auswählen.
5. Die PWA flasht Bootloader, Partitionen, Firmware (`openmotorbridge_main_v8.12.bin`) und SPIFFS-Dateisystem vollautomatisch mit Fortschrittsbalken und Live-Protokoll.

### 5.2 Der geführte 4-Punkte IKEA Smoke-Test
Vor dem Aufsetzen der Gehäusedeckel wird der interaktive Selbsttest in der PWA gestartet:
1. [x] **Bordnetz & USV (Check 1):** 12.6V Bordspannung, 5.04V Buck-Schiene, USV-LiPo (2.200 mAh) auf 4.18V.
2. [x] **Kassetten & Aktuatoren (Check 2):** 1-Wire DS2431 Auslesen der Kassetten-IDs (Sena / Cardo), Pogo-Pin Kontaktierung und automatischer 4-Aktuator Klicktest (Klick 1 bis 4).
3. [x] **Front-Knoten & Cockpit (Check 3):** I2C-Ping Knowles MEMS Mikrofon, SDP31 Staudruck-Sensor (0.02 hPa) und Lenker-PTT Taster.
4. [x] **Heck-Pod 3 (Check 4):** SX1262 LoRa 868 MHz Ping-Echo und u-blox GNSS 3D-Fix.

### 5.3 Methode B: Manuelles Flashen via PlatformIO (Power-User Fallback)
```bash
# 1. Zentralcontroller via USB-C flashen (ESP32-S3)
cd openMotorBridge/firmware/main_controller && pio run --target upload && pio run --target uploadfs
# 2. Heck-Co-Prozessor flashen (RP2040 in Pod 3)
cd ../rear_coprocessor && pio run --target upload
# 3. Front-Knoten flashen (ESP32-S3)
cd ../front_node && pio run --target upload
```

---

## 6. Wartung & Pflege

* **Dichtungsinspektion:** 1x pro Saison die Silikon-Rundschnur der Main Box, des Front-Knotens und der Kassetten dünn mit dielektrischem Silikonfett pflegen.
* **Druckausgleich:** Sicherstellen, dass die ePTFE-Gore-Membranen sauber und frei von Schlamm sind.
* **Firmware-Updates:** Drahtlos und ohne Werkzeug direkt über die WebBLE-PWA-Oberfläche durchführbar.
