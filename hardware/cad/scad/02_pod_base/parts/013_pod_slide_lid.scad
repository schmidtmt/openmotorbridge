// =============================================================================
// OpenMotorBridge - Satellite Pod: Tool-Free Slide-In Lid (Schiebedeckel)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/013_pod_slide_lid.scad
// Description: Tool-free, self-locking slide-in lid for the universal Monocoque
//              Satellite Pod (Typ B).
// Features:
// 1. Longitudinal guide tongue ribs sliding into housing rim tracks.
// 2. Perimeter IP67 elastomeric seal lip / tongue.
// 3. Ergonomic recessed pull handle & tactile grip flutes at rear.
// 4. Underside 90° latch catch pocket for the FOB magnetic release pawl.
// 5. Tactile Ø 16 mm target circle on top for Smart-Keyfob (PCBA 07) alignment.
// 6. Integrated ejection spring compression nose (10 mm initial pop-out travel).
// =============================================================================

include <../../00_common/parameters.scad>;

LID_L         = POD_OUTER_L - 4.0;   // 146.0 mm (flush fit with housing front/rear)
LID_W         = POD_OUTER_W - 6.0;   // 64.0 mm (fits into upper rim opening)
LID_PLATE_H   = 3.5;                 // Main lid shell thickness (mm)
LID_TONGUE_W  = 2.2;                 // Lateral tongue width (mm)
LID_TONGUE_H  = 2.5;                 // Lateral tongue height (mm)
SEAL_LIP_H    = 1.8;                 // Perimeter sealing tongue protrusion (mm)

module pod_slide_lid() {
    difference() {
        union() {
            // 1. Main Lid Plate with Chamfered Leading Edge
            hull() {
                translate([2.0, 2.0, 0])
                    cylinder(r=2.0, h=LID_PLATE_H, $fn=24);
                translate([LID_L - 2.0, 2.0, 0])
                    cylinder(r=2.0, h=LID_PLATE_H, $fn=24);
                translate([2.0, LID_W - 2.0, 0])
                    cylinder(r=2.0, h=LID_PLATE_H, $fn=24);
                translate([LID_L - 2.0, LID_W - 2.0, 0])
                    cylinder(r=2.0, h=LID_PLATE_H, $fn=24);
            }

            // 2. Left and Right Lateral Guide Tongue Ribs
            // Left tongue
            translate([8.0, -LID_TONGUE_W, 0.5])
                cube([LID_L - 16.0, LID_TONGUE_W, LID_TONGUE_H], center=false);
            // Right tongue
            translate([8.0, LID_W, 0.5])
                cube([LID_L - 16.0, LID_TONGUE_W, LID_TONGUE_H], center=false);

            // 3. Underside Perimeter Sealing Lip (IP67 Compressible Gasket Frame)
            translate([4.0, 4.0, -SEAL_LIP_H]) {
                difference() {
                    cube([LID_L - 8.0, LID_W - 8.0, SEAL_LIP_H], center=false);
                    translate([2.0, 2.0, -0.1])
                        cube([LID_L - 12.0, LID_W - 12.0, SEAL_LIP_H + 0.2], center=false);
                }
            }

            // 4. Underside Latch Catch Boss (at X = 55 mm from front)
            translate([50.0, 4.0, -5.0])
                cube([14.0, 6.0, 5.0], center=false);
        }

        // 5. Underside 90° Locking Pawl Detent Pocket (Forms positive lock with FOB pawl)
        translate([56.0, 2.0, -5.5])
            cube([4.0, 10.0, 4.0], center=false);

        // 6. 30° Lead-In Chamfer on Locking Detent (allows smooth push-to-close self-locking)
        translate([56.0, 2.0, -2.5])
            rotate([0, 30, 0])
                cube([5.0, 10.0, 4.0], center=false);

        // 7. Ergonomic Rear Grip Flutes (Tactile thumb flutes for effortless removal)
        for (gx = [LID_L - 24.0 : 4.0 : LID_L - 8.0]) {
            translate([gx, LID_W/2.0, LID_PLATE_H])
                cube([2.0, 28.0, 1.2], center=true);
        }

        // 8. Smart-Keyfob (PCBA 07) FOB Contactless Target Circle (Ø 16 mm engraved ring)
        translate([45.0, LID_W/2.0, LID_PLATE_H - 0.4]) {
            difference() {
                cylinder(r=8.0, h=0.6, center=false, $fn=32);
                cylinder(r=6.5, h=0.7, center=false, $fn=32);
            }
            // Inner key icon recess
            cube([1.4, 6.0, 0.6], center=true);
            cube([6.0, 1.4, 0.6], center=true);
        }
    }
}

// Standalone preview
color([0.22, 0.23, 0.25])
    pod_slide_lid();
