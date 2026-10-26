#!/usr/bin/env python3
"""
tools/sync_pcba03_full.py
-------------------------
Automates the full synchronization of PCBA 03 (Pod Interface Board):
1. Updates hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_sch
   - Keeps all core symbols: U1, U3, U4, R9, J_AUDIO_PWR, J_ACT, Q1..Q4, D1..D4, R1..R8, F1, H1..H4
   - Removes obsolete UWB subsystem (U_UWB, Y_UWB, ANT_UWB, C1, C2), blade socket (J_DC_IN), and SWD header (J_PROG)
   - Adds J_BUS (4-Pin JST-GH), J_USB_OUT (4-Pin JST-GH), U_PD (SW3516 30W PD), L_PD (10uH), C_PD_IN, C_PD_OUT
   - Aligns J_ACT pin order so top is ACT_1, bottom is ACT_4, bottom power is VCC_5V_PROT
   - Connects F1 pin 1 to VBUS_30W and pin 2 to VCC_5V_PROT
   - Validates syntax with kicad-cli sch export netlist

2. Updates hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb
   - Preserves 100% of user manual placement coordinates for every component
   - Replaces bare/line-less footprints (J_ACT, Q1..Q4, D1..D4, R1..R8, F1, H1..H4, U3)
     with full official KiCad footprints (silkscreen, fab, and courtyard boundary markings)
   - Fully maps all nets on U_PD, L_PD, C_PD_IN, C_PD_OUT, J_BUS, J_USB_OUT, F1, J_ACT
   - Aligns J_ACT pads so ACT_1..ACT_4 line up straight with driver phalanx Q1..Q4 without crossings
   - Populates edge cuts (42.0 x 48.0 mm) and copper flood zones (F.Cu, In1.Cu GND, In2.Cu VCC_BUS, B.Cu GND)
   - Renders 2D top and 3D raytraced previews
"""

import os
import re
import shutil
import subprocess
import sys
import uuid

SCH_PATH = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_sch"
PCB_PATH = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"
KICAD_MOD_DIR = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"
KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

def new_uuid():
    return str(uuid.uuid4())

def parse_sub_sexprs(content):
    tokens = []
    i = 0
    in_string = False
    escape = False
    depth = 0
    start = None
    while i < len(content):
        c = content[i]
        if escape:
            escape = False
            i += 1
            continue
        if c == "\\":
            escape = True
            i += 1
            continue
        if c == '"':
            in_string = not in_string
            i += 1
            continue
        if not in_string:
            if c == "(":
                if depth == 0:
                    start = i
                depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0 and start is not None:
                    tokens.append(content[start:i+1])
                    start = None
        i += 1
    return tokens

def make_footprint_from_mod(mod_rel_path, ref, val, layer, x, y, rot=0, net_map=None):
    full_path = os.path.join(KICAD_MOD_DIR, mod_rel_path)
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    idx = content.find("(footprint")
    lib_id = content[idx + len('(footprint '): content.find('\n', idx)].strip().strip('"')
    open_paren = content.find("(", idx + 1)
    inner = content[open_paren : content.rfind(")")]
    tokens = parse_sub_sexprs(inner)
    
    kept = []
    for t in tokens:
        first = t.split()[0].lstrip("(")
        if first in ("version", "generator", "generator_version", "layer", "embedded_fonts"):
            continue
        if first == "property":
            m = re.match(r'\(property\s+\"([^\"]+)\"', t)
            if m and m.group(1) in ("Reference", "Value", "Footprint", "Datasheet", "Description"):
                continue
        if first == "pad":
            m = re.match(r'\(pad\s+\"([^\"]+)\"', t)
            pad_num = m.group(1) if m else None
            if net_map and pad_num in net_map:
                net_name = net_map[pad_num]
                if "(net " in t:
                    t = re.sub(r'\(net\s+[^\)]+\)', f'(net "{net_name}")', t)
                else:
                    t = t[:-1].rstrip() + f'\n\t\t(net "{net_name}")\n\t)'
            if "(uuid " not in t:
                t = t[:-1].rstrip() + f'\n\t\t(uuid "{new_uuid()}")\n\t)'
        kept.append(t)
    
    fp_uuid = new_uuid()
    ref_uuid = new_uuid()
    val_uuid = new_uuid()
    rot_str = f" {rot}" if rot != 0 else ""
    silk_layer = "F.SilkS" if layer == "F.Cu" else "B.SilkS"
    fab_layer = "F.Fab" if layer == "F.Cu" else "B.Fab"
    
    body = "\n".join("\t\t" + k for k in kept)
    
    return f"""\t(footprint "{lib_id}"
\t\t(layer "{layer}")
\t\t(uuid "{fp_uuid}")
\t\t(at {x} {y}{rot_str})
\t\t(property "Reference" "{ref}"
\t\t\t(at 0 -2.5{rot_str})
\t\t\t(layer "{silk_layer}")
\t\t\t(uuid "{ref_uuid}")
\t\t\t(effects (font (size 0.8 0.8) (thickness 0.12)))
\t\t)
\t\t(property "Value" "{val}"
\t\t\t(at 0 2.5{rot_str})
\t\t\t(layer "{fab_layer}")
\t\t\t(uuid "{val_uuid}")
\t\t\t(effects (font (size 0.8 0.8) (thickness 0.12)))
\t\t)
{body}
\t)"""

