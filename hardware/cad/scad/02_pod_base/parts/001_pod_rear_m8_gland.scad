// =============================================================================
// OpenMotorBridge - Satellite Pod: Rear Dual-Port Glands & Pockets (Port A & B)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/001_pod_rear_m8_gland.scad
// Description: Parametric features for Dual-Port architecture on pod rear wall:
//              - Port A: Outer M8 6-Pin IP67 threaded cable gland neck (shifted left)
//              - Port B: Recessed USB-C Slim socket pocket & pass-through (shifted right)
//              - Sealing pocket for flush TPU dust plug (pod_base_usbc_cap_tpu)
// =============================================================================

include <../../00_common/parameters.scad>;

// 1. Outer M8 6-Pin IP67 Cable Stutzen (Horizontal cylinder along X axis, Port A)
module pod_rear_m8_neck(neck_len=10.0, outer_r=6.0, inner_r=4.0, yc=26.0, zc=19.0) {
    translate([-neck_len, yc, zc]) {
        difference() {
            rotate([0, 90, 0])
                cylinder(r=outer_r, h=neck_len + 2.0, center=false, $fn=32);
            translate([-0.1, 0, 0])
                rotate([0, 90, 0])
                    cylinder(r=inner_r, h=neck_len + 4.0, center=false, $fn=32);
        }
    }
}

// 2. M8 Rear Wall Through-Hole Cutout Tool (Ø 8.0 mm through-bore, Port A)
module pod_rear_m8_through_hole_tool(wall_th=5.0, inner_r=4.0, yc=26.0, zc=19.0) {
    translate([-1.0, yc, zc])
        rotate([0, 90, 0])
            cylinder(r=inner_r, h=wall_th + 2.0, center=false, $fn=32);
}

// 3. Port B: Recessed USB-C Slim Socket Outer Pocket & Pass-Through Tool
module pod_rear_usbc_pocket_tool(
    wall_th=5.0,
    pocket_depth=2.5,
    pocket_w=12.0,
    pocket_h=6.5,
    port_w=9.2,
    port_h=3.6,
    yc=44.0,
    zc=19.0
) {
    // A. Flush Recessed Pocket on Rear Exterior (holds TPU plug flange flush)
    translate([-0.5, yc, zc]) {
        rotate([0, 90, 0])
            hull() {
                translate([-(pocket_h/2 - 1.5), -(pocket_w/2 - 1.5), 0])
                    cylinder(r=1.5, h=pocket_depth + 0.5, center=false, $fn=24);
                translate([(pocket_h/2 - 1.5), -(pocket_w/2 - 1.5), 0])
                    cylinder(r=1.5, h=pocket_depth + 0.5, center=false, $fn=24);
                translate([-(pocket_h/2 - 1.5), (pocket_w/2 - 1.5), 0])
                    cylinder(r=1.5, h=pocket_depth + 0.5, center=false, $fn=24);
                translate([(pocket_h/2 - 1.5), (pocket_w/2 - 1.5), 0])
                    cylinder(r=1.5, h=pocket_depth + 0.5, center=false, $fn=24);
            }
    }

    // B. Inner Through-Window into Chamber for USB-C Receptacle
    translate([-1.0, yc, zc]) {
        rotate([0, 90, 0])
            hull() {
                translate([-(port_h/2 - 1.0), -(port_w/2 - 1.0), 0])
                    cylinder(r=1.0, h=wall_th + 3.0, center=false, $fn=20);
                translate([(port_h/2 - 1.0), -(port_w/2 - 1.0), 0])
                    cylinder(r=1.0, h=wall_th + 3.0, center=false, $fn=20);
                translate([-(port_h/2 - 1.0), (port_w/2 - 1.0), 0])
                    cylinder(r=1.0, h=wall_th + 3.0, center=false, $fn=20);
                translate([(port_h/2 - 1.0), (port_w/2 - 1.0), 0])
                    cylinder(r=1.0, h=wall_th + 3.0, center=false, $fn=20);
            }
    }
}

// Standalone preview
union() {
    pod_rear_m8_neck(yc=26.0, zc=19.0);
    translate([0, 44.0 - 26.0, 0])
        #pod_rear_usbc_pocket_tool(yc=26.0, zc=19.0);
}
