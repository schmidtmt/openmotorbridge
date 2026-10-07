#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
update_omm_intercom_stereo_and_usb.py
======================================
Pre-places and nets:
1. U4: Replace ES8311 (QFN-20 3x3mm) with Everest Semi ES8388 (QFN-28 4x4mm)
2. J1: Re-net USB-C port to 8-line Dual-Use Audio/Power/PTT mapping:
   - PGND / GND: A1, B12, A12, B1, SH
   - VBUS_5V: A4, B9, A9, B4
   - AGND_SPK: B8 (SBU2)
   - HP_OUT_L: A7, B7 (DN1, DN2)
   - HP_OUT_R: A6, B6 (DP1, DP2)
   - AGND_MIC: A5 (CC1)
   - MIC_IN+: A8 (SBU1)
   - PTT_IO: B5 (CC2)
3. Remove old tracks connected to the old U4 QFN-20 footprint to leave rat's nest clean for user.
"""

import os
import sys
import pcbnew

KICAD_FP_DIR = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"
PCB_PATH = "hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_pcb"
SCH_PATH = "hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_sch"

def to_nm(mm):
    return int(mm * 1e6)

def load_fp(lib, name):
    return pcbnew.FootprintLoad(os.path.join(KICAD_FP_DIR, lib), name)

def update_omm_pcb():
    board = pcbnew.LoadBoard(PCB_PATH)
    print("Updating PCBA 09 OMM Intercom PCB...")

    # 1. Setup required nets
    required_nets = [
        "GND", "VBUS_5V", "VBAT", "SYS_PWR", "VCC_3V3",
        "HP_OUT_L", "HP_OUT_R", "AGND_SPK", "MIC_IN+", "AGND_MIC", "PTT_IO",
        "I2S_MCLK", "I2S_BCLK", "I2S_WS", "I2S_DOUT", "I2S_DIN",
        "I2C_SDA", "I2C_SCL", "VREF", "MICBIAS",
        "BTN_PWR", "BTN_MESH", "BTN_VOL_UP", "BTN_VOL_DOWN",
        "WS2812_DATA", "CHG_STAT", "NTC_TS", "ISET", "ILIM"
    ]
    net_map = {}
    for name in required_nets:
        net = board.FindNet(name)
        if not net:
            net = pcbnew.NETINFO_ITEM(board, name)
            board.Add(net)
        net_map[name] = net

    # 2. Find and remove old U4 (ES8311)
    old_u4 = None
    u4_pos = pcbnew.VECTOR2I(to_nm(115.75), to_nm(101.25))
    for fp in board.GetFootprints():
        if fp.GetReference() == "U4":
            old_u4 = fp
            u4_pos = fp.GetPosition()
            break

    # Remove any tracks touching old U4 pads to avoid shorts with new QFN-28 footprint
    tracks_to_remove = []
    if old_u4:
        old_pads_boxes = [p.GetBoundingBox() for p in old_u4.Pads()]
        for t in board.GetTracks():
            for bbox in old_pads_boxes:
                if bbox.Contains(t.GetStart()) or bbox.Contains(t.GetEnd()):
                    tracks_to_remove.append(t)
                    break
        for t in tracks_to_remove:
            board.Remove(t)
        if tracks_to_remove:
            print(f"✓ Removed {len(tracks_to_remove)} old tracks at U4 footprint")
        board.Remove(old_u4)
        print("✓ Removed old mono U4 (ES8311 QFN-20)")

    # 3. Load and place new U4: ES8388 (QFN-28 4x4mm)
    new_u4 = load_fp("Package_DFN_QFN.pretty", "QFN-28-1EP_4x4mm_P0.4mm_EP2.4x2.4mm")
    if not new_u4:
        print("ERROR: Failed to load QFN-28-1EP_4x4mm_P0.4mm_EP2.4x2.4mm")
        return False

    new_u4.SetReference("U4")
    new_u4.SetValue("ES8388")
    new_u4.SetPosition(u4_pos)
    new_u4.SetOrientationDegrees(0.0)
    board.Add(new_u4)

    # ES8388 Pin Assignments:
    # 1: MCLK, 2: BCLK, 3: LRCK/WS, 4: SDIN (DOUT from C6), 5: SDOUT (DIN to C6)
    # 6: I2C_SDA, 7: I2C_SCL, 8: AD0 (GND), 9: DVDD (3V3), 10: DGND
    # 11: ROUT1 (HP_OUT_R), 12: LOUT1 (HP_OUT_L), 13: NC/ROUT2, 14: NC/LOUT2
    # 15: AVDD (3V3), 16: AGND (AGND_SPK), 17: VREF, 18: MICBIAS
    # 19: MIC1P (MIC_IN+), 20: MIC1N (AGND_MIC), 21: NC, 22: NC
    # 23: PVDD (3V3), 24: PGND (GND), 25: CE (3V3), 26-28: NC
    # 29 / EP: GND
    u4_net_assignments = {
        "1": "I2S_MCLK",
        "2": "I2S_BCLK",
        "3": "I2S_WS",
        "4": "I2S_DOUT",
        "5": "I2S_DIN",
        "6": "I2C_SDA",
        "7": "I2C_SCL",
        "8": "GND",
        "9": "VCC_3V3",
        "10": "GND",
        "11": "HP_OUT_R",
        "12": "HP_OUT_L",
        "15": "VCC_3V3",
        "16": "AGND_SPK",
        "17": "VREF",
        "18": "MICBIAS",
        "19": "MIC_IN+",
        "20": "AGND_MIC",
        "23": "VCC_3V3",
        "24": "GND",
        "25": "VCC_3V3",
        "29": "GND"
    }

    for pad in new_u4.Pads():
        num = pad.GetNumber()
        if num in u4_net_assignments:
            pad.SetNet(net_map[u4_net_assignments[num]])
        elif num in ["", "EP"]:
            pad.SetNet(net_map["GND"])
    print("✓ Placed and netted U4: ES8388 Stereo Codec (QFN-28 4x4mm)")

    # 4. Re-net J1 (USB-C) for Dual-Use Audio & 8-Pin Cartridge Connection
    j1_fp = None
    for fp in board.GetFootprints():
        if fp.GetReference() == "J1":
            j1_fp = fp
            break

    if j1_fp:
        # Reassign J1 pins to 8-line Dual-Use Audio/Power
        # A1, B12, A12, B1: PGND / GND
        # A4, B9, A9, B4: VBUS_5V
        # A5: AGND_MIC
        # B5: PTT_IO
        # A6, B6: HP_OUT_R (DP)
        # A7, B7: HP_OUT_L (DN)
        # A8: MIC_IN+ (SBU1)
        # B8: AGND_SPK (SBU2)
        j1_pad_assignments = {
            "A1": "GND",
            "B12": "GND",
            "A12": "GND",
            "B1": "GND",
            "A4": "VBUS_5V",
            "B9": "VBUS_5V",
            "A9": "VBUS_5V",
            "B4": "VBUS_5V",
            "A5": "AGND_MIC",
            "B5": "PTT_IO",
            "A6": "HP_OUT_R",
            "B6": "HP_OUT_R",
            "A7": "HP_OUT_L",
            "B7": "HP_OUT_L",
            "A8": "MIC_IN+",
            "B8": "AGND_SPK",
        }
        for pad in j1_fp.Pads():
            num = pad.GetNumber()
            if num in j1_pad_assignments:
                pad.SetNet(net_map[j1_pad_assignments[num]])
            else:
                pad.SetNet(net_map["GND"]) # Shield tabs / mounting pins to GND
        print("✓ Re-netted J1 (USB-C) to Dual-Use Audio/Power/PTT mapping")

    # Connect ESP32-C6 GPIO 2 (Pad BTN_PTT) to PTT_IO
    for fp in board.GetFootprints():
        if fp.GetReference() == "U1": # ESP32-C6
            for pad in fp.Pads():
                if pad.GetNumber() == "3": # GPIO 2 (BTN_PTT)
                    pad.SetNet(net_map["PTT_IO"])
                    print("✓ Connected U1 GPIO 2 to PTT_IO")

    # Refill copper zones
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())

    board.Save(PCB_PATH)
    print("✓ Saved updated openmotorbridge_omm_intercom.kicad_pcb")
    return True

def update_omm_schematic():
    sch_content = """(kicad_sch
\t(version 20260306)
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "f0000000-0000-0000-0000-000000000090")
\t(paper "A3")
\t(title_block
\t\t(title "OpenMotorBridge OMM 2.4 GHz Intercom & UCS Modul (PCBA 09)")
\t\t(date "2026-10-07")
\t\t(rev "v2.0-stereo")
\t\t(company "OpenMotorBridge Open Source Hardware")
\t\t(comment 1 "ESP32-C6-MINI-1U (On-Module U.FL), BQ24075 PMIC, ES8388 Stereo Codec, IP67 Dual-Use USB-C")
\t\t(comment 2 "USB-C mapped to 8-Pin Audio/Power/Kelvin Grounding for Smart Cartridge PCBA 03")
\t)

