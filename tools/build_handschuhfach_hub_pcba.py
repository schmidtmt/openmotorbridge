#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
tools/build_handschuhfach_hub_pcba.py
=====================================
Builds the complete, production-ready KiCad 10 project for:
PCBA 05B: Handschuhfach-Hub (Glovebox Media & Power-Injection Hub)
"""

import os
import sys
import pcbnew

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TARGET_DIR = os.path.join(REPO_ROOT, "hardware", "kicad_cockpit_breakout")
PRO_PATH = os.path.join(TARGET_DIR, "openmotorbridge_cockpit_breakout.kicad_pro")
SCH_PATH = os.path.join(TARGET_DIR, "openmotorbridge_cockpit_breakout.kicad_sch")
PCB_PATH = os.path.join(TARGET_DIR, "openmotorbridge_cockpit_breakout.kicad_pcb")

KICAD_FP_DIR = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"

def to_nm(val):
    return int(round(val * 1e6))

def create_project_file():
    pro_content = '''{
  "board": {
    "design_settings": {
      "defaults": {
        "board_outline_line_width": 0.15,
        "copper_line_width": 0.20,
        "silk_line_width": 0.12,
        "min_clearance": 0.15,
        "min_track_width": 0.15,
        "min_via_annular_width": 0.13,
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
  "boards": [],
  "cvpcb": {
    "equivalence_files": []
  },
  "libraries": {
    "pinned_footprint_libs": [],
    "pinned_symbol_libs": []
  },
  "meta": {
    "filename": "openmotorbridge_cockpit_breakout.kicad_pro",
    "version": 1
  },
  "net_settings": {
    "classes": [
      {
        "clearance": 0.15,
        "name": "Default",
        "track_width": 0.20,
        "via_diameter": 0.6,
        "via_drill": 0.3
      },
      {
        "clearance": 0.18,
        "name": "Power",
        "track_width": 0.50,
        "via_diameter": 0.8,
        "via_drill": 0.4
      }
    ]
  },
  "schematic": {
    "drawing": {
      "default_line_thickness": 0.15,
      "default_text_size": 1.27
    }
  },
  "sheets": [
    [
      "b605b000-0000-0000-0000-000000000001",
      ""
    ]
  ]
}
'''
    with open(PRO_PATH, "w", encoding="utf-8") as f:
        f.write(pro_content)

def create_schematic_file():
    sch_content = '''(kicad_sch
	(version 20260306)
	(generator "eeschema")
	(generator_version "10.0")
	(uuid "b605b000-0000-0000-0000-000000000001")
	(paper "A3")
	(title_block
		(title "OpenMotorBridge PCBA 05B: Handschuhfach-Hub")
		(date "2026-10-31")
		(rev "v10.0")
		(company "OpenMotorBridge Open Source Hardware")
		(comment 1 "Harley-Davidson Skyline OS / Boom! Box 4-Port USB Hub & Power-Injection")
		(comment 2 "Upstream Host, Front Node Link, 15W Phone Fast-Charge, Dongle, Media")
	)
	(lib_symbols
		(symbol "USB2514Bi_sym"
			(property "Reference" "U1" (at 0 25.4 0) (effects (font (size 1.27 1.27))))
			(property "Value" "USB2514Bi-AEZG" (at 0 -25.4 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Package_DFN_QFN:QFN-36-1EP_6x6mm_P0.5mm_EP4.1x4.1mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "USB2514Bi_1_1"
				(rectangle (start -15.24 22.86) (end 15.24 -22.86) (stroke (width 0.254) (type solid)) (fill (type background)))
				(pin input line (at -17.78 20.32 0) (length 2.54) (name "USB_UP_DP" (effects (font (size 1.27 1.27)))) (number "21" (effects (font (size 1.27 1.27)))))
				(pin input line (at -17.78 17.78 0) (length 2.54) (name "USB_UP_DM" (effects (font (size 1.27 1.27)))) (number "20" (effects (font (size 1.27 1.27)))))
				(pin input line (at -17.78 12.70 0) (length 2.54) (name "VBUS_DET" (effects (font (size 1.27 1.27)))) (number "24" (effects (font (size 1.27 1.27)))))
				(pin input line (at -17.78 7.62 0) (length 2.54) (name "RESET_N" (effects (font (size 1.27 1.27)))) (number "33" (effects (font (size 1.27 1.27)))))
				(pin input line (at -17.78 2.54 0) (length 2.54) (name "XTAL_IN" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
				(pin output line (at -17.78 0.00 0) (length 2.54) (name "XTAL_OUT" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -17.78 -5.08 0) (length 2.54) (name "RBIAS" (effects (font (size 1.27 1.27)))) (number "36" (effects (font (size 1.27 1.27)))))
				(pin input line (at -17.78 -10.16 0) (length 2.54) (name "CFG_SEL0" (effects (font (size 1.27 1.27)))) (number "23" (effects (font (size 1.27 1.27)))))
				(pin input line (at -17.78 -12.70 0) (length 2.54) (name "CFG_SEL1" (effects (font (size 1.27 1.27)))) (number "25" (effects (font (size 1.27 1.27)))))
				(pin input line (at -17.78 -15.24 0) (length 2.54) (name "NON_REM0" (effects (font (size 1.27 1.27)))) (number "26" (effects (font (size 1.27 1.27)))))
				(pin input line (at -17.78 -17.78 0) (length 2.54) (name "NON_REM1" (effects (font (size 1.27 1.27)))) (number "27" (effects (font (size 1.27 1.27)))))
				(pin input line (at -17.78 -20.32 0) (length 2.54) (name "TEST" (effects (font (size 1.27 1.27)))) (number "28" (effects (font (size 1.27 1.27)))))
				(pin bidi line (at 17.78 20.32 180) (length 2.54) (name "USB_DN1_DP" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin bidi line (at 17.78 17.78 180) (length 2.54) (name "USB_DN1_DM" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin bidi line (at 17.78 12.70 180) (length 2.54) (name "USB_DN2_DP" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin bidi line (at 17.78 10.16 180) (length 2.54) (name "USB_DN2_DM" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin bidi line (at 17.78 5.08 180) (length 2.54) (name "USB_DN3_DP" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
				(pin bidi line (at 17.78 2.54 180) (length 2.54) (name "USB_DN3_DM" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin bidi line (at 17.78 -2.54 180) (length 2.54) (name "USB_DN4_DP" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
				(pin bidi line (at 17.78 -5.08 180) (length 2.54) (name "USB_DN4_DM" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 0 25.4 270) (length 2.54) (name "VDD33" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at 2.54 25.4 270) (length 2.54) (name "VDD18" (effects (font (size 1.27 1.27)))) (number "31" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 0 -25.4 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 2.54 -25.4 90) (length 2.54) (name "EP_GND" (effects (font (size 1.27 1.27)))) (number "37" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "USBC_sym"
			(property "Reference" "J" (at 0 13.97 0) (effects (font (size 1.27 1.27))))
			(property "Value" "USB_C_Receptacle" (at 0 -13.97 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "USBC_1_1"
				(rectangle (start -10.16 11.43) (end 10.16 -11.43) (stroke (width 0.254) (type solid)) (fill (type background)))
				(pin power_in line (at -12.70 8.89 0) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "A4/B9" (effects (font (size 1.27 1.27)))))
				(pin bidi line (at -12.70 3.81 0) (length 2.54) (name "DP" (effects (font (size 1.27 1.27)))) (number "A6/B6" (effects (font (size 1.27 1.27)))))
				(pin bidi line (at -12.70 1.27 0) (length 2.54) (name "DM" (effects (font (size 1.27 1.27)))) (number "A7/B7" (effects (font (size 1.27 1.27)))))
				(pin bidi line (at -12.70 -3.81 0) (length 2.54) (name "CC1" (effects (font (size 1.27 1.27)))) (number "A5" (effects (font (size 1.27 1.27)))))
				(pin bidi line (at -12.70 -6.35 0) (length 2.54) (name "CC2" (effects (font (size 1.27 1.27)))) (number "B5" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at -12.70 -8.89 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "A1/B12" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 12.70 -8.89 180) (length 2.54) (name "SHIELD" (effects (font (size 1.27 1.27)))) (number "SH" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "LDO_sym"
			(property "Reference" "U2" (at 0 8.89 0) (effects (font (size 1.27 1.27))))
			(property "Value" "AP2112K-3.3" (at 0 -8.89 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Package_TO_SOT_SMD:SOT-23-5" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "LDO_1_1"
				(rectangle (start -7.62 6.35) (end 7.62 -6.35) (stroke (width 0.254) (type solid)) (fill (type background)))
				(pin power_in line (at -10.16 3.81 0) (length 2.54) (name "VIN" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 0 -8.89 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin input line (at -10.16 -3.81 0) (length 2.54) (name "EN" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at 10.16 3.81 180) (length 2.54) (name "VOUT" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "XTAL_sym"
			(property "Reference" "Y1" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
			(property "Value" "24.000MHz" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "XTAL_1_1"
				(rectangle (start -5.08 3.81) (end 5.08 -3.81) (stroke (width 0.254) (type solid)) (fill (type background)))
				(pin passive line (at -7.62 1.27 0) (length 2.54) (name "1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 7.62 1.27 180) (length 2.54) (name "3" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 0 -6.35 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "MountHole_sym"
			(property "Reference" "H" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
			(property "Value" "M2.5" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "MountingHole:MountingHole_2.7mm_M2.5_Pad" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "MountHole_1_1"
				(circle (center 0 0) (radius 1.778) (stroke (width 0.254) (type solid)) (fill (type none)))
				(pin passive line (at 0 -3.81 90) (length 2.032) (name "1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
		)
	)

	(symbol (lib_id "USBC_sym") (at 38.10 50.80 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "c0010000-0000-0000-0000-000000000001")
		(property "Reference" "J1" (at 38.10 35.56 0) (effects (font (size 1.27 1.27))))
		(property "Value" "SKYLINE_HOST" (at 38.10 38.10 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12" (at 38.10 50.80 0) (effects (font (size 1.27 1.27)) hide))
		(pin "A4/B9" (uuid "c0010000-0000-0000-0000-000000000002"))
		(pin "A6/B6" (uuid "c0010000-0000-0000-0000-000000000003"))
		(pin "A7/B7" (uuid "c0010000-0000-0000-0000-000000000004"))
		(pin "A5" (uuid "c0010000-0000-0000-0000-000000000005"))
		(pin "B5" (uuid "c0010000-0000-0000-0000-000000000006"))
		(pin "A1/B12" (uuid "c0010000-0000-0000-0000-000000000007"))
		(pin "SH" (uuid "c0010000-0000-0000-0000-000000000008"))
	)

	(symbol (lib_id "USBC_sym") (at 88.90 50.80 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "c0020000-0000-0000-0000-000000000001")
		(property "Reference" "J2" (at 88.90 35.56 0) (effects (font (size 1.27 1.27))))
		(property "Value" "FRONT_NODE" (at 88.90 38.10 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12" (at 88.90 50.80 0) (effects (font (size 1.27 1.27)) hide))
		(pin "A4/B9" (uuid "c0020000-0000-0000-0000-000000000002"))
		(pin "A6/B6" (uuid "c0020000-0000-0000-0000-000000000003"))
		(pin "A7/B7" (uuid "c0020000-0000-0000-0000-000000000004"))
		(pin "A5" (uuid "c0020000-0000-0000-0000-000000000005"))
		(pin "B5" (uuid "c0020000-0000-0000-0000-000000000006"))
		(pin "A1/B12" (uuid "c0020000-0000-0000-0000-000000000007"))
		(pin "SH" (uuid "c0020000-0000-0000-0000-000000000008"))
	)

	(symbol (lib_id "USBC_sym") (at 139.70 50.80 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "c0030000-0000-0000-0000-000000000001")
		(property "Reference" "J3" (at 139.70 35.56 0) (effects (font (size 1.27 1.27))))
		(property "Value" "PHONE_CHARGE" (at 139.70 38.10 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12" (at 139.70 50.80 0) (effects (font (size 1.27 1.27)) hide))
		(pin "A4/B9" (uuid "c0030000-0000-0000-0000-000000000002"))
		(pin "A6/B6" (uuid "c0030000-0000-0000-0000-000000000003"))
		(pin "A7/B7" (uuid "c0030000-0000-0000-0000-000000000004"))
		(pin "A5" (uuid "c0030000-0000-0000-0000-000000000005"))
		(pin "B5" (uuid "c0030000-0000-0000-0000-000000000006"))
		(pin "A1/B12" (uuid "c0030000-0000-0000-0000-000000000007"))
		(pin "SH" (uuid "c0030000-0000-0000-0000-000000000008"))
	)

	(symbol (lib_id "USBC_sym") (at 190.50 50.80 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "c0040000-0000-0000-0000-000000000001")
		(property "Reference" "J4" (at 190.50 35.56 0) (effects (font (size 1.27 1.27))))
		(property "Value" "DONGLE" (at 190.50 38.10 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12" (at 190.50 50.80 0) (effects (font (size 1.27 1.27)) hide))
		(pin "A4/B9" (uuid "c0040000-0000-0000-0000-000000000002"))
		(pin "A6/B6" (uuid "c0040000-0000-0000-0000-000000000003"))
		(pin "A7/B7" (uuid "c0040000-0000-0000-0000-000000000004"))
		(pin "A5" (uuid "c0040000-0000-0000-0000-000000000005"))
		(pin "B5" (uuid "c0040000-0000-0000-0000-000000000006"))
		(pin "A1/B12" (uuid "c0040000-0000-0000-0000-000000000007"))
		(pin "SH" (uuid "c0040000-0000-0000-0000-000000000008"))
	)

	(symbol (lib_id "USBC_sym") (at 241.30 50.80 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "c0050000-0000-0000-0000-000000000001")
		(property "Reference" "J5" (at 241.30 35.56 0) (effects (font (size 1.27 1.27))))
		(property "Value" "MEDIA" (at 241.30 38.10 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12" (at 241.30 50.80 0) (effects (font (size 1.27 1.27)) hide))
		(pin "A4/B9" (uuid "c0050000-0000-0000-0000-000000000002"))
		(pin "A6/B6" (uuid "c0050000-0000-0000-0000-000000000003"))
		(pin "A7/B7" (uuid "c0050000-0000-0000-0000-000000000004"))
		(pin "A5" (uuid "c0050000-0000-0000-0000-000000000005"))
		(pin "B5" (uuid "c0050000-0000-0000-0000-000000000006"))
		(pin "A1/B12" (uuid "c0050000-0000-0000-0000-000000000007"))
		(pin "SH" (uuid "c0050000-0000-0000-0000-000000000008"))
	)

	(symbol (lib_id "USB2514Bi_sym") (at 139.70 127.00 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "c0060000-0000-0000-0000-000000000001")
		(property "Reference" "U1" (at 139.70 99.06 0) (effects (font (size 1.27 1.27))))
		(property "Value" "USB2514Bi-AEZG" (at 139.70 101.60 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Package_DFN_QFN:QFN-36-1EP_6x6mm_P0.5mm_EP4.1x4.1mm" (at 139.70 127.00 0) (effects (font (size 1.27 1.27)) hide))
		(pin "21" (uuid "c0060000-0000-0000-0000-000000000002"))
		(pin "20" (uuid "c0060000-0000-0000-0000-000000000003"))
		(pin "24" (uuid "c0060000-0000-0000-0000-000000000004"))
		(pin "33" (uuid "c0060000-0000-0000-0000-000000000005"))
		(pin "12" (uuid "c0060000-0000-0000-0000-000000000006"))
		(pin "13" (uuid "c0060000-0000-0000-0000-000000000007"))
		(pin "36" (uuid "c0060000-0000-0000-0000-000000000008"))
		(pin "23" (uuid "c0060000-0000-0000-0000-000000000009"))
		(pin "25" (uuid "c0060000-0000-0000-0000-00000000000a"))
		(pin "26" (uuid "c0060000-0000-0000-0000-00000000000b"))
		(pin "27" (uuid "c0060000-0000-0000-0000-00000000000c"))
		(pin "28" (uuid "c0060000-0000-0000-0000-00000000000d"))
		(pin "2" (uuid "c0060000-0000-0000-0000-00000000000e"))
		(pin "1" (uuid "c0060000-0000-0000-0000-00000000000f"))
		(pin "4" (uuid "c0060000-0000-0000-0000-000000000010"))
		(pin "3" (uuid "c0060000-0000-0000-0000-000000000011"))
		(pin "7" (uuid "c0060000-0000-0000-0000-000000000012"))
		(pin "6" (uuid "c0060000-0000-0000-0000-000000000013"))
		(pin "9" (uuid "c0060000-0000-0000-0000-000000000014"))
		(pin "8" (uuid "c0060000-0000-0000-0000-000000000015"))
		(pin "5" (uuid "c0060000-0000-0000-0000-000000000016"))
		(pin "31" (uuid "c0060000-0000-0000-0000-000000000017"))
		(pin "14" (uuid "c0060000-0000-0000-0000-000000000018"))
		(pin "37" (uuid "c0060000-0000-0000-0000-000000000019"))
	)

	(symbol (lib_id "LDO_sym") (at 38.10 127.00 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "c0070000-0000-0000-0000-000000000001")
		(property "Reference" "U2" (at 38.10 115.57 0) (effects (font (size 1.27 1.27))))
		(property "Value" "AP2112K-3.3" (at 38.10 118.11 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Package_TO_SOT_SMD:SOT-23-5" (at 38.10 127.00 0) (effects (font (size 1.27 1.27)) hide))
		(pin "1" (uuid "c0070000-0000-0000-0000-000000000002"))
		(pin "2" (uuid "c0070000-0000-0000-0000-000000000003"))
		(pin "3" (uuid "c0070000-0000-0000-0000-000000000004"))
		(pin "5" (uuid "c0070000-0000-0000-0000-000000000005"))
	)

	(symbol (lib_id "XTAL_sym") (at 88.90 127.00 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "c0080000-0000-0000-0000-000000000001")
		(property "Reference" "Y1" (at 88.90 119.38 0) (effects (font (size 1.27 1.27))))
		(property "Value" "24.000MHz" (at 88.90 121.92 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm" (at 88.90 127.00 0) (effects (font (size 1.27 1.27)) hide))
		(pin "1" (uuid "c0080000-0000-0000-0000-000000000002"))
		(pin "3" (uuid "c0080000-0000-0000-0000-000000000003"))
		(pin "2" (uuid "c0080000-0000-0000-0000-000000000004"))
	)

	(symbol (lib_id "MountHole_sym") (at 215.90 127.00 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "c0090000-0000-0000-0000-000000000001")
		(property "Reference" "H1" (at 215.90 120.65 0) (effects (font (size 1.27 1.27))))
		(property "Value" "M2.5" (at 215.90 123.19 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "MountingHole:MountingHole_2.7mm_M2.5_Pad" (at 215.90 127.00 0) (effects (font (size 1.27 1.27)) hide))
		(pin "1" (uuid "c0090000-0000-0000-0000-000000000002"))
	)

	(symbol (lib_id "MountHole_sym") (at 241.30 127.00 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "c0100000-0000-0000-0000-000000000001")
		(property "Reference" "H2" (at 241.30 120.65 0) (effects (font (size 1.27 1.27))))
		(property "Value" "M2.5" (at 241.30 123.19 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "MountingHole:MountingHole_2.7mm_M2.5_Pad" (at 241.30 127.00 0) (effects (font (size 1.27 1.27)) hide))
		(pin "1" (uuid "c0100000-0000-0000-0000-000000000002"))
	)

	(no_connect (at 157.48 124.46) (uuid "c0990000-0000-0000-0000-000000000001"))
	(no_connect (at 157.48 121.92) (uuid "c0990000-0000-0000-0000-000000000002"))
	(global_label "VCC_5V" (shape bidirectional) (at 76.20 59.69 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "c1000000-0000-0000-0000-000000000001"))
	(global_label "GND" (shape bidirectional) (at 76.20 39.37 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "c1000000-0000-0000-0000-000000000002"))
	(global_label "+3V3" (shape bidirectional) (at 48.26 130.81 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "c1000000-0000-0000-0000-000000000003"))
	(sheet_instances
		(path "/" (page "1"))
	)
)
'''
    with open(SCH_PATH, "w", encoding="utf-8") as f:
        f.write(sch_content)

def build_pcb():
    board = pcbnew.BOARD()
    W, H = 76.0, 20.0

    net_names = [
        "", "GND", "VCC_5V", "+3V3", "+1V8", "VBUS_HOST_SENSE",
        "USB_UP_DP", "USB_UP_DM", "USB_DN1_DP", "USB_DN1_DM",
        "USB_DN2_DP", "USB_DN2_DM", "USB_DN3_DP", "USB_DN3_DM",
        "NET_J1_CC1", "NET_J1_CC2", "NET_J2_CC1", "NET_J2_CC2",
        "NET_J3_CC1", "NET_J3_CC2", "NET_PHONE_D",
        "NET_J4_CC1", "NET_J4_CC2", "NET_J5_CC1", "NET_J5_CC2",
        "XTAL_IN", "XTAL_OUT", "RESET_N", "RBIAS"
    ]

    net_map = {}
    for nname in net_names:
        net = pcbnew.NETINFO_ITEM(board, nname)
        board.Add(net)
        net_map[nname] = net

    # Edge.Cuts with 1.0mm chamfers
    pts = [
        (1.0, 0.0), (W - 1.0, 0.0), (W, 1.0), (W, H - 1.0),
        (W - 1.0, H), (1.0, H), (0.0, H - 1.0), (0.0, 1.0), (1.0, 0.0)
    ]
    for i in range(len(pts) - 1):
        seg = pcbnew.PCB_SHAPE(board)
        seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        seg.SetStart(pcbnew.VECTOR2I(to_nm(pts[i][0]), to_nm(pts[i][1])))
        seg.SetEnd(pcbnew.VECTOR2I(to_nm(pts[i+1][0]), to_nm(pts[i+1][1])))
        seg.SetWidth(to_nm(0.15))
        seg.SetLayer(pcbnew.Edge_Cuts)
        board.Add(seg)

    def place_fp(lib_folder, fp_name, ref, val, x, y, rot_deg, pin_nets, model_3d=None):
        lib_path = os.path.join(KICAD_FP_DIR, lib_folder)
        fp = pcbnew.FootprintLoad(lib_path, fp_name)
        if fp is None:
            raise RuntimeError(f"Could not load footprint {fp_name} from {lib_path}")
        fp.SetReference(ref)
        fp.SetValue(val)
        fp.SetLayer(pcbnew.F_Cu)
        fp.SetPosition(pcbnew.VECTOR2I(to_nm(x), to_nm(y)))
        fp.SetOrientationDegrees(rot_deg)
        fp.Reference().SetVisible(True)
        fp.Value().SetVisible(False)

        if model_3d:
            models = fp.Models()
            if len(models) > 0:
                models[0].m_Filename = model_3d

        for pad in fp.Pads():
            pnum = pad.GetNumber()
            if pnum in pin_nets:
                nname = pin_nets[pnum]
                if nname in net_map:
                    pad.SetNet(net_map[nname])
            elif pnum == "" or pnum == "0":
                pad.SetNet(net_map["GND"])

        board.Add(fp)
        return fp

    # Mounting Holes
    place_fp("MountingHole.pretty", "MountingHole_2.7mm_M2.5_Pad", "H1", "M2.5", 4.0, 16.0, 0, {"1": "GND"})
    place_fp("MountingHole.pretty", "MountingHole_2.7mm_M2.5_Pad", "H2", "M2.5", 72.0, 16.0, 0, {"1": "GND"})

    # 5x USB-C Receptacles in a row at Y = 4.55 mm
    usbc_3d = "${KICAD10_3DMODEL_DIR}/Connector_USB.3dshapes/USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal.step"
    def usbc_pins(vbus, dp, dm, cc1, cc2):
        return {
            "A1": "GND", "A12": "GND", "B1": "GND", "B12": "GND", "SH": "GND",
            "A4": vbus, "A9": vbus, "B4": vbus, "B9": vbus,
            "A6": dp, "B6": dp, "A7": dm, "B7": dm,
            "A5": cc1, "B5": cc2
        }

    place_fp("Connector_USB.pretty", "USB_C_Receptacle_HRO_TYPE-C-31-M-12", "J1", "SKYLINE_HOST",
             9.82, 4.55, 180,
             usbc_pins("VBUS_HOST_SENSE", "USB_UP_DP", "USB_UP_DM", "NET_J1_CC1", "NET_J1_CC2"),
             model_3d=usbc_3d)

    place_fp("Connector_USB.pretty", "USB_C_Receptacle_HRO_TYPE-C-31-M-12", "J2", "FRONT_NODE",
             21.82, 4.55, 180,
             usbc_pins("VCC_5V", "USB_DN3_DP", "USB_DN3_DM", "NET_J2_CC1", "NET_J2_CC2"),
             model_3d=usbc_3d)

    place_fp("Connector_USB.pretty", "USB_C_Receptacle_HRO_TYPE-C-31-M-12", "J3", "PHONE_CHARGE",
             33.82, 4.55, 180,
             usbc_pins("VCC_5V", "NET_PHONE_D", "NET_PHONE_D", "NET_J3_CC1", "NET_J3_CC2"),
             model_3d=usbc_3d)

    place_fp("Connector_USB.pretty", "USB_C_Receptacle_HRO_TYPE-C-31-M-12", "J4", "DONGLE",
             45.82, 4.55, 180,
             usbc_pins("VCC_5V", "USB_DN1_DP", "USB_DN1_DM", "NET_J4_CC1", "NET_J4_CC2"),
             model_3d=usbc_3d)

    place_fp("Connector_USB.pretty", "USB_C_Receptacle_HRO_TYPE-C-31-M-12", "J5", "MEDIA",
             57.82, 4.55, 180,
             usbc_pins("VCC_5V", "USB_DN2_DP", "USB_DN2_DM", "NET_J5_CC1", "NET_J5_CC2"),
             model_3d=usbc_3d)

    # U1: Microchip USB2514B Automotive 4-Port Hub Controller (rot = 180° so Upstream faces West, Downstream faces East)
    u1_pins = {
        "1": "USB_DN1_DM", "2": "USB_DN1_DP",
        "3": "USB_DN2_DM", "4": "USB_DN2_DP",
        "5": "+3V3",
        "6": "USB_DN3_DM", "7": "USB_DN3_DP",
        "8": "GND", "9": "GND",
        "10": "+3V3", "11": "+3V3",
        "12": "XTAL_IN", "13": "XTAL_OUT",
        "14": "GND",
        "15": "+3V3", "16": "+3V3", "17": "+3V3", "18": "+3V3", "19": "+3V3",
        "20": "USB_UP_DM", "21": "USB_UP_DP",
        "22": "+3V3", "23": "GND", "24": "VBUS_HOST_SENSE", "25": "GND",
        "26": "GND", "27": "GND", "28": "GND",
        "29": "+3V3", "30": "+3V3", "31": "+1V8", "32": "+3V3",
        "33": "RESET_N", "34": "GND", "35": "+3V3", "36": "RBIAS", "37": "GND"
    }
    qfn_3d = "${KICAD10_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/Texas_RHH0036C_VQFN-36-1EP_6x6mm_P0.5mm_EP4.4x4.4mm.step"
    place_fp("Package_DFN_QFN.pretty", "QFN-36-1EP_6x6mm_P0.5mm_EP4.1x4.1mm", "U1", "USB2514Bi-AEZG",
             38.0, 15.0, 180, u1_pins, model_3d=qfn_3d)


    # Passives (0603) - All placed well clear of U1 QFN-36 footprint (X=35..41, Y=12..18)
    # Crystal Caps (West of U1 at X = 26.5 and 31.5, Y = 17.5)
    place_fp("Capacitor_SMD.pretty", "C_0603_1608Metric", "C_XTAL1", "12pF", 26.5, 17.5, 0, {"1": "XTAL_IN", "2": "GND"})
    place_fp("Capacitor_SMD.pretty", "C_0603_1608Metric", "C_XTAL2", "12pF", 31.5, 17.5, 0, {"1": "XTAL_OUT", "2": "GND"})

    # Core & Reset Caps / Resistors (East of U1 at X = 44.5..48.0)
    place_fp("Resistor_SMD.pretty", "R_0603_1608Metric", "R_RBIAS", "12.0k", 44.5, 17.5, 0, {"1": "RBIAS", "2": "GND"})
    place_fp("Resistor_SMD.pretty", "R_0603_1608Metric", "R_RST", "10k", 44.5, 14.8, 0, {"1": "RESET_N", "2": "+3V3"})
    place_fp("Capacitor_SMD.pretty", "C_0603_1608Metric", "C_RST", "100nF", 44.5, 12.0, 0, {"1": "RESET_N", "2": "GND"})
    place_fp("Capacitor_SMD.pretty", "C_0603_1608Metric", "C_VDD18", "1uF", 48.0, 17.5, 0, {"1": "+1V8", "2": "GND"})

    # LDO Caps (East of U2 at X = 54.0)
    place_fp("Capacitor_SMD.pretty", "C_0603_1608Metric", "C_IN1", "10uF", 54.0, 12.8, 90, {"1": "VCC_5V", "2": "GND"})
    place_fp("Capacitor_SMD.pretty", "C_0603_1608Metric", "C_OUT1", "10uF", 54.0, 17.2, 90, {"1": "+3V3", "2": "GND"})

    # CC Resistors for J1, J2, J3, J4, J5 (Well clear of U1 and USB-C connectors)
    place_fp("Resistor_SMD.pretty", "R_0603_1608Metric", "R1", "5.1k", 8.0, 11.5, 90, {"1": "NET_J1_CC1", "2": "GND"})
    place_fp("Resistor_SMD.pretty", "R_0603_1608Metric", "R2", "5.1k", 11.5, 11.5, 90, {"1": "NET_J1_CC2", "2": "GND"})
    place_fp("Resistor_SMD.pretty", "R_0603_1608Metric", "R3", "5.1k", 20.0, 11.5, 90, {"1": "NET_J2_CC1", "2": "GND"})
    place_fp("Resistor_SMD.pretty", "R_0603_1608Metric", "R4", "5.1k", 23.5, 11.5, 90, {"1": "NET_J2_CC2", "2": "GND"})

    # J3 (Phone): 56k pull-ups to VCC_5V for 15W Type-C native charging (at X = 30.5 and X = 32.5, Y = 11.5)
    place_fp("Resistor_SMD.pretty", "R_0603_1608Metric", "R5", "56k", 30.5, 11.5, 90, {"1": "NET_J3_CC1", "2": "VCC_5V"})
    place_fp("Resistor_SMD.pretty", "R_0603_1608Metric", "R6", "56k", 32.5, 11.5, 90, {"1": "NET_J3_CC2", "2": "VCC_5V"})

    place_fp("Resistor_SMD.pretty", "R_0603_1608Metric", "R7", "5.1k", 48.0, 11.5, 90, {"1": "NET_J4_CC1", "2": "GND"})
    place_fp("Resistor_SMD.pretty", "R_0603_1608Metric", "R8", "5.1k", 51.5, 11.5, 90, {"1": "NET_J4_CC2", "2": "GND"})
    place_fp("Resistor_SMD.pretty", "R_0603_1608Metric", "R9", "5.1k", 56.0, 11.5, 90, {"1": "NET_J5_CC1", "2": "GND"})
    place_fp("Resistor_SMD.pretty", "R_0603_1608Metric", "R10", "5.1k", 59.5, 11.5, 90, {"1": "NET_J5_CC2", "2": "GND"})

    # Silkscreen Markings
    def add_silk(text, x, y, size=0.8, layer=pcbnew.F_SilkS, mirror=False):
        txt = pcbnew.PCB_TEXT(board)
        txt.SetText(text)
        txt.SetPosition(pcbnew.VECTOR2I(to_nm(x), to_nm(y)))
        txt.SetTextSize(pcbnew.VECTOR2I(to_nm(size), to_nm(size)))
        txt.SetTextThickness(to_nm(0.12))
        txt.SetLayer(layer)
        if mirror:
            txt.SetMirrored(True)
        board.Add(txt)

    add_silk("PCBA 05B // GLOVEBOX MEDIA & POWER-INJECTION HUB", 38.0, 1.3, 0.75)
    add_silk("HOST", 9.82, 10.0, 0.55)
    add_silk("FRONT", 21.82, 10.0, 0.55)
    add_silk("PHONE 15W", 33.82, 10.0, 0.55)
    add_silk("DONGLE", 45.82, 10.0, 0.55)
    add_silk("MEDIA", 57.82, 10.0, 0.55)
    add_silk("OPENMOTORBRIDGE v10.0 // MJF PA12 GLOVEBOX", 38.0, 7.5, 0.85, pcbnew.B_SilkS, True)
    add_silk("HARLEY SKYLINE OS // 4-PORT USB2514B HUB", 38.0, 10.5, 0.65, pcbnew.B_SilkS, True)

    # Ground Planes (Zones) on F.Cu and B.Cu
    gnd_net = net_map["GND"]
    for layer_id in [pcbnew.F_Cu, pcbnew.B_Cu]:
        zone = pcbnew.ZONE(board)
        zone.SetLayer(layer_id)
        zone.SetNet(gnd_net)
        zone.SetAssignedPriority(0)
        zone.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        zone.SetThermalReliefGap(to_nm(0.20))
        zone.SetThermalReliefSpokeWidth(to_nm(0.25))
        zone.SetMinThickness(to_nm(0.20))

        poly = zone.Outline()
        poly.NewOutline()
        poly.Append(to_nm(0.0), to_nm(0.0))
        poly.Append(to_nm(W), to_nm(0.0))
        poly.Append(to_nm(W), to_nm(H))
        poly.Append(to_nm(0.0), to_nm(H))

        board.Add(zone)

    # Zone fill
    zf = pcbnew.ZONE_FILLER(board)
    zf.Fill(board.Zones())

    board.Save(PCB_PATH)
    print(f"✅ Board successfully saved to {PCB_PATH}")

def main():
    os.makedirs(TARGET_DIR, exist_ok=True)
    create_project_file()
    create_schematic_file()
    build_pcb()

if __name__ == "__main__":
    main()
