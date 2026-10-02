# OpenMotorBridge - Firmware Developer & Build Guide (ESP-IDF v5.2 / v5.3)

Dieses Dokument ist die verbindliche Schritt-für-Schritt-Anleitung für Software-Entwickler und Nachbauer zum Einrichten der Build-Umgebung, Kompilieren, Partitionieren und Flashen der drei Firmware-Ziele von OpenMotorBridge.

---

## 1. Übersicht der Firmware-Ziele (Targets)

Das OpenMotorBridge-Gesamtsystem verteilt die Aufgaben auf drei dedizierte Mikrocontroller-Baugruppen:

```
+---------------------------------------------------------------------------------------------------+
| OPENMOTORBRIDGE FIRMWARE TARGET MATRIX                                                            |
+-------------------+---------+-----------------------+-------------+-------------------------------+
| Target-Verzeichnis| MCU     | Hardware-Baugruppe    | Takt / RAM  | Hauptaufgaben                 |
+-------------------+---------+-----------------------+-------------+-------------------------------+
| `main_controller` | ESP32-S3| Zentralbox (PCBA 01)  | 240 MHz     | * Audio-DSP Matrix & EKF      |
|                   | N16R8   | Batteriefach          | 8 MB OPI RAM| * CAN-Bus & Fahrzeugprofile   |
|                   |         |                       | 16 MB Flash | * UWB Backbone Hub & LoRa SX  |
+-------------------+---------+-----------------------+-------------+-------------------------------+
| `front_node`      | ESP32-S3| Front-Knoten (PCBA 05)| 240 MHz     | * GNSS SAM-M10Q & Sensorik    |
|                   | N16R8   | Cockpit / Verkleidung | 8 MB OPI RAM| * Knowles I2S Wind-AGC        |
|                   |         |                       | 16 MB Flash | * USB-PD / Ottocast Steuerung |
+-------------------+---------+-----------------------+-------------+-------------------------------+
| `smart_cartridge` | ESP32-C6| Smart Cartridge (03)  | 160 MHz     | * 4x AO3400A Mechatronik Gate |
|                   | RISC-V  | Bucht 1 & Bucht 2     | 512 KB SRAM | * ES8388 I2S Codec Streaming  |
|                   |         |                       | 4 MB Flash  | * All-UWB Backbone Node       |
+-------------------+---------+-----------------------+-------------+-------------------------------+
| `radar_submcu`    | ESP32-C5| Heck-Radar (PCBA 08)  | 160 MHz     | * Wheeltec MR20 mmWave Parser |
|                   | / C6    | Kennzeichenträger     | 512 KB SRAM | * 36x Halo RGB LED Animation  |
|                   |         |                       | 4 MB Flash  | * UWB Ziel-Telemetrie Stream  |
+-------------------+---------+-----------------------+-------------+-------------------------------+
```

---

## 2. Voraussetzungen & Toolchain-Installation

### 2.1 Systemanforderungen
* **Betriebssystem:** Linux (Ubuntu 22.04 / 24.04), macOS (Apple Silicon / Intel) oder Windows 11 (WSL2 empfohlen).
* **Python:** Python 3.10 oder neuer mit `pip` und `virtualenv`.
* **Build-Tools:** CMake >= 3.16, Ninja-Build, Git.

### 2.2 ESP-IDF v5.2 / v5.3 installieren

```bash
# 1. Arbeitsverzeichnis für ESP-IDF anlegen
mkdir -p ~/esp && cd ~/esp

# 2. ESP-IDF Repository klonen (Release v5.2 oder v5.3 LTS)
git clone -b v5.2.2 --recursive https://github.com/espressif/esp-idf.git esp-idf-v5.2

# 3. Toolchains für ESP32-S3 und ESP32-C6 / ESP32-C5 installieren
cd ~/esp/esp-idf-v5.2
./install.sh esp32s3,esp32c6,esp32c5

# 4. Umgebungsvariablen in die aktuelle Shell laden
. ./export.sh
```

> [!TIP]
> Um ESP-IDF dauerhaft bequem verfügbar zu machen, empfiehlt sich ein Alias in `~/.zshrc` oder `~/.bashrc`:
> ```bash
> alias get_idf='. $HOME/esp/esp-idf-v5.2/export.sh'
> ```

---

## 3. Kompilieren der 3 Targets

Klonen Sie das OpenMotorBridge-Repository oder wechseln Sie in das Hauptverzeichnis:

```bash
cd /path/to/openMotorBridge/firmware
```

### 3.1 Target 1: Hauptcontroller (`main_controller`)

```bash
cd main_controller

# Ziel-Architektur festlegen
idf.py set-target esp32s3

# (Optional) Menü-Konfiguration inspizieren
idf.py menuconfig

# Kompilieren
idf.py build
```

Das erzeugt:
* `build/bootloader/bootloader.bin`
* `build/partition_table/partition-table.bin`
* `build/openmotorbridge_main.bin`

### 3.2 Target 2: Front-Knoten (`front_node`)

