// =============================================================================
// OpenMotorBridge - Main Box: Translucent 3D X-Ray Inspection Scene
// =============================================================================
// File: hardware/cad/scad/01_main_box/97_main_box_xray.scad
// Description: Translucent Ghosted X-Ray inspection assembly of the Central Box
//              showing the internal Mainboard PCB (PCBA 01: 85x55 mm), Backup Battery,
//              and front interface ports inside the closed, transparent enclosure.
// =============================================================================

include <../00_common/parameters.scad>;
use <../00_common/dummies/dummy_main_pcb.scad>;
use <../00_common/dummies/dummy_lipo_battery.scad>;
use <00_lower_deck.scad>;
use <01_upper_deck.scad>;
use <02_colsure.scad>;

module main_box_xray_inspection_assembly() {
    // 1. Lower Case (Translucent Slate Grey, 30% alpha)
    color([0.2, 0.35, 0.55, 0.30])
        translate([0, 0, 0])
            main_box_lower_case();

    // 2. Mainboard PCB Assembly (PCBA 01: 85 x 55 mm, 77 x 47 mm mounting pitch)
    translate([12.5, 9.5, 6.0])
        dummy_main_pcb();

    // 3. Mid Tray Frame & Divider (Translucent Slate Grey, 32% alpha)
    color([0.25, 0.40, 0.60, 0.32])
        translate([0, 0, MAIN_BOX_LOWER_H])
            main_box_mid_tray();

    // 4. 1S LiPo Backup Battery (Opaque Silver Pouch)
    translate([MAIN_BOX_WALL + 18.5, MAIN_BOX_WALL + 14.5, MAIN_BOX_LOWER_H + 2.0])
        dummy_lipo_battery();

    // 5. Top Enclosure Lid (Translucent Graphite Grey, 28% alpha)
    color([0.3, 0.45, 0.65, 0.28])
        translate([0, 0, MAIN_BOX_LOWER_H + MAIN_BOX_MID_H])
            main_box_lid();

    // 6. Front Interface Hardware Fittings (Z center = MAIN_BOX_LOWER_H + 7.5 mm)
    z_intf = MAIN_BOX_LOWER_H + 7.5;

    // A. USB-C Waterproof Anodized Service Cap (at X = 24.0 mm)
    color([0.15, 0.45, 0.75], 0.9)
        translate([24.0, -2.5, z_intf])
            rotate([90, 0, 0])
                cylinder(r=5.5, h=5.0, center=true, $fn=32);

    // B. WS2812B RGB Status LED Diffuse PMMA Lens (at X = 42.0 mm)
    color("cyan", 0.9)
        translate([42.0, -1.0, z_intf])
            rotate([90, 0, 0])
                cylinder(r=1.6, h=3.0, center=true, $fn=20);

    // C. SW1 Pair / Reset IP67 Silicone Button (at X = 54.0 mm)
    color("black", 0.9)
        translate([54.0, -1.5, z_intf])
            rotate([90, 0, 0])
                cylinder(r=3.25, h=3.5, center=true, $fn=24);

    // D. Automotive Deutsch DTM-12 Flanged Receptacle (centered at X = 80.0 mm)
    color([0.18, 0.20, 0.22], 0.9)
        translate([80.0, -3.0, z_intf])
            cube([28.0, 6.0, 14.0], center=true);

    // 7. Rear SMA Antenna Bulkhead Port (Gold-plated, at X = 85.0 mm, Y = MAIN_BOX_OUTER_W)
    color("gold", 0.9)
        translate([85.0, MAIN_BOX_OUTER_W + 3.5, z_intf])
            rotate([-90, 0, 0])
                cylinder(r=3.2, h=7.0, center=true, $fn=24);
}

// Render inspection assembly
main_box_xray_inspection_assembly();
