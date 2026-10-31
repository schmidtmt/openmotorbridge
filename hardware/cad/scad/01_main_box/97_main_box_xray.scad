// =============================================================================
// OpenMotorBridge - Central Main Box: Translucent 3D X-Ray Inspection Scene (v10.0)
// =============================================================================
// File: hardware/cad/scad/01_main_box/97_main_box_xray.scad
// Description: Translucent Ghosted X-Ray inspection assembly of the Central Box
//              (Gehäuse Typ A) showing the internal Mainboard PCBA 01 v10,
//              Slide-In Intermediate Tray, 1S LiPo Backup Battery, Taoglas Dual
//              Antennas, and front/rear interfaces inside the closed enclosure.
// =============================================================================

include <../00_common/parameters.scad>;
use <../00_common/dummies/dummy_main_pcb.scad>;
use <../00_common/dummies/dummy_lipo_battery.scad>;
use <00_lower_deck.scad>;
use <01_upper_deck.scad>;
use <02_colsure.scad>;
use <99_overall_box.scad>; // For dummy antenna modules

// Optional: Set to true if an external SMA bulkhead connector is mounted
has_sma_bulkhead = false;

module main_box_xray_inspection_assembly(has_sma_bulkhead = has_sma_bulkhead) {
    // 1. Lower Monocoque Tub (Translucent Slate Grey, 28% alpha)
    color([0.20, 0.35, 0.55, 0.28])
        translate([0, 0, 0])
            main_box_lower_case();

    // 2. Mainboard PCBA 01 v10 (Opaque components and PCB)
    translate([12.5, 9.5, 6.0])
        dummy_main_pcb();

    // 3. Slide-In Zwischenboden / Intermediate Tray (Translucent Blue-Grey, 32% alpha)
    color([0.30, 0.45, 0.65, 0.32])
        translate([0, 0, 0])
            main_box_mid_tray();

    // 4. 1S LiPo Backup Battery (Opaque blue pouch cell)
    translate([21.6, 9.0, 19.0])
        dummy_lipo_battery();

    // 4b. Taoglas Flex Antennas (Opaque green & gold)
    translate([12.8, 51.8, 19.0])
        dummy_fxp895_antenna();

    translate([30.8, 3.7, 19.0])
        dummy_fxp73_antenna();

    // 5. Top L-Slide Lid (Translucent Graphite Grey, 25% alpha)
    color([0.35, 0.45, 0.55, 0.25])
        translate([0, 0, 0])
            main_box_lid();

    // -------------------------------------------------------------------------
    // 6. Front Interface Hardware Fittings (at Y = 0)
    // -------------------------------------------------------------------------
    // A. Deutsch DTM-6 Flanged Receptacle (centered at X = 25.0, Z = 11.5 mm)
    color([0.18, 0.20, 0.22], 0.9) {
        translate([25.0, -3.5, 11.5])
            cube([18.0, 7.0, 11.0], center=true);
        for (dx = [-14.0, 14.0]) {
            translate([25.0 + dx, -1.0, 11.5])
                rotate([-90, 0, 0])
                    color("dimgray")
                        cylinder(r=2.8, h=2.5, center=true, $fn=24);
        }
    }

    // B. 16-Pin Periphery Flanged Receptacle (centered at X = 58.0, Z = 11.5 mm)
    color([0.18, 0.20, 0.22], 0.9) {
        translate([58.0, -3.5, 11.5])
            cube([21.0, 7.0, 11.0], center=true);
        for (dx = [-16.0, 16.0]) {
            translate([58.0 + dx, -1.0, 11.5])
                rotate([-90, 0, 0])
                    color("dimgray")
                        cylinder(r=2.8, h=2.5, center=true, $fn=24);
        }
    }

    // C. USB-C Waterproof Anodized Aluminium Service Cap (centered at X = 82.0, Z = 7.6 mm)
    color([0.15, 0.45, 0.75], 0.9)
        translate([82.0, -2.5, 7.6])
            rotate([90, 0, 0])
                cylinder(r=5.0, h=4.5, center=true, $fn=32);

    // D. SW1 Pair / Reset IP67 Silicone Button & Status LED Window (centered at X = 96.0, Z = 8.5 mm)
    color("black", 0.9)
        translate([96.0, -1.8, 8.5])
            rotate([90, 0, 0])
                cylinder(r=3.2, h=3.0, center=true, $fn=28);

    color("cyan", 0.95)
        translate([96.0, -2.8, 8.5])
            rotate([90, 0, 0])
                cylinder(r=1.2, h=1.0, center=true, $fn=20);

    // -------------------------------------------------------------------------
    // 7. Rear Interface Hardware Fittings (at Y = 74.0 mm)
    // -------------------------------------------------------------------------
    color([0.25, 0.28, 0.30], 0.9)
        translate([49.8, MAIN_BOX_OUTER_W + 1.2, 6.25])
            cube([14.5, 2.5, 4.0], center=true);

    if (has_sma_bulkhead) {
        color("gold") {
            translate([85.0, MAIN_BOX_OUTER_W + 4.0, 8.5])
                rotate([-90, 0, 0]) {
                    cylinder(r=3.15, h=8.0, center=true, $fn=32);
                    cylinder(r=4.5, h=2.5, center=true, $fn=6);
                }
        }
    }
}

// Render complete X-ray assembly
main_box_xray_inspection_assembly(has_sma_bulkhead);
