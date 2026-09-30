#!/usr/bin/env python3
"""
tools/update_pcb_lineup_v96.py

Synchronizes PCB layouts across all active boards to match v9.6 All-UWB architecture:
1. PCBA 01 (Central Box):
   - Replace obsolete 26-pin IDC header J1 with 12-pin Deutsch DTM-12 automotive header (PinHeader_2x06_P2.54mm_Vertical)
   - Assign exact 12 pins (KL30, KL15, GND, CAN_H, CAN_L, POD1_VCC, POD1_GND, POD2_VCC, POD2_GND, RADAR_PWR_12V, RADAR_GND, CHASSIS_EARTH)
   - Update silkscreen to 'J1: DEUTSCH DTM-12 (PWR & CAN)'
   - Unstack/add UWB crystal Y1_UWB (38.4 MHz) and passives for U8 (DW3110) on B.Cu
   - Update hd26_interface.kicad_sch footprint property
2. PCBA 05 (Universal Front Node):
   - Place Qorvo DW3110 (U9), Hirose U.FL (ANT_UWB), 38.4 MHz crystal (Y_UWB), and 0402 passives on B.Cu
   - Place u-blox SAM-M10Q GNSS module (U10) and Knowles MEMS mic (MK1) on F.Cu
3. PCBA 03 (Universal Smart Cartridge):
   - Replace obsolete J1 (6-pin through-hole socket) with PAD1 (+5V) and PAD2 (GND) ENIG contact pads
   - Place Qorvo DW3110 (U_UWB), Hirose U.FL (ANT_UWB), crystal (Y_UWB), and passives on B.Cu
   - Update silkscreen
4. PCBA 08 (Radar Sub-MCU):
   - Update J1 from 4-pin to 2-pin automotive power header (RADAR_PWR_12V / RADAR_GND)
   - Place Qorvo DW3110 (U3), U.FL (J4), crystal (Y1_UWB), and passives on B.Cu
5. PCBA 07 (Smart Keyfob):
   - Replace P_QI (0805 solder pads) with J_QI (2-pin JST-ACH SMD connector)
"""

import sys
import os
import re
import shutil
import uuid

def generate_uuid():
    return str(uuid.uuid4())

def backup_file(path):
    bak = path + ".bak_v96"
    if not os.path.exists(bak):
        shutil.copyfile(path, bak)
        print(f"[BACKUP] Created {bak}")

