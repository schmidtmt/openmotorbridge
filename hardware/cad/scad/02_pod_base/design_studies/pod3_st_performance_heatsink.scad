// =============================================================================
// OpenMotorBridge - Satellite Pod 3: ST Performance Billet Heatsink (V3 - Racing Cowl)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/pod3_st_performance_heatsink.scad
// Description: MotoAmerica / King of the Baggers racing telemetry nacelle for Low Rider ST.
//              Features:
//              1. Fully enclosed aerodynamic racing cowl.
//              2. M8 Left-Exit Under-Wing Cable Route: 100% invisible, wide bending radii
//                 (R >= 35 mm), exits into OEM strut channel (forged carbon cowl untouched!).
//              3. Integrated Dorsal Shark Fin with 5 dBi 2.4 GHz Antenna Snap-In Channel.
//              4. Top Telemetry Window with CNC Bezel for GNSS Patch & Gore-Vent Breather.
//              5. 7 bold horizontal CNC cooling fins (4.5 mm depth) matching M-8 cylinder heads.
//              6. CNC skeletal truss strut brackets with 3 triangular machined windows.
//              7. 100% 2-manifold geometry (0 non-manifold edges).
// =============================================================================

include <../00_common/parameters.scad>;

FENDER_R_TRANS = 140.0;
POD_L          = 136.0;
POD_W          = 71.0;
POD_H          = 38.5;

ST_FUSE_W      = 90.0;  // 90 mm base width gives deep 5 mm wall for cooling fin cuts
ST_TOP_W       = 78.0;  // 78 mm shoulder width
ST_COWL_H      = 49.0;  // 49 mm height -> solid 5 mm roof over internal pod
R_CORNER       = 6.0;

WING_HALF_SPAN = 130.0;
LEG_DROP_Z     = -32.0;
LEG_LEN_X      = 72.0;

X_PROW_TIP    = -138.0;
X_POD_FRONT   = -68.0;
X_POD_REAR    = +68.0;
X_DIFF_TIP    = +138.0;

// High-fidelity 2D cross-section slice in Y-Z plane
module st_slice_2d(w_b, w_t, h, r_b=5.0, r_t=6.0) {
    hull() {
        translate([r_b, -w_b/2.0 + r_b]) circle(r=r_b, $fn=24);
        translate([r_b,  w_b/2.0 - r_b]) circle(r=r_b, $fn=24);
        translate([h - r_t, -w_t/2.0 + r_t]) circle(r=r_t, $fn=24);
        translate([h - r_t,  w_t/2.0 - r_t]) circle(r=r_t, $fn=24);
    }
}

module st_slice_yz(x, w_b, w_t, h, r_b=5.0, r_t=6.0, dx=0.4) {
    translate([x, 0, 0])
    rotate([0, -90, 0])
    linear_extrude(height=dx, center=true) {
        st_slice_2d(w_b, w_t, h, r_b, r_t);
    }
}

// Keyframe lofting for the aerodynamic telemetry cowl
ST_LOFT_KEYS = [
    [-138.0,  36.0,  28.0,   8.0, 3.0, 4.0],  // 0: Prow nose tip
    [-118.0,  58.0,  46.0,  20.0, 4.0, 5.0],  // 1: Forward wedge rise
    [ -92.0,  76.0,  64.0,  35.0, 5.0, 6.0],  // 2: Seat transition
    [ -68.0,  90.0,  78.0,  48.0, 5.0, 6.0],  // 3: Pod front
    [ -30.0,  92.0,  80.0,  49.0, 5.0, 6.0],  // 4: Pod center-front
    [ +10.0,  92.0,  80.0,  49.0, 5.0, 6.0],  // 5: Pod center-rear
    [ +50.0,  91.0,  79.0,  48.5, 5.0, 6.0],  // 6: Pod rear
    [ +68.0,  89.0,  77.0,  46.0, 5.0, 6.0],  // 7: Rear step
    [ +98.0,  84.0,  72.0,  40.0, 5.0, 5.0],  // 8: Diffuser cowl
    [+120.0,  78.0,  68.0,  32.0, 4.0, 5.0],  // 9: Diffuser mouth frame
    [+138.0,  74.0,  64.0,  26.0, 4.0, 4.0]   // 10: Exhaust bezel tip
];

module st_aerodynamic_cowl_hull() {
    num_k = len(ST_LOFT_KEYS);
    for (i = [0 : num_k - 2]) {
        k0 = ST_LOFT_KEYS[i];
        k1 = ST_LOFT_KEYS[i + 1];
        hull() {
            st_slice_yz(k0[0], k0[1], k0[2], k0[3], k0[4], k0[5]);
            st_slice_yz(k1[0], k1[1], k1[2], k1[3], k1[4], k1[5]);
        }
    }
}

