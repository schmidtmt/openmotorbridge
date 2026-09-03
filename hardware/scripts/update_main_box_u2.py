#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
import pcbnew

PCB_PATH = "/Users/schmidtm/openMotorBridge/hardware/kicad_main_box/openmotorbridge_main.kicad_pcb"
FP_LIB = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/RF_Module.pretty"

def swap_u2():
    print(f"Loading PCB: {PCB_PATH}")
    board = pcbnew.LoadBoard(PCB_PATH)

    fp_u2_old = None
    for fp in board.Footprints():
        if fp.GetReference() == "U2":
            fp_u2_old = fp
            break

    if not fp_u2_old:
        print("U2 not found!")
        return

    # Load new ESP32-S3-WROOM-1U footprint
    fp_u2_new = pcbnew.FootprintLoad(FP_LIB, "ESP32-S3-WROOM-1U")
    fp_u2_new.SetReference("U2")
    fp_u2_new.SetValue("ESP32-S3-WROOM-1U-N16R8")
    fp_u2_new.SetPosition(pcbnew.VECTOR2I(int(149.5 * 1e6), int(89.15 * 1e6)))

    # Map pad nets
    old_pad_nets = {p.GetNumber(): p.GetNet() for p in fp_u2_old.Pads()}
    for p_new in fp_u2_new.Pads():
        num = p_new.GetNumber()
        if num in old_pad_nets:
            p_new.SetNet(old_pad_nets[num])

    # Assign 3D model: ESP32-S3-WROOM-1.step with offset (0, 3.15, 0)
    fp_u2_new.Models().clear()
    m = pcbnew.FP_3DMODEL()
    m.m_Filename = "${KICAD10_3DMODEL_DIR}/RF_Module.3dshapes/ESP32-S3-WROOM-1.step"
    m.m_Offset = pcbnew.VECTOR3D(0.0, -3.15, 0.0)
    m.m_Scale = pcbnew.VECTOR3D(1.0, 1.0, 1.0)
    m.m_Show = True
    fp_u2_new.Add3DModel(m)

    board.Remove(fp_u2_old)
    board.Add(fp_u2_new)
    board.BuildListOfNets()

    board.Save(PCB_PATH)
    print("Successfully replaced U2 with ESP32-S3-WROOM-1U!")

if __name__ == "__main__":
    swap_u2()
