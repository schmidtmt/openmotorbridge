#!/usr/bin/env python3
"""
tools/apply_hub_and_c6_update.py
---------------------------------
Applies architectural updates for PCBA 03:
1. Replaces ESP32 module with ESP32-C6-MINI-1 (no U.FL external antenna)
2. Integrates 3-Port USB Hub (CH334 in QFN-16 3x3mm):
   - Upstream: J_BUS (USB_DP, USB_DM)
   - Downstream Port 1: ESP32 Native USB (USB_DP_MCU, USB_DM_MCU)
   - Downstream Port 2: J_USB_OUT (USB_DP_EXT, USB_DM_EXT)
3. Updates J_USB_OUT from 4-pin (BM04B) to 6-pin (BM06B):
   - Pin 1: VBUS_30W (SW3516 PD power up to 30W)
   - Pin 2: GND
   - Pin 3: CC1 (SW3516 Type-C PD handshake)
   - Pin 4: CC2 (SW3516 Type-C PD handshake)
   - Pin 5: USB_DP_EXT (Hub Port 2 D+)
   - Pin 6: USB_DM_EXT (Hub Port 2 D-)
   - Pin MP: GND
4. Corrects J_BUS Pin 4 net from PTT_USB_N to USB_DM
5. Synchronizes schematic and PCB while 100% preserving all user placements & rotations.
"""

import os
import re
import subprocess
import uuid

SCH_PATH = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_sch"
PCB_PATH = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"
KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

def new_uuid():
    return str(uuid.uuid4())

