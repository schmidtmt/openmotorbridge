// =============================================================================
// OpenMotorBridge - Main Box: Outer Mounting Ears (4x M4 Silentblock)
// =============================================================================
// File: hardware/cad/scad/01_main_box/parts/004_mounting_ears.scad
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module main_box_mounting_ears(length=110.0, width=74.0, ear_len=14.0, ear_w=12.0, ear_h=5.0, edge_offset=14.0) {
    // 1. Bottom-Left Ear (-X, -Y flank)
    translate([0, edge_offset, 0])
        rotate([0, 0, 180])
            mounting_ear_m4(ear_len=ear_len, ear_w=ear_w, ear_h=ear_h, hole_r=M4_SCREW_HOLE_R);

    // 2. Bottom-Right Ear (+X, -Y flank)
    translate([length, edge_offset, 0])
        rotate([0, 0, 0])
            mounting_ear_m4(ear_len=ear_len, ear_w=ear_w, ear_h=ear_h, hole_r=M4_SCREW_HOLE_R);

    // 3. Top-Left Ear (-X, +Y flank)
    translate([0, width - edge_offset, 0])
        rotate([0, 0, 180])
            mounting_ear_m4(ear_len=ear_len, ear_w=ear_w, ear_h=ear_h, hole_r=M4_SCREW_HOLE_R);

    // 4. Top-Right Ear (+X, +Y flank)
    translate([length, width - edge_offset, 0])
        rotate([0, 0, 0])
            mounting_ear_m4(ear_len=ear_len, ear_w=ear_w, ear_h=ear_h, hole_r=M4_SCREW_HOLE_R);
}

// Standalone preview
main_box_mounting_ears();
