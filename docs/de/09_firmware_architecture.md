# 09 - Firmware-Architektur, FreeRTOS Tasks & Rollback-OTA

Dieses Dokument spezifiziert die systemweite Firmware-Architektur der OpenMotorBridge v8.5 / v9.0 Clean Architecture: die Multi-Core-Aufteilung des ESP32-S3 Hauptcontrollers auf der Zentralbox (`PCBA 01`), des ESP32-S3 Front-Knotens (`PCBA 05`), des deterministischen **All-UWB Backbones (Qorvo DW3110 / 6.489 GHz Ch. 5, Latenz < 0,4 ms)** zu allen Satelliten (Front-Node, Bucht 1, Bucht 2, Heckradar), der **Group Split Fallback Engine**, der LittleFS-Profil-Engine sowie der **Dual-Bank Rollback-OTA-Architektur** gegen Stromausfälle während des Flashvorgangs.

---

## 1. Multi-Core & Multi-MCU Systemarchitektur

In v8.5 / v9.0 ist das Gesamtsystem auf eine strikte **All-UWB-Stern-/Mesh-Topologie** standardisiert. Sämtliche Daten- und Steuerverbindungen zwischen Zentralbox und externen Knoten erfolgen ausschließlich über Ultra-Wideband (Qorvo DW3110); Kassetten-Buchten und Heckradar erhalten über den Deutsch DTM-12 Kabelbaum ausschließlich reine DC-Stromversorgung:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        DIE FIRMWARE-KONTROLLER IM SYSTEMVERBUND                        │
├──────────────────────────────────────────────────────┬─────────────────────────────────┤
│ 1. ZENTRALBOX (ESP32-S3 Dual-Core, PCBA 01)          │ 2. FRONT-NODE (ESP32-S3, PCBA 05)│
├──────────────────────────────────────────────────────┼─────────────────────────────────┤
│ • Core 0: All-UWB Backbone, SX1262 LoRa 868, BLE,    │ • Core 0: UWB-Backbone, SAM-M10Q│
│   Power-Sequencing, UWB Cartridge & Radar Dispatch   │   Multi-GNSS, CAN, USB-PD, PTT  │
│ • Core 1: Echtzeit 48 kHz Audio-DSP, Ducking, AGC    │ • Core 1: Knowles Vector-DSP    │
├──────────────────────────────────────────────────────┼─────────────────────────────────┤
│ 3. SMART CARTRIDGES (CH32V003 + DW3110, PCBA 03)     │ 4. HECK-RADAR (RP2040 + DW3110) │
├──────────────────────────────────────────────────────┼─────────────────────────────────┤
│ • Bucht 1 (Links) & Bucht 2 (Rechts) All-UWB SMT     │ • Wheeltec MR20 mmWave Radar    │
│ • Mechatronische 4-Aktuator-Puls-Sequenzierung       │ • 20 Hz Tracking-Vektoren via   │
│ • 4x N-MOSFET AO3400A direkt auf Platinenunterseite  │   UWB; 12V DC-Power vom DTM-12  │
└──────────────────────────────────────────────────────┴─────────────────────────────────┘
```

### 1.1 Core-Aufteilung des ESP32-S3 Hauptcontrollers der Zentralbox (240 MHz)

#### CORE 0 (Kommunikation, Telemetrie, UWB-Backbone & Power-Sequencing):
- **All-UWB Backbone Driver (`uwb_vehicle_backbone.cpp`):** Deterministische SPI-Kommunikation mit dem Qorvo DW3110 Transceiver auf `B.Cu`. Empfängt Lenker-PTT-Events ($< 0{,}4\,\text{ms}$), Knowles MEMS dB(A)-Schallpegelwerte und 10 Hz Multi-GNSS-Pakete vom Front-Knoten, 20 Hz Zielvektoren vom Heckradar sowie Handshake- und Telemetriedaten von den Kassetten in Bucht 1 und 2.
- **UWB Smart Cartridge Dispatcher (`uwb_cartridge_dispatcher.cpp`):** Verwaltet die Funk-Interaktion mit den Smart Cartridges (PCBA 03) in Bucht 1 und 2. Überträgt 1-Byte Mechatronik-Opcodes (`UWB_PKT_CARTRIDGE_OPCODE`) drahtlos in $< 0{,}4\,\text{ms}$ zur Ansteuerung der 4 AO3400A N-MOSFETs auf der Kassette; empfängt Bestätigungen (`UWB_PKT_CARTRIDGE_ACK`).
- **Gestaffeltes Power-Sequencing (`power_sequencer.cpp`):** Steuert die High-Side Power-Switches auf PCBA 01 zur Vermeidung von Einschalt-Stromspitzen beim Booten:
  - $T = 0\,\text{ms}$: Zentralbox (PCBA 01) und Front-Node (PCBA 05) booten sofort bei Zündung EIN (KL15).
  - $T = 200\,\text{ms}$: Bucht 1 (+5V DC via TPS2051B / High-Side Schalter).
  - $T = 350\,\text{ms}$: Bucht 2 (+5V DC via TPS2051B / High-Side Schalter).
  - $T = 500\,\text{ms}$: Heckradar (+12V DC geschaltet).
- **Hardware-Taster `SW1` & Roaming-Manager (`pairing_roaming_mgr.cpp`):**
  - Überwacht Taster `SW1` (`SW_PAIR_RESET`) auf PCBA 01: 3 Sekunden Halten versetzt das System in den UWB-Pairing-Modus für neue Kassetten; 10 Sekunden Halten löscht alle NVS-Schlüssel (Hard-Purge).
  - Unterstützt Multi-Vehicle Roaming: Kassetten können bis zu 4 autorisierte Fahrzeug-Schlüssel im lokalen Flash/NVS speichern.
  - Alternativ: Pairing-Reset über PWA-Companion App (BLE) oder Halten der Lenker-PTT für 5 s beim Einschalten der Zündung.
- **UWB Radar Telemetrie Parser (`uwb_radar_parser.cpp`):** Empfängt 20 Hz Radar-Objektvektoren (TTC, Distanz, Relativgeschwindigkeit) von PCBA 08 via UWB (`UWB_PKT_RADAR_TARGETS`), berechnet Kollisionsrisiken und triggert bei Bedarf Audio-Ducking (Prio 1) und Spiegel-LEDs.
- **LoRa 868 MHz Mesh Engine (`lora_mesh_engine.cpp`):** Direkte SPI-Anbindung an den onboard Semtech SX1262 Transceiver auf PCBA 01 (24/7 USV-gepuffert für Diebstahl-Sentry und Gruppen-Telemetrie).
- **BLE GATT Server (`ble_service_server.cpp`):** Web-Bluetooth Anbindung für das PWA-Dashboard (`0x180D`, `0x180A`, `0xFFE0`).
- **Group Split Fallback Engine (`group_split_rescue_engine.cpp`):** Automatische Zustandsmaschine zur Überbrückung von Funkschatten zwischen Sena Mesh, Cardo DMC, OMM 2.4 GHz und LoRa 868 MHz Notfall-Beacon.
- **WebDAV TLS 1.3 Client:** Asynchroner Upload von GPX-Touren zu Nextcloud/Synology im Heim-WLAN bei Zündung AUS.
- **SDIO Logging Task:** 4-Bit High-Speed SD-Karten-Logger mit Ringpuffer und automatischem BGH-Datenschutz-Purge.
- **ADR-EKF Filter:** 15-State Sensorfusion aus 10 Hz Multi-GNSS-Telemetrie (vom Front-Knoten via UWB) und onboard Bosch BMI270 6-Achs IMU für unterbrechungsfreie Navigation in Tunneln.

#### CORE 1 (Echtzeit Audio-DSP Engine @ Höchste Priorität):
- **Dual-Helm Bluetooth Audio Hub:** Bindet Fahrer- und Sozius-Helme drahtlos per Bluetooth Audio an.
- **I2S Audio DMA Receiver & Transmitter:** Latenzarmes Streaming über ES8388 Audio-Codec ($f_s = 48\,\text{kHz}, 24\,\text{Bit}$, Double-Buffer à 128 Samples = $2{,}67\,\text{ms}$).
- **Raised-Cosine Ducking Engine:** Knackfreie, stetig differenzierbare Audio-Absenkung bei Durchsagen oder Radarwarnungen.
- **Dynamische AGC-Lautstärkeregelung:** Gleitende Anhebung des Helm-Ausgangspegels basierend auf dem Front-Node Fahrtwindpegel.
- **Lookahead Brickwall-Limiter:** Verhindert digitales Clipping über $0\,\text{dBFS}$.

---

## 2. Deterministischer All-UWB Fahrzeug-Backbone (`uwb_vehicle_backbone.cpp`)

Alle Daten- und Steuerverbindungen im Fahrzeugnetzwerk nutzen IEEE 802.15.4z Ultra-Wideband (Qorvo DW3110, Kanal 5 @ 6.489 GHz, Bandbreite 499.2 MHz, BPRF-Modus):
- **Rechtliche Konformität:** ETSI EN 302 065-1, EN 302 065-3 und EU-Beschluss 2019/785 ($-41{,}3\,\text{dBm/MHz}$, kontinuierlicher legaler Sendebetrieb ohne Duty-Cycle-Beschränkung).
- **Zero-Interference:** Arbeitet frequenzmäßig weit oberhalb von 2.4 GHz (WLAN, Bluetooth, Sena Mesh, Cardo DMC) und 5.8 GHz.
- **Deterministische Latenz:** Flug- und Verarbeitungszeit $< 0{,}4\,\text{ms}$.
- **Topologie:** Stern- und Punkt-zu-Mehrpunkt-Netzwerk mit der Zentralbox als UWB-Koordinator und Front-Node, Bucht 1, Bucht 2 und Heckradar als autorisierten Endpunkten.

```cpp
enum UwbBackbonePktType : uint8_t {
    // Front-Node Telemetrie & Steuerung
    UWB_PKT_HEARTBEAT          = 0x01,  // Status, Uptime, VBUS-Spannung, Ranging-Distanz
    UWB_PKT_PTT_EVENT          = 0x02,  // Lenker-PTT gedrückt/losgelassen (< 0.4 ms)
    UWB_PKT_AUDIO_RMS          = 0x03,  // Knowles MEMS Fahrtwind dB(A) Pegel (50 Hz)
    UWB_PKT_GNSS_PVT           = 0x04,  // u-blox SAM-M10Q 10 Hz PVT Telemetrieblock
    UWB_PKT_ENV_SENSORS        = 0x05,  // TI TMP117 (Temp) & TI OPT3001 (Lux)
    UWB_PKT_CAN_TELEMETRY      = 0x06,  // Cockpit-CAN Telemetriedaten (wenn Front J2 aktiv)
    UWB_PKT_OTTOCAST_STATUS    = 0x07,  // Status, Strom, Auto-Café Timer
    
