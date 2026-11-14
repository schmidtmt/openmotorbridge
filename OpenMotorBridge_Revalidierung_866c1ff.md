# OpenMotorBridge Revalidierung mit USB Werkstattbetrieb

Stand: 14. November 2026, Commit `866c1ff`, sauberes Arbeitsverzeichnis. Diese Bewertung ergänzt die Berichte zu `13ab023` und `b4fc629` und berücksichtigt die präzisierte Nutzervorgabe: Im Motorrad oder Auto kommt die Energie aus dem 12-V-Bordnetz; beim Aufbau und in der Werkstatt soll die Versorgung über USB erfolgen.

**Das Konzept zweier Einspeisungen ist schlüssig. Im vorliegenden Hardwarestand ist der USB-Betrieb der Zentralbox auf Netzebene vorgesehen, die USB-Versorgung der angeschlossenen Satelliten aber nicht nachvollziehbar umgesetzt.** Die Dokumentation verspricht weiterhin, alle Knoten ohne zusätzliche 12-V-Quelle flashen und diagnostizieren zu können. Genau diese Lücke bleibt wesentlich.

Die Bewertung setzt weder einen reinen Logiktest als endgültige Nutzeranforderung noch 60 W Ladeleistung im Werkstattbetrieb voraus. Der gewünschte Testumfang muss mit der tatsächlich verfügbaren Versorgung übereinstimmen. Ein angeschlossener USB-Datenbus allein versorgt einen Knoten nicht automatisch mit Energie.

## Erneute Prüfung der Stromversorgung

### P01 Der USB Eingang erreicht die Versorgung der Satelliten nicht

**P1 · Bestätigte Abweichung zwischen Anschlussnetzen und Dokumentation.** Ausgewertet wurden die Netze und Bauteilanschlüsse der aktuellen Main-Box-Platine sowie die separat vorliegende exportierte Netzliste. Beide zeigen dieselbe grundsätzliche Trennung:

| Pfad | Anschlussfolge im Platinenstand | Einordnung |
| --- | --- | --- |
| USB Eingang | J3 VBUS → `USBC_VBUS` → D3 LM66100 → `VCC_5V` | Vorgesehene Einspeisung der zentralen 5-V-Schiene |
| Zentrale Logik | `VCC_5V` → U11 TPS7A0533 → `VCC_3V3` | Logikversorgung der Main Box und ihres Hubs |
| Fahrzeug Eingang | J1 Pin 1 → `KL30_IN` | Bordnetzversorgung |
| Satellitenverteilung | `KL30_IN` → U12 → `VBUS_FRONT`, `VBUS_POD1`, `VBUS_POD2`, `VBUS_RADAR` → J6 | Die vier Zweige erhalten ihre Energie aus dem Bordnetzeingang |

Fundstellen: [USB-Einspeisung D3](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:6025), [Eingänge und Ausgänge U12](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:2867), [Netzliste](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.net:1).

In den ausgewerteten Verbindungen ist kein weiterer Energiepfad von `VCC_5V` oder `USBC_VBUS` zu diesen vier Satellitenzweigen enthalten. Die Zweige führen laut Pinbelegung jeweils Versorgung, Masse und zwei Datenadern; ein zusätzlicher separater 5-V-Serviceleiter ist dort nicht vorgesehen.

Demgegenüber verspricht [Kapitel 05](/Users/schmidtm/openMotorBridge/docs/de/05_power_management_ups.md:62), die Zentralbox und alle Satelliten-Logikplatinen allein über USB flashen zu können. [Kapitel 09](/Users/schmidtm/openMotorBridge/docs/de/09_firmware_architecture.md:117) wiederholt diese Zusage ausdrücklich für PCBA 03, 05 und 08.

**Folge:** Ohne Bordnetz oder eine andere lokale Versorgung der Satelliten reicht das dargestellte Main-Box-USB-Netz nicht aus, um sie zu betreiben. Dass die Main Box und der Hub versorgt sind, macht die nachgeschalteten Controller noch nicht erreichbar.

