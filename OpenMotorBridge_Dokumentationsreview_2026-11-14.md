# OpenMotorBridge Dokumentationsreview

Stand: 14. November 2026. Repository `/Users/schmidtm/openMotorBridge`, HEAD `13ab023`, einschließlich der beim Review vorhandenen Änderungen im Arbeitsverzeichnis.

Die Dokumentation besitzt eine brauchbare Kapitelstruktur, vermischt aber Zielarchitektur, ältere Konstruktionsstände und simulierte Funktionen. Der Nachbau wird besonders durch unterschiedliche Controller, Versorgungskonzepte, Montageprinzipien und nicht zusammenpassende Abbildungen erschwert. Dieser Bericht hält das erste Review und die ergänzende Prüfung von Text, Bildern und CAD gemeinsam fest.

P1 bezeichnet Befunde, die Nachbau, Betrieb oder wesentliche Funktionszusagen betreffen. P2 bezeichnet irreführende Darstellungen und widersprüchliche Angaben, die vor einer Freigabe der Dokumentation korrigiert werden sollten. Ein Bildbefund beweist für sich allein keine Kollision im aktuellen CAD.

## Bisheriges Review

### A01 Controller und Buildziele widersprechen sich

**P1 · Bestätigter Widerspruch.** Kapitel 09 beschreibt ESP32-S311/S31 und RISC-V, die Firmware-Anleitung und `sdkconfig.defaults` verwenden ESP32-S3 bzw. `esp32s3`. Für den Front-Knoten treten zusätzlich P4/E22-Angaben auf. Die passende Kombination aus Platinenrevision und Firmware bleibt unklar.

Fundstellen: [Architektur Kapitel 09](/Users/schmidtm/openMotorBridge/docs/de/09_firmware_architecture.md:5), [Firmware-Anleitung](/Users/schmidtm/openMotorBridge/firmware/README.md:14), [Main-Konfiguration](/Users/schmidtm/openMotorBridge/firmware/main_controller/sdkconfig.defaults:2), [Front-Konfiguration](/Users/schmidtm/openMotorBridge/firmware/front_node/sdkconfig.defaults:2).

Korrektur: Eine verbindliche Matrix aus Platinenrevision, MCU, Build-Target, Toolchain und Implementierungsstatus veröffentlichen und alle Kapitel daran ausrichten.

### A02 USB Stromversorgung beschreibt verschiedene Schaltungen

**P1 · Bestätigter Widerspruch.** Kapitel 07 nennt einen 5-V-Serviceeingang mit LM66100. Kapitel 05 beschreibt USB-PD mit CH224K und LM5050. Die Bauanleitung verspricht darüber die Versorgung der angeschlossenen Knoten mit bis zu 60 W. Aus der Doku ist nicht eindeutig ableitbar, welche Betriebsart zur vorliegenden Platine gehört.

Fundstellen: [Hardware](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:127), [Stromversorgung](/Users/schmidtm/openMotorBridge/docs/de/05_power_management_ups.md:40), [Werkbankbetrieb](/Users/schmidtm/openMotorBridge/docs/de/16_build_instructions_assembly.md:197).

Korrektur: Eingangsspannungen, Controller, OR-ing, Leistungsgrenzen und unterstützte Verbraucher pro Revision angeben. Serviceversorgung und vollständigen Systembetrieb unterscheiden.

### A03 Ringspeicher und Signierung sind im geprüften Speicherpfad nicht implementiert

**P1 · Bestätigte Abweichung zum Code.** Kapitel 06 beschreibt rollierendes Überschreiben, Crash-Freeze und ECDSA-Signierung als vorhandene Funktionen. Im Speicherpfad ist das Löschen nur kommentiert, der freie Speicher konstant mit 14500 MB simuliert und das Mounten lediglich durch ein Statusflag ersetzt. Die beschriebenen Schutzmechanismen sind damit in diesem Modul nicht nachgewiesen.

