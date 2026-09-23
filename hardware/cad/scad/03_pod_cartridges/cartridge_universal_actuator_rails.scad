// =============================================================================
// OpenMotorBridge - Smart Cartridge: Universal Actuator Rails & 2D Raster Plate
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_universal_actuator_rails.scad
// Description: Universal button actuation system for any third-party intercom,
//              pager, or radio transceiver placed inside the Smart Cartridge:
//              1. 2D Slotted Raster Lid (3mm pitch matrix & slotted guide rails)
//                 for pressing top-face buttons with Ø 6mm micro-solenoids.
//              2. Independent Left & Right Lateral Bracket Arms that slide along
//                 the sled flanks to actuate side rocker/volume keys at any position.
//              3. Eliminates custom CAD redesigns for future intercom generations.
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <00_base_sled.scad>;

RASTER_L        = 110.0;  // Length in X matching standard cartridge bay (mm)
RASTER_W        = 53.0;   // Width in Y (mm)
RASTER_THICK    = 3.2;    // Rigid plate thickness (mm)
ACTUATOR_BORE   = 6.2;    // Ø for standard 6mm miniature push-pull micro-solenoid
RASTER_PITCH_X  = 6.0;    // Grid pitch along X (mm)
RASTER_PITCH_Y  = 6.0;    // Grid pitch along Y (mm)

// 1. 2D Slotted Raster Plate (Top-Face Button Actuator Carrier)
module universal_actuator_raster_lid() {
    difference() {
        union() {
            // Main rigid partition deck
            cube([RASTER_L, RASTER_W, RASTER_THICK], center=false);

            // Perimeter reinforcement rim
            difference() {
                translate([0, 0, RASTER_THICK])
                    cube([RASTER_L, RASTER_W, 2.5], center=false);
                translate([2.5, 2.5, RASTER_THICK - 0.1])
                    cube([RASTER_L - 5.0, RASTER_W - 5.0, 3.0], center=false);
            }

            // Lateral slide dovetail tabs for left/right bracket clamping
            for (dx = [25.0, 55.0, 85.0]) {
                translate([dx - 5.0, -1.8, 0])
                    cube([10.0, 1.8, RASTER_THICK + 1.0], center=false);
                translate([dx - 5.0, RASTER_W, 0])
                    cube([10.0, 1.8, RASTER_THICK + 1.0], center=false);
            }
        }

        // --- SUBTRACTIONS ---

        // 4x Corner Screwdriver / M2 Mount Clearances
        translate([3.5, 3.5, -1.0]) cylinder(r=1.6, h=8.0, center=false, $fn=16);
        translate([RASTER_L - 3.5, 3.5, -1.0]) cylinder(r=1.6, h=8.0, center=false, $fn=16);
        translate([3.5, RASTER_W - 3.5, -1.0]) cylinder(r=1.6, h=8.0, center=false, $fn=16);
        translate([RASTER_L - 3.5, RASTER_W - 3.5, -1.0]) cylinder(r=1.6, h=8.0, center=false, $fn=16);

        // 2D Matrix of Actuator Mounting Holes & Slots (X = 15 .. 95, Y = 10 .. 43)
        for (x = [18.0 : RASTER_PITCH_X : RASTER_L - 18.0]) {
            for (y = [12.0 : RASTER_PITCH_Y : RASTER_W - 12.0]) {
                // Actuator bore
                translate([x, y, -0.5])
                    cylinder(r=ACTUATOR_BORE/2.0, h=RASTER_THICK + 1.0, center=false, $fn=24);
                // Dual M2 counter-clamp screw holes flanking each solenoid bore
                translate([x, y - 4.5, -0.5])
                    cylinder(r=1.1, h=RASTER_THICK + 1.0, center=false, $fn=16);
                translate([x, y + 4.5, -0.5])
                    cylinder(r=1.1, h=RASTER_THICK + 1.0, center=false, $fn=16);
            }
        }

        // Central Wiring & Visual Inspection Slot (along centerline X = 35 .. 75)
        translate([35.0, RASTER_W/2.0 - 4.0, -1.0])
            cube([40.0, 8.0, RASTER_THICK + 2.0], center=false);
    }
}

// 2. Modular Lateral Actuator Bracket Arm (Left or Right Flank)
module lateral_actuator_bracket_arm(side = "left") {
    y_sign = (side == "left") ? -1 : 1;

    difference() {
        union() {
            // Dovetail Slider Shoe (snaps onto sled top/flank rim)
            translate([-7.5, 0, 0])
                cube([15.0, 4.0, 16.0], center=false);

            // Cantilever Outrigger Arm extending downwards over intercom flank
            translate([-6.0, y_sign * 2.0, -12.0])
                cube([12.0, 6.0, 14.0], center=false);

            // Actuator Clamp Head (Holds horizontal Ø 6mm micro-solenoid facing inward)
            translate([0, y_sign * 9.0, -8.0]) {
                rotate([90, 0, 0])
                    cylinder(r=5.5, h=8.0, center=true, $fn=32);
            }
        }

        // Horizontal Actuator Bore (Ø 6.2 mm) facing inwards into intercom button
        translate([0, y_sign * 9.0, -8.0]) {
            rotate([90, 0, 0])
                cylinder(r=ACTUATOR_BORE/2.0, h=14.0, center=true, $fn=24);
        }

        // Pinch Clamping Slot (1.2 mm split to clamp solenoid with M2 bolt)
        translate([-0.6, y_sign * 3.0, -14.0])
            cube([1.2, 12.0, 12.0], center=false);

        // Clamping screw bore (M2 across split)
        translate([-8.0, y_sign * 9.0, -8.0])
            rotate([0, 90, 0])
                cylinder(r=1.2, h=16.0, center=false, $fn=16);

        // Dovetail rail engagement slot
        translate([-8.0, -0.5, 1.0])
            cube([16.0, 2.5, 5.0], center=false);
    }
}

// 3. Full 3D Assembly Preview
module universal_actuator_assembly() {
    // A. Cartridge Base Sled
    color("darkslategray", 0.9)
        cartridge_base_sled(show_latch = true);

    // B. 2D Slotted Raster Lid
    color("steelblue", 0.92)
        translate([2.5, 2.5, 8.5])
            universal_actuator_raster_lid();

    // C. Sample Top-Face 6mm Micro-Solenoid (Centered on intercom key)
    color("gold")
        translate([55.0, RASTER_W/2.0 + 2.5, 12.0])
            cylinder(r=3.0, h=12.0, center=false, $fn=24);

    // D. Left Lateral Actuator Bracket
    color("crimson", 0.95)
        translate([42.0, 2.5, 10.0])
            lateral_actuator_bracket_arm(side = "left");

    // E. Right Lateral Actuator Bracket
    color("forestgreen", 0.95)
        translate([68.0, RASTER_W + 2.5, 10.0])
            lateral_actuator_bracket_arm(side = "right");
}

universal_actuator_assembly();
