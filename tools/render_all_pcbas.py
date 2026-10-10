#!/usr/bin/env python3
"""
Render high-resolution 3D and orthogonal views for all active OpenMotorBridge PCBAs
using kicad-cli and sync them to docs/images/pcba/ and hardware/kicad_*/.
"""

import os
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_PCBA_DIR = os.path.join(BASE_DIR, "docs/images/pcba")
KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

BOARDS = [
    {
        "id": "pcba01",
        "name": "01_main_box",
        "pcb": os.path.join(BASE_DIR, "hardware/kicad_main_box/openmotorbridge_main.kicad_pcb"),
        "dest_dir": os.path.join(BASE_DIR, "hardware/kicad_main_box"),
        "outputs": [
            ("pcba01_central_box_3d.png", ["--side", "top", "--rotate", "-45,0,45", "--quality", "high", "--perspective", "--zoom", "1.1"]),
            ("pcba01_central_box_top.png", ["--side", "top", "--quality", "high", "--zoom", "1.05"]),
            ("pcba01_central_box_bottom_3d.png", ["--side", "bottom", "--rotate", "45,0,-45", "--quality", "high", "--perspective", "--zoom", "1.1"]),
        ],
        "aliases": [
            ("pcba01_central_box_3d.png", "kicad_3d_render.png"),
            ("pcba01_central_box_top.png", "kicad_3d_render_top.png"),
            ("pcba01_central_box_bottom_3d.png", "kicad_3d_render_bottom.png"),
        ]
    },
    {
        "id": "pcba03",
        "name": "03_pod_cartridge",
        "pcb": os.path.join(BASE_DIR, "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb"),
        "dest_dir": os.path.join(BASE_DIR, "hardware/kicad_pod_cartridge"),
        "outputs": [
            ("pcba03_pod_cartridge_3d.png", ["--side", "top", "--rotate", "-45,0,45", "--quality", "high", "--perspective", "--zoom", "1.15"]),
            ("pcba03_pod_cartridge_top.png", ["--side", "top", "--quality", "high", "--zoom", "1.05"]),
            ("pcba03_pod_cartridge_bottom_3d.png", ["--side", "bottom", "--rotate", "45,0,-45", "--quality", "high", "--perspective", "--zoom", "1.15"]),
        ],
        "aliases": [
            ("pcba03_pod_cartridge_3d.png", "cartridge_3d_render_perspective.png"),
            ("pcba03_pod_cartridge_3d.png", "kicad_3d_render.png"),
            ("pcba03_pod_cartridge_top.png", "cartridge_3d_render_top.png"),
            ("pcba03_pod_cartridge_bottom_3d.png", "cartridge_3d_render_bottom.png"),
            ("pcba03_pod_cartridge_bottom_3d.png", "cartridge_3d_render_bottom_perspective.png"),
        ]
    },
    {
        "id": "pcba05",
        "name": "05_front_node",
        "pcb": os.path.join(BASE_DIR, "hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb"),
        "dest_dir": os.path.join(BASE_DIR, "hardware/kicad_front_node"),
        "outputs": [
            ("pcba05_front_node_3d.png", ["--side", "top", "--rotate", "-45,0,45", "--quality", "high", "--perspective", "--zoom", "1.1"]),
            ("pcba05_front_node_top.png", ["--side", "top", "--quality", "high", "--zoom", "1.05"]),
            ("pcba05_front_node_bottom_3d.png", ["--side", "bottom", "--rotate", "45,0,-45", "--quality", "high", "--perspective", "--zoom", "1.1"]),
        ],
        "aliases": [
            ("pcba05_front_node_top.png", "front_node_3d_render_top.png"),
            ("pcba05_front_node_bottom_3d.png", "front_node_3d_render_bottom.png"),
            ("pcba05_front_node_bottom_3d.png", "pcba05_front_node_3d_bottom.png"),
        ]
    },
    {
        "id": "pcba06",
        "name": "06_magsafe_dock",
        "pcb": os.path.join(BASE_DIR, "hardware/kicad_magsafe_dock/openmotorbridge_magsafe_dock.kicad_pcb"),
        "dest_dir": os.path.join(BASE_DIR, "hardware/kicad_magsafe_dock"),
        "outputs": [
            ("pcba06_magsafe_dock_3d.png", ["--side", "top", "--rotate", "-45,0,45", "--quality", "high", "--perspective", "--zoom", "1.15"]),
            ("pcba06_magsafe_dock_top.png", ["--side", "top", "--quality", "high", "--zoom", "1.05"]),
            ("pcba06_magsafe_dock_bottom_3d.png", ["--side", "bottom", "--rotate", "45,0,-45", "--quality", "high", "--perspective", "--zoom", "1.15"]),
        ],
        "aliases": [
            ("pcba06_magsafe_dock_top.png", "magsafe_dock_3d_top.png"),
            ("pcba06_magsafe_dock_bottom_3d.png", "magsafe_dock_3d_bottom.png"),
            ("pcba06_magsafe_dock_3d.png", "magsafe_dock_3d_perspective.png"),
        ]
    },
    {
        "id": "pcba07",
        "name": "07_smart_keyfob",
        "pcb": os.path.join(BASE_DIR, "hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb"),
        "dest_dir": os.path.join(BASE_DIR, "hardware/kicad_smart_keyfob"),
        "outputs": [
            ("pcba07_smart_keyfob_3d.png", ["--side", "top", "--rotate", "-45,0,45", "--quality", "high", "--perspective", "--zoom", "1.15"]),
            ("pcba07_smart_keyfob_top.png", ["--side", "top", "--quality", "high", "--zoom", "1.05"]),
            ("pcba07_smart_keyfob_bottom_3d.png", ["--side", "bottom", "--rotate", "45,0,-45", "--quality", "high", "--perspective", "--zoom", "1.15"]),
        ],
        "aliases": [
            ("pcba07_smart_keyfob_bottom_3d.png", "pcba07_smart_keyfob_bottom.png"),
        ]
    },
    {
        "id": "pcba08",
        "name": "08_radar_submcu",
        "pcb": os.path.join(BASE_DIR, "hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb"),
        "dest_dir": os.path.join(BASE_DIR, "hardware/kicad_radar_submcu"),
        "outputs": [
            ("pcba08_radar_submcu_3d.png", ["--side", "top", "--rotate", "-45,0,45", "--quality", "high", "--perspective", "--zoom", "1.1"]),
            ("pcba08_radar_submcu_top.png", ["--side", "top", "--quality", "high", "--zoom", "1.05"]),
            ("pcba08_radar_submcu_bottom_3d.png", ["--side", "bottom", "--rotate", "45,0,-45", "--quality", "high", "--perspective", "--zoom", "1.1"]),
        ],
        "aliases": [
            ("pcba08_radar_submcu_top.png", "render_top.png"),
            ("pcba08_radar_submcu_bottom_3d.png", "render_bottom.png"),
        ]
    },
    {
        "id": "pcba09",
        "name": "09_omm_ucs",
        "pcb": os.path.join(BASE_DIR, "hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_pcb"),
        "dest_dir": os.path.join(BASE_DIR, "hardware/kicad_omm_intercom"),
        "outputs": [
            ("pcba09_omm_intercom_3d.png", ["--side", "top", "--rotate", "-45,0,45", "--quality", "high", "--perspective", "--zoom", "1.15"]),
            ("pcba09_omm_intercom_top_3d.png", ["--side", "top", "--rotate", "-45,0,45", "--quality", "high", "--perspective", "--zoom", "1.15"]),
            ("pcba09_omm_intercom_top.png", ["--side", "top", "--quality", "high", "--zoom", "1.05"]),
            ("pcba09_omm_intercom_bottom_3d.png", ["--side", "bottom", "--rotate", "45,0,-45", "--quality", "high", "--perspective", "--zoom", "1.15"]),
            ("pcba09_omm_intercom_bottom.png", ["--side", "bottom", "--quality", "high", "--zoom", "1.05"]),
        ],
        "aliases": []
    },
    {
        "id": "pcba10",
        "name": "10_omm446_ucs",
        "pcb": os.path.join(BASE_DIR, "hardware/kicad_omm446_intercom/openmotorbridge_omm446_intercom.kicad_pcb"),
        "dest_dir": os.path.join(BASE_DIR, "hardware/kicad_omm446_intercom"),
        "outputs": [
            ("pcba10_omm446_intercom_3d.png", ["--side", "top", "--rotate", "-45,0,45", "--quality", "high", "--perspective", "--zoom", "1.15"]),
            ("pcba10_omm446_intercom_top_3d.png", ["--side", "top", "--rotate", "-45,0,45", "--quality", "high", "--perspective", "--zoom", "1.15"]),
            ("pcba10_omm446_intercom_top.png", ["--side", "top", "--quality", "high", "--zoom", "1.05"]),
            ("pcba10_omm446_intercom_bottom_3d.png", ["--side", "bottom", "--rotate", "45,0,-45", "--quality", "high", "--perspective", "--zoom", "1.15"]),
            ("pcba10_omm446_intercom_bottom.png", ["--side", "bottom", "--quality", "high", "--zoom", "1.05"]),
        ],
        "aliases": []
    }
]

