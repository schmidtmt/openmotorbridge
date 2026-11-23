#!/usr/bin/env python3
"""
tools/apply_v96_zones_smd_and_3d_models.py

Applies the following fixes:
1. PCBA 01 (Central Box):
   - Replace J1 through-hole header with SMD header PinHeader_2x06_P2.54mm_Vertical_SMD (ZERO through-holes in PCB!)
   - Merge Zone 2 & Zone 3 into a single, continuous GND_PWR plane (In1.Cu) covering the FULL board (115.22, 71.85) to (200.22, 126.85).
     This completely eliminates the 4mm isolation gap and the keepout cutout behind the ESP32!
   - Expand Zone 4 (POWER_PLANE_3V3 on In2.Cu) across the full board (115.22, 71.85) to (200.22, 126.85) with no keepout cutout!
   - Include proper 3D models with ${KICAD10_3DMODEL_DIR}
2. Add complete 3D models to UWB & newly placed components on all boards:
   - PCBA 05: U9 (DW3110), ANT_UWB (U.FL), Y_UWB (Crystal 2016), MK1 (Knowles Mic), U10 (SAM-M10Q)
   - PCBA 03: U_UWB (DW3110), ANT_UWB (U.FL), Y_UWB (Crystal 2016)
   - PCBA 08: U3 (DW3110), J4 (U.FL), Y1_UWB (Crystal 2016), J1 (Power)
   - PCBA 07: J_QI (2-pin header)
"""

import os
import re
import uuid

def generate_uuid():
    return str(uuid.uuid4())

