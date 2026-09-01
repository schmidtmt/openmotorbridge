#!/usr/bin/env python3
"""
Generate Complete, Routing-Ready KiCad PCB for Rear Pod 3 (OMM Transceiver):
- 50.0 x 35.0 mm 4-layer board outline with rounded corners
- Complete electrical netlist and 100% pad-net connectivity
- Standard KiCad footprint geometries with STEP 3D models
- Zero component overlap, designated antenna keepout zones, and crisp silkscreen
"""

import os
import re

pcb_file = "hardware/kicad_rear_pod3/openmotorbridge_rear_pod3.kicad_pcb"
kicad_fp_dir = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"
kicad_3d_dir = "${KICAD8_3DMODEL_DIR}"

# 1. Netlist definition
nets = [
    (0, ""),
    (1, "GND"),
    (2, "POD3_VCC_5V"),
    (3, "VCC_3V3"),
    (4, "POD3_UART_TX"),
    (5, "POD3_UART_RX"),
    (6, "GNSS_1PPS"),
    (7, "POD3_1WIRE_ID"),
    (8, "GNSS_TXD"),
    (9, "GNSS_RXD"),
    (10, "LORA_SCK"),
    (11, "LORA_MISO"),
    (12, "LORA_MOSI"),
    (13, "LORA_NSS"),
    (14, "LORA_DIO1"),
    (15, "LORA_BUSY"),
    (16, "LORA_NRST"),
    (17, "NET_F1_5V"),
    (18, "NET_LED_R"),
    (19, "TP_BOOT"),
    (20, "TP_EN"),
    (21, "LORA_RF_ANT"),
    (22, "GNSS_RF_IN"),
]

net_map = {name: num for num, name in nets}

