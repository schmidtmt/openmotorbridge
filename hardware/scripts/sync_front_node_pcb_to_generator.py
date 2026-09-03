#!/usr/bin/env python3
"""
Sync Front Node Final PCB Placement to Generator Script
-------------------------------------------------------
Extracts exact footprint (X, Y, Rotation) coordinates from
`openmotorbridge_front_node.kicad_pcb` and updates the component
table in `generate_front_node_project.py`.
"""

import re

PCB_PATH = "hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb"
GEN_PATH = "hardware/scripts/generate_front_node_project.py"

def extract_placements():
    with open(PCB_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Match footprints: (footprint ... (at X Y [ROT]) ... (property "Reference" "REF"
    # Or in KiCad 10 format:
    fp_pattern = re.compile(
        r'\(footprint\s+"[^"]+"[\s\S]*?\(at\s+([\d.-]+)\s+([\d.-]+)(?:\s+([\d.-]+))?\)[\s\S]*?\(property\s+"Reference"\s+"([^"]+)"',
        re.MULTILINE
    )

    placements = {}
    for m in fp_pattern.finditer(content):
        x, y, rot, ref = m.groups()
        rot = float(rot) if rot is not None else 0.0
        placements[ref] = (float(x), float(y), rot)

    print(f"Extracted placement for {len(placements)} components from PCB:")
    for ref, (x, y, rot) in sorted(placements.items()):
        print(f"  {ref:6s} -> ({x:6.2f}, {y:6.2f}, rot={rot:5.1f})")

    return placements

def update_generator(placements):
    with open(GEN_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    # Pattern to match lines like:
    # ("Connector_JST.pretty", "JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", "J1", "OPT_12V_ACC", 104.5, 80.0, 0,
    comp_line_pattern = re.compile(
        r'(\s*\("[^"]+",\s*"[^"]+",\s*"([^"]+)",\s*"[^"]*",\s*)([\d.-]+),\s*([\d.-]+),\s*([\d.-]+)(,.*)'
    )

    updated_count = 0
    for line in lines:
        m = comp_line_pattern.match(line)
        if m:
            prefix, ref, old_x, old_y, old_rot, suffix = m.groups()
            if ref in placements:
                new_x, new_y, new_rot = placements[ref]
                # Format with 1 or 2 decimals
                rot_str = f"{int(new_rot)}" if new_rot.is_integer() else f"{new_rot:.1f}"
                new_line = f"{prefix}{new_x:.2f}, {new_y:.2f}, {rot_str}{suffix}\n"
                updated_lines.append(new_line)
                updated_count += 1
                continue
        updated_lines.append(line)

    with open(GEN_PATH, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

    print(f"✓ Updated {updated_count} component positions in {GEN_PATH}")

if __name__ == "__main__":
    placements = extract_placements()
    update_generator(placements)
