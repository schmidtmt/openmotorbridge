#!/usr/bin/env python3
"""
=============================================================================
OpenMotorBridge - Master Production & Manufacturing Exporter
=============================================================================
Automatically generates all production-ready manufacturing packages for:
1. PCB Fabrication & SMT Assembly (JLCPCB / Eurocircuits):
   - Gerber RS-274X & Excellon Drill ZIP packages (all 4 boards)
   - JLCPCB-formatted BOM CSV (Bill of Materials with LCSC Part Numbers)
   - JLCPCB-formatted CPL CSV (Component Placement List / Pick & Place)
2. Mechanical 3D Printing (HP MJF PA12):
   - Grouped STL packages for Main Box, Pod Housings, and Cartridge Inlays
3. Wiring Harness Assembly:
   - Complete Pinout & Crimp Specification CSV for JLCPCB Wire Harness Service

Usage:
  python3 hardware/scripts/export_manufacturing_packages.py
=============================================================================
"""

import os
import subprocess
import shutil
import zipfile
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_BASE = os.path.join(BASE_DIR, "production_packages")
KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

BOARDS = [
    {
        "name": "01_main_box_pcba",
        "title": "OpenMotorBridge Central Main Box PCB",
        "sch": os.path.join(BASE_DIR, "kicad_main_box/openmotorbridge_main.kicad_sch"),
        "pcb": os.path.join(BASE_DIR, "kicad_main_box/openmotorbridge_main.kicad_pcb"),
        "layers": "F.Cu,B.Cu,In1.Cu,In2.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts",
        "is_4layer": True
    },
    {
        "name": "02_pod_base_pcba",
        "title": "OpenMotorBridge Pod Base Carrier PCB",
        "sch": os.path.join(BASE_DIR, "kicad_pod_base/openmotorbridge_pod_base.kicad_sch"),
        "pcb": os.path.join(BASE_DIR, "kicad_pod_base/openmotorbridge_pod_base.kicad_pcb"),
        "layers": "F.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts",
        "is_4layer": False
    },
    {
        "name": "03_pod_cartridge_pcba",
        "title": "OpenMotorBridge Universal Cartridge Carrier PCB",
        "sch": os.path.join(BASE_DIR, "kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_sch"),
        "pcb": os.path.join(BASE_DIR, "kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"),
        "layers": "F.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts",
        "is_4layer": False
    },
    {
        "name": "04_rear_pod3_pcba",
        "title": "OpenMotorBridge Rear Pod 3 Transceiver PCB",
        "sch": os.path.join(BASE_DIR, "kicad_rear_pod3/openmotorbridge_rear_pod3.kicad_sch"),
        "pcb": os.path.join(BASE_DIR, "kicad_rear_pod3/openmotorbridge_rear_pod3.kicad_pcb"),
        "layers": "F.Cu,B.Cu,In1.Cu,In2.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts",
        "is_4layer": True
    }
]

