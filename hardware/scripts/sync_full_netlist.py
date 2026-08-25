#!/usr/bin/env python3
"""
Netlist Synchronizer & Complete Net Injector (Fixed KiCad 9 Pad S-Expr Parser):
Places (net <code_id> "<net_name>") as a direct child element of (pad ...).
"""

import os
import re

pcb_file = 'hardware/kicad_main_box/openmotorbridge_main.kicad_pcb'

# Restore from backup first to get clean baseline
with open('hardware/kicad_main_box/openmotorbridge_main_placement_v8_backup.kicad_pcb', 'r') as f:
    pcb_text = f.read()

NETS = {
    0: "",
    1: "GND_PWR",
    2: "VCC_3V3",
    3: "VCC_5V",
    4: "KL30_IN",
    5: "KL15_IGN",
    6: "SW_BUCK",
    7: "BST_BUCK",
    8: "VCC_BUCK",
    9: "EN_BUCK",
    10: "BAT_PLUS",
    11: "NTC_JEITA",
    12: "USB_D_N",
    13: "USB_D_P",
    14: "UART_TXD0",
    15: "UART_RXD0",
    16: "ESP_EN",
    17: "ESP_BOOT",
    18: "I2S_MCLK",
    19: "I2S_BCLK",
    20: "I2S_WS",
    21: "I2S_DOUT",
    22: "I2S_DIN",
    23: "I2C_SDA",
    24: "I2C_SCL",
    25: "CAN_TX",
    26: "CAN_RX",
    27: "CAN_H",
    28: "CAN_L",
    29: "SD_CLK",
    30: "SD_CMD",
    31: "SD_DAT0",
    32: "SD_DAT1",
    33: "SD_DAT2",
    34: "SD_DAT3",
    35: "AUDIO_OUT_P",
    36: "AUDIO_OUT_N",
    37: "AUDIO_IN_P",
    38: "AUDIO_IN_N",
    39: "POD1_VCC",
    40: "POD1_NF_P",
    41: "POD1_NF_N",
    42: "POD1_OPTO_KEY",
    43: "POD1_OPTO_RET",
    44: "POD2_VCC",
    45: "POD2_NF_P",
    46: "POD2_NF_N",
    47: "POD2_OPTO_KEY",
    48: "POD2_OPTO_RET",
    49: "POD3_VCC",
    50: "POD3_UART_TX",
    51: "POD3_UART_RX",
    52: "POD3_GNSS_PPS",
    53: "ONEWIRE_ID",
    54: "GND_SHIELD",
    55: "AGND",
    56: "RESERVE_GPIO_A",
    57: "RESERVE_GPIO_B",
    58: "STATUS_LED_MCU",
    59: "STATUS_LED_EXT",
    60: "PORT1_KEY_MCU",
    61: "PORT2_KEY_MCU",
    62: "PORT1_VCC_EN",
    63: "PORT2_VCC_EN",
    64: "ADC_BAT",
    65: "ADC_LINE_LVL",
    66: "ADC_VIGN",
}

NET_NAME_TO_ID = {name: code for code, name in NETS.items()}

