# OpenMotorBridge - Architecture Decisions Log (ADL)

### ADR-001: Wechsel auf 4-Punkte-Satelliten-Topologie
* **Datum:** 2026-08
* **Entscheidung:** Zentralbox unter die Sitzbank, getrennte Satelliten-Pods links (Sena), rechts (Cardo) und am Heck (OMM/GNSS).
* **Grund:** Physische Raumdiversität ($> 40\,\text{cm}$ Abstand über Metallrahmen) liefert $> 35\,\text{dB}$ HF-Dämpfung und verhindert De-Sensing im 2,4-GHz-Band.

### ADR-002: Zentraler HD26-Wandanschluss mit 2x13 Flachband-Adapter
* **Datum:** 2026-08
* **Entscheidung:** HD26 IP67 Flanschbuchse in der Gehäusewand; innen steckbar über Flachbandkabel auf die Platine.
* **Grund:** Erlaubt das Abnehmen des Gehäusedeckels zu Wartungszwecken ohne Kabelzugbelastung.

### ADR-003: Symmetrisches 6-Ader-Pod-Interface mit dedizierten 1-Wire- und Masseleitungen
* **Datum:** 2026-08
* **Entscheidung:** Alle drei Pods nutzen identische, geschirmte 6-Ader-Kabel ($3 \times 6 = 18$ Pins im HD26). Jeder Pod erhält eine eigene dedizierte Masseleitung (`GND`) und einen separaten 1-Wire Sense Pin.
* **Grund:** Verhindert Störeinkopplungen von Ladeströmen in das Audiosignal über den Schirm und ermöglicht sofortige, verwechslungssichere Steckplatz-Erkennung ohne komplexen ROM Search.

### ADR-004: Heck-Pod 3 mit autarkem ESP32-C3 Co-Prozessor
* **Datum:** 2026-08
* **Entscheidung:** Entfall des internen Mezzanine-Slots auf der Hauptplatine. Integration von MAX-M10S, SX1262 LoRa und ESP32-C3 direkt in Heck-Pod 3 mit High-Speed UART-Bridge (460.800 Baud).
* **Grund:** Optimale 360°-GNSS-Sicht, isolierte 868-MHz-Abstrahlung und Entlastung der Haupt-MCU von NMEA/UBX-Parsing.

### ADR-005: Hardware-Ergänzungen: Audio-Codec, CAN-Transceiver, Schutz & JEITA-Thermokontrolle
* **Datum:** 2026-08
* **Entscheidung:** Aufnahme des Everest ES8388 24-Bit I2S Audio-Codecs, TI TCAN334G CAN-FD Transceivers, Littelfuse SMBJ33CA TVS + Bourns PPTC Sicherung sowie 10k NTC am BQ24075 TS-Pin.
* **Grund:** Bereitstellung von HiFi-Audio-Wandlung für den ESP32-S3, standardkonforme Fahrzeug-CAN-Anbindung, $> 12\,\text{V}$ Headroom für den LM5164 Buck Regler bei Load-Dumps und Schutz des LiPo-Akkus vor Frost (< 0 °C) und Sitzbank-Hitze (> 45 °C).

### ADR-006: Adaptive Tiered QoS & LTE-Sidelink Cluster Partitioning Gateway Relay
* **Datum:** 2026-08
* **Entscheidung:** Einführung eines 3-Stufen-QoS-Kaskadenmodells (2.4 GHz Full-Duplex -> Randbereich ohne Music Sharing -> LoRa Codec2 PTT & Radar) und Adaption von 3GPP C-V2X / ProSe Sidelink Cluster Head Discovery bei getrennten Teilgruppen (Ampel- / Pass-Abriss).
* **Grund:** Verhindert den Totalabriss der Gruppenkommunikation bei Verbindungsverlust; ermöglicht Weitbereichs-Sprachtunnel zwischen autonom gewählten Gruppen-Koordinatoren bei minimalem LoRa-Duty-Cycle-Verbrauch.

