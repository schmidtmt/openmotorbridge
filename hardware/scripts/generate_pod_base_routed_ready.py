#!/usr/bin/env python3
"""
Generate Clean, Routing-Ready KiCad PCB for Pod Base with Dual-SMD Architecture:
- J1: 6-Pin 2.54mm SMD Pin Header on F.Cu with aligned KiCad SMD 3D Model!
- J2: M8 6-Pin + Shield SMD Socket on B.Cu
- U1: SP3012-06UTG TVS Array (DFN-14) on F.Cu at (108.0, 76.0)
- C1: 100nF 0603 Capacitor on F.Cu at (108.0, 84.0)
- H1 / H2: M2 Mounting Holes at (103.0, 80.0) and (133.0, 80.0)
"""

import os
import math

pcb_file = "hardware/kicad_pod_base/openmotorbridge_pod_base.kicad_pcb"
kicad10_3d_dir = "${KICAD10_3DMODEL_DIR}"

nets = [
    (0, ""),
    (1, "GND"),
    (2, "VCC"),
    (3, "SIG_P"),
    (4, "SIG_N"),
    (5, "TRIGGER_PPS"),
    (6, "1WIRE_ID"),
    (7, "GND_SHIELD"),
]

def generate_pod_base_sexpr():
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

    # Netlist lines
    for n_id, n_name in nets:
        out.append(f'\t(net {n_id} "{n_name}")')

    # Edge.Cuts (36.0 x 20.0 mm from X=100 to 136, Y=70 to 90 with 2mm chamfers and Poka-Yoke Notch on bottom edge)
    # Notch is 4.0 mm wide x 2.5 mm deep at X=125.0..129.0, Y=87.5..90.0
    X0 = 100.0
    Y0 = 70.0
    W = 36.0
    H = 20.0
    pts = [
        (X0 + 2.0, Y0),
        (X0 + W - 2.0, Y0),
        (X0 + W, Y0 + 2.0),
        (X0 + W, Y0 + H - 2.0),
        (X0 + W - 2.0, Y0 + H),
        (129.0, Y0 + H),
        (129.0, Y0 + H - 2.5),
        (125.0, Y0 + H - 2.5),
        (125.0, Y0 + H),
        (X0 + 2.0, Y0 + H),
        (X0, Y0 + H - 2.0),
        (X0, Y0 + 2.0),
        (X0 + 2.0, Y0)
    ]
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i+1]
        out.append(f'\t(gr_line (start {x1:.3f} {y1:.3f}) (end {x2:.3f} {y2:.3f}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts"))')

    # 1. Footprint J1: 1x06 SMD Pin Header (2.54mm pitch) on F.Cu at X=118.0, Pin 1 at Y=73.65
    out.append('\t(footprint "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical_SMD_Pin1Left"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 118 73.65)')
    out.append('\t\t(property "Reference" "J1" (at 0 -2.5 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "MILL_MAX_824_SMD_6P" (at 0 15 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    
    # 6 SMD pads on F.Cu (alternating left/right SMD feet: Pin 1 Left, Pin 2 Right...)
    j1_pads = [
        (1, -1.4, 0.00, 2, "VCC"),
        (2,  1.4, 2.54, 1, "GND"),
        (3, -1.4, 5.08, 3, "SIG_P"),
        (4,  1.4, 7.62, 4, "SIG_N"),
        (5, -1.4, 10.16, 5, "TRIGGER_PPS"),
        (6,  1.4, 12.70, 6, "1WIRE_ID"),
    ]
    for p_num, px, py, n_id, n_name in j1_pads:
        out.append(f'\t\t(pad "{p_num}" smd roundrect (at {px:.3f} {py:.3f}) (size 2.0 1.25) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2) (net {n_id} "{n_name}"))')
        
    out.append(f'\t\t(model "{kicad10_3d_dir}/Connector_PinHeader_2.54mm.3dshapes/PinHeader_1x06_P2.54mm_Vertical_SMD_Pin1Left.step"')
    out.append('\t\t\t(offset (xyz 0 -6.35 0))')
    out.append('\t\t\t(scale (xyz 1 1 1))')
    out.append('\t\t\t(rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # 2. Footprint U1: SP3012-06UTG TVS Array (DFN-14_1.35x3.5mm_P0.5mm) on F.Cu at (108.0, 76.0)
    out.append('\t(footprint "Package_DFN_QFN:DFN-14_1.35x3.5mm_P0.5mm"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 108 76)')
    out.append('\t\t(property "Reference" "U1" (at 0 -2.5 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "SP3012-06UTG" (at 0 2.5 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    
    u1_pads = [
        (1, -0.625, -1.5, 2, "VCC"),
        (2, -0.625, -1.0, 1, "GND"),
        (3, -0.625, -0.5, 3, "SIG_P"),
        (4, -0.625, 0.0, 1, "GND"),
        (5, -0.625, 0.5, 4, "SIG_N"),
        (6, -0.625, 1.0, 5, "TRIGGER_PPS"),
        (7, -0.625, 1.5, 6, "1WIRE_ID"),
        (8, 0.625, 1.5, 6, "1WIRE_ID"),
        (9, 0.625, 1.0, 5, "TRIGGER_PPS"),
        (10, 0.625, 0.5, 1, "GND"),
        (11, 0.625, 0.0, 4, "SIG_N"),
        (12, 0.625, -0.5, 1, "GND"),
        (13, 0.625, -1.0, 3, "SIG_P"),
        (14, 0.625, -1.5, 2, "VCC"),
    ]
    for p_num, px, py, n_id, n_name in u1_pads:
        out.append(f'\t\t(pad "{p_num}" smd roundrect (at {px:.3f} {py:.3f}) (size 0.55 0.25) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net {n_id} "{n_name}"))')
        
    out.append(f'\t\t(model "{kicad10_3d_dir}/Package_DFN_QFN.3dshapes/DFN-14-1EP_3x3mm_P0.4mm_EP1.78x2.35mm.step"')
    out.append('\t\t\t(offset (xyz 0 0 0))')
    out.append('\t\t\t(scale (xyz 0.5 1.1 0.7))')
    out.append('\t\t\t(rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # 3. Footprint C1: 100nF 50V 0603 Capacitor on F.Cu at (108.0, 84.0)
    out.append('\t(footprint "Capacitor_SMD:C_0603_1608Metric"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 108 84 90)')
    out.append('\t\t(property "Reference" "C1" (at 0 -1.5 90) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "100nF_50V" (at 0 1.5 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(pad "1" smd roundrect (at -0.775 0 90) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 2 "VCC"))')
    out.append('\t\t(pad "2" smd roundrect (at 0.775 0 90) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step"')
    out.append('\t\t\t(offset (xyz 0 0 0))')
    out.append('\t\t\t(scale (xyz 1 1 1))')
    out.append('\t\t\t(rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # 4. Footprint J2: Gesockelte M8 6-Pin IP67 Buchse on B.Cu at (118.0, 80.0)
    out.append('\t(footprint "Connector_M8:M8_6Pin_IP67_Receptacle_Socketed"')
    out.append('\t\t(layer "B.Cu")')
    out.append('\t\t(at 118 80)')
    out.append('\t\t(property "Reference" "J2" (at 0 -6 0) (layer "B.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12)) (justify mirror)))')
    out.append('\t\t(property "Value" "M8_6PIN_RECEPTACLE" (at 0 6 0) (layer "B.Fab") (effects (font (size 0.8 0.8) (thickness 0.12)) (justify mirror)))')
    
    angles_deg = [0, 60, 120, 180, 240, 300]
    j2_pin_nets = [(1, 2, "VCC"), (2, 1, "GND"), (3, 3, "SIG_P"), (4, 4, "SIG_N"), (5, 5, "TRIGGER_PPS"), (6, 6, "1WIRE_ID")]
    r_mm = 3.00
    for (p_num, n_id, n_name), ang in zip(j2_pin_nets, angles_deg):
        rad = math.radians(ang)
        px = r_mm * math.cos(rad)
        py = r_mm * math.sin(rad)
        out.append(f'\t\t(pad "{p_num}" smd roundrect (at {px:.3f} {py:.3f}) (size 1.2 1.2) (layers "B.Cu" "B.Paste" "B.Mask") (roundrect_rratio 0.25) (net {n_id} "{n_name}"))')
        
    out.append('\t\t(pad "7" smd roundrect (at 4.5 0.0) (size 1.5 1.5) (layers "B.Cu" "B.Paste" "B.Mask") (roundrect_rratio 0.25) (net 7 "GND_SHIELD"))')

    out.append(f'\t\t(model "${{KICAD10_3DMODEL_DIR}}/Connector_Coaxial.3dshapes/SMA_Amphenol_132134-10_Vertical.step"')
    out.append('\t\t\t(offset (xyz 0 0 0))')
    out.append('\t\t\t(scale (xyz 1.25 1.25 1.25))')
    out.append('\t\t\t(rotate (xyz 0 0 0))')
    out.append('\t\t)')
    out.append('\t)')

    # 5. Mounting Holes H1 & H2
    for ref, hx in [("H1", 103.0), ("H2", 133.0)]:
        out.append('\t(footprint "MountingHole:MountingHole_2.2mm_M2_Pad"')
        out.append('\t\t(layer "F.Cu")')
        out.append(f'\t\t(at {hx} 80)')
        out.append(f'\t\t(property "Reference" "{ref}" (at 0 -2.8 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
        out.append('\t\t(property "Value" "M2_MountingHole" (at 0 2.8 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
        out.append(f'\t\t(pad "1" thru_hole circle (at 0 0) (size 3.4 3.4) (drill 2.2) (layers "*.Cu" "*.Mask") (net 1 "GND"))')
        out.append('\t)')

    # 6. Silkscreen Markings
    out.append('\t(gr_text "OPENMOTORBRIDGE // POD BASE" (at 118 71.5 0) (layer "F.SilkS") (effects (font (size 0.45 0.45) (thickness 0.09))))')
    out.append('\t(gr_text "SP3012 TVS" (at 108 73.5 0) (layer "F.SilkS") (effects (font (size 0.35 0.35) (thickness 0.08))))')
    out.append('\t(gr_text "6-PIN SMD PIN HEADER (J1)" (at 118 88.5 0) (layer "F.SilkS") (effects (font (size 0.38 0.38) (thickness 0.08))))')
    out.append('\t(gr_text "▲ TOP / OBEN" (at 127 72.0 0) (layer "F.SilkS") (effects (font (size 0.45 0.45) (thickness 0.09))))')
    out.append('\t(gr_text "▼ POKA-YOKE KEY" (at 127 86.2 0) (layer "F.SilkS") (effects (font (size 0.40 0.40) (thickness 0.08))))')

    # 7. Routing Tracks & Vias
    tracks = [
        # Net 2 (VCC)
        (2, 116.60, 73.65, 108.625, 73.65, 0.40, "F.Cu"),
        (2, 108.625, 73.65, 108.625, 74.50, 0.40, "F.Cu"),
        (2, 108.625, 74.50, 108.00, 83.15, 0.40, "F.Cu"),
        (2, 116.60, 73.65, 121.00, 75.00, 0.40, "F.Cu"),
        (2, 121.00, 75.00, 121.00, 80.00, 0.40, "B.Cu"),

        # Net 1 (GND)
        (1, 119.40, 76.19, 108.00, 76.19, 0.40, "F.Cu"),
        (1, 108.00, 76.19, 108.00, 84.85, 0.40, "F.Cu"),
        (1, 123.00, 83.00, 119.50, 82.60, 0.40, "B.Cu"),

        # Net 3 (SIG_P)
        (3, 116.60, 78.73, 108.625, 75.50, 0.25, "F.Cu"),
        (3, 116.60, 78.73, 116.50, 80.00, 0.25, "F.Cu"),
        (3, 116.50, 80.00, 116.50, 82.60, 0.25, "B.Cu"),

        # Net 4 (SIG_N)
        (4, 119.40, 81.27, 108.625, 76.50, 0.25, "F.Cu"),
        (4, 119.40, 81.27, 115.00, 78.00, 0.25, "F.Cu"),
        (4, 115.00, 78.00, 115.00, 80.00, 0.25, "B.Cu"),

        # Net 5 (TRIGGER_PPS)
        (5, 116.60, 83.81, 108.625, 77.00, 0.25, "F.Cu"),
        (5, 116.60, 83.81, 116.50, 76.00, 0.25, "F.Cu"),
        (5, 116.50, 76.00, 116.50, 77.40, 0.25, "B.Cu"),

        # Net 6 (1WIRE_ID)
        (6, 119.40, 86.35, 108.625, 77.50, 0.25, "F.Cu"),
        (6, 119.40, 86.35, 119.50, 75.00, 0.25, "F.Cu"),
        (6, 119.50, 75.00, 119.50, 77.40, 0.25, "B.Cu"),
    ]
    for n_id, x1, y1, x2, y2, w, lay in tracks:
        out.append(f'\t(segment (start {x1:.3f} {y1:.3f}) (end {x2:.3f} {y2:.3f}) (width {w:.2f}) (layer "{lay}") (net {n_id}))')
        
    vias = [
        (2, 121.0, 75.0), # VCC
        (1, 123.0, 83.0), # GND
        (3, 116.5, 80.0), # SIG_P
        (4, 115.0, 78.0), # SIG_N
        (5, 116.5, 76.0), # TRIGGER_PPS
        (6, 119.5, 75.0), # 1WIRE_ID
        (1, 105.0, 75.0), # GND plane
        (1, 105.0, 85.0),
        (1, 131.0, 75.0),
        (1, 131.0, 85.0),
    ]
    for n_id, vx, vy in vias:
        out.append(f'\t(via (at {vx:.1f} {vy:.1f}) (size 0.6) (drill 0.3) (layers "F.Cu" "B.Cu") (net {n_id}))')

    out.append(')')
    
    with open(pcb_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
        
    print(f"✓ Successfully generated {pcb_file} with perfectly aligned SMD 3D model!")

if __name__ == '__main__':
    generate_pod_base_sexpr()
