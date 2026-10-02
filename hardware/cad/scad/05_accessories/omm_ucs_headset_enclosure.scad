// =============================================================================
// OpenMotorBridge - OMM 2.4 GHz ECE 22.06 UCS Headset & Helmet Mount Enclosure
// =============================================================================
// File: hardware/cad/scad/05_accessories/omm_ucs_headset_enclosure.scad
// Description: Standalone, parametric 3D CAD model of the OpenMotorMesh (OMM)
//              2.4 GHz Intercom Transceiver in standardized ECE 22.06 UCS form factor
//              including the universal Helmet Clamp & Adhesive Cradle:
//              1. Direct access to the autonomous OMM UCS module (PA12 MJF)
//              2. ECE 22.06 Universal Helmet Cradle (Snap-Fit Retention + Cable Duct)
//              3. Dual Helmet Mounting:
//                 - Method A: 3M VHB 5952 curved adhesive base (R130 mm helmet curve)
//                 - Method B: Two-screw stainless spring clamp for helmet rim
//              4. Strain-relieved cable tunnel for helmet speakers & boom microphone
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <../03_pod_cartridges/parts/omm_ucs_module.scad>;

// Universal Helmet Cradle Parameters
CRADLE_L        = 74.0;  // Outer cradle length (mm)
CRADLE_W        = 42.0;  // Outer cradle width (mm)
CRADLE_H        = 7.0;   // Base plate height (mm)
CRADLE_WALL     = 2.0;   // Wall thickness (mm)
HELMET_CURVE_R  = 135.0; // Typical motorcycle helmet outer shell radius (mm)

// 1. Universal Helmet Cradle (PA12 MJF, Anthracite)
module omm_ucs_helmet_cradle() {
    difference() {
        union() {
            // Main Cradle Body
            difference() {
                // Outer rounded block
                translate([3.0, 3.0, 0])
                    minkowski() {
                        cube([CRADLE_L - 6.0, CRADLE_W - 6.0, CRADLE_H - 1.0], center=false);
                        cylinder(r=3.0, h=1.0, $fn=32);
                    }

                // Helmet Curvature Cutout on Back Face (-Z)
                translate([CRADLE_L / 2.0, -10.0, -HELMET_CURVE_R + 1.2])
                    rotate([0, 90, 0])
                        cylinder(r=HELMET_CURVE_R, h=CRADLE_L + 10.0, center=true, $fn=72);
            }

            // Left Retention Catch Latch (+Y Flank)
            translate([CRADLE_L / 2.0 - 7.0, CRADLE_W - 2.5, CRADLE_H]) {
                cube([14.0, 2.5, 4.0], center=false);
                // Inward snap overhang
                translate([0, -0.8, 2.5])
                    cube([14.0, 0.8, 1.5], center=false);
            }

            // Right Retention Catch Latch (-Y Flank)
            translate([CRADLE_L / 2.0 - 7.0, 0.0, CRADLE_H]) {
                cube([14.0, 2.5, 4.0], center=false);
                // Inward snap overhang
                translate([0, 2.5, 2.5])
                    cube([14.0, 0.8, 1.5], center=false);
            }
        }

        // Inner Pocket for UCS Module (68.4 x 36.4 x 4.5 mm with lead-in chamfers)
        translate([(CRADLE_L - 68.4) / 2.0, (CRADLE_W - 36.4) / 2.0, 1.8]) {
            cube([68.4, 36.4, CRADLE_H + 2.0], center=false);
        }

        // Cable Strain-Relief Duct for Helmet Audio Loom (Ø 4.5 mm canal)
        translate([-1.0, CRADLE_W / 2.0, 2.5])
            rotate([0, 90, 0])
                cylinder(r=2.25, h=CRADLE_L + 2.0, $fn=24);

        // 2x M2.5 Fastening Screw Holes for Helmet Rim Clamp
        translate([12.0, CRADLE_W / 2.0, -0.5])
            cylinder(r=1.35, h=CRADLE_H + 2.0, $fn=20);
        translate([CRADLE_L - 12.0, CRADLE_W / 2.0, -0.5])
            cylinder(r=1.35, h=CRADLE_H + 2.0, $fn=20);

        // Weight-Reduction & 3M VHB Tape Adhesive Recess (0.8 mm depth on back)
        translate([8.0, 6.0, -0.1])
            cube([CRADLE_L - 16.0, CRADLE_W - 12.0, 0.9], center=false);
    }
}

// 2. Stainless Steel Rim Clamp Plate (Optional for Non-Adhesive Helmet Fit)
module omm_ucs_rim_clamp() {
    color("silver", 0.9) {
        difference() {
            union() {
                // Spring Clamp Base Plate (1.2 mm Spring Steel)
                translate([6.0, 12.0, 0])
                    cube([CRADLE_L - 12.0, 18.0, 1.2], center=false);
                // Curved Inner Hook Tongue slipping under helmet shell rim
                translate([6.0, 12.0, -18.0])
                    cube([CRADLE_L - 12.0, 1.5, 18.0], center=false);
            }
            // 2x M2.5 Through-Holes
            translate([12.0, CRADLE_W / 2.0, -1.0])
                cylinder(r=1.4, h=4.0, $fn=20);
            translate([CRADLE_L - 12.0, CRADLE_W / 2.0, -1.0])
                cylinder(r=1.4, h=4.0, $fn=20);
        }
    }
}

// 3. Complete Headset Assembly
module omm_ucs_headset_assembly(exploded = false) {
    z_clamp  = exploded ? -22.0 : -2.0;
    z_cradle = 0.0;
    z_module = exploded ? 24.0 : 2.0;

    // Optional Helmet Rim Clamp
    translate([0, 0, z_clamp])
        omm_ucs_rim_clamp();

    // Universal Helmet Mounting Cradle
    color([0.20, 0.22, 0.24])
        translate([0, 0, z_cradle])
            omm_ucs_helmet_cradle();

    // Autonomous OMM 2.4 GHz Transceiver Module
    translate([(CRADLE_L - 68.0) / 2.0, (CRADLE_W - 36.0) / 2.0, z_module])
        omm_ucs_module_assembly(exploded = false);
}

// Standalone Render Preview
omm_ucs_headset_assembly(exploded = true);
