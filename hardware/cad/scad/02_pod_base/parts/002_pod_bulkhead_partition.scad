// =============================================================================
// OpenMotorBridge - Satellite Pod: Monolithic Bulkhead & Contact Interface
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/002_pod_bulkhead_partition.scad
// Description: 100% Monolithic, screw-free partition wall integrated directly
//              into the 1-piece pod base housing (zero assembly screws!).
//              Features:
//              - 2x Mill-Max heavy-duty DC spring contact sleeves (10.0 mm pitch:
//                Y = 30.0 mm for +12V/5V and Y = 40.0 mm for GND, matching PAD1 & PAD2
//                on PCBA 03).
//              - 2x Auto-Eject spring guide posts (for Ø 4.5 mm V4A springs at
//                Y = 16.0 mm and Y = 54.0 mm).
//              - Hermetic internal partition isolating the rear cable chamber
//                from the front slide chamber.
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module pod_bulkhead_assembly(bulkhead_x=18.0, wall=3.5) {
    z_contacts = wall + 2.5 + 2.5; // Z = 8.5 mm (matches PCBA 03 B.Cu gold pads in sled)

    // 1. Monolithic Vertical Partition Wall (Fused directly into tunnel at x = 18.0 mm)
    translate([bulkhead_x, wall, wall]) {
        difference() {
            // Solid transverse bulkhead (2.5 mm thickness)
            cube(size=[2.5, POD_OUTER_W - 2*wall, POD_OUTER_H - 2*wall], center=false);

            // 2x Mill-Max Spring Contact Through-Bores (Ø 3.2 mm at Y = 30.0 and Y = 40.0)
            translate([-0.5, 30.0 - wall, z_contacts - wall])
                rotate([0, 90, 0])
                    cylinder(r=1.6, h=3.5, center=false, $fn=24);

            translate([-0.5, 40.0 - wall, z_contacts - wall])
                rotate([0, 90, 0])
                    cylinder(r=1.6, h=3.5, center=false, $fn=24);

            // 2x Convective Pressure Equalization Vents (Left & Right top corners)
            translate([-0.5, 5.0, POD_OUTER_H - 2*wall - 5.0])
                cube(size=[3.5, 4.0, 2.0], center=false);
            translate([-0.5, POD_OUTER_W - 2*wall - 9.0, POD_OUTER_H - 2*wall - 5.0])
                cube(size=[3.5, 4.0, 2.0], center=false);
        }
    }

    // 2. 2x Mill-Max Spring Contact Protective Boss Sleeves (projecting +X into chamber)
    // Provides solid mechanical guidance and axial retention for the gold contact pins
    translate([bulkhead_x + 2.5, 30.0, z_contacts]) {
        rotate([0, 90, 0]) {
            difference() {
                cylinder(r=3.0, h=3.0, center=false, $fn=24);
                translate([0, 0, -0.1])
                    cylinder(r=1.6, h=3.2, center=false, $fn=24);
            }
        }
    }
    translate([bulkhead_x + 2.5, 40.0, z_contacts]) {
        rotate([0, 90, 0]) {
            difference() {
                cylinder(r=3.0, h=3.0, center=false, $fn=24);
                translate([0, 0, -0.1])
                    cylinder(r=1.6, h=3.2, center=false, $fn=24);
            }
        }
    }

    // 3. 2x Auto-Eject Spring Retainer Posts (for Ø 4.5 mm V4A Springs at Y = 16.0 and Y = 54.0)
    // Symmetrical ±19.0 mm from pod centerline (Y = 35.0 mm)
    translate([bulkhead_x + 2.5, 16.0, POD_OUTER_H/2.0])
        rotate([0, 90, 0])
            cylinder(r=1.8, h=6.0, $fn=16);

    translate([bulkhead_x + 2.5, POD_OUTER_W - 16.0, POD_OUTER_H/2.0])
        rotate([0, 90, 0])
            cylinder(r=1.8, h=6.0, $fn=16);
}

// Standalone preview
pod_bulkhead_assembly();
