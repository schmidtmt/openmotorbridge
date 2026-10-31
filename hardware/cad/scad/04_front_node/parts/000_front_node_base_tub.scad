// =============================================================================
// OpenMotorBridge - Front Node: Monocoque Base Tub (v10.0 Slot-In)
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/000_front_node_base_tub.scad
// Description: Monolithic PA12-MJF monocoque enclosure tub for the Universal
//              Front Node (Gehäuse Typ E: 98 x 68 x 22 mm).
//              Implements the v10 Monocoque Slot-In architecture:
//              - 100% solid, leak-free bottom floor with 4-in-1 mounting system.
//              - Longitudinal C-profile guide rails (Z = 16.5 mm) along North & South.
//              - Solid PA12 retaining roof lips (Z = 17.9..19.5 mm) for form-fit hold-down.
//              - Front wedge-lock pocket (Keilanzug-Nut) at East wall (X = 98 mm).
//              - Rear insertion portal at West wall (X = 0 mm, Z = 6.0..19.5 mm).
// =============================================================================

include <../../00_common/parameters.scad>;

module front_node_base_tub(
    length   = FRONT_NODE_OUTER_L,
    width    = FRONT_NODE_OUTER_W,
    height   = FRONT_NODE_TUB_H,
    corner_r = FRONT_NODE_CORNER_R,
    wall     = FRONT_NODE_WALL
) {
    ch_x_start = wall + 3.5; // 6.0 mm
    ch_y_start = wall + 3.5; // 6.0 mm

    difference() {
        // 1. Solid Outer Block with Rounded Vertical Corners
        linear_extrude(height = height) {
            offset(r = corner_r) {
                offset(delta = -corner_r) {
                    square([length, width], center=false);
                }
            }
        }

        // 2. Hollow Internal Chamber (clears PCBA 05 and internal wiring)
        translate([ch_x_start, ch_y_start, wall]) {
            cube(size=[FRONT_NODE_CHAMBER_L, FRONT_NODE_CHAMBER_W, height - wall + 1.0], center=false);
        }

        // 3. Longitudinal C-Profile Guide Rails (Z = 16.5 mm)
        // A. South Guide Groove into South Wall (Y = 6.0 - 1.6 .. 6.0 mm)
        translate([ch_x_start - 1.0, ch_y_start - FRONT_NODE_RAIL_DEPTH, FRONT_NODE_RAIL_Z - FRONT_NODE_RAIL_H/2.0]) {
            cube([FRONT_NODE_CHAMBER_L + 2.0, FRONT_NODE_RAIL_DEPTH + 0.1, FRONT_NODE_RAIL_H], center=false);
        }

        // B. North Guide Groove into North Wall (Y = 62.0 .. 62.0 + 1.6 mm)
        translate([ch_x_start - 1.0, ch_y_start + FRONT_NODE_CHAMBER_W - 0.1, FRONT_NODE_RAIL_Z - FRONT_NODE_RAIL_H/2.0]) {
            cube([FRONT_NODE_CHAMBER_L + 2.0, FRONT_NODE_RAIL_DEPTH + 0.1, FRONT_NODE_RAIL_H], center=false);
        }

        // 4. Front Wedge-Lock Undercut Pocket (Keilanzug-Nut into East Wall at X = 92.0 mm)
        translate([ch_x_start + FRONT_NODE_CHAMBER_L - 0.1, ch_y_start + 1.0, FRONT_NODE_RAIL_Z - 0.5]) {
            cube([1.8, FRONT_NODE_CHAMBER_W - 2.0, FRONT_NODE_RAIL_H + 1.0], center=false);
        }

        // 5. Rear Insertion Portal Opening at West Wall (X = 0 mm, Z = 6.0..19.5 mm)
        translate([-0.5, ch_y_start, FRONT_NODE_REAR_SILL_H]) {
            cube([ch_x_start + 1.0, FRONT_NODE_CHAMBER_W, height - FRONT_NODE_REAR_SILL_H + 1.0], center=false);
        }

        // Throat expansion for C-rail lead-in at West portal
        translate([-0.5, ch_y_start - FRONT_NODE_RAIL_DEPTH, FRONT_NODE_RAIL_Z - FRONT_NODE_RAIL_H/2.0]) {
            cube([ch_x_start + 1.0, FRONT_NODE_CHAMBER_W + 2*FRONT_NODE_RAIL_DEPTH, height - FRONT_NODE_RAIL_Z + 1.0], center=false);
        }

        // 6. Dual Deadbolt Latch Sockets on Lower Sill (West, X = 2.0..5.0 mm, Z = 1.5..5.5 mm)
        translate([2.0, ch_y_start + 4.0, FRONT_NODE_REAR_SILL_H - 4.0]) {
            cube([3.5, 3.5, 4.5], center=false);
        }
        translate([2.0, ch_y_start + FRONT_NODE_CHAMBER_W - 7.5, FRONT_NODE_REAR_SILL_H - 4.0]) {
            cube([3.5, 3.5, 4.5], center=false);
        }
    }
}

// Standalone preview
front_node_base_tub();
