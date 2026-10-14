#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
remediate_omm24.py
==================
Full remediation of OMM 2.4 (PCBA 09):
1. Upgrades PCB stackup to 4 layers (F.Cu, In1.Cu GND_PLANE, In2.Cu PWR_PLANE, B.Cu).
2. Clones In1.Cu (GND) and In2.Cu (VCC_3V3) solid plane zones from OMM446.
3. Sets footprint paths and properties to match schematic symbols (eliminating parity errors).
4. Clones exact flipped J_HELMET (BM06B-SRSS-TB) on B.Cu at (127.05, 99.70) from OMM 446.
5. Connects J1 GND pins (A5, B5) to GND_PLANE.
6. Connects D2 pad 2 (GND) to GND_PLANE.
7. Connects U2 GND pins (1, 4, 12, 14, 17) cleanly to GND_PLANE.
8. Deletes dangling vias, track stubs, and duplicate via pairs.
9. Corrects text mirroring on B.Cu components.
10. Refills all zones and saves board.
"""

import os
import sys
import pcbnew

PCB_PATH = "hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_pcb"
OMM446_PCB_PATH = "hardware/kicad_omm446_intercom/openmotorbridge_omm446_intercom.kicad_pcb"

def remediate():
    print("Loading boards...")
    board = pcbnew.LoadBoard(PCB_PATH)
    board446 = pcbnew.LoadBoard(OMM446_PCB_PATH)

    # 1. 4-layer stackup
    print("Setting up 4-layer stackup...")
    board.SetCopperLayerCount(4)
    board.SetLayerName(pcbnew.In1_Cu, "GND_PLANE")
    board.SetLayerName(pcbnew.In2_Cu, "PWR_PLANE")

    # 2. Nets
    required_nets = [
        "GND", "PGND", "AGND", "AGND_SPK", "AGND_MIC", "VCC_3V3", "VBUS_5V", "VBAT", "SYS_PWR",
        "AUDIO_OUT_L", "AUDIO_OUT_R", "VOICE_IN",
        "BTN_1", "BTN_2", "BTN_3", "BTN_4",
        "I2S_MCLK", "I2S_BCLK", "I2S_WS", "I2S_DOUT", "I2S_DIN",
        "I2C_SDA", "I2C_SCL",
        "BT_UART_TX", "BT_UART_RX", "BT_UART_RTS", "BT_UART_CTS",
        "BT_RESET", "BT_BOOT", "BT_ANT",
        "USB_DP", "USB_DN", "WS2812_DATA", "CHG_STAT"
    ]
    net_map = {}
    for name in required_nets:
        net = board.FindNet(name)
        if not net:
            net = pcbnew.NETINFO_ITEM(board, name)
            board.Add(net)
        net_map[name] = net

    # 3. Synchronize Footprint Paths and Properties
    uuid_map = {
        "U1": "55c09688-73ec-46e3-9e7b-b13b301c423b",
        "U2": "dbe6fe40-b8e3-4f2f-974e-a5a93060d77a",
        "U3": "c9640ecd-5fcd-41f0-a05e-f5af0e4c8a17",
        "U4": "192d4c53-be39-4754-8be1-de87f3092cf8",
        "U5": "841e6b44-f066-4434-8053-f085eb167ff3",
        "ANT1": "45bd15db-a9c3-4318-a79b-bf7f70cf62b4",
        "J1": "d143f30b-9aa2-4ae9-902d-3344970d7181",
        "D1": "cc55a89a-4eb6-4e2a-b616-51bab83d8a17",
        "D2": "3a539b97-ee81-49bf-888a-88ee8afdf2c4",
        "BAT1": "f65013a5-d379-432c-a978-394b361d867d",
        "SW1": "adcdb75d-4a63-451d-8b74-9bc9e4c5bb30",
        "SW2": "38c0b98a-bde4-451e-8fad-afb8991c8fa1",
        "SW3": "4d45a39d-4118-48fa-8fc4-1e96d7b72f68",
        "SW4": "a8f52c3b-6aab-4f6a-beb6-ba453bb48968",
        "J_HELMET": "c0000000-0000-0000-0000-0000000001C0",
        "H1": "f0000000-0000-0000-0000-0000000001d1",
        "H2": "f0000000-0000-0000-0000-0000000001d2",
        "H3": "f0000000-0000-0000-0000-0000000001d3",
        "H4": "f0000000-0000-0000-0000-0000000001d4",
    }

    lcsc_map = {
        "U1": "C5287747",
        "U2": "C96825",
        "U3": "C82942",
        "U4": "C365736",
        "U5": "C2686884",
        "ANT1": "C2909988",
        "J1": "C2836262",
        "D1": "C965555",
        "D2": "C7519",
        "BAT1": "C160402",
        "SW1": "C115357",
        "SW2": "C115357",
        "SW3": "C115357",
        "SW4": "C115357",
        "J_HELMET": "C136657",
    }

    value_map = {
        "SW1": "SW_1",
        "SW2": "SW_2",
        "SW3": "SW_3",
        "SW4": "SW_4",
        "U3": "XC6206P332MR"
    }

    print("Synchronizing footprint paths, values, LCSC fields...")
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        if ref in uuid_map:
            path_str = f"/{uuid_map[ref]}"
            kiid_path = pcbnew.KIID_PATH(path_str)
            fp.SetPath(kiid_path)
        if ref in lcsc_map:
            fp.SetField("LCSC", lcsc_map[ref])
        if ref in value_map:
            fp.SetValue(value_map[ref])

        # Text mirroring on back layer
        if fp.GetLayer() == pcbnew.B_Cu:
            fp.Reference().SetMirrored(True)
            fp.Value().SetMirrored(True)

    # 4. Clone exact J_HELMET footprint from OMM446
    print("Upgrading J_HELMET footprint to exact vertical BM06B-SRSS-TB on B.Cu...")
    old_j = board.FindFootprintByReference("J_HELMET")
    j446 = board446.FindFootprintByReference("J_HELMET")
    
    if old_j and j446:
        board.Remove(old_j)
        new_j = pcbnew.FOOTPRINT(j446)
        new_j.SetPosition(j446.GetPosition())
        new_j.SetOrientation(j446.GetOrientation())
        new_j.SetReference("J_HELMET")
        new_j.SetValue("HELMET_AUDIO_6P")
        new_j.SetPath(pcbnew.KIID_PATH("/c0000000-0000-0000-0000-0000000001C0"))
        new_j.SetField("LCSC", "C136657")
        
        # Assign pad nets
        j_pad_nets = {
            "1": "AUDIO_OUT_L",
            "2": "AUDIO_OUT_R",
            "3": "AGND_SPK",
            "4": "VOICE_IN",
            "5": "AGND_MIC",
            "6": "BTN_1",
            "MP": "GND"
        }
        for pad in new_j.Pads():
            pname = pad.GetPadName()
            if pname in j_pad_nets:
                pad.SetNet(net_map[j_pad_nets[pname]])
            
        new_j.Reference().SetMirrored(True)
        new_j.Value().SetMirrored(True)
        board.Add(new_j)
        print("✓ Placed exact J_HELMET footprint on B.Cu.")

    # 5. Fix pad net assignments on chips
    print("Fixing pad net assignments...")
    u4 = board.FindFootprintByReference("U4")
    if u4:
        for p in u4.Pads():
            pnum = p.GetPadName()
            if pnum == "20":
                p.SetNet(net_map["AGND_MIC"])
            elif pnum == "24":
                p.SetNet(net_map["AGND_SPK"])
            elif pnum in ["16", "17", "18"]:
                p.SetNet(net_map["AGND"])
            elif pnum in ["8", "10", "29"]:
                p.SetNet(net_map["GND"])

    d1 = board.FindFootprintByReference("D1")
    if d1:
        d1_pad_nets = {"1": "GND", "2": "VCC_3V3", "3": "GND", "4": "WS2812_DATA"}
        for p in d1.Pads():
            pnum = p.GetPadName()
            if pnum in d1_pad_nets:
                p.SetNet(net_map[d1_pad_nets[pnum]])

    j1 = board.FindFootprintByReference("J1")
    if j1:
        for p in j1.Pads():
            pname = p.GetPadName()
            if pname in ["A8", "B8"]:
                p.SetNet(board.FindNet(""))
            elif pname in ["A5", "B5"]:
                p.SetNet(net_map["GND"])

    u1 = board.FindFootprintByReference("U1")
    if u1:
        u1_pad_nets = {
            "21": "I2S_MCLK", "22": "I2S_BCLK", "23": "I2S_WS",
            "24": "I2S_DOUT", "25": "I2S_DIN",
            "26": "BT_UART_CTS", "27": "BT_UART_RTS",
            "28": "BT_UART_TX", "29": "BT_UART_RX"
        }
        for p in u1.Pads():
            pnum = p.GetPadName()
            if pnum in u1_pad_nets:
                p.SetNet(net_map[u1_pad_nets[pnum]])
            elif pnum.isdigit() and int(pnum) >= 40:
                p.SetNet(net_map["GND"])

    # 6. Delete dangling vias, track stubs, duplicate vias
    print("Purging dangling and duplicate tracks/vias...")
    vias_to_remove = [
        (99.8, 102.2),
        (92.15, 103.55),
        (102.45, 102.25),
        (91.70, 103.45),
        (117.6, 92.6), # duplicate of 117.7, 92.5
        (116.9, 92.6), # duplicate of 116.8, 92.5
    ]
    items_removed = 0
    tracks_to_del = []
    for t in board.GetTracks():
        p1 = (t.GetStart().x / 1e6, t.GetStart().y / 1e6)
        p2 = (t.GetEnd().x / 1e6, t.GetEnd().y / 1e6)
        
        # Check dangling track stub on GND_PLANE at (84.8, 87.5) -> (84.8, 87.9)
        if abs(p1[0] - 84.8) < 0.05 and abs(p1[1] - 87.5) < 0.05 and abs(p2[0] - 84.8) < 0.05 and abs(p2[1] - 87.9) < 0.05:
            tracks_to_del.append(t)
            continue

        if t.GetClass() == "PCB_VIA":
            vp = (t.GetPosition().x / 1e6, t.GetPosition().y / 1e6)
            for target in vias_to_remove:
                if abs(vp[0] - target[0]) < 0.08 and abs(vp[1] - target[1]) < 0.08:
                    tracks_to_del.append(t)
                    break

    for item in tracks_to_del:
        board.Remove(item)
        items_removed += 1
    print(f"✓ Removed {items_removed} dangling/duplicate vias & stubs.")

    # 7. Add internal solid planes (In1.Cu GND_PLANE and In2.Cu PWR_PLANE)
    print("Configuring internal planes from OMM446 templates...")
    has_gnd_plane = False
    has_pwr_plane = False
    for z in board.Zones():
        if z.GetLayer() == pcbnew.In1_Cu and z.GetNetname() == "GND":
            has_gnd_plane = True
        elif z.GetLayer() == pcbnew.In2_Cu and z.GetNetname() == "VCC_3V3":
            has_pwr_plane = True

    if not has_gnd_plane and len(board446.Zones()) >= 3:
        z2 = board446.Zones()[2]
        new_z2 = pcbnew.ZONE(z2)
        new_z2.SetNet(net_map["GND"])
        board.Add(new_z2)
        print("✓ Cloned In1.Cu GND_PLANE.")

    if not has_pwr_plane and len(board446.Zones()) >= 4:
        z3 = board446.Zones()[3]
        new_z3 = pcbnew.ZONE(z3)
        new_z3.SetNet(net_map["VCC_3V3"])
        new_z3.SetZoneName("PWR_PLANE")
        board.Add(new_z3)
        print("✓ Cloned In2.Cu PWR_PLANE (VCC_3V3).")

    # 8. Connect J1 GND pins (A5, B5)
    print("Routing J1 GND pins...")
    p_a5 = pcbnew.VECTOR2I(int(77.695 * 1e6), int(98.750 * 1e6))
    p_b5 = pcbnew.VECTOR2I(int(77.695 * 1e6), int(101.750 * 1e6))
    p_via = pcbnew.VECTOR2I(int(78.595 * 1e6), int(98.750 * 1e6))

    # Add GND via at (78.595, 98.75)
    via_j1 = pcbnew.PCB_VIA(board)
    via_j1.SetPosition(p_via)
    via_j1.SetNet(net_map["GND"])
    via_j1.SetWidth(int(0.6 * 1e6))
    via_j1.SetDrill(int(0.3 * 1e6))
    board.Add(via_j1)

    # Track A5 -> via
    t_a5 = pcbnew.PCB_TRACK(board)
    t_a5.SetStart(p_a5)
    t_a5.SetEnd(p_via)
    t_a5.SetWidth(int(0.25 * 1e6))
    t_a5.SetLayer(pcbnew.F_Cu)
    t_a5.SetNet(net_map["GND"])
    board.Add(t_a5)

    # Track B5 -> (78.595, 101.75) -> via
    p_b5_corner = pcbnew.VECTOR2I(int(78.595 * 1e6), int(101.750 * 1e6))
    t_b5a = pcbnew.PCB_TRACK(board)
    t_b5a.SetStart(p_b5)
    t_b5a.SetEnd(p_b5_corner)
    t_b5a.SetWidth(int(0.25 * 1e6))
    t_b5a.SetLayer(pcbnew.F_Cu)
    t_b5a.SetNet(net_map["GND"])
    board.Add(t_b5a)

    t_b5b = pcbnew.PCB_TRACK(board)
    t_b5b.SetStart(p_b5_corner)
    t_b5b.SetEnd(p_via)
    t_b5b.SetWidth(int(0.25 * 1e6))
    t_b5b.SetLayer(pcbnew.F_Cu)
    t_b5b.SetNet(net_map["GND"])
    board.Add(t_b5b)
    print("✓ Connected J1 pins A5 and B5 to GND via.")

    # 9. Connect D2 pad 2 (GND)
    print("Connecting D2 pad 2 to GND...")
    p_d2_2 = pcbnew.VECTOR2I(int(85.475 * 1e6), int(97.950 * 1e6))
    p_d2_via = pcbnew.VECTOR2I(int(84.6 * 1e6), int(97.950 * 1e6))
    via_d2 = pcbnew.PCB_VIA(board)
    via_d2.SetPosition(p_d2_via)
    via_d2.SetNet(net_map["GND"])
    via_d2.SetWidth(int(0.6 * 1e6))
    via_d2.SetDrill(int(0.3 * 1e6))
    board.Add(via_d2)

    t_d2 = pcbnew.PCB_TRACK(board)
    t_d2.SetStart(p_d2_2)
    t_d2.SetEnd(p_d2_via)
    t_d2.SetWidth(int(0.25 * 1e6))
    t_d2.SetLayer(pcbnew.F_Cu)
    t_d2.SetNet(net_map["GND"])
    board.Add(t_d2)
    print("✓ Connected D2 pad 2 to GND.")

    # 10. Connect U2 GND pins (1, 4, 12, 14, 17)
    print("Connecting U2 GND pins...")
    p_u2_ep = pcbnew.VECTOR2I(int(117.250 * 1e6), int(92.987 * 1e6))
    
    # Add 2 thermal vias inside U2 EP (116.8, 93.4) and (117.7, 93.4)
    for vx, vy in [(116.8, 93.4), (117.7, 93.4)]:
        v = pcbnew.PCB_VIA(board)
        v.SetPosition(pcbnew.VECTOR2I(int(vx * 1e6), int(vy * 1e6)))
        v.SetNet(net_map["GND"])
        v.SetWidth(int(0.6 * 1e6))
        v.SetDrill(int(0.3 * 1e6))
        board.Add(v)

    # Short tracks connecting U2 pads 1, 4, 12, 14 to EP
    u2_gnd_pads = [
        (118.737, 93.737), # pad 1
        (118.737, 92.237), # pad 4
        (115.763, 93.737), # pad 12
        (117.000, 94.475), # pad 14
    ]
    for px, py in u2_gnd_pads:
        t = pcbnew.PCB_TRACK(board)
        t.SetStart(pcbnew.VECTOR2I(int(px * 1e6), int(py * 1e6)))
        t.SetEnd(p_u2_ep)
        t.SetWidth(int(0.25 * 1e6))
        t.SetLayer(pcbnew.F_Cu)
        t.SetNet(net_map["GND"])
        board.Add(t)
    print("✓ Connected U2 GND pads to thermal vias and EP.")

    # 11. Refill all zones
    print("Refilling all copper zones...")
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    print("✓ Zone fill complete.")

    # 12. Save board
    board.Save(PCB_PATH)
    print("✓ Remediated OMM 2.4 board saved successfully.")

if __name__ == "__main__":
    remediate()
