#!/usr/bin/env python3
"""
OpenMotorBridge - Master OpenSCAD STL & 3D Render Builder
=========================================================
Compiles all parametric OpenSCAD (.scad) source models into:
1. High-precision production STLs in `hardware/cad/stl/` and `hardware/3d_models_mjf/`
2. High-resolution photo-realistic PNG renders in `hardware/cad/`
3. Automatically sets full 777 permissions and strips macOS extended attributes.
"""

import os
import sys
import shutil
import subprocess
import time
from typing import List, Tuple

OPENSCAD_BIN = "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"
REPO_ROOT = "/Users/schmidtm/openMotorBridge"
SCAD_DIR = os.path.join(REPO_ROOT, "hardware/cad/scad")
STL_BASE = os.path.join(REPO_ROOT, "hardware/cad/stl")
MJF_BASE = os.path.join(REPO_ROOT, "hardware/3d_models_mjf")
CAD_IMG_DIR = os.path.join(REPO_ROOT, "hardware/cad")

# Check OpenSCAD binary
if not os.path.exists(OPENSCAD_BIN):
    print(f"ERROR: OpenSCAD binary not found at {OPENSCAD_BIN}")
    sys.exit(1)

# List of Master Production STL Targets (Source SCAD -> Target Relative STL)
STL_TARGETS: List[Tuple[str, str]] = [
    # 1. Main Box
    ("01_main_box/00_lower_deck.scad", "01_main_box/main_box_lower_case.stl"),
    ("01_main_box/01_upper_deck.scad", "01_main_box/main_box_mid_tray.stl"),
    ("01_main_box/02_colsure.scad", "01_main_box/main_box_lid.stl"),
    
    # 2. Satellite Pod Base
    ("02_pod_base/pod_base_housing.scad", "02_pod_base/pod_base_housing.stl"),
    ("02_pod_base/pod_mount_helmet_clamp.scad", "02_pod_base/pod_mount_helmet_clamp.stl"),
    ("02_pod_base/pod_mount_gopro_rack.scad", "02_pod_base/pod_mount_gopro_rack.stl"),
    
    # 3. Pod Cartridges
    ("03_pod_cartridges/00_base_sled.scad", "03_pod_cartridges/cartridge_base_sled.stl"),
    ("03_pod_cartridges/cartridge_omm_transceiver.scad", "03_pod_cartridges/cartridge_omm_transceiver_sled.stl"),
    ("03_pod_cartridges/cartridge_sena.scad", "03_pod_cartridges/cartridge_sena_sled.stl"),
    ("03_pod_cartridges/cartridge_cardo.scad", "03_pod_cartridges/cartridge_cardo_sled.stl"),
    ("03_pod_cartridges/cartridge_blindkassette.scad", "03_pod_cartridges/cartridge_blindkassette_waterproof.stl"),
    
    # 4. Modular Components (Main Box)
    ("01_main_box/parts/000_lower_base.scad", "01_main_box/components/01_lower_tub_empty.stl"),
    ("01_main_box/parts/001_lower_screws_enclosure.scad", "01_main_box/components/02_corner_screws_enclosure.stl"),
    ("01_main_box/parts/002_pcb_standoffs.scad", "01_main_box/components/03_pcb_standoffs.stl"),
    ("01_main_box/parts/003_copper_thermal_studs.scad", "01_main_box/components/04_copper_thermal_studs.stl"),
    ("01_main_box/parts/004_mounting_ears.scad", "01_main_box/components/05_mounting_ears.stl"),
    ("01_main_box/parts/010_mid_tray_frame.scad", "01_main_box/components/06_mid_tray_frame.stl"),
    ("01_main_box/parts/011_mid_partition_floor.scad", "01_main_box/components/07_mid_partition_floor.stl"),
    ("01_main_box/parts/020_lid_plate.scad", "01_main_box/components/08_lid_plate.stl"),
    
    # 5. Modular Components (Pod Base)
    ("02_pod_base/parts/000_pod_tunnel_base.scad", "02_pod_base/components/01_pod_tunnel_base.stl"),
    ("02_pod_base/parts/001_pod_rear_m8_gland.scad", "02_pod_base/components/02_pod_rear_m8_gland.stl"),
    ("02_pod_base/parts/002_pod_bulkhead_partition.scad", "02_pod_base/components/03_pod_bulkhead_partition.stl"),
    ("02_pod_base/parts/003_pod_guide_grooves.scad", "02_pod_base/components/04_pod_guide_grooves.stl"),
    ("02_pod_base/parts/004_pod_copper_studs.scad", "02_pod_base/components/05_pod_copper_studs.stl"),
    
    # 6. Dummies
    ("00_common/dummies/dummy_main_pcb.scad", "01_main_box/components/dummy_main_pcb.stl"),
    ("00_common/dummies/dummy_lipo_battery.scad", "01_main_box/components/dummy_lipo_battery.stl"),
    ("00_common/dummies/dummy_omm_transceiver_pcb.scad", "03_pod_cartridges/components/dummy_omm_transceiver_pcb.stl"),
    ("00_common/dummies/dummy_adapter_pcb.scad", "03_pod_cartridges/components/dummy_adapter_pcb.stl"),
    ("00_common/dummies/dummy_m8_connector.scad", "02_pod_base/components/dummy_m8_connector.stl"),
]

