// =============================================================================
// OpenMotorBridge - Central Main Box: Fully Closed 3D Assembly Preview (v10.0)
// =============================================================================
// File: hardware/cad/scad/01_main_box/98_closed_box.scad
// Description: Fully assembled, sealed IP67/IP69K Central Box (Gehäuse Typ A)
//              showing the monolithic Monocoque Tub with 4x M4 mounting ears,
//              modern front automotive interfaces (Deutsch DTM-6, 16-Pin Periphery,
//              USB-C waterproof service cap, SW1 pairing button), rear lower sill
//              with MicroSD service window and optional SMA bulkhead, and the
//              L-Slide Lid with Gore ePTFE pressure compensation vent.
// =============================================================================

include <../00_common/parameters.scad>;
use <../00_common/dummies/dummy_main_pcb.scad>;
use <../00_common/dummies/dummy_lipo_battery.scad>;
use <00_lower_deck.scad>;
use <01_upper_deck.scad>;
use <02_colsure.scad>;

// Optional: Set to true if an external SMA bulkhead connector is mounted
has_sma_bulkhead = false;

module main_box_closed_assembly(has_sma_bulkhead = has_sma_bulkhead) {
    // 1. Lower Monocoque Tub (Unterwanne, Dark Anthracite MJF PA12)
    color([0.16, 0.18, 0.20])
        translate([0, 0, 0])
            main_box_lower_case();

    // 2. Internal Mainboard PCBA 01 v10 (Mounted on 3.5 mm Standoffs)
    translate([12.5, 9.5, 6.0])
        dummy_main_pcb();

    // 3. Slide-In Zwischenboden / Intermediate Tray (PA12 Slate Grey)
    color([0.28, 0.32, 0.36])
        translate([0, 0, 0])
            main_box_mid_tray();

    // 4. 1S LiPo Backup Battery (Seated inside battery cradle)
    translate([21.6, 9.0, 19.0])
        dummy_lipo_battery();

    // 5. Top L-Slide Lid with Rear Heckwand & Gore Vent (MJF PA12 Graphite Grey)
    color([0.24, 0.26, 0.28])
        translate([0, 0, 0])
            main_box_lid();

    // -------------------------------------------------------------------------
    // 6. Front Interface Hardware Fittings (at Y = 0)
    // -------------------------------------------------------------------------
    // A. Deutsch DTM 6-Pin Automotive Flanged Receptacle (centered at X = 25.0, Z = 11.5 mm)
    color([0.18, 0.20, 0.22]) {
        translate([25.0, -3.5, 11.5])
            cube([18.0, 7.0, 11.0], center=true);
        // 2x M3 Flange Screws (Black Zinc)
        for (dx = [-14.0, 14.0]) {
            translate([25.0 + dx, -1.0, 11.5])
                rotate([-90, 0, 0])
                    color("dimgray")
                        cylinder(r=2.8, h=2.5, center=true, $fn=24);
        }
    }

    // B. Cable 2 Periphery Bus 16-Pin Flanged Receptacle (centered at X = 58.0, Z = 11.5 mm)
    color([0.18, 0.20, 0.22]) {
        translate([58.0, -3.5, 11.5])
            cube([21.0, 7.0, 11.0], center=true);
        // 2x M3 Flange Screws (Black Zinc)
        for (dx = [-16.0, 16.0]) {
            translate([58.0 + dx, -1.0, 11.5])
                rotate([-90, 0, 0])
                    color("dimgray")
                        cylinder(r=2.8, h=2.5, center=true, $fn=24);
        }
    }

    // C. USB-C Waterproof Anodized Aluminium Service Cap (centered at X = 82.0, Z = 7.6 mm)
    color([0.15, 0.45, 0.75])
        translate([82.0, -2.5, 7.6])
            rotate([90, 0, 0])
                cylinder(r=5.0, h=4.5, center=true, $fn=32);

    // D. SW1 Pair / Reset IP67 Silicone Button & Status LED Window (centered at X = 96.0, Z = 8.5 mm)
    color("black")
        translate([96.0, -1.8, 8.5])
            rotate([90, 0, 0])
                cylinder(r=3.2, h=3.0, center=true, $fn=28);

    color("cyan", 0.9)
        translate([96.0, -2.8, 8.5])
            rotate([90, 0, 0])
                cylinder(r=1.2, h=1.0, center=true, $fn=20);

    // -------------------------------------------------------------------------
    // 7. Rear Interface Hardware Fittings (at Y = 74.0 mm)
    // -------------------------------------------------------------------------
    // A. MicroSD Waterproof Silicone Service Cap (centered at X = 49.8, Z = 6.2 mm)
    color([0.25, 0.28, 0.30])
        translate([49.8, MAIN_BOX_OUTER_W + 1.2, 6.25])
            cube([14.5, 2.5, 4.0], center=true);

    // B. Optional Rear SMA Antenna Port Bulkhead & Brass Nut (at X = 85.0, Z = 8.5 mm)
    if (has_sma_bulkhead) {
        color("gold") {
            translate([85.0, MAIN_BOX_OUTER_W + 4.0, 8.5])
                rotate([-90, 0, 0]) {
                    cylinder(r=3.15, h=8.0, center=true, $fn=32);
                    // Hex nut
                    cylinder(r=4.5, h=2.5, center=true, $fn=6);
                }
        }
    }
}

// Render complete closed box assembly
main_box_closed_assembly(has_sma_bulkhead);
