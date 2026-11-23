#!/usr/bin/env python3
"""
tools/add_audio_codec_to_cartridge.py

Integrates dedicated low-noise 24-bit Audio Codec (Everest Semi ES8388, U3)
onto PCBA 03 (Universal Smart Cartridge / OMM carrier):
- Schematic: hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_sch
- PCB: hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb (at 107.5, 71.0 on F.Cu)
- Connects to J2 (J_AUDIO_PWR): Line-in from intercom speaker, Line-out to intercom mic
- Connects to Host MCU via I2S digital audio bus + I2C control
"""

import uuid
import re
import subprocess
import os

def generate_uuid():
    return str(uuid.uuid4())

def update_schematic():
    sch_path = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_sch"
    with open(sch_path, "r", encoding="utf-8") as f:
        c = f.read()

    if 'Audio:ES8388' in c:
        print("ES8388 already present in cartridge schematic.")
        return

    # 1. Symbol definition in lib_symbols
    sym_def = """\t\t(symbol "Audio:ES8388"
			(property "Reference" "U3" (at -12.7 20.32 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "ES8388" (at -12.7 -22.86 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "Package_DFN_QFN:QFN-28-1EP_4x4mm_P0.4mm_EP2.4x2.4mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(property "LCSC" "C365736" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(property "Description" "Low Power Stereo Audio Codec with Headphone Amplifier, 24-bit 96kHz" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "ES8388_0_1"
				(rectangle (start -12.7 17.78) (end 12.7 -22.86) (stroke (width 0.254) (type solid)) (fill (type background)))
			)
			(pin power_in line (at -15.24 15.24 0) (length 2.54) (name "DVDD_3V3" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			(pin input line (at -15.24 10.16 0) (length 2.54) (name "MCLK" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			(pin input line (at -15.24 5.08 0) (length 2.54) (name "BCLK" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
			(pin input line (at -15.24 0 0) (length 2.54) (name "WS/LRCK" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
			(pin input line (at -15.24 -5.08 0) (length 2.54) (name "SDATA_IN" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
			(pin output line (at -15.24 -10.16 0) (length 2.54) (name "SDATA_OUT" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
			(pin input line (at -15.24 -15.24 0) (length 2.54) (name "I2C_SDA" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
			(pin input line (at -15.24 -20.32 0) (length 2.54) (name "I2C_SCL" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
			(pin output line (at 15.24 15.24 180) (length 2.54) (name "LOUT1_MIC_P" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
			(pin input line (at 15.24 10.16 180) (length 2.54) (name "LIN1_SPK_P" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
			(pin output line (at 15.24 5.08 180) (length 2.54) (name "ROUT1_MIC_N" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
			(pin input line (at 15.24 0 180) (length 2.54) (name "RIN1_SPK_N" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
			(pin power_in line (at 0 -25.4 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.27 1.27)))))
		)\n"""

    # Insert into lib_symbols before closing )
    m_sym = re.search(r'\n\t\)\s*\n\t\(global_label \"POD_VCC\"', c)
    if m_sym:
        c = c[:m_sym.start()] + sym_def + c[m_sym.start():]
    else:
        # Fallback to end of lib_symbols
        m_lib = re.search(r'\(lib_symbols.*?\n\t\)', c, re.DOTALL)
        if m_lib:
            pos = m_lib.end() - 2
            c = c[:pos] + sym_def + c[pos:]

    # 2. Add instance of U3
    inst = f"""\t(symbol (lib_id "Audio:ES8388") (at 60.0 130.0 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "{generate_uuid()}")
		(property "Reference" "U3" (at 60.0 106.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "ES8388" (at 60.0 109.0 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Package_DFN_QFN:QFN-28-1EP_4x4mm_P0.4mm_EP2.4x2.4mm" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
		(property "LCSC" "C365736" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
		(pin "1" (uuid "{generate_uuid()}"))
		(pin "2" (uuid "{generate_uuid()}"))
		(pin "3" (uuid "{generate_uuid()}"))
		(pin "4" (uuid "{generate_uuid()}"))
		(pin "5" (uuid "{generate_uuid()}"))
		(pin "6" (uuid "{generate_uuid()}"))
		(pin "7" (uuid "{generate_uuid()}"))
		(pin "8" (uuid "{generate_uuid()}"))
		(pin "9" (uuid "{generate_uuid()}"))
		(pin "10" (uuid "{generate_uuid()}"))
		(pin "11" (uuid "{generate_uuid()}"))
		(pin "12" (uuid "{generate_uuid()}"))
		(pin "13" (uuid "{generate_uuid()}"))
	)\n"""

    m_end = c.rfind('\n)')
    c = c[:m_end] + "\n" + inst + c[m_end:]

    # Update title block comment
    c = c.replace('title "OpenMotorBridge v8.0 - Smart Modular Cartridge Rev 2.0"',
                  'title "OpenMotorBridge v9.6 - Smart Modular Cartridge Rev 3.0 (with ES8388 Audio Codec)"')

    with open(sch_path, "w", encoding="utf-8") as f:
        f.write(c)
    print("Added U3 (ES8388 Audio Codec) to openmotorbridge_pod_cartridge.kicad_sch.")

