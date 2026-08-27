#!/usr/bin/env python3
"""
Setup complete Net Classes in .kicad_pro and .kicad_pcb files
-------------------------------------------------------------
Configures 'Default' (Signal) and 'Power' Net Classes with JLCPCB standard rules:
- Signal: 0.15 mm / 0.20 mm trace, 0.60/0.30 mm via
- Power: 0.25 mm / 0.30 mm trace, 0.60/0.30 mm via
- Pattern matching for automatic assignment (*VCC*, *GND*, *PWR*, *3V3*, *5V*, *KL30*, *VBAT*)
- (net_class ...) blocks embedded directly in .kicad_pcb
"""

import os
import json
import re

BOARDS = [
    {
        "name": "Main Board",
        "pro": "hardware/kicad_main_box/openmotorbridge_main.kicad_pro",
        "pcb": "hardware/kicad_main_box/openmotorbridge_main.kicad_pcb",
        "sig_w": 0.15,
        "pwr_w": 0.30,
        "pwr_nets": ["KL30_IN", "VCC_5V", "VCC_3V3", "GND_PWR", "SW_BUCK", "VBAT", "SYS_PWR", "POD1_VCC", "POD2_VCC", "VBUS_IN"]
    },
    {
        "name": "Pod Base",
        "pro": "hardware/kicad_pod_base/openmotorbridge_pod_base.kicad_pro",
        "pcb": "hardware/kicad_pod_base/openmotorbridge_pod_base.kicad_pcb",
        "sig_w": 0.20,
        "pwr_w": 0.30,
        "pwr_nets": ["VCC", "GND", "GND_SHIELD"]
    },
    {
        "name": "Pod Cartridge",
        "pro": "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pro",
        "pcb": "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb",
        "sig_w": 0.20,
        "pwr_w": 0.30,
        "pwr_nets": ["VCC_5V_PROT", "GND", "NET_LED_R", "NET_LED_G"]
    },
    {
        "name": "Rear Pod 3",
        "pro": "hardware/kicad_rear_pod3/openmotorbridge_rear_pod3.kicad_pro",
        "pcb": "hardware/kicad_rear_pod3/openmotorbridge_rear_pod3.kicad_pcb",
        "sig_w": 0.15,
        "pwr_w": 0.25,
        "pwr_nets": ["VCC_3V3", "GND", "VBUS"]
    }
]

def update_pro(item):
    pro_path = item["pro"]
    with open(pro_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    ns = data.setdefault("net_settings", {})
    ns["classes"] = [
        {
            "bus_width": 12,
            "clearance": 0.127 if item["sig_w"] == 0.15 else 0.15,
            "diff_pair_gap": 0.25,
            "diff_pair_via_gap": 0.25,
            "diff_pair_width": 0.2,
            "line_style": 0,
            "microvia_diameter": 0.3,
            "microvia_drill": 0.15,
            "name": "Default",
            "pcb_color": "rgba(0, 0, 0, 0.000)",
            "priority": 2147483647,
            "schematic_color": "rgba(0, 0, 0, 0.000)",
            "track_width": item["sig_w"],
            "tuning_profile": "",
            "via_diameter": 0.6,
            "via_drill": 0.3,
            "wire_width": 6
        },
        {
            "bus_width": 12,
            "clearance": 0.15,
            "diff_pair_gap": 0.25,
            "diff_pair_via_gap": 0.25,
            "diff_pair_width": 0.2,
            "line_style": 0,
            "microvia_diameter": 0.3,
            "microvia_drill": 0.15,
            "name": "Power",
            "pcb_color": "rgba(200, 50, 50, 1.000)",
            "priority": 100,
            "schematic_color": "rgba(200, 50, 50, 1.000)",
            "track_width": item["pwr_w"],
            "tuning_profile": "",
            "via_diameter": 0.6,
            "via_drill": 0.3,
            "wire_width": 6
        }
    ]
    
    ns["netclass_patterns"] = [
        {"netclass": "Power", "pattern": "*VCC*"},
        {"netclass": "Power", "pattern": "*GND*"},
        {"netclass": "Power", "pattern": "*PWR*"},
        {"netclass": "Power", "pattern": "*KL30*"},
        {"netclass": "Power", "pattern": "*VBAT*"},
        {"netclass": "Power", "pattern": "*3V3*"},
        {"netclass": "Power", "pattern": "*5V*"},
        {"netclass": "Power", "pattern": "*VBUS*"},
        {"netclass": "Power", "pattern": "*BUCK*"}
    ]
    
    with open(pro_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"✓ Configured .kicad_pro net classes for {item['name']}")

def update_pcb(item):
    pcb_path = item["pcb"]
    with open(pcb_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Remove existing (net_class ...) blocks
    content = re.sub(r'\t\(net_class\s+"[^"]+"[\s\S]*?\n\t\)\n', '', content)
    
    # Generate net_class S-expressions
    pwr_net_lines = "\n".join([f'\t\t(add_net "{n}")' for n in item["pwr_nets"]])
    
    net_class_block = f"""\t(net_class "Default" "Standard Signal Net Class"
\t\t(clearance {0.127 if item["sig_w"] == 0.15 else 0.15})
\t\t(trace_width {item["sig_w"]})
\t\t(via_dia 0.6)
\t\t(via_drill 0.3)
\t\t(uvia_dia 0.3)
\t\t(uvia_drill 0.15)
\t)
\t(net_class "Power" "Power Net Class"
\t\t(clearance 0.15)
\t\t(trace_width {item["pwr_w"]})
\t\t(via_dia 0.6)
\t\t(via_drill 0.3)
\t\t(uvia_dia 0.3)
\t\t(uvia_drill 0.15)
{pwr_net_lines}
\t)
"""
    # Insert before the last closing parenthesis
    idx = content.rfind(')')
    if idx != -1:
        content = content[:idx] + net_class_block + content[idx:]
        
    with open(pcb_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Injected (net_class ...) into {item['name']} (.kicad_pcb)")

def main():
    for item in BOARDS:
        update_pro(item)
        update_pcb(item)
    print("\n🎉 All 4 KiCad projects & PCB files now have explicit 'Default' and 'Power' Net Classes!")

if __name__ == '__main__':
    main()
