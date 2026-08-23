# 02 - PCB Hardware & Pinout-Spezifikation

Die Hauptplatine in der Zentralbox nutzt ein standardisiertes 4-Lagen FR4 TG150 ENIG Layout ($85{,}0 \times 55{,}0\,\text{mm}$, Stärke $1{,}6\,\text{mm}$).

## 1. HD26 / 2x13 Wannenstecker-Pinbelegung (Gehäusewand-Interface)

```text
       REIHE 1: 100 % Satelliten-Pods        │       REIHE 2: Power, Busse & Shield
 ┌──────────────────────────────────────────┐ │ ┌──────────────────────────────────────────┐
 │ Pin  1: POD1_VCC (5V geschaltet)         │ │ │ Pin 14: KL30 (Bordnetz Dauerplus 12V)    │
 │ Pin  2: POD1_NF_P (Audio +)              │ │ │ Pin 15: KL15 (Bordnetz Zündungsplus 12V) │
 │ Pin  3: POD1_NF_N (Audio -)              │ │ │ Pin 16: GND_PWR (Bordnetz Power-Masse)   │
 │ Pin  4: POD1_OPTO_KEY (Tasten-Trigger)   │ │ │ Pin 17: CAN_H                            │
 │ Pin  5: POD2_VCC (5V geschaltet)         │ │ │ Pin 18: CAN_L                            │
 │ Pin  6: POD2_NF_P (Audio +)              │ │ │ Pin 19: ONEWIRE_ID (Gemeinsamer ID-Bus)  │
 │ Pin  7: POD2_NF_N (Audio -)              │ │ │ Pin 20: GND_SHIELD (Schirmung Pods)      │
 │ Pin  8: POD2_OPTO_KEY (Tasten-Trigger)   │ │ │ Pin 21: AGND (Audio-Masse Referenz)      │
 │ Pin  9: POD3_VCC (5V Dauer)              │ │ │ Pin 22: RESERVE_GPIO_A                   │
 │ Pin 10: POD3_UART_TX                     │ │ │ Pin 23: RESERVE_GPIO_B                   │
 │ Pin 11: POD3_UART_RX                     │ │ │ Pin 24: RESERVE_I2S_DATA                 │
 │ Pin 12: POD3_GND                         │ │ │ Pin 25: RESERVE_I2S_CLK                  │
 │ Pin 13: NC                               │ │ │ Pin 26: NC                               │
 └──────────────────────────────────────────┘ │ └──────────────────────────────────────────┘

 ```

 ## 2. GPIO-Mapping ESP32-S3

GPIOSignalnameFunktion & PeripherieGPIO 1ADC_BATMessung USV-Akkuspannung via Teiler 1:2 (BQ24075)GPIO 2ONEWIRE_ID1-Wire Bus zur Erkennung der Kassetten-IDs (DS2401)GPIO 3ADC_LINE_LVLNF-Pegelerkennung (Audio-Sense & Quittungston-Check)GPIO 4ADC_VIGNBordnetzüberwachung Zündung KL15 via Teiler 1:11GPIO 5PORT1_KEYOptokoppler TLP222A Trigger Port 1 (Sena Intercom Toggle)GPIO 6PORT1_VCC_ENHigh-Side MOSFET Port 1 SpeisespannungGPIO 7PORT2_KEYOptokoppler TLP222A Trigger Port 2 (Cardo Channel Next)GPIO 8PORT2_VCC_ENHigh-Side MOSFET Port 2 SpeisespannungGPIO 9I2S_MCLKMaster Clock Audio Codec (12,288 MHz)GPIO 10I2S_BCLKBit Clock Audio (3,072 MHz)GPIO 11I2S_WSWord Select / LRCLK (48 kHz)GPIO 12I2S_DOUTAudio Data Out (DSP zu Helm / BT Source)GPIO 13I2S_DINAudio Data In (Mikrofone / BT Sink)GPIO 14I2C_SDAI2C Datenbus (BMI270 IMU)GPIO 15I2C_SCLI2C Takt (400 kHz)GPIO 16CHG_STAT_NLadezustand BQ24075GPIO 17GNSS_RXu-blox MAX-M10S UART RX (Pod 3)GPIO 18GNSS_TXu-blox MAX-M10S UART TX (Pod 3)GPIO 21GNSS_PPS1-PPS Zeitnormal (Jitter < 1 µs)GPIO 48STATUS_LEDWS2812B RGB Statusanzeige
