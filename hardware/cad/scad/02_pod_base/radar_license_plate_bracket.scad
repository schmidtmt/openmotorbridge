// =============================================================================
// OpenMotorBridge - Radar License Plate Bracket (Decoupled Symmetrical Mount)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/radar_license_plate_bracket.scad
// Description: Symmetrical mounting bracket attaching the Garmin Varia mmWave
//              blind-spot radar centered below the motorcycle license plate.
//              Features:
//              1. Clamps to lower M6 license plate mounting bolts.
//              2. Suspends radar below the plate with zero upward visual occlusion.
//              3. M5 GoPro-style swivel hinge for precision horizontal beam leveling.
//              4. Concealed rear cable channel for the M8 4-pin PUR radar harness.
//              5. High-rigidity truss ribbing resisting 117 cui road vibration.
// =============================================================================

include <../00_common/parameters.scad>;

PLATE_BOLT_SPACING = 120.0; // Distance between lower license plate screws (mm)
RADAR_BRACKET_W    = 136.0; // Total bracket width in Y (mm)
RADAR_DROP_Z       = 48.0;  // Drop below license plate lower edge in Z (mm)

module radar_license_plate_bracket() {
    difference() {
        union() {
            // 1. Upper Crossbar Mounting Flange (sandwiched behind license plate)
            translate([-RADAR_BRACKET_W/2.0, 0, 0])
                cube([RADAR_BRACKET_W, 26.0, 4.0], center=false);

            // 2. Monolithic Central Spine Neck (Solid continuous column from top to bottom)
            hull() {
                translate([-18.0, 2.0, 0])
                    cube([36.0, 16.0, 4.0], center=false);
                translate([-12.0, 2.0, -RADAR_DROP_Z])
                    cube([24.0, 14.0, 16.0], center=false);
            }

            // 3. Dual Swivel Hinge Lugs (Protruding forward at bottom, monolithic with spine)
            // Left lug
            translate([-7.5, 12.0, -RADAR_DROP_Z])
                rotate([0, 90, 0])
                    cylinder(r=9.0, h=4.0, center=false, $fn=32);
            translate([-7.5, 4.0, -RADAR_DROP_Z - 5.0])
                cube([4.0, 8.0, 14.0], center=false);

            // Right lug
            translate([3.5, 12.0, -RADAR_DROP_Z])
                rotate([0, 90, 0])
                    cylinder(r=9.0, h=4.0, center=false, $fn=32);
            translate([3.5, 4.0, -RADAR_DROP_Z - 5.0])
                cube([4.0, 8.0, 14.0], center=false);

            // 4. Stiffening Gussets (Diagonal structural ribs)
            hull() {
                translate([-RADAR_BRACKET_W/2.0 + 12.0, 12.0, 0])
                    cube([8.0, 4.0, 3.5], center=false);
                translate([-10.0, 4.0, -RADAR_DROP_Z * 0.5])
                    cube([6.0, 4.0, 4.0], center=false);
            }
            hull() {
                translate([RADAR_BRACKET_W/2.0 - 20.0, 12.0, 0])
                    cube([8.0, 4.0, 3.5], center=false);
                translate([4.0, 4.0, -RADAR_DROP_Z * 0.5])
                    cube([6.0, 4.0, 4.0], center=false);
            }
        }

        // --- SUBTRACTIONS ---

        // A. Dual M6 License Plate Clamping Holes
        for (sx = [-PLATE_BOLT_SPACING/2.0, PLATE_BOLT_SPACING/2.0]) {
            translate([sx, 13.0, -1.0]) {
                cylinder(r=3.3, h=8.0, center=false, $fn=32);
                translate([0, 0, 2.5])
                    cylinder(r=5.5, h=4.0, center=false, $fn=32);
            }
        }

        // B. Clevis Tab Clearance Slot (between prongs, forward of the solid spine)
        translate([-3.5, 8.0, -RADAR_DROP_Z - 12.0])
            cube([7.0, 16.0, 24.0], center=false);

        // C. M5 Swivel Hinge Pin Bore (Horizontal through both prongs)
        translate([0, 12.0, -RADAR_DROP_Z])
            rotate([0, 90, 0])
                cylinder(r=2.6, h=25.0, center=true, $fn=32);

        // D. M5 Hex Nut Pocket on Right Lug
        translate([5.5, 12.0, -RADAR_DROP_Z])
            rotate([0, 90, 0])
                cylinder(r=4.6, h=5.0, center=false, $fn=6);

        // E. Rear M8 Cable Channel on Spine Backside (Y=0, Z down to -RADAR_DROP_Z + 10)
        translate([-3.0, -0.5, -RADAR_DROP_Z + 10.0])
            cube([6.0, 3.5, RADAR_DROP_Z], center=false);
    }
}

// Standalone preview / STL export
radar_license_plate_bracket();
