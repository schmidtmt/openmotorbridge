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
CAD_IMG_DIR = os.path.join(REPO_ROOT, "docs/images/cad")

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
    ("01_main_box/parts/004_mounting_ears.scad", "01_main_box/components/04_mounting_ears.stl"),
    ("01_main_box/parts/005_sealing_groove.scad", "01_main_box/components/05_sealing_groove.stl"),
    ("01_main_box/parts/010_mid_tray_frame.scad", "01_main_box/components/06_mid_tray_frame.stl"),
    ("01_main_box/parts/011_mid_partition_floor.scad", "01_main_box/components/07_mid_partition_floor.stl"),
    ("01_main_box/parts/020_lid_plate.scad", "01_main_box/components/08_lid_plate.stl"),
    
    # 5. Modular Components (Pod Base)
    ("02_pod_base/parts/000_pod_tunnel_base.scad", "02_pod_base/components/01_pod_tunnel_base.stl"),
    ("02_pod_base/parts/001_pod_rear_m8_gland.scad", "02_pod_base/components/02_pod_rear_m8_gland.stl"),
    ("02_pod_base/parts/002_pod_bulkhead_partition.scad", "02_pod_base/components/03_pod_bulkhead_partition.stl"),
    ("02_pod_base/parts/003_pod_guide_grooves.scad", "02_pod_base/components/04_pod_guide_grooves.stl"),
    ("02_pod_base/parts/005_pod_strap_hooks.scad", "02_pod_base/components/05_pod_strap_hooks.stl"),
    
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
        "55,37,65,55,0,310,360",
        "Tomorrow"
    ),
    (
        "01_main_box/98_closed_box.scad",
        os.path.join(CAD_IMG_DIR, "main_box_enclosure_cad.png"),
        "55,37,18,55,0,310,250",
        "Tomorrow"
    ),
    (
        "01_main_box/97_main_box_xray.scad",
        os.path.join(CAD_IMG_DIR, "main_box_assembly_mated_3d.png"),
        "55,37,18,55,0,310,250",
        "Tomorrow"
    ),
    (
        "02_pod_base/99_pod_base_assembly.scad",
        os.path.join(CAD_IMG_DIR, "openmotorbridge_pod_exploded_view.png"),
        "50,30,14,55,0,310,300",
        "Tomorrow"
    ),
    (
        "02_pod_base/97_pod_xray_assembly.scad",
        os.path.join(CAD_IMG_DIR, "openmotorbridge_pod_assembly_render_xray.png"),
        "50,30,14,55,0,310,250",
        "Tomorrow"
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
        "55,30,14,18,0,80,125",
        "Tomorrow"
    ),
    (
        "02_pod_base/99_pod3_rear_assembly.scad",
        os.path.join(CAD_IMG_DIR, "pod3_full_assembly_exploded_3d.png"),
        "50,30,14,55,0,310,340",
        "Tomorrow"
    ),
]

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_WORKERS = min(12, os.cpu_count() or 8)
print_lock = threading.Lock()

def clean_old_stls():
    print("🧹 Cleaning old STL directory...")
    if os.path.exists(STL_BASE):
        shutil.rmtree(STL_BASE)
    os.makedirs(STL_BASE, exist_ok=True)
    os.makedirs(os.path.join(STL_BASE, "01_main_box/components"), exist_ok=True)
    os.makedirs(os.path.join(STL_BASE, "02_pod_base/components"), exist_ok=True)
    os.makedirs(os.path.join(STL_BASE, "03_pod_cartridges/components"), exist_ok=True)
    sys.stdout.flush()