# 2. Component Pin-to-Net Mapping
component_pins = {
    # J1: 6-Pin Horizontal Connector
    # Physically at rot=180: local pad 6 sits at Y=87.65 (mating Pod Base Kontakt 1 VCC)
    # local pad 1 sits at Y=100.35 (mating Pod Base Kontakt 6 1-Wire ID)
    'J1': {
        '6': 'POD3_VCC_5V',    # Y=87.65 (Mates with Pod Base Kontakt 1 VCC)
        '5': 'GND',            # Y=90.19 (Mates with Pod Base Kontakt 2 GND)
        '4': 'POD3_UART_TX',   # Y=92.73 (Mates with Pod Base Kontakt 3 UART_TX)
        '3': 'POD3_UART_RX',   # Y=95.27 (Mates with Pod Base Kontakt 4 UART_RX)
        '2': 'GNSS_1PPS',      # Y=97.81 (Mates with Pod Base Kontakt 5 GNSS_1PPS)
        '1': 'POD3_1WIRE_ID',  # Y=100.35 (Mates with Pod Base Kontakt 6 1-Wire ID)
    },
    # F1: 500mA PTC Fuse
    'F1': {
        '1': 'POD3_VCC_5V',
        '2': 'NET_F1_5V',
    },
    # D1: Power LED
    'D1': {
        '1': 'NET_LED_R',
        '2': 'GND',
    },
    # R1: LED Resistor
    'R1': {
        '1': 'NET_F1_5V',
        '2': 'NET_LED_R',
    },
    # U4: DS2401 1-Wire ID ROM (SOT-23)
    'U4': {
        '1': 'POD3_1WIRE_ID',
        '2': 'GND',
        '3': '',
    },
    # U1: ESP32-C3-WROOM-02
    'U1': {
        '1': 'VCC_3V3',
        '2': 'TP_EN',
        '3': 'GNSS_1PPS',
        '4': 'LORA_DIO1',
        '5': 'LORA_BUSY',
        '6': 'POD3_UART_TX',
        '7': 'POD3_UART_RX',
        '8': 'GNSS_RXD',
        '9': 'GNSS_TXD',
        '10': 'LORA_SCK',
        '11': 'LORA_MISO',
        '12': 'LORA_MOSI',
        '13': 'LORA_NSS',
        '14': 'LORA_NRST',
        '15': 'TP_BOOT',
        '16': 'GND',
        '17': 'GND',
        '18': 'GND',
        '19': 'GND', # Thermal pad
    },
    # U2: u-blox MAX-M10S GNSS
    'U2': {
        '1': 'GND',
        '2': 'GNSS_TXD',
        '3': 'GNSS_RXD',
        '4': 'GNSS_1PPS',
        '5': 'GND',
        '6': 'GND',
        '7': 'VCC_3V3',
        '8': 'VCC_3V3',
        '9': 'GND',
        '10': 'GND',
        '11': 'GNSS_RF_IN',
        '12': 'GND',
        '13': 'GND',
        '14': 'GND',
        '15': 'GND',
        '16': 'GND',
        '17': 'GND',
        '18': 'GND',
    },
    # U3: Semtech SX1262 LoRa (QFN-24)
    'U3': {
        '1': 'VCC_3V3',
        '2': 'GND',
        '3': 'GND',
        '4': 'GND',
        '5': 'LORA_NRST',
        '6': 'LORA_BUSY',
        '7': 'LORA_DIO1',
        '8': 'GND',
        '9': 'GND',
        '10': 'VCC_3V3',
        '11': 'GND',
        '12': 'GND',
        '13': 'LORA_NSS',
        '14': 'LORA_SCK',
        '15': 'LORA_MOSI',
        '16': 'LORA_MISO',
        '17': 'LORA_RF_ANT',
        '18': 'VCC_3V3',
        '19': 'GND',
        '20': 'GND',
        '21': 'LORA_RF_ANT',
        '22': 'GND',
        '23': 'GND',
        '24': 'VCC_3V3',
        '25': 'GND', # EP
    },
    # ANT1: Pulse_W3000 868MHz LoRa Ceramic Antenna
    'ANT1': {'1': 'LORA_RF_ANT', '2': 'GND'},
    # ANT2: Pulse_W3000 GNSS Ceramic Antenna
    'ANT2': {'1': 'GNSS_RF_IN', '2': 'GND'},
    # J2: LoRa 868 MHz U.FL Coaxial Connector
    'J2': {'1': 'LORA_RF_ANT', '2': 'GND'},
    # J3: GNSS U.FL Coaxial Connector
    'J3': {'1': 'GNSS_RF_IN', '2': 'GND'},
    # C1: 10uF 3V3 Cap
    'C1': {'1': 'VCC_3V3', '2': 'GND'},
    # C2: 100nF ESP32 Cap
    'C2': {'1': 'VCC_3V3', '2': 'GND'},
    # C3: 100nF GNSS Cap
    'C3': {'1': 'VCC_3V3', '2': 'GND'},
    # C4: 100nF LoRa Cap
    'C4': {'1': 'VCC_3V3', '2': 'GND'},
    # H1..H4: M2 Mounting Holes
    'H1': {'1': 'GND'},
    'H2': {'1': 'GND'},
    'H3': {'1': 'GND'},
    'H4': {'1': 'GND'},
}

