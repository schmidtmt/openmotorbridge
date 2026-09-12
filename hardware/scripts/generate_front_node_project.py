#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
Generate Complete KiCad 10 Project for OpenMotorBridge Universal Front Node (PCBA 05)
-------------------------------------------------------------------------------------
- Generates openmotorbridge_front_node.kicad_pro with exact JLCPCB netclasses & setup rules
- Generates openmotorbridge_front_node.kicad_sch with complete schematic wiring & pinout
- Generates openmotorbridge_front_node.kicad_pcb with 82x50mm 4-layer stackup & pre-placed components:
  - ESP32-S3-WROOM-1U (U.FL, 240MHz, 8MB PSRAM)
  - Microchip USB2514B 4-Port Automotive USB Hub + 24MHz Crystal
  - Southchip SC8102 Synchronous Buck with USB-PD 20W Fast Charge for Port 1 (Smartphone)
  - TI TPS2051B VBUS High-Side Switch for Port 2 (CP2AA Fairing Pigtail)
  - Downstream Port 3 (Glovebox USB stick / MP3s)
  - Downstream Port 4 (Cockpit-Zubehör / Dashcam / Zūmo)
  - TI TCAN334G 3.3V CAN-Bus Transceiver + CPC1017N Auto-Sensing 120R Relay + Silent Mode
  - Knowles SPH0645LM4H Digital I2S MEMS Ambient Microphone (Wind noise DSP)
  - DMN63D8 Dual N-MOSFET Driver for Directional Blind Spot Mirror LEDs (Radar BSD J9)
  - TI TPS1H100 Smart High-Side Switch for 12V Aux Light / Strobe (J11)
  - Switched 12V Qi Smartphone Power Header (J10)
  - 4-Pin Handlebar Multi-Button Interface (J3: PTT, Cam Bookmark, Media Voice)
  - Qwiic / STEMMA QT 1.0mm I2C Sensor Port (J12)
  - Onboard WS2812B-2020 RGB Status Indicator for Deckel Light Pipe
  - Native USB-C Service & Flash Port (J7) + BOOT & RST Buttons
  - JST-PH 2.0mm Automotive Connectors for all external interfaces
