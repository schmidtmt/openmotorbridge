# OpenMotorBridge - PCBA 07 Smart Keyfob & Silent Pager Firmware

Dieses Verzeichnis enthält die Firmware für den **2-in-1 LoRa Smart-Keyfob & Silent Pager** ([PCBA 07](../../docs/de/07_pcba_hardware_pinouts.md#7-pcba-07-2-in-1-lora-smart-keyfob--silent-pager)).

---

## 1. Übersicht & Hardware-Architektur

Der Smart-Keyfob kombiniert Nahbereichs-Fernbedienung (BLE 5.4) und Weitbereichs-Alarmierung (SX1262 LoRa 868 MHz bis 4,5 km) in einem ultrakompakten Schlüsselanhänger ($38{,}0 \times 19{,}0 \times 1{,}0\,\text{mm}$):

* **MCU:** Nordic Semiconductor `nRF52840-QIAA` (ARM Cortex-M4F @ 64 MHz, 1 MB Flash, 256 KB RAM).
* **LoRa:** Semtech `SX1262` (868.5 MHz Kanal 3, empfängt Diebstahl-/Erschütterungsalarme bis zu 4,5 km Reichweite).
* **Haptik:** Texas Instruments `DRV2605L` Haptiktreiber & Vybronics 10x3.6mm LRA Linearmotor (spürbarer Vibrationsalarm in der Tasche).
* **Akustik:** Murata SMD Piezo-Buzzer `CPT-9019S` (2,7 kHz Bestätigungs-Chirps, 4,0 kHz Alarmsirene).
* **Optik:** `WS2812B-2020` Smart RGB-LED (Grün/Cyan = Scharf, Rot Strobe = Alarm, Gelb = Qi-Laden).
* **Laden:** TI `BQ51003` Qi-Empfänger & TI `BQ25100` LiPo-Lademanager (100 % lötfreier 2-Pin JST-ACH Akku- & Spulenanschluss).
* **Ruhestrom:** $< 25\,\mu\text{A}$ im System ON Standby (Monatelange Laufzeit mit 200 mAh LiPo).

---

## 2. Vollständige Pinbelegung (Nordic nRF52840 AQFN-73)

| Pad | Signalname | Zephyr Pin | Richtung | Funktion / Peripherie |
| :---: | :--- | :---: | :---: | :--- |
| **G1** | `BTN_ARM_N` | `P0.08` | Digital In | Scharfschalt-Taster SW1 (Active-LOW, 10k Pull-Up R1) |
| **J1** | `BTN_SOS_N` | `P0.07` | Digital In | SOS / Paniktaster SW2 (Active-LOW, 10k Pull-Up R2) |
| **K2** | `CHG_STAT` | `P0.05` | Digital In | BQ25100 Ladeanzeige (LOW = Qi-Laden aktiv) |
| **M2** | `DRV_EN` | `P0.03` | Digital Out | Hardware-Enable für TI DRV2605L Haptiktreiber |
| **N1** | `I2C_SDA` | `P0.02` | Open-Drain | I2C SDA zu DRV2605L (Adresse `0x5A`) |
| **P2** | `I2C_SCL` | `P0.28` | Open-Drain | I2C SCL zu DRV2605L |
| **F2** | `BUZZER_PWM` | `P0.06` | Digital Out | PWM-Tonsignal für Piezo-Buzzer LS1 |
| **L1** | `LED_DATA` | `P0.04` | Digital Out | 800 kHz Datenstrom für WS2812B Smart-LED D1 |
| **C1** | `LORA_SCK` | `P0.26` | Digital Out | SPI SCK zu Semtech SX1262 LoRa |
| **R1** | `LORA_NSS` | `P0.29` | Digital Out | SPI Chip-Select (Active-LOW) zu SX1262 |
| **T2** | `LORA_MOSI` | `P0.30` | Digital Out | SPI MOSI zu SX1262 |
| **U1** | `LORA_MISO` | `P0.31` | Digital In | SPI MISO von SX1262 |
| **W1** | `LORA_BUSY` | `P1.09` | Digital In | Busy-Leitung von SX1262 |
| **D2** | `LORA_DIO1` | `P0.27` | Digital In | IRQ Interrupt von SX1262 (Empfang 0xFE Alarmframe) |
| **Y2** | `LORA_RESET`| `P0.24` | Digital Out | Hardware-Reset zu SX1262 |
| **H2** | `SWDCLK` | SWD | Digital In | SWD Programmiertakt (`J_SWD.2`) |
| **AC24**| `SWDIO` | SWD | Bi-Dir | SWD Programmierdaten (`J_SWD.3`) |
| **A8** | `BLE_ANT_50R`| RF | RF 50R | 2.4 GHz Antennenleitung zur Johanson 2450AT Chipantenne |
| **A12/14**| `XTAL1/2` | Analog | Analog | 32.000 MHz HF-Präzisionsquarz |
| **F23/H23**| `RTC1/2` | Analog | Analog | 32.768 kHz Uhrenquarz |

---

## 3. Build & Kompilierung

Die Firmware basiert auf **Zephyr RTOS v3.5+** bzw. dem **Nordic nRF Connect SDK (NCS) v2.5+**:

### 3.1 Voraussetzungen
* [nRF Connect SDK](https://www.nordicsemi.com/Products/Development-software/nRF-Connect-SDK) oder Zephyr Toolchain installiert.
* `west` Build-Tool installiert (`pip install west`).
* ARM GCC Toolchain (`arm-none-eabi-gcc`).

### 3.2 Build ausführen

```bash
cd firmware/smart_keyfob

# Zephyr Build mit nRF52840 Target
west build -b nrf52840dk_nrf52840 -- -DEXTRA_DTC_OVERLAY_FILE=openmotorbridge_keyfob.overlay
```

Das erzeugt:
* `build/zephyr/zephyr.hex`
* `build/zephyr/zephyr.bin`

---

## 4. Flashen via SWD Header (`J_SWD`)

Der 4-polige SMD-Header `J_SWD` (1,27 mm Raster) auf der Unterseite der PCBA 07 führt:
* Pin 1: `VCC_3V3`
* Pin 2: `SWDCLK`
* Pin 3: `SWDIO`
* Pin 4: `GND`

### Flashen mit Segger J-Link:
```bash
nrfjprog --program build/zephyr/zephyr.hex --chiperase --reset
```

### Flashen mit OpenOCD & CMSIS-DAP / Raspberry Pi Debug Probe:
```bash
openocd -f interface/cmsis-dap.cfg -f target/nrf52.cfg -c "program build/zephyr/zephyr.hex verify reset exit"
```

---

## 5. Betriebsmodi & Benutzer-Feedback

| Zustand | Taster / Event | Haptik (LRA) | Akustik (Buzzer) | WS2812B RGB-LED | Funk-Aktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Scharfschalten** | SW1 kurz drücken | Doppel-Klick | 1x 2,7 kHz Chirp (80 ms) | Cyan pulsierend | BLE / LoRa Befehl `0x20` an Zentralbox |
| **Entschärfen** | SW1 kurz drücken | Einfacher Klick | 2x 2,4 kHz Chirp (60 ms) | Grün atmend | BLE / LoRa Befehl `0x21` an Zentralbox |
| **Bike-Alarm** | Empfang LoRa `0xFE` | Dauervibration | 2,7 / 4,0 kHz Sirene | Rot Strobe (10 Hz) | Pager vibriert in der Tasche |
| **Alarm quittieren**| Beliebiger Taster | Stoppt | Stoppt | Rückfall auf Scharf | Quittierungstelegramm gesendet |
| **SOS Notfall** | SW2 lang drücken | Dreifach-Alarm | Morse SOS (`... --- ...`) | Weiß / Rot Strobe | LoRa Notruf-Paket `0x05` gesendet |
| **Qi-Laden** | Auf Ladekissen | - | - | Gelb / Amber atmend | Akku lädt berührungslos |
