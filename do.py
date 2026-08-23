import os

os.makedirs("docs/de", exist_ok=True)

docs = {}

# 01 - Systemarchitektur
docs["docs/de/01_system_architecture.md"] = """# 01 - Systemarchitektur, Universelle Satelliten-Topologie & Akustik

## 1. Problemstellung & Architekturphilosophie
Klassische Motorrad-Intercom-Systeme sind stark fragmentiert (Sena Mesh 2.0/3.0, Cardo DMC Gen1/Gen2, PMR446 Analogfunk, proprietaere Infotainment-Systeme wie Harley-Davidson Boom! Box GTS / Skyline OS). Fruehere Versuche einer Integration scheiterten an massiven Kabelbaeumen, unguenstiger Ergonomie und massiven HF-Uebersteuerungen (De-Sensing bei multiplen 2.4-GHz-Sendern auf engstem Raum).

OpenMotorBridge v8.0 loest dies durch die **universelle 4-Punkte-Satelliten-Topologie**:
- **Zentrale Steuerbox (Unter Sitzbank):** Beherbergt MCU (ESP32-S3), USV-Stromversorgung, SDIO-Ringspeicher, DSP-Audio-Mixer und Bluetooth-Transceiver. Keine stoerenden 2.4-GHz-Mesh- oder Weitbereichs-HF-Sender im Gehaeuse.
- **Satelliten-Pod 1 (Linke Fahrzeugseite):** Kassetten-Einschub fuer Primaer-Intercom (z. B. Sena Apex / Spider).
- **Satelliten-Pod 2 (Rechte Fahrzeugseite):** Kassetten-Einschub fuer Sekundaer-Intercom (z. B. Cardo Packtalk Pro / Edge DMC Gen2 oder Midland PMR446).
- **Satelliten-Pod 3 (Heckbuerzel / Gepaecktraeger):** Kombinierte Einheit aus u-blox MAX-M10S GNSS (freie 360-Grad-Sicht) und OpenMotorMesh-Transceiver (SX1262 LoRa 868 MHz) mit eigenem ESP32-C3 Co-Prozessor.
- **Cockpit / Front:** 100 % drahtlos ueber BLE 5.0 (Lenkertaster mit CR2032-Spannungsmonitoring) und autarken USB-Hub in der Frontverkleidung.

## 2. HF-Koexistenz & Raumdiversitaet
Durch die Montage von Pod 1 links und Pod 2 rechts am Fahrzeugrahmen oder an den Seitendeckeln wird ein physischer Abstand von mindestens 40 bis 50 cm realisiert. Die Fahrzeugbatterie, der Stahl-/Alurahmen und der Heckfender fungieren als HF-Schirmwand. Dies garantiert eine Entkopplung von ueber 35 dB zwischen den 2.4-GHz-Mesh-Sendern und eliminiert Blocking- und De-Sensing-Effekte vollstaendig.

## 3. Integration von OEM-Infotainment (Harley-Davidson Boom! Box GTS & Skyline OS)
- **WHIM-Emulation & Apple CarPlay / Android Auto:** OpenMotorBridge emuliert die Praesenz eines aktiven Headsets ueber simulierte Mikrofon-Widerstandsnetzwerke. Dadurch wird Apple CarPlay / Android Auto im Boom! Box GTS Display freigeschaltet, ohne dass das teure, proprietaere HD-WHIM-Modul (Wireless Headset Interface Module) benoetigt wird.
- **Nahtlose Sprachfuehrung:** Navigationsansagen der Bordelektronik werden ueber den DSP priorisiert und mit einstellbarem Ducking ueber die Intercom-Gespraeche gemischt.
"""

