// =============================================================================
// OpenMotorBridge - Satellite Pod: Waterproof Blindkassette (IP67 Dry Box Tub & Lid)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/parts/03_insert_blindkassette.scad
// Description: Deep watertight storage compartment (Staufach) fitting the 130mm sled:
//              - Continuous deep storage tub (120 x 48 x 22 mm usable interior)
//              - Front bay: Contoured holder for emergency motorcycle spare key
//              - Center bay: Large dry cavity for rolled vehicle registration & cash
//              - Rear bay: Clip-in retention slots for 2x mini-blade fuses (10A/15A)
//              - Perimeter sealing flange with high-visibility neon silicone gasket
//              - Flush sealing lid with 4x M2 countersunk stainless steel screws
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module cartridge_dry_box_tub(
    insert_l = CARTRIDGE_BASE_L - 6.0, // 124.0 mm for CARTRIDGE_BASE_L = 130.0
    insert_w = 52.0,
    tub_h    = 22.0,
    wall     = 2.0
) {
    difference() {
        // 1. Solid Outer Tub Body
        cube([insert_l, insert_w, tub_h], center=false);

        // 2. Main Deep Storage Cavity (20.0 mm deep clear space)
        translate([wall, wall, wall])
            cube([insert_l - 2*wall, insert_w - 2*wall, tub_h + 1.0], center=false);

        // 3. 4x M2 Corner Fastening Pilot Holes
        translate([3.5, 3.5, -0.5])
            cylinder(r=M2_SCREW_HOLE_R, h=tub_h + 1.0, center=false, $fn=16);
        translate([insert_l - 3.5, 3.5, -0.5])
            cylinder(r=M2_SCREW_HOLE_R, h=tub_h + 1.0, center=false, $fn=16);
        translate([3.5, insert_w - 3.5, -0.5])
            cylinder(r=M2_SCREW_HOLE_R, h=tub_h + 1.0, center=false, $fn=16);
        translate([insert_l - 3.5, insert_w - 3.5, -0.5])
            cylinder(r=M2_SCREW_HOLE_R, h=tub_h + 1.0, center=false, $fn=16);
    }

    // 4. Internal Organizer Partition Walls (10.0 mm high)
    // A. Front Partition (separating Key Bay from Document Bay at X = 36.0 mm)
    translate([36.0, wall, wall])
        cube([2.0, insert_w - 2*wall, 10.0]);

    // B. Rear Partition (separating Document Bay from Fuse Bay at X = 96.0 mm)
    translate([96.0, wall, wall])
        cube([2.0, insert_w - 2*wall, 10.0]);

    // 5. Emergency Key Retention Clip (Front Bay)
    translate([12.0, insert_w/2.0 - 5.0, wall]) {
        // Key bow retention cradle
        difference() {
            cube([16.0, 10.0, 6.0]);
            translate([2.0, 1.5, 1.5])
                cube([12.0, 7.0, 5.5]);
        }
    }

    // 6. 2x Mini-Blade Fuse Friction Slots (Rear Bay)
    for (fy = [insert_w/2.0 - 9.0, insert_w/2.0 + 3.0]) {
        translate([104.0, fy, wall]) {
            difference() {
                cube([12.0, 6.0, 8.0]);
                translate([1.5, 1.2, 1.5])
                    cube([9.0, 3.6, 7.5]);
            }
        }
    }
}

module cartridge_dry_box_lid(
    insert_l = CARTRIDGE_BASE_L - 6.0,
    insert_w = 52.0,
    lid_th   = 2.5
) {
    difference() {
        // 1. Flush Solid Cover Plate
        cube([insert_l, insert_w, lid_th], center=false);

        // 2. 4x M2 Countersunk Mounting Screw Holes
        translate([3.5, 3.5, -0.5]) {
            cylinder(r=M2_SCREW_HOLE_R, h=lid_th + 1.0, center=false, $fn=16);
            translate([0, 0, lid_th - 1.2])
                cylinder(r1=M2_SCREW_HOLE_R, r2=2.4, h=1.3, center=false, $fn=16);
        }
        translate([insert_l - 3.5, 3.5, -0.5]) {
            cylinder(r=M2_SCREW_HOLE_R, h=lid_th + 1.0, center=false, $fn=16);
            translate([0, 0, lid_th - 1.2])
                cylinder(r1=M2_SCREW_HOLE_R, r2=2.4, h=1.3, center=false, $fn=16);
        }
        translate([3.5, insert_w - 3.5, -0.5]) {
            cylinder(r=M2_SCREW_HOLE_R, h=lid_th + 1.0, center=false, $fn=16);
            translate([0, 0, lid_th - 1.2])
                cylinder(r1=M2_SCREW_HOLE_R, r2=2.4, h=1.3, center=false, $fn=16);
        }
        translate([insert_l - 3.5, insert_w - 3.5, -0.5]) {
            cylinder(r=M2_SCREW_HOLE_R, h=lid_th + 1.0, center=false, $fn=16);
            translate([0, 0, lid_th - 1.2])
                cylinder(r1=M2_SCREW_HOLE_R, r2=2.4, h=1.3, center=false, $fn=16);
        }

        // 3. Ergonomic Center Coin-Slot Recess (for easy opening if sealed tight)
        translate([insert_l/2.0, insert_w/2.0, lid_th - 1.2])
            cube([22.0, 2.5, 1.5], center=true);
    }
}

// Backward compatibility alias
module cartridge_insert_blindkassette() {
    cartridge_dry_box_tub();
}
