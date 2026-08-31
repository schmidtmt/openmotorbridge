// =============================================================================
// OpenMotorBridge - Satellite Pod: Sena 50S/60S/30K Modular Insert (Deckel / Nest)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/parts/01_insert_sena.scad
// Description: Standalone 3D printable top cradle insert for Sena intercoms.
//              Mounts cleanly on top of cartridge_base_sled via 4x M2 countersunk
//              screws. Allows full access to the underlying Carrier PCB and wiring.
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module cartridge_insert_sena(
    insert_l = 68.0,
    insert_w = 47.0,
    deck_th  = 2.0,
    cradle_h = 8.0
) {
    difference() {
        union() {
            // 1. Intermediate Partition Deck (Grundplatte at z = 0 .. deck_th)
            cube(size=[insert_l, insert_w, deck_th], center=false);

            // 2. Sena 3D Ergonomic Cradle Body (Molded Nest from z = deck_th .. deck_th + cradle_h)
            translate([2.0, 2.0, deck_th]) {
                difference() {
                    cube(size=[insert_l - 4.0, insert_w - 4.0, cradle_h], center=false);

                    // A. Sena Main Body Ergonomic Bed (Recessed 5.0 mm contour)
                    translate([2.0, 2.0, 2.0])
                        cube(size=[insert_l - 8.0, insert_w - 8.0, cradle_h + 0.1], center=false);

                    // B. Sena Jog-Dial Wheel Pocket (Circular cutout at left flank)
                    translate([34.0, 2.0, 1.0])
                        cylinder(r=9.5, h=cradle_h + 1.0, center=false);

                    // C. 7-Pin Pogo Contact Array Pocket (Through-hole to lower PCB chamber)
                    translate([16.0, 15.0, -3.0])
                        cube(size=[24.0, 12.0, cradle_h + 4.0], center=false);

                    // D. Wiring Pass-Through / Routing Channel
                    translate([42.0, (insert_w - 4.0)/2.0 - 4.0, -3.0])
                        cube(size=[12.0, 8.0, cradle_h + 4.0], center=false);
                }
            }

            // 3. Lateral EPDM Rubber Strap Anchor Tabs (Left & Right Flanks)
            translate([insert_l/2.0 - 5.0, -1.2, deck_th + 1.0])
                cube(size=[10.0, 1.2, 4.0], center=false);
            translate([insert_l/2.0 - 5.0, insert_w, deck_th + 1.0])
                cube(size=[10.0, 1.2, 4.0], center=false);
        }

        // 4. 4x M2 Countersunk Mounting Screw Holes (aligned with Base Sled corner posts)
        // Corner screw positions relative to insert origin:
        // Base sled posts at x = 7.0, x = 66.0, y = 6.0, y = 48.0 (offset by 3.5 mm in X and 3.5 mm in Y)
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
cartridge_insert_sena();
