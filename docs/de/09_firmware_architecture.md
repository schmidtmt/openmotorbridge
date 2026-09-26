# 09 - Firmware-Architektur, FreeRTOS Tasks & Rollback-OTA

Dieses Dokument spezifiziert die systemweite Firmware-Architektur der OpenMotorBridge v8.0: die Multi-Core-Aufteilung des ESP32-S3 Hauptcontrollers auf der Zentralbox (`PCBA 01`), des ESP32-S3 Front-Knotens (`PCBA 05`), des deterministischen **UWB-Backbones (Qorvo DW3110 / 6.489 GHz Ch. 5, Latenz < 0,4 ms)**, der **Group Split Fallback Engine**, der LittleFS-Profil-Engine sowie der **Dual-Bank Rollback-OTA-Architektur** gegen Stromausfälle während des Flashvorgangs.

---

## 1. Multi-Core & Multi-MCU Systemarchitektur

In v8.0 ist das System strikt auf zwei primäre Hauptknoten konsolidiert (Heck-Pod 3 und PCBA 04 sind ersatzlos entfallen):

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        DIE FIRMWARE-KONTROLLER IM SYSTEMVERBUND                        │
├──────────────────────────────────────────────────────┬─────────────────────────────────┤
│ 1. ZENTRALBOX (ESP32-S3 Dual-Core, PCBA 01)          │ 2. FRONT-NODE (ESP32-S3, PCBA 05)│
├──────────────────────────────────────────────────────┼─────────────────────────────────┤
│ • Core 0: UWB-Backbone, SX1262 LoRa 868, BLE, WebDAV │ • Core 0: UWB-Backbone, SAM-M10Q│
│ • Core 1: Echtzeit 48 kHz Audio-DSP, Ducking, AGC    │   Multi-GNSS, CAN, USB-PD, PTT  │
│ • Co-MCUs: CH32V003 auf PCBA 03 (Smart Cartridges)   │ • Core 1: Knowles Vector-DSP    │
└──────────────────────────────────────────────────────┴─────────────────────────────────┘
```

### 1.1 Core-Aufteilung des ESP32-S3 Hauptcontrollers der Zentralbox (240 MHz)

#### CORE 0 (Kommunikation, Telemetrie & System):
- **UWB Backbone Driver (`uwb_vehicle_backbone.cpp`):** Deterministische SPI-Kommunikation mit dem Qorvo DW3110 Transceiver auf `B.Cu`. Empfängt Lenker-PTT-Events ($< 0{,}4\,\text{ms}$), Knowles MEMS dB(A)-Schallpegelwerte und 10 Hz Multi-GNSS-Pakete vom Front-Knoten.
- **LoRa 868 MHz Mesh Engine (`lora_mesh_engine.cpp`):** Direkte SPI-Anbindung an den onboard Semtech SX1262 Transceiver auf PCBA 01 (24/7 USV-gepuffert für Diebstahl-Sentry und Gruppen-Telemetrie).
- **BLE GATT Server (`ble_service_server.cpp`):** Web-Bluetooth Anbindung für das PWA-Dashboard (`0x180D`, `0x180A`, `0xFFE0`).
- **Dual 1-Wire Kassetten-Manager (`cartridge_onewire.cpp`):** Pollt zyklisch Port 1 & 2 auf Kassetten-IDs (emuliert vom CH32V003 MCU oder DS2401) und bindet LittleFS JSON-Profile ein.
- **Smart Cartridge Dispatcher & Opto-Puls-Sequenzer (`opto_pulse_sequencer.cpp`):** Erkennt Smart Cartridges (PCBA 03) und sendet 1-Byte Opcodes via Single-Wire UART auf Pin 5 (19.200 Baud) zur Ansteuerung der 4 mechatronischen Aktuatoren; schaltet bei PMR446-Funk alternativ auf TLP222A Relais-Tastung um.
- **Group Split Fallback Engine (`group_split_rescue_engine.cpp`):** Automatische Zustandsmaschine zur Überbrückung von Funkschatten zwischen Sena Mesh, Cardo DMC, OMM 2.4 GHz und LoRa 868 MHz Notfall-Beacon.
- **WebDAV TLS 1.3 Client:** Asynchroner Upload von GPX-Touren zu Nextcloud/Synology im Heim-WLAN bei Zündung AUS.
- **SDIO Logging Task:** 4-Bit High-Speed SD-Karten-Logger mit Ringpuffer und automatischem BGH-Datenschutz-Purge.
- **ADR-EKF Filter:** 15-State Sensorfusion aus 10 Hz Multi-GNSS-Telemetrie (vom Front-Knoten via UWB) und onboard Bosch BMI270 6-Achs IMU für unterbrechungsfreie Navigation in Tunneln.

#### CORE 1 (Echtzeit Audio-DSP Engine @ Höchste Priorität):
- **I2S Audio DMA Receiver & Transmitter:** Latenzarmes Streaming über ES8388 Audio-Codec ($f_s = 48\,\text{kHz}, 24\,\text{Bit}$, Double-Buffer à 128 Samples = $2{,}67\,\text{ms}$).
- **Raised-Cosine Ducking Engine:** Knackfreie, stetig differenzierbare Audio-Absenkung bei Durchsagen oder Radarwarnungen.
- **Dynamische AGC-Lautstärkeregelung:** Gleitende Anhebung des Helm-Ausgangspegels basierend auf dem Front-Node Fahrtwindpegel.
- **Lookahead Brickwall-Limiter:** Verhindert digitales Clipping über $0\,\text{dBFS}$.

---

## 2. Deterministischer UWB Fahrzeug-Backbone (`uwb_vehicle_backbone.cpp`)

Die drahtlose Verbindung zwischen Front-Knoten und Zentralbox nutzt IEEE 802.15.4z Ultra-Wideband (Qorvo DW3110, Kanal 5 @ 6.489 GHz, Bandbreite 499.2 MHz, BPRF-Modus):
- **Rechtliche Konformität:** ETSI EN 302 065-1, EN 302 065-3 und EU-Beschluss 2019/785 ($-41{,}3\,\text{dBm/MHz}$, kontinuierlicher legaler Sendebetrieb ohne Duty-Cycle-Beschränkung).
- **Zero-Interference:** Arbeitet frequenzmäßig weit oberhalb von 2.4 GHz (WLAN, Bluetooth, Sena Mesh, Cardo DMC) und 5.8 GHz.
- **Deterministische Latenz:** Flug- und Verarbeitungszeit $< 0{,}4\,\text{ms}$.

```cpp
enum UwbBackbonePktType : uint8_t {
    UWB_PKT_HEARTBEAT       = 0x01,  // Status, Uptime, VBUS-Spannung, Ranging-Distanz
    UWB_PKT_PTT_EVENT       = 0x02,  // Lenker-PTT gedrückt/losgelassen (< 0.4 ms)
    UWB_PKT_AUDIO_RMS       = 0x03,  // Knowles MEMS Fahrtwind dB(A) Pegel (50 Hz)
    UWB_PKT_GNSS_PVT        = 0x04,  // u-blox SAM-M10Q 10 Hz PVT Telemetrieblock
    UWB_PKT_ENV_SENSORS     = 0x05,  // TI TMP117 (Temp) & TI OPT3001 (Lux)
    UWB_PKT_CAN_TELEMETRY   = 0x06,  // Cockpit-CAN Telemetriedaten (wenn J2 aktiv)
    UWB_PKT_OTTOCAST_STATUS = 0x07,  // Status, Strom, Auto-Café Timer
    UWB_PKT_CMD_POWER_CYCLE = 0x10,  // Zentralbox -> Front-Node: 2.5s Kaltstart
    UWB_PKT_CMD_CONFIG      = 0x11   // Zentralbox -> Front-Node: Zündungs-Sync
};
```

### 2.1 Latenzbudget des PTT-Triggers
1. **Lenkertaster Schließen:** $12\,\mu\text{s}$ Hardware-Entprellung.
2. **Front-Node ESP32-S3 GPIO-Interrupt:** $25\,\mu\text{s}$ ISR-Verarbeitungszeit.
3. **UWB SPI TX & Funkübertragung (6.5 GHz):** $180\,\mu\text{s}$ (6.8 Mbps Datenrate).
4. **Zentralbox DW3110 SPI RX & Core 0 ISR:** $45\,\mu\text{s}$ Frame-Parsing & Opcode-Dispatch.
5. **Kassetten-Controller & N-MOSFETs (`AO3400`):** $< 100\,\mu\text{s}$ Schaltzeit der mechatronischen Aktuatoren.
* **Gesamtlatenz:** **$\approx 0{,}36\,\text{ms}$** (Mehr als 25-fach schneller als der physiologische Wahrnehmungsschwellwert von $10\,\text{ms}$).

### 2.2 UWB Cryptographic Binding & Distance Gating
- **PAN-ID & Session Key:** Im NVS hinterlegter 128-Bit AES-GCM Schlüssel verhindert Cross-Talk fremder Fahrzeuge.
- **Two-Way Ranging Gating:** Die Zentralbox verifiziert kontinuierlich die physische Distanz zum Front-Knoten. Liegt die Distanz außerhalb des Fahrzeugfensters ($0{,}5\,\text{m}\dots 2{,}5\,\text{m}$), wird die Verbindung verworfen (Schutz gegen Spoofing und Relay-Angriffe).

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
│ • Front Node erkennt Bus-Frames   │   HD26-Stecker Pins 17/18 am BCM / OBD2 │
│ • 120R-Relais CPC1017N SCHLIESST  │ • Front Node J2 bleibt UNVERBUNDEN      │
│ • Telemetrie wird per UWB         │ • Front Node deaktiviert J2 nach 2,5 s: │
│   (UWB_PKT_CAN_TELEMETRY) zur     │   - 120R-Relais bleibt OFFEN            │
│   Zentralbox gestreamt            │   - TCAN334G geht in Silent High-Z      │
│ • Zentralbox schaltet auf         │   - TWAI-Treiber wird gestoppt          │
│   `CAN_SOURCE_REMOTE_FRONT_NODE`  │ • Zentralbox nutzt lokalen HD26 CAN als │
│                                   │   `CAN_SOURCE_LOCAL_CENTRAL_BOX`        │
└───────────────────────────────────┴─────────────────────────────────────────┘
```