    // Smart Cartridges (Bucht 1 Links & Bucht 2 Rechts)
    UWB_PKT_CARTRIDGE_ANNOUNCE = 0x20,  // Handshake: Hardware-Klasse, UID, Status, Roaming-ID
    UWB_PKT_CARTRIDGE_OPCODE   = 0x21,  // Zentralbox -> Kassette: Mechatronik-Trigger-Opcode
    UWB_PKT_CARTRIDGE_ACK      = 0x22,  // Kassette -> Zentralbox: Ausführungsquittung
    
    // Heck-Radar (PCBA 08)
    UWB_PKT_RADAR_TARGETS      = 0x30,  // 20 Hz Radar-Objektliste, TTC, Distanz, Azimut
    UWB_PKT_RADAR_ALERT        = 0x31,  // Prio-1 Kollisionswarnung für Audio-Ducking & LED
    
    // System- & Pairing-Befehle
    UWB_PKT_CMD_POWER_CYCLE    = 0x10,  // Zentralbox -> Front-Node: 2.5s Kaltstart
    UWB_PKT_CMD_CONFIG         = 0x11,  // Zentralbox -> Satelliten: Zündungs-Sync
    UWB_PKT_PAIRING_REQUEST    = 0x40,  // Pairing-Ablauf nach SW1 Tasterdruck
    UWB_PKT_PAIRING_CONFIRM    = 0x41   // AES-128 Session-Key Austausch & NVS Speicherung
};
```

### 2.1 Latenzbudget des drahtlosen UWB Mechatronik-Triggers
1. **Lenkertaster Schließen:** $12\,\mu\text{s}$ Hardware-Entprellung am Front-Node.
2. **Front-Node ESP32-S3 GPIO-Interrupt:** $25\,\mu\text{s}$ ISR-Verarbeitungszeit.
3. **UWB SPI TX & Funkübertragung Front -> Zentralbox (6.5 GHz):** $180\,\mu\text{s}$ (6.8 Mbps Datenrate).
4. **Zentralbox DW3110 SPI RX & Core 0 Dispatcher:** $45\,\mu\text{s}$ Frame-Parsing & Opcode-Generierung.
5. **UWB SPI TX & Funkübertragung Zentralbox -> Kassette (6.5 GHz):** $180\,\mu\text{s}$.
6. **Kassetten-Controller & N-MOSFETs (`AO3400A`):** $< 100\,\mu\text{s}$ Schaltzeit der mechatronischen Aktuatoren.
* **Gesamtlatenz:** **$\approx 0{,}54\,\text{ms}$** (Mehr als 18-fach schneller als die menschliche Wahrnehmungsschwelle von $10\,\text{ms}$).

### 2.2 UWB Cryptographic Binding, Key Reset & Multi-Vehicle Roaming
- **PAN-ID & 128-Bit AES-GCM Verschlüsselung:** Alle UWB-Pakete werden per Hardware-AES-GCM authentifiziert und verschlüsselt. Cross-Talk zwischen benachbarten Fahrzeugen ist mathematisch ausgeschlossen.
- **Hardware-Taster `SW1` (`SW_PAIR_RESET`):**
  - **3 Sekunden Drücken:** Zentralbox öffnet ein 60-Sekunden-Pairing-Fenster (`UWB_PKT_PAIRING_REQUEST`). Neu eingesteckte Kassetten oder ein neuer Front-Node/Radar handeln automatisch neue Session-Keys aus.
  - **10 Sekunden Halten:** Hard-Purge aller gespeicherten UWB-Knoten und Rücksetzen auf Werkseinstellungen.
- **Multi-Vehicle Roaming (Kassetten):**
  - Da viele Fahrer ihre modularen Kassetten (z. B. Sena SPIDER oder Cardo Edge) flexibel zwischen mehreren Motorrädern wechseln, speichern die Kassetten bis zu **4 autorisierte Fahrzeug-Schlüssel im NVS**.
  - Beim Einstecken in ein bekanntes Fahrzeug erfolgt der UWB-Handshake ohne erneutes Pairing in $< 50\,\text{ms}$.
- **Two-Way Ranging Gating:** Die Zentralbox verifiziert kontinuierlich die physische Distanz zum Front-Knoten ($0{,}5\,\text{m}\dots 2{,}5\,\text{m}$), zu den Kassetten ($0{,}2\,\text{m}\dots 1{,}8\,\text{m}$) und zum Heckradar ($0{,}3\,\text{m}\dots 2{,}0\,\text{m}$). Außerhalb des Fahrzeugfensters liegende Pakete werden verworfen (Schutz gegen Spoofing und Relay-Angriffe).

### 2.3 CAN Dual-Ingress-Architektur & Auto-Sensing / Deaktivierung

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CAN DUAL-INGRESS & AUTO-SENSING MATRIX                   │
├───────────────────────────────────┬─────────────────────────────────────────┤
│ Szenario 1: Touring Fairing       │ Szenario 2: Naked / Road King / Adv     │
│ (Street Glide / Road Glide)       │ (Road King Special, BMW R1250/R1300 GS) │
├───────────────────────────────────┼─────────────────────────────────────────┤
│ • CAN-Anschluss am FRONT NODE     │ • Kein CAN im Frontscheinwerfer         │
│   Port J2 (3-Pin JST-GH)          │ • CAN-Anschluss an der ZENTRALBOX       │
│ • Front Node erkennt Bus-Frames   │   DTM-12 Pins 11/12 am BCM / OBD2       │
│ • 120R-Relais CPC1017N SCHLIESST  │ • Front Node J2 bleibt UNVERBUNDEN      │
│ • Telemetrie wird per UWB         │ • Front Node deaktiviert J2 nach 2,5 s: │
│   (UWB_PKT_CAN_TELEMETRY) zur     │   - 120R-Relais bleibt OFFEN            │
│   Zentralbox gestreamt            │   - TCAN334G geht in Silent High-Z      │
│ • Zentralbox schaltet auf         │   - TWAI-Treiber wird gestoppt          │
│   `CAN_SOURCE_REMOTE_FRONT_NODE`  │ • Zentralbox nutzt lokalen DTM-12 CAN   │
│                                   │   als `CAN_SOURCE_LOCAL_CENTRAL_BOX`    │
└───────────────────────────────────┴─────────────────────────────────────────┘
```

