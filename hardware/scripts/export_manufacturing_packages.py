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
import sys
import subprocess
import shutil
import zipfile
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(BASE_DIR)
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
        "name": "03_pod_cartridge_pcba",
        "title": "OpenMotorBridge Universal Cartridge Carrier PCB",
        "sch": os.path.join(BASE_DIR, "kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_sch"),
        "pcb": os.path.join(BASE_DIR, "kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"),
        "layers": "F.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts",
        "is_4layer": False
    },
    {
        "name": "05_front_node_pcba",
        "title": "OpenMotorBridge Universal Front Node PCB",
        "sch": os.path.join(BASE_DIR, "kicad_front_node/openmotorbridge_front_node.kicad_sch"),
        "pcb": os.path.join(BASE_DIR, "kicad_front_node/openmotorbridge_front_node.kicad_pcb"),
        "layers": "F.Cu,B.Cu,In1.Cu,In2.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts",
        "is_4layer": True
    },
    {
        "name": "06_magsafe_dock_pcba",
        "title": "OpenMotorBridge MagSafe Frame Dock Adapter PCB",
        "sch": os.path.join(BASE_DIR, "kicad_magsafe_dock/openmotorbridge_magsafe_dock.kicad_sch"),
        "pcb": os.path.join(BASE_DIR, "kicad_magsafe_dock/openmotorbridge_magsafe_dock.kicad_pcb"),
        "layers": "F.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts",
        "is_4layer": False
    },
    {
        "name": "07_smart_keyfob_pcba",
        "title": "OpenMotorBridge 2-in-1 LoRa Smart-Keyfob & Pager PCB",
        "sch": os.path.join(BASE_DIR, "kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_sch"),
        "pcb": os.path.join(BASE_DIR, "kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb"),
        "layers": "F.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts",
        "is_4layer": False
    },
    {
        "name": "08_radar_submcu_pcba",
        "title": "OpenMotorBridge Radar 2.0 Sub-MCU, 5.9 GHz V2X & Halo PCB",
        "sch": os.path.join(BASE_DIR, "kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_sch"),
        "pcb": os.path.join(BASE_DIR, "kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb"),
        "layers": "F.Cu,B.Cu,In1.Cu,In2.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts",
        "is_4layer": True
    },
    {
        "name": "09_omm_ucs_pcba",
        "title": "OpenMotorBridge OMM 2.4 GHz Intercom & UCS Modul PCB",
        "sch": os.path.join(BASE_DIR, "kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_sch"),
        "pcb": os.path.join(BASE_DIR, "kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_pcb"),
        "layers": "F.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts",
        "is_4layer": False
    },
    {
        "name": "10_omm446_ucs_pcba",
        "title": "OpenMotorBridge OMM 446 MHz PMR/DMR Transceiver Modul PCB",
        "sch": os.path.join(BASE_DIR, "kicad_omm446_intercom/openmotorbridge_omm446_intercom.kicad_sch"),
        "pcb": os.path.join(BASE_DIR, "kicad_omm446_intercom/openmotorbridge_omm446_intercom.kicad_pcb"),
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

        if not lcsc:
            known_lcsc = {
                "ESP32-C6-MINI-1U": "C5267233",
                "BQ24075RGTR": "C96825",
                "XC6206P332MR": "C5446",
                "ES8388": "C365736",
                "ES8388_Codec": "C365736",
                "ES8311_Codec": "C396781",
                "ES8311": "C396781",
                "TYPE-C-31-M-12_IP67": "C2765186",
                "JST_2P_LiPo_600mAh": "C2902341",
                "WS2812B-2020": "C2843785",
                "USBLC6-2SC6": "C7519",
                "5.1k_CC1": "C23186",
                "5.1k_CC2": "C23186",
                "Power_MFB": "C318884",
                "Mesh_Group": "C318884",
                "Vol_Plus": "C318884",
                "Vol_Minus": "C318884",
                "SA818-DMR": "C2839211",
                "NiceRF_SA818-DMR": "C2839211",
                "ME6211C33M5G": "C82942",
                "J_AUDIO_PWR": "C160404",
                "BM08B-SRSS-TB": "C160404",
                "J_HELMET": "C136657",
                "HELMET_AUDIO_6P": "C136657",
                "SM06B-SRSS-TB": "C136657",
                "U.FL-R-SMT-1": "C14899",
                "BTN_PTT": "C318884",
                "BTN_MODE": "C318884",
                "BTN_CH_UP": "C318884",
                "BTN_CH_DOWN": "C318884",
            }
            if val in known_lcsc:
                lcsc = known_lcsc[val]
            elif ref in known_lcsc:
                lcsc = known_lcsc[ref]

        if ref and not ref.startswith("#") and not ref.startswith("G***") and not (ref.startswith("H") and "MountingHole" in val):
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
        ["W01", "DEUTSCH_DTM12_MALE", "1", "VBAT_KL30", "Red-White", "AWG20 (0.50mm²)", "SUPERSEAL_4P_POWER", "1", "Permanent 12V Battery Power"],
        ["W02", "DEUTSCH_DTM12_MALE", "2", "IGNITION_KL15", "Yellow-Red", "AWG22 (0.34mm²)", "SUPERSEAL_4P_POWER", "2", "Switched Ignition 12V"],
        ["W03", "DEUTSCH_DTM12_MALE", "3", "VEHICLE_GND", "Black-White", "AWG20 (0.50mm²)", "SUPERSEAL_4P_POWER", "3", "Vehicle Main Ground (KL31)"],
        ["W04", "DEUTSCH_DTM12_MALE", "4", "CAN_H", "Yellow", "AWG24 (0.22mm²)", "SUPERSEAL_4P_POWER", "CAN_H", "CAN High (Twisted Pair with Pin 5)"],
        ["W05", "DEUTSCH_DTM12_MALE", "5", "CAN_L", "Green", "AWG24 (0.22mm²)", "SUPERSEAL_4P_POWER", "CAN_L", "CAN Low (Twisted Pair with Pin 4)"],
        ["W06", "DEUTSCH_DTM12_MALE", "6", "POD1_VCC", "Red", "AWG22 (0.34mm²)", "JWPF_2P_POD1", "1", "Pod 1 Switched 5V Power (Port 1 Left)"],
        ["W07", "DEUTSCH_DTM12_MALE", "7", "POD1_GND", "Black", "AWG22 (0.34mm²)", "JWPF_2P_POD1", "2", "Pod 1 Power Ground Return"],
        ["W08", "DEUTSCH_DTM12_MALE", "8", "POD2_VCC", "Red", "AWG22 (0.34mm²)", "JWPF_2P_POD2", "1", "Pod 2 Switched 5V Power (Port 2 Right)"],
        ["W09", "DEUTSCH_DTM12_MALE", "9", "POD2_GND", "Black", "AWG22 (0.34mm²)", "JWPF_2P_POD2", "2", "Pod 2 Power Ground Return"],
        ["W10", "DEUTSCH_DTM12_MALE", "10", "RADAR_PWR_12V", "Red-Blue", "AWG22 (0.34mm²)", "JWPF_2P_RADAR", "1", "Switched 12V Radar Power (KL15 protected)"],
        ["W11", "DEUTSCH_DTM12_MALE", "11", "RADAR_GND", "Black-Blue", "AWG22 (0.34mm²)", "JWPF_2P_RADAR", "2", "Radar Power Ground Return"],
        ["W12", "DEUTSCH_DTM12_MALE", "12", "CHASSIS_EARTH", "Green-Yellow", "AWG20 (0.50mm²)", "SUPERSEAL_4P_POWER", "4", "Direct Motorcycle Frame Earth / Shield"]
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
        for f in [
            "cartridge_base_sled.stl",
            "cartridge_insert_sena.stl",
            "cartridge_insert_cardo.stl",
            "cartridge_insert_blindkassette.stl",
            "cartridge_universal_actuator_rails.stl",
            "cartridge_insert_omm_ucs.stl",
            "cartridge_antenna_bracket_omm.stl"
        ]:
            p = os.path.join(src_stl_base, "03_pod_cartridges", f)
            if os.path.exists(p):
                z.write(p, arcname=f)
    print(f"  ✅ Created Cartridges STL Package: {os.path.basename(cartridge_zip)}")

    # 4. Front Node Enclosure Package
    front_node_zip = os.path.join(stl_dir, "04_front_node_3d_print_mjf.zip")
    with zipfile.ZipFile(front_node_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in [
            "front_node_lower_tub.stl",
            "front_node_upper_lid.stl",
            "front_node_cable_glands_tpu.stl",
            "front_node_usbc_cap_tpu.stl"
        ]:
            p = os.path.join(src_stl_base, "04_front_node", f)
            if os.path.exists(p):
                z.write(p, arcname=f)
    print(f"  ✅ Created Front Node STL Package: {os.path.basename(front_node_zip)}")

    # 5. Smart Keyfob Enclosure Package
    keyfob_zip = os.path.join(stl_dir, "05_smart_keyfob_3d_print_mjf.zip")
    with zipfile.ZipFile(keyfob_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in [
            "smart_keyfob_lower_shell.stl",
            "smart_keyfob_upper_shell.stl",
            "smart_keyfob_tpu_rim.stl"
        ]:
            p = os.path.join(src_stl_base, "05_accessories", f)
            if os.path.exists(p):
                z.write(p, arcname=f)
    print(f"  ✅ Created Smart Keyfob STL Package: {os.path.basename(keyfob_zip)}")

    # 6. Symmetrical Accessories, Radar 2.0 & Vehicle Docks Package
    acc_zip = os.path.join(stl_dir, "06_accessories_and_brackets_3d_print_mjf.zip")
    with zipfile.ZipFile(acc_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in [
            "radar_mr20_housing.stl",
            "road_glide_inductive_cam_dock.stl",
            "car_sun_visor_pod_clip.stl",
            "adventure_rack_radar_mount.stl"
        ]:
            p = os.path.join(src_stl_base, "05_accessories", f)
            if os.path.exists(p):
                z.write(p, arcname=f)
    print(f"  ✅ Created Accessories & Brackets STL Package: {os.path.basename(acc_zip)}")

    # 7. OMM UCS Modules Enclosure Package (PCBA 09 & PCBA 10)
    omm_zip = os.path.join(stl_dir, "07_omm_ucs_modules_3d_print_mjf.zip")
    with zipfile.ZipFile(omm_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in [
            "omm_ucs_top_shell.stl",
            "omm_ucs_bottom_shell.stl",
            "omm_ucs_silicone_keypad.stl",
            "cartridge_insert_omm_ucs.stl",
            "cartridge_antenna_bracket_omm.stl"
        ]:
            p = os.path.join(src_stl_base, "03_pod_cartridges", f)
            if os.path.exists(p):
                z.write(p, arcname=f)
    print(f"  ✅ Created OMM UCS Modules STL Package: {os.path.basename(omm_zip)}")

def build_cad_assets():
    """
    Executes OpenSCAD CAD compilation script to build all STLs and 3D CAD renders.
    """
    print("\n" + "=" * 75)
    print("📐 COMPILING OPENSCAD 3D CAD ASSETS & RENDERS")
    print("=" * 75)
    script_path = os.path.join(BASE_DIR, "scripts/build_cad_from_openscad.py")
    subprocess.check_call([sys.executable, script_path])

def render_pcba_assets():
    """
    Executes KiCad 3D Raytracing & PCBA Views renderer and syncs to docs.
    """
    print("\n" + "=" * 75)
    print("🎨 RENDERING HIGH-RES 3D KiCad PCBAs & SYNCING TO DOCS")
    print("=" * 75)
    script_path = os.path.join(REPO_ROOT, "tools/render_all_pcbas.py")
    subprocess.check_call([sys.executable, script_path])

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="OpenMotorBridge Master Manufacturing & Production Package Exporter")
    parser.add_argument("--build-cad", action="store_true", help="Compile OpenSCAD models to STLs and renders")
    parser.add_argument("--render-pcba", action="store_true", help="Render KiCad 3D PCBA views and sync to docs")
    parser.add_argument("--with-renders", action="store_true", help="Compile CAD models, render CAD and render all PCBAs")
    parser.add_argument("--only-renders", action="store_true", help="Only run CAD and PCBA render generation without packaging")
    args = parser.parse_args()

    if args.with_renders or args.only_renders or args.build_cad:
        build_cad_assets()

    if args.with_renders or args.only_renders or args.render_pcba:
        render_pcba_assets()

    if not args.only_renders:
        os.makedirs(OUTPUT_BASE, exist_ok=True)
        export_pcb_packages()
        export_wiring_harness_package()
        package_3d_print_stls()
        print("\n" + "=" * 75)
        print(f"🎉 ALL MANUFACTURING PACKAGES SUCCESSFULLY CREATED IN:")
        print(f"   {OUTPUT_BASE}")
        print("=" * 75)