1. **Front-Node Auto-Sensing & Deaktivierung (`cockpit_can_manager.cpp`):**
   - Bootet im sicheren **Listen-Only Modus** (`TWAI_MODE_LISTEN_ONLY`) mit geöffnetem Abschlussrelais (`PIN_CAN_TERM_EN = 0`).
   - Innerhalb eines $2{,}5\,\text{s}$ Zeitfensters wird der Bus überwacht.
   - **Bus erkannt:** Status wechselt auf `CAN_STATE_CONNECTED`, das OptoMOS-Relais `CPC1017N` schließt den $120\,\Omega$-Terminierungswiderstand, der Transceiver geht auf Normalbetrieb (`PIN_CAN_SILENT = 0`) und streamt Frames per UWB zur Zentralbox.
   - **Kein Bus erkannt:** Status wechselt auf `CAN_STATE_DEACTIVATED`. Das Relais bleibt offen, `PIN_CAN_SILENT` wird auf HIGH (Standby/High-Z) gesetzt und der TWAI-Treiber gestoppt (`twai_stop()`). Es entstehen 0 Bus-Fehler, keine Interrupt-Belastung und minimaler Ruhestrom.
2. **Zentralbox Quellen-Arbitrierung (`can_bus_manager.cpp`):**
   - Empfängt die Zentralbox lokale Frames auf HD26 Pins 17/18, wird `CAN_SOURCE_LOCAL_CENTRAL_BOX` aktiv.
   - Bleibt der lokale HD26-Port frei, schaltet der Manager nahtlos auf `CAN_SOURCE_REMOTE_FRONT_NODE` um.

