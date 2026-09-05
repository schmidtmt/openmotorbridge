// =============================================================================
// OpenMotorBridge - Front Node: Base Enclosure Tub (Unterwanne Grundkörper)
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/000_front_node_base_tub.scad
// Description: Monolithic solid outer body with rounded corners and hollowed-out
//              interior chamber (CSG constructive solid geometry).
// =============================================================================

include <../../00_common/parameters.scad>;

module front_node_base_tub(
    length   = FRONT_NODE_OUTER_L,
    width    = FRONT_NODE_OUTER_W,
    height   = FRONT_NODE_TUB_H,
    corner_r = FRONT_NODE_CORNER_R,
    wall     = FRONT_NODE_WALL
) {
    difference() {
        // 1. Solid Outer Block with Rounded Vertical Corners
        linear_extrude(height = height) {
            offset(r = corner_r) {
                offset(delta = -corner_r) {
                    square([length, width], center=false);
                }
            }
        }

        // 2. Hollow Internal Chamber (Leaves 2.5 mm wall and 2.5 mm solid floor)
        translate([wall + 3.5, wall + 3.5, wall]) {
            cube(size=[FRONT_NODE_CHAMBER_L, FRONT_NODE_CHAMBER_W, height + 1.0], center=false);
        }
    }
}

// Standalone preview / STL export
front_node_base_tub();
