# OpenMotorBridge Revalidierung des Dokumentationsreviews

Stand: 14. November 2026, Commit `b4fc629`. Vergleich mit den 19 Befunden des ersten Reviews auf Basis von `13ab023` und dem damaligen Arbeitsverzeichnis. Im aktuellen Repository ist ausschließlich die hineinkopierte ursprüngliche Reviewdatei unversioniert; die geprüften Änderungen sind eingecheckt.

**Ergebnis: 8 Befunde im ursprünglichen Kern behoben, 9 teilweise behoben, 2 weiterhin offen.** Das ist eine Prüfung von Dokumentation, Quelltext und vorhandenen Exporten, keine Freigabe für Fertigung oder Fahrzeugbetrieb. „Behoben“ bezieht sich auf den beschriebenen Einzelbefund und bedeutet keine vollständige Funktions- oder Kollisionsprüfung der Baugruppe.

## Status der bisherigen Befunde

| ID | Befund | Ergebnis | Aktueller Stand |
| --- | --- | --- | --- |
| A01 | MCU und Buildziele | Offen | Neue Targetmatrix nennt P4-Hardware, setzt dafür aber weiterhin `esp32s3`. Der Widerspruch wurde tabelliert, nicht technisch aufgelöst. |
| A02 | USB Serviceversorgung und PD | Teilweise behoben | Kapitel 05 und die Bauanleitung trennen 5-V-Service und 12-V-Hochlastbetrieb. Kapitel 09 beschreibt weiterhin LM5050 und 5–20-V-PD-Sink. |
| A03 | Ringspeicher und Integrität | Teilweise behoben | Mounten, Speicherabfrage und Löschen sind jetzt implementiert. Die zugesagte Signatur und die Crash-Anbindung bleiben problematisch. |
| A04 | WebDAV nur simuliert | Teilweise behoben | Reale MKCOL-/PUT-Aufrufe ersetzen die Wartezeit. Eine aktivierte Uplink-Verbindung und robuste Übertragung sind weiterhin nicht belegt. |
| A05 | Partitionen und Flashanleitung | Teilweise behoben | Main-Partitionstabelle und passende Offsets sind vorhanden. Der neue Image-Befehl liest aus einem nicht vorhandenen Verzeichnis. |
| A06 | Verifikation des alten UWB-Modells | Teilweise behoben | Das konkrete Python-Modell ist auf v10/USB umgestellt und läuft erfolgreich. Es führt aber weiterhin keine physische HIL-Prüfung durch. |
| A07 | Fehlender Front-Zwischenboden | Behoben | Der veraltete Zwischenboden ist aus der betreffenden Bauteilliste entfernt. Der erneute lokale Linkcheck findet keine fehlenden Dateiziele. |
| B01 | Podbilder ohne L-Deckel | Behoben | Die neuen Podbilder zeigen den vertikalen hinteren Schenkel und die farbigen Krallen. Die Frage nach dem realen Einbauweg bleibt unter B02 offen. |
| B02 | Nicht erklärter Einschubweg | Offen | Die Explosionen zeigen weiterhin vertikale Versätze. Eine vollständige Darstellung oder Prüfung des horizontalen Montagewegs fehlt. |
| B03 | Abgeschnittenes Schlossbild | Behoben | Die neue Ansicht zeigt U-Bügel, Krallen, Heckwand und Antennenbereich. Der Hub steht nun auch im Deckelmodell auf 3,2 mm. |
| B04 | Alte DTM-12-Schnittzeichnung | Behoben | Das Bild nennt nun DTM-6, J6 mit 16 Pins, Slide-in-Tray und L-Deckel. Seine Genauigkeit als CAD-Schnitt ist damit nicht automatisch nachgewiesen. |
| B05 | Falscher seitlicher Deckelversatz | Behoben | Der Einbauversatz verwendet jetzt die 63,8-mm-Deckelbreite und ergibt Y=3,1 mm. Ein weiterer rechnerischer Kontaktverdacht in Z steht unten als C01. |
| B06 | Bodenverschraubung statt Wandführung | Teilweise behoben | Die Montage beschreibt jetzt wandgeführte Traversen und DIN 7991. Die Einkaufsliste enthält weiterhin DIN 912 für deren Klemmung. |
| B07 | Widersprüchliche Dry-Flap-Mechanik | Teilweise behoben | Die neue Montage beschreibt das Auflegen von oben. Die Exporttabelle nennt weiter einen einschiebbaren Rail-1-Tray; Englisch enthält weiterhin eine federbelastete Klappe. |
| B08 | Alte Dockkabel und Portlagen | Behoben | Die zuvor beanstandeten GSA-/Transition-Dockstellen und Kofferdeckel-Bildbeschreibung sind auf Vierdraht-Bus und die neue Portlage umgestellt. Die reale Kabelpassung ist separat zu prüfen. |
| B09 | Falsche Pod-Innenmaße | Teilweise behoben | 141 × 61 mm am Boden ist jetzt genannt. Die alten 145 × 65 mm stehen noch in einer Bildunterschrift; die neu genannten oberen Einbauräume sind im Ausschnitt nicht nachvollziehbar. |
| B10 | Unterschiedliche Front-Node-Maße | Behoben | Die drei zuvor beanstandeten Stellen nennen nun 98 × 68 × 22 mm. |
| B11 | Hubports und Gehäusemaße | Teilweise behoben | Fünf USB-C-Ports sind jetzt klar benannt, aber ihre Zuordnung widerspricht zwischen CAD und Kapiteln. Die neuen Außenmaße widersprechen auch der STL. |
| B12 | Sena digital und mechatronischer Start | Behoben | Der Text trennt jetzt Kaltstart per Aktuator und laufende digitale Bedienung. Die behauptete OEM-Steuerbarkeit selbst wurde dabei nicht extern verifiziert. |

