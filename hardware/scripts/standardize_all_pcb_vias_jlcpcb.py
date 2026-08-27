#!/usr/bin/env python3
"""
Standardize all PCB vias to JLCPCB Mechanical Standard (0.30 mm Drill, 0.60 mm Pad, 0.15 mm Annular Ring)
--------------------------------------------------------------------------------------------------------
"""

import pcbnew

BOARDS = [
    "hardware/kicad_main_box/openmotorbridge_main.kicad_pcb",
    "hardware/kicad_pod_base/openmotorbridge_pod_base.kicad_pcb",
    "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb",
    "hardware/kicad_rear_pod3/openmotorbridge_rear_pod3.kicad_pcb"
]

for path in BOARDS:
    board = pcbnew.LoadBoard(path)
    count = 0
    for t in board.GetTracks():
        if isinstance(t, pcbnew.PCB_VIA):
            # Update to standard JLCPCB drill & pad
            t.SetDrill(pcbnew.FromMM(0.30))
            t.SetWidth(pcbnew.FromMM(0.60))
            count += 1
            
    # Standardize trace widths below 0.127 mm to standard 0.15 mm
    t_count = 0
    for t in board.GetTracks():
        if not isinstance(t, pcbnew.PCB_VIA):
            if pcbnew.ToMM(t.GetWidth()) < 0.127:
                t.SetWidth(pcbnew.FromMM(0.15))
                t_count += 1
                
    pcbnew.SaveBoard(path, board)
    print(f"✓ {path}: Standardized {count} vias (0.3/0.6 mm) and {t_count} traces (>=0.15 mm)")
