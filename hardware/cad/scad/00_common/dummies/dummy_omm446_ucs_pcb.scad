// =============================================================================
// OpenMotorBridge - Dummy 3D Model: OMM 446 MHz PMR/DMR Transceiver PCBA (PCBA 10)
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_omm446_ucs_pcb.scad
// Description: High-accuracy 3D CAD model of the OMM 446 MHz PCBA 10:
//              - 60.0 x 30.0 x 1.0 mm FR4 4-layer substrate (ENIG gold finish)
//              - 4x M2 mounting holes (pitch: 52.0 x 22.0 mm, 4.0 mm inset)
//              - Espressif ESP32-C6-MINI-1U with U.FL (Top face)
//              - NiceRF SA818-DMR SMD Transceiver 38.0 x 16.0 x 3.2 mm (Bottom face)
//              - Everest Semi ES8388 Stereo Audio Codec (QFN-28 4x4mm, Top face)
//              - Texas Instruments BQ24075 PMIC (QFN-16 3x3mm, Bottom face)
//              - Micropower ME6211 3.3V LDO (SOT-23-5, Top face)
//              - IP67 16-Pin USB-C receptacle (TYPE-C-31-M-12, -X edge)
//              - 8-Pin Kelvin JST-SH 1.0mm Docking Header (BM08B-SRSS-TB, Bottom face)
//              - U.FL Coaxial RF Receptacle (J_RF 50 Ohm, Bottom face)
//              - Spring Compression Contact Pad for Lid Helical Antenna (Top face)
//              - 4x tactile IP67 micro-switches (PTT, Mode, Ch+, Ch-)
//              - WS2812B-2020 RGB Status-LED
//              - 600 mAh LiPo Flat Pouch Cell (38 x 24 x 4.5 mm)
// =============================================================================

include <../parameters.scad>;

module dummy_omm446_ucs_pcb() {
    pcb_l = 60.0;
    pcb_w = 30.0;
    pcb_h = 1.0;

    // 1. FR4 Substrate (Black Soldermask, ENIG Gold Pads)
    color([0.12, 0.12, 0.14]) {
        difference() {
            // Main PCB outline with rounded corners (R=2.5mm)
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

    // 2. Espressif ESP32-C6-MINI-1U Module (Top Face, X=18.0mm, Y=7.0mm)
    color("silver") {
        translate([18.0, 7.0, pcb_h])
            cube(size=[16.6, 13.2, 2.4], center=false);
    }

    // 3. Everest Semi ES8388 Stereo Audio Codec (Top Face, QFN-28 4x4mm)
    color("black") {
        translate([37.5, 13.5, pcb_h])
            cube(size=[4.0, 4.0, 0.9], center=false);
    }

    // 4. Micropower ME6211 3.3V LDO (Top Face, SOT-23-5)
    color("darkslategray") {
        translate([45.0, 3.5, pcb_h])
            cube(size=[2.9, 1.6, 1.1], center=false);
    }

    // 5. IP67 16-Pin USB-C Receptacle (-X Edge, facing outward)
    color("silver") {
        translate([-1.5, pcb_w/2.0 - 4.5, pcb_h])
            cube(size=[7.5, 9.0, 3.2], center=false);
    }

    // 6. 4x Tactile IP67 Micro-Switches (Top Face, Y=22.0mm)
    color("darkslategray") {
        // SW1: PTT / MFB
        translate([13.0, 22.0, pcb_h]) cube(size=[3.5, 2.8, 1.2], center=true);
        // SW2: Mode (Analog FM <-> DMR)
        translate([25.0, 22.0, pcb_h]) cube(size=[3.5, 2.8, 1.2], center=true);
        // SW3: Channel Up (1-16)
        translate([37.0, 22.0, pcb_h]) cube(size=[3.5, 2.8, 1.2], center=true);
        // SW4: Channel Down (16-1)
        translate([49.0, 22.0, pcb_h]) cube(size=[3.5, 2.8, 1.2], center=true);
    }

    // 7. WS2812B-2020 RGB Status-LED (KiCad D1: X=30.98, Y=26.22 mm)
    color("cyan") {
        translate([30.98, 26.22, pcb_h])
            cube(size=[2.0, 2.0, 0.7], center=true);
    }

    // 8. Spring Compression Contact Pad for Helical Antenna (+X Edge, Top Face)
    color("gold") {
        translate([pcb_l - 4.0, pcb_w/2.0 - 2.0, pcb_h])
            cylinder(r=1.5, h=0.2, $fn=24);
    }

    // -------------------------------------------------------------------------
    // BOTTOM FACE COMPONENTS (SA818-DMR Transceiver, PMIC, Docking Header)
    // -------------------------------------------------------------------------

    // 9. NiceRF SA818-DMR Transceiver Module (Bottom Face, Shield Can 38.0 x 16.0 x 3.2 mm)
    color("silver") {
        translate([13.0, (pcb_w - 16.0)/2.0, -3.2])
            cube(size=[38.0, 16.0, 3.2], center=false);
    }

    // 10. TI BQ24075 PMIC (Bottom Face, QFN-16 3x3mm)
    color("black") {
        translate([52.0, 9.0, -0.9])
            cube(size=[3.0, 3.0, 0.9], center=false);
    }


    // 12. 2-Pin Battery Header BAT1 (Bottom Face, BM02B-SRSS-TB 3.5 x 4.2 x 2.9 mm)
    color("ghostwhite") {
        translate([8.0, 6.0, -2.9])
            cube(size=[3.5, 4.2, 2.9], center=false);
    }

    // 13. U.FL Coaxial RF Receptacle J_RF (Bottom Face, 3.0 x 3.0 x 1.25 mm)
    color("gold") {
        translate([52.5, 15.0, -1.25])
            cube(size=[3.0, 3.0, 1.25], center=false);
    }

    // 14. 600 mAh LiPo Flat Pouch Cell (Nested beneath or alongside module)
    color([0.15, 0.35, 0.65]) {
        translate([11.0, (pcb_w - 24.0)/2.0, -7.8])
            cube(size=[38.0, 24.0, 4.5], center=false);
    }
}

// Standalone Render Preview
dummy_omm446_ucs_pcb();
