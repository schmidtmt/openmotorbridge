# 09 - Firmware-Architektur, FreeRTOS Tasks & Rollback-OTA

*Hinweis: Sämtliche CAD-, Elektronik- und Blockschaltbilder spiegeln die standardisierte v10.0 Node-Architektur (PCBA 01 bis 10) wider.*

Dieses Dokument spezifiziert die systemweite Firmware-Architektur der OpenMotorBridge v10.0 (Native USB-PD & Edge-AI Generation): die Multi-Core-Aufteilung des **ESP32-S311 AI RISC-V** Hauptcontrollers auf der Zentralbox (`PCBA 01`) mit 128-bit SIMD AI-Beschleuniger, des ESP32-S31 Front-Knotens (`PCBA 05`), des deterministischen **4-Draht Automotive USB-PD & USB 2.0 Backbones (`VBUS`, `GND`, `D+`, `D-`, Latenz < 0,2 ms)** zu allen Satelliten (Front-Node, Pod 1, Pod 2, Heckradar), der **Dual-Power Input Engine** (12V DTM & USB-PD Sink 5V–20V via LM5050 Ideal-Diode OR-ing), der **5-Gesten-Trigger-Engine** für die symmetrischen Under-Perch Spiegel-Pods (`PCBA 05B`), der LittleFS-Profil-Engine sowie der **Dual-Bank Rollback-OTA-Architektur** gegen Stromausfälle während des Flashvorgangs.

---

## 1. Multi-Core & Multi-MCU Systemarchitektur

In v10.0 ist das Gesamtsystem auf einen robusten, geschirmten **4-Draht Automotive USB-PD & USB 2.0 Bus** standardisiert. Sämtliche Daten-, Audio- und Steuerverbindungen zwischen Zentralbox und externen Knoten erfolgen leitungsgebunden mit deterministischer Latenz ($< 0{,}2\,	ext{ms}$) und massiver Ladeleistung (bis zu 60 W je Zweig):

```
+----------------------------------------------------------------------------------------+
|                        DIE FIRMWARE-KONTROLLER IM SYSTEMVERBUND (v10.0)                |
+------------------------------------------------------+---------------------------------+
| 1. ZENTRALBOX (ESP32-S311 AI RISC-V, PCBA 01)         | 2. FRONT-NODE (ESP32-S31, PCBA 05)|
+------------------------------------------------------+---------------------------------+
| * Core 0: 4-Draht USB-PD Host Engine, SX1262 LoRa    | * Core 0: USB-Backbone Client,  |
|   868 MHz, Dual-Power OR-ing, BLE, Pod Dispatcher    |   SAM-M10Q GNSS, CAN, USB-PD    |
| * Core 1: 48 kHz SIMD AI Audio-DSP, Raised-Cosine    | * Core 1: Knowles Wind-DSP,     |
|   Ducking, AGC, Qualcomm QCC3084 BT 5.4 Hub          |   5-Gesten Mirror-Pod Engine    |
+------------------------------------------------------+---------------------------------+
| 3. SATELLITEN-PODS (ESP32-C6, PCBA 03 in Pod 1 & 2)  | 4. HECK-RADAR (ESP32-C5 Sub-MCU, PCBA 08)|
+------------------------------------------------------+---------------------------------+
| * USB 2.0 Device & USB-PD Sink Controller (bis 30W)  | * Wheeltec MR20 77-GHz mmWave   |
| * ES8388 Audio Codec / USB Audio Class Streamer      | * 20 Hz Tracking-Vektoren via   |
| * OptoMOS PTT-Keying & Direktes Headset-Interface    |   CAN / High-Speed Serial       |
+------------------------------------------------------+---------------------------------+
```

### 1.1 Core-Aufteilung des ESP32-S311 AI Hauptcontrollers der Zentralbox (320 MHz RISC-V)

#### CORE 0 (Kommunikation, Telemetrie, 4-Draht USB-Backbone & Power-Management):
- **Automotive USB-Backbone Host Engine (`usb_vehicle_backbone.cpp`):** Verwaltet die USB 2.0 High-Speed Verbindung über den onboard USB2514B Hub zu Front-Node und Koffer-Pods. Empfängt Lenker-PTT- und Gesten-Events ($< 0{,}15\,	ext{ms}$), Knowles MEMS Schallpegelwerte, 10 Hz Multi-GNSS-Pakete und Pod-Telemetrie.
- **Dual-Power Input Manager (`dual_power_mgr.cpp`):** Überwacht das TI LM5050-Q1 Ideal-Dioden-OR-ing zwischen 12V Bordnetz (Deutsch DTM-6 / Kabel 1) und USB-PD Sink (5V–20V USB-C). Ermöglicht nahtloses Umschalten und vollständiges Flashen, Kalibrieren und Testen auf der Werkbank ohne 12V-Labornetzgerät.
- **Gestaffeltes Power-Sequencing (`power_sequencer.cpp`):** Steuert die Automotive eFuses `TI TPS25982` auf PCBA 01 zur Vermeidung von Einschalt-Stromspitzen:
  - $T = 0\,	ext{ms}$: Zentralbox (PCBA 01) und Front-Node (PCBA 05) starten synchron bei Zündung EIN (KL15).
  - $T = 200\,	ext{ms}$: Pod 1 (VBUS über eFuse mit Soft-Start-Rampe).
  - $T = 350\,	ext{ms}$: Pod 2 (VBUS über eFuse mit Soft-Start-Rampe).
  - $T = 500\,	ext{ms}$: Heckradar (+12V geschaltet an Peitsche 3).
