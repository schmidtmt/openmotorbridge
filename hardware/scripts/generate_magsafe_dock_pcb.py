#!/usr/bin/env python3
"""
Generate Complete, Routing-Ready KiCad PCB for PCBA 06: MagSafe Frame Dock Adapter
- Dimensions: 28.0 x 11.5 mm 2-Layer FR4 with 4x 1.0mm 45° chamfers
- H1: Central M2.5 Mounting Hole (X=114.0, Y=75.75), Drill Ø 2.7mm, Pad Ø 4.5mm (GND chassis anchor)
- J1: M8 6-Pin + Shield wire-to-board solder pad strip (Bike Side, Left, X=102.5, Y=75.75) + 3D Horizontal Receptacle Model
- J2: 6-Pin MagSafe Gold SMD Contact Pads (Saddlebag Side, Right, X=125.5, Y=75.75) + 3D Magnetic Dock Model
- F1: 1206 PPTC Resettable Polyfuse (500mA hold, 1A trip, X=106.0, Y=71.2)
- D1: SOD-323 Unidirectional 5V TVS Diode (VCC Transient Clamp, X=109.0, Y=71.2)
- C1: 0603 100nF 50V Ceramic Decoupling Capacitor (X=112.0, Y=71.2)
- U1: SOT-23-6 USBLC6-4SC6 Ultra-Low-Capacitance 4-Ch ESD Array (X=119.5, Y=75.75)
- Clean unrouted canvas ready for user routing in KiCad GUI
"""