```bash
cd ../front_node

# Ziel-Architektur festlegen
idf.py set-target esp32s3

# Kompilieren
idf.py build
```

Das erzeugt:
* `build/bootloader/bootloader.bin`
* `build/partition_table/partition-table.bin`
* `build/openmotorbridge_front_node.bin`

### 3.3 Target 3: Smart Cartridge (`smart_cartridge`)

```bash
cd ../smart_cartridge

# Ziel-Architektur festlegen (ESP32-C6 RISC-V)
idf.py set-target esp32c6

# Kompilieren
idf.py build
```

Das erzeugt:
* `build/openmotorbridge_smart_cartridge.bin`

### 3.4 Target 4: Radar Sub-MCU (`radar_submcu`)

```bash
cd ../radar_submcu

# Ziel-Architektur festlegen (ESP32-C6 oder ESP32-C5)
idf.py set-target esp32c6

# Kompilieren
idf.py build
```

Das erzeugt:
* `build/openmotorbridge_radar2_submcu.bin`

---

## 4. Partition Table & Storage-Architektur

Alle Targets nutzen eine fehlertolerante Dual-Bank A/B OTA-Partitionierung mit automatischem Rollback-Schutz.

### 4.1 Partitions-Layout (`partitions.csv`)

```csv
# Name,   Type, SubType, Offset,   Size,     Flags
nvs,      data, nvs,     0x9000,   0x4000,
otadata,  data, ota,     0xd000,   0x2000,
phy_init, data, phy,     0xf000,   0x1000,
ota_0,    app,  ota_0,   0x10000,  0x300000,
ota_1,    app,  ota_1,   0x310000, 0x300000,
storage,  data, spiffs,  0x610000, 0x1E0000,
```

* **`nvs` (16 KB):** Speichert kryptografische Schlüssel (AES-128-GCM Gruppen-Session-Keys), Kalibrierdaten der IMU und das zuletzt aktive CAN-Fahrzeugprofil.
* **`otadata` (8 KB):** Verwaltet die aktive Boot-Partition und Rollback-Zähler (anti-bricking).
* **`ota_0` / `ota_1` (je 3 MB):** Dual-Bank Firmware-Partitionen. Updates werden in die inaktive Bank geflasht; bootet diese nicht erfolgreich innerhalb von 30 s, schlägt der Bootloader automatisch auf die vorherige Version zurück.
* **`storage` (LittleFS / SPIFFS):** Enthält CAN-Bus DBC/JSON-Fahrzeugprofile (`/can_profiles/bmw_k24.json`, `/can_profiles/harley_hdcan.json`) sowie Offline-Assets des PWA-Dashboards.

### 4.2 Dateisystem-Image erstellen und flashen

```bash
# LittleFS / SPIFFS Partition für Fahrzeugprofile erzeugen und flashen:
esptool.py --chip esp32s3 -p /dev/tty.usbmodem* write_flash 0x610000 data_image.bin
```

---

## 5. Flashen & Serieller Monitor

### 5.1 Direktes Flashen via USB-C

1. Verbinden Sie den USB-C Service-Port der Baugruppe mit dem PC.
2. Identifizieren Sie den seriellen Port:
   * **macOS:** `/dev/tty.usbmodem*`
   * **Linux:** `/dev/ttyACM0` oder `/dev/ttyUSB0`
   * **Windows:** `COM3`, `COM4`, etc.

```bash
# Flash und automatischer Start des seriellen Monitors
idf.py -p /dev/tty.usbmodem1101 flash monitor
```

### 5.2 Manuelles Bootstrapping (Bootloader-Recovery)
Sollte ein Modul nicht automatisch in den Bootloader wechseln:
1. Taste `BOOT` (oder `SW_PAIR_RESET`) gedrückt halten.
2. Taste `RESET` kurz drücken (oder Versorgungsspannung kurz trennen).
3. Taste `BOOT` loslassen.
4. Das Modul meldet sich im ROM-Bootloader-Modus (`waiting for download`).

### 5.3 Monitor beenden & Filter
* **Monitor beenden:** Tastenkombination `Ctrl + ]`.
* **Logging-Level zur Laufzeit filtern:**
  ```bash
  idf.py monitor --print-filter="*:I UWB:D CAN:D"
  ```

---

## 6. Häufige Fehler & Troubleshooting

1. **`PSRAM not detected` / Boot-Loop:**
   * Ursache: Falscher Octal-/Quad-SPI Modus in `sdkconfig`.
   * Lösung: `CONFIG_SPIRAM_MODE_OCT=y` für WROOM-1-N16R8 sicherstellen.
2. **`Flash size mismatch` (16 MB vs. 4 MB / 8 MB):**
   * Lösung: In `idf.py menuconfig` unter `Serial flasher config` -> `Flash size` exakt auf `16 MB` stellen.
3. **UWB SPI Transceiver Timeout:**
   * Prüfen, ob der SPI-Bus auf 20 MHz konfiguriert ist und der DW3110 Interrupt-Pin (`DW_IRQ`) GPIO-Konflikte aufweist.