---

## 3. BLE GATT Server Architektur (`ble_service_server.cpp`)

Das System exponiert standardkonforme Bluetooth SIG Services sowie proprietäre Vendor-Services für das PWA-Dashboard:

| Service UUID | Characteristic UUID | Properties | Funktion & Datenschema |
| :--- | :--- | :--- | :--- |
| **`0x180D`** (Audio RMS & Env)       | **`0x2A37`** | Notify | Knowles MEMS Fahrtwind-Schallpegel (50 Hz dB(A)) & TMP117 Temperatur. |
| **`0x180A`** (Device Information)    | **`0x2A24`** | Read   | Hardware-Revision (`OMB-V8-2026.1`), Serial, Firmware-Build. |
| **`0xFFE0`** (Proprietary Control)   | **`0xFFE1`** | Write  | Steuerbefehle: `0x01` Profilwechsel, `0x02` Reset, `0x09` Smart Cartridge Opcode. |
| **`0xFFE0`** (Proprietary Telemetry) | **`0xFFE2`** | Notify | 10 Hz Telemetrie-Stream: Lean-Angle (Roll/Pitch), Speed, TTC, Radar-Warnung. |
| **`0xFFE0`** (1-Wire & Cartridge ID) | **`0xFFE3`** | Notify/Read | Kassetten-Status Port 1 & 2: 64-Bit UID, Hardware-Klasse, DLE-Score. |

