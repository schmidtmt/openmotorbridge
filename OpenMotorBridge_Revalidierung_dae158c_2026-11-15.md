# OpenMotorBridge – Revalidierung aller aktiven Platinen

Stand: **15. November 2026, Commit `dae158c`**. Arbeitsverzeichnis zu Beginn sauber. Vergleichsbasis: Platinencheck `c2af859` mit H01–H22 sowie die vorherigen Dokumentationsreviews. Die Repository-Dokumente wurden als Prüfgegenstand behandelt; die Nutzervorgaben, insbesondere 12-V-Fahrzeugversorgung und USB-Werkstattbetrieb, bleiben Bewertungsmaßstab.

**Ergebnis: 6 der 22 bisherigen Befunde sind im ursprünglich beanstandeten Kern behoben, 9 teilweise behoben und 7 offen.** Es sind reale elektrische Korrekturen erfolgt. Trotzdem bleiben Fehler an Versorgung, MCU-Landpatterns und Fertigungsdaten. Eine Fertigungsfreigabe lässt sich aus diesem Stand nicht ableiten. Die folgenden Nachfolgebefunde konkretisieren bestehende Punkte und sind keine zusätzlich zu addierende Fehlerstatistik.

## Wesentliche verbleibende und neue Befunde

### N01 · P1 · Main-Lader: ISET liegt weiterhin falsch

Der früher fehlende BQ24075 ist jetzt als U4 vorhanden. BAT an Pins 2/3, OUT an 10/11 und der LDO-Eingang an `VCC_SYS` stellen einen tatsächlichen Fortschritt gegenüber dem rein messenden Akkuanschluss dar.

Die Ladestromprogrammierung ist aber falsch angeschlossen: **PCB-Pin 15 führt `CHG_ISET` über R16=1 kΩ nach Masse, Pin 16 liegt direkt auf `GND_PWR`.** Beim BQ24075 ist Pin 15 `SYSOFF`, der echte `ISET` liegt auf Pin 16. Die dokumentierte 1-A-Einstellung über R16 erreicht damit den falschen Pin; der direkte Masseanschluss am echten ISET entspricht nicht der vorgesehenen Widerstandsprogrammierung. Zusätzlich ist Pin 5 tatsächlich EN2 und kein Versorgungspin; sein Anschluss an `VCC_SYS` muss als bewusste Logikbeschaltung geprüft werden. EN1 an Masse ist für sich kein Fehler.

**Korrektur:** Das komplette BQ24075-Symbol mit den echten Pinnummern prüfen, R16 an ISET führen und die EN1/EN2-/SYSOFF-/TMR-Beschaltung anhand des gewünschten Betriebsmodus festlegen. Danach Schaltplan, Layout und Exporte erneuern. H02 bleibt teilweise behoben.