1. **Front-Node Auto-Sensing & Deaktivierung (`cockpit_can_manager.cpp`):**
   - Bootet im sicheren **Listen-Only Modus** (`TWAI_MODE_LISTEN_ONLY`) mit geöffnetem Abschlussrelais (`PIN_CAN_TERM_EN = 0`).
   - Innerhalb eines $2{,}5\,\text{s}$ Zeitfensters wird der Bus überwacht.
   - **Bus erkannt:** Status wechselt auf `CAN_STATE_CONNECTED`, das OptoMOS-Relais `CPC1017N` schließt den $120\,\Omega$-Terminierungswiderstand, der Transceiver geht auf Normalbetrieb (`PIN_CAN_SILENT = 0`) und streamt Frames per UWB zur Zentralbox.
   - **Kein Bus erkannt:** Status wechselt auf `CAN_STATE_DEACTIVATED`. Das Relais bleibt offen, `PIN_CAN_SILENT` wird auf HIGH (Standby/High-Z) gesetzt und der TWAI-Treiber gestoppt (`twai_stop()`). Es entstehen 0 Bus-Fehler, keine Interrupt-Belastung und minimaler Ruhestrom.
2. **Zentralbox Quellen-Arbitrierung (`can_bus_manager.cpp`):**
   - Empfängt die Zentralbox lokale Frames auf DTM-12 Pins 11/12, wird `CAN_SOURCE_LOCAL_CENTRAL_BOX` aktiv.
   - Bleibt der lokale DTM-12 CAN-Port frei, schaltet der Manager nahtlos auf `CAN_SOURCE_REMOTE_FRONT_NODE` um.

