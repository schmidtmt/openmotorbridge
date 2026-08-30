// =============================================================================
// OpenMotorBridge - Main Box: Thermal Copper Studs & Cutouts
// =============================================================================
// File: hardware/cad/scad/01_main_box/parts/003_copper_thermal_studs.scad
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

// 1. 4x Copper Stud Cutout Tool (for difference with floor)
module main_box_copper_stud_cutouts(h=5.0, clearance=0.1) {
    for (pos = MAIN_BOX_CU_POS) {
        translate([pos[0], pos[1], -1.0])
            cylinder(r=COPPER_STUD_R + clearance, h=h, center=false);
    }
}

// 2. 4x Thermal Copper Stud Solid Bodies (Ø 8.0 x 4.0 mm)
module main_box_copper_studs(h=4.0) {
    for (pos = MAIN_BOX_CU_POS) {
        translate([pos[0], pos[1], 0.0])
            copper_stud(r=COPPER_STUD_R, h=h);
    }
}

// Standalone preview
main_box_copper_studs();
