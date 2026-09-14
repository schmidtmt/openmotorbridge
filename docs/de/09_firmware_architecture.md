# 09 - Firmware-Architektur, FreeRTOS Tasks & Rollback-OTA

Dieses Dokument spezifiziert die systemweite Firmware-Architektur der OpenMotorBridge v8.0: die Multi-Core-Aufteilung des ESP32-S3 Hauptcontrollers, die Coprozessoren (RP2040 im Heck-Pod 3 und ESP32-S3 im Front-Knoten), das **ESP-NOW Low-Latency-Protokoll (< 1,8 ms)**, die LittleFS-Profil-Engine sowie die **Dual-Bank Rollback-OTA-Architektur** gegen Stromausfälle während des Flashvorgangs.

---

## 1. Multi-Core & Multi-MCU Systemarchitektur

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        DIE 3 FIRMWARE-KONTROLLER IM VERBUND                            │
├──────────────────────────────────────┬─────────────────────────┬───────────────────────┤
│ 1. ZENTRALBOX (ESP32-S3 Dual-Core)   │ 2. REAR POD 3 (RP2040)  │ 3. FRONT-NODE (ESP32-S3)│
├──────────────────────────────────────┼─────────────────────────┼───────────────────────┤
│ • Core 0: BLE, WebDAV, SDIO, ESP-NOW │ • Core 0: NMEA/UBX 10Hz │ • Core 0: ESP-NOW/BLE │
│ • Core 1: Echtzeit 48kHz Audio-DSP   │ • Core 1: LoRa SX1262   │ • Core 1: Vector-DSP  │
└──────────────────────────────────────┴─────────────────────────┴───────────────────────┘
```

### 1.1 Core-Aufteilung des ESP32-S3 Hauptcontrollers (240 MHz)

#### CORE 0 (Kommunikation, Telemetrie & System):
- **BLE GATT Server:** Web-Bluetooth Anbindung für das PWA-Dashboard (`0x180D`, `0x180A`).
- **ESP-NOW Front-Node Client (`esp_now_front_node_client.cpp`):** Unterbrechungsfreier Empfang von Lenker-PTT-Events ($< 1{,}8\,\text{ms}$) und Knowles MEMS dB(A)-Schallpegelwerten.
- **Dual 1-Wire Kassetten-Manager (`cartridge_onewire.cpp`):** Pollt zyklisch Port 1 & 2 auf 64-Bit ROM-IDs (vom Kassetten-MCU emuliert oder DS2401) und bindet LittleFS JSON-Profile ein.
- **Smart Cartridge Dispatcher & Opto-Puls-Sequenzer (`opto_pulse_sequencer.cpp`):** Erkennt Smart Cartridges (PCBA 03 Rev 2.0) und sendet 1-Byte Opcodes via Single-Wire UART auf Pin 5 (19.200 Baud) zur Ansteuerung der 4 mechatronischen Aktuatoren; schaltet bei PMR446-Funk alternativ auf TLP222A Relais-Tastung um.
- **WebDAV TLS 1.3 Client:** Asynchroner Upload von GPX-Touren zu Nextcloud/Synology im Heim-WLAN.
- **SDIO Logging Task:** 4-Bit High-Speed SD-Karten-Logger mit Ringpuffer und automatischem BGH-Datenschutz-Purge.
- **ADR-EKF Filter:** Sensorfusion aus 10 Hz GNSS-Telemetrie und BMI270 6-Achs IMU für unterbrechungsfreie Navigation in Tunneln.

#### CORE 1 (Echtzeit Audio-DSP Engine @ Höchste Priorität):
- **I2S Audio DMA Receiver & Transmitter:** Latenzarmes Streaming über ES8388 Audio-Codec ($f_s = 48\,\text{kHz}, 24\,\text{Bit}$, Double-Buffer à 128 Samples = $2{,}67\,\text{ms}$).
- **Raised-Cosine Ducking Engine:** Knackfreie, stetig differenzierbare Audio-Absenkung bei Durchsagen.
- **Dynamische AGC-Lautstärkeregelung:** Gleitende Anhebung des Helm-Ausgangspegels basierend auf dem Front-Node Fahrtwindpegel.
- **Lookahead Brickwall-Limiter:** Verhindert Clipping über $0\,\text{dBFS}$.

---

## 2. Ultra-Low-Latency ESP-NOW Protokoll (`esp_now_front_node_client`)

Die drahtlose Verbindung zwischen Front-Knoten und Zentralbox nutzt unverschlüsselte IEEE 802.11 Vendor-Specific Action Frames mit fest vereinbarten Paketstrukturen:

```cpp
enum FrontNodePktType : uint8_t {
    PKT_TYPE_HEARTBEAT       = 0x01,  // Status, Uptime, VBUS-Spannung
    PKT_TYPE_PTT_EVENT       = 0x02,  // Lenker-PTT gedrückt/losgelassen (< 1.8 ms)
    PKT_TYPE_AUDIO_RMS       = 0x03,  // Knowles MEMS Fahrtwind dB(A) Pegel (50 Hz)
    PKT_TYPE_OTTOCAST_STATUS = 0x04,  // Status, Strom, Auto-Café Timer
    PKT_TYPE_CAN_TELEMETRY   = 0x05,  // Cockpit-CAN Telemetriedaten
    PKT_TYPE_CMD_POWER_CYCLE = 0x10,  // Zentralbox -> Front-Node: 2.5s Kaltstart
    PKT_TYPE_CMD_CONFIG      = 0x11   // Zentralbox -> Front-Node: Zündungs-Sync
};
```

### 2.1 Latenzbudget des PTT-Triggers
1. **Lenkertaster Schließen:** $12\,\mu\text{s}$ Hardware-Entprellung.
2. **ESP32-S3 GPIO-Interrupt:** $25\,\mu\text{s}$ ISR-Verarbeitungszeit.
3. **ESP-NOW Funkübertragung (2.4 GHz):** $0{,}90\,\text{ms}$ Flugzeit (99,8 % PDR).
4. **Zentralbox ESP32-S3 Core 0 ISR:** $45\,\mu\text{s}$ Frame-Parsing & Opcode-Dispatch.
5. **Kassetten-Controller & N-MOSFETs (`AO3400`):** $< 0{,}10\,\text{ms}$ Schaltzeit der mechatronischen Aktuatoren.
* **Gesamtlatenz:** **$1{,}70\,\text{ms}$** (Weit unterhalb des physiologischen Schwellwerts von $10\,\text{ms}$).

### 2.2 Front-Node Binding, Proximity-Pairing & Zero-Touch Re-Pairing

Um gegenseitige Funk-Interferenzen oder Geister-Trigger bei Gruppenfahrten und an Ampeln (mehrere OpenMotorBridge-Bikes auf engem Raum) zu 100 % auszuschließen, nutzt das System ein striktes **1:1 Hardware-Binding** mit NVS-Persistierung:

```
                  FRONT-NODE BINDING- & RE-PAIRING ZUSTANDSAUTOMAT
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. INITIAL FACTORY STATE:                                                   │
│    • Kein Front-Node MAC im NVS hinterlegt (Status: UNPAIRED)               │
│    • Zentralbox öffnet 60s Pairing-Fenster bei erstem Systemstart           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                        ▼                                    │
│ 2. PROXIMITY-PAIRING & RSSI-GATING:                                         │
│    • Front-Node sendet Pairing-Beacon mit reduzierter TX-Power (-12 dBm)   │
│    • Zentralbox akzeptiert Pairing NUR bei RSSI > -45 dBm (< 30 cm Distanz) │
│    • Fahrer muss Front-Node direkt an die Zentralbox halten                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                        ▼                                    │
│ 3. PAIRING-HANDSHAKE & NVS-PERSISTIERUNG:                                   │
│    • Zentralbox bestätigt mit Vendor-Action-Frame (Pairing-Token)           │
│    • Beide Knoten speichern Peer-MAC & Token im verschlüsselten NVS         │
│    • Status wechselt auf PAIRED & LOCKED                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                        ▼                                    │
│ 4. ZERO-TOUCH AUTOMATISCHER RE-CONNECT:                                     │
│    • Bei jedem Zündung-EIN (KL15) sendet Front-Node Heartbeat Frame         │
│    • Zentralbox prüft MAC & Token in < 5 ms -> Sofortige PTT-Bereitschaft   │
│    • Keinerlei manuelles Koppeln oder Tastendrücken im Alltagsbetrieb nötig │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. BLE GATT Server Architektur (`ble_service_server.cpp`)