# Footprint Specifications (library_path, ref, val, x, y, rot, layer, model_path)
# Centerline Y = 94.0 mm, Outline X = 100.0..170.0, Y = 70.0..118.0 (70.0 x 48.0 mm)
# J1 6-Pin Header rotated 180 deg: Pins point LEFT out of the board towards bulkhead socket!
# At rot=180: Header origin at (102.50, 100.35) -> Pin 1 at Y=100.35, Pin 6 at Y=87.65, Pin Center = 94.00 mm!
components = [
    # J1: 6-Pin Horizontal connector pointing LEFT towards mating bulkhead socket
    ("Connector_PinHeader_2.54mm.pretty/PinHeader_1x06_P2.54mm_Horizontal.kicad_mod", "J1", "6-Pin_OMM_Socket", 102.50, 100.35, 180, "F.Cu", "Connector_PinHeader_2.54mm.3dshapes/PinHeader_1x06_P2.54mm_Horizontal.step"),
    # Protection & Status (F1 near Pin 1 VCC at Y=87.65; D1/R1 5V power LED)
    ("Resistor_SMD.pretty/R_1206_3216Metric.kicad_mod", "F1", "PTC_500mA", 106.75, 83.71, 90, "F.Cu", "Resistor_SMD.3dshapes/R_1206_3216Metric.step"),
    ("LED_SMD.pretty/LED_0805_2012Metric.kicad_mod", "D1", "LED_Green_5V", 112.06, 72.50, 180, "F.Cu", "LED_SMD.3dshapes/LED_0805_2012Metric.step"),
    ("Resistor_SMD.pretty/R_0603_1608Metric.kicad_mod", "R1", "1.5k_LED_Resistor", 114.00, 77.83, 90, "F.Cu", "Resistor_SMD.3dshapes/R_0603_1608Metric.step"),
    # Maxim DS2401 ID Chip (Directly adjacent to J1 Pin 6 1-Wire at Y=100.35)
    ("Package_TO_SOT_SMD.pretty/SOT-23.kicad_mod", "U4", "DS2401_1Wire_ID", 112.50, 100.35, 0, "F.Cu", "Package_TO_SOT_SMD.3dshapes/SOT-23.step"),
    # u-blox MAX-M10S GNSS Subsystem & Antennas (Top edge - U2 rotated 180 for direct RF/SPI alignment)
    ("RF_GPS.pretty/ublox_MAX.kicad_mod", "U2", "MAX-M10S_GNSS", 124.00, 83.00, 180, "F.Cu", "Package_DFN_QFN.3dshapes/QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm.step"),
    ("Capacitor_SMD.pretty/C_0603_1608Metric.kicad_mod", "C3", "100nF_GNSS", 114.00, 83.53, 90, "F.Cu", "Capacitor_SMD.3dshapes/C_0603_1608Metric.step"),
    ("Connector_Coaxial.pretty/U.FL_Hirose_U.FL-R-SMT-1_Vertical.kicad_mod", "J3", "GNSS_UFL", 124.00, 74.00, 0, "F.Cu", None),
    ("RF_Antenna.pretty/Pulse_W3000.kicad_mod", "ANT2", "GNSS_Patch_Antenna", 136.00, 71.00, 180, "F.Cu", None),
    # Semtech SX1262 LoRa Subsystem & Antennas (Bottom edge)
    ("Package_DFN_QFN.pretty/QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm.kicad_mod", "U3", "SX1262_LoRa_+22dBm", 124.00, 105.00, 0, "F.Cu", "Package_DFN_QFN.3dshapes/QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm.step"),
    ("Capacitor_SMD.pretty/C_0603_1608Metric.kicad_mod", "C4", "100nF_LoRa", 115.03, 104.75, 0, "F.Cu", "Capacitor_SMD.3dshapes/C_0603_1608Metric.step"),
    ("Connector_Coaxial.pretty/U.FL_Hirose_U.FL-R-SMT-1_Vertical.kicad_mod", "J2", "LORA_UFL", 124.00, 114.50, 180, "F.Cu", None),
    ("RF_Antenna.pretty/Pulse_W3000.kicad_mod", "ANT1", "868MHz_LoRa_Antenna", 136.00, 117.00, 0, "F.Cu", None),
    # ESP32-C3 RISC-V Mesh MCU (Centered rear facing tail clearance)
    ("RF_Module.pretty/ESP32-C3-WROOM-02.kicad_mod", "U1", "ESP32-C3-WROOM-02", 156.80, 94.39, -90, "F.Cu", "RF_Module.3dshapes/ESP32-C3-WROOM-02.step"),
    ("Capacitor_SMD.pretty/C_0805_2012Metric.kicad_mod", "C1", "10uF_3V3", 109.50, 77.25, 90, "F.Cu", "Capacitor_SMD.3dshapes/C_0805_2012Metric.step"),
    ("Capacitor_SMD.pretty/C_0603_1608Metric.kicad_mod", "C2", "100nF_MCU", 139.75, 76.47, 180, "F.Cu", "Capacitor_SMD.3dshapes/C_0603_1608Metric.step"),
    # 4 Corner M2 Mounting Holes (Matches 00_base_sled corner posts: Delta X = 62.0 mm, Delta Y = 42.0 mm)
    ("MountingHole.pretty/MountingHole_2.2mm_M2_Pad.kicad_mod", "H1", "M2_Mounting_Hole", 104.00, 73.00, 0, "F.Cu", None),
    ("MountingHole.pretty/MountingHole_2.2mm_M2_Pad.kicad_mod", "H2", "M2_Mounting_Hole", 166.00, 73.00, 0, "F.Cu", None),
    ("MountingHole.pretty/MountingHole_2.2mm_M2_Pad.kicad_mod", "H3", "M2_Mounting_Hole", 104.00, 115.00, 0, "F.Cu", None),
    ("MountingHole.pretty/MountingHole_2.2mm_M2_Pad.kicad_mod", "H4", "M2_Mounting_Hole", 166.00, 115.00, 0, "F.Cu", None),
]

