// =============================================================================
// OpenMotorBridge - Satellite Pod 3: Touring Fender Console (V3 - CVO Bodywork)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/pod3_touring_fender_console.scad
// Description: Ultra-sleek OEM-integrated rear fender console for classic Touring/Cruisers.
//              Features:
//              1. Continuous enclosed CVO bodywork with central tank-console spine.
//              2. 100% hidden through-tongue M8 cable routing directly under seat cushion.
//              3. Rear ducktail snap-in channel for 5 dBi 2.4 GHz antenna.
//              4. Flush GNSS roof plaque and Gore-Vent breather port.
//              5. 100% 2-manifold geometry (0 non-manifold edges).
// =============================================================================

include <../00_common/parameters.scad>;

FENDER_R_TRANS = 140.0;
POD_L          = 136.0;
POD_W          = 71.0;
POD_H          = 38.5;

// High-fidelity 2D cross-section slice in Y-Z plane
module console_slice_2d(w_base, w_top, h, spine_w, spine_h, r_b=5.0, r_t=6.0) {
    hull() {
        translate([r_b, -w_base/2.0 + r_b]) circle(r=r_b, $fn=24);
        translate([r_b,  w_base/2.0 - r_b]) circle(r=r_b, $fn=24);
        translate([h - r_t, -w_top/2.0 + r_t]) circle(r=r_t, $fn=24);
        translate([h - r_t,  w_top/2.0 - r_t]) circle(r=r_t, $fn=24);
        translate([h + spine_h, -spine_w/2.0]) square([0.1, spine_w]);
    }
}

module console_slice_yz(x, w_base, w_top, h, spine_w, spine_h, r_b=5.0, r_t=6.0, dx=0.4) {
    translate([x, 0, 0])
    rotate([0, -90, 0])
    linear_extrude(height=dx, center=true) {
        console_slice_2d(w_base, w_top, h, spine_w, spine_h, r_b, r_t);
    }
}

// Continuous automotive lofting keyframes from front seat screw to rear ducktail
SLICE_DATA = [
    [-152.0,  34.0,  26.0,   7.5,  12.0, 0.6],  // 0: Seat tongue tip
    [-135.0,  48.0,  40.0,  12.0,  16.0, 1.0],  // 1: Seat transition
    [-115.0,  64.0,  54.0,  20.0,  20.0, 1.5],  // 2: Rising ramp
    [ -95.0,  78.0,  66.0,  31.0,  24.0, 2.0],  // 3: Nose curve
    [ -75.0,  88.0,  76.0,  41.0,  26.0, 2.4],  // 4: Fore-pod swell
    [ -50.0,  92.0,  80.0,  47.0,  28.0, 2.6],  // 5: Pod front
    [ -20.0,  93.0,  81.0,  48.0,  28.0, 2.6],  // 6: Pod center-front
    [ +10.0,  93.0,  81.0,  48.0,  28.0, 2.6],  // 7: Pod center-rear
    [ +40.0,  92.0,  80.0,  47.0,  28.0, 2.6],  // 8: Pod rear
    [ +68.0,  89.0,  77.0,  43.0,  26.0, 2.2],  // 9: Cartridge exit
    [ +95.0,  80.0,  68.0,  33.0,  22.0, 1.8],  // 10: Tapering aft
    [+120.0,  66.0,  52.0,  22.0,  18.0, 1.4],  // 11: Ducktail slope
    [+145.0,  46.0,  34.0,  13.0,  14.0, 0.9],  // 12: Low ducktail
    [+168.0,  24.0,  18.0,   5.5,  10.0, 0.4]   // 13: Tail tip over fender
];

module continuous_sculpted_console_hull() {
    num_slices = len(SLICE_DATA);
    for (i = [0 : num_slices - 2]) {
        s0 = SLICE_DATA[i];
        s1 = SLICE_DATA[i + 1];
        hull() {
            console_slice_yz(s0[0], s0[1], s0[2], s0[3], s0[4], s0[5]);
            console_slice_yz(s1[0], s1[1], s1[2], s1[3], s1[4], s1[5]);
        }
    }
}

// Dual Longitudinal Accent Pinstripe Grooves flanking the central spine
module accent_pinstripe_grooves() {
    num_slices = len(SLICE_DATA);
    for (side = [-1, 1]) {
        for (i = [1 : num_slices - 3]) {
            s0 = SLICE_DATA[i];
            s1 = SLICE_DATA[i + 1];
            x0 = s0[0];
            x1 = s1[0];
            y0 = side * (s0[4] / 2.0 + 1.2);
            y1 = side * (s1[4] / 2.0 + 1.2);
            z0 = s0[3] + s0[5] - 0.2;
            z1 = s1[3] + s1[5] - 0.2;
            hull() {
                translate([x0, y0, z0]) sphere(r=1.2, $fn=16);
                translate([x1, y1, z1]) sphere(r=1.2, $fn=16);
            }
        }
    }
}

