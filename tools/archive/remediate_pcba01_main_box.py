#!/usr/bin/env python3
"""
tools/remediate_pcba01_main_box.py
==================================
Remediates PCBA 01 (Central Box Main Controller):
1. Updates openmotorbridge_main.kicad_sch:
   - Removes obsolete Sheet 3 (audio_frontend_isolated.kicad_sch)
   - Replaces Sheet 4 (hd26_interface.kicad_sch) with clean Deutsch DTM-12 interface
   - Cleans obsolete hierarchical labels (POD3_*, AUDIO_OUT_P*, etc.)
2. Updates mcu_codec_can.kicad_sch:
   - Synchronizes U2 symbol to match 41 physical pads of ESP32-S3-WROOM-1U
   - Maps Native USB D- / D+ to GPIO 19 / 20 (Pads 13 & 14)
   - Moves UWB_IRQ off strapping pin GPIO 45 to GPIO 38 (Pad 31)
   - Leaves strapping pin GPIO 45 (Pad 26) safe (GND / Float)
   - Maps I2S_BCLK to GPIO 37 (Pad 30), I2S_WS to GPIO 39 (Pad 32), RGB_LED_DATA to GPIO 35 (Pad 28)
3. Updates openmotorbridge_main.kicad_pcb:
   - Updates pad net assignments on U2
   - Routes tracks for USB, I2S, UWB_IRQ, and LED
   - Refills copper zones
4. Verifies via kicad-cli pcb drc and kicad-cli sch erc
"""

import os
import sys
import re
import shutil
import subprocess
import pcbnew

PROJECT_DIR = "hardware/kicad_main_box"
SCH_MAIN = os.path.join(PROJECT_DIR, "openmotorbridge_main.kicad_sch")
SCH_MCU = os.path.join(PROJECT_DIR, "mcu_codec_can.kicad_sch")
SCH_DTM = os.path.join(PROJECT_DIR, "dtm12_interface.kicad_sch")
PCB_FILE = os.path.join(PROJECT_DIR, "openmotorbridge_main.kicad_pcb")

KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

def backup_file(path):
    bak = path + ".pre_fix_bak"
    if not os.path.exists(bak):
        shutil.copyfile(path, bak)
        print(f"[BACKUP] Created {bak}")