def main():
    os.makedirs(DOCS_PCBA_DIR, exist_ok=True)
    print("=" * 70)
    print("🎨 RENDERING ALL OPENMOTORBRIDGE PCBAs & SYNCING TO DOCS")
    print("=" * 70)

    for board in BOARDS:
        pcb = board["pcb"]
        if not os.path.exists(pcb):
            print(f"⚠️  Skipping {board['name']}: PCB file not found at {pcb}")
            continue

        print(f"\n📦 Rendering [{board['name']}]...")
        for fname, render_args in board["outputs"]:
            dest_hw = os.path.join(board["dest_dir"], fname)
            dest_docs = os.path.join(DOCS_PCBA_DIR, fname)
            cmd = [KICAD_CLI, "pcb", "render", "--output", dest_hw] + render_args + [pcb]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0 and os.path.exists(dest_hw):
                shutil.copy2(dest_hw, dest_docs)
                print(f"  ✅ Rendered & copied to docs: {fname}")
            else:
                print(f"  ❌ Failed rendering {fname}: {res.stderr.strip() or res.stdout.strip()}")

        # Copy aliases
        for src_name, alias_name in board.get("aliases", []):
            src_path = os.path.join(board["dest_dir"], src_name)
            alias_path = os.path.join(board["dest_dir"], alias_name)
            if os.path.exists(src_path):
                shutil.copy2(src_path, alias_path)
                print(f"  🔗 Synced alias: {alias_name}")

    print("\n" + "=" * 70)
    print("🎉 ALL PCBA RENDERS COMPLETE & SYNCED TO docs/images/pcba/")
    print("=" * 70)

if __name__ == "__main__":
    main()
