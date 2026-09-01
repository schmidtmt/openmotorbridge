// =============================================================================
// OpenMotorBridge - Satellite Pod: OMM Rear Transceiver Cartridge Assembly
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_omm_transceiver.scad
// Description: Assembly of the Rear Pod 3 Transceiver Cartridge:
//              1. Universal Base Sled (cartridge_base_sled)
//              2. Rear Pod 3 Transceiver PCBA (70x48mm with GNSS / LoRa Antennas)
//              3. Solid RF-Transparent PA12 Top Cover (cartridge_insert_blindkassette)
//              4. 4x M2 Fastening Screws
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <00_base_sled.scad>;
use <parts/03_insert_blindkassette.scad>;
use <../00_common/dummies/dummy_omm_transceiver_pcb.scad>;

module cartridge_omm_transceiver_assembly(exploded = false) {
    z_pcb    = exploded ? 16.0 : 4.5;
    z_insert = exploded ? 32.0 : 9.5;
    z_screws = exploded ? 46.0 : 13.0;

    // 1. Universal Base Sled (Anthracite PA12)
    color("darkslategray", 0.92)
        cartridge_base_sled();

    // 2. Rear Pod 3 Transceiver PCBA (70x48mm)
    translate([2.5, 3.0, z_pcb])
        dummy_omm_transceiver_pcb();

    // 3. Solid RF-Transparent PA12 Top Cover (Weatherproof Seal)
    color("dimgray", 0.95)
        translate([2.5, 2.5, z_insert])
            cartridge_insert_blindkassette();

    // 4. 4x M2 Stainless Steel Fastening Screws
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

// Module alias for sled
module cartridge_omm_transceiver_sled() {
    cartridge_base_sled();
}

// Standalone assembly render
cartridge_omm_transceiver_assembly(exploded = false);
