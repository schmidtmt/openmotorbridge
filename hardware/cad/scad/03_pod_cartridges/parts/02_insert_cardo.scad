// =============================================================================
// OpenMotorBridge - Satellite Pod: Cardo Packtalk Edge Modular Insert (Deckel / Nest)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/parts/02_insert_cardo.scad
// Description: Standalone 3D printable top cradle insert for Cardo Packtalk Edge.
//              Features AirMount wedge contour, dual N52 magnet pockets, 5-pin
//              pogo contact array pocket, and 4x M2 countersunk mounting holes.
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module cartridge_insert_cardo(
    insert_l = 68.0,
    insert_w = 47.0,
    deck_th  = 2.0,
    cradle_h = 8.0
) {
    difference() {
        union() {
            // 1. Intermediate Partition Deck (Grundplatte at z = 0 .. deck_th)
            cube(size=[insert_l, insert_w, deck_th], center=false);

            // 2. Cardo AirMount 3D Contour Body (z = deck_th .. deck_th + cradle_h)
            translate([2.0, 2.0, deck_th]) {
                difference() {
                    cube(size=[insert_l - 4.0, insert_w - 4.0, cradle_h], center=false);

                    // A. Cardo Packtalk Edge Aerodynamic Wedge Bed (Recessed 5.0 mm contour)
                    translate([2.0, 2.0, 2.0])
                        cube(size=[insert_l - 8.0, insert_w - 8.0, cradle_h + 0.1], center=false);

                    // B. Dual N52 Neodymium Magnet Pockets (Ø 8.2 mm x 2.5 mm depth)
                    translate([16.0, (insert_w - 4.0)/2.0, 0.5])
                        cylinder(r=4.1, h=cradle_h, center=false);
                    translate([48.0, (insert_w - 4.0)/2.0, 0.5])
                        cylinder(r=4.1, h=cradle_h, center=false);

                    // C. 5-Pin Spring Contact Array Pocket (Centered pass-through)
                    translate([28.0, (insert_w - 4.0)/2.0 - 6.0, -3.0])
                        cube(size=[14.0, 12.0, cradle_h + 4.0], center=false);

                    // D. Underfloor Wiring Pass-Through Channel
                    translate([42.0, 4.0, -3.0])
                        cube(size=[10.0, 8.0, cradle_h + 4.0], center=false);
                }
            }

            // 3. Lateral EPDM Rubber Strap Anchor Tabs
            translate([insert_l/2.0 - 5.0, -1.2, deck_th + 1.0])
                cube(size=[10.0, 1.2, 4.0], center=false);
            translate([insert_l/2.0 - 5.0, insert_w, deck_th + 1.0])
                cube(size=[10.0, 1.2, 4.0], center=false);
        }

        // 4. 4x M2 Countersunk Mounting Screw Holes
        translate([3.5, 2.5, -0.5])
            cylinder(r=M2_SCREW_HOLE_R, h=deck_th + 1.0, center=false);
        translate([3.5, 2.5, deck_th - 0.8])
            cylinder(r1=M2_SCREW_HOLE_R, r2=2.2, h=1.0, center=false);

        translate([insert_l - 5.5, 2.5, -0.5])
            cylinder(r=M2_SCREW_HOLE_R, h=deck_th + 1.0, center=false);
        translate([insert_l - 5.5, 2.5, deck_th - 0.8])
            cylinder(r1=M2_SCREW_HOLE_R, r2=2.2, h=1.0, center=false);

        translate([3.5, insert_w - 2.5, -0.5])
            cylinder(r=M2_SCREW_HOLE_R, h=deck_th + 1.0, center=false);
        translate([3.5, insert_w - 2.5, deck_th - 0.8])
            cylinder(r1=M2_SCREW_HOLE_R, r2=2.2, h=1.0, center=false);

        translate([insert_l - 5.5, insert_w - 2.5, -0.5])
            cylinder(r=M2_SCREW_HOLE_R, h=deck_th + 1.0, center=false);
        translate([insert_l - 5.5, insert_w - 2.5, deck_th - 0.8])
            cylinder(r1=M2_SCREW_HOLE_R, r2=2.2, h=1.0, center=false);
    }
}

// Standalone printable preview
cartridge_insert_cardo();
