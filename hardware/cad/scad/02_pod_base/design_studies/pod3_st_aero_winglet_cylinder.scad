// =============================================================================
// OpenMotorBridge - Satellite Pod 3: King of the Baggers ST Performance Bridge (Typ D3)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/pod3_st_aero_winglet_nacelle.scad
// Description: High-performance aerodynamic aero-winglet bridge for Harley-Davidson
//              Road Glide ST (FLTRXST) and Street Glide ST with solo seat.
//              Key Architecture:
//              1. 100% UNCHANGED POD: Fits the universal Pod base housing
//                 (pod_base_housing.stl, 135 x 70 x 38 mm) with 0.5 mm sliding fit.
//              2. OPEN-TOP DOCK: Zero double-housing! Pod roof with Gore-Vent breather
//                 and GNSS patch antenna is 100% exposed directly to the sky.
//              3. AERO FRONT-WEDGE: Aerodynamic ramp (28° slope) eliminates the blunt
//                 70 x 38 mm frontal face and smoothly channels wind over the fuselage.
//              4. WINGLET BRIDGE TO SADDLEBAGS (260 mm span): Swept wings span
//                 laterally across the fender towards the saddlebags.
//              5. VERTICAL STRUT-MOUNTING LEGS: Outer wing tips dive vertically into the
//                 fender-saddlebag gap, anchoring via horizontal slots to the OEM
//                 fender strut bolts (5/16"-18 / 3/8"-16, 35 mm spacing). ZERO fender holes!
//              6. INTERNAL CONCEALED CABLE ROUTE: M8 cable from front pod neck routes
//                 through the left wing and dives down the left strut leg.
//              7. REAR DIFFUSER & ANTENNA INTEGRATION: Rear Kamm-tail diffuser with
//                 integrated dorsal snap-in retention clip for the rear-facing antenna.
//              8. 100% SINGLE MANIFOLD SOLID: Guaranteed watertight 3D printable mesh.
// =============================================================================

include <../00_common/parameters.scad>;
use <parts/007_pod_slide_dock_core.scad>;

FENDER_R_TRANS = 140.0; // Harley Touring transverse crown radius (mm)

// Dimensional Constants
ST_POD_L      = 136.0; // Dock bay length in X (centered at X=0)
ST_FUSE_W     = 78.0;  // Center fuselage width in Y (mm)
ST_DOCK_H     = 40.0;  // Center rim height in Z (mm)
HALF_WAIST_H  = 20.0;  // Half-height waist between front ramp and pod dock (Z = 20 mm)

// Wingspan and Leg Dimensions
WING_HALF_SPAN = 130.0; // Half span from centerline Y=0 to outer leg face (mm)
LEG_DROP_Z     = -32.0; // Downward reach of vertical strut legs (mm)
LEG_LEN_X      = 54.0;  // Leg length in X (mm)

// Longitudinal extents (mm):
// Extended front nose tip:  X = -148.0 (generous straight room for M8 gland & strain relief)
// Front wedge peak:         X = -90.0 (full height Z=40 mm)
// Pod dock front:           X = -68.0 (waist X in [-90, -68] at half-height Z=20 mm)
// Pod dock rear:            X = +68.0 (cradle X in [-68, +68] at full height Z=40 mm)
// Rear diffuser tip:        X = +145.0 (full-height Kamm-tail sloping down to Z=6 mm)
X_WEDGE_TIP   = -148.0;
X_WEDGE_PEAK  = -90.0;
X_POD_FRONT   = -68.0;
X_POD_REAR    = +68.0;
X_DIFF_TIP    = +145.0;

// Helper: 2D rounded rectangle extruded in Z
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

WING_THICK = 8.0;

// Continuous 100% seamless Rotationskörper wing (Rotationskörper-Schale)
// Carved mathematically from concentric cylindrical shells cut with the jet planform
module continuous_jet_wing(side=1) {
    R_out = 96.0;
    Y_c   = 46.0;
    Z_c   = -78.0;