- **LoRa 868 MHz Mesh Engine (`lora_mesh_engine.cpp`):** Direkte SPI-Anbindung an den onboard Semtech SX1262 Transceiver auf PCBA 01 (24/7 USV-gepuffert für Diebstahl-Sentry und Gruppen-Telemetrie).
- **BLE GATT Server (`ble_service_server.cpp`):** Web-Bluetooth Anbindung für das PWA-Dashboard (`0x180D`, `0x180A`, `0xFFE0`).
- **Group Split Fallback Engine (`group_split_rescue_engine.cpp`):** Automatische Zustandsmaschine zur Überbrückung von Funkschatten zwischen Sena Mesh, Cardo DMC, OMM 2.4 GHz und LoRa 868 MHz Notfall-Beacon.
- **WebDAV TLS 1.3 Client:** Asynchroner Upload von GPX-Touren zu Nextcloud/Synology im Heim-WLAN bei Zündung AUS.
- **SDIO Logging Task:** 4-Bit High-Speed SD-Karten-Logger mit Ringpuffer und automatischem BGH-Datenschutz-Purge.
- **ADR-EKF Filter:** 15-State Sensorfusion aus 10 Hz Multi-GNSS-Telemetrie (vom Front-Knoten via USB) und onboard Bosch BMI270 6-Achs IMU für unterbrechungsfreie Navigation in Tunneln.

#### CORE 1 (Echtzeit Edge-AI Audio-DSP & Qualcomm QCC3084 Hub @ Höchste Priorität):
- **128-bit SIMD AI Vektor-Beschleuniger:** Echtzeit-Filterung von Windgeräuschen, Transienten und Motorvibrationen sowie akustische Szenen-Klassifikation direkt auf dem Chip.
- **Qualcomm QCC3084 Dual-Helm Audio Hub (`bluetooth_audio_manager.cpp`):** Steuert den dedizierten QCC3084 BT 5.4 Audio-SoC (`U9` auf PCBA 01) über UART (GAIA/AT) für hardware-beschleunigtes Dual-A2DP (aptX HD / Adaptive) an Fahrer- und Sozius-Helme, LE Audio Auracast und synchronen HFP 1.8 Wideband-Sprachkanal.
- **I2S Audio DMA Receiver & Transmitter:** Latenzarmes Streaming über ES8388 Audio-Codec und Qualcomm QCC3084 ($f_s = 48\,	ext{kHz}, 24\,	ext{Bit}$, Double-Buffer à 128 Samples = $2{,}67\,	ext{ms}$).
- **Raised-Cosine Ducking Engine:** Knackfreie, stetig differenzierbare Audio-Absenkung bei Durchsagen oder Radarwarnungen.
- **Dynamische AGC-Lautstärkeregelung:** Gleitende Anhebung des Helm-Ausgangspegels basierend auf dem Front-Node Fahrtwindpegel.
- **Lookahead Brickwall-Limiter:** Verhindert digitales Clipping über $0\,	ext{dBFS}$.

---

## 2. Deterministischer 4-Draht Automotive Bus (`usb_vehicle_backbone.cpp`)

Alle Daten-, Steuer- und Audioverbindungen im Fahrzeugnetzwerk nutzen den geschirmten 4-Draht Automotive USB-PD & USB 2.0 Bus (`VBUS`, `GND`, `D+`, `D-`):
- **Zero RF Congestion & Zero De-Sensing:** Durch den physischen Kabelbus entfallen jegliche UWB- oder Funk-Backbone-Interferenzen im Cockpit oder an den Kofferflanken.
- **Deterministische Latenz:** Transferzeiten $< 0{,}2\,	ext{ms}$ über native USB 2.0 Interrupt- und Bulk-Endpunkte.
- **Automotive USB-PD:** Bis zu 60 W Ladeleistung je Strang mit automatischer Leistungsverteilung.

```cpp
enum UsbBackbonePktType : uint8_t {
    // --- Node-Management & System-Heartbeat ---
    USB_DESC_NODE_ANNOUNCE     = 0x01,  // Boot-Handshake: Node-Typ (Front, Pod 1/2, Radar), UID, FW-Version
    USB_PKT_NODE_HEARTBEAT     = 0x02,  // 1 Hz Heartbeat: Uptime, VBUS-Spannung, Stromaufnahme, Bus-Status
    USB_PKT_GESTURE_EVENT      = 0x03,  // 5-Gesten Lenkertaster (< 0.15 ms Latenz): Short, Double, Triple, Long, Hold

    // --- Konsolidierte Telemetrie (10 Hz Frame) & Peripherie ---
    USB_PKT_FRONT_TELEMETRY    = 0x04,  // Konsolidierter 10 Hz Frame: GNSS PVT + Wind-RMS + TMP117 + Lux + CAN
    USB_PKT_WIRELESS_CP_AA_STAT= 0x05,  // COTS CarPlay / Android Auto Bridge Status, Stromaufnahme, Auto-Café Timer

    // --- Steuerbefehle & System-Synchronisation ---
    USB_CMD_POWER_CYCLE        = 0x10,  // Zentralbox -> Front-Node / Pods: Kaltstart & Power-Gating
    USB_CMD_CONFIG             = 0x11,  // Zentralbox -> Satelliten: Zündungs-Sync & Sleep-State
    USB_CMD_PAIRING_REQUEST    = 0x12,  // Pairing-Ablauf nach SW1 Tasterdruck (60s Fenster)

    // --- Pod-Steuerung & Schnittstellen-Protokoll (Pod 1 & 2) ---
    USB_DESC_POD_ANNOUNCE      = 0x20,  // Handshake: Hardware-Klasse, Modell-ID, UID, Status, USB-PD Profil
    USB_CMD_POD_CONTROL        = 0x21,  // Zentralbox -> Pod: PTT-Trigger, BLE-Kommando, Audio-Routing
    USB_PKT_POD_ACK            = 0x22,  // Pod -> Zentralbox: Ausführungsquittung & Status

    // --- Digitales USB Audio Class Backbone (Bidirektional, 48 kHz / 24-Bit PCM) ---
    USB_PKT_AUDIO_STREAM_DOWN  = 0x24,  // Zentralbox -> Pods: Master-Mix an Headsets (Mic + Navigation + TTS)
    USB_PKT_AUDIO_STREAM_UP    = 0x25,  // Pods -> Zentralbox: Intercom Spk-Out / Helm-Audio zur Zentralbox
    USB_PKT_AUDIO_MEDIA_UP     = 0x26,  // Front-Node -> Zentralbox: Musik / Navigations-Ansagen

    // --- Radar 2.0 (PCBA 08 via CAN/UART): Vorfilterung & LED-Makrosteuerung ---
    USB_PKT_RADAR_TARGETS      = 0x30,  // 20 Hz voroptimierte Zielliste (TTC, Distanz, Azimut) + URGENT-Flag
    USB_PKT_RADAR_LED_CMD      = 0x31,  // Zentralbox -> Radar: Makro-Befehl (Idle, Warnung, Prio-1 Strobe)

    // --- Zero-Disassembly WebUSB DFU Flashing ---
    USB_PKT_FW_UPDATE_PUSH     = 0x50,  // Host -> Nodes: Blockweises Firmware-Update über USB 2.0
    USB_PKT_FW_UPDATE_DONE     = 0x51   // Nodes -> Host: Flash-Quittung / Reboot-Ready
};
```

