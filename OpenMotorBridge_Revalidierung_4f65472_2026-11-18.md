# OpenMotorBridge – Revalidierung `4f65472`

**18. November 2026, Vergleich mit `8724eff`; Arbeitsverzeichnis zu Beginn sauber.** Erneute Inventur und BOM-/CPL-Prüfung aller zehn aktiven Boards, direkte Herstellerprüfung der neu bestückten Keyfob-ICs, USB-Busversorgung, erweiterter S31-GPIO-Abgleich und Firmwareprüfung. Dokumente bleiben Prüfgegenstand.

**Ergebnis:** Der zuvor fehlende USB-Speisepfad und die Sensor-Reset-Kollision sind behoben. Die neue Keyfob-Version hat dagegen grundlegende falsche C3- und Qi-Pinzuordnungen. Bei Main und Front sind die zuletzt konkret beanstandeten I2C-GPIOs korrigiert, viele weitere S31-GPIOs bleiben falsch. D4 fehlt im Main-Fertigungsexport. Keine Gesamtfreigabe.

**H13 bleibt zurückgenommen.** Zwei Taster mit programmierbaren Einfach-/Doppel-/Langdruckgesten sind ausdrücklich die vorgesehene Bedienung.

## Bestätigte Korrekturen

- **USB-Energiepfad ergänzt:** D4 PMEG4050EP führt mit Anode Pin 2 an USBC_VBUS und Kathode Pin 1 an KL30_IN. Damit existiert jetzt ein vorgesehener Pfad `USB → D4 → KL30_IN → U12 → J6 → Satelliten`. Der alte Befund „USB erreicht die Satellitenversorgung nicht“ wird geschlossen. [main_box D4](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:4207). [Nexperia PMEG4050EP](https://assets.nexperia.com/documents/data-sheet/PMEG4050EP.pdf).
- **Sensor-Reset:** Front-J6 Pin 8 ist jetzt GNSS_RESET_N statt GND und passt zum Puck. Die bisherige Masse-/Reset-Kollision bei pinweisem Kabel ist behoben. Die Firmware-GPIO-Zuordnung ist eine getrennte Restfrage. [front_node J6](/Users/schmidtm/openMotorBridge/hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb:12998).
- **S31-I2C und RF:** Main und Front verwenden für I2C jetzt GPIO22/23 passend zu Modulpad 17/18. Main-ANT3 hängt jetzt tatsächlich am RF-Netz von U2 Pin 63. Die zuvor konkret fehlende Einspeisung ist ergänzt; die benötigte Modul-Antennenvariante und RF-Anpassung sind damit nicht praktisch geprüft. [main_box U2](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:4281).
- **OMM-Syntax:** Die überzählige Klammer ist entfernt; `is_vbus_present` liegt wieder innerhalb der Funktion. Der zuletzt konkret gemeldete Syntaxfehler ist geschlossen. Die weiter fest eingesetzten 80-/95-%-Akkuwerte bleiben ungemessene Platzhalter. [korrigierter OMM-Funktionsabschluss](/Users/schmidtm/openMotorBridge/firmware/omm_module/src/power_supervisor.cpp:35).
- **Alte Nordic-DEC-Befunde entfallen:** Der nRF52832 ist nicht mehr bestückt. Seine DEC1-/DEC4-Korrektur wird deshalb nicht weiter verlangt. Die neue C3-Version muss aber nach ihrem eigenen Pinplan geprüft werden, siehe V01.
- **Preflight-Exitstatus verbessert:** Das Skript sammelt jetzt Fehler und kann mit Exitcode 1 enden. Der alte unbedingte Erfolgscode ist behoben; Restprobleme stehen unter V07.
- **CAD:** Die frühere konkrete LoRa-/Träger-Kollisionsstelle bleibt ausgeräumt. Eine zusätzliche Stichprobe an drei Tray-STLs fand am alten Kollisionspunkt kein Material; ein Kontrollpunkt innerhalb des Bodens wurde als Material erkannt. Das ist keine vollständige Bewegungs- oder Kollisionsfreigabe.

## V01 · P1 · Neuer Keyfob-C3 ist nicht nach Herstellerpinplan angeschlossen

U1 ist jetzt ein ESP32-C3FH4 im QFN32. Die Zahl der Pads passt zur Bauteilfamilie, die elektrische Zuordnung aber nicht:

| Physischer Pin | Herstellerfunktion | Aktuelles PCB-Netz |
| --- | --- | --- |
| 1 | LNA_IN / RF | VCC_3V3 |
| 2 | VDD3P3 | VBAT |
| 3 | VDD3P3 | GND |
| 7 | CHIP_EN | BTN_SOS_N |
| 29 / 30 | XTAL_N / XTAL_P | beide ohne Netz |
| 31 / 32 | VDDA | beide ohne Netz |

Der 40-MHz-Quarz hängt stattdessen an Pads 14/15, also GPIO8/9. Die RF-Antenne hängt an Pad 23 statt am RF-Pin 1. Versorgung, Quarz und RF können so nicht die beschriebene Funktion erfüllen. Dies ist kein Layoutabstandsproblem und wird durch korrekte Schaltplan-/PCB-Parität nicht geheilt.

Auch das neue Firmwareprofil stimmt nicht mit der gespeicherten Verdrahtung überein. Es erwartet beispielsweise ARM an GPIO9/Pad15; dort hängt im PCB XTAL2, der ARM-Taster aber an Pad6/GPIO2. Die Firmware erwartet USB an Pads25/26; beide sind unbeschaltet, während J2 weiterhin an Pads18/19 hängt. Der ADC liest GPIO0/Pad4, das im PCB LORA_MISO führt; der behauptete 100k/100k-Akkuteiler ist nicht vorhanden.

**Erforderlich:** Das gesamte reale C3-Symbol einschließlich Versorgungs-, Takt-, Flash-, RF- und Enable-Pins übernehmen und anschließend das GPIO-Profil gemeinsam mit dem PCB daraus ableiten. Die aktuelle Firmware-PAD-Konfiguration allein ist kein Nachweis der Verdrahtung.

Evidenz: [smart_keyfob U1](/Users/schmidtm/openMotorBridge/hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb:2441), [smart_keyfob J2](/Users/schmidtm/openMotorBridge/hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb:844), [Keyfob-Pinprofil](/Users/schmidtm/openMotorBridge/firmware/smart_keyfob/src/keyfob_config.h:16). Hersteller: [Espressif ESP32-C3, Tabellen 2-1 und 2-8](https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf).

## V02 · P1 · Neuer BQ51050B-Lader hat grundlegende Pinvertauschungen

U4 wurde auf BQ51050BRHLR umgestellt. Für das ausgewählte RHL20-Gehäuse ergeben sich unter anderem:

| Pin | TI-Funktion | PCB-Netz |
| --- | --- | --- |
| 1 | PGND | VBAT |
| 3 | BOOT1 | QI_AC1 |
| 4 | BAT | QI_AC2 |
| 7 | CHG | ohne Netz |
| 17 | BOOT2 | GND |
| 18 | RECT | GND |
| 19 | AC2 | GND |

Damit liegt der Akku am realen Massepin und der tatsächliche Batterieausgang an einer Spulenleitung. Auch erforderliche Bootstrap-, Gleichrichter-, Kommunikations- und Einstellbeschaltung ist nicht als vollständige Referenzschaltung vorhanden. Die Direktladefähigkeit des gewählten ICs ersetzt diese Anschlüsse nicht.

**Erforderlich:** Den vollständigen TI-RHL20-Pinplan und die Referenzapplikation übernehmen, bevor dieses Design bestückt wird. Einzelne Netznamen umzubenennen reicht nicht.

Evidenz: [smart_keyfob U4](/Users/schmidtm/openMotorBridge/hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb:5632). Hersteller: [TI BQ51050B, Pin Configuration and Functions](https://www.ti.com/lit/ds/symlink/bq51050b.pdf).

## V03 · P1 · S31-Abgleich erweitert: viele GPIOs bleiben nach altem Profil belegt

Die vier zuvor konkret beanstandeten I2C-GPIOs sind korrigiert. Um weitere Einzelkorrektur-Schleifen zu vermeiden, wurde der Abgleich auf **54 explizit zugeordnete Headerkonstanten** beider S31-Boards erweitert. **5 stimmen mit dem tatsächlichen Modulpad überein, 49 weichen ab.** Das ist eine Quellen-/Pinprofilprüfung; nicht jede Konstante wird in jedem Betriebsmodus benutzt.

Beispiele:

| Funktion | Gespeichertes Modulpad → S31-GPIO | Firmware-GPIO |
| --- | --- | --- |
| Main LoRa-SCK | 4 → 2 | 12 |
| Main I2S-MCLK | 12 → 35 | 0 |
| Main SD-CLK | 35 → 55 | 35 |
| Front GNSS_RESET_N | 11 → 7 | 11 |
| Front Mikrofon DATA | 12 → 35 | 12 |
| Front E22_EN | 36 → 59 | 40 |

Mehrere davon werden direkt in den Treibern verwendet, etwa Main-LoRa-SCK, Main-I2S-MCLK und Front-E22_EN. Der neue Reset-Header enthält zudem eine Kollision in den Defines: GNSS_RESET_N und WS2812B_DIN werden beide als GPIO11 deklariert, obwohl sie an verschiedenen Modul-GPIOs liegen.

**Die vollständige korrigierbare Arbeitsliste liegt als TSV und JSON bei.** Beide Firmwareziele stehen weiterhin auf esp32s3; das ist kein Produktionsbuild für den RISC-V-S31. Ein S3-Referenzaufbau muss als eigener Stand erkennbar bleiben.

Evidenz: [Main-Pinprofil](/Users/schmidtm/openMotorBridge/firmware/main_controller/src/main_box_config.h:78), [Front-Pinprofil](/Users/schmidtm/openMotorBridge/firmware/front_node/src/front_node_config.h:51). Hersteller: [S31-WROOM-1/1U, Tabelle 3-2](https://documentation.espressif.com/esp32-s31-wroom-1_wroom-1u_datasheet_en.html). Die 64 Padnummern sind vorhanden; der frühere Padzahlvorwurf wird nicht wiederholt.

## V04 · P1 · D4 fehlt im Main-Fertigungspaket

Die für die neue USB-Busversorgung entscheidende D4 ist im Main-PCB und Schaltplan vorhanden, aber **weder in der aktuellen Main-BOM noch in der CPL enthalten**. Eine Bestellung ausschließlich nach diesen Dateien würde die gerade ergänzte Verbindung daher nicht bestücken.

**Erforderlich:** Main-BOM/CPL aus demselben aktuellen Board neu exportieren und die übrigen Fertigungsdaten auf denselben Stand bringen. Eine beabsichtigte Handbestückung müsste ausdrücklich ausgewiesen werden.

Evidenz: [main_box D4](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:4207), [Main-BOM](/Users/schmidtm/openMotorBridge/hardware/production_packages/01_main_box_pcba/01_main_box_pcba_bom_jlcpcb.csv:1), [Main-CPL](/Users/schmidtm/openMotorBridge/hardware/production_packages/01_main_box_pcba/01_main_box_pcba_cpl_jlcpcb.csv:1). Die übrigen neun BOM-/CPL-Pakete stimmen im ausgewerteten Referenz-/Wert-/Positionsumfang mit den Boards überein.

## V05 · P2 · USB-Pfad vorhanden, Spannungsreserve noch nicht nachgewiesen

Die Nutzervorgabe bleibt: Alle eingebauten Platinen sollen über die zentrale USB-Einspeisung starten, ohne zusätzliche Verbraucher an Front oder Hub. **Dafür ist der vorher fehlende Pfad nun vorhanden.** Die verbleibende Frage ist die garantierte Spannung an den lokalen Reglern:

- D4 und U12 verursachen einen lastabhängigen Spannungsabfall; die Satelliten erhalten deshalb weniger als die USB-Eingangsspannung.
- Front, Pod und Radar verwenden lokale TPS54302-Abwärtswandler für ihre 5-V-Schienen. Ein Abwärtswandler kann aus einer niedrigeren Eingangsspannung keine geregelten 5 V herstellen.
- TI spezifiziert den TPS54302 ab 4,5 V Eingang. Untere USB-Spannung, Diodenabfall, Leitungen und Einschaltstrom müssen gemeinsam in dieses Budget passen. Als reines Rechenbeispiel ergeben 4,75 V Eingang minus angenommene 0,30 V bereits 4,45 V vor weiteren Verlusten; dies ist kein gemessener Wert und keine bauteilgenaue Worst-Case-Rechnung.

**Bewertung:** Der alte Topologiefehler ist geschlossen. Ein zuverlässiger Systemstart und die Versorgung aller als aktiv zugesagten internen 5-V-Verbraucher sind dadurch noch nicht bestätigt. Die konkrete Mindestspannung und der Anlauf müssen für die erlaubte Werkstattkonfiguration ausgelegt werden; eine ausreichende Wattzahl allein genügt dafür nicht.

Quellen: [TI TPS54302](https://www.ti.com/lit/ds/symlink/tps54302.pdf), [TI TPS4H160-Q1, 3,4-V-Untergrenze](https://www.ti.com/lit/ds/symlink/tps4h160-q1.pdf). Dem TPS4H160 wird hier keine fälschliche 8-V-Mindestversorgung unterstellt.

## V06 · P2 · BMP390-Rohdruck wird ohne notwendige Kompensation als Pa ausgegeben

Ein BMP390-Pollpfad ist jetzt vorhanden. Die Funktion liest allerdings nur drei Rohdruckbytes und setzt `m_baro_pressure_pa = raw_press / 256`. Die BMP390-Rohwerte benötigen Temperatur- und Druckkompensation mit den werksseitigen NVM-Kalibrierkoeffizienten; es handelt sich nicht um bereits kalibrierte 1/256-Pa-Werte.

Schon der Zahlenbereich zeigt das Problem: Ein 24-Bit-Wert geteilt durch 256 erreicht höchstens 65.535 Pa und damit nicht einmal den normalen Referenzwert 101.325 Pa. Ein bloßer erfolgreicher I2C-Lesezugriff bestätigt daher keine korrekte Druck-/Höhenausgabe.

**Erforderlich:** Temperatur und Kalibrierdaten lesen und die Bosch-Kompensation bzw. den Hersteller-Sensortreiber verwenden. Evidenz: [BMP390-Auswertung](/Users/schmidtm/openMotorBridge/firmware/front_node/src/front_sensor_hub.cpp:166). Hersteller: [Bosch BMP390, Abschnitt 3.11 und Anhang 8.5/8.6](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmp390-ds002.pdf).

## V07 · P2 · Preflight-Fehlerstatus verbessert, falsche Pinmodelle und Ausführungsfehler bleiben

Das projektspezifische Skript kann jetzt bei gezählten Fehlern fehlschlagen. Zwei wesentliche Grenzen bleiben:

1. Der neue C3-Prüfzweig hält Pads18/19 für USB und Pad11 für GPIO9. Der tatsächliche C3-Plan nennt USB25/26 und GPIO9 an Pad15. Damit bestätigt die Prüfung gerade Teile derselben falschen Zuordnung wie im neuen PCB.
2. Wenn DRC keinen JSON-Report erzeugt, liefert `run_drc()` nur ein `error`-Feld. `audit_board()` prüft anschließend aber fehlende Fehlerzähler mit Default 0 und kann daraus „DRC Errors: 0“ und „100% Routed“ ausgeben. Ein Ausführungsfehler muss als fehlgeschlagene oder unbestätigte Prüfung gezählt werden.

Das betrifft das Zusatzskript, nicht die KiCad-Prüfengine. Es wurde hier quellengeprüft und nicht ausgeführt. Evidenz: [C3-Prüfzweig](/Users/schmidtm/openMotorBridge/tools/audit_pcbas_preflight.py:347), [Preflight-DRC-Fehlerbehandlung](/Users/schmidtm/openMotorBridge/tools/audit_pcbas_preflight.py:199).

## Audio- und übriger Dokumentationsstatus

Die Texte wurden an mehreren Stellen von „native C6 UAC“ auf ES8388-Codec plus CDC/DFU geändert. Die zurückgenommene Behauptung wird nicht als unverändert weitergeführt. Ein lokaler I2S-Codec stellt jedoch allein keinen USB-Audiotransport zwischen zwei Boards her; der weiterhin behauptete digitale Ende-zu-Ende-Audiopfad und seine Latenz bleiben separat nachzuweisen. Die aktuelle Änderung ist insoweit eine Präzisierung der Architektur, noch keine von diesem Review bestätigte Audiofunktion.

Die übrigen historischen Befunde gelten nur in ihrem jeweils zuletzt bestätigten Umfang. Insbesondere entfallen die nicht mehr bestückten Nordic-Pinanforderungen, H13 bleibt zurückgenommen und die USB-Speiseverbindung wird ausdrücklich als korrigiert geführt.

## KiCad-Prüflauf und Grenzen

Erneut KiCad CLI 10.0.5, zehn Boards seriell; ERC mit allen Schweregraden und DRC mit Schaltplan-Parität. Projektregeln und ignorierte Checks gelten weiter.

| PCBA | ERC Fehler | ERC Warnungen | DRC / unverbunden / Parität |
| --- | ---: | ---: | --- |
| 01 | 6 | 185 | SIGABRT_no_result |
| 03 | 0 | 334 | SIGABRT_no_result |
| 05 | 0 | 528 | SIGABRT_no_result |
| 05B | 0 | 69 | 0/0/0 |
| 05C | 0 | 27 | 0/0/0 |
| 05D | 1 | 55 | SIGABRT_no_result |
| 07 | 20 | 172 | SIGABRT_no_result |
| 08 | 2 | 119 | SIGABRT_no_result |
| 09 | 28 | 67 | SIGABRT_no_result |
| 10 | 28 | 67 | SIGABRT_no_result |

Hub und Spiegel-Pod sind unter den konfigurierten Regeln sauber. Acht DRC-Läufe enden weiterhin lokal mit SIGABRT ohne Ergebnis. Dies wird nicht als Hardwarefehler oder bestandene Prüfung gezählt. ERC-Zahlen sind Werkzeugmeldungen, keine ebenso große Anzahl bewiesener Defekte. Die direkten Hersteller-Pinbefunde sind davon unabhängig.

Schaltplan-/PCB-Referenzen und Bauteilwerte stimmen auf allen zehn Boards überein. Fertigungsabgleich: D4 fehlt bei Main, übrige ausgewertete Werte/Footprintnamen und CPL-Koordinaten/Drehungen passen. Keine vollständige Gerber-, Signal-, Thermik-, Hersteller-Landpattern- oder Firmwarebuild-Freigabe. Keine real elektrisch betriebenen Boards und keine vollständige Gehäuse-Bewegungsprüfung. Projektdateien wurden nicht verändert.

Begleitdateien: [S31-GPIO-Arbeitsliste TSV](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_S31_GPIO_Abgleich_4f65472.tsv), [Prüfevidenz JSON](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_Pruefevidenz_4f65472.json), [Inventar JSON](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_Platineninventar_4f65472.json), [KiCad-Reports ZIP](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_KiCad_Prueflauf_4f65472.zip).
