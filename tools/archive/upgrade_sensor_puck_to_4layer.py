#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
tools/upgrade_sensor_puck_to_4layer.py
======================================
Sets the stackup of openmotorbridge_sensor_puck.kicad_pcb to 4 copper layers:
- Layer 1: F.Cu (Top Signal / Component pads)
- Layer 2: In1.Cu (GND_PLANE solid ground pour)
- Layer 3: In2.Cu (PWR_PLANE solid VCC_3V3 power pour)
- Layer 4: B.Cu (Bottom Signal / Ground pour)

Preserves 100% of the user's footprint placements, silkscreen, and outlines.
"""

import os
import sys
import pcbnew

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PCB_PATH = os.path.join(REPO_ROOT, "hardware", "kicad_sensor_puck", "openmotorbridge_sensor_puck.kicad_pcb")

def to_nm(val):
    return int(round(val * 1e6))

def upgrade():
    board = pcbnew.LoadBoard(PCB_PATH)
    print("Loaded board.")

    # 1. Set 4 copper layers
    board.SetCopperLayerCount(4)
    board.SetLayerName(pcbnew.In1_Cu, "GND_PLANE")
    board.SetLayerType(pcbnew.In1_Cu, pcbnew.LT_POWER)
    board.SetLayerName(pcbnew.In2_Cu, "PWR_PLANE")
    board.SetLayerType(pcbnew.In2_Cu, pcbnew.LT_POWER)

    net_gnd = board.FindNet("GND")
    net_vcc3v3 = board.FindNet("VCC_3V3")

    W, H = 34.0, 34.0

    # 2. Add internal zones if not already present
    has_in1 = False
    has_in2 = False
    for z in board.Zones():
        if z.GetLayer() == pcbnew.In1_Cu:
            has_in1 = True
        elif z.GetLayer() == pcbnew.In2_Cu:
            has_in2 = True

    if not has_in1 and net_gnd:
        zone = pcbnew.ZONE(board)
        zone.SetLayer(pcbnew.In1_Cu)
        zone.SetNet(net_gnd)
        zone.SetAssignedPriority(0)
        zone.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        zone.SetThermalReliefGap(to_nm(0.20))
        zone.SetThermalReliefSpokeWidth(to_nm(0.25))
        zone.SetMinThickness(to_nm(0.20))

        poly = zone.Outline()
        poly.NewOutline()
        poly.Append(to_nm(0.0), to_nm(0.0))
        poly.Append(to_nm(W), to_nm(0.0))
        poly.Append(to_nm(W), to_nm(H))
        poly.Append(to_nm(0.0), to_nm(H))
        board.Add(zone)
        print("✓ Added solid GND zone on In1.Cu (Layer 2)")

    if not has_in2 and net_vcc3v3:
        zone = pcbnew.ZONE(board)
        zone.SetLayer(pcbnew.In2_Cu)
        zone.SetNet(net_vcc3v3)
        zone.SetAssignedPriority(0)
        zone.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        zone.SetThermalReliefGap(to_nm(0.20))
        zone.SetThermalReliefSpokeWidth(to_nm(0.25))
        zone.SetMinThickness(to_nm(0.20))

        poly = zone.Outline()
        poly.NewOutline()
        poly.Append(to_nm(0.0), to_nm(0.0))
        poly.Append(to_nm(W), to_nm(0.0))
        poly.Append(to_nm(W), to_nm(H))
        poly.Append(to_nm(0.0), to_nm(H))
        board.Add(zone)
        print("✓ Added solid VCC_3V3 zone on In2.Cu (Layer 3)")

    # 3. Fill zones
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())

    board.Save(PCB_PATH)
    print(f"✅ Board {PCB_PATH} successfully updated to 4-layer stackup!")

if __name__ == "__main__":
    upgrade()
