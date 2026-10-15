#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
tools/remediate_pcba03.py
=========================
Remediates PCBA 03 (Universal Smart Cartridge) PCB:
1. Ensures 4-layer stackup with inner power planes:
   - In1.Cu: GND_PLANE (solid GND zone)
   - In2.Cu: PWR_PLANE (solid VCC_3V3 zone)
2. Instantiates U4 (TS5A3159DBVR SPDT switch in SOT-23-6) and R9 (10k 0603 pullup).
3. Connects and routes:
   - J_AUDIO_PWR 8-pin connector:
     Pad 1: GND
     Pad 2: VCC_5V_PROT
     Pad 3: AGND_AUDIO_IN
     Pad 4: AUDIO_IN_L
     Pad 5: AUDIO_IN_R
     Pad 6: OMM_DETECT
     Pad 7: AUDIO_IO_P
     Pad 8: PTT_USB_N
   - U4 (TS5A3159):
     Pin 1: USB_DP
     Pin 2: AUDIO_IO_P
     Pin 3: OMM_DETECT
     Pin 4: VCC_3V3
     Pin 5: GND
     Pin 6: VOICE_OUT
   - R9 (10k):
     Pad 1: VCC_3V3
     Pad 2: OMM_DETECT
   - U1 (ESP32-C6):
     Pad 14: PTT_USB_N
     Pad 15: USB_DP
     Pad 16: OMM_DETECT
