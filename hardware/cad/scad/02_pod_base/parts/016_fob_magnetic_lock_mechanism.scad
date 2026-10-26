// =============================================================================
// OpenMotorBridge - Satellite Pod: Central Spring Latch & Lateral Teeth Mechanism
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/016_fob_magnetic_lock_mechanism.scad
// Description: Detail kinematic 3D view of the slot-in lid locking mechanism:
//              - 4 Lateral Locking Teeth (2 on left, 2 on right) engaging sidewall pockets.
//              - Central spring-loaded slider / pinch release on lid top.
//              - Spring tension pushes teeth outward into sidewalls.
//              - Actuation (manual pinch or contactless Smart-Keyfob N52 magnetic release)
//                compresses the central spring and retracts teeth inward.
// =============================================================================

include <../../00_common/parameters.scad>;

RETRACTED = false; // Toggle to true to visualize teeth in retracted state

module central_spring_latch_mechanism() {
    stroke_y = RETRACTED ? 2.5 : 0.0;

    // 1. Cutaway Section of Pod Housing Sidewall (Dark Anthracite PA12)
    color([0.30, 0.32, 0.36, 0.92]) {
        difference() {
            translate([15.0, -10.0, 10.0])
                cube([80.0, 15.0, 26.0], center=false);

            // Sidewall undercut pocket for locking tooth
            translate([35.0 - 4.0, 2.0, 27.5])
                cube([8.0, 4.0, 3.5], center=false);

            // Cutaway window into tooth pocket so the tooth is 100% visible
            translate([20.0, -11.0, 15.0])
                cube([38.0, 18.0, 20.0], center=false);

            // Lid longitudinal guide rail slot
            translate([14.0, 3.5, 27.0])
                cube([82.0, 16.0, 5.0], center=false);
        }
    }

    // 2. Slot-In Lid Body (Translucent Dark Gray)
    color([0.22, 0.23, 0.25, 0.85]) {
        difference() {
            translate([18.0, 4.5, 27.0])
                cube([74.0, 45.0, 4.0], center=false);

            // Central Slider Track & Spring Cavity
            translate([42.0, 20.0, 26.5])
                cube([26.0, 26.0, 4.5], center=false);

            // Cross-Link Channels for Lateral Tooth Arms
            translate([30.0, 4.0, 27.5])
                cube([10.0, 40.0, 3.0], center=false);

            // Inspection cut window over linkage channel
            translate([29.0, 4.0, 29.5])
                cube([12.0, 22.0, 3.0], center=false);
        }
    }

    // 3. Lateral Locking Tooth & Retracting Arm (Orange - engages sidewall pocket!)
    color([0.90, 0.52, 0.12]) {
        // Left locking tooth (X = 35 mm)
        translate([35.0 - 3.5, 2.2 + stroke_y, 28.0]) {
            // Tooth head engaging sidewall pocket
            hull() {
                cube([7.0, 3.5, 2.8], center=false);
                translate([1.0, 2.5, 0])
                    cube([5.0, 1.0, 2.8], center=false);
            }
            // Connecting linkage arm to central spring slider
            translate([1.5, 3.0, 0.4])
                cube([4.0, 22.0, 2.0], center=false);
        }
    }

    // 4. Central Spring-Loaded Slider & Return Spring (Cobalt Blue & Silver)
    // Central Slider Block
    color([0.15, 0.45, 0.85]) {
        translate([44.0, 22.0 + stroke_y, 28.0]) {
            cube([22.0, 16.0, 4.5], center=false);
            // Tactile pinch ridges on top of slider
            for (gx = [2.0 : 3.5 : 18.0]) {
                translate([gx, 8.0, 4.5])
                    cube([1.5, 12.0, 1.0], center=true);
            }
        }
    }

    // Central Coil Return Spring (Silver)
    color("silver") {
        translate([55.0, 41.0, 30.2]) {
            rotate([90, 0, 0])
                cylinder(r=2.2, h=10.0 + stroke_y, center=false, $fn=16);
        }
    }

    // 5. Embedded Steel/Neodymium Detent Core (Crimson Red) for FOB Magnetic Release
    color("crimson") {
        translate([55.0, 24.0 + stroke_y, 29.5])
            cylinder(r=3.5, h=2.5, center=true, $fn=24);
    }

    // 6. External Smart-Keyfob (PCBA 07) Hovering Over Release Target
    translate([55.0, 24.0, 39.0]) {
        // Keyfob Shell
        color([0.15, 0.15, 0.15, 0.75])
            cylinder(r=11.0, h=5.0, center=false, $fn=32);

        // N52 Permanent Magnet Core
        color("crimson")
            translate([0, 0, 0.5])
                cylinder(r=4.5, h=4.0, center=false, $fn=24);
    }
}

// Standalone execution preview
central_spring_latch_mechanism();
