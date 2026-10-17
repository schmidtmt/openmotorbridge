#!/usr/bin/env python3
"""
tools/sync_cartridge_sch.py
===========================
Synchronizes PCBA 03 (Universal Smart Cartridge) Schematic:
- 100% exact parity with openmotorbridge_pod_cartridge.kicad_pcb.
- Exact components (35 total):
  * U1: ESP32-C6-MINI-1U (65 pads, exact GPIO mappings)
  * U3: ES8388_Codec (QFN-28-1EP, 29 pads)
  * U4: TS5A3159DBVR SPDT Analog/Digital Switch (SOT-23-6, 6 pads)
  * U_UWB: DW3110 UWB Transceiver (QFN-16-1EP, 17 pads)
  * Y_UWB: 38.4MHz Crystal (4 pads: XTAL1, GND, XTAL2, GND)
  * ANT_UWB: U.FL Receptacle (2 pads: UWB_RF, GND)
  * J_ACT: 8P Actuators + MP Shield (9 pads: 2x 5V, 4x ACT, 2x GND, MP)
  * J_AUDIO_PWR: 8P Kelvin Audio/Power + MP Shield (9 pads: GND, 5V, AGND, 2x AUDIO_IN, OMM_DET, AUDIO_IO_P, PTT_USB_N, MP)
  * J_PROG: 4P Programming Header (4 pads: 3V3, USB_DP, GND, PTT_USB_N)
  * J_DC_IN: Automotive Horizontal Blade Slot Socket (10.0mm Pitch, 2 pads: +5V_IN, GND)
  * H1..H4: M2 Mounting Holes with Pads (GND)
  * F1: 1812 Polyfuse (MF-MSMF050-2: +5V_IN -> VCC_5V_PROT)
  * D1..D4: SOD-323 Freewheeling Diodes (1N4148WS)
  * Q1..Q4: SOT-23 MOSFETs (AO3400A: Gate, Source=GND, Drain=ACT)
  * R1..R4: 0603 100R Gate Resistors
  * R5..R8: 0603 100k Gate Pulldowns
  * R9: 0603 10k OMM_DETECT Pull-up
  * C1, C2: 0603 100nF / 0805 10uF Decoupling Caps
"""

import os
import sys
import uuid
import json
import subprocess

SCH_PATH = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_sch"
PCB_PATH = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"

def u():
    return str(uuid.uuid4())

