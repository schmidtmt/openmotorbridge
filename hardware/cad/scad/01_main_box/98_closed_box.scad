// =============================================================================
// OpenMotorBridge - Main Box: Fully Closed 3D Assembly Preview
// =============================================================================
// File: hardware/cad/scad/01_main_box/98_closed_box.scad
// Description: Fully assembled, sealed IP67 Central Box showing the Unterwanne
//              with 4x M4 mounting ears, Oberwanne with front interfaces (HD26,
//              USB-C, RGB LED), 4x M3 corner screws, and Top Lid with Gore vent.
// =============================================================================

include <../00_common/parameters.scad>;
include <00_lower_deck.scad>;
include <01_upper_deck.scad>;
include <02_colsure.scad>;

module main_box_closed_assembly() {
    // 1. Lower Case Tub (Unterwanne, Dark Slate Grey PA12)
    color("darkslategray", 0.95)
        translate([0, 0, 0])
            main_box_lower_case();

    // 2. Mid Tray / Upper Deck with Interfaces (Oberwanne, Slate Grey)
    color("slategray", 0.9)
        translate([0, 0, MAIN_BOX_LOWER_H])
            main_box_mid_tray();

    // 3. Top Enclosure Lid (Gehäusedeckel, Graphite Grey)
    color("dimgray", 0.85)
        translate([0, 0, MAIN_BOX_LOWER_H + MAIN_BOX_MID_H])
            main_box_lid();

    // 4. Front Interface Fittings (HD26 Metal Flange & USB-C Aluminum Cap)
    // HD26 Metal Flange Body (centered at x=30.0, z=MAIN_BOX_LOWER_H + 10.0)
    color("silver")
        translate([30.0, -1.0, MAIN_BOX_LOWER_H + 10.0])
            cube([39.0, 3.5, 9.5], center=true);

    // USB-C Metal Threaded Cap (centered at x=62.5, z=MAIN_BOX_LOWER_H + 9.75)
    color("silver")
        translate([62.5, -2.5, MAIN_BOX_LOWER_H + 9.75])
            rotate([90, 0, 0])
                cylinder(r=4.5, h=5.0, center=true, $fn=24);

    // RGB LED PMMA Light Windows (3x Ø 2.5 mm at x=77.5, 82.5, 87.5)
    color("cyan", 0.75) {
        for (i = [0:2]) {
            translate([77.5 + i * 5.0, -0.5, MAIN_BOX_LOWER_H + 9.5])
                rotate([90, 0, 0])
                    cylinder(r=1.25, h=3.0, center=true, $fn=16);
        }
    }

    // 5. 4x M3 Stainless Steel Corner Screws
    color("silver") {
        translate([MAIN_BOX_CORNER_POST/2, MAIN_BOX_CORNER_POST/2, MAIN_BOX_LOWER_H + MAIN_BOX_MID_H + MAIN_BOX_LID_H])
            cylinder(r=2.8, h=2.5, center=false);
        translate([MAIN_BOX_OUTER_L - MAIN_BOX_CORNER_POST/2, MAIN_BOX_CORNER_POST/2, MAIN_BOX_LOWER_H + MAIN_BOX_MID_H + MAIN_BOX_LID_H])
            cylinder(r=2.8, h=2.5, center=false);
        translate([MAIN_BOX_CORNER_POST/2, MAIN_BOX_OUTER_W - MAIN_BOX_CORNER_POST/2, MAIN_BOX_LOWER_H + MAIN_BOX_MID_H + MAIN_BOX_LID_H])
            cylinder(r=2.8, h=2.5, center=false);
        translate([MAIN_BOX_OUTER_L - MAIN_BOX_CORNER_POST/2, MAIN_BOX_OUTER_W - MAIN_BOX_CORNER_POST/2, MAIN_BOX_LOWER_H + MAIN_BOX_MID_H + MAIN_BOX_LID_H])
            cylinder(r=2.8, h=2.5, center=false);
    }
}

// Render closed assembly
main_box_closed_assembly();
