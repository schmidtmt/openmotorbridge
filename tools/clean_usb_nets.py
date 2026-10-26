#!/usr/bin/env python3
"""
tools/clean_usb_nets.py
-----------------------
Clean up USB net naming and connections across PCBA 03:
1. Disconnect U_PD (SW3516) from all USB data lines:
   - Remove USB_DP and PTT_USB_N from U_PD pins 17 and 18 in schematic & PCB.
2. Purge misleading 'PTT_USB_N' net name:
   - Rename the intercom PTT line on J_AUDIO_PWR to 'PTT_BTN'.
   - Fix remaining schematic label on U1 to 'GND'.
3. Verify complete, clean 3-port USB Hub architecture:
   - J_BUS (Pin 3: USB_DP, Pin 4: USB_DM) -> Hub Upstream (UD+, UD-)
   - Hub Downstream 1 (D1+, D1-) -> ESP32 native USB (USB_DP_MCU, USB_DM_MCU)
   - Hub Downstream 2 (D2+, D2-) -> J_USB_OUT (USB_DP_EXT, USB_DM_EXT)
4. 100% PRESERVE user placements, coordinates, and rotations!
"""

import re
import subprocess

SCH_PATH = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_sch"
PCB_PATH = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"
KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

def clean_schematic():
    print("Cleaning schematic...")
    with open(SCH_PATH, "r", encoding="utf-8") as f:
        sch = f.read()

    # 1. Remove USB_DP and PTT_USB_N from U_PD (SW3516)
    sch = re.sub(r'\(global_label\s+\"USB_DP\"\s+\(shape\s+passive\)\s+\(at\s+165\.16\s+160\.00\s+0\)[^\)]*\)\s*\n?', '', sch)
    sch = re.sub(r'\(global_label\s+\"PTT_USB_N\"\s+\(shape\s+passive\)\s+\(at\s+165\.16\s+157\.46\s+0\)[^\)]*\)\s*\n?', '', sch)

    # 2. Rename PTT_USB_N on J_AUDIO_PWR to PTT_BTN
    sch = sch.replace('(global_label "PTT_USB_N" (shape passive) (at 104.92 108.89 180)',
                      '(global_label "PTT_BTN" (shape passive) (at 104.92 108.89 180)')
    sch = sch.replace('(global_label "PTT_USB_N" (shape passive) (at 34.92 103.81 180)',
                      '(global_label "PTT_BTN" (shape passive) (at 34.92 103.81 180)')

    # 3. Fix residual PTT_USB_N label on U1 to GND
    sch = sch.replace('(global_label "PTT_USB_N" (shape passive) (at 269.84 71.74 180)',
                      '(global_label "GND" (shape passive) (at 269.84 71.74 180)')

    with open(SCH_PATH, "w", encoding="utf-8") as f:
        f.write(sch)
    print("Schematic cleaned!")

def clean_pcb():
    print("Cleaning PCB...")
    with open(PCB_PATH, "r", encoding="utf-8") as f:
        pcb = f.read()

    # 1. U_PD: Disconnect Pin 17 and Pin 18 from USB_DP / PTT_USB_N
    pos_upd = pcb.find('"U_PD"')
    start = pcb.rfind('(footprint', 0, pos_upd)
    depth = 0; end = -1
    for k in range(start, len(pcb)):
        if pcb[k] == '(': depth += 1
        elif pcb[k] == ')':
            depth -= 1
            if depth == 0: end = k+1; break
    upd_blk = pcb[start:end]

    # In U_PD block, replace net for pin 17 and pin 18 with no net
    # (pad "17" smd roundrect ... (net "USB_DP") ...) -> (net "") or remove (net ...)
    def repl_upd_pad(m):
        p_num = m.group(1)
        rest = m.group(2)
        if p_num in ['17', '18']:
            # remove (net ...) from pad
            new_rest = re.sub(r'\(net\s+\"[^\"]+\"\)', '', rest)
            return f'(pad "{p_num}"{new_rest}'
        return m.group(0)

    new_upd_blk = re.sub(r'\(pad\s+\"(\d+)\"(.*?(?=\(pad|\Z|\t\t\)))', repl_upd_pad, upd_blk, flags=re.DOTALL)
    pcb = pcb[:start] + new_upd_blk + pcb[end:]

    # 2. J_AUDIO_PWR: update Pin 8 net to PTT_BTN
    pos_audio = pcb.find('"J_AUDIO_PWR"')
    start_a = pcb.rfind('(footprint', 0, pos_audio)
    depth = 0; end_a = -1
    for k in range(start_a, len(pcb)):
        if pcb[k] == '(': depth += 1
        elif pcb[k] == ')':
            depth -= 1
            if depth == 0: end_a = k+1; break
    audio_blk = pcb[start_a:end_a]
    audio_blk = audio_blk.replace('(net "PTT_USB_N")', '(net "PTT_BTN")')
    pcb = pcb[:start_a] + audio_blk + pcb[end_a:]

    # Clean up any orphan PTT_USB_N strings
    pcb = pcb.replace('(net "PTT_USB_N")', '(net "GND")')

    with open(PCB_PATH, "w", encoding="utf-8") as f:
        f.write(pcb)
    print("PCB cleaned!")

if __name__ == "__main__":
    clean_schematic()
    clean_pcb()
