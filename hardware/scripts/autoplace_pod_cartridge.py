#!/usr/bin/env python3
"""
OpenMotorBridge Universal Pod Cartridge Auto-Placement & Low-Profile Model Binder
---------------------------------------------------------------------------------
Harmonizes and populates the 35x25mm Pod Cartridge PCB for ultra-slim cassette integration:
- J1: 6-Pin Mill-Max SMD Target Pad Array (Low-Profile, 1.0mm height, Bottom-facing)
- J2: 6-Pin Right-Angle Low-Profile Intercom Header (Horizontal side-entry, <2.0mm height)
- U1: Maxim DS2401 Silicon Serial ROM ID in SOT-23 (Center)
- C1: Decoupling Capacitor 0603
- H1, H2: 2x M2 Mounting Insets with Silicone Vibration Damping Bushings
"""

import sys
import os
import pcbnew

def auto_place_cartridge(pcb_path):
    print(f"Loading Cartridge PCB: {pcb_path}")
    board = pcbnew.LoadBoard(pcb_path)

    # Board Dimensions: 35.0 x 25.0 mm (X: 100.0 .. 135.0, Y: 70.0 .. 95.0)
    X0 = 100.0
    Y0 = 70.0
    W = 35.0
    H = 25.0
    X_center = X0 + W / 2.0  # 117.5 mm
    Y_center = Y0 + H / 2.0  # 82.5 mm

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
        'H1': (X0 + 3.5, Y_center, 0.0),    # (103.5, 82.5) Left
        'H2': (X0 + W - 3.5, Y_center, 0.0),# (131.5, 82.5) Right

        # 6-Pin Mill-Max Target Pad Array (Bottom edge, low-profile)
        'J1': (X_center, Y0 + H - 3.5, 0.0),# (117.5, 91.5)

        # 6-Pin Right-Angle Low-Profile Intercom Inlay Connector (Top edge, opening facing outward/upward)
        'J2': (X_center, Y0 + 4.5, 180.0),   # (117.5, 74.5) - Cable plugs in straight from top

        # Active ID Chip & Passives (Center)
        'U1': (X_center, Y_center, 0.0),     # (117.5, 82.5) DS2401 Silicon ROM
        'C1': (X_center + 4.5, Y_center, 0.0), # (122.0, 82.5) 100nF Decoupling
    }

    existing_refs = {fp.GetReference(): fp for fp in board.Footprints()}

    for ref, (x_mm, y_mm, rot_deg) in layout_rules.items():
        if ref in existing_refs:
            fp = existing_refs[ref]
        else:
            fp = pcbnew.FOOTPRINT(board)
            fp.SetReference(ref)
            fp.SetLayer(pcbnew.F_Cu)
            board.Add(fp)
            existing_refs[ref] = fp

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
    drawings_to_remove = []
    for d in board.GetDrawings():
        if isinstance(d, pcbnew.PCB_TEXT) and d.GetLayer() == pcbnew.F_SilkS:
            drawings_to_remove.append(d)
    for d in drawings_to_remove:
        board.Remove(d)

    labels = [
        ("OEM INLAY (JST-SH 6P)", 117.5, 78.5, 0.75, 0.75, 0.14),
        ("DS2401 ID", 117.5, 85.5, 0.75, 0.75, 0.14),
        ("POGO TARGET 6P (BOTTOM)", 117.5, 89.0, 0.70, 0.70, 0.13),
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
    print(f"\nSuccessfully auto-placed Cartridge PCB on {pcb_path} with low-profile models!\n")

if __name__ == '__main__':
    pcb_file = 'hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb'
    if len(sys.argv) > 1:
        pcb_file = sys.argv[1]
    auto_place_cartridge(pcb_file)