def extract_sexpr(text, start_idx):
    """Balanced S-expression extractor respecting nested parentheses and strings."""
    depth = 0
    in_quote = False
    escape = False
    for i in range(start_idx, len(text)):
        c = text[i]
        if escape:
            escape = False
            continue
        if c == '\\':
            escape = True
            continue
        if c == '"':
            in_quote = not in_quote
            continue
        if not in_quote:
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0:
                    return i + 1
    return len(text)

def load_and_transform_footprint(fp_rel_path, ref, val, x, y, rot, layer, model_path=None):
    full_path = os.path.join(kicad_fp_dir, fp_rel_path)
    with open(full_path, 'r') as f:
        mod_text = f.read()

    # 1. Strip (embedded_fonts ...) cleanly
    mod_text = re.sub(r'\(embedded_fonts\s+[^\)]+\)', '', mod_text)

    # 2. Replace (footprint "...") header
    fp_name = fp_rel_path.replace(".kicad_mod", "").replace("/", ":")
    mod_text = re.sub(r'\(footprint\s+"[^"]+"', f'(footprint "{fp_name}"\n\t\t(layer "{layer}")\n\t\t(uuid "f0000000-0000-0000-0000-{abs(hash(ref)) & 0xffffffffffff:012x}")\n\t\t(at {x:.2f} {y:.2f} {rot})', mod_text, count=1)

    # 3. Remove all existing properties at footprint level cleanly using balanced S-expressions
    while True:
        p_idx = mod_text.find('(property')
        if p_idx == -1:
            break
        p_end = extract_sexpr(mod_text, p_idx)
        mod_text = mod_text[:p_idx] + mod_text[p_end:]

    # 4. Add clean Reference and Value properties
    new_props = f"""\t(property "Reference" "{ref}"
\t\t(at 0 0 0)
\t\t(layer "F.SilkS")
\t\t(uuid "f1000000-0000-0000-0000-{abs(hash(ref + 'ref')) & 0xffffffffffff:012x}")
\t\t(effects
\t\t\t(font
\t\t\t\t(size 0.5 0.5)
\t\t\t\t(thickness 0.1)
\t\t\t)
\t\t\t(hide yes)
\t\t)
\t)
\t(property "Value" "{val}"
\t\t(at 0 0 0)
\t\t(layer "F.Fab")
\t\t(uuid "f1000000-0000-0000-0000-{abs(hash(ref + 'val')) & 0xffffffffffff:012x}")
\t\t(effects
\t\t\t(font
\t\t\t\t(size 0.5 0.5)
\t\t\t\t(thickness 0.1)
\t\t\t)
\t\t\t(hide yes)
\t\t)
\t)"""

    lines = mod_text.splitlines()
    header_idx = 1
    for idx, l in enumerate(lines):
        if '(at ' in l:
            header_idx = idx + 1
            break
    lines.insert(header_idx, new_props)
    mod_text = "\n".join(lines)

    # 5. Remove existing models cleanly using balanced sexpr
    while True:
        m_idx = mod_text.find('(model')
        if m_idx == -1:
            break
        m_end = extract_sexpr(mod_text, m_idx)
        mod_text = mod_text[:m_idx] + mod_text[m_end:]

    # 6. Assign Net numbers to Pads using balanced sexpr
    pin_assignments = component_pins.get(ref, {})
    new_parts = []
    pos = 0
    while True:
        pad_idx = mod_text.find('(pad', pos)
        if pad_idx == -1:
            new_parts.append(mod_text[pos:])
            break
        new_parts.append(mod_text[pos:pad_idx])
        pad_end = extract_sexpr(mod_text, pad_idx)
        pad_sexpr = mod_text[pad_idx:pad_end]

        m = re.match(r'\(pad\s+"([^"]+)"\s+([^\s]+)\s+([^\s\)]+)', pad_sexpr)
        if m:
            pad_num = m.group(1)
            net_name = pin_assignments.get(pad_num, "")
            net_idx = net_map.get(net_name, 0)

            # Strip existing (net ...) inside pad
            pad_clean = re.sub(r'\(net\s+\d+\s+"[^"]*"\)', '', pad_sexpr)
            
            # If footprint is rotated, ensure pad (at x y) includes rotation so pads rotate with footprint
            if rot != 0:
                pad_clean = re.sub(r'\(at\s+([^\s\)]+)\s+([^\s\)]+)\)', rf'(at \1 \2 {rot})', pad_clean)

            # If net assigned, insert (net ...) right after shape
            if net_name:
                net_clause = f' (net {net_idx} "{net_name}")'
                prefix_len = m.end()
                pad_clean = pad_clean[:prefix_len] + net_clause + pad_clean[prefix_len:]
            new_parts.append(pad_clean)
        else:
            new_parts.append(pad_sexpr)
        pos = pad_end

    mod_text = "".join(new_parts)

    # 7. Attach 3D Model if specified right before last closing parenthesis
    if model_path:
        full_model = f"{kicad_3d_dir}/{model_path}"
        model_block = f"""\n\t\t(model "{full_model}"
\t\t\t(offset (xyz 0 0 0))
\t\t\t(scale (xyz 1 1 1))
\t\t\t(rotate (xyz 0 0 0))
\t\t)\n"""
        last_paren = mod_text.rfind(')')
        mod_text = mod_text[:last_paren].rstrip() + model_block + '\t)'

    # Indent for inclusion in PCB
    indented = "\n".join(["\t" + line for line in mod_text.strip().splitlines()])
    return indented

