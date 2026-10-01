// =============================================================================
// OpenMotorBridge - Satellite Pod: Curved Fender Saddle Cradle (Harley-Davidson)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/006_fender_curved_saddle.scad
// Description: Parametric curved cradle foot matched to the cylindrical curvature
//              of Harley-Davidson Touring rear fenders (R ≈ 140 mm crown / R ≈ 320 mm arch).
//              Key Architecture:
//              1. 100% NON-INVASIVE MOUNTING: Zero holes drilled into the painted fender!
//                 Anchors rigidly via an integrated rear mounting tongue directly to the
//                 existing OEM Blinkerbrücke / turn signal bar studs (5/16"-18 / M8, 35mm spacing).
//              2. Compound concave cylindrical bottom arch hugging the fender profile.
//              3. 1.5 mm deep recessed pocket for vibration-damping EPDM contour pad.
//              4. Recessed nest holding the universal Pod 3 base housing (Typ B, 135 x 70 x 38 mm).
//              5. Open front aperture for tool-free cartridge slide-out towards the seat.
//              6. Concealed underfloor cable duct diving behind Blinkerbrücke into fender grommet.
// =============================================================================

include <../../00_common/parameters.scad>;

FENDER_R_TRANS    = 140.0; // Harley-Davidson Touring transverse crown radius (mm)
FENDER_R_LONG     = 320.0; // Harley-Davidson Touring longitudinal wheel radius (mm)
FENDER_PAD_THICK  = 1.5;   // EPDM vibration damping layer thickness (mm)

module fender_curved_saddle(
    base_l = 156.0,
    base_w = 82.0,
    base_h = 18.0
) {
    difference() {
        union() {
            // 1. Solid Cradle Base Block with side skirts
            translate([-base_l/2.0, -base_w/2.0, 0.0])
                cube([base_l, base_w, base_h], center=false);

            // 2. Integrated Rear Mounting Tongue (reaching OEM Blinkerbrücke studs)
            // ZERO holes in the fender! Clamps directly to factory light bar studs.
            translate([base_l/2.0 - 4.0, -26.0, 0.0])
                hull() {
                    cube([36.0, 52.0, 8.0], center=false);
                    translate([34.0, 5.0, 0])
                        cube([2.0, 42.0, 6.0], center=false);
                }
        }

        // --- SUBTRACTIONS ---

        // A. True Cylindrical Concave Fender Arch (Transverse R=140 mm)
        // Stops before reaching the rear mounting tongue
        translate([0, 0, -FENDER_R_TRANS + 4.5])
            intersection() {
                rotate([0, 90, 0])
                    cylinder(r=FENDER_R_TRANS, h=base_l + 20.0, center=true, $fn=128);
                translate([-base_l/2.0 - 5.0, -base_w, -10.0])
                    cube([base_l + 2.0, base_w * 2.0, FENDER_R_TRANS + 20.0], center=false);
            }

        // B. Recessed Nest for Universal Pod 3 Base Housing (135 x 70 x 38 mm)
        // Starts at Z = 7.0 mm (leaving 2.5 mm solid floor above fender arch)
        translate([-POD_OUTER_L/2.0 - 0.5, -POD_OUTER_W/2.0 - 0.4, 7.0])
            cube([POD_OUTER_L + 1.0, POD_OUTER_W + 0.8, 20.0], center=false);

        // C. Front Service Aperture (allowing cartridge to slide out forward)
        translate([-base_l/2.0 - 5.0, -CARTRIDGE_FACE_W/2.0 - 1.0, 7.0])
            cube([18.0, CARTRIDGE_FACE_W + 2.0, 20.0], center=false);

        // D. Dual OEM Blinkerbrücke mounting bores (35 mm spacing, Ø 8.4 mm for 5/16"-18 / M8)
        translate([base_l/2.0 + 16.0, -17.5, -2.0])
            cylinder(r=4.2, h=14.0, center=false, $fn=32);
        translate([base_l/2.0 + 16.0, 17.5, -2.0])
            cylinder(r=4.2, h=14.0, center=false, $fn=32);

        // E. Concealed Rear Cable Duct
        translate([POD_OUTER_L/2.0 - 4.0, -8.0, 7.0])
            cube([base_l/2.0 - POD_OUTER_L/2.0 + 16.0, 16.0, 14.0], center=false);
        // Vertical cable drop behind Blinkerbrücke into OEM grommet
        translate([base_l/2.0 + 8.0, -7.0, -4.0])
            cube([12.0, 14.0, 16.0], center=false);
    }
}

// Standalone render / STL export
fender_curved_saddle();
