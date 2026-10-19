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

            // 2. Integrated LiPo Battery Cradle Frame (71.0 x 42.0 x 4.0 mm, fits 2200 mAh 5.0mm flat cell)
            translate([17.0, 13.0, floor_t]) {
                difference() {
                    cube(size=[71.0, 42.0, 4.0], center=false);
                    // Inner cavity for battery
                    translate([1.5, 1.5, -0.1])
                        cube(size=[68.0, 39.0, 4.2], center=false);
                    // Left Side: 2x Hinge Pivot Sockets (for 013_battery_antenna_bridge tabs)
                    translate([-0.5, 9.0, 0.5])
                        cube(size=[2.5, 5.0, 3.6], center=false);
                    translate([-0.5, 27.0, 0.5])
                        cube(size=[2.5, 5.0, 3.6], center=false);
                    // Right Side: Snap Catch Recess (for 013 cantilever latch barb)
                    translate([71.0 - 1.5, 10.0, 0.2])
                        cube(size=[2.0, 12.0, 2.4], center=false);
                }
            }
        }

        // 3. Wide Open Front Cable Bay (70 x 10 mm open toward front Y=0)
        // Seamlessly clears all 6 cables (12-Pin, 10-Pin, Battery, Power, LoRa, 2.4G)
        translate([18.0, -0.5, -0.5])
            cube(size=[69.0, 10.5, floor_t + 1.0], center=false);

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
    }
}

// Standalone preview
main_box_mid_partition_floor();