Fundstellen: [Funktionszusagen](/Users/schmidtm/openMotorBridge/docs/de/06_telemetry_blackbox_webdav.md:200), [Mount-Platzhalter](/Users/schmidtm/openMotorBridge/firmware/main_controller/src/sdio_ring_buffer.cpp:45), [Purge und Speicherplatz](/Users/schmidtm/openMotorBridge/firmware/main_controller/src/sdio_ring_buffer.cpp:119).

Korrektur: Status als geplant oder unvollständig ausweisen. Aussagen zu Datenschutz und Integrität an tatsächlich implementierte und geprüfte Mechanismen binden. Dieser Befund ist keine juristische Bewertung der Konformität.

### A04 Automatischer WebDAV Upload ist im Firmwarepfad simuliert

**P1 · Bestätigte Abweichung zum Code.** Die Doku beschreibt WLAN-Suche, TLS-Verbindung und Übertragung neuer Dateien. Der geprüfte Firmwarepfad wartet 1,5 Sekunden und meldet Erfolg, ohne eine HTTP-Übertragung auszuführen.

Fundstellen: [Upload-Ablauf](/Users/schmidtm/openMotorBridge/docs/de/06_telemetry_blackbox_webdav.md:229), [Firmwarepfad](/Users/schmidtm/openMotorBridge/firmware/main_controller/src/webdav_uploader.cpp:41).

Korrektur: Implementierungsstatus von Firmware-Upload, PWA-Upload und separatem WebDAV-Proxy getrennt nennen. Ein Erfolg darf erst nach bestätigter Übertragung beschrieben werden.

### A05 Flashanleitung und Partitionslayouts passen nicht zusammen

**P1 · Bestätigter Widerspruch.** Die Anleitung erklärt ein gemeinsames A/B-Layout für alle Targets und zeigt `storage` bei `0x610000`. Beim Hauptcontroller fehlt eine `partitions.csv`; die Cartridge verwendet `0x370000`. Für das im Flash-Befehl genannte `data_image.bin` fehlt die Erzeugungsanleitung.

Fundstellen: [Partitions- und Flashanleitung](/Users/schmidtm/openMotorBridge/firmware/README.md:229), [Cartridge-Layout](/Users/schmidtm/openMotorBridge/firmware/smart_cartridge/partitions.csv:8), [Main-Konfiguration](/Users/schmidtm/openMotorBridge/firmware/main_controller/sdkconfig.defaults:1).

Korrektur: Pro Target das tatsächliche Partitionslayout und vollständige Schritte zum Erzeugen und Flashen des Dateisystemimages dokumentieren. Rollback-Zusagen separat mit Konfiguration und Boot-Verhalten belegen.

### A06 Beschriebene v10 Verifikation verwendet ein älteres Modell

**P2 · Bestätigter Versionswiderspruch.** Kapitel 13 beschreibt die Prüfung des USB-Backbones. Der referenzierte HIL-Simulator modelliert v9.6 mit UWB und Zweidrahtversorgung. Ein erfolgreicher Durchlauf bestätigt die neue Architektur nicht.

Fundstellen: [Simulationsbeschreibung](/Users/schmidtm/openMotorBridge/docs/de/13_simulation_testbench.md:7), [HIL-Modell](/Users/schmidtm/openMotorBridge/tools/simulators/firmware_hil_system_sim.py:5), [Master-Runner](/Users/schmidtm/openMotorBridge/tools/run_all_simulations.py:1).

Korrektur: Modellversion, Prüfumfang und Grenzen pro Test nennen; reine Simulation, ausgeführten Firmwarecode und Messungen an echter Hardware eindeutig unterscheiden.

### A07 Verlinkter Front Node Zwischenboden fehlt

**P2 · Bestätigter fehlender Dateipfad.** Die Bauanleitung verlinkt `hardware/cad/stl/04_front_node/010_front_node_slide_tray.stl`; diese Datei existiert nicht. Derselbe Fehler steht in der englischen Fassung.

Fundstelle: [Bauteilliste](/Users/schmidtm/openMotorBridge/docs/de/16_build_instructions_assembly.md:72).

