#!/usr/bin/env python3
"""
tools/setup_pcba01_clean_preconnect.py
======================================
Prepares PCBA 01 (Central Box Main Controller) for KiCad GUI Autorouting:
1. Restores clean board base if backup exists.
2. Updates U2 pad net assignments:
   - Pad 13: USB_D_N (GPIO 19)
   - Pad 14: USB_D_P (GPIO 20)
   - Pad 26: GND_PWR (GPIO 45 Strapping VDD_SPI -> Grounded/Safe)
   - Pad 28: RGB_LED_DATA (GPIO 35)
   - Pad 30: I2S_BCLK (GPIO 37)
   - Pad 31: UWB_IRQ (GPIO 38 - off strapping pin)
   - Pad 32: I2S_WS (GPIO 39)
3. Removes conflicting old trace stubs connected to these pads to eliminate DRC shorts.
4. Refills zones.
5. Exits cleanly with os._exit(0).
"""

import os
import sys
import shutil
import pcbnew

PCB_PATH = "hardware/kicad_main_box/openmotorbridge_main.kicad_pcb"
BAK_PATH = PCB_PATH + ".pre_fix_bak"

def main():
    if os.path.exists(BAK_PATH):
        shutil.copyfile(BAK_PATH, PCB_PATH)
        print(f"✓ Restored clean base from {BAK_PATH}")

    board = pcbnew.LoadBoard(PCB_PATH)
    u2 = board.FindFootprintByReference("U2")
    if not u2:
        print("❌ U2 not found!")
        os._exit(1)

    target_nets = {
        "13": "USB_D_N",
        "14": "USB_D_P",
        "26": "GND_PWR",
        "28": "RGB_LED_DATA",
        "30": "I2S_BCLK",
        "31": "UWB_IRQ",
        "32": "I2S_WS"
    }

    # Ensure nets exist
    net_map = {}
    for pin, net_name in target_nets.items():
        net = board.FindNet(net_name)
        if not net:
            net = pcbnew.NETINFO_ITEM(board, net_name)
            board.Add(net)
        net_map[net_name] = board.FindNet(net_name)

    # Collect pads to clean
    remediated_pad_nums = set(target_nets.keys())
    pads_to_clean = [p for p in u2.Pads() if p.GetNumber() in remediated_pad_nums]

    # Remove tracks touching these pads
    tracks_to_remove = []
    for p in pads_to_clean:
        p_box = p.GetBoundingBox()
        p_box.Inflate(int(0.3e6))
        for t in board.GetTracks():
            if p_box.Contains(t.GetStart()) or p_box.Contains(t.GetEnd()) or p_box.Intersects(t.GetBoundingBox()):
                if t not in tracks_to_remove:
                    tracks_to_remove.append(t)

    for t in tracks_to_remove:
        board.Remove(t)
    print(f"✓ Removed {len(tracks_to_remove)} conflicting track stubs at U2 pads.")

    # Assign target nets to U2 pads
    for p in pads_to_clean:
        num = p.GetNumber()
        p.SetNet(net_map[target_nets[num]])
    print("✓ Assigned target nets to U2 pads.")

    # Refill zones
    for zone in board.Zones():
        zone.SetNeedRefill(True)
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    print("✓ Refilled copper zones.")

    board.Save(PCB_PATH)
    print(f"✓ Saved updated {PCB_PATH}")
    os._exit(0)

if __name__ == "__main__":
    main()
