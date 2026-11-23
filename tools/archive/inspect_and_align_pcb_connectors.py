#!/usr/bin/env python3
"""
inspect_and_align_pcb_connectors.py - OpenMotorBridge PCB Connector Alignment Tool

Analysiert die Steckerpositionen an den Kanten der KiCad-Platinen (z. B. Front Node PCBA 05),
deckt Kanten-Versätze und ungleichmäßige Spaltmaße durch Maus-Rasterung auf und berechnet
mathematisch harmonisierte Zielkoordinaten.

Option:
    --board [front_node|main_box|pod_cartridge|radar_submcu|all]
    --apply : Führt die berechnete Kanten-Ausrichtung im .kicad_pcb File aus (erstellt Backup *.bak).

Usage:
    python3 tools/inspect_and_align_pcb_connectors.py --board front_node
    python3 tools/inspect_and_align_pcb_connectors.py --board front_node --apply
"""

import sys
import os
import re
import math
import shutil
import argparse

BOARDS = {
    'front_node': {
        'name': 'Front Node (PCBA 05)',
        'file': 'hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb',
        'outline_expected': {'w': 82.0, 'h': 50.0, 'x_min': 100.0, 'x_max': 182.0, 'y_min': 70.0, 'y_max': 120.0},
        'alignments': {
            # Obere Kante: Auf einheitliche Fluchtlinie Y=73.500 setzen (50µm Versatz beheben) + J9 Lücke harmonisieren
            'J9':  {'x': 125.750, 'y': 73.500, 'rot': 0.0,   'desc': 'Flucht Y=73.500 + Spaltmaß zu J3 exakt 1.60 mm'},
            'J1':  {'x': 146.750, 'y': 73.500, 'rot': 0.0,   'desc': 'Flucht Y=73.500 (50µm Höhenversatz behoben)'},
            'J10': {'x': 153.750, 'y': 73.500, 'rot': 0.0,   'desc': 'Flucht Y=73.500 (50µm Höhenversatz behoben)'},
            'J11': {'x': 160.750, 'y': 73.500, 'rot': 0.0,   'desc': 'Flucht Y=73.500 (50µm Höhenversatz behoben)'},
            'J2':  {'x': 167.750, 'y': 73.500, 'rot': 0.0,   'desc': 'Flucht Y=73.500 (50µm Höhenversatz behoben)'},
            # Untere Kante: Spaltmaße der USB-Reihe auf einheitlich exakt 1.60 mm harmonisieren
            'J5':  {'x': 128.750, 'y': 116.000, 'rot': 180.0, 'desc': 'Spaltmaß zu J4 auf exakt 1.60 mm harmonisiert (-0.25 mm)'},
            'J6':  {'x': 140.250, 'y': 116.000, 'rot': 180.0, 'desc': 'Spaltmaß zu J5 auf exakt 1.60 mm harmonisiert (-0.25 mm)'},
            # Rechte Kante: USB-C Servicebuchse von 104.930 auf sauberes 0.5mm-Raster 105.000 glätten
            'J7':  {'x': 177.700, 'y': 105.000, 'rot': 90.0,  'desc': 'Y von 104.930 auf 105.000 geglättet (0.5mm Raster)'},
        }
    },
    'pod_cartridge': {
        'name': 'Pod Cartridge (PCBA 03)',
        'file': 'hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb',
        'outline_expected': {'w': 35.0, 'h': 25.0, 'x_min': 100.0, 'x_max': 135.0, 'y_min': 67.5, 'y_max': 92.5},
        'alignments': {
            'J_ACT': {'x': 132.000, 'y': 80.200, 'rot': 90.0, 'desc': 'X von 131.870 auf 132.000 geglättet (Kantenabstand exakt 3.00 mm)'},
        }
    },
    'main_box': {
        'name': 'Central Box (PCBA 01)',
        'file': 'hardware/kicad_main_box/openmotorbridge_main.kicad_pcb',
        'outline_expected': {'w': 85.0, 'h': 55.0, 'x_min': 115.22, 'x_max': 200.22, 'y_min': 71.85, 'y_max': 126.85},
        'alignments': {}
    },
    'radar_submcu': {
        'name': 'Radar Sub-MCU (PCBA 08)',
        'file': 'hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb',
        'outline_expected': {'w': 115.0, 'h': 65.0, 'x_min': 42.5, 'x_max': 157.5, 'y_min': 67.5, 'y_max': 132.5},
        'alignments': {}
    }
}

