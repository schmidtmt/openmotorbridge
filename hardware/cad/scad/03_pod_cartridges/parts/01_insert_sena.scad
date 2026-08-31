// =============================================================================
// OpenMotorBridge - Satellite Pod: Sena 50S/60S/30K Modular Insert (Deckel / Nest)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/parts/01_insert_sena.scad
// Description: Standalone 3D printable top cradle insert for Sena intercoms.
//              Features:
//              - True through-deck wiring pass-through & pogo-pin contact pockets
//              - Convective airflow / breathing slots for optimal thermal dissipation
//              - Open corner cutouts giving 100% vertical screwdriver access
//              - Integrated outward-facing EPDM rubber strap retention hooks
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
            translate([2.0, 1.5, deck_th]) {
                difference() {
                    cube(size=[insert_l - 4.0, insert_w - 3.0, cradle_h], center=false);

                    // A. Sena Main Body Ergonomic Bed (Recessed 5.0 mm contour)
                    translate([2.0, 2.0, 2.0])
                        cube(size=[insert_l - 8.0, insert_w - 7.0, cradle_h + 0.1], center=false);

                    // B. Sena Jog-Dial Wheel Pocket (Circular cutout at left flank)
                    translate([35.0, 2.0, 1.0])
                        cylinder(r=9.5, h=cradle_h + 1.0, center=false);
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
        // A. 7-Pin Pogo Contact Array Pocket (Through-hole to lower Carrier PCB chamber)
        translate([18.0, 17.5, -1.0])
            cube(size=[24.0, 12.0, deck_th + cradle_h + 2.0], center=false);

        // B. Flexible Wiring Pass-Through / Routing Channel
        translate([46.0, (insert_w - 4.0)/2.0 - 4.0, -1.0])
            cube(size=[14.0, 10.0, deck_th + cradle_h + 2.0], center=false);

        // 5. 4x Convective Airflow & Breathing Slots (Lüftungsschlitze z = -1 .. deck_th + 1 mm)
        // Allows warm air from lower charging circuit to circulate upwards to ePTFE breather
        translate([12.0, 8.0, -1.0])
            cube(size=[12.0, 2.5, deck_th + 2.0], center=false);
        translate([12.0, insert_w - 10.5, -1.0])
            cube(size=[12.0, 2.5, deck_th + 2.0], center=false);
        translate([52.0, 8.0, -1.0])
            cube(size=[10.0, 2.5, deck_th + 2.0], center=false);
        translate([52.0, insert_w - 10.5, -1.0])
            cube(size=[10.0, 2.5, deck_th + 2.0], center=false);

        // 6. 2x Outward-Facing EPDM Rubber Strap Undercut Hook Slots (at x = 30 .. 40 mm)
        // Left Hook Undercut Slot (Band hooks under top lip from outside)
        translate([insert_l/2.0 - 5.1, -0.5, deck_th + 1.0])
            cube(size=[10.2, 3.5, 4.2], center=false);
        // Right Hook Undercut Slot
        translate([insert_l/2.0 - 5.1, insert_w - 3.0, deck_th + 1.0])
            cube(size=[10.2, 3.5, 4.2], center=false);

        // 7. 4x Screwdriver Vertical Access Clearances (Eckfreistellungen)
        // Completely clears the space above each screw head so screwdrivers have vertical line-of-sight
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
cartridge_insert_sena();
