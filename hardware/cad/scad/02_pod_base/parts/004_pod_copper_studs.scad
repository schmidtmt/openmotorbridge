// =============================================================================
// OpenMotorBridge - Satellite Pod: Thermal Copper Studs & Floor Pockets
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/004_pod_copper_studs.scad
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

// 1. 2x Copper Stud Cutout Tool (for through-holes in Pod floor)
module pod_copper_stud_cutouts(h=6.0, clearance=0.1) {
    for (pos = POD_CU_POS) {
        translate([pos[0], pos[1], -1.0])
            cylinder(r=COPPER_STUD_R + clearance, h=h, center=false);
    }
}

// 2. 2x Thermal Copper Stud Solid Bodies (Ø 8.0 x 2.5 mm)
module pod_copper_studs(h=2.5) {
    for (pos = POD_CU_POS) {
        translate([pos[0], pos[1], 0.0])
            copper_stud(r=COPPER_STUD_R, h=h);
    }
}

// Standalone preview
pod_copper_studs();
