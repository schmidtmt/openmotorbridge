#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
tools/update_front_node_pcb.py
==============================
Applies PCBA 05 (Front-Node) updates to PCB:
1. Migrates J7, J10, J8 to SMD JST-GH 2-pin (SM02B-GHS-TB) collinear at Y=73.35mm.
   - J7 at X=156.68, Y=73.35, rot=180
   - J10 at X=164.87, Y=73.35, rot=180
   - J8 at X=172.00, Y=73.35, rot=180 (clears H2 courtyard with 0.8mm margin)
2. Migrates J9, J11 to SMD JST-GH 4-pin (SM04B-GHS-TB) at Y=116.50mm, aligning South pitch to 12.76mm.
   - J11 at X=132.49, Y=116.50, rot=0
   - J9 at X=158.01, Y=116.50, rot=0
3. Rewires USB nets:
   - J1 pins 3&4 <-> U1 pins 55&54 (USB_HS_DP / USB_HS_DM)
   - J4 pins 7&8 <-> U2 pins 21&20 (USB_HOST_EXT_DP / USB_HOST_EXT_DM)
   - U2 pins 2&1 <-> J5 pins 3&4 (USB_DN1_DP / USB_DN1_DM)
   - U2 pins 4&3 <-> U10 pins 19&18 (USB_DN2_DP / USB_DN2_DM)
