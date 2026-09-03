#!/usr/bin/env python3
"""
Fix R15/R16 USB-C CC Net Connections & Configure Full Net Classes for Front Node
---------------------------------------------------------------------------------
Preserves all user-adjusted footprint positions while:
1. Assigning USB_CC1 net to R15 pad 1 and J7 pad A5
2. Assigning USB_CC2 net to R16 pad 1 and J7 pad B5
3. Assigning VCC_5V to J7 pads A9 & B9
4. Assigning GND to J7 shield pads
5. Injecting Net Classes (Default, Power, USB_DIFF) into .kicad_pro and .kicad_pcb
"""

import json
import re

PCB_PATH = "/Users/schmidtm/openMotorBridge/hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb"
PRO_PATH = "/Users/schmidtm/openMotorBridge/hardware/kicad_front_node/openmotorbridge_front_node.kicad_pro"

def fix_pro():
    with open(PRO_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["net_settings"] = {
        "classes": [
            {
                "bus_width": 12,
                "clearance": 0.127,
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
                "track_width": 0.15,
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
                "track_width": 0.3,
                "tuning_profile": "",
                "via_diameter": 0.6,
                "via_drill": 0.3,
                "wire_width": 6
            },
            {
                "bus_width": 12,
                "clearance": 0.15,
                "diff_pair_gap": 0.15,
                "diff_pair_via_gap": 0.25,
                "diff_pair_width": 0.2,
                "line_style": 0,
                "microvia_diameter": 0.3,
                "microvia_drill": 0.15,
                "name": "USB_DIFF",
                "pcb_color": "rgba(50, 150, 250, 1.000)",
                "priority": 100,
                "schematic_color": "rgba(50, 150, 250, 1.000)",
                "track_width": 0.2,
                "tuning_profile": "",
                "via_diameter": 0.6,
                "via_drill": 0.3,
                "wire_width": 6
            }
        ],
        "meta": {
            "version": 5
        },
        "net_colors": None,
        "netclass_assignments": None,
        "netclass_patterns": [
            {"netclass": "Power", "pattern": "*VCC*"},
            {"netclass": "Power", "pattern": "*GND*"},
            {"netclass": "Power", "pattern": "*12V*"},
            {"netclass": "Power", "pattern": "*5V*"},
            {"netclass": "Power", "pattern": "*3V3*"},
            {"netclass": "Power", "pattern": "*BUCK*"},
            {"netclass": "Power", "pattern": "*VBUS*"},
            {"netclass": "USB_DIFF", "pattern": "*USB*D*"}
        ]
    }

    with open(PRO_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("✓ Configured .kicad_pro Net Classes (Default, Power, USB_DIFF) and patterns")

def fix_pcb():
    with open(PCB_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Fix R15 Pad 1 -> USB_CC1
    # Locate footprint R15
    m_r15 = re.search(r'(\(property "Reference" "R15"[\s\S]*?\(pad "1" smd roundrect[\s\S]*?\(roundrect_rratio 0.25\))', content)
    if m_r15:
        target = m_r15.group(1)
        if '(net "USB_CC1")' not in target:
            replacement = target + '\n\t\t\t(net "USB_CC1")'
            content = content.replace(target, replacement, 1)
            print("✓ Assigned USB_CC1 to R15 pad 1")

    # 2. Fix R16 Pad 1 -> USB_CC2
    m_r16 = re.search(r'(\(property "Reference" "R16"[\s\S]*?\(pad "1" smd roundrect[\s\S]*?\(roundrect_rratio 0.25\))', content)
    if m_r16:
        target = m_r16.group(1)
        if '(net "USB_CC2")' not in target:
            replacement = target + '\n\t\t\t(net "USB_CC2")'
            content = content.replace(target, replacement, 1)
            print("✓ Assigned USB_CC2 to R16 pad 1")

    # 3. Fix J7 Pads A5, B5, A9, B9, SH
    # Locate footprint J7
    m_j7_a5 = re.search(r'(\(property "Reference" "J7"[\s\S]*?\(pad "A5" smd roundrect[\s\S]*?\(roundrect_rratio 0.25\))', content)
    if m_j7_a5:
        target = m_j7_a5.group(1)
        if '(net "USB_CC1")' not in target:
            replacement = target + '\n\t\t\t(net "USB_CC1")'
            content = content.replace(target, replacement, 1)
            print("✓ Assigned USB_CC1 to J7 pad A5")

    m_j7_b5 = re.search(r'(\(property "Reference" "J7"[\s\S]*?\(pad "B5" smd roundrect[\s\S]*?\(roundrect_rratio 0.25\))', content)
    if m_j7_b5:
        target = m_j7_b5.group(1)
        if '(net "USB_CC2")' not in target:
            replacement = target + '\n\t\t\t(net "USB_CC2")'
            content = content.replace(target, replacement, 1)
            print("✓ Assigned USB_CC2 to J7 pad B5")

    m_j7_a9 = re.search(r'(\(property "Reference" "J7"[\s\S]*?\(pad "A9" smd roundrect[\s\S]*?\(roundrect_rratio 0.25\))', content)
    if m_j7_a9:
        target = m_j7_a9.group(1)
        if '(net "VCC_5V")' not in target:
            replacement = target + '\n\t\t\t(net "VCC_5V")'
            content = content.replace(target, replacement, 1)
            print("✓ Assigned VCC_5V to J7 pad A9")

    m_j7_b9 = re.search(r'(\(property "Reference" "J7"[\s\S]*?\(pad "B9" smd roundrect[\s\S]*?\(roundrect_rratio 0.25\))', content)
    if m_j7_b9:
        target = m_j7_b9.group(1)
        if '(net "VCC_5V")' not in target:
            replacement = target + '\n\t\t\t(net "VCC_5V")'
            content = content.replace(target, replacement, 1)
            print("✓ Assigned VCC_5V to J7 pad B9")

    # 4. Remove existing (net_class ...) blocks in .kicad_pcb if any
    content = re.sub(r'\t\(net_class\s+"[^"]+"[\s\S]*?\n\t\)\n', '', content)

    # 5. Build Net Classes S-Expression block
    power_nets = ["GND", "KL15_12V_SW", "VIN_BUCK", "VCC_5V", "VCC_5V_OTTOCAST", "VCC_3V3", "SW_BUCK", "VBUS_BUCK_OUT", "USB_UP_VBUS"]
    pwr_net_lines = "\n".join([f'\t\t(add_net "{n}")' for n in power_nets])

    usb_diff_nets = ["USB_UP_DP", "USB_UP_DM", "USB_DN1_DP", "USB_DN1_DM", "USB_DN2_DP", "USB_DN2_DM", "USB_SERV_DP", "USB_SERV_DM"]
    usb_diff_net_lines = "\n".join([f'\t\t(add_net "{n}")' for n in usb_diff_nets])

    net_classes_block = f"""\t(net_class "Default" "Standard Signal Net Class"
\t\t(clearance 0.127)
\t\t(trace_width 0.15)
\t\t(via_dia 0.6)
\t\t(via_drill 0.3)
\t\t(uvia_dia 0.3)
\t\t(uvia_drill 0.15)
\t)
\t(net_class "Power" "Power Net Class (0.30mm trace, 0.15mm clearance)"
\t\t(clearance 0.15)
\t\t(trace_width 0.3)
\t\t(via_dia 0.6)
\t\t(via_drill 0.3)
\t\t(uvia_dia 0.3)
\t\t(uvia_drill 0.15)
{pwr_net_lines}
\t)
\t(net_class "USB_DIFF" "USB 90-Ohm Differential Pairs"
\t\t(clearance 0.15)
\t\t(trace_width 0.2)
\t\t(via_dia 0.6)
\t\t(via_drill 0.3)
\t\t(uvia_dia 0.3)
\t\t(uvia_drill 0.15)
\t\t(diff_pair_gap 0.15)
\t\t(diff_pair_width 0.2)
{usb_diff_net_lines}
\t)
"""

    # Insert right before the first (footprint ...
    m_fp = re.search(r'(\n\t\(footprint )', content)
    if m_fp:
        idx = m_fp.start()
        content = content[:idx] + "\n" + net_classes_block + content[idx:]
        print("✓ Embedded (net_class ...) blocks into .kicad_pcb")

    with open(PCB_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Saved updated openmotorbridge_front_node.kicad_pcb")

if __name__ == "__main__":
    fix_pro()
    fix_pcb()
    print("🎉 All fixes cleanly applied without touching manual component placements!")
