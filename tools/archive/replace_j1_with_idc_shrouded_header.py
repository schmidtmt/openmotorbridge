#!/usr/bin/env python3
"""
tools/replace_j1_with_idc_shrouded_header.py

Replaces J1 on Central Box (PCBA 01) with official Connector_IDC:IDC-Header_2x06_P2.54mm_Vertical.
This is a standard shrouded IDC box header (Wannenstecker) with protective outer housing,
polarization slot (Verpolschutz), and high-reliability through-hole pins matching J3 next to it.
"""

import re
import uuid

def generate_uuid():
    return str(uuid.uuid4())

def main():
    pcb_path = "hardware/kicad_main_box/openmotorbridge_main.kicad_pcb"
    sch_path = "hardware/kicad_main_box/hd26_interface.kicad_sch"
    
    # 1. Update schematic
    with open(sch_path, "r", encoding="utf-8") as f:
        sch_text = f.read()
    sch_text = sch_text.replace(
        'Connector_PinHeader_2.54mm:PinHeader_2x06_P2.54mm_Vertical',
        'Connector_IDC:IDC-Header_2x06_P2.54mm_Vertical'
    )
    with open(sch_path, "w", encoding="utf-8") as f:
        f.write(sch_text)
    print("Updated hd26_interface.kicad_sch footprint to Connector_IDC:IDC-Header_2x06_P2.54mm_Vertical.")

    # 2. Build official IDC-Header_2x06_P2.54mm_Vertical footprint
    idc_j1 = f"""	(footprint "Connector_IDC:IDC-Header_2x06_P2.54mm_Vertical"
		(layer "F.Cu")
		(uuid "{generate_uuid()}")
		(at 157 121.5 90)
		(descr "Through hole IDC box header, 2x06, 2.54mm pitch, DIN 41651 / IEC 60603-13, double rows, shrouded with polarization notch")
		(tags "Through hole vertical IDC box header THT 2x06 2.54mm double row shrouded")
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
		(property "Value" "DEUTSCH_DTM12_IDC_HEADER"
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
		(property "Datasheet" "" (at 0 0 90) (layer "F.Fab") (hide yes) (uuid "{generate_uuid()}") (effects (font (size 1.27 1.27))))
		(property "Description" "Deutsch DTM-12 Breakout Shrouded IDC Box Header (2x06, 2.54mm, DIN 41651)" (at 0 0 90) (layer "F.Fab") (hide yes) (uuid "{generate_uuid()}") (effects (font (size 1.27 1.27))))
		(property "LCSC" "C2934175" (at 0 0 0) (layer "F.SilkS") (uuid "{generate_uuid()}") (effects (font (size 1.27 1.27) (thickness 0.15))))
		(duplicate_pad_numbers_are_jumpers no)
		(fp_line (start -4.68 -0.5) (end -4.68 0.5) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (uuid "{generate_uuid()}"))
		(fp_line (start -4.68 0.5) (end -3.68 0) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (uuid "{generate_uuid()}"))
		(fp_line (start -3.68 0) (end -4.68 -0.5) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (uuid "{generate_uuid()}"))
		(fp_line (start -3.29 -5.21) (end 5.83 -5.21) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (uuid "{generate_uuid()}"))
		(fp_line (start -3.29 4.3) (end -1.98 4.3) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (uuid "{generate_uuid()}"))
		(fp_line (start -3.29 17.91) (end -3.29 -5.21) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (uuid "{generate_uuid()}"))
		(fp_line (start -1.98 -3.91) (end 4.52 -3.91) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (uuid "{generate_uuid()}"))
		(fp_line (start -1.98 4.3) (end -1.98 -3.91) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (uuid "{generate_uuid()}"))
		(fp_line (start -1.98 8.4) (end -3.29 8.4) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (uuid "{generate_uuid()}"))
		(fp_line (start -1.98 16.61) (end -1.98 8.4) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (uuid "{generate_uuid()}"))
		(fp_line (start 4.52 -3.91) (end 4.52 16.61) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (uuid "{generate_uuid()}"))
		(fp_line (start 4.52 16.61) (end -1.98 16.61) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (uuid "{generate_uuid()}"))
		(fp_line (start 5.83 -5.21) (end 5.83 17.91) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (uuid "{generate_uuid()}"))
		(fp_line (start 5.83 17.91) (end -3.29 17.91) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (uuid "{generate_uuid()}"))
		(fp_rect (start -3.68 -5.6) (end 6.22 18.3) (stroke (width 0.05) (type solid)) (fill no) (layer "F.CrtYd") (uuid "{generate_uuid()}"))
		(fp_line (start -3.18 -4.1) (end -2.18 -5.1) (stroke (width 0.1) (type solid)) (layer "F.Fab") (uuid "{generate_uuid()}"))
		(fp_line (start -3.18 4.3) (end -1.98 4.3) (stroke (width 0.1) (type solid)) (layer "F.Fab") (uuid "{generate_uuid()}"))
		(fp_line (start -3.18 17.8) (end -3.18 -4.1) (stroke (width 0.1) (type solid)) (layer "F.Fab") (uuid "{generate_uuid()}"))
		(fp_line (start -2.18 -5.1) (end 5.72 -5.1) (stroke (width 0.1) (type solid)) (layer "F.Fab") (uuid "{generate_uuid()}"))
		(fp_line (start -1.98 -3.91) (end 4.52 -3.91) (stroke (width 0.1) (type solid)) (layer "F.Fab") (uuid "{generate_uuid()}"))
		(fp_line (start -1.98 4.3) (end -1.98 -3.91) (stroke (width 0.1) (type solid)) (layer "F.Fab") (uuid "{generate_uuid()}"))
		(fp_line (start -1.98 8.4) (end -3.18 8.4) (stroke (width 0.1) (type solid)) (layer "F.Fab") (uuid "{generate_uuid()}"))
		(fp_line (start -1.98 16.61) (end -1.98 8.4) (stroke (width 0.1) (type solid)) (layer "F.Fab") (uuid "{generate_uuid()}"))
		(fp_line (start 4.52 -3.91) (end 4.52 16.61) (stroke (width 0.1) (type solid)) (layer "F.Fab") (uuid "{generate_uuid()}"))
		(fp_line (start 4.52 16.61) (end -1.98 16.61) (stroke (width 0.1) (type solid)) (layer "F.Fab") (uuid "{generate_uuid()}"))
		(fp_line (start 5.72 -5.1) (end 5.72 17.8) (stroke (width 0.1) (type solid)) (layer "F.Fab") (uuid "{generate_uuid()}"))
		(fp_line (start 5.72 17.8) (end -3.18 17.8) (stroke (width 0.1) (type solid)) (layer "F.Fab") (uuid "{generate_uuid()}"))
		(fp_text user "${{REFERENCE}}" (at 1.27 6.35 90) (layer "F.Fab") (uuid "{generate_uuid()}") (effects (font (size 1 1) (thickness 0.15))))
		(pad "1" thru_hole roundrect (at 0 0) (size 1.7 1.7) (drill 1) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (roundrect_rratio 0.147059) (net "KL30_IN") (uuid "{generate_uuid()}"))
		(pad "2" thru_hole circle (at 2.54 0) (size 1.7 1.7) (drill 1) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (net "KL15_IGN") (uuid "{generate_uuid()}"))
		(pad "3" thru_hole circle (at 0 2.54) (size 1.7 1.7) (drill 1) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (net "GND_PWR") (uuid "{generate_uuid()}"))
		(pad "4" thru_hole circle (at 2.54 2.54) (size 1.7 1.7) (drill 1) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (net "CAN_H") (uuid "{generate_uuid()}"))
		(pad "5" thru_hole circle (at 0 5.08) (size 1.7 1.7) (drill 1) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (net "CAN_L") (uuid "{generate_uuid()}"))
		(pad "6" thru_hole circle (at 2.54 5.08) (size 1.7 1.7) (drill 1) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (net "POD1_VCC") (uuid "{generate_uuid()}"))
		(pad "7" thru_hole circle (at 0 7.62) (size 1.7 1.7) (drill 1) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (net "GND_PWR") (uuid "{generate_uuid()}"))
		(pad "8" thru_hole circle (at 2.54 7.62) (size 1.7 1.7) (drill 1) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (net "POD2_VCC") (uuid "{generate_uuid()}"))
		(pad "9" thru_hole circle (at 0 10.16) (size 1.7 1.7) (drill 1) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (net "GND_PWR") (uuid "{generate_uuid()}"))
		(pad "10" thru_hole circle (at 2.54 10.16) (size 1.7 1.7) (drill 1) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (net "POD2_VCC") (uuid "{generate_uuid()}"))
		(pad "11" thru_hole circle (at 0 12.7) (size 1.7 1.7) (drill 1) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (net "GND_PWR") (uuid "{generate_uuid()}"))
		(pad "12" thru_hole circle (at 2.54 12.7) (size 1.7 1.7) (drill 1) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (net "GND_SHIELD") (uuid "{generate_uuid()}"))
		(embedded_fonts no)
		(model "${{KICAD10_3DMODEL_DIR}}/Connector_IDC.3dshapes/IDC-Header_2x06_P2.54mm_Vertical.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1 1 1))
			(rotate (xyz 0 0 0))
		)
	)"""

    # 3. Replace J1 footprint in PCB
    with open(pcb_path, "r", encoding="utf-8") as f:
        c = f.read()

    m = re.search(r'\(footprint \"[^\"]*PinHeader_2x06[^\"]*\".*?\(property \"Reference\" \"J1\".*?\n\t\)', c, re.DOTALL)
    if not m:
        m = re.search(r'\(footprint \"[^\"]*IDC-Header_2x06[^\"]*\".*?\(property \"Reference\" \"J1\".*?\n\t\)', c, re.DOTALL)
    
    if m:
        c = c[:m.start()] + idc_j1 + c[m.end():]
        print("Replaced J1 with official shrouded Connector_IDC:IDC-Header_2x06_P2.54mm_Vertical.")
    else:
        print("ERROR: Could not find J1 footprint in PCB!")
        return

    with open(pcb_path, "w", encoding="utf-8") as f:
        f.write(c)

if __name__ == "__main__":
    main()
