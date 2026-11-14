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

module rear_u_yoke_magnetic_lock_detail(unlocked = false, cutaway = true) {
    u_lift = unlocked ? 3.2 : 0.0;

    // 1. Fixed Lower Tub Rear Wall Section (Dark Anthracite PA12, Z = 0..14 mm)
    color([0.28, 0.30, 0.34, 0.92]) {
        difference() {
            union() {
                // Lower fixed rear wall block (Z = 0..14 mm)
                translate([-4.0, -35.0, 0])
                    cube([7.5, 70.0, 14.0], center=false);
                // Short floor stub (X = -24..-4 mm, Z = 0..3.5 mm) to show tub floor context
                translate([-24.0, -35.0, 0])
                    cube([20.0, 70.0, 3.5], center=false);
                // Left side wall stub (Y = -35..-31.5 mm, Z = 0..38 mm) with C-groove
                difference() {
                    translate([-24.0, -35.0, 0])
                        cube([27.5, 3.5, 38.0], center=false);
                    translate([-25.0, -33.5, 32.0])
                        cube([30.0, 2.5, 3.4], center=false);
                }
            }

            // Center SMA Antenna Passthrough (Ø 6.5 mm at Z = 7.5 mm)
            translate([-5.0, 0, 7.5])
                rotate([0, 90, 0])
                    cylinder(r=3.25, h=10.0, center=false, $fn=32);

            // Left Claw Catch Pocket (at Y = -26.0..-20.0 mm, Z = 9.8..14.2 mm)
            translate([-3.4, -26.0, 9.8])
                cube([3.4, 6.0, 4.5], center=false);

            // Right Claw Catch Pocket (at Y = +20.0..+26.0 mm, Z = 9.8..14.2 mm)
            translate([-3.4, 20.0, 9.8])
                cube([3.4, 6.0, 4.5], center=false);

            // Exterior Rebate Step for L-Lid Drip Apron (Tropfnase)
            translate([1.8, -36.0, 10.5])
                cube([3.0, 72.0, 4.0], center=false);

            // Cutaway right half (Y > 4 mm) AND front face of left catch pocket (Y = -26..-22.5 mm)
            // so the downward-gripping Plastikkralle inside the low rear wall is 100% visible!
            if (cutaway) {
                translate([-26.0, 4.0, -2.0])
                    cube([35.0, 40.0, 45.0], center=false);
                translate([-4.5, -26.5, 8.5])
                    cube([3.2, 4.0, 6.5], center=false);
            }
        }
    }

    // 2. Fixed SMA Antenna Bulkhead Connector in Lower Rear Wall (Gold / Brass at Z = 7.5 mm)
    color("gold") {
        translate([-6.0, 0, 7.5])
            rotate([0, 90, 0]) {
                cylinder(r=3.2, h=12.0, center=false, $fn=24);
                // Hex nut & washer on exterior
                translate([0, 0, 9.5])
                    cylinder(r=4.8, h=2.2, center=false, $fn=6);
            }
    }

    // 3. Upper L-Slide Lid & Vertical Heckwand Section (Charcoal PA12, Z = 14..38 mm)
    color([0.20, 0.22, 0.25, 0.88]) {
        difference() {
            union() {
                // Horizontal Top Lid Plate (L-Profile Horizontal Leg, X = -22..0 mm, Z = 32.4..35.6 mm)
                translate([-22.0, -31.9, 32.4])
                    cube([22.0, 63.8, 3.2], center=false);
                // Left Lateral Tongue in C-Groove
                translate([-22.0, -33.5, 32.8])
                    cube([22.0, 1.6, 2.4], center=false);

                // Upper Vertical Heckwand (L-Profile Vertical Leg, X = -3.8..0 mm, Z = 14.0..35.6 mm)
                translate([-3.8, -31.9, 14.0])
                    cube([3.8, 63.8, 21.6], center=false);

                // External Drip Apron (Tropfnase) overlapping lower rear wall down to Z = 10.5 mm
                translate([0.0, -31.9, 10.5])
                    cube([1.5, 63.8, 4.0], center=false);
            }

            // Internal Guide Cavity for U-Yoke Bracket
            translate([-2.6, -28.0, 12.0])
                cube([2.2, 56.0, 23.0], center=false);

            // Central Open Arch (Torbogen) clearing fixed SMA port completely
            translate([-4.5, -18.0, 12.0])
                cube([6.0, 36.0, 13.0], center=false);

            // Cutaway right half (Y > 2 mm) AND inner wall over left U-Yoke arm so the cyan U-Yoke & Plastikkralle are exposed!
            if (cutaway) {
                translate([-25.0, 2.0, 9.0])
                    cube([30.0, 35.0, 32.0], center=false);
                translate([-4.2, -27.5, 10.0])
                    cube([2.4, 29.5, 25.0], center=false);
            }
        }
    }