Korrektur: Entscheiden, ob der Zwischenboden zum aktuellen Front-Knoten gehört. Falls ja: CAD, Export und Montage ergänzen; andernfalls die veraltete Anforderung entfernen.

## Ergänzendes Review von Mechanik und Abbildungen

### B01 Podbilder zeigen den beschriebenen L Deckel nicht

**P1 · Visuell bestätigte Abweichung.** Kapitel 08 beschreibt einen einteiligen L-Deckel aus horizontaler Deckelfläche und oberer Heckwand. Die vorhandenen Schnitt- und Explosionsbilder zeigen einen flachen Deckel ohne den deutlich herabgezogenen hinteren Schenkel. Das Explosionsbild zeigt ihn zudem weit oberhalb des Gehäuses. Das vermittelt eine andere Konstruktion als der Text und erklärt die horizontale Montage nicht.

Fundstellen: [Abbildungen 8.6 und 8.7](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:194), [L-Kinematik](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:206), [aktuelles Deckel-CAD](/Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/parts/013_pod_slide_lid.scad:141).

Einordnung: Das aktuelle Deckel-CAD enthält bereits die integrierte Heckwand. Die Abweichung spricht für einen älteren Bildstand; sie beweist nicht, dass im aktuellen Quellmodell der L-Schenkel fehlt. Auch im aktuellen Explosionsskript wird der Deckel um 75 mm nach oben versetzt, obwohl die Bildunterschrift eine horizontale Einschubkinematik beschreibt.

Korrektur: Bilder aus dem finalen Modell neu erzeugen. Eine zusätzliche Darstellung muss den Deckel auf seiner realen Führungshöhe nach hinten ausgezogen zeigen, mit Bewegungsrichtung, freiem Portal und verbleibender Wannenschwelle. Eine vertikale Teileexplosion darf ergänzend bleiben, sollte aber als solche bezeichnet werden.

[Gesicherte Explosionsabbildung](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/review-bilder/pod_monocoque_assembly_exploded_3d.png) · [Gesicherter Anschnitt](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/review-bilder/pod_monocoque_assembly_cutaway_3d.png)

### B02 Bilder belegen keinen freien Montageweg für den mittleren Einschub

**P2 · Bestätigtes Darstellungsproblem, aktuelle Blockade nicht nachgewiesen.** Die Zentralbox soll den Zwischenboden horizontal von hinten auf Rail 1 aufnehmen. Die Explosionsdarstellung stapelt die Teile vertikal; am hinteren Bereich ist der freie Durchtritt des Zwischenbodens nicht nachvollziehbar dargestellt. Dadurch bleibt genau die vom Nutzer angesprochene Frage offen, wie das Teil an der Rückwand vorbei eingeschoben werden soll. Beim Pod ist zusätzlich zu beachten: Die gezeigte gelbe Dry-Flap deckt nur die vordere Elektronikzone ab und ist nicht derselbe großflächige Akku-Zwischenboden wie bei der Zentralbox.

Fundstellen: [Zentralbox Rail 1 und Heckportal](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:20), [Abbildung 8.2](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:71), [Montageschritt](/Users/schmidtm/openMotorBridge/docs/de/16_build_instructions_assembly.md:124), [aktuelles Heckportal im Main-CAD](/Users/schmidtm/openMotorBridge/hardware/cad/scad/01_main_box/parts/000_monocoque_tub.scad:138), [Pod-Dry-Flap](/Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/parts/014_pod_dry_flap.scad:23).

Einordnung: Das aktuelle Main-CAD schneidet das Heckportal oberhalb der 15-mm-Schwelle bereits frei; Rail 1 liegt bei 18 mm. Die Aussage „der aktuelle Zwischenboden wird sicher von der Rückwand blockiert“ wäre anhand der geprüften Quellen zu stark. Die Bilder lösen den Widerspruch aber nicht auf.

Korrektur: Je Gehäusetyp einen Längsschnitt durch die Einschuböffnung sowie mindestens die Positionen ausgebaut, halb eingeschoben und geschlossen zeigen. Bewegungsraum einschließlich Akku, Antennen und Kabeln prüfen und bemaßen.

