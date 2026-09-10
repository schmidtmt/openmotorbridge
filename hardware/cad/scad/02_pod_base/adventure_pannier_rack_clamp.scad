// =============================================================================
// OpenMotorBridge - Adventure Pannier Rack Clamp (Ø 18 mm Rohrträger-Klemmschelle)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/adventure_pannier_rack_clamp.scad
// Description: Heavy-duty Ø 18 mm stainless steel tube clamp attaching Pods 1 & 2
//              to the inside triangle of BMW GS Adventure / Touratech pannier racks.
//              Acts as an "Überrollkäfig" (roll-cage crash shield) providing
//              extreme impact and roost protection.
//              Features:
//              1. Precision semi-circular bore for Ø 18 mm round rack tubing.
//              2. Anti-slip friction ribs gripping EPDM protective tape.
//              3. Dual M5 clamping screw bosses with DIN 985 locknut pockets.
//              4. Rigid mounting interface bolting directly to Pod base housing.
// =============================================================================

include <../00_common/parameters.scad>;

// --- Parametric Dimensions ---
CLAMP_TUBE_DIA      = 18.2;  // Bore diameter for standard Ø 18 mm rack tube (mm)
CLAMP_TUBE_R        = CLAMP_TUBE_DIA / 2.0;
CLAMP_LENGTH_X      = 42.0;  // Clamp body length along tube axis (mm)
CLAMP_WIDTH_Y       = 48.0;  // Total width across clamping ears (mm)
CLAMP_HEIGHT_Z      = 15.0;  // Half-clamp block height (mm)
CLAMP_WALL          = 4.5;   // Heavy-duty structural wall (mm)

// Screw & Nut Specs
CLAMP_BOLT_SPACING  = 34.0;  // Distance between M5 clamping bolts in Y (mm)
CLAMP_BOLT_HOLE_R   = 2.7;   // M5 clearance hole (Ø 5.4 mm)
CLAMP_NUT_R         = 4.6;   // M5 hex nut socket across corners (mm)
CLAMP_NUT_DEPTH     = 4.8;   // Depth of hex stopnut cavity (mm)

module adventure_pannier_rack_clamp_base() {
    difference() {
        // Solid clamp block
        hull() {
            translate([-CLAMP_LENGTH_X/2.0, -CLAMP_WIDTH_Y/2.0, 0])
                cube([CLAMP_LENGTH_X, CLAMP_WIDTH_Y, CLAMP_HEIGHT_Z - 3.0]);
            translate([-CLAMP_LENGTH_X/2.0, -CLAMP_TUBE_R - 4.0, CLAMP_HEIGHT_Z])
                cube([CLAMP_LENGTH_X, 2*(CLAMP_TUBE_R + 4.0), 0.1]);
        }

        // Half-cylinder tube bore (Z = 0 parting line)
        translate([-CLAMP_LENGTH_X/2.0 - 1.0, 0, 0])
            rotate([0, 90, 0])
                cylinder(r=CLAMP_TUBE_R, h=CLAMP_LENGTH_X + 2.0);

        // Anti-slip internal ribs (0.5 mm grip ridges)
        for (rx = [-10.0, 0.0, 10.0]) {
            translate([rx, 0, 0])
                rotate([0, 90, 0])
                    difference() {
                        cylinder(r=CLAMP_TUBE_R + 0.6, h=1.5, center=true);
                        cylinder(r=CLAMP_TUBE_R, h=2.0, center=true);
                    }
        }

        // Dual M5 Clamping Bolt Bores
        for (y_pos = [-CLAMP_BOLT_SPACING/2.0, CLAMP_BOLT_SPACING/2.0]) {
            translate([0, y_pos, -1.0]) {
                cylinder(r=CLAMP_BOLT_HOLE_R, h=CLAMP_HEIGHT_Z + 2.0);
                // Counterbore for socket head cap screw DIN 912
                translate([0, 0, CLAMP_HEIGHT_Z - 5.0])
                    cylinder(r=5.0, h=7.0);
            }
        }

        // Pod Base Housing Interface Mounting Holes (M4 inserts on back face)
        for (x_pos = [-12.0, 12.0]) {
            translate([x_pos, 0, CLAMP_HEIGHT_Z - 6.0])
                cylinder(r=2.1, h=8.0); // M4 brass heat-set insert pocket
        }
    }
}

module adventure_pannier_rack_clamp_cap() {
    // Upper clamping counter-bracket
    difference() {
        translate([-CLAMP_LENGTH_X/2.0, -CLAMP_WIDTH_Y/2.0, 0])
            cube([CLAMP_LENGTH_X, CLAMP_WIDTH_Y, CLAMP_HEIGHT_Z - 4.0]);

        // Half-cylinder tube bore
        translate([-CLAMP_LENGTH_X/2.0 - 1.0, 0, CLAMP_HEIGHT_Z - 4.0])
            rotate([0, 90, 0])
                cylinder(r=CLAMP_TUBE_R, h=CLAMP_LENGTH_X + 2.0);

        // Dual M5 Clamping Bolt Bores with Nut Pockets
        for (y_pos = [-CLAMP_BOLT_SPACING/2.0, CLAMP_BOLT_SPACING/2.0]) {
            translate([0, y_pos, -1.0]) {
                cylinder(r=CLAMP_BOLT_HOLE_R, h=CLAMP_HEIGHT_Z + 2.0);
                // Hexagonal nut retention cavity
                translate([0, 0, 1.0])
                    cylinder(r=CLAMP_NUT_R, h=CLAMP_NUT_DEPTH, $fn=6);
            }
        }
    }
}

part = "base"; // "base", "cap", "assembly"

// Master assembly view (both halves clamped)
module adventure_pannier_rack_clamp() {
    adventure_pannier_rack_clamp_base();
    translate([0, 0, -2.0])
        rotate([180, 0, 0])
            adventure_pannier_rack_clamp_cap();
}

// Standalone render dispatch
if (part == "cap") {
    adventure_pannier_rack_clamp_cap();
} else if (part == "assembly") {
    adventure_pannier_rack_clamp();
} else {
    adventure_pannier_rack_clamp_base();
}
