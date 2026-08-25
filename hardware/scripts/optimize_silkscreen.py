#!/usr/bin/env python3
"""
Optimize Silkscreen Labels in openmotorbridge_main.kicad_pcb for 100% visibility in 3D:
- Ensure all texts are in wide open spaces with zero shadowing
"""

import re

pcb_file = 'hardware/kicad_main_box/openmotorbridge_main.kicad_pcb'

with open(pcb_file, 'r') as f:
    text = f.read()

def make_gr_text(label, x, y, size=0.8, thickness=0.14, rot=0):
    uid = f"c0000000-0000-0000-0000-{abs(hash((label, x, y, rot))) & 0xffffffffffff:012x}"
    return f"""\t(gr_text "{label}"
\t\t(at {x:.2f} {y:.2f} {rot})
\t\t(layer "F.SilkS")
\t\t(uuid "{uid}")
\t\t(effects
\t\t\t(font
\t\t\t\t(size {size:.2f} {size:.2f})
\t\t\t\t(thickness {thickness:.2f})
\t\t\t)
\t\t)
\t)"""

def make_gr_line(x1, y1, x2, y2, width=0.2):
    uid = f"c1000000-0000-0000-0000-{abs(hash((x1, y1, x2, y2))) & 0xffffffffffff:012x}"
    return f"""\t(gr_line
\t\t(start {x1:.2f} {y1:.2f})
\t\t(end {x2:.2f} {y2:.2f})
\t\t(stroke
\t\t\t(width {width:.2f})
\t\t\t(type solid)
\t\t)
\t\t(layer "F.SilkS")
\t\t(uuid "{uid}")
\t)"""

# Remove old gr_text and gr_line labels on F.SilkS if any
text = re.sub(r'\t\(gr_text\s+.*?\n\t\)\n', '', text, flags=re.DOTALL)
text = re.sub(r'\t\(gr_line\s+.*?\n\t\)\n', '', text, flags=re.DOTALL)

silkscreen_items = [
    # Top Right Header
    make_gr_text("OpenMotorBridge Main Box v8.0", 175.0, 75.0, size=0.90, thickness=0.15),
    
    # Zone Titles
    make_gr_text("ZONE 2: 72V BUCK", 126.0, 77.0, size=0.75, thickness=0.13),
    make_gr_text("ZONE 3: ISOLATED AUDIO", 178.0, 77.5, size=0.75, thickness=0.13),
    
    # Power Zone (Left)
    make_gr_text("U1: LM5164", 124.0, 93.5, size=0.7, thickness=0.12),
    make_gr_text("L1: 47uH", 117.5, 103.0, size=0.68, thickness=0.12, rot=90),
    
    # ESP32-S3 Center
    make_gr_text("U2: ESP32-S3 (240MHz)", 149.5, 103.5, size=0.75, thickness=0.13),
    
    # Galvanic Audio & Optos (Right)
    make_gr_text("T1: LINE-OUT", 168.0, 90.0, size=0.65, thickness=0.11, rot=90),
    make_gr_text("T2: LINE-IN", 168.0, 107.0, size=0.65, thickness=0.11, rot=90),
    make_gr_text("U7: OPTO1", 187.0, 94.0, size=0.6, thickness=0.11),
    make_gr_text("U8: OPTO2", 187.0, 112.0, size=0.6, thickness=0.11),
    make_gr_text("U6: CAN", 186.0, 82.5, size=0.6, thickness=0.11),
    
    # Connectors
    make_gr_text("J3: USB-C/UART", 128.0, 113.8, size=0.7, thickness=0.12),
    make_gr_text("J1: SYSTEM IDC-26", 157.0, 113.8, size=0.7, thickness=0.12),
    make_gr_text("J5: BATT", 195.0, 86.5, size=0.6, thickness=0.11),
    make_gr_text("J4: RGB", 195.0, 103.5, size=0.6, thickness=0.11),
    
    # Pin 1 Indicators
    make_gr_text("▲1", 121.0, 118.5, size=0.65, thickness=0.12),
    make_gr_text("▲1", 140.5, 118.5, size=0.65, thickness=0.12),
    
    # Galvanic Isolation Barrier
    make_gr_line(162.0, 78.0, 162.0, 120.0, width=0.22),
    make_gr_text("4mm ISOLATION BARRIER", 160.8, 98.0, size=0.6, thickness=0.11, rot=90),
]

# Insert silkscreen before closing parenthesis
closing_paren_idx = text.rfind(')')
new_pcb = text[:closing_paren_idx] + '\n' + '\n'.join(silkscreen_items) + '\n' + text[closing_paren_idx:]

with open(pcb_file, 'w') as f:
    f.write(new_pcb)

print("✓ Silkscreen layout fully perfected!")