[Gesicherte Zentralbox-Explosion](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/review-bilder/main_box_full_assembly_exploded_3d.png)

### B03 Schlossabbildung ist abgeschnitten und erklärt den Mechanismus nicht

**P2 · Visuell bestätigt.** Abbildung 8.8 soll den innenliegenden PA12-U-Bügel, beide Eckriegel, den Magneten und den freien SMA-Torbogen zeigen. Tatsächlich liegt der größte Bildbereich leer; die Bauteile sind links unten abgeschnitten. Die versprochene Zweipunktverriegelung ist daraus nicht nachvollziehbar.

Fundstellen: [Schlossbeschreibung und Abbildung](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:210), [Render-Zuordnung und Kamera](/Users/schmidtm/openMotorBridge/hardware/scripts/build_cad_from_openscad.py:241).

Korrektur: Kamera auf die aktuelle Geometrie zentrieren und gesperrten sowie entriegelten Zustand nebeneinander zeigen. Magnet, Federweg, beide Riegel und SMA-Freiraum beschriften. Den Hub vereinheitlichen: Doku und Detailmodell nennen 3,2 mm, das Deckelmodell setzt `U_LIFT_STROKE=3.0`.

[Gesicherte Schlossabbildung](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/review-bilder/pod_slide_lid_magnetic_lock_3d.png)

### B04 Als exakt bezeichneter Schnitt zeigt alte Zentralbox Anschlüsse

**P2 · Visuell bestätigter Versionsmix.** Die als exakte Schnittansicht bezeichnete Abbildung 8.5 enthält „DEUTSCH DTM-12“, einen „J1: DTM-12 HEADER“, eine schwenkbare Akkubrücke und ESP32-S3. Der aktuelle Text beschreibt DTM-6 plus separaten 16-poligen Peripherieanschluss, einen horizontal einschiebbaren Zwischenboden und die neuere MCU-Bezeichnung. Das Bild kann deshalb nicht als exakter Nachweis der beschriebenen v10-Montage dienen.

Fundstellen: [Schnitt und Bildunterschrift](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:81), [aktuelle Schnittstellen](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:151).

Korrektur: Den Schnitt aus derselben freigegebenen CAD-Baugruppe wie die Explosionsdarstellung ableiten. Bis dahin als historische Prinzipskizze kennzeichnen und keine exakte Passung daraus behaupten.

[Gesicherte Schnittabbildung](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/review-bilder/main_box_assembly_cross_section.png)

### B05 Poddeckel ist in der aktuellen Baugruppe seitlich falsch referenziert

**P1 · Rechnerisch belegte Maßinkonsistenz, geometrischer Export offen.** Die Baugruppe positioniert den Deckel mit `Y=(70-60.5)/2=4.75 mm`. Das aktuelle Deckelteil ist jedoch 63,8 mm breit und besitzt rechts zusätzlich eine 1,6-mm-Führungszunge. Dadurch liegt diese Zunge bei Y=68,55 bis 70,15 mm. Die rechte C-Nut der Wanne reicht nur von Y=64,5 bis 68,5 mm; die nominelle Außenbreite endet bei Y=70 mm. Die Kombination widerspricht der zugesagten freigängigen, zentrierten Führung und weist auf eine Überdeckung mit der rechten Wand hin.

Fundstellen: [Deckelposition](/Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/99_pod_monocoque_assembly.scad:149), [Deckelbreite und Führungszungen](/Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/parts/013_pod_slide_lid.scad:32), [rechte C-Nut](/Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/parts/015_pod_monocoque_tub.scad:145).

Korrektur: Breite, Einbaureferenz und Nutkoordinaten aus gemeinsamen Parametern ableiten. Anschließend die geschlossene Lage und den vollständigen Einschubweg mit einer geometrischen Schnittmengenprüfung kontrollieren. Ein Bild-Neurender allein behebt diese Maßinkonsistenz nicht.