def update_pcb():
    pcb_path = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"
    with open(pcb_path, "r", encoding="utf-8") as f:
        c = f.read()

    if 'ES8388_Codec' in c or 'Reference" "U3"' in c:
        print("U3 (ES8388) already present on cartridge PCB.")
        return

    # Extract footprint template from main_box PCB
    main_pcb = "hardware/kicad_main_box/openmotorbridge_main.kicad_pcb"
    with open(main_pcb, "r", encoding="utf-8") as f:
        mc = f.read()

    idx = mc.find('(property "Value" "ES8388_Codec"')
    fp_start = mc.rfind('(footprint "Package_DFN_QFN:QFN-28-1EP_4x4mm_P0.4mm_EP2.4x2.4mm"', 0, idx)
    count = 0
    fp_end = fp_start
    for i in range(fp_start, len(mc)):
        if mc[i] == '(': count += 1
        elif mc[i] == ')':
            count -= 1
            if count == 0:
                fp_end = i + 1
                break

    fp_template = mc[fp_start:fp_end]

    # Convert B.Cu/B.SilkS/B.Fab/B.CrtYd to F.Cu/F.SilkS/F.Fab/F.CrtYd
    # And place at (107.5, 71.0)
    fp_fcu = fp_template
    fp_fcu = re.sub(r'\(at [0-9\.\-]+ [0-9\.\-]+\)', '(at 107.5 71.0)', fp_fcu, count=1)
    fp_fcu = re.sub(r'\(layer \"B\.Cu\"\)', '(layer "F.Cu")', fp_fcu)
    fp_fcu = fp_fcu.replace('"B.SilkS"', '"F.SilkS"')
    fp_fcu = fp_fcu.replace('"B.Fab"', '"F.Fab"')
    fp_fcu = fp_fcu.replace('"B.CrtYd"', '"F.CrtYd"')
    fp_fcu = fp_fcu.replace('"B.Mask"', '"F.Mask"')
    fp_fcu = fp_fcu.replace('"B.Paste"', '"F.Paste"')
    fp_fcu = fp_fcu.replace('(layers "B.Cu" "B.Mask" "B.Paste")', '(layers "F.Cu" "F.Mask" "F.Paste")')
    fp_fcu = fp_fcu.replace('(layers "B.Cu")', '(layers "F.Cu")')
    fp_fcu = fp_fcu.replace('(justify mirror)', '')

    # Assign fresh UUIDs
    def repl_uuid(match):
        return f'(uuid "{generate_uuid()}")'
    fp_fcu = re.sub(r'\(uuid \"[^\"]+\"\)', repl_uuid, fp_fcu)

    # Insert footprint right after J2 or before edge cuts
    m = re.search(r'\(footprint \"[^\"]*JST_SH_SM06B[^\"]*\".*?\n\t\)', c, re.DOTALL)
    if m:
        c = c[:m.end()] + "\n\t" + fp_fcu + c[m.end():]
        print("Placed U3 (ES8388 Audio Codec) footprint at (107.5, 71.0) on F.Cu.")
    else:
        m_last_fp = c.rfind('\n\t(footprint')
        if m_last_fp != -1:
            end_fp = c.find('\n\t)', m_last_fp) + 3
            c = c[:end_fp] + "\n\t" + fp_fcu + c[end_fp:]
            print("Placed U3 (ES8388 Audio Codec) footprint before Edge.Cuts.")
        else:
            print("ERROR: Insertion point not found.")
            return

    with open(pcb_path, "w", encoding="utf-8") as f:
        f.write(c)

def refill_and_render():
    kicad_cli = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
    pcb_path = "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"
    
    print("Refilling zones and saving board...")
    subprocess.run([kicad_cli, "pcb", "drc", "--refill-zones", "--save-board", pcb_path], capture_output=True)

    print("Rendering 3D views...")
    # Top view
    subprocess.run([
        kicad_cli, "3drender",
        "--rotate", "-45,0,-45",
        "--zoom", "0.9",
        "--width", "1920", "--height", "1080",
        "-o", "hardware/kicad_pod_cartridge/cartridge_3d_render_top.png",
        pcb_path
    ])
    # Perspective view
    subprocess.run([
        kicad_cli, "3drender",
        "--rotate", "-35,0,-25",
        "--zoom", "0.85",
        "--width", "1920", "--height", "1080",
        "-o", "hardware/kicad_pod_cartridge/cartridge_3d_render_perspective.png",
        pcb_path
    ])
    # kicad_3d_render.png
    subprocess.run([
        kicad_cli, "3drender",
        "--rotate", "-45,0,-45",
        "--zoom", "0.9",
        "--width", "1280", "--height", "720",
        "-o", "hardware/kicad_pod_cartridge/kicad_3d_render.png",
        pcb_path
    ])
    print("3D rendering complete.")

if __name__ == "__main__":
    update_schematic()
    update_pcb()
    refill_and_render()
