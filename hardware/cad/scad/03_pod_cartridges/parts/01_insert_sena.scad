// =============================================================================
// OpenMotorBridge - Satellite Pod: Sena +Mesh Transverse Slide-Mount Inlay
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/parts/01_insert_sena.scad
// Description: Standalone 3D printable top cradle insert for Sena +Mesh (B2M-01)
//              and modular Sena intercoms.
//              Accurately reproduces the Sena OEM mounting geometry:
//              - Dual transverse guide rails along the SHORT axis (Y-axis)
//                spaced exactly 30 mm apart, each ~19 mm long with undercut retaining lips
//              - Transverse slide-in motion from lateral edge into positive retention lock
//              - Flexible cantilever snap latch with tactile release trigger (Auslöser)
//              - Lateral alignment ridges matching the +Mesh housing profile
//              - Dual retention hooks for Sena OEM heavy-duty rubber strap
//              - Underfloor wiring channel for 90° USB power and antenna coaxial cable
//              - 4x M2 countersunk mounting holes concentric with base sled posts
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module cartridge_insert_sena(
    insert_l = 110.0,
    insert_w = 53.0,
    deck_th  = 2.5,
    cradle_h = 10.0
) {
    // Kinematic & geometry parameters matching Sena +Mesh OEM bracket:
    // Hooks on +Mesh are spaced ~30 mm apart along X, ~19 mm long along Y
    rail_spacing = 30.0;
    rail_len     = 19.0;
    rail_h       = 5.5;
    lip_overhang = 1.6;
    lip_th       = 1.8;
    
    // Position rails centered along length X
    x_mid = insert_l / 2.0;               // 55.0 mm
    x1    = x_mid - rail_spacing / 2.0;   // 40.0 mm
    x2    = x_mid + rail_spacing / 2.0;   // 70.0 mm
    
    // Position rails along width Y (short axis slide travel)
    // Slide entry at y = 14.0 mm, locked home position at y = 33.0 mm
    y_entry = 14.0;
    y_stop  = y_entry + rail_len;         // 33.0 mm

    difference() {
        union() {
            // 1. Intermediate Partition Deck (Grundplatte at z = 0 .. deck_th)
            cube(size=[insert_l, insert_w, deck_th], center=false);

            // 2. Dual Transverse Slide Guide Rails (Parallel to short Y side)
            // Rear Rail at x1 = 40.0 mm
            translate([x1 - 2.0, y_entry, deck_th]) {
                // Vertical riser
                cube(size=[4.0, rail_len, rail_h], center=false);
                // Inward retaining lip (flange overhanging in +X towards center)
                translate([4.0, 0, rail_h - lip_th])
                    cube(size=[lip_overhang, rail_len, lip_th], center=false);
                // Slide entry lead-in chamfer
                translate([4.0, 0, rail_h - lip_th])
                    rotate([0, 0, 45])
                        cube(size=[lip_overhang * 1.4, 1.5, lip_th], center=false);
            }

            // Front Rail at x2 = 70.0 mm
            translate([x2 - 2.0, y_entry, deck_th]) {
                // Vertical riser
                cube(size=[4.0, rail_len, rail_h], center=false);
                // Inward retaining lip (flange overhanging in -X towards center)
                translate([-lip_overhang, 0, rail_h - lip_th])
                    cube(size=[lip_overhang, rail_len, lip_th], center=false);
                // Slide entry lead-in chamfer
                translate([-lip_overhang, 0, rail_h - lip_th])
                    rotate([0, 0, -45])
                        cube(size=[lip_overhang * 1.4, 1.5, lip_th], center=false);
            }

            // 3. Positive Slide Travel End Stops (at y = y_stop)
            translate([x1 - 2.0, y_stop, deck_th])
                cube(size=[4.0 + lip_overhang, 3.0, rail_h + 1.5], center=false);
            translate([x2 - 2.0 - lip_overhang, y_stop, deck_th])
                cube(size=[4.0 + lip_overhang, 3.0, rail_h + 1.5], center=false);

            // 4. Longitudinal Alignment & Cradle Ridges (Matching +Mesh 45mm housing width)
            // Left longitudinal ridge (y = 4.0 .. 7.0 mm)
            translate([22.0, 4.0, deck_th])
                cube(size=[insert_l - 44.0, 3.0, 4.0], center=false);
            // Right longitudinal ridge (y = insert_w - 7.0 .. insert_w - 4.0 mm)
            translate([22.0, insert_w - 7.0, deck_th])
                cube(size=[insert_l - 44.0, 3.0, 4.0], center=false);

            // 5. Cantilever Snap Latch with Release Trigger (Auslöser am Ende der Schiebebahn)
            // Positioned between rails at x_mid = 55.0 mm, latching the +Mesh along Y
            translate([x_mid - 5.0, y_stop + 3.0, deck_th]) {
                // Cantilever spring arm
                cube(size=[10.0, 11.0, 2.2], center=false);
                // Ramped latch tooth facing the incoming +Mesh (100% clean manifold wedge via hull)
                translate([0, 1.0, 2.2]) {
                    hull() {
                        cube(size=[10.0, 0.1, 2.8], center=false);
                        cube(size=[10.0, 3.5, 0.1], center=false);
                    }
                }
                // Textured Release Paddle / Trigger (Auslöser)
                translate([0, 5.0, 2.0]) {
                    cube(size=[10.0, 6.0, 4.5], center=false);
                    for (gy = [1.5, 3.2, 4.8]) {
                        translate([0, gy, 4.5])
                            cube(size=[10.0, 0.7, 0.6], center=false);
                    }
                }
            }

            // 6. Dual Retention Hooks for Sena OEM Rubber Strap (Spannband-Haken)
            // Hook 1: Leading edge (x = 5.0 mm, centered in Y)
            translate([5.0, insert_w/2.0 - 5.0, deck_th]) {
                difference() {
                    cube(size=[3.5, 10.0, cradle_h], center=false);
                    // Undercut retention lip for rubber band
                    translate([1.5, -0.5, 2.0])
                        cube(size=[2.5, 11.0, cradle_h - 4.0], center=false);
                }
            }
            // Hook 2: Trailing edge (x = insert_l - 8.5 mm, centered in Y)
            translate([insert_l - 8.5, insert_w/2.0 - 5.0, deck_th]) {
                difference() {
                    cube(size=[3.5, 10.0, cradle_h], center=false);
                    // Undercut retention lip for rubber band
                    translate([-0.5, -0.5, 2.0])
                        cube(size=[2.5, 11.0, cradle_h - 4.0], center=false);
                }
            }

            // 7. Outer Side Wall Stiffening Ledges (Continuous lateral support)
            translate([0, 0, deck_th])
                cube(size=[insert_l, 1.8, 5.0], center=false);
            translate([0, insert_w - 1.8, deck_th])
                cube(size=[insert_l, 1.8, 5.0], center=false);
        }

        // 8. Cantilever Latch Arm Flexure Slits (Enables elastic downward deflection)
        translate([x_mid - 6.2, y_stop + 2.0, -1.0])
            cube(size=[1.2, 13.0, deck_th + 3.0], center=false);
        translate([x_mid + 5.0, y_stop + 2.0, -1.0])
            cube(size=[1.2, 13.0, deck_th + 3.0], center=false);
        translate([x_mid - 6.2, y_stop + 14.0, -1.0])
            cube(size=[12.4, 1.2, deck_th + 3.0], center=false);

        // 9. Through-Deck Wiring & Cable Pass-Throughs (z = -1 .. 15 mm)
        // A. Lower Carrier PCB Header J2 Wiring Window (x = 14.0 .. 34.0 mm, y = 18.0 .. 35.0 mm)
        translate([14.0, insert_w/2.0 - 8.5, -1.0])
            cube(size=[20.0, 17.0, deck_th + cradle_h + 2.0], center=false);

        // B. Underfloor 90° USB-Pigtail & Coaxial Cable Routing Channel (x = 34.0 .. 85.0 mm)
        translate([34.0, insert_w/2.0 - 6.0, -1.0])
            cube(size=[50.0, 12.0, deck_th + 1.2], center=false);

        // C. Front Antenna Coax Clearance Notch (Direct path to SMA bulkhead on faceplate)
        translate([insert_l - 18.0, insert_w/2.0 - 15.0, -1.0])
            cube(size=[20.0, 8.0, deck_th + cradle_h + 2.0], center=false);

        // 10. 4x Convective Airflow & Breathing Slots
        translate([16.0, 8.0, -1.0])
            cube(size=[14.0, 2.8, deck_th + 2.0], center=false);
        translate([16.0, insert_w - 10.8, -1.0])
            cube(size=[14.0, 2.8, deck_th + 2.0], center=false);
        translate([78.0, 8.0, -1.0])
            cube(size=[14.0, 2.8, deck_th + 2.0], center=false);
        translate([78.0, insert_w - 10.8, -1.0])
            cube(size=[14.0, 2.8, deck_th + 2.0], center=false);

        // 11. 4x Screwdriver Vertical Access Clearances (Eckfreistellungen)
        translate([3.5, 3.5, deck_th - 0.1])
            cylinder(r=3.8, h=cradle_h + 2.0, center=false);
        translate([insert_l - 4.5, 3.5, deck_th - 0.1])
            cylinder(r=3.8, h=cradle_h + 2.0, center=false);
        translate([3.5, insert_w - 3.5, deck_th - 0.1])
            cylinder(r=3.8, h=cradle_h + 2.0, center=false);
        translate([insert_l - 4.5, insert_w - 3.5, deck_th - 0.1])
            cylinder(r=3.8, h=cradle_h + 2.0, center=false);

        // 12. 4x M2 Countersunk Mounting Screw Holes (DIN 7991 M2)
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
