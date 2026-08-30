// =============================================================================
// OpenMotorBridge - Main Box: Translucent 3D X-Ray Inspection Scene
// =============================================================================
// File: hardware/cad/scad/01_main_box/97_main_box_xray.scad
// Description: Translucent Ghosted X-Ray inspection assembly of the Central Box
//              showing the internal Mainboard PCB, 4x Copper Studs, Backup Battery,
//              and front interface ports inside the closed, transparent enclosure.
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/dummies/dummy_main_pcb.scad>;
include <../00_common/dummies/dummy_lipo_battery.scad>;
include <00_lower_deck.scad>;
include <01_upper_deck.scad>;
include <02_colsure.scad>;

module main_box_xray_inspection_assembly() {
    // 1. Lower Case (Translucent Slate Grey, 30% alpha)
    color([0.2, 0.35, 0.55, 0.30])
        translate([0, 0, 0])
            main_box_lower_case();

    // 2. 4x Solid Copper Thermal Studs (Opaque Gold/Copper)
    color("darkgoldenrod", 1.0)
        main_box_copper_studs(h=4.0);

    // 3. Mainboard PCB Assembly (Opaque Green PCB + Components)
    translate([7.5, 4.5, 6.0])
        dummy_main_pcb();

    // 4. Mid Tray Frame & Divider (Translucent Slate Grey, 35% alpha)
    color([0.25, 0.40, 0.60, 0.32])
        translate([0, 0, MAIN_BOX_LOWER_H])
            main_box_mid_tray();

    // 5. 1S LiPo Backup Battery (Opaque Silver Pouch)
    translate([MAIN_BOX_WALL + 28.0, MAIN_BOX_WALL + 17.5, MAIN_BOX_LOWER_H + 2.0])
        dummy_lipo_battery();

    // 6. Top Enclosure Lid (Translucent Graphite Grey, 28% alpha)
    color([0.3, 0.45, 0.65, 0.28])
        translate([0, 0, MAIN_BOX_LOWER_H + MAIN_BOX_MID_H])
            main_box_lid();

    // 7. Front HD26 Flange & USB-C Ports
    color("silver", 0.95)
        translate([MAIN_BOX_WALL + 6.0 + 19.5, -2.0, MAIN_BOX_LOWER_H + 2.0 + 6.5])
            cube([39.0, 3.0, 13.0], center=true);

    color("silver", 0.95)
        translate([MAIN_BOX_WALL + 6.0 + 39.0 + 6.0 + 5.5, -3.0, MAIN_BOX_LOWER_H + 2.0 + 6.5])
            rotate([90, 0, 0])
                cylinder(r=5.5, h=4.0, center=true);

    color("cyan", 0.8)
        translate([MAIN_BOX_WALL + 6.0 + 39.0 + 6.0 + 11.0 + 6.0 + 2.0, -1.0, MAIN_BOX_LOWER_H + 2.0 + 6.5])
            rotate([90, 0, 0])
                cylinder(r=2.0, h=3.0, center=true);
}

// Render complete X-Ray assembly
main_box_xray_inspection_assembly();
