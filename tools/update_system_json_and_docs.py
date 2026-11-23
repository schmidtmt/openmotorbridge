#!/usr/bin/env python3
"""
tools/update_system_json_and_docs.py
Synchronizes JSON SSOT files and regenerates Markdown documentation:
- tools/build_ssot_pinouts.py & data/pcba_pinouts.json
- data/system_communication_matrix.json
- data/bom_parts.json
- docs/de/07_pcba_hardware_pinouts.md & docs/en/07_pcba_hardware_pinouts.md
- docs/de/12_system_communication_matrix.md & docs/en/12_system_communication_matrix.md
"""

import json
import os
import subprocess
import sys

def update_comm_matrix():
    path = "data/system_communication_matrix.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Update nodes
    data["nodes"]["NODE_FRONT_CHIP1"] = {
        "id": "PCBA 05 - MCU",
        "name": "Frontnode Main Controller",
        "controller": "ESP32-S31-WROOM-1U (U1)",
        "role": "Sensor-Aggregation, Fahrtwind-Mikrofon, Daumentaster, Backbone-Uplink zur Zentralbox, Bluetooth Audio & AT-Control"
    }

    data["nodes"]["NODE_FRONT_CHIP2"] = {
        "id": "PCBA 05 - BT Transceiver",
        "name": "Frontnode Bluetooth Audio Gateway",
        "controller": "Feasycom FSC-BT802 (Qualcomm CSR8670, U2)",
        "role": "Dual-Mode Bluetooth 5.1 Audio Gateway zu SkylineOS / OEM-Headset / Navigation / Smartphone"
    }

    # 2. Update buses
    data["buses"]["BUS_FRONT_INTER_CHIP"] = "Inter-Chip Schnittstelle auf PCBA 05 zwischen ESP32-S31 (U1) und Feasycom FSC-BT802 (U2): I2S Digital Audio (BCLK, WS, DIN, DOUT) + AT-Command UART + EN/RST Control"
    data["buses"]["BUS_BT_RF_FRONT"] = "2.45 GHz Bluetooth 5.1 RF Verbindung von U2 (FSC-BT802) über 50-Ohm Microstrip und Keramik-Chipantenne ANT3 (Johanson 2450AT18A100) zu SkylineOS / Helm / Smartphone"
    data["buses"]["BUS_POWER_GLOVEBOX_J4"] = "6-Pin JST-GH Handschuhfach-Versorgung (J4): 30W USB-PD (SW3526 U5) + 5V/3A Dauerstrom (TPS54302 U3) für Qi-Lader und Zubehör"

    # 3. Update channels
    channels = data.get("channels", [])
    ch_map = {ch["id"]: ch for ch in channels}

    if "COMM_14_INTERCHIP_I2S_AUDIO" in ch_map:
        ch = ch_map["COMM_14_INTERCHIP_I2S_AUDIO"]
        ch["protocol"] = "I2S Digital Audio Bus (BCLK, WS, DIN, DOUT)"
        ch["pkt_type"] = "48 kHz 16-bit Stereo PCM"
        ch["rate"] = "Kontinuierlicher Audio-Stream"
        ch["purpose"] = "Verlustfreie bidirektionale Übergabe des Audiosignals zwischen ESP32-S31 (U1) und Feasycom FSC-BT802 (U2)"
        ch["fw_status"] = "implemented"

    if "COMM_15_INTERCHIP_UART_FLASH" in ch_map:
        ch = ch_map["COMM_15_INTERCHIP_UART_FLASH"]
        ch["id"] = "COMM_15_INTERCHIP_UART_CTRL"
        ch["protocol"] = "UART AT-Command Interface (115.200 Baud)"
        ch["pkt_type"] = "Feasycom ASCII AT-Commands & Responses"
        ch["rate"] = "Event-basiert / Setup"
        ch["payload"] = ["AT_Config", "AT_Connect", "AT_A2DP", "AT_HFP", "AT_Status"]
        ch["purpose"] = "ESP32-S31 steuert den FSC-BT802 vollautomatisch über AT-Befehle (Pairing, Verbindungsaufbau, Status)"
        ch["fw_status"] = "implemented"

    if "COMM_16_INTERCHIP_MEDIA_CONTROLS" in ch_map:
        ch = ch_map["COMM_16_INTERCHIP_MEDIA_CONTROLS"]
        ch["protocol"] = "UART AT-Commands (AVRCP Controls)"
        ch["pkt_type"] = "AT+TRACK_NEXT, AT+TRACK_PREV, AT+PLAY_PAUSE, AT+VOL"
        ch["payload"] = ["Opcode (Next_Track, Prev_Track, Play_Pause, Vol_Up, Vol_Down, Voice_Trigger)"]
        ch["purpose"] = "Leitet Lenkertaster-Eingaben für Musik und Sprachassistent an FSC-BT802 weiter"
        ch["fw_status"] = "implemented"

    if "COMM_17_INTERCHIP_MUX_CONTROL" in ch_map:
        ch = ch_map["COMM_17_INTERCHIP_MUX_CONTROL"]
        ch["id"] = "COMM_17_BT_HARDWARE_CONTROL"
        ch["protocol"] = "Hardware GPIO Control (BT_EN / BT_RST)"
        ch["pkt_type"] = "GPIO Level (U1.39 -> BT_EN, U1.38 -> BT_RST)"
        ch["payload"] = ["BT_Enable_State", "BT_Reset_Pulse"]
        ch["purpose"] = "Hardware Power-Management und Kaltstart-Reset des FSC-BT802 durch den ESP32-S31"
        ch["fw_status"] = "implemented"

    if "COMM_18_INTERCHIP_INFOTAINMENT_STATUS" in ch_map:
        ch = ch_map["COMM_18_INTERCHIP_INFOTAINMENT_STATUS"]
        ch["protocol"] = "UART AT Status Telemetrie"
        ch["pkt_type"] = "BT_STATUS_REPORT"
        ch["payload"] = ["A2DP_Connected (bool)", "HFP_Connected (bool)", "Streaming_Active", "Battery_Level", "RSSI"]
        ch["purpose"] = "Rückmeldung des Bluetooth-Betriebszustands an ESP32-S31 zur Weiterleitung an die Zentralbox"
        ch["fw_status"] = "implemented"

    if "COMM_19_UAC_SPEAKER_STREAM" in ch_map:
        ch = ch_map["COMM_19_UAC_SPEAKER_STREAM"]
        ch["id"] = "COMM_19_BT_A2DP_SPEAKER_STREAM"
        ch["bus"] = "BUS_BT_RF_FRONT"
        ch["protocol"] = "Bluetooth A2DP Sink / SBC Audio Stream via ANT3"
        ch["pkt_type"] = "Standard A2DP Audio Streaming Packets"
        ch["rate"] = "44.1 / 48 kHz Stereo Audio"
        ch["payload"] = ["Navi_Voice_Audio", "Intercom_Mix_Audio"]
        ch["purpose"] = "Drahtlose Audio-Wiedergabe von Navi-Ansagen und Intercom über das Harley SkylineOS / Boom! Box Bord-Audiosystem"
        ch["fw_status"] = "implemented"

    if "COMM_20_WHIM_HEADSET_BYPASS" in ch_map:
        ch = ch_map["COMM_20_WHIM_HEADSET_BYPASS"]
        ch["id"] = "COMM_20_BT_HFP_HEADSET_PROFILE"
        ch["bus"] = "BUS_BT_RF_FRONT"
        ch["protocol"] = "Bluetooth HFP 1.7 Handsfree Profile"
        ch["pkt_type"] = "HFP Audio & AT Commands"
        ch["payload"] = ["Call_Audio", "Voice_Recognition_Trigger"]
        ch["purpose"] = "Bluetooth Headset-Kopplung mit SkylineOS für Telefonie, Sprachassistent und WHIM-Kompatibilität"
        ch["fw_status"] = "implemented"

    if "COMM_21_HID_MEDIA_CONTROLS" in ch_map:
        ch = ch_map["COMM_21_HID_MEDIA_CONTROLS"]
        ch["id"] = "COMM_21_BT_AVRCP_MEDIA_CONTROLS"
        ch["bus"] = "BUS_BT_RF_FRONT"
        ch["protocol"] = "Bluetooth AVRCP 1.6 Controller Profile"
        ch["pkt_type"] = "AVRCP Control Commands"
        ch["payload"] = ["Play_Pause", "Scan_Next", "Scan_Previous", "Volume_Increment", "Volume_Decrement"]
        ch["purpose"] = "Steuerung des Musik-Playbacks auf dem Werks-Display über die OpenMotorBridge Daumentaster via Bluetooth"
        ch["fw_status"] = "implemented"

    if "COMM_23_AFTERMARKET_AA_DATAPATH" in ch_map:
        ch = ch_map["COMM_23_AFTERMARKET_AA_DATAPATH"]
        ch["source"] = "NODE_FRONT_CHIP1"
        ch["bus"] = "BUS_POWER_GLOVEBOX_J4"
        ch["protocol"] = "30W USB Power Delivery (SW3526) & 5V/3A DC (TPS54302)"
        ch["pkt_type"] = "USB-PD Negotiation & DC Power Feed"
        ch["rate"] = "Dauerhafte Speisung bis 30W"
        ch["payload"] = ["VBUS_PD (5V-20V)", "VCC_5V (Aux)"]
        ch["purpose"] = "Schnellladung und Stromversorgung für Handschuhfach-Geräte, Qi-Ladeschale oder Nachrüst-Displays an J4"
        ch["fw_status"] = "implemented"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("✅ system_communication_matrix.json updated successfully!")