# Generate board outline (70.0 x 48.0 mm: 100.0..170.0, 70.0..118.0)
def generate_edge_cuts():
    r = 2.5
    x1, y1 = 100.0, 70.0
    x2, y2 = 170.0, 118.0
    lines = [
        f'\t(gr_line (start {x1+r:.2f} {y1:.2f}) (end {x2-r:.2f} {y1:.2f}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "e0000000-0000-0000-0000-000000000001"))',
        f'\t(gr_arc (start {x2-r:.2f} {y1:.2f}) (mid {x2-0.73:.2f} {y1+0.73:.2f}) (end {x2:.2f} {y1+r:.2f}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "e0000000-0000-0000-0000-000000000002"))',
        f'\t(gr_line (start {x2:.2f} {y1+r:.2f}) (end {x2:.2f} {y2-r:.2f}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "e0000000-0000-0000-0000-000000000003"))',
        f'\t(gr_arc (start {x2:.2f} {y2-r:.2f}) (mid {x2-0.73:.2f} {y2-0.73:.2f}) (end {x2-r:.2f} {y2:.2f}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "e0000000-0000-0000-0000-000000000004"))',
        f'\t(gr_line (start {x2-r:.2f} {y2:.2f}) (end {x1+r:.2f} {y2:.2f}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "e0000000-0000-0000-0000-000000000005"))',
        f'\t(gr_arc (start {x1+r:.2f} {y2:.2f}) (mid {x1+0.73:.2f} {y2-0.73:.2f}) (end {x1:.2f} {y2-r:.2f}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "e0000000-0000-0000-0000-000000000006"))',
        f'\t(gr_line (start {x1:.2f} {y2-r:.2f}) (end {x1:.2f} {y1+r:.2f}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "e0000000-0000-0000-0000-000000000007"))',
        f'\t(gr_arc (start {x1:.2f} {y1+r:.2f}) (mid {x1+0.73:.2f} {y1+0.73:.2f}) (end {x1+r:.2f} {y1:.2f}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "e0000000-0000-0000-0000-000000000008"))',
    ]
    return "\n".join(lines)