### 2.1 Latenzbudget der 4-Draht USB PTT-Signalkette
1. **Lenkertaster Schließen:** $12\,\mu	ext{s}$ Hardware-Schmitt-Trigger-Entprellung am Front-Node.
2. **Front-Node ESP32-S31 GPIO-Interrupt:** $15\,\mu	ext{s}$ ISR-Verarbeitungszeit & Gesten-Detektor.
3. **USB 2.0 Interrupt Transfer (Front -> Zentralbox):** $60\,\mu	ext{s}$ Transitzeit über geschirmten 4-Draht Bus.
4. **Zentralbox ESP32-S311 Core 0 Dispatcher:** $20\,\mu	ext{s}$ Event-Parsing & PTT-Routing.
5. **Pod-Interface OptoMOS / Digital Audio:** $< 10\,\mu	ext{s}$ Schaltzeit des OptoMOS-Relais `CPC1017N` oder digitaler USB-Audio Stream.
* **Gesamtlatenz:** **$pprox 0{,}12\,	ext{ms}$** (Mehr als 80-fach schneller als die menschliche Wahrnehmungsschwelle von $10\,	ext{ms}$).

### 2.2 Dual-Power Input Management & Werkbank-Testing
- **TI LM5050-Q1 Ideal-Diode OR-ing:** Entkoppelt das 12V Bordnetz (Deutsch DTM-6) und den USB-PD Sink Eingang (5V–20V über den nativen USB-C Port) verlustfrei ohne thermischen Spannungsabfall klassischer Schottky-Dioden.
- **Nahtlose Umschaltung:** Wird das Motorrad bei gestecktem USB-C Ladekabel gestartet, übernimmt die 12V-Schiene unterbrechungsfrei die Last.
- **Zero-Disassembly Benchtop Flashing:** Auf der Werkbank kann das gesamte System mit jedem handelsüblichen USB-C PD Handy- oder Laptop-Netzteil betrieben, geflasht und kalibriert werden – ein schweres 12V-Labornetzgerät ist nicht erforderlich!

---

## 3. BLE GATT Server Architektur (`ble_service_server.cpp`)

Das System exponiert standardkonforme Bluetooth SIG Services sowie proprietäre Vendor-Services für das PWA-Dashboard:

| Service UUID | Characteristic UUID | Properties | Funktion & Datenschema |
| :--- | :--- | :--- | :--- |
| **`0x180D`** (Audio RMS & Env)       | **`0x2A37`** | Notify | Knowles MEMS Fahrtwind-Schallpegel (50 Hz dB(A)) & TMP117 Temperatur. |
| **`0x180A`** (Device Information)    | **`0x2A24`** | Read   | Hardware-Revision (`OMB-V8.5-2026.2`), Serial, Firmware-Build. |
| **`0xFFE0`** (Proprietary Control)   | **`0xFFE1`** | Write  | Steuerbefehle: `0x01` Profilwechsel, `0x02` Reset, `0x09` Pod Control Opcode, `0x0A` Pairing Trigger. |
| **`0xFFE0`** (Proprietary Telemetry) | **`0xFFE2`** | Notify | 10 Hz Telemetrie-Stream: Lean-Angle (Roll/Pitch), Speed, TTC, Radar-Warnung. |
| **`0xFFE0`** (Pod Status)            | **`0xFFE3`** | Notify/Read | Pod-Status 1 & 2: 64-Bit UID, Hardware-Klasse, USB-PD Profil, Status. |

---

## 4. Universal Group Split Fallback Engine (`group_split_rescue_engine.cpp`)

Bei Touren in Bergregionen oder dichtem Wald reißen 2.4 GHz Intercom-Verbindungen (Sena Mesh / Cardo DMC) ab ca. $800\dots 1200\,\text{m}$ Distanz ab, wenn Sichtkontakt verloren geht. Die in v8.5 / v9.0 integrierte **Group Split Fallback Engine** schützt Gruppen vor dem Auseinanderreißen:

