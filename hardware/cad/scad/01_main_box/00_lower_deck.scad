// =============================================================================
// OpenMotorBridge - Central Main Box: Complete Monocoque Tub (v10.0)
// =============================================================================
// File: hardware/cad/scad/01_main_box/00_lower_deck.scad
// Description: Ready-to-print monolithic PA12 monocoque housing tub for the
//              Central Box (Gehäuse Typ A: 110 x 74 x 38 mm). Implements the v10
//              Dual-Rail Monocoque Slide-In architecture:
//              - 100% solid, leak-free floor with 4x M4 silentblock mounting ears.
//              - 4x M2.5/M3 PCB standoffs (h = 3.5 mm) for PCBA 01 (85 x 55 mm).
//              - Solid front wall with DTM-6, 16-Pin Periphery, USB-C, and SW1.
//              - Rail 1 (Z = 18.0 mm) for Slide-In Zwischenboden (battery/antennas).
//              - Rail 2 (Z = 33.0 mm) C-grooves with PA12 retaining roof for L-Slide Lid.
//              - Rear insertion portal (Z = 15..38 mm) above lower sill (Z = 0..15 mm).
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <parts/000_monocoque_tub.scad>;

module main_box_lower_case() {
    main_box_monocoque_tub(
        length = MAIN_BOX_OUTER_L,
        width  = MAIN_BOX_OUTER_W,
        height = MAIN_BOX_TOTAL_H,
        wall   = MAIN_BOX_WALL
    );
}

// Render complete lower case tub
main_box_lower_case();