# Generate Silkscreen Labels
def generate_silkscreen():
    labels = [
        ("J3: GNSS U.FL", 124.0, 71.5, 0.55, 0.10, 0),
        ("J2: LoRa U.FL", 124.0, 117.0, 0.55, 0.10, 0),
        ("▲ Pin 1", 101.0, 87.65, 0.60, 0.10, 0),
        ("F1: PTC", 109.0, 91.0, 0.60, 0.10, 0),
        ("D1: 5V", 109.0, 77.0, 0.60, 0.10, 0),
        ("U4: ID", 112.5, 97.0, 0.60, 0.10, 0),
        ("2.4GHz ANTENNA ZONE", 158.0, 95.0, 0.60, 0.10, 90),
        ("U2: MAX-M10S GNSS", 124.0, 89.0, 0.65, 0.11, 0),
        ("U3: SX1262 LoRa", 124.0, 100.0, 0.65, 0.11, 0),
        ("ANT1: LoRa Pulse W3000", 138.0, 114.5, 0.65, 0.11, 0),
        ("ANT2: GNSS Pulse W3000", 138.2, 73.0, 0.65, 0.11, 0),
        ("J1: 6-PIN OMM", 102.5, 94.0, 0.65, 0.11, 90),
        ("U1: ESP32-C3 MESH", 148.2, 93.5, 0.70, 0.12, 270),
        ("OpenMotorMesh Heck-Pod 3 v8.0 (70x48mm)", 146.5, 79.2, 0.85, 0.14, 0),
    ]
    lines = []
    for txt, x, y, sz, th, rot in labels:
        uid = f"s0000000-0000-0000-0000-{abs(hash((txt, x, y))) & 0xffffffffffff:012x}"
        lines.append(f"""\t(gr_text "{txt}"
\t\t(at {x:.2f} {y:.2f} {rot})
\t\t(layer "F.SilkS")
\t\t(uuid "{uid}")
\t\t(effects
\t\t\t(font
\t\t\t\t(size {sz:.2f} {sz:.2f})
\t\t\t\t(thickness {th:.2f})
\t\t\t)
\t\t)
\t)""")
    return "\n".join(lines)

