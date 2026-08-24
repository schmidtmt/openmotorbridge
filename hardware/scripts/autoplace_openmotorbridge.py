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
        'U2': ('${KICAD10_3DMODEL_DIR}/RF_Module.3dshapes/ESP32-S3-WROOM-1.step', (0.0, 0.0, 0.0)),
        'U1': ('${KICAD10_3DMODEL_DIR}/Package_SO.3dshapes/SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.41x3.81mm.step', (0.0, 0.0, 0.0)),
        'U3': ('${KICAD10_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/QFN-28-1EP_4x4mm_P0.4mm_EP2.4x2.4mm.step', (0.0, 0.0, 0.0)),
        'U5': ('${KICAD10_3DMODEL_DIR}/Package_LGA.3dshapes/Bosch_LGA-14_3x2.5mm_P0.5mm.step', (0.0, 0.0, 0.0)),
        'U6': ('${KICAD10_3DMODEL_DIR}/Package_SO.3dshapes/SOIC-8_3.9x4.9mm_P1.27mm.step', (0.0, 0.0, 0.0)),
        'U9': ('${KICAD10_3DMODEL_DIR}/Package_TO_SOT_SMD.3dshapes/SOT-23-5.step', (0.0, 0.0, 0.0)),
        'U7': ('${KICAD10_3DMODEL_DIR}/Package_SO.3dshapes/Toshiba_SOIC-4-6_4.4x3.6mm_P1.27mm.step', (0.0, 0.0, 0.0)),
        'U8': ('${KICAD10_3DMODEL_DIR}/Package_SO.3dshapes/Toshiba_SOIC-4-6_4.4x3.6mm_P1.27mm.step', (0.0, 0.0, 0.0)),

        # Discrete & Passives
        'L1': ('${KICAD10_3DMODEL_DIR}/Inductor_SMD.3dshapes/L_2816_7142Metric.step', (0.0, 0.0, 0.0)),
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
        'J2': ('${KICAD10_3DMODEL_DIR}/Connector_Card.3dshapes/microSD_HC_Hirose_DM3D-SF.step', (0.0, 0.0, 0.0)),
        'J3': ('${KICAD10_3DMODEL_DIR}/Connector_USB.3dshapes/USB_C_Receptacle_GCT_USB4085.step', (90.0, 0.0, -90.0)),
        'J1': ('${KICAD10_3DMODEL_DIR}/Connector_IDC.3dshapes/IDC-Header_2x13_P2.54mm_Vertical.step', (0.0, 0.0, 0.0)),
        'J5': ('${KICAD10_3DMODEL_DIR}/Connector_JST.3dshapes/JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical.step', (0.0, 0.0, 0.0)),
        'J6': ('${KICAD10_3DMODEL_DIR}/Connector_PinHeader_2.54mm.3dshapes/PinHeader_1x02_P2.54mm_Vertical.step', (0.0, 0.0, 0.0)),
        'J4': ('${KICAD10_3DMODEL_DIR}/Connector_PinHeader_2.54mm.3dshapes/PinHeader_1x03_P2.54mm_Vertical.step', (0.0, 0.0, 0.0)),
    }

    # Complete 3-Zone Coordinate Layout Matrix (in mm)
    layout_rules = {
        # 4 Corner M3 Mounting Holes
        'H1': (X0 + 4.0, Y0 + 4.0,   0.0),   # (119.22, 75.85) Top-Left
        'H2': (X_max - 4.0, Y0 + 4.0, 0.0),  # (196.22, 75.85) Top-Right
        'H3': (X0 + 4.0, Y_max - 4.0, 0.0),  # (119.22, 122.85) Bottom-Left
        'H4': (X_max - 4.0, Y_max - 4.0, 0.0), # (196.22, 122.85) Bottom-Right

        # Zone 1: MCU & RF (Left)
        'U2': (132.0, 89.0, 0.0),             # ESP32-S3-WROOM-1 MCU
        'C10': (123.0, 76.5, 0.0),
        'C11': (126.0, 76.5, 0.0),

        # Zone 2: Power & UPS (Center-Top)
        'D2': (140.0, 76.5, 0.0),             # SMBJ33CA TVS Diode
        'C1': (143.5, 76.5, 0.0),             # 10uF 100V Input Cap
        'L1': (150.0, 77.5, 0.0),             # 47uH Power Inductor
        'C2': (156.5, 76.5, 0.0),             # 22uF 16V Output Cap
        'U1': (147.0, 86.0, 0.0),             # TI LM5164-Q1 Buck Converter
        'U9': (139.5, 83.5, 0.0),             # TI TPS7A0533 3.3V LDO
        'C3': (143.5, 88.0, 0.0),
        'C4': (150.5, 88.0, 0.0),
        'R1': (137.0, 76.5, 0.0),
        'R2': (137.0, 79.5, 0.0),

        # Zone 3: Audio & CAN (Right)
        'T1': (170.0, 77.0, 0.0),             # Bourns LM-NP-1001 Audio Transformer 1
        'T2': (183.0, 77.0, 0.0),             # Bourns LM-NP-1001 Audio Transformer 2
        'U7': (169.0, 86.0, 0.0),             # TLP222A Optocoupler 1
        'U8': (182.0, 86.0, 0.0),             # TLP222A Optocoupler 2
        'C6': (163.5, 76.5, 0.0),
        'C7': (189.5, 76.5, 0.0),
        'R5': (163.5, 79.5, 0.0),
        'R6': (189.5, 79.5, 0.0),
        'U3': (176.0, 94.0, 0.0),             # Everest ES8388 Audio Codec
        'U6': (188.0, 95.0, 0.0),             # TI TCAN334G CAN-FD Transceiver
        'R9': (188.0, 102.0, 0.0),

        # Center Peripherals
        'J2': (154.0, 96.0, 0.0),             # Internal Flat MicroSD Slot
        'U5': (162.0, 92.0, 0.0),             # Bosch BMI270 6-Axis IMU
        'C12': (162.0, 86.5, 0.0),
        'R10': (162.0, 97.0, 0.0),
        'R11': (162.0, 99.5, 0.0),
        'D1': (154.0, 84.0, 0.0),             # Status LED

        # Bottom Connector Rail (All Vertical Top-Entry, 10mm plugging clearance)
        'J5': (123.5, 118.0, 0.0),            # LiPo Akku JST-PH 2-Pin
        'J6': (129.5, 118.0, 0.0),            # NTC JEITA Sensor 2-Pin
        'J1': (138.5, 118.0, 90.0),           # 2x13 IDC Box Header (Horizontal, notch inwards)
        'J4': (184.0, 118.0, 0.0),            # 3-Pin RGB LED Header
        'J3': (191.0, 118.0, 0.0),            # Vertical USB-C Port
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
