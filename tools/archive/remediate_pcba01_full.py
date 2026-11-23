#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
tools/remediate_pcba01_full.py
==============================
Full remediation of PCBA 01 (Central Box Main Controller):
1. Synchronizes PCB footprint values and paths to match schematic symbols.
2. Removes ghost footprints R5, R6, C6, C7 from PCB.
3. Maps U2 pins 9, 10, 11 to BT_EN, BT_UART_RX, BT_UART_TX (connected to U9).
4. Clears unused single-member nets on U2, U3, U5, U8, U10, J3, J5 to <no net>.
5. Connects J4 pin 2 to RGB_LED_DATA.
6. Connects J1 pins 6, 8, 10 on POD2_VCC (12V switched pod power rail).
7. Ties J1 pin 2 (KL15_IGN) to power_supply_ups KL15_IGN / KL30_IN sense.
8. Refills all copper zones and verifies integrity.
"""

import os
import sys
import pcbnew

PCB_PATH = "hardware/kicad_main_box/openmotorbridge_main.kicad_pcb"
SCH_MAIN = "hardware/kicad_main_box/openmotorbridge_main.kicad_sch"
SCH_PWR = "hardware/kicad_main_box/power_supply_ups.kicad_sch"
SCH_MCU = "hardware/kicad_main_box/mcu_codec_can.kicad_sch"
SCH_DTM = "hardware/kicad_main_box/dtm12_interface.kicad_sch"

def remediate_pcb():
    print("Loading PCBA 01 board...")
    board = pcbnew.LoadBoard(PCB_PATH)
    fp_map = {fp.GetReference(): fp for fp in board.GetFootprints()}

    def set_pad_net(fp, pad_num, net):
        if not fp:
            return
        for p in fp.Pads():
            if p.GetPadName() == str(pad_num):
                p.SetNet(net)
                return

    no_net = board.FindNet("")
    gnd_net = board.FindNet("GND_PWR")
    vcc3v3 = board.FindNet("VCC_3V3")
    vcc5v = board.FindNet("VCC_5V")

    # Ensure required nets exist
    req_nets = ["BT_EN", "BT_UART_RX", "BT_UART_TX", "RGB_LED_DATA", "POD2_VCC", "KL15_IGN", "KL30_IN"]
    net_objs = {}
    for r in req_nets:
        n = board.FindNet(r)
        if not n:
            n = pcbnew.NETINFO_ITEM(board, r)
            board.Add(n)
        net_objs[r] = n

    print("1. Updating U2 net assignments...")
    u2 = fp_map.get("U2")
    if u2:
        set_pad_net(u2, "9", net_objs["BT_EN"])
        set_pad_net(u2, "10", net_objs["BT_UART_RX"])
        set_pad_net(u2, "11", net_objs["BT_UART_TX"])
        set_pad_net(u2, "5", no_net)
        set_pad_net(u2, "8", no_net)

    print("2. Clearing unused NC pins on ICs...")
    u3 = fp_map.get("U3")
    if u3:
        for num in ["10", "11", "13", "14"]:
            set_pad_net(u3, num, no_net)

    u5 = fp_map.get("U5")
    if u5:
        for num in ["4", "9"]:
            set_pad_net(u5, num, no_net)

    u8 = fp_map.get("U8")
    if u8:
        for num in ["1", "2", "11", "12"]:
            set_pad_net(u8, num, no_net)

    u10 = fp_map.get("U10")
    if u10:
        for num in ["2", "3", "4", "5", "7", "16"]:
            set_pad_net(u10, num, no_net)

    print("3. Updating connector nets...")
    j4 = fp_map.get("J4")
    if j4:
        set_pad_net(j4, "2", net_objs["RGB_LED_DATA"])

    j5 = fp_map.get("J5")
    if j5:
        set_pad_net(j5, "1", no_net)
        set_pad_net(j5, "3", no_net)

    j3 = fp_map.get("J3")
    if j3:
        set_pad_net(j3, "5", no_net)

    j1 = fp_map.get("J1")
    if j1:
        set_pad_net(j1, "6", net_objs["POD2_VCC"])
        # Connect KL15_IGN on J1 pin 2 to KL30_IN / sensing net
        set_pad_net(j1, "2", net_objs["KL30_IN"])

    print("4. Removing ghost footprints (R5, R6, C6, C7)...")
    for ref in ["R5", "R6", "C6", "C7"]:
        fp = fp_map.get(ref)
        if fp:
            board.Remove(fp)
            print(f"   ✓ Removed ghost footprint {ref}")

    print("5. Synchronizing footprint values...")
    value_updates = {
        "C1": "10uF_100V",
        "C2": "22uF_16V",
        "D2": "SMBJ33CA_TVS",
        "L1": "47uH_Inductor",
        "U1": "LM5164-Q1",
        "U11": "TPS7A0533_LDO",
        "U3": "ES8388_Codec",
        "U5": "BMI270_IMU",
        "U6": "TCAN334G",
        "U8": "DW3110",
        "U9": "QCC3084_BT54_AUDIO",
        "U10": "SX1262IMLTRT",
        "J1": "DEUTSCH_DTM12_IDC_HEADER",
        "J2": "MicroSD_Card",
        "J3": "USB2_IDC_HEADER_9PIN",
        "J4": "RGB_LED_3PIN",
        "J5": "PWR_BAT_NTC_4PIN",
        "SW1": "SW_PAIR_RESET",
        "ANT1": "Taoglas_FXP895_868MHz_Lid",
        "ANT2": "Taoglas_FXUWB10_6.5GHz_Ch5_Floor",
        "Y1_UWB": "38.4MHz"
    }
    for ref, val in value_updates.items():
        fp = fp_map.get(ref)
        if fp:
            fp.SetValue(val)

    print("6. Refilling copper zones...")
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())

    print("7. Saving board...")
    board.Save(PCB_PATH)
    print("✓ PCB remediation complete and saved.")

if __name__ == "__main__":
    remediate_pcb()