def update_schematic():
    print("Updating schematic...")
    with open(SCH_PATH, "r", encoding="utf-8") as f:
        sch = f.read()

    # 1. Update U1 in schematic to ESP32-C6-MINI-1
    sch = sch.replace('"MCU:ESP32-C6-MINI-1U"', '"MCU:ESP32-C6-MINI-1"')
    sch = sch.replace('"ESP32-C6-MINI-1U"', '"ESP32-C6-MINI-1"')
    sch = sch.replace('"RF_Module:ESP32-S2-MINI-1U"', '"RF_Module:ESP32-C6-MINI-1"')

    # 2. Update J_BUS net: rename PTT_USB_N on J_BUS pin 4 to USB_DM
    sch = sch.replace('(global_label "PTT_USB_N" (shape passive) (at 34.92 41.19 180)',
                      '(global_label "USB_DM" (shape passive) (at 34.92 41.19 180)')

    # 3. Add CH334 USB Hub symbol definition into lib_symbols if not present
    if 'Interface_USB:CH334' not in sch:
        ch334_lib = '''\t(symbol "Interface_USB:CH334"
\t\t(property "Reference" "U" (at 0 15.24 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "CH334U" (at 0 -15.24 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "Package_DFN_QFN:QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(pin power_in line (at 0 12.70 270) (length 2.54) (name "V33" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t(pin power_in line (at 0 -12.70 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t(pin bidirectional line (at -12.70 5.08 0) (length 2.54) (name "UD+" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\t\t(pin bidirectional line (at -12.70 2.54 0) (length 2.54) (name "UD-" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\t\t(pin bidirectional line (at 12.70 5.08 180) (length 2.54) (name "D1+" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
\t\t(pin bidirectional line (at 12.70 2.54 180) (length 2.54) (name "D1-" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
\t\t(pin bidirectional line (at 12.70 -2.54 180) (length 2.54) (name "D2+" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
\t\t(pin bidirectional line (at 12.70 -5.08 180) (length 2.54) (name "D2-" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
\t\t(pin passive line (at 0 -12.70 90) (length 2.54) (name "EP" (effects (font (size 1.27 1.27)))) (number "17" (effects (font (size 1.27 1.27)))))
\t)
'''
        lib_end = sch.find('(symbol "power:PWR_FLAG"')
        if lib_end != -1:
            sch = sch[:lib_end] + ch334_lib + sch[lib_end:]

    # 4. Add U_HUB instance in schematic
    if '"U_HUB"' not in sch:
        uhub_inst = f'''\t(symbol (lib_id "Interface_USB:CH334") (at 40.00 80.00 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (dnp no)
\t\t(uuid "{new_uuid()}")
\t\t(property "Reference" "U_HUB" (at 40.00 74.00 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "CH334U" (at 40.00 76.50 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "Package_DFN_QFN:QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm" (at 40.00 80.00 0) (effects (font (size 1.27 1.27)) hide))
\t\t(pin "1" (uuid "{new_uuid()}"))
\t\t(pin "3" (uuid "{new_uuid()}"))
\t\t(pin "5" (uuid "{new_uuid()}"))
\t\t(pin "6" (uuid "{new_uuid()}"))
\t\t(pin "7" (uuid "{new_uuid()}"))
\t\t(pin "8" (uuid "{new_uuid()}"))
\t\t(pin "9" (uuid "{new_uuid()}"))
\t\t(pin "10" (uuid "{new_uuid()}"))
\t\t(pin "17" (uuid "{new_uuid()}"))
\t)
\t(global_label "VCC_3V3" (shape passive) (at 40.00 67.30 90) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "GND" (shape passive) (at 40.00 92.70 270) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "USB_DP" (shape passive) (at 27.30 74.92 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "USB_DM" (shape passive) (at 27.30 77.46 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "USB_DP_MCU" (shape passive) (at 52.70 74.92 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "USB_DM_MCU" (shape passive) (at 52.70 77.46 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "USB_DP_EXT" (shape passive) (at 52.70 82.54 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "USB_DM_EXT" (shape passive) (at 52.70 85.08 0) (effects (font (size 1.27 1.27)) (justify left)))
'''
        sch = sch + uhub_inst

    # 5. Connect ESP32 U1 pins 14/15 to USB_DM_MCU / USB_DP_MCU
    sch = sch.replace('(global_label "USB_DP" (shape passive) (at 269.84 81.28 180)',
                      '(global_label "USB_DP_MCU" (shape passive) (at 269.84 81.28 180)')
    sch = sch.replace('(global_label "PTT_USB_N" (shape passive) (at 269.84 83.82 180)',
                      '(global_label "USB_DM_MCU" (shape passive) (at 269.84 83.82 180)')

    # 6. Update J_USB_OUT in schematic to 6-pin BM06B
    sch = re.sub(r'\(symbol\s+\(lib_id\s+\"Connector_JST:JST_GH_BM04B_Shielded\"\)\s+\(at\s+70\.00\s+45\.00\s+0\).*?\(pin\s+\"MP\"\s+\(uuid\s+\"[^\"]+\"\)\)\s*\)',
        f'''(symbol (lib_id "Connector_JST:JST_GH_BM06B_Shielded") (at 70.00 45.00 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (dnp no)
\t\t(uuid "{new_uuid()}")
\t\t(property "Reference" "J_USB_OUT" (at 70.00 39.00 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "30W_PD_DATA_OUT" (at 70.00 41.50 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "Connector_JST:JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Vertical" (at 70.00 45.00 0) (effects (font (size 1.27 1.27)) hide))
\t\t(pin "1" (uuid "{new_uuid()}"))
\t\t(pin "2" (uuid "{new_uuid()}"))
\t\t(pin "3" (uuid "{new_uuid()}"))
\t\t(pin "4" (uuid "{new_uuid()}"))
\t\t(pin "5" (uuid "{new_uuid()}"))
\t\t(pin "6" (uuid "{new_uuid()}"))
\t\t(pin "MP" (uuid "{new_uuid()}"))
\t)
\t(global_label "USB_DP_EXT" (shape passive) (at 64.92 38.65 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "USB_DM_EXT" (shape passive) (at 64.92 36.11 180) (effects (font (size 1.27 1.27)) (justify right)))''',
        sch, flags=re.DOTALL)

    with open(SCH_PATH, "w", encoding="utf-8") as f:
        f.write(sch)
    print("Schematic updated successfully!")