```
               GROUP SPLIT FALLBACK ENGINE ZUSTANDSAUTOMAT
+-----------------------------------------------------------------------------+
| 1. NORMAL STATUS: LINE-OF-SIGHT VERBUNDEN                                   |
|    * Bucht 1 (Sena Mesh) & Bucht 2 (Cardo DMC) voll aktiv                   |
|    * HD-Audio Stream im Helm; LoRa sendet periodische Heartbeats (0.2 Hz)   |
+-----------------------------------------------------------------------------+
|                                     v (Verbindungsverlust > 15 s)           |
| 2. RESCUE LEVEL 1: OMM 2.4 GHz KANAL-HOPPING MESH                           |
|    * Falls OMM-Modul in Pod 2 gesteckt: Erhöht TX-Power auf +20 dBm    |
|    * Sucht nach Relais-Knoten benachbarter Gruppenmitglieder                |
+-----------------------------------------------------------------------------+
|                                     v (Verbindungsverlust > 45 s)           |
| 3. RESCUE LEVEL 2: 868 MHz LoRa MESH (SX1262) TELEMETRIE & TEXT             |
|    * Reichweite bis zu 15 km (LOS) bzw. 3-5 km im Gebirge                   |
|    * Überträgt automatisch GPS-Position, Peilung, Entfernung & Distanzpfeil |
|    * Zeigt "Gruppe voraus: 2,4 km Nord-West" auf CarPlay/PWA-Dashboard      |
+-----------------------------------------------------------------------------+
|                                     v (Verbindungsverlust > 120 s)          |
| 4. RESCUE LEVEL 3: PMR446 ANALOG-VOICE FALLBACK (OPTIONAL)                  |
|    * Triggert automatischen Durchsage-Ping auf Midland Funkgerät         |
|    * Überträgt synthetisierte TTS-Ortsansage auf analogen Jedermannfunk     |
+-----------------------------------------------------------------------------+
```

---

## 5. Pod-Steuerung (PCBA 03) & Symmetrische 5-Gesten Spiegel-Pod Engine

### 5.1 Dynamische Pod- & Modell-Erkennung (Hardware-Deskriptoren & Profil-Matrix)
Zur flexiblen Anbindung moderner OEM-Intercoms ohne mechanische Hubmagnete nutzt die `PCBA 03` eine rein digitale und elektrische Identifikation:
1. **USB 2.0 Deskriptor-Handshake:** Beim Booten meldet die Trägerplatine ihre 16-Bit Modell-ID, Hardware-Klasse und 64-Bit UID nativ über USB 2.0 an die Zentralbox.
2. **Kabelstrang-Auto-Sense:** Erkennt automatisch, ob ein Sena SPIDER X Slim (Micro-Kabelpeitsche an `J_AUDIO_PWR`), ein Cardo Packtalk Edge (Air-Mount & USB-C Ladedose), ein OMM UCS 2.4 GHz Modul (USB Audio Class), ein analoges Funkgerät (Midland PMR446) oder eine hermetische Dry-Box angeschlossen ist.

| Modell-ID | Basis-Klasse | Modellbezeichnung | Physische Schnittstelle | Steuerungs- & Audio-Charakteristik |
| :---: | :---: | :--- | :--- | :--- |
| **`0x0101`** | Klasse A | **Sena SPIDER X Slim** | Micro-Kabelpeitsche an `J_AUDIO_PWR` | 3.85V Direct-DC, ES8388 Line-In/Out, BLE GATT |
| **`0x0102`** | Klasse A | **Sena +Mesh Adapter** | Interne USB-C Ladedose | Reines Bluetooth/Audio Gateway; USB-PD Ladespeisung |
| **`0x0201`** | Klasse B | **Cardo Packtalk Edge / Pro**| Air-Mount & USB-C Ladedose | DMC Gen2, USB-PD Ladespeisung ("Charge while Riding") |
| **`0x0301`** | Klasse C | **OMM UCS 2.4 GHz Modul** | Nativer USB 2.0 Port | Volldigitales USB Audio Class 2.0, IPv6-Mesh |
| **`0x0401`** | Klasse D | **Midland PMR446 (G9 Pro)** | 2-Pin Doppelklinkenpeitsche | OptoMOS PTT-Keying (`CPC1017N`), galvanisch getrennt |
| **`0x0000`** | Klasse 0 | **Dry-Box / Gepäckbucht** | Keine Audio-Endgeräte | Reiner 30W/60W USB-PD Ladeport für Smartphone/Powerbank |

### 5.2 Symmetrische Dual Under-Perch Spiegel-Pods & 5-Gesten-Engine (`PCBA 05B`)
Die beiden identischen Spiegel-Pods (`PCBA 05B`) unter den Spiegelschrauben bieten taktile Daumenbedienung und bilaterale Totwinkel-Warnung (BSD):
* **5 Gesten-Trigger:** Jeder Taster erfasst autark `SHORT_CLICK`, `DOUBLE_CLICK`, `TRIPLE_CLICK`, `LONG_PRESS` und `HOLD_GATE`.
* **100 % Freie Tastenbelegung:** Über das PWA Dashboard kann jede Geste frei einer Aktion zugewiesen werden (z. B. Push-to-Talk, Sprachassistent Siri/Google, Waze 1-Click Gefahren-Marker, Action-Cam Tags für Insta360/GoPro/DJI, Radar-Mute, Garagentor via BLE).

---

## 6. FreeRTOS Task-Architektur & Scheduling-Matrix (Zentralbox & Front-Knoten)

Das Gesamtsystem orchestriert spezialisierte Tasks über die beiden Hauptkontroller:

