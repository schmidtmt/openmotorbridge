#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
Generate Complete KiCad 10 Project for PCBA 08: OpenMotorBridge Radar 2.0 Sub-MCU, V2X & Halo (PCBA 08)
======================================================================================================
- Board Outline: 115.0 x 65.0 mm 4-Layer FR4 (matching radar_mr20_housing.scad Variante 1 Flügel-Rechteck)
- Inner Cutout: 61.0 x 51.0 mm (Dead Center at X=0, Y=0) for Wheeltec MR20 77-GHz radar module
- Generous 27.0 x 65.0 mm Left and Right Wing Areas (1755 mm² each!)
- 4x M2.5 Corner Mounting Holes (Pitch: 103.0 x 53.0 mm, X=±51.5, Y=±26.5)
- Front Layer (F.Cu):
    * 36x WS2812B-2020 addressable RGB LEDs:
        - 12x Left Wing: 3x4 Matrix for High-Intensity Blind-Spot Left Warning
        - 12x Right Wing: 3x4 Matrix for High-Intensity Blind-Spot Right Warning
        - 6x Top Edge: Horizontal Ambient Indicator Line
        - 6x Bottom Edge: Horizontal Ambient Indicator Line
- Bottom Layer (B.Cu) - Strictly on the 27mm Wings, ZERO parts in the cutout or narrow borders:
    * Left Wing (B.Cu):
        - U1: ESP32-C5 Sub-MCU Module (ESP32-C5-WROOM-1U / MINI-1U with onboard U.FL, 160MHz RISC-V, 5.9 GHz ITS-G5 Sniffer + Radar Parser)
        - J3: U.FL External Coaxial Connector (optional direct patch feed)
        - SW1: Tactile Pushbutton (Boot / IO9)
        - SW2: Tactile Pushbutton (Reset / EN)
        - C3, C4: 100nF 0603 Decoupling Capacitors
        - R1, R2: 10k 0603 Pull-up Resistors (EN, BOOT)
    * Right Wing (B.Cu):
        - U2: TPS7A0533 / AP2112K 3.3V 500mA LDO Regulator (SOT-23-5)
        - C1, C2: 10uF 0805 filter capacitors (5V input, 3.3V output)
        - J1: JST-SH 1.0mm 4-Pin Horizontal (Binder M5 Pigtail: 5V, GND, CENTRAL_TX, CENTRAL_RX)
        - J2: JST-SH 1.0mm 4-Pin Horizontal (MR20 Radar Adapter: 5V, GND, MR20_RX, MR20_TX)
        - D25: SOT-23 TVS diode array (PESD5V0S2BT) for UART line protection
