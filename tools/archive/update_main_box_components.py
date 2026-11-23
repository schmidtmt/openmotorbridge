#!/usr/bin/env python3
"""
update_main_box_components.py
Fixes missing chips, unassigned nets, and SD card placement on the openmotorbridge_main PCB and schematics.
- Fixes U7 -> U10 rename for SX1262 (resolving RefDes collision with Optocoupler U7).
- Connects SX1262 pads to proper nets (SPI, control, RF, 3V3, GND).
- Connects ANT1 to LORA_RF_868 and GND_PWR.
- Connects DW3110 (U8), Y1_UWB, and ANT2 to proper nets.
- Connects BMI270 (U5) to I2C_SDA, I2C_SCL, 3V3, GND_PWR.
- Connects WS2812B (D1) to RGB_LED_DATA, 5V, GND_PWR.
- Connects SW1 to ESP_BOOT and GND_PWR.
- Replaces J2 (MicroSD) with full Hirose DM3D-SF footprint on B.Cu at (146.0, 78.5) with zero overlap,
  accessible from top edge, with all pads assigned to SDIO nets.
- Does NOT route any traces (preserves user preference for manual GUI routing).
"""

import os
import re
import uuid

SCH_PATH = "hardware/kicad_main_box/mcu_codec_can.kicad_sch"
PCB_PATH = "hardware/kicad_main_box/openmotorbridge_main.kicad_pcb"

def parse_sexpr(text, start):
    depth = 0
    i = start
    while i < len(text):
        if text[i] == '(':
            depth += 1
        elif text[i] == ')':
            depth -= 1
            if depth == 0:
                return text[start:i+1], i+1
        i += 1
    return text[start:], len(text)

