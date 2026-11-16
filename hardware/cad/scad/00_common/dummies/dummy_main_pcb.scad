// =============================================================================
// OpenMotorBridge - Dummy 3D Model: Main Board PCB (PCBA 01 Rev 10.0)
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_main_pcb.scad
// Description: Accurate 3D representation of the central openMotorBridge
//              mainboard (PCBA 01: 85.0 x 55.0 x 1.6 mm, 4 layers ENIG)
//              with all v10 ICs, vertical connectors, and antenna ports.
//
// COORDINATE SYSTEM CONVENTION (OpenSCAD Cartesian):
// - X: 0.0 to 85.0 mm (West to East)
// - Y: 0.0 to 55.0 mm (South [Front Wall / Connectors] to North [Rear Wall / Antennas])
//   * Y = 0..10 mm (SOUTH): J1 (Bordnetz 6P), SW1 (Button), J6 (Periphery 16P), J3 (USB-C), D1 (Status LED)
//   * Y = 40..55 mm (NORTH): ANT1 (LoRa U.FL), U2 (ESP32-S31 U.FL), J2 (MicroSD Slot), U10 (SX1262)
//   * X = 80..85 mm (EAST): J5 (Battery 4P at Y = 35.0), J7 (Reserve USB 4P at Y = 25.0)
// =============================================================================

include <../parameters.scad>;

module dummy_main_pcb() {
    // 1. PCB Substrate (FR4 4-Layer High-TG150 Green ENIG: 85.0 x 55.0 x 1.6 mm)
    color("forestgreen") {
        difference() {
            cube(size=[85.0, 55.0, 1.6], center=false);
            // 4x M2.5 / M3 Mounting Holes (offset 4.0 mm: 77.0 x 47.0 mm pitch)
            translate([4.0, 4.0, -0.5]) cylinder(r=1.5, h=2.6, $fn=24);
            translate([81.0, 4.0, -0.5]) cylinder(r=1.5, h=2.6, $fn=24);
            translate([4.0, 51.0, -0.5]) cylinder(r=1.5, h=2.6, $fn=24);
            translate([81.0, 51.0, -0.5]) cylinder(r=1.5, h=2.6, $fn=24);
        }
    }

    // --- NORTH / REAR COMPONENTS (Y = 40..55 mm) ---

    // 2. Main Controller: ESP32-S31-WROOM-1U (U2: 18.0 x 19.2 x 3.2 mm)
    // KiCad: X = 37.28, Y_cad = 55.0 - 10.06 = 44.94 mm
    color("silver")
        translate([37.28 - 9.0, 44.94 - 9.6, 1.6])
            cube(size=[18.0, 19.2, 3.2], center=false);
    color("gold")
        translate([37.28 + 6.0, 44.94 + 7.0, 1.6 + 3.2])
            cylinder(r=1.1, h=1.0, $fn=16); // U.FL Port on S31

    // 3. Dedicated Helmet Audio SoC: Qualcomm QCC3084 BT 5.4 (U9: 13.0 x 18.0 x 2.8 mm)
    // KiCad: X = 66.48, Y_cad = 55.0 - 19.65 = 35.35 mm
    color([0.15, 0.40, 0.55])
        translate([66.48 - 6.5, 35.35 - 9.0, 1.6])
            cube(size=[13.0, 18.0, 2.6], center=false);
    // Integrated Ceramic Chip Antenna
    color("whitesmoke")
        translate([66.48 - 4.5, 35.35 + 6.0, 1.6 + 2.6])
            cube(size=[9.0, 3.0, 1.0], center=false);

    // 4. Semtech SX1262 LoRa 868 MHz Transceiver (U10: 4.0 x 4.0 mm) & ANT1 U.FL
    // KiCad: X = 52.53, Y_cad = 55.0 - 2.89 = 52.11 mm
    color("darkslategray")
        translate([52.53 - 2.0, 52.11 - 2.0, 1.6])
            cube(size=[4.0, 4.0, 1.0], center=false);
    color("gold")
        translate([60.81, 52.10, 1.6])
            cylinder(r=1.2, h=1.25, $fn=16); // ANT1 (U.FL for LoRa FXP895)

    // 5. LM5164-Q1 Power Choke L1 (12.0 x 12.0 x 6.0 mm)
    // KiCad: X = 8.78, Y_cad = 55.0 - 31.15 = 23.85 mm
    color([0.25, 0.25, 0.28])
        translate([8.78 - 6.0, 23.85 - 6.0, 1.6])
            cube(size=[12.0, 12.0, 6.0], center=false); // 47µH Power Inductor