# 02 - PCB Hardware
docs["docs/de/02_pcb_hardware_pinout.md"] = """# 02 - PCB Hardware & Pinout-Spezifikation

Die Hauptplatine in der Zentralbox nutzt ein standardisiertes 4-Lagen FR4 TG150 ENIG Layout (85.0 x 55.0 mm, Staerke 1.6 mm).

## 1. HD26 / 2x13 Wannenstecker-Pinbelegung (Gehaeusewand-Interface)

Reihe 1: 100 % Satelliten-Pods (Pins 1 bis 12)  
Reihe 2: Power, Busse & Shield (Pins 14 bis 26)

| Pin | Signal | Beschreibung |
| :--- | :--- | :--- |
| **Pin 1** | `POD1_VCC` | 5V geschaltete Speisespannung Pod 1 (via High-Side MOSFET) |
| **Pin 2** | `POD1_NF_P` | Symmetrisches Audio Signal + (Bourns LM-NP-1001-B1L) |
| **Pin 3** | `POD1_NF_N` | Symmetrisches Audio Signal - (Bourns LM-NP-1001-B1L) |
| **Pin 4** | `POD1_OPTO_KEY` | Optokoppler Tasten-Trigger (Toshiba TLP222A) |
| **Pin 5** | `POD2_VCC` | 5V geschaltete Speisespannung Pod 2 (via High-Side MOSFET) |
| **Pin 6** | `POD2_NF_P` | Symmetrisches Audio Signal + (Bourns LM-NP-1001-B1L) |
| **Pin 7** | `POD2_NF_N` | Symmetrisches Audio Signal - (Bourns LM-NP-1001-B1L) |
| **Pin 8** | `POD2_OPTO_KEY` | Optokoppler Tasten-Trigger (Toshiba TLP222A) |
| **Pin 9** | `POD3_VCC` | 5V Dauer-Versorgung Pod 3 (Heck) |
| **Pin 10** | `POD3_UART_TX` | Datenstrom vom Heck-Co-Prozessor zur Zentralbox |
| **Pin 11** | `POD3_UART_RX` | Steuerdaten von Zentralbox zum Heck-Co-Prozessor |
| **Pin 12** | `POD3_GND` | Power- und Signalmasse Pod 3 |
| **Pin 13** | `NC` | Nicht belegt (Mechanische Trennung) |
| **Pin 14** | `KL30` | Bordnetz Dauerplus 12V (abgesichert via KFZ-Sicherung) |
| **Pin 15** | `KL15` | Bordnetz Zuendungsplus 12V (Messabgriff & Aufwach-Trigger) |
| **Pin 16** | `GND_PWR` | Bordnetz Power-Masse |
| **Pin 17** | `CAN_H` | CAN-Bus High (Fahrzeug-Telemetrie) |
| **Pin 18** | `CAN_L` | CAN-Bus Low (Fahrzeug-Telemetrie) |
| **Pin 19** | `ONEWIRE_ID` | Gemeinsamer 1-Wire ID-Bus (Erkennung aller Kassetten via DS2401) |
| **Pin 20** | `GND_SHIELD` | Schirmungs-Masse fuer Pod-Kabel |
| **Pin 21** | `AGND` | Analoge Audio-Referenzmasse |
| **Pin 22** | `RESERVE_GPIO_A`| Reservierter digitaler Ein-/Ausgang |
| **Pin 23** | `RESERVE_GPIO_B`| Reservierter digitaler Ein-/Ausgang |
| **Pin 24** | `RESERVE_I2S_DATA`| Reservierter digitaler Audio-Pfad |
| **Pin 25** | `RESERVE_I2S_CLK` | Reservierter digitaler Audio-Takt |
| **Pin 26** | `NC` | Nicht belegt |

## 2. GPIO-Mapping ESP32-S3

| GPIO | Signalname | Funktion & Peripherie |
| :--- | :--- | :--- |
| GPIO 1 | `ADC_BAT` | Messung USV-Akkuspannung via Teiler 1:2 (BQ24075) |
| GPIO 2 | `ONEWIRE_ID` | 1-Wire Bus zur Erkennung der Kassetten-IDs (DS2401) |
| GPIO 3 | `ADC_LINE_LVL` | NF-Pegelerkennung (Audio-Sense & Quittungston-Check) |
| GPIO 4 | `ADC_VIGN` | Bordnetzueberwachung Zuendung KL15 via Teiler 1:11 |
| GPIO 5 | `PORT1_KEY` | Optokoppler TLP222A Trigger Port 1 (Sena Intercom Toggle) |
| GPIO 6 | `PORT1_VCC_EN` | High-Side MOSFET Port 1 Speisespannung |
| GPIO 7 | `PORT2_KEY` | Optokoppler TLP222A Trigger Port 2 (Cardo Channel Next) |
| GPIO 8 | `PORT2_VCC_EN` | High-Side MOSFET Port 2 Speisespannung |
| GPIO 9 | `I2S_MCLK` | Master Clock Audio Codec (12.288 MHz) |
| GPIO 10 | `I2S_BCLK` | Bit Clock Audio (3.072 MHz) |
| GPIO 11 | `I2S_WS` | Word Select / LRCLK (48 kHz) |
| GPIO 12 | `I2S_DOUT` | Audio Data Out (DSP zu Helm / BT Source) |
| GPIO 13 | `I2S_DIN` | Audio Data In (Mikrofone / BT Sink) |
| GPIO 14 | `I2C_SDA` | I2C Datenbus (BMI270 IMU) |
| GPIO 15 | `I2C_SCL` | I2C Takt (400 kHz) |
| GPIO 16 | `CHG_STAT_N` | Ladezustand BQ24075 |
| GPIO 17 | `GNSS_RX` | u-blox MAX-M10S UART RX (vom Heck-Pod 3) |
| GPIO 18 | `GNSS_TX` | u-blox MAX-M10S UART TX (zum Heck-Pod 3) |
| GPIO 21 | `GNSS_PPS` | 1-PPS Zeitnormal (Jitter < 1 us) |
| GPIO 48 | `STATUS_LED` | WS2812B RGB Statusanzeige |
"""

