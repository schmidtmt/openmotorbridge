// =============================================================================
// OpenMotorBridge - Satellite Pod: Leerkassette / Staufach Einlegeboden
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/parts/03_insert_blindkassette.scad
// Description: Clean organizer insert plate mounted directly on the sled floor (am Boden):
//              - Sits at Z = 2.5 mm on sled floor, screwed into 4x M2 corner bosses
//              - Front bay: Contoured retention cradle for emergency motorcycle spare key
//              - Middle bay: Deep open storage compartment for folded registration papers / cash
//              - Rear bay: 2x friction clip slots for mini-blade backup fuses (10A & 15A)
//              - 100% open-top design: sealed and protected by the pod tunnel upon insertion
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module cartridge_insert_blindkassette(
    insert_l = CARTRIDGE_BASE_L - 6.0, // 124.0 mm for CARTRIDGE_BASE_L = 130.0
    insert_w = 52.0,
    plate_th = 2.5,
    wall_h   = 9.5
) {
    difference() {
        union() {
            // 1. Solid Bottom Plate (sitting directly on sled floor)
            cube([insert_l, insert_w, plate_th], center=false);

            // 2. Perimeter Rim Rib (protects items, gives rigid tray structure)
            difference() {
                cube([insert_l, insert_w, wall_h], center=false);
                translate([2.0, 2.0, plate_th])
                    cube([insert_l - 4.0, insert_w - 4.0, wall_h + 1.0], center=false);
            }

            // 3. Divider Partitions
            // Front partition at X = 36.0 mm (Key bay)
            translate([36.0, 2.0, plate_th])
                cube([2.0, insert_w - 4.0, wall_h - plate_th]);
            // Rear partition at X = 96.0 mm (Document bay to Fuse bay)
            translate([96.0, 2.0, plate_th])
                cube([2.0, insert_w - 4.0, wall_h - plate_th]);

            // 4. Emergency Motorcycle Key Retention Cradle (Front Bay)
            translate([12.0, insert_w/2.0 - 5.5, plate_th]) {
                difference() {
                    cube([16.0, 11.0, 5.5]);
                    translate([2.0, 1.5, 1.2])
                        cube([12.0, 8.0, 5.0]);
                }
            }

            // 5. 2x Mini-Blade Fuse Retention Clips (Rear Bay)
            for (fy = [insert_w/2.0 - 9.0, insert_w/2.0 + 3.0]) {
                translate([104.0, fy, plate_th]) {
                    difference() {
                        cube([12.0, 6.0, 7.5]);
                        translate([1.5, 1.2, 1.2])
                            cube([9.0, 3.6, 7.0]);
                    }
                }
            }
        }

        // 6. 4x M2 Countersunk Screw Mounting Holes into Sled Floor Corner Bosses
        // Boss positions in base sled: X=6.0, L-7.0, Y=6.0, W-6.0 relative to sled [0,0]
        // Sled insert is translated by [3.0, (58-52)/2=3.0], so local holes are at:
        // X = 3.5, insert_l - 3.5; Y = 3.0, insert_w - 3.0
        for (hx = [3.5, insert_l - 3.5]) {
            for (hy = [3.0, insert_w - 3.0]) {
                translate([hx, hy, -0.5]) {
                    cylinder(r=M2_SCREW_HOLE_R, h=wall_h + 2.0, center=false, $fn=16);
                    translate([0, 0, plate_th - 1.2 + 0.5])
                        cylinder(r1=M2_SCREW_HOLE_R, r2=2.4, h=1.3, center=false, $fn=16);
                }
            }
        }
    }
}

// Standalone printable preview
cartridge_insert_blindkassette();
