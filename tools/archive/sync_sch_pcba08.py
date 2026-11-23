#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
tools/sync_sch_pcba08.py
========================
Synchronizes openmotorbridge_radar_submcu.kicad_sch:
- Removes duplicate J4 symbol.
- Attaches global labels and wires directly to U1, U3, and J4 pins.
"""

import re
import subprocess

SCH_PATH = "hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_sch"
KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

def main():
    with open(SCH_PATH, "r") as f:
        sch = f.read()

    # 1. Remove floating unattached UWB global labels
    floating_labels = [
        "UWB_SCK", "UWB_MOSI", "UWB_MISO", "UWB_CS", "UWB_IRQ", "UWB_RST"
    ]
    for lbl in floating_labels:
        sch = re.sub(rf'\(global_label\s+\"{lbl}\"[^\)]+\(at\s+120\.0\s+[0-9.]+\s+[0-9.]+\)[^\)]+\)\n?', '', sch)

    # 2. Remove duplicate J4 at (180.0 120.0 0)
    dup_j4_pattern = r'\(symbol\s+\(lib_id\s+\"Connector:Conn_Coaxial\"\)\s+\(at\s+180\.0\s+120\.0\s+0\).*?\(property\s+\"Reference\"\s+\"J4\".*?\)\n\t\)'
    sch = re.sub(dup_j4_pattern, '', sch, flags=re.DOTALL)

    # 3. Add proper global labels at U1 pins
    u1_labels = """
	(global_label "UWB_RST" (shape output) (at 75.24 84.76 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "UWB_SCK" (shape output) (at 75.24 102.54 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "UWB_MOSI" (shape output) (at 75.24 105.08 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "UWB_MISO" (shape input) (at 75.24 107.62 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "UWB_CS" (shape output) (at 75.24 110.16 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "UWB_IRQ" (shape input) (at 75.24 112.70 180) (effects (font (size 1.27 1.27)) (justify right)))
"""

    # 4. Add proper global labels & wires at U3 and J4 pins
    u3_labels_wires = """
	(global_label "VCC_3V3" (shape input) (at 132.22 102.30 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "UWB_SCK" (shape input) (at 132.22 107.38 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "UWB_MISO" (shape output) (at 132.22 112.46 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "UWB_MOSI" (shape input) (at 132.22 117.54 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "UWB_CS" (shape input) (at 132.22 122.62 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "UWB_IRQ" (shape output) (at 167.78 102.30 0) (effects (font (size 1.27 1.27)) (justify left)))
	(global_label "UWB_RST" (shape input) (at 167.78 107.38 180) (effects (font (size 1.27 1.27)) (justify right)))
	(global_label "GND" (shape passive) (at 150.00 137.86 270) (effects (font (size 1.27 1.27)) (justify right)))
	(wire (pts (xy 167.78 115.00) (xy 174.92 115.00)) (stroke (width 0) (type default)))
	(global_label "GND" (shape passive) (at 180.00 120.08 270) (effects (font (size 1.27 1.27)) (justify right)))
"""

    # Insert before the closing parenthesis of the schematic
    idx = sch.rfind(")")
    sch = sch[:idx] + u1_labels + u3_labels_wires + "\n)\n"

    with open(SCH_PATH, "w") as f:
        f.write(sch)
    print("✓ Successfully synchronized openmotorbridge_radar_submcu.kicad_sch.")

if __name__ == "__main__":
    main()
