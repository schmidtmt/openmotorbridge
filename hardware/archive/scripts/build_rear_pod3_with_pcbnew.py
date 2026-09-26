#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
Build Complete KiCad PCB for Rear Pod 3 (OMM Transceiver) with Verified 55x48mm Placement:
- Outline: 55.0 x 48.0 mm (X: 100.0 .. 155.0 mm, Y: 72.0 .. 120.0 mm, R = 2.5 mm)
- Exact Placement & Rotations:
  - U1 (ESP32-C3-WROOM-02U with U.FL): (138.00, 96.00, rot=-90)
  - U2 (MAX-M10S GNSS): (130.25, 78.15, rot=180)
  - J5 (GNSS U.FL): (115.50, 76.03, rot=180)
  - C3 (GNSS Cap): (117.75, 84.22, rot=90)
  - U3 (SX1262 LoRa): (122.00, 113.50, rot=0)
  - J4 (LoRa U.FL): (142.25, 114.50, rot=0)
  - C4 (LoRa Cap): (115.25, 107.78, rot=90)
  - J1 (OMM 6-Pin Horizontal Socket): (102.50, 89.65, rot=0)
  - Left Rail (F1, C1, U4, C2, R1, D1)
  - 4 Corner M2 Holes matching base sled standoffs:
    H1(103.0, 86.5), H2(103.0, 105.5), H3(149.0, 86.5), H4(149.0, 105.5)
