// =============================================================================
// OpenMotorBridge - Satellite Pod: Universal Dual-Carriage Actuator Slide Bracket
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/012_universal_actuator_slide_bracket.scad
// Description: "One Size Fits All" Universal Mechatronic Dual-Carriage Slide Bridge.
//
// Key Architectural Principles (v10.0 Monocoque Pod):
// 1. 100% Universal ("One Size Fits All"):
//    - Fully replaces OEM-specific adapter plates.
//    - Compatible with Cardo Packtalk Edge, Sena 50S / 30K, Sena SPIDER ST1/RT1,
//      Midland BTR1, generic PMR446 radios, or custom communicators.
// 2. Rigid 4-Point Chassis Portal Bridge:
//    - Spans over the rear equipment chamber from X = 56.0 mm to X = 140.0 mm (84 mm span).
//    - 4x solid corner pillars bolt directly into the 4x M2.5 brass threaded inserts
//      in the pod monocoque floor bosses at:
//      (56.0, 14.0), (56.0, 56.0), (140.0, 14.0), (140.0, 56.0).
// 3. Dual Longitudinal Slotted Guide Rails (C-Nuten / Langlöcher):
//    - Two parallel guide slots allow continuous X-adjustment from 15 mm to 75 mm
//      button spacing.
// 4. Two Independent Clamping Carriages (Schiebeschlitten 1 & 2):
//    - Carriage 1 (Front): Slide along Rail 1 (Y ≈ 13 mm), locked via M2.5 clamp screw.
//    - Carriage 2 (Rear): Slide along Rail 2 (Y ≈ 28 mm), locked via M2.5 clamp screw.
//    - Each carriage holds one flat 5V micro-solenoid with soft Shore A50 TPU pad.
// 5. Zero-Play Vibration Resistance & Reaction Force Compensation:
//    - Bolted firmly into the chassis with 4x M2.5 Torx stainless steel screws.
//    - Button actuation reaction forces (3..5 N) transfer directly into the 3 mm
//      carbon-reinforced PA12 chassis floor -- zero flexing, zero slipping.
// =============================================================================

include <../../00_common/parameters.scad>;
use <../../00_common/dummies/dummy_intercom_units.scad>;

$fn = 32;