Prüfgrenze: Eine OpenSCAD-Schnittmengenprüfung wurde angesetzt, konnte hier aber nicht ausgeführt werden. Das installierte Programm bricht mit „Incompatible processor … neon“ ab. Der Befund stützt sich deshalb auf die angegebenen Koordinaten, nicht auf einen erfolgreichen Mesh-Kollisionstest.

### B06 Aktuatormontage wechselt zwischen Bodenverschraubung und Wandführung

**P1 · Bestätigter Konstruktionswiderspruch.** Das Mechanikkapitel beschreibt zwei unabhängig von hinten eingeschobene Quertraversen, Kraftableitung in die Wandnuten, bündige DIN-7991-Schrauben und EPDM-Endstopfen. Die Bauanleitung verlangt dagegen eine im Pod-Boden verschraubte Schlittenbaugruppe und DIN-912-Schrauben. Das ist eine andere Befestigung und widerspricht dem beschriebenen glatten Boden sowie der Kopffreiheit über den Traversen.

Fundstellen: [Wandführung und Gegenkraft](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:348), [Bodenverschraubung](/Users/schmidtm/openMotorBridge/docs/de/16_build_instructions_assembly.md:144), [aktueller Traversenaufbau](/Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/parts/012_universal_actuator_slide_bracket.scad:58).

Korrektur: Einen Aufbau festlegen. Für die dargestellte Traversenlösung muss die Montage das Einführen in die Seitennuten, das Justieren und Klemmen, das Einsetzen der Endstopfen und die abschließende Freigängigkeitskontrolle beschreiben. Schraubentypen und Stückliste müssen dazu passen.

### B07 Dry Flap beschreibt drei unterschiedliche Mechanismen

**P1 · Bestätigter Widerspruch.** In der Bauteilliste und Exporttabelle heißt das Teil einschiebbarer Zwischendeckel bzw. Rail-1-Tray. Die Montagebeschreibung nennt eine federbelastete Spritzschutzklappe direkt hinter dem Außendeckel. Das CAD zeigt eine lokale flexible Abdeckung von 48 × 56 mm mit seitlichen Halteflanschen, vorderer Zunge und Zuglasche; die Baugruppe platziert sie über der vorderen PCBA-Zone. Eine separate Rückstellfeder oder ein ausgearbeiteter Scharniermechanismus ist in diesem Teil nicht modelliert.

Fundstellen: [Bauteilliste](/Users/schmidtm/openMotorBridge/docs/de/16_build_instructions_assembly.md:70), [federbelastete Klappe](/Users/schmidtm/openMotorBridge/docs/de/16_build_instructions_assembly.md:139), [Exporttabelle](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:1651), [Dry-Flap-CAD](/Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/parts/014_pod_dry_flap.scad:23), [Einbauort](/Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/99_pod_monocoque_assembly.scad:113).

Korrektur: Festlegen, ob das Teil geschoben, aufgelegt/eingerastet oder geschwenkt wird. Werkstoff, Befestigung, Bewegungsraum und Dichtkontakt passend dazu dokumentieren; den großflächigen Main-Zwischenboden begrifflich von der lokalen Pod-Abdeckung trennen.

### B08 Dockbeschreibungen verwenden alte Kabel und Portlagen

**P1 · Bestätigter Widerspruch.** Die neue Pod-Stirnwand besitzt zwei übereinanderliegende Ports bei Y=35 mm und benötigt vier Adern für Versorgung und USB. Die GSA-Dockbeschreibung spricht weiterhin von Port A bei Y=34,5 mm, Port B bei Y=50,5 mm und einem zweipoligen Versorgungskabel. Auch die Bildunterschrift des Kofferdeckel-Docks nennt Zweidrahtversorgung. Diese Angaben gehören zu einer anderen Anschlussgeometrie und lassen die Datenadern aus.

Fundstellen: [aktuelle Portanordnung](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:295), [GSA-Kabelkanal](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:905), [Kofferdeckel-Dock Abbildung 8.30](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:978), [Vierdraht-Backbone](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:399).

