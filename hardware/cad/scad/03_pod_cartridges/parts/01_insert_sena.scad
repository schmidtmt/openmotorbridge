// =============================================================================
// OpenMotorBridge - Satellite Pod: Sena +Mesh Transverse Slide-Mount Inlay
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/parts/01_insert_sena.scad
// Description: Standalone 3D printable top cradle insert for Sena +Mesh (B2M-01)
//              and modular Sena intercoms.
//              Features:
//              - Solid, clean ergonomic cradle nest with recessed contour bed
//              - Dual transverse guide rails along the SHORT axis (Y-axis)
//                spaced exactly 30 mm apart, each ~19 mm long with undercut retaining lips
//              - Transverse slide-in motion from lateral edge into positive retention lock
//              - Integrated snap latch with ergonomic release trigger (Auslöser)
//              - Integrated outward-facing EPDM rubber strap retention hooks on both flanks (Nase für den Gummi)
//              - Clean through-deck wiring pass-through for 90° USB power & antenna coax
//              - Open corner cutouts giving 100% vertical screwdriver access
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module cartridge_insert_sena(
    insert_l = 110.0,
    insert_w = 53.0,
    deck_th  = 2.5,
    cradle_h = 10.0
) {
    // Kinematic parameters matching Sena +Mesh OEM hooks:
    // 2 hooks on +Mesh spaced 30 mm apart along X, ~19 mm long along Y
    rail_spacing = 30.0;
    rail_len     = 19.0;
    rail_h       = 5.0;
    lip_overhang = 1.6;
    lip_th       = 1.6;

    x_mid = insert_l / 2.0;              // 55.0 mm
    x1    = x_mid - rail_spacing / 2.0;  // 40.0 mm
    x2    = x_mid + rail_spacing / 2.0;  // 70.0 mm
    y_entry = 15.0;
    y_stop  = y_entry + rail_len;        // 34.0 mm

    difference() {
        union() {
            // 1. Intermediate Partition Deck (Grundplatte at z = 0 .. deck_th)
            cube(size=[insert_l, insert_w, deck_th], center=false);

            // 2. Sena 3D Ergonomic Cradle Body (Solid body from z = deck_th .. deck_th + cradle_h)
            translate([2.0, 1.5, deck_th]) {
                difference() {
                    cube(size=[insert_l - 4.0, insert_w - 3.0, cradle_h], center=false);

                    // A. Sena +Mesh Main Body Recessed Contour Bed (recessed 4.0 mm)
                    translate([2.0, 2.0, 2.0])
                        cube(size=[insert_l - 8.0, insert_w - 7.0, cradle_h + 0.1], center=false);
                }
            }

            // 3. Dual Transverse Slide Guide Rails (Parallel to short Y side inside cradle bed)
            // Rail 1 at x1 = 40.0 mm
            translate([x1 - 2.0, y_entry, deck_th + 2.0]) {
                // Vertical rail riser
                cube(size=[3.5, rail_len, rail_h], center=false);
                // Inward retaining lip (flange overhanging in +X towards center)
                translate([3.5, 0, rail_h - lip_th])
                    cube(size=[lip_overhang, rail_len, lip_th], center=false);
            }

            // Rail 2 at x2 = 70.0 mm
            translate([x2 - 1.5, y_entry, deck_th + 2.0]) {
                // Vertical rail riser
                cube(size=[3.5, rail_len, rail_h], center=false);
                // Inward retaining lip (flange overhanging in -X towards center)
                translate([-lip_overhang, 0, rail_h - lip_th])
                    cube(size=[lip_overhang, rail_len, lip_th], center=false);
            }

            // 4. Positive Slide Travel End Stops (at y = y_stop)
            translate([x1 - 2.0, y_stop, deck_th + 2.0])
                cube(size=[3.5 + lip_overhang, 2.5, rail_h + 1.0], center=false);
            translate([x2 - 1.5 - lip_overhang, y_stop, deck_th + 2.0])
                cube(size=[3.5 + lip_overhang, 2.5, rail_h + 1.0], center=false);

            // 5. Spring Snap Latch with Release Trigger (Auslöser)
            // Centered between rails at x_mid = 55.0 mm at the end of the slide travel
            translate([x_mid - 4.0, y_stop + 1.5, deck_th + 2.0]) {
                // Latch arm
                cube(size=[8.0, 8.0, 2.0], center=false);
                // Ramped locking wedge
                translate([0, 0.5, 2.0]) {
                    hull() {
                        cube(size=[8.0, 0.1, 2.5], center=false);
                        cube(size=[8.0, 3.0, 0.1], center=false);
                    }
                }
                // Release Trigger Paddle (Auslöser)
                translate([0, 4.0, 2.0]) {
                    cube(size=[8.0, 5.0, 4.0], center=false);
                    for (gy = [1.5, 3.2]) {
                        translate([0, gy, 4.0])
                            cube(size=[8.0, 0.6, 0.5], center=false);
                    }
                }
            }

            // 6. Outward-Facing Rubber Strap Overhang Ledges on Left & Right Flanks (Nase für den Gummi)
            // Exactly matching Cardo geometry at insert_l/2.0 - 6.0 mm
            // Left Flank Top Lip
            translate([insert_l/2.0 - 6.0, 0.5, deck_th + 5.0])
                cube(size=[12.0, 2.5, cradle_h - 5.0], center=false);
            // Right Flank Top Lip
            translate([insert_l/2.0 - 6.0, insert_w - 3.0, deck_th + 5.0])
                cube(size=[12.0, 2.5, cradle_h - 5.0], center=false);
        }

        // 7. 2x Outward-Facing EPDM Rubber Strap Undercut Hook Slots (Nase für den Gummi)
        // Band hooks under top lip from outside across both flanks
        // Left Hook Undercut Slot
        translate([insert_l/2.0 - 6.1, -0.5, deck_th + 1.0])
            cube(size=[12.2, 3.5, 4.2], center=false);
        // Right Hook Undercut Slot
        translate([insert_l/2.0 - 6.1, insert_w - 3.0, deck_th + 1.0])
            cube(size=[12.2, 3.5, 4.2], center=false);

        // 8. Clean Through-Deck Wiring Pass-Throughs (z = -1 .. 15 mm)
        // A. J2 Header & USB Power Cable Window
        translate([20.0, insert_w/2.0 - 7.5, -1.0])
            cube(size=[16.0, 15.0, deck_th + cradle_h + 2.0], center=false);

        // B. Front Antenna Coax Pigtail Window to SMA Bulkhead
        translate([insert_l - 24.0, insert_w/2.0 - 6.0, -1.0])
            cube(size=[14.0, 12.0, deck_th + cradle_h + 2.0], center=false);

        // 9. 4x Screwdriver Vertical Access Clearances (Eckfreistellungen)
        translate([3.5, 3.5, deck_th - 0.1])
            cylinder(r=3.8, h=cradle_h + 1.0, center=false);
        translate([insert_l - 4.5, 3.5, deck_th - 0.1])
            cylinder(r=3.8, h=cradle_h + 1.0, center=false);
        translate([3.5, insert_w - 3.5, deck_th - 0.1])
            cylinder(r=3.8, h=cradle_h + 1.0, center=false);
        translate([insert_l - 4.5, insert_w - 3.5, deck_th - 0.1])
            cylinder(r=3.8, h=cradle_h + 1.0, center=false);

        // 10. 4x M2 Countersunk Mounting Screw Holes (DIN 7991 M2)
        translate([3.5, 3.5, -0.5])
            cylinder(r=M2_SCREW_HOLE_R, h=deck_th + 1.0, center=false);
        translate([3.5, 3.5, deck_th - 1.2])
            cylinder(r1=M2_SCREW_HOLE_R, r2=2.3, h=1.3, center=false);

        translate([insert_l - 4.5, 3.5, -0.5])
            cylinder(r=M2_SCREW_HOLE_R, h=deck_th + 1.0, center=false);
        translate([insert_l - 4.5, 3.5, deck_th - 1.2])
            cylinder(r1=M2_SCREW_HOLE_R, r2=2.3, h=1.3, center=false);

        translate([3.5, insert_w - 3.5, -0.5])
            cylinder(r=M2_SCREW_HOLE_R, h=deck_th + 1.0, center=false);
        translate([3.5, insert_w - 3.5, deck_th - 1.2])
            cylinder(r1=M2_SCREW_HOLE_R, r2=2.3, h=1.3, center=false);

        translate([insert_l - 4.5, insert_w - 3.5, -0.5])
            cylinder(r=M2_SCREW_HOLE_R, h=deck_th + 1.0, center=false);
        translate([insert_l - 4.5, insert_w - 3.5, deck_th - 1.2])
            cylinder(r1=M2_SCREW_HOLE_R, r2=2.3, h=1.3, center=false);
    }
}

// Standalone printable preview
cartridge_insert_sena();
