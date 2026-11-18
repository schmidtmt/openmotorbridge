# OpenMotorBridge – Revalidierung `8724eff`

**18. November 2026.** Vergleich mit `b1d5249`, Arbeitsverzeichnis zu Beginn sauber. Erneute Inventur aller zehn aktiven Platinen, unabhängiger Abgleich neuer Bauteilpins und der neuen Sensorverkabelung, Firmware-/CAD-Quellprüfung sowie BOM-/CPL-Vergleich. Die Repository-Dokumentation ist Prüfgegenstand.

**Wichtigste Ergebnisse:** Mehrere alte Punkte sind behoben. Es bleiben aber eine konkrete Reset-Kollision zwischen Front und Sensor-Puck, S31-Firmware-/RF-Konflikte, fehlende Reglerabblockung am neuen Keyfob-MCU und ein OMM-Syntaxfehler. Die ergänzte Preflight-Prüfung enthält selbst falsche Pinannahmen und darf nicht als unabhängige Herstellerfreigabe gelten.

**H13 bleibt zurückgenommen:** Zwei physische Spiegel-Taster mit konfigurierbaren Einfach-/Doppel-/Langdruckgesten entsprechen der Nutzeridee. Aus der Zahl der Funktionen wird kein zusätzlicher Hardwarebedarf abgeleitet.

## Bestätigte Fortschritte gegenüber dem letzten Bericht

| Alter Befund | Aktueller Stand |
| --- | --- |
| T01 S31-Footprint, HS-USB und Pin 40 | Eigener Footprint mit allen 64 Padnummern, HS-USB auf 54/55, Pin 40 auf Main und Front an Masse. Die konkreten alten Padzahl-/Anschlussfehler sind korrigiert; übrige GPIOs und RF bleiben U02. |
| T02 entfernte Konstanten | PIN_CARTRIDGE_LED und OMM_ADC_BAT_CHANNEL werden nicht mehr referenziert. Der alte undefinierte-Bezeichner-Befund ist geschlossen; OMM hat stattdessen den Syntaxfehler U04. |
| T03 feste Pod-Bay 1 | NVS wird initialisiert und `pod_cfg/bay_id` gelesen; Wert 2 wählt jetzt Bay 2. Die Konfiguration kann damit grundsätzlich beide Pods unterscheiden. Wer den Wert bei der Inbetriebnahme schreibt, ist hier nicht praktisch getestet. |
| T04 Antenne/Träger | LoRa-Ausnehmung wurde von 1,0 auf 1,4 mm vertieft. Sie endet nun global bei Z=20,0 mm und entfernt die zuvor konkret nachgewiesene Trägerüberschneidung. Keine neue vollständige CSG-/Bewegungsfreigabe. |
| T05 Radar-Footprint | Die PCB-Instanz enthält jetzt Pads 1–32; der alte Bibliothek-/PCB-Padzahlkonflikt ist geschlossen. |
| H17 Akku-/Qi-Anschlüsse | J1 und J3 am Keyfob sind jetzt reale zweipolige JST-SH-Stecker statt bloßer Lötpads. Der konkrete alte lötfreie-Anschlussmangel ist behoben. |
| PPS-Kabelpfad | PPS wird jetzt über Puck-J1.5 und Front-J6.5 bis zum MCU geführt. Die alte rein fehlende physische PPS-Leitung ist ergänzt; Reset und Firmwareauswertung sind getrennte Fragen. |

Evidenz: [Pod-NVS-Konfiguration](/Users/schmidtm/openMotorBridge/firmware/smart_cartridge/src/main.cpp:57), [vertiefte LoRa-Ausnehmung](/Users/schmidtm/openMotorBridge/hardware/cad/scad/01_main_box/parts/010_slide_tray.scad:136) und aktuelles Platineninventar. Die Front-/Puck-CAD-Darstellung wurde angesehen; Ausrichtung und 8-polige Anschlüsse wurden in den Quellen geändert. Eine optisch plausible Darstellung belegt die elektrische Kabelzuordnung nicht.

## U01 · P1 · Sensor-Puck-Reset trifft am Front-Kabel auf Masse

Die beiden Enden des neu beschriebenen achtpoligen Anschlusses sind nicht gleich belegt:

| Pin | Front PCBA 05, J6 | Sensor-Puck PCBA 05D, J1 |
| --- | --- | --- |
| 1–7 | Versorgung, GND, I2C, PPS, GNSS-TX/RX | Entsprechende sieben Netze |
| **8** | **GND** | **GNSS_RESET_N** |

