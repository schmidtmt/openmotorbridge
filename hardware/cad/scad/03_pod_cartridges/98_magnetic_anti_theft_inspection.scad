// =============================================================================
// OpenMotorBridge - Magnetic Anti-Theft Lock Functional Inspection & Kinematics
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/98_magnetic_anti_theft_inspection.scad
// Description: Interactive kinematic and clearance verification scene for the
//              patented OpenMotorBridge magnetic anti-theft cartridge lock:
//
//   1. LOCKED STATE (Default, LOCKED_STATE = true):
//      - Internal compression spring pushes rear rocker arm inwards.
//      - 1st-class lever pivots on M2 stainless steel dowel pin (X = 58 mm).
//      - Sawtooth pawl protrudes 2.5 mm into the housing's internal detent pocket.
//      - 90° front stop face creates absolute positive form-fit locking.
//      - Sled is 100% locked against theft or pull-out without key!
//
//   2. UNLOCKED & EJECTED STATE (LOCKED_STATE = false):
//      - External N52 Neodymium key block (20x10x5 mm) applied to outer wall mark.
//      - Magnetic flux pulls the Ø 6x8 mm ferromagnetic steel anchor outwards.
//      - Sawtooth pawl swings 2.5 mm inwards flush into the guide rail pocket.
//      - Dual V4A ejection coil springs immediately pop the cartridge outward
//        by 25 mm for effortless, one-handed removal!
// =============================================================================

include <../00_common/parameters.scad>;
use <00_base_sled.scad>;
use <parts/05_magnetic_lock_latch.scad>;
use <../02_pod_base/pod_base_housing.scad>;

// Interactive Mode Toggle:
LOCKED_STATE = true; // Set to false to inspect magnet-unlocked ejection motion!

// Kinematic parameters
ROCKER_SWING_ANGLE = LOCKED_STATE ? 0.0 : -4.8; // Degrees
EJECT_TRAVEL_X     = LOCKED_STATE ? 0.0 : 25.0; // Cartridge pop-out distance (mm)

LATCH_PIVOT_X      = 58.0;
LATCH_MAGNET_X     = 46.0;
LATCH_TOOTH_X      = 70.0;

module magnetic_anti_theft_inspection() {
    // 1. Pod Base Housing - Transparent Cutaway View (Left Half)
    color("slategray", 0.45) {
        difference() {
            pod_base_housing();
            // Longitudinal cutaway along Y = 35 mm centerline to inspect internal latching
            translate([-10.0, POD_OUTER_W/2.0, -10.0])
                cube([POD_OUTER_L + 20.0, POD_OUTER_W, POD_OUTER_H + 20.0]);
        }
    }

    // 2. Dual V4A Ejection Coil Springs (at Bulkhead x = 18 mm)
    color("gold") {
        spring_len = LOCKED_STATE ? 6.5 : (6.5 + EJECT_TRAVEL_X);
        translate([POD_BULKHEAD_X + 2.0, 16.0, POD_OUTER_H/2.0])
            rotate([0, 90, 0])
                cylinder(r=2.8, h=spring_len, $fn=16);
        translate([POD_BULKHEAD_X + 2.0, POD_OUTER_W - 16.0, POD_OUTER_H/2.0])
            rotate([0, 90, 0])
                cylinder(r=2.8, h=spring_len, $fn=16);
    }

    // 3. Cartridge Base Sled (Anthracite PA12 with Anti-Theft Rocker Pocket)
    translate([POD_BULKHEAD_X + 1.0 + EJECT_TRAVEL_X, (POD_OUTER_W - CARTRIDGE_BASE_W)/2.0, POD_WALL]) {
        color("#222831", 0.88)
            cartridge_base_sled(magnetic_lock = true);

        // 4. Kinematic Rocker Lever Assembly
        translate([0, 0, POD_GROOVE_LEFT_Z - CARTRIDGE_TONGUE_W/2.0 + 3.0]) {
            // Pivot around M2 stainless steel axis at (X = 58, Y = 1.25)
            translate([LATCH_PIVOT_X, 1.25, 0]) {
                rotate([0, 0, ROCKER_SWING_ANGLE]) {
                    translate([-LATCH_PIVOT_X, -1.25, 0]) {
                        // The Rocker Lever Body (Tough Red/Orange PA12-CF)
                        color(LOCKED_STATE ? "#30d158" : "#ff9f0a", 1.0)
                            magnetic_lock_rocker_lever();

                        // Ferromagnetic Steel Dowel Pin (Ø 6 x 8 mm)
                        color("silver", 1.0)
                            translate([LATCH_MAGNET_X, 0, 0])
                                rotate([90, 0, 0])
                                    cylinder(r=3.0, h=8.0, center=true, $fn=24);

                        // Return Compression Spring (Ø 3.5 x 10 mm)
                        color("goldenrod", 1.0)
                            translate([LATCH_MAGNET_X, 2.0, 0])
                                rotate([-90, 0, 0])
                                    cylinder(r=1.75, h=LOCKED_STATE ? 6.0 : 4.2, $fn=16);
                    }
                }

                // M2 Stainless Steel Dowel Pin (Hinge Axis)
                color("silver", 1.0)
                    cylinder(r=1.0, h=8.0, center=true, $fn=16);
            }
        }
    }

    // 5. External N52 Neodymium Key Magnet (Appears only during unlocking)
    if (!LOCKED_STATE) {
        // Positioned precisely over the alignment mark on outer left wall
        color("#ff453a", 0.95) {
            translate([POD_BULKHEAD_X + 1.0 + LATCH_MAGNET_X, -8.0, POD_GROOVE_LEFT_Z]) {
                cube([20.0, 6.0, 10.0], center=true);
                // North/South Pole Marker Line
                color("white")
                    translate([0, -3.1, 0])
                        cube([1.5, 0.2, 8.0], center=true);
            }
        }

        // Visual Magnetic Flux Lines (Cyan indicator)
        color("#00f2fe", 0.7) {
            translate([POD_BULKHEAD_X + 1.0 + LATCH_MAGNET_X, -2.0, POD_GROOVE_LEFT_Z])
                rotate([90, 0, 0])
                    cylinder(r=2.5, h=5.0, center=true, $fn=16);
        }
    }
}

// Render functional inspection scene
magnetic_anti_theft_inspection();
