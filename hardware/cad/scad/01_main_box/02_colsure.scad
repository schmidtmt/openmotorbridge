// =============================================================================
// OpenMotorBridge - Central Main Box: Complete L-Slide Lid (v10.0)
// =============================================================================
// File: hardware/cad/scad/01_main_box/02_colsure.scad
// Description: Ready-to-print L-shaped slide lid (Schiebedeckel) for the
//              Central Box (Gehäuse Typ A) utilizing the v10 Dual-Rail Principle:
//              - Form-fit slide-in mounting on Rail 2 (Z = 33.0 mm) C-grooves.
//              - Front wedge-lock nose (Keilanzug) for front gasket compression.
//              - Integrated Gore ePTFE pressure compensation membrane seat.
//              - Vertical rear Heckwand with drip apron overlapping lower sill.
//              - 100% non-metallic PA12 Slam-to-Shut deadbolt locking system.
// =============================================================================

include <../00_common/parameters.scad>;
use <parts/020_slide_lid.scad>;

module main_box_lid() {
    main_box_slide_lid(
        length = MAIN_BOX_OUTER_L,
        width  = MAIN_BOX_OUTER_W,
        height = MAIN_BOX_TOTAL_H,
        wall   = MAIN_BOX_WALL
    );
}

// Render complete slide lid
main_box_lid();
