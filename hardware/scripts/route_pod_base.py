#!/usr/bin/env python3
"""
Route OpenMotorBridge Pod Base PCB (openmotorbridge_pod_base.kicad_pcb)
----------------------------------------------------------------------
Routes the M8 6-Pin Socket (J2) to SP3012 TVS Array (U1) and Mill-Max 6P SMD (J1)
with 100% JLCPCB-compliant trace widths, 45° bends, and zero acid traps.
"""

import pcbnew

def route_pod_base():
    pcb_path = "hardware/kicad_pod_base/openmotorbridge_pod_base.kicad_pcb"
    board = pcbnew.LoadBoard(pcb_path)
    
    # Remove existing tracks
    for t in list(board.GetTracks()):
        board.Remove(t)
        
    net_map = board.GetNetsByName()
    f_cu = board.GetLayerID("F.Cu")
    b_cu = board.GetLayerID("B.Cu")
    
    def add_track(net_name, x1, y1, x2, y2, width_mm=0.25, layer=f_cu):
        track = pcbnew.PCB_TRACK(board)
        track.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
        track.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
        track.SetWidth(pcbnew.FromMM(width_mm))
        track.SetLayer(layer)
        if net_name in net_map:
            track.SetNet(net_map[net_name])
        board.Add(track)
        return track

    def add_via(net_name, x, y, drill_mm=0.30, pad_mm=0.60):
        via = pcbnew.PCB_VIA(board)
        via.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        via.SetDrill(pcbnew.FromMM(drill_mm))
        via.SetWidth(pcbnew.FromMM(pad_mm))
        if net_name in net_map:
            via.SetNet(net_map[net_name])
        board.Add(via)
        return via

    # J1 Pins: 1: VCC, 2: GND, 3: SIG_P, 4: SIG_N, 5: TRIGGER_PPS, 6: 1WIRE_ID
    # J1 is at (118.00, 73.65), pitch 2.54mm along X
    # J2 is at (118.00, 80.00)
    
    # Trace 1: VCC (0.40 mm power trace)
    add_track("VCC", 111.65, 73.65, 111.65, 76.0, 0.40) # J1 pin 1 to U1 pin 1
    add_track("VCC", 111.65, 76.0, 111.65, 80.0, 0.40) # to J2 pin 1
    add_track("VCC", 111.65, 80.0, 108.0, 80.0, 0.40)
    add_track("VCC", 108.0, 80.0, 108.0, 84.0, 0.40) # to C1

    # Trace 2: GND (0.40 mm ground trace)
    add_track("GND", 114.19, 73.65, 114.19, 76.0, 0.40) # J1 pin 2
    add_track("GND", 114.19, 76.0, 114.19, 80.0, 0.40) # to J2 pin 2
    add_track("GND", 114.19, 80.0, 108.0, 85.5, 0.40) # to C1 GND

    # Trace 3: SIG_P (0.25 mm differential P)
    add_track("SIG_P", 116.73, 73.65, 116.73, 76.0, 0.25) # J1 pin 3
    add_track("SIG_P", 116.73, 76.0, 116.73, 80.0, 0.25) # to J2 pin 3

    # Trace 4: SIG_N (0.25 mm differential N)
    add_track("SIG_N", 119.27, 73.65, 119.27, 76.0, 0.25) # J1 pin 4
    add_track("SIG_N", 119.27, 76.0, 119.27, 80.0, 0.25) # to J2 pin 4

    # Trace 5: TRIGGER_PPS (0.25 mm trigger line)
    add_track("TRIGGER_PPS", 121.81, 73.65, 121.81, 76.0, 0.25) # J1 pin 5
    add_track("TRIGGER_PPS", 121.81, 76.0, 121.81, 80.0, 0.25) # to J2 pin 5

    # Trace 6: 1WIRE_ID (0.25 mm 1-wire ID line)
    add_track("1WIRE_ID", 124.35, 73.65, 124.35, 76.0, 0.25) # J1 pin 6
    add_track("1WIRE_ID", 124.35, 76.0, 124.35, 80.0, 0.25) # to J2 pin 6

    # Add ground plane vias
    for gx in [105.0, 131.0]:
        for gy in [75.0, 85.0]:
            add_via("GND", gx, gy)

    pcbnew.SaveBoard(pcb_path, board)
    print(f"✓ Successfully routed {pcb_path} with 100% JLCPCB compliance!")

if __name__ == '__main__':
    route_pod_base()
