// =============================================================================
// OpenMotorBridge - Satellite Pod: Cardo Packtalk Edge Modular Cartridge Assembly
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_cardo.scad
// Description: Full 2-piece assembly preview showing:
//              1. Universal Base Sled (cartridge_base_sled)
//              2. Carrier PCB Assembly (dummy_adapter_pcb) in lower chamber
//              3. Interchangeable Cardo Insert (cartridge_insert_cardo)
//              4. 4x M2 Stainless Steel Countersunk Screws
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <00_base_sled.scad>;
use <parts/02_insert_cardo.scad>;
use <../00_common/dummies/dummy_adapter_pcb.scad>;

module cartridge_cardo_assembly(exploded = false) {
    z_pcb    = exploded ? 16.0 : 5.0;
    z_insert = exploded ? 34.0 : 8.0;
    z_screws = exploded ? 46.0 : 10.0;

    // 1. Universal Base Sled (Anthracite PA12) with visible magnetic lock latch
    color("darkslategray", 0.92)
        cartridge_base_sled(
            sled_l     = CARTRIDGE_BASE_L,
            sled_w     = CARTRIDGE_BASE_W,
            sled_h     = CARTRIDGE_BASE_H,
            wall       = 2.5,
            show_latch = true
        );

    // 2. Carrier PCB (Green FR4 + Gold Pads + Components aligned to front leading edge)
    translate([1.5, (CARTRIDGE_BASE_W - 25.0)/2.0, z_pcb])
        dummy_adapter_pcb();

    // 3. Interchangeable Cardo AirMount Insert (Slate Grey PA12)
    color("slategray", 0.95)
        translate([2.5, 2.5, z_insert])
            cartridge_insert_cardo();

    // 4. 4x M2 Stainless Steel Fastening Screws
    color("silver") {
        translate([6.0, 6.0, z_screws])
            cylinder(r=1.8, h=2.0, center=false);
        translate([CARTRIDGE_BASE_L - 7.0, 6.0, z_screws])
            cylinder(r=1.8, h=2.0, center=false);
        translate([6.0, CARTRIDGE_BASE_W - 6.0, z_screws])
            cylinder(r=1.8, h=2.0, center=false);
        translate([CARTRIDGE_BASE_L - 7.0, CARTRIDGE_BASE_W - 6.0, z_screws])
            cylinder(r=1.8, h=2.0, center=false);
    }

    // 5. Dual N52 Neodymium AirMount Permanent Magnets (Ø 8.0 x 3.0 mm, Glanzvernickelt)
    color("silver") {
        translate([29.5, 29.0, z_insert + 2.8])
            cylinder(r=4.0, h=3.0, center=false, $fn=32);
        translate([89.5, 29.0, z_insert + 2.8])
            cylinder(r=4.0, h=3.0, center=false, $fn=32);
    }

    // 6. 5-Pin Gold-Plated Spring Pogo Contact Array (Ø 1.5 mm, vergoldet)
    color("gold") {
        for (i = [-2:2]) {
            translate([60.5 + i * 2.54, 29.0, z_insert + 2.0]) {
                cylinder(r=0.9, h=3.5, center=false, $fn=16);
                translate([0, 0, 3.5])
                    sphere(r=0.9, $fn=16);
            }
        }
    }
}

// Standalone assembly render
cartridge_cardo_assembly(exploded = false);
