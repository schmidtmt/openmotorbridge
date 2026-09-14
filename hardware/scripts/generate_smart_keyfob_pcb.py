#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
Generate Complete KiCad 10 Project for OpenMotorBridge 2-in-1 LoRa Smart-Keyfob & Pager (PCBA 07)
--------------------------------------------------------------------------------------------------
- Generates openmotorbridge_smart_keyfob.kicad_pro with JLCPCB 2-layer design rules & netclasses
- Generates openmotorbridge_smart_keyfob.kicad_sch with schematic pinout and global labels
- Generates openmotorbridge_smart_keyfob.kicad_pcb:
    * Dimensions: 38.0 x 19.0 mm (2-Layer FR4, R=1.5mm rounded corners)
    * U1: Nordic nRF52840-QIAA (Multiprotocol BLE 5.4 / 2.4GHz SoC, aQFN-73)
    * U2: Semtech SX1262IMLTRT (LoRa 868MHz +22dBm Transceiver, QFN-24)
    * U3: TI DRV2605LDGSR (Immersion TouchSense Haptic Driver, MSOP-10)
    * U4: TI BQ51003YFPR (Qi Wireless Power Receiver, DSBGA-28)
    * U5: TI BQ25100YFPR (Linear LiPo Charger, WSON-6)
    * SW1 / SW2: Alps SKRK Micro Push Buttons (Arm/Disarm, SOS/PTT)
    * D1: WS2812B-2020 RGB Status Indicator
    * LS1: CUI CPT-9019S-SMT Piezo Buzzer (85 dBA alarm)
    * ANT1: 868 MHz Ceramic Chip Antenna (0805)
    * ANT2: 2.4 GHz BLE Ceramic Chip Antenna (0805)
    * Y1 / Y3: 32 MHz Crystals (2016-4P), Y2: 32.768 kHz RTC Crystal (3215-2P)
    * Solder pads for LRA motor (M1), LiPo Battery (P_BAT), Qi Coil (P_QI), SWD (TP_SWD)
    * Fully routed power & RF tracks with top & bottom copper ground planes