    union() {
        // 1. Mathematically continuous cylindrical shell for the ENTIRE wing and strake
        mirror([0, side < 0 ? 1 : 0, 0]) {
            intersection() {
                difference() {
                    translate([0, Y_c, Z_c])
                        rotate([0, 90, 0])
                            cylinder(r=R_out, h=300.0, center=true, $fn=128);
                    translate([0, Y_c, Z_c])
                        rotate([0, 90, 0])
                            cylinder(r=R_out - WING_THICK, h=320.0, center=true, $fn=128);
                }

                // Pure 2D Planform cut through the shell
                translate([0, 0, -60.0])
                    linear_extrude(height=120.0, center=false, convexity=10)
                        polygon([
                            [-118.0, ST_FUSE_W/2.0 - 3.0],  // Forward strake root
                            [-34.0,  64.0],                 // The Knick
                            [-27.0,  WING_HALF_SPAN],       // Front of wingtip
                            [+27.0,  WING_HALF_SPAN],       // Rear of wingtip
                            [+24.0,  70.0],                 // Trailing edge mid
                            [+35.0,  ST_FUSE_W/2.0 - 3.0]   // Trailing edge root
                        ]);
            }
        }

        // 2. Solid vertical mounting ear at the wingtip (Z in [-32, -8])
        // Integrates seamlessly with the diving shell and solidly encases bolt slots
        translate([-LEG_LEN_X/2.0, side > 0 ? (WING_HALF_SPAN - 8.0) : -WING_HALF_SPAN, LEG_DROP_Z])
            cube([LEG_LEN_X, 8.0, 24.0], center=false);
    }
}

// Dorsal Shark Fin (Heckleitwerk) with integrated antenna channel
module dorsal_shark_fin() {
    difference() {
        // Sculpted aerodynamic dorsal stabilizer fin
        hull() {
            // Front base of fin right behind pod roof (X = 72 mm, Z = 38 mm)
            translate([72.0, 0, 38.0])
                rounded_slab(6.0, 8.0, 4.0, r=2.5);

            // Fin peak (X = 104 mm, Z = 56 mm: 16 mm proud of pod roof!)
            translate([104.0, 0, 56.0])
                rounded_slab(16.0, 4.0, 3.0, r=1.5);

            // Tapered trailing edge near diffuser tip
            translate([138.0, 0, 10.0])
                rounded_slab(10.0, 5.0, 4.0, r=2.0);

            // Diffuser root anchor
            translate([95.0, 0, 24.0])
                rounded_slab(40.0, 12.0, 12.0, r=4.0);
        }

        // Integrated Antenna Channel along the raked trailing spar of the fin
        translate([76.0, 0, 24.0]) {
            rotate([0, 72, 0])
                cylinder(r=4.6, h=72.0, center=false, $fn=24);
        }
        // Top insertion snap slot
        translate([74.0, -3.5, 16.0])
            cube([70.0, 7.0, 25.0], center=false);
    }
}

