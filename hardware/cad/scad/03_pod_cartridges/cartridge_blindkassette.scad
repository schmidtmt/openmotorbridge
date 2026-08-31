// =============================================================================
// OpenMotorBridge - Satellite Pod: Waterproof Dummy Plug Cartridge Assembly
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_blindkassette.scad
// Description: Full 2-piece assembly preview showing:
//              1. Universal Base Sled (cartridge_base_sled)
//              2. Interchangeable Blindkassette Top Lid (cartridge_insert_blindkassette)
//              3. 4x M2 Stainless Steel Countersunk Screws
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
include <00_base_sled.scad>;
include <parts/03_insert_blindkassette.scad>;

module cartridge_blindkassette_assembly(exploded = false) {
    z_insert = exploded ? 24.0 : 8.0;
    z_screws = exploded ? 36.0 : 11.0;

    // 1. Universal Base Sled (Anthracite PA12)
    color("darkslategray", 0.92)
        cartridge_base_sled(
            sled_l = CARTRIDGE_BASE_L,
            sled_w = CARTRIDGE_BASE_W,
            sled_h = 16.0,
            wall   = 2.5
        );

    // 2. Interchangeable Solid Top Lid (Graphite Grey PA12)
    color("dimgray", 0.95)
        translate([3.5, 3.5, z_insert])
            cartridge_insert_blindkassette();

    // 3. 4x M2 Stainless Steel Fastening Screws
    color("silver") {
        translate([7.0, 6.0, z_screws])
            cylinder(r=1.8, h=2.0, center=false);
        translate([CARTRIDGE_BASE_L - 9.0, 6.0, z_screws])
            cylinder(r=1.8, h=2.0, center=false);
        translate([7.0, CARTRIDGE_BASE_W - 6.0, z_screws])
            cylinder(r=1.8, h=2.0, center=false);
        translate([CARTRIDGE_BASE_L - 9.0, CARTRIDGE_BASE_W - 6.0, z_screws])
            cylinder(r=1.8, h=2.0, center=false);
    }
}

// Standalone assembly render
cartridge_blindkassette_assembly(exploded = false);
