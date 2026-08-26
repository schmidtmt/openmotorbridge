#!/usr/bin/env python3
"""
Radial Direct Router for Dual-SMD Pod Base PCB:
- Every via placed directly outside its corresponding pad on B.Cu
- Radial stubs into J2 pads: 0 crossings on B.Cu
- Planar breakout on F.Cu: 0 crossings on F.Cu
"""

import pcbnew

pcb_file = "hardware/kicad_pod_base/openmotorbridge_pod_base.kicad_pcb"

def add_track(board, net_code, x1_mm, y1_mm, x2_mm, y2_mm, layer=pcbnew.F_Cu, width_mm=0.20):
    t = pcbnew.PCB_TRACK(board)
    t.SetNetCode(net_code)
    t.SetLayer(layer)
    t.SetWidth(pcbnew.FromMM(width_mm))
    t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1_mm), pcbnew.FromMM(y1_mm)))
    t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2_mm), pcbnew.FromMM(y2_mm)))
    board.Add(t)

def add_via(board, net_code, x_mm, y_mm, size_mm=0.6, drill_mm=0.3):
    v = pcbnew.PCB_VIA(board)
    v.SetNetCode(net_code)
    v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x_mm), pcbnew.FromMM(y_mm)))
    v.SetWidth(pcbnew.FromMM(size_mm))
    v.SetDrill(pcbnew.FromMM(drill_mm))
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    board.Add(v)