# JST-PH Shroud Breite W = (N-1)*2.0 + 3.9 mm
def jst_ph_width(n_pins):
    return (n_pins - 1) * 2.0 + 3.9

def analyze_board(key, config):
    filepath = config['file']
    if not os.path.exists(filepath):
        print(f"[ERROR] Datei nicht gefunden: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"\n================================================================================")
    print(f" PLATINEN-ANALYSE: {config['name']}")
    print(f" Datei: {filepath}")
    print(f"================================================================================")

    # Footprints parsen
    fps = re.findall(r'\(footprint\s+\"([^\"]+)\"\s+(.*?)\n\t\)', content, re.DOTALL)
    conns = []
    for fp_name, body in fps:
        ref_m = re.search(r'\(property\s+\"Reference\"\s+\"([^\"]+)\"', body)
        val_m = re.search(r'\(property\s+\"Value\"\s+\"([^\"]+)\"', body)
        at_m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)', body)
        if not (ref_m and at_m):
            continue
        ref = ref_m.group(1)
        val = val_m.group(1) if val_m else ''
        x = float(at_m.group(1))
        y = float(at_m.group(2))
        rot = float(at_m.group(3)) if at_m.group(3) else 0.0

        if ref.startswith('J') or 'conn' in fp_name.lower() or 'usb' in fp_name.lower():
            pads = re.findall(r'\(pad\s+\"([^\"]+)\"', body)
            n_pins = len([p for p in set(pads) if p.isdigit()])
            if n_pins == 0:
                n_pins = 2
            conns.append({
                'ref': ref, 'val': val, 'x': x, 'y': y, 'rot': rot,
                'fp': fp_name, 'n_pins': n_pins
            })

    exp = config['outline_expected']
    print(f"Platinen-Umriss (Soll): {exp['w']:.2f} x {exp['h']:.2f} mm | X: [{exp['x_min']:.2f}..{exp['x_max']:.2f}], Y: [{exp['y_min']:.2f}..{exp['y_max']:.2f}]\n")

    top_conns, bottom_conns, right_conns, left_conns = [], [], [], []

    for c in conns:
        d_top = abs(c['y'] - exp['y_min'])
        d_bottom = abs(c['y'] - exp['y_max'])
        d_left = abs(c['x'] - exp['x_min'])
        d_right = abs(c['x'] - exp['x_max'])
        min_d = min(d_top, d_bottom, d_left, d_right)

        if min_d == d_top:
            c['edge'] = 'TOP'; c['edge_dist'] = d_top; top_conns.append(c)
        elif min_d == d_bottom:
            c['edge'] = 'BOTTOM'; c['edge_dist'] = d_bottom; bottom_conns.append(c)
        elif min_d == d_left:
            c['edge'] = 'LEFT'; c['edge_dist'] = d_left; left_conns.append(c)
        else:
            c['edge'] = 'RIGHT'; c['edge_dist'] = d_right; right_conns.append(c)

    for edge_name, clist in [('OBERE KANTE (Y={:.2f} mm)'.format(exp['y_min']), sorted(top_conns, key=lambda x: x['x'])),
                             ('UNTERE KANTE (Y={:.2f} mm)'.format(exp['y_max']), sorted(bottom_conns, key=lambda x: x['x'])),
                             ('RECHTE KANTE (X={:.2f} mm)'.format(exp['x_max']), sorted(right_conns, key=lambda x: x['y'])),
                             ('LINKE KANTE (X={:.2f} mm)'.format(exp['x_min']), sorted(left_conns, key=lambda x: x['y']))]:
        if not clist:
            continue
        print(f"--- {edge_name} [{len(clist)} Verbinder] ---")
        prev = None
        for c in clist:
            w = jst_ph_width(c['n_pins'])
            c_offset = (c['n_pins'] - 1) * 1.0
            rad = math.radians(c['rot'])
            cx = c['x'] + c_offset * math.cos(rad)
            cy = c['y'] + c_offset * math.sin(rad)

            gap_info = ""
            if prev is not None:
                if 'OBERE' in edge_name or 'UNTERE' in edge_name:
                    pitch = cx - prev['cx']
                    clearance = (cx - w/2.0) - (prev['cx'] + prev['w']/2.0)
                    gap_info = f" | Pitch zu {prev['ref']:6s}: {pitch:5.2f} mm, Freiraum (Luft): {clearance:5.2f} mm"
                else:
                    pitch = cy - prev['cy']
                    gap_info = f" | Pitch zu {prev['ref']:6s}: {pitch:5.2f} mm"

            print(f"  * {c['ref']:8s} ({c['val']:20s}): Pin1=({c['x']:7.3f}, {c['y']:7.3f}) -> Center=({cx:7.3f}, {cy:7.3f}) Rot={c['rot']:5.1f} | Kantenabstand={c['edge_dist']:5.3f} mm{gap_info}")
            c['cx'] = cx
            c['cy'] = cy
            c['w'] = w
            prev = c
        print()

