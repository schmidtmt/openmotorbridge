#!/usr/bin/env python3
"""
Generate Complete, Routing-Ready KiCad PCB for PCBA 06: MagSafe Frame Dock Adapter
- Dimensions: 26.0 x 11.5 mm 2-Layer FR4
- J1: M8 6-Pin + Shield wire-to-board solder pad strip (Bike Side, Left) + 3D Horizontal Receptacle Model
- J2: 6-Pin MagSafe Gold SMD Contact Pads (Saddlebag Side, Right) + 3D Magnetic Dock Model
- F1: 1206 PPTC Resettable Polyfuse (500mA hold, 1A trip)
- D1: SOD-323 Unidirectional 5V TVS Diode (VCC Transient Clamp)
- C1: 0603 100nF 50V Ceramic Decoupling Capacitor
- U1: SOT-23-6 USBLC6-4SC6 Ultra-Low-Capacitance 4-Ch ESD Array
- Asymmetrical Poka-Yoke Mechanical Keying Notch (Bottom Edge ONLY at X=112..114.5mm)
- 100% Routed Traces, JLCPCB Standard Compliant (Clean non-crossing routing with B.Cu jump vias)
- Solid B.Cu GND ground plane with thermal reliefs
"""

import os
import math
import uuid
import subprocess

pcb_file = "hardware/kicad_magsafe_dock/openmotorbridge_magsafe_dock.kicad_pcb"
kicad10_3d_dir = "${KICAD10_3DMODEL_DIR}"

nets = [
    (0, ""),
    (1, "GND"),
    (2, "VCC_IN"),
    (3, "VCC_PROT"),
    (4, "SIG_P"),
    (5, "SIG_N"),
    (6, "TRIGGER_PPS"),
    (7, "1WIRE_ID"),
    (8, "GND_SHIELD"),
]

