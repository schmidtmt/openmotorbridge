// =============================================================================
// OpenMotorBridge - Dummy 3D Model: OMM Rear Transceiver PCB (Pod 3)
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_omm_transceiver_pcb.scad
// Description: 3D model of the OMM Rear Transceiver PCB (ESP32-S3, SX1262 LoRa,
//              GNSS Multi-Constellation Engine, Ceramic Patch Antenna).
// =============================================================================

include <../parameters.scad>;

module dummy_omm_transceiver_pcb() {
    // 1. PCB Substrate (FR4 Green, 70 x 48 x 1.6 mm)
    color("forestgreen") {
        difference() {
            cube(size=[70.0, 48.0, 1.6], center=false);
            // 4x M2.5 Mounting Holes
            translate([4.0, 4.0, -0.1])   cylinder(r=1.35, h=2.0);
            translate([66.0, 4.0, -0.1])  cylinder(r=1.35, h=2.0);
            translate([4.0, 44.0, -0.1])  cylinder(r=1.35, h=2.0);
            translate([66.0, 44.0, -0.1]) cylinder(r=1.35, h=2.0);
        }
    }

    // 2. 25x25x4mm Ceramic GNSS Patch Antenna
    color("burlywood")
        translate([40.0, 11.5, 1.6])
            cube(size=[25.0, 25.0, 4.0], center=false);

    // Silver Metallized Patch Center Dot
    color("silver")
        translate([52.5, 24.0, 5.6])
            cylinder(r=2.0, h=0.2);

    // 3. SX1262 868 MHz LoRa RF Shield Can
    color("silver")
        translate([10.0, 6.0, 1.6])
            cube(size=[15.0, 15.0, 2.5], center=false);

    // 4. ESP32-S3 Wireless MCU Module
    color("darkslategray")
        translate([10.0, 26.0, 1.6])
            cube(size=[18.0, 18.0, 3.2], center=false);

    // 5. 6-Pin Gold-Plated Pogo-Pin Array (Rear Interface)
    color("gold") {
        for (i = [0:5]) {
            translate([-1.0, 16.5 + i * 3.0, 0.5])
                rotate([0, 90, 0])
                    cylinder(r=0.6, h=3.0);
        }
    }

    // 6. 2x Thermal Copper Stud Pads (under the PCB)
    color("darkorange") {
        translate([42.0, 24.0, -2.5]) cylinder(r=COPPER_STUD_R, h=2.5);
        translate([60.0, 24.0, -2.5]) cylinder(r=COPPER_STUD_R, h=2.5);
    }
}

// Preview standalone
dummy_omm_transceiver_pcb();