Korrektur: Docks, Durchführungen und Zugentlastungen gegen die neue Stirnwand prüfen. Pro Montagevariante Kabelquerschnitt, Außendurchmesser, Biegeradius, Steckerfreiraum und freie Deckelbewegung konsistent angeben. Aus den alten Bildern lässt sich deren Eignung für den neuen Kabelbaum nicht ableiten.

### B09 Beworbene Pod Innenmaße passen nicht zum aktuellen Wannenausschnitt

**P1 · Rechnerisch belegter Widerspruch.** Kapitel 08 verspricht eine lichte Innenkammer von 145 × 65 × 32 mm und einen entsprechenden Raumgewinn. Die aktuellen Parameter setzen außen 150 × 70 mm und 3,5 mm Wandstärke. Der Hauptausschnitt zieht zusätzlich je Seite 1 mm ab: Seine rechteckigen XY-Maße sind damit 141 × 61 mm. Führungen, Elektronikabdeckung, Heckwand und Geräteeinleger reduzieren den nutzbaren Raum weiter.

Fundstellen: [Raumgewinn und Innenmaß](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:323), [Außenmaße und Wand](/Users/schmidtm/openMotorBridge/hardware/cad/scad/00_common/parameters.scad:33), [Innenausschnitt](/Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/parts/015_pod_monocoque_tub.scad:130).

Korrektur: Rohinnenraum und tatsächlich nutzbaren Einbauraum unterscheiden. Für jede Gerätevariante eine bemaßte Einbauhülle einschließlich Halterung, Steckern, Kabelbögen und Aktuatoren ausweisen. Die Prozentangabe zum Raumgewinn erst nach einheitlichem Vergleichsmaß übernehmen.

### B10 Front Node Abmessungen variieren innerhalb eines Kapitels

**P2 · Bestätigter Widerspruch.** Der Überblick nennt 98 × 68 × 25 mm, Abschnitt 5 nennt 98 × 68 × 22 mm, die Exporttabelle nennt 98 × 58 × 22 mm. Die gemeinsamen CAD-Parameter ergeben für das geschlossene Grundgehäuse 98 × 68 × 22 mm. Ein aufgesetzter Puck oder Befestigungsfüße müssten separat als größere Bauhülle angegeben werden.

Fundstellen: [Überblick](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:8), [Gehäuseabschnitt](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:425), [Exporttabelle](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:1666), [CAD-Parameter](/Users/schmidtm/openMotorBridge/hardware/cad/scad/00_common/parameters.scad:112).

Korrektur: Gehäusekörper, montierte Baugruppe und benötigten Einbauraum jeweils mit einer verbindlichen Bemaßung angeben.

### B11 Handschuhfach Hub hat keine einheitliche Portdefinition

**P1 · Bestätigter Schnittstellenwiderspruch.** Das CAD definiert fünf USB-C-Öffnungen: FRONT und HOST auf der einen, PHONE, DONGLE und MEDIA auf der anderen Seite. Das Mechanikkapitel nennt dagegen eine sechspolige Einspeisung und einen vierten Funktionsport für Headset-Emulation; die Bauanleitung beschreibt MEDIA als USB-A. Der abgebildete Hub zeigt USB-C-förmige Öffnungen. Damit ist nicht eindeutig, welcher physische Anschluss welche Funktion erfüllt und welcher Kabelsatz benötigt wird. Auch die Höhe differiert: Text 18 mm, CAD-Parameter `HUB_H` 15 mm.

Fundstellen: [Hubbeschreibung](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:576), [Bauanleitung](/Users/schmidtm/openMotorBridge/docs/de/16_build_instructions_assembly.md:306), [CAD-Portdefinition](/Users/schmidtm/openMotorBridge/hardware/cad/scad/04_front_node/glovebox_power_injection_hub.scad:9), [CAD-Höhe](/Users/schmidtm/openMotorBridge/hardware/cad/scad/04_front_node/glovebox_power_injection_hub.scad:36).

Korrektur: Eine physische Porttabelle mit Steckerform, Platinenreferenz, Datenrolle, Spannungen und Stromgrenzen festlegen und direkt auf der Gehäusezeichnung beschriften. Logische Headset-Emulation von einem tatsächlich vorhandenen Anschluss unterscheiden.

