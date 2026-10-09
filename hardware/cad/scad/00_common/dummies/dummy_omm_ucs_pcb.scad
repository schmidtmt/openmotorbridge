// =============================================================================
// OpenMotorBridge - Dummy 3D Model: OMM 2.4 GHz UCS Intercom PCBA (PCBA 09)
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_omm_ucs_pcb.scad
// Description: Accurate 3D CAD model of the autonomous OMM 2.4 GHz UCS PCB:
//              - 60.0 x 30.0 x 1.0 mm FR4 substrate (ENIG gold finish)
//              - 4x M2 mounting holes (pitch: 52.0 x 22.0 mm)
//              - Espressif ESP32-C6-MINI-1 (13.2 x 16.6 mm)
//              - Texas Instruments BQ24075 PMIC (QFN-16 3x3mm)
//              - Everest Semi ES8311 Audio Codec (QFN-20 3x3mm)
//              - Johanson 2450AT45A100 2.4 GHz ceramic antenna
//              - IP67 16-Pin USB-C receptacle (Korean HRO TYPE-C-31-M-12)
//              - 4x tactile IP67 micro-switches (Panasonic EVQ-P2)
//              - WS2812B-2020 RGB Status-LED
//              - 600 mAh LiPo Flat Pouch Cell (38 x 24 x 4.5 mm)
// =============================================================================

include <../parameters.scad>;

module dummy_omm_ucs_pcb() {
    pcb_l = 60.0;
    pcb_w = 30.0;
    pcb_h = 1.0;

    // 1. FR4 Substrate (Black Soldermask, ENIG Gold Pads)
    color([0.12, 0.12, 0.14]) {
        difference() {
            // Main PCB outline with rounded corners
            hull() {
                translate([2.5, 2.5, 0]) cylinder(r=2.5, h=pcb_h, $fn=32);
                translate([pcb_l - 2.5, 2.5, 0]) cylinder(r=2.5, h=pcb_h, $fn=32);
                translate([2.5, pcb_w - 2.5, 0]) cylinder(r=2.5, h=pcb_h, $fn=32);
                translate([pcb_l - 2.5, pcb_w - 2.5, 0]) cylinder(r=2.5, h=pcb_h, $fn=32);
            }
            // 4x M2 Mounting Holes (52.0 x 22.0 mm pitch, 4.0 mm from edges)
            translate([4.0, 4.0, -0.1]) cylinder(r=M2_SCREW_HOLE_R, h=pcb_h + 0.2, $fn=24);
            translate([pcb_l - 4.0, 4.0, -0.1]) cylinder(r=M2_SCREW_HOLE_R, h=pcb_h + 0.2, $fn=24);
            translate([4.0, pcb_w - 4.0, -0.1]) cylinder(r=M2_SCREW_HOLE_R, h=pcb_h + 0.2, $fn=24);
            translate([pcb_l - 4.0, pcb_w - 4.0, -0.1]) cylinder(r=M2_SCREW_HOLE_R, h=pcb_h + 0.2, $fn=24);
        }
    }

    // 2. Espressif ESP32-C6-MINI-1 Module (Top Face, Centered in X=26mm)
    color("silver") {
        translate([18.0, 7.0, pcb_h])
            cube(size=[16.6, 13.2, 2.4], center=false);
    }

    // 3. TI BQ24075 PMIC (QFN-16 3x3mm)
    color("black") {
        translate([38.0, 6.0, pcb_h])
            cube(size=[3.0, 3.0, 0.9], center=false);
    }

    // 4. Everest Semi ES8388 Stereo Audio Codec (QFN-28 4x4mm)
    color("black") {
        translate([37.5, 13.5, pcb_h])
            cube(size=[4.0, 4.0, 0.9], center=false);
    }

    // 5. Johanson 2450AT Ceramic Chip Antenna (+X Edge, Keepout zone)
    color("whitesmoke") {
        translate([pcb_l - 11.5, pcb_w/2.0 - 1.0, pcb_h])
            cube(size=[9.5, 2.0, 1.2], center=false);
    }

    // 6. IP67 16-Pin USB-C Receptacle (-X Edge, facing outward)
    color("silver") {
        translate([-1.5, pcb_w/2.0 - 4.5, pcb_h])
            cube(size=[7.5, 9.0, 3.2], center=false);
    }

    // 7. 4x Tactile IP67 Micro-Switches (Top Face, KiCad SW1..SW4: X=13, 25, 37, 49, Y=22.0 mm)
    color("darkslategray") {
        // SW1: Power / MFB
        translate([13.0, 22.0, pcb_h]) cube(size=[3.5, 2.8, 1.2], center=true);
        // SW2: Mesh / Group
        translate([25.0, 22.0, pcb_h]) cube(size=[3.5, 2.8, 1.2], center=true);
        // SW3: Vol+
        translate([37.0, 22.0, pcb_h]) cube(size=[3.5, 2.8, 1.2], center=true);
        // SW4: Vol-
        translate([49.0, 22.0, pcb_h]) cube(size=[3.5, 2.8, 1.2], center=true);
    }

    // 8. WS2812B-2020 RGB Status-LED (KiCad D1: X=30.98, Y=26.22 mm)
    color("cyan") {
        translate([30.98, 26.22, pcb_h])
            cube(size=[2.0, 2.0, 0.7], center=true);
    }

    // 9. 1S LiPo Flat Pouch Cell (Mounted on Bottom Face or Nested)
    color([0.15, 0.35, 0.65]) {
        translate([11.0, (pcb_w - 24.0)/2.0, -4.5])
            cube(size=[38.0, 24.0, 4.5], center=false);
    }

    // 10. J_HELMET: Internal 6-Pin Passive Helmet Audio & PTT Header (Bottom Face, SM06B-SRSS-TB)
    // Sits in rear chamber opposite USB-C (X = 56.625 mm, Y = 14.75 mm) facing through bottom shell slot into helmet
    color("ivory") {
        translate([56.625 - 4.25/2.0, 14.75 - 7.5/2.0, -2.8])
            cube(size=[4.25, 7.5, 2.8], center=false);
    }
}

// Standalone Render Preview
dummy_omm_ucs_pcb();
