// =============================================================================
// OpenMotorBridge - Dummy 3D Model: OMM Rear Transceiver PCB (Pod 3)
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_omm_transceiver_pcb.scad
// Description: Accurate 3D CAD model of the enlarged Rear Pod 3 PCBA (110 x 52 mm):
//              - 110 x 52 x 1.6 mm FR4 Substrate with 4x M2 Mounting Holes
//              - 6-Pin Horizontal Female Socket (PinSocket) perfectly centered at Y = 26.0 mm
//              - 3x Pulse W3000 Ceramic Chip Antennas (ANT2 GNSS top, ANT1 LoRa bottom, ANT3 2.4G right)
//              - Semtech SX1262 LoRa, u-blox MAX-M10S GNSS, ESP32-C3 MCU
//              - 3x Murata MM8030 Mechanical RF Switch Receptacles (J3, J4, J5)
//              - Routing path for internal RF coaxial pigtail to SMA bulkhead
// =============================================================================

include <../parameters.scad>;

module mm8030_rf_switch() {
    color("gold") {
        difference() {
            // Main gold-plated metal shell (2.1 x 2.0 x 0.9 mm)
            cube([2.1, 2.0, 0.9], center=true);
            // Internal coaxial probe cavity
            translate([0, 0, 0.1])
                cylinder(r=0.45, h=1.0, center=true, $fn=16);
        }
    }
    // Center spring contact pin
    color("black")
        translate([0, 0, 0.05])
            cylinder(r=0.15, h=0.8, center=true, $fn=12);
}

module dummy_omm_transceiver_pcb() {
    // 1. PCB Substrate (FR4 Green, 110 x 52 x 1.6 mm)
    color("forestgreen") {
        difference() {
            cube(size=[110.0, 52.0, 1.6], center=false);
            // 4x M2 Mounting Holes concentric with sled corner posts
            // Pitch: 103.0 x 46.0 mm (H1: 3.5, 3.0 | H2: 106.5, 3.0 | H3: 3.5, 49.0 | H4: 106.5, 49.0)
            translate([3.5, 3.0, -0.1])    cylinder(r=1.1, h=2.0, $fn=24);
            translate([106.5, 3.0, -0.1])  cylinder(r=1.1, h=2.0, $fn=24);
            translate([3.5, 49.0, -0.1])   cylinder(r=1.1, h=2.0, $fn=24);
            translate([106.5, 49.0, -0.1]) cylinder(r=1.1, h=2.0, $fn=24);
        }
    }

    // 2. 6-Pin Horizontal Female Socket (Black plastic housing projecting towards -X)
    // Centered at Y = 26.0 mm (Pin 1 at Y = 19.65 mm, Pin 6 at Y = 32.35 mm), projecting 6.0 mm over rear board edge
    color("darkslategray")
        translate([-6.0, 26.0 - 6.35 - 1.25, 0.0])
            cube(size=[8.5, 15.2, 5.0], center=false);

    // 3. ANT2: Pulse W3000 GNSS Ceramic Antenna (Top edge: 10.0 x 3.2 x 2.0 mm)
    color("white")
        translate([37.05, 1.0, 1.6])
            cube(size=[10.0, 3.2, 2.0], center=false);

    // 4. ANT1: Pulse W3000 LoRa Ceramic Antenna (Bottom edge: 10.0 x 3.2 x 2.0 mm)
    color("white")
        translate([36.8, 52.0 - 4.2, 1.6])
            cube(size=[10.0, 3.2, 2.0], center=false);

    // 5. Semtech SX1262 LoRa Transceiver (QFN-24 4x4mm)
    color("black")
        translate([24.0, 35.0, 1.6])
            cube(size=[4.0, 4.0, 0.9], center=false);

    // 6. u-blox MAX-M10S GNSS Receiver (QFN-24 4x4mm)
    color("black")
        translate([24.0, 13.0, 1.6])
            cube(size=[4.0, 4.0, 0.9], center=false);

    // 7. ESP32-C3-WROOM-02 Wireless MCU Module (18.0 x 18.0 x 3.2 mm)
    color("silver")
        translate([56.8, 14.0, 1.6])
            cube(size=[18.0, 18.0, 3.2], center=false);

    // 8. 3x Murata MM8030 Mechanical RF Switch Receptacles (J3, J4, J5)
    // J5: GNSS RF Switch (X = 39.85 mm, Y = 7.75 mm)
    translate([39.85, 7.75, 1.6 + 0.45])
        mm8030_rf_switch();

    // J4: 868 MHz LoRa RF Switch (X = 34.25 mm, Y = 46.05 mm)
    translate([34.25, 46.05, 1.6 + 0.45])
        mm8030_rf_switch();

    // ANT3: Pulse W3000 2.4 GHz Ceramic Antenna (X = 86.0 mm, Y = 22.0 mm)
    color("white")
        translate([86.0, 22.0 - 1.6, 1.6])
            cube(size=[10.0, 3.2, 2.0], center=false);

    // J3: 2.4 GHz Mesh RF Switch (X = 98.35 mm, Y = 22.0 mm, default connected to SMA)
    translate([98.35, 22.0, 1.6 + 0.45])
        mm8030_rf_switch();

    // 9. Coaxial Pigtail (RG178, 1.8mm OD) from J3 (2.4 GHz default) curving to front SMA
    color("dimgray") {
        translate([98.35, 22.0, 2.8])
            rotate([0, 90, 0])
                cylinder(r=0.9, h=10.0, $fn=16);
    }
}

// Preview standalone
dummy_omm_transceiver_pcb();
