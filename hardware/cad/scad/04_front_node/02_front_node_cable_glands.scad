// =============================================================================
// OpenMotorBridge - Front Node: Cable Gland Comb Inserts (TPU / EPDM)
// =============================================================================
// File: hardware/cad/scad/04_front_node/02_front_node_cable_glands.scad
// Description: Printable elastomeric cable seals for South and West openings.
// =============================================================================

include <../00_common/parameters.scad>;
include <parts/005_cable_combs.scad>;

// Pair of circular TPU cable boots arranged side-by-side for 3D printing in Shore 85A/95A TPU
module front_node_cable_glands_printable_pair() {
    front_node_cable_glands_pair();
}

front_node_cable_glands_printable_pair();