def export_jlcpcb_bom(pcb_file, sch_file, output_csv):
    import re
    components = []
    
    # Read components from .kicad_pcb
    with open(pcb_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match footprint blocks
    fp_pattern = re.compile(r'\(footprint\s+"([^"]+)"(?:[^\(\)]|\([^\(\)]*\))*\)', re.DOTALL)
    for m in re.finditer(r'\(footprint\s+"([^"]+)"', content):
        start = m.start()
        # Find balanced closing paren for this footprint
        depth = 0
        end = start
        for i in range(start, len(content)):
            if content[i] == '(':
                depth += 1
            elif content[i] == ')':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        fp_block = content[start:end]
        
        # Extract Reference, Value, Footprint, LCSC
        ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', fp_block)
        val_m = re.search(r'\(property\s+"Value"\s+"([^"]+)"', fp_block)
        lcsc_m = re.search(r'\(property\s+"LCSC"\s+"([^"]+)"', fp_block)
        footprint_name = m.group(1)

        ref = ref_m.group(1) if ref_m else ""
        val = val_m.group(1) if val_m else ""
        lcsc = lcsc_m.group(1) if lcsc_m else ""

        if ref and not ref.startswith("#") and not ref.startswith("G***"):
            components.append({
                "Designator": ref,
                "Comment": val,
                "Footprint": footprint_name,
                "LCSC Part #": lcsc
            })

    # Group components by Comment + Footprint + LCSC
    grouped = {}
    for c in components:
        key = (c["Comment"], c["Footprint"], c["LCSC Part #"])
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(c["Designator"])

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Designator", "Comment", "Footprint", "LCSC Part #", "Quantity"])
        for (comment, footprint, lcsc), refs in sorted(grouped.items(), key=lambda x: x[1][0]):
            writer.writerow([", ".join(sorted(refs)), comment, footprint, lcsc, len(refs)])

def export_pcb_packages():
    print("=" * 75)
    print("🚀 EXPORTING PCB GERBERS, DRILL, BOM & CPL FOR JLCPCB")
    print("=" * 75)

    for b in BOARDS:
        board_dir = os.path.join(OUTPUT_BASE, b["name"])
        gerber_tmp = os.path.join(board_dir, "gerbers_temp")
        os.makedirs(gerber_tmp, exist_ok=True)

        print(f"\n📦 Processing [{b['title']}]...")

        # 1. Export Gerbers
        cmd_gerbers = [
            KICAD_CLI, "pcb", "export", "gerbers",
            "-o", gerber_tmp,
            "-l", b["layers"],
            "--no-x2",
            "--subtract-soldermask",
            b["pcb"]
        ]
        subprocess.run(cmd_gerbers, check=True)

        # 2. Export Excellon Drill Files
        cmd_drill = [
            KICAD_CLI, "pcb", "export", "drill",
            "-o", gerber_tmp + "/",
            "--format", "excellon",
            "--excellon-separate-th",
            "--generate-map",
            b["pcb"]
        ]
        subprocess.run(cmd_drill, check=True)

        # 3. Zip Gerbers + Drill into JLCPCB production zip
        zip_path = os.path.join(board_dir, f"{b['name']}_gerbers_jlcpcb.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
            for root, _, files in os.walk(gerber_tmp):
                for f in files:
                    full_p = os.path.join(root, f)
                    z.write(full_p, arcname=f)
        shutil.rmtree(gerber_tmp)
        print(f"  ✅ Created Gerber ZIP: {os.path.basename(zip_path)} ({os.path.getsize(zip_path)} bytes)")

        # 4. Export Component Placement List (CPL / POS)
        pos_file = os.path.join(board_dir, f"{b['name']}_cpl_jlcpcb.csv")
        cmd_pos = [
            KICAD_CLI, "pcb", "export", "pos",
            "-o", pos_file,
            "--format", "csv",
            "--units", "mm",
            "--side", "both",
            b["pcb"]
        ]
        subprocess.run(cmd_pos, check=True)
        print(f"  ✅ Created CPL (Pick & Place): {os.path.basename(pos_file)}")

        # 5. Export BOM directly from PCB / SCH
        bom_file = os.path.join(board_dir, f"{b['name']}_bom_jlcpcb.csv")
        export_jlcpcb_bom(b["pcb"], b["sch"], bom_file)
        print(f"  ✅ Created BOM CSV: {os.path.basename(bom_file)}")

def export_wiring_harness_package():
    print("\n" + "=" * 75)
    print("🔌 GENERATING CENTRAL WIRING HARNESS MANUFACTURING SPECIFICATION")
    print("=" * 75)

    harness_dir = os.path.join(OUTPUT_BASE, "05_wiring_harness")
    os.makedirs(harness_dir, exist_ok=True)

    csv_path = os.path.join(harness_dir, "central_breakout_harness_wirelist.csv")
    
    rows = [
        ["Wire_ID", "Origin_Connector", "Origin_Pin", "Signal_Name", "Wire_Color", "Wire_Gauge", "Dest_Connector", "Dest_Pin", "Notes"],
        ["W01", "HD26_MALE", "1", "POD1_VCC", "Red", "AWG22 (0.34mm²)", "M8_6P_FEMALE_POD1", "1", "Pod 1 5V Power"],
        ["W02", "HD26_MALE", "2", "POD1_GND", "Black", "AWG22 (0.34mm²)", "M8_6P_FEMALE_POD1", "2", "Pod 1 Power GND"],
        ["W03", "HD26_MALE", "3", "POD1_AUDIO_P", "Blue", "AWG26 (0.14mm²)", "M8_6P_FEMALE_POD1", "3", "Twisted Pair with Pin 4"],
        ["W04", "HD26_MALE", "4", "POD1_AUDIO_N", "White-Blue", "AWG26 (0.14mm²)", "M8_6P_FEMALE_POD1", "4", "Twisted Pair with Pin 3"],
        ["W05", "HD26_MALE", "5", "POD1_PTT_TRIGGER", "Yellow", "AWG26 (0.14mm²)", "M8_6P_FEMALE_POD1", "5", "Isolated PhotoMOS Opto Key"],
        ["W06", "HD26_MALE", "6", "POD1_1WIRE_ID", "Green", "AWG26 (0.14mm²)", "M8_6P_FEMALE_POD1", "6", "DS2401 Silicon Serial ROM"],
        ["W07", "HD26_MALE", "7", "POD2_VCC", "Red", "AWG22 (0.34mm²)", "M8_6P_FEMALE_POD2", "1", "Pod 2 5V Power"],
        ["W08", "HD26_MALE", "8", "POD2_GND", "Black", "AWG22 (0.34mm²)", "M8_6P_FEMALE_POD2", "2", "Pod 2 Power GND"],
        ["W09", "HD26_MALE", "9", "POD2_AUDIO_P", "Orange", "AWG26 (0.14mm²)", "M8_6P_FEMALE_POD2", "3", "Twisted Pair with Pin 10"],
        ["W10", "HD26_MALE", "10", "POD2_AUDIO_N", "White-Orange", "AWG26 (0.14mm²)", "M8_6P_FEMALE_POD2", "4", "Twisted Pair with Pin 9"],
        ["W11", "HD26_MALE", "11", "POD2_PTT_TRIGGER", "Brown", "AWG26 (0.14mm²)", "M8_6P_FEMALE_POD2", "5", "Isolated PhotoMOS Opto Key"],
        ["W12", "HD26_MALE", "12", "POD2_1WIRE_ID", "Grey", "AWG26 (0.14mm²)", "M8_6P_FEMALE_POD2", "6", "DS2401 Silicon Serial ROM"],
        ["W13", "HD26_MALE", "13", "POD3_VCC", "Red", "AWG22 (0.34mm²)", "M8_6P_FEMALE_POD3", "1", "Pod 3 5V Power (Rear Transceiver)"],
        ["W14", "HD26_MALE", "14", "POD3_GND", "Black", "AWG22 (0.34mm²)", "M8_6P_FEMALE_POD3", "2", "Pod 3 Power GND"],
        ["W15", "HD26_MALE", "15", "POD3_UART_TX", "Violet", "AWG26 (0.14mm²)", "M8_6P_FEMALE_POD3", "3", "High-Speed UART (460.8k Baud)"],
        ["W16", "HD26_MALE", "16", "POD3_UART_RX", "White", "AWG26 (0.14mm²)", "M8_6P_FEMALE_POD3", "4", "High-Speed UART (460.8k Baud)"],
        ["W17", "HD26_MALE", "17", "POD3_GNSS_PPS", "Pink", "AWG26 (0.14mm²)", "M8_6P_FEMALE_POD3", "5", "1-PPS Hardware Time Sync"],
        ["W18", "HD26_MALE", "18", "POD3_1WIRE_ID", "Green-Black", "AWG26 (0.14mm²)", "M8_6P_FEMALE_POD3", "6", "DS2401 Silicon Serial ROM"],
        ["W19", "HD26_MALE", "19", "VBAT_KL30", "Red-White", "AWG20 (0.50mm²)", "SUPERSEAL_4P_POWER", "1", "Permanent 12V Battery Power"],
        ["W20", "HD26_MALE", "20", "IGNITION_KL15", "Yellow-Red", "AWG22 (0.34mm²)", "SUPERSEAL_4P_POWER", "2", "Switched Ignition 12V"],
        ["W21", "HD26_MALE", "21", "VEHICLE_GND", "Black-White", "AWG20 (0.50mm²)", "SUPERSEAL_4P_POWER", "3", "Vehicle Ground (KL31)"],
        ["W22", "HD26_MALE", "22", "CHASSIS_EARTH", "Green-Yellow", "AWG20 (0.50mm²)", "SUPERSEAL_4P_POWER", "4", "Direct Motorcycle Frame Earth"],
        ["W23", "HD26_MALE", "23", "CAN_H", "Yellow-Black", "AWG24 (0.22mm²)", "M8_4P_FEMALE_CAN_MIC", "1", "ISO 11898-2 CAN High (120Ω Diff)"],
        ["W24", "HD26_MALE", "24", "CAN_L", "Green-White", "AWG24 (0.22mm²)", "M8_4P_FEMALE_CAN_MIC", "2", "ISO 11898-2 CAN Low (120Ω Diff)"],
        ["W25", "HD26_MALE", "25", "FRONT_MIC_SIG", "Blue-Black", "AWG26 (0.14mm²)", "M8_4P_FEMALE_CAN_MIC", "3", "Ambient Mic Signal (SPH0645)"],
        ["W26", "HD26_MALE", "26", "FRONT_MIC_GND", "Black-Grey", "AWG26 (0.14mm²)", "M8_4P_FEMALE_CAN_MIC", "4", "Ambient Mic Ground Reference"]
    ]

    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"  ✅ Created Wire Harness Spec: {os.path.basename(csv_path)}")

def package_3d_print_stls():
    print("\n" + "=" * 75)
    print("🖨️  PACKAGING 3D PRINTING STL PACKAGES (HP MJF PA12)")
    print("=" * 75)

    stl_dir = os.path.join(OUTPUT_BASE, "06_3d_print_mjf_stls")
    os.makedirs(stl_dir, exist_ok=True)

    src_stl_base = os.path.join(BASE_DIR, "cad/stl")
    
    # 1. Main Box Package
    main_box_zip = os.path.join(stl_dir, "01_main_box_3d_print_mjf.zip")
    with zipfile.ZipFile(main_box_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in ["main_box_lower_case.stl", "main_box_mid_tray.stl", "main_box_lid.stl"]:
            p = os.path.join(src_stl_base, "01_main_box", f)
            if os.path.exists(p):
                z.write(p, arcname=f)
    print(f"  ✅ Created Main Box STL Package: {os.path.basename(main_box_zip)}")

    # 2. Satellite Pods Package
    pod_zip = os.path.join(stl_dir, "02_satellite_pods_3d_print_mjf.zip")
    with zipfile.ZipFile(pod_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in ["pod_base_housing.stl"]:
            p = os.path.join(src_stl_base, "02_pod_base", f)
            if os.path.exists(p):
                z.write(p, arcname=f)
    print(f"  ✅ Created Satellite Pods STL Package: {os.path.basename(pod_zip)}")

    # 3. Cartridges Package
    cartridge_zip = os.path.join(stl_dir, "03_cartridges_and_inlays_3d_print_mjf.zip")
    with zipfile.ZipFile(cartridge_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in ["cartridge_base_sled.stl", "cartridge_sena_sled.stl", "cartridge_cardo_sled.stl", "cartridge_omm_transceiver_sled.stl", "cartridge_blindkassette_waterproof.stl"]:
            p = os.path.join(src_stl_base, "03_pod_cartridges", f)
            if os.path.exists(p):
                z.write(p, arcname=f)
    print(f"  ✅ Created Cartridges STL Package: {os.path.basename(cartridge_zip)}")

if __name__ == "__main__":
    os.makedirs(OUTPUT_BASE, exist_ok=True)
    export_pcb_packages()
    export_wiring_harness_package()
    package_3d_print_stls()
    print("\n" + "=" * 75)
    print(f"🎉 ALL MANUFACTURING PACKAGES SUCCESSFULLY CREATED IN:")
    print(f"   {OUTPUT_BASE}")
    print("=" * 75)
