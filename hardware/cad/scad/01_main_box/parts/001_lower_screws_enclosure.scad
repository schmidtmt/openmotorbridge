// =============================================================================
// OpenMotorBridge - Main Box: Corner Clamping Posts (4x M3 Eck-Spannsäulen)
// =============================================================================
// File: hardware/cad/scad/01_main_box/parts/001_lower_screws_enclosure.scad
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module main_box_corner_posts(length=110.0, width=74.0, height=17.0, post_size=6.0, hole_r=1.65) {
    // 1. Bottom-Left Corner [0, 0]
    translate([0, 0, 0])
        corner_screw_post(size_x=post_size, size_y=post_size, h=height, hole_r=hole_r, hole_h=height, hole_offset_z=0);

    // 2. Bottom-Right Corner [length - post_size, 0]
    translate([length - post_size, 0, 0])
        corner_screw_post(size_x=post_size, size_y=post_size, h=height, hole_r=hole_r, hole_h=height, hole_offset_z=0);

    // 3. Top-Left Corner [0, width - post_size]
    translate([0, width - post_size, 0])
        corner_screw_post(size_x=post_size, size_y=post_size, h=height, hole_r=hole_r, hole_h=height, hole_offset_z=0);

    // 4. Top-Right Corner [length - post_size, width - post_size]
    translate([length - post_size, width - post_size, 0])
        corner_screw_post(size_x=post_size, size_y=post_size, h=height, hole_r=hole_r, hole_h=height, hole_offset_z=0);
}

// Standalone preview
main_box_corner_posts();
