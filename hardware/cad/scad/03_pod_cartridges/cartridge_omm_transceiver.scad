// =============================================================================
// OpenMotorBridge - Satellite Pod: OMM Rear Transceiver Cartridge Assembly
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_omm_transceiver.scad
// Description: Assembly preview of the Rear Pod 3 Transceiver.
//              Uses the exact same Universal Base Sled (cartridge_base_sled)
//              with the 70x48mm Rear Pod 3 PCBA mounted on the 4x M2.5 standoffs.
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <00_base_sled.scad>;
use <../00_common/dummies/dummy_omm_transceiver_pcb.scad>;

module cartridge_omm_transceiver_assembly(exploded = false) {
    z_pcb = exploded ? 20.0 : 5.5;

    // 1. Universal Base Sled (Anthracite PA12)
    color("darkslategray", 0.92)
        cartridge_base_sled();

    // 2. Rear Pod 3 Transceiver PCBA (70x48mm with GNSS / LoRa / Patch Antenna)
    translate([2.5, 3.0, z_pcb])
        dummy_omm_transceiver_pcb();
}

// Standalone assembly render
cartridge_omm_transceiver_assembly(exploded = false);
