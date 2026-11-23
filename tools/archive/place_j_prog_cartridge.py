#!/usr/bin/env python3
import sys
import pcbnew

def to_nm(mm):
    return int(mm * 1e6)

def main():
    pcb_path = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"
    board = pcbnew.LoadBoard(pcb_path)
    
    # 1. Remove any existing J_PROG footprint
    for fp in list(board.GetFootprints()):
        if fp.GetReference() == "J_PROG":
            board.Remove(fp)
            print("Removed old J_PROG")
            
    # 2. Load standard 1x04 1.27mm vertical SMD pin header
    fp = pcbnew.FootprintLoad("/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/Connector_PinHeader_1.27mm.pretty", "PinHeader_1x04_P1.27mm_Vertical_SMD_Pin1Left")
    if not fp:
        print("ERROR: Failed to load PinHeader_1x04_P1.27mm_Vertical_SMD_Pin1Left")
        sys.exit(1)
        
    fp.SetReference("J_PROG")
    fp.SetValue("SWD_PROG_4P")
    
    # Position on F.Cu (Top layer) at (126.50, 90.00) mm
    pos = pcbnew.VECTOR2I(to_nm(126.50), to_nm(90.00))
    fp.SetPosition(pos)
    fp.SetOrientationDegrees(0.0)
    
    # Replace the oversized generic courtyard with a tight standard IPC 0.25mm box
    for it in list(fp.GraphicalItems()):
        if it.GetLayer() == pcbnew.F_CrtYd:
            fp.Remove(it)
            
    pts = [
        (-3.25, -2.45),
        (3.25, -2.45),
        (3.25, 2.45),
        (-3.25, 2.45)
    ]
    for i in range(4):
        p1 = pts[i]
        p2 = pts[(i+1)%4]
        line = pcbnew.PCB_SHAPE(fp)
        line.SetShape(pcbnew.SHAPE_T_SEGMENT)
        line.SetLayer(pcbnew.F_CrtYd)
        line.SetStart(pcbnew.VECTOR2I(to_nm(p1[0]), to_nm(p1[1])))
        line.SetEnd(pcbnew.VECTOR2I(to_nm(p2[0]), to_nm(p2[1])))
        line.SetWidth(to_nm(0.05))
        fp.Add(line)
        
    # Net mapping
    net_map = {net.GetNetname(): net for net in board.GetNetsByName().values()}
    
    for pad in fp.Pads():
        num = pad.GetNumber()
        if num == "1":
            pad.SetNet(net_map["VCC_3V3"])
        elif num == "2":
            pad.SetNet(net_map["USB_DP"])
        elif num == "3":
            pad.SetNet(net_map["GND"])
        elif num == "4":
            pad.SetNet(net_map["USB_DN"])
            
    board.Add(fp)
    
    # Refill zones so GND zone pours cleanly around J_PROG on F.Cu
    zf = pcbnew.ZONE_FILLER(board)
    zf.Fill(board.Zones())
    
    board.Save(pcb_path)
    print("✓ Successfully placed and netted J_PROG on F.Cu at (126.50, 90.00) mm")

if __name__ == "__main__":
    main()
