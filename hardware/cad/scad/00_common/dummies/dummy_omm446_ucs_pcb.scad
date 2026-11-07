// =============================================================================
// OpenMotorBridge - Dummy 3D Model: Universal OMM Tri-Band UCS PCBA (PCBA 09/10)
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_omm446_ucs_pcb.scad
// Description: High-accuracy 3D CAD model of the unified Universal OMM Tri-Band
//              Intercom PCB (2.4 GHz Mesh + BT Classic/BLE Bridge + 446 MHz PMR/DMR):
//              - 60.0 x 30.0 x 1.0 mm FR4 4-layer substrate (ENIG gold finish)
//              - 4x M2 mounting holes (pitch: 52.0 x 22.0 mm, 4.0 mm inset)
//              - U1: Espressif ESP32-C6-MINI-1U with U.FL (Top face, 2.4 GHz Mesh)
//              - U2: Texas Instruments BQ24075RGTR PMIC (Top face, QFN-16 3x3mm)
//              - U3: NiceRF SA818-DMR SMD Transceiver 38.0 x 16.0 x 3.2 mm (Bottom face)
//              - U4: Everest Semi ES8388 Stereo Audio Codec (Top face, QFN-28 4x4mm)
//              - U5: Micropower ME6211C33M5G 3.3V LDO (Top face, SOT-23)
//              - U6: Espressif ESP32-PICO-V3-02 BT Classic/BLE Co-MCU (Bottom face)
//              - ANT1: Johanson 2450AT18x100 2.45 GHz Chip Antenna (Top face)
//              - J1: IP67 16-Pin USB-C receptacle (TYPE-C-31-M-12, -X edge, Top face)
//              - BAT1: 2-Pin JST-SH Battery Header directly beneath J1 on Bottom face
//                      (Local X=3.45, Y=15.05 mm, rot=-90°, 100% clear of battery!)
//              - J_HELMET: 6-Pin JST-SH Helmet Audio/PTT Header at +X edge on Bottom face
//                      (Local X=57.05, Y=14.70 mm, rot=+90°, 100% clear of battery!)
//              - J_RF: U.FL Coaxial RF Receptacle (Top face, Local X=40.20, Y=28.50 mm)
//              - SW1..SW4: 4x tactile IP67 micro-switches (PTT, Mode, Ch+/Vol+, Ch-/Vol-)
//              - D1: WS2812B-2020 RGB Status-LED
//              - 1000 mAh LiPo Flat Pouch Cell (Typ 603040 / 602840: 40 x 28 x 6.0 mm)
//                nested cleanly in the 48 mm center bay between BAT1 and J_HELMET
// =============================================================================

include <../parameters.scad>;

module dummy_omm446_ucs_pcb(include_battery = true) {
    pcb_l = 60.0;
    pcb_w = 30.0;
    pcb_h = 1.0;

    // 1. FR4 4-Layer Substrate (Black Soldermask, ENIG Gold Pads)
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

    // -------------------------------------------------------------------------
    // TOP FACE COMPONENTS (F.Cu)
    // -------------------------------------------------------------------------

    // 2. U1: Espressif ESP32-C6-MINI-1U Module (Top Face, Local X=30.70, Y=10.20 mm)
    color("silver") {
        translate([30.70 - 16.6/2.0, 10.20 - 13.2/2.0, pcb_h])
            cube(size=[16.6, 13.2, 2.4], center=false);
    }

    // 3. U2: TI BQ24075RGTR PMIC (Top Face, Local X=18.40, Y=19.30 mm, QFN-16 3x3mm)
    color("black") {
        translate([18.40 - 1.5, 19.30 - 1.5, pcb_h])
            cube(size=[3.0, 3.0, 0.9], center=false);
    }

    // 4. U4: Everest Semi ES8388 Stereo Audio Codec (Top Face, Local X=47.00, Y=7.90 mm, QFN-28 4x4mm)
    color("black") {
        translate([47.00 - 2.0, 7.90 - 2.0, pcb_h])
            cube(size=[4.0, 4.0, 0.9], center=false);
    }

    // 5. U5: Micropower ME6211C33M5G 3.3V LDO (Top Face, Local X=13.50, Y=27.69 mm, SOT-23)
    color("darkslategray") {
        translate([13.50 - 1.45, 27.69 - 0.8, pcb_h])
            cube(size=[2.9, 1.6, 1.1], center=false);
    }

    // 6. ANT1: Johanson 2450AT18x100 2.45 GHz Ceramic Chip Antenna (Top Face, Local X=9.70, Y=2.20 mm)
    color("whitesmoke") {
        translate([9.70 - 1.6, 2.20 - 0.8, pcb_h])
            cube(size=[3.2, 1.6, 1.2], center=false);
    }

