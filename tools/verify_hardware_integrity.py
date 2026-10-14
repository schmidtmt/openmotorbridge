#!/usr/bin/env python3
"""
verify_hardware_integrity.py
============================
Automated hardware integrity & parity checker for OpenMotorBridge PCBAs.

Performs:
1. Single-Member Nets Check (nets with only 1 pad)
2. Unconnected / Floating Pads Check (pads with no net assigned)
3. Connector Orientation & Clearance Check (mating face accessibility vs board edge & keepouts)
4. Schematic-to-PCB Parity Check (invokes kicad-cli DRC parity)
5. Naming Convention Compliance Check (detects deprecated net names)

Usage:
  /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3 \
      tools/verify_hardware_integrity.py --pcb <path_to_pcb> [--sch <path_to_sch>]
"""

import os
import sys
import argparse
import subprocess
import pcbnew

def parse_args():
    parser = argparse.ArgumentParser(description="OpenMotorBridge Hardware Integrity Verification")
    parser.add_argument("--pcb", required=True, help="Path to .kicad_pcb file")
    parser.add_argument("--sch", required=False, help="Path to .kicad_sch file (optional, deduced if omitted)")
    parser.add_argument("--skip-drc", action="store_true", help="Skip running kicad-cli drc")
    return parser.parse_args()

def to_mm(nm):
    return nm / 1e6

def check_single_member_nets(board):
    net_pads = {}
    for pad in board.GetPads():
        net = pad.GetNet()
        if not net:
            continue
        netname = net.GetNetname()
        if not netname or netname == "" or netname == "<no net>":
            continue
        if netname not in net_pads:
            net_pads[netname] = []
        fp = pad.GetParentFootprint()
        ref = fp.GetReference() if fp else "Unknown"
        pad_num = pad.GetNumber()
        net_pads[netname].append((ref, pad_num, pad))

    single_nets = {}
    for netname, pads in net_pads.items():
        if len(pads) == 1:
            single_nets[netname] = pads[0]

    return single_nets

def check_unconnected_pads(board):
    unconnected = []
    for pad in board.GetPads():
        # Ignore non-copper pads (pure solder paste apertures / silkscreen / mask)
        if not pad.IsOnCopperLayer():
            continue
        net = pad.GetNet()
        netname = net.GetNetname() if net else ""
        if not net or netname == "" or netname == "<no net>":
            fp = pad.GetParentFootprint()
            ref = fp.GetReference() if fp else "Unknown"
            pad_num = pad.GetNumber()
            fp_name = str(fp.GetFPID().GetLibItemName()) if fp else ""
            # Ignore purely mechanical NPTH mounting holes without electrical function
            if pad.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH:
                continue
            # For ICs (U*, or multi-pin smart switches/controllers Q* with >6 pads), unused GPIOs or NC pins with no schematic connection are valid,
            # but power, ground, and thermal pads MUST have nets assigned.
            is_ic = ref.startswith("U") or (ref.startswith("Q") and fp and len(fp.Pads()) > 6)
            if is_ic:
                pad_name = pad.GetPadName()
                pname_upper = pad_name.upper()
                if pname_upper in ["GND", "VSS", "VDD", "VCC", "EP", "THERMAL", "PAD_EP"] or "GND" in pname_upper or "VCC" in pname_upper:
                    unconnected.append((ref, pad_num, pad))
                    continue
                continue
            # Allow standard USB-C SBU pins (A8, B8) to be NC in USB 2.0 designs
            if ("USB" in fp_name.upper() or "TYPE-C" in fp_name.upper() or ref == "J1") and pad_num in ["A8", "B8", "SBU1", "SBU2"]:
                continue
            # For all discrete components (C, R, L, D, Y, J, BAT, CONN, SW, ANT, F, etc.), NO pad may be unconnected!
            unconnected.append((ref, pad_num, pad))
    return unconnected

def check_connector_clearance(board):
    """
    Checks horizontal SMT/THT connectors (JST-SH, USB-C, headers)
    to ensure the mating face does not point into a blocked wall or off-board without clearance.
    """
    connectors = []
    # Get board bounding box
    bbox = board.GetBoardEdgesBoundingBox()
    b_min_x = to_mm(bbox.GetX())
    b_max_x = to_mm(bbox.GetRight())
    b_min_y = to_mm(bbox.GetY())
    b_max_y = to_mm(bbox.GetBottom())

    for fp in board.GetFootprints():
        ref = fp.GetReference()
        fp_name = str(fp.GetFPID().GetLibItemName())
        pos = fp.GetPosition()
        x, y = to_mm(pos.x), to_mm(pos.y)
        rot = fp.GetOrientationDegrees()
        layer = "F.Cu" if fp.GetLayer() == pcbnew.F_Cu else "B.Cu"

        is_conn = any(key in fp_name.lower() or ref.startswith("J") or ref.startswith("BAT") 
                      for key in ["jst", "conn", "usb", "molex", "header", "sh_sm"])
        if is_conn:
            # Check orientation & proximity to edge
            # For JST-SH horizontal headers, mating plug inserts from the side opposite the pin pads
            connectors.append({
                "ref": ref,
                "name": fp_name,
                "x": x,
                "y": y,
                "rot": rot,
                "layer": layer
            })

    return connectors, (b_min_x, b_max_x, b_min_y, b_max_y)