### ADR-007: Akku-Grundfläche (2.200 mAh Flat-LiPo), Find My Dual-Beaconing, Smart Docking & Verzicht auf UWB
* **Datum:** 2026-09
* **Entscheidungen:**
  1. **Akku-Fläche statt Bauhöhe:** Vergrößerung der LiPo-Akkutasche auf $71 \times 42\,\text{mm}$ für eine flache 2.200 mAh Pouchzelle ($68 \times 39 \times 5{,}0\,\text{mm}$, Typ 504068 / 503870). Die Gehäuse-Außenhöhe bleibt strikt bei $38{,}0\,\text{mm}$ (maximaler Freigang unter der Sitzbank). Alle 11 Konvektionsschlitze und der Front-Kabeldurchbruch ($25 \times 4\,\text{mm}$) bleiben zu 100 % frei.
  2. **Apple & Google Find My Dual-Beaconing:** Interleaved BLE-Werbebursts ($15\,\mu\text{A}$) für weltweites Schwarm-Tracking über ~4,5 Milliarden Geräte ohne SIM-Karte oder Monatskosten. Ergibt zusammen mit der 2.200 mAh Zelle 3 bis 4 Jahre autarke Standby-Bereitschaft im Winter.
  3. **PCBA 07 (2-in-1 LoRa Smart-Keyfob):** Standardisierung als 7. Baugruppe mit nRF52840, SX1262 LoRa, TI DRV2605L LRA-Haptikmotor, 250 mAh LiPo und TI BQ51003 MagSafe Qi-Ladeempfänger.
  4. **Smart Docking & Ablauf-Agnostische Geräteerkennung:** Trennung zwischen dauerhaften USB-Speichersticks (Class 0x08 / < 0.5W, kein Alarm) und ladenden Fahrer-Smartphones (USB-PD / Qi > 10W mit BLE-Kopplung). Löst bei Zündung AUS und Entfernen des Fahrers (> 3 m) den "Handy am Lenker / Handschuhfach vergessen"-Alarm aus.
  5. **Flankengetriggerter Fahrmodus (User-Override Schutz):** Dashboard-Umschaltung ins Cockpit erfolgt nur einmalig auf der steigenden Flanke bei Ladebeginn. Manuelle Navigation zu anderen Tabs wird respektiert; kein aggressives Zurückspringen.
  6. **Verzicht auf UWB:** Da OpenMotorBridge kein OEM-Zündschloss ersetzt und der Motorstart am originalen Fahrzeugschlüssel hängt, bietet UWB keinen praktischen Schutz vor Fahrzeug-Entwendung, sondern würde Ruhestrom (30-50 mA) und Bauteilkosten unnötig in die Höhe treiben.

### ADR-008: Primat der stabilen Intercom-Sprachverbindung ("Den Lead unterstützen, nicht ersetzen"), visuelle Gruppenkultur & Verzicht auf fahrtbegleitende Push-Verkehrsdaten
* **Datum:** 2026-09
* **Entscheidungen:**
  1. **Leitmotiv "Den Lead unterstützen, nicht ersetzen":** Der erfahrene Lead-Fahrer (Tourguide) ist der beste und schnellste Sensor für das Kollektiv. Warnungen vor realen Straßenhindernissen (Rollsplitt, Baustellen, Traktoren) erfolgen per 2-Sekunden-Sprachansage über die Intercom mit $< 2\,\text{ms}$ Latenz und null Blickabwendung vom Asphalt.
  2. **Primat der stabilen, markenübergreifenden Intercom (Sena ↔ Cardo ↔ OMM):** Die Kernaufgabe von OMB ist die garantierte, unterbrechungsfreie Audio-Verbindung zwischen inkompatiblen Headsets, nicht die Bevormundung des Fahrers durch digitale Assistenten.
  3. **Respekt für bewährte visuelle Signale:** Selbst bei akutem Funkausfall bricht die Gruppe nicht zusammen: Der Lead kontrolliert die Rückspiegel; ein gesetzter Blinker rechts oder Lichthupe signalisiert sofort den Haltewunsch. Digitale Systeme dürfen diese erprobten Verhaltensmuster niemals durch Cockpit-Menüs behindern.
  4. **Strikte Anzeigestille während der Fahrt ($v > 0$):** Kein Push-Dienst für allgemeine Verkehrs- oder Staumeldungen auf dem Display. Keine störenden Pop-ups in Schräglage oder bei Bremsmanövern (Vermeidung des unwillkürlichen Sakkaden-Fixierungsreflexes und Blindflugs).
  5. **Aufgabenteilung Navigation vs. Cockpit:** Dynamische Stauumfahrung und Sperrungs-Handling verbleiben vollautomatisch in der nativen Navigations-App (CarPlay / Android Auto / Kurviger). Der Fahrer fährt nach Audio-Abbiegehinweisen und muss keine Stau-Texte lesen.
  6. **Gezielter Einsatz von Automatisierung:** Telemetrie und LoRa-Mesh greifen ausschließlich dort ein, wo der Mensch physikalisch versagt: Sturz/eCall bei Handlungsunfähigkeit ($> 6{,}5\,\text{g}$), LoRa-Abrisswarnung bei Abreißen des Schlusslichts über $1{,}5\,\text{km}$, Heckradar-Totwinkelüberwachung, Reifendruckverlust (TPMS) und Parkplatzwächter (Diebstahl-Pager).

