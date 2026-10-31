// =============================================================================
// OpenMotorBridge - Universal Front Node: Closed Enclosure Model (v10.0)
// =============================================================================
// File: hardware/cad/scad/04_front_node/98_front_node_closed.scad
// Description: Fully assembled and closed waterproof v10 Monocoque model for
//              collision verification, volume checks, and 3D rendering.
// =============================================================================

include <../00_common/parameters.scad>;
use <00_front_node_tub.scad>;
use <01_front_node_lid.scad>;
use <parts/005_cable_combs.scad>;
use <parts/sensor_puck_environmental.scad>;
use <03_front_node_usbc_plug.scad>;

module front_node_closed_assembly() {
    ch_x_start = FRONT_NODE_WALL + 3.5; // 6.0 mm
    ch_y_start = FRONT_NODE_WALL + 3.5; // 6.0 mm

    // 1. Lower Monocoque Enclosure Tub
    color([0.16, 0.18, 0.20])
        front_node_lower_tub();
        
    // 2. Upper L-Slide Lid (Mated form-fit in C-grooves and locked)
    color([0.22, 0.24, 0.26])
        front_node_upper_lid();
            
    // 3. South Cockpit Cable Gland Boot
    front_node_south_cable_boot_installed();
        
    // 4. North Vehicle Cable Gland Boot
    front_node_north_cable_boot_installed();
        
    // 5. USB-C Protective Plug (in position at East wall)
    translate([FRONT_NODE_OUTER_L - 7.2, 24.1, FRONT_NODE_WALL + FRONT_NODE_STANDOFF_H + FRONT_NODE_PCB_H + 1.8])
        rotate([0, 90, 90])
            front_node_usbc_plug();

    // 6. Modular Snap-On Environmental Sensor Puck (docked into top lid)
    translate([ch_x_start + 55.0 - 22.0, ch_y_start + 28.0 - 22.0, FRONT_NODE_OUTER_H - 1.2])
        sensor_puck_environmental_assembly();
}

front_node_closed_assembly();
