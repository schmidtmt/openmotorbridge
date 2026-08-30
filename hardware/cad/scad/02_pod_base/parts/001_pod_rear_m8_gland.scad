// =============================================================================
// OpenMotorBridge - Satellite Pod: Rear M8 Cable Gland Neck & Through-Bore
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/001_pod_rear_m8_gland.scad
// =============================================================================

include <../../00_common/parameters.scad>;

// 1. Outer M8 6-Pin IP67 Cable Stutzen (Horizontal cylinder along X axis)
module pod_rear_m8_neck(neck_len=10.0, outer_r=6.0, inner_r=4.0, yc=30.0, zc=14.0) {
    translate([-neck_len, yc, zc]) {
        difference() {
            rotate([0, 90, 0])
                cylinder(r=outer_r, h=neck_len, center=false);
            translate([-0.1, 0, 0])
                rotate([0, 90, 0])
                    cylinder(r=inner_r, h=neck_len + 0.2, center=false);
        }
    }
}

// 2. M8 Rear Wall Through-Hole Cutout Tool (Ø 8.0 mm through-bore)
module pod_rear_m8_through_hole_tool(wall_th=5.0, inner_r=4.0, yc=30.0, zc=14.0) {
    translate([-1.0, yc, zc])
        rotate([0, 90, 0])
            cylinder(r=inner_r, h=wall_th + 2.0, center=false);
}

// Standalone preview
pod_rear_m8_neck();