# 03 - Audio Frontend
docs["docs/de/03_audio_frontend_isolated.md"] = """# 03 - Audio-Frontend & Symmetrische Schnittstellen

## 1. Galvanische Trennung & Symmetrierung
- Jeder analoge Intercom-Kanal (Port 1 und Port 2) ist ueber einen Bourns LM-NP-1001-B1L Audio-Uebertrager mit 1500 V RMS galvanisch isoliert.
- Verhindert Brummschleifen und hochfrequente Zuendstoerungen ueber das Massepotential des Fahrzeugs.
- Echte symmetrische Signalfuehrung (NF+ / NF-) bis in die Kassetten-Pods.

## 2. Optokoppler-Schaltung (PhotoMOS)
- Tastensimulationen erfolgen ueber prellfreie Toshiba TLP222A Halbleiter-PhotoMOS-Relais (R_ON < 1 Ohm, V_CE,sat = 0 V).
- Ein Tiefpassfilter (100 nF Keramikkondensator) und eine 5.6 V TVS-Diode am Ausgang schuetzen die Trigger-Leitung gegen Spikes und ESD.

## 3. Quittungston- & Voice-Prompt-Erkennung
Nach einem optogekoppelten Schaltpuls prueft der ADC an `ADC_LINE_LVL` innerhalb von 500 ms auf einen Audio-Burst (> -30 dBFS). Dies bestaetigt das erfolgreiche Umschalten von Kanaelen oder Betriebsmodi unabhaengig von Systemsprache oder Firmwarestand des Endgeraets.
"""

# 04 - Stromversorgung & USV
docs["docs/de/04_power_management_ups.md"] = """# 04 - Stromversorgung, USV, Unterspannungsschutz & Winter-Erhaltung

## 1. Primaer-Schaltregler (Buck Converter)
- **Regler-IC:** Texas Instruments LM5164-Q1 Synchronous Step-Down Regulator (Automotive Grade AEC-Q100).
- **Eingangsspannungsbereich:** 6.0 V bis 65 V DC dauerhaft (Transientenschutz nach ISO 7637-2 bis 100 V).
- **Ausgangsleistung:** 5.0 V DC / 1.0 A Dauerstrom zur Versorgung des Systems, der Satelliten-Pods und des LiPo-Laders.
- **Wirkungsgrad:** > 88 % im Hauptlastbereich (12 V zu 5 V bei 400 mA).

## 2. Dynamisches Power-Path Management & Integrierte USV
- **Power-Path Controller:** Texas Instruments BQ24075 mit automatischer Last- und Ladestromaufteilung.
- **USV-Akkuzelle:** Integrierter 1000 mAh Single-Cell LiPo-Akku (3.7 V Nennspannung, 4.2 V Ladeschluss) mit integrierter NTC-Temperaturueberwachung (Abschaltung Ladevorgang bei < 0 °C und > 45 °C).
- **Unterbrechungsfreies Umschalten:** Beim Wegfall von KL15/KL30 schaltet der BQ24075 innerhalb von < 5 us ohne Spannungseinbruch am 3.3V-LDO (TPS7A05) auf den Akku um.
- **Nachlauf-Phase (Graceful Shutdown):** Ermoeglicht einen 60- bis 120-sekundigen Weiterbetrieb nach Zuendung AUS fuer:
  - Finalisierung und Flush des GPX-Dateisystems auf MicroSD.
  - Suche nach bekannten Heim-WLAN-SSIDs und Durchfuehrung des WebDAV-Uploads.
  - Geordnetes Senden von BLE-Disconnect-Events.

## 3. Kfz-Transienten-, EMV- & Verpolschutz
- **Ueberspannungs- & Spikeschutz:** Littelfuse SMCJ36CA Bidirektionale TVS-Diode (36 V Standoff, 58.1 V Clamping @ 25.8 A).
- **Verpolschutz:** Diodes Inc. DMP6023L P-Kanal MOSFET in der Masseleitung mit extrem niedrigem Durchlasswiderstand (R_DS(on) < 25 mOhm).
- **Filterung:** Zweistufiger LC-PI-Filter (10 uH Shielded Automotive Inductor + 2x 10 uF X7R 100V Keramikkondensatoren) am KL30/KL15-Eingang.

## 4. Bordbatterie-Ueberwachung, Unterspannungsschutz & Winter-Erhaltung

### 4.1 Spannungs-Messpfad & Batterie-Chemie
Die Bordnetzspannung an KL15 und KL30 wird ueber hochohmige Spannungsteiler (100 kOhm / 10 kOhm, Teiler 1:11) an `PIN_ADC_VIGN` (GPIO 4) und `ADC_BAT` mit 12-Bit Aufloesung erfasst:

| Batterietyp | Nennspannung | Warnschwelle (Low-Bat Alert) | Abschaltschwelle (Hard Cut-Off) |
| :--- | :--- | :--- | :--- |
| **Blei-Saeure / AGM / Gel** | 12.0 V - 12.8 V | 12.0 V | **11.8 V** |
| **Lithium-Eisenphosphat (LiFePO4)** | 13.2 V - 13.6 V | 13.0 V | **12.8 V** |

### 4.2 Mehrstufige Abschalt-Logik (Anti-Tiefentladung)
1. **Stufe 1 - Normaler Ruhezustand (KL15 = AUS, KL30 > Schwelle):** ESP32-S3 im Light Sleep / Deep Sleep mit Wake-Up ueber GPIO-Pegelaenderung an KL15. Ruhestrom: < 1.2 mA.
2. **Stufe 2 - Low-Battery Deep Sleep (KL30 < Abschaltschwelle):** Deaktivierung aller Power-Gates und Wechsel in den ULP Deep Sleep (< 25 uA).
3. **Stufe 3 - Winter-Storage-Mode (Langzeit-Stillstand ueber Monate):** Nach > 14 Tagen Stillstand trennt ein bistabiles Power-Latch-Gate die Elektronik komplett von KL30.
"""

