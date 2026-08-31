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

    // 2. DS2401 Silicon Serial Number 1-Wire ID Chip (SOT-23)
    color("black")
        translate([15.0, 12.5, 1.6])
            cube(size=[3.0, 1.5, 1.0], center=false);

    // 3. 6-Pin Gold-Plated Pogo Pin / Mating Array at leading edge (X = 0)
    color("gold") {
        for (i = [0:5]) {
            translate([-1.0, 6.15 + i * 2.54, 0.8])
                rotate([0, 90, 0])
                    cylinder(r=0.6, h=3.0);
        }
    }

    // 4. JST-SH 6-Pin Horizontal Connector to Sena/Cardo Nest (X = 26.5)
    color("whitesmoke")
        translate([24.0, 7.5, 1.6])
            cube(size=[5.0, 10.0, 2.0], center=false);
}

// Preview standalone
dummy_adapter_pcb();
