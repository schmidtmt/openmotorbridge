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
        'U1': ('${KICAD10_3DMODEL_DIR}/RF_Module.3dshapes/ESP32-C3-WROOM-02.step', (0.0, 0.0, 0.0)),
        'U2': ('${KICAD10_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/ArtInChip_QFN-88-1EP_10x10mm_P0.4mm_EP6.74x6.74mm.step', (0.0, 0.0, 0.0)),
        'U3': ('${KICAD10_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm.step', (0.0, 0.0, 0.0)),
        'U4': ('${KICAD10_3DMODEL_DIR}/Package_TO_SOT_SMD.3dshapes/SOT-23.step', (0.0, 0.0, 0.0)),
        'J1': ('${KICAD10_3DMODEL_DIR}/Connector_PinHeader_2.54mm.3dshapes/PinHeader_1x06_P2.54mm_Horizontal.step', (0.0, 0.0, 90.0)),
        'ANT1': ('${KICAD10_3DMODEL_DIR}/Connector_Coaxial.3dshapes/U.FL_Hirose_U.FL-R-SMT-1_Vertical.step', (0.0, 0.0, 0.0)),
        'ANT2': ('${KICAD10_3DMODEL_DIR}/Connector_Coaxial.3dshapes/U.FL_Hirose_U.FL-R-SMT-1_Vertical.step', (0.0, 0.0, 0.0)),
        'L1': ('${KICAD10_3DMODEL_DIR}/Inductor_SMD.3dshapes/L_0603_1608Metric.step', (0.0, 0.0, 0.0)),
        'D1': ('${KICAD10_3DMODEL_DIR}/Diode_SMD.3dshapes/D_SOD-323.step', (0.0, 0.0, 0.0)),
        'C1': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0805_2012Metric.step', (0.0, 0.0, 0.0)),
        'C2': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step', (0.0, 0.0, 0.0)),
        'C3': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step', (0.0, 0.0, 0.0)),
        'C4': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step', (0.0, 0.0, 0.0)),
    }

    # Verified Layout Matrix (in mm)
    layout_rules = {
        # 4 Corner M3 Mounting Holes (3.5 mm inset)
        'H1': (X0 + 3.5, Y0 + 3.5, 0.0, pcbnew.F_Cu),    # (103.5, 73.5)
        'H2': (X_max - 3.5, Y0 + 3.5, 0.0, pcbnew.F_Cu), # (146.5, 73.5)
        'H3': (X0 + 3.5, Y_max - 3.5, 0.0, pcbnew.F_Cu), # (103.5, 101.5)
        'H4': (X_max - 3.5, Y_max - 3.5, 0.0, pcbnew.F_Cu),# (146.5, 101.5)

        # Primary Active Components (Top Layer)
        'U1': (125.0, 84.5, 0.0, pcbnew.F_Cu),           # ESP32-C3-WROOM-02 (Antenna top)
        'U2': (114.0, 96.5, 0.0, pcbnew.F_Cu),           # u-blox MAX-M10S GNSS
        'U3': (137.0, 96.0, 0.0, pcbnew.F_Cu),           # Semtech SX1262 LoRa
        'U4': (125.0, 92.5, 0.0, pcbnew.F_Cu),           # DS2401 Silicon ROM ID

        # RF Antennas / U.FL Ports
        'ANT1': (144.0, 90.0, 0.0, pcbnew.F_Cu),         # 868 MHz LoRa RF Port
        'ANT2': (108.0, 90.0, 0.0, pcbnew.F_Cu),         # GNSS RF Port

        # Standardized 6-Pin Pogo Matrix Interface (UART Push Flashing Capable)
        'J1': (125.0, 99.0, 90.0, pcbnew.F_Cu),          # 6-Pin Interface (Horizontal)

        # Passives & RF Protection
        'L1': (142.5, 96.0, 0.0, pcbnew.F_Cu),           # 47nH RF Choke for SX1262
        'D1': (119.0, 99.0, 0.0, pcbnew.F_Cu),           # TVS Diode for 1-Wire Line
        'C1': (119.0, 84.5, 0.0, pcbnew.F_Cu),           # 10uF 3V3 Decoupling
        'C2': (131.0, 84.5, 0.0, pcbnew.F_Cu),           # 100nF ESP32
        'C3': (114.0, 90.5, 0.0, pcbnew.F_Cu),           # 100nF GNSS
        'C4': (137.0, 90.5, 0.0, pcbnew.F_Cu),           # 100nF LoRa

        # Factory Testpoints (Placed cleanly on Bottom Layer B_Cu)
        'TP1': (115.0, 80.0, 0.0, pcbnew.B_Cu),          # TP_BOOT (GPIO9)
        'TP2': (118.0, 80.0, 0.0, pcbnew.B_Cu),          # TP_RST (CHIP_PU)
        'TP3': (132.0, 80.0, 0.0, pcbnew.B_Cu),          # TP_TX (GPIO21)
        'TP4': (135.0, 80.0, 0.0, pcbnew.B_Cu),          # TP_RX (GPIO20)
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

        # Hide testpoint reference text on silk
        if ref.startswith('TP'):
            fp.Reference().SetVisible(False)

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

    # Add clean silkscreen labels
    drawings_to_remove = []
    for d in board.GetDrawings():
        if isinstance(d, pcbnew.PCB_TEXT) and d.GetLayer() == pcbnew.F_SilkS:
            drawings_to_remove.append(d)
    for d in drawings_to_remove:
        board.Remove(d)

    labels = [
        ("GNSS (1.575 GHz)", 108.0, 85.0, 0.85, 0.85, 0.15),
        ("868MHz LoRa", 143.0, 85.0, 0.85, 0.85, 0.15),
        ("POGO: VCC GND TX RX PPS 1W", 125.0, 103.5, 0.75, 0.75, 0.14),
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
    print(f"\nSuccessfully auto-placed Rear POD 3 PCB on {pcb_path} with bottom testpoints!\n")

if __name__ == '__main__':
    pcb_file = 'hardware/kicad_rear_pod3/openmotorbridge_rear_pod3.kicad_pcb'
    if len(sys.argv) > 1:
        pcb_file = sys.argv[1]
    auto_place_rear_pod(pcb_file)
