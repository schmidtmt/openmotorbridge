// =============================================================================
// OpenMotorBridge - Dummy 3D Model: Main Board PCB (PCBA 01 Rev 10.0)
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_main_pcb.scad
// Description: Accurate 3D representation of the central openMotorBridge
//              mainboard (PCBA 01: 85.0 x 55.0 x 1.6 mm, 4 layers ENIG)
//              with all v10 ICs, vertical connectors, and antenna ports for enclosure fitting.
// =============================================================================

include <../parameters.scad>;

module dummy_main_pcb() {
    // 1. PCB Substrate (FR4 4-Layer High-TG150 Green ENIG: 85.0 x 55.0 x 1.6 mm)
    color("forestgreen") {
        difference() {
            cube(size=[85.0, 55.0, 1.6], center=false);
            // 4x M2.5 / M3 Mounting Holes (inward offset 4.0 mm: 77.0 x 47.0 mm pitch)
            translate([4.0, 4.0, -0.5]) cylinder(r=1.5, h=2.6, $fn=24);
            translate([81.0, 4.0, -0.5]) cylinder(r=1.5, h=2.6, $fn=24);
            translate([4.0, 51.0, -0.5]) cylinder(r=1.5, h=2.6, $fn=24);
            translate([81.0, 51.0, -0.5]) cylinder(r=1.5, h=2.6, $fn=24);
        }
    }

    // 2. Main Controller: ESP32-S31-WROOM-1U (U2: 18.0 x 19.2 x 3.2 mm)
    color("silver")
        translate([37.28 - 9.0, 10.06 - 9.6, 1.6])
            cube(size=[18.0, 19.2, 3.2], center=false);
    color("gold")
        translate([37.28 + 6.0, 10.06 + 7.0, 1.6 + 3.2])
            cylinder(r=1.1, h=1.0, $fn=16); // U.FL Port on S31

    // 3. Dedicated Helmet Audio SoC: Qualcomm QCC3084 BT 5.4 (U9: 13.0 x 18.0 x 2.8 mm)
    color([0.15, 0.40, 0.55])
        translate([66.48 - 6.5, 19.65 - 9.0, 1.6])
            cube(size=[13.0, 18.0, 2.6], center=false);
    // Integrated Ceramic Chip Antenna
    color("whitesmoke")
        translate([66.48 - 4.5, 19.65 + 6.0, 1.6 + 2.6])
            cube(size=[9.0, 3.0, 1.0], center=false);

    // 4. Semtech SX1262 LoRa 868 MHz Transceiver (U10: 4.0 x 4.0 mm) & ANT1 U.FL
    color("darkslategray")
        translate([52.53 - 2.0, 2.89 - 2.0, 1.6])
            cube(size=[4.0, 4.0, 1.0], center=false);
    color("gold")
        translate([60.81, 2.90, 1.6])
            cylinder(r=1.2, h=1.25, $fn=16); // ANT1 (U.FL for LoRa FXP895)

    // 5. LM5164-Q1 Power Choke L1 (12.0 x 12.0 x 6.0 mm)
    color([0.25, 0.25, 0.28])
        translate([8.78 - 6.0, 31.15 - 6.0, 1.6])
            cube(size=[12.0, 12.0, 6.0], center=false); // 47µH Power Inductor

    // 6. Header J1: Molex Micro-Lock Plus 1.25mm 6-Pin Vertikal (Bordnetz & CAN)
    color("ivory")
        translate([16.16 - 4.5, 51.90 - 2.5, 1.6])
            cube(size=[9.0, 5.0, 7.5], center=false);

    // 7. Push-Button SW1 (Pairing / Reset: Alps SKRK)
    color("crimson")
        translate([28.43 - 2.25, 51.65 - 2.25, 1.6])
            cube(size=[4.5, 4.5, 2.5], center=false);

    // 8. Header J6: Molex Picoflex 16-Pin 2x08 Vertikal (4 Autarke OMB-Systemstränge)
    color("black")
        translate([40.78 - 11.5, 46.15 - 3.0, 1.6])
            cube(size=[23.0, 6.0, 8.5], center=false);

    // 9. Receptacle J3: USB Type-C 16-Pin Service & Flash Port (HRO TYPE-C-31-M-12)
    color("silver")
        translate([62.78 - 4.5, 50.90 - 3.5, 1.6])
            cube(size=[9.0, 7.5, 3.2], center=false);

    // 10. Status LED D1 (WS2812B RGB)
    color("cyan")
        translate([72.53 - 1.0, 34.65 - 1.0, 1.6])
            cube(size=[2.0, 2.0, 0.8], center=false);

    // 11. Side Headers: J4 (RGB 3P), J5 (Battery 4P), J7 (Reserve USB 4P)
    color("ivory") {
        // J5 (USV-Batterie & NTC at Y = 20.0 mm)
        translate([81.58 - 2.5, 20.00 - 3.5, 1.6])
            cube(size=[5.0, 7.0, 7.5], center=false);
        // J4 (Ext RGB LED at Y = 30.0 mm)
        translate([81.58 - 2.5, 30.00 - 3.0, 1.6])
            cube(size=[5.0, 6.0, 7.5], center=false);
        // J7 (Reserve USB 7 at Y = 40.0 mm)
        translate([81.58 - 2.5, 40.00 - 3.5, 1.6])
            cube(size=[5.0, 7.0, 7.5], center=false);
    }

    // --- BOTTOM LAYER (B.Cu) COMPONENTS ---

    // 12. Microchip USB2517I 7-Port Automotive USB 2.0 Hub (U8: QFN-64 9x9mm)
    color("darkslategray")
        translate([41.03 - 4.5, 34.75 - 4.5, -1.0])
            cube(size=[9.0, 9.0, 1.0], center=false);

    // 13. TI LM5164-Q1 72V Step-Down (U1) & BQ24075 USV Controller (U3)
    color("black") {
        translate([7.31 - 2.5, 20.81 - 2.0, -1.5]) cube(size=[5.0, 4.0, 1.5], center=false);
        translate([48.09 - 2.0, 24.60 - 2.0, -1.0]) cube(size=[4.0, 4.0, 1.0], center=false);
        // TI TCAN334G CAN Transceiver (U6)
        translate([14.31 - 2.5, 44.56 - 2.0, -1.5]) cube(size=[5.0, 4.0, 1.5], center=false);
        // Bosch BMI270 6-Axis IMU (U5)
        translate([28.03 - 1.5, 36.15 - 1.5, -0.9]) cube(size=[3.0, 3.0, 0.9], center=false);
    }

    // 14. Hirose DM3D-SF MicroSD Push-Pull Card Slot (J2 on B.Cu at rear edge)
    color("lightgrey")
        translate([37.28 - 7.0, 6.90 - 7.0, -1.8])
            cube(size=[14.0, 14.5, 1.8], center=false);
}

// Standalone preview
dummy_main_pcb();
