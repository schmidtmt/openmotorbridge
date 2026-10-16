// =============================================================================
// OpenMotorBridge - Satellite Pod: Waterproof Blindkassette (IP67 Dry Box)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_blindkassette.scad
// Description: Waterproof dummy plug & dry storage cassette:
//              - Full interior usable as watertight storage (spare key, documents, fuses)
//              - Perimeter high-visibility silicone sealing gasket
//              - Flush-sealing top lid with stainless steel M2 countersunk screws
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <00_base_sled.scad>;
use <parts/03_insert_blindkassette.scad>;

module cartridge_blindkassette_assembly(exploded = false) {
    z_gasket = exploded ? 26.0 : 24.5;
    z_insert = exploded ? 36.0 : 25.5;
    z_screws = exploded ? 46.0 : 28.5;

    // 1. Universal Base Sled (Anthracite PA12)
    color("darkslategray", 0.92)
        cartridge_base_sled(
            sled_l     = CARTRIDGE_BASE_L,
            sled_w     = CARTRIDGE_BASE_W,
            sled_h     = CARTRIDGE_BASE_H,
            wall       = 2.5,
            show_latch = true
        );

    // 2. High-Visibility Silicone Sealing Gasket (Neon Orange)
    color([1.0, 0.45, 0.1, 0.9]) {
        translate([3.5, 3.5, z_gasket]) {
            difference() {
                cube([CARTRIDGE_BASE_L - 7.0, CARTRIDGE_BASE_W - 7.0, 1.8]);
                translate([2.0, 2.0, -0.5])
                    cube([CARTRIDGE_BASE_L - 11.0, CARTRIDGE_BASE_W - 11.0, 2.8]);
            }
        }
    }

    // 3. Interchangeable Flush Top Lid (Graphite Grey PA12)
    color("dimgray", 0.95)
        translate([2.5, 2.5, z_insert])
            cartridge_insert_blindkassette();

    // 4. 4x M2 Stainless Steel Countersunk Screws
    color("silver") {
        translate([6.0, 6.0, z_screws])
            cylinder(r=1.8, h=2.0, center=false, $fn=16);
        translate([CARTRIDGE_BASE_L - 7.0, 6.0, z_screws])
            cylinder(r=1.8, h=2.0, center=false, $fn=16);
        translate([6.0, CARTRIDGE_BASE_W - 6.0, z_screws])
            cylinder(r=1.8, h=2.0, center=false, $fn=16);
        translate([CARTRIDGE_BASE_L - 7.0, CARTRIDGE_BASE_W - 6.0, z_screws])
            cylinder(r=1.8, h=2.0, center=false, $fn=16);
    }
}

// Standalone assembly render
cartridge_blindkassette_assembly(exploded = false);
