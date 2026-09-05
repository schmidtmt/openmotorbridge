// =============================================================================
// OpenMotorBridge - Universal Front Node: Closed Enclosure Model
// =============================================================================
// File: hardware/cad/scad/04_front_node/98_front_node_closed.scad
// Description: Fully assembled and closed waterproof enclosure model for
//              collision verification, volume checks, and 3D rendering.
// =============================================================================

include <../00_common/parameters.scad>;
use <00_front_node_tub.scad>;
use <01_front_node_lid.scad>;
use <parts/005_cable_combs.scad>;
use <03_front_node_usbc_plug.scad>;

module front_node_closed_assembly() {
    // 1. Lower Enclosure Tub
    color("dimgray")
        front_node_lower_tub();
        
    // 2. Upper Lid (Mated flush on top of lower tub)
    color([0.25, 0.25, 0.27])
        translate([0, 0, FRONT_NODE_TUB_H])
            front_node_upper_lid();
            
    // 3. South USB Cable Comb (in position)
    translate([17.2, 0.1, FRONT_NODE_TUB_H - 8.0])
        south_epdm_cable_comb();
        
    // 4. West Signal/Power Cable Comb (in position)
    translate([0.1, FRONT_NODE_WALL + 3.5 + 11.2, FRONT_NODE_TUB_H - 7.5])
        west_epdm_cable_comb();
        
    // 5. USB-C Protective Plug (in position at East wall)
    translate([FRONT_NODE_OUTER_L - 7.2, 38.82, FRONT_NODE_WALL + FRONT_NODE_STANDOFF_H + FRONT_NODE_PCB_H + 1.8])
        rotate([0, 90, 90])
            front_node_usbc_plug();
            
    // 6. 4x M3 Corner Clamping Screws (DIN 912 stainless steel)
    corner_offsets = [
        [FRONT_NODE_CORNER_R, FRONT_NODE_CORNER_R],
        [FRONT_NODE_OUTER_L - FRONT_NODE_CORNER_R, FRONT_NODE_CORNER_R],
        [FRONT_NODE_CORNER_R, FRONT_NODE_OUTER_W - FRONT_NODE_CORNER_R],
        [FRONT_NODE_OUTER_L - FRONT_NODE_CORNER_R, FRONT_NODE_OUTER_W - FRONT_NODE_CORNER_R]
    ];
    color("silver") {
        for (co = corner_offsets) {
            translate([co[0], co[1], FRONT_NODE_OUTER_H - 2.5])
                cylinder(r=2.8, h=2.5, center=false); // Screw heads
        }
    }
}

front_node_closed_assembly();