\t(lib_symbols
\t\t(symbol "Device:C_Small"
\t\t\t(pin passive line (at 0 2.54 270) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 0 -2.54 90) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t(property "Reference" "C" (at 1.905 0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t\t\t(property "Value" "C_Small" (at 1.905 -1.905 0) (effects (font (size 1.27 1.27)) (justify left)))
\t\t)
\t\t(symbol "Device:R_Small"
\t\t\t(pin passive line (at 0 2.54 270) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 0 -2.54 90) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t(property "Reference" "R" (at 1.905 0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t\t\t(property "Value" "R_Small" (at 1.905 -1.905 0) (effects (font (size 1.27 1.27)) (justify left)))
\t\t)
\t\t(symbol "Switch:SW_Push"
\t\t\t(pin passive line (at -5.08 0 0) (length 2.54) (name "1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 5.08 0 180) (length 2.54) (name "2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t(property "Reference" "SW" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "SW_Push" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
\t\t)
\t\t(symbol "Audio:ES8388"
\t\t\t(property "Reference" "U4" (at -12.7 20.32 0) (effects (font (size 1.27 1.27)) (justify left)))
\t\t\t(property "Value" "ES8388" (at -12.7 -22.86 0) (effects (font (size 1.27 1.27)) (justify left)))
\t\t\t(property "Footprint" "Package_DFN_QFN:QFN-28-1EP_4x4mm_P0.4mm_EP2.4x2.4mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(property "LCSC" "C365736" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(pin input line (at -15.24 15.24 0) (length 2.54) (name "MCLK" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin input line (at -15.24 10.16 0) (length 2.54) (name "BCLK" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t(pin input line (at -15.24 5.08 0) (length 2.54) (name "WS" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t(pin input line (at -15.24 0 0) (length 2.54) (name "SDIN" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t\t(pin output line (at -15.24 -5.08 0) (length 2.54) (name "SDOUT" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\t\t\t(pin bidirectional line (at -15.24 -10.16 0) (length 2.54) (name "SDA" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\t\t\t(pin input line (at -15.24 -15.24 0) (length 2.54) (name "SCL" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
\t\t\t(pin input line (at -15.24 -20.32 0) (length 2.54) (name "AD0" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
\t\t\t(pin power_in line (at 0 22.86 270) (length 2.54) (name "DVDD" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
\t\t\t(pin power_in line (at 0 -22.86 90) (length 2.54) (name "DGND" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
\t\t\t(pin output line (at 15.24 15.24 180) (length 2.54) (name "ROUT1" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
\t\t\t(pin output line (at 15.24 10.16 180) (length 2.54) (name "LOUT1" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
\t\t\t(pin power_in line (at 2.54 22.86 270) (length 2.54) (name "AVDD" (effects (font (size 1.27 1.27)))) (number "15" (effects (font (size 1.27 1.27)))))
\t\t\t(pin power_in line (at 2.54 -22.86 90) (length 2.54) (name "AGND" (effects (font (size 1.27 1.27)))) (number "16" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 15.24 5.08 180) (length 2.54) (name "VREF" (effects (font (size 1.27 1.27)))) (number "17" (effects (font (size 1.27 1.27)))))
\t\t\t(pin output line (at 15.24 0 180) (length 2.54) (name "MICBIAS" (effects (font (size 1.27 1.27)))) (number "18" (effects (font (size 1.27 1.27)))))
\t\t\t(pin input line (at 15.24 -5.08 180) (length 2.54) (name "MIC1P" (effects (font (size 1.27 1.27)))) (number "19" (effects (font (size 1.27 1.27)))))
\t\t\t(pin input line (at 15.24 -10.16 180) (length 2.54) (name "MIC1N" (effects (font (size 1.27 1.27)))) (number "20" (effects (font (size 1.27 1.27)))))
\t\t\t(pin power_in line (at 5.08 22.86 270) (length 2.54) (name "PVDD" (effects (font (size 1.27 1.27)))) (number "23" (effects (font (size 1.27 1.27)))))
\t\t\t(pin power_in line (at 5.08 -22.86 90) (length 2.54) (name "PGND" (effects (font (size 1.27 1.27)))) (number "24" (effects (font (size 1.27 1.27)))))
\t\t\t(pin input line (at -15.24 -25.4 0) (length 2.54) (name "CE" (effects (font (size 1.27 1.27)))) (number "25" (effects (font (size 1.27 1.27)))))
\t\t\t(pin power_in line (at 7.62 -22.86 90) (length 2.54) (name "EP" (effects (font (size 1.27 1.27)))) (number "29" (effects (font (size 1.27 1.27)))))
\t\t)
\t\t(symbol "Connector:USB_C_Receptacle_DualUse"
\t\t\t(pin power_in line (at -10.16 10.16 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "A1" (effects (font (size 1.27 1.27)))))
\t\t\t(pin power_in line (at -10.16 7.62 0) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "A4" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at -10.16 5.08 0) (length 2.54) (name "AGND_MIC" (effects (font (size 1.27 1.27)))) (number "A5" (effects (font (size 1.27 1.27)))))
\t\t\t(pin bidirectional line (at -10.16 2.54 0) (length 2.54) (name "HP_OUT_R" (effects (font (size 1.27 1.27)))) (number "A6" (effects (font (size 1.27 1.27)))))
\t\t\t(pin bidirectional line (at -10.16 0 0) (length 2.54) (name "HP_OUT_L" (effects (font (size 1.27 1.27)))) (number "A7" (effects (font (size 1.27 1.27)))))
\t\t\t(pin input line (at -10.16 -2.54 0) (length 2.54) (name "MIC_IN+" (effects (font (size 1.27 1.27)))) (number "A8" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 10.16 5.08 180) (length 2.54) (name "PTT_IO" (effects (font (size 1.27 1.27)))) (number "B5" (effects (font (size 1.27 1.27)))))
\t\t\t(pin passive line (at 10.16 -2.54 180) (length 2.54) (name "AGND_SPK" (effects (font (size 1.27 1.27)))) (number "B8" (effects (font (size 1.27 1.27)))))
\t\t\t(property "Reference" "J" (at -5.08 12.7 0) (effects (font (size 1.27 1.27)) (justify left)))
\t\t\t(property "Value" "USB_C_DualUse" (at -5.08 -12.7 0) (effects (font (size 1.27 1.27)) (justify left)))
\t\t)
\t)

\t(global_label "VBUS_5V" (shape input) (at 30.0 30.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "VBAT" (shape bidirectional) (at 30.0 35.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "SYS_PWR" (shape output) (at 80.0 30.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "VCC_3V3" (shape output) (at 80.0 35.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "GND" (shape passive) (at 30.0 40.0 180) (effects (font (size 1.27 1.27)) (justify right)))

\t(global_label "HP_OUT_L" (shape output) (at 140.0 30.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "HP_OUT_R" (shape output) (at 140.0 35.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "AGND_SPK" (shape passive) (at 140.0 40.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "MIC_IN+" (shape input) (at 140.0 45.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "AGND_MIC" (shape passive) (at 140.0 50.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "PTT_IO" (shape bidirectional) (at 140.0 55.0 0) (effects (font (size 1.27 1.27)) (justify left)))

\t(global_label "I2S_MCLK" (shape output) (at 200.0 30.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "I2S_BCLK" (shape output) (at 200.0 35.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "I2S_WS" (shape output) (at 200.0 40.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "I2S_DOUT" (shape output) (at 200.0 45.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "I2S_DIN" (shape input) (at 200.0 50.0 180) (effects (font (size 1.27 1.27)) (justify right)))
\t(global_label "I2C_SDA" (shape bidirectional) (at 200.0 55.0 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(global_label "I2C_SCL" (shape output) (at 200.0 60.0 0) (effects (font (size 1.27 1.27)) (justify left)))

\t(symbol (lib_id "Audio:ES8388") (at 120.0 100.0 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (dnp no)
\t\t(uuid "f0000000-0000-0000-0000-0000000000A0")
\t\t(property "Reference" "U4" (at 120.0 70.0 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "ES8388" (at 120.0 73.0 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "Package_DFN_QFN:QFN-28-1EP_4x4mm_P0.4mm_EP2.4x2.4mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(pin "1" (uuid "f0000000-0000-0000-0000-0000000000A1"))
\t\t(pin "2" (uuid "f0000000-0000-0000-0000-0000000000A2"))
\t\t(pin "3" (uuid "f0000000-0000-0000-0000-0000000000A3"))
\t\t(pin "4" (uuid "f0000000-0000-0000-0000-0000000000A4"))
\t\t(pin "5" (uuid "f0000000-0000-0000-0000-0000000000A5"))
\t\t(pin "6" (uuid "f0000000-0000-0000-0000-0000000000A6"))
\t\t(pin "7" (uuid "f0000000-0000-0000-0000-0000000000A7"))
\t\t(pin "8" (uuid "f0000000-0000-0000-0000-0000000000A8"))
\t\t(pin "9" (uuid "f0000000-0000-0000-0000-0000000000A9"))
\t\t(pin "10" (uuid "f0000000-0000-0000-0000-0000000000AA"))
\t\t(pin "11" (uuid "f0000000-0000-0000-0000-0000000000AB"))
\t\t(pin "12" (uuid "f0000000-0000-0000-0000-0000000000AC"))
\t\t(pin "15" (uuid "f0000000-0000-0000-0000-0000000000AD"))
\t\t(pin "16" (uuid "f0000000-0000-0000-0000-0000000000AE"))
\t\t(pin "17" (uuid "f0000000-0000-0000-0000-0000000000AF"))
\t\t(pin "18" (uuid "f0000000-0000-0000-0000-0000000000B0"))
\t\t(pin "19" (uuid "f0000000-0000-0000-0000-0000000000B1"))
\t\t(pin "20" (uuid "f0000000-0000-0000-0000-0000000000B2"))
\t\t(pin "23" (uuid "f0000000-0000-0000-0000-0000000000B3"))
\t\t(pin "24" (uuid "f0000000-0000-0000-0000-0000000000B4"))
\t\t(pin "25" (uuid "f0000000-0000-0000-0000-0000000000B5"))
\t\t(pin "29" (uuid "f0000000-0000-0000-0000-0000000000B6"))
\t)

\t(symbol (lib_id "Connector:USB_C_Receptacle_DualUse") (at 60.0 100.0 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (dnp no)
\t\t(uuid "f0000000-0000-0000-0000-0000000000C0")
\t\t(property "Reference" "J1" (at 60.0 85.0 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "TYPE-C-31-M-12_IP67" (at 60.0 88.0 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t(pin "A1" (uuid "f0000000-0000-0000-0000-0000000000C1"))
\t\t(pin "A4" (uuid "f0000000-0000-0000-0000-0000000000C2"))
\t\t(pin "A5" (uuid "f0000000-0000-0000-0000-0000000000C3"))
\t\t(pin "A6" (uuid "f0000000-0000-0000-0000-0000000000C4"))
\t\t(pin "A7" (uuid "f0000000-0000-0000-0000-0000000000C5"))
\t\t(pin "A8" (uuid "f0000000-0000-0000-0000-0000000000C6"))
\t\t(pin "B5" (uuid "f0000000-0000-0000-0000-0000000000C7"))
\t\t(pin "B8" (uuid "f0000000-0000-0000-0000-0000000000C8"))
\t)
)
"""
    with open(SCH_PATH, "w", encoding="utf-8") as f:
        f.write(sch_content)
    print("✓ Saved updated openmotorbridge_omm_intercom.kicad_sch")
    return True

if __name__ == "__main__":
    if update_omm_pcb() and update_omm_schematic():
        print("\n✨ PCBA 09 OMM Intercom successfully updated to ES8388 Stereo & Dual-Use USB-C!")
    else:
        print("\n❌ Update failed.")
        sys.exit(1)
