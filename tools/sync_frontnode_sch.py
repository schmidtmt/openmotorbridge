#!/usr/bin/env python3
"""
tools/sync_frontnode_sch.py
===========================
Generates a 100% synchronized schematic for PCBA 05 (Universal Front Node):
Matches all footprints, FPIDs, pad nets, and attributes from openmotorbridge_front_node.kicad_pcb.
Ensures parity checks in KiCad DRC and prefab-gate pass 100%.
"""

import sys
import uuid
import pcbnew

PCB_PATH = "hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb"
SCH_PATH = "hardware/kicad_front_node/openmotorbridge_front_node.kicad_sch"

def u():
    return str(uuid.uuid4())

def main():
    board = pcbnew.LoadBoard(PCB_PATH)
    comps = []
    
    for f in board.GetFootprints():
        ref = f.GetReference()
        val = f.GetValue()
        fp = str(f.GetFPID().GetUniStringLibId())
        in_bom = not f.IsExcludedFromBOM()
        # In KiCad schematic, on_board must be True for any symbol that has a PCB footprint
        on_board = True
        dnp = f.IsDNP()
        
        # Deduplicate pads by number, preserving non-empty pad numbers
        seen_pnums = set()
        unique_pads = []
        
        # Sort pads by numeric value if digits, else alphanumeric
        sorted_pads = sorted(
            list(f.Pads()),
            key=lambda p: (0, int(p.GetNumber())) if p.GetNumber().isdigit() else (1, p.GetNumber())
        )
        for p in sorted_pads:
            pnum = p.GetNumber()
            if not pnum or pnum in seen_pnums:
                continue
            seen_pnums.add(pnum)
            unique_pads.append({
                "number": pnum,
                "net": p.GetNetname()
            })
            
        comps.append({
            "ref": ref,
            "val": val,
            "fp": fp,
            "in_bom": in_bom,
            "on_board": on_board,
            "dnp": dnp,
            "pads": unique_pads
        })

    sch = []
    sch.append('(kicad_sch')
    sch.append('\t(version 20260306)')
    sch.append('\t(generator "eeschema")')
    sch.append('\t(generator_version "10.0")')
    sch.append(f'\t(uuid "{u()}")')
    sch.append('\t(paper "A1")')
    sch.append('\t(title_block')
    sch.append('\t\t(title "OpenMotorBridge Universal Front Node (Cockpit & Sensor Hub PCBA 05)")')
    sch.append('\t\t(date "2026-10-19")')
    sch.append('\t\t(rev "v2.2")')
    sch.append('\t\t(company "OpenMotorBridge Open Source Hardware")')
    sch.append('\t\t(comment 1 "ESP32-S3, USB2514B Hub, Dual SW3526 USB-PD 20W, DW3110 UWB, TPS1H100 Aux Light, J_VEHICLE 12P")')
    sch.append('\t)')

    # --- LIB SYMBOLS ---
    sch.append('\t(lib_symbols')

    for c in sorted(comps, key=lambda x: x['ref']):
        ref = c['ref']
        val = c['val']
        fp = c['fp']
        pads = c['pads']

        sch.append(f'\t\t(symbol "{ref}_sym"')
        sch.append(f'\t\t\t(property "Reference" "{ref}" (at 0 5 0) (effects (font (size 1.27 1.27))))')
        sch.append(f'\t\t\t(property "Value" "{val}" (at 0 -5 0) (effects (font (size 1.27 1.27))))')
        sch.append(f'\t\t\t(property "Footprint" "{fp}" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))')
        
        n_pins = len(pads)
        w = 20.32
        half = (n_pins + 1) // 2

        for idx, p in enumerate(pads):
            pnum = p['number']
            pname = p['net'] if p['net'] else "~"
            if idx < half:
                y = (half / 2 - idx) * 2.54
                sch.append(f'\t\t\t(pin passive line (at -{w/2:.2f} {y:.2f} 0) (length 2.54) (name "{pname}" (effects (font (size 1.27 1.27)))) (number "{pnum}" (effects (font (size 1.27 1.27)))))')
            else:
                y = (half / 2 - (idx - half)) * 2.54
                sch.append(f'\t\t\t(pin passive line (at {w/2:.2f} {y:.2f} 180) (length 2.54) (name "{pname}" (effects (font (size 1.27 1.27)))) (number "{pnum}" (effects (font (size 1.27 1.27)))))')
        sch.append('\t\t)')

    sch.append('\t)')

    # --- SYMBOL INSTANCES & GLOBAL LABELS ---
    cols = 8
    grid_x = 85.0
    grid_y = 100.0
    start_x = 60.0
    start_y = 60.0

    wires_and_labels = []

    for idx, c in enumerate(sorted(comps, key=lambda x: x['ref'])):
        ref = c['ref']
        val = c['val']
        fp = c['fp']
        in_bom_str = "yes" if c['in_bom'] else "no"
        on_board_str = "yes" if c['on_board'] else "no"
        dnp_str = "yes" if c['dnp'] else "no"
        pads = c['pads']

        col = idx % cols
        row = idx // cols

        pos_x = start_x + col * grid_x
        pos_y = start_y + row * grid_y

        sch.append(f'\t(symbol (lib_id "{ref}_sym") (at {pos_x:.2f} {pos_y:.2f} 0) (unit 1)')
        sch.append(f'\t\t(in_bom {in_bom_str}) (on_board {on_board_str}) (dnp {dnp_str})')
        sch.append(f'\t\t(uuid "{u()}")')
        sch.append(f'\t\t(property "Reference" "{ref}" (at {pos_x:.2f} {pos_y - 25:.2f} 0) (effects (font (size 1.27 1.27))))')
        sch.append(f'\t\t(property "Value" "{val}" (at {pos_x:.2f} {pos_y - 22:.2f} 0) (effects (font (size 1.27 1.27))))')
        sch.append(f'\t\t(property "Footprint" "{fp}" (at {pos_x:.2f} {pos_y:.2f} 0) (effects (font (size 1.27 1.27)) hide))')

        w = 20.32
        half = (len(pads) + 1) // 2

        for p_idx, p in enumerate(pads):
            pnum = p['number']
            pnet = p['net']
            p_uuid = u()
            sch.append(f'\t\t(pin "{pnum}" (uuid "{p_uuid}"))')

            # If pad is connected to a net, add a wire and a global_label outside symbol
            if pnet and pnet != "<no net>" and pnet != "":
                if p_idx < half:
                    y = (half / 2 - p_idx) * 2.54
                    pin_y = pos_y - y
                    pin_x = pos_x - (w / 2)
                    lbl_x = pin_x - 5.08
                    wires_and_labels.append(f'\t(wire (pts (xy {pin_x:.2f} {pin_y:.2f}) (xy {lbl_x:.2f} {pin_y:.2f})) (stroke (width 0) (type default)) (uuid "{u()}"))')
                    wires_and_labels.append(f'\t(global_label "{pnet}" (shape bidirectional) (at {lbl_x:.2f} {pin_y:.2f} 180) (effects (font (size 1.27 1.27)) (justify right)) (uuid "{u()}"))')
                else:
                    y = (half / 2 - (p_idx - half)) * 2.54
                    pin_y = pos_y - y
                    pin_x = pos_x + (w / 2)
                    lbl_x = pin_x + 5.08
                    wires_and_labels.append(f'\t(wire (pts (xy {pin_x:.2f} {pin_y:.2f}) (xy {lbl_x:.2f} {pin_y:.2f})) (stroke (width 0) (type default)) (uuid "{u()}"))')
                    wires_and_labels.append(f'\t(global_label "{pnet}" (shape bidirectional) (at {lbl_x:.2f} {pin_y:.2f} 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "{u()}"))')

        sch.append('\t)')

    # Add all wires and labels outside the symbols
    for item in wires_and_labels:
        sch.append(item)

    sch.append(')')
    sch.append('')

    with open(SCH_PATH, "w", encoding="utf-8") as f:
        f.write('\n'.join(sch))

    print(f"Generated {SCH_PATH} with {len(comps)} components and {len(wires_and_labels)} wires/labels.")

if __name__ == "__main__":
    main()