**Erforderliche Korrektur:** Für den gewünschten USB-Werkstattbetrieb einen realen, rückstromgesicherten Versorgungspfad bis zu den benötigten Satelliten auslegen und dokumentieren. Alternativ müsste eine zusätzliche Werkstatt-Einspeisung ausdrücklich vorgesehen werden; das wäre eine Einschränkung der Idee „Versorgung über USB“. Für jede Betriebsart sind verfügbare Baugruppen, Strombudget und zulässige Tests festzuhalten. Eine bloße Anpassung des Textes auf „5-V-Service“ erfüllt den weitergehenden Nutzerwunsch nicht automatisch.

Diese Prüfung bestätigt Anschlussnetze, keine physische Funktion, Leiterbahndimensionierung oder korrekte Bauteil-Pinbelegung nach Datenblatt.

### P02 Die beschriebene Eingangsschaltung entspricht nicht der Main Platine

**P1 · Bestätigter Bauteil- und Referenzwiderspruch.** Die jüngste Doku vereinheitlicht die Kapitel auf eine Schaltung mit LM74700, LM2596, TPS2115A und BQ24075. Die ausgewertete Main-Platine enthält an den betreffenden Referenzen jedoch einen anderen Stand:

| Referenz | Dokumentation | Aktuelle Main Platine |
| --- | --- | --- |
| U1 | LM74700-Q1 als Eingangsschutz | LM5164-Q1 als Schaltregler |
| U5 | TPS2115A als Power-Mux | BMI270 als IMU |
| U7 | LM2596S-5.0 | Kein entsprechender U7-Footprint in der ausgewerteten Main-Platine |
| D3 | LM66100 | LM66100 vorhanden, Netze USBC_VBUS/VCC_5V |

Fundstellen: [beschriebene Schaltung](/Users/schmidtm/openMotorBridge/docs/de/09_firmware_architecture.md:112), [U1 im Schaltplan](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_sch:1024), [U1 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:7591), [Netzliste mit Bauteilen](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.net:1).

TPS2115A, BQ24075 und LM74700 sind in der geprüften Main-PCB-Footprintliste nicht enthalten. Damit lässt sich die dokumentierte Umschalt- und USV-Funktion aus diesem Platinenstand nicht bestätigen. Ein erklärendes Stromversorgungsdiagramm muss an die freigegebene Schaltung gebunden werden; anderenfalls entstehen trotz sprachlich konsistenter Kapitel weiterhin falsche Nachbauzusagen.

### P03 Firmwarestatus ersetzt keine Versorgungsumschaltung

Die [Serviceerkennung](/Users/schmidtm/openMotorBridge/firmware/main_controller/src/power_sequencer.cpp:125) setzt einen Diagnosezustand und gibt eine Meldung aus. Sie erzeugt keinen zusätzlichen Speisepfad zu den Satelliten. Ein behaupteter USB-Werkstattmodus muss deshalb zuerst elektrisch möglich sein und erst danach durch passende Erkennung und Strombegrenzung unterstützt werden.

Der Fahrzeugbetrieb und der USB-Werkstattbetrieb sollten als getrennte, prüfbare Zustände beschrieben werden. Welche Hochlastverbraucher beim Werkstattbetrieb benötigt werden, ergibt sich aus dem konkreten Test, nicht aus der bloßen Bezeichnung „USB“.

## Aktualisierter Status der 19 ursprünglichen Befunde

**12 im ursprünglichen Kern behoben, 7 teilweise behoben.** Die neuen Hardwarebefunde P01/P02 verschärfen A02. Der zusätzliche geometrische Einzelbefund C01 aus der ersten Revalidierung ist rechnerisch behoben.

