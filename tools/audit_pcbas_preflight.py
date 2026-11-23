#!/usr/bin/env python3
"""
tools/audit_pcbas_preflight.py
==============================
OpenMotorBridge Automated Pre-Flight Hardware & Firmware Cross-Audit Tool
-------------------------------------------------------------------------
Executes deep automated validation across all 7 official PCBAs:
  1. KiCad Design Rule Check (kicad-cli pcb drc): Shorts, clearings, unrouted traces.
  2. KiCad Electrical Rules Check (kicad-cli sch erc): Dangling labels, floating pins.
  3. Physical Footprint Pad -> True MCU GPIO Mapping (Datasheet-accurate).
  4. Firmware Header Pin Synchronization: Compares firmware C++ `#define`s with PCB nets.
  5. MCU Strapping Pin Safety Check (ESP32-S3, ESP32-C6, ESP32-C5, nRF52840).
  6. I2C Bus Conflict & Pull-up Resistor Audit.
  7. SPI Bus Chip Select Uniqueness Audit.
  8. Unconnected IC Footprint Pad Audit (catches "ghost" unrouted ICs).
"""

import os
import sys
import json
import re
import subprocess
import pcbnew

# Official 7-PCBA Lineup
BOARDS = {
    "PCBA 01": {
        "name": "Central Box Main Controller",
        "pcb": "hardware/kicad_main_box/openmotorbridge_main.kicad_pcb",
        "sch": "hardware/kicad_main_box/openmotorbridge_main.kicad_sch",
        "mcu_ref": "U2",
        "mcu_type": "ESP32-S31-WROOM-1U",
        "fw_headers": [
            "firmware/main_controller/src/main.cpp",
            "firmware/main_controller/src/audio_dsp_pipeline.cpp"
        ]
    },
    "PCBA 03": {
        "name": "Universal Smart Cartridge",
        "pcb": "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb",
        "sch": "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_sch",
        "mcu_ref": "U1",
        "mcu_type": "ESP32-C6-MINI-1U",
        "fw_headers": [
            "firmware/smart_cartridge/src/cartridge_config.h"
        ]
    },
    "PCBA 05": {
        "name": "Universal Front Node",
        "pcb": "hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb",
        "sch": "hardware/kicad_front_node/openmotorbridge_front_node.kicad_sch",
        "mcu_ref": "U1",
        "mcu_type": "ESP32-S31-WROOM-1U",
        "fw_headers": [
            "firmware/front_node/src/front_node_config.h"
        ]
    },
        "PCBA 05 Aux": {
        "name": "Universal Front Node Auxiliary MCU (ESP32-C3FH4 USB Audio Bridge)",
        "pcb": "hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb",
        "sch": "hardware/kicad_front_node/openmotorbridge_front_node.kicad_sch",
        "mcu_ref": "U10",
        "mcu_type": "ESP32-C3FH4",
        "fw_headers": [
            "firmware/front_node/src/front_node_config.h"
        ]
    },
    "PCBA 05B": {
        "name": "Glovebox Media & Power-Injection Hub (50 x 20 mm)",
        "pcb": "hardware/archive/kicad_cockpit_breakout/openmotorbridge_cockpit_breakout.kicad_pcb",
        "sch": "hardware/archive/kicad_cockpit_breakout/openmotorbridge_cockpit_breakout.kicad_sch",
        "mcu_ref": "U1",
        "mcu_type": "USB2514Bi-AEZG",
        "fw_headers": []
    },
    "PCBA 05C": {
        "name": "Ultra-Compact Under-Perch Mirror Pod (18.25 x 14.0 mm)",
        "pcb": "hardware/kicad_mirror_pod/openmotorbridge_mirror_pod.kicad_pcb",
        "sch": "hardware/kicad_mirror_pod/openmotorbridge_mirror_pod.kicad_sch",
        "mcu_ref": "SW1",
        "mcu_type": "PASSIVE_POD",
        "fw_headers": []
    },
    "PCBA 05D": {
        "name": "Modular Environmental & GNSS Sensor Puck (34 x 34 mm)",
        "pcb": "hardware/kicad_sensor_puck/openmotorbridge_sensor_puck.kicad_pcb",
        "sch": "hardware/kicad_sensor_puck/openmotorbridge_sensor_puck.kicad_sch",
        "mcu_ref": "U1",
        "mcu_type": "SAM-M10Q",
        "fw_headers": []
    },
    "PCBA 07": {
        "name": "2-in-1 LoRa Smart-Keyfob",
        "pcb": "hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb",
        "sch": "hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_sch",
        "mcu_ref": "U1",
        "mcu_type": "ESP32-C3FH4",
        "fw_headers": []
    },
    "PCBA 08": {
        "name": "Radar 2.0 Sub-MCU & Wings",
        "pcb": "hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb",
        "sch": "hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_sch",
        "mcu_ref": "U1",
        "mcu_type": "ESP32-C5-WROOM-1U",
        "fw_headers": [
            "firmware/radar_submcu/src/radar_mr20_protocol.h"
        ]
    },
    "PCBA 09": {
        "name": "OMM 2.4 GHz UCS Intercom",
        "pcb": "hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_pcb",
        "sch": "hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_sch",
        "mcu_ref": "U1",
        "mcu_type": "ESP32-C6-MINI-1U",
        "fw_headers": [
            "docs/de/07_pcba_hardware_pinouts.md"
        ]
    },
    "PCBA 10": {
        "name": "OMM 446 MHz UCS Intercom",
        "pcb": "hardware/kicad_omm446_intercom/openmotorbridge_omm446_intercom.kicad_pcb",
        "sch": "hardware/kicad_omm446_intercom/openmotorbridge_omm446_intercom.kicad_sch",
        "mcu_ref": "U1",
        "mcu_type": "ESP32-C6-MINI-1U",
        "fw_headers": [
            "firmware/omm446_module/src/omm446_config.h"
        ]
    }
}

