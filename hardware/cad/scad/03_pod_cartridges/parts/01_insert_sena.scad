// =============================================================================
// OpenMotorBridge - Satellite Pod: Sena 50S/60S/30K Modular Insert (Deckel / Nest)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/parts/01_insert_sena.scad
// Description: Standalone 3D printable top cradle insert for Sena intercoms.
//              Features open corner cutouts giving 100% vertical screwdriver access
//              to all 4x M2 countersunk fastening screws from directly above.
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module cartridge_insert_sena(
    insert_l = 70.0,
    insert_w = 49.0,
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
                    translate([35.0, 2.0, 1.0])
                        cylinder(r=9.5, h=cradle_h + 1.0, center=false);

                    // C. 7-Pin Pogo Contact Array Pocket (Through-hole to lower PCB chamber)
                    translate([16.0, 16.0, -3.0])
                        cube(size=[24.0, 12.0, cradle_h + 4.0], center=false);

                    // D. Wiring Pass-Through / Routing Channel
                    translate([44.0, (insert_w - 4.0)/2.0 - 4.0, -3.0])
                        cube(size=[12.0, 8.0, cradle_h + 4.0], center=false);
                }
            }

            // 3. Lateral EPDM Rubber Strap Anchor Tabs (Left & Right Flanks)
            translate([insert_l/2.0 - 5.0, -1.2, deck_th + 1.0])
                cube(size=[10.0, 1.2, 4.0], center=false);
            translate([insert_l/2.0 - 5.0, insert_w, deck_th + 1.0])
                cube(size=[10.0, 1.2, 4.0], center=false);
        }

        // 4. 4x Screwdriver Vertical Access Clearances (Eckfreistellungen)
        // Completely clears the space above each screw head so screwdrivers have vertical line-of-sight
        translate([3.5, 3.5, deck_th - 0.1])
            cylinder(r=3.5, h=cradle_h + 1.0, center=false);
        translate([insert_l - 4.5, 3.5, deck_th - 0.1])
            cylinder(r=3.5, h=cradle_h + 1.0, center=false);
        translate([3.5, insert_w - 3.5, deck_th - 0.1])
            cylinder(r=3.5, h=cradle_h + 1.0, center=false);
        translate([insert_l - 4.5, insert_w - 3.5, deck_th - 0.1])
            cylinder(r=3.5, h=cradle_h + 1.0, center=false);

        // 5. 4x M2 Countersunk Mounting Screw Holes (DIN 7991 M2)
        translate([3.5, 3.5, -0.5])
            cylinder(r=M2_SCREW_HOLE_R, h=deck_th + 1.0, center=false);
        translate([3.5, 3.5, deck_th - 1.0])
            cylinder(r1=M2_SCREW_HOLE_R, r2=2.3, h=1.1, center=false);

        translate([insert_l - 4.5, 3.5, -0.5])
            cylinder(r=M2_SCREW_HOLE_R, h=deck_th + 1.0, center=false);
        translate([insert_l - 4.5, 3.5, deck_th - 1.0])
            cylinder(r1=M2_SCREW_HOLE_R, r2=2.3, h=1.1, center=false);

        translate([3.5, insert_w - 3.5, -0.5])
            cylinder(r=M2_SCREW_HOLE_R, h=deck_th + 1.0, center=false);
        translate([3.5, insert_w - 3.5, deck_th - 1.0])
            cylinder(r1=M2_SCREW_HOLE_R, r2=2.3, h=1.1, center=false);

        translate([insert_l - 4.5, insert_w - 3.5, -0.5])
            cylinder(r=M2_SCREW_HOLE_R, h=deck_th + 1.0, center=false);
        translate([insert_l - 4.5, insert_w - 3.5, deck_th - 1.0])
            cylinder(r1=M2_SCREW_HOLE_R, r2=2.3, h=1.1, center=false);
    }
}

// Standalone printable preview
cartridge_insert_sena();
