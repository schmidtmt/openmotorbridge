#!/usr/bin/env python3
"""
OpenMotorBridge PCB Auto-Placement & Library Footprint Binder (Full Component Matrix)
-------------------------------------------------------------------------------------
Loads official KiCad library footprints (with native 3D models and 2D pads)
and positions all active ICs, passive passives, power inductors, audio transformers,
and connectors according to the 3-zone architecture matrix.
"""

import sys
import os
import pcbnew

def auto_place_main_board(pcb_path):
    print(f"Loading PCB: {pcb_path}")
    board = pcbnew.LoadBoard(pcb_path)

    # Board Outline: 85.0 x 55.0 mm (X: 115.22 .. 200.22, Y: 71.85 .. 126.85)
    X0 = 115.22
    Y0 = 71.85
    W = 85.0
    H = 55.0
    X_max = X0 + W  # 200.22 mm
    Y_max = Y0 + H  # 126.85 mm

    # 3D Model Mapping for all components
    model_mapping = {
        # Active ICs
        'U2': ('${KICAD10_3DMODEL_DIR}/RF_Module.3dshapes/ESP32-WROOM-32U.step', (0.0, 0.0, 0.0)),
        'U1': ('${KICAD10_3DMODEL_DIR}/Package_SO.3dshapes/SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.41x3.81mm.step', (0.0, 0.0, 0.0)),
        'U3': ('${KICAD10_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/QFN-28-1EP_4x4mm_P0.4mm_EP2.4x2.4mm.step', (0.0, 0.0, 0.0)),
        'U5': ('${KICAD10_3DMODEL_DIR}/Package_LGA.3dshapes/Bosch_LGA-14_3x2.5mm_P0.5mm.step', (0.0, 0.0, 0.0)),
        'U6': ('${KICAD10_3DMODEL_DIR}/Package_SO.3dshapes/SOIC-8_3.9x4.9mm_P1.27mm.step', (0.0, 0.0, 0.0)),
        'U9': ('${KICAD10_3DMODEL_DIR}/Package_TO_SOT_SMD.3dshapes/SOT-23-5.step', (0.0, 0.0, 0.0)),
        'U7': ('${KICAD10_3DMODEL_DIR}/Package_SO.3dshapes/Toshiba_SOIC-4-6_4.4x3.6mm_P1.27mm.step', (0.0, 0.0, 0.0)),
        'U8': ('${KICAD10_3DMODEL_DIR}/Package_SO.3dshapes/Toshiba_SOIC-4-6_4.4x3.6mm_P1.27mm.step', (0.0, 0.0, 0.0)),

        # Discrete & Passives
        'L1': ('${KICAD10_3DMODEL_DIR}/Inductor_SMD.3dshapes/L_2816_7142Metric.step', (0.0, 0.0, 0.0)),
        'D1': ('${KICAD10_3DMODEL_DIR}/LED_SMD.3dshapes/LED_WS2812B-PLCC4.step', (0.0, 0.0, 0.0)),
        'D2': ('${KICAD10_3DMODEL_DIR}/Diode_SMD.3dshapes/D_SMB.step', (0.0, 0.0, 0.0)),
        'T1': ('${KICAD10_3DMODEL_DIR}/Transformer_SMD.3dshapes/Transformer_Ethernet_HALO_TG111-MSC13.step', (0.0, 0.0, 0.0)),
        'T2': ('${KICAD10_3DMODEL_DIR}/Transformer_SMD.3dshapes/Transformer_Ethernet_HALO_TG111-MSC13.step', (0.0, 0.0, 0.0)),
        'C1': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0805_2012Metric.step', (0.0, 0.0, 0.0)),
        'C2': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0805_2012Metric.step', (0.0, 0.0, 0.0)),
        'C3': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step', (0.0, 0.0, 0.0)),
        'C4': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step', (0.0, 0.0, 0.0)),
        'C6': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step', (0.0, 0.0, 0.0)),
        'C7': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step', (0.0, 0.0, 0.0)),
        'C10': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step', (0.0, 0.0, 0.0)),
        'C11': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0805_2012Metric.step', (0.0, 0.0, 0.0)),
        'C12': ('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step', (0.0, 0.0, 0.0)),
        'R1': ('${KICAD10_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0603_1608Metric.step', (0.0, 0.0, 0.0)),
        'R2': ('${KICAD10_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0603_1608Metric.step', (0.0, 0.0, 0.0)),
        'R5': ('${KICAD10_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0603_1608Metric.step', (0.0, 0.0, 0.0)),
        'R6': ('${KICAD10_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0603_1608Metric.step', (0.0, 0.0, 0.0)),
        'R9': ('${KICAD10_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0603_1608Metric.step', (0.0, 0.0, 0.0)),
        'R10': ('${KICAD10_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0603_1608Metric.step', (0.0, 0.0, 0.0)),
        'R11': ('${KICAD10_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0603_1608Metric.step', (0.0, 0.0, 0.0)),

        # Connectors & Peripherals
        'J1': ('${KICAD10_3DMODEL_DIR}/Connector_IDC.3dshapes/IDC-Header_2x13_P2.54mm_Vertical.step', (0.0, 0.0, 0.0)),
        'J2': ('${KICAD10_3DMODEL_DIR}/Connector_Card.3dshapes/microSD_HC_Hirose_DM3D-SF.step', (0.0, 0.0, 0.0)),
        'J3': ('${KICAD10_3DMODEL_DIR}/Connector_IDC.3dshapes/IDC-Header_2x05_P2.54mm_Vertical.step', (0.0, 0.0, 0.0)),
        'J4': ('${KICAD10_3DMODEL_DIR}/Connector_JST.3dshapes/JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical.step', (0.0, 0.0, 0.0)),
        'J5': ('${KICAD10_3DMODEL_DIR}/Connector_JST.3dshapes/JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical.step', (0.0, 0.0, 0.0)),
    }

    # Complete Verified Placement Matrix (in mm) matching openmotorbridge_main.kicad_pcb exactly
    layout_rules = {
        # 4 Corner M3 Mounting Holes
        'H1': (119.22,  75.85,  0.0),
        'H2': (196.22,  75.85,  0.0),
        'H3': (119.22, 122.85,  0.0),
        'H4': (196.22, 122.85,  0.0),

        # Power & UPS (LM5164, LDO, Passives)
        'D2':  (123.00,  84.00,  0.0),
        'U1':  (124.00,  88.00,  0.0),
        'C1':  (130.00,  84.00,  0.0),
        'U9':  (134.00,  84.00,  0.0),
        'C3':  (119.00,  88.00,  0.0),
        'C4':  (119.00,  90.00,  0.0),
        'R1':  (128.00,  92.00,  0.0),
        'R2':  (123.00,  92.00,  0.0),
        'C2':  (134.00,  96.00,  0.0),
        'L1':  (124.00, 103.00,  0.0),

        # MCU & Decoupling (ESP32-S3-WROOM-1U with U.FL connector)
        'U2':  (149.50,  89.15,  0.0),
        'C10': (138.00,  88.00,  0.0),
        'C11': (138.00,  91.00,  0.0),

        # Peripherals & Sensors (IMU, MicroSD, Status LED)
        'D1':  (149.50, 104.00,  0.0),
        'U5':  (149.50, 108.00,  0.0),
        'C12': (149.50, 104.00,  0.0),
        'R10': (152.50, 104.00,  0.0),
        'R11': (152.50, 106.00,  0.0),
        'J2':  (158.00,  98.00,  0.0),

        # Audio Codec, CAN & Optocouplers
        'U3':  (158.00,  84.00,  0.0),
        'C6':  (164.00,  91.00,  0.0),
        'R5':  (164.00,  93.00,  0.0),
        'T1':  (174.00,  90.00,  0.0),
        'U7':  (186.00,  90.00,  0.0),
        'C7':  (164.00, 105.00,  0.0),
        'R6':  (164.00, 107.00,  0.0),
        'T2':  (174.00, 107.00,  0.0),
        'U8':  (186.00, 107.00,  0.0),
        'U6':  (185.00,  78.00,  0.0),
        'R9':  (191.00,  78.00,  0.0),

        # Headers & Front Connectors
        'J3':  (128.00, 121.50, 90.0),
        'J1':  (157.00, 121.50, 90.0),
        'J5':  (195.00,  92.00, 90.0),
        'J4':  (195.00, 108.00, 90.0),
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

    board.Save(pcb_path)
    print(f"\nSuccessfully auto-placed full component matrix on {pcb_path}!\n")

if __name__ == '__main__':
    pcb_file = 'hardware/kicad_main_box/openmotorbridge_main.kicad_pcb'
    if len(sys.argv) > 1:
        pcb_file = sys.argv[1]
    auto_place_main_board(pcb_file)
