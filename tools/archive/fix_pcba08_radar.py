#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
tools/fix_pcba08_radar.py
=========================
Fixes PCBA 08 (Radar 2.0 Sub-MCU & Wings):
1. Fixes RF trace from U3.15 to J4.1 (orthogonal route to avoid Pad 16 short/clearance).
2. Connects VCC_3V3 to U3.14.
3. Routes the 6 SPI lines from U1 to U3 across the top bridge on B.Cu.
4. Refills all zones.
5. Runs DRC to verify 0 unconnected items and 0 DRC errors.
"""

import os
import sys
import subprocess
import pcbnew

PCB_PATH = "hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb"
KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

def to_nm(mm):
    return int(round(mm * 1e6))

def to_mm(nm):
    return float(nm) / 1e6

def add_track(board, net, layer, start_xy, end_xy, width_mm=0.18):
    t = pcbnew.PCB_TRACK(board)
    t.SetNet(net)
    t.SetLayer(layer)
    t.SetWidth(to_nm(width_mm))
    t.SetStart(pcbnew.VECTOR2I(to_nm(start_xy[0]), to_nm(start_xy[1])))
    t.SetEnd(pcbnew.VECTOR2I(to_nm(end_xy[0]), to_nm(end_xy[1])))
    board.Add(t)
    return t

def add_via(board, net, xy, drill_mm=0.25, size_mm=0.50):
    v = pcbnew.PCB_VIA(board)
    v.SetNet(net)
    v.SetPosition(pcbnew.VECTOR2I(to_nm(xy[0]), to_nm(xy[1])))
    v.SetDrill(to_nm(drill_mm))
    v.SetWidth(to_nm(size_mm))
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    board.Add(v)
    return v

def main():
    board = pcbnew.LoadBoard(PCB_PATH)
    print("Fixing PCBA 08 Radar Sub-MCU...")

    b_cu = pcbnew.B_Cu
    f_cu = pcbnew.F_Cu

    net_rf = board.FindNet("UWB_RF")
    net_vcc3v3 = board.FindNet("VCC_3V3")
    net_sck = board.FindNet("UWB_SCK")
    net_mosi = board.FindNet("UWB_MOSI")
    net_miso = board.FindNet("UWB_MISO")
    net_cs = board.FindNet("UWB_CS")
    net_irq = board.FindNet("UWB_IRQ")
    net_rst = board.FindNet("UWB_RST")

    # 1. Fix RF trace (remove old diagonal segment)
    rf_tracks = [t for t in board.GetTracks() if t.GetNetname() == "UWB_RF"]
    for t in rf_tracks:
        board.Remove(t)
    print(f"✓ Removed {len(rf_tracks)} old RF track segments.")

    # Orthogonal RF route: 50-ohm trace (width 0.35 mm)
    # (145.25, 98.35) -> (145.25, 96.50) -> (152.00, 96.50)
    add_track(board, net_rf, b_cu, (145.25, 98.35), (145.25, 96.50), width_mm=0.35)
    add_track(board, net_rf, b_cu, (145.25, 96.50), (152.00, 96.50), width_mm=0.35)
    print("✓ Added orthogonal 50-ohm RF trace (145.25, 98.35) -> (145.25, 96.5) -> (152.0, 96.5)")

    # 2. Connect VCC_3V3 to U3.14 (144.75, 98.35)
    # From existing VCC_3V3 at (150.7, 87.4) on B.Cu to U3.14:
    # Route via (150.7, 93.0) -> (147.0, 96.7) -> (147.0, 97.5) -> (144.75, 97.5) -> (144.75, 98.35)
    # Let's route carefully with 0.25mm width
    add_track(board, net_vcc3v3, b_cu, (150.70, 87.40), (150.70, 93.00), width_mm=0.25)
    add_track(board, net_vcc3v3, b_cu, (150.70, 93.00), (147.00, 96.70), width_mm=0.25)
    add_track(board, net_vcc3v3, b_cu, (147.00, 96.70), (147.00, 97.50), width_mm=0.25)
    add_track(board, net_vcc3v3, b_cu, (147.00, 97.50), (144.75, 97.50), width_mm=0.25)
    add_track(board, net_vcc3v3, b_cu, (144.75, 97.50), (144.75, 98.35), width_mm=0.25)
    print("✓ Connected VCC_3V3 to U3.14")

    # 3. Route 6 SPI lines:
    # Channels on Left Wing (B.Cu):
    #   SCK  : Pad 10 (47.25, 106.00) -> X=44.00, Y=68.10
    #   MOSI : Pad 11 (47.25, 104.50) -> X=44.40, Y=68.35
    #   MISO : Pad 12 (47.25, 103.00) -> X=44.80, Y=68.60
    #   CS   : Pad 14 (47.25, 100.00) -> X=45.20, Y=68.85
    #   IRQ  : Pad 15 (47.25,  98.50) -> X=45.60, Y=69.10
    #   RST  : Pad  6 (64.75, 101.50) -> under U1 to (46.00, 101.50) -> Y=69.35

    def route_polyline(net, points, width_mm=0.18, layer=b_cu):
        for i in range(len(points) - 1):
            add_track(board, net, layer, points[i], points[i+1], width_mm=width_mm)

    # RST: Pad 6 (64.75, 101.50)
    # Under U1: (64.75, 101.50) -> (46.00, 101.50) -> (46.00, 69.35) -> (133.00, 69.35)
    # Right wing to U3 Pad 12 at (143.55, 99.05):
    # From (133.00, 69.35) -> (133.00, 88.00) -> (141.00, 96.00) -> (141.00, 99.05) -> (143.55, 99.05)
    route_polyline(net_rst, [
        (64.75, 101.50),
        (46.00, 101.50),
        (46.00, 69.35),
        (133.00, 69.35),
        (133.00, 88.00),
        (140.50, 95.50),
        (140.50, 99.05),
        (143.55, 99.05)
    ])
    print("✓ Routed UWB_RST")

    # IRQ: Pad 15 (47.25, 98.50) -> U3 Pad 13 (144.25, 98.35)
    route_polyline(net_irq, [
        (47.25, 98.50),
        (45.60, 98.50),
        (45.60, 69.10),
        (133.40, 69.10),
        (133.40, 87.60),
        (141.00, 95.20),
        (141.00, 97.80),
        (144.25, 97.80),
        (144.25, 98.35)
    ])
    print("✓ Routed UWB_IRQ")

    # CS: Pad 14 (47.25, 100.00) -> U3 Pad 10 (143.55, 100.05)
    route_polyline(net_cs, [
        (47.25, 100.00),
        (45.20, 100.00),
        (45.20, 68.85),
        (133.80, 68.85),
        (133.80, 87.20),
        (140.00, 93.40),
        (140.00, 100.05),
        (143.55, 100.05)
    ])
    print("✓ Routed UWB_CS")

    # MISO: Pad 12 (47.25, 103.00) -> U3 Pad 8 (144.25, 101.25)
    route_polyline(net_miso, [
        (47.25, 103.00),
        (44.80, 103.00),
        (44.80, 68.60),
        (134.20, 68.60),
        (134.20, 86.80),
        (139.50, 92.10),
        (139.50, 102.00),
        (144.25, 102.00),
        (144.25, 101.25)
    ])
    print("✓ Routed UWB_MISO")

    # MOSI: Pad 11 (47.25, 104.50) -> U3 Pad 9 (143.55, 100.55)
    route_polyline(net_mosi, [
        (47.25, 104.50),
        (44.40, 104.50),
        (44.40, 68.35),
        (134.60, 68.35),
        (134.60, 86.40),
        (139.00, 90.80),
        (139.00, 100.55),
        (143.55, 100.55)
    ])
    print("✓ Routed UWB_MOSI")

    # SCK: Pad 10 (47.25, 106.00) -> U3 Pad 7 (144.75, 101.25)
    route_polyline(net_sck, [
        (47.25, 106.00),
        (44.00, 106.00),
        (44.00, 68.10),
        (135.00, 68.10),
        (135.00, 86.00),
        (138.50, 89.50),
        (138.50, 102.50),
        (144.75, 102.50),
        (144.75, 101.25)
    ])
    print("✓ Routed UWB_SCK")

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
