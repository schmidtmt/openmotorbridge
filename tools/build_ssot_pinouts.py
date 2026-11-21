#!/usr/bin/env python3
"""
tools/build_ssot_pinouts.py
SSOT Pinout & Connector Builder for OpenMotorBridge
Extracts and validates PCB nets from KiCad PCBs and injects sub_chips and connectors
into data/pcba_pinouts.json.
"""
import json, os, sys
import pcbnew

SSOT_PATH = "data/pcba_pinouts.json"

OFFICIAL_CHIPS = {
  "ESP32-S31-WROOM-1U": {
    "manufacturer": "Espressif Systems",
    "datasheet_title": "ESP32-S31-WROOM-1 & ESP32-S31-WROOM-1U Datasheet",
    "datasheet_url": "https://documentation.espressif.com/esp32-s31-wroom-1_wroom-1u_datasheet_en.html",
    "pin_description_url": "https://documentation.espressif.com/esp32-s31-wroom-1_wroom-1u_datasheet_en.html#pin-definitions",
    "table_ref": "Table 3-2: Pin Definitions (64-Pad Module)",
    "package": "64-Pad LGA / Surface Mount Module",
    "core": "Dual-Core 32-Bit LX7 @ 240 MHz with Native High-Speed USB 2.0 PHY & 2.4 GHz Wi-Fi 6 / BLE 5.4",
    "used_in_boards": ["PCBA_01", "PCBA_05"]
  },
  "ESP32-C6-MINI-1U": {
    "manufacturer": "Espressif Systems",
    "datasheet_title": "ESP32-C6-MINI-1 & ESP32-C6-MINI-1U Datasheet",
    "datasheet_url": "https://www.espressif.com/sites/default/files/documentation/esp32-c6-mini-1_mini-1u_datasheet_en.pdf",
    "pin_description_url": "https://docs.espressif.com/projects/esp-idf/en/latest/esp32c6/hw-reference/esp32-c6-mini-1-mini-1u_v1.5_en.pdf#page=12",
    "table_ref": "Section 3: Pin Definitions (Table 3-1)",
    "package": "53-Pad Surface Mount Module",
    "core": "32-Bit RISC-V @ 160 MHz with 2.4 GHz Wi-Fi 6, BLE 5.3 & IEEE 802.15.4 (Thread/Zigbee)",
    "used_in_boards": ["PCBA_03", "PCBA_09", "PCBA_10"]
  },
  "ESP32-C3FH4": {
    "manufacturer": "Espressif Systems",
    "datasheet_title": "ESP32-C3 Series Datasheet",
    "datasheet_url": "https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf",
    "pin_description_url": "https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf#page=17",
    "table_ref": "Table 2-2: Pin Description (QFN-32)",
    "package": "QFN-32 (5x5 mm) with 4 MB In-Package Flash (C3FH4)",
    "core": "32-Bit RISC-V @ 160 MHz with 2.4 GHz Wi-Fi 4 & BLE 5.0",
    "used_in_boards": ["PCBA_05", "PCBA_07"]
  },
  "ESP32-C5-WROOM-1U": {
    "manufacturer": "Espressif Systems",
    "datasheet_title": "ESP32-C5-WROOM-1 & ESP32-C5-WROOM-1U Datasheet",
    "datasheet_url": "https://www.espressif.com/sites/default/files/documentation/esp32-c5-wroom-1_wroom-1u_datasheet_en.pdf",
    "pin_description_url": "https://www.espressif.com/sites/default/files/documentation/esp32-c5-wroom-1_wroom-1u_datasheet_en.pdf#page=14",
    "table_ref": "Section 3: Pin Definitions (Table 3-2)",
    "package": "32-Pad Surface Mount Module",
    "core": "32-Bit RISC-V Dual-Band (2.4 & 5 GHz Wi-Fi 6) @ 240 MHz",
    "used_in_boards": ["PCBA_08"]
  },
  "CH554E": {
    "manufacturer": "WCH (Nanjing Qinheng Microelectronics)",
    "datasheet_title": "CH554DS1 USB Microcontroller Datasheet",
    "datasheet_url": "https://www.wch-ic.com/downloads/CH554DS1_PDF.html",
    "pin_description_url": "https://www.wch-ic.com/downloads/CH554DS1_PDF.html#page=5",
    "table_ref": "Section 3: Pin Definitions (MSOP-10)",
    "package": "MSOP-10",
    "core": "Enhanced E8051 Core @ 24 MHz with USB 2.0 Full-Speed Host / Device PHY",
    "used_in_boards": ["PCBA_03"]
  },
  "USB2517I": {
    "manufacturer": "Microchip Technology",
    "datasheet_title": "USB2517 / USB2517i Multi-Port USB 2.0 Hub Controller Datasheet",
    "datasheet_url": "https://ww1.microchip.com/downloads/en/DeviceDoc/00001692C.pdf",
    "pin_description_url": "https://ww1.microchip.com/downloads/en/DeviceDoc/00001692C.pdf#page=12",
    "table_ref": "Table 3-1: 64-Pin QFN Pin Descriptions",
    "package": "QFN-64 (9x9 mm)",
    "core": "7-Port Automotive USB 2.0 High-Speed Hub with Multi-TT",
    "used_in_boards": ["PCBA_01"]
  },
  "USB2514Bi": {
    "manufacturer": "Microchip Technology",
    "datasheet_title": "USB251xB/xBi Automotive USB 2.0 Hi-Speed Hub Controller Datasheet",
    "datasheet_url": "https://ww1.microchip.com/downloads/en/DeviceDoc/00001692C.pdf",
    "pin_description_url": "https://ww1.microchip.com/downloads/en/DeviceDoc/00001692C.pdf#page=12",
    "table_ref": "Table 3-1: 36-Pin QFN Pin Descriptions",
    "package": "QFN-36 (6x6 mm)",
    "core": "4-Port Automotive USB 2.0 High-Speed Hub Controller",
    "used_in_boards": ["PCBA_05", "PCBA_05B"]
  },
  "QCC3084": {
    "manufacturer": "Qualcomm Technologies, Inc.",
    "datasheet_title": "Qualcomm QCC3084 Bluetooth 5.4 Audio SoC Device Specification",
    "datasheet_url": "https://www.qualcomm.com/products/technology/audio/qcc30xx-series/qcc3084",
    "pin_description_url": "https://www.qualcomm.com/products/technology/audio/qcc30xx-series/qcc3084",
    "table_ref": "Pin Definitions & Audio Interface Routing",
    "package": "WLCSP / BGA Module",
    "core": "Dual-Core 32-Bit Audio App Core @ 240 MHz, Dual 120 MHz Kalimba Audio DSPs, Bluetooth 5.4 LE Audio & aptX Adaptive",
    "used_in_boards": ["PCBA_01"]
  },
  "SX1262": {
    "manufacturer": "Semtech Corporation",
    "datasheet_title": "SX1261/2 Long Range Low Power LoRa Transceiver Datasheet",
    "datasheet_url": "https://semtech.my.salesforce.com/sfc/p/#E0000000JelG/a/2R000000HT76/bvyK.51kF34K_iR49Q04kHjG4s3E2_q2kM8Q6u2k7d4",
    "pin_description_url": "https://semtech.my.salesforce.com/sfc/p/#E0000000JelG/a/2R000000HT76/bvyK.51kF34K_iR49Q04kHjG4s3E2_q2kM8Q6u2k7d4",
    "table_ref": "Section 4: Pinout & Pin Description (QFN-24)",
    "package": "QFN-24 (4x4 mm)",
    "core": "Sub-GHz LoRa Transceiver (+22 dBm PA, 150-960 MHz)",
    "used_in_boards": ["PCBA_01", "PCBA_07"]
  },
  "ES8388": {
    "manufacturer": "Everest Semiconductor",
    "datasheet_title": "ES8388 User Guide & Low Power Audio CODEC Datasheet",
    "datasheet_url": "http://www.everest-semi.com/pdf/ES8388%20DS.pdf",
    "pin_description_url": "http://www.everest-semi.com/pdf/ES8388%20DS.pdf#page=4",
    "table_ref": "Pin Configuration & Description (QFN-28)",
    "package": "QFN-28 (4x4 mm)",
    "core": "24-Bit, 8 kHz to 96 kHz Low-Power Multi-bit Delta-Sigma Audio CODEC",
    "used_in_boards": ["PCBA_01", "PCBA_03", "PCBA_09", "PCBA_10"]
  },
  "SA818-DMR": {
    "manufacturer": "NiceRF Wireless Technology",
    "datasheet_title": "SA818-DMR Digital Mobile Radio (DMR Tier I & Analog PMR446) Module Specification",
    "datasheet_url": "https://www.nicerf.com/item/dmr-walkie-talkie-module-sa818-dmr",
    "pin_description_url": "https://www.nicerf.com/item/dmr-walkie-talkie-module-sa818-dmr",
    "table_ref": "Section 3: Pin Definitions (18-Pad Module)",
    "package": "18-Pad SMD Module (36x19 mm)",
    "core": "DMR Tier I & Analog PMR446 Transceiver (1W / 0.5W RF, 400-470 MHz, Baseband Vocoder)",
    "used_in_boards": ["PCBA_10"]
  },
  "SW3516": {
    "manufacturer": "Ismartware Technology",
    "datasheet_title": "SW3516 Multi-Protocol Synchronous Buck USB-PD / QC Power Controller",
    "datasheet_url": "https://www.ismartware.com/upload/2021/04/SW3516_Datasheet_v1.0.pdf",
    "pin_description_url": "https://www.ismartware.com/upload/2021/04/SW3516_Datasheet_v1.0.pdf#page=4",
    "table_ref": "Table 2: Pin Description (QFN-32)",
    "package": "QFN-32 (5x5 mm)",
    "core": "Synchronous Step-Down 30W USB-PD 3.0 / PPS / QC4+ Controller",
    "used_in_boards": ["PCBA_03"]
  },
  "TS5A23157": {
    "manufacturer": "Texas Instruments",
    "datasheet_title": "TS5A23157 Dual 10-Ohm SPDT Analog Switch with 5-V Tolerant Control Inputs",
    "datasheet_url": "https://www.ti.com/lit/ds/symlink/ts5a23157.pdf",
    "pin_description_url": "https://www.ti.com/lit/ds/symlink/ts5a23157.pdf#page=3",
    "table_ref": "Pin Functions (MSOP-10 / VSSOP-10)",
    "package": "MSOP-10 / VSSOP-10",
    "core": "Dual SPDT High-Bandwidth Analog & Full-Speed USB Switch",
    "used_in_boards": ["PCBA_03"]
  },
  "TS3USB221": {
    "manufacturer": "Texas Instruments",
    "datasheet_title": "TS3USB221 High-Speed USB 2.0 (480-Mbps) 1:2 Multiplexer/Demultiplexer Switch",
    "datasheet_url": "https://www.ti.com/lit/ds/symlink/ts3usb221.pdf",
    "pin_description_url": "https://www.ti.com/lit/ds/symlink/ts3usb221.pdf#page=3",
    "table_ref": "Pin Functions (QFN-10 / RSER)",
    "package": "UQFN-10 (2x1.5 mm)",
    "core": "High-Speed USB 2.0 480 Mbps 1:2 Mux Switch with 1.1 GHz Bandwidth",
    "used_in_boards": ["PCBA_05"]
  },
  "TCAN334G": {
    "manufacturer": "Texas Instruments",
    "datasheet_title": "TCAN334G 3.3-V CAN Transceiver with CAN-FD and Standby Mode",
    "datasheet_url": "https://www.ti.com/lit/ds/symlink/tcan334g.pdf",
    "pin_description_url": "https://www.ti.com/lit/ds/symlink/tcan334g.pdf#page=4",
    "table_ref": "Pin Functions (SOIC-8)",
    "package": "SOIC-8",
    "core": "3.3V CAN-FD Automotive Transceiver up to 5 Mbps (ISO 11898-2:2016)",
    "used_in_boards": ["PCBA_01"]
  },
  "BQ24075": {
    "manufacturer": "Texas Instruments",
    "datasheet_title": "BQ24075 1.5-A USB-Friendly Li-Ion Battery Charger and Power-Path Management IC",
    "datasheet_url": "https://www.ti.com/lit/ds/symlink/bq24075.pdf",
    "pin_description_url": "https://www.ti.com/lit/ds/symlink/bq24075.pdf#page=4",
    "table_ref": "Pin Functions (QFN-16)",
    "package": "QFN-16 (3x3 mm)",
    "core": "Dynamic Power-Path Management (DPPM) Li-Ion Charger",
    "used_in_boards": ["PCBA_01", "PCBA_09", "PCBA_10"]
  },
  "BQ51050B": {
    "manufacturer": "Texas Instruments",
    "datasheet_title": "BQ51050B Highly Integrated Wireless Power Receiver and Battery Charger (Qi v1.2)",
    "datasheet_url": "https://www.ti.com/lit/ds/symlink/bq51050b.pdf",
    "pin_description_url": "https://www.ti.com/lit/ds/symlink/bq51050b.pdf#page=4",
    "table_ref": "Pin Functions (QFN-28)",
    "package": "QFN-28 (4.5x3.5 mm)",
    "core": "Wireless Power Consortium (WPC) Qi v1.2 Receiver & Li-Ion Charger",
    "used_in_boards": ["PCBA_07"]
  },
  "SAM-M10Q": {
    "manufacturer": "u-blox",
    "datasheet_title": "SAM-M10Q Ultra-low power multi-constellation GNSS patch antenna module",
    "datasheet_url": "https://content.u-blox.com/sites/default/files/SAM-M10Q_DataSheet_UBX-22013293.pdf",
    "pin_description_url": "https://content.u-blox.com/sites/default/files/SAM-M10Q_DataSheet_UBX-22013293.pdf#page=11",
    "table_ref": "Pin Assignment (Table 3)",
    "package": "Patch Antenna SMD Module (15.5x15.5x6.3 mm)",
    "core": "u-blox M10 concurrent GNSS (GPS, GLONASS, Galileo, BeiDou)",
    "used_in_boards": ["PCBA_05D"]
  },
  "ESP32-PICO-V3-02": {
    "manufacturer": "Espressif Systems",
    "datasheet_title": "ESP32-PICO-V3-02 Datasheet",
    "datasheet_url": "https://www.espressif.com/sites/default/files/documentation/esp32-pico-v3-02_datasheet_en.pdf",
    "pin_description_url": "https://www.espressif.com/sites/default/files/documentation/esp32-pico-v3-02_datasheet_en.pdf#page=10",
    "table_ref": "Table 2-2: Pin Description (QFN-48)",
    "package": "QFN-48 (7x7 mm) SiP with 8 MB Flash & 2 MB PSRAM",
    "core": "Dual-Core 32-Bit Xtensa LX6 @ 240 MHz with 2.4 GHz Wi-Fi & Bluetooth 4.2 / BR/EDR (Classic A2DP Source)",
    "used_in_boards": ["PCBA_01", "PCBA_09", "PCBA_10"]
  }
}

