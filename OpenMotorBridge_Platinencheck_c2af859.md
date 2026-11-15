# OpenMotorBridge Platinencheck und erneute Revalidierung

Stand: 14. November 2026, Commit `c2af859`, sauberes Arbeitsverzeichnis zu Beginn. Geprüft wurden alle zehn als aktiv beschriebenen PCBAs sowie zusätzlich die noch vorhandene, als entfallen bezeichnete PCBA 06.

**Ergebnis: 22 konkrete Abweichungen und Implementierungslücken. Mehrere betreffen die reale elektrische Funktion und Bestückbarkeit.** Besonders wesentlich sind falsche IC-Pinbelegungen, nicht passende MCU-Footprints, fehlende Spannungsquellen und widersprüchliche Produktions-BOMs. Vor einer Fertigungsbestellung müssen diese Punkte im Schaltungsstand aufgelöst werden; eine rein redaktionelle Harmonisierung reicht dafür nicht aus.

P1 bezeichnet einen Funktions- oder Bestückungsfehler beziehungsweise eine wesentliche nicht umgesetzte Zusage. P2 bezeichnet eine dokumentarische Abweichung oder einen fehlenden Nachweis, dessen genaue Auswirkung vom endgültigen Aufbau abhängt. Die Feststellungen stützen sich auf gespeicherte Pad-Netze und Herstellerunterlagen; es wurden keine Platinen elektrisch betrieben.

## Abdeckung aller beschriebenen Platinen

| PCBA | Platine | Komponenten im PCB inklusive Montageelementen | Kupferlagen | Ergebnis |
| --- | --- | ---: | ---: | --- |
| 01 | Zentralbox | 50 | 4 | eFuse, USV und USB-Werkstattversorgung offen |
| 03 | Pod Interface | 33 | 4 | Versorgung, Analogschalter, C6-Pinmapping und USB-Audio fehlerhaft oder unvollständig |
| 05 | Front Node | 64 | 4 | P4/S3-Footprintmix und widersprüchliche Schnittstellen |
| 05B | Handschuhfach Hub | 26 | 2 | 3,3-V-Versorgung und zugesagte Leistungs-/Schaltfunktionen fehlen |
| 05C | Spiegel Pod | 9 | 2 | Stecker, Kontur und Bestückungspositionen passen; System-Tasterzahl widersprüchlich |
| 05D | Sensor Puck | 16 | 4 | OPT3001 falsch versorgt; PPS nicht ausgeführt |
| 07 | Keyfob | 25 | 4 | Versorgung, Akku-/Qi-Bestückung und Dokumentation widersprüchlich |
| 08 | Radar Sub-MCU | 59 | 2 | MCU-Mix, falscher Buck-Pinplan und fehlende LED-Ausgabe |
| 09 | OMM 2.4G Variante | 21 | 4 | MCU-Footprint/USB-Audio und Produktionsdaten nicht konsistent |
| 10 | OMM Tri-Band | 21 | 4 | Gemeinsame MCU-Footprint-/USB-Audio-Probleme wie 09 |
| 06 | MagSafe Dock, laut Doku entfallen | 7 | 2 | Legacy-Dateien und Produktionspaket vorhanden; kein Bestandteil des aktiven Zehn-Platinen-Lineups |

Die Außenkonturen aller zehn aktiven Platinen entsprechen den jeweils genannten XY-Nennmaßen. Die Prüfbreite umfasst 324 PCB-Komponenten inklusive Befestigungselementen, zusätzlich sieben auf PCBA 06. Eine korrekte Außenkontur oder ein vollständiger Referenzsatz bestätigt noch keine richtige Schaltung.

## Befunde je Schaltung und Funktion

### H01 PCBA 01 verwendet einen einzelnen TPS25921 als erfundenen Vierkanalschalter

