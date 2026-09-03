# 09 - Firmware-Architektur, FreeRTOS Tasks & Rollback-OTA

Dieses Dokument spezifiziert die systemweite Firmware-Architektur der OpenMotorBridge v8.0: die Multi-Core-Aufteilung des ESP32-S3 Hauptcontrollers, die Coprozessoren (RP2040 im Heck-Pod 3 und ESP32-C3 im Front-Knoten), das **ESP-NOW Low-Latency-Protokoll (< 1,8 ms)**, die LittleFS-Profil-Engine sowie die **Dual-Bank Rollback-OTA-Architektur** gegen Stromausfälle während des Flashvorgangs.

---

## 1. Multi-Core & Multi-MCU Systemarchitektur

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        DIE 3 FIRMWARE-KONTROLLER IM VERBUND                            │
├──────────────────────────────────────┬─────────────────────────┬───────────────────────┤
│ 1. ZENTRALBOX (ESP32-S3 Dual-Core)   │ 2. REAR POD 3 (RP2040)  │ 3. FRONT-NODE (ESP-C3)│
├──────────────────────────────────────┼─────────────────────────┼───────────────────────┤
│ • Core 0: BLE, WebDAV, SDIO, ESP-NOW │ • Core 0: NMEA/UBX 10Hz │ • FreeRTOS Single-Core│
│ • Core 1: Echtzeit 48kHz Audio-DSP   │ • Core 1: LoRa SX1262   │ • I2S MEMS Filter     │
│ • LittleFS Kassetten-Profile Engine  │ • 1-PPS Timecode Sync   │ • VBUS Lastschalter   │
└──────────────────────────────────────┴─────────────────────────┴───────────────────────┘
```

### 1.1 Core-Aufteilung des ESP32-S3 Hauptcontrollers (240 MHz)

#### CORE 0 (Kommunikation, Telemetrie & System):
- **BLE GATT Server:** Web-Bluetooth Anbindung für das PWA-Dashboard (`0x180D`, `0x180A`).
- **ESP-NOW Front-Node Client (`esp_now_front_node_client.cpp`):** Unterbrechungsfreier Empfang von Lenker-PTT-Events ($< 1{,}8\,\text{ms}$) und Knowles MEMS dB(A)-Schallpegelwerten.
- **Dual 1-Wire Kassetten-Manager:** Pollt zyklisch Port 1 & 2 auf DS2401 Silicon Serial ROM IDs und lädt dynamische LittleFS JSON-Profile.
- **Opto-Puls-Sequenzer:** TLP222A Tastensimulation für OEM Sena- / Cardo-Inlays.
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
2. **ESP32-C3 GPIO-Interrupt:** $35\,\mu\text{s}$ ISR-Verarbeitungszeit.
3. **ESP-NOW Funkübertragung (2.4 GHz):** $0{,}90\,\text{ms}$ Flugzeit (99,8 % PDR).
4. **Zentralbox ESP32-S3 Core 0 ISR:** $45\,\mu\text{s}$ Frame-Parsing & GPIO-Schaltung.
5. **Toshiba TLP222A Optokoppler:** $0{,}50\,\text{ms}$ Durchschaltzeit $t_{\text{ON}}$.
* **Gesamtlatenz:** **$1{,}74\,\text{ms}$** (Weit unterhalb des physiologischen Schwellwerts von $10\,\text{ms}$).

---

## 3. Dual-Bank Rollback-OTA Partitionierung

Um das Risiko eines "Bricking" bei Unterbrechung der Stromversorgung (z. B. versehentliches Ausschalten der Zündung während des Firmware-Updates) auf **0,0 %** zu reduzieren, sind alle Controller mit einer 2-Bank OTA-Partitionierung ausgestattet:

```csv
# Name,   Type, SubType, Offset,  Size, Flags
nvs,      data, nvs,     0x9000,  0x4000,
otadata,  data, ota,     0xd000,  0x2000,
phy_init, data, phy,     0xf000,  0x1000,
factory,  app,  factory, 0x10000, 0x180000,
ota_0,    app,  ota_0,   0x190000,0x140000,
ota_1,    app,  ota_1,   0x2d0000,0x140000,
storage,  data, littlefs,0x410000,0x3f0000,
```

### 3.1 Automatischer Rollback-Mechanismus
1. Neue Firmware wird blockweise in die inaktive Partition (`ota_1`) geschrieben und per SHA-256 verifiziert.
2. Der Boot-Pointer in `otadata` wird auf `ESP_OTA_IMG_NEW` gesetzt.
3. Nach dem Neustart führt die Firmware einen internen Selbsttest durch (I2C-Busse, Audio-Codec, Funkmodule).
4. Erst wenn der Test erfolgreich war, markiert die Firmware das Image als `ESP_OTA_IMG_VALID`.
5. Bricht die Stromversorgung vor Abschluss ab oder stürzt die neue Firmware ab, schaltet der Bootloader beim nächsten Start automatisch auf das bewährte Image `ota_0` zurück.

---

## 4. OMM In-System UART-Push-Flasher (`omm_flasher.cpp`)

Für Firmware-Updates des Heck-Pods 3 ohne Ausbau aus dem Fahrzeug:
* Die Zentralbox liest das Binär-Image `omm_rear.bin` und versetzt den RP2040/C3 über UART mit dem Steuerbefehl `0xAA 0x55 0xFE 0x01 "BOOT"` in den Download-Modus.
* Die Übertragung erfolgt mit $460{,}800\,\text{Baud}$ in 1024-Byte-Blöcken ($< 6\,\text{s}$ Gesamtdauer).

---

## 5. TLP222A Optokoppler-Pulssynthese & Tastensimulation

Tastendrücke werden hardwaregenau und mikrocontrollergesteuert synthetisiert, um alle OEM-Headsets exakt nach Herstellerspezifikation zu bedienen:

| Tastenbefehl / Geste | Pulsdauer ($t_{\text{ON}}$) | Pausenzeit ($t_{\text{OFF}}$) | Funktion & Headset-Reaktion |
| :--- | :---: | :---: | :--- |
| **Single Click (Mesh On/Off)** | $200\,\text{ms}$ | $> 300\,\text{ms}$ | Schaltet Open Mesh oder DMC-Gruppenfunk ein/aus (Sena Mesh-Taste, Cardo Intercom). |
| **Double Click (Radio / Pair)** | 2x $150\,\text{ms}$ | $150\,\text{ms}$ | Startet UKW-Radio oder wechselt zwischen Musik und Sprechfunk. |
| **Channel Next (Kanalwechsel)** | $1000\,\text{ms}$ | $> 500\,\text{ms}$ | Schaltet im Sena Open Mesh auf den nächsten Funkkanal (Kanal 1 bis 9). |
| **Long Press (Power Toggle)** | $3500\,\text{ms}$ | $> 1000\,\text{ms}$ | Schaltet das Headset vollständig ein oder aus. |
| **Mute Toggle (Stummschaltung)** | $500\,\text{ms}$ | $> 300\,\text{ms}$ | Schaltet das eigene Mikrofon vorübergehend stumm. |

---

## 6. FreeRTOS Task-Architektur & Scheduling-Matrix (Alle 3 MCUs)

Das Gesamtsystem orchestriert 14 spezialisierte Tasks über 3 physikalisch getrennte Mikrocontroller mit festen Prioritäten und Kernzuweisungen:

| Task-Name | MCU / Kern | Prio | Stack | Auslöser / Rate | IPC / Schnittstelle | Aufgabe & Funktion |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **`audio_dsp_task`** | ESP32-S3 (Core 1) | **24** | 8 KB | 48 kHz DMA ISR | FreeRTOS StreamBuffer | Latenzfreier I2S Audio-Mix, Raised-Cosine Ducking & AGC. |
| **`esp_now_rx_task`** | ESP32-S3 (Core 0) | **22** | 4 KB | Event-Queue | Direct-to-Task Notify | Verarbeitet Front-Node PTT-Events ($< 1{,}8\,\text{ms}$) & Windpegel. |
| **`opto_seq_task`** | ESP32-S3 (Core 0) | **18** | 2 KB | Event-Queue | FreeRTOS Queue | Taktet prellfreie Pulse an Toshiba TLP222A PhotoMOS Relais. |
| **`radar_proc_task`** | ESP32-S3 (Core 0) | **16** | 4 KB | 20 Hz UART2 ISR | FreeRTOS Queue / UART | Garmin Varia / mmWave Parsing, TTC-Berechnung & Prio-1 Ducking. |
| **`adr_ekf_task`** | ESP32-S3 (Core 0) | **15** | 4 KB | 50 Hz Timer | I2C / CAN-Puffer | 15-State Kalman-Filter (GNSS + IMU + Raddrehzahl). |
| **`ble_server_task`** | ESP32-S3 (Core 0) | **10** | 4 KB | Event-Driven | NimBLE Stack | Web-Bluetooth PWA Dashboard (GATT Services `0x180D`/`0x180A`). |
| **`sdio_log_task`** | ESP32-S3 (Core 0) | **8** | 8 KB | 10 Hz Ringpuffer | FreeRTOS RingBuffer | 4-Bit SDIO Blackbox-Logging mit ECDSA SHA-256 Signatur. |
| **`onewire_task`** | ESP32-S3 (Core 0) | **5** | 2 KB | 0,5 Hz zyklisch | Bit-Banging Driver | Pollt DS2401 Silicon Serial ROM IDs an Pod 1 & 2. |
| **`webdav_sync_task`**| ESP32-S3 (Core 0) | **3** | 8 KB | Nachlauf (Graceful)| LwIP TLS 1.3 | Automatischer GPX-Upload im Heim-WLAN bei Zündung AUS. |
| **`rear_nmea_task`** | RP2040 (Core 0) | **High**| 2 KB | 10 Hz DMA | UART0 (460.8k Baud) | High-Speed UBX/NMEA Parsing & 1-PPS Timecode Capture. |
| **`rear_lora_task`** | RP2040 (Core 1) | **High**| 2 KB | SX1262 IRQ | SPI0 Bus | 868 MHz LoRa Mesh Paketierung & Notfall-Sprachtunnel. |
| **`front_ptt_task`** | ESP32-C3 | **24** | 2 KB | GPIO 0 Edge ISR | ESP-NOW TX Queue | Überträgt Lenker-PTT Schließvorgänge in unter $0{,}9\,\text{ms}$. |
| **`front_mems_task`** | ESP32-C3 | **18** | 4 KB | 48 kHz DMA | Biquad Filter | Knowles SPH0645 Digitalmikrofon A-Weighting & RMS-Pegel. |
| **`front_pwr_task`** | ESP32-C3 | **10** | 2 KB | 10 Hz Timer | GPIO Lastschalter | TPS2051B 1-Klick Kaltstart (2,5s) & Auto-Café 60s Countdown. |

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
