// =============================================================================
// OpenMotorBridge - Satellite Pod: Leerkassette / Blindkassette (Staufach)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_blindkassette.scad
// Description: Empty cartridge / dry storage organizer:
//              - Base sled with floor insert tray sitting firmly at the bottom (am Boden at Z = 2.5 mm)
//              - Secured via 4x M2 stainless steel countersunk screws into sled floor bosses
//              - Dedicated storage bays: Emergency motorcycle key, documents/cash, backup fuses
//              - 100% consistent with serial cartridge family (slides into IP67 pod tunnel)
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <00_base_sled.scad>;
use <parts/03_insert_blindkassette.scad>;

module cartridge_blindkassette_assembly(exploded = false) {
    z_insert = exploded ? 16.0 : 2.5;
    z_screws = exploded ? 28.0 : 4.5;
    z_items  = z_insert + 2.5;

    // 1. Universal Base Sled (Anthracite PA12)
    color("darkslategray", 0.92)
        cartridge_base_sled(
            sled_l     = CARTRIDGE_BASE_L,
            sled_w     = CARTRIDGE_BASE_W,
            sled_h     = CARTRIDGE_BASE_H,
            wall       = 2.5,
            show_latch = true
        );

    // 2. Organizer Floor Insert Tray (Sitting on sled floor, am Boden!)
    color([0.22, 0.24, 0.26])
        translate([3.0, (CARTRIDGE_BASE_W - 52.0)/2.0, z_insert])
            cartridge_insert_blindkassette();

    // 3. Stored Items inside Organizer Bays
    // A. Emergency Motorcycle Key (in Front Bay)
    color("silver") {
        translate([16.0, CARTRIDGE_BASE_W/2.0, z_items + 2.5]) {
            cube([22.0, 7.0, 2.0], center=true);
            translate([-11.0, 0, 0])
                cylinder(r=7.0, h=2.0, center=true, $fn=24);
        }
    }

    // B. Rolled / Folded Vehicle Registration Papers (in Middle Bay)
    color([0.9, 0.9, 0.85]) {
        translate([66.0, CARTRIDGE_BASE_W/2.0, z_items + 2.0])
            cube([44.0, 28.0, 3.5], center=true);
    }

    // C. Emergency Mini-Blade Fuses (10A Red & 15A Blue in Rear Bay)
    color("red")
        translate([110.0, CARTRIDGE_BASE_W/2.0 - 6.0, z_items + 4.0])
            cube([9.0, 3.2, 7.0], center=true);
    color([0.1, 0.5, 0.9])
        translate([110.0, CARTRIDGE_BASE_W/2.0 + 6.0, z_items + 4.0])
            cube([9.0, 3.2, 7.0], center=true);

    // 4. 4x M2 Stainless Steel Countersunk Fastening Screws
    color("silver") {
        translate([6.5, 6.0, z_screws])
            cylinder(r=1.8, h=2.0, center=false, $fn=16);
        translate([CARTRIDGE_BASE_L - 6.5, 6.0, z_screws])
            cylinder(r=1.8, h=2.0, center=false, $fn=16);
        translate([6.5, CARTRIDGE_BASE_W - 6.0, z_screws])
            cylinder(r=1.8, h=2.0, center=false, $fn=16);
        translate([CARTRIDGE_BASE_L - 6.5, CARTRIDGE_BASE_W - 6.0, z_screws])
            cylinder(r=1.8, h=2.0, center=false, $fn=16);
    }
}

// Standalone assembly render
cartridge_blindkassette_assembly(exploded = false);