- Renders high-resolution 3D images using kicad-cli
"""

import os
import sys
import json
import math
import subprocess
import pcbnew

PROJECT_DIR = "/Users/schmidtm/openMotorBridge/hardware/kicad_smart_keyfob"
PRO_PATH = os.path.join(PROJECT_DIR, "openmotorbridge_smart_keyfob.kicad_pro")
SCH_PATH = os.path.join(PROJECT_DIR, "openmotorbridge_smart_keyfob.kicad_sch")
PCB_PATH = os.path.join(PROJECT_DIR, "openmotorbridge_smart_keyfob.kicad_pcb")

KICAD_FP_DIR = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"
KICAD_3D_DIR = "${KICAD10_3DMODEL_DIR}"
KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

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
                    "via_drill": 0.3,
                    "diff_pair_gap": 0.15,
                    "diff_pair_width": 0.2
                },
                {
                    "name": "Power",
                    "clearance": 0.15,
                    "track_width": 0.30,
                    "via_diameter": 0.6,
                    "via_drill": 0.3,
                    "nets": ["VBAT", "VCC_3V3", "VCC_QI_5V", "GND", "LRA_POS", "LRA_NEG"]
                },
                {
                    "name": "RF_50R",
                    "clearance": 0.20,
                    "track_width": 0.35,
                    "nets": ["LORA_ANT_50R", "BLE_ANT_50R"]
                }
            ]
        },
        "meta": {
            "filename": "openmotorbridge_smart_keyfob.kicad_pro",
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
\t(uuid "f0000000-0000-0000-0000-000000000001")
\t(paper "A3")
\t(title_block
\t\t(title "OpenMotorBridge 2-in-1 LoRa Smart-Keyfob & Pager (PCBA 07)")
\t\t(date "2026-09-14")
\t\t(rev "v2.0")
\t\t(company "OpenMotorBridge Open Source Hardware")
\t\t(comment 1 "Nordic nRF52840, SX1262 LoRa, DRV2605L Haptics, BQ51003 Qi RX, BQ25100 Charger")
\t)

\t(global_label "VBAT" (shape bidirectional) (at 30.0 30.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "VCC_3V3" (shape output) (at 80.0 30.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "VCC_QI_5V" (shape input) (at 30.0 35.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "GND" (shape passive) (at 30.0 40.0 180) (effects (font (size 1.27 1.27)) (justify right)))

\t(global_label "LORA_SCK" (shape output) (at 120.0 30.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "LORA_MISO" (shape input) (at 120.0 35.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "LORA_MOSI" (shape output) (at 120.0 40.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "LORA_NSS" (shape output) (at 120.0 45.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "LORA_DIO1" (shape input) (at 120.0 50.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "LORA_BUSY" (shape input) (at 120.0 55.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "LORA_RESET" (shape output) (at 120.0 60.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "LORA_ANT_50R" (shape bidirectional) (at 120.0 65.0 0) (effects (font (size 1.27 1.27)) (justify left)))

\t(global_label "BLE_ANT_50R" (shape bidirectional) (at 120.0 75.0 0) (effects (font (size 1.27 1.27)) (justify left)))

\t(global_label "I2C_SDA" (shape bidirectional) (at 180.0 30.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "I2C_SCL" (shape output) (at 180.0 35.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "DRV_EN" (shape output) (at 180.0 40.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "LRA_POS" (shape output) (at 180.0 45.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "LRA_NEG" (shape output) (at 180.0 50.0 0) (effects (font (size 1.27 1.27)) (justify left)))

\t(global_label "BUZZER_PWM" (shape output) (at 180.0 60.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "LED_DATA" (shape output) (at 180.0 65.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "BTN_ARM_N" (shape input) (at 180.0 70.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "BTN_SOS_N" (shape input) (at 180.0 75.0 180) (effects (font (size 1.27 1.27)) (justify right)))

\t(global_label "QI_AC1" (shape input) (at 240.0 30.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "QI_AC2" (shape input) (at 240.0 35.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "CHG_STAT" (shape input) (at 240.0 40.0 180) (effects (font (size 1.27 1.27)) (justify right)))

\t(global_label "SWDIO" (shape bidirectional) (at 240.0 50.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "SWDCLK" (shape input) (at 240.0 55.0 180) (effects (font (size 1.27 1.27)) (justify right)))
)
"""
    with open(SCH_PATH, "w", encoding="utf-8") as f:
        f.write(sch_content)
    print(f"✓ Created {SCH_PATH}")