Das System exponiert standardkonforme Bluetooth SIG Services sowie proprietäre Vendor-Services für das PWA-Dashboard:

| Service UUID | Characteristic UUID | Properties | Funktion & Datenschema |
| :--- | :--- | :--- | :--- |
| **`0x180D`** (Heart Rate / Audio RMS) | **`0x2A37`** | Notify | Knowles MEMS Fahrtwind-Schallpegel (50 Hz, 8-Bit dB(A) + Peak). |
| **`0x180A`** (Device Information)   | **`0x2A24`** | Read   | Hardware-Revision (`OMB-V8-2026.1`), Serial, Firmware-Build. |
| **`0xFFE0`** (Proprietary Control)   | **`0xFFE1`** | Write  | Steuerbefehle: `0x01` Profilwechsel, `0x02` Reset, `0x09` Smart Cartridge Opcode. |
| **`0xFFE0`** (Proprietary Telemetry) | **`0xFFE2`** | Notify | 10 Hz Telemetrie-Stream: Lean-Angle (Roll/Pitch), Speed, TTC, Batteriestatus. |
| **`0xFFE0`** (1-Wire & DLE Gateway)  | **`0xFFE3`** | Notify/Read | Kassetten-Status Port 1 & 2: 64-Bit UID, erkannte Klasse, DLE-Score. |

