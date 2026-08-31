// =============================================================================
// OpenMotorBridge - Main Box: Translucent 3D X-Ray Inspection Scene
// =============================================================================
// File: hardware/cad/scad/01_main_box/97_main_box_xray.scad
// Description: Translucent Ghosted X-Ray inspection assembly of the Central Box
//              showing the internal Mainboard PCB, Backup Battery, and front
//              interface ports inside the closed, transparent enclosure.
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

    // 2. Mainboard PCB Assembly (Opaque Green PCB + Components)
    translate([7.5, 4.5, 6.0])
        dummy_main_pcb();

    // 3. Mid Tray Frame & Divider (Translucent Slate Grey, 35% alpha)
    color([0.25, 0.40, 0.60, 0.32])
        translate([0, 0, MAIN_BOX_LOWER_H])
            main_box_mid_tray();

    // 4. 1S LiPo Backup Battery (Opaque Silver Pouch)
    translate([MAIN_BOX_WALL + 28.0, MAIN_BOX_WALL + 17.5, MAIN_BOX_LOWER_H + 2.0])
        dummy_lipo_battery();

    // 5. Top Enclosure Lid (Translucent Graphite Grey, 28% alpha)
    color([0.3, 0.45, 0.65, 0.28])
        translate([0, 0, MAIN_BOX_LOWER_H + MAIN_BOX_MID_H])
            main_box_lid();

    // 6. Front Interface Fittings (HD26 Metal Flange & USB-C Aluminum Cap)
    // HD26 Metal Flange Body (centered at x=30.0, z=MAIN_BOX_LOWER_H + 10.0)
    color("silver", 0.95)
        translate([30.0, -1.0, MAIN_BOX_LOWER_H + 10.0])
            cube([39.0, 3.5, 9.5], center=true);

    // USB-C Metal Threaded Cap (centered at x=62.5, z=MAIN_BOX_LOWER_H + 9.75)
    color("silver", 0.95)
        translate([62.5, -2.5, MAIN_BOX_LOWER_H + 9.75])
            rotate([90, 0, 0])
                cylinder(r=4.5, h=5.0, center=true, $fn=24);

    // RGB LED PMMA Light Windows (3x Ø 2.5 mm at x=77.5, 82.5, 87.5)
    color("cyan", 0.8) {
        for (i = [0:2]) {
            translate([77.5 + i * 5.0, -0.5, MAIN_BOX_LOWER_H + 9.5])
                rotate([90, 0, 0])
                    cylinder(r=1.25, h=3.0, center=true, $fn=16);
        }
    }
}

// Render inspection assembly
main_box_xray_inspection_assembly();