def update_pcb():
    print("Updating PCB...")
    with open(PCB_PATH, "r", encoding="utf-8") as f:
        pcb = f.read()

    # 1. Update J_BUS Pin 4 net to USB_DM
    pos_jbus = pcb.find('"J_BUS"')
    start = pcb.rfind('(footprint', 0, pos_jbus)
    depth = 0; end = -1
    for k in range(start, len(pcb)):
        if pcb[k] == '(': depth += 1
        elif pcb[k] == ')':
            depth -= 1
            if depth == 0: end = k+1; break
    jbus_blk = pcb[start:end]
    jbus_blk = jbus_blk.replace('(net "PTT_USB_N")', '(net "USB_DM")')
    pcb = pcb[:start] + jbus_blk + pcb[end:]

    # 2. Update J_USB_OUT to BM06B (6-pin) at exact same position (103.5, 67, 90)
    pos_jusb = pcb.find('"J_USB_OUT"')
    start = pcb.rfind('(footprint', 0, pos_jusb)
    depth = 0; end = -1
    for k in range(start, len(pcb)):
        if pcb[k] == '(': depth += 1
        elif pcb[k] == ')':
            depth -= 1
            if depth == 0: end = k+1; break
    
    # 6-pin JST GH footprint (P1.25mm)
    # Pitch 1.25 mm: pins at -3.125, -1.875, -0.625, 0.625, 1.875, 3.125
    # Pads oriented with angle 90 to prevent shorting!
    bm06b_fp = f'''(footprint "JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Vertical"
\t\t(layer "F.Cu")
\t\t(uuid "{new_uuid()}")
\t\t(at 103.5 67 90)
\t\t(descr "JST GH series connector, BM06B-GHS-TBT (http://www.jst-mfg.com/product/pdf/eng/eGH.pdf)")
\t\t(tags "connector JST GH vertical")
\t\t(property "Reference" "J_USB_OUT" (at 0 -2.5 90) (layer "F.SilkS") (uuid "{new_uuid()}") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "30W_PD_DATA_OUT" (at 0 2.5 90) (layer "F.Fab") (uuid "{new_uuid()}") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Footprint" "Connector_JST:JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Vertical" (at 0 0 90) (layer "F.Fab") (hide yes) (uuid "{new_uuid()}"))
\t\t(attr smd)
\t\t(pad "1" smd roundrect (at -3.125 1.95 90) (size 0.6 1.7) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "VBUS_30W") (uuid "{new_uuid()}"))
\t\t(pad "2" smd roundrect (at -1.875 1.95 90) (size 0.6 1.7) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{new_uuid()}"))
\t\t(pad "3" smd roundrect (at -0.625 1.95 90) (size 0.6 1.7) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "CC1") (uuid "{new_uuid()}"))
\t\t(pad "4" smd roundrect (at 0.625 1.95 90) (size 0.6 1.7) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "CC2") (uuid "{new_uuid()}"))
\t\t(pad "5" smd roundrect (at 1.875 1.95 90) (size 0.6 1.7) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "USB_DP_EXT") (uuid "{new_uuid()}"))
\t\t(pad "6" smd roundrect (at 3.125 1.95 90) (size 0.6 1.7) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "USB_DM_EXT") (uuid "{new_uuid()}"))
\t\t(pad "MP" smd roundrect (at -4.975 -1.4 90) (size 1 2.8) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{new_uuid()}"))
\t\t(pad "MP" smd roundrect (at 4.975 -1.4 90) (size 1 2.8) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{new_uuid()}"))
\t\t(model "${{KICAD10_3DMODEL_DIR}}/Connector_JST.3dshapes/JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Vertical.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))
\t)'''
    pcb = pcb[:start] + bm06b_fp + pcb[end:]

    # 3. Add U_HUB (CH334 in QFN-16 3x3mm)
    if '"U_HUB"' not in pcb:
        ch334_fp = f'''(footprint "QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm"
\t\t(layer "F.Cu")
\t\t(uuid "{new_uuid()}")
\t\t(at 108.5 88 0)
\t\t(descr "QFN, 16 Pin, 3x3mm body, 0.5mm pitch")
\t\t(tags "QFN DFN")
\t\t(property "Reference" "U_HUB" (at 0 -2.5 0) (layer "F.SilkS") (uuid "{new_uuid()}") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "CH334U" (at 0 2.5 0) (layer "F.Fab") (uuid "{new_uuid()}") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(attr smd)
\t\t(pad "1" smd roundrect (at -1.4 0.75) (size 0.8 0.3) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "VCC_3V3") (uuid "{new_uuid()}"))
\t\t(pad "2" smd roundrect (at -1.4 0.25) (size 0.8 0.3) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "VCC_3V3") (uuid "{new_uuid()}"))
\t\t(pad "3" smd roundrect (at -1.4 -0.25) (size 0.8 0.3) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{new_uuid()}"))
\t\t(pad "4" smd roundrect (at -1.4 -0.75) (size 0.8 0.3) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{new_uuid()}"))
\t\t(pad "5" smd roundrect (at -0.75 -1.4 90) (size 0.8 0.3) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "USB_DM") (uuid "{new_uuid()}"))
\t\t(pad "6" smd roundrect (at -0.25 -1.4 90) (size 0.8 0.3) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "USB_DP") (uuid "{new_uuid()}"))
\t\t(pad "7" smd roundrect (at 0.25 -1.4 90) (size 0.8 0.3) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "USB_DM_MCU") (uuid "{new_uuid()}"))
\t\t(pad "8" smd roundrect (at 0.75 -1.4 90) (size 0.8 0.3) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "USB_DP_MCU") (uuid "{new_uuid()}"))
\t\t(pad "9" smd roundrect (at 1.4 -0.75) (size 0.8 0.3) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "USB_DM_EXT") (uuid "{new_uuid()}"))
\t\t(pad "10" smd roundrect (at 1.4 -0.25) (size 0.8 0.3) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "USB_DP_EXT") (uuid "{new_uuid()}"))
\t\t(pad "11" smd roundrect (at 1.4 0.25) (size 0.8 0.3) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{new_uuid()}"))
\t\t(pad "12" smd roundrect (at 1.4 0.75) (size 0.8 0.3) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{new_uuid()}"))
\t\t(pad "13" smd roundrect (at 0.75 1.4 90) (size 0.8 0.3) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{new_uuid()}"))
\t\t(pad "14" smd roundrect (at 0.25 1.4 90) (size 0.8 0.3) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{new_uuid()}"))
\t\t(pad "15" smd roundrect (at -0.25 1.4 90) (size 0.8 0.3) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{new_uuid()}"))
\t\t(pad "16" smd roundrect (at -0.75 1.4 90) (size 0.8 0.3) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "VCC_3V3") (uuid "{new_uuid()}"))
\t\t(pad "17" smd roundrect (at 0 0) (size 1.7 1.7) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{new_uuid()}"))
\t)'''
        # Insert before J_BUS
        pos_ins = pcb.find('"J_BUS"')
        start_ins = pcb.rfind('(footprint', 0, pos_ins)
        pcb = pcb[:start_ins] + ch334_fp + '\n\t' + pcb[start_ins:]

    # 4. Update U1 footprint to ESP32-C6-MINI-1 and map USB pins to USB_DM_MCU / USB_DP_MCU
    pos_u1 = pcb.find('"U1"')
    start = pcb.rfind('(footprint', 0, pos_u1)
    depth = 0; end = -1
    for k in range(start, len(pcb)):
        if pcb[k] == '(': depth += 1
        elif pcb[k] == ')':
            depth -= 1
            if depth == 0: end = k+1; break
    u1_blk = pcb[start:end]
    u1_blk = u1_blk.replace('"ESP32-S2-MINI-1U"', '"ESP32-C6-MINI-1"')
    u1_blk = u1_blk.replace('(net "PTT_USB_N")', '(net "USB_DM_MCU")')
    u1_blk = u1_blk.replace('(net "USB_DP")', '(net "USB_DP_MCU")')
    pcb = pcb[:start] + u1_blk + pcb[end:]

    with open(PCB_PATH, "w", encoding="utf-8") as f:
        f.write(pcb)
    print("PCB updated successfully!")

if __name__ == "__main__":
    update_schematic()
    update_pcb()
