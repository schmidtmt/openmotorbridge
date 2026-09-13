// =============================================================================
// OpenMotorBridge - Front Node Acoustic Vent Port
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/002_acoustic_vent.scad
// Description: Through-chassis acoustic port and Gore ePTFE membrane recess
//              aligned directly beneath Knowles SPH0645 MEMS microphone (PCBA 05).
// =============================================================================

include <../../00_common/parameters.scad>;

// Mic acoustic port coordinates relative to chamber origin (0,0)
// Knowles SPH0645 is at KiCad rel (43.00, 28.96) mm on the 82x50 mm board
MIC_CHAMBER_X = (FRONT_NODE_CHAMBER_L - FRONT_NODE_PCB_L) / 2.0 + 43.00; // 45.00 mm
MIC_CHAMBER_Y = (FRONT_NODE_CHAMBER_W - FRONT_NODE_PCB_W) / 2.0 + 28.96; // 31.96 mm

// Subtractive module (cutout in enclosure floor)
module front_node_acoustic_vent_cutout(floor_thickness = FRONT_NODE_WALL) {
    translate([MIC_CHAMBER_X, MIC_CHAMBER_Y, -0.1]) {
        // 1. Through-hole sound canal Ø 2.5 mm
        cylinder(r=FRONT_NODE_MIC_HOLE_R, h=floor_thickness + 0.2, center=false, $fn=24);
        
        // 2. Outer recess pocket for Ø 6.0 mm Gore ePTFE membrane
        cylinder(r=FRONT_NODE_MIC_MEMB_R, h=FRONT_NODE_MIC_MEMB_D + 0.1, center=false, $fn=32);
    }
}
