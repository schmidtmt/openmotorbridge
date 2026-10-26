// =============================================================================
// OpenMotorBridge - Satellite Pod: Compliant FOB Magnetic Latch (Slide-In Lid)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/016_fob_magnetic_lock_mechanism.scad
// Description: Intuitive, 1-piece compliant spring latch (monolithische PA12-Federzunge)
//              for the slide-in lid. Eliminates loose axles, rocker beams, and springs.
//
// How It Works:
// 1. A flexible spring tongue (elastische Federzunge) is 3D-printed directly into the
//    PA12 housing wall.
// 2. The tongue has an integrated 90° locking barb with a 30° push-to-close ramp.
// 3. A ferromagnetic steel/neodymium slug (Ø 6.0 mm x 2.0 mm) is press-fitted into the tongue.
// 4. In normal resting state, the spring tongue positively blocks the slide-in lid.
// 5. When the Smart-Keyfob (PCBA 07) approaches, magnetic attraction flexes the
//    spring tongue downward by 2.5 mm, releasing the lid smoothly and contact-free.
// =============================================================================

include <../../00_common/parameters.scad>;

FLEXED = false; // Set to true to view the magnetic release deflection

module fob_magnetic_lock_mechanism() {
    deflection_z = FLEXED ? -2.8 : 0.0;

    // 1. Cutaway Section of Pod Housing Wall with Integrated Spring Tongue
    color([0.35, 0.38, 0.42]) {
        // Main wall block
        difference() {
            translate([15.0, -8.0, 10.0])
                cube([80.0, 16.0, 24.0], center=false);

            // Pocket around compliant tongue (giving room to flex downward)
            translate([34.0, -9.0, 15.0])
                cube([38.0, 12.0, 18.0], center=false);

            // Slide lid guide groove at top
            translate([14.0, 0.0, 29.5])
                cube([82.0, 18.0, 5.0], center=false);
        }
    }

    // 2. Monolithic PA12 Compliant Spring Tongue (colored amber for clear visualization)
    color([0.88, 0.55, 0.15]) {
        translate([0, 0, deflection_z]) {
            // Flexible cantilever beam (2.0 mm thick leaf, elastic in PA12)
            translate([35.0, -3.0, 18.0])
                cube([25.0, 4.0, 2.2], center=false);

            // Rigid tongue head with locking barb
            translate([60.0, -3.0, 18.0]) {
                difference() {
                    union() {
                        // Head block
                        cube([10.0, 5.0, 11.5], center=false);
                        // 30° push-to-close lead-in chamfer
                        translate([0, 0, 11.5])
                            rotate([0, 30, 0])
                                cube([8.0, 5.0, 2.0], center=false);
                    }
                    // Pocket for ferromagnetic steel anchor disc (Ø 6.2 mm x 2.2 mm)
                    translate([5.0, 2.5, 9.0])
                        cylinder(r=3.1, h=2.5, center=true, $fn=24);
                }
            }

            // Ferromagnetic Steel Anchor Disc (Crimson Red)
            color("crimson")
                translate([65.0, -0.5, 27.0])
                    cylinder(r=3.0, h=2.0, center=true, $fn=24);
        }
    }

    // 3. Slide-In Lid Section (Dark Anthracite)
    color([0.22, 0.23, 0.25, 0.88]) {
        difference() {
            translate([15.0, 1.0, 29.5])
                cube([80.0, 22.0, 4.0], center=false);

            // 90° Locking Detent Pocket in Lid Underside
            translate([60.5, 0.0, 28.5])
                cube([9.5, 8.0, 3.5], center=false);

            // Tactile Keyfob Target Circle on Lid Top
            translate([65.0, 12.0, 33.1]) {
                difference() {
                    cylinder(r=7.0, h=0.6, center=false, $fn=32);
                    cylinder(r=5.5, h=0.7, center=false, $fn=32);
                }
            }
        }
    }

    // 4. External Smart-Keyfob (PCBA 07) Hovering Over Target
    translate([65.0, 12.0, 38.0]) {
        // Keyfob Shell (Translucent Dark Gray)
        color([0.15, 0.15, 0.15, 0.75])
            cylinder(r=11.0, h=5.0, center=false, $fn=32);

        // N52 Permanent Magnet Core (Red Neodymium)
        color("crimson")
            translate([0, 0, 0.5])
                cylinder(r=4.5, h=4.0, center=false, $fn=24);
    }
}

// Standalone execution preview
fob_magnetic_lock_mechanism();