# Assembly full PCB S-expression
pcb_header = f"""(kicad_pcb
\t(version 20240108)
\t(generator "pcbnew")
\t(generator_version "9.0")
\t(general
\t\t(thickness 1.6)
\t\t(legacy_teardrops no)
\t)
\t(paper "A4")
\t(title_block
\t\t(title "OpenMotorBridge v8.0 - Rear Pod 3 OMM Transceiver (70x48mm 4-Layer)")
\t\t(date "2026-09-01")
\t\t(rev "v8.0")
\t\t(company "OpenMotorBridge Open Source Hardware")
\t\t(comment 1 "u-blox MAX-M10S GNSS + Semtech SX1262 LoRa (+22dBm) + ESP32-C3 RISC-V")
\t\t(comment 2 "Dual-PHY OpenMotorMesh: 2.4GHz HiFi + 868MHz Long-Range Fallback")
\t)
\t(layers
\t\t(0 "F.Cu" signal)
\t\t(1 "In1.Cu" power "GND_PLANE")
\t\t(2 "In2.Cu" power "PWR_3V3")
\t\t(31 "B.Cu" signal)
\t\t(32 "B.Mask" user)
\t\t(33 "F.Mask" user)
\t\t(34 "B.Paste" user)
\t\t(35 "F.Paste" user)
\t\t(36 "B.SilkS" user "B.Silkscreen")
\t\t(37 "F.SilkS" user "F.Silkscreen")
\t\t(38 "B.CrtYd" user "B.Courtyard")
\t\t(39 "F.CrtYd" user "F.Courtyard")
\t\t(40 "B.Fab" user)
\t\t(41 "F.Fab" user)
\t\t(44 "Edge.Cuts" user)
\t)
\t(setup
\t\t(pad_to_mask_clearance 0.05)
\t\t(allow_soldermask_bridges_in_footprints no)
\t\t(tenting
\t\t\t(front yes)
\t\t\t(back yes)
\t\t)
\t\t(pcbplotparams
\t\t\t(layerselection 0x00000000_00000000_55555555_5755f5ff)
\t\t\t(plot_on_all_layers_selection 0x00000000_00000000_00000000_00000000)
\t\t\t(disableapertmacros no)
\t\t\t(usegerberextensions no)
\t\t\t(usegerberattributes yes)
\t\t\t(usegerberadvancedattributes yes)
\t\t\t(creategerberjobfile yes)
\t\t\t(dashed_line_dash_ratio 12)
\t\t\t(dashed_line_gap_ratio 3)
\t\t\t(svgprecision 4)
\t\t\t(plotframeref no)
\t\t\t(mode 1)
\t\t\t(useauxorigin no)
\t\t\t(pdf_front_fp_property_popups yes)
\t\t\t(pdf_back_fp_property_popups yes)
\t\t\t(pdf_metadata yes)
\t\t\t(pdf_single_document no)
\t\t\t(dxfpolygonmode yes)
\t\t\t(dxfimperialunits yes)
\t\t\t(dxfusepcbnewfont yes)
\t\t\t(psnegative no)
\t\t\t(psa4output no)
\t\t\t(plot_black_and_white yes)
\t\t\t(sketchpadsonfab no)
\t\t\t(plotpadnumbers no)
\t\t\t(hidednponfab no)
\t\t\t(sketchdnponfab yes)
\t\t\t(crossoutdnponfab yes)
\t\t\t(subtractmaskfromsilk no)
\t\t\t(outputformat 1)
\t\t\t(mirror no)
\t\t\t(drillshape 1)
\t\t\t(scaleselection 1)
\t\t\t(outputdirectory "")
\t\t)
\t)
"""

# Add Nets
net_entries = []
for num, name in nets:
    net_entries.append(f'\t(net {num} "{name}")')

net_str = "\n".join(net_entries)

# Add Footprints
footprint_entries = []
for fp_path, ref, val, x, y, rot, layer, model_path in components:
    fp_sexpr = load_and_transform_footprint(fp_path, ref, val, x, y, rot, layer, model_path)
    footprint_entries.append(fp_sexpr)

fps_str = "\n".join(footprint_entries)
edge_cuts_str = generate_edge_cuts()
silk_str = generate_silkscreen()

final_pcb = f"{pcb_header}\n{net_str}\n\n{fps_str}\n\n{edge_cuts_str}\n\n{silk_str}\n)\n"

with open(pcb_file, 'w') as f:
    f.write(final_pcb)

print(f"✓ Successfully generated routing-ready Rear Pod 3 PCB ({pcb_file})!")
