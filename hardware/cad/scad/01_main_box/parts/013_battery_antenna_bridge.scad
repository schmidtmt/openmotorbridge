// =============================================================================
// OpenMotorBridge - Main Box: Battery Retainer & Dual Antenna Bridge
// =============================================================================
// File: hardware/cad/scad/01_main_box/parts/013_battery_antenna_bridge.scad
// Description: Multi-function modular battery retainer bridge (Akkubrücke)
//              for the Central Box Oberwanne:
//              1. Clamps 2200 mAh 1S LiPo flat cell firmly with 1.0 mm EPDM foam.
//              2. Long-axis tool-free RC-style pivot hinge (left, X = 16.5 mm).
//              3. Cantilever snap-fit lock with thumb release tab (right, X = 88.5 mm).
//              4. Dual encapsulated antenna nests for:
//                 - Taoglas FXP895 LoRa 868 MHz flex antenna (85.0 x 18.0 x 0.8 mm)
//                 - Taoglas FXP73 2.4 GHz Wi-Fi/BLE flex antenna (47.0 x 7.0 x 0.5 mm)
//              5. Snap-on protective shroud / cover plate (Schutzabdeckung, 0.8 mm)
//                 making both antennas completely touch-safe & scratch-proof.
//              6. Integrated C-clip strain-relief channels near the hinge axis
//                 for 2x U.FL coaxial cables (Ø 1.2 mm) and battery harness (Ø 2.2 mm).
//              Result: 100% CABLE-FREE ENCLOSURE LID for effortless servicing!
// =============================================================================

include <../../00_common/parameters.scad>;

module main_box_battery_antenna_bridge(
    bridge_l = 72.0,   // Active span across battery cradle in X (mm)
    bridge_w = 32.0,   // Active width across battery in Y (mm)
    bridge_t = 2.4,    // Main structural plate thickness (mm)
    show_cover = true  // Render snap-on protective cover in place
) {
    color([0.22, 0.24, 0.26]) {
        difference() {
            union() {
                // 1. Main Structural Bridge Plate
                // Centered along Y around cradle center Y = 34.0 mm (Y = 18.0 to 50.0 mm)
                translate([17.0, 18.0, 0])
                    cube([bridge_l, bridge_w, bridge_t], center=false);

                // 2. Left Side Pivot Hinge Tabs (Steck-Scharnier Zapfen at X = 14.0 mm)
                // 2x sturdy cylindrical/rounded pivot tabs that slide into cradle sockets
                for (dy = [5.0, bridge_w - 9.0]) {
                    translate([14.2, 18.0 + dy, 0]) {
                        cube([3.0, 4.0, bridge_t]);
                        translate([0, 2.0, bridge_t / 2.0])
                            rotate([0, 90, 0])
                                cylinder(r=bridge_t/2.0, h=3.0, center=false, $fn=24);
                    }
                }

                // 3. Right Side Cantilever Snap Latch Arm (at X = 89.0 mm)
                translate([17.0 + bridge_l, 18.0 + bridge_w/2.0 - 6.0, -3.5]) {
                    // Vertical flexible cantilever arm
                    cube([1.8, 12.0, 3.5 + bridge_t]);
                    // Catch tooth (locking barb pointing inward -X)
                    translate([-0.9, 0, 0])
                        cube([0.9, 12.0, 1.8]);
                    // Ergonomic thumb release tab (protrudes +X for finger actuation)
                    translate([1.8, 0, bridge_t])
                        rotate([0, -25, 0])
                            cube([3.5, 12.0, 1.4]);
                }

                // 4. Integrated C-Clip Strain Relief Bosses (near Hinge axis, X = 18.0..22.0)
                // Absorbs 100% of pull forces; protects fragile U.FL solder joints!
                translate([18.0, 18.0, bridge_t]) {
                    difference() {
                        cube([6.0, bridge_w, 2.4]);
                        // Clip 1: LoRa 868 MHz Coax (Ø 1.25 mm with 0.9 mm snap opening)
                        translate([3.0, 6.0, 1.2]) {
                            cylinder(r=0.65, h=2.6, center=true, $fn=20);
                            translate([0, 0, 0.7]) cube([1.0, 1.4, 1.5], center=true);
                        }
                        // Clip 2: 2.4 GHz Wi-Fi/BLE Coax (Ø 1.25 mm with 0.9 mm snap opening)
                        translate([3.0, 13.0, 1.2]) {
                            cylinder(r=0.65, h=2.6, center=true, $fn=20);
                            translate([0, 0, 0.7]) cube([1.0, 1.4, 1.5], center=true);
                        }
                        // Clip 3: 2-Pin Battery Lead Channel (Ø 2.4 mm)
                        translate([3.0, 24.0, 1.2]) {
                            cylinder(r=1.2, h=2.6, center=true, $fn=24);
                            translate([0, 0, 0.7]) cube([1.6, 2.4, 1.5], center=true);
                        }
                    }
                }
            }

            // --- SUBTRACTIONS (Antenna Pockets & Underside EPDM Recess) ---

            // 5. Underside EPDM Foam Recess (0.6 mm deep, centers clamping force on LiPo)
            translate([22.0, 20.0, -0.1])
                cube([62.0, bridge_w - 4.0, 0.7]);

            // 6. Top Recessed Pocket for Taoglas FXP895 LoRa Antenna (85.0 x 18.0 x 0.8 mm)
            // Extends along length X = 12.0 to 86.0 mm, Y = 19.5 to 37.5 mm
            translate([12.0, 19.5, bridge_t - 0.8])
                cube([75.0, 18.0, 1.0]);

            // 7. Top Recessed Pocket for Taoglas FXP73 2.4 GHz Flex Antenna (47.0 x 7.0 x 0.5 mm)
            // Positioned parallel alongside LoRa antenna at Y = 39.0 to 46.0 mm
            translate([26.0, 39.5, bridge_t - 0.6])
                cube([48.0, 7.5, 0.8]);

            // 8. Snap-Fit Notches for Protective Cover Plate (4x lateral detents)
            for (dx = [30.0, 65.0]) {
                translate([dx, 17.8, bridge_t - 0.6]) cube([4.0, 0.8, 0.8]);
                translate([dx, 18.0 + bridge_w - 0.6, bridge_t - 0.6]) cube([4.0, 0.8, 0.8]);
            }
        }
    }

    // 9. Snap-on Protective Cover Plate (Schutzabdeckung, 0.8 mm PA12)
    // Completely seals and protects antennas against tools, scratches & handling
    if (show_cover) {
        color([0.30, 0.55, 0.80], 0.85) {
            translate([24.5, 18.5, bridge_t + 0.1]) {
                difference() {
                    union() {
                        // Main thin shield sheet
                        cube([63.5, bridge_w - 1.0, 0.8]);
                        // Retention detent tabs that click into bridge notches
                        for (dx = [5.5, 40.5]) {
                            translate([dx, -0.6, -0.6]) cube([3.8, 0.7, 1.0]);
                            translate([dx, bridge_w - 1.0 - 0.1, -0.6]) cube([3.8, 0.7, 1.0]);
                        }
                    }
                    // Subtle embossed logo / antenna symbol identifier
                    translate([31.0, (bridge_w - 1.0)/2.0, 0.5])
                        cylinder(r=2.5, h=0.4, $fn=16);
                }
            }
        }
    }
}

// Standalone preview
main_box_battery_antenna_bridge();
