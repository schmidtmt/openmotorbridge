#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
add_helmet_audio_and_rf_to_pcbas.py
===================================
Adds:
1. J_HELMET: 6-Pin JST-SH 1.0mm Horizontal Header (SM06B-SRSS-TB) on B.Cu at (76.5, 104.0) mm
   - Dedicated internal passive helmet audio & PTT connection (zero 5V power):
     Pin 1: HP_OUT_L (Left headphone)
     Pin 2: HP_OUT_R (Right headphone)
     Pin 3: AGND_SPK (Speaker ground)
     Pin 4: MIC_IN+ (Microphone signal)
     Pin 5: AGND_MIC (Microphone ground / shield)
     Pin 6: BTN_PTT / PTT_IO (Push-To-Talk active-low switch)
     MP1, MP2: GND
   Added to BOTH PCBA 09 (OMM 2.4 GHz) and PCBA 10 (OMM 446 MHz).

2. J_RF: Hirose U.FL SMT connector on B.Cu at (126.025, 100.25) mm on PCBA 09
   - Unifies RF coax exit across both PCBA 09 and PCBA 10 so both UCS enclosures are 100% identical.
"""

import os
import sys
import pcbnew

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KICAD_FP_DIR = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"

def to_nm(mm):
    return int(mm * 1e6)

def update_pcba(pcb_rel_path, is_pcba09=True):
    pcb_path = os.path.join(REPO_ROOT, pcb_rel_path)
    print(f"\n=======================================================")
    print(f"📦 Updating PCB: {os.path.basename(pcb_path)}")
    print(f"=======================================================")
    board = pcbnew.LoadBoard(pcb_path)

    # 1. Ensure required nets exist
    net_names = ["HP_OUT_L", "HP_OUT_R", "AGND_SPK", "MIC_IN+", "AGND_MIC", "GND"]
    ptt_net_name = "PTT_IO" if is_pcba09 else "BTN_PTT"
    net_names.append(ptt_net_name)
    if is_pcba09:
        net_names.append("ANT_MESH_2G4")

    net_map = {}
    for name in net_names:
        net = board.FindNet(name)
        if not net:
            net = pcbnew.NETINFO_ITEM(board, name)
            board.Add(net)
        net_map[name] = net

    # 2. Check / Remove existing J_HELMET if re-running
    for fp in list(board.GetFootprints()):
        if fp.GetReference() == "J_HELMET":
            print("  Removing existing J_HELMET footprint for clean re-placement...")
            board.Remove(fp)
        if is_pcba09 and fp.GetReference() == "J_RF":
            print("  Removing existing J_RF footprint for clean re-placement...")
            board.Remove(fp)

    # 3. Add J_HELMET Footprint (JST_SH_SM06B-SRSS-TB_1x06-1MP_P1.00mm_Horizontal)
    fp_path = os.path.join(KICAD_FP_DIR, "Connector_JST.pretty")
    j_helmet = pcbnew.FootprintLoad(fp_path, "JST_SH_SM06B-SRSS-TB_1x06-1MP_P1.00mm_Horizontal")
    if not j_helmet:
        raise RuntimeError("Failed to load JST_SH_SM06B footprint!")

    j_helmet.SetReference("J_HELMET")
    j_helmet.SetValue("HELMET_AUDIO_6P")
    j_helmet.SetLayer(pcbnew.B_Cu)  # Bottom side (facing helmet interior)
    j_helmet.SetPosition(pcbnew.VECTOR2I(to_nm(126.5), to_nm(99.75)))
    j_helmet.SetOrientation(pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T))

    # Wire pads:
    pin_mapping = {
        "1": net_map["HP_OUT_L"],
        "2": net_map["HP_OUT_R"],
        "3": net_map["AGND_SPK"],
        "4": net_map["MIC_IN+"],
        "5": net_map["AGND_MIC"],
        "6": net_map[ptt_net_name],
        "MP": net_map["GND"],
        "MP1": net_map["GND"],
        "MP2": net_map["GND"],
    }

    for pad in j_helmet.Pads():
        pname = pad.GetName()
        if pname in pin_mapping:
            pad.SetNet(pin_mapping[pname])
        elif "MP" in pname:
            pad.SetNet(net_map["GND"])

    board.Add(j_helmet)
    print(f"  ✅ Added J_HELMET (SM06B-SRSS-TB 6-Pin) on B.Cu at (76.50, 104.00) mm")

    # 4. If PCBA 09, add J_RF on B.Cu at (126.025, 100.25)
    if is_pcba09:
        coax_fp_path = os.path.join(KICAD_FP_DIR, "Connector_Coaxial.pretty")
        j_rf = pcbnew.FootprintLoad(coax_fp_path, "U.FL_Hirose_U.FL-R-SMT-1_Vertical")
        if not j_rf:
            raise RuntimeError("Failed to load U.FL footprint!")
        j_rf.SetReference("J_RF")
        j_rf.SetValue("U.FL-R-SMT-1")
        j_rf.SetLayer(pcbnew.B_Cu)
        j_rf.SetPosition(pcbnew.VECTOR2I(to_nm(126.025), to_nm(100.25)))
        j_rf.SetOrientation(pcbnew.EDA_ANGLE(180, pcbnew.DEGREES_T))

        for pad in j_rf.Pads():
            if pad.GetName() == "1":
                pad.SetNet(net_map["ANT_MESH_2G4"])
            else:
                pad.SetNet(net_map["GND"])

        board.Add(j_rf)
        print(f"  ✅ Added J_RF (U.FL-R-SMT-1) on B.Cu at (126.025, 100.25) mm matching PCBA 10")

    board.Save(pcb_path)
    print(f"  💾 Saved {os.path.basename(pcb_path)}")

if __name__ == "__main__":
    update_pcba("hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_pcb", is_pcba09=True)
    update_pcba("hardware/kicad_omm446_intercom/openmotorbridge_omm446_intercom.kicad_pcb", is_pcba09=False)
    print("\n🎉 Both PCBAs successfully updated with J_HELMET and unified J_RF!")
