// =============================================================================
// OpenMotorBridge - Dummy 3D Model: Main Board PCB (PCBA 01 Rev 10.0)
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_main_pcb.scad
// Description: Accurate 3D representation of the central openMotorBridge
//              mainboard (PCBA 01: 85.0 x 55.0 x 1.6 mm, 4 layers ENIG)
//              with all v10 ICs, vertical connectors, and triple antenna ports:
//              - ANT1: LoRa 868 MHz (Hirose U.FL at X=60.81, Y=52.10)
//              - ANT2: Helmet Audio BT 5.4 (Hirose U.FL at X=68.81, Y=52.85)
//              - ANT3: BLE 2.4 GHz (Johanson 2450AT18 Ceramic Chip at X=2.58, Y=38.60)
//
// COORDINATE SYSTEM CONVENTION (OpenSCAD Cartesian):
// - X: 0.0 to 85.0 mm (West to East)
// - Y: 0.0 to 55.0 mm (South [Front Wall / Connectors] to North [Rear Wall / Antennas])
//   * Y = 0..10 mm (SOUTH): J1 (Bordnetz 6P), SW1 (Button), J6 (Periphery 16P), J3 (USB-C), D1 (Status LED)
//   * Y = 40..55 mm (NORTH): ANT1 (LoRa U.FL), ANT2 (Helmaudio U.FL), U2 (ESP32-S31), U10 (SX1262)
//   * X = 0..5 mm (WEST): ANT3 (Johanson Ceramic Chip Antenna for BLE at X=2.58, Y=38.60)
//   * X = 75..85 mm (EAST): J5 (Battery 4P at Y = 35.0), J7 (Reserve USB 4P at Y = 25.0), J2 (MicroSD Slot on B.Cu at Y = 16.60)
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

    // --- NORTH / REAR COMPONENTS & DUAL U.FL PORTS (Y = 40..55 mm) ---

    // 2. Main Controller: ESP32-S31-WROOM-1U (U2: 18.0 x 19.2 x 3.2 mm)
    // KiCad: X = 37.28, Y_cad = 44.94 mm
    color("silver")
        translate([37.28 - 9.0, 44.94 - 9.6, 1.6])
            cube(size=[18.0, 19.2, 3.2], center=false);

    // 3. Dedicated Helmet Audio SoC: Qualcomm QCC3084 BT 5.4 (U9: 13.0 x 18.0 x 2.6 mm)
    // KiCad: X = 66.48, Y_cad = 35.35 mm (Routes RF via Pin 15 to ANT2 U.FL)
    color([0.15, 0.40, 0.55])
        translate([66.48 - 6.5, 35.35 - 9.0, 1.6])
            cube(size=[13.0, 18.0, 2.6], center=false);

    // 4. Semtech SX1262 LoRa 868 MHz Transceiver (U10: 4.0 x 4.0 x 1.0 mm)
    // KiCad: X = 52.53, Y_cad = 52.11 mm
    color("darkslategray")
        translate([52.53 - 2.0, 52.11 - 2.0, 1.6])
            cube(size=[4.0, 4.0, 1.0], center=false);

    // 5. ANT1: LoRa 868 MHz Hirose U.FL Receptacle (Taoglas FXP895 flex cable connection)
    // KiCad: X = 60.81, Y_cad = 52.10 mm
    color("gold") {
        translate([60.81 - 1.5, 52.10 - 1.5, 1.6])
            cube(size=[3.0, 3.0, 1.25], center=false);
        translate([60.81, 52.10, 1.6 + 1.25])
            cylinder(r=0.9, h=0.6, $fn=16);
    }
    // 50 Ohm CPW RF Microstrip from U10 to ANT1
    color("gold")
        translate([52.53 + 2.0, 52.10 - 0.25, 1.6])
            cube(size=[60.81 - (52.53 + 2.0) - 1.5, 0.5, 0.05], center=false);

    // 6. ANT2: Helmet Audio BT 5.4 Hirose U.FL Receptacle (Taoglas FXP73 flex cable connection)
    // Placed right next to ANT1: KiCad X = 68.81, Y_cad = 52.85 mm, rotated 90°
    color("gold") {
        translate([68.81 - 1.5, 52.85 - 1.5, 1.6])
            cube(size=[3.0, 3.0, 1.25], center=false);
        translate([68.81, 52.85, 1.6 + 1.25])
            cylinder(r=0.9, h=0.6, $fn=16);
    }
    // 50 Ohm CPW RF Microstrip from U9 to ANT2
    color("gold")
        translate([66.48 - 0.25, 35.35 + 9.0, 1.6])
            cube(size=[0.5, 52.85 - (35.35 + 9.0) - 1.5, 0.05], center=false);

    // --- WEST / LEFT EDGE ON-BOARD CERAMIC CHIP ANTENNA (X = 0..5 mm) ---

    // 7. ANT3: On-Board Johanson 2450AT18D0100 2.4 GHz Ceramic Chip Antenna for ESP32-S31 BLE
    // KiCad: X = 2.58, Y_cad = 38.60 mm, rotated 180° (feed facing inward to MCU, 2.58 mm edge clearance)
    // Dimensions: 3.2 x 1.6 x 1.3 mm (1206 footprint)
    translate([2.58, 38.60, 1.6]) {
        // Ceramic body
        color("ghostwhite")
            translate([-1.6, -0.8, 0])
                cube(size=[3.2, 1.6, 1.3], center=false);
        // Solder termination end caps
        color("silver") {
            translate([-1.6, -0.8, 0]) cube(size=[0.5, 1.6, 1.3], center=false); // GND terminal (facing edge)
            translate([1.1, -0.8, 0]) cube(size=[0.5, 1.6, 1.3], center=false);  // Feed terminal (facing MCU)
        }
    }
    // RF Feed Trace from ESP32-S31 to ANT3
    color("gold")
        translate([2.58 + 1.6, 38.60 - 0.25, 1.6])
            cube(size=[37.28 - 9.0 - (2.58 + 1.6), 0.5, 0.05], center=false);

    // --- POWER STAGE & ACTUATOR SWITCHES (X = 0..25 mm & X = 55..75 mm) ---

    // 8. LM5164-Q1 Power Choke L1 (Sunlord MWSA1206S-470: 12.0 x 12.0 x 6.0 mm)
    // KiCad: X = 8.78, Y_cad = 23.85 mm
    color([0.25, 0.25, 0.28])
        translate([8.78 - 6.0, 23.85 - 6.0, 1.6])
            cube(size=[12.0, 12.0, 6.0], center=false); // 47µH High-Current Inductor

    // 9. U12: TI TPS4H160BQPWPRQ1 Quad Smart High-Side Power Switch (HTSSOP-28: 9.7 x 4.4 x 1.2 mm)
    // KiCad: X = 62.06, Y_cad = 20.70 mm
    color("darkslategray")
        translate([62.06 - 4.85, 20.70 - 2.2, 1.6])
            cube(size=[9.7, 4.4, 1.2], center=false);

    // --- SOUTH / FRONT EDGE CONNECTORS (Y = 0..10 mm) ---

    // 10. Header J1: Molex Micro-Lock Plus 1.25mm 6-Pin Vertikal (Bordnetz & CAN)
    // KiCad: X = 16.16, Y_cad = 3.10 mm
    color("ivory")
        translate([16.16 - 4.5, 3.10 - 2.5, 1.6])
            cube(size=[9.0, 5.0, 7.5], center=false);

    // 11. Push-Button SW1 (Pairing / Reset: Alps SKRK)
    // KiCad: X = 28.43, Y_cad = 3.35 mm
    color("crimson")
        translate([28.43 - 2.25, 3.35 - 2.25, 1.6])
            cube(size=[4.5, 4.5, 2.5], center=false);

    // 12. Header J6: Molex Micro-Lock Plus 16-Pin 2x08 Vertikal (4 Autarke OMB-Systemstränge)
    // KiCad: X = 40.78, Y_cad = 4.35 mm
    color("ivory")
        translate([40.78 - 6.7, 4.35 - 3.2, 1.6])
            cube(size=[13.4, 6.4, 6.5], center=false);

    // 13. Receptacle J3: USB Type-C 16-Pin Service & Flash Port (HRO TYPE-C-31-M-12)
    // KiCad: X = 62.78, Y_cad = 4.10 mm
    color("silver")
        translate([62.78 - 4.5, 4.10 - 3.5, 1.6])
            cube(size=[9.0, 7.5, 3.2], center=false);

    // 14. Status LED D1 (WS2812B RGB directly to the right of J3 along front edge)
    // KiCad: X = 71.28, Y_cad = 3.35 mm (directly behind front light pipe window)
    color("cyan")
        translate([71.28 - 1.0, 3.35 - 1.0, 1.6])
            cube(size=[2.0, 2.0, 0.8], center=false);

    // --- EAST / SIDE EDGE HEADERS (X = 80..85 mm) ---

    // 15. Header J5: USV-Akku & NTC (Molex Micro-Lock Plus 4-Pin Vertikal)
    // KiCad: X = 81.58, Y_cad = 35.00 mm
    color("ivory")
        translate([81.58 - 2.5, 35.00 - 3.5, 1.6])
            cube(size=[5.0, 7.0, 7.5], center=false);

    // 16. Header J7: Reserve USB Port 7 (Molex Micro-Lock Plus 4-Pin Vertikal)
    // KiCad: X = 81.58, Y_cad = 25.00 mm
    color("ivory")
        translate([81.58 - 2.5, 25.00 - 3.5, 1.6])
            cube(size=[5.0, 7.0, 7.5], center=false);

    // --- BOTTOM LAYER (B.Cu) COMPONENTS ---

    // 17. Microchip USB2517I 7-Port Automotive USB 2.0 Hub (U8: QFN-64 9x9mm)
    // KiCad: X = 41.03, Y_cad = 20.25 mm
    color("darkslategray")
        translate([41.03 - 4.5, 20.25 - 4.5, -1.0])
            cube(size=[9.0, 9.0, 1.0], center=false);

    // 18. TI LM5164-Q1 72V Step-Down (U1), BQ24075 USV Controller (U4), ES8388 Codec (U3)
    color("black") {
        translate([7.31 - 2.5, 34.19 - 2.0, -1.5]) cube(size=[5.0, 4.0, 1.5], center=false);  // U1 LM5164
        translate([64.43 - 1.5, 40.41 - 1.5, -1.0]) cube(size=[3.0, 3.0, 1.0], center=false); // U4 BQ24075
        translate([48.09 - 2.0, 30.40 - 2.0, -1.0]) cube(size=[4.0, 4.0, 1.0], center=false); // U3 ES8388
        translate([14.31 - 2.5, 10.44 - 2.0, -1.5]) cube(size=[5.0, 4.0, 1.5], center=false); // U6 TCAN334G
        translate([28.03 - 1.5, 18.85 - 1.5, -0.9]) cube(size=[3.0, 3.0, 0.9], center=false); // U5 BMI270
    }

    // 19. Hirose DM3D-SF MicroSD Push-Pull Card Slot (J2 on B.Cu relocated to East edge)
    // KiCad: X = 193.50, Y = 110.25, Rot = 90 deg -> SCAD: X_cad = 78.28, Y_cad = 16.60 mm
    color("lightgrey")
        translate([78.28 - 7.25, 16.60 - 7.0, -1.8])
            cube(size=[14.5, 14.0, 1.8], center=false);
}

// Standalone preview
dummy_main_pcb();