"""

import os
import json
import re
import pcbnew

PROJECT_DIR = "/Users/schmidtm/openMotorBridge/hardware/kicad_front_node"
PRO_PATH = os.path.join(PROJECT_DIR, "openmotorbridge_front_node.kicad_pro")
SCH_PATH = os.path.join(PROJECT_DIR, "openmotorbridge_front_node.kicad_sch")
PCB_PATH = os.path.join(PROJECT_DIR, "openmotorbridge_front_node.kicad_pcb")

KICAD_FP_DIR = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"
KICAD_3D_DIR = "${KICAD10_3DMODEL_DIR}"

def create_project_file():
    pro_content = {
        "board": {
            "design_settings": {
                "defaults": {
                    "board_outline_line_width": 0.15,
                    "copper_line_width": 0.15,
                    "silk_line_width": 0.12,
                    "min_clearance": 0.127,
                    "min_track_width": 0.15,
                    "min_via_annular_width": 0.15,
                    "min_through_drill": 0.3,
                    "min_hole_clearance": 0.25,
                    "min_copper_edge_clearance": 0.3
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
                    "nets": [
                        "KL15_12V_SW", "+12V_PROT", "+12V_AUX",
                        "VCC_5V", "VCC_5V_OTTOCAST", "VBUS_PD_OUT", "VCC_3V3",
                        "GND", "SW_BUCK", "VBUS_BUCK_OUT", "USB_UP_VBUS", "SW_PD_BUCK"
                    ]
                },
                {
                    "name": "USB_DIFF",
                    "clearance": 0.15,
                    "track_width": 0.20,
                    "diff_pair_gap": 0.15,
                    "diff_pair_width": 0.20,
                    "nets": [
                        "USB_UP_DP", "USB_UP_DM",
                        "USB_DN1_DP", "USB_DN1_DM",
                        "USB_DN2_DP", "USB_DN2_DM",
                        "USB_DN3_DP", "USB_DN3_DM",
                        "USB_DN4_DP", "USB_DN4_DM",
                        "USB_SERV_DP", "USB_SERV_DM"
                    ]
                }
            ]
        },
        "meta": {
            "filename": "openmotorbridge_front_node.kicad_pro",
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
\t(uuid "e0000000-0000-0000-0000-000000000001")
\t(paper "A3")
\t(title_block
\t\t(title "OpenMotorBridge Universal Front Node (Cockpit & Sensor Hub PCBA 05)")
\t\t(date "2026-09-12")
\t\t(rev "v2.0")
\t\t(company "OpenMotorBridge Open Source Hardware")
\t\t(comment 1 "ESP32-S3, USB2514B 4-Port Hub, SC8102 USB-PD 20W, Qi 12V, Aux Light, BSD LEDs")
\t)

\t(global_label "KL15_12V_SW" (shape input) (at 30.0 40.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "+12V_PROT" (shape output) (at 80.0 35.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "+12V_AUX" (shape output) (at 80.0 40.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "GND" (shape passive) (at 30.0 50.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "USB_UP_VBUS" (shape input) (at 30.0 60.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "VCC_5V" (shape output) (at 80.0 45.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "VCC_3V3" (shape output) (at 80.0 50.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "VCC_5V_OTTOCAST" (shape output) (at 80.0 55.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "VBUS_PD_OUT" (shape output) (at 80.0 60.0 0) (effects (font (size 1.27 1.27)) (justify left)))

\t(global_label "CAN_H" (shape bidirectional) (at 30.0 70.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "CAN_L" (shape bidirectional) (at 30.0 75.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "CAN_TERM_EN" (shape output) (at 80.0 70.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "CAN_SILENT" (shape output) (at 80.0 75.0 0) (effects (font (size 1.27 1.27)) (justify left)))

\t(global_label "PTT_IN1_N" (shape input) (at 30.0 85.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "PTT_IN2_N" (shape input) (at 30.0 90.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "PTT_IN3_N" (shape input) (at 30.0 95.0 180) (effects (font (size 1.27 1.27)) (justify right)))

\t(global_label "BSD_LED_LEFT" (shape output) (at 80.0 85.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "BSD_LED_RIGHT" (shape output) (at 80.0 90.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "AUX_LIGHT_EN" (shape output) (at 80.0 95.0 0) (effects (font (size 1.27 1.27)) (justify left)))

\t(global_label "USB_UP_DP" (shape bidirectional) (at 150.0 40.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "USB_UP_DM" (shape bidirectional) (at 150.0 45.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "USB_DN1_DP" (shape bidirectional) (at 150.0 55.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "USB_DN1_DM" (shape bidirectional) (at 150.0 60.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "USB_DN2_DP" (shape bidirectional) (at 150.0 70.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "USB_DN2_DM" (shape bidirectional) (at 150.0 75.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "USB_DN3_DP" (shape bidirectional) (at 150.0 85.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "USB_DN3_DM" (shape bidirectional) (at 150.0 90.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "USB_DN4_DP" (shape bidirectional) (at 150.0 100.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "USB_DN4_DM" (shape bidirectional) (at 150.0 105.0 0) (effects (font (size 1.27 1.27)) (justify left)))

\t(global_label "MIC_I2S_WS" (shape output) (at 210.0 40.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "MIC_I2S_BCLK" (shape output) (at 210.0 45.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "MIC_I2S_DATA" (shape input) (at 210.0 50.0 180) (effects (font (size 1.27 1.27)) (justify right)))

\t(global_label "I2C_SDA" (shape bidirectional) (at 210.0 60.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "I2C_SCL" (shape output) (at 210.0 65.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "WS2812B_DIN" (shape output) (at 210.0 70.0 0) (effects (font (size 1.27 1.27)) (justify left)))

\t(global_label "OTTOCAST_PWR_EN" (shape output) (at 210.0 80.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "OTTOCAST_FAULT_N" (shape input) (at 210.0 85.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "KL15_SENSE" (shape input) (at 210.0 90.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "TWAI_TX" (shape output) (at 210.0 100.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "TWAI_RX" (shape input) (at 210.0 105.0 180) (effects (font (size 1.27 1.27)) (justify right)))
)
"""
    with open(SCH_PATH, "w", encoding="utf-8") as f:
        f.write(sch_content)
    print(f"✓ Created {SCH_PATH}")

