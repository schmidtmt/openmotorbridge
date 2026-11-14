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
LID_L       = 146.5; // Fits from front groove (X = 3.5 mm) flush to rear wall (X = 150.0 mm)
LID_W       = 60.5;  // Main plate width (mm), clears 61.0 mm tub chamber opening (Y = 4.5..65.5 mm) with 0.25 mm play
LID_PLATE_H = 2.8;   // Main rigid top plate thickness (mm), leaves 0.5 mm vertical clearance to 35.6 mm groove roof
TONGUE_W    = 2.2;   // Lateral guide tongue protrusion on each flank (mm, engages Y = 2.55 and 67.45 mm into C-grooves)
TONGUE_H    = 2.4;   // Tongue thickness sliding in 3.6 mm groove (mm, 0.6 mm total vertical clearance)

// Upper Heckwand (Vertical Leg of L) Dimensions
HECK_WALL_TH = 3.8;  // Rear wall thickness closing upper portal (X = 146.2..150.0 mm)
HECK_DROP_H  = 18.3; // Distance from lid underside (Z = 32.3) down to fixed rear wall sill (Z = 14.0 mm)
DRIP_APRON_H = 3.5;  // Overlapping drip skirt extending over lower sill down to Z = 10.5 mm
TOTAL_HECK_H = HECK_DROP_H + LID_PLATE_H + 2.0; // 23.1 mm total rear wall height (Z = 14.0..37.1 mm)

// Non-Metallic PA12 U-Yoke Claw Latch ("Plastikkrallen") Dimensions
U_SPAN_W     = 50.0; // Total width of U-bracket (claws at Y_tub = 10.0..15.0 & 55.0..60.0 mm)
U_LEG_W      = 5.0;  // Width of each downward-gripping plastic claw (mm)
U_BRIDGE_H   = 5.0;  // Height of horizontal cross-bridge (mm)
U_THICK      = 1.8;  // Thickness of PA12 bracket (mm)
U_LIFT_STROKE= 3.2;  // Vertical retraction stroke when Keyfob magnet approaches (mm)

// -----------------------------------------------------------------------------
// MODULE: Non-Metallic PA12 U-Lock Bracket with Downward-Gripping Claws ("Plastikkrallen")
// -----------------------------------------------------------------------------
module pod_u_lock_bracket(unlocked = false) {
    z_lift = unlocked ? U_LIFT_STROKE : 0.0;

    translate([0, 0, z_lift]) {
        // 1. RF-Transparent PA12 Portal Frame with Downward Claws (Signal Cyan)
        color([0.15, 0.75, 0.85]) {
            difference() {
                union() {
                    // Top Cross-Bridge spanning between both corner claw legs
                    translate([0, (LID_W - U_SPAN_W)/2.0, -U_BRIDGE_H])
                        cube([U_THICK, U_SPAN_W, U_BRIDGE_H], center=false);

                    // Left Plastic Claw Leg ("Plastikkralle" gripping down into low rear wall)
                    translate([0, (LID_W - U_SPAN_W)/2.0, -HECK_DROP_H - 3.6]) {
                        // Main vertical leg inside lid rear wall
                        cube([U_THICK, U_LEG_W, HECK_DROP_H + 3.6], center=false);
                        // Hooked claw barb ("Kralle") gripping behind the low rear wall catch lip
                        translate([-1.2, 0, 0])
                            cube([U_THICK + 1.2, U_LEG_W, 2.2], center=false);
                        // 45° Lead-in ramp on forward (-X) lower tip for horizontal slam-shut
                        translate([-1.2, 0, 0])
                            rotate([0, 45, 0])
                                cube([1.8, U_LEG_W, 1.8], center=false);
                    }

                    // Right Plastic Claw Leg ("Plastikkralle" gripping down into low rear wall)
                    translate([0, (LID_W + U_SPAN_W)/2.0 - U_LEG_W, -HECK_DROP_H - 3.6]) {
                        cube([U_THICK, U_LEG_W, HECK_DROP_H + 3.6], center=false);
                        translate([-1.2, 0, 0])
                            cube([U_THICK + 1.2, U_LEG_W, 2.2], center=false);
                        translate([-1.2, 0, 0])
                            rotate([0, 45, 0])
                                cube([1.8, U_LEG_W, 1.8], center=false);
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
module pod_slide_lid_body() {
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
}

module pod_slide_lid(show_internal_lock = true, unlocked = false, alpha = 0.95) {
    color([0.22, 0.23, 0.25, alpha])
        pod_slide_lid_body();

    // 12. Visual Display of the Internal RF-Transparent U-Lock Bracket ("Plastikkrallen")
    if (show_internal_lock) {
        translate([LID_L - HECK_WALL_TH + 1.0, 0, 0])
            pod_u_lock_bracket(unlocked = unlocked);
    }
}

// Standalone execution preview
pod_slide_lid(show_internal_lock = true, unlocked = false);
