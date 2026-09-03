// =============================================================================
// OpenMotorBridge - Front Node: 4-in-1 Universal Mounting System
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/004_mounting_system.scad
// Description: Multi-bike mounting interfaces:
//              1. AMPS 4-hole pattern (38x30 mm, M4 threaded brass inserts)
//              2. 90° crossed zip-tie & hose clamp channels
//              3. 2x M4/M5 slotted silentblock mounting ears
//              4. Recessed 3M Dual-Lock / VHB tape landing pad
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

CENTER_X = FRONT_NODE_OUTER_L / 2.0; // 42.0 mm
CENTER_Y = FRONT_NODE_OUTER_W / 2.0; // 30.0 mm

// 1. AMPS 4-Hole Threaded Insert Pockets (Subtractive in floor)
module front_node_amps_cutouts(h_depth = 5.0) {
    amps_coords = [
        [CENTER_X - AMPS_SPACING_X / 2.0, CENTER_Y - AMPS_SPACING_Y / 2.0], // [23.0, 15.0]
        [CENTER_X + AMPS_SPACING_X / 2.0, CENTER_Y - AMPS_SPACING_Y / 2.0], // [61.0, 15.0]
        [CENTER_X - AMPS_SPACING_X / 2.0, CENTER_Y + AMPS_SPACING_Y / 2.0], // [23.0, 45.0]
        [CENTER_X + AMPS_SPACING_X / 2.0, CENTER_Y + AMPS_SPACING_Y / 2.0]  // [61.0, 45.0]
    ];
    
    for (pt = amps_coords) {
        translate([pt[0], pt[1], -0.1])
            cylinder(r=AMPS_INSERT_R, h=h_depth + 0.1, center=false);
    }
}

// 2. Crossed Zip-Tie & Hose Clamp Tunnels (Subtractive in floor)
module front_node_ziptie_tunnels(slot_w = 5.5, slot_depth = 2.2) {
    // A. Longitudinal tunnel along X (centered in Y)
    translate([-1.0, CENTER_Y - slot_w/2.0, -0.1])
        cube(size=[FRONT_NODE_OUTER_L + 2.0, slot_w, slot_depth + 0.1], center=false);
        
    // B. Transverse tunnel along Y (centered in X)
    translate([CENTER_X - slot_w/2.0, -1.0, -0.1])
        cube(size=[slot_w, FRONT_NODE_OUTER_W + 2.0, slot_depth + 0.1], center=false);
}

// 3. 3M Dual-Lock / VHB Tape Recessed Landing Pad (Subtractive in floor)
module front_node_dual_lock_recess(pad_l = 50.0, pad_w = 28.0, pad_depth = 0.6) {
    translate([CENTER_X - pad_l/2.0, CENTER_Y - pad_w/2.0, -0.1])
        cube(size=[pad_l, pad_w, pad_depth + 0.1], center=false);
}

// 4. M4/M5 Slotted Silentblock Flange Mounting Ears (Additive to enclosure tub)
module front_node_flange_ears(ear_len = 14.0, ear_w = 14.0, ear_h = 5.0, hole_r = 2.5) {
    // Left ear (at X = 0, centered in Y)
    translate([0, CENTER_Y, 0])
        rotate([0, 0, 180])
            mounting_ear_m4(ear_len=ear_len, ear_w=ear_w, ear_h=ear_h, hole_r=hole_r);
            
    // Right ear (at X = FRONT_NODE_OUTER_L, centered in Y)
    translate([FRONT_NODE_OUTER_L, CENTER_Y, 0])
        mounting_ear_m4(ear_len=ear_len, ear_w=ear_w, ear_h=ear_h, hole_r=hole_r);
}