---

## 4. Universal Group Split Fallback Engine (`group_split_rescue_engine.cpp`)

Bei Touren in Bergregionen oder dichtem Wald reißen 2.4 GHz Intercom-Verbindungen (Sena Mesh / Cardo DMC) ab ca. $800\dots 1200\,\text{m}$ Distanz ab, wenn Sichtkontakt verloren geht. Die in v8.0 integrierte **Group Split Fallback Engine** schützt Gruppen vor dem Auseinanderreißen:

```
               GROUP SPLIT FALLBACK ENGINE ZUSTANDSAUTOMAT
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. NORMAL STATUS: LINE-OF-SIGHT VERBUNDEN                                   │
│    • Pod 1 (Sena Mesh) & Pod 2 (Cardo DMC) voll aktiv                       │
│    • HD-Audio Stream im Helm; LoRa sendet periodische Heartbeats (0.2 Hz)   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                     ▼ (Verbindungsverlust > 15 s)           │
│ 2. RESCUE LEVEL 1: OMM 2.4 GHz KANAL-HOPPING MESH                           │
│    • Falls OMM-Kassette gesteckt: Erhöht TX-Power auf +20 dBm               │
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

## 5. Kassetten-Steuerung: Mechatronische Smart Cartridge (PCBA 03) & Hardware-IDs

### 5.1 CH32V003 Hardware-IDs & 1-Wire Emulation
Jede Steckkassette meldet beim Einstecken ihre Hardware-Klasse über Single-Wire UART / 1-Wire ID:
* **`0x01`**: Sena SPIDER X Slim (Mechatronische 4-Aktuatoren Steuerung)
* **`0x02`**: Cardo Packtalk Edge (Mechatronische 4-Aktuatoren Steuerung)
* **`0x03`**: OMM 2.4 GHz Swap Cartridge (ESP32-C3 Digital Transceiver)
* **`0x04`**: Midland PMR446 / Funk (Relais-Tastung via TLP222A)

### 5.2 Smart Cartridge Mechatronik-Modus (PCBA 03)
Die Zentralbox sendet 1-Byte Opcodes via Single-Wire UART auf Pin 5 (19.200 Baud) an den CH32V003:

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
| **`smart_act_task`**  | Central Box (Core 0) | **18** | 2 KB | Event-Queue         | FreeRTOS Queue        | Dispatched 1-Byte Opcodes via Single-Wire UART / TLP222A Relais. |
| **`radar_proc_task`** | Central Box (Core 0) | **16** | 4 KB | 20 Hz UART2 ISR     | FreeRTOS Queue / UART | Wheeltec MR20 / Garmin Varia Parsing, TTC-Berechnung & Prio-1 Ducking. |
| **`adr_ekf_task`**    | Central Box (Core 0) | **15** | 4 KB | 50 Hz Timer         | I2C / CAN-Puffer      | 15-State Kalman-Filter (SAM-M10Q GNSS + BMI270 IMU + CAN Speed). |
| **`ble_server_task`** | Central Box (Core 0) | **10** | 4 KB | Event-Driven        | NimBLE Stack          | Web-Bluetooth PWA Dashboard (GATT Services `0x180D`/`0x180A`). |
| **`sdio_log_task`**   | Central Box (Core 0) | **8**  | 8 KB | 10 Hz Ringpuffer    | FreeRTOS RingBuffer   | 4-Bit SDIO Blackbox-Logging mit ECDSA SHA-256 Signatur. |
| **`onewire_task`**    | Central Box (Core 0) | **5**  | 2 KB | 0,5 Hz zyklisch     | Bit-Banging Driver    | Pollt Kassetten-IDs an Pod 1 & 2 (CH32V003 Emulation oder DS2401). |
| **`webdav_sync_task`**| Central Box (Core 0) | **3**  | 8 KB | Nachlauf (Graceful) | LwIP TLS 1.3          | Automatischer GPX-Upload im Heim-WLAN bei Zündung AUS. |
| **`front_ptt_task`**  | Front Node (Core 0)  | **24** | 2 KB | GPIO Edge ISR       | UWB TX Queue          | Sendet Lenker-PTT via UWB in $< 0{,}2\,\text{ms}$; Cam Toggle; HiLight Tag. |
| **`front_gnss_task`** | Front Node (Core 0)  | **20** | 4 KB | 10 Hz I2C DMA       | J12 Qwiic / UWB TX    | u-blox SAM-M10Q UBX-NAV-PVT Parsing, TMP117 Temp & OPT3001 Lux. |
| **`front_mems_task`** | Front Node (Core 1)  | **18** | 4 KB | 48 kHz DMA          | Vector-DSP Filter     | Knowles SPH0645 Digitalmikrofon A-Weighting & RMS-Pegel via Xtensa DSP. |
| **`front_can_task`**  | Front Node (Core 0)  | **16** | 4 KB | TWAI Interrupt      | CAN Message Queue     | Liest Cockpit-CAN (falls J2 verbunden), Auto-Terminierung CPC1017N. |
| **`front_pwr_task`**  | Front Node (Core 0)  | **10** | 2 KB | 10 Hz Timer         | GPIO Lastschalter     | SW3526 USB-PD Überwachung, TPS2051B Kaltstart (2,5s), Auto-Off. |

---

## 7. LittleFS Kassetten-Profil-Engine & JSON-Datenstruktur

Wird eine Kassette eingesteckt, lädt der Kassetten-Manager die Konfiguration aus `/storage/profiles/<UID>.json`:

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
| **Tier 1: Minimal Core** | Nur Zentralbox<br>*(Kein Front Node)* | • **Audio-Bridge & Intercoms voll aktiv:** Pod 1 & 2 mischen latenzfrei.<br>• **LoRa 868 MHz Mesh aktiv:** Direkte USV-gepufferte 24/7 Diebstahl-Sentry & Tracking.<br>• **CAN-Bus aktiv:** Tacho, Drehzahl & BCM-Telemetrie über HD26 Pins 17/18.<br>• **IMU aktiv:** Bosch BMI270 liefert Schräglage, Pitch & Erschütterung.<br>• **ADR-EKF:** Läuft im reinen Dead-Reckoning Modus gestützt auf IMU & Raddrehzahl.<br>• **UWB-Treiber:** Wartet passiv im Scan-Modus; AGC bleibt auf Nominalpegel. |
| **Tier 2: Vollsystem mit Front Node** | Zentralbox + Front Node | • Alle Tier 1 Funktionen + deterministischer UWB-Backbone (< 0,4 ms).<br>• u-blox SAM-M10Q Multi-GNSS mit 10 Hz PVT-Fix & Präzisions-Zeitsynchronisation.<br>• TI TMP117 Glatteis-Wächter ($\pm 0{,}1\,^\circ\text{C}$) & TI OPT3001 Helligkeitssensor.<br>• 4-Port USB-Hub & Dual 20W USB-PD Schnelllader im Cockpit.<br>• Ottocast Watchdog & automatische Zündungstrennung.<br>• Lenker-PTT (< 0,4 ms) und dynamische Fahrtwind-AGC über Knowles MEMS. |
| **Tier 3: Heckradar-Option** | Zentralbox + Front Node + Radar | • Alle Tier 2 Funktionen + Wheeltec MR20 77 GHz oder Garmin Varia auf Peitsche 5.<br>• Akustische Warn-Pings im Helm, optische Warn-Flügel & Spiegel-LEDs (Port `J9`).<br>• Automatische Action-Cam Bookmarks bei kritischem Radar TTC (< 2,5 s). |

### 8.1 Schutzmechanismen gegen fehlende Daten (Zero-Crash Policy)
1. **Asynchrone Non-Blocking Schnittstellen:** Die Kommunikation über UWB, LoRa (SPI) und Radar (UART2) läuft mit FreeRTOS Timeouts (`pdMS_TO_TICKS(50)`). Es existieren **keine blockierenden `while(1)`-Warteschleifen**.
2. **Dynamische DLE-Fähigkeiten (`omm_get_capabilities_vector`):** Die Zentralbox deklariert nur jene Hardware-Flags im Mesh, die physisch antworten (`gnss_is_connected()`, `is_linked`, `can_bus_is_connected()`).
3. **Sensor-Fusion Autarkie (`adr_ekf_filter.cpp`):** Fällt GNSS weg (z. B. Tunnel oder Front Node offline), schaltet der EKF verzögerungsfrei auf **Dead Reckoning** um und stützt sich auf IMU und CAN-Raddrehzahl.
4. **Fehlertoleranter Audiomixer (`audio_dsp_pipeline.cpp`):** Fehlt das Knowles MEMS Mikrofon des Front Nodes, läuft der Brickwall-Limiter und AGC-Level auf festem Rider-Standardwert (Unity Gain `1.0f`).