import os
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
    out.append('\t(general (thickness 1.6) (legacy_teardrops no))')
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
    out.append('\t)')

    for n_id, n_name in nets:
        out.append(f'\t(net {n_id} "{n_name}")')

    # Edge.Cuts (28.0 x 11.5 mm: X=100.0 to 128.0, Y=70.0 to 81.5)
    X0, Y0, W, H = 100.0, 70.0, 28.0, 11.5
    pts = [
        (X0 + 1.0, Y0),
        (X0 + W - 1.0, Y0),
        (X0 + W, Y0 + 1.0),
        (X0 + W, Y0 + H - 1.0),
        (X0 + W - 1.0, Y0 + H),
        (X0 + 1.0, Y0 + H),
        (X0, Y0 + H - 1.0),
        (X0, Y0 + 1.0),
        (X0 + 1.0, Y0)
    ]
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i+1]
        out.append(f'\t(gr_line (start {x1:.3f} {y1:.3f}) (end {x2:.3f} {y2:.3f}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts"))')

    # 1. Central Mounting Hole M2.5 (Center X=114.0, Y=75.75)
    out.append('\t(footprint "MountingHole:MountingHole_2.7mm_M2.5_Pad"')
    out.append('\t\t(layer "F.Cu") (at 114.0 75.75 0)')
    out.append('\t\t(property "Reference" "H1" (at 0 -2.9 0) (layer "F.SilkS") (effects (font (size 0.5 0.5) (thickness 0.08))))')
    out.append('\t\t(property "Value" "M2.5_MOUNT_HOLE" (at 0 2.9 0) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.08))))')
    out.append('\t\t(pad "1" thru_hole circle (at 0 0) (size 4.5 4.5) (drill 2.7) (layers "*.Cu" "*.Mask") (net 1 "GND"))')
    out.append('\t)')

    # 2. Footprint J1: M8 6-Pin + Shield (X=102.5, Y=75.75)
    out.append('\t(footprint "Connector_Wire:SolderWirePad_1x07_SMD_2.0mm"')
    out.append('\t\t(layer "F.Cu") (at 102.5 75.75 0)')
    out.append('\t\t(property "Reference" "J1" (at 0 -6.5 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "M8_6P_WIRE_PADS" (at 0 6.5 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    j1_pads = [
        (1, 0.0, -4.25, 2, "VCC_IN"),
        (2, 0.0, -2.85, 1, "GND"),
        (3, 0.0, -1.45, 4, "SIG_P"),
        (4, 0.0,  0.00, 5, "SIG_N"),
        (5, 0.0,  1.45, 6, "TRIGGER_PPS"),
        (6, 0.0,  2.85, 7, "1WIRE_ID"),
        (7, 0.0,  4.25, 8, "GND_SHIELD"),
    ]
    for p_num, px, py, n_id, n_name in j1_pads:
        out.append(f'\t\t(pad "{p_num}" thru_hole oval (at {px:.3f} {py:.3f}) (size 1.8 1.1) (drill 0.6) (layers "*.Cu" "*.Mask") (net {n_id} "{n_name}"))')
    out.append('\t\t(model "m8_6pin_horizontal_receptacle.wrl"')
    out.append('\t\t\t(offset (xyz 0 0 0)) (scale (xyz 0.3937 0.3937 0.3937)) (rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # 3. Footprint F1: 1206 PPTC Fuse (X=106.0, Y=71.2)
    out.append('\t(footprint "Fuse:Fuse_1206_3216Metric"')
    out.append('\t\t(layer "F.Cu") (at 106.0 71.2 0)')
    out.append('\t\t(property "Reference" "F1" (at 0 1.3 0) (layer "F.SilkS") (effects (font (size 0.5 0.5) (thickness 0.09))))')
    out.append('\t\t(property "Value" "500mA_PPTC" (at 0 -1.3 0) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.09))))')
    out.append('\t\t(pad "1" smd roundrect (at -1.4 0) (size 1.25 1.75) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2) (net 2 "VCC_IN"))')
    out.append('\t\t(pad "2" smd roundrect (at 1.4 0) (size 1.25 1.75) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2) (net 3 "VCC_PROT"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Fuse.3dshapes/Fuse_1206_3216Metric.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
    out.append('\t)')

    # 4. Footprint D1: SOD-323 TVS Diode (X=109.0, Y=71.2)
    out.append('\t(footprint "Diode_SMD:D_SOD-323"')
    out.append('\t\t(layer "F.Cu") (at 109.0 71.2 0)')
    out.append('\t\t(property "Reference" "D1" (at 0 -1.3 0) (layer "F.SilkS") (effects (font (size 0.5 0.5) (thickness 0.09))))')
    out.append('\t\t(property "Value" "ESD5Z5.0" (at 0 1.3 0) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.09))))')
    out.append('\t\t(pad "1" smd roundrect (at -1.05 0) (size 0.6 0.45) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 3 "VCC_PROT"))')
    out.append('\t\t(pad "2" smd roundrect (at 1.05 0) (size 0.6 0.45) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Diode_SMD.3dshapes/D_SOD-323.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
    out.append('\t)')

    # 5. Footprint C1: 0603 100nF Cap (X=112.0, Y=71.2)
    out.append('\t(footprint "Capacitor_SMD:C_0603_1608Metric"')
    out.append('\t\t(layer "F.Cu") (at 112.0 71.2 0)')
    out.append('\t\t(property "Reference" "C1" (at 0 -1.3 0) (layer "F.SilkS") (effects (font (size 0.5 0.5) (thickness 0.09))))')
    out.append('\t\t(property "Value" "100nF" (at 0 1.3 0) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.09))))')
    out.append('\t\t(pad "1" smd roundrect (at -0.775 0) (size 0.9 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 3 "VCC_PROT"))')
    out.append('\t\t(pad "2" smd roundrect (at 0.775 0) (size 0.9 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
    out.append('\t)')

    # 6. Footprint U1: SOT-23-6 ESD Array (X=119.5, Y=75.75)
    out.append('\t(footprint "Package_TO_SOT_SMD:SOT-23-6"')
    out.append('\t\t(layer "F.Cu") (at 119.5 75.75 0)')
    out.append('\t\t(property "Reference" "U1" (at 0 2.2 0) (layer "F.SilkS") (effects (font (size 0.5 0.5) (thickness 0.09))))')
    out.append('\t\t(property "Value" "USBLC6-4SC6" (at 0 -2.2 0) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.09))))')
    out.append('\t\t(pad "1" smd roundrect (at -1.137 -0.95) (size 1.325 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 4 "SIG_P"))')
    out.append('\t\t(pad "2" smd roundrect (at -1.137 0.0) (size 1.325 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
    out.append('\t\t(pad "3" smd roundrect (at -1.137 0.95) (size 1.325 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 5 "SIG_N"))')
    out.append('\t\t(pad "4" smd roundrect (at 1.137 0.95) (size 1.325 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 6 "TRIGGER_PPS"))')
    out.append('\t\t(pad "5" smd roundrect (at 1.137 0.0) (size 1.325 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 3 "VCC_PROT"))')
    out.append('\t\t(pad "6" smd roundrect (at 1.137 -0.95) (size 1.325 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 7 "1WIRE_ID"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Package_TO_SOT_SMD.3dshapes/SOT-23-6.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
    out.append('\t)')

    # 7. Footprint J2: MagSafe 6-Pin SMD Contact Array (X=125.5, Y=75.75)
    out.append('\t(footprint "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical_SMD_Pin1Left"')
    out.append('\t\t(layer "F.Cu") (at 125.5 75.75 0)')
    out.append('\t\t(property "Reference" "J2" (at 0 -6.5 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "MAGSAFE_6P_DOCK" (at 0 6.5 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    j2_pads = [
        (1, 0.0, -4.00, 3, "VCC_PROT"),
        (2, 0.0, -2.40, 1, "GND"),
        (3, 0.0, -0.80, 4, "SIG_P"),
        (4, 0.0,  0.80, 5, "SIG_N"),
        (5, 0.0,  2.40, 6, "TRIGGER_PPS"),
        (6, 0.0,  4.00, 7, "1WIRE_ID"),
    ]
    for p_num, px, py, n_id, n_name in j2_pads:
        out.append(f'\t\t(pad "{p_num}" smd roundrect (at {px:.3f} {py:.3f}) (size 2.4 1.1) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net {n_id} "{n_name}"))')
    out.append('\t\t(model "magsafe_6pin_dock_connector.wrl"')
    out.append('\t\t\t(offset (xyz 0 0 0)) (scale (xyz 0.3937 0.3937 0.3937)) (rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # Silkscreen
    out.append('\t(gr_text "PCBA 06 // MAGSAFE DOCK" (at 114.0 72.8 0) (layer "F.SilkS") (effects (font (size 0.45 0.45) (thickness 0.08))))')
    out.append('\t(gr_text "M8 BIKE" (at 104.5 70.8 0) (layer "F.SilkS") (effects (font (size 0.45 0.45) (thickness 0.08))))')
    out.append('\t(gr_text "MAGSAFE" (at 123.5 70.8 0) (layer "F.SilkS") (effects (font (size 0.45 0.45) (thickness 0.08))))')

    out.append('\t(gr_text "OPENMOTORBRIDGE v8.2" (at 114.0 73.5 0) (layer "B.SilkS") (effects (font (size 0.65 0.65) (thickness 0.11)) (justify mirror)))')
    out.append('\t(gr_text "CENTER MOUNT M2.5 // IP67 DOCK" (at 114.0 78.5 0) (layer "B.SilkS") (effects (font (size 0.50 0.50) (thickness 0.09)) (justify mirror)))')

    out.append(')')

    with open(pcb_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))

    print(f"✓ Successfully generated clean unrouted board {pcb_file} with central M2.5 mounting hole!")

if __name__ == '__main__':
    generate_magsafe_dock_pcb()