    // 7. J1: IP67 16-Pin USB-C Receptacle (-X Edge, Local X=4.55, Y=15.00 mm)
    color("silver") {
        translate([-1.5, pcb_w/2.0 - 4.5, pcb_h])
            cube(size=[7.5, 9.0, 3.2], center=false);
    }

    // 8. D2: USBLC6-2SC6 ESD Protection (Top Face, Local X=16.60, Y=12.90 mm)
    color("black") {
        translate([16.60 - 1.45, 12.90 - 1.4, pcb_h])
            cube(size=[2.9, 2.8, 1.1], center=false);
    }

    // 9. SW1..SW4: 4x Tactile IP67 Micro-Switches (Top Face, Local X=13, 25, 37, 49, Y=22.0 mm)
    color("darkslategray") {
        translate([13.0, 22.0, pcb_h]) cube(size=[3.5, 2.8, 1.2], center=true);
        translate([25.0, 22.0, pcb_h]) cube(size=[3.5, 2.8, 1.2], center=true);
        translate([37.0, 22.0, pcb_h]) cube(size=[3.5, 2.8, 1.2], center=true);
        translate([49.0, 22.0, pcb_h]) cube(size=[3.5, 2.8, 1.2], center=true);
    }

    // 10. D1: WS2812B-2020 RGB Status-LED (Top Face, Local X=30.90, Y=26.20 mm)
    color("cyan") {
        translate([30.90, 26.20, pcb_h])
            cube(size=[2.0, 2.0, 0.7], center=true);
    }

    // 11. J_RF: U.FL Coaxial RF Receptacle (Top Face, Local X=40.20, Y=28.50 mm)
    color("gold") {
        translate([40.20 - 1.5, 28.50 - 1.5, pcb_h])
            cube(size=[3.0, 3.0, 1.25], center=false);
    }

    // -------------------------------------------------------------------------
    // BOTTOM FACE COMPONENTS (B.Cu)
    // -------------------------------------------------------------------------

    // 12. U6: Espressif ESP32-PICO-V3-02 Bluetooth Classic/BLE Co-MCU (Bottom Face, Local X=16.70, Y=4.45 mm)
    color("black") {
        translate([16.70 - 3.5, 4.45 - 3.5, -0.9])
            cube(size=[7.0, 7.0, 0.9], center=false);
    }

    // 13. U3: NiceRF SA818-DMR Transceiver Module (Bottom Face, Local X=30.0, Y=18.0 mm, 38.0 x 16.0 x 3.2 mm)
    color("silver") {
        translate([30.0 - 19.0, 18.0 - 8.0, -3.2])
            cube(size=[38.0, 16.0, 3.2], center=false);
    }

    // 14. BAT1: 2-Pin JST-SH Battery Header directly beneath J1 USB-C on Bottom Face
    //     (KiCad X=73.45, Y=100.05 -> Local X=3.45, Y=15.05 mm, rot=-90°, completely outside battery!)
    color("ghostwhite") {
        translate([3.45 - 2.9/2.0, 15.05 - 4.0/2.0, -2.8])
            cube(size=[2.9, 4.0, 2.8], center=false);
    }

    // 15. J_HELMET: 6-Pin JST-SH Passive Helmet Audio & PTT Header at +X edge on Bottom Face
    //     (KiCad X=127.05, Y=99.70 -> Local X=57.05, Y=14.70 mm, rot=+90°, completely outside battery!)
    color("ivory") {
        difference() {
            translate([57.05 - 2.9/2.0, 14.70 - 8.0/2.0, -2.8])
                cube(size=[2.9, 8.0, 2.8], center=false);
            // Inward-facing mating socket (-X face)
            translate([57.05 - 2.9/2.0 - 0.1, 14.70 - 6.5/2.0, -2.5])
                cube(size=[2.0, 6.5, 2.2], center=false);
        }
    }

    // 16. 1000 mAh 1S LiPo Flat Pouch Cell (Typ 603040 / 602840: 40.0 x 28.0 x 6.0 mm)
    //     Sits centered in X=10.0..50.0 mm between BAT1 (X=3.45) and J_HELMET (X=57.05),
    //     directly beneath U3 SA818-DMR (Z = -9.4 .. -3.4 mm)
    if (include_battery) {
        color([0.15, 0.35, 0.65]) {
            translate([10.0, (pcb_w - 28.0)/2.0, -9.4])
                cube(size=[40.0, 28.0, 6.0], center=false);
        }
    }
}

// Standalone Render Preview
dummy_omm446_ucs_pcb();
