// =============================================================================
// OpenMotorBridge - Satellite Pod 3: Touring Stealth Console (Typ D2)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/pod3_touring_stealth_console.scad
// Description: Low-profile, OEM-integrated open-dock mounting console for
//              classic baggers and cruisers with 2-Up passenger seat.
//              Key Architecture:
//              1. 100% UNCHANGED POD: Fits the universal Pod base housing
//                 (pod_base_housing.stl, 135 x 70 x 38 mm) with 0.5 mm sliding fit.
//              2. OPEN-TOP DOCK: Zero double-housing! Pod roof with Gore-Vent breather
//                 and GNSS patch antenna is 100% exposed directly to the sky.
//              3. OEM PASSENGER SEAT MOUNTING: Front tongue anchors directly to the
//                 factory 1/4"-20 UNC fender nut behind the passenger seat.
//              4. SEAT-CONTOUR FRONT: Front hugs the curved tail of the passenger seat.
//              5. CONCEALED FORWARD CABLE ROUTING: M8 cable dives directly forward
//                 under the passenger seat into the bike's electrical harness.
//              6. REAR CARTRIDGE ACCESS & ANTENNA INTEGRATION: Cartridge slides in/out
//                 from the rear; smooth rear teardrop ducktail features a recessed
//                 aerodynamic snap-in clip channel for the rear-facing antenna.
//              7. FENDER PROTECTION: Compound concave saddle underside (R=140 mm
//                 transverse / R=320 mm longitudinal) with 1.5 mm EPDM pad recess.
// =============================================================================

include <../00_common/parameters.scad>;
use <parts/007_pod_slide_dock_core.scad>;

FENDER_R_TRANS = 140.0; // Harley Touring transverse crown radius (mm)
FENDER_R_LONG  = 320.0; // Harley Touring longitudinal wheel arch radius (mm)

// Dimensional Constants
TOURING_POD_L   = 136.0; // Dock bay length in X (centered at X=0)
TOURING_FUSE_W  = 78.0;  // Center fuselage width in Y (mm)
TOURING_SEAT_W  = 96.0;  // Front width hugging passenger seat in Y (mm)
TOURING_DOCK_H  = 40.0;  // Center rim height in Z (mm)
HALF_MOUTH_H    = 22.0;  // Front mouth connection height (half-height of pod)

// Longitudinal extents (mm):
// Front tip (1/4"-20 screw): X = -142.0
// Front pod mouth:           X = -68.0
// Rear pod mouth:            X = +68.0
// Rear teardrop tip:         X = +160.0
X_FRONT_TIP = -142.0;
X_POD_FRONT = -68.0;
X_POD_REAR  = +68.0;
X_REAR_TIP  = +160.0;

// Helper: 2D rounded rectangle extruded in Z for soft organic edges
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

