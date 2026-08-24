#!/usr/bin/env python3
"""
OpenMotorBridge Pod Base PCB Generator & Auto-Placement Script
--------------------------------------------------------------
Generates and populates the 24.0 x 14.0 mm Pod-Base PCB (`openmotorbridge_pod_base.kicad_pcb`):
- J1: Mill-Max 824-22-006-00-001101 6-Pin Spring-Loaded Pogo Pin Header (2.54mm pitch)
- U1: Littelfuse SP3012-06UTG 6-Channel Ultra-Low Capacitance (<0.5pF) TVS ESD Array
- C1: 100nF 50V 0603 Ceramic Filter/Decoupling Capacitor
- J2: M8 6-Pin Chassis Receptacle Interface Solder / Wire Connection Pad Array
- H1, H2: 2x M2 Mounting Holes with Shore 40A Silicone Vibration Decoupling
"""

import sys
import os
import pcbnew

def generate_pod_base_pcb(pcb_path):
    print(f"Creating/Loading Pod-Base PCB: {pcb_path}")
    os.makedirs(os.path.dirname(os.path.abspath(pcb_path)), exist_ok=True)
    
    board = pcbnew.BOARD()

    # Board Dimensions: 24.0 x 14.0 mm
    X0 = 100.0
    Y0 = 70.0
    W = 24.0
    H = 14.0
    X_center = X0 + W / 2.0  # 112.0 mm
    Y_center = Y0 + H / 2.0  # 77.0 mm

    # 1. Create Board Outline (Edge.Cuts) with rounded chamfers
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
        'J1': ('${KICAD10_3DMODEL_DIR}/Connector_PinHeader_2.54mm.3dshapes/PinHeader_1x06_P2.54mm_Vertical.step', (0.0, 0.0, 0.0)),
        'U1': ('${KICAD10_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/DFN-14-1EP_3x3mm_P0.4mm_EP1.78x2.35mm.step', (0.0, 0.0, 0.0)),
        'C1': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step', (0.0, 0.0, 0.0)),
        'J2': ('${KICAD10_3DMODEL_DIR}/Connector_PinHeader_2.54mm.3dshapes/PinHeader_1x07_P2.54mm_Horizontal.step', (0.0, 0.0, 0.0)),
    }

    layout_rules = {
        # 2 M2 Mounting Holes with Silicone Damping
        'H1': (X0 + 2.5, Y_center, 0.0),       # (102.5, 77.0) Left
        'H2': (X0 + W - 2.5, Y_center, 0.0),   # (121.5, 77.0) Right

        # Mill-Max 6-Pin Pogo Pin Header (Top half, protruding upwards into cassette bay)
        'J1': (X_center, Y0 + 3.2, 90.0),      # (112.0, 73.2) - Horizontal Left to Right

        # Littelfuse SP3012 6-Channel TVS ESD Protection Array (Center)
        'U1': (X_center, Y_center, 0.0),       # (112.0, 77.0)
        'C1': (X_center + 4.5, Y_center, 0.0), # (116.5, 77.0) 100nF VCC Decoupling

        # M8 Receptacle 6-Pin + Shield Interface Pad Block (Bottom edge, pins pointing down)
        'J2': (X_center, Y0 + H - 2.5, 270.0), # (112.0, 81.5) - Horizontal, pins facing downwards
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
            model_file, (rx, ry, rz) = model_mapping[ref]
            fp.Models().clear()
            m = pcbnew.FP_3DMODEL()
            m.m_Filename = model_file
            m.m_Scale = pcbnew.VECTOR3D(1.0, 1.0, 1.0)
            m.m_Offset = pcbnew.VECTOR3D(0.0, 0.0, 0.0)
            m.m_Rotation = pcbnew.VECTOR3D(rx, ry, rz)
            m.m_Show = True
            fp.Add3DModel(m)

        print(f"  ✓ Placed {ref:4s} at ({x_mm:6.2f}, {y_mm:6.2f}) mm, rot={rot_deg:5.1f}°")

    # 3. Add Silkscreen Labels
    labels = [
        ("MILL-MAX POGO 6P", X_center, Y0 + 1.2, 0.55, 0.55, 0.12),
        ("SP3012 ESD", X_center - 3.5, Y_center + 1.2, 0.45, 0.45, 0.10),
        ("M8 CHASSIS INTERFACE (6P+SHIELD)", X_center, Y0 + H - 0.7, 0.48, 0.48, 0.10),
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
    print(f"✓ Saved Pod-Base PCB successfully: {pcb_path}")

if __name__ == '__main__':
    default_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../kicad_pod_base/openmotorbridge_pod_base.kicad_pcb'))
    generate_pod_base_pcb(default_path)