### ADR-009: Integration des Sena SPIDER X Slim als schlanke, batterielose Mesh 3.0 Referenzkassette (Direct-DC)
* **Datum:** 2026-09
* **Entscheidungen:**
  1. **Aufnahme des Sena SPIDER X Slim in Klasse 2a (K2a):** Das Modul bietet natives **Mesh 3.0 & 2.0** sowie Wave Intercom und Bluetooth 5.3 auf Augenhöhe mit den Flaggschiffen 60S und Apex, verzichtet jedoch vollständig auf unnötigen Helm-Overhead (kein Jog-Dial, keine Helmlampen, kein integrierter Akku).
  2. **Direct-DC Versorgung ($3{,}85\,\text{V}$) über Carrier PCB:** Da Sena den LiPo-Akkupack ab Werk in ein externes Gehäuse mit Steckkabel ausgelagert hat, besitzt das Hauptmodul ($74{,}5 \times 31 \times 16\,\text{mm}$, nur $23{,}2\,\text{g}$) keinen internen Akku. Die Stromversorgung erfolgt direkt über den externen Akkuanschluss von der Trägerplatine im Satelliten-Pod 1.
  3. **Vorteile für Zuverlässigkeit & Sicherheit:** Kein LiPo-Dauerladen im heißen, geschlossenen Pod; keine Akku-Alterung oder Zellblähung; kein Aufhebeln des Gehäuses oder Zerstören von Garantiesiegeln nötig.
  4. **DLE-Scoring:** SPIDER X Slim erhält durch Mesh 3.0 und Wave volle **+60 DLE-Bonuspunkte** (wie K1 Flaggschiffe), während ältere Spider RT1/ST1 als K2b (Mesh 2.0) bei **+40 Punkten** verbleiben.
  5. **Offizielle Kern-Empfehlung für Pod 1:** Aufgrund der Mesh 3.0 Gleichstellung, der nativen Direct-DC-Fähigkeit ohne LiPo-Risiko und des um über 50 % günstigeren Anschaffungspreises gegenüber einem Sena 60S wird das SPIDER X Slim als offizielle Referenz- und Primärempfehlung für Pod 1 in OpenMotorBridge verankert.
  6. **Integrierte 3-fach Kabelpeitsche & Verzicht auf Pogo-Pin-Cradle:** Gemäß offiziellem Benutzerhandbuch (S. 6) führt das Modul Akku (⑧), Mikrofon (⑨) und Lautsprecher (⑩) auf separaten Miniatur-Steckverbindern an einer Kabelpeitsche heraus. Dadurch entfällt das für Motorradvibrationen ($> 20\,\text{g}$) und Feuchtigkeit anfällige Pogo-Pin-Cradle vollständig. Alle Signale werden über einen einfachen Adapterkabelstrang direkt mit dem 6-poligen JST-SH Header `J2` der Kassetten-Trägerplatine (PCBA 03) verbunden - 100 % zerstörungsfrei und ohne Lötarbeiten.
  7. **Präzise Opto-Pulssequenzen & Null-Tastendruck Power-Management (Handbuch v1.0.0):**
     * **Power ON/OFF (Handbuch S. 17):** Manuell `C` + `+` 1s (Ein) bzw. 1x kurz (Aus). Durch Aktivierung von *"Automatisch ein/aus"* (G-Sensor) schläft das Modul nach 2 min Stillstand ein ($< 1\,\text{mA}$) und wacht bei Motorrad-Bewegung innerhalb von 3 Tagen vollautomatisch auf. An der $3{,}85\,\text{V}$-Festspannungsschiene ist im Fahralltag keinerlei manueller Tastendruck zum Einschalten nötig.
     * **Kanalwechsel (Handbuch S. 26):** Doppelklick ($2 \times 150\,\text{ms}$ mit $150\,\text{ms}$ Pause) auf die Mesh-Taste aktiviert das Menü *"Kanaleinstellungen"*. Die Speicherung erfolgt nach 10s Inaktivitäts-Timeout automatisch. (Wichtig: Ein 1000-ms-Dauerdruck schaltet das Mikrofon stumm und darf nicht für Kanalwechsel verwendet werden).
     * **Open ↔ Group Mesh Umschaltung (Handbuch S. 29):** Ein 3000-ms-Haltepuls schaltet nahtlos zwischen Open Mesh und Group Mesh um (GATT-Kommando `0x08`, WebApp-Taste `btn-trigger-p1-group`).

