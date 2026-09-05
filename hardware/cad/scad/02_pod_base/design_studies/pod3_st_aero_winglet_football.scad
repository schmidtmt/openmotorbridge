// =============================================================================
// OpenMotorBridge - Satellite Pod 3: ST Aero-Winglet Nacelle (Master: Direct Football Loft)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/pod3_st_aero_winglet_football.scad
// Description: Master aerodynamic nacelle for Harley Low Rider ST / Touring ST.
//              Features:
//              1. Direct loft from base-cube into double-curved football nose (100% enclosed pod front).
//              2. Compound 3D football curved winglets to OEM fender struts (130 mm half-span).
//              3. Dorsal shark fin tail with integrated antenna channel.
//              4. 100% 2-manifold geometry (zero slicer import errors).
// =============================================================================

include <../00_common/parameters.scad>;
use <parts/007_pod_slide_dock_core.scad>;

FENDER_R_TRANS = 140.0;
ST_POD_L      = 136.0;
ST_FUSE_W     = 78.0;
ST_DOCK_H     = 40.5;
R_CORNER      = 7.0;

WING_HALF_SPAN = 130.0;
LEG_DROP_Z     = -32.0;
LEG_LEN_X      = 54.0;
WING_THICK     = 8.0;

X_WEDGE_TIP   = -148.0;
X_POD_FRONT   = -68.0;
X_POD_REAR    = +68.0;
X_DIFF_TIP    = +145.0;

// Prolate Spheroid Wing Parameters
FB_X0 = -35.0;
FB_Y0 = 35.0;
FB_Z0 = -42.0;
FB_RX = 100.0;
FB_RY = 96.5;
FB_RZ = 60.0;

module rounded_slab(l, w, h, r=6.0) {
    linear_extrude(height=h, center=false) {
        hull() {
            for (dx = [-l/2 + r, l/2 - r]) {
                for (dy = [-w/2 + r, w/2 - r]) {
                    translate([dx, dy]) circle(r=r, $fn=24);
                }
            }
        }
    }
}

// Cross-section slice in Y-Z plane for continuous nose morphing
module nose_slice_yz(x, w, h, r, dx=0.5) {
    translate([x, 0, 0])
    rotate([0, -90, 0])
    linear_extrude(height=dx, center=true) {
        hull() {
            for (dy = [-w/2 + r, w/2 - r]) {
                for (dz = [r, h - r]) {
                    translate([dz, dy]) circle(r=r, $fn=24);
                }
            }
        }
    }
}

// 1. Direct Morphing Football Nose
// Morphs seamlessly from base-cube (X = -68, W = 78, H = 40.5) to football tip (X = -148)
module direct_football_nose(l_nose=80.0, w_base=ST_FUSE_W, h_base=ST_DOCK_H, r_base=R_CORNER, x_start=X_POD_FRONT, steps=12) {
    for (i = [0 : steps - 1]) {
        t0 = i / steps;
        t1 = (i + 1) / steps;
        
        x0 = x_start - t0 * l_nose;
        x1 = x_start - t1 * l_nose;
        
        // Elliptical football curve k(t) = sqrt(1 - t^2)
        k0 = sqrt(max(0.001, 1.0 - t0*t0));
        k1 = sqrt(max(0.001, 1.0 - t1*t1));
        
        w0 = max(6.0, w_base * k0);
        w1 = max(6.0, w_base * k1);
        
        h0 = max(4.0, h_base * k0);
        h1 = max(4.0, h_base * k1);
        
        r0 = max(2.0, r_base * k0);
        r1 = max(2.0, r_base * k1);
        
        hull() {
            nose_slice_yz(x0, w0, h0, r0, dx=0.2);
            nose_slice_yz(x1, w1, h1, r1, dx=0.2);
        }
    }
}

// 2. Compound 3D Football Curved Wing (Left/Right)
module football_curved_wing(side=1) {
    union() {
        mirror([0, side < 0 ? 1 : 0, 0]) {
            intersection() {
                difference() {
                    translate([FB_X0, FB_Y0, FB_Z0])
                        scale([FB_RX, FB_RY, FB_RZ])
                            sphere(r=1.0, $fn=64);
                            
                    translate([FB_X0, FB_Y0, FB_Z0])
                        scale([FB_RX - WING_THICK, FB_RY - WING_THICK, FB_RZ - WING_THICK])
                            sphere(r=1.0, $fn=64);
                }

                // 90 deg quarter cut
                translate([FB_X0 - FB_RX - 10.0, FB_Y0 - 8.0, FB_Z0 - 5.0])
                    cube([2 * FB_RX + 20.0, FB_RY + 16.0, FB_RZ + 10.0]);

                // Jet planform
                translate([0, 0, -80.0])
                    linear_extrude(height=160.0, center=false, convexity=10)
                        polygon([
                            [-118.0, ST_FUSE_W/2.0 - 8.0],
                            [-34.0,  64.0],
                            [-27.0,  WING_HALF_SPAN],
                            [+27.0,  WING_HALF_SPAN],
                            [+24.0,  70.0],
                            [+38.0,  ST_FUSE_W/2.0 - 8.0]
                        ]);
            }
        }

