// =============================================================================
// OpenMotorBridge - Satellite Pod: Sena 50S/60S Modular Cartridge (Pod 1 & Pod 2)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_sena.scad
// Description: Fully detailed 2-tier modular cartridge for Sena 50S & 60S headsets.
//              Features:
//              1. Universal PA12 Base Sled with Poka-Yoke rails & front faceplate.
//              2. Lower compartment with M2 standoffs for openmotorbridge_pod_cartridge PCB.
//              3. Intermediate Partition Floor (Zwischenboden at z = 6.0 mm) with cable slot.
//              4. Upper 3D Contour Cradle (Konturbett) with Sena negative shape,
//                 Jog-Dial relief recess, 7-pin Pogo contact pocket, top latch hook,
//                 and lateral EPDM rubber strap anchor tabs.
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
include <00_base_sled.scad>;
include <../00_common/dummies/dummy_adapter_pcb.scad>;

module cartridge_sena_sled() {
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

            // 4. Upper Sena 3D-Konturbett (Molded Cradle from z = 8.0 to 16.0 mm)
            translate([5.0, 5.0, 8.0]) {
                difference() {
                    // Solid cradle block
                    cube(size=[CARTRIDGE_BASE_L - 8.0, CARTRIDGE_BASE_W - 10.0, 8.0], center=false);

                    // A. Sena Ergonomic Main Body Contour (Recessed 5.0 mm bed)
                    translate([2.0, 2.0, 3.0])
                        cube(size=[CARTRIDGE_BASE_L - 12.0, CARTRIDGE_BASE_W - 14.0, 6.0], center=false);

                    // B. Sena Jog-Dial Wheel Pocket (Circular cutout at left flank)
                    translate([38.0, 2.0, 2.0])
                        cylinder(r=10.0, h=7.0, center=false);

                    // C. 7-Pin Pogo Contact Pocket (Through-hole to underfloor cable slot)
                    translate([18.0, 18.0, -3.0])
                        cube(size=[14.0, 5.0, 10.0], center=false);

                    // D. Top Antenna & Flip-Latch Clearance
                    translate([48.0, 15.0, 2.0])
                        cube(size=[12.0, 14.0, 7.0], center=false);
                }
            }

            // 5. Sena Bottom Retention Hook (Formschlüssige Haltenase at leading nose)
            translate([6.0, (CARTRIDGE_BASE_W - 12.0)/2.0, 11.0])
                cube(size=[3.0, 12.0, 3.5], center=false);

            // 6. Lateral EPDM Strap Anchor Tabs (Left & Right T-Hooks)
            translate([35.0, -1.0, 14.0])
                cube(size=[8.0, 2.0, 3.0], center=false);
            translate([35.0, CARTRIDGE_BASE_W - 1.0, 14.0])
                cube(size=[8.0, 2.0, 3.0], center=false);
        }

        // 7. Cable Pass-Through Slot in Partition Deck (10 x 3 mm into lower floor)
        translate([23.0, 23.0, 4.0])
            cube(size=[10.0, 4.0, 6.0], center=false);
    }
}

// Render complete Sena Cartridge
cartridge_sena_sled();
