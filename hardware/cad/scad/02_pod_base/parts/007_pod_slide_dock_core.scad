// =============================================================================
// OpenMotorBridge - Satellite Pod: Open-Top Slide-In Dock Core (Aufnahmedock)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/007_pod_slide_dock_core.scad
// Description: Parametric core module defining the open-top cradle cavity for the
//              standard, 100% unchanged universal Pod base housing (135 x 70 x 38 mm).
//              Features:
//              1. 0.5 mm sliding clearance (135.5 x 70.5 x 38.0 mm)
//              2. Open top: Pod roof with Gore-Vent & GNSS patch antenna is exposed
//              3. Front M8 gland neck pocket (facing forward towards seat, -X)
//              4. Rear cartridge entrance mouth (facing rearward towards tail, +X)
//              5. Flank pockets for 4x EPDM strap hook lugs (X = 25 & 110 mm)
//              6. Transverse fender crown cradle at bottom
// =============================================================================

include <../../00_common/parameters.scad>;

// Standard Pod External Dimensions with clearance
DOCK_POD_L = POD_OUTER_L + 0.6; // 135.6 mm
DOCK_POD_W = POD_OUTER_W + 0.6; // 70.6 mm
DOCK_POD_H = POD_OUTER_H + 0.2; // 38.2 mm

// Subtraction tool to hollow out the open-top dock cradle
// Origin centered at (X = 0, Y = 0, Z = floor of dock)
module pod_slide_dock_subtraction(
    dock_l = DOCK_POD_L,
    dock_w = DOCK_POD_W,
    dock_h = DOCK_POD_H,
    open_sky_h = 50.0 // Cut through all material above pod roof
) {
    // 1. Main Pod Cavity (centered in X and Y, sitting at Z = 0 .. dock_h)
    translate([-dock_l/2.0, -dock_w/2.0, 0.0]) {
        // Main pod block plus infinite top clearance so pod roof is 100% exposed
        cube([dock_l, dock_w, dock_h + open_sky_h], center=false);
    }

    // 2. 4x Flank Pockets for Pod EPDM Strap Hooks
    // Hooks are located at X = 25.0 and X = 110.0 from pod front (-dock_l/2.0)
    // Hook width 8 mm, protrusion 3.0 mm, height 5 mm
    hook_x_offsets = [-dock_l/2.0 + 25.0, -dock_l/2.0 + (POD_OUTER_L - 25.0)];
    for (hx = hook_x_offsets) {
        // Left flank pocket (Y = +dock_w/2.0)
        translate([hx - 7.0, dock_w/2.0 - 0.5, 0.0])
            cube([14.0, 5.0, 10.0], center=false);

        // Right flank pocket (Y = -dock_w/2.0 - 4.5)
        translate([hx - 7.0, -dock_w/2.0 - 4.5, 0.0])
            cube([14.0, 5.0, 10.0], center=false);
    }

    // 3. Front M8 Cable Gland Neck Pocket (facing -X towards seat)
    // Neck is centered at Y = 0, Z = 19.0 mm, outer radius 6.0 mm
    translate([-dock_l/2.0 - 15.0, -8.0, 19.0 - 8.0])
        cube([16.0, 16.0, 20.0], center=false);

    // 4. Rear Mouth Clearance (facing +X towards tail)
    // Allows the cartridge faceplate (width 74 mm, height 34 mm) to slide through cleanly
    translate([dock_l/2.0 - 2.0, -dock_w/2.0 - 2.5, 0.0])
        cube([30.0, dock_w + 5.0, dock_h + open_sky_h], center=false);
}

// Standalone preview module
module pod_slide_dock_preview() {
    difference() {
        // Outer demonstration block
        translate([-(DOCK_POD_L + 16.0)/2.0, -(DOCK_POD_W + 16.0)/2.0, -4.0])
            cube([DOCK_POD_L + 16.0, DOCK_POD_W + 16.0, DOCK_POD_H + 4.0], center=false);

        // Subtract the open dock cavity
        pod_slide_dock_subtraction();
    }
}

// Standalone execution preview
pod_slide_dock_preview();
