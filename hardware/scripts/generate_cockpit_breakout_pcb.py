#!/usr/bin/env python3
"""
hardware/scripts/generate_cockpit_breakout_pcb.py
Redirects to / runs tools/build_cockpit_breakout_pcba.py
"""
import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BUILD_SCRIPT = os.path.join(SCRIPT_DIR, "..", "..", "tools", "build_cockpit_breakout_pcba.py")
KICAD_PYTHON = "/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3"

def main():
    cmd = [KICAD_PYTHON, BUILD_SCRIPT]
    res = subprocess.run(cmd)
    sys.exit(res.returncode)

if __name__ == "__main__":
    main()