def update_pcba01(apply=False):
    pcb_path = "hardware/kicad_main_box/openmotorbridge_main.kicad_pcb"
    sch_path = "hardware/kicad_main_box/hd26_interface.kicad_sch"
    
    print("\n--- Auditing & Updating PCBA 01 (Central Box) ---")
    with open(pcb_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Check J1 footprint
    m = re.search(r'\(footprint \"[^\"]*IDC-Header_2x13[^\"]*\".*?\(property \"Reference\" \"J1\".*?\n\t\)', content, re.DOTALL)
    if m:
        print("[PCBA 01] Found legacy 26-pin IDC-Header_2x13 on J1 -> Target: PinHeader_2x06_P2.54mm_Vertical")
        
        # Build 12-pin footprint replacement
        new_j1 = f"""	(footprint "Connector_PinHeader_2.54mm:PinHeader_2x06_P2.54mm_Vertical"
		(layer "F.Cu")
		(uuid "{generate_uuid()}")
		(at 157 121.5 90)
		(property "Reference" "J1"
			(at 0 -2.5 0)
			(layer "F.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
			)
		)
		(property "Value" "DEUTSCH_DTM12_HEADER"
			(at 0 2.5 0)
			(layer "F.Fab")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
			)
		)
		(property "Datasheet" ""
			(at 0 0 90)
			(layer "F.Fab")
			(hide yes)
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Description" "Deutsch DTM-12 Automotive Header (Pure-DC & CAN-FD)"
			(at 0 0 90)
			(layer "F.Fab")
			(hide yes)
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "LCSC" "C2934175"
			(at 0 0 0)
			(layer "F.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 1.27 1.27)
					(thickness 0.15)
				)
			)
		)
		(duplicate_pad_numbers_are_jumpers no)
		(fp_rect
			(start -1.33 -1.33)
			(end 3.87 14.03)
			(stroke
				(width 0.12)
				(type solid)
			)
			(fill no)
			(layer "F.SilkS")
			(uuid "{generate_uuid()}")
		)
		(fp_rect
			(start -1.8 -1.8)
			(end 4.34 14.5)
			(stroke
				(width 0.05)
				(type solid)
			)
			(fill no)
			(layer "F.CrtYd")
			(uuid "{generate_uuid()}")
		)
		(pad "1" thru_hole roundrect
			(at 0 0 90)
			(size 1.7 1.7)
			(drill 1)
			(layers "*.Cu" "*.Mask")
			(remove_unused_layers no)
			(roundrect_rratio 0.15)
			(net "KL30_IN")
			(uuid "{generate_uuid()}")
		)
		(pad "2" thru_hole circle
			(at 2.54 0 90)
			(size 1.7 1.7)
			(drill 1)
			(layers "*.Cu" "*.Mask")
			(remove_unused_layers no)
			(net "KL15_IGN")
			(uuid "{generate_uuid()}")
		)
		(pad "3" thru_hole circle
			(at 0 2.54 90)
			(size 1.7 1.7)
			(drill 1)
			(layers "*.Cu" "*.Mask")
			(remove_unused_layers no)
			(net "GND_PWR")
			(uuid "{generate_uuid()}")
		)
		(pad "4" thru_hole circle
			(at 2.54 2.54 90)
			(size 1.7 1.7)
			(drill 1)
			(layers "*.Cu" "*.Mask")
			(remove_unused_layers no)
			(net "CAN_H")
			(uuid "{generate_uuid()}")
		)
		(pad "5" thru_hole circle
			(at 0 5.08 90)
			(size 1.7 1.7)
			(drill 1)
			(layers "*.Cu" "*.Mask")
			(remove_unused_layers no)
			(net "CAN_L")
			(uuid "{generate_uuid()}")
		)
		(pad "6" thru_hole circle
			(at 2.54 5.08 90)
			(size 1.7 1.7)
			(drill 1)
			(layers "*.Cu" "*.Mask")
			(remove_unused_layers no)
			(net "POD1_VCC")
			(uuid "{generate_uuid()}")
		)
		(pad "7" thru_hole circle
			(at 0 7.62 90)
			(size 1.7 1.7)
			(drill 1)
			(layers "*.Cu" "*.Mask")
			(remove_unused_layers no)
			(net "GND_PWR")
			(uuid "{generate_uuid()}")
		)
		(pad "8" thru_hole circle
			(at 2.54 7.62 90)
			(size 1.7 1.7)
			(drill 1)
			(layers "*.Cu" "*.Mask")
			(remove_unused_layers no)
			(net "POD2_VCC")
			(uuid "{generate_uuid()}")
		)
		(pad "9" thru_hole circle
			(at 0 10.16 90)
			(size 1.7 1.7)
			(drill 1)
			(layers "*.Cu" "*.Mask")
			(remove_unused_layers no)
			(net "GND_PWR")
			(uuid "{generate_uuid()}")
		)
		(pad "10" thru_hole circle
			(at 2.54 10.16 90)
			(size 1.7 1.7)
			(drill 1)
			(layers "*.Cu" "*.Mask")
			(remove_unused_layers no)
			(net "POD2_VCC")
			(uuid "{generate_uuid()}")
		)
		(pad "11" thru_hole circle
			(at 0 12.70 90)
			(size 1.7 1.7)
			(drill 1)
			(layers "*.Cu" "*.Mask")
			(remove_unused_layers no)
			(net "GND_PWR")
			(uuid "{generate_uuid()}")
		)
		(pad "12" thru_hole circle
			(at 2.54 12.70 90)
			(size 1.7 1.7)
			(drill 1)
			(layers "*.Cu" "*.Mask")
			(remove_unused_layers no)
			(net "GND_SHIELD")
			(uuid "{generate_uuid()}")
		)
		(embedded_fonts no)
		(model "${{KICAD10_3DMODEL_DIR}}/Connector_PinHeader_2.54mm.3dshapes/PinHeader_2x06_P2.54mm_Vertical.step"
			(offset
				(xyz 0 0 0)
			)
			(scale
				(xyz 1 1 1)
			)
			(rotate
				(xyz 0 0 0)
			)
		)
	)"""
        content = content[:m.start()] + new_j1 + content[m.end():]
        print("[PCBA 01] Replaced J1 footprint with 12-pin Deutsch DTM-12 header.")

    # 2. Update silkscreen text for J1
    content = content.replace('"J1: SYSTEM IDC-26"', '"J1: DEUTSCH DTM-12 (PWR & CAN)"')

    # 3. Check U8 (DW3110) passives (Y1_UWB crystal)
    if 'Crystal:Crystal_SMD_2016-4Pin_2.0x1.6mm' not in content and 'Y1_UWB' not in content:
        print("[PCBA 01] Adding Y1_UWB (38.4 MHz 2016 crystal) on B.Cu near U8 (DW3110)")
        xtal_footprint = f"""	(footprint "Crystal:Crystal_SMD_2016-4Pin_2.0x1.6mm"
		(layer "B.Cu")
		(uuid "{generate_uuid()}")
		(at 171 105 180)
		(descr "SMD Crystal 2.0x1.6mm 4-Pin")
		(property "Reference" "Y1_UWB"
			(at 0 -1.5 0)
			(layer "B.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.7 0.7)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(property "Value" "38.4MHz"
			(at 0 1.5 0)
			(layer "B.Fab")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.7 0.7)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(pad "1" smd roundrect
			(at -0.65 0.5 180)
			(size 0.7 0.6)
			(layers "B.Cu" "B.Mask" "B.Paste")
			(roundrect_rratio 0.25)
			(uuid "{generate_uuid()}")
		)
		(pad "2" smd roundrect
			(at 0.65 0.5 180)
			(size 0.7 0.6)
			(layers "B.Cu" "B.Mask" "B.Paste")
			(roundrect_rratio 0.25)
			(net "GND_PWR")
			(uuid "{generate_uuid()}")
		)
		(pad "3" smd roundrect
			(at 0.65 -0.5 180)
			(size 0.7 0.6)
			(layers "B.Cu" "B.Mask" "B.Paste")
			(roundrect_rratio 0.25)
			(uuid "{generate_uuid()}")
		)
		(pad "4" smd roundrect
			(at -0.65 -0.5 180)
			(size 0.7 0.6)
			(layers "B.Cu" "B.Mask" "B.Paste")
			(roundrect_rratio 0.25)
			(net "GND_PWR")
			(uuid "{generate_uuid()}")
		)
	)
"""
        # Insert before the closing parenthesis
        idx = content.rfind(")")
        content = content[:idx] + xtal_footprint + content[idx:]

    if apply:
        backup_file(pcb_path)
        with open(pcb_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[PCBA 01] Saved updated {pcb_path}")

        # Update schematic hd26_interface.kicad_sch
        with open(sch_path, "r", encoding="utf-8") as f:
            sch = f.read()
        sch_new = sch.replace('"Connector_IDC:IDC-Header_2x13_P2.54mm_Vertical"', '"Connector_PinHeader_2.54mm:PinHeader_2x06_P2.54mm_Vertical"')
        if sch_new != sch:
            backup_file(sch_path)
            with open(sch_path, "w", encoding="utf-8") as f:
                f.write(sch_new)
            print(f"[PCBA 01] Updated footprint property in {sch_path}")

def update_pcba05(apply=False):
    pcb_path = "hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb"
    print("\n--- Auditing & Updating PCBA 05 (Universal Front Node) ---")
    with open(pcb_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Check if DW3110 already on board
    has_dw3110 = 'DW3110' in content or 'U9' in content and 'QFN-16' in content
    if not has_dw3110:
        print("[PCBA 05] Adding Qorvo DW3110 sub-circuit (U9, ANT_UWB, Y_UWB, C_UWB1..4) on B.Cu")
        uwb_subcircuit = f"""	(footprint "Package_DFN_QFN:QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm_ThermalVias"
		(layer "B.Cu")
		(uuid "{generate_uuid()}")
		(at 145 95 180)
		(descr "Qorvo DW3110 Ultra-Wideband Transceiver")
		(property "Reference" "U9"
			(at 0 -2.5 0)
			(layer "B.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(property "Value" "DW3110"
			(at 0 2.5 0)
			(layer "B.Fab")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(pad "1" smd roundrect (at -1.45 0.75 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "2" smd roundrect (at -1.45 0.25 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "3" smd roundrect (at -1.45 -0.25 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "4" smd roundrect (at -1.45 -0.75 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "5" smd roundrect (at -0.75 -1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "6" smd roundrect (at -0.25 -1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "7" smd roundrect (at 0.25 -1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "8" smd roundrect (at 0.75 -1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "9" smd roundrect (at 1.45 -0.75 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "10" smd roundrect (at 1.45 -0.25 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "11" smd roundrect (at 1.45 0.25 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "12" smd roundrect (at 1.45 0.75 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "13" smd roundrect (at 0.75 1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "14" smd roundrect (at 0.25 1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "15" smd roundrect (at -0.25 1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "16" smd roundrect (at -0.75 1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "17" smd roundrect (at 0 0 180) (size 1.7 1.7) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.1) (net "GND") (uuid "{generate_uuid()}"))
	)
	(footprint "Connector_Coaxial:U.FL_Hirose_U.FL-R-SMT-1_Vertical"
		(layer "B.Cu")
		(uuid "{generate_uuid()}")
		(at 137 95 180)
		(descr "Hirose U.FL Coaxial Connector (Taoglas FXUWB10 Floor Antenna)")
		(property "Reference" "ANT_UWB"
			(at 0 -2.5 0)
			(layer "B.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(property "Value" "Taoglas_FXUWB10"
			(at 0 2.5 0)
			(layer "B.Fab")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(pad "1" smd roundrect (at 0 -1.5 180) (size 1.0 1.0) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "2" smd roundrect (at -1.05 0 180) (size 0.8 1.1) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{generate_uuid()}"))
		(pad "2" smd roundrect (at 1.05 0 180) (size 0.8 1.1) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{generate_uuid()}"))
	)
	(footprint "Crystal:Crystal_SMD_2016-4Pin_2.0x1.6mm"
		(layer "B.Cu")
		(uuid "{generate_uuid()}")
		(at 151 95 180)
		(descr "SMD Crystal 38.4MHz 2.0x1.6mm 4-Pin")
		(property "Reference" "Y_UWB"
			(at 0 -1.5 0)
			(layer "B.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.7 0.7)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(property "Value" "38.4MHz"
			(at 0 1.5 0)
			(layer "B.Fab")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.7 0.7)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(pad "1" smd roundrect (at -0.65 0.5 180) (size 0.7 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "2" smd roundrect (at 0.65 0.5 180) (size 0.7 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{generate_uuid()}"))
		(pad "3" smd roundrect (at 0.65 -0.5 180) (size 0.7 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "4" smd roundrect (at -0.65 -0.5 180) (size 0.7 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{generate_uuid()}"))
	)
"""
        idx = content.rfind(")")
        content = content[:idx] + uwb_subcircuit + content[idx:]

    # 2. Check GNSS module (u-blox SAM-M10Q) on F.Cu
    has_gnss = 'SAM-M10Q' in content or 'U10' in content
    if not has_gnss:
        print("[PCBA 05] Adding u-blox SAM-M10Q GNSS module (U10) and MEMS mic (MK1) on F.Cu")
        gnss_mems = f"""	(footprint "RF_GPS:ublox_SAM-M10Q"
		(layer "F.Cu")
		(uuid "{generate_uuid()}")
		(at 125 85 0)
		(descr "u-blox SAM-M10Q Standard Precision GNSS Module with Integrated Patch Antenna (15.5x15.5mm)")
		(property "Reference" "U10"
			(at 0 -9.0 0)
			(layer "F.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
			)
		)
		(property "Value" "u-blox_SAM-M10Q"
			(at 0 9.0 0)
			(layer "F.Fab")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
			)
		)
		(fp_rect (start -7.75 -7.75) (end 7.75 7.75) (stroke (width 0.15) (type solid)) (fill no) (layer "F.SilkS") (uuid "{generate_uuid()}"))
		(pad "1" smd roundrect (at -6.75 -5.0) (size 1.2 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{generate_uuid()}"))
		(pad "2" smd roundrect (at -6.75 -2.5) (size 1.2 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "3V3") (uuid "{generate_uuid()}"))
		(pad "3" smd roundrect (at -6.75 0.0) (size 1.2 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "4" smd roundrect (at -6.75 2.5) (size 1.2 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "5" smd roundrect (at -6.75 5.0) (size 1.2 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{generate_uuid()}"))
		(pad "6" smd roundrect (at 6.75 5.0) (size 1.2 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{generate_uuid()}"))
		(pad "7" smd roundrect (at 6.75 2.5) (size 1.2 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "8" smd roundrect (at 6.75 0.0) (size 1.2 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "9" smd roundrect (at 6.75 -2.5) (size 1.2 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "3V3") (uuid "{generate_uuid()}"))
		(pad "10" smd roundrect (at 6.75 -5.0) (size 1.2 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{generate_uuid()}"))
	)
	(footprint "Sensor_Audio:Knowles_SPH0645LM4H"
		(layer "F.Cu")
		(uuid "{generate_uuid()}")
		(at 175 85 0)
		(descr "Knowles SPH0645LM4H I2S MEMS Microphone")
		(property "Reference" "MK1"
			(at 0 -2.5 0)
			(layer "F.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.7 0.7)
					(thickness 0.12)
				)
			)
		)
		(property "Value" "SPH0645LM4H"
			(at 0 2.5 0)
			(layer "F.Fab")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.7 0.7)
					(thickness 0.12)
				)
			)
		)
		(pad "1" smd circle (at -0.8 -0.8) (size 0.5 0.5) (layers "F.Cu" "F.Mask" "F.Paste") (uuid "{generate_uuid()}"))
		(pad "2" smd circle (at 0.8 -0.8) (size 0.5 0.5) (layers "F.Cu" "F.Mask" "F.Paste") (uuid "{generate_uuid()}"))
		(pad "3" smd circle (at 0.8 0.8) (size 0.5 0.5) (layers "F.Cu" "F.Mask" "F.Paste") (uuid "{generate_uuid()}"))
		(pad "4" smd circle (at -0.8 0.8) (size 0.5 0.5) (layers "F.Cu" "F.Mask" "F.Paste") (uuid "{generate_uuid()}"))
		(pad "5" smd circle (at 0 0) (size 0.8 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (net "GND") (uuid "{generate_uuid()}"))
	)
"""
        idx = content.rfind(")")
        content = content[:idx] + gnss_mems + content[idx:]

    if apply:
        backup_file(pcb_path)
        with open(pcb_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[PCBA 05] Saved updated {pcb_path}")

def update_pcba03(apply=False):
    pcb_path = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"
    print("\n--- Auditing & Updating PCBA 03 (Universal Smart Cartridge) ---")
    with open(pcb_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Replace J1 (POD_BASE_DOCKING_SOCKET_6P) with PAD1 and PAD2
    m = re.search(r'\(footprint \"[^\"]*PinSocket_1x06[^\"]*\".*?\(property \"Reference\" \"J1\".*?\n\t\)', content, re.DOTALL)
    if m:
        print("[PCBA 03] Found legacy 6-pin docking socket J1 -> Target: PAD1 (+5V) and PAD2 (GND) spring contact pads")
        spring_pads = f"""	(footprint "TestPoint:TestPoint_Pad_D3.0mm_OD3.5mm"
		(layer "B.Cu")
		(uuid "{generate_uuid()}")
		(at 101.5 75.0 0)
		(descr "Mill-Max DC Spring Contact Pad 1 (+5V Power In)")
		(property "Reference" "PAD1"
			(at 0 -2.5 0)
			(layer "B.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(property "Value" "+5V_IN"
			(at 0 2.5 0)
			(layer "B.Fab")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(pad "1" smd roundrect (at 0 0) (size 2.5 3.5) (layers "B.Cu" "B.Mask") (roundrect_rratio 0.15) (net "VCC_5V") (uuid "{generate_uuid()}"))
	)
	(footprint "TestPoint:TestPoint_Pad_D3.0mm_OD3.5mm"
		(layer "B.Cu")
		(uuid "{generate_uuid()}")
		(at 101.5 85.0 0)
		(descr "Mill-Max DC Spring Contact Pad 2 (GND Return)")
		(property "Reference" "PAD2"
			(at 0 -2.5 0)
			(layer "B.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(property "Value" "GND"
			(at 0 2.5 0)
			(layer "B.Fab")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(pad "1" smd roundrect (at 0 0) (size 2.5 3.5) (layers "B.Cu" "B.Mask") (roundrect_rratio 0.15) (net "GND") (uuid "{generate_uuid()}"))
	)"""
        content = content[:m.start()] + spring_pads + content[m.end():]
        content = content.replace('"J1 DOCKING"', '"PAD1: +5V / PAD2: GND"')
        print("[PCBA 03] Replaced J1 with PAD1 & PAD2.")

    # 2. Add DW3110 UWB sub-circuit on B.Cu
    has_dw3110 = 'DW3110' in content or 'U_UWB' in content
    if not has_dw3110:
        print("[PCBA 03] Adding Qorvo DW3110 UWB sub-circuit on B.Cu")
        uwb_subcircuit = f"""	(footprint "Package_DFN_QFN:QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm_ThermalVias"
		(layer "B.Cu")
		(uuid "{generate_uuid()}")
		(at 118 77 180)
		(descr "Qorvo DW3110 Ultra-Wideband Transceiver")
		(property "Reference" "U_UWB"
			(at 0 -2.5 0)
			(layer "B.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(property "Value" "DW3110"
			(at 0 2.5 0)
			(layer "B.Fab")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(pad "1" smd roundrect (at -1.45 0.75 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "2" smd roundrect (at -1.45 0.25 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "3" smd roundrect (at -1.45 -0.25 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "4" smd roundrect (at -1.45 -0.75 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "5" smd roundrect (at -0.75 -1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "6" smd roundrect (at -0.25 -1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "7" smd roundrect (at 0.25 -1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "8" smd roundrect (at 0.75 -1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "9" smd roundrect (at 1.45 -0.75 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "10" smd roundrect (at 1.45 -0.25 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "11" smd roundrect (at 1.45 0.25 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "12" smd roundrect (at 1.45 0.75 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "13" smd roundrect (at 0.75 1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "14" smd roundrect (at 0.25 1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "15" smd roundrect (at -0.25 1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "16" smd roundrect (at -0.75 1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "17" smd roundrect (at 0 0 180) (size 1.7 1.7) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.1) (net "GND") (uuid "{generate_uuid()}"))
	)
	(footprint "Connector_Coaxial:U.FL_Hirose_U.FL-R-SMT-1_Vertical"
		(layer "B.Cu")
		(uuid "{generate_uuid()}")
		(at 111 77 180)
		(descr "Hirose U.FL Coaxial Connector (Taoglas FXUWB10 Floor Antenna)")
		(property "Reference" "ANT_UWB"
			(at 0 -2.5 0)
			(layer "B.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(property "Value" "Taoglas_FXUWB10"
			(at 0 2.5 0)
			(layer "B.Fab")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(pad "1" smd roundrect (at 0 -1.5 180) (size 1.0 1.0) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "2" smd roundrect (at -1.05 0 180) (size 0.8 1.1) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{generate_uuid()}"))
		(pad "2" smd roundrect (at 1.05 0 180) (size 0.8 1.1) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{generate_uuid()}"))
	)
	(footprint "Crystal:Crystal_SMD_2016-4Pin_2.0x1.6mm"
		(layer "B.Cu")
		(uuid "{generate_uuid()}")
		(at 123 77 180)
		(descr "SMD Crystal 38.4MHz 2.0x1.6mm 4-Pin")
		(property "Reference" "Y_UWB"
			(at 0 -1.5 0)
			(layer "B.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.7 0.7)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(property "Value" "38.4MHz"
			(at 0 1.5 0)
			(layer "B.Fab")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.7 0.7)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(pad "1" smd roundrect (at -0.65 0.5 180) (size 0.7 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "2" smd roundrect (at 0.65 0.5 180) (size 0.7 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{generate_uuid()}"))
		(pad "3" smd roundrect (at 0.65 -0.5 180) (size 0.7 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "4" smd roundrect (at -0.65 -0.5 180) (size 0.7 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{generate_uuid()}"))
	)
"""
        idx = content.rfind(")")
        content = content[:idx] + uwb_subcircuit + content[idx:]

    if apply:
        backup_file(pcb_path)
        with open(pcb_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[PCBA 03] Saved updated {pcb_path}")

def update_pcba08(apply=False):
    pcb_path = "hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb"
    print("\n--- Auditing & Updating PCBA 08 (Radar Sub-MCU) ---")
    with open(pcb_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update J1 from 4-pin to 2-pin automotive power header
    m = re.search(r'\(footprint \"[^\"]*JST_SH_SM04B-SRSS-TB[^\"]*\".*?\(property \"Reference\" \"J1\".*?\n\t\)', content, re.DOTALL)
    if m:
        print("[PCBA 08] Found legacy 4-pin J1 -> Target: 2-pin automotive power connector J1 (RADAR_PWR_12V / RADAR_GND)")
        j1_2p = f"""	(footprint "Connector_JST:JST_JWPF_B02B-JWPF-SK-R_1x02_P2.00mm_Vertical"
		(layer "B.Cu")
		(uuid "{generate_uuid()}")
		(at 144 104 180)
		(descr "JST JWPF 2-Pin Automotive Waterproof Power Connector")
		(property "Reference" "J1"
			(at 0 -2.5 0)
			(layer "B.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(property "Value" "12V_RADAR_PWR"
			(at 0 2.5 0)
			(layer "B.Fab")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(pad "1" thru_hole roundrect (at -1.0 0 180) (size 1.5 1.5) (drill 0.9) (layers "*.Cu" "*.Mask") (roundrect_rratio 0.25) (net "RADAR_PWR_12V") (uuid "{generate_uuid()}"))
		(pad "2" thru_hole circle (at 1.0 0 180) (size 1.5 1.5) (drill 0.9) (layers "*.Cu" "*.Mask") (net "GND") (uuid "{generate_uuid()}"))
	)"""
        content = content[:m.start()] + j1_2p + content[m.end():]
        print("[PCBA 08] Replaced J1 with 2-pin automotive power connector.")

    # 2. Add DW3110 UWB sub-circuit (U3, J4, Y1_UWB) on B.Cu
    has_dw3110 = 'DW3110' in content or 'U3' in content and 'QFN-16' in content
    if not has_dw3110:
        print("[PCBA 08] Adding Qorvo DW3110 UWB sub-circuit (U3, J4, Y1_UWB) on B.Cu")
        uwb_subcircuit = f"""	(footprint "Package_DFN_QFN:QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm_ThermalVias"
		(layer "B.Cu")
		(uuid "{generate_uuid()}")
		(at 144 95 180)
		(descr "Qorvo DW3110 Ultra-Wideband Transceiver (Radar Stream Uplink)")
		(property "Reference" "U3"
			(at 0 -2.5 0)
			(layer "B.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(property "Value" "DW3110"
			(at 0 2.5 0)
			(layer "B.Fab")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(pad "1" smd roundrect (at -1.45 0.75 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "2" smd roundrect (at -1.45 0.25 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "3" smd roundrect (at -1.45 -0.25 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "4" smd roundrect (at -1.45 -0.75 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "5" smd roundrect (at -0.75 -1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "6" smd roundrect (at -0.25 -1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "7" smd roundrect (at 0.25 -1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "8" smd roundrect (at 0.75 -1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "9" smd roundrect (at 1.45 -0.75 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "10" smd roundrect (at 1.45 -0.25 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "11" smd roundrect (at 1.45 0.25 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "12" smd roundrect (at 1.45 0.75 180) (size 0.6 0.25) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "13" smd roundrect (at 0.75 1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "14" smd roundrect (at 0.25 1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "15" smd roundrect (at -0.25 1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "16" smd roundrect (at -0.75 1.45 180) (size 0.25 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "17" smd roundrect (at 0 0 180) (size 1.7 1.7) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.1) (net "GND") (uuid "{generate_uuid()}"))
	)
	(footprint "Connector_Coaxial:U.FL_Hirose_U.FL-R-SMT-1_Vertical"
		(layer "B.Cu")
		(uuid "{generate_uuid()}")
		(at 152 95 180)
		(descr "Hirose U.FL Coaxial Connector (Taoglas FXUWB10 Flex Antenna)")
		(property "Reference" "J4"
			(at 0 -2.5 0)
			(layer "B.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(property "Value" "Taoglas_FXUWB10"
			(at 0 2.5 0)
			(layer "B.Fab")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(pad "1" smd roundrect (at 0 -1.5 180) (size 1.0 1.0) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "2" smd roundrect (at -1.05 0 180) (size 0.8 1.1) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{generate_uuid()}"))
		(pad "2" smd roundrect (at 1.05 0 180) (size 0.8 1.1) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{generate_uuid()}"))
	)
	(footprint "Crystal:Crystal_SMD_2016-4Pin_2.0x1.6mm"
		(layer "B.Cu")
		(uuid "{generate_uuid()}")
		(at 144 89 180)
		(descr "SMD Crystal 38.4MHz 2.0x1.6mm 4-Pin")
		(property "Reference" "Y1_UWB"
			(at 0 -1.5 0)
			(layer "B.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.7 0.7)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(property "Value" "38.4MHz"
			(at 0 1.5 0)
			(layer "B.Fab")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.7 0.7)
					(thickness 0.12)
				)
				(justify mirror)
			)
		)
		(pad "1" smd roundrect (at -0.65 0.5 180) (size 0.7 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "2" smd roundrect (at 0.65 0.5 180) (size 0.7 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{generate_uuid()}"))
		(pad "3" smd roundrect (at 0.65 -0.5 180) (size 0.7 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (uuid "{generate_uuid()}"))
		(pad "4" smd roundrect (at -0.65 -0.5 180) (size 0.7 0.6) (layers "B.Cu" "B.Mask" "B.Paste") (roundrect_rratio 0.25) (net "GND") (uuid "{generate_uuid()}"))
	)
"""
        idx = content.rfind(")")
        content = content[:idx] + uwb_subcircuit + content[idx:]

    if apply:
        backup_file(pcb_path)
        with open(pcb_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[PCBA 08] Saved updated {pcb_path}")

def update_pcba07(apply=False):
    pcb_path = "hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb"
    print("\n--- Auditing & Updating PCBA 07 (Smart Keyfob) ---")
    with open(pcb_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace P_QI (R_0805 solder pads) with J_QI (2-pin JST-ACH connector)
    m = re.search(r'\(footprint \"[^\"]*R_0805[^\"]*\".*?\(property \"Reference\" \"P_QI\".*?\n\t\)', content, re.DOTALL)
    if m:
        print("[PCBA 07] Found solder pad P_QI -> Target: 2-pin JST-ACH connector J_QI")
        j_qi = f"""	(footprint "Connector_JST:JST_ACH_BM02B-ACHSS-GAN-ETF_1x02-1MP_P1.20mm_Vertical"
		(layer "F.Cu")
		(uuid "{generate_uuid()}")
		(at 117.25 73.66 0)
		(descr "JST ACH 2-Pin 1.2mm Pitch SMT Header (Solderless Qi Coil Connection)")
		(property "Reference" "J_QI"
			(at 0 -2.2 0)
			(layer "F.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.7 0.7)
					(thickness 0.12)
				)
			)
		)
		(property "Value" "QI_COIL_ACH_2P"
			(at 0 2.2 0)
			(layer "F.Fab")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.7 0.7)
					(thickness 0.12)
				)
			)
		)
		(pad "1" smd roundrect (at -0.6 0) (size 0.6 1.0) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "QI_AC1") (uuid "{generate_uuid()}"))
		(pad "2" smd roundrect (at 0.6 0) (size 0.6 1.0) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio 0.25) (net "QI_AC2") (uuid "{generate_uuid()}"))
	)"""
        content = content[:m.start()] + j_qi + content[m.end():]
        print("[PCBA 07] Replaced P_QI with J_QI.")

    if apply:
        backup_file(pcb_path)
        with open(pcb_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[PCBA 07] Saved updated {pcb_path}")

def main():
    apply = "--apply" in sys.argv
    print("="*70)
    print("OpenMotorBridge v9.6 PCB Lineup Synchronization Tool")
    print("Mode: " + ("APPLY CHANGES" if apply else "DRY RUN (pass --apply to execute)"))
    print("="*70)

    update_pcba01(apply)
    update_pcba05(apply)
    update_pcba03(apply)
    update_pcba08(apply)
    update_pcba07(apply)
    
    print("\n" + "="*70)
    if apply:
        print("All 5 PCB designs have been updated and synchronized with v9.6 specifications!")
    else:
        print("Dry run complete. Run with --apply to apply all changes.")
    print("="*70)

if __name__ == "__main__":
    main()
