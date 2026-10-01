// =============================================================================
// OpenMotorBridge - Dummy 3D Model: Main Board PCB (PCBA 01 Rev 9.6)
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_main_pcb.scad
// Description: Accurate 3D representation of the central openMotorBridge
//              mainboard (PCBA 01: 85.0 x 55.0 x 1.6 mm, 4 layers ENIG)
//              with all key ICs, connectors, and antenna ports for enclosure fitting.
// =============================================================================

include <../parameters.scad>;

module dummy_main_pcb() {
    // 1. PCB Substrate (FR4 4-Layer High-TG150 Green ENIG: 85.0 x 55.0 x 1.6 mm)
    color("forestgreen") {
        difference() {
            cube(size=[85.0, 55.0, 1.6], center=false);
            // 4x M2.5 / M3 Mounting Holes (inward offset 4.0 mm: 77.0 x 47.0 mm pitch)
            translate([4.0, 4.0, -0.5]) cylinder(r=1.35, h=2.6, $fn=24);
            translate([81.0, 4.0, -0.5]) cylinder(r=1.35, h=2.6, $fn=24);
            translate([4.0, 51.0, -0.5]) cylinder(r=1.35, h=2.6, $fn=24);
            translate([81.0, 51.0, -0.5]) cylinder(r=1.35, h=2.6, $fn=24);
        }
    }

    // 2. Main Controller: ESP32-S3-WROOM-1U (U2: 18.0 x 19.2 x 3.2 mm)
    color("silver")
        translate([34.3, 17.3, 1.6])
            cube(size=[18.0, 19.2, 3.2], center=false);
    color("gold")
        translate([34.3 + 14.5, 17.3 + 16.0, 1.6 + 3.2])
            cylinder(r=1.1, h=1.0, $fn=16);

    // 3. Dedicated Helmet Audio SoC: Qualcomm QCC3084 BT 5.4 (U9: 13.0 x 18.0 x 2.8 mm)
    color([0.15, 0.40, 0.55])
        translate([66.2, 32.2, 1.6])
            cube(size=[13.0, 18.0, 2.6], center=false);
    // Integrated Ceramic Chip Antenna (top of QCC3084 module)
    color("whitesmoke")
        translate([66.2 + 2.0, 32.2 + 14.0, 1.6 + 2.6])
            cube(size=[9.0, 3.0, 1.0], center=false);

    // 4. Semtech SX1262 LoRa 868 MHz Transceiver (U10: 4.0 x 4.0 mm) & ANT1 U.FL
    color("darkslategray")
        translate([59.8, 18.2, 1.6])
            cube(size=[4.0, 4.0, 1.0], center=false);
    color("gold")
        translate([70.8, 18.2, 1.6])
            cylinder(r=1.2, h=1.25, $fn=16); // ANT1 (U.FL for LoRa FXP895)

    // 5. LM5164-Q1 72V Automotive Buck Converter & Power Choke (U1)
    color("black")
        translate([8.8, 16.2, 1.6])
            cube(size=[5.0, 4.0, 1.5], center=false);
    color([0.25, 0.25, 0.28])
        translate([15.0, 15.0, 1.6])
            cube(size=[8.0, 8.0, 4.0], center=false); // 10µH Power Inductor

    // 6. TI BQ24075 USV Power-Path Controller & LiPo Charging Stage
    color("darkslategray")
        translate([12.0, 28.0, 1.6])
            cube(size=[4.0, 4.0, 1.0], center=false);

    // 7. Internal Harness Connectors: J1 (IDC 2x06) & J3 (IDC 2x05) along front edge (Y = 49.7 mm)
    color([0.2, 0.2, 0.22]) {
        translate([41.8, 49.7, 1.6])
            cube(size=[15.2, 5.0, 8.5], center=true);
        translate([12.8, 49.7, 1.6])
            cube(size=[12.7, 5.0, 8.5], center=true);
    }

    // 8. Push-Button SW1 (Pairing / Reset: 4.5 x 4.5 mm) & Status LED D1 (WS2812B)
    color("crimson")
        translate([49.8, 18.2, 1.6])
            cube(size=[4.5, 4.5, 2.5], center=false);
    color("cyan")
        translate([34.3, 32.2, 1.6])
            cube(size=[2.0, 2.0, 0.8], center=false);

    // 9. J4 & J5 JST-PH Auxiliary Connectors along right edge
    color("ivory") {
        translate([79.8, 30.0, 1.6])
            cube(size=[4.5, 8.0, 6.0], center=false);
        translate([79.8, 42.0, 1.6])
            cube(size=[4.5, 10.0, 6.0], center=false);
    }

    // --- BOTTOM LAYER (B.Cu) COMPONENTS ---

    // 10. Qorvo DW3110 UWB Transceiver (U8) & ANT2 U.FL
    color("navy")
        translate([59.8, 33.2, -1.0])
            cube(size=[3.0, 3.0, 1.0], center=false);
    color("gold")
        translate([54.0, 27.9, -1.25])
            cylinder(r=1.2, h=1.25, $fn=16); // ANT2 (U.FL for UWB FXUWB10)

    // 11. Hirose DM3D-SF MicroSD Push-Pull Card Slot (J2 at rear edge Y = 7.2 mm)
    color("lightgrey")
        translate([30.8, 7.2, -1.8])
            cube(size=[14.0, 14.5, 1.8], center=false);

    // 12. Bosch BMI270 6-Axis IMU (U5) & Everest ES8388 Audio Codec (U3)
    color("black") {
        translate([34.3, 40.0, -0.9]) cube(size=[2.5, 3.0, 0.9], center=false);
        translate([42.8, 12.0, -1.0]) cube(size=[4.0, 4.0, 1.0], center=false);
    }
}

// Standalone preview
dummy_main_pcb();
