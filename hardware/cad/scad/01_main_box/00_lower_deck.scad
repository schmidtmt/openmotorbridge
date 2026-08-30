// =============================================================================
// OpenMotorBridge - Main Box: Complete Lower Case (Unterwanne)
// =============================================================================
// File: hardware/cad/scad/01_main_box/00_lower_deck.scad
// Description: Ready-to-print lower case tub with 4x M3 corner clamping posts,
//              4x M2.5 PCB standoffs, 4x thermal copper stud floor through-holes,
//              perimeter sealing groove, and 4x M4 silentblock mounting ears.
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
include <parts/000_lower_base.scad>;
include <parts/001_lower_screws_enclosure.scad>;
include <parts/002_pcb_standoffs.scad>;
include <parts/003_copper_thermal_studs.scad>;
include <parts/004_mounting_ears.scad>;
include <parts/005_sealing_groove.scad>;

module main_box_lower_case() {
    difference() {
        union() {
            // 1. Base Enclosure Tub
            main_box_lower_base(
                length=MAIN_BOX_OUTER_L,
                width=MAIN_BOX_OUTER_W,
                height=MAIN_BOX_LOWER_H,
                wall=MAIN_BOX_WALL
            );

            // 2. 4x M3 Corner Clamping Posts
            main_box_corner_posts(
                length=MAIN_BOX_OUTER_L,
                width=MAIN_BOX_OUTER_W,
                height=MAIN_BOX_LOWER_H,
                post_size=MAIN_BOX_CORNER_POST,
                hole_r=M3_SCREW_HOLE_R
            );

            // 3. 4x M2.5 Mainboard PCB Screw Standoffs
            main_box_pcb_standoffs(
                pcb_x_offset=7.5,
                pcb_y_offset=4.5,
                h=3.5
            );

            // 4. 4x Outer M4 Silentblock Mounting Ears
            main_box_mounting_ears(
                length=MAIN_BOX_OUTER_L,
                width=MAIN_BOX_OUTER_W
            );
        }

        // 5. 4x Thermal Copper Stud Floor Pockets (Ø 8.0 mm through-holes)
        main_box_copper_stud_cutouts(h=6.0);

        // 6. Perimeter Sealing Groove (Nut for Ø 1.5 mm O-Ring Gasket)
        main_box_sealing_groove_tool(
            length=MAIN_BOX_OUTER_L,
            width=MAIN_BOX_OUTER_W,
            z_top=MAIN_BOX_LOWER_H
        );
    }
}

// Render complete lower case
main_box_lower_case();
