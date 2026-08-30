// =============================================================================
// OpenMotorBridge - Main Box: Overall Assembly & Component Inspection
// =============================================================================
// File: hardware/cad/scad/01_main_box/99_overall_box.scad
// Description: Full 3D assembly of the 3-Tier Central Box sandwich with
//              inserted Mainboard PCB, LiPo Backup Battery, and Copper Studs.
//              Supports both exploded view and fully closed assembly preview.
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/dummies/dummy_main_pcb.scad>;
include <../00_common/dummies/dummy_lipo_battery.scad>;
include <00_lower_deck.scad>;
include <01_upper_deck.scad>;
include <02_colsure.scad>;

// View Mode: Set to true for exploded view, false for closed assembly
EXPLODED_VIEW = true;
EXPLODE_GAP   = EXPLODED_VIEW ? 25.0 : 0.0;

module main_box_full_assembly() {
    // 1. Lower Case (Unterwanne, Anthracite Grey)
    color("darkslategray", 0.9)
        translate([0, 0, 0])
            main_box_lower_case();

    // 2. Mainboard PCB Dummy (Green PCB + Components)
    translate([7.5, 4.5, 6.0])
        dummy_main_pcb();

    // 3. 4x Copper Thermal Studs
    main_box_copper_studs(h=4.0);

    // 4. Mid Tray (Oberwanne / Zwischenboden, Slate Grey)
    color("slategray", 0.85)
        translate([0, 0, MAIN_BOX_LOWER_H + EXPLODE_GAP])
            main_box_mid_tray();

    // 5. 1S LiPo Backup Battery Dummy (Sitting in cradle on partition floor)
    translate([MAIN_BOX_WALL + 28.0, MAIN_BOX_WALL + 17.5, MAIN_BOX_LOWER_H + EXPLODE_GAP + 2.0])
        dummy_lipo_battery();

    // 6. Lid Plate (Gehäusedeckel, Dark Gray)
    color("dimgray", 0.8)
        translate([0, 0, MAIN_BOX_LOWER_H + MAIN_BOX_MID_H + 2 * EXPLODE_GAP])
            main_box_lid();
}

// Render complete assembly
main_box_full_assembly();
