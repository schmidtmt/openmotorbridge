// =============================================================================
// OpenMotorBridge - Main Box: Lower Base Tub (Unterwanne Grundkörper)
// =============================================================================
// File: hardware/cad/scad/01_main_box/parts/000_lower_base.scad
// =============================================================================

include <../../00_common/parameters.scad>;

module main_box_lower_base(length=110.0, width=74.0, height=17.0, wall=2.5) {
    difference() {
        // Solid outer box
        cube(size=[length, width, height], center=false);
        // Hollow interior pocket
        translate([wall, wall, wall]) {
            cube(size=[length - 2*wall, width - 2*wall, height], center=false);
        }
    }
}

// Standalone preview
main_box_lower_base();
