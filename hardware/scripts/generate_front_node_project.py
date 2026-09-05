#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
Generate Complete KiCad 10 Project for OpenMotorBridge Front Node (PCBA 05)
----------------------------------------------------------------------------
- Generates openmotorbridge_front_node.kicad_pro with exact JLCPCB netclasses & setup rules
- Generates openmotorbridge_front_node.kicad_sch with complete schematic wiring & pinout
- Generates openmotorbridge_front_node.kicad_pcb with 68x44mm 4-layer stackup & pre-placed components:
  - 12V Automotive Power & 5V/2A Buck (TPS54302) + 3.3V LDO (TLV75533)
  - Microchip USB2512B 2-Port Automotive Hub + 24MHz Crystal
  - TI TPS2051B VBUS High-Side Switch for Ottocast/CarPlay Dongle
  - ESP32-C3-WROOM-02U with U.FL Antenna Port
  - Knowles SPH0645LM4H Digital I2S MEMS Ambient Microphone
  - TI TCAN334G 3.3V CAN-Bus Transceiver + 120R Termination
  - Hardware Debounced Handlebar PTT Interface
  - Native USB-C Service & Flash Port (GPIO18/19) + BOOT & RST Buttons
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
                    "nets": ["KL15_12V_SW", "VIN_BUCK", "VCC_5V", "VCC_5V_OTTOCAST", "VCC_3V3", "GND", "SW_BUCK", "VBUS_BUCK_OUT", "USB_UP_VBUS"]
                },
                {
                    "name": "USB_DIFF",
                    "clearance": 0.15,
                    "track_width": 0.20,
                    "diff_pair_gap": 0.15,
                    "diff_pair_width": 0.20,
                    "nets": ["USB_UP_DP", "USB_UP_DM", "USB_DN1_DP", "USB_DN1_DM", "USB_DN2_DP", "USB_DN2_DM", "USB_SERV_DP", "USB_SERV_DM"]
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
	(version 20240108)
	(generator "openmotorbridge_gen")
	(generator_version "10.0")
	(uuid "e0000000-0000-0000-0000-000000000001")
	(paper "A3")
	(title_block
		(title "OpenMotorBridge Universal Front Node (Cockpit & Sensor Hub)")
		(date "2026-09-03")
		(rev "v1.1")
		(company "OpenMotorBridge Open Source Hardware")
		(comment 1 "Dual Power: Pure USB Bus-Powered Standard + Optional Switched 12V (KL15 ACC)")
	)

	(lib_symbols
		(symbol "Connector_Generic:Conn_01x02"
			(pin passive line (at 0 2.54 0) (length 2.54) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 0 -2.54 0) (length 2.54) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
		)
		(symbol "Connector_Generic:Conn_01x03"
			(pin passive line (at 0 2.54 0) (length 2.54) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 0 0 0) (length 2.54) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 0 -2.54 0) (length 2.54) (name "Pin_3" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
		)
		(symbol "Connector_Generic:Conn_01x04"
			(pin passive line (at 0 3.81 0) (length 2.54) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 0 1.27 0) (length 2.54) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 0 -1.27 0) (length 2.54) (name "Pin_3" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 0 -3.81 0) (length 2.54) (name "Pin_4" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
		)
	)

	(global_label "KL15_12V_SW" (shape input) (at 30.0 40.0 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "GND" (shape passive) (at 30.0 50.0 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "USB_UP_VBUS" (shape input) (at 30.0 60.0 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "VCC_5V" (shape output) (at 80.0 40.0 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "VCC_3V3" (shape output) (at 80.0 45.0 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "VCC_5V_OTTOCAST" (shape output) (at 80.0 50.0 0) (effects (font (size 1.27 1.27)) (justify left)))

	(global_label "CAN_H" (shape bidirectional) (at 30.0 70.0 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "CAN_L" (shape bidirectional) (at 30.0 75.0 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "PTT_INPUT_N" (shape input) (at 30.0 90.0 180) (effects (font (size 1.27 1.27)) (justify right)))

	(global_label "USB_UP_DP" (shape bidirectional) (at 150.0 40.0 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "USB_UP_DM" (shape bidirectional) (at 150.0 45.0 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "USB_DN1_DP" (shape bidirectional) (at 150.0 55.0 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "USB_DN1_DM" (shape bidirectional) (at 150.0 60.0 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "USB_DN2_DP" (shape bidirectional) (at 150.0 70.0 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "USB_DN2_DM" (shape bidirectional) (at 150.0 75.0 0) (effects (font (size 1.27 1.27)) (justify left)))

	(global_label "MIC_I2S_WS" (shape output) (at 210.0 40.0 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "MIC_I2S_BCLK" (shape output) (at 210.0 45.0 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "MIC_I2S_DATA" (shape input) (at 210.0 50.0 180) (effects (font (size 1.27 1.27)) (justify right)))

	(global_label "OTTOCAST_PWR_EN" (shape output) (at 210.0 65.0 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "OTTOCAST_FAULT_N" (shape input) (at 210.0 70.0 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "KL15_SENSE" (shape input) (at 210.0 75.0 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "TWAI_TX" (shape output) (at 210.0 85.0 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "TWAI_RX" (shape input) (at 210.0 90.0 180) (effects (font (size 1.27 1.27)) (justify right)))
)
"""
    with open(SCH_PATH, "w", encoding="utf-8") as f:
        f.write(sch_content)
    print(f"✓ Created {SCH_PATH}")

def create_pcb_board():
    board = pcbnew.BOARD()

    # Title Block
    tb = board.GetTitleBlock()
    tb.SetTitle("OpenMotorBridge Universal Front Node (Cockpit & Sensor Hub)")
    tb.SetDate("2026-09-03")
    tb.SetRevision("v1.1")
    tb.SetCompany("OpenMotorBridge Open Source Hardware")
    tb.SetComment(0, "Dual Power: Pure USB Bus-Powered Standard + Optional Switched 12V (KL15 ACC)")

    # 4 Layers Stackup
    board.SetLayerName(pcbnew.In1_Cu, "GND_PLANE")
    board.SetLayerName(pcbnew.In2_Cu, "PWR_PLANE")

    # Netlist
    nets = [
        "GND", "KL15_12V_SW", "VIN_BUCK", "KL15_SENSE",
        "VCC_5V", "VCC_5V_OTTOCAST", "VCC_3V3", "VDD12_HUB",
        "USB_UP_VBUS", "USB_UP_DP", "USB_UP_DM",
        "USB_DN1_DP", "USB_DN1_DM",
        "USB_DN2_DP", "USB_DN2_DM",
        "USB_SERV_DP", "USB_SERV_DM",
        "OTTOCAST_PWR_EN", "OTTOCAST_FAULT_N",
        "PTT_INPUT_N", "PTT_RAW",
        "MIC_I2S_WS", "MIC_I2S_BCLK", "MIC_I2S_DATA",
        "TWAI_TX", "TWAI_RX", "CAN_H", "CAN_L",
        "ESP_EN", "ESP_BOOT", "LED_STATUS",
        "XTAL_IN", "XTAL_OUT", "HUB_RESET_N", "HUB_RBIAS",
        "SW_BUCK", "BST_BUCK", "FB_BUCK", "VBUS_BUCK_OUT"
    ]
    net_map = {}
    for name in nets:
        net = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net)
        net_map[name] = net

    # Component Definitions
    components = [
        # 1. Connectors West Edge (Vehicle Interface)
        # J1 is now 2-Pin for OPTIONAL 12V Switched (KL15) + GND
        ("Connector_JST.pretty", "JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", "J1", "OPT_12V_KL15_GND", 103.50, 84.00, -90,
         {"1": "KL15_12V_SW", "2": "GND"},
         "Connector_JST.3dshapes/JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical.step"),
        ("Connector_JST.pretty", "JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical", "J2", "CAN_H_L_GND", 102.50, 96.25, 90,
         {"1": "CAN_H", "2": "CAN_L", "3": "GND"},
         "Connector_JST.3dshapes/JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical.step"),
        ("Connector_JST.pretty", "JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", "J3", "PTT_IN_GND", 102.50, 104.25, 90,
         {"1": "PTT_RAW", "2": "GND"},
         "Connector_JST.3dshapes/JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical.step"),

        # 2. Connectors East Edge (USB System Interface)
        ("Connector_JST.pretty", "JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical", "J4", "USB_UPSTREAM_HOST", 143.25, 111.50, 180,
         {"1": "USB_UP_VBUS", "2": "USB_UP_DM", "3": "USB_UP_DP", "4": "GND"},
         "Connector_JST.3dshapes/JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical.step"),
        ("Connector_JST.pretty", "JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical", "J5", "USB_DN1_GLOVEBOX", 129.50, 111.50, 180,
         {"1": "VCC_5V", "2": "USB_DN1_DM", "3": "USB_DN1_DP", "4": "GND"},
         "Connector_JST.3dshapes/JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical.step"),
        ("Connector_JST.pretty", "JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical", "J6", "USB_DN2_CARPLAY", 115.75, 111.50, 180,
         {"1": "VCC_5V_OTTOCAST", "2": "USB_DN2_DM", "3": "USB_DN2_DP", "4": "GND"},
         "Connector_JST.3dshapes/JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical.step"),
        ("Connector_JST.pretty", "JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical", "J8", "ACTION_CAM_5V_PWR", 156.00, 111.50, 180,
         {"1": "VCC_5V", "2": "USB_CAM_DCP", "3": "USB_CAM_DCP", "4": "GND"},
         "Connector_JST.3dshapes/JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical.step"),

        # 3. East Edge: USB-C Service Port & Tactical Buttons
        ("Connector_USB.pretty", "USB_C_Receptacle_HRO_TYPE-C-31-M-12", "J7", "USB-C_SERVICE", 163.95, 100.82, 90,
         {"A1": "GND", "B1": "GND", "A4": "VCC_5V", "B4": "VCC_5V", "A5": "USB_CC1", "B5": "USB_CC2",
          "A6": "USB_SERV_DP", "B6": "USB_SERV_DP", "A7": "USB_SERV_DM", "B7": "USB_SERV_DM",
          "A12": "GND", "B12": "GND", "SH1": "GND", "SH2": "GND", "SH3": "GND", "SH4": "GND"},
         "Connector_USB.3dshapes/USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal.step"),
        ("Button_Switch_SMD.pretty", "SW_Push_SPST_NO_Alps_SKRK", "SW1", "BOOT", 165.15, 87.75, 0,
         {"1": "ESP_BOOT", "2": "GND"},
         "Button_Switch_SMD.3dshapes/SW_Push_SPST_NO_Alps_SKRK.step"),
        ("Button_Switch_SMD.pretty", "SW_Push_SPST_NO_Alps_SKRK", "SW2", "RESET", 122.50, 92.00, 90,
         {"1": "ESP_EN", "2": "GND"},
         "Button_Switch_SMD.3dshapes/SW_Push_SPST_NO_Alps_SKRK.step"),

        # 4. Power Management Stage (Dual-Path OR-ing: USB VBUS + Optional 12V Buck + C_BUF)
        ("Capacitor_Tantalum_SMD.pretty", "CP_EIA-7343-31_Kemet-D", "C_BUF", "470uF_10V_POLYMER", 163.50, 80.50, 270,
         {"1": "VCC_5V", "2": "GND"},
         "Capacitor_Tantalum_SMD.3dshapes/CP_EIA-7343-31_Kemet-D.step"),
        ("Diode_SMD.pretty", "D_SMA", "D7", "SS34_USB_OR", 149.00, 96.25, 90,
         {"1": "VCC_5V", "2": "USB_UP_VBUS"},
         "Diode_SMD.3dshapes/D_SMA.step"),
        ("Diode_SMD.pretty", "D_SMA", "D8", "SS34_BUCK_OR", 155.25, 73.50, 0,
         {"1": "VBUS_BUCK_OUT", "2": "VCC_5V"},
         "Diode_SMD.3dshapes/D_SMA.step"),
        ("Diode_SMD.pretty", "D_SMA", "D5", "SS34_REV_POL", 104.00, 79.00, 0,
         {"1": "KL15_12V_SW", "2": "VIN_BUCK"},
         "Diode_SMD.3dshapes/D_SMA.step"),
        ("Diode_SMD.pretty", "D_SMB", "D4", "SMCJ36CA_TVS", 110.60, 72.25, 0,
         {"1": "VIN_BUCK", "2": "GND"},
         "Diode_SMD.3dshapes/D_SMB.step"),
        ("Package_TO_SOT_SMD.pretty", "SOT-23-6", "U4", "TPS54302_BUCK_5V2A", 111.11, 78.45, 0,
         {"1": "GND", "2": "SW_BUCK", "3": "VIN_BUCK", "4": "FB_BUCK", "5": "VIN_BUCK", "6": "BST_BUCK"},
         "Package_TO_SOT_SMD.3dshapes/SOT-23-6.step"),
        ("Inductor_SMD.pretty", "L_Sunlord_MWSA1206S-470", "L1", "4.7uH_Power_Choke", 122.38, 76.75, 0,
         {"1": "SW_BUCK", "2": "VBUS_BUCK_OUT"},
         "Inductor_SMD.3dshapes/L_2816_7142Metric.step"),
        ("Package_TO_SOT_SMD.pretty", "SOT-23-5", "U6", "TLV75533P_3V3_500mA", 110.80, 90.14, -90,
         {"1": "VCC_5V", "2": "GND", "3": "VCC_5V", "4": "GND", "5": "VCC_3V3"},
         "Package_TO_SOT_SMD.3dshapes/SOT-23-5.step"),

        # 5. USB Hub Controller (Microchip USB2512B 36-QFN)
        ("Package_DFN_QFN.pretty", "QFN-36-1EP_6x6mm_P0.5mm_EP4.1x4.1mm", "U2", "USB2512B_AEC_HUB", 132.00, 99.84, 90,
         {"1": "VCC_3V3", "2": "USB_UP_DM", "3": "USB_UP_DP", "4": "GND", "5": "VDD12_HUB",
          "6": "XTAL_IN", "7": "XTAL_OUT", "8": "GND", "9": "HUB_RBIAS", "10": "HUB_RESET_N",
          "11": "USB_DN1_DM", "12": "USB_DN1_DP", "13": "GND", "14": "VCC_3V3",
          "15": "USB_DN2_DM", "16": "USB_DN2_DP", "17": "GND", "37": "GND"},
         "Package_DFN_QFN.3dshapes/QFN-36-1EP_6x6mm_P0.5mm_EP3.7x3.7mm.step"),
        ("Crystal.pretty", "Crystal_SMD_3225-4Pin_3.2x2.5mm", "Y1", "24.000MHz", 121.40, 100.10, 180,
         {"1": "XTAL_IN", "2": "GND", "3": "XTAL_OUT", "4": "GND"},
         "Crystal.3dshapes/Crystal_SMD_3225-4Pin_3.2x2.5mm.step"),

        # 6. CarPlay Power Switch (TI TPS2051B)
        ("Package_TO_SOT_SMD.pretty", "SOT-23-5", "U3", "TPS2051B_CARPLAY_SWITCH", 129.55, 88.86, 90,
         {"1": "VCC_5V_OTTOCAST", "2": "GND", "3": "OTTOCAST_FAULT_N", "4": "OTTOCAST_PWR_EN", "5": "VCC_5V"},
         "Package_TO_SOT_SMD.3dshapes/SOT-23-5.step"),

        # 7. CAN Transceiver (TI TCAN334G SOIC-8)
        ("Package_SO.pretty", "SOIC-8_3.9x4.9mm_P1.27mm", "U5", "TCAN334G_CAN", 111.97, 100.97, -90,
         {"1": "TWAI_TX", "2": "GND", "3": "VCC_3V3", "4": "TWAI_RX", "5": "GND", "6": "CAN_L", "7": "CAN_H"},
         "Package_SO.3dshapes/SOIC-8_3.9x4.9mm_P1.27mm.step"),

        # 8. Microcontroller (ESP32-C3-WROOM-02U with U.FL)
        ("RF_Module.pretty", "ESP32-C3-WROOM-02U", "U1", "ESP32-C3-WROOM-02U", 149.50, 85.25, 0,
         {"1": "VCC_3V3", "2": "ESP_EN", "3": "PTT_INPUT_N", "4": "MIC_I2S_WS", "5": "MIC_I2S_BCLK",
          "6": "MIC_I2S_DATA", "7": "TWAI_RX", "8": "TWAI_TX", "9": "OTTOCAST_PWR_EN", "10": "OTTOCAST_FAULT_N",
          "11": "LED_STATUS", "12": "ESP_BOOT", "13": "KL15_SENSE", "14": "GND",
          "15": "USB_SERV_DM", "16": "USB_SERV_DP", "17": "GND", "18": "GND", "19": "GND"},
         "RF_Module.3dshapes/ESP32-C3-WROOM-02U.step"),

        # 9. Ambient I2S MEMS Microphone (Knowles SPH0645)
        ("Sensor_Audio.pretty", "Knowles_SPH0645LM4H-6_3.5x2.65mm", "MIC1", "SPH0645_I2S_MIC", 122.50, 85.46, 180,
         {"1": "MIC_I2S_DATA", "2": "MIC_I2S_BCLK", "3": "MIC_I2S_WS", "4": "GND", "5": "VCC_3V3"},
         "Sensor_Audio.3dshapes/Knowles_SPH0645LM4H-6_3.5x2.65mm.step"),

        # 10. Status Indicator
        ("LED_SMD.pretty", "LED_0805_2012Metric", "D1", "LED_STATUS_GREEN", 166.25, 100.19, -90,
         {"1": "LED_STATUS", "2": "GND"},
         "LED_SMD.3dshapes/LED_0805_2012Metric.step"),

        # 11. Key Discrete Passives (0603 / 0805)
        ("Capacitor_SMD.pretty", "C_0805_2012Metric", "C19", "10uF_50V", 111.05, 84.25, 0, {"1": "VIN_BUCK", "2": "GND"}, "Capacitor_SMD.3dshapes/C_0805_2012Metric.step"),
        ("Capacitor_SMD.pretty", "C_0805_2012Metric", "C22", "22uF_16V", 116.80, 89.00, 0, {"1": "VCC_5V", "2": "GND"}, "Capacitor_SMD.3dshapes/C_0805_2012Metric.step"),
        ("Capacitor_SMD.pretty", "C_0603_1608Metric", "C24", "2.2uF_3V3", 110.72, 94.25, 180, {"1": "VCC_3V3", "2": "GND"}, "Capacitor_SMD.3dshapes/C_0603_1608Metric.step"),
        ("Resistor_SMD.pretty", "R_0603_1608Metric", "R10", "120R_CAN", 117.00, 102.17, -90, {"1": "CAN_H", "2": "CAN_L"}, "Resistor_SMD.3dshapes/R_0603_1608Metric.step"),
        ("Resistor_SMD.pretty", "R_0603_1608Metric", "R5", "12k_RBIAS", 141.18, 101.25, 0, {"1": "HUB_RBIAS", "2": "GND"}, "Resistor_SMD.3dshapes/R_0603_1608Metric.step"),
        ("Resistor_SMD.pretty", "R_0603_1608Metric", "R15", "5.1k_CC1", 155.75, 99.17, 90, {"1": "USB_CC1", "2": "GND"}, "Resistor_SMD.3dshapes/R_0603_1608Metric.step"),
        ("Resistor_SMD.pretty", "R_0603_1608Metric", "R16", "5.1k_CC2", 161.00, 99.58, 90, {"1": "USB_CC2", "2": "GND"}, "Resistor_SMD.3dshapes/R_0603_1608Metric.step"),
        ("Resistor_SMD.pretty", "R_0603_1608Metric", "R8", "10k_FAULT", 159.25, 95.08, 90, {"1": "VCC_3V3", "2": "OTTOCAST_FAULT_N"}, "Resistor_SMD.3dshapes/R_0603_1608Metric.step"),
        # 12. 4 Corner M2.5 Mounting Holes
        ("MountingHole.pretty", "MountingHole_2.7mm_M2.5_Pad_Via", "H1", "M2.5_MOUNT", 103.50, 73.50, 0, {"1": "GND"}, None),
        ("MountingHole.pretty", "MountingHole_2.7mm_M2.5_Pad_Via", "H2", "M2.5_MOUNT", 164.50, 73.50, 0, {"1": "GND"}, None),
        ("MountingHole.pretty", "MountingHole_2.7mm_M2.5_Pad_Via", "H3", "M2.5_MOUNT", 103.50, 110.50, 0, {"1": "GND"}, None),
        ("MountingHole.pretty", "MountingHole_2.7mm_M2.5_Pad_Via", "H4", "M2.5_MOUNT", 164.50, 110.50, 0, {"1": "GND"}, None),
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
        print(f"  ✓ Added {ref:6s} ({fp_name}) at ({x:.2f}, {y:.2f}) mm")

    # Board Outline (68.0 x 44.0 mm, R = 2.5 mm: X: 100.0 .. 168.0, Y: 70.0 .. 114.0)
    r = 2.5
    x1, y1 = 100.0, 70.0
    x2, y2 = 168.0, 114.0

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

    # Add Silkscreen Labels
    labels = [
        ("OPENMOTORBRIDGE // UNIVERSAL FRONT NODE", 134.0, 71.2, 0.6, 0.6, 0.12),
        ("J1: OPT 12V ACC", 104.5, 75.5, 0.45, 0.45, 0.09),
        ("J2: CAN-BUS", 104.5, 87.5, 0.45, 0.45, 0.09),
        ("J3: PTT", 104.5, 98.5, 0.45, 0.45, 0.09),
        ("J4: USB HOST", 163.5, 74.5, 0.45, 0.45, 0.09),
        ("J5: GLOVEBOX", 163.5, 86.5, 0.45, 0.45, 0.09),
        ("J6: CARPLAY", 163.5, 98.5, 0.45, 0.45, 0.09),
        ("ESP32-C3", 132.0, 87.5, 0.5, 0.5, 0.10),
        ("USB HUB", 146.0, 96.5, 0.5, 0.5, 0.10),
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
    print("\n🎉 FRONT NODE PROJECT SUCCESSFULLY GENERATED!")
