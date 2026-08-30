// =============================================================================
// OpenMotorBridge - Main Box: PCB Screw Standoffs (4x M2.5 Platinendome)
// =============================================================================
// File: hardware/cad/scad/01_main_box/parts/002_pcb_standoffs.scad
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module main_box_pcb_standoffs(pcb_x_offset=7.5, pcb_y_offset=4.5, h=4.0) {
    // PCB size: 95 x 65 mm. Mounting holes at (4,4), (91,4), (4,61), (91,61) relative to PCB.
    translate([pcb_x_offset + 4.0, pcb_y_offset + 4.0, 2.5])
        screw_boss(outer_r=2.5, inner_r=M2_5_SCREW_HOLE_R, h=h);

    translate([pcb_x_offset + 91.0, pcb_y_offset + 4.0, 2.5])
        screw_boss(outer_r=2.5, inner_r=M2_5_SCREW_HOLE_R, h=h);

    translate([pcb_x_offset + 4.0, pcb_y_offset + 61.0, 2.5])
        screw_boss(outer_r=2.5, inner_r=M2_5_SCREW_HOLE_R, h=h);

    translate([pcb_x_offset + 91.0, pcb_y_offset + 61.0, 2.5])
        screw_boss(outer_r=2.5, inner_r=M2_5_SCREW_HOLE_R, h=h);
}

// Standalone preview
main_box_pcb_standoffs();
