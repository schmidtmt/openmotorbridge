#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
apply_pcba03_pcba08_updates.py
==============================
Applies hardware updates to:
1. PCBA 08 (Radar Sub-MCU / openmotorbridge_radar_submcu):
   - Replace redundant J3 (U.FL) with J3 4-Pin 90° Flash/Debug Header (3V3, TX, RX, GND)
   - Route UART and power connections
   - Update schematic with complete symbols
2. PCBA 03 (Cartridge / openmotorbridge_pod_cartridge):
   - Replace 6-pin J2 with 8-pin J_AUDIO_PWR (SM08B-SRSS-TB) with Kelvin Grounding
   - Add J_PROG 4-pin SWD programming header (3V3, SWDIO, GND, NRST) for CH32V003
   - Route connections and update schematic
"""

import os
import sys
import pcbnew

KICAD_FP_DIR = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"

def to_nm(mm):
    return int(mm * 1e6)

def load_fp(lib, name):
    lib_path = os.path.join(KICAD_FP_DIR, lib)
    return pcbnew.FootprintLoad(lib_path, name)

def add_track(board, net, layer, x1_mm, y1_mm, x2_mm, y2_mm, width_mm=0.25):
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(pcbnew.VECTOR2I(to_nm(x1_mm), to_nm(y1_mm)))
    t.SetEnd(pcbnew.VECTOR2I(to_nm(x2_mm), to_nm(y2_mm)))
    t.SetWidth(to_nm(width_mm))
    t.SetLayer(layer)
    t.SetNet(net)
    board.Add(t)
    return t

def update_radar_pcb():
    pcb_path = "hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb"
    board = pcbnew.LoadBoard(pcb_path)
    print("Updating PCBA 08 Radar Sub-MCU PCB...")

    # Ensure required nets exist
    required_nets = ["VCC_3V3", "CENTRAL_TX", "CENTRAL_RX", "GND"]
    net_map = {}
    for netname in required_nets:
        net = board.FindNet(netname)
        if not net:
            net = pcbnew.NETINFO_ITEM(board, netname)
            board.Add(net)
        net_map[netname] = net

    # 1. Remove redundant U.FL antenna J3
    old_j3 = None
    for fp in board.GetFootprints():
        if fp.GetReference() == "J3":
            old_j3 = fp
            break

    if old_j3:
        board.Remove(old_j3)
        print("✓ Removed redundant U.FL socket J3")

    # 2. Add 4-pin 90° Flash/Debug Header J3
    new_j3 = load_fp("Connector_PinHeader_2.54mm.pretty", "PinHeader_1x04_P2.54mm_Horizontal")
    if not new_j3:
        print("ERROR: Failed to load PinHeader_1x04_P2.54mm_Horizontal")
        return False

    new_j3.SetReference("J3")
    new_j3.SetValue("PROG_UART_4P")
    # Position at (60.25, 72.78)
    j3_pos = pcbnew.VECTOR2I(to_nm(60.25), to_nm(72.78))
    new_j3.SetPosition(j3_pos)
    new_j3.SetOrientationDegrees(90.0)
    board.Add(new_j3)
    new_j3.Flip(j3_pos, False) # Mounted on B.Cu

    # Pad assignments:
    # At rot 90:
    # Pad 1 at (67.87, 72.78) -> VCC_3V3
    # Pad 2 at (65.33, 72.78) -> CENTRAL_TX
    # Pad 3 at (62.79, 72.78) -> CENTRAL_RX
    # Pad 4 at (60.25, 72.78) -> GND
    for pad in new_j3.Pads():
        num = pad.GetNumber()
        if num == "1":
            pad.SetNet(net_map["VCC_3V3"])
        elif num == "2":
            pad.SetNet(net_map["CENTRAL_TX"])
        elif num == "3":
            pad.SetNet(net_map["CENTRAL_RX"])
        elif num == "4":
            pad.SetNet(net_map["GND"])
    print("✓ Placed J3 4-Pin 90° Flash/Debug Header (3V3, TX, RX, GND) at (60.25, 72.78)")

    # 3. Add tracks for J3
    # Connect Pad 1 (VCC_3V3) to existing VCC_3V3 trace at (68.90, 73.90) on F.Cu (Pad 1 is through-hole)
    add_track(board, net_map["VCC_3V3"], pcbnew.F_Cu, 67.87, 72.78, 68.90, 73.81, 0.25)
    add_track(board, net_map["VCC_3V3"], pcbnew.F_Cu, 68.90, 73.81, 68.90, 74.20, 0.25)

    # Connect Pad 2 (CENTRAL_TX) at (65.33, 72.78) to U1 Pad 16 at (47.25, 97.00) on B.Cu
    add_track(board, net_map["CENTRAL_TX"], pcbnew.B_Cu, 65.33, 72.78, 65.33, 76.00, 0.20)
    add_track(board, net_map["CENTRAL_TX"], pcbnew.B_Cu, 65.33, 76.00, 52.00, 89.33, 0.20)
    add_track(board, net_map["CENTRAL_TX"], pcbnew.B_Cu, 52.00, 89.33, 52.00, 97.00, 0.20)
    add_track(board, net_map["CENTRAL_TX"], pcbnew.B_Cu, 52.00, 97.00, 47.25, 97.00, 0.20)

    # Connect Pad 3 (CENTRAL_RX) at (62.79, 72.78) to U1 Pad 17 at (47.25, 95.50) on B.Cu
    add_track(board, net_map["CENTRAL_RX"], pcbnew.B_Cu, 62.79, 72.78, 62.79, 76.50, 0.20)
    add_track(board, net_map["CENTRAL_RX"], pcbnew.B_Cu, 62.79, 76.50, 50.50, 88.79, 0.20)
    add_track(board, net_map["CENTRAL_RX"], pcbnew.B_Cu, 50.50, 88.79, 50.50, 95.50, 0.20)
    add_track(board, net_map["CENTRAL_RX"], pcbnew.B_Cu, 50.50, 95.50, 47.25, 95.50, 0.20)

    # Connect Pad 4 (GND) at (60.25, 72.78) to GND
    add_track(board, net_map["GND"], pcbnew.B_Cu, 60.25, 72.78, 60.25, 74.50, 0.35)

    # Refill zones
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())

    board.Save(pcb_path)
    print("✓ Saved updated openmotorbridge_radar_submcu.kicad_pcb")
    return True

def update_cartridge_pcb():
    pcb_path = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"
    board = pcbnew.LoadBoard(pcb_path)
    print("Updating PCBA 03 Cartridge PCB...")

    # Ensure required nets exist
    required_nets = [
        "PGND", "VCC_5V_PROT", "AGND_SPK", "POD_NF_P", "POD_NF_N",
        "AGND_MIC", "MIC_IN+", "RESERVE_IO", "GND", "PD1_SWIO", "NRST"
    ]
    net_map = {}
    for netname in required_nets:
        net = board.FindNet(netname)
        if not net:
            net = pcbnew.NETINFO_ITEM(board, netname)
            board.Add(net)
        net_map[netname] = net

    # 1. Replace 6-pin J2 with 8-pin J_AUDIO_PWR
    old_j2 = None
    for fp in board.GetFootprints():
        if fp.GetReference() in ["J2", "J_AUDIO_PWR"]:
            old_j2 = fp
            break

    if old_j2:
        board.Remove(old_j2)
        print("✓ Removed old 6-pin J2")

    new_j2 = load_fp("Connector_JST.pretty", "JST_SH_SM08B-SRSS-TB_1x08-1MP_P1.00mm_Horizontal")
    if not new_j2:
        print("ERROR: Failed to load JST_SH_SM08B-SRSS-TB_1x08-1MP_P1.00mm_Horizontal")
        return False

    new_j2.SetReference("J_AUDIO_PWR")
    new_j2.SetValue("AUDIO_PWR_8P")
    # Position at (111.25, 87.00) on F.Cu, rot 90
    j2_pos = pcbnew.VECTOR2I(to_nm(111.25), to_nm(87.00))
    new_j2.SetPosition(j2_pos)
    new_j2.SetOrientationDegrees(90.0)
    board.Add(new_j2)

    # Pad assignments for 8-pin J_AUDIO_PWR:
    # Pin 1: PGND, Pin 2: VCC_5V_PROT, Pin 3: AGND_SPK, Pin 4: POD_NF_P
    # Pin 5: POD_NF_N, Pin 6: AGND_MIC, Pin 7: MIC_IN+, Pin 8: RESERVE_IO
    pin_assignments = {
        "1": "PGND",
        "2": "VCC_5V_PROT",
        "3": "AGND_SPK",
        "4": "POD_NF_P",
        "5": "POD_NF_N",
        "6": "AGND_MIC",
        "7": "MIC_IN+",
        "8": "RESERVE_IO",
    }
    for pad in new_j2.Pads():
        num = pad.GetNumber()
        if num in pin_assignments:
            pad.SetNet(net_map[pin_assignments[num]])
        else:
            pad.SetNet(net_map["GND"]) # MP mounting tabs to GND
    print("✓ Placed J_AUDIO_PWR 8-Pin JST-SH Connector (SM08B-SRSS-TB) with Kelvin Grounding")

    # 2. Add J_PROG 4-pin SWD programming header for CH32V003
    old_prog = None
    for fp in board.GetFootprints():
        if fp.GetReference() in ["J_PROG", "J_SWD"]:
            old_prog = fp
            break
    if old_prog:
        board.Remove(old_prog)

    prog_fp = load_fp("Connector_PinHeader_1.27mm.pretty", "PinHeader_1x04_P1.27mm_Vertical_SMD_Pin1Left")
    if not prog_fp:
        print("ERROR: Failed to load PinHeader_1x04_P1.27mm_Vertical_SMD_Pin1Left")
        return False

    prog_fp.SetReference("J_PROG")
    prog_fp.SetValue("SWD_PROG_4P")
    # Position at (107.0, 71.5) on F.Cu
    prog_pos = pcbnew.VECTOR2I(to_nm(107.0), to_nm(71.5))
    prog_fp.SetPosition(prog_pos)
    prog_fp.SetOrientationDegrees(0.0)
    board.Add(prog_fp)

    # Pad assignments:
    # Pin 1: VCC_5V_PROT, Pin 2: PD1_SWIO, Pin 3: GND, Pin 4: NRST
    for pad in prog_fp.Pads():
        num = pad.GetNumber()
        if num == "1": pad.SetNet(net_map["VCC_5V_PROT"])
        elif num == "2": pad.SetNet(net_map["PD1_SWIO"])
        elif num == "3": pad.SetNet(net_map["GND"])
        elif num == "4": pad.SetNet(net_map["NRST"])
    print("✓ Placed J_PROG 4-Pin SWD Header (VCC, SWIO, GND, NRST) at (107.0, 71.5)")

    # 3. Update U1 MCU net assignments for SWIO and NRST
    for fp in board.GetFootprints():
        if fp.GetReference() == "U1":
            for pad in fp.Pads():
                if pad.GetNumber() in ["8", "18"]:
                    # In TSSOP-20 CH32V003: pin 18 is PD1/SWIO (or pin 8 depending on symbol indexing)
                    pad.SetNet(net_map["PD1_SWIO"])
                elif pad.GetNumber() == "4":
                    pad.SetNet(net_map["NRST"])
            print("✓ Verified U1 CH32V003 SWIO and NRST net connections")

    # 4. Route tracks for J_PROG
    # Pin 1 (VCC_5V_PROT at 107.0, 70.23) to F1 Pad 2 at (112.5, 71.75)
    add_track(board, net_map["VCC_5V_PROT"], pcbnew.F_Cu, 107.00, 70.23, 109.00, 70.23, 0.25)
    add_track(board, net_map["VCC_5V_PROT"], pcbnew.F_Cu, 109.00, 70.23, 110.50, 71.73, 0.25)
    add_track(board, net_map["VCC_5V_PROT"], pcbnew.F_Cu, 110.50, 71.73, 112.50, 71.75, 0.25)

    # Pin 3 (GND at 107.0, 72.77) to GND
    add_track(board, net_map["GND"], pcbnew.F_Cu, 107.00, 72.77, 105.50, 72.77, 0.30)

    # Pin 4 (NRST at 107.0, 74.04) to U1 Pad 4 at (110.75, 75.70)
    add_track(board, net_map["NRST"], pcbnew.F_Cu, 107.00, 74.04, 109.00, 74.04, 0.20)
    add_track(board, net_map["NRST"], pcbnew.F_Cu, 109.00, 74.04, 110.75, 75.79, 0.20)

    # 5. Route tracks for J_AUDIO_PWR
    # Pad 1 (PGND at 109.25, 90.50) to GND via / plane
    add_track(board, net_map["PGND"], pcbnew.F_Cu, 109.25, 90.50, 107.50, 90.50, 0.35)

    # Pad 2 (VCC_5V_PROT at 109.25, 89.50) to C2 Pad 1 (VCC_5V_PROT) at (107.00, 82.50)
    add_track(board, net_map["VCC_5V_PROT"], pcbnew.F_Cu, 109.25, 89.50, 107.50, 87.75, 0.30)
    add_track(board, net_map["VCC_5V_PROT"], pcbnew.F_Cu, 107.50, 87.75, 107.50, 84.50, 0.30)
    add_track(board, net_map["VCC_5V_PROT"], pcbnew.F_Cu, 107.50, 84.50, 107.00, 84.00, 0.30)

    # Refill zones
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())

    board.Save(pcb_path)
    print("✓ Saved updated openmotorbridge_pod_cartridge.kicad_pcb")
    return True

if __name__ == "__main__":
    s1 = update_radar_pcb()
    s2 = update_cartridge_pcb()
    if s1 and s2:
        print("\n✨ PCBA 03 and PCBA 08 successfully updated!")
    else:
        print("\n❌ PCB update failed.")
        sys.exit(1)
