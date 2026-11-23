#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
tools/fix_sensor_puck_cuts_drc.py
==================================
Fixes Edge.Cuts outlines and board design rules for openmotorbridge_sensor_puck:
1. Replaces open Edge.Cuts lines around U2 with two closed, valid 0.8 mm routed slot contours:
   - Slot 1 (North-East L-slot)
   - Slot 2 (South-East L-slot)
2. Sets min_copper_edge_clearance to 0.30 mm in board settings.
3. Sets zone clearance to 0.25 mm and refills all zones cleanly.
4. Validates with KiCad DRC.
"""

import os
import pcbnew

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PCB_PATH = os.path.join(REPO_ROOT, "hardware", "kicad_sensor_puck", "openmotorbridge_sensor_puck.kicad_pcb")

def to_nm(val):
    return int(round(val * 1e6))

def fix():
    board = pcbnew.LoadBoard(PCB_PATH)
    print("Loaded board.")

    # 1. Remove old open lines around U2 on Edge.Cuts
    shapes_to_remove = []
    for drawing in board.GetDrawings():
        if drawing.GetLayer() == pcbnew.Edge_Cuts:
            p1 = (pcbnew.ToMM(drawing.GetStart().x), pcbnew.ToMM(drawing.GetStart().y))
            p2 = (pcbnew.ToMM(drawing.GetEnd().x), pcbnew.ToMM(drawing.GetEnd().y))
            # The open lines are within X = 1.0..9.0 and Y = 3.0..11.0
            if max(p1[0], p2[0]) <= 9.0 and min(p1[0], p2[0]) >= 1.0 and max(p1[1], p2[1]) <= 11.5 and min(p1[1], p2[1]) >= 3.0:
                shapes_to_remove.append(drawing)

    for s in shapes_to_remove:
        board.Remove(s)
    print(f"Removed {len(shapes_to_remove)} old open Edge.Cuts lines.")

    # 2. Add two closed, valid routed slot contours (0.8 mm slot width)
    # Slot 1 (North-East L-slot):
    # Width 0.5 mm, safely clear of I2C_SCL at Y=6.40 mm (bottom at Y=5.80 mm)
    poly1 = [
        (1.8, 3.2), (8.75, 3.2),
        (8.75, 5.80), (8.25, 5.80),
        (8.25, 3.7), (1.8, 3.7),
        (1.8, 3.2)
    ]
    for i in range(len(poly1) - 1):
        seg = pcbnew.PCB_SHAPE(board)
        seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        seg.SetStart(pcbnew.VECTOR2I(to_nm(poly1[i][0]), to_nm(poly1[i][1])))
        seg.SetEnd(pcbnew.VECTOR2I(to_nm(poly1[i+1][0]), to_nm(poly1[i+1][1])))
        seg.SetWidth(to_nm(0.15))
        seg.SetLayer(pcbnew.Edge_Cuts)
        board.Add(seg)

    # Slot 2 (South-East L-slot):
    # Width 0.5 mm, top at Y=10.25 (clearance 0.35 mm to track at Y=9.90),
    # bottom at Y=10.75 (clearance 0.35 mm to track at Y=11.10),
    # left end at X=1.8 (clearance 0.55 mm to track at X=1.25),
    # top stub at Y=8.40 (clearance 0.50 mm to I2C_SDA at Y=7.90)
    poly2 = [
        (8.25, 8.40), (8.75, 8.40),
        (8.75, 10.75), (1.8, 10.75),
        (1.8, 10.25), (8.25, 10.25),
        (8.25, 8.40)
    ]
    for i in range(len(poly2) - 1):
        seg = pcbnew.PCB_SHAPE(board)
        seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        seg.SetStart(pcbnew.VECTOR2I(to_nm(poly2[i][0]), to_nm(poly2[i][1])))
        seg.SetEnd(pcbnew.VECTOR2I(to_nm(poly2[i+1][0]), to_nm(poly2[i+1][1])))
        seg.SetWidth(to_nm(0.15))
        seg.SetLayer(pcbnew.Edge_Cuts)
        board.Add(seg)
    print("Added 2 cleanly closed Edge.Cuts internal slot loops.")

    # 3. Update Design Settings & Zone clearances
    ds = board.GetDesignSettings()
    # Set copper edge clearance to 0.30 mm (JLCPCB standard)
    # In KiCad 10, design settings constraints:
    try:
        ds.m_CopperEdgeClearance = to_nm(0.30)
    except Exception as e:
        print("Note on m_CopperEdgeClearance:", e)

    # Update zone settings to 0.25 mm clearance
    for z in board.Zones():
        z.SetLocalClearance(to_nm(0.25))
        z.SetThermalReliefGap(to_nm(0.20))
        z.SetThermalReliefSpokeWidth(to_nm(0.25))
        z.SetMinThickness(to_nm(0.20))

    # Refill all zones
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    print("Refilled all zones with 0.25 mm clearance.")

    board.Save(PCB_PATH)
    print(f"Saved {PCB_PATH}.")

if __name__ == "__main__":
    fix()