def get_pads_dict(fp):
    pads = {}
    for pad in fp.Pads():
        num = pad.GetNumber()
        net = pad.GetNetname()
        if not net:
            continue
        pads[num] = net
    return pads

def update_ssot():
    with open(SSOT_PATH, "r", encoding="utf-8") as f:
        ssot = json.load(f)

    # 1. Update _meta official_chips
    ssot["_meta"]["official_chips"] = OFFICIAL_CHIPS

    # 2. Board PCBA_01: Zentralbox
    b01 = ssot["boards"].get("PCBA_01")
    if b01:
        b01["sub_chips"] = {
            "U8": {
                "ref": "U8",
                "chip_key": "USB2517I",
                "name": "Microchip USB2517I 7-Port Automotive USB 2.0 Hub",
                "package": "QFN-64 (9x9 mm)",
                "datasheet_url": OFFICIAL_CHIPS["USB2517I"]["datasheet_url"],
                "pin_description_url": OFFICIAL_CHIPS["USB2517I"]["pin_description_url"],
                "table_ref": OFFICIAL_CHIPS["USB2517I"]["table_ref"],
                "pins": [
                    {"pad": "2", "pin_name": "RESET_N", "net": "HUB_RESET_N", "type": "Control In", "target": "U2 (ESP32-S31)", "spec": "Active-Low Hardware Reset via GPIO"},
                    {"pad": "8", "pin_name": "USBDN_DM7", "net": "USBC_DM", "type": "USB D-", "target": "J3 (USB-C Service)", "spec": "Port 7 Downstream USB D-"},
                    {"pad": "9", "pin_name": "USBDN_DP7", "net": "USBC_DP", "type": "USB D+", "target": "J3 (USB-C Service)", "spec": "Port 7 Downstream USB D+" },
                    {"pad": "16", "pin_name": "USBUP_DM", "net": "ESP_USB_DM", "type": "USB D-", "target": "U2.54 (ESP32-S31)", "spec": "Upstream Port USB High-Speed D-"},
                    {"pad": "17", "pin_name": "USBUP_DP", "net": "ESP_USB_DP", "type": "USB D+", "target": "U2.55 (ESP32-S31)", "spec": "Upstream Port USB High-Speed D+"},
                    {"pad": "24", "pin_name": "USBDN_DM1", "net": "BUS1_DM", "type": "USB D-", "target": "J6.3 (Strang 1 Front)", "spec": "Port 1 Downstream USB D-"},
                    {"pad": "25", "pin_name": "USBDN_DP1", "net": "BUS1_DP", "type": "USB D+", "target": "J6.4 (Strang 1 Front)", "spec": "Port 1 Downstream USB D+"},
                    {"pad": "32", "pin_name": "USBDN_DM2", "net": "BUS2_DM", "type": "USB D-", "target": "J6.7 (Strang 2 Pod L)", "spec": "Port 2 Downstream USB D-"},
                    {"pad": "33", "pin_name": "USBDN_DP2", "net": "BUS2_DP", "type": "USB D+", "target": "J6.8 (Strang 2 Pod L)", "spec": "Port 2 Downstream USB D+"},
                    {"pad": "40", "pin_name": "USBDN_DM3", "net": "BUS3_DM", "type": "USB D-", "target": "J6.11 (Strang 3 Pod R)", "spec": "Port 3 Downstream USB D-"},
                    {"pad": "41", "pin_name": "USBDN_DP3", "net": "BUS3_DP", "type": "USB D+", "target": "J6.12 (Strang 3 Pod R)", "spec": "Port 3 Downstream USB D+"},
                    {"pad": "48", "pin_name": "USBDN_DM4", "net": "BUS4_DM", "type": "USB D-", "target": "J6.15 (Strang 4 Radar)", "spec": "Port 4 Downstream USB D-"},
                    {"pad": "49", "pin_name": "USBDN_DP4", "net": "BUS4_DP", "type": "USB D+", "target": "J6.16 (Strang 4 Radar)", "spec": "Port 4 Downstream USB D+"},
                    {"pad": "56", "pin_name": "USBDN_DM5", "net": "BT_USB_DM", "type": "USB D-", "target": "U9.13 (QCC3084)", "spec": "Port 5 Downstream USB D- an Qualcomm BT Audio SoC"},
                    {"pad": "57", "pin_name": "USBDN_DP5", "net": "BT_USB_DP", "type": "USB D+", "target": "U9.14 (QCC3084)", "spec": "Port 5 Downstream USB D+ an Qualcomm BT Audio SoC"},
                    {"pad": "60", "pin_name": "USBDN_DM6", "net": "RES_USB_DM", "type": "USB D-", "target": "J7.3 (Reserve)", "spec": "Port 6 Downstream USB D-"},
                    {"pad": "61", "pin_name": "USBDN_DP6", "net": "RES_USB_DP", "type": "USB D+", "target": "J7.4 (Reserve)", "spec": "Port 6 Downstream USB D+"}
                ]
            },
            "U9": {
                "ref": "U9",
                "chip_key": "QCC3084",
                "name": "Qualcomm QCC3084 Bluetooth 5.4 Audio SoC",
                "package": "WLCSP / BGA Module",
                "datasheet_url": OFFICIAL_CHIPS["QCC3084"]["datasheet_url"],
                "pin_description_url": OFFICIAL_CHIPS["QCC3084"]["pin_description_url"],
                "table_ref": OFFICIAL_CHIPS["QCC3084"]["table_ref"],
                "pins": [
                    {"pad": "3", "pin_name": "I2S_MCLK", "net": "I2S_MCLK", "type": "Clock In", "target": "U2 (ESP32-S31)", "spec": "I2S Master Clock 12.288 MHz"},
                    {"pad": "4", "pin_name": "I2S_BCLK", "net": "I2S_BCLK", "type": "Clock In", "target": "U2 (ESP32-S31)", "spec": "I2S Bit Clock 3.072 MHz"},
                    {"pad": "5", "pin_name": "I2S_WS", "net": "I2S_WS", "type": "Sync In", "target": "U2 (ESP32-S31)", "spec": "I2S Word Select / LRCLK 48 kHz"},
                    {"pad": "6", "pin_name": "I2S_DOUT", "net": "I2S_DOUT", "type": "Audio In", "target": "U2 (ESP32-S31)", "spec": "Digital Audio Stream vom ESP32-S31 DSP zum Helm"},
                    {"pad": "7", "pin_name": "I2S_DIN", "net": "I2S_DIN", "type": "Audio Out", "target": "U2 (ESP32-S31)", "spec": "Helmmikrofon-Audio Stream an den DSP"},
                    {"pad": "9", "pin_name": "UART_TX", "net": "BT_UART_TX", "type": "UART Out", "target": "U2 (ESP32-S31)", "spec": "HCI / AT-Befehle TX zum ESP32-S31"},
                    {"pad": "10", "pin_name": "UART_RX", "net": "BT_UART_RX", "type": "UART In", "target": "U2 (ESP32-S31)", "spec": "HCI / AT-Befehle RX vom ESP32-S31"},
                    {"pad": "11", "pin_name": "CHIP_EN", "net": "BT_EN", "type": "Control In", "target": "U2 (ESP32-S31)", "spec": "Power Enable Active High"},
                    {"pad": "13", "pin_name": "USB_DM", "net": "BT_USB_DM", "type": "USB D-", "target": "U8.56 (Hub Port 5)", "spec": "USB Audio Class 2.0 / DFU Datenleitung D-"},
                    {"pad": "14", "pin_name": "USB_DP", "net": "BT_USB_DP", "type": "USB D+", "target": "U8.57 (Hub Port 5)", "spec": "USB Audio Class 2.0 / DFU Datenleitung D+"},
                    {"pad": "15", "pin_name": "RF_ANT", "net": "BT_RF_AUDIO", "type": "RF 2.4 GHz", "target": "ANT2 (U.FL)", "spec": "Bluetooth 5.4 Dual-A2DP / Auracast Antennenport"}
                ]
            },
            "U10": {
                "ref": "U10",
                "chip_key": "SX1262",
                "name": "Semtech SX1262 LoRa 868 MHz Transceiver",
                "package": "QFN-24 (4x4 mm)",
                "datasheet_url": OFFICIAL_CHIPS["SX1262"]["datasheet_url"],
                "pin_description_url": OFFICIAL_CHIPS["SX1262"]["pin_description_url"],
                "table_ref": OFFICIAL_CHIPS["SX1262"]["table_ref"],
                "pins": [
                    {"pad": "1", "pin_name": "NRESET", "net": "LORA_RST", "type": "Control In", "target": "U2 (ESP32-S31)", "spec": "Hardware Reset Active Low"},
                    {"pad": "10", "pin_name": "RFI_P / RFO", "net": "LORA_RF_868", "type": "RF 868 MHz", "target": "ANT1 (U.FL)", "spec": "LoRa HF-Ausgang (+22 dBm PA)"},
                    {"pad": "14", "pin_name": "BUSY", "net": "LORA_BUSY", "type": "Digital Out", "target": "U2 (ESP32-S31)", "spec": "LoRa Modem Busy Indicator"},
                    {"pad": "15", "pin_name": "DIO1", "net": "LORA_DIO1", "type": "Digital Out", "target": "U2 (ESP32-S31)", "spec": "LoRa Paket-Interrupt / TX-Done IRQ"},
                    {"pad": "18", "pin_name": "MISO", "net": "SPI_MISO", "type": "SPI MISO", "target": "U2 (ESP32-S31)", "spec": "SPI Serial Data Out"},
                    {"pad": "19", "pin_name": "MOSI", "net": "SPI_MOSI", "type": "SPI MOSI", "target": "U2 (ESP32-S31)", "spec": "SPI Serial Data In"},
                    {"pad": "20", "pin_name": "SCK", "net": "SPI_SCK", "type": "SPI CLK", "target": "U2 (ESP32-S31)", "spec": "SPI Serial Clock"},
                    {"pad": "21", "pin_name": "NSS", "net": "LORA_NSS", "type": "SPI CS", "target": "U2 (ESP32-S31)", "spec": "SPI Chip Select Active Low"}
                ]
            },
            "U6": {
                "ref": "U6",
                "chip_key": "TCAN334G",
                "name": "TI TCAN334G Automotive 3.3V CAN-FD Transceiver",
                "package": "SOIC-8",
                "datasheet_url": OFFICIAL_CHIPS["TCAN334G"]["datasheet_url"],
                "pin_description_url": OFFICIAL_CHIPS["TCAN334G"]["pin_description_url"],
                "table_ref": OFFICIAL_CHIPS["TCAN334G"]["table_ref"],
                "pins": [
                    {"pad": "1", "pin_name": "TXD", "net": "CAN_TX", "type": "Digital In", "target": "U2 (ESP32-S31)", "spec": "CAN Sendedaten von ESP32-S31 TWAI"},
                    {"pad": "4", "pin_name": "RXD", "net": "CAN_RX", "type": "Digital Out", "target": "U2 (ESP32-S31)", "spec": "CAN Empfangsdaten an ESP32-S31 TWAI"},
                    {"pad": "6", "pin_name": "CANL", "net": "CAN_L", "type": "CAN Bus", "target": "J1.5", "spec": "Differenzielle CAN-Bus-Leitung LOW"},
                    {"pad": "7", "pin_name": "CANH", "net": "CAN_H", "type": "CAN Bus", "target": "J1.4", "spec": "Differenzielle CAN-Bus-Leitung HIGH"}
                ]
            }
        }
        b01["connectors"] = {
            "J1": {
                "ref": "J1",
                "name": "Fahrzeug-Stromversorgung & CAN-Bus Eingang",
                "type": "Molex MicroLock Plus 6-Pin 1.25mm SMD Vertikal (5055680671)",
                "mating": "Molex 5055650601 (Crimp 5054311000 AWG26-30)",
                "pins": [
                    {"pin": "1", "net": "KL30_IN", "type": "Power In (+12V Dauer)", "spec": "Batterie-Dauerplus über externe Sicherung (5A)"},
                    {"pin": "2", "net": "KL15_IN", "type": "Power In (+12V Zündung)", "spec": "Zündungsplus für Aufwach-Logik & Sleep-Trigger"},
                    {"pin": "3", "net": "GND_PWR", "type": "Power Return", "spec": "Fahrzeugmasse Leistungsrückstrom"},
                    {"pin": "4", "net": "CAN_H", "type": "Automotive CAN High", "spec": "Fahrzeug-CAN Bus Signal High (HD-LAN)"},
                    {"pin": "5", "net": "CAN_L", "type": "Automotive CAN Low", "spec": "Fahrzeug-CAN Bus Signal Low (HD-LAN)"},
                    {"pin": "6", "net": "GND_SHIELD", "type": "Shield", "spec": "Kabelbaum-Schirmungsanschluss"}
                ]
            },
            "J6": {
                "ref": "J6",
                "name": "Automotive 4-Strang USB-Backbone & Power Hub",
                "type": "Molex MicroLock Plus 16-Pin 2x08 1.25mm SMD Vertikal (5054331671)",
                "mating": "Molex 5054321601 (Crimp 5054311000 AWG26-30)",
                "pins": [
                    {"pin": "1", "net": "VBUS_FRONT", "type": "Power Out (+12V/60W)", "spec": "Strang 1: Front-Knoten Stromversorgung (eFuse CH1)"},
                    {"pin": "2", "net": "GND_PWR", "type": "Power Return", "spec": "Strang 1: Masse Rückstrom"},
                    {"pin": "3", "net": "BUS1_DM", "type": "USB 2.0 D-", "spec": "Strang 1: Front-Knoten USB 2.0 Datenleitung D-"},
                    {"pin": "4", "net": "BUS1_DP", "type": "USB 2.0 D+", "spec": "Strang 1: Front-Knoten USB 2.0 Datenleitung D+"},
                    {"pin": "5", "net": "VBUS_POD1", "type": "Power Out (+12V/30W)", "spec": "Strang 2: Koffer-Pod 1 Links Stromversorgung (eFuse CH2)"},
                    {"pin": "6", "net": "GND_PWR", "type": "Power Return", "spec": "Strang 2: Masse Rückstrom"},
                    {"pin": "7", "net": "BUS2_DM", "type": "USB 2.0 D-", "spec": "Strang 2: Pod 1 USB 2.0 Datenleitung D-"},
                    {"pin": "8", "net": "BUS2_DP", "type": "USB 2.0 D+", "spec": "Strang 2: Pod 1 USB 2.0 Datenleitung D+"},
                    {"pin": "9", "net": "VBUS_POD2", "type": "Power Out (+12V/30W)", "spec": "Strang 3: Koffer-Pod 2 Rechts Stromversorgung (eFuse CH3)"},
                    {"pin": "10", "net": "GND_PWR", "type": "Power Return", "spec": "Strang 3: Masse Rückstrom"},
                    {"pin": "11", "net": "BUS3_DM", "type": "USB 2.0 D-", "spec": "Strang 3: Pod 2 USB 2.0 Datenleitung D-"},
                    {"pin": "12", "net": "BUS3_DP", "type": "USB 2.0 D+", "spec": "Strang 3: Pod 2 USB 2.0 Datenleitung D+"},
                    {"pin": "13", "net": "VBUS_RADAR", "type": "Power Out (+12V/15W)", "spec": "Strang 4: Heck-Radar 2.0 Stromversorgung (eFuse CH4)"},
                    {"pin": "14", "net": "GND_PWR", "type": "Power Return", "spec": "Strang 4: Masse Rückstrom"},
                    {"pin": "15", "net": "BUS4_DM", "type": "USB 2.0 D-", "spec": "Strang 4: Heck-Radar USB 2.0 Datenleitung D-"},
                    {"pin": "16", "net": "BUS4_DP", "type": "USB 2.0 D+", "spec": "Strang 4: Heck-Radar USB 2.0 Datenleitung D+"}
                ]
            },
            "J5": {
                "ref": "J5",
                "name": "USV Li-Ion Puffer-Akku & NTC-Temperatursensor",
                "type": "JST-GH 4-Pin 1.25mm SMD Vertikal (BM04B-GHS-TBT)",
                "mating": "JST GHR-04V-S (AWG26-30)",
                "pins": [
                    {"pin": "1", "net": "BAT_PLUS", "type": "Power (3.7V Li-Ion)", "spec": "Puffer-Akku Pluspol (3.0V - 4.2V)"},
                    {"pin": "2", "net": "GND_PWR", "type": "Power Return", "spec": "Puffer-Akku Masse"},
                    {"pin": "3", "net": "BAT_NTC", "type": "Analog In", "spec": "10k NTC Thermistor zu GND zur Lade-Temperaturüberwachung"},
                    {"pin": "4", "net": "GND_PWR", "type": "Power Return", "spec": "NTC Referenzmasse"}
                ]
            }
        }

    # 3. Board PCBA_03: Smart Cartridge
    b03 = ssot["boards"].get("PCBA_03")
    if b03:
        b03["sub_chips"] = {
            "U7": {
                "ref": "U7",
                "chip_key": "CH554E",
                "name": "WCH CH554E USB 2.0 Full-Speed Host Controller",
                "package": "MSOP-10",
                "datasheet_url": OFFICIAL_CHIPS["CH554E"]["datasheet_url"],
                "pin_description_url": OFFICIAL_CHIPS["CH554E"]["pin_description_url"],
                "table_ref": OFFICIAL_CHIPS["CH554E"]["table_ref"],
                "pins": [
                    {"pad": "3", "pin_name": "RXD1 / P1.6", "net": "CH554_UART_TX", "type": "UART In", "target": "U1.26 (ESP32-C6 GPIO20)", "spec": "3.0 Mbps UART RX vom ESP32-C6 (TX)"},
                    {"pad": "4", "pin_name": "TXD1 / P1.7", "net": "CH554_UART_RX", "type": "UART Out", "target": "U1.27 (ESP32-C6 GPIO21)", "spec": "3.0 Mbps UART TX zum ESP32-C6 (RX)"},
                    {"pad": "5", "pin_name": "GND", "net": "GND", "type": "Power Return", "target": "GND Plane", "spec": "Massebezug"},
                    {"pad": "6", "pin_name": "UDM", "net": "OMM_USB_DM", "type": "USB D-", "target": "U4.7 (TS5A23157)", "spec": "USB 2.0 Host Datenleitung D- zum OMM-Modul via U4/J4"},
                    {"pad": "7", "pin_name": "UDP", "net": "OMM_USB_DP", "type": "USB D+", "target": "U4.9 (TS5A23157)", "spec": "USB 2.0 Host Datenleitung D+ zum OMM-Modul via U4/J4"},
                    {"pad": "8", "pin_name": "GND", "net": "GND", "type": "Power Return", "target": "GND Plane", "spec": "Massebezug"},
                    {"pad": "9", "pin_name": "V33", "net": "VCC_3V3", "type": "Power In", "target": "3.3V Rail (C8 100nF)", "spec": "3.3V Versorgungsspannung"},
                    {"pad": "10", "pin_name": "VCC", "net": "VCC_3V3", "type": "Power In", "target": "3.3V Rail", "spec": "3.3V Versorgungsspannung"}
                ]
            },
            "U4": {
                "ref": "U4",
                "chip_key": "TS5A23157",
                "name": "TI TS5A23157 Dual SPDT Analog/USB-Switch",
                "package": "MSOP-10",
                "datasheet_url": OFFICIAL_CHIPS["TS5A23157"]["datasheet_url"],
                "pin_description_url": OFFICIAL_CHIPS["TS5A23157"]["pin_description_url"],
                "table_ref": OFFICIAL_CHIPS["TS5A23157"]["table_ref"],
                "pins": [
                    {"pad": "1", "pin_name": "1IN", "net": "OMM_DETECT", "type": "Control In", "target": "J4.6 / R9 Pull-Up", "spec": "Steuereingang Schalter 1 (HIGH=Analog Codec, LOW=Digital OMM)"},
                    {"pad": "2", "pin_name": "1NO", "net": "AUDIO_IN_L", "type": "Analog Audio In", "target": "U3.8 (ES8388 LIN1)", "spec": "Schließer 1: Analog Line-In Links vom OEM Headset"},
                    {"pad": "3", "pin_name": "GND", "net": "GND", "type": "Power Return", "target": "GND Plane", "spec": "Massebezug"},
                    {"pad": "4", "pin_name": "2NO", "net": "AUDIO_IN_R", "type": "Analog Audio In", "target": "U3.9 (ES8388 RIN1)", "spec": "Schließer 2: Analog Line-In Rechts vom OEM Headset"},
                    {"pad": "5", "pin_name": "2IN", "net": "OMM_DETECT", "type": "Control In", "target": "J4.6 / R9 Pull-Up", "spec": "Steuereingang Schalter 2"},
                    {"pad": "6", "pin_name": "2COM", "net": "POD_IO_DM_R", "type": "Dual-Mode I/O", "target": "J4.5", "spec": "Gemeinsamer Kontakt 2 zu Pin 5 des Hybrid-Steckers J4"},
                    {"pad": "7", "pin_name": "2NC", "net": "OMM_USB_DM", "type": "USB D-", "target": "U7.6 (CH554E UDM)", "spec": "Öffner 2: Digital USB D- Verbindung zum CH554E Host"},
                    {"pad": "8", "pin_name": "V+", "net": "VCC_3V3", "type": "Power In", "target": "3.3V Rail", "spec": "3.3V Versorgungsspannung"},
                    {"pad": "9", "pin_name": "1NC", "net": "OMM_USB_DP", "type": "USB D+", "target": "U7.7 (CH554E UDP)", "spec": "Öffner 1: Digital USB D+ Verbindung zum CH554E Host"},
                    {"pad": "10", "pin_name": "1COM", "net": "POD_IO_DP_L", "type": "Dual-Mode I/O", "target": "J4.4", "spec": "Gemeinsamer Kontakt 1 zu Pin 4 des Hybrid-Steckers J4"}
                ]
            },
            "U3": {
                "ref": "U3",
                "chip_key": "ES8388",
                "name": "Everest Semi ES8388 24-Bit Audio Codec",
                "package": "QFN-28 (4x4 mm)",
                "datasheet_url": OFFICIAL_CHIPS["ES8388"]["datasheet_url"],
                "pin_description_url": OFFICIAL_CHIPS["ES8388"]["pin_description_url"],
                "table_ref": OFFICIAL_CHIPS["ES8388"]["table_ref"],
                "pins": [
                    {"pad": "1", "pin_name": "MCLK", "net": "I2S_MCLK", "type": "Clock In", "target": "U1.15 (ESP32-C6)", "spec": "I2S Master Clock (12.288 MHz)"},
                    {"pad": "2", "pin_name": "BCLK", "net": "I2S_BCLK", "type": "Clock In", "target": "U1.16 (ESP32-C6)", "spec": "I2S Bit Clock (3.072 MHz)"},
                    {"pad": "3", "pin_name": "LRCK", "net": "I2S_WS", "type": "Sync In", "target": "U1.19 (ESP32-C6)", "spec": "I2S Word Select / Frame Sync (48 kHz)"},
                    {"pad": "4", "pin_name": "DSOUT", "net": "I2S_DIN", "type": "Audio Out", "target": "U1.24 (ESP32-C6)", "spec": "Digitalisiertes Mikrofon-Signal an MCU"},
                    {"pad": "5", "pin_name": "DSIN", "net": "I2S_DOUT", "type": "Audio In", "target": "U1.20 (ESP32-C6)", "spec": "Downlink Audio vom DSP zum DAC"},
                    {"pad": "8", "pin_name": "LIN1", "net": "AUDIO_IN_L", "type": "Analog In", "target": "U4.2 (via J4.4)", "spec": "Analoger Audio-Eingang Links vom OEM-Intercom"},
                    {"pad": "9", "pin_name": "RIN1", "net": "AUDIO_IN_R", "type": "Analog In", "target": "U4.4 (via J4.5)", "spec": "Analoger Audio-Eingang Rechts vom OEM-Intercom"},
                    {"pad": "12", "pin_name": "LOUT1", "net": "VOICE_OUT", "type": "Analog Out", "target": "J4.7", "spec": "Analoger Mikrofon-Pegel Ausgang an OEM-Headset Mic-In"},
                    {"pad": "20", "pin_name": "SCL", "net": "I2C_SCL", "type": "I2C SCL", "target": "U1.13 (ESP32-C6)", "spec": "I2C Taktleitung zur Codec-Registerprogrammierung"},
                    {"pad": "21", "pin_name": "SDA", "net": "I2C_SDA", "type": "I2C SDA", "target": "U1.23 (ESP32-C6)", "spec": "I2C Datenleitung zur Codec-Registerprogrammierung"}
                ]
            }
        }
        b03["connectors"] = {
            "J1": {
                "ref": "J1",
                "name": "J_BUS (Backbone Bus-Eingang von Zentralbox)",
                "type": "JST-GH 4-Pin 1.25mm SMD Vertikal (BM04B-GHS-TBT)",
                "mating": "JST GHR-04V-S (AWG26-30)",
                "pins": [
                    {"pin": "1", "net": "VCC_BUS", "type": "Power In (+12V...+20V)", "spec": "Bordnetz-/PD-Speisung von Zentralbox (abgesichert 30W)"},
                    {"pin": "2", "net": "GND", "type": "Power Return", "spec": "Leistungs- und Signalmasse"},
                    {"pin": "3", "net": "USB_DP", "type": "USB 2.0 D+", "spec": "USB 2.0 High-Speed D+ zur Zentralbox"},
                    {"pin": "4", "net": "USB_DM", "type": "USB 2.0 D-", "spec": "USB 2.0 High-Speed D- zur Zentralbox"},
                    {"pin": "MP", "net": "GND", "type": "Shield", "spec": "Rastlaschen auf Masse-Plane gelegt"}
                ]
            },
            "J2": {
                "ref": "J2",
                "name": "J_USB_OUT (In-Bag 30W USB-PD Ladedose)",
                "type": "JST-GH 4-Pin 1.25mm SMD Vertikal (BM04B-GHS-TBT)",
                "mating": "JST GHR-04V-S (AWG26-30)",
                "pins": [
                    {"pin": "1", "net": "VBUS_30W", "type": "Power Out (+5V..+20V)", "spec": "Geregelte 30W USB-PD Ladespannung (SW3516)"},
                    {"pin": "2", "net": "GND", "type": "Power Return", "spec": "Ladeleistungs-Rückstrom"},
                    {"pin": "3", "net": "CC1", "type": "PD Config", "spec": "Configuration Channel 1 für USB-PD Aushandlung"},
                    {"pin": "4", "net": "CC2", "type": "PD Config", "spec": "Configuration Channel 2 für USB-PD Aushandlung"},
                    {"pin": "MP", "net": "GND", "type": "Shield", "spec": "Rastlaschen auf Masse-Plane"}
                ]
            },
            "J3": {
                "ref": "J3",
                "name": "J_ACT (4-Kanal Mechatronik-Aktuatorschiene)",
                "type": "JST-SH 8-Pin 1.0mm SMD Vertikal (BM08B-SRSS-TB)",
                "mating": "JST SHR-08V-S-B (AWG28-30)",
                "pins": [
                    {"pin": "1", "net": "GND", "type": "Power Return", "spec": "Massebezug"},
                    {"pin": "2", "net": "GND", "type": "Power Return", "spec": "Massebezug"},
                    {"pin": "3", "net": "ACT_4", "type": "Open-Drain Out", "spec": "Aktuator 4 (Mesh-Taste, geschaltet via Q4 AO3400A)"},
                    {"pin": "4", "net": "ACT_3", "type": "Open-Drain Out", "spec": "Aktuator 3 (Center-Taste, geschaltet via Q3 AO3400A)"},
                    {"pin": "5", "net": "ACT_2", "type": "Open-Drain Out", "spec": "Aktuator 2 (Minus-Taste, geschaltet via Q2 AO3400A)"},
                    {"pin": "6", "net": "ACT_1", "type": "Open-Drain Out", "spec": "Aktuator 1 (Plus-Taste, geschaltet via Q1 AO3400A)"},
                    {"pin": "7", "net": "VCC_5V_PROT", "type": "Power Out (+5V)", "spec": "Polyfuse-geschützte 5V Speisung für Aktuatoren"},
                    {"pin": "8", "net": "VCC_5V_PROT", "type": "Power Out (+5V)", "spec": "Polyfuse-geschützte 5V Speisung für Aktuatoren"},
                    {"pin": "MP", "net": "GND", "type": "Shield", "spec": "Rastlaschen auf Masse"}
                ]
            },
            "J4": {
                "ref": "J4",
                "name": "J_AUDIO_PWR (Hybrid Intercom & OMM Module Header)",
                "type": "JST-SH 8-Pin 1.0mm SMD Vertikal (BM08B-SRSS-TB)",
                "mating": "JST SHR-08V-S-B (AWG28-30)",
                "pins": [
                    {"pin": "1", "net": "GND", "type": "Power Return", "spec": "Gemeinsame Signal- und Lastmasse"},
                    {"pin": "2", "net": "VCC_5V_PROT", "type": "Power Out (+5V)", "spec": "Polyfuse-geschützte 5V Speisung (F1 1.1A gesichert)"},
                    {"pin": "3", "net": "GND", "type": "Power Return", "spec": "Massebezug"},
                    {"pin": "4", "net": "POD_IO_DP_L", "type": "Dual-Mode I/O", "spec": "Modus A: Line-In Links / Modus B: OMM USB D+"},
                    {"pin": "5", "net": "POD_IO_DM_R", "type": "Dual-Mode I/O", "spec": "Modus A: Line-In Rechts / Modus B: OMM USB D-"},
                    {"pin": "6", "net": "OMM_DETECT", "type": "Control In", "spec": "Mode-Sense (HIGH 3.3V = Analog-Codec, LOW 0V = Digital-OMM USB Host)"},
                    {"pin": "7", "net": "VOICE_OUT", "type": "Analog Audio Out", "spec": "Modus A: Sprache vom ES8388 DAC an Headset Mic-In"},
                    {"pin": "8", "net": "PTT_BTN", "type": "Digital In", "spec": "Hardware PTT-Taster (Active-Low gegen Masse, 10k PU)"},
                    {"pin": "MP", "net": "GND", "type": "Shield", "spec": "Rastlaschen auf Masse"}
                ]
            }
        }

    # 4. Board PCBA_05: Front Node
    b05 = ssot["boards"].get("PCBA_05")
    if b05:
        b05["sub_chips"] = {
            "U10": {
                "ref": "U10",
                "chip_key": "ESP32-C3FH4",
                "name": "ESP32-C3FH4 Infotainment Client & WHIM Bypass Sub-MCU",
                "package": "QFN-32 (5x5 mm)",
                "datasheet_url": OFFICIAL_CHIPS["ESP32-C3FH4"]["datasheet_url"],
                "pin_description_url": OFFICIAL_CHIPS["ESP32-C3FH4"]["pin_description_url"],
                "table_ref": OFFICIAL_CHIPS["ESP32-C3FH4"]["table_ref"],
                "pins": [
                    {"pad": "12", "pin_name": "GPIO18 / USB_D-", "net": "C3_USB_DM", "type": "USB D-", "target": "U8 (TS3USB221)", "spec": "USB 2.0 Client D- zu Boom! Box / Nachrüst-AA"},
                    {"pad": "13", "pin_name": "GPIO19 / USB_D+", "net": "C3_USB_DP", "type": "USB D+", "target": "U8 (TS3USB221)", "spec": "USB 2.0 Client D+ zu Boom! Box / Nachrüst-AA"},
                    {"pad": "18", "pin_name": "GPIO4 / I2S_MCLK", "net": "C3_I2S_MCLK", "type": "Clock In", "target": "U1 (ESP32-S31)", "spec": "I2S Master Clock vom S31"},
                    {"pad": "19", "pin_name": "GPIO5 / I2S_BCLK", "net": "C3_I2S_BCLK", "type": "Clock In", "target": "U1 (ESP32-S31)", "spec": "I2S Bit Clock vom S31"},
                    {"pad": "20", "pin_name": "GPIO6 / I2S_WS", "net": "C3_I2S_WS", "type": "Sync In", "target": "U1 (ESP32-S31)", "spec": "I2S Word Select vom S31"},
                    {"pad": "21", "pin_name": "GPIO7 / I2S_SDO", "net": "C3_I2S_SDO", "type": "Audio In", "target": "U1 (ESP32-S31)", "spec": "Audio Playback Stream für Boom! Box Bordlautsprecher"},
                    {"pad": "22", "pin_name": "GPIO8 / I2S_SDI", "net": "C3_I2S_SDI", "type": "Audio Out", "target": "U1 (ESP32-S31)", "spec": "Mikrofon-Rückkanal an Zentralbox DSP"}
                ]
            },
            "U2": {
                "ref": "U2",
                "chip_key": "USB2514Bi",
                "name": "Microchip USB2514Bi 4-Port USB 2.0 Hub",
                "package": "QFN-36 (6x6 mm)",
                "datasheet_url": OFFICIAL_CHIPS["USB2514Bi"]["datasheet_url"],
                "pin_description_url": OFFICIAL_CHIPS["USB2514Bi"]["pin_description_url"],
                "table_ref": OFFICIAL_CHIPS["USB2514Bi"]["table_ref"],
                "pins": [
                    {"pad": "15", "pin_name": "USBUP_DM", "net": "HUB_UP_DM", "type": "USB D-", "target": "U1 (ESP32-S31)", "spec": "Upstream USB D- vom ESP32-S31 Host"},
                    {"pad": "16", "pin_name": "USBUP_DP", "net": "HUB_UP_DP", "type": "USB D+", "target": "U1 (ESP32-S31)", "spec": "Upstream USB D+ vom ESP32-S31 Host"},
                    {"pad": "20", "pin_name": "USBDN_DM1", "net": "HUB_P1_DM", "type": "USB D-", "target": "J4 (Hub Ext JST-GH)", "spec": "Port 1 D- zu PCBA 05B Handschuhfach"},
                    {"pad": "21", "pin_name": "USBDN_DP1", "net": "HUB_P1_DP", "type": "USB D+", "target": "J4 (Hub Ext JST-GH)", "spec": "Port 1 D+ zu PCBA 05B Handschuhfach"},
                    {"pad": "24", "pin_name": "USBDN_DM2", "net": "HUB_P2_DM", "type": "USB D-", "target": "J5 (Wireless Dongle)", "spec": "Port 2 D- an CP2AA CarPlay/AA Dongle"},
                    {"pad": "25", "pin_name": "USBDN_DP2", "net": "HUB_P2_DP", "type": "USB D+", "target": "J5 (Wireless Dongle)", "spec": "Port 2 D+ an CP2AA CarPlay/AA Dongle"}
                ]
            }
        }
        b05["connectors"] = {
            "J1": {
                "ref": "J1",
                "name": "Backbone Bus-Eingang von Zentralbox (Molex J6.1-4)",
                "type": "JST-GH 4-Pin 1.25mm SMD Vertikal (BM04B-GHS-TBT)",
                "mating": "JST GHR-04V-S (AWG26-30)",
                "pins": [
                    {"pin": "1", "net": "VCC_BUS", "type": "Power In (+12V/60W)", "spec": "Bordnetz-/PD-Speisung von Zentralbox"},
                    {"pin": "2", "net": "GND", "type": "Power Return", "spec": "Masse Leistungsrückstrom"},
                    {"pin": "3", "net": "USB_DP", "type": "USB 2.0 D+", "spec": "USB 2.0 High-Speed D+ zur Zentralbox"},
                    {"pin": "4", "net": "USB_DM", "type": "USB 2.0 D-", "spec": "USB 2.0 High-Speed D- zur Zentralbox"},
                    {"pin": "MP", "net": "GND", "type": "Shield", "spec": "Rastlaschen auf Masse"}
                ]
            },
            "J10": {
                "ref": "J10",
                "name": "Navi-Stromversorgungsbuchse (Garmin Zūmo / TomTom)",
                "type": "JST-GH 2-Pin 1.25mm SMD Vertikal (BM02B-GHS-TBT)",
                "mating": "JST GHR-02V-S (AWG24-28)",
                "pins": [
                    {"pin": "1", "net": "VCC_12V_PROT", "type": "Power Out (+12V/2A)", "spec": "Polyfuse-geschützte 12V Speisung für Navi-Cradle"},
                    {"pin": "2", "net": "GND", "type": "Power Return", "spec": "Masse Leistungsrückstrom"},
                    {"pin": "MP", "net": "GND", "type": "Shield", "spec": "Rastlaschen auf Masse"}
                ]
            },
            "J6": {
                "ref": "J6",
                "name": "GNSS & Umweltsensor-Puck Interconnect (PCBA 05D)",
                "type": "JST-GH 8-Pin 1.25mm SMD Vertikal (BM08B-GHS-TBT)",
                "mating": "JST GHR-08V-S (AWG28-30)",
                "pins": [
                    {"pin": "1", "net": "VCC_3V3", "type": "Power Out (+3.3V)", "spec": "Sensor-Versorgung 3.3V LDO"},
                    {"pin": "2", "net": "GND", "type": "Power Return", "spec": "Sensor-Masse"},
                    {"pin": "3", "net": "I2C_SDA", "type": "I2C SDA", "spec": "I2C Datenleitung für TMP117 / OPT3001 / BMP390"},
                    {"pin": "4", "net": "I2C_SCL", "type": "I2C SCL", "spec": "I2C Taktleitung für Umweltsensoren"},
                    {"pin": "5", "net": "GNSS_TX", "type": "UART In", "spec": "u-blox SAM-M10Q NMEA/UBX TX an ESP32-S31 RX"},
                    {"pin": "6", "net": "GNSS_RX", "type": "UART Out", "spec": "ESP32-S31 TX an u-blox SAM-M10Q RX"},
                    {"pin": "7", "net": "GNSS_1PPS", "type": "Sync In", "spec": "u-blox SAM-M10Q 1-PPS Hochpräzisions-Zeittakt"},
                    {"pin": "8", "net": "GND", "type": "Power Return", "spec": "Schirm-Masse"},
                    {"pin": "MP", "net": "GND", "type": "Shield", "spec": "Rastlaschen auf Masse"}
                ]
            }
        }

    # 5. Board PCBA_07: LoRa Smart-Keyfob
    b07 = ssot["boards"].get("PCBA_07")
    if b07:
        b07["sub_chips"] = {
            "U2": {
                "ref": "U2",
                "chip_key": "SX1262",
                "name": "Semtech SX1262 LoRa 868 MHz Transceiver",
                "package": "QFN-24 (4x4 mm)",
                "datasheet_url": OFFICIAL_CHIPS["SX1262"]["datasheet_url"],
                "pin_description_url": OFFICIAL_CHIPS["SX1262"]["pin_description_url"],
                "table_ref": OFFICIAL_CHIPS["SX1262"]["table_ref"],
                "pins": [
                    {"pad": "1", "pin_name": "NRESET", "net": "LORA_RST", "type": "Control In", "target": "U1 (ESP32-C3)", "spec": "Hardware Reset Active Low"},
                    {"pad": "10", "pin_name": "RFI_P / RFO", "net": "LORA_RF_868", "type": "RF 868 MHz", "target": "Johanson 868M Chip-Antenne", "spec": "LoRa HF-Ausgang"},
                    {"pad": "14", "pin_name": "BUSY", "net": "LORA_BUSY", "type": "Digital Out", "target": "U1 (ESP32-C3)", "spec": "LoRa Busy Status"},
                    {"pad": "15", "pin_name": "DIO1", "net": "LORA_DIO1", "type": "Digital Out", "target": "U1 (ESP32-C3)", "spec": "LoRa Interrupt IRQ"},
                    {"pad": "18", "pin_name": "MISO", "net": "SPI_MISO", "type": "SPI MISO", "target": "U1 (ESP32-C3)", "spec": "SPI Data Out"},
                    {"pad": "19", "pin_name": "MOSI", "net": "SPI_MOSI", "type": "SPI MOSI", "target": "U1 (ESP32-C3)", "spec": "SPI Data In"},
                    {"pad": "20", "pin_name": "SCK", "net": "SPI_SCK", "type": "SPI CLK", "target": "U1 (ESP32-C3)", "spec": "SPI Clock"},
                    {"pad": "21", "pin_name": "NSS", "net": "LORA_NSS", "type": "SPI CS", "target": "U1 (ESP32-C3)", "spec": "SPI Chip Select Active Low"}
                ]
            },
            "U4": {
                "ref": "U4",
                "chip_key": "BQ51050B",
                "name": "TI BQ51050B Qi Wireless Power Receiver & Li-Ion Charger",
                "package": "QFN-28 (4.5x3.5 mm)",
                "datasheet_url": OFFICIAL_CHIPS["BQ51050B"]["datasheet_url"],
                "pin_description_url": OFFICIAL_CHIPS["BQ51050B"]["pin_description_url"],
                "table_ref": OFFICIAL_CHIPS["BQ51050B"]["table_ref"],
                "pins": [
                    {"pad": "1", "pin_name": "AC1", "net": "QI_COIL_AC1", "type": "AC In", "target": "J3.1 (Qi Spule)", "spec": "Drahtlose Qi-Empfangsspule AC1"},
                    {"pad": "2", "pin_name": "AC2", "net": "QI_COIL_AC2", "type": "AC In", "target": "J3.2 (Qi Spule)", "spec": "Drahtlose Qi-Empfangsspule AC2"},
                    {"pad": "12", "pin_name": "BAT", "net": "BAT_3V7", "type": "Power Out", "target": "J1.1 (LiPo Akku)", "spec": "Geregelter 4.2V / 500mA Li-Ion Ladestrom"},
                    {"pad": "15", "pin_name": "CHG_STAT", "net": "QI_CHG_STAT", "type": "Digital Out", "target": "U1 (ESP32-C3)", "spec": "Qi Ladestatus (Active Low = lädt)"}
                ]
            }
        }
        b07["connectors"] = {
            "J1": {
                "ref": "J1",
                "name": "LiPo Akku-Anschluss (150 mAh Zelle)",
                "type": "JST-SH 2-Pin 1.0mm SMD Vertikal (BM02B-SRSS-TB)",
                "mating": "JST SHR-02V-S-B (AWG28-30)",
                "pins": [
                    {"pin": "1", "net": "BAT_3V7", "type": "Power (+3.7V)", "spec": "LiPo Akku Pluspol"},
                    {"pin": "2", "net": "GND", "type": "Power Return", "spec": "LiPo Akku Masse"}
                ]
            },
            "J3": {
                "ref": "J3",
                "name": "Qi Drahtlos-Ladespule Eingang",
                "type": "JST-SH 2-Pin 1.0mm SMD Vertikal (BM02B-SRSS-TB)",
                "mating": "JST SHR-02V-S-B (AWG28-30)",
                "pins": [
                    {"pin": "1", "net": "QI_COIL_AC1", "type": "AC In", "spec": "Resonanz-Empfangsspule Anschluss 1"},
                    {"pin": "2", "net": "QI_COIL_AC2", "type": "AC In", "spec": "Resonanz-Empfangsspule Anschluss 2"}
                ]
            }
        }

    # 6. Board PCBA_10: OMM 446 MHz DMR
    b10 = ssot["boards"].get("PCBA_10")
    if b10:
        b10["sub_chips"] = {
            "U3": {
                "ref": "U3",
                "chip_key": "SA818-DMR",
                "name": "NiceRF SA818-DMR Tier I & Analog PMR446 Funk-Transceiver",
                "package": "18-Pad SMD Module",
                "datasheet_url": OFFICIAL_CHIPS["SA818-DMR"]["datasheet_url"],
                "pin_description_url": OFFICIAL_CHIPS["SA818-DMR"]["pin_description_url"],
                "table_ref": OFFICIAL_CHIPS["SA818-DMR"]["table_ref"],
                "pins": [
                    {"pad": "1", "pin_name": "ANT", "net": "RF_446M_ANT", "type": "RF 446 MHz", "target": "J3 (U.FL / Helix)", "spec": "446 MHz Funk-Antennenanschluss (1W TX / RX)"},
                    {"pad": "4", "pin_name": "PTT", "net": "SA818_PTT", "type": "Digital In", "target": "U1 (ESP32-C6)", "spec": "Sendetaste PTT (Active Low = Senden)"},
                    {"pad": "5", "pin_name": "PD / SLEEP", "net": "SA818_PD", "type": "Digital In", "target": "U1 (ESP32-C6)", "spec": "Power Down / Sleep Mode"},
                    {"pad": "6", "pin_name": "AUDIO_IN", "net": "VOICE_MIC_DMR", "type": "Analog Audio In", "target": "U4.12 (ES8388)", "spec": "Sprach-Modulationseingang vom Codec"},
                    {"pad": "7", "pin_name": "AUDIO_OUT", "net": "VOICE_RX_DMR", "type": "Analog Audio Out", "target": "U4.8 (ES8388)", "spec": "Empfangenes Sprachsignal an Codec ADC"},
                    {"pad": "8", "pin_name": "SQ / CARRIER", "net": "SA818_SQ", "type": "Digital Out", "target": "U1 (ESP32-C6)", "spec": "Squelch / Trägererkennung (Carrier Detect)"},
                    {"pad": "9", "pin_name": "UART_TX", "net": "SA818_UART_TX", "type": "UART Out", "target": "U1 (ESP32-C6)", "spec": "Konfigurations-UART TX (Kanal, CTCSS, DMR ID)"},
                    {"pad": "10", "pin_name": "UART_RX", "net": "SA818_UART_RX", "type": "UART In", "target": "U1 (ESP32-C6)", "spec": "Konfigurations-UART RX"}
                ]
            },
            "U4": {
                "ref": "U4",
                "chip_key": "ES8388",
                "name": "Everest Semi ES8388 24-Bit Audio Codec",
                "package": "QFN-28 (4x4 mm)",
                "datasheet_url": OFFICIAL_CHIPS["ES8388"]["datasheet_url"],
                "pin_description_url": OFFICIAL_CHIPS["ES8388"]["pin_description_url"],
                "table_ref": OFFICIAL_CHIPS["ES8388"]["table_ref"],
                "pins": [
                    {"pad": "1", "pin_name": "MCLK", "net": "I2S_MCLK", "type": "Clock In", "target": "U1 (ESP32-C6)", "spec": "I2S Master Clock (12.288 MHz)"},
                    {"pad": "2", "pin_name": "BCLK", "net": "I2S_BCLK", "type": "Clock In", "target": "U1 (ESP32-C6)", "spec": "I2S Bit Clock (3.072 MHz)"},
                    {"pad": "3", "pin_name": "LRCK", "net": "I2S_WS", "type": "Sync In", "target": "U1 (ESP32-C6)", "spec": "I2S Word Select (48 kHz)"},
                    {"pad": "4", "pin_name": "DSOUT", "net": "I2S_DIN", "type": "Audio Out", "target": "U1 (ESP32-C6)", "spec": "Empfangenes Funk-Audio digital an ESP32-C6"},
                    {"pad": "5", "pin_name": "DSIN", "net": "I2S_DOUT", "type": "Audio In", "target": "U1 (ESP32-C6)", "spec": "Sendesprache digital vom ESP32-C6 zum Funkmodul"}
                ]
            }
        }
        b10["connectors"] = {
            "J1": {
                "ref": "J1",
                "name": "USB-C IP67 Service- & Ladeport",
                "type": "USB-C 12-Pin IP67 Wasserdicht SMD (TYPE-C-31-M-12)",
                "mating": "Standard USB-C Kabel",
                "pins": [
                    {"pin": "A1/B12", "net": "GND", "type": "Power Return", "spec": "Massebezug"},
                    {"pin": "A4/B9", "net": "VBUS_USB", "type": "Power In (+5V)", "spec": "5V USB Ladespannung für BQ24075"},
                    {"pin": "A6/B6", "net": "USB_DP", "type": "USB D+", "spec": "USB 2.0 Full-Speed D+ zu ESP32-C6"},
                    {"pin": "A7/B7", "net": "USB_DM", "type": "USB 2.0 D-", "spec": "USB 2.0 Full-Speed D- zu ESP32-C6"}
                ]
            },
            "J2": {
                "ref": "J2",
                "name": "UCS ECE 22.06 Helm-Headset Audio-Interface",
                "type": "JST-SH 6-Pin 1.0mm SMD Vertikal (BM06B-SRSS-TB)",
                "mating": "JST SHR-06V-S-B (AWG28-30)",
                "pins": [
                    {"pin": "1", "net": "HELMET_SPK_L", "type": "Analog Out", "spec": "Lautsprecher Links (32 Ohm Treiber)"},
                    {"pin": "2", "net": "HELMET_SPK_R", "type": "Analog Out", "spec": "Lautsprecher Rechts (32 Ohm Treiber)"},
                    {"pin": "3", "net": "GND", "type": "Power Return", "spec": "Gemeinsame Lautsprecher- und Mikrofonmasse"},
                    {"pin": "4", "net": "HELMET_MIC_P", "type": "Analog In", "spec": "Mikrofonsignal Positiv (Bias 2.2V)"},
                    {"pin": "5", "net": "HELMET_PTT", "type": "Digital In", "spec": "Helm PTT-Taster gegen Masse"},
                    {"pin": "6", "net": "GND", "type": "Power Return", "spec": "Schirmmasse"}
                ]
            }
        }

    # Write back to SSOT
    with open(SSOT_PATH, "w", encoding="utf-8") as f:
        json.dump(ssot, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully updated {SSOT_PATH} with official_chips, sub_chips, and connectors!")

if __name__ == "__main__":
    update_ssot()

def append_remaining_boards():
    with open(SSOT_PATH, "r", encoding="utf-8") as f:
        ssot = json.load(f)

    # PCBA_08: Heck-Radar
    b08 = ssot["boards"].get("PCBA_08")
    if b08:
        b08["sub_chips"] = {
            "U_MR20": {
                "ref": "U_MR20",
                "chip_key": "MR20_RADAR",
                "name": "Wheeltec MR20 77 GHz mmWave FMCW Radar Sensor",
                "package": "Antenna-on-Package (AoP)",
                "datasheet_url": "https://wheeltec.net",
                "pin_description_url": "https://wheeltec.net",
                "table_ref": "MR20 4-Pin Interface Header",
                "pins": [
                    {"pad": "1", "pin_name": "VCC_5V", "net": "VCC_5V", "type": "Power In", "target": "U3.3 (TPS54302)", "spec": "+5V Speisung für 77GHz Radar-Frontend"},
                    {"pad": "2", "pin_name": "GND", "net": "GND", "type": "Power Return", "target": "GND Plane", "spec": "Massebezug"},
                    {"pad": "3", "pin_name": "TX", "net": "RADAR_TX", "type": "UART Out", "target": "U1 (ESP32-C5 RX)", "spec": "20 Hz Radar Objekt-Target Stream (921.6 kbps)"},
                    {"pad": "4", "pin_name": "RX", "net": "RADAR_RX", "type": "UART In", "target": "U1 (ESP32-C5 TX)", "spec": "Radar Konfigurations- und Schwellenwerte"}
                ]
            }
        }
        b08["connectors"] = {
            "J1": {
                "ref": "J1",
                "name": "Backbone Bus-Eingang von Zentralbox (Molex J6.13-16)",
                "type": "JST-GH 4-Pin 1.25mm SMD Vertikal (BM04B-GHS-TBT)",
                "mating": "JST GHR-04V-S (AWG26-30)",
                "pins": [
                    {"pin": "1", "net": "VCC_BUS", "type": "Power In (+12V/15W)", "spec": "Bordnetz-Speisung von Zentralbox (eFuse CH4)"},
                    {"pin": "2", "net": "GND", "type": "Power Return", "spec": "Leistungs- und Signalmasse"},
                    {"pin": "3", "net": "USB_DP", "type": "USB 2.0 D+", "spec": "USB 2.0 High-Speed D+ zur Zentralbox"},
                    {"pin": "4", "net": "USB_DM", "type": "USB 2.0 D-", "spec": "USB 2.0 High-Speed D- zur Zentralbox"},
                    {"pin": "MP", "net": "GND", "type": "Shield", "spec": "Rastlaschen auf Masse"}
                ]
            },
            "J2": {
                "ref": "J2",
                "name": "MR20 77 GHz Radar-Modul Verbindung",
                "type": "JST-SH 4-Pin 1.0mm SMD Vertikal (BM04B-SRSS-TB)",
                "mating": "JST SHR-04V-S-B (AWG28-30)",
                "pins": [
                    {"pin": "1", "net": "VCC_5V", "type": "Power Out (+5V)", "spec": "+5V Radar-Sensor Versorgung"},
                    {"pin": "2", "net": "GND", "type": "Power Return", "spec": "Sensor-Masse"},
                    {"pin": "3", "net": "RADAR_TX", "type": "UART In", "spec": "Objekt-Target Stream vom Radar-Modul"},
                    {"pin": "4", "net": "RADAR_RX", "type": "UART Out", "spec": "Konfigurationsbefehle an Radar-Modul"}
                ]
            }
        }

    # PCBA_09: OMM 2.4 GHz Intercom
    b09 = ssot["boards"].get("PCBA_09")
    if b09:
        b09["sub_chips"] = {
            "U4": {
                "ref": "U4",
                "chip_key": "ES8388",
                "name": "Everest Semi ES8388 24-Bit Audio Codec",
                "package": "QFN-28 (4x4 mm)",
                "datasheet_url": OFFICIAL_CHIPS["ES8388"]["datasheet_url"],
                "pin_description_url": OFFICIAL_CHIPS["ES8388"]["pin_description_url"],
                "table_ref": OFFICIAL_CHIPS["ES8388"]["table_ref"],
                "pins": [
                    {"pad": "1", "pin_name": "MCLK", "net": "I2S_MCLK", "type": "Clock In", "target": "U1 (ESP32-C6)", "spec": "I2S Master Clock (12.288 MHz)"},
                    {"pad": "2", "pin_name": "BCLK", "net": "I2S_BCLK", "type": "Clock In", "target": "U1 (ESP32-C6)", "spec": "I2S Bit Clock (3.072 MHz)"},
                    {"pad": "3", "pin_name": "LRCK", "net": "I2S_WS", "type": "Sync In", "target": "U1 (ESP32-C6)", "spec": "I2S Word Select (48 kHz)"},
                    {"pad": "4", "pin_name": "DSOUT", "net": "I2S_DIN", "type": "Audio Out", "target": "U1 (ESP32-C6)", "spec": "Digitalisiertes Mikrofon-Signal an MCU"},
                    {"pad": "5", "pin_name": "DSIN", "net": "I2S_DOUT", "type": "Audio In", "target": "U1 (ESP32-C6)", "spec": "Mesh/Funk Audio Stream zum Kopfhörer DAC"}
                ]
            },
            "U2": {
                "ref": "U2",
                "chip_key": "BQ24075",
                "name": "TI BQ24075 Li-Ion Akkulader & Power-Path PMIC",
                "package": "QFN-16 (3x3 mm)",
                "datasheet_url": OFFICIAL_CHIPS["BQ24075"]["datasheet_url"],
                "pin_description_url": OFFICIAL_CHIPS["BQ24075"]["pin_description_url"],
                "table_ref": OFFICIAL_CHIPS["BQ24075"]["table_ref"],
                "pins": [
                    {"pad": "13", "pin_name": "IN", "net": "VBUS_USB", "type": "Power In (+5V)", "target": "J1 (USB-C)", "spec": "5V Ladespannungseingang über USB-C"},
                    {"pad": "2", "pin_name": "OUT", "net": "SYS_PWR", "type": "Power Out", "target": "LDO / System Rail", "spec": "System-Betriebsspannung mit unterbrechungsfreier Umschaltung"},
                    {"pad": "3", "pin_name": "BAT", "net": "BAT_3V7", "type": "Power (3.7V)", "target": "LiPo Akku", "spec": "Li-Ion Akku Lade- und Entladeanschluss"},
                    {"pad": "11", "pin_name": "CHG", "net": "CHG_STAT", "type": "Digital Out", "target": "U1 (ESP32-C6)", "spec": "Ladestatusanzeige (Active Low)"}
                ]
            }
        }
        b09["connectors"] = {
            "J1": {
                "ref": "J1",
                "name": "USB-C IP67 Service- & Ladeport",
                "type": "USB-C 12-Pin IP67 Wasserdicht SMD (TYPE-C-31-M-12)",
                "mating": "Standard USB-C Kabel",
                "pins": [
                    {"pin": "A1/B12", "net": "GND", "type": "Power Return", "spec": "Massebezug"},
                    {"pin": "A4/B9", "net": "VBUS_USB", "type": "Power In (+5V)", "spec": "5V USB Ladespannung für BQ24075"},
                    {"pin": "A6/B6", "net": "USB_DP", "type": "USB D+", "spec": "USB 2.0 Full-Speed D+ zu ESP32-C6"},
                    {"pin": "A7/B7", "net": "USB_DM", "type": "USB D-", "spec": "USB 2.0 Full-Speed D- zu ESP32-C6"}
                ]
            },
            "J2": {
                "ref": "J2",
                "name": "UCS ECE 22.06 Helm-Headset Audio-Interface",
                "type": "JST-SH 6-Pin 1.0mm SMD Vertikal (BM06B-SRSS-TB)",
                "mating": "JST SHR-06V-S-B (AWG28-30)",
                "pins": [
                    {"pin": "1", "net": "HELMET_SPK_L", "type": "Analog Out", "spec": "Lautsprecher Links (32 Ohm Treiber)"},
                    {"pin": "2", "net": "HELMET_SPK_R", "type": "Analog Out", "spec": "Lautsprecher Rechts (32 Ohm Treiber)"},
                    {"pin": "3", "net": "GND", "type": "Power Return", "spec": "Gemeinsame Lautsprecher- und Mikrofonmasse"},
                    {"pin": "4", "net": "HELMET_MIC_P", "type": "Analog In", "spec": "Mikrofonsignal Positiv (Bias 2.2V)"},
                    {"pin": "5", "net": "HELMET_PTT", "type": "Digital In", "spec": "Helm PTT-Taster gegen Masse"},
                    {"pin": "6", "net": "GND", "type": "Power Return", "spec": "Schirmmasse"}
                ]
            }
        }

    with open(SSOT_PATH, "w", encoding="utf-8") as f:
        json.dump(ssot, f, indent=2, ensure_ascii=False)
    print("✅ Successfully appended PCBA_08 and PCBA_09 to SSOT!")

if __name__ == "__main__":
    append_remaining_boards()
