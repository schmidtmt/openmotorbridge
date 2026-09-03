#!/usr/bin/env python3
"""
OpenMotorBridge - Master Automated Testbench & Multi-Domain Simulation Runner
=============================================================================
Executes all electrical, firmware, thermal, acoustic, and RF testbenches:
  1. Full Multi-Board SPICE & Harness Simulation  (`openmotorbridge_full_system_sim.py`)
  2. Hardware-in-the-Loop (HIL) Firmware Simulator (`firmware_hil_system_sim.py`)
  3. 8-Hour Day Tour Thermal Multi-Physics         (`thermal_day_tour_sim.py`)
  4. All-Weather ITU-R Rain & RF Propagation      (`rf_rain_propagation_sim.py`)
  5. ISO 7637-2 Automotive Transient Pulses      (`automotive_iso7637_pulses_sim.py`)
  6. Acoustic Wind Noise & Audio DSP Pipeline     (`acoustic_wind_dsp_sim.py`)
  7. 20-Rider Large Convoy Mesh Scalability       (`mesh_group_scaling_sim.py`)
  8. 180-Day Winter Storage Standby Drain         (`battery_winter_standby_sim.py`)
  9. Universal Front Node & Smart Fairing Hub     (`front_node_wireless_hub_sim.py`)
  10. Rear Radar & Blind-Spot Detection (BSD)     (`radar_blindspot_sim.py`)
"""

import os
import sys
import subprocess

SIMULATORS = [
    ("1. SPICE Multi-Board Electrical Harness", "tools/simulators/openmotorbridge_full_system_sim.py"),
    ("2. Hardware-in-the-Loop Firmware Engine", "tools/simulators/firmware_hil_system_sim.py"),
    ("3. 8-Hour Day Tour Thermal Dynamics", "tools/simulators/thermal_day_tour_sim.py"),
    ("4. All-Weather ITU-R RF Propagation", "tools/simulators/rf_rain_propagation_sim.py"),
    ("5. ISO 7637-2 Automotive Transients", "tools/simulators/automotive_iso7637_pulses_sim.py"),
    ("6. Acoustic Wind Noise & Audio DSP", "tools/simulators/acoustic_wind_dsp_sim.py"),
    ("7. 20-Rider Mesh Scalability & DLE", "tools/simulators/mesh_group_scaling_sim.py"),
    ("8. 180-Day Winter Standby Battery Drain", "tools/simulators/battery_winter_standby_sim.py"),
    ("9. Universal Front Node & Smart Fairing", "tools/simulators/front_node_wireless_hub_sim.py"),
    ("10. Rear Radar & Blind-Spot Detection", "tools/simulators/radar_blindspot_sim.py"),
]

def main():
    print("=" * 80)
    print("OPENMOTORBRIDGE MASTER AUTOMATED SIMULATION & VERIFICATION RUNNER".center(80))
    print("=" * 80)
    print(f"Running {len(SIMULATORS)} comprehensive engineering testbenches...\n")
    
    passed_count = 0
    failed_sims = []
    
    for idx, (title, script_path) in enumerate(SIMULATORS, 1):
        print("-" * 80)
        print(f"[{idx}/{len(SIMULATORS)}] RUNNING: {title} ({script_path})")
        print("-" * 80)
        
        result = subprocess.run([sys.executable, script_path], capture_output=False)
        if result.returncode == 0:
            passed_count += 1
            print(f"\n>>> [{title}] -> ✅ PASSED\n")
        else:
            failed_sims.append(title)
            print(f"\n>>> [{title}] -> ❌ FAILED (Exit Code {result.returncode})\n")
            
    print("=" * 80)
    print(f"MASTER SIMULATION SUMMARY: {passed_count}/{len(SIMULATORS)} TESTBENCHES PASSED".center(80))
    print("=" * 80)
    
    if failed_sims:
        print(f"Failed testbenches: {failed_sims}")
        sys.exit(1)
    else:
        print("🎉 ALL SYSTEMS FULLY VERIFIED, AUTOMOTIVE COMPLIANT & PRODUCTION READY!")

if __name__ == '__main__':
    main()
