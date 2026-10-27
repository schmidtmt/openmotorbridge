// =============================================================================
// OpenMotorBridge - Satellite Pod: 100% Non-Metallic U-Yoke Magnetic Lock
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/016_fob_magnetic_lock_mechanism.scad
// Description: High-precision cross-section of the 100% RF-TRANSPARENT PA12
//              U-Yoke magnetic lock at the rear Heckwand.
//
// Key Security & RF Concept:
// - Non-metallic PA12 portal bracket prevents RF shielding / attenuation
//   for 868 MHz LoRa, 2.4 GHz BLE, and 5.8 GHz Mesh radios.
// - An embedded N52 coin magnet (Ø 6 x 2 mm) at the center of the arch
//   lifts both corner deadbolt legs simultaneously against return springs.
// - Open central arch leaves 100% free clearance for the fixed SMA antenna port.
// - Slam-shut: 45° lead-in chamfers on legs snap automatically into the
//   lower sill sockets when sliding shut.
// =============================================================================

$fn = 32;

module rear_u_yoke_magnetic_lock_detail(unlocked = false) {
    u_lift = unlocked ? 3.2 : 0.0;

    // 1. Lower Tub Sill Section (Dark Anthracite PA12, Z = 0..14 mm)
    color([0.28, 0.30, 0.34, 0.9]) {
        difference() {
            // Lower sill wall block
            translate([-4.0, -35.0, 0])
                cube([7.5, 70.0, 14.0], center=false);

            // Center SMA Antenna Passthrough (Ø 6.5 mm at Z = 7.5 mm)
            translate([-5.0, 0, 7.5])
                rotate([0, 90, 0])
                    cylinder(r=3.25, h=10.0, center=false, $fn=32);

            // Left Corner Latch Socket (at Y = -23.5 mm)
            translate([-1.8, -26.0, 10.0])
                cube([3.0, 6.0, 4.5], center=false);

            // Right Corner Latch Socket (at Y = +23.5 mm)
            translate([-1.8, 20.0, 10.0])
                cube([3.0, 6.0, 4.5], center=false);

            // Exterior Rebate Step for L-Lid Drip Apron (Tropfnase)
            translate([1.5, -36.0, 10.5])
                cube([3.0, 72.0, 4.0], center=false);
        }
    }

    // 2. Fixed SMA Antenna Bulkhead Connector (Gold / Brass in Center)
    color("gold") {
        translate([-6.0, 0, 7.5])
            rotate([0, 90, 0]) {
                cylinder(r=3.2, h=12.0, center=false, $fn=24);
                // Hex nut
                translate([0, 0, 8.0])
                    cylinder(r=4.5, h=2.5, center=false, $fn=6);
            }
    }

    // 3. Upper L-Lid Heckwand Section (Charcoal PA12, Z = 14..38 mm)
    color([0.20, 0.22, 0.25]) {
        difference() {
            union() {
                // Upper vertical Heckwand
                translate([-3.8, -32.0, 14.0])
                    cube([3.8, 64.0, 24.0], center=false);

                // External Drip Apron (Tropfnase) overlapping sill by 3.5 mm
                translate([0.0, -32.0, 10.5])
                    cube([1.5, 64.0, 3.6], center=false);
            }

            // Internal Guide Cavity for U-Yoke Bracket
            translate([-2.4, -28.0, 12.0])
                cube([2.2, 56.0, 25.0], center=false);

            // Central Open Arch (Torbogen) clearing SMA port completely
            translate([-4.5, -18.0, 12.0])
                cube([6.0, 36.0, 13.0], center=false);

            // Exterior RFID / Keyfob Proximity Target Badge
            translate([1.3, 0, 32.0]) {
                rotate([0, 90, 0]) {
                    cube([8.0, 14.0, 0.4], center=true);
                    cube([1.2, 6.0, 0.6], center=true);
                }
            }
        }
    }

    // 4. Non-Metallic PA12 U-Yoke Deadbolt Bracket (Cyan / RF-Transparent)
    translate([0, 0, u_lift]) {
        // PA12 Body
        color([0.15, 0.75, 0.85, 0.95]) {
            difference() {
                union() {
                    // Top Horizontal Cross-Bridge (at Z = 32 mm)
                    translate([-2.0, -26.0, 29.5])
                        cube([1.8, 52.0, 5.0], center=false);

                    // Left Corner Locking Leg
                    translate([-2.0, -25.5, 10.5]) {
                        cube([1.8, 5.0, 19.5], center=false);
                        // 45° Lead-in chamfer
                        translate([1.8, 0, 0])
                            rotate([0, -45, 0])
                                cube([2.0, 5.0, 2.0], center=false);
                    }

                    // Right Corner Locking Leg
                    translate([-2.0, 20.5, 10.5]) {
                        cube([1.8, 5.0, 19.5], center=false);
                        translate([1.8, 0, 0])
                            rotate([0, -45, 0])
                                cube([2.0, 5.0, 2.0], center=false);
                    }
                }

                // Magnet Coin Pocket in Bridge Center
                translate([-2.2, 0, 32.0])
                    rotate([0, 90, 0])
                        cylinder(r=3.1, h=2.5, center=false, $fn=24);
            }
        }

        // Central N52 Neodymium Coin Magnet (Silver, Ø 6.0 x 2.0 mm)
        color("silver") {
            translate([-1.9, 0, 32.0])
                rotate([0, 90, 0])
                    cylinder(r=3.0, h=1.8, center=false, $fn=24);
        }

        // Dual Miniature Return Springs (Gold)
        color("gold") {
            translate([-1.1, -23.0, 34.5])
                cylinder(r=1.3, h=3.0 - u_lift * 0.6, center=false, $fn=16);
            translate([-1.1, 23.0, 34.5])
                cylinder(r=1.3, h=3.0 - u_lift * 0.6, center=false, $fn=16);
        }
    }

    // 5. Smart-Keyfob (PCBA 07) Hovering Against Rear Target (Approaching to Unlock)
    translate([8.0, 0, 32.0]) {
        rotate([0, 90, 0]) {
            // Keyfob Housing
            color([0.12, 0.12, 0.14, 0.9])
                cylinder(r=12.0, h=5.0, center=false, $fn=32);
            // N52 Magnet Core
            color("silver")
                translate([0, 0, 0.5])
                    cylinder(r=5.0, h=4.0, center=false, $fn=32);
            // Green Proximity Ring
            color([0.2, 0.9, 0.3])
                translate([0, 0, 4.8])
                    difference() {
                        cylinder(r=10.0, h=0.4, center=false, $fn=32);
                        cylinder(r=8.5, h=0.5, center=false, $fn=32);
                    }
        }
    }

    // Magnetic Attraction Flux Lines (Cyan Arrows)
    color([0.0, 0.85, 1.0, 0.8]) {
        for (offset_y = [-2.0, 2.0]) {
            translate([4.5, offset_y, 32.0])
                rotate([0, 90, 0])
                    cylinder(r1=0.8, r2=0.2, h=3.0, center=true, $fn=12);
        }
    }
}

// Standalone execution preview (with cross section)
difference() {
    rear_u_yoke_magnetic_lock_detail(unlocked = false);
    // Cut away front-right half (Y > 0) to clearly expose internals
    translate([-10.0, 0.0, -5.0])
        cube([30.0, 45.0, 50.0], center=false);
}