# 05 - Mechanische Konstruktion
docs["docs/de/05_mechanical_enclosure_pods.md"] = """# 05 - Mechanische Konstruktion: Zentralbox, Dichtungskonzept & Universal-Kassetten-Pods

## 1. Gehaeuse Typ A: Zentrale Steuerbox (Unter Sitzbank)
- **Aussenabmessungen:** 95.0 x 65.0 x 24.0 mm (ohne Befestigungslaschen).
- **Material & Fertigung:** PA12 im HP Multi Jet Fusion (MJF) 3D-Druck, kugelgestrahlt, im Heissbad schwarz chemisch geglaettet und hydrophob versiegelt.
- **Schutzart:** IP67.

### 1.1 Sandwich-Aufbau & Platinenbefestigung
1. **Bodenwanne:** Vertiefte Akkutasche (52.0 x 36.0 x 6.5 mm) fuer den 1000 mAh LiPo-Akku, gedaempft durch 2.0 mm EPDM-Moosgummi. Vier Ruthex M3 x 5.7 mm Messing-Gewindeeinsaetze.
2. **Elektronik-Ebene:** 4-Lagen-Platine (85.0 x 55.0 mm) auf vier 4.0-mm-Domen mit M3 x 6 mm Torx-Schrauben (ISO 14581, Edelstahl A2, Loctite 243) fixiert.
3. **Gehaeusedeckel:** Verschraubt ueber sechs M3 x 12 mm Zylinderschrauben (ISO 4762) mit 0.8 Nm Anzugsmoment.

### 1.2 Dichtungskonzept & Druckausgleich
- **Umlaufende Nut-Feder-Dichtung:** Silikon-Rundschnur (Shore 45-50 A, D = 1.8 mm), definiert um 30 % auf 1.25 mm vorkomprimiert.
- **Druckausgleich:** Gore Automotive Vent AVS 41 mit ePTFE-Membran (M8 x 1.25).
- **HD26-Wandbuchse:** IP67 Flansch mit EPDM-Flachdichtung, intern ueber 26-poliges Flachbandkabel auf 2x13 Wannenstecker entkoppelt.

## 2. Gehaeuse Typ B: Universeller Satelliten-Pod (Identisch fuer Pod 1, 2 und 3)
- **Abmessungen Schacht:** 64.0 x 46.0 x 23.5 mm.
- **Elektronik-Kassette:** 54.0 x 37.5 x 17.0 mm (PA12 MJF).
- **Kontaktblock:** 6-poliges Mill-Max Pogo-Pin-Array (Serie 824-22-006-00-001101, Raster 2.54 mm, 1.4 mm Arbeitshub) mit Silikon-Formschuhdichtung gegen vergoldete ENIG-Pads.
- **3-Stufen-Sicherheitsarretierung:**
  1. *Snap-Lock:* POM-C Federklinken mit akustischem Klick.
  2. *Cam-Lock:* Stirnseitiger 90-Grad-Edelstahl-Drehriegel blockiert Klinken formschluessig gegen Stoesse > 20 g.
  3. *Push-to-Eject:* Gummierte Hebelwippe wirft Kassette nach Entriegelung um 8.0 mm aus.
- **Befestigung:** M5-Rueckenplatte fuer Flachmontage oder CNC-Rohrschellen (22.0 mm, 28.6 mm, 1 Zoll).
"""

# 06 - Dynamische Profile
docs["docs/de/06_dynamic_profiles_spec.md"] = """# 06 - Dynamische Hardwareprofile (LittleFS JSON)

Die Profile in `/profiles/` steuern Gain, Rauschunterdrueckung, Pegel, DLE-Boni und RF-Hardening dynamisch beim Einstecken einer Kassette.

## 1. Referenz-Profile
- `sena_apex.json`: Sena Apex / Apex Plus (Mesh 3.0, 32 Nodes, DLE +60 Pkt., Bluetooth Classic deaktiviert).
- `sena_legacy.json`: Sena Spider / 50S / 30K (Mesh 2.0, 24 Nodes, DLE +30 Pkt.).
- `cardo_dmc_gen2.json`: Cardo Edge / Pro (DMC 2.0, 32 Nodes, Open DMC, DLE +60 Pkt., Bluetooth Classic deaktiviert).
- `cardo_dmc_legacy.json`: Cardo Bold / Black (DMC 1.0, 15 Nodes, DLE +30 Pkt.).
- `pmr446_gateway.json`: Midland G9 Pro / Analogfunk VOX / PTT-Relay Profil.
"""

# 07 - MicroSD, BGH & WebDAV
docs["docs/de/07_microsd_bgh_webdav.md"] = """# 07 - MicroSD-Speicher, BGH-Ringspeicher & WebDAV-Sync

## 1. Speicheranbindung
- 4-Bit SDIO-Bus (40 MHz) angebunden an den ESP32-S3 fuer Durchsatzraten > 12 MB/s.
- Dateisystem: FAT32 mit dynamischer Sektor-Pufferung.

## 2. Ringspeicher & BGH-Konformitaet (BGH VI ZR 233/17 / DSGVO)
- Tourdaten werden als rollierender Puffer in `/tracks/` gespeichert.
- Sinkt der freie Speicher unter 200 MB, loescht die Firmware automatisch die aeltesten ungeschuetzten GPX-Dateien in 50-MB-Bloecken.
- Favoriten und manuell markierte Abschnitte (`*.fav.gpx`) sind dauerhaft vor dem Ueberschreiben geschuetzt.

## 3. WebDAV-Upload im Heim-WLAN
- Beim Ausschalten der Zuendung (KL15 < 11.8 V) scannt das System fuer 60 s nach bekannten SSIDs.
- Wird ein konfiguriertes Heim-WLAN erkannt, laedt ein TLS 1.3 WebDAV-Client neue Touren vollautomatisch auf Nextcloud oder Synology hoch (ca. 1.8 MB/s).
- Nach erfolgreichem Upload schaltet sich die Box geordnet in den Deep Sleep.
"""

