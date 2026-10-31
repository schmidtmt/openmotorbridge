// =============================================================================
// OpenMotorBridge - Central Main Box: Full v10.0 Assembly & Inspection
// =============================================================================
// File: hardware/cad/scad/01_main_box/99_overall_box.scad
// Description: Full 3D assembly of the v10.0 Dual-Rail Monocoque Central Box
//              (Gehäuse Typ A: 110 x 74 x 38 mm) with PCBA 01 v10 (ESP32-S31,
//              QCC3084, SX1262 LoRa), Slide-In Intermediate Tray, 1S LiPo
//              Backup Battery, Taoglas Dual Antennas, and L-Slide Lid.
//
// View Modes:
// - EXPLODED_VIEW = true:  Vertical 5-tier exploded stack for layer inspection
// - EXPLODED_VIEW = false: Assembled closed state for fit & clearance validation
// =============================================================================

include <../00_common/parameters.scad>;
use <../00_common/dummies/dummy_main_pcb.scad>;
use <../00_common/dummies/dummy_lipo_battery.scad>;
use <00_lower_deck.scad>;
use <01_upper_deck.scad>;
use <02_colsure.scad>;

// View Mode: Toggle true for exploded stack, false for assembled state
EXPLODED_VIEW = true;

// Vertical offsets for distinct 5-tier exploded layers
Z_LOWER_TUB   = 0.0;
Z_MAIN_PCB    = EXPLODED_VIEW ? 32.0 : 6.0;
Z_SLIDE_TRAY  = EXPLODED_VIEW ? 68.0 : 0.0;
Z_LIPO_CELL   = EXPLODED_VIEW ? 96.0 : 19.0;
Z_SLIDE_LID   = EXPLODED_VIEW ? 130.0 : 0.0;

// Module for Taoglas FXP895 LoRa 868 MHz Flex Antenna Dummy
module dummy_fxp895_antenna() {
    color([0.20, 0.45, 0.25]) // Dark green solder mask
        cube([85.0, 18.0, 0.8], center=false);
    color("gold") // Exposed radiating copper trace
        translate([3.0, 2.0, 0.8])
            cube([79.0, 14.0, 0.05], center=false);
    color("black") // U.FL miniature coaxial cable
        translate([82.0, 9.0, 0.8])
            rotate([0, 0, 90])
                cylinder(r=0.6, h=25.0, $fn=16);
}

// Module for Taoglas FXP73 2.4 GHz Wi-Fi / BLE Flex Antenna Dummy
module dummy_fxp73_antenna() {
    color([0.15, 0.35, 0.20]) // Dark green flex substrate
        cube([47.0, 7.0, 0.5], center=false);
    color("gold") // Exposed dipole copper pattern
        translate([2.0, 1.0, 0.5])
            cube([43.0, 5.0, 0.05], center=false);
    color("black") // U.FL coax
        translate([45.0, 3.5, 0.5])
            rotate([0, 0, 90])
                cylinder(r=0.6, h=20.0, $fn=16);
}

module main_box_full_assembly(exploded = EXPLODED_VIEW) {
    // -------------------------------------------------------------------------
    // Layer 1: Monolithic PA12 Monocoque Tub (Unterwanne, Dark Anthracite)
    // -------------------------------------------------------------------------
    color([0.16, 0.18, 0.20], 0.95)
        translate([0, 0, Z_LOWER_TUB])
            main_box_lower_case();

    // -------------------------------------------------------------------------
    // Layer 2: Mainboard PCBA 01 v10 (85 x 55 mm, ESP32-S31, QCC3084, SX1262)
    // -------------------------------------------------------------------------
    translate([12.5, 9.5, Z_MAIN_PCB])
        dummy_main_pcb();

    // -------------------------------------------------------------------------
    // Layer 3: Slide-In Zwischenboden / Intermediate Tray (PA12 Slate Grey)
    // -------------------------------------------------------------------------
    color([0.30, 0.34, 0.38], 0.90)
        translate([0, 0, Z_SLIDE_TRAY])
            main_box_mid_tray();

    // -------------------------------------------------------------------------
    // Layer 4: 1S LiPo Backup Battery & Taoglas Flex Antennas
    // -------------------------------------------------------------------------
    // A. 1S LiPo 2200 mAh Flat Cell (seated in tray cradle)
    translate([21.6, 9.0, Z_LIPO_CELL])
        dummy_lipo_battery();

    // B. Taoglas FXP895 LoRa 868 MHz Flex Antenna (seated in rear tray nest)
    translate([12.8, 51.8, Z_LIPO_CELL])
        dummy_fxp895_antenna();

    // C. Taoglas FXP73 2.4 GHz Wi-Fi/BLE Flex Antenna (seated in front tray nest)
    translate([30.8, 3.7, Z_LIPO_CELL])
        dummy_fxp73_antenna();

    // -------------------------------------------------------------------------
    // Layer 5: L-Slide Lid with Gore Vent & Deadbolt Heckwand (PA12 Graphite Grey)
    // -------------------------------------------------------------------------
    color([0.24, 0.26, 0.28], 0.88)
        translate([0, 0, Z_SLIDE_LID])
            main_box_lid();
}

// Render complete assembly
main_box_full_assembly(EXPLODED_VIEW);
