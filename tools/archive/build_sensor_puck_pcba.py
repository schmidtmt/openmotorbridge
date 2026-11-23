#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
tools/build_sensor_puck_pcba.py
================================
Builds the complete, production-ready KiCad 10 project for:
PCBA 05D: Modular Environmental & GNSS Sensor Puck (openmotorbridge_sensor_puck)

Components:
- U1: u-blox SAM-M10Q Multi-GNSS module (15.5 x 15.5 mm patch antenna)
- U2: TI TMP117 High-Precision Digital Thermometer (WSON-6 2x2 mm)
- U3: TI OPT3001 Ambient Light Sensor (WSON-6 2x2 mm)
- J1: JST-GH 6-Pin horizontal SMD (SM06B-GHS-TB) - Primary In from Front Node
- J2: JST-SH 6-Pin horizontal SMD (SM06B-SRSS-TB) - Daisy-Chain Expansion Out
- C1-C5: Decoupling and bulk capacitors (0603)
- R1-R3: Pull-up resistors for I2C and Reset (0603)
- H1-H3: M2 mounting / rest pads
"""

import os
import sys
import pcbnew

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TARGET_DIR = os.path.join(REPO_ROOT, "hardware", "kicad_sensor_puck")
PRO_PATH = os.path.join(TARGET_DIR, "openmotorbridge_sensor_puck.kicad_pro")
SCH_PATH = os.path.join(TARGET_DIR, "openmotorbridge_sensor_puck.kicad_sch")
PCB_PATH = os.path.join(TARGET_DIR, "openmotorbridge_sensor_puck.kicad_pcb")

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
    "filename": "openmotorbridge_sensor_puck.kicad_pro",
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
        "track_width": 0.35,
        "via_diameter": 0.65,
        "via_drill": 0.35
      }
    ]
  },
  "sheets": [
    [
      "e0000000-0000-0000-0000-000000000001",
      ""
    ]
  ]
}'''
    with open(PRO_PATH, "w", encoding="utf-8") as f:
        f.write(pro_content)
    print(f"Created {PRO_PATH}")

def create_schematic_file():
    sch_content = '''(kicad_sch
	(version 20260306)
	(generator "eeschema")
	(generator_version "10.0")
	(uuid "e0000000-0000-0000-0000-000000000001")
	(paper "A3")
	(title_block
		(title "OpenMotorBridge PCBA 05D: Modular Sensor Puck")
		(date "2026-11-01")
		(rev "v10.0")
		(company "OpenMotorBridge Project")
		(comment 1 "SAM-M10Q GNSS, TMP117 Thermometer, OPT3001 Lux Sensor")
		(comment 2 "J1 Primary In (JST-GH), J2 Daisy-Chain Expansion (JST-SH)")
	)
	(lib_symbols
		(symbol "SAM_M10Q_sym"
			(property "Reference" "U1" (at 0 25.4 0) (effects (font (size 1.27 1.27))))
			(property "Value" "SAM-M10Q" (at 0 -25.4 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "RF_GPS:ublox_SAM-M8Q" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "SAM_M10Q_1_1"
				(rectangle (start -15.24 22.86) (end 15.24 -22.86) (stroke (width 0.254) (type solid)) (fill (type background)))
				(pin power_in line (at 0 25.4 270) (length 2.54) (name "VCC" (effects (font (size 1.27 1.27)))) (number "17" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 2.54 25.4 270) (length 2.54) (name "V_IO" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 5.08 25.4 270) (length 2.54) (name "V_BCKP" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 0 -25.4 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin bidi line (at 17.78 12.70 180) (length 2.54) (name "SDA" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
				(pin input line (at 17.78 7.62 180) (length 2.54) (name "SCL" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
				(pin output line (at 17.78 -5.08 180) (length 2.54) (name "TIMEPULSE" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
				(pin input line (at -17.78 0.00 0) (length 2.54) (name "RESET_N" (effects (font (size 1.27 1.27)))) (number "18" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "TMP117_sym"
			(property "Reference" "U2" (at 0 12.7 0) (effects (font (size 1.27 1.27))))
			(property "Value" "TMP117AIDRVR" (at 0 -12.7 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Package_SON:WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "TMP117_1_1"
				(rectangle (start -10.16 10.16) (end 10.16 -10.16) (stroke (width 0.254) (type solid)) (fill (type background)))
				(pin power_in line (at 0 12.7 270) (length 2.54) (name "V+" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 0 -12.7 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin input line (at -12.70 5.08 0) (length 2.54) (name "SCL" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin bidi line (at 12.70 5.08 180) (length 2.54) (name "SDA" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin input line (at -12.70 -5.08 0) (length 2.54) (name "ADD0" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 2.54 -12.7 90) (length 2.54) (name "EP" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "OPT3001_sym"
			(property "Reference" "U3" (at 0 12.7 0) (effects (font (size 1.27 1.27))))
			(property "Value" "OPT3001DNPR" (at 0 -12.7 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Package_SON:WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "OPT3001_1_1"
				(rectangle (start -10.16 10.16) (end 10.16 -10.16) (stroke (width 0.254) (type solid)) (fill (type background)))
				(pin power_in line (at 0 12.7 270) (length 2.54) (name "VDD" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 0 -12.7 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin input line (at -12.70 -5.08 0) (length 2.54) (name "ADDR" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin input line (at -12.70 5.08 0) (length 2.54) (name "SCL" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin bidi line (at 12.70 5.08 180) (length 2.54) (name "SDA" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 2.54 -12.7 90) (length 2.54) (name "EP" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "CONN_06P_sym"
			(property "Reference" "J" (at 0 12.7 0) (effects (font (size 1.27 1.27))))
			(property "Value" "CONN_06P" (at 0 -12.7 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Connector_JST:JST_GH_SM06B-GHS-TB_1x06-1MP_P1.25mm_Horizontal" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "CONN_06P_1_1"
				(rectangle (start -7.62 10.16) (end 7.62 -10.16) (stroke (width 0.254) (type solid)) (fill (type background)))
				(pin power_in line (at -10.16 7.62 0) (length 2.54) (name "3V3" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at -10.16 5.08 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin bidi line (at -10.16 2.54 0) (length 2.54) (name "I2C_SDA" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin input line (at -10.16 0.00 0) (length 2.54) (name "I2C_SCL" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin bidi line (at -10.16 -2.54 0) (length 2.54) (name "EXT_I2S_DATA" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin bidi line (at -10.16 -5.08 0) (length 2.54) (name "EXT_I2S_WS" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
			)
		)
	)

	(symbol (lib_id "CONN_06P_sym") (at 38.10 50.80 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "e0010000-0000-0000-0000-000000000001")
		(property "Reference" "J1" (at 38.10 38.10 0) (effects (font (size 1.27 1.27))))
		(property "Value" "J_SENSOR_IN" (at 38.10 40.64 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Connector_JST:JST_GH_SM06B-GHS-TB_1x06-1MP_P1.25mm_Horizontal" (at 38.10 50.80 0) (effects (font (size 1.27 1.27)) hide))
		(pin "1" (uuid "e0010000-0000-0000-0000-000000000002"))
		(pin "2" (uuid "e0010000-0000-0000-0000-000000000003"))
		(pin "3" (uuid "e0010000-0000-0000-0000-000000000004"))
		(pin "4" (uuid "e0010000-0000-0000-0000-000000000005"))
		(pin "5" (uuid "e0010000-0000-0000-0000-000000000006"))
		(pin "6" (uuid "e0010000-0000-0000-0000-000000000007"))
	)

	(symbol (lib_id "CONN_06P_sym") (at 38.10 88.90 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "e0020000-0000-0000-0000-000000000001")
		(property "Reference" "J2" (at 38.10 76.20 0) (effects (font (size 1.27 1.27))))
		(property "Value" "J_EXPANSION_OUT" (at 38.10 78.74 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Connector_JST:JST_SH_SM06B-SRSS-TB_1x06-1MP_P1.00mm_Horizontal" (at 38.10 88.90 0) (effects (font (size 1.27 1.27)) hide))
		(pin "1" (uuid "e0020000-0000-0000-0000-000000000002"))
		(pin "2" (uuid "e0020000-0000-0000-0000-000000000003"))
		(pin "3" (uuid "e0020000-0000-0000-0000-000000000004"))
		(pin "4" (uuid "e0020000-0000-0000-0000-000000000005"))
		(pin "5" (uuid "e0020000-0000-0000-0000-000000000006"))
		(pin "6" (uuid "e0020000-0000-0000-0000-000000000007"))
	)

	(symbol (lib_id "SAM_M10Q_sym") (at 101.60 63.50 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "e0030000-0000-0000-0000-000000000001")
		(property "Reference" "U1" (at 101.60 35.56 0) (effects (font (size 1.27 1.27))))
		(property "Value" "SAM-M10Q" (at 101.60 38.10 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "RF_GPS:ublox_SAM-M8Q" (at 101.60 63.50 0) (effects (font (size 1.27 1.27)) hide))
		(pin "17" (uuid "e0030000-0000-0000-0000-000000000002"))
		(pin "2" (uuid "e0030000-0000-0000-0000-000000000003"))
		(pin "3" (uuid "e0030000-0000-0000-0000-000000000004"))
		(pin "1" (uuid "e0030000-0000-0000-0000-000000000005"))
		(pin "9" (uuid "e0030000-0000-0000-0000-000000000006"))
		(pin "12" (uuid "e0030000-0000-0000-0000-000000000007"))
		(pin "7" (uuid "e0030000-0000-0000-0000-000000000008"))
		(pin "18" (uuid "e0030000-0000-0000-0000-000000000009"))
	)

	(symbol (lib_id "TMP117_sym") (at 152.40 45.72 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "e0040000-0000-0000-0000-000000000001")
		(property "Reference" "U2" (at 152.40 30.48 0) (effects (font (size 1.27 1.27))))
		(property "Value" "TMP117AIDRVR" (at 152.40 33.02 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Package_SON:WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm" (at 152.40 45.72 0) (effects (font (size 1.27 1.27)) hide))
		(pin "5" (uuid "e0040000-0000-0000-0000-000000000002"))
		(pin "2" (uuid "e0040000-0000-0000-0000-000000000003"))
		(pin "1" (uuid "e0040000-0000-0000-0000-000000000004"))
		(pin "6" (uuid "e0040000-0000-0000-0000-000000000005"))
		(pin "4" (uuid "e0040000-0000-0000-0000-000000000006"))
		(pin "7" (uuid "e0040000-0000-0000-0000-000000000007"))
	)

	(symbol (lib_id "OPT3001_sym") (at 152.40 88.90 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "e0050000-0000-0000-0000-000000000001")
		(property "Reference" "U3" (at 152.40 73.66 0) (effects (font (size 1.27 1.27))))
		(property "Value" "OPT3001DNPR" (at 152.40 76.20 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Package_SON:WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm" (at 152.40 88.90 0) (effects (font (size 1.27 1.27)) hide))
		(pin "2" (uuid "e0050000-0000-0000-0000-000000000002"))
		(pin "3" (uuid "e0050000-0000-0000-0000-000000000003"))
		(pin "1" (uuid "e0050000-0000-0000-0000-000000000004"))
		(pin "4" (uuid "e0050000-0000-0000-0000-000000000005"))
		(pin "6" (uuid "e0050000-0000-0000-0000-000000000006"))
		(pin "7" (uuid "e0050000-0000-0000-0000-000000000007"))
	)

	(global_label "VCC_3V3" (shape bidirectional) (at 60.96 43.18 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "e0100000-0000-0000-0000-000000000001"))
	(global_label "GND" (shape bidirectional) (at 60.96 45.72 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "e0100000-0000-0000-0000-000000000002"))
	(global_label "I2C_SDA" (shape bidirectional) (at 60.96 48.26 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "e0100000-0000-0000-0000-000000000003"))
	(global_label "I2C_SCL" (shape bidirectional) (at 60.96 50.80 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "e0100000-0000-0000-0000-000000000004"))
	(global_label "EXT_I2S_DATA" (shape bidirectional) (at 60.96 53.34 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "e0100000-0000-0000-0000-000000000005"))
	(global_label "EXT_I2S_WS" (shape bidirectional) (at 60.96 55.88 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "e0100000-0000-0000-0000-000000000006"))
	(sheet_instances
		(path "/" (page "1"))
	)
)'''
    with open(SCH_PATH, "w", encoding="utf-8") as f:
        f.write(sch_content)
    print(f"Created {SCH_PATH}")

def build_pcb():
    board = pcbnew.BOARD()
    board.SetCopperLayerCount(4)
    board.SetLayerName(pcbnew.In1_Cu, "GND_PLANE")
    board.SetLayerType(pcbnew.In1_Cu, pcbnew.LT_POWER)
    board.SetLayerName(pcbnew.In2_Cu, "PWR_PLANE")
    board.SetLayerType(pcbnew.In2_Cu, pcbnew.LT_POWER)
    
    W, H = 34.0, 34.0
    chamfer = 2.0

    net_names = [
        "", "GND", "VCC_3V3", "I2C_SDA", "I2C_SCL",
        "EXT_I2S_DATA", "EXT_I2S_WS", "GNSS_TIMEPULSE", "GNSS_RESET_N"
    ]
    net_map = {}
    for nname in net_names:
        net = pcbnew.NETINFO_ITEM(board, nname)
        board.Add(net)
        net_map[nname] = net

    # 1. Outline (34 x 34 mm with 2.0 mm chamfered corners on Edge.Cuts)
    pts = [
        (chamfer, 0.0), (W - chamfer, 0.0),
        (W, chamfer), (W, H - chamfer),
        (W - chamfer, H), (chamfer, H),
        (0.0, H - chamfer), (0.0, chamfer),
        (chamfer, 0.0)
    ]
    for i in range(len(pts) - 1):
        seg = pcbnew.PCB_SHAPE(board)
        seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        seg.SetStart(pcbnew.VECTOR2I(to_nm(pts[i][0]), to_nm(pts[i][1])))
        seg.SetEnd(pcbnew.VECTOR2I(to_nm(pts[i+1][0]), to_nm(pts[i+1][1])))
        seg.SetWidth(to_nm(0.15))
        seg.SetLayer(pcbnew.Edge_Cuts)
        board.Add(seg)

    # 2. Thermal isolation slot around TMP117 (at X = 5.0, Y = 7.0)
    # U-shaped milled slot: (1.5, 3.5) -> (8.5, 3.5) -> (8.5, 10.5) -> (1.5, 10.5)
    slot_pts = [
        (1.5, 3.5, 8.5, 3.5),
        (8.5, 3.5, 8.5, 10.5),
        (8.5, 10.5, 1.5, 10.5)
    ]
    for x1, y1, x2, y2 in slot_pts:
        seg = pcbnew.PCB_SHAPE(board)
        seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        seg.SetStart(pcbnew.VECTOR2I(to_nm(x1), to_nm(y1)))
        seg.SetEnd(pcbnew.VECTOR2I(to_nm(x2), to_nm(y2)))
        seg.SetWidth(to_nm(0.8)) # 0.8 mm routed slot
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

    # 3. Footprint Placement
    wson_3d = "${KICAD10_3DMODEL_DIR}/Package_SON.3dshapes/WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm.step"
    jst_gh_3d = "${KICAD10_3DMODEL_DIR}/Connector_JST.3dshapes/JST_GH_SM06B-GHS-TB_1x06-1MP_P1.25mm_Horizontal.step"
    jst_sh_3d = "${KICAD10_3DMODEL_DIR}/Connector_JST.3dshapes/JST_SH_SM06B-SRSS-TB_1x06-1MP_P1.00mm_Horizontal.step"
    c_3d = "${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step"
    r_3d = "${KICAD10_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0603_1608Metric.step"

    # A. u-blox SAM-M10Q GNSS Module (X = 20.0, Y = 17.0 mm)
    sam_nets = {
        "1": "GND", "2": "VCC_3V3", "3": "VCC_3V3", "4": "GND", "5": "GND", "6": "GND",
        "7": "GNSS_TIMEPULSE", "9": "I2C_SDA", "10": "GND", "11": "GND", "12": "I2C_SCL",
        "15": "GND", "16": "GND", "17": "VCC_3V3", "18": "GNSS_RESET_N", "20": "GND"
    }
    place_fp("RF_GPS.pretty", "ublox_SAM-M8Q", "U1", "SAM-M10Q", 20.0, 17.0, 0, sam_nets)

    # B. TI TMP117 High-Precision Thermometer (X = 5.0, Y = 7.0 mm)
    tmp_nets = {
        "1": "I2C_SCL", "2": "GND", "4": "GND", "5": "VCC_3V3", "6": "I2C_SDA", "7": "GND"
    }
    place_fp("Package_SON.pretty", "WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm", "U2", "TMP117AIDRVR", 5.0, 7.0, 0, tmp_nets, wson_3d)

    # C. TI OPT3001 Ambient Light Sensor (X = 7.0, Y = 17.0 mm)
    opt_nets = {
        "1": "GND", "2": "VCC_3V3", "3": "GND", "4": "I2C_SCL", "6": "I2C_SDA", "7": "GND"
    }
    place_fp("Package_SON.pretty", "WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm", "U3", "OPT3001DNPR", 7.0, 17.0, 0, opt_nets, wson_3d)

    # D. Connectors (East edge at X = 31.0 mm, rot = 180° so cable entrance faces East)
    conn_nets = {
        "1": "VCC_3V3", "2": "GND", "3": "I2C_SDA", "4": "I2C_SCL",
        "5": "EXT_I2S_DATA", "6": "EXT_I2S_WS", "MP": "GND"
    }
    # J1: Primary Sensor In (JST-GH 1.25 mm) at Y = 9.0 mm
    place_fp("Connector_JST.pretty", "JST_GH_SM06B-GHS-TB_1x06-1MP_P1.25mm_Horizontal", "J1", "JST_GH_06P_SENSOR_IN", 31.0, 9.0, 180, conn_nets, jst_gh_3d)

    # J2: Daisy-Chain / Expansion Out (JST-SH 1.00 mm) at Y = 25.0 mm
    place_fp("Connector_JST.pretty", "JST_SH_SM06B-SRSS-TB_1x06-1MP_P1.00mm_Horizontal", "J2", "JST_SH_06P_EXP_OUT", 31.0, 25.0, 180, conn_nets, jst_sh_3d)

    # E. Passives (0603)
    # North Rail Passives (Y = 4.5 .. 6.5 mm)
    place_fp("Capacitor_SMD.pretty", "C_0603_1608Metric", "C5", "10uF", 28.0, 4.5, 0, {"1": "VCC_3V3", "2": "GND"}, c_3d)
    place_fp("Capacitor_SMD.pretty", "C_0603_1608Metric", "C2", "4.7uF", 22.0, 6.5, 0, {"1": "VCC_3V3", "2": "GND"}, c_3d)
    place_fp("Capacitor_SMD.pretty", "C_0603_1608Metric", "C1", "0.1uF", 19.0, 6.5, 0, {"1": "VCC_3V3", "2": "GND"}, c_3d)
    place_fp("Resistor_SMD.pretty", "R_0603_1608Metric", "R3", "10k", 16.0, 6.5, 0, {"1": "VCC_3V3", "2": "GNSS_RESET_N"}, r_3d)

    # TMP117 Cap (C3) on Tongue
    place_fp("Capacitor_SMD.pretty", "C_0603_1608Metric", "C3", "0.1uF", 3.0, 5.0, 90, {"1": "VCC_3V3", "2": "GND"}, c_3d)

    # OPT3001 Cap (C4)
    place_fp("Capacitor_SMD.pretty", "C_0603_1608Metric", "C4", "0.1uF", 4.0, 17.0, 90, {"1": "VCC_3V3", "2": "GND"}, c_3d)

    # I2C Pull-ups (R1 & R2)
    place_fp("Resistor_SMD.pretty", "R_0603_1608Metric", "R2", "4.7k", 29.0, 18.0, 0, {"1": "VCC_3V3", "2": "I2C_SCL"}, r_3d)
    place_fp("Resistor_SMD.pretty", "R_0603_1608Metric", "R1", "4.7k", 29.0, 20.5, 0, {"1": "VCC_3V3", "2": "I2C_SDA"}, r_3d)

    # Corner Mounting Pads (M2 Clearance / Rest Bosses)
    for h_ref, hx, hy in [("H1", 3.5, 30.5), ("H2", 30.5, 30.5), ("H3", 30.5, 3.5)]:
        place_fp("MountingHole.pretty", "MountingHole_2.2mm_M2_Pad", h_ref, "M2", hx, hy, 0, {"1": "GND"})

    print("Footprints placed successfully.")

    # 4. Routing
    def add_track(net, x1, y1, x2, y2, width_mm=0.2, layer=pcbnew.F_Cu):
        t = pcbnew.PCB_TRACK(board)
        t.SetNet(net)
        t.SetLayer(layer)
        t.SetWidth(to_nm(width_mm))
        t.SetStart(pcbnew.VECTOR2I(to_nm(x1), to_nm(y1)))
        t.SetEnd(pcbnew.VECTOR2I(to_nm(x2), to_nm(y2)))
        board.Add(t)

    def add_via(net, x, y, drill_mm=0.3, dia_mm=0.6):
        v = pcbnew.PCB_VIA(board)
        v.SetNet(net)
        v.SetViaType(pcbnew.VIATYPE_THROUGH)
        v.SetPosition(pcbnew.VECTOR2I(to_nm(x), to_nm(y)))
        v.SetDrill(to_nm(drill_mm))
        v.SetWidth(to_nm(dia_mm))
        board.Add(v)

    def pad_pos(ref, pnum):
        fp = board.FindFootprintByReference(ref)
        p = fp.FindPadByNumber(str(pnum))
        pos = p.GetPosition()
        return pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y)

    # A. EXT_I2S_WS & EXT_I2S_DATA (Bottom layer B.Cu bus between J1 and J2)
    # J1 pin 6 -> B.Cu via -> trace along X=27.5 -> B.Cu via -> J2 pin 6
    p_j1_6x, p_j1_6y = pad_pos("J1", "6")
    p_j2_6x, p_j2_6y = pad_pos("J2", "6")
    add_track(net_map["EXT_I2S_WS"], p_j1_6x, p_j1_6y, 27.5, 12.0, 0.2, pcbnew.F_Cu)
    add_via(net_map["EXT_I2S_WS"], 27.5, 12.0)
    add_track(net_map["EXT_I2S_WS"], 27.5, 12.0, 27.5, 24.5, 0.2, pcbnew.B_Cu)
    add_via(net_map["EXT_I2S_WS"], 27.5, 24.5)
    add_track(net_map["EXT_I2S_WS"], 27.5, 24.5, p_j2_6x, p_j2_6y, 0.2, pcbnew.F_Cu)

    # J1 pin 5 -> B.Cu via -> trace along X=28.5 -> B.Cu via -> J2 pin 5
    p_j1_5x, p_j1_5y = pad_pos("J1", "5")
    p_j2_5x, p_j2_5y = pad_pos("J2", "5")
    add_track(net_map["EXT_I2S_DATA"], p_j1_5x, p_j1_5y, 28.5, 12.0, 0.2, pcbnew.F_Cu)
    add_via(net_map["EXT_I2S_DATA"], 28.5, 12.0)
    add_track(net_map["EXT_I2S_DATA"], 28.5, 12.0, 28.5, 24.5, 0.2, pcbnew.B_Cu)
    add_via(net_map["EXT_I2S_DATA"], 28.5, 24.5)
    add_track(net_map["EXT_I2S_DATA"], 28.5, 24.5, p_j2_5x, p_j2_5y, 0.2, pcbnew.F_Cu)

    # B. I2C SCL Bus
    # J1 pin 4 -> B.Cu via -> trace along X=30.0 -> branches to U1 pin 12 & R2 pin 2 -> J2 pin 4
    p_j1_4x, p_j1_4y = pad_pos("J1", "4")
    p_j2_4x, p_j2_4y = pad_pos("J2", "4")
    add_track(net_map["I2C_SCL"], p_j1_4x, p_j1_4y, 30.0, 12.0, 0.2, pcbnew.F_Cu)
    add_via(net_map["I2C_SCL"], 30.0, 12.0)
    add_track(net_map["I2C_SCL"], 30.0, 12.0, 30.0, 24.5, 0.2, pcbnew.B_Cu)
    add_via(net_map["I2C_SCL"], 30.0, 24.5)
    add_track(net_map["I2C_SCL"], 30.0, 24.5, p_j2_4x, p_j2_4y, 0.2, pcbnew.F_Cu)

    # Tap SCL at (30.0, 18.0)
    add_via(net_map["I2C_SCL"], 30.0, 18.0)
    p_r2_2x, p_r2_2y = pad_pos("R2", "2")
    add_track(net_map["I2C_SCL"], 30.0, 18.0, p_r2_2x, p_r2_2y, 0.2, pcbnew.F_Cu)
    p_u1_12x, p_u1_12y = pad_pos("U1", "12")
    add_track(net_map["I2C_SCL"], p_r2_2x, p_r2_2y, p_u1_12x, p_u1_12y, 0.2, pcbnew.F_Cu)

    # Route SCL on B.Cu to U3 pin 4 & U2 pin 1
    add_via(net_map["I2C_SCL"], 25.5, 18.9)
    add_track(net_map["I2C_SCL"], p_u1_12x, p_u1_12y, 25.5, 18.9, 0.2, pcbnew.F_Cu)
    add_track(net_map["I2C_SCL"], 25.5, 18.9, 9.5, 18.9, 0.2, pcbnew.B_Cu)
    add_via(net_map["I2C_SCL"], 9.5, 18.9)
    p_u3_4x, p_u3_4y = pad_pos("U3", "4")
    add_track(net_map["I2C_SCL"], 9.5, 18.9, p_u3_4x, p_u3_4y, 0.2, pcbnew.F_Cu)

    # SCL to U2 pin 1 (through neck at West edge)
    add_track(net_map["I2C_SCL"], 9.5, 18.9, 1.0, 18.9, 0.2, pcbnew.B_Cu)
    add_track(net_map["I2C_SCL"], 1.0, 18.9, 1.0, 6.35, 0.2, pcbnew.B_Cu)
    add_via(net_map["I2C_SCL"], 1.0, 6.35)
    p_u2_1x, p_u2_1y = pad_pos("U2", "1")
    add_track(net_map["I2C_SCL"], 1.0, 6.35, p_u2_1x, p_u2_1y, 0.2, pcbnew.F_Cu)

    # C. I2C SDA Bus
    # J1 pin 3 -> B.Cu via -> trace along X=31.5 -> branches to U1 pin 9 & R1 pin 2 -> J2 pin 3
    p_j1_3x, p_j1_3y = pad_pos("J1", "3")
    p_j2_3x, p_j2_3y = pad_pos("J2", "3")
    add_track(net_map["I2C_SDA"], p_j1_3x, p_j1_3y, 31.5, 12.0, 0.2, pcbnew.F_Cu)
    add_via(net_map["I2C_SDA"], 31.5, 12.0)
    add_track(net_map["I2C_SDA"], 31.5, 12.0, 31.5, 24.5, 0.2, pcbnew.B_Cu)
    add_via(net_map["I2C_SDA"], 31.5, 24.5)
    add_track(net_map["I2C_SDA"], 31.5, 24.5, p_j2_3x, p_j2_3y, 0.2, pcbnew.F_Cu)

    # Tap SDA at (31.5, 20.5)
    add_via(net_map["I2C_SDA"], 31.5, 20.5)
    p_r1_2x, p_r1_2y = pad_pos("R1", "2")
    add_track(net_map["I2C_SDA"], 31.5, 20.5, p_r1_2x, p_r1_2y, 0.2, pcbnew.F_Cu)

    # SDA to U1 pin 9 (21.90, 23.60)
    p_u1_9x, p_u1_9y = pad_pos("U1", "9")
    add_track(net_map["I2C_SDA"], p_r1_2x, p_r1_2y, 25.0, 20.5, 0.2, pcbnew.F_Cu)
    add_track(net_map["I2C_SDA"], 25.0, 20.5, 21.9, 22.0, 0.2, pcbnew.F_Cu)
    add_track(net_map["I2C_SDA"], 21.9, 22.0, p_u1_9x, p_u1_9y, 0.2, pcbnew.F_Cu)

    # Route SDA on B.Cu to U3 pin 6 & U2 pin 6
    add_via(net_map["I2C_SDA"], 21.9, 22.0)
    add_track(net_map["I2C_SDA"], 21.9, 22.0, 9.5, 16.35, 0.2, pcbnew.B_Cu)
    add_via(net_map["I2C_SDA"], 9.5, 16.35)
    p_u3_6x, p_u3_6y = pad_pos("U3", "6")
    add_track(net_map["I2C_SDA"], 9.5, 16.35, p_u3_6x, p_u3_6y, 0.2, pcbnew.F_Cu)

    # SDA to U2 pin 6 (through neck at West edge)
    add_track(net_map["I2C_SDA"], 9.5, 16.35, 0.6, 16.35, 0.2, pcbnew.B_Cu)
    add_track(net_map["I2C_SDA"], 0.6, 16.35, 0.6, 5.5, 0.2, pcbnew.B_Cu)
    add_via(net_map["I2C_SDA"], 0.6, 5.5)
    p_u2_6x, p_u2_6y = pad_pos("U2", "6")
    add_track(net_map["I2C_SDA"], 0.6, 5.5, p_u2_6x, p_u2_6y, 0.2, pcbnew.F_Cu)

    # D. VCC_3V3 Power Trunk (0.35 mm width)
    # J1 pin 1 -> along East edge to J2 pin 1
    p_j1_1x, p_j1_1y = pad_pos("J1", "1")
    p_j2_1x, p_j2_1y = pad_pos("J2", "1")
    add_track(net_map["VCC_3V3"], p_j1_1x, p_j1_1y, 33.5, 12.0, 0.35, pcbnew.F_Cu)
    add_track(net_map["VCC_3V3"], 33.5, 12.0, 33.5, 27.0, 0.35, pcbnew.F_Cu)
    add_track(net_map["VCC_3V3"], 33.5, 27.0, p_j2_1x, p_j2_1y, 0.35, pcbnew.F_Cu)

    # VCC North Distribution Trunk (along Y = 4.5 mm)
    p_c5_1x, p_c5_1y = pad_pos("C5", "1")
    add_track(net_map["VCC_3V3"], p_j1_1x, p_j1_1y, 33.5, 4.5, 0.35, pcbnew.F_Cu)
    add_track(net_map["VCC_3V3"], 33.5, 4.5, p_c5_1x, p_c5_1y, 0.35, pcbnew.F_Cu)

    # C5 to C2 & U1 pin 17
    p_c2_1x, p_c2_1y = pad_pos("C2", "1")
    p_u1_17x, p_u1_17y = pad_pos("U1", "17")
    add_track(net_map["VCC_3V3"], p_c5_1x, p_c5_1y, p_c2_1x, p_c2_1y, 0.35, pcbnew.F_Cu)
    add_track(net_map["VCC_3V3"], p_c2_1x, p_c2_1y, p_u1_17x, p_u1_17y, 0.30, pcbnew.F_Cu)

    # C2 to C1 & R3
    p_c1_1x, p_c1_1y = pad_pos("C1", "1")
    p_r3_1x, p_r3_1y = pad_pos("R3", "1")
    add_track(net_map["VCC_3V3"], p_c2_1x, p_c2_1y, p_c1_1x, p_c1_1y, 0.30, pcbnew.F_Cu)
    add_track(net_map["VCC_3V3"], p_c1_1x, p_c1_1y, p_r3_1x, p_r3_1y, 0.25, pcbnew.F_Cu)

    # R3 pin 2 to U1 pin 18 (RESET_N)
    p_r3_2x, p_r3_2y = pad_pos("R3", "2")
    p_u1_18x, p_u1_18y = pad_pos("U1", "18")
    add_track(net_map["GNSS_RESET_N"], p_r3_2x, p_r3_2y, p_u1_18x, p_u1_18y, 0.20, pcbnew.F_Cu)

    # 3.3V to U1 pin 2 & 3 (V_IO & V_BCKP)
    p_u1_2x, p_u1_2y = pad_pos("U1", "2")
    p_u1_3x, p_u1_3y = pad_pos("U1", "3")
    add_track(net_map["VCC_3V3"], p_r3_1x, p_r3_1y, 13.4, 6.5, 0.25, pcbnew.F_Cu)
    add_track(net_map["VCC_3V3"], 13.4, 6.5, p_u1_2x, p_u1_2y, 0.25, pcbnew.F_Cu)
    add_track(net_map["VCC_3V3"], p_u1_2x, p_u1_2y, p_u1_3x, p_u1_3y, 0.25, pcbnew.F_Cu)

    # 3.3V to Pull-ups R1 & R2
    p_r1_1x, p_r1_1y = pad_pos("R1", "1")
    p_r2_1x, p_r2_1y = pad_pos("R2", "1")
    add_track(net_map["VCC_3V3"], 33.5, 18.0, p_r2_1x, p_r2_1y, 0.25, pcbnew.F_Cu)
    add_track(net_map["VCC_3V3"], p_r2_1x, p_r2_1y, p_r1_1x, p_r1_1y, 0.25, pcbnew.F_Cu)

    # 3.3V to C4 & U3 pin 2
    p_c4_1x, p_c4_1y = pad_pos("C4", "1")
    p_u3_2x, p_u3_2y = pad_pos("U3", "2")
    add_track(net_map["VCC_3V3"], p_u1_3x, p_u1_3y, p_c4_1x, p_c4_1y, 0.25, pcbnew.F_Cu)
    add_track(net_map["VCC_3V3"], p_c4_1x, p_c4_1y, p_u3_2x, p_u3_2y, 0.25, pcbnew.F_Cu)

    # 3.3V to TMP117 tongue: C3 pin 1 & U2 pin 5 (via neck)
    p_c3_1x, p_c3_1y = pad_pos("C3", "1")
    p_u2_5x, p_u2_5y = pad_pos("U2", "5")
    add_track(net_map["VCC_3V3"], 13.4, 6.5, 8.5, 2.0, 0.25, pcbnew.F_Cu)
    add_track(net_map["VCC_3V3"], 8.5, 2.0, 1.0, 2.0, 0.25, pcbnew.F_Cu)
    add_track(net_map["VCC_3V3"], 1.0, 2.0, 1.0, 4.5, 0.25, pcbnew.F_Cu)
    add_track(net_map["VCC_3V3"], 1.0, 4.5, p_c3_1x, p_c3_1y, 0.25, pcbnew.F_Cu)
    add_track(net_map["VCC_3V3"], p_c3_1x, p_c3_1y, p_u2_5x, p_u2_5y, 0.25, pcbnew.F_Cu)

    # 5. Silkscreen Markings
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

    add_silk("PCBA 05D // SENSOR PUCK", 17.0, 1.5, 0.75)
    add_silk("TMP117", 5.0, 2.0, 0.55)
    add_silk("OPT3001", 7.0, 20.0, 0.55)
    add_silk("SAM-M10Q GNSS", 20.0, 23.5, 0.60)
    add_silk("J1 IN", 31.0, 4.5, 0.55)
    add_silk("J2 EXP", 31.0, 29.5, 0.55)
    add_silk("OPENMOTORBRIDGE v10.0 // 34x34mm SENSOR PUCK", 17.0, 17.0, 0.80, pcbnew.B_SilkS, True)

    # 6. Solid Ground Planes (F_Cu and B_Cu)
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

    # 7. Ground Stitching Vias (strategically placed in clear areas to tie planes)
    stitching_vias = [
        (3.5, 12.0), (3.5, 24.0),
        (13.4, 23.0), (25.0, 23.0),
        (26.0, 5.0), (32.0, 6.0),
        (32.0, 23.0), (26.0, 26.5),
        (16.0, 30.5), (24.0, 30.5)
    ]
    for vx, vy in stitching_vias:
        add_via(gnd_net, vx, vy)

    # Zone Filler
    zf = pcbnew.ZONE_FILLER(board)
    zf.Fill(board.Zones())

    board.Save(PCB_PATH)
    print(f"Board successfully saved to {PCB_PATH}")

def main():
    os.makedirs(TARGET_DIR, exist_ok=True)
    create_project_file()
    create_schematic_file()
    build_pcb()

if __name__ == "__main__":
    main()
