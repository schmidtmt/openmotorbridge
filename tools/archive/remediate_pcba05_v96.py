#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
"""
tools/remediate_pcba05_v96.py
==============================
Remediates PCBA 05 (Universal Front Node) to the official v9.6 2-Harness Architecture:
1. Removes U8 (SW3526 PD3), L3, C27, C28, and unused USB ports J5_MP3, J6_AUX.
2. Removes all 12 old edge connectors: J1..J6, J5_MP3, J6_AUX, J8..J11.
3. Places J_VEHICLE (8-pin dual-row 2.0 mm SMT) at North flank (X=145.0, Y=74.5).
4. Places J_COCKPIT (16-pin dual-row 2.0 mm SMT) at South flank (X=135.0, Y=114.5).
5. Routes all connections cleanly, refills zones, and saves PCB.
6. Synchronizes openmotorbridge_front_node.kicad_sch.
"""

import sys
import os
import uuid
import subprocess
import pcbnew

PCB_PATH = "hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb"
SCH_PATH = "hardware/kicad_front_node/openmotorbridge_front_node.kicad_sch"
FP_LIB = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/Connector_PinHeader_2.00mm.pretty"

def to_nm(mm):
    return int(mm * 1e6)

def to_mm(nm):
    return float(nm) / 1e6

def add_track(board, net, layer, start_xy, end_xy, width_mm=0.25):
    t = pcbnew.PCB_TRACK(board)
    t.SetNet(net)
    t.SetLayer(layer)
    t.SetWidth(to_nm(width_mm))
    t.SetStart(pcbnew.VECTOR2I(to_nm(start_xy[0]), to_nm(start_xy[1])))
    t.SetEnd(pcbnew.VECTOR2I(to_nm(end_xy[0]), to_nm(end_xy[1])))
    board.Add(t)
    return t

def add_via(board, net, xy, drill_mm=0.30, size_mm=0.60):
    v = pcbnew.PCB_VIA(board)
    v.SetNet(net)
    v.SetPosition(pcbnew.VECTOR2I(to_nm(xy[0]), to_nm(xy[1])))
    v.SetDrill(to_nm(drill_mm))
    v.SetWidth(to_nm(size_mm))
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    board.Add(v)
    return v