---

## 4. OMM In-System UART-Push-Flasher (`omm_flasher.cpp`)

Für Firmware-Updates des Heck-Pods 3 ohne Ausbau aus dem Fahrzeug:
* Die Zentralbox liest das Binär-Image `omm_rear.bin` und versetzt den RP2040 über UART mit dem Steuerbefehl `0xAA 0x55 0xFE 0x01 "BOOT"` in den Download-Modus.
* Die Übertragung erfolgt mit $460{,}800\,\text{Baud}$ in 1024-Byte-Blöcken ($< 6\,\text{s}$ Gesamtdauer).
* Der Front-Node (PCBA 05) wird über OTA Rollback-Partitionen via ESP-NOW bzw. das WebApp PWA Dashboard geflasht.

---

## 5. Kassetten-Tastensteuerung: Mechatronische Smart Cartridge (PCBA 03 Rev 2.0) & TLP222A Legacy-Modus

OpenMotorBridge steuert Intercoms und Funkgeräte über zwei hochoptimierte Betriebsmodi an:

### 5.1 Smart Cartridge Mechatronik-Modus (PCBA 03 Rev 2.0 – Standard für Intercoms)
Die Zentralbox kommuniziert über Pin 5 (`TRIGGER_PPS`) per 19.200-Baud Single-Wire UART mit dem Kassetten-MCU (WCH CH32V003). Dieser steuert vier unabhängige N-MOSFETs (`AO3400`) an:

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

### 5.2 TLP222A Legacy-Modus (PMR446 Funk / K7)
Für analoge Funkgeräte (z. B. Midland G9 / SA818S Transceiver) wird Pin 5/6 weiterhin als potentialfreie Relais-Tastung (PhotoMOS TLP222A) zur PTT-Tastung synchron mit dem Lenkertaster genutzt.

---

## 6. FreeRTOS Task-Architektur & Scheduling-Matrix (Alle 3 MCUs)

Das Gesamtsystem orchestriert 16 spezialisierte Tasks über 3 physikalisch getrennte Mikrocontroller mit festen Prioritäten und Kernzuweisungen:

