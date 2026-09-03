#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
OpenMotorBridge - Rear Pod 3 PCB Geometry & Component Pre-Placement Updater
===========================================================================
1. Resizes board outline (Edge.Cuts) to 55.0 x 48.0 mm (X: 100.0..155.0, Y: 72.0..120.0, R=2.5mm)
2. Removes deleted components (ANT1, ANT2, ANT3, J3)
3. Updates U1 footprint to ESP32-C3-WROOM-02U
4. Updates J4 and J5 footprints to U.FL (U.FL_Hirose_U.FL-R-SMT-1_Vertical)
5. Positions 4x M2 mounting holes (H1..H4) to match base sled standoffs:
   H1: (103.0, 86.5)
   H2: (103.0, 105.5)
   H3: (149.0, 86.5)
   H4: (149.0, 105.5)
6. Pre-places components in functional zones with clean routing clearances
"""

import sys
import os
import pcbnew

PCB_PATH = "/Users/schmidtm/openMotorBridge/hardware/kicad_rear_pod3/openmotorbridge_rear_pod3.kicad_pcb"
FP_LIB_COAX = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/Connector_Coaxial.pretty"
FP_LIB_RF   = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/RF_Module.pretty"

def to_nm(mm):
    return int(mm * 1e6)

def update_rear_pod3():
    print(f"Loading PCB: {PCB_PATH}")
    board = pcbnew.LoadBoard(PCB_PATH)

    # -------------------------------------------------------------------------
    # 1. REMOVE OLD EDGE.CUTS & REDRAW 55x48 mm OUTLINE (R = 2.5 mm)
    # -------------------------------------------------------------------------
    drawings_to_remove = []
    for d in board.GetDrawings():
        if d.GetLayer() == pcbnew.Edge_Cuts:
            drawings_to_remove.append(d)
    for d in drawings_to_remove:
        board.Remove(d)

    # Coordinates:
    # X0 = 100.0, X1 = 155.0 (Length 55.0 mm)
    # Y0 = 72.0,  Y1 = 120.0 (Width 48.0 mm, Centered at Y = 96.0 mm)
    # R = 2.5 mm
    X0, X1 = 100.0, 155.0
    Y0, Y1 = 72.0, 120.0
    R = 2.5

    def add_line(x1, y1, x2, y2):
        seg = pcbnew.PCB_SHAPE(board)
        seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        seg.SetLayer(pcbnew.Edge_Cuts)
        seg.SetWidth(to_nm(0.15))
        seg.SetStart(pcbnew.VECTOR2I(to_nm(x1), to_nm(y1)))
        seg.SetEnd(pcbnew.VECTOR2I(to_nm(x2), to_nm(y2)))
        board.Add(seg)

    def add_arc(x_start, y_start, x_mid, y_mid, x_end, y_end):
        arc = pcbnew.PCB_SHAPE(board)
        arc.SetShape(pcbnew.SHAPE_T_ARC)
        arc.SetLayer(pcbnew.Edge_Cuts)
        arc.SetWidth(to_nm(0.15))
        arc.SetStart(pcbnew.VECTOR2I(to_nm(x_start), to_nm(y_start)))
        arc.SetArcGeometry(
            pcbnew.VECTOR2I(to_nm(x_start), to_nm(y_start)),
            pcbnew.VECTOR2I(to_nm(x_mid), to_nm(y_mid)),
            pcbnew.VECTOR2I(to_nm(x_end), to_nm(y_end))
        )
        board.Add(arc)

    # 4 straight segments
    add_line(X0 + R, Y0, X1 - R, Y0)          # Top
    add_line(X1, Y0 + R, X1, Y1 - R)          # Right
    add_line(X1 - R, Y1, X0 + R, Y1)          # Bottom
    add_line(X0, Y1 - R, X0, Y0 + R)          # Left

    # 4 rounded corners (R = 2.5 mm)
    # Top-Right
    add_arc(X1 - R, Y0, X1 - R + R*0.7071, Y0 + R - R*0.7071, X1, Y0 + R)
    # Bottom-Right
    add_arc(X1, Y1 - R, X1 - R + R*0.7071, Y1 - R + R*0.7071, X1 - R, Y1)
    # Bottom-Left
    add_arc(X0 + R, Y1, X0 + R - R*0.7071, Y1 - R + R*0.7071, X0, Y1 - R)
    # Top-Left
    add_arc(X0, Y0 + R, X0 + R - R*0.7071, Y0 + R - R*0.7071, X0 + R, Y0)

    print("  ✓ Updated Edge.Cuts to 55.0 x 48.0 mm (R = 2.5 mm)")

    # -------------------------------------------------------------------------
    # 2. REMOVE DELETED COMPONENTS (ANT1, ANT2, ANT3, J3)
    # -------------------------------------------------------------------------
    to_delete = ["ANT1", "ANT2", "ANT3", "J3"]
    fps_to_remove = [fp for fp in board.Footprints() if fp.GetReference() in to_delete]
    for fp in fps_to_remove:
        board.Remove(fp)
        print(f"  ✓ Removed obsolete component: {fp.GetReference()}")

    # -------------------------------------------------------------------------
    # 3. UPDATE FOOTPRINTS FOR J4, J5 (U.FL) & U1 (ESP32-C3-WROOM-02U)
    # -------------------------------------------------------------------------
    # Load U.FL footprint from KiCad library
    ufl_fp_name = "U.FL_Hirose_U.FL-R-SMT-1_Vertical"
    ufl_fp_sample = pcbnew.FootprintLoad(FP_LIB_COAX, ufl_fp_name)
    
    c3u_fp_name = "ESP32-C3-WROOM-02U"
    c3u_fp_sample = pcbnew.FootprintLoad(FP_LIB_RF, c3u_fp_name)

    # Replace J4 and J5 footprints if needed
    for fp in list(board.Footprints()):
        ref = fp.GetReference()
        if ref in ["J4", "J5"] and ufl_fp_sample:
            # Transfer nets and replace with U.FL
            pos = fp.GetPosition()
            new_fp = pcbnew.FOOTPRINT(board)
            new_fp = pcbnew.FootprintLoad(FP_LIB_COAX, ufl_fp_name)
            new_fp.SetReference(ref)
            new_fp.SetValue("U.FL_LORA" if ref == "J4" else "U.FL_GNSS")
            # Map pad nets
            for p_old in fp.Pads():
                for p_new in new_fp.Pads():
                    if p_new.GetNumber() == p_old.GetNumber():
                        p_new.SetNet(p_old.GetNet())
            board.Remove(fp)
            board.Add(new_fp)
            print(f"  ✓ Replaced {ref} with U.FL footprint")

        elif ref == "U1" and c3u_fp_sample:
            new_fp = pcbnew.FootprintLoad(FP_LIB_RF, c3u_fp_name)
            new_fp.SetReference("U1")
            new_fp.SetValue("ESP32-C3-WROOM-02U")
            for p_old in fp.Pads():
                for p_new in new_fp.Pads():
                    if p_new.GetNumber() == p_old.GetNumber():
                        p_new.SetNet(p_old.GetNet())
            board.Remove(fp)
            board.Add(new_fp)
            print(f"  ✓ Replaced U1 with ESP32-C3-WROOM-02U footprint")

    # -------------------------------------------------------------------------
    # 4. PRE-PLACEMENT RULES (OPTIMAL ZONING ON 55 x 48 mm BOARD)
    # -------------------------------------------------------------------------
    # X0 = 100.0, X_mid = 127.5, X1 = 155.0
    # Y0 = 72.0,  Y_mid = 96.0,  Y1 = 120.0
    placement_rules = {
        # 4x M2 Mounting Holes (Matching base sled floor standoffs)
        "H1": (103.0, 86.5, 0.0),
        "H2": (103.0, 105.5, 0.0),
        "H3": (149.0, 86.5, 0.0),
        "H4": (149.0, 105.5, 0.0),

        # J1: 6-Pin Socket (Centered at Y = 96.0 mm, mating through front edge)
        "J1": (102.5, 89.65, 0.0),

        # Power & Identification Zone (near J1)
        "F1": (108.5, 80.0, 90.0),       # PTC 500mA
        "C1": (113.0, 80.0, 90.0),       # 10uF bulk capacitor
        "U4": (109.0, 96.0, 0.0),        # DS2401 1-Wire ID (SOT-23)
        "D1": (108.5, 112.0, 180.0),     # 5V Green LED
        "R1": (112.5, 112.0, 90.0),      # LED Resistor 1.5k

        # Top Zone: GNSS Subsystem (Y = 74 .. 82 mm)
        "U2": (122.0, 78.5, 180.0),      # MAX-M10S GNSS QFN-24
        "C3": (117.0, 78.5, 90.0),       # 100nF GNSS
        "J5": (132.5, 78.5, 0.0),        # U.FL GNSS RF Connector

        # Bottom Zone: LoRa Subsystem (Y = 110 .. 118 mm)
        "U3": (122.0, 113.5, 0.0),       # Semtech SX1262 LoRa QFN-24
        "C4": (117.0, 113.5, 90.0),      # 100nF LoRa
        "J4": (132.5, 113.5, 180.0),     # U.FL LoRa RF Connector

        # Center Zone: ESP32-C3-WROOM-02U Wireless MCU (Y = 89 .. 103 mm)
        "U1": (138.0, 96.0, 0.0),        # ESP32-C3 with U.FL facing rear (+X)
        "C2": (124.0, 90.0, 90.0),       # 100nF MCU
    }

    fps_dict = {fp.GetReference(): fp for fp in board.Footprints()}

    for ref, (x_mm, y_mm, rot_deg) in placement_rules.items():
        if ref in fps_dict:
            fp = fps_dict[ref]
            fp.SetPosition(pcbnew.VECTOR2I(to_nm(x_mm), to_nm(y_mm)))
            fp.SetOrientationDegrees(rot_deg)
            print(f"  ✓ Placed {ref:4s} at ({x_mm:6.2f}, {y_mm:6.2f}) mm, rot={rot_deg:5.1f}°")
        else:
            print(f"  ⚠️ Reference {ref} not found on board")

    # -------------------------------------------------------------------------
    # 5. CLEAN SILKSCREEN LABELS
    # -------------------------------------------------------------------------
    texts_to_remove = []
    for d in board.GetDrawings():
        if isinstance(d, pcbnew.PCB_TEXT) and d.GetLayer() == pcbnew.F_SilkS:
            texts_to_remove.append(d)
    for d in texts_to_remove:
        board.Remove(d)

    silks = [
        ("OMM TRANSCEIVER v8.1", 130.0, 74.0, 0.6, 0.6, 0.12),
        ("GNSS", 122.0, 74.0, 0.5, 0.5, 0.1),
        ("LoRa 868", 122.0, 118.0, 0.5, 0.5, 0.1),
        ("U.FL GNSS", 134.0, 74.0, 0.45, 0.45, 0.09),
        ("U.FL LoRa", 134.0, 118.0, 0.45, 0.45, 0.09),
        ("55x48mm", 150.0, 118.0, 0.45, 0.45, 0.09),
        ("J1", 101.0, 89.65, 0.5, 0.5, 0.1),
    ]

    for text_str, x_mm, y_mm, sx, sy, th in silks:
        txt = pcbnew.PCB_TEXT(board)
        txt.SetText(text_str)
        txt.SetLayer(pcbnew.F_SilkS)
        txt.SetPosition(pcbnew.VECTOR2I(to_nm(x_mm), to_nm(y_mm)))
        txt.SetTextSize(pcbnew.VECTOR2I(to_nm(sx), to_nm(sy)))
        txt.SetTextThickness(to_nm(th))
        txt.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
        board.Add(txt)

    board.Save(PCB_PATH)
    print(f"\n🎉 Successfully updated and pre-placed Rear Pod 3 PCB ({PCB_PATH})!")

if __name__ == "__main__":
    update_rear_pod3()
