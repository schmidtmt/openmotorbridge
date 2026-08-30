// =============================================================================
// OpenMotorBridge - Main Box: Mid Tray Frame (Oberwannen-Rahmen)
// =============================================================================
// File: hardware/cad/scad/01_main_box/parts/010_mid_tray_frame.scad
// =============================================================================

include <../../00_common/parameters.scad>;

module main_box_mid_tray_frame(length=110.0, width=74.0, height=15.0, wall=2.5) {
    difference() {
        // Outer solid block
        cube(size=[length, width, height], center=false);
        // Hollow interior (open top and bottom for partition plate insertion)
        translate([wall, wall, -0.1])
            cube(size=[length - 2*wall, width - 2*wall, height + 0.2], center=false);
    }
}

// Standalone preview
main_box_mid_tray_frame();
