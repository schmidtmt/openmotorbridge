#!/usr/bin/env python3
import re

pcb_path = "hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update J1 pads: change (net "PGND") to (net "GND")
def update_j1(m):
    fp = m.group(0)
    fp = fp.replace('(net "PGND")', '(net "GND")')
    return fp

content = re.sub(r'\(footprint\s+.*?"Reference"\s+"J1".*?\n\t\)', update_j1, content, flags=re.DOTALL)

# 2. Update U1 pads: remove SA818 nets
sa818_nets = [
    '(net "SA818_TXD")',
    '(net "SA818_RXD")',
    '(net "SA818_PTT")',
    '(net "SA818_SQL")',
    '(net "SA818_PWR_HL")',
    '(net "SA818_MIC_IN")',
    '(net "SA818_AF_OUT")',
]

for s_net in sa818_nets:
    content = content.replace(f"\n\t\t\t{s_net}", "")
    content = content.replace(f"\t\t\t{s_net}\n", "")
    content = content.replace(s_net, "")

# 3. Remove dangling PGND tracks if any
content = re.sub(r'\(segment\s+[^)]*?\(net\s+"PGND"\)[^)]*?\)\n?', '', content)

# 4. Remove net declarations for PGND and SA818_*
content = re.sub(r'\s*\(net\s+\d+\s+"(PGND|SA818_[^"]+)"\)', '', content)
content = re.sub(r'\s*\(net\s+"(PGND|SA818_[^"]+)"\)', '', content)

with open(pcb_path, "w", encoding="utf-8") as f:
    f.write(content)

print("PCBA 09 PCB updated successfully.")
