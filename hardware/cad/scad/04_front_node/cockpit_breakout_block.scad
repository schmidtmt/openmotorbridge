// =============================================================================
// OpenMotorBridge - Cockpit Breakout Satellite Housing
// =============================================================================
// File: hardware/cad/scad/04_front_node/cockpit_breakout_block.scad
// Description: Modular 3D-printed distribution bar for handlebar & cockpit.
//              Houses 5x USB-C female receptacles (Phone 20W, Dongle, Host,
//              Cam 5V, Navi 5V), PTT screw terminal, M3 anti-vibration strain
//              clamp, and lateral dovetail rail for fairing interlock.
// =============================================================================

include <../00_common/parameters.scad>;

part = "all"; // [all, body, clamp]

// Main dimensions
COCKPIT_BLOCK_L = 86.0;
COCKPIT_BLOCK_W = 28.0;
COCKPIT_BLOCK_H = 18.0;
WALL            = 2.2;

// Dovetail interlocking parameters (standardized for both satellites)
DOVETAIL_W_BOTTOM = 6.0;
DOVETAIL_W_TOP    = 8.4;
DOVETAIL_H        = 3.0;
DOVETAIL_L        = COCKPIT_BLOCK_L - 10.0;

module dovetail_male(length = DOVETAIL_L) {
    linear_extrude(height = length) {
        polygon(points=[
            [-DOVETAIL_W_BOTTOM/2, 0],
            [ DOVETAIL_W_BOTTOM/2, 0],
            [ DOVETAIL_W_TOP/2,    DOVETAIL_H],
            [-DOVETAIL_W_TOP/2,    DOVETAIL_H]
        ]);
    }
}

module dovetail_female(length = DOVETAIL_L + 1.0, clearance = 0.25) {
    linear_extrude(height = length) {
        polygon(points=[
            [-(DOVETAIL_W_BOTTOM/2 + clearance), -0.1],
            [ (DOVETAIL_W_BOTTOM/2 + clearance), -0.1],
            [ (DOVETAIL_W_TOP/2 + clearance),    DOVETAIL_H + 0.1],
            [-(DOVETAIL_W_TOP/2 + clearance),    DOVETAIL_H + 0.1]
        ]);
    }
}