# 08 - DSP Audio-Engine
docs["docs/de/08_dsp_audio_engine.md"] = """# 08 - DSP Audio-Engine & Betriebsmodi

## 1. Prioritaeten- & Ducking-Matrix
Der DSP-Task auf Core 1 mischt Audioquellen latenzfrei (< 8 ms) ueber Raised-Cosine-Fadekurven:

| Prioritaet | Signalquelle | Ducking-Daempfung | Attack-Zeit | Release-Zeit |
| :--- | :--- | :--- | :--- | :--- |
| **Prio 1** | Navi-Ansagen (Smartphone/Boom! Box) | -12 dB | 15 ms | 800 ms |
| **Prio 2** | Intercom Port 1 & 2 (Sena / Cardo) | -8 dB | 25 ms | 500 ms |
| **Prio 3** | Musik (A2DP Streaming) | 0 dB (Hintergrund) | -- | -- |

## 2. Betriebsmodi
- **Standard Mode:** Beide Intercom-Ports aktiv, automatische Ducking-Mischung zum Fahrerhelm.
- **Single Rider Mode:** Port 2 stummgeschaltet, volle Konzentration auf Fahrerhelm und Navi.
- **Cruise Mode:** Bluetooth-Helmverbindung getrennt; Infotainment schaltet auf die Harley-Bordlautsprecher um.
"""

# 09 - Firmware-Architektur
docs["docs/de/09_firmware_architecture.md"] = """# 09 - Firmware-Architektur (C++ / FreeRTOS)

Die Firmware basiert auf ESP-IDF v5.x und FreeRTOS mit strikter CPU-Core-Trennung auf dem ESP32-S3:

## 1. Core-Aufteilung (Dual Core @ 240 MHz)
- **CORE 0 (Kommunikation & System):**
  - BLE Server (PWA Dashboard Verbindung)
  - BLE Client (Lenkertaster mit Batterie-Service 0x180F)
  - 1-Wire Kassetten-Manager (DS2401 ROM Search)
  - Opto-Puls-Sequenzer (TLP222A)
  - WebDAV TLS 1.3 Client (Nextcloud / Synology)
  - SDIO Logging & BGH Purge Manager
- **CORE 1 (Audio DSP & Echtzeit):**
  - I2S Audio DMA Receiver & Transmitter
  - Raised-Cosine Ducking Engine
  - ADC Peak Level Detector

## 2. TLP222A Puls-Synthese
Tastendruecke werden exakt getaktet:
- **Single Click (Mesh On/Off):** 200 ms aktiv, > 300 ms Pause.
- **Channel Next Pulse:** 1000 ms aktiv, > 500 ms Pause.
"""

# 10 - Web Bluetooth Dashboard
docs["docs/de/10_web_bluetooth_dashboard.md"] = """# 10 - Web Bluetooth Dashboard & PWA Frontend

## 1. Architektur & Offline-Faehigkeit
Das Dashboard ist eine vollstaendig autarke Progressive Web App (PWA) basierend auf standardisiertem HTML5, CSS3 und ES6 JavaScript. Die App kommuniziert ueber die Web Bluetooth API (WebBLE) direkt mit dem ESP32-S3 der Zentralbox - ohne Cloud-Zwang oder externe Serverabhaengigkeiten.
- **Lokaler Offline-Speicher:** GPX-Touren koennen ueber BLE direkt heruntergeladen und in der lokalen IndexedDB des Browsers gesichert werden.

## 2. Telemetrie & Steuerungsfunktionen
- **Echtzeit-Telemetrie:** Ueberwachung der Bordnetzspannung (KL15/KL30), USV-Akkuspannung (BQ24075) und CR2032-Batteriestatus des BLE-Lenkertasters (Service 0x180F).
- **Audio-Matrix-Steuerung:** Interaktiver Umschalter fuer Betriebsmodi (Standard, Single Rider, Cruise Mode) sowie Schieberegler fuer Ducking-Schwellwerte und Gain.
- **Kassetten- & Profilmanager:** Erkennung der via 1-Wire gesteckten Module, Anzeige der aktiven Hardwareprofile und Ground-Truth-Kanalwahl mit Re-Sync-Trigger.
- **Kassetten-Onboarding-Wizard:** Schritt-fuer-Schritt-Anleitung bei Neu-Kopplung (Bluetooth Classic am Intercom deaktivieren, Pairings loeschen, reinen Mesh-Betrieb erzwingen).
"""

