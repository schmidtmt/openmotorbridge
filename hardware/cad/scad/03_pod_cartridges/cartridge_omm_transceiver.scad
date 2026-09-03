// =============================================================================
// OpenMotorBridge - Satellite Pod: OMM Rear Transceiver Cartridge Assembly
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_omm_transceiver.scad
// Description: Assembly of the Rear Pod 3 Transceiver Cartridge:
//              1. Universal Base Sled (cartridge_base_sled, 100% identical)
//              2. Compact Rear Pod 3 Transceiver PCBA (55x48mm with U.FL jacks)
//              3. Modular OMM Antenna Bracket (holds GNSS patch, LoRa FPC, SMA coax)
//              4. Solid RF-Transparent PA12 Top Cover (cartridge_insert_blindkassette)
//              5. M2 Fastening Screws
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <00_base_sled.scad>;
use <parts/03_insert_blindkassette.scad>;
use <parts/04_antenna_bracket_omm.scad>;
use <../00_common/dummies/dummy_omm_transceiver_pcb.scad>;

module cartridge_omm_transceiver_assembly(exploded = false) {
    z_pcb     = exploded ? 16.0 : 4.5;
    z_bracket = exploded ? 24.0 : 4.5;
    z_insert  = exploded ? 36.0 : 9.5;
    z_screws  = exploded ? 48.0 : 13.0;

    // 1. Universal Base Sled (Anthracite PA12 - 100% Identical for All Pods)
    color("darkslategray", 0.92)
        cartridge_base_sled();

    // 2. Compact Rear Pod 3 Transceiver PCBA (55x48mm in front bay X = 1.5 .. 56.5 mm)
    translate([1.5, (CARTRIDGE_BASE_W - 48.0)/2.0, z_pcb])
        dummy_omm_transceiver_pcb();

    // 3. Modular OMM Antenna Bracket (X = 57.0 .. 109.0 mm in rear bay)
    color("steelblue", 0.95)
        translate([57.0, (CARTRIDGE_BASE_W - 52.0)/2.0, z_bracket])
            omm_antenna_bracket();

    // 4. Solid RF-Transparent PA12 Top Cover (Weatherproof Seal)
    color("dimgray", 0.95)
        translate([2.5, 2.5, z_insert])
            cartridge_insert_blindkassette();

    // 5. 4x M2 Stainless Steel Fastening Screws (Corner Posts)
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