"""

import os
import sys
import json
import math
import subprocess
import pcbnew

PROJECT_DIR = "/Users/schmidtm/openMotorBridge/hardware/kicad_radar_submcu"
PRO_PATH = os.path.join(PROJECT_DIR, "openmotorbridge_radar_submcu.kicad_pro")
SCH_PATH = os.path.join(PROJECT_DIR, "openmotorbridge_radar_submcu.kicad_sch")
PCB_PATH = os.path.join(PROJECT_DIR, "openmotorbridge_radar_submcu.kicad_pcb")

KICAD_FP_DIR = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"
KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

def to_nm(mm):
    return int(mm * 1e6)

def create_project_file():
    os.makedirs(PROJECT_DIR, exist_ok=True)
    pro_content = {
        "board": {
            "design_settings": {
                "defaults": {
                    "board_outline_line_width": 0.15,
                    "copper_line_width": 0.20,
                    "silk_line_width": 0.12,
                    "min_clearance": 0.127,
                    "min_track_width": 0.15,
                    "min_via_annular_width": 0.15,
                    "min_through_drill": 0.2,
                    "min_hole_clearance": 0.25,
                    "min_copper_edge_clearance": 0.30
                },
                "rules": {
                    "solder_mask_min_width": 0.08,
                    "silk_edge_clearance": 0.15
                }
            },
            "net_classes": [
                {
                    "name": "Default",
                    "clearance": 0.127,
                    "track_width": 0.15,
                    "via_diameter": 0.6,
                    "via_drill": 0.3
                },
                {
                    "name": "Power",
                    "clearance": 0.15,
                    "track_width": 0.35,
                    "via_diameter": 0.6,
                    "via_drill": 0.3,
                    "nets": ["VCC_5V", "VCC_3V3", "GND"]
                },
                {
                    "name": "RF_5G9",
                    "clearance": 0.25,
                    "track_width": 0.45,
                    "via_diameter": 0.6,
                    "via_drill": 0.3,
                    "nets": ["RF_5G9"]
                }
            ]
        },
        "meta": {
            "filename": "openmotorbridge_radar_submcu.kicad_pro",
            "version": 1
        }
    }
    with open(PRO_PATH, "w", encoding="utf-8") as f:
        json.dump(pro_content, f, indent=2)
    print(f"✓ Created {PRO_PATH}")

def create_schematic_file():
    sch_content = """(kicad_sch
\t(version 20240108)
\t(generator "openmotorbridge_gen")
\t(generator_version "10.0")
\t(uuid "f0000000-0000-0000-0000-000000000080")
\t(paper "A3")
\t(title_block
\t\t(title "OpenMotorBridge Radar 2.0 Sub-MCU, 5.9 GHz V2X & LED Halo (PCBA 08)")
\t\t(date "2026-09-23")
\t\t(rev "v2.0-wing")
\t\t(company "OpenMotorBridge Open Source Hardware")
\t\t(comment 1 "ESP32-C5 Sub-MCU (ITS-G5 5.9 GHz Sniffer), Wheeltec MR20 Adapter, 36-LED Matrix")
\t)

\t(global_label "VCC_5V" (shape input) (at 30.0 30.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "VCC_3V3" (shape output) (at 80.0 30.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "GND" (shape passive) (at 30.0 35.0 180) (effects (font (size 1.27 1.27)) (justify right)))

\t(global_label "CENTRAL_TX" (shape input) (at 30.0 45.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "CENTRAL_RX" (shape output) (at 30.0 50.0 0) (effects (font (size 1.27 1.27)) (justify left)))

\t(global_label "MR20_TX" (shape input) (at 120.0 45.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "MR20_RX" (shape output) (at 120.0 50.0 0) (effects (font (size 1.27 1.27)) (justify left)))

\t(global_label "WS2812_DATA" (shape output) (at 120.0 60.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "ESP_EN" (shape input) (at 120.0 65.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "ESP_IO9_BOOT" (shape input) (at 120.0 70.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "RF_5G9" (shape passive) (at 120.0 75.0 0) (effects (font (size 1.27 1.27)) (justify left)))
)
"""
    with open(SCH_PATH, "w", encoding="utf-8") as f:
        f.write(sch_content)
    print(f"✓ Created {SCH_PATH}")

def build_pcb():
    board = pcbnew.BOARD()
    board.SetFileName(PCB_PATH)

    # Design settings: support 0.2mm micro-vias / thermal pad vias (standard 4-layer FR4)
    ds = board.GetDesignSettings()
    ds.m_MinThroughDrill = to_nm(0.2)
    ds.m_MinHoleClearance = to_nm(0.2)
    ds.m_CopperEdgeClearance = to_nm(0.3)

    # Net setup
    net_names = [
        "GND", "VCC_5V", "VCC_3V3",
        "CENTRAL_TX", "CENTRAL_RX",
        "MR20_TX", "MR20_RX",
        "WS2812_DATA", "ESP_EN", "ESP_IO9_BOOT", "RF_5G9"
    ]
    net_map = {}
    for name in net_names:
        net = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net)
        net_map[name] = net

    # Board Center at (100.0, 100.0) mm
    cx, cy = 100.0, 100.0
    w_out, h_out = 115.0, 65.0
    w_in, h_in = 61.0, 51.0
    chamfer = 2.5

    x0 = cx - w_out / 2.0
    x1 = cx + w_out / 2.0
    y0 = cy - h_out / 2.0
    y1 = cy + h_out / 2.0

    def add_line(x_s, y_s, x_e, y_e, layer=pcbnew.Edge_Cuts):
        seg = pcbnew.PCB_SHAPE(board)
        seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        seg.SetLayer(layer)
        seg.SetWidth(to_nm(0.15))
        seg.SetStart(pcbnew.VECTOR2I(to_nm(x_s), to_nm(y_s)))
        seg.SetEnd(pcbnew.VECTOR2I(to_nm(x_e), to_nm(y_e)))
        board.Add(seg)

    # 1. Closed Outer Contour on Edge.Cuts with 2.5 mm chamfered corners
    add_line(x0 + chamfer, y0, x1 - chamfer, y0)
    add_line(x1 - chamfer, y0, x1, y0 + chamfer)
    add_line(x1, y0 + chamfer, x1, y1 - chamfer)
    add_line(x1, y1 - chamfer, x1 - chamfer, y1)
    add_line(x1 - chamfer, y1, x0 + chamfer, y1)
    add_line(x0 + chamfer, y1, x0, y1 - chamfer)
    add_line(x0, y1 - chamfer, x0, y0 + chamfer)
    add_line(x0, y0 + chamfer, x0 + chamfer, y0)

    # 2. Closed Inner Cutout Contour for MR20 (61.0 x 51.0 mm)
    ix0 = cx - w_in / 2.0
    ix1 = cx + w_in / 2.0
    iy0 = cy - h_in / 2.0
    iy1 = cy + h_in / 2.0

    add_line(ix0, iy0, ix1, iy0)
    add_line(ix1, iy0, ix1, iy1)
    add_line(ix1, iy1, ix0, iy1)
    add_line(ix0, iy1, ix0, iy0)

    # 3. Helper to load footprints
    def load_fp(lib, name):
        return pcbnew.FootprintLoad(os.path.join(KICAD_FP_DIR, lib), name)

    # 4. 4x M2.5 Mounting Holes in corners (H1..H4, Pitch: 103.0 x 53.0 mm)
    hole_dx = 51.5
    hole_dy = 26.5
    for idx, (hx, hy) in enumerate([
        (cx - hole_dx, cy - hole_dy),
        (cx + hole_dx, cy - hole_dy),
        (cx + hole_dx, cy + hole_dy),
        (cx - hole_dx, cy + hole_dy)
    ], start=1):
        fp = load_fp("MountingHole.pretty", "MountingHole_2.7mm_M2.5_Pad")
        if fp:
            fp.SetReference(f"H{idx}")
            fp.SetValue("M2.5_MountingHole")
            fp.SetPosition(pcbnew.VECTOR2I(to_nm(hx), to_nm(hy)))
            for pad in fp.Pads():
                pad.SetNet(net_map["GND"])
            board.Add(fp)

    # --- 36x WS2812B-2020 LEDs on Front Layer (F.Cu) ---
    led_fp_name = "LED_WS2812B-2020_PLCC4_2.0x2.0mm"
    led_positions = []

    # Left Wing: 3 columns x 4 rows matrix (D1..D12)
    for col_x in [-48.0, -42.0, -36.0]:
        for row_y in [-18.0, -6.0, 6.0, 18.0]:
            led_positions.append((cx + col_x, cy + row_y, 0.0))

    # Top Edge: 6 LEDs line (D13..D18)
    for x in [-25.0, -15.0, -5.0, 5.0, 15.0, 25.0]:
        led_positions.append((cx + x, cy - 28.5, 0.0))

    # Right Wing: 3 columns x 4 rows matrix (D19..D30)
    for col_x in [36.0, 42.0, 48.0]:
        for row_y in [-18.0, -6.0, 6.0, 18.0]:
            led_positions.append((cx + col_x, cy + row_y, 0.0))

    # Bottom Edge: 6 LEDs line (D31..D36)
    for x in [25.0, 15.0, 5.0, -5.0, -15.0, -25.0]:
        led_positions.append((cx + x, cy + 28.5, 180.0))

    for i, (lx, ly, rot) in enumerate(led_positions, start=1):
        fp = load_fp("LED_SMD.pretty", led_fp_name)
        if fp:
            fp.SetReference(f"D{i}")
            fp.SetValue("WS2812B-2020")
            fp.SetPosition(pcbnew.VECTOR2I(to_nm(lx), to_nm(ly)))
            fp.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
            fp.SetLayer(pcbnew.F_Cu)
            for pad in fp.Pads():
                num = pad.GetNumber()
                if num == "1": pad.SetNet(net_map["WS2812_DATA"])
                elif num == "2": pad.SetNet(net_map["VCC_5V"])
                elif num == "3": pad.SetNet(net_map["GND"])
                elif num == "4": pad.SetNet(net_map["WS2812_DATA"])
            board.Add(fp)

    # --- Bottom Layer Components (B.Cu) - Strictly on the 27mm Wings ---
    
    # U1: ESP32-C5 Sub-MCU Module (WROOM-02U/MINI-1U with onboard U.FL, 18 pins)
    # Centered on Left Wing at (cx - 44.0, cy)
    u1_fp = load_fp("RF_Module.pretty", "ESP32-C3-WROOM-02U")
    if u1_fp:
        u1_fp.SetReference("U1")
        u1_fp.SetValue("ESP32-C5-WROOM-1U")
        pos = pcbnew.VECTOR2I(to_nm(cx - 44.0), to_nm(cy))
        u1_fp.SetPosition(pos)
        board.Add(u1_fp)
        u1_fp.Flip(pos, False)
        for pad in u1_fp.Pads():
            num = pad.GetNumber()
            if num in ["1", "9", "18", "19"]: pad.SetNet(net_map["GND"])
            elif num == "2": pad.SetNet(net_map["VCC_3V3"])
            elif num == "7": pad.SetNet(net_map["ESP_EN"])
            elif num == "13": pad.SetNet(net_map["ESP_IO9_BOOT"])
            elif num == "16": pad.SetNet(net_map["CENTRAL_TX"]) # UART RX from Central
            elif num == "17": pad.SetNet(net_map["CENTRAL_RX"]) # UART TX to Central
            elif num == "4": pad.SetNet(net_map["MR20_TX"])     # UART RX from MR20
            elif num == "5": pad.SetNet(net_map["MR20_RX"])     # UART TX to MR20
            elif num == "8": pad.SetNet(net_map["WS2812_DATA"]) # RMT NeoPixel out

    # J3: U.FL RF Coaxial Connector for 5.9 GHz V2X Antenna (Left Wing, Top)
    j3_fp = load_fp("Connector_Coaxial.pretty", "U.FL_Hirose_U.FL-R-SMT-1_Vertical")
    if j3_fp:
        j3_fp.SetReference("J3")
        j3_fp.SetValue("U.FL_5G9_V2X")
        pos = pcbnew.VECTOR2I(to_nm(cx - 44.0), to_nm(cy - 18.0))
        j3_fp.SetPosition(pos)
        board.Add(j3_fp)
        j3_fp.Flip(pos, False)
        for pad in j3_fp.Pads():
            if pad.GetNumber() == "1":
                pad.SetNet(net_map["RF_5G9"])
            else:
                pad.SetNet(net_map["GND"])

    # SW1: Boot Switch (IO9) on Left Wing, Bottom
    sw1_fp = load_fp("Button_Switch_SMD.pretty", "SW_Push_SPST_NO_Alps_SKRK")
    if sw1_fp:
        sw1_fp.SetReference("SW1")
        sw1_fp.SetValue("BOOT_SW")
        pos = pcbnew.VECTOR2I(to_nm(cx - 36.0), to_nm(cy + 22.0))
        sw1_fp.SetPosition(pos)
        board.Add(sw1_fp)
        sw1_fp.Flip(pos, False)
        for pad in sw1_fp.Pads():
            if pad.GetNumber() == "1": pad.SetNet(net_map["ESP_IO9_BOOT"])
            else: pad.SetNet(net_map["GND"])

    # SW2: Reset Switch (EN) on Left Wing, Bottom
    sw2_fp = load_fp("Button_Switch_SMD.pretty", "SW_Push_SPST_NO_Alps_SKRK")
    if sw2_fp:
        sw2_fp.SetReference("SW2")
        sw2_fp.SetValue("RESET_SW")
        pos = pcbnew.VECTOR2I(to_nm(cx - 51.0), to_nm(cy + 22.0))
        sw2_fp.SetPosition(pos)
        board.Add(sw2_fp)
        sw2_fp.Flip(pos, False)
        for pad in sw2_fp.Pads():
            if pad.GetNumber() == "1": pad.SetNet(net_map["ESP_EN"])
            else: pad.SetNet(net_map["GND"])

    # C3, C4: 100nF Decoupling Capacitors (Left Wing)
    for idx, (c_name, c_x, c_y) in enumerate([
        ("C3", cx - 35.0, cy - 9.0),
        ("C4", cx - 35.0, cy + 12.0)
    ], start=3):
        c_fp = load_fp("Capacitor_SMD.pretty", "C_0603_1608Metric")
        if c_fp:
            c_fp.SetReference(c_name)
            c_fp.SetValue("100nF")
            pos = pcbnew.VECTOR2I(to_nm(c_x), to_nm(c_y))
            c_fp.SetPosition(pos)
            board.Add(c_fp)
            c_fp.Flip(pos, False)
            for pad in c_fp.Pads():
                if pad.GetNumber() == "1": pad.SetNet(net_map["VCC_3V3"])
                else: pad.SetNet(net_map["GND"])

    # R1, R2: 10k Pull-up Resistors (Left Wing)
    for r_name, r_net, r_x, r_y in [
        ("R1", "ESP_EN", cx - 52.0, cy - 9.0),
        ("R2", "ESP_IO9_BOOT", cx - 52.0, cy + 12.0)
    ]:
        r_fp = load_fp("Resistor_SMD.pretty", "R_0603_1608Metric")
        if r_fp:
            r_fp.SetReference(r_name)
            r_fp.SetValue("10k")
            pos = pcbnew.VECTOR2I(to_nm(r_x), to_nm(r_y))
            r_fp.SetPosition(pos)
            board.Add(r_fp)
            r_fp.Flip(pos, False)
            for pad in r_fp.Pads():
                if pad.GetNumber() == "1": pad.SetNet(net_map["VCC_3V3"])
                else: pad.SetNet(net_map[r_net])

    # --- Right Wing Components (B.Cu) ---

    # U2: SOT-23-5 LDO Regulator (Right Wing, Top)
    u2_fp = load_fp("Package_TO_SOT_SMD.pretty", "SOT-23-5")
    if u2_fp:
        u2_fp.SetReference("U2")
        u2_fp.SetValue("TPS7A0533")
        pos = pcbnew.VECTOR2I(to_nm(cx + 44.0), to_nm(cy - 16.0))
        u2_fp.SetPosition(pos)
        board.Add(u2_fp)
        u2_fp.Flip(pos, False)
        for pad in u2_fp.Pads():
            num = pad.GetNumber()
            if num in ["1", "3"]: pad.SetNet(net_map["VCC_5V"]) # VIN, EN
            elif num == "2": pad.SetNet(net_map["GND"])
            elif num == "5": pad.SetNet(net_map["VCC_3V3"]) # VOUT

    # C1..C2 Filter Capacitors (10uF 0805 for LDO in Right Wing, Top)
    c1_fp = load_fp("Capacitor_SMD.pretty", "C_0805_2012Metric")
    if c1_fp:
        c1_fp.SetReference("C1")
        c1_fp.SetValue("10uF_16V")
        pos = pcbnew.VECTOR2I(to_nm(cx + 36.0), to_nm(cy - 16.0))
        c1_fp.SetPosition(pos)
        board.Add(c1_fp)
        c1_fp.Flip(pos, False)
        for pad in c1_fp.Pads():
            if pad.GetNumber() == "1": pad.SetNet(net_map["VCC_5V"])
            else: pad.SetNet(net_map["GND"])

    c2_fp = load_fp("Capacitor_SMD.pretty", "C_0805_2012Metric")
    if c2_fp:
        c2_fp.SetReference("C2")
        c2_fp.SetValue("10uF_10V")
        pos = pcbnew.VECTOR2I(to_nm(cx + 52.0), to_nm(cy - 16.0))
        c2_fp.SetPosition(pos)
        board.Add(c2_fp)
        c2_fp.Flip(pos, False)
        for pad in c2_fp.Pads():
            if pad.GetNumber() == "1": pad.SetNet(net_map["VCC_3V3"])
            else: pad.SetNet(net_map["GND"])

    # J1: JST-SH 4-Pin (Central Box Binder M5 UART & Power) in Right Wing, Mid
    j1_fp = load_fp("Connector_JST.pretty", "JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal")
    if j1_fp:
        j1_fp.SetReference("J1")
        j1_fp.SetValue("JST_SH_4P_CENTRAL")
        pos = pcbnew.VECTOR2I(to_nm(cx + 44.0), to_nm(cy + 4.0))
        j1_fp.SetPosition(pos)
        board.Add(j1_fp)
        j1_fp.Flip(pos, False)
        for pad in j1_fp.Pads():
            num = pad.GetNumber()
            if num == "1": pad.SetNet(net_map["VCC_5V"])
            elif num == "2": pad.SetNet(net_map["GND"])
            elif num == "3": pad.SetNet(net_map["CENTRAL_TX"])
            elif num == "4": pad.SetNet(net_map["CENTRAL_RX"])
            else: pad.SetNet(net_map["GND"])

    # J2: JST-SH 4-Pin (MR20 Radar Cable Adapter Interface) in Right Wing, Bottom
    j2_fp = load_fp("Connector_JST.pretty", "JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal")
    if j2_fp:
        j2_fp.SetReference("J2")
        j2_fp.SetValue("JST_SH_4P_MR20")
        pos = pcbnew.VECTOR2I(to_nm(cx + 44.0), to_nm(cy + 20.0))
        j2_fp.SetPosition(pos)
        board.Add(j2_fp)
        j2_fp.Flip(pos, False)
        for pad in j2_fp.Pads():
            num = pad.GetNumber()
            if num == "1": pad.SetNet(net_map["VCC_5V"])
            elif num == "2": pad.SetNet(net_map["GND"])
            elif num == "3": pad.SetNet(net_map["MR20_TX"])
            elif num == "4": pad.SetNet(net_map["MR20_RX"])
            else: pad.SetNet(net_map["GND"])

    # D25: SOT-23 TVS Diode in Right Wing (near J1)
    d25_fp = load_fp("Package_TO_SOT_SMD.pretty", "SOT-23")
    if d25_fp:
        d25_fp.SetReference("D25")
        d25_fp.SetValue("PESD5V0S2BT")
        pos = pcbnew.VECTOR2I(to_nm(cx + 35.0), to_nm(cy + 4.0))
        d25_fp.SetPosition(pos)
        board.Add(d25_fp)
        d25_fp.Flip(pos, False)
        for pad in d25_fp.Pads():
            num = pad.GetNumber()
            if num == "1": pad.SetNet(net_map["CENTRAL_TX"])
            elif num == "2": pad.SetNet(net_map["CENTRAL_RX"])
            elif num == "3": pad.SetNet(net_map["GND"])

    board.Save(PCB_PATH)
    print(f"✓ Saved {PCB_PATH}")

if __name__ == "__main__":
    create_project_file()
    create_schematic_file()
    build_pcb()
    print("✨ PCBA 08: OpenMotorBridge Radar 2.0 Sub-MCU Project Successfully Built!")
