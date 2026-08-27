#!/usr/bin/env python3
"""
Set exact JLCPCB Board Setup Constraints in .kicad_pcb files
------------------------------------------------------------
Injects:
- min_clearance: 0.127 mm (5 mil) / 0.15 mm
- min_track_width: 0.15 mm (6 mil) / 0.20 mm
- min_through_drill: 0.30 mm
- min_via_annular_width: 0.15 mm (min via size = 0.60 mm)
- min_hole_clearance: 0.25 mm
- min_copper_edge_clearance: 0.30 mm
"""

import re

BOARDS = [
    {
        "name": "Main Board",
        "file": "hardware/kicad_main_box/openmotorbridge_main.kicad_pcb",
        "min_w": 0.15,
        "min_clr": 0.127
    },
    {
        "name": "Pod Base",
        "file": "hardware/kicad_pod_base/openmotorbridge_pod_base.kicad_pcb",
        "min_w": 0.20,
        "min_clr": 0.15
    },
    {
        "name": "Pod Cartridge",
        "file": "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb",
        "min_w": 0.20,
        "min_clr": 0.15
    },
    {
        "name": "Rear Pod 3",
        "file": "hardware/kicad_rear_pod3/openmotorbridge_rear_pod3.kicad_pcb",
        "min_w": 0.15,
        "min_clr": 0.127
    }
]

def update_setup_constraints(item):
    pcb_path = item["file"]
    with open(pcb_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Remove existing constraint fields in setup block if any
    for k in ["min_clearance", "min_track_width", "min_via_annular_width", "min_through_drill", "min_hole_clearance", "min_copper_edge_clearance"]:
        content = re.sub(rf'\t\t\({k}\s+[^\)]+\)\n', '', content)
        
    constraints_block = f"""\t\t(min_clearance {item['min_clr']})
\t\t(min_track_width {item['min_w']})
\t\t(min_via_annular_width 0.15)
\t\t(min_through_drill 0.3)
\t\t(min_hole_clearance 0.25)
\t\t(min_copper_edge_clearance 0.3)
"""
    # Insert right after (setup
    m = re.search(r'(\t\(setup\n)', content)
    if m:
        idx = m.end()
        content = content[:idx] + constraints_block + content[idx:]
        
    with open(pcb_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Configured JLCPCB Board Setup constraints in {item['name']} ({pcb_path})")

def main():
    for item in BOARDS:
        update_setup_constraints(item)
    print("\n🎉 All 4 PCB files now have explicit JLCPCB Constraints in Board Setup!")

if __name__ == '__main__':
    main()
