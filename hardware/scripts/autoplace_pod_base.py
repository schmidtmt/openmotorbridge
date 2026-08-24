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
        # J1: 6-Pin Horizontal Pin Header (Centered at Y=80.0mm, X=120.0mm)
        'J1': (
            '${KICAD10_3DMODEL_DIR}/Connector_PinHeader_2.54mm.3dshapes/PinHeader_1x06_P2.54mm_Horizontal.step',
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
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
    }

    # Symmetrical, spacious, non-overlapping layout (Variante A)
    # ref: (x_mm, y_mm, rot_deg, layer_name)
    layout_rules = {
        # Symmetrical M2 Mounting Holes on Left & Right Flanks (Through-Hole)
        'H1': (X0 + 3.0, Y_center, 0.0, 'F.Cu'),             # (103.0, 80.0) Left Mounting Hole
        'H2': (X0 + W - 3.0, Y_center, 0.0, 'F.Cu'),         # (133.0, 80.0) Right Mounting Hole

        # 6-Pin Horizontal Pin Header (OBERSEITE / INNEN: Horizontal in den Kassetteneinschub ragend)
        'J1': (X_center + 2.0, 73.65, 0.0, 'F.Cu'),          # (120.0, 73.65) Horizontal Pin Header (Y 73.65..86.35mm)

        # 6-Pad Wire Terminal for M8 Panel-Mount Pigtail Leads (Left Wing: Pure Flat Solder Pads)
        'J2': (X0 + 8.5, 75.0, 0.0, 'F.Cu'),                 # (108.5, 75.0) M8 Wire Connection Pads

        # Center Stage: SP3012 TVS Array & 100nF Cap
        'U1': (X_center - 4.5, Y_center - 3.5, 0.0, 'F.Cu'), # (113.5, 76.5) TVS Array (Top)
        'C1': (X_center - 4.5, Y_center + 3.5, 0.0, 'F.Cu'), # (113.5, 83.5) 100nF Cap (Top)
    }

    for ref, (x_mm, y_mm, rot_deg, layer_name) in layout_rules.items():
        fp = pcbnew.FOOTPRINT(board)
        fp.SetReference(ref)
        fp.Reference().SetVisible(False) # Clean professional look
        target_layer = pcbnew.B_Cu if layer_name == 'B.Cu' else pcbnew.F_Cu
        fp.SetLayer(target_layer)
        board.Add(fp)

        pos = pcbnew.VECTOR2I(int(x_mm * 1e6), int(y_mm * 1e6))
        fp.SetPosition(pos)
        fp.SetOrientationDegrees(rot_deg)

        # Add physical pads for J2 (6 Solder Pads) and H1/H2 (M2 screw holes)
        if ref == 'J2':
            for p_idx in range(6):
                pad = pcbnew.PAD(fp)
                pad.SetNumber(str(p_idx + 1))
                pad.SetShape(pcbnew.PAD_SHAPE_ROUNDRECT)
                pad.SetSize(pcbnew.VECTOR2I(int(1.8 * 1e6), int(1.2 * 1e6)))
                pad.SetDrillSize(pcbnew.VECTOR2I(int(0.85 * 1e6), int(0.85 * 1e6)))
                pad.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
                pad.SetLayerSet(pcbnew.LSET.AllCuMask())
                pad.SetPosition(pcbnew.VECTOR2I(int(x_mm * 1e6), int((y_mm + p_idx * 2.0) * 1e6)))
                fp.Add(pad)
        elif ref in ('H1', 'H2'):
            pad = pcbnew.PAD(fp)
            pad.SetNumber("1")
            pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
            pad.SetSize(pcbnew.VECTOR2I(int(3.5 * 1e6), int(3.5 * 1e6)))
            pad.SetDrillSize(pcbnew.VECTOR2I(int(2.2 * 1e6), int(2.2 * 1e6)))
            pad.SetAttribute(pcbnew.PAD_ATTRIB_NPTH)
            pad.SetLayerSet(pcbnew.LSET.AllCuMask())
            pad.SetPosition(pos)
            fp.Add(pad)

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

        print(f"  ✓ Placed {ref:4s} on {layer_name:4s} at ({x_mm:6.2f}, {y_mm:6.2f}) mm, rot={rot_deg:5.1f}°")

    # 3. Add Silkscreen Labels on Top (F.SilkS) and Bottom (B.SilkS)
    top_labels = [
        ("OPENMOTORBRIDGE // POD BASE", 123.0, Y0 + 2.0, 0.48, 0.48, 0.10),
        ("M8 WIRE IN (1..6)", 108.5, Y0 + 2.0, 0.36, 0.36, 0.08),
        ("SP3012 TVS", 114.0, 73.0, 0.30, 0.30, 0.07),
        ("MATES TO CARTRIDGE", 123.0, Y0 + H - 2.0, 0.36, 0.36, 0.08),
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
        ("OPENMOTORBRIDGE POD BASE (B.Cu)", X_center, Y_center, 0.50, 0.50, 0.11),
        ("GND SHIELD PLANE // 0 HOLES IN MATING ZONE", X_center, Y0 + H - 2.5, 0.40, 0.40, 0.09),
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
    print(f"✓ Saved Pod Stirnwand-Adapter PCB successfully: {pcb_path}")

if __name__ == '__main__':
    default_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../kicad_pod_base/openmotorbridge_pod_base.kicad_pcb'))
    generate_pod_base_pcb(default_path)