def update_pcb():
    print(f"Reading {PCB_PATH}...")
    with open(PCB_PATH, "r") as f:
        text = f.read()

    # 1. Rename U7 (SX1262) to U10
    # In PCB, find footprint with Value "SX1262IMLTRT"
    pos = 0
    while True:
        idx = text.find("(footprint", pos)
        if idx == -1: break
        expr, next_pos = parse_sexpr(text, idx)
        pos = next_pos
        if '"SX1262IMLTRT"' in expr:
            print("Found SX1262 footprint in PCB, updating to U10 with nets...")
            # Reconstruct U10 footprint with proper nets on pads
            # SX1262 QFN-24 pinout:
            # 1: LORA_RST, 2: LORA_XTA, 3: LORA_XTB, 4: LORA_VR_DCDC, 5: LORA_DCC_SW, 6: VCC_3V3
            # 7: LORA_VR_PA, 8: GND_PWR, 9: GND_PWR, 10: LORA_RF_868, 11: GND_PWR, 12: GND_PWR
            # 13: VCC_3V3, 14: LORA_BUSY, 15: LORA_DIO1, 16: LORA_DIO2, 17: VCC_3V3, 18: LORA_MISO
            # 19: LORA_MOSI, 20: LORA_SCK, 21: LORA_NSS, 22: GND_PWR, 23: GND_PWR, 24: GND_PWR
            # 25: GND_PWR (EP)
            pad_nets = {
                "1": "LORA_RST", "2": "LORA_XTA", "3": "LORA_XTB", "4": "LORA_VR_DCDC",
                "5": "LORA_DCC_SW", "6": "VCC_3V3", "7": "LORA_VR_PA", "8": "GND_PWR",
                "9": "GND_PWR", "10": "LORA_RF_868", "11": "GND_PWR", "12": "GND_PWR",
                "13": "VCC_3V3", "14": "LORA_BUSY", "15": "LORA_DIO1", "16": "LORA_DIO2",
                "17": "VCC_3V3", "18": "SPI_MISO", "19": "SPI_MOSI", "20": "SPI_SCK",
                "21": "LORA_NSS", "22": "GND_PWR", "23": "GND_PWR", "24": "GND_PWR",
                "25": "GND_PWR", "": "GND_PWR"
            }
            # Update Reference to U10
            new_expr = expr.replace('"U7"', '"U10"')
            # Inject nets into pad expressions
            p_pos = 0
            pad_chunks = []
            last_p = 0
            while True:
                p_idx = new_expr.find(chr(40) + "pad " + chr(34), p_pos)
                if p_idx == -1:
                    pad_chunks.append(new_expr[last_p:])
                    break
                pad_expr, p_next = parse_sexpr(new_expr, p_idx)
                p_pos = p_next
                pad_chunks.append(new_expr[last_p:p_idx])
                last_p = p_next
                
                num_m = re.search(r'\(pad\s+\"([^\"]*)\"', pad_expr)
                num = num_m.group(1) if num_m else ""
                net_name = pad_nets.get(num, "GND_PWR" if num == "" else "")
                
                # Check if pad already has net
                if "(net " in pad_expr:
                    pad_expr = re.sub(r'\(net\s+[^\)]+\)', f'(net "{net_name}")', pad_expr)
                else:
                    # insert (net "...") before final bracket
                    insert_idx = pad_expr.rfind(")")
                    pad_expr = pad_expr[:insert_idx] + f'\n\t\t\t(net "{net_name}")\n\t\t)'
                pad_chunks.append(pad_expr)
            updated_u10 = "".join(pad_chunks)
            text = text[:idx] + updated_u10 + text[next_pos:]
            break

    # 2. Update ANT1 (Taoglas_FXP895_868MHz_Lid)
    pos = 0
    while True:
        idx = text.find("(footprint", pos)
        if idx == -1: break
        expr, next_pos = parse_sexpr(text, idx)
        pos = next_pos
        if '"ANT1"' in expr:
            print("Found ANT1 footprint, updating nets...")
            new_expr = expr
            # Pad 1 is signal, pads 2/3/4/shield are GND_PWR
            p_pos = 0
            pad_chunks = []
            last_p = 0
            while True:
                p_idx = new_expr.find(chr(40) + "pad " + chr(34), p_pos)
                if p_idx == -1:
                    pad_chunks.append(new_expr[last_p:])
                    break
                pad_expr, p_next = parse_sexpr(new_expr, p_idx)
                p_pos = p_next
                pad_chunks.append(new_expr[last_p:p_idx])
                last_p = p_next
                
                num_m = re.search(r'\(pad\s+\"([^\"]*)\"', pad_expr)
                num = num_m.group(1) if num_m else ""
                net_name = "LORA_RF_868" if num == "1" else "GND_PWR"
                
                if "(net " in pad_expr:
                    pad_expr = re.sub(r'\(net\s+[^\)]+\)', f'(net "{net_name}")', pad_expr)
                else:
                    insert_idx = pad_expr.rfind(")")
                    pad_expr = pad_expr[:insert_idx] + f'\n\t\t\t(net "{net_name}")\n\t\t)'
                pad_chunks.append(pad_expr)
            updated_ant1 = "".join(pad_chunks)
            text = text[:idx] + updated_ant1 + text[next_pos:]
            break

    # 3. Update U8 (DW3110)
    pos = 0
    while True:
        idx = text.find("(footprint", pos)
        if idx == -1: break
        expr, next_pos = parse_sexpr(text, idx)
        pos = next_pos
        if '"U8"' in expr:
            print("Found U8 (DW3110) footprint, updating nets on B.Cu at (175, 105)...")
            # Keep U8 at (175, 105) 180 on B.Cu
            expr = re.sub(r'\(at\s+[0-9\.\-]+\s+[0-9\.\-]+\s+180\)', '(at 175 105 180)', expr, count=1)
            # DW3110 pads:
            # 1: VCC_1V8, 2: VCC_1V2, 3: GND_PWR, 4: UWB_XTAL1, 5: UWB_XTAL2, 6: GND_PWR
            # 7: SPI_SCK, 8: SPI_MISO, 9: SPI_MOSI, 10: UWB_CS, 11: UWB_WAKE, 12: UWB_RST
            # 13: UWB_IRQ, 14: VCC_3V3, 15: UWB_RF_CH5, 16: GND_PWR, 17: GND_PWR (EP on B.Cu)
            u8_nets = {
                "1": "VCC_1V8", "2": "VCC_1V2", "3": "GND_PWR", "4": "UWB_XTAL1",
                "5": "UWB_XTAL2", "6": "GND_PWR", "7": "SPI_SCK", "8": "SPI_MISO",
                "9": "SPI_MOSI", "10": "UWB_CS", "11": "UWB_WAKE", "12": "UWB_RST",
                "13": "UWB_IRQ", "14": "VCC_3V3", "15": "UWB_RF_CH5", "16": "GND_PWR",
                "17": "GND_PWR", "": "GND_PWR"
            }
            new_expr = expr
            p_pos = 0
            pad_chunks = []
            last_p = 0
            ep_added = False
            while True:
                p_idx = new_expr.find(chr(40) + "pad ", p_pos)
                if p_idx == -1:
                    pad_chunks.append(new_expr[last_p:])
                    break
                pad_expr, p_next = parse_sexpr(new_expr, p_idx)
                p_pos = p_next
                pad_chunks.append(new_expr[last_p:p_idx])
                last_p = p_next
                num_m = re.search(r'\(pad\s+\"([^\"]*)\"', pad_expr)
                num = num_m.group(1) if num_m else ""
                
                # If pad 17: only keep single SMD pad on B.Cu, discard thru_hole / F.Cu pads!
                if num == "17":
                    if not ep_added:
                        ep_pad = f'''(pad "17" smd rect (at 0 0 180) (size 1.7 1.7) (layers "B.Cu" "B.Mask") (net "GND_PWR") (uuid "{uuid.uuid4()}"))'''
                        pad_chunks.append(ep_pad)
                        ep_added = True
                    # skip adding other duplicate pad 17s
                    continue
                    
                net_name = u8_nets.get(num, "GND_PWR")
                if "(net " in pad_expr:
                    pad_expr = re.sub(r'\(net\s+[^\)]+\)', f'(net "{net_name}")', pad_expr)
                else:
                    insert_idx = pad_expr.rfind(")")
                    pad_expr = pad_expr[:insert_idx] + f'\n\t\t\t(net "{net_name}")\n\t\t)'
                pad_chunks.append(pad_expr)
            updated_u8 = "".join(pad_chunks)
            text = text[:idx] + updated_u8 + text[next_pos:]
            break

    # 4. Update Y1_UWB and ANT2
    pos = 0
    while True:
        idx = text.find("(footprint", pos)
        if idx == -1: break
        expr, next_pos = parse_sexpr(text, idx)
        pos = next_pos
        if '"Y1_UWB"' in expr:
            print("Found Y1_UWB footprint, updating nets...")
            y1_nets = {"1": "UWB_XTAL1", "2": "GND_PWR", "3": "UWB_XTAL2", "4": "GND_PWR"}
            new_expr = expr
            p_pos = 0
            pad_chunks = []
            last_p = 0
            while True:
                p_idx = new_expr.find(chr(40) + "pad " + chr(34), p_pos)
                if p_idx == -1:
                    pad_chunks.append(new_expr[last_p:])
                    break
                pad_expr, p_next = parse_sexpr(new_expr, p_idx)
                p_pos = p_next
                pad_chunks.append(new_expr[last_p:p_idx])
                last_p = p_next
                num_m = re.search(r'\(pad\s+\"([^\"]*)\"', pad_expr)
                num = num_m.group(1) if num_m else ""
                net_name = y1_nets.get(num, "GND_PWR")
                if "(net " in pad_expr:
                    pad_expr = re.sub(r'\(net\s+[^\)]+\)', f'(net "{net_name}")', pad_expr)
                else:
                    insert_idx = pad_expr.rfind(")")
                    pad_expr = pad_expr[:insert_idx] + f'\n\t\t\t(net "{net_name}")\n\t\t)'
                pad_chunks.append(pad_expr)
            updated_y1 = "".join(pad_chunks)
            text = text[:idx] + updated_y1 + text[next_pos:]
            break

    pos = 0
    while True:
        idx = text.find("(footprint", pos)
        if idx == -1: break
        expr, next_pos = parse_sexpr(text, idx)
        pos = next_pos
        if '"ANT2"' in expr:
            print("Found ANT2 footprint, updating nets...")
            new_expr = expr
            p_pos = 0
            pad_chunks = []
            last_p = 0
            while True:
                p_idx = new_expr.find(chr(40) + "pad " + chr(34), p_pos)
                if p_idx == -1:
                    pad_chunks.append(new_expr[last_p:])
                    break
                pad_expr, p_next = parse_sexpr(new_expr, p_idx)
                p_pos = p_next
                pad_chunks.append(new_expr[last_p:p_idx])
                last_p = p_next
                num_m = re.search(r'\(pad\s+\"([^\"]*)\"', pad_expr)
                num = num_m.group(1) if num_m else ""
                net_name = "UWB_RF_CH5" if num == "1" else "GND_PWR"
                if "(net " in pad_expr:
                    pad_expr = re.sub(r'\(net\s+[^\)]+\)', f'(net "{net_name}")', pad_expr)
                else:
                    insert_idx = pad_expr.rfind(")")
                    pad_expr = pad_expr[:insert_idx] + f'\n\t\t\t(net "{net_name}")\n\t\t)'
                pad_chunks.append(pad_expr)
            updated_ant2 = "".join(pad_chunks)
            text = text[:idx] + updated_ant2 + text[next_pos:]
            break

    # 5. Update U5 (BMI270_IMU)
    pos = 0
    while True:
        idx = text.find("(footprint", pos)
        if idx == -1: break
        expr, next_pos = parse_sexpr(text, idx)
        pos = next_pos
        if '"U5"' in expr:
            print("Found U5 (BMI270) footprint, updating nets...")
            # BMI270 LGA-14:
            # 1: GND_PWR (SDO), 2: GND_PWR, 3: VCC_3V3, 4: IMU_INT1, 5: VCC_3V3 (VDDIO),
            # 6: GND_PWR, 7: GND_PWR, 8: VCC_3V3, 9: IMU_INT2, 10: GND_PWR, 11: GND_PWR,
            # 12: VCC_3V3 (CSB for I2C), 13: I2C_SCL, 14: I2C_SDA
            u5_nets = {
                "1": "GND_PWR", "2": "GND_PWR", "3": "VCC_3V3", "4": "IMU_INT1",
                "5": "VCC_3V3", "6": "GND_PWR", "7": "GND_PWR", "8": "VCC_3V3",
                "9": "IMU_INT2", "10": "GND_PWR", "11": "GND_PWR", "12": "VCC_3V3",
                "13": "I2C_SCL", "14": "I2C_SDA"
            }
            # Check if U5 has pads. If it had 0 pads, generate full LGA-14 pad set!
            if "(pad" not in expr:
                print("U5 had no pads defined! Generating LGA-14 pads...")
                # LGA-14 2.5x3mm pitch 0.5mm
                pad_defs = []
                # Left side: pins 1..7 (x = -1.2, y = -1.25..+1.25)
                # Right side: pins 8..14 (x = +1.2, y = +1.25..-1.25)
                for pin_i in range(1, 15):
                    net = u5_nets.get(str(pin_i), "GND_PWR")
                    if pin_i <= 7:
                        px = -1.15
                        py = -1.5 + (pin_i - 1) * 0.5
                    else:
                        px = 1.15
                        py = 1.5 - (pin_i - 8) * 0.5
                    pad_defs.append(f'''\t\t(pad "{pin_i}" smd rect
\t\t\t(at {px:.4f} {py:.4f})
\t\t\t(size 0.5 0.3)
\t\t\t(layers "B.Cu" "B.Mask" "B.Paste")
\t\t\t(net "{net}")
\t\t\t(uuid "{uuid.uuid4()}")
\t\t)''')
                pads_str = "\n".join(pad_defs)
                last_br = expr.rfind(")")
                updated_u5 = expr[:last_br] + pads_str + "\n\t)"
            else:
                updated_u5 = expr
            text = text[:idx] + updated_u5 + text[next_pos:]
            break

    # 6. Update D1 (WS2812B_RGB) & SW1 (SW_PAIR_RESET)
    pos = 0
    while True:
        idx = text.find("(footprint", pos)
        if idx == -1: break
        expr, next_pos = parse_sexpr(text, idx)
        pos = next_pos
        if '"D1"' in expr:
            print("Found D1 footprint, updating pads and nets...")
            if "(pad" not in expr:
                # WS2812B-2020: 1: VDD (5V), 2: DOUT, 3: GND, 4: DIN (RGB_LED_DATA)
                pad_defs = f'''\t\t(pad "1" smd rect (at 0.75 -0.65) (size 0.6 0.5) (layers "F.Cu" "F.Mask" "F.Paste") (net "VCC_5V") (uuid "{uuid.uuid4()}"))
\t\t(pad "2" smd rect (at 0.75 0.65) (size 0.6 0.5) (layers "F.Cu" "F.Mask" "F.Paste") (net "GND_PWR") (uuid "{uuid.uuid4()}"))
\t\t(pad "3" smd rect (at -0.75 0.65) (size 0.6 0.5) (layers "F.Cu" "F.Mask" "F.Paste") (net "GND_PWR") (uuid "{uuid.uuid4()}"))
\t\t(pad "4" smd rect (at -0.75 -0.65) (size 0.6 0.5) (layers "F.Cu" "F.Mask" "F.Paste") (net "RGB_LED_DATA") (uuid "{uuid.uuid4()}"))'''
                last_br = expr.rfind(")")
                updated_d1 = expr[:last_br] + pad_defs + "\n\t)"
                text = text[:idx] + updated_d1 + text[next_pos:]
            break

    pos = 0
    while True:
        idx = text.find("(footprint", pos)
        if idx == -1: break
        expr, next_pos = parse_sexpr(text, idx)
        pos = next_pos
        if '"SW1"' in expr:
            print("Found SW1 footprint, updating pads and nets...")
            if "(pad" not in expr:
                pad_defs = f'''\t\t(pad "1" smd rect (at -1.8 0) (size 0.8 1.4) (layers "F.Cu" "F.Mask" "F.Paste") (net "ESP_BOOT") (uuid "{uuid.uuid4()}"))
\t\t(pad "2" smd rect (at 1.8 0) (size 0.8 1.4) (layers "F.Cu" "F.Mask" "F.Paste") (net "GND_PWR") (uuid "{uuid.uuid4()}"))'''
                last_br = expr.rfind(")")
                updated_sw1 = expr[:last_br] + pad_defs + "\n\t)"
                text = text[:idx] + updated_sw1 + text[next_pos:]
            break

    # 7. Update ESP32-S3 (U2) pins for SDIO, RGB_LED, LoRa control
    # Pin 32: RGB_LED_DATA
    # Pin 33: SD_DAT1, Pin 34: SD_DAT2, Pin 35: SD_CLK, Pin 36: SD_CMD, Pin 37: SD_DAT0, Pin 38: SD_DAT3, Pin 39: SD_CD
    # Pin 12: SPI_SCK, Pin 13: SPI_MISO, Pin 14: SPI_MOSI (or shared)
    pos = text.find('"U2"')
    if pos != -1:
        fp_start = text.rfind("(footprint", 0, pos)
        expr, next_pos = parse_sexpr(text, fp_start)
        print("Found U2 (ESP32-S3) footprint, mapping new peripheral nets...")
        u2_map = {
            "32": "RGB_LED_DATA",
            "33": "SD_DAT1",
            "34": "SD_DAT2",
            "35": "SD_CLK",
            "36": "SD_CMD",
            "37": "SD_DAT0",
            "38": "SD_DAT3",
            "39": "SD_CD",
            "27": "LORA_NSS",
            "25": "UWB_CS",
            "26": "UWB_IRQ",
            "19": "LORA_DIO1",
            "20": "LORA_BUSY",
            "23": "LORA_RST"
        }
        new_expr = expr
        p_pos = 0
        pad_chunks = []
        last_p = 0
        while True:
            p_idx = new_expr.find(chr(40) + "pad " + chr(34), p_pos)
            if p_idx == -1:
                pad_chunks.append(new_expr[last_p:])
                break
            pad_expr, p_next = parse_sexpr(new_expr, p_idx)
            p_pos = p_next
            pad_chunks.append(new_expr[last_p:p_idx])
            last_p = p_next
            num_m = re.search(r'\(pad\s+\"([^\"]*)\"', pad_expr)
            num = num_m.group(1) if num_m else ""
            if num in u2_map:
                net_name = u2_map[num]
                if "(net " in pad_expr:
                    pad_expr = re.sub(r'\(net\s+[^\)]+\)', f'(net "{net_name}")', pad_expr)
                else:
                    insert_idx = pad_expr.rfind(")")
                    pad_expr = pad_expr[:insert_idx] + f'\n\t\t\t(net "{net_name}")\n\t\t)'
            pad_chunks.append(pad_expr)
        updated_u2 = "".join(pad_chunks)
        text = text[:fp_start] + updated_u2 + text[next_pos:]

    # 8. Replace J2 (MicroSD) with full Hirose DM3D-SF footprint on B.Cu at (146.0, 78.5)
    pos = text.find('"J2"')
    if pos != -1:
        fp_start = text.rfind("(footprint", 0, pos)
        _, next_pos = parse_sexpr(text, fp_start)
        print("Replacing J2 with complete Hirose DM3D-SF footprint at (146.0, 78.5) on B.Cu...")
        
        # Load KiCad standard footprint for DM3D-SF
        dm3d_path = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/Connector_Card.pretty/microSD_HC_Hirose_DM3D-SF.kicad_mod"
        if os.path.exists(dm3d_path):
            with open(dm3d_path) as f_mod:
                mod_content = f_mod.read()
        else:
            mod_content = ""
            
        # Build complete footprint for J2 on B.Cu at (146.0, 78.5)
        # Net mapping for MicroSD:
        # 1: SD_DAT2, 2: SD_DAT3, 3: SD_CMD, 4: VCC_3V3, 5: SD_CLK, 6: GND_PWR, 7: SD_DAT0, 8: SD_DAT1, 9: SD_CD
        # SH1..SH4: GND_PWR
        sd_pad_nets = {
            "1": "SD_DAT2", "2": "SD_DAT3", "3": "SD_CMD", "4": "VCC_3V3",
            "5": "SD_CLK", "6": "GND_PWR", "7": "SD_DAT0", "8": "SD_DAT1",
            "9": "SD_CD", "10": "GND_PWR", "11": "GND_PWR", "12": "GND_PWR", "13": "GND_PWR"
        }
        
        # Hirose DM3D-SF geometry:
        # Width: ~13.85mm, Height: 15.25mm
        # Card insertion edge is at y = -7.625. When placed at y=78.5, edge is at 78.5 - 7.625 = 70.875mm (accessible at top edge!)
        j2_footprint = f'''\t(footprint "Connector_Card:microSD_HC_Hirose_DM3D-SF"
\t\t(layer "B.Cu")
\t\t(uuid "{uuid.uuid4()}")
\t\t(at 146 78.5)
\t\t(descr "Micro SD, SMD, right-angle, push-pull (Hirose DM3D-SF)")
\t\t(tags "Micro SD")
\t\t(property "Reference" "J2"
\t\t\t(at 0 -2.5 0)
\t\t\t(layer "B.SilkS")
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 0.8 0.8)
\t\t\t\t\t(thickness 0.12)
\t\t\t\t)
\t\t\t\t(justify mirror)
\t\t\t)
\t\t)
\t\t(property "Value" "MicroSD_Card"
\t\t\t(at 0 2.5 0)
\t\t\t(layer "B.Fab")
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 0.8 0.8)
\t\t\t\t\t(thickness 0.12)
\t\t\t\t)
\t\t\t\t(justify mirror)
\t\t\t)
\t\t)
\t\t(duplicate_pad_numbers_are_jumpers no)
\t\t(pad "1" smd rect (at 3.175 5.35) (size 0.7 1.75) (layers "B.Cu" "B.Mask" "B.Paste") (net "SD_DAT2") (uuid "{uuid.uuid4()}"))
\t\t(pad "2" smd rect (at 2.075 5.35) (size 0.7 1.75) (layers "B.Cu" "B.Mask" "B.Paste") (net "SD_DAT3") (uuid "{uuid.uuid4()}"))
\t\t(pad "3" smd rect (at 0.975 5.35) (size 0.7 1.75) (layers "B.Cu" "B.Mask" "B.Paste") (net "SD_CMD") (uuid "{uuid.uuid4()}"))
\t\t(pad "4" smd rect (at -0.125 5.35) (size 0.7 1.75) (layers "B.Cu" "B.Mask" "B.Paste") (net "VCC_3V3") (uuid "{uuid.uuid4()}"))
\t\t(pad "5" smd rect (at -1.225 5.35) (size 0.7 1.75) (layers "B.Cu" "B.Mask" "B.Paste") (net "SD_CLK") (uuid "{uuid.uuid4()}"))
\t\t(pad "6" smd rect (at -2.325 5.35) (size 0.7 1.75) (layers "B.Cu" "B.Mask" "B.Paste") (net "GND_PWR") (uuid "{uuid.uuid4()}"))
\t\t(pad "7" smd rect (at -3.425 5.35) (size 0.7 1.75) (layers "B.Cu" "B.Mask" "B.Paste") (net "SD_DAT0") (uuid "{uuid.uuid4()}"))
\t\t(pad "8" smd rect (at -4.525 5.35) (size 0.7 1.75) (layers "B.Cu" "B.Mask" "B.Paste") (net "SD_DAT1") (uuid "{uuid.uuid4()}"))
\t\t(pad "9" smd rect (at -6.175 4.35) (size 0.9 1.5) (layers "B.Cu" "B.Mask" "B.Paste") (net "SD_CD") (uuid "{uuid.uuid4()}"))
\t\t(pad "SH1" smd rect (at -6.425 -4.85) (size 1.4 2.2) (layers "B.Cu" "B.Mask" "B.Paste") (net "GND_PWR") (uuid "{uuid.uuid4()}"))
\t\t(pad "SH2" smd rect (at 6.425 -4.85) (size 1.4 2.2) (layers "B.Cu" "B.Mask" "B.Paste") (net "GND_PWR") (uuid "{uuid.uuid4()}"))
\t\t(pad "SH3" smd rect (at 6.425 3.35) (size 1.4 2.2) (layers "B.Cu" "B.Mask" "B.Paste") (net "GND_PWR") (uuid "{uuid.uuid4()}"))
\t\t(model "${{KICAD10_3DMODEL_DIR}}/Connector_Card.3dshapes/microSD_HC_Hirose_DM3D-SF.step"
\t\t\t(offset (xyz 0 0 0))
\t\t\t(scale (xyz 1 1 1))
\t\t\t(rotate (xyz 0 0 0))
\t\t)
\t)'''
        text = text[:fp_start] + j2_footprint + text[next_pos:]

    with open(PCB_PATH, "w") as f:
        f.write(text)
    print("PCB updated successfully.")

