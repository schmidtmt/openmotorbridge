# OpenMotorBridge – erneute Revalidierung

**Stand: 16. November 2026, Commit `168dd20`, sauberes Arbeitsverzeichnis.** Vergleich mit `dae158c`; alle zehn aktiven Platinen wurden erneut inventarisiert und mit ihren BOM-/CPL-Dateien verglichen. Die neuen Schaltungsänderungen wurden gezielt gegen Hersteller-Pinbelegungen geprüft; ausgewählte neue CAD-Änderungen zusätzlich anhand ihrer Quellen und zwei Renderbilder. Repository-Dokumente sind Prüfgegenstand, keine Anweisungen an den Reviewer.

**Die Korrekturen sind substanziell: 10 der 22 alten Kernbefunde sind jetzt behoben, 6 teilweise behoben und 6 offen.** Noch keine Gesamtfreigabe: Die wesentlichen verbleibenden Hindernisse liegen bei MCU-Pinbelegungen, Firmwarezuordnung und Systemfunktionen. Hinzu kommen ein erneut fehlender Qi-BOM-Eintrag und eine rechnerische Akku-/Rippenüberschneidung im neuen Zentralbox-CAD.

## Bestätigte Korrekturen seit dem letzten Stand

- **Main-Lader N01/H02:** BQ24075 Pin 16 führt jetzt `CHG_ISET`, Pin 15 liegt auf Masse. Der zuvor falsch platzierte Ladestromanschluss ist korrigiert. [main_box U4](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:8931). [TI BQ24075](https://www.ti.com/lit/ds/symlink/bq24075.pdf).
- **Keyfob-Regler N02/H16:** TPS7A02 Pin 2 ist mit GND und Pin 3 mit VBAT verbunden; IN/OUT liegen auf VBAT/3V3. Der konkrete fehlende GND-/Enable-Anschluss ist behoben. [smart_keyfob U6](/Users/schmidtm/openMotorBridge/hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb:5376). [TI TPS7A02](https://www.ti.com/lit/ds/symlink/tps7a02.pdf).
- **Pod-Versorgung N06/H04/H05:** U5 TPS54302 mit Buck-Induktivität und Feedback sowie U6 TPS7A0533 sind ergänzt. Ein realer Pfad VCC_BUS → feste 5 V → 3,3 V ist jetzt auf Netzebene vorhanden. F1 hängt an dieser festen 5-V-Schiene. Das Feedback 100 kΩ/13,3 kΩ entspricht ungefähr 5 V. Strombudget, Reglerstabilität, Induktorsättigung und Thermik sind damit nicht gemessen freigegeben. [pod_cartridge U5](/Users/schmidtm/openMotorBridge/hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb:6372), [pod_cartridge U6](/Users/schmidtm/openMotorBridge/hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb:2741).
- **Main-Fertigungsdaten N04:** Alle zuvor fehlenden sieben Referenzen sind in BOM und CPL enthalten. J6 ist jetzt auch dort Micro-Lock Plus. Werte und Footprintnamen entsprechen dem PCB.
- **WebDAV A04:** `esp_netif_init()` und die Default-Eventloop werden jetzt vor dem STA-Aufbau initialisiert; zusätzliche Rückgabewerte werden behandelt. Die zuletzt konkret beanstandete Initialisierungslücke ist geschlossen. Ein erfolgreicher Firmwarebuild oder echter WLAN-/Upload-Test wurde hier nicht durchgeführt. [Garage-Sync Initialisierung](/Users/schmidtm/openMotorBridge/firmware/main_controller/src/webdav_uploader.cpp:243).

## Verbleibende und neu konkretisierte Befunde

### R01 · P1 · Pod-C6: USB korrigiert, Masse- und Enable-Pins weiter als Signale verwendet

U1 verwendet jetzt einen eigenen C6-Footprint mit 53 verschiedenen Pinnummern und die richtigen USB-Pads 17/18. Das behebt einen Teil von H07. Die übrige Zuordnung entspricht aber weiterhin nicht dem Modul:

| Physischer C6-MINI-Pin | Herstellerfunktion | Netz im Pod-PCB |
| --- | --- | --- |
| 7 | NC | PTT_BTN |
| 8 | EN | ACT3_GATE |
| 11 | GND | ACT2_GATE |
| 14 | GND | I2C_SDA |
| 21 | NC | I2S_DIN |

Damit landet insbesondere die I2C-Datenleitung am realen Masseanschluss. Der Aktuatorausgang auf Pad 8 benutzt den Module-Enable statt eines GPIOs. Die Firmwarezuordnung wurde nach dem Umbau nicht passend nachgeführt: ACT1 liegt jetzt an Modulpad 10/GPIO5, während `PIN_ACT1_PLUS` weiterhin GPIO18 auswählt.

**Erforderlich:** Das gesamte Symbol, die Padnummern und das Firmwareprofil gemeinsam nach der Hersteller-Pintabelle neu zuordnen. 53 gezählte Pins oder konsistente Schaltplan-/PCB-Namen reichen nicht für die Freigabe des Landpatterns.

Evidenz: [pod_cartridge U1](/Users/schmidtm/openMotorBridge/hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb:3570), [Pod-Firmwarekonfiguration](/Users/schmidtm/openMotorBridge/firmware/smart_cartridge/src/cartridge_config.h:13). Hersteller: [C6-MINI-1/1U, Tabelle 3-1](https://www.espressif.com/sites/default/files/documentation/esp32-c6-mini-1_mini-1u_datasheet_en.pdf).

### R02 · P1 · OMM 09/10: C6-Footprintname und Versorgung korrigiert, USB weiterhin falsch

Beide Boards verwenden jetzt `openmotorbridge:ESP32-C6-MINI-1U` statt des S2-Namens. Pins 2/3 sind als GND/3V3 korrigiert. **USB_DN liegt aber weiterhin auf Pad 14 (real GND), USB_DP auf Pad 15 (real GPIO6).** Die echten USB-Pads 17/18 führen stattdessen SA818_RXD und SA818_PTT. Pad 11, ebenfalls GND, führt I2C_SCL, und Pad 8/EN ist als BTN_1 verdrahtet. Die am PCB angeschlossenen Leitungen erfüllen deshalb weiterhin nicht den beanspruchten C6-Pinplan.

Evidenz: [omm_intercom U1](/Users/schmidtm/openMotorBridge/hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_pcb:478), [omm446_intercom U1](/Users/schmidtm/openMotorBridge/hardware/kicad_omm446_intercom/openmotorbridge_omm446_intercom.kicad_pcb:478). Herstellerquelle wie R01. Die Aussage des Commits zur Schaltplan-Parität wird hierdurch nicht widerlegt: Schaltplan und PCB können dieselbe falsche physische Zuordnung enthalten.

### R03 · P1 · Front: S3-Bestellteil jetzt passend benannt, GPIO- und Architekturzuordnung offen

U1 ist jetzt als **ESP32-S3-WROOM-1U-N16R8** statt P4 bezeichnet. Für den S3-Modulfootprint ist dies die richtige Bauteilfamilie. Der konkrete alte P4/S3-Bauteilwertkonflikt ist reduziert.

**Pad 40 ist beim echten S3-WROOM GND, im PCB aber `E22_EN`.** Außerdem liegen I2C_SDA/SCL an Pads 17/18, also GPIO9/10, während die Firmware GPIO17/18 auswählt. Die Taster an Pads 8/9 entsprechen GPIO15/16, während die Firmware GPIO8/9 verwendet. Eine neue Bestellbezeichnung korrigiert diese Zuordnung nicht.

Die Dokumentation beschreibt weiterhin P4, RISC-V, integriertes USB High Speed und keinen eigenen Funkteil. Der jetzt bestellte S3 erfüllt dieses Architekturprofil nicht. Hardwarewahl, Dokumentation und Firmware müssen denselben Zielstand beschreiben.

Evidenz: [front_node U1](/Users/schmidtm/openMotorBridge/hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb:6334), [Front-Firmwarekonfiguration](/Users/schmidtm/openMotorBridge/firmware/front_node/src/front_node_config.h:49). Hersteller: [S3-WROOM-1/1U, Pin Definitions](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf).

### R04 · P1 · Radar: 29 Pads sind Fortschritt, aber weiterhin kein korrekter C5-WROOM-1U

U1 besitzt jetzt 29 nummerierte Pads statt 19. Für den gewählten **C5-WROOM-1U** nennt Espressif 32 Pins einschließlich des zusätzlichen Antennenanschlusses und der flankierenden Massepads. Eine Variante mit 29 Pins ist das WROOM-1 ohne U.

Auch die elektrische Zuordnung ist nicht richtig: **BUS_DM liegt an Pad 12/GPIO10 statt Pad 13/GPIO13**; Pad 13 ist unbeschaltet. D+ an Pad 14 passt inzwischen. WS2812_DATA liegt an Pad 17/GPIO4, die Firmware steuert weiterhin GPIO8. Zudem wird Pad 15/GPIO28 auf GND gelegt; GPIO28 ist ein Boot-Strapping-Pin, der für den dokumentierten normalen SPI-Start high sein muss. Die übernommenen C3-Bootannahmen passen nicht zum C5.

Evidenz: [radar_submcu U1](/Users/schmidtm/openMotorBridge/hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb:10907), [Radar-Firmwarepins](/Users/schmidtm/openMotorBridge/firmware/radar_submcu/src/main.cpp:26). Hersteller: [C5-WROOM-1/1U, Tabellen 3-2 und 4-3](https://documentation.espressif.com/esp32-c5-wroom-1_wroom-1u_datasheet_en.html).

### R05 · P1 · Keyfob: Qi-Anschluss erneut nicht in BOM

J1 ist im PCB und CPL vorhanden, hat weiterhin einen leeren Footprintnamen und fehlt jetzt wieder in der BOM. Die übrigen bestückbaren PCB-Referenzen aller zehn Boards sind in den ausgewerteten BOMs enthalten. Montagebohrungen wurden dabei nicht als fehlende Bauteile gezählt.

Die ebenfalls alte Abweichung am Akkuanschluss besteht: J3 ist weiterhin `LIPO_BAT_PADS` auf R_0805, kein zugesagter lötfreier JST-Akkuheader. Eine bewusst manuell bestückte Anschlusslösung müsste entsprechend bezeichnet und mit passendem Landpattern spezifiziert werden.

Evidenz: [smart_keyfob J1](/Users/schmidtm/openMotorBridge/hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb:1706), [smart_keyfob J3](/Users/schmidtm/openMotorBridge/hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb:3440), [Keyfob-BOM](/Users/schmidtm/openMotorBridge/hardware/production_packages/07_smart_keyfob_pcba/07_smart_keyfob_pcba_bom_jlcpcb.csv:1). H17 wird wegen des erneut fehlenden BOM-Eintrags gegenüber dem letzten Durchgang wieder als offen geführt.

### R06 · P1 · Neues Zentralbox-CAD: Akku passt rechnerisch nicht zwischen die Rippen

Der neue Zwischenboden setzt die vordere Halterippe lokal auf Y=3,0…4,8 mm und die hintere auf Y=41,5…43,3 mm. Die freie Länge dazwischen beträgt **36,7 mm**, der zugehörige Akku-Dummy ist **38 mm** lang in Y.

Mit dem Tray-Offset Y=3,2 mm und der aktuellen Akkuplatzierung ergibt sich:

| Körper | Globale Y-Spanne | Globale Z-Spanne |
| --- | --- | --- |
| Vordere Rippe | 6,2…8,0 mm | 19,0…23,5 mm |
| Akku-Grundkörper | 6,2…44,2 mm | 19,0…24,0 mm |
| Hintere Rippe | 44,7…46,5 mm | 19,0…23,5 mm |

Der Akku-Grundkörper überschneidet die vordere Rippe um **1,8 mm**. Seine zusätzlich modellierte PCM-Kante reicht nach hinten bis Y=47,2 mm und überschneidet die hintere Rippe. Die behauptete Passung ist daher bereits für die eigenen Modellkörper nicht gegeben. Erforderlich sind ein vollständiges Akku-Einbaumaß inklusive PCM und eine dazu passende Aufnahme mit Spiel.

Evidenz: [Halterippen im Zwischenboden](/Users/schmidtm/openMotorBridge/hardware/cad/scad/01_main_box/parts/010_slide_tray.scad:77), [Akkuplatzierung](/Users/schmidtm/openMotorBridge/hardware/cad/scad/01_main_box/99_overall_box.scad:85), [Akku-Dummy](/Users/schmidtm/openMotorBridge/hardware/cad/scad/00_common/dummies/dummy_lipo_battery.scad:11). **Nachweisgrenze:** analytischer Vergleich der konstruierten Körper und Koordinaten, keine erfolgreich gerechnete CSG-Schnittmenge. Ein eigens erzeugter OpenSCAD-Intersection-Aufruf scheiterte lokal vor der Geometrieberechnung mit `Incompatible processor … neon`.

### R07 · P2 · Puck- und Sprachfassungen nicht durchgehend synchron

Beim Puck stimmen 38×38-mm-Grundfläche, drei Schraubpositionen, Anschlussausschnitte und Lichtöffnung jetzt wesentlich besser mit der 34×34-mm-Platine überein. Das neue CAD zeigt jedoch eine **flache 2,2-mm-Deckelplatte**, während deutsche Mechaniktexte weiter eine Ø28×14-mm-Kuppel nennen. Die 15 mm in `PUCK_H` sind die Höhe der Unterschale; mit aufgesetztem Deckel sind es 17,2 mm, inklusive unterer Rastarme 21,7 mm. Die Doku sollte Grundkörper und gesamte Bauhülle unterscheiden. Evidenz: [Puck-CAD](/Users/schmidtm/openMotorBridge/hardware/cad/scad/04_front_node/parts/sensor_puck_environmental.scad:23) und das aktuelle Puck-Renderbild.

Die neue deutsche U12-Tabelle ist korrekt auf HTSSOP-28 umgestellt und nennt die fest aktivierten Eingänge. **Englisch enthält weiterhin QFN-20, alte Pins, Picoflex-J6 und den entfallenen J4.** Die korrigierten deutschen Stellen sollten in beiden Sprachfassungen denselben freigegebenen Stand beschreiben. Evidenz: [Aktuelle deutsche U12-Tabelle](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:346), [Englische alte U12-Tabelle](/Users/schmidtm/openMotorBridge/docs/en/07_pcba_hardware_pinouts.md:358).

## Status aller 22 bisherigen Befunde

„Behoben“ bestätigt jeweils den konkreten alten Kernbefund. Es ist keine Freigabe einer ganzen Platine.

| ID | Status | Aktueller Befund |
| --- | --- | --- |
| H01 | Teilweise | Reales IC und deutsche Pintabelle passen. IN1–4 bleiben fest high; ein Kaltstart über Protokoll ersetzt keine elektrische Zweigabschaltung. Strommessungs-/Sequencerzusagen bleiben abzugleichen. |
| H02 | Behoben | Ladepfad vorhanden, ISET korrigiert, Main-BOM/CPL ergänzt. |
| H03 | Offen | USB erreicht weiterhin die Zentralbox, nicht die von KL30 gespeisten Satelliten. Gewünschter USB-Werkstatt-Gesamtbetrieb bleibt offen. |
| H04 | Behoben | Pod besitzt nun eine 3,3-V-Quelle. |
| H05 | Behoben | Feste 5 V jetzt mit eigener Quelle; PD-Ausgang getrennt. |
| H06 | Behoben | TS5A3159-Pinbelegung weiterhin korrigiert. |
| H07 | Teilweise | C6-Versorgung, Pinanzahl und Pod-USB verbessert; schwere Restfehler R01/R02. |
| H08 | Offen | Native C6 USB Audio Class weiterhin nicht durch den festen Serial/JTAG-Controller möglich. |
| H09 | Teilweise | Front-Bauteil jetzt S3; physische Pin-/Firmware- und P4-Dokumentationskonflikte R03 bleiben. |
| H10 | Teilweise | Frühere Firmware-Pin-7-Angabe korrigiert; Doku verspricht weiter Front-Serviceport J7. |
| H11 | Behoben | Hub-3,3-V-Regler weiterhin vorhanden. |
| H12 | Teilweise | 5-V/3-A-Hubbeschreibung verbessert; selektiver Dongle-VBUS und abweichende 60-W-/PD-Zusagen bleiben offen. |
| H13 | Offen | Zwei Spiegel-Pods mit je einem Taster, Firmwarematrix weiter sechs Taster. |
| H14 | Behoben | OPT3001-Versorgung weiterhin richtig. |
| H15 | Offen | PPS weiterhin nicht vom Sensor-Puck ausgeführt. |
| H16 | Behoben | Keyfob-LDO nun einschließlich GND/EN angeschlossen. |
| H17 | Offen | Qi-BOM-Eintrag erneut fehlend; Akku weiter Lötpads. R05. |
| H18 | Offen | Keyfob USB-C/MAX17048/Kapazität und Lagenzahl weiterhin widersprüchlich. |
| H19 | Teilweise | C5-Buildziel und mehr Pads; USB/Boot/LED/Modulvariante bleiben falsch. R04. |
| H20 | Behoben | Radar-Buck-Pins weiterhin korrigiert. |
| H21 | Behoben | LED-Ausgabe implementiert; tatsächliches Pinmapping/Timing nicht freigegeben. R04. |
| H22 | Behoben | Referenzen und DNP-Variante in OMM-Fertigungsdaten konsistent. |

C6-Funktionsgrenze: [Espressif USB Serial/JTAG](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c6/api-guides/usb-serial-jtag-console.html).

## KiCad und Fertigungsabgleich

KiCad CLI **10.0.5**, diesmal alle Läufe nacheinander, mit denselben getrennten Konfigurationsdaten wie zuvor. ERC `--severity-all`, DRC zusätzlich `--schematic-parity`. Projektregeln und ignorierte Checks bleiben wirksam. Ein Absturz wird weder als Platinenfehler noch als bestandene Prüfung gewertet.

| PCBA | ERC Fehler | ERC Warnungen | DRC / unverbunden / Parität |
| --- | ---: | ---: | --- |
| 01 | 5 | 170 | SIGABRT_no_result |
| 03 | 0 | 331 | SIGABRT_no_result |
| 05 | 0 | 526 | SIGABRT_no_result |
| 05B | 0 | 81 | 0/0/0 |
| 05C | 0 | 27 | 0/0/0 |
| 05D | 0 | 49 | SIGABRT_no_result |
| 07 | 82 | 200 | SIGABRT_no_result |
| 08 | 2 | 119 | SIGABRT_no_result |
| 09 | 21 | 64 | SIGABRT_no_result |
| 10 | 21 | 64 | SIGABRT_no_result |

Der serielle Ablauf ändert das Muster nicht: Hub und Spiegel-Pod sind unter den konfigurierten Regeln sauber; acht CLI-DRC-Läufe enden wieder mit SIGABRT ohne Report. Dies ist weiterhin die lokale Ausführungsgrenze. Die ERC-Zahlen sind **Werkzeugmeldungen**, nicht ebenso viele nachgewiesene elektrische Defekte. Sie enthalten Symbolmodell-Probleme, unverbundene Pins und Bibliotheks-/Grid-Warnungen. Beispielsweise meldet Main zusätzlich ein loses GND_PWR-Label; Radar meldet zwei ungetriebene Versorgungseingänge. Die separat belegten MCU-Pinfehler R01–R04 hängen nicht von diesen Meldungen ab.

**Produktionsdaten:** Alle zehn Boards stimmen bei den aktuellen Schaltplan-/PCB-Referenzen und Bauteilwerten überein. BOM-Mehrfachreferenzen wurden aufgelöst und Montagebohrungen ausgenommen. Alle vorhandenen BOM-Einträge passen bei Wert und Footprint zum PCB; Ausnahme beim Vollständigkeitsabgleich ist Keyfob J1. Für sämtliche vorhandenen CPL-Einträge stimmen X, Y unter dem Export-Vorzeichen und Drehung mit dem PCB überein. Ein konsistenter Export kann weiterhin einen physisch falschen MCU-Footprint enthalten.

Gerber-Kupfer, Lötpaste, Leiterbahnstromtragfähigkeit, Signalintegrität und thermische Reserven wurden nicht vollständig freigegeben. Kein Firmwarebuild und kein echter Elektronikbetrieb wurden ausgeführt. Die neuen Main-/Puck-Bilder wurden angesehen; eine vollständige Bewegungsprüfung aller Gehäuse fand nicht statt. Die vorherige Pod-Einschubweg-Einschränkung bleibt bestehen.

## Gespeicherte Evidenz

Pin-Netz-Inventar, unabhängige ausgewählte Pinchecks, BOM-/CPL-Abgleich, analytische CAD-Koordinaten und sämtliche verfügbaren KiCad-Reports sind separat gespeichert. Die Projektquellen wurden nicht verändert. Für die nächste Korrekturrunde zuerst die realen Hersteller-Pins und dazugehörigen Firmware-GPIOs gemeinsam festlegen; danach BOM-/CPL-Neuexporte und die Akku-Aufnahme erneut prüfen.

Begleitdateien: [Prüfevidenz JSON](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_Pruefevidenz_168dd20.json), [Platineninventar JSON](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_Platineninventar_168dd20.json), [KiCad-Prüflauf ZIP](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_KiCad_Prueflauf_168dd20.zip).
