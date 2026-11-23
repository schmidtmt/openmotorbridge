#!/usr/bin/env python3
"""
tools/route_pcba01_remediated_nets.py
=====================================
Cleans old conflicting tracks and cleanly routes the remediated signals on PCBA 01:
  - U2.13 (USB_D_N) -> J3.2
  - U2.14 (USB_D_P) -> J3.3
  - U2.26 (GND_PWR) -> GND Ground Plane
  - U2.28 (RGB_LED_DATA) -> D1.4
  - U2.30 (I2S_BCLK) -> U3.2 & U9.4
  - U2.31 (UWB_IRQ) -> U8.13
  - U2.32 (I2S_WS) -> U3.3 & U9.5
"""

import sys
import os
import math
import subprocess
import pcbnew

PCB_FILE = "hardware/kicad_main_box/openmotorbridge_main.kicad_pcb"
KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

def to_nm(mm):
    return int(mm * 1e6)

def to_mm(nm):
    return float(nm) / 1e6

def add_track(board, net, layer, start_xy, end_xy, width_mm=0.20):
    t = pcbnew.PCB_TRACK(board)
    t.SetNet(net)
    t.SetLayer(layer)
    t.SetWidth(to_nm(width_mm))
    t.SetStart(pcbnew.VECTOR2I(to_nm(start_xy[0]), to_nm(start_xy[1])))
    t.SetEnd(pcbnew.VECTOR2I(to_nm(end_xy[0]), to_nm(end_xy[1])))
    board.Add(t)
    return t

def add_via(board, net, xy, drill_mm=0.30, size_mm=0.60):
    v = pcbnew.PCB_VIA(board)
    v.SetNet(net)
    v.SetPosition(pcbnew.VECTOR2I(to_nm(xy[0]), to_nm(xy[1])))
    v.SetDrill(to_nm(drill_mm))
    v.SetWidth(to_nm(size_mm))
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    board.Add(v)
    return v

