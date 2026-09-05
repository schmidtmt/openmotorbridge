// =============================================================================
// OpenMotorBridge - Front Node: Cable Gland Comb Inserts (TPU / EPDM)
// =============================================================================
// File: hardware/cad/scad/04_front_node/02_front_node_cable_glands.scad
// Description: Printable elastomeric cable seals for South and West openings.
// =============================================================================

include <../00_common/parameters.scad>;
include <parts/005_cable_combs.scad>;

// Pair of cable combs arranged side-by-side for 3D printing in TPU / Elastomer
// Connected via a 1.0 mm thin breakaway sprue runner so it forms a single solid mesh for slicing.
module front_node_cable_glands_printable_pair() {
    union() {
        // 1. South USB Comb
        translate([0, 0, 0])
            south_epdm_cable_comb();
            
        // 2. West Signal/Power Comb
        translate([0, 15.0, 0])
            west_epdm_cable_comb();
            
        // 3. Breakaway sprue runner connecting the two parts (1.0 mm thick)
        translate([2.0, 5.5, 0])
            cube(size=[3.0, 15.0 - 5.5 + 0.5, 1.0], center=false);
    }
}

front_node_cable_glands_printable_pair();

