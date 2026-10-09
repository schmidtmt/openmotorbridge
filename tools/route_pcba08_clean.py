#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
tools/route_pcba08_clean.py
===========================
Clean, deterministic planar routing for PCBA 08 (Radar 2.0 Sub-MCU & Wings):
- 50-ohm RF trace (orthogonal): (145.25, 98.35) -> (145.25, 96.50) -> (152.00, 96.50)
- Parallel 0.5mm-pitch bus on Right Wing (X=138.0..141.0):
    SCK, MISO, MOSI, CS, RST, IRQ, VCC_3V3
- Top bridge crossing (Y=68.0..71.0)
- Left wing breakout to U1 pads (10, 11, 12, 14, 15)
- RST breakout to U1 Pad 6 via east channel
"""

import os
import sys
import subprocess
import pcbnew

PCB_PATH = "hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb"
KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

def to_nm(mm):
    return int(round(mm * 1e6))

def add_track(board, net, layer, p1, p2, width_mm=0.18):
    t = pcbnew.PCB_TRACK(board)
    t.SetNet(net)
    t.SetLayer(layer)
    t.SetWidth(to_nm(width_mm))
    t.SetStart(pcbnew.VECTOR2I(to_nm(p1[0]), to_nm(p1[1])))
    t.SetEnd(pcbnew.VECTOR2I(to_nm(p2[0]), to_nm(p2[1])))
    board.Add(t)
    return t

def add_polyline(board, net, layer, points, width_mm=0.18):
    for i in range(len(points) - 1):
        add_track(board, net, layer, points[i], points[i+1], width_mm=width_mm)

def add_via(board, net, p, drill_mm=0.25, size_mm=0.50):
    v = pcbnew.PCB_VIA(board)
    v.SetNet(net)
    v.SetPosition(pcbnew.VECTOR2I(to_nm(p[0]), to_nm(p[1])))
    v.SetDrill(to_nm(drill_mm))
    v.SetWidth(to_nm(size_mm))
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    board.Add(v)
    return v

def main():
    board = pcbnew.LoadBoard(PCB_PATH)
    print("Executing clean routing on PCBA 08...")

    b_cu = pcbnew.B_Cu
    f_cu = pcbnew.F_Cu

    nets_managed = ["UWB_RF", "UWB_SCK", "UWB_MOSI", "UWB_MISO", "UWB_CS", "UWB_IRQ", "UWB_RST"]
    
    # 1. Clean existing/temporary tracks for managed nets
    to_remove = [t for t in board.GetTracks() if t.GetNetname() in nets_managed]
    for t in to_remove:
        board.Remove(t)
        
    # Also clean any dangling VCC_3V3 stubs near U3
    for t in list(board.GetTracks()):
        if t.GetNetname() == "VCC_3V3":
            s, e = t.GetStart(), t.GetEnd()
            sx, sy = s.x/1e6, s.y/1e6
            ex, ey = e.x/1e6, e.y/1e6
            if (143 <= sx <= 148 or 143 <= ex <= 148) and (93 <= sy <= 99 or 93 <= ey <= 99):
                board.Remove(t)
                
    print("✓ Cleaned old tracks.")

    net_rf   = board.FindNet("UWB_RF")
    net_sck  = board.FindNet("UWB_SCK")
    net_mosi = board.FindNet("UWB_MOSI")
    net_miso = board.FindNet("UWB_MISO")
    net_cs   = board.FindNet("UWB_CS")
    net_irq  = board.FindNet("UWB_IRQ")
    net_rst  = board.FindNet("UWB_RST")
    net_3v3  = board.FindNet("VCC_3V3")

    # 2. RF Trace: 50 ohm trace (0.35 mm width)
    # (145.25, 98.35) -> (145.25, 96.50) -> (152.00, 96.50)
    add_polyline(board, net_rf, b_cu, [
        (145.25, 98.35),
        (145.25, 96.50),
        (152.00, 96.50)
    ], width_mm=0.35)
    print("✓ Routed UWB_RF.")

    # 3. VCC_3V3 to U3.14 (144.75, 98.35)
    # Connect Pad 14 to existing VCC_3V3 at (147.20, 83.90) on B.Cu
    # Notice: at (147.20, 83.90) B.Cu has VCC_3V3 track going to (148.70, 82.40).
    # From U3.14 (144.75, 98.35):
    # Go north to (144.75, 96.80) -> west to (141.00, 96.80) -> north to (141.00, 84.00) -> (147.00, 84.00) -> (147.20, 83.90)
    add_polyline(board, net_3v3, b_cu, [
        (144.75, 98.35),
        (144.75, 96.80),
        (141.00, 96.80),
        (141.00, 84.00),
        (147.00, 84.00),
        (147.20, 83.90)
    ], width_mm=0.25)
    print("✓ Routed VCC_3V3 to U3.14.")

    # 4. IRQ: U1.15 (47.25, 98.50) -> U3.13 (144.25, 98.35)
    # Right wing: (144.25, 98.35) -> (144.25, 97.20) -> (140.50, 97.20) -> (140.50, 70.00)
    # Bridge: (140.50, 70.00) -> (45.60, 70.00)
    # Left wing: (45.60, 70.00) -> (45.60, 98.50) -> (47.25, 98.50)
    add_polyline(board, net_irq, b_cu, [
        (144.25, 98.35),
        (144.25, 97.20),
        (140.50, 97.20),
        (140.50, 70.00),
        (45.60, 70.00),
        (45.60, 98.50),
        (47.25, 98.50)
    ], width_mm=0.18)
    print("✓ Routed UWB_IRQ.")

    # 5. CS: U1.14 (47.25, 100.00) -> U3.10 (143.55, 100.05)
    # Right wing: (143.55, 100.05) -> (139.50, 100.05) -> (139.50, 69.50)
    # Bridge: (139.50, 69.50) -> (45.20, 69.50)
    # Left wing: (45.20, 69.50) -> (45.20, 100.00) -> (47.25, 100.00)
    add_polyline(board, net_cs, b_cu, [
        (143.55, 100.05),
        (139.50, 100.05),
        (139.50, 69.50),
        (45.20, 69.50),
        (45.20, 100.00),
        (47.25, 100.00)
    ], width_mm=0.18)
    print("✓ Routed UWB_CS.")

    # 6. MOSI: U1.11 (47.25, 104.50) -> U3.9 (143.55, 100.55)
    # Right wing: (143.55, 100.55) -> (139.00, 100.55) -> (139.00, 69.00)
    # Bridge: (139.00, 69.00) -> (44.80, 69.00)
    # Left wing: (44.80, 69.00) -> (44.80, 104.50) -> (47.25, 104.50)
    add_polyline(board, net_mosi, b_cu, [
        (143.55, 100.55),
        (139.00, 100.55),
        (139.00, 69.00),
        (44.80, 69.00),
        (44.80, 104.50),
        (47.25, 104.50)
    ], width_mm=0.18)
    print("✓ Routed UWB_MOSI.")

    # 7. MISO: U1.12 (47.25, 103.00) -> U3.8 (144.25, 101.25)
    # Right wing: (144.25, 101.25) -> (144.25, 102.50) -> (138.50, 102.50) -> (138.50, 68.50)
    # Bridge: (138.50, 68.50) -> (44.40, 68.50)
    # Left wing: (44.40, 68.50) -> (44.40, 103.00) -> (47.25, 103.00)
    add_polyline(board, net_miso, b_cu, [
        (144.25, 101.25),
        (144.25, 102.50),
        (138.50, 102.50),
        (138.50, 68.50),
        (44.40, 68.50),
        (44.40, 103.00),
        (47.25, 103.00)
    ], width_mm=0.18)
    print("✓ Routed UWB_MISO.")

    # 8. SCK: U1.10 (47.25, 106.00) -> U3.7 (144.75, 101.25)
    # Right wing: (144.75, 101.25) -> (144.75, 103.00) -> (138.00, 103.00) -> (138.00, 68.00)
    # Bridge: (138.00, 68.00) -> (44.00, 68.00)
    # Left wing: (44.00, 68.00) -> (44.00, 106.00) -> (47.25, 106.00)
    add_polyline(board, net_sck, b_cu, [
        (144.75, 101.25),
        (144.75, 103.00),
        (138.00, 103.00),
        (138.00, 68.00),
        (44.00, 68.00),
        (44.00, 106.00),
        (47.25, 106.00)
    ], width_mm=0.18)
    print("✓ Routed UWB_SCK.")

    # 9. RST: U1.6 (64.75, 101.50) -> U3.12 (143.55, 99.05)
    # Right wing: (143.55, 99.05) -> (140.00, 99.05) -> (140.00, 70.50)
    # Bridge: (140.00, 70.50) -> (66.60, 70.50)
    # Left wing breakout to Pad 6:
    # From (66.60, 70.50) down to (66.60, 74.50)
    # Via to F.Cu at (66.60, 74.50), down to (66.60, 79.50) on F.Cu (hopping over B.Cu VCC_5V at 77.0)
    # Via back to B.Cu at (66.60, 79.50)
    # Down B.Cu: (66.60, 79.50) -> (66.60, 101.50) -> (64.75, 101.50)
    add_polyline(board, net_rst, b_cu, [
        (143.55, 99.05),
        (140.00, 99.05),
        (140.00, 70.50),
        (66.60, 70.50),
        (66.60, 74.50)
    ], width_mm=0.18)
    add_via(board, net_rst, (66.60, 74.50))
    add_polyline(board, net_rst, f_cu, [
        (66.60, 74.50),
        (66.60, 79.50)
    ], width_mm=0.18)
    add_via(board, net_rst, (66.60, 79.50))
    add_polyline(board, net_rst, b_cu, [
        (66.60, 79.50),
        (66.60, 101.50),
        (64.75, 101.50)
    ], width_mm=0.18)
    print("✓ Routed UWB_RST.")

    # Refill zones
    for zone in board.Zones():
        zone.SetNeedRefill(True)
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    print("✓ Refilled all zones.")

    board.Save(PCB_PATH)
    print(f"✓ Saved updated {PCB_PATH}")

if __name__ == "__main__":
    main()