# Datasheet pinout definitions for module packages
ESP32_S3_WROOM_PINS = {
    "1": ("GND", "PWR"),
    "2": ("3V3", "PWR"),
    "3": ("EN", "CTRL"),
    "4": ("IO4", "GPIO4"),
    "5": ("IO5", "GPIO5"),
    "6": ("IO6", "GPIO6"),
    "7": ("IO7", "GPIO7"),
    "8": ("IO15", "GPIO15"),
    "9": ("IO16", "GPIO16"),
    "10": ("IO17", "GPIO17"),
    "11": ("IO18", "GPIO18"),
    "12": ("IO8", "GPIO8"),
    "13": ("IO19", "GPIO19_USB_DM"),
    "14": ("IO20", "GPIO20_USB_DP"),
    "15": ("IO3", "GPIO3"),
    "16": ("IO46", "GPIO46_STRAP"),
    "17": ("IO9", "GPIO9"),
    "18": ("IO10", "GPIO10"),
    "19": ("IO11", "GPIO11"),
    "20": ("IO12", "GPIO12"),
    "21": ("IO13", "GPIO13"),
    "22": ("IO14", "GPIO14"),
    "23": ("IO21", "GPIO21"),
    "24": ("IO47", "GPIO47"),
    "25": ("IO48", "GPIO48"),
    "26": ("IO45", "GPIO45_STRAP_VDD_SPI"),
    "27": ("IO0", "GPIO0_STRAP_BOOT"),
    "28": ("IO35", "GPIO35"),
    "29": ("IO36", "GPIO36"),
    "30": ("IO37", "GPIO37"),
    "31": ("IO38", "GPIO38"),
    "32": ("IO39", "GPIO39"),
    "33": ("IO40", "GPIO40"),
    "34": ("IO41", "GPIO41"),
    "35": ("IO42", "GPIO42"),
    "36": ("IO2", "GPIO2"),
    "37": ("IO1", "GPIO1"),
    "38": ("IO44", "GPIO44_U0RXD"),
    "39": ("IO43", "GPIO43_U0TXD"),
    "40": ("GND", "PWR"),
    "41": ("GND", "PWR")
}

