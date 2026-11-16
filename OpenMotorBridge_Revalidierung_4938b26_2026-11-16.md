# OpenMotorBridge – Revalidierung `4938b26`

**16. November 2026.** Vergleichsbasis `168dd20`; Arbeitsverzeichnis zu Beginn sauber. Erneut geprüft: Inventar aller zehn aktiven Platinen, ausgewählte Hersteller-Pins, zugehörige Firmware-GPIOs, BOM/CPL und die geänderte Akku-/Antennenaufnahme. Dokumente bleiben Prüfgegenstand; die Nutzeridee der USB-Werkstattversorgung wird nicht durch eine eingeschränkte Beschreibung ersetzt.

**Ergebnis: Deutliche Fortschritte an C6-Belegung, Pod-Firmware, Qi-Fertigungsdaten und Akkuaufnahme. Kritische Restpunkte bestehen am Front-Footprint sowie an OMM-/Radar-Firmwarezuordnungen.** Die alte feste Akku-/Rippenkollision ist beseitigt; die verschobenen Antennen-Dummys überschneiden sich jetzt stattdessen. Eine Gesamtfreigabe ist weiterhin nicht gegeben.

Von H01–H22 sind **11 im alten Kern behoben, 5 teilweise behoben und 6 offen**. Diese Zählung verfolgt historische Befunde; sie ersetzt nicht die nachstehende Liste der heutigen Restprobleme.

## Bestätigte Korrekturen

- **C6 auf Pod und OMM:** Pins 11/14 jetzt GND, Pin 8 EN an 3V3, USB auf 17/18 und keine Signalbelegung mehr auf den zuvor beanstandeten NC-Pads 7/21. Die konkreten kritischen Hardware-Pinfehler aus dem letzten Review sind korrigiert. Beim Pod sind die verwendeten Aktuator-, PTT-, OMM-Detect-, I2C- und I2S-GPIOs in der Firmware passend nachgeführt. Ein vollständiger maßlicher Landpatternnachweis ist damit nicht ersetzt. [pod_cartridge U1](/Users/schmidtm/openMotorBridge/hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb:2487), [Pod-Konfiguration](/Users/schmidtm/openMotorBridge/firmware/smart_cartridge/src/cartridge_config.h:13), [omm_intercom U1](/Users/schmidtm/openMotorBridge/hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_pcb:478), [omm446_intercom U1](/Users/schmidtm/openMotorBridge/hardware/kicad_omm446_intercom/openmotorbridge_omm446_intercom.kicad_pcb:478).
- **Radar-USB und Bootpegel:** BUS_DM/DP jetzt an Modulpad 13/14; die Firmware nennt GPIO13/14. Pad 15/GPIO28 liegt nun auf 3V3 statt GND. Der konkret beanstandete falsche Low-Pegel für den normalen Start ist entfernt.
- **Qi:** J1 hat nun einen Footprintnamen und ist wieder in BOM und CPL enthalten. [smart_keyfob J1](/Users/schmidtm/openMotorBridge/hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb:1706), [Keyfob-BOM](/Users/schmidtm/openMotorBridge/hardware/production_packages/07_smart_keyfob_pcba/07_smart_keyfob_pcba_bom_jlcpcb.csv:9).
- **Akkuaufnahme:** Zwischen den festen Rippen stehen jetzt X=22,4…90,8 mm und Y=5,6…47,6 mm zur Verfügung. Akku inklusive modellierter PCM-Kante liegt bei X=22,9…89,9 mm und Y=6,0…47,0 mm. Die alte Überschneidung mit den festen Vorder-/Hinterrippen ist rechnerisch behoben. Die linke elastische Haltenase greift noch 0,3 mm in den Dummy; das ist als beabsichtigte Klemmung mit Verformung/Toleranz zu prüfen, kein erneuter Nachweis der alten festen Rippenkollision. [Zwischenboden](/Users/schmidtm/openMotorBridge/hardware/cad/scad/01_main_box/parts/010_slide_tray.scad:78), [Akkuplatzierung](/Users/schmidtm/openMotorBridge/hardware/cad/scad/01_main_box/99_overall_box.scad:85).
- **Produktionsabgleich:** Jetzt keine fehlende bestückbare Referenz in den zehn BOMs oder CPLs. Werte/Footprintnamen der BOM und Positionen/Drehungen der CPL passen zum aktuellen PCB. Gruppierte BOM-Referenzen wurden aufgelöst, Montagebohrungen ausgenommen.

