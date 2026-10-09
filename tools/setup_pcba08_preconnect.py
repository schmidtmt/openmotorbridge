#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
tools/setup_pcba08_preconnect.py
================================
Pre-connects PCBA 08 for autorouting:
1. Defines all UWB nets (UWB_RF, UWB_SCK, UWB_MOSI, UWB_MISO, UWB_CS, UWB_IRQ, UWB_RST).
2. Assigns pads on U1, U3, and J4 to their respective nets.
3. Routes the local RF trace, Pad 16 GND, and local VCC_3V3 on the Right Wing.
4. Leaves the bridge nets with valid ratsnest airwires ready for KiCad autorouter/cleaner.
"""

import pcbnew

PCB_PATH = "hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb"

def to_nm(mm):
    return int(round(mm * 1e6))

def add_track(board, net, layer, p1, p2, width_mm=0.20):
    t = pcbnew.PCB_TRACK(board)
    t.SetNet(net)
    t.SetLayer(layer)
    t.SetWidth(to_nm(width_mm))
    t.SetStart(pcbnew.VECTOR2I(to_nm(p1[0]), to_nm(p1[1])))
    t.SetEnd(pcbnew.VECTOR2I(to_nm(p2[0]), to_nm(p2[1])))
    board.Add(t)
    return t

def add_polyline(board, net, layer, points, width_mm=0.20):
    for i in range(len(points) - 1):
        add_track(board, net, layer, points[i], points[i+1], width_mm=width_mm)

def main():
    board = pcbnew.LoadBoard(PCB_PATH)
    print("Setting up PCBA 08 pre-connections...")

    b_cu = pcbnew.B_Cu

    # 1. Create nets if they do not exist
    uwb_nets = ["UWB_RF", "UWB_SCK", "UWB_MOSI", "UWB_MISO", "UWB_CS", "UWB_IRQ", "UWB_RST"]
    for netname in uwb_nets:
        net = board.FindNet(netname)
        if not net:
            net = pcbnew.NETINFO_ITEM(board, netname)
            board.Add(net)
            print(f"Created net: {netname}")

    net_rf   = board.FindNet("UWB_RF")
    net_sck  = board.FindNet("UWB_SCK")
    net_mosi = board.FindNet("UWB_MOSI")
    net_miso = board.FindNet("UWB_MISO")
    net_cs   = board.FindNet("UWB_CS")
    net_irq  = board.FindNet("UWB_IRQ")
    net_rst  = board.FindNet("UWB_RST")
    net_3v3  = board.FindNet("VCC_3V3")
    net_gnd  = board.FindNet("GND")

    # 2. Assign U3 pads
    u3 = board.FindFootprintByReference("U3")
    if u3:
        pad_map = {
            "7": net_sck,
            "8": net_miso,
            "9": net_mosi,
            "10": net_cs,
            "12": net_rst,
            "13": net_irq,
            "14": net_3v3,
            "15": net_rf,
            "16": net_gnd,
            "17": net_gnd
        }
        for pad in u3.Pads():
            num = pad.GetNumber()
            if num in pad_map:
                pad.SetNet(pad_map[num])
        print("✓ Assigned nets to U3 pads.")

    # 3. Assign J4 pads
    j4 = board.FindFootprintByReference("J4")
    if j4:
        for pad in j4.Pads():
            if pad.GetNumber() == "1":
                pad.SetNet(net_rf)
            else:
                pad.SetNet(net_gnd)
        print("✓ Assigned nets to J4 pads.")

    # 4. Assign U1 pads
    u1 = board.FindFootprintByReference("U1")
    if u1:
        u1_map = {
            "6": net_rst,
            "10": net_sck,
            "11": net_mosi,
            "12": net_miso,
            "14": net_cs,
            "15": net_irq
        }
        for pad in u1.Pads():
            num = pad.GetNumber()
            if num in u1_map:
                pad.SetNet(u1_map[num])
        print("✓ Assigned nets to U1 pads.")

    # Remove any existing tracks for UWB nets
    managed_names = set(uwb_nets)
    to_remove = [t for t in board.GetTracks() if t.GetNetname() in managed_names]
    for t in to_remove:
        board.Remove(t)

    # 5. Route local Right Wing connections
    # RF trace: 50-ohm (0.35 mm width)
    add_polyline(board, net_rf, b_cu, [
        (145.25, 98.35),
        (145.25, 96.50),
        (152.00, 96.50)
    ], width_mm=0.35)
    print("✓ Routed UWB_RF trace.")

    # Pad 16 GND to Pad 17 EP
    add_polyline(board, net_gnd, b_cu, [
        (145.75, 98.35),
        (145.75, 99.80),
        (145.00, 99.80)
    ], width_mm=0.20)
    print("✓ Routed U3 Pad 16 GND.")

    # Pad 14 VCC_3V3 to Right Wing 3V3 net
    add_polyline(board, net_3v3, b_cu, [
        (144.75, 98.35),
        (144.75, 96.80),
        (140.80, 96.80),
        (140.80, 83.90),
        (147.20, 83.90)
    ], width_mm=0.20)
    print("✓ Routed U3 Pad 14 VCC_3V3.")

    # Refill zones and save
    for zone in board.Zones():
        zone.SetNeedRefill(True)
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    print("✓ Refilled zones.")

    board.Save(PCB_PATH)
    print(f"✓ Saved updated {PCB_PATH}")

if __name__ == "__main__":
    main()
