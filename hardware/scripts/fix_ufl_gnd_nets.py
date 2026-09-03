#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
import sys
import pcbnew

PCB_PATH = "/Users/schmidtm/openMotorBridge/hardware/kicad_rear_pod3/openmotorbridge_rear_pod3.kicad_pcb"

def fix_ufl():
    print(f"Loading board: {PCB_PATH}")
    board = pcbnew.LoadBoard(PCB_PATH)

    net_gnd = board.FindNet("GND")
    if not net_gnd:
        print("ERROR: GND net not found!")
        return

    net_lora = board.FindNet("LORA_RF_ANT")
    net_gnss = board.FindNet("GNSS_RF_IN")

    for fp in board.Footprints():
        ref = fp.GetReference()
        if ref == "J4":
            print(f"Found {ref}:")
            for pad in fp.Pads():
                num = pad.GetNumber()
                if num == "1":
                    if net_lora:
                        pad.SetNet(net_lora)
                    print(f"  Pad 1 set to net: {pad.GetNetname()}")
                elif num == "2":
                    pad.SetNet(net_gnd)
                    print(f"  Pad 2 set to net: {pad.GetNetname()}")
        elif ref == "J5":
            print(f"Found {ref}:")
            for pad in fp.Pads():
                num = pad.GetNumber()
                if num == "1":
                    if net_gnss:
                        pad.SetNet(net_gnss)
                    print(f"  Pad 1 set to net: {pad.GetNetname()}")
                elif num == "2":
                    pad.SetNet(net_gnd)
                    print(f"  Pad 2 set to net: {pad.GetNetname()}")

    board.BuildListOfNets()
    board.Save(PCB_PATH)
    print("Saved board with fixed GND nets on J4 & J5!")

if __name__ == "__main__":
    fix_ufl()
