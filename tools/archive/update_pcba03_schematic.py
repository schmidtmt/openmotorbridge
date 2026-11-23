#!/usr/bin/env python3
"""
tools/update_pcba03_schematic.py
--------------------------------
Synchronizes the PCBA 03 Schematic (openmotorbridge_pod_cartridge.kicad_sch)
with the revised PCBA 03 component configuration:
- Keeps all 4 actuator channels (Q1..Q4, D1..D4, R1..R8, F1) and 8-Pin J_ACT intact
- Keeps Audio subsystem (U3 ES8388, U4 TS5A3159, R9, 8-Pin J_AUDIO_PWR) intact
- Updates mounting holes H1..H4 to M2.5
- Removes obsolete UWB circuit (U_UWB, Y_UWB, ANT_UWB, C1, C2), blade socket (J_DC_IN), and SWD header (J_PROG)
- Adds J_BUS (4-Pin JST-GH), J_USB_OUT (4-Pin JST-GH), U_PD (SW3516 30W PD), L_PD (10uH inductor), C_PD_IN, C_PD_OUT
- Validates syntax using kicad-cli sch export netlist
"""

import os
import re
import shutil
import subprocess
import sys
import uuid

SCH_PATH = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_sch"
BAK_PATH = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_sch.bak"
KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

def new_uuid():
    return str(uuid.uuid4())

def run():
    source_file = BAK_PATH if os.path.exists(BAK_PATH) else SCH_PATH
    print(f"Reading {source_file}...")
    with open(source_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Step 1: Update title_block and M2 -> M2.5
    text = re.sub(r'MountingHole:MountingHole_2\.2mm_M2_Pad', 'MountingHole:MountingHole_2.7mm_M2.5_Pad', text)
    text = text.replace('"M2_MountingHole"', '"M2.5_MountingHole"')
    text = re.sub(r'\(comment 1 \"[^\"]*\"\)', '(comment 1 "ESP32-C6 Host MCU + ES8388 Audio Codec + SW3516 30W USB-PD Sync Buck")', text)
    text = re.sub(r'\(comment 2 \"[^\"]*\"\)', '(comment 2 "TS5A3159 SPDT Audio/USB Switch + 4x AO3400A Actuator MOSFETs + 4P JST-GH Bus")', text)

    # Step 2: Remove obsolete symbols from lib_symbols
    obsolete_libs = [
        'Connector:Blade_Slot_Socket_1x02',
        'Connector_Coaxial:U.FL',
        'Device:Crystal_4Pin',
        'RF_Module:DW3110',
        'Connector_PinHeader:PinHeader_1x04'
    ]
    for sym in obsolete_libs:
        text = re.sub(rf'\t\t\(symbol\s+\"{sym}\"[\s\S]*?\n\t\t\)\n', '', text)

    # Step 3: Insert new symbol definitions into lib_symbols
    idx_lib_close = text.find('\n\t)\n\t(symbol (lib_id')
    new_symbols = '''
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
    text = text[:idx_lib_close] + new_symbols + text[idx_lib_close:]

    # Step 4: Remove obsolete symbol instances
    obsolete_syms = ['ANT_UWB', 'Y_UWB', 'U_UWB', 'C1', 'C2', 'J_DC_IN', 'J_PROG']
    for s in obsolete_syms:
        text = re.sub(rf'\t\(symbol\s+\(lib_id\s+\"[^\"]+\"\)[\s\S]*?\(property\s+\"Reference\"\s+\"{s}\"[\s\S]*?\n\t\)\n', '', text)

    # Step 5: Clean obsolete labels
    lines = text.splitlines(keepends=True)
    new_lines = []
    for l in lines:
        if '(global_label "UWB_' in l:
            continue
        if '+5V_IN' in l:
            continue
        new_lines.append(l)
    text = ''.join(new_lines)

    # Step 6: Insert new symbol instances and global labels
    idx_close = text.rfind('\n)')

    u_pd_pin_lines = '\n'.join([f'\t\t(pin "{p}" (uuid "{new_uuid()}"))' for p in range(1, 34)])

    new_instances = f'''
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
	(global_label "USB_DN" (shape passive) (at 34.92 41.19 180) (effects (font (size 1.27 1.27)) (justify right)))
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
{u_pd_pin_lines}
	)
	(global_label "VCC_BUS" (shape passive) (at 144.84 180.32 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "VCC_BUS" (shape passive) (at 144.84 177.78 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "SW_NODE" (shape passive) (at 165.16 180.32 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "SW_NODE" (shape passive) (at 165.16 177.78 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "VBUS_30W" (shape passive) (at 165.16 172.70 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "VBUS_30W" (shape passive) (at 165.16 170.16 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "CC1" (shape passive) (at 165.16 165.08 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "CC2" (shape passive) (at 165.16 162.54 0) (effects (font (size 1.27 1.27)) (justify left)))
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
'''

    text = text[:idx_close] + new_instances + text[idx_close:]

    with open(SCH_PATH, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Successfully updated {SCH_PATH}")

    # Validate with kicad-cli
    print("Validating schematic with kicad-cli sch export netlist...")
    res = subprocess.run([KICAD_CLI, "sch", "export", "netlist", "-o", "/tmp/pcba03_netlist.net", SCH_PATH], capture_output=True, text=True)
    if res.returncode == 0:
        print("Schematic export netlist SUCCESSFUL (exit code 0)!")
    else:
        print(f"Schematic export failed with code {res.returncode}:\n{res.stderr}\n{res.stdout}")
        sys.exit(res.returncode)

if __name__ == "__main__":
    run()
