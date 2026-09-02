// =============================================================================
// OpenMotorBridge - Satellite Pod: Poka-Yoke Asymmetrical Guide Cross-Section
// =============================================================================
// File: hardware/cad/scad/02_pod_base/pod_poka_yoke_cross_section.scad
// Description: 3D cross-sectional inspection model demonstrating the asymmetrical
//              Poka-Yoke tongue & groove linear rail mating (Left Z=8.2mm, Right Z=14.2mm).
//              Slices the pod at X=55mm, looking directly into the cross-section
//              with the inserted cartridge sled, guide rails, V-tube saddle,
//              and interior bulkhead with Auto-Eject springs.
// =============================================================================

include <../00_common/parameters.scad>;
include <pod_base_housing.scad>;
include <../03_pod_cartridges/00_base_sled.scad>;

// Cut plane in X (keep rear half X = 0 .. CUT_X, cut away front mouth X > CUT_X)
CUT_X = 55.0;

module poka_yoke_cross_section_demo() {
    // 1. Pod Base Housing Cross-Section (Sliced at X = CUT_X)
    intersection() {
        color("darkslategray", 0.90)
            pod_base_housing();
        
        translate([-20.0, -15.0, -20.0])
            cube(size=[CUT_X + 20.0, POD_OUTER_W + 30.0, POD_OUTER_H + 40.0], center=false);
    }

    // 2. Correctly Inserted Cartridge Sled (Vibrant Royal Blue / Orange)
    intersection() {
        translate([POD_BULKHEAD_X + 1.0, (POD_OUTER_W - CARTRIDGE_BASE_W)/2.0, POD_WALL]) {
            color("dodgerblue", 0.95)
                cartridge_base_sled(
                    sled_l = CARTRIDGE_BASE_L,
                    sled_w = CARTRIDGE_BASE_W,
                    sled_h = CARTRIDGE_BASE_H,
                    wall   = 2.5
                );
        }
        translate([-20.0, -15.0, -20.0])
            cube(size=[CUT_X + 20.0, POD_OUTER_W + 30.0, POD_OUTER_H + 40.0], center=false);
    }

    // 3. Highlight Markers / Dimension Indicators for Asymmetrical Rail Heights
    // Left Groove Indicator Pin (Bright Crimson)
    color("crimson")
        translate([CUT_X - 1.0, -1.5, POD_GROOVE_LEFT_Z])
            rotate([0, 90, 0])
                cylinder(r=1.5, h=3.0, center=false, $fn=16);

    // Right Groove Indicator Pin (Bright Crimson)
    color("crimson")
        translate([CUT_X - 1.0, POD_OUTER_W - 1.5, POD_GROOVE_RIGHT_Z])
            rotate([0, 90, 0])
                cylinder(r=1.5, h=3.0, center=false, $fn=16);

    // 4. 2x Golden Auto-Eject Compression Springs (Visible in bulkhead background)
    color("gold") {
        translate([POD_BULKHEAD_X + 2.0, 16.0, POD_OUTER_H/2.0])
            rotate([0, 90, 0])
                cylinder(r=2.25, h=7.0, $fn=16);
        translate([POD_BULKHEAD_X + 2.0, POD_OUTER_W - 16.0, POD_OUTER_H/2.0])
            rotate([0, 90, 0])
                cylinder(r=2.25, h=7.0, $fn=16);
    }
}

// Render cross section inspection
poka_yoke_cross_section_demo();
