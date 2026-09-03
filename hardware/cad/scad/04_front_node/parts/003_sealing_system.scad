// =============================================================================
// OpenMotorBridge - Front Node: Perimeter Sealing Groove & Tongue (Nut & Feder)
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/003_sealing_system.scad
// Description: Parametric IP67 perimeter O-ring groove (lower tub) and matching
//              compression tongue (upper lid) for Ø 1.5 mm elastomeric seal.
// =============================================================================

include <../../00_common/parameters.scad>;

// 1. Gasket Groove Cutout Tool (Nut for Lower Tub upper rim)
module front_node_sealing_groove_tool(
    length = FRONT_NODE_OUTER_L,
    width  = FRONT_NODE_OUTER_W,
    z_top  = FRONT_NODE_TUB_H,
    groove_w = 2.0,
    groove_depth = 1.6
) {
    translate([0, 0, z_top - groove_depth]) {
        difference() {
            translate([1.2, 1.2, 0])
                cube(size=[length - 2.4, width - 2.4, groove_depth + 0.1], center=false);
            translate([1.2 + groove_w, 1.2 + groove_w, -0.1])
                cube(size=[length - 2.4 - 2*groove_w, width - 2.4 - 2*groove_w, groove_depth + 0.3], center=false);
        }
    }
}

// 2. Gasket Tongue / Lip (Feder for Lid lower rim: 1.5 mm wide x 1.4 mm high)
module front_node_sealing_tongue_lip(
    length = FRONT_NODE_OUTER_L,
    width  = FRONT_NODE_OUTER_W,
    lip_w  = 1.5,
    lip_h  = 1.4
) {
    difference() {
        translate([1.45, 1.45, -lip_h])
            cube(size=[length - 2.9, width - 2.9, lip_h], center=false);
        translate([1.45 + lip_w, 1.45 + lip_w, -lip_h - 0.1])
            cube(size=[length - 2.9 - 2*lip_w, width - 2.9 - 2*lip_w, lip_h + 0.2], center=false);
    }
}

// 3. Silicone Gasket Ring (for exploded 3D rendering)
module front_node_silicone_gasket(
    length = FRONT_NODE_OUTER_L,
    width  = FRONT_NODE_OUTER_W,
    cord_dia = 1.5
) {
    color([0.2, 0.6, 0.85, 0.9]) // Translucent silicone blue
    translate([1.5, 1.5, 0])
    difference() {
        cube(size=[length - 3.0, width - 3.0, cord_dia], center=false);
        translate([cord_dia, cord_dia, -0.1])
            cube(size=[length - 3.0 - 2*cord_dia, width - 3.0 - 2*cord_dia, cord_dia + 0.2], center=false);
    }
}
