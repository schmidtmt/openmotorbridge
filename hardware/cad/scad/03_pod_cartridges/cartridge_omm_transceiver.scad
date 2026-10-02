// =============================================================================
// OpenMotorBridge - Satellite Pod: OMM 2.4 GHz UCS Cartridge Assembly
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_omm_transceiver.scad
// Description: Assembly of the OMM 2.4 GHz UCS (Universal Communication Solution)
//              interchangeable cartridge:
//              1. Universal Base Sled (cartridge_base_sled, 100% identical)
//              2. Carrier PCBA 03 (35x25mm with Mill-Max DC pads & DW3110 UWB)
//              3. OMM 2.4 GHz UCS Cradle Insert (cartridge_insert_omm_ucs)
//              4. OMM 2.4 GHz Transceiver Module (with 600 mAh LiPo & USB-C)
//              5. 4x M2 Fastening Screws
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <00_base_sled.scad>;
use <parts/06_insert_omm_ucs.scad>;
use <parts/omm_ucs_module.scad>;
use <../00_common/dummies/dummy_adapter_pcb.scad>;

module cartridge_omm_transceiver_assembly(exploded = false) {
    z_pcb    = exploded ? 16.0 : 5.0;
    z_insert = exploded ? 34.0 : 8.0;
    z_module = exploded ? 46.0 : 10.5;
    z_screws = exploded ? 58.0 : 14.0;

    // 1. Universal Base Sled (Anthracite PA12 - 100% Identical for All Pods)
    color("darkslategray", 0.92)
        cartridge_base_sled(show_latch = true);

    // 2. Carrier PCB PCBA 03 (35 x 25 mm with 2-pin Mill-Max DC Pads & DW3110 UWB)
    translate([1.5, (CARTRIDGE_BASE_W - 25.0)/2.0, z_pcb])
        dummy_adapter_pcb();

    // 3. OMM 2.4 GHz UCS PA12 Cradle Insert
    color("slategray", 0.95)
        translate([2.5, 2.5, z_insert])
            cartridge_insert_omm_ucs();

    // 4. OMM 2.4 GHz UCS Autonomous Transceiver Module Assembly
    translate([20.0, (CARTRIDGE_BASE_W - 36.0)/2.0, z_module])
        omm_ucs_module_assembly(exploded = false);

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
