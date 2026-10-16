// =============================================================================
// OpenMotorBridge - Satellite Pod: Waterproof Blindkassette (IP67 Dry Box)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_blindkassette.scad
// Description: Waterproof dummy plug & dry storage cassette:
//              - Full interior usable as watertight storage (spare key, documents, fuses)
//              - Continuous 22.0 mm deep organizer storage tub (NO false floors)
//              - Perimeter high-visibility silicone sealing gasket
//              - Flush-sealing top lid with stainless steel M2 countersunk screws
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <00_base_sled.scad>;
use <parts/03_insert_blindkassette.scad>;

module cartridge_blindkassette_assembly(exploded = false) {
    z_tub    = 2.5;
    z_gasket = exploded ? 32.0 : 24.5;
    z_lid    = exploded ? 40.0 : 26.5;
    z_screws = exploded ? 50.0 : 28.5;

    // 1. Universal Base Sled (Anthracite PA12)
    color("darkslategray", 0.92)
        cartridge_base_sled(
            sled_l     = CARTRIDGE_BASE_L,
            sled_w     = CARTRIDGE_BASE_W,
            sled_h     = CARTRIDGE_BASE_H,
            wall       = 2.5,
            show_latch = true
        );

    // 2. Deep Watertight Organizer Tub (22.0 mm continuous deep cavity, no false floors!)
    color([0.22, 0.24, 0.26])
        translate([3.0, (CARTRIDGE_BASE_W - 52.0)/2.0, z_tub])
            cartridge_dry_box_tub();

    // 3. Stored Items inside Dry Box (Visible in open / inspection views)
    // A. Emergency Motorcycle Key (in Front Bay)
    color("silver") {
        translate([16.0, CARTRIDGE_BASE_W/2.0, z_tub + 4.5]) {
            cube([22.0, 7.0, 2.0], center=true);
            translate([-11.0, 0, 0])
                cylinder(r=7.0, h=2.0, center=true, $fn=24);
        }
    }
    // B. Emergency Mini-Blade Fuses (10A Red & 15A Blue in Rear Bay)
    color("red")
        translate([109.0, CARTRIDGE_BASE_W/2.0 - 6.0, z_tub + 5.0])
            cube([9.0, 3.2, 7.0], center=true);
    color([0.1, 0.5, 0.9])
        translate([109.0, CARTRIDGE_BASE_W/2.0 + 6.0, z_tub + 5.0])
            cube([9.0, 3.2, 7.0], center=true);

    // 4. High-Visibility Silicone Sealing Gasket (Neon Orange)
    color([1.0, 0.45, 0.1, 0.9]) {
        translate([3.5, (CARTRIDGE_BASE_W - 52.0)/2.0, z_gasket]) {
            difference() {
                cube([CARTRIDGE_BASE_L - 7.0, 52.0, 1.8]);
                translate([2.0, 2.0, -0.5])
                    cube([CARTRIDGE_BASE_L - 11.0, 48.0, 2.8]);
            }
        }
    }

    // 5. Flush Sealing Top Lid (Graphite Grey PA12)
    color("dimgray", exploded ? 0.95 : 0.85)
        translate([3.0, (CARTRIDGE_BASE_W - 52.0)/2.0, z_lid])
            cartridge_dry_box_lid();

    // 6. 4x M2 Stainless Steel Countersunk Screws
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

// Standalone assembly render (shown exploded/open by default so storage cavity is visible)
cartridge_blindkassette_assembly(exploded = true);
