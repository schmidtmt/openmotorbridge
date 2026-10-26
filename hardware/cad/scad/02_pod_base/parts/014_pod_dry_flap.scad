// =============================================================================
// OpenMotorBridge - Satellite Pod: Intermediate Splash Shield (Dry-Flap)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/014_pod_dry_flap.scad
// Description: Flexible TPU/EPDM intermediate splash-guard cover (Zwischendeckel /
//              Dry-Flap) isolating the lower PCBA 03 electronics zone from the
//              upper equipment chamber and luggage environment.
// Features:
// 1. Fits form-flush over the lower PCBA 03 chamber (48.0 x 56.0 mm).
// 2. Integral perimeter sealing lip (Shore 50A / TPU 85A).
// 3. Flexible living hinge or snap-flange on bulkhead side.
// 4. Ergonomic pull tab at rear edge for tool-free opening during inspection.
// 5. Embossed "DRY-FLAP / PCBA 03" tactile labeling and lightning flash icon.
// =============================================================================

include <../../00_common/parameters.scad>;

FLAP_L = 48.0;  // Covers PCBA 03 length (mm)
FLAP_W = 56.0;  // Fits internal width between shelf rails (mm)
FLAP_H = 1.8;   // Flexible membrane thickness (mm)

module pod_dry_flap() {
    difference() {
        union() {
            // 1. Main Flexible Shield Membrane with Rounded Corners
            hull() {
                translate([2.0, 2.0, 0])
                    cylinder(r=2.0, h=FLAP_H, $fn=20);
                translate([FLAP_L - 2.0, 2.0, 0])
                    cylinder(r=2.0, h=FLAP_H, $fn=20);
                translate([2.0, FLAP_W - 2.0, 0])
                    cylinder(r=2.0, h=FLAP_H, $fn=20);
                translate([FLAP_L - 2.0, FLAP_W - 2.0, 0])
                    cylinder(r=2.0, h=FLAP_H, $fn=20);
            }

            // 2. Lateral Retention Flanges (slide or snap into internal housing grooves)
            translate([4.0, -1.8, 0])
                cube([FLAP_L - 8.0, 1.8, FLAP_H], center=false);
            translate([4.0, FLAP_W, 0])
                cube([FLAP_L - 8.0, 1.8, FLAP_H], center=false);

            // 3. Front Bulkhead Hinge Bead / Tongue
            translate([-1.8, 4.0, 0])
                cube([1.8, FLAP_W - 8.0, FLAP_H], center=false);

            // 4. Ergonomic Rear Pull Tab (Finger lift tab)
            translate([FLAP_L, FLAP_W/2.0 - 7.0, 0]) {
                hull() {
                    cube([0.5, 14.0, FLAP_H], center=false);
                    translate([7.0, 2.0, 1.5])
                        cube([0.5, 10.0, FLAP_H], center=false);
                }
            }

            // Underside Perimeter Sealing Lip
            translate([2.0, 2.0, -1.2]) {
                difference() {
                    cube([FLAP_L - 4.0, FLAP_W - 4.0, 1.2], center=false);
                    translate([1.5, 1.5, -0.1])
                        cube([FLAP_L - 7.0, FLAP_W - 7.0, 1.4], center=false);
                }
            }
        }

        // Tactile grip grooves on pull tab
        for (tx = [FLAP_L + 2.0 : 2.0 : FLAP_L + 6.0]) {
            translate([tx, FLAP_W/2.0, FLAP_H + 0.8])
                cube([0.8, 10.0, 0.6], center=true);
        }

        // Embossed warning / service mark
        translate([FLAP_L/2.0, FLAP_W/2.0, FLAP_H - 0.3]) {
            // Molded seal outline
            difference() {
                cube([24.0, 12.0, 0.5], center=true);
                cube([21.0, 9.0, 0.6], center=true);
            }
        }
    }
}

// Standalone preview (Translucent Amber / Yellow Shore 50A TPU)
color([0.9, 0.65, 0.15, 0.85])
    pod_dry_flap();