# 11 - OpenMotorMesh
docs["docs/de/11_openmotormesh_dle_election.md"] = """# 11 - OpenMotorMesh (OMM) - Protokoll-Stack, DLE & Cross-Domain Audio

OpenMotorMesh (OMM) ist ein hierarchisches, latenzoptimiertes Mesh-Routing-Protokoll, das speziell fuer hochdynamische Fahrzeugverbaende im Ad-hoc-Betrieb (868 MHz LoRa & 2.4 GHz IEEE 802.15.4) entwickelt wurde. Es verbindet proprietaere Audio-Inseln (Sena Mesh, Cardo DMC) mit einem offenen, IP-faehigen Daten- und Voice-Backbone.

## 1. Layer 2: Schlanker MAC-Layer (3GPP LTE-Anlehnung)
Um Kollisionen bei schnellen Gruppenfahrten ohne feste Basisstation zu vermeiden, nutzt OMM einen abgeleiteten Mini-Cellular TDMA/CSMA-Hybrid-Frame (100 ms Superframe-Dauer):
- **Beacon Slot (10 ms):** DLE Leader Sync & Clock Normal
- **Control Slot (10 ms):** Join/Leave & Routing Requests
- **Voice Slots (TDMA, 4x 15 ms = 60 ms):** Stream 1 (Master Voice), Stream 2 (Relay Voice)
- **CSMA Slots (20 ms):** Ad-hoc Daten, GPS Telemetrie, Alerting

### Frame-Header Definition (Layer 2 Frame - 5 Bytes)
- `VER` (2 Bit): Protokollversion (01 = v8.0)
- `PRIO` (2 Bit): 00 Notfall/SOS, 01 Echtzeit-Sprache (RTP), 10 Telemetrie, 11 Hintergrund-Sync
- `FRAME_TYPE` (4 Bit): Beacon (0x1), Route Request (0x2), Route Reply (0x3), Voice Data (0x4), Telemetrie (0x5), ACK (0x6)
- `NETWORK_ID` (16 Bit PAN ID), `SOURCE_NODE_ID` (16 Bit), `DESTINATION_NODE_ID` (16 Bit), `SEQUENCE_NUM` (8 Bit)

## 2. Layer 3: Stateless IPv6 & 6LoWPAN
- **Adressierung:** Link-lokale IPv6-Adresse (fe80::/64) abgeleitet von der 64-Bit Chip-UID (DS2401).
- **6LoWPAN Kompression (RFC 6282):** Reduziert den 40-Byte IPv6-Header auf bis zu 2 bis 4 Bytes (LOWPAN_IPHC).
- **Routing:** Ad-hoc On-Demand Distance Vector (AODV-R) basierend auf LQI, RSSI und DLE-Score.

## 3. Layer 4 & Audio: RTP & Opus Voice Streaming
- **Voice-Codec:** Opus Audio mit SILK-Modus (12 kbps VBR, 20 ms Frame-Groesse).
- **RTP-Kompression:** Reduziert auf 3 Bytes Header (Sequence 16-Bit + Timestamp 8-Bit Delta).
- **Adaptiver Jitter-Buffer:** Dynamische Latenzanpassung im DSP (30 bis 80 ms).

## 4. Dynamic Leader Election (DLE) Algorithmus
Score_DLE = S_HW + S_PWR + S_GNSS + S_LORA + S_UPTIME

| Parameter | Bedingung | Punkte |
| :--- | :--- | :--- |
| **S_HW (Hardware Tier)** | Sena Apex (Mesh 3.0) ODER Cardo Edge (DMC Gen2) gesteckt | +60 Pkt. |
| | Sena Legacy / Cardo DMC Gen1 gesteckt | +30 Pkt. |
| **S_PWR (Stromversorgung)** | Zuendung aktiv (KL15 > 12.5 V) | +20 Pkt. |
| | Pufferbetrieb (USV-Akku > 3.8 V) | +5 Pkt. |
| **S_GNSS (Positionsstabilitaet)** | 3D Fix mit PDOP < 1.5 | +10 Pkt. |
| **S_LORA (Link-Qualitaet)** | Durchschnittlicher Nachbar-RSSI > -85 dBm | +10 Pkt. |
| **S_UPTIME (Hysterese-Schutz)** | Bereits aktiver Leader (verhindert Flattern) | +15 Pkt. |
"""

