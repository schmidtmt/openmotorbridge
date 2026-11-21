// =============================================================================
// OpenMotorBridge - Front Node Acoustic Vent Port
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/002_acoustic_vent.scad
// Description: Through-chassis acoustic port and Gore ePTFE membrane recess
//              aligned directly beneath Knowles SPH0645 MEMS microphone (PCBA 05).
// =============================================================================

include <../../00_common/parameters.scad>;

// Mic acoustic port coordinates relative to chamber origin (0,0)
// Knowles SPH0645 (MK1) is at KiCad (111.20, 116.30) -> PCB rel (11.20, 3.70) mm on the 82x50 mm board
MIC_PCB_X     = 11.20; // KiCad X=111.20 - 100.00
MIC_PCB_Y     = 3.70;  // CAD Y: 50.00 - (116.30 - 70.00) = 3.70 mm
MIC_CHAMBER_X = (FRONT_NODE_CHAMBER_L - FRONT_NODE_PCB_L) / 2.0 + MIC_PCB_X; // 2.0 + 11.20 = 13.20 mm (X_tub = 19.20 mm)
MIC_CHAMBER_Y = (FRONT_NODE_CHAMBER_W - FRONT_NODE_PCB_W) / 2.0 + MIC_PCB_Y; // 3.0 + 3.70 = 6.70 mm (Y_tub = 12.70 mm)

// Subtractive module (cutout in enclosure floor)
module front_node_acoustic_vent_cutout(floor_thickness = FRONT_NODE_WALL) {
    translate([MIC_CHAMBER_X, MIC_CHAMBER_Y, -0.1]) {
        // 1. Through-hole sound canal Ø 2.5 mm
        cylinder(r=FRONT_NODE_MIC_HOLE_R, h=floor_thickness + 0.2, center=false, $fn=24);
        
        // 2. Outer recess pocket for Ø 6.0 mm Gore ePTFE membrane
        cylinder(r=FRONT_NODE_MIC_MEMB_R, h=FRONT_NODE_MIC_MEMB_D + 0.1, center=false, $fn=32);
    }
}
