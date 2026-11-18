# OpenMotorBridge - PCBA 07 Smart Keyfob & Acoustic Pager Firmware

Dieses Verzeichnis enthält die Firmware für den **2-in-1 LoRa Smart-Keyfob & Acoustic Pager** ([PCBA 07](../../docs/de/07_pcba_hardware_pinouts.md#9-pcba-07-2-in-1-lora-smart-keyfob-openmotorbridge_smart_keyfob)).

---

## 1. Übersicht & Hardware-Architektur

Der Smart-Keyfob kombiniert Nahbereichs-Fernbedienung (BLE 5.0) und Weitbereichs-Alarmierung (SX1262 LoRa 868,5 MHz bis 4,5 km) in einem ultrakompakten Schlüsselanhänger ($38{,}0 \times 19{,}0 \times 1{,}0\,\text{mm}$, 4 Lagen FR-4 ENIG):

* **MCU:** Espressif `ESP32-C3FH4` (32-Bit RISC-V Single-Core @ 160 MHz, 4 MB embedded Flash, QFN-32 $5 \times 5\,\text{mm}$, internes LDO-Decoupling).
* **LoRa:** Semtech `SX1262` (868.5 MHz Kanal 3, empfängt Diebstahl-/Erschütterungsalarme bis zu 4,5 km Reichweite).
* **Akustik:** CUI Devices SMD Piezo-Buzzer `CPT-9019S-SMT` (`LS1`, 85 dBA @ 10 cm, 2,7 kHz Bestätigungs-Chirps, 4,0 kHz Alarmsirene).
* **Optik:** `WS2812B-2020` Smart RGB-LED (Grün = Standby, Cyan = Scharf, Rot Strobe = Alarm, Gelb = Qi-Laden, Weiß/Rot = SOS).
* **Laden:** Texas Instruments `BQ51050BRHLR` All-in-One 5W Qi-Wireless-Receiver & integrierter Li-Ion/LiPo-Direktlader (VQFN-20). Lädt die LiPo-Zelle direkt ohne Zwischenwandler.
* **Stromversorgung & Ruhestrom:** TI `TPS7A0233PDBVR` Ultra-Low-$I_q$ LDO ($I_q = 25\,\text{nA}$). ESP32-C3 Light-/Deep-Sleep mit sofortigem GPIO-Aufwecken über SW1, SW2, LoRa-IRQ oder Qi-Ladekontakt.

---

## 2. Vollständige Pinbelegung (ESP32-C3FH4 QFN-32)

| QFN-32 Pin | Signalname | ESP-IDF GPIO | Richtung | Funktion / Peripherie |
| :---: | :--- | :---: | :---: | :--- |
| **1** | `BLE_ANT_50R` | RF 2.4G | HF 50R | 50-Ohm-Leitung zur Johanson 2450AT Chipantenne (`ANT2`) |
| **2, 3** | `VCC_3V3` | Power | Power In | +3.3V VDD Hauptversorgung |
| **4** | `BAT_SENSE` | `GPIO 0` | Analog In | LiPo-Spannungsteiler (100k/100k, ADC1_CH0) |
| **5** | `LORA_DIO1` | `GPIO 1` | Digital In | IRQ Interrupt von SX1262 (Empfang 0xFE Alarmframe) |
| **6** | `LORA_MISO` | `GPIO 2` | Digital In | SPI Master-In Slave-Out von SX1262 (`U2`, FSPIQ) |
| **7** | `CHIP_EN` | CHIP_PU | Reset In | Chip Enable / Reset (10k Pullup an 3.3V, 100nF an GND) |
| **8** | `LORA_MOSI` | `GPIO 3` | Digital Out | SPI Master-Out Slave-In zu SX1262 (`U2`, FSPID) |
| **9** | `LORA_SCK` | `GPIO 4` | Digital Out | SPI Serial Clock zu SX1262 (`U2`, FSPIHD) |
| **10** | `LORA_NSS` | `GPIO 5` | Digital Out | SPI Chip-Select (Active-LOW) zu SX1262 (`U2`, FSPIWP) |
| **11** | `VCC_3V3` | Power | Power In | +3.3V RTC-Versorgung |
| **12** | `LORA_BUSY` | `GPIO 6` | Digital In | Busy-Statusleitung von SX1262 (`U2`, FSPICLK) |
| **13** | `LORA_RESET`| `GPIO 7` | Digital Out | Hardware-Resetleitung zu SX1262 (`U2`, FSPICS0) |
| **14** | `LED_DATA` | `GPIO 8` | Digital Out | 800 kHz Datenstrom für WS2812B RGB Status-LED (`D1`, Strapping) |
| **15** | `BTN_ARM_N` | `GPIO 9` | Digital In | Scharfschalt-Taster SW1 (Active-LOW, 10k Pullup R1, Strapping Boot) |
| **16** | `BTN_SOS_N` | `GPIO 10` | Digital In | SOS / Paniktaster SW2 (Active-LOW, 10k Pullup R2) |
| **17** | `VCC_3V3` | Power | Power In | +3.3V CPU-Core-Versorgung |
| **18–24** | `NC` | Intern | - | Interne SIP-Flash-Verbindungen (4 MB Flash) |
| **25** | `USB_DM` | `GPIO 18` | USB D- | Nativer USB CDC / JTAG D- Datenanschluss (`J2.2`) |
| **26** | `USB_DP` | `GPIO 19` | USB D+ | Nativer USB CDC / JTAG D+ Datenanschluss (`J2.3`) |
| **27** | `BUZZER_PWM`| `GPIO 20` | Digital Out | LEDC PWM-Tonsignal für CUI 9mm Piezo-Summer (`LS1`) |
| **28** | `CHG_STAT` | `GPIO 21` | Digital In | BQ51050B Ladeanzeige (Active-LOW: 0 = Qi-Laden aktiv) |
| **29, 30**| `XTAL_N/P` | Analog | Analog | 40.000 MHz HF-Präzisionsquarz `Y1` |
| **31, 32**| `VCC_3V3` | Power | Power In | +3.3V Analog-Versorgung |
| **33 (EP)**| `GND` | Ground | Ground | Thermal & Ground Pad |

---

## 3. Build & Flashen (ESP-IDF)

### 3.1 Kompilieren über das zentrale Build-Skript
```bash
./tools/build_firmware.sh keyfob
```

### 3.2 Flashen über USB CDC / JTAG
Den 4-poligen JST-SH Adapter (`J2`) mit dem PC verbinden und flashen:
```bash
./tools/build_firmware.sh keyfob flash -p /dev/cu.usbmodem*
```