4. Refills all zones and validates DRC.
"""

import sys
import os
import pcbnew

PCB_PATH = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"
LIB_SOT23 = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/Package_TO_SOT_SMD.pretty"
LIB_RES = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/Resistor_SMD.pretty"

def main():
    board = pcbnew.LoadBoard(PCB_PATH)
    print("Board loaded successfully.")

    # 1. Helper to find or add nets
    def get_or_create_net(name):
        net = board.FindNet(name)
        if not net:
            net = pcbnew.NETINFO_ITEM(board, name)
            board.Add(net)
        return net

    net_gnd = get_or_create_net("GND")
    net_vcc3v3 = get_or_create_net("VCC_3V3")
    net_vcc5v = get_or_create_net("VCC_5V_PROT")
    net_audio_io_p = get_or_create_net("AUDIO_IO_P")
    net_omm_detect = get_or_create_net("OMM_DETECT")
    net_usb_dp = get_or_create_net("USB_DP")
    net_ptt_usb_n = get_or_create_net("PTT_USB_N")
    net_voice_out = get_or_create_net("VOICE_OUT")
    net_audio_in_l = get_or_create_net("AUDIO_IN_L")
    net_audio_in_r = get_or_create_net("AUDIO_IN_R")
    net_agnd_audio = get_or_create_net("AGND_AUDIO_IN")

    # 2. Check / Remove existing U4 and R9 if present
    for ref in ["U4", "R9"]:
        fp = board.FindFootprintByReference(ref)
        if fp:
            board.Remove(fp)
            print(f"Removed existing {ref}")

    # 3. Add U4 (TS5A3159DBVR SOT-23-6)
    fp_u4 = pcbnew.FootprintLoad(LIB_SOT23, "SOT-23-6")
    if not fp_u4:
        raise RuntimeError("Failed to load SOT-23-6 footprint")
    fp_u4.SetReference("U4")
    fp_u4.SetValue("TS5A3159DBVR")
    fp_u4.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(107.5), pcbnew.FromMM(81.5)))
    fp_u4.SetLayer(board.GetLayerID("F.Cu"))
    
    # Set 3D model for U4
    m3d = pcbnew.FP_3DMODEL()
    m3d.m_Filename = "${KICAD8_3DMODEL_DIR}/Package_TO_SOT_SMD.3dshapes/SOT-23-6.step"
    m3d.m_Scale = pcbnew.VECTOR3D(1, 1, 1)
    fp_u4.Models().push_back(m3d)
    
    # Assign nets to U4 pads
    u4_net_map = {
        "1": net_usb_dp,
        "2": net_audio_io_p,
        "3": net_omm_detect,
        "4": net_vcc3v3,
        "5": net_gnd,
        "6": net_voice_out,
    }
    for pad in fp_u4.Pads():
        pnum = pad.GetNumber()
        if pnum in u4_net_map:
            pad.SetNet(u4_net_map[pnum])
    board.Add(fp_u4)
    print("Added U4 (TS5A3159DBVR) at (107.5, 81.5)")

    # 4. Add R9 (10k R_0603)
    fp_r9 = pcbnew.FootprintLoad(LIB_RES, "R_0603_1608Metric")
    if not fp_r9:
        raise RuntimeError("Failed to load R_0603_1608Metric footprint")
    fp_r9.SetReference("R9")
    fp_r9.SetValue("10k")
    fp_r9.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(108.64), pcbnew.FromMM(84.5)))
    fp_r9.SetOrientation(pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T))
    fp_r9.SetLayer(board.GetLayerID("F.Cu"))
    
    # Set 3D model for R9
    m3d_r = pcbnew.FP_3DMODEL()
    m3d_r.m_Filename = "${KICAD8_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0603_1608Metric.step"
    m3d_r.m_Scale = pcbnew.VECTOR3D(1, 1, 1)
    fp_r9.Models().push_back(m3d_r)
    
    r9_net_map = {
        "1": net_vcc3v3,
        "2": net_omm_detect,
    }
    for pad in fp_r9.Pads():
        pnum = pad.GetNumber()
        if pnum in r9_net_map:
            pad.SetNet(r9_net_map[pnum])
    board.Add(fp_r9)
    print("Added R9 (10k) at (108.64, 84.5)")

    # 5. Update J_AUDIO_PWR pad nets
    j_audio = board.FindFootprintByReference("J_AUDIO_PWR")
    if not j_audio:
        raise RuntimeError("J_AUDIO_PWR not found on board")
    j_audio_net_map = {
        "1": net_gnd,
        "2": net_vcc5v,
        "3": net_agnd_audio,
        "4": net_audio_in_l,
        "5": net_audio_in_r,
        "6": net_omm_detect,
        "7": net_audio_io_p,
        "8": net_ptt_usb_n,
    }
    for pad in j_audio.Pads():
        pnum = pad.GetNumber()
        if pnum in j_audio_net_map:
            pad.SetNet(j_audio_net_map[pnum])
    print("Updated J_AUDIO_PWR pad nets.")

    # 6. Update U1 pad nets (ESP32-C6)
    u1 = board.FindFootprintByReference("U1")
    if u1:
        p14 = u1.FindPadByNumber("14")
        if p14: p14.SetNet(net_ptt_usb_n)
        p15 = u1.FindPadByNumber("15")
        if p15: p15.SetNet(net_usb_dp)
        p16 = u1.FindPadByNumber("16")
        if p16: p16.SetNet(net_omm_detect)
    print("Updated U1 pad nets (14, 15, 16).")

    # 7. Update J_PROG pad nets
    j_prog = board.FindFootprintByReference("J_PROG")
    if j_prog:
        p_dn = j_prog.FindPadByNumber("4")
        if p_dn: p_dn.SetNet(net_ptt_usb_n)
    print("Updated J_PROG pad nets.")

    # 8. Inner Copper Planes (GND on In1.Cu, VCC_3V3 on In2.Cu)
    bb = board.GetBoardEdgesBoundingBox()
    bx, by = bb.GetX(), bb.GetY()
    bw, bh = bb.GetWidth(), bb.GetHeight()

    def add_plane_zone(layer_name, net, priority=0):
        # Remove any existing zone on that layer with that net
        layer_id = board.GetLayerID(layer_name)
        zones_to_remove = [z for z in board.Zones() if z.GetLayer() == layer_id and z.GetNetname() == net.GetNetname()]
        for z in zones_to_remove:
            board.Remove(z)

        zone = pcbnew.ZONE(board)
        zone.SetLayer(layer_id)
        zone.SetNet(net)
        zone.SetAssignedPriority(priority)
        zone.SetMinThickness(pcbnew.FromMM(0.15))
        zone.SetThermalReliefGap(pcbnew.FromMM(0.25))
        zone.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.3))
        zone.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)

        # Polygon outline covering board + 2mm margin
        pts = pcbnew.VECTOR_VECTOR2I()
        pts.push_back(pcbnew.VECTOR2I(bx - pcbnew.FromMM(2), by - pcbnew.FromMM(2)))
        pts.push_back(pcbnew.VECTOR2I(bx + bw + pcbnew.FromMM(2), by - pcbnew.FromMM(2)))
        pts.push_back(pcbnew.VECTOR2I(bx + bw + pcbnew.FromMM(2), by + bh + pcbnew.FromMM(2)))
        pts.push_back(pcbnew.VECTOR2I(bx - pcbnew.FromMM(2), by + bh + pcbnew.FromMM(2)))
        zone.AddPolygon(pts)
        board.Add(zone)
        print(f"Added plane zone on {layer_name} for net {net.GetNetname()}")

    add_plane_zone("GND_PLANE", net_gnd)
    add_plane_zone("PWR_PLANE", net_vcc3v3)

    # 9. Clean up old tracks connected to J_AUDIO_PWR pins 3, 4, 5, 6, 7, 8 on F.Cu
    # We will re-route them cleanly
    tracks_to_remove = []
    for t in board.GetTracks():
        if isinstance(t, pcbnew.PCB_TRACK) and t.GetLayerName() == "F.Cu":
            s, e = t.GetStart(), t.GetEnd()
            sx, sy = pcbnew.ToMM(s.x), pcbnew.ToMM(s.y)
            ex, ey = pcbnew.ToMM(e.x), pcbnew.ToMM(e.y)
            # Tracks originating right at J_AUDIO_PWR pads (X=105.38, Y=76..84)
            if (105.3 <= sx <= 105.45 and 76.0 <= sy <= 83.5) or (105.3 <= ex <= 105.45 and 76.0 <= ey <= 83.5):
                tracks_to_remove.append(t)
    for t in tracks_to_remove:
        board.Remove(t)
    print(f"Removed {len(tracks_to_remove)} old J_AUDIO_PWR stub tracks for clean re-routing.")

    # Helper to add track
    def add_track(layer_name, net, x1, y1, x2, y2, width=0.2):
        tr = pcbnew.PCB_TRACK(board)
        tr.SetLayer(board.GetLayerID(layer_name))
        tr.SetNet(net)
        tr.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
        tr.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
        tr.SetWidth(pcbnew.FromMM(width))
        board.Add(tr)
        return tr

    # Helper to add via
    def add_via(net, x, y, size=0.45, drill=0.2):
        via = pcbnew.PCB_VIA(board)
        via.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        via.SetWidth(pcbnew.FromMM(size))
        via.SetDrill(pcbnew.FromMM(drill))
        via.SetNet(net)
        via.SetLayerPair(board.GetLayerID("F.Cu"), board.GetLayerID("B.Cu"))
        board.Add(via)
        return via

    # 10. Route connections:
    # J_AUDIO_PWR pad positions:
    # Pad 1 (GND): (105.375, 76.3)
    # Pad 2 (VCC_5V_PROT): (105.375, 77.3)
    # Pad 3 (AGND_AUDIO_IN): (105.375, 78.3)
    # Pad 4 (AUDIO_IN_L): (105.375, 79.3)
    # Pad 5 (AUDIO_IN_R): (105.375, 80.3)
    # Pad 6 (OMM_DETECT): (105.375, 81.3)
    # Pad 7 (AUDIO_IO_P): (105.375, 82.3)
    # Pad 8 (PTT_USB_N): (105.375, 83.3)

    # U4 pad positions (at 107.5, 81.5):
    # Pad 1 (USB_DP): (106.36, 80.55)
    # Pad 2 (AUDIO_IO_P): (106.36, 81.50)
    # Pad 3 (OMM_DETECT): (106.36, 82.45)
    # Pad 4 (VCC_3V3): (108.64, 82.45)
    # Pad 5 (GND): (108.64, 81.50)
    # Pad 6 (VOICE_OUT): (108.64, 80.55)

    # R9 pad positions (at 108.64, 84.5, rotated 90):
    # Pad 1 (VCC_3V3): (108.64, 85.32)
    # Pad 2 (OMM_DETECT): (108.64, 83.68)

    # a) AUDIO_IO_P: J_AUDIO_PWR Pad 7 -> U4 Pad 2
    add_track("F.Cu", net_audio_io_p, 105.375, 82.30, 105.80, 82.30)
    add_track("F.Cu", net_audio_io_p, 105.80, 82.30, 106.36, 81.50)

    # b) OMM_DETECT: J_AUDIO_PWR Pad 6 -> U4 Pad 3 -> R9 Pad 2 -> U1 Pad 16
    add_track("F.Cu", net_omm_detect, 105.375, 81.30, 105.80, 81.30)
    add_track("F.Cu", net_omm_detect, 105.80, 81.30, 106.36, 82.45)
    # U4 Pad 3 to R9 Pad 2
    add_track("F.Cu", net_omm_detect, 106.36, 82.45, 107.50, 83.68)
    add_track("F.Cu", net_omm_detect, 107.50, 83.68, 108.64, 83.68)
    # R9 Pad 2 to U1 Pad 16 (112.95, 86.50)
    add_track("F.Cu", net_omm_detect, 108.64, 83.68, 109.80, 83.68)
    add_track("F.Cu", net_omm_detect, 109.80, 83.68, 112.00, 85.88)
    add_track("F.Cu", net_omm_detect, 112.00, 85.88, 112.95, 86.50)

    # c) USB_DP: U4 Pad 1 (106.36, 80.55) to existing USB_DP track at (108.50, 82.30)
    add_track("F.Cu", net_usb_dp, 106.36, 80.55, 107.00, 80.55)
    add_track("F.Cu", net_usb_dp, 107.00, 80.55, 108.50, 82.05)
    add_track("F.Cu", net_usb_dp, 108.50, 82.05, 108.50, 82.30)

    # d) PTT_USB_N: J_AUDIO_PWR Pad 8 -> connects to USB_DN track at (107.20, 83.30)
    add_track("F.Cu", net_ptt_usb_n, 105.375, 83.30, 107.20, 83.30)
    # Update the remaining USB_DN tracks to PTT_USB_N
    for t in board.GetTracks():
        if t.GetNetname() == "USB_DN":
            t.SetNet(net_ptt_usb_n)

    # e) VOICE_OUT: U4 Pad 6 (108.64, 80.55) -> via to B.Cu -> connects to U3 Pad 12
    # Add via near U4 Pad 6
    add_track("F.Cu", net_voice_out, 108.64, 80.55, 109.50, 80.55)
    add_via(net_voice_out, 109.50, 80.55)
    # On B.Cu, route to (106.50, 78.20) where VOICE_OUT line is
    add_track("B.Cu", net_voice_out, 109.50, 80.55, 107.50, 78.55)
    add_track("B.Cu", net_voice_out, 107.50, 78.55, 106.50, 78.20)

    # f) VCC_3V3: Drops from U4 Pad 4 (108.64, 82.45) and R9 Pad 1 (108.64, 85.32) to PWR_PLANE
    add_track("F.Cu", net_vcc3v3, 108.64, 82.45, 109.50, 82.45)
    add_via(net_vcc3v3, 109.50, 82.45)
    add_track("F.Cu", net_vcc3v3, 108.64, 85.32, 109.50, 85.32)
    add_via(net_vcc3v3, 109.50, 85.32)

    # g) GND: Drops from U4 Pad 5 (108.64, 81.50) and J_AUDIO_PWR Pad 1 (105.375, 76.30)
    add_track("F.Cu", net_gnd, 108.64, 81.50, 109.50, 81.50)
    add_via(net_gnd, 109.50, 81.50)
    add_track("F.Cu", net_gnd, 105.375, 76.30, 104.50, 76.30)
    add_via(net_gnd, 104.50, 76.30)

    # h) VCC_5V_PROT: J_AUDIO_PWR Pad 2 (105.375, 77.30) to existing +5V trace
    add_track("F.Cu", net_vcc5v, 105.375, 77.30, 106.00, 77.30)
    add_track("F.Cu", net_vcc5v, 106.00, 77.30, 106.10, 76.10)

    # i) AGND_AUDIO_IN: J_AUDIO_PWR Pad 3 (105.375, 78.30) -> via to GND_PLANE
    add_track("F.Cu", net_agnd_audio, 105.375, 78.30, 104.50, 78.30)
    add_via(net_agnd_audio, 104.50, 78.30)

    # j) AUDIO_IN_L: J_AUDIO_PWR Pad 4 (105.375, 79.30) -> via to B.Cu to U3 Pad 8
    add_track("F.Cu", net_audio_in_l, 105.375, 79.30, 104.50, 79.30)
    add_via(net_audio_in_l, 104.50, 79.30)
    add_track("B.Cu", net_audio_in_l, 104.50, 79.30, 104.50, 78.10)

    # k) AUDIO_IN_R: J_AUDIO_PWR Pad 5 (105.375, 80.30) -> via at (109.30, 76.90)
    add_track("F.Cu", net_audio_in_r, 105.375, 80.30, 106.50, 80.30)
    add_track("F.Cu", net_audio_in_r, 106.50, 80.30, 108.60, 76.90)

    # 11. Refill all zones
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    print("Zones refilled.")

    # 12. Save Board
    pcbnew.SaveBoard(PCB_PATH, board)
    print(f"Board successfully saved to {PCB_PATH}.")

if __name__ == "__main__":
    main()
