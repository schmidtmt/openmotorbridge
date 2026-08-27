#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
OpenMotorBridge Pod Cartridge Carrier PCB Generator (KiCad Native)
------------------------------------------------------------------
Populates the 35x25mm Pod Cartridge Carrier PCB using official KiCad footprint libraries,
ensuring exact 90° CCW rotation for J2 (pads on left towards board center, receptacle opening facing right +X).
"""

import sys
import os
import subprocess
import pcbnew

kicad_fp_dir = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"
kicad_cli = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

pcb_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../kicad_pod_cartridge"))
os.makedirs(pcb_dir, exist_ok=True)
pcb_file = os.path.join(pcb_dir, "openmotorbridge_pod_cartridge.kicad_pcb")

def build_cartridge_pcb():
    board = pcbnew.BOARD()

    # Title Block
    tb = board.GetTitleBlock()
    tb.SetTitle("OpenMotorBridge v8.0 - Pod Cartridge Carrier PCB (35x25mm)")
    tb.SetDate("2026-08-27")
    tb.SetRevision("v8.0")
    tb.SetCompany("OpenMotorBridge Open Source Hardware")
    tb.SetComment(0, "Axial Inlay Cable Interface (JST-SH 1.0mm 6-Pin opening facing +X)")
    tb.SetComment(1, "Maxim DS2401 Silicon Serial ROM ID + PTC 500mA Protection")

    # Dimensions
    X0 = 100.0
    Y0 = 67.5
    W = 35.0
    H = 25.0
    X_center = X0 + W / 2.0  # 117.5 mm
    Y_center = Y0 + H / 2.0  # 80.0 mm

    # 1. Board Outline (Edge.Cuts) with 2.0 mm chamfers
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
        seg = pcbnew.PCB_SHAPE(board)
        seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        seg.SetLayer(pcbnew.Edge_Cuts)
        seg.SetWidth(int(0.15 * 1e6))
        p1 = pcbnew.VECTOR2I(int(pts[i][0] * 1e6), int(pts[i][1] * 1e6))
        p2 = pcbnew.VECTOR2I(int(pts[i+1][0] * 1e6), int(pts[i+1][1] * 1e6))
        seg.SetStart(p1)
        seg.SetEnd(p2)
        board.Add(seg)

    # 2. Netlist
    net_names = [
        "GND",
        "POD_VCC",
        "VCC_5V_PROT",
        "POD_NF_P",
        "POD_NF_N",
        "POD_OPTO_KEY",
        "POD_1WIRE_ID",
        "NET_LED_R",
    ]
    net_objs = {}
    for n in net_names:
        netinfo = pcbnew.NETINFO_ITEM(board, n)
        board.Add(netinfo)
        net_objs[n] = netinfo

    # 3. Footprint Placement
    # Footprints definition: (ref, lib, mod_name, x, y, rot_deg, layer)
    fp_defs = [
        # J1: 6-Pin 2.54mm Horizontal Socket on FRONT EDGE (Pins at X=102.5, opening at X=100 facing -X)
        ('J1', 'Connector_PinSocket_2.54mm.pretty', 'PinSocket_1x06_P2.54mm_Horizontal',
         102.5, 73.65, 0.0, pcbnew.F_Cu),

        # J2: JST-SH 1.0mm 6-Pin Horizontal Header on F.Cu at X=126.5, Y=80.0
        # In KiCad library: at rot=90, pads are at X=-2.0 (left, X=124.5), opening faces right (+X, towards X=135)
        ('J2', 'Connector_JST.pretty', 'JST_SH_SM06B-SRSS-TB_1x06-1MP_P1.00mm_Horizontal',
         126.5, Y_center, 90.0, pcbnew.F_Cu),

        # U1: Maxim DS2401 ID in SOT-23 on F.Cu
        ('U1', 'Package_TO_SOT_SMD.pretty', 'SOT-23',
         115.0, Y_center, 0.0, pcbnew.F_Cu),

        # C1: 100nF 0603 Cap
        ('C1', 'Capacitor_SMD.pretty', 'C_0603_1608Metric',
         115.0, Y_center + 4.5, 90.0, pcbnew.F_Cu),

        # F1: 500mA PTC Fuse 0603
        ('F1', 'Resistor_SMD.pretty', 'R_0603_1608Metric',
         108.0, 75.0, 90.0, pcbnew.F_Cu),

        # R1: 1.5k LED Resistor 0603
        ('R1', 'Resistor_SMD.pretty', 'R_0603_1608Metric',
         108.0, 82.5, 90.0, pcbnew.F_Cu),

        # D1: Power LED 0603
        ('D1', 'LED_SMD.pretty', 'LED_0603_1608Metric',
         108.0, 85.0, 90.0, pcbnew.F_Cu),

        # H1, H2: M2 Mounting Holes with Pads
        ('H1', 'MountingHole.pretty', 'MountingHole_2.2mm_M2_Pad',
         103.0, 70.5, 0.0, pcbnew.F_Cu),

        ('H2', 'MountingHole.pretty', 'MountingHole_2.2mm_M2_Pad',
         103.0, 89.5, 0.0, pcbnew.F_Cu),
    ]

    loaded_fps = {}
    for ref, lib, mod_name, x, y, rot, layer in fp_defs:
        lib_path = os.path.join(kicad_fp_dir, lib)
        fp = pcbnew.FootprintLoad(lib_path, mod_name)
        if not fp:
            print(f"Error loading {lib}/{mod_name}")
            continue
        fp.SetReference(ref)
        fp.Reference().SetVisible(False)  # Hide ref label to keep PCB clean
        fp.SetLayer(layer)
        board.Add(fp)

        pos = pcbnew.VECTOR2I(int(x * 1e6), int(y * 1e6))
        fp.SetPosition(pos)
        fp.SetOrientationDegrees(rot)
        loaded_fps[ref] = fp
        print(f"  ✓ Loaded & Placed {ref:4s} ({mod_name}) at ({x:6.2f}, {y:6.2f}) mm, rot={rot:5.1f}°")

    # 4. Net Assignments
    net_map = {
        'J1': {
            '1': 'POD_VCC',
            '2': 'GND',
            '3': 'POD_NF_P',
            '4': 'POD_NF_N',
            '5': 'POD_OPTO_KEY',
            '6': 'POD_1WIRE_ID',
        },
        'F1': {
            '1': 'POD_VCC',
            '2': 'VCC_5V_PROT',
        },
        'R1': {
            '1': 'VCC_5V_PROT',
            '2': 'NET_LED_R',
        },
        'D1': {
            '1': 'NET_LED_R',
            '2': 'GND',
        },
        'U1': {
            '1': 'POD_1WIRE_ID',
            '2': 'GND',
            '3': 'GND',
        },
        'C1': {
            '1': 'POD_1WIRE_ID',
            '2': 'GND',
        },
        'J2': {
            '1': 'GND',
            '2': 'VCC_5V_PROT',
            '3': 'POD_NF_P',
            '4': 'POD_NF_N',
            '5': 'POD_1WIRE_ID',
            '6': 'POD_OPTO_KEY',
        },
        'H1': {'1': 'GND'},
        'H2': {'1': 'GND'},
    }

    for ref, pads in net_map.items():
        if ref in loaded_fps:
            fp = loaded_fps[ref]
            for pad in fp.Pads():
                pname = pad.GetName()
                if pname in pads and pads[pname] in net_objs:
                    pad.SetNet(net_objs[pads[pname]])
                elif 'MP' in pname:
                    pad.SetNet(net_objs['GND'])

    # 5. Silkscreen Text
    top_labels = [
        ("OPENMOTORBRIDGE // CARRIER", 120.0, Y0 + 2.5, 0.55, 0.55, 0.11),
        ("FRONT MATING", 106.0, Y0 + 2.5, 0.40, 0.40, 0.08),
        ("DS2401 ID", 115.0, Y_center - 3.5, 0.35, 0.35, 0.08),
        ("PTC 500mA", 108.0, 72.5, 0.30, 0.30, 0.07),
        ("PWR LED", 108.0, 87.5, 0.30, 0.30, 0.07),
        ("AXIAL JST-SH (TO HEADSET)", 125.0, Y0 + H - 2.5, 0.40, 0.40, 0.09),
    ]

    for text_str, x_mm, y_mm, sx, sy, th in top_labels:
        txt = pcbnew.PCB_TEXT(board)
        txt.SetText(text_str)
        txt.SetLayer(pcbnew.F_SilkS)
        txt.SetPosition(pcbnew.VECTOR2I(int(x_mm * 1e6), int(y_mm * 1e6)))
        txt.SetTextSize(pcbnew.VECTOR2I(int(sx * 1e6), int(sy * 1e6)))
        txt.SetTextThickness(int(th * 1e6))
        txt.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
        board.Add(txt)

    bottom_labels = [
        ("OPENMOTORBRIDGE CARRIER (B.Cu)", X_center, Y_center, 0.45, 0.45, 0.10),
        ("GND SHIELD PLANE", X_center, Y0 + H - 2.5, 0.40, 0.40, 0.09),
    ]

    for text_str, x_mm, y_mm, sx, sy, th in bottom_labels:
        txt = pcbnew.PCB_TEXT(board)
        txt.SetText(text_str)
        txt.SetLayer(pcbnew.B_SilkS)
        txt.SetPosition(pcbnew.VECTOR2I(int(x_mm * 1e6), int(y_mm * 1e6)))
        txt.SetTextSize(pcbnew.VECTOR2I(int(sx * 1e6), int(sy * 1e6)))
        txt.SetTextThickness(int(th * 1e6))
        txt.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
        board.Add(txt)

    # Save board
    board.Save(pcb_file)
    print(f"\n✓ Saved clean KiCad board at {pcb_file}")

    # Generate 3D Renders
    out_top = os.path.join(pcb_dir, "cartridge_3d_render_top.png")
    out_bot = os.path.join(pcb_dir, "cartridge_3d_render_bottom.png")
    out_persp = os.path.join(pcb_dir, "cartridge_3d_render_perspective.png")

    subprocess.run([kicad_cli, 'pcb', 'render', '--output', out_top, '--zoom', '1.25', '--side', 'top', pcb_file], check=True)
    subprocess.run([kicad_cli, 'pcb', 'render', '--output', out_bot, '--zoom', '1.25', '--side', 'bottom', pcb_file], check=True)
    subprocess.run([kicad_cli, 'pcb', 'render', '--output', out_persp, '--zoom', '1.25', '--rotate', '45,0,-30', '--perspective', pcb_file], check=True)
    print(f"✓ Generated high-res 3D renders:\n  - {out_top}\n  - {out_bot}\n  - {out_persp}")

if __name__ == '__main__':
    build_cartridge_pcb()
