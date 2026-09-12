// =============================================================================
// OpenMotorBridge - Front Node: IP67 EPDM Cable Comb & Compression Clamp System
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/005_cable_combs.scad
// Description: IP67 elastomeric compression glands for South (6-Port USB/Charge)
//              and West (6-Port Vehicle/Sensor) cable exits, plus East USB-C service port.
// =============================================================================

include <../../00_common/parameters.scad>;

// 1. South USB/Charge Cable Pocket Cutout (in Tub rim, Y = 0)
// Accommodates 6x USB/Power cables: J4 (Host, X=20.5), J5 (Phone PD, X=32.5),
//                                   J6 (CP2AA, X=44.5), J5_MP3 (Glovebox, X=56.5),
//                                   J6_AUX (Cockpit, X=68.5), J8 (Action-Cam, X=78.5)
module south_cable_comb_cutout(z_start = FRONT_NODE_TUB_H - 8.0, h = 8.1) {
    // Cutout spans Tub X in [14.0, 84.0] mm (70.0 mm width, centered between corner bosses)
    translate([14.0, -1.0, z_start])
        cube(size=[70.0, FRONT_NODE_WALL + 5.0, h], center=false);
}

// 2. West Signal/Power Cable Pocket Cutout (in Tub rim, X = 0)
// Accommodates 6x harnesses: J9 (BSD, Y=14.5), J3 (PTT, Y=22.0), J2 (CAN, Y=29.5),
//                            J11 (Aux, Y=36.5), J10 (Qi, Y=43.5), J1 (12V, Y=50.5)
module west_cable_comb_cutout(z_start = FRONT_NODE_TUB_H - 7.5, h = 7.6) {
    // Cutout spans Tub Y in [9.0, 56.0] mm (47.0 mm width)
    translate([-1.0, 9.0, z_start])
        cube(size=[FRONT_NODE_WALL + 5.0, 47.0, h], center=false);
}

// 3. USB-C Service Port Cutout (East wall, X = 98.0 mm, Y = 24.1 mm, forward right flank)
module front_node_usbc_service_cutout(
    z_center = FRONT_NODE_WALL + FRONT_NODE_STANDOFF_H + FRONT_NODE_PCB_H + 1.8,
    y_center = 24.1, // Aligned with J7 (KiCad: Y=104.93 on board spanning Y=70..120 mm -> 120 - 104.93 = 15.07 mm + 9.0 mm tub offset)
    w = 10.5,
    h = 4.8
) {
    // A. Main pass-through rectangular bore through East wall
    translate([FRONT_NODE_OUTER_L - 7.0, y_center - w/2.0, z_center - h/2.0])
        cube(size=[8.0, w, h], center=false);
        
    // B. Recessed pocket for silicone dust plug collar (1.2 mm deep on outer East face)
    translate([FRONT_NODE_OUTER_L - 1.2, y_center - (w + 3.0)/2.0, z_center - (h + 3.0)/2.0])
        cube(size=[1.4, w + 3.0, h + 3.0], center=false);
}

// 4. South 6-Slot EPDM Elastomer Comb (Insert Model)
module south_epdm_cable_comb() {
    color([0.15, 0.15, 0.15, 0.95]) // Black soft rubber
    difference() {
        cube(size=[69.6, FRONT_NODE_WALL + 3.2, 7.8], center=false);
        
        // 6x Cable Channels (Ø 4.2 mm) for J4, J5, J6, J5_MP3, J6_AUX, J8
        // Positions relative to comb origin (starts at X_Tub = 14.0 mm):
        cable_x = [20.5 - 14.0, 32.5 - 14.0, 44.5 - 14.0, 56.5 - 14.0, 68.5 - 14.0, 78.5 - 14.0];
        for (cx = cable_x) {
            translate([cx, -0.5, 4.0])
                rotate([-90, 0, 0])
                    cylinder(r=2.1, h=FRONT_NODE_WALL + 5.0, center=false, $fn=24);
                    
            // Slit for easy cable insertion without cutting connectors
            translate([cx - 0.4, -0.5, 4.0])
                cube(size=[0.8, FRONT_NODE_WALL + 5.0, 4.5], center=false);
        }
    }
}

// 5. West 6-Slot EPDM Elastomer Comb (Insert Model)
module west_epdm_cable_comb() {
    color([0.15, 0.15, 0.15, 0.95]) // Black soft rubber
    difference() {
        cube(size=[FRONT_NODE_WALL + 3.2, 46.6, 7.3], center=false);
        
        // 6x Cable Channels (Ø 3.2 mm) for J9, J3, J2, J11, J10, J1
        // Positions relative to comb origin (starts at Y_Tub = 9.0 mm):
        cable_y = [14.5 - 9.0, 22.0 - 9.0, 29.5 - 9.0, 36.5 - 9.0, 43.5 - 9.0, 50.5 - 9.0];
        for (cy = cable_y) {
            translate([-0.5, cy, 3.8])
                rotate([0, 90, 0])
                    cylinder(r=1.6, h=FRONT_NODE_WALL + 5.0, center=false, $fn=24);
                    
            // Slit for easy cable insertion
            translate([-0.5, cy - 0.4, 3.8])
                cube(size=[FRONT_NODE_WALL + 5.0, 0.8, 4.0], center=false);
        }
    }
}
