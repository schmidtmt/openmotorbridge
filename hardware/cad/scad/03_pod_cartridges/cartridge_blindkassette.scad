// =============================================================================
// OpenMotorBridge - Satellite Pod: Leerkassette / Blindkassette (Staufach)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_blindkassette.scad
// Description: Empty cartridge / dry storage organizer:
//              - Base sled with floor insert tray sitting firmly at the bottom (am Boden at Z = 2.5 mm)
//              - Secured via 4x M2 stainless steel countersunk screws into sled floor bosses
//              - Rear EPDM contact seal block hermetically shielding the pod's pogo pins
//              - Continuous solid plastic storage bays: Key cradle, document bay, fuse slots
//              - 100% clean CAD: No confusing colored dummy blocks or floor cutouts
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <00_base_sled.scad>;
use <parts/03_insert_blindkassette.scad>;

module cartridge_blindkassette_assembly(exploded = false) {
    z_insert = exploded ? 16.0 : 2.5;
    z_screws = exploded ? 28.0 : 4.5;

    // 1. Universal Base Sled (Anthracite PA12)
    color("darkslategray", 0.92)
        cartridge_base_sled(
            sled_l     = CARTRIDGE_BASE_L,
            sled_w     = CARTRIDGE_BASE_W,
            sled_h     = CARTRIDGE_BASE_H,
            wall       = 2.5,
            show_latch = true
        );

    // 2. Rear EPDM Hermetic Contact Seal Block (at X = -0.5 .. 3.5 mm)
    // Firmly covers the sled contact window and seals against the pod bulkhead pogo pins
    color([0.12, 0.12, 0.14])
        translate([-0.5, CARTRIDGE_BASE_W/2.0 - 7.5, 1.5])
            cube([4.0, 15.0, 7.0]);

    // 3. Organizer Floor Insert Tray (Solid bottom plate am Boden at Z = 2.5 mm)
    color([0.24, 0.26, 0.28])
        translate([3.0, (CARTRIDGE_BASE_W - 52.0)/2.0, z_insert])
            cartridge_insert_blindkassette();

    // 4. Emergency Motorcycle Key (in Front Key Bay, silver key blade & bow)
    color("silver") {
        translate([16.0, CARTRIDGE_BASE_W/2.0, z_insert + 4.0]) {
            cube([20.0, 6.0, 1.8], center=true);
            translate([-10.0, 0, 0])
                cylinder(r=6.5, h=1.8, center=true, $fn=24);
        }
    }

    // 5. 4x M2 Stainless Steel Countersunk Fastening Screws
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
