// =============================================================================
// OpenMotorBridge - Satellite Pod: Sena +Mesh & Multi-Series Slide-Mount Inlay
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/parts/01_insert_sena.scad
// Description: Standalone 3D printable top cradle insert for Sena intercoms &
//              off-the-shelf wireless adapters (e.g. Sena +Mesh B2M-01, 50S/60S).
//              Features:
//              - Dual longitudinal slide rails matching Sena OEM frame-mount plate
//              - Flexible cantilever snap latch with release trigger (Auslöser)
//              - Dual transverse hooks for Sena OEM rubber tension strap
//              - Recessed underfloor wiring channel for 90° USB power and RG178 coax
//              - Convective thermal breathing slots and vertical screwdriver bores
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module cartridge_insert_sena(
    insert_l = 110.0,
    insert_w = 53.0,
    deck_th  = 2.5,
    cradle_h = 11.0
) {
    difference() {
        union() {
            // 1. Intermediate Partition Deck (Grundplatte at z = 0 .. deck_th)
            cube(size=[insert_l, insert_w, deck_th], center=false);

            // 2. Sena Dual Longitudinal Slide Rails (Parallel to long X side)
            // Left Guide Rail (y = 6.0 .. 9.5 mm) with Inward Retaining Lip
            translate([15.0, 6.0, deck_th]) {
                cube(size=[insert_l - 30.0, 3.5, cradle_h], center=false);
                // Inward retaining lip (at top)
                translate([0, 3.5, cradle_h - 2.5])
                    cube(size=[insert_l - 30.0, 1.8, 2.5], center=false);
            }

            // Right Guide Rail (y = insert_w - 9.5 .. insert_w - 6.0 mm) with Inward Retaining Lip
            translate([15.0, insert_w - 9.5, deck_th]) {
                cube(size=[insert_l - 30.0, 3.5, cradle_h], center=false);
                // Inward retaining lip (at top)
                translate([0, -1.8, cradle_h - 2.5])
                    cube(size=[insert_l - 30.0, 1.8, 2.5], center=false);
            }

            // 3. Cantilever Snap Latch with Release Trigger (Auslöser am vorderen Ende)
            // Latch arm rising from deck with release paddle
            translate([insert_l - 25.0, insert_w/2.0 - 5.0, deck_th]) {
                // Cantilever spring arm
                cube(size=[18.0, 10.0, 2.2], center=false);
                // Locking wedge tooth
                translate([4.0, 0, 2.2])
                    polyhedron(
                        points=[
                            [0, 0, 0], [4.0, 0, 0], [4.0, 10.0, 0], [0, 10.0, 0],
                            [0, 0, 3.0], [4.0, 0, 0], [4.0, 10.0, 0], [0, 10.0, 3.0]
                        ],
                        faces=[
                            [0,1,2,3], [4,5,6,7], [0,4,7,3], [1,2,6,5], [0,1,5,4], [3,7,6,2]
                        ]
                    );
                // Textured Release Paddle / Trigger (Auslöser)
                translate([10.0, 0, 2.0]) {
                    cube(size=[8.0, 10.0, 4.0], center=false);
                    // Tactile grip grooves
                    for (gx = [2.0, 4.5, 7.0]) {
                        translate([gx, 0, 4.0])
                            cube(size=[0.8, 10.0, 0.6], center=false);
                    }
                }
            }

            // 4. Dual Transverse Hooks for Sena OEM Rubber Strap (Parallel to short Y side)
            // Rear Short-Side Hook (x = 4.0 mm, centered in Y)
            translate([4.0, insert_w/2.0 - 6.0, deck_th]) {
                difference() {
                    cube(size=[3.5, 12.0, cradle_h], center=false);
                    // Undercut retention lip
                    translate([1.5, -0.5, 2.0])
                        cube(size=[2.5, 13.0, cradle_h - 4.5], center=false);
                }
            }

            // Front Short-Side Hook (x = insert_l - 7.5 mm, centered in Y)
            translate([insert_l - 7.5, insert_w/2.0 - 6.0, deck_th]) {
                difference() {
                    cube(size=[3.5, 12.0, cradle_h], center=false);
                    // Undercut retention lip
                    translate([-0.5, -0.5, 2.0])
                        cube(size=[2.5, 13.0, cradle_h - 4.5], center=false);
                }
            }

            // 5. Outer Side Wall Stiffening Ledges (Continuous lateral support)
            translate([0, 0, deck_th])
                cube(size=[insert_l, 2.0, cradle_h - 3.0], center=false);
            translate([0, insert_w - 2.0, deck_th])
                cube(size=[insert_l, 2.0, cradle_h - 3.0], center=false);
        }

        // 6. Cantilever Latch Arm Flexure Slit (Enables downward spring deflection)
        translate([insert_l - 27.0, insert_w/2.0 - 6.0, -1.0])
            cube(size=[21.0, 1.2, deck_th + 3.0], center=false);
        translate([insert_l - 27.0, insert_w/2.0 + 4.8, -1.0])
            cube(size=[21.0, 1.2, deck_th + 3.0], center=false);
        translate([insert_l - 27.0, insert_w/2.0 - 6.0, -1.0])
            cube(size=[1.5, 12.0, deck_th + 3.0], center=false);

        // 7. Through-Deck Wiring & Cable Pass-Throughs (z = -1 .. 15 mm)
        // A. Lower Carrier PCB Header J2 Wiring Window (x = 14.0 .. 34.0 mm, y = 18.0 .. 35.0 mm)
        translate([14.0, insert_w/2.0 - 8.5, -1.0])
            cube(size=[20.0, 17.0, deck_th + cradle_h + 2.0], center=false);

        // B. Underfloor 90° USB-Pigtail & Coaxial Cable Routing Channel (x = 34.0 .. 85.0 mm)
        translate([34.0, insert_w/2.0 - 6.0, -1.0])
            cube(size=[50.0, 12.0, deck_th + 1.2], center=false);

        // C. Front Antenna Coax Clearance Notch (Direct path to SMA bulkhead on faceplate)
        translate([insert_l - 18.0, insert_w/2.0 - 15.0, -1.0])
            cube(size=[20.0, 8.0, deck_th + cradle_h + 2.0], center=false);

        // 8. 4x Convective Airflow & Breathing Slots
        translate([16.0, 11.5, -1.0])
            cube(size=[16.0, 3.0, deck_th + 2.0], center=false);
        translate([16.0, insert_w - 14.5, -1.0])
            cube(size=[16.0, 3.0, deck_th + 2.0], center=false);
        translate([70.0, 11.5, -1.0])
            cube(size=[16.0, 3.0, deck_th + 2.0], center=false);
        translate([70.0, insert_w - 14.5, -1.0])
            cube(size=[16.0, 3.0, deck_th + 2.0], center=false);

        // 9. 4x Screwdriver Vertical Access Clearances (Eckfreistellungen)
        translate([3.5, 3.5, deck_th - 0.1])
            cylinder(r=3.8, h=cradle_h + 2.0, center=false);
        translate([insert_l - 4.5, 3.5, deck_th - 0.1])
            cylinder(r=3.8, h=cradle_h + 2.0, center=false);
        translate([3.5, insert_w - 3.5, deck_th - 0.1])
            cylinder(r=3.8, h=cradle_h + 2.0, center=false);
        translate([insert_l - 4.5, insert_w - 3.5, deck_th - 0.1])
            cylinder(r=3.8, h=cradle_h + 2.0, center=false);

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
