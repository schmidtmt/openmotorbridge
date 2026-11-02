#!/usr/bin/env python3
"""
OpenMotorBridge - CAD 3D Render & STL Master Tool
=================================================
Automated rendering and build script for all OpenMotorBridge CAD enclosures
and mechanical components using OpenSCAD.
Outputs are directly placed in `docs/images/cad/` and `hardware/cad/stl/`.

Usage:
    python3 tools/render_all_cad.py                      # Renders all 3D CAD images for documentation
    python3 tools/render_all_cad.py <filter>             # Render only targets matching filter (e.g. front_node, glovebox, pod)
    python3 tools/render_all_cad.py --stls               # Compile production STLs
    python3 tools/render_all_cad.py --all                # Compile both STLs and renders
    python3 tools/render_all_cad.py --help               # Show help options
"""

import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
MASTER_BUILDER = os.path.join(REPO_ROOT, "hardware/scripts/build_cad_from_openscad.py")

def main():
    if not os.path.exists(MASTER_BUILDER):
        print(f"ERROR: Master CAD builder script not found at {MASTER_BUILDER}")
        sys.exit(1)

    args = sys.argv[1:]
    
    if "--help" in args or "-h" in args:
        print(__doc__)
        sys.exit(0)

    forward_args = []
    has_mode_flag = False
    
    for arg in args:
        if arg == "--all":
            has_mode_flag = True
        elif arg == "--stls":
            forward_args.append("--stls-only")
            has_mode_flag = True
        elif arg == "--renders":
            forward_args.append("--renders-only")
            has_mode_flag = True
        else:
            forward_args.append(arg)

    # By default, render_all_cad renders images for documentation
    if not has_mode_flag and not any(a.startswith("--") for a in forward_args):
        forward_args.insert(0, "--renders-only")

    cmd = [sys.executable, MASTER_BUILDER] + forward_args
    res = subprocess.run(cmd)
    sys.exit(res.returncode)

if __name__ == '__main__':
    main()