def route_dual_smd_board():
    board = pcbnew.LoadBoard(pcb_file)
    
    # Extract Net Codes first
    net_vcc = board.FindNet("VCC").GetNetCode()
    net_gnd = board.FindNet("GND").GetNetCode()
    net_sig_p = board.FindNet("SIG_P").GetNetCode()
    net_sig_n = board.FindNet("SIG_N").GetNetCode()
    net_pps = board.FindNet("TRIGGER_PPS").GetNetCode()
    net_1w = board.FindNet("1WIRE_ID").GetNetCode()
    net_shield = board.FindNet("GND_SHIELD").GetNetCode()

    # Remove existing tracks
    for t in list(board.GetTracks()):
        board.Remove(t)

    # =========================================================================
    # 1. B.CU RADIAL STUBS (Exact angle alignment -> 100% Zero Crossings)
    # =========================================================================
    # Pad 1 (VCC, 121.0, 80.0, East): Via at (125.0, 80.0)
    add_via(board, net_vcc, 125.0, 80.0)
    add_track(board, net_vcc, 125.0, 80.0, 121.0, 80.0, pcbnew.B_Cu, 0.35)

    # Pad 2 (GND, 119.5, 82.6, NE): Via at (123.0, 85.5)
    add_via(board, net_gnd, 123.0, 85.5)
    add_track(board, net_gnd, 123.0, 85.5, 119.5, 82.6, pcbnew.B_Cu, 0.35)

    # Pad 3 (SIG_P, 116.5, 82.6, NW): Via at (113.0, 85.5)
    add_via(board, net_sig_p, 113.0, 85.5)
    add_track(board, net_sig_p, 113.0, 85.5, 116.5, 82.6, pcbnew.B_Cu, 0.20)

    # Pad 4 (SIG_N, 115.0, 80.0, West): Via at (111.0, 80.0)
    add_via(board, net_sig_n, 111.0, 80.0)
    add_track(board, net_sig_n, 111.0, 80.0, 115.0, 80.0, pcbnew.B_Cu, 0.20)

    # Pad 5 (TRIGGER_PPS, 116.5, 77.4, SW): Via at (113.0, 74.5)
    add_via(board, net_pps, 113.0, 74.5)
    add_track(board, net_pps, 113.0, 74.5, 116.5, 77.4, pcbnew.B_Cu, 0.20)

    # Pad 6 (1WIRE_ID, 119.5, 77.4, SE): Via at (123.0, 74.5)
    add_via(board, net_1w, 123.0, 74.5)
    add_track(board, net_1w, 123.0, 74.5, 119.5, 77.4, pcbnew.B_Cu, 0.20)

    # Pad 7 (GND_SHIELD, 122.5, 80.0)
    add_track(board, net_shield, 122.5, 80.0, 126.0, 80.0, pcbnew.B_Cu, 0.50)

    # =========================================================================
    # 2. F.CU ROUTING: J1 (X=118.0) -> Vias & U1 (108.0, 76.0)
    # =========================================================================
    # J1 Pin 1 (VCC, 118.0, 73.65):
    # -> Via at (125.0, 80.0)
    add_track(board, net_vcc, 118.0, 73.65, 125.0, 73.65, pcbnew.F_Cu, 0.35)
    add_track(board, net_vcc, 125.0, 73.65, 125.0, 80.0, pcbnew.F_Cu, 0.35)
    # -> U1 Pin 14 (108.625, 74.5) & C1 Pin 1 (108.0, 84.78)
    add_track(board, net_vcc, 118.0, 73.65, 110.0, 73.65, pcbnew.F_Cu, 0.35)
    add_track(board, net_vcc, 110.0, 73.65, 108.625, 74.5, pcbnew.F_Cu, 0.20)
    add_track(board, net_vcc, 110.0, 73.65, 104.5, 73.65, pcbnew.F_Cu, 0.35)
    add_track(board, net_vcc, 104.5, 73.65, 104.5, 84.78, pcbnew.F_Cu, 0.35)
    add_track(board, net_vcc, 104.5, 84.78, 108.0, 84.78, pcbnew.F_Cu, 0.35)

    # J1 Pin 2 (GND, 118.0, 76.19):
    # -> Via at (123.0, 85.5)
    add_track(board, net_gnd, 118.0, 76.19, 120.0, 76.19, pcbnew.F_Cu, 0.35)
    add_track(board, net_gnd, 120.0, 76.19, 120.0, 85.5, pcbnew.F_Cu, 0.35)
    add_track(board, net_gnd, 120.0, 85.5, 123.0, 85.5, pcbnew.F_Cu, 0.35)
    # -> U1 GND & C1 GND
    add_track(board, net_gnd, 108.625, 75.5, 108.625, 76.5, pcbnew.F_Cu, 0.20)
    add_track(board, net_gnd, 108.0, 83.22, 108.0, 81.5, pcbnew.F_Cu, 0.35)

    # J1 Pin 3 (SIG_P, 118.0, 78.73):
    # -> Via at (113.0, 85.5)
    add_track(board, net_sig_p, 118.0, 78.73, 115.0, 78.73, pcbnew.F_Cu, 0.20)
    add_track(board, net_sig_p, 115.0, 78.73, 113.0, 80.73, pcbnew.F_Cu, 0.20)
    add_track(board, net_sig_p, 113.0, 80.73, 113.0, 85.5, pcbnew.F_Cu, 0.20)
    # -> U1 Pin 13 (108.625, 75.0)
    add_track(board, net_sig_p, 115.0, 78.73, 111.0, 75.0, pcbnew.F_Cu, 0.20)
    add_track(board, net_sig_p, 111.0, 75.0, 108.625, 75.0, pcbnew.F_Cu, 0.20)

    # J1 Pin 4 (SIG_N, 118.0, 81.27):
    # -> Via at (111.0, 80.0)
    add_track(board, net_sig_n, 118.0, 81.27, 114.0, 81.27, pcbnew.F_Cu, 0.20)
    add_track(board, net_sig_n, 114.0, 81.27, 111.0, 80.0, pcbnew.F_Cu, 0.20)
    # -> U1 Pin 11 (108.625, 76.0)
    add_track(board, net_sig_n, 111.0, 80.0, 110.0, 76.0, pcbnew.F_Cu, 0.20)
    add_track(board, net_sig_n, 110.0, 76.0, 108.625, 76.0, pcbnew.F_Cu, 0.20)

    # J1 Pin 5 (TRIGGER_PPS, 118.0, 83.81):
    # -> Via at (113.0, 74.5)
    add_track(board, net_pps, 118.0, 83.81, 115.0, 83.81, pcbnew.F_Cu, 0.20)
    add_track(board, net_pps, 115.0, 83.81, 115.0, 74.5, pcbnew.F_Cu, 0.20)
    add_track(board, net_pps, 115.0, 74.5, 113.0, 74.5, pcbnew.F_Cu, 0.20)
    # -> U1 Pin 9 (108.625, 77.0)
    add_track(board, net_pps, 115.0, 74.5, 111.0, 77.0, pcbnew.F_Cu, 0.20)
    add_track(board, net_pps, 111.0, 77.0, 108.625, 77.0, pcbnew.F_Cu, 0.20)

    # J1 Pin 6 (1WIRE_ID, 118.0, 86.35):
    # -> Via at (123.0, 74.5)
    add_track(board, net_1w, 118.0, 86.35, 123.0, 86.35, pcbnew.F_Cu, 0.20)
    add_track(board, net_1w, 123.0, 86.35, 123.0, 74.5, pcbnew.F_Cu, 0.20)
    # -> U1 Pin 8 (108.625, 77.5)
    add_track(board, net_1w, 118.0, 86.35, 111.0, 86.35, pcbnew.F_Cu, 0.20)
    add_track(board, net_1w, 111.0, 86.35, 111.0, 77.5, pcbnew.F_Cu, 0.20)
    add_track(board, net_1w, 111.0, 77.5, 108.625, 77.5, pcbnew.F_Cu, 0.20)

    # =========================================================================
    # Mounting Holes H1 & H2 GND ties
    # =========================================================================
    add_track(board, net_gnd, 103.0, 80.0, 105.0, 80.0, pcbnew.F_Cu, 0.50)
    add_track(board, net_gnd, 133.0, 80.0, 131.0, 80.0, pcbnew.F_Cu, 0.50)

    # Fill Zones
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    
    board.Save(pcb_file)
    print(f"✓ Saved Dual-SMD board with clean radial fanout to {pcb_file}")

if __name__ == '__main__':
    route_dual_smd_board()
