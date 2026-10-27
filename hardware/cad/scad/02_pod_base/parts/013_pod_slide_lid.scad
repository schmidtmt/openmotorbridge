// =============================================================================
// OpenMotorBridge - Satellite Pod: L-Slide Lid with U-Yoke Magnetic Lock
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/013_pod_slide_lid.scad
// Description: L-shaped Monocoque Satellite Pod Lid (horizontal slide lid +
//              upper rear wall) with 100% NON-METALLIC PA12 U-Yoke Deadbolt Latch.
//
// Key Architectural Features:
// 1. True L-Profile Monolithic Construction:
//    - Horizontal slide plate with smooth underside (ZERO downward bosses!).
//    - Integrated upper rear wall (Heckwand) with external drip apron (Tropfnase)
//      overlapping the lower sill for IP67 seal.
// 2. 100% RF-Transparent PA12 U-Yoke Deadbolt (No Metal Shielding!):
//    - Inverted wide U-bracket (portal shape) made from PA12-MJF.
//    - Avoids all metal shielding for 868 MHz LoRa / 2.4 GHz Bluetooth / Mesh.
//    - Central N52 Neodymium coin magnet (Ø 6.0 x 2.0 mm) in the arch bridge.
//    - Two lateral corner deadbolt legs (Y = 8.5 mm & Y = 55.5 mm) with 45°
//      lead-in chamfers for automatic "Slam-Shut" latching.
//    - Central open arch provides wide clearance around the fixed SMA port!
// 3. Dual Mini-Nippel End-Stops:
//    - Lateral studs engaging the C-grooves at full insertion to lock in X/Y/Z
//      and prevent sidewall splay under vibration.
// 4. Proximity Keyfob (PCBA 07) Release:
//    - Holding the Smart-Keyfob over the rear center RFID target lifts the
//      central magnet and retracts both corner deadbolts simultaneously.
// =============================================================================

include <../../00_common/parameters.scad>;

$fn = 32;

// Lid Mechanical Dimensions
LID_L       = 143.0; // Fits inside tub along X (mm)
LID_W       = 63.8;  // Fits into side grooves along Y (mm)
LID_PLATE_H = 3.2;   // Main rigid top plate thickness (mm)
TONGUE_W    = 1.6;   // Lateral guide tongue protrusion on each flank (mm)
TONGUE_H    = 2.4;   // Tongue thickness sliding in groove (mm)

// Upper Heckwand (Vertical Leg of L) Dimensions
HECK_WALL_TH = 3.8;  // Ultra-slim rear wall thickness (mm, leaves >10mm to OEM adapter)
HECK_DROP_H  = 18.4; // Distance from lid underside down to tub sill (Z = 14.0 mm)
DRIP_APRON_H = 3.5;  // Overlapping drip skirt extending over lower sill (mm)
TOTAL_HECK_H = HECK_DROP_H + LID_PLATE_H; // 21.6 mm total rear wall height

// U-Yoke Deadbolt Dimensions
U_SPAN_W     = 55.0; // Total width of U-bracket (mm)
U_LEG_W      = 5.0;  // Width of each corner locking leg (mm)
U_BRIDGE_H   = 5.0;  // Height of horizontal cross-bridge (mm)
U_THICK      = 1.8;  // Thickness of PA12 bracket (mm)
U_LIFT_STROKE= 3.0;  // Vertical retraction stroke (mm)

// -----------------------------------------------------------------------------
// MODULE: Non-Metallic PA12 U-Lock Bracket
// -----------------------------------------------------------------------------
module pod_u_lock_bracket(unlocked = false) {
    z_lift = unlocked ? U_LIFT_STROKE : 0.0;

    translate([0, 0, z_lift]) {
        // 1. RF-Transparent PA12 Portal Frame (High-contrast signal cyan/orange)
        color([0.15, 0.75, 0.85]) {
            difference() {
                union() {
                    // Top Cross-Bridge spanning between both corner legs
                    translate([0, (LID_W - U_SPAN_W)/2.0, -U_BRIDGE_H])
                        cube([U_THICK, U_SPAN_W, U_BRIDGE_H], center=false);

                    // Left Corner Locking Leg
                    translate([0, (LID_W - U_SPAN_W)/2.0, -HECK_DROP_H - 3.2]) {
                        // Main vertical strut
                        cube([U_THICK, U_LEG_W, HECK_DROP_H + 3.2], center=false);
                        // 45° Lead-in chamfer on forward lower edge for slam-shut
                        translate([U_THICK, 0, 0])
                            rotate([0, -45, 0])
                                cube([2.5, U_LEG_W, 2.5], center=false);
                    }

                    // Right Corner Locking Leg
                    translate([0, (LID_W + U_SPAN_W)/2.0 - U_LEG_W, -HECK_DROP_H - 3.2]) {
                        cube([U_THICK, U_LEG_W, HECK_DROP_H + 3.2], center=false);
                        translate([U_THICK, 0, 0])
                            rotate([0, -45, 0])
                                cube([2.5, U_LEG_W, 2.5], center=false);
                    }
                }

                // Central Magnet Press-Fit Cavity (Ø 6.2 mm x 2.0 mm deep)
                translate([-0.1, LID_W/2.0, -U_BRIDGE_H/2.0])
                    rotate([0, 90, 0])
                        cylinder(r=3.1, h=U_THICK + 0.2, center=false, $fn=24);
            }
        }

        // 2. Central Rare-Earth N52 Neodymium Coin Magnet (Silver)
        color("silver") {
            translate([0.1, LID_W/2.0, -U_BRIDGE_H/2.0])
                rotate([0, 90, 0])
                    cylinder(r=3.0, h=1.6, center=false, $fn=24);
        }

        // 3. Dual Miniature Helical Return Springs (Gold)
        color("gold") {
            // Left Spring above leg
            translate([U_THICK/2.0, (LID_W - U_SPAN_W)/2.0 + U_LEG_W/2.0, 0.2])
                cylinder(r=1.4, h=2.8 - z_lift * 0.5, center=false, $fn=16);
            // Right Spring above leg
            translate([U_THICK/2.0, (LID_W + U_SPAN_W)/2.0 - U_LEG_W/2.0, 0.2])
                cylinder(r=1.4, h=2.8 - z_lift * 0.5, center=false, $fn=16);
        }
    }
}