PAD_NET_MAP = {
    # Power Stage
    ('U1', '1'): 'KL30_IN',
    ('U1', '2'): 'EN_BUCK',
    ('U1', '3'): 'KL30_IN',
    ('U1', '4'): 'GND_PWR',
    ('U1', '5'): 'VCC_5V',
    ('U1', '6'): 'VCC_BUCK',
    ('U1', '7'): 'BST_BUCK',
    ('U1', '8'): 'SW_BUCK',
    ('U1', '9'): 'GND_PWR',

    ('L1', '1'): 'SW_BUCK',
    ('L1', '2'): 'VCC_5V',

    ('D2', '1'): 'KL30_IN',
    ('D2', '2'): 'GND_PWR',

    ('C1', '1'): 'KL30_IN',
    ('C1', '2'): 'GND_PWR',

    ('C2', '1'): 'VCC_5V',
    ('C2', '2'): 'GND_PWR',

    ('C3', '1'): 'BST_BUCK',
    ('C3', '2'): 'SW_BUCK',

    ('C4', '1'): 'VCC_BUCK',
    ('C4', '2'): 'GND_PWR',

    ('R1', '1'): 'KL30_IN',
    ('R1', '2'): 'EN_BUCK',

    ('R2', '1'): 'EN_BUCK',
    ('R2', '2'): 'GND_PWR',

    ('U9', '1'): 'VCC_5V',
    ('U9', '2'): 'GND_PWR',
    ('U9', '3'): 'VCC_5V',
    ('U9', '4'): '',
    ('U9', '5'): 'VCC_3V3',

    # Digital Core
    ('U2', '1'): 'GND_PWR',
    ('U2', '2'): 'VCC_3V3',
    ('U2', '3'): 'ESP_EN',
    ('U2', '4'): 'ADC_BAT',
    ('U2', '5'): 'ONEWIRE_ID',
    ('U2', '6'): 'ADC_LINE_LVL',
    ('U2', '7'): 'ADC_VIGN',
    ('U2', '8'): 'PORT1_KEY_MCU',
    ('U2', '9'): 'PORT1_VCC_EN',
    ('U2', '10'): 'PORT2_KEY_MCU',
    ('U2', '11'): 'PORT2_VCC_EN',
    ('U2', '12'): 'I2S_MCLK',
    ('U2', '13'): 'I2S_BCLK',
    ('U2', '14'): 'I2S_WS',
    ('U2', '15'): 'I2S_DOUT',
    ('U2', '16'): 'I2S_DIN',
    ('U2', '17'): 'I2C_SDA',
    ('U2', '18'): 'I2C_SCL',
    ('U2', '19'): 'POD3_UART_RX',
    ('U2', '20'): 'POD3_UART_TX',
    ('U2', '21'): 'CAN_TX',
    ('U2', '22'): 'CAN_RX',
    ('U2', '23'): 'POD3_GNSS_PPS',
    ('U2', '24'): 'ONEWIRE_ID',
    ('U2', '25'): 'RESERVE_GPIO_A',
    ('U2', '26'): 'RESERVE_GPIO_B',
    ('U2', '27'): 'STATUS_LED_MCU',
    ('U2', '28'): 'UART_TXD0',
    ('U2', '29'): 'UART_RXD0',
    ('U2', '30'): 'USB_D_N',
    ('U2', '31'): 'USB_D_P',
    ('U2', '40'): 'GND_PWR',
    ('U2', '41'): 'GND_PWR',

    ('C10', '1'): 'VCC_3V3',
    ('C10', '2'): 'GND_PWR',
    ('C11', '1'): 'VCC_3V3',
    ('C11', '2'): 'GND_PWR',

    # Sensors & MicroSD
    ('U5', '1'): 'VCC_3V3',
    ('U5', '2'): 'I2C_SDA',
    ('U5', '3'): 'GND_PWR',
    ('U5', '4'): '',
    ('U5', '5'): 'VCC_3V3',
    ('U5', '6'): 'GND_PWR',
    ('U5', '7'): 'GND_PWR',
    ('U5', '8'): 'VCC_3V3',
    ('U5', '9'): '',
    ('U5', '10'): 'GND_PWR',
    ('U5', '11'): 'GND_PWR',
    ('U5', '12'): 'VCC_3V3',
    ('U5', '13'): 'I2C_SCL',
    ('U5', '14'): 'GND_PWR',

    ('C12', '1'): 'VCC_3V3',
    ('C12', '2'): 'GND_PWR',

    ('R10', '1'): 'VCC_3V3',
    ('R10', '2'): 'I2C_SDA',
    ('R11', '1'): 'VCC_3V3',
    ('R11', '2'): 'I2C_SCL',

    ('J2', '1'): 'SD_DAT2',
    ('J2', '2'): 'SD_DAT3',
    ('J2', '3'): 'SD_CMD',
    ('J2', '4'): 'VCC_3V3',
    ('J2', '5'): 'SD_CLK',
    ('J2', '6'): 'GND_PWR',
    ('J2', '7'): 'SD_DAT0',
    ('J2', '8'): 'SD_DAT1',
    ('J2', '9'): 'GND_PWR',
    ('J2', '10'): 'GND_PWR',
    ('J2', '11'): 'GND_PWR',
    ('J2', '12'): 'GND_PWR',

    # CAN Transceiver
    ('U6', '1'): 'CAN_TX',
    ('U6', '2'): 'GND_PWR',
    ('U6', '3'): 'VCC_3V3',
    ('U6', '4'): 'CAN_RX',
    ('U6', '5'): '',
    ('U6', '6'): 'CAN_L',
    ('U6', '7'): 'CAN_H',
    ('U6', '8'): 'GND_PWR',

    ('R9', '1'): 'CAN_H',
    ('R9', '2'): 'CAN_L',

    # Audio Codec
    ('U3', '1'): 'I2S_MCLK',
    ('U3', '2'): 'I2S_BCLK',
    ('U3', '3'): 'I2S_WS',
    ('U3', '4'): 'I2S_DIN',
    ('U3', '5'): 'I2S_DOUT',
    ('U3', '6'): 'I2C_SCL',
    ('U3', '7'): 'I2C_SDA',
    ('U3', '8'): 'VCC_3V3',
    ('U3', '9'): 'GND_PWR',
    ('U3', '10'): 'AUDIO_OUT_P',
    ('U3', '11'): 'AUDIO_OUT_N',
    ('U3', '12'): 'AGND',
    ('U3', '13'): 'AUDIO_IN_P',
    ('U3', '14'): 'AUDIO_IN_N',
    ('U3', '15'): 'AGND',
    ('U3', '16'): 'VCC_3V3',
    ('U3', '17'): 'AGND',
    ('U3', '28'): 'VCC_3V3',
    ('U3', '29'): 'GND_PWR',

    # Audio Transformers & Optos
    ('T1', '1'): 'AUDIO_OUT_P',
    ('T1', '2'): 'AUDIO_OUT_N',
    ('T1', '3'): 'POD1_NF_P',
    ('T1', '4'): 'POD1_NF_N',

    ('T2', '1'): 'AUDIO_IN_P',
    ('T2', '2'): 'AUDIO_IN_N',
    ('T2', '3'): 'POD2_NF_P',
    ('T2', '4'): 'POD2_NF_N',

    ('C6', '1'): 'POD1_NF_P',
    ('C6', '2'): 'POD1_NF_N',
    ('R5', '1'): 'PORT1_KEY_MCU',
    ('R5', '2'): 'POD1_OPTO_KEY',

    ('C7', '1'): 'POD2_NF_P',
    ('C7', '2'): 'POD2_NF_N',
    ('R6', '1'): 'PORT2_KEY_MCU',
    ('R6', '2'): 'POD2_OPTO_KEY',

    ('U7', '1'): 'PORT1_KEY_MCU',
    ('U7', '2'): 'GND_PWR',
    ('U7', '3'): 'POD1_OPTO_KEY',
    ('U7', '4'): 'POD1_OPTO_RET',

    ('U8', '1'): 'PORT2_KEY_MCU',
    ('U8', '2'): 'GND_PWR',
    ('U8', '3'): 'POD2_OPTO_KEY',
    ('U8', '4'): 'POD2_OPTO_RET',

    # Status LEDs
    ('D1', '1'): 'VCC_5V',
    ('D1', '2'): 'STATUS_LED_MCU',
    ('D1', '3'): 'GND_PWR',
    ('D1', '4'): 'STATUS_LED_EXT',

    # Connectors
    ('J3', '1'): 'VCC_5V',
    ('J3', '2'): 'USB_D_N',
    ('J3', '3'): 'USB_D_P',
    ('J3', '4'): 'GND_PWR',
    ('J3', '5'): 'UART_TXD0',
    ('J3', '6'): 'UART_RXD0',
    ('J3', '7'): 'ESP_EN',
    ('J3', '8'): 'ESP_BOOT',
    ('J3', '9'): 'GND_PWR',
    ('J3', '10'): 'GND_SHIELD',

    ('J1', '1'): 'POD1_VCC',
    ('J1', '2'): 'POD1_NF_P',
    ('J1', '3'): 'POD1_NF_N',
    ('J1', '4'): 'POD1_OPTO_KEY',
    ('J1', '5'): 'POD2_VCC',
    ('J1', '6'): 'POD2_NF_P',
    ('J1', '7'): 'POD2_NF_N',
    ('J1', '8'): 'POD2_OPTO_KEY',
    ('J1', '9'): 'POD3_VCC',
    ('J1', '10'): 'POD3_UART_TX',
    ('J1', '11'): 'POD3_UART_RX',
    ('J1', '12'): 'GND_PWR',
    ('J1', '13'): 'GND_PWR',
    ('J1', '14'): 'KL30_IN',
    ('J1', '15'): 'KL15_IGN',
    ('J1', '16'): 'GND_PWR',
    ('J1', '17'): 'CAN_H',
    ('J1', '18'): 'CAN_L',
    ('J1', '19'): 'ONEWIRE_ID',
    ('J1', '20'): 'GND_SHIELD',
    ('J1', '21'): 'AGND',
    ('J1', '22'): 'RESERVE_GPIO_A',
    ('J1', '23'): 'RESERVE_GPIO_B',
    ('J1', '24'): 'I2S_DOUT',
    ('J1', '25'): 'I2S_BCLK',
    ('J1', '26'): 'GND_SHIELD',

    ('J4', '1'): 'VCC_5V',
    ('J4', '2'): 'STATUS_LED_EXT',
    ('J4', '3'): 'GND_PWR',

    ('J5', '1'): 'BAT_PLUS',
    ('J5', '2'): 'GND_PWR',
    ('J5', '3'): 'NTC_JEITA',
    ('J5', '4'): 'GND_PWR',

    ('H1', '1'): 'GND_SHIELD',
    ('H2', '1'): 'GND_SHIELD',
    ('H3', '1'): 'GND_SHIELD',
    ('H4', '1'): 'GND_SHIELD',
}