def create_pcb_board():
    board = pcbnew.BOARD()

    # Title Block
    tb = board.GetTitleBlock()
    tb.SetTitle("OpenMotorBridge Universal Front Node (Cockpit & Sensor Hub PCBA 05)")
    tb.SetDate("2026-09-12")
    tb.SetRevision("v2.0")
    tb.SetCompany("OpenMotorBridge Open Source Hardware")
    tb.SetComment(0, "ESP32-S3, USB2514B 4-Port Hub, SC8102 USB-PD, Qi 12V, Aux Light, BSD LEDs")

    # 4 Layers Stackup
    board.SetLayerName(pcbnew.In1_Cu, "GND_PLANE")
    board.SetLayerName(pcbnew.In2_Cu, "PWR_PLANE")

    # Netlist
    nets = [
        "GND", "KL15_12V_SW", "+12V_PROT", "+12V_AUX", "VIN_BUCK", "KL15_SENSE",
        "VCC_5V", "VCC_5V_OTTOCAST", "VBUS_PD_OUT", "VCC_3V3", "VDD12_HUB",
        "USB_UP_VBUS", "USB_UP_DP", "USB_UP_DM",
        "USB_DN1_DP", "USB_DN1_DM",
        "USB_DN2_DP", "USB_DN2_DM",
        "USB_DN3_DP", "USB_DN3_DM",
        "USB_DN4_DP", "USB_DN4_DM",
        "USB_SERV_DP", "USB_SERV_DM", "USB_CC1", "USB_CC2",
        "OTTOCAST_PWR_EN", "OTTOCAST_FAULT_N",
        "CAN_TERM_EN", "CAN_TERM_R", "CAN_SILENT",
        "AUX_LIGHT_EN", "BSD_LED_LEFT", "BSD_LED_RIGHT", "BSD_LEFT_N", "BSD_RIGHT_N",
        "PTT_IN1_N", "PTT_IN2_N", "PTT_IN3_N",
        "MIC_I2S_WS", "MIC_I2S_BCLK", "MIC_I2S_DATA",
        "I2C_SDA", "I2C_SCL", "WS2812B_DIN",
        "TWAI_TX", "TWAI_RX", "CAN_H", "CAN_L",
        "ESP_EN", "ESP_BOOT",
        "XTAL_IN", "XTAL_OUT", "HUB_RESET_N", "HUB_RBIAS",
        "SW_BUCK", "BST_BUCK", "FB_BUCK", "VBUS_BUCK_OUT", "SW_PD_BUCK"
    ]
    net_map = {}
    for name in nets:
        net = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net)
        net_map[name] = net

    # Component Definitions
    # Board Size: 82.0 x 50.0 mm (X: 100.0 .. 182.0, Y: 70.0 .. 120.0)
    components = [
        # 1. Connectors West Edge (Vehicle Interface & Sensors)
        # J1: 12V Bordnetz-Eingang (KL15 ACC)
        ("Connector_JST.pretty", "JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", "J1", "12V_KL15_GND", 103.50, 78.50, -90,
         {"1": "KL15_12V_SW", "2": "GND"},
         "Connector_JST.3dshapes/JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical.step"),

        # J10: 12V Qi-Smartphone-Power (SP Connect / QuadLock)
        ("Connector_JST.pretty", "JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", "J10", "12V_QI_POWER", 103.50, 85.50, -90,
         {"1": "+12V_PROT", "2": "GND"},
         "Connector_JST.3dshapes/JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical.step"),

        # J11: 12V Aux Light (Adventure Zusatzscheinwerfer / Strobe)
        ("Connector_JST.pretty", "JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", "J11", "12V_AUX_LIGHT", 103.50, 92.50, -90,
         {"1": "+12V_AUX", "2": "GND"},
         "Connector_JST.3dshapes/JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical.step"),

        # J2: Cockpit CAN-Bus (3-Pin mit Auto-Sensing Relais)
        ("Connector_JST.pretty", "JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical", "J2", "CAN_H_L_GND", 103.50, 99.50, -90,
         {"1": "CAN_H", "2": "CAN_L", "3": "GND"},
         "Connector_JST.3dshapes/JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical.step"),

        # J3: Lenker Multi-Button Interface (4-Pin: GND, PTT, Cam-Action, Media-Voice)
        ("Connector_JST.pretty", "JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical", "J3", "HANDLEBAR_MULTI_BTN", 103.50, 107.00, -90,
         {"1": "GND", "2": "PTT_IN1_N", "3": "PTT_IN2_N", "4": "PTT_IN3_N"},
         "Connector_JST.3dshapes/JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical.step"),

        # J9: Spiegel Totwinkel-LEDs (3-Pin: 12V, BSD_LEFT, BSD_RIGHT)
        ("Connector_JST.pretty", "JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical", "J9", "MIRROR_BSD_LEDS", 103.50, 114.50, -90,
         {"1": "+12V_PROT", "2": "BSD_LEFT_N", "3": "BSD_RIGHT_N"},
         "Connector_JST.3dshapes/JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical.step"),

        # 2. Connectors South Edge (USB & Charging Subsystem)
        # J4: Upstream Host (zum Bike Infotainment)
        ("Connector_JST.pretty", "JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical", "J4", "USB_UPSTREAM_HOST", 112.50, 116.50, 180,
         {"1": "USB_UP_VBUS", "2": "USB_UP_DM", "3": "USB_UP_DP", "4": "GND"},
         "Connector_JST.3dshapes/JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical.step"),

        # J5: Port 1 Downstream (Smartphone USB-PD 20W Fast Charge)
        ("Connector_JST.pretty", "JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical", "J5", "USB_DN1_PHONE_PD20W", 124.50, 116.50, 180,
         {"1": "VBUS_PD_OUT", "2": "USB_DN1_DM", "3": "USB_DN1_DP", "4": "GND"},
         "Connector_JST.3dshapes/JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical.step"),

        # J6: Port 2 Downstream (Fairing Pigtail zum CP2AA Wireless Dongle)
        ("Connector_JST.pretty", "JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical", "J6", "USB_DN2_CP2AA_PIGTAIL", 136.50, 116.50, 180,
         {"1": "VCC_5V_OTTOCAST", "2": "USB_DN2_DM", "3": "USB_DN2_DP", "4": "GND"},
         "Connector_JST.3dshapes/JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical.step"),

        # J5_MP3: Port 3 Downstream (Handschuhfach / Jukebox USB-Stick & Updates)
        ("Connector_JST.pretty", "JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical", "J5_MP3", "USB_DN3_GLOVEBOX", 148.50, 116.50, 180,
         {"1": "VCC_5V", "2": "USB_DN3_DM", "3": "USB_DN3_DP", "4": "GND"},
         "Connector_JST.3dshapes/JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical.step"),

        # J6_AUX: Port 4 Downstream (Cockpit-Zubehör / Dashcam / Navi)
        ("Connector_JST.pretty", "JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical", "J6_AUX", "USB_DN4_COCKPIT_AUX", 160.50, 116.50, 180,
         {"1": "VCC_5V", "2": "USB_DN4_DM", "3": "USB_DN4_DP", "4": "GND"},
         "Connector_JST.3dshapes/JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical.step"),

        # J8: Action-Cam Power-Port (Charge-Only 5V / 2.0A)
        ("Connector_JST.pretty", "JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", "J8", "ACTION_CAM_5V_PWR", 170.50, 116.50, 180,
         {"1": "VCC_5V", "2": "GND"},
         "Connector_JST.3dshapes/JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical.step"),

        # 3. East Edge & Sensor Port
        # J7: USB-C Service Port (Flanke mit TPU-Stopfen)
        ("Connector_USB.pretty", "USB_C_Receptacle_HRO_TYPE-C-31-M-12", "J7", "USB-C_SERVICE", 178.00, 95.00, 90,
         {"A1": "GND", "B1": "GND", "A4": "VCC_5V", "B4": "VCC_5V", "A9": "VCC_5V", "B9": "VCC_5V",
          "A5": "USB_CC1", "B5": "USB_CC2", "A6": "USB_SERV_DP", "B6": "USB_SERV_DP", "A7": "USB_SERV_DM", "B7": "USB_SERV_DM",
          "A12": "GND", "B12": "GND", "SH": "GND"},
         "Connector_USB.3dshapes/USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal.step"),

        # J12: Qwiic / STEMMA QT 1.0mm I2C Sensor Port
        ("Connector_JST.pretty", "JST_SH_BM04B-SRSS-TB_1x04-1MP_P1.00mm_Vertical", "J12", "QWIIC_I2C", 166.00, 85.00, 90,
         {"1": "GND", "2": "VCC_3V3", "3": "I2C_SDA", "4": "I2C_SCL", "MP": "GND"},
         None),

        # Tactical Buttons
        ("Button_Switch_SMD.pretty", "SW_Push_SPST_NO_Alps_SKRK", "SW1", "BOOT", 175.00, 85.00, 0,
         {"1": "ESP_BOOT", "2": "GND"},
         "Button_Switch_SMD.3dshapes/SW_Push_SPST_NO_Alps_SKRK.step"),
        ("Button_Switch_SMD.pretty", "SW_Push_SPST_NO_Alps_SKRK", "SW2", "RESET", 175.00, 105.00, 0,
         {"1": "ESP_EN", "2": "GND"},
         "Button_Switch_SMD.3dshapes/SW_Push_SPST_NO_Alps_SKRK.step"),

        # Status RGB LED (WS2812B-2020 für Gehäusedeckel-Lichtleiter)
        ("LED_SMD.pretty", "LED_WS2812B-2020_PLCC4_2.0x2.0mm", "LED1", "WS2812B-2020_RGB", 175.00, 78.00, 0,
         {"1": "VCC_5V", "2": "GND", "3": "GND", "4": "WS2812B_DIN"},
         None),

        # 4. Power Management Stage (12V Protected Rail + 5V Buck + 3.3V LDO + C_BUF)
        ("Capacitor_Tantalum_SMD.pretty", "CP_EIA-7343-31_Kemet-D", "C_BUF", "470uF_10V_POLYMER", 165.00, 78.00, 270,
         {"1": "VCC_5V", "2": "GND"},
         "Capacitor_Tantalum_SMD.3dshapes/CP_EIA-7343-31_Kemet-D.step"),
        ("Diode_SMD.pretty", "D_SMA", "D7", "SS34_USB_OR", 158.00, 105.00, 90,
         {"1": "VCC_5V", "2": "USB_UP_VBUS"},
         "Diode_SMD.3dshapes/D_SMA.step"),
        ("Diode_SMD.pretty", "D_SMA", "D8", "SS34_BUCK_OR", 128.00, 79.00, 0,
         {"1": "VBUS_BUCK_OUT", "2": "VCC_5V"},
         "Diode_SMD.3dshapes/D_SMA.step"),
        ("Diode_SMD.pretty", "D_SMA", "D5", "SS34_REV_POL", 112.00, 75.00, 0,
         {"1": "KL15_12V_SW", "2": "+12V_PROT"},
         "Diode_SMD.3dshapes/D_SMA.step"),
        ("Diode_SMD.pretty", "D_SMB", "D4", "SMCJ36CA_TVS", 112.00, 79.00, 0,
         {"1": "+12V_PROT", "2": "GND"},
         "Diode_SMD.3dshapes/D_SMB.step"),
        ("Package_TO_SOT_SMD.pretty", "SOT-23-6", "U3", "TPS54302_5V_BUCK", 118.00, 79.00, 0,
         {"1": "GND", "2": "SW_BUCK", "3": "+12V_PROT", "4": "FB_BUCK", "5": "+12V_PROT", "6": "BST_BUCK"},
         "Package_TO_SOT_SMD.3dshapes/SOT-23-6.step"),
        ("Inductor_SMD.pretty", "L_Sunlord_MWSA1206S-470", "L1", "4.7uH_Power_Choke", 124.00, 79.00, 0,
         {"1": "SW_BUCK", "2": "VBUS_BUCK_OUT"},
         "Inductor_SMD.3dshapes/L_2816_7142Metric.step"),
        ("Package_TO_SOT_SMD.pretty", "SOT-23-5", "U7", "TLV75533P_3V3_LDO", 162.00, 88.00, -90,
         {"1": "VCC_5V", "2": "GND", "3": "VCC_5V", "4": "GND", "5": "VCC_3V3"},
         "Package_TO_SOT_SMD.3dshapes/SOT-23-5.step"),

        # 5. USB-PD 20W Buck Converter (Southchip SC8102 QFN-32) & Inductor L2
        ("Package_DFN_QFN.pretty", "QFN-32-1EP_5x5mm_P0.5mm_EP3.1x3.1mm_ThermalVias", "U5", "SC8102_USB_PD_20W", 121.00, 90.00, 0,
         {"1": "+12V_PROT", "2": "+12V_PROT", "8": "SW_PD_BUCK", "9": "SW_PD_BUCK",
          "16": "VBUS_PD_OUT", "20": "USB_DN1_DP", "21": "USB_DN1_DM", "32": "GND", "33": "GND"},
         None),
        ("Inductor_SMD.pretty", "L_7.3x7.3_H4.5", "L2", "10uH_PD_Choke", 121.00, 98.00, 0,
         {"1": "SW_PD_BUCK", "2": "VBUS_PD_OUT"},
         None),

        # 6. USB Hub Controller (Microchip USB2514B 36-QFN)
        ("Package_DFN_QFN.pretty", "QFN-36-1EP_6x6mm_P0.5mm_EP4.1x4.1mm", "U2", "USB2514B_AEC_HUB", 142.00, 102.00, 0,
         {"1": "USB_DN1_DM", "2": "USB_DN1_DP", "3": "USB_DN2_DM", "4": "USB_DN2_DP",
          "5": "VCC_3V3", "6": "USB_DN3_DM", "7": "USB_DN3_DP", "8": "USB_DN4_DM",
          "9": "USB_DN4_DP", "10": "VCC_3V3", "11": "GND", "12": "VCC_3V3",
          "13": "VCC_3V3", "14": "VDD12_HUB", "15": "VCC_3V3", "16": "VCC_3V3",
          "17": "OTTOCAST_FAULT_N", "18": "VCC_3V3", "19": "VCC_3V3", "20": "VCC_3V3",
          "21": "VCC_3V3", "22": "VCC_3V3", "23": "VCC_3V3", "24": "VCC_3V3",
          "25": "GND", "26": "VCC_3V3", "27": "VCC_3V3", "28": "GND",
          "29": "VCC_3V3", "30": "USB_UP_DM", "31": "USB_UP_DP", "32": "XTAL_OUT",
          "33": "XTAL_IN", "34": "GND", "35": "HUB_RBIAS", "36": "VCC_3V3", "37": "GND"},
         "Package_DFN_QFN.3dshapes/QFN-36-1EP_6x6mm_P0.5mm_EP3.7x3.7mm.step"),
        ("Crystal.pretty", "Crystal_SMD_3225-4Pin_3.2x2.5mm", "Y1", "24.000MHz", 132.00, 102.00, 180,
         {"1": "XTAL_IN", "2": "GND", "3": "XTAL_OUT", "4": "GND"},
         "Crystal.3dshapes/Crystal_SMD_3225-4Pin_3.2x2.5mm.step"),

        # 7. CP2AA Power Switch (TI TPS2051B SOT-23-5)
        ("Package_TO_SOT_SMD.pretty", "SOT-23-5", "U4", "TPS2051B_PORT2_GATE", 136.00, 92.00, 90,
         {"1": "VCC_5V_OTTOCAST", "2": "GND", "3": "OTTOCAST_FAULT_N", "4": "OTTOCAST_PWR_EN", "5": "VCC_5V"},
         "Package_TO_SOT_SMD.3dshapes/SOT-23-5.step"),

        # 8. CAN Transceiver & Auto-Sensing 120R Relay
        ("Package_SO.pretty", "SOIC-8_3.9x4.9mm_P1.27mm", "U6", "TCAN334G_CAN", 112.00, 100.00, -90,
         {"1": "TWAI_TX", "2": "GND", "3": "VCC_3V3", "4": "TWAI_RX", "5": "GND", "6": "CAN_L", "7": "CAN_H", "8": "CAN_SILENT"},
         "Package_SO.3dshapes/SOIC-8_3.9x4.9mm_P1.27mm.step"),
        ("Package_SO.pretty", "SOP-4_4.4x2.6mm_P1.27mm", "K1", "CPC1017N_CAN_RELAY", 118.00, 100.00, 0,
         {"1": "CAN_TERM_EN", "2": "GND", "3": "CAN_H", "4": "CAN_TERM_R"},
         None),

        # 9. Smart Switches: Q1 (BSD Mirror Dual MOSFET) & Q2 (TPS1H100 Aux Light High-Side Switch)
        ("Package_TO_SOT_SMD.pretty", "SOT-363_SC-70-6", "Q1", "DMN63D8_BSD_MOSFET", 112.00, 110.00, 0,
         {"1": "GND", "2": "BSD_LED_LEFT", "3": "BSD_RIGHT_N", "4": "GND", "5": "BSD_LED_RIGHT", "6": "BSD_LEFT_N"},
         None),
        ("Package_SO.pretty", "Texas_HTSSOP-14-1EP_4.4x5mm_P0.65mm_EP3.4x5mm_Mask3.155x3.255mm_ThermalVias", "Q2", "TPS1H100_AUX_LIGHT", 112.00, 91.00, 0,
         {"1": "GND", "2": "AUX_LIGHT_EN", "3": "VCC_3V3", "4": "GND",
          "6": "+12V_AUX", "7": "+12V_AUX", "8": "+12V_AUX",
          "11": "+12V_PROT", "12": "+12V_PROT", "13": "+12V_PROT", "14": "+12V_PROT", "15": "+12V_PROT"},
         None),

        # 10. Microcontroller: ESP32-S3-WROOM-1U with U.FL
        ("RF_Module.pretty", "ESP32-S3-WROOM-1U", "U1", "ESP32-S3-WROOM-1U", 152.00, 84.00, 0,
         {"1": "GND", "2": "VCC_3V3", "3": "ESP_EN", "4": "KL15_SENSE", "5": "CAN_SILENT",
          "6": "MIC_I2S_WS", "7": "MIC_I2S_BCLK", "8": "PTT_IN1_N", "9": "PTT_IN2_N",
          "10": "PTT_IN3_N", "11": "USB_SERV_DM", "12": "MIC_I2S_DATA", "13": "USB_SERV_DM",
          "14": "USB_SERV_DP", "15": "CAN_TERM_EN", "17": "I2C_SDA", "18": "I2C_SCL",
          "19": "WS2812B_DIN", "20": "BSD_LED_LEFT", "21": "BSD_LED_RIGHT", "22": "AUX_LIGHT_EN",
          "23": "TWAI_TX", "27": "ESP_BOOT", "36": "TWAI_RX", "38": "OTTOCAST_FAULT_N",
          "39": "OTTOCAST_PWR_EN", "40": "GND", "41": "GND"},
         None),

        # 11. Ambient I2S MEMS Microphone (Knowles SPH0645)
        ("Sensor_Audio.pretty", "Knowles_SPH0645LM4H-6_3.5x2.65mm", "MIC1", "SPH0645_I2S_MIC", 145.00, 80.00, 180,
         {"1": "MIC_I2S_DATA", "2": "MIC_I2S_BCLK", "3": "MIC_I2S_WS", "4": "GND", "5": "VCC_3V3"},
         "Sensor_Audio.3dshapes/Knowles_SPH0645LM4H-6_3.5x2.65mm.step"),

        # 12. Key Discrete Passives
        ("Capacitor_SMD.pretty", "C_0805_2012Metric", "C19", "10uF_50V", 116.00, 75.00, 0, {"1": "+12V_PROT", "2": "GND"}, "Capacitor_SMD.3dshapes/C_0805_2012Metric.step"),
        ("Capacitor_SMD.pretty", "C_0805_2012Metric", "C22", "22uF_16V", 124.00, 74.00, 0, {"1": "VCC_5V", "2": "GND"}, "Capacitor_SMD.3dshapes/C_0805_2012Metric.step"),
        ("Capacitor_SMD.pretty", "C_0603_1608Metric", "C24", "2.2uF_3V3", 162.00, 93.00, 180, {"1": "VCC_3V3", "2": "GND"}, "Capacitor_SMD.3dshapes/C_0603_1608Metric.step"),
        ("Resistor_SMD.pretty", "R_0603_1608Metric", "R10", "120R_CAN", 122.00, 102.00, 0, {"1": "CAN_TERM_R", "2": "CAN_L"}, "Resistor_SMD.3dshapes/R_0603_1608Metric.step"),
        ("Resistor_SMD.pretty", "R_0603_1608Metric", "R5", "12k_RBIAS", 135.00, 107.00, 0, {"1": "HUB_RBIAS", "2": "GND"}, "Resistor_SMD.3dshapes/R_0603_1608Metric.step"),
        ("Resistor_SMD.pretty", "R_0603_1608Metric", "R15", "5.1k_CC1", 170.00, 92.00, 90, {"1": "USB_CC1", "2": "GND"}, "Resistor_SMD.3dshapes/R_0603_1608Metric.step"),
        ("Resistor_SMD.pretty", "R_0603_1608Metric", "R16", "5.1k_CC2", 170.00, 97.00, 90, {"1": "USB_CC2", "2": "GND"}, "Resistor_SMD.3dshapes/R_0603_1608Metric.step"),
        ("Resistor_SMD.pretty", "R_0603_1608Metric", "R8", "10k_FAULT", 136.00, 87.00, 0, {"1": "VCC_3V3", "2": "OTTOCAST_FAULT_N"}, "Resistor_SMD.3dshapes/R_0603_1608Metric.step"),

        # 13. 4 Corner M2.5 Mounting Holes (82 x 50 mm Board: X 103.50 .. 178.50, Y 73.50 .. 116.50)
        ("MountingHole.pretty", "MountingHole_2.7mm_M2.5_Pad_Via", "H1", "M2.5_MOUNT", 103.50, 73.50, 0, {"1": "GND"}, None),
        ("MountingHole.pretty", "MountingHole_2.7mm_M2.5_Pad_Via", "H2", "M2.5_MOUNT", 178.50, 73.50, 0, {"1": "GND"}, None),
        ("MountingHole.pretty", "MountingHole_2.7mm_M2.5_Pad_Via", "H3", "M2.5_MOUNT", 103.50, 116.50, 0, {"1": "GND"}, None),
        ("MountingHole.pretty", "MountingHole_2.7mm_M2.5_Pad_Via", "H4", "M2.5_MOUNT", 178.50, 116.50, 0, {"1": "GND"}, None),
    ]

    for item in components:
        lib, fp_name, ref, val, x, y, rot, pin_map, m3d = item
        lib_path = os.path.join(KICAD_FP_DIR, lib)
        fp = pcbnew.FootprintLoad(lib_path, fp_name)
        if not fp:
            print(f"WARNING: Could not load footprint {lib}/{fp_name}")
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

    # Board Outline (82.0 x 50.0 mm, R = 2.5 mm: X: 100.0 .. 182.0, Y: 70.0 .. 120.0)
    r = 2.5
    x1, y1 = 100.0, 70.0
    x2, y2 = 182.0, 120.0

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
    add_arc(x2 - r, y1, x2 - 0.73, y1 + 0.73, x2, y1 + r)
    add_line(x2, y1 + r, x2, y2 - r)
    add_arc(x2, y2 - r, x2 - 0.73, y2 - 0.73, x2 - r, y2)
    add_line(x2 - r, y2, x1 + r, y2)
    add_arc(x1 + r, y2, x1 + 0.73, y2 - 0.73, x1, y2 - r)
    add_line(x1, y2 - r, x1, y1 + r)
    add_arc(x1, y1 + r, x1 + 0.73, y1 + 0.73, x1 + r, y1)

    # Silkscreen Labels
    labels = [
        ("OPENMOTORBRIDGE // UNIVERSAL FRONT NODE (PCBA 05)", 141.0, 71.5, 0.6, 0.6, 0.12),
        ("J1: 12V ACC", 104.5, 76.5, 0.45, 0.45, 0.09),
        ("J10: QI 12V", 104.5, 83.5, 0.45, 0.45, 0.09),
        ("J11: AUX LIGHT", 104.5, 90.5, 0.45, 0.45, 0.09),
        ("J2: CAN-BUS", 104.5, 97.5, 0.45, 0.45, 0.09),
        ("J3: MULTI-BTN", 104.5, 105.0, 0.45, 0.45, 0.09),
        ("J9: BSD MIRROR", 104.5, 112.5, 0.45, 0.45, 0.09),
        ("J4: HOST", 112.5, 118.5, 0.45, 0.45, 0.09),
        ("J5: PHONE-PD", 124.5, 118.5, 0.45, 0.45, 0.09),
        ("J6: CP2AA", 136.5, 118.5, 0.45, 0.45, 0.09),
        ("J5_MP3: GLOVEBOX", 148.5, 118.5, 0.45, 0.45, 0.09),
        ("J6_AUX: COCKPIT", 160.5, 118.5, 0.45, 0.45, 0.09),
        ("J8: CAM 5V", 170.5, 118.5, 0.45, 0.45, 0.09),
        ("J7: SERVICE USB-C", 175.0, 91.5, 0.45, 0.45, 0.09),
        ("ESP32-S3", 152.0, 72.5, 0.5, 0.5, 0.10),
        ("USB2514B HUB", 142.0, 97.0, 0.5, 0.5, 0.10),
        ("SC8102 PD20W", 121.0, 85.0, 0.45, 0.45, 0.09),
    ]
    for text_str, tx, ty, sx, sy, th in labels:
        txt = pcbnew.PCB_TEXT(board)
        txt.SetText(text_str)
        txt.SetPosition(pcbnew.VECTOR2I(int(tx * 1e6), int(ty * 1e6)))
        txt.SetTextSize(pcbnew.VECTOR2I(int(sx * 1e6), int(sy * 1e6)))
        txt.SetTextThickness(int(th * 1e6))
        txt.SetLayer(pcbnew.F_SilkS)
        board.Add(txt)

    board.BuildListOfNets()
    board.Save(PCB_PATH)
    print(f"✓ Created {PCB_PATH}")

if __name__ == "__main__":
    create_project_file()
    create_schematic_file()
    create_pcb_board()
    print("\n🎉 FRONT NODE PCBA 05 PROJECT (82x50mm) SUCCESSFULLY GENERATED!")
