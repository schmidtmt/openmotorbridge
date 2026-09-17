// =============================================================================
// OpenMotorBridge - Main Box: Corner Clamping Posts (4x M3 Eck-Spannsäulen)
// =============================================================================
// File: hardware/cad/scad/01_main_box/parts/001_lower_screws_enclosure.scad
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module main_box_corner_posts(length=110.0, width=74.0, height=17.0, post_size=MAIN_BOX_CORNER_POST, hole_r=M3_SCREW_HOLE_R) {
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

// 5. 4x Captive DIN 934 / DIN 985 M3 Hex Nut Pockets for lower case underside (z=0)
module main_box_corner_nut_pockets(length=110.0, width=74.0, post_size=MAIN_BOX_CORNER_POST, sw=NUT_M3_SW, h=NUT_M3_H, screw_r=M3_SCREW_HOLE_R) {
    offset = post_size / 2.0;
    nut_coords = [
        [offset, offset],
        [length - offset, offset],
        [offset, width - offset],
        [length - offset, width - offset]
    ];

    for (pt = nut_coords) {
        translate([pt[0], pt[1], -0.1])
            rotate([0, 0, 30])
                hex_nut_pocket(sw=sw, h=h + 0.1, screw_r=screw_r, through_h=10.0);
    }
}

// Standalone preview
main_box_corner_posts();

