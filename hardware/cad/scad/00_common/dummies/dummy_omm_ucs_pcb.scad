// =============================================================================
// OpenMotorBridge - Dummy 3D Model: Universal OMM Tri-Band UCS PCBA (PCBA 09/10)
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_omm_ucs_pcb.scad
// Description: Unified 3D CAD model of the Universal OMM Tri-Band UCS PCB
//              (2.4 GHz Mesh + BT Classic/BLE Bridge + 446 MHz PMR/DMR + 1000 mAh LiPo).
//              Delegates directly to dummy_omm446_ucs_pcb() as both OMM variants
//              have been unified onto the single Universal Tri-Band PCB with
//              100% software-defined mode switching.
// =============================================================================

include <../parameters.scad>;
use <dummy_omm446_ucs_pcb.scad>;

module dummy_omm_ucs_pcb(include_battery = true) {
    dummy_omm446_ucs_pcb(include_battery = include_battery);
}

// Standalone Render Preview
dummy_omm_ucs_pcb();
