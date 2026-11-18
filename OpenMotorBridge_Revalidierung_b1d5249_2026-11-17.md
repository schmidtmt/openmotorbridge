# OpenMotorBridge – Revalidierung `b1d5249`

**17. November 2026, Vergleich mit `4938b26`.** Das Repository war zu Beginn sauber. Alle zehn aktiven Platinen wurden erneut inventarisiert und mit ihren BOM-/CPL-Dateien verglichen. Schwerpunkt: neue S31-Umstellung, korrigierte OMM-/Radar-GPIOs, entfernte Firmwaredefinitionen und neue Antennentopologie. Die Dokumentation wurde als Prüfgegenstand behandelt.

**Die zuvor beanstandeten OMM-/Radar-GPIO-Beispiele sind jetzt korrigiert. Dafür bleiben ein schwerer S31-Modulkonflikt an Main und Front sowie zwei neue quellseitige Build-Blocker.** Der Antennenabstand zwischen den Dummy-Körpern ist verbessert; eine Überschneidung mit dem Träger verbleibt. Aus dem aktuellen Stand folgt weiterhin keine Gesamtfreigabe.

## Bestätigte Korrekturen

- Die unabhängigen **13 OMM-/Radar-GPIO-Beispielprüfungen bestehen jetzt vollständig**: OMM-I2C, Status-LED und SA818-PTT auf beiden Varianten; Radar RX/TX, Halo und USB. Das schließt die konkreten letzten S02-/S03-GPIO-Beispiele. [korrigierte OMM-GPIOs](/Users/schmidtm/openMotorBridge/firmware/omm_module/src/omm_module_config.h:29), [korrigierte Radar-GPIOs](/Users/schmidtm/openMotorBridge/firmware/radar_submcu/src/main.cpp:26).
- Radar-Boot wurde von GPIO9 auf den GPIO28-Pfad mit Pull-up und Taster nach GND verlegt. Die weitere Strapping-/Recovery-Funktion ist nicht am Gerät geprüft.
- Der Qi-Footprint ist jetzt als Bibliotheksdatei mitgeliefert. Seine BOM-/CPL-Einträge bleiben vorhanden.
- Die getrennten LoRa-/Helmaudio-Antennen-Dummys überschneiden sich nicht mehr gegenseitig: LoRa Z=19,0…19,8 mm, Helmaudio Z=20,2…20,7 mm, **0,4 mm Abstand**. Dies schließt die alte reine Körper-gegen-Körper-Überschneidung, nicht die nachstehende Trägerkollision.
- Die vieradrige Akkuverkabelung und die Triple-Antennen-Darstellung wurden in CAD-Dummy, Bildunterschrift und neuen Main-Renderbildern nachgeführt. Die neue Explosionsansicht wurde angesehen.
- Auf allen zehn Boards passen die geprüften Schaltplan-/PCB-Referenzen und Bauteilwerte. BOM-Werte und Footprintnamen stimmen mit den Boards überein; keine bestückbare Referenz fehlt. CPL-Positionen und Drehungen passen ebenfalls. Das bestätigt den Exportabgleich, nicht die Herstellerkompatibilität der zugrunde liegenden Footprints.

## T01 · P1 · S31 auf Main und Front benötigt ein anderes Landpattern und Pinprofil

Front U1 heißt jetzt ESP32-S31-WROOM-1U statt P4. Main U2 verwendete diesen S31-Wert bereits zuvor. **Beide Boards enthalten weiterhin einen S3-WROOM-Footprint mit nur 41 verschiedenen Padnummern.** Der direkte Abgleich mit dem aktuellen Espressif-Moduldatenblatt ergibt:

| Merkmal | Reales S31-WROOM-1U | Aktueller Entwurf |
| --- | --- | --- |
| Anschlusszahl | 64 | 41 |
| HS-USB | Pins 54/55 | USB-Netze an 13/14; 54/55 fehlen |
| Pin 40 | GND | Main: BLE_RF_2G4; Front: E22_EN |
| Zusätzlicher RF-Anschluss | ANT2 an Pin 63 | Pin 63 fehlt |

