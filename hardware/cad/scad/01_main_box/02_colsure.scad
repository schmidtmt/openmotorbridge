// =============================================================================
// OpenMotorBridge - Main Box: Complete Lid Plate (Gehäusedeckel)
// =============================================================================
// File: hardware/cad/scad/01_main_box/02_colsure.scad
// Description: Ready-to-print lid plate with continuous perimeter sealing tongue lip,
//              integrated Gore ePTFE breather vent seat, and 4x M3 countersunk holes.
// =============================================================================

include <../00_common/parameters.scad>;
include <parts/020_lid_plate.scad>;

module main_box_lid() {
    main_box_lid_plate(
        length=MAIN_BOX_OUTER_L,
        width=MAIN_BOX_OUTER_W,
        plate_h=MAIN_BOX_LID_H,
        lip_h=1.5,
        lip_w=1.6
    );
}

// Render complete lid
main_box_lid();