// Authentic CNC Skeletal Truss Strut Bracket (Winglet)
module cnc_skeletal_strut_bracket(side=1) {
    mirror([0, side < 0 ? 1 : 0, 0]) {
        difference() {
            union() {
                // 1. Diagonal Truss Arm Sweeping from Nacelle Root to Strut
                hull() {
                    // Nacelle body root
                    translate([-24.0, ST_FUSE_W/2.0 - 4.0, 14.0])
                        cube([48.0, 4.0, 16.0], center=false);
                    // Strut bracket top transition
                    translate([-LEG_LEN_X/2.0 + 8.0, WING_HALF_SPAN - 12.0, LEG_DROP_Z + 16.0])
                        cube([LEG_LEN_X - 16.0, 10.0, 10.0], center=false);
                }

                // 2. Vertical Strut Mounting Plate
                translate([-LEG_LEN_X/2.0, WING_HALF_SPAN - 10.0, LEG_DROP_Z])
                    cube([LEG_LEN_X, 10.0, 28.0], center=false);
            }

            // Machined CNC Skeletal Truss Windows (3 angled slots through bracket)
            for (i = [-1, 0, 1]) {
                translate([i * 16.0, 85.0, -1.0])
                    rotate([25, 0, 0])
                        cube([10.0, 45.0, 30.0], center=true);
            }
        }
    }
}

// Dorsal Shark Fin with 5 dBi 2.4 GHz Antenna Snap-In Channel
module st_dorsal_shark_fin() {
    difference() {
        // 1. Solid aerodynamic fin body standing on rear diffuser
        hull() {
            translate([68.0, 0, 44.0]) cylinder(r=6.5, h=4.0, center=false, $fn=24);
            translate([98.0, 0, 60.0]) cylinder(r=5.5, h=4.0, center=false, $fn=24);
            translate([136.0, 0, 26.0]) cylinder(r=4.5, h=4.0, center=false, $fn=24);
            translate([72.0, 0, 36.0]) cube([60.0, 13.0, 4.0], center=true);
        }
        
        // 2. Snap-in C-channel for 5 dBi Antenna (Ø 9.2 mm) along dorsal trailing slope
        hull() {
            translate([68.0, 0, 45.0]) rotate([0, 72, 0]) cylinder(r=4.6, h=75.0, center=false, $fn=24);
            translate([68.0, 0, 47.0]) rotate([0, 72, 0]) cylinder(r=3.8, h=75.0, center=false, $fn=24);
        }
        // Top slot for snap-in insertion (width 7.6 mm for tactile click retention)
        translate([68.0, -3.8, 44.0]) rotate([0, 72, 0]) cube([75.0, 7.6, 20.0], center=false);

        // 3. Forward Antenna Coax Pigtail Conduit (Ø 3.2 mm) into internal chamber
        translate([65.0, 0, 42.0]) rotate([0, 90, 0]) cylinder(r=1.6, h=10.0, center=true, $fn=16);
    }
}

// Bold Horizontal Cooling Fins / Speed-Ribs (Milwaukee-Eight 117 Engine Match)
module m8_deep_cooling_fins() {
    fin_z = [11.0, 16.5, 22.0, 27.5, 33.0, 38.5, 44.0];
    for (z_pos = fin_z) {
        for (side = [-1, 1]) {
            y_pos = side * (ST_FUSE_W/2.0 + 1.0);
            translate([0, y_pos, z_pos]) {
                rotate([0, 90, 0]) {
                    hull() {
                        translate([0, -side * 1.5, -95.0]) cylinder(r=1.5, h=190.0, center=true, $fn=16);
                        translate([0, -side * 6.5, -90.0]) cylinder(r=2.5, h=180.0, center=true, $fn=16);
                    }
                }
            }
        }
    }
}

// Top Radiator Strakes / Longitudinal Louvres flanking the telemetry window
module top_radiator_strakes() {
    y_flank_offsets = [-26.0, +26.0];
    for (y_off = y_flank_offsets) {
        hull() {
            translate([-50.0, y_off, 49.5]) sphere(r=1.6, $fn=16);
            translate([+65.0, y_off, 49.0]) sphere(r=1.6, $fn=16);
            translate([+95.0, y_off, 42.0]) sphere(r=1.6, $fn=16);
        }
    }
}

// Technical Top Telemetry / GNSS & Gore-Vent Membrane Aperture
module st_top_telemetry_aperture() {
    translate([-10.0, 0, 48.0]) {
        hull() {
            for (dx = [-20.0, 20.0]) {
                for (dy = [-18.0, 18.0]) {
                    translate([dx, dy, 0]) cylinder(r=3.5, h=25.0, center=true, $fn=24);
                }
            }
        }
    }
    translate([-10.0, 0, 48.5]) {
        hull() {
            for (dx = [-23.0, 23.0]) {
                for (dy = [-21.0, 21.0]) {
                    translate([dx, dy, 0]) cylinder(r=4.5, h=4.0, center=true, $fn=24);
                }
            }
        }
    }
}

// Internal Enclosed Slide-In Chamber for Pod 3
module pod3_internal_chamber_st() {
    // 1. Pod dock chamber (floor at Z = 5.0 mm -> 3.5 mm solid floor over fender crown)
    translate([-POD_L/2.0, -POD_W/2.0, 5.0])
        cube([POD_L, POD_W, POD_H], center=false);

