#!/usr/bin/env python3
"""
tools/setup_pcba05_preconnect.py
================================
Assigns nets to U9 (DW3110) and ANT_UWB on PCBA 05 (Universal Front Node):
- U9 (DW3110) SPI, IRQ, RST, RF, Power
- ANT_UWB (Taoglas FXUWB10) RF, GND
- Synchronizes openmotorbridge_front_node.kicad_sch
"""

import os
import sys
import pcbnew

PCB_PATH = "hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb"
SCH_PATH = "hardware/kicad_front_node/openmotorbridge_front_node.kicad_sch"

def main():
    board = pcbnew.LoadBoard(PCB_PATH)

    # 1. Ensure required nets exist
    required_nets = [
        "UWB_SCK", "UWB_MOSI", "UWB_MISO", "UWB_CS", "UWB_IRQ", "UWB_RST", "UWB_RF",
        "VCC_3V3", "GND"
    ]
    net_map = {}
    for n in required_nets:
        net = board.FindNet(n)
        if not net:
            net = pcbnew.NETINFO_ITEM(board, n)
            board.Add(net)
        net_map[n] = board.FindNet(n)

    # 2. Assign nets to U9 (DW3110)
    u9 = board.FindFootprintByReference("U9")
    if u9:
        u9_map = {
            "7": net_map["UWB_SCK"],
            "8": net_map["UWB_MISO"],
            "9": net_map["UWB_MOSI"],
            "10": net_map["UWB_CS"],
            "12": net_map["UWB_RST"],
            "13": net_map["UWB_IRQ"],
            "14": net_map["VCC_3V3"],
            "15": net_map["UWB_RF"],
            "16": net_map["GND"],
            "17": net_map["GND"]
        }
        for p in u9.Pads():
            num = p.GetNumber()
            if num in u9_map:
                p.SetNet(u9_map[num])
            else:
                p.SetNet(net_map["GND"])
        print("✓ Assigned nets to U9 (DW3110).")

    # 3. Assign nets to ANT_UWB
    ant = board.FindFootprintByReference("ANT_UWB")
    if ant:
        for p in ant.Pads():
            if p.GetNumber() == "1":
                p.SetNet(net_map["UWB_RF"])
            else:
                p.SetNet(net_map["GND"])
        print("✓ Assigned nets to ANT_UWB.")

    # 4. Refill zones and save
    for zone in board.Zones():
        zone.SetNeedRefill(True)
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())

    board.Save(PCB_PATH)
    print(f"✓ Saved updated {PCB_PATH}")

    # 5. Update schematic with UWB global labels
    with open(SCH_PATH, "r", encoding="utf-8") as f:
        c = f.read()

    if "UWB_SCK" not in c:
        labels = """
\t(global_label "UWB_SCK" (shape output) (at 210.0 115.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "UWB_MOSI" (shape output) (at 210.0 120.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "UWB_MISO" (shape input) (at 210.0 125.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "UWB_CS" (shape output) (at 210.0 130.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "UWB_IRQ" (shape input) (at 210.0 135.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "UWB_RST" (shape output) (at 210.0 140.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "UWB_RF" (shape passive) (at 210.0 145.0 0) (effects (font (size 1.27 1.27)) (justify left)))
)
"""
        c = c.rstrip()
        if c.endswith(")"):
            c = c[:-1] + labels
        with open(SCH_PATH, "w", encoding="utf-8") as f:
            f.write(c)
        print(f"✓ Added UWB global labels to {SCH_PATH}")

    os._exit(0)

if __name__ == "__main__":
    main()