# 12 - GNSS Multi-Constellation & IMU
docs["docs/de/12_gnss_track_lifecycle_video.md"] = """# 12 - GNSS Multi-Constellation, IMU Traegheitsnavigation & Video-Sync

Das OMB-TourLog-Subsystem kombiniert hochpraezise Satellitennavigation mit inertialsensorischer Koppelnavigation (Dead Reckoning), um auch in Tunnels, engen Schluchten und bei Abschattungen lueckenlose Tracks mit vollstaendiger Fahrzeugdynamik aufzuzeichnen.

## 1. 15-State Extended Kalman Filter (EKF) & Traegheitsnavigation
Faellt das Satellitensignal aus, schaltet das System nahtlos auf Traegheitskopplung um. Der EKF schaetzt kontinuierlich folgende Zustaende:
- Position im Navigationskoordinatensystem (Nord, Ost, Hoehe)
- Geschwindigkeitsvektor ueber Grund
- Orientierungsquaternion (Schraeglage / Lean Angle, Nickwinkel, Gierwinkel)
- Dynamischer Sensor-Bias von Beschleunigungsmesser und Gyroskop (Bosch BMI270)

### Schraeglagen- und Zentrifugalkraft-Berechnung
Lean_Angle = arctan((v * yaw_rate) / g)  
Das Filter unterscheidet anhand der Querbeschleunigung und Gierrate zuverlaessig zwischen echter Kurvenschraeglage und statischer Fahrbahnneigung.

## 2. Track-Lifecycle & Intelligente Segmentierung
- **Auto-Start:** Startet eine neue Tour-Datei (`YYYY-MM-DD_HH-MM-SS.gpx`), sobald die Zuendung an ist und das Bike sich laenger als 10 s mit > 5 km/h bewegt.
- **Segment-Split (`<trkseg>`):** Bei Ampel- oder Tankstopps unter 15 Minuten wird die GPX-Datei nicht geschlossen, sondern ein neues Track-Segment geoeffnet.
- **Auto-Finalisierung:** Nach 15 Minuten Dauerstillstand oder 60 Sekunden nach Zuendung AUS wird die GPX-Struktur sauber abgeschlossen und fuer den WebDAV-Upload markiert.

## 3. GPX 2.0 Telemetrie & 1-PPS Video-Sync
- **Telemetrie-Tags:** Geschwindigkeit, Schraeglage, Beschleunigungswerte und Satelliten-Metadaten pro Trackpunkt.
- **1-PPS Hardware-Sync:** Das u-blox MAX-M10S Modul liefert an `PIN_GNSS_PPS` einen hochpraezisen 1-Hz-Takt mit Zeitjitter < 1 us.
- **Video-Marker:** Shutter-Events vom BLE-Lenkertaster werden mit Mikrozeitstempel eingebettet, um Actioncam-Footage (GoPro/Insta360) framegenau mit Schraeglagendaten zu ueberblenden.
"""

# 13 - Heck-Pod 3
docs["docs/de/13_rear_pod3_transceiver_arch.md"] = """# 13 - Heck-Pod 3 & Digitale OMM-Transceiver-Architektur

Der Heck-Pod 3 buendelt Positionsbestimmung (GNSS) und digitalen Weitbereichsfunk (OpenMotorMesh) in einem aerodynamischen Gehaeuse am Heckbuerzel oder Gepaecktraeger.

## 1. Hardware-Architektur im Heck-Pod
- **GNSS Engine:** u-blox MAX-M10S mit 25 x 25 mm Keramik-Patchantenne fuer gleichzeitigen 4-System-Empfang (GPS, GLONASS, Galileo, BeiDou).
- **LoRa Transceiver:** Semtech SX1262 (+22 dBm PA, 868 MHz) fuer OpenMotorMesh Weitbereichs-Routing.
- **Co-Prozessor:** ESP32-C3 (32-Bit RISC-V @ 160 MHz) uebernimmt lokales NMEA/UBX-Parsing bei 10 Hz und LoRa Frame En-/Decodierung.
- **Schnittstelle zur Zentralbox:** High-Speed UART (460.800 Baud) ueber ein 4-Ader-Kabel (VCC 5V, UART TX, UART RX, GND).

## 2. Vorteile der Auslagerung
- Stoerungsfreie 360-Grad-GNSS-Sicht ohne Daempfung durch Fahrer oder Verkleidung.
- 868-MHz-Sender strahlt am Heck ab - ohne Beeinflussung der 2.4-GHz-Mesh-Systeme an den Seiten.
- Entlastung der Haupt-MCU (ESP32-S3) von Interrupt-Spitzen beim NMEA-Parsing.
"""

# 14 - EMV & Hardening
docs["docs/de/14_emv_rf_hardening.md"] = """# 14 - EMV-, HF- & Umwelthaertung

## 1. Kfz-Transienten- und Ueberspannungsschutz
- **Bordnetz-Absicherung:** Konformitaet nach ISO 7637-2 (Pulse 1, 2a, 3a/b bis 100 V).
- **Ueberspannungsschutz:** Littelfuse SMCJ36CA TVS-Diode (36 V Standoff) am Eingang des LM5164 Schaltreglers.
- **Verpolschutz:** Diodes Inc. DMP6023L P-Kanal MOSFET in der Masseleitung (R_DS(on) < 25 mOhm).
- **Entstoerung:** Zweistufiger PI-Filter (Ferrit-Induktivitaet 10 uH / 3 A + Keramikkondensatoren X7R) am 12V-Bordnetzeingang.

## 2. HF-Entkopplung & Raumdiversitaet
- Durch die raeumliche Trennung von Pod 1 (links) und Pod 2 (rechts) ueber das Fahrzeugchassis wird eine minimale Freiraumdaempfung von > 35 dB sichergestellt.
- Alle Zuleitungen (NF-Audio, UART, 1-Wire) sind ueber geschirmte Leitungen gefuehrt; Schirme liegen ueber niederinduktive Masseflaechen am HD26-Stecker an.

## 3. Umweltschutz & Beschichtung
- Vollflaechige Schutzlackierung aller Platinen nach IPC-CC-830B (Conformal Coating) gegen Feuchtigkeit und Salzspruehnebel.
- Gehaeuse nach IP67 spezifiziert mit Gore-Druckausgleichselement Typ AVS 41.
"""