// 1. Cockpit Breakout Main Body
module cockpit_breakout_body() {
    color([0.22, 0.22, 0.24]) // Charcoal ASA / MJF PA12
    difference() {
        union() {
            // Main solid rounded housing block
            hull() {
                translate([2.5, 2.5, 0])
                    cylinder(r=2.5, h=COCKPIT_BLOCK_H, center=false, $fn=32);
                translate([COCKPIT_BLOCK_L - 2.5, 2.5, 0])
                    cylinder(r=2.5, h=COCKPIT_BLOCK_H, center=false, $fn=32);
                translate([2.5, COCKPIT_BLOCK_W - 2.5, 0])
                    cylinder(r=2.5, h=COCKPIT_BLOCK_H, center=false, $fn=32);
                translate([COCKPIT_BLOCK_L - 2.5, COCKPIT_BLOCK_W - 2.5, 0])
                    cylinder(r=2.5, h=COCKPIT_BLOCK_H, center=false, $fn=32);
            }
            
            // Lateral Male Dovetail Rail along North edge (Y = COCKPIT_BLOCK_W)
            translate([COCKPIT_BLOCK_L - 5.0, COCKPIT_BLOCK_W, 3.5])
                rotate([0, -90, 0])
                    rotate([0, 0, 90])
                        dovetail_male();
        }
        
        // Internal wiring cavity
        translate([WALL, WALL, WALL])
            cube(size=[COCKPIT_BLOCK_L - 2*WALL - 10.0, COCKPIT_BLOCK_W - 2*WALL, COCKPIT_BLOCK_H], center=false);
            
        // Cable Inflow Gland on West Flank (Ø 6.2 mm bore for 16-wire shielded round harness)
        translate([-0.5, COCKPIT_BLOCK_W / 2.0, COCKPIT_BLOCK_H / 2.0])
            rotate([0, 90, 0])
                cylinder(r=3.1, h=WALL + 2.0, center=false, $fn=32);
                
        // Internal strain-relief zip-tie channel across cable entry
        translate([WALL + 3.0, COCKPIT_BLOCK_W/2.0 - 1.25, 0])
            cube(size=[2.5, 2.5, COCKPIT_BLOCK_H - 2.0], center=false);
            
        // 5x USB-C Receptacle Face Pockets (Top face Z = COCKPIT_BLOCK_H)
        // Spaced along X at 14.0, 26.0, 38.0, 50.0, 62.0 mm
        usb_x = [14.0, 26.0, 38.0, 50.0, 62.0];
        for (ux = usb_x) {
            // Cutout for USB-C female port PCB / flange (9.2 x 3.6 mm)
            translate([ux - 4.6, 6.0, COCKPIT_BLOCK_H - 12.0])
                cube(size=[9.2, 3.6, 12.5], center=false);
                
            // Solder lead / wire clearance underneath
            translate([ux - 5.5, 4.0, WALL - 0.1])
                cube(size=[11.0, 8.0, COCKPIT_BLOCK_H - 10.0], center=false);
        }
        
        // PTT 2-Pin Screw/Spring Terminal cutout at X = 74.0 mm
        translate([74.0 - 5.0, 5.0, COCKPIT_BLOCK_H - 12.0])
            cube(size=[10.0, 8.0, 12.5], center=false);
            
        // 2x M3 Clamping Screw Pilot Holes for strain-relief clamp (X = 6.0 and X = 70.0)
        translate([6.0, 18.0, COCKPIT_BLOCK_H - 10.0])
            cylinder(r=M3_PILOT_HOLE_R, h=10.5, center=false, $fn=24);
        translate([70.0, 18.0, COCKPIT_BLOCK_H - 10.0])
            cylinder(r=M3_PILOT_HOLE_R, h=10.5, center=false, $fn=24);
            
        // 2x Zip-Tie Channels on bottom for handlebar / tube fastening (4.0 x 2.2 mm)
        translate([20.0, -0.5, 0])
            cube(size=[4.0, COCKPIT_BLOCK_W + 1.0, 2.2], center=false);
        translate([56.0, -0.5, 0])
            cube(size=[4.0, COCKPIT_BLOCK_W + 1.0, 2.2], center=false);
    }
}

// 2. Mechanical Anti-Vibration Strain-Relief Clamping Bar
module cockpit_breakout_clamp() {
    color([0.30, 0.30, 0.32]) // Stiff clamp bar
    difference() {
        // Main clamping bar spanning over the 5 USB-C plug necks
        translate([2.0, 13.0, 0])
            cube(size=[74.0, 10.0, 4.5], center=false);
            
        // 2x M3 Clearance Holes
        translate([6.0, 18.0, -0.5])
            cylinder(r=M3_SCREW_HOLE_R, h=6.0, center=false, $fn=24);
        translate([70.0, 18.0, -0.5])
            cylinder(r=M3_SCREW_HOLE_R, h=6.0, center=false, $fn=24);
            
        // M3 Counterbore pockets for DIN 912 socket head screws
        translate([6.0, 18.0, 2.0])
            cylinder(r=3.1, h=3.0, center=false, $fn=24);
        translate([70.0, 18.0, 2.0])
            cylinder(r=3.1, h=3.0, center=false, $fn=24);
            
        // 5x Semicircular clamping grooves for USB-C cable collars
        usb_x = [14.0, 26.0, 38.0, 50.0, 62.0];
        for (ux = usb_x) {
            translate([ux, 13.0 - 0.1, 2.2])
                rotate([-90, 0, 0])
                    cylinder(r=2.5, h=10.5, center=false, $fn=24);
        }
    }
}

// Assembly / Component Selector
if (part == "body") {
    cockpit_breakout_body();
} else if (part == "clamp") {
    cockpit_breakout_clamp();
} else {
    cockpit_breakout_body();
    translate([0, 0, COCKPIT_BLOCK_H + 6.0])
        cockpit_breakout_clamp();
}