# Build net block in KiCad format
net_lines = []
for code in sorted(NETS.keys()):
    name = NETS[code]
    net_lines.append(f'\t(net {code} "{name}")')
new_net_block = '\n'.join(net_lines)

# Replace (net ...) declarations
pcb_text = re.sub(r'(\t\(net \d+ "[^"]*"\)\n)+', new_net_block + '\n', pcb_text)

# Robust pad parser that balances parentheses
def parse_sexpr_element(text, start_idx):
    depth = 0
    idx = start_idx
    while idx < len(text):
        if text[idx] == '(':
            depth += 1
        elif text[idx] == ')':
            depth -= 1
            if depth == 0:
                return text[start_idx:idx+1], idx+1
        idx += 1
    return text[start_idx:], len(text)

# Find each footprint
fp_matches = list(re.finditer(r'\(footprint\s+"[^"]+"', pcb_text))
new_pcb_text = ""
last_end = 0

for m in fp_matches:
    start_pos = m.start()
    new_pcb_text += pcb_text[last_end:start_pos]
    fp_str, end_pos = parse_sexpr_element(pcb_text, start_pos)
    last_end = end_pos
    
    # Get reference
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', fp_str)
    if not ref_m:
        new_pcb_text += fp_str
        continue
    ref = ref_m.group(1)
    
    # Process pads in fp_str
    pad_matches = list(re.finditer(r'\(pad\s+"[^"]+"', fp_str))
    new_fp_str = ""
    last_pad_end = 0
    for pm in pad_matches:
        p_start = pm.start()
        new_fp_str += fp_str[last_pad_end:p_start]
        pad_str, p_end = parse_sexpr_element(fp_str, p_start)
        last_pad_end = p_end
        
        num_m = re.search(r'\(pad "([^"]+)"', pad_str)
        pad_num = num_m.group(1) if num_m else ''
        
        # Remove any existing (net ...)
        pad_str = re.sub(r'\s*\(net\s+\d+(\s+"[^"]*")?\)', '', pad_str)
        
        net_name = PAD_NET_MAP.get((ref, pad_num), '')
        net_code = NET_NAME_TO_ID.get(net_name, 0)
        
        if net_code > 0:
            # Strip trailing ')' and add (net code "name") before closing
            pad_str = pad_str.rstrip()[:-1].rstrip() + f'\n\t\t\t(net {net_code} "{net_name}")\n\t\t)'
        new_fp_str += pad_str
        
    new_fp_str += fp_str[last_pad_end:]
    new_pcb_text += new_fp_str

new_pcb_text += pcb_text[last_end:]

with open(pcb_file, 'w') as f:
    f.write(new_pcb_text)

print("✓ Fixed netlist injection written successfully!")