# 15 - BOM & Fertigung
docs["docs/de/15_bom_manufacturing.md"] = """# 15 - BOM & Fertigungsleitfaden

## 1. Kern-Bauelemente (SMT-Bestueckung via JLCPCB)

| Designator | Bauteil | Hersteller / MPN | Gehaeuse | Funktion |
| :--- | :--- | :--- | :--- | :--- |
| U1 | ESP32-S3-WROOM-1-N16R8 | Espressif Systems | SMD Modul | Haupt-MCU (Dual-Core, 16 MB Flash, 8 MB PSRAM) |
| U2 | LM5164-Q1 | Texas Instruments | SOIC-8-EP | Automotive 65V Buck Converter |
| U3 | BQ24075RGTR | Texas Instruments | VQFN-16 | Dynamisches Power-Path Management & LiPo-Lader |
| U4 | BMI270 | Bosch Sensortec | LGA-14 | 6-Achsen IMU fuer Schraeglagen- & Bewegungserkennung |
| T1, T2 | LM-NP-1001-B1L | Bourns Inc. | SMD Uebertrager | 1:1 Audio-Uebertrager (1500 V RMS Trennung) |
| OC1, OC2 | TLP222A(F) | Toshiba | SOP-4 | Halbleiter-PhotoMOS-Relais fuer Tastensimulation |
| J1 | 2x13 Wannenstecker | Standard 2.54 mm | THT | Interner Pfostenverbinder zur HD26-Buchse |
| CN1 | HD26 Buchse IP67 | Amphenol / D-Sub HD | Flansch | Wasserdichte Haupt-Schnittstelle in der Gehaeusewand |

## 2. Fertigungshinweise & CPL-Ausrichtung
- **CPL-Rotationsabgleich:** Bei der JLCPCB-Bestueckung ist auf die Pin-1-Ausrichtung der Bourns-Uebertrager und TLP222A Optokoppler im CPL-File zu achten (0-Grad vs. 180-Grad Rotation).
- **Gehaeuse (Typ A & B):** HP Multi Jet Fusion (MJF) in PA12 Schwarz, kugelgestrahlt und im Heissbad versiegelt.
- **Dichtungen:** Massgefertigte Silikon-O-Ringe (Shore-Haerte 50 A) fuer Deckel und Kassetten-Einschuebe.
- **Pogo-Pins:** Mill-Max 824-22-006-00-001101 Federkontaktleiste mit 1.4 mm Arbeitshub.
"""

# 16 - Legal & DSGVO
docs["docs/de/16_legal_compliance_dsgvo.md"] = """# 16 - Rechtliche Compliance, Lizenzen & DSGVO

## 1. Open-Source-Lizenzierung
- **Hardware & CAD:** CERN Open Hardware Licence Strongly Reciprocal v2 (CERN-OHL-S v2).
- **Firmware & Software:** GNU General Public License v3.0 (GPL-3.0).
- **Dokumentation:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).

## 2. Kfz- und Funk-Zulassung
- **ECE R10 Rev. 6:** Einhaltung der Grenzwerte fuer elektromagnetische Vertraeglichkeit im Kfz-Betrieb.
- **RED 2014/53/EU:** Konformitaet der Funkmodule (ESP32-S3, ESP32-C3, SX1262 LoRa) mit den europaeischen Frequenz- und Leistungsnormen.

## 3. Datenschutz & BGH-Konformitaet (BGH VI ZR 233/17)
- **Anlassbezogenes Logging:** Daten werden ausschliesslich lokal auf der MicroSD-Karte im rollierenden Puffer gespeichert.
- **Automatisches Ueberschreiben:** Ungeschuetzte Tracks werden bei Erreichen des Schwellwerts (< 200 MB freier Speicher) zyklisch ueberschrieben.
- **Kein Cloud-Zwang:** Der optionale WebDAV-Upload erfolgt ausschliesslich in private Benutzernetzwerke.
"""

# 17 - Quellen & Normen
docs["docs/de/17_standards_references.md"] = """# 17 - Quellen- & Normenverzeichnis

## 1. Normen & Richtlinien
- **ISO 7637-2:** Strassenfahrzeuge - Elektrische Stoerungen durch Leitung und Kopplung.
- **ETSI EN 300 328:** Breitband-Uebertragungssysteme im 2.4-GHz-ISM-Band.
- **ETSI EN 300 220:** Funkanlagen mit geringer Reichweite (SRD) im Bereich 25 MHz bis 1000 MHz (LoRa 868 MHz).
- **IPC-CC-830B:** Qualifikation und Leistungsfaehigkeit von Schutzlacken fuer Leiterplatten.

## 2. Protokoll-Spezifikationen
- **Bluetooth SIG:** Battery Service Specification v1.0 (UUID `0x180F`), Battery Level Characteristic (`0x2A19`).
- **u-blox M10 Interface Description:** UBX- und NMEA-Protokollreferenz (Docu-Nr. UBX-21035062).
- **Cardo Systems:** Dynamic Mesh Communications (DMC 2.0 Open Intercom Referenz).
- **Sena Technologies:** Mesh 2.0 / 3.0 Intercom Operational Specs.
"""

for path, content in docs.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"OK: {path}")

print("\nAlle 17 Kapitel erfolgreich auf den maximalen, vollstaendigen Stand aktualisiert.")
