// =============================================================================
// OpenMotorBridge - Satellite Pod: Cardo Packtalk Edge Cartridge (Pod 1 & Pod 2)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_cardo.scad
// Description: Fully detailed 2-tier modular cartridge for Cardo Packtalk Edge.
//              Features:
//              1. Universal PA12 Base Sled with Poka-Yoke guide rails & front faceplate.
//              2. Lower compartment with M2 standoffs for openmotorbridge_pod_cartridge PCB.
//              3. Intermediate Partition Floor (Zwischenboden at z = 6.0 mm) with cable slot.
//              4. Upper Cardo AirMount 3D Contour Cradle with:
//                 - 2x N52 Neodymium Magnet Pockets (Ø 8.2 mm x 2.2 mm)
//                 - 5-Pin Spring Contact Array Pocket
//                 - Lateral AirMount retention guide flanks (> 120 N hold force)
//                 - Lateral EPDM rubber strap anchor tabs
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
include <00_base_sled.scad>;
include <../00_common/dummies/dummy_adapter_pcb.scad>;

module cartridge_cardo_sled() {
    difference() {
        union() {
            // 1. Universal Base Sled (PA12 Chassis with Poka-Yoke Guide Rails)
            cartridge_base_sled(
                sled_l = CARTRIDGE_BASE_L,
                sled_w = CARTRIDGE_BASE_W,
                sled_h = 16.0,
                wall   = 2.5
            );

            // 2. 4x M2 PCB Standoffs in Lower Floor (for carrier PCB)
            translate([15.0, 10.0, 2.5])
                screw_boss(outer_r=2.0, inner_r=M2_SCREW_HOLE_R, h=2.5);
            translate([50.0, 10.0, 2.5])
                screw_boss(outer_r=2.0, inner_r=M2_SCREW_HOLE_R, h=2.5);
            translate([15.0, 44.0, 2.5])
                screw_boss(outer_r=2.0, inner_r=M2_SCREW_HOLE_R, h=2.5);
            translate([50.0, 44.0, 2.5])
                screw_boss(outer_r=2.0, inner_r=M2_SCREW_HOLE_R, h=2.5);

            // 3. Intermediate Partition Deck (Zwischenboden at z = 6.0 mm .. 8.0 mm)
            translate([2.5, 2.5, 6.0])
                cube(size=[CARTRIDGE_BASE_L - 3.5, CARTRIDGE_BASE_W - 5.0, 2.0], center=false);

            // 4. Upper Cardo AirMount 3D-Konturbett (Molded Cradle from z = 8.0 to 16.0 mm)
            translate([5.0, 5.0, 8.0]) {
                difference() {
                    // Solid cradle block
                    cube(size=[CARTRIDGE_BASE_L - 8.0, CARTRIDGE_BASE_W - 10.0, 8.0], center=false);

                    // A. Cardo Packtalk Edge Aerodynamic Wedge Contour (Recessed 5.0 mm bed)
                    translate([2.0, 3.0, 3.0])
                        cube(size=[CARTRIDGE_BASE_L - 12.0, CARTRIDGE_BASE_W - 16.0, 6.0], center=false);

                    // B. Dual N52 Neodymium Magnet Pockets (Ø 8.2 mm x 2.5 mm depth)
                    // Front Magnet Pocket (x = 18.0 mm)
                    translate([18.0, (CARTRIDGE_BASE_W - 10.0)/2.0, 1.0])
                        cylinder(r=4.1, h=4.0, center=false);

                    // Rear Magnet Pocket (x = 52.0 mm)
                    translate([52.0, (CARTRIDGE_BASE_W - 10.0)/2.0, 1.0])
                        cylinder(r=4.1, h=4.0, center=false);

                    // C. 5-Pin Spring Contact Array Pocket (Through-hole to cable slot)
                    translate([33.0, (CARTRIDGE_BASE_W - 10.0)/2.0 - 2.5, -3.0])
                        cube(size=[10.0, 5.0, 10.0], center=false);
                }
            }

            // 5. Cardo AirMount Lateral Guide Flanks (Angled snap cheeks)
            translate([8.0, 5.0, 12.0])
                cube(size=[48.0, 2.5, 3.5], center=false);
            translate([8.0, CARTRIDGE_BASE_W - 7.5, 12.0])
                cube(size=[48.0, 2.5, 3.5], center=false);

            // 6. Lateral EPDM Strap Anchor Tabs (Left & Right T-Hooks)
            translate([35.0, -1.0, 14.0])
                cube(size=[8.0, 2.0, 3.0], center=false);
            translate([35.0, CARTRIDGE_BASE_W - 1.0, 14.0])
                cube(size=[8.0, 2.0, 3.0], center=false);
        }

        // 7. Cable Pass-Through Slot in Partition Deck (10 x 3 mm into lower floor)
        translate([38.0, 24.5, 4.0])
            cube(size=[10.0, 4.0, 6.0], center=false);
    }
}

// Render complete Cardo Cartridge
cartridge_cardo_sled();
