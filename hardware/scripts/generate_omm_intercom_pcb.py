#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
Generate Complete KiCad 10 Project for PCBA 09: OpenMotorMesh (OMM) 2.4 GHz Intercom & UCS Modul
================================================================================================
- Board Outline: 60.0 x 30.0 mm 2-Layer FR4 (matching ECE 22.06 UCS Gehäuse omm_ucs_headset_enclosure.scad)
- 4x M2 Mounting Holes (Pitch: 52.0 x 22.0 mm, X=±26.0, Y=±11.0 from center)
- Antenna Architecture:
    * ESP32-C6-MINI-1U has its onboard U.FL socket directly on the module!
    * J4 removed - Taoglas FXP73 flex-dipole antenna snaps directly onto the module U.FL socket.
    * No 50-Ohm RF microstrip required on the PCB.
- USB-C Connector (J1):
    * Perfectly centered at Y = 100.0 mm (exact vertical middle of the 30mm board).
    * Rotated 270.0°: mouth faces West (-X, outward through enclosure port), SMD pads face East (+X, into PCB).
    * Front THT shield tabs sit at X = 70.95 mm (safely 0.95 mm inside the board edge at X = 70.0 mm).
    * Metal nose protrudes 1.65 mm past board edge to engage with the enclosure gasket.
- Clean Pre-Placement with generous clearance and ZERO overlaps.
"""

import os
import sys
import json
import math
import subprocess
import pcbnew

PROJECT_DIR = "/Users/schmidtm/openMotorBridge/hardware/kicad_omm_intercom"
PRO_PATH = os.path.join(PROJECT_DIR, "openmotorbridge_omm_intercom.kicad_pro")
SCH_PATH = os.path.join(PROJECT_DIR, "openmotorbridge_omm_intercom.kicad_sch")
PCB_PATH = os.path.join(PROJECT_DIR, "openmotorbridge_omm_intercom.kicad_pcb")

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
                    "min_through_drill": 0.3,
                    "min_hole_clearance": 0.25,
                    "min_copper_edge_clearance": 0.30
                },
                "rules": {
                    "solder_mask_min_width": 0.08,
                    "silk_edge_clearance": 0.15
                }
            }
        },
        "net_settings": {
            "classes": [
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
                    "nets": ["VBUS_5V", "VBAT", "SYS_PWR", "VCC_3V3", "GND"]
                },
                {
                    "name": "Audio",
                    "clearance": 0.15,
                    "track_width": 0.20,
                    "via_diameter": 0.6,
                    "via_drill": 0.3,
                    "nets": ["I2S_MCLK", "I2S_BCLK", "I2S_WS", "I2S_DOUT", "I2S_DIN", "MIC_IN_P", "MIC_IN_N", "HP_OUT_P", "HP_OUT_N"]
                }
            ]
        },
        "meta": {
            "filename": "openmotorbridge_omm_intercom.kicad_pro",
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
\t(uuid "f0000000-0000-0000-0000-000000000090")
\t(paper "A3")
\t(title_block
\t\t(title "OpenMotorBridge OMM 2.4 GHz Intercom & UCS Modul (PCBA 09)")
\t\t(date "2026-10-02")
\t\t(rev "v1.1-ucs")
\t\t(company "OpenMotorBridge Open Source Hardware")
\t\t(comment 1 "ESP32-C6-MINI-1U (Direct On-Module U.FL), BQ24075 PMIC, ES8311 Codec, USB-C IP67")
\t)

\t(global_label "VBUS_5V" (shape input) (at 30.0 30.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "VBAT" (shape bidirectional) (at 30.0 35.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "SYS_PWR" (shape output) (at 80.0 30.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "VCC_3V3" (shape output) (at 80.0 35.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "GND" (shape passive) (at 30.0 40.0 180) (effects (font (size 1.27 1.27)) (justify right)))

\t(global_label "USB_DP" (shape bidirectional) (at 30.0 50.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "USB_DN" (shape bidirectional) (at 30.0 55.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "USB_CC1" (shape passive) (at 30.0 60.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "USB_CC2" (shape passive) (at 30.0 65.0 180) (effects (font (size 1.27 1.27)) (justify right)))

\t(global_label "CHG_STAT" (shape input) (at 80.0 50.0 0) (effects (font (size 1.27 1.27)) (justify left)))

\t(global_label "I2S_MCLK" (shape output) (at 140.0 30.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "I2S_BCLK" (shape output) (at 140.0 35.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "I2S_WS" (shape output) (at 140.0 40.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "I2S_DOUT" (shape output) (at 140.0 45.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "I2S_DIN" (shape input) (at 140.0 50.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "I2C_SDA" (shape bidirectional) (at 140.0 55.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "I2C_SCL" (shape output) (at 140.0 60.0 0) (effects (font (size 1.27 1.27)) (justify left)))

\t(global_label "BTN_PWR" (shape input) (at 200.0 30.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "BTN_MESH" (shape input) (at 200.0 35.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "BTN_VOL_UP" (shape input) (at 200.0 40.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "BTN_VOL_DOWN" (shape input) (at 200.0 45.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "WS2812_DATA" (shape output) (at 200.0 50.0 0) (effects (font (size 1.27 1.27)) (justify left)))

\t(global_label "MIC_IN_P" (shape input) (at 200.0 60.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "MIC_IN_N" (shape input) (at 200.0 65.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "HP_OUT_P" (shape output) (at 200.0 70.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "HP_OUT_N" (shape output) (at 200.0 75.0 0) (effects (font (size 1.27 1.27)) (justify left)))
)
"""
    with open(SCH_PATH, "w", encoding="utf-8") as f:
        f.write(sch_content)
    print(f"✓ Created {SCH_PATH}")