---

## 3. BLE GATT Server Architektur (`ble_service_server.cpp`)

Das System exponiert standardkonforme Bluetooth SIG Services sowie proprietäre Vendor-Services für das PWA-Dashboard:

| Service UUID | Characteristic UUID | Properties | Funktion & Datenschema |
| :--- | :--- | :--- | :--- |
| **`0x180D`** (Audio RMS & Env)       | **`0x2A37`** | Notify | Knowles MEMS Fahrtwind-Schallpegel (50 Hz dB(A)) & TMP117 Temperatur. |
| **`0x180A`** (Device Information)    | **`0x2A24`** | Read   | Hardware-Revision (`OMB-V8.5-2026.2`), Serial, Firmware-Build. |
| **`0xFFE0`** (Proprietary Control)   | **`0xFFE1`** | Write  | Steuerbefehle: `0x01` Profilwechsel, `0x02` Reset, `0x09` Smart Cartridge Opcode, `0x0A` UWB Pairing Trigger. |
| **`0xFFE0`** (Proprietary Telemetry) | **`0xFFE2`** | Notify | 10 Hz Telemetrie-Stream: Lean-Angle (Roll/Pitch), Speed, TTC, Radar-Warnung. |
| **`0xFFE0`** (UWB Cartridge Status)  | **`0xFFE3`** | Notify/Read | Kassetten-Status Bucht 1 & 2: UID, Hardware-Klasse, UWB-Latenz, Batteriestatus. |

