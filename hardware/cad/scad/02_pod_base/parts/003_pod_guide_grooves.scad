// =============================================================================
// OpenMotorBridge - Satellite Pod: Poka-Yoke Internal Guide Grooves (Nuten)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/003_pod_guide_grooves.scad
// =============================================================================

include <../../00_common/parameters.scad>;

// 1. Internal Guide Ribs (Added along inside tunnel walls to form the 3.0mm guide grooves)
module pod_internal_guide_ribs(start_x=24.0, length=76.0, wall=2.5) {
    // --- Left Side Wall (y = wall = 2.5 mm) ---
    // Lower left rib (z = 4.5 .. 6.7 mm)
    translate([start_x, wall, POD_GROOVE_LEFT_Z - POD_GROOVE_W/2.0 - 2.2])
        cube(size=[length, POD_GROOVE_DEPTH, 2.2], center=false);

    // Upper left rib (z = 9.7 .. 11.9 mm) -> Forms 3.0 mm groove at z = 6.7 .. 9.7 mm (center z = 8.2 mm)
    translate([start_x, wall, POD_GROOVE_LEFT_Z + POD_GROOVE_W/2.0])
        cube(size=[length, POD_GROOVE_DEPTH, 2.2], center=false);

    // --- Right Side Wall (y = POD_OUTER_W - wall - POD_GROOVE_DEPTH = 56.0 mm) ---
    // Lower right rib (z = 10.5 .. 12.7 mm)
    translate([start_x, POD_OUTER_W - wall - POD_GROOVE_DEPTH, POD_GROOVE_RIGHT_Z - POD_GROOVE_W/2.0 - 2.2])
        cube(size=[length, POD_GROOVE_DEPTH, 2.2], center=false);

    // Upper right rib (z = 15.7 .. 17.9 mm) -> Forms 3.0 mm groove at z = 12.7 .. 15.7 mm (center z = 14.2 mm)
    translate([start_x, POD_OUTER_W - wall - POD_GROOVE_DEPTH, POD_GROOVE_RIGHT_Z + POD_GROOVE_W/2.0])
        cube(size=[length, POD_GROOVE_DEPTH, 2.2], center=false);
}

// 2. Guide Groove Cutout Tool (Alternative subtractive approach for Tinkercad/CSG boolean)
module pod_internal_guide_grooves_tool(start_x=22.0, length=78.0) {
    // Left Groove Tool (3.0 mm width at z = 6.7 .. 9.7 mm)
    translate([start_x, 1.0, POD_GROOVE_LEFT_Z - POD_GROOVE_W/2.0])
        cube(size=[length, 3.0, POD_GROOVE_W], center=false);

    // Right Groove Tool (3.0 mm width at z = 12.7 .. 15.7 mm)
    translate([start_x, POD_OUTER_W - 4.0, POD_GROOVE_RIGHT_Z - POD_GROOVE_W/2.0])
        cube(size=[length, 3.0, POD_GROOVE_W], center=false);
}

// Standalone preview
pod_internal_guide_ribs();
