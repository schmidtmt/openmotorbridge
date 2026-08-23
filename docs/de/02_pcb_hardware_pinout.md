# 02 - PCB Hardware & Pinout-Spezifikation

Die Hauptplatine in der Zentralbox nutzt ein standardisiertes 4-Lagen FR4 TG150 ENIG Layout (85.0 x 55.0 mm, Staerke 1.6 mm).

## 1. HD26 / 2x13 Wannenstecker-Pinbelegung (Gehaeusewand-Interface)

Pins 1 bis 18: 100 % Satelliten-Pods ($3 \times 6$-Ader geschirmt)  
Pins 19 bis 26: Bordnetz, Fahrzeugbusse, Schirmung & Reserve

| Pin | Signal | Beschreibung |
| :--- | :--- | :--- |
| **Pin 1** | `POD1_VCC` | 5V geschaltete Speisespannung Pod 1 (via High-Side MOSFET) |
| **Pin 2** | `POD1_GND` | Dedizierte Power- und Signalmasse Pod 1 |
| **Pin 3** | `POD1_NF_P` | Symmetrisches Audiosignal + (Bourns LM-NP-1001-B1L) |
| **Pin 4** | `POD1_NF_N` | Symmetrisches Audiosignal - (Bourns LM-NP-1001-B1L) |
| **Pin 5** | `POD1_OPTO` | Optokoppler Tasten-Trigger (Toshiba TLP222A) |
| **Pin 6** | `POD1_1WIRE_ID`| Dedizierte 1-Wire ID-Leitung fuer Pod 1 (DS2401) |
| **Pin 7** | `POD2_VCC` | 5V geschaltete Speisespannung Pod 2 (via High-Side MOSFET) |
| **Pin 8** | `POD2_GND` | Dedizierte Power- und Signalmasse Pod 2 |
| **Pin 9** | `POD2_NF_P` | Symmetrisches Audiosignal + (Bourns LM-NP-1001-B1L) |
| **Pin 10** | `POD2_NF_N` | Symmetrisches Audiosignal - (Bourns LM-NP-1001-B1L) |
| **Pin 11** | `POD2_OPTO` | Optokoppler Tasten-Trigger (Toshiba TLP222A) |
| **Pin 12** | `POD2_1WIRE_ID`| Dedizierte 1-Wire ID-Leitung fuer Pod 2 (DS2401) |
| **Pin 13** | `POD3_VCC` | 5V Dauer-Versorgung Pod 3 (Heck) |
| **Pin 14** | `POD3_GND` | Dedizierte Power- und Signalmasse Pod 3 |
| **Pin 15** | `POD3_UART_TX` | Datenstrom vom Heck-Co-Prozessor zur Zentralbox |
| **Pin 16** | `POD3_UART_RX` | Steuerdaten von Zentralbox zum Heck-Co-Prozessor |
| **Pin 17** | `POD3_GNSS_PPS`| 1-PPS Zeitnormal-Synchronisation (Jitter < 1 us) |
| **Pin 18** | `POD3_1WIRE_ID`| Dedizierte 1-Wire ID-Leitung fuer Pod 3 (DS2401) |
| **Pin 19** | `KL30` | Bordnetz Dauerplus 12V (abgesichert via Bourns PPTC) |
| **Pin 20** | `KL15` | Bordnetz Zuendungsplus 12V (Messabgriff & Aufwach-Trigger) |
| **Pin 21** | `GND_PWR` | Bordnetz Power-Masse (Hauptmasse) |
| **Pin 22** | `GND_SHIELD` | Gesamtschirmung fuer Kabelbaum und Gehaeusemasse |
| **Pin 23** | `CAN_H` | CAN-Bus High (TI TCAN334G Transceiver) |
| **Pin 24** | `CAN_L` | CAN-Bus Low (TI TCAN334G Transceiver) |
| **Pin 25** | `RESERVE_GPIO_A`| Multifunktions-Eingang (z. B. externer PTT / Analog-In) |
| **Pin 26** | `RESERVE_GPIO_B`| Multifunktions-Ausgang (z. B. Relais / Actioncam Power) |

## 2. GPIO-Mapping ESP32-S3

| GPIO | Signalname | Funktion & Peripherie |
| :--- | :--- | :--- |
| **GPIO 1** | `ADC_BAT` | Messung USV-Akkuspannung via Teiler 1:2 (BQ24075) |
| **GPIO 2** | `POD1_1WIRE_ID`| 1-Wire Bus zur Erkennung der Kassette an Port 1 (DS2401) |
| **GPIO 3** | `ADC_LINE_LVL` | NF-Pegelerkennung (Audio-Sense & Quittungston-Check) |
| **GPIO 4** | `ADC_VIGN` | Bordnetzueberwachung Zuendung KL15 via Teiler 1:11 |
| **GPIO 5** | `PORT1_KEY` | Optokoppler TLP222A Trigger Port 1 (Sena Intercom Toggle) |
| **GPIO 6** | `PORT1_VCC_EN` | High-Side MOSFET Port 1 Speisespannung |
| **GPIO 7** | `PORT2_KEY` | Optokoppler TLP222A Trigger Port 2 (Cardo Channel Next) |
| **GPIO 8** | `PORT2_VCC_EN` | High-Side MOSFET Port 2 Speisespannung |
| **GPIO 9** | `I2S_MCLK` | Master Clock fuer ES8388 Audio Codec (12.288 MHz) |
| **GPIO 10** | `I2S_BCLK` | Bit Clock Audio (3.072 MHz) |
| **GPIO 11** | `I2S_WS` | Word Select / LRCLK (48 kHz) |
| **GPIO 12** | `I2S_DOUT` | Audio Data Out (DSP zum ES8388 DAC) |
| **GPIO 13** | `I2S_DIN` | Audio Data In (Vom ES8388 ADC zum DSP) |
| **GPIO 14** | `I2C_SDA` | I2C Datenbus (BMI270 IMU & ES8388 Konfiguration) |
| **GPIO 15** | `I2C_SCL` | I2C Takt (400 kHz) |
| **GPIO 16** | `CHG_STAT_N` | Ladezustand BQ24075 |
| **GPIO 17** | `GNSS_RX` | u-blox MAX-M10S UART RX (vom Heck-Pod 3) |
| **GPIO 18** | `GNSS_TX` | u-blox MAX-M10S UART TX (zum Heck-Pod 3) |
| **GPIO 19** | `CAN_TX` | TWAI / CAN-Bus Sendedaten zum TCAN334G |
| **GPIO 20** | `CAN_RX` | TWAI / CAN-Bus Empfangsdaten vom TCAN334G |
| **GPIO 21** | `GNSS_PPS` | 1-PPS Zeitnormal (Jitter < 1 us) |
| **GPIO 22** | `POD2_1WIRE_ID`| 1-Wire Bus zur Erkennung der Kassette an Port 2 (DS2401) |
| **GPIO 38** | `RESERVE_A` | Externer Multifunktions-I/O Pin A (HD26 Pin 25) |
| **GPIO 39** | `RESERVE_B` | Externer Multifunktions-I/O Pin B (HD26 Pin 26) |
| **GPIO 48** | `STATUS_LED` | WS2812B RGB Statusanzeige |
