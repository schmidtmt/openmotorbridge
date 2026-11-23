#!/usr/bin/env python3
"""
tools/add_qualcomm_qcc3084_to_main_box.py

Adds Qualcomm QCC3084 Bluetooth 5.4 Audio SoC module (U9) to Central Box (PCBA 01):
- Schematic: hardware/kicad_main_box/mcu_codec_can.kicad_sch
- PCB: hardware/kicad_main_box/openmotorbridge_main.kicad_pcb (at 175, 106 on F.Cu)
- Features: Dual-A2DP (aptX HD, Low Latency), LE Audio Auracast, HFP 1.8 Wideband Speech
- Antenna: Integrated ceramic chip antenna on module substrate (no coax cable needed)
"""

import uuid
import re

def generate_uuid():
    return str(uuid.uuid4())

def update_schematic():
    sch_path = "hardware/kicad_main_box/mcu_codec_can.kicad_sch"
    with open(sch_path, "r", encoding="utf-8") as f:
        c = f.read()

    if 'Qualcomm_QCC3084' in c:
        print("Qualcomm QCC3084 already present in schematic.")
        return

    # Add symbol definition for Qualcomm QCC3084 Module in lib_symbols
    sym_def = """\t\t(symbol "RF_Module:Qualcomm_QCC3084_Module"
			(property "Reference" "U9" (at -12.7 15.24 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "QCC3084_BT54_AUDIO" (at -12.7 -17.78 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "RF_Module:Qualcomm_QCC3084_Module" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(property "LCSC" "C983084" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(property "Description" "Qualcomm QCC3084 Bluetooth 5.4 Audio SoC (Dual-A2DP aptX-HD, LE Audio Auracast, HFP 1.8)" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "QCC3084_0_1"
				(rectangle (start -15.24 15.24) (end 15.24 -17.78) (stroke (width 0.254) (type solid)) (fill (type background)))
			)
			(pin power_in line (at -17.78 12.7 0) (length 2.54) (name "3V3" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			(pin power_in line (at 0 -20.32 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			(pin input line (at -17.78 7.62 0) (length 2.54) (name "I2S_MCLK" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
			(pin input line (at -17.78 2.54 0) (length 2.54) (name "I2S_BCLK" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
			(pin input line (at -17.78 -2.54 0) (length 2.54) (name "I2S_WS" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
			(pin input line (at -17.78 -7.62 0) (length 2.54) (name "I2S_DOUT" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
			(pin output line (at -17.78 -12.7 0) (length 2.54) (name "I2S_DIN" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
			(pin output line (at 17.78 7.62 180) (length 2.54) (name "UART_TX" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
			(pin input line (at 17.78 2.54 180) (length 2.54) (name "UART_RX" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
			(pin input line (at 17.78 -2.54 180) (length 2.54) (name "BT_EN" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
			(pin output line (at 17.78 -7.62 180) (length 2.54) (name "BT_STATUS" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
		)\n"""

    # Insert into lib_symbols before closing )
    m_sym = re.search(r'\n\t\)\s*\n\t\(symbol \(lib_id \"RF_Module:ESP32-S3-WROOM-1\"', c)
    if m_sym:
        c = c[:m_sym.start()] + sym_def + c[m_sym.start():]

    # Add instance of U9
    inst = f"""\t(symbol (lib_id "RF_Module:Qualcomm_QCC3084_Module") (at 200.0 140.0 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "{generate_uuid()}")
		(property "Reference" "U9" (at 200.0 122.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "QCC3084_BT54_AUDIO" (at 200.0 125.0 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "RF_Module:Qualcomm_QCC3084_Module" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
		(property "LCSC" "C983084" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
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
	)\n"""
    
    # Insert instance before final wire or closing )
    m_last = c.rfind('\n\t(wire')
    if m_last != -1:
        c = c[:m_last] + "\n" + inst + c[m_last:]
    else:
        m_end = c.rfind('\n)')
        c = c[:m_end] + "\n" + inst + c[m_end:]

    with open(sch_path, "w", encoding="utf-8") as f:
        f.write(c)
    print("Added U9 (Qualcomm QCC3084) to mcu_codec_can.kicad_sch.")

