#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
tools/build_mirror_pod_pcba.py
==============================
Builds the complete, production-ready KiCad 10 project for:
PCBA 05C: Bilateral-Symmetric Under-Perch Mirror Pod (openmotorbridge_mirror_pod)

Key Symmetry Architecture:
- 100% Bilaterally Symmetric across the central longitudinal axis (Y = 7.00 mm).
- One single, universal PCBA serves BOTH Left and Right motorcycle mirror perches.
- J1: 4-pin JST-GH Horizontal SMD connector on West edge (X = 5.25, Y = 7.00).
- H1: Single M2 central mounting hole at center (X = 16.00, Y = 7.00).
- LED1 & LED2: Dual 1206 Amber BSD Warning LEDs placed symmetrically
  above (Y = 11.20) and below (Y = 2.80) the central mounting hole.
- R1 & R2: Independent 150 Ohm series resistors for LED1 and LED2.
- SW1: Omron B3SL-1002P sealed IP67 tactile switch at East edge (X = 26.50, Y = 7.00).
- C1: 100 nF debounce capacitor.
- D1: SOD-323 TVS ESD protection diode.
"""

import os
import sys
import uuid
import pcbnew

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TARGET_DIR = os.path.join(REPO_ROOT, "hardware", "kicad_mirror_pod")
PRO_PATH = os.path.join(TARGET_DIR, "openmotorbridge_mirror_pod.kicad_pro")
SCH_PATH = os.path.join(TARGET_DIR, "openmotorbridge_mirror_pod.kicad_sch")
PCB_PATH = os.path.join(TARGET_DIR, "openmotorbridge_mirror_pod.kicad_pcb")

KICAD_FP_DIR = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"
KICAD_3D_DIR = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/3dmodels"

def to_nm(val):
    return int(round(val * 1e6))

def gen_uuid():
    return str(uuid.uuid4())

def create_project_file():
    os.makedirs(TARGET_DIR, exist_ok=True)
    pro_content = '''{
  "board": {
    "design_settings": {
      "defaults": {
        "board_outline_line_width": 0.15,
        "copper_line_width": 0.20,
        "silk_line_width": 0.12,
        "min_clearance": 0.15,
        "min_track_width": 0.20,
        "min_via_annular_width": 0.15,
        "min_through_drill": 0.3,
        "min_hole_clearance": 0.25,
        "min_copper_edge_clearance": 0.25
      },
      "rules": {
        "max_error": 0.005,
        "min_clearance": 0.15,
        "min_copper_edge_clearance": 0.25,
        "min_hole_clearance": 0.25,
        "min_hole_to_hole": 0.25,
        "min_text_height": 0.6,
        "min_text_thickness": 0.08,
        "min_through_hole_diameter": 0.3,
        "min_track_width": 0.20,
        "min_via_annular_width": 0.15,
        "min_via_diameter": 0.6,
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
    "filename": "openmotorbridge_mirror_pod.kicad_pro",
    "version": 1
  },
  "net_settings": {
    "classes": [
      {
        "clearance": 0.15,
        "name": "Default",
        "track_width": 0.25,
        "via_diameter": 0.6,
        "via_drill": 0.3
      },
      {
        "clearance": 0.20,
        "name": "Power",
        "track_width": 0.35,
        "via_diameter": 0.65,
        "via_drill": 0.35
      }
    ]
  },
  "sheets": [
    [
      "c005c000-0000-0000-0000-000000000001",
      ""
    ]
  ]
}
'''
    with open(PRO_PATH, "w", encoding="utf-8") as f:
        f.write(pro_content)
    print(f"Created {PRO_PATH}")

def build_pcb():
    board = pcbnew.BOARD()
    W, H = 32.0, 14.0

    net_names = [
        "", "GND", "VCC_LED", "BSD_LED_N", "BTN_SIG_N", "NET_LED1_ANODE", "NET_LED2_ANODE"
    ]

    net_map = {}
    for nname in net_names:
        net = pcbnew.NETINFO_ITEM(board, nname)
        board.Add(net)
        net_map[nname] = net

    # Edge.Cuts with 1.5mm chamfers
    pts = [
        (1.5, 0.0), (W - 1.5, 0.0), (W, 1.5), (W, H - 1.5),
        (W - 1.5, H), (1.5, H), (0.0, H - 1.5), (0.0, 1.5), (1.5, 0.0)
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
        fp.Reference().SetVisible(False)
        fp.Value().SetVisible(False)

        if model_3d:
            full_model = os.path.join(KICAD_3D_DIR, model_3d)
            if os.path.exists(full_model):
                models = fp.Models()
                if len(models) > 0:
                    models[0].m_Filename = full_model
                else:
                    m = pcbnew.FP_3DMODEL()
                    m.m_Filename = full_model
                    fp.Add3DModel(m)

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

    # 1. J1: JST-GH 4-Pin Horizontal SMD (centered at X = 5.25, Y = 7.00)
    # Rot = 270: Solder pads face East (+X), cable entry from West (X=0)
    place_fp(
        "Connector_JST.pretty", "JST_GH_SM04B-GHS-TB_1x04-1MP_P1.25mm_Horizontal",
        "J1", "JST_GH_4P_POD",
        5.25, 7.00, 270.0,
        {
            "1": "VCC_LED",
            "2": "BSD_LED_N",
            "3": "BTN_SIG_N",
            "4": "GND",
            "MP": "GND"
        },
        model_3d="Connector_JST.3dshapes/JST_GH_SM04B-GHS-TB_1x04-1MP_P1.25mm_Horizontal.step"
    )

    # 2. H1: Central Single M2 Mounting Hole (centered at X = 16.00, Y = 7.00)
    place_fp(
        "MountingHole.pretty", "MountingHole_2.2mm_M2_Pad",
        "H1", "M2",
        16.00, 7.00, 0.0,
        {"1": "GND"}
    )

    # 3. LED1: Upper 1206 Amber BSD Warning LED (Y = 11.20)
    # Pad 1 = Cathode (BSD_LED_N), Pad 2 = Anode (NET_LED1_ANODE)
    place_fp(
        "LED_SMD.pretty", "LED_1206_3216Metric",
        "LED1", "AMBER_590NM",
        16.00, 11.20, 0.0,
        {
            "1": "BSD_LED_N",
            "2": "NET_LED1_ANODE"
        },
        model_3d="LED_SMD.3dshapes/LED_1206_3216Metric.step"
    )

    # 4. LED2: Lower 1206 Amber BSD Warning LED (Y = 2.80)
    # Pad 1 = Cathode (BSD_LED_N), Pad 2 = Anode (NET_LED2_ANODE)
    place_fp(
        "LED_SMD.pretty", "LED_1206_3216Metric",
        "LED2", "AMBER_590NM",
        16.00, 2.80, 0.0,
        {
            "1": "BSD_LED_N",
            "2": "NET_LED2_ANODE"
        },
        model_3d="LED_SMD.3dshapes/LED_1206_3216Metric.step"
    )

    # 5. R1: Series Resistor for LED1 (150 Ohm 0603 at Y = 11.20)
    place_fp(
        "Resistor_SMD.pretty", "R_0603_1608Metric",
        "R1", "150R",
        20.50, 11.20, 0.0,
        {
            "1": "NET_LED1_ANODE",
            "2": "VCC_LED"
        },
        model_3d="Resistor_SMD.3dshapes/R_0603_1608Metric.step"
    )

    # 6. R2: Series Resistor for LED2 (150 Ohm 0603 at Y = 2.80)
    place_fp(
        "Resistor_SMD.pretty", "R_0603_1608Metric",
        "R2", "150R",
        20.50, 2.80, 0.0,
        {
            "1": "NET_LED2_ANODE",
            "2": "VCC_LED"
        },
        model_3d="Resistor_SMD.3dshapes/R_0603_1608Metric.step"
    )

    # 7. SW1: Omron B3SL-1002P Tactile Switch at East Edge (centered at X = 26.50, Y = 7.00)
    place_fp(
        "Button_Switch_SMD.pretty", "SW_SPST_B3SL-1002P",
        "SW1", "PTT_CAM_SW",
        26.50, 7.00, 0.0,
        {
            "1": "GND",
            "2": "BTN_SIG_N"
        },
        model_3d="Button_Switch_SMD.3dshapes/SW_SPST_B3SL-1002P.step"
    )

    # 8. C1: Debounce Capacitor (100nF 0603 at upper channel)
    place_fp(
        "Capacitor_SMD.pretty", "C_0603_1608Metric",
        "C1", "100nF",
        10.50, 10.00, 0.0,
        {
            "1": "BTN_SIG_N",
            "2": "GND"
        },
        model_3d="Capacitor_SMD.3dshapes/C_0603_1608Metric.step"
    )

    # 9. D1: TVS ESD Diode (SOD-323 at lower channel)
    place_fp(
        "Diode_SMD.pretty", "D_SOD-323",
        "D1", "PESD5V0S1BL",
        10.50, 4.00, 0.0,
        {
            "1": "BTN_SIG_N",
            "2": "GND"
        },
        model_3d="Diode_SMD.3dshapes/D_SOD-323.step"
    )

    # Clean non-overlapping Silkscreen
    def add_silk_text(text, x, y, size=0.6, thick=0.10):
        t = pcbnew.PCB_TEXT(board)
        t.SetText(text)
        t.SetPosition(pcbnew.VECTOR2I(to_nm(x), to_nm(y)))
        t.SetTextSize(pcbnew.VECTOR2I(to_nm(size), to_nm(size)))
        t.SetTextThickness(to_nm(thick))
        t.SetLayer(pcbnew.F_SilkS)
        board.Add(t)
        return t

    add_silk_text("PCBA 05C // SYMMETRIC", 16.0, 0.9, size=0.55, thick=0.09)
    add_silk_text("OMB BSD", 16.0, 13.1, size=0.55, thick=0.09)
    add_silk_text("SW1", 26.5, 2.6, size=0.6, thick=0.10)
    add_silk_text("J1", 5.25, 2.6, size=0.6, thick=0.10)

    # Routing helper
    def add_track(layer, net_name, x1, y1, x2, y2, width=0.25):
        t = pcbnew.PCB_TRACK(board)
        t.SetStart(pcbnew.VECTOR2I(to_nm(x1), to_nm(y1)))
        t.SetEnd(pcbnew.VECTOR2I(to_nm(x2), to_nm(y2)))
        t.SetWidth(to_nm(width))
        t.SetLayer(layer)
        t.SetNet(net_map[net_name])
        board.Add(t)
        return t

    def add_via(net_name, x, y):
        v = pcbnew.PCB_VIA(board)
        v.SetPosition(pcbnew.VECTOR2I(to_nm(x), to_nm(y)))
        v.SetWidth(to_nm(0.6))
        v.SetDrill(to_nm(0.3))
        v.SetNet(net_map[net_name])
        board.Add(v)
        return v

    # Coordinates:
    # J1: (5.25, 7.00), Rot 270
    # J1 Pad 1 (VCC_LED): (7.10, 5.125)
    # J1 Pad 2 (BSD_LED_N): (7.10, 6.375)
    # J1 Pad 3 (BTN_SIG_N): (7.10, 7.625)
    # J1 Pad 4 (GND): (7.10, 8.875)

    # Route 1: VCC_LED
    # From J1 Pad 1 (7.10, 5.125) -> routes to R2 (Pad 2 at 21.25, 2.80) along lower corridor Y=1.5
    add_track(pcbnew.F_Cu, "VCC_LED", 7.10, 5.125, 7.50, 4.00, 0.30)
    add_track(pcbnew.F_Cu, "VCC_LED", 7.50, 4.00, 7.50, 1.80, 0.30)
    add_track(pcbnew.F_Cu, "VCC_LED", 7.50, 1.80, 21.25, 1.80, 0.30)
    add_track(pcbnew.F_Cu, "VCC_LED", 21.25, 1.80, 21.25, 2.80, 0.30)

    # Branch to R1 (Pad 2 at 21.25, 11.20) via B_Cu
    add_via("VCC_LED", 7.50, 1.80)
    add_track(pcbnew.B_Cu, "VCC_LED", 7.50, 1.80, 7.50, 12.20, 0.30)
    add_via("VCC_LED", 7.50, 12.20)
    add_track(pcbnew.F_Cu, "VCC_LED", 7.50, 12.20, 21.25, 12.20, 0.30)
    add_track(pcbnew.F_Cu, "VCC_LED", 21.25, 12.20, 21.25, 11.20, 0.30)

    # Route 2: NET_LED1_ANODE
    # R1 Pad 1 (19.75, 11.20) -> LED1 Pad 2 (17.40, 11.20)
    add_track(pcbnew.F_Cu, "NET_LED1_ANODE", 19.75, 11.20, 17.40, 11.20, 0.25)

    # Route 3: NET_LED2_ANODE
    # R2 Pad 1 (19.75, 2.80) -> LED2 Pad 2 (17.40, 2.80)
    add_track(pcbnew.F_Cu, "NET_LED2_ANODE", 19.75, 2.80, 17.40, 2.80, 0.25)

    # Route 4: BSD_LED_N
    # From J1 Pad 2 (7.10, 6.375) -> split to LED1 (Pad 1 at 14.60, 11.20) and LED2 (Pad 1 at 14.60, 2.80)
    add_track(pcbnew.F_Cu, "BSD_LED_N", 7.10, 6.375, 8.50, 6.375, 0.25)
    # Lower branch to LED2
    add_track(pcbnew.F_Cu, "BSD_LED_N", 8.50, 6.375, 9.50, 5.00, 0.25)
    add_track(pcbnew.F_Cu, "BSD_LED_N", 9.50, 5.00, 13.00, 5.00, 0.25)
    add_track(pcbnew.F_Cu, "BSD_LED_N", 13.00, 5.00, 14.60, 3.40, 0.25)
    add_track(pcbnew.F_Cu, "BSD_LED_N", 14.60, 3.40, 14.60, 2.80, 0.25)
    # Upper branch to LED1
    add_via("BSD_LED_N", 8.50, 6.375)
    add_track(pcbnew.B_Cu, "BSD_LED_N", 8.50, 6.375, 13.00, 9.00, 0.25)
    add_via("BSD_LED_N", 13.00, 9.00)
    add_track(pcbnew.F_Cu, "BSD_LED_N", 13.00, 9.00, 14.60, 10.60, 0.25)
    add_track(pcbnew.F_Cu, "BSD_LED_N", 14.60, 10.60, 14.60, 11.20, 0.25)

    # Route 5: BTN_SIG_N
    # From J1 Pad 3 (7.10, 7.625) -> C1 Pad 1 (9.75, 10.00) & D1 Pad 1 (9.75, 4.00)
    add_track(pcbnew.F_Cu, "BTN_SIG_N", 7.10, 7.625, 8.20, 7.625, 0.25)
    add_track(pcbnew.F_Cu, "BTN_SIG_N", 8.20, 7.625, 9.75, 9.175, 0.25)
    add_track(pcbnew.F_Cu, "BTN_SIG_N", 9.75, 9.175, 9.75, 10.00, 0.25)

    # To D1 Pad 1 via B_Cu
    add_via("BTN_SIG_N", 8.20, 7.625)
    add_track(pcbnew.B_Cu, "BTN_SIG_N", 8.20, 7.625, 9.75, 4.00, 0.25)
    add_via("BTN_SIG_N", 9.75, 4.00)

    # From C1 / D1 to SW1 Pad 2 (23.625, 9.00) via B_Cu under center
    add_track(pcbnew.B_Cu, "BTN_SIG_N", 8.20, 7.625, 11.00, 7.00, 0.25)
    # Route safely around H1 hole (H1 is at 16.0, 7.0)
    add_track(pcbnew.B_Cu, "BTN_SIG_N", 11.00, 7.00, 13.50, 7.00, 0.25)
    add_track(pcbnew.B_Cu, "BTN_SIG_N", 13.50, 7.00, 16.00, 4.60, 0.25)
    add_track(pcbnew.B_Cu, "BTN_SIG_N", 16.00, 4.60, 18.50, 7.00, 0.25)
    add_track(pcbnew.B_Cu, "BTN_SIG_N", 18.50, 7.00, 22.00, 7.00, 0.25)
    add_track(pcbnew.B_Cu, "BTN_SIG_N", 22.00, 7.00, 23.625, 8.625, 0.25)
    add_via("BTN_SIG_N", 23.625, 8.625)
    add_track(pcbnew.F_Cu, "BTN_SIG_N", 23.625, 8.625, 23.625, 9.00, 0.25)

    # Ground Copper Zones on F.Cu and B.Cu
    for layer in [pcbnew.F_Cu, pcbnew.B_Cu]:
        zone = pcbnew.ZONE(board)
        zone.SetLayer(layer)
        zone.SetNet(net_map["GND"])
        zone.SetLocalClearance(to_nm(0.25))
        zone.SetMinThickness(to_nm(0.20))
        zone.SetThermalReliefGap(to_nm(0.20))
        zone.SetThermalReliefSpokeWidth(to_nm(0.25))

        outline = pcbnew.SHAPE_LINE_CHAIN()
        outline.Append(to_nm(0.0), to_nm(0.0))
        outline.Append(to_nm(W), to_nm(0.0))
        outline.Append(to_nm(W), to_nm(H))
        outline.Append(to_nm(0.0), to_nm(H))
        outline.Append(to_nm(0.0), to_nm(0.0))
        outline.SetClosed(True)
        zone.AddPolygon(outline)
        board.Add(zone)

    # Refill zones
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())

    board.Save(PCB_PATH)
    print(f"✓ Saved bilateral-symmetric PCB to {PCB_PATH}")
    return board

def generate_schematic(board):
    fps = sorted(board.GetFootprints(), key=lambda x: x.GetReference())
    components = []

    for fp in fps:
        ref = fp.GetReference()
        val = fp.GetValue()
        fpid = fp.GetFPID().GetUniStringLibId()
        fields = {f.GetName(): f.GetText() for f in fp.GetFields()}
        datasheet = fields.get('Datasheet', '')
        description = fields.get('Description', '')

        pads_map = {}
        for p in fp.Pads():
            pnum = p.GetNumber()
            if not pnum:
                continue
            net = p.GetNetname()
            if pnum not in pads_map:
                pads_map[pnum] = net
            elif not pads_map[pnum] and net:
                pads_map[pnum] = net

        components.append({
            'ref': ref,
            'val': val,
            'fpid': fpid,
            'datasheet': datasheet,
            'description': description,
            'pads': pads_map
        })

    lines = []
    lines.append('(kicad_sch')
    lines.append('\t(version 20260306)')
    lines.append('\t(generator "eeschema")')
    lines.append('\t(generator_version "10.0")')
    lines.append(f'\t(uuid "{gen_uuid()}")')
    lines.append('\t(paper "A3")')
    lines.append('\t(title_block')
    lines.append('\t\t(title "OpenMotorBridge PCBA 05C: Universal Bilateral-Symmetric Under-Perch Pod")')
    lines.append('\t\t(date "2026-11-03")')
    lines.append('\t\t(rev "v10.1-symmetric")')
    lines.append('\t\t(company "OpenMotorBridge Open Source Hardware")')
    lines.append('\t\t(comment 1 "Dual Amber BSD LEDs (LED1/LED2), Central M2 Hole, Omron B3SL IP67 Switch")')
    lines.append('\t\t(comment 2 "Universal 1-PCB for both Left & Right Mirror Perch Pods")')
    lines.append('\t)')
    lines.append('\t(lib_symbols')

    for comp in components:
        ref = comp['ref']
        pads = comp['pads']
        clean_val = comp['val'].replace(' ', '_').replace(':', '_').replace('/', '_')
        sym_name = f"OMB_MirrorPod:{ref}_{clean_val}"
        comp['sym_name'] = sym_name

        c_ref = ref[0] if ref else "U"
        c_val = comp['val']
        c_fpid = comp['fpid']
        c_ds = comp['datasheet']
        c_desc = comp['description']

        lines.append(f'\t\t(symbol "{sym_name}"')
        lines.append('\t\t\t(in_bom yes) (on_board yes)')
        lines.append(f'\t\t\t(property "Reference" "{c_ref}" (at 0 0 0) (effects (font (size 1.27 1.27))))')
        lines.append(f'\t\t\t(property "Value" "{c_val}" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))')
        lines.append(f'\t\t\t(property "Footprint" "{c_fpid}" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))')
        lines.append(f'\t\t\t(property "Datasheet" "{c_ds}" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))')
        lines.append(f'\t\t\t(property "Description" "{c_desc}" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))')

        sorted_pnums = sorted(pads.keys(), key=lambda x: (int(x) if x.isdigit() else 999, x))
        for idx, pnum in enumerate(sorted_pnums):
            py = -idx * 2.54
            lines.append(f'\t\t\t(pin passive line (at -5.08 {py:.2f} 0) (length 2.54) (name "{pnum}" (effects (font (size 1.27 1.27)))) (number "{pnum}" (effects (font (size 1.27 1.27)))))')
        lines.append('\t\t)')

    lines.append('\t)')
    lines.append('')

    cur_x = 40.0
    cur_y = 40.0
    col_width = 65.0
    max_y = 260.0

    for comp in components:
        ref = comp['ref']
        val = comp['val']
        fpid = comp['fpid']
        sym_name = comp['sym_name']
        c_ds = comp['datasheet']
        c_desc = comp['description']
        pads = comp['pads']
        sorted_pnums = sorted(pads.keys(), key=lambda x: (int(x) if x.isdigit() else 999, x))

        comp_h = max(len(sorted_pnums) * 2.54 + 15.0, 20.0)
        if cur_y + comp_h > max_y:
            cur_y = 40.0
            cur_x += col_width

        in_bom_val = "no" if ref.startswith('H') else "yes"
        sym_uuid = gen_uuid()
        lines.append(f'\t(symbol (lib_id "{sym_name}") (at {cur_x:.2f} {cur_y:.2f} 0) (unit 1)')
        lines.append(f'\t\t(in_bom {in_bom_val}) (on_board yes) (dnp no)')
        lines.append(f'\t\t(uuid "{sym_uuid}")')
        lines.append(f'\t\t(property "Reference" "{ref}" (at {cur_x:.2f} {cur_y - 5.0:.2f} 0) (effects (font (size 1.27 1.27))))')
        lines.append(f'\t\t(property "Value" "{val}" (at {cur_x:.2f} {cur_y - 2.5:.2f} 0) (effects (font (size 1.27 1.27))))')
        lines.append(f'\t\t(property "Footprint" "{fpid}" (at {cur_x:.2f} {cur_y:.2f} 0) (effects (font (size 1.27 1.27)) hide))')
        lines.append(f'\t\t(property "Datasheet" "{c_ds}" (at {cur_x:.2f} {cur_y:.2f} 0) (effects (font (size 1.27 1.27)) hide))')
        lines.append(f'\t\t(property "Description" "{c_desc}" (at {cur_x:.2f} {cur_y:.2f} 0) (effects (font (size 1.27 1.27)) hide))')

        for pnum in sorted_pnums:
            pin_uuid = gen_uuid()
            lines.append(f'\t\t(pin "{pnum}" (uuid "{pin_uuid}"))')
        lines.append('\t)')

        for idx, pnum in enumerate(sorted_pnums):
            net = pads[pnum]
            if not net:
                continue
            px = cur_x - 5.08
            py = cur_y + idx * 2.54
            lines.append(f'\t(global_label "{net}" (shape bidirectional) (at {px:.2f} {py:.2f} 180) (effects (font (size 1.27 1.27))))')

        cur_y += comp_h

    lines.append('\t(sheet_instances')
    lines.append('\t\t(path "/" (page "1"))')
    lines.append('\t)')
    lines.append(')')
    lines.append('')

    content = '\n'.join(lines)
    with open(SCH_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Generated 100% parity schematic {SCH_PATH}")

def main():
    print("Building OpenMotorBridge PCBA 05C (Bilateral-Symmetric Mirror Pod)...")
    create_project_file()
    board = build_pcb()
    generate_schematic(board)
    print("PCBA 05C bilateral-symmetric build complete!")

if __name__ == '__main__':
    main()