---

## 4. Universal Group Split Fallback Engine (`group_split_rescue_engine.cpp`)

Bei Touren in Bergregionen oder dichtem Wald reißen 2.4 GHz Intercom-Verbindungen (Sena Mesh / Cardo DMC) ab ca. $800\dots 1200\,\text{m}$ Distanz ab, wenn Sichtkontakt verloren geht. Die in v8.5 / v9.0 integrierte **Group Split Fallback Engine** schützt Gruppen vor dem Auseinanderreißen:

```
               GROUP SPLIT FALLBACK ENGINE ZUSTANDSAUTOMAT
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. NORMAL STATUS: LINE-OF-SIGHT VERBUNDEN                                   │
│    • Bucht 1 (Sena Mesh) & Bucht 2 (Cardo DMC) voll aktiv                   │
│    • HD-Audio Stream im Helm; LoRa sendet periodische Heartbeats (0.2 Hz)   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                     ▼ (Verbindungsverlust > 15 s)           │
│ 2. RESCUE LEVEL 1: OMM 2.4 GHz KANAL-HOPPING MESH                           │
│    • Falls OMM-Kassette in Bucht 2 gesteckt: Erhöht TX-Power auf +20 dBm    │
│    • Sucht nach Relais-Knoten benachbarter Gruppenmitglieder                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                     ▼ (Verbindungsverlust > 45 s)           │
│ 3. RESCUE LEVEL 2: 868 MHz LoRa MESH (SX1262) TELEMETRIE & TEXT             │
│    • Reichweite bis zu 15 km (LOS) bzw. 3-5 km im Gebirge                   │
│    • Überträgt automatisch GPS-Position, Peilung, Entfernung & Distanzpfeil │
│    • Zeigt "Gruppe voraus: 2,4 km Nord-West" auf CarPlay/PWA-Dashboard      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                     ▼ (Verbindungsverlust > 120 s)          │
│ 4. RESCUE LEVEL 3: PMR446 ANALOG-VOICE FALLBACK (OPTIONAL)                  │
│    • Triggert automatischen Durchsage-Ping auf Midland Funkkassette         │
│    • Überträgt synthetisierte TTS-Ortsansage auf analogen Jedermannfunk     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Kassetten-Steuerung: Mechatronische Smart Cartridge (PCBA 03 All-UWB) & Hardware-IDs

### 5.1 Kassetten-Handshake via UWB (`UWB_PKT_CARTRIDGE_ANNOUNCE`)
Jede Smart Cartridge (PCBA 03) bootet bei Bestromung durch das Power-Sequencing ($T = 200\,\text{ms}$ bzw. $T = 350\,\text{ms}$) und sendet sofort ein UWB-Handshake-Paket an die Zentralbox mit ihrer Hardware-Klasse und UID:
* **`0x01`**: Sena SPIDER X Slim (Mechatronische 4-Aktuatoren Steuerung)
* **`0x02`**: Cardo Packtalk Edge (Mechatronische 4-Aktuatoren Steuerung)
* **`0x03`**: OMM 2.4 GHz Swap Cartridge (ESP32-C3 Digital Transceiver)
* **`0x04`**: Midland PMR446 / Funk (PTT-Tastung via MOSFET)

### 5.2 Smart Cartridge Mechatronik-Modus (PCBA 03)
Die Zentralbox sendet 1-Byte Opcodes drahtlos per UWB-Paket (`UWB_PKT_CARTRIDGE_OPCODE`) an den Host-Controller der Kassette. Dieser schaltet die 4x AO3400A N-MOSFETs auf der Platinenunterseite (`B.Cu`), welche die Taster des eingesetzten Headsets mechatronisch betätigen:

| Opcode | Funktion / Geste | Aktive Aktuatoren | Pulsdauer / Ablauf | Headset-Reaktion (Sena SPIDER X Slim) |
| :---: | :--- | :--- | :--- | :--- |
| **`0x01`** | **Power Boot (Kaltstart)** | **ACT_CENTER + PLUS** | $1000\,\text{ms}$ synchron | Bootet das Headset vollautomatisch bei Zündung AN |
| **`0x02`** | **Power Off (Ausschalten)**| **ACT_CENTER + PLUS** | $200\,\text{ms}$ synchron | Sauberes Herunterfahren vor Spannungsabschaltung |
| **`0x03`** | **Lauter (+)** | **ACT_PLUS** (solo) | $100\,\text{ms}$ Einzelpuls | Lautstärke +1 Schritt |
| **`0x04`** | **Leiser (-)** | **ACT_MINUS** (solo) | $100\,\text{ms}$ Einzelpuls | Lautstärke -1 Schritt |
| **`0x05`** | **Mesh Intercom Ein/Aus** | **ACT_MESH** (solo) | $200\,\text{ms}$ Einzelpuls | Mesh-Intercom Toggle (Sprachansage "Mesh On/Off") |
| **`0x06`** | **Open ↔ Group Mesh** | **ACT_MESH** (solo) | $3000\,\text{ms}$ Haltepuls | Wechsel zwischen öffentlichem und privatem Gruppenmesh |
| **`0x07`** | **Kanal +1 (Makro)** | **ACT_MESH (2x) + PLUS (1x)** | 2x $150\,\text{ms}$, Pause $200\,\text{ms}$, 1x $150\,\text{ms}$ | Schaltet im Mesh-Menü autonom auf nächsten Kanal |
| **`0x08`** | **Kanal -1 (Makro)** | **ACT_MESH (2x) + MINUS (1x)**| 2x $150\,\text{ms}$, Pause $200\,\text{ms}$, 1x $150\,\text{ms}$ | Schaltet im Mesh-Menü autonom auf vorherigen Kanal |

---

## 6. FreeRTOS Task-Architektur & Scheduling-Matrix (Zentralbox & Front-Knoten)

Das Gesamtsystem orchestriert spezialisierte Tasks über 2 ESP32-S3 Hauptkontroller:

| Task-Name | MCU / Kern | Prio | Stack | Auslöser / Rate | IPC / Schnittstelle | Aufgabe & Funktion |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **`audio_dsp_task`** | Central Box (Core 1) | **24** | 8 KB | 48 kHz DMA ISR | FreeRTOS StreamBuffer | Latenzfreier I2S Audio-Mix, Raised-Cosine Ducking & AGC. |
| **`uwb_backbone_task`**| Central Box (Core 0) | **22** | 4 KB | DW3110 IRQ / Event | Direct-to-Task Notify | Verarbeitet Front-Node PTT-Events ($< 0{,}4\,\text{ms}$), GNSS & Windpegel. |
| **`lora_mesh_task`**  | Central Box (Core 0) | **20** | 4 KB | SX1262 IRQ / Timer  | FreeRTOS Queue        | 868 MHz LoRa Mesh Protokoll, Diebstahl-Sentry & Group Split Rescue. |
| **`uwb_cart_disp_task`**| Central Box (Core 0) | **18** | 4 KB | Event-Queue         | UWB TX Queue          | Dispatched Mechatronik-Opcodes per UWB an Bucht 1 & Bucht 2. |
| **`uwb_radar_task`**  | Central Box (Core 0) | **16** | 4 KB | UWB Event Queue     | FreeRTOS Queue        | Empfängt 20 Hz Radar-Ziele per UWB, TTC-Berechnung & Prio-1 Ducking. |
| **`adr_ekf_task`**    | Central Box (Core 0) | **15** | 4 KB | 50 Hz Timer         | I2C / CAN-Puffer      | 15-State Kalman-Filter (SAM-M10Q GNSS + BMI270 IMU + CAN Speed). |
| **`power_seq_task`**  | Central Box (Core 0) | **14** | 2 KB | Boot-Event / Timer  | GPIO Power-Gates      | Gestaffeltes Power-Sequencing ($T=0, 200, 350, 500\,\text{ms}$). |
| **`pairing_mgr_task`**| Central Box (Core 0) | **12** | 3 KB | SW1 Edge / Timer    | NVS Key Storage       | Überwacht SW1 (3s Pairing, 10s Purge), Multi-Vehicle Roaming. |
| **`ble_server_task`** | Central Box (Core 0) | **10** | 4 KB | Event-Driven        | NimBLE Stack          | Web-Bluetooth PWA Dashboard (GATT Services `0x180D`/`0x180A`). |
| **`sdio_log_task`**   | Central Box (Core 0) | **8**  | 8 KB | 10 Hz Ringpuffer    | FreeRTOS RingBuffer   | 4-Bit SDIO Blackbox-Logging mit ECDSA SHA-256 Signatur. |
| **`webdav_sync_task`**| Central Box (Core 0) | **3**  | 8 KB | Nachlauf (Graceful) | LwIP TLS 1.3          | Automatischer GPX-Upload im Heim-WLAN bei Zündung AUS. |
| **`front_ptt_task`**  | Front Node (Core 0)  | **24** | 2 KB | GPIO Edge ISR       | UWB TX Queue          | Sendet Lenker-PTT via UWB in $< 0{,}2\,\text{ms}$; Cam Toggle; HiLight Tag. |
| **`front_gnss_task`** | Front Node (Core 0)  | **20** | 4 KB | 10 Hz I2C DMA       | J12 Qwiic / UWB TX    | u-blox SAM-M10Q UBX-NAV-PVT Parsing, TMP117 Temp & OPT3001 Lux. |
| **`front_mems_task`** | Front Node (Core 1)  | **18** | 4 KB | 48 kHz DMA          | Vector-DSP Filter     | Knowles SPH0645 Digitalmikrofon A-Weighting & RMS-Pegel via Xtensa DSP. |
| **`front_can_task`**  | Front Node (Core 0)  | **16** | 4 KB | TWAI Interrupt      | CAN Message Queue     | Liest Cockpit-CAN (falls J2 verbunden), Auto-Terminierung CPC1017N. |
| **`front_pwr_task`**  | Front Node (Core 0)  | **10** | 2 KB | 10 Hz Timer         | GPIO Lastschalter     | SW3526 USB-PD Überwachung, TPS2051B Kaltstart (2,5s), Auto-Off. |

---

## 7. LittleFS Kassetten-Profil-Engine & JSON-Datenstruktur

Wird eine Kassette eingesteckt und meldet sich per UWB (`UWB_PKT_CARTRIDGE_ANNOUNCE`), lädt der Kassetten-Manager die Konfiguration aus `/storage/profiles/<UID>.json`:

```json
{
  "profile_schema": 2,
  "uid": "01:A4:7B:3F:00:00:00:1E",
  "device_name": "Sena SPIDER X Slim Inlay",
  "hardware_class": "0x01",
  "power": {
    "vcc_enabled": true,
    "vcc_voltage_mv": 5000,
    "max_current_ma": 350,
    "soft_start_ms": 120
  },
  "audio": {
    "input_gain_db": 6.0,
    "output_gain_db": 0.0,
    "ducking_priority": 3,
    "auto_agc_enabled": true,
    "clip_limit_dbfs": -0.5
  },
  "opto_trigger": {
    "enabled": true,
    "mode": "sena_spider_mesh",
    "pulse_click_ms": 150,
    "pulse_channel_ms": 1000
  },
  "mesh_routing": {
    "dle_bonus_points": 60,
    "protocol_family": "sena_mesh_3"
  }
}
```

* **Zero-Trust Fallback (`disabled.json`):** Bei unbekannter UID, Kurzschluss oder leerem Schacht bleibt der 5V MOSFET gesperrt (`vcc_enabled: false`), der Codec wird auf `-96 dB` gedämpft und der DLE-Score auf `0` gesetzt.

---

## 8. Modulare Hardware-Topologie & Graceful Degradation

OpenMotorBridge ist als **losgelöstes, fehlertolerantes Baukastensystem** konzipiert. Kein Subsystem blockiert den Start der Zentralbox:

| Konfiguration | Verbaute Komponenten | Systemverhalten & Graceful Degradation |
| :--- | :--- | :--- |
| **Tier 1: Minimal Core** | Nur Zentralbox<br>*(Kein Front Node)* | • **Audio-Bridge & Intercoms voll aktiv:** Bucht 1 & 2 mischen latenzfrei via UWB.<br>• **LoRa 868 MHz Mesh aktiv:** Direkte USV-gepufferte 24/7 Diebstahl-Sentry & Tracking.<br>• **CAN-Bus aktiv:** Tacho, Drehzahl & BCM-Telemetrie über DTM-12 Pins 11/12.<br>• **IMU aktiv:** Bosch BMI270 liefert Schräglage, Pitch & Erschütterung.<br>• **ADR-EKF:** Läuft im reinen Dead-Reckoning Modus gestützt auf IMU & Raddrehzahl.<br>• **UWB-Treiber:** Wartet passiv im Scan-Modus; AGC bleibt auf Nominalpegel. |
| **Tier 2: Vollsystem mit Front Node** | Zentralbox + Front Node | • Alle Tier 1 Funktionen + deterministischer UWB-Backbone (< 0,4 ms).<br>• u-blox SAM-M10Q Multi-GNSS mit 10 Hz PVT-Fix & Präzisions-Zeitsynchronisation.<br>• TI TMP117 Glatteis-Wächter ($\pm 0{,}1\,^\circ\text{C}$) & TI OPT3001 Helligkeitssensor.<br>• 4-Port USB-Hub & Dual 20W USB-PD Schnelllader im Cockpit.<br>• Ottocast Watchdog & automatische Zündungstrennung.<br>• Lenker-PTT (< 0,4 ms) und dynamische Fahrtwind-AGC über Knowles MEMS. |
| **Tier 3: Heckradar-Option** | Zentralbox + Front Node + Radar | • Alle Tier 2 Funktionen + Wheeltec MR20 77 GHz oder Garmin Varia (PCBA 08).<br>• 2-Draht 12V DC-Power vom DTM-12; Telemetrie 100% drahtlos via UWB.<br>• Akustische Warn-Pings im Helm, optische Warn-Flügel & Spiegel-LEDs (Port `J9`).<br>• Automatische Action-Cam Bookmarks bei kritischem Radar TTC (< 2,5 s). |

### 8.1 Schutzmechanismen gegen fehlende Daten (Zero-Crash Policy)
1. **Asynchrone Non-Blocking Schnittstellen:** Die Kommunikation über UWB, LoRa (SPI) und Radar läuft mit FreeRTOS Timeouts (`pdMS_TO_TICKS(50)`). Es existieren **keine blockierenden `while(1)`-Warteschleifen**.
2. **Dynamische DLE-Fähigkeiten (`omm_get_capabilities_vector`):** Die Zentralbox deklariert nur jene Hardware-Flags im Mesh, die physisch antworten (`gnss_is_connected()`, `is_linked`, `can_bus_is_connected()`).
3. **Sensor-Fusion Autarkie (`adr_ekf_filter.cpp`):** Fällt GNSS weg (z. B. Tunnel oder Front Node offline), schaltet der EKF verzögerungsfrei auf **Dead Reckoning** um und stützt sich auf IMU und CAN-Raddrehzahl.
4. **Fehlertoleranter Audiomixer (`audio_dsp_pipeline.cpp`):** Fehlt das Knowles MEMS Mikrofon des Front Nodes, läuft der Brickwall-Limiter und AGC-Level auf festem Rider-Standardwert (Unity Gain `1.0f`).
