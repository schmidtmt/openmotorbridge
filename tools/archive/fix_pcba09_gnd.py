#!/usr/bin/env python3
"""
tools/fix_pcba09_gnd.py
=======================
Fixes the 7 unconnected GND items on PCBA 09:
- Connects J1 shield tabs and ground pins (A12, B12) to GND plane with vias.
- Connects U2 (BQ24075) ground pins (4, 5, 7, 14, 15) to GND plane with vias.
- Refills all zones and runs DRC to verify 0 unconnected items.
"""

import os
import subprocess
import pcbnew

PCB_PATH = "hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_pcb"
KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

def to_nm(mm):
    return int(mm * 1e6)

def to_mm(nm):
    return float(nm) / 1e6

def add_via(board, net, xy, drill_mm=0.30, size_mm=0.60):
    v = pcbnew.PCB_VIA(board)
    v.SetNet(net)
    v.SetPosition(pcbnew.VECTOR2I(to_nm(xy[0]), to_nm(xy[1])))
    v.SetDrill(to_nm(drill_mm))
    v.SetWidth(to_nm(size_mm))
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    board.Add(v)
    return v

def add_track(board, net, layer, start_xy, end_xy, width_mm=0.25):
    t = pcbnew.PCB_TRACK(board)
    t.SetNet(net)
    t.SetLayer(layer)
    t.SetWidth(to_nm(width_mm))
    t.SetStart(pcbnew.VECTOR2I(to_nm(start_xy[0]), to_nm(start_xy[1])))
    t.SetEnd(pcbnew.VECTOR2I(to_nm(end_xy[0]), to_nm(end_xy[1])))
    board.Add(t)
    return t

def fix_gnd():
    board = pcbnew.LoadBoard(PCB_PATH)
    f_cu = board.GetLayerID("F.Cu")
    b_cu = board.GetLayerID("B.Cu")
    gnd_net = board.FindNet("GND")

    # 1. J1 USB-C Ground & Shield
    j1 = board.FindFootprintByReference("J1")
    if j1:
        for p in j1.Pads():
            if p.GetNetname() == "GND":
                pos = (to_mm(p.GetPosition().x), to_mm(p.GetPosition().y))
                # Add via close to pad
                via_pos = (pos[0] + 0.8, pos[1])
                add_via(board, gnd_net, via_pos)
                add_track(board, gnd_net, f_cu, pos, via_pos)

    # 2. U2 BQ24075 Ground Pins (Pads 4, 5, 7, 14, 15, 17/EPAD)
    u2 = board.FindFootprintByReference("U2")
    if u2:
        for p in u2.Pads():
            if p.GetNetname() == "GND":
                pos = (to_mm(p.GetPosition().x), to_mm(p.GetPosition().y))
                # Connect to U2 thermal pad EPAD or add via
                via_pos = (pos[0], pos[1] + (0.8 if pos[1] > 95 else -0.8))
                add_via(board, gnd_net, via_pos)
                add_track(board, gnd_net, f_cu, pos, via_pos)

    # Refill all zones
    for zone in board.Zones():
        zone.SetNeedRefill(True)
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())

    board.Save(PCB_PATH)
    print("✓ Saved updated PCBA 09 PCB with ground connections.")

    # Run DRC
    json_out = "/tmp/pcba09_drc.json"
    subprocess.run([KICAD_CLI, "pcb", "drc", "--format", "json", "-o", json_out, PCB_PATH], capture_output=True)
    if os.path.exists(json_out):
        import json
        with open(json_out) as f:
            d = json.load(f)
        unconnected = len(d.get("unconnected_items", []))
        errors = [v for v in d.get("violations", []) if v.get("severity") == "error"]
        print(f"PCBA 09 DRC: Unconnected={unconnected} | Critical Errors={len(errors)}")

if __name__ == "__main__":
    fix_gnd()