        // Solid Vertical Mounting Ear at Strut
        translate([-LEG_LEN_X/2.0, side > 0 ? (WING_HALF_SPAN - 8.0) : -WING_HALF_SPAN, LEG_DROP_Z])
            cube([LEG_LEN_X, 8.0, 24.0], center=false);
            
        // Transition Fillet
        mirror([0, side < 0 ? 1 : 0, 0]) {
            hull() {
                translate([-27.0, WING_HALF_SPAN - 8.0, LEG_DROP_Z + 12.0])
                    cube([54.0, 8.0, 4.0], center=false);
                translate([-24.0, WING_HALF_SPAN - 12.0, LEG_DROP_Z + 20.0])
                    cube([48.0, 4.0, 4.0], center=false);
            }
        }
    }
}

// 3. Dorsal Shark Fin (positioned cleanly behind dock slide mouth at X >= 98 mm)
module dorsal_shark_fin() {
    difference() {
        hull() {
            translate([98.0, 0, 36.0]) rounded_slab(6.0, 8.0, 4.0, r=2.5);
            translate([114.0, 0, 54.0]) rounded_slab(14.0, 4.0, 4.0, r=1.5);
            translate([138.0, 0, 10.0]) rounded_slab(10.0, 5.0, 4.0, r=2.0);
            translate([108.0, 0, 22.0]) rounded_slab(28.0, 12.0, 12.0, r=4.0);
        }
        translate([98.0, 0, 22.0]) rotate([0, 72, 0]) cylinder(r=4.4, h=70.0, center=false, $fn=24);
        translate([97.0, -3.5, 14.0]) cube([45.0, 7.0, 26.0], center=false);
    }
}

module pod3_st_aero_winglet_football() {
    difference() {
        union() {
            // A. Base-Cube (Pod Cradle) with rounded flanks
            hull() {
                translate([X_POD_FRONT + 0.5, 0, 0]) rounded_slab(1.0, ST_FUSE_W, ST_DOCK_H, r=R_CORNER);
                translate([X_POD_REAR - 0.5, 0, 0]) rounded_slab(1.0, ST_FUSE_W, ST_DOCK_H, r=R_CORNER);
            }
            
            // B. Direct Football Nose (seamless morph from base-cube)
            direct_football_nose();

            // C. Rear Kamm-Tail Diffuser
            hull() {
                translate([X_POD_REAR - 1.0, 0, 0]) rounded_slab(2.0, ST_FUSE_W, ST_DOCK_H, r=R_CORNER);
                translate([X_POD_REAR + 38.0, 0, 0]) rounded_slab(2.0, 56.0, 18.0, r=R_CORNER);
                translate([X_DIFF_TIP - 6.0, 0, 0]) rounded_slab(12.0, 36.0, 6.0, r=4.0);
            }

            // D. Dorsal Shark Fin
            dorsal_shark_fin();

            // E. Compound 3D Football Wings (Left & Right)
            for (side = [-1, 1]) {
                football_curved_wing(side);
            }
        }

        // Subtractions:
        // 1. Pod 3 Dock Subtraction
        translate([0, 0, 2.5]) {
            pod_slide_dock_subtraction(
                dock_l = ST_POD_L,
                dock_w = 70.8,
                dock_h = 38.2,
                open_sky_h = 50.0
            );
        }

        // 2. Direct M8 Cable Bore (dives 42 deg forward-downward under the seat)
        translate([-72.0, 0, 19.0])
            rotate([0, 42, 0])
                cylinder(r=4.5, h=60.0, center=true, $fn=24);

        // 3. Strut Bolt Slots
        for (x_bolt = [-17.5, +17.5]) {
            translate([x_bolt, -WING_HALF_SPAN - 2.0, LEG_DROP_Z + 14.0])
                rotate([-90, 0, 0]) cylinder(r=4.6, h=14.0, center=false, $fn=24);
            translate([x_bolt - 4.6, -WING_HALF_SPAN - 2.0, LEG_DROP_Z + 11.0])
                cube([9.2, 14.0, 6.0], center=false);

            translate([x_bolt, WING_HALF_SPAN - 14.0, LEG_DROP_Z + 14.0])
                rotate([-90, 0, 0]) cylinder(r=4.6, h=16.0, center=false, $fn=24);
            translate([x_bolt - 4.6, WING_HALF_SPAN - 14.0, LEG_DROP_Z + 11.0])
                cube([9.2, 16.0, 6.0], center=false);
        }

        // 4. Fender crown clearance
        translate([0, 0, -(FENDER_R_TRANS - 2.0)]) {
            rotate([0, 90, 0])
                cylinder(r=FENDER_R_TRANS, h=abs(X_WEDGE_TIP) + X_DIFF_TIP + 20.0, center=true, $fn=64);
        }
    }
}

// Module alias for nacelle
module pod3_st_aero_winglet_nacelle() {
    pod3_st_aero_winglet_football();
}

pod3_st_aero_winglet_football();
