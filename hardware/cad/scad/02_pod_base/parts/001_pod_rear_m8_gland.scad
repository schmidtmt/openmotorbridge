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

// 3. Port B: Internal Enclosing Sleeve Boss (Seals rear chamber around USB-C tunnel)
module pod_rear_usbc_internal_sleeve(
    depth=10.0,
    outer_w=17.0,
    outer_h=11.5,
    yc=43.0,
    zc=19.0
) {
    translate([0, yc, zc]) {
        rotate([0, 90, 0])
            hull() {
                translate([-(outer_h/2 - 2.0), -(outer_w/2 - 2.0), 0])
                    cylinder(r=2.0, h=depth, center=false, $fn=24);
                translate([(outer_h/2 - 2.0), -(outer_w/2 - 2.0), 0])
                    cylinder(r=2.0, h=depth, center=false, $fn=24);
                translate([-(outer_h/2 - 2.0), (outer_w/2 - 2.0), 0])
                    cylinder(r=2.0, h=depth, center=false, $fn=24);
                translate([(outer_h/2 - 2.0), (outer_w/2 - 2.0), 0])
                    cylinder(r=2.0, h=depth, center=false, $fn=24);
            }
    }
}

// 4. Port B: Recessed USB-C Vertical Socket Plug-Well & Pass-Through Tool
module pod_rear_usbc_pocket_tool(
    wall_th=18.0,
    pocket_depth=7.0,
    pocket_w=14.0,
    pocket_h=8.5,
    port_w=9.6,
    port_h=4.0,
    yc=43.0,
    zc=19.0
) {
    // A. Recessed Plug-Well on Rear Exterior (7.0 mm deep: accepts USB-C cable overmold)
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

    // B. Inner Receptacle Seat Tunnel (meets the 9.5 mm vertical USB-C socket on the PCB at x = 16.4)
    translate([pocket_depth - 0.1, yc, zc]) {
        rotate([0, 90, 0])
            hull() {
                translate([-(port_h/2 - 1.0), -(port_w/2 - 1.0), 0])
                    cylinder(r=1.0, h=wall_th, center=false, $fn=20);
                translate([(port_h/2 - 1.0), -(port_w/2 - 1.0), 0])
                    cylinder(r=1.0, h=wall_th, center=false, $fn=20);
                translate([-(port_h/2 - 1.0), (port_w/2 - 1.0), 0])
                    cylinder(r=1.0, h=wall_th, center=false, $fn=20);
                translate([(port_h/2 - 1.0), (port_w/2 - 1.0), 0])
                    cylinder(r=1.0, h=wall_th, center=false, $fn=20);
            }
    }
}

// Standalone preview
union() {
    pod_rear_m8_neck(yc=26.0, zc=19.0);
    translate([0, 44.0 - 26.0, 0])
        #pod_rear_usbc_pocket_tool(yc=26.0, zc=19.0);
}