module pod3_touring_stealth_console() {
    difference() {
        union() {
            // 1. Center Fuselage Cradle with soft rounded flanks (X in [-68, +68])
            hull() {
                translate([-TOURING_POD_L/2.0 + 1.0, 0, 0])
                    rounded_slab(2.0, TOURING_FUSE_W, TOURING_DOCK_H, r=7.0);
                translate([TOURING_POD_L/2.0 - 1.0, 0, 0])
                    rounded_slab(2.0, TOURING_FUSE_W, TOURING_DOCK_H, r=7.0);
            }

            // 2. Front Seat-Contoured Transition (The "SCHRÄGE", Full Height Z = 40.0 mm, X in [-142, -82])
            hull() {
                // Peak of front ramp (Full height Z = 40 mm)
                translate([-82.0, 0, 0])
                    rounded_slab(4.0, TOURING_FUSE_W, TOURING_DOCK_H, r=7.0);

                // Mid transition step hugging passenger seat tail
                translate([X_POD_FRONT - 32.0, 0, 0])
                    rounded_slab(4.0, TOURING_SEAT_W, 22.0, r=8.0);

                // Front 1/4"-20 mounting tongue tab
                translate([X_FRONT_TIP + 10.0, 0, 0])
                    rounded_slab(20.0, 48.0, 9.0, r=6.0);
            }

            // 3. Intermediate Waist (The "ETWAS_FREI" -> HALBHOCH, Z = 20.0 mm, X in [-82, -68])
            // Connects the full-height front ramp and full-height cradle at half height
            hull() {
                translate([-82.0, 0, 0])
                    rounded_slab(4.0, TOURING_FUSE_W, 20.0, r=7.0);
                translate([X_POD_FRONT, 0, 0])
                    rounded_slab(4.0, TOURING_FUSE_W, 20.0, r=7.0);
            }

            // 4. Rear Teardrop Ducktail at Kassetteneinschub (X in [+68, +160])
            // Connects HALF-HIGH (Z = 20.0 mm) at the rear cartridge mouth for tool-free finger access
            hull() {
                // Junction at rear pod mouth (half-height Z = 20 mm)
                translate([X_POD_REAR - 1.0, 0, 0])
                    rounded_slab(2.0, TOURING_FUSE_W, 20.0, r=7.0);

                // Mid slope
                translate([X_POD_REAR + 42.0, 0, 0])
                    rounded_slab(4.0, 56.0, 14.0, r=8.0);

                // Rear teardrop tip
                translate([X_REAR_TIP - 12.0, 0, 0])
                    rounded_slab(16.0, 26.0, 5.0, r=6.0);
            }

            // Rear flank blend: raises side walls from half-height rear mouth up to 40 mm
            hull() {
                translate([X_POD_REAR - 1.0, 0, 0])
                    rounded_slab(2.0, TOURING_FUSE_W, 20.0, r=7.0);
                translate([X_POD_REAR - 16.0, 0, 0])
                    rounded_slab(2.0, TOURING_FUSE_W, TOURING_DOCK_H, r=7.0);
            }
        }

        // =====================================================================
        // SUBTRACTIONS
        // =====================================================================

        // A. Open-Top Slide-In Pod Dock Cavity (centered at X=0, Y=0, Z=2.5 mm floor)
        translate([0, 0, 2.5]) {
            pod_slide_dock_subtraction(
                dock_l = TOURING_POD_L,
                dock_w = 70.8,
                dock_h = 38.2,
                open_sky_h = 50.0
            );
        }

        // B. Front 1/4"-20 Passenger Seat Screw Mounting Hole (at X = -130.0 mm)
        // Through-hole Ø 7.0 mm (clears 1/4" / 6.35 mm screw with tolerance)
        translate([X_FRONT_TIP + 12.0, 0, -5.0])
            cylinder(r=3.5, h=25.0, center=false, $fn=32);

        // Counterbore pocket for screw head & washer (Ø 15.0 mm, depth 5.0 mm)
        translate([X_FRONT_TIP + 12.0, 0, 4.2])
            cylinder(r=7.5, h=20.0, center=false, $fn=32);

        // C. Forward M8 Cable Tunnel (dives forward under seat into bike harness)
        // Bore running from M8 neck (X = -75) forward to front nose (X = -145)
        translate([X_FRONT_TIP - 2.0, 0, 6.0]) {
            rotate([0, 90, 0])
                cylinder(r=5.0, h=abs(X_FRONT_TIP - X_POD_FRONT) + 5.0, center=false, $fn=24);
        }

        // D. Rear-Facing Antenna Snap-in Retention Channel (along dorsal ridge of ducktail)
        // Semi-cylindrical groove (Ø 9.2 mm, length 72 mm) along X in [+78, +150] mm
        translate([X_POD_REAR + 10.0, 0, 17.5]) {
            rotate([0, 80, 0]) // Follows the gentle downward slope of the teardrop
                cylinder(r=4.6, h=72.0, center=false, $fn=24);
        }

        // Top slot for antenna snap insertion
        translate([X_POD_REAR + 8.0, -3.5, 9.5])
            cube([75.0, 7.0, 18.0], center=false);

        // E. Compound Concave Cylindrical Fender Saddle Underside (R=140 mm transverse)
        // Arch restricted to Z <= 4.0 mm, leaving solid 2.5 mm floor everywhere
        translate([0, 0, -(FENDER_R_TRANS - 2.0)]) {
            rotate([0, 90, 0])
                cylinder(r=FENDER_R_TRANS, h=abs(X_FRONT_TIP) + X_REAR_TIP + 20.0, center=true, $fn=80);
        }

        // F. Recessed Pocket for 1.5 mm EPDM Anti-Scratch Damping Pad
        translate([0, 0, -(FENDER_R_TRANS - 3.5)]) {
            rotate([0, 90, 0])
                cylinder(r=FENDER_R_TRANS, h=abs(X_FRONT_TIP) + X_REAR_TIP - 20.0, center=true, $fn=80);
        }
    }
}

// Standalone compilation / preview
pod3_touring_stealth_console();