Am Puck führt GNSS_RESET_N zum SAM-M10Q Pin 18 und über R3=10 kΩ nach 3,3 V. Der Hersteller definiert diesen Eingang als aktiven Low-Reset. **Mit einem pinweisen 1:1-Kabel wird der GNSS-Empfänger dauerhaft auf Reset gezogen.** Der Pull-up verhindert das nicht. Auch die dokumentierte GPIO-gesteuerte Resetfunktion ist so nicht vorhanden.

**Erforderlich:** Front-J6 Pin 8 an eine definierte, tatsächlich verdrahtete Reset-Steuerleitung führen oder die Schnittstelle ausdrücklich anders auslegen. Die Kabeltabelle muss an beiden Enden dieselbe Funktion beschreiben. Danach Resetfreigabe und GNSS-Betrieb kontrollieren.

Evidenz: [front_node J6](/Users/schmidtm/openMotorBridge/hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb:12998), [sensor_puck J1](/Users/schmidtm/openMotorBridge/hardware/kicad_sensor_puck/openmotorbridge_sensor_puck.kicad_pcb:1470), [sensor_puck U1](/Users/schmidtm/openMotorBridge/hardware/kicad_sensor_puck/openmotorbridge_sensor_puck.kicad_pcb:3055). Hersteller: [u-blox SAM-M10Q, Tabelle 9](https://content.u-blox.com/sites/default/files/documents/SAM-M10Q_DataSheet_UBX-22013293.pdf).

## U02 · P1 · S31-Footprint ergänzt, Firmwarezuordnung und RF-Pfad weiter offen

Main U2 und Front U1 verwenden jetzt einen eigenen `openmotorbridge:ESP32-S31-WROOM-1U`-Footprint mit **allen 64 verschiedenen Padnummern**, auch in den PCB-Instanzen. Der alte konkrete Padzahlmangel ist damit behoben. Eine vollständige maßliche Landpatternprüfung wurde hier nicht durchgeführt. Die erste gekürzte Konsolenausgabe zeigte nur Pins bis 58; diese Zwischenannahme wurde vor Abschluss anhand der vollständigen Inventur korrigiert.

Die korrigierte HS-USB-Zuordnung ist real. Die restlichen Netze/GPIOs wurden jedoch nicht umfassend auf S31 umgestellt. Beispiele:

| Board / Netz | Physisches Modulpad → realer GPIO | Firmware wählt |
| --- | --- | --- |
| Main I2C_SDA | 17 → GPIO22 | GPIO8 |
| Main I2C_SCL | 18 → GPIO23 | GPIO9 |
| Front I2C_SDA | 17 → GPIO22 | GPIO17 |
| Front I2C_SCL | 18 → GPIO23 | GPIO18 |

Diese Beispiele betreffen tatsächlich benutzte Sensor-/Codec-Busse. Main und Front stehen zudem unverändert auf **Buildziel esp32s3**, obwohl S31 eine andere RISC-V-Plattform ist.

Die Main-Keramikantenne ANT3 hängt nicht mehr am falschen Massepin 40. Ihr Netz BLE_RF_2G4 enthält jetzt allerdings **ausschließlich ANT3 Pin 1**, keinen RF-Ausgang. Die zugesagte Onboard-Antenne wird damit nicht gespeist. Dies verneint nicht pauschal eine Funkverbindung über den vorhandenen Modul-Antennenanschluss.

**Erforderlich:** Vollständiges Hersteller-Landpattern und einen konsistenten S31-Netz-/Firmwareplan einschließlich RF-Variante übernehmen. Weitere reine Namensänderungen schließen diese Punkte nicht.

Evidenz: [main_box U2](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:4208), [front_node U1](/Users/schmidtm/openMotorBridge/hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb:6332), [S31-Footprintbeschreibung](/Users/schmidtm/openMotorBridge/hardware/openmotorbridge.pretty/ESP32-S31-WROOM-1U.kicad_mod:6), [main_box ANT3](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:7024), [Main-I2C-GPIOs](/Users/schmidtm/openMotorBridge/firmware/main_controller/src/main_box_config.h:45), [Front-I2C-GPIOs](/Users/schmidtm/openMotorBridge/firmware/front_node/src/front_node_config.h:49), [Main-Buildziel](/Users/schmidtm/openMotorBridge/firmware/main_controller/sdkconfig.defaults:2), [Front-Buildziel](/Users/schmidtm/openMotorBridge/firmware/front_node/sdkconfig.defaults:2). Hersteller: [Espressif S31-WROOM-1/1U, Tabelle 3-2](https://documentation.espressif.com/esp32-s31-wroom-1_wroom-1u_datasheet_en.html).

## U03 · P1 · Beim neuen nRF52832 fehlen DEC1-/DEC4-Abblockung

Der Keyfob wurde vom nRF52840-AQFN auf einen nRF52832-QFN48 umgestellt. Die geprüften GPIO-Zuordnungen für LoRa, Taster, SWD und die Versorgungspins sind dabei nachvollziehbar umgesetzt. **U1 Pin 1 DEC1 und Pin 46 DEC4 haben im aktuellen PCB jedoch kein Netz.** Es gibt damit an diesen internen Reglerknoten auch keine angebundenen Abblockkondensatoren. Die vorhandenen MCU-Kondensatoren liegen stattdessen auf VCC_3V3.

Der nackte QFN-SoC benötigt die vom Hersteller vorgegebene Reglerbeschaltung. Ein Kondensator an der äußeren VDD-Schiene ersetzt DEC1-/DEC4-Abblockung nicht. Konkret zeigt die Nordic-LDO-Referenz DEC1-Abblockung und einen 1-µF-Kondensator im Reglerpfad; die genaue Konfiguration ist als Ganzes zu übernehmen.

**Erforderlich:** Eine konkrete QFAA-/QFAB-Bestellvariante und LDO-/DCDC-Betriebsart festlegen, die entsprechende Nordic-Referenzschaltung samt RF-/Quarz- und Reglerpassiven übernehmen und danach Netzliste/PCB/BOM neu abgleichen. DEC2 wird hier ausdrücklich nicht allein wegen eines offenen Pads beanstandet; seine Beschaltung ist gehäuseabhängig.

Evidenz: [smart_keyfob U1](/Users/schmidtm/openMotorBridge/hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb:2189). Hersteller: [Nordic QFN48-Pins](https://docs.nordicsemi.com/r/bundle/ps_nrf52832/page/pin.html), [Nordic Referenzschaltung](https://docs.nordicsemi.com/r/bundle/ps_nrf52832/page/ref_circuitry.html).

## U04 · P1 · OMM-Power-Supervisor hat eine Anweisung außerhalb der Funktion

Die alten ADC-Makroverwendungen wurden entfernt. Im aktuellen Quelltext steht jedoch sinngemäß:

```cpp
    status->jeita_fault = false;
}  // beendet power_supervisor_poll
    status->is_vbus_present = ...;
}  // zusätzliche schließende Klammer
```

Die Zuweisung steht damit auf Dateiebene und die folgende Klammer hat keinen passenden offenen Funktionsblock. Die Datei wird weiterhin in der OMM-Komponente mitgebaut. **Dies ist ein neuer quellseitiger Syntax- und damit Build-Blocker.** Der alte undefinierte-ADC-Konstanten-Befund wird nicht weitergeführt.

Zusätzlich werden Spannung und Ladezustand jetzt fest auf 4,15 V/95 % beim Laden bzw. 3,85 V/80 % sonst gesetzt. Das sind keine Messwerte. Eine Überwachung der beschriebenen 20-/10-/5-%-Schwellen lässt sich aus diesen Werten nicht ableiten; für unbekannte Zustände einen solchen Status ausweisen oder eine reale Messung vorsehen.

Evidenz: [OMM-Power-Supervisor](/Users/schmidtm/openMotorBridge/firmware/omm_module/src/power_supervisor.cpp:35). Kein vollständiger ESP-IDF-Build wurde hier ausgeführt; der ungültige Funktionsabschluss ist unmittelbar am mitgebauten Quelltext belegt.

## U05 · P1 für die Prüfzuverlässigkeit · Projekt-Preflight verwendet falsche MCU-Annahmen

Dies betrifft **das projektspezifische Python-Skript**, nicht die KiCad-DRC-/ERC-Engine:

- Der S31-Zweig bezeichnet Pad 27 als GPIO0 und Pad 26 als GPIO45. Tatsächlich sind es GPIO61/60. Der alte S3-Test wurde hier teilweise übernommen.
- Die C6-Tabelle nennt unter anderem Pin 2 als 3V3 und Pins 14/15 als USB. Das entspricht nicht dem Herstellerplan des gewählten C6-MINI-Moduls.
- In der Boardkonfiguration stehen weiterhin nRF52840 für den inzwischen umgestellten Keyfob und C3 für den C5-Radarcontroller.
- Der Abschluss erfolgt ausdrücklich mit `os._exit(0)`. Gedruckte Fehlermeldungen ergeben dadurch keinen fehlgeschlagenen Prozessstatus; das Skript ist so kein verlässliches automatisches Freigabegatter.

**Erforderlich:** Hersteller-Pinmodelle, Boardvarianten und den Exitstatus der Prüfung korrigieren. Bis dahin positive Ausgaben nur als begrenzten Projektcheck behandeln. Eine zweite Prüfung, die dieselbe falsche Pintabelle übernimmt, ist keine unabhängige Bestätigung.

Evidenz: [Preflight-S31-Prüfung](/Users/schmidtm/openMotorBridge/tools/audit_pcbas_preflight.py:297), [Preflight-Abschluss](/Users/schmidtm/openMotorBridge/tools/audit_pcbas_preflight.py:395). Das Skript wurde in diesem Durchgang quellengeprüft, nicht ausgeführt. Die obenstehenden unabhängigen Checks verwenden direkt die Herstellerunterlagen.

## Neue Sensorik und übriger Prüfstatus

**BMP390:** Die ausgewerteten Anschlüsse passen zum Bosch-Pinplan: VDDIO=1, SCL=2, GND=3/8/9, SDA=4, SDO=5 an GND, CSB=6 an 3V3 und VDD=10 an 3V3. Die I2C-Adresswahl 0x76 ist damit plausibel. Das bestätigt die Pins, keine vollständige Treiber-, Druckkanal- oder mechanische Portfreigabe. Im Front-Sensorcode wurde noch kein BMP390-Treiberpfad gefunden. Evidenz: [sensor_puck U4](/Users/schmidtm/openMotorBridge/hardware/kicad_sensor_puck/openmotorbridge_sensor_puck.kicad_pcb:566). [Bosch BMP390, Tabelle 52](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmp390-ds002.pdf).

**Hub:** Telefon-VBUS und CC sind jetzt als vom Front-PD-Pfad weitergeführte Netze getrennt geführt. Eine fehlende lokale PD-Controller-Bestückung wird deshalb nicht für sich als Fehler gewertet. Die Konstruktion nutzt an Hub-J2 auch A8/B8 für VCC_5V; der genaue Sonderkabelplan und das PD-Verhalten wurden hier nicht vollständig validiert. Selektive Dongle-Abschaltung bleibt separat offen.

**Weiterhin:** USB-Werkstattversorgung aller Satelliten, native C6 USB Audio Class und mehrere alte Keyfob-/System-Dokumentationszusagen sind nicht insgesamt freigegeben. H13 ist zurückgenommen und wird künftig nicht als Fehler gezählt. Die zuvor geprüften OMM-/Radar-GPIO-Korrekturen werden durch die neuen unabhängigen Befunde nicht wieder geöffnet.

## Eigener KiCad-Prüflauf und Produktionsvergleich

Erneut KiCad CLI 10.0.5, alle zehn Boards seriell; ERC mit allen Schweregraden und DRC einschließlich Schaltplan-Parität. Projektregeln und ignorierte Checks gelten weiter.

| PCBA | ERC Fehler | ERC Warnungen | DRC / unverbunden / Parität |
| --- | ---: | ---: | --- |
| 01 | 6 | 182 | SIGABRT_no_result |
| 03 | 0 | 334 | SIGABRT_no_result |
| 05 | 0 | 530 | SIGABRT_no_result |
| 05B | 0 | 69 | 0/0/0 |
| 05C | 0 | 27 | 0/0/0 |
| 05D | 1 | 55 | SIGABRT_no_result |
| 07 | 50 | 203 | SIGABRT_no_result |
| 08 | 2 | 119 | SIGABRT_no_result |
| 09 | 28 | 67 | SIGABRT_no_result |
| 10 | 28 | 67 | SIGABRT_no_result |

Acht DRC-Läufe enden weiterhin mit lokalem SIGABRT ohne Ergebnis; Hub und Spiegel-Pod sind unter den konfigurierten Regeln sauber. Diese Ausführungsgrenze wird nicht als Platinenfehler gezählt. ERC-Zahlen sind Werkzeugmeldungen, keine entsprechend große Anzahl bewiesener realer Defekte.

BOM-/CPL-Referenzen, Werte/Footprintnamen und CPL-Positionen/Drehungen passen im geprüften Umfang auf allen zehn Boards. Schaltplan-/PCB-Referenzen und Werte stimmen ebenfalls überein. Das ist kein Nachweis, dass die gemeinsam verwendeten Symbole/Footprints physisch richtig sind. Keine vollständige Gerber-, Thermik-, Stromtragfähigkeits-, Firmwarebuild- oder Gehäuse-Bewegungsfreigabe. Projektdateien wurden nicht verändert.

Evidenz: [Prüfdetails JSON](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_Pruefevidenz_8724eff.json), [Platineninventar JSON](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_Platineninventar_8724eff.json), [KiCad-Reports ZIP](/Users/schmidtm/Documents/Codex/2026-11-14/ka/outputs/OpenMotorBridge_KiCad_Prueflauf_8724eff.zip).
