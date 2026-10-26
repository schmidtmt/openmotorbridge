// =============================================================================
// OpenMotorBridge - Satellite Pod: Universal Dual-Actuator Slide Bracket
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/012_universal_actuator_slide_bracket.scad
// Description: Overhead mechatronic actuator gantry spanning directly over
//              OEM communicators (demonstrated with Cardo Packtalk Edge).
//
// Solves:
// "Where and how do the two actuators align over the two buttons?"
// - The Cardo Packtalk Edge sits in its OEM Air-Mount cradle on the floor.
// - Cardo has 3 top ridge keys:
//   1. Front Key (Media / Power) at X = 22.0 mm
//   2. Center Key (Phone) at X = 42.0 mm
//   3. Rear Key (Intercom / Power) at X = 63.0 mm
// - Cold-boot power-on requires pressing Front Key + Rear Key simultaneously!
// - This universal bridge positions Actuator 1 at X = 22.0 mm and Actuator 2
//   at X = 63.0 mm (41 mm span) directly over the two power keys with soft
//   orange TPU pusher tips!
// =============================================================================

include <../../00_common/parameters.scad>;
use <../../00_common/dummies/dummy_intercom_units.scad>;

$fn = 32;

// 1. Sliding Solenoid Carriage (Adjustable along longitudinal bridge slots)
module actuator_overhead_carriage(carriage_color = [0.85, 0.52, 0.12]) {
    color(carriage_color) {
        difference() {
            union() {
                // Main clamping slider body
                translate([-9.0, -10.0, 0])
                    cube([18.0, 20.0, 4.0], center=false);
                // Vertical solenoid clamp collar (Ø 12 mm x 8 mm)
                translate([0, 0, 4.0])
                    cylinder(r=6.0, h=8.0, center=false);
            }
            // Vertical Ø 6.2 mm bore for miniature push-pull solenoid
            translate([0, 0, -2.0])
                cylinder(r=3.1, h=16.0, center=false);
            // Lateral clamp pinch slit (1.2 mm)
            translate([-0.6, 0, 2.0])
                cube([1.2, 10.0, 11.0], center=false);
            // M2.5 locking screw hole
            translate([-7.0, 0, -1.0])
                cylinder(r=1.3, h=6.0, center=false);
        }
    }

    // Installed Micro-Solenoid (Metallic Coil & Spring)
    color("silver") {
        translate([0, 0, 1.0])
            cylinder(r=2.8, h=10.0, center=false);
    }
    // Return spring (Gold)
    color("gold") {
        translate([0, 0, -3.0])
            cylinder(r=1.8, h=4.0, center=false);
    }
    // Plunger shaft extending downward
    color("silver") {
        translate([0, 0, -8.0])
            cylinder(r=1.0, h=10.0, center=false);
    }
    // Soft High-Vis Orange TPU Button Pusher Tip (angulated to match key slope)
    color([0.95, 0.45, 0.10]) {
        translate([0, 0, -8.5])
            hull() {
                cylinder(r=2.5, h=1.8, center=true);
                translate([0, 0, -0.6])
                    cube([7.0, 5.0, 1.0], center=true);
            }
    }
}

// 2. Overhead Gantry Bridge Frame (Spans over Cardo unit)
module actuator_gantry_bridge() {
    bridge_l = 92.0;
    bridge_w = 48.0;
    bridge_h = 24.0; // Clear height above cradle floor

    color([0.22, 0.24, 0.28]) {
        difference() {
            union() {
                // Top horizontal bridge deck (spans over the Cardo)
                translate([0, 0, bridge_h - 3.5])
                    cube([bridge_l, bridge_w, 3.5], center=false);

                // 4x Corner Stilt Pillars (Resting on floor bosses)
                for (cx = [2.0, bridge_l - 8.0]) {
                    // Left flank pillars
                    translate([cx, 0, 0])
                        cube([6.0, 5.0, bridge_h], center=false);
                    // Right flank pillars
                    translate([cx, bridge_w - 5.0, 0])
                        cube([6.0, 5.0, bridge_h], center=false);
                }

                // Stiffening longitudinal top ribs
                translate([0, 0, bridge_h]) {
                    cube([bridge_l, 2.5, 2.5], center=false);
                    translate([0, bridge_w - 2.5, 0])
                        cube([bridge_l, 2.5, 2.5], center=false);
                }
            }

            // Longitudinal adjustment slot directly over the Cardo button line (Y = 17 mm)
            translate([15.0, 17.0, bridge_h - 5.0]) {
                hull() {
                    cylinder(r=2.5, h=10.0, center=false);
                    translate([60.0, 0, 0])
                        cylinder(r=2.5, h=10.0, center=false);
                }
            }

            // 4x M2.5 Floor Fixing Counterbore Holes
            for (cx = [5.0, bridge_l - 5.0]) {
                translate([cx, 2.5, -1.0])
                    cylinder(r=1.4, h=bridge_h + 2.0, center=false);
                translate([cx, bridge_w - 2.5, -1.0])
                    cylinder(r=1.4, h=bridge_h + 2.0, center=false);
            }
        }
    }
}

// 3. Complete Assembly: Cardo Packtalk Edge WITH Overhead Actuators Aligned Over Keys
module cardo_with_overhead_actuator_assembly() {
    // A. Cardo OEM Air-Mount Cradle (Screwed to pod floor)
    dummy_cardo_oem_airmount_cradle();

    // B. Cardo Packtalk Edge (Docked inside cradle)
    translate([0, 0, 3.5])
        dummy_cardo_packtalk_edge(with_actuators = false);

    // C. Overhead Gantry Bridge Frame (Spans over Cardo)
    translate([-4.0, -1.0, 0])
        actuator_gantry_bridge();

    // D. Actuator 1: Positioned at X = 22.0 mm (EXACTLY over Front Media / Power Key)
    translate([22.0, 16.0, 24.0])
        actuator_overhead_carriage(carriage_color = [0.85, 0.48, 0.12]);

    // E. Actuator 2: Positioned at X = 63.0 mm (EXACTLY over Rear Intercom / Power Key)
    translate([63.0, 16.0, 24.0])
        actuator_overhead_carriage(carriage_color = [0.15, 0.55, 0.85]);

    // F. Key Span Dimension Label Indicator (41 mm between keys)
    color([0.2, 0.8, 0.3]) {
        translate([22.0, 36.0, 24.0]) {
            // Dimension line across 41 mm gap
            cube([41.0, 1.2, 1.0], center=false);
            // End ticks
            translate([0, -3.0, 0])
                cube([1.2, 7.0, 1.0], center=false);
            translate([41.0 - 1.2, -3.0, 0])
                cube([1.2, 7.0, 1.0], center=false);
        }
    }
}

// Standalone execution preview
cardo_with_overhead_actuator_assembly();