Der S31 ist als Bauteil real und bietet die gewünschten Funktionen. **Die Annahme eines unverändert verwendbaren S3-Pinplans ist aber falsch.** Insbesondere speist die neue Johanson-Antenne ANT3 im Main-Netzplan aus einem realen Massepin statt einem RF-Anschluss. Das lässt sich nicht durch einen neuen Netznamen oder ein Renderbild beheben. Die Pins 13/14 sind beim S31 GPIO33/34 mit USB-Serial/JTAG-Funktion; sie belegen nicht den zugesagten HS-OTG-Pfad.

**Erforderlich:** Für Main und Front das Hersteller-Landpattern einschließlich zusätzlicher Unterseitenpads übernehmen und alle Netze/GPIOs neu zuordnen. Die tatsächliche Antennenvariante separat festlegen; der Modulhersteller kennzeichnet ANT2 als standardmäßig deaktiviert. S31-Bestellvariante und RF-Ausführung müssen dazu passen.

Dieser neue gezielte Herstellerabgleich erweitert den bisherigen Front-Befund ausdrücklich auf **Main U2**; die früheren Reviews hatten diesen Main-Modulpinplan nicht vollständig validiert.

Evidenz: [main_box U2](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:4489), [front_node U1](/Users/schmidtm/openMotorBridge/hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb:6333), [main_box ANT3](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:7167), [Main-Antennenannahme](/Users/schmidtm/openMotorBridge/firmware/main_controller/src/main_box_config.h:95). Hersteller: [Espressif S31-WROOM-1/1U, Tabelle 3-2](https://documentation.espressif.com/esp32-s31-wroom-1_wroom-1u_datasheet_en.html).

**Separater Buildzielkonflikt:** Main und Front stehen weiterhin auf `esp32s3`. Der S31 ist eine RISC-V-Plattform; ein S3-Build ist kein Produktionsbuild für diesen Chip. Ein beabsichtigter S3-Referenzaufbau muss als eigener Hardwarestand behandelt werden. [Main-Buildziel](/Users/schmidtm/openMotorBridge/firmware/main_controller/sdkconfig.defaults:2), [Front-Buildziel](/Users/schmidtm/openMotorBridge/firmware/front_node/sdkconfig.defaults:2).

## T02 · P1 · Entfernte Definitionen werden in mitgebauten Firmwaredateien weiter verwendet

Zwei konkrete Regressionen seit dem letzten Review:

| Entfernte Konstante | Weiterverwendung |
| --- | --- |
| PIN_CARTRIDGE_LED | cartridge_mechatronics.cpp: GPIO-Maske, Initialisierung und Statusausgabe |
| OMM_ADC_BAT_CHANNEL | power_supervisor.cpp: ADC-Konfiguration und ADC-Lesen |

Eine Definition wurde im Firmwarebaum nicht gefunden. Die beiden `.cpp`-Dateien stehen weiterhin ausdrücklich in den jeweiligen `idf_component_register(SRCS …)`-Listen. Damit sind diese Bezeichner im normalen Komponentenbuild unaufgelöst.

Die beabsichtigte Korrektur ist nachvollziehbar: Der Pod besitzt keine angeschlossene Status-LED, und OMM soll den Ladezustand über das Statussignal statt über eine nicht ausgeführte ADC-Leitung behandeln. **Dafür müssen aber auch die aufrufenden Implementierungen angepasst werden.** Bloßes Entfernen der Headerdefinition erzeugt keinen konsistenten Build.

Evidenz: [weiter verwendete Pod-LED-Konstante](/Users/schmidtm/openMotorBridge/firmware/smart_cartridge/src/cartridge_mechatronics.cpp:33), [neue Pod-Konfiguration](/Users/schmidtm/openMotorBridge/firmware/smart_cartridge/src/cartridge_config.h:32), [weiter verwendete ADC-Konstante](/Users/schmidtm/openMotorBridge/firmware/omm_module/src/power_supervisor.cpp:34). Dies ist ein quellseitiger Build-Blocker-Nachweis; ein vollständiger ESP-IDF-Build wurde in diesem Durchgang nicht ausgeführt.

## T03 · P1 · Beide identischen Pods werden weiterhin als Bay 1 initialisiert

Der alte unverdrahtete Bay-Strap wird nicht mehr gelesen. Stattdessen gibt `detect_bay_and_mode()` nun aber **immer USB_NODE_POD_BAY1 zurück**. Der Kommentar und Header sprechen von NVS-/USB-Port-Zuordnung; eine entsprechende Lade-/Zuweisungsimplementierung ist im Pod-Quellbaum nicht vorhanden. Auch `CARTRIDGE_DEFAULT_BAY_ID` wird dort nicht ausgewertet.

Mit derselben Firmware auf beiden baugleichen Pod-Platinen werden folglich beide zunächst als linke Bay 1 und mit dem entsprechenden Hubport initialisiert. Die zweite Instanz ist so nicht wie beschrieben unterscheidbar.

**Erforderlich:** Die reale Portzuweisung durch den Host oder eine gespeicherte Bay-Konfiguration tatsächlich implementieren und vor der Initialisierung des jeweiligen Busknotens anwenden. Evidenz: [fest zurückgegebene Bay 1](/Users/schmidtm/openMotorBridge/firmware/smart_cartridge/src/main.cpp:54), [neue Pod-Konfiguration](/Users/schmidtm/openMotorBridge/firmware/smart_cartridge/src/cartridge_config.h:32).

## T04 · P2 · LoRa-Dummy überschneidet weiterhin die erhöhte Trägerfläche

Die obere Antenne wurde angehoben und ihr Träger erhöht. Zwischen den Antennenkörpern ist jetzt Luft. Unter der oberen Antenne bleibt aber im Bereich der LoRa-Antenne Material stehen:

- Trägerkörper beginnt global bei Z=19,0 mm und reicht bis 20,2 mm.
- Die untere LoRa-Ausnehmung endet bei Z=19,6 mm.
- Die obere Antennenausnehmung beginnt erst bei Z=19,8 mm.
- Die LoRa-Antenne selbst reicht bis Z=19,8 mm.

Damit verbleibt dort **Z=19,6…19,8 mm Trägermaterial innerhalb des LoRa-Dummys**. Als konkrete, von der Koax-Durchführung unberührte Nachweisbox liegt X=31…40 mm, Y=66…67 mm, Z=19,65…19,75 mm sowohl im Dummy als auch im nach den Subtraktionen verbleibenden Träger.

**Erforderlich:** Die LoRa-Ausnehmung an die tatsächliche Antennenlage und den angehobenen Träger anpassen oder den gesamten Schichtaufbau konsistent verschieben. Der neue Abstand der beiden Antennen allein schließt diesen anderen Kollisionspfad nicht.

Evidenz: [Träger und Aussparungen](/Users/schmidtm/openMotorBridge/hardware/cad/scad/01_main_box/parts/010_slide_tray.scad:107), [Antennenpositionen](/Users/schmidtm/openMotorBridge/hardware/cad/scad/01_main_box/99_overall_box.scad:90). Analytischer Nachweis anhand der SCAD-Körper, keine erfolgreiche OpenSCAD-CSG-Schnittrechnung und keine RF-Messung. Die frühere lokale OpenSCAD-Ausführungsgrenze bleibt bestehen.

## T05 · P2 · Neue Radar-Footprintbibliothek noch nicht vollständig ins Board übernommen

Die neu mitgelieferte C5-WROOM-1U-Bibliotheksdatei enthält jetzt auch Pads 30/31/32. **Der im Radar-PCB gespeicherte U1-Footprint hat weiterhin nur Pads 1–29.** Die Verbesserung der Bibliothek ist real, die Übernahme in das Board bleibt offen. Der veraltete Beschreibungstext der Bibliothek nennt ebenfalls noch „29-pad genuine module footprint“.

Evidenz: [radar_submcu U1](/Users/schmidtm/openMotorBridge/hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb:10907), [neue C5-Bibliothek](/Users/schmidtm/openMotorBridge/hardware/openmotorbridge.pretty/ESP32-C5-WROOM-1U.kicad_mod:312). Bibliotheksfootprint und platzierte PCB-Instanz synchronisieren, dann Pin-/Geometrie- und Paritätsprüfung erneut ausführen. Die bereits korrigierten USB-/UART-/LED-Zuordnungen werden dadurch nicht wieder als falsch eingestuft.

## Weitere bestehende Punkte und Dokumentationsstatus

Die bisherigen konkreten OMM-/Radar-GPIO-Restfehler sind geschlossen; die Front-Umstellung ist wegen T01 weiterhin offen. Der frühere Qi-Bibliotheksmangel ist geschlossen; die zugesagte lötfreie Akku-/Qi-Montage bleibt eine andere Frage, da weiterhin Lötpads verwendet werden.

Unverändert nicht vollständig umgesetzt bzw. nachgewiesen bleiben: USB-Werkstattversorgung aller Satelliten, echte elektrische Zweigabschaltung, native C6 USB Audio Class, selektives Hub-Dongle-VBUS, PPS-Kabelpfad und widersprüchliche Keyfob-Funktionen/Lagenangaben. Die Firmwarematrix nennt weiter sechs Spiegel-Taster, obwohl zwei physische Taster vorhanden sind; die Radar-GPIO-Zusammenfassung dort enthält noch alte Zahlen. Die vollständige frühere Statusliste gilt mit diesen konkretisierten Änderungen weiter; die Zahl geschlossener Altfunde ist keine Gesamtfreigabe.

Die zwischen den Commits auf 0 Byte verkleinerte Datei `pod_poka_yoke_cross_section_cad.png` wird in den durchsuchten Dokumenten nicht referenziert und wurde deshalb nicht als defektes aktives Dokumentbild gezählt.

## Eigener KiCad-Prüflauf und Grenzen

Erneut KiCad CLI 10.0.5, alle zehn Boards seriell, ERC mit allen Schweregraden und DRC mit Schaltplan-Parität. Projektregeln und ignorierte Checks gelten weiter.

| PCBA | ERC Fehler | ERC Warnungen | DRC / unverbunden / Parität |
| --- | ---: | ---: | --- |
| 01 | 6 | 176 | SIGABRT_no_result |
| 03 | 0 | 334 | SIGABRT_no_result |
| 05 | 0 | 526 | SIGABRT_no_result |
| 05B | 0 | 81 | 0/0/0 |
| 05C | 0 | 27 | 0/0/0 |
| 05D | 0 | 49 | SIGABRT_no_result |
| 07 | 82 | 201 | SIGABRT_no_result |
| 08 | 3 | 120 | SIGABRT_no_result |
| 09 | 28 | 67 | SIGABRT_no_result |
| 10 | 28 | 67 | SIGABRT_no_result |

Hub und Spiegel-Pod sind unter den konfigurierten Regeln sauber. Acht DRC-Läufe brechen weiterhin lokal mit SIGABRT ab; diese Ergebnisse bleiben unbestätigt. ERC-Meldungen werden nicht als ebenso viele reale Defekte gezählt. Die separat belegten Herstellerpin-, Quellcode- und CAD-Befunde hängen nicht vom Erfolg dieser DRC-Läufe ab.

BOM/CPL-Abgleich über alle zehn Boards ohne Abweichung im geprüften Umfang. Keine vollständige Gerber-, Thermik-, Signal- oder Stromtragfähigkeitsfreigabe; kein vollständiger Firmwarebuild, keine elektrisch betriebenen Boards und keine vollständige Gehäuse-Bewegungsprüfung. Die Projektdateien wurden nicht verändert.

Begleitdateien: [Prüfevidenz JSON](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_Pruefevidenz_b1d5249.json), [Platineninventar JSON](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_Platineninventar_b1d5249.json), [KiCad-Reports ZIP](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_KiCad_Prueflauf_b1d5249.zip).