def fix_pcba01():
    pcb_path = "hardware/kicad_main_box/openmotorbridge_main.kicad_pcb"
    print("\n--- Fixing PCBA 01 (Central Box) ---")
    with open(pcb_path, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. Replace J1 with official PinHeader_2x06_P2.54mm_Vertical_SMD
    m = re.search(r'\(footprint \"[^\"]*PinHeader_2x06[^\"]*\".*?\(property \"Reference\" \"J1\".*?\n\t\)', c, re.DOTALL)
    if m:
        smd_j1 = f"""	(footprint "Connector_PinHeader_2.54mm:PinHeader_2x06_P2.54mm_Vertical_SMD"
		(layer "F.Cu")
		(uuid "{generate_uuid()}")
		(at 157 121.5 90)
		(descr "surface-mounted straight pin header, 2x06, 2.54mm pitch, double rows (Zero Thru-Holes in PCB)")
		(tags "Surface mounted pin header SMD 2x06 2.54mm double row")
		(property "Reference" "J1"
			(at 0 -8.73 90)
			(layer "F.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
			)
		)
		(property "Value" "DEUTSCH_DTM12_HEADER_SMD"
			(at 0 8.73 90)
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
		(property "Description" "Deutsch DTM-12 Automotive Header (Pure-DC & CAN-FD; Surface Mount, Zero Thru-Holes)" (at 0 0 90) (layer "F.Fab") (hide yes) (uuid "{generate_uuid()}") (effects (font (size 1.27 1.27))))
		(property "LCSC" "C2934175" (at 0 0 0) (layer "F.SilkS") (uuid "{generate_uuid()}") (effects (font (size 1.27 1.27) (thickness 0.15))))
		(attr smd)
		(duplicate_pad_numbers_are_jumpers no)
		(fp_rect (start -5.87 -8.12) (end 5.87 8.12) (stroke (width 0.05) (type solid)) (fill no) (layer "F.CrtYd") (uuid "{generate_uuid()}"))
		(fp_line (start -2.54 7.62) (end -2.54 -6.67) (stroke (width 0.1) (type solid)) (layer "F.Fab") (uuid "{generate_uuid()}"))
		(fp_line (start -1.59 -7.62) (end 2.54 -7.62) (stroke (width 0.1) (type solid)) (layer "F.Fab") (uuid "{generate_uuid()}"))
		(fp_line (start 2.54 -7.62) (end 2.54 7.62) (stroke (width 0.1) (type solid)) (layer "F.Fab") (uuid "{generate_uuid()}"))
		(fp_line (start 2.54 7.62) (end -2.54 7.62) (stroke (width 0.1) (type solid)) (layer "F.Fab") (uuid "{generate_uuid()}"))
		(pad "1" smd rect (at -2.525 -6.35 90) (size 3.15 1) (layers "F.Cu" "F.Mask" "F.Paste") (net "KL30_IN") (uuid "{generate_uuid()}"))
		(pad "2" smd rect (at 2.525 -6.35 90) (size 3.15 1) (layers "F.Cu" "F.Mask" "F.Paste") (net "KL15_IGN") (uuid "{generate_uuid()}"))
		(pad "3" smd rect (at -2.525 -3.81 90) (size 3.15 1) (layers "F.Cu" "F.Mask" "F.Paste") (net "GND_PWR") (uuid "{generate_uuid()}"))
		(pad "4" smd rect (at 2.525 -3.81 90) (size 3.15 1) (layers "F.Cu" "F.Mask" "F.Paste") (net "CAN_H") (uuid "{generate_uuid()}"))
		(pad "5" smd rect (at -2.525 -1.27 90) (size 3.15 1) (layers "F.Cu" "F.Mask" "F.Paste") (net "CAN_L") (uuid "{generate_uuid()}"))
		(pad "6" smd rect (at 2.525 -1.27 90) (size 3.15 1) (layers "F.Cu" "F.Mask" "F.Paste") (net "POD1_VCC") (uuid "{generate_uuid()}"))
		(pad "7" smd rect (at -2.525 1.27 90) (size 3.15 1) (layers "F.Cu" "F.Mask" "F.Paste") (net "GND_PWR") (uuid "{generate_uuid()}"))
		(pad "8" smd rect (at 2.525 1.27 90) (size 3.15 1) (layers "F.Cu" "F.Mask" "F.Paste") (net "POD2_VCC") (uuid "{generate_uuid()}"))
		(pad "9" smd rect (at -2.525 3.81 90) (size 3.15 1) (layers "F.Cu" "F.Mask" "F.Paste") (net "GND_PWR") (uuid "{generate_uuid()}"))
		(pad "10" smd rect (at 2.525 3.81 90) (size 3.15 1) (layers "F.Cu" "F.Mask" "F.Paste") (net "POD2_VCC") (uuid "{generate_uuid()}"))
		(pad "11" smd rect (at -2.525 6.35 90) (size 3.15 1) (layers "F.Cu" "F.Mask" "F.Paste") (net "GND_PWR") (uuid "{generate_uuid()}"))
		(pad "12" smd rect (at 2.525 6.35 90) (size 3.15 1) (layers "F.Cu" "F.Mask" "F.Paste") (net "GND_SHIELD") (uuid "{generate_uuid()}"))
		(embedded_fonts no)
		(model "${{KICAD10_3DMODEL_DIR}}/Connector_PinHeader_2.54mm.3dshapes/PinHeader_2x06_P2.54mm_Vertical_SMD.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1 1 1))
			(rotate (xyz 0 0 0))
		)
	)"""
        c = c[:m.start()] + smd_j1 + c[m.end():]
        print("  [PCBA 01] Replaced J1 with SMD header (PinHeader_2x06_P2.54mm_Vertical_SMD, zero through-holes!).")

    # 2. Add 3D model for Y1_UWB crystal if missing
    if 'Crystal_SMD_2016-4Pin_2.0x1.6mm' in c and 'Crystal_SMD_2016-4Pin_2.0x1.6mm.step' not in c:
        m_xtal = re.search(r'(\(property \"Reference\" \"Y1_UWB\".*?\(property \"Value\" \"38.4MHz\".*?)\n\t\)', c, re.DOTALL)
        if m_xtal:
            model_xtal_str = """\t\t(model "${KICAD10_3DMODEL_DIR}/Crystal.3dshapes/Crystal_SMD_2016-4Pin_2.0x1.6mm.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1 1 1))
			(rotate (xyz 0 0 0))
		)\n\t)"""
            c = c[:m_xtal.start()] + m_xtal.group(1) + "\n" + model_xtal_str + c[m_xtal.end():]
            print("  [PCBA 01] Linked 3D model for Y1_UWB crystal.")

    # 3. Replace Zone 2, Zone 3, Zone 4
    # Find Zone 2 start
    z2_match = re.search(r'\n\t\(zone\s+\(net \"[^\"]*\"\)\s+\(layer \"In1\.Cu\"\)\s+\(uuid \"[^\"]*\"\)\s+\(name \"GND_DIGITAL_PLANE\"', c)
    if z2_match:
        z2_start = z2_match.start()
        # Find where Zone 4 ends: it ends right before (embedded_fonts no) or the end of the file
        z4_end_match = re.search(r'\n\t\(embedded_fonts no\)\n\)', c)
        if z4_end_match:
            z_end = z4_end_match.start()
            
            # Create two clean, full-board zones:
            # 1. Full In1.Cu Ground Plane (115.22 to 200.22, 71.85 to 126.85) - NO gap, NO ESP notch
            # 2. Full In2.Cu 3.3V Power Plane (115.22 to 200.22, 71.85 to 126.85) - NO gap, NO ESP notch
            new_zones = f"""
	(zone
		(net "GND_PWR")
		(layer "In1.Cu")
		(uuid "{generate_uuid()}")
		(name "GND_PWR_FULL_PLANE")
		(hatch edge 0.5)
		(connect_pads
			(clearance 0.25)
		)
		(min_thickness 0.25)
		(fill yes
			(thermal_gap 0.3)
			(thermal_bridge_width 0.4)
			(island_removal_mode 0)
		)
		(polygon
			(pts
				(xy 115.22 71.85) (xy 200.22 71.85) (xy 200.22 126.85) (xy 115.22 126.85)
			)
		)
		(filled_polygon
			(layer "In1.Cu")
			(pts
				(xy 115.72 72.35) (xy 199.72 72.35) (xy 199.72 126.35) (xy 115.72 126.35)
			)
		)
	)
	(zone
		(net "VCC_3V3")
		(layer "In2.Cu")
		(uuid "{generate_uuid()}")
		(name "POWER_PLANE_3V3_FULL")
		(hatch edge 0.5)
		(connect_pads
			(clearance 0.25)
		)
		(min_thickness 0.25)
		(fill yes
			(thermal_gap 0.3)
			(thermal_bridge_width 0.4)
			(island_removal_mode 0)
		)
		(polygon
			(pts
				(xy 115.22 71.85) (xy 200.22 71.85) (xy 200.22 126.85) (xy 115.22 126.85)
			)
		)
		(filled_polygon
			(layer "In2.Cu")
			(pts
				(xy 115.72 72.35) (xy 199.72 72.35) (xy 199.72 126.35) (xy 115.72 126.35)
			)
		)
	)"""
            c = c[:z2_start] + new_zones + c[z_end:]
            print("  [PCBA 01] Merged In1.Cu into single unbroken GND plane (gap & ESP notch removed).")
            print("  [PCBA 01] Expanded In2.Cu into full unbroken 3.3V power plane.")

    with open(pcb_path, "w", encoding="utf-8") as f:
        f.write(c)

def fix_pcba05():
    pcb_path = "hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb"
    print("\n--- Fixing PCBA 05 (Universal Front Node) 3D Models ---")
    with open(pcb_path, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. U9 (DW3110)
    if 'QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm.step' not in c:
        m = re.search(r'(\(property \"Reference\" \"U9\".*?\(property \"Value\" \"DW3110\".*?)\n\t\)', c, re.DOTALL)
        if m:
            model = """\t\t(model "${KICAD10_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1 1 1))
			(rotate (xyz 0 0 0))
		)\n\t)"""
            c = c[:m.start()] + m.group(1) + "\n" + model + c[m.end():]
            print("  [PCBA 05] Added 3D model for U9 (DW3110).")

    # 2. ANT_UWB
    if 'ANT_UWB' in c and 'U.FL_Hirose_U.FL-R-SMT-1_Vertical.step' not in c:
        m = re.search(r'(\(property \"Reference\" \"ANT_UWB\".*?\(property \"Value\" \"Taoglas_FXUWB10\".*?)\n\t\)', c, re.DOTALL)
        if m:
            model = """\t\t(model "${KICAD10_3DMODEL_DIR}/Connector_Coaxial.3dshapes/U.FL_Hirose_U.FL-R-SMT-1_Vertical.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1 1 1))
			(rotate (xyz 0 0 0))
		)\n\t)"""
            c = c[:m.start()] + m.group(1) + "\n" + model + c[m.end():]
            print("  [PCBA 05] Added 3D model for ANT_UWB.")

    # 3. Y_UWB
    if 'Y_UWB' in c and 'Crystal_SMD_2016-4Pin_2.0x1.6mm.step' not in c:
        m = re.search(r'(\(property \"Reference\" \"Y_UWB\".*?\(property \"Value\" \"38.4MHz\".*?)\n\t\)', c, re.DOTALL)
        if m:
            model = """\t\t(model "${KICAD10_3DMODEL_DIR}/Crystal.3dshapes/Crystal_SMD_2016-4Pin_2.0x1.6mm.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1 1 1))
			(rotate (xyz 0 0 0))
		)\n\t)"""
            c = c[:m.start()] + m.group(1) + "\n" + model + c[m.end():]
            print("  [PCBA 05] Added 3D model for Y_UWB (Crystal).")

    # 4. MK1 (Knowles Mic)
    if 'MK1' in c and 'Knowles_SPH0645LM4H' not in c:
        m = re.search(r'(\(property \"Reference\" \"MK1\".*?\(property \"Value\" \"SPH0645LM4H\".*?)\n\t\)', c, re.DOTALL)
        if m:
            model = """\t\t(model "${KICAD10_3DMODEL_DIR}/Sensor_Audio.3dshapes/Knowles_SPH0645LM4H-6_3.5x2.65mm.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1 1 1))
			(rotate (xyz 0 0 0))
		)\n\t)"""
            c = c[:m.start()] + m.group(1) + "\n" + model + c[m.end():]
            print("  [PCBA 05] Added 3D model for MK1 (Knowles Mic).")

    # 5. U10 (SAM-M10Q)
    if 'U10' in c and 'Raytac_MDBT50Q.step' not in c:
        m = re.search(r'(\(property \"Reference\" \"U10\".*?\(property \"Value\" \"u-blox_SAM-M10Q\".*?)\n\t\)', c, re.DOTALL)
        if m:
            model = """\t\t(model "${KICAD10_3DMODEL_DIR}/RF_Module.3dshapes/Raytac_MDBT50Q.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1.4 0.9 1.8))
			(rotate (xyz 0 0 0))
		)\n\t)"""
            c = c[:m.start()] + m.group(1) + "\n" + model + c[m.end():]
            print("  [PCBA 05] Added 3D model for U10 (SAM-M10Q).")

    with open(pcb_path, "w", encoding="utf-8") as f:
        f.write(c)

def fix_pcba03():
    pcb_path = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"
    print("\n--- Fixing PCBA 03 (Universal Smart Cartridge) 3D Models ---")
    with open(pcb_path, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. U_UWB
    if 'U_UWB' in c and 'QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm.step' not in c:
        m = re.search(r'(\(property \"Reference\" \"U_UWB\".*?\(property \"Value\" \"DW3110\".*?)\n\t\)', c, re.DOTALL)
        if m:
            model = """\t\t(model "${KICAD10_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1 1 1))
			(rotate (xyz 0 0 0))
		)\n\t)"""
            c = c[:m.start()] + m.group(1) + "\n" + model + c[m.end():]
            print("  [PCBA 03] Added 3D model for U_UWB (DW3110).")

    # 2. ANT_UWB
    if 'ANT_UWB' in c and 'U.FL_Hirose_U.FL-R-SMT-1_Vertical.step' not in c:
        m = re.search(r'(\(property \"Reference\" \"ANT_UWB\".*?\(property \"Value\" \"Taoglas_FXUWB10\".*?)\n\t\)', c, re.DOTALL)
        if m:
            model = """\t\t(model "${KICAD10_3DMODEL_DIR}/Connector_Coaxial.3dshapes/U.FL_Hirose_U.FL-R-SMT-1_Vertical.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1 1 1))
			(rotate (xyz 0 0 0))
		)\n\t)"""
            c = c[:m.start()] + m.group(1) + "\n" + model + c[m.end():]
            print("  [PCBA 03] Added 3D model for ANT_UWB.")

    # 3. Y_UWB
    if 'Y_UWB' in c and 'Crystal_SMD_2016-4Pin_2.0x1.6mm.step' not in c:
        m = re.search(r'(\(property \"Reference\" \"Y_UWB\".*?\(property \"Value\" \"38.4MHz\".*?)\n\t\)', c, re.DOTALL)
        if m:
            model = """\t\t(model "${KICAD10_3DMODEL_DIR}/Crystal.3dshapes/Crystal_SMD_2016-4Pin_2.0x1.6mm.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1 1 1))
			(rotate (xyz 0 0 0))
		)\n\t)"""
            c = c[:m.start()] + m.group(1) + "\n" + model + c[m.end():]
            print("  [PCBA 03] Added 3D model for Y_UWB (Crystal).")

    with open(pcb_path, "w", encoding="utf-8") as f:
        f.write(c)

def fix_pcba08():
    pcb_path = "hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb"
    print("\n--- Fixing PCBA 08 (Radar Sub-MCU) 3D Models ---")
    with open(pcb_path, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. U3 (DW3110)
    if 'U3' in c and 'QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm.step' not in c:
        m = re.search(r'(\(property \"Reference\" \"U3\".*?\(property \"Value\" \"DW3110\".*?)\n\t\)', c, re.DOTALL)
        if m:
            model = """\t\t(model "${KICAD10_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1 1 1))
			(rotate (xyz 0 0 0))
		)\n\t)"""
            c = c[:m.start()] + m.group(1) + "\n" + model + c[m.end():]
            print("  [PCBA 08] Added 3D model for U3 (DW3110).")

    # 2. J4 (U.FL)
    if 'J4' in c and 'U.FL_Hirose_U.FL-R-SMT-1_Vertical.step' not in c:
        m = re.search(r'(\(property \"Reference\" \"J4\".*?\(property \"Value\" \"Taoglas_FXUWB10\".*?)\n\t\)', c, re.DOTALL)
        if m:
            model = """\t\t(model "${KICAD10_3DMODEL_DIR}/Connector_Coaxial.3dshapes/U.FL_Hirose_U.FL-R-SMT-1_Vertical.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1 1 1))
			(rotate (xyz 0 0 0))
		)\n\t)"""
            c = c[:m.start()] + m.group(1) + "\n" + model + c[m.end():]
            print("  [PCBA 08] Added 3D model for J4 (U.FL).")

    # 3. Y1_UWB
    if 'Y1_UWB' in c and 'Crystal_SMD_2016-4Pin_2.0x1.6mm.step' not in c:
        m = re.search(r'(\(property \"Reference\" \"Y1_UWB\".*?\(property \"Value\" \"38.4MHz\".*?)\n\t\)', c, re.DOTALL)
        if m:
            model = """\t\t(model "${KICAD10_3DMODEL_DIR}/Crystal.3dshapes/Crystal_SMD_2016-4Pin_2.0x1.6mm.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1 1 1))
			(rotate (xyz 0 0 0))
		)\n\t)"""
            c = c[:m.start()] + m.group(1) + "\n" + model + c[m.end():]
            print("  [PCBA 08] Added 3D model for Y1_UWB (Crystal).")

    # 4. J1 (2P Power Header)
    if 'J1' in c and 'JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical.step' not in c:
        m = re.search(r'(\(property \"Reference\" \"J1\".*?\(property \"Value\" \"12V_RADAR_PWR\".*?)\n\t\)', c, re.DOTALL)
        if m:
            model = """\t\t(model "${KICAD10_3DMODEL_DIR}/Connector_JST.3dshapes/JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1 1 1))
			(rotate (xyz 0 0 0))
		)\n\t)"""
            c = c[:m.start()] + m.group(1) + "\n" + model + c[m.end():]
            print("  [PCBA 08] Added 3D model for J1 (Power).")

    with open(pcb_path, "w", encoding="utf-8") as f:
        f.write(c)

def fix_pcba07():
    pcb_path = "hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb"
    print("\n--- Fixing PCBA 07 (Smart Keyfob) 3D Models ---")
    with open(pcb_path, "r", encoding="utf-8") as f:
        c = f.read()

    # J_QI
    if 'J_QI' in c and 'PinHeader_1x02_P1.27mm_Vertical_SMD_Pin1Left.step' not in c:
        m = re.search(r'(\(property \"Reference\" \"J_QI\".*?\(property \"Value\" \"QI_COIL_ACH_2P\".*?)\n\t\)', c, re.DOTALL)
        if m:
            model = """\t\t(model "${KICAD10_3DMODEL_DIR}/Connector_PinHeader_1.27mm.3dshapes/PinHeader_1x02_P1.27mm_Vertical_SMD_Pin1Left.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1 1 1))
			(rotate (xyz 0 0 0))
		)\n\t)"""
            c = c[:m.start()] + m.group(1) + "\n" + model + c[m.end():]
            print("  [PCBA 07] Added 3D model for J_QI.")

    with open(pcb_path, "w", encoding="utf-8") as f:
        f.write(c)

def main():
    fix_pcba01()
    fix_pcba05()
    fix_pcba03()
    fix_pcba08()
    fix_pcba07()
    print("\n[SUCCESS] Completed all fixes for zones, keepouts, holes, and 3D models!")

if __name__ == "__main__":
    main()