    // 2. Rear Cartridge Slide Exit Mouth through Diffuser Bezel
    translate([POD_L/2.0 - 2.0, -37.0, 5.0])
        cube([76.0, 74.0, 36.0], center=false);

    // 3. Front M8 Gland Straight Chamber (X = -68 to -98 mm, 30 mm long)
    translate([-POD_L/2.0 - 30.0, -11.0, 19.0 - 11.0])
        cube([32.0, 22.0, 22.0], center=false);

    // 4. Strap Hook Reliefs inside chamber
    hook_x = [-POD_L/2.0 + 25.0, -POD_L/2.0 + 110.0];
    for (hx = hook_x) {
        translate([hx - 7.0, -POD_W/2.0 - 1.0, 5.0]) cube([14.0, 2.5, 10.0]);
        translate([hx - 7.0,  POD_W/2.0 - 1.5, 5.0]) cube([14.0, 2.5, 10.0]);
    }
}

// Left Under-Wing M8 Cable Channel (100% invisible, sweeps left to strut channel)
module st_left_underwing_cable_channel() {
    // Large bending radius (R >= 35 mm) from nose into left wing underside
    hull() {
        translate([-96.0, 0, 19.0]) cylinder(r=5.5, h=10.0, center=true, $fn=24);
        translate([-88.0, -22.0, 14.0]) cylinder(r=5.0, h=10.0, center=true, $fn=24);
    }
    hull() {
        translate([-88.0, -22.0, 14.0]) cylinder(r=5.0, h=10.0, center=true, $fn=24);
        translate([-65.0, -42.0, 8.0]) cylinder(r=4.8, h=10.0, center=true, $fn=24);
    }
    
    // Underside left wing conduit out to strut foot (Y = -42 to -125 mm)
    hull() {
        translate([-65.0, -42.0, 8.0]) cylinder(r=4.8, h=10.0, center=true, $fn=24);
        translate([-32.0, -78.0, -2.0]) cylinder(r=4.6, h=10.0, center=true, $fn=24);
    }
    hull() {
        translate([-32.0, -78.0, -2.0]) cylinder(r=4.6, h=10.0, center=true, $fn=24);
        translate([-10.0, -122.0, -16.0]) cylinder(r=4.5, h=10.0, center=true, $fn=24);
    }
    
    // Strut wire exit opening (into Harley OEM strut wire channel)
    translate([-16.0, -WING_HALF_SPAN - 2.0, LEG_DROP_Z + 10.0])
        cube([18.0, 14.0, 14.0], center=false);
}

module pod3_st_performance_heatsink() {
    difference() {
        // 1. Solid Aerodynamic Cowl, Billet Strut Brackets & Dorsal Shark Fin
        union() {
            st_aerodynamic_cowl_hull();

            for (side = [-1, 1]) {
                cnc_skeletal_strut_bracket(side);
            }

            // Dorsal Shark Fin with 5 dBi Antenna Channel
            st_dorsal_shark_fin();
        }

        // 2. Internal Slide-In Chamber for Pod 3
        pod3_internal_chamber_st();

        // 3. Deep Milwaukee-Eight Cooling Fins / Speed-Ribs along Flanks
        m8_deep_cooling_fins();

        // 4. Top Radiator Louvres / Strakes
        top_radiator_strakes();

        // 5. Technical GNSS Patch & Gore-Vent Membrane Aperture
        st_top_telemetry_aperture();

        // 6. Left Under-Wing M8 Cable Channel (Bypasses carbon cowl!)
        st_left_underwing_cable_channel();

        // 7. Strut Mounting Bolt Counterbores (OEM 35 mm spacing)
        for (x_bolt = [-17.5, +17.5]) {
            // Left strut bolt & washer counterbore
            translate([x_bolt, -WING_HALF_SPAN - 2.0, LEG_DROP_Z + 14.0])
                rotate([-90, 0, 0]) cylinder(r=4.6, h=16.0, center=false, $fn=24);
            translate([x_bolt, -WING_HALF_SPAN + 6.0, LEG_DROP_Z + 14.0])
                rotate([-90, 0, 0]) cylinder(r=8.5, h=10.0, center=false, $fn=24);

            // Right strut bolt & washer counterbore
            translate([x_bolt, WING_HALF_SPAN - 14.0, LEG_DROP_Z + 14.0])
                rotate([-90, 0, 0]) cylinder(r=4.6, h=16.0, center=false, $fn=24);
            translate([x_bolt, WING_HALF_SPAN - 6.0, LEG_DROP_Z + 14.0])
                rotate([-90, 0, 0]) cylinder(r=8.5, h=10.0, center=false, $fn=24);
        }

        // 8. Fender crown clearance
        translate([0, 0, -(FENDER_R_TRANS - 2.0)]) {
            rotate([0, 90, 0])
                cylinder(r=FENDER_R_TRANS, h=360.0, center=true, $fn=64);
        }
    }
}

pod3_st_performance_heatsink();
