#!/usr/bin/env python3
"""
tools/sync_cartridge_sch.py
===========================
Synchronizes PCBA 03 (Universal Smart Cartridge) Schematic:
- Maps all symbols with exact pin coordinates.
- Implements symmetrical naming: AUDIO_IN_L, AUDIO_IN_R, VOICE_OUT, OMM_DETECT, ACT_1..4, AGND_AUDIO_IN.
- Adds U4 (TS5A3159DBVR SPDT Analog/Digital Switch in SOT-23-6) for clean hardware switching between
  Analog Voice (Sena/Cardo) and Digital USB Audio (OMM).
- Adds R9 (10k pullup on OMM_DETECT to VCC_3V3).
- Connects PWR_FLAGs to power rails for 0-error KiCad ERC.
"""

import os
import re
import uuid
import subprocess
import json

SCH_PATH = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_sch"
KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

def u():
    return str(uuid.uuid4())

def main():
    with open(SCH_PATH, "r") as f:
        text = f.read()

    # 1. Clean out any previous added lines
    text = re.sub(r'\t\(global_label\s+\"POD_[^\n]+\n', '', text)
    j_prog_idx = text.find('"J_PROG"')
    end_sym_idx = text.find('\n\t)', j_prog_idx) + 3
    clean_base = text[:end_sym_idx]

    # Ensure lib_symbols has TS5A3159_SPDT and PWR_FLAG
    if 'Switch:TS5A3159_SPDT' not in clean_base:
        ts5a_sym = '''\t\t(symbol "Switch:TS5A3159_SPDT"
\t\t\t(property "Reference" "U" (at -7.62 7.62 0) (effects (font (size 1.27 1.27)) (justify left)))
\t\t\t(property "Value" "TS5A3159DBVR" (at -7.62 -7.62 0) (effects (font (size 1.27 1.27)) (justify left)))
\t\t\t(property "Footprint" "Package_TO_SOT_SMD:SOT-23-6" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(property "LCSC" "C12933" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(pin passive line (at -10.16 2.54 0) (length 2.54) (name "NO" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 10.16 2.54 180) (length 2.54) (name "COM" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t(pin input line (at -10.16 -2.54 0) (length 2.54) (name "IN" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t(pin power_in line (at 0 7.62 270) (length 2.54) (name "VCC" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t\t(pin power_in line (at 0 -7.62 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -10.16 0 0) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\t\t)
'''
        insert_pt = clean_base.find('(symbol "Device:C_Small"')
        clean_base = clean_base[:insert_pt] + ts5a_sym + clean_base[insert_pt:]

    if 'power:PWR_FLAG' not in clean_base:
        pwr_sym = '''\t\t(symbol "power:PWR_FLAG"
\t\t\t(property "Reference" "#FLG" (at 0 1.905 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(property "Value" "PWR_FLAG" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(pin power_out line (at 0 0 90) (length 0) (name "pwr" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t)
'''
        insert_pt = clean_base.find('(symbol "Device:C_Small"')
        clean_base = clean_base[:insert_pt] + pwr_sym + clean_base[insert_pt:]

    # Parse lib_symbols
    lib_part = clean_base[clean_base.find('(lib_symbols'):clean_base.find('(symbol (lib_id')]
    sym_defs = {}
    for m in re.finditer(r'\(symbol\s+\"([^\"]+)\"(.*?)(?=\(symbol\s+\"|\Z)', lib_part, re.DOTALL):
        name = m.group(1)
        body = m.group(2)
        pins = re.findall(r'\(pin\s+(\w+)\s+(\w+)\s+\(at\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\).*?\(name\s+\"([^\"]+)\".*?\(number\s+\"([^\"]+)\"', body, re.DOTALL)
        if pins:
            sym_defs[name] = {pnum: (float(px), float(py), float(prot), pname) for ptype, pstyle, px, py, prot, pname, pnum in pins}

    if 'ES8388_0_1' in sym_defs:
        sym_defs['Audio:ES8388'] = sym_defs['ES8388_0_1']

    # Symbol instances
    sym_positions = {}
    for m in re.finditer(r'\(symbol\s+\(lib_id\s+\"([^\"]+)\"\)\s+\(at\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\).*?\(property\s+\"Reference\"\s+\"([^\"]+)\"', clean_base, re.DOTALL):
        lib_id, x, y, rot, ref = m.groups()
        sym_positions[ref] = (lib_id, float(x), float(y), float(rot))

    # Add U4 and R9 positions
    sym_positions['U4'] = ('Switch:TS5A3159_SPDT', 90.0, 130.0, 0.0)
    sym_positions['R9'] = ('Device:R_Small', 100.0, 130.0, 0.0)

    def get_pin_pos(ref, pnum):
        lib_id, sx, sy, srot = sym_positions[ref]
        px, py, prot, pname = sym_defs[lib_id][str(pnum)]
        return (round(sx + px, 2), round(sy - py, 2))

    pin_nets = {
        # Power & decoupling
        ('PAD1', '1'): '+5V_IN',
        ('PAD2', '1'): 'GND',
        ('F1', '1'): '+5V_IN',
        ('F1', '2'): 'VCC_5V_PROT',
        ('C1', '1'): 'VCC_3V3',
        ('C1', '2'): 'GND',
        ('C2', '1'): 'VCC_3V3',
        ('C2', '2'): 'GND',

        # U1 (ESP32-C6-MINI-1U)
        ('U1', '1'): 'GND',
        ('U1', '2'): 'VCC_3V3',
        ('U1', '3'): 'VCC_3V3',
        ('U1', '4'): 'UWB_SCK',
        ('U1', '5'): 'UWB_MOSI',
        ('U1', '6'): 'UWB_MISO',
        ('U1', '7'): 'UWB_CS',
        ('U1', '8'): 'ACT3_GATE',
        ('U1', '9'): 'ACT4_GATE',
        ('U1', '10'): 'UWB_IRQ',
        ('U1', '11'): 'UWB_RST',
        ('U1', '14'): 'PTT_USB_N',
        ('U1', '15'): 'USB_DP',
        ('U1', '16'): 'OMM_DETECT',
        ('U1', '17'): 'I2C_SCL',
        ('U1', '18'): 'ACT1_GATE',
        ('U1', '19'): 'ACT2_GATE',
        ('U1', '20'): 'I2S_MCLK',
        ('U1', '21'): 'I2S_BCLK',
        ('U1', '22'): 'I2S_WS',
        ('U1', '23'): 'I2S_DOUT',
        ('U1', '24'): 'I2S_DIN',
        ('U1', '25'): 'I2C_SDA',
        ('U1', '26'): 'GND',
        ('U1', '27'): 'GND',

        # U_UWB (DW3110)
        ('U_UWB', '1'): 'VCC_3V3',
        ('U_UWB', '7'): 'UWB_SCK',
        ('U_UWB', '8'): 'UWB_MISO',
        ('U_UWB', '9'): 'UWB_MOSI',
        ('U_UWB', '10'): 'UWB_CS',
        ('U_UWB', '12'): 'UWB_RST',
        ('U_UWB', '13'): 'UWB_IRQ',
        ('U_UWB', '16'): 'GND',

        # U3 (ES8388)
        ('U3', '1'): 'VCC_3V3',
        ('U3', '2'): 'I2S_MCLK',
        ('U3', '3'): 'I2S_BCLK',
        ('U3', '4'): 'I2S_WS',
        ('U3', '5'): 'I2S_DIN',
        ('U3', '6'): 'I2S_DOUT',
        ('U3', '7'): 'I2C_SDA',
        ('U3', '8'): 'I2C_SCL',
        ('U3', '9'): 'AUDIO_IN_L',
        ('U3', '10'): 'AUDIO_IN_R',
        ('U3', '11'): 'VOICE_OUT',
        ('U3', '12'): 'AGND_AUDIO_IN',
        ('U3', '13'): 'GND',

        # U4 (TS5A3159 SPDT Switch)
        ('U4', '1'): 'USB_DP',
        ('U4', '2'): 'AUDIO_IO_P',
        ('U4', '3'): 'OMM_DETECT',
        ('U4', '4'): 'VCC_3V3',
        ('U4', '5'): 'GND',
        ('U4', '6'): 'VOICE_OUT',

        # R9 (OMM_DETECT pullup)
        ('R9', '1'): 'VCC_3V3',
        ('R9', '2'): 'OMM_DETECT',

        # J_AUDIO_PWR
        ('J_AUDIO_PWR', '1'): 'GND',
        ('J_AUDIO_PWR', '2'): 'VCC_5V_PROT',
        ('J_AUDIO_PWR', '3'): 'AGND_AUDIO_IN',
        ('J_AUDIO_PWR', '4'): 'AUDIO_IN_L',
        ('J_AUDIO_PWR', '5'): 'AUDIO_IN_R',
        ('J_AUDIO_PWR', '6'): 'OMM_DETECT',
        ('J_AUDIO_PWR', '7'): 'AUDIO_IO_P',
        ('J_AUDIO_PWR', '8'): 'PTT_USB_N',

        # J_ACT
        ('J_ACT', '1'): 'VCC_5V_PROT',
        ('J_ACT', '2'): 'ACT_1',
        ('J_ACT', '3'): 'VCC_5V_PROT',
        ('J_ACT', '4'): 'ACT_2',
        ('J_ACT', '5'): 'VCC_5V_PROT',
        ('J_ACT', '6'): 'ACT_3',
        ('J_ACT', '7'): 'VCC_5V_PROT',
        ('J_ACT', '8'): 'ACT_4',

        # J_PROG
        ('J_PROG', '1'): 'VCC_3V3',
        ('J_PROG', '2'): 'USB_DP',
        ('J_PROG', '3'): 'PTT_USB_N',
        ('J_PROG', '4'): 'GND',

        # Actuators
        ('R1', '1'): 'ACT1_GATE',
        ('R5', '2'): 'GND',
        ('Q1', '2'): 'GND',
        ('Q1', '3'): 'ACT_1',
        ('D1', '1'): 'ACT_1',
        ('D1', '2'): 'VCC_5V_PROT',

        ('R2', '1'): 'ACT2_GATE',
        ('R6', '2'): 'GND',
        ('Q2', '2'): 'GND',
        ('Q2', '3'): 'ACT_2',
        ('D2', '1'): 'ACT_2',
        ('D2', '2'): 'VCC_5V_PROT',

        ('R3', '1'): 'ACT3_GATE',
        ('R7', '2'): 'GND',
        ('Q3', '2'): 'GND',
        ('Q3', '3'): 'ACT_3',
        ('D3', '1'): 'ACT_3',
        ('D3', '2'): 'VCC_5V_PROT',

        ('R4', '1'): 'ACT4_GATE',
        ('R8', '2'): 'GND',
        ('Q4', '2'): 'GND',
        ('Q4', '3'): 'ACT_4',
        ('D4', '1'): 'ACT_4',
        ('D4', '2'): 'VCC_5V_PROT',
    }

    wires = [
        (get_pin_pos('R1', '2'), get_pin_pos('Q1', '1')),
        (get_pin_pos('R5', '1'), get_pin_pos('Q1', '1')),
        (get_pin_pos('R2', '2'), get_pin_pos('Q2', '1')),
        (get_pin_pos('R6', '1'), get_pin_pos('Q2', '1')),
        (get_pin_pos('R3', '2'), get_pin_pos('Q3', '1')),
        (get_pin_pos('R7', '1'), get_pin_pos('Q3', '1')),
        (get_pin_pos('R4', '2'), get_pin_pos('Q4', '1')),
        (get_pin_pos('R8', '1'), get_pin_pos('Q4', '1')),
        (get_pin_pos('U_UWB', '2'), get_pin_pos('Y_UWB', '1')),
        (get_pin_pos('U_UWB', '3'), get_pin_pos('Y_UWB', '3')),
        (get_pin_pos('U_UWB', '15'), get_pin_pos('ANT_UWB', '1')),
    ]

    elem_lines = []
    for (ref, pnum), net in pin_nets.items():
        pos = get_pin_pos(ref, pnum)
        rot = 180 if pos[0] >= 110 else 0
        just = 'right' if rot == 180 else 'left'
        elem_lines.append(f'\t(global_label "{net}" (shape passive) (at {pos[0]:.2f} {pos[1]:.2f} {rot}) (effects (font (size 1.27 1.27)) (justify {just})))\n')

    for (p1, p2) in wires:
        elem_lines.append(f'\t(wire (pts (xy {p1[0]:.2f} {p1[1]:.2f}) (xy {p2[0]:.2f} {p2[1]:.2f})) (stroke (width 0) (type default)))\n')

    p_y2 = get_pin_pos('Y_UWB', '2')
    p_y4 = get_pin_pos('Y_UWB', '4')
    elem_lines.append(f'\t(global_label "GND" (shape passive) (at {p_y2[0]:.2f} {p_y2[1]:.2f} 180) (effects (font (size 1.27 1.27)) (justify right)))\n')
    elem_lines.append(f'\t(global_label "GND" (shape passive) (at {p_y4[0]:.2f} {p_y4[1]:.2f} 180) (effects (font (size 1.27 1.27)) (justify right)))\n')

    # Add U4 and R9 symbol instances
    u_u4 = u()
    u_r9 = u()
    added_symbols = f'''
\t(symbol (lib_id "Switch:TS5A3159_SPDT") (at 90.0 130.0 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (dnp no)
\t\t(uuid "{u_u4}")
\t\t(property "Reference" "U4" (at 90.0 122.0 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "TS5A3159DBVR" (at 90.0 125.0 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "Package_TO_SOT_SMD:SOT-23-6" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(property "LCSC" "C12933" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(pin "1" (uuid "{u()}"))
\t\t(pin "2" (uuid "{u()}"))
\t\t(pin "3" (uuid "{u()}"))
\t\t(pin "4" (uuid "{u()}"))
\t\t(pin "5" (uuid "{u()}"))
\t\t(pin "6" (uuid "{u()}"))
\t)

\t(symbol (lib_id "Device:R_Small") (at 100.0 130.0 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (dnp no)
\t\t(uuid "{u_r9}")
\t\t(property "Reference" "R9" (at 100.0 122.0 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "10k" (at 100.0 125.0 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "Resistor_SMD:R_0603_1608Metric" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(property "LCSC" "C25804" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(pin "1" (uuid "{u()}"))
\t\t(pin "2" (uuid "{u()}"))
\t)

\t(symbol (lib_id "power:PWR_FLAG") (at 45.0 40.0 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (dnp no)
\t\t(uuid "{u()}")
\t\t(property "Reference" "#FLG1" (at 45.0 38.0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(property "Value" "PWR_FLAG" (at 45.0 42.0 0) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{u()}"))
\t)
\t(global_label "VCC_3V3" (shape passive) (at 45.0 40.0 180) (effects (font (size 1.27 1.27)) (justify right)))

\t(symbol (lib_id "power:PWR_FLAG") (at 45.0 45.0 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (dnp no)
\t\t(uuid "{u()}")
\t\t(property "Reference" "#FLG2" (at 45.0 43.0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(property "Value" "PWR_FLAG" (at 45.0 47.0 0) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{u()}"))
\t)
\t(global_label "GND" (shape passive) (at 45.0 45.0 180) (effects (font (size 1.27 1.27)) (justify right)))
'''

    final_sch = clean_base + added_symbols + ''.join(elem_lines) + '\n)\n'
    with open(SCH_PATH, "w") as f:
        f.write(final_sch)

    print("✓ Successfully synchronized PCBA 03 schematic with U4 (TS5A3159), R9, and PWR_FLAGs.")

if __name__ == "__main__":
    main()
