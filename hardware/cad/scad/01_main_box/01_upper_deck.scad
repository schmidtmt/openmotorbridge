// =============================================================================
// OpenMotorBridge - Central Main Box: Complete Slide-In Tray (v10.0)
// =============================================================================
// File: hardware/cad/scad/01_main_box/01_upper_deck.scad
// Description: Ready-to-print slide-in intermediate tray (Zwischenboden) for the
//              Central Box (Gehäuse Typ A) utilizing the v10 Dual-Rail Principle:
//              - Tool-free slide-in mounting on Rail 1 (Z = 18.0 mm).
//              - Integrated cradle for 1S LiPo backup battery (67 x 38 x 5 mm).
//              - Dedicated RF nests for Taoglas FXP895 (LoRa) & FXP73 (2.4 GHz).
//              - Thermal convection breathing slots for PCBA 01 buck converter.
//              - J7 battery lead and dual U.FL coaxial cable drop channels.
// =============================================================================

include <../00_common/parameters.scad>;
use <parts/010_slide_tray.scad>;

module main_box_mid_tray() {
    main_box_slide_tray(
        tray_l = 104.4,
        tray_w = 68.0,
        tray_t = 2.0,
        rail_z = MAIN_BOX_RAIL1_Z
    );
}

// Render complete slide-in tray
main_box_mid_tray();
