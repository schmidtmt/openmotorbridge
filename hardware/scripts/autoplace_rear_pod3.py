#!/usr/bin/env python3
"""
OpenMotorBridge Rear POD 3 Auto-Placement & Clear Silkscreen Binder
-------------------------------------------------------------------
Harmonizes and populates the 50x35mm Rear POD 3 PCB with crystal-clear,
unambiguous silkscreen labels and UART In-System Flashing architecture:
- ESP32-C3 2.4GHz HiFi Mesh Transceiver (Onboard Antenna)
- u-blox MAX-M10S Multi-GNSS Engine (U2)
- Semtech SX1262 LoRa Transceiver (U3)
- Maxim DS2401 Silicon Serial ROM ID (U4)
- 868 MHz LoRa RF Port (ANT1)
- GNSS 1.575 GHz RF Port (ANT2)
- Standardized 6-Pin Pogo Interface (J1, UART Push Flashing capable)
- Factory Flashing / Production Testpoints on Bottom Layer (TP1..TP4)
"""

import sys
import os
import pcbnew

def auto_place_rear_pod(pcb_path):
    print(f"Loading Rear POD 3 PCB: {pcb_path}")
    board = pcbnew.LoadBoard(pcb_path)

    # Board Dimensions: 50.0 x 35.0 mm (X: 100.0 .. 150.0, Y: 70.0 .. 105.0)
    X0 = 100.0
    Y0 = 70.0
    W = 50.0
    H = 35.0
    X_max = X0 + W  # 150.0 mm
    Y_max = Y0 + H  # 105.0 mm

    # 3D Model Mapping
    model_mapping = {
        'U1': ('${KICAD10_3DMODEL_DIR}/RF_Module.3dshapes/ESP32-C3-WROOM-02.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'U2': ('${KICAD10_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'U3': ('${KICAD10_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'U4': ('${KICAD10_3DMODEL_DIR}/Package_TO_SOT_SMD.3dshapes/SOT-23.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        # J1: 6-Pin 2.54mm Socket on Bottom (B.Cu) - Female socket pointing downward to mate with Pod-Base
        'J1': ('${KICAD10_3DMODEL_DIR}/Connector_PinSocket_2.54mm.3dshapes/PinSocket_1x06_P2.54mm_Vertical.step', (0.0, 0.0, 0.0), (0.0, 6.35, 0.0)),
        'ANT1': ('${KICAD10_3DMODEL_DIR}/Connector_Coaxial.3dshapes/U.FL_Hirose_U.FL-R-SMT-1_Vertical.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'ANT2': ('${KICAD10_3DMODEL_DIR}/Connector_Coaxial.3dshapes/U.FL_Hirose_U.FL-R-SMT-1_Vertical.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'L1': ('${KICAD10_3DMODEL_DIR}/Inductor_SMD.3dshapes/L_0603_1608Metric.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'D1': ('${KICAD10_3DMODEL_DIR}/LED_SMD.3dshapes/LED_0603_1608Metric.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'C1': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0805_2012Metric.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'C2': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'C3': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        'C4': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
    }

    # Verified Layout Matrix (in mm)
    layout_rules = {
        # 4 Corner M3 Mounting Holes (3.5 mm inset)
        'H1': (X0 + 3.5, Y0 + 3.5, 0.0, pcbnew.F_Cu),    # (103.5, 73.5) Top-Left
        'H2': (X_max - 3.5, Y0 + 3.5, 0.0, pcbnew.F_Cu), # (146.5, 73.5) Top-Right
        'H3': (X0 + 3.5, Y_max - 3.5, 0.0, pcbnew.F_Cu), # (103.5, 101.5) Bottom-Left
        'H4': (X_max - 3.5, Y_max - 3.5, 0.0, pcbnew.F_Cu),# (146.5, 101.5) Bottom-Right

        # Primary Active Components (ESP32 fully inside board boundary: Y 70.0 .. 105.0mm)
        'U1': (125.0, 86.0, 0.0, pcbnew.F_Cu),           # ESP32-C3 (Antenna moved safely down inside PCB outline)
        'U2': (109.0, 86.0, 0.0, pcbnew.F_Cu),           # u-blox MAX-M10S GNSS (Left Wing)
        'U3': (141.0, 86.0, 0.0, pcbnew.F_Cu),           # Semtech SX1262 LoRa (Right Wing)
        'U4': (110.0, 98.0, 0.0, pcbnew.F_Cu),           # DS2401 Silicon ROM ID (Bottom Left)

        # RF Antennas / U.FL Ports (Symmetrical Left & Right)
        'ANT2': (108.0, 76.0, 0.0, pcbnew.F_Cu),         # GNSS 1.575 GHz RF Port (Direct short trace to U2)
        'ANT1': (142.0, 76.0, 0.0, pcbnew.F_Cu),         # 868 MHz LoRa RF Port (Direct short trace to U3)

        # J1: 6-Pin Socket on UNTERSEITE (B.Cu) - Horizontal, centered below ESP32 with generous clearance!
        'J1': (125.0, 100.5, 90.0, pcbnew.B_Cu),         # 6-Pin Interface (Bottom layer B.Cu, Horizontal)

        # Passives & Status LEDs placed on flanks (leaving center channel completely free)
        'C1': (113.5, 92.5, 0.0, pcbnew.F_Cu),           # 10uF 3V3 Decoupling (Left flank)
        'C2': (136.5, 92.5, 0.0, pcbnew.F_Cu),           # 100nF ESP32 Decoupling (Right flank)
        'L1': (141.0, 91.5, 0.0, pcbnew.F_Cu),           # 47nH RF Choke for SX1262
        'D1': (140.0, 98.0, 0.0, pcbnew.F_Cu),           # Green Status / Mesh Activity LED (Bottom Right)
        'C3': (109.0, 91.5, 0.0, pcbnew.F_Cu),           # 100nF GNSS Decoupling
        'C4': (145.5, 91.5, 0.0, pcbnew.F_Cu),           # 100nF LoRa Decoupling

        # Factory Testpoints (Placed cleanly on Bottom Layer B_Cu)
        'TP1': (115.0, 78.0, 0.0, pcbnew.B_Cu),          # TP_BOOT (GPIO9)
        'TP2': (118.0, 78.0, 0.0, pcbnew.B_Cu),          # TP_RST (CHIP_PU)
        'TP3': (132.0, 78.0, 0.0, pcbnew.B_Cu),          # TP_TX (GPIO21)
        'TP4': (135.0, 78.0, 0.0, pcbnew.B_Cu),          # TP_RX (GPIO20)
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
        fp.Reference().SetVisible(False) # Clean, high-end production look without reference clutter

        if ref in model_mapping:
            model_file, (rx, ry, rz), (ox, oy, oz) = model_mapping[ref]
            fp.Models().clear()
            m = pcbnew.FP_3DMODEL()
            m.m_Filename = model_file
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
        ("OPENMOTORBRIDGE", 110.0, 71.8, 0.50, 0.50, 0.11),
        ("OMM TRANSCEIVER", 140.0, 71.8, 0.50, 0.50, 0.11),
        ("GNSS 1.575G", 110.0, 74.5, 0.40, 0.40, 0.09),
        ("868M LoRa", 140.0, 74.5, 0.40, 0.40, 0.09),
        ("MAX-M10S", 109.0, 81.0, 0.45, 0.45, 0.10),
        ("SX1262", 141.0, 81.0, 0.45, 0.45, 0.10),
        ("DS2401 ID", 110.0, 94.8, 0.40, 0.40, 0.09),
        ("STATUS LED", 140.0, 94.8, 0.40, 0.40, 0.09),
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
        ("6-PIN SOCKET (MATES TO POD-BASE)", 125.0, 102.5, 0.50, 0.50, 0.11),
        ("FACTORY TESTPOINTS (PROD FLASH)", 125.0, 74.0, 0.45, 0.45, 0.10),
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
    print(f"\nSuccessfully auto-placed Rear POD 3 PCB on {pcb_path} with bottom testpoints!\n")

if __name__ == '__main__':
    pcb_file = 'hardware/kicad_rear_pod3/openmotorbridge_rear_pod3.kicad_pcb'
    if len(sys.argv) > 1:
        pcb_file = sys.argv[1]
    auto_place_rear_pod(pcb_file)
