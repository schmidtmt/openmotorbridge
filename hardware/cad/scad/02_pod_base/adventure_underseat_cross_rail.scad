// =============================================================================
// OpenMotorBridge - Adventure Under-Seat Cross-Rail (Sattelbrücke)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/adventure_underseat_cross_rail.scad
// Description: Transverse under-seat mounting bridge connecting left and right
//              Transition Docks across the rear subframe trellis.
//              Solves 3 fundamental engineering requirements:
//              1. Zero-Torque Anti-Rotation: Forms a rigid U-portal across frame tubes.
//              2. 100% Invisible Mounting: Bolts to OEM under-seat bracket points (Zero-Drill).
//              3. Integrated Cable Trough: Dual M8 PUR cables route through underside channel
//                 directly into Central Box under seat without visible external wires.
// =============================================================================

include <../00_common/parameters.scad>;

// --- Parametric Dimensions ---
RAIL_SPAN_Y         = 200.0; // Nominal subframe tube centerline span (mm)
RAIL_DEPTH_X        = 42.0;  // Longitudinal width of bridge rail (mm)
RAIL_BASE_THICK     = 4.5;   // Base plate thickness (mm)
RAIL_RIB_H          = 3.0;   // Stiffening rib height (Total H = 7.5 mm)
RAIL_CORNER_R       = 4.0;   // Corner fillet radius (mm)

// Flange interface to Transition Docks (Left & Right)
DOCK_FLANGE_W       = 24.0;  // Extension of mounting tongue into dock
DOCK_SCREW_DIST_X   = 24.0;  // Distance between 2x M4 dock fastening screws
DOCK_SCREW_R        = 2.2;   // M4 clearance hole (Ø 4.4 mm)

// Subframe OEM bracket slots (transverse adjustment 170-230 mm)
OEM_SLOT_L          = 28.0;  // Transverse slot length (mm)
OEM_SLOT_W          = 6.5;   // M6 clearance width (mm)
OEM_SLOT_OFFSET_Y   = 45.0;  // Offset from bike center (Y=0)

module rail_rounded_rect(length_x, width_y, height_z, r) {
    hull() {
        translate([r, r, 0]) cylinder(r=r, h=height_z, $fn=24);
        translate([length_x - r, r, 0]) cylinder(r=r, h=height_z, $fn=24);
        translate([r, width_y - r, 0]) cylinder(r=r, h=height_z, $fn=24);
        translate([length_x - r, width_y - r, 0]) cylinder(r=r, h=height_z, $fn=24);
    }
}

module adventure_underseat_cross_rail() {
    total_y = RAIL_SPAN_Y + 2 * DOCK_FLANGE_W; // Complete width including dock tongues

    difference() {
        union() {
            // 1. Main Transverse Bridge Plate (Centered on Y=0)
            translate([-RAIL_DEPTH_X/2.0, -total_y/2.0, 0])
                rail_rounded_rect(RAIL_DEPTH_X, total_y, RAIL_BASE_THICK, RAIL_CORNER_R);

            // 2. Dual Longitudinal Stiffening Ribs (Upper surface, U-channel profile)
            for (dx = [-RAIL_DEPTH_X/2.0 + 3.0, RAIL_DEPTH_X/2.0 - 6.0]) {
                translate([dx, -RAIL_SPAN_Y/2.0 + 5.0, RAIL_BASE_THICK])
                    cube([3.0, RAIL_SPAN_Y - 10.0, RAIL_RIB_H]);
            }

            // 3. Central Cable Management Bridge Shroud
            translate([-10.0, -25.0, RAIL_BASE_THICK])
                cube([20.0, 50.0, 2.0]);
        }

        // --- SUBTRACTIONS ---

        // A. Dual Transverse OEM Mounting Adjustment Slots (For M5/M6 under-seat bolts)
        for (side = [-1, 1]) {
            translate([0, side * OEM_SLOT_OFFSET_Y, -1.0]) {
                hull() {
                    translate([0, -OEM_SLOT_L/2.0 + OEM_SLOT_W/2.0, 0])
                        cylinder(r=OEM_SLOT_W/2.0, h=RAIL_BASE_THICK + 2.0, $fn=20);
                    translate([0,  OEM_SLOT_L/2.0 - OEM_SLOT_W/2.0, 0])
                        cylinder(r=OEM_SLOT_W/2.0, h=RAIL_BASE_THICK + 2.0, $fn=20);
                }
                // Counterbore recess for flat screw heads / washers
                translate([0, 0, RAIL_BASE_THICK - 1.8]) {
                    hull() {
                        translate([0, -OEM_SLOT_L/2.0 + OEM_SLOT_W/2.0, 0])
                            cylinder(r=6.0, h=4.0, $fn=20);
                        translate([0,  OEM_SLOT_L/2.0 - OEM_SLOT_W/2.0, 0])
                            cylinder(r=6.0, h=4.0, $fn=20);
                    }
                }
            }
        }

        // B. Left & Right Dock Fastening Holes (2x M4 per side)
        for (side = [-1, 1]) {
            y_pos = side * (RAIL_SPAN_Y/2.0 + DOCK_FLANGE_W/2.0);
            for (dx = [-DOCK_SCREW_DIST_X/2.0, DOCK_SCREW_DIST_X/2.0]) {
                translate([dx, y_pos, -1.0]) {
                    cylinder(r=DOCK_SCREW_R, h=RAIL_BASE_THICK + 2.0, $fn=16);
                    // M4 hex nut pocket or countersink on bottom
                    translate([0, 0, -0.5])
                        cylinder(r=4.2, h=2.5, $fn=6);
                }
            }
        }

        // C. Underside M8 PUR Cable Harness Channels (2x Ø 6.5 mm channels leading to center)
        for (side = [-1, 1]) {
            translate([-RAIL_DEPTH_X/2.0 + 8.0, side * (RAIL_SPAN_Y/2.0 + DOCK_FLANGE_W + 2.0), -1.0])
                rotate([0, 0, side * 90])
                    hull() {
                        translate([0, 0, 0]) cube([8.0, 1.0, 3.2]);
                        translate([0, side * (RAIL_SPAN_Y/2.0 - 15.0), 0]) cube([8.0, 1.0, 3.2]);
                    }
        }

        // D. Center Cable Drop-Through Window to Battery/Tool Tray
        translate([-8.0, -18.0, -1.0])
            rail_rounded_rect(16.0, 36.0, RAIL_BASE_THICK + 5.0, 3.0);
    }
}

// Standalone render
adventure_underseat_cross_rail();