def apply_alignment(key, config):
    filepath = config['file']
    alignments = config.get('alignments', {})
    if not alignments:
        print(f"[{config['name']}] Keine Anpassungen erforderlich - alles bereits exakt ausgerichtet.")
        return

    print(f"\n>>> WENDE AUSRICHTUNG AN: {config['name']} ({len(alignments)} Anpassungen)")
    backup_file = filepath + ".bak"
    shutil.copy2(filepath, backup_file)
    print(f"  [BACKUP] Sicherungskopie erstellt: {backup_file}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified_count = 0
    for ref, target in alignments.items():
        # Suche den Footprint-Block fuer diese Reference
        pattern = r'(\(footprint\s+\"[^\"]+\"\s+(?:(?!\(footprint\s+).)*?\(property\s+\"Reference\"\s+\"' + re.escape(ref) + r'\".*?\n\t\))'
        m = re.search(pattern, content, re.DOTALL)
        if not m:
            print(f"  [WARNUNG] Footprint '{ref}' nicht gefunden!")
            continue

        block = m.group(1)
        # Suche (at X Y [ROT]) im Block
        at_pattern = r'\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)'
        at_m = re.search(at_pattern, block)
        if not at_m:
            print(f"  [WARNUNG] (at ...) in Footprint '{ref}' nicht gefunden!")
            continue

        old_at_str = at_m.group(0)
        old_x = float(at_m.group(1))
        old_y = float(at_m.group(2))
        old_rot = float(at_m.group(3)) if at_m.group(3) else 0.0

        new_x = target['x']
        new_y = target['y']
        new_rot = target.get('rot', old_rot)

        if new_rot != 0.0:
            new_at_str = f"(at {new_x:.3f} {new_y:.3f} {new_rot:.1f})"
        else:
            new_at_str = f"(at {new_x:.3f} {new_y:.3f})"

        new_block = block.replace(old_at_str, new_at_str, 1)
        content = content.replace(block, new_block, 1)
        modified_count += 1
        print(f"  [ALIGNED] {ref:8s}: {old_at_str} -> {new_at_str} ({target['desc']})")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[ERFOLG] {modified_count} Verbinder in {filepath} mathematisch sauber ausgerichtet!\n")

def main():
    parser = argparse.ArgumentParser(description="OpenMotorBridge PCB Connector Alignment Inspection & Application")
    parser.add_argument('--board', choices=['front_node', 'main_box', 'pod_cartridge', 'radar_submcu', 'all'], default='all')
    parser.add_argument('--apply', action='store_true', help="Ausrichtung anwenden und .kicad_pcb Datei patchen")
    args = parser.parse_args()

    if args.apply:
        if args.board == 'all':
            for b in BOARDS:
                apply_alignment(b, BOARDS[b])
        else:
            apply_alignment(args.board, BOARDS[args.board])
    else:
        if args.board == 'all':
            for b in BOARDS:
                analyze_board(b, BOARDS[b])
        else:
            analyze_board(args.board, BOARDS[args.board])

if __name__ == '__main__':
    main()
