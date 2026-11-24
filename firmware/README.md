# OpenMotorBridge - Firmware Developer & Build Guide (v10.0 Architecture / ESP-IDF v6.1.1)

Dieses Dokument ist die verbindliche Referenz für Software-Entwickler zum Einrichten der Build-Umgebung, Kompilieren, Partitionieren und zentralen Flashen (Zero-Disassembly Bus-DFU) aller Firmware-Ziele der **OpenMotorBridge v10.0 Hardware-Architektur**.

---

## 1. Übersicht der Firmware-Ziele & Verbindliche Target-Matrix

In OpenMotorBridge v10.0 sind alle Knoten im Fahrzeug über den **geschirmten 4-Draht USB 2.0 + 12V/5V Automotive-Backbone** (`USB2517I-JZX` 7-Port Hub auf `PCBA 01`) miteinander vernetzt. Das frühere 6.5-GHz-UWB-Backbone (`DW3110`) sowie alle dedizierten UART-Flash-Header (`J_PROG`) auf den Satelliten-Platinen sind in v10.0 vollständig entfallen.

| Target-Verzeichnis | Physischer SoC / Modul (KiCad / BOM) | ESP-IDF Build-Target (`CONFIG_IDF_TARGET`) | Hardware-Baugruppe | Flash / RAM | Hauptaufgaben in v10.0 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`main_controller`](file:///Users/schmidtm/openMotorBridge/firmware/main_controller) | `ESP32-S31-WROOM-1U` (320 MHz Dual-Core RISC-V, BT Classic + BLE 5.4) | `esp32s31` | Zentralbox (`PCBA 01`) | 8/16 MB Flash, 8 MB Octal PSRAM | USB-Backbone Root-Host (`USB2517I`), Quad-eFuse Power-Sequencer (`GPIO 13..16`), Zentraler Bus-DFU-Flasher (`0x50`/`0x51`), Audio-DSP (`ES8388` + 3x `QCC3086`), `SX1262` LoRa (`GPIO 9..12`), CAN-FD (`SN65HVD230`), Action-Cam BLE-Client, 4-Bit SDIO Blackbox (`GPIO 33..39`) |
| [`front_node`](file:///Users/schmidtm/openMotorBridge/firmware/front_node) | `ESP32-S31-WROOM-1U` + `ESP32-E22` (Wi-Fi 6E Companion via SDIO 3.0) | `esp32s31` | Universal Front-Node (`PCBA 05` + `05C`/`05D`) | 8/16 MB Flash, 8 MB Octal PSRAM | 480 Mbps nativer USB-Backbone Node, Dual Under-Perch Cockpit OLEDs (`SSD1306` 128×32 via I2C `0x3C`), 6× Lenkertaster (`PCBA 05C`), Sensor-Puck (`PCBA 05D`: `SAM-M10Q` GNSS, `TMP117`, `OPT3001`, `SPH0645` I2S), `FSC-BT802` Infotainment Bridge, Handschuhfach-Schnelllader (`SW3526` 30W USB-PD & 15W Qi-Puck) |
| [`front_node_c3`](file:///Users/schmidtm/openMotorBridge/firmware/front_node_c3) | `ESP32-C3FH4` (RISC-V) | `esp32c3` | Infotainment Audio Bridge (`PCBA 05` `U10`) | 4 MB Flash, 400 KB SRAM | USB Audio Class (UAC) Headunit-Device für Boom! Box / SkylineOS, WHIM-Emulation, I2S Audio Bridge zu U1, Mux-Umschaltung |
| [`smart_cartridge`](file:///Users/schmidtm/openMotorBridge/firmware/smart_cartridge) | `ESP32-C6-MINI-1U` (RISC-V) | `esp32c6` | Satelliten-Pod Interface (`PCBA 03`) | 4 MB Flash, 512 KB SRAM | Nativer USB 2.0 Bus-Node (`GPIO 12/13`), `ES8388` Audio-Codec, `OMM_DETECT` Auto-Sense (`GPIO 14` -> `TS5A3159DBVR` `GPIO 15`), 4× `AO3400A` Kaltstart-Aktuatortreiber (`GPIO 4/5/6/7`), `SW3516` 30W USB-PD |
| [`radar_submcu`](file:///Users/schmidtm/openMotorBridge/firmware/radar_submcu) | `ESP32-C5-WROOM-1U` (Dual-Band 2.4 & 5 GHz RISC-V) | `esp32c5` | Heck-Radar & V2X Node (`PCBA 08`) | 4 MB Flash, 512 KB SRAM | Nativer USB 2.0 Bus-Node (`GPIO 18/19`), 77 GHz MR20 mmWave UART-Parser (`GPIO 3/4`), 5.9 GHz ETSI ITS-G5 802.11p OCB V2X C-ITS Parser (`0x32`), 36× `WS2812B` Halo-Wings (`GPIO 8`) |
| [`omm_module`](file:///Users/schmidtm/openMotorBridge/firmware/omm_module) | `ESP32-C6-MINI-1U` (RISC-V) | `esp32c6` | OMM 2.4 GHz / Unified UCS (`PCBA 09/10`) | 4 MB Flash, 512 KB SRAM | Nativer USB 2.0 Audio/CDC Node (`GPIO 12/13`), `SX1262` 868 MHz LoRa + `SA868S` UHF + 2.4 GHz Mesh, `ES8388` 48 kHz Audio (`GPIO 6/7`, I2S `GPIO 4/5/8/9`) |
| [`omm446_module`](file:///Users/schmidtm/openMotorBridge/firmware/omm446_module) | `ESP32-C6-MINI-1U` (RISC-V) | `esp32c6` | OMM 446 MHz PMR/DMR Profil (`PCBA 10`) | 4 MB Flash, 512 KB SRAM | Dediziertes PMR446 / DMR Tier I/II Profil für die Unified Tri-Band UCS Hardware (`PCBA 10`) mit `SA868S`/`SA818` UART-Steuerung (`GPIO 20/21`, PTT `GPIO 10`, PD `GPIO 11`) |
| [`smart_keyfob`](file:///Users/schmidtm/openMotorBridge/firmware/smart_keyfob) | `ESP32-C6` / Nordic `nRF52840` | Zephyr / C6 | 2-in-1 LoRa Smart-Keyfob (`PCBA 07`) | 4 MB / 1 MB Flash | BLE 5.4 Proximity Key, `SX1262` 868 MHz Bi-Direktionaler Alarm-Pager, Piezo/LRA Haptik, `BQ25120A` Qi-Lademanagement |

> [!NOTE]
> **Front-Node Target-Architektur:** Die Produktions-Hardware (`PCBA 05`) setzt auf den `ESP32-S31-WROOM-1U` (Dual-Core 320 MHz RISC-V SoC mit nativem 480 Mbps High-Speed USB PHY) mit externem `ESP32-E22` Wi-Fi 6E (5/6 GHz 2x2 MIMO via 4-Bit SDIO 3.0). Das interne 2.4 GHz Funkteil des S31 ist per Software (`front_node_config.h`) deaktiviert, um den Lenkerbereich funktechnisch zu entlasten und Kollisionen mit dem 5/6-GHz-Stream des E22 zu verhindern.

---

## 2. Voraussetzungen & Automatisierter Build

### 2.1 One-Command Komplett-Build (Alle 8 ESP-IDF Targets)

Das Repository enthält ein vollautomatisches Build-Skript ([`tools/build_firmware.sh`](file:///Users/schmidtm/openMotorBridge/tools/build_firmware.sh) bzw. [`firmware/build.sh`](file:///Users/schmidtm/openMotorBridge/firmware/build.sh)), das via [`tools/esp_env.sh`](file:///Users/schmidtm/openMotorBridge/tools/esp_env.sh) automatisch ESP-IDF (`~/esp-idf/export.sh`), CMake und Ninja lädt und das korrekte `IDF_TARGET` (`esp32s31`, `esp32c6`, `esp32c5`, `esp32c3`) für jedes Verzeichnis setzt:

```bash
# Alle 8 ESP-IDF Targets nacheinander kompilieren und verifizieren:
./firmware/build.sh all

# Einzelnes Target kompilieren:
./firmware/build.sh main_controller
./firmware/build.sh front_node
./firmware/build.sh front_node_c3
./firmware/build.sh smart_cartridge
./firmware/build.sh radar_submcu
./firmware/build.sh omm_module
./firmware/build.sh omm446_module
./firmware/build.sh smart_keyfob
```

---

## 3. Partition Table & Storage-Architektur

### 3.1 Hauptcontroller (`firmware/main_controller/partitions.csv` — 8 MB / 16 MB Flash)

```csv
# Name,   Type, SubType, Offset,   Size,     Flags
nvs,      data, nvs,     0x9000,   0x6000,
otadata,  data, ota,     0xf000,   0x2000,
phy_init, data, phy,     0x11000,  0x1000,
ota_0,    app,  ota_0,   0x20000,  0x2E0000,
ota_1,    app,  ota_1,   0x300000, 0x2E0000,
storage,  data, spiffs,  0x5E0000, 0x200000,
```

### 3.2 Front-Node (`firmware/front_node/partitions.csv` — 4 MB / 8 MB Flash)

```csv
# Name,   Type, SubType, Offset,  Size,     Flags
nvs,      data, nvs,     0x9000,  0x4000,
otadata,  data, ota,     0xd000,  0x2000,
phy_init, data, phy,     0xf000,  0x1000,
ota_0,    app,  ota_0,   0x10000, 0x1B0000,
ota_1,    app,  ota_1,   0x1C0000,0x1B0000,
storage,  data, spiffs,  0x370000,0x80000,
```

### 3.3 Dateisystem-Image (`data_image.bin`) erzeugen und flashen

Um die Fahrzeugprofile (`firmware/main_controller/data/can_profiles/`) in ein SPIFFS-Image zu packen und in die `storage`-Partition der Zentralbox (`0x5E0000`) zu schreiben:

```bash
# 1. SPIFFS-Image (2 MB = 0x200000) aus den Controller-Daten (can_profiles & profiles) generieren:
python3 $IDF_PATH/components/spiffs/spiffsgen.py 0x200000 firmware/main_controller/data build/data_image.bin

# 2. Image in die storage-Partition (Offset 0x5E0000) flashen:
esptool.py --chip esp32s3 -p /dev/cu.usbmodem1101 write_flash 0x5E0000 build/data_image.bin
```

---

## 4. Zentrales Flashen über den Fahrzeug-Bus (Zero-Disassembly Bus-DFU)

In v10.0 besitzt **nur die Zentralbox (`PCBA 01`)** einen von außen zugänglichen USB-C Service-Port (`J3`, abgesichert über die 5V Ideal-Diode `D3` `LM66100` und `U10` `USBLC6-2SC6`). Alle Satelliten-Knoten (`PCBA 03`, `PCBA 05`, `PCBA 08`, `PCBA 09/10`) hängen mit ihren nativen USB-D+/D--Leitungen (`GPIO 12/13` bzw. `GPIO 19/20`) direkt am internen 7-Port USB 2.0 Automotive-Hub (`U9` `USB2517I-JZX`) der Zentralbox.

### 4.1 Flashen der Zentralbox (`PCBA 01`) über USB-C Service-Port `J3`
Bei angestecktem USB-C-Kabel an `J3` wird die 5V/3.3V-Logik der Zentralbox über `D3` (`LM66100`) direkt vom Laptop gespeist (auch ohne 12V-Bordspannung). Dies reicht für das Flashen, Debuggen und Kalibrieren der Zentralbox (`PCBA 01`) vollständig aus:

```bash
./firmware/build.sh main_controller flash monitor -p /dev/cu.usbmodem1101
```

### 4.2 Flashen aller Satelliten-Knoten (`PCBA 03`, `05`, `08`, `09/10`) über die Zentralbox
Kein einziges Satelliten-Gehäuse muss zum Flashen geöffnet werden (`Zero-Disassembly Bus-DFU`).

> [!IMPORTANT]
> **Spannungsversorgung für Bus-DFU der Satelliten:** Der Quad-Automotive-Smart-Switch `U12` (`TPS4H160-Q1`), welcher die 12V-Bus-Zweige zu den Satelliten an `J6` schaltet, wird direkt aus `KL30_IN` (12V) gespeist. Im reinen 5V-USB-C-Betrieb an `J3` sind die Satelliten an `J6` daher stromlos. Für das Flashen der Satelliten über den Bus muss daher **12V an `J1` (DTM-6)** anliegen (oder der jeweilige Satellit auf der Werkbank lokal versorgt werden).

1. **Reguläres Bus-DFU (`USB_PKT_DFU_ENTER = 0x50` / `USB_PKT_DFU_CHUNK = 0x51`):**
   - [`omm_flasher.cpp`](file:///Users/schmidtm/openMotorBridge/firmware/main_controller/src/omm_flasher.cpp) auf der Zentralbox versetzt den Zielknoten per signiertem USB-Backbone-Befehl `0x50` in den DFU-Empfangsmodus, überträgt das Firmware-Image in 1024-Byte-Blöcken (`0x51` mit CRC32) mit 420 KB/s in dessen `ota_1`-Partition und löst nach erfolgreicher SHA-256-Prüfung den Reboot aus.
2. **Hardware-Unbricking (Power-Cycle Recovery):**
   - Reagiert ein Knoten nicht mehr auf Software-Befehle, schaltet die Zentralbox den jeweiligen Zweig über den Quad-Smart-Switch `U12` (`TPS4H160-Q1` auf `GPIO 13..16`) kurzzeitig stromlos (`250 ms`) und fängt das USB-Serial/JTAG-ROM-Bootloader-Fenster des Ziel-ESP32 direkt auf dem USB-Hub (`U9`) ab.
