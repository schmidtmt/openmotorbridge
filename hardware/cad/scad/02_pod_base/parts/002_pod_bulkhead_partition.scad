// =============================================================================
// OpenMotorBridge - Satellite Pod: Bulkhead Partition & 6-Pin Shroud Funnel
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/002_pod_bulkhead_partition.scad
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module pod_bulkhead_assembly(bulkhead_x=22.0, wall=2.5) {
    // 1. Vertical Partition Bulkhead Wall (x = 22.0 mm)
    translate([bulkhead_x, wall, wall]) {
        difference() {
            cube(size=[2.0, POD_OUTER_W - 2*wall, POD_OUTER_H - 2*wall], center=false);

            // 6-Pin Interface Center Window
            translate([-0.5, (POD_OUTER_W - 2*wall)/2.0 - 5.0, (POD_OUTER_H - 2*wall)/2.0 - 3.5])
                cube(size=[3.0, 10.0, 7.0], center=false);

            // 2x Convective Breathing Slots (Left & Right)
            translate([-0.5, 6.0, (POD_OUTER_H - 2*wall)/2.0 - 1.0])
                cube(size=[3.0, 6.0, 2.0], center=false);
            translate([-0.5, POD_OUTER_W - 2*wall - 12.0, (POD_OUTER_H - 2*wall)/2.0 - 1.0])
                cube(size=[3.0, 6.0, 2.0], center=false);
        }
    }

    // 2. 6-Pin Protective Shroud with 45° Lead-in Funnel
    translate([bulkhead_x + 2.0, POD_OUTER_W/2.0 - 6.0, POD_OUTER_H/2.0 - 4.0]) {
        difference() {
            cube(size=[4.0, 12.0, 8.0], center=false);
            translate([-0.1, 1.0, 1.0])
                cube(size=[4.2, 10.0, 6.0], center=false);
        }
    }

    // 3. 2x Auto-Eject Spring Retainer Posts (V4A Springs at y = 16 and y = 44)
    translate([bulkhead_x + 2.0, 16.0, POD_OUTER_H/2.0])
        rotate([0, 90, 0])
            cylinder(r=2.5, h=5.0);

    translate([bulkhead_x + 2.0, 44.0, POD_OUTER_H/2.0])
        rotate([0, 90, 0])
            cylinder(r=2.5, h=5.0);

    // 4. 4x M2 Screw Standoff Bosses (for Bulkhead Mounting to Tunnel)
    translate([bulkhead_x, 5.0, wall])
        rotate([0, 90, 0])
            screw_boss(outer_r=2.0, inner_r=M2_SCREW_HOLE_R, h=3.0);
    translate([bulkhead_x, POD_OUTER_W - 5.0, wall])
        rotate([0, 90, 0])
            screw_boss(outer_r=2.0, inner_r=M2_SCREW_HOLE_R, h=3.0);
    translate([bulkhead_x, 5.0, POD_OUTER_H - wall])
        rotate([0, 90, 0])
            screw_boss(outer_r=2.0, inner_r=M2_SCREW_HOLE_R, h=3.0);
    translate([bulkhead_x, POD_OUTER_W - 5.0, POD_OUTER_H - wall])
        rotate([0, 90, 0])
            screw_boss(outer_r=2.0, inner_r=M2_SCREW_HOLE_R, h=3.0);
}

// Standalone preview
pod_bulkhead_assembly();