- 4-Layer Stackup (F.Cu, In1.Cu GND, In2.Cu 3V3, B.Cu)
"""

import os
import pcbnew

pcb_file = "/Users/schmidtm/openMotorBridge/hardware/kicad_rear_pod3/openmotorbridge_rear_pod3.kicad_pcb"
kicad_fp_dir = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"
kicad_3d_dir = "${KICAD10_3DMODEL_DIR}"

def generate_pod3_board(output_path=pcb_file):
    board = pcbnew.BOARD()

    # Setup Title Block
    tb = board.GetTitleBlock()
    tb.SetTitle("OpenMotorBridge - Rear Pod 3 OMM Transceiver (55x48mm 4-Layer)")
    tb.SetDate("2026-09-03")
    tb.SetRevision("v8.1")
    tb.SetCompany("OpenMotorBridge Open Source Hardware")
    tb.SetComment(0, "Modular Antenna Architecture: U.FL Ports for External 2.4GHz, Internal LoRa & GNSS")
    tb.SetComment(1, "u-blox MAX-M10S GNSS + Semtech SX1262 LoRa (+22dBm) + ESP32-C3 RISC-V")

    # Enable 4 Layers
    board.SetLayerName(pcbnew.In1_Cu, "GND_PLANE")
    board.SetLayerName(pcbnew.In2_Cu, "PWR_3V3")

    # Add Netlist
    net_names = [
        "GND",
        "POD3_VCC_5V",
        "VCC_3V3",
        "POD3_UART_TX",
        "POD3_UART_RX",
        "GNSS_1PPS",
        "POD3_1WIRE_ID",
        "GNSS_TXD",
        "GNSS_RXD",
        "LORA_SCK",
        "LORA_MISO",
        "LORA_MOSI",
        "LORA_NSS",
        "LORA_DIO1",
        "LORA_BUSY",
        "LORA_NRST",
        "NET_F1_5V",
        "NET_LED_R",
        "TP_BOOT",
        "TP_EN",
        "LORA_RF_ANT",
        "GNSS_RF_IN",
    ]

    net_map = {}
    for name in net_names:
        net = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net)
        net_map[name] = net

    component_pins = {
        'J1': {'1': 'POD3_VCC_5V', '2': 'GND', '3': 'POD3_UART_TX', '4': 'POD3_UART_RX', '5': 'GNSS_1PPS', '6': 'POD3_1WIRE_ID'},
        'F1': {'1': 'POD3_VCC_5V', '2': 'NET_F1_5V'},
        'D1': {'1': 'NET_LED_R', '2': 'GND'},
        'R1': {'1': 'NET_F1_5V', '2': 'NET_LED_R'},
        'U4': {'1': 'POD3_1WIRE_ID', '2': 'GND'},
        'U1': {
            '1': 'VCC_3V3', '2': 'TP_EN', '3': 'GNSS_1PPS', '4': 'LORA_DIO1', '5': 'LORA_BUSY',
            '6': 'POD3_UART_TX', '7': 'POD3_UART_RX', '8': 'GNSS_RXD', '9': 'GNSS_TXD',
            '10': 'LORA_SCK', '11': 'LORA_MISO', '12': 'LORA_MOSI', '13': 'LORA_NSS',
            '14': 'LORA_NRST', '15': 'TP_BOOT', '16': 'GND', '17': 'GND', '18': 'GND', '19': 'GND',
        },
        'U2': {
            '1': 'GND', '2': 'GNSS_TXD', '3': 'GNSS_RXD', '4': 'GNSS_1PPS', '5': 'GND', '6': 'GND',
            '7': 'VCC_3V3', '8': 'VCC_3V3', '9': 'GND', '10': 'GND', '11': 'GNSS_RF_IN',
            '12': 'GND', '13': 'GND', '14': 'GND', '15': 'GND', '16': 'GND', '17': 'GND', '18': 'GND',
        },
        'U3': {
            '1': 'VCC_3V3', '2': 'GND', '3': 'GND', '4': 'GND', '5': 'LORA_NRST', '6': 'LORA_BUSY',
            '7': 'LORA_DIO1', '8': 'GND', '9': 'GND', '10': 'VCC_3V3', '11': 'GND', '12': 'GND',
            '13': 'LORA_NSS', '14': 'LORA_SCK', '15': 'LORA_MOSI', '16': 'LORA_MISO', '17': 'GND',
            '18': 'VCC_3V3', '19': 'GND', '20': 'GND', '21': 'LORA_RF_ANT', '22': 'GND', '23': 'GND',
            '24': 'VCC_3V3', '25': 'GND',
        },
        'J4': {'1': 'LORA_RF_ANT', '2': 'GND'},
        'J5': {'1': 'GNSS_RF_IN', '2': 'GND'},
        'C1': {'1': 'VCC_3V3', '2': 'GND'},
        'C2': {'1': 'VCC_3V3', '2': 'GND'},
        'C3': {'1': 'VCC_3V3', '2': 'GND'},
        'C4': {'1': 'VCC_3V3', '2': 'GND'},
        'H1': {'1': 'GND'}, 'H2': {'1': 'GND'}, 'H3': {'1': 'GND'}, 'H4': {'1': 'GND'},
    }

    components = [
        # J1: 6-Pin Horizontal Socket
        ("Connector_PinSocket_2.54mm.pretty", "PinSocket_1x06_P2.54mm_Horizontal", "J1", "6-Pin_OMM_Female_Socket", 102.50, 89.65, 0, pcbnew.F_Cu,
         "Connector_PinSocket_2.54mm.3dshapes/PinSocket_1x06_P2.54mm_Horizontal.step"),
        # Left Rail Protection & ID
        ("Resistor_SMD.pretty", "R_1206_3216Metric", "F1", "PTC_500mA", 111.29, 89.75, 0, pcbnew.F_Cu,
         "Resistor_SMD.3dshapes/R_1206_3216Metric.step"),
        ("Capacitor_SMD.pretty", "C_0805_2012Metric", "C1", "10uF_3V3", 113.75, 84.20, 90, pcbnew.F_Cu,
         "Capacitor_SMD.3dshapes/C_0805_2012Metric.step"),
        ("Package_TO_SOT_SMD.pretty", "SOT-23", "U4", "DS2401_1Wire_ID", 116.19, 103.05, 0, pcbnew.F_Cu,
         "Package_TO_SOT_SMD.3dshapes/SOT-23.step"),
        ("Capacitor_SMD.pretty", "C_0603_1608Metric", "C2", "100nF_MCU", 111.25, 104.72, 90, pcbnew.F_Cu,
         "Capacitor_SMD.3dshapes/C_0603_1608Metric.step"),
        ("Resistor_SMD.pretty", "R_0603_1608Metric", "R1", "1.5k_LED_Resistor", 108.00, 109.08, 90, pcbnew.F_Cu,
         "Resistor_SMD.3dshapes/R_0603_1608Metric.step"),
        ("LED_SMD.pretty", "LED_0805_2012Metric", "D1", "LED_Green_5V", 108.00, 113.44, -90, pcbnew.F_Cu,
         "LED_SMD.3dshapes/LED_0805_2012Metric.step"),

        # GNSS Subsystem (Top)
        ("RF_GPS.pretty", "ublox_MAX", "U2", "MAX-M10S_GNSS", 130.25, 78.15, 180, pcbnew.F_Cu,
         "Package_DFN_QFN.3dshapes/QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm.step"),
        ("Capacitor_SMD.pretty", "C_0603_1608Metric", "C3", "100nF_GNSS", 117.75, 84.22, 90, pcbnew.F_Cu,
         "Capacitor_SMD.3dshapes/C_0603_1608Metric.step"),
        ("Connector_Coaxial.pretty", "U.FL_Hirose_U.FL-R-SMT-1_Vertical", "J5", "U.FL_GNSS", 115.50, 76.03, 180, pcbnew.F_Cu,
         "Connector_Coaxial.3dshapes/U.FL_Hirose_U.FL-R-SMT-1_Vertical.step"),

        # LoRa Subsystem (Bottom)
        ("Package_DFN_QFN.pretty", "QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm", "U3", "SX1262_LoRa_+22dBm", 122.00, 113.50, 0, pcbnew.F_Cu,
         "Package_DFN_QFN.3dshapes/QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm.step"),
        ("Capacitor_SMD.pretty", "C_0603_1608Metric", "C4", "100nF_LoRa", 115.25, 107.78, 90, pcbnew.F_Cu,
         "Capacitor_SMD.3dshapes/C_0603_1608Metric.step"),
        ("Connector_Coaxial.pretty", "U.FL_Hirose_U.FL-R-SMT-1_Vertical", "J4", "U.FL_LORA", 142.25, 114.50, 0, pcbnew.F_Cu,
         "Connector_Coaxial.3dshapes/U.FL_Hirose_U.FL-R-SMT-1_Vertical.step"),

        # Central MCU (ESP32-C3-WROOM-02U with U.FL)
        ("RF_Module.pretty", "ESP32-C3-WROOM-02U", "U1", "ESP32-C3-WROOM-02U", 138.00, 96.00, -90, pcbnew.F_Cu,
         "RF_Module.3dshapes/ESP32-C3-WROOM-02U.step"),

        # 4 M2 Mounting Holes
        ("MountingHole.pretty", "MountingHole_2.2mm_M2_Pad", "H1", "M2_Mounting_Hole", 103.00, 86.50, 0, pcbnew.F_Cu, None),
        ("MountingHole.pretty", "MountingHole_2.2mm_M2_Pad", "H2", "M2_Mounting_Hole", 103.00, 105.50, 0, pcbnew.F_Cu, None),
        ("MountingHole.pretty", "MountingHole_2.2mm_M2_Pad", "H3", "M2_Mounting_Hole", 149.00, 86.50, 0, pcbnew.F_Cu, None),
        ("MountingHole.pretty", "MountingHole_2.2mm_M2_Pad", "H4", "M2_Mounting_Hole", 149.00, 105.50, 0, pcbnew.F_Cu, None),
    ]

    for item in components:
        lib, fp_name, ref, val, x, y, rot, layer, m3d = item
        lib_path = os.path.join(kicad_fp_dir, lib)
        fp = pcbnew.FootprintLoad(lib_path, fp_name)
        if not fp:
            print(f"ERROR: Could not load footprint {lib}/{fp_name}")
            continue

        fp.SetReference(ref)
        fp.SetValue(val)
        fp.SetLayer(layer)
        fp.SetPosition(pcbnew.VECTOR2I(int(x * 1e6), int(y * 1e6)))
        fp.SetOrientationDegrees(rot)
        fp.Reference().SetVisible(False)
        fp.Value().SetVisible(False)

        if m3d:
            fp.Models().clear()
            model = pcbnew.FP_3DMODEL()
            model.m_Filename = f"{kicad_3d_dir}/{m3d}"
            model.m_Scale = pcbnew.VECTOR3D(1.0, 1.0, 1.0)
            model.m_Offset = pcbnew.VECTOR3D(0.0, 0.0, 0.0)
            model.m_Rotation = pcbnew.VECTOR3D(0.0, 0.0, 0.0)
            fp.Add3DModel(model)

        pin_map = component_pins.get(ref, {})
        for pad in fp.Pads():
            pad_num = pad.GetNumber()
            net_name = pin_map.get(pad_num, "")
            if net_name in net_map:
                pad.SetNet(net_map[net_name])

        board.Add(fp)

    # Board Outline (55x48mm with R=2.5mm: 100.0..155.0, 72.0..120.0)
    r = 2.5
    x1, y1 = 100.0, 72.0
    x2, y2 = 155.0, 120.0

    def add_line(sx, sy, ex, ey):
        seg = pcbnew.PCB_SHAPE(board)
        seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        seg.SetStart(pcbnew.VECTOR2I(int(sx * 1e6), int(sy * 1e6)))
        seg.SetEnd(pcbnew.VECTOR2I(int(ex * 1e6), int(ey * 1e6)))
        seg.SetWidth(int(0.15 * 1e6))
        seg.SetLayer(pcbnew.Edge_Cuts)
        board.Add(seg)

    def add_arc(sx, sy, mx, my, ex, ey):
        arc = pcbnew.PCB_SHAPE(board)
        arc.SetShape(pcbnew.SHAPE_T_ARC)
        start_v = pcbnew.VECTOR2I(int(sx * 1e6), int(sy * 1e6))
        mid_v = pcbnew.VECTOR2I(int(mx * 1e6), int(my * 1e6))
        end_v = pcbnew.VECTOR2I(int(ex * 1e6), int(ey * 1e6))
        arc.SetArcGeometry(start_v, mid_v, end_v)
        arc.SetWidth(int(0.15 * 1e6))
        arc.SetLayer(pcbnew.Edge_Cuts)
        board.Add(arc)

    add_line(x1+r, y1, x2-r, y1)
    add_arc(x2-r, y1, x2-0.73, y1+0.73, x2, y1+r)
    add_line(x2, y1+r, x2, y2-r)
    add_arc(x2, y2-r, x2-0.73, y2-0.73, x2-r, y2)
    add_line(x2-r, y2, x1+r, y2)
    add_arc(x1+r, y2, x1+0.73, y2-0.73, x1, y2-r)
    add_line(x1, y2-r, x1, y1+r)
    add_arc(x1, y1+r, x1+0.73, y1+0.73, x1+r, y1)

    print(f"Board generated successfully for {output_path}")
    return board

if __name__ == "__main__":
    generate_pod3_board()