| Task-Name | MCU / Kern | Prio | Stack | Auslöser / Rate | IPC / Schnittstelle | Aufgabe & Funktion |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **`audio_dsp_task`** | Central Box (Core 1) | **24** | 8 KB | 48 kHz DMA ISR | FreeRTOS StreamBuffer | Latenzfreier I2S Audio-Mix, SIMD AI Rauschfilter, Ducking & AGC. |
| **`usb_backbone_task`**| Central Box (Core 0) | **22** | 6 KB | USB Host IRQ / Event | FreeRTOS StreamBuffer | 4-Draht Automotive USB 2.0 Host Engine für Front-Node & Pods (< 0.2 ms). |
| **`qcc3084_hub_task`**| Central Box (Core 1) | **21** | 4 KB | UART DMA ISR / Queue | FreeRTOS Queue / UART1| QCC3084 Supervisor: aptX HD Dual-A2DP, Auracast & HFP Call Handling. |
| **`lora_mesh_task`**  | Central Box (Core 0) | **20** | 4 KB | SX1262 IRQ / Timer  | FreeRTOS Queue        | 868 MHz LoRa Mesh Protokoll, Diebstahl-Sentry & Group Split Rescue. |
| **`gesture_engine_task`**| Front Node (Core 0)| **24** | 2 KB | GPIO Edge ISR       | USB TX Queue          | Verarbeitet Mirror-Pod Taster Links/Rechts, generiert 5 Gesten (< 0.15 ms). |
| **`radar_task`**      | Central Box (Core 0) | **16** | 4 KB | CAN / UART DMA ISR  | FreeRTOS Queue        | 20 Hz Radar-Zielvektoren von Wheeltec MR20; TTC-Berechnung & Prio-1 Ducking. |
| **`adr_ekf_task`**    | Central Box (Core 0) | **15** | 4 KB | 50 Hz Timer         | I2C / CAN-Puffer      | 15-State Kalman-Filter (SAM-M10Q GNSS + BMI270 IMU + CAN Speed). |
| **`power_mgmt_task`** | Central Box (Core 0) | **14** | 2 KB | Boot-Event / Timer  | GPIO / I2C Power      | Automotive eFuses, Dual-Power LM5050 Monitoring, gestaffelter Start. |
| **`ble_server_task`** | Central Box (Core 0) | **10** | 4 KB | Event-Driven        | NimBLE Stack          | Web-Bluetooth PWA Dashboard (GATT Services `0x180D`/`0x180A`/`0xFFE0`). |
| **`sdio_log_task`**   | Central Box (Core 0) | **8**  | 8 KB | 10 Hz Ringpuffer    | FreeRTOS RingBuffer   | 4-Bit SDIO Blackbox-Logging mit ECDSA SHA-256 Signatur. |
| **`webdav_sync_task`**| Central Box (Core 0) | **3**  | 8 KB | Nachlauf (Graceful) | LwIP TLS 1.3          | Automatischer GPX-Upload im Heim-WLAN bei Zündung AUS. |
| **`front_gnss_task`** | Front Node (Core 0)  | **20** | 4 KB | 10 Hz I2C DMA       | J12 Qwiic / USB TX    | u-blox SAM-M10Q UBX-NAV-PVT Parsing, TMP117 Temp & OPT3001 Lux. |
| **`front_mems_task`** | Front Node (Core 1)  | **18** | 4 KB | 48 kHz DMA          | Vector-DSP Filter     | Knowles I2S Digitalmikrofon A-Weighting & RMS-Pegel via Xtensa DSP. |
| **`front_can_task`**  | Front Node (Core 0)  | **16** | 4 KB | TWAI Interrupt      | CAN Message Queue     | Liest Cockpit-CAN (falls J2 verbunden), Auto-Terminierung CPC1017N. |
| **`front_pwr_task`**  | Front Node (Core 0)  | **10** | 2 KB | 10 Hz Timer         | GPIO Lastschalter     | SW3526 USB-PD Überwachung, TPS2051B Kaltstart (2,5s), Auto-Off. |

---

## 7. LittleFS Pod-Profil-Engine & JSON-Datenstruktur

Wird ein Pod angeschlossen und meldet sich per USB (`USB_DESC_POD_ANNOUNCE`), lädt der Pod-Manager die Konfiguration aus `/storage/profiles/<UID>.json`:

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
| **Tier 1: Minimal Core** | Nur Zentralbox<br>*(Kein Front Node)* | * **Audio-Bridge & Intercoms voll aktiv:** Bucht 1 & 2 mischen latenzfrei via 4-Draht Bus.<br>* **LoRa 868 MHz Mesh aktiv:** Direkte USV-gepufferte 24/7 Diebstahl-Sentry & Tracking.<br>* **CAN-Bus aktiv:** Tacho, Drehzahl & BCM-Telemetrie über Kabel 1 (DTM-6 Pins 4/5).<br>* **IMU aktiv:** Bosch BMI270 liefert Schräglage, Pitch & Erschütterung.<br>* **ADR-EKF:** Läuft im reinen Dead-Reckoning Modus gestützt auf IMU & Raddrehzahl.<br>* **USB-Host:** Wartet passiv auf Verbindungsaufbau an den USB-Ports. |
| **Tier 2: Vollsystem mit Front Node** | Zentralbox + Front Node | * Alle Tier 1 Funktionen + deterministischer 4-Draht USB-Backbone (< 0,2 ms).<br>* u-blox SAM-M10Q Multi-GNSS mit 10 Hz PVT-Fix & Präzisions-Zeitsynchronisation.<br>* TI TMP117 Glatteis-Wächter ($\pm 0{,}1\,^\circ\text{C}$) & TI OPT3001 Helligkeitssensor.<br>* 4-Port USB-Hub & Dual 20W USB-PD Schnelllader im Cockpit.<br>* Ottocast Watchdog & automatische Zündungstrennung.<br>* Lenker-PTT (< 0,2 ms) und dynamische Fahrtwind-AGC über Knowles MEMS. |
| **Tier 3: Heckradar-Option** | Zentralbox + Front Node + Radar | * Alle Tier 2 Funktionen + Wheeltec MR20 77 GHz oder Garmin Varia (PCBA 08).<br>* 2-Draht 12V DC-Power & Telemetrie vom 16-Pin Peripherie-Header (Strang 4).<br>* Akustische Warn-Pings im Helm, optische Warn-Flügel & Spiegel-LEDs (Port `J9`).<br>* Automatische Action-Cam Bookmarks bei kritischem Radar TTC (< 2,5 s). |

