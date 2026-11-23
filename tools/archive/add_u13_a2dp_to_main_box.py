#!/usr/bin/env python3
"""
Adds U13 (ESP32-PICO-V3-02 A2DP Transmitter) and ANT4 (Johanson 2450AT Ceramic Antenna)
to PCBA 01 (Central Box) schematic and PCB in the designated space above the SD slot.
"""

import sys
import uuid
import pcbnew

SCH_PATH = "hardware/kicad_main_box/openmotorbridge_main.kicad_sch"
PCB_PATH = "hardware/kicad_main_box/openmotorbridge_main.kicad_pcb"

def generate_uuid():
    return str(uuid.uuid4())

def update_schematic():
    with open(SCH_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add lib symbols before the closing parenthesis of (lib_symbols ...)
    # Find the end of lib_symbols
    ant3_sym_idx = content.find('(symbol "OMB_Main:ANT3_Johanson_2450AT18x100_BLE"')
    if ant3_sym_idx == -1:
        print("Error: ANT3 symbol not found in schematic!")
        sys.exit(1)

    # We will insert ANT4 and U13 symbol definitions
    ant4_sym = '''		(symbol "OMB_Main:ANT4_Johanson_2450AT18x100_A2DP"
			(in_bom yes) (on_board yes)
			(property "Reference" "A" (at 0 0 0) (effects (font (size 1.27 1.27))))
			(property "Value" "Johanson_2450AT18x100" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "RF_Antenna:Johanson_2450AT18x100" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(property "Datasheet" "https://www.johansontechnology.com/datasheets/2450AT18A100/2450AT18A100.pdf" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(property "Description" "Johanson 2.45GHz SMD Ceramic Chip Antenna 3.2x1.6mm for Mesh A2DP Transmitter" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(pin passive line (at -5.08 0.00 0) (length 2.54) (name "1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			(pin passive line (at -5.08 -2.54 0) (length 2.54) (name "2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
		)
		(symbol "OMB_Main:U13_ESP32-PICO-V3-02_A2DP"
			(in_bom yes) (on_board yes)
			(property "Reference" "U" (at 0 0 0) (effects (font (size 1.27 1.27))))
			(property "Value" "ESP32-PICO-V3-02" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Package_DFN_QFN:QFN-48-1EP_7x7mm_P0.5mm_EP5.3x5.3mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(property "Datasheet" "https://www.espressif.com/sites/default/files/documentation/esp32-pico-v3-02_datasheet_en.pdf" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(property "Description" "Espressif SiP Dual-Core Xtensa @ 240MHz, 4MB Flash, 2MB PSRAM, Bluetooth Classic A2DP Source for Pod Mesh-Sharing" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
'''
    # Generate 49 pins (1..48 + 49 for EPAD)
    for p in range(1, 50):
        y_offset = (p - 1) * 2.54
        ant4_sym += f'\t\t\t(pin passive line (at -10.16 -{y_offset:.2f} 0) (length 2.54) (name "{p}" (effects (font (size 1.27 1.27)))) (number "{p}" (effects (font (size 1.27 1.27)))))\n'
    ant4_sym += '\t\t)\n'

    # Insert after ANT3 symbol
    end_ant3_idx = content.find('\t)\n\n\t(symbol (lib_id "OMB_Main:ANT1', ant3_sym_idx)
    if end_ant3_idx == -1:
        print("Error: Could not locate insertion point for symbols in lib_symbols!")
        sys.exit(1)

    content = content[:end_ant3_idx] + ant4_sym + content[end_ant3_idx:]

    # 2. Add instances of U13 and ANT4 before the final closing parenthesis of the schematic
    instances = f'''
	(symbol (lib_id "OMB_Main:ANT4_Johanson_2450AT18x100_A2DP") (at 50.00 430.00 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "{generate_uuid()}")
		(property "Reference" "ANT4" (at 50.00 425.00 0) (effects (font (size 1.27 1.27))))
		(property "Value" "Johanson_2450AT18x100" (at 50.00 427.50 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "RF_Antenna:Johanson_2450AT18x100" (at 50.00 430.00 0) (effects (font (size 1.27 1.27)) hide))
		(property "Datasheet" "" (at 50.00 430.00 0) (effects (font (size 1.27 1.27)) hide))
		(property "Description" "" (at 50.00 430.00 0) (effects (font (size 1.27 1.27)) hide))
		(pin "1" (uuid "{generate_uuid()}"))
		(pin "2" (uuid "{generate_uuid()}"))
	)
	(global_label "A2DP_RF_2G4" (shape bidirectional) (at 44.92 430.00 180) (effects (font (size 1.27 1.27))))
	(global_label "GND_PWR" (shape bidirectional) (at 44.92 432.54 180) (effects (font (size 1.27 1.27))))

	(symbol (lib_id "OMB_Main:U13_ESP32-PICO-V3-02_A2DP") (at 120.00 430.00 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "{generate_uuid()}")
		(property "Reference" "U13" (at 120.00 425.00 0) (effects (font (size 1.27 1.27))))
		(property "Value" "ESP32-PICO-V3-02" (at 120.00 427.50 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Package_DFN_QFN:QFN-48-1EP_7x7mm_P0.5mm_EP5.3x5.3mm" (at 120.00 430.00 0) (effects (font (size 1.27 1.27)) hide))
		(property "Datasheet" "" (at 120.00 430.00 0) (effects (font (size 1.27 1.27)) hide))
		(property "Description" "" (at 120.00 430.00 0) (effects (font (size 1.27 1.27)) hide))
'''
    for p in range(1, 50):
        instances += f'\t\t(pin "{p}" (uuid "{generate_uuid()}"))\n'
    instances += '\t)\n'

    # Add net connections to U13 pins
    # Pin 1: VCC_3V3 (at 120.00 - 10.16, 430.00 - 0.00 = 109.84, 430.00)
    pin_connections = {
        1: "VCC_3V3",
        2: "A2DP_RF_2G4",
        3: "VCC_3V3",
        4: "VCC_3V3",
        9: "A2DP_EN",
        14: "I2S_DOUT",
        15: "I2S_BCLK",
        16: "I2S_WS",
        19: "VCC_3V3",
        23: "A2DP_BOOT",
        37: "VCC_3V3",
        40: "A2DP_UART_RX",
        41: "A2DP_UART_TX",
        43: "VCC_3V3",
        46: "VCC_3V3",
        49: "GND_PWR",
    }
    for pin_num, net_name in pin_connections.items():
        y_pos = 430.00 + (pin_num - 1) * 2.54
        instances += f'\t(global_label "{net_name}" (shape bidirectional) (at 109.84 {y_pos:.2f} 180) (effects (font (size 1.27 1.27))))\n'

    # Insert before the last closing parenthesis
    last_paren = content.rfind(')')
    content = content[:last_paren] + instances + '\n)\n'

    with open(SCH_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Schematic updated with U13 and ANT4 successfully.")

def update_pcb():
    board = pcbnew.LoadBoard(PCB_PATH)

    # 1. Ensure nets exist in the board
    net_rf = board.FindNet("A2DP_RF_2G4")
    if not net_rf:
        net_rf = pcbnew.NETINFO_ITEM(board, "A2DP_RF_2G4")
        board.Add(net_rf)

    net_en = board.FindNet("A2DP_EN")
    if not net_en:
        net_en = pcbnew.NETINFO_ITEM(board, "A2DP_EN")
        board.Add(net_en)

    net_boot = board.FindNet("A2DP_BOOT")
    if not net_boot:
        net_boot = pcbnew.NETINFO_ITEM(board, "A2DP_BOOT")
        board.Add(net_boot)

    net_tx = board.FindNet("A2DP_UART_TX")
    if not net_tx:
        net_tx = pcbnew.NETINFO_ITEM(board, "A2DP_UART_TX")
        board.Add(net_tx)

    net_rx = board.FindNet("A2DP_UART_RX")
    if not net_rx:
        net_rx = pcbnew.NETINFO_ITEM(board, "A2DP_UART_RX")
        board.Add(net_rx)

    net_vcc = board.FindNet("VCC_3V3")
    net_gnd = board.FindNet("GND_PWR")
    net_bclk = board.FindNet("I2S_BCLK")
    net_ws = board.FindNet("I2S_WS")
    net_dout = board.FindNet("I2S_DOUT")

    # 2. Check if ANT4 already exists
    fp_ant4 = None
    for fp in board.GetFootprints():
        if fp.GetReference() == 'ANT4':
            fp_ant4 = fp
            break

    if not fp_ant4:
        fp_ant4 = pcbnew.FootprintLoad('/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/RF_Antenna.pretty', 'Johanson_2450AT18x100')
        if not fp_ant4:
            print("Error: Could not load Johanson_2450AT18x100 footprint!")
            sys.exit(1)
        fp_ant4.SetReference('ANT4')
        fp_ant4.SetValue('Johanson_2450AT18x100')
        board.Add(fp_ant4)

    if fp_ant4:
        # Position at South edge: X = 189.5 mm, Y = 124.5 mm
        pos_ant4 = pcbnew.VECTOR2I(int(189.5 * 1e6), int(124.5 * 1e6))
        fp_ant4.SetPosition(pos_ant4)
        fp_ant4.SetLayer(pcbnew.F_Cu)
        fp_ant4.SetOrientation(pcbnew.EDA_ANGLE(0, pcbnew.DEGREES_T))
        fpid_ant4 = pcbnew.LIB_ID('RF_Antenna', 'Johanson_2450AT18x100')
        fp_ant4.SetFPID(fpid_ant4)
        # Assign pad nets
        for pad in fp_ant4.Pads():
            if pad.GetNumber() == "1":
                pad.SetNet(net_rf)
            elif pad.GetNumber() == "2":
                pad.SetNet(net_gnd)
        print(f"✅ Placed ANT4 at X=189.5 mm, Y=124.5 mm (Top Layer)")

    # 3. Check if U13 already exists
    fp_u13 = None
    for fp in board.GetFootprints():
        if fp.GetReference() == 'U13':
            fp_u13 = fp
            break

    if not fp_u13:
        fp_u13 = pcbnew.FootprintLoad('/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/Package_DFN_QFN.pretty', 'QFN-48-1EP_7x7mm_P0.5mm_EP5.3x5.3mm')
        if not fp_u13:
            print("Error: Could not load QFN-48 footprint!")
            sys.exit(1)
        fp_u13.SetReference('U13')
        fp_u13.SetValue('ESP32-PICO-V3-02')
        board.Add(fp_u13)

    if fp_u13:
        # Position above SD slot: X = 189.5 mm, Y = 113.5 mm
        pos_u13 = pcbnew.VECTOR2I(int(189.5 * 1e6), int(113.5 * 1e6))
        fp_u13.SetPosition(pos_u13)
        fp_u13.SetLayer(pcbnew.F_Cu)
        fpid_u13 = pcbnew.LIB_ID('Package_DFN_QFN', 'QFN-48-1EP_7x7mm_P0.5mm_EP5.3x5.3mm')
        fp_u13.SetFPID(fpid_u13)

        # Pad net mapping
        pad_map = {
            "1": net_vcc,
            "2": net_rf,
            "3": net_vcc,
            "4": net_vcc,
            "9": net_en,
            "14": net_dout,
            "15": net_bclk,
            "16": net_ws,
            "19": net_vcc,
            "23": net_boot,
            "37": net_vcc,
            "40": net_rx,
            "41": net_tx,
            "43": net_vcc,
            "46": net_vcc,
            "49": net_gnd,
        }
        for pad in fp_u13.Pads():
            p_num = pad.GetNumber()
            if p_num in pad_map and pad_map[p_num]:
                pad.SetNet(pad_map[p_num])

        print(f"✅ Placed U13 (ESP32-PICO-V3-02) at X=189.5 mm, Y=113.5 mm (Top Layer)")

    board.BuildConnectivity()
    board.Save(PCB_PATH)
    print("✅ PCB updated and saved successfully.")

if __name__ == "__main__":
    update_schematic()
    update_pcb()
