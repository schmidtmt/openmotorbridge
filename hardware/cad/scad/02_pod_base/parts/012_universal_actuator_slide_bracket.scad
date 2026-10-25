// =============================================================================
// OpenMotorBridge - Satellite Pod: Universal Dual-Actuator Slide Bracket
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/012_universal_actuator_slide_bracket.scad
// Description: "One Size Fits All" mechatronic cold-boot actuation system.
//              Mounts inside the Pod base without requiring individual form-fit
//              cartridges for each OEM intercom model (Cardo Packtalk Edge,
//              Sena 50S, Sena Spider, Midland Rush, etc.):
//              1. Dual independent longitudinal sliding carriages on slotted rails.
//              2. Accommodates two 5V linear micro-solenoids (Ø 6.2 mm bore) with
//                 silicone pusher tips (Shore A50).
//              3. Continuous X-axis adjustment (15 mm to 85 mm span, covering both
//                 adjacent keys and widely spaced keys like Cardo's 50 mm gap).
//              4. M3 locking set-screw / thumb-screw clamp for vibration-proof hold.
//              5. Universal bottom retention base with soft silicone/foam bed pads.
// =============================================================================

$fn = 32;

// --- Mechanical Dimensions ---
BRACKET_BASE_L      = 105.0;  // Longitudinal frame length (mm)
BRACKET_BASE_W      = 54.0;   // Transverse width matching pod cavity (mm)
BRACKET_BASE_H      = 4.0;    // Rigid base bridge thickness (mm)
RAIL_SLOT_W         = 4.2;    // Longitudinal adjustment slot width for M3/M4 screws (mm)
RAIL_SLOT_L         = 70.0;   // Usable sliding range along X (mm)
SOLENOID_BORE       = 6.2;    // Standard Ø for 5V miniature push-pull solenoids (mm)
CARRIAGE_L          = 18.0;   // Length of each sliding actuator shoe (mm)
CARRIAGE_W          = 22.0;   // Width of each sliding actuator shoe (mm)
CARRIAGE_H          = 14.0;   // Height of solenoid clamp tower (mm)

// 1. Universal Base Rail Deck
module universal_actuator_base_deck() {
    difference() {
        union() {
            // Main rigid perimeter frame
            cube([BRACKET_BASE_L, BRACKET_BASE_W, BRACKET_BASE_H], center=false);

            // Perimeter stiffening and alignment ribs
            translate([0, 0, BRACKET_BASE_H]) {
                cube([BRACKET_BASE_L, 3.0, 3.5], center=false);
                translate([0, BRACKET_BASE_W - 3.0, 0])
                    cube([BRACKET_BASE_L, 3.0, 3.5], center=false);
            }

            // Lateral mounting lugs (M2.5 screw bosses to pod base floor)
            for (lx = [10.0, BRACKET_BASE_L - 10.0]) {
                translate([lx, -3.5, 0])
                    cube([12.0, 4.0, BRACKET_BASE_H], center=false);
                translate([lx, BRACKET_BASE_W - 0.5, 0])
                    cube([12.0, 4.0, BRACKET_BASE_H], center=false);
            }
        }

        // 4x Pod mounting screw holes (Ø 2.8 mm for M2.5 threaded inserts)
        for (lx = [16.0, BRACKET_BASE_L - 4.0]) {
            translate([lx, -1.5, -1.0])
                cylinder(r=1.4, h=BRACKET_BASE_H + 2.0, center=false);
            translate([lx, BRACKET_BASE_W + 1.5, -1.0])
                cylinder(r=1.4, h=BRACKET_BASE_H + 2.0, center=false);
        }

        // Dual longitudinal adjustment slots (Left slot at Y = 16 mm, Right slot at Y = 38 mm)
        translate([18.0, 16.0 - RAIL_SLOT_W/2.0, -1.0])
            hull() {
                cylinder(r=RAIL_SLOT_W/2.0, h=BRACKET_BASE_H + 2.0, center=false);
                translate([RAIL_SLOT_L, 0, 0])
                    cylinder(r=RAIL_SLOT_W/2.0, h=BRACKET_BASE_H + 2.0, center=false);
            }

        translate([18.0, 38.0 - RAIL_SLOT_W/2.0, -1.0])
            hull() {
                cylinder(r=RAIL_SLOT_W/2.0, h=BRACKET_BASE_H + 2.0, center=false);
                translate([RAIL_SLOT_L, 0, 0])
                    cylinder(r=RAIL_SLOT_W/2.0, h=BRACKET_BASE_H + 2.0, center=false);
            }

        // Central cutout for headset body clearance & wiring
        translate([20.0, 22.0, -1.0])
            cube([BRACKET_BASE_L - 40.0, 10.0, BRACKET_BASE_H + 2.0], center=false);
    }
}