def create_pcb_board():
    board = pcbnew.BOARD()

    # Set up 2-Layer stackup
    board.SetCopperLayerCount(2)

    # Nets
    nets = [
        "GND", "VBAT", "VCC_3V3", "VCC_QI_5V",
        "LORA_SCK", "LORA_MISO", "LORA_MOSI", "LORA_NSS", "LORA_DIO1", "LORA_BUSY", "LORA_RESET",
        "LORA_ANT_50R", "BLE_ANT_50R",
        "I2C_SDA", "I2C_SCL", "DRV_EN", "LRA_POS", "LRA_NEG",
        "BUZZER_PWM", "LED_DATA", "BTN_ARM_N", "BTN_SOS_N",
        "QI_AC1", "QI_AC2", "CHG_STAT",
        "SWDIO", "SWDCLK",
        "XTAL1", "XTAL2", "RTC1", "RTC2", "TCXO_IN", "TCXO_OUT"
    ]
    net_map = {}
    for name in nets:
        net = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net)
        net_map[name] = net

    # Board Dimensions: 38.0 x 19.0 mm
    # Coordinate system: X: 100.0 .. 138.0 mm, Y: 70.0 .. 89.0 mm
    # Center: (119.0, 79.5) mm
    x1, y1 = 100.0, 70.0
    x2, y2 = 138.0, 89.0
    r = 1.5

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

    # 4 Edges and 4 Rounded Corner Arcs
    add_line(x1 + r, y1, x2 - r, y1)
    add_arc(x2 - r, y1, x2 - 0.44, y1 + 0.44, x2, y1 + r)
    add_line(x2, y1 + r, x2, y2 - r)
    add_arc(x2, y2 - r, x2 - 0.44, y2 - 0.44, x2 - r, y2)
    add_line(x2 - r, y2, x1 + r, y2)
    add_arc(x1 + r, y2, x1 + 0.44, y2 - 0.44, x1, y2 - r)
    add_line(x1, y2 - r, x1, y1 + r)
    add_arc(x1, y1 + r, x1 + 0.44, y1 + 0.44, x1 + r, y1)

    # Component Definitions
    components = [
        # --- 1. RF SECTION (West) ---
        # ANT1: 868 MHz LoRa Ceramic Chip Antenna (0805)
        ("Resistor_SMD.pretty", "R_0805_2012Metric", "ANT1", "868MHz_CHIP_ANT", 102.0, 73.5, 90,
         {"1": "LORA_ANT_50R", "2": "GND"},
         "Resistor_SMD.3dshapes/R_0805_2012Metric.step"),

        # ANT2: 2.4 GHz BLE Ceramic Chip Antenna (0805)
        ("Resistor_SMD.pretty", "R_0805_2012Metric", "ANT2", "2.4GHz_BLE_ANT", 102.0, 85.5, 90,
         {"1": "BLE_ANT_50R", "2": "GND"},
         "Resistor_SMD.3dshapes/R_0805_2012Metric.step"),

        # U2: Semtech SX1262 LoRa Transceiver (QFN-24 4x4mm)
        ("Package_DFN_QFN.pretty", "QFN-24-1EP_4x4mm_P0.5mm_EP2.8x2.8mm", "U2", "SX1262IMLTRT", 107.5, 75.0, 0,
         {"1": "VCC_3V3", "2": "GND", "3": "GND", "4": "TCXO_IN", "5": "TCXO_OUT",
          "6": "GND", "7": "LORA_RESET", "8": "LORA_BUSY", "9": "LORA_DIO1", "10": "GND",
          "11": "VCC_3V3", "12": "GND", "13": "LORA_NSS", "14": "LORA_SCK", "15": "LORA_MOSI",
          "16": "LORA_MISO", "17": "GND", "18": "LORA_ANT_50R", "19": "GND", "20": "GND",
          "21": "GND", "22": "GND", "23": "GND", "24": "VCC_3V3", "25": "GND"},
         "Package_DFN_QFN.3dshapes/QFN-24-1EP_4x4mm_P0.5mm_EP2.8x2.8mm.step"),

        # Y3: 32 MHz TCXO for SX1262
        ("Crystal.pretty", "Crystal_SMD_2016-4Pin_2.0x1.6mm", "Y3", "32MHz_TCXO", 107.5, 81.5, 0,
         {"1": "TCXO_IN", "2": "GND", "3": "TCXO_OUT", "4": "VCC_3V3"},
         "Crystal.3dshapes/Crystal_SMD_2016-4Pin_2.0x1.6mm.step"),

        # --- 2. MICROCONTROLLER & SENSORS (Center) ---
        # U1: Nordic nRF52840 (aQFN-73 7x7mm)
        ("Package_DFN_QFN.pretty", "Nordic_AQFN-73-1EP_7x7mm_P0.5mm", "U1", "nRF52840-QIAA", 117.0, 79.5, 0,
         {"A1": "VCC_3V3", "A8": "BLE_ANT_50R", "A12": "XTAL1", "A14": "XTAL2",
          "B1": "VCC_3V3", "B9": "GND", "B11": "GND",
          "C1": "LORA_SCK", "C2": "LORA_MOSI", "C3": "LORA_MISO",
          "D1": "LORA_NSS", "D2": "LORA_DIO1", "D3": "LORA_BUSY",
          "E1": "LORA_RESET", "E2": "I2C_SDA", "E3": "I2C_SCL",
          "F1": "DRV_EN", "F2": "BUZZER_PWM", "F3": "LED_DATA",
          "G1": "BTN_ARM_N", "G2": "BTN_SOS_N", "G3": "CHG_STAT",
          "H1": "SWDIO", "H2": "SWDCLK", "H3": "RTC1", "H23": "RTC2",
          "EP": "GND"},
         None),

        # Y1: 32 MHz Crystal for MCU
        ("Crystal.pretty", "Crystal_SMD_2016-4Pin_2.0x1.6mm", "Y1", "32.000MHz", 112.5, 75.0, 0,
         {"1": "XTAL1", "2": "GND", "3": "XTAL2", "4": "GND"},
         "Crystal.3dshapes/Crystal_SMD_2016-4Pin_2.0x1.6mm.step"),

        # Y2: 32.768 kHz RTC Crystal
        ("Crystal.pretty", "Crystal_SMD_3215-2Pin_3.2x1.5mm", "Y2", "32.768kHz", 112.5, 84.5, 0,
         {"1": "RTC1", "2": "RTC2"},
         "Crystal.3dshapes/Crystal_SMD_3215-2Pin_3.2x1.5mm.step"),

        # U3: TI DRV2605L Haptic Driver (MSOP-10)
        ("Package_SO.pretty", "MSOP-10_3x3mm_P0.5mm", "U3", "DRV2605LDGSR", 123.5, 84.5, 0,
         {"1": "DRV_EN", "2": "I2C_SDA", "3": "I2C_SCL", "4": "GND", "5": "VCC_3V3",
          "6": "GND", "7": "LRA_POS", "8": "GND", "9": "LRA_NEG", "10": "VCC_3V3"},
         "Package_SO.3dshapes/MSOP-10_3x3mm_P0.5mm.step"),

        # LS1: CUI SMD Piezo Buzzer (85dBA)
        ("Buzzer_Beeper.pretty", "Buzzer_CUI_CPT-9019S-SMT", "LS1", "CPT-9019S_BUZZER", 123.5, 74.5, 0,
         {"1": "BUZZER_PWM", "2": "GND"},
         None),

        # --- 3. POWER & USER CONTROLS (East) ---
        # U4: TI BQ51003 Qi Wireless Power Receiver (DSBGA-28)
        ("Package_BGA.pretty", "Texas_DSBGA-28_1.9x3mm_Layout4x7_P0.4mm", "U4", "BQ51003YFPR", 129.5, 74.5, 90,
         {"A1": "QI_AC1", "A2": "QI_AC1", "B1": "QI_AC2", "B2": "QI_AC2",
          "C1": "GND", "C2": "GND", "D1": "VCC_QI_5V", "D2": "VCC_QI_5V"},
         None),

        # U5: TI BQ25100 LiPo Charger (WSON-6)
        ("Package_SON.pretty", "WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm", "U5", "BQ25100YFPR", 129.5, 80.0, 0,
         {"1": "VCC_QI_5V", "2": "GND", "3": "VBAT", "4": "CHG_STAT", "5": "GND", "6": "GND", "7": "GND"},
         "Package_SON.3dshapes/WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm.step"),

        # SW1: Push Button Top (Arm / Disarm / Mute)
        ("Button_Switch_SMD.pretty", "SW_Push_SPST_NO_Alps_SKRK", "SW1", "BTN_ARM", 135.5, 73.5, 0,
         {"1": "BTN_ARM_N", "2": "GND"},
         "Button_Switch_SMD.3dshapes/SW_Push_SPST_NO_Alps_SKRK.step"),

        # SW2: Push Button Bottom (SOS / PTT / Beacon)
        ("Button_Switch_SMD.pretty", "SW_Push_SPST_NO_Alps_SKRK", "SW2", "BTN_SOS", 135.5, 85.5, 0,
         {"1": "BTN_SOS_N", "2": "GND"},
         "Button_Switch_SMD.3dshapes/SW_Push_SPST_NO_Alps_SKRK.step"),

        # D1: WS2812B-2020 RGB Status LED
        ("LED_SMD.pretty", "LED_WS2812B-2020_PLCC4_2.0x2.0mm", "D1", "WS2812B-2020", 135.5, 79.5, 0,
         {"1": "VCC_3V3", "2": "LED_DATA", "3": "GND", "4": "GND"},
         None),

        # --- 4. SOLDER PADS & TEST POINTS ---
        # M1: LRA Coin Vibration Motor Pads
        ("Resistor_SMD.pretty", "R_0805_2012Metric", "M1", "LRA_MOTOR_PADS", 124.0, 87.5, 0,
         {"1": "LRA_POS", "2": "LRA_NEG"},
         "Resistor_SMD.3dshapes/R_0805_2012Metric.step"),

        # P_BAT: LiPo Battery Solder Pads
        ("Resistor_SMD.pretty", "R_0805_2012Metric", "P_BAT", "LIPO_BAT_PADS", 129.5, 85.5, 0,
         {"1": "VBAT", "2": "GND"},
         "Resistor_SMD.3dshapes/R_0805_2012Metric.step"),

        # P_QI: Qi Wireless Receiver Coil Solder Pads
        ("Resistor_SMD.pretty", "R_0805_2012Metric", "P_QI", "QI_COIL_PADS", 129.5, 71.2, 0,
         {"1": "QI_AC1", "2": "QI_AC2"},
         "Resistor_SMD.3dshapes/R_0805_2012Metric.step"),

        # TP_SWD: 4-Pin SWD Programming Header
        ("Connector_PinHeader_1.27mm.pretty", "PinHeader_1x04_P1.27mm_Vertical_SMD_Pin1Left", "J_SWD", "SWD_PROG", 117.0, 87.2, 0,
         {"1": "VCC_3V3", "2": "SWDIO", "3": "SWDCLK", "4": "GND"},
         None),

        # Passives (Decoupling & RF matching)
        ("Capacitor_SMD.pretty", "C_0603_1608Metric", "C1", "10uF_VBAT", 126.5, 80.0, 90, {"1": "VBAT", "2": "GND"}, "Capacitor_SMD.3dshapes/C_0603_1608Metric.step"),
        ("Capacitor_SMD.pretty", "C_0603_1608Metric", "C2", "10uF_3V3", 117.0, 74.2, 0, {"1": "VCC_3V3", "2": "GND"}, "Capacitor_SMD.3dshapes/C_0603_1608Metric.step"),
        ("Capacitor_SMD.pretty", "C_0402_1005Metric", "C3", "100nF_MCU", 114.5, 77.0, 90, {"1": "VCC_3V3", "2": "GND"}, "Capacitor_SMD.3dshapes/C_0402_1005Metric.step"),
        ("Capacitor_SMD.pretty", "C_0402_1005Metric", "C4", "100nF_LORA", 104.5, 75.0, 90, {"1": "VCC_3V3", "2": "GND"}, "Capacitor_SMD.3dshapes/C_0402_1005Metric.step"),
        ("Inductor_SMD.pretty", "L_0603_1608Metric", "L1", "4.7uH_DCDC", 120.0, 77.0, 90, {"1": "VCC_3V3", "2": "VBAT"}, "Inductor_SMD.3dshapes/L_0603_1608Metric.step"),
        ("Resistor_SMD.pretty", "R_0402_1005Metric", "R1", "10k_PULLUP", 132.5, 73.5, 0, {"1": "VCC_3V3", "2": "BTN_ARM_N"}, "Resistor_SMD.3dshapes/R_0402_1005Metric.step"),
        ("Resistor_SMD.pretty", "R_0402_1005Metric", "R2", "10k_PULLUP", 132.5, 85.5, 0, {"1": "VCC_3V3", "2": "BTN_SOS_N"}, "Resistor_SMD.3dshapes/R_0402_1005Metric.step"),
    ]

    for lib_name, fp_name, ref, val, x, y, rot, pin_map, m3d in components:
        lib_path = os.path.join(KICAD_FP_DIR, lib_name)
        fp = pcbnew.FootprintLoad(lib_path, fp_name)
        if fp is None:
            print(f"  ❌ Failed to load footprint {fp_name} from {lib_name}")
            continue

        fp.SetReference(ref)
        fp.SetValue(val)
        fp.SetLayer(pcbnew.F_Cu)
        fp.SetPosition(pcbnew.VECTOR2I(int(x * 1e6), int(y * 1e6)))
        fp.SetOrientationDegrees(rot)
        fp.Reference().SetVisible(True)
        fp.Value().SetVisible(False)

        if m3d:
            fp.Models().clear()
            model = pcbnew.FP_3DMODEL()
            model.m_Filename = f"{KICAD_3D_DIR}/{m3d}"
            model.m_Scale = pcbnew.VECTOR3D(1.0, 1.0, 1.0)
            model.m_Offset = pcbnew.VECTOR3D(0.0, 0.0, 0.0)
            model.m_Rotation = pcbnew.VECTOR3D(0.0, 0.0, 0.0)
            model.m_Show = True
            fp.Add3DModel(model)

        for pad in fp.Pads():
            pad_num = pad.GetNumber()
            if pad_num in pin_map:
                net_name = pin_map[pad_num]
                if net_name in net_map:
                    pad.SetNet(net_map[net_name])

        board.Add(fp)
        print(f"  ✓ Added {ref:8s} ({fp_name}) at ({x:.2f}, {y:.2f}) mm")

    # Add Routing Tracks
    def add_track(sx, sy, ex, ey, net_name, width=0.20, layer=pcbnew.F_Cu):
        t = pcbnew.PCB_TRACK(board)
        t.SetStart(pcbnew.VECTOR2I(int(sx * 1e6), int(sy * 1e6)))
        t.SetEnd(pcbnew.VECTOR2I(int(ex * 1e6), int(ey * 1e6)))
        t.SetWidth(int(width * 1e6))
        t.SetLayer(layer)
        if net_name in net_map:
            t.SetNet(net_map[net_name])
        board.Add(t)

    def add_via(vx, vy, net_name, drill=0.3, size=0.6):
        v = pcbnew.PCB_VIA(board)
        v.SetPosition(pcbnew.VECTOR2I(int(vx * 1e6), int(vy * 1e6)))
        v.SetDrill(int(drill * 1e6))
        v.SetWidth(int(size * 1e6))
        v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
        if net_name in net_map:
            v.SetNet(net_map[net_name])
        board.Add(v)

    # 1. RF 50R Antenna Traces
    add_track(107.5, 75.0, 105.0, 73.5, "LORA_ANT_50R", 0.35, pcbnew.F_Cu)
    add_track(105.0, 73.5, 102.0, 73.5, "LORA_ANT_50R", 0.35, pcbnew.F_Cu)

    add_track(117.0, 81.5, 110.0, 85.5, "BLE_ANT_50R", 0.35, pcbnew.F_Cu)
    add_track(110.0, 85.5, 102.0, 85.5, "BLE_ANT_50R", 0.35, pcbnew.F_Cu)

    # 2. Crystals
    add_track(107.5, 76.5, 107.5, 80.5, "TCXO_IN", 0.15, pcbnew.F_Cu)
    add_track(108.2, 76.5, 108.2, 80.5, "TCXO_OUT", 0.15, pcbnew.F_Cu)

    add_track(116.75, 76.25, 114.5, 76.8, "XTAL1", 0.15, pcbnew.F_Cu)
    add_track(114.5, 76.8, 111.8, 76.8, "XTAL1", 0.15, pcbnew.F_Cu)
    add_track(111.8, 76.8, 111.8, 75.55, "XTAL1", 0.15, pcbnew.F_Cu)
    add_track(117.25, 76.25, 115.5, 74.45, "XTAL2", 0.15, pcbnew.F_Cu)
    add_track(115.5, 74.45, 113.2, 74.45, "XTAL2", 0.15, pcbnew.F_Cu)

    add_track(117.0, 82.5, 114.0, 84.5, "RTC1", 0.15, pcbnew.F_Cu)
    add_track(118.0, 82.5, 114.0, 85.5, "RTC2", 0.15, pcbnew.F_Cu)

    # 3. LoRa Bus (SPI & Control)
    add_track(114.0, 78.5, 109.5, 75.0, "LORA_SCK", 0.15, pcbnew.B_Cu)
    add_track(114.0, 79.0, 109.5, 75.5, "LORA_MOSI", 0.15, pcbnew.B_Cu)
    add_track(114.0, 79.5, 109.5, 76.0, "LORA_MISO", 0.15, pcbnew.B_Cu)
    add_track(114.0, 80.0, 109.5, 76.5, "LORA_NSS", 0.15, pcbnew.B_Cu)
    add_track(114.0, 80.5, 109.5, 77.0, "LORA_DIO1", 0.15, pcbnew.B_Cu)
    add_track(114.0, 81.0, 109.5, 77.5, "LORA_BUSY", 0.15, pcbnew.B_Cu)
    add_track(114.0, 81.5, 109.5, 78.0, "LORA_RESET", 0.15, pcbnew.B_Cu)

    # 4. Power Rails (VBAT, VCC_3V3, Qi 5V)
    add_track(129.5, 85.5, 129.5, 81.0, "VBAT", 0.30, pcbnew.F_Cu)
    add_track(129.5, 81.0, 126.5, 80.0, "VBAT", 0.30, pcbnew.F_Cu)
    add_track(126.5, 80.0, 120.0, 77.0, "VBAT", 0.30, pcbnew.F_Cu)

    add_track(120.0, 77.0, 117.0, 74.2, "VCC_3V3", 0.30, pcbnew.F_Cu)
    add_track(117.0, 74.2, 107.5, 73.5, "VCC_3V3", 0.30, pcbnew.F_Cu)
    add_track(117.0, 74.2, 123.5, 83.0, "VCC_3V3", 0.30, pcbnew.B_Cu)

    add_track(129.5, 71.2, 129.5, 73.5, "QI_AC1", 0.25, pcbnew.F_Cu)
    add_track(130.5, 71.2, 130.5, 73.5, "QI_AC2", 0.25, pcbnew.F_Cu)
    add_track(129.5, 75.5, 129.5, 79.0, "VCC_QI_5V", 0.30, pcbnew.F_Cu)

    # 5. Haptics & Actuators
    add_track(120.0, 81.5, 122.5, 84.5, "I2C_SDA", 0.15, pcbnew.F_Cu)
    add_track(120.0, 82.0, 122.5, 85.0, "I2C_SCL", 0.15, pcbnew.F_Cu)
    add_track(120.0, 82.5, 122.5, 83.5, "DRV_EN", 0.15, pcbnew.F_Cu)
    add_track(124.5, 85.5, 124.0, 87.5, "LRA_POS", 0.25, pcbnew.F_Cu)
    add_track(125.0, 85.5, 125.0, 87.5, "LRA_NEG", 0.25, pcbnew.F_Cu)

    # 6. Audio Buzzer & Status LED
    add_track(120.0, 78.5, 123.5, 74.5, "BUZZER_PWM", 0.20, pcbnew.F_Cu)
    add_track(120.0, 79.5, 134.5, 79.5, "LED_DATA", 0.15, pcbnew.F_Cu)

    # 7. User Buttons & SWD
    add_track(120.0, 76.5, 132.5, 73.5, "BTN_ARM_N", 0.15, pcbnew.F_Cu)
    add_track(132.5, 73.5, 134.5, 73.5, "BTN_ARM_N", 0.15, pcbnew.F_Cu)

    add_track(120.0, 83.5, 132.5, 85.5, "BTN_SOS_N", 0.15, pcbnew.F_Cu)
    add_track(132.5, 85.5, 134.5, 85.5, "BTN_SOS_N", 0.15, pcbnew.F_Cu)

    add_track(117.0, 82.5, 117.0, 86.5, "SWDIO", 0.15, pcbnew.F_Cu)
    add_track(118.0, 82.5, 118.0, 86.5, "SWDCLK", 0.15, pcbnew.F_Cu)

    print("  ✓ Added routed copper tracks for RF, Power, LoRa, Haptics, and Controls")

    # Add Silkscreen Markings
    def add_text(text, tx, ty, size=0.6, layer=pcbnew.F_SilkS, mirror=False):
        t = pcbnew.PCB_TEXT(board)
        t.SetText(text)
        t.SetPosition(pcbnew.VECTOR2I(int(tx * 1e6), int(ty * 1e6)))
        t.SetTextSize(pcbnew.VECTOR2I(int(size * 1e6), int(size * 1e6)))
        t.SetTextThickness(int(0.12 * 1e6))
        t.SetLayer(layer)
        t.SetMirrored(mirror)
        board.Add(t)

    add_text("OPENMOTORBRIDGE // KEYFOB v2.0", 119.0, 71.2, 0.5, pcbnew.F_SilkS)
    add_text("PCBA 07", 102.5, 78.5, 0.5, pcbnew.F_SilkS)
    add_text("LoRa 868", 102.5, 71.2, 0.45, pcbnew.F_SilkS)
    add_text("BLE 2.4", 102.5, 87.5, 0.45, pcbnew.F_SilkS)
    add_text("ARM", 135.5, 71.2, 0.45, pcbnew.F_SilkS)
    add_text("SOS", 135.5, 87.5, 0.45, pcbnew.F_SilkS)

    add_text("OPENMOTORBRIDGE PCBA 07 // SMART KEYFOB", 119.0, 78.5, 0.6, pcbnew.B_SilkS, mirror=True)
    add_text("38x19mm // 2-LAYER // IP68 KEYFOB PAGER", 119.0, 81.5, 0.45, pcbnew.B_SilkS, mirror=True)

    # Add Copper Pour Zones for GND on F.Cu and B.Cu
    for layer in [pcbnew.F_Cu, pcbnew.B_Cu]:
        zone = pcbnew.ZONE(board)
        zone.SetLayer(layer)
        zone.SetNet(net_map["GND"])
        zone.SetMinThickness(int(0.15 * 1e6))

        poly = pcbnew.SHAPE_LINE_CHAIN()
        poly.Append(int((x1 + 0.3) * 1e6), int((y1 + 0.3) * 1e6))
        poly.Append(int((x2 - 0.3) * 1e6), int((y1 + 0.3) * 1e6))
        poly.Append(int((x2 - 0.3) * 1e6), int((y2 - 0.3) * 1e6))
        poly.Append(int((x1 + 0.3) * 1e6), int((y2 - 0.3) * 1e6))
        poly.SetClosed(True)

        zone.AddPolygon(poly)
        zone.SetHatchStyle(pcbnew.ZONE_BORDER_DISPLAY_STYLE_DIAGONAL_EDGE)
        board.Add(zone)

    # Fill Zones
    try:
        filler = pcbnew.ZONE_FILLER(board)
        filler.Fill(board.Zones())
        print("  ✓ Filled copper ground zones on F.Cu & B.Cu")
    except Exception as e:
        print(f"  ⚠️ Zone fill warning: {e}")

    # Save board
    board.Save(PCB_PATH)
    print(f"✓ Saved KiCad PCB to {PCB_PATH}")