| ID | Status | Bewertung im aktuellen Stand |
| --- | --- | --- |
| A01 | Teilweise behoben | S3-Prototyp und P4-Serienziel sind jetzt ausdrücklich getrennt. Ein eigener validierter P4-Konfigurationsstand ist damit noch nicht belegt; die zentrale S31/S3-Zuordnung bleibt zu klären. |
| A02 | Teilweise behoben | Die zwei Betriebsarten sind jetzt sprachlich konsistent. Die Versorgung der Satelliten aus USB und die dokumentierte Eingangsschaltung passen aber nicht zur Main-Platine; siehe P01/P02. |
| A03 | Teilweise behoben | Favoriten- und Radarereignisse rufen jetzt die Schutzfunktionen auf. Der behauptete fälschungssichere HMAC verwendet weiterhin einen aus öffentlicher MAC und Konstanten berechenbaren Schlüssel. |
| A04 | Teilweise behoben | Positive Teilschreibvorgänge und Lesefehler werden jetzt behandelt; Chunks entsprechen der Doku. Beim Ausschalten wird der Uplink allerdings nur auf true gesetzt, ohne nachgewiesenen Verbindungsaufbau. |
| A05 | Behoben | Der Image-Befehl verwendet nun das existierende Controller-Datenverzeichnis, einschließlich `can_profiles` und `profiles`; die dokumentierte Main-Partitionstabelle ist vorhanden. |
| A06 | Behoben | Das Modell ist auf v10 umgestellt; Kapitel 13 erklärt jetzt ausdrücklich die Grenze zwischen Python-Ablaufmodell und realer Hardware-/Firmwareprüfung. |
| A07 | Behoben | Der unpassende Front-Zwischenboden bleibt aus der Bauteilliste entfernt. |
| B01 | Behoben | L-Deckel und Krallen sind in den Podbildern erkennbar. |
| B02 | Teilweise behoben | Die Abbildung wird jetzt korrekt als vertikale Teileübersicht erklärt. Eine Darstellung oder Prüfung des vollständigen realen Einschubwegs fehlt weiterhin. |
| B03 | Behoben | Schlossbild ist lesbar; die vormals unterschiedlichen Hubangaben sind vereinheitlicht. |
| B04 | Behoben | Die alten DTM-12-Beschriftungen sind durch den aktuellen Anschlussstand ersetzt. |
| B05 | Behoben | Seitlicher Versatz ist korrigiert; auch der neue Z-Kontaktverdacht C01 ist nach Änderung von Nut und Deckeldicke rechnerisch beseitigt. |
| B06 | Behoben | Montage und Einkaufsliste verlangen nun passende DIN-7991-Senkkopfschrauben für die wandgeführten Traversen. |
| B07 | Teilweise behoben | Mechanik ist nun konsistent als eingelegte Abdeckung beschrieben. Die neue Exportverlinkung zeigt allerdings auf eine fehlende STL-Datei; siehe unten. |
| B08 | Behoben | Die beanstandeten Dockstellen nennen Vierdraht-Bus und neue Portlage. Eine physische Kabelpassung ist weiterhin kein Gegenstand der Textfreigabe. |
| B09 | Teilweise behoben | Die alte 145×65-Bildunterschrift ist angepasst. Die weiterhin genannten 143×63 bzw. 113×61 mm bleiben aus dem Hauptausschnitt und der Einbauposition nicht nachvollziehbar. |
| B10 | Behoben | Die beanstandeten Front-Abmessungen sind vereinheitlicht. |
| B11 | Behoben | Hubmaße unterscheiden jetzt 55×25×15 mm Grundkörper und 55×25×17 mm Bauhülle. Portreferenzen in beiden Kapiteln entsprechen nun dem Gehäuse-CAD. |
| B12 | Behoben | Mechanischer Kaltstart und digitale laufende Bedienung sind getrennt beschrieben. |

## Verbleibende Punkte außerhalb der Versorgung

### A03 Prüfsiegel bleibt reproduzierbar

In [sdio_ring_buffer.cpp](/Users/schmidtm/openMotorBridge/firmware/main_controller/src/sdio_ring_buffer.cpp:190) ist die Schlüsselbildung unverändert: Factory-MAC lesen, restliche Bytes mit einer konstanten Formel ergänzen. Die Doku verspricht dagegen weiterhin einen [fälschungssicheren Nachweis](/Users/schmidtm/openMotorBridge/docs/de/06_telemetry_blackbox_webdav.md:202). Ein hardwaregebundener, aber öffentlich reproduzierbarer Wert ersetzt kein Geheimnis. Dieser Befund ist durch die Umbenennung von ECDSA auf HMAC nicht geschlossen.