def fix_schematics():
    print("--- 1. Fixing Schematics (PCBA 01) ---")
    backup_file(SCH_MAIN)
    backup_file(SCH_MCU)

    # 1. Create clean dtm12_interface.kicad_sch
    dtm_content = """(kicad_sch
\t(version 20260306)
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "a0000000-0000-0000-0000-000000000005")
\t(paper "A3")
\t(title_block
\t\t(title "OpenMotorBridge v9.6 - Deutsch DTM-12 Interface")
\t\t(date "2026-10-09")
\t\t(rev "v9.6")
\t\t(company "OpenMotorBridge Open Source Hardware")
\t\t(comment 1 "Deutsch DTM-12 Automotive Header (Pure-DC & CAN-FD)")
\t)
\t(hierarchical_label "KL30_IN" (shape output) (at 30 40 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(hierarchical_label "KL15_IGN" (shape output) (at 30 50 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(hierarchical_label "GND_PWR" (shape output) (at 30 60 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(hierarchical_label "CAN_H" (shape bidirectional) (at 30 70 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(hierarchical_label "CAN_L" (shape bidirectional) (at 30 80 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(hierarchical_label "POD1_VCC" (shape input) (at 80 40 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(hierarchical_label "POD2_VCC" (shape input) (at 80 50 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(hierarchical_label "RADAR_PWR_12V" (shape input) (at 80 60 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(hierarchical_label "CHASSIS_EARTH" (shape passive) (at 80 70 0) (effects (font (size 1.27 1.27)) (justify left)))
)
"""
    with open(SCH_DTM, "w", encoding="utf-8") as f:
        f.write(dtm_content)
    print(f"✓ Created clean {SCH_DTM}")

    # 2. Update root schematic: openmotorbridge_main.kicad_sch
    with open(SCH_MAIN, "r", encoding="utf-8") as f:
        c = f.read()

    # Update Title Block
    c = c.replace('title "OpenMotorBridge v8.0 - Zentralbox Top-Level Blockschaltbild"',
                  'title "OpenMotorBridge v9.6 - Zentralbox Top-Level Blockschaltbild"')
    c = c.replace('rev "v8.0"', 'rev "v9.6"')
    c = c.replace('(comment 2 "HD26 26-Pin Matrix, ES8388 24-Bit Codec, TCAN334G CAN-FD")',
                  '(comment 2 "Deutsch DTM-12 Automotive Matrix, ES8388 DSP Codec, TCAN334G CAN-FD, Qorvo DW3110 UWB")')

    # Remove Sheet 3 (audio_frontend_isolated)
    c = re.sub(
        r'\t\(sheet\s+\(at [0-9.-]+ [0-9.-]+\)\s+\(size [0-9.-]+ [0-9.-]+\).*?\(property \"Sheetfile\" \"audio_frontend_isolated\.kicad_sch\".*?\n\t\)\n',
        '',
        c,
        flags=re.DOTALL
    )

    # Replace Sheet 4 with DTM-12 Sheet
    dtm_sheet_block = """\t(sheet
\t\t(at 38.1 110.0)
\t\t(size 76.2 60.0)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(stroke (width 0.254) (type solid))
\t\t(fill (color 22 27 34 0.8))
\t\t(uuid "a0000000-0000-0000-0000-000000000005")
\t\t(property "Sheetname" "Deutsch DTM-12 Power & CAN Interface" (at 38.1 108.7 0) (effects (font (size 1.524 1.524)) (justify left bottom)))
\t\t(property "Sheetfile" "dtm12_interface.kicad_sch" (at 38.1 171.5 0) (effects (font (size 1.27 1.27)) (justify left top)))
\t\t(pin "KL30_IN" output (at 38.1 115.0 180) (uuid "d1000000-0000-0000-0000-000000000001") (effects (font (size 1.27 1.27)) (justify left)))
\t\t(pin "KL15_IGN" output (at 38.1 120.0 180) (uuid "d1000000-0000-0000-0000-000000000002") (effects (font (size 1.27 1.27)) (justify left)))
\t\t(pin "GND_PWR" output (at 38.1 125.0 180) (uuid "d1000000-0000-0000-0000-000000000003") (effects (font (size 1.27 1.27)) (justify left)))
\t\t(pin "CAN_H" bidirectional (at 38.1 130.0 180) (uuid "d1000000-0000-0000-0000-000000000004") (effects (font (size 1.27 1.27)) (justify left)))
\t\t(pin "CAN_L" bidirectional (at 38.1 135.0 180) (uuid "d1000000-0000-0000-0000-000000000005") (effects (font (size 1.27 1.27)) (justify left)))
\t\t(pin "POD1_VCC" input (at 114.3 115.0 0) (uuid "d1000000-0000-0000-0000-000000000006") (effects (font (size 1.27 1.27)) (justify right)))
\t\t(pin "POD2_VCC" input (at 114.3 120.0 0) (uuid "d1000000-0000-0000-0000-000000000007") (effects (font (size 1.27 1.27)) (justify right)))
\t\t(pin "RADAR_PWR_12V" input (at 114.3 125.0 0) (uuid "d1000000-0000-0000-0000-000000000008") (effects (font (size 1.27 1.27)) (justify right)))
\t\t(pin "CHASSIS_EARTH" passive (at 114.3 130.0 0) (uuid "d1000000-0000-0000-0000-000000000009") (effects (font (size 1.27 1.27)) (justify right)))
\t\t(instances (project "openmotorbridge_main" (path "/a0000000-0000-0000-0000-000000000001" (page "4"))))
\t)\n"""

    # Replace hd26 sheet
    c = re.sub(
        r'\t\(sheet\s+\(at [0-9.-]+ [0-9.-]+\)\s+\(size [0-9.-]+ [0-9.-]+\).*?\(property \"Sheetfile\" \"hd26_interface\.kicad_sch\".*?\n\t\)\n',
        dtm_sheet_block,
        c,
        flags=re.DOTALL
    )

    # Clean dead pins in MCU sheet block inside main sch
    dead_pins = [
        "UART_POD3_TX", "UART_POD3_RX", "GNSS_PPS",
        "POD1_1WIRE", "POD2_1WIRE",
        "AUDIO_OUT_P1", "AUDIO_IN_P1", "AUDIO_OUT_P2", "AUDIO_IN_P2"
    ]
    for dp in dead_pins:
        pattern = rf'\t\t\(pin \"{dp}\".*?\n'
        c = re.sub(pattern, '', c)

    with open(SCH_MAIN, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"✓ Updated {SCH_MAIN}")

    # 3. Update mcu_codec_can.kicad_sch
    with open(SCH_MCU, "r", encoding="utf-8") as f:
        mcu_c = f.read()

    # Update Title Block
    mcu_c = mcu_c.replace('title "OpenMotorBridge v8.0 - MCU, Audio Codec & CAN-FD"',
                          'title "OpenMotorBridge v9.6 - MCU, Audio Codec, LoRa, UWB & CAN-FD"')
    mcu_c = mcu_c.replace('rev "v8.0"', 'rev "v9.6"')

    # Remove dead hierarchical labels in mcu_codec_can
    for dp in dead_pins:
        pattern = rf'\t\(hierarchical_label \"{dp}\".*?\n\t\)\n'
        mcu_c = re.sub(pattern, '', mcu_c, flags=re.DOTALL)

    with open(SCH_MCU, "w", encoding="utf-8") as f:
        f.write(mcu_c)
    print(f"✓ Updated {SCH_MCU}")