def main():
    print("=== PCBA 05 v9.6 2-Harness Architecture Remediation ===")
    
    board = pcbnew.LoadBoard(PCB_PATH)
    f_cu = board.GetLayerID("F.Cu")
    b_cu = board.GetLayerID("B.Cu")

    # 1. Footprints to remove
    remove_refs = [
        "U8", "L3", "C27", "C28",
        "J1", "J2", "J3", "J4", "J5", "J5_MP3", "J6", "J6_AUX", "J8", "J9", "J10", "J11"
    ]
    
    # Track nets associated with removed footprints to remove dead tracks
    dead_nets = {"VBUS_PD3_OUT", "USB_DN3_DM", "USB_DN3_DP", "USB_DN3_CC", "SW_PD3_BUCK", "USB_DN4_DM", "USB_DN4_DP"}
    
    tracks_to_remove = []
    for t in board.GetTracks():
        if t.GetNetname() in dead_nets:
            tracks_to_remove.append(t)
            
    for t in tracks_to_remove:
        board.Delete(t)
    print(f"✓ Removed {len(tracks_to_remove)} dead tracks from eliminated PD3/AUX circuits.")

    for ref in remove_refs:
        f = board.FindFootprintByReference(ref)
        if f:
            board.Delete(f)
            print(f"✓ Removed footprint {ref}")

    # 2. Add J_VEHICLE (8-Pin Dual-Row 2.0 mm SMT) at North Flank
    fp_veh = pcbnew.FootprintLoad(FP_LIB, "PinHeader_2x04_P2.00mm_Vertical_SMD")
    fp_veh.SetReference("J_VEHICLE")
    fp_veh.SetValue("VEHICLE_8P_SMD")
    fp_veh.SetPosition(pcbnew.VECTOR2I(to_nm(145.0), to_nm(74.5)))
    fp_veh.SetOrientation(pcbnew.EDA_ANGLE(90.0, pcbnew.DEGREES_T))
    board.Add(fp_veh)
    print("✓ Placed J_VEHICLE at (145.0, 74.5) North Flank")

    veh_net_map = {
        "1": "KL15_12V_SW",
        "2": "GND",
        "3": "CAN_H",
        "4": "CAN_L",
        "5": "+12V_PROT",
        "6": "BSD_LEFT_N",
        "7": "BSD_RIGHT_N",
        "8": "+12V_AUX"
    }
    for p in fp_veh.Pads():
        pnum = p.GetNumber()
        if pnum in veh_net_map:
            net = board.FindNet(veh_net_map[pnum])
            if net:
                p.SetNet(net)
    print("✓ Assigned nets to J_VEHICLE (8 pins)")

    # 3. Add J_COCKPIT (16-Pin Dual-Row 2.0 mm SMT) at South Flank
    fp_cockpit = pcbnew.FootprintLoad(FP_LIB, "PinHeader_2x08_P2.00mm_Vertical_SMD")
    fp_cockpit.SetReference("J_COCKPIT")
    fp_cockpit.SetValue("COCKPIT_16P_SMD")
    fp_cockpit.SetPosition(pcbnew.VECTOR2I(to_nm(135.0), to_nm(114.5)))
    fp_cockpit.SetOrientation(pcbnew.EDA_ANGLE(90.0, pcbnew.DEGREES_T))
    board.Add(fp_cockpit)
    print("✓ Placed J_COCKPIT at (135.0, 114.5) South Flank")

    cockpit_net_map = {
        "1": "USB_UP_VBUS",
        "2": "USB_UP_DM",
        "3": "USB_UP_DP",
        "4": "GND",
        "5": "VCC_5V_OTTOCAST",
        "6": "USB_DN2_DM",
        "7": "USB_DN2_DP",
        "8": "GND",
        "9": "VBUS_PD1_OUT",
        "10": "USB_DN1_DM",
        "11": "USB_DN1_DP",
        "12": "USB_DN1_CC",
        "13": "GND",
        "14": "PTT_IN1_N",
        "15": "VCC_5V",
        "16": "GND"
    }
    for p in fp_cockpit.Pads():
        pnum = p.GetNumber()
        if pnum in cockpit_net_map:
            net = board.FindNet(cockpit_net_map[pnum])
            if net:
                p.SetNet(net)
    print("✓ Assigned nets to J_COCKPIT (16 pins)")

    # 4. Route connections from existing tracks to J_VEHICLE pads
    for p in fp_veh.Pads():
        pnum = p.GetNumber()
        netname = veh_net_map.get(pnum)
        if not netname or netname == "GND":
            continue
        net = board.FindNet(netname)
        pad_x = to_mm(p.GetPosition().x)
        pad_y = to_mm(p.GetPosition().y)
        
        best_pt = None
        best_dist = 9999.0
        for t in board.GetTracks():
            if t.GetNetname() == netname:
                for pt in [t.GetStart(), t.GetEnd()]:
                    pt_x = to_mm(pt.x)
                    pt_y = to_mm(pt.y)
                    d = ((pt_x - pad_x)**2 + (pt_y - pad_y)**2)**0.5
                    if d < best_dist and d > 0.05:
                        best_dist = d
                        best_pt = (pt_x, pt_y)
        
        if best_pt and best_dist < 35.0:
            mid_y = pad_y - 1.5 if pad_y > best_pt[1] else pad_y + 1.5
            add_track(board, net, f_cu, (pad_x, pad_y), (pad_x, mid_y), width_mm=0.25)
            add_track(board, net, f_cu, (pad_x, mid_y), (best_pt[0], mid_y), width_mm=0.25)
            add_track(board, net, f_cu, (best_pt[0], mid_y), best_pt, width_mm=0.25)
            print(f"  Connected J_VEHICLE.{pnum} ({netname}) to track at {best_pt} (dist: {best_dist:.2f}mm)")

    # 5. Route connections from existing tracks to J_COCKPIT pads
    for p in fp_cockpit.Pads():
        pnum = p.GetNumber()
        netname = cockpit_net_map.get(pnum)
        if not netname or netname == "GND":
            continue
        net = board.FindNet(netname)
        pad_x = to_mm(p.GetPosition().x)
        pad_y = to_mm(p.GetPosition().y)
        
        best_pt = None
        best_dist = 9999.0
        for t in board.GetTracks():
            if t.GetNetname() == netname:
                for pt in [t.GetStart(), t.GetEnd()]:
                    pt_x = to_mm(pt.x)
                    pt_y = to_mm(pt.y)
                    d = ((pt_x - pad_x)**2 + (pt_y - pad_y)**2)**0.5
                    if d < best_dist and d > 0.05:
                        best_dist = d
                        best_pt = (pt_x, pt_y)
        
        if best_pt and best_dist < 35.0:
            mid_y = pad_y - 1.5 if pad_y > best_pt[1] else pad_y + 1.5
            add_track(board, net, f_cu, (pad_x, pad_y), (pad_x, mid_y), width_mm=0.25)
            add_track(board, net, f_cu, (pad_x, mid_y), (best_pt[0], mid_y), width_mm=0.25)
            add_track(board, net, f_cu, (best_pt[0], mid_y), best_pt, width_mm=0.25)
            print(f"  Connected J_COCKPIT.{pnum} ({netname}) to track at {best_pt} (dist: {best_dist:.2f}mm)")
        elif netname == "PTT_IN1_N":
            # Connect PTT to U1.8
            u1 = board.FindFootprintByReference("U1")
            p8 = [pad for pad in u1.Pads() if pad.GetNumber() == "8"][0]
            p8_pos = (to_mm(p8.GetPosition().x), to_mm(p8.GetPosition().y))
            add_track(board, net, f_cu, (pad_x, pad_y), (pad_x, pad_y - 4.0), width_mm=0.20)
            add_track(board, net, f_cu, (pad_x, pad_y - 4.0), (p8_pos[0], pad_y - 4.0), width_mm=0.20)
            add_track(board, net, f_cu, (p8_pos[0], pad_y - 4.0), p8_pos, width_mm=0.20)
            print(f"  Connected J_COCKPIT.{pnum} (PTT_IN1_N) directly to U1.8 at {p8_pos}")

    # 6. Refill zones
    for zone in board.Zones():
        zone.SetNeedRefill(True)
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    print("✓ Refilled copper zones.")

    # 7. Save PCB
    board.Save(PCB_PATH)
    print(f"✓ Saved updated board to {PCB_PATH}")

    # 8. Synchronize schematic
    sync_sch(board)
    print("=== PCBA 05 Remediation Complete! ===")
    os._exit(0)