### A04 Uplinkflag stellt keine Netzwerkverbindung her

Beim Ausschalten der Zündung wird nun `webdav_set_uplink_status(true)` gesetzt. Im geprüften Main-Firmwarebaum findet sich aber weiterhin kein WLAN-Verbindungsaufbau mit `esp_wifi_connect`, Initialisierung mit `esp_wifi_init` oder Auswertung von `IP_EVENT_STA_GOT_IP`. Der neue Aufruf bestätigt damit keinen erreichbaren WebDAV-Server. Die Behauptung automatischer Heim-WLAN-Synchronisation bleibt unvollständig.

Fundstelle: [Abschaltablauf](/Users/schmidtm/openMotorBridge/firmware/main_controller/src/main.cpp:230).

### B07 Neuer fehlender STL Link

Die aktualisierte Exporttabelle verlinkt jetzt `hardware/cad/stl/02_pod_base/014_pod_dry_flap.stl`; diese Datei existiert nicht. Der Fehler steht in Deutsch und Englisch. Vorhanden ist unter anderem der bisherige Alias `011_pod_slide_tray.stl`. Entweder den neuen Export liefern oder auf eine vorhandene Datei verweisen.

Fundstellen: [Deutsch](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:1652), [Englisch](/Users/schmidtm/openMotorBridge/docs/en/08_enclosures_mechanics_cad.md:1387).

### B09 Freier Geräteraum bleibt unklar

Die [Raumangaben](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:326) nennen weiterhin 143×63 mm oberhalb einer Stufe und 113×61 mm hinter der Elektronikbucht. Der [Hauptausschnitt](/Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/parts/015_pod_monocoque_tub.scad:130) ist weiterhin 141×61 mm groß; die seitlichen zusätzlichen Ausnehmungen sind lokal als Nuten ausgeführt. Bei Gerätebeginn X=52 mm bis zum Hauptausschnittende X=145,5 mm bleiben 93,5 mm. Eine freigegebene Einbauhülle muss diese Unterschiede nachvollziehbar auflösen.

### C01 Rechnerischer Z Kontakt behoben

Die [Deckelplatte](/Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/parts/013_pod_slide_lid.scad:35) ist jetzt 2,8 mm dick und liegt bei Z=32,3 mm. Ihre Oberkante liegt damit bei 35,1 mm. Die [Nut](/Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/parts/015_pod_monocoque_tub.scad:142) endet bei 35,6 mm: rechnerisch 0,5 mm Spiel an dieser Stelle. Das schließt den konkreten alten Z-Befund, aber keine vollständige Bewegungs- und Kollisionsprüfung.

## Prüfumfang

Die Strompfade wurden aus Main-PCB-Footprints, deren Pad-Netzen und der exportierten Netzliste gelesen; die Front-Node-Eingangspins wurden ergänzend betrachtet. Die verbleibenden Dokumentationsbefunde wurden gegen den Commitdiff und die betroffenen aktuellen Quellstellen abgeglichen. Zwei erneuerte Podbilder wurden erneut visuell betrachtet.

Der lokale Linkcheck der READMEs und deutschen/englischen Kapitel findet zwei fehlende Dateiverweise, beide auf denselben neuen Dry-Flap-STL-Pfad. Keine Schaltung, Firmware oder Originaldokumentation wurde verändert. Es wurden keine Spannungen angelegt, keine Verbraucher getestet und keine neue Firmware oder CSG-Geometrie ausgeführt. Die frühere OpenSCAD-Startbegrenzung bleibt für eine vollständige geometrische Freigabe relevant.

Die bisherigen Berichte bleiben als historische Stände erhalten. Diese Revalidierung korrigiert insbesondere die frühere Annahme, ein reiner 5-V-Logikservice sei bereits die verbindliche Nutzeranforderung.