def update_bom_parts():
    path = "data/bom_parts.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    parts = data.get("parts", {})
    if "pcba_05" in parts:
        parts["pcba_05"]["spec"] = "82x50mm 4-Layer, ESP32-S31-WROOM-1U, Feasycom FSC-BT802 (CSR8670 BT 5.1 Audio), Johanson 2450AT18A100, TPS54302, SW3526 30W USB-PD, SPH0645LM4H MEMS"
        parts["pcba_05"]["desc"] = {
            "de": "Cockpit-Hauptknoten für 30W USB-PD, Bluetooth 5.1 Dual-Mode Audio-Gateway (FSC-BT802), Knowles MEMS Wind-Tracking & BSD-Spiegelansteuerung",
            "en": "Cockpit main node for 30W USB-PD, Bluetooth 5.1 dual-mode audio gateway (FSC-BT802), Knowles MEMS wind tracking & BSD mirror drive"
        }

    # Add FSC-BT802 if not present
    if "ic_fsc_bt802" not in parts:
        parts["ic_fsc_bt802"] = {
            "type": "ic",
            "name": {
                "de": "Feasycom FSC-BT802 Bluetooth 5.1 Dual-Mode Modul (CSR8670)",
                "en": "Feasycom FSC-BT802 Bluetooth 5.1 Dual-Mode Module (CSR8670)"
            },
            "spec": "SMD-27 (9.7x11.5 mm), Qualcomm CSR8670, A2DP Sink, HFP, AVRCP, I2S Digital Audio",
            "source": "Feasycom / JLCPCB",
            "unit": "Stk.",
            "cost_eur": [6.50, 7.80],
            "desc": {
                "de": "Dual-Mode Bluetooth 5.1 Audio-Transceiver für drahtlose SkylineOS / Helm-Anbindung auf PCBA 05",
                "en": "Dual-mode Bluetooth 5.1 audio transceiver for wireless SkylineOS / helmet link on PCBA 05"
            }
        }

    # Add Johanson ceramic antenna if not present
    if "ant_johanson_2450" not in parts:
        parts["ant_johanson_2450"] = {
            "type": "component",
            "name": {
                "de": "Johanson 2450AT18A100 2.45 GHz Keramik-Chip-Antenne",
                "en": "Johanson 2450AT18A100 2.45 GHz Ceramic Chip Antenna"
            },
            "spec": "EIA 1206 (3.2x1.6 mm) SMD, 2.4-2.5 GHz, 0.5 dBi Peak Gain, 50 Ohm",
            "source": "Johanson Technology / Mouser / DigiKey",
            "unit": "Stk.",
            "cost_eur": [0.45, 0.65],
            "desc": {
                "de": "Kompakte Onboard-Keramikantenne für Bluetooth-Transceiver U2 an der Ostkante von PCBA 05",
                "en": "Compact onboard ceramic chip antenna for Bluetooth transceiver U2 at East edge of PCBA 05"
            }
        }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("✅ bom_parts.json updated successfully!")

