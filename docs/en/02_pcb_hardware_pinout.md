# 02 - PCB Hardware & Pinout Specification

The central control box mainboard utilizes a standardized 4-layer FR4 TG150 ENIG layout (85.0 x 55.0 mm, 1.6 mm board thickness).

## 1. HD26 / 2x13 Pin Header Assignment (Enclosure Wall Interface)

Pins 1 to 18: 100% Satellite Pod Connections ($3 \times 6$-Conductor Shielded PUR)  
Pins 19 to 26: Vehicle Power, Automotive Buses, Shield & Dedicated Reserve

| Pin | Signal | Description |
| :--- | :--- | :--- |
| **Pin 1** | `POD1_VCC` | 5V switched supply Pod 1 (via High-Side P-MOSFET) |
| **Pin 2** | `POD1_GND` | Dedicated power and signal ground Pod 1 |
| **Pin 3** | `POD1_NF_P` | Balanced audio signal + (Bourns LM-NP-1001-B1L) |
| **Pin 4** | `POD1_NF_N` | Balanced audio signal - (Bourns LM-NP-1001-B1L) |
| **Pin 5** | `POD1_OPTO` | Optocoupler key trigger (Toshiba TLP222A) |
| **Pin 6** | `POD1_1WIRE_ID`| Dedicated 1-Wire ID bus for Pod 1 (DS2401) |
| **Pin 7** | `POD2_VCC` | 5V switched supply Pod 2 (via High-Side P-MOSFET) |
| **Pin 8** | `POD2_GND` | Dedicated power and signal ground Pod 2 |
| **Pin 9** | `POD2_NF_P` | Balanced audio signal + (Bourns LM-NP-1001-B1L) |
| **Pin 10** | `POD2_NF_N` | Balanced audio signal - (Bourns LM-NP-1001-B1L) |
| **Pin 11** | `POD2_OPTO` | Optocoupler key trigger (Toshiba TLP222A) |
| **Pin 12** | `POD2_1WIRE_ID`| Dedicated 1-Wire ID bus for Pod 2 (DS2401) |
| **Pin 13** | `POD3_VCC` | 5V continuous power supply Pod 3 (Rear) |
| **Pin 14** | `POD3_GND` | Dedicated power and signal ground Pod 3 |
| **Pin 15** | `POD3_UART_TX` | Data stream from Rear Co-Processor to Central Box |
| **Pin 16** | `POD3_UART_RX` | Command data from Central Box to Rear Co-Processor |
| **Pin 17** | `POD3_GNSS_PPS`| 1-PPS time reference sync (jitter < 1 µs) |
| **Pin 18** | `POD3_1WIRE_ID`| Dedicated 1-Wire ID bus for Pod 3 (DS2401) |
| **Pin 19** | `KL30` | Vehicle permanent battery +12V (PPTC fuse protected) |
| **Pin 20** | `KL15` | Vehicle switched ignition +12V (sense & wake-up) |
| **Pin 21** | `GND_PWR` | Main vehicle power ground |
| **Pin 22** | `GND_SHIELD` | Overall cable shield and chassis ground |
| **Pin 23** | `CAN_H` | CAN-Bus High (TI TCAN334G Transceiver) |
| **Pin 24** | `CAN_L` | CAN-Bus Low (TI TCAN334G Transceiver) |
| **Pin 25** | `RESERVE_GPIO_A`| Multifunction input (e.g. external PTT / analog input) |
| **Pin 26** | `RESERVE_GPIO_B`| Multifunction output (e.g. relay / action cam power) |

## 2. ESP32-S3 GPIO Mapping

| GPIO | Signal Name | Function & Peripheral |
| :--- | :--- | :--- |
| **GPIO 1** | `ADC_BAT` | UPS battery voltage sense via 1:2 divider (BQ24075) |
| **GPIO 2** | `POD1_1WIRE_ID`| 1-Wire bus for Port 1 cartridge detection (DS2401) |
| **GPIO 3** | `ADC_LINE_LVL` | Audio peak level sense & acknowledgement tone detect |
| **GPIO 4** | `ADC_VIGN` | Ignition KL15 monitoring via 1:11 precision divider |
| **GPIO 5** | `PORT1_KEY` | TLP222A trigger Port 1 (Sena Intercom toggle) |
| **GPIO 6** | `PORT1_VCC_EN` | High-Side MOSFET Port 1 power gate |
| **GPIO 7** | `PORT2_KEY` | TLP222A trigger Port 2 (Cardo channel advance) |
| **GPIO 8** | `PORT2_VCC_EN` | High-Side MOSFET Port 2 power gate |
| **GPIO 9** | `I2S_MCLK` | Master clock for ES8388 audio codec (12.288 MHz) |
| **GPIO 10** | `I2S_BCLK` | Bit clock audio (3.072 MHz) |
| **GPIO 11** | `I2S_WS` | Word select / LRCLK (48 kHz) |
| **GPIO 12** | `I2S_DOUT` | Audio data out (DSP to ES8388 DAC) |
| **GPIO 13** | `I2S_DIN` | Audio data in (From ES8388 ADC to DSP) |
| **GPIO 14** | `I2C_SDA` | I2C data bus (BMI270 IMU & ES8388 control) |
| **GPIO 15** | `I2C_SCL` | I2C clock (400 kHz) |
| **GPIO 16** | `CHG_STAT_N` | BQ24075 charging state monitor |
| **GPIO 17** | `GNSS_RX` | u-blox MAX-M10S UART RX (from Rear Pod 3) |
| **GPIO 18** | `GNSS_TX` | u-blox MAX-M10S UART TX (to Rear Pod 3) |
| **GPIO 19** | `CAN_TX` | TWAI / CAN-Bus TX to TCAN334G |
| **GPIO 20** | `CAN_RX` | TWAI / CAN-Bus RX from TCAN334G |
| **GPIO 21** | `GNSS_PPS` | 1-PPS hardware time sync interrupt (< 1 µs jitter) |
| **GPIO 22** | `POD2_1WIRE_ID`| 1-Wire bus for Port 2 cartridge detection (DS2401) |
| **GPIO 38** | `RESERVE_A` | Multifunction I/O Pin A (HD26 Pin 25) |
| **GPIO 39** | `RESERVE_B` | Multifunction I/O Pin B (HD26 Pin 26) |
| **GPIO 48** | `STATUS_LED` | WS2812B RGB status indicator |