// 2. Sliding Actuator Carriage (Independent adjustable clamp shoe)
module sliding_actuator_carriage() {
    difference() {
        union() {
            // Slider base plate with guide tongues
            translate([-CARRIAGE_L/2.0, -CARRIAGE_W/2.0, 0])
                cube([CARRIAGE_L, CARRIAGE_W, 4.0], center=false);

            // Vertical solenoid clamping head
            translate([0, 0, 4.0]) {
                cylinder(r=CARRIAGE_W/2.0 - 2.0, h=CARRIAGE_H - 4.0, center=false);
            }

            // Downward T-guide rib for zero play in rail slot
            translate([-CARRIAGE_L/2.0 + 2.0, -RAIL_SLOT_W/2.0 + 0.15, -2.0])
                cube([CARRIAGE_L - 4.0, RAIL_SLOT_W - 0.3, 2.0], center=false);
        }

        // Vertical Solenoid Bore (Ø 6.2 mm) for push-pull linear micro-solenoid
        translate([0, 0, -3.0])
            cylinder(r=SOLENOID_BORE/2.0, h=CARRIAGE_H + 6.0, center=false);

        // Clamping pinch split (1.2 mm gap)
        translate([-0.6, 0, 2.0])
            cube([1.2, CARRIAGE_W/2.0 + 1.0, CARRIAGE_H + 2.0], center=false);

        // Horizontal M3 transverse pinch clamp screw bore
        translate([-CARRIAGE_L/2.0 - 1.0, 5.5, CARRIAGE_H - 4.0])
            rotate([0, 90, 0])
                cylinder(r=1.6, h=CARRIAGE_L + 2.0, center=false);

        // Vertical M3 locking set-screw hole to secure carriage onto rail deck
        translate([-CARRIAGE_L/2.0 + 3.5, 0, -3.0])
            cylinder(r=1.6, h=10.0, center=false);
    }
}

// 3. Silicone Pusher Tip (Soft Shore A50 plunger buffer)
module silicone_pusher_tip() {
    color([0.85, 0.2, 0.2, 0.9]) {
        difference() {
            union() {
                // Cylindrical stem (plugs onto solenoid rod Ø 2.0 mm)
                cylinder(r=2.5, h=5.0, center=false);
                // Hemisphere button contact pad (gentle on OEM rubber keys)
                translate([0, 0, 5.0])
                    sphere(r=3.2);
            }
            // Inner bore for solenoid metal pin
            translate([0, 0, -0.5])
                cylinder(r=1.05, h=4.0, center=false);
        }
    }
}

// 4. Complete Universal System Assembly Preview
module universal_actuator_slide_bracket_assembly() {
    // Rigid Base Rail Frame
    color([0.25, 0.25, 0.28])
        universal_actuator_base_deck();

    // Actuator Carriage 1 (e.g. Cardo Intercom key at X = 32 mm, Y = 16 mm)
    color([0.8, 0.5, 0.1])
        translate([32.0, 16.0, BRACKET_BASE_H])
            sliding_actuator_carriage();

    // Actuator Carriage 2 (e.g. Cardo Media key at X = 82 mm, Y = 38 mm -> 50 mm distance!)
    color([0.1, 0.6, 0.8])
        translate([82.0, 38.0, BRACKET_BASE_H])
            sliding_actuator_carriage();

    // Demonstration Silicone Pusher Tips under Solenoids
    translate([32.0, 16.0, -4.0])
        silicone_pusher_tip();
    translate([82.0, 38.0, -4.0])
        silicone_pusher_tip();
}

// Standalone execution preview
universal_actuator_slide_bracket_assembly();
