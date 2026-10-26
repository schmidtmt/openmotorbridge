// =============================================================================
// OpenMotorBridge - Satellite Pod: Slide-in Lid (Schiebedeckel)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/013_pod_slide_lid.scad
// Description: Monocoque Satellite Pod Slide-in Lid with continuous lateral
//              guide tongues and 100% INTERNAL tamper-proof magnetic FOB lock.
//
// Mechanical Features:
// 1. True Slide-in design: Slides in horizontally from the rear along the X-axis
//    within precision U-profile guide grooves in the housing sidewalls.
// 2. 100% Internal Anti-Theft Latch (Zero external sliders / tamper-proof):
//    An internal spring-loaded magnetic deadbolt clicks down into a blind
//    socket in the tub floor when fully inserted.
// 3. Proximity Keyfob (PCBA 07) Release:
//    Holding the smart keyfob over the marked RFID target zone magnetically
//    lifts the internal deadbolt against its spring, releasing the lid.
// 4. Smooth exterior with ergonomic rear push-grip flutes for motorcycle gloves.
// =============================================================================

include <../../00_common/parameters.scad>;

$fn = 32;

// Lid Mechanical Dimensions
LID_L       = 143.0; // Fits inside tub with front stop collar (mm)
LID_W       = 63.8;  // Fits into side grooves (mm)
LID_PLATE_H = 3.2;   // Main rigid top plate thickness (mm)
TONGUE_W    = 1.6;   // Lateral guide tongue protrusion on each flank (mm)
TONGUE_H    = 2.4;   // Tongue thickness sliding in groove (mm)

module pod_slide_lid(show_internal_lock = true) {
    difference() {
        union() {
            // 1. Main Slide-in Lid Plate (Smooth, flush automotive surface)
            cube([LID_L, LID_W, LID_PLATE_H], center=false);

            // 2. Continuous Lateral Guide Tongues (Left & Right Flanks)
            // Left flank tongue (slides in Y = POD_WALL groove)
            translate([0, -TONGUE_W, 0.4])
                cube([LID_L, TONGUE_W, TONGUE_H], center=false);
            // Right flank tongue (slides in Y = POD_OUTER_W - POD_WALL groove)
            translate([0, LID_W, 0.4])
                cube([LID_L, TONGUE_W, TONGUE_H], center=false);

            // 3. Front Nose Lead-in Chamfer (for smooth insertion into rear slot)
            translate([0, -TONGUE_W, 0])
                rotate([0, -25, 0])
                    cube([2.0, LID_W + 2*TONGUE_W, LID_PLATE_H], center=false);

            // 4. Underside Perimeter Sealing Tongue (IP67 compressible EPDM seal)
            translate([4.0, 3.0, -1.8]) {
                difference() {
                    cube([LID_L - 8.0, LID_W - 6.0, 1.8], center=false);
                    translate([2.0, 2.0, -0.2])
                        cube([LID_L - 12.0, LID_W - 10.0, 2.2], center=false);
                }
            }

            // 5. Internal Deadbolt Housing Boss (on underside, 100% INTERNAL)
            translate([8.0, LID_W/2.0 - 5.0, -5.5]) {
                cube([14.0, 10.0, 5.5], center=false);
            }
        }

        // --- SUBTRACTIONS (100% Smooth Exterior - Zero External Sliders!) ---

        // 6. Rear Glove-Grip Push Flutes (Tactile thumb grip for sliding)
        for (gx = [LID_L - 25.0 : 4.5 : LID_L - 8.0]) {
            translate([gx, LID_W/2.0, LID_PLATE_H - 0.2])
                cube([2.2, 28.0, 0.8], center=true);
        }

        // 7. Flush RFID / Keyfob Proximity Target Badge (at X = 15.0 mm)
        // Subtle 0.3 mm recessed marking on top indicating keyfob placement
        translate([15.0, LID_W/2.0, LID_PLATE_H - 0.15]) {
            cube([16.0, 10.0, 0.4], center=true);
            // Subtle embossed key icon groove
            cube([8.0, 1.2, 0.6], center=true);
        }

        // 8. Internal Deadbolt Guide Bore (Ø 4.2 mm x 5.0 mm deep on underside)
        // Spring and magnetic steel pin reside entirely within this cavity
        translate([15.0, LID_W/2.0, -6.0])
            cylinder(r=2.1, h=6.5, center=false, $fn=24);
    }

    // Visual demonstration of internal magnetic latch mechanism (if enabled)
    if (show_internal_lock) {
        // Internal Stainless Steel Magnetic Deadbolt Pin (Ø 4.0 x 5.0 mm)
        color("silver")
            translate([15.0, LID_W/2.0, -5.0])
                cylinder(r=2.0, h=5.0, center=false, $fn=24);

        // Internal Helical Return Spring (Gold)
        color("gold")
            translate([15.0, LID_W/2.0, -1.0])
                cylinder(r=1.5, h=2.0, center=false, $fn=16);
    }
}

// Standalone execution preview
color([0.22, 0.23, 0.25])
    pod_slide_lid(show_internal_lock = true);
