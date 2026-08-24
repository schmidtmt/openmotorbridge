#!/usr/bin/env python3
"""
OpenMotorBridge Universal Pod Cartridge Auto-Placement & Low-Profile Model Binder
---------------------------------------------------------------------------------
Harmonizes and populates the 35x25mm Pod Cartridge Carrier PCB for Sena/Cardo Inlays:
- J1: 6-Pin Mill-Max ENIG Gold Target Pad Array (Left Stirnwand edge, matching Pod Base Pogo Pins)
- J2: JST-SH 1.0mm 6-Pin Right-Angle Low-Profile Flex Header (Facing +X towards Sena OEM Inlay)
- U1: Maxim DS2401 Silicon Serial ROM ID in SOT-23 (Center)
- C1: 100nF Decoupling Capacitor 0603 (Center)
- H1, H2: 2x M2 Mounting Insets with Silicone Vibration Damping Bushings
"""

import sys
import os
import pcbnew

def auto_place_cartridge(pcb_path):
    print(f"Loading/Creating Cartridge Carrier PCB: {pcb_path}")
    os.makedirs(os.path.dirname(os.path.abspath(pcb_path)), exist_ok=True)
    board = pcbnew.BOARD()

    # Board Dimensions: 35.0 x 25.0 mm (X: 100.0 .. 135.0, Y: 67.5 .. 92.5, Center: 117.5, 80.0)
    X0 = 100.0
    Y0 = 67.5
    W = 35.0
    H = 25.0
    X_center = X0 + W / 2.0  # 117.5 mm
    Y_center = Y0 + H / 2.0  # 80.0 mm (matches Pod Base Y_center exactly)

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

    # 3D Model Mapping (Ultra-Low-Profile & Right-Angle Components)
    model_mapping = {
        'J1': ('${KICAD10_3DMODEL_DIR}/Connector_PinHeader_2.54mm.3dshapes/PinHeader_1x06_P2.54mm_Horizontal.step', (0.0, 0.0, 90.0)),
        'J2': ('${KICAD10_3DMODEL_DIR}/Connector_JST.3dshapes/JST_SH_SM06B-SRSS-TB_1x06-1MP_P1.00mm_Horizontal.step', (0.0, 0.0, 0.0)),
        'U1': ('${KICAD10_3DMODEL_DIR}/Package_TO_SOT_SMD.3dshapes/SOT-23.step', (0.0, 0.0, 0.0)),
        'C1': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step', (0.0, 0.0, 0.0)),
    }

    # Verified Layout Matrix (in mm)
    layout_rules = {
        # 2 M2 Side Mounting Holes with Silicone Damping Bushings (Shore 40A)
        'H1': (X0 + 4.0, Y0 + 4.0, 0.0),             # (104.0, 71.5) Top-Left Mounting Hole
        'H2': (X0 + 4.0, Y0 + H - 4.0, 0.0),         # (104.0, 88.5) Bottom-Left Mounting Hole

        # 6-Pin Mill-Max Target Pad Array (Linke Stirnkante, zentriert auf Y = 80.0 mm)
        'J1': (X0 + 2.5, Y_center, 90.0),            # (102.5, 80.0) - Trifft 1:1 auf Pod-Base Pogo-Pins!

        # JST-SH 1.0mm 6-Pin Header (Rechte Seite, Öffnung zeigt nach rechts zum Sena Inlay)
        'J2': (X0 + 24.0, Y_center, 0.0),            # (124.0, 80.0) - Flexkabel zum Sena Apex Modul

        # Active ID Chip & Passives (Center-Mitte)
        'U1': (X_center, Y_center - 4.5, 0.0),       # (117.5, 75.5) DS2401 Silicon ROM
        'C1': (X_center, Y_center + 4.5, 0.0),       # (117.5, 84.5) 100nF Decoupling Cap
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

    # Add clear silkscreen labels
    labels = [
        ("SENA / CARDO CARRIER", X_center, Y0 + 2.5, 0.60, 0.60, 0.12),
        ("DS2401 ID", X_center, Y_center - 5.5, 0.45, 0.45, 0.10),
        ("JST-SH 6P (TO OEM INLAY)", X_center + 2.0, Y0 + H - 2.5, 0.45, 0.45, 0.10),
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
    print(f"\n✓ Successfully saved Cartridge Carrier PCB on {pcb_path}!\n")

if __name__ == '__main__':
    pcb_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb'))
    if len(sys.argv) > 1:
        pcb_file = sys.argv[1]
    auto_place_cartridge(pcb_file)

