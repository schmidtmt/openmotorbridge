// =============================================================================
// OpenMotorBridge - Dummy 3D Model: OMM Rear Transceiver PCB (Pod 3)
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_omm_transceiver_pcb.scad
// Description: Accurate 3D CAD model of the Rear Pod 3 PCBA (70 x 48 mm):
//              - 70 x 48 x 1.6 mm FR4 Substrate with 4x M2 Mounting Holes
//              - 6-Pin Horizontal Female Socket (PinSocket) mating into Pod Base
//              - 2x Pulse W3000 Ceramic Chip Antennas (GNSS top, LoRa bottom)
//              - Semtech SX1262 LoRa, u-blox MAX-M10S GNSS, ESP32-C3 MCU
// =============================================================================

include <../parameters.scad>;

module dummy_omm_transceiver_pcb() {
    // 1. PCB Substrate (FR4 Green, 70 x 48 x 1.6 mm)
    color("forestgreen") {
        difference() {
            cube(size=[70.0, 48.0, 1.6], center=false);
            // 4x M2 Mounting Holes (H1: 4,3 | H2: 66,3 | H3: 4,45 | H4: 66,45)
            translate([4.0, 3.0, -0.1])   cylinder(r=1.1, h=2.0, $fn=24);
            translate([66.0, 3.0, -0.1])  cylinder(r=1.1, h=2.0, $fn=24);
            translate([4.0, 45.0, -0.1])  cylinder(r=1.1, h=2.0, $fn=24);
            translate([66.0, 45.0, -0.1]) cylinder(r=1.1, h=2.0, $fn=24);
        }
    }

    // 2. 6-Pin Horizontal Female Socket (Black plastic housing projecting towards -X)
    // Sits on board edge at Y=17.65..30.35, projecting 6.0 mm over edge
    color("darkslategray")
        translate([-6.0, 16.5, 0.0])
            cube(size=[8.5, 15.2, 5.0], center=false);

    // 3. Pulse W3000 GNSS Ceramic Antenna (Top edge: 10.0 x 3.2 x 2.0 mm)
    color("white")
        translate([31.0, 0.5, 1.6])
            cube(size=[10.0, 3.2, 2.0], center=false);

    // 4. Pulse W3000 LoRa Ceramic Antenna (Bottom edge: 10.0 x 3.2 x 2.0 mm)
    color("white")
        translate([31.0, 44.3, 1.6])
            cube(size=[10.0, 3.2, 2.0], center=false);

    // 5. Semtech SX1262 LoRa Transceiver (QFN-24 4x4mm)
    color("black")
        translate([22.0, 33.0, 1.6])
            cube(size=[4.0, 4.0, 0.9], center=false);

    // 6. u-blox MAX-M10S GNSS Receiver (QFN-24 4x4mm)
    color("black")
        translate([22.0, 11.0, 1.6])
            cube(size=[4.0, 4.0, 0.9], center=false);

    // 7. ESP32-C3-WROOM-02 Wireless MCU Module
    color("silver")
        translate([50.0, 15.0, 1.6])
            cube(size=[18.0, 18.0, 3.2], center=false);
}

// Preview standalone
dummy_omm_transceiver_pcb();