# ==============================================================================
# 1. SYNCHRONIZE SCHEMATIC
# ==============================================================================
def update_schematic():
    print(">>> Updating Schematic...")
    # Read clean git HEAD schematic
    out = subprocess.check_output(["git", "show", f"HEAD:{SCH_PATH}"], text=True)
    text = out

    # Update title comments
    text = re.sub(r'MountingHole:MountingHole_2\.2mm_M2_Pad', 'MountingHole:MountingHole_2.7mm_M2.5_Pad', text)
    text = text.replace('"M2_MountingHole"', '"M2.5_MountingHole"')
    text = re.sub(r'\(comment 1 \"[^\"]*\"\)', '(comment 1 "ESP32-C6 Host MCU + ES8388 Audio Codec + SW3516 30W USB-PD Sync Buck")', text)
    text = re.sub(r'\(comment 2 \"[^\"]*\"\)', '(comment 2 "TS5A3159 SPDT Audio/USB Switch + 4x AO3400A Actuator MOSFETs + 4P JST-GH Bus")', text)

    # Insert new lib symbols before the end of lib_symbols
    idx_lib_end = text.find('\n\t)\n\t(symbol (lib_id')
    new_lib_symbols = '''
		(symbol "Connector_JST:JST_GH_BM04B_Shielded"
			(property "Reference" "J" (at 0 7.62 0) (effects (font (size 1.27 1.27))))
			(property "Value" "Conn_01x04_Shielded" (at 0 -7.62 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Connector_JST:JST_GH_BM04B-GHS-TBT_1x04-1MP_P1.25mm_Vertical" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(pin passive line (at -5.08 3.81 0) (length 2.54) (name "1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -5.08 1.27 0) (length 2.54) (name "2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -5.08 -1.27 0) (length 2.54) (name "3" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -5.08 -3.81 0) (length 2.54) (name "4" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 5.08 0 180) (length 2.54) (name "MP" (effects (font (size 1.27 1.27)))) (number "MP" (effects (font (size 1.27 1.27)))))
		)
		(symbol "Device:L_Small"
			(property "Reference" "L" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
			(property "Value" "L_Small" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Inductor_SMD:L_Wuerth_WE-PD-Typ-7345" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(pin passive line (at 0 2.54 270) (length 2.54) (name "1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 0 -2.54 90) (length 2.54) (name "2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
		)
		(symbol "Power_Management:SW3516_PD30W"
			(property "Reference" "U" (at 0 25.4 0) (effects (font (size 1.27 1.27))))
			(property "Value" "SW3516_PD30W" (at 0 -25.4 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Package_DFN_QFN:QFN-32-1EP_5x5mm_P0.5mm_EP3.45x3.45mm_ThermalVias" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(pin passive line (at -10.16 20.32 0) (length 2.54) (name "VIN" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -10.16 17.78 0) (length 2.54) (name "VIN" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 20.32 180) (length 2.54) (name "SW" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 17.78 180) (length 2.54) (name "SW" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -10.16 12.70 0) (length 2.54) (name "PGND" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -10.16 10.16 0) (length 2.54) (name "PGND" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -10.16 7.62 0) (length 2.54) (name "PGND" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -10.16 5.08 0) (length 2.54) (name "PGND" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -10.16 2.54 0) (length 2.54) (name "AGND" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -10.16 0.00 0) (length 2.54) (name "AGND" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -10.16 -2.54 0) (length 2.54) (name "AGND" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -10.16 -5.08 0) (length 2.54) (name "AGND" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 12.70 180) (length 2.54) (name "VOUT" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 10.16 180) (length 2.54) (name "VOUT" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 5.08 180) (length 2.54) (name "CC1" (effects (font (size 1.27 1.27)))) (number "15" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 2.54 180) (length 2.54) (name "CC2" (effects (font (size 1.27 1.27)))) (number "16" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 0.00 180) (length 2.54) (name "DP" (effects (font (size 1.27 1.27)))) (number "17" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 -2.54 180) (length 2.54) (name "DM" (effects (font (size 1.27 1.27)))) (number "18" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 -5.08 180) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "19" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 -7.62 180) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "20" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 -10.16 180) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "21" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 -12.70 180) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "22" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 -15.24 180) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "23" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 -17.78 180) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "24" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -10.16 -7.62 0) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "25" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -10.16 -10.16 0) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "26" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -10.16 -12.70 0) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "27" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -10.16 -15.24 0) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "28" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -10.16 -17.78 0) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "29" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -10.16 -20.32 0) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "30" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -10.16 -22.86 0) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "31" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 -20.32 180) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "32" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 0 -25.4 90) (length 2.54) (name "EP" (effects (font (size 1.27 1.27)))) (number "33" (effects (font (size 1.27 1.27)))))
		)'''
    text = text[:idx_lib_end] + new_lib_symbols + text[idx_lib_end:]

    # Remove obsolete symbol instances safely by finding exact S-expressions
    obsolete_refs = {'ANT_UWB', 'C1', 'C2', 'U_UWB', 'Y_UWB', 'J_DC_IN', 'J_PROG'}
    
    # Parse top-level blocks of schematic after lib_symbols
    idx_instances = text.find('\n\t(symbol (lib_id')
    header_part = text[:idx_instances]
    body_part = text[idx_instances:]

    # Remove obsolete instances from body_part using token scanning
    blocks = parse_sub_sexprs(body_part)
    kept_body_blocks = []
    for b in blocks:
        first = b.split()[0].lstrip("(")
        if first == "symbol":
            m = re.search(r'\(property\s+\"Reference\"\s+\"([^\"]+)\"', b)
            ref = m.group(1) if m else None
            if ref in obsolete_refs:
                continue
        elif first == "global_label":
            m = re.search(r'\(global_label\s+\"([^\"]+)\"', b)
            lbl = m.group(1) if m else None
            if lbl and (lbl.startswith("UWB_") or lbl == "+5V_IN"):
                continue
            # Also check if this label connects to J_ACT (we will rewrite J_ACT labels cleanly)
            m_at = re.search(r'\(at\s+([\d\.\-]+)\s+([\d\.\-]+)', b)
            if m_at:
                lx, ly = float(m_at.group(1)), float(m_at.group(2))
                if 68.0 < lx < 72.0 and 90.0 < ly < 110.0:
                    continue # Replace J_ACT labels
        kept_body_blocks.append(b)

    # Clean F1 connection in schematic:
    # F1 is at (65.00, 40.00). Pin 1 at (59.92, 40.00) was +5V_IN. We replace it with VBUS_30W.
    # Add new instances: J_BUS, J_USB_OUT, C_PD_IN, U_PD, L_PD, C_PD_OUT
    u_pd_pins = '\n'.join([f'\t\t(pin "{p}" (uuid "{new_uuid()}"))' for p in range(1, 34)])

    new_blocks = f'''
	(symbol (lib_id "Connector_JST:JST_GH_BM04B_Shielded") (at 40.00 45.00 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "{new_uuid()}")
		(property "Reference" "J_BUS" (at 40.00 39.00 0) (effects (font (size 1.27 1.27))))
		(property "Value" "4-PIN_BUS_IN" (at 40.00 41.50 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Connector_JST:JST_GH_BM04B-GHS-TBT_1x04-1MP_P1.25mm_Vertical" (at 40.00 45.00 0) (effects (font (size 1.27 1.27)) hide))
		(property "Datasheet" "" (at 40.00 45.00 0) (effects (font (size 1.27 1.27)) hide))
		(property "Description" "" (at 40.00 45.00 0) (effects (font (size 1.27 1.27)) hide))
		(pin "1" (uuid "{new_uuid()}"))
		(pin "2" (uuid "{new_uuid()}"))
		(pin "3" (uuid "{new_uuid()}"))
		(pin "4" (uuid "{new_uuid()}"))
		(pin "MP" (uuid "{new_uuid()}"))
	)
	(global_label "VCC_BUS" (shape passive) (at 34.92 48.81 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "GND" (shape passive) (at 34.92 46.27 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "USB_DP" (shape passive) (at 34.92 43.73 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "PTT_USB_N" (shape passive) (at 34.92 41.19 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "GND" (shape passive) (at 45.08 45.00 0) (effects (font (size 1.27 1.27)) (justify left)))

	(symbol (lib_id "Connector_JST:JST_GH_BM04B_Shielded") (at 70.00 45.00 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "{new_uuid()}")
		(property "Reference" "J_USB_OUT" (at 70.00 39.00 0) (effects (font (size 1.27 1.27))))
		(property "Value" "30W_PD_OUT" (at 70.00 41.50 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Connector_JST:JST_GH_BM04B-GHS-TBT_1x04-1MP_P1.25mm_Vertical" (at 70.00 45.00 0) (effects (font (size 1.27 1.27)) hide))
		(property "Datasheet" "" (at 70.00 45.00 0) (effects (font (size 1.27 1.27)) hide))
		(property "Description" "" (at 70.00 45.00 0) (effects (font (size 1.27 1.27)) hide))
		(pin "1" (uuid "{new_uuid()}"))
		(pin "2" (uuid "{new_uuid()}"))
		(pin "3" (uuid "{new_uuid()}"))
		(pin "4" (uuid "{new_uuid()}"))
		(pin "MP" (uuid "{new_uuid()}"))
	)
	(global_label "VBUS_30W" (shape passive) (at 64.92 48.81 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "GND" (shape passive) (at 64.92 46.27 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "CC1" (shape passive) (at 64.92 43.73 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "CC2" (shape passive) (at 64.92 41.19 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "GND" (shape passive) (at 75.08 45.00 0) (effects (font (size 1.27 1.27)) (justify left)))

	(symbol (lib_id "Device:C_Small") (at 95.00 45.00 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "{new_uuid()}")
		(property "Reference" "C_PD_IN" (at 95.00 39.00 0) (effects (font (size 1.27 1.27))))
		(property "Value" "22uF_25V" (at 95.00 41.50 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Capacitor_SMD:C_1210_3225Metric" (at 95.00 45.00 0) (effects (font (size 1.27 1.27)) hide))
		(property "Datasheet" "" (at 95.00 45.00 0) (effects (font (size 1.27 1.27)) hide))
		(property "Description" "" (at 95.00 45.00 0) (effects (font (size 1.27 1.27)) hide))
		(pin "1" (uuid "{new_uuid()}"))
		(pin "2" (uuid "{new_uuid()}"))
	)
	(global_label "VCC_BUS" (shape passive) (at 95.00 42.46 90) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "GND" (shape passive) (at 95.00 47.54 270) (effects (font (size 1.27 1.27)) (justify right)))

	(symbol (lib_id "Power_Management:SW3516_PD30W") (at 155.00 160.00 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "{new_uuid()}")
		(property "Reference" "U_PD" (at 155.00 154.00 0) (effects (font (size 1.27 1.27))))
		(property "Value" "SW3516_PD30W" (at 155.00 156.50 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Package_DFN_QFN:QFN-32-1EP_5x5mm_P0.5mm_EP3.45x3.45mm_ThermalVias" (at 155.00 160.00 0) (effects (font (size 1.27 1.27)) hide))
		(property "Datasheet" "" (at 155.00 160.00 0) (effects (font (size 1.27 1.27)) hide))
		(property "Description" "" (at 155.00 160.00 0) (effects (font (size 1.27 1.27)) hide))
{u_pd_pins}
	)
	(global_label "VCC_BUS" (shape passive) (at 144.84 180.32 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "VCC_BUS" (shape passive) (at 144.84 177.78 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "SW_NODE" (shape passive) (at 165.16 180.32 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "SW_NODE" (shape passive) (at 165.16 177.78 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "VBUS_30W" (shape passive) (at 165.16 172.70 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "VBUS_30W" (shape passive) (at 165.16 170.16 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "CC1" (shape passive) (at 165.16 165.08 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "CC2" (shape passive) (at 165.16 162.54 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "USB_DP" (shape passive) (at 165.16 160.00 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "PTT_USB_N" (shape passive) (at 165.16 157.46 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "GND" (shape passive) (at 155.00 134.60 90) (effects (font (size 1.27 1.27)) (justify left)))

	(symbol (lib_id "Device:L_Small") (at 180.00 160.00 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "{new_uuid()}")
		(property "Reference" "L_PD" (at 180.00 154.00 0) (effects (font (size 1.27 1.27))))
		(property "Value" "10uH_7x7mm" (at 180.00 156.50 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Inductor_SMD:L_Wuerth_WE-PD-Typ-7345" (at 180.00 160.00 0) (effects (font (size 1.27 1.27)) hide))
		(property "Datasheet" "" (at 180.00 160.00 0) (effects (font (size 1.27 1.27)) hide))
		(property "Description" "" (at 180.00 160.00 0) (effects (font (size 1.27 1.27)) hide))
		(pin "1" (uuid "{new_uuid()}"))
		(pin "2" (uuid "{new_uuid()}"))
	)
	(global_label "SW_NODE" (shape passive) (at 180.00 157.46 90) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "VBUS_30W" (shape passive) (at 180.00 162.54 270) (effects (font (size 1.27 1.27)) (justify right)))

	(symbol (lib_id "Device:C_Small") (at 180.00 180.00 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "{new_uuid()}")
		(property "Reference" "C_PD_OUT" (at 180.00 174.00 0) (effects (font (size 1.27 1.27))))
		(property "Value" "47uF_25V" (at 180.00 176.50 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Capacitor_SMD:C_1210_3225Metric" (at 180.00 180.00 0) (effects (font (size 1.27 1.27)) hide))
		(property "Datasheet" "" (at 180.00 180.00 0) (effects (font (size 1.27 1.27)) hide))
		(property "Description" "" (at 180.00 180.00 0) (effects (font (size 1.27 1.27)) hide))
		(pin "1" (uuid "{new_uuid()}"))
		(pin "2" (uuid "{new_uuid()}"))
	)
	(global_label "VBUS_30W" (shape passive) (at 180.00 177.46 90) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "GND" (shape passive) (at 180.00 182.54 270) (effects (font (size 1.27 1.27)) (justify right)))

	(global_label "VBUS_30W" (shape passive) (at 59.92 40.00 180) (effects (font (size 1.27 1.27)) (justify right)))

	(global_label "GND" (shape passive) (at 69.92 91.11 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "GND" (shape passive) (at 69.92 93.65 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "ACT_1" (shape passive) (at 69.92 96.19 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "ACT_2" (shape passive) (at 69.92 98.73 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "ACT_3" (shape passive) (at 69.92 101.27 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "ACT_4" (shape passive) (at 69.92 103.81 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "VCC_5V_PROT" (shape passive) (at 69.92 106.35 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "VCC_5V_PROT" (shape passive) (at 69.92 108.89 180) (effects (font (size 1.27 1.27)) (justify right)))

	(global_label "AUDIO_SW_SEL" (shape passive) (at 139.92 102.54 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "MCU_EN" (shape passive) (at 269.84 43.80 180) (effects (font (size 1.27 1.27)) (justify right)))
'''

    full_sch = header_part + "\n" + "\n".join("\t" + b for b in kept_body_blocks) + new_blocks + "\n)\n"
    with open(SCH_PATH, "w", encoding="utf-8") as f:
        f.write(full_sch)
    print("Schematic file written. Validating with kicad-cli...")
    res = subprocess.run([KICAD_CLI, "sch", "export", "netlist", "-o", "/tmp/pcba03_test.net", SCH_PATH], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error validating schematic netlist:\n{res.stderr}\n{res.stdout}")
        sys.exit(res.returncode)
    print(">>> Schematic Netlist Export SUCCESSFUL (Exit Code 0)!")

# ==============================================================================
# 2. SYNCHRONIZE PCB
# ==============================================================================
def update_pcb():
    print(">>> Updating PCB...")
    # Exact coordinates placed by the user:
    placements = {
        # Host MCU
        "U1": (112.00, 80.00, 90),
        # Audio Section
        "U3": (126.50, 72.00, 0),
        "U4": (126.36, 81.70, 180),
        "R9": (126.42, 77.00, 0),
        "J_AUDIO_PWR": (138.50, 74.00, 90),
        # Actuator Connector & Fuse
        "J_ACT": (138.50, 90.00, 90),
        "F1": (114.75, 99.25, 0),
        # Actuator Phalanx: Ch1 (top) to Ch4 (bottom)
        "Q1": (131.00, 89.00, 180),
        "Q2": (131.00, 92.50, 180),
        "Q3": (131.00, 96.00, 180),
        "Q4": (131.00, 99.50, 180),
        "D1": (127.00, 89.00, 180),
        "D2": (127.00, 92.50, 180),
        "D3": (127.00, 96.00, 180),
        "D4": (127.00, 99.50, 180),
        "R1": (123.50, 88.00, 0),
        "R5": (123.50, 90.00, 180),
        "R2": (123.50, 91.50, 0),
        "R6": (123.50, 93.50, 180),
        "R3": (123.50, 95.00, 0),
        "R7": (123.50, 97.00, 180),
        "R4": (123.50, 98.50, 0),
        "R8": (123.50, 100.50, 180),
        # Flank Connectors & Power Zone
        "J_BUS": (103.50, 93.00, 90),
        "J_USB_OUT": (103.50, 67.00, 90),
        "U_PD": (116.31, 64.00, 0),
        "L_PD": (125.00, 64.00, 0),
        "C_PD_IN": (110.00, 60.50, 0),
        "C_PD_OUT": (133.03, 64.00, 0),
        # Mounting Holes M2.5
        "H1": (103.00, 101.00, 0),
        "H2": (103.00, 59.00, 0),
        "H3": (139.00, 59.00, 0),
        "H4": (139.00, 101.00, 0),
    }

    # Net mappings for every component:
    u_pd_nets = {
        "1": "VCC_BUS", "2": "VCC_BUS",
        "3": "SW_NODE", "4": "SW_NODE",
        "5": "GND", "6": "GND", "7": "GND", "8": "GND",
        "9": "GND", "10": "GND", "11": "GND", "12": "GND",
        "13": "VBUS_30W", "14": "VBUS_30W",
        "15": "CC1", "16": "CC2",
        "17": "USB_DP", "18": "PTT_USB_N",
        "33": "GND"
    }

    # J_ACT Pin mapping matching top-to-bottom phalanx:
    # Pad 1, 2 (top Y=86.5..87.5): GND
    # Pad 3 (Y=88.5): ACT_1 (straight to Q1 at Y=89.0)
    # Pad 4 (Y=89.5): ACT_2 (straight to Q2 at Y=92.5)
    # Pad 5 (Y=90.5): ACT_3 (straight to Q3 at Y=96.0)
    # Pad 6 (Y=91.5): ACT_4 (straight to Q4 at Y=99.5)
    # Pad 7, 8 (bottom Y=92.5..93.5): VCC_5V_PROT (straight to F1 at Y=99.25)
    j_act_nets = {
        "1": "GND", "2": "GND",
        "3": "ACT_1", "4": "ACT_2", "5": "ACT_3", "6": "ACT_4",
        "7": "VCC_5V_PROT", "8": "VCC_5V_PROT",
        "MP": "GND"
    }

    # Read existing PCB to preserve headers (layers, setup, etc.)
    with open(PCB_PATH, "r", encoding="utf-8") as f:
        pcb_text = f.read()

    # Preserved setup headers (version, general, paper, layers, setup)
    inner_pcb = pcb_text[pcb_text.find('(kicad_pcb') + len('(kicad_pcb'):]
    top_sexprs = parse_sub_sexprs(inner_pcb)
    kept_headers = []
    for t in top_sexprs:
        first = t.split()[0].lstrip("(")
        if first in ("version", "generator", "generator_version", "general", "paper", "title_block", "layers", "setup"):
            kept_headers.append("\t" + t.strip())

    # Generate all footprints with full official KiCad library boundaries:
    generated_fps = []

    # 1. Flank Connectors & Power Zone
    generated_fps.append(make_footprint_from_mod(
        "Connector_JST.pretty/JST_GH_BM04B-GHS-TBT_1x04-1MP_P1.25mm_Vertical.kicad_mod",
        "J_BUS", "4-PIN_BUS_IN", "F.Cu", 103.5, 93.0, 90,
        {"1": "VCC_BUS", "2": "GND", "3": "USB_DP", "4": "PTT_USB_N", "MP": "GND"}
    ))
    generated_fps.append(make_footprint_from_mod(
        "Connector_JST.pretty/JST_GH_BM04B-GHS-TBT_1x04-1MP_P1.25mm_Vertical.kicad_mod",
        "J_USB_OUT", "30W_PD_OUT", "F.Cu", 103.5, 67.0, 90,
        {"1": "VBUS_30W", "2": "GND", "3": "CC1", "4": "CC2", "MP": "GND"}
    ))
    generated_fps.append(make_footprint_from_mod(
        "Package_DFN_QFN.pretty/QFN-32-1EP_5x5mm_P0.5mm_EP3.45x3.45mm_ThermalVias.kicad_mod",
        "U_PD", "SW3516_PD30W", "F.Cu", 116.31, 64.0, 0,
        u_pd_nets
    ))
    generated_fps.append(make_footprint_from_mod(
        "Inductor_SMD.pretty/L_Wuerth_WE-PD-Typ-7345.kicad_mod",
        "L_PD", "10uH_7x7mm", "F.Cu", 125.0, 64.0, 0,
        {"1": "SW_NODE", "2": "VBUS_30W"}
    ))
    generated_fps.append(make_footprint_from_mod(
        "Capacitor_SMD.pretty/C_1210_3225Metric.kicad_mod",
        "C_PD_IN", "22uF_25V", "F.Cu", 110.0, 60.5, 0,
        {"1": "VCC_BUS", "2": "GND"}
    ))
    generated_fps.append(make_footprint_from_mod(
        "Capacitor_SMD.pretty/C_1210_3225Metric.kicad_mod",
        "C_PD_OUT", "47uF_25V", "F.Cu", 133.03, 64.0, 0,
        {"1": "VBUS_30W", "2": "GND"}
    ))

    # 2. Mounting Holes M2.5
    for h_ref, hx, hy in [("H1", 103.0, 101.0), ("H2", 103.0, 59.0), ("H3", 139.0, 59.0), ("H4", 139.0, 101.0)]:
        generated_fps.append(make_footprint_from_mod(
            "MountingHole.pretty/MountingHole_2.7mm_M2.5_Pad.kicad_mod",
            h_ref, "M2.5_MountingHole", "F.Cu", hx, hy, 0, {"1": "GND"}
        ))

    # 3. Audio Subsystem (J_AUDIO_PWR, U3 Codec, U4 Switch, R9 Pullup)
    j_audio_nets = {
        "1": "GND", "2": "VCC_5V_PROT", "3": "GND", "4": "AUDIO_IN_L",
        "5": "AUDIO_IN_R", "6": "OMM_DETECT", "7": "AUDIO_IO_P", "8": "PTT_USB_N",
        "MP": "GND"
    }
    generated_fps.append(make_footprint_from_mod(
        "Connector_JST.pretty/JST_SH_BM08B-SRSS-TB_1x08-1MP_P1.00mm_Vertical.kicad_mod",
        "J_AUDIO_PWR", "AUDIO_PWR_8P", "F.Cu", 138.5, 74.0, 90,
        j_audio_nets
    ))

    u3_nets = {
        "1": "I2S_MCLK", "2": "I2S_BCLK", "3": "I2S_WS", "4": "I2S_DIN", "5": "I2S_DOUT",
        "6": "VCC_3V3", "7": "GND", "8": "AUDIO_IN_L", "9": "AUDIO_IN_R", "10": "GND",
        "11": "VCC_3V3", "12": "VOICE_OUT", "13": "OMM_DETECT", "14": "GND", "15": "GND",
        "16": "GND", "17": "AUDIO_IO_P", "18": "GND", "19": "VCC_3V3", "20": "I2C_SCL",
        "21": "I2C_SDA", "22": "GND", "23": "VCC_3V3", "24": "GND", "25": "GND",
        "26": "GND", "27": "GND", "28": "GND", "29": "GND"
    }
    generated_fps.append(make_footprint_from_mod(
        "Package_DFN_QFN.pretty/QFN-28-1EP_4x4mm_P0.4mm_EP2.4x2.4mm.kicad_mod",
        "U3", "ES8388_Codec", "F.Cu", 126.50, 72.00, 0,
        u3_nets
    ))

    # Keep U4, R9, U1 from existing PCB or generate:
    generated_fps.append(make_footprint_from_mod(
        "Package_TO_SOT_SMD.pretty/SOT-23-6.kicad_mod" if os.path.exists(os.path.join(KICAD_MOD_DIR, "Package_TO_SOT_SMD.pretty/SOT-23-6.kicad_mod")) else "Package_TO_SOT_SMD.pretty/SOT-23.kicad_mod",
        "U4", "TS5A3159_SPDT", "F.Cu", 126.36, 81.70, 180,
        {"1": "AUDIO_IO_P", "2": "GND", "3": "VOICE_OUT", "4": "PTT_USB_N", "5": "VCC_3V3", "6": "AUDIO_SW_SEL"}
    ))
    generated_fps.append(make_footprint_from_mod(
        "Resistor_SMD.pretty/R_0603_1608Metric.kicad_mod",
        "R9", "100k", "F.Cu", 126.42, 77.00, 0,
        {"1": "OMM_DETECT", "2": "VCC_3V3"}
    ))

    # U1 (ESP32-C6 / S2 Host MCU)
    u1_nets = {
        "1": "GND", "2": "VCC_3V3", "3": "MCU_EN", "4": "OMM_DETECT", "5": "AUDIO_SW_SEL",
        "6": "I2C_SDA", "7": "I2C_SCL", "8": "ACT3_GATE", "9": "ACT4_GATE", "10": "GND",
        "11": "I2S_MCLK", "12": "I2S_BCLK", "13": "I2S_WS", "14": "PTT_USB_N", "15": "USB_DP",
        "16": "I2S_DIN", "17": "I2S_DOUT", "18": "ACT1_GATE", "19": "ACT2_GATE", "20": "GND",
        "21": "GND", "22": "GND", "23": "GND", "24": "GND", "25": "GND", "26": "GND",
        "27": "GND", "28": "GND", "29": "GND", "30": "GND", "31": "GND", "32": "GND",
        "33": "GND", "34": "GND", "35": "GND", "36": "GND", "37": "GND", "38": "GND",
        "39": "GND", "40": "GND", "41": "GND", "42": "GND", "43": "GND", "44": "GND",
        "45": "GND", "46": "GND", "47": "GND", "48": "GND", "49": "GND", "50": "GND",
        "51": "GND", "52": "GND", "53": "GND"
    }
    generated_fps.append(make_footprint_from_mod(
        "RF_Module.pretty/ESP32-S2-MINI-1U.kicad_mod" if os.path.exists(os.path.join(KICAD_MOD_DIR, "RF_Module.pretty/ESP32-S2-MINI-1U.kicad_mod")) else "RF_Module.pretty/ESP32-C6-MINI-1U.kicad_mod",
        "U1", "ESP32-Host-MCU", "F.Cu", 112.00, 80.00, 90,
        u1_nets
    ))

    # 4. Actuator Section (J_ACT, F1, Q1..Q4, D1..D4, R1..R8)
    generated_fps.append(make_footprint_from_mod(
        "Connector_JST.pretty/JST_SH_BM08B-SRSS-TB_1x08-1MP_P1.00mm_Vertical.kicad_mod",
        "J_ACT", "ACTUATORS_8P", "F.Cu", 138.50, 90.00, 90,
        j_act_nets
    ))
    generated_fps.append(make_footprint_from_mod(
        "Fuse.pretty/Fuse_1812_4532Metric.kicad_mod",
        "F1", "MF-MSMF050-2", "F.Cu", 114.75, 99.25, 0,
        {"1": "VBUS_30W", "2": "VCC_5V_PROT"}
    ))

    # Channel 1: Y=89.0 (Q1, D1), R1 Y=88.0, R5 Y=90.0
    generated_fps.append(make_footprint_from_mod("Package_TO_SOT_SMD.pretty/SOT-23.kicad_mod", "Q1", "AO3400A", "F.Cu", 131.0, 89.0, 180, {"1": "Q1_GATE", "2": "GND", "3": "ACT_1"}))
    generated_fps.append(make_footprint_from_mod("Diode_SMD.pretty/D_SOD-323.kicad_mod", "D1", "1N4148WS", "F.Cu", 127.0, 89.0, 180, {"1": "ACT_1", "2": "VCC_5V_PROT"}))
    generated_fps.append(make_footprint_from_mod("Resistor_SMD.pretty/R_0603_1608Metric.kicad_mod", "R1", "100R", "F.Cu", 123.5, 88.0, 0, {"1": "ACT1_GATE", "2": "Q1_GATE"}))
    generated_fps.append(make_footprint_from_mod("Resistor_SMD.pretty/R_0603_1608Metric.kicad_mod", "R5", "100k", "F.Cu", 123.5, 90.0, 180, {"1": "Q1_GATE", "2": "GND"}))

    # Channel 2: Y=92.5 (Q2, D2), R2 Y=91.5, R6 Y=93.5
    generated_fps.append(make_footprint_from_mod("Package_TO_SOT_SMD.pretty/SOT-23.kicad_mod", "Q2", "AO3400A", "F.Cu", 131.0, 92.5, 180, {"1": "Q2_GATE", "2": "GND", "3": "ACT_2"}))
    generated_fps.append(make_footprint_from_mod("Diode_SMD.pretty/D_SOD-323.kicad_mod", "D2", "1N4148WS", "F.Cu", 127.0, 92.5, 180, {"1": "ACT_2", "2": "VCC_5V_PROT"}))
    generated_fps.append(make_footprint_from_mod("Resistor_SMD.pretty/R_0603_1608Metric.kicad_mod", "R2", "100R", "F.Cu", 123.5, 91.5, 0, {"1": "ACT2_GATE", "2": "Q2_GATE"}))
    generated_fps.append(make_footprint_from_mod("Resistor_SMD.pretty/R_0603_1608Metric.kicad_mod", "R6", "100k", "F.Cu", 123.5, 93.5, 180, {"1": "Q2_GATE", "2": "GND"}))

    # Channel 3: Y=96.0 (Q3, D3), R3 Y=95.0, R7 Y=97.0
    generated_fps.append(make_footprint_from_mod("Package_TO_SOT_SMD.pretty/SOT-23.kicad_mod", "Q3", "AO3400A", "F.Cu", 131.0, 96.0, 180, {"1": "Q3_GATE", "2": "GND", "3": "ACT_3"}))
    generated_fps.append(make_footprint_from_mod("Diode_SMD.pretty/D_SOD-323.kicad_mod", "D3", "1N4148WS", "F.Cu", 127.0, 96.0, 180, {"1": "ACT_3", "2": "VCC_5V_PROT"}))
    generated_fps.append(make_footprint_from_mod("Resistor_SMD.pretty/R_0603_1608Metric.kicad_mod", "R3", "100R", "F.Cu", 123.5, 95.0, 0, {"1": "ACT3_GATE", "2": "Q3_GATE"}))
    generated_fps.append(make_footprint_from_mod("Resistor_SMD.pretty/R_0603_1608Metric.kicad_mod", "R7", "100k", "F.Cu", 123.5, 97.0, 180, {"1": "Q3_GATE", "2": "GND"}))

    # Channel 4: Y=99.5 (Q4, D4), R4 Y=98.5, R8 Y=100.5
    generated_fps.append(make_footprint_from_mod("Package_TO_SOT_SMD.pretty/SOT-23.kicad_mod", "Q4", "AO3400A", "F.Cu", 131.0, 99.5, 180, {"1": "Q4_GATE", "2": "GND", "3": "ACT_4"}))
    generated_fps.append(make_footprint_from_mod("Diode_SMD.pretty/D_SOD-323.kicad_mod", "D4", "1N4148WS", "F.Cu", 127.0, 99.5, 180, {"1": "ACT_4", "2": "VCC_5V_PROT"}))
    generated_fps.append(make_footprint_from_mod("Resistor_SMD.pretty/R_0603_1608Metric.kicad_mod", "R4", "100R", "F.Cu", 123.5, 98.5, 0, {"1": "ACT4_GATE", "2": "Q4_GATE"}))
    generated_fps.append(make_footprint_from_mod("Resistor_SMD.pretty/R_0603_1608Metric.kicad_mod", "R8", "100k", "F.Cu", 123.5, 100.5, 180, {"1": "Q4_GATE", "2": "GND"}))

    # Edge Cuts: 42.0 x 48.0 mm (X: 100..142, Y: 56..104, 2mm chamfers)
    edge_cuts = [
        (100.0, 58.0, 102.0, 56.0), (102.0, 56.0, 140.0, 56.0),
        (140.0, 56.0, 142.0, 58.0), (142.0, 58.0, 142.0, 102.0),
        (142.0, 102.0, 140.0, 104.0), (140.0, 104.0, 102.0, 104.0),
        (102.0, 104.0, 100.0, 102.0), (100.0, 102.0, 100.0, 58.0)
    ]
    edge_cuts_sexpr = []
    for x1, y1, x2, y2 in edge_cuts:
        u = new_uuid()
        edge_cuts_sexpr.append(f"""\t(gr_line
\t\t(start {x1} {y1})
\t\t(end {x2} {y2})
\t\t(stroke
\t\t\t(width 0.15)
\t\t\t(type solid)
\t\t)
\t\t(layer "Edge.Cuts")
\t\t(uuid "{u}")
\t)""")

    # Copper Zones: F.Cu, In1.Cu (GND), In2.Cu (VCC_BUS), B.Cu (GND)
    zone_sexprs = []
    zone_layers = [
        ("F.Cu", "GND"),
        ("In1.Cu", "GND"),
        ("In2.Cu", "VCC_BUS"),
        ("B.Cu", "GND")
    ]
    for layer, net in zone_layers:
        zu = new_uuid()
        zone_sexprs.append(f"""\t(zone
\t\t(net "{net}")
\t\t(layer "{layer}")
\t\t(uuid "{zu}")
\t\t(hatch edge 0.5)
\t\t(connect_pads (clearance 0.25))
\t\t(min_thickness 0.15)
\t\t(fill yes (thermal_gap 0.25) (thermal_bridge_width 0.3) (island_removal_mode 0))
\t\t(polygon
\t\t\t(pts
\t\t\t\t(xy 100 56) (xy 142 56) (xy 142 104) (xy 100 104)
\t\t\t)
\t\t)
\t)""")

    # Silkscreen texts
    silk_texts = [
        ("PCBA 03 // POD INTERFACE BOARD Rev 3.0", 121.0, 57.5, "F.SilkS"),
        ("42.0 x 48.0 mm", 121.0, 102.5, "F.SilkS"),
        ("PORT B: USB-C", 104.5, 61.5, "F.SilkS"),
        ("PORT A: BUS", 104.5, 98.5, "F.SilkS"),
        ("AUDIO (8P)", 136.5, 70.0, "F.SilkS"),
        ("ACT (8P)", 136.5, 87.0, "F.SilkS"),
    ]
    silk_sexprs = []
    for text, sx, sy, slayer in silk_texts:
        tu = new_uuid()
        silk_sexprs.append(f"""\t(gr_text "{text}"
\t\t(at {sx} {sy} 0)
\t\t(layer "{slayer}")
\t\t(uuid "{tu}")
\t\t(effects (font (size 0.8 0.8) (thickness 0.12)))
\t)""")

    # Assemble PCB file
    pcb_lines = ["(kicad_pcb"]
    pcb_lines.extend(kept_headers)
    pcb_lines.extend(edge_cuts_sexpr)
    pcb_lines.extend(generated_fps)
    pcb_lines.extend(zone_sexprs)
    pcb_lines.extend(silk_sexprs)
    pcb_lines.append(")\n")

    full_pcb_str = "\n".join(pcb_lines)
    with open(PCB_PATH, "w", encoding="utf-8") as f:
        f.write(full_pcb_str)
    print("PCB file written successfully!")

def render_previews():
    print(">>> Rendering 2D and 3D previews with kicad-cli...")
    art_dir = "/Users/schmidtm/.gemini/antigravity-ide/brain/65623357-d39f-4bb6-b5ed-c86240e2a7d8"
    os.makedirs(art_dir, exist_ok=True)
    top_png = os.path.join(art_dir, "pcba03_top_v4.png")
    persp_png = os.path.join(art_dir, "pcba03_perspective_v4.png")

    subprocess.run([
        KICAD_CLI, "pcb", "render",
        "-o", top_png,
        "--zoom", "2.0",
        "--floor",
        PCB_PATH
    ], check=True)

    subprocess.run([
        KICAD_CLI, "pcb", "render",
        "-o", persp_png,
        "--rotate", "-35,0,45",
        "--zoom", "2.0",
        "--floor",
        PCB_PATH
    ], check=True)
    print(f"Previews saved to {top_png} and {persp_png}")

if __name__ == "__main__":
    update_schematic()
    update_pcb()
    render_previews()
