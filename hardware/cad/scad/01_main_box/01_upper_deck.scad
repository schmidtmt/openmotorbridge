// =============================================================================
// OpenMotorBridge - Main Box: Complete Mid Tray (Oberwanne / Zwischenboden)
// =============================================================================
// File: hardware/cad/scad/01_main_box/01_upper_deck.scad
// Description: Ready-to-print mid tray with partition floor, LiPo battery cradle,
//              wire routing slot, convective vent slots, front port cutouts,
//              and lower tongue lip / upper sealing groove.
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <parts/001_lower_screws_enclosure.scad>;
use <parts/005_sealing_groove.scad>;
use <parts/010_mid_tray_frame.scad>;
use <parts/011_mid_partition_floor.scad>;
use <parts/012_front_cutouts.scad>;

module main_box_mid_tray() {
    difference() {
        union() {
            // 1. Outer Frame
            main_box_mid_tray_frame(
                length=MAIN_BOX_OUTER_L,
                width=MAIN_BOX_OUTER_W,
                height=MAIN_BOX_MID_H,
                wall=MAIN_BOX_WALL
            );

            // 2. Mid Partition Floor (Akkubett + Lüftungsschlitze)
            translate([MAIN_BOX_WALL, MAIN_BOX_WALL, 0.0]) {
                main_box_mid_partition_floor(
                    floor_l=MAIN_BOX_OUTER_L - 2*MAIN_BOX_WALL,
                    floor_w=MAIN_BOX_OUTER_W - 2*MAIN_BOX_WALL,
                    floor_t=2.0
                );
            }

            // 3. 4x M3 Corner Clamping Posts (Continuous clamping chimney)
            main_box_corner_posts(
                length=MAIN_BOX_OUTER_L,
                width=MAIN_BOX_OUTER_W,
                height=MAIN_BOX_MID_H,
                post_size=MAIN_BOX_CORNER_POST,
                hole_r=M3_SCREW_HOLE_R
            );

            // 4. Bottom Sealing Tongue Lip (Feder for Lower Case sealing groove)
            main_box_sealing_tongue_lip(
                length=MAIN_BOX_OUTER_L,
                width=MAIN_BOX_OUTER_W
            );
        }

        // 5. Front Wall Port Cutouts (HD26, USB-C, Status LEDs)
        main_box_front_cutout_tool(wall_th=MAIN_BOX_WALL);

        // 6. Top Perimeter Sealing Groove (Nut for Lid O-Ring Gasket)
        main_box_sealing_groove_tool(
            length=MAIN_BOX_OUTER_L,
            width=MAIN_BOX_OUTER_W,
            z_top=MAIN_BOX_MID_H
        );
    }
}

// Render complete mid tray
main_box_mid_tray();