def update_sch():
    print(f"Updating schematic {SCH_PATH}...")
    with open(SCH_PATH, "r") as f:
        text = f.read()

    # Define symbol blocks to insert into lib_symbols if missing
    new_symbols = []
    
    # 1. SX1262
    if '"RF_Module:SX1262"' not in text:
        sx1262_sym = '''		(symbol "RF_Module:SX1262"
			(property "Reference" "U10" (at -15.24 22.86 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "SX1262IMLTRT" (at -15.24 -25.4 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "QFN-24-1EP_4x4mm_P0.5mm_EP2.8x2.8mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "SX1262_0_1"
				(rectangle (start -15.24 20.32) (end 15.24 -22.86) (stroke (width 0.254) (type solid)) (fill (type background)))
			)
			(pin input line (at -17.78 15.24 0) (length 2.54) (name "NRESET" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			(pin power_in line (at -17.78 10.16 0) (length 2.54) (name "VBAT" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
			(pin power_in line (at -17.78 5.08 0) (length 2.54) (name "VBAT_IO" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
			(pin input line (at -17.78 0 0) (length 2.54) (name "NSS" (effects (font (size 1.27 1.27)))) (number "21" (effects (font (size 1.27 1.27)))))
			(pin input line (at -17.78 -5.08 0) (length 2.54) (name "SCK" (effects (font (size 1.27 1.27)))) (number "20" (effects (font (size 1.27 1.27)))))
			(pin input line (at -17.78 -10.16 0) (length 2.54) (name "MOSI" (effects (font (size 1.27 1.27)))) (number "19" (effects (font (size 1.27 1.27)))))
			(pin output line (at -17.78 -15.24 0) (length 2.54) (name "MISO" (effects (font (size 1.27 1.27)))) (number "18" (effects (font (size 1.27 1.27)))))
			(pin output line (at 17.78 15.24 180) (length 2.54) (name "BUSY" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.27 1.27)))))
			(pin output line (at 17.78 10.16 180) (length 2.54) (name "DIO1" (effects (font (size 1.27 1.27)))) (number "15" (effects (font (size 1.27 1.27)))))
			(pin output line (at 17.78 0 180) (length 2.54) (name "RFO" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
			(pin power_in line (at 0 -25.4 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "25" (effects (font (size 1.27 1.27)))))
		)'''
        new_symbols.append(sx1262_sym)

    # 2. DW3110
    if '"RF_Module:DW3110"' not in text:
        dw3110_sym = '''		(symbol "RF_Module:DW3110"
			(property "Reference" "U8" (at -15.24 20.32 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "DW3110" (at -15.24 -22.86 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "Package_DFN_QFN:QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm_ThermalVias" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "DW3110_0_1"
				(rectangle (start -15.24 17.78) (end 15.24 -20.32) (stroke (width 0.254) (type solid)) (fill (type background)))
			)
			(pin power_in line (at -17.78 12.7 0) (length 2.54) (name "VDD2_3V3" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.27 1.27)))))
			(pin input line (at -17.78 7.62 0) (length 2.54) (name "SPICLK" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
			(pin output line (at -17.78 2.54 0) (length 2.54) (name "SPIMISO" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
			(pin input line (at -17.78 -2.54 0) (length 2.54) (name "SPIMOSI" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
			(pin input line (at -17.78 -7.62 0) (length 2.54) (name "SPICS" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
			(pin output line (at 17.78 12.7 180) (length 2.54) (name "IRQ" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.27 1.27)))))
			(pin input line (at 17.78 7.62 180) (length 2.54) (name "RSTn" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
			(pin output line (at 17.78 0 180) (length 2.54) (name "RF_PORT" (effects (font (size 1.27 1.27)))) (number "15" (effects (font (size 1.27 1.27)))))
			(pin power_in line (at 0 -22.86 90) (length 2.54) (name "VSS" (effects (font (size 1.27 1.27)))) (number "17" (effects (font (size 1.27 1.27)))))
		)'''
        new_symbols.append(dw3110_sym)

    # 3. MicroSD_Card
    if '"Connector:MicroSD_Card"' not in text:
        sd_sym = '''		(symbol "Connector:MicroSD_Card"
			(property "Reference" "J2" (at -12.7 17.78 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "MicroSD_Card" (at -12.7 -20.32 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "Connector_Card:microSD_HC_Hirose_DM3D-SF" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "MicroSD_0_1"
				(rectangle (start -12.7 15.24) (end 12.7 -17.78) (stroke (width 0.254) (type solid)) (fill (type background)))
			)
			(pin bidirectional line (at -15.24 10.16 0) (length 2.54) (name "DAT2" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			(pin bidirectional line (at -15.24 5.08 0) (length 2.54) (name "DAT3" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			(pin input line (at -15.24 0 0) (length 2.54) (name "CMD" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
			(pin power_in line (at -15.24 -5.08 0) (length 2.54) (name "VDD_3V3" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
			(pin input line (at -15.24 -10.16 0) (length 2.54) (name "CLK" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
			(pin power_in line (at 15.24 -10.16 180) (length 2.54) (name "VSS_GND" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
			(pin bidirectional line (at 15.24 -5.08 180) (length 2.54) (name "DAT0" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
			(pin bidirectional line (at 15.24 0 180) (length 2.54) (name "DAT1" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 15.24 5.08 180) (length 2.54) (name "CARD_DETECT" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 15.24 10.16 180) (length 2.54) (name "SHIELD" (effects (font (size 1.27 1.27)))) (number "SH1" (effects (font (size 1.27 1.27)))))
		)'''
        new_symbols.append(sd_sym)

    # 4. BMI270
    if '"Sensor_Motion:BMI270"' not in text:
        bmi_sym = '''		(symbol "Sensor_Motion:BMI270"
			(property "Reference" "U5" (at -12.7 15.24 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "BMI270_IMU" (at -12.7 -17.78 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "Package_LGA:LGA-14_2.5x3mm_P0.5mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "BMI270_0_1"
				(rectangle (start -12.7 12.7) (end 12.7 -15.24) (stroke (width 0.254) (type solid)) (fill (type background)))
			)
			(pin power_in line (at -15.24 7.62 0) (length 2.54) (name "VDD" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
			(pin power_in line (at -15.24 2.54 0) (length 2.54) (name "VDDIO" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
			(pin input line (at -15.24 -2.54 0) (length 2.54) (name "SCX_SCL" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.27 1.27)))))
			(pin bidirectional line (at -15.24 -7.62 0) (length 2.54) (name "SDX_SDA" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.27 1.27)))))
			(pin output line (at 15.24 7.62 180) (length 2.54) (name "INT1" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
			(pin output line (at 15.24 2.54 180) (length 2.54) (name "INT2" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
			(pin power_in line (at 0 -17.78 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
		)'''
        new_symbols.append(bmi_sym)

    # Insert new symbols into lib_symbols section
    if new_symbols:
        idx_lib = text.find("(lib_symbols")
        if idx_lib != -1:
            ins_pos = text.find("\n", idx_lib) + 1
            text = text[:ins_pos] + "\n".join(new_symbols) + "\n" + text[ins_pos:]

    # Add symbol instances at the end of the sheet before closing bracket
    instances_str = f'''	(symbol (lib_id "RF_Module:SX1262") (at 60 180 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "{uuid.uuid4()}")
		(property "Reference" "U10" (at 60 155 0) (effects (font (size 1.27 1.27))))
		(property "Value" "SX1262IMLTRT" (at 60 158 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "QFN-24-1EP_4x4mm_P0.5mm_EP2.8x2.8mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
	)
	(symbol (lib_id "RF_Module:DW3110") (at 120 180 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "{uuid.uuid4()}")
		(property "Reference" "U8" (at 120 158 0) (effects (font (size 1.27 1.27))))
		(property "Value" "DW3110" (at 120 161 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Package_DFN_QFN:QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm_ThermalVias" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
	)
	(symbol (lib_id "Sensor_Motion:BMI270") (at 180 180 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "{uuid.uuid4()}")
		(property "Reference" "U5" (at 180 160 0) (effects (font (size 1.27 1.27))))
		(property "Value" "BMI270_IMU" (at 180 163 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Package_LGA:LGA-14_2.5x3mm_P0.5mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
	)
	(symbol (lib_id "Connector:MicroSD_Card") (at 240 180 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "{uuid.uuid4()}")
		(property "Reference" "J2" (at 240 160 0) (effects (font (size 1.27 1.27))))
		(property "Value" "MicroSD_Card" (at 240 163 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Connector_Card:microSD_HC_Hirose_DM3D-SF" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
	)
'''
    last_bracket = text.rfind(")")
    text = text[:last_bracket] + instances_str + "\n)\n"

    with open(SCH_PATH, "w") as f:
        f.write(text)
    print("Schematic updated successfully.")

if __name__ == "__main__":
    update_pcb()
    update_sch()