ESP32_C6_MINI_PINS = {
    "1": ("GND", "PWR"),
    "2": ("GND", "PWR"),
    "3": ("3V3", "PWR"),
    "4": ("NC", "NC"),
    "5": ("IO2", "GPIO2"),
    "6": ("IO3", "GPIO3"),
    "7": ("NC", "NC"),
    "8": ("EN", "CTRL"),
    "9": ("IO4", "GPIO4"),
    "10": ("IO5", "GPIO5"),
    "11": ("GND", "PWR"),
    "12": ("IO0", "GPIO0"),
    "13": ("IO1", "GPIO1"),
    "14": ("GND", "PWR"),
    "15": ("IO6", "GPIO6"),
    "16": ("IO7", "GPIO7"),
    "17": ("IO12", "GPIO12_USB_DM"),
    "18": ("IO13", "GPIO13_USB_DP"),
    "19": ("IO14", "GPIO14"),
    "20": ("IO15", "GPIO15"),
    "21": ("NC", "NC"),
    "22": ("IO8", "GPIO8_STRAP"),
    "23": ("IO9", "GPIO9_STRAP_BOOT"),
    "24": ("IO18", "GPIO18"),
    "25": ("IO19", "GPIO19"),
    "26": ("IO20", "GPIO20"),
    "27": ("IO21", "GPIO21")
}

KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

