#!/usr/bin/env python3
"""
OpenMotorBridge Central Main Board Layout Collision Detector & Top-Down Renderer
---------------------------------------------------------------------------------
Checks geometric bounding box intersections for all components on the 85x55 mm PCB
and renders a crisp 2D top-down diagram with millimeter grid.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def check_and_render_pcb(layout, output_path):
    # PCB Dimensions
    X0, Y0 = 115.22, 71.85
    W, H = 85.0, 55.0
    X_max, Y_max = X0 + W, Y0 + H

    # Component dimensions: {ref: (width_x, height_y, color, name)}
    dims = {
        # Active ICs & Modules
        'U2': (18.0, 25.5, '#3b82f6', 'ESP32-S3-WROOM-1'),
        'U1': (5.0, 6.0, '#f59e0b', 'LM5164-Q1 Buck'),
        'U9': (3.0, 2.8, '#f59e0b', 'TPS7A0533 LDO'),
        'U3': (4.0, 4.0, '#38bdf8', 'ES8388 Codec'),
        'U6': (5.0, 6.0, '#10b981', 'TCAN334G CAN'),
        'U5': (3.0, 2.5, '#a855f7', 'BMI270 IMU'),
        'U7': (4.5, 4.0, '#fbbf24', 'TLP222A Opto 1'),
        'U8': (4.5, 4.0, '#fbbf24', 'TLP222A Opto 2'),

        # Power & Passives
        'L1': (7.2, 4.5, '#d97706', '47uH Inductor'),
        'D2': (5.4, 3.6, '#ef4444', 'SMBJ33CA TVS'),
        'C1': (3.2, 2.5, '#94a3b8', '10uF 100V'),
        'C2': (2.0, 1.3, '#94a3b8', '22uF 16V'),
        'C3': (1.6, 0.8, '#94a3b8', 'C0603'),
        'C4': (1.6, 0.8, '#94a3b8', 'C0603'),
        'C6': (1.6, 0.8, '#94a3b8', 'C0603'),
        'C7': (1.6, 0.8, '#94a3b8', 'C0603'),
        'C10': (1.6, 0.8, '#94a3b8', 'C0603'),
        'C11': (2.0, 1.3, '#94a3b8', 'C0805'),
        'C12': (1.6, 0.8, '#94a3b8', 'C0603'),
        'R1': (1.6, 0.8, '#64748b', 'R0603'),
        'R2': (1.6, 0.8, '#64748b', 'R0603'),
        'R5': (1.6, 0.8, '#64748b', 'R0603'),
        'R6': (1.6, 0.8, '#64748b', 'R0603'),
        'R9': (1.6, 0.8, '#64748b', 'R0603'),
        'R10': (1.6, 0.8, '#64748b', 'R0603'),
        'R11': (1.6, 0.8, '#64748b', 'R0603'),
        'D1': (3.5, 3.5, '#10b981', 'WS2812B LED'),

        # Audio Transformers
        'T1': (12.5, 9.5, '#eab308', 'Bourns Trafo 1'),
        'T2': (12.5, 9.5, '#eab308', 'Bourns Trafo 2'),

        # Connectors & Storage
        'J2': (14.0, 14.5, '#475569', 'MicroSD Slot'),
        'J1': (6.0, 33.0, '#e2e8f0', 'IDC26 2x13 Header'),
        'J5': (6.0, 4.5, '#ef4444', 'JST-PH 2P Akku'),
        'J6': (2.5, 5.0, '#3b82f6', 'NTC 2P'),
        'J4': (2.5, 7.6, '#10b981', 'RGB 3P'),
        'J3': (9.0, 6.0, '#38bdf8', 'USB-C Vertical'),

        # Mounting Holes (Ø 6.0 mm keepout)
        'H1': (6.0, 6.0, '#334155', 'M3 Hole'),
        'H2': (6.0, 6.0, '#334155', 'M3 Hole'),
        'H3': (6.0, 6.0, '#334155', 'M3 Hole'),
        'H4': (6.0, 6.0, '#334155', 'M3 Hole'),
    }

    # 1. Collision Detection
    boxes = {}
    for ref, (cx, cy, rot) in layout.items():
        if ref in dims:
            w, h, _, _ = dims[ref]
            if int(rot) % 180 == 90:
                w, h = h, w # Swap width and height for 90/270 deg rotation
            actual_cx = cx + (15.24 if ref == 'J1' and cx < 160 else 0)
            boxes[ref] = (actual_cx - w/2, cy - h/2, actual_cx + w/2, cy + h/2)

    overlaps = []
    refs = list(boxes.keys())
    for i in range(len(refs)):
        for j in range(i + 1, len(refs)):
            r1, r2 = refs[i], refs[j]
            b1, b2 = boxes[r1], boxes[r2]
            # Check overlap with margin
            if not (b1[2] < b2[0] or b1[0] > b2[2] or b1[3] < b2[1] or b1[1] > b2[3]):
                overlaps.append((r1, r2))

    print(f"=== OVERLAP AUDIT ===")
    if overlaps:
        print(f"⚠️ FOUND {len(overlaps)} COMPONENT OVERLAPS:")
        for r1, r2 in overlaps:
            print(f"  • {r1} ({dims[r1][3]}) overlaps with {r2} ({dims[r2][3]})")
    else:
        print("✅ NO OVERLAPS FOUND! Clean layout.")

    # 2. Render 2D Top-Down View
    fig, ax = plt.subplots(figsize=(20, 13), dpi=220, facecolor='#080c14')
    ax.set_facecolor('#080c14')
    
    # Board Outline
    board_rect = patches.Rectangle((X0, Y0), W, H, linewidth=2.0, edgecolor='#10b981', facecolor='#064e3b', alpha=0.35)
    ax.add_patch(board_rect)
    
    # Grid lines
    for x in np.arange(X0, X_max + 1, 5):
        ax.axvline(x, color='#1e293b', linestyle='--', linewidth=0.5, alpha=0.7)
    for y in np.arange(Y0, Y_max + 1, 5):
        ax.axhline(y, color='#1e293b', linestyle='--', linewidth=0.5, alpha=0.7)

    # Zones background shading
    # Zone 2: Power (Top-Left)
    ax.add_patch(patches.Rectangle((X0 + 1, Y0 + 1), 38, 20, facecolor='#ef4444', alpha=0.07, edgecolor='#ef4444', linestyle=':'))
    ax.text(X0 + 2, Y0 + 4, "ZONE 2: POWER & USV", color='#f87171', fontsize=9, fontweight='bold')

    # Zone 1: Digital Core (Bottom-Left)
    ax.add_patch(patches.Rectangle((X0 + 1, Y0 + 22), 34, 28, facecolor='#3b82f6', alpha=0.07, edgecolor='#3b82f6', linestyle=':'))
    ax.text(X0 + 2, Y0 + 25, "ZONE 1: ESP32-S3 CORE", color='#60a5fa', fontsize=9, fontweight='bold')

    # Zone 5: IMU & Storage (Center)
    ax.add_patch(patches.Rectangle((X0 + 36, Y0 + 10), 20, 38, facecolor='#a855f7', alpha=0.07, edgecolor='#a855f7', linestyle=':'))
    ax.text(X0 + 37, Y0 + 13, "ZONE 5: IMU / SD", color='#c084fc', fontsize=9, fontweight='bold')

    # Zone 4: Audio & Isolation (Right)
    ax.add_patch(patches.Rectangle((X0 + 57, Y0 + 1), 27, 48, facecolor='#eab308', alpha=0.07, edgecolor='#eab308', linestyle=':'))
    ax.text(X0 + 58, Y0 + 4, "ZONE 4: GALV. AUDIO", color='#facc15', fontsize=9, fontweight='bold')

    # Draw Components
    for ref, (cx, cy, rot) in layout.items():
        if ref in dims:
            w, h, col, name = dims[ref]
            if int(rot) % 180 == 90:
                w, h = h, w
            actual_cx = cx + (15.24 if ref == 'J1' and cx < 160 else 0)
            is_overlap = any(ref in ov for ov in overlaps)
            edge_col = '#ff0055' if is_overlap else '#e2e8f0'
            line_w = 2.0 if is_overlap else 1.0
            
            # Box
            rect = patches.Rectangle((actual_cx - w/2, cy - h/2), w, h, linewidth=line_w, edgecolor=edge_col, facecolor=col, alpha=0.85)
            ax.add_patch(rect)
            
            # Label
            label_text = f"{ref}\n{name}" if w > 5 and h > 4 else f"{ref}"
            font_s = 7.5 if w > 10 else 6.0
            ax.text(actual_cx, cy, label_text, color='#ffffff', fontsize=font_s, fontweight='bold', ha='center', va='center')

    # Title & Legend
    ax.set_title("OPENMOTORBRIDGE v8.0 - ZENTRALPLATINE (85 x 55 mm) - TOP-DOWN BESTÜCKUNGSPLAN\n(Draufsicht mit Bauteil-Bounding-Boxes, Kollisionsprüfung & Zonen-Architektur)", 
                 color='#38bdf8', fontsize=13, fontweight='bold', pad=15)
    
    ax.set_xlim([X0 - 4, X_max + 4])
    ax.set_ylim([Y_max + 4, Y0 - 4]) # Invert Y so top is at top
    ax.set_xlabel("X Koordinate (mm)", color='#94a3b8', fontsize=10)
    ax.set_ylabel("Y Koordinate (mm)", color='#94a3b8', fontsize=10)
    ax.tick_params(colors='#94a3b8')

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor='#080c14')
    plt.close()
    print(f"✓ Saved top-down diagram to {output_path}")

if __name__ == "__main__":
    import re
    # Extract layout_rules from autoplace script without importing pcbnew
    with open('/Users/schmidtm/openMotorBridge/hardware/scripts/autoplace_openmotorbridge.py', 'r') as f:
        text = f.read()

    X0 = 115.22
    Y0 = 71.85
    W = 85.0
    H = 55.0
    X_max = X0 + W
    Y_max = Y0 + H

    # Evaluate layout_rules safely
    match = re.search(r'layout_rules = (\{.*?\n    \})', text, re.DOTALL)
    if match:
        layout_str = match.group(1)
        layout_rules = eval(layout_str, {"X0": X0, "Y0": Y0, "X_max": X_max, "Y_max": Y_max})
        check_and_render_pcb(layout_rules, "/Users/schmidtm/openMotorBridge/hardware/cad/main_board_pcb_top_down.png")
    else:
        print("Could not find layout_rules in autoplace script")