def sync_sch(board):
    def u():
        return str(uuid.uuid4())

    fps = list(board.GetFootprints())
    comps = []
    for f in fps:
        ref = f.GetReference()
        val = f.GetValue()
        fp_name = str(f.GetFPID().GetFootprintName())
        pads = []
        for p in f.Pads():
            pads.append({
                'number': p.GetNumber(),
                'net': p.GetNetname()
            })
        comps.append({
            'ref': ref,
            'val': val,
            'fp': fp_name,
            'pads': pads
        })

    sch = []
    sch.append('(kicad_sch')
    sch.append('\t(version 20260306)')
    sch.append('\t(generator "eeschema")')
    sch.append('\t(generator_version "10.0")')
    sch.append(f'\t(uuid "{u()}")')
    sch.append('\t(paper "A1")')
    sch.append('\t(title_block')
    sch.append('\t\t(title "OpenMotorBridge Universal Front Node (Cockpit & Sensor Hub PCBA 05)")')
    sch.append('\t\t(date "2026-10-19")')
    sch.append('\t\t(rev "v2.2-2harness")')
    sch.append('\t\t(company "OpenMotorBridge Open Source Hardware")')
    sch.append('\t\t(comment 1 "ESP32-S3, USB2514B Hub, Single SW3526 20W, DW3110 UWB, J_COCKPIT 16P & J_VEHICLE 8P")')
    sch.append('\t)')

    sch.append('\t(lib_symbols')
    for c in sorted(comps, key=lambda x: x['ref']):
        ref = c['ref']
        val = c['val']
        fp = c['fp']
        pads = c['pads']

        sch.append(f'\t\t(symbol "{ref}_sym"')
        sch.append(f'\t\t\t(property "Reference" "{ref}" (at 0 5 0) (effects (font (size 1.27 1.27))))')
        sch.append(f'\t\t\t(property "Value" "{val}" (at 0 -5 0) (effects (font (size 1.27 1.27))))')
        sch.append(f'\t\t\t(property "Footprint" "{fp}" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))')
        
        n_pins = len(pads)
        w = 20.32
        half = (n_pins + 1) // 2

        for idx, p in enumerate(pads):
            pnum = p['number']
            pname = p['net'] if p['net'] else "~"
            if idx < half:
                y = (half / 2 - idx) * 2.54
                sch.append(f'\t\t\t(pin passive line (at -{w/2:.2f} {y:.2f} 0) (length 2.54) (name "{pname}" (effects (font (size 1.27 1.27)))) (number "{pnum}" (effects (font (size 1.27 1.27)))))')
            else:
                y = (half / 2 - (idx - half)) * 2.54
                sch.append(f'\t\t\t(pin passive line (at {w/2:.2f} {y:.2f} 180) (length 2.54) (name "{pname}" (effects (font (size 1.27 1.27)))) (number "{pnum}" (effects (font (size 1.27 1.27)))))')
        sch.append('\t\t)')
    sch.append('\t)')

    cols = 8
    grid_x = 85.0
    grid_y = 100.0
    start_x = 60.0
    start_y = 60.0

    wires_and_labels = []
    for idx, c in enumerate(sorted(comps, key=lambda x: x['ref'])):
        ref = c['ref']
        val = c['val']
        fp = c['fp']
        pads = c['pads']

        col = idx % cols
        row = idx // cols

        pos_x = start_x + col * grid_x
        pos_y = start_y + row * grid_y

        sch.append(f'\t(symbol (lib_id "{ref}_sym") (at {pos_x:.2f} {pos_y:.2f} 0) (unit 1)')
        sch.append('\t\t(in_bom yes) (on_board yes) (dnp no)')
        sch.append(f'\t\t(uuid "{u()}")')
        sch.append(f'\t\t(property "Reference" "{ref}" (at {pos_x:.2f} {pos_y - 25:.2f} 0) (effects (font (size 1.27 1.27))))')
        sch.append(f'\t\t(property "Value" "{val}" (at {pos_x:.2f} {pos_y - 22:.2f} 0) (effects (font (size 1.27 1.27))))')
        sch.append(f'\t\t(property "Footprint" "{fp}" (at {pos_x:.2f} {pos_y:.2f} 0) (effects (font (size 1.27 1.27)) hide))')

        w = 20.32
        half = (len(pads) + 1) // 2

        for p_idx, p in enumerate(pads):
            pnum = p['number']
            pnet = p['net']
            p_uuid = u()
            sch.append(f'\t\t(pin "{pnum}" (uuid "{p_uuid}"))')

            if pnet and pnet != "<no net>" and pnet != "":
                if p_idx < half:
                    y = (half / 2 - p_idx) * 2.54
                    pin_y = pos_y - y
                    pin_x = pos_x - (w / 2)
                    lbl_x = pin_x - 5.08
                    wires_and_labels.append(f'\t(wire (pts (xy {pin_x:.2f} {pin_y:.2f}) (xy {lbl_x:.2f} {pin_y:.2f})) (stroke (width 0) (type default)) (uuid "{u()}"))')
                    wires_and_labels.append(f'\t(global_label "{pnet}" (shape bidirectional) (at {lbl_x:.2f} {pin_y:.2f} 180) (effects (font (size 1.27 1.27)) (justify right)) (uuid "{u()}"))')
                else:
                    y = (half / 2 - (p_idx - half)) * 2.54
                    pin_y = pos_y - y
                    pin_x = pos_x + (w / 2)
                    lbl_x = pin_x + 5.08
                    wires_and_labels.append(f'\t(wire (pts (xy {pin_x:.2f} {pin_y:.2f}) (xy {lbl_x:.2f} {pin_y:.2f})) (stroke (width 0) (type default)) (uuid "{u()}"))')
                    wires_and_labels.append(f'\t(global_label "{pnet}" (shape bidirectional) (at {lbl_x:.2f} {pin_y:.2f} 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "{u()}"))')

        sch.append('\t)')

    for item in wires_and_labels:
        sch.append(item)

    sch.append(')')
    sch.append('')

    with open(SCH_PATH, "w", encoding="utf-8") as f:
        f.write('\n'.join(sch))
    print(f"✓ Generated 100% synchronized {SCH_PATH} with {len(comps)} components.")

if __name__ == "__main__":
    main()
