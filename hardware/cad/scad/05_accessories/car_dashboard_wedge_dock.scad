// =============================================================================
// OpenMotorBridge - Dual-Stack Dashboard Wedge Dock (Central Box + Front Node)
// =============================================================================
// File: hardware/cad/scad/05_accessories/car_dashboard_wedge_dock.scad
// Description: Two-tier vibration-damped automotive dashboard dock for support cars:
//              1. Lower Chamber (Tier 1, horizontal base):
//                 Slide-in pocket for the Front Node (PCBA 05, 98 x 68 x 25 mm).
//                 Front aperture provides direct sky/windshield view for the SAM-M10Q
//                 GNSS and Knowles MEMS microphone, with side access for Dual USB-PD.
//              2. Upper Deck (Tier 2, 15° forward tilt):
//                 Form-fit pocket for Central Control Box (PCBA 01, 110 x 74 x 32 mm).
//                 Ergonomically tilted at 15° for glare-free visibility of status LEDs.
//              3. Internal Vertical Passthrough Duct:
//                 Concealed cable channel connecting lower Front Node J1 (JWPF 2-pin)
//                 and upper Central Box J1 (Deutsch DTM-12) to the 12V Y-adapter harness.
//              4. Dual lateral finger release notches for 1-second insertion & removal.
//              5. 4x underside recesses for anti-slip silicone feet (Ø 12 x 1.5 mm).
// =============================================================================

include <../00_common/parameters.scad>;

// --- Parametric Dual-Stack Dock Dimensions ---
DOCK_TILT_ANGLE      = 15.0; // Ergonomic viewing angle for top deck (degrees)
DOCK_WALL            = 3.2;  // Wall thickness (mm)
DOCK_BASE_L          = MAIN_BOX_OUTER_L + 18.0; // 128.0 mm in X
DOCK_BASE_W          = MAIN_BOX_OUTER_W + 16.0; // 90.0 mm in Y

// Lower Tier (Front Node Chamber)
LOWER_POCKET_L       = FRONT_NODE_OUTER_L + 2.0; // 100.0 mm
LOWER_POCKET_W       = FRONT_NODE_OUTER_W + 2.0; // 70.0 mm
LOWER_POCKET_H       = FRONT_NODE_OUTER_H + 1.5; // 26.5 mm
LOWER_FLOOR_Z        = 2.5;                      // Floor thickness (mm)

// Upper Tier (Central Box Deck)
UPPER_POCKET_L       = MAIN_BOX_OUTER_L + 1.5;   // 111.5 mm
UPPER_POCKET_W       = MAIN_BOX_OUTER_W + 1.5;   // 75.5 mm
UPPER_POCKET_DEPTH   = 18.0;                     // Depth of upper pocket (mm)
UPPER_DECK_Z         = LOWER_FLOOR_Z + LOWER_POCKET_H + 3.0; // 32.0 mm base height of upper wedge

module car_dashboard_wedge_dock() {
    difference() {
        // --- 1. SOLID MULTI-TIER WEDGE BODY ---
        hull() {
            // Flat base footprint on dashboard
            translate([-DOCK_BASE_L/2.0, -DOCK_BASE_W/2.0, 0])
                cube([DOCK_BASE_L, DOCK_BASE_W, 2.0], center=false);

            // Intermediate body height for lower tier
            translate([-DOCK_BASE_L/2.0, -DOCK_BASE_W/2.0, UPPER_DECK_Z - 4.0])
                cube([DOCK_BASE_L, DOCK_BASE_W, 2.0], center=false);

            // Tilted upper rim
            translate([0, 0, UPPER_DECK_Z]) {
                rotate([0, -DOCK_TILT_ANGLE, 0]) {
                    translate([-DOCK_BASE_L/2.0, -DOCK_BASE_W/2.0, UPPER_POCKET_DEPTH + 2.0])
                        cube([DOCK_BASE_L, DOCK_BASE_W, 2.0], center=false);
                }
            }
        }

        // --- 2. LOWER TIER: FRONT NODE CAVITY (PCBA 05) ---
        translate([-LOWER_POCKET_L/2.0, -LOWER_POCKET_W/2.0, LOWER_FLOOR_Z]) {
            cube([LOWER_POCKET_L, LOWER_POCKET_W, LOWER_POCKET_H], center=false);
        }

        // Front Node front opening (slide-in & acoustic/GNSS aperture towards windshield)
        translate([-DOCK_BASE_L/2.0 - 5.0, -(LOWER_POCKET_W - 12.0)/2.0, LOWER_FLOOR_Z]) {
            cube([15.0, LOWER_POCKET_W - 12.0, LOWER_POCKET_H + 2.0], center=false);
        }

        // Lateral access cutouts for Front Node USB-PD ports (left & right)
        for (side = [-DOCK_BASE_W/2.0 - 2.0, DOCK_BASE_W/2.0 - 10.0]) {
            translate([-25.0, side, LOWER_FLOOR_Z + 4.0])
                cube([50.0, 12.0, LOWER_POCKET_H - 6.0], center=false);
        }

        // --- 3. UPPER TIER: TILTED CENTRAL BOX INSERTION POCKET ---
        translate([0, 0, UPPER_DECK_Z]) {
            rotate([0, -DOCK_TILT_ANGLE, 0]) {
                // Main Central Box cavity
                translate([-UPPER_POCKET_L/2.0, -UPPER_POCKET_W/2.0, 0])
                    cube([UPPER_POCKET_L, UPPER_POCKET_W, 40.0], center=false);

                // Front status LED viewing window
                translate([-DOCK_BASE_L/2.0 - 5.0, -(MAIN_BOX_OUTER_W - 12.0)/2.0, 5.0])
                    cube([15.0, MAIN_BOX_OUTER_W - 12.0, 35.0], center=false);

                // Rear cable passthrough (for Deutsch DTM-12 harness & USB-C media cable)
                translate([MAIN_BOX_OUTER_L/2.0 - 5.0, -22.0, 4.0])
                    cube([25.0, 44.0, 35.0], center=false);

                // Lateral finger extraction notches (left & right)
                for (side = [-DOCK_BASE_W/2.0 - 2.0, DOCK_BASE_W/2.0 - 10.0]) {
                    translate([-20.0, side, 8.0])
                        cube([40.0, 12.0, 30.0], center=false);
                }
            }
        }

        // --- 4. INTERNAL VERTICAL PASSTHROUGH DUCT ---
        // Connects lower tier (Front Node J1 JWPF) and upper tier (Central Box J1 DTM-12)
        translate([MAIN_BOX_OUTER_L/2.0 - 20.0, -18.0, LOWER_FLOOR_Z + 5.0]) {
            cube([22.0, 36.0, UPPER_DECK_Z + 15.0], center=false);
        }

        // --- 5. BASELINE CUTOUT (Ensure perfectly flat bottom at Z = 0) ---
        translate([-DOCK_BASE_L, -DOCK_BASE_W, -20.0])
            cube([DOCK_BASE_L * 2.0, DOCK_BASE_W * 2.0, 20.0], center=false);

        // --- 6. UNDERSIDE RUBBER FEET RECESSES (4x Ø 12 mm x 1.5 mm deep) ---
        for (dx = [-DOCK_BASE_L/2.0 + 16.0, DOCK_BASE_L/2.0 - 16.0]) {
            for (dy = [-DOCK_BASE_W/2.0 + 14.0, DOCK_BASE_W/2.0 - 14.0]) {
                translate([dx, dy, -0.1])
                    cylinder(r=6.0, h=1.6, center=false, $fn=32);
            }
        }
    }
}

car_dashboard_wedge_dock();