### ADR-010: Smart Modular Cartridge (PCBA 03) mit In-System Profil-Flashing, 4 unabhängigen MOSFET-Aktuatoren & Entfall von Optokoppler und DS2401
* **Datum:** 2026-09
* **Entscheidungen:**
  1. **Smart Cartridge Controller (PCBA 03 Rev 2.0):** Integration eines kostengünstigen 32-Bit RISC-V Mikrocontrollers (WCH CH32V003 / ATtiny404, ca. 0,15 €) direkt auf die Kassetten-Trägerplatine.
  2. **Ersatzloser Entfall des DS2401-Chips:** Der Kassetten-MCU emuliert das 64-Bit 1-Wire ROM-ID-Protokoll nativ in Firmware auf Pin 6 (`ONEWIRE_ID`). Der separate Maxim DS2401Z+ Silizium-Chip entfällt.
  3. **Vollständiger Entfall des Optokopplers für Intercom-Kassetten:** Da mechatronische Aktuatoren die Original-Gummitasten von außen berührungslos bedienen, ist die galvanische Isolation physikalisch unendlich (Luft/Kunststoff). Der hochohmige TLP222A PhotoMOS entfällt zugunsten von 4 niederohmigen N-Kanal Power-MOSFETs (`AO3400`, $R_{\text{ON}} < 30\,\text{m}\Omega$). (Nur für analoge PMR446-Funkgeräte mit galvanischer PTT-Tastung bleibt eine Bestückungsoption bestehen).
  4. **4 unabhängige mechatronische Aktuatoren:** Volle Entkopplung der Tasterbedienung mit 4 dedizierten Kanälen:
     * `ACT_PLUS`: Taste (+) für Lauter & Menü-Weiterschaltung
     * `ACT_MINUS`: Taste (-) für Leiser & Menü-Zurückschaltung
     * `ACT_CENTER`: Mittlere Taste (Center / Bestätigen / Phone)
     * `ACT_MESH`: Mesh Intercom-Taste
     Kombinationen (wie `Power ON = Center + (+)` für 1.000 ms) werden synchron per Software angesteuert.
  5. **In-System Profil-Flashing (ISP) durch die Zentralbox:** Bei Zuweisung eines Profils in der WebApp (z. B. `sena_spider_x`) überträgt der ESP32-S3 über die Single-Wire Steuerleitung Pin 5 (`TRIGGER_PPS`) per 19.200-Baud UART vollautomatisch die Timing- und Makro-Konfiguration in den EEPROM des Kassetten-MCUs. Der Nutzer benötigt keinerlei Programmiergeräte.
  6. **Autonome Kassetten-Makros:** Komplexe Choreografien (wie Doppelklick Mesh + Pause + 1x Lauter für Kanalwechsel) taktet der Kassetten-Controller autonom auf der Platine.
  7. **Formbündige Fixierung im Kassettenbett:** Das Kassetten-Inlay (PA12-MJF) arretiert das OEM-Headset spielfrei gegen $20\,\text{g}$ Vibration, sodass die gefederten Aktuatorstößel die Gummitasten zentrisch und mit kalibriertem Hub ($1{,}0\dots 1{,}2\,\text{mm}$) treffen.

