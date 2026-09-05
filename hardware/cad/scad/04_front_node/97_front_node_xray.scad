// =============================================================================
// OpenMotorBridge - Universal Front Node: Cross-Section Cutaway & Inspection
// =============================================================================
// File: hardware/cad/scad/04_front_node/97_front_node_xray.scad
// Description: 3D Cross-Section cutaway showing internal PCB seating, standoffs,
//              gasket compression groove, acoustic vent, and cable combs.
// =============================================================================

include <../00_common/parameters.scad>;
use <00_front_node_tub.scad>;
use <01_front_node_lid.scad>;
use <parts/005_cable_combs.scad>;
use <parts/006_dummy_front_node_pcb.scad>;
use <03_front_node_usbc_plug.scad>;

module front_node_cross_section_cutaway() {
    difference() {
        union() {
            // 1. Lower Enclosure Tub
            color("dimgray")
                front_node_lower_tub();
                
            // 2. Upper Enclosure Lid (Mated)
            color([0.28, 0.28, 0.30])
                translate([0, 0, FRONT_NODE_TUB_H])
                    front_node_upper_lid();
                    
            // 3. Cable Combs (in place)
            translate([17.2, 0.1, FRONT_NODE_TUB_H - 8.0])
                south_epdm_cable_comb();
                
            translate([0.1, FRONT_NODE_WALL + 3.5 + 11.2, FRONT_NODE_TUB_H - 7.5])
                west_epdm_cable_comb();
                
            // 4. USB-C Plug (East wall)
            translate([FRONT_NODE_OUTER_L - 7.2, 38.82, FRONT_NODE_WALL + FRONT_NODE_STANDOFF_H + FRONT_NODE_PCB_H + 1.8])
                rotate([0, 90, 90])
                    front_node_usbc_plug();
        }
        
        // 5. 90° Front-Right Cutaway Cube (slices away front-right quarter)
        translate([FRONT_NODE_OUTER_L / 2.0, -10.0, -5.0])
            cube(size=[FRONT_NODE_OUTER_L, FRONT_NODE_OUTER_W / 2.0 + 10.0, FRONT_NODE_OUTER_H + 15.0], center=false);
    }
    
    // 6. Intact Front Node PCB Assembly inside the cutaway
    translate([FRONT_NODE_WALL + 3.5, FRONT_NODE_WALL + 3.5, FRONT_NODE_WALL + FRONT_NODE_STANDOFF_H])
        dummy_front_node_pcb();
}

front_node_cross_section_cutaway();
