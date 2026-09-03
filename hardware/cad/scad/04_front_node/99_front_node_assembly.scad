// =============================================================================
// OpenMotorBridge - Universal Front Node: Exploded 3D Assembly View
// =============================================================================
// File: hardware/cad/scad/04_front_node/99_front_node_assembly.scad
// Description: Multi-tier exploded view for assembly documentation, demonstrating
//              component stack-up, sealing elements, and PCB integration.
// =============================================================================

include <../00_common/parameters.scad>;
use <00_front_node_tub.scad>;
use <01_front_node_lid.scad>;
use <parts/003_sealing_system.scad>;
use <parts/005_cable_combs.scad>;
use <parts/006_dummy_front_node_pcb.scad>;
use <03_front_node_usbc_plug.scad>;

// Exploded offsets in Z
EXPLODE_PCB_Z    = 10.0;
EXPLODE_GASKET_Z = 24.0;
EXPLODE_LID_Z    = 38.0;
EXPLODE_SCREWS_Z = 52.0;

module front_node_exploded_assembly() {
    // 1. Lower Enclosure Tub (Base level)
    color("dimgray")
        front_node_lower_tub();
        
    // 2. Gore ePTFE Acoustic Vent Membrane (under the tub floor)
    color("white")
        translate([FRONT_NODE_WALL + 3.5 + 24.50, FRONT_NODE_WALL + 3.5 + 17.46, -10.0])
            cylinder(r=FRONT_NODE_MIC_MEMB_R, h=0.2, center=false);
            
    // 3. Universal Front Node PCB Assembly
    translate([FRONT_NODE_WALL + 3.5, FRONT_NODE_WALL + 3.5, FRONT_NODE_WALL + FRONT_NODE_STANDOFF_H + EXPLODE_PCB_Z])
        dummy_front_node_pcb();
        
    // 4. South USB Cable Comb (floating forwards)
    translate([FRONT_NODE_WALL + 3.5 + 12.2, -18.0, FRONT_NODE_TUB_H - 8.0])
        south_epdm_cable_comb();
        
    // 5. West Signal/Power Cable Comb (floating leftwards)
    translate([-18.0, FRONT_NODE_WALL + 3.5 + 11.2, FRONT_NODE_TUB_H - 7.5])
        west_epdm_cable_comb();
        
    // 6. USB-C Protective Plug (floating forwards)
    translate([FRONT_NODE_WALL + 3.5 + 55.82, -22.0, FRONT_NODE_STANDOFF_H + FRONT_NODE_PCB_H + 1.8])
        rotate([90, 0, 0])
            front_node_usbc_plug();
            
    // 7. Perimeter Silicone Gasket Ring
    translate([0, 0, FRONT_NODE_TUB_H + EXPLODE_GASKET_Z])
        front_node_silicone_gasket();
        
    // 8. Upper Lid Plate
    color([0.28, 0.28, 0.30])
        translate([0, 0, FRONT_NODE_TUB_H + EXPLODE_LID_Z])
            front_node_upper_lid();
            
    // 9. 4x M3 Stainless Steel Clamping Screws (DIN 912)
    corner_offsets = [
        [FRONT_NODE_CORNER_R, FRONT_NODE_CORNER_R],
        [FRONT_NODE_OUTER_L - FRONT_NODE_CORNER_R, FRONT_NODE_CORNER_R],
        [FRONT_NODE_CORNER_R, FRONT_NODE_OUTER_W - FRONT_NODE_CORNER_R],
        [FRONT_NODE_OUTER_L - FRONT_NODE_CORNER_R, FRONT_NODE_OUTER_W - FRONT_NODE_CORNER_R]
    ];
    color("silver") {
        for (co = corner_offsets) {
            translate([co[0], co[1], FRONT_NODE_TUB_H + EXPLODE_SCREWS_Z]) {
                cylinder(r=2.8, h=3.0, center=false); // Head
                translate([0, 0, -18.0])
                    cylinder(r=1.5, h=18.0, center=false); // Shaft
            }
        }
    }
}

front_node_exploded_assembly();
