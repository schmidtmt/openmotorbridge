// =============================================================================
// OpenMotorBridge - Front Node: IP67 EPDM Cable Comb & Compression Clamp System
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/005_cable_combs.scad
// Description: IP67 elastomeric compression glands for South (4-Port USB)
//              and West (Power/Signal) cable exits, plus East USB-C service port.
// =============================================================================

include <../../00_common/parameters.scad>;

// 1. South USB Cable Pocket Cutout (in Tub rim, Y = 0)
// Accommodates 4x USB cables: J6 (CarPlay, X=23.75), J5 (Glovebox, X=37.50),
//                             J4 (Host, X=51.25), J8 (Action-Cam, X=64.00)
module south_cable_comb_cutout(z_start = FRONT_NODE_TUB_H - 8.0, h = 8.1) {
    // Cutout spans Tub X in [17.0, 70.0] mm (53.0 mm width, leaves >10 mm to corner bosses)
    translate([11.0, -1.0, z_start])
        cube(size=[53.0, FRONT_NODE_WALL + 5.0, h], center=false);
}

// 2. West Signal/Power Cable Pocket Cutout (in Tub rim, X = 0)
// Accommodates 3x harnesses: J1 (12V, Y=16), J2 (CAN, Y=28), J3 (PTT, Y=36)
module west_cable_comb_cutout(z_start = FRONT_NODE_TUB_H - 7.5, h = 7.6) {
    translate([-1.0, 11.0, z_start])
        cube(size=[FRONT_NODE_WALL + 5.0, 30.0, h], center=false);
}

// 3. USB-C Service Port Cutout (East wall, X = 84.0 mm, Y = 38.82 mm)
module front_node_usbc_service_cutout(
    z_center = FRONT_NODE_WALL + FRONT_NODE_STANDOFF_H + FRONT_NODE_PCB_H + 1.8,
    y_center = (FRONT_NODE_CHAMBER_W - FRONT_NODE_PCB_W)/2.0 + FRONT_NODE_WALL + 3.5 + 30.82, // 38.82 mm
    w = 10.5,
    h = 4.8
) {
    // A. Main pass-through rectangular bore through East wall (X = 77.0 to 85.0 mm)
    translate([FRONT_NODE_OUTER_L - 7.0, y_center - w/2.0, z_center - h/2.0])
        cube(size=[8.0, w, h], center=false);
        
    // B. Recessed pocket for silicone dust plug collar (1.2 mm deep on outer East face)
    translate([FRONT_NODE_OUTER_L - 1.2, y_center - (w + 3.0)/2.0, z_center - (h + 3.0)/2.0])
        cube(size=[1.4, w + 3.0, h + 3.0], center=false);
}

// 4. South 4-Slot EPDM Elastomer Comb (Insert Model)
module south_epdm_cable_comb() {
    color([0.15, 0.15, 0.15, 0.95]) // Black soft rubber
    difference() {
        cube(size=[52.6, FRONT_NODE_WALL + 3.2, 7.8], center=false);
        
        // 4x Cable Channels (Ø 4.2 mm) for J6, J5, J4, J8
        // Positions relative to comb origin (starts at X_Tub = 17.2 mm):
        cable_x = [23.75 - 17.0, 37.50 - 17.0, 51.25 - 17.0, 64.00 - 17.0]; // [6.75, 20.50, 34.25, 47.00]
        for (cx = cable_x) {
            translate([cx, -0.5, 4.0])
                rotate([-90, 0, 0])
                    cylinder(r=2.1, h=FRONT_NODE_WALL + 5.0, center=false);
                    
            // Slit for easy cable insertion without cutting connectors
            translate([cx - 0.4, -0.5, 4.0])
                cube(size=[0.8, FRONT_NODE_WALL + 5.0, 4.5], center=false);
        }
    }
}

// 5. West 3-Slot EPDM Elastomer Comb (Insert Model)
module west_epdm_cable_comb() {
    color([0.15, 0.15, 0.15, 0.95]) // Black soft rubber
    difference() {
        cube(size=[FRONT_NODE_WALL + 3.2, 29.6, 7.3], center=false);
        
        // 3x Cable Channels (Ø 3.2 mm) for J1, J2, J3
        cable_y = [16.0 - 11.0, 28.2 - 11.0, 36.2 - 11.0];
        for (cy = cable_y) {
            translate([-0.5, cy, 3.8])
                rotate([0, 90, 0])
                    cylinder(r=1.6, h=FRONT_NODE_WALL + 5.0, center=false);
                    
            // Slit for easy cable insertion
            translate([-0.5, cy - 0.4, 3.8])
                cube(size=[FRONT_NODE_WALL + 5.0, 0.8, 4.0], center=false);
        }
    }
}