// -----------------------------------------------------------------------------
// MODULE: Main L-Slide Lid with Upper Heckwand & Integrated U-Lock
// -----------------------------------------------------------------------------
module pod_slide_lid(show_internal_lock = true, unlocked = false) {
    difference() {
        union() {
            // 1. Horizontal Slide-in Lid Plate (100% SMOOTH UNDERSIDE - ZERO BOSSES!)
            cube([LID_L, LID_W, LID_PLATE_H], center=false);

            // 2. Continuous Lateral Guide Tongues (Left & Right Flanks)
            translate([0, -TONGUE_W, 0.4])
                cube([LID_L, TONGUE_W, TONGUE_H], center=false);
            translate([0, LID_W, 0.4])
                cube([LID_L, TONGUE_W, TONGUE_H], center=false);

            // 3. Front Nose Lead-in Chamfer (for smooth insertion into rails)
            translate([0, -TONGUE_W, 0])
                rotate([0, -25, 0])
                    cube([2.0, LID_W + 2*TONGUE_W, LID_PLATE_H], center=false);

            // 4. Underside Perimeter Sealing Tongue (IP67 EPDM groove compression)
            translate([4.0, 3.0, -1.5]) {
                difference() {
                    cube([LID_L - 8.0, LID_W - 6.0, 1.5], center=false);
                    translate([2.0, 2.0, -0.2])
                        cube([LID_L - 12.0, LID_W - 10.0, 1.9], center=false);
                }
            }

            // 5. Integrated Upper Heckwand (Vertical Leg of L at rear X = LID_L - HECK_WALL_TH)
            translate([LID_L - HECK_WALL_TH, 0, -HECK_DROP_H]) {
                cube([HECK_WALL_TH, LID_W, TOTAL_HECK_H], center=false);
            }

            // 6. External Drip Apron (Tropfnase) overlapping lower tub sill by 3.5 mm
            translate([LID_L - 1.5, 0, -HECK_DROP_H - DRIP_APRON_H]) {
                cube([1.5, LID_W, DRIP_APRON_H + 0.1], center=false);
            }

            // 7. Dual Mini-Nippel End-Stops at Upper Rear Flanks (engage C-grooves)
            translate([LID_L - HECK_WALL_TH, -TONGUE_W - 0.2, 0.4])
                cube([HECK_WALL_TH, TONGUE_W + 0.2, TONGUE_H], center=false);
            translate([LID_L - HECK_WALL_TH, LID_W, 0.4])
                cube([HECK_WALL_TH, TONGUE_W + 0.2, TONGUE_H], center=false);
        }

        // --- SUBTRACTIONS ---

        // 8. Internal Guide Pocket for U-Yoke Bracket (inside Upper Heckwand)
        translate([LID_L - HECK_WALL_TH + 0.8, (LID_W - U_SPAN_W - 1.0)/2.0, -HECK_DROP_H - 4.0]) {
            cube([U_THICK + 0.4, U_SPAN_W + 1.0, TOTAL_HECK_H + 2.0], center=false);
        }

        // 9. Central Open Arch (Torbogen) through lower part of Heckwand
        // Fully clears the lower tub SMA connector (width 36 mm, height up to Z = -6.0 mm)
        translate([LID_L - HECK_WALL_TH - 0.5, (LID_W - 36.0)/2.0, -HECK_DROP_H - 1.0]) {
            cube([HECK_WALL_TH + 1.0, 36.0, 12.0], center=false);
        }

        // 10. Rear Glove-Grip Push Flutes (Tactile thumb grips for motorcycle gloves)
        for (gx = [LID_L - 32.0 : 4.5 : LID_L - 12.0]) {
            translate([gx, LID_W/2.0, LID_PLATE_H - 0.2])
                cube([2.2, 28.0, 0.8], center=true);
        }

        // 11. Rear Exterior RFID / Keyfob Proximity Target Badge on Heckwand
        // Subtle 0.3 mm recessed badge indicating where the keyfob is placed to unlock
        translate([LID_L - 0.2, LID_W/2.0, -U_BRIDGE_H/2.0]) {
            rotate([0, 90, 0]) {
                cube([10.0, 16.0, 0.4], center=true);
                // Key icon slot
                cube([1.2, 8.0, 0.6], center=true);
            }
        }
    }

    // 12. Visual Display of the Internal RF-Transparent U-Lock Bracket
    if (show_internal_lock) {
        translate([LID_L - HECK_WALL_TH + 1.0, 0, 0])
            pod_u_lock_bracket(unlocked = unlocked);
    }
}

// Standalone execution preview
color([0.22, 0.23, 0.25])
    pod_slide_lid(show_internal_lock = true, unlocked = false);