def compile_single_stl(scad_rel: str, stl_rel: str, idx: int, total: int) -> Tuple[bool, str, float]:
    scad_path = os.path.join(SCAD_DIR, scad_rel)
    stl_path = os.path.join(STL_BASE, stl_rel)
    os.makedirs(os.path.dirname(stl_path), exist_ok=True)
    
    t0 = time.time()
    cmd = [
        OPENSCAD_BIN,
        "-o", stl_path,
        "--export-format", "binstl",
        scad_path
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    dt = time.time() - t0
    
    if res.returncode != 0:
        return False, f"❌ Error compiling {scad_rel}:\n{res.stderr}", dt
    else:
        size_kb = os.path.getsize(stl_path) / 1024.0
        return True, f"✅ Exported {stl_rel} ({size_kb:.1f} KB) in {dt:.1f}s", dt

def compile_stls():
    total = len(STL_TARGETS)
    print(f"\n🔨 Compiling {total} OpenSCAD models to Production STLs (Parallel across {MAX_WORKERS} workers)...")
    sys.stdout.flush()
    start_total = time.time()
    
    completed_count = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_map = {
            executor.submit(compile_single_stl, scad_rel, stl_rel, idx, total): (scad_rel, stl_rel)
            for idx, (scad_rel, stl_rel) in enumerate(STL_TARGETS, 1)
        }
        for future in as_completed(future_map):
            completed_count += 1
            success, msg, dt = future.result()
            with print_lock:
                print(f"[{completed_count:2d}/{total:2d}] {msg}")
                sys.stdout.flush()
                
    print(f"✨ All {total} STLs compiled in {time.time() - start_total:.1f}s.")
    sys.stdout.flush()

def render_single_image(scad_rel: str, img_path: str, camera_args: str, scheme: str, idx: int, total: int) -> Tuple[bool, str, float]:
    scad_path = os.path.join(SCAD_DIR, scad_rel)
    os.makedirs(os.path.dirname(img_path), exist_ok=True)
    img_name = os.path.basename(img_path)
    
    t0 = time.time()
    cmd = [
        OPENSCAD_BIN,
        "--preview",
        "-o", img_path,
        f"--camera={camera_args}",
        f"--colorscheme={scheme}",
        "--imgsize=1920,1080",
        scad_path
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    dt = time.time() - t0
    
    if res.returncode != 0:
        return False, f"❌ Error rendering {img_name}:\n{res.stderr}", dt
    else:
        size_kb = os.path.getsize(img_path) / 1024.0
        return True, f"✅ Rendered {img_name} ({size_kb:.1f} KB) in {dt:.1f}s", dt

def render_images():
    total = len(RENDER_TARGETS)
    print(f"\n📸 Generating {total} High-Resolution 3D PNG Renders (Parallel across {MAX_WORKERS} workers)...")
    sys.stdout.flush()
    start_total = time.time()
    
    completed_count = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_map = {
            executor.submit(render_single_image, scad_rel, img_path, camera_args, scheme, idx, total): img_path
            for idx, (scad_rel, img_path, camera_args, scheme) in enumerate(RENDER_TARGETS, 1)
        }
        for future in as_completed(future_map):
            completed_count += 1
            success, msg, dt = future.result()
            with print_lock:
                print(f"[{completed_count:2d}/{total:2d}] {msg}")
                sys.stdout.flush()
                
    print(f"✨ All {total} 3D Renders generated in {time.time() - start_total:.1f}s.")
    sys.stdout.flush()

def fix_permissions_and_attributes():
    print("\n🔓 Setting full permissions and stripping macOS attributes...")
    for path in [STL_BASE, CAD_IMG_DIR, SCAD_DIR]:
        try:
            subprocess.run(["xattr", "-c", "-r", path], capture_output=True)
            subprocess.run(["chmod", "-R", "777", path], capture_output=True)
        except Exception as e:
            print(f"Warning: {e}")
    print("Permissions and attributes fixed.")
    sys.stdout.flush()

def main():
    print("=" * 80)
    print("OPENMOTORBRIDGE OPENSCAD MASTER BUILDER".center(80))
    print("=" * 80)
    sys.stdout.flush()
    
    clean_old_stls()
    compile_stls()
    render_images()
    fix_permissions_and_attributes()
    
    print("\n" + "=" * 80)
    print("🎉 ALL STLS & 3D RENDERS GENERATED DIRECTLY FROM OPENSCAD!".center(80))
    print("=" * 80)
    sys.stdout.flush()

if __name__ == '__main__':
    main()
