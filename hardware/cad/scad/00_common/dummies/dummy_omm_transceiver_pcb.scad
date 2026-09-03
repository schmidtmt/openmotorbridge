// =============================================================================
// OpenMotorBridge - Dummy 3D Model: Compact OMM Rear Transceiver PCB (Pod 3)
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_omm_transceiver_pcb.scad
// Description: Accurate 3D CAD model of the compact Rear Pod 3 PCBA (55 x 48 mm):
//              - 55 x 48 x 1.6 mm FR4 Substrate with 4x M2 Mounting Holes
//              - 6-Pin Horizontal Female Socket centered at Y = 24.0 mm
//              - ESP32-C3-WROOM-02U (with U.FL micro-coax connector)
//              - Semtech SX1262 LoRa with U.FL connector
//              - u-blox MAX-M10S GNSS with U.FL connector
//              - 3x U.FL pigtail leads running to rear antenna bracket & SMA
// =============================================================================

include <../parameters.scad>;

module ufl_connector() {
    color("gold") {
        difference() {
            cube([2.0, 2.0, 1.25], center=true);
            cylinder(r=0.6, h=1.5, center=true, $fn=16);
        }
    }
    color("black")
        cylinder(r=0.2, h=1.0, center=true, $fn=12);
}

module dummy_omm_transceiver_pcb() {
    pcb_l = 55.0;
    pcb_w = 48.0;
    y_c   = pcb_w / 2.0; // 24.0 mm

    // 1. PCB Substrate (FR4 Green, 55 x 48 x 1.6 mm)
    color("forestgreen") {
        difference() {
            cube(size=[pcb_l, pcb_w, 1.6], center=false);
            // 4x M2 Mounting Holes concentric with sled standoffs (pitch: 46.0 x 19.0 mm)
            translate([4.5, y_c - 9.5, -0.1]) cylinder(r=1.1, h=2.0, $fn=24);
            translate([50.5, y_c - 9.5, -0.1]) cylinder(r=1.1, h=2.0, $fn=24);
            translate([4.5, y_c + 9.5, -0.1]) cylinder(r=1.1, h=2.0, $fn=24);
            translate([50.5, y_c + 9.5, -0.1]) cylinder(r=1.1, h=2.0, $fn=24);
        }
    }

    // 2. 6-Pin Horizontal Female Socket (Black plastic housing projecting towards -X)
    // Centered at Y = 24.0 mm, projecting 6.0 mm over front board edge
    color("darkslategray")
        translate([-6.0, y_c - 7.6, 0.0])
            cube(size=[8.5, 15.2, 5.0], center=false);

    // 3. Semtech SX1262 LoRa Transceiver (QFN-24 4x4mm)
    color("black")
        translate([16.0, y_c + 10.0, 1.6])
            cube(size=[4.0, 4.0, 0.9], center=false);

    // U.FL for LoRa 868 MHz
    translate([25.0, y_c + 12.0, 1.6 + 0.6])
        ufl_connector();

    // 4. u-blox MAX-M10S GNSS Receiver (QFN-24 4x4mm)
    color("black")
        translate([16.0, y_c - 14.0, 1.6])
            cube(size=[4.0, 4.0, 0.9], center=false);

    // U.FL for GNSS 1575 MHz
    translate([25.0, y_c - 12.0, 1.6 + 0.6])
        ufl_connector();

    // 5. ESP32-C3-WROOM-02U Wireless MCU Module (18.0 x 13.5 x 3.2 mm) with U.FL
    color("silver")
        translate([32.0, y_c - 6.75, 1.6])
            cube(size=[18.0, 13.5, 3.2], center=false);

    // U.FL for 2.4 GHz Mesh
    translate([46.0, y_c, 1.6 + 3.2 + 0.6])
        ufl_connector();

    // 6. 3x Flexible Micro-Coax Leads (1.13mm OD) trailing to the rear
    color("dimgray") {
        // LoRa Pigtail to rear
        translate([25.0, y_c + 12.0, 2.5])
            rotate([0, 90, 0])
                cylinder(r=0.55, h=pcb_l - 25.0 + 5.0, $fn=12);
        // GNSS Pigtail to rear
        translate([25.0, y_c - 12.0, 2.5])
            rotate([0, 90, 0])
                cylinder(r=0.55, h=pcb_l - 25.0 + 5.0, $fn=12);
        // 2.4 GHz Pigtail to rear
        translate([46.0, y_c, 5.0])
            rotate([0, 90, 0])
                cylinder(r=0.55, h=pcb_l - 46.0 + 5.0, $fn=12);
    }
}

// Preview standalone
dummy_omm_transceiver_pcb();