### 8.1 Schutzmechanismen gegen fehlende Daten (Zero-Crash Policy)
1. **Asynchrone Non-Blocking Schnittstellen:** Die Kommunikation über USB, LoRa (SPI) und Radar läuft mit FreeRTOS Timeouts (`pdMS_TO_TICKS(50)`). Es existieren **keine blockierenden `while(1)`-Warteschleifen**.
2. **Dynamische DLE-Fähigkeiten (`omm_get_capabilities_vector`):** Die Zentralbox deklariert nur jene Hardware-Flags im Mesh, die physisch antworten (`gnss_is_connected()`, `is_linked`, `can_bus_is_connected()`).
3. **Sensor-Fusion Autarkie (`adr_ekf_filter.cpp`):** Fällt GNSS weg (z. B. Tunnel oder Front Node offline), schaltet der EKF verzögerungsfrei auf **Dead Reckoning** um und stützt sich auf IMU und CAN-Raddrehzahl.
4. **Fehlertoleranter Audiomixer (`audio_dsp_pipeline.cpp`):** Fehlt das Knowles MEMS Mikrofon des Front Nodes, läuft der Brickwall-Limiter und AGC-Level auf festem Rider-Standardwert (Unity Gain `1.0f`).


---

## 9. Autonome Gruppen-Lifecycle State Machine, Kaffeepausen-Persistenz & Anruf-Management

### 9.1 Hierarchisches Zero-Touch Discovery: Micro-Cluster (Heim-Setup) & Macro-Merge am Treffpunkt
Die Koordination von gemeinsamen Ausfahrten erfordert weder Smartphone-Apps noch manuelle Konfiguration am Lenker. Das System arbeitet mit einer hierarchischen Zwei-Ebenen-Architektur:
1. **Tier 1: Verteilter Start & Autarkes Micro-Cluster (Heim-Setup):**
   * Starten eng verbundene Fahrer (z. B. Familie, Partner auf zwei Bikes oder enge Freunde) im heimatlichen Nahbereich ($d < 500\,\text{m}$, Zeitfenster $\Delta t < 15\,\text{min}$), schließen sich ihre OMB-Zentralboxen über das Smart-Keyfob-FOB-Kanalprofil **sofort zu einem autarken Micro-Cluster** zusammen.
   * Auf der Anfahrt zum großen Haupttreffpunkt läuft die Sprachkommunikation und das Routing privat und verzögerungsfrei über diesen Micro-Kanal.
2. **Tier 2: Macro-Merge am Sammel-Treffpunkt (Stillstands-Erkennung & Discovery):**
   * Am gemeinsamen Treffpunkt (z. B. Autobahnraststätte, Tankstelle) versammeln sich verschiedene Micro-Cluster und Einzelfahrer im Stillstand ($v = 0\,\text{km/h}$, $d < 40\,\text{m}$).
   * Die Knoten detektieren die Versammlung und wechseln in den Zustand `PRE_MERGE_DISCOVERY`. Über LoRa Kanal 1 tauschen sie diskrete Discovery-Beacons aus.

### 9.2 Gestaffelter Wiederanfahr-Puffer (Konvoi-Toleranz) & Multi-Route Sub-Groups
1. **Gestaffelter Wiederanfahr-Puffer:**
   * Beim Losfahren einer 10- bis 20-köpfigen Großgruppe rollen die Motorräder nie zeitgleich an, sondern ziehen sich über 60 bis 120 Sekunden auseinander.
   * Der Algorithmus toleriert dieses gestaffelte Anfahren über einen Beschleunigungs- und Heading-Filter.
2. **Generierung des Macro-Cluster Session-Keys:**
   * Sobald die Kolonne in dieselbe Fahrtachse eingeschwenkt ist ($\Delta\text{Heading} < 30^\circ$, $v > 25\,\text{km/h}$ über $90\,\text{s}$), erzeugt ein temporärer Master (niedrigste MAC) einen gemeinsamen **AES-256 Großgruppen-Session-Key** und verteilt diesen verschlüsselt an alle Teilnehmer.
   * **Dual-Layer Topology:** Die Großgruppe nutzt den Macro-Kanal für Konvoi-Funk, Gefahrenwarnungen und DLE-Mesh-Routing. Das unterliegende Micro-Cluster bleibt als Sub-Layer im Speicher erhalten.
3. **Multi-Route-Start:**
   * Treffen sich am Startpunkt mehrere Gruppen mit unterschiedlichen Routen (z. B. Cruiser vs. Pässe-Heizer), überwacht die Firmware in den ersten 3 Minuten die Richtungsvektoren (**Heading-Lernphase**).
   * Driften die Vektoren auseinander, teilt sich das System vollautomatisch in zwei autonome Sub-Gruppen auf - ohne Fehlalarme.

### 9.3 Der "Doubt-Timer" bei Kursabweichungen (Prävention vor Fehlalarmen)
Weicht ein Teilnehmer vom gemeinsamen Routen-Vektor ab (z. B. verpasste Autobahnausfahrt oder Abbiegen an einer Kreuzung), schlägt das System nicht unmittelbar Alarm:
* **Start des Doubt-Timers ($T_{\text{doubt}} = 15\dots 30\,\text{s}$):** Das System stuft den Fahrer temporär in den Zustand `DOUBT_SPLIT` ein.
* **Szenario A (Verpasster Abzweig):** Hält der Fahrer nach 10 Sekunden an oder verringert die Geschwindigkeit drastisch, ertönt im Helm die lokale TTS-Ansage: *"Möglicher Kursverlust der Gruppe - bitte Route prüfen"*.
* **Szenario B (Bewusstes Verlassen):** Fährt der Fahrer mit hoher Geschwindigkeit auf der abweichenden Route kontinuierlich weiter, deklariert die State Machine nach Ablauf von $T_{\text{doubt}}$ das reguläre Verlassen der Gruppe (`GROUP_LEFT`).