**P1.** Die Doku und Firmware behandeln U12 als vier unabhängig schaltbare eFuse-Kanäle. Das PCB führt KL30_IN auf Pads 1/2 und vier Zweige auf Pads 5/6/7/8. Der reale TPS25921 ist ein einkanaliger eFuse im SOIC-8, dessen Pin 1 GND, Pin 4 IN und Pin 5 OUT ist; Pins 6/7/8 sind FLT, ILIM und OVP. Zusätzlich passt der als QFN-20 bezeichnete Footprint nicht zum angegebenen Bauteil. Die Stromgrenze des genannten ICs liegt bei 0,4–1,6 A, während die Doku 5 A bzw. 2,5 A pro Zweig beschreibt. Quelle: [TI TPS25921, Pin Functions und Features](https://www.ti.com/lit/ds/symlink/tps25921l.pdf).

Fundstellen: [U12 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:2800), [Vierkanalbeschreibung](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:358), [Sequencer](/Users/schmidtm/openMotorBridge/firmware/main_controller/src/power_sequencer.cpp:41). Erforderlich sind reale, passend dimensionierte Schutzkanäle mit korrekten Symbolen, Footprints, Enable- und Fehlerleitungen. Das ist ein elektrischer Fehler, keine bloße Benennungsfrage.

### H02 PCBA 01 hat keinen nachgewiesenen Akku Leistungspfad

**P1.** J5 Pin 1 liegt auf BAT_PLUS. Dieses Netz enthält im PCB nur J5.1 und R12.1, also den Eingang des Spannungsteilers. Es führt nicht zu einem Lade- oder Power-Path-IC. Ein BQ24075 ist weder in den 50 Footprints noch in der Main-Produktions-BOM enthalten. Damit ist der beschriebene Akkuanschluss zum Messen vorhanden, die zugesagte USV-Einspeisung und Akkuaufladung aber nicht umgesetzt.

Fundstellen: [J5 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:3061), [R12 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:1040), [USV-Beschreibung](/Users/schmidtm/openMotorBridge/docs/de/05_power_management_ups.md:3). Ladepfad, Akkuschutz, Umschaltung und Betrieb bei Bordnetzausfall sind als echte Schaltung zu ergänzen oder ausdrücklich als noch ausstehend zu kennzeichnen.

### H03 USB Werkstattbetrieb versorgt weiterhin nur die Zentralbox

**P1.** Die jüngste Doku beschreibt die tatsächliche Trennung jetzt korrekt: USB J3 speist VCC_5V der Main Box; die Satellitenzweige erhalten ihre Leistung von KL30_IN. Für Satelliten ist zusätzliche 12-V-Einspeisung oder eine eigene lokale Quelle nötig. Die präzisierte Nutzeridee „Aufbau und Checks über USB“ ist damit als Gesamtsystemversorgung weiterhin nicht umgesetzt, auch wenn der Dokumentationswiderspruch bereinigt wurde.

Fundstellen: [aktuelle Einschränkung](/Users/schmidtm/openMotorBridge/docs/de/05_power_management_ups.md:67), [D3 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:5958), [J6 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb:6325). Welche Verbraucher im USB-Test verfügbar sein müssen, muss vor der Auslegung des Versorgungspfads feststehen. Dabei wird keine 60-W-Vollast als Nutzeranforderung unterstellt.

### H04 PCBA 03 besitzt keine erkennbare Quelle für VCC_3V3

**P1.** Das Netz VCC_3V3 verbindet MCU, Codec, Analogschalter und Pull-up R9. Es hat keinen Reglerausgang und keinen externen Versorgungspin. Die vierpolige Busbuchse führt VCC_BUS, GND und USB; U_PD erzeugt VBUS_30W. Auf der Platine existiert kein eigener 3,3-V-Regler. Die Logikversorgung bleibt damit in den ausgewerteten Netzen ohne Quelle.

Fundstellen: [U1 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb:8917), [U3 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb:2164), [J_BUS im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb:2817), [beschriebene ICs](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:529). Einen festen geregelten Logikpfad ergänzen und Schaltplan, PCB und BOM daraus neu erzeugen.

### H05 PCBA 03 verwechselt geregelte 5 V mit dem variablen PD Ausgang

**P1.** F1 verbindet VBUS_30W direkt mit VCC_5V_PROT. Dasselbe VCC_5V_PROT versorgt J_AUDIO_PWR Pin 2 sowie J_ACT Pins 7/8. Ein PPTC ist keine Spannungsregelung. Die Doku beschreibt VBUS_30W selbst als 5/9/12/15/20-V-Ausgang, nennt die dahinterliegenden Intercom- und Aktuatoranschlüsse aber feste +5 V. Bei einer höheren PD-Spannung liegt diese auch hinter F1 an. Gleichzeitig nennt die Bauanleitung 12-V-Hubmagnete, während die J_ACT-Tabelle 5 V verspricht.

Fundstellen: [F1 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb:386), [J_ACT im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb:6099), [PD-Abgang](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:544), [Aktuatoranschluss](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:568). Festspannungsversorgung und verhandelten Ladeausgang elektrisch trennen; Spulenspannung und Treiberbudget verbindlich festlegen.

### H06 PCBA 03 Analogschalter ist nicht nach Datenblatt angeschlossen

**P1.** U4 TS5A3159 führt im PCB Pin 2 auf AUDIO_IO_P, Pin 4 auf VCC_3V3, Pin 5 auf GND und Pin 6 auf VOICE_OUT. Laut [TI-Pinbelegung](https://www.ti.com/lit/ds/symlink/ts5a3159.pdf) sind diese Pins GND, COM, V+ und IN. Insbesondere liegt damit die Versorgung V+ auf Masse und GND auf einem Signal. Die beschriebene automatische Analog-/Digital-Umschaltung kann so nicht funktionieren.

Fundstellen: [U4 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb:532), [U4-Funktionsbeschreibung](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:529). Symbol-Pinnummern und Footprintzuordnung korrigieren; anschließend Umschaltfunktion und nötige Zahl der Signalpfade neu prüfen.

### H07 C6 Modulbelegung passt auf PCBA 03 und 09/10 nicht zum Hersteller

**P1.** Die drei Platinen verwenden eine nicht passende Modulbelegung. Laut [Espressif C6-MINI-Datenblatt, Tabelle 3-1](https://www.espressif.com/sites/default/files/documentation/esp32-c6-mini-1_mini-1u_datasheet_en.pdf) besitzt das Modul 53 Pins; Pin 2 und 14 sind GND, 3 ist 3V3, USB-D− liegt auf 17 und D+ auf 18. PCBA 03 führt Pin 2 auf VCC_3V3, USB-D− auf 14 und D+ auf 15; ihr Footprint enthält Nummern bis 65. Auf PCBA 09/10 liegt Pin 3 auf GND statt der Versorgung. Dort ist der Footprint zudem als ESP32-S2-MINI-1U bezeichnet, obwohl der Bauteilwert C6-MINI-1U lautet.

Fundstellen: [U1 PCBA 03](/Users/schmidtm/openMotorBridge/hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb:8917), [U1 PCBA 09](/Users/schmidtm/openMotorBridge/hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_pcb:455), [U1 PCBA 10](/Users/schmidtm/openMotorBridge/hardware/kicad_omm446_intercom/openmotorbridge_omm446_intercom.kicad_pcb:455). Hersteller-Landpattern und Symbol gemeinsam übernehmen; eine Änderung des Bauteilwerts oder der Firmwarekommentare reicht nicht.

### H08 Der native C6 USB Controller erfüllt die versprochene Audio Class nicht

**P1.** Die Doku verspricht native USB Audio Class auf den C6-Pods und OMM-Modulen. Espressif dokumentiert den USB-Serial/JTAG-Block des C6 jedoch als fest auf seriellen Port und JTAG beschränkt. Er lässt sich nicht als frei konfigurierbares USB-Audiogerät betreiben. Quelle: [Espressif USB Serial/JTAG Controller](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c6/api-guides/usb-serial-jtag-console.html).

Fundstellen: [Pod-Architektur](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:500), [USB-Modus der OMM-Buchse](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:976), [OMM USB-Zusage](/Users/schmidtm/openMotorBridge/firmware/omm_module/src/omm_module_config.h:51). Serielles eigenes Audioprotokoll und standardisierte UAC sind verschiedene Architekturen; MCU oder USB-Audiobaustein entsprechend auswählen und den tatsächlichen Modus dokumentieren.

### H09 Front Node P4 ist auf einen S3 Modulfootprint gesetzt

**P1.** U1 trägt den Wert ESP32-P4-NR16, der Footprint ist jedoch ESP32-S3-WROOM-1U mit 40 Randpads plus Massepad. Der P4 ist laut [Espressif-P4-Datenblatt, Packaging](https://documentation.espressif.com/esp32-p4_datasheet_en.html) ein QFN104-Baustein. Das ist kein durch Umbenennen bestückbarer S3-Ersatz. Die Unterscheidung S3-Prototyp/P4-Serie in der Build-Anleitung behebt den vorhandenen Footprint nicht.

Fundstellen: [U1 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb:7768), [P4-Architektur](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:599), [Target-Erklärung](/Users/schmidtm/openMotorBridge/firmware/README.md:22). Einen echten P4-Schaltplan und ein P4-Layout erstellen oder den aktuellen Stand ausdrücklich als S3-Prototyp führen. Auch U9 wird als WROOM-Modul bezeichnet, liegt aber auf einem generischen QFN-16-Footprint; dessen konkrete Bestell- und Gehäusezuordnung ist separat offen.

### H10 Front Node Schnittstellenkommentare nennen nicht existierende Pins und Ports

**P2.** Kapitel 07 beschreibt einen unabhängigen USB-C-Serviceport J7; im PCB und der zugehörigen BOM fehlt J7. Der Firmwareheader erklärt J7 dagegen ausdrücklich als entfernt. Derselbe Header nennt J_SENSOR_EXT Pin 7 für MIC_I2S_DATA, obwohl der Stecker sechs Pins hat. Im PCB ist Pin 5 MIC_I2S_DATA und Pin 6 MIC_I2S_WS; SCL liegt auf Pin 4 und nicht dem ebenfalls kommentierten Pin 2.

Fundstellen: [J7-Zusage](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:614), [J_SENSOR_EXT im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb:13858), [Service- und Sensor-Pinangaben](/Users/schmidtm/openMotorBridge/firmware/front_node/src/front_node_config.h:19). Die Stecker müssen als tatsächliche Pinliste dokumentiert werden. Der Sensor-Puck selbst enthält kein Mikrofon; MK1 sitzt auf der Front-Platine, während andere Abschnitte ihn dem Puck zurechnen.

### H11 PCBA 05B besitzt keine Quelle für die 3,3 V des Hubs

**P1.** Der Handschuhfach-Hub hat als einziges IC U1 USB2514Bi. Sein +3V3-Netz enthält Versorgungspins, Kondensator und Reset-Pull-up, aber keinen Regler und keinen nach außen geführten 3,3-V-Eingang. Die Buchsen bringen VCC_5V beziehungsweise VBUS_HOST_SENSE. Ein Pfad zur Erzeugung von +3V3 ist auf dieser Platine nicht vorhanden.

Fundstellen: [U1 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_cockpit_breakout/openmotorbridge_cockpit_breakout.kicad_pcb:2528), [C_OUT1 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_cockpit_breakout/openmotorbridge_cockpit_breakout.kicad_pcb:2270), [Hubbeschreibung](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:675). Die reale Hubversorgung einschließlich benötigter Spannungsdomänen auslegen und in PCB und Fertigungsdaten ergänzen.

### H12 PCBA 05B realisiert weder die versprochene PD Regelung noch Dongle Trennung

**P1.** PHONE J3, DONGLE J4, MEDIA J5 und FRONT_NODE J2 liegen mit ihren VBUS-Pins direkt am selben VCC_5V-Netz. Es gibt auf dieser Platine keinen PD-Controller und keinen Lastschalter; als IC ist nur der USB-Hub bestückt. Damit fehlen die beschriebene 15/30-W-PD-Ausgangsregelung und ein individuell schaltbarer Dongle-VBUS. Ein Lastschalter auf dem Front-Node ist kein separat schaltbarer Ausgang am ansonsten gemeinsamen Hubnetz.

Fundstellen: [J3 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_cockpit_breakout/openmotorbridge_cockpit_breakout.kicad_pcb:3683), [J4 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_cockpit_breakout/openmotorbridge_cockpit_breakout.kicad_pcb:1768), [zugesagte Portfunktionen](/Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md:583). Den Kabel- und Strompfad zwischen sechspoligem Front-J4 und den beiden USB-C-Buchsen des Hubs vollständig spezifizieren. Signal- und Leistungsrollen dürfen nicht allein aus Portnamen abgeleitet werden.

### H13 Spiegel Pods haben zwei physische Taster im Gesamtsystem statt sechs

**P2.** PCBA 05C enthält pro Platine genau einen SW1 sowie einen vierpoligen Anschluss für LED, LED-Rückleitung, Tastersignal und Masse. Die Firmware-Targetmatrix nennt dagegen sechs Lenkertaster. Gesten auf einem Taster sind keine zusätzlichen physischen Eingänge. Der vorhandene Spiegel-Pod entspricht der Ein-Taster-Beschreibung in Kapitel 07; die abweichende Systembeschreibung muss angepasst werden.

Fundstellen: [SW1 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_mirror_pod/openmotorbridge_mirror_pod.kicad_pcb:1731), [korrekte Steckerbelegung](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:703), [sechs Taster in Targetmatrix](/Users/schmidtm/openMotorBridge/firmware/README.md:14). Positiv: dokumentierte Positionen, zwei Amber-LEDs, Steckerpins, 18,25×14-mm-Kontur und Zweilagenaufbau passen zum ausgewerteten PCB.

### H14 Sensor Puck OPT3001 Versorgungspin liegt auf Masse

**P1.** U3 OPT3001 hat PCB-Pin 1 an GND und Pin 2 an VCC_3V3. Das [TI-Datenblatt](https://www.ti.com/lit/ds/symlink/opt3001.pdf) verlangt Pin 1 als VDD und Pin 2 als ADDR. Damit ist der Lichtsensor nicht korrekt versorgt. Die Versorgung von ADDR mit 3,3 V behebt das nicht. Die I2C-Pins 4/6 sind demgegenüber als SCL/SDA angeschlossen.

Fundstelle: [U3 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_sensor_puck/openmotorbridge_sensor_puck.kicad_pcb:2648), [Lichtsensorzusage](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:734). Das echte Symbol-Pinmapping korrigieren und danach die tatsächliche I2C-Adresse im Treiber prüfen. Dieser Fehler ist im Schaltplan/PCB-Abgleich allein nicht aufgefallen, weil beide dieselbe falsche Zuordnung übernehmen.

### H15 GNSS PPS wird auf dem Sensor Puck nicht nach außen geführt

**P2.** GNSS_TIMEPULSE liegt ausschließlich an U1 Pin 7. J1/J2 führen 3,3 V, GND, I2C und zwei generische I2S-Signale, aber keinen PPS. Die Main-Telemetriedoku verspricht hardwaregenaue 1-PPS-Synchronisation für Action-Cam-Marker. Der ausgewertete Kabelweg stellt diese Hardwarezeitreferenz nicht bereit.

Fundstellen: [U1 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_sensor_puck/openmotorbridge_sensor_puck.kicad_pcb:2973), [J1 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_sensor_puck/openmotorbridge_sensor_puck.kicad_pcb:1084), [PPS-Zusage](/Users/schmidtm/openMotorBridge/docs/de/06_telemetry_blackbox_webdav.md:54). Eine benötigte PPS-Leitung bis zum auswertenden Controller tatsächlich führen oder die Zusage auf die implementierte Zeitübertragung begrenzen. Eine reine GPX-Markerfunktion belegt keine PPS-Anbindung.

### H16 Keyfob VBAT ist nur über eine Spule mit der 3V3 Schiene verbunden

**P1.** L1 verbindet VBAT direkt mit VCC_3V3. Das Netz VBAT kommt vom Akkuanschluss und Lade-IC. Auf der Platine gibt es keinen separaten Regler zwischen diesen beiden Netzen. Eine Induktivität allein regelt die Gleichspannung eines geladenen 1S-Akkus nicht auf 3,3 V. Das als VCC_3V3 bezeichnete Netz versorgt dabei MCU, SX1262 und Haptik.

Fundstellen: [L1 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb:346), [P_BAT im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb:4153), [zugesagte 3,3-V-Versorgung](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:787). Das komplette Versorgungskonzept mit realer Reglerschaltung und zulässigen Spannungen aller Verbraucher überprüfen. Die Beschriftung 4.7uH_DCDC ersetzt keine solche Schaltung.

### H17 Keyfob lötfreier Akkuanschluss fehlt und Qi Header fehlt in der BOM

**P1.** Die Anleitung verspricht einen JST-ACH-Akkuheader J_BAT. Im PCB liegt stattdessen P_BAT als LIPO_BAT_PADS auf einem R_0805-Footprint. Ein J_BAT fehlt. J_QI existiert im PCB und CPL, ist aber in der Produktions-BOM nicht enthalten. Eine vollständig lötfreie Akku- und Spulenmontage ist mit diesen Daten nicht vorbereitet.

Fundstellen: [lötfreie Montage](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:774), [P_BAT im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb:4153), [J_QI im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb:1908), [Keyfob-BOM](/Users/schmidtm/openMotorBridge/hardware/production_packages/07_smart_keyfob_pcba/07_smart_keyfob_pcba_bom_jlcpcb.csv). Stecker auslegen, bestücken und in BOM/CPL konsistent ausweisen; absichtlich manuell montierte Teile müssen gekennzeichnet sein.

### H18 Keyfob Funktionsumfang und Lagenzahl sind widersprüchlich

**P2.** Kapitel 05 beschreibt USB-C-Ladung, 350–500 mAh und einen MAX17048-Fuel-Gauge. Im PCB gibt es Qi-Empfang und BQ25100, aber keinen USB-C-Port und keinen MAX17048. Kapitel 07 nennt wiederum 180–200 mAh und zwei Lagen; das PCB enthält vier Kupferlagen. Eine Akkukapazität lässt sich aus Anschluss-Pads allein nicht bestätigen, die mechanische und elektrische Referenz ist daher festzulegen.

Fundstellen: [USB-C und Fuel-Gauge](/Users/schmidtm/openMotorBridge/docs/de/05_power_management_ups.md:203), [Keyfob-Platinenangaben](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:767), [U4 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb:4300). Das aktuelle Qi-Design als Referenz dokumentieren oder die fehlenden Funktionen tatsächlich ergänzen; den Fertigungsauftrag auf den echten Lagenaufbau abstimmen.

### H19 Radar Controller ist gleichzeitig C3 C5 und C6

**P1.** Das PCB verwendet einen ESP32-C3-WROOM-02U-Footprint, beschriftet ihn aber ESP32-C5-WROOM-1U. Die Doku-Pinmatrix bezieht sich auf C3, die Firmwarequelle erklärt C5/C3-Pinout und das Buildziel ist esp32c6. USB-, UART- und Bootpins unterscheiden sich damit schon innerhalb der projektinternen Quellen. Diese Varianten sind nicht durch einen Kommentar als identische Hardware belegt.

Fundstellen: [U1 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb:10251), [C3-Pinmatrix](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:871), [Firmware-Pinannahmen](/Users/schmidtm/openMotorBridge/firmware/radar_submcu/src/main.cpp:21), [Buildziel](/Users/schmidtm/openMotorBridge/firmware/radar_submcu/sdkconfig.defaults:2). Einen konkreten Controller mit geprüftem Landpattern und zusammenpassendem Build-/Pinprofil festlegen.

### H20 Radar TPS54302 Pins sind vertauscht

**P1.** Auf PCBA 08 liegt U3 Pin 1 auf BUCK_BOOT, Pin 2 auf VCC_12V, Pin 3 auf VCC_12V, Pin 5 auf GND und Pin 6 auf BUCK_SW. Laut [TI TPS54302](https://www.ti.com/lit/ds/symlink/tps54302.pdf) sind 1=GND, 2=SW, 3=VIN, 4=FB, 5=EN und 6=BOOT. Der Regler kann so die zugesagte 5-V-Versorgung nicht liefern. Zum Vergleich folgt die Pinzuordnung des gleichnamigen Front-Node-Reglers diesen Datenblattfunktionen; ein einheitlich verwendeter korrekter Symbolstandard fehlt.

Fundstellen: [Radar U3](/Users/schmidtm/openMotorBridge/hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb:13230), [Front U3](/Users/schmidtm/openMotorBridge/hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb:5959), [Radar-Leistungsstufe](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:835). Regler-Pinnummern korrigieren und Leistungsstufe einschließlich Bootstrap-, Feedback- und Enablebeschaltung neu prüfen.

### H21 Radar LED Treiber ist nur als leere Funktion vorhanden

**P1.** Die 36 WS2812B sind im PCB vorhanden, und ihre Zahl passt zur Doku. Die Funktion update_neopixel_halo() enthält im geprüften Firmwarestand aber nur einen Kommentar, keine Übertragung über RMT/SPI oder einen LED-Treiber. Das beschriebene autonome Warn-Stroboskop ist deshalb aus diesem Firmwarepfad nicht implementiert nachgewiesen. Die ETSI-Nachrichten-IDs allein belegen ebenfalls keinen vollständigen 5,9-GHz-Empfängerpfad.

Fundstellen: [leere LED-Ausgabe](/Users/schmidtm/openMotorBridge/firmware/radar_submcu/src/main.cpp:73), [Halo-Warnfunktion](/Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md:825). Die reale LED-Ausgabe implementieren und prüfen. Für V2X Empfängerhardware, Antennenanschluss, PHY/MAC-Unterstützung und Eingangsdatenpfad separat nachweisen; die V2X-Funktion wird in diesem Review nicht als verifiziert eingestuft.

### H22 PCBA 09 Produktionsdaten verwenden falsche Referenzen

**P1.** Im PCB ist U3=SA818-DMR, U5=ME6211C33M5G und U6=ESP32-PICO-V3-02. Die PCBA-09-BOM und CPL führen dagegen U3 als ME6211 und U5 als ESP32-PICO; U6 fehlt. Das ist keine gültige DNP-Variante: Eine Bestückungsvariante darf Teile weglassen, aber nicht dieselbe Referenz auf ein anderes Gehäuse und eine andere Funktion umdeuten. Außerdem nennt die aktuelle Variantenbeschreibung für 2.4G-only DNP U3/J_RF, während die vorhandene BOM U3 mit einem Regler belegt.

Fundstellen: [U3 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_pcb:6117), [U5 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_pcb:4869), [U6 im PCB](/Users/schmidtm/openMotorBridge/hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_pcb:5234), [PCBA-09-BOM](/Users/schmidtm/openMotorBridge/hardware/production_packages/09_omm_ucs_pcba/09_omm_ucs_pcba_bom_jlcpcb.csv), [PCBA-09-CPL](/Users/schmidtm/openMotorBridge/hardware/production_packages/09_omm_ucs_pcba/09_omm_ucs_pcba_cpl_jlcpcb.csv), [DNP-Varianten](/Users/schmidtm/openMotorBridge/docs/de/04b_omm_intercom_module.md:39). Fertigungsdaten aus demselben Layout und expliziten Variantenregeln regenerieren.

## Produktionsdaten und Quervergleich

Die Referenzen und Bauteilwerte der aktuellen Schaltplaninstanzen wurden mit den PCB-Footprints verglichen. Neun aktive Platinen stimmen dabei wörtlich überein. Beim Front-Node unterscheiden sich vor allem Zusatztexte in Passivwerten wie `100nF` und `100nF_BOOT`; diese Unterschiede wurden nicht pauschal als elektrische Fehler gezählt. Wichtig ist die Grenze dieses Checks: Ein falsches Symbol kann in Schaltplan und PCB identisch falsch sein, wie bei H14. Deshalb wurden ausgewählte kritische Pins zusätzlich direkt gegen Herstellerdaten geprüft.

Die Produktions-BOMs enthalten im Wesentlichen alle bestückbaren Referenzen. Montagebohrungen fehlen erwartungsgemäß und wurden nicht als fehlende Bauteile gewertet. Reale Ausnahmen sind J_QI bei PCBA 07 sowie die falsche Referenzzuordnung bei PCBA 09. Auf PCBA 09 und 10 steht zusätzlich ein 600-mAh-Akku in der BOM-Bezeichnung, während der PCB-Wert 1000 mAh nennt; die gewählte Kapazität muss als Variante gekennzeichnet werden.

Die Pakete 01, 03, 05, 07 und 08 enthalten zahlreiche Zeilen ohne LCSC-Nummer. Das ist kein Beweis, dass ein Bauteil nicht beschaffbar ist, aber die Daten sind damit nicht ohne Bauteilauswahl als vollständig zugeordnete SMT-Bestellung verwendbar. Bei PCBA 07 hat J_QI im CPL zudem kein Package. Die als entfernt bezeichnete PCBA 06 besitzt weiterhin ein Produktionspaket; dessen Legacy-Status sollte im Bestellablauf klar sein.

## Revalidierung der vorherigen Rückmeldungen

- **Stromversorgung P01/P02:** Die Doku nennt jetzt die Main-Bauteile LM5164 und TPS7A0533 und erklärt ehrlich, dass USB allein die Satelliten nicht speist. Der alte Textwiderspruch ist damit korrigiert. Die Nutzeridee eines über USB versorgten Werkstatt-Gesamtsystems bleibt eine offene Implementierungsanforderung; H01/H02 zeigen zusätzlich reale Hardwareprobleme.
- **Dry-Flap B07:** Die zuvor fehlende `014_pod_dry_flap.stl` ist jetzt vorhanden und als Exportziel eingetragen. Der damalige fehlende Link ist behoben.
- **Pod-Innenraum B09:** Die Doku nennt jetzt 141×61 mm Gesamtausschnitt und 93,5×61 mm Geräteraum ab X=52 mm. Das passt zur zuvor beanstandeten rechnerischen Referenz. Eine vollständige Bestückungs- und Bewegungskollisionsprüfung ist damit nicht ersetzt.
- **HMAC A03:** Die Zusage ist auf Korruptions-/Integritätserkennung eingegrenzt; ein digitaler Signaturnachweis Dritter wird ausdrücklich verneint. Das ist eine sinnvolle Korrektur. Der MAC-basierte Schlüssel bleibt öffentlich reproduzierbar und bietet entsprechend keinen belastbaren Schutz gegen einen absichtlichen Angreifer.
- **WebDAV A04:** Der Main-Uploader enthält weiterhin keinen echten Heim-WLAN-Verbindungsaufbau. Das Setzen des Uplinkflags beim Ausschalten belegt keine Verbindung. Der vollständige automatische Sync bleibt offen.
- **Mechanik:** Die bereits korrigierten Bilder und Deckelkoordinaten wurden hier nicht vollständig erneut geometrisch vermessen. Dieser Durchgang konzentriert sich auf die Platinen und ihre Schnittstellen.

## Sinnvolle Reihenfolge der Korrekturen

1. Für jede aktive Platine eine konkrete Hardwareversion mit echten Bestellteilen, Herstellersymbolen und freigegebenen Landpatterns festlegen. Zuerst H01, H06, H07, H09, H14, H19 und H20 bearbeiten.
2. Pro Platine den vollständigen Energiepfad vom Stecker bis zu jedem IC zeichnen; feste Logikschienen, PD-Ausgänge, Akku- und Aktuatorversorgung trennen. Fehlende Quellen und USV-Pfade beheben.
3. Boardübergreifende Verbindungen als Pin-zu-Pin-Kabeltabellen freigeben und Firmwarekonfigurationen daraus ableiten. Besonderes Augenmerk auf USB-Audio-Architektur, Front/Hub-Verbindung, Puck und Radar legen.
4. BOM und CPL aus genau diesen Layouts und expliziten DNP-Varianten neu exportieren. Vor jeder Bestellung Referenz, Wert, Gehäuse, Bestückungsseite und Bezugsquelle abgleichen.
5. Erst danach Funktions- und Hardwaretests ansetzen. Simulationen mit übernommenen falschen Pinannahmen können diese Fehler nicht ausschließen.

## Grenzen und gespeicherte Evidenz

Die automatisierte Inventur liest Footprints, Pads, Netznamen, Schaltplaninstanzen, Kupferlagen und Konturen direkt aus den KiCad-Dateien. Ein passender Netzname beweist keine durchgehend geroutete Leiterbahn. Eine vollständige ERC-/DRC-, Fertigungs-, Signalintegritäts-, Thermik- oder Messprüfung wurde nicht ausgeführt. Nicht jedes IC-Pinout wurde gegen ein Datenblatt geprüft; die genannten Herstellerabweichungen wurden gezielt nachgeschlagen. Weitere Fehler können deshalb bestehen.

Die im Bericht genannten 22 Punkte sind keine 22 voneinander unabhängigen Ursachen: H07/H08 betreffen mehrere Platinen, während H22 einen separaten Fertigungsexportfehler beschreibt. Der Spiegel-Pod wurde auf dokumentierte Pins und Struktur abgeglichen, damit ist aber keine elektrische Gesamtfreigabe verbunden.

Die maschinenlesbare Inventur aller elf vorhandenen Boards sowie eine Textfassung liegen dem Bericht bei. Die Quellplatinen, Firmware, Doku und Produktionsdaten wurden nicht verändert.
