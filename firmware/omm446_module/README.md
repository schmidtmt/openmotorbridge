# OpenMotorMesh (OMM) 446 MHz PMR/DMR Transceiver Module Firmware

Dieses Verzeichnis enthält die native ESP-IDF C++ Firmware für das **OMM 446 MHz Analog & Digital PMR/DMR Transceiver Modul (`PCBA 10`)**.

---

## 1. Systemübersicht & Hardware-Architektur

* **Host-MCU:** Espressif ESP32-C6-MINI-1U (RISC-V 32-Bit @ 160 MHz)
* **Funk-Transceiver:** NiceRF SA818-DMR (CMX7141 DSP + 0.2W/0.5W PA)
* **Audio-Codec:** Everest Semi ES8388 (24-Bit / 16 kHz Schmalband-optimiert)
* **Lade- & Power-Management:** Texas Instruments BQ24075 PMIC
* **Formfaktor:** ECE 22.06 UCS ($60{,}0 \times 30{,}0 \times 1{,}0\,\text{mm}$ PCBA)

---

## 2. Vollständiges Hardware-Pinout (`PCBA 10`)

| GPIO / Pin | Signalname | Richtung | Funktion |
| :---: | :--- | :---: | :--- |
| **`GPIO 2`** | `BTN_PTT` | Input | SW1: Push-To-Talk / MFB (Low-aktiv) |
| **`GPIO 3`** | `BTN_MODE` | Input | SW2: Mode Switch (Analog PMR446 <-> Digital DMR Tier I) |
| **`GPIO 4`** | `BTN_CH_UP` | Input | SW3: Kanalwahl Aufwärts (CH 1–16) |
| **`GPIO 5`** | `BTN_CH_DOWN` | Input | SW4: Kanalwahl Abwärts (CH 16–1) |
| **`GPIO 6`** | `WS2812_DATA` | Output | D1: WS2812B-2020 RGB Statusanzeige |
| **`GPIO 7`** | `CHG_STAT` | Input | BQ24075 /STAT Ladeanzeige |
| **`GPIO 8`** | `I2C_SDA` | I/O | ES8388 Audio-Codec I2C Control SDA |
| **`GPIO 9`** | `I2C_SCL` | Output | ES8388 Audio-Codec I2C Control SCL |
| **`GPIO 12`** | `USB_DN` | I/O | USB-C D- Datenleitung (DFU Flashing) |
| **`GPIO 13`** | `USB_DP` | I/O | USB-C D+ Datenleitung (DFU Flashing) |
| **`GPIO 14`** | `SA818_TXD` | Output | UART TX -> SA818 RXD (AT-Befehle, 9600 Baud) |
| **`GPIO 15`** | `SA818_RXD` | Input | UART RX <- SA818 TXD (Telemetrie/Status) |
| **`GPIO 16`** | `SA818_PTT` | Output | SA818 Sende-Aktivierung (**Low = Senden**, High = Empfang) |
| **`GPIO 17`** | `SA818_SQL` | Input | SA818 Rauschsperren-Status (**Low = Träger erkannt**) |
| **`GPIO 18`** | `SA818_PWR_HL` | Output | SA818 Power Umschaltung (**Low = 0.2W Helm**, High = 0.5W Bike) |
| **`GPIO 19`** | `I2S_MCLK` | Output | ES8388 Master Clock |
| **`GPIO 20`** | `I2S_BCLK` | Output | ES8388 Bit Clock |
| **`GPIO 21`** | `I2S_WS` | Output | ES8388 Word Select |
| **`GPIO 22`** | `I2S_DOUT` | Output | ES8388 DAC Audio Stream (Sprachausgabe) |
| **`GPIO 23`** | `I2S_DIN` | Input | ES8388 ADC Audio Stream (Mikrofonaufnahme) |

---

## 3. Betriebsmodi & LED-Farbkodierung

| Zustand | LED-Modus | Farbe / Animation | Bedeutung |
| :--- | :--- | :--- | :--- |
| **Analog Standby** | `LED_MODE_RX_STANDBY_ANALOG` | Grün atmend | Analog PMR446 aktiv, Rauschsperre geschlossen |
| **Digital Standby** | `LED_MODE_RX_STANDBY_DMR` | Cyan atmend | Digital DMR Tier I aktiv, Standby |
| **Analog RX** | `LED_MODE_RX_ACTIVE_ANALOG` | Grün dauerhaft | Funkspruch auf analogem Kanal wird empfangen |
| **Digital RX** | `LED_MODE_RX_ACTIVE_DMR` | Cyan dauerhaft | Glasklarer digitaler DMR-Sprachstrom aktiv |
| **Analog TX** | `LED_MODE_TX_ANALOG` | Rot dauerhaft | Sendet analog mit PTT |
| **Digital TX** | `LED_MODE_TX_DMR` | Blau dauerhaft | Sendet DMR 4FSK digital mit PTT |
| **Kanalwechsel** | `LED_MODE_CHANNEL_CHANGE` | Bernstein aufblitzend | Neuer Kanal eingestellt |
| **Moduswechsel** | `LED_MODE_MODE_SWITCH` | Lila aufblitzend | Wechsel zwischen Analog und Digital |
| **Akku schwach** | `LED_MODE_BATTERY_LOW` | Rot blinkend schnell | Akkuspannung $< 3{,}4\,\text{V}$ |

---

## 4. BLE GATT Fernsteuerung (Cockpit / CarPlay / PWA Dashboard)

* **Service UUID:** `0xFE46` (`OMM-446-Radio`)
* **Char `0x0001` (PTT):** `1` = Senden starten, `0` = Senden beenden.
* **Char `0x0002` (Mode):** `0` = Analog PMR446, `1` = Digital DMR Tier I.
* **Char `0x0003` (Channel):** Kanal `1` bis `16`.
* **Char `0x0004` (CTCSS):** Subton-Index `0` bis `38`.
* **Char `0x0005` (Color Code):** DMR Color Code `1` bis `16`.
* **Char `0x0006` (Squelch):** Rauschsperren-Empfindlichkeit `1` bis `8`.
* **Char `0x0007` (Power):** `0` = 0.2W (Helm), `1` = 0.5W (Bike).
* **Char `0x0008` (Telemetrie):** Akkustand, S-Meter (RSSI in dBm), RX/TX Status.
