// =============================================================================
// OpenMotorBridge - Front Node: IP67 EPDM Cable Comb & Compression Clamp System
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/005_cable_combs.scad
// Description: Variant A (Approved): Two 3-channel elastomeric compression
//              glands for South (USB) and West (Power/Signal) cable exits.
// =============================================================================

include <../../00_common/parameters.scad>;

// 1. South USB Cable Pocket Cutout (in Tub rim, Y = 0)
// Accommodates 3x USB cables: J6 (CarPlay, X=18), J5 (Glovebox, X=32), J4 (Host, X=45)
module south_cable_comb_cutout(z_start = FRONT_NODE_TUB_H - 8.0, h = 8.1) {
    translate([12.0, -1.0, z_start])
        cube(size=[38.0, FRONT_NODE_WALL + 2.0, h], center=false);
}

// 2. West Signal/Power Cable Pocket Cutout (in Tub rim, X = 0)
// Accommodates 3x harnesses: J1 (12V, Y=16), J2 (CAN, Y=28), J3 (PTT, Y=36)
module west_cable_comb_cutout(z_start = FRONT_NODE_TUB_H - 7.5, h = 7.6) {
    translate([-1.0, 11.0, z_start])
        cube(size=[FRONT_NODE_WALL + 2.0, 30.0, h], center=false);
}

// 3. USB-C Service Port Cutout (South wall, X = 55.8 mm)
module front_node_usbc_service_cutout(
    z_center = FRONT_NODE_STANDOFF_H + FRONT_NODE_PCB_H + 1.8,
    w = 10.5,
    h = 4.8
) {
    translate([55.82 - w/2.0, -1.0, z_center - h/2.0])
        cube(size=[w, FRONT_NODE_WALL + 2.0, h], center=false);
        
    // Recess pocket for silicone dust plug collar
    translate([55.82 - (w+3.0)/2.0, -0.1, z_center - (h+3.0)/2.0])
        cube(size=[w + 3.0, 1.2, h + 3.0], center=false);
}

// 4. South 3-Slot EPDM Elastomer Comb (Insert Model)
module south_epdm_cable_comb() {
    color([0.15, 0.15, 0.15, 0.95]) // Black soft rubber
    difference() {
        cube(size=[37.6, FRONT_NODE_WALL - 0.2, 7.8], center=false);
        
        // 3x Cable Channels (Ø 4.2 mm) for J6, J5, J4
        cable_x = [18.0 - 12.0, 31.5 - 12.0, 45.2 - 12.0];
        for (cx = cable_x) {
            translate([cx, -0.5, 4.0])
                rotate([-90, 0, 0])
                    cylinder(r=2.1, h=FRONT_NODE_WALL + 1.0, center=false);
                    
            // Slit for easy cable insertion without cutting connectors
            translate([cx - 0.4, -0.5, 4.0])
                cube(size=[0.8, FRONT_NODE_WALL + 1.0, 4.5], center=false);
        }
    }
}

// 5. West 3-Slot EPDM Elastomer Comb (Insert Model)
module west_epdm_cable_comb() {
    color([0.15, 0.15, 0.15, 0.95]) // Black soft rubber
    difference() {
        cube(size=[FRONT_NODE_WALL - 0.2, 29.6, 7.3], center=false);
        
        // 3x Cable Channels (Ø 3.2 mm) for J1, J2, J3
        cable_y = [16.0 - 11.0, 28.2 - 11.0, 36.2 - 11.0];
        for (cy = cable_y) {
            translate([-0.5, cy, 3.8])
                rotate([0, 90, 0])
                    cylinder(r=1.6, h=FRONT_NODE_WALL + 1.0, center=false);
                    
            // Slit for easy cable insertion
            translate([-0.5, cy - 0.4, 3.8])
                cube(size=[FRONT_NODE_WALL + 1.0, 0.8, 4.0], center=false);
        }
    }
}
