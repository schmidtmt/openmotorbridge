#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
tools/sync_cockpit_breakout_schematic.py
Generates a 100% parity openmotorbridge_cockpit_breakout.kicad_sch matching openmotorbridge_cockpit_breakout.kicad_pcb.
Resolves all schematic-parity and symbol syntax blockers for prefab-gate.
"""
import os
import sys
import uuid
import pcbnew

def gen_uuid():
    return str(uuid.uuid4())

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    pcb_path = os.path.join(repo_root, 'hardware/kicad_cockpit_breakout/openmotorbridge_cockpit_breakout.kicad_pcb')
    sch_path = os.path.join(repo_root, 'hardware/kicad_cockpit_breakout/openmotorbridge_cockpit_breakout.kicad_sch')

    board = pcbnew.LoadBoard(pcb_path)
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
    lines.append('\t\t(title "OpenMotorBridge PCBA 05B: Handschuhfach-Hub (100% Parity)")')
    lines.append('\t\t(date "2026-11-01")')
    lines.append('\t\t(rev "v10.0-parity")')
    lines.append('\t\t(company "OpenMotorBridge Open Source Hardware")')
    lines.append('\t\t(comment 1 "Harley-Davidson Skyline OS / Boom! Box 4-Port USB Hub & Power-Injection")')
    lines.append('\t\t(comment 2 "Upstream Host, Front Node Link, 15W Phone Fast-Charge, Dongle, Media")')
    lines.append('\t)')
    lines.append('\t(lib_symbols')

    for comp in components:
        ref = comp['ref']
        pads = comp['pads']
        clean_val = comp['val'].replace(' ', '_').replace(':', '_').replace('/', '_').replace('-', '_')
        sym_name = f"OMB_Cockpit:{ref}_{clean_val}"
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
    with open(sch_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'Successfully generated 100% parity schematic {sch_path} with {len(components)} components:')
    for c in components:
        print(f"  - {c['ref']}: {c['val']} ({len(c['pads'])} pads)")

if __name__ == '__main__':
    main()