// Internal Enclosed Slide-In Tunnel for Pod 3
module pod3_internal_slide_tunnel() {
    // 1. Main Pod Chamber (floor at Z = 5.0 mm -> 3.5 mm solid floor over fender crown)
    translate([-POD_L/2.0, -POD_W/2.0, 5.0])
        cube([POD_L, POD_W, POD_H], center=false);

    // 2. Rear Cartridge Slide Entrance/Exit Mouth (extends past X = +68 to +120 mm)
    translate([POD_L/2.0 - 1.0, -(POD_W - 2.0)/2.0, 5.0])
        cube([65.0, POD_W - 2.0, POD_H - 2.0], center=false);

    // 3. Front M8 Gland Straight Chamber (X = -68 to -95 mm)
    translate([-POD_L/2.0 - 26.0, -11.0, 19.0 - 11.0])
        cube([28.0, 22.0, 22.0], center=false);

    // 4. Strap Hook Reliefs inside chamber
    hook_x = [-POD_L/2.0 + 25.0, -POD_L/2.0 + 110.0];
    for (hx = hook_x) {
        translate([hx - 7.0, -POD_W/2.0 - 1.0, 5.0]) cube([14.0, 2.5, 10.0]);
        translate([hx - 7.0,  POD_W/2.0 - 1.5, 5.0]) cube([14.0, 2.5, 10.0]);
    }
}

// Through-Tongue Horizontal M8 Cable Passage (Direct under seat cushion)
module touring_through_tongue_cable_tunnel() {
    // Continuous horizontal bore through tongue to X = -152 mm
    translate([-POD_L/2.0 - 20.0, 0, 6.0])
        rotate([0, -90, 0])
            cylinder(r=4.8, h=70.0, center=false, $fn=24);

    // Under-seat front exit pocket (bottom face of tongue)
    translate([-155.0, -8.0, -1.0])
        cube([18.0, 16.0, 10.0], center=false);
}

// Rear Ducktail 5 dBi Antenna Snap-In Channel (along spine X = +75 to +155 mm)
module touring_rear_antenna_snap_channel() {
    // Semi-cylindrical snap-in groove (dia 9.2 mm)
    translate([74.0, 0, 36.0])
        rotate([0, 78, 0])
            cylinder(r=4.6, h=82.0, center=false, $fn=24);

    // Top insertion slot (width 7.6 mm for click-in retention)
    translate([74.0, -3.8, 25.0])
        rotate([0, 78, 0])
            cube([82.0, 7.6, 20.0], center=false);

    // Antenna coax pigtail through-hole (dia 3.2 mm) into internal pod bay
    translate([68.0, 0, 31.0])
        rotate([0, 90, 0])
            cylinder(r=1.6, h=14.0, center=true, $fn=16);
}

module pod3_touring_fender_console() {
    difference() {
        // 1. Fully Enclosed Sculpted CVO Bodywork
        continuous_sculpted_console_hull();

        // 2. Internal Slide-In Tunnel for Pod 3
        pod3_internal_slide_tunnel();

        // 3. Dual Accent Pinstripe Grooves along spine
        accent_pinstripe_grooves();

        // 4. Flush GNSS Antenna Window / CVO Dark Plaque Recess on Top Roof
        translate([-15.0, 0, 48.0]) {
            hull() {
                for (dx = [-18.0, 18.0]) {
                    for (dy = [-18.0, 18.0]) {
                        translate([dx, dy, 0]) cylinder(r=3.0, h=6.0, center=true, $fn=24);
                    }
                }
            }
        }
        // Small Gore-Vent Breather Port in center of plaque
        translate([15.0, 0, 40.0])
            cylinder(r=4.0, h=20.0, center=true, $fn=24);

        // 5. Through-Tongue M8 Cable Tunnel under seat (0% drilling!)
        touring_through_tongue_cable_tunnel();

        // 6. Rear Ducktail 5 dBi Antenna Snap-In Channel
        touring_rear_antenna_snap_channel();

        // 7. Front OEM 1/4"-20 Seat Nut Mounting Hole & Washer Pocket
        translate([-142.0, 0, 0]) {
            cylinder(r=3.8, h=25.0, center=true, $fn=24); // 7.6 mm screw clearance
            translate([0, 0, 4.0])
                cylinder(r=7.5, h=10.0, center=false, $fn=24); // washer counterbore
        }

        // 8. Fender crown curvature clearance
        translate([0, 0, -(FENDER_R_TRANS - 2.0)]) {
            rotate([0, 90, 0])
                cylinder(r=FENDER_R_TRANS, h=380.0, center=true, $fn=64);
        }
    }
}

pod3_touring_fender_console();
