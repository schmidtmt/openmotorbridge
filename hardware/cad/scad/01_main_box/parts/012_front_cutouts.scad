// =============================================================================
// OpenMotorBridge - Main Box: Front Face Cutout Tools (HD26, USB-C, Status LEDs)
// =============================================================================
// File: hardware/cad/scad/01_main_box/parts/012_front_cutouts.scad
// =============================================================================

include <../../00_common/parameters.scad>;

module main_box_front_cutout_tool(wall_th=5.0) {
    // 1. High-Density 26-Pin D-Sub Port Cutout (40.0 x 10.0 mm)
    translate([10.0, -1.0, 5.0])
        cube(size=[40.0, wall_th + 2.0, 10.0], center=false);

    // 2. IP67 USB-C Waterproof Port Cutout (10.0 x 4.5 mm)
    translate([57.5, -1.0, 7.5])
        cube(size=[10.0, wall_th + 2.0, 4.5], center=false);

    // 3. Status LED Light Pipe Windows (3x Ø 2.5 mm holes)
    for (i = [0:2]) {
        translate([77.5 + i * 5.0, -1.0, 9.5])
            rotate([-90, 0, 0])
                cylinder(r=1.25, h=wall_th + 2.0, center=false);
    }
}

// Standalone preview
main_box_front_cutout_tool();