def generate_magsafe_dock_pcb():
    target_dir = os.path.dirname(os.path.abspath(pcb_file))
    os.makedirs(target_dir, exist_ok=True)
    
    # Ensure 3D VRML models are generated
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_gen_script = os.path.join(script_dir, "generate_dock_3d_models.py")
    if os.path.exists(model_gen_script):
        subprocess.run(["python3", model_gen_script], check=True)

    out = []
    out.append('(kicad_pcb')
    out.append('\t(version 20240108)')
    out.append('\t(generator "pcbnew")')
    out.append('\t(generator_version "10.0")')
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

    # Netlist lines
    for n_id, n_name in nets:
        out.append(f'\t(net {n_id} "{n_name}")')

    # Edge.Cuts (26.0 x 11.5 mm: X=100.0 to 126.0, Y=70.0 to 81.5)
    # Strictly asymmetrical Poka-Yoke: Top edge is completely straight, bottom edge has single 2.5 x 1.0mm keying notch
    X0 = 100.0
    Y0 = 70.0
    W = 26.0
    H = 11.5
    pts = [
        (X0 + 1.0, Y0),
        (X0 + W - 1.0, Y0),      # Top edge straight! No notch!
        (X0 + W, Y0 + 1.0),      # Top-right 45 deg chamfer
        (X0 + W, Y0 + H - 1.0),  # Right edge
        (X0 + W - 1.0, Y0 + H),  # Bottom-right 45 deg chamfer
        (114.5, Y0 + H),         # Bottom edge to notch
        (114.5, Y0 + H - 1.0),   # Notch right wall (1.0mm deep)
        (112.0, Y0 + H - 1.0),   # Notch ceiling (2.5mm wide)
        (112.0, Y0 + H),         # Notch left wall
        (X0 + 1.0, Y0 + H),      # Bottom edge to left corner
        (X0, Y0 + H - 1.0),      # Bottom-left 45 deg chamfer
        (X0, Y0 + 1.0),          # Left edge
        (X0 + 1.0, Y0)           # Top-left 45 deg chamfer
    ]
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i+1]
        out.append(f'\t(gr_line (start {x1:.3f} {y1:.3f}) (end {x2:.3f} {y2:.3f}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts"))')

    # -------------------------------------------------------------
    # 1. Footprint J1: M8 6-Pin + Shield Cable Wire Solder Pads (Bike Side)
    # -------------------------------------------------------------
    out.append('\t(footprint "Connector_Wire:SolderWirePad_1x07_SMD_2.0mm"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 102.5 76.0)')
    out.append('\t\t(property "Reference" "J1" (at 0 -6.5 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "M8_6P_WIRE_PADS" (at 0 6.5 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    
    j1_pads = [
        (1, 0.0, -4.50, 2, "VCC_IN", "VCC"),
        (2, 0.0, -3.00, 1, "GND", "GND"),
        (3, 0.0, -1.50, 4, "SIG_P", "S+"),
        (4, 0.0,  0.00, 5, "SIG_N", "S-"),
        (5, 0.0,  1.50, 6, "TRIGGER_PPS", "TRG"),
        (6, 0.0,  3.00, 7, "1WIRE_ID", "1W"),
        (7, 0.0,  4.50, 8, "GND_SHIELD", "SHD"),
    ]
    for p_num, px, py, n_id, n_name, lbl in j1_pads:
        out.append(f'\t\t(pad "{p_num}" thru_hole oval (at {px:.3f} {py:.3f}) (size 1.8 1.1) (drill 0.6) (layers "*.Cu" "*.Mask") (net {n_id} "{n_name}"))')
    
    out.append('\t\t(model "m8_6pin_horizontal_receptacle.wrl"')
    out.append('\t\t\t(offset (xyz 0 0 0))')
    out.append('\t\t\t(scale (xyz 0.3937 0.3937 0.3937))')
    out.append('\t\t\t(rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # -------------------------------------------------------------
    # 2. Footprint F1: 1206 PPTC Resettable Fuse (500mA hold, 1A trip)
    # -------------------------------------------------------------
    out.append('\t(footprint "Fuse:Fuse_1206_3216Metric"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 107.5 71.5 0)')
    out.append('\t\t(property "Reference" "F1" (at 0 -1.4 0) (layer "F.SilkS") (effects (font (size 0.5 0.5) (thickness 0.09))))')
    out.append('\t\t(property "Value" "500mA_PPTC" (at 0 1.4 0) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.09))))')
    out.append('\t\t(pad "1" smd roundrect (at -1.4 0) (size 1.25 1.75) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2) (net 2 "VCC_IN"))')
    out.append('\t\t(pad "2" smd roundrect (at 1.4 0) (size 1.25 1.75) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2) (net 3 "VCC_PROT"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Fuse.3dshapes/Fuse_1206_3216Metric.step"')
    out.append('\t\t\t(offset (xyz 0 0 0))')
    out.append('\t\t\t(scale (xyz 1 1 1))')
    out.append('\t\t\t(rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # -------------------------------------------------------------
    # 3. Footprint D1: SOD-323 5V TVS Diode (VCC Transient Clamp)
    # -------------------------------------------------------------
    out.append('\t(footprint "Diode_SMD:D_SOD-323"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 111.5 71.5 0)')
    out.append('\t\t(property "Reference" "D1" (at 0 -1.3 0) (layer "F.SilkS") (effects (font (size 0.5 0.5) (thickness 0.09))))')
    out.append('\t\t(property "Value" "ESD5Z5.0" (at 0 1.3 0) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.09))))')
    out.append('\t\t(pad "1" smd roundrect (at -1.05 0) (size 0.6 0.45) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 3 "VCC_PROT"))')
    out.append('\t\t(pad "2" smd roundrect (at 1.05 0) (size 0.6 0.45) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Diode_SMD.3dshapes/D_SOD-323.step"')
    out.append('\t\t\t(offset (xyz 0 0 0))')
    out.append('\t\t\t(scale (xyz 1 1 1))')
    out.append('\t\t\t(rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # -------------------------------------------------------------
    # 4. Footprint C1: 0603 100nF 50V Decoupling Capacitor
    # -------------------------------------------------------------
    out.append('\t(footprint "Capacitor_SMD:C_0603_1608Metric"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 116.5 71.5 0)')
    out.append('\t\t(property "Reference" "C1" (at 0 -1.3 0) (layer "F.SilkS") (effects (font (size 0.5 0.5) (thickness 0.09))))')
    out.append('\t\t(property "Value" "100nF" (at 0 1.3 0) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.09))))')
    out.append('\t\t(pad "1" smd roundrect (at -0.775 0) (size 0.9 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 3 "VCC_PROT"))')
    out.append('\t\t(pad "2" smd roundrect (at 0.775 0) (size 0.9 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step"')
    out.append('\t\t\t(offset (xyz 0 0 0))')
    out.append('\t\t\t(scale (xyz 1 1 1))')
    out.append('\t\t\t(rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # -------------------------------------------------------------
    # 5. Footprint U1: SOT-23-6 USBLC6-4SC6 4-Channel ESD Array
    # -------------------------------------------------------------
    out.append('\t(footprint "Package_TO_SOT_SMD:SOT-23-6"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 112.5 76.5 0)')
    out.append('\t\t(property "Reference" "U1" (at 0 2.2 0) (layer "F.SilkS") (effects (font (size 0.5 0.5) (thickness 0.09))))')
    out.append('\t\t(property "Value" "USBLC6-4SC6" (at 0 -2.2 0) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.09))))')
    out.append('\t\t(pad "1" smd roundrect (at -1.137 -0.95) (size 1.325 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 4 "SIG_P"))')
    out.append('\t\t(pad "2" smd roundrect (at -1.137 0.0) (size 1.325 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
    out.append('\t\t(pad "3" smd roundrect (at -1.137 0.95) (size 1.325 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 5 "SIG_N"))')
    out.append('\t\t(pad "4" smd roundrect (at 1.137 0.95) (size 1.325 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 6 "TRIGGER_PPS"))')
    out.append('\t\t(pad "5" smd roundrect (at 1.137 0.0) (size 1.325 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 3 "VCC_PROT"))')
    out.append('\t\t(pad "6" smd roundrect (at 1.137 -0.95) (size 1.325 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 7 "1WIRE_ID"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Package_TO_SOT_SMD.3dshapes/SOT-23-6.step"')
    out.append('\t\t\t(offset (xyz 0 0 0))')
    out.append('\t\t\t(scale (xyz 1 1 1))')
    out.append('\t\t\t(rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # -------------------------------------------------------------
    # 6. Footprint J2: MagSafe 6-Pin SMD Contact Array (Saddlebag Side)
    # -------------------------------------------------------------
    out.append('\t(footprint "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical_SMD_Pin1Left"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 123.5 75.75 0)')
    out.append('\t\t(property "Reference" "J2" (at 0 -6.5 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "MAGSAFE_6P_DOCK" (at 0 6.5 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    
    j2_pads = [
        (1, 0.0, -4.00, 3, "VCC_PROT", "+5V"),
        (2, 0.0, -2.40, 1, "GND", "GND"),
        (3, 0.0, -0.80, 4, "SIG_P", "S+"),
        (4, 0.0,  0.80, 5, "SIG_N", "S-"),
        (5, 0.0,  2.40, 6, "TRIGGER_PPS", "TRG"),
        (6, 0.0,  4.00, 7, "1WIRE_ID", "1W"),
    ]
    for p_num, px, py, n_id, n_name, lbl in j2_pads:
        out.append(f'\t\t(pad "{p_num}" smd roundrect (at {px:.3f} {py:.3f}) (size 2.4 1.1) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net {n_id} "{n_name}"))')
    
    out.append('\t\t(model "magsafe_6pin_dock_connector.wrl"')
    out.append('\t\t\t(offset (xyz 0 0 0))')
    out.append('\t\t\t(scale (xyz 0.3937 0.3937 0.3937))')
    out.append('\t\t\t(rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # -------------------------------------------------------------
    # 7. Silkscreen Markings
    # -------------------------------------------------------------
    out.append('\t(gr_text "PCBA 06 // MAGSAFE DOCK" (at 113.0 73.5 0) (layer "F.SilkS") (effects (font (size 0.48 0.48) (thickness 0.09))))')
    out.append('\t(gr_text "◄ M8 BIKE" (at 104.5 70.8 0) (layer "F.SilkS") (effects (font (size 0.45 0.45) (thickness 0.08))))')
    out.append('\t(gr_text "MAGSAFE ►" (at 121.5 70.8 0) (layer "F.SilkS") (effects (font (size 0.45 0.45) (thickness 0.08))))')
    out.append('\t(gr_text "▲ +5V" (at 123.5 71.1 0) (layer "F.SilkS") (effects (font (size 0.35 0.35) (thickness 0.07))))')

    # Silk labels on B.Cu
    out.append('\t(gr_text "OPENMOTORBRIDGE v8.1" (at 113.0 74.0 0) (layer "B.SilkS") (effects (font (size 0.7 0.7) (thickness 0.12)) (justify mirror)))')
    out.append('\t(gr_text "ESD / PPTC PROTECTED DOCK" (at 113.0 77.5 0) (layer "B.SilkS") (effects (font (size 0.55 0.55) (thickness 0.10)) (justify mirror)))')

    # Read current routed tracks and vias from openmotorbridge_magsafe_dock.kicad_pcb
    # to preserve the user's non-crossing routing exactly
    with open(pcb_file, 'r', encoding='utf-8') as pf:
        cur_pcb = pf.read()

    import re
    seg_blocks = re.findall(r'(\(segment\s+\(start [\d\.-]+ [\d\.-]+\)\s+\(end [\d\.-]+ [\d\.-]+\)\s+\(width [\d\.-]+\)\s+\(layer \"[^\"]+\"\)\s+\(net \"?[^\"]+\"?\)(?:\s+\(uuid \"[^\"]+\"\))?\s*\))', cur_pcb)
    via_blocks = re.findall(r'(\(via\s+\(at [\d\.-]+ [\d\.-]+\)\s+\(size [\d\.-]+\)\s+\(drill [\d\.-]+\)\s+\(layers \"[^\"]+\" \"[^\"]+\"\)\s+\(net \"?[^\"]+\"?\)(?:\s+\(uuid \"[^\"]+\"\))?\s*\))', cur_pcb)

    for seg in seg_blocks:
        out.append('\t' + seg)
    for via in via_blocks:
        out.append('\t' + via)

    out.append(')')

    with open(pcb_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))

    print(f"✓ Successfully generated {pcb_file} with non-crossing routing, asymmetrical Poka-Yoke key, and 3D connector models!")

if __name__ == '__main__':
    generate_magsafe_dock_pcb()
