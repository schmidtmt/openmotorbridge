#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
remediate_omm446_kopie.py
=========================
Remediates hardware/kicad_omm446_intercom Kopie:
1. Rebuilds openmotorbridge_omm446_intercom.kicad_sch with proper labels at exact pin coordinates.
2. Synchronizes openmotorbridge_omm446_intercom.kicad_pcb:
   - Sets pad net assignments matching the schematic.
   - Updates U5 to SOT-23 (3-pin: 1=GND, 2=VCC_3V3, 3=SYS_PWR).
   - Sets J_HELMET to B.Cu with -90° orientation (facing inward -X, perfectly matching Y pitch of vias).
   - Re-nets existing copper tracks and vias to unified net names.
   - Fixes silkscreen text mirroring.
3. Eliminates all single-member nets and schematic parity errors.
"""

import os
import sys
import re
import pcbnew

PCB_PATH = "hardware/kicad_omm446_intercom Kopie/openmotorbridge_omm446_intercom.kicad_pcb"
SCH_PATH = "hardware/kicad_omm446_intercom Kopie/openmotorbridge_omm446_intercom.kicad_sch"

def remediate_schematic():
    print("Rebuilding schematic with exact pin labels...")
    with open(SCH_PATH, "r") as f:
        content = f.read()

    # Update U5 symbol definition to 3-pin SOT-23 if it was 5-pin
    old_u5_sym = r'\(symbol "Regulator:ME6211C33M5G".*?\n\t\)'
    new_u5_sym = '''(symbol "Regulator:ME6211C33M5G"
\t\t\t(property "Reference" "U" (at 0 0 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "ME6211C33M5G" (at 0 0 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Package_TO_SOT_SMD:SOT-23" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(property "LCSC" "C82942" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(pin power_in line (at 0 -7.62 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin power_out line (at 10.16 2.54 180) (length 2.54) (name "VOUT" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t(pin power_in line (at -10.16 2.54 0) (length 2.54) (name "VIN" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t)'''
    content = re.sub(old_u5_sym, new_u5_sym, content, flags=re.DOTALL)

    # Define pin net mapping for each symbol
    pin_nets = {
        "U1": { # ESP32-C6-MINI-1U / ESP32-S2
            "1": "GND", "2": "VCC_3V3", "3": "GND",
            "4": "BTN_3", "5": "BTN_4", "6": "WS2812_DATA", "7": "CHG_STAT",
            "8": "BTN_1", "9": "BTN_2", "10": "I2C_SDA", "11": "I2C_SCL",
            "12": "BT_BOOT", "13": "BT_RESET",
            "14": "USB_DN", "15": "USB_DP",
            "16": "SA818_TXD", "17": "SA818_RXD", "18": "SA818_PTT",
            "19": "SA818_SQL", "20": "SA818_PWR_HL",
            "21": "I2S_MCLK", "22": "I2S_BCLK", "23": "I2S_WS",
            "24": "I2S_DOUT", "25": "I2S_DIN",
            "26": "BT_UART_CTS", "27": "BT_UART_RTS",
            "28": "BT_UART_TX", "29": "BT_UART_RX",
            "40": "GND", "41": "GND", "42": "GND", "43": "GND",
            "44": "GND", "45": "GND", "46": "GND", "47": "GND",
            "48": "GND", "49": "GND", "50": "GND", "51": "GND",
            "52": "GND", "53": "GND",
            "54": "GND", "55": "GND", "56": "GND", "57": "GND",
            "58": "GND", "59": "GND", "60": "GND", "61": "GND",
            "62": "GND", "63": "GND", "64": "GND", "65": "GND"
        },
        "U2": { # BQ24075RGTR
            "1": "GND", "2": "VBAT", "3": "VBAT",
            "4": "GND", "5": "GND", "6": "GND",
            "7": "GND", "8": "GND", "9": "CHG_STAT",
            "10": "SYS_PWR", "11": "SYS_PWR",
            "12": "GND", "13": "VBUS_5V", "14": "GND",
            "15": "GND", "16": "GND", "17": "GND"
        },
        "U3": { # SA818-DMR
            "1": "VCC_3V3", "3": "SA818_AF_OUT", "5": "SA818_PTT",
            "6": "SYS_PWR", "7": "SA818_PWR_HL", "8": "SYS_PWR",
            "9": "PGND", "10": "GND", "12": "RF_ANT",
            "14": "SA818_SQL", "15": "SA818_TXD", "16": "SA818_RXD",
            "17": "SA818_MIC_IN", "18": "AGND"
        },
        "U4": { # ES8388
            "1": "I2S_MCLK", "2": "I2S_BCLK", "3": "I2S_WS",
            "4": "I2S_DOUT", "5": "I2S_DIN", "6": "I2C_SDA", "7": "I2C_SCL",
            "8": "GND", "9": "VCC_3V3", "10": "GND",
            "11": "AUDIO_OUT_R", "12": "AUDIO_OUT_L",
            "14": "SA818_MIC_IN", "15": "VCC_3V3", "16": "AGND",
            "17": "AGND", "18": "AGND",
            "19": "VOICE_IN", "20": "AGND",
            "21": "SA818_AF_OUT", "23": "VCC_3V3", "24": "PGND",
            "25": "VCC_3V3", "29": "GND"
        },
        "U5": { # ME6211 3-pin SOT-23
            "1": "GND", "2": "VCC_3V3", "3": "SYS_PWR"
        },
        "U6": { # ESP32-PICO-V3-02
            "1": "VCC_3V3", "2": "BT_ANT", "3": "VCC_3V3", "4": "VCC_3V3",
            "9": "BT_RESET", "19": "VCC_3V3",
            "20": "BT_UART_CTS", "21": "BT_UART_RTS", "23": "BT_BOOT",
            "37": "VCC_3V3", "40": "BT_UART_RX", "41": "BT_UART_TX",
            "43": "VCC_3V3", "46": "VCC_3V3", "49": "GND"
        },
        "D1": { # WS2812B
            "1": "GND", "2": "VCC_3V3", "3": "GND", "4": "WS2812_DATA"
        },
        "D2": { # USBLC6-2SC6
            "1": "USB_DP", "2": "GND", "3": "USB_DN",
            "4": "USB_DN", "5": "VBUS_5V", "6": "USB_DP"
        },
        "J1": { # USB-C
            "A1": "PGND", "A4": "VBUS_5V", "A5": "AUDIO_OUT_L",
            "A6": "USB_DP", "A7": "USB_DN", "A8": "VOICE_IN",
            "A9": "VBUS_5V", "A12": "PGND",
            "B1": "PGND", "B4": "VBUS_5V", "B5": "AUDIO_OUT_R",
            "B6": "USB_DP", "B7": "USB_DN", "B8": "AGND",
            "B9": "VBUS_5V", "B12": "PGND", "SH": "PGND"
        },
        "J_HELMET": { # 6-Pin JST-SH
            "1": "AUDIO_OUT_L", "2": "AUDIO_OUT_R", "3": "AGND",
            "4": "VOICE_IN", "5": "AGND", "6": "BTN_1",
            "MP": "GND"
        },
        "J_RF": { # U.FL
            "1": "RF_ANT", "2": "GND", "3": "GND"
        },
        "BAT1": { # LiPo
            "1": "VBAT", "2": "GND", "MP": "GND"
        },
        "SW1": { "1": "BTN_1", "2": "GND" },
        "SW2": { "1": "BTN_2", "2": "GND" },
        "SW3": { "1": "BTN_3", "2": "GND" },
        "SW4": { "1": "BTN_4", "2": "GND" },
        "ANT1": { "1": "BT_ANT", "2": "GND" }
    }

    # Extract symbol library pins
    lib_section = content[content.find('(lib_symbols'):content.find('\n\t(symbol ')]
    sym_defs = re.split(r'\(symbol\s+\"([^\"]+)\"', lib_section)
    lib_pins = {}
    for i in range(1, len(sym_defs), 2):
        name = sym_defs[i]
        body = sym_defs[i+1]
        p_matches = re.finditer(r'\(pin\s+\w+\s+line\s+\(at\s+([-\d\.]+)\s+([-\d\.]+)\s+(\d+)\)\s+\(length\s+[-\d\.]+\).*?\(number\s+\"([^\"]+)\"', body, re.DOTALL)
        pins = {}
        for pm in p_matches:
            px, py, prot, pnum = pm.groups()
            pins[pnum] = (float(px), float(py), int(prot))
        lib_pins[name] = pins

    # Find placed symbol instances
    inst_matches = re.finditer(r'\(symbol\s+\(lib_id\s+\"([^\"]+)\"\)\s+\(at\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\).*?\(property\s+\"Reference\"\s+\"([^\"]+)\"', content, re.DOTALL)
    labels_to_add = []
    
    for m in inst_matches:
        lib_id, sx, sy, srot, ref = m.groups()
        sx, sy, srot = float(sx), float(sy), float(srot)
        if ref not in pin_nets:
            continue
        pins = lib_pins.get(lib_id, {})
        for pnum, net in pin_nets[ref].items():
            if pnum not in pins:
                continue
            px, py, prot = pins[pnum]
            # KiCad eeschema coordinate: X = sx + px, Y = sy - py (Cartesian to eeschema screen Y)
            lx = round(sx + px, 2)
            ly = round(sy - py, 2)
            labels_to_add.append(f'\t(label "{net}" (at {lx} {ly} 0) (effects (font (size 1.27 1.27))))')

    # Remove any existing labels and append clean set
    clean_content = re.sub(r'\n\t\((?:global_)?label\s+.*?\)\)\)', '', content)
    # Strip trailing paren
    clean_content = clean_content.rstrip()
    if clean_content.endswith(')'):
        clean_content = clean_content[:-1].rstrip()

    new_content = clean_content + "\n\n" + "\n".join(labels_to_add) + "\n)\n"
    with open(SCH_PATH, "w") as f:
        f.write(new_content)
    print(f"✓ Added {len(labels_to_add)} pin labels to schematic.")

def remediate_pcb():
    print("Remediating PCB layout & net assignments...")
    board = pcbnew.LoadBoard(PCB_PATH)

    # 1. Ensure required nets exist
    required_nets = [
        "GND", "PGND", "AGND", "VCC_3V3", "VBUS_5V", "VBAT", "SYS_PWR",
        "AUDIO_OUT_L", "AUDIO_OUT_R", "VOICE_IN",
        "BTN_1", "BTN_2", "BTN_3", "BTN_4",
        "I2S_MCLK", "I2S_BCLK", "I2S_WS", "I2S_DOUT", "I2S_DIN",
        "I2C_SDA", "I2C_SCL",
        "SA818_TXD", "SA818_RXD", "SA818_PTT", "SA818_SQL", "SA818_PWR_HL",
        "SA818_MIC_IN", "SA818_AF_OUT", "RF_ANT",
        "BT_UART_TX", "BT_UART_RX", "BT_UART_RTS", "BT_UART_CTS",
        "BT_RESET", "BT_BOOT", "BT_ANT",
        "USB_DP", "USB_DN", "WS2812_DATA", "CHG_STAT"
    ]
    net_map = {}
    for name in required_nets:
        net = board.FindNet(name)
        if not net:
            net = pcbnew.NETINFO_ITEM(board, name)
            board.Add(net)
        net_map[name] = net

    # 2. Update pad net assignments
    assignments = {
        "U1": {
            "1": "GND", "2": "VCC_3V3", "3": "GND",
            "4": "BTN_3", "5": "BTN_4", "6": "WS2812_DATA", "7": "CHG_STAT",
            "8": "BTN_1", "9": "BTN_2", "10": "I2C_SDA", "11": "I2C_SCL",
            "12": "BT_BOOT", "13": "BT_RESET",
            "14": "USB_DN", "15": "USB_DP",
            "16": "SA818_TXD", "17": "SA818_RXD", "18": "SA818_PTT",
            "19": "SA818_SQL", "20": "SA818_PWR_HL",
            "21": "I2S_MCLK", "22": "I2S_BCLK", "23": "I2S_WS",
            "24": "I2S_DOUT", "25": "I2S_DIN",
            "26": "BT_UART_CTS", "27": "BT_UART_RTS",
            "28": "BT_UART_TX", "29": "BT_UART_RX",
            "40": "GND", "41": "GND", "42": "GND", "43": "GND",
            "44": "GND", "45": "GND", "46": "GND", "47": "GND",
            "48": "GND", "49": "GND", "50": "GND", "51": "GND",
            "52": "GND", "53": "GND",
            "54": "GND", "55": "GND", "56": "GND", "57": "GND",
            "58": "GND", "59": "GND", "60": "GND", "61": "GND",
            "62": "GND", "63": "GND", "64": "GND", "65": "GND"
        },
        "U2": {
            "1": "GND", "2": "VBAT", "3": "VBAT",
            "4": "GND", "5": "GND", "6": "GND",
            "7": "GND", "8": "GND", "9": "CHG_STAT",
            "10": "SYS_PWR", "11": "SYS_PWR",
            "12": "GND", "13": "VBUS_5V", "14": "GND",
            "15": "GND", "16": "GND", "17": "GND"
        },
        "U3": {
            "1": "VCC_3V3", "3": "SA818_AF_OUT", "5": "SA818_PTT",
            "6": "SYS_PWR", "7": "SA818_PWR_HL", "8": "SYS_PWR",
            "9": "PGND", "10": "GND", "12": "RF_ANT",
            "14": "SA818_SQL", "15": "SA818_TXD", "16": "SA818_RXD",
            "17": "SA818_MIC_IN", "18": "AGND"
        },
        "U4": {
            "1": "I2S_MCLK", "2": "I2S_BCLK", "3": "I2S_WS",
            "4": "I2S_DOUT", "5": "I2S_DIN", "6": "I2C_SDA", "7": "I2C_SCL",
            "8": "GND", "9": "VCC_3V3", "10": "GND",
            "11": "AUDIO_OUT_R", "12": "AUDIO_OUT_L",
            "14": "SA818_MIC_IN", "15": "VCC_3V3", "16": "AGND",
            "17": "AGND", "18": "AGND",
            "19": "VOICE_IN", "20": "AGND",
            "21": "SA818_AF_OUT", "23": "VCC_3V3", "24": "PGND",
            "25": "VCC_3V3", "29": "GND"
        },
        "U5": {
            "1": "GND", "2": "VCC_3V3", "3": "SYS_PWR"
        },
        "U6": {
            "1": "VCC_3V3", "2": "BT_ANT", "3": "VCC_3V3", "4": "VCC_3V3",
            "9": "BT_RESET", "19": "VCC_3V3",
            "20": "BT_UART_CTS", "21": "BT_UART_RTS", "23": "BT_BOOT",
            "37": "VCC_3V3", "40": "BT_UART_RX", "41": "BT_UART_TX",
            "43": "VCC_3V3", "46": "VCC_3V3", "49": "GND"
        },
        "D1": {
            "1": "GND", "2": "VCC_3V3", "3": "GND", "4": "WS2812_DATA"
        },
        "D2": {
            "1": "USB_DP", "2": "GND", "3": "USB_DN",
            "4": "USB_DN", "5": "VBUS_5V", "6": "USB_DP"
        },
        "J1": {
            "A1": "PGND", "A4": "VBUS_5V", "A5": "AUDIO_OUT_L",
            "A6": "USB_DP", "A7": "USB_DN", "A8": "VOICE_IN",
            "A9": "VBUS_5V", "A12": "PGND",
            "B1": "PGND", "B4": "VBUS_5V", "B5": "AUDIO_OUT_R",
            "B6": "USB_DP", "B7": "USB_DN", "B8": "AGND",
            "B9": "VBUS_5V", "B12": "PGND", "SH": "PGND"
        },
        "J_HELMET": {
            "1": "AUDIO_OUT_L", "2": "AUDIO_OUT_R", "3": "AGND",
            "4": "VOICE_IN", "5": "AGND", "6": "BTN_1",
            "MP": "GND"
        },
        "J_RF": {
            "1": "RF_ANT", "2": "GND", "3": "GND"
        },
        "BAT1": {
            "1": "VBAT", "2": "GND", "MP": "GND"
        },
        "SW1": { "1": "BTN_1", "2": "GND" },
        "SW2": { "1": "BTN_2", "2": "GND" },
        "SW3": { "1": "BTN_3", "2": "GND" },
        "SW4": { "1": "BTN_4", "2": "GND" },
        "ANT1": { "1": "BT_ANT", "2": "GND" }
    }

    for ref, pads in assignments.items():
        fp = board.FindFootprintByReference(ref)
        if not fp:
            continue
        for pad in fp.Pads():
            pnum = pad.GetPadName()
            if pnum in pads and pads[pnum] in net_map:
                pad.SetNet(net_map[pads[pnum]])

    # Assign U6 center thermal pads (empty name) to GND
    u6 = board.FindFootprintByReference("U6")
    if u6:
        for p in u6.Pads():
            if p.GetPadName() == "" or p.GetPadName() == "49":
                p.SetNet(net_map["GND"])

    # 3. Orient J_HELMET on B.Cu with -90° rotation
    fp_jhelm = board.FindFootprintByReference("J_HELMET")
    if fp_jhelm:
        if fp_jhelm.GetLayer() == pcbnew.F_Cu:
            fp_jhelm.Flip(fp_jhelm.GetPosition(), True)
            print("✓ Flipped J_HELMET to B.Cu (Bottom layer)")
        fp_jhelm.SetOrientationDegrees(-90.0)

    # 4. Re-net tracks and vias to match updated net names
    track_net_remap = {
        "HP_OUT_L": "AUDIO_OUT_L",
        "HP_OUT_R": "AUDIO_OUT_R",
        "MIC_IN+": "VOICE_IN",
        "MIC_IN": "VOICE_IN",
        "AGND_SPK": "AGND",
        "AGND_AUDIO_OUT": "AGND",
        "AGND_HP": "AGND",
        "AGND_MIC": "AGND",
        "BTN_PTT": "BTN_1"
    }
    for t in board.GetTracks():
        old_net = t.GetNetname()
        if old_net in track_net_remap:
            target_name = track_net_remap[old_net]
            if target_name in net_map:
                t.SetNet(net_map[target_name])

    # 5. Clean up silkscreen texts that caused warnings
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        texts = fp.GraphicalItems()
        for t in texts:
            if isinstance(t, pcbnew.PCB_TEXT):
                t.SetMirrored(fp.GetLayer() == pcbnew.B_Cu)

    board.Save(PCB_PATH)
    print("✓ PCB updated and saved successfully.")

def main():
    remediate_schematic()
    remediate_pcb()

if __name__ == "__main__":
    main()