    // --- SOUTH / FRONT EDGE CONNECTORS (Y = 0..10 mm) ---

    // 6. Header J1: Molex Micro-Lock Plus 1.25mm 6-Pin Vertikal (Bordnetz & CAN)
    // KiCad: X = 16.16, Y_cad = 55.0 - 51.90 = 3.10 mm
    color("ivory")
        translate([16.16 - 4.5, 3.10 - 2.5, 1.6])
            cube(size=[9.0, 5.0, 7.5], center=false);

    // 7. Push-Button SW1 (Pairing / Reset: Alps SKRK)
    // KiCad: X = 28.43, Y_cad = 55.0 - 51.65 = 3.35 mm
    color("crimson")
        translate([28.43 - 2.25, 3.35 - 2.25, 1.6])
            cube(size=[4.5, 4.5, 2.5], center=false);

    // 8. Header J6: Molex Micro-Lock Plus 16-Pin 2x08 Vertikal (4 Autarke OMB-Systemstränge)
    // KiCad: X = 40.78, Y_cad = 55.0 - 50.65 = 4.35 mm
    color("ivory")
        translate([40.78 - 6.7, 4.35 - 3.2, 1.6])
            cube(size=[13.4, 6.4, 6.5], center=false);

    // 9. Receptacle J3: USB Type-C 16-Pin Service & Flash Port (HRO TYPE-C-31-M-12)
    // KiCad: X = 62.78, Y_cad = 55.0 - 50.90 = 4.10 mm
    color("silver")
        translate([62.78 - 4.5, 4.10 - 3.5, 1.6])
            cube(size=[9.0, 7.5, 3.2], center=false);

    // 10. Status LED D1 (WS2812B RGB directly to the right of J3 along front edge)
    // Located at X = 72.0, Y = 3.35 mm (directly behind front light pipe window)
    color("cyan")
        translate([72.0 - 1.0, 3.35 - 1.0, 1.6])
            cube(size=[2.0, 2.0, 0.8], center=false);

    // --- EAST / SIDE EDGE HEADERS (X = 80..85 mm) ---

    // 11. Header J5: USV-Akku & NTC (Molex Micro-Lock Plus 4-Pin Vertikal)
    // KiCad: X = 81.58, Y_cad = 55.0 - 20.00 = 35.00 mm
    color("ivory")
        translate([81.58 - 2.5, 35.00 - 3.5, 1.6])
            cube(size=[5.0, 7.0, 7.5], center=false);

    // 12. Header J7: Reserve USB Port 7 (Molex Micro-Lock Plus 4-Pin Vertikal)
    // Shifted to the former J4 position: X = 81.58, Y_cad = 55.0 - 30.00 = 25.00 mm
    color("ivory")
        translate([81.58 - 2.5, 25.00 - 3.5, 1.6])
            cube(size=[5.0, 7.0, 7.5], center=false);

    // --- BOTTOM LAYER (B.Cu) COMPONENTS ---

    // 13. Microchip USB2517I 7-Port Automotive USB 2.0 Hub (U8: QFN-64 9x9mm)
    // KiCad: X = 41.03, Y_cad = 55.0 - 34.75 = 20.25 mm
    color("darkslategray")
        translate([41.03 - 4.5, 20.25 - 4.5, -1.0])
            cube(size=[9.0, 9.0, 1.0], center=false);

    // 14. TI LM5164-Q1 72V Step-Down (U1) & BQ24075 USV Controller (U4)
    color("black") {
        translate([7.31 - 2.5, 34.19 - 2.0, -1.5]) cube(size=[5.0, 4.0, 1.5], center=false);
        translate([48.09 - 2.0, 30.40 - 2.0, -1.0]) cube(size=[4.0, 4.0, 1.0], center=false);
        // TI TCAN334G CAN Transceiver (U6)
        translate([14.31 - 2.5, 10.44 - 2.0, -1.5]) cube(size=[5.0, 4.0, 1.5], center=false);
        // Bosch BMI270 6-Axis IMU (U5)
        translate([28.03 - 1.5, 18.85 - 1.5, -0.9]) cube(size=[3.0, 3.0, 0.9], center=false);
    }

    // 15. Hirose DM3D-SF MicroSD Push-Pull Card Slot (J2 on B.Cu at North / rear edge)
    // KiCad: X = 37.28, Y_cad = 55.0 - 6.90 = 48.10 mm
    color("lightgrey")
        translate([37.28 - 7.0, 48.10 - 7.0, -1.8])
            cube(size=[14.0, 14.5, 1.8], center=false);
}

// Standalone preview
dummy_main_pcb();
