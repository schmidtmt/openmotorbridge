// =============================================================================
// OpenMotorBridge - Satellite Pod: FOB Magnetic Latch Kinematics (Slide-In Lid)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/016_fob_magnetic_lock_mechanism.scad
// Description: Detailed 3D kinematic inspection of the contactless FOB magnetic
//              anti-theft latch for the slide-in lid.
//
// Kinematics:
// 1. Pivot pin (M2 stainless steel dowel) at X = 58 mm.
// 2. Rear arm (X = 45 mm): Ø 6.0 mm ferromagnetic steel anchor disc and V4A leaf spring.
// 3. Front arm (X = 72 mm): 90° vertical locking pawl and 30° push-to-close ramp.
// 4. Slide-in lid above: Underbody 90° detent pocket.
// 5. External Smart-Keyfob (PCBA 07) with N52 Neodymium magnet applied to target zone.
// =============================================================================

include <../../00_common/parameters.scad>;

UNLOCKED = false; // Set to true to view the magnet-pulled open position

module fob_magnetic_lock_mechanism() {
    swing_angle = UNLOCKED ? -6.5 : 0.0; // Degrees downward

    // 1. Reference Housing Rim Mounting Bracket
    color([0.45, 0.48, 0.52]) {
        // Rear mounting bracket for pivot pin
        translate([56.0, -10.0, 14.0])
            cube([4.0, 8.0, 14.0], center=false);
        // Bottom floor seat for leaf spring
        translate([36.0, -8.0, 14.0])
            cube([24.0, 8.0, 2.0], center=false);
    }

    // 2. Slide-In Lid Section (Dark Anthracite with Cutaway)
    color([0.22, 0.23, 0.25, 0.9]) {
        difference() {
            translate([20.0, 0.0, 28.5])
                cube([75.0, 18.0, 4.0], center=false);
            // 90° Locking Pawl Detent Pocket
            translate([68.0, -0.5, 27.5])
                cube([4.5, 8.0, 3.5], center=false);
            // 30° Lead-In Chamfer
            translate([68.0, -0.5, 29.5])
                rotate([0, 30, 0])
                    cube([5.0, 8.0, 3.0], center=false);
            // Engraved Keyfob Target Circle on Lid Top
            translate([45.0, 8.0, 32.1]) {
                difference() {
                    cylinder(r=6.5, h=0.6, center=false, $fn=32);
                    cylinder(r=5.0, h=0.7, center=false, $fn=32);
                }
            }
        }
    }

    // 3. External Smart-Keyfob (PCBA 07) Hovering Over Target (Dark Shell with N52 Magnet)
    translate([45.0, 8.0, 37.0]) {
        // Keyfob Shell
        color([0.18, 0.18, 0.20, 0.85])
            cylinder(r=10.0, h=4.0, center=false, $fn=32);
        // N52 Permanent Magnet (Red Cylindrical Core)
        color("crimson")
            translate([0, 0, -0.5])
                cylinder(r=4.0, h=3.0, center=false, $fn=24);
    }

    // 4. Pivoting Locking Rocker Lever (First-Class Lever)
    translate([58.0, 0.0, 24.0]) {
        rotate([0, swing_angle, 0]) {
            // Main Rocker Lever Body (Brass / V4A Silver)
            color("silver") {
                translate([-14.0, -2.0, -2.5])
                    cube([28.0, 4.0, 5.0], center=false);

                // Front Locking Pawl (Vertical Tooth with 30° Lead-In)
                translate([11.0, -2.0, 2.5]) {
                    difference() {
                        cube([3.5, 4.0, 6.5], center=false);
                        // 30° lead-in ramp on top face
                        translate([3.5, -0.5, 6.5])
                            rotate([0, -60, 0])
                                cube([6.0, 5.0, 6.0], center=false);
                    }
                }
            }

            // Ferromagnetic Steel Anchor Disc (at X = 45 mm -> rel X = -13 mm)
            color("crimson") {
                translate([-13.0, 0.0, 2.0])
                    cylinder(r=3.0, h=2.5, center=false, $fn=24);
            }
        }

        // M2 Stainless Steel Dowel Pin (Pivot Axis)
        color("gold") {
            translate([0, -6.0, 0])
                rotate([-90, 0, 0])
                    cylinder(r=1.0, h=12.0, center=false, $fn=20);
        }
    }

    // 5. V4A Return Leaf Spring (Pushing rear arm upwards)
    color("goldenrod") {
        translate([38.0, -1.5, 17.0])
            cube([12.0, 3.0, 1.2], center=false);
        translate([48.0, -1.5, 17.0])
            rotate([0, -25, 0])
                cube([8.0, 3.0, 1.0], center=false);
    }
}

// Standalone execution preview
fob_magnetic_lock_mechanism();
