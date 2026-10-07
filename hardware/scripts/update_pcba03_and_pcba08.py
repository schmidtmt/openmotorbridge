#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
Update PCBA 03 (Cartridge) and PCBA 08 (Radar Sub-MCU)
======================================================
1. PCBA 03 (openmotorbridge_pod_cartridge):
   - Replace 6-pin J2 (SM06B-SRSS-TB) with 8-pin J_AUDIO_PWR (SM08B-SRSS-TB) with Kelvin grounding.
   - Add J_PROG 4-pin SWD programming header (3V3, SWDIO, GND, NRST) for CH32V003F4P6.
2. PCBA 08 (openmotorbridge_radar_submcu):
   - Remove redundant U.FL antenna socket J3 (U.FL_5G9_V2X) as ESP32-C5 already has onboard U.FL.
   - Add J3 4-pin flash/programming header (3V3, TX, RX, GND) for ESP32-C5 UART flashing.
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

def update_cartridge_pcb():
    pcb_path = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"
    board = pcbnew.LoadBoard(pcb_path)
    print("Updating Cartridge PCB...")

    # Ensure required nets exist
    required_nets = ["PGND", "AGND_SPK", "AGND_MIC", "PD1_SWIO", "NRST", "VCC_5V_PROT", "POD_NF_P", "POD_NF_N", "MIC_IN+", "RESERVE_IO", "GND"]
    net_map = {}
    for netname in required_nets:
        net = board.FindNet(netname)
        if not net:
            net = pcbnew.NETINFO_ITEM(board, netname)
            board.Add(net)
        net_map[netname] = net

    # 1. Update J2 to 8-pin SM08B-SRSS-TB
    old_j2 = None
    for fp in board.GetFootprints():
        if fp.GetReference() in ["J2", "J_AUDIO_PWR"]:
            old_j2 = fp
            break

    j2_pos = pcbnew.VECTOR2I(to_nm(111.25), to_nm(87.75))
    j2_rot = 90.0
    if old_j2:
        j2_pos = old_j2.GetPosition()
        j2_rot = old_j2.GetOrientationDegrees()
        board.Remove(old_j2)
        print("✓ Removed old 6-pin J2")

    new_j2 = load_fp("Connector_JST.pretty", "JST_SH_SM08B-SRSS-TB_1x08-1MP_P1.00mm_Horizontal")
    if not new_j2:
        print("ERROR: Failed to load JST_SH_SM08B-SRSS-TB_1x08-1MP_P1.00mm_Horizontal")
        return False

    new_j2.SetReference("J_AUDIO_PWR")
    new_j2.SetValue("AUDIO_PWR_8P")
    new_j2.SetPosition(j2_pos)
    new_j2.SetOrientationDegrees(j2_rot)
    board.Add(new_j2)

    # Wire 8 pins of J_AUDIO_PWR:
    # Pin 1: PGND, Pin 2: VCC_5V_PROT, Pin 3: AGND_SPK, Pin 4: POD_NF_P,
    # Pin 5: POD_NF_N, Pin 6: AGND_MIC, Pin 7: MIC_IN+, Pin 8: RESERVE_IO
    pin_net_assignments = {
        "1": "PGND",
        "2": "VCC_5V_PROT",
        "3": "AGND_SPK",
        "4": "POD_NF_P",
        "5": "POD_NF_N",
        "6": "AGND_MIC",
        "7": "MIC_IN+",
        "8": "RESERVE_IO"
    }

    for pad in new_j2.Pads():
        num = pad.GetNumber()
        if num in pin_net_assignments:
            pad.SetNet(net_map[pin_net_assignments[num]])
        else:
            pad.SetNet(net_map["GND"]) # MP mounting tabs to GND
    print("✓ Placed and netted 8-pin J_AUDIO_PWR (SM08B-SRSS-TB)")

    # 2. Add J_PROG (4-Pin SWD programming header for CH32V003F4P6)
    # Check if J_PROG already exists
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
    # Position at (107.5, 72.0) on F.Cu (open space near U1)
    prog_pos = pcbnew.VECTOR2I(to_nm(107.5), to_nm(72.0))
    prog_fp.SetPosition(prog_pos)
    prog_fp.SetOrientationDegrees(0.0)
    board.Add(prog_fp)

    # Connect J_PROG pads:
    # Pin 1: VCC_5V_PROT (or 3V3 power rail), Pin 2: PD1_SWIO (SWDIO), Pin 3: GND, Pin 4: NRST
    for pad in prog_fp.Pads():
        num = pad.GetNumber()
        if num == "1":
            pad.SetNet(net_map["VCC_5V_PROT"])
        elif num == "2":
            pad.SetNet(net_map["PD1_SWIO"])
        elif num == "3":
            pad.SetNet(net_map["GND"])
        elif num == "4":
            pad.SetNet(net_map["NRST"])
    print("✓ Placed and netted J_PROG 4-pin SWD programming header")

    # Connect PD1_SWIO to Pad 18 of U1 (CH32V003) if needed
    for fp in board.GetFootprints():
        if fp.GetReference() == "U1":
            for pad in fp.Pads():
                if pad.GetNumber() == "18":
                    pad.SetNet(net_map["PD1_SWIO"])
                    print("✓ Assigned U1 pin 18 to PD1_SWIO")
                elif pad.GetNumber() == "4":
                    pad.SetNet(net_map["NRST"])
                    print("✓ Assigned U1 pin 4 to NRST")

    board.Save(pcb_path)
    print(f"✓ Saved {pcb_path}")
    return True

def update_radar_pcb():
    pcb_path = "hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb"
    board = pcbnew.LoadBoard(pcb_path)
    print("Updating Radar PCB...")

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

    j3_pos = pcbnew.VECTOR2I(to_nm(60.25), to_nm(72.78))
    if old_j3:
        j3_pos = old_j3.GetPosition()
        board.Remove(old_j3)
        print("✓ Removed redundant U.FL socket J3 (U.FL_5G9_V2X)")

    # 2. Add 4-pin 90° Flash/Debug Header J3 at the board edge
    # Footprint: PinHeader_1x04_P2.54mm_Horizontal
    new_j3 = load_fp("Connector_PinHeader_2.54mm.pretty", "PinHeader_1x04_P2.54mm_Horizontal")
    if not new_j3:
        # Fallback to JST-SH 1.0mm 4-pin horizontal if 2.54mm not found
        new_j3 = load_fp("Connector_JST.pretty", "JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal")

    if not new_j3:
        print("ERROR: Failed to load 4-pin programming header")
        return False

    new_j3.SetReference("J3")
    new_j3.SetValue("PROG_UART_4P")
    new_j3.SetPosition(j3_pos)
    board.Add(new_j3)
    new_j3.Flip(j3_pos, False) # Place on B.Cu matching U1

    # Connect J3 pads:
    # Pin 1: VCC_3V3, Pin 2: CENTRAL_TX (ESP32-C5 TX), Pin 3: CENTRAL_RX (ESP32-C5 RX), Pin 4: GND
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
        else:
            pad.SetNet(net_map["GND"])
    print("✓ Placed and netted J3 4-pin UART Flash/Debug header (3V3, TX, RX, GND)")

    board.Save(pcb_path)
    print(f"✓ Saved {pcb_path}")
    return True

if __name__ == "__main__":
    s1 = update_cartridge_pcb()
    s2 = update_radar_pcb()
    if s1 and s2:
        print("\n✅ Successfully updated both PCBA 03 and PCBA 08!")
    else:
        print("\n❌ Failed to update boards.")
        sys.exit(1)