// Universal Dual-Carriage Actuator Slide Bracket
module universal_actuator_slide_bracket(
    carriage1_x = 22.0,   // Position of Carriage 1 along slot (default: Cardo Media key)
    carriage2_x = 63.0,   // Position of Carriage 2 along slot (default: Cardo Intercom key)
    show_actuators = true
) {
    // 4-Point Mounting Hole Centers (matching floor bosses at X = 56, 140; Y = 14, 56)
    span_x = 84.0;
    span_y = 42.0;
    deck_th = 2.5;
    deck_z = 21.0; // Height of deck underside above boss tops
    pillar_w = 8.0;
    pillar_l = 8.0;

    // 1. Injection-Molded / SLS PA12 Carbon Portal Bridge Main Frame
    color([0.20, 0.22, 0.25]) {
        difference() {
            union() {
                // Top Bridge Deck (spanning between all 4 pillars)
                translate([-pillar_l/2.0, -pillar_w/2.0, deck_z])
                    cube([span_x + pillar_l, span_y + pillar_w, deck_th], center=false);

                // 4x Solid Corner Standoff Pillars (reaching down to tub floor bosses)
                for (px = [0, span_x]) {
                    for (py = [0, span_y]) {
                        translate([px - pillar_l/2.0, py - pillar_w/2.0, 0])
                            cube([pillar_l, pillar_w, deck_z], center=false);
                    }
                }

                // Longitudinal Side Reinforcement Trusses (Left and Right Flanks)
                translate([-pillar_l/2.0, -pillar_w/2.0, deck_z - 3.5])
                    cube([span_x + pillar_l, 4.0, 3.5], center=false);
                translate([-pillar_l/2.0, span_y + pillar_w/2.0 - 4.0, deck_z - 3.5])
                    cube([span_x + pillar_l, 4.0, 3.5], center=false);

                // Transverse End Trusses (Front and Rear Arches)
                translate([-pillar_l/2.0, -pillar_w/2.0, deck_z - 3.5])
                    cube([4.0, span_y + pillar_w, 3.5], center=false);
                translate([span_x + pillar_l/2.0 - 4.0, -pillar_w/2.0, deck_z - 3.5])
                    cube([4.0, span_y + pillar_w, 3.5], center=false);
            }

            // 4x M2.5 Screw Counterbore Holes into Floor Bosses
            for (px = [0, span_x]) {
                for (py = [0, span_y]) {
                    // Screw clearance shaft through pillar
                    translate([px, py, -1.0])
                        cylinder(r=1.4, h=deck_z + deck_th + 2.0, $fn=20);
                    // Screw head counterbore recess in top deck
                    translate([px, py, deck_z + deck_th - 1.2])
                        cylinder(r=2.5, h=2.0, $fn=24);
                }
            }

            // Central Inspection / Display Cutout Window
            translate([30.0, 10.0, deck_z - 1.0])
                cube([24.0, span_y - 20.0, deck_th + 2.0], center=false);

            // Rail 1: Slotted Guide Rail (Langloch 1) along X (Y = 12.0 mm, span 12..72 mm)
            translate([12.0, 12.0, deck_z - 1.0])
                hull() {
                    cylinder(r=1.6, h=deck_th + 2.0, $fn=16);
                    translate([58.0, 0, 0])
                        cylinder(r=1.6, h=deck_th + 2.0, $fn=16);
                }

            // Rail 2: Slotted Guide Rail (Langloch 2) along X (Y = 30.0 mm, span 12..72 mm)
            translate([12.0, 30.0, deck_z - 1.0])
                hull() {
                    cylinder(r=1.6, h=deck_th + 2.0, $fn=16);
                    translate([58.0, 0, 0])
                        cylinder(r=1.6, h=deck_th + 2.0, $fn=16);
                }
        }
    }

    // 2. 4x M2.5 Stainless Steel Torx Chassis Fastening Screws (Bolted into tub floor brass inserts)
    color("silver") {
        for (px = [0, span_x]) {
            for (py = [0, span_y]) {
                translate([px, py, deck_z + deck_th - 1.0]) {
                    cylinder(r=2.3, h=1.8, center=false, $fn=20);
                    translate([0, 0, 1.8]) cylinder(r=1.0, h=0.2, center=false, $fn=6); // hex socket
                    translate([0, 0, -deck_z - 3.0]) cylinder(r=1.25, h=deck_z + 3.0, center=false, $fn=16);
                }
            }
        }
    }

    if (show_actuators) {
        // =========================================================================
        // CARRIAGE 1 (Front Key Actuator - Continuously Adjustable in X)
        // =========================================================================
        translate([carriage1_x, 12.0, deck_z]) {
            // Slider Carriage Body
            color([0.28, 0.30, 0.34]) {
                difference() {
                    translate([-6.0, -6.0, 0])
                        cube([12.0, 12.0, 3.5], center=false);
                    // Clamp screw bore
                    translate([0, 0, -1.0])
                        cylinder(r=1.4, h=6.0, $fn=16);
                }
            }

            // M2.5 Clamping Knurled / Hex Locking Screw
            color("silver") {
                translate([0, 0, 3.5]) {
                    cylinder(r=2.2, h=2.0, center=false, $fn=20);
                    translate([0, 0, 2.0]) cylinder(r=0.9, h=0.2, center=false, $fn=6);
                }
            }

            // Micro-Actuator (Flat Horizontal Solenoid with 90° Downward Bellcrank Rocker)
            color("silver")
                translate([8.0, 0, 1.8])
                    rotate([0, 90, 0])
                        cylinder(r=2.2, h=12.0, center=true, $fn=20);
            color("gold")
                translate([2.0, 0, 1.8])
                    rotate([0, 90, 0])
                        cylinder(r=1.5, h=3.0, center=true, $fn=16);

            // 90° Downward Bellcrank Rocker (Orange Anodized Aluminum)
            color([0.92, 0.45, 0.10]) {
                translate([0, 0, -2.5]) {
                    rotate([0, 12, 0])
                        cube([3.0, 2.4, 5.0], center=true);
                    translate([3.0, 0, 1.8])
                        cube([6.0, 1.8, 1.6], center=true);
                }
            }
            // Front Soft Shore A50 TPU Pusher Tip
            color([1.0, 0.6, 0.1])
                translate([0, 0, -5.5])
                    cylinder(r=2.2, h=2.0, center=true, $fn=16);
        }

        // =========================================================================
        // CARRIAGE 2 (Rear Key Actuator - Continuously Adjustable in X)
        // =========================================================================
        translate([carriage2_x, 30.0, deck_z]) {
            // Slider Carriage Body
            color([0.28, 0.30, 0.34]) {
                difference() {
                    translate([-6.0, -6.0, 0])
                        cube([12.0, 12.0, 3.5], center=false);
                    // Clamp screw bore
                    translate([0, 0, -1.0])
                        cylinder(r=1.4, h=6.0, $fn=16);
                }
            }

            // M2.5 Clamping Knurled / Hex Locking Screw
            color("silver") {
                translate([0, 0, 3.5]) {
                    cylinder(r=2.2, h=2.0, center=false, $fn=20);
                    translate([0, 0, 2.0]) cylinder(r=0.9, h=0.2, center=false, $fn=6);
                }
            }

            // Micro-Actuator (Flat Horizontal Solenoid with 90° Downward Bellcrank Rocker)
            color("silver")
                translate([8.0, 0, 1.8])
                    rotate([0, 90, 0])
                        cylinder(r=2.2, h=12.0, center=true, $fn=20);
            color("gold")
                translate([2.0, 0, 1.8])
                    rotate([0, 90, 0])
                        cylinder(r=1.5, h=3.0, center=true, $fn=16);

            // 90° Downward Bellcrank Rocker (Blue Anodized Aluminum)
            color([0.15, 0.48, 0.88]) {
                translate([0, 0, -2.5]) {
                    rotate([0, 12, 0])
                        cube([3.0, 2.4, 5.0], center=true);
                    translate([3.0, 0, 1.8])
                        cube([6.0, 1.8, 1.6], center=true);
                }
            }
            // Rear Soft Shore A50 TPU Pusher Tip
            color([0.2, 0.7, 1.0])
                translate([0, 0, -5.5])
                    cylinder(r=2.2, h=2.0, center=true, $fn=16);
        }

        // Flat Actuator Ribbon Cable (routes forward to PCBA 03 J_ACT)
        color([0.15, 0.15, 0.15]) {
            translate([-pillar_l/2.0 - 15.0, 18.0, deck_z + 0.8])
                cube([25.0, 6.0, 0.6], center=false);
            translate([-pillar_l/2.0 - 19.0, 18.0, deck_z + 0.2])
                cube([4.0, 6.0, 2.0], center=false);
        }
    }
}

// Complete assembly: Universal Slide Bridge mounted over Cardo Packtalk Edge
module cardo_with_universal_slide_bracket_assembly() {
    // A. Cardo OEM Air-Mount Cradle (Screwed to pod floor)
    translate([6.0, (42.0 - 46.0)/2.0 + 1.0, 0])
        dummy_cardo_oem_airmount_cradle();

    // B. Cardo Packtalk Edge (Docked inside cradle)
    translate([6.0, (42.0 - 46.0)/2.0 + 1.0, 3.5])
        dummy_cardo_packtalk_edge(with_actuators = false);

    // C. Universal Dual-Carriage Slide Bracket (Bolted into the 4 floor bosses)
    // Carriage 1 aligned over Front Media key (X = 28.0), Carriage 2 over Rear Intercom key (X = 69.0)
    universal_actuator_slide_bracket(
        carriage1_x = 28.0,
        carriage2_x = 69.0,
        show_actuators = true
    );
}

// Standalone execution preview
cardo_with_universal_slide_bracket_assembly();