def route_pcba01():
    board = pcbnew.LoadBoard(PCB_FILE)
    print("Routing remediated signals on PCBA 01...")

    f_cu = board.GetLayerID("F.Cu")
    b_cu = board.GetLayerID("B.Cu")
    
    remediated_nets = ["USB_D_N", "USB_D_P", "I2S_BCLK", "I2S_WS", "UWB_IRQ", "RGB_LED_DATA"]
    
    # 1. Remove old tracks for these nets
    tracks_to_remove = []
    for t in board.GetTracks():
        netname = t.GetNetname()
        if netname in remediated_nets:
            tracks_to_remove.append(t)
            
    # Also remove any tracks touching U2 pad 26
    u2 = board.FindFootprintByReference("U2")
    pad26 = [p for p in u2.Pads() if p.GetNumber() == "26"][0]
    p26_box = pad26.GetBoundingBox()
    for t in board.GetTracks():
        if p26_box.Contains(t.GetStart()) or p26_box.Contains(t.GetEnd()):
            if t not in tracks_to_remove:
                tracks_to_remove.append(t)

    for t in tracks_to_remove:
        board.Remove(t)
    print(f"✓ Removed {len(tracks_to_remove)} old conflicting tracks.")

    # 2. Get destination pad positions
    def get_pad_pos(ref, pad_num):
        fp = board.FindFootprintByReference(ref)
        if not fp:
            return None
        pads = [p for p in fp.Pads() if p.GetNumber() == pad_num]
        if not pads:
            return None
        p = pads[0]
        return (to_mm(p.GetPosition().x), to_mm(p.GetPosition().y))

    # Net objects
    net_usb_n = board.FindNet("USB_D_N")
    net_usb_p = board.FindNet("USB_D_P")
    net_i2s_bclk = board.FindNet("I2S_BCLK")
    net_i2s_ws = board.FindNet("I2S_WS")
    net_uwb_irq = board.FindNet("UWB_IRQ")
    net_led = board.FindNet("RGB_LED_DATA")
    net_gnd = board.FindNet("GND_PWR")

    # Pad positions
    p_u2_13 = get_pad_pos("U2", "13") # (140.75, 95.98)
    p_u2_14 = get_pad_pos("U2", "14") # (140.75, 97.25)
    p_u2_26 = get_pad_pos("U2", "26") # (156.485, 98.50)
    p_u2_28 = get_pad_pos("U2", "28") # (158.25, 95.98)
    p_u2_30 = get_pad_pos("U2", "30") # (158.25, 93.44)
    p_u2_31 = get_pad_pos("U2", "31") # (158.25, 92.17)
    p_u2_32 = get_pad_pos("U2", "32") # (158.25, 90.90)

    p_j3_2 = get_pad_pos("J3", "2")   # USB D-
    p_j3_3 = get_pad_pos("J3", "3")   # USB D+
    p_d1_4 = get_pad_pos("D1", "4")   # LED DIN
    p_u3_2 = get_pad_pos("U3", "2")   # ES8388 BCLK
    p_u3_3 = get_pad_pos("U3", "3")   # ES8388 WS
    p_u9_4 = get_pad_pos("U9", "4")   # QCC3084 BCLK
    p_u9_5 = get_pad_pos("U9", "5")   # QCC3084 WS
    p_u8_13 = get_pad_pos("U8", "13") # DW3110 IRQ

    print(f"Routing targets:")
    print(f"  USB D- : U2.13 {p_u2_13} -> J3.2 {p_j3_2}")
    print(f"  USB D+ : U2.14 {p_u2_14} -> J3.3 {p_j3_3}")
    print(f"  LED    : U2.28 {p_u2_28} -> D1.4 {p_d1_4}")
    print(f"  BCLK   : U2.30 {p_u2_30} -> U3.2 {p_u3_2} & U9.4 {p_u9_4}")
    print(f"  UWB IRQ: U2.31 {p_u2_31} -> U8.13 {p_u8_13}")
    print(f"  WS     : U2.32 {p_u2_32} -> U3.3 {p_u3_3} & U9.5 {p_u9_5}")

    # 3. Route Pad 26 to GND_PWR (small stub to bottom ground plane via)
    add_track(board, net_gnd, f_cu, p_u2_26, (p_u2_26[0], p_u2_26[1] + 1.2), 0.3)
    add_via(board, net_gnd, (p_u2_26[0], p_u2_26[1] + 1.2))

    # 4. Route USB_D_N: U2.13 -> J3.2 (West down to South-West)
    # U2.13 is on F.Cu at (140.75, 95.98). J3.2 is at p_j3_2
    add_track(board, net_usb_n, f_cu, p_u2_13, (139.5, 95.98))
    add_track(board, net_usb_n, f_cu, (139.5, 95.98), (139.5, 112.0))
    add_via(board, net_usb_n, (139.5, 112.0))
    add_track(board, net_usb_n, b_cu, (139.5, 112.0), (p_j3_2[0], 112.0))
    add_track(board, net_usb_n, b_cu, (p_j3_2[0], 112.0), p_j3_2)

    # 5. Route USB_D_P: U2.14 -> J3.3
    # U2.14 is on F.Cu at (140.75, 97.25)
    add_track(board, net_usb_p, f_cu, p_u2_14, (138.8, 97.25))
    add_track(board, net_usb_p, f_cu, (138.8, 97.25), (138.8, 113.0))
    add_via(board, net_usb_p, (138.8, 113.0))
    add_track(board, net_usb_p, b_cu, (138.8, 113.0), (p_j3_3[0], 113.0))
    add_track(board, net_usb_p, b_cu, (p_j3_3[0], 113.0), p_j3_3)

    # 6. Route RGB_LED_DATA: U2.28 -> D1.4
    # U2.28 is at (158.25, 95.98). D1.4 is at p_d1_4
    add_track(board, net_led, f_cu, p_u2_28, (160.0, 95.98))
    add_via(board, net_led, (160.0, 95.98))
    add_track(board, net_led, b_cu, (160.0, 95.98), (160.0, 102.5))
    add_track(board, net_led, b_cu, (160.0, 102.5), (p_d1_4[0], 102.5))
    add_track(board, net_led, b_cu, (p_d1_4[0], 102.5), p_d1_4)

    # 7. Route UWB_IRQ: U2.31 -> U8.13
    # U2.31 is at (158.25, 92.17). U8.13 is on B.Cu at p_u8_13
    add_track(board, net_uwb_irq, f_cu, p_u2_31, (161.0, 92.17))
    add_via(board, net_uwb_irq, (161.0, 92.17))
    add_track(board, net_uwb_irq, b_cu, (161.0, 92.17), (161.0, 99.0))
    add_track(board, net_uwb_irq, b_cu, (161.0, 99.0), (p_u8_13[0], 99.0))
    add_track(board, net_uwb_irq, b_cu, (p_u8_13[0], 99.0), p_u8_13)

    # 8. Route I2S_BCLK: U2.30 -> U3.2 (ES8388) & U9.4 (QCC3084)
    # U2.30 is at (158.25, 93.44)
    add_track(board, net_i2s_bclk, f_cu, p_u2_30, (162.0, 93.44))
    add_track(board, net_i2s_bclk, f_cu, (162.0, 93.44), (162.0, 87.0))
    add_track(board, net_i2s_bclk, f_cu, (162.0, 87.0), p_u3_2)
    # Branch to U9.4
    if p_u9_4:
        add_via(board, net_i2s_bclk, (162.0, 93.44))
        add_track(board, net_i2s_bclk, b_cu, (162.0, 93.44), (p_u9_4[0], 93.44))
        add_track(board, net_i2s_bclk, b_cu, (p_u9_4[0], 93.44), p_u9_4)

    # 9. Route I2S_WS: U2.32 -> U3.3 (ES8388) & U9.5 (QCC3084)
    # U2.32 is at (158.25, 90.90)
    add_track(board, net_i2s_ws, f_cu, p_u2_32, (163.0, 90.90))
    add_track(board, net_i2s_ws, f_cu, (163.0, 90.90), (163.0, 86.0))
    add_track(board, net_i2s_ws, f_cu, (163.0, 86.0), p_u3_3)
    # Branch to U9.5
    if p_u9_5:
        add_via(board, net_i2s_ws, (163.0, 90.90))
        add_track(board, net_i2s_ws, b_cu, (163.0, 90.90), (p_u9_5[0], 90.90))
        add_track(board, net_i2s_ws, b_cu, (p_u9_5[0], 90.90), p_u9_5)

    # 10. Refill zones
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    print("✓ Refilled zones.")

    board.Save(PCB_FILE)
    print(f"✓ Saved {PCB_FILE}")

def run_drc():
    print("\n--- Running DRC Verification ---")
    json_path = "/tmp/route_drc.json"
    if os.path.exists(json_path):
        os.remove(json_path)
    cmd = [KICAD_CLI, "pcb", "drc", "--format", "json", "--output", json_path, PCB_FILE]
    subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(json_path):
        import json
        with open(json_path) as f:
            d = json.load(f)
        unconnected = len(d.get("unconnected_items", []))
        errors = [v for v in d.get("violations", []) if v.get("severity") == "error"]
        print(f"DRC Summary: Unconnected={unconnected} | Critical Errors={len(errors)}")
        if unconnected > 0:
            for item in d.get("unconnected_items", []):
                print(f"  - Unconnected: {item.get('description')} ({[i.get('description') for i in item.get('items', [])]})")
        if len(errors) > 0:
            for err in errors[:10]:
                print(f"  - Error [{err.get('type')}]: {err.get('description')}")
        return unconnected == 0 and len(errors) == 0
    return False

if __name__ == "__main__":
    route_pcba01()
    run_drc()
    os._exit(0)