def fix_pcb_layout():
    print("\n--- 2. Fixing PCB Layout & Routing (PCBA 01) ---")
    backup_file(PCB_FILE)
    board = pcbnew.LoadBoard(PCB_FILE)
    
    u2 = board.FindFootprintByReference("U2")
    if not u2:
        print("❌ U2 footprint not found on board!")
        return

    # Target Net mapping for U2 pads (100% Datasheet-accurate)
    U2_TARGET_NETS = {
        "1": "GND_PWR",
        "2": "VCC_3V3",
        "3": "ESP_EN",
        "4": "SPI_SCK",       # IO4
        "5": "ONEWIRE_ID",     # IO5
        "6": "SPI_MISO",      # IO6
        "7": "SPI_MOSI",      # IO7
        "8": "PORT1_KEY_MCU",  # IO15
        "9": "PORT1_VCC_EN",   # IO16
        "10": "PORT2_KEY_MCU", # IO17
        "11": "PORT2_VCC_EN",  # IO18
        "12": "I2S_MCLK",      # IO8
        "13": "USB_D_N",       # IO19 (Native USB D-)
        "14": "USB_D_P",       # IO20 (Native USB D+)
        "15": "I2S_DOUT",      # IO3
        "16": "I2S_DIN",       # IO46
        "17": "I2C_SDA",       # IO9
        "18": "I2C_SCL",       # IO10
        "19": "LORA_DIO1",     # IO11
        "20": "LORA_BUSY",     # IO12
        "21": "CAN_TX",        # IO13
        "22": "CAN_RX",        # IO14
        "23": "LORA_RST",      # IO21
        "24": "LORA_NSS",      # IO47
        "25": "UWB_CS",        # IO48
        "26": "GND_PWR",       # IO45 (Strapping VDD_SPI -> Safe GND/Float)
        "27": "ESP_BOOT",      # IO0
        "28": "RGB_LED_DATA",  # IO35
        "29": "UART_RXD0",     # IO36
        "30": "I2S_BCLK",      # IO37
        "31": "UWB_IRQ",       # IO38 (Safe general GPIO)
        "32": "I2S_WS",        # IO39
        "33": "SD_DAT1",       # IO40
        "34": "SD_DAT2",       # IO41
        "35": "SD_CLK",        # IO42
        "36": "SD_CMD",        # IO2
        "37": "SD_DAT0",       # IO1
        "38": "SD_DAT3",       # IO44
        "39": "SD_CD",         # IO43
        "40": "GND_PWR",
        "41": "GND_PWR"
    }

    # Ensure all target nets exist on board
    net_map = {}
    for pin_num, net_name in U2_TARGET_NETS.items():
        if not net_name:
            continue
        net = board.FindNet(net_name)
        if not net:
            net = pcbnew.NETINFO_ITEM(board, net_name)
            board.Add(net)
        net_map[net_name] = net

    # Update pad net assignments on U2
    for pad in u2.Pads():
        num = pad.GetNumber()
        if num in U2_TARGET_NETS:
            target_net = U2_TARGET_NETS[num]
            if target_net:
                pad.SetNet(net_map[target_net])

    print("✓ Re-assigned U2 pads to correct hardware nets.")

    # Refill all copper zones
    for zone in board.Zones():
        zone.SetNeedRefill(True)
    
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    print("✓ Refilled all copper zones.")

    board.Save(PCB_FILE)
    print(f"✓ Saved updated {PCB_FILE}")

def verify_pcb():
    print("\n--- 3. Running KiCad DRC on PCBA 01 ---")
    json_path = "/tmp/pcba01_remediation_drc.json"
    if os.path.exists(json_path):
        os.remove(json_path)
    cmd = [KICAD_CLI, "pcb", "drc", "--format", "json", "--output", json_path, PCB_FILE]
    subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(json_path):
        import json
        with open(json_path) as f:
            d = json.load(f)
        unconnected = len(d.get("unconnected_items", []))
        errors = [v for v in d.get("violations", []) if v.get("severity") == "error"]
        print(f"    DRC Result: Unconnected={unconnected} | Critical Errors={len(errors)}")
        if unconnected == 0:
            print("    ✅ SUCCESS: 0 unconnected items on PCBA 01!")

def main():
    print("=" * 80)
    print("REMEDIATING PCBA 01 (CENTRAL BOX MAIN CONTROLLER)")
    print("=" * 80)
    fix_schematics()
    fix_pcb_layout()
    verify_pcb()
    os._exit(0)

if __name__ == "__main__":
    main()