Evidenz: [main_box U4](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:9070). Hersteller: [TI BQ24075, Pin Functions](https://www.ti.com/lit/ds/symlink/bq24075.pdf).

### N02 · P1 · Keyfob-LDO: GND und Enable fehlen

Die frühere direkte Verbindung von Akku und 3,3-V-Schiene über L1 wurde entfernt. U6 ist jetzt ein TPS7A0233PDBVR. Im PCB sind allerdings nur **Pin 1=`VBAT` und Pin 5=`VCC_3V3`** angeschlossen. **Pin 2 GND und Pin 3 EN haben kein Netz.** Laut Datenblatt muss GND mit Masse verbunden werden; ein offener EN hält den Regler deaktiviert. Ein vorhandener Reglername allein behebt den Versorgungspfad daher nicht.

**Korrektur:** GND verbinden, EN definiert beschalten und die nötige Ein-/Ausgangsbeschaltung prüfen. H16 bleibt teilweise behoben. In der maschinenlesbaren Evidenz ist EN=VBAT als eine mögliche Dauer-Ein-Beschaltung hinterlegt, nicht als einzig zulässige Lösung.

Evidenz: [smart_keyfob U6](/Users/schmidtm/openMotorBridge/hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb:5376). Hersteller: [TI TPS7A02, DBV-Pinbelegung und Enable-Verhalten](https://www.ti.com/lit/ds/symlink/tps7a02.pdf).

### N03 · P1 · Vierkanalschalter vorhanden, individuelle Ansteuerung fehlt

U12 ist jetzt ein echter TPS4H160BQPWPRQ1 im HTSSOP-28 mit zugeordneten Versorgungspins 20–23 und den passenden Ausgangspaaren. Der alte erfundene TPS25921-Vierkanalbaustein ist damit ersetzt.

**IN1–IN4 an Pins 3–6 hängen jedoch gemeinsam an `VCC_3V3`.** Es gibt dort keine vier individuellen MCU-Steuerleitungen. Der Sequencer setzt weiterhin Zustandsvariablen, erzeugt Logmeldungen und wartet; er schaltet diese vier Eingänge nicht. Gestaffeltes Einschalten, selektives Abschalten und echte Kaltstarts einzelner Zweige sind damit nicht umgesetzt. CL an Pin 11 liegt auf Masse; die versprochenen individuellen Stromgrenzen 5/2,5/2,5/1,5 A sind aus dieser Beschaltung nicht nachgewiesen. FAULT/CS sind nicht angeschlossen. Die integrierten Schutzfunktionen des ICs werden dadurch nicht pauschal verneint.

Zusätzlich zeigt Kapitel 07 weiter die **alte QFN-20-Tabelle mit Eingang 1/2 und Ausgängen 5–8**. Diese ist nach dem Bauteilwechsel eindeutig falsch.

**Korrektur:** Benötigte Hardwaresteuerung tatsächlich verdrahten, Firmware daran anbinden und Schutz-/Diagnosezusagen auf die ausgelegte Schaltung abstimmen. H01 bleibt teilweise behoben.

Evidenz: [main_box U12](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:164), [Power-Sequencer](/Users/schmidtm/openMotorBridge/firmware/main_controller/src/power_sequencer.cpp:40), [veraltete U12-Pintabelle](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:366). Hersteller: [TI TPS4H160-Q1](https://www.ti.com/lit/ds/symlink/tps4h160-q1.pdf).

### N04 · P1 · Main-BOM und CPL enthalten den neuen Ladepfad nicht

In **beiden** Fertigungsdateien fehlen U4, C13, C14, C15, R15, R16 und R17, obwohl sie im aktuellen PCB vorhanden sind. Außerdem führen BOM und CPL J6 weiterhin als Picoflex mit 1,27-mm-Raster, während das PCB jetzt `MicroLock_Plus_16Pin_2x08_Vertical` mit einem anderen Footprint enthält. Kapitel 07 nennt J6 ebenfalls noch Picoflex.

Das ist für eine Bestückungsbestellung eine konkrete Abweichung: Der neue Ladepfad wäre unvollständig und für J6 wäre ein anderes Steckersystem ausgewiesen. Der U12-Footprinttext unterscheidet sich außerdem beim EP-Maß 9,7/9,5 mm; das ist als Geometrieabgleich offen, nicht als allein durch den Namen bewiesener Montagefehler eingestuft.

**Korrektur:** BOM und CPL aus genau dem geprüften PCB und der gewählten Variante neu exportieren; Stecker und zugehörige Kabelgegenstücke gemeinsam aktualisieren. Gerber-, Pasten- und Bohrdaten wurden in diesem Durchgang nicht geometrisch gegen die aktuelle Platine freigegeben.

Evidenz: [Main-BOM](/Users/schmidtm/openMotorBridge/hardware/production_packages/01_main_box_pcba/01_main_box_pcba_bom_jlcpcb.csv:1), [Main-CPL](/Users/schmidtm/openMotorBridge/hardware/production_packages/01_main_box_pcba/01_main_box_pcba_cpl_jlcpcb.csv:1), [main_box J6](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:7659). Die fehlenden Referenzen sind auch im Evidenz-JSON dokumentiert.

### N05 · P1 · MCU-Footprints: Umbenennung ersetzt kein Landpattern

**Radar:** U1 heißt im Wert und Footprint jetzt ESP32-C5-WROOM-1U, und das Firmwareziel lautet korrekt `esp32c5`. Der gespeicherte Footprint besitzt aber weiterhin nur **19 nummerierte Pads**. Das reale WROOM-1U hat **32 Pins**. Der Namensabgleich ist bereinigt, die Bestückbarkeit nicht. H19 bleibt teilweise behoben. Evidenz: [radar_submcu U1](/Users/schmidtm/openMotorBridge/hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb:10907). Hersteller: [Espressif C5-WROOM-1/1U, Abschnitt 3](https://documentation.espressif.com/esp32-c5-wroom-1_wroom-1u_datasheet_en.html).

**Pod:** U1 Pin 2=GND und Pin 3=3V3 sind korrigiert. USB liegt aber weiterhin auf Pads 14/15, statt 17/18 des C6-MINI; der Footprint reicht bis Pad 65, das reale Modul hat 53 Pins. **OMM 09/10** führen den C6 weiterhin auf einem S2-MINI-Footprint; dort liegt die Versorgung noch auf Pad 2 und Pad 3 auf Masse. H07 bleibt teilweise behoben über die drei betroffenen Platinen betrachtet.

Evidenz: [pod_cartridge U1](/Users/schmidtm/openMotorBridge/hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb:9530), [omm_intercom U1](/Users/schmidtm/openMotorBridge/hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_pcb:478), [omm446_intercom U1](/Users/schmidtm/openMotorBridge/hardware/kicad_omm446_intercom/openmotorbridge_omm446_intercom.kicad_pcb:478). Hersteller: [Espressif C6-MINI-1/1U](https://www.espressif.com/sites/default/files/documentation/esp32-c6-mini-1_mini-1u_datasheet_en.pdf).

**Front:** ESP32-P4 steht weiterhin auf einem S3-WROOM-Modulfootprint. Der alte H09 ist offen. Evidenz: [front_node U1](/Users/schmidtm/openMotorBridge/hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb:8447).

### N06 · P1 · Pod: Überspannungspfad getrennt, neue 5-V-Schiene ohne Quelle

F1 hängt jetzt an `VCC_5V` statt am variablen `VBUS_30W`. Das entfernt die frühere unmittelbare Kopplung des PD-Ausgangs an die angeblich feste 5-V-Versorgung. Das neue Netz `VCC_5V` enthält allerdings **ausschließlich F1 Pin 1**. Ein 5-V-Reglerausgang oder externer Einspeisepin fehlt. Auch für `VCC_3V3` ist weiterhin keine Quelle vorhanden.

**Korrektur:** Tatsächliche feste 5-V- und 3,3-V-Pfade bis zu den Verbrauchern auslegen. H04 bleibt offen, H05 teilweise behoben. Evidenz: [pod_cartridge F1](/Users/schmidtm/openMotorBridge/hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb:412) und Inventar-/Evidenzdateien.

## Vollständiger Status H01–H22

„Behoben“ bezieht sich auf den konkreten alten Befund und ist keine Funktionsfreigabe der ganzen Platine.

| ID | Status | Ergebnis am aktuellen Stand |
| --- | --- | --- |
| H01 | Teilweise | Echter Vierkanalschalter und passendes Gehäuse; Steuerung, dokumentierte Limits und Pintabelle offen. Siehe N03. |
| H02 | Teilweise | BQ24075 und Akku-Leistungspfad ergänzt; falscher ISET-Anschluss und fehlender Fertigungsexport. N01/N04. |
| H03 | Offen | USB speist weiterhin die Main Box; die Satellitenzweige kommen von KL30. Der gewünschte USB-Werkstattbetrieb des Gesamtsystems bleibt unerfüllt. Die Doku beschreibt diese Einschränkung inzwischen. |
| H04 | Offen | Pod ohne Quelle für 3,3 V. |
| H05 | Teilweise | PD-Ausgang getrennt; neues festes 5-V-Netz hat keine Quelle. N06. |
| H06 | Behoben | TS5A3159: GND=2, COM=4, V+=5, IN=6 passen jetzt. |
| H07 | Teilweise | Zwei Pod-Versorgungspins korrigiert; Modulgeometrie, USB und OMM-Belegung bleiben falsch. N05. |
| H08 | Offen | C6 bleibt festes USB Serial/JTAG-Gerät. Die behauptete native USB Audio Class ergibt sich daraus nicht. |
| H09 | Offen | Front-P4 auf S3-Modulfootprint. |
| H10 | Teilweise | Nicht existierender Sensor-Pin 7 und Firmware-Serviceport-Kommentar korrigiert; Kapitel 07 verspricht weiterhin lokalen Serviceport J7. Mikrofon sitzt weiterhin auf Front, nicht auf dem Puck. |
| H11 | Behoben | Hub-U2 TLV75533P ergänzt: IN/EN an 5 V, GND an Masse, OUT an +3V3. |
| H12 | Teilweise | Hauptbeschreibung nennt jetzt 5 V/3 A. Dafür ist PD allein nicht erforderlich. Individueller Dongle-Kaltstart bleibt unverdrahtet: J2–J5 teilen VCC_5V. Firmwarematrix nennt weiterhin SW3526/60W am Hub. |
| H13 | Offen | Spiegelplatine weiterhin ein Taster; zwei Pods ergeben zwei physische Taster. Firmwarematrix nennt sechs. |
| H14 | Behoben | OPT3001: VDD=1 an 3,3 V, ADDR=2 und GND=3 an Masse, SCL/SDA=4/6. |
| H15 | Offen | GNSS_TIMEPULSE weiterhin ausschließlich an U1.7, ohne Kabelanschluss; Hardware-PPS weiter zugesagt. |
| H16 | Teilweise | Spule entfernt, Regler ergänzt; GND und EN des Reglers fehlen. N02. |
| H17 | Teilweise | Qi jetzt in BOM enthalten; J1 hat im PCB weiterhin keinen Footprintnamen. Akkuanschluss J3 weiterhin Lötpads auf R_0805 statt zugesagtem lötfreiem JST-Header. |
| H18 | Offen | Keyfob-Doku weiter mit USB-C/MAX17048 und abweichender Kapazität; tatsächliche Platine Qi, ohne diese Bauteile, mit vier statt dokumentierten zwei Lagen. |
| H19 | Teilweise | C5-Name und Buildziel vereinheitlicht, aber weiterhin 19-Pad-Landpattern. N05. |
| H20 | Behoben | Radar-TPS54302: GND/SW/VIN/FB/EN/BOOT passen jetzt zu Pins 1–6. |
| H21 | Behoben | Die früher leere LED-Funktion überträgt jetzt GRB-Bits per GPIO/Cycle-Counter. Timing und Ausgabe wurden nicht am Gerät gemessen; V2X bleibt separat unbestätigt. |
| H22 | Behoben | PCBA-09-BOM/CPL haben jetzt die richtigen Referenzen U3/U5/U6 samt DNP-Variante. Weiterhin separater U1-Footprintkonflikt BOM gegen PCB und 600-/1000-mAh-Akkubezeichnung auf 09/10. |

Positive Pinprüfungen: [pod_cartridge U4](/Users/schmidtm/openMotorBridge/hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb:571), [cockpit_breakout U2](/Users/schmidtm/openMotorBridge/hardware/kicad_cockpit_breakout/openmotorbridge_cockpit_breakout.kicad_pcb:1344), [sensor_puck U3](/Users/schmidtm/openMotorBridge/hardware/kicad_sensor_puck/openmotorbridge_sensor_puck.kicad_pcb:2843), [radar_submcu U3](/Users/schmidtm/openMotorBridge/hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb:14121). Hersteller: [TS5A3159](https://www.ti.com/lit/ds/symlink/ts5a3159.pdf), [TLV755P](https://www.ti.com/lit/ds/symlink/tlv755p.pdf), [OPT3001](https://www.ti.com/lit/ds/symlink/opt3001.pdf), [TPS54302](https://www.ti.com/lit/ds/symlink/tps54302.pdf).

Zur Grenze des C6: [Espressif USB Serial/JTAG Controller](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c6/api-guides/usb-serial-jtag-console.html). Aktuelle Firmwarestellen: [neue LED-Ausgabe](/Users/schmidtm/openMotorBridge/firmware/radar_submcu/src/main.cpp:77), [weiterhin zugesagter Serviceport J7](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:617).

## Eigener KiCad-Prüflauf

Ausgeführt mit **KiCad CLI 10.0.5** für alle zehn aktiven Platinen. ERC mit allen Schweregraden; DRC mit Schaltplan-Paritätsprüfung. Vorhandene Projektregeln und ausgeschaltete Prüfungen wurden übernommen. Kein Leiterplatten- oder Schaltplanfile wurde gespeichert oder verändert. Exitcode 0 wurde nicht mit Fehlerfreiheit gleichgesetzt.

| PCBA | ERC Fehler | ERC Warnungen | DRC / unverbunden / Parität |
| --- | ---: | ---: | --- |
| 01 | 4 | 173 | Abbruch SIGABRT; unbestätigt |
| 03 | 0 | 309 | Abbruch SIGABRT; unbestätigt |
| 05 | 0 | 526 | Abbruch SIGABRT; unbestätigt |
| 05B | 0 | 81 | 0 / 0 / 0 |
| 05C | 0 | 27 | 0 / 0 / 0 |
| 05D | 0 | 49 | Abbruch SIGABRT; unbestätigt |
| 07 | 81 | 198 | Abbruch SIGABRT; unbestätigt |
| 08 | 0 | 118 | Abbruch SIGABRT; unbestätigt |
| 09 | 21 | 65 | Abbruch SIGABRT; unbestätigt |
| 10 | 21 | 65 | Abbruch SIGABRT; unbestätigt |

Die acht abgebrochenen DRC-Läufe lieferten **kein verwertbares Ergebnis**. Ein zusätzlicher serieller Main-Lauf ohne Paritätsprüfung brach ebenfalls mit SIGABRT ab; der lokale macOS-Crashbericht zeigt einen Abbruch bei der AppKit-/Application-Registrierung. Das ist hier eine Ausführungsgrenze, kein nachgewiesener Layoutfehler und keine erfolgreiche DRC-Bestätigung. Die beiden erfolgreichen Reports enthalten jeweils null Verstöße, null unverbundene Elemente und null Paritätsabweichungen unter den jeweiligen Projektregeln.

**ERC-Einordnung:** Die 4 Main-Fehler betreffen zwei Power-Output-Konflikte innerhalb des Mehrfach-Pin-Ladersymbols und zwei nicht getriebene Power-Eingänge. Die 21 Fehler je OMM umfassen Power-/Pin-Konflikte und fehlende Verbindungen. Beim Keyfob sind es 78 unverbundene Symbolpins und 3 doppelte Pins. Nicht jeder ERC-Fehler ist ein realer Kurzschluss; Symbolmodell und Anschlussabsicht müssen einzeln bereinigt werden. Die oben aufgeführten Datenblattfehler sind unabhängig davon direkt aus den PCB-Pad-Netzen belegt.

Warnungen enthalten viele Off-Grid-Anschlüsse und Meldungen zu nicht gefundenen/verknüpften Symbol- und Footprintbibliotheken. Letztere hängen auch von der lokalen KiCad-Bibliothekskonfiguration ab und wurden nicht als ebenso viele physische Defekte gewertet. Ignorierte Prüfungen stehen in den Rohreports.

## Vorherige Dokumentations- und Mechanikpunkte

**WebDAV A04 hat Fortschritte gemacht:** Das Ausschalten ruft jetzt einen echten STA-Verbindungsablauf mit Wi-Fi-/IP-Events auf. Der alte Vorwurf „nur Uplinkflag auf true“ trifft nicht mehr zu. Vollständig geschlossen ist der Punkt noch nicht: Im Main-Firmwarebaum fehlen Aufrufe von `esp_netif_init()` und `esp_event_loop_create_default()` vor dem neuen Default-STA-Aufbau. Die Rückgabewerte mehrerer Initialisierungs-/Startaufrufe bleiben unbehandelt. Ein Firmwarebuild und ein Lauf mit echtem Heim-WLAN wurden hier nicht ausgeführt. Evidenz: [neuer Garage-Sync](/Users/schmidtm/openMotorBridge/firmware/main_controller/src/webdav_uploader.cpp:225). Initialisierungsfolge: [ESP-IDF ESP-NETIF](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/network/esp_netif.html).

Die im vorherigen Platinencheck bereits bestätigten Korrekturen an Dry-Flap-Export und Pod-Innenraum werden nicht wieder geöffnet. Seit jenem Stand wurden die wesentlichen Pod-Mechanikquellen nicht geändert; eine neue vollständige Bewegungs-/Kollisionsprüfung und erneute Sichtung aller Renderbilder erfolgten in diesem Durchgang nicht. Die frühere Einschränkung zum durchgängig nachgewiesenen Einschubweg bleibt bestehen. Die archivierte PCBA 06 liegt jetzt ausdrücklich im Legacy-Verzeichnis und gehört nicht zur aktiven Zehn-Platinen-Prüfung.

Die HMAC-Zusage bleibt auf Korruptions-/Integritätserkennung eingegrenzt. Eine neue Freigabe als Schutz gegen absichtliche Manipulation wird daraus nicht abgeleitet.

## Evidenz und nächste Korrekturen

Gespeichert sind das aktuelle Inventar, unabhängige Pad-/Netzprüfungen und sämtliche verfügbaren KiCad-JSON-Reports einschließlich der abgebrochenen Läufe im Laufprotokoll. Die Quellplatinen, Firmware, Dokumentation und Produktionspakete wurden nicht geändert.

Für den nächsten Durchgang zuerst N01/N02, die echten MCU-Landpatterns und die fehlenden Pod-Spannungsquellen korrigieren. Danach Steuerleitungen und konkrete Kabelpfade abgleichen und erst aus diesem Stand die Fertigungsdateien neu exportieren. Diese Schritte lassen sich am bestehenden Entwurf vor einer kostenpflichtigen Bestellung erledigen.

Begleitdateien: [Prüfevidenz JSON](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_Pruefevidenz_dae158c.json), [Platineninventar JSON](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_Platineninventar_dae158c.json), [Inventar Text](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_Platineninventar_dae158c.txt), [KiCad-Rohreports und Laufprotokoll ZIP](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_KiCad_Prueflauf_dae158c.zip).