module pod3_st_aero_winglet_nacelle() {
    difference() {
        union() {
            // 1. Pod Cradle (The "REST", Full Height Z = 40 mm, X in [-68, +68])
            hull() {
                translate([-ST_POD_L/2.0 + 1.0, 0, 0])
                    rounded_slab(2.0, ST_FUSE_W, ST_DOCK_H, r=7.0);
                translate([ST_POD_L/2.0 - 1.0, 0, 0])
                    rounded_slab(2.0, ST_FUSE_W, ST_DOCK_H, r=7.0);
            }

            // 2. Extended Front Ramp (The "SCHRÄGE", Full Height Z = 40 mm, X in [-148, -90])
            hull() {
                translate([X_WEDGE_PEAK, 0, 0])
                    rounded_slab(4.0, ST_FUSE_W, ST_DOCK_H, r=7.0);
                translate([X_WEDGE_PEAK - 28.0, 0, 0])
                    rounded_slab(4.0, 58.0, 20.0, r=6.0);
                translate([X_WEDGE_TIP + 6.0, 0, 0])
                    rounded_slab(12.0, 36.0, 5.0, r=5.0);
            }

            // 3. Intermediate Waist (The "ETWAS_FREI" -> HALBHOCH, Z = 20 mm, X in [-90, -68])
            hull() {
                translate([X_WEDGE_PEAK, 0, 0])
                    rounded_slab(4.0, ST_FUSE_W, 20.0, r=7.0);
                translate([X_POD_FRONT, 0, 0])
                    rounded_slab(4.0, ST_FUSE_W, 20.0, r=7.0);
            }

            // 4. FULL-HEIGHT Rear Kamm-Tail Diffuser (X in [+68, +145])
            hull() {
                translate([X_POD_REAR - 1.0, 0, 0])
                    rounded_slab(2.0, ST_FUSE_W, ST_DOCK_H, r=7.0);
                translate([X_POD_REAR + 38.0, 0, 0])
                    rounded_slab(2.0, 56.0, 18.0, r=7.0);
                translate([X_DIFF_TIP - 6.0, 0, 0])
                    rounded_slab(12.0, 38.0, 6.0, r=5.0);
            }

            // 5. Dorsal Shark Fin (Heckleitwerk mit integrierter Antenne)
            dorsal_shark_fin();

            // 6. Extreme Swooping Wings (Left & Right - Wingtip IS the Mounting Flange!)
            for (side = [-1, 1]) {
                continuous_jet_wing(side);
            }
        }

        // =====================================================================
        // SUBTRACTIONS
        // =====================================================================

        // A. Open-Top Slide-In Pod Dock Cavity (centered at X=0, Y=0, Z=2.5 mm floor)
        translate([0, 0, 2.5]) {
            pod_slide_dock_subtraction(
                dock_l = ST_POD_L,
                dock_w = 70.8,
                dock_h = 38.2,
                open_sky_h = 50.0
            );
        }

        // B. Continuous Concave Underside Cable Channel (Left Wing, +Y)
        // Follows the concave underbody of the wing into the inner face of the mounting flange
        hull() {
            translate([X_POD_FRONT - 2.0, 0, 16.0]) sphere(r=3.0, $fn=16);
            translate([-82.0, 20.0, 15.0]) sphere(r=3.0, $fn=16);
        }
        hull() {
            translate([-82.0, 20.0, 15.0]) sphere(r=3.0, $fn=16);
            translate([-34.0, 64.0, 10.0]) sphere(r=3.0, $fn=16);
        }
        hull() {
            translate([-34.0, 64.0, 10.0]) sphere(r=3.0, $fn=16);
            translate([-14.0, 98.0, -4.0]) sphere(r=3.0, $fn=16);
        }
        hull() {
            translate([-14.0, 98.0, -4.0]) sphere(r=3.0, $fn=16);
            translate([-8.0, 122.0, -16.0]) sphere(r=3.0, $fn=16);
        }
        // Vertical slot on inner face of wingtip mounting flange
        translate([-8.0, 122.0, -24.0])
            cube([5.6, 6.0, 22.0], center=true);

        // C. Strut Mounting Bolt Slots in the Sculpted Wingtips
        for (x_bolt = [-17.5, +17.5]) {
            // Right Wingtip
            translate([x_bolt, -WING_HALF_SPAN - 2.0, LEG_DROP_Z + 14.0])
                rotate([-90, 0, 0]) cylinder(r=4.6, h=14.0, center=false, $fn=32);
            translate([x_bolt - 4.6, -WING_HALF_SPAN - 2.0, LEG_DROP_Z + 11.0])
                cube([9.2, 14.0, 6.0], center=false);

            // Left Wingtip
            translate([x_bolt, WING_HALF_SPAN - 14.0, LEG_DROP_Z + 14.0])
                rotate([-90, 0, 0]) cylinder(r=4.6, h=16.0, center=false, $fn=32);
            translate([x_bolt - 4.6, WING_HALF_SPAN - 14.0, LEG_DROP_Z + 11.0])
                cube([9.2, 16.0, 6.0], center=false);
        }

        // D. Compound Concave Cylindrical Fender Clearance Underside (R=140 mm transverse)
        translate([0, 0, -(FENDER_R_TRANS - 2.0)]) {
            rotate([0, 90, 0])
                cylinder(r=FENDER_R_TRANS, h=abs(X_WEDGE_TIP) + X_DIFF_TIP + 20.0, center=true, $fn=80);
        }
    }
}

// Standalone compilation / preview
pod3_st_aero_winglet_nacelle();