def generate_schematic():
    with open('/tmp/pcba03_pcb_exact.json') as f:
        comps = json.load(f)

    sch = []
    sch.append('(kicad_sch')
    sch.append('\t(version 20260306)')
    sch.append('\t(generator "eeschema")')
    sch.append('\t(generator_version "10.0")')
    sch.append(f'\t(uuid "{u()}")')
    sch.append('\t(paper "A3")')
    sch.append('\t(title_block')
    sch.append('\t\t(title "OpenMotorBridge PCBA 03 - Universal Smart Modular Cartridge Rev 3.0")')
    sch.append('\t\t(date "2026-10-15")')
    sch.append('\t\t(rev "v3.0")')
    sch.append('\t\t(company "OpenMotorBridge Open Source Hardware")')
    sch.append('\t\t(comment 1 "ESP32-C6-MINI-1U Host MCU + Everest Semi ES8388 I2S Codec + Qorvo DW3110 UWB")')
    sch.append('\t\t(comment 2 "TS5A3159 SPDT Audio/USB Switch + 4x AO3400A Actuator MOSFETs + 8P Kelvin Docking")')
    sch.append('\t)')

    # --- LIB SYMBOLS ---
    sch.append('\t(lib_symbols')

    # power:PWR_FLAG
    sch.append('''\t\t(symbol "power:PWR_FLAG"
\t\t\t(property "Reference" "#FLG" (at 0 1.905 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(property "Value" "PWR_FLAG" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(pin power_out line (at 0 0 90) (length 0) (name "pwr" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t)''')

    # MountingHole
    sch.append('''\t\t(symbol "Mechanical:MountingHole_Pad"
\t\t\t(property "Reference" "H" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "MountingHole_Pad" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "MountingHole:MountingHole_2.2mm_M2_Pad" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(pin passive line (at -5.08 0 0) (length 2.54) (name "1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t)''')

    # Blade Slot Socket (J_DC_IN)
    sch.append('''\t\t(symbol "Connector:Blade_Slot_Socket_1x02"
\t\t\t(property "Reference" "J" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "Blade_Slot_Socket_1x02" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Connector:Blade_Slot_Socket_1x02_P10.0mm_Horizontal_SMD" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(pin passive line (at -5.08 2.54 0) (length 2.54) (name "1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 -2.54 0) (length 2.54) (name "2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t)''')

    # U.FL (ANT_UWB)
    sch.append('''\t\t(symbol "Connector_Coaxial:U.FL"
\t\t\t(property "Reference" "ANT" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "U.FL" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Connector_Coaxial:U.FL_Hirose_U.FL-R-SMT-1_Vertical" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(pin passive line (at -5.08 0 0) (length 2.54) (name "RF" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 5.08 0 180) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t)''')

    # Crystal 4Pin
    sch.append('''\t\t(symbol "Device:Crystal_4Pin"
\t\t\t(property "Reference" "Y" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "Crystal_4Pin" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Crystal:Crystal_SMD_2016-4Pin_2.0x1.6mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(pin passive line (at -5.08 2.54 0) (length 2.54) (name "1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 -2.54 0) (length 2.54) (name "2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 5.08 2.54 180) (length 2.54) (name "3" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 5.08 -2.54 180) (length 2.54) (name "4" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t)''')

    # DW3110 QFN-16-1EP
    dw_pins = []
    dw_pin_names = {
        "1": "GND", "2": "XTAL1", "3": "XTAL2", "4": "GND", "5": "GND", "6": "GND",
        "7": "SCK", "8": "MISO", "9": "MOSI", "10": "CS", "11": "GND", "12": "RSTn",
        "13": "IRQ", "14": "VDD3V3", "15": "RF", "16": "GND", "17": "EP"
    }
    for i in range(1, 18):
        s_i = str(i)
        name = dw_pin_names.get(s_i, f"P{i}")
        y_pos = 20.32 - (i - 1) * 2.54
        dw_pins.append(f'\t\t\t(pin passive line (at -10.16 {y_pos:.2f} 0) (length 2.54) (name "{name}" (effects (font (size 1.27 1.27)))) (number "{s_i}" (effects (font (size 1.27 1.27)))))')

    dw_pins_str = '\n'.join(dw_pins)
    sch.append(f'''\t\t(symbol "RF_Module:DW3110"
\t\t\t(property "Reference" "U" (at 0 25.4 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "DW3110" (at 0 -25.4 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Package_DFN_QFN:QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm_ThermalVias" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
{dw_pins_str}
\t\t)''')

    # ES8388 QFN-28-1EP
    es_pins = []
    es_pin_names = {
        "1": "MCLK", "2": "BCLK", "3": "WS", "4": "DIN", "5": "DOUT", "6": "DVDD",
        "7": "DGND", "8": "LIN", "9": "RIN", "10": "AGND", "11": "AVDD", "12": "LOUT",
        "13": "ROUT", "14": "AGND", "15": "AGND", "16": "AGND", "17": "PVDD", "18": "PGND",
        "19": "SDA", "20": "SCL", "21": "DVDD", "22": "DGND", "23": "DGND", "24": "DGND",
        "25": "DGND", "26": "DGND", "27": "PVDD", "28": "PGND", "29": "EP"
    }
    for i in range(1, 30):
        s_i = str(i)
        name = es_pin_names.get(s_i, f"P{i}")
        y_pos = 35.56 - (i - 1) * 2.54
        es_pins.append(f'\t\t\t(pin passive line (at -10.16 {y_pos:.2f} 0) (length 2.54) (name "{name}" (effects (font (size 1.27 1.27)))) (number "{s_i}" (effects (font (size 1.27 1.27)))))')

    es_pins_str = '\n'.join(es_pins)
    sch.append(f'''\t\t(symbol "Audio:ES8388_Codec"
\t\t\t(property "Reference" "U" (at 0 40.64 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "ES8388_Codec" (at 0 -40.64 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Package_DFN_QFN:QFN-28-1EP_4x4mm_P0.4mm_EP2.4x2.4mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
{es_pins_str}
\t\t)''')

    # ESP32-C6-MINI-1U (65 pads)
    c6_pins = []
    c6_pin_names = {
        "1": "GND", "2": "3V3", "3": "EN", "4": "IO4", "5": "IO5", "6": "IO6", "7": "IO7",
        "8": "IO2", "9": "IO3", "10": "IO8", "11": "IO9", "12": "GND", "13": "GND",
        "14": "IO12", "15": "IO13", "16": "IO14", "17": "IO15", "18": "IO16", "19": "IO17",
        "20": "IO18", "21": "IO19", "22": "IO20", "23": "IO21", "24": "IO22", "25": "IO23"
    }
    for i in range(1, 66):
        s_i = str(i)
        name = c6_pin_names.get(s_i, "GND")
        y_pos = 81.28 - (i - 1) * 2.54
        c6_pins.append(f'\t\t\t(pin passive line (at -10.16 {y_pos:.2f} 0) (length 2.54) (name "{name}" (effects (font (size 1.27 1.27)))) (number "{s_i}" (effects (font (size 1.27 1.27)))))')

    c6_pins_str = '\n'.join(c6_pins)
    sch.append(f'''\t\t(symbol "MCU:ESP32-C6-MINI-1U"
\t\t\t(property "Reference" "U" (at 0 86.36 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "ESP32-C6-MINI-1U" (at 0 -86.36 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "RF_Module:ESP32-S2-MINI-1U" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
{c6_pins_str}
\t\t)''')

    # Connector_JST 8P + MP
    sch.append('''\t\t(symbol "Connector_JST:JST_SH_SM08B_Shielded"
\t\t\t(property "Reference" "J" (at 0 12.7 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "Conn_01x08_Shielded" (at 0 -12.7 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Connector_JST:JST_SH_SM08B-SRSS-TB_1x08-1MP_P1.00mm_Horizontal" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(pin passive line (at -5.08 8.89 0) (length 2.54) (name "1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 6.35 0) (length 2.54) (name "2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 3.81 0) (length 2.54) (name "3" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 1.27 0) (length 2.54) (name "4" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 -1.27 0) (length 2.54) (name "5" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 -3.81 0) (length 2.54) (name "6" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 -6.35 0) (length 2.54) (name "7" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 -8.89 0) (length 2.54) (name "8" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 5.08 0 180) (length 2.54) (name "MP" (effects (font (size 1.27 1.27)))) (number "MP" (effects (font (size 1.27 1.27)))))
\t\t)''')

    # Connector_PinHeader 4P
    sch.append('''\t\t(symbol "Connector_PinHeader:PinHeader_1x04"
\t\t\t(property "Reference" "J" (at 0 6.35 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "PinHeader_1x04" (at 0 -6.35 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Connector_PinHeader_1.27mm:PinHeader_1x04_P1.27mm_Vertical_SMD_Pin1Left" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(pin passive line (at -5.08 3.81 0) (length 2.54) (name "1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 1.27 0) (length 2.54) (name "2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 -1.27 0) (length 2.54) (name "3" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 -3.81 0) (length 2.54) (name "4" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t)''')

    # Switch:TS5A3159_SPDT
    sch.append('''\t\t(symbol "Switch:TS5A3159_SPDT"
\t\t\t(property "Reference" "U" (at 0 7.62 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "TS5A3159DBVR" (at 0 -7.62 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Package_TO_SOT_SMD:SOT-23-6" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(pin passive line (at -5.08 2.54 0) (length 2.54) (name "NO" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 5.08 2.54 180) (length 2.54) (name "COM" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 -2.54 0) (length 2.54) (name "IN" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 0 5.08 270) (length 2.54) (name "VCC" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 0 -5.08 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -5.08 0 0) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\t\t)''')

    # Transistor_FET:AO3400A
    sch.append('''\t\t(symbol "Transistor_FET:AO3400A"
\t\t\t(property "Reference" "Q" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "AO3400A" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Package_TO_SOT_SMD:SOT-23" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(pin passive line (at -5.08 0 0) (length 2.54) (name "G" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 2.54 -5.08 90) (length 2.54) (name "S" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 2.54 5.08 270) (length 2.54) (name "D" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t)''')

    # Device:R_Small
    sch.append('''\t\t(symbol "Device:R_Small"
\t\t\t(property "Reference" "R" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "R_Small" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Resistor_SMD:R_0603_1608Metric" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(pin passive line (at 0 2.54 270) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 0 -2.54 90) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t)''')

    # Device:C_Small
    sch.append('''\t\t(symbol "Device:C_Small"
\t\t\t(property "Reference" "C" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "C_Small" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Capacitor_SMD:C_0603_1608Metric" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(pin passive line (at 0 2.54 270) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 0 -2.54 90) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t)''')

    # Device:Polyfuse_Small
    sch.append('''\t\t(symbol "Device:Polyfuse_Small"
\t\t\t(property "Reference" "F" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "Polyfuse_Small" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Fuse:Fuse_1812_4532Metric" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(pin passive line (at -5.08 0 0) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 5.08 0 180) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t)''')

    # Diode:1N4148WS
    sch.append('''\t\t(symbol "Diode:1N4148WS"
\t\t\t(property "Reference" "D" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "1N4148WS" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Diode_SMD:D_SOD-323" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(pin passive line (at -5.08 0 0) (length 2.54) (name "A" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 5.08 0 180) (length 2.54) (name "K" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t)''')

    sch.append('\t)') # end lib_symbols

    # --- INSTANCES & WIRING ---
    sym_map = {
        'ANT_UWB': 'Connector_Coaxial:U.FL',
        'C1': 'Device:C_Small',
        'C2': 'Device:C_Small',
        'D1': 'Diode:1N4148WS',
        'D2': 'Diode:1N4148WS',
        'D3': 'Diode:1N4148WS',
        'D4': 'Diode:1N4148WS',
        'F1': 'Device:Polyfuse_Small',
        'H1': 'Mechanical:MountingHole_Pad',
        'H2': 'Mechanical:MountingHole_Pad',
        'H3': 'Mechanical:MountingHole_Pad',
        'H4': 'Mechanical:MountingHole_Pad',
        'J_ACT': 'Connector_JST:JST_SH_SM08B_Shielded',
        'J_AUDIO_PWR': 'Connector_JST:JST_SH_SM08B_Shielded',
        'J_PROG': 'Connector_PinHeader:PinHeader_1x04',
        'J_DC_IN': 'Connector:Blade_Slot_Socket_1x02',
        'Q1': 'Transistor_FET:AO3400A',
        'Q2': 'Transistor_FET:AO3400A',
        'Q3': 'Transistor_FET:AO3400A',
        'Q4': 'Transistor_FET:AO3400A',
        'R1': 'Device:R_Small',
        'R2': 'Device:R_Small',
        'R3': 'Device:R_Small',
        'R4': 'Device:R_Small',
        'R5': 'Device:R_Small',
        'R6': 'Device:R_Small',
        'R7': 'Device:R_Small',
        'R8': 'Device:R_Small',
        'R9': 'Device:R_Small',
        'U1': 'MCU:ESP32-C6-MINI-1U',
        'U3': 'Audio:ES8388_Codec',
        'U4': 'Switch:TS5A3159_SPDT',
        'U_UWB': 'RF_Module:DW3110',
        'Y_UWB': 'Device:Crystal_4Pin'
    }

    # Layout coordinate mapping for readability
    positions = {
        'J_DC_IN': (40.0, 45.0),
        'F1': (65.0, 40.0),
        'C1': (85.0, 40.0),
        'C2': (105.0, 40.0),
        'H1': (40.0, 70.0),
        'H2': (55.0, 70.0),
        'H3': (70.0, 70.0),
        'H4': (85.0, 70.0),

        'J_PROG': (40.0, 100.0),
        'J_ACT': (75.0, 100.0),
        'J_AUDIO_PWR': (110.0, 100.0),

        'U4': (145.0, 100.0),
        'R9': (165.0, 100.0),

        'D1': (40.0, 140.0),
        'D2': (65.0, 140.0),
        'D3': (90.0, 140.0),
        'D4': (115.0, 140.0),

        'Q1': (40.0, 160.0),
        'Q2': (65.0, 160.0),
        'Q3': (90.0, 160.0),
        'Q4': (115.0, 160.0),

        'R1': (40.0, 180.0),
        'R2': (65.0, 180.0),
        'R3': (90.0, 180.0),
        'R4': (115.0, 180.0),

        'R5': (40.0, 195.0),
        'R6': (65.0, 195.0),
        'R7': (90.0, 195.0),
        'R8': (115.0, 195.0),

        'Y_UWB': (145.0, 140.0),
        'ANT_UWB': (165.0, 140.0),
        'U_UWB': (155.0, 180.0),

        'U3': (210.0, 100.0),
        'U1': (280.0, 120.0),
    }

    # Pin offsets for symbol instances
    # (relative to instance at x, y)
    def get_pin_offset(sym_type, pnum):
        if sym_type == 'power:PWR_FLAG':
            return (0.0, 0.0)
        elif sym_type in ('Mechanical:MountingHole_Pad', 'Connector:Conn_01x01'):
            return (-5.08, 0.0)
        elif sym_type in ('Connector_Automotive:Blade_Slot_Socket_1x02', 'Connector:Blade_Slot_Socket_1x02'):
            return (-5.08, -2.54) if pnum == '1' else (-5.08, 2.54)
        elif sym_type == 'Connector_Coaxial:U.FL':
            return (-5.08, 0.0) if pnum == '1' else (5.08, 0.0)
        elif sym_type == 'Device:Crystal_4Pin':
            return {'1': (-5.08, -2.54), '2': (-5.08, 2.54), '3': (5.08, -2.54), '4': (5.08, 2.54)}[pnum]
        elif sym_type == 'Device:Polyfuse_Small':
            return (-5.08, 0.0) if pnum == '1' else (5.08, 0.0)
        elif sym_type == 'Diode:1N4148WS':
            return (-5.08, 0.0) if pnum == '1' else (5.08, 0.0)
        elif sym_type in ('Device:R_Small', 'Device:C_Small'):
            return (0.0, -2.54) if pnum == '1' else (0.0, 2.54)
        elif sym_type == 'Transistor_FET:AO3400A':
            return {'1': (-5.08, 0.0), '2': (2.54, 5.08), '3': (2.54, -5.08)}[pnum]
        elif sym_type == 'Switch:TS5A3159_SPDT':
            return {'1': (-5.08, -2.54), '2': (5.08, -2.54), '3': (-5.08, 2.54), '4': (0.0, -5.08), '5': (0.0, 5.08), '6': (-5.08, 0.0)}[pnum]
        elif sym_type == 'Connector_PinHeader:PinHeader_1x04':
            return {'1': (-5.08, -3.81), '2': (-5.08, -1.27), '3': (-5.08, 1.27), '4': (-5.08, 3.81)}[pnum]
        elif sym_type == 'Connector_JST:JST_SH_SM08B_Shielded':
            y_offsets = {'1': -8.89, '2': -6.35, '3': -3.81, '4': -1.27, '5': 1.27, '6': 3.81, '7': 6.35, '8': 8.89}
            if pnum in y_offsets:
                return (-5.08, y_offsets[pnum])
            return (5.08, 0.0) # MP
        elif sym_type == 'RF_Module:DW3110':
            i = int(pnum)
            return (-10.16, -(20.32 - (i - 1) * 2.54))
        elif sym_type == 'Audio:ES8388_Codec':
            i = int(pnum)
            return (-10.16, -(35.56 - (i - 1) * 2.54))
        elif sym_type == 'MCU:ESP32-C6-MINI-1U':
            i = int(pnum)
            return (-10.16, -(81.28 - (i - 1) * 2.54))
        return (-5.08, 0.0)

    # Place each symbol instance and its global labels
    labels = []
    for ref in sorted(comps.keys()):
        c = comps[ref]
        sym_type = sym_map[ref]
        pos = positions.get(ref, (50.0, 50.0))
        val = c['value']
        fpid = c['fpid']

        sch.append(f'\t(symbol (lib_id "{sym_type}") (at {pos[0]:.2f} {pos[1]:.2f} 0) (unit 1)')
        sch.append('\t\t(in_bom yes) (on_board yes) (dnp no)')
        sch.append(f'\t\t(uuid "{u()}")')
        sch.append(f'\t\t(property "Reference" "{ref}" (at {pos[0]:.2f} {pos[1]-6.0:.2f} 0) (effects (font (size 1.27 1.27))))')
        sch.append(f'\t\t(property "Value" "{val}" (at {pos[0]:.2f} {pos[1]-3.5:.2f} 0) (effects (font (size 1.27 1.27))))')
        sch.append(f'\t\t(property "Footprint" "{fpid}" (at {pos[0]:.2f} {pos[1]:.2f} 0) (effects (font (size 1.27 1.27)) hide))')

        for pnum in sorted(c['pads'].keys(), key=lambda x: int(x) if x.isdigit() else 999):
            sch.append(f'\t\t(pin "{pnum}" (uuid "{u()}"))')
            net = c['pads'][pnum]
            if net:
                offset = get_pin_offset(sym_type, pnum)
                pin_x = pos[0] + offset[0]
                pin_y = pos[1] + offset[1]
                rot = 180 if offset[0] < 0 else 0
                just = 'right' if rot == 180 else 'left'
                labels.append(f'\t(global_label "{net}" (shape passive) (at {pin_x:.2f} {pin_y:.2f} {rot}) (effects (font (size 1.27 1.27)) (justify {just})))\n')

        sch.append('\t)')

    # Add PWR_FLAGS
    sch.append(f'''\t(symbol (lib_id "power:PWR_FLAG") (at 30.0 30.0 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (dnp no)
\t\t(uuid "{u()}")
\t\t(property "Reference" "#FLG1" (at 30.0 28.0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(property "Value" "PWR_FLAG" (at 30.0 32.0 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at 30.0 30.0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(pin "1" (uuid "{u()}"))
\t)''')
    labels.append('\t(global_label "VCC_3V3" (shape passive) (at 30.0 30.0 180) (effects (font (size 1.27 1.27)) (justify right)))\n')

    sch.append(f'''\t(symbol (lib_id "power:PWR_FLAG") (at 30.0 35.0 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (dnp no)
\t\t(uuid "{u()}")
\t\t(property "Reference" "#FLG2" (at 30.0 33.0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(property "Value" "PWR_FLAG" (at 30.0 37.0 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at 30.0 35.0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(pin "1" (uuid "{u()}"))
\t)''')
    labels.append('\t(global_label "GND" (shape passive) (at 30.0 35.0 180) (effects (font (size 1.27 1.27)) (justify right)))\n')

    sch.append(f'''\t(symbol (lib_id "power:PWR_FLAG") (at 30.0 40.0 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (dnp no)
\t\t(uuid "{u()}")
\t\t(property "Reference" "#FLG3" (at 30.0 38.0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(property "Value" "PWR_FLAG" (at 30.0 42.0 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at 30.0 40.0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(pin "1" (uuid "{u()}"))
\t)''')
    labels.append('\t(global_label "VCC_5V_PROT" (shape passive) (at 30.0 40.0 180) (effects (font (size 1.27 1.27)) (justify right)))\n')

    # Append all labels
    sch.extend(labels)
    sch.append(')\n')

    content = '\n'.join(sch)
    with open(SCH_PATH, 'w') as f:
        f.write(content)
    print(f'Successfully wrote {SCH_PATH} with {len(comps)} components.')

if __name__ == '__main__':
    generate_schematic()