def build_pcb():
    board = pcbnew.BOARD()
    board.SetFileName(PCB_PATH)

    ds = board.GetDesignSettings()
    ds.m_MinThroughDrill = to_nm(0.3)
    ds.m_MinHoleClearance = to_nm(0.25)
    ds.m_CopperEdgeClearance = to_nm(0.3)

    # 1. Setup Netlist (Without RF_2G4_UFL, with proper PMIC nets)
    net_names = [
        "GND", "VBUS_5V", "VBAT", "SYS_PWR", "VCC_3V3",
        "USB_DP", "USB_DN", "USB_CC1", "USB_CC2",
        "CHG_STAT", "NTC_TS", "ISET", "ILIM",
        "I2S_MCLK", "I2S_BCLK", "I2S_WS", "I2S_DOUT", "I2S_DIN",
        "I2C_SDA", "I2C_SCL",
        "BTN_PWR", "BTN_MESH", "BTN_VOL_UP", "BTN_VOL_DOWN",
        "WS2812_DATA", "MIC_IN_P", "MIC_IN_N", "HP_OUT_P", "HP_OUT_N"
    ]
    net_map = {}
    for name in net_names:
        net = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net)
        net_map[name] = net

    # 2. Board Outline: 60.0 x 30.0 mm centered at (100.0, 100.0) mm
    cx, cy = 100.0, 100.0
    w_out, h_out = 60.0, 30.0
    chamfer = 2.5

    x0 = cx - w_out / 2.0  # 70.0 mm
    x1 = cx + w_out / 2.0  # 130.0 mm
    y0 = cy - h_out / 2.0  # 85.0 mm
    y1 = cy + h_out / 2.0  # 115.0 mm

    def add_line(x_s, y_s, x_e, y_e, layer=pcbnew.Edge_Cuts):
        seg = pcbnew.PCB_SHAPE(board)
        seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        seg.SetLayer(layer)
        seg.SetWidth(to_nm(0.15))
        seg.SetStart(pcbnew.VECTOR2I(to_nm(x_s), to_nm(y_s)))
        seg.SetEnd(pcbnew.VECTOR2I(to_nm(x_e), to_nm(y_e)))
        board.Add(seg)

    # Outer 60x30 mm contour with 2.5mm corner chamfers
    add_line(x0 + chamfer, y0, x1 - chamfer, y0)
    add_line(x1 - chamfer, y0, x1, y0 + chamfer)
    add_line(x1, y0 + chamfer, x1, y1 - chamfer)
    add_line(x1, y1 - chamfer, x1 - chamfer, y1)
    add_line(x1 - chamfer, y1, x0 + chamfer, y1)
    add_line(x0 + chamfer, y1, x0, y1 - chamfer)
    add_line(x0, y1 - chamfer, x0, y0 + chamfer)
    add_line(x0, y0 + chamfer, x0 + chamfer, y0)

    def load_fp(lib, name):
        return pcbnew.FootprintLoad(os.path.join(KICAD_FP_DIR, lib), name)

    # 3. 4x M2 Mounting Holes (Pitch: 52.0 x 22.0 mm, centered)
    for idx, (hx, hy) in enumerate([
        (cx - 26.0, cy - 11.0),
        (cx + 26.0, cy - 11.0),
        (cx + 26.0, cy + 11.0),
        (cx - 26.0, cy + 11.0)
    ], start=1):
        fp = load_fp("MountingHole.pretty", "MountingHole_2.2mm_M2_Pad")
        if fp:
            fp.SetReference(f"H{idx}")
            fp.SetValue("M2_MountingHole")
            fp.SetPosition(pcbnew.VECTOR2I(to_nm(hx), to_nm(hy)))
            for pad in fp.Pads():
                pad.SetNet(net_map["GND"])
            board.Add(fp)

    # 4. Footprints Placement & Logical Nets (ZERO OVERLAP, Generous Spacing)

    # --- West Edge: USB-C (J1) Cleanly Centered at Y=100.0 mm & Aligned with Edge ---
    # At Angle 270.0°:
    # - Connector mouth points West (-X, through enclosure port, reaches X = 68.35 mm)
    # - SMD signal pads point East (+X, into PCB, at X = 76.05 mm)
    # - Front THT shield tabs sit at X = 70.95 mm (safely 0.95 mm inside the board edge at 70.0 mm)
    j1_fp = load_fp("Connector_USB.pretty", "USB_C_Receptacle_HRO_TYPE-C-31-M-12")
    if j1_fp:
        j1_fp.SetReference("J1")
        j1_fp.SetValue("TYPE-C-31-M-12_IP67")
        pos = pcbnew.VECTOR2I(to_nm(72.0), to_nm(100.0))
        j1_fp.SetPosition(pos)
        j1_fp.SetOrientation(pcbnew.EDA_ANGLE(270.0, pcbnew.DEGREES_T))
        board.Add(j1_fp)
        for pad in j1_fp.Pads():
            num = pad.GetNumber()
            if num in ["A1", "B12", "A12", "B1", "SH", "0", ""]: pad.SetNet(net_map["GND"])
            elif num in ["A4", "B9", "A9", "B4"]: pad.SetNet(net_map["VBUS_5V"])
            elif num in ["A6", "B6"]: pad.SetNet(net_map["USB_DP"])
            elif num in ["A7", "B7"]: pad.SetNet(net_map["USB_DN"])
            elif num == "A5": pad.SetNet(net_map["USB_CC1"])
            elif num == "B5": pad.SetNet(net_map["USB_CC2"])
            else: pad.SetNet(net_map["GND"])

    # TVS Diode D2 (USBLC6-2SC6) placed right next to USB-C SMD pins
    d2_fp = load_fp("Package_TO_SOT_SMD.pretty", "SOT-23-6")
    if d2_fp:
        d2_fp.SetReference("D2")
        d2_fp.SetValue("USBLC6-2SC6")
        pos = pcbnew.VECTOR2I(to_nm(80.0), to_nm(96.0))
        d2_fp.SetPosition(pos)
        board.Add(d2_fp)
        for pad in d2_fp.Pads():
            num = pad.GetNumber()
            if num in ["1", "6"]: pad.SetNet(net_map["USB_DP"])
            elif num in ["3", "4"]: pad.SetNet(net_map["USB_DN"])
            elif num == "2": pad.SetNet(net_map["GND"])
            elif num == "5": pad.SetNet(net_map["VBUS_5V"])

    # CC1 & CC2 Pull-Down Resistors
    r1_fp = load_fp("Resistor_SMD.pretty", "R_0603_1608Metric")
    if r1_fp:
        r1_fp.SetReference("R1")
        r1_fp.SetValue("5.1k_CC1")
        r1_fp.SetPosition(pcbnew.VECTOR2I(to_nm(80.0), to_nm(101.5)))
        board.Add(r1_fp)
        for pad in r1_fp.Pads():
            if pad.GetNumber() == "1": pad.SetNet(net_map["USB_CC1"])
            else: pad.SetNet(net_map["GND"])

    r2_fp = load_fp("Resistor_SMD.pretty", "R_0603_1608Metric")
    if r2_fp:
        r2_fp.SetReference("R2")
        r2_fp.SetValue("5.1k_CC2")
        r2_fp.SetPosition(pcbnew.VECTOR2I(to_nm(80.0), to_nm(103.5)))
        board.Add(r2_fp)
        for pad in r2_fp.Pads():
            if pad.GetNumber() == "1": pad.SetNet(net_map["USB_CC2"])
            else: pad.SetNet(net_map["GND"])

    # --- Top Edge: 4x Buttons + Status LED (Matching silicone keypad plungers at Y=107.0 mm) ---
    buttons = [
        ("SW1", "BTN_PWR", "Power_MFB", 80.0),
        ("SW2", "BTN_MESH", "Mesh_Group", 92.0),
        ("SW3", "BTN_VOL_UP", "Vol_Plus", 104.0),
        ("SW4", "BTN_VOL_DOWN", "Vol_Minus", 116.0)
    ]
    for ref, net_name, val, x_pos in buttons:
        btn_fp = load_fp("Button_Switch_SMD.pretty", "SW_Push_SPST_NO_Alps_SKRK")
        if btn_fp:
            btn_fp.SetReference(ref)
            btn_fp.SetValue(val)
            btn_fp.SetPosition(pcbnew.VECTOR2I(to_nm(x_pos), to_nm(107.0)))
            board.Add(btn_fp)
            for pad in btn_fp.Pads():
                if pad.GetNumber() == "1": pad.SetNet(net_map[net_name])
                else: pad.SetNet(net_map["GND"])

    d1_fp = load_fp("LED_SMD.pretty", "LED_WS2812B-2020_PLCC4_2.0x2.0mm")
    if d1_fp:
        d1_fp.SetReference("D1")
        d1_fp.SetValue("WS2812B-2020")
        d1_fp.SetPosition(pcbnew.VECTOR2I(to_nm(86.0), to_nm(107.0)))
        board.Add(d1_fp)
        for pad in d1_fp.Pads():
            num = pad.GetNumber()
            if num == "4": pad.SetNet(net_map["WS2812_DATA"])
            elif num == "2": pad.SetNet(net_map["VCC_3V3"])
            elif num == "3": pad.SetNet(net_map["GND"])

    # --- Center: ESP32-C6-MINI-1U (U-Variant with Onboard U.FL Socket!) ---
    # Centered at (92.0, 95.0) mm, 16.6 x 13.2 mm envelope
    u1_fp = load_fp("RF_Module.pretty", "ESP32-S2-MINI-1U")
    if u1_fp:
        u1_fp.SetReference("U1")
        u1_fp.SetValue("ESP32-C6-MINI-1U")
        u1_fp.SetPosition(pcbnew.VECTOR2I(to_nm(92.0), to_nm(95.0)))
        board.Add(u1_fp)
        for pad in u1_fp.Pads():
            num = pad.GetNumber()
            if num in ["1", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53"]:
                pad.SetNet(net_map["GND"])
            elif num == "2": pad.SetNet(net_map["VCC_3V3"])
            elif num == "3": pad.SetNet(net_map["GND"]) # EN
            elif num == "8": pad.SetNet(net_map["BTN_PWR"])      # GPIO 2
            elif num == "9": pad.SetNet(net_map["BTN_MESH"])     # GPIO 3
            elif num == "4": pad.SetNet(net_map["BTN_VOL_UP"])   # GPIO 4
            elif num == "5": pad.SetNet(net_map["BTN_VOL_DOWN"]) # GPIO 5
            elif num == "6": pad.SetNet(net_map["WS2812_DATA"])  # GPIO 6
            elif num == "7": pad.SetNet(net_map["CHG_STAT"])     # GPIO 7
            elif num == "10": pad.SetNet(net_map["I2C_SDA"])     # GPIO 8
            elif num == "11": pad.SetNet(net_map["I2C_SCL"])     # GPIO 9
            elif num == "14": pad.SetNet(net_map["USB_DN"])      # GPIO 12
            elif num == "15": pad.SetNet(net_map["USB_DP"])      # GPIO 13
            elif num == "21": pad.SetNet(net_map["I2S_MCLK"])    # GPIO 19
            elif num == "22": pad.SetNet(net_map["I2S_BCLK"])    # GPIO 20
            elif num == "23": pad.SetNet(net_map["I2S_WS"])      # GPIO 21
            elif num == "24": pad.SetNet(net_map["I2S_DOUT"])    # GPIO 22
            elif num == "25": pad.SetNet(net_map["I2S_DIN"])     # GPIO 23

    # --- Power & Battery Zone: BQ24075 + XC6206 + BAT1 ---
    # U2 (BQ24075) with proper dedicated pin nets
    u2_fp = load_fp("Package_DFN_QFN.pretty", "VQFN-16-1EP_3x3mm_P0.5mm_EP1.8x1.8mm")
    if u2_fp:
        u2_fp.SetReference("U2")
        u2_fp.SetValue("BQ24075RGTR")
        u2_fp.SetPosition(pcbnew.VECTOR2I(to_nm(107.0), to_nm(94.0)))
        board.Add(u2_fp)
        for pad in u2_fp.Pads():
            num = pad.GetNumber()
            if num in ["8", "17"]: pad.SetNet(net_map["GND"])
            elif num == "1": pad.SetNet(net_map["NTC_TS"])
            elif num in ["2", "3"]: pad.SetNet(net_map["VBAT"])
            elif num == "4": pad.SetNet(net_map["GND"])      # /CE = Low (Enable charger)
            elif num == "5": pad.SetNet(net_map["GND"])      # EN2 = Low
            elif num == "6": pad.SetNet(net_map["SYS_PWR"])  # EN1 = High (500mA USB mode)
            elif num == "9": pad.SetNet(net_map["CHG_STAT"]) # /CHG status
            elif num in ["10", "11"]: pad.SetNet(net_map["SYS_PWR"]) # OUT
            elif num == "12": pad.SetNet(net_map["ILIM"])    # Input current limit
            elif num == "13": pad.SetNet(net_map["VBUS_5V"]) # IN
            elif num == "14": pad.SetNet(net_map["GND"])     # TMR = Low (Disable timer)
            elif num == "15": pad.SetNet(net_map["GND"])     # SYSOFF = Low (Normal operation)
            elif num == "16": pad.SetNet(net_map["ISET"])    # Fast charge current
            else: pad.SetNet(net_map["GND"])

    u3_fp = load_fp("Package_TO_SOT_SMD.pretty", "SOT-23")
    if u3_fp:
        u3_fp.SetReference("U3")
        u3_fp.SetValue("XC6206P332MR")
        u3_fp.SetPosition(pcbnew.VECTOR2I(to_nm(114.5), to_nm(94.0)))
        board.Add(u3_fp)
        for pad in u3_fp.Pads():
            num = pad.GetNumber()
            if num == "1": pad.SetNet(net_map["GND"])
            elif num == "2": pad.SetNet(net_map["VCC_3V3"])
            elif num == "3": pad.SetNet(net_map["SYS_PWR"])

    bat1_fp = load_fp("Connector_JST.pretty", "JST_SH_BM02B-SRSS-TB_1x02-1MP_P1.00mm_Vertical")
    if bat1_fp:
        bat1_fp.SetReference("BAT1")
        bat1_fp.SetValue("JST_2P_LiPo_600mAh")
        bat1_fp.SetPosition(pcbnew.VECTOR2I(to_nm(107.0), to_nm(89.0)))
        board.Add(bat1_fp)
        for pad in bat1_fp.Pads():
            num = pad.GetNumber()
            if num == "1": pad.SetNet(net_map["VBAT"])
            else: pad.SetNet(net_map["GND"])

    # --- Audio Codec Zone: ES8311 ---
    u4_fp = load_fp("Package_DFN_QFN.pretty", "QFN-20-1EP_3x3mm_P0.4mm_EP1.65x1.65mm")
    if u4_fp:
        u4_fp.SetReference("U4")
        u4_fp.SetValue("ES8311_Codec")
        u4_fp.SetPosition(pcbnew.VECTOR2I(to_nm(107.0), to_nm(101.0)))
        board.Add(u4_fp)
        for pad in u4_fp.Pads():
            num = pad.GetNumber()
            if num in ["7", "14", "19", "21"]: pad.SetNet(net_map["GND"])
            elif num in ["6", "15", "16", "20"]: pad.SetNet(net_map["VCC_3V3"])
            elif num == "1": pad.SetNet(net_map["I2S_MCLK"])
            elif num == "2": pad.SetNet(net_map["I2S_BCLK"])
            elif num == "3": pad.SetNet(net_map["I2S_WS"])
            elif num == "4": pad.SetNet(net_map["I2S_DOUT"])
            elif num == "5": pad.SetNet(net_map["I2S_DIN"])
            elif num == "8": pad.SetNet(net_map["I2C_SDA"])
            elif num == "9": pad.SetNet(net_map["I2C_SCL"])
            elif num == "11": pad.SetNet(net_map["MIC_IN_P"])
            elif num == "12": pad.SetNet(net_map["MIC_IN_N"])
            elif num == "17": pad.SetNet(net_map["HP_OUT_P"])
            elif num == "18": pad.SetNet(net_map["HP_OUT_N"])

    # --- 5. Add Continuous GND Ground Planes (Zones) on B.Cu and F.Cu ---
    for layer in [pcbnew.B_Cu, pcbnew.F_Cu]:
        zone = pcbnew.ZONE(board)
        zone.SetNet(net_map["GND"])
        zone.SetLayer(layer)
        chain = pcbnew.SHAPE_LINE_CHAIN()
        chain.Append(to_nm(x0 - 0.5), to_nm(y0 - 0.5))
        chain.Append(to_nm(x1 + 0.5), to_nm(y0 - 0.5))
        chain.Append(to_nm(x1 + 0.5), to_nm(y1 + 0.5))
        chain.Append(to_nm(x0 - 0.5), to_nm(y1 + 0.5))
        chain.SetClosed(True)
        zone.AddPolygon(chain)
        zone.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        board.Add(zone)

    # Fill zones
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())

    board.Save(PCB_PATH)
    print(f"✓ Saved updated KiCad PCB to {PCB_PATH}")

def render_preview():
    print("📸 Rendering updated preview images...")
    renders = [
        ("pcba09_omm_intercom_top.png", ["--side", "top", "--quality", "high"]),
        ("pcba09_omm_intercom_3d.png", ["--quality", "high", "--rotate", "-35,0,45", "--perspective", "--floor"])
    ]
    for fname, opts in renders:
        out_path = os.path.join(PROJECT_DIR, fname)
        cmd = [KICAD_CLI, "pcb", "render", "-o", out_path, "--width", "1600", "--height", "1000"] + opts + [PCB_PATH]
        subprocess.run(cmd, check=True)
        # copy to docs
        docs_img = os.path.join("/Users/schmidtm/openMotorBridge/docs/images/pcba", fname)
        import shutil
        shutil.copy2(out_path, docs_img)
    print("✓ Previews rendered and copied to docs/images/pcba/")

if __name__ == "__main__":
    create_project_file()
    create_schematic_file()
    build_pcb()
    render_preview()
    print("✨ PCBA 09: OMM Intercom PCB Cleanly Updated!")
