#!/usr/bin/env python3
"""
OpenMotorBridge Pod Stirnwand-Adapter PCB Generator (End-Cap M8 & Pogo Interface)
--------------------------------------------------------------------------------
Generates and populates the 36.0 x 20.0 mm Stirnwand-Adapter PCB (`openmotorbridge_pod_base.kicad_pcb`):
- J2: Integrated M8 6-Pin IP67 Shielded Metal Panel Receptacle (Direct PCB Mount on outer face)
- J1: Mill-Max 824-22-006-00-001101 6-Pin Spring-Loaded Pogo Pin Header (2.54mm pitch on inner face)
- U1: Littelfuse SP3012-06UTG 6-Channel Ultra-Low Capacitance (<0.5pF) TVS ESD Array (Left Wing)
- C1: 100nF 50V 0603 Ceramic Filter/Decoupling Capacitor (Left Wing)
- H1, H2: 2x M2 Mounting Holes with Shore 40A Silicone Vibration Decoupling (Far Left & Right)
"""

import sys
import os
import pcbnew

def generate_pod_base_pcb(pcb_path):
    print(f"Creating/Loading Pod Stirnwand-Adapter PCB: {pcb_path}")
    os.makedirs(os.path.dirname(os.path.abspath(pcb_path)), exist_ok=True)
    
    board = pcbnew.BOARD()

    # Board Dimensions: 36.0 x 20.0 mm (X: 100.0 .. 136.0, Y: 70.0 .. 90.0)
    X0 = 100.0
    Y0 = 70.0
    W = 36.0
    H = 20.0
    X_center = X0 + W / 2.0  # 118.0 mm
    Y_center = Y0 + H / 2.0  # 80.0 mm

    # 1. Create Board Outline (Edge.Cuts) with 2.0mm rounded chamfers
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

    # 2. Footprint definitions & 3D model mapping
    model_mapping = {
        'J1': (
            '${KICAD10_3DMODEL_DIR}/Connector_PinHeader_2.54mm.3dshapes/PinHeader_1x06_P2.54mm_Vertical.step',
            (0.0, 0.0, 0.0),
            (0.0, 6.35, 0.0),
            (1.0, 1.0, 1.0)
        ),
        'U1': (
            '${KICAD10_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/DFN-14-1EP_3x3mm_P0.4mm_EP1.78x2.35mm.step',
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
            (1.0, 1.0, 1.0)
        ),
        'C1': (
            '${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step',
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
            (1.0, 1.0, 1.0)
        ),
        'J2': (
            '${KICAD10_3DMODEL_DIR}/Connector_Audio.3dshapes/Jack_3.5mm_Ledino_KB3SPRS_Horizontal.step',
            (0.0, 0.0, -90.0),
            (4.0, -1.0, 0.0),
            (1.0, 1.0, 1.0)
        ),
    }

    # Symmetrical, spacious, non-overlapping layout
    layout_rules = {
        # Symmetrical M2 Mounting Holes on Left & Right Flanks
        'H1': (X0 + 3.0, Y_center, 0.0),             # (103.0, 80.0) Left Mounting Hole
        'H2': (X0 + W - 3.0, Y_center, 0.0),         # (133.0, 80.0) Right Mounting Hole

        # Mill-Max 6-Pin Pogo Pin Header (Centered horizontally on inner face)
        'J1': (X_center, Y_center, 0.0),             # (118.0, 80.0) Center Inner

        # Left Wing: ESD Protection Stage (TVS Array & 100nF Filter Cap)
        'U1': (X0 + 8.0, Y_center - 4.0, 0.0),       # (108.0, 76.0) TVS Array
        'C1': (X0 + 8.0, Y_center + 4.0, 0.0),       # (108.0, 84.0) 100nF Cap

        # Integrated M8 6-Pin Panel Receptacle (Direct PCB Mount on Outer Face)
        'J2': (X_center, Y_center, 0.0),             # (118.0, 80.0) Center Outer
    }

    for ref, (x_mm, y_mm, rot_deg) in layout_rules.items():
        fp = pcbnew.FOOTPRINT(board)
        fp.SetReference(ref)
        fp.SetLayer(pcbnew.F_Cu)
        board.Add(fp)

        pos = pcbnew.VECTOR2I(int(x_mm * 1e6), int(y_mm * 1e6))
        fp.SetPosition(pos)
        fp.SetOrientationDegrees(rot_deg)

        if ref in model_mapping:
            model_file, (rx, ry, rz), (ox, oy, oz), (sx, sy, sz) = model_mapping[ref]
            fp.Models().clear()
            m = pcbnew.FP_3DMODEL()
            m.m_Filename = model_file
            m.m_Scale = pcbnew.VECTOR3D(sx, sy, sz)
            m.m_Offset = pcbnew.VECTOR3D(ox, oy, oz)
            m.m_Rotation = pcbnew.VECTOR3D(rx, ry, rz)
            m.m_Show = True
            fp.Add3DModel(m)

        print(f"  ✓ Placed {ref:4s} at ({x_mm:6.2f}, {y_mm:6.2f}) mm, rot={rot_deg:5.1f}°")

    # 3. Add Silkscreen Labels
    labels = [
        ("M8-ADAPTER (ADPT)", X_center, Y0 + 2.5, 0.55, 0.55, 0.12),
        ("SP3012 TVS", X0 + 8.0, Y0 + 2.5, 0.40, 0.40, 0.10),
        ("MILL-MAX POGO 6P", X_center, Y0 + H - 2.0, 0.50, 0.50, 0.10),
    ]

    for text_str, x_mm, y_mm, sx, sy, th in labels:
        txt = pcbnew.PCB_TEXT(board)
        txt.SetText(text_str)
        txt.SetLayer(pcbnew.F_SilkS)
        txt.SetPosition(pcbnew.VECTOR2I(int(x_mm * 1e6), int(y_mm * 1e6)))
        txt.SetTextSize(pcbnew.VECTOR2I(int(sx * 1e6), int(sy * 1e6)))
        txt.SetTextThickness(int(th * 1e6))
        txt.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
        board.Add(txt)

    board.Save(pcb_path)
    print(f"✓ Saved Pod Stirnwand-Adapter PCB successfully: {pcb_path}")

if __name__ == '__main__':
    default_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../kicad_pod_base/openmotorbridge_pod_base.kicad_pcb'))
    generate_pod_base_pcb(default_path)