### 9.4 Kaffeepausen-Schutz & 30-Minuten Deep-Sleep Persistenz
Bei Pausen (Tankstelle, Restaurant, Café) muss die Gruppe zusammengehalten werden, ohne die Motorradbatterie zu belasten:
1. **Stillstands-Cluster ($v = 0\,\text{km/h}$ & Radius $< 30\,\text{m}$):** Reduzieren alle Motorräder die Geschwindigkeit auf null und schalten die Motoren ab, wechselt die State Machine in den Modus `GROUP_PAUSED`.
2. **USV-Nachlauf & Deep Sleep:** Nach 15 Minuten Inaktivität schaltet die Zentralbox die Peripherie (Pods, Front Node, Radar) ab und versetzt den ESP32-S31 in den stromsparenden Tiefschlaf ($< 150\,\mu\text{A}$ aus der 1S LiPo-USV).
3. **Persistierung des Gruppen-States in NVS & RTC-RAM:** Vor dem Schlafengehen sichert die Firmware folgende Daten im nichtflüchtigen Speicher:
   * 256-Bit AES Gruppen-Session-Key (Macro & Micro)
   * Vollständige Teilnehmer-Liste (Node-UIDs, Rufzeichen, Rollen)
   * Aktueller Gruppen-Kanal und Mesh-Sequenznummern
   * Letzte bekannte GNSS-Referenzkoordinate
4. **Nahtlose Rekonstitution nach 30+ Minuten:** Schalten die Fahrer nach 30 oder 60 Minuten die Zündung wieder ein, lädt die Firmware den Gruppen-Status in $< 50\,\text{ms}$ aus dem NVS. Die Gruppe ist **sofort und ohne erneute Discovery wieder voll einsatzbereit**.

### 9.5 Spontaner Gruppenbeitritt während der Fahrt (Proximity-Flyby & Unterwegs-Treffpunkt)
Trifft ein Fahrer während der Tour auf die Gruppe (z. B. Aufgabeln an einem vereinbarten Treffpunkt entlang der Route):
* **Proximity-Flyby Kriterium:** Nähert sich ein OMB-Node auf $< 50\,\text{m}$ und fährt für mindestens $30\,\text{s}$ im gleichen Kursvektor (Geschwindigkeit $\Delta v < 15\,\text{km/h}$, Fahrtrichtung $\Delta \theta < 15^\circ$), sendet der Master ein diskretes Einladungs-Beacon.
* **One-Click Bestätigung:** Im Helm des Gruppenleiters und des beitretenden Fahrers ertönt: *"Neuer Teilnehmer in Reichweite - Beitreten?"*. Ein einfacher Klick auf die Lenker-PTT bestätigt den Beitritt; der Session-Key wird in $< 200\,\text{ms}$ übertragen.
* **Unterwegs-Treffpunkt:** Steht der beitretende Fahrer an einer Raststätte oder Kreuzung und schließt sich dem Konvoi an, genügt am Treffpunkt ein Doppelklick auf die PTT-Taste, um den Quick-Join zu initiieren.

### 9.6 Gestaffelte End-of-Trip Dispersion & Re-Aktivierung des Micro-Clusters
Am Ende der Tagestour erfolgt die saubere, lautlose Trennung der Großgruppe bei gleichzeitigem Erhalt des Micro-Clusters:
1. **End-of-Trip Stillstand (`PRE_DISPERSE`):**
   * Am finalen Sammelpunkt schalten alle Fahrer die Motoren ab ($v = 0\,\text{km/h}$, KL15 AUS). Nach 5 Minuten Stillstand wechselt die State Machine in den Zustand `PRE_DISPERSE`.
2. **Schweigendes Macro-Disperse:**
   * Verabschieden sich die Teilnehmer und fahren in unterschiedliche Himmelsrichtungen auseinander, schließt sich die Macro-Session vollkommen geräuschlos ohne Fehlalarme.
3. **Automatischer Erhalt des Micro-Clusters für den Heimweg:**
   * Das unterliegende Micro-Cluster (Familie / Buddies) wird **automatisch wieder als primärer Kommunikationskanal geschaltet**.
   * Die Gruppe kann den gesamten Heimweg ohne erneutes Pairing oder manuelle Umschaltung miteinander sprechen, bis jeder zu Hause angekommen ist.

### 9.7 Smartphone-Anruf-Erkennung (HFP 1.8 via Qualcomm QCC3084) & Intelligenter PTT-Schutz
Geht auf dem gekoppelten Smartphone ein Telefonat ein, erkennt der **Qualcomm QCC3084 Hardware-Audio-SoC (`U9`)** über das Hands-Free Profile (HFP 1.8) den Status `RINGING` bzw. `CALL_ACTIVE` und meldet ihn per UART (`+HFP_STATUS`) in $< 1\,\text{ms}$ an den ESP32-S31:
1. **Mikrofon-Mute zur Gruppe:** Das Helm-Mikrofon wird für die Intercom- und Mesh-Kanäle sofort stummgeschaltet. Das private Telefonat wird unter keinen Umständen in die Motorradgruppe übertragen.
2. **PTT-Lock (Befehlssperre):** Während des Telefonats werden PTT-Tastendrücke am Lenker **vollständig für Sonderfunktionen gesperrt**:
   * Ein Klick auf PTT wird *nicht* als Start einer Action-Cam, kein HiLight-Tag und kein Durchruf auf Analogfunk/PMR interpretiert.
   * Der Tastendruck wird transparent an den QCC3084 weitergeleitet (`AT+ATA` zum Abheben / `AT+ATH` zum Auflegen des Anrufs).
3. **Prio-1 Sicherheits-Overlay (Radar & SOS):** Selbst während eines intensiven Telefonats bleiben lebenswichtige Radar-Kollisionswarnungen (Prio 1) und Gruppen-Notrufe aktiv. Sie werden mit $-12\,\text{dB}$ geducktem Telefon-Audio klar verständlich in den Helm eingespielt.
4. **Automatischer Reconnect:** Sobald der Anruf beendet ist (`CALL_TERMINATED`), kehrt der Audio-Router in $< 100\,\text{ms}$ in den normalen gemischten Intercom-Betrieb zurück.

### 9.8 Alarm-Dispatch & Zielgruppen-Routing: Diskrete Signalisierung (Human-in-the-Loop)

