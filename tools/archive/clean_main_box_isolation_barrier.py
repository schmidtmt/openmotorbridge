#!/usr/bin/env python3
"""
tools/clean_main_box_isolation_barrier.py

Removes legacy audio isolation barrier artifacts from PCBA 01 (Central Box):
1. In openmotorbridge_main.kicad_pcb:
   - Remove 4mm separation line at X=162 on F.SilkS
   - Remove legacy silkscreen texts:
     - "4mm ISOLATION BARRIER"
     - "ZONE 3: ISOLATED AUDIO"
     - "T1: LINE-OUT"
     - "T2: LINE-IN"
     - "U7: OPTO1"
     - "U8: OPTO2"
   - Merge split zone on In1.Cu (/Audio-Frontend & Opto/POD1_NF_N) to solid GND_PWR
2. In openmotorbridge_main.kicad_sch:
   - Remove Sheet 3 (Audio-Frontend & Opto / audio_frontend_isolated.kicad_sch)
   - Update Sheet 4 to Deutsch DTM-12 Interface with exact 12 pins
   - Update Title Block comment from 'HD26 26-Pin Matrix' to 'Deutsch DTM-12 Matrix'
"""

import os
import re
import shutil

def backup(path):
    bak = path + ".bak_barrier"
    if not os.path.exists(bak):
        shutil.copyfile(path, bak)
        print(f"[BACKUP] Created {bak}")

def clean_pcb():
    pcb_path = "hardware/kicad_main_box/openmotorbridge_main.kicad_pcb"
    backup(pcb_path)
    
    with open(pcb_path, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. Remove separation line (gr_line (start 162 78) (end 162 120) ... (layer "F.SilkS"))
    c = re.sub(
        r'\t\(gr_line\s+\(start 162 78\)\s+\(end 162 120\)\s+\(stroke\s+\(width 0\.22\)\s+\(type solid\)\s+\)\s+\(layer \"F\.SilkS\"\)\s+\(uuid \"[^\"]+\"\)\s+\)\n',
        '',
        c
    )

    # 2. Remove legacy isolation texts
    legacy_texts = [
        "4mm ISOLATION BARRIER",
        "ZONE 3: ISOLATED AUDIO",
        "T1: LINE-OUT",
        "T2: LINE-IN",
        "U7: OPTO1",
        "U8: OPTO2"
    ]
    for txt in legacy_texts:
        pattern = rf'\t\(gr_text \"{re.escape(txt)}\".*?\n\t\)\n'
        c = re.sub(pattern, '', c, flags=re.DOTALL)

    # 3. Update zone net on In1.Cu from /Audio-Frontend & Opto/POD1_NF_N to GND_PWR
    c = c.replace('"/Audio-Frontend & Opto/POD1_NF_N"', '"GND_PWR"')

    with open(pcb_path, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"[SUCCESS] Cleaned {pcb_path}")

def clean_sch():
    sch_path = "hardware/kicad_main_box/openmotorbridge_main.kicad_sch"
    backup(sch_path)

    with open(sch_path, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. Update Title Block comment
    c = c.replace(
        '(comment 2 "HD26 26-Pin Matrix, ES8388 24-Bit Codec, TCAN334G CAN-FD")',
        '(comment 2 "Deutsch DTM-12 Automotive Matrix, ES8388 DSP Codec, TCAN334G CAN-FD, Qorvo DW3110 UWB")'
    )

    # 2. Remove sheet "Audio-Frontend & Opto"
    # Match the sheet block for audio_frontend_isolated.kicad_sch
    c = re.sub(
        r'\t\(sheet\s+\(at [0-9.-]+ [0-9.-]+\)\s+\(size [0-9.-]+ [0-9.-]+\).*?\(property \"Sheetfile\" \"audio_frontend_isolated\.kicad_sch\".*?\n\t\)\n',
        '',
        c,
        flags=re.DOTALL
    )

    # 3. Update Sheet "HD26 Flansch & 2x13 Header" to "Deutsch DTM-12 Power & CAN Interface"
    c = c.replace(
        '(property "Sheetname" "HD26 Flansch & 2x13 Header"',
        '(property "Sheetname" "Deutsch DTM-12 Power & CAN Interface"'
    )

    with open(sch_path, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"[SUCCESS] Cleaned {sch_path}")

if __name__ == "__main__":
    clean_pcb()
    clean_sch()