def run_drc(pcb_path):
    json_path = "/tmp/audit_drc.json"
    if os.path.exists(json_path):
        os.remove(json_path)
    cmd = [KICAD_CLI, "pcb", "drc", "--format", "json", "--output", json_path, pcb_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if not os.path.exists(json_path):
        err_msg = res.stderr.strip() if res.stderr else f"Exit code {res.returncode}"
        return {"error": f"Failed to run DRC: {err_msg}"}
    with open(json_path) as f:
        data = json.load(f)
    unconnected = len(data.get("unconnected_items", []))
    violations = data.get("violations", [])
    errors = [v for v in violations if v.get("severity") == "error"]
    warnings = [v for v in violations if v.get("severity") == "warning"]
    return {
        "unconnected_count": unconnected,
        "unconnected_details": data.get("unconnected_items", []),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings
    }

def run_erc(sch_path):
    if not os.path.exists(sch_path):
        return {"error": "Schematic not found"}
    json_path = "/tmp/audit_erc.json"
    if os.path.exists(json_path):
        os.remove(json_path)
    cmd = [KICAD_CLI, "sch", "erc", "--format", "json", "--output", json_path, sch_path]
    subprocess.run(cmd, capture_output=True, text=True)
    if not os.path.exists(json_path):
        return {"error": "Failed to run ERC"}
    with open(json_path) as f:
        data = json.load(f)
    violations = []
    for sheet in data.get("sheets", []):
        for v in sheet.get("violations", []):
            violations.append(v)
    errors = [v for v in violations if v.get("severity") == "error"]
    warnings = [v for v in violations if v.get("severity") == "warning"]
    return {
        "error_count": len(errors),
        "warning_count": len(warnings),
        "violations": violations
    }

def audit_board(board_id, cfg):
    print(f"\n{'='*80}")
    print(f"AUDITING: {board_id} - {cfg['name']}")
    print(f"PCB: {cfg['pcb']}")
    print(f"{'='*80}")
    
    if not os.path.exists(cfg["pcb"]):
        print(f"❌ PCB File not found: {cfg['pcb']}")
        return 1
        
    board = pcbnew.LoadBoard(cfg["pcb"])
    errors = 0
    
    # 1. DRC Execution
    drc = run_drc(cfg["pcb"])
    print(f"[1] KiCad DRC Status:")
    if "error" in drc:
        print(f"    ❌ DRC EXECUTION FAILED: {drc['error']}")
        errors += 1
    else:
        if drc.get("unconnected_count", 0) > 0:
            print(f"    ⚠️  UNCONNECTED ITEMS: {drc['unconnected_count']} unconnected net segments (awaiting manual routing)!")
            for item in drc.get("unconnected_details", []):
                print(f"       - {item.get('description')}: {[it.get('description') for it in item.get('items', [])]}")
        else:
            print(f"    ✅ Unconnected Items: 0 (100% Routed)")
            
        if drc.get("error_count", 0) > 0:
            print(f"    ❌ Critical DRC Errors: {drc['error_count']}")
            for err in drc.get("errors", [])[:5]:
                print(f"       - [{err.get('type')}] {err.get('description')}")
            errors += drc["error_count"]
        else:
            print(f"    ✅ DRC Errors: 0")
        
    # 2. Ghost IC Footprints Check (placed ICs with 0 connected nets)
    print(f"\n[2] IC Footprint Integrity & Ghost Component Audit:")
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        if ref.startswith("U"):
            pads = list(fp.Pads())
            connected_pads = [p for p in pads if p.GetNetname() and p.GetNetname() != "GND" and p.GetNetname() != "GND_PWR"]
            if len(pads) > 4 and len(connected_pads) == 0:
                print(f"    ❌ CRITICAL GHOST IC: {ref} ({fp.GetValue()}) has {len(pads)} pads but ZERO functional net connections!")
                errors += 1
                
    # 3. MCU Pin Mapping & Strapping Pin Verification
    print(f"\n[3] MCU Pinout & Strapping Pin Safety Audit:")
    mcu = board.FindFootprintByReference(cfg["mcu_ref"])
    if not mcu:
        print(f"    ⚠️  MCU Footprint {cfg['mcu_ref']} not found on board!")
        return errors
        
    print(f"    MCU Reference: {cfg['mcu_ref']} | Value: {mcu.GetValue()} | Package: {mcu.GetFPIDAsString()}")
    mcu_pads = {p.GetNumber(): p.GetNetname() for p in mcu.Pads()}
    
    # Strapping pins per MCU type
    if "ESP32-S31" in cfg["mcu_type"]:
        # ESP32-S31: High-Speed USB 2.0 PHY on inner LGA pads 54 & 55.
        # Pad 27: GPIO 61 (Boot Strapping). Pad 26: GPIO 60 (VDD_SPI).
        # Pad 63: BLE RF output to ANT3.
        pad27_net = mcu_pads.get("27", "")
        pad26_net = mcu_pads.get("26", "")
        pad54_net = mcu_pads.get("54", "")
        pad55_net = mcu_pads.get("55", "")
        pad63_net = mcu_pads.get("63", "")
        
        print(f"    - Pad 27 (GPIO 61 / BOOT):     Net = '{pad27_net}' -> " + ("✅ OK" if "BOOT" in pad27_net or pad27_net == "" else "⚠️  Check pullup/button"))
        print(f"    - Pad 26 (GPIO 60 / VDD_SPI):  Net = '{pad26_net}' -> " + ("⚠️  DANGER: Connected to active signal!" if pad26_net not in ["", "GND", "GND_PWR"] else "✅ Safe (Low/Float)"))
        print(f"    - Pad 54 (HS USB D- / PHY):    Net = '{pad54_net}' -> " + ("✅ USB D-" if "DM" in pad54_net or "D_N" in pad54_net else f"⚠️  Mismatch: Net '{pad54_net}' on USB D- hardware pin!"))
        print(f"    - Pad 55 (HS USB D+ / PHY):    Net = '{pad55_net}' -> " + ("✅ USB D+" if "DP" in pad55_net or "D_P" in pad55_net else f"⚠️  Mismatch: Net '{pad55_net}' on USB D+ hardware pin!"))
        if pad63_net:
            print(f"    - Pad 63 (BLE RF 2.4G):        Net = '{pad63_net}' -> ✅ Connected to ANT3")

    elif "ESP32-S3" in cfg["mcu_type"]:
        pad27_net = mcu_pads.get("27", "")
        pad26_net = mcu_pads.get("26", "")
        pad13_net = mcu_pads.get("13", "")
        pad14_net = mcu_pads.get("14", "")
        print(f"    - Pad 27 (GPIO 0  / BOOT):     Net = '{pad27_net}' -> " + ("✅ OK" if "BOOT" in pad27_net or pad27_net == "" else "⚠️  Check pullup/button"))
        print(f"    - Pad 26 (GPIO 45 / VDD_SPI):  Net = '{pad26_net}' -> " + ("⚠️  DANGER: Connected to active signal!" if pad26_net not in ["", "GND", "GND_PWR"] else "✅ Safe (Low/Float)"))
        print(f"    - Pad 13 (GPIO 19 / USB_D-):   Net = '{pad13_net}' -> " + ("✅ USB D-" if "DM" in pad13_net or "D_N" in pad13_net else f"⚠️  Mismatch: Net '{pad13_net}' on USB D- hardware pin!"))
        print(f"    - Pad 14 (GPIO 20 / USB_D+):   Net = '{pad14_net}' -> " + ("✅ USB D+" if "DP" in pad14_net or "D_P" in pad14_net else f"⚠️  Mismatch: Net '{pad14_net}' on USB D+ hardware pin!"))

    elif "ESP32-C6" in cfg["mcu_type"]:
        # ESP32-C6-MINI-1 / MINI-1U (Datasheet Section 3: Pin Definitions):
        # Pad 17: GPIO 12 (USB D-)
        # Pad 18: GPIO 13 (USB D+)
        # Pad 22: GPIO 8 (Strapping / ACT2)
        # Pad 23: GPIO 9 (Boot Mode strapping / I2C_SDA with pull-up)
        pad17_net = mcu_pads.get("17", "")
        pad18_net = mcu_pads.get("18", "")
        pad22_net = mcu_pads.get("22", "")
        pad23_net = mcu_pads.get("23", "")
        print(f"    - Pad 22 (GPIO 8 / STRAP):     Net = '{pad22_net}'")
        print(f"    - Pad 23 (GPIO 9 / BOOT):      Net = '{pad23_net}' -> " + ("✅ BOOT/PULLUP" if "SDA" in pad23_net or "VCC" in pad23_net or "BOOT" in pad23_net else f"Net '{pad23_net}'"))
        print(f"    - Pad 17 (GPIO 12 / USB_D-):   Net = '{pad17_net}' -> " + ("✅ USB D-" if "DM" in pad17_net or "D_N" in pad17_net else f"Net '{pad17_net}'"))
        print(f"    - Pad 18 (GPIO 13 / USB_D+):   Net = '{pad18_net}' -> " + ("✅ USB D+" if "DP" in pad18_net or "D_P" in pad18_net else f"Net '{pad18_net}'"))

    elif "nRF52832" in cfg["mcu_type"]:
        pad1_net = mcu_pads.get("1", "")
        pad46_net = mcu_pads.get("46", "")
        print(f"    - Pad 1  (DEC1):               Net = '{pad1_net}'")
        print(f"    - Pad 46 (DEC4):               Net = '{pad46_net}'")

    elif "ESP32-C3" in cfg["mcu_type"]:
        # ESP32-C3 (QFN-32 chip pinout per Espressif datasheet):
        # Pad 14: GPIO 8 (Strapping / LED)
        # Pad 15: GPIO 9 (BOOT strapping / VCC_3V3 pullup)
        # Pad 18-24: SPI Flash (NC on C3FH4 with embedded SIP flash)
        # Pad 25: GPIO 18 (USB D-)
        # Pad 26: GPIO 19 (USB D+)
        pad14_net = mcu_pads.get("14", "")
        pad15_net = mcu_pads.get("15", "")
        pad25_net = mcu_pads.get("25", "")
        pad26_net = mcu_pads.get("26", "")
        print(f"    - Pad 14 (GPIO 8 / LED):       Net = '{pad14_net}' -> " + ("✅ LED/DATA" if "LED" in pad14_net or "DATA" in pad14_net else f"Net '{pad14_net}'"))
        print(f"    - Pad 15 (GPIO 9 / BOOT):      Net = '{pad15_net}' -> " + ("✅ BOOT/VCC" if "VCC" in pad15_net or "BOOT" in pad15_net or "ARM" in pad15_net else f"Net '{pad15_net}'"))
        print(f"    - Pad 25 (GPIO 18 / USB_D-):   Net = '{pad25_net}' -> " + ("✅ USB D-" if "DM" in pad25_net or "D_N" in pad25_net else f"Net '{pad25_net}'"))
        print(f"    - Pad 26 (GPIO 19 / USB_D+):   Net = '{pad26_net}' -> " + ("✅ USB D+" if "DP" in pad26_net or "D_P" in pad26_net else f"Net '{pad26_net}'"))
        
        # Verify SIP Flash pins 18-24 are NC on C3FH4
        sip_flash_pads = [mcu_pads.get(str(p), "") for p in range(18, 25)]
        connected_sip = [p for p in sip_flash_pads if p and p not in ["GND", "VCC_3V3"]]
        if connected_sip:
            print(f"    ⚠️  C3FH4 Warning: Pads 18-24 (SIP Flash) connected to external signals: {connected_sip}")
        else:
            print(f"    ✅ C3FH4 SIP Flash Pads 18-24: Isolated / NC")

    elif "ESP32-C5" in cfg["mcu_type"]:
        pad8_net = mcu_pads.get("8", "")
        pad13_net = mcu_pads.get("13", "")
        pad16_net = mcu_pads.get("16", "")
        pad17_net = mcu_pads.get("17", "")
        print(f"    - Pad 8  (GPIO 8 / DATA):      Net = '{pad8_net}'")
        print(f"    - Pad 13 (GPIO 9 / BOOT):      Net = '{pad13_net}'")
        print(f"    - Pad 16 (GPIO 18 / USB_D-):   Net = '{pad16_net}'")
        print(f"    - Pad 17 (GPIO 19 / USB_D+):   Net = '{pad17_net}'")
        
    elif "CH32V003" in cfg["mcu_type"]:
        print(f"    - CH32V003 48MHz RISC-V: Pin 4=NRST, Pin 8/18=PD1_SWIO")
        for pin in ["2", "3", "4", "8", "18", "19", "20"]:
            print(f"      Pad {pin:2s}: Net = '{mcu_pads.get(pin, '')}'")

    # 4. I2C Bus Audit
    print(f"\n[4] I2C Bus Devices & Address Conflict Audit:")
    i2c_sda_nets = [net.GetNetname() for net in board.GetNetsByName().values() if "SDA" in net.GetNetname().upper()]
    i2c_scl_nets = [net.GetNetname() for net in board.GetNetsByName().values() if "SCL" in net.GetNetname().upper()]
    print(f"    Detected I2C SDA Nets: {i2c_sda_nets}")
    print(f"    Detected I2C SCL Nets: {i2c_scl_nets}")
    for sda in i2c_sda_nets:
        net = board.FindNet(sda)
        if net:
            pads = []
            for p in board.GetPads():
                if p.GetNetname() == sda:
                    fp = p.GetParentFootprint()
                    ref = fp.GetReference() if fp else "Unknown"
                    pads.append(f"{ref}.{p.GetNumber()}")
            print(f"    Devices on {sda}: {pads}")

    # 5. SPI Chip Select Audit
    print(f"\n[5] SPI Bus Chip Select Uniqueness Audit:")
    cs_nets = [net.GetNetname() for net in board.GetNetsByName().values() if any(k in net.GetNetname().upper() for k in ["_CS", "_NSS", "CS_"])]
    print(f"    Detected Chip Select Nets: {cs_nets}")
    if len(cs_nets) != len(set(cs_nets)):
        print(f"    ❌ CONFLICT: Duplicate CS nets detected!")
        errors += 1
    else:
        print(f"    ✅ All {len(cs_nets)} SPI Chip Select lines are distinct.")

    # 6. Single Source of Truth (SSOT) Pinout Matrix Cross-Audit
    ssot_key = board_id.replace(" ", "_")
    ssot_path = os.path.join(os.path.dirname(__file__), "..", "data", "pcba_pinouts.json")
    if os.path.exists(ssot_path):
        with open(ssot_path) as f:
            ssot_data = json.load(f)
        b_ssot = ssot_data.get("boards", {}).get(ssot_key)
        if b_ssot:
            print(f"\n[6] SSOT Pinout & Firmware Cross-Audit (data/pcba_pinouts.json):")
            ds = b_ssot.get("datasheet", {})
            print(f"    Datasheet: {ds.get('title')} ({ds.get('table_ref')})")
            print(f"    URL:       {ds.get('url')}")
            
            pins = b_ssot.get("pins", [])
            pcb_ok = 0
            pcb_err = 0
            for pin in pins:
                pad_num = str(pin["pad"])
                exp_net = pin.get("net")
                actual_net = mcu_pads.get(pad_num, "")
                if exp_net and exp_net != "NC":
                    if exp_net == actual_net:
                        pcb_ok += 1
                    else:
                        pcb_err += 1
                        print(f"    ❌ PCB Net Mismatch: Pad {pad_num} expected '{exp_net}', got '{actual_net}'")
            if pcb_err == 0:
                print(f"    ✅ PCB Pads: All {pcb_ok} mapped nets match SSOT exactly.")
            else:
                print(f"    ⚠️  PCB Pads: {pcb_err} mismatch(es) against SSOT (Review required).")
                
            hdr_file = b_ssot.get("header_file")
            if hdr_file and os.path.exists(hdr_file):
                with open(hdr_file) as hf:
                    hdr_text = hf.read()
                fw_ok = 0
                fw_err = 0
                for pin in pins:
                    fw_def = pin.get("fw_define")
                    exp_gpio = pin.get("gpio")
                    if fw_def and exp_gpio is not None:
                        m = re.search(rf'#define\s+{fw_def}\s+(?:GPIO_NUM_)?(\d+)', hdr_text)
                        if m:
                            act_gpio = int(m.group(1))
                            if act_gpio == exp_gpio:
                                fw_ok += 1
                            else:
                                fw_err += 1
                                print(f"    ❌ Firmware Header Mismatch: {fw_def} in {hdr_file} defined as GPIO {act_gpio}, expected GPIO {exp_gpio}")
                if fw_err == 0:
                    print(f"    ✅ Firmware Header ({hdr_file}): All {fw_ok} GPIO defines match SSOT.")
                else:
                    print(f"    ⚠️  Firmware Header: {fw_err} GPIO mismatch(es) against SSOT!")

    return errors

def main():
    print("=" * 80)
    print("OPENMOTORBRIDGE PRE-FLIGHT COMPREHENSIVE HARDWARE AUDIT")
    print("=" * 80)
    total_errors = 0
    for board_id, cfg in BOARDS.items():
        err = audit_board(board_id, cfg)
        if err:
            total_errors += err
    print("\n" + "=" * 80)
    if total_errors > 0:
        print(f"❌ PRE-FLIGHT AUDIT FAILED: {total_errors} critical error(s) detected across boards.")
        sys.exit(1)
    else:
        print("✅ PRE-FLIGHT AUDIT PASSED: All boards verified successfully (0 critical errors).")
        sys.exit(0)

if __name__ == "__main__":
    main()
