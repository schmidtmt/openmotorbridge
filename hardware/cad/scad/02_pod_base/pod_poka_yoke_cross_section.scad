// =============================================================================
// OpenMotorBridge - Satellite Pod: Poka-Yoke Asymmetrical Guide Cross-Section
// =============================================================================
// File: hardware/cad/scad/02_pod_base/pod_poka_yoke_cross_section.scad
// Description: 3D cross-sectional inspection model demonstrating the asymmetrical
//              Poka-Yoke tongue & groove linear rail mating (Left Z=8.2mm, Right Z=14.2mm).
//              Visually highlights the mechanical polarity protection and clearance fit.
// =============================================================================

include <../00_common/parameters.scad>;
include <pod_base_housing.scad>;
include <../03_pod_cartridges/00_base_sled.scad>;

module poka_yoke_cross_section_demo() {
    // 1. Pod Base Housing Cross-Section (Sliced at X = 50.0 mm, Translucent Slate Gray)
    intersection() {
        color("darkslategray", 0.75)
            pod_base_housing();
        
        translate([30.0, -10.0, -5.0])
            cube(size=[40.0, POD_OUTER_W + 20.0, POD_OUTER_H + 15.0], center=false);
    }

    // 2. Correctly Inserted Cartridge Sled (Vibrant Royal Blue / Orange)
    intersection() {
        translate([24.0, 3.0, 2.5]) {
            // Cartridge body
            color("dodgerblue", 0.95)
                cartridge_base_sled(
                    sled_l = CARTRIDGE_BASE_L,
                    sled_w = CARTRIDGE_BASE_W,
                    sled_h = 18.0,
                    wall   = 2.5
                );
        }
        translate([30.0, -10.0, -5.0])
            cube(size=[40.0, POD_OUTER_W + 20.0, POD_OUTER_H + 15.0], center=false);
    }

    // 3. Highlight Markers for the Asymmetrical Rail Heights
    // Left Groove Indicator Pin (Z = 8.2 mm)
    color("crimson")
        translate([50.0, -2.0, POD_GROOVE_LEFT_Z])
            rotate([0, 90, 0])
                cylinder(r=1.2, h=8.0, center=false);

    // Right Groove Indicator Pin (Z = 14.2 mm)
    color("crimson")
        translate([50.0, POD_OUTER_W - 6.0, POD_GROOVE_RIGHT_Z])
            rotate([0, 90, 0])
                cylinder(r=1.2, h=8.0, center=false);
}

// Render cross section inspection
poka_yoke_cross_section_demo();
