#!/usr/bin/env python3
"""
OpenMotorBridge Rear POD 3 Auto-Placement & Clear Silkscreen Binder
-------------------------------------------------------------------
Harmonizes and populates the 50x35mm Rear POD 3 OMM Transceiver PCB with:
- Horizontal 6-Pin Socket (J1) on the short leading edge (X=100mm)
- 500mA PTC Resettable Fuse (F1) & Green Power LED (D1) + Resistor (R1)
- ESP32-C3 2.4GHz HiFi Mesh Transceiver (U1)
- u-blox MAX-M10S Multi-GNSS Engine (U2) + U.FL GNSS Port (ANT2)
- Semtech SX1262 LoRa Transceiver (U3) + U.FL LoRa Port (ANT1)
- Maxim DS2401 Silicon Serial ROM ID (U4)
- 4 Symmetrical Corner M3 Mounting Holes (H1..H4)
- Factory Flashing / Production Testpoints on Bottom Layer (TP1..TP4)
"""

import sys
import os
import pcbnew

def auto_place_rear_pod(pcb_path):
    print(f"Loading Rear POD 3 PCB: {pcb_path}")
    board = pcbnew.LoadBoard(pcb_path)

    # Board Dimensions: 55.0 x 48.0 mm (X: 100.0 .. 155.0, Y: 72.0 .. 120.0)
    X0 = 100.0
    Y0 = 72.0
    W = 55.0
    H = 48.0
    X_max = X0 + W  # 155.0 mm
    Y_max = Y0 + H  # 120.0 mm
    Y_center = Y0 + H / 2.0  # 96.0 mm

    # 3D Model Mapping
    model_mapping = {
        'U1': ('${KICAD10_3DMODEL_DIR}/RF_Module.3dshapes/ESP32-C3-WROOM-02U.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'U2': ('${KICAD10_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'U3': ('${KICAD10_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'U4': ('${KICAD10_3DMODEL_DIR}/Package_TO_SOT_SMD.3dshapes/SOT-23.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'J1': ('${KICAD10_3DMODEL_DIR}/Connector_PinSocket_2.54mm.3dshapes/PinSocket_1x06_P2.54mm_Horizontal.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'J4': ('${KICAD10_3DMODEL_DIR}/Connector_Coaxial.3dshapes/U.FL_Hirose_U.FL-R-SMT-1_Vertical.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'J5': ('${KICAD10_3DMODEL_DIR}/Connector_Coaxial.3dshapes/U.FL_Hirose_U.FL-R-SMT-1_Vertical.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'F1': ('${KICAD10_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_1206_3216Metric.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'D1': ('${KICAD10_3DMODEL_DIR}/LED_SMD.3dshapes/LED_0805_2012Metric.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'R1': ('${KICAD10_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0603_1608Metric.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'C1': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0805_2012Metric.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'C2': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'C3': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'C4': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
    }

    # Verified Layout Matrix matching openmotorbridge_rear_pod3.kicad_pcb exactly
    layout_rules = {
        # 4 Corner M2 Mounting Holes (Matching base sled standoffs)
        'H1': (103.00,  86.50,   0.0, pcbnew.F_Cu),
        'H2': (103.00, 105.50,   0.0, pcbnew.F_Cu),
        'H3': (149.00,  86.50,   0.0, pcbnew.F_Cu),
        'H4': (149.00, 105.50,   0.0, pcbnew.F_Cu),

        # Front Connector, Protection & 1-Wire ID
        'J1': (102.50,  89.65,   0.0, pcbnew.F_Cu),
        'F1': (111.29,  89.75,   0.0, pcbnew.F_Cu),
        'C1': (113.75,  84.20,  90.0, pcbnew.F_Cu),
        'U4': (116.19, 103.05,   0.0, pcbnew.F_Cu),
        'C2': (111.25, 104.72,  90.0, pcbnew.F_Cu),
        'R1': (108.00, 109.08,  90.0, pcbnew.F_Cu),
        'D1': (108.00, 113.44, -90.0, pcbnew.F_Cu),

        # GNSS Subsystem (Top)
        'U2': (130.25,  78.15, 180.0, pcbnew.F_Cu),
        'C3': (117.75,  84.22,  90.0, pcbnew.F_Cu),
        'J5': (115.50,  76.03, 180.0, pcbnew.F_Cu),

        # LoRa Subsystem (Bottom)
        'U3': (122.00, 113.50,   0.0, pcbnew.F_Cu),
        'C4': (115.25, 107.78,  90.0, pcbnew.F_Cu),
        'J4': (142.25, 114.50,   0.0, pcbnew.F_Cu),

        # Central MCU Subsystem (ESP32-C3-WROOM-02U with U.FL)
        'U1': (138.00,  96.00, -90.0, pcbnew.F_Cu),
    }

    existing_refs = {fp.GetReference(): fp for fp in board.Footprints()}

    for ref, (x_mm, y_mm, rot_deg, layer) in layout_rules.items():
        if ref in existing_refs:
            fp = existing_refs[ref]
        else:
            fp = pcbnew.FOOTPRINT(board)
            fp.SetReference(ref)
            board.Add(fp)
            existing_refs[ref] = fp

        fp.SetLayer(layer)
        pos = pcbnew.VECTOR2I(int(x_mm * 1e6), int(y_mm * 1e6))
        fp.SetPosition(pos)
        fp.SetOrientationDegrees(rot_deg)
        fp.Reference().SetVisible(False) # Clean production look without reference clutter

        if ref in model_mapping:
            model_file, (rx, ry, rz), (ox, oy, oz) = model_mapping[ref]
            fp.Models().clear()
            m = pcbnew.FP_3DMODEL()
            m.m_Filename = model_file
            if ref == 'ANT2':
                m.m_Scale = pcbnew.VECTOR3D(0.9, 0.9, 1.0) # Compact 10x10x3mm SMT Patch
            elif ref == 'ANT1':
                m.m_Scale = pcbnew.VECTOR3D(0.6, 0.6, 0.6) # Compact 7x3mm Helical Coil
            else:
                m.m_Scale = pcbnew.VECTOR3D(1.0, 1.0, 1.0)
            m.m_Offset = pcbnew.VECTOR3D(ox, oy, oz)
            m.m_Rotation = pcbnew.VECTOR3D(rx, ry, rz)
            m.m_Show = True
            fp.Add3DModel(m)

        print(f"  ✓ Placed {ref:4s} on layer at ({x_mm:6.2f}, {y_mm:6.2f}) mm, rot={rot_deg:5.1f}°")

    # Add clean silkscreen labels
    drawings_to_remove = []
    for d in board.GetDrawings():
        if isinstance(d, pcbnew.PCB_TEXT) and (d.GetLayer() == pcbnew.F_SilkS or d.GetLayer() == pcbnew.B_SilkS):
            drawings_to_remove.append(d)
    for d in drawings_to_remove:
        board.Remove(d)

    top_labels = [
        ("OPENMOTORBRIDGE // OMM TRANSCEIVER", 125.0, 103.5, 0.45, 0.45, 0.09),
        ("FRONT MATING", 102.5, 74.0, 0.35, 0.35, 0.08),
        ("MAX-M10S", 116.5, 71.5, 0.32, 0.32, 0.07),
        ("GNSS PATCH", 126.5, 80.5, 0.32, 0.32, 0.07),
        ("SX1262", 116.5, 94.5, 0.32, 0.32, 0.07),
        ("868M LORA", 126.5, 94.5, 0.32, 0.32, 0.07),
        ("PTC", 108.5, 71.5, 0.28, 0.28, 0.06),
        ("LED", 108.5, 103.5, 0.28, 0.28, 0.06),
        ("DS2401 ID", 113.0, 84.5, 0.32, 0.32, 0.07),
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
        ("OPENMOTORBRIDGE // OMM TRANSCEIVER (B.Cu)", 125.0, 102.5, 0.50, 0.50, 0.11),
        ("FACTORY TESTPOINTS (PROD FLASH)", 130.0, 74.0, 0.45, 0.45, 0.10),
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

    board.Save(pcb_path)
    print(f"\nSuccessfully auto-placed Rear POD 3 PCB on {pcb_path} with horizontal front mating socket!\n")

if __name__ == '__main__':
    pcb_file = 'hardware/kicad_rear_pod3/openmotorbridge_rear_pod3.kicad_pcb'
    if len(sys.argv) > 1:
        pcb_file = sys.argv[1]
    auto_place_rear_pod(pcb_file)

