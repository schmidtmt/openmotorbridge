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

// Vertical offsets for distinct 6-tier exploded layers
Z_LOWER_CASE   = 0.0;
Z_COPPER_STUDS = EXPLODED_VIEW ? 18.0 : 0.0;
Z_MAIN_PCB     = EXPLODED_VIEW ? 38.0 : 6.0;
Z_MID_TRAY     = EXPLODED_VIEW ? 70.0 : MAIN_BOX_LOWER_H;
Z_LIPO_BATTERY = EXPLODED_VIEW ? 102.0 : (MAIN_BOX_LOWER_H + 2.0);
Z_TOP_LID      = EXPLODED_VIEW ? 132.0 : (MAIN_BOX_LOWER_H + MAIN_BOX_MID_H);

module main_box_full_assembly() {
    // Layer 1: Lower Case Tub (Unterwanne, Dark Anthracite PA12 with Mounting Ears)
    color("darkslategray", 0.92)
        translate([0, 0, Z_LOWER_CASE])
            main_box_lower_case();

    // Layer 2: 4x Solid Copper Thermal Studs (Floating into floor pockets)
    color("darkgoldenrod", 1.0)
        translate([0, 0, Z_COPPER_STUDS])
            main_box_copper_studs(h=8.0);

    // Layer 3: Mainboard PCB Assembly (Green FR4 + Gold Pads + Components)
    translate([7.5, 4.5, Z_MAIN_PCB])
        dummy_main_pcb();

    // Layer 4: Mid Tray Frame with Partition Floor (Oberwanne, Slate Grey with Front Cutouts)
    color("slategray", 0.88)
        translate([0, 0, Z_MID_TRAY])
            main_box_mid_tray();

    // Layer 5: 1S LiPo Backup Battery (Floating into battery compartment tray)
    translate([MAIN_BOX_WALL + 28.0, MAIN_BOX_WALL + 17.5, Z_LIPO_BATTERY])
        dummy_lipo_battery();

    // Layer 6: Enclosure Top Lid (Gehäusedeckel, Graphite Grey with Vent & Lightpipe)
    color("dimgray", 0.82)
        translate([0, 0, Z_TOP_LID])
            main_box_lid();
}

// Render complete assembly
main_box_full_assembly();