### ADR-011: All-UWB Wireless Data Backbone, Pure-DC 2-Draht-Kabelbaum, Deutsch DTM-12 & 6-PCBA Clean Architecture (v8.5 / v9.0)
* **Datum:** 2026-09
* **Entscheidungen:**
  1. **100 % drahtloser Daten- und Audiopfad (All-UWB & Bluetooth):**
     * Sämtliche Interconnects (Cockpit PTT, GNSS, Sensoren, Radar 20 Hz Zielerkennung, Kassetten-Mechatronik und Steuerung) zwischen Zentralbox und allen Satellitenknoten laufen **ausschließlich über Ultra-Wideband (Qorvo DW3110 6.5 GHz Ch. 5, $< 0{,}4\,\text{ms}$ Latenz, AES-128-CCM)**.
     * Der reale Audiopfad von OEM-Headsets (Sena SPIDER X Slim, Cardo Packtalk Edge) in den Kassetten verbindet sich per Bluetooth mit der Zentralbox (`PCBA 01`). Der ESP32-S3 und ES8388 24-Bit Audio-DSP mischen alle Streams und übertragen den Mix per Bluetooth an die Helme von Fahrer und Sozius.
     * **Kompletter Entfall von NF-Audiokabeln:** Bourns-Audioübertrager (`T1, T2`) und PhotoMOS-Relais (`OC1, OC2`) auf der Zentralbox entfallen ersatzlos.
  2. **Bereinigung auf ein 6-Platinen-Lineup (Clean Architecture):**
     * Der Hardware-Baukasten schrumpft von 8 auf **exakt 6 aktive Platinen**: `PCBA 01` (Zentralbox), `PCBA 03` (Smart Cartridge), `PCBA 05` (Universal Front-Knoten), `PCBA 06` (MagSafe Dock), `PCBA 07` (Smart Keyfob) und `PCBA 08` (Radar 2.0 Sub-MCU).
     * `PCBA 02` (Pod Base Platine) und `PCBA 04` (Heck-Pod 3) entfallen ersatzlos.
  3. **Reiner 2-Draht-DC-Power-Kabelbaum:**
     * Alle Satellitenpeitschen (Pod 1, Pod 2, Radar) sind reine 2-Draht-Gleichstromleitungen (+5V/GND bzw. +12V/GND).
     * M8- und USB-C-Steckverbinder an den Pods entfallen komplett.
     * Das Pod-Gehäuse (`pod_base_housing.stl`) wird als monolithisches MJF-3D-Druckteil ohne interne Platine ausgeführt; die 2-Draht-Leitung führt direkt auf zwei vergoldete Federkontakte.
  4. **Zentraler Bordnetz-Stecker (Deutsch DTM-12):**
     * Der sperrige 26-polige HD26-Stecker wird durch einen kompakten, hochgradig automotiven **Deutsch DTM-12** Industriestecker (11 aktive Kontakte: KL30, KL15, GND, CAN-FD, 2x Pod 1 5V, 2x Pod 2 5V, 2x Radar 12V, 1x Gehäuseschirm) ersetzt.
  5. **100 % einheitliches Kassetten-Layout (PCBA 03 Unified DNP Strategy & 2-seitig SMT):**
     * Ein einziges Leiterplattenlayout für alle Kassettenvarianten (`PCBA 03`, $35 \times 25\,\text{mm}$, 2 Lagen ENIG, 2-seitig SMT).
     * **Top-Seite:** Qorvo DW3110 UWB Transceiver, UWB Antenne, SPI Host-MCU.
     * **Bottom-Seite:** 4x AO3400A MOSFETs für Aktuatoren, J_ACT Header, 2-Pin DC-Frontpads und DNP-Codec-Pads.
     * Kassetten für Sena / Cardo mechatronische Betätigung bestücken 4x AO3400A MOSFETs; der Audio-Codec ES8311 bleibt unbestückt (DNP).
     * Kassetten für analoge Funkgeräte (Midland PMR446) bestücken den ES8311-Codec zur Digitalisierung des Funksignals und streamen via UWB.
     * *Optionale Swap-Kassette:* OMM 2.4 GHz ist eine rein optionale Wechselkassette für reinen Open-Source-Meshfunk.
  6. **Sequential Power-Sequencing für Slot-Erkennung (Keyless-Ride optimiert):**
     * Gestaffeltes Einschalten der Strompfade: $T = 0\,\text{ms}$ Front-Knoten & Zentralbox (Cockpit sofort aktiv), $T = 200\,\text{ms}$ Bucht 1 (Links), $T = 350\,\text{ms}$ Bucht 2 (Rechts), $T = 500\,\text{ms}$ Radar.
     * Pod 1 und Pod 2 sind reine symmetrische physische Montagebuchten für Gateways (keine Zuordnung Fahrer/Sozius; Helme sind separat per Bluetooth angebunden).
     * Ein Vertauschen von Slots oder Einbuchen von Nachbar-Bikes ist physikalisch unmöglich.
  7. **Key-Reset & Nahtloses Multi-Vehicle Roaming (Auto ↔ Bike):**
     * Physischer SMD-Taster `SW1` (`SW_PAIR_RESET`) auf `PCBA 01` (3s Pairing-Modus, 10s Key-Purge).
     * Bis zu 4 Fahrzeug-Netzwerkschlüssel im NVS der Kassette (`PCBA 03`) gespeichert.
     * Beim Umstecken einer Kassette aus dem Auto in das Motorrad erfolgt eine unkomplizierte "Plug & Confirm"-Übernahme (Bestätigung per App oder PTT-Doppelklick) ohne Datenverlust oder Werksreset.