Aus dem Grundsatz *"Den Lead unterstützen, nicht ersetzen"* ([Kapitel 01](01_system_architecture.md)) und der Realität gemischter Gruppen ([Kapitel 04, Abs. 2.8](04_mesh_lora_navigation.md)) leitet die Firmware ein strikt hierarchisches und diskretes Alarm-Dispatching ab:

```c
typedef enum {
    SCOPE_SELF_ONLY   = 0x01, // Nur der eigene Fahrer (Radar-Toter-Winkel, Sensor-Fehler, lokaler Zweifel)
    SCOPE_MICRO_BUDDY = 0x02, // Eigenes Micro-Cluster (Familie/Freunde aus dem gemeinsamen Start-Cluster)
    SCOPE_LEAD_SWEEP  = 0x04, // Taktische OMB-Anker (Spitze und Schlusslicht der Gruppe)
    SCOPE_ALL_MACRO   = 0x08  // Vollständige Großgruppe (nur Prio-1 SOS / Crash-Notruf / Geisterfahrer)
} AlarmTargetScope;

typedef struct __attribute__((packed)) {
    uint8_t  pkt_type;        // LORA_PKT_ALARM (0x12)
    uint32_t origin_node_id;  // UID des auslösenden Nodes
    uint8_t  alarm_severity;  // 1 = INFO, 2 = WARNING (Split/Doubt), 3 = CRITICAL (SOS/Crash)
    uint8_t  target_scope;    // Bitmask aus AlarmTargetScope
    uint16_t reason_code;     // z. B. CONVOY_SPLIT_SUSPECTED, TIRE_PRESSURE_LOSS
    int32_t  latitude;        // 1e-7 deg
    int32_t  longitude;       // 1e-7 deg
    uint16_t crc16;
} LoRaAlarmPacket;
```

#### Lokale Aktuator-Kaskade statt Roboter-TTS
Empfängt ein Node ein `LoRaAlarmPacket` (oder löst lokal einen Alarm aus), greift die lokale Aktuator-Prioritätsmatrix:

```
[Alarm-Event]
      |
      +---> 1. Smart-Keyfob (PCBA 07) : Haptisches Vibrationsmuster (LRA-Motor in der Jackentasche)
      +---> 2. Lokales Helm-Audio     : Dezenter Zweiklang-Gong (NUR im eigenen Headset via BLE)
      +---> 3. Spiegel-LEDs (PCBA 05) : Kurzes Doppelblinken am Rückspiegel (peripheres Sichtfeld)
      +---> 4. PWA Dashboard (BLE/WiFi): Optischer Warnbanner mit Entfernungs- und Richtungsvektor
      |
      X (BLOCKIERT): Keine automatische TTS-Injektion in fremde Meshes (Sena Mesh / Cardo DMC)!
```

#### Fahrer-Souveränität & Handlungsablauf
1. **Kein Stören des Gruppen-Funks:** Der Gruppen-Sprechkanal (Sena/Cardo) bleibt vollkommen frei von automatisierten Computerstimmen.
2. **Schnelle Selbstkontrolle:** Der OMB-Fahrer spürt die Vibration am Keyfob, wirft einen kurzen Blick in den Rückspiegel oder auf das Dashboard und erkennt:
   * *Fall A (Eigener Rückstand):* Der Fahrer sieht, dass er den Anschluss verloren hat -> beschleunigt oder passt die Linie an, ohne dass die Gruppe behelligt werden muss.
   * *Fall B (Konvoi hinter ihm abgerissen):* Der Fahrer sieht im Rückspiegel oder am HUD, dass das Sweep-Bike oder Nachfolger fehlen -> Er betätigt aktiv die PTT-Taste am Lenker und funkt den Tourguide mit seiner eigenen, natürlichen Stimme an (*"Du, vorn kurz Tempo raus, hinten an der Kehre hängt jemand fest"*).
3. **Harmonie mit Kapitel 01:** Die Technik liefert verlässliche Sensor- und Telemetriedaten als diskreter Co-Pilot im Hintergrund, lässt aber die Führungskompetenz, soziale Gruppenabstimmung und Entscheidungsgewalt zu 100 % in den Händen der fahrenden Menschen.

---

## 8. Build- & Flash-Anleitung (Developer Guide)

Für die schrittweise Einrichtung der ESP-IDF Toolchain (v5.2 / v5.3 LTS), das Kompilieren der sechs Firmware-Ziele (`main_controller`, `front_node`, `pod_gateway`, `radar_submcu`, `omm_module`, `omm446_module`), das Erstellen der LittleFS-Dateisystem-Images für Pod- und Fahrzeugprofile sowie das Flashen und Debuggen via USB-C verweist OpenMotorBridge auf den zentralen Entwickler-Leitfaden:

> [!TIP]
> Die vollständige Schritt-für-Schritt-Anleitung mit allen CLI-Befehlen und Fehlerbehebungsstrategien ist dokumentiert in:  
> [`firmware/README.md`](../../firmware/README.md)

### 8.1 Schnellübersicht der Build-Befehle

```bash
# Umgebung laden
. $HOME/esp/esp-idf-v5.2/export.sh

# 1. Hauptcontroller (Zentralbox PCBA 01)
cd firmware/main_controller
idf.py set-target esp32s3
idf.py build flash monitor

# 2. Front-Knoten (PCBA 05)
cd ../front_node
idf.py set-target esp32s3
idf.py build flash monitor

# 3. Satelliten-Pod Trägerplatine (PCBA 03)
cd ../pod_gateway
idf.py set-target esp32c6
idf.py build flash monitor

# 4. Heck-Radar Sub-MCU (PCBA 08)
cd ../radar_submcu
idf.py set-target esp32c6
idf.py build flash monitor

# 5. OMM 2.4 GHz UCS Funkmodul (PCBA 09)
cd ../omm_module
idf.py set-target esp32c6
idf.py build flash monitor

# 6. OMM 446 MHz PMR/DMR Funkmodul (PCBA 10)
cd ../omm446_module
idf.py set-target esp32c6
idf.py build flash monitor
```


