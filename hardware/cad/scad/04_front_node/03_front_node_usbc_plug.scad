// =============================================================================
// OpenMotorBridge - Front Node: USB-C Service Port Protective Cap
// =============================================================================
// File: hardware/cad/scad/04_front_node/03_front_node_usbc_plug.scad
// Description: IP67 silicone / TPU protective sealing cap for USB-C service port
//              with retaining collar and finger tab.
// =============================================================================

include <../00_common/parameters.scad>;

module front_node_usbc_plug() {
    color([0.2, 0.2, 0.2, 0.9]) // Black elastomer
    union() {
        // 1. USB-C Receptacle Male Insert (snug fit into TYPE-C-31-M-12)
        translate([-4.1, -1.2, 0])
            cube(size=[8.2, 2.4, 6.0], center=false);
            
        // 2. Outer Waterproof Sealing Flange Collar
        translate([-6.5, -3.5, 6.0])
            cube(size=[13.0, 7.0, 1.5], center=false);
            
        // 3. Ergonomic Pull Tab / Lanyard Loop
        translate([-3.0, -1.0, 7.5])
            cube(size=[6.0, 2.0, 4.0], center=false);
    }
}

front_node_usbc_plug();