4. Adds U10 (ESP32-C3FH4) + Y2 (40MHz) + passives on B.Cu in pristine vacant area next to Y1 (X=153.0, Y=98.0).
5. Cleans old intersecting traces for rewired nets and shifted connectors.
6. Refills zones.
"""

import sys
import os
import pcbnew

PCB_PATH = "hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb"
FP_BASE = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"

def to_nm(mm):
    return int(mm * 1e6)

def to_mm(nm):
    return float(nm) / 1e6

def get_or_create_net(board, netname):
    if not netname:
        return None
    netinfo = board.GetNetInfo()
    net = netinfo.GetNetItem(netname)
    if not net:
        net = pcbnew.NETINFO_ITEM(board, netname)
        board.Add(net)
    return net

def set_pad_net(board, pad, netname):
    net = get_or_create_net(board, netname)
    if net:
        pad.SetNet(net)

def main():
    print("=== Updating PCBA 05 PCB ===")
    board = pcbnew.LoadBoard(PCB_PATH)
    b_cu_id = board.GetLayerID("B.Cu")

    # Symbol UUIDs extracted from openmotorbridge_front_node.kicad_sch
    uuids = {
        "J7": "0d7ffad6-b8b4-4e17-a294-c7abf6a85b74",
        "J8": "6ffd8952-3b5b-4804-96b5-4ae274f3ef4f",
        "J10": "e91341d0-ead9-4eba-827e-ff0655beba8e",
        "J9": "9cb917e5-d4b5-4ddf-8f00-7c6d7652b9c4",
        "J11": "33fb97d5-ed0a-4680-bbf7-cce8b5180f54",
        "U10": "f5560a8b-cd8f-4cea-ace3-6ee6986fd4a5",
        "Y2": "72f86c92-012b-4ae5-bc83-5edf2f35c8d2",
        "C27": "107d1023-ba2d-43d3-88a1-4697a3f7e25a",
        "C28": "18be5be1-a07d-4899-b742-2075d67088f4",
        "C29": "b1409fab-f0df-44c0-8010-3e8097b25e20",
        "C30": "9e023982-56ac-45a8-8389-e48e0deb5e31",
        "C31": "62fac156-444f-44cb-8a43-3ddb843eaf3d",
        "R17": "44cbaf6b-9259-4fc8-a0cf-a08a88941b4f",
        "R18": "b221503b-002f-4039-b3ce-2c5923095c9c",
    }

    # 1. Clean up old rewired / dead tracks and connector stubs
    nets_to_clean = {
        "USB_UP_DP", "USB_UP_DM", "USB_DN1_DP", "USB_DN1_DM",
        "USB_DN2_DP", "USB_DN2_DM", "USB_DN3_DP", "USB_DN3_DM"
    }
    tracks_to_delete = []
    for t in board.GetTracks():
        if t.GetNetname() in nets_to_clean:
            tracks_to_delete.append(t)

    # Clean old tracks touching J7, J8, J10, J9, J11 regions
    for t in board.GetTracks():
        if isinstance(t, pcbnew.PCB_VIA):
            continue
        s, e = t.GetStart(), t.GetEnd()
        sx, sy, ex, ey = to_mm(s.x), to_mm(s.y), to_mm(e.x), to_mm(e.y)
        # Check North connector corridor (J7, J10, J8)
        if (153.0 <= sx <= 176.0 and 71.0 <= sy <= 79.0) or (153.0 <= ex <= 176.0 and 71.0 <= ey <= 79.0):
            if t.GetNetname() in {"+12V_AUX", "+12V_PROT", "VCC_5V", "AUX_LIGHT_EN", "GND"}:
                if t not in tracks_to_delete:
                    tracks_to_delete.append(t)
        # Check South connector corridor (J11 at X~132.5, J9 at X~158)
        if (124.0 <= sx <= 138.0 and 113.0 <= sy <= 119.0) or (124.0 <= ex <= 138.0 and 113.0 <= ey <= 119.0):
            if t.GetNetname() in {"VCC_3V3", "GND", "I2C_SCL", "I2C_SDA", "GNSS_TXD"}:
                if t not in tracks_to_delete:
                    tracks_to_delete.append(t)
        if (154.0 <= sx <= 163.0 and 113.0 <= sy <= 119.0) or (154.0 <= ex <= 163.0 and 113.0 <= ey <= 119.0):
            if t.GetNetname() in {"VCC_3V3", "GND", "I2C_SCL", "I2C_SDA"}:
                if t not in tracks_to_delete:
                    tracks_to_delete.append(t)

    for t in tracks_to_delete:
        board.Delete(t)
    print(f"Removed {len(tracks_to_delete)} old tracks for rewired USB nets and shifted connectors.")

    # 2. Remove old footprints J7, J8, J10, J9, J11 and any previous U10 subsystem
    for ref in ["J7", "J8", "J10", "J9", "J11", "U10", "Y2", "C27", "C28", "C29", "C30", "C31", "R17", "R18"]:
        f = board.FindFootprintByReference(ref)
        if f:
            board.Delete(f)
            print(f"Deleted old/previous footprint {ref}")

    # 3. Add new JST-GH Connectors
    fp_gh = os.path.join(FP_BASE, "Connector_JST.pretty")

    def add_gh02(ref, val, x, y, rot, net_p1, net_p2, uuid_str):
        f = pcbnew.FootprintLoad(fp_gh, "JST_GH_SM02B-GHS-TB_1x02-1MP_P1.25mm_Horizontal")
        f.SetReference(ref)
        f.SetValue(val)
        f.SetPosition(pcbnew.VECTOR2I(to_nm(x), to_nm(y)))
        f.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
        f.SetPath(pcbnew.KIID_PATH(f"/{uuid_str}"))
        for p in f.Pads():
            name = p.GetName()
            if name == "1": set_pad_net(board, p, net_p1)
            elif name == "2": set_pad_net(board, p, net_p2)
            elif name == "MP": set_pad_net(board, p, "GND")
        board.Add(f)
        print(f"Added {ref} ({val}) at ({x}, {y}) rot={rot}")
        return f

    def add_gh04(ref, val, x, y, rot, p1_net, p2_net, p3_net, p4_net, uuid_str):
        f = pcbnew.FootprintLoad(fp_gh, "JST_GH_SM04B-GHS-TB_1x04-1MP_P1.25mm_Horizontal")
        f.SetReference(ref)
        f.SetValue(val)
        f.SetPosition(pcbnew.VECTOR2I(to_nm(x), to_nm(y)))
        f.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
        f.SetPath(pcbnew.KIID_PATH(f"/{uuid_str}"))
        for p in f.Pads():
            name = p.GetName()
            if name == "1": set_pad_net(board, p, p1_net)
            elif name == "2": set_pad_net(board, p, p2_net)
            elif name == "3": set_pad_net(board, p, p3_net)
            elif name == "4": set_pad_net(board, p, p4_net)
            elif name == "MP": set_pad_net(board, p, "GND")
        board.Add(f)
        print(f"Added {ref} ({val}) at ({x}, {y}) rot={rot}")
        return f

    # Place North connectors (collinear at Y=73.35mm, J8 at X=172.00 clears H2 courtyard)
    add_gh02("J7", "AUX_LIGHT_12V", 156.68, 73.35, 180.0, "+12V_AUX", "GND", uuids["J7"])
    add_gh02("J10", "NAVI_12V", 164.87, 73.35, 180.0, "+12V_PROT", "GND", uuids["J10"])
    add_gh02("J8", "CAM_5V", 172.00, 73.35, 180.0, "VCC_5V", "GND", uuids["J8"])

    # Place South connectors (equidistant 12.76mm pitch: 119.73, 132.49, 145.25, 158.01, 170.77)
    add_gh04("J11", "DISP_RIGHT", 132.49, 116.50, 0.0, "VCC_3V3", "GND", "I2C_SCL", "I2C_SDA", uuids["J11"])
    add_gh04("J9", "DISP_LEFT", 158.01, 116.50, 0.0, "VCC_3V3", "GND", "I2C_SCL", "I2C_SDA", uuids["J9"])

    # 4. Update Net mappings on existing ICs and Connectors
    # J1 (pins 3 & 4)
    j1 = board.FindFootprintByReference("J1")
    if j1:
        for p in j1.Pads():
            if p.GetName() == "3": set_pad_net(board, p, "USB_HS_DP")
            elif p.GetName() == "4": set_pad_net(board, p, "USB_HS_DM")
        print("Updated J1 nets -> USB_HS_DP / USB_HS_DM")

    # U1 (ESP32-S31)
    u1 = board.FindFootprintByReference("U1")
    if u1:
        for p in u1.Pads():
            if p.GetName() == "13": set_pad_net(board, p, "C3_UART_RX")
            elif p.GetName() == "14": set_pad_net(board, p, "C3_UART_TX")
            elif p.GetName() == "15": set_pad_net(board, p, "C3_EN")
            elif p.GetName() == "16": set_pad_net(board, p, "C3_BOOT")
            elif p.GetName() == "54": set_pad_net(board, p, "USB_HS_DM")
            elif p.GetName() == "55": set_pad_net(board, p, "USB_HS_DP")
        print("Updated U1 nets -> C3_UART_RX, C3_UART_TX, C3_EN, C3_BOOT, USB_HS_DM, USB_HS_DP")

    # J4 (HUB_EXT pins 7 & 8)
    j4 = board.FindFootprintByReference("J4")
    if j4:
        for p in j4.Pads():
            if p.GetName() == "7": set_pad_net(board, p, "USB_HOST_EXT_DP")
            elif p.GetName() == "8": set_pad_net(board, p, "USB_HOST_EXT_DM")
        print("Updated J4 nets -> USB_HOST_EXT_DP / USB_HOST_EXT_DM")

    # U2 (USB2514Bi)
    u2 = board.FindFootprintByReference("U2")
    if u2:
        for p in u2.Pads():
            if p.GetName() == "21": set_pad_net(board, p, "USB_HOST_EXT_DP")
            elif p.GetName() == "20": set_pad_net(board, p, "USB_HOST_EXT_DM")
            elif p.GetName() == "2": set_pad_net(board, p, "USB_DN1_DP")
            elif p.GetName() == "1": set_pad_net(board, p, "USB_DN1_DM")
            elif p.GetName() == "4": set_pad_net(board, p, "USB_DN2_DP")
            elif p.GetName() == "3": set_pad_net(board, p, "USB_DN2_DM")
        print("Updated U2 nets -> Host Ext on Upstream, Port 1 to Dongle, Port 2 to C3")

    # J5 (Dongle pins 3 & 4)
    j5 = board.FindFootprintByReference("J5")
    if j5:
        for p in j5.Pads():
            if p.GetName() == "3": set_pad_net(board, p, "USB_DN1_DP")
            elif p.GetName() == "4": set_pad_net(board, p, "USB_DN1_DM")
        print("Updated J5 nets -> USB_DN1_DP / USB_DN1_DM")

    # U5 (SW3526 DP/DM disconnect: Pin 16=DP, Pin 17=DM, Pin 21=VBUS)
    u5 = board.FindFootprintByReference("U5")
    if u5:
        for p in u5.Pads():
            if p.GetName() == "16": set_pad_net(board, p, "U5_DP_NC")
            elif p.GetName() == "17": set_pad_net(board, p, "U5_DM_NC")
            elif p.GetName() == "21": set_pad_net(board, p, "VBUS_PD1_OUT")
        print("Updated U5 nets -> Pin 16=U5_DP_NC, Pin 17=U5_DM_NC, Pin 21=VBUS_PD1_OUT")

    # 5. Instantiate U10 subsystem on B.Cu in pristine vacant area (X=153.0, Y=98.0)
    # Using QFN-32-1EP_5x5mm_P0.5mm_EP3.7x3.7mm (SMD pad 33, no PTH through-vias)
    fp_qfn = os.path.join(FP_BASE, "Package_DFN_QFN.pretty")
    u10 = pcbnew.FootprintLoad(fp_qfn, "QFN-32-1EP_5x5mm_P0.5mm_EP3.7x3.7mm")
    u10.SetReference("U10")
    u10.SetValue("ESP32-C3FH4")
    u10.SetPosition(pcbnew.VECTOR2I(to_nm(153.0), to_nm(98.0)))
    u10.SetOrientation(pcbnew.EDA_ANGLE(180.0, pcbnew.DEGREES_T))
    u10.SetPath(pcbnew.KIID_PATH(f"/{uuids['U10']}"))
    board.Add(u10)
    u10.SetLayerAndFlip(b_cu_id)

    u10_pin_map = {
        "1": "GND",
        "2": "VCC_3V3",
        "3": "VCC_3V3",
        "4": "C3_NC_GPIO0",
        "5": "C3_NC_GPIO1",
        "6": "C3_NC_GPIO2",
        "7": "C3_EN",
        "8": "C3_NC_GPIO3",
        "9": "C3_NC_GPIO4",
        "10": "C3_NC_GPIO5",
        "11": "VCC_3V3",
        "12": "C3_NC_GPIO6",
        "13": "C3_NC_GPIO7",
        "14": "C3_NC_GPIO8",
        "15": "C3_BOOT",
        "16": "C3_NC_GPIO10",
        "17": "VCC_3V3",
        "18": "USB_DN2_DM",
        "19": "USB_DN2_DP",
        "20": "C3_UART_TX",
        "21": "C3_UART_RX",
        "22": "C3_NC22",
        "23": "C3_NC23",
        "24": "C3_NC24",
        "25": "C3_NC25",
        "26": "C3_NC26",
        "27": "C3_NC27",
        "28": "C3_NC28",
        "29": "C3_XTAL_OUT",
        "30": "C3_XTAL_IN",
        "31": "VCC_3V3",
        "32": "VCC_3V3",
        "33": "GND",
    }
    for p in u10.Pads():
        num = p.GetName()
        net = u10_pin_map.get(num, "GND")
        set_pad_net(board, p, net)
    print("Added U10 (ESP32-C3FH4) at (153.0, 98.0) on B.Cu (flipped)")

    # Y2: Crystal_SMD_3225-4Pin_3.2x2.5mm at (153.0, 104.0), rot=0, B.Cu
    fp_xtal = os.path.join(FP_BASE, "Crystal.pretty")
    y2 = pcbnew.FootprintLoad(fp_xtal, "Crystal_SMD_3225-4Pin_3.2x2.5mm")
    y2.SetReference("Y2")
    y2.SetValue("40.000MHz")
    y2.SetPosition(pcbnew.VECTOR2I(to_nm(153.0), to_nm(104.0)))
    y2.SetOrientation(pcbnew.EDA_ANGLE(0.0, pcbnew.DEGREES_T))
    y2.SetPath(pcbnew.KIID_PATH(f"/{uuids['Y2']}"))
    board.Add(y2)
    y2.SetLayerAndFlip(b_cu_id)
    for p in y2.Pads():
        num = p.GetName()
        if num == "1": set_pad_net(board, p, "C3_XTAL_IN")
        elif num == "2": set_pad_net(board, p, "GND")
        elif num == "3": set_pad_net(board, p, "C3_XTAL_OUT")
        elif num == "4": set_pad_net(board, p, "GND")
    print("Added Y2 (40MHz Crystal) at (153.0, 104.0) on B.Cu (flipped)")

    # Helper for 2-pad passives on B.Cu
    fp_r = os.path.join(FP_BASE, "Resistor_SMD.pretty")
    fp_c = os.path.join(FP_BASE, "Capacitor_SMD.pretty")

    def add_passive_bcu(lib_path, fp_name, ref, val, x, y, rot, net_p1, net_p2, uuid_str):
        f = pcbnew.FootprintLoad(lib_path, fp_name)
        f.SetReference(ref)
        f.SetValue(val)
        f.SetPosition(pcbnew.VECTOR2I(to_nm(x), to_nm(y)))
        f.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
        f.SetPath(pcbnew.KIID_PATH(f"/{uuid_str}"))
        board.Add(f)
        f.SetLayerAndFlip(b_cu_id)
        for p in f.Pads():
            if p.GetName() == "1": set_pad_net(board, p, net_p1)
            elif p.GetName() == "2": set_pad_net(board, p, net_p2)
        print(f"Added {ref} ({val}) at ({x}, {y}) on B.Cu (flipped)")
        return f

    # C28 (10pF XTAL1) at (150.0, 104.0)
    add_passive_bcu(fp_c, "C_0402_1005Metric", "C28", "10pF_50V_XTAL1", 150.0, 104.0, 90.0, "C3_XTAL_IN", "GND", uuids["C28"])
    # C29 (10pF XTAL2) at (156.0, 104.0)
    add_passive_bcu(fp_c, "C_0402_1005Metric", "C29", "10pF_50V_XTAL2", 156.0, 104.0, 90.0, "C3_XTAL_OUT", "GND", uuids["C29"])
    # C30 (10uF VDD) at (153.0, 93.5)
    add_passive_bcu(fp_c, "C_0603_1608Metric", "C30", "10uF_10V", 153.0, 93.5, 0.0, "VCC_3V3", "GND", uuids["C30"])
    # C31 (100nF VDD) at (156.0, 93.5)
    add_passive_bcu(fp_c, "C_0402_1005Metric", "C31", "100nF_16V", 156.0, 93.5, 0.0, "VCC_3V3", "GND", uuids["C31"])
    # R17 (10k EN PU) at (148.5, 96.0)
    add_passive_bcu(fp_r, "R_0402_1005Metric", "R17", "10k_C3_EN_PU", 148.5, 96.0, 0.0, "VCC_3V3", "C3_EN", uuids["R17"])
    # C27 (100nF EN) at (148.5, 94.0)
    add_passive_bcu(fp_c, "C_0402_1005Metric", "C27", "100nF_16V_EN", 148.5, 94.0, 0.0, "C3_EN", "GND", uuids["C27"])
    # R18 (10k BOOT PU) at (148.5, 100.0)
    add_passive_bcu(fp_r, "R_0402_1005Metric", "R18", "10k_C3_BOOT_PU", 148.5, 100.0, 0.0, "VCC_3V3", "C3_BOOT", uuids["R18"])

    # 6. Refill all zones
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    print("Refilled all copper zones.")

    # 7. Save Board
    board.Save(PCB_PATH)
    print(f"✅ Successfully saved updated board to {PCB_PATH}")

if __name__ == "__main__":
    main()
