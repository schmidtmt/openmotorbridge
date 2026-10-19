// =============================================================================
// OpenMotorBridge - Vehicle Breakout Satellite Housing (5-Port Standard)
// =============================================================================
// File: hardware/cad/scad/04_front_node/vehicle_breakout_block.scad
// Description: Modular 3D-printed distribution bar for vehicle subframe/beak.
//              Houses 5x latching sockets:
//              1. 12V In (KL15 switched ignition & Ground)
//              2. CAN Bus (CAN_H, CAN_L, GND)
//              3. Mirror BSD (Left & Right amber radar alert LEDs)
//              4. Aux Light / 12V GPS Cradle (Switched 12V via TPS1H100)
//              5. GNSS & Climate Puck (I2C: 3V3, GND, SDA, SCL for SAM-M10Q & TMP117)
//              Includes dovetail mating groove to slide-lock with cockpit_breakout_block.
// =============================================================================

include <../00_common/parameters.scad>;

part = "all"; // [all, body, lid]

// Main dimensions (Standardized 86.0 mm length for flush dovetail mating with Cockpit Satellite)
VEHICLE_BLOCK_L = 86.0;
VEHICLE_BLOCK_W = 28.0;
VEHICLE_BLOCK_H = 18.0;
WALL            = 2.2;

// Dovetail interlocking parameters (matching cockpit_breakout_block)
DOVETAIL_W_BOTTOM = 6.0;
DOVETAIL_W_TOP    = 8.4;
DOVETAIL_H        = 3.0;
DOVETAIL_L        = VEHICLE_BLOCK_L - 10.0;

module dovetail_female(length = DOVETAIL_L + 2.0, clearance = 0.25) {
    linear_extrude(height = length) {
        polygon(points=[
            [-(DOVETAIL_W_BOTTOM/2 + clearance), -0.1],
            [ (DOVETAIL_W_BOTTOM/2 + clearance), -0.1],
            [ (DOVETAIL_W_TOP/2 + clearance),    DOVETAIL_H + 0.1],
            [-(DOVETAIL_W_TOP/2 + clearance),    DOVETAIL_H + 0.1]
        ]);
    }
}

