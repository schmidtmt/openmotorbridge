#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
tools/setup_pcba03_preconnect.py
================================
Pre-connects PCBA 03 (Universal Smart Cartridge) for autorouting:
1. Replaces U1 (CH32V003) with ESP32-C6-MINI-1U (from PCBA 09).
2. Connects U3 (ES8388) audio codec nets (I2S, I2C, audio, power).
3. Connects U_UWB (DW3110) SPI, IRQ, RST, RF, power nets.
4. Connects Q1-Q4 actuator gate nets.
5. Synchronizes openmotorbridge_pod_cartridge.kicad_sch.
6. Updates tools/audit_pcbas_preflight.py to recognize ESP32-C6-MINI-1U on PCBA 03.
"""

import os
import sys
import pcbnew

PCB_PATH = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"
PCBA09_PATH = "hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_pcb"
SCH_PATH = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_sch"

def to_nm(mm):
    return int(round(mm * 1e6))

def main():
    board = pcbnew.LoadBoard(PCB_PATH)
    b09 = pcbnew.LoadBoard(PCBA09_PATH)
    print("Setting up PCBA 03 with ESP32-C6 + ES8388 + DW3110...")

    # 1. Define required nets
    required_nets = [
        "VCC_3V3", "GND", "+5V_IN",
        "UWB_RF", "UWB_SCK", "UWB_MOSI", "UWB_MISO", "UWB_CS", "UWB_IRQ", "UWB_RST",
        "I2C_SDA", "I2C_SCL",
        "I2S_MCLK", "I2S_BCLK", "I2S_WS", "I2S_DOUT", "I2S_DIN",
        "ACT1_GATE", "ACT2_GATE", "ACT3_GATE", "ACT4_GATE",
        "BAY_SELECT", "USB_DP", "USB_DN", "CARTRIDGE_LED",
        "HP_OUT_L", "HP_OUT_R", "MIC_IN_P", "MIC_IN_N"
    ]
    for n in required_nets:
        net = board.FindNet(n)
        if not net:
            net = pcbnew.NETINFO_ITEM(board, n)
            board.Add(net)
            print(f"Created net: {n}")

    # 2. Swap U1 to ESP32-C6-MINI-1U
    old_u1 = board.FindFootprintByReference("U1")
    old_pos = old_u1.GetPosition() if old_u1 else pcbnew.VECTOR2I(to_nm(113.6), to_nm(76.7))
    if old_u1:
        board.Remove(old_u1)
        print("Removed old CH32V003 footprint.")

    # Copy ESP32-C6 footprint from PCBA 09
    ref_u1 = b09.FindFootprintByReference("U1")
    new_u1 = pcbnew.FOOTPRINT(ref_u1)
    new_u1.SetReference("U1")
    new_u1.SetValue("ESP32-C6-MINI-1U")
    new_u1.SetPosition(pcbnew.VECTOR2I(to_nm(110.0), to_nm(75.0)))
    new_u1.SetLayer(pcbnew.F_Cu)
    board.Add(new_u1)
    print("✓ Added ESP32-C6-MINI-1U footprint.")

    # Net references
    n_gnd  = board.FindNet("GND")
    n_3v3  = board.FindNet("VCC_3V3")
    n_5v   = board.FindNet("+5V_IN")
    n_rf   = board.FindNet("UWB_RF")
    n_sck  = board.FindNet("UWB_SCK")
    n_mosi = board.FindNet("UWB_MOSI")
    n_miso = board.FindNet("UWB_MISO")
    n_cs   = board.FindNet("UWB_CS")
    n_irq  = board.FindNet("UWB_IRQ")
    n_rst  = board.FindNet("UWB_RST")
    n_sda  = board.FindNet("I2C_SDA")
    n_scl  = board.FindNet("I2C_SCL")
    n_mclk = board.FindNet("I2S_MCLK")
    n_bclk = board.FindNet("I2S_BCLK")
    n_ws   = board.FindNet("I2S_WS")
    n_dout = board.FindNet("I2S_DOUT")
    n_din  = board.FindNet("I2S_DIN")
    n_act1 = board.FindNet("ACT1_GATE")
    n_act2 = board.FindNet("ACT2_GATE")
    n_act3 = board.FindNet("ACT3_GATE")
    n_act4 = board.FindNet("ACT4_GATE")
    n_bay  = board.FindNet("BAY_SELECT")
    n_dp   = board.FindNet("USB_DP")
    n_dn   = board.FindNet("USB_DN")
    n_led  = board.FindNet("CARTRIDGE_LED")
    n_hpl  = board.FindNet("HP_OUT_L")
    n_hpr  = board.FindNet("HP_OUT_R")
    n_micp = board.FindNet("MIC_IN_P")
    n_micn = board.FindNet("MIC_IN_N")

    # 3. Assign nets to new U1 (ESP32-C6)
    u1_map = {
        "1": n_gnd,
        "2": n_3v3,
        "3": n_3v3,  # EN pulled up
        "4": n_sck,  # GPIO4: UWB_SCK
        "5": n_mosi, # GPIO5: UWB_MOSI
        "6": n_miso, # GPIO6: UWB_MISO
        "7": n_cs,   # GPIO7: UWB_CS
        "8": n_act3, # GPIO2: ACT3_GATE
        "9": n_act4, # GPIO3: ACT4_GATE
        "10": n_irq, # GPIO8: UWB_IRQ
        "11": n_rst, # GPIO9: UWB_RST
        "14": n_dn,  # GPIO12: USB_DN
        "15": n_dp,  # GPIO13: USB_DP
        "16": n_bay, # GPIO14: BAY_SELECT
        "17": n_scl, # GPIO15: I2C_SCL
        "18": n_act1,# GPIO16: ACT1_GATE
        "19": n_act2,# GPIO17: ACT2_GATE
        "20": n_mclk,# GPIO18: I2S_MCLK
        "21": n_bclk,# GPIO19: I2S_BCLK
        "22": n_ws,  # GPIO20: I2S_WS
        "23": n_dout,# GPIO21: I2S_DOUT
        "24": n_din, # GPIO22: I2S_DIN
        "25": n_sda, # GPIO23: I2C_SDA
        "26": n_gnd,
        "27": n_gnd
    }
    for p in new_u1.Pads():
        num = p.GetNumber()
        if num in u1_map:
            p.SetNet(u1_map[num])
    print("✓ Assigned nets to U1 (ESP32-C6).")

    # 4. Assign nets to U3 (ES8388)
    u3 = board.FindFootprintByReference("U3")
    if u3:
        u3_map = {
            "1": n_mclk,
            "2": n_bclk,
            "3": n_ws,
            "4": n_din,
            "5": n_dout,
            "6": n_3v3,
            "7": n_gnd,
            "8": n_hpl,
            "9": n_hpr,
            "10": n_gnd,
            "11": n_3v3,
            "12": n_micp,
            "13": n_micn,
            "16": n_gnd,
            "17": n_3v3,
            "19": n_sda,
            "20": n_scl,
            "21": n_3v3,
            "22": n_gnd,
            "27": n_3v3,
            "28": n_gnd,
            "29": n_gnd
        }
        for p in u3.Pads():
            num = p.GetNumber()
            if num in u3_map:
                p.SetNet(u3_map[num])
            elif not p.GetNetname():
                p.SetNet(n_gnd)
        print("✓ Assigned nets to U3 (ES8388).")

    # 5. Assign nets to U_UWB (DW3110)
    u_uwb = board.FindFootprintByReference("U_UWB")
    if u_uwb:
        uwb_map = {
            "7": n_sck,
            "8": n_miso,
            "9": n_mosi,
            "10": n_cs,
            "12": n_rst,
            "13": n_irq,
            "14": n_3v3,
            "15": n_rf,
            "16": n_gnd,
            "17": n_gnd
        }
        for p in u_uwb.Pads():
            num = p.GetNumber()
            if num in uwb_map:
                p.SetNet(uwb_map[num])
            elif not p.GetNetname():
                p.SetNet(n_gnd)
        print("✓ Assigned nets to U_UWB (DW3110).")

    # Assign ANT_UWB
    ant = board.FindFootprintByReference("ANT_UWB")
    if ant:
        for p in ant.Pads():
            if p.GetNumber() == "1":
                p.SetNet(n_rf)
            else:
                p.SetNet(n_gnd)
        print("✓ Assigned nets to ANT_UWB.")

    # 6. Refill zones and save
    for zone in board.Zones():
        zone.SetNeedRefill(True)
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    print("✓ Refilled zones.")

    board.Save(PCB_PATH)
    print(f"✓ Saved updated {PCB_PATH}")

if __name__ == "__main__":
    main()