| Task-Name | MCU / Kern | Prio | Stack | Auslöser / Rate | IPC / Schnittstelle | Aufgabe & Funktion |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **`audio_dsp_task`** | ESP32-S3 Main (Core 1) | **24** | 8 KB | 48 kHz DMA ISR | FreeRTOS StreamBuffer | Latenzfreier I2S Audio-Mix, Raised-Cosine Ducking & AGC. |
| **`esp_now_rx_task`** | ESP32-S3 Main (Core 0) | **22** | 4 KB | Event-Queue | Direct-to-Task Notify | Verarbeitet Front-Node PTT-Events ($< 1{,}8\,\text{ms}$) & Windpegel. |
| **`smart_act_task`** | ESP32-S3 Main (Core 0) | **18** | 2 KB | Event-Queue | FreeRTOS Queue | Dispatched 1-Byte Opcodes via Single-Wire UART bzw. steuert TLP222A Relais. |
| **`radar_proc_task`** | ESP32-S3 Main (Core 0) | **16** | 4 KB | 20 Hz UART2 ISR | FreeRTOS Queue / UART | Garmin Varia / mmWave Parsing, TTC-Berechnung & Prio-1 Ducking. |
| **`adr_ekf_task`** | ESP32-S3 Main (Core 0) | **15** | 4 KB | 50 Hz Timer | I2C / CAN-Puffer | 15-State Kalman-Filter (GNSS + IMU + Raddrehzahl). |
| **`ble_server_task`** | ESP32-S3 Main (Core 0) | **10** | 4 KB | Event-Driven | NimBLE Stack | Web-Bluetooth PWA Dashboard (GATT Services `0x180D`/`0x180A`). |
| **`sdio_log_task`** | ESP32-S3 Main (Core 0) | **8** | 8 KB | 10 Hz Ringpuffer | FreeRTOS RingBuffer | 4-Bit SDIO Blackbox-Logging mit ECDSA SHA-256 Signatur. |
| **`onewire_task`** | ESP32-S3 Main (Core 0) | **5** | 2 KB | 0,5 Hz zyklisch | Bit-Banging Driver | Pollt 1-Wire UIDs an Pod 1 & 2 (CH32V003 Emulation oder DS2401). |
| **`webdav_sync_task`**| ESP32-S3 Main (Core 0) | **3** | 8 KB | Nachlauf (Graceful)| LwIP TLS 1.3 | Automatischer GPX-Upload im Heim-WLAN bei Zündung AUS. |
| **`rear_nmea_task`** | RP2040 (Core 0) | **High**| 2 KB | 10 Hz DMA | UART0 (460.8k Baud) | High-Speed UBX/NMEA Parsing & 1-PPS Timecode Capture. |
| **`rear_lora_task`** | RP2040 (Core 1) | **High**| 2 KB | SX1262 IRQ | SPI0 Bus | 868 MHz LoRa Mesh Paketierung & Notfall-Sprachtunnel. |
| **`front_ptt_task`** | ESP32-S3 Front (Core 0)| **24** | 2 KB | GPIO Edge ISR | ESP-NOW TX Queue | Überträgt Lenker-PTT: 1x kurz = Funk-PTT via ESP-NOW in $< 0{,}9\,\text{ms}$; 2x kurz = Action-Cam Toggle; 1x lang = HiLight Tag. |
| **`front_mems_task`** | ESP32-S3 Front (Core 1)| **18** | 4 KB | 48 kHz DMA | Vector-DSP Filter | Knowles SPH0645 Digitalmikrofon A-Weighting & RMS-Pegel via Xtensa DSP. |
| **`front_cam_ble_task`**| ESP32-S3 Front (Core 0)| **12** | 4 KB | Event / KL15 ISR | NimBLE Client | Steuert GoPro / Insta360 / DJI per BLE; führt bei Zündungsaus sofortigen Auto-Stop aus. |
| **`front_pwr_task`** | ESP32-S3 Front (Core 0)| **10** | 2 KB | 10 Hz Timer | GPIO Lastschalter | TPS2051B Kaltstart (2,5s), Not-Power-Gating & Auto-Off Countdown. |
| **`front_can_task`** | ESP32-S3 Front (Core 0)| **16** | 4 KB | TWAI Interrupt | CAN Message Queue | Liest Lenker-Joysticks, Quellengating & Auto-Term CPC1017N. |

---

## 7. LittleFS Kassetten-Profil-Engine & JSON-Datenstruktur

Wird eine Kassette eingesteckt, liest der 1-Wire Treiber die 64-Bit-UID aus und lädt die zugehörige Konfigurationsdatei aus der LittleFS-Partition `/storage/profiles/<UID>.json`:

```json
{
  "profile_schema": 2,
  "uid": "01:A4:7B:3F:00:00:00:1E",
  "device_name": "Sena 50S Mesh 2.0 Inlay",
  "hardware_class": "K1",
  "power": {
    "vcc_enabled": true,
    "vcc_voltage_mv": 5000,
    "max_current_ma": 300,
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
    "mode": "sena_mesh_button",
    "pulse_click_ms": 200,
    "pulse_channel_ms": 1000
  },
  "mesh_routing": {
    "dle_bonus_points": 60,
    "protocol_family": "sena_wave_3"
  }
}
```

* **Zero-Trust Fallback (`disabled.json`):** Bei unbekannter UID, Kurzschluss oder leerem Schacht bleibt der 5V MOSFET gesperrt (`vcc_enabled: false`), der Codec wird auf `-96 dB` gedämpft und der DLE-Score auf `0` gesetzt.
