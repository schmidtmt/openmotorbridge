// =============================================================================
// OpenMotorBridge - Satellite Pod: Cardo Packtalk Edge Modular Insert (Deckel / Nest)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/parts/02_insert_cardo.scad
// Description: Standalone 3D printable top cradle insert for Cardo Packtalk Edge.
//              Features:
//              - True through-deck wiring pass-through & pogo contact pockets
//              - Convective airflow / breathing slots for optimal thermal dissipation
//              - Open corner cutouts giving 100% vertical screwdriver access
//              - Integrated outward-facing EPDM rubber strap retention hooks
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module cartridge_insert_cardo(
    insert_l = 70.0,
    insert_w = 49.0,
    deck_th  = 2.0,
    cradle_h = 8.0
) {
    difference() {
        union() {
            // 1. Intermediate Partition Deck (Grundplatte at z = 0 .. deck_th)
            cube(size=[insert_l, insert_w, deck_th], center=false);

            // 2. Cardo AirMount 3D Contour Body (z = deck_th .. deck_th + cradle_h)
            translate([2.0, 1.5, deck_th]) {
                difference() {
                    cube(size=[insert_l - 4.0, insert_w - 3.0, cradle_h], center=false);

                    // A. Cardo Packtalk Edge Aerodynamic Wedge Bed (Recessed 5.0 mm contour)
                    translate([2.0, 2.0, 2.0])
                        cube(size=[insert_l - 8.0, insert_w - 7.0, cradle_h + 0.1], center=false);

                    // B. Dual N52 Neodymium Magnet Pockets (Ø 8.2 mm x 2.5 mm depth)
                    translate([16.0, (insert_w - 4.0)/2.0, 0.5])
                        cylinder(r=4.1, h=cradle_h, center=false);
                    translate([48.0, (insert_w - 4.0)/2.0, 0.5])
                        cylinder(r=4.1, h=cradle_h, center=false);
                }
            }

            // 3. Outward-Facing Rubber Strap Overhang Ledges (Top Lip at z = deck_th + 5.0 .. deck_th + cradle_h)
            // Left Flank Top Lip
            translate([insert_l/2.0 - 5.0, 0.5, deck_th + 5.0])
                cube(size=[10.0, 2.5, cradle_h - 5.0], center=false);
            // Right Flank Top Lip
            translate([insert_l/2.0 - 5.0, insert_w - 3.0, deck_th + 5.0])
                cube(size=[10.0, 2.5, cradle_h - 5.0], center=false);
        }

        // 4. True Through-Deck Contact & Wiring Pass-Throughs (Cuts all the way through Grundplatte z = -1 .. 12 mm)
        // A. 5-Pin Spring Contact Array Pocket (Centered pass-through)
        translate([28.0, (insert_w - 4.0)/2.0 - 6.0, -1.0])
            cube(size=[14.0, 12.0, deck_th + cradle_h + 2.0], center=false);

        // B. Underfloor Wiring Pass-Through Channel
        translate([42.0, 6.0, -1.0])
            cube(size=[12.0, 10.0, deck_th + cradle_h + 2.0], center=false);

        // 5. 4x Convective Airflow & Breathing Slots (Lüftungsschlitze z = -1 .. deck_th + 1 mm)
        translate([12.0, 8.0, -1.0])
            cube(size=[12.0, 2.5, deck_th + 2.0], center=false);
        translate([12.0, insert_w - 10.5, -1.0])
            cube(size=[12.0, 2.5, deck_th + 2.0], center=false);
        translate([54.0, 8.0, -1.0])
            cube(size=[10.0, 2.5, deck_th + 2.0], center=false);
        translate([54.0, insert_w - 10.5, -1.0])
            cube(size=[10.0, 2.5, deck_th + 2.0], center=false);

        // 6. 2x Outward-Facing EPDM Rubber Strap Undercut Hook Slots (at x = 30 .. 40 mm)
        // Left Hook Undercut Slot (Band hooks under top lip from outside)
        translate([insert_l/2.0 - 5.1, -0.5, deck_th + 1.0])
            cube(size=[10.2, 3.5, 4.2], center=false);
        // Right Hook Undercut Slot
        translate([insert_l/2.0 - 5.1, insert_w - 3.0, deck_th + 1.0])
            cube(size=[10.2, 3.5, 4.2], center=false);

        // 7. 4x Screwdriver Vertical Access Clearances (Eckfreistellungen)
        translate([3.5, 3.5, deck_th - 0.1])
            cylinder(r=3.5, h=cradle_h + 1.0, center=false);
        translate([insert_l - 4.5, 3.5, deck_th - 0.1])
            cylinder(r=3.5, h=cradle_h + 1.0, center=false);
        translate([3.5, insert_w - 3.5, deck_th - 0.1])
            cylinder(r=3.5, h=cradle_h + 1.0, center=false);
        translate([insert_l - 4.5, insert_w - 3.5, deck_th - 0.1])
            cylinder(r=3.5, h=cradle_h + 1.0, center=false);

        // 8. 4x M2 Countersunk Mounting Screw Holes (DIN 7991 M2)
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
cartridge_insert_cardo();