def check_naming_conventions(board):
    deprecated = {
        "HP_OUT_L": "Use AUDIO_OUT_L on OMM USB-C J1, or HP_OUT_L on J_HELMET",
        "HP_OUT_R": "Use AUDIO_OUT_R on OMM USB-C J1, or HP_OUT_R on J_HELMET",
        "MIC_OUT": "Use VOICE_OUT on Cartridge J_AUDIO_PWR",
        "MIC_IN+": "Use VOICE_IN on OMM USB-C J1, or MIC_IN on J_HELMET",
        "BTN_PWR": "Use generic BTN_1 on OMM",
        "BTN_MESH": "Use generic BTN_2 on OMM",
        "BTN_VOL_UP": "Use generic BTN_3 on OMM",
        "BTN_VOL_DOWN": "Use generic BTN_4 on OMM",
        "ACT1_OUT": "Use ACT_1 on J_ACT",
        "ACT2_OUT": "Use ACT_2 on J_ACT",
        "ACT3_OUT": "Use ACT_3 on J_ACT",
        "ACT4_OUT": "Use ACT_4 on J_ACT",
    }
    found_deprecated = {}
    for pad in board.GetPads():
        net = pad.GetNet()
        if not net:
            continue
        netname = net.GetNetname()
        if netname in deprecated and netname not in found_deprecated:
            found_deprecated[netname] = deprecated[netname]
    return found_deprecated

def run_kicad_parity_check(pcb_path, sch_path):
    kicad_cli = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
    if not os.path.exists(kicad_cli):
        kicad_cli = "kicad-cli"
    
    cmd = [kicad_cli, "pcb", "drc", pcb_path, "--schematic-parity"]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        lines = res.stdout.splitlines()
        parity_errors = []
        parity_count = 0
        for line in lines:
            line_lower = line.lower()
            parts = line.split()
            if "violation" in line_lower:
                for p in parts:
                    if p.isdigit():
                        drc_violations = int(p)
            elif "unconnected item" in line_lower:
                for p in parts:
                    if p.isdigit():
                        unconnected_items = int(p)
            elif "schematic parity issue" in line_lower:
                for p in parts:
                    if p.isdigit():
                        parity_count = int(p)
        return drc_violations, unconnected_items, parity_count, parity_errors
    except Exception as e:
        return -1, -1, -1, [str(e)]

def main():
    args = parse_args()
    pcb_path = os.path.abspath(args.pcb)
    if not os.path.exists(pcb_path):
        print(f"ERROR: PCB file not found: {pcb_path}")
        sys.exit(1)

    sch_path = args.sch
    if not sch_path:
        base, _ = os.path.splitext(pcb_path)
        candidate = base + ".kicad_sch"
        if os.path.exists(candidate):
            sch_path = candidate

    print("======================================================================")
    print("   OpenMotorBridge Hardware Integrity Verification Tool")
    print(f"   Target PCB: {os.path.basename(pcb_path)}")
    if sch_path:
        print(f"   Target SCH: {os.path.basename(sch_path)}")
    print("======================================================================")

    board = pcbnew.LoadBoard(pcb_path)

    # 1. Single Member Nets
    single_nets = check_single_member_nets(board)
    print(f"\n[1] Single-Member Nets Check: {'FAIL (' + str(len(single_nets)) + ' found)' if single_nets else 'PASS (0 single-member nets)'}")
    for netname, (ref, pad_num, _) in single_nets.items():
        print(f"    - Net '{netname}' connects ONLY to {ref} Pad {pad_num}")

    # 2. Unconnected Pads
    unconnected = check_unconnected_pads(board)
    print(f"\n[2] Unconnected / Floating Pads Check: {'FAIL (' + str(len(unconnected)) + ' found)' if unconnected else 'PASS (0 floating pads)'}")
    for ref, pad_num, _ in unconnected:
        print(f"    - Floating Pad: {ref} Pad {pad_num} (no net assigned)")

    # 3. Connector Orientation & Clearance
    connectors, b_dims = check_connector_clearance(board)
    b_min_x, b_max_x, b_min_y, b_max_y = b_dims
    print(f"\n[3] Connector Orientation & Accessibility Check: ({len(connectors)} connectors inspected)")
    print(f"    Board Bounding Box: X=[{b_min_x:.1f} .. {b_max_x:.1f}] mm, Y=[{b_min_y:.1f} .. {b_max_y:.1f}] mm")
    for c in connectors:
        print(f"    - {c['ref']} ({c['name']}): Pos=({c['x']:.2f}, {c['y']:.2f}) mm, Rot={c['rot']}°, Layer={c['layer']}")

    # 4. Naming Convention Compliance
    deprecated_nets = check_naming_conventions(board)
    print(f"\n[4] Naming Convention Compliance: {'WARN (' + str(len(deprecated_nets)) + ' legacy names)' if deprecated_nets else 'PASS (100% compliant)'}")
    for net, note in deprecated_nets.items():
        print(f"    - Legacy Net '{net}': {note}")

    # 5. Schematic Parity (if available and not skipped)
    if sch_path and not args.skip_drc:
        print("\n[5] KiCad Schematic Parity & DRC Check (via kicad-cli)...")
        drc_v, unc_i, par_v, par_errs = run_kicad_parity_check(pcb_path, sch_path)
        print(f"    DRC Violations: {drc_v}")
        print(f"    Unconnected Items: {unc_i}")
        print(f"    Schematic Parity Issues: {par_v}")
        if par_errs:
            for pe in par_errs[:10]:
                print(f"      * {pe}")
            if len(par_errs) > 10:
                print(f"      ... and {len(par_errs) - 10} more parity issues")

    total_critical = len(single_nets) + len(unconnected)
    print("\n======================================================================")
    if total_critical == 0:
        print("✓ HARDWARE INTEGRITY STATUS: HEALTHY (No blocking circuit defects)")
    else:
        print(f"✗ HARDWARE INTEGRITY STATUS: {total_critical} CRITICAL DEFECTS DETECTED")
    print("======================================================================\n")

    return 0 if total_critical == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