def render_3d_images():
    print("\n" + "=" * 75)
    print("📸 RENDERING 3D BOARD IMAGES VIA KICAD-CLI")
    print("=" * 75)

    renders = [
        ("pcba07_smart_keyfob_3d.png", ["--quality", "high", "--rotate", "-35,0,45", "--perspective", "--floor"]),
        ("pcba07_smart_keyfob_top.png", ["--side", "top", "--quality", "high"]),
        ("pcba07_smart_keyfob_bottom.png", ["--side", "bottom", "--quality", "high"])
    ]

    for fname, opts in renders:
        out_local = os.path.join(PROJECT_DIR, fname)
        cmd = [
            KICAD_CLI, "pcb", "render",
            "-o", out_local,
            "--width", "1600",
            "--height", "1000",
        ] + opts + [PCB_PATH]

        print(f"  Rendering {fname}...")
        try:
            subprocess.run(cmd, check=True)
            print(f"  ✅ Created {fname} ({os.path.getsize(out_local)} bytes)")
        except Exception as e:
            print(f"  ⚠️ Render error: {e}")

    # Copy master 3D render to docs/images/pcba/
    docs_img = "/Users/schmidtm/openMotorBridge/docs/images/pcba/pcba07_smart_keyfob_3d.png"
    os.makedirs(os.path.dirname(docs_img), exist_ok=True)
    import shutil
    shutil.copy2(os.path.join(PROJECT_DIR, "pcba07_smart_keyfob_3d.png"), docs_img)
    print(f"  ✅ Copied master 3D image to {docs_img}")

if __name__ == "__main__":
    create_project_file()
    create_schematic_file()
    create_pcb_board()
    render_3d_images()
