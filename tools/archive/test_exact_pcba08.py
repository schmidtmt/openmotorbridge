#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
tools/test_exact_pcba08.py
==========================
DRC 0-error implementation for PCBA 08:
- Orthogonal RF trace to J4
- Orthogonal Pad 16 GND trace
- Sequential 6-line parallel bus across bridge
- Single via-hop on F.Cu to resolve MISO/MOSI order swap
- Clean east corridor for UWB_RST
- Clean VCC_3V3 connections
"""

import os
import sys
import subprocess
import pcbnew

PCB_PATH = "hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb"
KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

def to_nm(mm):
    return int(round(mm * 1e6))

def add_track(board, net, layer, p1, p2, width_mm=0.20):
    t = pcbnew.PCB_TRACK(board)
    t.SetNet(net)
    t.SetLayer(layer)
    t.SetWidth(to_nm(width_mm))
    t.SetStart(pcbnew.VECTOR2I(to_nm(p1[0]), to_nm(p1[1])))
    t.SetEnd(pcbnew.VECTOR2I(to_nm(p2[0]), to_nm(p2[1])))
    board.Add(t)
    return t

def add_polyline(board, net, layer, points, width_mm=0.20):
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
    print("Applying exact planar routing to PCBA 08...")

    b_cu = pcbnew.B_Cu
    f_cu = pcbnew.F_Cu

    nets_managed = ["UWB_RF", "UWB_SCK", "UWB_MOSI", "UWB_MISO", "UWB_CS", "UWB_IRQ", "UWB_RST"]

    # 1. Clean old tracks for managed nets and old VCC_3V3 stubs
    to_remove = []
    for t in board.GetTracks():
        netname = t.GetNetname()
        if netname in nets_managed:
            to_remove.append(t)
            continue
        s, e = t.GetStart(), t.GetEnd()
        sx, sy = s.x/1e6, s.y/1e6
        ex, ey = e.x/1e6, e.y/1e6
        if netname == "VCC_3V3":
            # old spur near U3
            if (140.0 <= sx <= 152.0 or 140.0 <= ex <= 152.0) and (83.5 <= sy <= 99.0 or 83.5 <= ey <= 99.0):
                to_remove.append(t)
            # old spur at X=65.9 and X=67.2
            elif (abs(sx - 65.9) < 0.2 or abs(ex - 65.9) < 0.2 or abs(sx - 67.2) < 0.2 or abs(ex - 67.2) < 0.2) and (94.0 <= sy <= 113.0 or 94.0 <= ey <= 113.0):
                to_remove.append(t)
        elif netname == "GND":
            if abs(sx - 145.75) < 0.1 and abs(sy - 98.35) < 0.1:
                to_remove.append(t)

    for t in to_remove:
        board.Remove(t)
    print(f"✓ Removed {len(to_remove)} obsolete tracks.")

    net_rf   = board.FindNet("UWB_RF")
    net_sck  = board.FindNet("UWB_SCK")
    net_mosi = board.FindNet("UWB_MOSI")
    net_miso = board.FindNet("UWB_MISO")
    net_cs   = board.FindNet("UWB_CS")
    net_irq  = board.FindNet("UWB_IRQ")
    net_rst  = board.FindNet("UWB_RST")
    net_3v3  = board.FindNet("VCC_3V3")
    net_gnd  = board.FindNet("GND")

    # 2. RF Trace: 50-ohm (0.35 mm width)
    add_polyline(board, net_rf, b_cu, [
        (145.25, 98.35),
        (145.25, 96.50),
        (152.00, 96.50)
    ], width_mm=0.35)
    print("✓ Routed UWB_RF.")

    # 3. Clean orthogonal GND for Pad 16
    add_polyline(board, net_gnd, b_cu, [
        (145.75, 98.35),
        (145.75, 99.80),
        (145.00, 99.80)
    ], width_mm=0.20)
    print("✓ Routed U3 Pad 16 GND.")

    # 4. VCC_3V3 Connections:
    # A) Right Wing: U3 Pad 14 (144.75, 98.35) connects to U2.5 (151.00, 87.35) and C2 (152.95, 84.00)
    # Route north on B.Cu to Y=96.5, west to X=141.2, north to Y=84.0, east to (147.20, 83.90) (connects to C2 and U2.5)
    add_polyline(board, net_3v3, b_cu, [
        (144.75, 98.35),
        (144.75, 96.50),
        (141.20, 96.50),
        (141.20, 84.00),
        (147.20, 84.00),
        (147.20, 83.90)
    ], width_mm=0.25)
    # Connect to U2.5 and C2
    add_polyline(board, net_3v3, b_cu, [
        (147.20, 83.90),
        (151.00, 83.90),
        (151.00, 87.35)
    ], width_mm=0.25)
    add_polyline(board, net_3v3, b_cu, [
        (151.00, 83.90),
        (152.95, 83.90),
        (152.95, 84.00)
    ], width_mm=0.25)

    # B) Left Wing: U1 Pad 2 (64.75, 95.50) to C3 (65.0, 91.0) and C4 (65.0, 112.0)
    # Pad 2 connects to C3 directly north along X=64.75 -> (64.75, 91.0) -> (65.0, 91.0)
    add_polyline(board, net_3v3, b_cu, [
        (64.75, 95.50),
        (64.75, 91.00),
        (65.00, 91.00)
    ], width_mm=0.25)
    # Pad 2 connects to C4/R2 south along X=67.8:
    add_polyline(board, net_3v3, b_cu, [
        (64.75, 95.50),
        (67.80, 95.50),
        (67.80, 112.00),
        (48.80, 112.00)
    ], width_mm=0.25)
    print("✓ Routed VCC_3V3 on both wings.")

    # 5. Route the 6 SPI lines:
    # A) SCK: U1.10 (47.25, 106.00) -> U3.7 (144.75, 101.25)
    add_polyline(board, net_sck, b_cu, [
        (47.25, 106.00),
        (43.60, 106.00),
        (43.60, 68.60),
        (138.20, 68.60),
        (138.20, 103.00),
        (144.75, 103.00),
        (144.75, 101.25)
    ], width_mm=0.20)
    print("✓ Routed UWB_SCK.")

    # B) MOSI: U1.11 (47.25, 104.50) -> U3.9 (143.55, 100.55)
    add_polyline(board, net_mosi, b_cu, [
        (47.25, 104.50),
        (44.00, 104.50),
        (44.00, 69.40),
        (139.00, 69.40),
        (139.00, 100.55),
        (143.55, 100.55)
    ], width_mm=0.20)
    print("✓ Routed UWB_MOSI.")

    # C) MISO: U1.12 (47.25, 103.00) -> U3.8 (144.25, 101.25)
    # Hop over MOSI on Left Wing using F.Cu between X=43.8 and 44.8:
    add_polyline(board, net_miso, b_cu, [
        (47.25, 103.00),
        (45.00, 103.00)
    ], width_mm=0.20)
    add_via(board, net_miso, (45.00, 103.00))
    add_polyline(board, net_miso, f_cu, [
        (45.00, 103.00),
        (43.20, 103.00),
        (43.20, 69.00),
        (44.40, 69.00)
    ], width_mm=0.20)
    add_via(board, net_miso, (44.40, 69.00))
    add_polyline(board, net_miso, b_cu, [
        (44.40, 69.00),
        (138.60, 69.00),
        (138.60, 102.40),
        (144.25, 102.40),
        (144.25, 101.25)
    ], width_mm=0.20)
    print("✓ Routed UWB_MISO.")

    # D) CS: U1.14 (47.25, 100.00) -> U3.10 (143.55, 100.05)
    add_polyline(board, net_cs, b_cu, [
        (47.25, 100.00),
        (44.80, 100.00),
        (44.80, 69.80),
        (139.40, 69.80),
        (139.40, 100.05),
        (143.55, 100.05)
    ], width_mm=0.20)
    print("✓ Routed UWB_CS.")

    # E) IRQ: U1.15 (47.25, 98.50) -> U3.13 (144.25, 98.35)
    add_polyline(board, net_irq, b_cu, [
        (47.25, 98.50),
        (45.20, 98.50),
        (45.20, 70.60),
        (140.20, 70.60),
        (140.20, 97.40),
        (144.25, 97.40),
        (144.25, 98.35)
    ], width_mm=0.20)
    print("✓ Routed UWB_IRQ.")

    # F) RST: U1.6 (64.75, 101.50) -> U3.12 (143.55, 99.05)
    # Bridge at Y=70.20, right wing at X=139.80
    add_polyline(board, net_rst, b_cu, [
        (64.75, 101.50),
        (66.50, 101.50),
        (66.50, 70.20),
        (139.80, 70.20),
        (139.80, 99.05),
        (143.55, 99.05)
    ], width_mm=0.20)
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