## Verbleibende wesentliche Probleme

### A01 Targetmatrix löst den Controllerwechsel nicht auf

Die [neue Matrix](/Users/schmidtm/openMotorBridge/firmware/README.md:14) nennt einen ESP32-P4 als physischen Front-Controller und `esp32s3` als „Host-Build“. Die [Front-Konfiguration](/Users/schmidtm/openMotorBridge/firmware/front_node/sdkconfig.defaults:2) setzt weiterhin `esp32s3`.

Espressif beschreibt für P4 ausdrücklich `idf.py set-target esp32p4`, auch in der zur Anleitung passenden Version [ESP-IDF v5.5](https://docs.espressif.com/projects/esp-idf/en/v5.5/esp32p4/get-started/linux-macos-setup.html). Ein S3-Build ist damit keine ausreichende Erklärung für eine auf P4 lauffähige Firmware. Falls es bewusst einen S3-Entwicklungsstand gibt, muss die Matrix diesen als separaten Entwicklungsstand kennzeichnen und einen P4-Build mit passender Konfiguration ausweisen.

### A02 Versorgungskonzept ist noch nicht in allen Kapiteln bereinigt

[Kapitel 05](/Users/schmidtm/openMotorBridge/docs/de/05_power_management_ups.md:62) beschreibt den reinen 5-V-Servicebetrieb mit LM66100 und inaktiven Hochlastzweigen nachvollziehbar. [Kapitel 09](/Users/schmidtm/openMotorBridge/docs/de/09_firmware_architecture.md:111) beschreibt weiterhin LM5050 und einen 5–20-V-USB-PD-Sink. Die zugehörige Tasktabelle nennt ebenfalls noch LM5050.

Beide Kapitel müssen dieselbe freigegebene Eingangsschaltung beschreiben. Die neue Behauptung, alle Satelliten ließen sich allein aus dem 5-V-Serviceeingang versorgen, benötigt zusätzlich einen nachvollziehbaren Strompfad zu deren Logik; sie folgt nicht allein aus einem gemeinsamen USB-Datenbus.

Verstanden. Die beabsichtigten Betriebsarten sind damit:
- Im Fahrzeug: Versorgung über das 12-V-Bordnetz.
- Beim Aufbau und in der Werkstatt: Versorgung über USB für Aufbau, Diagnose und Funktionstests.
Das ist ein schlüssiges Konzept. Mein Stromversorgungsbefund muss entsprechend präzisiert werden: Zu prüfen bleibt, ob Schaltung und Dokumentation beide Betriebsarten tatsächlich unterstützen — insbesondere, welche Verbraucher über USB funktionieren und welche USB-Spannung beziehungsweise Leistung dafür benötigt wird. Die bisherige Eingrenzung auf einen reinen 5-V-Servicebetrieb war als Zielvorgabe zu eng.

### A03 Speicher implementiert aber Integrität weiterhin falsch zugesagt

Die ursprünglichen Platzhalter wurden durch reale FAT-Mount-, Kapazitäts- und Löschoperationen ersetzt. Der frühere pauschale Befund „Ringspeicher nur simuliert“ gilt deshalb nicht mehr.

Die [neue Prüfsiegelberechnung](/Users/schmidtm/openMotorBridge/firmware/main_controller/src/sdio_ring_buffer.cpp:173) liest jedoch die Factory-MAC mit `esp_efuse_mac_get_default()` und erweitert sie mit einer fest im Quelltext stehenden Formel zu einem HMAC-Schlüssel. Das ist kein geheimer Hardware-Schlüssel: Wer die MAC kennt, kann denselben Schlüssel berechnen. Das Prüfsiegel erfüllt daher die behauptete Fälschungssicherheit nicht. Zudem spricht der [Kapitelanfang](/Users/schmidtm/openMotorBridge/docs/de/06_telemetry_blackbox_webdav.md:3) weiter von ECDSA, während die Umsetzung HMAC verwendet.

Die Doku behauptet ferner unter [Crash-Freeze](/Users/schmidtm/openMotorBridge/docs/de/06_telemetry_blackbox_webdav.md:201) die automatische Anbindung an IMU und Lenkertaster. Im Firmwarebaum findet sich `sdio_track_lock_incident()` nur als Definition und Deklaration, kein Aufruf. Die Funktion setzt außerdem zunächst ein Flag und benennt erst beim Finalisieren um; ein eigener Favoritenpfad ist dort nicht implementiert. Entsprechend müssen Implementierung und Zusagen weiter angepasst werden.

### A04 HTTP Upload vorhanden aber automatische Synchronisation nicht geschlossen

Der [Uploader](/Users/schmidtm/openMotorBridge/firmware/main_controller/src/webdav_uploader.cpp:144) führt jetzt echte HTTP-Operationen aus. `s_has_internet_uplink` startet aber mit `false`; der Setter `webdav_set_uplink_status()` hat im Firmwarebaum keinen Aufrufer. Damit erreicht die geprüfte Firmware den Uploadablauf über diesen Gatekeeper nicht. Der Aufruf beim Ausschalten der Zündung allein stellt keinen Heim-WLAN-Uplink her.

Außerdem behandelt die Schreibschleife nur negative Rückgaben als Fehler und schreibt einen positiven Teilerfolg nicht vollständig nach. Ein Datei-Lesefehler wird nicht mit `ferror()` erkannt. Die Doku nennt 2-kB-Chunks, der Code verwendet 1024 Byte. Der ursprüngliche Simulationsbefund ist behoben, die vollständige und zuverlässige automatische Synchronisation bleibt offen.

### A05 Dateisystemimage verwendet weiterhin keinen ausführbaren Quellenpfad

Die neue Main-Partitionstabelle existiert und die Anleitung verwendet passend `0x5E0000`. Der [Erzeugungsbefehl](/Users/schmidtm/openMotorBridge/firmware/README.md:72) nennt jedoch `hardware/vehicle_profiles`; dieses Verzeichnis fehlt. Vorhandene Fahrzeugprofile liegen unter `firmware/main_controller/data/can_profiles/`. Der Befehl muss vom dokumentierten Arbeitsverzeichnis aus auf existierende Daten zugreifen und die vom Laufzeitcode erwartete Verzeichnisstruktur erzeugen. Ein passender Flashoffset allein schließt A05 nicht.

### A06 v10 Modell aktualisiert aber weiter keine Hardwareverifikation

Der aktualisierte [Simulator](/Users/schmidtm/openMotorBridge/tools/simulators/firmware_hil_system_sim.py:1) lief mit Exitcode 0 durch. Die alte UWB-Modellbeschreibung ist dort ersetzt. Das Programm modelliert die Zustände jedoch selbst in Python; seine Erfolgsmeldungen sind kein Nachweis, dass die C++-Firmware auf echten USB-Knoten läuft oder dass HTTP-Dateien übertragen wurden.

[Kapitel 13](/Users/schmidtm/openMotorBridge/docs/de/13_simulation_testbench.md:66) enthält weiterhin widersprechende Aussagen, etwa den ersatzlosen Entfall der Hubmagnete, obwohl die neue Pod-Montage sie ausdrücklich benötigt. Modelltests, Firmwaretests und Messungen müssen getrennt benannt werden.

### B06 und B07 Reststellen in Listen und englischer Fassung

Die [Montage](/Users/schmidtm/openMotorBridge/docs/de/16_build_instructions_assembly.md:152) verlangt jetzt DIN-7991-Senkkopfschrauben, die [Einkaufsliste](/Users/schmidtm/openMotorBridge/docs/de/16_build_instructions_assembly.md:89) weiterhin DIN 912.

Die Dry-Flap wird in der [Exporttabelle](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:1652) weiterhin als einschiebbarer Rail-1-Tray geführt. Die [englische Fassung](/Users/schmidtm/openMotorBridge/docs/en/08_enclosures_mechanics_cad.md:675) nennt weiterhin eine „spring-loaded flap“. Das widerspricht der jetzt klar beschriebenen eingelegten TPU-Abdeckung.

### B09 Neue Innenraumangaben sind noch nicht vollständig hergeleitet

Die [Trockenfach-Bildunterschrift](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:398) nennt weiterhin 145 × 65 mm. Der Text nennt jetzt zusätzlich 143 × 63 mm oberhalb einer Auflageleiste sowie 113 × 61 mm hinter der Elektronikbucht.

Der [Hauptausschnitt](/Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/parts/015_pod_monocoque_tub.scad:130) beträgt weiterhin durchgehend 141 × 61 mm; größere seitliche Aussparungen sind nur lokal als Führungsnuten vorhanden. In der [Baugruppe](/Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/99_pod_monocoque_assembly.scad:125) beginnt das Intercom bei X=52 mm. Bis zum Ende dieses Hauptausschnitts bei X=145,5 mm bleiben rechnerisch 93,5 mm. Die behauptete freie Länge von 113 mm ist daraus nicht ableitbar. Erforderlich sind bemaßte Einbauhüllen mit derselben Referenzebene wie im CAD.

### B11 Hubmaße und Portzuordnung widersprechen sich erneut

Die überarbeitete [Mechanikbeschreibung](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:579) nennt 82 × 54 × 15 mm. Das [Gehäuse-CAD](/Users/schmidtm/openMotorBridge/hardware/cad/scad/04_front_node/glovebox_power_injection_hub.scad:34) ergibt weiterhin nominell 55 × 25 mm in XY. Die direkt aus den Dreieckskoordinaten der vorhandenen STL gemessene vollständige Bauhülle beträgt **55 × 25 × 17 mm**. Der Unterschied zwischen der nominellen CAD-Höhe und 17 mm kommt bei dieser Prüfung aus der Gesamtgeometrie, nicht aus einer angenommenen Drucktoleranz.

Auch die Ports sind noch nicht gleich definiert:

| Referenz | CAD | Mechanikkapitel | Bauanleitung |
| --- | --- | --- | --- |
| J1 | HOST | FRONT | Upstream vom Front-Node |
| J2 | FRONT | HOST | Headunit Out |
| J3 | PHONE | PHONE | DONGLE |
| J4 | DONGLE | DONGLE | PHONE |
| J5 | MEDIA | MEDIA | MEDIA |

Fundstellen: [CAD-Portdefinition](/Users/schmidtm/openMotorBridge/hardware/cad/scad/04_front_node/glovebox_power_injection_hub.scad:9), [Kapitel 08](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:581), [Bauanleitung](/Users/schmidtm/openMotorBridge/docs/de/16_build_instructions_assembly.md:310). Eine verbindliche Porttabelle muss Schaltplan, Gehäusebeschriftung und beide Kapitel zusammenführen.

## Weitere mechanische Prüfpunkte

### C01 Mögliche Überdeckung zwischen Deckelplatte und Nutdach

Der alte seitliche Versatz aus B05 ist korrigiert. In Z besteht aber ein weiterer rechnerischer Kontaktverdacht: Die Deckelplatte beginnt bei 32,4 mm und ist 3,2 mm dick, endet also bei 35,6 mm. Der Nut-Ausschnitt endet bei `32,0 + 3,4 = 35,4 mm`. Die Platte greift seitlich bis Y=3,1 bzw. 66,9 mm in Bereiche hinein, in denen die Wanne oberhalb dieser Nut wieder massiv ist. Das weist auf etwa 0,2 mm Überdeckung am Nutdach hin.

Fundstellen: [Deckelparameter](/Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/parts/013_pod_slide_lid.scad:35), [Einbauhöhe](/Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/99_pod_monocoque_assembly.scad:152), [Nutgeometrie](/Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/parts/015_pod_monocoque_tub.scad:142).

Das ist eine Koordinatenprüfung, kein erfolgreich ausgeführter Mesh-Kollisionstest. Vor einer mechanischen Freigabe sind die geschlossene Lage und der vollständige Einschubweg mit der finalen Geometrie zu prüfen.

### B02 Einbauweg weiterhin nicht belegt

Die erneuerten Bilder machen die Teile verständlicher. Sie ersetzen aber keine Montagefolge auf realer Führungshöhe: Die Pod-Explosion hebt den Deckel weiterhin um 36 mm und die Traversen um 18 mm an. Auch die Zentralbox ist vertikal explodiert; Teile der neuen Darstellung reichen über den Bildrand. Der freie horizontale Weg von Zwischenboden, Akku und Antennen bleibt damit unbewiesen. In der Doku sollte eine Teileexplosion als Teileübersicht bezeichnet werden; eine separate Einschubfolge sollte die tatsächliche Bewegung und den benötigten Freiraum zeigen.

## Ausgeführte Prüfungen

- Alle 19 Befunde wurden gegen den neuen Commit bewertet; gezielte Quelltextsuche in Deutsch, Englisch, Firmware und CAD.
- Die fünf für die ursprünglichen Bildbefunde maßgeblichen Abbildungen wurden erneut visuell betrachtet und separat gesichert.
- Die lokalen Markdown-Dateilinks in README sowie den deutschen und englischen Kapiteln wurden erneut geprüft. Ergebnis: keine fehlenden lokalen Dateiziele. Maschinengebundene `file:///Users/...`-Links wurden dabei nicht als portable Repository-Links bewertet; ihr vermehrter Einsatz bleibt eine zusätzliche Dokumentationsschwäche.
- Der aktualisierte Python-Simulator lief erfolgreich durch. Sein Konsolenlog liegt der Revalidierung als Textdatei bei.
- Hub-STL und Pod-Deckel-STL wurden direkt aus ihren Dreieckskoordinaten auf Bauhüllen geprüft. Das ersetzt keine Kollisionsprüfung zwischen mehreren Teilen.
- OpenSCAD scheitert weiterhin beim Programmstart mit der NEON-Prozessorfehlermeldung, auch mit explizitem ARM-Aufruf. Der x86-Aufruf ist hier nicht ausführbar. Daher keine erfolgreiche neue CSG-Prüfung und kein Firmware- oder Hardware-Funktionsnachweis.

Der erste Bericht und seine Belegbilder bleiben als historischer Stand erhalten. Diese Revalidierung ergänzt ihn; Quellcode und Originaldokumentation wurden nicht verändert.
