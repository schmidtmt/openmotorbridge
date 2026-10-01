// =============================================================================
// OpenMotorBridge - Main Box: PCB Screw Standoffs (4x M2.5 Platinendome)
// =============================================================================
// File: hardware/cad/scad/01_main_box/parts/002_pcb_standoffs.scad
// Description: Parametric screw bosses for the 85.0 x 55.0 mm PCBA 01 mainboard
//              with 77.0 x 47.0 mm mounting pitch. 100% Soldering-Iron Free
//              using PA12 self-tapping / thread-forming pilot holes (Ø 2.1 mm).
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module main_box_pcb_standoffs(pcb_x_offset=12.5, pcb_y_offset=9.5, h=3.5) {
    // PCBA 01 size: 85.0 x 55.0 mm. Mounting holes at (4,4), (81,4), (4,51), (81,51) relative to PCB.
    // Mounting pitch: 77.0 mm in X, 47.0 mm in Y.
    standoff_z = MAIN_BOX_WALL; // Floor thickness = 2.5 mm

    // Bottom-Left (Front-Left in vehicle orientation)
    translate([pcb_x_offset + 4.0, pcb_y_offset + 4.0, standoff_z])
        screw_boss(outer_r=3.0, inner_r=M2_5_PILOT_HOLE_R, h=h);

    // Bottom-Right (Front-Right)
    translate([pcb_x_offset + 81.0, pcb_y_offset + 4.0, standoff_z])
        screw_boss(outer_r=3.0, inner_r=M2_5_PILOT_HOLE_R, h=h);

    // Top-Left (Rear-Left)
    translate([pcb_x_offset + 4.0, pcb_y_offset + 51.0, standoff_z])
        screw_boss(outer_r=3.0, inner_r=M2_5_PILOT_HOLE_R, h=h);

    // Top-Right (Rear-Right)
    translate([pcb_x_offset + 81.0, pcb_y_offset + 51.0, standoff_z])
        screw_boss(outer_r=3.0, inner_r=M2_5_PILOT_HOLE_R, h=h);
}

// Standalone preview
main_box_pcb_standoffs();
