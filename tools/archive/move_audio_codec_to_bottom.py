#!/usr/bin/env python3
"""
tools/move_audio_codec_to_bottom.py

Moves Everest Semi ES8388 Audio Codec (U3) to the bottom layer (B.Cu)
at (128.0, 80.0) on PCBA 03 (Universal Smart Cartridge):
- Eliminates any overlap on F.Cu
- Places U3 in the spacious, open ground shield plane on B.Cu
- Re-renders all 3D views and updates documentation images
"""

import uuid
import re
import subprocess
import os

def generate_uuid():
    return str(uuid.uuid4())

def move_u3_to_bcu():
    pcb_path = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"
    with open(pcb_path, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. Extract clean B.Cu template from openmotorbridge_main.kicad_pcb
    main_pcb = "hardware/kicad_main_box/openmotorbridge_main.kicad_pcb"
    with open(main_pcb, "r", encoding="utf-8") as f:
        mc = f.read()

    idx = mc.find('(property "Value" "ES8388_Codec"')
    fp_start = mc.rfind('(footprint "Package_DFN_QFN:QFN-28-1EP_4x4mm_P0.4mm_EP2.4x2.4mm"', 0, idx)
    cnt = 0
    fp_end = fp_start
    for i in range(fp_start, len(mc)):
        if mc[i] == '(': cnt += 1
        elif mc[i] == ')':
            cnt -= 1
            if cnt == 0:
                fp_end = i + 1
                break

    fp_template = mc[fp_start:fp_end]

    # Native B.Cu footprint, set position to (128.0 80.0 180)
    fp_bcu = re.sub(r'\(at [0-9\.\-]+ [0-9\.\-]+\)', '(at 128 80 180)', fp_template, count=1)
    
    # Assign fresh UUIDs
    def repl_uuid(match):
        return f'(uuid "{generate_uuid()}")'
    fp_bcu = re.sub(r'\(uuid \"[^\"]+\"\)', repl_uuid, fp_bcu)

    # 2. Remove existing U3 footprint from openmotorbridge_pod_cartridge.kicad_pcb
    idx_u3 = c.find('(property "Reference" "U3"')
    if idx_u3 != -1:
        u3_start = c.rfind('\t(footprint', 0, idx_u3)
        cnt = 0
        u3_end = u3_start
        for i in range(u3_start, len(c)):
            if c[i] == '(': cnt += 1
            elif c[i] == ')':
                cnt -= 1
                if cnt == 0:
                    u3_end = i + 1
                    break
        print(f"Removing old U3 footprint on F.Cu (bytes {u3_start} to {u3_end})...")
        c = c[:u3_start] + c[u3_end:]
    else:
        print("Existing U3 footprint not found, will insert new one.")

    # 3. Insert new U3 footprint on B.Cu right after U_UWB
    idx_uwb = c.find('(property "Reference" "U_UWB"')
    if idx_uwb != -1:
        uwb_start = c.rfind('\t(footprint', 0, idx_uwb)
        cnt = 0
        uwb_end = uwb_start
        for i in range(uwb_start, len(c)):
            if c[i] == '(': cnt += 1
            elif c[i] == ')':
                cnt -= 1
                if cnt == 0:
                    uwb_end = i + 1
                    break
        c = c[:uwb_end] + "\n\t" + fp_bcu + c[uwb_end:]
        print("Inserted U3 (ES8388 Audio Codec) on B.Cu at (128.0, 80.0).")
    else:
        m_last = c.rfind('\n\t(footprint')
        end_fp = c.find('\n\t)', m_last) + 3
        c = c[:end_fp] + "\n\t" + fp_bcu + c[end_fp:]
        print("Inserted U3 before Edge.Cuts.")

    with open(pcb_path, "w", encoding="utf-8") as f:
        f.write(c)

def refill_and_render():
    kicad_cli = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
    pcb_path = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"
    
    print("Refilling zones and saving board...")
    subprocess.run([kicad_cli, "pcb", "drc", "--refill-zones", "--save-board", pcb_path], check=True)

    print("Rendering 3D views...")
    # Bottom view (showing U3 ES8388 and U_UWB DW3110)
    subprocess.run([
        kicad_cli, "pcb", "render",
        "--side", "bottom",
        "--rotate", "45,0,45",
        "--zoom", "1.1",
        "--width", "1920", "--height", "1080",
        "-o", "hardware/kicad_pod_cartridge/cartridge_3d_render_bottom.png",
        pcb_path
    ], check=True)

    # Top view (clean F.Cu without any overlaps)
    subprocess.run([
        kicad_cli, "pcb", "render",
        "--side", "top",
        "--rotate", "-45,0,-45",
        "--zoom", "1.1",
        "--width", "1920", "--height", "1080",
        "-o", "hardware/kicad_pod_cartridge/cartridge_3d_render_top.png",
        pcb_path
    ], check=True)

    # Perspective view
    subprocess.run([
        kicad_cli, "pcb", "render",
        "--rotate", "-35,0,-25",
        "--zoom", "1.05",
        "--width", "1920", "--height", "1080",
        "-o", "hardware/kicad_pod_cartridge/cartridge_3d_render_perspective.png",
        pcb_path
    ], check=True)

    # kicad_3d_render.png
    subprocess.run([
        kicad_cli, "pcb", "render",
        "--rotate", "-45,0,-45",
        "--zoom", "1.1",
        "--width", "1280", "--height", "720",
        "-o", "hardware/kicad_pod_cartridge/kicad_3d_render.png",
        pcb_path
    ], check=True)

    # Copy to docs
    subprocess.run(["cp", "hardware/kicad_pod_cartridge/cartridge_3d_render_perspective.png",
                    "docs/images/pcba/pcba03_pod_cartridge_3d.png"], check=True)
    print("3D rendering and documentation sync complete.")

if __name__ == "__main__":
    move_u3_to_bcu()
    refill_and_render()
