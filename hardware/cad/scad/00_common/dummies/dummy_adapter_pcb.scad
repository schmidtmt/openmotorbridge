// =============================================================================
// OpenMotorBridge - Dummy 3D Model: Pod Cartridge Adapter PCB (Pod 1 & Pod 2)
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_adapter_pcb.scad
// Description: 3D model of the Cartridge Adapter PCB with DS2401 Silicon Serial
//              Number ID chip, Pogo Pin interface & Headset routing.
// =============================================================================

include <../parameters.scad>;

module dummy_adapter_pcb() {
    // 1. PCB Substrate (FR4 Green, 50 x 22 x 1.6 mm)
    color("forestgreen") {
        difference() {
            cube(size=[50.0, 22.0, 1.6], center=false);
            // 2x M2 Mounting Holes
            translate([4.0, 4.0, -0.1])  cylinder(r=1.1, h=2.0);
            translate([46.0, 4.0, -0.1]) cylinder(r=1.1, h=2.0);
        }
    }

    // 2. DS2401 Silicon Serial Number 1-Wire ID Chip (SOT-23)
    color("black")
        translate([12.0, 8.0, 1.6])
            cube(size=[3.0, 1.5, 1.0], center=false);

    // 3. 6-Pin Gold-Plated Pogo Pin Array (to Bulkhead)
    color("gold") {
        for (i = [0:5]) {
            translate([-1.0, 3.5 + i * 3.0, 0.5])
                rotate([0, 90, 0])
                    cylinder(r=0.6, h=3.0);
        }
    }

    // 4. Headset Ribbon Connector / Wiring Harness to Sena/Cardo Nest
    color("whitesmoke")
        translate([30.0, 6.0, 1.6])
            cube(size=[12.0, 10.0, 2.5], center=false);
}

// Preview standalone
dummy_adapter_pcb();
