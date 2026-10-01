// =============================================================================
// OpenMotorBridge - Satellite Pod: Rear Dual-Port Glands & Pockets (Port A & B)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/001_pod_rear_m8_gland.scad
// Description: Parametric features for Dual-Port architecture on pod rear wall:
//              - Port A: Square pass-through opening (11.5 x 11.5 mm) allowing
//                the massive square base of the M8 PCB receptacle to pass through
//                the rear wall without requiring extra pod length or interior space.
//              - Port B: Deep recessed USB-C socket pocket (14.0 x 8.5 x 7.0 mm)
//                with 45° lead-in chamfer and internal isolating sleeve boss.
//              - Sealing pocket for flush TPU dust plug (pod_base_usbc_cap_tpu).
// =============================================================================

include <../../00_common/parameters.scad>;

// 1. Port A: Low-Profile M8 Collar / Outer Sealing Shoulder (X = -2.0 .. 0.0 mm)
module pod_rear_m8_neck(collar_len=2.0, outer_size=16.0, inner_size=11.5, r_corner=1.5, yc=27.0, zc=19.0) {
    translate([-collar_len, yc, zc]) {
        difference() {
            rotate([0, 90, 0])
                hull() {
                    translate([-(outer_size/2 - 2.5), -(outer_size/2 - 2.5), 0])
                        cylinder(r=2.5, h=collar_len + 0.1, center=false, $fn=24);
                    translate([(outer_size/2 - 2.5), -(outer_size/2 - 2.5), 0])
                        cylinder(r=2.5, h=collar_len + 0.1, center=false, $fn=24);
                    translate([-(outer_size/2 - 2.5), (outer_size/2 - 2.5), 0])
                        cylinder(r=2.5, h=collar_len + 0.1, center=false, $fn=24);
                    translate([(outer_size/2 - 2.5), (outer_size/2 - 2.5), 0])
                        cylinder(r=2.5, h=collar_len + 0.1, center=false, $fn=24);
                }
            translate([-0.1, 0, 0])
                rotate([0, 90, 0])
                    hull() {
                        translate([-(inner_size/2 - r_corner), -(inner_size/2 - r_corner), 0])
                            cylinder(r=r_corner, h=collar_len + 0.5, center=false, $fn=24);
                        translate([(inner_size/2 - r_corner), -(inner_size/2 - r_corner), 0])
                            cylinder(r=r_corner, h=collar_len + 0.5, center=false, $fn=24);
                        translate([-(inner_size/2 - r_corner), (inner_size/2 - r_corner), 0])
                            cylinder(r=r_corner, h=collar_len + 0.5, center=false, $fn=24);
                        translate([(inner_size/2 - r_corner), (inner_size/2 - r_corner), 0])
                            cylinder(r=r_corner, h=collar_len + 0.5, center=false, $fn=24);
                    }
        }
    }
}

// 2. Port A: Rear Wall Cutout Tool for M8 Square Base Pass-Through
//    (11.5 x 11.5 mm with R = 1.5 mm corner radius; cuts cleanly through 3.5 mm rear wall)
module pod_rear_m8_through_hole_tool(wall_th=8.0, base_size=11.5, r_corner=1.5, yc=27.0, zc=19.0) {
    translate([-2.5, yc, zc]) {
        rotate([0, 90, 0])
            hull() {
                translate([-(base_size/2 - r_corner), -(base_size/2 - r_corner), 0])
                    cylinder(r=r_corner, h=wall_th + 3.0, center=false, $fn=24);
                translate([(base_size/2 - r_corner), -(base_size/2 - r_corner), 0])
                    cylinder(r=r_corner, h=wall_th + 3.0, center=false, $fn=24);
                translate([-(base_size/2 - r_corner), (base_size/2 - r_corner), 0])
                    cylinder(r=r_corner, h=wall_th + 3.0, center=false, $fn=24);
                translate([(base_size/2 - r_corner), (base_size/2 - r_corner), 0])
                    cylinder(r=r_corner, h=wall_th + 3.0, center=false, $fn=24);
            }
    }
}

// 3. Port B: Internal Enclosing Sleeve Boss (Seals rear chamber around USB-C tunnel to PCB at X=16.4)
module pod_rear_usbc_internal_sleeve(
    depth=14.0,
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
    // A. 45° Lead-in Chamfer at outer mouth (X = -0.5 .. 1.0 mm)
    translate([-0.6, yc, zc]) {
        rotate([0, 90, 0])
            hull() {
                translate([-(pocket_h/2 - 0.5), -(pocket_w/2 - 0.5), 0])
                    cylinder(r=2.5, h=1.6, center=false, $fn=24);
                translate([(pocket_h/2 - 0.5), -(pocket_w/2 - 0.5), 0])
                    cylinder(r=2.5, h=1.6, center=false, $fn=24);
                translate([-(pocket_h/2 - 0.5), (pocket_w/2 - 0.5), 0])
                    cylinder(r=2.5, h=1.6, center=false, $fn=24);
                translate([(pocket_h/2 - 0.5), (pocket_w/2 - 0.5), 0])
                    cylinder(r=2.5, h=1.6, center=false, $fn=24);
            }
    }

    // B. Recessed Plug-Well on Rear Exterior (7.0 mm deep: accepts USB-C cable overmold)
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

    // C. Inner Receptacle Seat Tunnel (meets the 9.5 mm vertical USB-C socket on the PCB at x = 16.4)
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
    pod_rear_m8_neck(yc=27.0, zc=19.0);
    translate([0, 43.0 - 27.0, 0])
        #pod_rear_usbc_pocket_tool(yc=27.0, zc=19.0);
}
