// =============================================================================
// OpenMotorBridge - Main Box: Overall Assembly & Component Inspection
// =============================================================================
// File: hardware/cad/scad/01_main_box/99_overall_box.scad
// Description: Full 3D assembly of the 3-Tier Central Box sandwich with
//              inserted Mainboard PCB, LiPo Backup Battery, and Solid Unterwanne.
//              Supports both exploded view and fully closed assembly preview.
// =============================================================================

include <../00_common/parameters.scad>;
use <../00_common/dummies/dummy_main_pcb.scad>;
use <../00_common/dummies/dummy_lipo_battery.scad>;
use <00_lower_deck.scad>;
use <01_upper_deck.scad>;
use <02_colsure.scad>;

// View Mode: Set to true for exploded view, false for closed assembly
EXPLODED_VIEW = true;

// Vertical offsets for distinct 5-tier exploded layers
Z_LOWER_CASE   = 0.0;
Z_MAIN_PCB     = EXPLODED_VIEW ? 32.0 : 6.0;
Z_MID_TRAY     = EXPLODED_VIEW ? 64.0 : MAIN_BOX_LOWER_H;
Z_LIPO_BATTERY = EXPLODED_VIEW ? 96.0 : (MAIN_BOX_LOWER_H + 2.0);
Z_TOP_LID      = EXPLODED_VIEW ? 126.0 : (MAIN_BOX_LOWER_H + MAIN_BOX_MID_H);

module main_box_full_assembly() {
    // Layer 1: Lower Case Tub (Unterwanne, Dark Anthracite PA12 with Mounting Ears, Solid Floor)
    color("darkslategray", 0.92)
        translate([0, 0, Z_LOWER_CASE])
            main_box_lower_case();

    // Layer 2: Mainboard PCB Assembly (Green FR4 + Gold Pads + Components)
    translate([7.5, 4.5, Z_MAIN_PCB])
        dummy_main_pcb();

    // Layer 3: Mid Tray Frame with Partition Floor & 10x Breathing Slots (Oberwanne)
    color("slategray", 0.88)
        translate([0, 0, Z_MID_TRAY])
            main_box_mid_tray();

    // Layer 4: 1S LiPo Backup Battery (Floating into battery compartment tray)
    translate([MAIN_BOX_WALL + 28.0, MAIN_BOX_WALL + 17.5, Z_LIPO_BATTERY])
        dummy_lipo_battery();

    // Layer 5: Enclosure Top Lid (Gehäusedeckel, Graphite Grey with Vent & Lightpipe)
    color("dimgray", 0.82)
        translate([0, 0, Z_TOP_LID])
            main_box_lid();
}

// Render complete assembly
main_box_full_assembly();
