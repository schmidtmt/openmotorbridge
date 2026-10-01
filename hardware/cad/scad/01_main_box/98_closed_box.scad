// =============================================================================
// OpenMotorBridge - Main Box: Fully Closed 3D Assembly Preview
// =============================================================================
// File: hardware/cad/scad/01_main_box/98_closed_box.scad
// Description: Fully assembled, sealed IP67 Central Box showing the Unterwanne
//              with 4x M4 mounting ears, Oberwanne with modern front interfaces
//              (Deutsch DTM-12, USB-C, SW1, RGB LED), rear SMA antenna port,
//              4x M3 corner screws, and Top Lid with Gore breather vent.
// =============================================================================

include <../00_common/parameters.scad>;
use <00_lower_deck.scad>;
use <01_upper_deck.scad>;
use <02_colsure.scad>;

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

    // 4. Front Interface Hardware Fittings (Z center = MAIN_BOX_LOWER_H + 7.5 mm)
    z_intf = MAIN_BOX_LOWER_H + 7.5;

    // A. USB-C Waterproof Anodized Service Cap (at X = 24.0 mm)
    color([0.15, 0.45, 0.75])
        translate([24.0, -2.5, z_intf])
            rotate([90, 0, 0])
                cylinder(r=5.5, h=5.0, center=true, $fn=32);

    // B. WS2812B RGB Status LED Diffuse PMMA Lens (at X = 42.0 mm)
    color("cyan", 0.85)
        translate([42.0, -1.0, z_intf])
            rotate([90, 0, 0])
                cylinder(r=1.6, h=3.0, center=true, $fn=20);

    // C. SW1 Pair / Reset IP67 Silicone Button (at X = 54.0 mm)
    color("black")
        translate([54.0, -1.5, z_intf])
            rotate([90, 0, 0])
                cylinder(r=3.25, h=3.5, center=true, $fn=24);

    // D. Automotive Deutsch DTM-12 Flanged Receptacle (centered at X = 80.0 mm)
    color([0.18, 0.20, 0.22]) {
        translate([80.0, -3.0, z_intf])
            cube([28.0, 6.0, 14.0], center=true);
        // 2x M3 Flange screws
        for (dx = [-18.0, 18.0]) {
            translate([80.0 + dx, -4.5, z_intf])
                rotate([90, 0, 0])
                    cylinder(r=2.8, h=2.5, center=true, $fn=20);
        }
    }

    // 5. Rear SMA Antenna Bulkhead Port (Gold-plated, at X = 85.0 mm, Y = MAIN_BOX_OUTER_W)
    color("gold") {
        translate([85.0, MAIN_BOX_OUTER_W + 3.5, z_intf])
            rotate([-90, 0, 0]) {
                cylinder(r=3.2, h=7.0, center=true, $fn=24);
                // Hex nut
                cylinder(r=4.5, h=2.5, center=true, $fn=6);
            }
    }

    // 6. 4x M3 Stainless Steel Corner Screws
    color("silver") {
        corner_offset = MAIN_BOX_CORNER_POST / 2.0;
        z_top = MAIN_BOX_LOWER_H + MAIN_BOX_MID_H + MAIN_BOX_LID_H;
        for (pos = [
            [corner_offset, corner_offset],
            [MAIN_BOX_OUTER_L - corner_offset, corner_offset],
            [corner_offset, MAIN_BOX_OUTER_W - corner_offset],
            [MAIN_BOX_OUTER_L - corner_offset, MAIN_BOX_OUTER_W - corner_offset]
        ]) {
            translate([pos[0], pos[1], z_top - 1.0])
                cylinder(r=2.8, h=2.0, center=false, $fn=24);
        }
    }
}

// Render closed assembly
main_box_closed_assembly();