// 1. Vehicle Breakout Main Housing
module vehicle_breakout_body() {
    color([0.22, 0.22, 0.24]) // Charcoal ASA / MJF PA12
    difference() {
        // Main solid rounded housing block
        hull() {
            translate([2.5, 2.5, 0])
                cylinder(r=2.5, h=VEHICLE_BLOCK_H, center=false, $fn=32);
            translate([VEHICLE_BLOCK_L - 2.5, 2.5, 0])
                cylinder(r=2.5, h=VEHICLE_BLOCK_H, center=false, $fn=32);
            translate([2.5, VEHICLE_BLOCK_W - 2.5, 0])
                cylinder(r=2.5, h=VEHICLE_BLOCK_H, center=false, $fn=32);
            translate([VEHICLE_BLOCK_L - 2.5, VEHICLE_BLOCK_W - 2.5, 0])
                cylinder(r=2.5, h=VEHICLE_BLOCK_H, center=false, $fn=32);
        }
        
        // Female Dovetail Slide Groove on South Edge (Y = 0) to mate with Cockpit Satellite
        translate([VEHICLE_BLOCK_L - 5.0, -0.1, 3.5])
            rotate([0, -90, 0])
                rotate([0, 0, 90])
                    dovetail_female();
                    
        // Internal wiring cavity
        translate([WALL, WALL, WALL])
            cube(size=[VEHICLE_BLOCK_L - 2*WALL - 8.0, VEHICLE_BLOCK_W - 2*WALL, VEHICLE_BLOCK_H], center=false);
            
        // Cable Inflow Gland on West Flank (Ø 6.2 mm bore for 12-conductor shielded harness)
        translate([-0.5, VEHICLE_BLOCK_W / 2.0, VEHICLE_BLOCK_H / 2.0])
            rotate([0, 90, 0])
                cylinder(r=3.1, h=WALL + 2.0, center=false, $fn=32);
                
        // Internal zip-tie strain relief channel
        translate([WALL + 3.0, VEHICLE_BLOCK_W/2.0 - 1.25, 0])
            cube(size=[2.5, 2.5, VEHICLE_BLOCK_H - 2.0], center=false);
            
        // 5x COTS Connector Sockets (Top face Z = VEHICLE_BLOCK_H)
        // Spaced along X at 13.0, 27.0, 41.0, 55.0, 69.0 mm
        conn_x = [13.0, 27.0, 41.0, 55.0, 69.0];
        for (cx = conn_x) {
            // Rectangular receptacle pocket for JST-JWPF / JST-SM latching plug (10.5 x 8.0 mm)
            translate([cx - 5.25, 10.0, VEHICLE_BLOCK_H - 12.0])
                cube(size=[10.5, 8.0, 12.5], center=false);
                
            // Latch clearance slot on rear face of socket
            translate([cx - 2.5, 18.0 - 0.1, VEHICLE_BLOCK_H - 8.0])
                cube(size=[5.0, 2.0, 8.5], center=false);
                
            // Solder lead wire passage down to floor
            translate([cx - 4.5, 7.0, WALL - 0.1])
                cube(size=[9.0, 12.0, VEHICLE_BLOCK_H - 10.0], center=false);
        }
        
        // 2x M4 Clearance Holes for direct subframe/beak bracket mounting (X = 5.0 and X = 81.0)
        translate([5.0, VEHICLE_BLOCK_W / 2.0, -0.5])
            cylinder(r=M4_SCREW_HOLE_R, h=VEHICLE_BLOCK_H + 1.0, center=false, $fn=24);
        translate([81.0, VEHICLE_BLOCK_W / 2.0, -0.5])
            cylinder(r=M4_SCREW_HOLE_R, h=VEHICLE_BLOCK_H + 1.0, center=false, $fn=24);
            
        // 2x Captive M4 Hex Nut Pockets on bottom (DIN 934)
        translate([5.0, VEHICLE_BLOCK_W / 2.0, -0.1])
            rotate([0, 0, 30])
                cylinder(r=NUT_M4_SW / (2 * cos(30)), h=NUT_M4_H, center=false, $fn=6);
        translate([81.0, VEHICLE_BLOCK_W / 2.0, -0.1])
            rotate([0, 0, 30])
                cylinder(r=NUT_M4_SW / (2 * cos(30)), h=NUT_M4_H, center=false, $fn=6);
                
        // 2x Zip-Tie Channels on bottom for frame tube fastening (4.0 x 2.2 mm)
        translate([20.0, -0.5, 0])
            cube(size=[4.0, VEHICLE_BLOCK_W + 1.0, 2.2], center=false);
        translate([62.0, -0.5, 0])
            cube(size=[4.0, VEHICLE_BLOCK_W + 1.0, 2.2], center=false);
    }
}

// 2. Weatherproof Snap-On Lid Plate
module vehicle_breakout_lid() {
    color([0.28, 0.28, 0.30])
    difference() {
        translate([WALL + 0.2, WALL + 0.2, VEHICLE_BLOCK_H - 1.5])
            cube(size=[VEHICLE_BLOCK_L - 2*WALL - 8.4, VEHICLE_BLOCK_W - 2*WALL - 0.4, 1.4], center=false);
            
        // Apertures for the 5 connectors
        conn_x = [13.0, 27.0, 41.0, 55.0, 69.0];
        for (cx = conn_x) {
            translate([cx - 5.0, 10.2, VEHICLE_BLOCK_H - 2.0])
                cube(size=[10.0, 7.6, 3.0], center=false);
        }
    }
}

// Render selector
if (part == "lid") {
    vehicle_breakout_lid();
} else if (part == "body") {
    vehicle_breakout_body();
} else {
    vehicle_breakout_body();
    vehicle_breakout_lid();
}