    // 4. Non-Metallic PA12 U-Yoke Claw Latch ("Plastikkrallen", Bright Cyan — uncut on left & center!)
    translate([0, 0, u_lift]) {
        // PA12 Body
        color([0.15, 0.75, 0.85, 1.0]) {
            difference() {
                union() {
                    // Top Horizontal Cross-Bridge (at Z = 29.0..34.0 mm)
                    translate([-2.0, -25.5, 29.0])
                        cube([1.8, 51.0, 5.0], center=false);

                    // Left Corner Plastic Claw Leg ("Plastikkralle" gripping down into low rear wall)
                    translate([-2.0, -25.5, 10.2]) {
                        cube([1.8, 5.0, 19.0], center=false);
                        // Hooked claw barb ("Kralle") gripping behind the low rear wall catch lip
                        translate([-1.2, 0, 0])
                            cube([3.0, 5.0, 2.2], center=false);
                        // 45° Lead-in ramp on forward (-X) lower tip for horizontal slam-shut
                        translate([-1.2, 0, 0])
                            rotate([0, 45, 0])
                                cube([1.8, 5.0, 1.8], center=false);
                    }

                    // Right Corner Plastic Claw Leg ("Plastikkralle" gripping down into low rear wall)
                    translate([-2.0, 20.5, 10.2]) {
                        cube([1.8, 5.0, 19.0], center=false);
                        translate([-1.2, 0, 0])
                            cube([3.0, 5.0, 2.2], center=false);
                        translate([-1.2, 0, 0])
                            rotate([0, 45, 0])
                                cube([1.8, 5.0, 1.8], center=false);
                    }
                }

                // Magnet Coin Pocket in Bridge Center
                translate([-2.2, 0, 31.5])
                    rotate([0, 90, 0])
                        cylinder(r=3.1, h=2.5, center=false, $fn=24);
            }
        }

        // Central N52 Neodymium Coin Magnet (Silver, Ø 6.0 x 2.0 mm)
        color("silver") {
            translate([-2.1, 0, 31.5])
                rotate([0, 90, 0])
                    cylinder(r=3.0, h=1.9, center=false, $fn=24);
        }

        // Dual Miniature Return Springs (Gold)
        color("gold") {
            translate([-1.1, -23.0, 34.0])
                cylinder(r=1.3, h=2.4 - u_lift * 0.5, center=false, $fn=16);
            translate([-1.1, 23.0, 34.0])
                cylinder(r=1.3, h=2.4 - u_lift * 0.5, center=false, $fn=16);
        }
    }

    // 5. Smart-Keyfob (PCBA 07) Hovering Against Rear Target (Approaching to Unlock)
    translate([7.5, 0, 31.5]) {
        rotate([0, 90, 0]) {
            // Keyfob Housing (cut in half for visibility)
            color([0.14, 0.15, 0.18, 0.92])
                difference() {
                    cylinder(r=10.5, h=4.5, center=false, $fn=32);
                    translate([-12.0, 2.0, -1.0])
                        cube([24.0, 12.0, 7.0], center=false);
                }
            // N52 Magnet Core
            color("silver")
                translate([0, 0, 0.4])
                    cylinder(r=4.2, h=3.6, center=false, $fn=32);
            // Green Proximity Ring
            color([0.2, 0.9, 0.3])
                translate([0, 0, 4.3])
                    difference() {
                        cylinder(r=9.0, h=0.4, center=false, $fn=32);
                        cylinder(r=7.6, h=0.5, center=false, $fn=32);
                    }
        }
    }

    // Magnetic Attraction Flux Lines (Cyan Arrows)
    color([0.0, 0.85, 1.0, 0.9]) {
        for (offset_y = [-2.0, 2.0]) {
            translate([4.2, offset_y, 31.5])
                rotate([0, 90, 0])
                    cylinder(r1=0.8, r2=0.2, h=2.8, center=true, $fn=12);
        }
    }
}

// Standalone execution preview (with cross section preserving all component colors)
rear_u_yoke_magnetic_lock_detail(unlocked = false, cutaway = true);
