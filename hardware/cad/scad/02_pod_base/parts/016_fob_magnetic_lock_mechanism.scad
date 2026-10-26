// =============================================================================
// OpenMotorBridge - Satellite Pod: 100% Internal Anti-Theft Magnetic Lock
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/016_fob_magnetic_lock_mechanism.scad
// Description: Detailed cross-section of the 100% INTERNAL magnetic deadbolt.
//
// Key Security Concept:
// - Zero external buttons, sliders, or pry points on the lid exterior!
// - A spring-loaded stainless steel / N52 deadbolt pin (Ø 4.0 x 6.0 mm) sits
//   entirely on the inside, locking the slide-in lid to the monocoque tub.
// - Holding the Smart-Keyfob (PCBA 07) over the exterior RFID target zone
//   magnetically pulls the internal deadbolt upward against the spring,
//   disengaging the socket and allowing the lid to slide open.
// =============================================================================

$fn = 32;

module internal_fob_deadbolt_lock_detail(unlocked = false) {
    pin_lift = unlocked ? 3.5 : 0.0;

    // 1. Cross-Section of Monocoque Tub Front Bulkhead (Dark Anthracite PA12)
    color([0.28, 0.30, 0.34, 0.9]) {
        difference() {
            translate([0, -18.0, 0])
                cube([38.0, 36.0, 24.0], center=false);

            // Front stop collar recess
            translate([6.0, -16.0, 15.0])
                cube([33.0, 32.0, 10.0], center=false);

            // Left & Right U-groove rail cutaways
            translate([6.0, -17.5, 17.5])
                cube([33.0, 2.2, 3.2], center=false);
            translate([6.0, 15.3, 17.5])
                cube([33.0, 2.2, 3.2], center=false);

            // Internal Deadbolt Latch Socket (Blind bore in tub floor, 100% inside!)
            translate([15.0, 0, 10.0])
                cylinder(r=2.5, h=6.0, center=false, $fn=24);
        }
    }

    // 2. Slide-in Lid Front Tongue & Body (Charcoal PA12)
    color([0.20, 0.22, 0.25]) {
        difference() {
            translate([6.0, -15.0, 18.0])
                cube([28.0, 30.0, 4.0], center=false);

            // Lateral tongues engaged in grooves
            // (tongues are part of lid)

            // Blind internal bore for deadbolt pin (drilled from UNDERSIDE only!)
            translate([15.0, 0, 17.0])
                cylinder(r=2.2, h=4.2, center=false, $fn=24);

            // Exterior RFID target marking (0.3 mm recessed badge on top - NO hole!)
            translate([15.0, 0, 21.7])
                cube([14.0, 8.0, 0.4], center=true);
        }
    }

    // Lateral guide tongues sliding in U-grooves
    color([0.18, 0.20, 0.23]) {
        translate([6.0, -17.2, 18.0])
            cube([28.0, 2.2, 2.5], center=false);
        translate([6.0, 15.0, 18.0])
            cube([28.0, 2.2, 2.5], center=false);
    }

    // 3. Internal Stainless Steel / Neodym Deadbolt Pin (Ø 4.0 x 6.0 mm)
    // When locked (pin_lift = 0): Pin extends 3 mm down into tub socket!
    // When unlocked (pin_lift = 3.5): Pin lifts completely into lid bore!
    color("silver") {
        translate([15.0, 0, 12.0 + pin_lift])
            cylinder(r=2.0, h=6.0, center=false, $fn=24);
    }

    // 4. Internal Return Spring (Tensioned when unlocked, pushes down when locked)
    color("gold") {
        translate([15.0, 0, 17.5 + pin_lift * 0.4])
            cylinder(r=1.5, h=2.5 - pin_lift * 0.4, center=false, $fn=16);
    }

    // 5. Smart-Keyfob (PCBA 07) Hovering Above Exterior (Approaching to Unlock)
    translate([15.0, 0, 26.0]) {
        // Keyfob Housing (Rugged Matte Black Puck)
        color([0.12, 0.12, 0.14, 0.9])
            cylinder(r=12.0, h=5.0, center=false, $fn=32);
        // N52 High-Flux Neodymium Magnet Core (Silver)
        color("silver")
            translate([0, 0, 0.5])
                cylinder(r=6.0, h=4.0, center=false, $fn=32);
        // Green Proximity Unlock Indicator Ring
        color([0.2, 0.9, 0.3])
            translate([0, 0, 4.8])
                difference() {
                    cylinder(r=10.0, h=0.4, center=false, $fn=32);
                    cylinder(r=8.5, h=0.5, center=false, $fn=32);
                }
    }

    // Magnetic flux indication arrows (Cyan)
    color([0.0, 0.85, 1.0, 0.7]) {
        for (a = [-3.0, 3.0]) {
            translate([15.0 + a, 0, 22.5])
                cylinder(r1=0.8, r2=0.2, h=3.0, center=false, $fn=12);
        }
    }
}

// Standalone execution preview with clean midplane cross section
difference() {
    internal_fob_deadbolt_lock_detail(unlocked = false);
    // Cut away front half (Y < 0) to reveal internal pin, spring, socket, and tongues
    translate([-10.0, -40.0, -5.0])
        cube([60.0, 40.0, 40.0], center=false);
}
