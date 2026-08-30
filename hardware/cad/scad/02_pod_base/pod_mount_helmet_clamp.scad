// =============================================================================
// OpenMotorBridge - Satellite Pod: Helmet Clamp Mounting Bracket (Pod 1 & 2)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/pod_mount_helmet_clamp.scad
// Description: Ergonomic helmet shell clamping bracket for left/right helmet mounting.
// =============================================================================

include <../00_common/parameters.scad>;

module pod_mount_helmet_clamp(base_l=80.0, base_w=50.0, base_t=3.0, jaw_h=15.0) {
    difference() {
        union() {
            // 1. Base Plate (Bolts/clips to Pod bottom)
            cube(size=[base_l, base_w, base_t], center=false);

            // 2. Vertical Helmet Shell Drop Bracket
            translate([0, 0, -jaw_h])
                cube(size=[5.0, base_w, jaw_h], center=false);

            // 3. Inner Helmet Clamping Jaw (with 4° inward spring tension angle)
            translate([0, 0, -jaw_h - 3.0])
                cube(size=[30.0, base_w, 4.0], center=false);
        }

        // 4. 2x M3 Mounting Counterbores (to Pod base)
        translate([20.0, base_w/2.0, -jaw_h - 4.0])
            cylinder(r=M3_SCREW_HOLE_R, h=jaw_h + 10.0, center=false);
        translate([60.0, base_w/2.0, -jaw_h - 4.0])
            cylinder(r=M3_SCREW_HOLE_R, h=jaw_h + 10.0, center=false);
    }
}

// Render complete helmet clamp
pod_mount_helmet_clamp();
