// =============================================================================
// OpenMotorBridge - Dashboard Wedge Dock for Central Control Box
// =============================================================================
// File: hardware/cad/scad/05_accessories/car_dashboard_wedge_dock.scad
// Description: Vibration-damped automotive dashboard dock for the Central Box:
//              1. Ergonomic 15° forward tilt angle for optimal status LED visibility
//                 and easy cable routing on car dashboards or center consoles.
//              2. Form-fit docking pocket for Central Box (110 x 74 mm).
//              3. 4x non-slip silicone bumper recesses (Ø 12 x 1.5 mm) or 3M VHB base.
//              4. Dual lateral finger release notches for 1-second insertion & removal.
//              5. Rear cable passthrough for 12V cigarette lighter PD adapter & HD26 whip.
// =============================================================================

include <../00_common/parameters.scad>;

// --- Parametric Wedge Dock Dimensions ---
DOCK_TILT_ANGLE      = 15.0; // Ergonomic viewing & cable angle (degrees)
DOCK_WALL            = 3.2;  // Wall thickness (mm)
DOCK_BASE_L          = MAIN_BOX_OUTER_L + 16.0; // 126.0 mm in X
DOCK_BASE_W          = MAIN_BOX_OUTER_W + 14.0; // 88.0 mm in Y
DOCK_FRONT_H         = 10.0; // Front lip height above dashboard (mm)
DOCK_POCKET_DEPTH    = 18.0; // Insertion pocket depth (mm)

module car_dashboard_wedge_dock() {
    difference() {
        // --- 1. SOLID WEDGE BODY ---
        hull() {
            // Flat base footprint on dashboard
            translate([-DOCK_BASE_L/2.0, -DOCK_BASE_W/2.0, 0])
                cube([DOCK_BASE_L, DOCK_BASE_W, 2.0], center=false);

            // Tilted upper rim
            rotate([0, -DOCK_TILT_ANGLE, 0]) {
                translate([-DOCK_BASE_L/2.0, -DOCK_BASE_W/2.0, DOCK_POCKET_DEPTH])
                    cube([DOCK_BASE_L, DOCK_BASE_W, 2.0], center=false);
            }
        }

        // --- 2. TILTED CENTRAL BOX INSERTION POCKET ---
        rotate([0, -DOCK_TILT_ANGLE, 0]) {
            // Main Central Box cavity (111 x 75 mm clearance)
            translate([-(MAIN_BOX_OUTER_L + 1.2)/2.0, -(MAIN_BOX_OUTER_W + 1.2)/2.0, DOCK_POCKET_DEPTH - 15.0])
                cube([MAIN_BOX_OUTER_L + 1.2, MAIN_BOX_OUTER_W + 1.2, 35.0], center=false);

            // Front connector access & status LED viewing cut
            translate([-DOCK_BASE_L/2.0 - 5.0, -(MAIN_BOX_OUTER_W - 12.0)/2.0, DOCK_POCKET_DEPTH - 10.0])
                cube([15.0, MAIN_BOX_OUTER_W - 12.0, 30.0], center=false);

            // Rear cable passthrough (for HD26 harness whip & 12V car charger)
            translate([MAIN_BOX_OUTER_L/2.0 - 5.0, -22.0, DOCK_POCKET_DEPTH - 12.0])
                cube([25.0, 44.0, 30.0], center=false);

            // Lateral finger extraction notches (left & right)
            for (side = [-DOCK_BASE_W/2.0 - 2.0, DOCK_BASE_W/2.0 - 10.0]) {
                translate([-20.0, side, DOCK_POCKET_DEPTH - 8.0])
                    cube([40.0, 12.0, 25.0], center=false);
            }
        }

        // --- 3. BASELINE CUTOUT (Ensure perfectly flat bottom at Z = 0) ---
        translate([-DOCK_BASE_L, -DOCK_BASE_W, -20.0])
            cube([DOCK_BASE_L * 2.0, DOCK_BASE_W * 2.0, 20.0], center=false);

        // --- 4. UNDERSIDE RUBBER FEET RECESSES (4x Ø 12 mm x 1.5 mm deep) ---
        for (dx = [-DOCK_BASE_L/2.0 + 16.0, DOCK_BASE_L/2.0 - 16.0]) {
            for (dy = [-DOCK_BASE_W/2.0 + 14.0, DOCK_BASE_W/2.0 - 14.0]) {
                translate([dx, dy, -0.1])
                    cylinder(r=6.0, h=1.6, center=false, $fn=32);
            }
        }

        // --- 5. WEIGHT REDUCTION / INTERNAL PASSIVE COOLING VOIDS ---
        for (vx = [-25.0, 25.0]) {
            translate([vx, 0, -1.0])
                cylinder(r=14.0, h=12.0, center=false, $fn=36);
        }
    }
}

car_dashboard_wedge_dock();