def update_build_ssot_pinouts_script():
    path = "tools/build_ssot_pinouts.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add FSC-BT802 to OFFICIAL_CHIPS
    fsc_chip_def = '''  "FSC-BT802": {
    "manufacturer": "Feasycom / Qualcomm",
    "datasheet_title": "Feasycom FSC-BT802 CSR8670 Bluetooth 5.1 Dual-Mode Audio Module Datasheet",
    "datasheet_url": "https://www.feasycom.com/uploads/20210323/FSC-BT802-Datasheet.pdf",
    "pin_description_url": "https://www.feasycom.com/uploads/20210323/FSC-BT802-Datasheet.pdf#page=6",
    "table_ref": "Table 3-1: Pin Descriptions",
    "package": "27-Pad SMD Module (9.7x11.5x1.8 mm)",
    "core": "Qualcomm CSR8670 Dual-Mode Bluetooth 5.1 Audio SoC @ 80 MHz with DSP & 16-Bit Stereo Codec",
    "used_in_boards": ["PCBA_05"]
  },
'''
    if '"FSC-BT802":' not in content:
        content = content.replace('OFFICIAL_CHIPS = {\n', 'OFFICIAL_CHIPS = {\n' + fsc_chip_def)
        print("Added FSC-BT802 to OFFICIAL_CHIPS in tools/build_ssot_pinouts.py")

    # 2. Update used_in_boards for ESP32-C3FH4 and USB2514Bi
    content = content.replace('"used_in_boards": ["PCBA_05", "PCBA_07"]', '"used_in_boards": ["PCBA_07"]')
    content = content.replace('"used_in_boards": ["PCBA_05", "PCBA_05B"]', '"used_in_boards": ["PCBA_05B"]')

    # 3. Replace PCBA_05 section
    old_b05_marker = '    # 4. Board PCBA_05: Front Node'
    next_b_marker = '    # 5. Board PCBA_07: LoRa Smart-Keyfob'
    
    start_idx = content.find(old_b05_marker)
    end_idx = content.find(next_b_marker)
    assert start_idx != -1 and end_idx != -1, "Could not find PCBA_05 block in tools/build_ssot_pinouts.py"

    new_b05_block = '''    # 4. Board PCBA_05: Front Node
    b05 = ssot["boards"].get("PCBA_05")
    if b05:
        # Update U1 (ESP32-S31) MCU pins to match redesigned PCB & Schematic
        b05["pins"] = [
            {"pad": "3", "gpio": None, "net": "ESP_EN", "fw_define": None, "signal_type": "Power/Reset", "target": "R1 / C3 / SW1", "description": "Chip Enable / Hardware Reset"},
            {"pad": "4", "gpio": 2, "net": "GNSS_TIMEPULSE", "fw_define": None, "signal_type": "Digital In", "target": "J6.5", "description": "u-blox SAM-M10Q 1-PPS Timepulse Synchronization"},
            {"pad": "5", "gpio": 3, "net": "GNSS_TXD", "fw_define": None, "signal_type": "UART_RX", "target": "J6.6", "description": "u-blox SAM-M10Q Primary NMEA / UBX Stream RX"},
            {"pad": "6", "gpio": 4, "net": "MIC_I2S_WS", "fw_define": "PIN_MIC_I2S_WS", "signal_type": "I2S_WS", "target": "MK1.2", "description": "Fahrtwindmikrofon Knowles SPH0645 Word Select"},
            {"pad": "7", "gpio": 5, "net": "MIC_I2S_BCLK", "fw_define": "PIN_MIC_I2S_BCLK", "signal_type": "I2S_BCLK", "target": "MK1.3", "description": "Fahrtwindmikrofon Knowles SPH0645 Bit Clock"},
            {"pad": "8", "gpio": 8, "net": "BTN_SIG_L_N", "fw_define": "PIN_BTN_SIG_L", "signal_type": "Digital In", "target": "J2.3", "description": "Linker Spiegeltaster (PTT / Intercom / HFP)"},
            {"pad": "9", "gpio": 9, "net": "BTN_SIG_R_N", "fw_define": "PIN_BTN_SIG_R", "signal_type": "Digital In", "target": "J3.3", "description": "Rechter Spiegeltaster (Action-Cam Tagging / Mode)"},
            {"pad": "10", "gpio": 6, "net": "GNSS_RXD", "fw_define": None, "signal_type": "UART_TX", "target": "J6.7", "description": "u-blox SAM-M10Q Configuration Stream TX"},
            {"pad": "11", "gpio": 7, "net": "GNSS_RESET_N", "fw_define": None, "signal_type": "Control Out", "target": "J6.8", "description": "u-blox SAM-M10Q Hardware Reset (Active Low)"},
            {"pad": "12", "gpio": 35, "net": "MIC_I2S_DATA", "fw_define": "PIN_MIC_I2S_DATA", "signal_type": "I2S_DATA", "target": "MK1.1", "description": "Fahrtwindmikrofon Knowles SPH0645 Serial Data"},
            {"pad": "13", "gpio": 33, "net": "BT_UART_TX", "fw_define": "PIN_BT_UART_TX", "signal_type": "UART_TX", "target": "U2.18", "description": "AT Command TX an Feasycom FSC-BT802 Pin 18 (CSR8670)"},
            {"pad": "14", "gpio": 34, "net": "BT_UART_RX", "fw_define": "PIN_BT_UART_RX", "signal_type": "UART_RX", "target": "U2.17", "description": "AT Command RX von Feasycom FSC-BT802 Pin 17 (CSR8670)"},
            {"pad": "15", "gpio": 15, "net": "GPIO15", "fw_define": None, "signal_type": "GPIO", "target": "Testpunkt", "description": "General Purpose I/O (Reserve)"},
            {"pad": "16", "gpio": 16, "net": "GPIO16", "fw_define": None, "signal_type": "GPIO", "target": "Testpunkt", "description": "General Purpose I/O (Reserve)"},
            {"pad": "17", "gpio": 22, "net": "I2C_SDA", "fw_define": "PIN_I2C_SDA", "signal_type": "I2C_SDA", "target": "J6.3 / J9.4 / J11.4", "description": "Cockpit I2C Data (Sensoren & Dual OLEDs)"},
            {"pad": "18", "gpio": 23, "net": "I2C_SCL", "fw_define": "PIN_I2C_SCL", "signal_type": "I2C_SCL", "target": "J6.4 / J9.3 / J11.3", "description": "Cockpit I2C Clock (400 kHz Fast-Mode)"},
            {"pad": "19", "gpio": 24, "net": "WS2812B_DIN", "fw_define": "PIN_WS2812B_DIN", "signal_type": "Digital Out", "target": "LED1.4", "description": "Onboard RGB-Status-LED WS2812B-2020 Data"},
            {"pad": "20", "gpio": 25, "net": "BSD_LED_LEFT", "fw_define": "PIN_BSD_LED_L", "signal_type": "Digital Out", "target": "Q1.2 -> J2.2", "description": "Toter-Winkel-Warn-LED Spiegel Links (BSD)"},
            {"pad": "21", "gpio": 26, "net": "BSD_LED_RIGHT", "fw_define": "PIN_BSD_LED_R", "signal_type": "Digital Out", "target": "Q1.5 -> J3.2", "description": "Toter-Winkel-Warn-LED Spiegel Rechts (BSD)"},
            {"pad": "22", "gpio": 27, "net": "AUX_LIGHT_EN", "fw_define": "PIN_AUX_LIGHT_EN", "signal_type": "Digital Out", "target": "Q2.3 -> J7.1", "description": "Zusatzscheinwerfer High-Power Schaltausgang (12V/10A via MOSFET)"},
            {"pad": "23", "gpio": 7, "net": "BT_I2S_BCLK", "fw_define": "PIN_BT_I2S_BCLK", "signal_type": "I2S_BCLK", "target": "U2.15", "description": "Digital Audio I2S Bit Clock an U2 Feasycom FSC-BT802 (CSR8670)"},
            {"pad": "24", "gpio": 10, "net": "BT_I2S_WS", "fw_define": "PIN_BT_I2S_WS", "signal_type": "I2S_WS", "target": "U2.12", "description": "Digital Audio I2S Word Select / Frame Sync an U2 Feasycom FSC-BT802"},
            {"pad": "25", "gpio": 15, "net": "BT_I2S_DOUT", "fw_define": "PIN_BT_I2S_DOUT", "signal_type": "I2S_DOUT", "target": "U2.13", "description": "Digital Audio I2S Serial Data Out an U2 (PCM_IN vom FSC-BT802)"},
            {"pad": "27", "gpio": 0, "net": "ESP_BOOT", "fw_define": None, "signal_type": "Strapping", "target": "SW2", "description": "Boot Mode Strapping Pin / Service Taster"},
            {"pad": "28", "gpio": 48, "net": "BT_I2S_DIN", "fw_define": "PIN_BT_I2S_DIN", "signal_type": "I2S_DIN", "target": "U2.14", "description": "Digital Audio I2S Serial Data In von U2 (PCM_OUT vom FSC-BT802)"},
            {"pad": "29", "gpio": 29, "net": "GPIO29", "fw_define": None, "signal_type": "GPIO", "target": "Testpunkt", "description": "General Purpose I/O (Reserve)"},
            {"pad": "30", "gpio": 35, "net": "SDIO_CLK", "fw_define": None, "signal_type": "SDIO_CLK", "target": "U9.10", "description": "ESP32-E22 Wi-Fi 6E SDIO Clock (50 MHz)"},
            {"pad": "31", "gpio": 36, "net": "SDIO_CMD", "fw_define": None, "signal_type": "SDIO_CMD", "target": "U9.11", "description": "ESP32-E22 Wi-Fi 6E SDIO Command Line"},
            {"pad": "32", "gpio": 37, "net": "SDIO_D0", "fw_define": None, "signal_type": "SDIO_D0", "target": "U9.12", "description": "ESP32-E22 Wi-Fi 6E SDIO Data Line 0"},
            {"pad": "33", "gpio": 33, "net": "SDIO_D1", "fw_define": None, "signal_type": "SDIO_D1", "target": "U9.13", "description": "ESP32-E22 Wi-Fi 6E SDIO Data Line 1"},
            {"pad": "34", "gpio": 34, "net": "SDIO_D2", "fw_define": None, "signal_type": "SDIO_D2", "target": "U9.14", "description": "ESP32-E22 Wi-Fi 6E SDIO Data Line 2"},
            {"pad": "35", "gpio": 38, "net": "SDIO_D3", "fw_define": None, "signal_type": "SDIO_D3", "target": "U9.15", "description": "ESP32-E22 Wi-Fi 6E SDIO Data Line 3"},
            {"pad": "36", "gpio": 59, "net": "E22_EN", "fw_define": None, "signal_type": "Digital Out", "target": "U9.3", "description": "ESP32-E22 Wi-Fi 6E Chip Enable / Power Gate"},
            {"pad": "37", "gpio": 60, "net": "E22_IRQ", "fw_define": None, "signal_type": "Digital In", "target": "U9.16", "description": "ESP32-E22 Wi-Fi 6E Interrupt Request"},
            {"pad": "38", "gpio": 56, "net": "BT_RST", "fw_define": "PIN_BT_RST", "signal_type": "Digital Out", "target": "U2.4", "description": "Feasycom FSC-BT802 Hardware Reset Active Low (RESETB)"},
            {"pad": "39", "gpio": 57, "net": "BT_EN", "fw_define": "PIN_BT_EN", "signal_type": "Digital Out", "target": "U2.3", "description": "Feasycom FSC-BT802 Power Enable Active High (VREGENABLE)"},
            {"pad": "54", "gpio": None, "net": "USB_UP_DM", "fw_define": None, "signal_type": "USB_DM", "target": "J1.4", "description": "Native USB 2.0 High-Speed D- (Direct 4-Wire Backbone zu Zentralbox)"},
            {"pad": "55", "gpio": None, "net": "USB_UP_DP", "fw_define": None, "signal_type": "USB_DP", "target": "J1.3", "description": "Native USB 2.0 High-Speed D+ (Direct 4-Wire Backbone zu Zentralbox)"}
        ]

        b05["sub_chips"] = {
            "U2": {
                "ref": "U2",
                "chip_key": "FSC-BT802",
                "name": "Feasycom FSC-BT802 Bluetooth 5.1 Dual-Mode Modul (CSR8670)",
                "package": "27-Pad SMD Module (9.7x11.5 mm)",
                "datasheet_url": OFFICIAL_CHIPS["FSC-BT802"]["datasheet_url"],
                "pin_description_url": OFFICIAL_CHIPS["FSC-BT802"]["pin_description_url"],
                "table_ref": OFFICIAL_CHIPS["FSC-BT802"]["table_ref"],
                "pins": [
                    {"pad": "1", "pin_name": "GND", "net": "GND", "type": "Power Return", "target": "Ground Plane", "spec": "Modul-Masse"},
                    {"pad": "2", "pin_name": "VDD_IO", "net": "VCC_3V3", "type": "Power In (+3.3V)", "target": "3.3V Rail", "spec": "I/O Versorgungsspannung"},
                    {"pad": "3", "pin_name": "VREGENABLE", "net": "BT_EN", "type": "Control In", "target": "U1.39 (ESP32-S31)", "spec": "Power Enable Active High"},
                    {"pad": "4", "pin_name": "RESETB", "net": "BT_RST", "type": "Control In", "target": "U1.38 (ESP32-S31)", "spec": "Hardware Reset Active Low"},
                    {"pad": "6", "pin_name": "VBAT", "net": "VCC_3V3", "type": "Power In (+3.3V)", "target": "3.3V Rail", "spec": "Batterie-/Hauptversorgung"},
                    {"pad": "12", "pin_name": "PCM_SYNC", "net": "BT_I2S_WS", "type": "Clock In", "target": "U1.24 (ESP32-S31)", "spec": "I2S Word Select / Frame Sync"},
                    {"pad": "13", "pin_name": "PCM_IN", "net": "BT_I2S_DOUT", "type": "Audio In", "target": "U1.25 (ESP32-S31)", "spec": "I2S Audio RX von S31 MCU"},
                    {"pad": "14", "pin_name": "PCM_OUT", "net": "BT_I2S_DIN", "type": "Audio Out", "target": "U1.28 (ESP32-S31)", "spec": "I2S Audio TX zur S31 MCU"},
                    {"pad": "15", "pin_name": "PCM_CLK", "net": "BT_I2S_BCLK", "type": "Clock In", "target": "U1.23 (ESP32-S31)", "spec": "I2S Bit Clock"},
                    {"pad": "17", "pin_name": "UART_RX", "net": "BT_UART_RX", "type": "UART In", "target": "U1.14 (ESP32-S31)", "spec": "AT Command RX"},
                    {"pad": "18", "pin_name": "UART_TX", "net": "BT_UART_TX", "type": "UART Out", "target": "U1.13 (ESP32-S31)", "spec": "AT Command TX"},
                    {"pad": "19", "pin_name": "RF_ANT", "net": "BT_RF_ANT", "type": "RF 2.4 GHz", "target": "ANT3 (Johanson 2450AT18A100)", "spec": "50 Ohm RF-Ausgang an Keramikantenne"},
                    {"pad": "25", "pin_name": "GND", "net": "GND", "type": "Power Return", "target": "Ground Plane", "spec": "HF/Modul Masse"},
                    {"pad": "27", "pin_name": "GND", "net": "GND", "type": "Power Return", "target": "Ground Plane", "spec": "HF Ground Return"}
                ]
            }
        }

        b05["connectors"] = {
            "J1": {
                "ref": "J1",
                "name": "Backbone Bus-Eingang von Zentralbox (Molex J6.1-4)",
                "type": "JST-GH 4-Pin 1.25mm SMD Horizontal (SM04B-GHS-TB)",
                "mating": "JST GHR-04V-S (AWG26-30)",
                "pins": [
                    {"pin": "1", "net": "VIN_60W", "type": "Power In (+12V/60W)", "spec": "Bordnetz-/PD-Speisung von Zentralbox"},
                    {"pin": "2", "net": "GND", "type": "Power Return", "spec": "Masse Leistungsrückstrom"},
                    {"pin": "3", "net": "USB_UP_DP", "type": "USB 2.0 D+", "spec": "USB 2.0 High-Speed D+ direkt zu ESP32-S31 (U1.55)"},
                    {"pin": "4", "net": "USB_UP_DM", "type": "USB 2.0 D-", "spec": "USB 2.0 High-Speed D- direkt zu ESP32-S31 (U1.54)"},
                    {"pin": "MP", "net": "GND", "type": "Shield", "spec": "Rastlaschen auf Masse"}
                ]
            },
            "J4": {
                "ref": "J4",
                "name": "Handschuhfach Qi / 5V Aux Power Receptacle",
                "type": "JST-GH 6-Pin 1.25mm SMD Horizontal (SM06B-GHS-TB)",
                "mating": "JST GHR-06V-S (AWG24-28)",
                "pins": [
                    {"pin": "1", "net": "VBUS_PD1_OUT", "type": "Power Out (5-20V/30W)", "spec": "USB Power Delivery von SW3526 (U5) für Handschuhfach"},
                    {"pin": "2", "net": "GND", "type": "Power Return", "spec": "Masse Leistungsrückstrom für USB-PD"},
                    {"pin": "3", "net": "USB_DN1_CC1", "type": "USB-PD CC1", "spec": "Configuration Channel 1 von SW3526 (U5)"},
                    {"pin": "4", "net": "USB_DN1_CC2", "type": "USB-PD CC2", "spec": "Configuration Channel 2 von SW3526 (U5)"},
                    {"pin": "5", "net": "VCC_5V", "type": "Power Out (+5V/3A)", "spec": "Dauerhafte 5V Hilfsspannung von TPS54302 (U3)"},
                    {"pin": "6", "net": "GND", "type": "Power Return", "spec": "Gemeinsame Signal- und Lastmasse"},
                    {"pin": "MP", "net": "SHIELD", "type": "Shield", "spec": "Gehäuseschirmung"}
                ]
            },
            "J7": {
                "ref": "J7",
                "name": "Zusatzscheinwerfer High-Power Schaltausgang (Aux Lights)",
                "type": "JST-GH 2-Pin 1.25mm SMD Horizontal (SM02B-GHS-TB)",
                "mating": "JST GHR-02V-S (AWG20-24)",
                "pins": [
                    {"pin": "1", "net": "+12V_AUX", "type": "Power Out (+12V/10A)", "spec": "Geschaltete 12V für High-Power LED Scheinwerfer"},
                    {"pin": "2", "net": "GND", "type": "Power Return", "spec": "Lastmasse Rückstrom"},
                    {"pin": "MP", "net": "GND", "type": "Shield", "spec": "Rastlaschen auf Masse"}
                ]
            },
            "J10": {
                "ref": "J10",
                "name": "Navi-Stromversorgungsbuchse (Garmin Zūmo / TomTom)",
                "type": "JST-GH 2-Pin 1.25mm SMD Horizontal (SM02B-GHS-TB)",
                "mating": "JST GHR-02V-S (AWG24-28)",
                "pins": [
                    {"pin": "1", "net": "+12V_PROT", "type": "Power Out (+12V/2A)", "spec": "Polyfuse-geschützte 12V Speisung für Navi-Cradle"},
                    {"pin": "2", "net": "GND", "type": "Power Return", "spec": "Masse Leistungsrückstrom"},
                    {"pin": "MP", "net": "GND", "type": "Shield", "spec": "Rastlaschen auf Masse"}
                ]
            },
            "J8": {
                "ref": "J8",
                "name": "Action-Cam 5V Stromversorgung (GoPro / Insta360)",
                "type": "JST-GH 2-Pin 1.25mm SMD Horizontal (SM02B-GHS-TB)",
                "mating": "JST GHR-02V-S (AWG24-28)",
                "pins": [
                    {"pin": "1", "net": "VCC_5V", "type": "Power Out (+5V/3A)", "spec": "Dauerhafte 5V Speisung für Cockpit Action-Cam"},
                    {"pin": "2", "net": "GND", "type": "Power Return", "spec": "Masse Leistungsrückstrom"},
                    {"pin": "MP", "net": "GND", "type": "Shield", "spec": "Rastlaschen auf Masse"}
                ]
            },
            "J2": {
                "ref": "J2",
                "name": "Under-Perch Spiegel-Pod Links (PCBA 05C)",
                "type": "JST-GH 4-Pin 1.25mm SMD Horizontal (SM04B-GHS-TB)",
                "mating": "JST GHR-04V-S (AWG28-30)",
                "pins": [
                    {"pin": "1", "net": "VCC_5V", "type": "Power Out (+5V)", "spec": "Speisespannung für bernsteinfarbene BSD Warn-LEDs"},
                    {"pin": "2", "net": "BSD_LED_L_N", "type": "Open-Drain Out", "spec": "Geschaltete Masse für linke BSD Warn-LED"},
                    {"pin": "3", "net": "BTN_SIG_L_N", "type": "Digital In", "spec": "Daumentaster Links (Active Low, interner Pull-Up)"},
                    {"pin": "4", "net": "GND", "type": "Power Return", "spec": "Gemeinsame Schalter- und Signalmasse"},
                    {"pin": "MP", "net": "GND", "type": "Shield", "spec": "Rastlaschen auf Masse"}
                ]
            },
            "J3": {
                "ref": "J3",
                "name": "Under-Perch Spiegel-Pod Rechts (PCBA 05C)",
                "type": "JST-GH 4-Pin 1.25mm SMD Horizontal (SM04B-GHS-TB)",
                "mating": "JST GHR-04V-S (AWG28-30)",
                "pins": [
                    {"pin": "1", "net": "VCC_5V", "type": "Power Out (+5V)", "spec": "Speisespannung für bernsteinfarbene BSD Warn-LEDs"},
                    {"pin": "2", "net": "BSD_LED_R_N", "type": "Open-Drain Out", "spec": "Geschaltete Masse für rechte BSD Warn-LED"},
                    {"pin": "3", "net": "BTN_SIG_R_N", "type": "Digital In", "spec": "Daumentaster Rechts (Active Low, interner Pull-Up)"},
                    {"pin": "4", "net": "GND", "type": "Power Return", "spec": "Gemeinsame Schalter- und Signalmasse"},
                    {"pin": "MP", "net": "GND", "type": "Shield", "spec": "Rastlaschen auf Masse"}
                ]
            },
            "J6": {
                "ref": "J6",
                "name": "GNSS & Umweltsensor-Puck Interconnect (PCBA 05D)",
                "type": "JST-GH 8-Pin 1.25mm SMD Horizontal (SM08B-GHS-TB)",
                "mating": "JST GHR-08V-S (AWG28-30)",
                "pins": [
                    {"pin": "1", "net": "VCC_3V3", "type": "Power Out (+3.3V)", "spec": "Sensor-Versorgung 3.3V LDO"},
                    {"pin": "2", "net": "GND", "type": "Power Return", "spec": "Sensor-Masse"},
                    {"pin": "3", "net": "I2C_SDA", "type": "I2C SDA", "spec": "I2C Datenleitung für TMP117 / OPT3001 / BMP390"},
                    {"pin": "4", "net": "I2C_SCL", "type": "I2C SCL", "spec": "I2C Taktleitung für Umweltsensoren"},
                    {"pin": "5", "net": "GNSS_TIMEPULSE", "type": "Sync In", "spec": "u-blox SAM-M10Q 1-PPS Hochpräzisions-Zeittakt"},
                    {"pin": "6", "net": "GNSS_TXD", "type": "UART In", "spec": "u-blox SAM-M10Q NMEA/UBX TX an ESP32-S31 RX (U1.5)"},
                    {"pin": "7", "net": "GNSS_RXD", "type": "UART Out", "spec": "ESP32-S31 TX (U1.10) an u-blox SAM-M10Q RX"},
                    {"pin": "8", "net": "GNSS_RESET_N", "type": "Control Out", "spec": "Hardware Reset für SAM-M10Q"},
                    {"pin": "MP", "net": "GND", "type": "Shield", "spec": "Rastlaschen auf Masse"}
                ]
            },
            "J9": {
                "ref": "J9",
                "name": "OLED / HUD Displayanschluss Links (Optional)",
                "type": "JST-GH 4-Pin 1.25mm SMD Horizontal (SM04B-GHS-TB)",
                "mating": "JST GHR-04V-S (AWG28-30)",
                "pins": [
                    {"pin": "1", "net": "VCC_3V3", "type": "Power Out (+3.3V)", "spec": "Display-Speisung"},
                    {"pin": "2", "net": "GND", "type": "Power Return", "spec": "Display-Masse"},
                    {"pin": "3", "net": "I2C_SCL", "type": "I2C SCL", "spec": "I2C Takt für linkes Cockpit-Display"},
                    {"pin": "4", "net": "I2C_SDA", "type": "I2C SDA", "spec": "I2C Daten für linkes Cockpit-Display"},
                    {"pin": "MP", "net": "GND", "type": "Shield", "spec": "Rastlaschen auf Masse"}
                ]
            },
            "J11": {
                "ref": "J11",
                "name": "OLED / HUD Displayanschluss Rechts (Optional)",
                "type": "JST-GH 4-Pin 1.25mm SMD Horizontal (SM04B-GHS-TB)",
                "mating": "JST GHR-04V-S (AWG28-30)",
                "pins": [
                    {"pin": "1", "net": "VCC_3V3", "type": "Power Out (+3.3V)", "spec": "Display-Speisung"},
                    {"pin": "2", "net": "GND", "type": "Power Return", "spec": "Display-Masse"},
                    {"pin": "3", "net": "I2C_SCL", "type": "I2C SCL", "spec": "I2C Takt für rechtes Cockpit-Display"},
                    {"pin": "4", "net": "I2C_SDA", "type": "I2C SDA", "spec": "I2C Daten für rechtes Cockpit-Display"},
                    {"pin": "MP", "net": "GND", "type": "Shield", "spec": "Rastlaschen auf Masse"}
                ]
            }
        }
'''
    content = content[:start_idx] + new_b05_block + content[end_idx:]

    # 4. Fix __main__ to run both update_ssot and append_remaining_boards
    main_pattern = '''if __name__ == "__main__":
    append_remaining_boards()'''
    new_main = '''if __name__ == "__main__":
    update_ssot()
    append_remaining_boards()'''
    content = content.replace(main_pattern, new_main)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ tools/build_ssot_pinouts.py updated successfully!")

if __name__ == "__main__":
    update_comm_matrix()
    update_bom_parts()
    update_build_ssot_pinouts_script()

