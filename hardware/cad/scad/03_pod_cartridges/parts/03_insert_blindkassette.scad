// =============================================================================
// OpenMotorBridge - Satellite Pod: Waterproof Dummy Plug Insert (Deckel)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/parts/03_insert_blindkassette.scad
// Description: Standalone 3D printable solid top cover for waterproof dummy pod.
//              Seals the top opening with internal stiffening ribs and 4x M2
//              countersunk screws.
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module cartridge_insert_blindkassette(
    insert_l = 110.0,
    insert_w = 53.0,
    deck_th  = 3.0
) {
    difference() {
        union() {
            // 1. Solid Top Lid (3.0 mm thick)
            cube(size=[insert_l, insert_w, deck_th], center=false);

            // 2. Internal Stiffening Ribs (Kreuzverrippung)
            translate([insert_l/2.0 - 1.0, 4.0, -2.5])
                cube(size=[2.0, insert_w - 8.0, 2.5], center=false);
            translate([4.0, insert_w/2.0 - 1.0, -2.5])
                cube(size=[insert_l - 8.0, 2.0, 2.5], center=false);
            translate([insert_l/4.0 - 1.0, 4.0, -2.5])
                cube(size=[2.0, insert_w - 8.0, 2.5], center=false);
            translate([3*insert_l/4.0 - 1.0, 4.0, -2.5])
                cube(size=[2.0, insert_w - 8.0, 2.5], center=false);
        }

        // 3. 4x M2 Countersunk Mounting Screw Holes
        translate([3.5, 3.5, -3.0])
            cylinder(r=M2_SCREW_HOLE_R, h=deck_th + 4.0, center=false);
        translate([3.5, 3.5, deck_th - 1.2])
            cylinder(r1=M2_SCREW_HOLE_R, r2=2.3, h=1.3, center=false);

        translate([insert_l - 4.5, 3.5, -3.0])
            cylinder(r=M2_SCREW_HOLE_R, h=deck_th + 4.0, center=false);
        translate([insert_l - 4.5, 3.5, deck_th - 1.2])
            cylinder(r1=M2_SCREW_HOLE_R, r2=2.3, h=1.3, center=false);

        translate([3.5, insert_w - 3.5, -3.0])
            cylinder(r=M2_SCREW_HOLE_R, h=deck_th + 4.0, center=false);
        translate([3.5, insert_w - 3.5, deck_th - 1.2])
            cylinder(r1=M2_SCREW_HOLE_R, r2=2.3, h=1.3, center=false);

        translate([insert_l - 4.5, insert_w - 3.5, -3.0])
            cylinder(r=M2_SCREW_HOLE_R, h=deck_th + 4.0, center=false);
        translate([insert_l - 4.5, insert_w - 3.5, deck_th - 1.2])
            cylinder(r1=M2_SCREW_HOLE_R, r2=2.3, h=1.3, center=false);
    }
}

// Standalone printable preview
cartridge_insert_blindkassette();