### B12 Sena Bedienkonzept widerspricht dem universellen Kaltstart

**P1 · Bestätigter Widerspruch in der Doku.** Die Sena-Variante verspricht hundertprozentig digitale Bedienung ohne Stößeljustage. Wenige Zeilen später erklärt derselbe Abschnitt, dass ausgeschaltete Sena-/Cardo-Geräte nicht per BLE aufwachen und eine mechatronische Lösung benötigen. Die Bauanleitung fordert dementsprechend Hubmagnete und Kaltstart-Tastendruck für OEM-Intercoms. Die beiden Aussagen könnten nur dann zusammenpassen, wenn laufender Betrieb und Einschalten aus dem ausgeschalteten Zustand ausdrücklich getrennt beschrieben würden.

Fundstellen: [Sena ohne Stößel](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:331), [fehlendes Bluetooth-Wakeup](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:343), [Kaltstart-Montage](/Users/schmidtm/openMotorBridge/docs/de/16_build_instructions_assembly.md:144).

Korrektur: Pro Gerätemodell separat angeben: Einschalten, Ausschalten, PTT, Lautstärke und Kanalwahl. Dabei digitale Steuerung und mechanische Betätigung je Betriebszustand nennen. Dieser Befund bewertet die innere Konsistenz der Doku, nicht die externen OEM-Produkteigenschaften.

## Reihenfolge der Korrekturen

1. Die freigegebene Referenzarchitektur mit Platinenrevisionen, Controllern, Versorgung und physischen Schnittstellen festlegen.
2. Pod-Deckelbreite und Einbaureferenz, Innenmaße, Traversenmontage sowie Dry-Flap-Prinzip bereinigen. Eine bloße Textharmonisierung reicht bei B05 und B09 nicht aus.
3. Für Zentralbox, Pod und Front-Knoten reale Einbauwege und Freiräume anhand derselben CAD-Revision prüfen. Rückwand, Dichtlippen, Kabel, Antennen und montierte Geräte in die Prüfung aufnehmen.
4. Bauanleitung, Stückliste und CAD-Exportliste auf genau diesen Stand bringen.
5. Abbildungen neu erzeugen und visuell abnehmen. Bildunterschriften müssen die tatsächlich sichtbare Revision und Darstellung beschreiben; getrennte Bilder für Teileexplosion und reale Einschubbewegung verwenden.
6. Die Änderungen in Deutsch und Englisch nachziehen. Beide Sprachen teilen sich die Bilddateien; mehrere der alten Zweidraht- und Klappenbeschreibungen stehen auch in der englischen Fassung.

## Prüfumfang und offene Verifikation

Der erste Durchgang umfasste zentrale Architektur-, Firmware-, Speicher-, Simulations- und Baukapitel sowie lokale Linkziele in 40 Markdown-Dateien. Der ergänzende Durchgang konzentrierte sich auf Kapitel 08 und 16 und die zugehörigen CAD-Quellen und Render-Zuordnungen.

Visuell betrachtet wurden zehn vorhandene Abbildungen: Pod-Explosion, Pod-Anschnitt, Pod-Schloss, Zentralbox-Explosion, Zentralbox-Schnitt, Front-Node-Explosion, Pod-Variantenübersicht, Handschuhfach-Hub, Kofferdeckel-Dock und Radar-Gehäuse. Für die Radar- und Variantenansichten wird hier kein zusätzlicher, hinreichend abgesicherter Einzelbefund behauptet. Dies ist keine vollständige Maß- oder Kollisionsprüfung aller CAD-, STL-, PCB- und Bilddateien.

Eine geometrische OpenSCAD-Prüfung scheiterte am lokalen Programmstart. Hardwaretests, erfolgreiche CAD-Neuexporte, Firmware-Builds, EMV-, Dichtigkeits- und Festigkeitsmessungen sind nicht Bestandteil dieses Berichts. Beschriebene Sicht- und Quellenbefunde sind von noch offenen physikalischen Nachweisen zu unterscheiden.
