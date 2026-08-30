// =============================================================================
// OpenMotorBridge - Screw Bosses & Fastener Primitives
// =============================================================================
// File: hardware/cad/scad/00_common/screw_bosses.scad
// Description: Reusable parametric modules for screw standoffs, corner clamping
//              posts, and mounting ears.
// =============================================================================

include <parameters.scad>;

// 1. Cylindrical Screw Standoff Boss (with center hole)
module screw_boss(outer_r=2.5, inner_r=1.2, h=5.0) {
    difference() {
        cylinder(r=outer_r, h=h, center=false);
        translate([0, 0, -0.1])
            cylinder(r=inner_r, h=h + 0.2, center=false);
    }
}

// 2. Rectangular Corner Clamping Post (with center screw hole)
module corner_screw_post(size_x=5.0, size_y=5.0, h=12.0, hole_r=1.65, hole_h=10.0, hole_offset_z=2.0) {
    difference() {
        cube(size=[size_x, size_y, h], center=false);
        translate([size_x/2.0, size_y/2.0, hole_offset_z])
            cylinder(r=hole_r, h=hole_h + 0.1, center=false);
    }
}

// 3. M4 Silentblock Outer Mounting Ear (with rubber buffer hole)
module mounting_ear_m4(ear_len=12.0, ear_w=10.0, ear_h=6.0, hole_r=2.2) {
    difference() {
        union() {
            cube(size=[ear_len - ear_w/2.0, ear_w, ear_h], center=false);
            translate([ear_len - ear_w/2.0, ear_w/2.0, 0])
                cylinder(r=ear_w/2.0, h=ear_h, center=false);
        }
        translate([ear_len - ear_w/2.0, ear_w/2.0, -0.1])
            cylinder(r=hole_r, h=ear_h + 0.2, center=false);
    }
}

// 4. Copper Thermal Stud Pad / Pocket
module copper_stud(r=COPPER_STUD_R, h=2.5) {
    color("darkorange")
        cylinder(r=r, h=h, center=false);
}
