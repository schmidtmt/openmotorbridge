// =============================================================================
// OpenMotorBridge - Symmetrical Dual Speaker Corner-Pod (Cockpit Glance Display)
// =============================================================================
// File: hardware/cad/scad/04_front_node/cockpit_speaker_corner_pod.scad
// Description: Symmetrical miniature glance display pod mounting to the lower
//              inner corner of Rockford Fosgate Stage II speaker grilles on
//              Harley-Davidson Touring / Bagger / CVO Road Glide ST (2024+
//              Skyline OS cockpit).
// Key Constraints:
// - Leaves upper Rockford Fosgate branding and Bar & Shield badge 100% visible.
// - Leaves the handlebar riser plate ("CVO ST / Screamin' Eagle 121") free.
// - Routes thin display wiring invisibly into the lower speaker pod shadow seam
//   down into the steering head / triple tree area to Front Node (PCBA 05).
// - Zero fairing disassembly, 0 cm visible cable!
// =============================================================================

$fn = 60;

// Display module dimensions (standard 1.28" Round GC9A01 or 1.69" IPS ST7789)
DISP_DIA        = 36.5; // Outer diameter of round display PCB (mm)
DISP_ACTIVE_DIA = 33.0; // Active viewable window diameter (mm)
DISP_DEPTH      = 11.5; // Total display module cavity depth (mm)
WALL_T          = 2.2;  // Pod wall thickness (mm)
POD_OD          = DISP_DIA + 2*WALL_T; // 40.9 mm

// Speaker grille matching radius & corner bevel
SPEAKER_ARC_R   = 86.0; // Curvature radius of Rockford Fosgate grille rim (mm)
CORNER_BEVEL_H  = 18.0; // Lower corner taper height (mm)
CLIP_LIP_D      = 1.8;  // Grille clip engagement depth (mm)
CABLE_EXIT_DIA  = 3.8;  // Egress bore for 4-5 wire SPI/power ribbon lead (mm)

module display_bezel_housing() {
    difference() {
        // Outer housing body
        cylinder(r=POD_OD/2, h=DISP_DEPTH + WALL_T, center=false);
        
        // Front view aperture (beveled bezel)
        translate([0, 0, -0.5])
            cylinder(r1=DISP_ACTIVE_DIA/2 + 1.0, r2=DISP_ACTIVE_DIA/2, h=WALL_T + 1.0);
            
        // Internal display module pocket
        translate([0, 0, WALL_T])
            cylinder(r=DISP_DIA/2, h=DISP_DEPTH + 1.0);
            
        // Glass / display rebate step
        translate([0, 0, WALL_T - 0.8])
            cylinder(r=DISP_DIA/2 + 0.4, h=1.0);
    }
}

module speaker_corner_mount_flange(side="left") {
    mirror_x = (side == "right") ? 1 : 0;
    
    mirror([mirror_x, 0, 0]) {
        difference() {
            // Curvature transition block that hugs the speaker rim
            intersection() {
                translate([-POD_OD/2 - 2.0, -POD_OD/2 - 2.0, 0])
                    cube([POD_OD + 4.0, POD_OD + 4.0, DISP_DEPTH + WALL_T]);
                cylinder(r=SPEAKER_ARC_R, h=DISP_DEPTH + WALL_T);
            }
            // Cut-out matching outer display housing
            cylinder(r=POD_OD/2 + 0.2, h=DISP_DEPTH + WALL_T + 2.0, center=true);
        }
    }
}

module speaker_retention_clips() {
    // Lower clip tabs that hook behind speaker grille rim
    translate([0, -POD_OD/2 + 2.0, DISP_DEPTH + WALL_T]) {
        cube([8.0, 2.0, 5.0], center=true);
        translate([0, 0.8, 2.0])
            rotate([45, 0, 0]) cube([8.0, 1.8, 2.2], center=true);
    }
}

module cable_shadow_exit() {
    // Lower rear downward exit slot dropping into the speaker rim shadow seam
    translate([0, -POD_OD/2 - 1.0, DISP_DEPTH/2 + WALL_T])
        rotate([90, 0, 0])
            cylinder(r=CABLE_EXIT_DIA/2, h=10.0, center=true);
}

module cockpit_speaker_corner_pod(side="left") {
    difference() {
        union() {
            display_bezel_housing();
            speaker_corner_mount_flange(side);
            speaker_retention_clips();
        }
        cable_shadow_exit();
    }
}

// Parametric part selector
part = "pair"; // ["left", "right", "pair"]

if (part == "left") {
    cockpit_speaker_corner_pod(side="left");
} else if (part == "right") {
    cockpit_speaker_corner_pod(side="right");
} else {
    // Print-plate with left & right symmetrical pair
    translate([-26.0, 0, 0])
        cockpit_speaker_corner_pod(side="left");
    translate([26.0, 0, 0])
        cockpit_speaker_corner_pod(side="right");
}
