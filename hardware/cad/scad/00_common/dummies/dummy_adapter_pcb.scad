// =============================================================================
// OpenMotorBridge - Dummy 3D Model: Pod Cartridge Adapter PCB (Pod 1 & Pod 2)
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_adapter_pcb.scad
// Description: 3D model of the Cartridge Carrier PCB (35.0 x 25.0 x 1.6 mm)
//              with 4x M2 mounting holes matching KiCad openmotorbridge_pod_cartridge.
// =============================================================================

include <../parameters.scad>;

module dummy_adapter_pcb() {
    // 1. PCB Substrate (FR4 Green, 35.0 x 25.0 x 1.6 mm with 2.0 mm chamfers)
    color("forestgreen") {
        difference() {
            cube(size=[35.0, 25.0, 1.6], center=false);
            // 4x M2 Mounting Holes (3.0mm from edges in X, 3.0mm in Y)
            translate([3.0, 3.0, -0.1])   cylinder(r=1.1, h=2.0);
            translate([3.0, 22.0, -0.1])  cylinder(r=1.1, h=2.0);
            translate([32.0, 3.0, -0.1])  cylinder(r=1.1, h=2.0);
            translate([32.0, 22.0, -0.1]) cylinder(r=1.1, h=2.0);
        }
    }

    // 2. WCH CH32V003 RISC-V MCU & 4x AO3400A MOSFETs (Rev 2.0 Smart Cartridge)
    color("black") {
        // MCU (QFN-20 3x3mm)
        translate([12.0, 11.0, 1.6])
            cube(size=[3.0, 3.0, 0.8], center=false);
        // 4x AO3400A MOSFET Driver Stages (SOT-23)
        translate([18.0, 5.0, 1.6])  cube(size=[2.9, 1.3, 1.0], center=false);
        translate([18.0, 8.0, 1.6])  cube(size=[2.9, 1.3, 1.0], center=false);
        translate([18.0, 14.0, 1.6]) cube(size=[2.9, 1.3, 1.0], center=false);
        translate([18.0, 17.0, 1.6]) cube(size=[2.9, 1.3, 1.0], center=false);
    }

    // 3. J1: 6-Pin Precision Horizontal Female Socket Strip (Mating to Pod-Base J1 Pins)
    // Black thermoplastic insulator body projecting -5.5mm over leading edge at X = 0
    color("darkslategray") {
        difference() {
            translate([-5.5, 4.8, 0.0])
                cube(size=[7.5, 15.4, 5.0], center=false);
            // 6x Contact Insertion Cavities on front face
            for (i = [0:5]) {
                translate([-5.6, 6.15 + i * 2.54 - 0.5, 1.5])
                    cube(size=[3.5, 1.0, 2.0], center=false);
            }
        }
    }
    // Internal gold contact leaves visible inside the socket apertures
    color("gold") {
        for (i = [0:5]) {
            translate([-4.0, 6.15 + i * 2.54, 2.5])
                cube(size=[2.0, 0.6, 1.2], center=true);
        }
    }

    // 4. J_ACT: 8-Pin JST-SH 1.0mm Horizontal Mechatronics Header (X = 26.0, Y = 14.0)
    color("whitesmoke")
        translate([24.0, 13.0, 1.6])
            cube(size=[4.5, 9.5, 2.2], center=false);

    // 5. J2: 6-Pin JST-SH 1.0mm Horizontal Audio/Power Header (X = 26.0, Y = 3.0)
    color("whitesmoke")
        translate([24.0, 2.5, 1.6])
            cube(size=[4.5, 7.5, 2.2], center=false);
}

// Preview standalone
dummy_adapter_pcb();

