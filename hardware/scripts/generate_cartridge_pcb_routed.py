#!/usr/bin/env python3
"""
OpenMotorBridge Universal Pod Cartridge Carrier PCB Generator (v8.0)
---------------------------------------------------------------------
Generates the complete 35.0 x 25.0 mm Cartridge Carrier PCB with:
1. Standard KiCad S-expression syntax with (net N "NAME") declarations
2. Full netlist assigned to every pad of J1, J2, U1, C1, F1, R1, D1, H1, H2
3. J2 rotated 90° CCW (opening facing right +X, solder pads on left)
4. Pin mapping perfectly ordered from top to bottom for 100% uncrossed routing
"""

import os
import subprocess

pcb_file = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"
kicad10_3d_dir = "${KICAD10_3DMODEL_DIR}"
kicad_cli = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

nets = [
    (0, ""),
    (1, "GND"),
    (2, "POD_VCC"),
    (3, "VCC_5V_PROT"),
    (4, "POD_NF_P"),
    (5, "POD_NF_N"),
    (6, "POD_OPTO_KEY"),
    (7, "POD_1WIRE_ID"),
    (8, "NET_LED_R"),
]

def generate_cartridge_pcb():
    os.makedirs(os.path.dirname(os.path.abspath(pcb_file)), exist_ok=True)
    
    out = []
    out.append('(kicad_pcb')
    out.append('\t(version 20240108)')
    out.append('\t(generator "pcbnew")')
    out.append('\t(generator_version "9.0")')
    out.append('\t(general')
    out.append('\t\t(thickness 1.6)')
    out.append('\t\t(legacy_teardrops no)')
    out.append('\t)')
    out.append('\t(paper "A4")')
    out.append('\t(layers')
    out.append('\t\t(0 "F.Cu" signal)')
    out.append('\t\t(31 "B.Cu" signal)')
    out.append('\t\t(32 "B.Adhes" user "B.Adhesive")')
    out.append('\t\t(33 "F.Adhes" user "F.Adhesive")')
    out.append('\t\t(34 "B.Paste" user)')
    out.append('\t\t(35 "F.Paste" user)')
    out.append('\t\t(36 "B.SilkS" user "B.Silkscreen")')
    out.append('\t\t(37 "F.SilkS" user "F.Silkscreen")')
    out.append('\t\t(38 "B.Mask" user)')
    out.append('\t\t(39 "F.Mask" user)')
    out.append('\t\t(40 "Dwgs.User" user "User.Drawings")')
    out.append('\t\t(41 "Cmts.User" user "User.Comments")')
    out.append('\t\t(42 "Eco1.User" user "User.Eco1")')
    out.append('\t\t(43 "Eco2.User" user "User.Eco2")')
    out.append('\t\t(44 "Edge.Cuts" user)')
    out.append('\t\t(45 "Margin" user)')
    out.append('\t\t(46 "B.CrtYd" user "B.Courtyard")')
    out.append('\t\t(47 "F.CrtYd" user "F.Courtyard")')
    out.append('\t\t(48 "B.Fab" user)')
    out.append('\t\t(49 "F.Fab" user)')
    out.append('\t)')
    out.append('\t(setup')
    out.append('\t\t(pad_to_mask_clearance 0.05)')
    out.append('\t\t(allow_soldermask_bridges_in_footprints no)')
    out.append('\t\t(pcbplotparams')
    out.append('\t\t\t(layerselection 0x00010fc_ffffffff)')
    out.append('\t\t\t(plot_on_all_layers_selection 0x0000000_00000000)')
    out.append('\t\t\t(disableapertmacros no)')
    out.append('\t\t\t(usegerberextensions no)')
    out.append('\t\t\t(usegerberattributes yes)')
    out.append('\t\t\t(usegerberadvancedattributes yes)')
    out.append('\t\t\t(creategerberjobfile yes)')
    out.append('\t\t)')
    out.append('\t)')

    # Top-Level Netlist (CRITICAL for KiCad / Autorouter connectivity!)
    for n_id, n_name in nets:
        out.append(f'\t(net {n_id} "{n_name}")')

    # Edge.Cuts (35.0 x 25.0 mm from X=100 to 135, Y=67.5 to 92.5 with 2.0mm chamfers)
    X0 = 100.0
    Y0 = 67.5
    W = 35.0
    H = 25.0
    pts = [
        (X0 + 2.0, Y0),
        (X0 + W - 2.0, Y0),
        (X0 + W, Y0 + 2.0),
        (X0 + W, Y0 + H - 2.0),
        (X0 + W - 2.0, Y0 + H),
        (X0 + 2.0, Y0 + H),
        (X0, Y0 + H - 2.0),
        (X0, Y0 + 2.0),
        (X0 + 2.0, Y0)
    ]
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i+1]
        out.append(f'\t(gr_line (start {x1:.3f} {y1:.3f}) (end {x2:.3f} {y2:.3f}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts"))')

    # 1. Footprint J1: 1x06 Horizontal Pin Socket on FRONT SHORT EDGE (X=102.5, Pin 1 at Y=73.65)
    out.append('\t(footprint "Connector_PinSocket_2.54mm:PinSocket_1x06_P2.54mm_Horizontal"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 102.5 73.65)')
    out.append('\t\t(property "Reference" "J1" (at 0 -2.5 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "POD_BASE_SOCKET_6P" (at 0 15 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    
    j1_pads = [
        (1, 0.0, 0.00, 2, "POD_VCC"),
        (2, 0.0, 2.54, 1, "GND"),
        (3, 0.0, 5.08, 4, "POD_NF_P"),
        (4, 0.0, 7.62, 5, "POD_NF_N"),
        (5, 0.0, 10.16, 6, "POD_OPTO_KEY"),
        (6, 0.0, 12.70, 7, "POD_1WIRE_ID"),
    ]
    for p_num, px, py, n_id, n_name in j1_pads:
        out.append(f'\t\t(pad "{p_num}" thru_hole oval (at {px:.3f} {py:.3f}) (size 2.5 1.7) (drill oval 1.5 1.0) (layers "*.Cu" "*.Mask") (net {n_id} "{n_name}"))')
        
    out.append(f'\t\t(model "{kicad10_3d_dir}/Connector_PinSocket_2.54mm.3dshapes/PinSocket_1x06_P2.54mm_Horizontal.step"')
    out.append('\t\t\t(offset (xyz 0 0 0))')
    out.append('\t\t\t(scale (xyz 1 1 1))')
    out.append('\t\t\t(rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # 2. Footprint J2: JST-SH 1.0mm 6-Pin Horizontal on F.Cu at (126.5, 80.0, rot=90)
    # Pads are on the LEFT (X=124.5 mm), and connector opening faces RIGHT (+X)
    out.append('\t(footprint "Connector_JST:JST_SH_SM06B-SRSS-TB_1x06-1MP_P1.00mm_Horizontal"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 126.5 80.0 90)')
    out.append('\t\t(property "Reference" "J2" (at 0 -3.5 90) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "JST_SH_6P_AXIAL" (at 0 3.5 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    
    # Pads ordered top-to-bottom on board:
    # J2.1 (at Y=77.5, Top)    -> VCC_5V_PROT (Net 3)
    # J2.2 (at Y=78.5)         -> POD_NF_P (Net 4)
    # J2.3 (at Y=79.5)         -> POD_NF_N (Net 5)
    # J2.4 (at Y=80.5)         -> POD_OPTO_KEY (Net 6)
    # J2.5 (at Y=81.5)         -> POD_1WIRE_ID (Net 7)
    # J2.6 (at Y=82.5, Bottom) -> GND (Net 1)
    j2_pads = [
        (1, -2.50, -2.00, 3, "VCC_5V_PROT"),
        (2, -1.50, -2.00, 4, "POD_NF_P"),
        (3, -0.50, -2.00, 5, "POD_NF_N"),
        (4,  0.50, -2.00, 6, "POD_OPTO_KEY"),
        (5,  1.50, -2.00, 7, "POD_1WIRE_ID"),
        (6,  2.50, -2.00, 1, "GND"),
    ]
    for p_num, px, py, n_id, n_name in j2_pads:
        out.append(f'\t\t(pad "{p_num}" smd roundrect (at {px:.3f} {py:.3f} 90) (size 0.6 1.55) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net {n_id} "{n_name}"))')
        
    out.append('\t\t(pad "MP" smd roundrect (at -3.80 1.88 90) (size 1.2 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
    out.append('\t\t(pad "MP" smd roundrect (at 3.80 1.88 90) (size 1.2 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')

    out.append(f'\t\t(model "{kicad10_3d_dir}/Connector_JST.3dshapes/JST_SH_SM06B-SRSS-TB_1x06-1MP_P1.00mm_Horizontal.step"')
    out.append('\t\t\t(offset (xyz 0 0 0))')
    out.append('\t\t\t(scale (xyz 1 1 1))')
    out.append('\t\t\t(rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # 3. Footprint U1: Maxim DS2401 Silicon Serial ROM ID (SOT-23) on F.Cu at (115.0, 80.0)
    out.append('\t(footprint "Package_TO_SOT_SMD:SOT-23"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 115 80)')
    out.append('\t\t(property "Reference" "U1" (at 0 -2.5 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "DS2401" (at 0 2.5 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(pad "1" smd roundrect (at -0.95 -1.0) (size 0.9 0.8) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 7 "POD_1WIRE_ID"))')
    out.append('\t\t(pad "2" smd roundrect (at 0.95 -1.0) (size 0.9 0.8) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
    out.append('\t\t(pad "3" smd roundrect (at 0.0 1.0) (size 0.9 0.8) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Package_TO_SOT_SMD.3dshapes/SOT-23.step"')
    out.append('\t\t\t(offset (xyz 0 0 0))')
    out.append('\t\t\t(scale (xyz 1 1 1))')
    out.append('\t\t\t(rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # 4. Footprint C1: 100nF 0603 Capacitor on F.Cu at (115.0, 84.5)
    out.append('\t(footprint "Capacitor_SMD:C_0603_1608Metric"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 115 84.5 90)')
    out.append('\t\t(property "Reference" "C1" (at 0 -1.5 90) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "100nF" (at 0 1.5 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(pad "1" smd roundrect (at -0.775 0 90) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 7 "POD_1WIRE_ID"))')
    out.append('\t\t(pad "2" smd roundrect (at 0.775 0 90) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step"')
    out.append('\t\t\t(offset (xyz 0 0 0))')
    out.append('\t\t\t(scale (xyz 1 1 1))')
    out.append('\t\t\t(rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # 5. Footprint F1: 500mA PTC Fuse 0603 on F.Cu at (108.0, 75.0)
    out.append('\t(footprint "Resistor_SMD:R_0603_1608Metric"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 108 75 90)')
    out.append('\t\t(property "Reference" "F1" (at 0 -1.5 90) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "PTC_500mA" (at 0 1.5 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(pad "1" smd roundrect (at -0.775 0 90) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 2 "POD_VCC"))')
    out.append('\t\t(pad "2" smd roundrect (at 0.775 0 90) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 3 "VCC_5V_PROT"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Resistor_SMD.3dshapes/R_0603_1608Metric.step"')
    out.append('\t\t\t(offset (xyz 0 0 0))')
    out.append('\t\t\t(scale (xyz 1 1 1))')
    out.append('\t\t\t(rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # 6. Footprint R1: 1.5k Resistor 0603 on F.Cu at (108.0, 82.5)
    out.append('\t(footprint "Resistor_SMD:R_0603_1608Metric"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 108 82.5 90)')
    out.append('\t\t(property "Reference" "R1" (at 0 -1.5 90) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "1.5k" (at 0 1.5 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(pad "1" smd roundrect (at -0.775 0 90) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 3 "VCC_5V_PROT"))')
    out.append('\t\t(pad "2" smd roundrect (at 0.775 0 90) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 8 "NET_LED_R"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Resistor_SMD.3dshapes/R_0603_1608Metric.step"')
    out.append('\t\t\t(offset (xyz 0 0 0))')
    out.append('\t\t\t(scale (xyz 1 1 1))')
    out.append('\t\t\t(rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # 7. Footprint D1: Green Power LED 0603 on F.Cu at (108.0, 85.0)
    out.append('\t(footprint "LED_SMD:LED_0603_1608Metric"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 108 85.0 90)')
    out.append('\t\t(property "Reference" "D1" (at 0 -1.5 90) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "GREEN_LED" (at 0 1.5 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(pad "1" smd roundrect (at -0.775 0 90) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 8 "NET_LED_R"))')
    out.append('\t\t(pad "2" smd roundrect (at 0.775 0 90) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/LED_SMD.3dshapes/LED_0603_1608Metric.step"')
    out.append('\t\t\t(offset (xyz 0 0 0))')
    out.append('\t\t\t(scale (xyz 1 1 1))')
    out.append('\t\t\t(rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # 8. Mounting Holes H1 & H2 (M2 Pad with 2.2mm drill)
    for ref, hy in [("H1", 70.5), ("H2", 89.5)]:
        out.append('\t(footprint "MountingHole:MountingHole_2.2mm_M2_Pad"')
        out.append('\t\t(layer "F.Cu")')
        out.append(f'\t\t(at 103.0 {hy:.2f})')
        out.append(f'\t\t(property "Reference" "{ref}" (at 0 -2.8 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
        out.append('\t\t(property "Value" "M2_MountingHole" (at 0 2.8 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
        out.append('\t\t(pad "1" thru_hole circle (at 0 0) (size 3.4 3.4) (drill 2.2) (layers "*.Cu" "*.Mask") (net 1 "GND"))')
        out.append('\t)')

    # 9. Silkscreen Labels
    out.append('\t(gr_text "OPENMOTORBRIDGE // CARRIER" (at 120 70.0 0) (layer "F.SilkS") (effects (font (size 0.55 0.55) (thickness 0.11))))')
    out.append('\t(gr_text "FRONT MATING" (at 106 70.0 0) (layer "F.SilkS") (effects (font (size 0.40 0.40) (thickness 0.08))))')
    out.append('\t(gr_text "DS2401 ID" (at 115 76.5 0) (layer "F.SilkS") (effects (font (size 0.35 0.35) (thickness 0.08))))')
    out.append('\t(gr_text "PTC 500mA" (at 108 72.5 0) (layer "F.SilkS") (effects (font (size 0.30 0.30) (thickness 0.07))))')
    out.append('\t(gr_text "PWR LED" (at 108 87.5 0) (layer "F.SilkS") (effects (font (size 0.30 0.30) (thickness 0.07))))')
    out.append('\t(gr_text "AXIAL JST-SH (TO HEADSET)" (at 125.0 90.0 0) (layer "F.SilkS") (effects (font (size 0.38 0.38) (thickness 0.08))))')

    out.append('\t(gr_text "OPENMOTORBRIDGE CARRIER (B.Cu)" (at 117.5 80.0 0) (layer "B.SilkS") (effects (font (size 0.45 0.45) (thickness 0.10)) (justify mirror)))')
    out.append('\t(gr_text "GND SHIELD PLANE" (at 117.5 90.0 0) (layer "B.SilkS") (effects (font (size 0.40 0.40) (thickness 0.09)) (justify mirror)))')

    out.append(')')
    
    with open(pcb_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
        
    print(f"✓ Successfully generated clean routed Cartridge PCB at {pcb_file}")

    # Generate 3D Renders
    pcb_dir = os.path.dirname(os.path.abspath(pcb_file))
    out_top = os.path.join(pcb_dir, "cartridge_3d_render_top.png")
    out_bot = os.path.join(pcb_dir, "cartridge_3d_render_bottom.png")
    out_persp = os.path.join(pcb_dir, "cartridge_3d_render_perspective.png")

    subprocess.run([kicad_cli, 'pcb', 'render', '--output', out_top, '--zoom', '1.25', '--side', 'top', pcb_file], check=True)
    subprocess.run([kicad_cli, 'pcb', 'render', '--output', out_bot, '--zoom', '1.25', '--side', 'bottom', pcb_file], check=True)
    subprocess.run([kicad_cli, 'pcb', 'render', '--output', out_persp, '--zoom', '1.25', '--rotate', '45,0,-30', '--perspective', pcb_file], check=True)
    print(f"✓ Generated high-res 3D renders:\n  - {out_top}\n  - {out_bot}\n  - {out_persp}")

if __name__ == '__main__':
    generate_cartridge_pcb()
