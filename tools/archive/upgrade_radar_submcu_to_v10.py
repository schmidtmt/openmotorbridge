#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
tools/upgrade_radar_submcu_to_v10.py
====================================
Upgrades PCBA 08 (Radar 2.0 Sub-MCU & Wings) to OpenMotorBridge v10.0:
1. Strips all old segments and vias (user will review placement & route fresh in KiCad).
2. Removes obsolete footprints:
   - U3 (DW3110 UWB transceiver)
   - Y1_UWB (38.4MHz crystal)
   - J4 (Taoglas U.FL UWB antenna connector)
   - J3 (4-Pin PROG_UART header)
   - J1 (old 2-pin JWPF) -> Replaced by 4-Pin JST-GH SM04B-GHS-TB (12V, GND, BUS_DP, BUS_DM)
3. Connects ESP32-C5 native USB pins (Pad 16 = BUS_DM, Pad 17 = BUS_DP) to J1.
4. Updates openmotorbridge_radar_submcu.kicad_pro with v10 design rules:
   - min_copper_edge_clearance = 0.25 mm
   - min_resolved_spokes = 1
   - min_text_height = 0.5 mm
5. Generates 100% parity schematic openmotorbridge_radar_submcu.kicad_sch.
"""

import os
import sys
import re
import uuid
import pcbnew

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RADAR_DIR = os.path.join(REPO_ROOT, "hardware", "kicad_radar_submcu")
PCB_PATH = os.path.join(RADAR_DIR, "openmotorbridge_radar_submcu.kicad_pcb")
SCH_PATH = os.path.join(RADAR_DIR, "openmotorbridge_radar_submcu.kicad_sch")
PRO_PATH = os.path.join(RADAR_DIR, "openmotorbridge_radar_submcu.kicad_pro")
KICAD_FP_DIR = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"

OBSOLETE_REFS = {"U3", "Y1_UWB", "J4", "J3", "J1"}
OBSOLETE_NETS = {
    "UWB_RF", "UWB_SCK", "UWB_MOSI", "UWB_MISO",
    "UWB_CS", "UWB_IRQ", "UWB_RST", "UWB_CLK"
}

def to_nm(val):
    return int(round(val * 1e6))

def gen_uuid():
    return str(uuid.uuid4())

def parse_sexp_blocks(text):
    m = re.search(r'^\(kicad_pcb', text, re.MULTILINE)
    if not m:
        raise ValueError("Not a valid kicad_pcb file")

    idx = m.end()
    blocks = []
    header_part = text[:idx]

    while idx < len(text):
        while idx < len(text) and text[idx].isspace():
            idx += 1
        if idx >= len(text):
            break

        if text[idx] == ')':
            break

        if text[idx] == '(':
            start = idx
            depth = 1
            idx += 1
            in_str = False
            escape = False
            while idx < len(text) and depth > 0:
                c = text[idx]
                if escape:
                    escape = False
                elif c == '\\':
                    escape = True
                elif c == '"':
                    in_str = not in_str
                elif not in_str:
                    if c == '(':
                        depth += 1
                    elif c == ')':
                        depth -= 1
                idx += 1
            blocks.append(text[start:idx])
        else:
            idx += 1

    return header_part, blocks

def clean_and_rebuild_pcb():
    print(f"Reading {PCB_PATH}...")
    with open(PCB_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    header, blocks = parse_sexp_blocks(content)
    cleaned_blocks = []

    for b in blocks:
        m_tag = re.match(r'^\(\s*([a-zA-Z0-9_\.]+)', b)
        if not m_tag:
            cleaned_blocks.append(b)
            continue

        tag = m_tag.group(1)

        # 1. Strip all tracks and vias
        if tag in ("segment", "via", "arc"):
            continue

        # 2. Drop obsolete footprints
        if tag == "footprint":
            m_ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', b)
            if m_ref and m_ref.group(1) in OBSOLETE_REFS:
                continue

            # In U1 footprint, clear UWB nets
            if m_ref and m_ref.group(1) == "U1":
                for onet in OBSOLETE_NETS:
                    b = re.sub(rf'\(net\s+"\d+"\s+"{onet}"\)', '(net "0" "")', b)
                    b = re.sub(rf'\(net\s+"{onet}"\)', '(net "")', b)
                # Map Pad 16 to BUS_DM and Pad 17 to BUS_DP
                b = re.sub(r'\(pad\s+"16"\s+smd\s+rect\s+\(at\s+[-0-9\.]+\s+[-0-9\.]+\s*[-0-9\.]*\)\s+\(size\s+[-0-9\.]+\s+[-0-9\.]+\)\s+\(layers\s+"[^"]+"\s+"[^"]+"\s+"[^"]+"\)\s+\(net\s+"\d+"\s+"[^"]*"\)',
                           r'(pad "16" smd rect (at 7.5 5.5 180) (size 1.5 0.9) (layers "B.Cu" "B.Mask" "B.Paste") (net "BUS_DM"))', b)
                b = re.sub(r'\(pad\s+"17"\s+smd\s+rect\s+\(at\s+[-0-9\.]+\s+[-0-9\.]+\s*[-0-9\.]*\)\s+\(size\s+[-0-9\.]+\s+[-0-9\.]+\)\s+\(layers\s+"[^"]+"\s+"[^"]+"\s+"[^"]+"\)\s+\(net\s+"\d+"\s+"[^"]*"\)',
                           r'(pad "17" smd rect (at 7.5 6.77 180) (size 1.5 0.9) (layers "B.Cu" "B.Mask" "B.Paste") (net "BUS_DP"))', b)

        # 3. Clean net declarations for obsolete nets
        if tag == "net":
            m_net = re.match(r'^\(\s*net\s+\d+\s+"([^"]+)"', b)
            if m_net and m_net.group(1) in OBSOLETE_NETS:
                continue

        cleaned_blocks.append(b)

    out = header + "\n" + "\n".join("\t" + b for b in cleaned_blocks) + "\n)\n"
    with open(PCB_PATH, "w", encoding="utf-8") as f:
        f.write(out)
    print("Cleaned base PCB written.")

    # Now load with pcbnew to add clean 4-pin JST-GH connector J1 and configure nets
    board = pcbnew.LoadBoard(PCB_PATH)

    # Add nets
    for netname in ["VCC_12V", "BUS_DP", "BUS_DM"]:
        if not board.FindNet(netname):
            net = pcbnew.NETINFO_ITEM(board, netname)
            board.Add(net)

    net_12v = board.FindNet("VCC_12V")
    net_gnd = board.FindNet("GND")
    net_dp = board.FindNet("BUS_DP")
    net_dm = board.FindNet("BUS_DM")

    # Connect U1 native USB pads
    u1 = [fp for fp in board.GetFootprints() if fp.GetReference() == "U1"][0]
    for p in u1.Pads():
        if p.GetNumber() == "16":
            p.SetNet(net_dm)
        elif p.GetNumber() == "17":
            p.SetNet(net_dp)

    # Load and add J1 (JST-GH 4-Pin Horizontal)
    # Placed on right wing at (152.00, 112.75) rotated 90 degrees
    lib_path = os.path.join(KICAD_FP_DIR, "Connector_JST.pretty")
    j1 = pcbnew.FootprintLoad(lib_path, "JST_GH_SM04B-GHS-TB_1x04-1MP_P1.25mm_Horizontal")
    if j1 is None:
        raise RuntimeError("Could not load JST_GH footprint")

    j1.SetReference("J1")
    j1.SetValue("JST_GH_4P_BUS")
    j1.SetLayer(pcbnew.F_Cu)
    j1.SetPosition(pcbnew.VECTOR2I(to_nm(152.00), to_nm(112.75)))
    j1.SetOrientationDegrees(90.0)
    j1.Reference().SetVisible(True)
    j1.Value().SetVisible(False)

    for p in j1.Pads():
        pnum = p.GetNumber()
        if pnum == "1":
            p.SetNet(net_12v)
        elif pnum == "2":
            p.SetNet(net_gnd)
        elif pnum == "3":
            p.SetNet(net_dp)
        elif pnum == "4":
            p.SetNet(net_dm)
        else: # MP
            p.SetNet(net_gnd)

    board.Add(j1)
    board.Save(PCB_PATH)
    print(f"Added J1 (JST-GH 4-Pin) at (152.00, 112.75) and saved board.")
    return board

def update_pro_rules():
    print(f"Updating rules in {PRO_PATH}...")
    with open(PRO_PATH, "r", encoding="utf-8") as f:
        pro = f.read()

    pro = pro.replace('"min_copper_edge_clearance": 0.5', '"min_copper_edge_clearance": 0.25')
    pro = pro.replace('"min_resolved_spokes": 2', '"min_resolved_spokes": 1')
    pro = pro.replace('"min_text_height": 0.8', '"min_text_height": 0.5')

    with open(PRO_PATH, "w", encoding="utf-8") as f:
        f.write(pro)
    print("Project rules updated to v10 standards.")

def generate_v10_schematic(board):
    print(f"Generating 100% parity schematic from clean PCB...")
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
    lines.append('\t(paper "A1")')
    lines.append('\t(title_block')
    lines.append('\t\t(title "OpenMotorBridge PCBA 08: Radar 2.0 Sub-MCU & 36-LED Halo (v10.0)")')
    lines.append('\t\t(date "2026-11-01")')
    lines.append('\t\t(rev "v10.0")')
    lines.append('\t\t(company "OpenMotorBridge Open Source Hardware")')
    lines.append('\t\t(comment 1 "ESP32-C5 Dual-Band Sub-MCU (2.4/5GHz Wi-Fi 6 + 5.9GHz C-ITS/V2X)")')
    lines.append('\t\t(comment 2 "Wheeltec MR20 77-GHz mmWave Radar & 36-LED Warning Wings (4-Draht JST-GH)")')
    lines.append('\t)')
    lines.append('\t(lib_symbols')

    for comp in components:
        ref = comp['ref']
        pads = comp['pads']
        clean_val = comp['val'].replace(' ', '_').replace(':', '_').replace('/', '_').replace('-', '_')
        sym_name = f"OMB_Radar:{ref}_{clean_val}"
        comp['sym_name'] = sym_name

        c_ref = ref[0] if ref else "U"
        c_val = comp['val']
        c_fpid = comp['fpid']
        c_ds = comp['datasheet']
        c_desc = comp['description']

        in_bom_val = "no" if ref.startswith('H') else "yes"

        lines.append(f'\t\t(symbol "{sym_name}"')
        lines.append(f'\t\t\t(in_bom {in_bom_val}) (on_board yes)')
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
    max_y = 520.0

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
    print(f"Successfully generated 100% parity schematic with {len(components)} components.")

def main():
    board = clean_and_rebuild_pcb()
    update_pro_rules()
    generate_v10_schematic(board)
    print("\n🎉 PCBA 08 Radar Sub-MCU v10 preparation complete!")
    print("J1 is now 4-pin JST-GH (12V, GND, BUS_DP, BUS_DM) matching OMB architecture.")
    print("Ready for user inspection of placement & routing in KiCad.")

if __name__ == '__main__':
    main()