Herstellerbezug für die C6-Pinprüfungen: [Espressif C6-MINI-1/1U, Tabelle 3-1](https://www.espressif.com/sites/default/files/documentation/esp32-c6-mini-1_mini-1u_datasheet_en.pdf).

## Aktuelle Restbefunde

### S01 · P1 · Front wieder mit P4-Wert auf S3-Modulfootprint

U1 wurde von `ESP32-S3-WROOM-1U-N16R8` zurück auf **`ESP32-P4-NR16`** geändert. Der gespeicherte Footprint ist weiterhin **`ESP32-S3-WROOM-1U`** mit 41 verschiedenen Padnummern. Der P4 ist ein QFN104-Baustein, kein auf diesen S3-Modulanschluss bestückbarer Ersatz. Damit ist der ursprüngliche konkrete H09-Konflikt wieder vollständig vorhanden.

**Erforderlich:** Entweder ein wirkliches P4-Layout mit Hersteller-Landpattern und passendem Pinplan oder ein konsequent auf das reale S3-Modul abgestimmter Hardware-/Firmware-/Dokumentationsstand. Eine Umbenennung des Wertes erfüllt das nicht.

Evidenz: [front_node U1](/Users/schmidtm/openMotorBridge/hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb:6333). Hersteller: [Espressif P4, Packaging](https://documentation.espressif.com/esp32-p4_datasheet_en.html).

### S02 · P1 · OMM-Hardware korrigiert, mehrere Firmware-GPIOs bleiben alt

Beide OMM-Boards haben jetzt die richtigen grundlegenden C6-Masse-/Enable-/USB-Anschlüsse. Die Firmwarekonfigurationen sind nach der neuen Signalverteilung aber nicht vollständig angepasst:

| Signal auf PCBA 09/10 | Modulpad → realer GPIO | Firmware 09 und 10 |
| --- | --- | --- |
| I2C_SDA | 16 → GPIO7 | GPIO8 |
| I2C_SCL | 15 → GPIO6 | GPIO9 |
| WS2812_DATA | 12 → GPIO0 | GPIO6 |
| SA818_PTT | 22 → GPIO8 | GPIO16 |

Damit werden beispielsweise Codec-I2C und LED weiterhin an anderen Pins betrieben als verdrahtet. PTT betrifft insbesondere die bestückte Funkvariante PCBA 10. Die I2S-GPIO-Werte passen inzwischen zur neu verlegten Hardware; es wird nicht die gesamte Konfiguration pauschal als falsch eingestuft.

**Erforderlich:** Alle aktiv verwendeten Firmwarepins gegen die echten Modul-GPIOs abgleichen, einschließlich Ladezustand, Taster und Bluetooth-Steuerleitungen. Die unabhängigen Beispielprüfungen liegen im JSON.

Evidenz: [OMM-Konfiguration](/Users/schmidtm/openMotorBridge/firmware/omm_module/src/omm_module_config.h:29), [OMM446-Konfiguration](/Users/schmidtm/openMotorBridge/firmware/omm446_module/src/omm446_config.h:34), [omm_intercom U1](/Users/schmidtm/openMotorBridge/hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_pcb:478), [omm446_intercom U1](/Users/schmidtm/openMotorBridge/hardware/kicad_omm446_intercom/openmotorbridge_omm446_intercom.kicad_pcb:478). Herstellerquelle: C6-Tabelle oben.

### S03 · P1 · Radar-LED und UART verwenden weiterhin falsche GPIOs

USB ist korrigiert. Bei LED/UART wurden teilweise nur Kommentare angepasst:

| Netz | Physisches C5-Modulpad → GPIO | Gewählter Firmware-GPIO |
| --- | --- | --- |
| WS2812_DATA | 12 → GPIO10 | GPIO8 |
| MR20_TX → MCU-RX | 4 → GPIO2 | GPIO3 |
| MR20_RX ← MCU-TX | 5 → GPIO3 | GPIO4 |

Die Zeile `GPIO_NUM_8 // U1 Pad 12` ist daher weiterhin falsch. Ein echter Halo-Treiber im Code erreicht so den verdrahteten Halo nicht. Der MR20-UART ist ebenfalls nicht passend zugeordnet.

Außerdem enthält der als C5-WROOM-1U bezeichnete Footprint weiterhin **29 statt 32 Pins**. Die drei Zusatzpins des 1U betreffen den zusätzlichen Antennenanschluss und Masse; auch wenn der zweite Antennenpfad nicht benutzt wird, ist damit noch kein vollständiges Hersteller-Landpattern nachgewiesen. Der Boot-Taster liegt weiter auf GPIO9, während der C5 andere Download-Strapping-Pins verwendet. Die korrigierte GPIO28-Freigabe ersetzt diesen Recovery-Nachweis nicht.

Evidenz: [radar_submcu U1](/Users/schmidtm/openMotorBridge/hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb:10907), [Radar-Konfiguration](/Users/schmidtm/openMotorBridge/firmware/radar_submcu/src/main.cpp:26). Hersteller: [C5-WROOM-1/1U, Pin Definitions und Boot Configurations](https://documentation.espressif.com/esp32-c5-wroom-1_wroom-1u_datasheet_en.html).

### S04 · P2 · Nach Akku-Korrektur überschneiden sich beide Antennen-Dummys

Die LoRa-Antenne wurde nach hinten verschoben. Bei geschlossenem Aufbau definieren die Quellen folgende rechteckige Grundkörper:

| Antenne | X | Y | Z |
| --- | --- | --- | --- |
| LoRa | 12,8…97,8 | 49,2…67,2 | 19,0…19,8 |
| 2,4 GHz | 30,8…77,8 | 63,7…70,7 | 19,6…20,1 |

Alle Maße in mm. Die gemeinsame Körpermenge hat **47 × 3,5 × 0,2 mm**. Der Höhenversatz von 0,6 mm ist kleiner als die modellierte LoRa-Dicke von 0,8 mm. Bei beabsichtigter Überlappung muss der Z-Abstand einschließlich Spiel und Trägergeometrie passen; alternativ die Y-Anordnung ändern.

Dies ist ein analytischer CAD-Befund, keine gemessene RF-Beeinflussung und keine erfolgreiche OpenSCAD-CSG-Prüfung. Die bekannten lokalen OpenSCAD-Ausführungsprobleme wurden nicht als Konstruktionsfehler gezählt. Die Render-PNGs wurden zwischen den beiden geprüften Commits nicht erneuert, obwohl SCAD und Tray-STLs geändert wurden; sie bestätigen daher nicht die neue Anordnung.

Evidenz: [Antennenpositionen](/Users/schmidtm/openMotorBridge/hardware/cad/scad/01_main_box/99_overall_box.scad:88). Koordinaten und Schnittmaße stehen in der Prüfevidenz.

### S05 · P2 · Korrekturen der Beschreibung bleiben unvollständig

Die englische U12-Pintabelle ist jetzt auf HTSSOP-28 umgestellt und J6 an wichtigen Stellen auf Micro-Lock Plus korrigiert. Ein anderer englischer U12-Absatz nennt aber weiterhin **QFN-20**, und die alte J4-Pintabelle ist noch vorhanden. [Englischer alter U12-Absatz](/Users/schmidtm/openMotorBridge/docs/en/07_pcba_hardware_pinouts.md:135).

Die Puck-Bauhülle wird in neu korrigierten Abschnitten nun sauber mit 15/17,2/21,7 mm unterschieden. Der Mechanik-Eingangstext nennt noch den alten Dom auf 44×44-mm-Basis. Frühere Punkte bleiben ebenfalls offen: Front-Serviceport J7, sechs statt zwei physische Spiegel-Taster, PPS-Leitung, Keyfob USB-C/MAX17048/Lagenzahl und zugesagte Hub-Dongle-Abschaltung.

Beim Pod erklärt die Firmware weiterhin eine Status-LED an Pad 25 und einen Bay-Strap an Pad 26; beide Pads sind im PCB ohne Netz. `PIN_BAY_SELECT` wird tatsächlich zur Bay-Zuordnung gelesen. Einen physischen Strap oder eine alternative eindeutig implementierte Konfiguration ergänzen beziehungsweise die Zusage anpassen.

Die Qi-BOM-Lücke ist geschlossen, aber der Name `Qi_Coil_SolderPads_2P` belegt keine lötfreie JST-ACH-Buchse. Der Akkuanschluss bleibt Lötpads auf R_0805. Für den neuen Qi-Footprintnamen ist zudem keine gleichnamige `.kicad_mod` im Repository vorhanden; eingebettete PCB-Pads bleiben zwar exportierbar, die Bibliotheksquelle ist so nicht reproduzierbar mitgeliefert.

## Status H01–H22

| ID | Status | Kurzbegründung |
| --- | --- | --- |
| H01 | Teilweise | Reales IC und Pintabelle; feste Enables statt echter elektrischer Zweigsequenzierung. |
| H02 | Behoben | Ladepfad/ISET und Export weiterhin korrigiert. |
| H03 | Offen | USB-Werkstattversorgung erreicht weiter nicht die KL30-Satellitenzweige. |
| H04 | Behoben | Pod-3,3-V-Quelle vorhanden. |
| H05 | Behoben | Feste 5-V-Quelle vom PD-Ausgang getrennt. |
| H06 | Behoben | Analogschalter-Pins korrigiert. |
| H07 | Behoben | Die konkreten alten C6-Versorgungs-/Masse-/Enable-/USB-Pinfehler sind korrigiert; Firmware-Restfehler S02 separat. Keine vollständige Landpatternfreigabe. |
| H08 | Offen | Native C6 Audio Class weiterhin nicht durch den festen Serial/JTAG-Controller bereitgestellt. |
| H09 | Offen | P4-Wert wieder auf S3-Modulfootprint. S01. |
| H10 | Teilweise | Firmware-Pin-7-Angabe korrigiert, Front-Serviceport in Doku weiter falsch. |
| H11 | Behoben | Hub-3,3-V-Regler vorhanden. |
| H12 | Teilweise | Hubbeschreibung verbessert; Dongle-VBUS weiterhin gemeinsam versorgt. |
| H13 | Offen | Physisch zwei statt beschriebener sechs Spiegel-Taster. |
| H14 | Behoben | OPT3001-Pins korrigiert. |
| H15 | Offen | PPS nicht über Kabel ausgeführt. |
| H16 | Behoben | Keyfob-LDO mit GND/EN. |
| H17 | Teilweise | Qi in BOM und mit Footprintname; lötfreie Akku-/Qi-Steckermontage nicht umgesetzt. |
| H18 | Offen | Keyfob-Funktions-/Lagenwidersprüche unverändert. |
| H19 | Teilweise | USB und GPIO28 verbessert; Modulvariante, UART/LED und Recovery offen. |
| H20 | Behoben | Radar-Buck-Pins korrigiert. |
| H21 | Behoben | Früher leere LED-Funktion implementiert; erreichbarer Hardwarepin weiter S03. |
| H22 | Behoben | OMM-Fertigungsreferenzen konsistent. |

## Eigener Prüflauf und Grenzen

Erneut KiCad CLI 10.0.5, seriell, ERC mit allen Schweregraden und DRC mit Schaltplan-Parität. Gleiche separate Konfiguration wie zuvor. Projektregeln und ignorierte Checks gelten weiter.

| PCBA | ERC Fehler | ERC Warnungen | DRC / unverbunden / Parität |
| --- | ---: | ---: | --- |
| 01 | 5 | 170 | SIGABRT_no_result |
| 03 | 0 | 334 | SIGABRT_no_result |
| 05 | 0 | 526 | SIGABRT_no_result |
| 05B | 0 | 81 | 0/0/0 |
| 05C | 0 | 27 | 0/0/0 |
| 05D | 0 | 49 | SIGABRT_no_result |
| 07 | 82 | 201 | SIGABRT_no_result |
| 08 | 2 | 119 | SIGABRT_no_result |
| 09 | 28 | 67 | SIGABRT_no_result |
| 10 | 28 | 67 | SIGABRT_no_result |

Zwei DRC-Läufe sind unter den konfigurierten Regeln sauber; acht enden erneut mit SIGABRT ohne Ergebnis. **Die Commit-Zusagen „100 % geroutet“ und „0 Paritätsfehler“ kann ich mit meinem lokalen DRC deshalb nicht unabhängig bestätigen oder widerlegen.** Die ERC-Zahlen sind Werkzeugmeldungen, keine ebenso große Anzahl bewiesener realer Defekte. Der Hersteller-/GPIO-Abgleich oben ist davon unabhängig.

Bei Main wurde die minimale Kupfer-Kantenentfernung von 0,35 auf 0,275 mm reduziert, beim Keyfob wurden 0,1021 auf 0,1016 mm angepasst. Das ist nicht automatisch unzulässig; ein Vergleich alter/neuer DRC-Ergebnisse muss diese geänderten Prüfschwellen berücksichtigen und sie an den gewählten Fertigungsprozess binden.

Schaltplan-/PCB-Referenzen und Werte passen auf allen zehn Boards; BOM/CPL haben im geprüften Umfang keine Abweichungen. Durchgängige elektrische Funktion, thermische Reserven, reale Stromtragfähigkeit, Gerber-Geometrie und jedes einzelne Hersteller-Landpattern wurden nicht vollständig freigegeben. Kein Firmwarebuild oder Betrieb echter Elektronik. CAD-Prüfung anhand der Quellen, keine vollständige Bewegungssimulation. Projektdateien wurden nicht verändert.

Gespeichert: [Prüfevidenz JSON](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_Pruefevidenz_4938b26.json), [Inventar JSON](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_Platineninventar_4938b26.json), [KiCad-Reports ZIP](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_KiCad_Prueflauf_4938b26.zip).
