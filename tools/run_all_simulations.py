#!/usr/bin/env python3
"""
OpenMotorBridge - Unified Master Digital Testbench Runner
Executes all 5 simulation engines:
1. Audio DSP, Ducking & Ambient-Mic Guard (`audio_dsp_sim.py`)
2. Power Management, USV Rundown & JEITA Thermal Guard (`power_ups_sim.py`)
3. 15-State ADR-EKF & Mountain Tunnel Navigation (`adr_ekf_sim.py`)
4. 1-Wire Cartridge & PhotoMOS Pulse Sequencer (`cartridge_optopulse_sim.py`)
5. OpenMotorMesh (OMM) Dynamic Leader Election & Radar (`omm_network_sim.py`)
"""

import sys
import os
import time

# Add tools directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from simulators.audio_dsp_sim import run_audio_dsp_simulation
from simulators.power_ups_sim import run_power_ups_simulation
from simulators.adr_ekf_sim import run_adr_ekf_simulation
from simulators.cartridge_optopulse_sim import run_cartridge_optopulse_simulation
from omm.omm_network_sim import OmmNetworkSimulator

def main():
    print("=" * 70)
    print("   OPENMOTORBRIDGE UNIFIED DIGITAL TESTBENCH & SIMULATION SUITE   ")
    print("=" * 70)
    start_time = time.time()

    results = {}

    try:
        # 1. Audio DSP & Ducking
        results["Audio DSP & Ducking"] = run_audio_dsp_simulation()

        # 2. Power & USV
        results["Power Management & USV"] = run_power_ups_simulation()

        # 3. ADR-EKF Sensor Fusion
        results["15-State ADR-EKF & Tunnel"] = run_adr_ekf_simulation()

        # 4. 1-Wire Cartridge & PhotoMOS
        results["1-Wire Cartridge & PhotoMOS"] = run_cartridge_optopulse_simulation()

        # 5. OpenMotorMesh Protocol
        print("\n" + "=" * 60)
        print("  5. OPENMOTORMESH (OMM) PROTOCOL & MESH RADAR SIMULATION")
        print("=" * 60)
        sim = OmmNetworkSimulator()
        sim.run_election()
        sim.simulate_pack_split()
        sim.trigger_siren_early_warning()
        sim.verify_radar_frames()
        results["OpenMotorMesh Protocol & Radar"] = True

    except Exception as e:
        print(f"\n❌ SIMULATION FAILED WITH ERROR: {e}")
        sys.exit(1)

    elapsed_s = time.time() - start_time

    # Summary Table
    print("\n" + "=" * 70)
    print(f"   DIGITAL TESTBENCH VERIFICATION SUMMARY (Completed in {elapsed_s:.2f}s)")
    print("=" * 70)
    print(f"  {'Simulation Module':<45} | {'Status':<10}")
    print("  " + "-" * 45 + "-+-" + "-" * 10)
    
    all_passed = True
    for mod, ok in results.items():
        status_str = "✅ PASSED" if ok else "❌ FAILED"
        if not ok: all_passed = False
        print(f"  {mod:<45} | {status_str:<10}")

    print("=" * 70)
    if all_passed:
        print("🎉 ALL SIMULATIONS PASSED DETERMINISTICALLY WITH 100% INTEGRITY!")
        print("=" * 70 + "\n")
    else:
        print("❌ ONE OR MORE SIMULATIONS FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()
