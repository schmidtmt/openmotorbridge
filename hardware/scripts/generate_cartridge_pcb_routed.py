#!/usr/bin/env python3
"""
OpenMotorBridge Smart Modular Cartridge PCB Generator (Rev 2.0)
---------------------------------------------------------------------
Generates the clean canvas for the 35.0 x 25.0 mm Smart Modular Cartridge (PCBA 03 Rev 2.0)
with all Rev 2.0 components pre-placed and fully netted for manual placement & routing:

Key Components:
1. J1: 6-Pin Horizontal Pin Socket at X=102.5, Y=73.65 (POD-BASE DOCKING INTERFACE - PRESERVED 100%)
2. U1: WCH CH32V003F4P6 RISC-V MCU (TSSOP-20) for 1-Wire ROM-ID emulation, ISP flashing & pattern control
3. Q1..Q4: 4x AO3400A N-MOSFETs (SOT-23) for independent mechatronic actuators
4. D1..D4: 4x 1N4148WS Flyback Diodes (SOD-323)
5. J_ACT: 8-Pin JST-SH 1.0mm Horizontal Connector for Actuators
6. J2: 6-Pin JST-SH 1.0mm Horizontal Connector for Intercom Audio & DC
7. R1..R4: 100R Gate Resistors, R5..R8: 100k Pulldowns, R9: 4.7k 1-Wire Pullup
8. C1: 100nF 0603, C2: 10uF 0805, F1: 500mA 1812 PPTC Fuse
9. H1..H4: 4x M2 Mounting Holes in corners
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
    (6, "POD_TRIGGER_PPS"),
    (7, "POD_1WIRE"),
    (8, "ACT1_GATE"),
    (9, "ACT2_GATE"),
    (10, "ACT3_GATE"),
    (11, "ACT4_GATE"),
    (12, "Q1_GATE"),
    (13, "Q2_GATE"),
    (14, "Q3_GATE"),
    (15, "Q4_GATE"),
    (16, "ACT_PLUS"),
    (17, "ACT_MINUS"),
    (18, "ACT_CENTER"),
    (19, "ACT_MESH"),
    (20, "MIC_IN+"),
    (21, "RESERVE_IO"),
    (22, "NRST"),
    (23, "PD1_SWIO"),
]

def generate_cartridge_pcb():
    os.makedirs(os.path.dirname(os.path.abspath(pcb_file)), exist_ok=True)
    
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

    # Netlist declarations
    for n_id, n_name in nets:
        out.append(f'\t(net {n_id} "{n_name}")')

    # Edge.Cuts (35.0 x 25.0 mm from X=100.0 to 135.0, Y=67.5 to 92.5 with 2.0mm chamfers)
    X0, Y0, W, H = 100.0, 67.5, 35.0, 25.0
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

    # 1. Footprint J1: 1x06 Horizontal Pin Socket on FRONT/REAR DOCKING EDGE (X=102.5, Pin 1 at Y=73.65)
    # CRITICAL: THIS CONNECTOR POSITION MUST NOT BE MOVED BY A SINGLE MILLIMETER!
    out.append('\t(footprint "Connector_PinSocket_2.54mm:PinSocket_1x06_P2.54mm_Horizontal"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 102.500 73.650)')
    out.append('\t\t(property "Reference" "J1" (at 0 -2.5 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "POD_BASE_DOCKING_SOCKET_6P" (at 0 15 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Description" "6-Pin Horizontal Precision Receptacle (Rear Edge Docking to PCBA 02 Pod-Base)" (at 0 0 0) (layer "F.Fab") (hide yes) (effects (font (size 1.27 1.27))))')
    
    j1_pads = [
        (1, 0.0, 0.00, 2, "POD_VCC"),
        (2, 0.0, 2.54, 1, "GND"),
        (3, 0.0, 5.08, 4, "POD_NF_P"),
        (4, 0.0, 7.62, 5, "POD_NF_N"),
        (5, 0.0, 10.16, 6, "POD_TRIGGER_PPS"),
        (6, 0.0, 12.70, 7, "POD_1WIRE"),
    ]
    for p_num, px, py, n_id, n_name in j1_pads:
        out.append(f'\t\t(pad "{p_num}" thru_hole oval (at {px:.3f} {py:.3f}) (size 2.5 1.7) (drill oval 1.5 1.0) (layers "*.Cu" "*.Mask") (net {n_id} "{n_name}"))')
        
    out.append(f'\t\t(model "{kicad10_3d_dir}/Connector_PinSocket_2.54mm.3dshapes/PinSocket_1x06_P2.54mm_Horizontal.step"')
    out.append('\t\t\t(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
    out.append('\t)')

    # 2. Footprint F1: 500mA PPTC Fuse 1812 at (109.0, 72.0, rot=90)
    out.append('\t(footprint "Fuse:Fuse_1812_4532Metric"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 109.000 72.000 90)')
    out.append('\t\t(property "Reference" "F1" (at 0 -2.0 90) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "MF-MSMF050-2" (at 0 2.0 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(pad "1" smd roundrect (at -2.00 0 90) (size 1.4 3.4) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2) (net 2 "POD_VCC"))')
    out.append('\t\t(pad "2" smd roundrect (at 2.00 0 90) (size 1.4 3.4) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2) (net 3 "VCC_5V_PROT"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Fuse.3dshapes/Fuse_1812_4532Metric.step"')
    out.append('\t\t\t(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
    out.append('\t)')

    # 3. Footprint C1: 100nF 0603 Capacitor at (111.0, 76.0, rot=90)
    out.append('\t(footprint "Capacitor_SMD:C_0603_1608Metric"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 111.000 76.000 90)')
    out.append('\t\t(property "Reference" "C1" (at 0 -1.5 90) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "100nF" (at 0 1.5 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(pad "1" smd roundrect (at -0.775 0 90) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 3 "VCC_5V_PROT"))')
    out.append('\t\t(pad "2" smd roundrect (at 0.775 0 90) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step"')
    out.append('\t\t\t(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
    out.append('\t)')

    # 4. Footprint C2: 10uF 0805 Capacitor at (111.0, 79.5, rot=90)
    out.append('\t(footprint "Capacitor_SMD:C_0805_2012Metric"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 111.000 79.500 90)')
    out.append('\t\t(property "Reference" "C2" (at 0 -1.8 90) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "10uF" (at 0 1.8 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(pad "1" smd roundrect (at -0.95 0 90) (size 1.0 1.45) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 3 "VCC_5V_PROT"))')
    out.append('\t\t(pad "2" smd roundrect (at 0.95 0 90) (size 1.0 1.45) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Capacitor_SMD.3dshapes/C_0805_2012Metric.step"')
    out.append('\t\t\t(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
    out.append('\t)')

    # 5. Footprint R9: 4.7k 0603 1-Wire Pullup Resistor at (111.0, 84.0, rot=90)
    out.append('\t(footprint "Resistor_SMD:R_0603_1608Metric"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 111.000 84.000 90)')
    out.append('\t\t(property "Reference" "R9" (at 0 -1.5 90) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "4.7k" (at 0 1.5 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(pad "1" smd roundrect (at -0.775 0 90) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 3 "VCC_5V_PROT"))')
    out.append('\t\t(pad "2" smd roundrect (at 0.775 0 90) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 7 "POD_1WIRE"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Resistor_SMD.3dshapes/R_0603_1608Metric.step"')
    out.append('\t\t\t(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
    out.append('\t)')

    # 6. Footprint U1: WCH CH32V003F4P6 TSSOP-20 MCU at (116.5, 80.0)
    out.append('\t(footprint "Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 116.500 80.000)')
    out.append('\t\t(property "Reference" "U1" (at 0 -4.2 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "CH32V003F4P6" (at 0 4.2 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    
    u1_pins = [
        # Left side: Pins 1..10 (X = -2.85)
        (1,  -2.85, -2.925, 0, ""),
        (2,  -2.85, -2.275, 7, "POD_1WIRE"),
        (3,  -2.85, -1.625, 6, "POD_TRIGGER_PPS"),
        (4,  -2.85, -0.975, 22, "NRST"),
        (5,  -2.85, -0.325, 0, ""),
        (6,  -2.85,  0.325, 0, ""),
        (7,  -2.85,  0.975, 1, "GND"),
        (8,  -2.85,  1.625, 23, "PD1_SWIO"),
        (9,  -2.85,  2.275, 3, "VCC_5V_PROT"),
        (10, -2.85,  2.925, 0, ""),
        # Right side: Pins 11..20 (X = +2.85)
        (11,  2.85,  2.925, 10, "ACT3_GATE"),
        (12,  2.85,  2.275, 0, ""),
        (13,  2.85,  1.625, 0, ""),
        (14,  2.85,  0.975, 21, "RESERVE_IO"),
        (15,  2.85,  0.325, 0, ""),
        (16,  2.85, -0.325, 0, ""),
        (17,  2.85, -0.975, 0, ""),
        (18,  2.85, -1.625, 11, "ACT4_GATE"),
        (19,  2.85, -2.275, 8, "ACT1_GATE"),
        (20,  2.85, -2.925, 9, "ACT2_GATE"),
    ]
    for p_num, px, py, n_id, n_name in u1_pins:
        out.append(f'\t\t(pad "{p_num}" smd roundrect (at {px:.3f} {py:.3f}) (size 1.45 0.45) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net {n_id} "{n_name}"))')
        
    out.append(f'\t\t(model "{kicad10_3d_dir}/Package_SO.3dshapes/TSSOP-20_4.4x6.5mm_P0.65mm.step"')
    out.append('\t\t\t(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
    out.append('\t)')

    # 7. Footprints R1..R4 (100R Gate Resistors 0603) and R5..R8 (100k Gate Pulldowns 0603)
    gate_r = [
        ("R1", "100R", 121.5, 71.5, 8, "ACT1_GATE", 12, "Q1_GATE"),
        ("R5", "100k", 121.5, 73.5, 12, "Q1_GATE", 1, "GND"),
        ("R2", "100R", 121.5, 76.0, 9, "ACT2_GATE", 13, "Q2_GATE"),
        ("R6", "100k", 121.5, 78.0, 13, "Q2_GATE", 1, "GND"),
        ("R3", "100R", 121.5, 80.5, 10, "ACT3_GATE", 14, "Q3_GATE"),
        ("R7", "100k", 121.5, 82.5, 14, "Q3_GATE", 1, "GND"),
        ("R4", "100R", 121.5, 85.0, 11, "ACT4_GATE", 15, "Q4_GATE"),
        ("R8", "100k", 121.5, 87.0, 15, "Q4_GATE", 1, "GND"),
    ]
    for ref, val, rx, ry, n1, name1, n2, name2 in gate_r:
        out.append('\t(footprint "Resistor_SMD:R_0603_1608Metric"')
        out.append('\t\t(layer "F.Cu")')
        out.append(f'\t\t(at {rx:.3f} {ry:.3f})')
        out.append(f'\t\t(property "Reference" "{ref}" (at 0 -1.5 0) (layer "F.SilkS") (effects (font (size 0.7 0.7) (thickness 0.1))))')
        out.append(f'\t\t(property "Value" "{val}" (at 0 1.5 0) (layer "F.Fab") (effects (font (size 0.7 0.7) (thickness 0.1))))')
        out.append(f'\t\t(pad "1" smd roundrect (at -0.775 0) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net {n1} "{name1}"))')
        out.append(f'\t\t(pad "2" smd roundrect (at 0.775 0) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net {n2} "{name2}"))')
        out.append(f'\t\t(model "{kicad10_3d_dir}/Resistor_SMD.3dshapes/R_0603_1608Metric.step"')
        out.append('\t\t\t(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
        out.append('\t)')

    # 8. Footprints Q1..Q4: AO3400A N-MOSFETs (SOT-23)
    mosfets = [
        ("Q1", 125.0, 72.0, 12, "Q1_GATE", 16, "ACT_PLUS"),
        ("Q2", 125.0, 76.5, 13, "Q2_GATE", 17, "ACT_MINUS"),
        ("Q3", 125.0, 81.0, 14, "Q3_GATE", 18, "ACT_CENTER"),
        ("Q4", 125.0, 85.5, 15, "Q4_GATE", 19, "ACT_MESH"),
    ]
    for ref, qx, qy, g_net, g_name, d_net, d_name in mosfets:
        out.append('\t(footprint "Package_TO_SOT_SMD:SOT-23"')
        out.append('\t\t(layer "F.Cu")')
        out.append(f'\t\t(at {qx:.3f} {qy:.3f})')
        out.append(f'\t\t(property "Reference" "{ref}" (at 0 -2.5 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
        out.append('\t\t(property "Value" "AO3400A" (at 0 2.5 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
        out.append(f'\t\t(pad "1" smd roundrect (at -0.95 -1.0) (size 0.9 0.8) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net {g_net} "{g_name}"))')
        out.append(f'\t\t(pad "2" smd roundrect (at 0.95 -1.0) (size 0.9 0.8) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
        out.append(f'\t\t(pad "3" smd roundrect (at 0.0 1.0) (size 0.9 0.8) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net {d_net} "{d_name}"))')
        out.append(f'\t\t(model "{kicad10_3d_dir}/Package_TO_SOT_SMD.3dshapes/SOT-23.step"')
        out.append('\t\t\t(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
        out.append('\t)')

    # 9. Footprints D1..D4: 1N4148WS Flyback Diodes (SOD-323)
    diodes = [
        ("D1", 128.5, 72.0, 16, "ACT_PLUS"),
        ("D2", 128.5, 76.5, 17, "ACT_MINUS"),
        ("D3", 128.5, 81.0, 18, "ACT_CENTER"),
        ("D4", 128.5, 85.5, 19, "ACT_MESH"),
    ]
    for ref, dx, dy, a_net, a_name in diodes:
        out.append('\t(footprint "Diode_SMD:D_SOD-323"')
        out.append('\t\t(layer "F.Cu")')
        out.append(f'\t\t(at {dx:.3f} {dy:.3f})')
        out.append(f'\t\t(property "Reference" "{ref}" (at 0 -1.3 0) (layer "F.SilkS") (effects (font (size 0.7 0.7) (thickness 0.1))))')
        out.append('\t\t(property "Value" "1N4148WS" (at 0 1.3 0) (layer "F.Fab") (effects (font (size 0.7 0.7) (thickness 0.1))))')
        out.append(f'\t\t(pad "1" smd roundrect (at -1.05 0) (size 0.6 0.45) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net {a_net} "{a_name}"))')
        out.append('\t\t(pad "2" smd roundrect (at 1.05 0) (size 0.6 0.45) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 3 "VCC_5V_PROT"))')
        out.append(f'\t\t(model "{kicad10_3d_dir}/Diode_SMD.3dshapes/D_SOD-323.step"')
        out.append('\t\t\t(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
        out.append('\t)')

    # 10. Footprint J_ACT: JST-SH 1.0mm 8-Pin Horizontal on F.Cu at (132.5, 75.0, rot=90)
    out.append('\t(footprint "Connector_JST:JST_SH_SM08B-SRSS-TB_1x08-1MP_P1.00mm_Horizontal"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 132.500 75.000 90)')
    out.append('\t\t(property "Reference" "J_ACT" (at 0 -4.5 90) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "ACTUATORS_8P" (at 0 4.5 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    
    j_act_pads = [
        (1, -3.50, -2.00, 3, "VCC_5V_PROT"),
        (2, -2.50, -2.00, 3, "VCC_5V_PROT"),
        (3, -1.50, -2.00, 16, "ACT_PLUS"),
        (4, -0.50, -2.00, 17, "ACT_MINUS"),
        (5,  0.50, -2.00, 18, "ACT_CENTER"),
        (6,  1.50, -2.00, 19, "ACT_MESH"),
        (7,  2.50, -2.00, 1, "GND"),
        (8,  3.50, -2.00, 1, "GND"),
    ]
    for p_num, px, py, n_id, n_name in j_act_pads:
        out.append(f'\t\t(pad "{p_num}" smd roundrect (at {px:.3f} {py:.3f} 90) (size 0.6 1.55) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net {n_id} "{n_name}"))')
        
    out.append('\t\t(pad "MP" smd roundrect (at -4.80 1.88 90) (size 1.2 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
    out.append('\t\t(pad "MP" smd roundrect (at 4.80 1.88 90) (size 1.2 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Connector_JST.3dshapes/JST_SH_SM08B-SRSS-TB_1x08-1MP_P1.00mm_Horizontal.step"')
    out.append('\t\t\t(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
    out.append('\t)')

    # 11. Footprint J2: JST-SH 1.0mm 6-Pin Horizontal on F.Cu at (132.5, 85.0, rot=90)
    out.append('\t(footprint "Connector_JST:JST_SH_SM06B-SRSS-TB_1x06-1MP_P1.00mm_Horizontal"')
    out.append('\t\t(layer "F.Cu")')
    out.append('\t\t(at 132.500 85.000 90)')
    out.append('\t\t(property "Reference" "J2" (at 0 -3.5 90) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    out.append('\t\t(property "Value" "INTERCOM_HEADSET_6P" (at 0 3.5 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    
    j2_pads = [
        (1, -2.50, -2.00, 3, "VCC_5V_PROT"),
        (2, -1.50, -2.00, 1, "GND"),
        (3, -0.50, -2.00, 4, "POD_NF_P"),
        (4,  0.50, -2.00, 5, "POD_NF_N"),
        (5,  1.50, -2.00, 20, "MIC_IN+"),
        (6,  2.50, -2.00, 21, "RESERVE_IO"),
    ]
    for p_num, px, py, n_id, n_name in j2_pads:
        out.append(f'\t\t(pad "{p_num}" smd roundrect (at {px:.3f} {py:.3f} 90) (size 0.6 1.55) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net {n_id} "{n_name}"))')
        
    out.append('\t\t(pad "MP" smd roundrect (at -3.80 1.88 90) (size 1.2 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
    out.append('\t\t(pad "MP" smd roundrect (at 3.80 1.88 90) (size 1.2 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "GND"))')
    out.append(f'\t\t(model "{kicad10_3d_dir}/Connector_JST.3dshapes/JST_SH_SM06B-SRSS-TB_1x06-1MP_P1.00mm_Horizontal.step"')
    out.append('\t\t\t(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
    out.append('\t)')

    # 12. 4x Mounting Holes H1..H4 (M2 Pad with 2.2mm drill in 4 corners)
    holes = [
        ("H1", 103.0, 70.5),
        ("H2", 103.0, 89.5),
        ("H3", 132.0, 70.5),
        ("H4", 132.0, 89.5),
    ]
    for ref, hx, hy in holes:
        out.append('\t(footprint "MountingHole:MountingHole_2.2mm_M2_Pad"')
        out.append('\t\t(layer "F.Cu")')
        out.append(f'\t\t(at {hx:.2f} {hy:.2f})')
        out.append(f'\t\t(property "Reference" "{ref}" (at 0 -2.8 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
        out.append('\t\t(property "Value" "M2_MountingHole" (at 0 2.8 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
        out.append('\t\t(pad "1" thru_hole circle (at 0 0) (size 3.4 3.4) (drill 2.2) (layers "*.Cu" "*.Mask") (net 1 "GND"))')
        out.append('\t)')

    # 13. Silkscreen Labels
    out.append('\t(gr_text "PCBA 03 // SMART CARTRIDGE Rev 2.0" (at 116.5 69.0 0) (layer "F.SilkS") (effects (font (size 0.45 0.45) (thickness 0.09))))')
    out.append('\t(gr_text "J1 DOCKING" (at 106.0 71.5 0) (layer "F.SilkS") (effects (font (size 0.35 0.35) (thickness 0.07))))')
    out.append('\t(gr_text "CH32V003 RISC-V MCU" (at 116.5 75.8 0) (layer "F.SilkS") (effects (font (size 0.38 0.38) (thickness 0.08))))')
    out.append('\t(gr_text "J_ACT (8P)" (at 130.0 69.2 0) (layer "F.SilkS") (effects (font (size 0.35 0.35) (thickness 0.07))))')
    out.append('\t(gr_text "J2 (6P)" (at 130.0 91.2 0) (layer "F.SilkS") (effects (font (size 0.35 0.35) (thickness 0.07))))')

    out.append('\t(gr_text "OPENMOTORBRIDGE v8.2" (at 117.5 78.0 0) (layer "B.SilkS") (effects (font (size 0.60 0.60) (thickness 0.11)) (justify mirror)))')
    out.append('\t(gr_text "SMART MODULAR CARTRIDGE Trägerplatine (B.Cu)" (at 117.5 83.0 0) (layer "B.SilkS") (effects (font (size 0.45 0.45) (thickness 0.09)) (justify mirror)))')
    out.append('\t(gr_text "GND SHIELD PLANE" (at 117.5 88.0 0) (layer "B.SilkS") (effects (font (size 0.40 0.40) (thickness 0.08)) (justify mirror)))')

    out.append(')')
    
    with open(pcb_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
        
    print(f"✓ Successfully generated clean pre-placed Cartridge PCB Rev 2.0 at {pcb_file}")

    # Generate 3D Renders using KiCad CLI
    if os.path.exists(kicad_cli):
        pcb_dir = os.path.dirname(os.path.abspath(pcb_file))
        out_top = os.path.join(pcb_dir, "cartridge_3d_render_top.png")
        out_bot = os.path.join(pcb_dir, "cartridge_3d_render_bottom.png")
        out_persp = os.path.join(pcb_dir, "cartridge_3d_render_perspective.png")

        subprocess.run([kicad_cli, 'pcb', 'render', '--output', out_top, '--zoom', '1.05', '--side', 'top', pcb_file], check=True)
        subprocess.run([kicad_cli, 'pcb', 'render', '--output', out_bot, '--zoom', '1.05', '--side', 'bottom', pcb_file], check=True)
        subprocess.run([kicad_cli, 'pcb', 'render', '--output', out_persp, '--zoom', '0.85', '--rotate', '45,0,-30', '--perspective', pcb_file], check=True)
        print(f"✓ Generated high-res 3D renders:\n  - {out_top}\n  - {out_bot}\n  - {out_persp}")

if __name__ == '__main__':
    generate_cartridge_pcb()
