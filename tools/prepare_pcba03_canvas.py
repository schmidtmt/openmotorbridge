#!/usr/bin/env python3
"""
tools/prepare_pcba03_canvas.py
------------------------------
Reference script matching the REAL physical layout of PCBA 03 (Pod Interface Board):
- Dimensions: 42.0 x 48.0 mm (X: 100.0..142.0, Y: 56.0..104.0) with 2.0 mm chamfers
- Single-sided SMT: 100% of all components mounted on F.Cu (Top Layer)
- Bottom layer (B.Cu) is an unbroken solid GND plane (ENIG)
- 4x M2.5 mounting holes at (103, 59), (103, 101), (139, 59), (139, 101)

Layout Topology (F.Cu):
- Left Edge: J_BUS at (103.50, 93.03) & J_USB_OUT at (103.50, 66.97)
- Top Zone: U_PD (SW3516) at (114.25, 67.69), L_PD at (124.25, 62.25), C_PD_IN/OUT, F1
- Center-Left: U1 (ESP32-C6-MINI-1) at (108.50, 80.00, rot 90)
- Right Edge Upper: J_ACT (8P/4P) at (138.95, 74.45) with Q1..Q4, D1..D4, R1..R8 on F.Cu
- Right Edge Lower: J_AUDIO_PWR (8P) at (138.95, 90.70) with U3 (ES8388) & U4 (TS5A3159) on F.Cu
"""

import os
import re
import uuid

PCB_PATH = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"

def get_current_pcb_info():
    if not os.path.exists(PCB_PATH):
        return None
    with open(PCB_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    
    fps = re.findall(
        r'\(footprint\s+\"([^\"]+)\".*?\(layer\s+\"([^\"]+)\"\).*?\(at\s+([-\d\.]+)\s+([-\d\.]+)(?:\s+([-\d\.]+))?\).*?\(property\s+\"Reference\"\s+\"([^\"]+)\"',
        text, re.DOTALL
    )
    return {ref: {"fp": fp, "layer": layer, "x": float(x), "y": float(y), "rot": float(rot or 0)} for fp, layer, x, y, rot, ref in fps}

if __name__ == "__main__":
    info = get_current_pcb_info()
    if info:
        print(f"PCBA 03 Reality Check: {len(info)} components on PCB:")
        for ref in sorted(info.keys()):
            c = info[ref]
            print(f"  {ref:12} | Layer: {c['layer']:5} | ({c['x']:6.2f}, {c['y']:6.2f}, rot={c['rot']:3}) | {c['fp']}")