def update_pcb():
    pcb_path = "hardware/kicad_main_box/openmotorbridge_main.kicad_pcb"
    with open(pcb_path, "r", encoding="utf-8") as f:
        c = f.read()

    if 'Qualcomm_QCC3084_Module' in c:
        print("Qualcomm QCC3084 already present on PCB.")
        return

    # Build footprint for Qualcomm QCC3084 Module at (175, 106) on F.Cu
    # Size 13 x 18 mm with castellated SMD pads and Raytac MDBT50Q 3D model
    fp = f"""	(footprint "RF_Module:Qualcomm_QCC3084_Module"
		(layer "F.Cu")
		(uuid "{generate_uuid()}")
		(at 175 106)
		(descr "Qualcomm QCC3084 Bluetooth 5.4 Audio SoC Module (Dual-A2DP aptX-HD, LE Audio Auracast, HFP 1.8), 13x18mm with integrated ceramic antenna")
		(tags "Qualcomm QCC3084 Bluetooth 5.4 aptX HD Audio Module")
		(property "Reference" "U9"
			(at 0 -10.2 0)
			(layer "F.SilkS")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
			)
		)
		(property "Value" "QCC3084_BT54_AUDIO"
			(at 0 10.2 0)
			(layer "F.Fab")
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.12)
				)
			)
		)
		(property "Datasheet" "https://www.qualcomm.com/products/application/audio/qcc3084" (at 0 0 0) (layer "F.Fab") (hide yes) (uuid "{generate_uuid()}") (effects (font (size 1.27 1.27))))
		(property "Description" "Qualcomm QCC3084 Dual-A2DP aptX HD / LE Audio Auracast BT 5.4 Module" (at 0 0 0) (layer "F.Fab") (hide yes) (uuid "{generate_uuid()}") (effects (font (size 1.27 1.27))))
		(property "LCSC" "C983084" (at 0 0 0) (layer "F.SilkS") (uuid "{generate_uuid()}") (effects (font (size 1.27 1.27) (thickness 0.15))))
		(attr smd)
		(duplicate_pad_numbers_are_jumpers no)
		(fp_rect (start -6.5 -9.0) (end 6.5 9.0) (stroke (width 0.15) (type solid)) (fill no) (layer "F.SilkS") (uuid "{generate_uuid()}"))
		(fp_rect (start -6.8 -9.3) (end 6.8 9.3) (stroke (width 0.05) (type solid)) (fill no) (layer "F.CrtYd") (uuid "{generate_uuid()}"))
		(fp_rect (start 3.5 -8.0) (end 6.0 -4.5) (stroke (width 0.12) (type solid)) (fill yes) (layer "F.SilkS") (uuid "{generate_uuid()}"))
		(fp_text user "CERAMIC_ANT" (at 4.75 -2.5 90) (layer "F.SilkS") (uuid "{generate_uuid()}") (effects (font (size 0.6 0.6) (thickness 0.1))))
		(fp_text user "${{REFERENCE}}" (at 0 0 0) (layer "F.Fab") (uuid "{generate_uuid()}") (effects (font (size 0.8 0.8) (thickness 0.12))))
		(pad "1" smd rect (at -6.2 -6.0) (size 1.4 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (net "VCC_3V3") (uuid "{generate_uuid()}"))
		(pad "2" smd rect (at -6.2 -4.0) (size 1.4 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (net "GND_PWR") (uuid "{generate_uuid()}"))
		(pad "3" smd rect (at -6.2 -2.0) (size 1.4 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (net "I2S_MCLK") (uuid "{generate_uuid()}"))
		(pad "4" smd rect (at -6.2 0.0) (size 1.4 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (net "I2S_BCLK") (uuid "{generate_uuid()}"))
		(pad "5" smd rect (at -6.2 2.0) (size 1.4 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (net "I2S_WS") (uuid "{generate_uuid()}"))
		(pad "6" smd rect (at -6.2 4.0) (size 1.4 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (net "I2S_DOUT") (uuid "{generate_uuid()}"))
		(pad "7" smd rect (at -6.2 6.0) (size 1.4 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (net "I2S_DIN") (uuid "{generate_uuid()}"))
		(pad "8" smd rect (at 6.2 6.0) (size 1.4 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (net "GND_PWR") (uuid "{generate_uuid()}"))
		(pad "9" smd rect (at 6.2 4.0) (size 1.4 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (net "BT_UART_TX") (uuid "{generate_uuid()}"))
		(pad "10" smd rect (at 6.2 2.0) (size 1.4 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (net "BT_UART_RX") (uuid "{generate_uuid()}"))
		(pad "11" smd rect (at 6.2 0.0) (size 1.4 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (net "BT_EN") (uuid "{generate_uuid()}"))
		(pad "12" smd rect (at 6.2 -2.0) (size 1.4 0.8) (layers "F.Cu" "F.Mask" "F.Paste") (net "GND_PWR") (uuid "{generate_uuid()}"))
		(embedded_fonts no)
		(model "${{KICAD10_3DMODEL_DIR}}/RF_Module.3dshapes/Raytac_MDBT50Q.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1.25 1.0 1.2))
			(rotate (xyz 0 0 0))
		)
	)\n"""

    # Insert footprint right after J1 or another footprint
    m = re.search(r'\(footprint \"[^\"]*IDC-Header_2x06[^\"]*\".*?\n\t\)', c, re.DOTALL)
    if m:
        c = c[:m.end()] + "\n" + fp + c[m.end():]
        print("Placed U9 (Qualcomm QCC3084) footprint on PCB at (175, 106) on F.Cu.")
    else:
        print("ERROR: Could not locate insertion point on PCB!")
        return

    with open(pcb_path, "w", encoding="utf-8") as f:
        f.write(c)

if __name__ == "__main__":
    update_schematic()
    update_pcb()