# List of High-Resolution 3D Render Targets
RENDER_TARGETS: List[Tuple[str, str, str, str]] = [
    # (Source SCAD, Target PNG, Camera Parameters, Color Scheme)
    (
        "01_main_box/99_overall_box.scad",
        os.path.join(CAD_IMG_DIR, "main_box_full_assembly_exploded_3d.png"),
        "55,37,25,55,0,310,400",
        "Tomorrow"
    ),
    (
        "01_main_box/00_lower_deck.scad",
        os.path.join(CAD_IMG_DIR, "main_box_enclosure_cad.png"),
        "55,37,10,55,0,310,250",
        "Solarized"
    ),
    (
        "02_pod_base/99_pod_base_assembly.scad",
        os.path.join(CAD_IMG_DIR, "openmotorbridge_pod_exploded_view.png"),
        "50,30,14,55,0,310,300",
        "Tomorrow"
    ),
    (
        "02_pod_base/pod_base_housing.scad",
        os.path.join(CAD_IMG_DIR, "openmotorbridge_pod_assembly_render_xray.png"),
        "50,30,14,55,0,310,250",
        "Solarized"
    ),
    (
        "03_pod_cartridges/99_cartridge_assembly.scad",
        os.path.join(CAD_IMG_DIR, "cartridge_variants_trio.png"),
        "50,40,10,55,0,310,380",
        "Tomorrow"
    ),
    (
        "03_pod_cartridges/cartridge_sena.scad",
        os.path.join(CAD_IMG_DIR, "sena_cartridge_assembly_cad.png"),
        "37.5,27,10,55,0,310,200",
        "Solarized"
    ),
    (
        "03_pod_cartridges/cartridge_cardo.scad",
        os.path.join(CAD_IMG_DIR, "cardo_cartridge_assembly_cad.png"),
        "37.5,27,10,55,0,310,200",
        "Solarized"
    ),
    (
        "03_pod_cartridges/cartridge_blindkassette.scad",
        os.path.join(CAD_IMG_DIR, "dummy_cartridge_cad.png"),
        "37.5,27,10,55,0,310,200",
        "Solarized"
    ),
    (
        "02_pod_base/pod_poka_yoke_cross_section.scad",
        os.path.join(CAD_IMG_DIR, "pod_poka_yoke_cross_section_cad.png"),
        "50,30,14,25,0,325,180",
        "Tomorrow"
    ),
]

def clean_old_stls():
    print("🧹 Cleaning old STL directories...")
    for base in [STL_BASE, MJF_BASE]:
        if os.path.exists(base):
            shutil.rmtree(base)
        os.makedirs(base, exist_ok=True)
        os.makedirs(os.path.join(base, "01_main_box/components"), exist_ok=True)
        os.makedirs(os.path.join(base, "02_pod_base/components"), exist_ok=True)
        os.makedirs(os.path.join(base, "03_pod_cartridges/components"), exist_ok=True)

def compile_stls():
    print("\n🔨 Compiling OpenSCAD models to Production STLs...")
    start_total = time.time()
    
    for idx, (scad_rel, stl_rel) in enumerate(STL_TARGETS, 1):
        scad_path = os.path.join(SCAD_DIR, scad_rel)
        stl_path = os.path.join(STL_BASE, stl_rel)
        mjf_path = os.path.join(MJF_BASE, stl_rel)
        
        os.makedirs(os.path.dirname(stl_path), exist_ok=True)
        os.makedirs(os.path.dirname(mjf_path), exist_ok=True)
        
        print(f"[{idx}/{len(STL_TARGETS)}] Exporting {stl_rel}...")
        t0 = time.time()
        
        cmd = [
            OPENSCAD_BIN,
            "-o", stl_path,
            scad_path
        ]
        
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"  ❌ Error compiling {scad_rel}:\n{res.stderr}")
        else:
            size_kb = os.path.getsize(stl_path) / 1024.0
            dt = time.time() - t0
            print(f"  ✅ Done in {dt:.1f}s ({size_kb:.1f} KB)")
            # Copy to MJF folder as well
            shutil.copy2(stl_path, mjf_path)
            
    print(f"All STLs compiled in {time.time() - start_total:.1f}s.")

def render_images():
    print("\n📸 Generating High-Resolution 3D PNG Renders...")
    for idx, (scad_rel, img_path, camera_args, scheme) in enumerate(RENDER_TARGETS, 1):
        scad_path = os.path.join(SCAD_DIR, scad_rel)
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        
        img_name = os.path.basename(img_path)
        print(f"[{idx}/{len(RENDER_TARGETS)}] Rendering {img_name}...")
        t0 = time.time()
        
        cmd = [
            OPENSCAD_BIN,
            "--render",
            "-o", img_path,
            f"--camera={camera_args}",
            f"--colorscheme={scheme}",
            "--imgsize=1920,1080",
            scad_path
        ]
        
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"  ❌ Error rendering {img_name}:\n{res.stderr}")
        else:
            size_kb = os.path.getsize(img_path) / 1024.0
            dt = time.time() - t0
            print(f"  ✅ Rendered in {dt:.1f}s ({size_kb:.1f} KB)")

def fix_permissions_and_attributes():
    print("\n🔓 Setting full permissions and stripping macOS attributes...")
    for path in [STL_BASE, MJF_BASE, CAD_IMG_DIR, SCAD_DIR]:
        try:
            subprocess.run(["xattr", "-c", "-r", path], capture_output=True)
            subprocess.run(["chmod", "-R", "777", path], capture_output=True)
        except Exception as e:
            print(f"Warning: {e}")
    print("Permissions and attributes fixed.")

def main():
    print("=" * 80)
    print("OPENMOTORBRIDGE OPENSCAD MASTER BUILDER".center(80))
    print("=" * 80)
    
    clean_old_stls()
    compile_stls()
    render_images()
    fix_permissions_and_attributes()
    
    print("\n" + "=" * 80)
    print("🎉 ALL STLS & 3D RENDERS GENERATED DIRECTLY FROM OPENSCAD!".center(80))
    print("=" * 80)

if __name__ == '__main__':
    main()
