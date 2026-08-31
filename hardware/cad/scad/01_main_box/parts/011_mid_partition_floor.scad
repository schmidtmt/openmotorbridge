// =============================================================================
// OpenMotorBridge - Main Box: Mid Partition Floor (Zwischenboden)
// =============================================================================
// File: hardware/cad/scad/01_main_box/parts/011_mid_partition_floor.scad
// =============================================================================

include <../../00_common/parameters.scad>;

module main_box_mid_partition_floor(floor_l=105.0, floor_w=69.0, floor_t=2.0) {
    difference() {
        union() {
            // 1. Solid Base Floor Plate
            cube(size=[floor_l, floor_w, floor_t], center=false);

            // 2. Integrated LiPo Battery Cradle Frame (52 x 37 x 4.0 mm, fits 1000 mAh cell)
            translate([26.5, 16.0, floor_t]) {
                difference() {
                    cube(size=[54.0, 39.0, 4.0], center=false);
                    translate([1.5, 1.5, -0.1])
                        cube(size=[51.0, 36.0, 4.2], center=false);
                }
            }
        }

        // 3. Front Wire Routing Slot (for Battery wires & internal flex connections: 25 x 4 mm)
        translate([40.0, 4.0, -0.5])
            cube(size=[25.0, 4.0, floor_t + 1.0], center=false);

        // 4. Enhanced Convective Ventilation & Air Circulation Slots (10x slots):
        // Rear Row (5x slots along y = 58.0 mm)
        for (i = [0:4]) {
            translate([15.0 + i * 16.0, 58.0, -0.5])
                cube(size=[12.0, 2.5, floor_t + 1.0], center=false);
        }

        // Left Side Flank (2x slots along x = 10.0 mm)
        translate([10.0, 20.0, -0.5]) cube(size=[2.5, 14.0, floor_t + 1.0], center=false);
        translate([10.0, 38.0, -0.5]) cube(size=[2.5, 14.0, floor_t + 1.0], center=false);

        // Right Side Flank (2x slots along x = 92.0 mm)
        translate([92.0, 20.0, -0.5]) cube(size=[2.5, 14.0, floor_t + 1.0], center=false);
        translate([92.0, 38.0, -0.5]) cube(size=[2.5, 14.0, floor_t + 1.0], center=false);

        // Front Row Flanks (2x slots along y = 8.0 mm)
        translate([15.0, 8.0, -0.5]) cube(size=[14.0, 2.5, floor_t + 1.0], center=false);
        translate([76.0, 8.0, -0.5]) cube(size=[14.0, 2.5, floor_t + 1.0], center=false);
    }
}

// Standalone preview
main_box_mid_partition_floor();
